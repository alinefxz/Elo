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
