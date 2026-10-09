# accounts/test_triagem_models.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

**Arquivo original:** [accounts/test_triagem_models.py](<C:/Users/lb119/Elo/accounts/test_triagem_models.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
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
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 1

```python
"""Testes da persistência das triagens e de suas respostas."""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 3 a 3

```python
from django.db import IntegrityError, transaction
```

**Explicação deste trecho:**

**Linha 3 — ImportFrom** (nível 0 do bloco).

Importa de `django.db` os nomes `IntegrityError`, `transaction`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 4 a 4

```python
from django.test import TestCase
```

**Explicação deste trecho:**

**Linha 4 — ImportFrom** (nível 0 do bloco).

Importa de `django.test` os nomes `TestCase`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 6 a 6

```python
from .models import RespostaTriagem, Triagem, Usuario
```

**Explicação deste trecho:**

**Linha 6 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `RespostaTriagem`, `Triagem`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

### TriagemModelTests — linhas 9 a 76

```python
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
```

**Explicação deste trecho:**

**Linha 9 — ClassDef** (nível 0 do bloco).

Define a classe `TriagemModelTests` herdando de `TestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 9:

**Linha 10 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 12 — FunctionDef** (nível 1 do bloco).

Define `setUp(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 12:

**Linha 14 — Assign** (nível 2 do bloco).

Associa `self.usuario` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email='model-triagem@teste.com'`, `password='SenhaForte123!'`, `nome='Pessoa em Triagem'`, `perfil=Usuario.Perfil.DOADOR`.

- `email='model-triagem@teste.com'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `password='SenhaForte123!'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Pessoa em Triagem'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.DOADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 21 — FunctionDef** (nível 1 do bloco).

Define `test_nova_triagem_comeca_em_andamento(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: nova triagem comeca em andamento.

Bloco `body` da linha 21:

**Linha 22 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 24 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.usuario`, `modalidade=Triagem.Modalidade.EXTENSA`.

- `usuario=self.usuario`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `modalidade=Triagem.Modalidade.EXTENSA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 29 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.status`, `Triagem.Status.EM_ANDAMENTO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 33 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.pergunta_atual`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 34 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.fluxo_perguntas`, `[]`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 35 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.resultado`, `''`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 37 — FunctionDef** (nível 1 do bloco).

Define `test_uma_pergunta_tem_uma_unica_resposta_por_triagem(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: uma pergunta tem uma unica resposta por triagem.

Bloco `body` da linha 37:

**Linha 38 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 40 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.usuario`, `modalidade=Triagem.Modalidade.EXTENSA`.

- `usuario=self.usuario`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `modalidade=Triagem.Modalidade.EXTENSA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 44 — Expr** (nível 2 do bloco).

Executa a chamada `RespostaTriagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `triagem=triagem`, `id_pergunta='EXT-01'`, `codigo_resposta='SIM'`, `resposta_label='Sim'`, `valor={'codigos': ['SIM']}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 53 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(IntegrityError)`, `transaction.atomic()`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 53:

**Linha 54 — Expr** (nível 3 do bloco).

Executa a chamada `RespostaTriagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `triagem=triagem`, `id_pergunta='EXT-01'`, `codigo_resposta='NAO'`, `resposta_label='Não'`, `valor={'codigos': ['NAO']}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 62 — FunctionDef** (nível 1 do bloco).

Define `test_triagem_simplificada_pode_apontar_para_extensa_base(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: triagem simplificada pode apontar para extensa base.

Bloco `body` da linha 62:

**Linha 63 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 65 — Assign** (nível 2 do bloco).

Associa `extensa` a a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.usuario`, `modalidade=Triagem.Modalidade.EXTENSA`.

- `usuario=self.usuario`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `modalidade=Triagem.Modalidade.EXTENSA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 69 — Assign** (nível 2 do bloco).

Associa `simplificada` a a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.usuario`, `modalidade=Triagem.Modalidade.SIMPLIFICADA`, `triagem_base=extensa`.

- `usuario=self.usuario`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `modalidade=Triagem.Modalidade.SIMPLIFICADA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `triagem_base=extensa`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 75 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `simplificada.triagem_base`, `extensa`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 76 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `simplificada`, `extensa.verificacoes_simplificadas.all()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 13: `# Cada teste usa uma conta real do model personalizado do projeto.`
- Linha 52: `# O bloco atomic mantém o TestCase utilizável após o IntegrityError.`

