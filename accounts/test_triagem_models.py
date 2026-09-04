"""Testes da persistência das triagens e de suas respostas."""

from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import RespostaTriagem, Triagem, Usuario


class TriagemModelTests(TestCase):
    """Garante que andamento e correções sejam persistidos sem duplicação."""

    def setUp(self):
        # Cada teste usa uma conta real do model personalizado do projeto.
        self.usuario = Usuario.objects.create_user(
            email="model-triagem@teste.com",
            password="SenhaForte123!",
            nome="Pessoa em Triagem",
            perfil=Usuario.Perfil.DOADOR,
        )

    def test_nova_triagem_comeca_em_andamento(self):
        """Falha se uma triagem nova nascer como concluída ou sem fluxo vazio."""

        triagem = Triagem.objects.create(
            usuario=self.usuario,
            modalidade=Triagem.Modalidade.EXTENSA,
        )

        self.assertEqual(
            triagem.status,
            Triagem.Status.EM_ANDAMENTO,
        )
        self.assertEqual(triagem.pergunta_atual, 0)
        self.assertEqual(triagem.fluxo_perguntas, [])
        self.assertEqual(triagem.resultado, "")

    def test_uma_pergunta_tem_uma_unica_resposta_por_triagem(self):
        """Falha se a mesma pergunta puder gerar respostas concorrentes."""

        triagem = Triagem.objects.create(
            usuario=self.usuario,
            modalidade=Triagem.Modalidade.EXTENSA,
        )
        RespostaTriagem.objects.create(
            triagem=triagem,
            id_pergunta="EXT-01",
            codigo_resposta="SIM",
            resposta_label="Sim",
            valor={"codigos": ["SIM"]},
        )

        # O bloco atomic mantém o TestCase utilizável após o IntegrityError.
        with self.assertRaises(IntegrityError), transaction.atomic():
            RespostaTriagem.objects.create(
                triagem=triagem,
                id_pergunta="EXT-01",
                codigo_resposta="NAO",
                resposta_label="Não",
                valor={"codigos": ["NAO"]},
            )

    def test_triagem_simplificada_pode_apontar_para_extensa_base(self):
        """Falha se a checagem rápida perder a extensa usada como referência."""

        extensa = Triagem.objects.create(
            usuario=self.usuario,
            modalidade=Triagem.Modalidade.EXTENSA,
        )
        simplificada = Triagem.objects.create(
            usuario=self.usuario,
            modalidade=Triagem.Modalidade.SIMPLIFICADA,
            triagem_base=extensa,
        )

        self.assertEqual(simplificada.triagem_base, extensa)
        self.assertIn(simplificada, extensa.verificacoes_simplificadas.all())
