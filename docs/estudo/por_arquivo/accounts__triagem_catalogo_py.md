# accounts/triagem_catalogo.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Acesso e validacao dos catalogos versionados.

**Arquivo original:** [accounts/triagem_catalogo.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""Acesso único aos catálogos extensa e simplificado da triagem."""

from .triagem_catalogo_extensa import PERGUNTAS_EXTENSAS, REGRA_VERSION
from .triagem_catalogo_simplificada import PERGUNTAS_SIMPLIFICADAS


def obter_catalogo(modalidade):
    """Retorna o catálogo adequado e rejeita modalidade desconhecida."""

    if modalidade == "EXTENSA":
        return PERGUNTAS_EXTENSAS
    if modalidade == "SIMPLIFICADA":
        return PERGUNTAS_SIMPLIFICADAS
    raise ValueError("Modalidade de triagem inválida.")


def obter_pergunta(id_pergunta):
    """Localiza uma pergunta pelo identificador estável."""

    pergunta = PERGUNTAS_EXTENSAS.get(id_pergunta)
    if pergunta is None:
        pergunta = PERGUNTAS_SIMPLIFICADAS.get(id_pergunta)
    if pergunta is None:
        raise KeyError(f"Pergunta inexistente: {id_pergunta}")
    return pergunta


def todas_as_perguntas():
    """Fornece todas as perguntas para validação e auditoria."""

    return [
        *PERGUNTAS_EXTENSAS.values(),
        *PERGUNTAS_SIMPLIFICADAS.values(),
    ]


def validar_catalogos():
    """Interrompe a inicialização de testes se o catálogo estiver incoerente."""

    for pergunta in todas_as_perguntas():
        if pergunta["id"] not in (
            PERGUNTAS_EXTENSAS | PERGUNTAS_SIMPLIFICADAS
        ):
            raise ValueError("O identificador interno não corresponde à chave.")

        codigos = [opcao["codigo"] for opcao in pergunta["opcoes"]]
        if len(codigos) != len(set(codigos)):
            raise ValueError(
                f"Há alternativas duplicadas em {pergunta['id']}."
            )

        desconhecidos = set(pergunta["regras"]) - set(codigos)
        if desconhecidos:
            raise ValueError(
                f"Há regras para alternativas inexistentes em {pergunta['id']}."
            )

        for destinos in pergunta["abrir_extensa"].values():
            for destino in destinos:
                if destino not in PERGUNTAS_EXTENSAS:
                    raise ValueError(
                        f"Destino {destino} inexistente em {pergunta['id']}."
                    )

    return None


# Compatibilidade com o nome usado na primeira implementação.
TRIAGEM_RULE_VERSION = REGRA_VERSION
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 1

```python
"""Acesso único aos catálogos extensa e simplificado da triagem."""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 3 a 3

```python
from .triagem_catalogo_extensa import PERGUNTAS_EXTENSAS, REGRA_VERSION
```

**Explicação deste trecho:**

**Linha 3 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_catalogo_extensa` os nomes `PERGUNTAS_EXTENSAS`, `REGRA_VERSION`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 4 a 4

```python
from .triagem_catalogo_simplificada import PERGUNTAS_SIMPLIFICADAS
```

**Explicação deste trecho:**

**Linha 4 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_catalogo_simplificada` os nomes `PERGUNTAS_SIMPLIFICADAS`. Pontos iniciais indicam importação relativa ao pacote.

### obter_catalogo — linhas 7 a 14

```python
def obter_catalogo(modalidade):
    """Retorna o catálogo adequado e rejeita modalidade desconhecida."""

    if modalidade == "EXTENSA":
        return PERGUNTAS_EXTENSAS
    if modalidade == "SIMPLIFICADA":
        return PERGUNTAS_SIMPLIFICADAS
    raise ValueError("Modalidade de triagem inválida.")
```

**Explicação deste trecho:**

**Linha 7 — FunctionDef** (nível 0 do bloco).

Define `obter_catalogo(modalidade)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 7:

**Linha 8 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 10 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `modalidade` igual a `'EXTENSA'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 10:

**Linha 11 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `PERGUNTAS_EXTENSAS` ao chamador.

**Linha 12 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `modalidade` igual a `'SIMPLIFICADA'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 12:

**Linha 13 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `PERGUNTAS_SIMPLIFICADAS` ao chamador.

**Linha 14 — Raise** (nível 1 do bloco).

Interrompe o caminho levantando a chamada `ValueError`; argumentos posicionais: `'Modalidade de triagem inválida.'`.

### obter_pergunta — linhas 17 a 25

```python
def obter_pergunta(id_pergunta):
    """Localiza uma pergunta pelo identificador estável."""

    pergunta = PERGUNTAS_EXTENSAS.get(id_pergunta)
    if pergunta is None:
        pergunta = PERGUNTAS_SIMPLIFICADAS.get(id_pergunta)
    if pergunta is None:
        raise KeyError(f"Pergunta inexistente: {id_pergunta}")
    return pergunta
```

**Explicação deste trecho:**

**Linha 17 — FunctionDef** (nível 0 do bloco).

Define `obter_pergunta(id_pergunta)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 17:

**Linha 18 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 20 — Assign** (nível 1 do bloco).

Associa `pergunta` a a chamada `PERGUNTAS_EXTENSAS.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `id_pergunta`.


**Linha 21 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `pergunta` o mesmo objeto que `None`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 21:

**Linha 22 — Assign** (nível 2 do bloco).

Associa `pergunta` a a chamada `PERGUNTAS_SIMPLIFICADAS.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `id_pergunta`.


**Linha 23 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `pergunta` o mesmo objeto que `None`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 23:

**Linha 24 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `KeyError`; argumentos posicionais: `f'Pergunta inexistente: {id_pergunta}'`.

**Linha 25 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `pergunta` ao chamador.

### todas_as_perguntas — linhas 28 a 34

```python
def todas_as_perguntas():
    """Fornece todas as perguntas para validação e auditoria."""

    return [
        *PERGUNTAS_EXTENSAS.values(),
        *PERGUNTAS_SIMPLIFICADAS.values(),
    ]
```

**Explicação deste trecho:**

**Linha 28 — FunctionDef** (nível 0 do bloco).

Define `todas_as_perguntas()`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 28:

**Linha 29 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 31 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve uma coleção List com 2 itens, na expressão `[*PERGUNTAS_EXTENSAS.values(), *PERGUNTAS_SIMPLIFICADAS.values()]` ao chamador.

### validar_catalogos — linhas 37 a 65

```python
def validar_catalogos():
    """Interrompe a inicialização de testes se o catálogo estiver incoerente."""

    for pergunta in todas_as_perguntas():
        if pergunta["id"] not in (
            PERGUNTAS_EXTENSAS | PERGUNTAS_SIMPLIFICADAS
        ):
            raise ValueError("O identificador interno não corresponde à chave.")

        codigos = [opcao["codigo"] for opcao in pergunta["opcoes"]]
        if len(codigos) != len(set(codigos)):
            raise ValueError(
                f"Há alternativas duplicadas em {pergunta['id']}."
            )

        desconhecidos = set(pergunta["regras"]) - set(codigos)
        if desconhecidos:
            raise ValueError(
                f"Há regras para alternativas inexistentes em {pergunta['id']}."
            )

        for destinos in pergunta["abrir_extensa"].values():
            for destino in destinos:
                if destino not in PERGUNTAS_EXTENSAS:
                    raise ValueError(
                        f"Destino {destino} inexistente em {pergunta['id']}."
                    )

    return None
```

**Explicação deste trecho:**

**Linha 37 — FunctionDef** (nível 0 do bloco).

Define `validar_catalogos()`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 37:

**Linha 38 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 40 — For** (nível 1 do bloco).

Percorre `todas_as_perguntas()`; cada item é atribuído a `pergunta` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 40:

**Linha 41 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `pergunta['id']` não contido em `PERGUNTAS_EXTENSAS | PERGUNTAS_SIMPLIFICADAS`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 41:

**Linha 44 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `ValueError`; argumentos posicionais: `'O identificador interno não corresponde à chave.'`.

**Linha 46 — Assign** (nível 2 do bloco).

Associa `codigos` a uma coleção/gerador construído por compreensão em `[opcao['codigo'] for opcao in pergunta['opcoes']]`: percorre as fontes e aplica os filtros declarados.

**Linha 47 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `len(codigos)` diferente de `len(set(codigos))`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 47:

**Linha 48 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `ValueError`; argumentos posicionais: `f"Há alternativas duplicadas em {pergunta['id']}."`.

**Linha 52 — Assign** (nível 2 do bloco).

Associa `desconhecidos` a a expressão `set(pergunta['regras']) - set(codigos)`; seus operadores determinam o cálculo.

**Linha 53 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `desconhecidos`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 53:

**Linha 54 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `ValueError`; argumentos posicionais: `f"Há regras para alternativas inexistentes em {pergunta['id']}."`.

**Linha 58 — For** (nível 2 do bloco).

Percorre `pergunta['abrir_extensa'].values()`; cada item é atribuído a `destinos` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 58:

**Linha 59 — For** (nível 3 do bloco).

Percorre `destinos`; cada item é atribuído a `destino` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 59:

**Linha 60 — If** (nível 4 do bloco).

Escolhe um caminho verificando a comparação `destino` não contido em `PERGUNTAS_EXTENSAS`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 60:

**Linha 61 — Raise** (nível 5 do bloco).

Interrompe o caminho levantando a chamada `ValueError`; argumentos posicionais: `f"Destino {destino} inexistente em {pergunta['id']}."`.

**Linha 65 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

### Assign — linhas 69 a 69

```python
TRIAGEM_RULE_VERSION = REGRA_VERSION
```

**Explicação deste trecho:**

**Linha 69 — Assign** (nível 0 do bloco).

Associa `TRIAGEM_RULE_VERSION` a o valor associado ao nome `REGRA_VERSION`.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 68: `# Compatibilidade com o nome usado na primeira implementação.`

