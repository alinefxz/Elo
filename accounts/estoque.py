"""
Regras de negocio do estoque de sangue por Hemocentro.

UC_29 - Cadastrar Estoque:
    ``cadastrar_estoque`` cria a estrutura de estoque (quantidade, niveis
    de alerta e status calculado) para um par hemocentro + tipo sanguineo.

UC_30 - Atualizar Estoque:
    ``registrar_movimentacao_estoque`` aplica uma entrada, saida ou ajuste
    de bolsas, atualiza a quantidade do Estoque e grava o historico em
    EstoqueMovimentacao com o responsavel pela alteracao.
"""

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.urls import reverse

from .auditoria import registrar_auditoria
from .compatibilidade import doadores_compativeis_para, normalizar_tipo_sanguineo
from .models import (
    AuditoriaAcaoCritica,
    Estoque,
    EstoqueMovimentacao,
    Notificacao,
    Usuario,
)
from .validacao_hemocentro import validar_publicacao_hemocentro


STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA = {
    Estoque.StatusCalculado.BAIXO: Notificacao.Tipo.ESTOQUE_BAIXO,
    Estoque.StatusCalculado.CRITICO: Notificacao.Tipo.ESTOQUE_CRITICO,
}


def criar_notificacoes_para_doadores_compativeis(*, estoque, status_calculado):
    """
    Cria notificacoes internas para doadores compativeis.

    Quando o estoque atualizado fica BAIXO ou CRITICO, o sistema procura
    doadores ativos cujo tipo sanguineo seja compativel com aquele estoque.
    """

    if status_calculado not in STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA:
        return 0

    tipos_compativeis = doadores_compativeis_para(estoque.tipo_sanguineo)
    tipo_notificacao = STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA[status_calculado]

    doadores = Usuario.objects.filter(
        perfil=Usuario.Perfil.DOADOR,
        tipo_sanguineo__in=tipos_compativeis,
        is_active=True,
    )

    usuarios_com_alerta_aberto = set(
        Notificacao.objects.filter(
            usuario__in=doadores,
            estoque=estoque,
            tipo=tipo_notificacao,
            lida=False,
        ).values_list("usuario_id", flat=True)
    )

    nivel = "critico"
    if status_calculado == Estoque.StatusCalculado.BAIXO:
        nivel = "baixo"

    notificacoes = []

    for doador in doadores:
        if doador.pk in usuarios_com_alerta_aberto:
            continue

        notificacoes.append(
            Notificacao(
                usuario=doador,
                estoque=estoque,
                tipo=tipo_notificacao,
                titulo=f"Estoque {nivel} para {estoque.tipo_sanguineo}",
                mensagem=(
                    f"O estoque {estoque.tipo_sanguineo} do Hemocentro "
                    f"{estoque.hemocentro.nome} esta em nivel {nivel}. "
                    f"Seu tipo sanguineo ({doador.tipo_sanguineo}) "
                    "e compativel para doacao."
                ),
                url_destino=reverse("accounts:estoque_publico"),
            )
        )

    Notificacao.objects.bulk_create(notificacoes)

    return len(notificacoes)


def calcular_status_calculado(*, quantidade_bolsas, nivel_minimo, nivel_critico):
    """
    Deriva o status do estoque a partir da quantidade e dos niveis de alerta.

    Regra:
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
    possa gerenciar aquele registro.
    """

    validar_publicacao_hemocentro(usuario)

    if estoque is not None and estoque.hemocentro_id != usuario.pk:
        raise PermissionDenied(
            "Este estoque pertence a outro Hemocentro."
        )

    return True


def obter_estoque_do_hemocentro(*, hemocentro, tipo_sanguineo):
    """Busca um Estoque de um tipo sanguineo especifico."""

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
    """

    validar_publicacao_hemocentro(hemocentro)

    tipo = normalizar_tipo_sanguineo(tipo_sanguineo)

    if nivel_critico > nivel_minimo:
        raise ValidationError(
            {
                "nivel_critico": (
                    "O nivel critico deve ser menor ou igual ao nivel minimo."
                )
            }
        )

    if Estoque.objects.filter(
        hemocentro=hemocentro,
        tipo_sanguineo=tipo,
    ).exists():
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

        else:
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

        notificacoes_geradas = criar_notificacoes_para_doadores_compativeis(
            estoque=estoque_atual,
            status_calculado=status_calculado,
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
                "notificacoes_geradas": notificacoes_geradas,
                "motivo": movimentacao.motivo,
            },
        )

    return movimentacao


def calcular_status_publico(quantidade_bolsas, nivel_minimo, nivel_critico):
    """
    Calcula o status que sera exibido publicamente.

    Os niveis minimo e critico sao utilizados apenas internamente
    para determinar a situacao do estoque.
    """

    if quantidade_bolsas <= nivel_critico:
        return "CRITICO"

    if quantidade_bolsas <= nivel_minimo:
        return "BAIXO"

    if quantidade_bolsas > nivel_minimo * 2:
        return "ALTO"

    return "ADEQUADO"


def obter_estoques_publicos():
    """
    Busca os estoques dos Hemocentros aprovados e retorna somente
    os dados que podem ser exibidos publicamente.
    """

    estoques = (
        Estoque.objects
        .select_related("hemocentro")
        .filter(
            hemocentro__perfil=Usuario.Perfil.HEMOCENTRO,
            hemocentro__status_validacao=(
                Usuario.StatusValidacaoHemocentro.APROVADO
            ),
        )
        .order_by(
            "hemocentro__cidade",
            "hemocentro__nome",
            "tipo_sanguineo",
        )
    )

    resultado = []

    for estoque in estoques:
        resultado.append(
            {
                "nome": estoque.hemocentro.nome,
                "cidade": estoque.hemocentro.cidade,
                "estado": estoque.hemocentro.estado,
                "tipo_sanguineo": estoque.tipo_sanguineo,
                "quantidade_bolsas": estoque.quantidade_bolsas,
                "status": calcular_status_publico(
                    estoque.quantidade_bolsas,
                    estoque.nivel_minimo,
                    estoque.nivel_critico,
                ),
                "data_atualizacao": estoque.data_atualizacao,
            }
        )

    return resultado