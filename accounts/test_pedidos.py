from django.test import TestCase
from django.urls import reverse

from .forms import PedidoSangueForm
from .models import PedidoSangue, Usuario
from .validacao_hemocentro import aprovar_hemocentro


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
        self.doador = self.criar_usuario(
            email="doador@elo.test",
            nome="Doador Elo",
            perfil=Usuario.Perfil.DOADOR,
        )
        self.receptor = self.criar_usuario(
            email="receptor@elo.test",
            nome="Receptor Elo",
            perfil=Usuario.Perfil.RECEPTOR,
        )
        self.observador = self.criar_usuario(
            email="observador@elo.test",
            nome="Familiar Elo",
            perfil=Usuario.Perfil.OBSERVADOR,
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
            "para_quem": "OUTRA_PESSOA",
            "tipo_sanguineo": "O-",
            "hemocentro": self.hemocentro.pk,
            "urgencia": "CRITICO",
            "nome_paciente": "Paciente de exemplo",
            "descricao": (
                "Precisamos de doadores para auxiliar um paciente em atendimento."
            ),
        }
        dados.update(alteracoes)
        return dados

    def test_formulario_pergunta_para_quem_e_lista_apenas_hemocentros_aprovados(self):
        form = PedidoSangueForm()

        self.assertIn("para_quem", form.fields)
        self.assertEqual(
            list(form.fields["hemocentro"].queryset),
            [self.hemocentro],
        )
        self.assertNotIn("cidade", form.fields)

    def test_doador_publica_para_outra_pessoa_e_salva_pendente(self):
        self.client.force_login(self.doador)

        resposta = self.client.post(
            reverse("accounts:pedido_publicar"),
            self.dados_validos(),
        )

        pedido = PedidoSangue.objects.get()
        self.assertRedirects(
            resposta,
            reverse(
                "accounts:pedido_detalhe",
                kwargs={"id_pedido": pedido.pk},
            ),
        )
        self.assertEqual(pedido.solicitante, self.doador)
        self.assertEqual(pedido.para_quem, PedidoSangue.ParaQuem.OUTRA_PESSOA)
        self.assertEqual(pedido.hemocentro, self.hemocentro)
        self.assertEqual(pedido.cidade, "Muzambinho")
        self.assertEqual(pedido.status, PedidoSangue.Status.PENDENTE)

    def test_receptor_pode_publicar_para_si(self):
        self.client.force_login(self.receptor)

        resposta = self.client.post(
            reverse("accounts:pedido_publicar"),
            self.dados_validos(
                para_quem="MIM",
                nome_paciente="",
            ),
        )

        self.assertEqual(resposta.status_code, 302)
        pedido = PedidoSangue.objects.get()
        self.assertEqual(pedido.solicitante, self.receptor)
        self.assertEqual(pedido.para_quem, PedidoSangue.ParaQuem.MIM)

    def test_observador_pode_publicar_como_familiar_ou_solicitante(self):
        self.client.force_login(self.observador)

        resposta = self.client.post(
            reverse("accounts:pedido_publicar"),
            self.dados_validos(),
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(
            PedidoSangue.objects.get().solicitante,
            self.observador,
        )

    def test_administrador_pode_acessar_publicacao_de_pedido(self):
        self.client.force_login(self.administrador)

        resposta = self.client.get(reverse("accounts:pedido_publicar"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Publicar pedido de sangue")
        self.assertFalse(PedidoSangue.objects.exists())

    def test_visitante_precisa_entrar(self):
        resposta = self.client.get(reverse("accounts:pedido_publicar"))

        self.assertRedirects(
            resposta,
            f"{reverse('accounts:login')}?next={reverse('accounts:pedido_publicar')}",
        )

    def test_formulario_rejeita_descricao_curta(self):
        form = PedidoSangueForm(self.dados_validos(descricao="Curto"))

        self.assertFalse(form.is_valid())
        self.assertIn("descricao", form.errors)

    def test_pedido_pendente_nao_pode_ser_escolhido_como_destino(self):
        form = PedidoSangueForm(
            self.dados_validos(hemocentro=self.hemocentro_pendente.pk)
        )

        self.assertFalse(form.is_valid())
        self.assertIn("hemocentro", form.errors)

    def test_detalhe_so_pode_ser_visto_pelo_solicitante(self):
        pedido = PedidoSangue.objects.create(
            solicitante=self.doador,
            para_quem=PedidoSangue.ParaQuem.OUTRA_PESSOA,
            hemocentro=self.hemocentro,
            tipo_sanguineo="O-",
            cidade="Muzambinho",
            urgencia=PedidoSangue.Urgencia.NORMAL,
            descricao="Descrição suficiente para o pedido de sangue.",
        )
        self.client.force_login(self.receptor)

        resposta = self.client.get(
            reverse(
                "accounts:pedido_detalhe",
                kwargs={"id_pedido": pedido.pk},
            )
        )

        self.assertEqual(resposta.status_code, 404)
