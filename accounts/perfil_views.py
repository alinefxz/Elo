"""Rotas do perfil próprio: o proprietário sempre vem da sessão autenticada."""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .compatibilidade import atualizar_preferencia_convocacao
from .forms import PreferenciaConvocacaoForm
from .models import ConsentimentoLGPD
from .notificacoes import destino_seguro, rotulo_acao
from .perfil_forms import AlterarSenhaForm, PerfilUsuarioForm
from .perfis import HistoricoUsuario, acoes_usuario, apresentar_perfil, resumo_usuario
from .permissoes import acessos_usuario


def formulario_preferencia(usuario, dados=None):
    consentiu = usuario.consentimentos_lgpd.filter(
        tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
        versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO,
        aceito=True, revogado_em__isnull=True,
    ).exists()
    return PreferenciaConvocacaoForm(dados, initial={
        "aceita_convocacoes": usuario.aceita_notificacoes_pedidos and consentiu,
    })


@never_cache
@login_required
@require_GET
def perfil(request):
    usuario = request.user
    avisos = list(usuario.notificacoes.order_by("-criada_em", "-pk")[:5])
    for aviso in avisos:
        aviso.url_acao = destino_seguro(request, aviso.url_destino)
        aviso.rotulo_acao = rotulo_acao(aviso.tipo)
    return render(request, "accounts/perfil.html", {
        "perfil": apresentar_perfil(usuario),
        "acoes_perfil": acoes_usuario(usuario),
        "historico": Paginator(HistoricoUsuario(usuario), 10).get_page(request.GET.get("pagina")),
        "resumo_perfil": resumo_usuario(usuario),
        "notificacoes_perfil": avisos,
        "notificacoes_nao_lidas": usuario.notificacoes.filter(lida=False).count(),
        "validacao_atual": usuario.validacoes_hemocentro.first() if usuario.is_hemocentro else None,
        "preferencia_convocacao": formulario_preferencia(usuario) if acessos_usuario(usuario)["responder_triagem"] else None,
    })


@never_cache
@login_required
@require_http_methods(["GET", "POST"])
def perfil_editar(request):
    form = PerfilUsuarioForm(request.POST if request.method == "POST" else None, instance=request.user)
    if request.method == "POST":
        if form.is_valid():
            with transaction.atomic():
                form.save()
            messages.success(request, "Informações do perfil atualizadas com sucesso.")
            return redirect("accounts:perfil")
        messages.error(request, "Revise os campos indicados para salvar seu perfil.")
    return render(request, "accounts/perfil_editar.html", {"form": form, "perfil": apresentar_perfil(request.user)})


@never_cache
@login_required
@require_http_methods(["GET", "POST"])
def perfil_senha(request):
    form = AlterarSenhaForm(request.user, request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        update_session_auth_hash(request, usuario)
        messages.success(request, "Senha alterada com sucesso.")
        return redirect("accounts:perfil")
    return render(request, "accounts/perfil_senha.html", {"form": form, "perfil": apresentar_perfil(request.user)})


@never_cache
@login_required
@require_POST
def perfil_preferencias(request):
    if not acessos_usuario(request.user)["responder_triagem"]:
        raise PermissionDenied("Somente doadores podem configurar convocações.")
    form = formulario_preferencia(request.user, request.POST)
    if form.is_valid():
        atualizar_preferencia_convocacao(request.user, form.cleaned_data["aceita_convocacoes"], request)
        messages.success(request, "Preferência de alertas salva.")
    else:
        messages.error(request, "Não foi possível salvar a preferência de alertas.")
    return redirect("accounts:perfil")
