"""
Sinais do Django usados para auditoria automatica.

Nesta etapa registramos falhas de login e marcamos como suspeito quando ha
muitas tentativas recentes para o mesmo e-mail ou IP.
"""

from datetime import timedelta

from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver
from django.utils import timezone

from .auditoria import obter_ip, obter_user_agent, registrar_auditoria
from .models import AuditoriaAcaoCritica


LIMITE_LOGIN_SUSPEITO = 5
JANELA_LOGIN_SUSPEITO_MINUTOS = 10


@receiver(user_login_failed)
def auditar_login_falho(sender, credentials, request, **kwargs):
    """Registra falha e login suspeito sem guardar a senha enviada."""

    email = (credentials or {}).get("username") or (credentials or {}).get("email")
    email = (email or "").strip().lower()
    ip = obter_ip(request)
    user_agent = obter_user_agent(request)

    registrar_auditoria(
        acao=AuditoriaAcaoCritica.Acao.LOGIN_FALHO,
        resultado=AuditoriaAcaoCritica.Resultado.FALHA,
        descricao="Tentativa de login sem sucesso.",
        request=request,
        ip=ip,
        user_agent=user_agent,
        metadados={"email": email},
    )

    inicio_janela = timezone.now() - timedelta(minutes=JANELA_LOGIN_SUSPEITO_MINUTOS)
    falhas_recentes = AuditoriaAcaoCritica.objects.filter(
        acao=AuditoriaAcaoCritica.Acao.LOGIN_FALHO,
        criado_em__gte=inicio_janela,
    )

    if email:
        falhas_recentes = falhas_recentes.filter(metadados__email=email)
    elif ip:
        falhas_recentes = falhas_recentes.filter(ip=ip)

    if falhas_recentes.count() >= LIMITE_LOGIN_SUSPEITO:
        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.LOGIN_SUSPEITO,
            resultado=AuditoriaAcaoCritica.Resultado.BLOQUEADO,
            descricao="Muitas tentativas de login falhas em curto periodo.",
            request=request,
            ip=ip,
            user_agent=user_agent,
            metadados={
                "email": email,
                "falhas_recentes": falhas_recentes.count(),
                "janela_minutos": JANELA_LOGIN_SUSPEITO_MINUTOS,
            },
        )
