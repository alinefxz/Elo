"""
Formularios de cadastro e login do sistema Elo.

O formulario de cadastro:
- valida e-mail;
- valida CPF e CNPJ;
- exige CPF para Doador/Receptor;
- exige CNPJ para Hemocentro;
- exige data de nascimento para Doador/Receptor;
- valida senha;
- registra o aceite da LGPD por meio da view.
"""

import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Usuario

from datetime import date


def apenas_digitos(valor):
    """Retira todos os caracteres que nao sejam numeros."""
    return re.sub(r"\D", "", valor or "")


class CadastroUsuarioForm(UserCreationForm):
    """Formulario publico utilizado para criar contas."""

    cpf = forms.CharField(
        label="CPF",
        required=False,
        max_length=14,
        help_text="Obrigatorio para Doador e Receptor/Solicitante.",
        widget=forms.TextInput(
            attrs={
                "placeholder": "000.000.000-00",
                "autocomplete": "off",
                "inputmode": "numeric",
            }
        ),
    )

    cnpj = forms.CharField(
        label="CNPJ",
        required=False,
        max_length=18,
        help_text="Obrigatorio somente para Hemocentro.",
        widget=forms.TextInput(
            attrs={
                "placeholder": "00.000.000/0000-00",
                "autocomplete": "off",
                "inputmode": "numeric",
            }
        ),
    )

    perfil = forms.ChoiceField(
        label="Tipo de perfil",
        choices=[
            (Usuario.Perfil.DOADOR, "Doador"),
            (Usuario.Perfil.RECEPTOR, "Receptor / Solicitante"),
            (Usuario.Perfil.HEMOCENTRO, "Hemocentro"),
            (Usuario.Perfil.OBSERVADOR, "Observador"),
        ],
        help_text=(
            "Escolha Hemocentro somente para uma instituicao que sera "
            "analisada por um administrador."
        ),
        widget=forms.RadioSelect,
    )

    data_nascimento = forms.DateField(
        label="Data de nascimento",
        required=False,
        help_text="Obrigatoria para Doador e Receptor/Solicitante.",
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
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
            "telefone": "Telefone",
            "sexo": "Sexo",
            "cidade": "Cidade",
            "estado": "Estado (UF)",
        }

        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "autocomplete": "email",
                }
            ),
            "telefone": forms.TextInput(
                attrs={
                    "placeholder": "(00) 00000-0000",
                    "inputmode": "tel",
                }
            ),
            "estado": forms.TextInput(
                attrs={
                    "maxlength": 2,
                    "placeholder": "MG",
                    "style": "text-transform: uppercase;",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].label = "Senha"
        self.fields["password1"].help_text = (
            "Use no minimo 8 caracteres, incluindo letras e numeros."
        )

        self.fields["password2"].label = "Confirme a senha"

    def clean_nome(self):
        """Remove espacos desnecessarios do nome."""
        nome = (self.cleaned_data.get("nome") or "").strip()

        if not nome:
            raise forms.ValidationError("Informe o nome completo.")

        return nome

    def clean_email(self):
        """Padroniza o e-mail e verifica duplicidade."""
        email = (self.cleaned_data.get("email") or "").strip().lower()

        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Ja existe uma conta cadastrada com este e-mail."
            )

        return email

    def clean_cpf(self):
        """Limpa e valida o CPF."""
        cpf = apenas_digitos(self.cleaned_data.get("cpf"))

        if cpf and len(cpf) != 11:
            raise forms.ValidationError(
                "O CPF deve conter exatamente 11 numeros."
            )

        if cpf and Usuario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError(
                "Este CPF ja esta cadastrado."
            )

        return cpf or None

    def clean_cnpj(self):
        """Limpa e valida o CNPJ."""
        cnpj = apenas_digitos(self.cleaned_data.get("cnpj"))

        if cnpj and len(cnpj) != 14:
            raise forms.ValidationError(
                "O CNPJ deve conter exatamente 14 numeros."
            )

        if cnpj and Usuario.objects.filter(cnpj=cnpj).exists():
            raise forms.ValidationError(
                "Este CNPJ ja esta cadastrado."
            )

        return cnpj or None

    def clean_estado(self):
        """Padroniza a UF."""
        estado = (self.cleaned_data.get("estado") or "").strip().upper()

        if estado and len(estado) != 2:
            raise forms.ValidationError(
                "Informe a UF com 2 letras, por exemplo: MG."
            )

        return estado

    def clean_password1(self):
        """Valida a senha."""
        senha = self.cleaned_data.get("password1", "")

        if not senha:
            return senha

        possui_letra = bool(re.search(r"[A-Za-z]", senha))
        possui_numero = bool(re.search(r"\d", senha))

        if len(senha) < 8:
            raise forms.ValidationError(
                "A senha deve possuir pelo menos 8 caracteres."
            )

        if not possui_letra or not possui_numero:
            raise forms.ValidationError(
                "A senha precisa conter pelo menos uma letra e um numero."
            )

        return senha

    def clean(self):
        """
        Faz as validacoes que dependem do tipo de perfil.

        Regras:
        - Hemocentro -> CNPJ obrigatorio.
        - Doador/Receptor -> CPF e data de nascimento obrigatorios.
        - Observador -> pode ficar sem CPF/CNPJ.
        """
        dados = super().clean()

        perfil = dados.get("perfil")
        cpf = dados.get("cpf")
        cnpj = dados.get("cnpj")
        data_nascimento = dados.get("data_nascimento")

        perfis_pessoa = (
            Usuario.Perfil.DOADOR,
            Usuario.Perfil.RECEPTOR,
        )

        if perfil == Usuario.Perfil.HEMOCENTRO:
            if not cnpj:
                self.add_error(
                    "cnpj",
                    "Informe o CNPJ do hemocentro.",
                )

        if perfil in perfis_pessoa:
            if not cpf:
                self.add_error(
                    "cpf",
                    "Informe o CPF para este tipo de perfil.",
                )

            if not data_nascimento:
                self.add_error(
                    "data_nascimento",
                    "Informe a data de nascimento para este tipo de perfil.",
                )

        return dados


class LoginUsuarioForm(AuthenticationForm):
    """Formulario de login usando e-mail."""

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
            attrs={
                "autocomplete": "current-password",
            }
        ),
    )

class TriagemExtensaForm(forms.Form):
    """
    Formulário inicial da triagem extensa.

    Esta primeira etapa utiliza as perguntas EXT-01 até EXT-05B
    da especificação.
    """

    entende_orientacao = forms.ChoiceField(
        label=(
            "Você entende que esta triagem é apenas uma orientação "
            "e que a decisão final será feita pela equipe do hemocentro?"
        ),
        choices=[
            ("SIM", "Sim, entendo e quero continuar."),
            ("NAO", "Não entendi ou quero receber a explicação novamente."),
        ],
        widget=forms.RadioSelect,
    )

    idade = forms.ChoiceField(
        label="Qual é a sua idade hoje?",
        choices=[
            ("MENOS_16", "Menos de 16 anos"),
            ("16_17", "16 ou 17 anos"),
            ("18_60", "18 a 60 anos"),
            ("61_69", "61 a 69 anos"),
            ("70_MAIS", "70 anos ou mais"),
        ],
        widget=forms.RadioSelect,
    )

    peso = forms.ChoiceField(
        label="Quanto você pesa aproximadamente?",
        choices=[
            ("MENOS_50", "Menos de 50 kg"),
            ("50_55_9", "De 50 a 55,9 kg"),
            ("56_129_9", "De 56 a 129,9 kg"),
            ("130_MAIS", "130 kg ou mais"),
            ("NAO_SEI", "Não sei meu peso atual"),
        ],
        widget=forms.RadioSelect,
    )

    sexo_biologico = forms.ChoiceField(
        label="Qual opção corresponde ao seu sexo biológico?",
        choices=[
            ("FEMININO", "Feminino"),
            ("MASCULINO", "Masculino"),
            ("OUTRO", "Outra situação ou não sei qual regra se aplica"),
            ("NAO_INFORMAR", "Prefiro não informar"),
        ],
        widget=forms.RadioSelect,
    )

    ja_doou = forms.ChoiceField(
        label="Você já doou sangue alguma vez?",
        choices=[
            ("NAO", "Nunca doei"),
            ("SIM", "Sim, já doei"),
            ("NAO_LEMBRO", "Não tenho certeza ou não lembro"),
        ],
        widget=forms.RadioSelect,
    )

    data_ultima_doacao = forms.DateField(
        label="Qual foi a data da sua última doação de sangue total?",
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )

    doacoes_12_meses = forms.ChoiceField(
        label="Quantas doações de sangue total você fez nos últimos 12 meses?",
        required=False,
        choices=[
            ("0", "Nenhuma"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4_MAIS", "4 ou mais"),
            ("NAO_LEMBRO", "Não lembro"),
        ],
        widget=forms.RadioSelect,
    )

    def clean(self):
        """
        Exige data e quantidade de doações quando o usuário
        informa que já doou sangue.
        """

        dados = super().clean()

        ja_doou = dados.get("ja_doou")
        data_ultima_doacao = dados.get("data_ultima_doacao")
        doacoes_12_meses = dados.get("doacoes_12_meses")

        if ja_doou == "SIM" and not data_ultima_doacao:
            self.add_error(
                "data_ultima_doacao",
                "Informe a data da última doação.",
            )

        if ja_doou == "SIM" and not doacoes_12_meses:
            self.add_error(
                "doacoes_12_meses",
                "Informe a quantidade de doações.",
            )

        if data_ultima_doacao and data_ultima_doacao > date.today():
            self.add_error(
                "data_ultima_doacao",
                "A data da última doação não pode estar no futuro.",
            )

        return dados