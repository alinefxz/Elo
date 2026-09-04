"""Testes das decisões e dos cálculos do motor orientativo."""

from datetime import date

from django.test import SimpleTestCase

from .models import Triagem
from .triagem_motor import avaliar_triagem


class MotorTriagemTests(SimpleTestCase):
    """Exercita regras reais sem depender de banco, view ou formulário."""

    def test_resultado_prioriza_definitiva_e_preserva_todos_os_achados(self):
        """Falha se o motor parar no primeiro impedimento ou usar prioridade errada."""

        calculo = avaliar_triagem(
            Triagem.Modalidade.EXTENSA,
            {
                "EXT-03": {"codigos": ["MENOS_50"]},
                "EXT-20": {"codigos": ["ANEMIA_HEREDITARIA"]},
                "EXT-46": {"codigos": ["OUTRO"]},
            },
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            calculo["resultado"],
            Triagem.Resultado.DEFINITIVA,
        )
        self.assertEqual(len(calculo["achados"]), 3)

    def test_resultado_usa_a_maior_data_temporaria(self):
        """Falha se um prazo curto esconder uma espera mais longa."""

        calculo = avaliar_triagem(
            Triagem.Modalidade.EXTENSA,
            {
                "EXT-13": {
                    "codigos": ["COVID_SINTOMATICO"],
                    "datas": {"COVID_SINTOMATICO": "2026-08-25"},
                },
                "EXT-48": {
                    "codigos": ["DENGUE"],
                    "datas": {"DENGUE": "2026-08-20"},
                },
            },
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            calculo["data_liberacao"],
            date(2026, 9, 19),
        )

    def test_prazo_em_meses_respeita_o_calendario(self):
        """Falha se um mês for tratado sempre como trinta dias."""

        calculo = avaliar_triagem(
            Triagem.Modalidade.EXTENSA,
            {
                "EXT-47": {
                    "codigos": ["FINASTERIDA"],
                    "datas": {"FINASTERIDA": "2026-01-31"},
                },
            },
            hoje=date(2026, 2, 1),
        )

        self.assertEqual(
            calculo["data_liberacao"],
            date(2026, 2, 28),
        )

    def test_regra_com_prazo_sem_data_exige_avaliacao(self):
        """Falha se o motor inventar a data de uma vacina não datada."""

        calculo = avaliar_triagem(
            Triagem.Modalidade.EXTENSA,
            {"EXT-48": {"codigos": ["DENGUE"]}},
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            calculo["resultado"],
            Triagem.Resultado.AVALIACAO,
        )
        self.assertIsNone(calculo["data_liberacao"])

    def test_estetica_sem_seguranca_usa_doze_meses(self):
        """Falha se um procedimento inseguro receber apenas o prazo de três dias."""

        calculo = avaliar_triagem(
            Triagem.Modalidade.EXTENSA,
            {
                "EXT-24": {
                    "codigos": ["BOTOX"],
                    "datas": {"BOTOX": "2026-08-01"},
                    "seguranca": "NAO_SEI",
                    "inflamacao": "NAO",
                },
            },
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            calculo["data_liberacao"],
            date(2027, 8, 1),
        )

    def test_estetica_com_inflamacao_exige_avaliacao(self):
        """Falha se uma complicação estética for tratada como recuperação simples."""

        calculo = avaliar_triagem(
            Triagem.Modalidade.EXTENSA,
            {
                "EXT-24": {
                    "codigos": ["BOTOX"],
                    "datas": {"BOTOX": "2026-08-01"},
                    "seguranca": "SIM",
                    "inflamacao": "SIM",
                },
            },
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            calculo["resultado"],
            Triagem.Resultado.AVALIACAO,
        )

    def test_ultima_doacao_calcula_intervalo_feminino(self):
        """Falha se o intervalo feminino não usar noventa dias."""

        calculo = avaliar_triagem(
            Triagem.Modalidade.EXTENSA,
            {
                "EXT-02": {"codigos": ["18_60"]},
                "EXT-04": {"codigos": ["FEMININO"]},
                "EXT-05A": {
                    "codigos": ["DATA"],
                    "datas": {"DATA": "2026-08-01"},
                },
            },
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            calculo["data_liberacao"],
            date(2026, 10, 30),
        )

    def test_ultima_doacao_acima_de_60_usa_seis_meses(self):
        """Falha se a regra especial de 61 a 69 anos for ignorada."""

        calculo = avaliar_triagem(
            Triagem.Modalidade.EXTENSA,
            {
                "EXT-02": {"codigos": ["61_69"]},
                "EXT-04": {"codigos": ["MASCULINO"]},
                "EXT-05A": {
                    "codigos": ["DATA"],
                    "datas": {"DATA": "2026-08-01"},
                },
            },
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            calculo["data_liberacao"],
            date(2027, 2, 1),
        )

    def test_limite_anual_sem_datas_nao_inventa_liberacao(self):
        """Falha se somente a contagem gerar uma data fictícia."""

        calculo = avaliar_triagem(
            Triagem.Modalidade.EXTENSA,
            {
                "EXT-04": {"codigos": ["FEMININO"]},
                "EXT-05B": {"codigos": ["3"]},
            },
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            calculo["resultado"],
            Triagem.Resultado.AVALIACAO,
        )
        self.assertIsNone(calculo["data_liberacao"])

    def test_simplificada_reutiliza_doenca_estavel_da_extensa(self):
        """Falha se uma condição permanente salva for esquecida na versão rápida."""

        calculo = avaliar_triagem(
            Triagem.Modalidade.SIMPLIFICADA,
            {"SIM-18": {"codigos": ["ENTENDO"]}},
            respostas_base={
                "EXT-20": {"codigos": ["ANEMIA_HEREDITARIA"]},
            },
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            calculo["resultado"],
            Triagem.Resultado.DEFINITIVA,
        )

    def test_simplificada_nao_reutiliza_estado_de_saude_antigo(self):
        """Falha se uma febre antiga for tratada como estado atual sem nova resposta."""

        calculo = avaliar_triagem(
            Triagem.Modalidade.SIMPLIFICADA,
            {"SIM-18": {"codigos": ["ENTENDO"]}},
            respostas_base={
                "EXT-12": {"codigos": ["PERSISTENTE"]},
            },
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            calculo["resultado"],
            Triagem.Resultado.SEM_IMPEDIMENTO,
        )

    def test_resultado_sem_achados_mantem_aviso_presencial(self):
        """Falha se a mensagem declarar que a pessoa está apta."""

        calculo = avaliar_triagem(
            Triagem.Modalidade.EXTENSA,
            {"EXT-51": {"codigos": ["CONFIRMAR"]}},
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            calculo["resultado"],
            Triagem.Resultado.SEM_IMPEDIMENTO,
        )
        self.assertIn("decisão final", calculo["mensagem"])
        self.assertNotIn("apto", calculo["mensagem"].lower())
