from django.core.exceptions import PermissionDenied, ValidationError
from django.core.validators import validate_email
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .auditoria import registrar_auditoria
from .models import (
    AuditoriaAcaoCritica,
    PedidoSangue,
    Usuario,
    ValidacaoPedido,
)
from .validacao_hemocentro import hemocentro_aprovado


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

    if not pedido.nome_solicitante.strip():
        raise ValidationError("Informe o nome ou identificação do solicitante.")

    if not pedido.contato.strip():
        raise ValidationError("Informe um e-mail para retorno.")

    try:
        validate_email(pedido.contato.strip())
    except ValidationError as erro:
        raise ValidationError("Informe um e-mail válido para retorno.") from erro

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
    Cria um pedido de sangue sem publicá-lo imediatamente.

    Podem criar pedidos:
    - Receptor/Solicitante;
    - Hemocentro aprovado.

    Um Hemocentro pendente, recusado ou em correção não pode
    criar pedidos institucionais.
    """

    if getattr(solicitante, "is_authenticated", False) and solicitante.perfil in {
        Usuario.Perfil.HEMOCENTRO,
        Usuario.Perfil.ADMINISTRADOR,
    }:
        raise PermissionDenied(
            "Este perfil não pode enviar solicitação de divulgação."
        )

    if not getattr(solicitante, "is_authenticated", False):
        solicitante = None

    dados = dict(dados)
    hemocentro_destino = dados.get("hemocentro_destino")
    if hemocentro_destino and not hasattr(hemocentro_destino, "pk"):
        try:
            dados["hemocentro_destino"] = Usuario.objects.get(
                pk=hemocentro_destino,
                perfil=Usuario.Perfil.HEMOCENTRO,
            )
        except Usuario.DoesNotExist as erro:
            raise ValidationError("Hemocentro de destino inválido.") from erro

    pedido = PedidoSangue(
        solicitante=solicitante,
        status=PedidoSangue.Status.ENVIADA,
        **dados,
    )

    validar_dados_pedido(pedido)
    pedido.full_clean()

    pedido.save()

    # Semelhança é apenas um alerta para o Hemocentro; nunca bloqueia uma
    # necessidade legítima automaticamente.
    limite = timezone.now() - timedelta(days=7)
    duplicado = PedidoSangue.objects.filter(
        hemocentro_destino=pedido.hemocentro_destino,
        tipo_sanguineo=pedido.tipo_sanguineo,
        cidade__iexact=pedido.cidade,
        data_criacao__gte=limite,
    ).exclude(pk=pedido.pk).filter(
        status__in=[
            PedidoSangue.Status.ENVIADA,
            PedidoSangue.Status.EM_ANALISE,
            PedidoSangue.Status.PUBLICADA,
            PedidoSangue.Status.CORRECAO_SOLICITADA,
        ]
    ).exists()
    if duplicado:
        pedido.duplicidade_suspeita = True
        pedido.save(update_fields=["duplicidade_suspeita", "atualizado_em"])

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

    if not hemocentro_aprovado(moderador):
        raise PermissionDenied(
            "Somente Hemocentro aprovado pode analisar pedidos."
        )

    if pedido.hemocentro_destino_id != moderador.pk:
        raise PermissionDenied(
            "O Hemocentro só pode analisar solicitações destinadas a ele."
        )

    motivo = (motivo or "").strip()

    if status_validacao not in [
        ValidacaoPedido.StatusValidacao.APROVADO,
        ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA,
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

    if status_validacao == (
        ValidacaoPedido.StatusValidacao.APROVADO
    ):
        novo_status = PedidoSangue.Status.PUBLICADA

        if not motivo:
            motivo = (
                "Pedido aprovado pelo administrador."
            )

    elif status_validacao == (
        ValidacaoPedido.StatusValidacao.RECUSADO
    ):
        novo_status = PedidoSangue.Status.RECUSADA

        if not motivo:
            motivo = (
                "Pedido recusado pelo administrador."
            )

    elif status_validacao == ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA:
        novo_status = PedidoSangue.Status.CORRECAO_SOLICITADA

        if not motivo:
            motivo = "O Hemocentro solicitou correção das informações."

    else:
        novo_status = PedidoSangue.Status.EM_ANALISE

        if not motivo:
            motivo = (
                "Pedido marcado como suspeito "
                "e mantido em análise."
            )

    pedido.status = novo_status

    if novo_status == PedidoSangue.Status.PUBLICADA:
        pedido.publicado_por = moderador
        pedido.publicado_em = timezone.now()

    pedido.save(
        update_fields=[
            "status",
            "atualizado_em",
            "publicado_por",
            "publicado_em",
        ]
    )

    notificacoes_geradas = 0
    if novo_status == PedidoSangue.Status.PUBLICADA:
        from .pedidos import criar_notificacoes_para_pedido

        notificacoes_geradas = criar_notificacoes_para_pedido(pedido=pedido)

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
            "Decisão administrativa sobre pedido de sangue."
        ),
        request=request,
        metadados={
            "id_pedido": pedido.pk,
            "id_validacao": validacao.pk,
            "status_validacao": status_validacao,
            "status_pedido": novo_status,
            "motivo": motivo,
            "notificacoes_geradas": notificacoes_geradas,
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


def solicitar_correcao_pedido(
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
            ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA
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
