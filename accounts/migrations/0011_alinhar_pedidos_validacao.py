import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


def converter_valores_legados(apps, schema_editor):
    PedidoSangue = apps.get_model("accounts", "PedidoSangue")

    conversoes_urgencia = {
        "NORMAL": "BAIXA",
        "URGENTE": "ALTA",
        "CRITICO": "CRITICA",
    }
    conversoes_status = {
        "PENDENTE": "PENDENTE_VALIDACAO",
        "ATENDIDO": "ENCERRADO",
        "EXPIRADO": "ENCERRADO",
    }

    for valor_antigo, valor_novo in conversoes_urgencia.items():
        PedidoSangue.objects.filter(urgencia=valor_antigo).update(
            urgencia=valor_novo
        )

    for valor_antigo, valor_novo in conversoes_status.items():
        PedidoSangue.objects.filter(status=valor_antigo).update(
            status=valor_novo
        )


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0010_pedidosangue"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pedidosangue",
            old_name="hemocentro",
            new_name="hemocentro_destino",
        ),
        migrations.AlterField(
            model_name="pedidosangue",
            name="hemocentro_destino",
            field=models.ForeignKey(
                db_column="id_hemocentro_destino",
                limit_choices_to={"perfil": "HEMOCENTRO"},
                on_delete=django.db.models.deletion.PROTECT,
                related_name="pedidos_recebidos",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="pedidosangue",
            name="titulo",
            field=models.CharField(
                default="Pedido de sangue",
                max_length=150,
            ),
        ),
        migrations.AddField(
            model_name="pedidosangue",
            name="justificativa_urgencia",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="pedidosangue",
            name="atualizado_em",
            field=models.DateTimeField(
                auto_now=True,
                default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="pedidosangue",
            name="descricao",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="pedidosangue",
            name="solicitante",
            field=models.ForeignKey(
                db_column="id_solicitante",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pedidos_sangue",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="pedidosangue",
            name="urgencia",
            field=models.CharField(
                choices=[
                    ("BAIXA", "Baixa"),
                    ("MEDIA", "Media"),
                    ("ALTA", "Alta"),
                    ("CRITICA", "Critica"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="pedidosangue",
            name="status",
            field=models.CharField(
                choices=[
                    (
                        "PENDENTE_VALIDACAO",
                        "Pendente de validacao",
                    ),
                    ("ATIVO", "Ativo"),
                    ("SUSPEITO", "Suspeito"),
                    ("RECUSADO", "Recusado"),
                    ("ENCERRADO", "Encerrado"),
                ],
                default="PENDENTE_VALIDACAO",
                max_length=30,
            ),
        ),
        migrations.RunPython(
            converter_valores_legados,
            migrations.RunPython.noop,
        ),
        migrations.RemoveIndex(
            model_name="pedidosangue",
            name="pedido_sangue_status_idx",
        ),
        migrations.RemoveIndex(
            model_name="pedidosangue",
            name="pedido_sangue_busca_idx",
        ),
        migrations.AddIndex(
            model_name="pedidosangue",
            index=models.Index(
                fields=["status", "-data_criacao"],
                name="pedido_status_data_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="pedidosangue",
            index=models.Index(
                fields=["tipo_sanguineo", "urgencia"],
                name="pedido_tipo_urg_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="pedidosangue",
            index=models.Index(
                fields=["cidade"],
                name="pedido_cidade_idx",
            ),
        ),
        migrations.CreateModel(
            name="ValidacaoPedido",
            fields=[
                (
                    "id_validacao",
                    models.BigAutoField(
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status_validacao",
                    models.CharField(
                        choices=[
                            ("APROVADO", "Aprovado"),
                            ("SUSPEITO", "Suspeito"),
                            ("RECUSADO", "Recusado"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "motivo",
                    models.TextField(blank=True, default=""),
                ),
                (
                    "data_validacao",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "moderador",
                    models.ForeignKey(
                        blank=True,
                        db_column="id_moderador",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="validacoes_pedido_realizadas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "pedido",
                    models.ForeignKey(
                        db_column="id_pedido",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="validacoes",
                        to="accounts.pedidosangue",
                    ),
                ),
            ],
            options={
                "db_table": "validacoes_pedido",
                "ordering": ["-data_validacao"],
            },
        ),
    ]
