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

from .models import AuditoriaAcaoCritica, Usuario, ValidacaoHemocentro
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
        self.assertEqual(validacao.status, Usuario.StatusValidacaoHemocentro.APROVADO)
        self.assertEqual(
            ValidacaoHemocentro.objects.filter(hemocentro=self.hemocentro).count(),
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