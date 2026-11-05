"""Localidades brasileiras com catálogo oficial local e sugestões públicas."""
import json
from pathlib import Path

from django import forms
from django.core.exceptions import ValidationError

ESTADOS = (
    ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
    ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
    ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'),
    ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'),
    ('SE', 'Sergipe'), ('TO', 'Tocantins'),
)


def localidades_publicas():
    from .models import Usuario
    return list(Usuario.objects.filter(
        perfil=Usuario.Perfil.HEMOCENTRO,
        status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO,
    ).exclude(cidade='').order_by('cidade', 'estado').values_list('cidade', 'estado').distinct())


class CidadeSugeridaInput(forms.TextInput):
    template_name = 'accounts/widgets/cidade_sugerida.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['cidades'] = localidades_publicas()
        return context


def configurar_cidades_filtro(form, origem):
    from .models import PedidoSangue, Usuario
    if origem == 'pedidos':
        cidades = PedidoSangue.objects.filter(
            status=PedidoSangue.Status.PUBLICADA,
            hemocentro_destino__perfil=Usuario.Perfil.HEMOCENTRO,
            hemocentro_destino__status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO,
        ).exclude(cidade='').order_by('cidade').values_list('cidade', flat=True).distinct()
    else:
        cidades = [cidade for cidade, _ in localidades_publicas()]
    opcoes = sorted(set(cidades), key=str.casefold)
    # Preserva links de busca existentes, inclusive buscas parciais digitadas antes.
    selecionada = form.data.get(form.add_prefix('cidade')) if form.is_bound else None
    if selecionada and selecionada not in opcoes:
        opcoes.append(selecionada)
    form.fields['cidade'].widget = forms.Select(choices=[('', 'Todas as cidades')] + [(c, c) for c in opcoes])


def _carregar_municipios():
    """Lê o snapshot versionado, sem rede nem consultas a dados de usuários."""
    caminho = Path(__file__).resolve().parent / "data" / "municipios_ibge.json"
    try:
        documento = json.loads(caminho.read_text(encoding="utf-8"))
        catalogo = documento["municipios_por_estado"]
        if not isinstance(catalogo, dict) or set(catalogo) != {uf for uf, _ in ESTADOS}:
            raise ValueError("o catálogo deve conter todas as 27 UFs")
        if sum(len(nomes) for nomes in catalogo.values()) < 5500:
            raise ValueError("o catálogo municipal está incompleto")
        for nomes in catalogo.values():
            if not isinstance(nomes, list) or not all(isinstance(nome, str) and nome for nome in nomes):
                raise ValueError("o catálogo contém nomes municipais inválidos")
            if len(nomes) != len(set(nomes)):
                raise ValueError("o catálogo contém municípios duplicados na mesma UF")
    except (OSError, ValueError, KeyError, TypeError) as erro:
        raise RuntimeError(f"Não foi possível carregar o catálogo oficial de municípios: {caminho}") from erro
    return {uf: tuple(catalogo[uf]) for uf, _ in ESTADOS}


CIDADES_POR_ESTADO: dict[str, tuple[str, ...]] = _carregar_municipios()
ESTADOS_CHOICES = [(uf, nome) for uf, nome in ESTADOS]


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
