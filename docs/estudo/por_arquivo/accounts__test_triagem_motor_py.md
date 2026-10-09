# accounts/test_triagem_motor.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

**Arquivo original:** [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""
Testes automatizados do motor de triagem orientativa.

Verificam a prioridade dos resultados, a preservação dos achados,
o cálculo de prazos e datas de liberação, a exigência de avaliação
quando faltam informações, as regras para procedimentos estéticos e
intervalos entre doações, os limites anuais de doação, a reutilização
segura de respostas na triagem simplificada e a apresentação de
mensagens que reforçam a necessidade de avaliação final pelo hemocentro.
"""

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
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 10

```python
"""
Testes automatizados do motor de triagem orientativa.

Verificam a prioridade dos resultados, a preservação dos achados,
o cálculo de prazos e datas de liberação, a exigência de avaliação
quando faltam informações, as regras para procedimentos estéticos e
intervalos entre doações, os limites anuais de doação, a reutilização
segura de respostas na triagem simplificada e a apresentação de
mensagens que reforçam a necessidade de avaliação final pelo hemocentro.
"""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 12 a 12

```python
from datetime import date
```

**Explicação deste trecho:**

**Linha 12 — ImportFrom** (nível 0 do bloco).

Importa de `datetime` os nomes `date`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 14 a 14

```python
from django.test import SimpleTestCase
```

**Explicação deste trecho:**

**Linha 14 — ImportFrom** (nível 0 do bloco).

Importa de `django.test` os nomes `SimpleTestCase`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 16 a 16

```python
from .models import Triagem
```

**Explicação deste trecho:**

**Linha 16 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `Triagem`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 17 a 17

```python
from .triagem_motor import avaliar_triagem
```

**Explicação deste trecho:**

**Linha 17 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_motor` os nomes `avaliar_triagem`. Pontos iniciais indicam importação relativa ao pacote.

### MotorTriagemTests — linhas 20 a 249

```python
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
```

**Explicação deste trecho:**

**Linha 20 — ClassDef** (nível 0 do bloco).

Define a classe `MotorTriagemTests` herdando de `SimpleTestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 20:

**Linha 21 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 23 — FunctionDef** (nível 1 do bloco).

Define `test_resultado_prioriza_definitiva_e_preserva_todos_os_achados(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: resultado prioriza definitiva e preserva todos os achados.

Bloco `body` da linha 23:

**Linha 24 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 26 — Assign** (nível 2 do bloco).

Associa `calculo` a a chamada `avaliar_triagem`; argumentos posicionais: `Triagem.Modalidade.EXTENSA`, `{'EXT-03': {'codigos': ['MENOS_50']}, 'EXT-20': {'codigos': ['ANEMIA_HEREDITARIA']}, 'EXT-46': {'codigos': ['OUTRO']}}`; argumentos nomeados: `hoje=date(2026, 8, 28)`.

- `hoje=date(2026, 8, 28)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 36 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calculo['resultado']`, `Triagem.Resultado.DEFINITIVA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 40 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `len(calculo['achados'])`, `3`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 42 — FunctionDef** (nível 1 do bloco).

Define `test_resultado_usa_a_maior_data_temporaria(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: resultado usa a maior data temporaria.

Bloco `body` da linha 42:

**Linha 43 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 45 — Assign** (nível 2 do bloco).

Associa `calculo` a a chamada `avaliar_triagem`; argumentos posicionais: `Triagem.Modalidade.EXTENSA`, `{'EXT-13': {'codigos': ['COVID_SINTOMATICO'], 'datas': {'COVID_SINTOMATICO': '2026-08-25'}}, 'EXT-48': {'codigos': ['DENGUE'], 'datas': {'DENGUE': '2026-08-20'}}}`; argumentos nomeados: `hoje=date(2026, 8, 28)`.

- `hoje=date(2026, 8, 28)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 60 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calculo['data_liberacao']`, `date(2026, 9, 19)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 65 — FunctionDef** (nível 1 do bloco).

Define `test_prazo_em_meses_respeita_o_calendario(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: prazo em meses respeita o calendario.

Bloco `body` da linha 65:

**Linha 66 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 68 — Assign** (nível 2 do bloco).

Associa `calculo` a a chamada `avaliar_triagem`; argumentos posicionais: `Triagem.Modalidade.EXTENSA`, `{'EXT-47': {'codigos': ['FINASTERIDA'], 'datas': {'FINASTERIDA': '2026-01-31'}}}`; argumentos nomeados: `hoje=date(2026, 2, 1)`.

- `hoje=date(2026, 2, 1)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 79 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calculo['data_liberacao']`, `date(2026, 2, 28)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 84 — FunctionDef** (nível 1 do bloco).

Define `test_regra_com_prazo_sem_data_exige_avaliacao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: regra com prazo sem data exige avaliacao.

Bloco `body` da linha 84:

**Linha 85 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 87 — Assign** (nível 2 do bloco).

Associa `calculo` a a chamada `avaliar_triagem`; argumentos posicionais: `Triagem.Modalidade.EXTENSA`, `{'EXT-48': {'codigos': ['DENGUE']}}`; argumentos nomeados: `hoje=date(2026, 8, 28)`.

- `hoje=date(2026, 8, 28)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 93 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calculo['resultado']`, `Triagem.Resultado.AVALIACAO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 97 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIsNone`; argumentos posicionais: `calculo['data_liberacao']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 99 — FunctionDef** (nível 1 do bloco).

Define `test_estetica_sem_seguranca_usa_doze_meses(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: estetica sem seguranca usa doze meses.

Bloco `body` da linha 99:

**Linha 100 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 102 — Assign** (nível 2 do bloco).

Associa `calculo` a a chamada `avaliar_triagem`; argumentos posicionais: `Triagem.Modalidade.EXTENSA`, `{'EXT-24': {'codigos': ['BOTOX'], 'datas': {'BOTOX': '2026-08-01'}, 'seguranca': 'NAO_SEI', 'inflamacao': 'NAO'}}`; argumentos nomeados: `hoje=date(2026, 8, 28)`.

- `hoje=date(2026, 8, 28)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 115 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calculo['data_liberacao']`, `date(2027, 8, 1)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 120 — FunctionDef** (nível 1 do bloco).

Define `test_estetica_com_inflamacao_exige_avaliacao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: estetica com inflamacao exige avaliacao.

Bloco `body` da linha 120:

**Linha 121 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 123 — Assign** (nível 2 do bloco).

Associa `calculo` a a chamada `avaliar_triagem`; argumentos posicionais: `Triagem.Modalidade.EXTENSA`, `{'EXT-24': {'codigos': ['BOTOX'], 'datas': {'BOTOX': '2026-08-01'}, 'seguranca': 'SIM', 'inflamacao': 'SIM'}}`; argumentos nomeados: `hoje=date(2026, 8, 28)`.

- `hoje=date(2026, 8, 28)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 136 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calculo['resultado']`, `Triagem.Resultado.AVALIACAO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 141 — FunctionDef** (nível 1 do bloco).

Define `test_ultima_doacao_calcula_intervalo_feminino(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: ultima doacao calcula intervalo feminino.

Bloco `body` da linha 141:

**Linha 142 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 144 — Assign** (nível 2 do bloco).

Associa `calculo` a a chamada `avaliar_triagem`; argumentos posicionais: `Triagem.Modalidade.EXTENSA`, `{'EXT-02': {'codigos': ['18_60']}, 'EXT-04': {'codigos': ['FEMININO']}, 'EXT-05A': {'codigos': ['DATA'], 'datas': {'DATA': '2026-08-01'}}}`; argumentos nomeados: `hoje=date(2026, 8, 28)`.

- `hoje=date(2026, 8, 28)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 157 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calculo['data_liberacao']`, `date(2026, 10, 30)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 162 — FunctionDef** (nível 1 do bloco).

Define `test_ultima_doacao_acima_de_60_usa_seis_meses(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: ultima doacao acima de 60 usa seis meses.

Bloco `body` da linha 162:

**Linha 163 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 165 — Assign** (nível 2 do bloco).

Associa `calculo` a a chamada `avaliar_triagem`; argumentos posicionais: `Triagem.Modalidade.EXTENSA`, `{'EXT-02': {'codigos': ['61_69']}, 'EXT-04': {'codigos': ['MASCULINO']}, 'EXT-05A': {'codigos': ['DATA'], 'datas': {'DATA': '2026-08-01'}}}`; argumentos nomeados: `hoje=date(2026, 8, 28)`.

- `hoje=date(2026, 8, 28)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 178 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calculo['data_liberacao']`, `date(2027, 2, 1)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 183 — FunctionDef** (nível 1 do bloco).

Define `test_limite_anual_sem_datas_nao_inventa_liberacao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: limite anual sem datas nao inventa liberacao.

Bloco `body` da linha 183:

**Linha 184 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 186 — Assign** (nível 2 do bloco).

Associa `calculo` a a chamada `avaliar_triagem`; argumentos posicionais: `Triagem.Modalidade.EXTENSA`, `{'EXT-04': {'codigos': ['FEMININO']}, 'EXT-05B': {'codigos': ['3']}}`; argumentos nomeados: `hoje=date(2026, 8, 28)`.

- `hoje=date(2026, 8, 28)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 195 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calculo['resultado']`, `Triagem.Resultado.AVALIACAO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 199 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIsNone`; argumentos posicionais: `calculo['data_liberacao']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 201 — FunctionDef** (nível 1 do bloco).

Define `test_simplificada_reutiliza_doenca_estavel_da_extensa(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: simplificada reutiliza doenca estavel da extensa.

Bloco `body` da linha 201:

**Linha 202 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 204 — Assign** (nível 2 do bloco).

Associa `calculo` a a chamada `avaliar_triagem`; argumentos posicionais: `Triagem.Modalidade.SIMPLIFICADA`, `{'SIM-18': {'codigos': ['ENTENDO']}}`; argumentos nomeados: `respostas_base={'EXT-20': {'codigos': ['ANEMIA_HEREDITARIA']}}`, `hoje=date(2026, 8, 28)`.

- `respostas_base={'EXT-20': {'codigos': ['ANEMIA_HEREDITARIA']}}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `hoje=date(2026, 8, 28)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 213 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calculo['resultado']`, `Triagem.Resultado.DEFINITIVA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 218 — FunctionDef** (nível 1 do bloco).

Define `test_simplificada_nao_reutiliza_estado_de_saude_antigo(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: simplificada nao reutiliza estado de saude antigo.

Bloco `body` da linha 218:

**Linha 219 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 221 — Assign** (nível 2 do bloco).

Associa `calculo` a a chamada `avaliar_triagem`; argumentos posicionais: `Triagem.Modalidade.SIMPLIFICADA`, `{'SIM-18': {'codigos': ['ENTENDO']}}`; argumentos nomeados: `respostas_base={'EXT-12': {'codigos': ['PERSISTENTE']}}`, `hoje=date(2026, 8, 28)`.

- `respostas_base={'EXT-12': {'codigos': ['PERSISTENTE']}}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `hoje=date(2026, 8, 28)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 230 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calculo['resultado']`, `Triagem.Resultado.SEM_IMPEDIMENTO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 235 — FunctionDef** (nível 1 do bloco).

Define `test_resultado_sem_achados_mantem_aviso_presencial(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: resultado sem achados mantem aviso presencial.

Bloco `body` da linha 235:

**Linha 236 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 238 — Assign** (nível 2 do bloco).

Associa `calculo` a a chamada `avaliar_triagem`; argumentos posicionais: `Triagem.Modalidade.EXTENSA`, `{'EXT-51': {'codigos': ['CONFIRMAR']}}`; argumentos nomeados: `hoje=date(2026, 8, 28)`.

- `hoje=date(2026, 8, 28)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 244 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calculo['resultado']`, `Triagem.Resultado.SEM_IMPEDIMENTO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 248 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'decisão final'`, `calculo['mensagem']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 249 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotIn`; argumentos posicionais: `'apto'`, `calculo['mensagem'].lower()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

