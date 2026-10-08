from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from .auditoria import registrar_auditoria
from .models import (
    AuditoriaAcaoCritica,
    PedidoSangue,
    Usuario,
    ValidacaoPedido,
)
from .validacao_hemocentro import hemocentro_aprovado, usuario_e_administrador


def validar_dados_pedido(pedido):
    """
    Valida as informações básicas antes da decisão administrativa.
    """

    if not pedido.titulo.strip():
        raise ValidationError(
            "O pedido precisa possuir um título."
        )

    if not pedido.tipo_sanguineo:
        raise ValidationError(
            "Informe o tipo sanguíneo."
        )

    if not pedido.urgencia:
        raise ValidationError(
            "Informe a urgência."
        )

    if not pedido.cidade.strip():
        raise ValidationError(
            "Informe a cidade."
        )

    if not pedido.descricao.strip():
        raise ValidationError(
            "Informe a descrição do pedido."
        )

    if not pedido.hemocentro_destino_id:
        raise ValidationError(
            "Informe o Hemocentro de destino."
        )

    if (
        pedido.hemocentro_destino.perfil
        != Usuario.Perfil.HEMOCENTRO
    ):
        raise ValidationError(
            "O destino precisa ser um Hemocentro."
        )

    if (
        pedido.hemocentro_destino.status_validacao
        != Usuario.StatusValidacaoHemocentro.APROVADO
    ):
        raise ValidationError(
            "O Hemocentro de destino precisa estar aprovado."
        )


def criar_pedido_pendente(
    *,
    dados,
    solicitante,
):
    """
    Cria o pedido sem publicá-lo.
    """

    if solicitante.perfil != Usuario.Perfil.RECEPTOR:
        raise PermissionDenied(
            "Somente Receptor/Solicitante pode criar "
            "pedidos de sangue."
        )

    pedido = PedidoSangue(
        solicitante=solicitante,
        status=(
            PedidoSangue.Status.PENDENTE_VALIDACAO
        ),
        **dados,
    )

    validar_dados_pedido(pedido)

    pedido.save()

    return pedido


@transaction.atomic
def registrar_decisao_validacao_pedido(
    *,
    pedido,
    moderador,
    status_validacao,
    motivo="",
    request=None,
):
    """
    Registra a decisão administrativa e atualiza
    o status do pedido.
    """

    institucional = hemocentro_aprovado(moderador)
    if not usuario_e_administrador(moderador) and not institucional:
        raise PermissionDenied(
            "Somente administradores ou Hemocentros aprovados podem analisar pedidos."
        )

    motivo = (motivo or "").strip()

    if status_validacao not in [
        ValidacaoPedido.StatusValidacao.APROVADO,
        ValidacaoPedido.StatusValidacao.RECUSADO,
        ValidacaoPedido.StatusValidacao.SUSPEITO,
    ]:
        raise ValidationError(
            "Status de validação inválido."
        )

    pedido = (
        PedidoSangue.objects
        .select_for_update()
        .select_related(
            "solicitante",
            "hemocentro_destino",
        )
        .get(pk=pedido.pk)
    )

    if institucional and pedido.hemocentro_destino_id != moderador.pk:
        raise PermissionDenied("O pedido pertence a outro Hemocentro.")

    status_anterior = pedido.status
    if status_validacao == (
        ValidacaoPedido.StatusValidacao.APROVADO
    ):
        # A decisao administrativa registra a validacao sem publicar.
        novo_status = (
            PedidoSangue.Status.ATIVO if institucional else pedido.status
        )
        if institucional:
            validar_dados_pedido(pedido)

        if not motivo:
            motivo = (
                "Pedido publicado pelo Hemocentro." if institucional
                else "Pedido validado pelo administrador, sem publicacao."
            )

    elif status_validacao == (
        ValidacaoPedido.StatusValidacao.RECUSADO
    ):
        novo_status = PedidoSangue.Status.RECUSADO

        if not motivo:
            motivo = (
                "Pedido recusado pelo Hemocentro." if institucional
                else "Pedido recusado pelo administrador."
            )

    else:
        novo_status = PedidoSangue.Status.SUSPEITO

        if not motivo:
            motivo = (
                "Pedido marcado como suspeito "
                "e mantido em análise."
            )

    pedido.status = novo_status

    pedido.save(
        update_fields=[
            "status",
            "atualizado_em",
        ]
    )

    validacao = ValidacaoPedido.objects.create(
        pedido=pedido,
        status_validacao=status_validacao,
        motivo=motivo,
        moderador=moderador,
    )

    registrar_auditoria(
        acao=AuditoriaAcaoCritica.Acao.MODERACAO,
        resultado=AuditoriaAcaoCritica.Resultado.SUCESSO,
        usuario=moderador,
        alvo=pedido,
        descricao=(
            "Decisao institucional sobre pedido de sangue." if institucional
            else "Validacao administrativa de pedido de sangue."
        ),
        request=request,
        metadados={
            "evento": "PUBLICACAO_PEDIDO" if institucional and status_validacao == ValidacaoPedido.StatusValidacao.APROVADO else "VALIDACAO_PEDIDO",
            "status_anterior": status_anterior,
            "perfil_responsavel": moderador.perfil,
            "id_pedido": pedido.pk,
            "id_validacao": validacao.pk,
            "status_validacao": status_validacao,
            "status_pedido": novo_status,
            "motivo": motivo,
        },
    )

    return validacao


def aprovar_pedido(
    *,
    pedido,
    moderador,
    motivo="",
    request=None,
):
    return registrar_decisao_validacao_pedido(
        pedido=pedido,
        moderador=moderador,
        status_validacao=(
            ValidacaoPedido.StatusValidacao.APROVADO
        ),
        motivo=motivo,
        request=request,
    )


def recusar_pedido(
    *,
    pedido,
    moderador,
    motivo="",
    request=None,
):
    return registrar_decisao_validacao_pedido(
        pedido=pedido,
        moderador=moderador,
        status_validacao=(
            ValidacaoPedido.StatusValidacao.RECUSADO
        ),
        motivo=motivo,
        request=request,
    )


def marcar_pedido_suspeito(
    *,
    pedido,
    moderador,
    motivo="",
    request=None,
):
    return registrar_decisao_validacao_pedido(
        pedido=pedido,
        moderador=moderador,
        status_validacao=(
            ValidacaoPedido.StatusValidacao.SUSPEITO
        ),
        motivo=motivo,
        request=request,
    )
