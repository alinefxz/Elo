# accounts/views.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Entrada HTTP: permissoes, formularios, chamadas de servico e respostas/telas.

**Arquivo original:** [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""

Views do aplicativo accounts.

As views recebem requisicoes do navegador, executam a regra da pagina

e devolvem uma resposta.

Fluxo do cadastro:

GET  -> mostra formulario vazio.

POST -> valida -> grava usuario + consentimento -> cria sessao -> dashboard.

O cadastro usa uma transacao para impedir que apenas metade da operacao

seja salva. O dashboard usa login_required para bloquear visitantes.

"""

from django import forms

from django.contrib import messages

from django.contrib.auth import login

from django.contrib.auth.decorators import login_required

from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.utils import timezone

from django.db import transaction

from django.http import Http404, JsonResponse

from django.shortcuts import get_object_or_404, redirect, render

from django.views.decorators.http import require_POST

from django.db.models import Case, IntegerField, Prefetch, Value, When

from .forms import (
    CadastrarEstoqueForm,
    CadastroUsuarioForm,
    PreferenciaConvocacaoForm,
    MovimentarEstoqueForm,
    FiltroEstoquePublicoForm,
    PedidoSangueForm,
    FiltroPedidoSangueForm,
)
from .auditoria import registrar_auditoria

from .models import (
    ConsentimentoLGPD,
    Estoque,
    EstoqueMovimentacao,
    PedidoSangue,
    Triagem,
    Usuario,
    ValidacaoHemocentro,
    ValidacaoPedido,
    AuditoriaAcaoCritica,
)

from .estoque import (
    cadastrar_estoque,
    obter_estoques_publicos,
    registrar_movimentacao_estoque,
)

from .validacao_hemocentro import (
    aprovar_hemocentro as aprovar_hemocentro_servico,
    exigir_hemocentro_aprovado,
    validar_publicacao_hemocentro,
    hemocentro_aprovado,
    recusar_hemocentro as recusar_hemocentro_servico,
    solicitar_correcao_hemocentro as solicitar_correcao_hemocentro_servico,
    usuario_e_administrador,
)

from .compatibilidade import (
    TIPOS_SANGUINEOS,
    doadores_compativeis_para,
    tabela_de_compatibilidade,
    tipos_que_recebem_de,
    atualizar_preferencia_convocacao,
)
from django.conf import settings

from .triagem_servico import (
    TriagemExtensaNecessaria,
    TriagemIncompleta,
    PerguntaInvalida,
    TriagemSimplificadaIndisponivel,
    concluir_triagem,
    iniciar_triagem,
    obter_extensa_base,
    obter_extensa_reutilizavel,
    editar_pergunta,
    obter_pergunta_atual,
    pode_responder,
    salvar_resposta,
    voltar_pergunta,
)

from .triagem_forms import FormularioPergunta as FormularioPerguntaTriagem
from .triagem_catalogo import obter_pergunta

from .validacao_pedido import (
    aprovar_pedido as aprovar_pedido_servico,
    marcar_pedido_suspeito as marcar_pedido_suspeito_servico,
    recusar_pedido as recusar_pedido_servico,
    solicitar_correcao_pedido as solicitar_correcao_pedido_servico,
    criar_pedido_pendente,
)


class FormularioPergunta(forms.Form):
    """
    Formulario dinamico usado pela triagem por etapas.

    A pergunta vem da camada triagem_servico como um dicionario. O formulario
    aceita os formatos de resposta mais comuns do projeto sem obrigar cada
    pergunta a ter uma classe de formulario separada.
    """

    def __init__(self, pergunta, *args, valor_inicial=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.pergunta = pergunta

        texto = (
            pergunta.get("texto")
            or pergunta.get("pergunta")
            or pergunta.get("label")
            or "Resposta"
        )

        ajuda = (
            pergunta.get("explicacao")
            or pergunta.get("ajuda")
            or pergunta.get("help_text")
            or ""
        )

        obrigatoria = pergunta.get("obrigatoria", True)

        tipo = str(
            pergunta.get("tipo_resposta")
            or pergunta.get("tipo")
            or pergunta.get("formato")
            or "ESCOLHA"
        ).strip().upper()

        opcoes = self._normalizar_opcoes(
            pergunta.get("opcoes")
            or pergunta.get("alternativas")
            or pergunta.get("choices")
            or []
        )

        initial = self._normalizar_valor_inicial(valor_inicial)

        if opcoes:
            if tipo in {
                "MULTIPLAS",
                "MULTIPLA_SELECAO",
                "MULTIPLA_SELEÇÃO",
                "CHECKBOX",
                "CHECKBOXES",
            }:
                campo = forms.MultipleChoiceField(
                    label=texto,
                    choices=opcoes,
                    required=obrigatoria,
                    initial=initial,
                    help_text=ajuda,
                    widget=forms.CheckboxSelectMultiple,
                )
            else:
                campo = forms.ChoiceField(
                    label=texto,
                    choices=opcoes,
                    required=obrigatoria,
                    initial=initial,
                    help_text=ajuda,
                    widget=forms.RadioSelect,
                )

        elif tipo in {"SIM_NAO", "SIM/NÃO", "SIM/NAO", "BOOLEAN", "BOOL"}:
            campo = forms.ChoiceField(
                label=texto,
                choices=[
                    ("SIM", "Sim"),
                    ("NAO", "Não"),
                    ("NAO_SEI", "Não sei"),
                ],
                required=obrigatoria,
                initial=initial,
                help_text=ajuda,
                widget=forms.RadioSelect,
            )

        elif tipo in {"DATA", "DATE"}:
            campo = forms.DateField(
                label=texto,
                required=obrigatoria,
                initial=initial,
                help_text=ajuda,
                widget=forms.DateInput(attrs={"type": "date"}),
            )

        elif tipo in {
            "NUMERO",
            "NÚMERO",
            "NUMBER",
            "INTEIRO",
            "INTEGER",
            "DECIMAL",
        }:
            campo = forms.DecimalField(
                label=texto,
                required=obrigatoria,
                initial=initial,
                help_text=ajuda,
            )

        else:
            campo = forms.CharField(
                label=texto,
                required=obrigatoria,
                initial=initial,
                help_text=ajuda,
                max_length=pergunta.get("max_length", 500),
                widget=forms.Textarea(attrs={"rows": 3})
                if tipo in {"TEXTO", "TEXT", "TEXTAREA"}
                else forms.TextInput(),
            )

        self.fields["valor"] = campo

    @staticmethod
    def _primeiro_valor(dados, chaves):
        for chave in chaves:
            if chave in dados and dados[chave] is not None:
                return dados[chave]

        return None

    @classmethod
    def _normalizar_opcoes(cls, opcoes):
        """
        Converte opcoes em pares (valor, rotulo).

        Aceita:

        - lista de dicionarios;

        - lista de tuplas;

        - lista de textos;

        - dicionario no formato codigo -> rotulo.
        """

        if isinstance(opcoes, dict):
            return [
                (str(valor), str(rotulo))
                for valor, rotulo in opcoes.items()
            ]

        resultado = []

        for opcao in opcoes:
            if isinstance(opcao, dict):
                valor = cls._primeiro_valor(
                    opcao,
                    (
                        "codigo",
                        "codigo_resposta",
                        "valor",
                        "value",
                        "id",
                        "chave",
                    ),
                )

                rotulo = cls._primeiro_valor(
                    opcao,
                    (
                        "texto",
                        "resposta_label",
                        "label",
                        "rotulo",
                        "nome",
                    ),
                )

                if valor is None and rotulo is not None:
                    valor = rotulo

                if valor is not None:
                    resultado.append(
                        (
                            str(valor),
                            str(rotulo if rotulo is not None else valor),
                        )
                    )

            elif isinstance(opcao, (list, tuple)) and len(opcao) >= 2:
                resultado.append((str(opcao[0]), str(opcao[1])))

            else:
                resultado.append((str(opcao), str(opcao)))

        return resultado

    @classmethod
    def _normalizar_valor_inicial(cls, valor):
        if not isinstance(valor, dict):
            return valor

        return cls._primeiro_valor(
            valor,
            (
                "valor",
                "codigo",
                "codigo_resposta",
                "resposta",
                "opcao",
                "data",
                "numero",
                "texto",
            ),
        )


POSTOS_COLETA = [
    {
        "nome": "Hemocentro Central Elo",
        "cidade": "Sao Paulo",
        "estado": "SP",
        "endereco": "Av. Paulista, 1000",
        "horario": "Segunda a sexta, 8h as 17h",
    },
    {
        "nome": "Banco de Sangue Vida",
        "cidade": "Campinas",
        "estado": "SP",
        "endereco": "Rua das Flores, 250",
        "horario": "Segunda a sabado, 7h as 13h",
    },
    {
        "nome": "Unidade Hematologica Norte",
        "cidade": "Santos",
        "estado": "SP",
        "endereco": "Rua do Porto, 75",
        "horario": "Terca a sexta, 9h as 16h",
    },
]


ESTOQUE_GERAL = [
    {"tipo": "O-", "nivel": "Critico", "percentual": 18},
    {"tipo": "O+", "nivel": "Baixo", "percentual": 32},
    {"tipo": "A+", "nivel": "Estavel", "percentual": 64},
    {"tipo": "A-", "nivel": "Baixo", "percentual": 28},
    {"tipo": "B+", "nivel": "Estavel", "percentual": 58},
    {"tipo": "B-", "nivel": "Critico", "percentual": 16},
    {"tipo": "AB+", "nivel": "Estavel", "percentual": 70},
    {"tipo": "AB-", "nivel": "Baixo", "percentual": 25},
]


CAMPANHAS_ATIVAS = [
    {
        "titulo": "Mutirao de inverno",
        "cidade": "Sao Paulo",
        "data": "24/08/2026",
    },
    {
        "titulo": "Semana do doador universitario",
        "cidade": "Campinas",
        "data": "29/08/2026",
    },
]


PAINEIS_POR_PERFIL = {
    Usuario.Perfil.DOADOR: {
        "rotulo": "Doador",
        "titulo": "Painel do doador",
        "descricao": "Acompanhe sua jornada de doacao e encontre oportunidades para ajudar.",
        "acoes": [
            "Responder ou continuar a triagem de doacao.",
            "Ver campanhas de doacao ativas.",
            "Consultar pedidos de sangue em andamento.",
            "Consultar o estoque publico dos Hemocentros.",
            "Encontrar postos de coleta.",
            "Consultar a compatibilidade sanguinea.",
        ],
        "mostra_triagem": True,
        "mostra_campanhas": True,
        "mostra_pedidos": True,
        "mostra_estoque_publico": True,
        "mostra_postos": True,
    },
    Usuario.Perfil.RECEPTOR: {
        "rotulo": "Receptor / Solicitante",
        "titulo": "Painel do receptor",
        "descricao": "Acompanhe pedidos de sangue e consulte a disponibilidade publica.",
        "acoes": [
            "Ver estoque publico dos Hemocentros.",
            "Consultar pedidos de sangue ativos.",
            "Enviar solicitacao de pedido ao Hemocentro.",
            "Consultar a compatibilidade sanguinea.",
        ],
        "mostra_triagem": False,
        "mostra_campanhas": False,
        "mostra_pedidos": True,
        "mostra_estoque_publico": True,
        "mostra_postos": True,
    },
    Usuario.Perfil.OBSERVADOR: {
        "rotulo": "Observador",
        "titulo": "Painel do observador",
        "descricao": "Consulte informacoes publicas sobre campanhas, pedidos, postos e estoques.",
        "acoes": [
            "Ver estoque publico dos Hemocentros.",
            "Consultar postos de coleta.",
            "Acompanhar pedidos publicos.",
            "Acompanhar campanhas publicas.",
        ],
        "mostra_triagem": False,
        "mostra_campanhas": True,
        "mostra_pedidos": True,
        "mostra_estoque_publico": True,
        "mostra_postos": True,
    },
    Usuario.Perfil.HEMOCENTRO: {
        "rotulo": "Hemocentro",
        "titulo": "Painel do hemocentro",
        "descricao": "Acompanhe a validacao institucional e gerencie recursos liberados.",
        "acoes": [
            "Acompanhar o status da validacao institucional.",
            "Cadastrar estoque quando o cadastro estiver aprovado.",
            "Atualizar estoque quando o cadastro estiver aprovado.",
            "Consultar historico de movimentacoes de estoque.",
            "Analisar solicitações destinadas ao Hemocentro.",
        ],
        "mostra_triagem": False,
        "mostra_campanhas": False,
        "mostra_pedidos": True,
        "mostra_estoque_publico": False,
        "mostra_postos": False,
    },
    Usuario.Perfil.ADMINISTRADOR: {
        "rotulo": "Administrador",
        "titulo": "Painel administrativo",
        "descricao": "Gerencie validacoes institucionais e acompanhe operacoes sensiveis.",
        "acoes": [
            "Aprovar Hemocentros.",
            "Recusar Hemocentros.",
            "Solicitar correcao cadastral de Hemocentros.",
            "Acessar o painel administrativo do Django.",
        ],
        "mostra_triagem": False,
        "mostra_campanhas": True,
        "mostra_pedidos": True,
        "mostra_estoque_publico": True,
        "mostra_postos": False,
    },
}


def montar_visibilidade_dashboard(usuario, painel):
    """
    Centraliza a particularizacao do dashboard por perfil.

    O dicionario PAINEIS_POR_PERFIL define o que cada tipo de conta pode ver
    por padrao. Esta funcao acrescenta regras que dependem do estado atual do
    usuario, como Hemocentro aprovado e Administrador.
    """

    hemocentro_aprovado = (
        usuario.perfil == Usuario.Perfil.HEMOCENTRO
        and usuario.status_validacao == Usuario.StatusValidacaoHemocentro.APROVADO
    )

    administrador = usuario_e_administrador(usuario)

    return {
        "mostra_triagem": painel.get("mostra_triagem", False),
        "mostra_campanhas": painel.get("mostra_campanhas", False),
        "mostra_pedidos": painel.get("mostra_pedidos", False) and (
            usuario.perfil != Usuario.Perfil.HEMOCENTRO or hemocentro_aprovado
        ),
        "mostra_estoque_publico": painel.get("mostra_estoque_publico", False),
        "mostra_postos": painel.get("mostra_postos", False),
        "pode_solicitar_divulgacao": usuario.perfil == Usuario.Perfil.RECEPTOR,
        "mostra_status_hemocentro": usuario.perfil == Usuario.Perfil.HEMOCENTRO,
        "pode_solicitar_pedido": usuario.perfil == Usuario.Perfil.RECEPTOR,
        "pode_gerenciar_estoque": hemocentro_aprovado,
        "pode_analisar_pedidos": hemocentro_aprovado,
        "pode_aprovar_hemocentros": administrador,
        "pode_moderar_pedidos": administrador,
    }


def obter_ip(request):
    """Extrai o IP usado no registro do consentimento LGPD."""

    encaminhado = request.META.get("HTTP_X_FORWARDED_FOR")

    if encaminhado:
        return encaminhado.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


def filtrar_postos(consulta):
    """Filtra a lista publica por nome, cidade, estado ou endereco."""

    termo = (consulta or "").strip().lower()

    if not termo:
        return POSTOS_COLETA

    return [
        posto
        for posto in POSTOS_COLETA
        if termo
        in " ".join(
            [
                posto["nome"],
                posto["cidade"],
                posto["estado"],
                posto["endereco"],
            ]
        ).lower()
    ]


def exigir_administrador(usuario):
    """Bloqueia acoes institucionais para quem nao e administrador."""

    if not usuario_e_administrador(usuario):
        raise PermissionDenied(
            "Somente administradores podem executar esta acao."
        )


def obter_hemocentro_ou_404(id_hemocentro):
    """Busca somente contas cadastradas com perfil Hemocentro."""

    return get_object_or_404(
        Usuario,
        pk=id_hemocentro,
        perfil=Usuario.Perfil.HEMOCENTRO,
    )


def inicio(request):
    """Mostra o acesso publico usado pelo ator Visitante."""

    consulta = request.GET.get("q", "")

    contexto = {
        "consulta": consulta,
        "postos": filtrar_postos(consulta),
        "estoque_geral": ESTOQUE_GERAL,
        "pedidos_ativos": (
            PedidoSangue.objects
            .select_related("hemocentro_destino")
            .filter(status=PedidoSangue.Status.PUBLICADA)
            .order_by("-data_criacao")[:10]
        ),
    }

    return render(
        request,
        "accounts/inicio.html",
        contexto,
    )


def cadastro(request):
    """
    Exibe e processa o cadastro de usuarios.

    Hemocentro:

    - cria a conta;

    - fica com status PENDENTE;

    - registra consentimento LGPD;

    - entra no sistema;

    - recebe a mensagem de aguardando aprovacao.
    """

    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = CadastroUsuarioForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                usuario = form.save()

                # Todo Hemocentro novo deve comecar como PENDENTE.
                if usuario.perfil == Usuario.Perfil.HEMOCENTRO:
                    usuario.status_validacao = (
                        Usuario.StatusValidacaoHemocentro.PENDENTE
                    )

                    usuario.save(
                        update_fields=["status_validacao"]
                    )

                # Registro do aceite da LGPD.
                ConsentimentoLGPD.objects.create(
                    usuario=usuario,
                    tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL,
                    versao_termo="1.0",
                    aceito=True,
                    ip=obter_ip(request),
                )

                if usuario.perfil == Usuario.Perfil.DOADOR:
                    atualizar_preferencia_convocacao(
                        usuario, form.cleaned_data["aceita_notificacoes_pedidos"], request,
                    )

            # Cria a sessao do usuario.
            login(request, usuario)

            # Mensagem especifica para Hemocentro.
            if usuario.perfil == Usuario.Perfil.HEMOCENTRO:
                messages.success(
                    request,
                    (
                        "Cadastro realizado com sucesso! "
                        "Seu cadastro de Hemocentro esta aguardando "
                        "a aprovacao de um administrador."
                    ),
                )

            else:
                messages.success(
                    request,
                    "Cadastro realizado com sucesso.",
                )

            return redirect("accounts:dashboard")

        # Se o formulario tiver erro, permanece na pagina
        # e o template podera exibir os erros de cada campo.
        messages.error(
            request,
            (
                "O cadastro nao foi concluido. "
                "Corrija os erros destacados no formulario."
            ),
        )

    else:
        form = CadastroUsuarioForm()

    return render(
        request,
        "accounts/cadastro.html",
        {"form": form},
    )


def compatibilidade_sanguinea(request):
    """Exibe a tabela e a consulta de compatibilidade sanguinea."""

    tipo_selecionado = request.GET.get("tipo", "")

    compatibilidade_selecionada = None
    tipo_invalido = False

    if tipo_selecionado:
        tipo_selecionado = tipo_selecionado.strip().upper()

        try:
            compatibilidade_selecionada = {
                "tipo": tipo_selecionado,
                "doar_para": tipos_que_recebem_de(
                    tipo_selecionado
                ),
                "receber_de": doadores_compativeis_para(
                    tipo_selecionado
                ),
            }

        except ValueError:
            tipo_invalido = True

    return render(
        request,
        "accounts/compatibilidade_sanguinea.html",
        {
            "tipos_sanguineos": TIPOS_SANGUINEOS,
            "tipo_selecionado": tipo_selecionado,
            "compatibilidade_selecionada": compatibilidade_selecionada,
            "tipo_invalido": tipo_invalido,
            "tabela_compatibilidade": tabela_de_compatibilidade(),
        },
    )


@login_required
def dashboard(request):
    """Mostra o painel protegido particularizado pelo perfil do usuario."""

    if request.method == "POST":
        if request.POST.get("acao") == "marcar_notificacao_lida":
            try:
                id_notificacao = int(request.POST.get("id_notificacao", ""))
            except (TypeError, ValueError):
                raise Http404("Notificacao nao encontrada.")
            notificacao = get_object_or_404(
                request.user.notificacoes, pk=id_notificacao,
            )
            request.user.notificacoes.filter(pk=notificacao.pk, lida=False).update(
                lida=True, lida_em=timezone.now(),
            )
            return redirect("accounts:dashboard")
        if request.user.perfil != Usuario.Perfil.DOADOR:
            raise PermissionDenied("Somente Doadores podem configurar convocacoes.")
        form = PreferenciaConvocacaoForm(request.POST)
        if form.is_valid():
            atualizar_preferencia_convocacao(
                request.user, form.cleaned_data["aceita_convocacoes"], request,
            )
            messages.success(request, "Preferencia de convocacao salva.")
            return redirect("accounts:dashboard")

    preferencia_convocacao = None
    if request.user.perfil == Usuario.Perfil.DOADOR:
        consentimento_vigente = request.user.consentimentos_lgpd.filter(
            tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
            versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO,
            aceito=True, revogado_em__isnull=True,
        ).exists()
        preferencia_convocacao = PreferenciaConvocacaoForm(initial={
            "aceita_convocacoes": request.user.aceita_notificacoes_pedidos and consentimento_vigente,
        })

    painel = PAINEIS_POR_PERFIL.get(
        request.user.perfil,
        PAINEIS_POR_PERFIL[Usuario.Perfil.OBSERVADOR],
    )

    if request.user.perfil == Usuario.Perfil.HEMOCENTRO and not hemocentro_aprovado(request.user):
        painel = {**painel, "acoes": ["Acompanhar o status da validacao institucional."]}
    elif hemocentro_aprovado(request.user):
        painel = {**painel, "acoes": [*painel["acoes"], "Analisar e publicar solicitacoes destinadas ao proprio Hemocentro."]}

    # Busca a ultima analise administrativa do Hemocentro.
    validacao_atual = None

    if request.user.perfil == Usuario.Perfil.HEMOCENTRO:
        validacao_atual = (
            ValidacaoHemocentro.objects
            .filter(
                hemocentro=request.user
            )
            .order_by("-data_analise")
            .first()
        )

    # O resumo usa apenas registros do usuário autenticado. As respostas
    # detalhadas não são expostas no painel geral.
    ultima_triagem = None

    if pode_responder(request.user):
        ultima_triagem = request.user.triagens.order_by("-iniciada_em").first()

    visibilidade = montar_visibilidade_dashboard(
        request.user,
        painel,
    )

    notificacoes_usuario = request.user.notificacoes.order_by("-criada_em", "-pk")
    notificacoes_dashboard = Paginator(notificacoes_usuario, 10).get_page(
        request.GET.get("pagina_notificacoes"),
    )

    contexto = {
        "painel": painel,
        "visibilidade": visibilidade,
        "postos": POSTOS_COLETA,
        "estoque_geral": ESTOQUE_GERAL,
        "pedidos_ativos": (
            PedidoSangue.objects
            .select_related("hemocentro_destino")
            .filter(status=PedidoSangue.Status.PUBLICADA)
            .order_by("-data_criacao")[:10]
        ),
        "campanhas_ativas": CAMPANHAS_ATIVAS,
        "validacao_atual": validacao_atual,
        "ultima_triagem": ultima_triagem,
        "notificacoes_dashboard": notificacoes_dashboard,
        "notificacoes_nao_lidas": notificacoes_usuario.filter(lida=False).count(),
        "preferencia_convocacao": preferencia_convocacao,
        "convocacao_intervalo_horas": settings.CONVOCACAO_INTERVALO_HORAS,
        "convocacao_limite": settings.CONVOCACAO_LIMITE_NOTIFICACOES,
    }

    return render(
        request,
        "accounts/dashboard.html",
        contexto,
    )


@login_required
def painel_aprovacao_hemocentros(request):
    """Mostra a tela administrativa de aprovacao de Hemocentros."""

    exigir_administrador(request.user)

    hemocentros = (
        Usuario.objects
        .filter(
            perfil=Usuario.Perfil.HEMOCENTRO,
            status_validacao=(
                Usuario.StatusValidacaoHemocentro.PENDENTE
            ),
        )
        .order_by("date_joined")
    )

    contexto = {
        "hemocentros": hemocentros,
    }

    return render(
        request,
        "accounts/painel_aprovacao_hemocentros.html",
        contexto,
    )


@login_required
def hemocentros_pendentes(request):
    """Retorna os Hemocentros que ainda aguardam decisao administrativa."""

    exigir_administrador(request.user)

    hemocentros = (
        Usuario.objects
        .filter(
            perfil=Usuario.Perfil.HEMOCENTRO,
            status_validacao=(
                Usuario.StatusValidacaoHemocentro.PENDENTE
            ),
        )
        .order_by("date_joined")
    )

    dados = [
        {
            "id_hemocentro": hemocentro.pk,
            "nome": hemocentro.nome,
            "email": hemocentro.email,
            "cnpj": hemocentro.cnpj,
            "cidade": hemocentro.cidade,
            "estado": hemocentro.estado,
            "status_validacao": hemocentro.status_validacao,
            "data_cadastro": hemocentro.date_joined.isoformat(),
        }
        for hemocentro in hemocentros
    ]

    return JsonResponse(
        {
            "hemocentros": dados
        }
    )


@login_required
@require_POST
def aprovar_hemocentro(request, id_hemocentro):
    """Acao administrativa para aprovar um Hemocentro."""

    exigir_administrador(request.user)

    hemocentro = obter_hemocentro_ou_404(
        id_hemocentro
    )

    aprovar_hemocentro_servico(
        hemocentro=hemocentro,
        admin=request.user,
        parecer=request.POST.get("parecer", ""),
        request=request,
    )

    messages.success(
        request,
        "Hemocentro aprovado com sucesso.",
    )

    return redirect(
        "accounts:painel_aprovacao_hemocentros"
    )


@login_required
@require_POST
def recusar_hemocentro(request, id_hemocentro):
    """Acao administrativa para recusar um Hemocentro."""

    exigir_administrador(request.user)

    hemocentro = obter_hemocentro_ou_404(
        id_hemocentro
    )

    recusar_hemocentro_servico(
        hemocentro=hemocentro,
        admin=request.user,
        parecer=request.POST.get("parecer", ""),
        request=request,
    )

    messages.success(
        request,
        "Hemocentro recusado com sucesso.",
    )

    return redirect(
        "accounts:painel_aprovacao_hemocentros"
    )


@login_required
@require_POST
def solicitar_correcao_hemocentro(request, id_hemocentro):
    """Solicita correcao cadastral para um Hemocentro."""

    exigir_administrador(request.user)

    hemocentro = obter_hemocentro_ou_404(
        id_hemocentro
    )

    solicitar_correcao_hemocentro_servico(
        hemocentro=hemocentro,
        admin=request.user,
        parecer=request.POST.get("parecer", ""),
        request=request,
    )

    messages.success(
        request,
        "Solicitacao de correcao registrada com sucesso.",
    )

    return redirect(
        "accounts:painel_aprovacao_hemocentros"
    )


def triagem_apresentacao(request):
    """
    Exibe a apresentação pública da triagem.

    Somente usuários com perfil permitido podem iniciar a triagem.

    A modalidade simplificada é liberada quando existe uma triagem
    extensa concluída que possa ser utilizada como base.
    """

    pode_iniciar = False
    pode_simplificada = False
    triagem_em_andamento = None
    ultima_triagem = None
    extensa_base = None
    extensa_reutilizavel = None

    if request.user.is_authenticated:
        pode_iniciar = pode_responder(request.user)

        if pode_iniciar:
            triagens = (
                request.user.triagens
                .select_related("triagem_base")
                .order_by("-iniciada_em")
            )

            ultima_triagem = triagens.first()

            triagem_em_andamento = (
                triagens
                .filter(status=Triagem.Status.EM_ANDAMENTO)
                .first()
            )

            extensa_base = obter_extensa_base(request.user)
            extensa_reutilizavel = obter_extensa_reutilizavel(request.user)

            # A simplificada só fica disponível quando existe
            # uma triagem extensa concluída válida como base.
            pode_simplificada = extensa_base is not None

    return render(
        request,
        "accounts/triagem_apresentacao.html",
        {
            "pode_iniciar": pode_iniciar,
            "pode_simplificada": pode_simplificada,
            "triagem_em_andamento": triagem_em_andamento,
            "ultima_triagem": ultima_triagem,
            "triagem_extensa_base": extensa_base,
            "triagem_extensa_reutilizavel": extensa_reutilizavel,
        },
    )


@login_required
def triagem_historico(request):
    """
    Lista somente as triagens pertencentes ao usuario autenticado.

    O historico mostra tanto triagens em andamento quanto concluidas e
    canceladas, permitindo que o template ofereça continuar ou consultar
    o resultado conforme o status.
    """

    if not pode_responder(request.user):
        messages.error(
            request,
            "A triagem de doacao nao esta disponivel para este perfil.",
        )

        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.MODERACAO,
            resultado=AuditoriaAcaoCritica.Resultado.BLOQUEADO,
            usuario=request.user, request=request,
            descricao="Tentativa de acesso ao historico de triagens bloqueada.",
            metadados={"evento": "TENTATIVA_ACESSO", "rota": "accounts:triagem_historico"},
        )

        return redirect("accounts:dashboard")

    triagens = (
        request.user.triagens
        .select_related("triagem_base")
        .order_by("-iniciada_em")
    )

    return render(
        request,
        "accounts/triagem_historico.html",
        {
            "triagens": triagens,
        },
    )


@login_required
@require_POST
def triagem_iniciar(request, modalidade):
    """Inicia ou retoma uma triagem somente após clique explícito."""

    modalidades = {
        "extensa": Triagem.Modalidade.EXTENSA,
        "simplificada": Triagem.Modalidade.SIMPLIFICADA,
    }

    if modalidade not in modalidades:
        raise Http404("Modalidade de triagem inexistente.")

    if not pode_responder(request.user):
        raise PermissionDenied(
            "A triagem está disponível somente para Doador e Receptor."
        )

    if request.POST.get("aceite_termo") not in {"on", "1", "true"}:
        messages.error(
            request,
            "Leia e confirme o termo da pré-triagem para continuar.",
        )
        return redirect("accounts:triagem_apresentacao")

    try:
        triagem = iniciar_triagem(
            request.user,
            modalidades[modalidade],
            ip=obter_ip(request),
            aceite_termo=True,
            reutilizar_respostas=(
                modalidade == "extensa"
                and request.POST.get("reutilizar_respostas")
                in {"on", "1", "true"}
            ),
        )

    except TriagemSimplificadaIndisponivel:
        messages.info(
            request,
            "Conclua primeiro a triagem extensa para usar a versão simplificada.",
        )

        return redirect("accounts:triagem_apresentacao")

    return redirect(
        "accounts:triagem_pergunta",
        id_triagem=triagem.pk,
    )


def _triagem_do_usuario_ou_404(request, id_triagem):
    """Evita que uma conta consulte o questionário privado de outra."""

    if not pode_responder(request.user):
        raise PermissionDenied("Somente Doadores podem acessar a triagem.")

    return get_object_or_404(
        Triagem,
        pk=id_triagem,
        usuario=request.user,
    )


@login_required
def triagem_pergunta(request, id_triagem):
    """Mostra, valida e salva uma única pergunta por página."""

    triagem = _triagem_do_usuario_ou_404(
        request,
        id_triagem,
    )

    if triagem.status == Triagem.Status.CONCLUIDA:
        return redirect(
            "accounts:triagem_resultado",
            id_triagem=triagem.pk,
        )

    if triagem.status == Triagem.Status.CANCELADA:
        return redirect("accounts:triagem_apresentacao")

    pergunta_para_editar = request.GET.get("pergunta")
    if pergunta_para_editar:
        try:
            editar_pergunta(triagem, pergunta_para_editar)
        except PerguntaInvalida as erro:
            raise Http404("Pergunta de triagem inexistente.") from erro

    # O botão anterior muda apenas o cursor e não valida campos da página.
    if request.method == "POST" and request.POST.get("acao") == "anterior":
        voltar_pergunta(triagem)

        return redirect(
            "accounts:triagem_pergunta",
            id_triagem=triagem.pk,
        )

    pergunta = obter_pergunta_atual(triagem)

    if pergunta is None:
        return redirect("accounts:triagem_revisao", id_triagem=triagem.pk)

    resposta_anterior = triagem.respostas.filter(
        id_pergunta=pergunta["id"]
    ).first()

    valor_inicial = resposta_anterior.valor if resposta_anterior else None

    form = FormularioPerguntaTriagem(
        pergunta,
        request.POST or None,
        valor_inicial=valor_inicial,
    )

    if request.method == "POST" and form.is_valid():
        try:
            salvar_resposta(
                triagem,
                pergunta["id"],
                form.cleaned_data["valor"],
            )

        except TriagemExtensaNecessaria:
            # O serviço já cancelou a rápida antes de solicitar a troca.
            nova_extensa = iniciar_triagem(
                request.user,
                Triagem.Modalidade.EXTENSA,
                ip=obter_ip(request),
                aceite_termo=True,
            )

            messages.info(
                request,
                "Como o resumo mudou, continue pela triagem extensa.",
            )

            return redirect(
                "accounts:triagem_pergunta",
                id_triagem=nova_extensa.pk,
            )

        if request.POST.get("acao") == "salvar":
            messages.success(request, "Andamento da triagem salvo.")

            return redirect("accounts:triagem_historico")

        # O serviço mantém o cursor na explicação quando a pessoa não entendeu
        # e volta ao início quando ela escolhe revisar a confirmação final.
        if triagem.pergunta_atual >= len(triagem.fluxo_perguntas):
            return redirect("accounts:triagem_revisao", id_triagem=triagem.pk)

        return redirect(
            "accounts:triagem_pergunta",
            id_triagem=triagem.pk,
        )

    return render(
        request,
        "accounts/triagem_pergunta.html",
        {
            "triagem": triagem,
            "pergunta": pergunta,
            "form": form,
            "numero_pergunta": triagem.pergunta_atual + 1,
            "total_perguntas": len(triagem.fluxo_perguntas),
        },
    )


@login_required
def triagem_revisao(request, id_triagem):
    """Mostra todas as respostas antes do cálculo final."""

    triagem = _triagem_do_usuario_ou_404(request, id_triagem)
    if triagem.status == Triagem.Status.CONCLUIDA:
        return redirect("accounts:triagem_resultado", id_triagem=triagem.pk)
    if triagem.status == Triagem.Status.CANCELADA:
        return redirect("accounts:triagem_apresentacao")

    if request.method == "POST" and request.POST.get("acao") == "finalizar":
        try:
            triagem = concluir_triagem(triagem)
        except TriagemIncompleta as erro:
            messages.error(request, str(erro))
        else:
            return redirect("accounts:triagem_resultado", id_triagem=triagem.pk)

    respostas = []
    registros = triagem.respostas.order_by("id_resposta")
    for resposta in registros:
        try:
            pergunta = obter_pergunta(resposta.id_pergunta)
        except KeyError:
            continue
        respostas.append(
            {
                "id": resposta.id_pergunta,
                "titulo": pergunta["titulo"],
                "resposta": resposta.resposta_label,
                "detalhes": (resposta.valor or {}).get("detalhes", ""),
            }
        )

    return render(
        request,
        "accounts/triagem_revisao.html",
        {"triagem": triagem, "respostas_revisao": respostas},
    )


@login_required
def triagem_resultado(request, id_triagem):
    """Mostra a orientação concluída somente ao dono da triagem."""

    triagem = _triagem_do_usuario_ou_404(
        request,
        id_triagem,
    )

    if triagem.status == Triagem.Status.EM_ANDAMENTO:
        return redirect(
            "accounts:triagem_revisao",
            id_triagem=triagem.pk,
        )

    if triagem.status == Triagem.Status.CANCELADA:
        return redirect("accounts:triagem_historico")

    return render(
        request,
        "accounts/triagem_resultado.html",
        {
            "triagem": triagem,
        },
    )


def visualizacao_publica_estoque(request):
    """
    Exibe publicamente os estoques dos Hemocentros aprovados.

    A camada accounts.estoque devolve apenas os dados permitidos para
    exibicao publica, sem expor os limites internos usados pelo Hemocentro.
    """

    parametros = request.GET.copy()
    # Mantém compatibilidade com os parâmetros antigos da tela (q e tipo).
    if "q" in parametros and "busca" not in parametros:
        parametros["busca"] = parametros.get("q", "")
    if "tipo" in parametros and "tipo_sanguineo" not in parametros:
        parametros["tipo_sanguineo"] = parametros.get("tipo", "")
    if "status" in parametros and "situacao" not in parametros:
        parametros["situacao"] = parametros.get("status", "")

    form = FiltroEstoquePublicoForm(parametros or None)
    estoques = obter_estoques_publicos()

    if form.is_valid():
        tipo = form.cleaned_data.get("tipo_sanguineo")
        cidade = (form.cleaned_data.get("cidade") or "").strip().lower()
        hemocentro = (form.cleaned_data.get("hemocentro") or "").strip().lower()
        situacao = form.cleaned_data.get("situacao")
        busca = (form.cleaned_data.get("busca") or "").strip().lower()

        if tipo:
            estoques = [
                estoque for estoque in estoques
                if estoque["tipo_sanguineo"] == tipo
            ]

        if cidade:
            estoques = [
                estoque for estoque in estoques
                if cidade in estoque["cidade"].lower()
            ]

        if hemocentro:
            estoques = [
                estoque for estoque in estoques
                if hemocentro in estoque["nome"].lower()
            ]

        if situacao:
            estoques = [
                estoque for estoque in estoques
                if estoque["status_codigo"] == situacao
            ]

        if busca:
            estoques = [
                estoque for estoque in estoques
                if busca in " ".join(
                    [
                        estoque["nome"],
                        estoque["cidade"],
                        estoque["estado"],
                        estoque["tipo_sanguineo"],
                        estoque["status_label"],
                    ]
                ).lower()
            ]

    return render(
        request,
        "accounts/estoque_publico.html",
        {
            "estoques": estoques,
            "form": form,
        },
    )


def _formatar_erro_validacao(erro):
    """Converte um ValidationError (string, lista ou dict) em texto legivel."""

    if hasattr(erro, "message_dict"):
        return "; ".join(
            f"{campo}: {', '.join(mensagens)}"
            for campo, mensagens in erro.message_dict.items()
        )

    return "; ".join(erro.messages)


@login_required
@exigir_hemocentro_aprovado
def estoque_hemocentro(request):
    """
    UC_29 / UC_30 - Mostra o estoque do proprio Hemocentro logado e os
    formularios para cadastrar um novo tipo sanguineo ou movimentar um
    estoque ja existente.
    """

    estoques = (
        Estoque.objects
        .filter(hemocentro=request.user)
        .prefetch_related(
            Prefetch(
                "movimentacoes",
                queryset=EstoqueMovimentacao.objects.select_related(
                    "usuario_resp"
                ).order_by("-data_hora"),
            )
        )
        .order_by("tipo_sanguineo")
    )

    tipos_cadastrados = set(
        estoques.values_list("tipo_sanguineo", flat=True)
    )

    tipos_disponiveis = [
        tipo
        for tipo in TIPOS_SANGUINEOS
        if tipo not in tipos_cadastrados
    ]

    form_cadastro = CadastrarEstoqueForm()

    form_cadastro.fields["tipo_sanguineo"].choices = [
        (tipo, tipo)
        for tipo in tipos_disponiveis
    ]

    return render(
        request,
        "accounts/estoque_hemocentro.html",
        {
            "estoques": estoques,
            "tipos_disponiveis": tipos_disponiveis,
            "form_cadastro": form_cadastro,
            "form_movimentacao": MovimentarEstoqueForm(),
        },
    )


@login_required
@require_POST
@exigir_hemocentro_aprovado
def cadastrar_estoque_view(request):
    """UC_29 - Cria a estrutura de estoque de um tipo sanguineo."""

    form = CadastrarEstoqueForm(request.POST)

    if form.is_valid():
        try:
            cadastrar_estoque(
                hemocentro=request.user,
                tipo_sanguineo=form.cleaned_data["tipo_sanguineo"],
                quantidade_bolsas=form.cleaned_data["quantidade_bolsas"],
                nivel_minimo=form.cleaned_data["nivel_minimo"],
                nivel_critico=form.cleaned_data["nivel_critico"],
                request=request,
            )

        except ValidationError as erro:
            messages.error(
                request,
                _formatar_erro_validacao(erro),
            )

        else:
            messages.success(
                request,
                "Estoque cadastrado com sucesso.",
            )

    else:
        messages.error(
            request,
            "Corrija os erros destacados no formulario de cadastro.",
        )

    return redirect("accounts:estoque_hemocentro")


@login_required
@require_POST
@exigir_hemocentro_aprovado
def atualizar_estoque_view(request, id_estoque):
    """UC_30 - Registra uma entrada, saida ou ajuste em um estoque existente."""

    estoque = get_object_or_404(
        Estoque,
        pk=id_estoque,
    )

    form = MovimentarEstoqueForm(request.POST)

    if form.is_valid():
        try:
            registrar_movimentacao_estoque(
                estoque=estoque,
                usuario_resp=request.user,
                tipo_movimento=form.cleaned_data["tipo_movimento"],
                quantidade=form.cleaned_data["quantidade"],
                motivo=form.cleaned_data["motivo"],
                request=request,
            )

        except PermissionDenied as erro:
            messages.error(
                request,
                str(erro),
            )

        except ValidationError as erro:
            messages.error(
                request,
                _formatar_erro_validacao(erro),
            )

        else:
            messages.success(
                request,
                "Estoque atualizado com sucesso.",
            )

    else:
        messages.error(
            request,
            "Corrija os erros destacados no formulario de movimentacao.",
        )

    return redirect("accounts:estoque_hemocentro")


@login_required
def criar_pedido_sangue(request):
    """
    Recebe uma solicitação de divulgação, sem publicá-la.

    Apenas Receptor/Solicitante pode enviar solicitacao de pedido.

    Ao salvar, a solicitacao aguarda analise do Hemocentro.
    """

    if request.user.perfil != Usuario.Perfil.RECEPTOR:
        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.MODERACAO,
            resultado=AuditoriaAcaoCritica.Resultado.BLOQUEADO,
            usuario=request.user, request=request,
            descricao="Tentativa de enviar solicitacao de pedido bloqueada.",
            metadados={"evento": "TENTATIVA_ACESSO", "rota": "accounts:pedido_publicar"},
        )
        messages.error(
            request,
            "Este perfil não envia solicitações de divulgação.",
        )

        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = PedidoSangueForm(request.POST)

        if form.is_valid():
            try:
                pedido = criar_pedido_pendente(
                    dados=form.cleaned_data,
                    solicitante=(
                        request.user if request.user.is_authenticated else None
                    ),
                )

                mensagem = (
                    "Solicitação enviada para análise do Hemocentro. "
                    f"Protocolo {pedido.pk}."
                )
                if pedido.duplicidade_suspeita:
                    mensagem += " Há uma solicitação semelhante; ela será analisada."
                messages.success(request, mensagem)

                if request.user.is_authenticated:
                    return redirect("accounts:minhas_solicitacoes")
                return redirect("accounts:consultar_pedidos")

            except ValidationError as erro:
                form.add_error(None, erro)

    else:
        form = PedidoSangueForm()

    return render(
        request,
        "accounts/pedido_publicar.html",
        {
            "form": form,
        },
    )


@login_required
def minhas_solicitacoes(request):
    """Lista somente as solicitações enviadas pelo usuário autenticado."""

    solicitacoes = (
        PedidoSangue.objects
        .select_related("hemocentro_destino")
        .prefetch_related(
            Prefetch(
                "validacoes",
                queryset=ValidacaoPedido.objects.select_related("moderador"),
            )
        )
        .filter(solicitante=request.user)
        .order_by("-data_criacao")
    )

    status = request.GET.get("status")
    if status in dict(PedidoSangue.Status.choices):
        solicitacoes = solicitacoes.filter(status=status)

    return render(
        request,
        "accounts/minhas_solicitacoes.html",
        {
            "solicitacoes": solicitacoes,
            "status_opcoes": PedidoSangue.Status.choices,
            "status_atual": status or "",
        },
    )


@login_required
@exigir_hemocentro_aprovado
def painel_pedidos_hemocentro(request):
    """Fila de solicitações destinadas ao Hemocentro aprovado logado."""

    PedidoSangue.objects.filter(
        hemocentro_destino=request.user,
        status=PedidoSangue.Status.ENVIADA,
    ).update(status=PedidoSangue.Status.EM_ANALISE)

    solicitacoes = (
        PedidoSangue.objects
        .select_related("solicitante", "hemocentro_destino")
        .filter(hemocentro_destino=request.user)
        .exclude(status=PedidoSangue.Status.ENCERRADA)
        .order_by("-data_criacao")
    )
    status = request.GET.get("status")
    if status in dict(PedidoSangue.Status.choices):
        solicitacoes = solicitacoes.filter(status=status)

    return render(
        request,
        "accounts/painel_validacao_pedidos.html",
        {
            "solicitacoes": solicitacoes,
            "status_opcoes": PedidoSangue.Status.choices,
        },
    )


def consultar_pedidos(request):
    """
    UC_18 - Consultar Pedidos.

    Exibe apenas pedidos ativos e aplica filtros por tipo sanguineo,
    urgencia, cidade, hemocentro e data. A ordenacao prioriza urgencia
    e depois os mais recentes.
    """

    form = FiltroPedidoSangueForm(request.GET or None)

    pedidos = (
        PedidoSangue.objects
        .select_related("hemocentro_destino")
        .filter(
            status=PedidoSangue.Status.PUBLICADA,
            hemocentro_destino__perfil=Usuario.Perfil.HEMOCENTRO,
            hemocentro_destino__status_validacao=(
                Usuario.StatusValidacaoHemocentro.APROVADO
            ),
        )
    )

    if form.is_valid():
        tipo = form.cleaned_data.get("tipo_sanguineo")
        urgencia = form.cleaned_data.get("urgencia")
        cidade = form.cleaned_data.get("cidade")
        hemocentro = form.cleaned_data.get("hemocentro")
        data = form.cleaned_data.get("data")
        status = form.cleaned_data.get("status")

        # A consulta pública nunca pode revelar solicitações em análise,
        # recusadas ou dados ainda não publicados.
        if status and status != PedidoSangue.Status.PUBLICADA:
            pedidos = pedidos.none()

        if tipo:
            pedidos = pedidos.filter(tipo_sanguineo=tipo)

        if urgencia:
            pedidos = pedidos.filter(urgencia=urgencia)

        if cidade:
            pedidos = pedidos.filter(cidade__icontains=cidade)

        if hemocentro:
            pedidos = pedidos.filter(
                hemocentro_destino__nome__icontains=hemocentro
            )

        if data:
            pedidos = pedidos.filter(data_criacao__date=data)

    prioridade = Case(
        When(
            urgencia=PedidoSangue.Urgencia.CRITICA,
            then=Value(1),
        ),
        When(
            urgencia=PedidoSangue.Urgencia.ALTA,
            then=Value(2),
        ),
        When(
            urgencia=PedidoSangue.Urgencia.MEDIA,
            then=Value(3),
        ),
        When(
            urgencia=PedidoSangue.Urgencia.BAIXA,
            then=Value(4),
        ),
        default=Value(5),
        output_field=IntegerField(),
    )

    pedidos = pedidos.annotate(
        prioridade=prioridade
    ).order_by(
        "prioridade",
        "-data_criacao",
    )

    return render(
        request,
        "accounts/pedidos_listar.html",
        {
            "form": form,
            "pedidos": pedidos,
        },
    )


@login_required
def painel_validacao_pedidos(request):
    """Painel de moderação do Administrador, sem publicar pedidos."""

    exigir_administrador(request.user)

    pedidos = (
        PedidoSangue.objects
        .select_related("solicitante", "hemocentro_destino")
        .prefetch_related(
            Prefetch(
                "validacoes",
                queryset=ValidacaoPedido.objects.select_related("moderador"),
            )
        )
        .filter(
            status__in=[
                PedidoSangue.Status.ENVIADA,
                PedidoSangue.Status.EM_ANALISE,
                PedidoSangue.Status.CORRECAO_SOLICITADA,
                PedidoSangue.Status.PUBLICADA,
            ]
        )
        .order_by("-duplicidade_suspeita", "-data_criacao")
    )

    status = request.GET.get("status")
    if status in dict(PedidoSangue.Status.choices):
        pedidos = pedidos.filter(status=status)

    return render(
        request,
        "accounts/painel_moderacao_pedidos.html",
        {
            "pedidos": pedidos,
            "status_opcoes": PedidoSangue.Status.choices,
            "status_atual": status or "",
        },
    )


@login_required
@require_POST
def aprovar_pedido(request, id_pedido):
    """Publica uma solicitação após análise do Hemocentro de destino."""

    validar_publicacao_hemocentro(request.user)

    pedido = get_object_or_404(
        PedidoSangue,
        pk=id_pedido,
    )

    aprovar_pedido_servico(
        pedido=pedido,
        moderador=request.user,
        motivo=request.POST.get("motivo", ""),
        request=request,
    )

    messages.success(
        request,
        "Pedido publicado com sucesso." if hemocentro_aprovado(request.user)
        else "Pedido validado sem publicacao.",
    )

    return redirect("accounts:painel_pedidos_hemocentro")


@login_required
@require_POST
def recusar_pedido(request, id_pedido):
    """Recusa uma solicitação pelo Hemocentro de destino."""

    validar_publicacao_hemocentro(request.user)

    pedido = get_object_or_404(
        PedidoSangue,
        pk=id_pedido,
    )

    recusar_pedido_servico(
        pedido=pedido,
        moderador=request.user,
        motivo=request.POST.get("motivo", ""),
        request=request,
    )

    messages.success(
        request,
        "Pedido recusado com sucesso.",
    )

    return redirect("accounts:painel_pedidos_hemocentro")


@login_required
@require_POST
@exigir_hemocentro_aprovado
def solicitar_correcao_pedido(request, id_pedido):
    pedido = get_object_or_404(PedidoSangue, pk=id_pedido)
    solicitar_correcao_pedido_servico(
        pedido=pedido,
        moderador=request.user,
        motivo=request.POST.get("motivo", ""),
        request=request,
    )
    messages.success(request, "Correção solicitada ao responsável.")
    return redirect("accounts:painel_pedidos_hemocentro")


@login_required
@require_POST
def marcar_pedido_suspeito(request, id_pedido):
    """Registra uma suspeita para moderação, sem publicar o pedido."""

    pedido = get_object_or_404(PedidoSangue, pk=id_pedido)
    marcar_pedido_suspeito_servico(
        pedido=pedido,
        moderador=request.user,
        motivo=request.POST.get("motivo", ""),
        request=request,
    )
    messages.success(request, "Pedido marcado para moderação como suspeito.")

    if usuario_e_administrador(request.user):
        return redirect("accounts:painel_validacao_pedidos")
    return redirect("accounts:painel_pedidos_hemocentro")
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 19

```python
"""

Views do aplicativo accounts.

As views recebem requisicoes do navegador, executam a regra da pagina

e devolvem uma resposta.

Fluxo do cadastro:

GET  -> mostra formulario vazio.

POST -> valida -> grava usuario + consentimento -> cria sessao -> dashboard.

O cadastro usa uma transacao para impedir que apenas metade da operacao

seja salva. O dashboard usa login_required para bloquear visitantes.

"""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 21 a 21

```python
from django import forms
```

**Explicação deste trecho:**

**Linha 21 — ImportFrom** (nível 0 do bloco).

Importa de `django` os nomes `forms`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 23 a 23

```python
from django.contrib import messages
```

**Explicação deste trecho:**

**Linha 23 — ImportFrom** (nível 0 do bloco).

Importa de `django.contrib` os nomes `messages`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 25 a 25

```python
from django.contrib.auth import login
```

**Explicação deste trecho:**

**Linha 25 — ImportFrom** (nível 0 do bloco).

Importa de `django.contrib.auth` os nomes `login`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 27 a 27

```python
from django.contrib.auth.decorators import login_required
```

**Explicação deste trecho:**

**Linha 27 — ImportFrom** (nível 0 do bloco).

Importa de `django.contrib.auth.decorators` os nomes `login_required`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 29 a 29

```python
from django.core.exceptions import PermissionDenied, ValidationError
```

**Explicação deste trecho:**

**Linha 29 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.exceptions` os nomes `PermissionDenied`, `ValidationError`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 30 a 30

```python
from django.core.paginator import Paginator
```

**Explicação deste trecho:**

**Linha 30 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.paginator` os nomes `Paginator`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 31 a 31

```python
from django.utils import timezone
```

**Explicação deste trecho:**

**Linha 31 — ImportFrom** (nível 0 do bloco).

Importa de `django.utils` os nomes `timezone`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 33 a 33

```python
from django.db import transaction
```

**Explicação deste trecho:**

**Linha 33 — ImportFrom** (nível 0 do bloco).

Importa de `django.db` os nomes `transaction`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 35 a 35

```python
from django.http import Http404, JsonResponse
```

**Explicação deste trecho:**

**Linha 35 — ImportFrom** (nível 0 do bloco).

Importa de `django.http` os nomes `Http404`, `JsonResponse`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 37 a 37

```python
from django.shortcuts import get_object_or_404, redirect, render
```

**Explicação deste trecho:**

**Linha 37 — ImportFrom** (nível 0 do bloco).

Importa de `django.shortcuts` os nomes `get_object_or_404`, `redirect`, `render`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 39 a 39

```python
from django.views.decorators.http import require_POST
```

**Explicação deste trecho:**

**Linha 39 — ImportFrom** (nível 0 do bloco).

Importa de `django.views.decorators.http` os nomes `require_POST`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 41 a 41

```python
from django.db.models import Case, IntegerField, Prefetch, Value, When
```

**Explicação deste trecho:**

**Linha 41 — ImportFrom** (nível 0 do bloco).

Importa de `django.db.models` os nomes `Case`, `IntegerField`, `Prefetch`, `Value`, `When`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 43 a 51

```python
from .forms import (
    CadastrarEstoqueForm,
    CadastroUsuarioForm,
    PreferenciaConvocacaoForm,
    MovimentarEstoqueForm,
    FiltroEstoquePublicoForm,
    PedidoSangueForm,
    FiltroPedidoSangueForm,
)
```

**Explicação deste trecho:**

**Linha 43 — ImportFrom** (nível 0 do bloco).

Importa de `.forms` os nomes `CadastrarEstoqueForm`, `CadastroUsuarioForm`, `PreferenciaConvocacaoForm`, `MovimentarEstoqueForm`, `FiltroEstoquePublicoForm`, `PedidoSangueForm`, `FiltroPedidoSangueForm`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 52 a 52

```python
from .auditoria import registrar_auditoria
```

**Explicação deste trecho:**

**Linha 52 — ImportFrom** (nível 0 do bloco).

Importa de `.auditoria` os nomes `registrar_auditoria`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 54 a 64

```python
from .models import (
    ConsentimentoLGPD,
    Estoque,
    EstoqueMovimentacao,
    PedidoSangue,
    Triagem,
    Usuario,
    ValidacaoHemocentro,
    ValidacaoPedido,
    AuditoriaAcaoCritica,
)
```

**Explicação deste trecho:**

**Linha 54 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `ConsentimentoLGPD`, `Estoque`, `EstoqueMovimentacao`, `PedidoSangue`, `Triagem`, `Usuario`, `ValidacaoHemocentro`, `ValidacaoPedido`, `AuditoriaAcaoCritica`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 66 a 70

```python
from .estoque import (
    cadastrar_estoque,
    obter_estoques_publicos,
    registrar_movimentacao_estoque,
)
```

**Explicação deste trecho:**

**Linha 66 — ImportFrom** (nível 0 do bloco).

Importa de `.estoque` os nomes `cadastrar_estoque`, `obter_estoques_publicos`, `registrar_movimentacao_estoque`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 72 a 80

```python
from .validacao_hemocentro import (
    aprovar_hemocentro as aprovar_hemocentro_servico,
    exigir_hemocentro_aprovado,
    validar_publicacao_hemocentro,
    hemocentro_aprovado,
    recusar_hemocentro as recusar_hemocentro_servico,
    solicitar_correcao_hemocentro as solicitar_correcao_hemocentro_servico,
    usuario_e_administrador,
)
```

**Explicação deste trecho:**

**Linha 72 — ImportFrom** (nível 0 do bloco).

Importa de `.validacao_hemocentro` os nomes `aprovar_hemocentro` como `aprovar_hemocentro_servico`, `exigir_hemocentro_aprovado`, `validar_publicacao_hemocentro`, `hemocentro_aprovado`, `recusar_hemocentro` como `recusar_hemocentro_servico`, `solicitar_correcao_hemocentro` como `solicitar_correcao_hemocentro_servico`, `usuario_e_administrador`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 82 a 88

```python
from .compatibilidade import (
    TIPOS_SANGUINEOS,
    doadores_compativeis_para,
    tabela_de_compatibilidade,
    tipos_que_recebem_de,
    atualizar_preferencia_convocacao,
)
```

**Explicação deste trecho:**

**Linha 82 — ImportFrom** (nível 0 do bloco).

Importa de `.compatibilidade` os nomes `TIPOS_SANGUINEOS`, `doadores_compativeis_para`, `tabela_de_compatibilidade`, `tipos_que_recebem_de`, `atualizar_preferencia_convocacao`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 89 a 89

```python
from django.conf import settings
```

**Explicação deste trecho:**

**Linha 89 — ImportFrom** (nível 0 do bloco).

Importa de `django.conf` os nomes `settings`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 91 a 105

```python
from .triagem_servico import (
    TriagemExtensaNecessaria,
    TriagemIncompleta,
    PerguntaInvalida,
    TriagemSimplificadaIndisponivel,
    concluir_triagem,
    iniciar_triagem,
    obter_extensa_base,
    obter_extensa_reutilizavel,
    editar_pergunta,
    obter_pergunta_atual,
    pode_responder,
    salvar_resposta,
    voltar_pergunta,
)
```

**Explicação deste trecho:**

**Linha 91 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_servico` os nomes `TriagemExtensaNecessaria`, `TriagemIncompleta`, `PerguntaInvalida`, `TriagemSimplificadaIndisponivel`, `concluir_triagem`, `iniciar_triagem`, `obter_extensa_base`, `obter_extensa_reutilizavel`, `editar_pergunta`, `obter_pergunta_atual`, `pode_responder`, `salvar_resposta`, `voltar_pergunta`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 107 a 107

```python
from .triagem_forms import FormularioPergunta as FormularioPerguntaTriagem
```

**Explicação deste trecho:**

**Linha 107 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_forms` os nomes `FormularioPergunta` como `FormularioPerguntaTriagem`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 108 a 108

```python
from .triagem_catalogo import obter_pergunta
```

**Explicação deste trecho:**

**Linha 108 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_catalogo` os nomes `obter_pergunta`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 110 a 116

```python
from .validacao_pedido import (
    aprovar_pedido as aprovar_pedido_servico,
    marcar_pedido_suspeito as marcar_pedido_suspeito_servico,
    recusar_pedido as recusar_pedido_servico,
    solicitar_correcao_pedido as solicitar_correcao_pedido_servico,
    criar_pedido_pendente,
)
```

**Explicação deste trecho:**

**Linha 110 — ImportFrom** (nível 0 do bloco).

Importa de `.validacao_pedido` os nomes `aprovar_pedido` como `aprovar_pedido_servico`, `marcar_pedido_suspeito` como `marcar_pedido_suspeito_servico`, `recusar_pedido` como `recusar_pedido_servico`, `solicitar_correcao_pedido` como `solicitar_correcao_pedido_servico`, `criar_pedido_pendente`. Pontos iniciais indicam importação relativa ao pacote.

### FormularioPergunta — linhas 119 a 336

```python
class FormularioPergunta(forms.Form):
    """
    Formulario dinamico usado pela triagem por etapas.

    A pergunta vem da camada triagem_servico como um dicionario. O formulario
    aceita os formatos de resposta mais comuns do projeto sem obrigar cada
    pergunta a ter uma classe de formulario separada.
    """

    def __init__(self, pergunta, *args, valor_inicial=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.pergunta = pergunta

        texto = (
            pergunta.get("texto")
            or pergunta.get("pergunta")
            or pergunta.get("label")
            or "Resposta"
        )

        ajuda = (
            pergunta.get("explicacao")
            or pergunta.get("ajuda")
            or pergunta.get("help_text")
            or ""
        )

        obrigatoria = pergunta.get("obrigatoria", True)

        tipo = str(
            pergunta.get("tipo_resposta")
            or pergunta.get("tipo")
            or pergunta.get("formato")
            or "ESCOLHA"
        ).strip().upper()

        opcoes = self._normalizar_opcoes(
            pergunta.get("opcoes")
            or pergunta.get("alternativas")
            or pergunta.get("choices")
            or []
        )

        initial = self._normalizar_valor_inicial(valor_inicial)

        if opcoes:
            if tipo in {
                "MULTIPLAS",
                "MULTIPLA_SELECAO",
                "MULTIPLA_SELEÇÃO",
                "CHECKBOX",
                "CHECKBOXES",
            }:
                campo = forms.MultipleChoiceField(
                    label=texto,
                    choices=opcoes,
                    required=obrigatoria,
                    initial=initial,
                    help_text=ajuda,
                    widget=forms.CheckboxSelectMultiple,
                )
            else:
                campo = forms.ChoiceField(
                    label=texto,
                    choices=opcoes,
                    required=obrigatoria,
                    initial=initial,
                    help_text=ajuda,
                    widget=forms.RadioSelect,
                )

        elif tipo in {"SIM_NAO", "SIM/NÃO", "SIM/NAO", "BOOLEAN", "BOOL"}:
            campo = forms.ChoiceField(
                label=texto,
                choices=[
                    ("SIM", "Sim"),
                    ("NAO", "Não"),
                    ("NAO_SEI", "Não sei"),
                ],
                required=obrigatoria,
                initial=initial,
                help_text=ajuda,
                widget=forms.RadioSelect,
            )

        elif tipo in {"DATA", "DATE"}:
            campo = forms.DateField(
                label=texto,
                required=obrigatoria,
                initial=initial,
                help_text=ajuda,
                widget=forms.DateInput(attrs={"type": "date"}),
            )

        elif tipo in {
            "NUMERO",
            "NÚMERO",
            "NUMBER",
            "INTEIRO",
            "INTEGER",
            "DECIMAL",
        }:
            campo = forms.DecimalField(
                label=texto,
                required=obrigatoria,
                initial=initial,
                help_text=ajuda,
            )

        else:
            campo = forms.CharField(
                label=texto,
                required=obrigatoria,
                initial=initial,
                help_text=ajuda,
                max_length=pergunta.get("max_length", 500),
                widget=forms.Textarea(attrs={"rows": 3})
                if tipo in {"TEXTO", "TEXT", "TEXTAREA"}
                else forms.TextInput(),
            )

        self.fields["valor"] = campo

    @staticmethod
    def _primeiro_valor(dados, chaves):
        for chave in chaves:
            if chave in dados and dados[chave] is not None:
                return dados[chave]

        return None

    @classmethod
    def _normalizar_opcoes(cls, opcoes):
        """
        Converte opcoes em pares (valor, rotulo).

        Aceita:

        - lista de dicionarios;

        - lista de tuplas;

        - lista de textos;

        - dicionario no formato codigo -> rotulo.
        """

        if isinstance(opcoes, dict):
            return [
                (str(valor), str(rotulo))
                for valor, rotulo in opcoes.items()
            ]

        resultado = []

        for opcao in opcoes:
            if isinstance(opcao, dict):
                valor = cls._primeiro_valor(
                    opcao,
                    (
                        "codigo",
                        "codigo_resposta",
                        "valor",
                        "value",
                        "id",
                        "chave",
                    ),
                )

                rotulo = cls._primeiro_valor(
                    opcao,
                    (
                        "texto",
                        "resposta_label",
                        "label",
                        "rotulo",
                        "nome",
                    ),
                )

                if valor is None and rotulo is not None:
                    valor = rotulo

                if valor is not None:
                    resultado.append(
                        (
                            str(valor),
                            str(rotulo if rotulo is not None else valor),
                        )
                    )

            elif isinstance(opcao, (list, tuple)) and len(opcao) >= 2:
                resultado.append((str(opcao[0]), str(opcao[1])))

            else:
                resultado.append((str(opcao), str(opcao)))

        return resultado

    @classmethod
    def _normalizar_valor_inicial(cls, valor):
        if not isinstance(valor, dict):
            return valor

        return cls._primeiro_valor(
            valor,
            (
                "valor",
                "codigo",
                "codigo_resposta",
                "resposta",
                "opcao",
                "data",
                "numero",
                "texto",
            ),
        )
```

**Explicação deste trecho:**

**Linha 119 — ClassDef** (nível 0 do bloco).

Define a classe `FormularioPergunta` herdando de `forms.Form`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 119:

**Linha 120 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 128 — FunctionDef** (nível 1 do bloco).

Define `__init__(self, pergunta, *args, valor_inicial=None, **kwargs)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 128:

**Linha 129 — Expr** (nível 2 do bloco).

Executa a chamada `super().__init__`; argumentos posicionais: `*args`; argumentos nomeados: `**=kwargs`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 131 — Assign** (nível 2 do bloco).

Associa `self.pergunta` a o valor associado ao nome `pergunta`.

**Linha 133 — Assign** (nível 2 do bloco).

Associa `texto` a pelo menos uma das condições: `pergunta.get('texto')` ; `pergunta.get('pergunta')` ; `pergunta.get('label')` ; `'Resposta'` (com avaliação interrompida assim que o resultado é determinado).

**Linha 140 — Assign** (nível 2 do bloco).

Associa `ajuda` a pelo menos uma das condições: `pergunta.get('explicacao')` ; `pergunta.get('ajuda')` ; `pergunta.get('help_text')` ; `''` (com avaliação interrompida assim que o resultado é determinado).

**Linha 147 — Assign** (nível 2 do bloco).

Associa `obrigatoria` a a chamada `pergunta.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'obrigatoria'`, `True`.


**Linha 149 — Assign** (nível 2 do bloco).

Associa `tipo` a a chamada `str(pergunta.get('tipo_resposta') or pergunta.get('tipo') or pergunta.get('formato') or 'ESCOLHA').strip().upper`, que converte texto para maiúsculas.


**Linha 156 — Assign** (nível 2 do bloco).

Associa `opcoes` a a chamada `self._normalizar_opcoes`; argumentos posicionais: `pergunta.get('opcoes') or pergunta.get('alternativas') or pergunta.get('choices') or []`.


**Linha 163 — Assign** (nível 2 do bloco).

Associa `initial` a a chamada `self._normalizar_valor_inicial`; argumentos posicionais: `valor_inicial`.


**Linha 165 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `opcoes`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 165:

**Linha 166 — If** (nível 3 do bloco).

Escolhe um caminho verificando a comparação `tipo` contido em `{'MULTIPLAS', 'MULTIPLA_SELECAO', 'MULTIPLA_SELEÇÃO', 'CHECKBOX', 'CHECKBOXES'}`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 166:

**Linha 173 — Assign** (nível 4 do bloco).

Associa `campo` a a chamada `forms.MultipleChoiceField`; argumentos nomeados: `label=texto`, `choices=opcoes`, `required=obrigatoria`, `initial=initial`, `help_text=ajuda`, `widget=forms.CheckboxSelectMultiple`.

- `label=texto`: texto apresentado ao usuário.
- `choices=opcoes`: alternativas declaradas para validação e apresentação.
- `required=obrigatoria`: indica se o formulário exige preenchimento.
- `initial=initial`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `help_text=ajuda`: orientação apresentada junto ao campo.
- `widget=forms.CheckboxSelectMultiple`: componente de entrada utilizado na tela.

Bloco `orelse` da linha 166:

**Linha 182 — Assign** (nível 4 do bloco).

Associa `campo` a a chamada `forms.ChoiceField`; argumentos nomeados: `label=texto`, `choices=opcoes`, `required=obrigatoria`, `initial=initial`, `help_text=ajuda`, `widget=forms.RadioSelect`.

- `label=texto`: texto apresentado ao usuário.
- `choices=opcoes`: alternativas declaradas para validação e apresentação.
- `required=obrigatoria`: indica se o formulário exige preenchimento.
- `initial=initial`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `help_text=ajuda`: orientação apresentada junto ao campo.
- `widget=forms.RadioSelect`: componente de entrada utilizado na tela.

Bloco `orelse` da linha 165:

**Linha 191 — If** (nível 3 do bloco).

Escolhe um caminho verificando a comparação `tipo` contido em `{'SIM_NAO', 'SIM/NÃO', 'SIM/NAO', 'BOOLEAN', 'BOOL'}`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 191:

**Linha 192 — Assign** (nível 4 do bloco).

Associa `campo` a a chamada `forms.ChoiceField`; argumentos nomeados: `label=texto`, `choices=[('SIM', 'Sim'), ('NAO', 'Não'), ('NAO_SEI', 'Não sei')]`, `required=obrigatoria`, `initial=initial`, `help_text=ajuda`, `widget=forms.RadioSelect`.

- `label=texto`: texto apresentado ao usuário.
- `choices=[('SIM', 'Sim'), ('NAO', 'Não'), ('NAO_SEI', 'Não sei')]`: alternativas declaradas para validação e apresentação.
- `required=obrigatoria`: indica se o formulário exige preenchimento.
- `initial=initial`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `help_text=ajuda`: orientação apresentada junto ao campo.
- `widget=forms.RadioSelect`: componente de entrada utilizado na tela.

Bloco `orelse` da linha 191:

**Linha 205 — If** (nível 4 do bloco).

Escolhe um caminho verificando a comparação `tipo` contido em `{'DATA', 'DATE'}`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 205:

**Linha 206 — Assign** (nível 5 do bloco).

Associa `campo` a a chamada `forms.DateField`; argumentos nomeados: `label=texto`, `required=obrigatoria`, `initial=initial`, `help_text=ajuda`, `widget=forms.DateInput(attrs={'type': 'date'})`.

- `label=texto`: texto apresentado ao usuário.
- `required=obrigatoria`: indica se o formulário exige preenchimento.
- `initial=initial`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `help_text=ajuda`: orientação apresentada junto ao campo.
- `widget=forms.DateInput(attrs={'type': 'date'})`: componente de entrada utilizado na tela.

Bloco `orelse` da linha 205:

**Linha 214 — If** (nível 5 do bloco).

Escolhe um caminho verificando a comparação `tipo` contido em `{'NUMERO', 'NÚMERO', 'NUMBER', 'INTEIRO', 'INTEGER', 'DECIMAL'}`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 214:

**Linha 222 — Assign** (nível 6 do bloco).

Associa `campo` a a chamada `forms.DecimalField`; argumentos nomeados: `label=texto`, `required=obrigatoria`, `initial=initial`, `help_text=ajuda`.

- `label=texto`: texto apresentado ao usuário.
- `required=obrigatoria`: indica se o formulário exige preenchimento.
- `initial=initial`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `help_text=ajuda`: orientação apresentada junto ao campo.

Bloco `orelse` da linha 214:

**Linha 230 — Assign** (nível 6 do bloco).

Associa `campo` a a chamada `forms.CharField`; argumentos nomeados: `label=texto`, `required=obrigatoria`, `initial=initial`, `help_text=ajuda`, `max_length=pergunta.get('max_length', 500)`, `widget=forms.Textarea(attrs={'rows': 3}) if tipo in {'TEXTO', 'TEXT', 'TEXTAREA'} else forms.TextInput()`.

- `label=texto`: texto apresentado ao usuário.
- `required=obrigatoria`: indica se o formulário exige preenchimento.
- `initial=initial`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `help_text=ajuda`: orientação apresentada junto ao campo.
- `max_length=pergunta.get('max_length', 500)`: limite de comprimento do campo.
- `widget=forms.Textarea(attrs={'rows': 3}) if tipo in {'TEXTO', 'TEXT', 'TEXTAREA'} else forms.TextInput()`: componente de entrada utilizado na tela.

**Linha 241 — Assign** (nível 2 do bloco).

Associa `self.fields['valor']` a o valor associado ao nome `campo`.

**Linha 244 — FunctionDef** (nível 1 do bloco).

Define `_primeiro_valor(dados, chaves)`. O corpo só executa quando a função/método é chamado. Decoradores: `staticmethod`.

Bloco `body` da linha 244:

**Linha 245 — For** (nível 2 do bloco).

Percorre `chaves`; cada item é atribuído a `chave` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 245:

**Linha 246 — If** (nível 3 do bloco).

Escolhe um caminho verificando todas as condições: `chave in dados` ; `dados[chave] is not None` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 246:

**Linha 247 — Return** (nível 4 do bloco).

Encerra esta chamada e devolve o item ou recorte `chave` de `dados` ao chamador.

**Linha 249 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

**Linha 252 — FunctionDef** (nível 1 do bloco).

Define `_normalizar_opcoes(cls, opcoes)`. O corpo só executa quando a função/método é chamado. Decoradores: `classmethod`.

Bloco `body` da linha 252:

**Linha 253 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 267 — If** (nível 2 do bloco).

Escolhe um caminho verificando a chamada `isinstance`; argumentos posicionais: `opcoes`, `dict`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 267:

**Linha 268 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve uma coleção/gerador construído por compreensão em `[(str(valor), str(rotulo)) for valor, rotulo in opcoes.items()]`: percorre as fontes e aplica os filtros declarados ao chamador.

**Linha 273 — Assign** (nível 2 do bloco).

Associa `resultado` a uma coleção List com 0 itens, na expressão `[]`.

**Linha 275 — For** (nível 2 do bloco).

Percorre `opcoes`; cada item é atribuído a `opcao` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 275:

**Linha 276 — If** (nível 3 do bloco).

Escolhe um caminho verificando a chamada `isinstance`; argumentos posicionais: `opcao`, `dict`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 276:

**Linha 277 — Assign** (nível 4 do bloco).

Associa `valor` a a chamada `cls._primeiro_valor`; argumentos posicionais: `opcao`, `('codigo', 'codigo_resposta', 'valor', 'value', 'id', 'chave')`.


**Linha 289 — Assign** (nível 4 do bloco).

Associa `rotulo` a a chamada `cls._primeiro_valor`; argumentos posicionais: `opcao`, `('texto', 'resposta_label', 'label', 'rotulo', 'nome')`.


**Linha 300 — If** (nível 4 do bloco).

Escolhe um caminho verificando todas as condições: `valor is None` ; `rotulo is not None` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 300:

**Linha 301 — Assign** (nível 5 do bloco).

Associa `valor` a o valor associado ao nome `rotulo`.

**Linha 303 — If** (nível 4 do bloco).

Escolhe um caminho verificando a comparação `valor` um objeto diferente de `None`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 303:

**Linha 304 — Expr** (nível 5 do bloco).

Executa a chamada `resultado.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `(str(valor), str(rotulo if rotulo is not None else valor))`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 276:

**Linha 311 — If** (nível 4 do bloco).

Escolhe um caminho verificando todas as condições: `isinstance(opcao, (list, tuple))` ; `len(opcao) >= 2` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 311:

**Linha 312 — Expr** (nível 5 do bloco).

Executa a chamada `resultado.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `(str(opcao[0]), str(opcao[1]))`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 311:

**Linha 315 — Expr** (nível 5 do bloco).

Executa a chamada `resultado.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `(str(opcao), str(opcao))`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 317 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `resultado` ao chamador.

**Linha 320 — FunctionDef** (nível 1 do bloco).

Define `_normalizar_valor_inicial(cls, valor)`. O corpo só executa quando a função/método é chamado. Decoradores: `classmethod`.

Bloco `body` da linha 320:

**Linha 321 — If** (nível 2 do bloco).

Escolhe um caminho verificando a negação de `isinstance(valor, dict)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 321:

**Linha 322 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `valor` ao chamador.

**Linha 324 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `cls._primeiro_valor`; argumentos posicionais: `valor`, `('valor', 'codigo', 'codigo_resposta', 'resposta', 'opcao', 'data', 'numero', 'texto')` ao chamador.

### Assign — linhas 339 a 361

```python
POSTOS_COLETA = [
    {
        "nome": "Hemocentro Central Elo",
        "cidade": "Sao Paulo",
        "estado": "SP",
        "endereco": "Av. Paulista, 1000",
        "horario": "Segunda a sexta, 8h as 17h",
    },
    {
        "nome": "Banco de Sangue Vida",
        "cidade": "Campinas",
        "estado": "SP",
        "endereco": "Rua das Flores, 250",
        "horario": "Segunda a sabado, 7h as 13h",
    },
    {
        "nome": "Unidade Hematologica Norte",
        "cidade": "Santos",
        "estado": "SP",
        "endereco": "Rua do Porto, 75",
        "horario": "Terca a sexta, 9h as 16h",
    },
]
```

**Explicação deste trecho:**

**Linha 339 — Assign** (nível 0 do bloco).

Associa `POSTOS_COLETA` a uma coleção List com 3 itens, na expressão `[{'nome': 'Hemocentro Central Elo', 'cidade': 'Sao Paulo', 'estado': 'SP', 'endereco': 'Av. Paulista, 1000', 'horario': 'Segunda a sexta, 8h as 17h'}, {'nome': 'Banco de Sangue Vida', 'cidade': 'Campinas', 'estado': 'SP', 'endereco': 'Rua das Flores, 250', 'horario': 'Segunda a sabado, 7h as 13h'}, {'nome': 'Unidade Hematologica Norte', 'cidade': 'Santos', 'estado': 'SP', 'endereco': 'Rua do Porto, 75', 'horario': 'Terca a sexta, 9h as 16h'}]`.

### Assign — linhas 364 a 373

```python
ESTOQUE_GERAL = [
    {"tipo": "O-", "nivel": "Critico", "percentual": 18},
    {"tipo": "O+", "nivel": "Baixo", "percentual": 32},
    {"tipo": "A+", "nivel": "Estavel", "percentual": 64},
    {"tipo": "A-", "nivel": "Baixo", "percentual": 28},
    {"tipo": "B+", "nivel": "Estavel", "percentual": 58},
    {"tipo": "B-", "nivel": "Critico", "percentual": 16},
    {"tipo": "AB+", "nivel": "Estavel", "percentual": 70},
    {"tipo": "AB-", "nivel": "Baixo", "percentual": 25},
]
```

**Explicação deste trecho:**

**Linha 364 — Assign** (nível 0 do bloco).

Associa `ESTOQUE_GERAL` a uma coleção List com 8 itens, na expressão `[{'tipo': 'O-', 'nivel': 'Critico', 'percentual': 18}, {'tipo': 'O+', 'nivel': 'Baixo', 'percentual': 32}, {'tipo': 'A+', 'nivel': 'Estavel', 'percentual': 64}, {'tipo': 'A-', 'nivel': 'Baixo', 'percentual': 28}, {'tipo': 'B+', 'nivel': 'Estavel', 'percentual': 58}, {'tipo': 'B-', 'nivel': 'Critico', 'percentual': 16}, {'tipo': 'AB+', 'nivel': 'Estavel', 'percentual': 70}, {'tipo': 'AB-', 'nivel': 'Baixo', 'percentual': 25}]`.

### Assign — linhas 376 a 387

```python
CAMPANHAS_ATIVAS = [
    {
        "titulo": "Mutirao de inverno",
        "cidade": "Sao Paulo",
        "data": "24/08/2026",
    },
    {
        "titulo": "Semana do doador universitario",
        "cidade": "Campinas",
        "data": "29/08/2026",
    },
]
```

**Explicação deste trecho:**

**Linha 376 — Assign** (nível 0 do bloco).

Associa `CAMPANHAS_ATIVAS` a uma coleção List com 2 itens, na expressão `[{'titulo': 'Mutirao de inverno', 'cidade': 'Sao Paulo', 'data': '24/08/2026'}, {'titulo': 'Semana do doador universitario', 'cidade': 'Campinas', 'data': '29/08/2026'}]`.

### Assign — linhas 390 a 474

```python
PAINEIS_POR_PERFIL = {
    Usuario.Perfil.DOADOR: {
        "rotulo": "Doador",
        "titulo": "Painel do doador",
        "descricao": "Acompanhe sua jornada de doacao e encontre oportunidades para ajudar.",
        "acoes": [
            "Responder ou continuar a triagem de doacao.",
            "Ver campanhas de doacao ativas.",
            "Consultar pedidos de sangue em andamento.",
            "Consultar o estoque publico dos Hemocentros.",
            "Encontrar postos de coleta.",
            "Consultar a compatibilidade sanguinea.",
        ],
        "mostra_triagem": True,
        "mostra_campanhas": True,
        "mostra_pedidos": True,
        "mostra_estoque_publico": True,
        "mostra_postos": True,
    },
    Usuario.Perfil.RECEPTOR: {
        "rotulo": "Receptor / Solicitante",
        "titulo": "Painel do receptor",
        "descricao": "Acompanhe pedidos de sangue e consulte a disponibilidade publica.",
        "acoes": [
            "Ver estoque publico dos Hemocentros.",
            "Consultar pedidos de sangue ativos.",
            "Enviar solicitacao de pedido ao Hemocentro.",
            "Consultar a compatibilidade sanguinea.",
        ],
        "mostra_triagem": False,
        "mostra_campanhas": False,
        "mostra_pedidos": True,
        "mostra_estoque_publico": True,
        "mostra_postos": True,
    },
    Usuario.Perfil.OBSERVADOR: {
        "rotulo": "Observador",
        "titulo": "Painel do observador",
        "descricao": "Consulte informacoes publicas sobre campanhas, pedidos, postos e estoques.",
        "acoes": [
            "Ver estoque publico dos Hemocentros.",
            "Consultar postos de coleta.",
            "Acompanhar pedidos publicos.",
            "Acompanhar campanhas publicas.",
        ],
        "mostra_triagem": False,
        "mostra_campanhas": True,
        "mostra_pedidos": True,
        "mostra_estoque_publico": True,
        "mostra_postos": True,
    },
    Usuario.Perfil.HEMOCENTRO: {
        "rotulo": "Hemocentro",
        "titulo": "Painel do hemocentro",
        "descricao": "Acompanhe a validacao institucional e gerencie recursos liberados.",
        "acoes": [
            "Acompanhar o status da validacao institucional.",
            "Cadastrar estoque quando o cadastro estiver aprovado.",
            "Atualizar estoque quando o cadastro estiver aprovado.",
            "Consultar historico de movimentacoes de estoque.",
            "Analisar solicitações destinadas ao Hemocentro.",
        ],
        "mostra_triagem": False,
        "mostra_campanhas": False,
        "mostra_pedidos": True,
        "mostra_estoque_publico": False,
        "mostra_postos": False,
    },
    Usuario.Perfil.ADMINISTRADOR: {
        "rotulo": "Administrador",
        "titulo": "Painel administrativo",
        "descricao": "Gerencie validacoes institucionais e acompanhe operacoes sensiveis.",
        "acoes": [
            "Aprovar Hemocentros.",
            "Recusar Hemocentros.",
            "Solicitar correcao cadastral de Hemocentros.",
            "Acessar o painel administrativo do Django.",
        ],
        "mostra_triagem": False,
        "mostra_campanhas": True,
        "mostra_pedidos": True,
        "mostra_estoque_publico": True,
        "mostra_postos": False,
    },
}
```

**Explicação deste trecho:**

**Linha 390 — Assign** (nível 0 do bloco).

Associa `PAINEIS_POR_PERFIL` a um dicionário de 5 entradas; as chaves dão nome aos valores associados.

- Chave `Usuario.Perfil.DOADOR`: recebe um dicionário de 9 entradas; as chaves dão nome aos valores associados.
- Chave `Usuario.Perfil.RECEPTOR`: recebe um dicionário de 9 entradas; as chaves dão nome aos valores associados.
- Chave `Usuario.Perfil.OBSERVADOR`: recebe um dicionário de 9 entradas; as chaves dão nome aos valores associados.
- Chave `Usuario.Perfil.HEMOCENTRO`: recebe um dicionário de 9 entradas; as chaves dão nome aos valores associados.
- Chave `Usuario.Perfil.ADMINISTRADOR`: recebe um dicionário de 9 entradas; as chaves dão nome aos valores associados.

### montar_visibilidade_dashboard — linhas 477 a 508

```python
def montar_visibilidade_dashboard(usuario, painel):
    """
    Centraliza a particularizacao do dashboard por perfil.

    O dicionario PAINEIS_POR_PERFIL define o que cada tipo de conta pode ver
    por padrao. Esta funcao acrescenta regras que dependem do estado atual do
    usuario, como Hemocentro aprovado e Administrador.
    """

    hemocentro_aprovado = (
        usuario.perfil == Usuario.Perfil.HEMOCENTRO
        and usuario.status_validacao == Usuario.StatusValidacaoHemocentro.APROVADO
    )

    administrador = usuario_e_administrador(usuario)

    return {
        "mostra_triagem": painel.get("mostra_triagem", False),
        "mostra_campanhas": painel.get("mostra_campanhas", False),
        "mostra_pedidos": painel.get("mostra_pedidos", False) and (
            usuario.perfil != Usuario.Perfil.HEMOCENTRO or hemocentro_aprovado
        ),
        "mostra_estoque_publico": painel.get("mostra_estoque_publico", False),
        "mostra_postos": painel.get("mostra_postos", False),
        "pode_solicitar_divulgacao": usuario.perfil == Usuario.Perfil.RECEPTOR,
        "mostra_status_hemocentro": usuario.perfil == Usuario.Perfil.HEMOCENTRO,
        "pode_solicitar_pedido": usuario.perfil == Usuario.Perfil.RECEPTOR,
        "pode_gerenciar_estoque": hemocentro_aprovado,
        "pode_analisar_pedidos": hemocentro_aprovado,
        "pode_aprovar_hemocentros": administrador,
        "pode_moderar_pedidos": administrador,
    }
```

**Explicação deste trecho:**

**Linha 477 — FunctionDef** (nível 0 do bloco).

Define `montar_visibilidade_dashboard(usuario, painel)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 477:

**Linha 478 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 486 — Assign** (nível 1 do bloco).

Associa `hemocentro_aprovado` a todas as condições: `usuario.perfil == Usuario.Perfil.HEMOCENTRO` ; `usuario.status_validacao == Usuario.StatusValidacaoHemocentro.APROVADO` (com avaliação interrompida assim que o resultado é determinado).

**Linha 491 — Assign** (nível 1 do bloco).

Associa `administrador` a a chamada `usuario_e_administrador`; argumentos posicionais: `usuario`.


**Linha 493 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve um dicionário de 12 entradas; as chaves dão nome aos valores associados ao chamador.

### obter_ip — linhas 511 a 519

```python
def obter_ip(request):
    """Extrai o IP usado no registro do consentimento LGPD."""

    encaminhado = request.META.get("HTTP_X_FORWARDED_FOR")

    if encaminhado:
        return encaminhado.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")
```

**Explicação deste trecho:**

**Linha 511 — FunctionDef** (nível 0 do bloco).

Define `obter_ip(request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 511:

**Linha 512 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 514 — Assign** (nível 1 do bloco).

Associa `encaminhado` a a chamada `request.META.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'HTTP_X_FORWARDED_FOR'`.


**Linha 516 — If** (nível 1 do bloco).

Escolhe um caminho verificando o valor associado ao nome `encaminhado`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 516:

**Linha 517 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `encaminhado.split(',')[0].strip`, que remove espaços nas extremidades do texto ao chamador.

**Linha 519 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `request.META.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'REMOTE_ADDR'` ao chamador.

### filtrar_postos — linhas 522 a 542

```python
def filtrar_postos(consulta):
    """Filtra a lista publica por nome, cidade, estado ou endereco."""

    termo = (consulta or "").strip().lower()

    if not termo:
        return POSTOS_COLETA

    return [
        posto
        for posto in POSTOS_COLETA
        if termo
        in " ".join(
            [
                posto["nome"],
                posto["cidade"],
                posto["estado"],
                posto["endereco"],
            ]
        ).lower()
    ]
```

**Explicação deste trecho:**

**Linha 522 — FunctionDef** (nível 0 do bloco).

Define `filtrar_postos(consulta)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 522:

**Linha 523 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 525 — Assign** (nível 1 do bloco).

Associa `termo` a a chamada `(consulta or '').strip().lower`, que converte texto para minúsculas.


**Linha 527 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `termo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 527:

**Linha 528 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `POSTOS_COLETA` ao chamador.

**Linha 530 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve uma coleção/gerador construído por compreensão em `[posto for posto in POSTOS_COLETA if termo in ' '.join([posto['nome'], posto['cidade'], posto['estado'], posto['endereco']]).lower()]`: percorre as fontes e aplica os filtros declarados ao chamador.

### exigir_administrador — linhas 545 a 551

```python
def exigir_administrador(usuario):
    """Bloqueia acoes institucionais para quem nao e administrador."""

    if not usuario_e_administrador(usuario):
        raise PermissionDenied(
            "Somente administradores podem executar esta acao."
        )
```

**Explicação deste trecho:**

**Linha 545 — FunctionDef** (nível 0 do bloco).

Define `exigir_administrador(usuario)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 545:

**Linha 546 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 548 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `usuario_e_administrador(usuario)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 548:

**Linha 549 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'Somente administradores podem executar esta acao.'`.

### obter_hemocentro_ou_404 — linhas 554 a 561

```python
def obter_hemocentro_ou_404(id_hemocentro):
    """Busca somente contas cadastradas com perfil Hemocentro."""

    return get_object_or_404(
        Usuario,
        pk=id_hemocentro,
        perfil=Usuario.Perfil.HEMOCENTRO,
    )
```

**Explicação deste trecho:**

**Linha 554 — FunctionDef** (nível 0 do bloco).

Define `obter_hemocentro_ou_404(id_hemocentro)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 554:

**Linha 555 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 557 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `get_object_or_404`, que busca um objeto na consulta fornecida; ausência gera resposta 404; argumentos posicionais: `Usuario`; argumentos nomeados: `pk=id_hemocentro`, `perfil=Usuario.Perfil.HEMOCENTRO` ao chamador.

### inicio — linhas 564 a 585

```python
def inicio(request):
    """Mostra o acesso publico usado pelo ator Visitante."""

    consulta = request.GET.get("q", "")

    contexto = {
        "consulta": consulta,
        "postos": filtrar_postos(consulta),
        "estoque_geral": ESTOQUE_GERAL,
        "pedidos_ativos": (
            PedidoSangue.objects
            .select_related("hemocentro_destino")
            .filter(status=PedidoSangue.Status.PUBLICADA)
            .order_by("-data_criacao")[:10]
        ),
    }

    return render(
        request,
        "accounts/inicio.html",
        contexto,
    )
```

**Explicação deste trecho:**

**Linha 564 — FunctionDef** (nível 0 do bloco).

Define `inicio(request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 564:

**Linha 565 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 567 — Assign** (nível 1 do bloco).

Associa `consulta` a a chamada `request.GET.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'q'`, `''`.


**Linha 569 — Assign** (nível 1 do bloco).

Associa `contexto` a um dicionário de 4 entradas; as chaves dão nome aos valores associados.

- Chave `'consulta'`: recebe o valor associado ao nome `consulta`.
- Chave `'postos'`: recebe a chamada `filtrar_postos`; argumentos posicionais: `consulta`.
- Chave `'estoque_geral'`: recebe o valor associado ao nome `ESTOQUE_GERAL`.
- Chave `'pedidos_ativos'`: recebe o item ou recorte `:10` de `PedidoSangue.objects.select_related('hemocentro_destino').filter(status=PedidoSangue.Status.PUBLICADA).order_by('-data_criacao')`.

**Linha 581 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/inicio.html'`, `contexto` ao chamador.

### cadastro — linhas 588 a 678

```python
def cadastro(request):
    """
    Exibe e processa o cadastro de usuarios.

    Hemocentro:

    - cria a conta;

    - fica com status PENDENTE;

    - registra consentimento LGPD;

    - entra no sistema;

    - recebe a mensagem de aguardando aprovacao.
    """

    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = CadastroUsuarioForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                usuario = form.save()

                # Todo Hemocentro novo deve comecar como PENDENTE.
                if usuario.perfil == Usuario.Perfil.HEMOCENTRO:
                    usuario.status_validacao = (
                        Usuario.StatusValidacaoHemocentro.PENDENTE
                    )

                    usuario.save(
                        update_fields=["status_validacao"]
                    )

                # Registro do aceite da LGPD.
                ConsentimentoLGPD.objects.create(
                    usuario=usuario,
                    tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL,
                    versao_termo="1.0",
                    aceito=True,
                    ip=obter_ip(request),
                )

                if usuario.perfil == Usuario.Perfil.DOADOR:
                    atualizar_preferencia_convocacao(
                        usuario, form.cleaned_data["aceita_notificacoes_pedidos"], request,
                    )

            # Cria a sessao do usuario.
            login(request, usuario)

            # Mensagem especifica para Hemocentro.
            if usuario.perfil == Usuario.Perfil.HEMOCENTRO:
                messages.success(
                    request,
                    (
                        "Cadastro realizado com sucesso! "
                        "Seu cadastro de Hemocentro esta aguardando "
                        "a aprovacao de um administrador."
                    ),
                )

            else:
                messages.success(
                    request,
                    "Cadastro realizado com sucesso.",
                )

            return redirect("accounts:dashboard")

        # Se o formulario tiver erro, permanece na pagina
        # e o template podera exibir os erros de cada campo.
        messages.error(
            request,
            (
                "O cadastro nao foi concluido. "
                "Corrija os erros destacados no formulario."
            ),
        )

    else:
        form = CadastroUsuarioForm()

    return render(
        request,
        "accounts/cadastro.html",
        {"form": form},
    )
```

**Explicação deste trecho:**

**Linha 588 — FunctionDef** (nível 0 do bloco).

Define `cadastro(request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 588:

**Linha 589 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 605 — If** (nível 1 do bloco).

Escolhe um caminho verificando o atributo `is_authenticated` de `request.user`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 605:

**Linha 606 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:dashboard'` ao chamador.

**Linha 608 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `request.method` igual a `'POST'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 608:

**Linha 609 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `CadastroUsuarioForm`; argumentos posicionais: `request.POST`.


**Linha 611 — If** (nível 2 do bloco).

Escolhe um caminho verificando a chamada `form.is_valid`, que valida o formulário e disponibiliza cleaned_data quando válido. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 611:

**Linha 612 — With** (nível 3 do bloco).

Executa sob os contextos `transaction.atomic()`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 612:

**Linha 613 — Assign** (nível 4 do bloco).

Associa `usuario` a a chamada `form.save`, que persiste a instância; update_fields limita os campos gravados.


**Linha 616 — If** (nível 4 do bloco).

Escolhe um caminho verificando a comparação `usuario.perfil` igual a `Usuario.Perfil.HEMOCENTRO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 616:

**Linha 617 — Assign** (nível 5 do bloco).

Associa `usuario.status_validacao` a o atributo `PENDENTE` de `Usuario.StatusValidacaoHemocentro`.

**Linha 621 — Expr** (nível 5 do bloco).

Executa a chamada `usuario.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['status_validacao']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 626 — Expr** (nível 4 do bloco).

Executa a chamada `ConsentimentoLGPD.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=usuario`, `tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL`, `versao_termo='1.0'`, `aceito=True`, `ip=obter_ip(request)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 634 — If** (nível 4 do bloco).

Escolhe um caminho verificando a comparação `usuario.perfil` igual a `Usuario.Perfil.DOADOR`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 634:

**Linha 635 — Expr** (nível 5 do bloco).

Executa a chamada `atualizar_preferencia_convocacao`; argumentos posicionais: `usuario`, `form.cleaned_data['aceita_notificacoes_pedidos']`, `request`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 640 — Expr** (nível 3 do bloco).

Executa a chamada `login`; argumentos posicionais: `request`, `usuario`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 643 — If** (nível 3 do bloco).

Escolhe um caminho verificando a comparação `usuario.perfil` igual a `Usuario.Perfil.HEMOCENTRO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 643:

**Linha 644 — Expr** (nível 4 do bloco).

Executa a chamada `messages.success`; argumentos posicionais: `request`, `'Cadastro realizado com sucesso! Seu cadastro de Hemocentro esta aguardando a aprovacao de um administrador.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 643:

**Linha 654 — Expr** (nível 4 do bloco).

Executa a chamada `messages.success`; argumentos posicionais: `request`, `'Cadastro realizado com sucesso.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 659 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:dashboard'` ao chamador.

**Linha 663 — Expr** (nível 2 do bloco).

Executa a chamada `messages.error`; argumentos posicionais: `request`, `'O cadastro nao foi concluido. Corrija os erros destacados no formulario.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 608:

**Linha 672 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `CadastroUsuarioForm`.


**Linha 674 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/cadastro.html'`, `{'form': form}` ao chamador.

### compatibilidade_sanguinea — linhas 681 a 716

```python
def compatibilidade_sanguinea(request):
    """Exibe a tabela e a consulta de compatibilidade sanguinea."""

    tipo_selecionado = request.GET.get("tipo", "")

    compatibilidade_selecionada = None
    tipo_invalido = False

    if tipo_selecionado:
        tipo_selecionado = tipo_selecionado.strip().upper()

        try:
            compatibilidade_selecionada = {
                "tipo": tipo_selecionado,
                "doar_para": tipos_que_recebem_de(
                    tipo_selecionado
                ),
                "receber_de": doadores_compativeis_para(
                    tipo_selecionado
                ),
            }

        except ValueError:
            tipo_invalido = True

    return render(
        request,
        "accounts/compatibilidade_sanguinea.html",
        {
            "tipos_sanguineos": TIPOS_SANGUINEOS,
            "tipo_selecionado": tipo_selecionado,
            "compatibilidade_selecionada": compatibilidade_selecionada,
            "tipo_invalido": tipo_invalido,
            "tabela_compatibilidade": tabela_de_compatibilidade(),
        },
    )
```

**Explicação deste trecho:**

**Linha 681 — FunctionDef** (nível 0 do bloco).

Define `compatibilidade_sanguinea(request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 681:

**Linha 682 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 684 — Assign** (nível 1 do bloco).

Associa `tipo_selecionado` a a chamada `request.GET.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'tipo'`, `''`.


**Linha 686 — Assign** (nível 1 do bloco).

Associa `compatibilidade_selecionada` a o valor literal `None`.

**Linha 687 — Assign** (nível 1 do bloco).

Associa `tipo_invalido` a o valor literal `False`.

**Linha 689 — If** (nível 1 do bloco).

Escolhe um caminho verificando o valor associado ao nome `tipo_selecionado`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 689:

**Linha 690 — Assign** (nível 2 do bloco).

Associa `tipo_selecionado` a a chamada `tipo_selecionado.strip().upper`, que converte texto para maiúsculas.


**Linha 692 — Try** (nível 2 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 692:

**Linha 693 — Assign** (nível 3 do bloco).

Associa `compatibilidade_selecionada` a um dicionário de 3 entradas; as chaves dão nome aos valores associados.

- Chave `'tipo'`: recebe o valor associado ao nome `tipo_selecionado`.
- Chave `'doar_para'`: recebe a chamada `tipos_que_recebem_de`; argumentos posicionais: `tipo_selecionado`.
- Chave `'receber_de'`: recebe a chamada `doadores_compativeis_para`; argumentos posicionais: `tipo_selecionado`.

Erro tratado: `ValueError`.

**Linha 704 — Assign** (nível 3 do bloco).

Associa `tipo_invalido` a o valor literal `True`.

**Linha 706 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/compatibilidade_sanguinea.html'`, `{'tipos_sanguineos': TIPOS_SANGUINEOS, 'tipo_selecionado': tipo_selecionado, 'compatibilidade_selecionada': compatibilidade_selecionada, 'tipo_invalido': tipo_invalido, 'tabela_compatibilidade': tabela_de_compatibilidade()}` ao chamador.

### dashboard — linhas 719 a 822

```python
@login_required
def dashboard(request):
    """Mostra o painel protegido particularizado pelo perfil do usuario."""

    if request.method == "POST":
        if request.POST.get("acao") == "marcar_notificacao_lida":
            try:
                id_notificacao = int(request.POST.get("id_notificacao", ""))
            except (TypeError, ValueError):
                raise Http404("Notificacao nao encontrada.")
            notificacao = get_object_or_404(
                request.user.notificacoes, pk=id_notificacao,
            )
            request.user.notificacoes.filter(pk=notificacao.pk, lida=False).update(
                lida=True, lida_em=timezone.now(),
            )
            return redirect("accounts:dashboard")
        if request.user.perfil != Usuario.Perfil.DOADOR:
            raise PermissionDenied("Somente Doadores podem configurar convocacoes.")
        form = PreferenciaConvocacaoForm(request.POST)
        if form.is_valid():
            atualizar_preferencia_convocacao(
                request.user, form.cleaned_data["aceita_convocacoes"], request,
            )
            messages.success(request, "Preferencia de convocacao salva.")
            return redirect("accounts:dashboard")

    preferencia_convocacao = None
    if request.user.perfil == Usuario.Perfil.DOADOR:
        consentimento_vigente = request.user.consentimentos_lgpd.filter(
            tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
            versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO,
            aceito=True, revogado_em__isnull=True,
        ).exists()
        preferencia_convocacao = PreferenciaConvocacaoForm(initial={
            "aceita_convocacoes": request.user.aceita_notificacoes_pedidos and consentimento_vigente,
        })

    painel = PAINEIS_POR_PERFIL.get(
        request.user.perfil,
        PAINEIS_POR_PERFIL[Usuario.Perfil.OBSERVADOR],
    )

    if request.user.perfil == Usuario.Perfil.HEMOCENTRO and not hemocentro_aprovado(request.user):
        painel = {**painel, "acoes": ["Acompanhar o status da validacao institucional."]}
    elif hemocentro_aprovado(request.user):
        painel = {**painel, "acoes": [*painel["acoes"], "Analisar e publicar solicitacoes destinadas ao proprio Hemocentro."]}

    # Busca a ultima analise administrativa do Hemocentro.
    validacao_atual = None

    if request.user.perfil == Usuario.Perfil.HEMOCENTRO:
        validacao_atual = (
            ValidacaoHemocentro.objects
            .filter(
                hemocentro=request.user
            )
            .order_by("-data_analise")
            .first()
        )

    # O resumo usa apenas registros do usuário autenticado. As respostas
    # detalhadas não são expostas no painel geral.
    ultima_triagem = None

    if pode_responder(request.user):
        ultima_triagem = request.user.triagens.order_by("-iniciada_em").first()

    visibilidade = montar_visibilidade_dashboard(
        request.user,
        painel,
    )

    notificacoes_usuario = request.user.notificacoes.order_by("-criada_em", "-pk")
    notificacoes_dashboard = Paginator(notificacoes_usuario, 10).get_page(
        request.GET.get("pagina_notificacoes"),
    )

    contexto = {
        "painel": painel,
        "visibilidade": visibilidade,
        "postos": POSTOS_COLETA,
        "estoque_geral": ESTOQUE_GERAL,
        "pedidos_ativos": (
            PedidoSangue.objects
            .select_related("hemocentro_destino")
            .filter(status=PedidoSangue.Status.PUBLICADA)
            .order_by("-data_criacao")[:10]
        ),
        "campanhas_ativas": CAMPANHAS_ATIVAS,
        "validacao_atual": validacao_atual,
        "ultima_triagem": ultima_triagem,
        "notificacoes_dashboard": notificacoes_dashboard,
        "notificacoes_nao_lidas": notificacoes_usuario.filter(lida=False).count(),
        "preferencia_convocacao": preferencia_convocacao,
        "convocacao_intervalo_horas": settings.CONVOCACAO_INTERVALO_HORAS,
        "convocacao_limite": settings.CONVOCACAO_LIMITE_NOTIFICACOES,
    }

    return render(
        request,
        "accounts/dashboard.html",
        contexto,
    )
```

**Explicação deste trecho:**

**Linha 720 — FunctionDef** (nível 0 do bloco).

Define `dashboard(request)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`.

Bloco `body` da linha 720:

**Linha 721 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 723 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `request.method` igual a `'POST'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 723:

**Linha 724 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `request.POST.get('acao')` igual a `'marcar_notificacao_lida'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 724:

**Linha 725 — Try** (nível 3 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 725:

**Linha 726 — Assign** (nível 4 do bloco).

Associa `id_notificacao` a a chamada `int`; argumentos posicionais: `request.POST.get('id_notificacao', '')`.


Erro tratado: `(TypeError, ValueError)`.

**Linha 728 — Raise** (nível 4 do bloco).

Interrompe o caminho levantando a chamada `Http404`; argumentos posicionais: `'Notificacao nao encontrada.'`.

**Linha 729 — Assign** (nível 3 do bloco).

Associa `notificacao` a a chamada `get_object_or_404`, que busca um objeto na consulta fornecida; ausência gera resposta 404; argumentos posicionais: `request.user.notificacoes`; argumentos nomeados: `pk=id_notificacao`.

- `pk=id_notificacao`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 732 — Expr** (nível 3 do bloco).

Executa a chamada `request.user.notificacoes.filter(pk=notificacao.pk, lida=False).update`, que no QuerySet grava diretamente os campos dos resultados, sem chamar save de cada instância; argumentos nomeados: `lida=True`, `lida_em=timezone.now()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 735 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:dashboard'` ao chamador.

**Linha 736 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `request.user.perfil` diferente de `Usuario.Perfil.DOADOR`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 736:

**Linha 737 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'Somente Doadores podem configurar convocacoes.'`.

**Linha 738 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `PreferenciaConvocacaoForm`; argumentos posicionais: `request.POST`.


**Linha 739 — If** (nível 2 do bloco).

Escolhe um caminho verificando a chamada `form.is_valid`, que valida o formulário e disponibiliza cleaned_data quando válido. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 739:

**Linha 740 — Expr** (nível 3 do bloco).

Executa a chamada `atualizar_preferencia_convocacao`; argumentos posicionais: `request.user`, `form.cleaned_data['aceita_convocacoes']`, `request`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 743 — Expr** (nível 3 do bloco).

Executa a chamada `messages.success`; argumentos posicionais: `request`, `'Preferencia de convocacao salva.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 744 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:dashboard'` ao chamador.

**Linha 746 — Assign** (nível 1 do bloco).

Associa `preferencia_convocacao` a o valor literal `None`.

**Linha 747 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `request.user.perfil` igual a `Usuario.Perfil.DOADOR`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 747:

**Linha 748 — Assign** (nível 2 do bloco).

Associa `consentimento_vigente` a a chamada `request.user.consentimentos_lgpd.filter(tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES, versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO, aceito=True, revogado_em__isnull=True).exists`, que verifica se há pelo menos um resultado.


**Linha 753 — Assign** (nível 2 do bloco).

Associa `preferencia_convocacao` a a chamada `PreferenciaConvocacaoForm`; argumentos nomeados: `initial={'aceita_convocacoes': request.user.aceita_notificacoes_pedidos and consentimento_vigente}`.

- `initial={'aceita_convocacoes': request.user.aceita_notificacoes_pedidos and consentimento_vigente}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 757 — Assign** (nível 1 do bloco).

Associa `painel` a a chamada `PAINEIS_POR_PERFIL.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `request.user.perfil`, `PAINEIS_POR_PERFIL[Usuario.Perfil.OBSERVADOR]`.


**Linha 762 — If** (nível 1 do bloco).

Escolhe um caminho verificando todas as condições: `request.user.perfil == Usuario.Perfil.HEMOCENTRO` ; `not hemocentro_aprovado(request.user)` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 762:

**Linha 763 — Assign** (nível 2 do bloco).

Associa `painel` a um dicionário de 2 entradas; as chaves dão nome aos valores associados.

- Chave `**`: recebe o valor associado ao nome `painel`.
- Chave `'acoes'`: recebe uma coleção List com 1 itens, na expressão `['Acompanhar o status da validacao institucional.']`.

Bloco `orelse` da linha 762:

**Linha 764 — If** (nível 2 do bloco).

Escolhe um caminho verificando a chamada `hemocentro_aprovado`; argumentos posicionais: `request.user`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 764:

**Linha 765 — Assign** (nível 3 do bloco).

Associa `painel` a um dicionário de 2 entradas; as chaves dão nome aos valores associados.

- Chave `**`: recebe o valor associado ao nome `painel`.
- Chave `'acoes'`: recebe uma coleção List com 2 itens, na expressão `[*painel['acoes'], 'Analisar e publicar solicitacoes destinadas ao proprio Hemocentro.']`.

**Linha 768 — Assign** (nível 1 do bloco).

Associa `validacao_atual` a o valor literal `None`.

**Linha 770 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `request.user.perfil` igual a `Usuario.Perfil.HEMOCENTRO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 770:

**Linha 771 — Assign** (nível 2 do bloco).

Associa `validacao_atual` a a chamada `ValidacaoHemocentro.objects.filter(hemocentro=request.user).order_by('-data_analise').first`, que obtém o primeiro resultado ou None.


**Linha 782 — Assign** (nível 1 do bloco).

Associa `ultima_triagem` a o valor literal `None`.

**Linha 784 — If** (nível 1 do bloco).

Escolhe um caminho verificando a chamada `pode_responder`; argumentos posicionais: `request.user`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 784:

**Linha 785 — Assign** (nível 2 do bloco).

Associa `ultima_triagem` a a chamada `request.user.triagens.order_by('-iniciada_em').first`, que obtém o primeiro resultado ou None.


**Linha 787 — Assign** (nível 1 do bloco).

Associa `visibilidade` a a chamada `montar_visibilidade_dashboard`; argumentos posicionais: `request.user`, `painel`.


**Linha 792 — Assign** (nível 1 do bloco).

Associa `notificacoes_usuario` a a chamada `request.user.notificacoes.order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'-criada_em'`, `'-pk'`.


**Linha 793 — Assign** (nível 1 do bloco).

Associa `notificacoes_dashboard` a a chamada `Paginator(notificacoes_usuario, 10).get_page`; argumentos posicionais: `request.GET.get('pagina_notificacoes')`.


**Linha 797 — Assign** (nível 1 do bloco).

Associa `contexto` a um dicionário de 13 entradas; as chaves dão nome aos valores associados.

- Chave `'painel'`: recebe o valor associado ao nome `painel`.
- Chave `'visibilidade'`: recebe o valor associado ao nome `visibilidade`.
- Chave `'postos'`: recebe o valor associado ao nome `POSTOS_COLETA`.
- Chave `'estoque_geral'`: recebe o valor associado ao nome `ESTOQUE_GERAL`.
- Chave `'pedidos_ativos'`: recebe o item ou recorte `:10` de `PedidoSangue.objects.select_related('hemocentro_destino').filter(status=PedidoSangue.Status.PUBLICADA).order_by('-data_criacao')`.
- Chave `'campanhas_ativas'`: recebe o valor associado ao nome `CAMPANHAS_ATIVAS`.
- Chave `'validacao_atual'`: recebe o valor associado ao nome `validacao_atual`.
- Chave `'ultima_triagem'`: recebe o valor associado ao nome `ultima_triagem`.
- Chave `'notificacoes_dashboard'`: recebe o valor associado ao nome `notificacoes_dashboard`.
- Chave `'notificacoes_nao_lidas'`: recebe a chamada `notificacoes_usuario.filter(lida=False).count`, que conta os resultados.
- Chave `'preferencia_convocacao'`: recebe o valor associado ao nome `preferencia_convocacao`.
- Chave `'convocacao_intervalo_horas'`: recebe o atributo `CONVOCACAO_INTERVALO_HORAS` de `settings`.
- Chave `'convocacao_limite'`: recebe o atributo `CONVOCACAO_LIMITE_NOTIFICACOES` de `settings`.

**Linha 818 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/dashboard.html'`, `contexto` ao chamador.

### painel_aprovacao_hemocentros — linhas 825 a 850

```python
@login_required
def painel_aprovacao_hemocentros(request):
    """Mostra a tela administrativa de aprovacao de Hemocentros."""

    exigir_administrador(request.user)

    hemocentros = (
        Usuario.objects
        .filter(
            perfil=Usuario.Perfil.HEMOCENTRO,
            status_validacao=(
                Usuario.StatusValidacaoHemocentro.PENDENTE
            ),
        )
        .order_by("date_joined")
    )

    contexto = {
        "hemocentros": hemocentros,
    }

    return render(
        request,
        "accounts/painel_aprovacao_hemocentros.html",
        contexto,
    )
```

**Explicação deste trecho:**

**Linha 826 — FunctionDef** (nível 0 do bloco).

Define `painel_aprovacao_hemocentros(request)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`.

Bloco `body` da linha 826:

**Linha 827 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 829 — Expr** (nível 1 do bloco).

Executa a chamada `exigir_administrador`; argumentos posicionais: `request.user`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 831 — Assign** (nível 1 do bloco).

Associa `hemocentros` a a chamada `Usuario.objects.filter(perfil=Usuario.Perfil.HEMOCENTRO, status_validacao=Usuario.StatusValidacaoHemocentro.PENDENTE).order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'date_joined'`.


**Linha 842 — Assign** (nível 1 do bloco).

Associa `contexto` a um dicionário de 1 entradas; as chaves dão nome aos valores associados.

- Chave `'hemocentros'`: recebe o valor associado ao nome `hemocentros`.

**Linha 846 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/painel_aprovacao_hemocentros.html'`, `contexto` ao chamador.

### hemocentros_pendentes — linhas 853 a 888

```python
@login_required
def hemocentros_pendentes(request):
    """Retorna os Hemocentros que ainda aguardam decisao administrativa."""

    exigir_administrador(request.user)

    hemocentros = (
        Usuario.objects
        .filter(
            perfil=Usuario.Perfil.HEMOCENTRO,
            status_validacao=(
                Usuario.StatusValidacaoHemocentro.PENDENTE
            ),
        )
        .order_by("date_joined")
    )

    dados = [
        {
            "id_hemocentro": hemocentro.pk,
            "nome": hemocentro.nome,
            "email": hemocentro.email,
            "cnpj": hemocentro.cnpj,
            "cidade": hemocentro.cidade,
            "estado": hemocentro.estado,
            "status_validacao": hemocentro.status_validacao,
            "data_cadastro": hemocentro.date_joined.isoformat(),
        }
        for hemocentro in hemocentros
    ]

    return JsonResponse(
        {
            "hemocentros": dados
        }
    )
```

**Explicação deste trecho:**

**Linha 854 — FunctionDef** (nível 0 do bloco).

Define `hemocentros_pendentes(request)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`.

Bloco `body` da linha 854:

**Linha 855 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 857 — Expr** (nível 1 do bloco).

Executa a chamada `exigir_administrador`; argumentos posicionais: `request.user`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 859 — Assign** (nível 1 do bloco).

Associa `hemocentros` a a chamada `Usuario.objects.filter(perfil=Usuario.Perfil.HEMOCENTRO, status_validacao=Usuario.StatusValidacaoHemocentro.PENDENTE).order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'date_joined'`.


**Linha 870 — Assign** (nível 1 do bloco).

Associa `dados` a uma coleção/gerador construído por compreensão em `[{'id_hemocentro': hemocentro.pk, 'nome': hemocentro.nome, 'email': hemocentro.email, 'cnpj': hemocentro.cnpj, 'cidade': hemocentro.cidade, 'estado': hemocentro.estado, 'status_validacao': hemocentro.status_validacao, 'data_cadastro': hemocentro.date_joined.isoformat()} for hemocentro in hemocentros]`: percorre as fontes e aplica os filtros declarados.

**Linha 884 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `JsonResponse`; argumentos posicionais: `{'hemocentros': dados}` ao chamador.

### aprovar_hemocentro — linhas 891 a 916

```python
@login_required
@require_POST
def aprovar_hemocentro(request, id_hemocentro):
    """Acao administrativa para aprovar um Hemocentro."""

    exigir_administrador(request.user)

    hemocentro = obter_hemocentro_ou_404(
        id_hemocentro
    )

    aprovar_hemocentro_servico(
        hemocentro=hemocentro,
        admin=request.user,
        parecer=request.POST.get("parecer", ""),
        request=request,
    )

    messages.success(
        request,
        "Hemocentro aprovado com sucesso.",
    )

    return redirect(
        "accounts:painel_aprovacao_hemocentros"
    )
```

**Explicação deste trecho:**

**Linha 893 — FunctionDef** (nível 0 do bloco).

Define `aprovar_hemocentro(request, id_hemocentro)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`, `require_POST`.

Bloco `body` da linha 893:

**Linha 894 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 896 — Expr** (nível 1 do bloco).

Executa a chamada `exigir_administrador`; argumentos posicionais: `request.user`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 898 — Assign** (nível 1 do bloco).

Associa `hemocentro` a a chamada `obter_hemocentro_ou_404`; argumentos posicionais: `id_hemocentro`.


**Linha 902 — Expr** (nível 1 do bloco).

Executa a chamada `aprovar_hemocentro_servico`; argumentos nomeados: `hemocentro=hemocentro`, `admin=request.user`, `parecer=request.POST.get('parecer', '')`, `request=request`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 909 — Expr** (nível 1 do bloco).

Executa a chamada `messages.success`; argumentos posicionais: `request`, `'Hemocentro aprovado com sucesso.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 914 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:painel_aprovacao_hemocentros'` ao chamador.

### recusar_hemocentro — linhas 919 a 944

```python
@login_required
@require_POST
def recusar_hemocentro(request, id_hemocentro):
    """Acao administrativa para recusar um Hemocentro."""

    exigir_administrador(request.user)

    hemocentro = obter_hemocentro_ou_404(
        id_hemocentro
    )

    recusar_hemocentro_servico(
        hemocentro=hemocentro,
        admin=request.user,
        parecer=request.POST.get("parecer", ""),
        request=request,
    )

    messages.success(
        request,
        "Hemocentro recusado com sucesso.",
    )

    return redirect(
        "accounts:painel_aprovacao_hemocentros"
    )
```

**Explicação deste trecho:**

**Linha 921 — FunctionDef** (nível 0 do bloco).

Define `recusar_hemocentro(request, id_hemocentro)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`, `require_POST`.

Bloco `body` da linha 921:

**Linha 922 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 924 — Expr** (nível 1 do bloco).

Executa a chamada `exigir_administrador`; argumentos posicionais: `request.user`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 926 — Assign** (nível 1 do bloco).

Associa `hemocentro` a a chamada `obter_hemocentro_ou_404`; argumentos posicionais: `id_hemocentro`.


**Linha 930 — Expr** (nível 1 do bloco).

Executa a chamada `recusar_hemocentro_servico`; argumentos nomeados: `hemocentro=hemocentro`, `admin=request.user`, `parecer=request.POST.get('parecer', '')`, `request=request`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 937 — Expr** (nível 1 do bloco).

Executa a chamada `messages.success`; argumentos posicionais: `request`, `'Hemocentro recusado com sucesso.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 942 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:painel_aprovacao_hemocentros'` ao chamador.

### solicitar_correcao_hemocentro — linhas 947 a 972

```python
@login_required
@require_POST
def solicitar_correcao_hemocentro(request, id_hemocentro):
    """Solicita correcao cadastral para um Hemocentro."""

    exigir_administrador(request.user)

    hemocentro = obter_hemocentro_ou_404(
        id_hemocentro
    )

    solicitar_correcao_hemocentro_servico(
        hemocentro=hemocentro,
        admin=request.user,
        parecer=request.POST.get("parecer", ""),
        request=request,
    )

    messages.success(
        request,
        "Solicitacao de correcao registrada com sucesso.",
    )

    return redirect(
        "accounts:painel_aprovacao_hemocentros"
    )
```

**Explicação deste trecho:**

**Linha 949 — FunctionDef** (nível 0 do bloco).

Define `solicitar_correcao_hemocentro(request, id_hemocentro)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`, `require_POST`.

Bloco `body` da linha 949:

**Linha 950 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 952 — Expr** (nível 1 do bloco).

Executa a chamada `exigir_administrador`; argumentos posicionais: `request.user`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 954 — Assign** (nível 1 do bloco).

Associa `hemocentro` a a chamada `obter_hemocentro_ou_404`; argumentos posicionais: `id_hemocentro`.


**Linha 958 — Expr** (nível 1 do bloco).

Executa a chamada `solicitar_correcao_hemocentro_servico`; argumentos nomeados: `hemocentro=hemocentro`, `admin=request.user`, `parecer=request.POST.get('parecer', '')`, `request=request`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 965 — Expr** (nível 1 do bloco).

Executa a chamada `messages.success`; argumentos posicionais: `request`, `'Solicitacao de correcao registrada com sucesso.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 970 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:painel_aprovacao_hemocentros'` ao chamador.

### triagem_apresentacao — linhas 975 a 1028

```python
def triagem_apresentacao(request):
    """
    Exibe a apresentação pública da triagem.

    Somente usuários com perfil permitido podem iniciar a triagem.

    A modalidade simplificada é liberada quando existe uma triagem
    extensa concluída que possa ser utilizada como base.
    """

    pode_iniciar = False
    pode_simplificada = False
    triagem_em_andamento = None
    ultima_triagem = None
    extensa_base = None
    extensa_reutilizavel = None

    if request.user.is_authenticated:
        pode_iniciar = pode_responder(request.user)

        if pode_iniciar:
            triagens = (
                request.user.triagens
                .select_related("triagem_base")
                .order_by("-iniciada_em")
            )

            ultima_triagem = triagens.first()

            triagem_em_andamento = (
                triagens
                .filter(status=Triagem.Status.EM_ANDAMENTO)
                .first()
            )

            extensa_base = obter_extensa_base(request.user)
            extensa_reutilizavel = obter_extensa_reutilizavel(request.user)

            # A simplificada só fica disponível quando existe
            # uma triagem extensa concluída válida como base.
            pode_simplificada = extensa_base is not None

    return render(
        request,
        "accounts/triagem_apresentacao.html",
        {
            "pode_iniciar": pode_iniciar,
            "pode_simplificada": pode_simplificada,
            "triagem_em_andamento": triagem_em_andamento,
            "ultima_triagem": ultima_triagem,
            "triagem_extensa_base": extensa_base,
            "triagem_extensa_reutilizavel": extensa_reutilizavel,
        },
    )
```

**Explicação deste trecho:**

**Linha 975 — FunctionDef** (nível 0 do bloco).

Define `triagem_apresentacao(request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 975:

**Linha 976 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 985 — Assign** (nível 1 do bloco).

Associa `pode_iniciar` a o valor literal `False`.

**Linha 986 — Assign** (nível 1 do bloco).

Associa `pode_simplificada` a o valor literal `False`.

**Linha 987 — Assign** (nível 1 do bloco).

Associa `triagem_em_andamento` a o valor literal `None`.

**Linha 988 — Assign** (nível 1 do bloco).

Associa `ultima_triagem` a o valor literal `None`.

**Linha 989 — Assign** (nível 1 do bloco).

Associa `extensa_base` a o valor literal `None`.

**Linha 990 — Assign** (nível 1 do bloco).

Associa `extensa_reutilizavel` a o valor literal `None`.

**Linha 992 — If** (nível 1 do bloco).

Escolhe um caminho verificando o atributo `is_authenticated` de `request.user`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 992:

**Linha 993 — Assign** (nível 2 do bloco).

Associa `pode_iniciar` a a chamada `pode_responder`; argumentos posicionais: `request.user`.


**Linha 995 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `pode_iniciar`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 995:

**Linha 996 — Assign** (nível 3 do bloco).

Associa `triagens` a a chamada `request.user.triagens.select_related('triagem_base').order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'-iniciada_em'`.


**Linha 1002 — Assign** (nível 3 do bloco).

Associa `ultima_triagem` a a chamada `triagens.first`, que obtém o primeiro resultado ou None.


**Linha 1004 — Assign** (nível 3 do bloco).

Associa `triagem_em_andamento` a a chamada `triagens.filter(status=Triagem.Status.EM_ANDAMENTO).first`, que obtém o primeiro resultado ou None.


**Linha 1010 — Assign** (nível 3 do bloco).

Associa `extensa_base` a a chamada `obter_extensa_base`; argumentos posicionais: `request.user`.


**Linha 1011 — Assign** (nível 3 do bloco).

Associa `extensa_reutilizavel` a a chamada `obter_extensa_reutilizavel`; argumentos posicionais: `request.user`.


**Linha 1015 — Assign** (nível 3 do bloco).

Associa `pode_simplificada` a a comparação `extensa_base` um objeto diferente de `None`.

**Linha 1017 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/triagem_apresentacao.html'`, `{'pode_iniciar': pode_iniciar, 'pode_simplificada': pode_simplificada, 'triagem_em_andamento': triagem_em_andamento, 'ultima_triagem': ultima_triagem, 'triagem_extensa_base': extensa_base, 'triagem_extensa_reutilizavel': extensa_reutilizavel}` ao chamador.

### triagem_historico — linhas 1031 a 1069

```python
@login_required
def triagem_historico(request):
    """
    Lista somente as triagens pertencentes ao usuario autenticado.

    O historico mostra tanto triagens em andamento quanto concluidas e
    canceladas, permitindo que o template ofereça continuar ou consultar
    o resultado conforme o status.
    """

    if not pode_responder(request.user):
        messages.error(
            request,
            "A triagem de doacao nao esta disponivel para este perfil.",
        )

        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.MODERACAO,
            resultado=AuditoriaAcaoCritica.Resultado.BLOQUEADO,
            usuario=request.user, request=request,
            descricao="Tentativa de acesso ao historico de triagens bloqueada.",
            metadados={"evento": "TENTATIVA_ACESSO", "rota": "accounts:triagem_historico"},
        )

        return redirect("accounts:dashboard")

    triagens = (
        request.user.triagens
        .select_related("triagem_base")
        .order_by("-iniciada_em")
    )

    return render(
        request,
        "accounts/triagem_historico.html",
        {
            "triagens": triagens,
        },
    )
```

**Explicação deste trecho:**

**Linha 1032 — FunctionDef** (nível 0 do bloco).

Define `triagem_historico(request)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`.

Bloco `body` da linha 1032:

**Linha 1033 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1041 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `pode_responder(request.user)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1041:

**Linha 1042 — Expr** (nível 2 do bloco).

Executa a chamada `messages.error`; argumentos posicionais: `request`, `'A triagem de doacao nao esta disponivel para este perfil.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1047 — Expr** (nível 2 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.MODERACAO`, `resultado=AuditoriaAcaoCritica.Resultado.BLOQUEADO`, `usuario=request.user`, `request=request`, `descricao='Tentativa de acesso ao historico de triagens bloqueada.'`, `metadados={'evento': 'TENTATIVA_ACESSO', 'rota': 'accounts:triagem_historico'}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1055 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:dashboard'` ao chamador.

**Linha 1057 — Assign** (nível 1 do bloco).

Associa `triagens` a a chamada `request.user.triagens.select_related('triagem_base').order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'-iniciada_em'`.


**Linha 1063 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/triagem_historico.html'`, `{'triagens': triagens}` ao chamador.

### triagem_iniciar — linhas 1072 a 1121

```python
@login_required
@require_POST
def triagem_iniciar(request, modalidade):
    """Inicia ou retoma uma triagem somente após clique explícito."""

    modalidades = {
        "extensa": Triagem.Modalidade.EXTENSA,
        "simplificada": Triagem.Modalidade.SIMPLIFICADA,
    }

    if modalidade not in modalidades:
        raise Http404("Modalidade de triagem inexistente.")

    if not pode_responder(request.user):
        raise PermissionDenied(
            "A triagem está disponível somente para Doador e Receptor."
        )

    if request.POST.get("aceite_termo") not in {"on", "1", "true"}:
        messages.error(
            request,
            "Leia e confirme o termo da pré-triagem para continuar.",
        )
        return redirect("accounts:triagem_apresentacao")

    try:
        triagem = iniciar_triagem(
            request.user,
            modalidades[modalidade],
            ip=obter_ip(request),
            aceite_termo=True,
            reutilizar_respostas=(
                modalidade == "extensa"
                and request.POST.get("reutilizar_respostas")
                in {"on", "1", "true"}
            ),
        )

    except TriagemSimplificadaIndisponivel:
        messages.info(
            request,
            "Conclua primeiro a triagem extensa para usar a versão simplificada.",
        )

        return redirect("accounts:triagem_apresentacao")

    return redirect(
        "accounts:triagem_pergunta",
        id_triagem=triagem.pk,
    )
```

**Explicação deste trecho:**

**Linha 1074 — FunctionDef** (nível 0 do bloco).

Define `triagem_iniciar(request, modalidade)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`, `require_POST`.

Bloco `body` da linha 1074:

**Linha 1075 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1077 — Assign** (nível 1 do bloco).

Associa `modalidades` a um dicionário de 2 entradas; as chaves dão nome aos valores associados.

- Chave `'extensa'`: recebe o atributo `EXTENSA` de `Triagem.Modalidade`.
- Chave `'simplificada'`: recebe o atributo `SIMPLIFICADA` de `Triagem.Modalidade`.

**Linha 1082 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `modalidade` não contido em `modalidades`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1082:

**Linha 1083 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `Http404`; argumentos posicionais: `'Modalidade de triagem inexistente.'`.

**Linha 1085 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `pode_responder(request.user)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1085:

**Linha 1086 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'A triagem está disponível somente para Doador e Receptor.'`.

**Linha 1090 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `request.POST.get('aceite_termo')` não contido em `{'on', '1', 'true'}`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1090:

**Linha 1091 — Expr** (nível 2 do bloco).

Executa a chamada `messages.error`; argumentos posicionais: `request`, `'Leia e confirme o termo da pré-triagem para continuar.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1095 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_apresentacao'` ao chamador.

**Linha 1097 — Try** (nível 1 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 1097:

**Linha 1098 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `iniciar_triagem`; argumentos posicionais: `request.user`, `modalidades[modalidade]`; argumentos nomeados: `ip=obter_ip(request)`, `aceite_termo=True`, `reutilizar_respostas=modalidade == 'extensa' and request.POST.get('reutilizar_respostas') in {'on', '1', 'true'}`.

- `ip=obter_ip(request)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `aceite_termo=True`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `reutilizar_respostas=modalidade == 'extensa' and request.POST.get('reutilizar_respostas') in {'on', '1', 'true'}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

Erro tratado: `TriagemSimplificadaIndisponivel`.

**Linha 1111 — Expr** (nível 2 do bloco).

Executa a chamada `messages.info`; argumentos posicionais: `request`, `'Conclua primeiro a triagem extensa para usar a versão simplificada.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1116 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_apresentacao'` ao chamador.

**Linha 1118 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_pergunta'`; argumentos nomeados: `id_triagem=triagem.pk` ao chamador.

### _triagem_do_usuario_ou_404 — linhas 1124 a 1134

```python
def _triagem_do_usuario_ou_404(request, id_triagem):
    """Evita que uma conta consulte o questionário privado de outra."""

    if not pode_responder(request.user):
        raise PermissionDenied("Somente Doadores podem acessar a triagem.")

    return get_object_or_404(
        Triagem,
        pk=id_triagem,
        usuario=request.user,
    )
```

**Explicação deste trecho:**

**Linha 1124 — FunctionDef** (nível 0 do bloco).

Define `_triagem_do_usuario_ou_404(request, id_triagem)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 1124:

**Linha 1125 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1127 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `pode_responder(request.user)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1127:

**Linha 1128 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'Somente Doadores podem acessar a triagem.'`.

**Linha 1130 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `get_object_or_404`, que busca um objeto na consulta fornecida; ausência gera resposta 404; argumentos posicionais: `Triagem`; argumentos nomeados: `pk=id_triagem`, `usuario=request.user` ao chamador.

### triagem_pergunta — linhas 1137 a 1240

```python
@login_required
def triagem_pergunta(request, id_triagem):
    """Mostra, valida e salva uma única pergunta por página."""

    triagem = _triagem_do_usuario_ou_404(
        request,
        id_triagem,
    )

    if triagem.status == Triagem.Status.CONCLUIDA:
        return redirect(
            "accounts:triagem_resultado",
            id_triagem=triagem.pk,
        )

    if triagem.status == Triagem.Status.CANCELADA:
        return redirect("accounts:triagem_apresentacao")

    pergunta_para_editar = request.GET.get("pergunta")
    if pergunta_para_editar:
        try:
            editar_pergunta(triagem, pergunta_para_editar)
        except PerguntaInvalida as erro:
            raise Http404("Pergunta de triagem inexistente.") from erro

    # O botão anterior muda apenas o cursor e não valida campos da página.
    if request.method == "POST" and request.POST.get("acao") == "anterior":
        voltar_pergunta(triagem)

        return redirect(
            "accounts:triagem_pergunta",
            id_triagem=triagem.pk,
        )

    pergunta = obter_pergunta_atual(triagem)

    if pergunta is None:
        return redirect("accounts:triagem_revisao", id_triagem=triagem.pk)

    resposta_anterior = triagem.respostas.filter(
        id_pergunta=pergunta["id"]
    ).first()

    valor_inicial = resposta_anterior.valor if resposta_anterior else None

    form = FormularioPerguntaTriagem(
        pergunta,
        request.POST or None,
        valor_inicial=valor_inicial,
    )

    if request.method == "POST" and form.is_valid():
        try:
            salvar_resposta(
                triagem,
                pergunta["id"],
                form.cleaned_data["valor"],
            )

        except TriagemExtensaNecessaria:
            # O serviço já cancelou a rápida antes de solicitar a troca.
            nova_extensa = iniciar_triagem(
                request.user,
                Triagem.Modalidade.EXTENSA,
                ip=obter_ip(request),
                aceite_termo=True,
            )

            messages.info(
                request,
                "Como o resumo mudou, continue pela triagem extensa.",
            )

            return redirect(
                "accounts:triagem_pergunta",
                id_triagem=nova_extensa.pk,
            )

        if request.POST.get("acao") == "salvar":
            messages.success(request, "Andamento da triagem salvo.")

            return redirect("accounts:triagem_historico")

        # O serviço mantém o cursor na explicação quando a pessoa não entendeu
        # e volta ao início quando ela escolhe revisar a confirmação final.
        if triagem.pergunta_atual >= len(triagem.fluxo_perguntas):
            return redirect("accounts:triagem_revisao", id_triagem=triagem.pk)

        return redirect(
            "accounts:triagem_pergunta",
            id_triagem=triagem.pk,
        )

    return render(
        request,
        "accounts/triagem_pergunta.html",
        {
            "triagem": triagem,
            "pergunta": pergunta,
            "form": form,
            "numero_pergunta": triagem.pergunta_atual + 1,
            "total_perguntas": len(triagem.fluxo_perguntas),
        },
    )
```

**Explicação deste trecho:**

**Linha 1138 — FunctionDef** (nível 0 do bloco).

Define `triagem_pergunta(request, id_triagem)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`.

Bloco `body` da linha 1138:

**Linha 1139 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1141 — Assign** (nível 1 do bloco).

Associa `triagem` a a chamada `_triagem_do_usuario_ou_404`; argumentos posicionais: `request`, `id_triagem`.


**Linha 1146 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `triagem.status` igual a `Triagem.Status.CONCLUIDA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1146:

**Linha 1147 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_resultado'`; argumentos nomeados: `id_triagem=triagem.pk` ao chamador.

**Linha 1152 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `triagem.status` igual a `Triagem.Status.CANCELADA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1152:

**Linha 1153 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_apresentacao'` ao chamador.

**Linha 1155 — Assign** (nível 1 do bloco).

Associa `pergunta_para_editar` a a chamada `request.GET.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'pergunta'`.


**Linha 1156 — If** (nível 1 do bloco).

Escolhe um caminho verificando o valor associado ao nome `pergunta_para_editar`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1156:

**Linha 1157 — Try** (nível 2 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 1157:

**Linha 1158 — Expr** (nível 3 do bloco).

Executa a chamada `editar_pergunta`; argumentos posicionais: `triagem`, `pergunta_para_editar`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Erro tratado: `PerguntaInvalida` sob o nome `erro`.

**Linha 1160 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `Http404`; argumentos posicionais: `'Pergunta de triagem inexistente.'`.

**Linha 1163 — If** (nível 1 do bloco).

Escolhe um caminho verificando todas as condições: `request.method == 'POST'` ; `request.POST.get('acao') == 'anterior'` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1163:

**Linha 1164 — Expr** (nível 2 do bloco).

Executa a chamada `voltar_pergunta`; argumentos posicionais: `triagem`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1166 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_pergunta'`; argumentos nomeados: `id_triagem=triagem.pk` ao chamador.

**Linha 1171 — Assign** (nível 1 do bloco).

Associa `pergunta` a a chamada `obter_pergunta_atual`; argumentos posicionais: `triagem`.


**Linha 1173 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `pergunta` o mesmo objeto que `None`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1173:

**Linha 1174 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_revisao'`; argumentos nomeados: `id_triagem=triagem.pk` ao chamador.

**Linha 1176 — Assign** (nível 1 do bloco).

Associa `resposta_anterior` a a chamada `triagem.respostas.filter(id_pergunta=pergunta['id']).first`, que obtém o primeiro resultado ou None.


**Linha 1180 — Assign** (nível 1 do bloco).

Associa `valor_inicial` a `resposta_anterior.valor` se `resposta_anterior` for verdadeiro; caso contrário, `None`.

**Linha 1182 — Assign** (nível 1 do bloco).

Associa `form` a a chamada `FormularioPerguntaTriagem`; argumentos posicionais: `pergunta`, `request.POST or None`; argumentos nomeados: `valor_inicial=valor_inicial`.

- `valor_inicial=valor_inicial`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1188 — If** (nível 1 do bloco).

Escolhe um caminho verificando todas as condições: `request.method == 'POST'` ; `form.is_valid()` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1188:

**Linha 1189 — Try** (nível 2 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 1189:

**Linha 1190 — Expr** (nível 3 do bloco).

Executa a chamada `salvar_resposta`; argumentos posicionais: `triagem`, `pergunta['id']`, `form.cleaned_data['valor']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Erro tratado: `TriagemExtensaNecessaria`.

**Linha 1198 — Assign** (nível 3 do bloco).

Associa `nova_extensa` a a chamada `iniciar_triagem`; argumentos posicionais: `request.user`, `Triagem.Modalidade.EXTENSA`; argumentos nomeados: `ip=obter_ip(request)`, `aceite_termo=True`.

- `ip=obter_ip(request)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `aceite_termo=True`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1205 — Expr** (nível 3 do bloco).

Executa a chamada `messages.info`; argumentos posicionais: `request`, `'Como o resumo mudou, continue pela triagem extensa.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1210 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_pergunta'`; argumentos nomeados: `id_triagem=nova_extensa.pk` ao chamador.

**Linha 1215 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `request.POST.get('acao')` igual a `'salvar'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1215:

**Linha 1216 — Expr** (nível 3 do bloco).

Executa a chamada `messages.success`; argumentos posicionais: `request`, `'Andamento da triagem salvo.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1218 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_historico'` ao chamador.

**Linha 1222 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `triagem.pergunta_atual` maior ou igual a `len(triagem.fluxo_perguntas)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1222:

**Linha 1223 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_revisao'`; argumentos nomeados: `id_triagem=triagem.pk` ao chamador.

**Linha 1225 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_pergunta'`; argumentos nomeados: `id_triagem=triagem.pk` ao chamador.

**Linha 1230 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/triagem_pergunta.html'`, `{'triagem': triagem, 'pergunta': pergunta, 'form': form, 'numero_pergunta': triagem.pergunta_atual + 1, 'total_perguntas': len(triagem.fluxo_perguntas)}` ao chamador.

### triagem_revisao — linhas 1243 a 1281

```python
@login_required
def triagem_revisao(request, id_triagem):
    """Mostra todas as respostas antes do cálculo final."""

    triagem = _triagem_do_usuario_ou_404(request, id_triagem)
    if triagem.status == Triagem.Status.CONCLUIDA:
        return redirect("accounts:triagem_resultado", id_triagem=triagem.pk)
    if triagem.status == Triagem.Status.CANCELADA:
        return redirect("accounts:triagem_apresentacao")

    if request.method == "POST" and request.POST.get("acao") == "finalizar":
        try:
            triagem = concluir_triagem(triagem)
        except TriagemIncompleta as erro:
            messages.error(request, str(erro))
        else:
            return redirect("accounts:triagem_resultado", id_triagem=triagem.pk)

    respostas = []
    registros = triagem.respostas.order_by("id_resposta")
    for resposta in registros:
        try:
            pergunta = obter_pergunta(resposta.id_pergunta)
        except KeyError:
            continue
        respostas.append(
            {
                "id": resposta.id_pergunta,
                "titulo": pergunta["titulo"],
                "resposta": resposta.resposta_label,
                "detalhes": (resposta.valor or {}).get("detalhes", ""),
            }
        )

    return render(
        request,
        "accounts/triagem_revisao.html",
        {"triagem": triagem, "respostas_revisao": respostas},
    )
```

**Explicação deste trecho:**

**Linha 1244 — FunctionDef** (nível 0 do bloco).

Define `triagem_revisao(request, id_triagem)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`.

Bloco `body` da linha 1244:

**Linha 1245 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1247 — Assign** (nível 1 do bloco).

Associa `triagem` a a chamada `_triagem_do_usuario_ou_404`; argumentos posicionais: `request`, `id_triagem`.


**Linha 1248 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `triagem.status` igual a `Triagem.Status.CONCLUIDA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1248:

**Linha 1249 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_resultado'`; argumentos nomeados: `id_triagem=triagem.pk` ao chamador.

**Linha 1250 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `triagem.status` igual a `Triagem.Status.CANCELADA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1250:

**Linha 1251 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_apresentacao'` ao chamador.

**Linha 1253 — If** (nível 1 do bloco).

Escolhe um caminho verificando todas as condições: `request.method == 'POST'` ; `request.POST.get('acao') == 'finalizar'` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1253:

**Linha 1254 — Try** (nível 2 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 1254:

**Linha 1255 — Assign** (nível 3 do bloco).

Associa `triagem` a a chamada `concluir_triagem`; argumentos posicionais: `triagem`.


Bloco `orelse` da linha 1254:

**Linha 1259 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_resultado'`; argumentos nomeados: `id_triagem=triagem.pk` ao chamador.

Erro tratado: `TriagemIncompleta` sob o nome `erro`.

**Linha 1257 — Expr** (nível 3 do bloco).

Executa a chamada `messages.error`; argumentos posicionais: `request`, `str(erro)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1261 — Assign** (nível 1 do bloco).

Associa `respostas` a uma coleção List com 0 itens, na expressão `[]`.

**Linha 1262 — Assign** (nível 1 do bloco).

Associa `registros` a a chamada `triagem.respostas.order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'id_resposta'`.


**Linha 1263 — For** (nível 1 do bloco).

Percorre `registros`; cada item é atribuído a `resposta` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 1263:

**Linha 1264 — Try** (nível 2 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 1264:

**Linha 1265 — Assign** (nível 3 do bloco).

Associa `pergunta` a a chamada `obter_pergunta`; argumentos posicionais: `resposta.id_pergunta`.


Erro tratado: `KeyError`.

**Linha 1267 — Continue** (nível 3 do bloco).

Pula o restante da iteração atual e segue para o próximo item do laço.

**Linha 1268 — Expr** (nível 2 do bloco).

Executa a chamada `respostas.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `{'id': resposta.id_pergunta, 'titulo': pergunta['titulo'], 'resposta': resposta.resposta_label, 'detalhes': (resposta.valor or {}).get('detalhes', '')}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1277 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/triagem_revisao.html'`, `{'triagem': triagem, 'respostas_revisao': respostas}` ao chamador.

### triagem_resultado — linhas 1284 a 1308

```python
@login_required
def triagem_resultado(request, id_triagem):
    """Mostra a orientação concluída somente ao dono da triagem."""

    triagem = _triagem_do_usuario_ou_404(
        request,
        id_triagem,
    )

    if triagem.status == Triagem.Status.EM_ANDAMENTO:
        return redirect(
            "accounts:triagem_revisao",
            id_triagem=triagem.pk,
        )

    if triagem.status == Triagem.Status.CANCELADA:
        return redirect("accounts:triagem_historico")

    return render(
        request,
        "accounts/triagem_resultado.html",
        {
            "triagem": triagem,
        },
    )
```

**Explicação deste trecho:**

**Linha 1285 — FunctionDef** (nível 0 do bloco).

Define `triagem_resultado(request, id_triagem)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`.

Bloco `body` da linha 1285:

**Linha 1286 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1288 — Assign** (nível 1 do bloco).

Associa `triagem` a a chamada `_triagem_do_usuario_ou_404`; argumentos posicionais: `request`, `id_triagem`.


**Linha 1293 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `triagem.status` igual a `Triagem.Status.EM_ANDAMENTO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1293:

**Linha 1294 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_revisao'`; argumentos nomeados: `id_triagem=triagem.pk` ao chamador.

**Linha 1299 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `triagem.status` igual a `Triagem.Status.CANCELADA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1299:

**Linha 1300 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:triagem_historico'` ao chamador.

**Linha 1302 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/triagem_resultado.html'`, `{'triagem': triagem}` ao chamador.

### visualizacao_publica_estoque — linhas 1311 a 1383

```python
def visualizacao_publica_estoque(request):
    """
    Exibe publicamente os estoques dos Hemocentros aprovados.

    A camada accounts.estoque devolve apenas os dados permitidos para
    exibicao publica, sem expor os limites internos usados pelo Hemocentro.
    """

    parametros = request.GET.copy()
    # Mantém compatibilidade com os parâmetros antigos da tela (q e tipo).
    if "q" in parametros and "busca" not in parametros:
        parametros["busca"] = parametros.get("q", "")
    if "tipo" in parametros and "tipo_sanguineo" not in parametros:
        parametros["tipo_sanguineo"] = parametros.get("tipo", "")
    if "status" in parametros and "situacao" not in parametros:
        parametros["situacao"] = parametros.get("status", "")

    form = FiltroEstoquePublicoForm(parametros or None)
    estoques = obter_estoques_publicos()

    if form.is_valid():
        tipo = form.cleaned_data.get("tipo_sanguineo")
        cidade = (form.cleaned_data.get("cidade") or "").strip().lower()
        hemocentro = (form.cleaned_data.get("hemocentro") or "").strip().lower()
        situacao = form.cleaned_data.get("situacao")
        busca = (form.cleaned_data.get("busca") or "").strip().lower()

        if tipo:
            estoques = [
                estoque for estoque in estoques
                if estoque["tipo_sanguineo"] == tipo
            ]

        if cidade:
            estoques = [
                estoque for estoque in estoques
                if cidade in estoque["cidade"].lower()
            ]

        if hemocentro:
            estoques = [
                estoque for estoque in estoques
                if hemocentro in estoque["nome"].lower()
            ]

        if situacao:
            estoques = [
                estoque for estoque in estoques
                if estoque["status_codigo"] == situacao
            ]

        if busca:
            estoques = [
                estoque for estoque in estoques
                if busca in " ".join(
                    [
                        estoque["nome"],
                        estoque["cidade"],
                        estoque["estado"],
                        estoque["tipo_sanguineo"],
                        estoque["status_label"],
                    ]
                ).lower()
            ]

    return render(
        request,
        "accounts/estoque_publico.html",
        {
            "estoques": estoques,
            "form": form,
        },
    )
```

**Explicação deste trecho:**

**Linha 1311 — FunctionDef** (nível 0 do bloco).

Define `visualizacao_publica_estoque(request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 1311:

**Linha 1312 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1319 — Assign** (nível 1 do bloco).

Associa `parametros` a a chamada `request.GET.copy`.


**Linha 1321 — If** (nível 1 do bloco).

Escolhe um caminho verificando todas as condições: `'q' in parametros` ; `'busca' not in parametros` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1321:

**Linha 1322 — Assign** (nível 2 do bloco).

Associa `parametros['busca']` a a chamada `parametros.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'q'`, `''`.


**Linha 1323 — If** (nível 1 do bloco).

Escolhe um caminho verificando todas as condições: `'tipo' in parametros` ; `'tipo_sanguineo' not in parametros` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1323:

**Linha 1324 — Assign** (nível 2 do bloco).

Associa `parametros['tipo_sanguineo']` a a chamada `parametros.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'tipo'`, `''`.


**Linha 1325 — If** (nível 1 do bloco).

Escolhe um caminho verificando todas as condições: `'status' in parametros` ; `'situacao' not in parametros` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1325:

**Linha 1326 — Assign** (nível 2 do bloco).

Associa `parametros['situacao']` a a chamada `parametros.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'status'`, `''`.


**Linha 1328 — Assign** (nível 1 do bloco).

Associa `form` a a chamada `FiltroEstoquePublicoForm`; argumentos posicionais: `parametros or None`.


**Linha 1329 — Assign** (nível 1 do bloco).

Associa `estoques` a a chamada `obter_estoques_publicos`.


**Linha 1331 — If** (nível 1 do bloco).

Escolhe um caminho verificando a chamada `form.is_valid`, que valida o formulário e disponibiliza cleaned_data quando válido. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1331:

**Linha 1332 — Assign** (nível 2 do bloco).

Associa `tipo` a a chamada `form.cleaned_data.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'tipo_sanguineo'`.


**Linha 1333 — Assign** (nível 2 do bloco).

Associa `cidade` a a chamada `(form.cleaned_data.get('cidade') or '').strip().lower`, que converte texto para minúsculas.


**Linha 1334 — Assign** (nível 2 do bloco).

Associa `hemocentro` a a chamada `(form.cleaned_data.get('hemocentro') or '').strip().lower`, que converte texto para minúsculas.


**Linha 1335 — Assign** (nível 2 do bloco).

Associa `situacao` a a chamada `form.cleaned_data.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'situacao'`.


**Linha 1336 — Assign** (nível 2 do bloco).

Associa `busca` a a chamada `(form.cleaned_data.get('busca') or '').strip().lower`, que converte texto para minúsculas.


**Linha 1338 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `tipo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1338:

**Linha 1339 — Assign** (nível 3 do bloco).

Associa `estoques` a uma coleção/gerador construído por compreensão em `[estoque for estoque in estoques if estoque['tipo_sanguineo'] == tipo]`: percorre as fontes e aplica os filtros declarados.

**Linha 1344 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `cidade`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1344:

**Linha 1345 — Assign** (nível 3 do bloco).

Associa `estoques` a uma coleção/gerador construído por compreensão em `[estoque for estoque in estoques if cidade in estoque['cidade'].lower()]`: percorre as fontes e aplica os filtros declarados.

**Linha 1350 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `hemocentro`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1350:

**Linha 1351 — Assign** (nível 3 do bloco).

Associa `estoques` a uma coleção/gerador construído por compreensão em `[estoque for estoque in estoques if hemocentro in estoque['nome'].lower()]`: percorre as fontes e aplica os filtros declarados.

**Linha 1356 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `situacao`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1356:

**Linha 1357 — Assign** (nível 3 do bloco).

Associa `estoques` a uma coleção/gerador construído por compreensão em `[estoque for estoque in estoques if estoque['status_codigo'] == situacao]`: percorre as fontes e aplica os filtros declarados.

**Linha 1362 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `busca`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1362:

**Linha 1363 — Assign** (nível 3 do bloco).

Associa `estoques` a uma coleção/gerador construído por compreensão em `[estoque for estoque in estoques if busca in ' '.join([estoque['nome'], estoque['cidade'], estoque['estado'], estoque['tipo_sanguineo'], estoque['status_label']]).lower()]`: percorre as fontes e aplica os filtros declarados.

**Linha 1376 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/estoque_publico.html'`, `{'estoques': estoques, 'form': form}` ao chamador.

### _formatar_erro_validacao — linhas 1386 a 1395

```python
def _formatar_erro_validacao(erro):
    """Converte um ValidationError (string, lista ou dict) em texto legivel."""

    if hasattr(erro, "message_dict"):
        return "; ".join(
            f"{campo}: {', '.join(mensagens)}"
            for campo, mensagens in erro.message_dict.items()
        )

    return "; ".join(erro.messages)
```

**Explicação deste trecho:**

**Linha 1386 — FunctionDef** (nível 0 do bloco).

Define `_formatar_erro_validacao(erro)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 1386:

**Linha 1387 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1389 — If** (nível 1 do bloco).

Escolhe um caminho verificando a chamada `hasattr`; argumentos posicionais: `erro`, `'message_dict'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1389:

**Linha 1390 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `'; '.join`; argumentos posicionais: `(f"{campo}: {', '.join(mensagens)}" for campo, mensagens in erro.message_dict.items())` ao chamador.

**Linha 1395 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `'; '.join`; argumentos posicionais: `erro.messages` ao chamador.

### estoque_hemocentro — linhas 1398 a 1447

```python
@login_required
@exigir_hemocentro_aprovado
def estoque_hemocentro(request):
    """
    UC_29 / UC_30 - Mostra o estoque do proprio Hemocentro logado e os
    formularios para cadastrar um novo tipo sanguineo ou movimentar um
    estoque ja existente.
    """

    estoques = (
        Estoque.objects
        .filter(hemocentro=request.user)
        .prefetch_related(
            Prefetch(
                "movimentacoes",
                queryset=EstoqueMovimentacao.objects.select_related(
                    "usuario_resp"
                ).order_by("-data_hora"),
            )
        )
        .order_by("tipo_sanguineo")
    )

    tipos_cadastrados = set(
        estoques.values_list("tipo_sanguineo", flat=True)
    )

    tipos_disponiveis = [
        tipo
        for tipo in TIPOS_SANGUINEOS
        if tipo not in tipos_cadastrados
    ]

    form_cadastro = CadastrarEstoqueForm()

    form_cadastro.fields["tipo_sanguineo"].choices = [
        (tipo, tipo)
        for tipo in tipos_disponiveis
    ]

    return render(
        request,
        "accounts/estoque_hemocentro.html",
        {
            "estoques": estoques,
            "tipos_disponiveis": tipos_disponiveis,
            "form_cadastro": form_cadastro,
            "form_movimentacao": MovimentarEstoqueForm(),
        },
    )
```

**Explicação deste trecho:**

**Linha 1400 — FunctionDef** (nível 0 do bloco).

Define `estoque_hemocentro(request)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`, `exigir_hemocentro_aprovado`.

Bloco `body` da linha 1400:

**Linha 1401 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1407 — Assign** (nível 1 do bloco).

Associa `estoques` a a chamada `Estoque.objects.filter(hemocentro=request.user).prefetch_related(Prefetch('movimentacoes', queryset=EstoqueMovimentacao.objects.select_related('usuario_resp').order_by('-data_hora'))).order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'tipo_sanguineo'`.


**Linha 1421 — Assign** (nível 1 do bloco).

Associa `tipos_cadastrados` a a chamada `set`; argumentos posicionais: `estoques.values_list('tipo_sanguineo', flat=True)`.


**Linha 1425 — Assign** (nível 1 do bloco).

Associa `tipos_disponiveis` a uma coleção/gerador construído por compreensão em `[tipo for tipo in TIPOS_SANGUINEOS if tipo not in tipos_cadastrados]`: percorre as fontes e aplica os filtros declarados.

**Linha 1431 — Assign** (nível 1 do bloco).

Associa `form_cadastro` a a chamada `CadastrarEstoqueForm`.


**Linha 1433 — Assign** (nível 1 do bloco).

Associa `form_cadastro.fields['tipo_sanguineo'].choices` a uma coleção/gerador construído por compreensão em `[(tipo, tipo) for tipo in tipos_disponiveis]`: percorre as fontes e aplica os filtros declarados.

**Linha 1438 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/estoque_hemocentro.html'`, `{'estoques': estoques, 'tipos_disponiveis': tipos_disponiveis, 'form_cadastro': form_cadastro, 'form_movimentacao': MovimentarEstoqueForm()}` ao chamador.

### cadastrar_estoque_view — linhas 1450 a 1487

```python
@login_required
@require_POST
@exigir_hemocentro_aprovado
def cadastrar_estoque_view(request):
    """UC_29 - Cria a estrutura de estoque de um tipo sanguineo."""

    form = CadastrarEstoqueForm(request.POST)

    if form.is_valid():
        try:
            cadastrar_estoque(
                hemocentro=request.user,
                tipo_sanguineo=form.cleaned_data["tipo_sanguineo"],
                quantidade_bolsas=form.cleaned_data["quantidade_bolsas"],
                nivel_minimo=form.cleaned_data["nivel_minimo"],
                nivel_critico=form.cleaned_data["nivel_critico"],
                request=request,
            )

        except ValidationError as erro:
            messages.error(
                request,
                _formatar_erro_validacao(erro),
            )

        else:
            messages.success(
                request,
                "Estoque cadastrado com sucesso.",
            )

    else:
        messages.error(
            request,
            "Corrija os erros destacados no formulario de cadastro.",
        )

    return redirect("accounts:estoque_hemocentro")
```

**Explicação deste trecho:**

**Linha 1453 — FunctionDef** (nível 0 do bloco).

Define `cadastrar_estoque_view(request)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`, `require_POST`, `exigir_hemocentro_aprovado`.

Bloco `body` da linha 1453:

**Linha 1454 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1456 — Assign** (nível 1 do bloco).

Associa `form` a a chamada `CadastrarEstoqueForm`; argumentos posicionais: `request.POST`.


**Linha 1458 — If** (nível 1 do bloco).

Escolhe um caminho verificando a chamada `form.is_valid`, que valida o formulário e disponibiliza cleaned_data quando válido. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1458:

**Linha 1459 — Try** (nível 2 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 1459:

**Linha 1460 — Expr** (nível 3 do bloco).

Executa a chamada `cadastrar_estoque`; argumentos nomeados: `hemocentro=request.user`, `tipo_sanguineo=form.cleaned_data['tipo_sanguineo']`, `quantidade_bolsas=form.cleaned_data['quantidade_bolsas']`, `nivel_minimo=form.cleaned_data['nivel_minimo']`, `nivel_critico=form.cleaned_data['nivel_critico']`, `request=request`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 1459:

**Linha 1476 — Expr** (nível 3 do bloco).

Executa a chamada `messages.success`; argumentos posicionais: `request`, `'Estoque cadastrado com sucesso.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Erro tratado: `ValidationError` sob o nome `erro`.

**Linha 1470 — Expr** (nível 3 do bloco).

Executa a chamada `messages.error`; argumentos posicionais: `request`, `_formatar_erro_validacao(erro)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 1458:

**Linha 1482 — Expr** (nível 2 do bloco).

Executa a chamada `messages.error`; argumentos posicionais: `request`, `'Corrija os erros destacados no formulario de cadastro.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1487 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:estoque_hemocentro'` ao chamador.

### atualizar_estoque_view — linhas 1490 a 1538

```python
@login_required
@require_POST
@exigir_hemocentro_aprovado
def atualizar_estoque_view(request, id_estoque):
    """UC_30 - Registra uma entrada, saida ou ajuste em um estoque existente."""

    estoque = get_object_or_404(
        Estoque,
        pk=id_estoque,
    )

    form = MovimentarEstoqueForm(request.POST)

    if form.is_valid():
        try:
            registrar_movimentacao_estoque(
                estoque=estoque,
                usuario_resp=request.user,
                tipo_movimento=form.cleaned_data["tipo_movimento"],
                quantidade=form.cleaned_data["quantidade"],
                motivo=form.cleaned_data["motivo"],
                request=request,
            )

        except PermissionDenied as erro:
            messages.error(
                request,
                str(erro),
            )

        except ValidationError as erro:
            messages.error(
                request,
                _formatar_erro_validacao(erro),
            )

        else:
            messages.success(
                request,
                "Estoque atualizado com sucesso.",
            )

    else:
        messages.error(
            request,
            "Corrija os erros destacados no formulario de movimentacao.",
        )

    return redirect("accounts:estoque_hemocentro")
```

**Explicação deste trecho:**

**Linha 1493 — FunctionDef** (nível 0 do bloco).

Define `atualizar_estoque_view(request, id_estoque)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`, `require_POST`, `exigir_hemocentro_aprovado`.

Bloco `body` da linha 1493:

**Linha 1494 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1496 — Assign** (nível 1 do bloco).

Associa `estoque` a a chamada `get_object_or_404`, que busca um objeto na consulta fornecida; ausência gera resposta 404; argumentos posicionais: `Estoque`; argumentos nomeados: `pk=id_estoque`.

- `pk=id_estoque`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1501 — Assign** (nível 1 do bloco).

Associa `form` a a chamada `MovimentarEstoqueForm`; argumentos posicionais: `request.POST`.


**Linha 1503 — If** (nível 1 do bloco).

Escolhe um caminho verificando a chamada `form.is_valid`, que valida o formulário e disponibiliza cleaned_data quando válido. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1503:

**Linha 1504 — Try** (nível 2 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 1504:

**Linha 1505 — Expr** (nível 3 do bloco).

Executa a chamada `registrar_movimentacao_estoque`; argumentos nomeados: `estoque=estoque`, `usuario_resp=request.user`, `tipo_movimento=form.cleaned_data['tipo_movimento']`, `quantidade=form.cleaned_data['quantidade']`, `motivo=form.cleaned_data['motivo']`, `request=request`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 1504:

**Linha 1527 — Expr** (nível 3 do bloco).

Executa a chamada `messages.success`; argumentos posicionais: `request`, `'Estoque atualizado com sucesso.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Erro tratado: `PermissionDenied` sob o nome `erro`.

**Linha 1515 — Expr** (nível 3 do bloco).

Executa a chamada `messages.error`; argumentos posicionais: `request`, `str(erro)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Erro tratado: `ValidationError` sob o nome `erro`.

**Linha 1521 — Expr** (nível 3 do bloco).

Executa a chamada `messages.error`; argumentos posicionais: `request`, `_formatar_erro_validacao(erro)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 1503:

**Linha 1533 — Expr** (nível 2 do bloco).

Executa a chamada `messages.error`; argumentos posicionais: `request`, `'Corrija os erros destacados no formulario de movimentacao.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1538 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:estoque_hemocentro'` ao chamador.

### criar_pedido_sangue — linhas 1541 a 1602

```python
@login_required
def criar_pedido_sangue(request):
    """
    Recebe uma solicitação de divulgação, sem publicá-la.

    Apenas Receptor/Solicitante pode enviar solicitacao de pedido.

    Ao salvar, a solicitacao aguarda analise do Hemocentro.
    """

    if request.user.perfil != Usuario.Perfil.RECEPTOR:
        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.MODERACAO,
            resultado=AuditoriaAcaoCritica.Resultado.BLOQUEADO,
            usuario=request.user, request=request,
            descricao="Tentativa de enviar solicitacao de pedido bloqueada.",
            metadados={"evento": "TENTATIVA_ACESSO", "rota": "accounts:pedido_publicar"},
        )
        messages.error(
            request,
            "Este perfil não envia solicitações de divulgação.",
        )

        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = PedidoSangueForm(request.POST)

        if form.is_valid():
            try:
                pedido = criar_pedido_pendente(
                    dados=form.cleaned_data,
                    solicitante=(
                        request.user if request.user.is_authenticated else None
                    ),
                )

                mensagem = (
                    "Solicitação enviada para análise do Hemocentro. "
                    f"Protocolo {pedido.pk}."
                )
                if pedido.duplicidade_suspeita:
                    mensagem += " Há uma solicitação semelhante; ela será analisada."
                messages.success(request, mensagem)

                if request.user.is_authenticated:
                    return redirect("accounts:minhas_solicitacoes")
                return redirect("accounts:consultar_pedidos")

            except ValidationError as erro:
                form.add_error(None, erro)

    else:
        form = PedidoSangueForm()

    return render(
        request,
        "accounts/pedido_publicar.html",
        {
            "form": form,
        },
    )
```

**Explicação deste trecho:**

**Linha 1542 — FunctionDef** (nível 0 do bloco).

Define `criar_pedido_sangue(request)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`.

Bloco `body` da linha 1542:

**Linha 1543 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1551 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `request.user.perfil` diferente de `Usuario.Perfil.RECEPTOR`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1551:

**Linha 1552 — Expr** (nível 2 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.MODERACAO`, `resultado=AuditoriaAcaoCritica.Resultado.BLOQUEADO`, `usuario=request.user`, `request=request`, `descricao='Tentativa de enviar solicitacao de pedido bloqueada.'`, `metadados={'evento': 'TENTATIVA_ACESSO', 'rota': 'accounts:pedido_publicar'}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1559 — Expr** (nível 2 do bloco).

Executa a chamada `messages.error`; argumentos posicionais: `request`, `'Este perfil não envia solicitações de divulgação.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1564 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:dashboard'` ao chamador.

**Linha 1566 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `request.method` igual a `'POST'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1566:

**Linha 1567 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `PedidoSangueForm`; argumentos posicionais: `request.POST`.


**Linha 1569 — If** (nível 2 do bloco).

Escolhe um caminho verificando a chamada `form.is_valid`, que valida o formulário e disponibiliza cleaned_data quando válido. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1569:

**Linha 1570 — Try** (nível 3 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 1570:

**Linha 1571 — Assign** (nível 4 do bloco).

Associa `pedido` a a chamada `criar_pedido_pendente`; argumentos nomeados: `dados=form.cleaned_data`, `solicitante=request.user if request.user.is_authenticated else None`.

- `dados=form.cleaned_data`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `solicitante=request.user if request.user.is_authenticated else None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1578 — Assign** (nível 4 do bloco).

Associa `mensagem` a o texto formatado `f'Solicitação enviada para análise do Hemocentro. Protocolo {pedido.pk}.'`, inserindo valores nas partes entre chaves.

**Linha 1582 — If** (nível 4 do bloco).

Escolhe um caminho verificando o atributo `duplicidade_suspeita` de `pedido`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1582:

**Linha 1583 — AugAssign** (nível 5 do bloco).

Atualiza `mensagem` pelo operador da expressão `mensagem += ' Há uma solicitação semelhante; ela será analisada.'`. O valor anterior participa do cálculo.

**Linha 1584 — Expr** (nível 4 do bloco).

Executa a chamada `messages.success`; argumentos posicionais: `request`, `mensagem`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1586 — If** (nível 4 do bloco).

Escolhe um caminho verificando o atributo `is_authenticated` de `request.user`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1586:

**Linha 1587 — Return** (nível 5 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:minhas_solicitacoes'` ao chamador.

**Linha 1588 — Return** (nível 4 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:consultar_pedidos'` ao chamador.

Erro tratado: `ValidationError` sob o nome `erro`.

**Linha 1591 — Expr** (nível 4 do bloco).

Executa a chamada `form.add_error`; argumentos posicionais: `None`, `erro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 1566:

**Linha 1594 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `PedidoSangueForm`.


**Linha 1596 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/pedido_publicar.html'`, `{'form': form}` ao chamador.

### minhas_solicitacoes — linhas 1605 a 1634

```python
@login_required
def minhas_solicitacoes(request):
    """Lista somente as solicitações enviadas pelo usuário autenticado."""

    solicitacoes = (
        PedidoSangue.objects
        .select_related("hemocentro_destino")
        .prefetch_related(
            Prefetch(
                "validacoes",
                queryset=ValidacaoPedido.objects.select_related("moderador"),
            )
        )
        .filter(solicitante=request.user)
        .order_by("-data_criacao")
    )

    status = request.GET.get("status")
    if status in dict(PedidoSangue.Status.choices):
        solicitacoes = solicitacoes.filter(status=status)

    return render(
        request,
        "accounts/minhas_solicitacoes.html",
        {
            "solicitacoes": solicitacoes,
            "status_opcoes": PedidoSangue.Status.choices,
            "status_atual": status or "",
        },
    )
```

**Explicação deste trecho:**

**Linha 1606 — FunctionDef** (nível 0 do bloco).

Define `minhas_solicitacoes(request)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`.

Bloco `body` da linha 1606:

**Linha 1607 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1609 — Assign** (nível 1 do bloco).

Associa `solicitacoes` a a chamada `PedidoSangue.objects.select_related('hemocentro_destino').prefetch_related(Prefetch('validacoes', queryset=ValidacaoPedido.objects.select_related('moderador'))).filter(solicitante=request.user).order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'-data_criacao'`.


**Linha 1622 — Assign** (nível 1 do bloco).

Associa `status` a a chamada `request.GET.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'status'`.


**Linha 1623 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `status` contido em `dict(PedidoSangue.Status.choices)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1623:

**Linha 1624 — Assign** (nível 2 do bloco).

Associa `solicitacoes` a a chamada `solicitacoes.filter`, que restringe os resultados às condições informadas; não grava os registros; argumentos nomeados: `status=status`.

- `status=status`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1626 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/minhas_solicitacoes.html'`, `{'solicitacoes': solicitacoes, 'status_opcoes': PedidoSangue.Status.choices, 'status_atual': status or ''}` ao chamador.

### painel_pedidos_hemocentro — linhas 1637 a 1665

```python
@login_required
@exigir_hemocentro_aprovado
def painel_pedidos_hemocentro(request):
    """Fila de solicitações destinadas ao Hemocentro aprovado logado."""

    PedidoSangue.objects.filter(
        hemocentro_destino=request.user,
        status=PedidoSangue.Status.ENVIADA,
    ).update(status=PedidoSangue.Status.EM_ANALISE)

    solicitacoes = (
        PedidoSangue.objects
        .select_related("solicitante", "hemocentro_destino")
        .filter(hemocentro_destino=request.user)
        .exclude(status=PedidoSangue.Status.ENCERRADA)
        .order_by("-data_criacao")
    )
    status = request.GET.get("status")
    if status in dict(PedidoSangue.Status.choices):
        solicitacoes = solicitacoes.filter(status=status)

    return render(
        request,
        "accounts/painel_validacao_pedidos.html",
        {
            "solicitacoes": solicitacoes,
            "status_opcoes": PedidoSangue.Status.choices,
        },
    )
```

**Explicação deste trecho:**

**Linha 1639 — FunctionDef** (nível 0 do bloco).

Define `painel_pedidos_hemocentro(request)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`, `exigir_hemocentro_aprovado`.

Bloco `body` da linha 1639:

**Linha 1640 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1642 — Expr** (nível 1 do bloco).

Executa a chamada `PedidoSangue.objects.filter(hemocentro_destino=request.user, status=PedidoSangue.Status.ENVIADA).update`, que no QuerySet grava diretamente os campos dos resultados, sem chamar save de cada instância; argumentos nomeados: `status=PedidoSangue.Status.EM_ANALISE`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1647 — Assign** (nível 1 do bloco).

Associa `solicitacoes` a a chamada `PedidoSangue.objects.select_related('solicitante', 'hemocentro_destino').filter(hemocentro_destino=request.user).exclude(status=PedidoSangue.Status.ENCERRADA).order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'-data_criacao'`.


**Linha 1654 — Assign** (nível 1 do bloco).

Associa `status` a a chamada `request.GET.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'status'`.


**Linha 1655 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `status` contido em `dict(PedidoSangue.Status.choices)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1655:

**Linha 1656 — Assign** (nível 2 do bloco).

Associa `solicitacoes` a a chamada `solicitacoes.filter`, que restringe os resultados às condições informadas; não grava os registros; argumentos nomeados: `status=status`.

- `status=status`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1658 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/painel_validacao_pedidos.html'`, `{'solicitacoes': solicitacoes, 'status_opcoes': PedidoSangue.Status.choices}` ao chamador.

### consultar_pedidos — linhas 1668 a 1756

```python
def consultar_pedidos(request):
    """
    UC_18 - Consultar Pedidos.

    Exibe apenas pedidos ativos e aplica filtros por tipo sanguineo,
    urgencia, cidade, hemocentro e data. A ordenacao prioriza urgencia
    e depois os mais recentes.
    """

    form = FiltroPedidoSangueForm(request.GET or None)

    pedidos = (
        PedidoSangue.objects
        .select_related("hemocentro_destino")
        .filter(
            status=PedidoSangue.Status.PUBLICADA,
            hemocentro_destino__perfil=Usuario.Perfil.HEMOCENTRO,
            hemocentro_destino__status_validacao=(
                Usuario.StatusValidacaoHemocentro.APROVADO
            ),
        )
    )

    if form.is_valid():
        tipo = form.cleaned_data.get("tipo_sanguineo")
        urgencia = form.cleaned_data.get("urgencia")
        cidade = form.cleaned_data.get("cidade")
        hemocentro = form.cleaned_data.get("hemocentro")
        data = form.cleaned_data.get("data")
        status = form.cleaned_data.get("status")

        # A consulta pública nunca pode revelar solicitações em análise,
        # recusadas ou dados ainda não publicados.
        if status and status != PedidoSangue.Status.PUBLICADA:
            pedidos = pedidos.none()

        if tipo:
            pedidos = pedidos.filter(tipo_sanguineo=tipo)

        if urgencia:
            pedidos = pedidos.filter(urgencia=urgencia)

        if cidade:
            pedidos = pedidos.filter(cidade__icontains=cidade)

        if hemocentro:
            pedidos = pedidos.filter(
                hemocentro_destino__nome__icontains=hemocentro
            )

        if data:
            pedidos = pedidos.filter(data_criacao__date=data)

    prioridade = Case(
        When(
            urgencia=PedidoSangue.Urgencia.CRITICA,
            then=Value(1),
        ),
        When(
            urgencia=PedidoSangue.Urgencia.ALTA,
            then=Value(2),
        ),
        When(
            urgencia=PedidoSangue.Urgencia.MEDIA,
            then=Value(3),
        ),
        When(
            urgencia=PedidoSangue.Urgencia.BAIXA,
            then=Value(4),
        ),
        default=Value(5),
        output_field=IntegerField(),
    )

    pedidos = pedidos.annotate(
        prioridade=prioridade
    ).order_by(
        "prioridade",
        "-data_criacao",
    )

    return render(
        request,
        "accounts/pedidos_listar.html",
        {
            "form": form,
            "pedidos": pedidos,
        },
    )
```

**Explicação deste trecho:**

**Linha 1668 — FunctionDef** (nível 0 do bloco).

Define `consultar_pedidos(request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 1668:

**Linha 1669 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1677 — Assign** (nível 1 do bloco).

Associa `form` a a chamada `FiltroPedidoSangueForm`; argumentos posicionais: `request.GET or None`.


**Linha 1679 — Assign** (nível 1 do bloco).

Associa `pedidos` a a chamada `PedidoSangue.objects.select_related('hemocentro_destino').filter`, que restringe os resultados às condições informadas; não grava os registros; argumentos nomeados: `status=PedidoSangue.Status.PUBLICADA`, `hemocentro_destino__perfil=Usuario.Perfil.HEMOCENTRO`, `hemocentro_destino__status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO`.

- `status=PedidoSangue.Status.PUBLICADA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `hemocentro_destino__perfil=Usuario.Perfil.HEMOCENTRO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `hemocentro_destino__status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1691 — If** (nível 1 do bloco).

Escolhe um caminho verificando a chamada `form.is_valid`, que valida o formulário e disponibiliza cleaned_data quando válido. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1691:

**Linha 1692 — Assign** (nível 2 do bloco).

Associa `tipo` a a chamada `form.cleaned_data.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'tipo_sanguineo'`.


**Linha 1693 — Assign** (nível 2 do bloco).

Associa `urgencia` a a chamada `form.cleaned_data.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'urgencia'`.


**Linha 1694 — Assign** (nível 2 do bloco).

Associa `cidade` a a chamada `form.cleaned_data.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'cidade'`.


**Linha 1695 — Assign** (nível 2 do bloco).

Associa `hemocentro` a a chamada `form.cleaned_data.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'hemocentro'`.


**Linha 1696 — Assign** (nível 2 do bloco).

Associa `data` a a chamada `form.cleaned_data.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'data'`.


**Linha 1697 — Assign** (nível 2 do bloco).

Associa `status` a a chamada `form.cleaned_data.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'status'`.


**Linha 1701 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `status` ; `status != PedidoSangue.Status.PUBLICADA` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1701:

**Linha 1702 — Assign** (nível 3 do bloco).

Associa `pedidos` a a chamada `pedidos.none`.


**Linha 1704 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `tipo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1704:

**Linha 1705 — Assign** (nível 3 do bloco).

Associa `pedidos` a a chamada `pedidos.filter`, que restringe os resultados às condições informadas; não grava os registros; argumentos nomeados: `tipo_sanguineo=tipo`.

- `tipo_sanguineo=tipo`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1707 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `urgencia`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1707:

**Linha 1708 — Assign** (nível 3 do bloco).

Associa `pedidos` a a chamada `pedidos.filter`, que restringe os resultados às condições informadas; não grava os registros; argumentos nomeados: `urgencia=urgencia`.

- `urgencia=urgencia`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1710 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `cidade`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1710:

**Linha 1711 — Assign** (nível 3 do bloco).

Associa `pedidos` a a chamada `pedidos.filter`, que restringe os resultados às condições informadas; não grava os registros; argumentos nomeados: `cidade__icontains=cidade`.

- `cidade__icontains=cidade`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1713 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `hemocentro`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1713:

**Linha 1714 — Assign** (nível 3 do bloco).

Associa `pedidos` a a chamada `pedidos.filter`, que restringe os resultados às condições informadas; não grava os registros; argumentos nomeados: `hemocentro_destino__nome__icontains=hemocentro`.

- `hemocentro_destino__nome__icontains=hemocentro`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1718 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `data`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1718:

**Linha 1719 — Assign** (nível 3 do bloco).

Associa `pedidos` a a chamada `pedidos.filter`, que restringe os resultados às condições informadas; não grava os registros; argumentos nomeados: `data_criacao__date=data`.

- `data_criacao__date=data`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1721 — Assign** (nível 1 do bloco).

Associa `prioridade` a a chamada `Case`; argumentos posicionais: `When(urgencia=PedidoSangue.Urgencia.CRITICA, then=Value(1))`, `When(urgencia=PedidoSangue.Urgencia.ALTA, then=Value(2))`, `When(urgencia=PedidoSangue.Urgencia.MEDIA, then=Value(3))`, `When(urgencia=PedidoSangue.Urgencia.BAIXA, then=Value(4))`; argumentos nomeados: `default=Value(5)`, `output_field=IntegerField()`.

- `default=Value(5)`: valor inicial quando não é informado outro.
- `output_field=IntegerField()`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1742 — Assign** (nível 1 do bloco).

Associa `pedidos` a a chamada `pedidos.annotate(prioridade=prioridade).order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'prioridade'`, `'-data_criacao'`.


**Linha 1749 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/pedidos_listar.html'`, `{'form': form, 'pedidos': pedidos}` ao chamador.

### painel_validacao_pedidos — linhas 1759 a 1797

```python
@login_required
def painel_validacao_pedidos(request):
    """Painel de moderação do Administrador, sem publicar pedidos."""

    exigir_administrador(request.user)

    pedidos = (
        PedidoSangue.objects
        .select_related("solicitante", "hemocentro_destino")
        .prefetch_related(
            Prefetch(
                "validacoes",
                queryset=ValidacaoPedido.objects.select_related("moderador"),
            )
        )
        .filter(
            status__in=[
                PedidoSangue.Status.ENVIADA,
                PedidoSangue.Status.EM_ANALISE,
                PedidoSangue.Status.CORRECAO_SOLICITADA,
                PedidoSangue.Status.PUBLICADA,
            ]
        )
        .order_by("-duplicidade_suspeita", "-data_criacao")
    )

    status = request.GET.get("status")
    if status in dict(PedidoSangue.Status.choices):
        pedidos = pedidos.filter(status=status)

    return render(
        request,
        "accounts/painel_moderacao_pedidos.html",
        {
            "pedidos": pedidos,
            "status_opcoes": PedidoSangue.Status.choices,
            "status_atual": status or "",
        },
    )
```

**Explicação deste trecho:**

**Linha 1760 — FunctionDef** (nível 0 do bloco).

Define `painel_validacao_pedidos(request)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`.

Bloco `body` da linha 1760:

**Linha 1761 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1763 — Expr** (nível 1 do bloco).

Executa a chamada `exigir_administrador`; argumentos posicionais: `request.user`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1765 — Assign** (nível 1 do bloco).

Associa `pedidos` a a chamada `PedidoSangue.objects.select_related('solicitante', 'hemocentro_destino').prefetch_related(Prefetch('validacoes', queryset=ValidacaoPedido.objects.select_related('moderador'))).filter(status__in=[PedidoSangue.Status.ENVIADA, PedidoSangue.Status.EM_ANALISE, PedidoSangue.Status.CORRECAO_SOLICITADA, PedidoSangue.Status.PUBLICADA]).order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'-duplicidade_suspeita'`, `'-data_criacao'`.


**Linha 1785 — Assign** (nível 1 do bloco).

Associa `status` a a chamada `request.GET.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'status'`.


**Linha 1786 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `status` contido em `dict(PedidoSangue.Status.choices)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1786:

**Linha 1787 — Assign** (nível 2 do bloco).

Associa `pedidos` a a chamada `pedidos.filter`, que restringe os resultados às condições informadas; não grava os registros; argumentos nomeados: `status=status`.

- `status=status`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1789 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `render`, que combina template e contexto e devolve uma resposta HTML; argumentos posicionais: `request`, `'accounts/painel_moderacao_pedidos.html'`, `{'pedidos': pedidos, 'status_opcoes': PedidoSangue.Status.choices, 'status_atual': status or ''}` ao chamador.

### aprovar_pedido — linhas 1800 a 1825

```python
@login_required
@require_POST
def aprovar_pedido(request, id_pedido):
    """Publica uma solicitação após análise do Hemocentro de destino."""

    validar_publicacao_hemocentro(request.user)

    pedido = get_object_or_404(
        PedidoSangue,
        pk=id_pedido,
    )

    aprovar_pedido_servico(
        pedido=pedido,
        moderador=request.user,
        motivo=request.POST.get("motivo", ""),
        request=request,
    )

    messages.success(
        request,
        "Pedido publicado com sucesso." if hemocentro_aprovado(request.user)
        else "Pedido validado sem publicacao.",
    )

    return redirect("accounts:painel_pedidos_hemocentro")
```

**Explicação deste trecho:**

**Linha 1802 — FunctionDef** (nível 0 do bloco).

Define `aprovar_pedido(request, id_pedido)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`, `require_POST`.

Bloco `body` da linha 1802:

**Linha 1803 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1805 — Expr** (nível 1 do bloco).

Executa a chamada `validar_publicacao_hemocentro`; argumentos posicionais: `request.user`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1807 — Assign** (nível 1 do bloco).

Associa `pedido` a a chamada `get_object_or_404`, que busca um objeto na consulta fornecida; ausência gera resposta 404; argumentos posicionais: `PedidoSangue`; argumentos nomeados: `pk=id_pedido`.

- `pk=id_pedido`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1812 — Expr** (nível 1 do bloco).

Executa a chamada `aprovar_pedido_servico`; argumentos nomeados: `pedido=pedido`, `moderador=request.user`, `motivo=request.POST.get('motivo', '')`, `request=request`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1819 — Expr** (nível 1 do bloco).

Executa a chamada `messages.success`; argumentos posicionais: `request`, `'Pedido publicado com sucesso.' if hemocentro_aprovado(request.user) else 'Pedido validado sem publicacao.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1825 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:painel_pedidos_hemocentro'` ao chamador.

### recusar_pedido — linhas 1828 a 1852

```python
@login_required
@require_POST
def recusar_pedido(request, id_pedido):
    """Recusa uma solicitação pelo Hemocentro de destino."""

    validar_publicacao_hemocentro(request.user)

    pedido = get_object_or_404(
        PedidoSangue,
        pk=id_pedido,
    )

    recusar_pedido_servico(
        pedido=pedido,
        moderador=request.user,
        motivo=request.POST.get("motivo", ""),
        request=request,
    )

    messages.success(
        request,
        "Pedido recusado com sucesso.",
    )

    return redirect("accounts:painel_pedidos_hemocentro")
```

**Explicação deste trecho:**

**Linha 1830 — FunctionDef** (nível 0 do bloco).

Define `recusar_pedido(request, id_pedido)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`, `require_POST`.

Bloco `body` da linha 1830:

**Linha 1831 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1833 — Expr** (nível 1 do bloco).

Executa a chamada `validar_publicacao_hemocentro`; argumentos posicionais: `request.user`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1835 — Assign** (nível 1 do bloco).

Associa `pedido` a a chamada `get_object_or_404`, que busca um objeto na consulta fornecida; ausência gera resposta 404; argumentos posicionais: `PedidoSangue`; argumentos nomeados: `pk=id_pedido`.

- `pk=id_pedido`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1840 — Expr** (nível 1 do bloco).

Executa a chamada `recusar_pedido_servico`; argumentos nomeados: `pedido=pedido`, `moderador=request.user`, `motivo=request.POST.get('motivo', '')`, `request=request`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1847 — Expr** (nível 1 do bloco).

Executa a chamada `messages.success`; argumentos posicionais: `request`, `'Pedido recusado com sucesso.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1852 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:painel_pedidos_hemocentro'` ao chamador.

### solicitar_correcao_pedido — linhas 1855 a 1867

```python
@login_required
@require_POST
@exigir_hemocentro_aprovado
def solicitar_correcao_pedido(request, id_pedido):
    pedido = get_object_or_404(PedidoSangue, pk=id_pedido)
    solicitar_correcao_pedido_servico(
        pedido=pedido,
        moderador=request.user,
        motivo=request.POST.get("motivo", ""),
        request=request,
    )
    messages.success(request, "Correção solicitada ao responsável.")
    return redirect("accounts:painel_pedidos_hemocentro")
```

**Explicação deste trecho:**

**Linha 1858 — FunctionDef** (nível 0 do bloco).

Define `solicitar_correcao_pedido(request, id_pedido)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`, `require_POST`, `exigir_hemocentro_aprovado`.

Bloco `body` da linha 1858:

**Linha 1859 — Assign** (nível 1 do bloco).

Associa `pedido` a a chamada `get_object_or_404`, que busca um objeto na consulta fornecida; ausência gera resposta 404; argumentos posicionais: `PedidoSangue`; argumentos nomeados: `pk=id_pedido`.

- `pk=id_pedido`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1860 — Expr** (nível 1 do bloco).

Executa a chamada `solicitar_correcao_pedido_servico`; argumentos nomeados: `pedido=pedido`, `moderador=request.user`, `motivo=request.POST.get('motivo', '')`, `request=request`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1866 — Expr** (nível 1 do bloco).

Executa a chamada `messages.success`; argumentos posicionais: `request`, `'Correção solicitada ao responsável.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1867 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:painel_pedidos_hemocentro'` ao chamador.

### marcar_pedido_suspeito — linhas 1870 a 1886

```python
@login_required
@require_POST
def marcar_pedido_suspeito(request, id_pedido):
    """Registra uma suspeita para moderação, sem publicar o pedido."""

    pedido = get_object_or_404(PedidoSangue, pk=id_pedido)
    marcar_pedido_suspeito_servico(
        pedido=pedido,
        moderador=request.user,
        motivo=request.POST.get("motivo", ""),
        request=request,
    )
    messages.success(request, "Pedido marcado para moderação como suspeito.")

    if usuario_e_administrador(request.user):
        return redirect("accounts:painel_validacao_pedidos")
    return redirect("accounts:painel_pedidos_hemocentro")
```

**Explicação deste trecho:**

**Linha 1872 — FunctionDef** (nível 0 do bloco).

Define `marcar_pedido_suspeito(request, id_pedido)`. O corpo só executa quando a função/método é chamado. Decoradores: `login_required`, `require_POST`.

Bloco `body` da linha 1872:

**Linha 1873 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1875 — Assign** (nível 1 do bloco).

Associa `pedido` a a chamada `get_object_or_404`, que busca um objeto na consulta fornecida; ausência gera resposta 404; argumentos posicionais: `PedidoSangue`; argumentos nomeados: `pk=id_pedido`.

- `pk=id_pedido`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 1876 — Expr** (nível 1 do bloco).

Executa a chamada `marcar_pedido_suspeito_servico`; argumentos nomeados: `pedido=pedido`, `moderador=request.user`, `motivo=request.POST.get('motivo', '')`, `request=request`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1882 — Expr** (nível 1 do bloco).

Executa a chamada `messages.success`; argumentos posicionais: `request`, `'Pedido marcado para moderação como suspeito.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1884 — If** (nível 1 do bloco).

Escolhe um caminho verificando a chamada `usuario_e_administrador`; argumentos posicionais: `request.user`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1884:

**Linha 1885 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:painel_validacao_pedidos'` ao chamador.

**Linha 1886 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `redirect`, que devolve resposta para o navegador abrir outro endereço; argumentos posicionais: `'accounts:painel_pedidos_hemocentro'` ao chamador.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 615: `# Todo Hemocentro novo deve comecar como PENDENTE.`
- Linha 625: `# Registro do aceite da LGPD.`
- Linha 639: `# Cria a sessao do usuario.`
- Linha 642: `# Mensagem especifica para Hemocentro.`
- Linha 661: `# Se o formulario tiver erro, permanece na pagina`
- Linha 662: `# e o template podera exibir os erros de cada campo.`
- Linha 767: `# Busca a ultima analise administrativa do Hemocentro.`
- Linha 780: `# O resumo usa apenas registros do usuário autenticado. As respostas`
- Linha 781: `# detalhadas não são expostas no painel geral.`
- Linha 1013: `# A simplificada só fica disponível quando existe`
- Linha 1014: `# uma triagem extensa concluída válida como base.`
- Linha 1162: `# O botão anterior muda apenas o cursor e não valida campos da página.`
- Linha 1197: `# O serviço já cancelou a rápida antes de solicitar a troca.`
- Linha 1220: `# O serviço mantém o cursor na explicação quando a pessoa não entendeu`
- Linha 1221: `# e volta ao início quando ela escolhe revisar a confirmação final.`
- Linha 1320: `# Mantém compatibilidade com os parâmetros antigos da tela (q e tipo).`
- Linha 1699: `# A consulta pública nunca pode revelar solicitações em análise,`
- Linha 1700: `# recusadas ou dados ainda não publicados.`

