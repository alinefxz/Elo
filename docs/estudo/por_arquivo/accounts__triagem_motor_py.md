# accounts/triagem_motor.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Calculo da orientacao a partir das respostas e regras dos catalogos.

**Arquivo original:** [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
#Este arquivo é o motor que calcula o resultado da triagem.

# - Recebe as respostas e não acessa diretamente o banco de dados.
# - Usa as regras declaradas no catálogo de perguntas.
# - Cria achados para cada condição identificada.
# - Calcula prazos em horas, dias, semanas, meses ou anos.
# - Solicita avaliação quando falta uma data necessária.
# - Aplica regras específicas de intervalo entre doações.
# - Verifica limites de doações nos últimos 12 meses.
# - Analisa procedimentos estéticos e prazos de segurança.
# - Na triagem simplificada, reutiliza somente respostas estáveis da extensa.
# - Mantém todos os achados encontrados.
# - Escolhe sempre o resultado mais restritivo.
# - Calcula a data de liberação mais distante, quando existir.
# - Retorna resultado, mensagem, achados, data e versão das regras.

# Este motor apenas calcula a orientação. O resultado não substitui a avaliação clínica final do Hemocentro.

"""Motor puro que transforma respostas em orientação de triagem.

O módulo não acessa o banco. Isso torna os cálculos repetíveis e permite manter
o histórico antigo ligado à versão de regra que produziu cada resultado.
"""

import calendar
import math
from datetime import date, datetime, timedelta

from .models import Triagem
from .triagem_catalogo import (
    TRIAGEM_RULE_VERSION,
    obter_pergunta,
)


# Um resultado mais restritivo sempre prevalece, mas nenhum achado é apagado.
PRIORIDADE_RESULTADOS = (
    Triagem.Resultado.DEFINITIVA,
    Triagem.Resultado.AVALIACAO,
    Triagem.Resultado.TEMPORARIA,
    Triagem.Resultado.DOCUMENTACAO,
)


# Estes dados mudam rapidamente e nunca são herdados pela versão simplificada.
PERGUNTAS_NAO_REUTILIZAVEIS = {
    "EXT-08",
    "EXT-09",
    "EXT-10",
    "EXT-11",
    "EXT-11A",
    "EXT-12",
    "EXT-13",
    "EXT-14",
    "EXT-15",
    "EXT-16",
    "EXT-17",
    "EXT-18",
    "EXT-19",
    "EXT-33",
    "EXT-44",
}


MENSAGENS_RESULTADO = {
    Triagem.Resultado.SEM_IMPEDIMENTO: (
        "Com base no que você informou, não identificamos um impedimento "
        "nesta orientação. Isso não significa liberação para doar: a decisão "
        "final será tomada pela equipe do hemocentro."
    ),
    Triagem.Resultado.TEMPORARIA: (
        "Encontramos uma condição com prazo de espera. A data apresentada é "
        "orientativa e só vale se você estiver recuperado(a) e não houver "
        "outro impedimento. A decisão final é do hemocentro."
    ),
    Triagem.Resultado.DEFINITIVA: (
        "Uma condição informada é classificada como impedimento definitivo "
        "pela regra consultada. Confirme a orientação com um serviço oficial, "
        "pois normas e diagnósticos podem precisar de atualização."
    ),
    Triagem.Resultado.AVALIACAO: (
        "Sua resposta depende de avaliação profissional, relatório, exame ou "
        "detalhe que o sistema não consegue confirmar com segurança. A decisão "
        "final será feita no hemocentro."
    ),
    Triagem.Resultado.DOCUMENTACAO: (
        "Existe uma exigência de documentação ou conferência presencial. Isso "
        "não substitui a avaliação clínica da equipe do hemocentro."
    ),
}


def escolher_resultado(achados):
    """Escolhe o estado principal sem descartar os demais achados."""

    encontrados = {achado["resultado"] for achado in achados}

    for resultado in PRIORIDADE_RESULTADOS:
        if resultado in encontrados:
            return resultado

    return Triagem.Resultado.SEM_IMPEDIMENTO


def _converter_data(valor):
    """Aceita data, datetime ou ISO; valor inválido volta como ausente."""

    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    if not valor:
        return None

    try:
        return date.fromisoformat(str(valor))
    except ValueError:
        return None


def _somar_meses(data_base, quantidade):
    """Soma meses pelo calendário e ajusta dias como 31 de janeiro."""

    indice_mes = data_base.month - 1 + quantidade
    ano = data_base.year + indice_mes // 12
    mes = indice_mes % 12 + 1
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    return date(ano, mes, min(data_base.day, ultimo_dia))


def calcular_data_liberacao(data_base, prazo):
    """Calcula a data final para horas, dias, semanas, meses ou anos."""

    unidade = prazo["unidade"]
    quantidade = prazo["valor"]

    if unidade == "horas":
        # Como o model guarda uma data, qualquer fração de dia é conservadora.
        return data_base + timedelta(days=math.ceil(quantidade / 24))
    if unidade == "dias":
        return data_base + timedelta(days=quantidade)
    if unidade == "semanas":
        return data_base + timedelta(weeks=quantidade)
    if unidade == "meses":
        return _somar_meses(data_base, quantidade)
    if unidade == "anos":
        return _somar_meses(data_base, quantidade * 12)

    raise ValueError(f"Unidade de prazo inválida: {unidade}")


def _data_da_resposta(valor, codigo):
    """Obtém a data específica da alternativa ou a data legada da resposta."""

    datas = valor.get("datas") or {}
    return _converter_data(
        datas.get(codigo) or valor.get("data_evento")
    )


def _novo_achado(
    pergunta,
    codigo,
    resultado,
    mensagem,
    *,
    data_liberacao=None,
    exige_relatorio=False,
):
    """Padroniza a estrutura persistida no campo JSON de achados."""

    achado = {
        "id_pergunta": pergunta["id"],
        "codigo_regra": f"{pergunta['id']}:{codigo}",
        "categoria": pergunta["titulo"],
        "resultado": resultado,
        "mensagem": mensagem,
        "exige_relatorio": exige_relatorio,
        "fonte": pergunta["fonte"],
        "regra_version": TRIAGEM_RULE_VERSION,
    }

    if data_liberacao:
        achado["data_liberacao"] = data_liberacao.isoformat()

    return achado


def _avaliar_regra_declarada(pergunta, codigo, valor, hoje):
    """Avalia uma alternativa simples definida diretamente no catálogo."""

    item_regra = pergunta["regras"].get(codigo)
    if not item_regra:
        return None

    resultado = item_regra["resultado"]
    mensagem = item_regra["mensagem"]
    prazo = item_regra.get("prazo")
    data_final = None

    if prazo:
        if prazo.get("referencia") == "hoje":
            data_base = hoje
        else:
            data_base = _data_da_resposta(valor, codigo)

        # Prazos após cura, dose, alta ou procedimento precisam da data real.
        if data_base is None:
            return _novo_achado(
                pergunta,
                f"{codigo}_SEM_DATA",
                Triagem.Resultado.AVALIACAO,
                "Informe a data do evento ou confirme o prazo presencialmente.",
            )

        data_final = calcular_data_liberacao(data_base, prazo)

        # Um prazo já encerrado não é impedimento atual.
        if (
            resultado == Triagem.Resultado.TEMPORARIA
            and data_final <= hoje
        ):
            return None

    return _novo_achado(
        pergunta,
        codigo,
        resultado,
        mensagem,
        data_liberacao=data_final,
        exige_relatorio=item_regra.get("exige_relatorio", False),
    )


def _primeiro_codigo(respostas, id_pergunta):
    """Retorna a primeira alternativa quando a pergunta é de escolha única."""

    valor = respostas.get(id_pergunta) or {}
    codigos = valor.get("codigos") or []
    return codigos[0] if codigos else None


def _avaliar_intervalo_ultima_doacao(respostas, hoje):
    """Aplica 60/90 dias e a regra adicional de seis meses após os 60."""

    valor = respostas.get("EXT-05A") or {}
    if "DATA" not in (valor.get("codigos") or []):
        return None

    pergunta = obter_pergunta("EXT-05A")
    data_doacao = _data_da_resposta(valor, "DATA")
    if data_doacao is None:
        return _novo_achado(
            pergunta,
            "INTERVALO_SEM_DATA",
            Triagem.Resultado.AVALIACAO,
            "A data da última doação é necessária para calcular o intervalo.",
        )

    sexo = _primeiro_codigo(respostas, "EXT-04")
    idade = _primeiro_codigo(respostas, "EXT-02")
    datas = []

    if sexo == "FEMININO":
        datas.append(data_doacao + timedelta(days=90))
    elif sexo == "MASCULINO":
        datas.append(data_doacao + timedelta(days=60))

    if idade == "61_69":
        datas.append(_somar_meses(data_doacao, 6))

    if not datas:
        return None

    data_final = max(datas)
    if data_final <= hoje:
        return None

    return _novo_achado(
        pergunta,
        "INTERVALO_DOACAO",
        Triagem.Resultado.TEMPORARIA,
        "Ainda não terminou o intervalo orientativo desde a última doação.",
        data_liberacao=data_final,
    )


def _avaliar_limite_doacoes(respostas):
    """Sem datas históricas, sinaliza o limite sem inventar uma liberação."""

    codigo = _primeiro_codigo(respostas, "EXT-05B")
    sexo = _primeiro_codigo(respostas, "EXT-04")

    quantidades = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4_MAIS": 4,
    }
    quantidade = quantidades.get(codigo)
    atingiu_limite = (
        quantidade is not None
        and (
            (sexo == "FEMININO" and quantidade >= 3)
            or (sexo == "MASCULINO" and quantidade >= 4)
        )
    )

    if not atingiu_limite:
        return None

    pergunta = obter_pergunta("EXT-05B")
    return _novo_achado(
        pergunta,
        "LIMITE_ANUAL_SEM_DATAS",
        Triagem.Resultado.AVALIACAO,
        "O limite anual foi alcançado; as datas históricas precisam ser conferidas.",
    )


def _avaliar_seguranca_estetica(respostas, hoje):
    """Aplica 12 meses quando a segurança estética não é comprovada."""

    valor = respostas.get("EXT-24") or {}
    codigos = set(valor.get("codigos") or []) - {"NENHUM"}
    if not codigos:
        return []

    pergunta = obter_pergunta("EXT-24")
    achados = []

    if valor.get("inflamacao") in {"SIM", "NAO_SEI"}:
        achados.append(
            _novo_achado(
                pergunta,
                "COM_INFLAMACAO",
                Triagem.Resultado.AVALIACAO,
                "Inflamação ou infecção precisa estar curada e ser avaliada.",
            )
        )

    seguranca = valor.get("seguranca")
    if seguranca == "SIM":
        return achados

    for codigo in codigos:
        data_evento = _data_da_resposta(valor, codigo)
        if data_evento is None:
            achados.append(
                _novo_achado(
                    pergunta,
                    f"{codigo}_SEGURANCA_SEM_DATA",
                    Triagem.Resultado.AVALIACAO,
                    "Sem comprovação de segurança, informe a data ou confirme presencialmente.",
                )
            )
            continue

        data_final = _somar_meses(data_evento, 12)
        if data_final > hoje:
            achados.append(
                _novo_achado(
                    pergunta,
                    f"{codigo}_SEM_SEGURANCA",
                    Triagem.Resultado.TEMPORARIA,
                    "Sem comprovação de antissepsia ou material, aguarde 12 meses.",
                    data_liberacao=data_final,
                )
            )

    return achados


def _respostas_para_avaliar(modalidade, respostas, respostas_base):
    """Combina somente dados estáveis da extensa com a checagem rápida."""

    if modalidade != Triagem.Modalidade.SIMPLIFICADA:
        return dict(respostas)

    combinadas = {
        id_pergunta: valor
        for id_pergunta, valor in (respostas_base or {}).items()
        if id_pergunta not in PERGUNTAS_NAO_REUTILIZAVEIS
    }
    combinadas.update(respostas)
    return combinadas


def avaliar_triagem(
    modalidade,
    respostas,
    *,
    hoje=None,
    respostas_base=None,
):
    """Avalia todas as respostas e devolve resultado, mensagem e achados."""

    if modalidade not in {
        Triagem.Modalidade.EXTENSA,
        Triagem.Modalidade.SIMPLIFICADA,
    }:
        raise ValueError("Modalidade de triagem inválida.")

    hoje = hoje or date.today()
    respostas_atuais = _respostas_para_avaliar(
        modalidade,
        respostas,
        respostas_base,
    )
    achados = []

    for id_pergunta, valor in respostas_atuais.items():
        try:
            pergunta = obter_pergunta(id_pergunta)
        except KeyError:
            # O serviço rejeita IDs inválidos; o motor permanece tolerante a legado.
            continue

        for codigo in valor.get("codigos") or []:
            # EXT-24 usa a regra curta somente quando a segurança foi confirmada.
            if (
                id_pergunta == "EXT-24"
                and valor.get("seguranca") != "SIM"
            ):
                continue

            achado = _avaliar_regra_declarada(
                pergunta,
                codigo,
                valor,
                hoje,
            )
            if achado:
                achados.append(achado)

    # Regras que dependem de respostas de mais de uma pergunta ficam explícitas.
    achado_intervalo = _avaliar_intervalo_ultima_doacao(
        respostas_atuais,
        hoje,
    )
    if achado_intervalo:
        achados.append(achado_intervalo)

    achado_limite = _avaliar_limite_doacoes(respostas_atuais)
    if achado_limite:
        achados.append(achado_limite)

    achados.extend(
        _avaliar_seguranca_estetica(respostas_atuais, hoje)
    )

    resultado = escolher_resultado(achados)
    datas = [
        date.fromisoformat(achado["data_liberacao"])
        for achado in achados
        if achado.get("data_liberacao")
    ]

    return {
        "resultado": resultado,
        "mensagem": MENSAGENS_RESULTADO[resultado],
        "data_liberacao": max(datas) if datas else None,
        "achados": achados,
        "regra_version": TRIAGEM_RULE_VERSION,
    }
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 19 a 23

```python
"""Motor puro que transforma respostas em orientação de triagem.

O módulo não acessa o banco. Isso torna os cálculos repetíveis e permite manter
o histórico antigo ligado à versão de regra que produziu cada resultado.
"""
```

**Explicação deste trecho:**

**Linha 19 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### Import — linhas 25 a 25

```python
import calendar
```

**Explicação deste trecho:**

**Linha 25 — Import** (nível 0 do bloco).

Importa módulos: `calendar`.

### Import — linhas 26 a 26

```python
import math
```

**Explicação deste trecho:**

**Linha 26 — Import** (nível 0 do bloco).

Importa módulos: `math`.

### ImportFrom — linhas 27 a 27

```python
from datetime import date, datetime, timedelta
```

**Explicação deste trecho:**

**Linha 27 — ImportFrom** (nível 0 do bloco).

Importa de `datetime` os nomes `date`, `datetime`, `timedelta`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 29 a 29

```python
from .models import Triagem
```

**Explicação deste trecho:**

**Linha 29 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `Triagem`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 30 a 33

```python
from .triagem_catalogo import (
    TRIAGEM_RULE_VERSION,
    obter_pergunta,
)
```

**Explicação deste trecho:**

**Linha 30 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_catalogo` os nomes `TRIAGEM_RULE_VERSION`, `obter_pergunta`. Pontos iniciais indicam importação relativa ao pacote.

### Assign — linhas 37 a 42

```python
PRIORIDADE_RESULTADOS = (
    Triagem.Resultado.DEFINITIVA,
    Triagem.Resultado.AVALIACAO,
    Triagem.Resultado.TEMPORARIA,
    Triagem.Resultado.DOCUMENTACAO,
)
```

**Explicação deste trecho:**

**Linha 37 — Assign** (nível 0 do bloco).

Associa `PRIORIDADE_RESULTADOS` a uma coleção Tuple com 4 itens, na expressão `(Triagem.Resultado.DEFINITIVA, Triagem.Resultado.AVALIACAO, Triagem.Resultado.TEMPORARIA, Triagem.Resultado.DOCUMENTACAO)`.

### Assign — linhas 46 a 62

```python
PERGUNTAS_NAO_REUTILIZAVEIS = {
    "EXT-08",
    "EXT-09",
    "EXT-10",
    "EXT-11",
    "EXT-11A",
    "EXT-12",
    "EXT-13",
    "EXT-14",
    "EXT-15",
    "EXT-16",
    "EXT-17",
    "EXT-18",
    "EXT-19",
    "EXT-33",
    "EXT-44",
}
```

**Explicação deste trecho:**

**Linha 46 — Assign** (nível 0 do bloco).

Associa `PERGUNTAS_NAO_REUTILIZAVEIS` a uma coleção Set com 15 itens, na expressão `{'EXT-08', 'EXT-09', 'EXT-10', 'EXT-11', 'EXT-11A', 'EXT-12', 'EXT-13', 'EXT-14', 'EXT-15', 'EXT-16', 'EXT-17', 'EXT-18', 'EXT-19', 'EXT-33', 'EXT-44'}`.

### Assign — linhas 65 a 90

```python
MENSAGENS_RESULTADO = {
    Triagem.Resultado.SEM_IMPEDIMENTO: (
        "Com base no que você informou, não identificamos um impedimento "
        "nesta orientação. Isso não significa liberação para doar: a decisão "
        "final será tomada pela equipe do hemocentro."
    ),
    Triagem.Resultado.TEMPORARIA: (
        "Encontramos uma condição com prazo de espera. A data apresentada é "
        "orientativa e só vale se você estiver recuperado(a) e não houver "
        "outro impedimento. A decisão final é do hemocentro."
    ),
    Triagem.Resultado.DEFINITIVA: (
        "Uma condição informada é classificada como impedimento definitivo "
        "pela regra consultada. Confirme a orientação com um serviço oficial, "
        "pois normas e diagnósticos podem precisar de atualização."
    ),
    Triagem.Resultado.AVALIACAO: (
        "Sua resposta depende de avaliação profissional, relatório, exame ou "
        "detalhe que o sistema não consegue confirmar com segurança. A decisão "
        "final será feita no hemocentro."
    ),
    Triagem.Resultado.DOCUMENTACAO: (
        "Existe uma exigência de documentação ou conferência presencial. Isso "
        "não substitui a avaliação clínica da equipe do hemocentro."
    ),
}
```

**Explicação deste trecho:**

**Linha 65 — Assign** (nível 0 do bloco).

Associa `MENSAGENS_RESULTADO` a um dicionário de 5 entradas; as chaves dão nome aos valores associados.

- Chave `Triagem.Resultado.SEM_IMPEDIMENTO`: recebe o valor literal `'Com base no que você informou, não identificamos um impedimento nesta orientação. Isso não significa liberação para doar: a decisão final será tomada pela equipe do hemocentro.'`.
- Chave `Triagem.Resultado.TEMPORARIA`: recebe o valor literal `'Encontramos uma condição com prazo de espera. A data apresentada é orientativa e só vale se você estiver recuperado(a) e não houver outro impedimento. A decisão final é do hemocentro.'`.
- Chave `Triagem.Resultado.DEFINITIVA`: recebe o valor literal `'Uma condição informada é classificada como impedimento definitivo pela regra consultada. Confirme a orientação com um serviço oficial, pois normas e diagnósticos podem precisar de atualização.'`.
- Chave `Triagem.Resultado.AVALIACAO`: recebe o valor literal `'Sua resposta depende de avaliação profissional, relatório, exame ou detalhe que o sistema não consegue confirmar com segurança. A decisão final será feita no hemocentro.'`.
- Chave `Triagem.Resultado.DOCUMENTACAO`: recebe o valor literal `'Existe uma exigência de documentação ou conferência presencial. Isso não substitui a avaliação clínica da equipe do hemocentro.'`.

### escolher_resultado — linhas 93 a 102

```python
def escolher_resultado(achados):
    """Escolhe o estado principal sem descartar os demais achados."""

    encontrados = {achado["resultado"] for achado in achados}

    for resultado in PRIORIDADE_RESULTADOS:
        if resultado in encontrados:
            return resultado

    return Triagem.Resultado.SEM_IMPEDIMENTO
```

**Explicação deste trecho:**

**Linha 93 — FunctionDef** (nível 0 do bloco).

Define `escolher_resultado(achados)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 93:

**Linha 94 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 96 — Assign** (nível 1 do bloco).

Associa `encontrados` a uma coleção/gerador construído por compreensão em `{achado['resultado'] for achado in achados}`: percorre as fontes e aplica os filtros declarados.

**Linha 98 — For** (nível 1 do bloco).

Percorre `PRIORIDADE_RESULTADOS`; cada item é atribuído a `resultado` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 98:

**Linha 99 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `resultado` contido em `encontrados`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 99:

**Linha 100 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `resultado` ao chamador.

**Linha 102 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o atributo `SEM_IMPEDIMENTO` de `Triagem.Resultado` ao chamador.

### _converter_data — linhas 105 a 118

```python
def _converter_data(valor):
    """Aceita data, datetime ou ISO; valor inválido volta como ausente."""

    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    if not valor:
        return None

    try:
        return date.fromisoformat(str(valor))
    except ValueError:
        return None
```

**Explicação deste trecho:**

**Linha 105 — FunctionDef** (nível 0 do bloco).

Define `_converter_data(valor)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 105:

**Linha 106 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 108 — If** (nível 1 do bloco).

Escolhe um caminho verificando a chamada `isinstance`; argumentos posicionais: `valor`, `datetime`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 108:

**Linha 109 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `valor.date` ao chamador.

**Linha 110 — If** (nível 1 do bloco).

Escolhe um caminho verificando a chamada `isinstance`; argumentos posicionais: `valor`, `date`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 110:

**Linha 111 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `valor` ao chamador.

**Linha 112 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `valor`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 112:

**Linha 113 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

**Linha 115 — Try** (nível 1 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 115:

**Linha 116 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `date.fromisoformat`; argumentos posicionais: `str(valor)` ao chamador.

Erro tratado: `ValueError`.

**Linha 118 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

### _somar_meses — linhas 121 a 128

```python
def _somar_meses(data_base, quantidade):
    """Soma meses pelo calendário e ajusta dias como 31 de janeiro."""

    indice_mes = data_base.month - 1 + quantidade
    ano = data_base.year + indice_mes // 12
    mes = indice_mes % 12 + 1
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    return date(ano, mes, min(data_base.day, ultimo_dia))
```

**Explicação deste trecho:**

**Linha 121 — FunctionDef** (nível 0 do bloco).

Define `_somar_meses(data_base, quantidade)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 121:

**Linha 122 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 124 — Assign** (nível 1 do bloco).

Associa `indice_mes` a a expressão `data_base.month - 1 + quantidade`; seus operadores determinam o cálculo.

**Linha 125 — Assign** (nível 1 do bloco).

Associa `ano` a a expressão `data_base.year + indice_mes // 12`; seus operadores determinam o cálculo.

**Linha 126 — Assign** (nível 1 do bloco).

Associa `mes` a a expressão `indice_mes % 12 + 1`; seus operadores determinam o cálculo.

**Linha 127 — Assign** (nível 1 do bloco).

Associa `ultimo_dia` a o item ou recorte `1` de `calendar.monthrange(ano, mes)`.

**Linha 128 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `date`; argumentos posicionais: `ano`, `mes`, `min(data_base.day, ultimo_dia)` ao chamador.

### calcular_data_liberacao — linhas 131 a 149

```python
def calcular_data_liberacao(data_base, prazo):
    """Calcula a data final para horas, dias, semanas, meses ou anos."""

    unidade = prazo["unidade"]
    quantidade = prazo["valor"]

    if unidade == "horas":
        # Como o model guarda uma data, qualquer fração de dia é conservadora.
        return data_base + timedelta(days=math.ceil(quantidade / 24))
    if unidade == "dias":
        return data_base + timedelta(days=quantidade)
    if unidade == "semanas":
        return data_base + timedelta(weeks=quantidade)
    if unidade == "meses":
        return _somar_meses(data_base, quantidade)
    if unidade == "anos":
        return _somar_meses(data_base, quantidade * 12)

    raise ValueError(f"Unidade de prazo inválida: {unidade}")
```

**Explicação deste trecho:**

**Linha 131 — FunctionDef** (nível 0 do bloco).

Define `calcular_data_liberacao(data_base, prazo)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 131:

**Linha 132 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 134 — Assign** (nível 1 do bloco).

Associa `unidade` a o item ou recorte `'unidade'` de `prazo`.

**Linha 135 — Assign** (nível 1 do bloco).

Associa `quantidade` a o item ou recorte `'valor'` de `prazo`.

**Linha 137 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `unidade` igual a `'horas'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 137:

**Linha 139 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a expressão `data_base + timedelta(days=math.ceil(quantidade / 24))`; seus operadores determinam o cálculo ao chamador.

**Linha 140 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `unidade` igual a `'dias'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 140:

**Linha 141 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a expressão `data_base + timedelta(days=quantidade)`; seus operadores determinam o cálculo ao chamador.

**Linha 142 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `unidade` igual a `'semanas'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 142:

**Linha 143 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a expressão `data_base + timedelta(weeks=quantidade)`; seus operadores determinam o cálculo ao chamador.

**Linha 144 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `unidade` igual a `'meses'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 144:

**Linha 145 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `_somar_meses`; argumentos posicionais: `data_base`, `quantidade` ao chamador.

**Linha 146 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `unidade` igual a `'anos'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 146:

**Linha 147 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `_somar_meses`; argumentos posicionais: `data_base`, `quantidade * 12` ao chamador.

**Linha 149 — Raise** (nível 1 do bloco).

Interrompe o caminho levantando a chamada `ValueError`; argumentos posicionais: `f'Unidade de prazo inválida: {unidade}'`.

### _data_da_resposta — linhas 152 a 158

```python
def _data_da_resposta(valor, codigo):
    """Obtém a data específica da alternativa ou a data legada da resposta."""

    datas = valor.get("datas") or {}
    return _converter_data(
        datas.get(codigo) or valor.get("data_evento")
    )
```

**Explicação deste trecho:**

**Linha 152 — FunctionDef** (nível 0 do bloco).

Define `_data_da_resposta(valor, codigo)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 152:

**Linha 153 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 155 — Assign** (nível 1 do bloco).

Associa `datas` a pelo menos uma das condições: `valor.get('datas')` ; `{}` (com avaliação interrompida assim que o resultado é determinado).

**Linha 156 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `_converter_data`; argumentos posicionais: `datas.get(codigo) or valor.get('data_evento')` ao chamador.

### _novo_achado — linhas 161 a 186

```python
def _novo_achado(
    pergunta,
    codigo,
    resultado,
    mensagem,
    *,
    data_liberacao=None,
    exige_relatorio=False,
):
    """Padroniza a estrutura persistida no campo JSON de achados."""

    achado = {
        "id_pergunta": pergunta["id"],
        "codigo_regra": f"{pergunta['id']}:{codigo}",
        "categoria": pergunta["titulo"],
        "resultado": resultado,
        "mensagem": mensagem,
        "exige_relatorio": exige_relatorio,
        "fonte": pergunta["fonte"],
        "regra_version": TRIAGEM_RULE_VERSION,
    }

    if data_liberacao:
        achado["data_liberacao"] = data_liberacao.isoformat()

    return achado
```

**Explicação deste trecho:**

**Linha 161 — FunctionDef** (nível 0 do bloco).

Define `_novo_achado(pergunta, codigo, resultado, mensagem, *, data_liberacao=None, exige_relatorio=False)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 161:

**Linha 170 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 172 — Assign** (nível 1 do bloco).

Associa `achado` a um dicionário de 8 entradas; as chaves dão nome aos valores associados.

- Chave `'id_pergunta'`: recebe o item ou recorte `'id'` de `pergunta`.
- Chave `'codigo_regra'`: recebe o texto formatado `f"{pergunta['id']}:{codigo}"`, inserindo valores nas partes entre chaves.
- Chave `'categoria'`: recebe o item ou recorte `'titulo'` de `pergunta`.
- Chave `'resultado'`: recebe o valor associado ao nome `resultado`.
- Chave `'mensagem'`: recebe o valor associado ao nome `mensagem`.
- Chave `'exige_relatorio'`: recebe o valor associado ao nome `exige_relatorio`.
- Chave `'fonte'`: recebe o item ou recorte `'fonte'` de `pergunta`.
- Chave `'regra_version'`: recebe o valor associado ao nome `TRIAGEM_RULE_VERSION`.

**Linha 183 — If** (nível 1 do bloco).

Escolhe um caminho verificando o valor associado ao nome `data_liberacao`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 183:

**Linha 184 — Assign** (nível 2 do bloco).

Associa `achado['data_liberacao']` a a chamada `data_liberacao.isoformat`.


**Linha 186 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `achado` ao chamador.

### _avaliar_regra_declarada — linhas 189 a 232

```python
def _avaliar_regra_declarada(pergunta, codigo, valor, hoje):
    """Avalia uma alternativa simples definida diretamente no catálogo."""

    item_regra = pergunta["regras"].get(codigo)
    if not item_regra:
        return None

    resultado = item_regra["resultado"]
    mensagem = item_regra["mensagem"]
    prazo = item_regra.get("prazo")
    data_final = None

    if prazo:
        if prazo.get("referencia") == "hoje":
            data_base = hoje
        else:
            data_base = _data_da_resposta(valor, codigo)

        # Prazos após cura, dose, alta ou procedimento precisam da data real.
        if data_base is None:
            return _novo_achado(
                pergunta,
                f"{codigo}_SEM_DATA",
                Triagem.Resultado.AVALIACAO,
                "Informe a data do evento ou confirme o prazo presencialmente.",
            )

        data_final = calcular_data_liberacao(data_base, prazo)

        # Um prazo já encerrado não é impedimento atual.
        if (
            resultado == Triagem.Resultado.TEMPORARIA
            and data_final <= hoje
        ):
            return None

    return _novo_achado(
        pergunta,
        codigo,
        resultado,
        mensagem,
        data_liberacao=data_final,
        exige_relatorio=item_regra.get("exige_relatorio", False),
    )
```

**Explicação deste trecho:**

**Linha 189 — FunctionDef** (nível 0 do bloco).

Define `_avaliar_regra_declarada(pergunta, codigo, valor, hoje)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 189:

**Linha 190 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 192 — Assign** (nível 1 do bloco).

Associa `item_regra` a a chamada `pergunta['regras'].get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `codigo`.


**Linha 193 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `item_regra`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 193:

**Linha 194 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

**Linha 196 — Assign** (nível 1 do bloco).

Associa `resultado` a o item ou recorte `'resultado'` de `item_regra`.

**Linha 197 — Assign** (nível 1 do bloco).

Associa `mensagem` a o item ou recorte `'mensagem'` de `item_regra`.

**Linha 198 — Assign** (nível 1 do bloco).

Associa `prazo` a a chamada `item_regra.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'prazo'`.


**Linha 199 — Assign** (nível 1 do bloco).

Associa `data_final` a o valor literal `None`.

**Linha 201 — If** (nível 1 do bloco).

Escolhe um caminho verificando o valor associado ao nome `prazo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 201:

**Linha 202 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `prazo.get('referencia')` igual a `'hoje'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 202:

**Linha 203 — Assign** (nível 3 do bloco).

Associa `data_base` a o valor associado ao nome `hoje`.

Bloco `orelse` da linha 202:

**Linha 205 — Assign** (nível 3 do bloco).

Associa `data_base` a a chamada `_data_da_resposta`; argumentos posicionais: `valor`, `codigo`.


**Linha 208 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `data_base` o mesmo objeto que `None`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 208:

**Linha 209 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve a chamada `_novo_achado`; argumentos posicionais: `pergunta`, `f'{codigo}_SEM_DATA'`, `Triagem.Resultado.AVALIACAO`, `'Informe a data do evento ou confirme o prazo presencialmente.'` ao chamador.

**Linha 216 — Assign** (nível 2 do bloco).

Associa `data_final` a a chamada `calcular_data_liberacao`; argumentos posicionais: `data_base`, `prazo`.


**Linha 219 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `resultado == Triagem.Resultado.TEMPORARIA` ; `data_final <= hoje` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 219:

**Linha 223 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

**Linha 225 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `_novo_achado`; argumentos posicionais: `pergunta`, `codigo`, `resultado`, `mensagem`; argumentos nomeados: `data_liberacao=data_final`, `exige_relatorio=item_regra.get('exige_relatorio', False)` ao chamador.

### _primeiro_codigo — linhas 235 a 240

```python
def _primeiro_codigo(respostas, id_pergunta):
    """Retorna a primeira alternativa quando a pergunta é de escolha única."""

    valor = respostas.get(id_pergunta) or {}
    codigos = valor.get("codigos") or []
    return codigos[0] if codigos else None
```

**Explicação deste trecho:**

**Linha 235 — FunctionDef** (nível 0 do bloco).

Define `_primeiro_codigo(respostas, id_pergunta)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 235:

**Linha 236 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 238 — Assign** (nível 1 do bloco).

Associa `valor` a pelo menos uma das condições: `respostas.get(id_pergunta)` ; `{}` (com avaliação interrompida assim que o resultado é determinado).

**Linha 239 — Assign** (nível 1 do bloco).

Associa `codigos` a pelo menos uma das condições: `valor.get('codigos')` ; `[]` (com avaliação interrompida assim que o resultado é determinado).

**Linha 240 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve `codigos[0]` se `codigos` for verdadeiro; caso contrário, `None` ao chamador.

### _avaliar_intervalo_ultima_doacao — linhas 243 a 285

```python
def _avaliar_intervalo_ultima_doacao(respostas, hoje):
    """Aplica 60/90 dias e a regra adicional de seis meses após os 60."""

    valor = respostas.get("EXT-05A") or {}
    if "DATA" not in (valor.get("codigos") or []):
        return None

    pergunta = obter_pergunta("EXT-05A")
    data_doacao = _data_da_resposta(valor, "DATA")
    if data_doacao is None:
        return _novo_achado(
            pergunta,
            "INTERVALO_SEM_DATA",
            Triagem.Resultado.AVALIACAO,
            "A data da última doação é necessária para calcular o intervalo.",
        )

    sexo = _primeiro_codigo(respostas, "EXT-04")
    idade = _primeiro_codigo(respostas, "EXT-02")
    datas = []

    if sexo == "FEMININO":
        datas.append(data_doacao + timedelta(days=90))
    elif sexo == "MASCULINO":
        datas.append(data_doacao + timedelta(days=60))

    if idade == "61_69":
        datas.append(_somar_meses(data_doacao, 6))

    if not datas:
        return None

    data_final = max(datas)
    if data_final <= hoje:
        return None

    return _novo_achado(
        pergunta,
        "INTERVALO_DOACAO",
        Triagem.Resultado.TEMPORARIA,
        "Ainda não terminou o intervalo orientativo desde a última doação.",
        data_liberacao=data_final,
    )
```

**Explicação deste trecho:**

**Linha 243 — FunctionDef** (nível 0 do bloco).

Define `_avaliar_intervalo_ultima_doacao(respostas, hoje)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 243:

**Linha 244 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 246 — Assign** (nível 1 do bloco).

Associa `valor` a pelo menos uma das condições: `respostas.get('EXT-05A')` ; `{}` (com avaliação interrompida assim que o resultado é determinado).

**Linha 247 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `'DATA'` não contido em `valor.get('codigos') or []`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 247:

**Linha 248 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

**Linha 250 — Assign** (nível 1 do bloco).

Associa `pergunta` a a chamada `obter_pergunta`; argumentos posicionais: `'EXT-05A'`.


**Linha 251 — Assign** (nível 1 do bloco).

Associa `data_doacao` a a chamada `_data_da_resposta`; argumentos posicionais: `valor`, `'DATA'`.


**Linha 252 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `data_doacao` o mesmo objeto que `None`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 252:

**Linha 253 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `_novo_achado`; argumentos posicionais: `pergunta`, `'INTERVALO_SEM_DATA'`, `Triagem.Resultado.AVALIACAO`, `'A data da última doação é necessária para calcular o intervalo.'` ao chamador.

**Linha 260 — Assign** (nível 1 do bloco).

Associa `sexo` a a chamada `_primeiro_codigo`; argumentos posicionais: `respostas`, `'EXT-04'`.


**Linha 261 — Assign** (nível 1 do bloco).

Associa `idade` a a chamada `_primeiro_codigo`; argumentos posicionais: `respostas`, `'EXT-02'`.


**Linha 262 — Assign** (nível 1 do bloco).

Associa `datas` a uma coleção List com 0 itens, na expressão `[]`.

**Linha 264 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `sexo` igual a `'FEMININO'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 264:

**Linha 265 — Expr** (nível 2 do bloco).

Executa a chamada `datas.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `data_doacao + timedelta(days=90)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 264:

**Linha 266 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `sexo` igual a `'MASCULINO'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 266:

**Linha 267 — Expr** (nível 3 do bloco).

Executa a chamada `datas.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `data_doacao + timedelta(days=60)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 269 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `idade` igual a `'61_69'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 269:

**Linha 270 — Expr** (nível 2 do bloco).

Executa a chamada `datas.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `_somar_meses(data_doacao, 6)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 272 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `datas`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 272:

**Linha 273 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

**Linha 275 — Assign** (nível 1 do bloco).

Associa `data_final` a a chamada `max`; argumentos posicionais: `datas`.


**Linha 276 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `data_final` menor ou igual a `hoje`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 276:

**Linha 277 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

**Linha 279 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `_novo_achado`; argumentos posicionais: `pergunta`, `'INTERVALO_DOACAO'`, `Triagem.Resultado.TEMPORARIA`, `'Ainda não terminou o intervalo orientativo desde a última doação.'`; argumentos nomeados: `data_liberacao=data_final` ao chamador.

### _avaliar_limite_doacoes — linhas 288 a 319

```python
def _avaliar_limite_doacoes(respostas):
    """Sem datas históricas, sinaliza o limite sem inventar uma liberação."""

    codigo = _primeiro_codigo(respostas, "EXT-05B")
    sexo = _primeiro_codigo(respostas, "EXT-04")

    quantidades = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4_MAIS": 4,
    }
    quantidade = quantidades.get(codigo)
    atingiu_limite = (
        quantidade is not None
        and (
            (sexo == "FEMININO" and quantidade >= 3)
            or (sexo == "MASCULINO" and quantidade >= 4)
        )
    )

    if not atingiu_limite:
        return None

    pergunta = obter_pergunta("EXT-05B")
    return _novo_achado(
        pergunta,
        "LIMITE_ANUAL_SEM_DATAS",
        Triagem.Resultado.AVALIACAO,
        "O limite anual foi alcançado; as datas históricas precisam ser conferidas.",
    )
```

**Explicação deste trecho:**

**Linha 288 — FunctionDef** (nível 0 do bloco).

Define `_avaliar_limite_doacoes(respostas)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 288:

**Linha 289 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 291 — Assign** (nível 1 do bloco).

Associa `codigo` a a chamada `_primeiro_codigo`; argumentos posicionais: `respostas`, `'EXT-05B'`.


**Linha 292 — Assign** (nível 1 do bloco).

Associa `sexo` a a chamada `_primeiro_codigo`; argumentos posicionais: `respostas`, `'EXT-04'`.


**Linha 294 — Assign** (nível 1 do bloco).

Associa `quantidades` a um dicionário de 5 entradas; as chaves dão nome aos valores associados.

- Chave `'0'`: recebe o valor literal `0`.
- Chave `'1'`: recebe o valor literal `1`.
- Chave `'2'`: recebe o valor literal `2`.
- Chave `'3'`: recebe o valor literal `3`.
- Chave `'4_MAIS'`: recebe o valor literal `4`.

**Linha 301 — Assign** (nível 1 do bloco).

Associa `quantidade` a a chamada `quantidades.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `codigo`.


**Linha 302 — Assign** (nível 1 do bloco).

Associa `atingiu_limite` a todas as condições: `quantidade is not None` ; `sexo == 'FEMININO' and quantidade >= 3 or (sexo == 'MASCULINO' and quantidade >= 4)` (com avaliação interrompida assim que o resultado é determinado).

**Linha 310 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `atingiu_limite`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 310:

**Linha 311 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

**Linha 313 — Assign** (nível 1 do bloco).

Associa `pergunta` a a chamada `obter_pergunta`; argumentos posicionais: `'EXT-05B'`.


**Linha 314 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `_novo_achado`; argumentos posicionais: `pergunta`, `'LIMITE_ANUAL_SEM_DATAS'`, `Triagem.Resultado.AVALIACAO`, `'O limite anual foi alcançado; as datas históricas precisam ser conferidas.'` ao chamador.

### _avaliar_seguranca_estetica — linhas 322 a 372

```python
def _avaliar_seguranca_estetica(respostas, hoje):
    """Aplica 12 meses quando a segurança estética não é comprovada."""

    valor = respostas.get("EXT-24") or {}
    codigos = set(valor.get("codigos") or []) - {"NENHUM"}
    if not codigos:
        return []

    pergunta = obter_pergunta("EXT-24")
    achados = []

    if valor.get("inflamacao") in {"SIM", "NAO_SEI"}:
        achados.append(
            _novo_achado(
                pergunta,
                "COM_INFLAMACAO",
                Triagem.Resultado.AVALIACAO,
                "Inflamação ou infecção precisa estar curada e ser avaliada.",
            )
        )

    seguranca = valor.get("seguranca")
    if seguranca == "SIM":
        return achados

    for codigo in codigos:
        data_evento = _data_da_resposta(valor, codigo)
        if data_evento is None:
            achados.append(
                _novo_achado(
                    pergunta,
                    f"{codigo}_SEGURANCA_SEM_DATA",
                    Triagem.Resultado.AVALIACAO,
                    "Sem comprovação de segurança, informe a data ou confirme presencialmente.",
                )
            )
            continue

        data_final = _somar_meses(data_evento, 12)
        if data_final > hoje:
            achados.append(
                _novo_achado(
                    pergunta,
                    f"{codigo}_SEM_SEGURANCA",
                    Triagem.Resultado.TEMPORARIA,
                    "Sem comprovação de antissepsia ou material, aguarde 12 meses.",
                    data_liberacao=data_final,
                )
            )

    return achados
```

**Explicação deste trecho:**

**Linha 322 — FunctionDef** (nível 0 do bloco).

Define `_avaliar_seguranca_estetica(respostas, hoje)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 322:

**Linha 323 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 325 — Assign** (nível 1 do bloco).

Associa `valor` a pelo menos uma das condições: `respostas.get('EXT-24')` ; `{}` (com avaliação interrompida assim que o resultado é determinado).

**Linha 326 — Assign** (nível 1 do bloco).

Associa `codigos` a a expressão `set(valor.get('codigos') or []) - {'NENHUM'}`; seus operadores determinam o cálculo.

**Linha 327 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `codigos`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 327:

**Linha 328 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve uma coleção List com 0 itens, na expressão `[]` ao chamador.

**Linha 330 — Assign** (nível 1 do bloco).

Associa `pergunta` a a chamada `obter_pergunta`; argumentos posicionais: `'EXT-24'`.


**Linha 331 — Assign** (nível 1 do bloco).

Associa `achados` a uma coleção List com 0 itens, na expressão `[]`.

**Linha 333 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `valor.get('inflamacao')` contido em `{'SIM', 'NAO_SEI'}`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 333:

**Linha 334 — Expr** (nível 2 do bloco).

Executa a chamada `achados.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `_novo_achado(pergunta, 'COM_INFLAMACAO', Triagem.Resultado.AVALIACAO, 'Inflamação ou infecção precisa estar curada e ser avaliada.')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 343 — Assign** (nível 1 do bloco).

Associa `seguranca` a a chamada `valor.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'seguranca'`.


**Linha 344 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `seguranca` igual a `'SIM'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 344:

**Linha 345 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `achados` ao chamador.

**Linha 347 — For** (nível 1 do bloco).

Percorre `codigos`; cada item é atribuído a `codigo` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 347:

**Linha 348 — Assign** (nível 2 do bloco).

Associa `data_evento` a a chamada `_data_da_resposta`; argumentos posicionais: `valor`, `codigo`.


**Linha 349 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `data_evento` o mesmo objeto que `None`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 349:

**Linha 350 — Expr** (nível 3 do bloco).

Executa a chamada `achados.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `_novo_achado(pergunta, f'{codigo}_SEGURANCA_SEM_DATA', Triagem.Resultado.AVALIACAO, 'Sem comprovação de segurança, informe a data ou confirme presencialmente.')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 358 — Continue** (nível 3 do bloco).

Pula o restante da iteração atual e segue para o próximo item do laço.

**Linha 360 — Assign** (nível 2 do bloco).

Associa `data_final` a a chamada `_somar_meses`; argumentos posicionais: `data_evento`, `12`.


**Linha 361 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `data_final` maior que `hoje`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 361:

**Linha 362 — Expr** (nível 3 do bloco).

Executa a chamada `achados.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `_novo_achado(pergunta, f'{codigo}_SEM_SEGURANCA', Triagem.Resultado.TEMPORARIA, 'Sem comprovação de antissepsia ou material, aguarde 12 meses.', data_liberacao=data_final)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 372 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `achados` ao chamador.

### _respostas_para_avaliar — linhas 375 a 387

```python
def _respostas_para_avaliar(modalidade, respostas, respostas_base):
    """Combina somente dados estáveis da extensa com a checagem rápida."""

    if modalidade != Triagem.Modalidade.SIMPLIFICADA:
        return dict(respostas)

    combinadas = {
        id_pergunta: valor
        for id_pergunta, valor in (respostas_base or {}).items()
        if id_pergunta not in PERGUNTAS_NAO_REUTILIZAVEIS
    }
    combinadas.update(respostas)
    return combinadas
```

**Explicação deste trecho:**

**Linha 375 — FunctionDef** (nível 0 do bloco).

Define `_respostas_para_avaliar(modalidade, respostas, respostas_base)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 375:

**Linha 376 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 378 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `modalidade` diferente de `Triagem.Modalidade.SIMPLIFICADA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 378:

**Linha 379 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `dict`; argumentos posicionais: `respostas` ao chamador.

**Linha 381 — Assign** (nível 1 do bloco).

Associa `combinadas` a uma coleção/gerador construído por compreensão em `{id_pergunta: valor for id_pergunta, valor in (respostas_base or {}).items() if id_pergunta not in PERGUNTAS_NAO_REUTILIZAVEIS}`: percorre as fontes e aplica os filtros declarados.

**Linha 386 — Expr** (nível 1 do bloco).

Executa a chamada `combinadas.update`, que no QuerySet grava diretamente os campos dos resultados, sem chamar save de cada instância; argumentos posicionais: `respostas`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 387 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `combinadas` ao chamador.

### avaliar_triagem — linhas 390 a 466

```python
def avaliar_triagem(
    modalidade,
    respostas,
    *,
    hoje=None,
    respostas_base=None,
):
    """Avalia todas as respostas e devolve resultado, mensagem e achados."""

    if modalidade not in {
        Triagem.Modalidade.EXTENSA,
        Triagem.Modalidade.SIMPLIFICADA,
    }:
        raise ValueError("Modalidade de triagem inválida.")

    hoje = hoje or date.today()
    respostas_atuais = _respostas_para_avaliar(
        modalidade,
        respostas,
        respostas_base,
    )
    achados = []

    for id_pergunta, valor in respostas_atuais.items():
        try:
            pergunta = obter_pergunta(id_pergunta)
        except KeyError:
            # O serviço rejeita IDs inválidos; o motor permanece tolerante a legado.
            continue

        for codigo in valor.get("codigos") or []:
            # EXT-24 usa a regra curta somente quando a segurança foi confirmada.
            if (
                id_pergunta == "EXT-24"
                and valor.get("seguranca") != "SIM"
            ):
                continue

            achado = _avaliar_regra_declarada(
                pergunta,
                codigo,
                valor,
                hoje,
            )
            if achado:
                achados.append(achado)

    # Regras que dependem de respostas de mais de uma pergunta ficam explícitas.
    achado_intervalo = _avaliar_intervalo_ultima_doacao(
        respostas_atuais,
        hoje,
    )
    if achado_intervalo:
        achados.append(achado_intervalo)

    achado_limite = _avaliar_limite_doacoes(respostas_atuais)
    if achado_limite:
        achados.append(achado_limite)

    achados.extend(
        _avaliar_seguranca_estetica(respostas_atuais, hoje)
    )

    resultado = escolher_resultado(achados)
    datas = [
        date.fromisoformat(achado["data_liberacao"])
        for achado in achados
        if achado.get("data_liberacao")
    ]

    return {
        "resultado": resultado,
        "mensagem": MENSAGENS_RESULTADO[resultado],
        "data_liberacao": max(datas) if datas else None,
        "achados": achados,
        "regra_version": TRIAGEM_RULE_VERSION,
    }
```

**Explicação deste trecho:**

**Linha 390 — FunctionDef** (nível 0 do bloco).

Define `avaliar_triagem(modalidade, respostas, *, hoje=None, respostas_base=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 390:

**Linha 397 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 399 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `modalidade` não contido em `{Triagem.Modalidade.EXTENSA, Triagem.Modalidade.SIMPLIFICADA}`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 399:

**Linha 403 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValueError`; argumentos posicionais: `'Modalidade de triagem inválida.'`.

**Linha 405 — Assign** (nível 1 do bloco).

Associa `hoje` a pelo menos uma das condições: `hoje` ; `date.today()` (com avaliação interrompida assim que o resultado é determinado).

**Linha 406 — Assign** (nível 1 do bloco).

Associa `respostas_atuais` a a chamada `_respostas_para_avaliar`; argumentos posicionais: `modalidade`, `respostas`, `respostas_base`.


**Linha 411 — Assign** (nível 1 do bloco).

Associa `achados` a uma coleção List com 0 itens, na expressão `[]`.

**Linha 413 — For** (nível 1 do bloco).

Percorre `respostas_atuais.items()`; cada item é atribuído a `(id_pergunta, valor)` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 413:

**Linha 414 — Try** (nível 2 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 414:

**Linha 415 — Assign** (nível 3 do bloco).

Associa `pergunta` a a chamada `obter_pergunta`; argumentos posicionais: `id_pergunta`.


Erro tratado: `KeyError`.

**Linha 418 — Continue** (nível 3 do bloco).

Pula o restante da iteração atual e segue para o próximo item do laço.

**Linha 420 — For** (nível 2 do bloco).

Percorre `valor.get('codigos') or []`; cada item é atribuído a `codigo` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 420:

**Linha 422 — If** (nível 3 do bloco).

Escolhe um caminho verificando todas as condições: `id_pergunta == 'EXT-24'` ; `valor.get('seguranca') != 'SIM'` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 422:

**Linha 426 — Continue** (nível 4 do bloco).

Pula o restante da iteração atual e segue para o próximo item do laço.

**Linha 428 — Assign** (nível 3 do bloco).

Associa `achado` a a chamada `_avaliar_regra_declarada`; argumentos posicionais: `pergunta`, `codigo`, `valor`, `hoje`.


**Linha 434 — If** (nível 3 do bloco).

Escolhe um caminho verificando o valor associado ao nome `achado`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 434:

**Linha 435 — Expr** (nível 4 do bloco).

Executa a chamada `achados.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `achado`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 438 — Assign** (nível 1 do bloco).

Associa `achado_intervalo` a a chamada `_avaliar_intervalo_ultima_doacao`; argumentos posicionais: `respostas_atuais`, `hoje`.


**Linha 442 — If** (nível 1 do bloco).

Escolhe um caminho verificando o valor associado ao nome `achado_intervalo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 442:

**Linha 443 — Expr** (nível 2 do bloco).

Executa a chamada `achados.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `achado_intervalo`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 445 — Assign** (nível 1 do bloco).

Associa `achado_limite` a a chamada `_avaliar_limite_doacoes`; argumentos posicionais: `respostas_atuais`.


**Linha 446 — If** (nível 1 do bloco).

Escolhe um caminho verificando o valor associado ao nome `achado_limite`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 446:

**Linha 447 — Expr** (nível 2 do bloco).

Executa a chamada `achados.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `achado_limite`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 449 — Expr** (nível 1 do bloco).

Executa a chamada `achados.extend`; argumentos posicionais: `_avaliar_seguranca_estetica(respostas_atuais, hoje)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 453 — Assign** (nível 1 do bloco).

Associa `resultado` a a chamada `escolher_resultado`; argumentos posicionais: `achados`.


**Linha 454 — Assign** (nível 1 do bloco).

Associa `datas` a uma coleção/gerador construído por compreensão em `[date.fromisoformat(achado['data_liberacao']) for achado in achados if achado.get('data_liberacao')]`: percorre as fontes e aplica os filtros declarados.

**Linha 460 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve um dicionário de 5 entradas; as chaves dão nome aos valores associados ao chamador.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 1: `#Este arquivo é o motor que calcula o resultado da triagem.`
- Linha 3: `# - Recebe as respostas e não acessa diretamente o banco de dados.`
- Linha 4: `# - Usa as regras declaradas no catálogo de perguntas.`
- Linha 5: `# - Cria achados para cada condição identificada.`
- Linha 6: `# - Calcula prazos em horas, dias, semanas, meses ou anos.`
- Linha 7: `# - Solicita avaliação quando falta uma data necessária.`
- Linha 8: `# - Aplica regras específicas de intervalo entre doações.`
- Linha 9: `# - Verifica limites de doações nos últimos 12 meses.`
- Linha 10: `# - Analisa procedimentos estéticos e prazos de segurança.`
- Linha 11: `# - Na triagem simplificada, reutiliza somente respostas estáveis da extensa.`
- Linha 12: `# - Mantém todos os achados encontrados.`
- Linha 13: `# - Escolhe sempre o resultado mais restritivo.`
- Linha 14: `# - Calcula a data de liberação mais distante, quando existir.`
- Linha 15: `# - Retorna resultado, mensagem, achados, data e versão das regras.`
- Linha 17: `# Este motor apenas calcula a orientação. O resultado não substitui a avaliação clínica final do Hemocentro.`
- Linha 36: `# Um resultado mais restritivo sempre prevalece, mas nenhum achado é apagado.`
- Linha 45: `# Estes dados mudam rapidamente e nunca são herdados pela versão simplificada.`
- Linha 138: `# Como o model guarda uma data, qualquer fração de dia é conservadora.`
- Linha 207: `# Prazos após cura, dose, alta ou procedimento precisam da data real.`
- Linha 218: `# Um prazo já encerrado não é impedimento atual.`
- Linha 417: `# O serviço rejeita IDs inválidos; o motor permanece tolerante a legado.`
- Linha 421: `# EXT-24 usa a regra curta somente quando a segurança foi confirmada.`
- Linha 437: `# Regras que dependem de respostas de mais de uma pergunta ficam explícitas.`

