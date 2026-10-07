from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from .models import ConsentimentoLGPD, Notificacao, PedidoSangue, Triagem, Usuario
from .forms import CadastroUsuarioForm
from .triagem_servico import atualizar_tipo_sanguineo_do_usuario
from .validacao_hemocentro import aprovar_hemocentro
from .validacao_pedido import aprovar_pedido, criar_pedido_pendente


class FluxoCadastroTriagemPedidosTests(TestCase):
    def usuario(self, email, perfil, **extras):
        return Usuario.objects.create_user(
            email=email,
            password="SenhaForte123!",
            nome=extras.pop("nome", perfil.title()),
            perfil=perfil,
            **extras,
        )

    def setUp(self):
        self.admin = self.usuario("admin@elo.test", Usuario.Perfil.ADMINISTRADOR)
        self.doador = self.usuario("doador@elo.test", Usuario.Perfil.DOADOR)
        self.receptor = self.usuario("receptor@elo.test", Usuario.Perfil.RECEPTOR)
        self.observador = self.usuario("observador@elo.test", Usuario.Perfil.OBSERVADOR)
        self.hemocentro = self.usuario(
            "hemocentro@elo.test",
            Usuario.Perfil.HEMOCENTRO,
            cidade="Belo Horizonte",
        )
        aprovar_hemocentro(hemocentro=self.hemocentro, admin=self.admin)
        self.hemocentro.refresh_from_db()

    def dados_solicitacao(self):
        return {
            "nome_solicitante": "Pessoa solicitante",
            "contato": "(31) 99999-0000",
            "para_quem": PedidoSangue.ParaQuem.MIM,
            "hemocentro_destino": self.hemocentro.pk,
            "titulo": "Necessidade de sangue",
            "tipo_sanguineo": "O-",
            "urgencia": PedidoSangue.Urgencia.MEDIA,
            "cidade": "Belo Horizonte",
            "nome_paciente": "Paciente",
            "descricao": "Necessidade de doadores para atendimento hospitalar.",
            "justificativa_urgencia": "",
            "informacoes_complementares": "Retorno pelo contato informado.",
        }

    def test_cadastro_nao_permite_admin_e_exige_consentimento(self):
        resposta = self.client.post(
            reverse("accounts:cadastro"),
            {
                "nome": "Nova pessoa",
                "email": "nova@elo.test",
                "perfil": Usuario.Perfil.OBSERVADOR,
                "password1": "SenhaForte123!",
                "password2": "SenhaForte123!",
                "aceite_lgpd": "",
            },
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(Usuario.objects.filter(email="nova@elo.test").exists())

        self.assertNotIn(
            Usuario.Perfil.ADMINISTRADOR,
            dict(CadastroUsuarioForm().fields["perfil"].choices),
        )

    def test_cadastro_valido_grava_senha_hash_e_consentimento(self):
        resposta = self.client.post(
            reverse("accounts:cadastro"),
            {
                "nome": "Doador cadastrado",
                "email": "cadastro@elo.test",
                "perfil": Usuario.Perfil.DOADOR,
                "cpf": "12345678901",
                "data_nascimento": "1990-01-01",
                "password1": "SenhaForte123!",
                "password2": "SenhaForte123!",
                "aceite_lgpd": "on",
            },
        )
        self.assertRedirects(resposta, reverse("accounts:dashboard"))
        usuario = Usuario.objects.get(email="cadastro@elo.test")
        self.assertTrue(usuario.check_password("SenhaForte123!"))
        self.assertNotEqual(usuario.password, "SenhaForte123!")
        self.assertTrue(
            ConsentimentoLGPD.objects.filter(
                usuario=usuario,
                tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL,
                aceito=True,
            ).exists()
        )

    def test_login_bloqueia_conta_suspensa(self):
        self.doador.suspensa = True
        self.doador.save(update_fields=["suspensa"])
        resposta = self.client.post(
            reverse("accounts:login"),
            {"username": self.doador.email, "password": "SenhaForte123!"},
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_triagem_exige_aceite_explicito(self):
        self.client.force_login(self.doador)
        url = reverse("accounts:triagem_iniciar", kwargs={"modalidade": "extensa"})

        self.client.post(url)
        self.assertFalse(Triagem.objects.filter(usuario=self.doador).exists())

        resposta = self.client.post(url, {"aceite_termo": "on"})
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(
            ConsentimentoLGPD.objects.filter(
                usuario=self.doador,
                tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM,
            ).exists()
        )

    def test_solicitacao_nao_publica_e_hemocentro_publica(self):
        resposta = self.client.post(
            reverse("accounts:pedido_publicar"),
            self.dados_solicitacao(),
        )
        self.assertEqual(resposta.status_code, 302)
        pedido = PedidoSangue.objects.get()
        self.assertEqual(pedido.status, PedidoSangue.Status.ENVIADA)

        with self.assertRaises(PermissionDenied):
            aprovar_pedido(pedido=pedido, moderador=self.admin)

        aprovar_pedido(pedido=pedido, moderador=self.hemocentro)
        pedido.refresh_from_db()
        self.assertEqual(pedido.status, PedidoSangue.Status.PUBLICADA)
        self.assertEqual(pedido.publicado_por, self.hemocentro)

    def test_observador_pode_solicitar_mas_nao_analisar(self):
        self.client.force_login(self.observador)
        resposta = self.client.get(reverse("accounts:painel_pedidos_hemocentro"))
        self.assertEqual(resposta.status_code, 403)

    def test_receptor_acompanha_somente_suas_solicitacoes(self):
        pedido = criar_pedido_pendente(
            dados={**self.dados_solicitacao(), "contato": "receptor@elo.test"},
            solicitante=self.receptor,
        )
        self.client.force_login(self.receptor)
        resposta = self.client.get(reverse("accounts:minhas_solicitacoes"))
        self.assertContains(resposta, str(pedido.pk))
        self.assertNotContains(resposta, "outra-pessoa")

    def test_tipo_sanguineo_confirmado_nao_e_sobrescrito_pela_triagem(self):
        self.doador.tipo_sanguineo = "A+"
        self.doador.tipo_sanguineo_confirmado = True
        self.doador.save(update_fields=["tipo_sanguineo", "tipo_sanguineo_confirmado"])
        triagem = Triagem.objects.create(usuario=self.doador)

        atualizar_tipo_sanguineo_do_usuario(
            triagem,
            {"codigos": ["O+"]},
        )

        self.doador.refresh_from_db()
        self.assertEqual(self.doador.tipo_sanguineo, "A+")

    def test_publicacao_notifica_somente_doador_apto_compativel(self):
        self.doador.tipo_sanguineo = "O-"
        self.doador.save(update_fields=["tipo_sanguineo"])
        Triagem.objects.create(
            usuario=self.doador,
            status=Triagem.Status.CONCLUIDA,
            resultado=Triagem.Resultado.APTO,
        )
        pedido = criar_pedido_pendente(
            dados=self.dados_solicitacao(),
            solicitante=self.receptor,
        )

        aprovar_pedido(pedido=pedido, moderador=self.hemocentro)

        self.assertTrue(
            Notificacao.objects.filter(
                usuario=self.doador,
                pedido=pedido,
                tipo=Notificacao.Tipo.PEDIDO_COMPATIVEL,
            ).exists()
        )
