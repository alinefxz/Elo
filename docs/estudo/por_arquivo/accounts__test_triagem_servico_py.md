# accounts/test_triagem_servico.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

**Arquivo original:** [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""
Testes automatizados do serviço de triagem.

Verificam o início e a retomada de triagens, o registro do consentimento,
a reutilização de respostas anteriores, as permissões de acesso, o fluxo
condicional das perguntas, o salvamento e a correção de respostas, a
remoção de respostas inválidas, o encaminhamento da triagem simplificada
para a extensa e a conclusão do processo, garantindo a integridade do
histórico e o bloqueio de alterações após a finalização.
"""

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

    def test_nova_extensa_pode_reutilizar_respostas_concluidas(self):
        """Copia respostas sem alterar a triagem concluída original."""

        origem = Triagem.objects.create(
            usuario=self.usuario,
            modalidade=Triagem.Modalidade.EXTENSA,
            status=Triagem.Status.CONCLUIDA,
            resultado=Triagem.Resultado.SEM_IMPEDIMENTO,
        )
        pergunta = obter_pergunta("EXT-01")
        RespostaTriagem.objects.create(
            triagem=origem,
            id_pergunta="EXT-01",
            codigo_resposta="SIM",
            resposta_label="Sim, entendo e quero continuar.",
            valor={"codigos": ["SIM"], "datas": {}, "detalhes": ""},
            rule_version=pergunta["regra_version"],
            source_ref=pergunta["fonte"],
        )

        nova = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.EXTENSA,
            ip=None,
            reutilizar_respostas=True,
        )

        self.assertNotEqual(nova.pk, origem.pk)
        self.assertEqual(
            nova.respostas.get(id_pergunta="EXT-01").codigo_resposta,
            "SIM",
        )
        self.assertEqual(origem.respostas.count(), 1)
        self.assertEqual(nova.pergunta_atual, 0)

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
        """Falha se um perfil fora de Doador responder à triagem."""

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
            "LEVE", "NAO_MEDI", "NAO_SEI", "CONFIRMAR",
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
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 10

```python
"""
Testes automatizados do serviço de triagem.

Verificam o início e a retomada de triagens, o registro do consentimento,
a reutilização de respostas anteriores, as permissões de acesso, o fluxo
condicional das perguntas, o salvamento e a correção de respostas, a
remoção de respostas inválidas, o encaminhamento da triagem simplificada
para a extensa e a conclusão do processo, garantindo a integridade do
histórico e o bloqueio de alterações após a finalização.
"""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 12 a 12

```python
from django.core.exceptions import PermissionDenied
```

**Explicação deste trecho:**

**Linha 12 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.exceptions` os nomes `PermissionDenied`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 13 a 13

```python
from django.test import TestCase
```

**Explicação deste trecho:**

**Linha 13 — ImportFrom** (nível 0 do bloco).

Importa de `django.test` os nomes `TestCase`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 15 a 15

```python
from .models import ConsentimentoLGPD, RespostaTriagem, Triagem, Usuario
```

**Explicação deste trecho:**

**Linha 15 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `ConsentimentoLGPD`, `RespostaTriagem`, `Triagem`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 16 a 16

```python
from .triagem_catalogo import obter_pergunta
```

**Explicação deste trecho:**

**Linha 16 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_catalogo` os nomes `obter_pergunta`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 17 a 26

```python
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
```

**Explicação deste trecho:**

**Linha 17 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_servico` os nomes `TriagemConcluida`, `TriagemExtensaNecessaria`, `TriagemSimplificadaIndisponivel`, `concluir_triagem`, `iniciar_triagem`, `obter_pergunta_atual`, `salvar_resposta`, `voltar_pergunta`. Pontos iniciais indicam importação relativa ao pacote.

### TriagemServicoTests — linhas 29 a 448

```python
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

    def test_nova_extensa_pode_reutilizar_respostas_concluidas(self):
        """Copia respostas sem alterar a triagem concluída original."""

        origem = Triagem.objects.create(
            usuario=self.usuario,
            modalidade=Triagem.Modalidade.EXTENSA,
            status=Triagem.Status.CONCLUIDA,
            resultado=Triagem.Resultado.SEM_IMPEDIMENTO,
        )
        pergunta = obter_pergunta("EXT-01")
        RespostaTriagem.objects.create(
            triagem=origem,
            id_pergunta="EXT-01",
            codigo_resposta="SIM",
            resposta_label="Sim, entendo e quero continuar.",
            valor={"codigos": ["SIM"], "datas": {}, "detalhes": ""},
            rule_version=pergunta["regra_version"],
            source_ref=pergunta["fonte"],
        )

        nova = iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.EXTENSA,
            ip=None,
            reutilizar_respostas=True,
        )

        self.assertNotEqual(nova.pk, origem.pk)
        self.assertEqual(
            nova.respostas.get(id_pergunta="EXT-01").codigo_resposta,
            "SIM",
        )
        self.assertEqual(origem.respostas.count(), 1)
        self.assertEqual(nova.pergunta_atual, 0)

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
        """Falha se um perfil fora de Doador responder à triagem."""

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
            "LEVE", "NAO_MEDI", "NAO_SEI", "CONFIRMAR",
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
```

**Explicação deste trecho:**

**Linha 29 — ClassDef** (nível 0 do bloco).

Define a classe `TriagemServicoTests` herdando de `TestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 29:

**Linha 30 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 32 — FunctionDef** (nível 1 do bloco).

Define `setUp(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 32:

**Linha 33 — Assign** (nível 2 do bloco).

Associa `self.usuario` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email='servico@teste.com'`, `password='SenhaForte123!'`, `nome='Pessoa Serviço'`, `perfil=Usuario.Perfil.DOADOR`.

- `email='servico@teste.com'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `password='SenhaForte123!'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Pessoa Serviço'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.DOADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 40 — FunctionDef** (nível 1 do bloco).

Define `test_inicio_extenso_cria_fluxo_e_consentimento(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: inicio extenso cria fluxo e consentimento.

Bloco `body` da linha 40:

**Linha 41 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 43 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.EXTENSA`; argumentos nomeados: `ip='127.0.0.1'`.

- `ip='127.0.0.1'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 49 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.fluxo_perguntas[0]`, `'EXT-01'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 50 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.fluxo_perguntas[-1]`, `'EXT-51'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 51 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.status`, `Triagem.Status.EM_ANDAMENTO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 55 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `ConsentimentoLGPD.objects.filter(usuario=self.usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM, versao_termo='HEMOMINAS_2026_08', aceito=True).exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 64 — FunctionDef** (nível 1 do bloco).

Define `test_inicio_reutiliza_triagem_em_andamento(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: inicio reutiliza triagem em andamento.

Bloco `body` da linha 64:

**Linha 65 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 67 — Assign** (nível 2 do bloco).

Associa `primeira` a a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.EXTENSA`; argumentos nomeados: `ip=None`.

- `ip=None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 72 — Assign** (nível 2 do bloco).

Associa `segunda` a a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.EXTENSA`; argumentos nomeados: `ip=None`.

- `ip=None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 78 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `primeira.pk`, `segunda.pk`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 79 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.usuario.triagens.count()`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 81 — FunctionDef** (nível 1 do bloco).

Define `test_nova_extensa_pode_reutilizar_respostas_concluidas(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: nova extensa pode reutilizar respostas concluidas.

Bloco `body` da linha 81:

**Linha 82 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 84 — Assign** (nível 2 do bloco).

Associa `origem` a a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.usuario`, `modalidade=Triagem.Modalidade.EXTENSA`, `status=Triagem.Status.CONCLUIDA`, `resultado=Triagem.Resultado.SEM_IMPEDIMENTO`.

- `usuario=self.usuario`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `modalidade=Triagem.Modalidade.EXTENSA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status=Triagem.Status.CONCLUIDA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `resultado=Triagem.Resultado.SEM_IMPEDIMENTO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 90 — Assign** (nível 2 do bloco).

Associa `pergunta` a a chamada `obter_pergunta`; argumentos posicionais: `'EXT-01'`.


**Linha 91 — Expr** (nível 2 do bloco).

Executa a chamada `RespostaTriagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `triagem=origem`, `id_pergunta='EXT-01'`, `codigo_resposta='SIM'`, `resposta_label='Sim, entendo e quero continuar.'`, `valor={'codigos': ['SIM'], 'datas': {}, 'detalhes': ''}`, `rule_version=pergunta['regra_version']`, `source_ref=pergunta['fonte']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 101 — Assign** (nível 2 do bloco).

Associa `nova` a a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.EXTENSA`; argumentos nomeados: `ip=None`, `reutilizar_respostas=True`.

- `ip=None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `reutilizar_respostas=True`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 108 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotEqual`; argumentos posicionais: `nova.pk`, `origem.pk`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 109 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `nova.respostas.get(id_pergunta='EXT-01').codigo_resposta`, `'SIM'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 113 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `origem.respostas.count()`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 114 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `nova.pergunta_atual`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 116 — FunctionDef** (nível 1 do bloco).

Define `test_simplificada_exige_extensa_concluida_do_mesmo_usuario(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: simplificada exige extensa concluida do mesmo usuario.

Bloco `body` da linha 116:

**Linha 117 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 119 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(TriagemSimplificadaIndisponivel)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 119:

**Linha 120 — Expr** (nível 3 do bloco).

Executa a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.SIMPLIFICADA`; argumentos nomeados: `ip=None`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 126 — FunctionDef** (nível 1 do bloco).

Define `test_simplificada_registra_a_extensa_base(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: simplificada registra a extensa base.

Bloco `body` da linha 126:

**Linha 127 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 129 — Assign** (nível 2 do bloco).

Associa `extensa` a a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.usuario`, `modalidade=Triagem.Modalidade.EXTENSA`, `status=Triagem.Status.CONCLUIDA`, `resultado=Triagem.Resultado.SEM_IMPEDIMENTO`.

- `usuario=self.usuario`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `modalidade=Triagem.Modalidade.EXTENSA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status=Triagem.Status.CONCLUIDA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `resultado=Triagem.Resultado.SEM_IMPEDIMENTO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 136 — Assign** (nível 2 do bloco).

Associa `simplificada` a a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.SIMPLIFICADA`; argumentos nomeados: `ip=None`.

- `ip=None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 142 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `simplificada.triagem_base`, `extensa`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 143 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `simplificada.fluxo_perguntas[0]`, `'SIM-01'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 145 — FunctionDef** (nível 1 do bloco).

Define `test_observador_nao_pode_iniciar_questionario(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: observador nao pode iniciar questionario.

Bloco `body` da linha 145:

**Linha 146 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 148 — Assign** (nível 2 do bloco).

Associa `observador` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email='observador-servico@teste.com'`, `password='SenhaForte123!'`, `nome='Observador'`, `perfil=Usuario.Perfil.OBSERVADOR`.

- `email='observador-servico@teste.com'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `password='SenhaForte123!'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Observador'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.OBSERVADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 155 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(PermissionDenied)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 155:

**Linha 156 — Expr** (nível 3 do bloco).

Executa a chamada `iniciar_triagem`; argumentos posicionais: `observador`, `Triagem.Modalidade.EXTENSA`; argumentos nomeados: `ip=None`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 162 — FunctionDef** (nível 1 do bloco).

Define `test_corrigir_resposta_substitui_sem_duplicar(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: corrigir resposta substitui sem duplicar.

Bloco `body` da linha 162:

**Linha 163 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 165 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.EXTENSA`; argumentos nomeados: `ip=None`.

- `ip=None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 170 — Expr** (nível 2 do bloco).

Executa a chamada `salvar_resposta`; argumentos posicionais: `triagem`, `'EXT-01'`, `{'codigos': ['SIM'], 'datas': {}, 'detalhes': ''}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 175 — Expr** (nível 2 do bloco).

Executa a chamada `voltar_pergunta`; argumentos posicionais: `triagem`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 176 — Expr** (nível 2 do bloco).

Executa a chamada `salvar_resposta`; argumentos posicionais: `triagem`, `'EXT-01'`, `{'codigos': ['NAO'], 'datas': {}, 'detalhes': ''}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 182 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.respostas.count()`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 183 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.respostas.get().codigo_resposta`, `'NAO'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 188 — FunctionDef** (nível 1 do bloco).

Define `test_resposta_simplificada_insere_bloco_extenso_sem_duplicar(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: resposta simplificada insere bloco extenso sem duplicar.

Bloco `body` da linha 188:

**Linha 189 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 191 — Assign** (nível 2 do bloco).

Associa `extensa` a a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.usuario`, `modalidade=Triagem.Modalidade.EXTENSA`, `status=Triagem.Status.CONCLUIDA`, `resultado=Triagem.Resultado.SEM_IMPEDIMENTO`.

- `usuario=self.usuario`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `modalidade=Triagem.Modalidade.EXTENSA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status=Triagem.Status.CONCLUIDA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `resultado=Triagem.Resultado.SEM_IMPEDIMENTO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 197 — Assign** (nível 2 do bloco).

Associa `simplificada` a a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.SIMPLIFICADA`; argumentos nomeados: `ip=None`.

- `ip=None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 203 — Assign** (nível 2 do bloco).

Associa `respostas_ate_sim_10` a um dicionário de 10 entradas; as chaves dão nome aos valores associados.

- Chave `'SIM-01'`: recebe o valor literal `'CORRETO'`.
- Chave `'SIM-02'`: recebe o valor literal `'NAO'`.
- Chave `'SIM-03'`: recebe o valor literal `'SIM'`.
- Chave `'SIM-04'`: recebe o valor literal `'SIM'`.
- Chave `'SIM-05'`: recebe o valor literal `'NAO'`.
- Chave `'SIM-06'`: recebe o valor literal `'NAO'`.
- Chave `'SIM-07'`: recebe o valor literal `'NAO'`.
- Chave `'SIM-08'`: recebe o valor literal `'NAO'`.
- Chave `'SIM-09'`: recebe o valor literal `'NAO'`.
- Chave `'SIM-10'`: recebe o valor literal `'SIM'`.

**Linha 215 — For** (nível 2 do bloco).

Percorre `respostas_ate_sim_10.items()`; cada item é atribuído a `(id_pergunta, codigo)` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 215:

**Linha 216 — Expr** (nível 3 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `obter_pergunta_atual(simplificada)['id']`, `id_pergunta`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 220 — Expr** (nível 3 do bloco).

Executa a chamada `salvar_resposta`; argumentos posicionais: `simplificada`, `id_pergunta`, `{'codigos': [codigo], 'datas': {}, 'detalhes': ''}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 226 — For** (nível 2 do bloco).

Percorre `('EXT-21', 'EXT-22', 'EXT-23', 'EXT-24')`; cada item é atribuído a `id_pergunta` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 226:

**Linha 227 — Expr** (nível 3 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `simplificada.fluxo_perguntas.count(id_pergunta)`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 231 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertLess`; argumentos posicionais: `simplificada.fluxo_perguntas.index('EXT-24')`, `simplificada.fluxo_perguntas.index('SIM-17')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 235 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `simplificada.triagem_base`, `extensa`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 237 — FunctionDef** (nível 1 do bloco).

Define `test_conclusao_salva_resultado_e_bloqueia_nova_resposta(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: conclusao salva resultado e bloqueia nova resposta.

Bloco `body` da linha 237:

**Linha 238 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 240 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.EXTENSA`; argumentos nomeados: `ip=None`.

- `ip=None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 248 — Assign** (nível 2 do bloco).

Associa `preferencias_neutras` a uma coleção Tuple com 14 itens, na expressão `('NAO', 'NENHUMA', 'NENHUM', 'NUNCA', 'SIM', '18_60', '56_129_9', 'MASCULINO', 'ORIGINAL', 'DESCANSADO', 'LEVE', 'NAO_MEDI', 'NAO_SEI', 'CONFIRMAR')`.

**Linha 253 — For** (nível 2 do bloco).

Percorre `triagem.fluxo_perguntas`; cada item é atribuído a `id_pergunta` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 253:

**Linha 254 — Assign** (nível 3 do bloco).

Associa `pergunta` a a chamada `obter_pergunta`; argumentos posicionais: `id_pergunta`.


**Linha 255 — Assign** (nível 3 do bloco).

Associa `opcoes` a uma coleção/gerador construído por compreensão em `{item['codigo']: item['rotulo'] for item in pergunta['opcoes']}`: percorre as fontes e aplica os filtros declarados.

**Linha 261 — Assign** (nível 3 do bloco).

Associa `codigo` a `'SIM'` se `id_pergunta in {'EXT-01', 'EXT-08', 'EXT-11'}` for verdadeiro; caso contrário, `next((candidato for candidato in preferencias_neutras if candidato in opcoes))`.

**Linha 270 — Expr** (nível 3 do bloco).

Executa a chamada `RespostaTriagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `triagem=triagem`, `id_pergunta=id_pergunta`, `codigo_resposta=codigo`, `resposta_label=opcoes[codigo]`, `valor={'codigos': [codigo], 'datas': {}, 'detalhes': ''}`, `rule_version=pergunta['regra_version']`, `source_ref=pergunta['fonte']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 280 — Expr** (nível 2 do bloco).

Executa a chamada `concluir_triagem`; argumentos posicionais: `triagem`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 281 — Expr** (nível 2 do bloco).

Executa a chamada `triagem.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 283 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.status`, `Triagem.Status.CONCLUIDA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 284 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `triagem.finalizada_em`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 285 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.resultado`, `Triagem.Resultado.SEM_IMPEDIMENTO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 289 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(TriagemConcluida)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 289:

**Linha 290 — Expr** (nível 3 do bloco).

Executa a chamada `salvar_resposta`; argumentos posicionais: `triagem`, `'EXT-51'`, `{'codigos': ['REVISAR'], 'datas': {}, 'detalhes': ''}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 296 — FunctionDef** (nível 1 do bloco).

Define `test_resposta_mantem_campos_legados_e_valor_completo(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: resposta mantem campos legados e valor completo.

Bloco `body` da linha 296:

**Linha 297 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 299 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.EXTENSA`; argumentos nomeados: `ip=None`.

- `ip=None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 304 — Expr** (nível 2 do bloco).

Executa a chamada `salvar_resposta`; argumentos posicionais: `triagem`, `'EXT-01'`, `{'codigos': ['SIM'], 'datas': {}, 'detalhes': 'Entendi.'}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 310 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `RespostaTriagem.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `triagem=triagem`.

- `triagem=triagem`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 311 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.codigo_resposta`, `'SIM'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 312 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.resposta_label`, `'Sim, entendo e quero continuar.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 316 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.valor['detalhes']`, `'Entendi.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 318 — FunctionDef** (nível 1 do bloco).

Define `test_nao_entendeu_permanece_na_primeira_pergunta(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: nao entendeu permanece na primeira pergunta.

Bloco `body` da linha 318:

**Linha 319 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 321 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.EXTENSA`; argumentos nomeados: `ip=None`.

- `ip=None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 327 — Expr** (nível 2 do bloco).

Executa a chamada `salvar_resposta`; argumentos posicionais: `triagem`, `'EXT-01'`, `{'codigos': ['NAO'], 'datas': {}, 'detalhes': ''}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 333 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.pergunta_atual`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 335 — FunctionDef** (nível 1 do bloco).

Define `test_revisar_confirmacao_extensa_volta_ao_inicio(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: revisar confirmacao extensa volta ao inicio.

Bloco `body` da linha 335:

**Linha 336 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 338 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.EXTENSA`; argumentos nomeados: `ip=None`.

- `ip=None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 343 — Assign** (nível 2 do bloco).

Associa `triagem.pergunta_atual` a a chamada `triagem.fluxo_perguntas.index`; argumentos posicionais: `'EXT-51'`.


**Linha 344 — Expr** (nível 2 do bloco).

Executa a chamada `triagem.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['pergunta_atual']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 346 — Expr** (nível 2 do bloco).

Executa a chamada `salvar_resposta`; argumentos posicionais: `triagem`, `'EXT-51'`, `{'codigos': ['REVISAR'], 'datas': {}, 'detalhes': ''}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 352 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.pergunta_atual`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 354 — FunctionDef** (nível 1 do bloco).

Define `test_resumo_incorreto_cancela_rapida_e_exige_extensa(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: resumo incorreto cancela rapida e exige extensa.

Bloco `body` da linha 354:

**Linha 355 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 357 — Expr** (nível 2 do bloco).

Executa a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.usuario`, `modalidade=Triagem.Modalidade.EXTENSA`, `status=Triagem.Status.CONCLUIDA`, `resultado=Triagem.Resultado.SEM_IMPEDIMENTO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 363 — Assign** (nível 2 do bloco).

Associa `simplificada` a a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.SIMPLIFICADA`; argumentos nomeados: `ip=None`.

- `ip=None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 369 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(TriagemExtensaNecessaria)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 369:

**Linha 370 — Expr** (nível 3 do bloco).

Executa a chamada `salvar_resposta`; argumentos posicionais: `simplificada`, `'SIM-01'`, `{'codigos': ['INCORRETO'], 'datas': {}, 'detalhes': ''}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 380 — Expr** (nível 2 do bloco).

Executa a chamada `simplificada.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 381 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `simplificada.status`, `Triagem.Status.CANCELADA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 383 — FunctionDef** (nível 1 do bloco).

Define `test_correcao_remove_resposta_de_subpergunta_oculta(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: correcao remove resposta de subpergunta oculta.

Bloco `body` da linha 383:

**Linha 384 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 386 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.EXTENSA`; argumentos nomeados: `ip=None`.

- `ip=None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 391 — Expr** (nível 2 do bloco).

Executa a chamada `salvar_resposta`; argumentos posicionais: `triagem`, `'EXT-05'`, `{'codigos': ['SIM'], 'datas': {}, 'detalhes': ''}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 396 — Expr** (nível 2 do bloco).

Executa a chamada `salvar_resposta`; argumentos posicionais: `triagem`, `'EXT-05A'`, `{'codigos': ['DATA'], 'datas': {'DATA': '2026-08-01'}, 'detalhes': ''}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 407 — Expr** (nível 2 do bloco).

Executa a chamada `salvar_resposta`; argumentos posicionais: `triagem`, `'EXT-05'`, `{'codigos': ['NAO'], 'datas': {}, 'detalhes': ''}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 413 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotIn`; argumentos posicionais: `'EXT-05A'`, `triagem.fluxo_perguntas`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 414 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `triagem.respostas.filter(id_pergunta='EXT-05A').exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 418 — FunctionDef** (nível 1 do bloco).

Define `test_rapida_respeita_condicoes_das_perguntas_detalhadas(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: rapida respeita condicoes das perguntas detalhadas.

Bloco `body` da linha 418:

**Linha 419 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 421 — Expr** (nível 2 do bloco).

Executa a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.usuario`, `modalidade=Triagem.Modalidade.EXTENSA`, `status=Triagem.Status.CONCLUIDA`, `resultado=Triagem.Resultado.SEM_IMPEDIMENTO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 427 — Assign** (nível 2 do bloco).

Associa `simplificada` a a chamada `iniciar_triagem`; argumentos posicionais: `self.usuario`, `Triagem.Modalidade.SIMPLIFICADA`; argumentos nomeados: `ip=None`.

- `ip=None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 433 — Expr** (nível 2 do bloco).

Executa a chamada `salvar_resposta`; argumentos posicionais: `simplificada`, `'SIM-02'`, `{'codigos': ['DOOU'], 'datas': {}, 'detalhes': ''}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 439 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'EXT-05'`, `simplificada.fluxo_perguntas`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 440 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotIn`; argumentos posicionais: `'EXT-05A'`, `simplificada.fluxo_perguntas`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 442 — Expr** (nível 2 do bloco).

Executa a chamada `salvar_resposta`; argumentos posicionais: `simplificada`, `'EXT-05'`, `{'codigos': ['SIM'], 'datas': {}, 'detalhes': ''}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 447 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'EXT-05A'`, `simplificada.fluxo_perguntas`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 448 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'EXT-05B'`, `simplificada.fluxo_perguntas`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 246: `# Preenche o fluxo efetivo com alternativas neutras para isolar a`
- Linha 247: `# transição de conclusão que este teste protege.`
- Linha 259: `# Algumas perguntas são escritas de forma positiva. Nelas, "SIM"`
- Linha 260: `# representa o cenário neutro; nas demais usamos a lista geral.`
- Linha 406: `# Ao corrigir EXT-05, EXT-05A e EXT-05B deixam de pertencer ao fluxo.`

