# """
# RESUMO DO ARQUIVO
# =================
# Configura como Usuario, ConsentimentoLGPD e auditorias aparecem no /admin/.

# O admin e uma ferramenta interna para pessoas autorizadas. Ele nao substitui
# as telas normais do sistema. Os formularios abaixo garantem que uma senha
# criada no painel tambem seja transformada em hash.
# """

# from django.contrib import admin, messages
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# from .auditoria import campos_sensiveis_alterados, registrar_auditoria
# from .models import (
#     AuditoriaAcaoCritica,
#     ConsentimentoLGPD,
#     Estoque,
#     EstoqueMovimentacao,
#     Usuario,
#     ValidacaoHemocentro,
# )
# from .validacao_hemocentro import (
#     aprovar_hemocentro,
#     recusar_hemocentro,
#     solicitar_correcao_hemocentro,
# )

# class UsuarioAdminCreationForm(UserCreationForm):
#     """Formulario usado quando o admin cria uma conta."""

#     class Meta:
#         model = Usuario
#         # Estes sao os dados minimos pedidos na tela de criacao do admin.
#         # Os outros dados podem ser completados depois na tela de edicao.
#         fields = ("email", "nome", "perfil")


# class UsuarioAdminChangeForm(UserChangeForm):
#     """Formulario usado quando o admin edita uma conta existente."""

#     class Meta:
#         model = Usuario
#         fields = "__all__"


# @admin.register(Usuario)
# class UsuarioAdmin(UserAdmin):
#     """Define listagem, busca e organizacao dos campos de Usuario."""

#     # UserAdmin foi criado pensando no usuario padrao. Estas atribuicoes dizem
#     # a ele para usar os formularios e o model personalizados do Elo.
#     add_form = UsuarioAdminCreationForm
#     form = UsuarioAdminChangeForm
#     model = Usuario

#     # Colunas exibidas na lista principal de usuarios.
#     list_display = (
#         "email",
#         "nome",
#         "perfil",
#         "status_validacao",
#         "is_active",
#         "email_verificado",
#         "is_staff",
#     )

#     # Filtros laterais e campos pesquisaveis no painel.
#     list_filter = (
#         "perfil",
#         "status_validacao",
#         "is_active",
#         "email_verificado",
#         "is_staff",
#     )
#     search_fields = ("email", "nome", "cpf", "cnpj")
#     ordering = ("nome",)
#     actions = (
#         "aprovar_hemocentros_selecionados",
#         "recusar_hemocentros_selecionados",
#         "solicitar_correcao_hemocentros_selecionados",
#     )

#     # Datas automaticas devem ser visualizadas, nao digitadas manualmente.
#     readonly_fields = (
#         "status_validacao",
#         "last_login",
#         "date_joined",
#         "atualizado_em",
#     )

#     # fieldsets organiza a tela de EDICAO de uma conta existente.
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         (
#             "Dados da conta",
#             {
#                 "fields": (
#                     "nome",
#                     "perfil",
#                     "cpf",
#                     "cnpj",
#                     "telefone",
#                     "data_nascimento",
#                     "sexo",
#                     "cidade",
#                     "estado",
#                     "status_validacao",
#                     "email_verificado",
#                 )
#             },
#         ),
#         (
#             "Permissoes internas do Django",
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                 )
#             },
#         ),
#         ("Datas", {"fields": ("last_login", "date_joined", "atualizado_em")}),
#     )

#     # add_fieldsets organiza a tela de CRIACAO de uma conta no admin.
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": (
#                     "email",
#                     "nome",
#                     "perfil",
#                     "password1",
#                     "password2",
#                     "is_active",
#                     "is_staff",
#                 ),
#             },
#         ),
#     )

#     def save_model(self, request, obj, form, change):
#         """Audita mudancas administrativas em perfil e permissoes."""

#         campos_auditados = [
#             "perfil",
#             "is_active",
#             "is_staff",
#             "is_superuser",
#             "email_verificado",
#         ]
#         alteracoes = campos_sensiveis_alterados(obj, campos_auditados) if change else {}

#         super().save_model(request, obj, form, change)

#         if alteracoes:
#             registrar_auditoria(
#                 acao=AuditoriaAcaoCritica.Acao.ALTERACAO_PERMISSAO,
#                 usuario=request.user,
#                 alvo=obj,
#                 descricao="Alteracao administrativa de perfil ou permissao.",
#                 request=request,
#                 metadados={"alteracoes": alteracoes},
#             )

#     def _executar_acao_validacao(self, request, queryset, funcao, parecer):
#         """Aplica uma decisao de validacao aos Hemocentros selecionados."""

#         hemocentros = queryset.filter(perfil=Usuario.Perfil.HEMOCENTRO)
#         ignorados = queryset.exclude(perfil=Usuario.Perfil.HEMOCENTRO).count()
#         total = 0

#         for hemocentro in hemocentros:
#             funcao(
#                 hemocentro=hemocentro,
#                 admin=request.user,
#                 parecer=parecer,
#                 request=request,
#             )
#             total += 1

#         if total:
#             self.message_user(
#                 request,
#                 f"{total} Hemocentro(s) atualizado(s) com sucesso.",
#                 level=messages.SUCCESS,
#             )
#         if ignorados:
#             self.message_user(
#                 request,
#                 f"{ignorados} usuario(s) ignorado(s) por nao serem Hemocentros.",
#                 level=messages.WARNING,
#             )

#     @admin.action(description="Aprovar Hemocentros selecionados")
#     def aprovar_hemocentros_selecionados(self, request, queryset):
#         """Acao em lote que aprova Hemocentros e registra historico."""

#         self._executar_acao_validacao(
#             request,
#             queryset,
#             aprovar_hemocentro,
#             "Hemocentro aprovado pelo painel administrativo.",
#         )

#     @admin.action(description="Recusar Hemocentros selecionados")
#     def recusar_hemocentros_selecionados(self, request, queryset):
#         """Acao em lote que recusa Hemocentros e registra historico."""

#         self._executar_acao_validacao(
#             request,
#             queryset,
#             recusar_hemocentro,
#             "Hemocentro recusado pelo painel administrativo.",
#         )

#     @admin.action(description="Solicitar correcao dos Hemocentros selecionados")
#     def solicitar_correcao_hemocentros_selecionados(self, request, queryset):
#         """Acao em lote que solicita correcao cadastral e registra historico."""

#         self._executar_acao_validacao(
#             request,
#             queryset,
#             solicitar_correcao_hemocentro,
#             "Correcao cadastral solicitada pelo painel administrativo.",
#         )

#     def save_related(self, request, form, formsets, change):
#         """Audita mudancas em grupos e permissoes diretas do usuario."""

#         obj = form.instance
#         grupos_antes = set()
#         permissoes_antes = set()

#         if change and obj.pk:
#             usuario_atual = Usuario.objects.get(pk=obj.pk)
#             grupos_antes = set(
#                 usuario_atual.groups.values_list("name", flat=True)
#             )
#             permissoes_antes = set(
#                 usuario_atual.user_permissions.values_list("codename", flat=True)
#             )

#         super().save_related(request, form, formsets, change)

#         if not change:
#             return

#         grupos_depois = set(obj.groups.values_list("name", flat=True))
#         permissoes_depois = set(
#             obj.user_permissions.values_list("codename", flat=True)
#         )

#         alteracoes = {}
#         if grupos_antes != grupos_depois:
#             alteracoes["groups"] = {
#                 "antes": sorted(grupos_antes),
#                 "depois": sorted(grupos_depois),
#             }
#         if permissoes_antes != permissoes_depois:
#             alteracoes["user_permissions"] = {
#                 "antes": sorted(permissoes_antes),
#                 "depois": sorted(permissoes_depois),
#             }

#         if alteracoes:
#             registrar_auditoria(
#                 acao=AuditoriaAcaoCritica.Acao.ALTERACAO_PERMISSAO,
#                 usuario=request.user,
#                 alvo=obj,
#                 descricao="Alteracao administrativa de grupos ou permissoes.",
#                 request=request,
#                 metadados={"alteracoes": alteracoes},
#             )


# @admin.register(ValidacaoHemocentro)
# class ValidacaoHemocentroAdmin(admin.ModelAdmin):
#     """Consulta somente leitura do historico institucional de Hemocentros."""

#     list_display = (
#         "data_analise",
#         "hemocentro",
#         "status",
#         "admin",
#         "parecer_resumido",
#     )
#     list_filter = ("status", "data_analise")
#     search_fields = (
#         "hemocentro__email",
#         "hemocentro__nome",
#         "hemocentro__cnpj",
#         "admin__email",
#         "admin__nome",
#         "parecer",
#     )
#     readonly_fields = (
#         "id_validacao",
#         "hemocentro",
#         "admin",
#         "status",
#         "parecer",
#         "data_analise",
#     )
#     date_hierarchy = "data_analise"
#     ordering = ("-data_analise",)

#     def parecer_resumido(self, obj):
#         """Mostra um trecho curto do parecer na listagem."""

#         if len(obj.parecer) <= 80:
#             return obj.parecer
#         return f"{obj.parecer[:77]}..."

#     parecer_resumido.short_description = "Parecer"

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False


# @admin.register(ConsentimentoLGPD)
# class ConsentimentoLGPDAdmin(admin.ModelAdmin):
#     """Permite consultar os aceites LGPD no painel administrativo."""

#     list_display = (
#         "usuario",
#         "tipo_termo",
#         "versao_termo",
#         "aceito",
#         "data_aceite",
#     )
#     list_filter = ("tipo_termo", "aceito", "versao_termo")
#     search_fields = ("usuario__email", "usuario__nome")

#     # A data representa um evento real e nao deve ser alterada pelo formulario.
#     readonly_fields = ("data_aceite",)


# @admin.register(AuditoriaAcaoCritica)
# class AuditoriaAcaoCriticaAdmin(admin.ModelAdmin):
#     """Consulta somente leitura das acoes criticas registradas."""

#     list_display = (
#         "criado_em",
#         "acao",
#         "resultado",
#         "usuario",
#         "alvo_tipo",
#         "alvo_id",
#         "ip",
#     )
#     list_filter = ("acao", "resultado", "criado_em")
#     search_fields = (
#         "usuario__email",
#         "usuario__nome",
#         "descricao",
#         "alvo_tipo",
#         "alvo_id",
#         "ip",
#     )
#     readonly_fields = (
#         "id_auditoria",
#         "usuario",
#         "acao",
#         "resultado",
#         "alvo_tipo",
#         "alvo_id",
#         "descricao",
#         "ip",
#         "user_agent",
#         "metadados",
#         "criado_em",
#     )
#     date_hierarchy = "criado_em"
#     ordering = ("-criado_em",)

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

# @admin.register(Estoque)
# class EstoqueAdmin(admin.ModelAdmin):
#     """
#     Consulta administrativa do estoque de cada Hemocentro.

#     status_calculado e data_atualizacao ficam somente leitura porque sao
#     derivados automaticamente pela camada de servico (accounts/estoque.py)
#     sempre que a quantidade de bolsas muda.
#     """

#     list_display = (
#         "hemocentro",
#         "tipo_sanguineo",
#         "quantidade_bolsas",
#         "nivel_minimo",
#         "nivel_critico",
#         "status_calculado",
#         "data_atualizacao",
#     )
#     list_filter = ("status_calculado", "tipo_sanguineo")
#     search_fields = ("hemocentro__email", "hemocentro__nome")
#     ordering = ("hemocentro__nome", "tipo_sanguineo")
#     readonly_fields = ("status_calculado", "data_atualizacao")


# @admin.register(EstoqueMovimentacao)
# class EstoqueMovimentacaoAdmin(admin.ModelAdmin):
#     """
#     Historico somente leitura das movimentacoes de estoque (UC_30).

#     Assim como ValidacaoHemocentroAdmin, este historico nunca deve ser
#     criado, editado ou apagado pelo admin: toda movimentacao precisa
#     passar por registrar_movimentacao_estoque para manter a quantidade
#     de bolsas e a auditoria consistentes.
#     """

#     list_display = (
#         "data_hora",
#         "estoque",
#         "tipo_movimento",
#         "quantidade_anterior",
#         "quantidade_movimentada",
#         "quantidade_nova",
#         "usuario_resp",
#     )
#     list_filter = ("tipo_movimento", "data_hora")
#     search_fields = (
#         "estoque__hemocentro__email",
#         "estoque__hemocentro__nome",
#         "usuario_resp__email",
#         "usuario_resp__nome",
#         "motivo",
#     )
#     readonly_fields = (
#         "id_mov",
#         "estoque",
#         "usuario_resp",
#         "tipo_movimento",
#         "quantidade_anterior",
#         "quantidade_movimentada",
#         "quantidade_nova",
#         "motivo",
#         "data_hora",
#     )
#     date_hierarchy = "data_hora"
#     ordering = ("-data_hora",)

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

"""
Regras de negocio do estoque de sangue por Hemocentro.

UC_29 - Cadastrar Estoque:
    ``cadastrar_estoque`` cria a estrutura de estoque (quantidade, niveis
    de alerta e status calculado) para um par hemocentro + tipo sanguineo.

UC_30 - Atualizar Estoque:
    ``registrar_movimentacao_estoque`` aplica uma entrada, saida ou ajuste
    de bolsas, atualiza a quantidade do Estoque e grava o historico em
    EstoqueMovimentacao com o responsavel pela alteracao.

Assim como em validacao_hemocentro.py, as views nunca devem criar ou
alterar Estoque/EstoqueMovimentacao diretamente: elas devem chamar estas
funcoes, que concentram validacao, transacao e auditoria em um so lugar.
"""

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from .auditoria import registrar_auditoria
from .compatibilidade import normalizar_tipo_sanguineo
from .models import AuditoriaAcaoCritica, Estoque, EstoqueMovimentacao, Usuario
from .validacao_hemocentro import validar_publicacao_hemocentro


def calcular_status_calculado(*, quantidade_bolsas, nivel_minimo, nivel_critico):
    """
    Deriva o status do estoque a partir da quantidade e dos niveis de alerta.

    Regra (da mais grave para a mais leve):
    - quantidade <= nivel_critico  -> CRITICO;
    - quantidade <= nivel_minimo   -> BAIXO;
    - caso contrario               -> ESTAVEL.
    """

    if quantidade_bolsas <= nivel_critico:
        return Estoque.StatusCalculado.CRITICO

    if quantidade_bolsas <= nivel_minimo:
        return Estoque.StatusCalculado.BAIXO

    return Estoque.StatusCalculado.ESTAVEL


def validar_responsavel_pelo_estoque(*, estoque, usuario):
    """
    Garante que somente o proprio Hemocentro aprovado, dono do estoque,
    possa gerenciar aquele registro (cadastrar ou movimentar bolsas).
    """

    # validar_publicacao_hemocentro ja cobre: autenticado, perfil
    # Hemocentro e status_validacao == APROVADO. Reaproveitar essa funcao
    # evita duas regras de aprovacao divergentes no projeto.
    validar_publicacao_hemocentro(usuario)

    if estoque is not None and estoque.hemocentro_id != usuario.pk:
        raise PermissionDenied(
            "Este estoque pertence a outro Hemocentro."
        )

    return True


def obter_estoque_do_hemocentro(*, hemocentro, tipo_sanguineo):
    """Busca (ou None) o Estoque de um tipo sanguineo especifico."""

    tipo = normalizar_tipo_sanguineo(tipo_sanguineo)

    return Estoque.objects.filter(
        hemocentro=hemocentro,
        tipo_sanguineo=tipo,
    ).first()


def cadastrar_estoque(
    *,
    hemocentro,
    tipo_sanguineo,
    nivel_minimo,
    nivel_critico,
    quantidade_bolsas=0,
    request=None,
):
    """
    UC_29 - Cria a estrutura de estoque de um tipo sanguineo para um
    Hemocentro aprovado.

    Levanta ValidationError se o tipo sanguineo for invalido, se os
    niveis estiverem incoerentes ou se ja existir estoque cadastrado
    para aquele par hemocentro + tipo sanguineo.
    """

    # Somente Hemocentro aprovado pode cadastrar o proprio estoque.
    validar_publicacao_hemocentro(hemocentro)

    tipo = normalizar_tipo_sanguineo(tipo_sanguineo)

    if nivel_critico > nivel_minimo:
        raise ValidationError(
            {"nivel_critico": "O nivel critico deve ser menor ou igual ao nivel minimo."}
        )

    if Estoque.objects.filter(hemocentro=hemocentro, tipo_sanguineo=tipo).exists():
        raise ValidationError(
            f"Ja existe estoque cadastrado para o tipo {tipo} neste hemocentro."
        )

    status_calculado = calcular_status_calculado(
        quantidade_bolsas=quantidade_bolsas,
        nivel_minimo=nivel_minimo,
        nivel_critico=nivel_critico,
    )

    with transaction.atomic():
        estoque = Estoque.objects.create(
            hemocentro=hemocentro,
            tipo_sanguineo=tipo,
            quantidade_bolsas=quantidade_bolsas,
            nivel_minimo=nivel_minimo,
            nivel_critico=nivel_critico,
            status_calculado=status_calculado,
        )

        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.CADASTRO_ESTOQUE,
            usuario=hemocentro,
            alvo=estoque,
            descricao="Cadastro da estrutura de estoque de um tipo sanguineo.",
            request=request,
            metadados={
                "tipo_sanguineo": tipo,
                "quantidade_bolsas": quantidade_bolsas,
                "nivel_minimo": nivel_minimo,
                "nivel_critico": nivel_critico,
                "status_calculado": status_calculado,
            },
        )

    return estoque


def registrar_movimentacao_estoque(
    *,
    estoque,
    usuario_resp,
    tipo_movimento,
    quantidade,
    motivo="",
    request=None,
):
    """
    UC_30 - Aplica uma movimentacao de bolsas sobre um Estoque existente
    e grava o historico correspondente.

    ``quantidade`` tem um significado diferente por tipo_movimento:
    - ENTRADA / SAIDA: quantidade de bolsas a somar ou subtrair (> 0);
    - AJUSTE: a nova quantidade absoluta de bolsas no estoque (>= 0),
      usada por exemplo apos uma contagem fisica.

    A funcao trava a linha do Estoque (select_for_update) durante a
    transacao para que duas movimentacoes simultaneas nunca calculem a
    quantidade nova a partir do mesmo valor antigo.
    """

    validar_responsavel_pelo_estoque(estoque=estoque, usuario=usuario_resp)

    if tipo_movimento not in EstoqueMovimentacao.TipoMovimento.values:
        raise ValidationError("Tipo de movimentacao invalido.")

    if tipo_movimento in (
        EstoqueMovimentacao.TipoMovimento.ENTRADA,
        EstoqueMovimentacao.TipoMovimento.SAIDA,
    ) and quantidade <= 0:
        raise ValidationError(
            {"quantidade": "Informe uma quantidade maior que zero."}
        )

    if tipo_movimento == EstoqueMovimentacao.TipoMovimento.AJUSTE and quantidade < 0:
        raise ValidationError(
            {"quantidade": "A quantidade ajustada nao pode ser negativa."}
        )

    with transaction.atomic():
        # select_for_update busca o Estoque de novo, ja bloqueado para
        # escrita, para evitar condicao de corrida entre duas
        # movimentacoes feitas quase ao mesmo tempo.
        estoque_atual = Estoque.objects.select_for_update().get(pk=estoque.pk)

        quantidade_anterior = estoque_atual.quantidade_bolsas

        if tipo_movimento == EstoqueMovimentacao.TipoMovimento.ENTRADA:
            quantidade_movimentada = quantidade
            quantidade_nova = quantidade_anterior + quantidade

        elif tipo_movimento == EstoqueMovimentacao.TipoMovimento.SAIDA:
            if quantidade > quantidade_anterior:
                raise ValidationError(
                    {
                        "quantidade": (
                            "Nao ha bolsas suficientes para esta saida. "
                            f"Quantidade atual: {quantidade_anterior}."
                        )
                    }
                )
            quantidade_movimentada = quantidade
            quantidade_nova = quantidade_anterior - quantidade

        else:  # AJUSTE
            quantidade_nova = quantidade
            quantidade_movimentada = quantidade_nova - quantidade_anterior

        status_calculado = calcular_status_calculado(
            quantidade_bolsas=quantidade_nova,
            nivel_minimo=estoque_atual.nivel_minimo,
            nivel_critico=estoque_atual.nivel_critico,
        )

        estoque_atual.quantidade_bolsas = quantidade_nova
        estoque_atual.status_calculado = status_calculado
        estoque_atual.save(
            update_fields=[
                "quantidade_bolsas",
                "status_calculado",
                "data_atualizacao",
            ]
        )

        movimentacao = EstoqueMovimentacao.objects.create(
            estoque=estoque_atual,
            usuario_resp=usuario_resp,
            tipo_movimento=tipo_movimento,
            quantidade_anterior=quantidade_anterior,
            quantidade_movimentada=quantidade_movimentada,
            quantidade_nova=quantidade_nova,
            motivo=(motivo or "").strip(),
        )

        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.ATUALIZACAO_ESTOQUE,
            usuario=usuario_resp,
            alvo=estoque_atual,
            descricao="Movimentacao de bolsas no estoque.",
            request=request,
            metadados={
                "id_mov": movimentacao.pk,
                "tipo_movimento": tipo_movimento,
                "quantidade_anterior": quantidade_anterior,
                "quantidade_movimentada": quantidade_movimentada,
                "quantidade_nova": quantidade_nova,
                "status_calculado": status_calculado,
                "motivo": movimentacao.motivo,
            },
        )

    return movimentacao