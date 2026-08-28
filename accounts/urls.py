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
from . import views
from .forms import LoginUsuarioForm


# O namespace evita conflito com rotas de outros apps que tambem possam se
# chamar login, cadastro ou dashboard.
app_name = "accounts"

urlpatterns = [
    # A raiz / representa o acesso do Visitante, sem cadastro ou login.
    path("", views.inicio, name="inicio"),

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

    # UC_07 - Aprovar Hemocentro. As acoes alteram apenas o backend: status
    # atual do Hemocentro, historico de validacao e auditoria administrativa.
    path(
        "hemocentros/validacao/pendentes/",
        views.hemocentros_pendentes,
        name="hemocentros_pendentes",
    ),
    path(
        "hemocentros/<int:id_hemocentro>/aprovar/",
        views.aprovar_hemocentro,
        name="aprovar_hemocentro",
    ),
    path(
        "hemocentros/<int:id_hemocentro>/recusar/",
        views.recusar_hemocentro,
        name="recusar_hemocentro",
    ),
    path(
        "hemocentros/<int:id_hemocentro>/solicitar-correcao/",
        views.solicitar_correcao_hemocentro,
        name="solicitar_correcao_hemocentro",
    ),
    path(
    "hemocentros/validacao/",
    views.painel_aprovacao_hemocentros,
    name="painel_aprovacao_hemocentros",
),
    path(
    "compatibilidade-sanguinea/",
    views.compatibilidade_sanguinea,
    name="compatibilidade_sanguinea",
),
]