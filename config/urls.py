"""
RESUMO DO ARQUIVO
=================
Este e o roteador principal do projeto. Ele recebe a URL primeiro e encaminha
para o painel administrativo ou para o conjunto de rotas do app accounts.
"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    # Todas as paginas internas do admin ficam abaixo de /admin/.
    path("admin/", admin.site.urls),

    # include transfere as demais URLs para accounts/urls.py. Como o prefixo e
    # vazio, rotas como cadastro/ ficam diretamente em /cadastro/.
    path("", include("accounts.urls")),
]
