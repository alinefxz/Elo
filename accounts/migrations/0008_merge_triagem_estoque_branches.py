# Generated manually to reconcile independent accounts migration branches.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "accounts",
            "0007_alter_auditoriaacaocritica_acao_estoque_and_more",
        ),
        (
            "accounts",
            "0007_alter_respostatriagem_options_alter_triagem_options_and_more",
        ),
    ]

    operations = []
