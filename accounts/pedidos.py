"""Operações de publicação de pedidos de sangue."""

from datetime import date

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import OuterRef, Subquery
from django.urls import reverse

from .compatibilidade import doadores_compativeis_para
from .models import AuditoriaAcaoCritica, Notificacao, PedidoSangue, Triagem, Usuario
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
    pedido.status = PedidoSangue.Status.PUBLICADA
    pedido.cidade = pedido.hemocentro_destino.cidade
    pedido.full_clean()
    pedido.save()
    registrar_auditoria(
        acao=AuditoriaAcaoCritica.Acao.MODERACAO, usuario=usuario, alvo=pedido, request=request,
        descricao="Publicacao institucional de pedido de sangue.",
        metadados={"evento": "PUBLICACAO_PEDIDO", "status_pedido": pedido.status},
    )
    return pedido


def criar_notificacoes_para_pedido(*, pedido):
    """Notifica apenas doadores compatíveis e aptos para o pedido publicado."""

    tipos_compativeis = doadores_compativeis_para(pedido.tipo_sanguineo)
    ultima_triagem = Triagem.objects.filter(
        usuario=OuterRef("pk"),
        status=Triagem.Status.CONCLUIDA,
    ).order_by("-finalizada_em", "-iniciada_em")

    doadores = (
        Usuario.objects
        .filter(
            perfil=Usuario.Perfil.DOADOR,
            is_active=True,
            suspensa=False,
            aceita_notificacoes_pedidos=True,
            tipo_sanguineo__in=tipos_compativeis,
        )
        .annotate(
            ultima_triagem_resultado=Subquery(
                ultima_triagem.values("resultado")[:1]
            ),
            ultima_data_liberacao=Subquery(
                ultima_triagem.values("data_liberacao")[:1]
            ),
        )
        .filter(ultima_triagem_resultado=Triagem.Resultado.APTO)
    )

    notificacoes = []
    for doador in doadores:
        if doador.ultima_data_liberacao and doador.ultima_data_liberacao > date.today():
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
