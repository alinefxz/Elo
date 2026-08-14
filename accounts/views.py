from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import CadastroUsuarioForm
from .models import ConsentimentoLGPD


def obter_ip(request):
    """Obtem o IP para registrar a origem do consentimento LGPD."""

    encaminhado = request.META.get("HTTP_X_FORWARDED_FOR")
    if encaminhado:
        return encaminhado.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def cadastro(request):
    """Exibe o formulario e cria usuario e consentimento em uma transacao."""

    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            # Se uma das gravacoes falhar, nenhuma delas fica incompleta no banco.
            with transaction.atomic():
                usuario = form.save()
                ConsentimentoLGPD.objects.create(
                    usuario=usuario,
                    tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL,
                    versao_termo="1.0",
                    aceito=True,
                    ip=obter_ip(request),
                )

            # O novo usuario ja entra no sistema depois do cadastro.
            login(request, usuario)
            messages.success(request, "Cadastro realizado com sucesso.")
            return redirect("accounts:dashboard")
    else:
        form = CadastroUsuarioForm()

    return render(request, "accounts/cadastro.html", {"form": form})


@login_required
def dashboard(request):
    """Pagina simples protegida: apenas usuarios autenticados podem acessa-la."""

    return render(request, "accounts/dashboard.html")
