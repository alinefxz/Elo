"""Catálogo de localidades aceitas em novas submissões públicas."""

from django.core.exceptions import ValidationError


CIDADES_POR_ESTADO: dict[str, tuple[str, ...]] = {
    "SP": ("São Paulo", "Campinas", "Santos"),
}

ESTADOS_CHOICES = [(estado, estado) for estado in CIDADES_POR_ESTADO]


def cidades_choices(estado: str | None) -> list[tuple[str, str]]:
    """Devolve as cidades disponíveis para uma UF, incluindo opção vazia."""

    cidades = CIDADES_POR_ESTADO.get(estado or "", ())
    return [("", "Selecione uma cidade")] + [
        (cidade, cidade) for cidade in cidades
    ]


def cidade_pertence_ao_estado(estado: str | None, cidade: str | None) -> bool:
    """Informa se cidade e UF formam um par do catálogo atual."""

    if not estado and not cidade:
        return True

    return bool(estado and cidade in CIDADES_POR_ESTADO.get(estado, ()))


def validar_localidade(estado: str | None, cidade: str | None) -> None:
    """Rejeita pares de UF/cidade que não pertencem ao catálogo."""

    if not cidade_pertence_ao_estado(estado, cidade):
        raise ValidationError("Selecione uma cidade compatível com a UF.")
