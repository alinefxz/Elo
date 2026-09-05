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


app_name = "accounts"


urlpatterns = [
    # Acesso publico.
    path("", views.inicio, name="inicio"),

    # Cadastro.
    path("cadastro/", views.cadastro, name="cadastro"),

    # Login.
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=LoginUsuarioForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),

    # Logout.
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    # Dashboard.
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    # ==========================================================
    # TRIAGEM
    # ==========================================================

    # Pagina publica que explica a triagem e apresenta as modalidades.
    path(
        "triagem/",
        views.triagem_apresentacao,
        name="triagem_apresentacao",
    ),

    # Inicia ou retoma a modalidade escolhida.
    path(
        "triagem/iniciar/<str:modalidade>/",
        views.triagem_iniciar,
        name="triagem_iniciar",
    ),

    # Pergunta atual da triagem.
    path(
        "triagem/<int:id_triagem>/pergunta/",
        views.triagem_pergunta,
        name="triagem_pergunta",
    ),

    # Resultado.
    path(
        "triagem/<int:id_triagem>/resultado/",
        views.triagem_resultado,
        name="triagem_resultado",
    ),

    # Historico do usuario.
    path(
        "triagens/historico/",
        views.triagem_historico,
        name="triagem_historico",
    ),

    # ==========================================================
    # VALIDACAO DE HEMOCENTROS
    # ==========================================================

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

    # ==========================================================
    # COMPATIBILIDADE SANGUINEA
    # ==========================================================

    path(
<<<<<<< HEAD
    "compatibilidade-sanguinea/",
    views.compatibilidade_sanguinea,
    name="compatibilidade_sanguinea",
),
# Essa URL não possui login_required.
# Portanto, visitantes e usuários autenticados podem acessá-la.
path(
    "estoque/",
    views.visualizacao_publica_estoque,
    name="estoque_publico",
),
# Rotas para gerenciamento do estoque pelo Hemocentro.
# O acesso é protegido pelas validações presentes nas views.
path(
    "estoque/hemocentro/",
    views.estoque_hemocentro,
    name="estoque_hemocentro",
),

path(
    "estoque/hemocentro/cadastrar/",
    views.cadastrar_estoque_view,
    name="cadastrar_estoque",
),

path(
    "estoque/hemocentro/<int:id_estoque>/atualizar/",
    views.atualizar_estoque_view,
    name="atualizar_estoque",
),
]
=======
        "compatibilidade-sanguinea/",
        views.compatibilidade_sanguinea,
        name="compatibilidade_sanguinea",
    ),

    # ==========================================================
    # ESTOQUE PUBLICO
    # ==========================================================

    path(
        "estoque/",
        views.visualizacao_publica_estoque,
        name="estoque_publico",
    ),
]
>>>>>>> 943ae952b268b41598072082432051f3f0fbf984
