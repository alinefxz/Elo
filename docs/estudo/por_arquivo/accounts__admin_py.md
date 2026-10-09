# accounts/admin.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Telas do Django admin, autorizacoes e auditoria de operacoes.

**Arquivo original:** [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""
RESUMO DO ARQUIVO
=================

Configura como Usuario, ConsentimentoLGPD e auditorias aparecem no /admin/.

O admin e uma ferramenta interna para pessoas autorizadas. Ele nao substitui
as telas normais do sistema. Os formularios abaixo garantem que uma senha
criada no painel tambem seja transformada em hash.
"""

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .auditoria import campos_sensiveis_alterados, registrar_auditoria
from .models import (
    Usuario,
    ValidacaoHemocentro,
    ConsentimentoLGPD,
    AuditoriaAcaoCritica,
    Triagem,
    RespostaTriagem,
    Estoque,
    EstoqueMovimentacao,
    Notificacao,
    PedidoSangue,
    ValidacaoPedido,
)

from .validacao_hemocentro import (
    aprovar_hemocentro,
    recusar_hemocentro,
    solicitar_correcao_hemocentro,
)


class UsuarioAdminCreationForm(UserCreationForm):
    """Formulario usado quando o admin cria uma conta."""

    class Meta:
        model = Usuario

        # Estes sao os dados minimos pedidos na tela de criacao do admin.
        # Os outros dados podem ser completados depois na tela de edicao.
        fields = ("email", "nome", "perfil")


class UsuarioAdminChangeForm(UserChangeForm):
    """Formulario usado quando o admin edita uma conta existente."""

    class Meta:
        model = Usuario
        fields = "__all__"


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Define listagem, busca e organizacao dos campos de Usuario."""

    # UserAdmin foi criado pensando no usuario padrao. Estas atribuicoes dizem
    # a ele para usar os formularios e o model personalizados do Elo.
    add_form = UsuarioAdminCreationForm
    form = UsuarioAdminChangeForm
    model = Usuario

    # Colunas exibidas na lista principal de usuarios.
    list_display = (
        "email",
        "nome",
        "perfil",
        "tipo_sanguineo",
        "status_validacao",
        "is_active",
        "suspensa",
        "email_verificado",
        "is_staff",
    )

    # Filtros laterais e campos pesquisaveis no painel.
    list_filter = (
        "perfil",
        "tipo_sanguineo",
        "status_validacao",
        "is_active",
        "suspensa",
        "email_verificado",
        "is_staff",
    )

    search_fields = ("email", "nome", "cpf", "cnpj")
    ordering = ("nome",)

    actions = (
        "aprovar_hemocentros_selecionados",
        "recusar_hemocentros_selecionados",
        "solicitar_correcao_hemocentros_selecionados",
    )

    # Datas automaticas devem ser visualizadas, nao digitadas manualmente.
    readonly_fields = (
        "status_validacao",
        "last_login",
        "date_joined",
        "atualizado_em",
    )

    # fieldsets organiza a tela de EDICAO de uma conta existente.
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Dados da conta",
            {
                "fields": (
                    "nome",
                    "perfil",
                    "cpf",
                    "cnpj",
                    "telefone",
                    "data_nascimento",
                    "sexo",
                    "tipo_sanguineo",
                    "tipo_sanguineo_confirmado",
                    "cidade",
                    "estado",
                    "status_validacao",
                    "email_verificado",
                )
            },
        ),
        (
            "Permissoes internas do Django",
            {
                "fields": (
                    "is_active",
                    "suspensa",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Datas",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "atualizado_em",
                )
            },
        ),
    )

    # add_fieldsets organiza a tela de CRIACAO de uma conta no admin.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "nome",
                    "perfil",
                    "password1",
                    "password2",
                    "is_active",
                    "suspensa",
                    "is_staff",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        """Audita mudancas administrativas em perfil e permissoes."""

        campos_auditados = [
            "perfil",
            "is_active",
            "is_staff",
            "is_superuser",
            "email_verificado",
            "suspensa",
            "nome",
            "email",
            "cpf",
            "cnpj",
            "cidade",
            "estado",
            "data_nascimento",
            "tipo_sanguineo",
        ]

        alteracoes = (
            campos_sensiveis_alterados(obj, campos_auditados)
            if change
            else {}
        )

        super().save_model(request, obj, form, change)

        if alteracoes:
            # Alteracoes cadastrais guardam apenas nomes de campos, sem
            # duplicar CPF, nascimento ou outros dados pessoais na auditoria.
            permissoes = {campo: valor for campo, valor in alteracoes.items()
                          if campo in {"perfil", "is_active", "is_staff", "is_superuser", "email_verificado", "suspensa"}}
            suspensao = (
                "is_active" in permissoes and not obj.is_active
            ) or ("suspensa" in permissoes and obj.suspensa)
            registrar_auditoria(
                acao=(AuditoriaAcaoCritica.Acao.ALTERACAO_PERMISSAO if permissoes
                      else AuditoriaAcaoCritica.Acao.MODERACAO),
                usuario=request.user,
                alvo=obj,
                descricao="Desativacao administrativa de usuario." if suspensao
                else "Alteracao administrativa de usuario.",
                request=request,
                metadados={"evento": "SUSPENSAO_USUARIO" if suspensao else "ALTERACAO_ADMINISTRATIVA",
                           "alteracoes": permissoes, "campos_alterados": sorted(alteracoes)},
            )
        elif not change:
            registrar_auditoria(
                acao=AuditoriaAcaoCritica.Acao.MODERACAO,
                usuario=request.user, alvo=obj, request=request,
                descricao="Criacao administrativa de usuario.",
                metadados={"evento": "ALTERACAO_ADMINISTRATIVA", "operacao": "CRIACAO_USUARIO"},
            )

    def _executar_acao_validacao(
        self,
        request,
        queryset,
        funcao,
        parecer,
    ):
        """Aplica uma decisao de validacao aos Hemocentros selecionados."""

        hemocentros = queryset.filter(
            perfil=Usuario.Perfil.HEMOCENTRO
        )

        ignorados = queryset.exclude(
            perfil=Usuario.Perfil.HEMOCENTRO
        ).count()

        total = 0

        for hemocentro in hemocentros:
            funcao(
                hemocentro=hemocentro,
                admin=request.user,
                parecer=parecer,
                request=request,
            )
            total += 1

        if total:
            self.message_user(
                request,
                f"{total} Hemocentro(s) atualizado(s) com sucesso.",
                level=messages.SUCCESS,
            )

        if ignorados:
            self.message_user(
                request,
                f"{ignorados} usuario(s) ignorado(s) por nao serem Hemocentros.",
                level=messages.WARNING,
            )

    @admin.action(description="Aprovar Hemocentros selecionados")
    def aprovar_hemocentros_selecionados(self, request, queryset):
        """Acao em lote que aprova Hemocentros e registra historico."""

        self._executar_acao_validacao(
            request,
            queryset,
            aprovar_hemocentro,
            "Hemocentro aprovado pelo painel administrativo.",
        )

    @admin.action(description="Recusar Hemocentros selecionados")
    def recusar_hemocentros_selecionados(self, request, queryset):
        """Acao em lote que recusa Hemocentros e registra historico."""

        self._executar_acao_validacao(
            request,
            queryset,
            recusar_hemocentro,
            "Hemocentro recusado pelo painel administrativo.",
        )

    @admin.action(
        description="Solicitar correcao dos Hemocentros selecionados"
    )
    def solicitar_correcao_hemocentros_selecionados(
        self,
        request,
        queryset,
    ):
        """Acao em lote que solicita correcao cadastral e registra historico."""

        self._executar_acao_validacao(
            request,
            queryset,
            solicitar_correcao_hemocentro,
            "Correcao cadastral solicitada pelo painel administrativo.",
        )

    def save_related(self, request, form, formsets, change):
        """Audita mudancas em grupos e permissoes diretas do usuario."""

        obj = form.instance

        grupos_antes = set()
        permissoes_antes = set()

        if change and obj.pk:
            usuario_atual = Usuario.objects.get(pk=obj.pk)

            grupos_antes = set(
                usuario_atual.groups.values_list(
                    "name",
                    flat=True,
                )
            )

            permissoes_antes = set(
                usuario_atual.user_permissions.values_list(
                    "codename",
                    flat=True,
                )
            )

        super().save_related(
            request,
            form,
            formsets,
            change,
        )

        if not change:
            return

        grupos_depois = set(
            obj.groups.values_list(
                "name",
                flat=True,
            )
        )

        permissoes_depois = set(
            obj.user_permissions.values_list(
                "codename",
                flat=True,
            )
        )

        alteracoes = {}

        if grupos_antes != grupos_depois:
            alteracoes["groups"] = {
                "antes": sorted(grupos_antes),
                "depois": sorted(grupos_depois),
            }

        if permissoes_antes != permissoes_depois:
            alteracoes["user_permissions"] = {
                "antes": sorted(permissoes_antes),
                "depois": sorted(permissoes_depois),
            }

        if alteracoes:
            registrar_auditoria(
                acao=AuditoriaAcaoCritica.Acao.ALTERACAO_PERMISSAO,
                usuario=request.user,
                alvo=obj,
                descricao="Alteracao administrativa de grupos ou permissoes.",
                request=request,
                metadados={"evento": "ALTERACAO_PERMISSAO", "alteracoes": alteracoes},
            )


@admin.register(ValidacaoHemocentro)
class ValidacaoHemocentroAdmin(admin.ModelAdmin):
    """Consulta somente leitura do historico institucional de Hemocentros."""

    list_display = (
        "data_analise",
        "hemocentro",
        "status",
        "admin",
        "parecer_resumido",
    )

    list_filter = (
        "status",
        "data_analise",
    )

    search_fields = (
        "hemocentro__email",
        "hemocentro__nome",
        "hemocentro__cnpj",
        "admin__email",
        "admin__nome",
        "parecer",
    )

    readonly_fields = (
        "id_validacao",
        "hemocentro",
        "admin",
        "status",
        "parecer",
        "data_analise",
    )

    date_hierarchy = "data_analise"
    ordering = ("-data_analise",)

    def parecer_resumido(self, obj):
        """Mostra um trecho curto do parecer na listagem."""

        if len(obj.parecer) <= 80:
            return obj.parecer

        return f"{obj.parecer[:77]}..."

    parecer_resumido.short_description = "Parecer"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ConsentimentoLGPD)
class ConsentimentoLGPDAdmin(admin.ModelAdmin):
    """Permite consultar os aceites LGPD no painel administrativo."""

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.MODERACAO,
            usuario=request.user, alvo=obj, request=request,
            descricao="Alteracao administrativa de consentimento." if change
            else "Criacao administrativa de consentimento.",
            metadados={"evento": "ALTERACAO_ADMINISTRATIVA",
                       "campos_alterados": list(form.changed_data)},
        )

    list_display = (
        "usuario",
        "tipo_termo",
        "versao_termo",
        "aceito",
        "data_aceite",
    )

    list_filter = (
        "tipo_termo",
        "aceito",
        "versao_termo",
    )

    search_fields = (
        "usuario__email",
        "usuario__nome",
    )

    # A data representa um evento real e nao deve ser alterada pelo formulario.
    readonly_fields = (
        "data_aceite",
    )


@admin.register(AuditoriaAcaoCritica)
class AuditoriaAcaoCriticaAdmin(admin.ModelAdmin):
    """Consulta somente leitura das acoes criticas registradas."""

    def has_view_permission(self, request, obj=None):
        return (
            request.user.perfil == Usuario.Perfil.ADMINISTRADOR
            and super().has_view_permission(request, obj)
        )

    def has_module_permission(self, request):
        return self.has_view_permission(request)

    list_display = (
        "criado_em",
        "acao",
        "resultado",
        "usuario",
        "alvo_tipo",
        "alvo_id",
        "ip",
    )

    list_filter = (
        "acao",
        "resultado",
        "criado_em",
    )

    search_fields = (
        "usuario__email",
        "usuario__nome",
        "descricao",
        "metadados",
        "alvo_tipo",
        "alvo_id",
        "ip",
    )

    readonly_fields = (
        "id_auditoria",
        "usuario",
        "acao",
        "resultado",
        "alvo_tipo",
        "alvo_id",
        "descricao",
        "ip",
        "user_agent",
        "metadados",
        "criado_em",
    )

    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    """
    Consulta administrativa do estoque de cada Hemocentro.

    status_calculado e data_atualizacao ficam somente leitura porque sao
    derivados automaticamente pela camada de servico (accounts/estoque.py)
    sempre que a quantidade de bolsas muda.
    """

    list_display = (
        "hemocentro",
        "tipo_sanguineo",
        "quantidade_bolsas",
        "nivel_minimo",
        "nivel_critico",
        "status_calculado",
        "data_atualizacao",
    )

    list_filter = (
        "status_calculado",
        "tipo_sanguineo",
    )

    search_fields = (
        "hemocentro__email",
        "hemocentro__nome",
    )

    ordering = (
        "hemocentro__nome",
        "tipo_sanguineo",
    )

    readonly_fields = (
        "status_calculado",
        "data_atualizacao",
    )


@admin.register(EstoqueMovimentacao)
class EstoqueMovimentacaoAdmin(admin.ModelAdmin):
    """
    Historico somente leitura das movimentacoes de estoque (UC_30).

    Assim como ValidacaoHemocentroAdmin, este historico nunca deve ser
    criado, editado ou apagado pelo admin: toda movimentacao precisa
    passar por registrar_movimentacao_estoque para manter a quantidade
    de bolsas e a auditoria consistentes.
    """

    list_display = (
        "data_hora",
        "estoque",
        "tipo_movimento",
        "quantidade_anterior",
        "quantidade_movimentada",
        "quantidade_nova",
        "usuario_resp",
    )

    list_filter = (
        "tipo_movimento",
        "data_hora",
    )

    search_fields = (
        "estoque__hemocentro__email",
        "estoque__hemocentro__nome",
        "usuario_resp__email",
        "usuario_resp__nome",
        "motivo",
    )

    readonly_fields = (
        "id_mov",
        "estoque",
        "usuario_resp",
        "tipo_movimento",
        "quantidade_anterior",
        "quantidade_movimentada",
        "quantidade_nova",
        "motivo",
        "data_hora",
    )

    date_hierarchy = "data_hora"
    ordering = ("-data_hora",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Triagem)
class TriagemAdmin(admin.ModelAdmin):
    """
    Permite ao administrador consultar as triagens realizadas.

    Os dados ficam somente para consulta no painel administrativo.
    """

    # Colunas exibidas na listagem de triagens.
    list_display = (
        "id_triagem",
        "usuario",
        "modalidade",
        "status",
        "resultado",
        "regra_version",
        "data_liberacao",
        "iniciada_em",
        "finalizada_em",
    )

    # Filtros disponíveis no lado direito do admin.
    list_filter = (
        "modalidade",
        "status",
        "resultado",
        "regra_version",
        "iniciada_em",
    )

    # Campos usados na busca.
    search_fields = (
        "usuario__nome",
        "usuario__email",
        "regra_version",
    )

    # Impede alteração manual de resultados médicos.
    readonly_fields = (
        "id_triagem",
        "usuario",
        "modalidade",
        "status",
        "pergunta_atual",
        "fluxo_perguntas",
        "triagem_base",
        "regra_version",
        "resultado",
        "mensagem_resultado",
        "data_liberacao",
        "achados",
        "iniciada_em",
        "finalizada_em",
        "atualizada_em",
    )

    # Mostra a navegação por data.
    date_hierarchy = "iniciada_em"

    # Ordena as triagens mais recentes primeiro.
    ordering = ("-iniciada_em",)

    # Impede criação manual pelo administrador.
    def has_add_permission(self, request):
        return False

    # Impede alteração pelo administrador.
    def has_change_permission(self, request, obj=None):
        return False

    # Impede exclusão pelo administrador.
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RespostaTriagem)
class RespostaTriagemAdmin(admin.ModelAdmin):
    """
    Permite consultar as respostas individuais das triagens.
    """

    # Colunas exibidas na listagem.
    list_display = (
        "id_resposta",
        "triagem",
        "id_pergunta",
        "codigo_resposta",
        "resposta_label",
        "data_evento",
        "respondido_em",
    )

    # Filtros disponíveis.
    list_filter = (
        "id_pergunta",
        "rule_version",
        "respondido_em",
    )

    # Campos pesquisáveis.
    search_fields = (
        "triagem__usuario__nome",
        "triagem__usuario__email",
        "id_pergunta",
        "codigo_resposta",
        "resposta_label",
    )

    # Respostas não devem ser editadas manualmente.
    readonly_fields = (
        "id_resposta",
        "triagem",
        "id_pergunta",
        "codigo_resposta",
        "resposta_label",
        "data_evento",
        "metadata",
        "valor",
        "rule_version",
        "source_ref",
        "respondido_em",
    )

    # Ordena pelas respostas mais recentes.
    ordering = ("-respondido_em",)

    # Impede criação manual.
    def has_add_permission(self, request):
        return False

    # Impede alteração.
    def has_change_permission(self, request, obj=None):
        return False

    # Impede exclusão.
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    """Permite consultar os avisos internos enviados aos usuarios."""

    list_display = (
        "usuario",
        "tipo",
        "titulo",
        "lida",
        "criada_em",
    )

    list_filter = (
        "tipo",
        "lida",
        "criada_em",
    )

    search_fields = (
        "usuario__email",
        "usuario__nome",
        "titulo",
        "mensagem",
    )

    readonly_fields = (
        "criada_em",
        "lida_em",
    )

    ordering = ("-criada_em",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PedidoSangue)
class PedidoSangueAdmin(admin.ModelAdmin):
    """
    Consulta administrativa dos pedidos de sangue.

    A validacao deve acontecer pela camada de servico e pelo painel de
    validacao, nao editando status manualmente no admin.
    """

    list_display = (
        "id_pedido",
        "titulo",
        "solicitante",
        "contato",
        "hemocentro_destino",
        "tipo_sanguineo",
        "urgencia",
        "cidade",
        "status",
        "data_criacao",
    )

    list_filter = (
        "status",
        "urgencia",
        "tipo_sanguineo",
        "data_criacao",
    )

    search_fields = (
        "titulo",
        "cidade",
        "solicitante__email",
        "solicitante__nome",
        "hemocentro_destino__email",
        "hemocentro_destino__nome",
    )

    readonly_fields = (
        "id_pedido",
        "status",
        "data_criacao",
        "atualizado_em",
    )

    date_hierarchy = "data_criacao"
    ordering = ("-data_criacao",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ValidacaoPedido)
class ValidacaoPedidoAdmin(admin.ModelAdmin):
    """Historico somente leitura das validacoes de pedidos."""

    list_display = (
        "data_validacao",
        "pedido",
        "status_validacao",
        "moderador",
        "motivo_resumido",
    )

    list_filter = (
        "status_validacao",
        "data_validacao",
    )

    search_fields = (
        "pedido__titulo",
        "pedido__cidade",
        "moderador__email",
        "moderador__nome",
        "motivo",
    )

    readonly_fields = (
        "id_validacao",
        "pedido",
        "status_validacao",
        "motivo",
        "moderador",
        "data_validacao",
    )

    date_hierarchy = "data_validacao"
    ordering = ("-data_validacao",)

    def motivo_resumido(self, obj):
        if len(obj.motivo) <= 80:
            return obj.motivo

        return f"{obj.motivo[:77]}..."

    motivo_resumido.short_description = "Motivo"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 10

```python
"""
RESUMO DO ARQUIVO
=================

Configura como Usuario, ConsentimentoLGPD e auditorias aparecem no /admin/.

O admin e uma ferramenta interna para pessoas autorizadas. Ele nao substitui
as telas normais do sistema. Os formularios abaixo garantem que uma senha
criada no painel tambem seja transformada em hash.
"""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 12 a 12

```python
from django.contrib import admin, messages
```

**Explicação deste trecho:**

**Linha 12 — ImportFrom** (nível 0 do bloco).

Importa de `django.contrib` os nomes `admin`, `messages`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 13 a 13

```python
from django.contrib.auth.admin import UserAdmin
```

**Explicação deste trecho:**

**Linha 13 — ImportFrom** (nível 0 do bloco).

Importa de `django.contrib.auth.admin` os nomes `UserAdmin`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 14 a 14

```python
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
```

**Explicação deste trecho:**

**Linha 14 — ImportFrom** (nível 0 do bloco).

Importa de `django.contrib.auth.forms` os nomes `UserChangeForm`, `UserCreationForm`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 16 a 16

```python
from .auditoria import campos_sensiveis_alterados, registrar_auditoria
```

**Explicação deste trecho:**

**Linha 16 — ImportFrom** (nível 0 do bloco).

Importa de `.auditoria` os nomes `campos_sensiveis_alterados`, `registrar_auditoria`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 17 a 29

```python
from .models import (
    Usuario,
    ValidacaoHemocentro,
    ConsentimentoLGPD,
    AuditoriaAcaoCritica,
    Triagem,
    RespostaTriagem,
    Estoque,
    EstoqueMovimentacao,
    Notificacao,
    PedidoSangue,
    ValidacaoPedido,
)
```

**Explicação deste trecho:**

**Linha 17 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `Usuario`, `ValidacaoHemocentro`, `ConsentimentoLGPD`, `AuditoriaAcaoCritica`, `Triagem`, `RespostaTriagem`, `Estoque`, `EstoqueMovimentacao`, `Notificacao`, `PedidoSangue`, `ValidacaoPedido`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 31 a 35

```python
from .validacao_hemocentro import (
    aprovar_hemocentro,
    recusar_hemocentro,
    solicitar_correcao_hemocentro,
)
```

**Explicação deste trecho:**

**Linha 31 — ImportFrom** (nível 0 do bloco).

Importa de `.validacao_hemocentro` os nomes `aprovar_hemocentro`, `recusar_hemocentro`, `solicitar_correcao_hemocentro`. Pontos iniciais indicam importação relativa ao pacote.

### UsuarioAdminCreationForm — linhas 38 a 46

```python
class UsuarioAdminCreationForm(UserCreationForm):
    """Formulario usado quando o admin cria uma conta."""

    class Meta:
        model = Usuario

        # Estes sao os dados minimos pedidos na tela de criacao do admin.
        # Os outros dados podem ser completados depois na tela de edicao.
        fields = ("email", "nome", "perfil")
```

**Explicação deste trecho:**

**Linha 38 — ClassDef** (nível 0 do bloco).

Define a classe `UsuarioAdminCreationForm` herdando de `UserCreationForm`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 38:

**Linha 39 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 41 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 41:

**Linha 42 — Assign** (nível 2 do bloco).

Associa `model` a o valor associado ao nome `Usuario`.

**Linha 46 — Assign** (nível 2 do bloco).

Associa `fields` a uma coleção Tuple com 3 itens, na expressão `('email', 'nome', 'perfil')`.

### UsuarioAdminChangeForm — linhas 49 a 54

```python
class UsuarioAdminChangeForm(UserChangeForm):
    """Formulario usado quando o admin edita uma conta existente."""

    class Meta:
        model = Usuario
        fields = "__all__"
```

**Explicação deste trecho:**

**Linha 49 — ClassDef** (nível 0 do bloco).

Define a classe `UsuarioAdminChangeForm` herdando de `UserChangeForm`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 49:

**Linha 50 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 52 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 52:

**Linha 53 — Assign** (nível 2 do bloco).

Associa `model` a o valor associado ao nome `Usuario`.

**Linha 54 — Assign** (nível 2 do bloco).

Associa `fields` a o valor literal `'__all__'`.

### UsuarioAdmin — linhas 57 a 391

```python
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Define listagem, busca e organizacao dos campos de Usuario."""

    # UserAdmin foi criado pensando no usuario padrao. Estas atribuicoes dizem
    # a ele para usar os formularios e o model personalizados do Elo.
    add_form = UsuarioAdminCreationForm
    form = UsuarioAdminChangeForm
    model = Usuario

    # Colunas exibidas na lista principal de usuarios.
    list_display = (
        "email",
        "nome",
        "perfil",
        "tipo_sanguineo",
        "status_validacao",
        "is_active",
        "suspensa",
        "email_verificado",
        "is_staff",
    )

    # Filtros laterais e campos pesquisaveis no painel.
    list_filter = (
        "perfil",
        "tipo_sanguineo",
        "status_validacao",
        "is_active",
        "suspensa",
        "email_verificado",
        "is_staff",
    )

    search_fields = ("email", "nome", "cpf", "cnpj")
    ordering = ("nome",)

    actions = (
        "aprovar_hemocentros_selecionados",
        "recusar_hemocentros_selecionados",
        "solicitar_correcao_hemocentros_selecionados",
    )

    # Datas automaticas devem ser visualizadas, nao digitadas manualmente.
    readonly_fields = (
        "status_validacao",
        "last_login",
        "date_joined",
        "atualizado_em",
    )

    # fieldsets organiza a tela de EDICAO de uma conta existente.
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Dados da conta",
            {
                "fields": (
                    "nome",
                    "perfil",
                    "cpf",
                    "cnpj",
                    "telefone",
                    "data_nascimento",
                    "sexo",
                    "tipo_sanguineo",
                    "tipo_sanguineo_confirmado",
                    "cidade",
                    "estado",
                    "status_validacao",
                    "email_verificado",
                )
            },
        ),
        (
            "Permissoes internas do Django",
            {
                "fields": (
                    "is_active",
                    "suspensa",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Datas",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "atualizado_em",
                )
            },
        ),
    )

    # add_fieldsets organiza a tela de CRIACAO de uma conta no admin.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "nome",
                    "perfil",
                    "password1",
                    "password2",
                    "is_active",
                    "suspensa",
                    "is_staff",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        """Audita mudancas administrativas em perfil e permissoes."""

        campos_auditados = [
            "perfil",
            "is_active",
            "is_staff",
            "is_superuser",
            "email_verificado",
            "suspensa",
            "nome",
            "email",
            "cpf",
            "cnpj",
            "cidade",
            "estado",
            "data_nascimento",
            "tipo_sanguineo",
        ]

        alteracoes = (
            campos_sensiveis_alterados(obj, campos_auditados)
            if change
            else {}
        )

        super().save_model(request, obj, form, change)

        if alteracoes:
            # Alteracoes cadastrais guardam apenas nomes de campos, sem
            # duplicar CPF, nascimento ou outros dados pessoais na auditoria.
            permissoes = {campo: valor for campo, valor in alteracoes.items()
                          if campo in {"perfil", "is_active", "is_staff", "is_superuser", "email_verificado", "suspensa"}}
            suspensao = (
                "is_active" in permissoes and not obj.is_active
            ) or ("suspensa" in permissoes and obj.suspensa)
            registrar_auditoria(
                acao=(AuditoriaAcaoCritica.Acao.ALTERACAO_PERMISSAO if permissoes
                      else AuditoriaAcaoCritica.Acao.MODERACAO),
                usuario=request.user,
                alvo=obj,
                descricao="Desativacao administrativa de usuario." if suspensao
                else "Alteracao administrativa de usuario.",
                request=request,
                metadados={"evento": "SUSPENSAO_USUARIO" if suspensao else "ALTERACAO_ADMINISTRATIVA",
                           "alteracoes": permissoes, "campos_alterados": sorted(alteracoes)},
            )
        elif not change:
            registrar_auditoria(
                acao=AuditoriaAcaoCritica.Acao.MODERACAO,
                usuario=request.user, alvo=obj, request=request,
                descricao="Criacao administrativa de usuario.",
                metadados={"evento": "ALTERACAO_ADMINISTRATIVA", "operacao": "CRIACAO_USUARIO"},
            )

    def _executar_acao_validacao(
        self,
        request,
        queryset,
        funcao,
        parecer,
    ):
        """Aplica uma decisao de validacao aos Hemocentros selecionados."""

        hemocentros = queryset.filter(
            perfil=Usuario.Perfil.HEMOCENTRO
        )

        ignorados = queryset.exclude(
            perfil=Usuario.Perfil.HEMOCENTRO
        ).count()

        total = 0

        for hemocentro in hemocentros:
            funcao(
                hemocentro=hemocentro,
                admin=request.user,
                parecer=parecer,
                request=request,
            )
            total += 1

        if total:
            self.message_user(
                request,
                f"{total} Hemocentro(s) atualizado(s) com sucesso.",
                level=messages.SUCCESS,
            )

        if ignorados:
            self.message_user(
                request,
                f"{ignorados} usuario(s) ignorado(s) por nao serem Hemocentros.",
                level=messages.WARNING,
            )

    @admin.action(description="Aprovar Hemocentros selecionados")
    def aprovar_hemocentros_selecionados(self, request, queryset):
        """Acao em lote que aprova Hemocentros e registra historico."""

        self._executar_acao_validacao(
            request,
            queryset,
            aprovar_hemocentro,
            "Hemocentro aprovado pelo painel administrativo.",
        )

    @admin.action(description="Recusar Hemocentros selecionados")
    def recusar_hemocentros_selecionados(self, request, queryset):
        """Acao em lote que recusa Hemocentros e registra historico."""

        self._executar_acao_validacao(
            request,
            queryset,
            recusar_hemocentro,
            "Hemocentro recusado pelo painel administrativo.",
        )

    @admin.action(
        description="Solicitar correcao dos Hemocentros selecionados"
    )
    def solicitar_correcao_hemocentros_selecionados(
        self,
        request,
        queryset,
    ):
        """Acao em lote que solicita correcao cadastral e registra historico."""

        self._executar_acao_validacao(
            request,
            queryset,
            solicitar_correcao_hemocentro,
            "Correcao cadastral solicitada pelo painel administrativo.",
        )

    def save_related(self, request, form, formsets, change):
        """Audita mudancas em grupos e permissoes diretas do usuario."""

        obj = form.instance

        grupos_antes = set()
        permissoes_antes = set()

        if change and obj.pk:
            usuario_atual = Usuario.objects.get(pk=obj.pk)

            grupos_antes = set(
                usuario_atual.groups.values_list(
                    "name",
                    flat=True,
                )
            )

            permissoes_antes = set(
                usuario_atual.user_permissions.values_list(
                    "codename",
                    flat=True,
                )
            )

        super().save_related(
            request,
            form,
            formsets,
            change,
        )

        if not change:
            return

        grupos_depois = set(
            obj.groups.values_list(
                "name",
                flat=True,
            )
        )

        permissoes_depois = set(
            obj.user_permissions.values_list(
                "codename",
                flat=True,
            )
        )

        alteracoes = {}

        if grupos_antes != grupos_depois:
            alteracoes["groups"] = {
                "antes": sorted(grupos_antes),
                "depois": sorted(grupos_depois),
            }

        if permissoes_antes != permissoes_depois:
            alteracoes["user_permissions"] = {
                "antes": sorted(permissoes_antes),
                "depois": sorted(permissoes_depois),
            }

        if alteracoes:
            registrar_auditoria(
                acao=AuditoriaAcaoCritica.Acao.ALTERACAO_PERMISSAO,
                usuario=request.user,
                alvo=obj,
                descricao="Alteracao administrativa de grupos ou permissoes.",
                request=request,
                metadados={"evento": "ALTERACAO_PERMISSAO", "alteracoes": alteracoes},
            )
```

**Explicação deste trecho:**

**Linha 58 — ClassDef** (nível 0 do bloco).

Define a classe `UsuarioAdmin` herdando de `UserAdmin`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 58:

**Linha 59 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 63 — Assign** (nível 1 do bloco).

Associa `add_form` a o valor associado ao nome `UsuarioAdminCreationForm`.

**Linha 64 — Assign** (nível 1 do bloco).

Associa `form` a o valor associado ao nome `UsuarioAdminChangeForm`.

**Linha 65 — Assign** (nível 1 do bloco).

Associa `model` a o valor associado ao nome `Usuario`.

**Linha 68 — Assign** (nível 1 do bloco).

Associa `list_display` a uma coleção Tuple com 9 itens, na expressão `('email', 'nome', 'perfil', 'tipo_sanguineo', 'status_validacao', 'is_active', 'suspensa', 'email_verificado', 'is_staff')`.

**Linha 81 — Assign** (nível 1 do bloco).

Associa `list_filter` a uma coleção Tuple com 7 itens, na expressão `('perfil', 'tipo_sanguineo', 'status_validacao', 'is_active', 'suspensa', 'email_verificado', 'is_staff')`.

**Linha 91 — Assign** (nível 1 do bloco).

Associa `search_fields` a uma coleção Tuple com 4 itens, na expressão `('email', 'nome', 'cpf', 'cnpj')`.

**Linha 92 — Assign** (nível 1 do bloco).

Associa `ordering` a uma coleção Tuple com 1 itens, na expressão `('nome',)`.

**Linha 94 — Assign** (nível 1 do bloco).

Associa `actions` a uma coleção Tuple com 3 itens, na expressão `('aprovar_hemocentros_selecionados', 'recusar_hemocentros_selecionados', 'solicitar_correcao_hemocentros_selecionados')`.

**Linha 101 — Assign** (nível 1 do bloco).

Associa `readonly_fields` a uma coleção Tuple com 4 itens, na expressão `('status_validacao', 'last_login', 'date_joined', 'atualizado_em')`.

**Linha 109 — Assign** (nível 1 do bloco).

Associa `fieldsets` a uma coleção Tuple com 4 itens, na expressão `((None, {'fields': ('email', 'password')}), ('Dados da conta', {'fields': ('nome', 'perfil', 'cpf', 'cnpj', 'telefone', 'data_nascimento', 'sexo', 'tipo_sanguineo', 'tipo_sanguineo_confirmado', 'cidade', 'estado', 'status_validacao', 'email_verificado')}), ('Permissoes internas do Django', {'fields': ('is_active', 'suspensa', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), ('Datas', {'fields': ('last_login', 'date_joined', 'atualizado_em')}))`.

**Linha 165 — Assign** (nível 1 do bloco).

Associa `add_fieldsets` a uma coleção Tuple com 1 itens, na expressão `((None, {'classes': ('wide',), 'fields': ('email', 'nome', 'perfil', 'password1', 'password2', 'is_active', 'suspensa', 'is_staff')}),)`.

**Linha 184 — FunctionDef** (nível 1 do bloco).

Define `save_model(self, request, obj, form, change)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 184:

**Linha 185 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 187 — Assign** (nível 2 do bloco).

Associa `campos_auditados` a uma coleção List com 14 itens, na expressão `['perfil', 'is_active', 'is_staff', 'is_superuser', 'email_verificado', 'suspensa', 'nome', 'email', 'cpf', 'cnpj', 'cidade', 'estado', 'data_nascimento', 'tipo_sanguineo']`.

**Linha 204 — Assign** (nível 2 do bloco).

Associa `alteracoes` a `campos_sensiveis_alterados(obj, campos_auditados)` se `change` for verdadeiro; caso contrário, `{}`.

**Linha 210 — Expr** (nível 2 do bloco).

Executa a chamada `super().save_model`; argumentos posicionais: `request`, `obj`, `form`, `change`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 212 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `alteracoes`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 212:

**Linha 215 — Assign** (nível 3 do bloco).

Associa `permissoes` a uma coleção/gerador construído por compreensão em `{campo: valor for campo, valor in alteracoes.items() if campo in {'perfil', 'is_active', 'is_staff', 'is_superuser', 'email_verificado', 'suspensa'}}`: percorre as fontes e aplica os filtros declarados.

**Linha 217 — Assign** (nível 3 do bloco).

Associa `suspensao` a pelo menos uma das condições: `'is_active' in permissoes and (not obj.is_active)` ; `'suspensa' in permissoes and obj.suspensa` (com avaliação interrompida assim que o resultado é determinado).

**Linha 220 — Expr** (nível 3 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.ALTERACAO_PERMISSAO if permissoes else AuditoriaAcaoCritica.Acao.MODERACAO`, `usuario=request.user`, `alvo=obj`, `descricao='Desativacao administrativa de usuario.' if suspensao else 'Alteracao administrativa de usuario.'`, `request=request`, `metadados={'evento': 'SUSPENSAO_USUARIO' if suspensao else 'ALTERACAO_ADMINISTRATIVA', 'alteracoes': permissoes, 'campos_alterados': sorted(alteracoes)}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 212:

**Linha 231 — If** (nível 3 do bloco).

Escolhe um caminho verificando a negação de `change`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 231:

**Linha 232 — Expr** (nível 4 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.MODERACAO`, `usuario=request.user`, `alvo=obj`, `request=request`, `descricao='Criacao administrativa de usuario.'`, `metadados={'evento': 'ALTERACAO_ADMINISTRATIVA', 'operacao': 'CRIACAO_USUARIO'}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 239 — FunctionDef** (nível 1 do bloco).

Define `_executar_acao_validacao(self, request, queryset, funcao, parecer)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 239:

**Linha 246 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 248 — Assign** (nível 2 do bloco).

Associa `hemocentros` a a chamada `queryset.filter`, que restringe os resultados às condições informadas; não grava os registros; argumentos nomeados: `perfil=Usuario.Perfil.HEMOCENTRO`.

- `perfil=Usuario.Perfil.HEMOCENTRO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 252 — Assign** (nível 2 do bloco).

Associa `ignorados` a a chamada `queryset.exclude(perfil=Usuario.Perfil.HEMOCENTRO).count`, que conta os resultados.


**Linha 256 — Assign** (nível 2 do bloco).

Associa `total` a o valor literal `0`.

**Linha 258 — For** (nível 2 do bloco).

Percorre `hemocentros`; cada item é atribuído a `hemocentro` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 258:

**Linha 259 — Expr** (nível 3 do bloco).

Executa a chamada `funcao`; argumentos nomeados: `hemocentro=hemocentro`, `admin=request.user`, `parecer=parecer`, `request=request`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 265 — AugAssign** (nível 3 do bloco).

Atualiza `total` pelo operador da expressão `total += 1`. O valor anterior participa do cálculo.

**Linha 267 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `total`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 267:

**Linha 268 — Expr** (nível 3 do bloco).

Executa a chamada `self.message_user`; argumentos posicionais: `request`, `f'{total} Hemocentro(s) atualizado(s) com sucesso.'`; argumentos nomeados: `level=messages.SUCCESS`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 274 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `ignorados`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 274:

**Linha 275 — Expr** (nível 3 do bloco).

Executa a chamada `self.message_user`; argumentos posicionais: `request`, `f'{ignorados} usuario(s) ignorado(s) por nao serem Hemocentros.'`; argumentos nomeados: `level=messages.WARNING`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 282 — FunctionDef** (nível 1 do bloco).

Define `aprovar_hemocentros_selecionados(self, request, queryset)`. O corpo só executa quando a função/método é chamado. Decoradores: `admin.action(description='Aprovar Hemocentros selecionados')`.

Bloco `body` da linha 282:

**Linha 283 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 285 — Expr** (nível 2 do bloco).

Executa a chamada `self._executar_acao_validacao`; argumentos posicionais: `request`, `queryset`, `aprovar_hemocentro`, `'Hemocentro aprovado pelo painel administrativo.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 293 — FunctionDef** (nível 1 do bloco).

Define `recusar_hemocentros_selecionados(self, request, queryset)`. O corpo só executa quando a função/método é chamado. Decoradores: `admin.action(description='Recusar Hemocentros selecionados')`.

Bloco `body` da linha 293:

**Linha 294 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 296 — Expr** (nível 2 do bloco).

Executa a chamada `self._executar_acao_validacao`; argumentos posicionais: `request`, `queryset`, `recusar_hemocentro`, `'Hemocentro recusado pelo painel administrativo.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 306 — FunctionDef** (nível 1 do bloco).

Define `solicitar_correcao_hemocentros_selecionados(self, request, queryset)`. O corpo só executa quando a função/método é chamado. Decoradores: `admin.action(description='Solicitar correcao dos Hemocentros selecionados')`.

Bloco `body` da linha 306:

**Linha 311 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 313 — Expr** (nível 2 do bloco).

Executa a chamada `self._executar_acao_validacao`; argumentos posicionais: `request`, `queryset`, `solicitar_correcao_hemocentro`, `'Correcao cadastral solicitada pelo painel administrativo.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 320 — FunctionDef** (nível 1 do bloco).

Define `save_related(self, request, form, formsets, change)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 320:

**Linha 321 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 323 — Assign** (nível 2 do bloco).

Associa `obj` a o atributo `instance` de `form`.

**Linha 325 — Assign** (nível 2 do bloco).

Associa `grupos_antes` a a chamada `set`.


**Linha 326 — Assign** (nível 2 do bloco).

Associa `permissoes_antes` a a chamada `set`.


**Linha 328 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `change` ; `obj.pk` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 328:

**Linha 329 — Assign** (nível 3 do bloco).

Associa `usuario_atual` a a chamada `Usuario.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `pk=obj.pk`.

- `pk=obj.pk`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 331 — Assign** (nível 3 do bloco).

Associa `grupos_antes` a a chamada `set`; argumentos posicionais: `usuario_atual.groups.values_list('name', flat=True)`.


**Linha 338 — Assign** (nível 3 do bloco).

Associa `permissoes_antes` a a chamada `set`; argumentos posicionais: `usuario_atual.user_permissions.values_list('codename', flat=True)`.


**Linha 345 — Expr** (nível 2 do bloco).

Executa a chamada `super().save_related`; argumentos posicionais: `request`, `form`, `formsets`, `change`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 352 — If** (nível 2 do bloco).

Escolhe um caminho verificando a negação de `change`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 352:

**Linha 353 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve nenhum valor explícito (None) ao chamador.

**Linha 355 — Assign** (nível 2 do bloco).

Associa `grupos_depois` a a chamada `set`; argumentos posicionais: `obj.groups.values_list('name', flat=True)`.


**Linha 362 — Assign** (nível 2 do bloco).

Associa `permissoes_depois` a a chamada `set`; argumentos posicionais: `obj.user_permissions.values_list('codename', flat=True)`.


**Linha 369 — Assign** (nível 2 do bloco).

Associa `alteracoes` a um dicionário de 0 entradas; as chaves dão nome aos valores associados.


**Linha 371 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `grupos_antes` diferente de `grupos_depois`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 371:

**Linha 372 — Assign** (nível 3 do bloco).

Associa `alteracoes['groups']` a um dicionário de 2 entradas; as chaves dão nome aos valores associados.

- Chave `'antes'`: recebe a chamada `sorted`; argumentos posicionais: `grupos_antes`.
- Chave `'depois'`: recebe a chamada `sorted`; argumentos posicionais: `grupos_depois`.

**Linha 377 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `permissoes_antes` diferente de `permissoes_depois`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 377:

**Linha 378 — Assign** (nível 3 do bloco).

Associa `alteracoes['user_permissions']` a um dicionário de 2 entradas; as chaves dão nome aos valores associados.

- Chave `'antes'`: recebe a chamada `sorted`; argumentos posicionais: `permissoes_antes`.
- Chave `'depois'`: recebe a chamada `sorted`; argumentos posicionais: `permissoes_depois`.

**Linha 383 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `alteracoes`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 383:

**Linha 384 — Expr** (nível 3 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.ALTERACAO_PERMISSAO`, `usuario=request.user`, `alvo=obj`, `descricao='Alteracao administrativa de grupos ou permissoes.'`, `request=request`, `metadados={'evento': 'ALTERACAO_PERMISSAO', 'alteracoes': alteracoes}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

### ValidacaoHemocentroAdmin — linhas 394 a 449

```python
@admin.register(ValidacaoHemocentro)
class ValidacaoHemocentroAdmin(admin.ModelAdmin):
    """Consulta somente leitura do historico institucional de Hemocentros."""

    list_display = (
        "data_analise",
        "hemocentro",
        "status",
        "admin",
        "parecer_resumido",
    )

    list_filter = (
        "status",
        "data_analise",
    )

    search_fields = (
        "hemocentro__email",
        "hemocentro__nome",
        "hemocentro__cnpj",
        "admin__email",
        "admin__nome",
        "parecer",
    )

    readonly_fields = (
        "id_validacao",
        "hemocentro",
        "admin",
        "status",
        "parecer",
        "data_analise",
    )

    date_hierarchy = "data_analise"
    ordering = ("-data_analise",)

    def parecer_resumido(self, obj):
        """Mostra um trecho curto do parecer na listagem."""

        if len(obj.parecer) <= 80:
            return obj.parecer

        return f"{obj.parecer[:77]}..."

    parecer_resumido.short_description = "Parecer"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
```

**Explicação deste trecho:**

**Linha 395 — ClassDef** (nível 0 do bloco).

Define a classe `ValidacaoHemocentroAdmin` herdando de `admin.ModelAdmin`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 395:

**Linha 396 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 398 — Assign** (nível 1 do bloco).

Associa `list_display` a uma coleção Tuple com 5 itens, na expressão `('data_analise', 'hemocentro', 'status', 'admin', 'parecer_resumido')`.

**Linha 406 — Assign** (nível 1 do bloco).

Associa `list_filter` a uma coleção Tuple com 2 itens, na expressão `('status', 'data_analise')`.

**Linha 411 — Assign** (nível 1 do bloco).

Associa `search_fields` a uma coleção Tuple com 6 itens, na expressão `('hemocentro__email', 'hemocentro__nome', 'hemocentro__cnpj', 'admin__email', 'admin__nome', 'parecer')`.

**Linha 420 — Assign** (nível 1 do bloco).

Associa `readonly_fields` a uma coleção Tuple com 6 itens, na expressão `('id_validacao', 'hemocentro', 'admin', 'status', 'parecer', 'data_analise')`.

**Linha 429 — Assign** (nível 1 do bloco).

Associa `date_hierarchy` a o valor literal `'data_analise'`.

**Linha 430 — Assign** (nível 1 do bloco).

Associa `ordering` a uma coleção Tuple com 1 itens, na expressão `('-data_analise',)`.

**Linha 432 — FunctionDef** (nível 1 do bloco).

Define `parecer_resumido(self, obj)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 432:

**Linha 433 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 435 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `len(obj.parecer)` menor ou igual a `80`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 435:

**Linha 436 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve o atributo `parecer` de `obj` ao chamador.

**Linha 438 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o texto formatado `f'{obj.parecer[:77]}...'`, inserindo valores nas partes entre chaves ao chamador.

**Linha 440 — Assign** (nível 1 do bloco).

Associa `parecer_resumido.short_description` a o valor literal `'Parecer'`.

**Linha 442 — FunctionDef** (nível 1 do bloco).

Define `has_add_permission(self, request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 442:

**Linha 443 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 445 — FunctionDef** (nível 1 do bloco).

Define `has_change_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 445:

**Linha 446 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 448 — FunctionDef** (nível 1 do bloco).

Define `has_delete_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 448:

**Linha 449 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

### ConsentimentoLGPDAdmin — linhas 452 a 489

```python
@admin.register(ConsentimentoLGPD)
class ConsentimentoLGPDAdmin(admin.ModelAdmin):
    """Permite consultar os aceites LGPD no painel administrativo."""

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.MODERACAO,
            usuario=request.user, alvo=obj, request=request,
            descricao="Alteracao administrativa de consentimento." if change
            else "Criacao administrativa de consentimento.",
            metadados={"evento": "ALTERACAO_ADMINISTRATIVA",
                       "campos_alterados": list(form.changed_data)},
        )

    list_display = (
        "usuario",
        "tipo_termo",
        "versao_termo",
        "aceito",
        "data_aceite",
    )

    list_filter = (
        "tipo_termo",
        "aceito",
        "versao_termo",
    )

    search_fields = (
        "usuario__email",
        "usuario__nome",
    )

    # A data representa um evento real e nao deve ser alterada pelo formulario.
    readonly_fields = (
        "data_aceite",
    )
```

**Explicação deste trecho:**

**Linha 453 — ClassDef** (nível 0 do bloco).

Define a classe `ConsentimentoLGPDAdmin` herdando de `admin.ModelAdmin`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 453:

**Linha 454 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 456 — FunctionDef** (nível 1 do bloco).

Define `save_model(self, request, obj, form, change)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 456:

**Linha 457 — Expr** (nível 2 do bloco).

Executa a chamada `super().save_model`; argumentos posicionais: `request`, `obj`, `form`, `change`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 458 — Expr** (nível 2 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.MODERACAO`, `usuario=request.user`, `alvo=obj`, `request=request`, `descricao='Alteracao administrativa de consentimento.' if change else 'Criacao administrativa de consentimento.'`, `metadados={'evento': 'ALTERACAO_ADMINISTRATIVA', 'campos_alterados': list(form.changed_data)}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 467 — Assign** (nível 1 do bloco).

Associa `list_display` a uma coleção Tuple com 5 itens, na expressão `('usuario', 'tipo_termo', 'versao_termo', 'aceito', 'data_aceite')`.

**Linha 475 — Assign** (nível 1 do bloco).

Associa `list_filter` a uma coleção Tuple com 3 itens, na expressão `('tipo_termo', 'aceito', 'versao_termo')`.

**Linha 481 — Assign** (nível 1 do bloco).

Associa `search_fields` a uma coleção Tuple com 2 itens, na expressão `('usuario__email', 'usuario__nome')`.

**Linha 487 — Assign** (nível 1 do bloco).

Associa `readonly_fields` a uma coleção Tuple com 1 itens, na expressão `('data_aceite',)`.

### AuditoriaAcaoCriticaAdmin — linhas 492 a 555

```python
@admin.register(AuditoriaAcaoCritica)
class AuditoriaAcaoCriticaAdmin(admin.ModelAdmin):
    """Consulta somente leitura das acoes criticas registradas."""

    def has_view_permission(self, request, obj=None):
        return (
            request.user.perfil == Usuario.Perfil.ADMINISTRADOR
            and super().has_view_permission(request, obj)
        )

    def has_module_permission(self, request):
        return self.has_view_permission(request)

    list_display = (
        "criado_em",
        "acao",
        "resultado",
        "usuario",
        "alvo_tipo",
        "alvo_id",
        "ip",
    )

    list_filter = (
        "acao",
        "resultado",
        "criado_em",
    )

    search_fields = (
        "usuario__email",
        "usuario__nome",
        "descricao",
        "metadados",
        "alvo_tipo",
        "alvo_id",
        "ip",
    )

    readonly_fields = (
        "id_auditoria",
        "usuario",
        "acao",
        "resultado",
        "alvo_tipo",
        "alvo_id",
        "descricao",
        "ip",
        "user_agent",
        "metadados",
        "criado_em",
    )

    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
```

**Explicação deste trecho:**

**Linha 493 — ClassDef** (nível 0 do bloco).

Define a classe `AuditoriaAcaoCriticaAdmin` herdando de `admin.ModelAdmin`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 493:

**Linha 494 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 496 — FunctionDef** (nível 1 do bloco).

Define `has_view_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 496:

**Linha 497 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve todas as condições: `request.user.perfil == Usuario.Perfil.ADMINISTRADOR` ; `super().has_view_permission(request, obj)` (com avaliação interrompida assim que o resultado é determinado) ao chamador.

**Linha 502 — FunctionDef** (nível 1 do bloco).

Define `has_module_permission(self, request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 502:

**Linha 503 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `self.has_view_permission`; argumentos posicionais: `request` ao chamador.

**Linha 505 — Assign** (nível 1 do bloco).

Associa `list_display` a uma coleção Tuple com 7 itens, na expressão `('criado_em', 'acao', 'resultado', 'usuario', 'alvo_tipo', 'alvo_id', 'ip')`.

**Linha 515 — Assign** (nível 1 do bloco).

Associa `list_filter` a uma coleção Tuple com 3 itens, na expressão `('acao', 'resultado', 'criado_em')`.

**Linha 521 — Assign** (nível 1 do bloco).

Associa `search_fields` a uma coleção Tuple com 7 itens, na expressão `('usuario__email', 'usuario__nome', 'descricao', 'metadados', 'alvo_tipo', 'alvo_id', 'ip')`.

**Linha 531 — Assign** (nível 1 do bloco).

Associa `readonly_fields` a uma coleção Tuple com 11 itens, na expressão `('id_auditoria', 'usuario', 'acao', 'resultado', 'alvo_tipo', 'alvo_id', 'descricao', 'ip', 'user_agent', 'metadados', 'criado_em')`.

**Linha 545 — Assign** (nível 1 do bloco).

Associa `date_hierarchy` a o valor literal `'criado_em'`.

**Linha 546 — Assign** (nível 1 do bloco).

Associa `ordering` a uma coleção Tuple com 1 itens, na expressão `('-criado_em',)`.

**Linha 548 — FunctionDef** (nível 1 do bloco).

Define `has_add_permission(self, request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 548:

**Linha 549 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 551 — FunctionDef** (nível 1 do bloco).

Define `has_change_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 551:

**Linha 552 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 554 — FunctionDef** (nível 1 do bloco).

Define `has_delete_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 554:

**Linha 555 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

### EstoqueAdmin — linhas 558 a 596

```python
@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    """
    Consulta administrativa do estoque de cada Hemocentro.

    status_calculado e data_atualizacao ficam somente leitura porque sao
    derivados automaticamente pela camada de servico (accounts/estoque.py)
    sempre que a quantidade de bolsas muda.
    """

    list_display = (
        "hemocentro",
        "tipo_sanguineo",
        "quantidade_bolsas",
        "nivel_minimo",
        "nivel_critico",
        "status_calculado",
        "data_atualizacao",
    )

    list_filter = (
        "status_calculado",
        "tipo_sanguineo",
    )

    search_fields = (
        "hemocentro__email",
        "hemocentro__nome",
    )

    ordering = (
        "hemocentro__nome",
        "tipo_sanguineo",
    )

    readonly_fields = (
        "status_calculado",
        "data_atualizacao",
    )
```

**Explicação deste trecho:**

**Linha 559 — ClassDef** (nível 0 do bloco).

Define a classe `EstoqueAdmin` herdando de `admin.ModelAdmin`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 559:

**Linha 560 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 568 — Assign** (nível 1 do bloco).

Associa `list_display` a uma coleção Tuple com 7 itens, na expressão `('hemocentro', 'tipo_sanguineo', 'quantidade_bolsas', 'nivel_minimo', 'nivel_critico', 'status_calculado', 'data_atualizacao')`.

**Linha 578 — Assign** (nível 1 do bloco).

Associa `list_filter` a uma coleção Tuple com 2 itens, na expressão `('status_calculado', 'tipo_sanguineo')`.

**Linha 583 — Assign** (nível 1 do bloco).

Associa `search_fields` a uma coleção Tuple com 2 itens, na expressão `('hemocentro__email', 'hemocentro__nome')`.

**Linha 588 — Assign** (nível 1 do bloco).

Associa `ordering` a uma coleção Tuple com 2 itens, na expressão `('hemocentro__nome', 'tipo_sanguineo')`.

**Linha 593 — Assign** (nível 1 do bloco).

Associa `readonly_fields` a uma coleção Tuple com 2 itens, na expressão `('status_calculado', 'data_atualizacao')`.

### EstoqueMovimentacaoAdmin — linhas 599 a 655

```python
@admin.register(EstoqueMovimentacao)
class EstoqueMovimentacaoAdmin(admin.ModelAdmin):
    """
    Historico somente leitura das movimentacoes de estoque (UC_30).

    Assim como ValidacaoHemocentroAdmin, este historico nunca deve ser
    criado, editado ou apagado pelo admin: toda movimentacao precisa
    passar por registrar_movimentacao_estoque para manter a quantidade
    de bolsas e a auditoria consistentes.
    """

    list_display = (
        "data_hora",
        "estoque",
        "tipo_movimento",
        "quantidade_anterior",
        "quantidade_movimentada",
        "quantidade_nova",
        "usuario_resp",
    )

    list_filter = (
        "tipo_movimento",
        "data_hora",
    )

    search_fields = (
        "estoque__hemocentro__email",
        "estoque__hemocentro__nome",
        "usuario_resp__email",
        "usuario_resp__nome",
        "motivo",
    )

    readonly_fields = (
        "id_mov",
        "estoque",
        "usuario_resp",
        "tipo_movimento",
        "quantidade_anterior",
        "quantidade_movimentada",
        "quantidade_nova",
        "motivo",
        "data_hora",
    )

    date_hierarchy = "data_hora"
    ordering = ("-data_hora",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
```

**Explicação deste trecho:**

**Linha 600 — ClassDef** (nível 0 do bloco).

Define a classe `EstoqueMovimentacaoAdmin` herdando de `admin.ModelAdmin`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 600:

**Linha 601 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 610 — Assign** (nível 1 do bloco).

Associa `list_display` a uma coleção Tuple com 7 itens, na expressão `('data_hora', 'estoque', 'tipo_movimento', 'quantidade_anterior', 'quantidade_movimentada', 'quantidade_nova', 'usuario_resp')`.

**Linha 620 — Assign** (nível 1 do bloco).

Associa `list_filter` a uma coleção Tuple com 2 itens, na expressão `('tipo_movimento', 'data_hora')`.

**Linha 625 — Assign** (nível 1 do bloco).

Associa `search_fields` a uma coleção Tuple com 5 itens, na expressão `('estoque__hemocentro__email', 'estoque__hemocentro__nome', 'usuario_resp__email', 'usuario_resp__nome', 'motivo')`.

**Linha 633 — Assign** (nível 1 do bloco).

Associa `readonly_fields` a uma coleção Tuple com 9 itens, na expressão `('id_mov', 'estoque', 'usuario_resp', 'tipo_movimento', 'quantidade_anterior', 'quantidade_movimentada', 'quantidade_nova', 'motivo', 'data_hora')`.

**Linha 645 — Assign** (nível 1 do bloco).

Associa `date_hierarchy` a o valor literal `'data_hora'`.

**Linha 646 — Assign** (nível 1 do bloco).

Associa `ordering` a uma coleção Tuple com 1 itens, na expressão `('-data_hora',)`.

**Linha 648 — FunctionDef** (nível 1 do bloco).

Define `has_add_permission(self, request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 648:

**Linha 649 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 651 — FunctionDef** (nível 1 do bloco).

Define `has_change_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 651:

**Linha 652 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 654 — FunctionDef** (nível 1 do bloco).

Define `has_delete_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 654:

**Linha 655 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

### TriagemAdmin — linhas 658 a 730

```python
@admin.register(Triagem)
class TriagemAdmin(admin.ModelAdmin):
    """
    Permite ao administrador consultar as triagens realizadas.

    Os dados ficam somente para consulta no painel administrativo.
    """

    # Colunas exibidas na listagem de triagens.
    list_display = (
        "id_triagem",
        "usuario",
        "modalidade",
        "status",
        "resultado",
        "regra_version",
        "data_liberacao",
        "iniciada_em",
        "finalizada_em",
    )

    # Filtros disponíveis no lado direito do admin.
    list_filter = (
        "modalidade",
        "status",
        "resultado",
        "regra_version",
        "iniciada_em",
    )

    # Campos usados na busca.
    search_fields = (
        "usuario__nome",
        "usuario__email",
        "regra_version",
    )

    # Impede alteração manual de resultados médicos.
    readonly_fields = (
        "id_triagem",
        "usuario",
        "modalidade",
        "status",
        "pergunta_atual",
        "fluxo_perguntas",
        "triagem_base",
        "regra_version",
        "resultado",
        "mensagem_resultado",
        "data_liberacao",
        "achados",
        "iniciada_em",
        "finalizada_em",
        "atualizada_em",
    )

    # Mostra a navegação por data.
    date_hierarchy = "iniciada_em"

    # Ordena as triagens mais recentes primeiro.
    ordering = ("-iniciada_em",)

    # Impede criação manual pelo administrador.
    def has_add_permission(self, request):
        return False

    # Impede alteração pelo administrador.
    def has_change_permission(self, request, obj=None):
        return False

    # Impede exclusão pelo administrador.
    def has_delete_permission(self, request, obj=None):
        return False
```

**Explicação deste trecho:**

**Linha 659 — ClassDef** (nível 0 do bloco).

Define a classe `TriagemAdmin` herdando de `admin.ModelAdmin`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 659:

**Linha 660 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 667 — Assign** (nível 1 do bloco).

Associa `list_display` a uma coleção Tuple com 9 itens, na expressão `('id_triagem', 'usuario', 'modalidade', 'status', 'resultado', 'regra_version', 'data_liberacao', 'iniciada_em', 'finalizada_em')`.

**Linha 680 — Assign** (nível 1 do bloco).

Associa `list_filter` a uma coleção Tuple com 5 itens, na expressão `('modalidade', 'status', 'resultado', 'regra_version', 'iniciada_em')`.

**Linha 689 — Assign** (nível 1 do bloco).

Associa `search_fields` a uma coleção Tuple com 3 itens, na expressão `('usuario__nome', 'usuario__email', 'regra_version')`.

**Linha 696 — Assign** (nível 1 do bloco).

Associa `readonly_fields` a uma coleção Tuple com 15 itens, na expressão `('id_triagem', 'usuario', 'modalidade', 'status', 'pergunta_atual', 'fluxo_perguntas', 'triagem_base', 'regra_version', 'resultado', 'mensagem_resultado', 'data_liberacao', 'achados', 'iniciada_em', 'finalizada_em', 'atualizada_em')`.

**Linha 715 — Assign** (nível 1 do bloco).

Associa `date_hierarchy` a o valor literal `'iniciada_em'`.

**Linha 718 — Assign** (nível 1 do bloco).

Associa `ordering` a uma coleção Tuple com 1 itens, na expressão `('-iniciada_em',)`.

**Linha 721 — FunctionDef** (nível 1 do bloco).

Define `has_add_permission(self, request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 721:

**Linha 722 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 725 — FunctionDef** (nível 1 do bloco).

Define `has_change_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 725:

**Linha 726 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 729 — FunctionDef** (nível 1 do bloco).

Define `has_delete_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 729:

**Linha 730 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

### RespostaTriagemAdmin — linhas 733 a 794

```python
@admin.register(RespostaTriagem)
class RespostaTriagemAdmin(admin.ModelAdmin):
    """
    Permite consultar as respostas individuais das triagens.
    """

    # Colunas exibidas na listagem.
    list_display = (
        "id_resposta",
        "triagem",
        "id_pergunta",
        "codigo_resposta",
        "resposta_label",
        "data_evento",
        "respondido_em",
    )

    # Filtros disponíveis.
    list_filter = (
        "id_pergunta",
        "rule_version",
        "respondido_em",
    )

    # Campos pesquisáveis.
    search_fields = (
        "triagem__usuario__nome",
        "triagem__usuario__email",
        "id_pergunta",
        "codigo_resposta",
        "resposta_label",
    )

    # Respostas não devem ser editadas manualmente.
    readonly_fields = (
        "id_resposta",
        "triagem",
        "id_pergunta",
        "codigo_resposta",
        "resposta_label",
        "data_evento",
        "metadata",
        "valor",
        "rule_version",
        "source_ref",
        "respondido_em",
    )

    # Ordena pelas respostas mais recentes.
    ordering = ("-respondido_em",)

    # Impede criação manual.
    def has_add_permission(self, request):
        return False

    # Impede alteração.
    def has_change_permission(self, request, obj=None):
        return False

    # Impede exclusão.
    def has_delete_permission(self, request, obj=None):
        return False
```

**Explicação deste trecho:**

**Linha 734 — ClassDef** (nível 0 do bloco).

Define a classe `RespostaTriagemAdmin` herdando de `admin.ModelAdmin`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 734:

**Linha 735 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 740 — Assign** (nível 1 do bloco).

Associa `list_display` a uma coleção Tuple com 7 itens, na expressão `('id_resposta', 'triagem', 'id_pergunta', 'codigo_resposta', 'resposta_label', 'data_evento', 'respondido_em')`.

**Linha 751 — Assign** (nível 1 do bloco).

Associa `list_filter` a uma coleção Tuple com 3 itens, na expressão `('id_pergunta', 'rule_version', 'respondido_em')`.

**Linha 758 — Assign** (nível 1 do bloco).

Associa `search_fields` a uma coleção Tuple com 5 itens, na expressão `('triagem__usuario__nome', 'triagem__usuario__email', 'id_pergunta', 'codigo_resposta', 'resposta_label')`.

**Linha 767 — Assign** (nível 1 do bloco).

Associa `readonly_fields` a uma coleção Tuple com 11 itens, na expressão `('id_resposta', 'triagem', 'id_pergunta', 'codigo_resposta', 'resposta_label', 'data_evento', 'metadata', 'valor', 'rule_version', 'source_ref', 'respondido_em')`.

**Linha 782 — Assign** (nível 1 do bloco).

Associa `ordering` a uma coleção Tuple com 1 itens, na expressão `('-respondido_em',)`.

**Linha 785 — FunctionDef** (nível 1 do bloco).

Define `has_add_permission(self, request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 785:

**Linha 786 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 789 — FunctionDef** (nível 1 do bloco).

Define `has_change_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 789:

**Linha 790 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 793 — FunctionDef** (nível 1 do bloco).

Define `has_delete_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 793:

**Linha 794 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

### NotificacaoAdmin — linhas 797 a 836

```python
@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    """Permite consultar os avisos internos enviados aos usuarios."""

    list_display = (
        "usuario",
        "tipo",
        "titulo",
        "lida",
        "criada_em",
    )

    list_filter = (
        "tipo",
        "lida",
        "criada_em",
    )

    search_fields = (
        "usuario__email",
        "usuario__nome",
        "titulo",
        "mensagem",
    )

    readonly_fields = (
        "criada_em",
        "lida_em",
    )

    ordering = ("-criada_em",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
```

**Explicação deste trecho:**

**Linha 798 — ClassDef** (nível 0 do bloco).

Define a classe `NotificacaoAdmin` herdando de `admin.ModelAdmin`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 798:

**Linha 799 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 801 — Assign** (nível 1 do bloco).

Associa `list_display` a uma coleção Tuple com 5 itens, na expressão `('usuario', 'tipo', 'titulo', 'lida', 'criada_em')`.

**Linha 809 — Assign** (nível 1 do bloco).

Associa `list_filter` a uma coleção Tuple com 3 itens, na expressão `('tipo', 'lida', 'criada_em')`.

**Linha 815 — Assign** (nível 1 do bloco).

Associa `search_fields` a uma coleção Tuple com 4 itens, na expressão `('usuario__email', 'usuario__nome', 'titulo', 'mensagem')`.

**Linha 822 — Assign** (nível 1 do bloco).

Associa `readonly_fields` a uma coleção Tuple com 2 itens, na expressão `('criada_em', 'lida_em')`.

**Linha 827 — Assign** (nível 1 do bloco).

Associa `ordering` a uma coleção Tuple com 1 itens, na expressão `('-criada_em',)`.

**Linha 829 — FunctionDef** (nível 1 do bloco).

Define `has_add_permission(self, request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 829:

**Linha 830 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 832 — FunctionDef** (nível 1 do bloco).

Define `has_change_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 832:

**Linha 833 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 835 — FunctionDef** (nível 1 do bloco).

Define `has_delete_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 835:

**Linha 836 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

### PedidoSangueAdmin — linhas 839 a 894

```python
@admin.register(PedidoSangue)
class PedidoSangueAdmin(admin.ModelAdmin):
    """
    Consulta administrativa dos pedidos de sangue.

    A validacao deve acontecer pela camada de servico e pelo painel de
    validacao, nao editando status manualmente no admin.
    """

    list_display = (
        "id_pedido",
        "titulo",
        "solicitante",
        "contato",
        "hemocentro_destino",
        "tipo_sanguineo",
        "urgencia",
        "cidade",
        "status",
        "data_criacao",
    )

    list_filter = (
        "status",
        "urgencia",
        "tipo_sanguineo",
        "data_criacao",
    )

    search_fields = (
        "titulo",
        "cidade",
        "solicitante__email",
        "solicitante__nome",
        "hemocentro_destino__email",
        "hemocentro_destino__nome",
    )

    readonly_fields = (
        "id_pedido",
        "status",
        "data_criacao",
        "atualizado_em",
    )

    date_hierarchy = "data_criacao"
    ordering = ("-data_criacao",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
```

**Explicação deste trecho:**

**Linha 840 — ClassDef** (nível 0 do bloco).

Define a classe `PedidoSangueAdmin` herdando de `admin.ModelAdmin`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 840:

**Linha 841 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 848 — Assign** (nível 1 do bloco).

Associa `list_display` a uma coleção Tuple com 10 itens, na expressão `('id_pedido', 'titulo', 'solicitante', 'contato', 'hemocentro_destino', 'tipo_sanguineo', 'urgencia', 'cidade', 'status', 'data_criacao')`.

**Linha 861 — Assign** (nível 1 do bloco).

Associa `list_filter` a uma coleção Tuple com 4 itens, na expressão `('status', 'urgencia', 'tipo_sanguineo', 'data_criacao')`.

**Linha 868 — Assign** (nível 1 do bloco).

Associa `search_fields` a uma coleção Tuple com 6 itens, na expressão `('titulo', 'cidade', 'solicitante__email', 'solicitante__nome', 'hemocentro_destino__email', 'hemocentro_destino__nome')`.

**Linha 877 — Assign** (nível 1 do bloco).

Associa `readonly_fields` a uma coleção Tuple com 4 itens, na expressão `('id_pedido', 'status', 'data_criacao', 'atualizado_em')`.

**Linha 884 — Assign** (nível 1 do bloco).

Associa `date_hierarchy` a o valor literal `'data_criacao'`.

**Linha 885 — Assign** (nível 1 do bloco).

Associa `ordering` a uma coleção Tuple com 1 itens, na expressão `('-data_criacao',)`.

**Linha 887 — FunctionDef** (nível 1 do bloco).

Define `has_add_permission(self, request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 887:

**Linha 888 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 890 — FunctionDef** (nível 1 do bloco).

Define `has_change_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 890:

**Linha 891 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 893 — FunctionDef** (nível 1 do bloco).

Define `has_delete_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 893:

**Linha 894 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

### ValidacaoPedidoAdmin — linhas 897 a 949

```python
@admin.register(ValidacaoPedido)
class ValidacaoPedidoAdmin(admin.ModelAdmin):
    """Historico somente leitura das validacoes de pedidos."""

    list_display = (
        "data_validacao",
        "pedido",
        "status_validacao",
        "moderador",
        "motivo_resumido",
    )

    list_filter = (
        "status_validacao",
        "data_validacao",
    )

    search_fields = (
        "pedido__titulo",
        "pedido__cidade",
        "moderador__email",
        "moderador__nome",
        "motivo",
    )

    readonly_fields = (
        "id_validacao",
        "pedido",
        "status_validacao",
        "motivo",
        "moderador",
        "data_validacao",
    )

    date_hierarchy = "data_validacao"
    ordering = ("-data_validacao",)

    def motivo_resumido(self, obj):
        if len(obj.motivo) <= 80:
            return obj.motivo

        return f"{obj.motivo[:77]}..."

    motivo_resumido.short_description = "Motivo"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
```

**Explicação deste trecho:**

**Linha 898 — ClassDef** (nível 0 do bloco).

Define a classe `ValidacaoPedidoAdmin` herdando de `admin.ModelAdmin`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 898:

**Linha 899 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 901 — Assign** (nível 1 do bloco).

Associa `list_display` a uma coleção Tuple com 5 itens, na expressão `('data_validacao', 'pedido', 'status_validacao', 'moderador', 'motivo_resumido')`.

**Linha 909 — Assign** (nível 1 do bloco).

Associa `list_filter` a uma coleção Tuple com 2 itens, na expressão `('status_validacao', 'data_validacao')`.

**Linha 914 — Assign** (nível 1 do bloco).

Associa `search_fields` a uma coleção Tuple com 5 itens, na expressão `('pedido__titulo', 'pedido__cidade', 'moderador__email', 'moderador__nome', 'motivo')`.

**Linha 922 — Assign** (nível 1 do bloco).

Associa `readonly_fields` a uma coleção Tuple com 6 itens, na expressão `('id_validacao', 'pedido', 'status_validacao', 'motivo', 'moderador', 'data_validacao')`.

**Linha 931 — Assign** (nível 1 do bloco).

Associa `date_hierarchy` a o valor literal `'data_validacao'`.

**Linha 932 — Assign** (nível 1 do bloco).

Associa `ordering` a uma coleção Tuple com 1 itens, na expressão `('-data_validacao',)`.

**Linha 934 — FunctionDef** (nível 1 do bloco).

Define `motivo_resumido(self, obj)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 934:

**Linha 935 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `len(obj.motivo)` menor ou igual a `80`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 935:

**Linha 936 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve o atributo `motivo` de `obj` ao chamador.

**Linha 938 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o texto formatado `f'{obj.motivo[:77]}...'`, inserindo valores nas partes entre chaves ao chamador.

**Linha 940 — Assign** (nível 1 do bloco).

Associa `motivo_resumido.short_description` a o valor literal `'Motivo'`.

**Linha 942 — FunctionDef** (nível 1 do bloco).

Define `has_add_permission(self, request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 942:

**Linha 943 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 945 — FunctionDef** (nível 1 do bloco).

Define `has_change_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 945:

**Linha 946 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 948 — FunctionDef** (nível 1 do bloco).

Define `has_delete_permission(self, request, obj=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 948:

**Linha 949 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 44: `# Estes sao os dados minimos pedidos na tela de criacao do admin.`
- Linha 45: `# Os outros dados podem ser completados depois na tela de edicao.`
- Linha 61: `# UserAdmin foi criado pensando no usuario padrao. Estas atribuicoes dizem`
- Linha 62: `# a ele para usar os formularios e o model personalizados do Elo.`
- Linha 67: `# Colunas exibidas na lista principal de usuarios.`
- Linha 80: `# Filtros laterais e campos pesquisaveis no painel.`
- Linha 100: `# Datas automaticas devem ser visualizadas, nao digitadas manualmente.`
- Linha 108: `# fieldsets organiza a tela de EDICAO de uma conta existente.`
- Linha 164: `# add_fieldsets organiza a tela de CRIACAO de uma conta no admin.`
- Linha 213: `# Alteracoes cadastrais guardam apenas nomes de campos, sem`
- Linha 214: `# duplicar CPF, nascimento ou outros dados pessoais na auditoria.`
- Linha 486: `# A data representa um evento real e nao deve ser alterada pelo formulario.`
- Linha 666: `# Colunas exibidas na listagem de triagens.`
- Linha 679: `# Filtros disponíveis no lado direito do admin.`
- Linha 688: `# Campos usados na busca.`
- Linha 695: `# Impede alteração manual de resultados médicos.`
- Linha 714: `# Mostra a navegação por data.`
- Linha 717: `# Ordena as triagens mais recentes primeiro.`
- Linha 720: `# Impede criação manual pelo administrador.`
- Linha 724: `# Impede alteração pelo administrador.`
- Linha 728: `# Impede exclusão pelo administrador.`
- Linha 739: `# Colunas exibidas na listagem.`
- Linha 750: `# Filtros disponíveis.`
- Linha 757: `# Campos pesquisáveis.`
- Linha 766: `# Respostas não devem ser editadas manualmente.`
- Linha 781: `# Ordena pelas respostas mais recentes.`
- Linha 784: `# Impede criação manual.`
- Linha 788: `# Impede alteração.`
- Linha 792: `# Impede exclusão.`

