"""
Validacao de pedidos de sangue.

Este arquivo segue a mesma ideia de validacao_hemocentro.py:
centraliza regras de negocio fora da view para manter o fluxo testavel,
auditavel e reutilizavel.
"""

from datetime import timedelta

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone

from .auditoria import registrar_auditoria
from .models import AuditoriaAcaoCritica, PedidoSangue, Usuario, ValidacaoPedido
from .validacao_hemocentro import usuario_e_administrador


def validar_campos_minimos_pedido(pedido):
    """
    Garante os campos minimos do RF.

    Campos obrigatorios:
    - titulo;
    - tipo sanguineo;
    - urgencia;
    - cidade;
    - descricao;
    - hemocentro de destino.
    """

    campos = [
        pedido.titulo,
        pedido.tipo_sanguineo,
        pedido.urgencia,
        pedido.cidade,
        pedido.descricao,
        pedido.hemocentro_destino_id,
    ]

    if any(not campo for campo in campos):
        raise ValidationError("Preencha todos os campos obrigatorios do pedido.")

    if pedido.hemocentro_destino.perfil != Usuario.Perfil.HEMOCENTRO:
        raise ValidationError("O hemocentro de destino precisa estar cadastrado.")


def pedido_duplicado(pedido):
    """
    Impede duplicidade evidente.

    Considera duplicado quando o mesmo solicitante cria pedido parecido
    para o mesmo hemocentro, tipo sanguineo e cidade em ate 48 horas.
    """

    limite = timezone.now() - timedelta(hours=48)

    return (
        PedidoSangue.objects
        .filter(
            solicitante=pedido.solicitante,
            hemocentro_destino=pedido.hemocentro_destino,
            tipo_sanguineo=pedido.tipo_sanguineo,
            cidade__iexact=pedido.cidade,
            status__in=[
                PedidoSangue.Status.PENDENTE_VALIDACAO,
                PedidoSangue.Status.ATIVO,
                PedidoSangue.Status.SUSPEITO,
            ],
            data_criacao__gte=limite,
        )
        .exclude(pk=pedido.pk)
        .exists()
    )


def motivos_suspeita_pedido(pedido):
    """
    Retorna uma lista de motivos caso o pedido pareca suspeito.

    A regra nao recusa automaticamente: ela sinaliza para moderacao.
    """

    motivos = []
    limite = timezone.now() - timedelta(hours=24)

    if pedido.urgencia in [
        PedidoSangue.Urgencia.ALTA,
        PedidoSangue.Urgencia.CRITICA,
    ]:
        if len((pedido.justificativa_urgencia or "").strip()) < 20:
            motivos.append("Urgencia alta/critica sem justificativa suficiente.")

    pedidos_recentes = (
        PedidoSangue.objects
        .filter(
            solicitante=pedido.solicitante,
            data_criacao__gte=limite,
            status__in=[
                PedidoSangue.Status.ATIVO,
                PedidoSangue.Status.SUSPEITO,
                PedidoSangue.Status.PENDENTE_VALIDACAO,
            ],
        )
        .exclude(pk=pedido.pk)
        .count()
    )

    if pedidos_recentes >= 3:
        motivos.append("Solicitante possui muitos pedidos recentes.")

    if len((pedido.descricao or "").strip()) < 20:
        motivos.append("Descricao muito curta para justificar o pedido.")

    return motivos


def validar_pedido_sangue(*, pedido, moderador=None, request=None):
    """
    UC_17 - Validar Pedido.

    Se estiver correto, ativa o pedido.
    Se parecer suspeito, muda o status para SUSPEITO.
    Sempre registra uma linha em validacoes_pedido.
    """

    validar_campos_minimos_pedido(pedido)

    if pedido_duplicado(pedido):
        raise ValidationError(
            "Ja existe um pedido muito semelhante nas ultimas 48 horas."
        )

    motivos = motivos_suspeita_pedido(pedido)

    with transaction.atomic():
        pedido_atualizado = PedidoSangue.objects.select_for_update().get(
            pk=pedido.pk
        )

        if motivos:
            pedido_atualizado.status = PedidoSangue.Status.SUSPEITO
            status_validacao = ValidacaoPedido.StatusValidacao.SUSPEITO
            motivo = " ".join(motivos)
        else:
            pedido_atualizado.status = PedidoSangue.Status.ATIVO
            status_validacao = ValidacaoPedido.StatusValidacao.APROVADO
            motivo = "Pedido aprovado automaticamente."

        pedido_atualizado.save(update_fields=["status", "atualizado_em"])

        validacao = ValidacaoPedido.objects.create(
            pedido=pedido_atualizado,
            status_validacao=status_validacao,
            motivo=motivo,
            moderador=moderador,
        )

        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.MODERACAO,
            resultado=AuditoriaAcaoCritica.Resultado.SUCESSO,
            usuario=moderador or pedido_atualizado.solicitante,
            alvo=pedido_atualizado,
            descricao="Validacao de pedido de sangue.",
            request=request,
            metadados={
                "id_validacao": validacao.pk,
                "status_pedido": pedido_atualizado.status,
                "motivo": motivo,
            },
        )

    return validacao


def registrar_pedido_com_validacao(*, dados, solicitante, request=None):
    """
    Cria o pedido e imediatamente executa a validacao.

    Se alguma regra falhar, a transacao desfaz o pedido criado.
    """

    with transaction.atomic():
        pedido = PedidoSangue.objects.create(
            solicitante=solicitante,
            status=PedidoSangue.Status.PENDENTE_VALIDACAO,
            **dados,
        )

        validar_pedido_sangue(
            pedido=pedido,
            moderador=None,
            request=request,
        )

    return pedido


def registrar_decisao_validacao_pedido(
    *,
    pedido,
    moderador,
    status_validacao,
    motivo="",
    request=None,
):
    """
    Moderacao manual do pedido.

    Apenas administrador pode aprovar ou recusar pedido suspeito.
    """

    if not usuario_e_administrador(moderador):
        raise PermissionDenied("Somente administradores podem validar pedidos.")

    motivo = (motivo or "").strip()

    with transaction.atomic():
        pedido_atualizado = PedidoSangue.objects.select_for_update().get(
            pk=pedido.pk
        )

        if status_validacao == ValidacaoPedido.StatusValidacao.APROVADO:
            pedido_atualizado.status = PedidoSangue.Status.ATIVO
            motivo = motivo or "Pedido aprovado pelo moderador."

        elif status_validacao == ValidacaoPedido.StatusValidacao.RECUSADO:
            pedido_atualizado.status = PedidoSangue.Status.RECUSADO
            motivo = motivo or "Pedido recusado pelo moderador."

        else:
            pedido_atualizado.status = PedidoSangue.Status.SUSPEITO
            motivo = motivo or "Pedido mantido como suspeito para moderacao."

        pedido_atualizado.save(update_fields=["status", "atualizado_em"])

        validacao = ValidacaoPedido.objects.create(
            pedido=pedido_atualizado,
            status_validacao=status_validacao,
            motivo=motivo,
            moderador=moderador,
        )

        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.MODERACAO,
            resultado=AuditoriaAcaoCritica.Resultado.SUCESSO,
            usuario=moderador,
            alvo=pedido_atualizado,
            descricao="Moderacao manual de pedido de sangue.",
            request=request,
            metadados={
                "id_validacao": validacao.pk,
                "status_validacao": status_validacao,
                "motivo": motivo,
            },
        )

    return validacao


def aprovar_pedido(*, pedido, moderador, motivo="", request=None):
    return registrar_decisao_validacao_pedido(
        pedido=pedido,
        moderador=moderador,
        status_validacao=ValidacaoPedido.StatusValidacao.APROVADO,
        motivo=motivo,
        request=request,
    )


def recusar_pedido(*, pedido, moderador, motivo="", request=None):
    return registrar_decisao_validacao_pedido(
        pedido=pedido,
        moderador=moderador,
        status_validacao=ValidacaoPedido.StatusValidacao.RECUSADO,
        motivo=motivo,
        request=request,
    )