TIPOS_SANGUINEOS = ("O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+")

COMPATIBILIDADE_RECEBIMENTO = {
    "O-": ("O-",),
    "O+": ("O-", "O+"),
    "A-": ("O-", "A-"),
    "A+": ("O-", "O+", "A-", "A+"),
    "B-": ("O-", "B-"),
    "B+": ("O-", "O+", "B-", "B+"),
    "AB-": ("O-", "A-", "B-", "AB-"),
    "AB+": TIPOS_SANGUINEOS,
}

POPULACAO_APROXIMADA = {
    "O-": "7%",
    "O+": "38%",
    "A-": "6%",
    "A+": "34%",
    "B-": "2%",
    "B+": "9%",
    "AB-": "1%",
    "AB+": "3%",
}


def normalizar_tipo_sanguineo(tipo_sanguineo):
    tipo = (tipo_sanguineo or "").strip().upper()
    if tipo not in TIPOS_SANGUINEOS:
        raise ValueError("Tipo sanguineo invalido.")
    return tipo


def doadores_compativeis_para(tipo_solicitado):
    tipo = normalizar_tipo_sanguineo(tipo_solicitado)
    return COMPATIBILIDADE_RECEBIMENTO[tipo]


def tipos_que_recebem_de(tipo_doador):
    tipo = normalizar_tipo_sanguineo(tipo_doador)
    return tuple(
        receptor
        for receptor, doadores in COMPATIBILIDADE_RECEBIMENTO.items()
        if tipo in doadores
    )


def tabela_de_compatibilidade():
    return [
        {
            "tipo": tipo,
            "doar_para": tipos_que_recebem_de(tipo),
            "receber_de": doadores_compativeis_para(tipo),
            "populacao": POPULACAO_APROXIMADA[tipo],
        }
        for tipo in TIPOS_SANGUINEOS
    ]


def doadores_aptos_para_convocacao(tipo_solicitado):
    """Aplica a mesma elegibilidade para os alertas de estoque e pedidos."""
    # Imports locais evitam o ciclo: models usa TIPOS_SANGUINEOS deste modulo.
    from django.conf import settings
    from django.db.models import Exists, OuterRef, Q, Subquery
    from django.utils import timezone
    from .models import ConsentimentoLGPD, Triagem, Usuario

    ultima_triagem = Triagem.objects.filter(
        usuario=OuterRef("pk"), status=Triagem.Status.CONCLUIDA,
    ).order_by("-finalizada_em", "-iniciada_em", "-id_triagem")
    consentimento = ConsentimentoLGPD.objects.filter(
        usuario=OuterRef("pk"),
        tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
        versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO,
        aceito=True, revogado_em__isnull=True,
    )
    return (
        Usuario.objects.filter(
            perfil=Usuario.Perfil.DOADOR, is_active=True, suspensa=False,
            aceita_notificacoes_pedidos=True,
            tipo_sanguineo__in=doadores_compativeis_para(tipo_solicitado),
        ).annotate(
            resultado_ultima_triagem=Subquery(ultima_triagem.values("resultado")[:1]),
            liberacao_ultima_triagem=Subquery(ultima_triagem.values("data_liberacao")[:1]),
            consentimento_convocacao=Exists(consentimento),
        ).filter(
            resultado_ultima_triagem=Triagem.Resultado.APTO,
            consentimento_convocacao=True,
        ).filter(
            Q(liberacao_ultima_triagem__isnull=True)
            | Q(liberacao_ultima_triagem__lte=timezone.localdate())
        ).order_by("pk")
    )


def limite_convocacao_atingido(usuario):
    """Soma os alertas de estoque e pedidos, mesmo os que ja foram lidos."""
    from datetime import timedelta
    from django.conf import settings
    from django.utils import timezone
    from .models import Notificacao

    inicio = timezone.now() - timedelta(hours=settings.CONVOCACAO_INTERVALO_HORAS)
    quantidade = Notificacao.objects.filter(
        usuario=usuario,
        tipo__in=[Notificacao.Tipo.ESTOQUE_BAIXO, Notificacao.Tipo.ESTOQUE_CRITICO,
                  Notificacao.Tipo.PEDIDO_COMPATIVEL],
        criada_em__gte=inicio,
    ).count()
    return quantidade >= settings.CONVOCACAO_LIMITE_NOTIFICACOES


def atualizar_preferencia_convocacao(usuario, aceita, request=None):
    """Registra a escolha explicita e sua revogacao nas tabelas existentes."""
    from django.conf import settings
    from django.core.exceptions import PermissionDenied
    from django.db import transaction
    from django.utils import timezone
    from .auditoria import obter_ip, registrar_auditoria
    from .models import AuditoriaAcaoCritica, ConsentimentoLGPD, Usuario

    if not usuario.is_authenticated or usuario.perfil != Usuario.Perfil.DOADOR:
        raise PermissionDenied("Somente Doadores podem configurar convocacoes.")
    with transaction.atomic():
        usuario = Usuario.objects.select_for_update().get(pk=usuario.pk)
        anterior = usuario.aceita_notificacoes_pedidos
        usuario.aceita_notificacoes_pedidos = bool(aceita)
        usuario.save(update_fields=["aceita_notificacoes_pedidos", "atualizado_em"])
        consentimento, criado = ConsentimentoLGPD.objects.get_or_create(
            usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
            versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO,
            defaults={"aceito": bool(aceita), "ip": obter_ip(request),
                      "revogado_em": None if aceita else timezone.now()},
        )
        if not criado:
            if aceita and (not consentimento.aceito or consentimento.revogado_em):
                consentimento.data_aceite = timezone.now()
            consentimento.aceito = bool(aceita)
            consentimento.revogado_em = None if aceita else timezone.now()
            consentimento.ip = obter_ip(request)
            consentimento.save(update_fields=["aceito", "revogado_em", "data_aceite", "ip"])
        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.MODERACAO,
            usuario=usuario, alvo=consentimento, request=request,
            descricao="Preferencia de convocacao atualizada pelo doador.",
            metadados={"evento": "PREFERENCIA_CONVOCACAO", "antes": anterior,
                       "depois": bool(aceita), "versao_termo": consentimento.versao_termo},
        )
