"""Operações de publicação de pedidos de sangue."""

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.urls import reverse
from django.utils import timezone

from .compatibilidade import doadores_aptos_para_convocacao, limite_convocacao_atingido
from .models import AuditoriaAcaoCritica, Notificacao, PedidoSangue, Usuario
from .auditoria import registrar_auditoria


def pode_publicar_pedido(usuario):
    """Somente o Hemocentro aprovado pode publicar oficialmente."""

    return (
        usuario.is_authenticated
        and usuario.perfil == Usuario.Perfil.HEMOCENTRO
        and usuario.status_validacao
        == Usuario.StatusValidacaoHemocentro.APROVADO
    )


@transaction.atomic
def publicar_pedido(usuario, form, request=None):
    """Publica um pedido já analisado pelo próprio Hemocentro."""

    if not pode_publicar_pedido(usuario):
        raise PermissionDenied(
            "Este perfil não pode publicar pedidos de sangue."
        )

    pedido = form.save(commit=False)
    if pedido.hemocentro_destino_id != usuario.pk:
        raise PermissionDenied("O pedido pertence a outro Hemocentro.")
    pedido.publicado_por = usuario
    pedido.publicado_em = timezone.now()
    pedido.status = PedidoSangue.Status.PUBLICADA
    pedido.cidade = pedido.hemocentro_destino.cidade
    pedido.full_clean()
    pedido.save()
    criar_notificacoes_para_pedido(pedido=pedido)
    registrar_auditoria(
        acao=AuditoriaAcaoCritica.Acao.MODERACAO, usuario=usuario, alvo=pedido, request=request,
        descricao="Publicacao institucional de pedido de sangue.",
        metadados={"evento": "PUBLICACAO_PEDIDO", "status_pedido": pedido.status},
    )
    return pedido


@transaction.atomic
def criar_notificacoes_para_pedido(*, pedido):
    """Notifica apenas doadores compatíveis e aptos para o pedido publicado."""

    if pedido.status != PedidoSangue.Status.PUBLICADA or not pode_publicar_pedido(pedido.hemocentro_destino):
        return 0
    doadores = doadores_aptos_para_convocacao(pedido.tipo_sanguineo).select_for_update()

    notificacoes = []
    for doador in doadores:
        if limite_convocacao_atingido(doador):
            continue
        if Notificacao.objects.filter(usuario=doador, pedido=pedido).exists():
            continue
        notificacoes.append(
            Notificacao(
                usuario=doador,
                pedido=pedido,
                tipo=Notificacao.Tipo.PEDIDO_COMPATIVEL,
                titulo=f"Pedido compatível: {pedido.tipo_sanguineo}",
                mensagem=(
                    f"Há uma necessidade publicada pelo Hemocentro "
                    f"{pedido.hemocentro_destino.nome} em {pedido.cidade}."
                ),
                url_destino=reverse("accounts:consultar_pedidos"),
            )
        )

    Notificacao.objects.bulk_create(notificacoes)
    return len(notificacoes)
