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
