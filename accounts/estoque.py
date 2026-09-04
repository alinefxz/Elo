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