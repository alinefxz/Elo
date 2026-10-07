from functools import wraps

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from .auditoria import registrar_auditoria
from .models import AuditoriaAcaoCritica, Usuario, ValidacaoHemocentro


PARECER_PADRAO = {
    Usuario.StatusValidacaoHemocentro.APROVADO: "Hemocentro aprovado pelo administrador.",
    Usuario.StatusValidacaoHemocentro.RECUSADO: "Cadastro de hemocentro recusado pelo administrador.",
    Usuario.StatusValidacaoHemocentro.CORRECAO: "Administrador solicitou correcao dos dados cadastrais.",
}


def usuario_e_administrador(usuario):
    return bool(
        getattr(usuario, "is_authenticated", False)
        and (
            usuario.is_staff
            or usuario.is_superuser
            or usuario.perfil == Usuario.Perfil.ADMINISTRADOR
        )
    )


def usuario_e_hemocentro(usuario):
    return bool(
        getattr(usuario, "is_authenticated", False)
        and usuario.perfil == Usuario.Perfil.HEMOCENTRO
    )


def hemocentro_aprovado(usuario):
    return (
        usuario_e_hemocentro(usuario)
        and usuario.status_validacao == Usuario.StatusValidacaoHemocentro.APROVADO
    )


def validar_publicacao_hemocentro(usuario):
    if not getattr(usuario, "is_authenticated", False):
        raise PermissionDenied("Faca login para publicar estoque ou campanha.")

    if not usuario_e_hemocentro(usuario):
        raise PermissionDenied(
            "Somente usuarios com perfil Hemocentro podem publicar estoque ou campanha."
        )

    if not hemocentro_aprovado(usuario):
        raise PermissionDenied(
            "Hemocentro ainda nao aprovado. "
            f"Status atual: {usuario.get_status_validacao_display()}."
        )

    return True


def exigir_hemocentro_aprovado(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        validar_publicacao_hemocentro(request.user)
        return view_func(request, *args, **kwargs)

    return wrapper


def registrar_decisao_validacao_hemocentro(
    *,
    hemocentro,
    admin,
    status,
    parecer="",
    request=None,
):
    if hemocentro.perfil != Usuario.Perfil.HEMOCENTRO:
        raise ValidationError(
            "Somente usuarios com perfil Hemocentro podem passar por validacao."
        )

    if not usuario_e_administrador(admin):
        raise PermissionDenied("Somente administradores podem validar Hemocentros.")

    parecer = (parecer or "").strip() or PARECER_PADRAO.get(status, "")

    with transaction.atomic():
        hemocentro_atualizado = Usuario.objects.select_for_update().get(
            pk=hemocentro.pk
        )

        status_anterior = hemocentro_atualizado.status_validacao
        hemocentro_atualizado.status_validacao = status
        hemocentro_atualizado.save(
            update_fields=["status_validacao", "atualizado_em"]
        )

        validacao = ValidacaoHemocentro.objects.create(
            hemocentro=hemocentro_atualizado,
            admin=admin,
            status=status,
            parecer=parecer,
        )

        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.APROVACAO_HEMOCENTRO,
            resultado=AuditoriaAcaoCritica.Resultado.SUCESSO,
            usuario=admin,
            alvo=hemocentro_atualizado,
            descricao="Validacao institucional de hemocentro.",
            request=request,
            metadados={
                "id_validacao": validacao.pk,
                "status_anterior": status_anterior,
                "status_novo": status,
                "parecer": parecer,
            },
        )

    return validacao


def aprovar_hemocentro(*, hemocentro, admin, parecer="", request=None):
    return registrar_decisao_validacao_hemocentro(
        hemocentro=hemocentro,
        admin=admin,
        status=Usuario.StatusValidacaoHemocentro.APROVADO,
        parecer=parecer,
        request=request,
    )


def recusar_hemocentro(*, hemocentro, admin, parecer="", request=None):
    return registrar_decisao_validacao_hemocentro(
        hemocentro=hemocentro,
        admin=admin,
        status=Usuario.StatusValidacaoHemocentro.RECUSADO,
        parecer=parecer,
        request=request,
    )


def solicitar_correcao_hemocentro(*, hemocentro, admin, parecer="", request=None):
    return registrar_decisao_validacao_hemocentro(
        hemocentro=hemocentro,
        admin=admin,
        status=Usuario.StatusValidacaoHemocentro.CORRECAO,
        parecer=parecer,
        request=request,
    )