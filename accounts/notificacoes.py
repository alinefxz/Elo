"""Consulta privada e leitura dos avisos existentes; nao cria convocacoes."""
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Max, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST


def destino_seguro(request, url):
    if url and url_has_allowed_host_and_scheme(
        url, allowed_hosts={request.get_host()}, require_https=request.is_secure(),
    ):
        return url
    return ''


def rotulo_acao(tipo):
    if tipo in ('ESTOQUE_CRITICO', 'ESTOQUE_BAIXO'):
        return 'Ver estoque'
    if tipo == 'PEDIDO_COMPATIVEL':
        return 'Ver pedido'
    return 'Ver detalhes'


def apresentar(request, aviso):
    return {
        'id': aviso.pk, 'titulo': aviso.titulo, 'mensagem': aviso.mensagem,
        'tipo': aviso.get_tipo_display(), 'lida': aviso.lida,
        'data': timezone.localtime(aviso.criada_em).strftime('%d/%m/%Y %H:%M'),
        'data_iso': aviso.criada_em.isoformat(),
        'url': destino_seguro(request, aviso.url_destino),
        'acao': rotulo_acao(aviso.tipo),
        'url_leitura': reverse('accounts:notificacao_ler', args=[aviso.pk]),
    }


def resumo(request, depois=None):
    avisos = request.user.notificacoes.all()
    totais = avisos.aggregate(nao_lidas=Count('pk', filter=Q(lida=False)), ultimo_id=Max('pk'))
    resultado = {
        'nao_lidas': totais['nao_lidas'], 'ultimo_id': totais['ultimo_id'] or 0,
        'itens': [apresentar(request, aviso) for aviso in avisos.order_by('-criada_em', '-pk')[:8]],
        'novas': [],
    }
    if depois is not None:
        resultado['novas'] = [apresentar(request, aviso) for aviso in
                              avisos.filter(pk__gt=depois, lida=False).order_by('-pk')[:5]]
    return resultado


def contexto_sino(request):
    if not request.user.is_authenticated:
        return {}
    return {'sino_notificacoes': resumo(request)}


@never_cache
@require_GET
def atualizacoes(request):
    if not request.user.is_authenticated:
        return JsonResponse({'erro': 'Entre novamente para consultar os avisos.'}, status=401)
    depois = request.GET.get('depois')
    if depois is not None:
        try:
            depois = int(depois)
            if not 0 <= depois <= 9223372036854775807:
                raise ValueError
        except (TypeError, ValueError):
            return JsonResponse({'erro': 'Identificador invalido.'}, status=400)
    return JsonResponse(resumo(request, depois))


@never_cache
@login_required
@require_GET
def central(request):
    pagina = Paginator(request.user.notificacoes.order_by('-criada_em', '-pk'), 10).get_page(
        request.GET.get('pagina'),
    )
    for aviso in pagina:
        aviso.url_acao = destino_seguro(request, aviso.url_destino)
        aviso.rotulo_acao = rotulo_acao(aviso.tipo)
    return render(request, 'accounts/notificacoes.html', {'pagina_notificacoes': pagina})


@never_cache
@login_required
@require_POST
def marcar_lida(request, id_notificacao):
    aviso = get_object_or_404(request.user.notificacoes, pk=id_notificacao)
    request.user.notificacoes.filter(pk=aviso.pk, lida=False).update(lida=True, lida_em=timezone.now())
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse({'id': aviso.pk, 'lida': True})
    return redirect('accounts:notificacoes')
