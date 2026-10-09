# accounts/test_triagem_catalogos.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

**Arquivo original:** [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""Testes que impedem perguntas ou alternativas de desaparecerem do catálogo."""

from django.test import SimpleTestCase

from .triagem_catalogo import (
    PERGUNTAS_EXTENSAS,
    PERGUNTAS_SIMPLIFICADAS,
    todas_as_perguntas,
    validar_catalogos,
)


IDS_EXTENSOS = {
    "EXT-01", "EXT-01A", "EXT-02", "EXT-03", "EXT-04", "EXT-05", "EXT-05A",
    "EXT-05B", "EXT-06", "EXT-07", "EXT-07A", "EXT-08", "EXT-09",
    "EXT-10", "EXT-11", "EXT-11A", "EXT-12", "EXT-13", "EXT-14",
    "EXT-15", "EXT-16", "EXT-17", "EXT-18", "EXT-19", "EXT-20",
    "EXT-21", "EXT-22", "EXT-23", "EXT-24", "EXT-25", "EXT-26",
    "EXT-27", "EXT-28", "EXT-29", "EXT-30", "EXT-31", "EXT-32",
    "EXT-33", "EXT-34", "EXT-35", "EXT-36", "EXT-37", "EXT-38",
    "EXT-39", "EXT-40", "EXT-41", "EXT-42", "EXT-43", "EXT-44",
    "EXT-45", "EXT-46", "EXT-47", "EXT-48", "EXT-49", "EXT-50",
    "EXT-51",
}

IDS_SIMPLIFICADOS = {
    f"SIM-{numero:02d}"
    for numero in range(1, 19)
}


class CatalogosTriagemTests(SimpleTestCase):
    """Valida a estrutura consumida pelo formulário, serviço e motor."""

    def test_catalogo_extenso_possui_todas_as_56_entradas(self):
        """Falha se qualquer pergunta extensa da especificação for omitida."""

        self.assertEqual(set(PERGUNTAS_EXTENSAS), IDS_EXTENSOS)

    def test_catalogo_simplificado_possui_todas_as_18_entradas(self):
        """Falha se a versão rápida ficar incompleta."""

        self.assertEqual(set(PERGUNTAS_SIMPLIFICADAS), IDS_SIMPLIFICADOS)

    def test_perguntas_possuem_conteudo_e_rastreabilidade(self):
        """Falha se uma pergunta não puder ser exibida ou auditada."""

        for pergunta in todas_as_perguntas():
            self.assertTrue(pergunta["titulo"], pergunta["id"])
            self.assertTrue(pergunta["texto"], pergunta["id"])
            self.assertTrue(pergunta["explicacao"], pergunta["id"])
            self.assertTrue(pergunta["fonte"], pergunta["id"])
            self.assertEqual(
                pergunta["regra_version"],
                "HEMOMINAS_2026_08",
                pergunta["id"],
            )

            if pergunta["tipo"] not in {"data", "numero", "texto"}:
                self.assertTrue(pergunta["opcoes"], pergunta["id"])

    def test_codigos_de_opcao_nao_se_repetem_na_mesma_pergunta(self):
        """Falha se dois rótulos diferentes forem salvos com o mesmo código."""

        for pergunta in todas_as_perguntas():
            codigos = [opcao["codigo"] for opcao in pergunta["opcoes"]]
            self.assertEqual(len(codigos), len(set(codigos)), pergunta["id"])

    def test_destinos_da_simplificada_existem_no_catalogo_extenso(self):
        """Falha se a versão rápida tentar abrir uma pergunta inexistente."""

        for pergunta in PERGUNTAS_SIMPLIFICADAS.values():
            for destinos in pergunta["abrir_extensa"].values():
                for destino in destinos:
                    self.assertIn(destino, PERGUNTAS_EXTENSAS)

    def test_funcao_de_validacao_aceita_os_catalogos_oficiais(self):
        """Falha se o catálogo publicado violar seu próprio contrato."""

        self.assertIsNone(validar_catalogos())
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 1

```python
"""Testes que impedem perguntas ou alternativas de desaparecerem do catálogo."""
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

### ImportFrom — linhas 5 a 10

```python
from .triagem_catalogo import (
    PERGUNTAS_EXTENSAS,
    PERGUNTAS_SIMPLIFICADAS,
    todas_as_perguntas,
    validar_catalogos,
)
```

**Explicação deste trecho:**

**Linha 5 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_catalogo` os nomes `PERGUNTAS_EXTENSAS`, `PERGUNTAS_SIMPLIFICADAS`, `todas_as_perguntas`, `validar_catalogos`. Pontos iniciais indicam importação relativa ao pacote.

### Assign — linhas 13 a 24

```python
IDS_EXTENSOS = {
    "EXT-01", "EXT-01A", "EXT-02", "EXT-03", "EXT-04", "EXT-05", "EXT-05A",
    "EXT-05B", "EXT-06", "EXT-07", "EXT-07A", "EXT-08", "EXT-09",
    "EXT-10", "EXT-11", "EXT-11A", "EXT-12", "EXT-13", "EXT-14",
    "EXT-15", "EXT-16", "EXT-17", "EXT-18", "EXT-19", "EXT-20",
    "EXT-21", "EXT-22", "EXT-23", "EXT-24", "EXT-25", "EXT-26",
    "EXT-27", "EXT-28", "EXT-29", "EXT-30", "EXT-31", "EXT-32",
    "EXT-33", "EXT-34", "EXT-35", "EXT-36", "EXT-37", "EXT-38",
    "EXT-39", "EXT-40", "EXT-41", "EXT-42", "EXT-43", "EXT-44",
    "EXT-45", "EXT-46", "EXT-47", "EXT-48", "EXT-49", "EXT-50",
    "EXT-51",
}
```

**Explicação deste trecho:**

**Linha 13 — Assign** (nível 0 do bloco).

Associa `IDS_EXTENSOS` a uma coleção Set com 56 itens, na expressão `{'EXT-01', 'EXT-01A', 'EXT-02', 'EXT-03', 'EXT-04', 'EXT-05', 'EXT-05A', 'EXT-05B', 'EXT-06', 'EXT-07', 'EXT-07A', 'EXT-08', 'EXT-09', 'EXT-10', 'EXT-11', 'EXT-11A', 'EXT-12', 'EXT-13', 'EXT-14', 'EXT-15', 'EXT-16', 'EXT-17', 'EXT-18', 'EXT-19', 'EXT-20', 'EXT-21', 'EXT-22', 'EXT-23', 'EXT-24', 'EXT-25', 'EXT-26', 'EXT-27', 'EXT-28', 'EXT-29', 'EXT-30', 'EXT-31', 'EXT-32', 'EXT-33', 'EXT-34', 'EXT-35', 'EXT-36', 'EXT-37', 'EXT-38', 'EXT-39', 'EXT-40', 'EXT-41', 'EXT-42', 'EXT-43', 'EXT-44', 'EXT-45', 'EXT-46', 'EXT-47', 'EXT-48', 'EXT-49', 'EXT-50', 'EXT-51'}`.

### Assign — linhas 26 a 29

```python
IDS_SIMPLIFICADOS = {
    f"SIM-{numero:02d}"
    for numero in range(1, 19)
}
```

**Explicação deste trecho:**

**Linha 26 — Assign** (nível 0 do bloco).

Associa `IDS_SIMPLIFICADOS` a uma coleção/gerador construído por compreensão em `{f'SIM-{numero:02d}' for numero in range(1, 19)}`: percorre as fontes e aplica os filtros declarados.

### CatalogosTriagemTests — linhas 32 a 80

```python
class CatalogosTriagemTests(SimpleTestCase):
    """Valida a estrutura consumida pelo formulário, serviço e motor."""

    def test_catalogo_extenso_possui_todas_as_56_entradas(self):
        """Falha se qualquer pergunta extensa da especificação for omitida."""

        self.assertEqual(set(PERGUNTAS_EXTENSAS), IDS_EXTENSOS)

    def test_catalogo_simplificado_possui_todas_as_18_entradas(self):
        """Falha se a versão rápida ficar incompleta."""

        self.assertEqual(set(PERGUNTAS_SIMPLIFICADAS), IDS_SIMPLIFICADOS)

    def test_perguntas_possuem_conteudo_e_rastreabilidade(self):
        """Falha se uma pergunta não puder ser exibida ou auditada."""

        for pergunta in todas_as_perguntas():
            self.assertTrue(pergunta["titulo"], pergunta["id"])
            self.assertTrue(pergunta["texto"], pergunta["id"])
            self.assertTrue(pergunta["explicacao"], pergunta["id"])
            self.assertTrue(pergunta["fonte"], pergunta["id"])
            self.assertEqual(
                pergunta["regra_version"],
                "HEMOMINAS_2026_08",
                pergunta["id"],
            )

            if pergunta["tipo"] not in {"data", "numero", "texto"}:
                self.assertTrue(pergunta["opcoes"], pergunta["id"])

    def test_codigos_de_opcao_nao_se_repetem_na_mesma_pergunta(self):
        """Falha se dois rótulos diferentes forem salvos com o mesmo código."""

        for pergunta in todas_as_perguntas():
            codigos = [opcao["codigo"] for opcao in pergunta["opcoes"]]
            self.assertEqual(len(codigos), len(set(codigos)), pergunta["id"])

    def test_destinos_da_simplificada_existem_no_catalogo_extenso(self):
        """Falha se a versão rápida tentar abrir uma pergunta inexistente."""

        for pergunta in PERGUNTAS_SIMPLIFICADAS.values():
            for destinos in pergunta["abrir_extensa"].values():
                for destino in destinos:
                    self.assertIn(destino, PERGUNTAS_EXTENSAS)

    def test_funcao_de_validacao_aceita_os_catalogos_oficiais(self):
        """Falha se o catálogo publicado violar seu próprio contrato."""

        self.assertIsNone(validar_catalogos())
```

**Explicação deste trecho:**

**Linha 32 — ClassDef** (nível 0 do bloco).

Define a classe `CatalogosTriagemTests` herdando de `SimpleTestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 32:

**Linha 33 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 35 — FunctionDef** (nível 1 do bloco).

Define `test_catalogo_extenso_possui_todas_as_56_entradas(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: catalogo extenso possui todas as 56 entradas.

Bloco `body` da linha 35:

**Linha 36 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 38 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `set(PERGUNTAS_EXTENSAS)`, `IDS_EXTENSOS`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 40 — FunctionDef** (nível 1 do bloco).

Define `test_catalogo_simplificado_possui_todas_as_18_entradas(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: catalogo simplificado possui todas as 18 entradas.

Bloco `body` da linha 40:

**Linha 41 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 43 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `set(PERGUNTAS_SIMPLIFICADAS)`, `IDS_SIMPLIFICADOS`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 45 — FunctionDef** (nível 1 do bloco).

Define `test_perguntas_possuem_conteudo_e_rastreabilidade(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: perguntas possuem conteudo e rastreabilidade.

Bloco `body` da linha 45:

**Linha 46 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 48 — For** (nível 2 do bloco).

Percorre `todas_as_perguntas()`; cada item é atribuído a `pergunta` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 48:

**Linha 49 — Expr** (nível 3 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `pergunta['titulo']`, `pergunta['id']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 50 — Expr** (nível 3 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `pergunta['texto']`, `pergunta['id']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 51 — Expr** (nível 3 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `pergunta['explicacao']`, `pergunta['id']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 52 — Expr** (nível 3 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `pergunta['fonte']`, `pergunta['id']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 53 — Expr** (nível 3 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pergunta['regra_version']`, `'HEMOMINAS_2026_08'`, `pergunta['id']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 59 — If** (nível 3 do bloco).

Escolhe um caminho verificando a comparação `pergunta['tipo']` não contido em `{'data', 'numero', 'texto'}`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 59:

**Linha 60 — Expr** (nível 4 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `pergunta['opcoes']`, `pergunta['id']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 62 — FunctionDef** (nível 1 do bloco).

Define `test_codigos_de_opcao_nao_se_repetem_na_mesma_pergunta(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: codigos de opcao nao se repetem na mesma pergunta.

Bloco `body` da linha 62:

**Linha 63 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 65 — For** (nível 2 do bloco).

Percorre `todas_as_perguntas()`; cada item é atribuído a `pergunta` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 65:

**Linha 66 — Assign** (nível 3 do bloco).

Associa `codigos` a uma coleção/gerador construído por compreensão em `[opcao['codigo'] for opcao in pergunta['opcoes']]`: percorre as fontes e aplica os filtros declarados.

**Linha 67 — Expr** (nível 3 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `len(codigos)`, `len(set(codigos))`, `pergunta['id']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 69 — FunctionDef** (nível 1 do bloco).

Define `test_destinos_da_simplificada_existem_no_catalogo_extenso(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: destinos da simplificada existem no catalogo extenso.

Bloco `body` da linha 69:

**Linha 70 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 72 — For** (nível 2 do bloco).

Percorre `PERGUNTAS_SIMPLIFICADAS.values()`; cada item é atribuído a `pergunta` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 72:

**Linha 73 — For** (nível 3 do bloco).

Percorre `pergunta['abrir_extensa'].values()`; cada item é atribuído a `destinos` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 73:

**Linha 74 — For** (nível 4 do bloco).

Percorre `destinos`; cada item é atribuído a `destino` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 74:

**Linha 75 — Expr** (nível 5 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `destino`, `PERGUNTAS_EXTENSAS`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 77 — FunctionDef** (nível 1 do bloco).

Define `test_funcao_de_validacao_aceita_os_catalogos_oficiais(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: funcao de validacao aceita os catalogos oficiais.

Bloco `body` da linha 77:

**Linha 78 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 80 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIsNone`; argumentos posicionais: `validar_catalogos()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

