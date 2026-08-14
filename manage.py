#!/usr/bin/env python
"""
RESUMO DO ARQUIVO
=================
Ponto de entrada dos comandos administrativos executados no terminal.

Exemplos: ``runserver``, ``check``, ``makemigrations``, ``migrate``, ``test`` e
``createsuperuser``. Normalmente este arquivo nao precisa ser alterado.
"""

import os
import sys


def main():
    """Configura o projeto e entrega o comando ao Django."""

    # Indica que config/settings.py contem as configuracoes deste projeto.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    try:
        # A importacao acontece aqui para gerar uma mensagem mais clara quando
        # Django nao foi instalado ou o ambiente virtual nao esta ativo.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Nao foi possivel importar o Django. Confirme a instalacao e "
            "a ativacao do ambiente virtual .venv."
        ) from exc

    # sys.argv contem tudo que veio depois de python manage.py.
    execute_from_command_line(sys.argv)


# Impede que main execute apenas por este arquivo ser importado em outro modulo.
if __name__ == "__main__":
    main()
