"""Opcoes locais de localizacao, sem limitar a participacao por regiao."""
from django import forms

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
