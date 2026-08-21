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
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib import admin
from django.test import RequestFactory

from .admin import UsuarioAdmin
from .auditoria import registrar_auditoria
from .models import AuditoriaAcaoCritica, ConsentimentoLGPD, Usuario


class AutenticacaoTests(TestCase):
    """Agrupa os testes do cadastro e da autenticacao comum."""

    def test_inicio_visitante_mostra_busca_estoque_e_pedidos(self):
        """Confirma que Visitante tem acesso publico limitado."""

        resposta = self.client.get(reverse("accounts:inicio"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Acesso visitante")
        self.assertContains(resposta, "Postos de coleta")
        self.assertContains(resposta, "Estoque geral")
        self.assertContains(resposta, "Pedidos ativos")

    def test_inicio_filtra_postos_de_coleta(self):
        """Confirma que a busca publica filtra os postos apresentados."""

        resposta = self.client.get(reverse("accounts:inicio"), {"q": "Campinas"})

        self.assertContains(resposta, "Banco de Sangue Vida")
        self.assertNotContains(resposta, "Unidade Hematologica Norte")

    def dados_de_cadastro(self):
        """Retorna dados validos reutilizados pelo teste de cadastro."""

        return {
            "nome": "Maria Silva",
            "email": "maria@example.com",
            "perfil": Usuario.Perfil.DOADOR,
            "cpf": "123.456.789-01",
            "cnpj": "",
            "telefone": "(11) 99999-9999",
            "data_nascimento": "1995-06-10",
            "sexo": Usuario.Sexo.FEMININO,
            "cidade": "Sao Paulo",
            "estado": "sp",
            "password1": "SenhaElo123",
            "password2": "SenhaElo123",
            "aceite_lgpd": "on",
        }

    def test_cadastro_cria_hash_e_consentimento(self):
        """Confirma que cadastro nao armazena a senha pura."""

        resposta = self.client.post(
            reverse("accounts:cadastro"),
            self.dados_de_cadastro(),
        )

        # O fluxo concluido redireciona para o dashboard.
        self.assertRedirects(resposta, reverse("accounts:dashboard"))

        usuario = Usuario.objects.get(email="maria@example.com")

        # O formulario retira a pontuacao do CPF e padroniza a UF.
        self.assertEqual(usuario.cpf, "12345678901")
        self.assertEqual(usuario.estado, "SP")
        self.assertEqual(usuario.perfil, Usuario.Perfil.DOADOR)

        # check_password aplica o algoritmo de hash e compara o resultado.
        # A segunda verificacao confirma que o texto original nao foi salvo.
        self.assertTrue(usuario.check_password("SenhaElo123"))
        self.assertNotEqual(usuario.password, "SenhaElo123")
        self.assertTrue(
            ConsentimentoLGPD.objects.filter(
                usuario=usuario,
                aceito=True,
            ).exists()
        )

    def test_login_usa_email_e_senha(self):
        """Confirma que o identificador de login e o e-mail."""

        Usuario.objects.create_user(
            email="joao@example.com",
            nome="Joao Souza",
            password="SenhaElo123",
            perfil=Usuario.Perfil.OBSERVADOR,
        )

        resposta = self.client.post(
            reverse("accounts:login"),
            {
                # AuthenticationForm chama o identificador interno de username,
                # mesmo quando USERNAME_FIELD aponta para email.
                "username": "joao@example.com",
                "password": "SenhaElo123",
            },
        )

        self.assertRedirects(resposta, reverse("accounts:dashboard"))

    def test_login_falho_gera_auditoria(self):
        """Confirma que uma tentativa invalida gera registro de auditoria."""

        resposta = self.client.post(
            reverse("accounts:login"),
            {
                "username": "naoexiste@example.com",
                "password": "SenhaErrada123",
            },
        )

        self.assertEqual(resposta.status_code, 200)
        auditoria = AuditoriaAcaoCritica.objects.get(
            acao=AuditoriaAcaoCritica.Acao.LOGIN_FALHO
        )
        self.assertEqual(auditoria.resultado, AuditoriaAcaoCritica.Resultado.FALHA)
        self.assertEqual(auditoria.metadados["email"], "naoexiste@example.com")
        self.assertNotIn("SenhaErrada123", str(auditoria.metadados))

    def test_login_suspeito_gera_auditoria_apos_muitas_falhas(self):
        """Confirma que muitas falhas recentes marcam login suspeito."""

        for _ in range(5):
            self.client.post(
                reverse("accounts:login"),
                {
                    "username": "suspeito@example.com",
                    "password": "SenhaErrada123",
                },
            )

        self.assertEqual(
            AuditoriaAcaoCritica.objects.filter(
                acao=AuditoriaAcaoCritica.Acao.LOGIN_FALHO
            ).count(),
            5,
        )
        auditoria = AuditoriaAcaoCritica.objects.get(
            acao=AuditoriaAcaoCritica.Acao.LOGIN_SUSPEITO
        )
        self.assertEqual(
            auditoria.resultado,
            AuditoriaAcaoCritica.Resultado.BLOQUEADO,
        )
        self.assertEqual(auditoria.metadados["falhas_recentes"], 5)

    def test_hemocentro_exige_cnpj(self):
        """Confirma a regra simples de documento para Hemocentro."""

        dados = self.dados_de_cadastro()
        dados.update(
            {
                "email": "hemocentro@example.com",
                "perfil": Usuario.Perfil.HEMOCENTRO,
                "cpf": "",
                "cnpj": "",
            }
        )

        resposta = self.client.post(reverse("accounts:cadastro"), dados)

        # Um formulario invalido volta com status 200 para mostrar os erros e
        # nao cria nenhuma conta no banco.
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Informe o CNPJ do hemocentro.")
        self.assertFalse(
            Usuario.objects.filter(email="hemocentro@example.com").exists()
        )

    def test_observador_tem_cadastro_simples(self):
        """Confirma que Observador nao precisa de CPF ou nascimento."""

        dados = self.dados_de_cadastro()
        dados.update(
            {
                "email": "observadora@example.com",
                "perfil": Usuario.Perfil.OBSERVADOR,
                "cpf": "",
                "cnpj": "",
                "data_nascimento": "",
            }
        )

        resposta = self.client.post(reverse("accounts:cadastro"), dados)

        self.assertRedirects(resposta, reverse("accounts:dashboard"))
        usuario = Usuario.objects.get(email="observadora@example.com")
        self.assertEqual(usuario.perfil, Usuario.Perfil.OBSERVADOR)
        self.assertIsNone(usuario.cpf)
        self.assertIsNone(usuario.data_nascimento)

    def test_dashboard_exige_login(self):
        """Confirma que visitante nao acessa a pagina protegida."""

        resposta = self.client.get(reverse("accounts:dashboard"))
        destino = f"{reverse('accounts:login')}?next={reverse('accounts:dashboard')}"
        self.assertRedirects(resposta, destino)

    def test_dashboard_doador_mostra_funcoes_do_perfil(self):
        """Confirma que Doador visualiza a jornada propria."""

        usuario = Usuario.objects.create_user(
            email="doador@example.com",
            nome="Doador Exemplo",
            password="SenhaElo123",
            perfil=Usuario.Perfil.DOADOR,
        )
        self.client.force_login(usuario)

        resposta = self.client.get(reverse("accounts:dashboard"))

        self.assertContains(resposta, "Painel do doador")
        self.assertContains(resposta, "pre-triagem")
        self.assertContains(resposta, "ranking")

    def test_dashboard_hemocentro_mostra_gestao_de_estoque(self):
        """Confirma que Hemocentro visualiza a operacao de estoque."""

        usuario = Usuario.objects.create_user(
            email="hemocentro@example.com",
            nome="Hemocentro Exemplo",
            password="SenhaElo123",
            perfil=Usuario.Perfil.HEMOCENTRO,
            cnpj="12345678000190",
        )
        self.client.force_login(usuario)

        resposta = self.client.get(reverse("accounts:dashboard"))

        self.assertContains(resposta, "Painel do hemocentro")
        self.assertContains(resposta, "Atualizar quantidade de bolsas")
        self.assertContains(resposta, "Confirmar comparecimento")

    def test_registrar_auditoria_remove_metadados_sensiveis(self):
        """Confirma que senha e token nao ficam gravados na auditoria."""

        auditoria = registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.ACESSO_DADOS_SENSIVEIS,
            resultado=AuditoriaAcaoCritica.Resultado.SUCESSO,
            descricao="Teste de saneamento.",
            metadados={
                "email": "maria@example.com",
                "password": "SenhaElo123",
                "token": "abc123",
            },
        )

        self.assertEqual(auditoria.metadados["email"], "maria@example.com")
        self.assertEqual(auditoria.metadados["password"], "[removido]")
        self.assertEqual(auditoria.metadados["token"], "[removido]")

    def test_admin_alteracao_de_perfil_gera_auditoria(self):
        """Confirma auditoria quando admin altera perfil ou permissao."""

        administrador = Usuario.objects.create_superuser(
            email="admin@example.com",
            nome="Admin Elo",
            password="SenhaElo123",
        )
        usuario = Usuario.objects.create_user(
            email="usuario@example.com",
            nome="Usuario Elo",
            password="SenhaElo123",
            perfil=Usuario.Perfil.OBSERVADOR,
        )

        request = RequestFactory().post("/admin/accounts/usuario/")
        request.user = administrador

        usuario.perfil = Usuario.Perfil.HEMOCENTRO
        usuario_admin = UsuarioAdmin(Usuario, admin.site)
        usuario_admin.save_model(request, usuario, form=None, change=True)

        auditoria = AuditoriaAcaoCritica.objects.get(
            acao=AuditoriaAcaoCritica.Acao.ALTERACAO_PERMISSAO
        )
        self.assertEqual(auditoria.usuario, administrador)
        self.assertEqual(auditoria.alvo_tipo, "accounts.Usuario")
        self.assertEqual(auditoria.alvo_id, str(usuario.pk))
        self.assertEqual(
            auditoria.metadados["alteracoes"]["perfil"]["antes"],
            Usuario.Perfil.OBSERVADOR,
        )
        self.assertEqual(
            auditoria.metadados["alteracoes"]["perfil"]["depois"],
            Usuario.Perfil.HEMOCENTRO,
        )
