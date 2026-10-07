"""
RESUMO DO ARQUIVO
=================
Testes automatizados executam o fluxo sem abrir o navegador. Cada teste usa um
banco temporario e e isolado dos demais.

Os testes abaixo verificam o minimo mais importante desta entrega:

1. cadastro cria conta, hash de senha e consentimento;
2. login aceita e-mail e senha corretos;
3. visitante acessa busca publica, estoque geral e pedidos ativos;
4. dashboard redireciona visitantes para o login;
5. perfis cadastrados recebem paineis proprios.

Execute com: ``python manage.py test``.


Os testes verificam:
- novo Hemocentro inicia como PENDENTE;
- administrador consegue aprovar, recusar ou solicitar correcao;
- cada decisao gera historico;
- usuario comum nao pode executar a decisao;
- Hemocentro nao aprovado nao consegue publicar;
- Hemocentro aprovado pode seguir para a rotina de publicacao.
"""

from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse

from .models import AuditoriaAcaoCritica, Estoque, Usuario, ValidacaoHemocentro
from .validacao_hemocentro import (
    aprovar_hemocentro,
    hemocentro_aprovado,
    recusar_hemocentro,
    solicitar_correcao_hemocentro,
    validar_publicacao_hemocentro,
)


class ValidacaoHemocentroTests(TestCase):
    """Testes principais do UC_07."""

    def criar_usuario(
        self,
        *,
        email,
        nome,
        perfil,
        is_staff=False,
        is_superuser=False,
    ):
        """Cria usuario usando o manager real do projeto."""

        return Usuario.objects.create_user(
            email=email,
            password="SenhaForte123!",
            nome=nome,
            perfil=perfil,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )

    def setUp(self):
        """Prepara um administrador e um Hemocentro para cada teste."""

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

    def test_hemocentro_inicia_pendente(self):
        """Conta de Hemocentro nova deve aguardar analise."""

        self.assertEqual(
            self.hemocentro.status_validacao,
            Usuario.StatusValidacaoHemocentro.PENDENTE,
        )
        self.assertFalse(hemocentro_aprovado(self.hemocentro))

    def test_admin_aprova_e_cria_historico(self):
        """Aprovacao altera status, cria historico e gera auditoria."""

        validacao = aprovar_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.admin,
        )

        self.hemocentro.refresh_from_db()

        self.assertEqual(
            self.hemocentro.status_validacao,
            Usuario.StatusValidacaoHemocentro.APROVADO,
        )
        self.assertEqual(
            validacao.status,
            Usuario.StatusValidacaoHemocentro.APROVADO,
        )
        self.assertEqual(
            ValidacaoHemocentro.objects.filter(
                hemocentro=self.hemocentro
            ).count(),
            1,
        )
        self.assertTrue(
            AuditoriaAcaoCritica.objects.filter(
                acao=AuditoriaAcaoCritica.Acao.APROVACAO_HEMOCENTRO,
                usuario=self.admin,
                alvo_id=str(self.hemocentro.pk),
            ).exists()
        )

    def test_admin_recusa(self):
        """Recusa altera o status e guarda o parecer."""

        validacao = recusar_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.admin,
            parecer="CNPJ nao confere com os documentos enviados.",
        )

        self.hemocentro.refresh_from_db()

        self.assertEqual(
            self.hemocentro.status_validacao,
            Usuario.StatusValidacaoHemocentro.RECUSADO,
        )
        self.assertEqual(
            validacao.parecer,
            "CNPJ nao confere com os documentos enviados.",
        )

    def test_admin_solicita_correcao(self):
        """Solicitacao de correcao coloca o cadastro em CORRECAO."""

        solicitar_correcao_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.admin,
            parecer="Atualize telefone e endereco.",
        )

        self.hemocentro.refresh_from_db()

        self.assertEqual(
            self.hemocentro.status_validacao,
            Usuario.StatusValidacaoHemocentro.CORRECAO,
        )

    def test_usuario_comum_nao_pode_validar(self):
        """Somente administrador pode registrar a decisao."""

        usuario_comum = self.criar_usuario(
            email="doador@elo.test",
            nome="Doador",
            perfil=Usuario.Perfil.DOADOR,
        )

        with self.assertRaises(PermissionDenied):
            aprovar_hemocentro(
                hemocentro=self.hemocentro,
                admin=usuario_comum,
            )

    def test_hemocentro_nao_aprovado_nao_publica(self):
        """Pendente, recusado e correcao devem bloquear publicacao."""

        for status in (
            Usuario.StatusValidacaoHemocentro.PENDENTE,
            Usuario.StatusValidacaoHemocentro.RECUSADO,
            Usuario.StatusValidacaoHemocentro.CORRECAO,
        ):
            self.hemocentro.status_validacao = status
            self.hemocentro.save(update_fields=["status_validacao"])

            with self.assertRaises(PermissionDenied):
                validar_publicacao_hemocentro(self.hemocentro)

    def test_hemocentro_aprovado_pode_publicar(self):
        """Status aprovado libera a regra de publicacao."""

        aprovar_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.admin,
        )
        self.hemocentro.refresh_from_db()

        self.assertTrue(validar_publicacao_hemocentro(self.hemocentro))

    def test_dashboard_hemocentro_mostra_status_sem_link_de_aprovacao(self):
        """Hemocentro ve seu status, mas nao acessa validacao administrativa."""

        self.client.force_login(self.hemocentro)

        resposta = self.client.get(reverse("accounts:dashboard"))

        self.assertContains(
            resposta,
            "Status da validação institucional",
        )
        self.assertContains(resposta, "Pendente")
        self.assertNotContains(resposta, "Gestão de Hemocentros")
        self.assertNotContains(
            resposta,
            "Acessar aprovação de Hemocentros",
        )

    def test_admin_acessa_tela_de_validacao_e_ve_pendente(self):
        """Administrador deve receber a tela da aplicacao com os pendentes."""

        self.client.force_login(self.admin)

        resposta = self.client.get(reverse("accounts:dashboard"))

        self.assertContains(resposta, "Validação de Hemocentros")
        self.assertContains(
            resposta,
            "Acessar aprovação de Hemocentros",
        )
        self.assertContains(
            resposta,
            "<li>Aprovar Hemocentros.</li>",
            html=True,
        )
        self.assertContains(resposta, 'href="/admin/"')

        painel = self.client.get(
            reverse("accounts:painel_aprovacao_hemocentros")
        )

        self.assertEqual(painel.status_code, 200)
        self.assertContains(painel, self.hemocentro.nome)
        self.assertContains(painel, "Pendente")
        self.assertContains(painel, "Voltar ao painel")
        self.assertContains(painel, "Página inicial")
        self.assertContains(painel, "Estoques públicos")

    def test_admin_aprova_pelo_painel_e_libera_estoque(self):
        """A aprovacao feita na tela altera o status e libera o estoque."""

        self.client.force_login(self.admin)

        resposta = self.client.post(
            reverse(
                "accounts:aprovar_hemocentro",
                kwargs={"id_hemocentro": self.hemocentro.pk},
            ),
            {"parecer": "Documentacao conferida."},
        )

        self.assertRedirects(
            resposta,
            reverse("accounts:painel_aprovacao_hemocentros"),
        )

        self.hemocentro.refresh_from_db()

        self.assertEqual(
            self.hemocentro.status_validacao,
            Usuario.StatusValidacaoHemocentro.APROVADO,
        )

        self.client.force_login(self.hemocentro)

        estoque = self.client.get(
            reverse("accounts:estoque_hemocentro")
        )

        self.assertEqual(estoque.status_code, 200)
        self.assertContains(estoque, "Cadastrar novo estoque")

        cadastro_estoque = self.client.post(
            reverse("accounts:cadastrar_estoque"),
            {
                "tipo_sanguineo": "O+",
                "quantidade_bolsas": 8,
                "nivel_minimo": 10,
                "nivel_critico": 5,
            },
        )

        self.assertRedirects(
            cadastro_estoque,
            reverse("accounts:estoque_hemocentro"),
        )

        self.assertTrue(
            Estoque.objects.filter(
                hemocentro=self.hemocentro,
                tipo_sanguineo="O+",
            ).exists()
        )

    def test_usuario_comum_nao_acessa_tela_de_validacao(self):
        """A tela e suas acoes continuam restritas ao Administrador."""

        usuario_comum = self.criar_usuario(
            email="doador-tela@elo.test",
            nome="Doador",
            perfil=Usuario.Perfil.DOADOR,
        )

        self.client.force_login(usuario_comum)

        resposta = self.client.get(
            reverse("accounts:painel_aprovacao_hemocentros")
        )

        self.assertEqual(resposta.status_code, 403)

    def test_dashboard_admin_nao_mostra_publicacao_de_pedido(self):
        """Administrador não atua como Hemocentro na publicação."""

        self.client.force_login(self.admin)

        resposta = self.client.get(reverse("accounts:dashboard"))

        self.assertContains(resposta, "Pedidos ativos")
        self.assertNotContains(
            resposta,
            "Publicar pedido de sangue",
        )
        self.assertNotContains(
            resposta,
            "Solicitar divulgação de necessidade",
        )
