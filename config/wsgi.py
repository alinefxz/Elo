"""
RESUMO DO ARQUIVO
=================
Ponto de entrada WSGI para publicacao em servidores web tradicionais.

Servidores como Gunicorn ou uWSGI importam ``application`` deste modulo. Durante
o desenvolvimento, ``runserver`` cuida disso automaticamente.
"""

import os

from django.core.wsgi import get_wsgi_application


# Informa ao Django onde estao as configuracoes do projeto.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Objeto chamado pelo servidor para processar cada requisicao HTTP.
application = get_wsgi_application()
