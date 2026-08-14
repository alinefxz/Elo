"""
RESUMO DO ARQUIVO
=================
Configura como Usuario e ConsentimentoLGPD aparecem no painel /admin/.

O admin e uma ferramenta interna para pessoas autorizadas. Ele nao substitui
as telas normais do sistema. Os formularios abaixo garantem que uma senha
criada no painel tambem seja transformada em hash.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import ConsentimentoLGPD, Usuario


class UsuarioAdminCreationForm(UserCreationForm):
    """Formulario usado quando o admin cria uma conta."""

    class Meta:
        model = Usuario
        fields = ("email", "nome")


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
        "is_active",
        "email_verificado",
        "is_staff",
    )

    # Filtros laterais e campos pesquisaveis no painel.
    list_filter = ("is_active", "email_verificado", "is_staff")
    search_fields = ("email", "nome")
    ordering = ("nome",)

    # Datas automaticas devem ser visualizadas, nao digitadas manualmente.
    readonly_fields = ("last_login", "date_joined", "atualizado_em")

    # fieldsets organiza a tela de EDICAO de uma conta existente.
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Dados da conta",
            {"fields": ("nome", "email_verificado")},
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
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
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
