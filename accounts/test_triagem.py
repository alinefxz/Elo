from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import (
    ConsentimentoLGPD,
    RespostaTriagem,
    Triagem,
    Usuario,
)
from .triagem import calcular_resultado


class TriagemExtensaTests(TestCase):
    """
    Testa o cálculo e o salvamento da triagem inicial.
    """

    def criar_doador(self):
        """
        Cria um usuário Doador para os testes.
        """

        return Usuario.objects.create_user(
            email="doador@teste.com",
            password="SenhaForte123!",
            nome="Doador Teste",
            perfil=Usuario.Perfil.DOADOR,
        )

    def dados_sem_impedimento(self):
        """
        Retorna respostas básicas sem impedimento inicial.
        """

        return {
            "entende_orientacao": "SIM",
            "idade": "18_60",
            "peso": "56_129_9",
            "sexo_biologico": "MASCULINO",
            "ja_doou": "NAO",
        }

    def test_peso_abaixo_de_50_gera_inaptidao_temporaria(self):
        """
        Peso abaixo de 50 kg deve gerar resultado temporário.
        """

        respostas = self.dados_sem_impedimento()
        respostas["peso"] = "MENOS_50"

        resultado = calcular_resultado(
            respostas,
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            resultado["resultado"],
            Triagem.Resultado.TEMPORARIA,
        )

    def test_respostas_basicas_sem_impedimento(self):
        """
        Respostas básicas devem gerar orientação sem impedimento identificado.
        """

        resultado = calcular_resultado(
            self.dados_sem_impedimento(),
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            resultado["resultado"],
            Triagem.Resultado.SEM_IMPEDIMENTO,
        )

    def test_post_inicia_triagem_e_consentimento(self):
        """
        O clique inicial cria a triagem e o consentimento versionado.
        """

        usuario = self.criar_doador()
        self.client.force_login(usuario)

        resposta = self.client.post(
            reverse(
                "accounts:triagem_iniciar",
                kwargs={"modalidade": "extensa"},
            ),
        )

        self.assertEqual(
            resposta.status_code,
            302,
        )

        triagem = Triagem.objects.get(
            usuario=usuario,
        )

        self.assertRedirects(
            resposta,
            reverse(
                "accounts:triagem_pergunta",
                kwargs={"id_triagem": triagem.pk},
            ),
        )

        self.assertEqual(
            RespostaTriagem.objects.filter(
                triagem=triagem,
            ).count(),
            0,
        )

        self.assertTrue(
            ConsentimentoLGPD.objects.filter(
                usuario=usuario,
                tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM,
            ).exists()
        )

    def test_usuario_nao_doador_nao_acessa_triagem(self):
        """
        A primeira versão da triagem só aceita usuários Doador.
        """

        usuario = Usuario.objects.create_user(
            email="observador@teste.com",
            password="SenhaForte123!",
            nome="Observador Teste",
            perfil=Usuario.Perfil.OBSERVADOR,
        )

        self.client.force_login(usuario)

        resposta = self.client.post(
            reverse(
                "accounts:triagem_iniciar",
                kwargs={"modalidade": "extensa"},
            ),
        )

        self.assertEqual(resposta.status_code, 403)

    def test_receptor_pode_acessar_a_triagem(self):
        """
        Receptor também pode responder à triagem para doação.
        """

        usuario = Usuario.objects.create_user(
            email="receptor@teste.com",
            password="SenhaForte123!",
            nome="Receptor Teste",
            perfil=Usuario.Perfil.RECEPTOR,
        )

        self.client.force_login(usuario)

        resposta = self.client.post(
            reverse(
                "accounts:triagem_iniciar",
                kwargs={"modalidade": "extensa"},
            ),
        )

        self.assertEqual(
            resposta.status_code,
            302,
        )

    def test_visitante_pode_ver_apresentacao_da_triagem(self):
        """
        Visitante pode conhecer a triagem sem estar autenticado.
        """

        resposta = self.client.get(
            reverse("accounts:triagem_apresentacao"),
        )

        self.assertEqual(
            resposta.status_code,
            200,
        )

        self.assertContains(
            resposta,
            "Seu gesto de cuidado começa aqui.",
        )

        self.assertContains(
            resposta,
            "Criar conta",
        )
