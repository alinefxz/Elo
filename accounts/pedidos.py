"""Operações de publicação de pedidos de sangue."""

from django.core.exceptions import PermissionDenied
from django.db import transaction

from .models import PedidoSangue, Usuario
from .models import AuditoriaAcaoCritica
from .auditoria import registrar_auditoria
from .validacao_hemocentro import hemocentro_aprovado


PERFIS_QUE_PUBLICAM_PEDIDOS = {
    Usuario.Perfil.HEMOCENTRO,
}


def pode_publicar_pedido(usuario):
    """Somente Hemocentro aprovado pode publicar oficialmente."""

    return (
        hemocentro_aprovado(usuario)
    )


@transaction.atomic
def publicar_pedido(usuario, form, request=None):
    """Publica um pedido do proprio Hemocentro aprovado."""

    if not pode_publicar_pedido(usuario):
        raise PermissionDenied(
            "Este perfil não pode publicar pedidos de sangue."
        )

    pedido = form.save(commit=False)
    if pedido.hemocentro_destino_id != usuario.pk:
        raise PermissionDenied("O pedido pertence a outro Hemocentro.")
    pedido.solicitante = usuario
    pedido.status = PedidoSangue.Status.ATIVO
    pedido.full_clean()
    pedido.save()
    registrar_auditoria(
        acao=AuditoriaAcaoCritica.Acao.MODERACAO,
        usuario=usuario, alvo=pedido, request=request,
        descricao="Publicacao institucional de pedido de sangue.",
        metadados={"evento": "PUBLICACAO_PEDIDO", "status_pedido": pedido.status},
    )
    return pedido
