"""
RESUMO DO ARQUIVO
=================
Este arquivo associa cada endereco do app a uma view.

Exemplo: quando o navegador pede /cadastro/, o Django procura esta lista e
executa views.cadastro. Os nomes das rotas permitem gerar links sem escrever
enderecos manualmente nos templates.
"""

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import RedirectView

from . import views
from .forms import LoginUsuarioForm


# O namespace evita conflito com rotas de outros apps que tambem possam se
# chamar login, cadastro ou dashboard.
app_name = "accounts"

urlpatterns = [
    # A raiz / nao possui pagina propria. RedirectView envia para a rota login.
    # permanent=False produz redirecionamento HTTP 302, adequado neste momento.
    path(
        "",
        RedirectView.as_view(
            pattern_name="accounts:login",
            permanent=False,
        ),
        name="inicio",
    ),

    # View escrita no projeto para criar usuario e consentimento.
    path("cadastro/", views.cadastro, name="cadastro"),

    # LoginView e fornecida pelo Django. Informamos apenas o template, o
    # formulario por e-mail e o comportamento para quem ja esta autenticado.
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=LoginUsuarioForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),

    # LogoutView encerra a sessao. O template chama esta rota usando POST.
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    # A protecao desta rota esta no decorador login_required da view.
    path("dashboard/", views.dashboard, name="dashboard"),
]
