from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .estoque import cadastrar_estoque
from .models import Estoque, PedidoSangue, Usuario
from .validacao_hemocentro import aprovar_hemocentro


class VisualizacaoPublicaTests(TestCase):
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
        self.admin = self.criar_usuario(
            email="admin@visualizacao.test",
            nome="Administrador",
            perfil=Usuario.Perfil.ADMINISTRADOR,
        )

        self.hemocentro = self.criar_usuario(
            email="hemocentro@visualizacao.test",
            nome="Hemocentro Central",
            perfil=Usuario.Perfil.HEMOCENTRO,
            cidade="Muzambinho",
            estado="MG",
        )

        aprovar_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.admin,
        )

        self.hemocentro.refresh_from_db()

        self.hemocentro_pendente = self.criar_usuario(
            email="pendente@visualizacao.test",
            nome="Hemocentro Pendente",
            perfil=Usuario.Perfil.HEMOCENTRO,
            cidade="Alfenas",
            estado="MG",
        )

    def pedido(self, *, status, tipo="O-", urgencia="ALTA"):
        return PedidoSangue.objects.create(
            nome_solicitante="Solicitante",
            contato="solicitante@visualizacao.test",
            hemocentro_destino=self.hemocentro,
            para_quem=PedidoSangue.ParaQuem.MIM,
            titulo=f"Pedido urgente de sangue {tipo}",
            tipo_sanguineo=tipo,
            urgencia=urgencia,
            cidade="Muzambinho",
            descricao=(
                "Necessidade de doadores para atendimento hospitalar."
            ),
            status=status,
            publicado_em=(
                timezone.now()
                if status == PedidoSangue.Status.PUBLICADA
                else None
            ),
        )

    def test_consulta_de_pedidos_aplica_filtros_e_oculta_nao_publicados(
        self,
    ):
        publicado = self.pedido(
            status=PedidoSangue.Status.PUBLICADA,
        )

        pendente = self.pedido(
            status=PedidoSangue.Status.ENVIADA,
            tipo="A+",
        )

        resposta = self.client.get(
            reverse("accounts:consultar_pedidos"),
            {
                "tipo_sanguineo": "O-",
                "urgencia": "ALTA",
                "cidade": "Muzambinho",
                "hemocentro": "Central",
                "data": date.today().isoformat(),
                "status": "PUBLICADA",
            },
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, publicado.titulo)
        self.assertNotContains(resposta, pendente.titulo)

        resposta = self.client.get(
            reverse("accounts:consultar_pedidos"),
            {
                "status": "ENVIADA",
            },
        )

        self.assertNotContains(resposta, publicado.titulo)

    def test_consulta_de_pedidos_nao_exibe_destino_nao_aprovado(self):
        pedido = PedidoSangue.objects.create(
            nome_solicitante="Solicitante",
            contato="solicitante@visualizacao.test",
            hemocentro_destino=self.hemocentro_pendente,
            para_quem=PedidoSangue.ParaQuem.MIM,
            titulo="Pedido de destino pendente",
            tipo_sanguineo="O-",
            urgencia=PedidoSangue.Urgencia.MEDIA,
            cidade="Alfenas",
            descricao=(
                "Pedido que não deve aparecer na consulta pública."
            ),
            status=PedidoSangue.Status.PUBLICADA,
        )

        resposta = self.client.get(
            reverse("accounts:consultar_pedidos")
        )

        self.assertNotContains(resposta, pedido.titulo)

    def test_consulta_de_estoques_filtra_por_tipo_situacao_e_busca(
        self,
    ):
        cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="O-",
            quantidade_bolsas=2,
            nivel_minimo=10,
            nivel_critico=5,
        )

        cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="A+",
            quantidade_bolsas=20,
            nivel_minimo=10,
            nivel_critico=5,
        )

        Estoque.objects.create(
            hemocentro=self.hemocentro_pendente,
            tipo_sanguineo="B+",
            quantidade_bolsas=10,
            nivel_minimo=10,
            nivel_critico=5,
        )

        resposta = self.client.get(
            reverse("accounts:estoque_publico"),
            {
                "tipo_sanguineo": "O-",
                "situacao": "CRITICO",
                "busca": "Central",
            },
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "O-")
        self.assertContains(resposta, "Crítico")
        self.assertNotContains(resposta, "20 bolsas")
        self.assertNotContains(resposta, "Hemocentro Pendente")

    def test_consulta_de_estoques_preserva_parametros_antigos(self):
        cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="O-",
            quantidade_bolsas=2,
            nivel_minimo=10,
            nivel_critico=5,
        )

        resposta = self.client.get(
            reverse("accounts:estoque_publico"),
            {
                "q": "Muzambinho",
                "tipo": "O-",
            },
        )

        self.assertContains(resposta, "O-")