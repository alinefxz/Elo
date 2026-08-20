"""
RESUMO DO ARQUIVO
=================
As views recebem requisicoes do navegador, executam a regra da pagina e
devolvem uma resposta.

Fluxo do cadastro:
GET -> mostra formulario vazio.
POST -> valida -> grava usuario + consentimento -> cria sessao -> dashboard.

O cadastro usa uma transacao para impedir que apenas metade da operacao seja
salva. O dashboard usa login_required para bloquear visitantes.
"""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import CadastroUsuarioForm
from .models import ConsentimentoLGPD, Usuario


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

    # Proxies podem informar uma lista de IPs no cabecalho X-Forwarded-For.
    # O primeiro normalmente representa o cliente original.
    encaminhado = request.META.get("HTTP_X_FORWARDED_FOR")
    if encaminhado:
        return encaminhado.split(",")[0].strip()

    # Em desenvolvimento local, REMOTE_ADDR normalmente sera 127.0.0.1.
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


def inicio(request):
    """Mostra o acesso publico usado pelo ator Visitante."""

    consulta = request.GET.get("q", "")
    contexto = {
        "consulta": consulta,
        "postos": filtrar_postos(consulta),
        "estoque_geral": ESTOQUE_GERAL,
        "pedidos_ativos": PEDIDOS_ATIVOS,
    }
    return render(request, "accounts/inicio.html", contexto)


def cadastro(request):
    """Mostra o formulario e processa a criacao de uma conta do Elo."""

    # Uma pessoa que ja entrou nao precisa abrir cadastro novamente.
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    # GET apenas exibe a pagina. POST significa que o formulario foi enviado.
    if request.method == "POST":
        # request.POST contem os valores enviados pelos inputs do HTML.
        form = CadastroUsuarioForm(request.POST)

        # is_valid executa validacoes de campo, senha e unicidade.
        if form.is_valid():
            # atomic abre uma transacao no PostgreSQL. Se a criacao do usuario
            # ou do consentimento falhar, o banco desfaz as duas operacoes.
            with transaction.atomic():
                # UserCreationForm chama set_password antes de salvar.
                usuario = form.save()

                # O aceite nao pertence a usuarios: ele gera uma linha propria
                # em consentimentos_lgpd ligada pela chave estrangeira.
                ConsentimentoLGPD.objects.create(
                    usuario=usuario,
                    tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL,
                    versao_termo="1.0",
                    aceito=True,
                    ip=obter_ip(request),
                )

            # login grava a identidade do usuario na sessao do Django.
            # O navegador recebe apenas um cookie de sessao, nunca a senha.
            login(request, usuario)

            # A mensagem fica na sessao ate base.html exibi-la uma vez.
            messages.success(request, "Cadastro realizado com sucesso.")
            return redirect("accounts:dashboard")
    else:
        # No GET, nao existem dados enviados: criamos um formulario vazio.
        form = CadastroUsuarioForm()

    # render combina o template com o dicionario de contexto.
    # O HTML acessa o objeto usando a variavel {{ form }}.
    return render(request, "accounts/cadastro.html", {"form": form})


@login_required
def dashboard(request):
    """Mostra o painel protegido particularizado pelo perfil do usuario."""

    # Se nao houver sessao valida, login_required redireciona para LOGIN_URL.
    painel = PAINEIS_POR_PERFIL.get(
        request.user.perfil,
        PAINEIS_POR_PERFIL[Usuario.Perfil.OBSERVADOR],
    )
    contexto = {
        "painel": painel,
        "postos": POSTOS_COLETA,
        "estoque_geral": ESTOQUE_GERAL,
        "pedidos_ativos": PEDIDOS_ATIVOS,
        "campanhas_ativas": CAMPANHAS_ATIVAS,
    }
    return render(request, "accounts/dashboard.html", contexto)
