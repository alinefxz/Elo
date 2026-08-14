"""
RESUMO DO ARQUIVO
=================
As views recebem requisicoes do navegador, executam a regra da pagina e
devolvem uma resposta.

Fluxo do cadastro:
GET -> mostra formulario vazio.
POST -> valida -> grava usuario + consentimento -> cria sessao -> dashboard.

O cadastro usa uma transacao para impedir que apenas metade da operacao seja
salva. O dashboard usa login_required para bloquear visitantes.
"""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import CadastroUsuarioForm
from .models import ConsentimentoLGPD


def obter_ip(request):
    """Extrai o IP usado no registro do consentimento LGPD."""

    # Proxies podem informar uma lista de IPs no cabecalho X-Forwarded-For.
    # O primeiro normalmente representa o cliente original.
    encaminhado = request.META.get("HTTP_X_FORWARDED_FOR")
    if encaminhado:
        return encaminhado.split(",")[0].strip()

    # Em desenvolvimento local, REMOTE_ADDR normalmente sera 127.0.0.1.
    return request.META.get("REMOTE_ADDR")


def cadastro(request):
    """Mostra o formulario e processa a criacao de uma conta do Elo."""

    # Uma pessoa que ja entrou nao precisa abrir cadastro novamente.
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    # GET apenas exibe a pagina. POST significa que o formulario foi enviado.
    if request.method == "POST":
        # request.POST contem os valores enviados pelos inputs do HTML.
        form = CadastroUsuarioForm(request.POST)

        # is_valid executa validacoes de campo, senha e unicidade.
        if form.is_valid():
            # atomic abre uma transacao no PostgreSQL. Se a criacao do usuario
            # ou do consentimento falhar, o banco desfaz as duas operacoes.
            with transaction.atomic():
                # UserCreationForm chama set_password antes de salvar.
                usuario = form.save()

                # O aceite nao pertence a usuarios: ele gera uma linha propria
                # em consentimentos_lgpd ligada pela chave estrangeira.
                ConsentimentoLGPD.objects.create(
                    usuario=usuario,
                    tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL,
                    versao_termo="1.0",
                    aceito=True,
                    ip=obter_ip(request),
                )

            # login grava a identidade do usuario na sessao do Django.
            # O navegador recebe apenas um cookie de sessao, nunca a senha.
            login(request, usuario)

            # A mensagem fica na sessao ate base.html exibi-la uma vez.
            messages.success(request, "Cadastro realizado com sucesso.")
            return redirect("accounts:dashboard")
    else:
        # No GET, nao existem dados enviados: criamos um formulario vazio.
        form = CadastroUsuarioForm()

    # render combina o template com o dicionario de contexto.
    # O HTML acessa o objeto usando a variavel {{ form }}.
    return render(request, "accounts/cadastro.html", {"form": form})


@login_required
def dashboard(request):
    """Mostra uma pagina protegida para confirmar que o login funcionou."""

    # Se nao houver sessao valida, login_required redireciona para LOGIN_URL.
    return render(request, "accounts/dashboard.html")
