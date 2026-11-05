"""Avisos persistentes de eventos reais, sem dados clínicos nas mensagens."""

from django.db.models import Q
from django.urls import reverse

from .models import Notificacao, Usuario


def cadastro_institucional_recebido(hemocentro):
    administradores = Usuario.objects.filter(is_active=True).filter(
        Q(perfil=Usuario.Perfil.ADMINISTRADOR) | Q(is_superuser=True),
    )
    Notificacao.objects.bulk_create([
        Notificacao(
            usuario=admin, titulo="Cadastro institucional para análise",
            mensagem="Um novo hemocentro aguarda validação institucional.",
            url_destino=reverse("accounts:painel_aprovacao_hemocentros"),
        ) for admin in administradores
    ])


def validacao_institucional_registrada(validacao):
    Notificacao.objects.create(
        usuario=validacao.hemocentro, titulo="Validação institucional atualizada",
        mensagem=f"A análise do cadastro foi registrada: {validacao.get_status_display()}.",
        url_destino=reverse("accounts:perfil"),
    )


def solicitacao_recebida(pedido):
    Notificacao.objects.create(
        usuario=pedido.hemocentro_destino, pedido=pedido,
        titulo="Nova solicitação de divulgação",
        mensagem="Uma solicitação foi enviada à sua instituição e aguarda análise.",
        url_destino=reverse("accounts:painel_pedidos_hemocentro"),
    )


def decisao_pedido_registrada(pedido, *, status_anterior):
    if pedido.solicitante_id and status_anterior != pedido.status:
        Notificacao.objects.create(
            usuario=pedido.solicitante, pedido=pedido,
            titulo="Sua solicitação foi atualizada",
            mensagem=f"O status da sua solicitação agora é: {pedido.get_status_display()}.",
            url_destino=reverse("accounts:minhas_solicitacoes"),
        )
