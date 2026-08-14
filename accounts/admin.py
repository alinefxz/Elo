from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import ConsentimentoLGPD, Usuario


class UsuarioAdminCreationForm(UserCreationForm):
    """Garante que senhas criadas pelo painel tambem sejam transformadas em hash."""

    class Meta:
        model = Usuario
        fields = ("email", "nome", "perfil")


class UsuarioAdminChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = "__all__"


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioAdminCreationForm
    form = UsuarioAdminChangeForm
    model = Usuario

    list_display = ("email", "nome", "perfil", "is_active", "email_verificado")
    list_filter = ("perfil", "is_active", "email_verificado", "is_staff")
    search_fields = ("email", "nome", "cpf", "cnpj")
    ordering = ("nome",)
    readonly_fields = ("last_login", "date_joined", "atualizado_em")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Dados pessoais",
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
                )
            },
        ),
        (
            "Permissoes",
            {
                "fields": (
                    "is_active",
                    "email_verificado",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Datas", {"fields": ("last_login", "date_joined", "atualizado_em")}),
    )
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


@admin.register(ConsentimentoLGPD)
class ConsentimentoLGPDAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tipo_termo", "versao_termo", "aceito", "data_aceite")
    list_filter = ("tipo_termo", "aceito", "versao_termo")
    search_fields = ("usuario__email", "usuario__nome")
    readonly_fields = ("data_aceite",)
