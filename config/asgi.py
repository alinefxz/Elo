"""
RESUMO DO ARQUIVO
=================
Ponto de entrada ASGI para publicacao em servidores assincronos.

ASGI permite recursos como WebSockets e conexoes assincronas. O desenvolvimento
atual nao usa esses recursos diretamente, mas o Django gera este arquivo para
deixar o projeto preparado para um servidor compativel.
"""

import os

from django.core.asgi import get_asgi_application


# Informa ao Django onde estao as configuracoes antes de criar a aplicacao.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Servidores ASGI importam esta variavel para encaminhar requisicoes ao Django.
application = get_asgi_application()
