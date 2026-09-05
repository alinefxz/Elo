"""Testes do formulário construído a partir do catálogo."""

from django.test import SimpleTestCase

from .triagem_catalogo import obter_pergunta
from .triagem_forms import FormularioPergunta


class FormularioPerguntaTests(SimpleTestCase):
    """Protege a normalização usada para salvar respostas estruturadas."""

    def test_escolha_com_data_e_normalizada(self):
        """Falha se a data da alternativa não chegar ao motor com seu código."""

        form = FormularioPergunta(
            obter_pergunta("EXT-05A"),
            data={
                "resposta": "DATA",
                "data_DATA": "2026-08-01",
            },
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.cleaned_data["valor"],
            {
                "codigos": ["DATA"],
                "datas": {"DATA": "2026-08-01"},
                "detalhes": "",
            },
        )

    def test_selecao_multipla_preserva_uma_data_por_item(self):
        """Falha se duas vacinas diferentes compartilharem uma única data."""

        form = FormularioPergunta(
            obter_pergunta("EXT-48"),
            data={
                "resposta": ["DENGUE", "FEBRE_AMARELA"],
                "data_DENGUE": "2026-08-01",
                "data_FEBRE_AMARELA": "2026-08-10",
            },
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.cleaned_data["valor"]["datas"],
            {
                "DENGUE": "2026-08-01",
                "FEBRE_AMARELA": "2026-08-10",
            },
        )

    def test_data_futura_e_rejeitada(self):
        """Falha se uma data impossível produzir prazo de liberação."""

        form = FormularioPergunta(
            obter_pergunta("EXT-05A"),
            data={
                "resposta": "DATA",
                "data_DATA": "2999-01-01",
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("data_DATA", form.errors)

    def test_alternativa_com_prazo_exige_sua_data(self):
        """Falha se uma vacina sem data for aceita pelo formulário."""

        form = FormularioPergunta(
            obter_pergunta("EXT-48"),
            data={"resposta": ["DENGUE"]},
        )

        self.assertFalse(form.is_valid())
        self.assertIn("data_DENGUE", form.errors)

    def test_nenhuma_nao_pode_ser_marcada_com_uma_condicao(self):
        """Falha se uma resposta contraditória for persistida."""

        form = FormularioPergunta(
            obter_pergunta("EXT-20"),
            data={
                "resposta": ["NENHUMA", "ANEMIA_HEREDITARIA"],
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("resposta", form.errors)

    def test_descricao_e_obrigatoria_quando_usuario_informa_outra_condicao(self):
        """Falha se EXT-50 aceitar uma condição sem qualquer descrição."""

        form = FormularioPergunta(
            obter_pergunta("EXT-50"),
            data={"resposta": "SIM", "detalhes": ""},
        )

        self.assertFalse(form.is_valid())
        self.assertIn("detalhes", form.errors)

    def test_procedimento_estetico_registra_seguranca_e_inflamacao(self):
        """Falha se os fatores que alteram o prazo estético forem perdidos."""

        form = FormularioPergunta(
            obter_pergunta("EXT-24"),
            data={
                "resposta": ["BOTOX"],
                "data_BOTOX": "2026-08-01",
                "seguranca": "SIM",
                "inflamacao": "NAO",
            },
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["valor"]["seguranca"], "SIM")
        self.assertEqual(form.cleaned_data["valor"]["inflamacao"], "NAO")
