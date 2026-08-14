"""
RESUMO DO ARQUIVO
=================
Testes automatizados executam o fluxo sem abrir o navegador. Cada teste usa um
banco temporario e e isolado dos demais.

Os testes abaixo verificam o minimo mais importante desta entrega:

1. cadastro cria conta, hash de senha e consentimento;
2. login aceita e-mail e senha corretos;
3. dashboard redireciona visitantes para o login.

Execute com: ``python manage.py test``.
"""

from django.test import TestCase
from django.urls import reverse

from .models import ConsentimentoLGPD, Usuario


class AutenticacaoTests(TestCase):
    """Agrupa os testes do cadastro e da autenticacao comum."""

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

    def test_dashboard_exige_login(self):
        """Confirma que visitante nao acessa a pagina protegida."""

        resposta = self.client.get(reverse("accounts:dashboard"))
        destino = f"{reverse('accounts:login')}?next={reverse('accounts:dashboard')}"
        self.assertRedirects(resposta, destino)
