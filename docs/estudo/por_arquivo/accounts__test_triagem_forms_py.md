# accounts/test_triagem_forms.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

**Arquivo original:** [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
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
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 1

```python
"""Testes do formulário construído a partir do catálogo."""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 3 a 3

```python
from django.test import SimpleTestCase
```

**Explicação deste trecho:**

**Linha 3 — ImportFrom** (nível 0 do bloco).

Importa de `django.test` os nomes `SimpleTestCase`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 5 a 5

```python
from .triagem_catalogo import obter_pergunta
```

**Explicação deste trecho:**

**Linha 5 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_catalogo` os nomes `obter_pergunta`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 6 a 6

```python
from .triagem_forms import FormularioPergunta
```

**Explicação deste trecho:**

**Linha 6 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_forms` os nomes `FormularioPergunta`. Pontos iniciais indicam importação relativa ao pacote.

### FormularioPerguntaTests — linhas 9 a 118

```python
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
```

**Explicação deste trecho:**

**Linha 9 — ClassDef** (nível 0 do bloco).

Define a classe `FormularioPerguntaTests` herdando de `SimpleTestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 9:

**Linha 10 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 12 — FunctionDef** (nível 1 do bloco).

Define `test_escolha_com_data_e_normalizada(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: escolha com data e normalizada.

Bloco `body` da linha 12:

**Linha 13 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 15 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `FormularioPergunta`; argumentos posicionais: `obter_pergunta('EXT-05A')`; argumentos nomeados: `data={'resposta': 'DATA', 'data_DATA': '2026-08-01'}`.

- `data={'resposta': 'DATA', 'data_DATA': '2026-08-01'}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 23 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `form.is_valid()`, `form.errors`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 24 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `form.cleaned_data['valor']`, `{'codigos': ['DATA'], 'datas': {'DATA': '2026-08-01'}, 'detalhes': ''}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 33 — FunctionDef** (nível 1 do bloco).

Define `test_selecao_multipla_preserva_uma_data_por_item(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: selecao multipla preserva uma data por item.

Bloco `body` da linha 33:

**Linha 34 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 36 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `FormularioPergunta`; argumentos posicionais: `obter_pergunta('EXT-48')`; argumentos nomeados: `data={'resposta': ['DENGUE', 'FEBRE_AMARELA'], 'data_DENGUE': '2026-08-01', 'data_FEBRE_AMARELA': '2026-08-10'}`.

- `data={'resposta': ['DENGUE', 'FEBRE_AMARELA'], 'data_DENGUE': '2026-08-01', 'data_FEBRE_AMARELA': '2026-08-10'}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 45 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `form.is_valid()`, `form.errors`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 46 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `form.cleaned_data['valor']['datas']`, `{'DENGUE': '2026-08-01', 'FEBRE_AMARELA': '2026-08-10'}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 54 — FunctionDef** (nível 1 do bloco).

Define `test_data_futura_e_rejeitada(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: data futura e rejeitada.

Bloco `body` da linha 54:

**Linha 55 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 57 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `FormularioPergunta`; argumentos posicionais: `obter_pergunta('EXT-05A')`; argumentos nomeados: `data={'resposta': 'DATA', 'data_DATA': '2999-01-01'}`.

- `data={'resposta': 'DATA', 'data_DATA': '2999-01-01'}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 65 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `form.is_valid()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 66 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'data_DATA'`, `form.errors`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 68 — FunctionDef** (nível 1 do bloco).

Define `test_alternativa_com_prazo_exige_sua_data(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: alternativa com prazo exige sua data.

Bloco `body` da linha 68:

**Linha 69 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 71 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `FormularioPergunta`; argumentos posicionais: `obter_pergunta('EXT-48')`; argumentos nomeados: `data={'resposta': ['DENGUE']}`.

- `data={'resposta': ['DENGUE']}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 76 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `form.is_valid()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 77 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'data_DENGUE'`, `form.errors`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 79 — FunctionDef** (nível 1 do bloco).

Define `test_nenhuma_nao_pode_ser_marcada_com_uma_condicao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: nenhuma nao pode ser marcada com uma condicao.

Bloco `body` da linha 79:

**Linha 80 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 82 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `FormularioPergunta`; argumentos posicionais: `obter_pergunta('EXT-20')`; argumentos nomeados: `data={'resposta': ['NENHUMA', 'ANEMIA_HEREDITARIA']}`.

- `data={'resposta': ['NENHUMA', 'ANEMIA_HEREDITARIA']}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 89 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `form.is_valid()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 90 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'resposta'`, `form.errors`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 92 — FunctionDef** (nível 1 do bloco).

Define `test_descricao_e_obrigatoria_quando_usuario_informa_outra_condicao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: descricao e obrigatoria quando usuario informa outra condicao.

Bloco `body` da linha 92:

**Linha 93 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 95 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `FormularioPergunta`; argumentos posicionais: `obter_pergunta('EXT-50')`; argumentos nomeados: `data={'resposta': 'SIM', 'detalhes': ''}`.

- `data={'resposta': 'SIM', 'detalhes': ''}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 100 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `form.is_valid()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 101 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'detalhes'`, `form.errors`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 103 — FunctionDef** (nível 1 do bloco).

Define `test_procedimento_estetico_registra_seguranca_e_inflamacao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: procedimento estetico registra seguranca e inflamacao.

Bloco `body` da linha 103:

**Linha 104 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 106 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `FormularioPergunta`; argumentos posicionais: `obter_pergunta('EXT-24')`; argumentos nomeados: `data={'resposta': ['BOTOX'], 'data_BOTOX': '2026-08-01', 'seguranca': 'SIM', 'inflamacao': 'NAO'}`.

- `data={'resposta': ['BOTOX'], 'data_BOTOX': '2026-08-01', 'seguranca': 'SIM', 'inflamacao': 'NAO'}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 116 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `form.is_valid()`, `form.errors`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 117 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `form.cleaned_data['valor']['seguranca']`, `'SIM'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 118 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `form.cleaned_data['valor']['inflamacao']`, `'NAO'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

