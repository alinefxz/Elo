"""
RESUMO DO ARQUIVO
=================
Este arquivo transforma os models em formularios HTML e valida o que a pessoa
digitou antes de qualquer gravacao no PostgreSQL.

``CadastroUsuarioForm`` cria uma conta comum com nome, e-mail, senha e aceite
LGPD. ``LoginUsuarioForm`` usa o formulario de autenticacao do Django, mas
apresenta o campo de identificacao como e-mail.

Validar no formulario melhora a mensagem mostrada ao usuario. As restricoes do
banco, como e-mail unico, continuam sendo uma segunda camada de protecao.
"""

import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Usuario


class CadastroUsuarioForm(UserCreationForm):
    """
    Formulario de criacao da conta comum.

    A heranca de UserCreationForm e importante porque ela cria os campos
    password1/password2, compara as senhas, executa os validadores configurados
    em settings.py e chama set_password ao salvar.
    """

    # Este campo pertence apenas ao formulario. Ele nao e uma coluna da tabela
    # usuarios; a view o usa para criar um ConsentimentoLGPD separado.
    aceite_lgpd = forms.BooleanField(
        label="Li e aceito os Termos de Uso e a Politica de Privacidade.",
        required=True,
    )

    class Meta:
        """Liga o formulario ao model Usuario e escolhe os campos visiveis."""

        model = Usuario
        fields = [
            "nome",
            "email",
            "password1",
            "password2",
            "aceite_lgpd",
        ]
        labels = {
            "nome": "Nome completo",
            "email": "E-mail",
        }
        widgets = {
            # autocomplete ajuda o navegador sem alterar a validacao do Django.
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
        }

    def __init__(self, *args, **kwargs):
        """Ajusta textos dos campos herdados quando o formulario e criado."""

        # O construtor da classe pai precisa criar os campos antes da alteracao.
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Senha"
        self.fields["password2"].label = "Confirme a senha"
        self.fields["password1"].help_text = (
            "Use no minimo 8 caracteres, incluindo letras e numeros."
        )

    def clean_email(self):
        """Normaliza o e-mail e mostra um erro amigavel se ele ja existir."""

        # cleaned_data contem somente campos que passaram pela validacao basica.
        email = self.cleaned_data["email"].strip().lower()

        # iexact faz uma comparacao sem diferenciar maiusculas e minusculas.
        # exists gera uma consulta eficiente que pergunta apenas se ha resultado.
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ja existe uma conta com este e-mail.")
        return email

    def clean_password1(self):
        """Exige pelo menos uma letra e um numero na senha."""

        senha = self.cleaned_data.get("password1", "")
        possui_letra = bool(re.search(r"[A-Za-z]", senha))
        possui_numero = bool(re.search(r"\d", senha))

        if senha and (not possui_letra or not possui_numero):
            raise forms.ValidationError("A senha precisa conter letras e numeros.")
        return senha


class LoginUsuarioForm(AuthenticationForm):
    """
    Formulario de login por e-mail.

    O nome interno continua sendo ``username`` porque AuthenticationForm envia
    esse parametro ao authenticate(). Como USERNAME_FIELD e ``email``, o
    backend do Django interpreta corretamente o valor como e-mail.
    """

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
