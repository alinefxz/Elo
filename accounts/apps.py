"""
RESUMO DO ARQUIVO
=================
Define a configuracao do app accounts. O Django le esta classe durante a
inicializacao para registrar models, admin, migrations e outros componentes.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Metadados basicos do app de contas."""

    # BigAutoField e usado como padrao para chaves primarias nao declaradas.
    default_auto_field = "django.db.models.BigAutoField"

    # Deve ser igual ao nome da pasta Python do app.
    name = "accounts"

    # Nome amigavel exibido no painel administrativo.
    verbose_name = "Contas e autenticacao"

    def ready(self):
        """Carrega os sinais de auditoria quando o app inicia."""

        from . import signals  # noqa: F401
