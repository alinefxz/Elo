"""
RESUMO DO ARQUIVO
=================
Este arquivo define os formularios de cadastro e login.

O cadastro recebe os campos completos, limpa CPF/CNPJ, verifica documentos
repetidos, exige o documento certo para cada tipo de perfil e valida a senha.
O login usa o recurso pronto do Django, adaptado para mostrar e-mail.

O formulario e a primeira camada de validacao, pois mostra erros claros na
tela. O model e o PostgreSQL continuam como camadas adicionais de protecao.
"""

import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Usuario


def apenas_digitos(valor):
    """Retira pontos, tracos, espacos e barras de CPF ou CNPJ."""

    # \D representa qualquer caractere que nao seja numero.
    return re.sub(r"\D", "", valor or "")


class CadastroUsuarioForm(UserCreationForm):
    """
    Formulario completo usado na pagina de cadastro.

    UserCreationForm ja sabe criar password1 e password2, comparar as duas,
    executar os validadores de settings.py e chamar set_password() ao salvar.
    O Elo reaproveita esse comportamento e acrescenta seus proprios campos.
    """

    # No banco o CPF ocupa 11 caracteres, mas na tela a pessoa pode digitar
    # pontos e traco. Por isso o formulario aceita ate 14 caracteres e o
    # metodo clean_cpf retira a pontuacao antes de o model receber o valor.
    cpf = forms.CharField(
        label="CPF",
        required=False,
        max_length=14,
        help_text="Obrigatorio para Doador, Receptor e Observador.",
        widget=forms.TextInput(attrs={"placeholder": "000.000.000-00"}),
    )

    # O mesmo raciocinio vale para o CNPJ: 14 numeros no banco e ate 18
    # caracteres quando digitado como 00.000.000/0000-00.
    cnpj = forms.CharField(
        label="CNPJ",
        required=False,
        max_length=18,
        help_text="Obrigatorio somente para Hemocentro.",
        widget=forms.TextInput(attrs={"placeholder": "00.000.000/0000-00"}),
    )

    # Administrador nao aparece no cadastro publico. Ele e criado pelo comando
    # createsuperuser ou por uma pessoa autorizada no painel interno.
    perfil = forms.ChoiceField(
        label="Tipo de perfil",
        choices=[
            (Usuario.Perfil.DOADOR, "Doador"),
            (Usuario.Perfil.RECEPTOR, "Receptor"),
            (Usuario.Perfil.HEMOCENTRO, "Hemocentro"),
            (Usuario.Perfil.OBSERVADOR, "Observador"),
        ],
    )

    # O navegador mostra um seletor de data por causa de type=date.
    data_nascimento = forms.DateField(
        label="Data de nascimento",
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    # Este campo e validado no formulario. A view cria uma linha separada na
    # tabela consentimentos_lgpd quando o cadastro for concluido.
    aceite_lgpd = forms.BooleanField(
        label="Li e aceito os Termos de Uso e a Politica de Privacidade.",
        required=True,
    )

    class Meta:
        # Informa qual model sera preenchido pelo formulario.
        model = Usuario

        # A ordem desta lista tambem define a ordem exibida por form.as_p.
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

        # Textos apresentados acima dos campos.
        labels = {
            "nome": "Nome completo",
            "email": "E-mail",
            "telefone": "Telefone",
            "sexo": "Sexo",
            "cidade": "Cidade",
            "estado": "Estado (UF)",
        }

        # Widgets controlam o tipo e pequenos comportamentos do input HTML.
        widgets = {
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "telefone": forms.TextInput(attrs={"placeholder": "(00) 00000-0000"}),
            "estado": forms.TextInput(attrs={"maxlength": 2, "placeholder": "SP"}),
        }

    def __init__(self, *args, **kwargs):
        """Ajusta os textos dos campos de senha herdados do Django."""

        # O formulario-pai precisa criar password1/password2 antes de podermos
        # alterar seus textos.
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Senha"
        self.fields["password2"].label = "Confirme a senha"
        self.fields["password1"].help_text = (
            "Use no minimo 8 caracteres, incluindo letras e numeros."
        )

    def clean_email(self):
        """Padroniza o e-mail e impede uma conta repetida."""

        email = self.cleaned_data["email"].strip().lower()

        # cleaned_data contem o valor que ja passou pela validacao de e-mail.
        # iexact ignora diferenca entre maiusculas e minusculas. exists() faz
        # uma consulta curta: pergunta somente se ja ha um resultado.
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ja existe uma conta com este e-mail.")
        return email

    def clean_cpf(self):
        """Mantem somente numeros e verifica tamanho e repeticao do CPF."""

        cpf = apenas_digitos(self.cleaned_data.get("cpf"))
        # Esta etapa valida formato e repeticao, mas ainda nao calcula os
        # digitos verificadores oficiais do CPF.
        if cpf and len(cpf) != 11:
            raise forms.ValidationError("O CPF deve ter 11 digitos.")
        if cpf and Usuario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF ja esta cadastrado.")
        return cpf or None

    def clean_cnpj(self):
        """Mantem somente numeros e verifica tamanho e repeticao do CNPJ."""

        cnpj = apenas_digitos(self.cleaned_data.get("cnpj"))
        # Assim como no CPF, a validacao completa dos digitos verificadores
        # pode ser acrescentada depois sem mudar a tabela.
        if cnpj and len(cnpj) != 14:
            raise forms.ValidationError("O CNPJ deve ter 14 digitos.")
        if cnpj and Usuario.objects.filter(cnpj=cnpj).exists():
            raise forms.ValidationError("Este CNPJ ja esta cadastrado.")
        return cnpj or None

    def clean_estado(self):
        """Transforma a sigla em maiusculas e retira espacos."""

        return (self.cleaned_data.get("estado") or "").strip().upper()

    def clean_password1(self):
        """Exige pelo menos uma letra e um numero."""

        senha = self.cleaned_data.get("password1", "")
        possui_letra = bool(re.search(r"[A-Za-z]", senha))
        possui_numero = bool(re.search(r"\d", senha))

        if senha and (not possui_letra or not possui_numero):
            raise forms.ValidationError("A senha precisa conter letras e numeros.")
        return senha

    def clean(self):
        """Aplica a regra que compara perfil, CPF e CNPJ."""

        # Os metodos clean_campo executam antes. Depois, este clean geral pode
        # comparar varios campos. O clean da classe pai tambem mantem as
        # validacoes de senha do Django.
        dados = super().clean()
        perfil = dados.get("perfil")
        cpf = dados.get("cpf")
        cnpj = dados.get("cnpj")

        # Esta e uma regra inicial e simples. As regras detalhadas de cada
        # perfil ainda serao criadas nas proximas etapas.
        if perfil == Usuario.Perfil.HEMOCENTRO and not cnpj:
            self.add_error("cnpj", "Informe o CNPJ do hemocentro.")
        elif perfil and perfil != Usuario.Perfil.HEMOCENTRO and not cpf:
            self.add_error("cpf", "Informe o CPF para este tipo de perfil.")

        return dados


class LoginUsuarioForm(AuthenticationForm):
    """Formulario pronto do Django adaptado para login por e-mail."""

    # O nome interno continua username porque AuthenticationForm espera esse
    # nome. USERNAME_FIELD="email" faz o Django tratar o valor como e-mail.
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
