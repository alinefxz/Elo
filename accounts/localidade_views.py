"""Consulta pública ao catálogo local de municípios, sem consultar contas."""

from django.http import JsonResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from .localidades import CIDADES_POR_ESTADO


@require_GET
@cache_control(public=True, max_age=86400)
def cidades(request):
    estado = request.GET.get("estado", "").upper()
    if estado not in CIDADES_POR_ESTADO:
        return JsonResponse({"erro": "Selecione um estado brasileiro válido."}, status=400)
    return JsonResponse({"estado": estado, "cidades": CIDADES_POR_ESTADO[estado]})
