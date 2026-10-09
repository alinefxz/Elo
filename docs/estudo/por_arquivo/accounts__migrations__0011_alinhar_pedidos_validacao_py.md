# accounts/migrations/0011_alinhar_pedidos_validacao.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

**Arquivo original:** [accounts/migrations/0011_alinhar_pedidos_validacao.py](<C:/Users/lb119/Elo/accounts/migrations/0011_alinhar_pedidos_validacao.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
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
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Import — linhas 1 a 1

```python
import django.db.models.deletion
```

**Explicação deste trecho:**

**Linha 1 — Import** (nível 0 do bloco).

Importa módulos: `django.db.models.deletion`.

### Import — linhas 2 a 2

```python
import django.utils.timezone
```

**Explicação deste trecho:**

**Linha 2 — Import** (nível 0 do bloco).

Importa módulos: `django.utils.timezone`.

### ImportFrom — linhas 3 a 3

```python
from django.conf import settings
```

**Explicação deste trecho:**

**Linha 3 — ImportFrom** (nível 0 do bloco).

Importa de `django.conf` os nomes `settings`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 4 a 4

```python
from django.db import migrations, models
```

**Explicação deste trecho:**

**Linha 4 — ImportFrom** (nível 0 do bloco).

Importa de `django.db` os nomes `migrations`, `models`. Pontos iniciais indicam importação relativa ao pacote.

### converter_valores_legados — linhas 7 a 29

```python
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
```

**Explicação deste trecho:**

**Linha 7 — FunctionDef** (nível 0 do bloco).

Define `converter_valores_legados(apps, schema_editor)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 7:

**Linha 8 — Assign** (nível 1 do bloco).

Associa `PedidoSangue` a a chamada `apps.get_model`; argumentos posicionais: `'accounts'`, `'PedidoSangue'`.


**Linha 10 — Assign** (nível 1 do bloco).

Associa `conversoes_urgencia` a um dicionário de 3 entradas; as chaves dão nome aos valores associados.

- Chave `'NORMAL'`: recebe o valor literal `'BAIXA'`.
- Chave `'URGENTE'`: recebe o valor literal `'ALTA'`.
- Chave `'CRITICO'`: recebe o valor literal `'CRITICA'`.

**Linha 15 — Assign** (nível 1 do bloco).

Associa `conversoes_status` a um dicionário de 3 entradas; as chaves dão nome aos valores associados.

- Chave `'PENDENTE'`: recebe o valor literal `'PENDENTE_VALIDACAO'`.
- Chave `'ATENDIDO'`: recebe o valor literal `'ENCERRADO'`.
- Chave `'EXPIRADO'`: recebe o valor literal `'ENCERRADO'`.

**Linha 21 — For** (nível 1 do bloco).

Percorre `conversoes_urgencia.items()`; cada item é atribuído a `(valor_antigo, valor_novo)` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 21:

**Linha 22 — Expr** (nível 2 do bloco).

Executa a chamada `PedidoSangue.objects.filter(urgencia=valor_antigo).update`, que no QuerySet grava diretamente os campos dos resultados, sem chamar save de cada instância; argumentos nomeados: `urgencia=valor_novo`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 26 — For** (nível 1 do bloco).

Percorre `conversoes_status.items()`; cada item é atribuído a `(valor_antigo, valor_novo)` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 26:

**Linha 27 — Expr** (nível 2 do bloco).

Executa a chamada `PedidoSangue.objects.filter(status=valor_antigo).update`, que no QuerySet grava diretamente os campos dos resultados, sem chamar save de cada instância; argumentos nomeados: `status=valor_novo`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

### Migration — linhas 32 a 211

```python
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
```

**Explicação deste trecho:**

**Linha 32 — ClassDef** (nível 0 do bloco).

Define a classe `Migration` herdando de `migrations.Migration`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 32:

**Linha 34 — Assign** (nível 1 do bloco).

Associa `dependencies` a uma coleção List com 1 itens, na expressão `[('accounts', '0010_pedidosangue')]`.

**Linha 38 — Assign** (nível 1 do bloco).

Associa `operations` a uma coleção List com 16 itens, na expressão `[migrations.RenameField(model_name='pedidosangue', old_name='hemocentro', new_name='hemocentro_destino'), migrations.AlterField(model_name='pedidosangue', name='hemocentro_destino', field=models.ForeignKey(db_column='id_hemocentro_destino', limit_choices_to={'perfil': 'HEMOCENTRO'}, on_delete=django.db.models.deletion.PROTECT, related_name='pedidos_recebidos', to=settings.AUTH_USER_MODEL)), migrations.AddField(model_name='pedidosangue', name='titulo', field=models.CharField(default='Pedido de sangue', max_length=150)), migrations.AddField(model_name='pedidosangue', name='justificativa_urgencia', field=models.TextField(blank=True, default='')), migrations.AddField(model_name='pedidosangue', name='atualizado_em', field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now), preserve_default=False), migrations.AlterField(model_name='pedidosangue', name='descricao', field=models.TextField()), migrations.AlterField(model_name='pedidosangue', name='solicitante', field=models.ForeignKey(db_column='id_solicitante', on_delete=django.db.models.deletion.CASCADE, related_name='pedidos_sangue', to=settings.AUTH_USER_MODEL)), migrations.AlterField(model_name='pedidosangue', name='urgencia', field=models.CharField(choices=[('BAIXA', 'Baixa'), ('MEDIA', 'Media'), ('ALTA', 'Alta'), ('CRITICA', 'Critica')], max_length=10)), migrations.AlterField(model_name='pedidosangue', name='status', field=models.CharField(choices=[('PENDENTE_VALIDACAO', 'Pendente de validacao'), ('ATIVO', 'Ativo'), ('SUSPEITO', 'Suspeito'), ('RECUSADO', 'Recusado'), ('ENCERRADO', 'Encerrado')], default='PENDENTE_VALIDACAO', max_length=30)), migrations.RunPython(converter_valores_legados, migrations.RunPython.noop), migrations.RemoveIndex(model_name='pedidosangue', name='pedido_sangue_status_idx'), migrations.RemoveIndex(model_name='pedidosangue', name='pedido_sangue_busca_idx'), migrations.AddIndex(model_name='pedidosangue', index=models.Index(fields=['status', '-data_criacao'], name='pedido_status_data_idx')), migrations.AddIndex(model_name='pedidosangue', index=models.Index(fields=['tipo_sanguineo', 'urgencia'], name='pedido_tipo_urg_idx')), migrations.AddIndex(model_name='pedidosangue', index=models.Index(fields=['cidade'], name='pedido_cidade_idx')), migrations.CreateModel(name='ValidacaoPedido', fields=[('id_validacao', models.BigAutoField(primary_key=True, serialize=False)), ('status_validacao', models.CharField(choices=[('APROVADO', 'Aprovado'), ('SUSPEITO', 'Suspeito'), ('RECUSADO', 'Recusado')], max_length=20)), ('motivo', models.TextField(blank=True, default='')), ('data_validacao', models.DateTimeField(auto_now_add=True)), ('moderador', models.ForeignKey(blank=True, db_column='id_moderador', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='validacoes_pedido_realizadas', to=settings.AUTH_USER_MODEL)), ('pedido', models.ForeignKey(db_column='id_pedido', on_delete=django.db.models.deletion.CASCADE, related_name='validacoes', to='accounts.pedidosangue'))], options={'db_table': 'validacoes_pedido', 'ordering': ['-data_validacao']})]`.

