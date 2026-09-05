"""Configurações usadas somente pela suíte automatizada de testes.

O projeto continua usando PostgreSQL normalmente. Nos testes, o SQLite em
memória evita exigir a permissão CREATEDB do usuário local do PostgreSQL.
"""

from .settings import *  # noqa: F403


# O banco em memória é criado no início dos testes e descartado ao final.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
