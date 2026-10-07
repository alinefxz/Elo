from django.test import TestCase
from django.urls import reverse

from .forms import PedidoSangueForm
from .models import PedidoSangue, Usuario, ValidacaoPedido
from .validacao_hemocentro import aprovar_hemocentro
from .validacao_pedido import aprovar_pedido, criar_pedido_pendente


class PedidoSangueTests(TestCase):
    def criar_usuario(self, *, email, nome, perfil, cidade="", estado=""):
        return Usuario.objects.create_user(
            email=email,
            password="SenhaForte123!",
            nome=nome,
            perfil=perfil,
            cidade=cidade,
            estado=estado,
        )

    def setUp(self):
        self.receptor = self.criar_usuario(
            email="receptor@elo.test",
            nome="Receptor Elo",
            perfil=Usuario.Perfil.RECEPTOR,
        )
        self.doador = self.criar_usuario(
            email="doador@elo.test",
            nome="Doador Elo",
            perfil=Usuario.Perfil.DOADOR,
        )
        self.administrador = self.criar_usuario(
            email="admin@elo.test",
            nome="Administrador Elo",
            perfil=Usuario.Perfil.ADMINISTRADOR,
        )
        self.hemocentro = self.criar_usuario(
            email="hemocentro@elo.test",
            nome="Hemocentro Muzambinho",
            perfil=Usuario.Perfil.HEMOCENTRO,
            cidade="Muzambinho",
            estado="MG",
        )
        aprovar_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.administrador,
        )
        self.hemocentro.refresh_from_db()

        self.hemocentro_pendente = self.criar_usuario(
            email="pendente@elo.test",
            nome="Hemocentro Pendente",
            perfil=Usuario.Perfil.HEMOCENTRO,
            cidade="Alfenas",
            estado="MG",
        )

    def dados_validos(self, **alteracoes):
        dados = {
            "nome_solicitante": "Solicitante de exemplo",
            "contato": "receptor@elo.test",
            "para_quem": PedidoSangue.ParaQuem.OUTRA_PESSOA,
            "hemocentro_destino": self.hemocentro.pk,
            "titulo": "Doacao para paciente internado",
            "tipo_sanguineo": "O-",
            "urgencia": PedidoSangue.Urgencia.BAIXA,
            "cidade": "Muzambinho",
            "nome_paciente": "Paciente de exemplo",
            "descricao": (
                "Precisamos de doadores para auxiliar um paciente internado."
            ),
            "justificativa_urgencia": "",
            "informacoes_complementares": "Retorno por telefone.",
        }
        dados.update(alteracoes)
        return dados

    def test_formulario_lista_apenas_hemocentros_aprovados(self):
        form = PedidoSangueForm()

        self.assertIn("para_quem", form.fields)
        self.assertIn("nome_paciente", form.fields)
        self.assertEqual(
            list(form.fields["hemocentro_destino"].queryset),
            [self.hemocentro],
        )

    def test_receptor_cria_solicitacao_enviada(self):
        self.client.force_login(self.receptor)

        resposta = self.client.post(
            reverse("accounts:pedido_publicar"),
            self.dados_validos(),
        )

        self.assertRedirects(resposta, reverse("accounts:minhas_solicitacoes"))
        pedido = PedidoSangue.objects.get()
        self.assertEqual(pedido.solicitante, self.receptor)
        self.assertEqual(pedido.hemocentro_destino, self.hemocentro)
        self.assertEqual(
            pedido.status,
            PedidoSangue.Status.ENVIADA,
        )

    def test_doador_pode_enviar_solicitacao(self):
        self.client.force_login(self.doador)

        resposta = self.client.post(
            reverse("accounts:pedido_publicar"),
            self.dados_validos(),
        )

        self.assertRedirects(resposta, reverse("accounts:minhas_solicitacoes"))
        self.assertTrue(PedidoSangue.objects.exists())

    def test_visitante_pode_enviar_formulario(self):
        resposta = self.client.get(reverse("accounts:pedido_publicar"))
        self.assertEqual(resposta.status_code, 200)

    def test_formulario_rejeita_descricao_curta(self):
        form = PedidoSangueForm(self.dados_validos(descricao="Curto"))

        self.assertFalse(form.is_valid())
        self.assertIn("descricao", form.errors)

    def test_formulario_exige_email_no_contato(self):
        form_invalido = PedidoSangueForm(
            self.dados_validos(contato="(31) 99999-0000")
        )
        self.assertFalse(form_invalido.is_valid())
        self.assertIn("contato", form_invalido.errors)

        form_valido = PedidoSangueForm(
            self.dados_validos(contato="  Receptor@Elo.Test ")
        )
        self.assertTrue(form_valido.is_valid())
        self.assertEqual(
            form_valido.cleaned_data["contato"],
            "receptor@elo.test",
        )

    def test_formulario_rejeita_hemocentro_pendente(self):
        form = PedidoSangueForm(
            self.dados_validos(
                hemocentro_destino=self.hemocentro_pendente.pk,
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn("hemocentro_destino", form.errors)

    def test_urgencia_critica_exige_justificativa(self):
        form = PedidoSangueForm(
            self.dados_validos(
                urgencia=PedidoSangue.Urgencia.CRITICA,
                justificativa_urgencia="Curta",
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn("justificativa_urgencia", form.errors)

    def test_hemocentro_aprova_pedido_e_registra_historico(self):
        self.client.force_login(self.receptor)
        self.client.post(
            reverse("accounts:pedido_publicar"),
            self.dados_validos(),
        )
        pedido = PedidoSangue.objects.get()

        validacao = aprovar_pedido(
            pedido=pedido,
            moderador=self.hemocentro,
            motivo="Dados conferidos pelo administrador.",
        )

        pedido.refresh_from_db()
        self.assertEqual(pedido.status, PedidoSangue.Status.PUBLICADA)
        self.assertEqual(
            validacao.status_validacao,
            ValidacaoPedido.StatusValidacao.APROVADO,
        )
        self.assertEqual(pedido.validacoes.count(), 1)

    def test_admin_moderar_pedido_nao_publica(self):
        pedido = criar_pedido_pendente(
            dados=self.dados_validos(),
            solicitante=self.receptor,
        )

        self.client.force_login(self.administrador)

        resposta = self.client.get(
            reverse("accounts:painel_validacao_pedidos")
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, str(pedido.pk))

        resposta = self.client.post(
            reverse(
                "accounts:marcar_pedido_suspeito",
                kwargs={"id_pedido": pedido.pk},
            ),
            {"motivo": "Há solicitação semelhante para o mesmo destino."},
        )

        self.assertRedirects(
            resposta,
            reverse("accounts:painel_validacao_pedidos"),
        )
        pedido.refresh_from_db()
        self.assertEqual(
            pedido.status,
            PedidoSangue.Status.EM_ANALISE,
        )
        self.assertFalse(pedido.publicado_por_id)
        self.assertEqual(
            pedido.validacoes.latest("data_validacao").status_validacao,
            ValidacaoPedido.StatusValidacao.SUSPEITO,
        )

    def test_hemocentro_nao_acessa_moderacao_administrativa(self):
        self.client.force_login(self.hemocentro)

        resposta = self.client.get(
            reverse("accounts:painel_validacao_pedidos")
        )

        self.assertEqual(resposta.status_code, 403)
