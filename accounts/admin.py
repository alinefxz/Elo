"""
RESUMO DO ARQUIVO
=================
Configura como Usuario, ConsentimentoLGPD e auditorias aparecem no /admin/.

O admin e uma ferramenta interna para pessoas autorizadas. Ele nao substitui
as telas normais do sistema. Os formularios abaixo garantem que uma senha
criada no painel tambem seja transformada em hash.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .auditoria import campos_sensiveis_alterados, registrar_auditoria
from .models import AuditoriaAcaoCritica, ConsentimentoLGPD, Usuario


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
        "is_active",
        "email_verificado",
        "is_staff",
    )

    # Filtros laterais e campos pesquisaveis no painel.
    list_filter = ("perfil", "is_active", "email_verificado", "is_staff")
    search_fields = ("email", "nome", "cpf", "cnpj")
    ordering = ("nome",)

    # Datas automaticas devem ser visualizadas, nao digitadas manualmente.
    readonly_fields = ("last_login", "date_joined", "atualizado_em")

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
