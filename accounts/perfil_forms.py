"""Edição da própria conta com campos permitidos pelo papel já cadastrado."""

import re

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.utils import timezone
from django.urls import reverse_lazy

from .localidades import CidadeSugeridaInput, ESTADOS, validar_localidade
from .models import Usuario


class PerfilUsuarioForm(forms.ModelForm):
    """A instância vem da sessão, nunca de um identificador enviado pelo cliente.

    Documentos, papel, validação institucional e permissões não são campos do
    formulário. A gravação parcial também preserva alterações concorrentes
    nesses atributos e nos campos que a pessoa não editou.
    """

    estado = forms.ChoiceField(
        label="Estado (UF)",
        required=False,
        choices=[("", "Selecione o estado")]
        + [(uf, f"{nome} ({uf})") for uf, nome in ESTADOS],
    )

    CAMPOS_PESSOA = (
        "nome", "email", "telefone", "data_nascimento", "sexo", "estado", "cidade",
    )
    CAMPOS_INSTITUICAO = (
        "nome", "email", "telefone", "estado", "cidade", "endereco", "horario_funcionamento",
    )
    CAMPOS_ADMINISTRADOR = ("nome", "email", "telefone", "estado", "cidade")

    class Meta:
        model = Usuario
        fields = (
            "nome", "email", "telefone", "data_nascimento", "sexo", "estado",
            "cidade", "tipo_sanguineo", "endereco", "horario_funcionamento",
        )
        labels = {
            "nome": "Nome completo",
            "email": "E-mail",
            "telefone": "Telefone",
            "data_nascimento": "Data de nascimento",
            "sexo": "Sexo",
            "cidade": "Município",
            "tipo_sanguineo": "Tipo sanguíneo",
            "endereco": "Endereço da instituição",
            "horario_funcionamento": "Horários de funcionamento",
        }
        widgets = {
            "nome": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "telefone": forms.TextInput(attrs={"type": "tel", "autocomplete": "tel"}),
            "data_nascimento": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "cidade": CidadeSugeridaInput(attrs={
                "autocomplete": "address-level2", "list": "cidades-perfil",
                "data-municipios-url": reverse_lazy("accounts:localidades_cidades"),
            }),
            "endereco": forms.TextInput(attrs={"autocomplete": "street-address"}),
            "horario_funcionamento": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, instance=None, **kwargs):
        if not isinstance(instance, Usuario) or instance._state.adding or not instance.is_authenticated:
            raise ValueError("Informe a conta autenticada já cadastrada para editar o perfil.")
        super().__init__(*args, instance=instance, **kwargs)
        if instance.perfil == Usuario.Perfil.HEMOCENTRO:
            campos = self.CAMPOS_INSTITUICAO
            self.fields["nome"].label = "Nome da instituição"
            self.fields["nome"].widget.attrs["autocomplete"] = "organization"
            self.fields["email"].label = "E-mail institucional"
            self.fields["telefone"].label = "Telefone institucional"
        elif instance.perfil == Usuario.Perfil.ADMINISTRADOR:
            campos = self.CAMPOS_ADMINISTRADOR
        else:
            campos = self.CAMPOS_PESSOA
            if instance.perfil in {Usuario.Perfil.DOADOR, Usuario.Perfil.RECEPTOR}:
                campos += ("tipo_sanguineo",)

        self.fields = {nome: self.fields[nome] for nome in campos}
        self._campos_permitidos = campos
        if "tipo_sanguineo" in self.fields:
            self.fields["tipo_sanguineo"].disabled = instance.tipo_sanguineo_confirmado
            self.fields["tipo_sanguineo"].help_text = (
                "Confirmado pelo hemocentro. Alterações devem ser solicitadas à instituição."
                if instance.tipo_sanguineo_confirmado
                else "Informação declarada, sujeita à confirmação pelo hemocentro."
            )
        self.fields["cidade"].help_text = "Selecione o estado e busque seu município nas sugestões do IBGE."
        if instance.estado and instance.estado not in dict(ESTADOS):
            # Dados antigos podem ser preservados sem exigir sua correção
            # durante uma alteração que não envolve a localização.
            self.fields["estado"].choices = [
                *self.fields["estado"].choices, (instance.estado, instance.estado),
            ]

    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()
        if not nome:
            raise forms.ValidationError("Informe o nome da conta.")
        return nome

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if Usuario.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Já existe uma conta cadastrada com este e-mail.")
        return email

    def clean_telefone(self):
        telefone = self.cleaned_data.get("telefone", "").strip()
        if telefone and (
            re.search(r"[^\d\s()+.\-]", telefone)
            or not 8 <= len(re.sub(r"\D", "", telefone)) <= 15
        ):
            raise forms.ValidationError("Informe um telefone com 8 a 15 números, incluindo o DDD.")
        return telefone

    def clean_data_nascimento(self):
        nascimento = self.cleaned_data.get("data_nascimento")
        if nascimento and nascimento > timezone.localdate():
            raise forms.ValidationError("A data de nascimento não pode estar no futuro.")
        return nascimento

    def clean(self):
        dados = super().clean()
        if {"estado", "cidade"} & set(self.changed_data):
            estado = dados.get("estado", "")
            cidade = dados.get("cidade", "").strip()
            if estado and estado not in dict(ESTADOS):
                self.add_error("estado", "Selecione um estado brasileiro válido.")
            if estado and not cidade:
                self.add_error("cidade", "Informe o município correspondente ao estado.")
            elif cidade and not estado:
                self.add_error("estado", "Selecione o estado do município informado.")
            elif estado and cidade:
                try:
                    validar_localidade(estado, cidade)
                except forms.ValidationError as erro:
                    self.add_error("cidade", erro)
        return dados

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if not commit:
            return usuario
        campos = [nome for nome in self.changed_data if nome in self._campos_permitidos]
        with transaction.atomic():
            atual = Usuario.objects.select_for_update().get(pk=usuario.pk)
            if "email" in campos and usuario.email != atual.email:
                # A verificação comprova o endereço anterior, não o novo.
                usuario.email_verificado = False
                campos.append("email_verificado")
            if "tipo_sanguineo" in campos and atual.tipo_sanguineo_confirmado:
                campos.remove("tipo_sanguineo")
                usuario.tipo_sanguineo = atual.tipo_sanguineo
            if campos:
                usuario.save(update_fields=[*campos, "atualizado_em"])
        return usuario


class AlterarSenhaForm(PasswordChangeForm):
    """Mantém os validadores do Django e a regra de senha usada no cadastro."""

    def clean_new_password1(self):
        senha = self.cleaned_data.get("new_password1", "")
        if senha and not (re.search(r"[A-Za-z]", senha) and re.search(r"\d", senha)):
            raise forms.ValidationError("A senha precisa conter pelo menos uma letra e um número.")
        return senha
