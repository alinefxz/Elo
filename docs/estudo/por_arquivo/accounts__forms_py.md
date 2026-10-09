# accounts/forms.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Campos e validacoes de cadastro, login, estoque, pedidos e filtros.

**Arquivo original:** [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
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
from datetime import date

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .compatibilidade import TIPOS_SANGUINEOS
from .models import EstoqueMovimentacao, PedidoSangue, Usuario


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

    aceita_notificacoes_pedidos = forms.BooleanField(
        label="Autorizo alertas internos de estoque e pedidos compativeis (para Doadores).",
        required=False,
        initial=False,
        help_text="Opcional. Posso cancelar a autorizacao no meu painel.",
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
            "aceita_notificacoes_pedidos",
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
        if perfil != Usuario.Perfil.DOADOR:
            dados["aceita_notificacoes_pedidos"] = False
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
            if cpf:
                self.add_error(
                    "cpf",
                    "Hemocentro deve informar CNPJ, não CPF.",
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
            if cnpj:
                self.add_error(
                    "cnpj",
                    "Doador e Receptor devem informar CPF, não CNPJ.",
                )

        if perfil == Usuario.Perfil.OBSERVADOR and (cpf or cnpj):
            self.add_error(
                "cpf" if cpf else "cnpj",
                "Observador não precisa informar CPF ou CNPJ.",
            )

        return dados


class PreferenciaConvocacaoForm(forms.Form):
    aceita_convocacoes = forms.BooleanField(
        label="Autorizo receber alertas internos de estoque e pedidos compativeis.",
        required=False,
        help_text="Opcional. Desmarque para cancelar futuras convocacoes.",
    )


class LoginUsuarioForm(AuthenticationForm):
    """Formulario de login usando e-mail."""

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if getattr(user, "suspensa", False):
            raise forms.ValidationError(
                "Esta conta está suspensa. Procure o administrador.",
                code="inactive",
            )

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


class CadastrarEstoqueForm(forms.Form):
    """
    UC_29 - Formulario usado pelo Hemocentro para cadastrar a estrutura
    de estoque de um tipo sanguineo.

    A validacao de "ja existe estoque para este tipo" e de "hemocentro
    aprovado" fica na camada de servico (accounts/estoque.py), porque
    depende do usuario logado, que o form nao conhece sozinho.
    """

    tipo_sanguineo = forms.ChoiceField(
        label="Tipo sanguíneo",
        choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
    )

    quantidade_bolsas = forms.IntegerField(
        label="Quantidade atual de bolsas",
        min_value=0,
        initial=0,
        help_text="Quantidade de bolsas já disponíveis, se houver.",
    )

    nivel_minimo = forms.IntegerField(
        label="Nível mínimo",
        min_value=0,
        help_text=(
            "A partir de quantas bolsas o tipo passa a ser considerado baixo."
        ),
    )

    nivel_critico = forms.IntegerField(
        label="Nível crítico",
        min_value=0,
        help_text=(
            "A partir de quantas bolsas o tipo passa a ser considerado crítico."
        ),
    )

    def clean(self):
        """Garante que o nível crítico nunca seja maior que o mínimo."""

        dados = super().clean()

        nivel_minimo = dados.get("nivel_minimo")
        nivel_critico = dados.get("nivel_critico")

        if (
            nivel_minimo is not None
            and nivel_critico is not None
            and nivel_critico > nivel_minimo
        ):
            self.add_error(
                "nivel_critico",
                "O nível crítico deve ser menor ou igual ao nível mínimo.",
            )

        return dados


class MovimentarEstoqueForm(forms.Form):
    """
    Formulario usado pelo Hemocentro para registrar entrada,
    saída ou ajuste de bolsas em um estoque já cadastrado.
    """

    tipo_movimento = forms.ChoiceField(
        label="Tipo de movimentação",
        choices=EstoqueMovimentacao.TipoMovimento.choices,
        widget=forms.RadioSelect,
    )

    quantidade = forms.IntegerField(
        label="Quantidade",
        min_value=0,
        help_text=(
            "Para entrada/saída: quantidade a movimentar. "
            "Para ajuste: nova quantidade total de bolsas."
        ),
    )

    motivo = forms.CharField(
        label="Motivo",
        required=True,
        max_length=255,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=(
            "Obrigatório. Ex.: doação recebida, transfusão realizada, "
            "contagem física."
        ),
    )

    def clean(self):
        dados = super().clean()

        tipo_movimento = dados.get("tipo_movimento")
        quantidade = dados.get("quantidade")

        movimentos_positivos = (
            EstoqueMovimentacao.TipoMovimento.ENTRADA,
            EstoqueMovimentacao.TipoMovimento.SAIDA,
        )

        if (
            tipo_movimento in movimentos_positivos
            and quantidade is not None
            and quantidade <= 0
        ):
            self.add_error(
                "quantidade",
                "Informe uma quantidade maior que zero.",
            )

        return dados

class PedidoSangueForm(forms.ModelForm):
    """
    Formulário para solicitar a divulgação de uma necessidade.

    As validacoes mais sensiveis ficam em validacao_pedido.py.
    Aqui ficam as validacoes de formulario.
    """

    contato = forms.EmailField(
        label="E-mail de contato",
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "seuemail@exemplo.com",
            }
        ),
    )

    class Meta:
        model = PedidoSangue

        fields = [
            "nome_solicitante",
            "contato",
            "para_quem",
            "hemocentro_destino",
            "titulo",
            "tipo_sanguineo",
            "urgencia",
            "cidade",
            "nome_paciente",
            "descricao",
            "justificativa_urgencia",
            "informacoes_complementares",
        ]

        labels = {
            "para_quem": "Para quem e este pedido?",
            "nome_solicitante": "Nome ou identificação do solicitante",
            "contato": "E-mail de contato",
            "hemocentro_destino": "Hemocentro de destino",
            "titulo": "Titulo do pedido",
            "tipo_sanguineo": "Tipo sanguineo",
            "urgencia": "Urgencia",
            "cidade": "Cidade",
            "nome_paciente": "Nome da pessoa (opcional)",
            "descricao": "Descricao",
            "justificativa_urgencia": "Justificativa da urgencia",
            "informacoes_complementares": "Informações complementares",
        }

        widgets = {
            "para_quem": forms.RadioSelect,
            "tipo_sanguineo": forms.RadioSelect,
            "urgencia": forms.RadioSelect,
            "descricao": forms.Textarea(attrs={"rows": 5}),
            "justificativa_urgencia": forms.Textarea(attrs={"rows": 4}),
            "informacoes_complementares": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["hemocentro_destino"].queryset = (
            Usuario.objects
            .filter(
                perfil=Usuario.Perfil.HEMOCENTRO,
                status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO,
            )
            .order_by("nome")
        )

    def clean_nome_paciente(self):
        return (self.cleaned_data.get("nome_paciente") or "").strip()

    def clean_nome_solicitante(self):
        nome = (self.cleaned_data.get("nome_solicitante") or "").strip()
        if not nome:
            raise forms.ValidationError(
                "Informe o nome ou uma identificação do solicitante."
            )
        return nome

    def clean_contato(self):
        contato = (self.cleaned_data.get("contato") or "").strip()
        if not contato:
            raise forms.ValidationError("Informe um e-mail para retorno.")
        return contato.lower()

    def clean_descricao(self):
        descricao = (self.cleaned_data.get("descricao") or "").strip()

        if len(descricao) < 10:
            raise forms.ValidationError(
                "Descreva a necessidade com pelo menos 10 caracteres."
            )

        return descricao

    def clean(self):
        dados = super().clean()

        urgencia = dados.get("urgencia")
        justificativa = (
            dados.get("justificativa_urgencia") or ""
        ).strip()

        if urgencia in [
            PedidoSangue.Urgencia.ALTA,
            PedidoSangue.Urgencia.CRITICA,
        ]:
            if len(justificativa) < 20:
                self.add_error(
                    "justificativa_urgencia",
                    (
                        "Pedidos de urgencia alta ou critica precisam "
                        "de justificativa com pelo menos 20 caracteres."
                    ),
                )

        return dados


class FiltroPedidoSangueForm(forms.Form):
    """
    RF - Visualizar e filtrar pedidos.

    Filtros:

    - tipo sanguineo;
    - urgencia;
    - cidade;
    - hemocentro;
    - data.
    """

    tipo_sanguineo = forms.ChoiceField(
        label="Tipo sanguineo",
        required=False,
        choices=[
            ("", "Todos")
        ] + [(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
    )

    urgencia = forms.ChoiceField(
        label="Urgencia",
        required=False,
        choices=[("", "Todas")] + list(PedidoSangue.Urgencia.choices),
    )

    cidade = forms.CharField(
        label="Cidade",
        required=False,
    )

    hemocentro = forms.CharField(
        label="Hemocentro",
        required=False,
    )

    data = forms.DateField(
        label="Data",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    status = forms.ChoiceField(
        label="Status",
        required=False,
        choices=[("", "Todos")] + list(PedidoSangue.Status.choices),
    )


class FiltroEstoquePublicoForm(forms.Form):
    """Filtros da consulta pública de estoques.

    A situação usa os códigos calculados pelo sistema. Os níveis mínimo e
    crítico continuam ocultos, pois são parâmetros internos do Hemocentro.
    """

    tipo_sanguineo = forms.ChoiceField(
        label="Tipo sanguíneo",
        required=False,
        choices=[("", "Todos")] + [(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
    )

    cidade = forms.CharField(
        label="Cidade",
        required=False,
    )

    hemocentro = forms.CharField(
        label="Hemocentro",
        required=False,
    )

    situacao = forms.ChoiceField(
        label="Situação do estoque",
        required=False,
        choices=[
            ("", "Todas"),
            ("CRITICO", "Crítico"),
            ("BAIXO", "Baixo"),
            ("ADEQUADO", "Adequado"),
            ("ALTO", "Alto"),
        ],
    )

    busca = forms.CharField(
        label="Busca",
        required=False,
        help_text="Nome do Hemocentro, cidade, UF ou tipo sanguíneo.",
    )
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 13

```python
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
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### Import — linhas 15 a 15

```python
import re
```

**Explicação deste trecho:**

**Linha 15 — Import** (nível 0 do bloco).

Importa módulos: `re`.

### ImportFrom — linhas 16 a 16

```python
from datetime import date
```

**Explicação deste trecho:**

**Linha 16 — ImportFrom** (nível 0 do bloco).

Importa de `datetime` os nomes `date`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 18 a 18

```python
from django import forms
```

**Explicação deste trecho:**

**Linha 18 — ImportFrom** (nível 0 do bloco).

Importa de `django` os nomes `forms`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 19 a 19

```python
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
```

**Explicação deste trecho:**

**Linha 19 — ImportFrom** (nível 0 do bloco).

Importa de `django.contrib.auth.forms` os nomes `AuthenticationForm`, `UserCreationForm`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 21 a 21

```python
from .compatibilidade import TIPOS_SANGUINEOS
```

**Explicação deste trecho:**

**Linha 21 — ImportFrom** (nível 0 do bloco).

Importa de `.compatibilidade` os nomes `TIPOS_SANGUINEOS`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 22 a 22

```python
from .models import EstoqueMovimentacao, PedidoSangue, Usuario
```

**Explicação deste trecho:**

**Linha 22 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `EstoqueMovimentacao`, `PedidoSangue`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

### apenas_digitos — linhas 25 a 27

```python
def apenas_digitos(valor):
    """Retira todos os caracteres que nao sejam numeros."""
    return re.sub(r"\D", "", valor or "")
```

**Explicação deste trecho:**

**Linha 25 — FunctionDef** (nível 0 do bloco).

Define `apenas_digitos(valor)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 25:

**Linha 26 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 27 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `re.sub`; argumentos posicionais: `'\\D'`, `''`, `valor or ''` ao chamador.

### CadastroUsuarioForm — linhas 30 a 304

```python
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

    aceita_notificacoes_pedidos = forms.BooleanField(
        label="Autorizo alertas internos de estoque e pedidos compativeis (para Doadores).",
        required=False,
        initial=False,
        help_text="Opcional. Posso cancelar a autorizacao no meu painel.",
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
            "aceita_notificacoes_pedidos",
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
        if perfil != Usuario.Perfil.DOADOR:
            dados["aceita_notificacoes_pedidos"] = False
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
            if cpf:
                self.add_error(
                    "cpf",
                    "Hemocentro deve informar CNPJ, não CPF.",
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
            if cnpj:
                self.add_error(
                    "cnpj",
                    "Doador e Receptor devem informar CPF, não CNPJ.",
                )

        if perfil == Usuario.Perfil.OBSERVADOR and (cpf or cnpj):
            self.add_error(
                "cpf" if cpf else "cnpj",
                "Observador não precisa informar CPF ou CNPJ.",
            )

        return dados
```

**Explicação deste trecho:**

**Linha 30 — ClassDef** (nível 0 do bloco).

Define a classe `CadastroUsuarioForm` herdando de `UserCreationForm`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 30:

**Linha 31 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 33 — Assign** (nível 1 do bloco).

Associa `cpf` a a chamada `forms.CharField`; argumentos nomeados: `label='CPF'`, `required=False`, `max_length=14`, `help_text='Obrigatorio para Doador e Receptor/Solicitante.'`, `widget=forms.TextInput(attrs={'placeholder': '000.000.000-00', 'autocomplete': 'off', 'inputmode': 'numeric'})`.

- `label='CPF'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `max_length=14`: limite de comprimento do campo.
- `help_text='Obrigatorio para Doador e Receptor/Solicitante.'`: orientação apresentada junto ao campo.
- `widget=forms.TextInput(attrs={'placeholder': '000.000.000-00', 'autocomplete': 'off', 'inputmode': 'numeric'})`: componente de entrada utilizado na tela.

**Linha 47 — Assign** (nível 1 do bloco).

Associa `cnpj` a a chamada `forms.CharField`; argumentos nomeados: `label='CNPJ'`, `required=False`, `max_length=18`, `help_text='Obrigatorio somente para Hemocentro.'`, `widget=forms.TextInput(attrs={'placeholder': '00.000.000/0000-00', 'autocomplete': 'off', 'inputmode': 'numeric'})`.

- `label='CNPJ'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `max_length=18`: limite de comprimento do campo.
- `help_text='Obrigatorio somente para Hemocentro.'`: orientação apresentada junto ao campo.
- `widget=forms.TextInput(attrs={'placeholder': '00.000.000/0000-00', 'autocomplete': 'off', 'inputmode': 'numeric'})`: componente de entrada utilizado na tela.

**Linha 61 — Assign** (nível 1 do bloco).

Associa `perfil` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Tipo de perfil'`, `choices=[(Usuario.Perfil.DOADOR, 'Doador'), (Usuario.Perfil.RECEPTOR, 'Receptor / Solicitante'), (Usuario.Perfil.HEMOCENTRO, 'Hemocentro'), (Usuario.Perfil.OBSERVADOR, 'Observador')]`, `help_text='Escolha Hemocentro somente para uma instituicao que sera analisada por um administrador.'`, `widget=forms.RadioSelect`.

- `label='Tipo de perfil'`: texto apresentado ao usuário.
- `choices=[(Usuario.Perfil.DOADOR, 'Doador'), (Usuario.Perfil.RECEPTOR, 'Receptor / Solicitante'), (Usuario.Perfil.HEMOCENTRO, 'Hemocentro'), (Usuario.Perfil.OBSERVADOR, 'Observador')]`: alternativas declaradas para validação e apresentação.
- `help_text='Escolha Hemocentro somente para uma instituicao que sera analisada por um administrador.'`: orientação apresentada junto ao campo.
- `widget=forms.RadioSelect`: componente de entrada utilizado na tela.

**Linha 76 — Assign** (nível 1 do bloco).

Associa `data_nascimento` a a chamada `forms.DateField`; argumentos nomeados: `label='Data de nascimento'`, `required=False`, `help_text='Obrigatoria para Doador e Receptor/Solicitante.'`, `widget=forms.DateInput(attrs={'type': 'date'})`.

- `label='Data de nascimento'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `help_text='Obrigatoria para Doador e Receptor/Solicitante.'`: orientação apresentada junto ao campo.
- `widget=forms.DateInput(attrs={'type': 'date'})`: componente de entrada utilizado na tela.

**Linha 87 — Assign** (nível 1 do bloco).

Associa `aceite_lgpd` a a chamada `forms.BooleanField`; argumentos nomeados: `label='Li e aceito os Termos de Uso e a Politica de Privacidade.'`, `required=True`.

- `label='Li e aceito os Termos de Uso e a Politica de Privacidade.'`: texto apresentado ao usuário.
- `required=True`: indica se o formulário exige preenchimento.

**Linha 92 — Assign** (nível 1 do bloco).

Associa `aceita_notificacoes_pedidos` a a chamada `forms.BooleanField`; argumentos nomeados: `label='Autorizo alertas internos de estoque e pedidos compativeis (para Doadores).'`, `required=False`, `initial=False`, `help_text='Opcional. Posso cancelar a autorizacao no meu painel.'`.

- `label='Autorizo alertas internos de estoque e pedidos compativeis (para Doadores).'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `initial=False`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `help_text='Opcional. Posso cancelar a autorizacao no meu painel.'`: orientação apresentada junto ao campo.

**Linha 99 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 99:

**Linha 100 — Assign** (nível 2 do bloco).

Associa `model` a o valor associado ao nome `Usuario`.

**Linha 102 — Assign** (nível 2 do bloco).

Associa `fields` a uma coleção List com 14 itens, na expressão `['nome', 'email', 'perfil', 'cpf', 'cnpj', 'telefone', 'data_nascimento', 'sexo', 'cidade', 'estado', 'password1', 'password2', 'aceite_lgpd', 'aceita_notificacoes_pedidos']`.

**Linha 119 — Assign** (nível 2 do bloco).

Associa `labels` a um dicionário de 6 entradas; as chaves dão nome aos valores associados.

- Chave `'nome'`: recebe o valor literal `'Nome completo'`.
- Chave `'email'`: recebe o valor literal `'E-mail'`.
- Chave `'telefone'`: recebe o valor literal `'Telefone'`.
- Chave `'sexo'`: recebe o valor literal `'Sexo'`.
- Chave `'cidade'`: recebe o valor literal `'Cidade'`.
- Chave `'estado'`: recebe o valor literal `'Estado (UF)'`.

**Linha 128 — Assign** (nível 2 do bloco).

Associa `widgets` a um dicionário de 3 entradas; as chaves dão nome aos valores associados.

- Chave `'email'`: recebe a chamada `forms.EmailInput`; argumentos nomeados: `attrs={'autocomplete': 'email'}`.
- Chave `'telefone'`: recebe a chamada `forms.TextInput`; argumentos nomeados: `attrs={'placeholder': '(00) 00000-0000', 'inputmode': 'tel'}`.
- Chave `'estado'`: recebe a chamada `forms.TextInput`; argumentos nomeados: `attrs={'maxlength': 2, 'placeholder': 'MG', 'style': 'text-transform: uppercase;'}`.

**Linha 149 — FunctionDef** (nível 1 do bloco).

Define `__init__(self, *args, **kwargs)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 149:

**Linha 150 — Expr** (nível 2 do bloco).

Executa a chamada `super().__init__`; argumentos posicionais: `*args`; argumentos nomeados: `**=kwargs`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 152 — Assign** (nível 2 do bloco).

Associa `self.fields['password1'].label` a o valor literal `'Senha'`.

**Linha 153 — Assign** (nível 2 do bloco).

Associa `self.fields['password1'].help_text` a o valor literal `'Use no minimo 8 caracteres, incluindo letras e numeros.'`.

**Linha 157 — Assign** (nível 2 do bloco).

Associa `self.fields['password2'].label` a o valor literal `'Confirme a senha'`.

**Linha 159 — FunctionDef** (nível 1 do bloco).

Define `clean_nome(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 159:

**Linha 160 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 161 — Assign** (nível 2 do bloco).

Associa `nome` a a chamada `(self.cleaned_data.get('nome') or '').strip`, que remove espaços nas extremidades do texto.


**Linha 163 — If** (nível 2 do bloco).

Escolhe um caminho verificando a negação de `nome`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 163:

**Linha 164 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `forms.ValidationError`; argumentos posicionais: `'Informe o nome completo.'`.

**Linha 166 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `nome` ao chamador.

**Linha 168 — FunctionDef** (nível 1 do bloco).

Define `clean_email(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 168:

**Linha 169 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 170 — Assign** (nível 2 do bloco).

Associa `email` a a chamada `(self.cleaned_data.get('email') or '').strip().lower`, que converte texto para minúsculas.


**Linha 172 — If** (nível 2 do bloco).

Escolhe um caminho verificando a chamada `Usuario.objects.filter(email__iexact=email).exists`, que verifica se há pelo menos um resultado. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 172:

**Linha 173 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `forms.ValidationError`; argumentos posicionais: `'Ja existe uma conta cadastrada com este e-mail.'`.

**Linha 177 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `email` ao chamador.

**Linha 179 — FunctionDef** (nível 1 do bloco).

Define `clean_cpf(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 179:

**Linha 180 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 181 — Assign** (nível 2 do bloco).

Associa `cpf` a a chamada `apenas_digitos`; argumentos posicionais: `self.cleaned_data.get('cpf')`.


**Linha 183 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `cpf` ; `len(cpf) != 11` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 183:

**Linha 184 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `forms.ValidationError`; argumentos posicionais: `'O CPF deve conter exatamente 11 numeros.'`.

**Linha 188 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `cpf` ; `Usuario.objects.filter(cpf=cpf).exists()` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 188:

**Linha 189 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `forms.ValidationError`; argumentos posicionais: `'Este CPF ja esta cadastrado.'`.

**Linha 193 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve pelo menos uma das condições: `cpf` ; `None` (com avaliação interrompida assim que o resultado é determinado) ao chamador.

**Linha 195 — FunctionDef** (nível 1 do bloco).

Define `clean_cnpj(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 195:

**Linha 196 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 197 — Assign** (nível 2 do bloco).

Associa `cnpj` a a chamada `apenas_digitos`; argumentos posicionais: `self.cleaned_data.get('cnpj')`.


**Linha 199 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `cnpj` ; `len(cnpj) != 14` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 199:

**Linha 200 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `forms.ValidationError`; argumentos posicionais: `'O CNPJ deve conter exatamente 14 numeros.'`.

**Linha 204 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `cnpj` ; `Usuario.objects.filter(cnpj=cnpj).exists()` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 204:

**Linha 205 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `forms.ValidationError`; argumentos posicionais: `'Este CNPJ ja esta cadastrado.'`.

**Linha 209 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve pelo menos uma das condições: `cnpj` ; `None` (com avaliação interrompida assim que o resultado é determinado) ao chamador.

**Linha 211 — FunctionDef** (nível 1 do bloco).

Define `clean_estado(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 211:

**Linha 212 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 213 — Assign** (nível 2 do bloco).

Associa `estado` a a chamada `(self.cleaned_data.get('estado') or '').strip().upper`, que converte texto para maiúsculas.


**Linha 215 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `estado` ; `len(estado) != 2` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 215:

**Linha 216 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `forms.ValidationError`; argumentos posicionais: `'Informe a UF com 2 letras, por exemplo: MG.'`.

**Linha 220 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `estado` ao chamador.

**Linha 222 — FunctionDef** (nível 1 do bloco).

Define `clean_password1(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 222:

**Linha 223 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 224 — Assign** (nível 2 do bloco).

Associa `senha` a a chamada `self.cleaned_data.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'password1'`, `''`.


**Linha 226 — If** (nível 2 do bloco).

Escolhe um caminho verificando a negação de `senha`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 226:

**Linha 227 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `senha` ao chamador.

**Linha 229 — Assign** (nível 2 do bloco).

Associa `possui_letra` a a chamada `bool`; argumentos posicionais: `re.search('[A-Za-z]', senha)`.


**Linha 230 — Assign** (nível 2 do bloco).

Associa `possui_numero` a a chamada `bool`; argumentos posicionais: `re.search('\\d', senha)`.


**Linha 232 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `len(senha)` menor que `8`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 232:

**Linha 233 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `forms.ValidationError`; argumentos posicionais: `'A senha deve possuir pelo menos 8 caracteres.'`.

**Linha 237 — If** (nível 2 do bloco).

Escolhe um caminho verificando pelo menos uma das condições: `not possui_letra` ; `not possui_numero` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 237:

**Linha 238 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `forms.ValidationError`; argumentos posicionais: `'A senha precisa conter pelo menos uma letra e um numero.'`.

**Linha 242 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `senha` ao chamador.

**Linha 244 — FunctionDef** (nível 1 do bloco).

Define `clean(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 244:

**Linha 245 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 254 — Assign** (nível 2 do bloco).

Associa `dados` a a chamada `super().clean`.


**Linha 256 — Assign** (nível 2 do bloco).

Associa `perfil` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'perfil'`.


**Linha 257 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `perfil` diferente de `Usuario.Perfil.DOADOR`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 257:

**Linha 258 — Assign** (nível 3 do bloco).

Associa `dados['aceita_notificacoes_pedidos']` a o valor literal `False`.

**Linha 259 — Assign** (nível 2 do bloco).

Associa `cpf` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'cpf'`.


**Linha 260 — Assign** (nível 2 do bloco).

Associa `cnpj` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'cnpj'`.


**Linha 261 — Assign** (nível 2 do bloco).

Associa `data_nascimento` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'data_nascimento'`.


**Linha 263 — Assign** (nível 2 do bloco).

Associa `perfis_pessoa` a uma coleção Tuple com 2 itens, na expressão `(Usuario.Perfil.DOADOR, Usuario.Perfil.RECEPTOR)`.

**Linha 268 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `perfil` igual a `Usuario.Perfil.HEMOCENTRO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 268:

**Linha 269 — If** (nível 3 do bloco).

Escolhe um caminho verificando a negação de `cnpj`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 269:

**Linha 270 — Expr** (nível 4 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `'cnpj'`, `'Informe o CNPJ do hemocentro.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 274 — If** (nível 3 do bloco).

Escolhe um caminho verificando o valor associado ao nome `cpf`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 274:

**Linha 275 — Expr** (nível 4 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `'cpf'`, `'Hemocentro deve informar CNPJ, não CPF.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 280 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `perfil` contido em `perfis_pessoa`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 280:

**Linha 281 — If** (nível 3 do bloco).

Escolhe um caminho verificando a negação de `cpf`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 281:

**Linha 282 — Expr** (nível 4 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `'cpf'`, `'Informe o CPF para este tipo de perfil.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 287 — If** (nível 3 do bloco).

Escolhe um caminho verificando a negação de `data_nascimento`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 287:

**Linha 288 — Expr** (nível 4 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `'data_nascimento'`, `'Informe a data de nascimento para este tipo de perfil.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 292 — If** (nível 3 do bloco).

Escolhe um caminho verificando o valor associado ao nome `cnpj`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 292:

**Linha 293 — Expr** (nível 4 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `'cnpj'`, `'Doador e Receptor devem informar CPF, não CNPJ.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 298 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `perfil == Usuario.Perfil.OBSERVADOR` ; `cpf or cnpj` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 298:

**Linha 299 — Expr** (nível 3 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `'cpf' if cpf else 'cnpj'`, `'Observador não precisa informar CPF ou CNPJ.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 304 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `dados` ao chamador.

### PreferenciaConvocacaoForm — linhas 307 a 312

```python
class PreferenciaConvocacaoForm(forms.Form):
    aceita_convocacoes = forms.BooleanField(
        label="Autorizo receber alertas internos de estoque e pedidos compativeis.",
        required=False,
        help_text="Opcional. Desmarque para cancelar futuras convocacoes.",
    )
```

**Explicação deste trecho:**

**Linha 307 — ClassDef** (nível 0 do bloco).

Define a classe `PreferenciaConvocacaoForm` herdando de `forms.Form`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 307:

**Linha 308 — Assign** (nível 1 do bloco).

Associa `aceita_convocacoes` a a chamada `forms.BooleanField`; argumentos nomeados: `label='Autorizo receber alertas internos de estoque e pedidos compativeis.'`, `required=False`, `help_text='Opcional. Desmarque para cancelar futuras convocacoes.'`.

- `label='Autorizo receber alertas internos de estoque e pedidos compativeis.'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `help_text='Opcional. Desmarque para cancelar futuras convocacoes.'`: orientação apresentada junto ao campo.

### LoginUsuarioForm — linhas 315 a 344

```python
class LoginUsuarioForm(AuthenticationForm):
    """Formulario de login usando e-mail."""

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if getattr(user, "suspensa", False):
            raise forms.ValidationError(
                "Esta conta está suspensa. Procure o administrador.",
                code="inactive",
            )

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
```

**Explicação deste trecho:**

**Linha 315 — ClassDef** (nível 0 do bloco).

Define a classe `LoginUsuarioForm` herdando de `AuthenticationForm`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 315:

**Linha 316 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 318 — FunctionDef** (nível 1 do bloco).

Define `confirm_login_allowed(self, user)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 318:

**Linha 319 — Expr** (nível 2 do bloco).

Executa a chamada `super().confirm_login_allowed`; argumentos posicionais: `user`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 320 — If** (nível 2 do bloco).

Escolhe um caminho verificando a chamada `getattr`; argumentos posicionais: `user`, `'suspensa'`, `False`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 320:

**Linha 321 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `forms.ValidationError`; argumentos posicionais: `'Esta conta está suspensa. Procure o administrador.'`; argumentos nomeados: `code='inactive'`.

**Linha 326 — Assign** (nível 1 do bloco).

Associa `username` a a chamada `forms.EmailField`; argumentos nomeados: `label='E-mail'`, `widget=forms.EmailInput(attrs={'autocomplete': 'email', 'autofocus': True})`.

- `label='E-mail'`: texto apresentado ao usuário.
- `widget=forms.EmailInput(attrs={'autocomplete': 'email', 'autofocus': True})`: componente de entrada utilizado na tela.

**Linha 336 — Assign** (nível 1 do bloco).

Associa `password` a a chamada `forms.CharField`; argumentos nomeados: `label='Senha'`, `strip=False`, `widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})`.

- `label='Senha'`: texto apresentado ao usuário.
- `strip=False`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})`: componente de entrada utilizado na tela.

### TriagemExtensaForm — linhas 347 a 465

```python
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
```

**Explicação deste trecho:**

**Linha 347 — ClassDef** (nível 0 do bloco).

Define a classe `TriagemExtensaForm` herdando de `forms.Form`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 347:

**Linha 348 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 355 — Assign** (nível 1 do bloco).

Associa `entende_orientacao` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Você entende que esta triagem é apenas uma orientação e que a decisão final será feita pela equipe do hemocentro?'`, `choices=[('SIM', 'Sim, entendo e quero continuar.'), ('NAO', 'Não entendi ou quero receber a explicação novamente.')]`, `widget=forms.RadioSelect`.

- `label='Você entende que esta triagem é apenas uma orientação e que a decisão final será feita pela equipe do hemocentro?'`: texto apresentado ao usuário.
- `choices=[('SIM', 'Sim, entendo e quero continuar.'), ('NAO', 'Não entendi ou quero receber a explicação novamente.')]`: alternativas declaradas para validação e apresentação.
- `widget=forms.RadioSelect`: componente de entrada utilizado na tela.

**Linha 367 — Assign** (nível 1 do bloco).

Associa `idade` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Qual é a sua idade hoje?'`, `choices=[('MENOS_16', 'Menos de 16 anos'), ('16_17', '16 ou 17 anos'), ('18_60', '18 a 60 anos'), ('61_69', '61 a 69 anos'), ('70_MAIS', '70 anos ou mais')]`, `widget=forms.RadioSelect`.

- `label='Qual é a sua idade hoje?'`: texto apresentado ao usuário.
- `choices=[('MENOS_16', 'Menos de 16 anos'), ('16_17', '16 ou 17 anos'), ('18_60', '18 a 60 anos'), ('61_69', '61 a 69 anos'), ('70_MAIS', '70 anos ou mais')]`: alternativas declaradas para validação e apresentação.
- `widget=forms.RadioSelect`: componente de entrada utilizado na tela.

**Linha 379 — Assign** (nível 1 do bloco).

Associa `peso` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Quanto você pesa aproximadamente?'`, `choices=[('MENOS_50', 'Menos de 50 kg'), ('50_55_9', 'De 50 a 55,9 kg'), ('56_129_9', 'De 56 a 129,9 kg'), ('130_MAIS', '130 kg ou mais'), ('NAO_SEI', 'Não sei meu peso atual')]`, `widget=forms.RadioSelect`.

- `label='Quanto você pesa aproximadamente?'`: texto apresentado ao usuário.
- `choices=[('MENOS_50', 'Menos de 50 kg'), ('50_55_9', 'De 50 a 55,9 kg'), ('56_129_9', 'De 56 a 129,9 kg'), ('130_MAIS', '130 kg ou mais'), ('NAO_SEI', 'Não sei meu peso atual')]`: alternativas declaradas para validação e apresentação.
- `widget=forms.RadioSelect`: componente de entrada utilizado na tela.

**Linha 391 — Assign** (nível 1 do bloco).

Associa `sexo_biologico` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Qual opção corresponde ao seu sexo biológico?'`, `choices=[('FEMININO', 'Feminino'), ('MASCULINO', 'Masculino'), ('OUTRO', 'Outra situação ou não sei qual regra se aplica'), ('NAO_INFORMAR', 'Prefiro não informar')]`, `widget=forms.RadioSelect`.

- `label='Qual opção corresponde ao seu sexo biológico?'`: texto apresentado ao usuário.
- `choices=[('FEMININO', 'Feminino'), ('MASCULINO', 'Masculino'), ('OUTRO', 'Outra situação ou não sei qual regra se aplica'), ('NAO_INFORMAR', 'Prefiro não informar')]`: alternativas declaradas para validação e apresentação.
- `widget=forms.RadioSelect`: componente de entrada utilizado na tela.

**Linha 402 — Assign** (nível 1 do bloco).

Associa `ja_doou` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Você já doou sangue alguma vez?'`, `choices=[('NAO', 'Nunca doei'), ('SIM', 'Sim, já doei'), ('NAO_LEMBRO', 'Não tenho certeza ou não lembro')]`, `widget=forms.RadioSelect`.

- `label='Você já doou sangue alguma vez?'`: texto apresentado ao usuário.
- `choices=[('NAO', 'Nunca doei'), ('SIM', 'Sim, já doei'), ('NAO_LEMBRO', 'Não tenho certeza ou não lembro')]`: alternativas declaradas para validação e apresentação.
- `widget=forms.RadioSelect`: componente de entrada utilizado na tela.

**Linha 412 — Assign** (nível 1 do bloco).

Associa `data_ultima_doacao` a a chamada `forms.DateField`; argumentos nomeados: `label='Qual foi a data da sua última doação de sangue total?'`, `required=False`, `widget=forms.DateInput(attrs={'type': 'date'})`.

- `label='Qual foi a data da sua última doação de sangue total?'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `widget=forms.DateInput(attrs={'type': 'date'})`: componente de entrada utilizado na tela.

**Linha 422 — Assign** (nível 1 do bloco).

Associa `doacoes_12_meses` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Quantas doações de sangue total você fez nos últimos 12 meses?'`, `required=False`, `choices=[('0', 'Nenhuma'), ('1', '1'), ('2', '2'), ('3', '3'), ('4_MAIS', '4 ou mais'), ('NAO_LEMBRO', 'Não lembro')]`, `widget=forms.RadioSelect`.

- `label='Quantas doações de sangue total você fez nos últimos 12 meses?'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `choices=[('0', 'Nenhuma'), ('1', '1'), ('2', '2'), ('3', '3'), ('4_MAIS', '4 ou mais'), ('NAO_LEMBRO', 'Não lembro')]`: alternativas declaradas para validação e apresentação.
- `widget=forms.RadioSelect`: componente de entrada utilizado na tela.

**Linha 436 — FunctionDef** (nível 1 do bloco).

Define `clean(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 436:

**Linha 437 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 441 — Assign** (nível 2 do bloco).

Associa `dados` a a chamada `super().clean`.


**Linha 443 — Assign** (nível 2 do bloco).

Associa `ja_doou` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'ja_doou'`.


**Linha 444 — Assign** (nível 2 do bloco).

Associa `data_ultima_doacao` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'data_ultima_doacao'`.


**Linha 445 — Assign** (nível 2 do bloco).

Associa `doacoes_12_meses` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'doacoes_12_meses'`.


**Linha 447 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `ja_doou == 'SIM'` ; `not data_ultima_doacao` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 447:

**Linha 448 — Expr** (nível 3 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `'data_ultima_doacao'`, `'Informe a data da última doação.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 453 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `ja_doou == 'SIM'` ; `not doacoes_12_meses` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 453:

**Linha 454 — Expr** (nível 3 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `'doacoes_12_meses'`, `'Informe a quantidade de doações.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 459 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `data_ultima_doacao` ; `data_ultima_doacao > date.today()` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 459:

**Linha 460 — Expr** (nível 3 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `'data_ultima_doacao'`, `'A data da última doação não pode estar no futuro.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 465 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `dados` ao chamador.

### CadastrarEstoqueForm — linhas 468 a 524

```python
class CadastrarEstoqueForm(forms.Form):
    """
    UC_29 - Formulario usado pelo Hemocentro para cadastrar a estrutura
    de estoque de um tipo sanguineo.

    A validacao de "ja existe estoque para este tipo" e de "hemocentro
    aprovado" fica na camada de servico (accounts/estoque.py), porque
    depende do usuario logado, que o form nao conhece sozinho.
    """

    tipo_sanguineo = forms.ChoiceField(
        label="Tipo sanguíneo",
        choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
    )

    quantidade_bolsas = forms.IntegerField(
        label="Quantidade atual de bolsas",
        min_value=0,
        initial=0,
        help_text="Quantidade de bolsas já disponíveis, se houver.",
    )

    nivel_minimo = forms.IntegerField(
        label="Nível mínimo",
        min_value=0,
        help_text=(
            "A partir de quantas bolsas o tipo passa a ser considerado baixo."
        ),
    )

    nivel_critico = forms.IntegerField(
        label="Nível crítico",
        min_value=0,
        help_text=(
            "A partir de quantas bolsas o tipo passa a ser considerado crítico."
        ),
    )

    def clean(self):
        """Garante que o nível crítico nunca seja maior que o mínimo."""

        dados = super().clean()

        nivel_minimo = dados.get("nivel_minimo")
        nivel_critico = dados.get("nivel_critico")

        if (
            nivel_minimo is not None
            and nivel_critico is not None
            and nivel_critico > nivel_minimo
        ):
            self.add_error(
                "nivel_critico",
                "O nível crítico deve ser menor ou igual ao nível mínimo.",
            )

        return dados
```

**Explicação deste trecho:**

**Linha 468 — ClassDef** (nível 0 do bloco).

Define a classe `CadastrarEstoqueForm` herdando de `forms.Form`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 468:

**Linha 469 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 478 — Assign** (nível 1 do bloco).

Associa `tipo_sanguineo` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Tipo sanguíneo'`, `choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS]`.

- `label='Tipo sanguíneo'`: texto apresentado ao usuário.
- `choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS]`: alternativas declaradas para validação e apresentação.

**Linha 483 — Assign** (nível 1 do bloco).

Associa `quantidade_bolsas` a a chamada `forms.IntegerField`; argumentos nomeados: `label='Quantidade atual de bolsas'`, `min_value=0`, `initial=0`, `help_text='Quantidade de bolsas já disponíveis, se houver.'`.

- `label='Quantidade atual de bolsas'`: texto apresentado ao usuário.
- `min_value=0`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `initial=0`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `help_text='Quantidade de bolsas já disponíveis, se houver.'`: orientação apresentada junto ao campo.

**Linha 490 — Assign** (nível 1 do bloco).

Associa `nivel_minimo` a a chamada `forms.IntegerField`; argumentos nomeados: `label='Nível mínimo'`, `min_value=0`, `help_text='A partir de quantas bolsas o tipo passa a ser considerado baixo.'`.

- `label='Nível mínimo'`: texto apresentado ao usuário.
- `min_value=0`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `help_text='A partir de quantas bolsas o tipo passa a ser considerado baixo.'`: orientação apresentada junto ao campo.

**Linha 498 — Assign** (nível 1 do bloco).

Associa `nivel_critico` a a chamada `forms.IntegerField`; argumentos nomeados: `label='Nível crítico'`, `min_value=0`, `help_text='A partir de quantas bolsas o tipo passa a ser considerado crítico.'`.

- `label='Nível crítico'`: texto apresentado ao usuário.
- `min_value=0`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `help_text='A partir de quantas bolsas o tipo passa a ser considerado crítico.'`: orientação apresentada junto ao campo.

**Linha 506 — FunctionDef** (nível 1 do bloco).

Define `clean(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 506:

**Linha 507 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 509 — Assign** (nível 2 do bloco).

Associa `dados` a a chamada `super().clean`.


**Linha 511 — Assign** (nível 2 do bloco).

Associa `nivel_minimo` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'nivel_minimo'`.


**Linha 512 — Assign** (nível 2 do bloco).

Associa `nivel_critico` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'nivel_critico'`.


**Linha 514 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `nivel_minimo is not None` ; `nivel_critico is not None` ; `nivel_critico > nivel_minimo` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 514:

**Linha 519 — Expr** (nível 3 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `'nivel_critico'`, `'O nível crítico deve ser menor ou igual ao nível mínimo.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 524 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `dados` ao chamador.

### MovimentarEstoqueForm — linhas 527 a 580

```python
class MovimentarEstoqueForm(forms.Form):
    """
    Formulario usado pelo Hemocentro para registrar entrada,
    saída ou ajuste de bolsas em um estoque já cadastrado.
    """

    tipo_movimento = forms.ChoiceField(
        label="Tipo de movimentação",
        choices=EstoqueMovimentacao.TipoMovimento.choices,
        widget=forms.RadioSelect,
    )

    quantidade = forms.IntegerField(
        label="Quantidade",
        min_value=0,
        help_text=(
            "Para entrada/saída: quantidade a movimentar. "
            "Para ajuste: nova quantidade total de bolsas."
        ),
    )

    motivo = forms.CharField(
        label="Motivo",
        required=True,
        max_length=255,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=(
            "Obrigatório. Ex.: doação recebida, transfusão realizada, "
            "contagem física."
        ),
    )

    def clean(self):
        dados = super().clean()

        tipo_movimento = dados.get("tipo_movimento")
        quantidade = dados.get("quantidade")

        movimentos_positivos = (
            EstoqueMovimentacao.TipoMovimento.ENTRADA,
            EstoqueMovimentacao.TipoMovimento.SAIDA,
        )

        if (
            tipo_movimento in movimentos_positivos
            and quantidade is not None
            and quantidade <= 0
        ):
            self.add_error(
                "quantidade",
                "Informe uma quantidade maior que zero.",
            )

        return dados
```

**Explicação deste trecho:**

**Linha 527 — ClassDef** (nível 0 do bloco).

Define a classe `MovimentarEstoqueForm` herdando de `forms.Form`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 527:

**Linha 528 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 533 — Assign** (nível 1 do bloco).

Associa `tipo_movimento` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Tipo de movimentação'`, `choices=EstoqueMovimentacao.TipoMovimento.choices`, `widget=forms.RadioSelect`.

- `label='Tipo de movimentação'`: texto apresentado ao usuário.
- `choices=EstoqueMovimentacao.TipoMovimento.choices`: alternativas declaradas para validação e apresentação.
- `widget=forms.RadioSelect`: componente de entrada utilizado na tela.

**Linha 539 — Assign** (nível 1 do bloco).

Associa `quantidade` a a chamada `forms.IntegerField`; argumentos nomeados: `label='Quantidade'`, `min_value=0`, `help_text='Para entrada/saída: quantidade a movimentar. Para ajuste: nova quantidade total de bolsas.'`.

- `label='Quantidade'`: texto apresentado ao usuário.
- `min_value=0`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `help_text='Para entrada/saída: quantidade a movimentar. Para ajuste: nova quantidade total de bolsas.'`: orientação apresentada junto ao campo.

**Linha 548 — Assign** (nível 1 do bloco).

Associa `motivo` a a chamada `forms.CharField`; argumentos nomeados: `label='Motivo'`, `required=True`, `max_length=255`, `widget=forms.Textarea(attrs={'rows': 3})`, `help_text='Obrigatório. Ex.: doação recebida, transfusão realizada, contagem física.'`.

- `label='Motivo'`: texto apresentado ao usuário.
- `required=True`: indica se o formulário exige preenchimento.
- `max_length=255`: limite de comprimento do campo.
- `widget=forms.Textarea(attrs={'rows': 3})`: componente de entrada utilizado na tela.
- `help_text='Obrigatório. Ex.: doação recebida, transfusão realizada, contagem física.'`: orientação apresentada junto ao campo.

**Linha 559 — FunctionDef** (nível 1 do bloco).

Define `clean(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 559:

**Linha 560 — Assign** (nível 2 do bloco).

Associa `dados` a a chamada `super().clean`.


**Linha 562 — Assign** (nível 2 do bloco).

Associa `tipo_movimento` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'tipo_movimento'`.


**Linha 563 — Assign** (nível 2 do bloco).

Associa `quantidade` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'quantidade'`.


**Linha 565 — Assign** (nível 2 do bloco).

Associa `movimentos_positivos` a uma coleção Tuple com 2 itens, na expressão `(EstoqueMovimentacao.TipoMovimento.ENTRADA, EstoqueMovimentacao.TipoMovimento.SAIDA)`.

**Linha 570 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `tipo_movimento in movimentos_positivos` ; `quantidade is not None` ; `quantidade <= 0` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 570:

**Linha 575 — Expr** (nível 3 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `'quantidade'`, `'Informe uma quantidade maior que zero.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 580 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `dados` ao chamador.

### PedidoSangueForm — linhas 582 a 702

```python
class PedidoSangueForm(forms.ModelForm):
    """
    Formulário para solicitar a divulgação de uma necessidade.

    As validacoes mais sensiveis ficam em validacao_pedido.py.
    Aqui ficam as validacoes de formulario.
    """

    contato = forms.EmailField(
        label="E-mail de contato",
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "seuemail@exemplo.com",
            }
        ),
    )

    class Meta:
        model = PedidoSangue

        fields = [
            "nome_solicitante",
            "contato",
            "para_quem",
            "hemocentro_destino",
            "titulo",
            "tipo_sanguineo",
            "urgencia",
            "cidade",
            "nome_paciente",
            "descricao",
            "justificativa_urgencia",
            "informacoes_complementares",
        ]

        labels = {
            "para_quem": "Para quem e este pedido?",
            "nome_solicitante": "Nome ou identificação do solicitante",
            "contato": "E-mail de contato",
            "hemocentro_destino": "Hemocentro de destino",
            "titulo": "Titulo do pedido",
            "tipo_sanguineo": "Tipo sanguineo",
            "urgencia": "Urgencia",
            "cidade": "Cidade",
            "nome_paciente": "Nome da pessoa (opcional)",
            "descricao": "Descricao",
            "justificativa_urgencia": "Justificativa da urgencia",
            "informacoes_complementares": "Informações complementares",
        }

        widgets = {
            "para_quem": forms.RadioSelect,
            "tipo_sanguineo": forms.RadioSelect,
            "urgencia": forms.RadioSelect,
            "descricao": forms.Textarea(attrs={"rows": 5}),
            "justificativa_urgencia": forms.Textarea(attrs={"rows": 4}),
            "informacoes_complementares": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["hemocentro_destino"].queryset = (
            Usuario.objects
            .filter(
                perfil=Usuario.Perfil.HEMOCENTRO,
                status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO,
            )
            .order_by("nome")
        )

    def clean_nome_paciente(self):
        return (self.cleaned_data.get("nome_paciente") or "").strip()

    def clean_nome_solicitante(self):
        nome = (self.cleaned_data.get("nome_solicitante") or "").strip()
        if not nome:
            raise forms.ValidationError(
                "Informe o nome ou uma identificação do solicitante."
            )
        return nome

    def clean_contato(self):
        contato = (self.cleaned_data.get("contato") or "").strip()
        if not contato:
            raise forms.ValidationError("Informe um e-mail para retorno.")
        return contato.lower()

    def clean_descricao(self):
        descricao = (self.cleaned_data.get("descricao") or "").strip()

        if len(descricao) < 10:
            raise forms.ValidationError(
                "Descreva a necessidade com pelo menos 10 caracteres."
            )

        return descricao

    def clean(self):
        dados = super().clean()

        urgencia = dados.get("urgencia")
        justificativa = (
            dados.get("justificativa_urgencia") or ""
        ).strip()

        if urgencia in [
            PedidoSangue.Urgencia.ALTA,
            PedidoSangue.Urgencia.CRITICA,
        ]:
            if len(justificativa) < 20:
                self.add_error(
                    "justificativa_urgencia",
                    (
                        "Pedidos de urgencia alta ou critica precisam "
                        "de justificativa com pelo menos 20 caracteres."
                    ),
                )

        return dados
```

**Explicação deste trecho:**

**Linha 582 — ClassDef** (nível 0 do bloco).

Define a classe `PedidoSangueForm` herdando de `forms.ModelForm`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 582:

**Linha 583 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 590 — Assign** (nível 1 do bloco).

Associa `contato` a a chamada `forms.EmailField`; argumentos nomeados: `label='E-mail de contato'`, `widget=forms.EmailInput(attrs={'autocomplete': 'email', 'placeholder': 'seuemail@exemplo.com'})`.

- `label='E-mail de contato'`: texto apresentado ao usuário.
- `widget=forms.EmailInput(attrs={'autocomplete': 'email', 'placeholder': 'seuemail@exemplo.com'})`: componente de entrada utilizado na tela.

**Linha 600 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 600:

**Linha 601 — Assign** (nível 2 do bloco).

Associa `model` a o valor associado ao nome `PedidoSangue`.

**Linha 603 — Assign** (nível 2 do bloco).

Associa `fields` a uma coleção List com 12 itens, na expressão `['nome_solicitante', 'contato', 'para_quem', 'hemocentro_destino', 'titulo', 'tipo_sanguineo', 'urgencia', 'cidade', 'nome_paciente', 'descricao', 'justificativa_urgencia', 'informacoes_complementares']`.

**Linha 618 — Assign** (nível 2 do bloco).

Associa `labels` a um dicionário de 12 entradas; as chaves dão nome aos valores associados.

- Chave `'para_quem'`: recebe o valor literal `'Para quem e este pedido?'`.
- Chave `'nome_solicitante'`: recebe o valor literal `'Nome ou identificação do solicitante'`.
- Chave `'contato'`: recebe o valor literal `'E-mail de contato'`.
- Chave `'hemocentro_destino'`: recebe o valor literal `'Hemocentro de destino'`.
- Chave `'titulo'`: recebe o valor literal `'Titulo do pedido'`.
- Chave `'tipo_sanguineo'`: recebe o valor literal `'Tipo sanguineo'`.
- Chave `'urgencia'`: recebe o valor literal `'Urgencia'`.
- Chave `'cidade'`: recebe o valor literal `'Cidade'`.
- Chave `'nome_paciente'`: recebe o valor literal `'Nome da pessoa (opcional)'`.
- Chave `'descricao'`: recebe o valor literal `'Descricao'`.
- Chave `'justificativa_urgencia'`: recebe o valor literal `'Justificativa da urgencia'`.
- Chave `'informacoes_complementares'`: recebe o valor literal `'Informações complementares'`.

**Linha 633 — Assign** (nível 2 do bloco).

Associa `widgets` a um dicionário de 6 entradas; as chaves dão nome aos valores associados.

- Chave `'para_quem'`: recebe o atributo `RadioSelect` de `forms`.
- Chave `'tipo_sanguineo'`: recebe o atributo `RadioSelect` de `forms`.
- Chave `'urgencia'`: recebe o atributo `RadioSelect` de `forms`.
- Chave `'descricao'`: recebe a chamada `forms.Textarea`; argumentos nomeados: `attrs={'rows': 5}`.
- Chave `'justificativa_urgencia'`: recebe a chamada `forms.Textarea`; argumentos nomeados: `attrs={'rows': 4}`.
- Chave `'informacoes_complementares'`: recebe a chamada `forms.Textarea`; argumentos nomeados: `attrs={'rows': 4}`.

**Linha 642 — FunctionDef** (nível 1 do bloco).

Define `__init__(self, *args, **kwargs)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 642:

**Linha 643 — Expr** (nível 2 do bloco).

Executa a chamada `super().__init__`; argumentos posicionais: `*args`; argumentos nomeados: `**=kwargs`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 645 — Assign** (nível 2 do bloco).

Associa `self.fields['hemocentro_destino'].queryset` a a chamada `Usuario.objects.filter(perfil=Usuario.Perfil.HEMOCENTRO, status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO).order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'nome'`.


**Linha 654 — FunctionDef** (nível 1 do bloco).

Define `clean_nome_paciente(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 654:

**Linha 655 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `(self.cleaned_data.get('nome_paciente') or '').strip`, que remove espaços nas extremidades do texto ao chamador.

**Linha 657 — FunctionDef** (nível 1 do bloco).

Define `clean_nome_solicitante(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 657:

**Linha 658 — Assign** (nível 2 do bloco).

Associa `nome` a a chamada `(self.cleaned_data.get('nome_solicitante') or '').strip`, que remove espaços nas extremidades do texto.


**Linha 659 — If** (nível 2 do bloco).

Escolhe um caminho verificando a negação de `nome`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 659:

**Linha 660 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `forms.ValidationError`; argumentos posicionais: `'Informe o nome ou uma identificação do solicitante.'`.

**Linha 663 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `nome` ao chamador.

**Linha 665 — FunctionDef** (nível 1 do bloco).

Define `clean_contato(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 665:

**Linha 666 — Assign** (nível 2 do bloco).

Associa `contato` a a chamada `(self.cleaned_data.get('contato') or '').strip`, que remove espaços nas extremidades do texto.


**Linha 667 — If** (nível 2 do bloco).

Escolhe um caminho verificando a negação de `contato`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 667:

**Linha 668 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `forms.ValidationError`; argumentos posicionais: `'Informe um e-mail para retorno.'`.

**Linha 669 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `contato.lower`, que converte texto para minúsculas ao chamador.

**Linha 671 — FunctionDef** (nível 1 do bloco).

Define `clean_descricao(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 671:

**Linha 672 — Assign** (nível 2 do bloco).

Associa `descricao` a a chamada `(self.cleaned_data.get('descricao') or '').strip`, que remove espaços nas extremidades do texto.


**Linha 674 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `len(descricao)` menor que `10`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 674:

**Linha 675 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `forms.ValidationError`; argumentos posicionais: `'Descreva a necessidade com pelo menos 10 caracteres.'`.

**Linha 679 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `descricao` ao chamador.

**Linha 681 — FunctionDef** (nível 1 do bloco).

Define `clean(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 681:

**Linha 682 — Assign** (nível 2 do bloco).

Associa `dados` a a chamada `super().clean`.


**Linha 684 — Assign** (nível 2 do bloco).

Associa `urgencia` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'urgencia'`.


**Linha 685 — Assign** (nível 2 do bloco).

Associa `justificativa` a a chamada `(dados.get('justificativa_urgencia') or '').strip`, que remove espaços nas extremidades do texto.


**Linha 689 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `urgencia` contido em `[PedidoSangue.Urgencia.ALTA, PedidoSangue.Urgencia.CRITICA]`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 689:

**Linha 693 — If** (nível 3 do bloco).

Escolhe um caminho verificando a comparação `len(justificativa)` menor que `20`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 693:

**Linha 694 — Expr** (nível 4 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `'justificativa_urgencia'`, `'Pedidos de urgencia alta ou critica precisam de justificativa com pelo menos 20 caracteres.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 702 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `dados` ao chamador.

### FiltroPedidoSangueForm — linhas 705 a 752

```python
class FiltroPedidoSangueForm(forms.Form):
    """
    RF - Visualizar e filtrar pedidos.

    Filtros:

    - tipo sanguineo;
    - urgencia;
    - cidade;
    - hemocentro;
    - data.
    """

    tipo_sanguineo = forms.ChoiceField(
        label="Tipo sanguineo",
        required=False,
        choices=[
            ("", "Todos")
        ] + [(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
    )

    urgencia = forms.ChoiceField(
        label="Urgencia",
        required=False,
        choices=[("", "Todas")] + list(PedidoSangue.Urgencia.choices),
    )

    cidade = forms.CharField(
        label="Cidade",
        required=False,
    )

    hemocentro = forms.CharField(
        label="Hemocentro",
        required=False,
    )

    data = forms.DateField(
        label="Data",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    status = forms.ChoiceField(
        label="Status",
        required=False,
        choices=[("", "Todos")] + list(PedidoSangue.Status.choices),
    )
```

**Explicação deste trecho:**

**Linha 705 — ClassDef** (nível 0 do bloco).

Define a classe `FiltroPedidoSangueForm` herdando de `forms.Form`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 705:

**Linha 706 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 718 — Assign** (nível 1 do bloco).

Associa `tipo_sanguineo` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Tipo sanguineo'`, `required=False`, `choices=[('', 'Todos')] + [(tipo, tipo) for tipo in TIPOS_SANGUINEOS]`.

- `label='Tipo sanguineo'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `choices=[('', 'Todos')] + [(tipo, tipo) for tipo in TIPOS_SANGUINEOS]`: alternativas declaradas para validação e apresentação.

**Linha 726 — Assign** (nível 1 do bloco).

Associa `urgencia` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Urgencia'`, `required=False`, `choices=[('', 'Todas')] + list(PedidoSangue.Urgencia.choices)`.

- `label='Urgencia'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `choices=[('', 'Todas')] + list(PedidoSangue.Urgencia.choices)`: alternativas declaradas para validação e apresentação.

**Linha 732 — Assign** (nível 1 do bloco).

Associa `cidade` a a chamada `forms.CharField`; argumentos nomeados: `label='Cidade'`, `required=False`.

- `label='Cidade'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.

**Linha 737 — Assign** (nível 1 do bloco).

Associa `hemocentro` a a chamada `forms.CharField`; argumentos nomeados: `label='Hemocentro'`, `required=False`.

- `label='Hemocentro'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.

**Linha 742 — Assign** (nível 1 do bloco).

Associa `data` a a chamada `forms.DateField`; argumentos nomeados: `label='Data'`, `required=False`, `widget=forms.DateInput(attrs={'type': 'date'})`.

- `label='Data'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `widget=forms.DateInput(attrs={'type': 'date'})`: componente de entrada utilizado na tela.

**Linha 748 — Assign** (nível 1 do bloco).

Associa `status` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Status'`, `required=False`, `choices=[('', 'Todos')] + list(PedidoSangue.Status.choices)`.

- `label='Status'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `choices=[('', 'Todos')] + list(PedidoSangue.Status.choices)`: alternativas declaradas para validação e apresentação.

### FiltroEstoquePublicoForm — linhas 755 a 794

```python
class FiltroEstoquePublicoForm(forms.Form):
    """Filtros da consulta pública de estoques.

    A situação usa os códigos calculados pelo sistema. Os níveis mínimo e
    crítico continuam ocultos, pois são parâmetros internos do Hemocentro.
    """

    tipo_sanguineo = forms.ChoiceField(
        label="Tipo sanguíneo",
        required=False,
        choices=[("", "Todos")] + [(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
    )

    cidade = forms.CharField(
        label="Cidade",
        required=False,
    )

    hemocentro = forms.CharField(
        label="Hemocentro",
        required=False,
    )

    situacao = forms.ChoiceField(
        label="Situação do estoque",
        required=False,
        choices=[
            ("", "Todas"),
            ("CRITICO", "Crítico"),
            ("BAIXO", "Baixo"),
            ("ADEQUADO", "Adequado"),
            ("ALTO", "Alto"),
        ],
    )

    busca = forms.CharField(
        label="Busca",
        required=False,
        help_text="Nome do Hemocentro, cidade, UF ou tipo sanguíneo.",
    )
```

**Explicação deste trecho:**

**Linha 755 — ClassDef** (nível 0 do bloco).

Define a classe `FiltroEstoquePublicoForm` herdando de `forms.Form`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 755:

**Linha 756 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 762 — Assign** (nível 1 do bloco).

Associa `tipo_sanguineo` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Tipo sanguíneo'`, `required=False`, `choices=[('', 'Todos')] + [(tipo, tipo) for tipo in TIPOS_SANGUINEOS]`.

- `label='Tipo sanguíneo'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `choices=[('', 'Todos')] + [(tipo, tipo) for tipo in TIPOS_SANGUINEOS]`: alternativas declaradas para validação e apresentação.

**Linha 768 — Assign** (nível 1 do bloco).

Associa `cidade` a a chamada `forms.CharField`; argumentos nomeados: `label='Cidade'`, `required=False`.

- `label='Cidade'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.

**Linha 773 — Assign** (nível 1 do bloco).

Associa `hemocentro` a a chamada `forms.CharField`; argumentos nomeados: `label='Hemocentro'`, `required=False`.

- `label='Hemocentro'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.

**Linha 778 — Assign** (nível 1 do bloco).

Associa `situacao` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Situação do estoque'`, `required=False`, `choices=[('', 'Todas'), ('CRITICO', 'Crítico'), ('BAIXO', 'Baixo'), ('ADEQUADO', 'Adequado'), ('ALTO', 'Alto')]`.

- `label='Situação do estoque'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `choices=[('', 'Todas'), ('CRITICO', 'Crítico'), ('BAIXO', 'Baixo'), ('ADEQUADO', 'Adequado'), ('ALTO', 'Alto')]`: alternativas declaradas para validação e apresentação.

**Linha 790 — Assign** (nível 1 do bloco).

Associa `busca` a a chamada `forms.CharField`; argumentos nomeados: `label='Busca'`, `required=False`, `help_text='Nome do Hemocentro, cidade, UF ou tipo sanguíneo.'`.

- `label='Busca'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `help_text='Nome do Hemocentro, cidade, UF ou tipo sanguíneo.'`: orientação apresentada junto ao campo.

