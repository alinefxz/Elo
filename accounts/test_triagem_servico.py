"""Testes do serviço que controla o andamento persistente da triagem."""

from django.core.exceptions import PermissionDenied
from django.test import TestCase

from .models import ConsentimentoLGPD, RespostaTriagem, Triagem, Usuario
from .triagem_catalogo import obter_pergunta
from .triagem_servico import (
    TriagemConcluida,
    TriagemExtensaNecessaria,
    TriagemSimplificadaIndisponivel,
    concluir_triagem,
    iniciar_triagem,
    obter_pergunta_atual,
    salvar_resposta,
    voltar_pergunta,
)


class TriagemServicoTests(TestCase):
    """Protege transições de estado e vínculos entre as duas modalidades."""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email="servico@teste.com",
            password="SenhaForte123!",
            nome="Pessoa Serviço",
            perfil=Usuario.Perfil.DOADOR,
        )

    def test_inicio_extenso_cria_fluxo_e_consentimento(self):
        """Falha se uma triagem começar sem pergunta ou sem aceite versionado."""

        triagem = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.EXTENSA,
            ip="127.0.0.1",
        )

        self.assertEqual(triagem.fluxo_perguntas[0], "EXT-01")
        self.assertEqual(triagem.fluxo_perguntas[-1], "EXT-51")
        self.assertEqual(
            triagem.status,
            Triagem.Status.EM_ANDAMENTO,
        )
        self.assertTrue(
            ConsentimentoLGPD.objects.filter(
                usuario=self.usuario,
                tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM,
                versao_termo="HEMOMINAS_2026_08",
                aceito=True,
            ).exists()
        )

    def test_inicio_reutiliza_triagem_em_andamento(self):
        """Falha se cada clique em iniciar criar um histórico vazio duplicado."""

        primeira = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.EXTENSA,
            ip=None,
        )
        segunda = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.EXTENSA,
            ip=None,
        )

        self.assertEqual(primeira.pk, segunda.pk)
        self.assertEqual(self.usuario.triagens.count(), 1)

    def test_simplificada_exige_extensa_concluida_do_mesmo_usuario(self):
        """Falha se a versão rápida puder ser usada sem histórico completo."""

        with self.assertRaises(TriagemSimplificadaIndisponivel):
            iniciar_triagem(
                self.usuario,
                Triagem.Modalidade.SIMPLIFICADA,
                ip=None,
            )

    def test_simplificada_registra_a_extensa_base(self):
        """Falha se o resultado rápido perder a origem das respostas reutilizadas."""

        extensa = Triagem.objects.create(
            usuario=self.usuario,
            modalidade=Triagem.Modalidade.EXTENSA,
            status=Triagem.Status.CONCLUIDA,
            resultado=Triagem.Resultado.SEM_IMPEDIMENTO,
        )

        simplificada = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.SIMPLIFICADA,
            ip=None,
        )

        self.assertEqual(simplificada.triagem_base, extensa)
        self.assertEqual(simplificada.fluxo_perguntas[0], "SIM-01")

    def test_observador_nao_pode_iniciar_questionario(self):
        """Falha se um perfil fora de Doador/Receptor responder à triagem."""

        observador = Usuario.objects.create_user(
            email="observador-servico@teste.com",
            password="SenhaForte123!",
            nome="Observador",
            perfil=Usuario.Perfil.OBSERVADOR,
        )

        with self.assertRaises(PermissionDenied):
            iniciar_triagem(
                observador,
                Triagem.Modalidade.EXTENSA,
                ip=None,
            )

    def test_corrigir_resposta_substitui_sem_duplicar(self):
        """Falha se voltar e corrigir criar duas respostas para EXT-01."""

        triagem = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.EXTENSA,
            ip=None,
        )
        salvar_resposta(
            triagem,
            "EXT-01",
            {"codigos": ["SIM"], "datas": {}, "detalhes": ""},
        )
        voltar_pergunta(triagem)
        salvar_resposta(
            triagem,
            "EXT-01",
            {"codigos": ["NAO"], "datas": {}, "detalhes": ""},
        )

        self.assertEqual(triagem.respostas.count(), 1)
        self.assertEqual(
            triagem.respostas.get().codigo_resposta,
            "NAO",
        )

    def test_resposta_simplificada_insere_bloco_extenso_sem_duplicar(self):
        """Falha se uma mudança estética não abrir todas as perguntas detalhadas."""

        extensa = Triagem.objects.create(
            usuario=self.usuario,
            modalidade=Triagem.Modalidade.EXTENSA,
            status=Triagem.Status.CONCLUIDA,
            resultado=Triagem.Resultado.SEM_IMPEDIMENTO,
        )
        simplificada = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.SIMPLIFICADA,
            ip=None,
        )

        respostas_ate_sim_10 = {
            "SIM-01": "CORRETO",
            "SIM-02": "NAO",
            "SIM-03": "SIM",
            "SIM-04": "SIM",
            "SIM-05": "NAO",
            "SIM-06": "NAO",
            "SIM-07": "NAO",
            "SIM-08": "NAO",
            "SIM-09": "NAO",
            "SIM-10": "SIM",
        }
        for id_pergunta, codigo in respostas_ate_sim_10.items():
            self.assertEqual(
                obter_pergunta_atual(simplificada)["id"],
                id_pergunta,
            )
            salvar_resposta(
                simplificada,
                id_pergunta,
                {"codigos": [codigo], "datas": {}, "detalhes": ""},
            )

        for id_pergunta in ("EXT-21", "EXT-22", "EXT-23", "EXT-24"):
            self.assertEqual(
                simplificada.fluxo_perguntas.count(id_pergunta),
                1,
            )
        self.assertLess(
            simplificada.fluxo_perguntas.index("EXT-24"),
            simplificada.fluxo_perguntas.index("SIM-17"),
        )
        self.assertEqual(simplificada.triagem_base, extensa)

    def test_conclusao_salva_resultado_e_bloqueia_nova_resposta(self):
        """Falha se uma triagem concluída puder ser reescrita."""

        triagem = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.EXTENSA,
            ip=None,
        )

        # Preenche o fluxo efetivo com alternativas neutras para isolar a
        # transição de conclusão que este teste protege.
        preferencias_neutras = (
            "NAO", "NENHUMA", "NENHUM", "NUNCA", "SIM", "18_60",
            "56_129_9", "MASCULINO", "ORIGINAL", "DESCANSADO",
            "LEVE", "NAO_MEDI", "CONFIRMAR",
        )
        for id_pergunta in triagem.fluxo_perguntas:
            pergunta = obter_pergunta(id_pergunta)
            opcoes = {
                item["codigo"]: item["rotulo"]
                for item in pergunta["opcoes"]
            }
            # Algumas perguntas são escritas de forma positiva. Nelas, "SIM"
            # representa o cenário neutro; nas demais usamos a lista geral.
            codigo = (
                "SIM"
                if id_pergunta in {"EXT-01", "EXT-08", "EXT-11"}
                else next(
                    candidato
                    for candidato in preferencias_neutras
                    if candidato in opcoes
                )
            )
            RespostaTriagem.objects.create(
                triagem=triagem,
                id_pergunta=id_pergunta,
                codigo_resposta=codigo,
                resposta_label=opcoes[codigo],
                valor={"codigos": [codigo], "datas": {}, "detalhes": ""},
                rule_version=pergunta["regra_version"],
                source_ref=pergunta["fonte"],
            )

        concluir_triagem(triagem)
        triagem.refresh_from_db()

        self.assertEqual(triagem.status, Triagem.Status.CONCLUIDA)
        self.assertTrue(triagem.finalizada_em)
        self.assertEqual(
            triagem.resultado,
            Triagem.Resultado.SEM_IMPEDIMENTO,
        )
        with self.assertRaises(TriagemConcluida):
            salvar_resposta(
                triagem,
                "EXT-51",
                {"codigos": ["REVISAR"], "datas": {}, "detalhes": ""},
            )

    def test_resposta_mantem_campos_legados_e_valor_completo(self):
        """Falha se o admin antigo ou o novo motor perderem dados."""

        triagem = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.EXTENSA,
            ip=None,
        )
        salvar_resposta(
            triagem,
            "EXT-01",
            {"codigos": ["SIM"], "datas": {}, "detalhes": "Entendi."},
        )

        resposta = RespostaTriagem.objects.get(triagem=triagem)
        self.assertEqual(resposta.codigo_resposta, "SIM")
        self.assertEqual(
            resposta.resposta_label,
            "Sim, entendo e quero continuar.",
        )
        self.assertEqual(resposta.valor["detalhes"], "Entendi.")

    def test_nao_entendeu_permanece_na_primeira_pergunta(self):
        """Falha se EXT-01=NAO avançar sem repetir a explicação."""

        triagem = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.EXTENSA,
            ip=None,
        )

        salvar_resposta(
            triagem,
            "EXT-01",
            {"codigos": ["NAO"], "datas": {}, "detalhes": ""},
        )

        self.assertEqual(triagem.pergunta_atual, 0)

    def test_revisar_confirmacao_extensa_volta_ao_inicio(self):
        """Falha se EXT-51=REVISAR não permitir conferir as respostas."""

        triagem = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.EXTENSA,
            ip=None,
        )
        triagem.pergunta_atual = triagem.fluxo_perguntas.index("EXT-51")
        triagem.save(update_fields=["pergunta_atual"])

        salvar_resposta(
            triagem,
            "EXT-51",
            {"codigos": ["REVISAR"], "datas": {}, "detalhes": ""},
        )

        self.assertEqual(triagem.pergunta_atual, 0)

    def test_resumo_incorreto_cancela_rapida_e_exige_extensa(self):
        """Falha se dados antigos incorretos continuarem na versão rápida."""

        Triagem.objects.create(
            usuario=self.usuario,
            modalidade=Triagem.Modalidade.EXTENSA,
            status=Triagem.Status.CONCLUIDA,
            resultado=Triagem.Resultado.SEM_IMPEDIMENTO,
        )
        simplificada = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.SIMPLIFICADA,
            ip=None,
        )

        with self.assertRaises(TriagemExtensaNecessaria):
            salvar_resposta(
                simplificada,
                "SIM-01",
                {
                    "codigos": ["INCORRETO"],
                    "datas": {},
                    "detalhes": "",
                },
            )

        simplificada.refresh_from_db()
        self.assertEqual(simplificada.status, Triagem.Status.CANCELADA)

    def test_correcao_remove_resposta_de_subpergunta_oculta(self):
        """Falha se uma resposta escondida continuar alterando o resultado."""

        triagem = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.EXTENSA,
            ip=None,
        )
        salvar_resposta(
            triagem,
            "EXT-05",
            {"codigos": ["SIM"], "datas": {}, "detalhes": ""},
        )
        salvar_resposta(
            triagem,
            "EXT-05A",
            {
                "codigos": ["DATA"],
                "datas": {"DATA": "2026-08-01"},
                "detalhes": "",
            },
        )

        # Ao corrigir EXT-05, EXT-05A e EXT-05B deixam de pertencer ao fluxo.
        salvar_resposta(
            triagem,
            "EXT-05",
            {"codigos": ["NAO"], "datas": {}, "detalhes": ""},
        )

        self.assertNotIn("EXT-05A", triagem.fluxo_perguntas)
        self.assertFalse(
            triagem.respostas.filter(id_pergunta="EXT-05A").exists()
        )

    def test_rapida_respeita_condicoes_das_perguntas_detalhadas(self):
        """Falha se a rápida mostrar data de doação antes de confirmar doação."""

        Triagem.objects.create(
            usuario=self.usuario,
            modalidade=Triagem.Modalidade.EXTENSA,
            status=Triagem.Status.CONCLUIDA,
            resultado=Triagem.Resultado.SEM_IMPEDIMENTO,
        )
        simplificada = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.SIMPLIFICADA,
            ip=None,
        )

        salvar_resposta(
            simplificada,
            "SIM-02",
            {"codigos": ["DOOU"], "datas": {}, "detalhes": ""},
        )

        self.assertIn("EXT-05", simplificada.fluxo_perguntas)
        self.assertNotIn("EXT-05A", simplificada.fluxo_perguntas)

        salvar_resposta(
            simplificada,
            "EXT-05",
            {"codigos": ["SIM"], "datas": {}, "detalhes": ""},
        )
        self.assertIn("EXT-05A", simplificada.fluxo_perguntas)
        self.assertIn("EXT-05B", simplificada.fluxo_perguntas)
