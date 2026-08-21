"""
Funcoes centrais para registrar auditorias de acoes criticas.

As demais partes do sistema devem usar ``registrar_auditoria`` em vez de criar
AuditoriaAcaoCritica diretamente. Isso mantem saneamento de metadados,
captura de IP e regras de seguranca em um unico ponto.
"""

from django.forms.models import model_to_dict

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


def obter_ip(request):
    """Extrai o IP de uma requisicao HTTP, considerando proxies."""

    if not request:
        return None

    encaminhado = request.META.get("HTTP_X_FORWARDED_FOR")
    if encaminhado:
        return encaminhado.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


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
