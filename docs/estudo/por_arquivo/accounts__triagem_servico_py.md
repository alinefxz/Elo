# accounts/triagem_servico.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Andamento, respostas, revisao, persistencia e conclusao de triagem.

**Arquivo original:** [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
# Este arquivo controla o fluxo e o salvamento da triagem.

# - Permite triagem somente para Doadores e Receptores.
# - Inicia triagens extensas e simplificadas após o aceite do termo.
# - A simplificada utiliza uma triagem extensa concluída como base.
# - Organiza as perguntas conforme as respostas anteriores.
# - Mostra perguntas condicionais quando necessário.
# - Valida perguntas, alternativas e datas recebidas.
# - Salva, atualiza e reutiliza respostas anteriores quando solicitado.
# - Permite voltar ou editar enquanto a triagem está em andamento.
# - Remove respostas que deixam de ser válidas após uma alteração.
# - Impede alterações depois da conclusão.
# - Exige confirmação final antes de calcular o resultado.
# - Envia as respostas para o motor da triagem.
# - Salva resultado, mensagem, achados e data de liberação.
# - Usa transações para evitar dados incompletos ou alterações simultâneas.

# Os catálogos fornecem as perguntas, o motor aplica as regras e este arquivo controla o fluxo, as respostas e a persistência da triagem.

"""Serviço transacional que controla o questionário e sua persistência."""

from datetime import date

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone

from .compatibilidade import normalizar_tipo_sanguineo
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


class TriagemExtensaNecessaria(Exception):
    """Indica que a versão rápida deixou de ser segura para o usuário."""


class PerguntaInvalida(Exception):
    """Impede códigos de pergunta ou alternativa fora do catálogo."""


PERFIS_COM_TRIAGEM = {
    Usuario.Perfil.DOADOR,
}


# A ordem explícita evita que a posição dependa da organização física do arquivo.
ORDEM_EXTENSA = [
    "EXT-01", "EXT-01A", "EXT-02", "EXT-03", "EXT-04", "EXT-05", "EXT-05A",
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


def obter_extensa_reutilizavel(usuario):
    """Retorna a extensa concluída atual que pode preencher uma nova triagem."""

    return (
        usuario.triagens.filter(
            modalidade=Triagem.Modalidade.EXTENSA,
            status=Triagem.Status.CONCLUIDA,
            regra_version=TRIAGEM_RULE_VERSION,
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


def _copiar_respostas_para_nova_triagem(origem, destino):
    """Copia respostas para uma nova triagem sem alterar o histórico original."""

    RespostaTriagem.objects.bulk_create(
        [
            RespostaTriagem(
                triagem=destino,
                id_pergunta=resposta.id_pergunta,
                codigo_resposta=resposta.codigo_resposta,
                resposta_label=resposta.resposta_label,
                data_evento=resposta.data_evento,
                metadata=resposta.metadata,
                valor=resposta.valor,
                rule_version=resposta.rule_version,
                source_ref=resposta.source_ref,
            )
            for resposta in origem.respostas.order_by("id_resposta")
        ]
    )


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
        and _condicao_atendida(
            PERGUNTAS_EXTENSAS[id_pergunta],
            respostas,
        )
    ]
    indice_confirmacao = ORDEM_SIMPLIFICADA.index("SIM-17")
    return [
        *ORDEM_SIMPLIFICADA[:indice_confirmacao],
        *detalhadas,
        *ORDEM_SIMPLIFICADA[indice_confirmacao:],
    ]


@transaction.atomic
def iniciar_triagem(
    usuario,
    modalidade,
    ip=None,
    aceite_termo=True,
    reutilizar_respostas=False,
):
    """Cria/retoma a triagem após o aceite registrado pela camada de entrada.

    A view exige o checkbox explicitamente; o valor padrão preserva a API de
    serviço usada por integrações internas que já representam esse aceite.
    """

    if not pode_responder(usuario):
        raise PermissionDenied(
            "A triagem está disponível para Doadores."
        )

    if modalidade not in {
        Triagem.Modalidade.EXTENSA,
        Triagem.Modalidade.SIMPLIFICADA,
    }:
        raise ValueError("Modalidade de triagem inválida.")

    if not aceite_termo:
        raise PermissionDenied(
            "Confirme ciência do termo da pré-triagem antes de começar."
        )

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

    if modalidade == Triagem.Modalidade.EXTENSA and reutilizar_respostas:
        origem = obter_extensa_reutilizavel(usuario)
        if origem is not None:
            _copiar_respostas_para_nova_triagem(origem, triagem)

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


def _resposta_exige_extensa(id_pergunta, codigos):
    """Centraliza as respostas que invalidam o resumo da versão rápida."""

    escolhas = set(codigos)
    return (
        (
            id_pergunta == "SIM-01"
            and bool(escolhas & {"INCORRETO", "NAO_FIZ", "NAO_SEI"})
        )
        or (
            id_pergunta == "SIM-17"
            and bool(escolhas & {"SIM", "NAO_SEI"})
        )
        or (id_pergunta == "SIM-18" and "EXTENSA" in escolhas)
    )


def atualizar_tipo_sanguineo_do_usuario(triagem, valor):
    """
    Atualiza o tipo sanguineo do usuario a partir da pergunta informativa.

    Essa informacao nao interfere no resultado da triagem; ela apenas liga o
    usuario aos alertas internos de estoque e a compatibilidade sanguinea.
    """

    codigos = valor.get("codigos") or []
    if not codigos:
        return

    try:
        tipo_sanguineo = normalizar_tipo_sanguineo(codigos[0])
    except ValueError:
        return

    usuario = triagem.usuario
    if usuario.tipo_sanguineo_confirmado:
        return

    if usuario.tipo_sanguineo == tipo_sanguineo:
        return

    usuario.tipo_sanguineo = tipo_sanguineo
    usuario.save(update_fields=["tipo_sanguineo", "atualizado_em"])


def salvar_resposta(triagem, id_pergunta, valor):
    """Salva ou corrige uma resposta e avança o fluxo com segurança."""

    triagem_recebida = triagem
    exige_extensa = False

    # O bloco atômico termina antes da exceção de redirecionamento. Assim, a
    # tentativa rápida fica cancelada no histórico sem deixar dados pela metade.
    with transaction.atomic():
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

        if id_pergunta == "EXT-01A":
            atualizar_tipo_sanguineo_do_usuario(registro, valor)

        exige_extensa = (
            registro.modalidade == Triagem.Modalidade.SIMPLIFICADA
            and _resposta_exige_extensa(id_pergunta, codigos)
        )
        if exige_extensa:
            registro.status = Triagem.Status.CANCELADA
            registro.save(update_fields=["status", "atualizada_em"])
        else:
            fluxo = calcular_fluxo(registro)
            registro.fluxo_perguntas = fluxo

            # Se uma correção fechar uma ramificação, suas respostas antigas
            # deixam de ser válidas e não podem participar do cálculo final.
            registro.respostas.exclude(id_pergunta__in=fluxo).delete()

            # Estas respostas pedem revisão, portanto não avançam o cursor.
            if (
                id_pergunta == "EXT-01"
                and "NAO" in codigos
            ) or (
                id_pergunta == "EXT-51"
                and "REVISAR" in codigos
            ):
                registro.pergunta_atual = 0
            else:
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

        # Mantém o objeto recebido sincronizado para a view usar imediatamente.
        triagem_recebida.fluxo_perguntas = registro.fluxo_perguntas
        triagem_recebida.pergunta_atual = registro.pergunta_atual
        triagem_recebida.status = registro.status
        triagem_recebida.atualizada_em = registro.atualizada_em

    if exige_extensa:
        raise TriagemExtensaNecessaria(
            "O resumo mudou; continue em uma nova triagem extensa."
        )

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
def editar_pergunta(triagem, id_pergunta):
    """Reposiciona uma triagem em andamento para uma resposta já salva."""

    registro = Triagem.objects.select_for_update().get(pk=triagem.pk)
    if registro.status != Triagem.Status.EM_ANDAMENTO:
        raise TriagemConcluida("Uma triagem concluída não pode ser alterada.")
    if id_pergunta not in registro.fluxo_perguntas:
        raise PerguntaInvalida("A pergunta não pertence a esta triagem.")

    registro.pergunta_atual = registro.fluxo_perguntas.index(id_pergunta)
    registro.save(update_fields=["pergunta_atual", "atualizada_em"])
    triagem.pergunta_atual = registro.pergunta_atual
    triagem.atualizada_em = registro.atualizada_em
    return triagem


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
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 20 a 20

```python
"""Serviço transacional que controla o questionário e sua persistência."""
```

**Explicação deste trecho:**

**Linha 20 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 22 a 22

```python
from datetime import date
```

**Explicação deste trecho:**

**Linha 22 — ImportFrom** (nível 0 do bloco).

Importa de `datetime` os nomes `date`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 24 a 24

```python
from django.core.exceptions import PermissionDenied
```

**Explicação deste trecho:**

**Linha 24 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.exceptions` os nomes `PermissionDenied`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 25 a 25

```python
from django.db import transaction
```

**Explicação deste trecho:**

**Linha 25 — ImportFrom** (nível 0 do bloco).

Importa de `django.db` os nomes `transaction`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 26 a 26

```python
from django.utils import timezone
```

**Explicação deste trecho:**

**Linha 26 — ImportFrom** (nível 0 do bloco).

Importa de `django.utils` os nomes `timezone`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 28 a 28

```python
from .compatibilidade import normalizar_tipo_sanguineo
```

**Explicação deste trecho:**

**Linha 28 — ImportFrom** (nível 0 do bloco).

Importa de `.compatibilidade` os nomes `normalizar_tipo_sanguineo`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 29 a 29

```python
from .models import ConsentimentoLGPD, RespostaTriagem, Triagem, Usuario
```

**Explicação deste trecho:**

**Linha 29 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `ConsentimentoLGPD`, `RespostaTriagem`, `Triagem`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 30 a 35

```python
from .triagem_catalogo import (
    PERGUNTAS_EXTENSAS,
    PERGUNTAS_SIMPLIFICADAS,
    TRIAGEM_RULE_VERSION,
    obter_pergunta,
)
```

**Explicação deste trecho:**

**Linha 30 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_catalogo` os nomes `PERGUNTAS_EXTENSAS`, `PERGUNTAS_SIMPLIFICADAS`, `TRIAGEM_RULE_VERSION`, `obter_pergunta`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 36 a 36

```python
from .triagem_motor import avaliar_triagem
```

**Explicação deste trecho:**

**Linha 36 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_motor` os nomes `avaliar_triagem`. Pontos iniciais indicam importação relativa ao pacote.

### TriagemSimplificadaIndisponivel — linhas 39 a 40

```python
class TriagemSimplificadaIndisponivel(Exception):
    """Indica que a pessoa ainda não concluiu uma triagem extensa."""
```

**Explicação deste trecho:**

**Linha 39 — ClassDef** (nível 0 do bloco).

Define a classe `TriagemSimplificadaIndisponivel` herdando de `Exception`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 39:

**Linha 40 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### TriagemConcluida — linhas 43 a 44

```python
class TriagemConcluida(Exception):
    """Impede alteração de um resultado já registrado no histórico."""
```

**Explicação deste trecho:**

**Linha 43 — ClassDef** (nível 0 do bloco).

Define a classe `TriagemConcluida` herdando de `Exception`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 43:

**Linha 44 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### TriagemIncompleta — linhas 47 a 48

```python
class TriagemIncompleta(Exception):
    """Indica que existem perguntas obrigatórias ainda sem resposta."""
```

**Explicação deste trecho:**

**Linha 47 — ClassDef** (nível 0 do bloco).

Define a classe `TriagemIncompleta` herdando de `Exception`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 47:

**Linha 48 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### TriagemExtensaNecessaria — linhas 51 a 52

```python
class TriagemExtensaNecessaria(Exception):
    """Indica que a versão rápida deixou de ser segura para o usuário."""
```

**Explicação deste trecho:**

**Linha 51 — ClassDef** (nível 0 do bloco).

Define a classe `TriagemExtensaNecessaria` herdando de `Exception`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 51:

**Linha 52 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### PerguntaInvalida — linhas 55 a 56

```python
class PerguntaInvalida(Exception):
    """Impede códigos de pergunta ou alternativa fora do catálogo."""
```

**Explicação deste trecho:**

**Linha 55 — ClassDef** (nível 0 do bloco).

Define a classe `PerguntaInvalida` herdando de `Exception`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 55:

**Linha 56 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### Assign — linhas 59 a 61

```python
PERFIS_COM_TRIAGEM = {
    Usuario.Perfil.DOADOR,
}
```

**Explicação deste trecho:**

**Linha 59 — Assign** (nível 0 do bloco).

Associa `PERFIS_COM_TRIAGEM` a uma coleção Set com 1 itens, na expressão `{Usuario.Perfil.DOADOR}`.

### Assign — linhas 65 a 76

```python
ORDEM_EXTENSA = [
    "EXT-01", "EXT-01A", "EXT-02", "EXT-03", "EXT-04", "EXT-05", "EXT-05A",
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
```

**Explicação deste trecho:**

**Linha 65 — Assign** (nível 0 do bloco).

Associa `ORDEM_EXTENSA` a uma coleção List com 56 itens, na expressão `['EXT-01', 'EXT-01A', 'EXT-02', 'EXT-03', 'EXT-04', 'EXT-05', 'EXT-05A', 'EXT-05B', 'EXT-06', 'EXT-07', 'EXT-07A', 'EXT-08', 'EXT-09', 'EXT-10', 'EXT-11', 'EXT-11A', 'EXT-12', 'EXT-13', 'EXT-14', 'EXT-15', 'EXT-16', 'EXT-17', 'EXT-18', 'EXT-19', 'EXT-20', 'EXT-21', 'EXT-22', 'EXT-23', 'EXT-24', 'EXT-25', 'EXT-26', 'EXT-27', 'EXT-28', 'EXT-29', 'EXT-30', 'EXT-31', 'EXT-32', 'EXT-33', 'EXT-34', 'EXT-35', 'EXT-36', 'EXT-37', 'EXT-38', 'EXT-39', 'EXT-40', 'EXT-41', 'EXT-42', 'EXT-43', 'EXT-44', 'EXT-45', 'EXT-46', 'EXT-47', 'EXT-48', 'EXT-49', 'EXT-50', 'EXT-51']`.

### Assign — linhas 78 a 81

```python
ORDEM_SIMPLIFICADA = [
    f"SIM-{numero:02d}"
    for numero in range(1, 19)
]
```

**Explicação deste trecho:**

**Linha 78 — Assign** (nível 0 do bloco).

Associa `ORDEM_SIMPLIFICADA` a uma coleção/gerador construído por compreensão em `[f'SIM-{numero:02d}' for numero in range(1, 19)]`: percorre as fontes e aplica os filtros declarados.

### pode_responder — linhas 84 a 87

```python
def pode_responder(usuario):
    """Diz se o perfil pode realizar uma triagem para doação."""

    return usuario.perfil in PERFIS_COM_TRIAGEM
```

**Explicação deste trecho:**

**Linha 84 — FunctionDef** (nível 0 do bloco).

Define `pode_responder(usuario)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 84:

**Linha 85 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 87 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a comparação `usuario.perfil` contido em `PERFIS_COM_TRIAGEM` ao chamador.

### obter_extensa_base — linhas 90 a 100

```python
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
```

**Explicação deste trecho:**

**Linha 90 — FunctionDef** (nível 0 do bloco).

Define `obter_extensa_base(usuario)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 90:

**Linha 91 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 93 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `usuario.triagens.filter(modalidade=Triagem.Modalidade.EXTENSA, status=Triagem.Status.CONCLUIDA).order_by('-finalizada_em', '-iniciada_em').first`, que obtém o primeiro resultado ou None ao chamador.

### obter_extensa_reutilizavel — linhas 103 a 114

```python
def obter_extensa_reutilizavel(usuario):
    """Retorna a extensa concluída atual que pode preencher uma nova triagem."""

    return (
        usuario.triagens.filter(
            modalidade=Triagem.Modalidade.EXTENSA,
            status=Triagem.Status.CONCLUIDA,
            regra_version=TRIAGEM_RULE_VERSION,
        )
        .order_by("-finalizada_em", "-iniciada_em")
        .first()
    )
```

**Explicação deste trecho:**

**Linha 103 — FunctionDef** (nível 0 do bloco).

Define `obter_extensa_reutilizavel(usuario)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 103:

**Linha 104 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 106 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `usuario.triagens.filter(modalidade=Triagem.Modalidade.EXTENSA, status=Triagem.Status.CONCLUIDA, regra_version=TRIAGEM_RULE_VERSION).order_by('-finalizada_em', '-iniciada_em').first`, que obtém o primeiro resultado ou None ao chamador.

### _respostas_da_triagem — linhas 117 a 123

```python
def _respostas_da_triagem(triagem):
    """Transforma registros do banco no mapa esperado pelo catálogo e motor."""

    return {
        resposta.id_pergunta: resposta.valor
        for resposta in triagem.respostas.all()
    }
```

**Explicação deste trecho:**

**Linha 117 — FunctionDef** (nível 0 do bloco).

Define `_respostas_da_triagem(triagem)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 117:

**Linha 118 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 120 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve uma coleção/gerador construído por compreensão em `{resposta.id_pergunta: resposta.valor for resposta in triagem.respostas.all()}`: percorre as fontes e aplica os filtros declarados ao chamador.

### _condicao_atendida — linhas 126 a 139

```python
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
```

**Explicação deste trecho:**

**Linha 126 — FunctionDef** (nível 0 do bloco).

Define `_condicao_atendida(pergunta, respostas)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 126:

**Linha 127 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 129 — Assign** (nível 1 do bloco).

Associa `condicao` a a chamada `pergunta.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'mostrar_se'`.


**Linha 130 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `condicao`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 130:

**Linha 131 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `True` ao chamador.

**Linha 133 — For** (nível 1 do bloco).

Percorre `condicao.items()`; cada item é atribuído a `(id_anterior, codigos_aceitos)` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 133:

**Linha 134 — Assign** (nível 2 do bloco).

Associa `valor` a pelo menos uma das condições: `respostas.get(id_anterior)` ; `{}` (com avaliação interrompida assim que o resultado é determinado).

**Linha 135 — Assign** (nível 2 do bloco).

Associa `codigos` a a chamada `set`; argumentos posicionais: `valor.get('codigos') or []`.


**Linha 136 — If** (nível 2 do bloco).

Escolhe um caminho verificando a negação de `codigos.intersection(codigos_aceitos)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 136:

**Linha 137 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve o valor literal `False` ao chamador.

**Linha 139 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor literal `True` ao chamador.

### _copiar_respostas_para_nova_triagem — linhas 142 a 160

```python
def _copiar_respostas_para_nova_triagem(origem, destino):
    """Copia respostas para uma nova triagem sem alterar o histórico original."""

    RespostaTriagem.objects.bulk_create(
        [
            RespostaTriagem(
                triagem=destino,
                id_pergunta=resposta.id_pergunta,
                codigo_resposta=resposta.codigo_resposta,
                resposta_label=resposta.resposta_label,
                data_evento=resposta.data_evento,
                metadata=resposta.metadata,
                valor=resposta.valor,
                rule_version=resposta.rule_version,
                source_ref=resposta.source_ref,
            )
            for resposta in origem.respostas.order_by("id_resposta")
        ]
    )
```

**Explicação deste trecho:**

**Linha 142 — FunctionDef** (nível 0 do bloco).

Define `_copiar_respostas_para_nova_triagem(origem, destino)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 142:

**Linha 143 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 145 — Expr** (nível 1 do bloco).

Executa a chamada `RespostaTriagem.objects.bulk_create`, que grava uma coleção em lote, sem executar save de cada instância; argumentos posicionais: `[RespostaTriagem(triagem=destino, id_pergunta=resposta.id_pergunta, codigo_resposta=resposta.codigo_resposta, resposta_label=resposta.resposta_label, data_evento=resposta.data_evento, metadata=resposta.metadata, valor=resposta.valor, rule_version=resposta.rule_version, source_ref=resposta.source_ref) for resposta in origem.respostas.order_by('id_resposta')]`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

### calcular_fluxo — linhas 163 a 203

```python
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
        and _condicao_atendida(
            PERGUNTAS_EXTENSAS[id_pergunta],
            respostas,
        )
    ]
    indice_confirmacao = ORDEM_SIMPLIFICADA.index("SIM-17")
    return [
        *ORDEM_SIMPLIFICADA[:indice_confirmacao],
        *detalhadas,
        *ORDEM_SIMPLIFICADA[indice_confirmacao:],
    ]
```

**Explicação deste trecho:**

**Linha 163 — FunctionDef** (nível 0 do bloco).

Define `calcular_fluxo(triagem)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 163:

**Linha 164 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 166 — Assign** (nível 1 do bloco).

Associa `respostas` a a chamada `_respostas_da_triagem`; argumentos posicionais: `triagem`.


**Linha 168 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `triagem.modalidade` igual a `Triagem.Modalidade.EXTENSA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 168:

**Linha 169 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve uma coleção/gerador construído por compreensão em `[id_pergunta for id_pergunta in ORDEM_EXTENSA if _condicao_atendida(PERGUNTAS_EXTENSAS[id_pergunta], respostas)]`: percorre as fontes e aplica os filtros declarados ao chamador.

**Linha 178 — Assign** (nível 1 do bloco).

Associa `ids_abertos` a a chamada `set`.


**Linha 179 — For** (nível 1 do bloco).

Percorre `respostas.items()`; cada item é atribuído a `(id_pergunta, valor)` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 179:

**Linha 180 — Assign** (nível 2 do bloco).

Associa `pergunta` a a chamada `PERGUNTAS_SIMPLIFICADAS.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `id_pergunta`.


**Linha 181 — If** (nível 2 do bloco).

Escolhe um caminho verificando a negação de `pergunta`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 181:

**Linha 182 — Continue** (nível 3 do bloco).

Pula o restante da iteração atual e segue para o próximo item do laço.

**Linha 183 — For** (nível 2 do bloco).

Percorre `valor.get('codigos') or []`; cada item é atribuído a `codigo` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 183:

**Linha 184 — Expr** (nível 3 do bloco).

Executa a chamada `ids_abertos.update`, que no QuerySet grava diretamente os campos dos resultados, sem chamar save de cada instância; argumentos posicionais: `pergunta['abrir_extensa'].get(codigo, [])`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 189 — Assign** (nível 1 do bloco).

Associa `detalhadas` a uma coleção/gerador construído por compreensão em `[id_pergunta for id_pergunta in ORDEM_EXTENSA if id_pergunta in ids_abertos and _condicao_atendida(PERGUNTAS_EXTENSAS[id_pergunta], respostas)]`: percorre as fontes e aplica os filtros declarados.

**Linha 198 — Assign** (nível 1 do bloco).

Associa `indice_confirmacao` a a chamada `ORDEM_SIMPLIFICADA.index`; argumentos posicionais: `'SIM-17'`.


**Linha 199 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve uma coleção List com 3 itens, na expressão `[*ORDEM_SIMPLIFICADA[:indice_confirmacao], *detalhadas, *ORDEM_SIMPLIFICADA[indice_confirmacao:]]` ao chamador.

### iniciar_triagem — linhas 206 a 284

```python
@transaction.atomic
def iniciar_triagem(
    usuario,
    modalidade,
    ip=None,
    aceite_termo=True,
    reutilizar_respostas=False,
):
    """Cria/retoma a triagem após o aceite registrado pela camada de entrada.

    A view exige o checkbox explicitamente; o valor padrão preserva a API de
    serviço usada por integrações internas que já representam esse aceite.
    """

    if not pode_responder(usuario):
        raise PermissionDenied(
            "A triagem está disponível para Doadores."
        )

    if modalidade not in {
        Triagem.Modalidade.EXTENSA,
        Triagem.Modalidade.SIMPLIFICADA,
    }:
        raise ValueError("Modalidade de triagem inválida.")

    if not aceite_termo:
        raise PermissionDenied(
            "Confirme ciência do termo da pré-triagem antes de começar."
        )

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

    if modalidade == Triagem.Modalidade.EXTENSA and reutilizar_respostas:
        origem = obter_extensa_reutilizavel(usuario)
        if origem is not None:
            _copiar_respostas_para_nova_triagem(origem, triagem)

    triagem.fluxo_perguntas = calcular_fluxo(triagem)
    triagem.save(update_fields=["fluxo_perguntas", "atualizada_em"])
    return triagem
```

**Explicação deste trecho:**

**Linha 207 — FunctionDef** (nível 0 do bloco).

Define `iniciar_triagem(usuario, modalidade, ip=None, aceite_termo=True, reutilizar_respostas=False)`. O corpo só executa quando a função/método é chamado. Decoradores: `transaction.atomic`.

Bloco `body` da linha 207:

**Linha 214 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 220 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `pode_responder(usuario)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 220:

**Linha 221 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'A triagem está disponível para Doadores.'`.

**Linha 225 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `modalidade` não contido em `{Triagem.Modalidade.EXTENSA, Triagem.Modalidade.SIMPLIFICADA}`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 225:

**Linha 229 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValueError`; argumentos posicionais: `'Modalidade de triagem inválida.'`.

**Linha 231 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `aceite_termo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 231:

**Linha 232 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'Confirme ciência do termo da pré-triagem antes de começar.'`.

**Linha 236 — Assign** (nível 1 do bloco).

Associa `existente` a a chamada `usuario.triagens.filter(modalidade=modalidade, status=Triagem.Status.EM_ANDAMENTO).order_by('-iniciada_em').first`, que obtém o primeiro resultado ou None.


**Linha 244 — If** (nível 1 do bloco).

Escolhe um caminho verificando o valor associado ao nome `existente`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 244:

**Linha 245 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `existente` ao chamador.

**Linha 247 — Assign** (nível 1 do bloco).

Associa `extensa_base` a o valor literal `None`.

**Linha 248 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `modalidade` igual a `Triagem.Modalidade.SIMPLIFICADA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 248:

**Linha 249 — Assign** (nível 2 do bloco).

Associa `extensa_base` a a chamada `obter_extensa_base`; argumentos posicionais: `usuario`.


**Linha 250 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `extensa_base` o mesmo objeto que `None`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 250:

**Linha 251 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `TriagemSimplificadaIndisponivel`; argumentos posicionais: `'Conclua primeiro uma triagem extensa.'`.

**Linha 255 — Assign** (nível 1 do bloco).

Associa `(consentimento, _)` a a chamada `ConsentimentoLGPD.objects.get_or_create`, que procura pelas chaves; se não existir, cria usando também defaults; argumentos nomeados: `usuario=usuario`, `tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM`, `versao_termo=TRIAGEM_RULE_VERSION`, `defaults={'aceito': True, 'ip': ip}`.

- `usuario=usuario`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `versao_termo=TRIAGEM_RULE_VERSION`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `defaults={'aceito': True, 'ip': ip}`: valores adicionais usados na criação/atualização.

**Linha 261 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `consentimento.aceito`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 261:

**Linha 262 — Assign** (nível 2 do bloco).

Associa `consentimento.aceito` a o valor literal `True`.

**Linha 263 — Assign** (nível 2 do bloco).

Associa `consentimento.revogado_em` a o valor literal `None`.

**Linha 264 — Assign** (nível 2 do bloco).

Associa `consentimento.ip` a o valor associado ao nome `ip`.

**Linha 265 — Expr** (nível 2 do bloco).

Executa a chamada `consentimento.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['aceito', 'revogado_em', 'ip']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 269 — Assign** (nível 1 do bloco).

Associa `triagem` a a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=usuario`, `modalidade=modalidade`, `status=Triagem.Status.EM_ANDAMENTO`, `regra_version=TRIAGEM_RULE_VERSION`, `triagem_base=extensa_base`.

- `usuario=usuario`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `modalidade=modalidade`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status=Triagem.Status.EM_ANDAMENTO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `regra_version=TRIAGEM_RULE_VERSION`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `triagem_base=extensa_base`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 277 — If** (nível 1 do bloco).

Escolhe um caminho verificando todas as condições: `modalidade == Triagem.Modalidade.EXTENSA` ; `reutilizar_respostas` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 277:

**Linha 278 — Assign** (nível 2 do bloco).

Associa `origem` a a chamada `obter_extensa_reutilizavel`; argumentos posicionais: `usuario`.


**Linha 279 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `origem` um objeto diferente de `None`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 279:

**Linha 280 — Expr** (nível 3 do bloco).

Executa a chamada `_copiar_respostas_para_nova_triagem`; argumentos posicionais: `origem`, `triagem`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 282 — Assign** (nível 1 do bloco).

Associa `triagem.fluxo_perguntas` a a chamada `calcular_fluxo`; argumentos posicionais: `triagem`.


**Linha 283 — Expr** (nível 1 do bloco).

Executa a chamada `triagem.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['fluxo_perguntas', 'atualizada_em']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 284 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `triagem` ao chamador.

### obter_pergunta_atual — linhas 287 a 297

```python
def obter_pergunta_atual(triagem):
    """Retorna a pergunta apontada pelo andamento ou nada após o fim."""

    if triagem.status != Triagem.Status.EM_ANDAMENTO:
        return None
    if triagem.pergunta_atual >= len(triagem.fluxo_perguntas):
        return None

    return obter_pergunta(
        triagem.fluxo_perguntas[triagem.pergunta_atual]
    )
```

**Explicação deste trecho:**

**Linha 287 — FunctionDef** (nível 0 do bloco).

Define `obter_pergunta_atual(triagem)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 287:

**Linha 288 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 290 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `triagem.status` diferente de `Triagem.Status.EM_ANDAMENTO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 290:

**Linha 291 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

**Linha 292 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `triagem.pergunta_atual` maior ou igual a `len(triagem.fluxo_perguntas)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 292:

**Linha 293 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

**Linha 295 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `obter_pergunta`; argumentos posicionais: `triagem.fluxo_perguntas[triagem.pergunta_atual]` ao chamador.

### _validar_valor — linhas 300 a 315

```python
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
```

**Explicação deste trecho:**

**Linha 300 — FunctionDef** (nível 0 do bloco).

Define `_validar_valor(pergunta, valor)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 300:

**Linha 301 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 303 — Assign** (nível 1 do bloco).

Associa `codigos` a pelo menos uma das condições: `valor.get('codigos')` ; `[]` (com avaliação interrompida assim que o resultado é determinado).

**Linha 304 — Assign** (nível 1 do bloco).

Associa `permitidos` a uma coleção/gerador construído por compreensão em `{opcao['codigo'] for opcao in pergunta['opcoes']}`: percorre as fontes e aplica os filtros declarados.

**Linha 308 — If** (nível 1 do bloco).

Escolhe um caminho verificando pelo menos uma das condições: `not codigos` ; `not set(codigos).issubset(permitidos)` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 308:

**Linha 309 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PerguntaInvalida`; argumentos posicionais: `'A resposta não pertence às alternativas da pergunta.'`.

**Linha 312 — If** (nível 1 do bloco).

Escolhe um caminho verificando todas as condições: `not pergunta['multipla']` ; `len(codigos) != 1` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 312:

**Linha 313 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PerguntaInvalida`; argumentos posicionais: `'Esta pergunta aceita somente uma alternativa.'`.

### _rotulo_resposta — linhas 318 a 325

```python
def _rotulo_resposta(pergunta, codigos):
    """Mantém no campo legado os rótulos visíveis ao usuário."""

    rotulos = {
        opcao["codigo"]: opcao["rotulo"]
        for opcao in pergunta["opcoes"]
    }
    return "; ".join(rotulos[codigo] for codigo in codigos)
```

**Explicação deste trecho:**

**Linha 318 — FunctionDef** (nível 0 do bloco).

Define `_rotulo_resposta(pergunta, codigos)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 318:

**Linha 319 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 321 — Assign** (nível 1 do bloco).

Associa `rotulos` a uma coleção/gerador construído por compreensão em `{opcao['codigo']: opcao['rotulo'] for opcao in pergunta['opcoes']}`: percorre as fontes e aplica os filtros declarados.

**Linha 325 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `'; '.join`; argumentos posicionais: `(rotulos[codigo] for codigo in codigos)` ao chamador.

### _primeira_data — linhas 328 a 338

```python
def _primeira_data(valor):
    """Preenche o campo legado com a primeira data estruturada disponível."""

    datas = valor.get("datas") or {}
    if not datas:
        return None

    try:
        return date.fromisoformat(next(iter(datas.values())))
    except (TypeError, ValueError):
        raise PerguntaInvalida("A data da resposta é inválida.") from None
```

**Explicação deste trecho:**

**Linha 328 — FunctionDef** (nível 0 do bloco).

Define `_primeira_data(valor)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 328:

**Linha 329 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 331 — Assign** (nível 1 do bloco).

Associa `datas` a pelo menos uma das condições: `valor.get('datas')` ; `{}` (com avaliação interrompida assim que o resultado é determinado).

**Linha 332 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `datas`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 332:

**Linha 333 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

**Linha 335 — Try** (nível 1 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 335:

**Linha 336 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `date.fromisoformat`; argumentos posicionais: `next(iter(datas.values()))` ao chamador.

Erro tratado: `(TypeError, ValueError)`.

**Linha 338 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PerguntaInvalida`; argumentos posicionais: `'A data da resposta é inválida.'`.

### _resposta_exige_extensa — linhas 341 a 355

```python
def _resposta_exige_extensa(id_pergunta, codigos):
    """Centraliza as respostas que invalidam o resumo da versão rápida."""

    escolhas = set(codigos)
    return (
        (
            id_pergunta == "SIM-01"
            and bool(escolhas & {"INCORRETO", "NAO_FIZ", "NAO_SEI"})
        )
        or (
            id_pergunta == "SIM-17"
            and bool(escolhas & {"SIM", "NAO_SEI"})
        )
        or (id_pergunta == "SIM-18" and "EXTENSA" in escolhas)
    )
```

**Explicação deste trecho:**

**Linha 341 — FunctionDef** (nível 0 do bloco).

Define `_resposta_exige_extensa(id_pergunta, codigos)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 341:

**Linha 342 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 344 — Assign** (nível 1 do bloco).

Associa `escolhas` a a chamada `set`; argumentos posicionais: `codigos`.


**Linha 345 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve pelo menos uma das condições: `id_pergunta == 'SIM-01' and bool(escolhas & {'INCORRETO', 'NAO_FIZ', 'NAO_SEI'})` ; `id_pergunta == 'SIM-17' and bool(escolhas & {'SIM', 'NAO_SEI'})` ; `id_pergunta == 'SIM-18' and 'EXTENSA' in escolhas` (com avaliação interrompida assim que o resultado é determinado) ao chamador.

### atualizar_tipo_sanguineo_do_usuario — linhas 358 a 383

```python
def atualizar_tipo_sanguineo_do_usuario(triagem, valor):
    """
    Atualiza o tipo sanguineo do usuario a partir da pergunta informativa.

    Essa informacao nao interfere no resultado da triagem; ela apenas liga o
    usuario aos alertas internos de estoque e a compatibilidade sanguinea.
    """

    codigos = valor.get("codigos") or []
    if not codigos:
        return

    try:
        tipo_sanguineo = normalizar_tipo_sanguineo(codigos[0])
    except ValueError:
        return

    usuario = triagem.usuario
    if usuario.tipo_sanguineo_confirmado:
        return

    if usuario.tipo_sanguineo == tipo_sanguineo:
        return

    usuario.tipo_sanguineo = tipo_sanguineo
    usuario.save(update_fields=["tipo_sanguineo", "atualizado_em"])
```

**Explicação deste trecho:**

**Linha 358 — FunctionDef** (nível 0 do bloco).

Define `atualizar_tipo_sanguineo_do_usuario(triagem, valor)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 358:

**Linha 359 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 366 — Assign** (nível 1 do bloco).

Associa `codigos` a pelo menos uma das condições: `valor.get('codigos')` ; `[]` (com avaliação interrompida assim que o resultado é determinado).

**Linha 367 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `codigos`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 367:

**Linha 368 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve nenhum valor explícito (None) ao chamador.

**Linha 370 — Try** (nível 1 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 370:

**Linha 371 — Assign** (nível 2 do bloco).

Associa `tipo_sanguineo` a a chamada `normalizar_tipo_sanguineo`; argumentos posicionais: `codigos[0]`.


Erro tratado: `ValueError`.

**Linha 373 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve nenhum valor explícito (None) ao chamador.

**Linha 375 — Assign** (nível 1 do bloco).

Associa `usuario` a o atributo `usuario` de `triagem`.

**Linha 376 — If** (nível 1 do bloco).

Escolhe um caminho verificando o atributo `tipo_sanguineo_confirmado` de `usuario`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 376:

**Linha 377 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve nenhum valor explícito (None) ao chamador.

**Linha 379 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `usuario.tipo_sanguineo` igual a `tipo_sanguineo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 379:

**Linha 380 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve nenhum valor explícito (None) ao chamador.

**Linha 382 — Assign** (nível 1 do bloco).

Associa `usuario.tipo_sanguineo` a o valor associado ao nome `tipo_sanguineo`.

**Linha 383 — Expr** (nível 1 do bloco).

Executa a chamada `usuario.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['tipo_sanguineo', 'atualizado_em']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

### salvar_resposta — linhas 386 a 477

```python
def salvar_resposta(triagem, id_pergunta, valor):
    """Salva ou corrige uma resposta e avança o fluxo com segurança."""

    triagem_recebida = triagem
    exige_extensa = False

    # O bloco atômico termina antes da exceção de redirecionamento. Assim, a
    # tentativa rápida fica cancelada no histórico sem deixar dados pela metade.
    with transaction.atomic():
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

        if id_pergunta == "EXT-01A":
            atualizar_tipo_sanguineo_do_usuario(registro, valor)

        exige_extensa = (
            registro.modalidade == Triagem.Modalidade.SIMPLIFICADA
            and _resposta_exige_extensa(id_pergunta, codigos)
        )
        if exige_extensa:
            registro.status = Triagem.Status.CANCELADA
            registro.save(update_fields=["status", "atualizada_em"])
        else:
            fluxo = calcular_fluxo(registro)
            registro.fluxo_perguntas = fluxo

            # Se uma correção fechar uma ramificação, suas respostas antigas
            # deixam de ser válidas e não podem participar do cálculo final.
            registro.respostas.exclude(id_pergunta__in=fluxo).delete()

            # Estas respostas pedem revisão, portanto não avançam o cursor.
            if (
                id_pergunta == "EXT-01"
                and "NAO" in codigos
            ) or (
                id_pergunta == "EXT-51"
                and "REVISAR" in codigos
            ):
                registro.pergunta_atual = 0
            else:
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

        # Mantém o objeto recebido sincronizado para a view usar imediatamente.
        triagem_recebida.fluxo_perguntas = registro.fluxo_perguntas
        triagem_recebida.pergunta_atual = registro.pergunta_atual
        triagem_recebida.status = registro.status
        triagem_recebida.atualizada_em = registro.atualizada_em

    if exige_extensa:
        raise TriagemExtensaNecessaria(
            "O resumo mudou; continue em uma nova triagem extensa."
        )

    return triagem_recebida
```

**Explicação deste trecho:**

**Linha 386 — FunctionDef** (nível 0 do bloco).

Define `salvar_resposta(triagem, id_pergunta, valor)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 386:

**Linha 387 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 389 — Assign** (nível 1 do bloco).

Associa `triagem_recebida` a o valor associado ao nome `triagem`.

**Linha 390 — Assign** (nível 1 do bloco).

Associa `exige_extensa` a o valor literal `False`.

**Linha 394 — With** (nível 1 do bloco).

Executa sob os contextos `transaction.atomic()`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 394:

**Linha 395 — Assign** (nível 2 do bloco).

Associa `registro` a a chamada `Triagem.objects.select_for_update().get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `pk=triagem.pk`.

- `pk=triagem.pk`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 396 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `registro.status` diferente de `Triagem.Status.EM_ANDAMENTO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 396:

**Linha 397 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `TriagemConcluida`; argumentos posicionais: `'Uma triagem concluída não pode ser alterada.'`.

**Linha 400 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `id_pergunta` não contido em `registro.fluxo_perguntas`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 400:

**Linha 401 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `PerguntaInvalida`; argumentos posicionais: `'A pergunta não pertence a esta triagem.'`.

**Linha 403 — Assign** (nível 2 do bloco).

Associa `pergunta` a a chamada `obter_pergunta`; argumentos posicionais: `id_pergunta`.


**Linha 404 — Expr** (nível 2 do bloco).

Executa a chamada `_validar_valor`; argumentos posicionais: `pergunta`, `valor`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 405 — Assign** (nível 2 do bloco).

Associa `codigos` a o item ou recorte `'codigos'` de `valor`.

**Linha 407 — Expr** (nível 2 do bloco).

Executa a chamada `RespostaTriagem.objects.update_or_create`, que procura pelas chaves; atualiza defaults se existir ou cria se não existir; argumentos nomeados: `triagem=registro`, `id_pergunta=id_pergunta`, `defaults={'codigo_resposta': codigos[0], 'resposta_label': _rotulo_resposta(pergunta, codigos), 'data_evento': _primeira_data(valor), 'metadata': {chave: conteudo for chave, conteudo in valor.items() if chave not in {'codigos', 'datas'}}, 'valor': valor, 'rule_version': pergunta['regra_version'], 'source_ref': pergunta['fonte']}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 425 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `id_pergunta` igual a `'EXT-01A'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 425:

**Linha 426 — Expr** (nível 3 do bloco).

Executa a chamada `atualizar_tipo_sanguineo_do_usuario`; argumentos posicionais: `registro`, `valor`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 428 — Assign** (nível 2 do bloco).

Associa `exige_extensa` a todas as condições: `registro.modalidade == Triagem.Modalidade.SIMPLIFICADA` ; `_resposta_exige_extensa(id_pergunta, codigos)` (com avaliação interrompida assim que o resultado é determinado).

**Linha 432 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `exige_extensa`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 432:

**Linha 433 — Assign** (nível 3 do bloco).

Associa `registro.status` a o atributo `CANCELADA` de `Triagem.Status`.

**Linha 434 — Expr** (nível 3 do bloco).

Executa a chamada `registro.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['status', 'atualizada_em']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 432:

**Linha 436 — Assign** (nível 3 do bloco).

Associa `fluxo` a a chamada `calcular_fluxo`; argumentos posicionais: `registro`.


**Linha 437 — Assign** (nível 3 do bloco).

Associa `registro.fluxo_perguntas` a o valor associado ao nome `fluxo`.

**Linha 441 — Expr** (nível 3 do bloco).

Executa a chamada `registro.respostas.exclude(id_pergunta__in=fluxo).delete`, que remove o objeto/conjunto conforme o tipo e as relações envolvidas. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 444 — If** (nível 3 do bloco).

Escolhe um caminho verificando pelo menos uma das condições: `id_pergunta == 'EXT-01' and 'NAO' in codigos` ; `id_pergunta == 'EXT-51' and 'REVISAR' in codigos` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 444:

**Linha 451 — Assign** (nível 4 do bloco).

Associa `registro.pergunta_atual` a o valor literal `0`.

Bloco `orelse` da linha 444:

**Linha 453 — Assign** (nível 4 do bloco).

Associa `registro.pergunta_atual` a a chamada `min`; argumentos posicionais: `fluxo.index(id_pergunta) + 1`, `len(fluxo)`.


**Linha 458 — Expr** (nível 3 do bloco).

Executa a chamada `registro.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['fluxo_perguntas', 'pergunta_atual', 'atualizada_em']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 467 — Assign** (nível 2 do bloco).

Associa `triagem_recebida.fluxo_perguntas` a o atributo `fluxo_perguntas` de `registro`.

**Linha 468 — Assign** (nível 2 do bloco).

Associa `triagem_recebida.pergunta_atual` a o atributo `pergunta_atual` de `registro`.

**Linha 469 — Assign** (nível 2 do bloco).

Associa `triagem_recebida.status` a o atributo `status` de `registro`.

**Linha 470 — Assign** (nível 2 do bloco).

Associa `triagem_recebida.atualizada_em` a o atributo `atualizada_em` de `registro`.

**Linha 472 — If** (nível 1 do bloco).

Escolhe um caminho verificando o valor associado ao nome `exige_extensa`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 472:

**Linha 473 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `TriagemExtensaNecessaria`; argumentos posicionais: `'O resumo mudou; continue em uma nova triagem extensa.'`.

**Linha 477 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `triagem_recebida` ao chamador.

### voltar_pergunta — linhas 480 a 495

```python
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
```

**Explicação deste trecho:**

**Linha 481 — FunctionDef** (nível 0 do bloco).

Define `voltar_pergunta(triagem)`. O corpo só executa quando a função/método é chamado. Decoradores: `transaction.atomic`.

Bloco `body` da linha 481:

**Linha 482 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 484 — Assign** (nível 1 do bloco).

Associa `triagem_recebida` a o valor associado ao nome `triagem`.

**Linha 485 — Assign** (nível 1 do bloco).

Associa `registro` a a chamada `Triagem.objects.select_for_update().get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `pk=triagem.pk`.

- `pk=triagem.pk`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 486 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `registro.status` diferente de `Triagem.Status.EM_ANDAMENTO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 486:

**Linha 487 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `TriagemConcluida`; argumentos posicionais: `'Uma triagem concluída não pode ser alterada.'`.

**Linha 491 — Assign** (nível 1 do bloco).

Associa `registro.pergunta_atual` a a chamada `max`; argumentos posicionais: `0`, `registro.pergunta_atual - 1`.


**Linha 492 — Expr** (nível 1 do bloco).

Executa a chamada `registro.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['pergunta_atual', 'atualizada_em']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 493 — Assign** (nível 1 do bloco).

Associa `triagem_recebida.pergunta_atual` a o atributo `pergunta_atual` de `registro`.

**Linha 494 — Assign** (nível 1 do bloco).

Associa `triagem_recebida.atualizada_em` a o atributo `atualizada_em` de `registro`.

**Linha 495 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `triagem_recebida` ao chamador.

### editar_pergunta — linhas 498 a 512

```python
@transaction.atomic
def editar_pergunta(triagem, id_pergunta):
    """Reposiciona uma triagem em andamento para uma resposta já salva."""

    registro = Triagem.objects.select_for_update().get(pk=triagem.pk)
    if registro.status != Triagem.Status.EM_ANDAMENTO:
        raise TriagemConcluida("Uma triagem concluída não pode ser alterada.")
    if id_pergunta not in registro.fluxo_perguntas:
        raise PerguntaInvalida("A pergunta não pertence a esta triagem.")

    registro.pergunta_atual = registro.fluxo_perguntas.index(id_pergunta)
    registro.save(update_fields=["pergunta_atual", "atualizada_em"])
    triagem.pergunta_atual = registro.pergunta_atual
    triagem.atualizada_em = registro.atualizada_em
    return triagem
```

**Explicação deste trecho:**

**Linha 499 — FunctionDef** (nível 0 do bloco).

Define `editar_pergunta(triagem, id_pergunta)`. O corpo só executa quando a função/método é chamado. Decoradores: `transaction.atomic`.

Bloco `body` da linha 499:

**Linha 500 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 502 — Assign** (nível 1 do bloco).

Associa `registro` a a chamada `Triagem.objects.select_for_update().get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `pk=triagem.pk`.

- `pk=triagem.pk`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 503 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `registro.status` diferente de `Triagem.Status.EM_ANDAMENTO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 503:

**Linha 504 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `TriagemConcluida`; argumentos posicionais: `'Uma triagem concluída não pode ser alterada.'`.

**Linha 505 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `id_pergunta` não contido em `registro.fluxo_perguntas`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 505:

**Linha 506 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PerguntaInvalida`; argumentos posicionais: `'A pergunta não pertence a esta triagem.'`.

**Linha 508 — Assign** (nível 1 do bloco).

Associa `registro.pergunta_atual` a a chamada `registro.fluxo_perguntas.index`; argumentos posicionais: `id_pergunta`.


**Linha 509 — Expr** (nível 1 do bloco).

Executa a chamada `registro.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['pergunta_atual', 'atualizada_em']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 510 — Assign** (nível 1 do bloco).

Associa `triagem.pergunta_atual` a o atributo `pergunta_atual` de `registro`.

**Linha 511 — Assign** (nível 1 do bloco).

Associa `triagem.atualizada_em` a o atributo `atualizada_em` de `registro`.

**Linha 512 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `triagem` ao chamador.

### concluir_triagem — linhas 515 a 572

```python
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
```

**Explicação deste trecho:**

**Linha 516 — FunctionDef** (nível 0 do bloco).

Define `concluir_triagem(triagem, hoje=None)`. O corpo só executa quando a função/método é chamado. Decoradores: `transaction.atomic`.

Bloco `body` da linha 516:

**Linha 517 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 519 — Assign** (nível 1 do bloco).

Associa `triagem` a a chamada `Triagem.objects.select_for_update().get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `pk=triagem.pk`.

- `pk=triagem.pk`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 520 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `triagem.status` diferente de `Triagem.Status.EM_ANDAMENTO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 520:

**Linha 521 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `TriagemConcluida`; argumentos posicionais: `'Uma triagem concluída não pode ser alterada.'`.

**Linha 525 — Assign** (nível 1 do bloco).

Associa `respostas` a a chamada `_respostas_da_triagem`; argumentos posicionais: `triagem`.


**Linha 526 — Assign** (nível 1 do bloco).

Associa `faltantes` a a expressão `set(triagem.fluxo_perguntas) - set(respostas)`; seus operadores determinam o cálculo.

**Linha 527 — If** (nível 1 do bloco).

Escolhe um caminho verificando o valor associado ao nome `faltantes`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 527:

**Linha 528 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `TriagemIncompleta`; argumentos posicionais: `'Ainda existem perguntas sem resposta.'`.

**Linha 532 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `triagem.modalidade` igual a `Triagem.Modalidade.EXTENSA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 532:

**Linha 533 — Assign** (nível 2 do bloco).

Associa `confirmacao` a pelo menos uma das condições: `respostas.get('EXT-51', {}).get('codigos')` ; `[]` (com avaliação interrompida assim que o resultado é determinado).

**Linha 536 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `'CONFIRMAR'` não contido em `confirmacao`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 536:

**Linha 537 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `TriagemIncompleta`; argumentos posicionais: `'Revise e confirme a triagem extensa.'`.

**Linha 538 — Assign** (nível 2 do bloco).

Associa `respostas_base` a o valor literal `None`.

Bloco `orelse` da linha 532:

**Linha 540 — Assign** (nível 2 do bloco).

Associa `confirmacao` a pelo menos uma das condições: `respostas.get('SIM-18', {}).get('codigos')` ; `[]` (com avaliação interrompida assim que o resultado é determinado).

**Linha 543 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `'ENTENDO'` não contido em `confirmacao`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 543:

**Linha 544 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `TriagemIncompleta`; argumentos posicionais: `'Confirme a limitação da versão rápida.'`.

**Linha 545 — Assign** (nível 2 do bloco).

Associa `respostas_base` a a chamada `_respostas_da_triagem`; argumentos posicionais: `triagem.triagem_base`.


**Linha 547 — Assign** (nível 1 do bloco).

Associa `calculo` a a chamada `avaliar_triagem`; argumentos posicionais: `triagem.modalidade`, `respostas`; argumentos nomeados: `hoje=hoje`, `respostas_base=respostas_base`.

- `hoje=hoje`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `respostas_base=respostas_base`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 553 — Assign** (nível 1 do bloco).

Associa `triagem.resultado` a o item ou recorte `'resultado'` de `calculo`.

**Linha 554 — Assign** (nível 1 do bloco).

Associa `triagem.mensagem_resultado` a o item ou recorte `'mensagem'` de `calculo`.

**Linha 555 — Assign** (nível 1 do bloco).

Associa `triagem.data_liberacao` a o item ou recorte `'data_liberacao'` de `calculo`.

**Linha 556 — Assign** (nível 1 do bloco).

Associa `triagem.achados` a o item ou recorte `'achados'` de `calculo`.

**Linha 557 — Assign** (nível 1 do bloco).

Associa `triagem.status` a o atributo `CONCLUIDA` de `Triagem.Status`.

**Linha 558 — Assign** (nível 1 do bloco).

Associa `triagem.finalizada_em` a a chamada `timezone.now`, que obtém o instante atual; timezone.now respeita o tratamento de fuso do Django.


**Linha 559 — Assign** (nível 1 do bloco).

Associa `triagem.pergunta_atual` a a chamada `len`; argumentos posicionais: `triagem.fluxo_perguntas`.


**Linha 560 — Expr** (nível 1 do bloco).

Executa a chamada `triagem.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['resultado', 'mensagem_resultado', 'data_liberacao', 'achados', 'status', 'finalizada_em', 'pergunta_atual', 'atualizada_em']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 572 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `triagem` ao chamador.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 1: `# Este arquivo controla o fluxo e o salvamento da triagem.`
- Linha 3: `# - Permite triagem somente para Doadores e Receptores.`
- Linha 4: `# - Inicia triagens extensas e simplificadas após o aceite do termo.`
- Linha 5: `# - A simplificada utiliza uma triagem extensa concluída como base.`
- Linha 6: `# - Organiza as perguntas conforme as respostas anteriores.`
- Linha 7: `# - Mostra perguntas condicionais quando necessário.`
- Linha 8: `# - Valida perguntas, alternativas e datas recebidas.`
- Linha 9: `# - Salva, atualiza e reutiliza respostas anteriores quando solicitado.`
- Linha 10: `# - Permite voltar ou editar enquanto a triagem está em andamento.`
- Linha 11: `# - Remove respostas que deixam de ser válidas após uma alteração.`
- Linha 12: `# - Impede alterações depois da conclusão.`
- Linha 13: `# - Exige confirmação final antes de calcular o resultado.`
- Linha 14: `# - Envia as respostas para o motor da triagem.`
- Linha 15: `# - Salva resultado, mensagem, achados e data de liberação.`
- Linha 16: `# - Usa transações para evitar dados incompletos ou alterações simultâneas.`
- Linha 18: `# Os catálogos fornecem as perguntas, o motor aplica as regras e este arquivo controla o fluxo, as respostas e a persistência da triagem.`
- Linha 64: `# A ordem explícita evita que a posição dependa da organização física do arquivo.`
- Linha 188: `# Os blocos detalhados aparecem antes das confirmações rápidas finais.`
- Linha 392: `# O bloco atômico termina antes da exceção de redirecionamento. Assim, a`
- Linha 393: `# tentativa rápida fica cancelada no histórico sem deixar dados pela metade.`
- Linha 439: `# Se uma correção fechar uma ramificação, suas respostas antigas`
- Linha 440: `# deixam de ser válidas e não podem participar do cálculo final.`
- Linha 443: `# Estas respostas pedem revisão, portanto não avançam o cursor.`
- Linha 466: `# Mantém o objeto recebido sincronizado para a view usar imediatamente.`

