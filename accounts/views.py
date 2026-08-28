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

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CadastroUsuarioForm
from .models import ConsentimentoLGPD, Usuario, ValidacaoHemocentro
from .validacao_hemocentro import (
    aprovar_hemocentro as aprovar_hemocentro_servico,
    recusar_hemocentro as recusar_hemocentro_servico,
    solicitar_correcao_hemocentro as solicitar_correcao_hemocentro_servico,
    usuario_e_administrador,
)
from .compatibilidade import (
    TIPOS_SANGUINEOS,
    doadores_compativeis_para,
    tabela_de_compatibilidade,
    tipos_que_recebem_de,
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


PEDIDOS_ATIVOS = [
    {
        "titulo": "Solicitacao para cirurgia cardiaca",
        "tipo_sanguineo": "O-",
        "cidade": "Sao Paulo",
        "urgencia": "Alta",
    },
    {
        "titulo": "Reposicao de estoque pediatrico",
        "tipo_sanguineo": "B-",
        "cidade": "Campinas",
        "urgencia": "Alta",
    },
    {
        "titulo": "Apoio para tratamento oncologico",
        "tipo_sanguineo": "A+",
        "cidade": "Santos",
        "urgencia": "Media",
    },
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
        "descricao": "Organize sua jornada de doacao e acompanhe sua evolucao.",
        "acoes": [
            "Responder ao questionario de saude da pre-triagem.",
            "Registrar intencao de doacao em um posto de coleta.",
            "Confirmar presenca em mutiroes e campanhas.",
            "Consultar historico de doacoes, pontos e ranking.",
        ],
        "mostra_campanhas": True,
        "mostra_pedidos": True,
        "mostra_estoque": True,
    },
    Usuario.Perfil.RECEPTOR: {
        "rotulo": "Receptor / Solicitante",
        "titulo": "Painel do receptor",
        "descricao": "Publique pedidos de sangue e acompanhe a disponibilidade.",
        "acoes": [
            "Publicar pedido de socorro para si, familiar ou amigo.",
            "Informar tipo sanguineo, cidade e urgencia do pedido.",
            "Verificar bolsas disponiveis no estoque geral.",
            "Acompanhar a situacao dos pedidos publicados.",
        ],
        "mostra_campanhas": False,
        "mostra_pedidos": True,
        "mostra_estoque": True,
    },
    Usuario.Perfil.OBSERVADOR: {
        "rotulo": "Observador",
        "titulo": "Painel do observador",
        "descricao": "Acompanhe o cenario de pedidos e estoques ativos.",
        "acoes": [
            "Consultar pedidos de sangue ativos.",
            "Acompanhar os niveis gerais dos estoques.",
            "Pesquisar postos de coleta por cidade ou UF.",
        ],
        "mostra_campanhas": False,
        "mostra_pedidos": True,
        "mostra_estoque": True,
    },
    Usuario.Perfil.HEMOCENTRO: {
        "rotulo": "Hemocentro",
        "titulo": "Painel do hemocentro",
        "descricao": "Gerencie a operacao de doacao e disponibilidade de bolsas.",
        "acoes": [
            "Atualizar quantidade de bolsas por tipo sanguineo.",
            "Criar campanhas e mutiroes de arrecadacao.",
            "Confirmar comparecimento e doacao realizada pelo doador.",
            "Monitorar pedidos ativos que dependem do estoque.",
        ],
        "mostra_campanhas": True,
        "mostra_pedidos": True,
        "mostra_estoque": True,
    },
    Usuario.Perfil.ADMINISTRADOR: {
        "rotulo": "Administrador",
        "titulo": "Painel administrativo",
        "descricao": "Acompanhe cadastros, consentimentos e operacoes internas.",
        "acoes": [
            "Gerenciar usuarios e perfis no painel administrativo.",
            "Consultar consentimentos LGPD registrados.",
            "Apoiar hemocentros e solicitantes em fluxos excepcionais.",
        ],
        "mostra_campanhas": True,
        "mostra_pedidos": True,
        "mostra_estoque": True,
    },
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
        "pedidos_ativos": PEDIDOS_ATIVOS,
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

    painel = PAINEIS_POR_PERFIL.get(
        request.user.perfil,
        PAINEIS_POR_PERFIL[Usuario.Perfil.OBSERVADOR],
    )

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

    contexto = {
        "painel": painel,
        "postos": POSTOS_COLETA,
        "estoque_geral": ESTOQUE_GERAL,
        "pedidos_ativos": PEDIDOS_ATIVOS,
        "campanhas_ativas": CAMPANHAS_ATIVAS,
        "validacao_atual": validacao_atual,
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