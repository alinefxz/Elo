"""Capacidades por papel, compartilhadas pelas páginas privadas e menus.

O papel existente continua sendo a fonte de autorização. As permissões do
Django limitam separadamente os links para a administração técnica.
"""

from .models import Usuario
from .validacao_hemocentro import hemocentro_aprovado, usuario_e_administrador


def acessos_usuario(usuario):
    ativo = bool(usuario.is_authenticated and usuario.is_active)
    papel = getattr(usuario, "perfil", None)
    administrador = ativo and usuario_e_administrador(usuario)
    institucional = ativo and hemocentro_aprovado(usuario)
    painel_django = bool(ativo and usuario.is_staff and usuario.has_module_perms("accounts"))
    return {
        "responder_triagem": ativo and papel == Usuario.Perfil.DOADOR,
        "solicitar_pedido": ativo and papel in {
            Usuario.Perfil.DOADOR, Usuario.Perfil.RECEPTOR, Usuario.Perfil.OBSERVADOR,
        },
        "gerenciar_estoque": institucional,
        "analisar_pedidos": institucional,
        "validar_hemocentros": administrador,
        "moderar_pedidos": administrador,
        "painel_django": painel_django,
        "gerenciar_usuarios": painel_django and (
            usuario.has_perm("accounts.view_usuario") or usuario.has_perm("accounts.change_usuario")
        ),
        "consultar_auditoria": painel_django and papel == Usuario.Perfil.ADMINISTRADOR and (
            usuario.has_perm("accounts.view_auditoriaacaocritica")
            or usuario.has_perm("accounts.change_auditoriaacaocritica")
        ),
    }


def contexto_permissoes(request):
    return {"acessos": acessos_usuario(request.user)}
