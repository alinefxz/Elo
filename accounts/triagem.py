"""
Regras iniciais da triagem extensa.

Estas regras são orientativas e não substituem a avaliação
clínica feita pelo hemocentro.
"""

from datetime import date, timedelta

from .models import Triagem


# Versão identificável das regras utilizadas.
TRIAGEM_RULE_VERSION = "HEMOMINAS_2026_08"


# Associação entre os campos do formulário e as perguntas do documento.
QUESTION_FIELDS = [
    (
        "entende_orientacao",
        "EXT-01",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-01",
    ),
    (
        "idade",
        "EXT-02",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-02",
    ),
    (
        "peso",
        "EXT-03",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-03",
    ),
    (
        "sexo_biologico",
        "EXT-04",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-04",
    ),
    (
        "ja_doou",
        "EXT-05",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05",
    ),
    (
        "data_ultima_doacao",
        "EXT-05A",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05A",
    ),
    (
        "doacoes_12_meses",
        "EXT-05B",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05B",
    ),
]


def adicionar_achado(
    achados,
    codigo,
    resultado,
    mensagem,
    data_liberacao=None,
):
    """
    Adiciona um impedimento ou alerta sem apagar achados anteriores.
    """

    achado = {
        "codigo": codigo,
        "resultado": resultado,
        "mensagem": mensagem,
    }

    if data_liberacao:
        achado["data_liberacao"] = data_liberacao.isoformat()

    achados.append(achado)


def escolher_resultado(achados):
    """
    Escolhe o resultado mais restritivo entre todos os achados.

    A triagem não para no primeiro problema:
    todos os achados continuam registrados.
    """

    ordem = [
        Triagem.Resultado.DEFINITIVA,
        Triagem.Resultado.AVALIACAO,
        Triagem.Resultado.TEMPORARIA,
        Triagem.Resultado.DOCUMENTACAO,
    ]

    resultados = {
        achado["resultado"]
        for achado in achados
    }

    for resultado in ordem:
        if resultado in resultados:
            return resultado

    return Triagem.Resultado.SEM_IMPEDIMENTO


def mensagem_do_resultado(resultado):
    """
    Retorna a mensagem segura apresentada ao usuário.
    """

    mensagens = {
        Triagem.Resultado.SEM_IMPEDIMENTO: (
            "Com base no que você informou, não identificamos "
            "um impedimento nesta orientação. Isso não significa "
            "liberação para doar: a decisão final será tomada "
            "pela equipe do hemocentro."
        ),
        Triagem.Resultado.TEMPORARIA: (
            "Encontramos uma condição com prazo de espera. "
            "A data é apenas orientativa e só vale se não existir "
            "outro impedimento."
        ),
        Triagem.Resultado.DEFINITIVA: (
            "A condição informada foi classificada como impedimento "
            "pela regra consultada. Confirme a orientação com o "
            "hemocentro ou serviço oficial."
        ),
        Triagem.Resultado.AVALIACAO: (
            "Sua resposta depende de avaliação profissional, "
            "relatório, exame ou informação que o sistema não "
            "consegue confirmar com segurança."
        ),
        Triagem.Resultado.DOCUMENTACAO: (
            "Para continuar, será necessária documentação especial "
            "ou conferência presencial pelo hemocentro."
        ),
    }

    return mensagens[resultado]


def calcular_resultado(respostas, hoje=None):
    """
    Calcula o resultado inicial da triagem extensa.

    O parâmetro hoje existe para facilitar testes e garantir
    que o cálculo possa ser repetido com uma data conhecida.
    """

    hoje = hoje or date.today()
    achados = []

    # EXT-01: entendimento da finalidade da triagem.
    if respostas.get("entende_orientacao") != "SIM":
        adicionar_achado(
            achados,
            "EXT-01",
            Triagem.Resultado.AVALIACAO,
            (
                "A triagem só pode continuar com o entendimento "
                "de que ela é orientativa."
            ),
        )

    # EXT-02: idade.
    idade = respostas.get("idade")

    if idade == "MENOS_16":
        adicionar_achado(
            achados,
            "EXT-02",
            Triagem.Resultado.AVALIACAO,
            (
                "A idade informada exige avaliação específica "
                "do hemocentro."
            ),
        )

    elif idade == "16_17":
        adicionar_achado(
            achados,
            "EXT-06",
            Triagem.Resultado.DOCUMENTACAO,
            (
                "Pessoas de 16 ou 17 anos precisam apresentar "
                "autorização e documentação específica."
            ),
        )

    elif idade == "70_MAIS":
        adicionar_achado(
            achados,
            "EXT-02",
            Triagem.Resultado.AVALIACAO,
            (
                "A idade informada não deve ser liberada pela "
                "pré-triagem comum e exige avaliação do hemocentro."
            ),
        )

    # EXT-03: peso.
    peso = respostas.get("peso")

    if peso == "MENOS_50":
        adicionar_achado(
            achados,
            "EXT-03",
            Triagem.Resultado.TEMPORARIA,
            (
                "O peso informado está abaixo do limite utilizado "
                "nesta orientação."
            ),
        )

    elif peso in ("130_MAIS", "NAO_SEI"):
        adicionar_achado(
            achados,
            "EXT-03",
            Triagem.Resultado.AVALIACAO,
            (
                "O peso informado precisa ser confirmado e avaliado "
                "pela unidade de coleta."
            ),
        )

    # EXT-05: histórico de doação.
    ja_doou = respostas.get("ja_doou")

    if ja_doou == "NAO_LEMBRO":
        adicionar_achado(
            achados,
            "EXT-05",
            Triagem.Resultado.AVALIACAO,
            (
                "Não foi possível confirmar o histórico da última "
                "doação."
            ),
        )

    if ja_doou == "SIM":
        sexo = respostas.get("sexo_biologico")
        ultima_doacao = respostas.get("data_ultima_doacao")
        doacoes_12_meses = respostas.get("doacoes_12_meses")

        # Sexo desconhecido não deve gerar uma falsa liberação.
        if sexo not in ("FEMININO", "MASCULINO"):
            adicionar_achado(
                achados,
                "EXT-04",
                Triagem.Resultado.AVALIACAO,
                (
                    "Não foi possível aplicar com segurança a regra "
                    "do intervalo entre doações."
                ),
            )

        # Calcula o intervalo mínimo desde a última doação.
        if ultima_doacao and sexo in ("FEMININO", "MASCULINO"):
            intervalo_dias = (
                90
                if sexo == "FEMININO"
                else 60
            )

            data_intervalo = (
                ultima_doacao
                + timedelta(days=intervalo_dias)
            )

            if data_intervalo > hoje:
                adicionar_achado(
                    achados,
                    "EXT-05A",
                    Triagem.Resultado.TEMPORARIA,
                    (
                        "Ainda não terminou o intervalo orientativo "
                        "desde a última doação."
                    ),
                    data_liberacao=data_intervalo,
                )

        # Verifica o limite orientativo de doações em 12 meses.
        if doacoes_12_meses == "NAO_LEMBRO":
            adicionar_achado(
                achados,
                "EXT-05B",
                Triagem.Resultado.AVALIACAO,
                (
                    "Não foi possível confirmar a quantidade de "
                    "doações nos últimos 12 meses."
                ),
            )

        elif ultima_doacao:
            limite = (
                3
                if sexo == "FEMININO"
                else 4
            )

            quantidade_excedida = (
                doacoes_12_meses == "4_MAIS"
                or (
                    doacoes_12_meses.isdigit()
                    and int(doacoes_12_meses) >= limite
                )
            )

            if quantidade_excedida:
                # Data orientativa e conservadora para completar
                # uma janela aproximada de 12 meses.
                data_janela = (
                    ultima_doacao
                    + timedelta(days=365)
                )

                if data_janela > hoje:
                    adicionar_achado(
                        achados,
                        "EXT-05B",
                        Triagem.Resultado.TEMPORARIA,
                        (
                            "A quantidade informada atingiu o limite "
                            "orientativo de doações em 12 meses."
                        ),
                        data_liberacao=data_janela,
                    )

    # Escolhe o resultado final depois de analisar todos os achados.
    resultado = escolher_resultado(achados)

    # Usa a data mais distante quando existem vários prazos.
    datas_liberacao = []

    for achado in achados:
        data_texto = achado.get("data_liberacao")

        if data_texto:
            datas_liberacao.append(
                date.fromisoformat(data_texto)
            )

    data_liberacao = (
        max(datas_liberacao)
        if datas_liberacao
        else None
    )

    return {
        "resultado": resultado,
        "mensagem": mensagem_do_resultado(resultado),
        "data_liberacao": data_liberacao,
        "achados": achados,
    }


def preparar_respostas(form):
    """
    Converte as respostas do formulário para os registros do banco.
    """

    respostas = []

    for campo, id_pergunta, source_ref in QUESTION_FIELDS:
        valor = form.cleaned_data.get(campo)

        # Não cria registro para campos opcionais vazios.
        if valor in (None, ""):
            continue

        if isinstance(valor, date):
            codigo_resposta = valor.isoformat()
            resposta_label = valor.strftime("%d/%m/%Y")
            data_evento = valor
        else:
            codigo_resposta = str(valor)
            opcoes = dict(form.fields[campo].choices)
            resposta_label = opcoes.get(
                valor,
                str(valor),
            )
            data_evento = None

        respostas.append(
            {
                "id_pergunta": id_pergunta,
                "codigo_resposta": codigo_resposta,
                "resposta_label": resposta_label,
                "data_evento": data_evento,
                "metadata": {},
                "rule_version": TRIAGEM_RULE_VERSION,
                "source_ref": source_ref,
            }
        )

    return respostas