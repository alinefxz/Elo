"""
Funcoes centrais para registrar auditorias de acoes criticas.

As demais partes do sistema devem usar ``registrar_auditoria`` em vez de criar
AuditoriaAcaoCritica diretamente. Isso mantem saneamento de metadados,
captura de IP e regras de seguranca em um unico ponto.
"""

from ipaddress import ip_address

from django.forms.models import model_to_dict
from django.utils.deprecation import MiddlewareMixin

from .models import AuditoriaAcaoCritica


CAMPOS_SENSIVEIS = {
    "password",
    "senha",
    "senha_hash",
    "token",
    "csrfmiddlewaretoken",
    "secret",
    "authorization",
}

"""serve para identiifcar de onde a ação veio"""
def obter_ip(request):
    """Usa o endereco da conexao, sem confiar em cabecalhos enviados pelo cliente."""

    if not request:
        return None

    try:
        return str(ip_address(request.META.get("REMOTE_ADDR", "")))
    except ValueError:
        return None


def obter_user_agent(request):
    """Extrai o user agent sem obrigar chamadas internas a terem request."""

    if not request:
        return ""
    return request.META.get("HTTP_USER_AGENT", "")


def limpar_metadados(valor):
    """Remove dados sensiveis de estruturas simples antes de salvar auditoria."""

    if isinstance(valor, dict):
        metadados_limpos = {}
        for chave, item in valor.items():
            chave_texto = str(chave)
            if chave_texto.lower() in CAMPOS_SENSIVEIS:
                metadados_limpos[chave_texto] = "[removido]"
            else:
                metadados_limpos[chave_texto] = limpar_metadados(item)
        return metadados_limpos

    if isinstance(valor, (list, tuple, set)):
        return [limpar_metadados(item) for item in valor]

    return valor


def identificar_alvo(alvo):
    """Transforma um model ou valor simples em alvo_tipo e alvo_id."""

    if alvo is None:
        return "", ""

    if hasattr(alvo, "_meta"):
        alvo_tipo = alvo._meta.label
        chave_primaria = alvo.pk
        return alvo_tipo, str(chave_primaria or "")

    return alvo.__class__.__name__, str(alvo)


def registrar_auditoria(
    *,
    acao,
    usuario=None,
    resultado=AuditoriaAcaoCritica.Resultado.SUCESSO,
    alvo=None,
    alvo_tipo="",
    alvo_id="",
    descricao="",
    request=None,
    ip=None,
    user_agent="",
    metadados=None,
):
    """Cria um registro de auditoria padronizado e sanitizado."""

    tipo_detectado, id_detectado = identificar_alvo(alvo)
    usuario_autenticado = getattr(usuario, "is_authenticated", False)

    if usuario is not None and not usuario_autenticado:
        usuario = None

    return AuditoriaAcaoCritica.objects.create(
        usuario=usuario,
        acao=acao,
        resultado=resultado,
        alvo_tipo=alvo_tipo or tipo_detectado,
        alvo_id=alvo_id or id_detectado,
        descricao=descricao,
        ip=ip or obter_ip(request),
        user_agent=user_agent or obter_user_agent(request),
        metadados=limpar_metadados(metadados or {}),
    )


def campos_sensiveis_alterados(objeto, campos):
    """Compara campos sensiveis de um model antes e depois da alteracao."""

    if not objeto.pk:
        return {}

    antigo = objeto.__class__.objects.filter(pk=objeto.pk).first()
    if not antigo:
        return {}

    alteracoes = {}
    for campo in campos:
        valor_antigo = getattr(antigo, campo)
        valor_novo = getattr(objeto, campo)
        if valor_antigo != valor_novo:
            alteracoes[campo] = {
                "antes": str(valor_antigo),
                "depois": str(valor_novo),
            }
    return alteracoes


def snapshot_campos(objeto, campos):
    """Retorna um dicionario com campos simples de um model."""

    dados = model_to_dict(objeto, fields=campos)
    return {campo: str(valor) for campo, valor in dados.items()}


class AuditoriaAcessosMiddleware(MiddlewareMixin):
    """Audita respostas protegidas sem copiar formularios ou dados clinicos."""

    ROTAS_SENSIVEIS = {
        "accounts:triagem_pergunta", "accounts:triagem_resultado",
        "accounts:triagem_historico", "accounts:painel_validacao_pedidos",
        "accounts:triagem_revisao", "accounts:minhas_solicitacoes",
        "accounts:painel_pedidos_hemocentro",
    }
    MODELOS_SENSIVEIS_ADMIN = {
        "usuario", "triagem", "respostatriagem", "consentimentolgpd",
        "pedidosangue", "validacaopedido", "validacaohemocentro",
        "notificacao", "auditoriaacaocritica",
    }

    def process_response(self, request, response):
        rota = getattr(request, "resolver_match", None)
        if rota is None:
            return response
        usuario = getattr(request, "user", None)
        autenticado = getattr(usuario, "is_authenticated", False)
        nome = rota.view_name
        protegido = nome.startswith("accounts:") and (
            nome in self.ROTAS_SENSIVEIS
            or any(parte in nome for parte in (
                "triagem_iniciar", "estoque_hemocentro", "cadastrar_estoque",
                "atualizar_estoque", "aprovar_pedido", "recusar_pedido",
                "pedido_publicar", "criar_pedido_sangue",
                "solicitar_correcao_pedido", "marcar_pedido_suspeito",
            ))
        )
        login_exigido = response.status_code == 302 and not autenticado and protegido
        bloqueado = response.status_code == 403 or (
            response.status_code == 404 and protegido and autenticado
        ) or login_exigido
        admin_sensivel = nome.startswith("admin:") and any(
            nome.startswith("admin:accounts_" + modelo + "_")
            for modelo in self.MODELOS_SENSIVEIS_ADMIN
        )
        dados_sensiveis = nome in self.ROTAS_SENSIVEIS or admin_sensivel or (
            nome == "accounts:dashboard" and getattr(usuario, "perfil", "") == "DOADOR"
        )
        if bloqueado:
            registrar_auditoria(
                acao=AuditoriaAcaoCritica.Acao.MODERACAO,
                resultado=AuditoriaAcaoCritica.Resultado.BLOQUEADO,
                usuario=usuario, request=request,
                descricao="Tentativa de acesso bloqueada.",
                metadados={"evento": "TENTATIVA_ACESSO", "rota": nome,
                           "metodo": request.method, "status_http": response.status_code},
            )
        elif dados_sensiveis and request.method == "GET" and response.status_code == 200 and autenticado:
            registrar_auditoria(
                acao=AuditoriaAcaoCritica.Acao.ACESSO_DADOS_SENSIVEIS,
                usuario=usuario, request=request,
                descricao="Consulta de dados sensiveis.",
                metadados={"rota": nome, "parametros": rota.kwargs},
            )
        return response
