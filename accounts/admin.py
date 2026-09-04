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
        "status_validacao",
        "is_active",
        "email_verificado",
        "is_staff",
    )

    # Filtros laterais e campos pesquisaveis no painel.
    list_filter = (
        "perfil",
        "status_validacao",
        "is_active",
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
        (None, {"fields": ("email", "password")}),
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
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Datas", {"fields": ("last_login", "date_joined", "atualizado_em")}),
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
        ]
        alteracoes = campos_sensiveis_alterados(obj, campos_auditados) if change else {}

        super().save_model(request, obj, form, change)

        if alteracoes:
            registrar_auditoria(
                acao=AuditoriaAcaoCritica.Acao.ALTERACAO_PERMISSAO,
                usuario=request.user,
                alvo=obj,
                descricao="Alteracao administrativa de perfil ou permissao.",
                request=request,
                metadados={"alteracoes": alteracoes},
            )

    def _executar_acao_validacao(self, request, queryset, funcao, parecer):
        """Aplica uma decisao de validacao aos Hemocentros selecionados."""

        hemocentros = queryset.filter(perfil=Usuario.Perfil.HEMOCENTRO)
        ignorados = queryset.exclude(perfil=Usuario.Perfil.HEMOCENTRO).count()
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

    @admin.action(description="Solicitar correcao dos Hemocentros selecionados")
    def solicitar_correcao_hemocentros_selecionados(self, request, queryset):
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
                usuario_atual.groups.values_list("name", flat=True)
            )
            permissoes_antes = set(
                usuario_atual.user_permissions.values_list("codename", flat=True)
            )

        super().save_related(request, form, formsets, change)

        if not change:
            return

        grupos_depois = set(obj.groups.values_list("name", flat=True))
        permissoes_depois = set(
            obj.user_permissions.values_list("codename", flat=True)
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
                metadados={"alteracoes": alteracoes},
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
    list_filter = ("status", "data_analise")
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

    list_display = (
        "usuario",
        "tipo_termo",
        "versao_termo",
        "aceito",
        "data_aceite",
    )
    list_filter = ("tipo_termo", "aceito", "versao_termo")
    search_fields = ("usuario__email", "usuario__nome")

    # A data representa um evento real e nao deve ser alterada pelo formulario.
    readonly_fields = ("data_aceite",)


@admin.register(AuditoriaAcaoCritica)
class AuditoriaAcaoCriticaAdmin(admin.ModelAdmin):
    """Consulta somente leitura das acoes criticas registradas."""

    list_display = (
        "criado_em",
        "acao",
        "resultado",
        "usuario",
        "alvo_tipo",
        "alvo_id",
        "ip",
    )
    list_filter = ("acao", "resultado", "criado_em")
    search_fields = (
        "usuario__email",
        "usuario__nome",
        "descricao",
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
    list_filter = ("status_calculado", "tipo_sanguineo")
    search_fields = ("hemocentro__email", "hemocentro__nome")
    ordering = ("hemocentro__nome", "tipo_sanguineo")
    readonly_fields = ("status_calculado", "data_atualizacao")


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
    list_filter = ("tipo_movimento", "data_hora")
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
