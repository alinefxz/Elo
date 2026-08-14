import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Usuario


def apenas_digitos(valor):
    """Remove pontos, tracos, barras e outros caracteres de CPF/CNPJ."""

    return re.sub(r"\D", "", valor or "")


class CadastroUsuarioForm(UserCreationForm):
    """Valida os dados e usa o mecanismo seguro de senhas do Django."""

    perfil = forms.ChoiceField(
        label="Tipo de perfil",
        choices=[
            (Usuario.Perfil.DOADOR, "Doador"),
            (Usuario.Perfil.RECEPTOR, "Receptor"),
            (Usuario.Perfil.HEMOCENTRO, "Hemocentro"),
            (Usuario.Perfil.OBSERVADOR, "Observador"),
        ],
    )
    data_nascimento = forms.DateField(
        label="Data de nascimento",
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    aceite_lgpd = forms.BooleanField(
        label="Li e aceito os Termos de Uso e a Politica de Privacidade.",
        required=True,
    )

    class Meta:
        model = Usuario
        fields = [
            "nome",
            "email",
            "perfil",
            "cpf",
            "cnpj",
            "telefone",
            "data_nascimento",
            "sexo",
            "cidade",
            "estado",
            "password1",
            "password2",
            "aceite_lgpd",
        ]
        labels = {
            "nome": "Nome completo",
            "email": "E-mail",
            "cpf": "CPF",
            "cnpj": "CNPJ",
            "telefone": "Telefone",
            "sexo": "Sexo",
            "cidade": "Cidade",
            "estado": "Estado (UF)",
        }
        widgets = {
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "telefone": forms.TextInput(attrs={"placeholder": "(00) 00000-0000"}),
            "cpf": forms.TextInput(attrs={"placeholder": "Somente 11 digitos"}),
            "cnpj": forms.TextInput(attrs={"placeholder": "Somente 14 digitos"}),
            "estado": forms.TextInput(attrs={"maxlength": 2, "placeholder": "SP"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Senha"
        self.fields["password2"].label = "Confirme a senha"
        self.fields["password1"].help_text = (
            "Use no minimo 8 caracteres, incluindo letras e numeros."
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ja existe uma conta com este e-mail.")
        return email

    def clean_cpf(self):
        cpf = apenas_digitos(self.cleaned_data.get("cpf"))
        if cpf and len(cpf) != 11:
            raise forms.ValidationError("O CPF deve ter 11 digitos.")
        if cpf and Usuario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF ja esta cadastrado.")
        return cpf or None

    def clean_cnpj(self):
        cnpj = apenas_digitos(self.cleaned_data.get("cnpj"))
        if cnpj and len(cnpj) != 14:
            raise forms.ValidationError("O CNPJ deve ter 14 digitos.")
        if cnpj and Usuario.objects.filter(cnpj=cnpj).exists():
            raise forms.ValidationError("Este CNPJ ja esta cadastrado.")
        return cnpj or None

    def clean_estado(self):
        return (self.cleaned_data.get("estado") or "").strip().upper()

    def clean_password1(self):
        senha = self.cleaned_data.get("password1", "")
        if senha and (not re.search(r"[A-Za-z]", senha) or not re.search(r"\d", senha)):
            raise forms.ValidationError("A senha precisa conter letras e numeros.")
        return senha

    def clean(self):
        dados = super().clean()
        perfil = dados.get("perfil")
        cpf = dados.get("cpf")
        cnpj = dados.get("cnpj")

        # Hemocentro usa CNPJ; os demais perfis publicos usam CPF.
        if perfil == Usuario.Perfil.HEMOCENTRO and not cnpj:
            self.add_error("cnpj", "Informe o CNPJ do hemocentro.")
        elif perfil and perfil != Usuario.Perfil.HEMOCENTRO and not cpf:
            self.add_error("cpf", "Informe o CPF para este tipo de perfil.")

        return dados


class LoginUsuarioForm(AuthenticationForm):
    """Adapta o formulario nativo para apresentar o login como e-mail."""

    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password"}
        ),
    )
