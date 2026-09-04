"""Serviço transacional que controla o questionário e sua persistência."""

from datetime import date

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone

from .models import ConsentimentoLGPD, RespostaTriagem, Triagem, Usuario
from .triagem_catalogo import (
    PERGUNTAS_EXTENSAS,
    PERGUNTAS_SIMPLIFICADAS,
    TRIAGEM_RULE_VERSION,
    obter_pergunta,
)
from .triagem_motor import avaliar_triagem


class TriagemSimplificadaIndisponivel(Exception):
    """Indica que a pessoa ainda não concluiu uma triagem extensa."""


class TriagemConcluida(Exception):
    """Impede alteração de um resultado já registrado no histórico."""


class TriagemIncompleta(Exception):
    """Indica que existem perguntas obrigatórias ainda sem resposta."""


class PerguntaInvalida(Exception):
    """Impede códigos de pergunta ou alternativa fora do catálogo."""


PERFIS_COM_TRIAGEM = {
    Usuario.Perfil.DOADOR,
    Usuario.Perfil.RECEPTOR,
}


# A ordem explícita evita que a posição dependa da organização física do arquivo.
ORDEM_EXTENSA = [
    "EXT-01", "EXT-02", "EXT-03", "EXT-04", "EXT-05", "EXT-05A",
    "EXT-05B", "EXT-06", "EXT-07", "EXT-07A", "EXT-08", "EXT-09",
    "EXT-10", "EXT-11", "EXT-11A", "EXT-12", "EXT-13", "EXT-14",
    "EXT-15", "EXT-16", "EXT-17", "EXT-18", "EXT-19", "EXT-20",
    "EXT-21", "EXT-22", "EXT-23", "EXT-24", "EXT-25", "EXT-26",
    "EXT-27", "EXT-28", "EXT-29", "EXT-30", "EXT-31", "EXT-32",
    "EXT-33", "EXT-34", "EXT-35", "EXT-36", "EXT-37", "EXT-38",
    "EXT-39", "EXT-40", "EXT-41", "EXT-42", "EXT-43", "EXT-44",
    "EXT-45", "EXT-46", "EXT-47", "EXT-48", "EXT-49", "EXT-50",
    "EXT-51",
]

ORDEM_SIMPLIFICADA = [
    f"SIM-{numero:02d}"
    for numero in range(1, 19)
]


def pode_responder(usuario):
    """Diz se o perfil pode realizar uma triagem para doação."""

    return usuario.perfil in PERFIS_COM_TRIAGEM


def obter_extensa_base(usuario):
    """Retorna a extensa concluída mais recente do próprio usuário."""

    return (
        usuario.triagens.filter(
            modalidade=Triagem.Modalidade.EXTENSA,
            status=Triagem.Status.CONCLUIDA,
        )
        .order_by("-finalizada_em", "-iniciada_em")
        .first()
    )


def _respostas_da_triagem(triagem):
    """Transforma registros do banco no mapa esperado pelo catálogo e motor."""

    return {
        resposta.id_pergunta: resposta.valor
        for resposta in triagem.respostas.all()
    }


def _condicao_atendida(pergunta, respostas):
    """Verifica as condições simples que mostram uma subpergunta."""

    condicao = pergunta.get("mostrar_se")
    if not condicao:
        return True

    for id_anterior, codigos_aceitos in condicao.items():
        valor = respostas.get(id_anterior) or {}
        codigos = set(valor.get("codigos") or [])
        if not codigos.intersection(codigos_aceitos):
            return False

    return True


def calcular_fluxo(triagem):
    """Recalcula ramificações sem duplicar perguntas já adicionadas."""

    respostas = _respostas_da_triagem(triagem)

    if triagem.modalidade == Triagem.Modalidade.EXTENSA:
        return [
            id_pergunta
            for id_pergunta in ORDEM_EXTENSA
            if _condicao_atendida(
                PERGUNTAS_EXTENSAS[id_pergunta],
                respostas,
            )
        ]

    ids_abertos = set()
    for id_pergunta, valor in respostas.items():
        pergunta = PERGUNTAS_SIMPLIFICADAS.get(id_pergunta)
        if not pergunta:
            continue
        for codigo in valor.get("codigos") or []:
            ids_abertos.update(
                pergunta["abrir_extensa"].get(codigo, [])
            )

    # Os blocos detalhados aparecem antes das confirmações rápidas finais.
    detalhadas = [
        id_pergunta
        for id_pergunta in ORDEM_EXTENSA
        if id_pergunta in ids_abertos
    ]
    indice_confirmacao = ORDEM_SIMPLIFICADA.index("SIM-17")
    return [
        *ORDEM_SIMPLIFICADA[:indice_confirmacao],
        *detalhadas,
        *ORDEM_SIMPLIFICADA[indice_confirmacao:],
    ]


@transaction.atomic
def iniciar_triagem(usuario, modalidade, ip=None):
    """Cria uma triagem ou retoma a execução em andamento da modalidade."""

    if not pode_responder(usuario):
        raise PermissionDenied(
            "A triagem está disponível para Doadores e Receptores."
        )

    if modalidade not in {
        Triagem.Modalidade.EXTENSA,
        Triagem.Modalidade.SIMPLIFICADA,
    }:
        raise ValueError("Modalidade de triagem inválida.")

    existente = (
        usuario.triagens.filter(
            modalidade=modalidade,
            status=Triagem.Status.EM_ANDAMENTO,
        )
        .order_by("-iniciada_em")
        .first()
    )
    if existente:
        return existente

    extensa_base = None
    if modalidade == Triagem.Modalidade.SIMPLIFICADA:
        extensa_base = obter_extensa_base(usuario)
        if extensa_base is None:
            raise TriagemSimplificadaIndisponivel(
                "Conclua primeiro uma triagem extensa."
            )

    consentimento, _ = ConsentimentoLGPD.objects.get_or_create(
        usuario=usuario,
        tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM,
        versao_termo=TRIAGEM_RULE_VERSION,
        defaults={"aceito": True, "ip": ip},
    )
    if not consentimento.aceito:
        consentimento.aceito = True
        consentimento.revogado_em = None
        consentimento.ip = ip
        consentimento.save(
            update_fields=["aceito", "revogado_em", "ip"]
        )

    triagem = Triagem.objects.create(
        usuario=usuario,
        modalidade=modalidade,
        status=Triagem.Status.EM_ANDAMENTO,
        regra_version=TRIAGEM_RULE_VERSION,
        triagem_base=extensa_base,
    )
    triagem.fluxo_perguntas = calcular_fluxo(triagem)
    triagem.save(update_fields=["fluxo_perguntas", "atualizada_em"])
    return triagem


def obter_pergunta_atual(triagem):
    """Retorna a pergunta apontada pelo andamento ou nada após o fim."""

    if triagem.status != Triagem.Status.EM_ANDAMENTO:
        return None
    if triagem.pergunta_atual >= len(triagem.fluxo_perguntas):
        return None

    return obter_pergunta(
        triagem.fluxo_perguntas[triagem.pergunta_atual]
    )


def _validar_valor(pergunta, valor):
    """Rejeita dados forjados mesmo quando não vieram do formulário Django."""

    codigos = valor.get("codigos") or []
    permitidos = {
        opcao["codigo"]
        for opcao in pergunta["opcoes"]
    }
    if not codigos or not set(codigos).issubset(permitidos):
        raise PerguntaInvalida(
            "A resposta não pertence às alternativas da pergunta."
        )
    if not pergunta["multipla"] and len(codigos) != 1:
        raise PerguntaInvalida(
            "Esta pergunta aceita somente uma alternativa."
        )


def _rotulo_resposta(pergunta, codigos):
    """Mantém no campo legado os rótulos visíveis ao usuário."""

    rotulos = {
        opcao["codigo"]: opcao["rotulo"]
        for opcao in pergunta["opcoes"]
    }
    return "; ".join(rotulos[codigo] for codigo in codigos)


def _primeira_data(valor):
    """Preenche o campo legado com a primeira data estruturada disponível."""

    datas = valor.get("datas") or {}
    if not datas:
        return None

    try:
        return date.fromisoformat(next(iter(datas.values())))
    except (TypeError, ValueError):
        raise PerguntaInvalida("A data da resposta é inválida.") from None


@transaction.atomic
def salvar_resposta(triagem, id_pergunta, valor):
    """Salva ou corrige uma resposta e avança o fluxo com segurança."""

    triagem_recebida = triagem
    registro = Triagem.objects.select_for_update().get(pk=triagem.pk)
    if registro.status != Triagem.Status.EM_ANDAMENTO:
        raise TriagemConcluida(
            "Uma triagem concluída não pode ser alterada."
        )
    if id_pergunta not in registro.fluxo_perguntas:
        raise PerguntaInvalida("A pergunta não pertence a esta triagem.")

    pergunta = obter_pergunta(id_pergunta)
    _validar_valor(pergunta, valor)
    codigos = valor["codigos"]

    RespostaTriagem.objects.update_or_create(
        triagem=registro,
        id_pergunta=id_pergunta,
        defaults={
            "codigo_resposta": codigos[0],
            "resposta_label": _rotulo_resposta(pergunta, codigos),
            "data_evento": _primeira_data(valor),
            "metadata": {
                chave: conteudo
                for chave, conteudo in valor.items()
                if chave not in {"codigos", "datas"}
            },
            "valor": valor,
            "rule_version": pergunta["regra_version"],
            "source_ref": pergunta["fonte"],
        },
    )

    fluxo = calcular_fluxo(registro)
    registro.fluxo_perguntas = fluxo
    registro.pergunta_atual = min(
        fluxo.index(id_pergunta) + 1,
        len(fluxo),
    )
    registro.save(
        update_fields=[
            "fluxo_perguntas",
            "pergunta_atual",
            "atualizada_em",
        ]
    )

    # Mantém o objeto do chamador sincronizado para uso imediato na mesma view.
    triagem_recebida.fluxo_perguntas = registro.fluxo_perguntas
    triagem_recebida.pergunta_atual = registro.pergunta_atual
    triagem_recebida.atualizada_em = registro.atualizada_em
    return triagem_recebida


@transaction.atomic
def voltar_pergunta(triagem):
    """Move uma posição para trás sem apagar a resposta existente."""

    triagem_recebida = triagem
    registro = Triagem.objects.select_for_update().get(pk=triagem.pk)
    if registro.status != Triagem.Status.EM_ANDAMENTO:
        raise TriagemConcluida(
            "Uma triagem concluída não pode ser alterada."
        )

    registro.pergunta_atual = max(0, registro.pergunta_atual - 1)
    registro.save(update_fields=["pergunta_atual", "atualizada_em"])
    triagem_recebida.pergunta_atual = registro.pergunta_atual
    triagem_recebida.atualizada_em = registro.atualizada_em
    return triagem_recebida


@transaction.atomic
def concluir_triagem(triagem, hoje=None):
    """Calcula e congela o resultado depois da confirmação final."""

    triagem = Triagem.objects.select_for_update().get(pk=triagem.pk)
    if triagem.status != Triagem.Status.EM_ANDAMENTO:
        raise TriagemConcluida(
            "Uma triagem concluída não pode ser alterada."
        )

    respostas = _respostas_da_triagem(triagem)
    faltantes = set(triagem.fluxo_perguntas) - set(respostas)
    if faltantes:
        raise TriagemIncompleta(
            "Ainda existem perguntas sem resposta."
        )

    if triagem.modalidade == Triagem.Modalidade.EXTENSA:
        confirmacao = (
            respostas.get("EXT-51", {}).get("codigos") or []
        )
        if "CONFIRMAR" not in confirmacao:
            raise TriagemIncompleta("Revise e confirme a triagem extensa.")
        respostas_base = None
    else:
        confirmacao = (
            respostas.get("SIM-18", {}).get("codigos") or []
        )
        if "ENTENDO" not in confirmacao:
            raise TriagemIncompleta("Confirme a limitação da versão rápida.")
        respostas_base = _respostas_da_triagem(triagem.triagem_base)

    calculo = avaliar_triagem(
        triagem.modalidade,
        respostas,
        hoje=hoje,
        respostas_base=respostas_base,
    )
    triagem.resultado = calculo["resultado"]
    triagem.mensagem_resultado = calculo["mensagem"]
    triagem.data_liberacao = calculo["data_liberacao"]
    triagem.achados = calculo["achados"]
    triagem.status = Triagem.Status.CONCLUIDA
    triagem.finalizada_em = timezone.now()
    triagem.pergunta_atual = len(triagem.fluxo_perguntas)
    triagem.save(
        update_fields=[
            "resultado",
            "mensagem_resultado",
            "data_liberacao",
            "achados",
            "status",
            "finalizada_em",
            "pergunta_atual",
            "atualizada_em",
        ]
    )
    return triagem
