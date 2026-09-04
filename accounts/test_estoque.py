"""
Testes automatizados do estoque (UC_29 - Cadastrar Estoque e
UC_30 - Atualizar Estoque).

Cobrem:
- calculo do status (critico/baixo/estavel);
- cadastro de estoque, incluindo bloqueios (nao aprovado, duplicado,
  niveis incoerentes);
- movimentacoes de entrada, saida e ajuste, incluindo bloqueios (saida
  maior que o disponivel, estoque de outro hemocentro);
- geracao de historico (EstoqueMovimentacao) e auditoria
  (AuditoriaAcaoCritica) a cada operacao;
- as views, por meio do client de testes do Django.

Execute com: ``python manage.py test accounts.test_estoque``.
"""

from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase
from django.urls import reverse

from .estoque import (
    calcular_status_calculado,
    cadastrar_estoque,
    registrar_movimentacao_estoque,
)
from .models import AuditoriaAcaoCritica, Estoque, EstoqueMovimentacao, Usuario
from .validacao_hemocentro import aprovar_hemocentro


class EstoqueTestsBase(TestCase):
    """Prepara um administrador e Hemocentros usados pelos testes."""

    def criar_usuario(self, *, email, nome, perfil):
        return Usuario.objects.create_user(
            email=email,
            password="SenhaForte123!",
            nome=nome,
            perfil=perfil,
        )

    def setUp(self):
        self.admin = self.criar_usuario(
            email="admin@elo.test",
            nome="Administrador Elo",
            perfil=Usuario.Perfil.ADMINISTRADOR,
        )

        self.hemocentro = self.criar_usuario(
            email="hemocentro@elo.test",
            nome="Hemocentro Elo",
            perfil=Usuario.Perfil.HEMOCENTRO,
        )
        aprovar_hemocentro(hemocentro=self.hemocentro, admin=self.admin)
        self.hemocentro.refresh_from_db()

        self.hemocentro_pendente = self.criar_usuario(
            email="pendente@elo.test",
            nome="Hemocentro Pendente",
            perfil=Usuario.Perfil.HEMOCENTRO,
        )

        self.doador = self.criar_usuario(
            email="doador@elo.test",
            nome="Doador Elo",
            perfil=Usuario.Perfil.DOADOR,
        )


class CalcularStatusCalculadoTests(TestCase):
    """Testa a regra pura de calculo de status, sem tocar o banco."""

    def test_quantidade_igual_ao_critico_e_critico(self):
        self.assertEqual(
            calcular_status_calculado(
                quantidade_bolsas=5, nivel_minimo=10, nivel_critico=5
            ),
            Estoque.StatusCalculado.CRITICO,
        )

    def test_quantidade_abaixo_do_critico_e_critico(self):
        self.assertEqual(
            calcular_status_calculado(
                quantidade_bolsas=0, nivel_minimo=10, nivel_critico=5
            ),
            Estoque.StatusCalculado.CRITICO,
        )

    def test_quantidade_igual_ao_minimo_e_baixo(self):
        self.assertEqual(
            calcular_status_calculado(
                quantidade_bolsas=10, nivel_minimo=10, nivel_critico=5
            ),
            Estoque.StatusCalculado.BAIXO,
        )

    def test_quantidade_acima_do_minimo_e_estavel(self):
        self.assertEqual(
            calcular_status_calculado(
                quantidade_bolsas=11, nivel_minimo=10, nivel_critico=5
            ),
            Estoque.StatusCalculado.ESTAVEL,
        )


class CadastrarEstoqueTests(EstoqueTestsBase):
    """Testes principais do UC_29."""

    def test_hemocentro_aprovado_cadastra_estoque(self):
        estoque = cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="o-",  # minusculo de proposito: deve normalizar
            quantidade_bolsas=8,
            nivel_minimo=10,
            nivel_critico=5,
        )

        self.assertEqual(estoque.tipo_sanguineo, "O-")
        self.assertEqual(estoque.status_calculado, Estoque.StatusCalculado.BAIXO)

        self.assertTrue(
            AuditoriaAcaoCritica.objects.filter(
                acao=AuditoriaAcaoCritica.Acao.CADASTRO_ESTOQUE,
                usuario=self.hemocentro,
                alvo_id=str(estoque.pk),
            ).exists()
        )

    def test_hemocentro_pendente_nao_pode_cadastrar_estoque(self):
        with self.assertRaises(PermissionDenied):
            cadastrar_estoque(
                hemocentro=self.hemocentro_pendente,
                tipo_sanguineo="O+",
                nivel_minimo=10,
                nivel_critico=5,
            )

    def test_nao_permite_cadastro_duplicado(self):
        cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="A+",
            nivel_minimo=10,
            nivel_critico=5,
        )

        with self.assertRaises(ValidationError):
            cadastrar_estoque(
                hemocentro=self.hemocentro,
                tipo_sanguineo="A+",
                nivel_minimo=20,
                nivel_critico=10,
            )

    def test_nivel_critico_maior_que_minimo_gera_erro(self):
        with self.assertRaises(ValidationError):
            cadastrar_estoque(
                hemocentro=self.hemocentro,
                tipo_sanguineo="B+",
                nivel_minimo=5,
                nivel_critico=10,
            )

    def test_tipo_sanguineo_invalido_gera_erro(self):
        with self.assertRaises(ValueError):
            cadastrar_estoque(
                hemocentro=self.hemocentro,
                tipo_sanguineo="C+",
                nivel_minimo=10,
                nivel_critico=5,
            )


class RegistrarMovimentacaoEstoqueTests(EstoqueTestsBase):
    """Testes principais do UC_30."""

    def setUp(self):
        super().setUp()

        self.estoque = cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="O-",
            quantidade_bolsas=10,
            nivel_minimo=10,
            nivel_critico=5,
        )

    def test_entrada_soma_quantidade_e_recalcula_status(self):
        movimentacao = registrar_movimentacao_estoque(
            estoque=self.estoque,
            usuario_resp=self.hemocentro,
            tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
            quantidade=15,
            motivo="Doação recebida em mutirão.",
        )

        self.estoque.refresh_from_db()

        self.assertEqual(movimentacao.quantidade_anterior, 10)
        self.assertEqual(movimentacao.quantidade_movimentada, 15)
        self.assertEqual(movimentacao.quantidade_nova, 25)
        self.assertEqual(self.estoque.quantidade_bolsas, 25)
        self.assertEqual(self.estoque.status_calculado, Estoque.StatusCalculado.ESTAVEL)

    def test_saida_subtrai_quantidade(self):
        movimentacao = registrar_movimentacao_estoque(
            estoque=self.estoque,
            usuario_resp=self.hemocentro,
            tipo_movimento=EstoqueMovimentacao.TipoMovimento.SAIDA,
            quantidade=6,
            motivo="Transfusão de emergência.",
        )

        self.estoque.refresh_from_db()

        self.assertEqual(movimentacao.quantidade_nova, 4)
        self.assertEqual(self.estoque.quantidade_bolsas, 4)
        self.assertEqual(self.estoque.status_calculado, Estoque.StatusCalculado.CRITICO)

    def test_saida_maior_que_estoque_gera_erro_e_nao_altera_nada(self):
        with self.assertRaises(ValidationError):
            registrar_movimentacao_estoque(
                estoque=self.estoque,
                usuario_resp=self.hemocentro,
                tipo_movimento=EstoqueMovimentacao.TipoMovimento.SAIDA,
                quantidade=999,
            )

        self.estoque.refresh_from_db()
        self.assertEqual(self.estoque.quantidade_bolsas, 10)
        self.assertEqual(
            EstoqueMovimentacao.objects.filter(estoque=self.estoque).count(), 0
        )

    def test_ajuste_define_quantidade_absoluta_e_aceita_delta_negativo(self):
        movimentacao = registrar_movimentacao_estoque(
            estoque=self.estoque,
            usuario_resp=self.hemocentro,
            tipo_movimento=EstoqueMovimentacao.TipoMovimento.AJUSTE,
            quantidade=3,
            motivo="Contagem física apontou divergência.",
        )

        self.estoque.refresh_from_db()

        self.assertEqual(movimentacao.quantidade_anterior, 10)
        self.assertEqual(movimentacao.quantidade_movimentada, -7)
        self.assertEqual(movimentacao.quantidade_nova, 3)
        self.assertEqual(self.estoque.quantidade_bolsas, 3)

    def test_movimentacao_gera_historico_e_auditoria(self):
        registrar_movimentacao_estoque(
            estoque=self.estoque,
            usuario_resp=self.hemocentro,
            tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
            quantidade=2,
        )

        self.assertEqual(
            EstoqueMovimentacao.objects.filter(estoque=self.estoque).count(), 1
        )
        self.assertTrue(
            AuditoriaAcaoCritica.objects.filter(
                acao=AuditoriaAcaoCritica.Acao.ATUALIZACAO_ESTOQUE,
                usuario=self.hemocentro,
                alvo_id=str(self.estoque.pk),
            ).exists()
        )

    def test_outro_hemocentro_nao_pode_movimentar_estoque_alheio(self):
        outro_hemocentro = self.criar_usuario(
            email="outro@elo.test",
            nome="Outro Hemocentro",
            perfil=Usuario.Perfil.HEMOCENTRO,
        )
        aprovar_hemocentro(hemocentro=outro_hemocentro, admin=self.admin)
        outro_hemocentro.refresh_from_db()

        with self.assertRaises(PermissionDenied):
            registrar_movimentacao_estoque(
                estoque=self.estoque,
                usuario_resp=outro_hemocentro,
                tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
                quantidade=1,
            )

    def test_doador_nao_pode_movimentar_estoque(self):
        with self.assertRaises(PermissionDenied):
            registrar_movimentacao_estoque(
                estoque=self.estoque,
                usuario_resp=self.doador,
                tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
                quantidade=1,
            )


class EstoqueViewsTests(EstoqueTestsBase):
    """Testes de ponta a ponta usando o client de testes do Django."""

    def test_painel_bloqueia_hemocentro_pendente(self):
        self.client.force_login(self.hemocentro_pendente)

        resposta = self.client.get(reverse("accounts:estoque_hemocentro"))

        self.assertEqual(resposta.status_code, 403)

    def test_post_cadastra_estoque_via_view(self):
        self.client.force_login(self.hemocentro)

        resposta = self.client.post(
            reverse("accounts:cadastrar_estoque"),
            {
                "tipo_sanguineo": "AB+",
                "quantidade_bolsas": 4,
                "nivel_minimo": 10,
                "nivel_critico": 5,
            },
        )

        self.assertRedirects(resposta, reverse("accounts:estoque_hemocentro"))
        self.assertTrue(
            Estoque.objects.filter(
                hemocentro=self.hemocentro, tipo_sanguineo="AB+"
            ).exists()
        )

    def test_post_movimenta_estoque_via_view(self):
        estoque = cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="B-",
            quantidade_bolsas=5,
            nivel_minimo=10,
            nivel_critico=5,
        )

        self.client.force_login(self.hemocentro)

        resposta = self.client.post(
            reverse("accounts:atualizar_estoque", kwargs={"id_estoque": estoque.pk}),
            {
                "tipo_movimento": EstoqueMovimentacao.TipoMovimento.ENTRADA,
                "quantidade": 5,
                "motivo": "Reposição semanal.",
            },
        )

        self.assertRedirects(resposta, reverse("accounts:estoque_hemocentro"))

        estoque.refresh_from_db()
        self.assertEqual(estoque.quantidade_bolsas, 10)