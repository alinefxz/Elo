TIPOS_SANGUINEOS = ("O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+")

COMPATIBILIDADE_RECEBIMENTO = {
    "O-": ("O-",),
    "O+": ("O-", "O+"),
    "A-": ("O-", "A-"),
    "A+": ("O-", "O+", "A-", "A+"),
    "B-": ("O-", "B-"),
    "B+": ("O-", "O+", "B-", "B+"),
    "AB-": ("O-", "A-", "B-", "AB-"),
    "AB+": TIPOS_SANGUINEOS,
}

POPULACAO_APROXIMADA = {
    "O-": "7%",
    "O+": "38%",
    "A-": "6%",
    "A+": "34%",
    "B-": "2%",
    "B+": "9%",
    "AB-": "1%",
    "AB+": "3%",
}


def normalizar_tipo_sanguineo(tipo_sanguineo):
    tipo = (tipo_sanguineo or "").strip().upper()
    if tipo not in TIPOS_SANGUINEOS:
        raise ValueError("Tipo sanguineo invalido.")
    return tipo


def doadores_compativeis_para(tipo_solicitado):
    tipo = normalizar_tipo_sanguineo(tipo_solicitado)
    return COMPATIBILIDADE_RECEBIMENTO[tipo]


def tipos_que_recebem_de(tipo_doador):
    tipo = normalizar_tipo_sanguineo(tipo_doador)
    return tuple(
        receptor
        for receptor, doadores in COMPATIBILIDADE_RECEBIMENTO.items()
        if tipo in doadores
    )


def tabela_de_compatibilidade():
    return [
        {
            "tipo": tipo,
            "doar_para": tipos_que_recebem_de(tipo),
            "receber_de": doadores_compativeis_para(tipo),
            "populacao": POPULACAO_APROXIMADA[tipo],
        }
        for tipo in TIPOS_SANGUINEOS
    ]