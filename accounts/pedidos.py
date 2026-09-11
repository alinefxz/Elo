"""Operações de publicação de pedidos de sangue."""

from django.core.exceptions import PermissionDenied
from django.db import transaction

from .models import PedidoSangue, Usuario


PERFIS_QUE_PUBLICAM_PEDIDOS = {
    Usuario.Perfil.DOADOR,
    Usuario.Perfil.RECEPTOR,
    Usuario.Perfil.OBSERVADOR,
    Usuario.Perfil.HEMOCENTRO,
    Usuario.Perfil.ADMINISTRADOR,
}


def pode_publicar_pedido(usuario):
    """Permite publicação para pessoas e instituições, mas não para admin."""

    return (
        usuario.is_authenticated
        and usuario.perfil in PERFIS_QUE_PUBLICAM_PEDIDOS
    )


@transaction.atomic
def publicar_pedido(usuario, form):
    """Cria um pedido pendente com o usuário autenticado como solicitante."""

    if not pode_publicar_pedido(usuario):
        raise PermissionDenied(
            "Este perfil não pode publicar pedidos de sangue."
        )

    pedido = form.save(commit=False)
    pedido.solicitante = usuario
    pedido.status = PedidoSangue.Status.PENDENTE
    pedido.cidade = pedido.hemocentro.cidade
    pedido.full_clean()
    pedido.save()
    return pedido
