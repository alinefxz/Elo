# accounts/estoque.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Cadastro, movimentacao, estado publico e alertas de estoque.

**Arquivo original:** [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
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
from .compatibilidade import normalizar_tipo_sanguineo
from .compatibilidade import doadores_aptos_para_convocacao, limite_convocacao_atingido
from .models import (
    AuditoriaAcaoCritica,
    Estoque,
    EstoqueMovimentacao,
    Notificacao,
    Usuario,
)
from .validacao_hemocentro import validar_publicacao_hemocentro


STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA = {
    Estoque.StatusCalculado.CRITICO: Notificacao.Tipo.ESTOQUE_CRITICO,
}


@transaction.atomic
def criar_notificacoes_para_doadores_compativeis(*, estoque, status_calculado):
    """
    Cria notificacoes internas para doadores compativeis.

    Quando o estoque atualizado fica CRITICO, o sistema procura
    doadores compativeis e aptos que autorizaram convocacoes, respeitando
    o limite conjunto de notificacoes de estoque e pedidos.
    """

    if status_calculado not in STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA:
        return 0

    tipo_notificacao = STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA[status_calculado]

    # Serializa as convocacoes por doador antes de conferir o limite conjunto.
    doadores = doadores_aptos_para_convocacao(estoque.tipo_sanguineo).select_for_update()

    nivel = "critico"

    notificacoes = []

    for doador in doadores:
        if limite_convocacao_atingido(doador) or Notificacao.objects.filter(
            usuario=doador, estoque=estoque, tipo=tipo_notificacao, lida=False,
        ).exists():
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

    motivo_limpo = (motivo or "").strip()
    if not motivo_limpo:
        raise ValidationError(
            {"motivo": "Informe o motivo da movimentacao de estoque."}
        )

    motivo_limpo = (motivo or "").strip()

    if not motivo_limpo:
        raise ValidationError(
            {
                "motivo": (
                    "Informe o motivo da movimentacao de estoque."
                )
            }
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
            motivo=motivo_limpo,
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


STATUS_PUBLICO_LABEL = {
    "CRITICO": "Crítico",
    "BAIXO": "Baixo",
    "ADEQUADO": "Adequado",
    "ALTO": "Alto",
}


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
        status_codigo = calcular_status_publico(
            estoque.quantidade_bolsas,
            estoque.nivel_minimo,
            estoque.nivel_critico,
        )
        resultado.append(
            {
                "nome": estoque.hemocentro.nome,
                "cidade": estoque.hemocentro.cidade,
                "estado": estoque.hemocentro.estado,
                "tipo_sanguineo": estoque.tipo_sanguineo,
                "quantidade_bolsas": estoque.quantidade_bolsas,
                # ``status`` permanece como código para compatibilidade com
                # integrações; os campos abaixo facilitam a exibição e os
                # filtros sem expor níveis internos.
                "status": status_codigo,
                "status_codigo": status_codigo,
                "status_label": STATUS_PUBLICO_LABEL[status_codigo],
                "data_atualizacao": estoque.data_atualizacao,
            }
        )

    return resultado
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 12

```python
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
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 14 a 14

```python
from django.core.exceptions import PermissionDenied, ValidationError
```

**Explicação deste trecho:**

**Linha 14 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.exceptions` os nomes `PermissionDenied`, `ValidationError`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 15 a 15

```python
from django.db import transaction
```

**Explicação deste trecho:**

**Linha 15 — ImportFrom** (nível 0 do bloco).

Importa de `django.db` os nomes `transaction`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 16 a 16

```python
from django.urls import reverse
```

**Explicação deste trecho:**

**Linha 16 — ImportFrom** (nível 0 do bloco).

Importa de `django.urls` os nomes `reverse`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 18 a 18

```python
from .auditoria import registrar_auditoria
```

**Explicação deste trecho:**

**Linha 18 — ImportFrom** (nível 0 do bloco).

Importa de `.auditoria` os nomes `registrar_auditoria`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 19 a 19

```python
from .compatibilidade import normalizar_tipo_sanguineo
```

**Explicação deste trecho:**

**Linha 19 — ImportFrom** (nível 0 do bloco).

Importa de `.compatibilidade` os nomes `normalizar_tipo_sanguineo`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 20 a 20

```python
from .compatibilidade import doadores_aptos_para_convocacao, limite_convocacao_atingido
```

**Explicação deste trecho:**

**Linha 20 — ImportFrom** (nível 0 do bloco).

Importa de `.compatibilidade` os nomes `doadores_aptos_para_convocacao`, `limite_convocacao_atingido`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 21 a 27

```python
from .models import (
    AuditoriaAcaoCritica,
    Estoque,
    EstoqueMovimentacao,
    Notificacao,
    Usuario,
)
```

**Explicação deste trecho:**

**Linha 21 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `AuditoriaAcaoCritica`, `Estoque`, `EstoqueMovimentacao`, `Notificacao`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 28 a 28

```python
from .validacao_hemocentro import validar_publicacao_hemocentro
```

**Explicação deste trecho:**

**Linha 28 — ImportFrom** (nível 0 do bloco).

Importa de `.validacao_hemocentro` os nomes `validar_publicacao_hemocentro`. Pontos iniciais indicam importação relativa ao pacote.

### Assign — linhas 31 a 33

```python
STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA = {
    Estoque.StatusCalculado.CRITICO: Notificacao.Tipo.ESTOQUE_CRITICO,
}
```

**Explicação deste trecho:**

**Linha 31 — Assign** (nível 0 do bloco).

Associa `STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA` a um dicionário de 1 entradas; as chaves dão nome aos valores associados.

- Chave `Estoque.StatusCalculado.CRITICO`: recebe o atributo `ESTOQUE_CRITICO` de `Notificacao.Tipo`.

### criar_notificacoes_para_doadores_compativeis — linhas 36 a 82

```python
@transaction.atomic
def criar_notificacoes_para_doadores_compativeis(*, estoque, status_calculado):
    """
    Cria notificacoes internas para doadores compativeis.

    Quando o estoque atualizado fica CRITICO, o sistema procura
    doadores compativeis e aptos que autorizaram convocacoes, respeitando
    o limite conjunto de notificacoes de estoque e pedidos.
    """

    if status_calculado not in STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA:
        return 0

    tipo_notificacao = STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA[status_calculado]

    # Serializa as convocacoes por doador antes de conferir o limite conjunto.
    doadores = doadores_aptos_para_convocacao(estoque.tipo_sanguineo).select_for_update()

    nivel = "critico"

    notificacoes = []

    for doador in doadores:
        if limite_convocacao_atingido(doador) or Notificacao.objects.filter(
            usuario=doador, estoque=estoque, tipo=tipo_notificacao, lida=False,
        ).exists():
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
```

**Explicação deste trecho:**

**Linha 37 — FunctionDef** (nível 0 do bloco).

Define `criar_notificacoes_para_doadores_compativeis(*, estoque, status_calculado)`. O corpo só executa quando a função/método é chamado. Decoradores: `transaction.atomic`.

Bloco `body` da linha 37:

**Linha 38 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 46 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `status_calculado` não contido em `STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 46:

**Linha 47 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `0` ao chamador.

**Linha 49 — Assign** (nível 1 do bloco).

Associa `tipo_notificacao` a o item ou recorte `status_calculado` de `STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA`.

**Linha 52 — Assign** (nível 1 do bloco).

Associa `doadores` a a chamada `doadores_aptos_para_convocacao(estoque.tipo_sanguineo).select_for_update`, que solicita bloqueio dos registros no banco durante a transação.


**Linha 54 — Assign** (nível 1 do bloco).

Associa `nivel` a o valor literal `'critico'`.

**Linha 56 — Assign** (nível 1 do bloco).

Associa `notificacoes` a uma coleção List com 0 itens, na expressão `[]`.

**Linha 58 — For** (nível 1 do bloco).

Percorre `doadores`; cada item é atribuído a `doador` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 58:

**Linha 59 — If** (nível 2 do bloco).

Escolhe um caminho verificando pelo menos uma das condições: `limite_convocacao_atingido(doador)` ; `Notificacao.objects.filter(usuario=doador, estoque=estoque, tipo=tipo_notificacao, lida=False).exists()` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 59:

**Linha 62 — Continue** (nível 3 do bloco).

Pula o restante da iteração atual e segue para o próximo item do laço.

**Linha 64 — Expr** (nível 2 do bloco).

Executa a chamada `notificacoes.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `Notificacao(usuario=doador, estoque=estoque, tipo=tipo_notificacao, titulo=f'Estoque {nivel} para {estoque.tipo_sanguineo}', mensagem=f'O estoque {estoque.tipo_sanguineo} do Hemocentro {estoque.hemocentro.nome} esta em nivel {nivel}. Seu tipo sanguineo ({doador.tipo_sanguineo}) e compativel para doacao.', url_destino=reverse('accounts:estoque_publico'))`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 80 — Expr** (nível 1 do bloco).

Executa a chamada `Notificacao.objects.bulk_create`, que grava uma coleção em lote, sem executar save de cada instância; argumentos posicionais: `notificacoes`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 82 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `len`; argumentos posicionais: `notificacoes` ao chamador.

### calcular_status_calculado — linhas 85 a 101

```python
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
```

**Explicação deste trecho:**

**Linha 85 — FunctionDef** (nível 0 do bloco).

Define `calcular_status_calculado(*, quantidade_bolsas, nivel_minimo, nivel_critico)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 85:

**Linha 86 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 95 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `quantidade_bolsas` menor ou igual a `nivel_critico`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 95:

**Linha 96 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o atributo `CRITICO` de `Estoque.StatusCalculado` ao chamador.

**Linha 98 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `quantidade_bolsas` menor ou igual a `nivel_minimo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 98:

**Linha 99 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o atributo `BAIXO` de `Estoque.StatusCalculado` ao chamador.

**Linha 101 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o atributo `ESTAVEL` de `Estoque.StatusCalculado` ao chamador.

### validar_responsavel_pelo_estoque — linhas 104 a 117

```python
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
```

**Explicação deste trecho:**

**Linha 104 — FunctionDef** (nível 0 do bloco).

Define `validar_responsavel_pelo_estoque(*, estoque, usuario)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 104:

**Linha 105 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 110 — Expr** (nível 1 do bloco).

Executa a chamada `validar_publicacao_hemocentro`; argumentos posicionais: `usuario`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 112 — If** (nível 1 do bloco).

Escolhe um caminho verificando todas as condições: `estoque is not None` ; `estoque.hemocentro_id != usuario.pk` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 112:

**Linha 113 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'Este estoque pertence a outro Hemocentro.'`.

**Linha 117 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor literal `True` ao chamador.

### obter_estoque_do_hemocentro — linhas 120 a 128

```python
def obter_estoque_do_hemocentro(*, hemocentro, tipo_sanguineo):
    """Busca um Estoque de um tipo sanguineo especifico."""

    tipo = normalizar_tipo_sanguineo(tipo_sanguineo)

    return Estoque.objects.filter(
        hemocentro=hemocentro,
        tipo_sanguineo=tipo,
    ).first()
```

**Explicação deste trecho:**

**Linha 120 — FunctionDef** (nível 0 do bloco).

Define `obter_estoque_do_hemocentro(*, hemocentro, tipo_sanguineo)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 120:

**Linha 121 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 123 — Assign** (nível 1 do bloco).

Associa `tipo` a a chamada `normalizar_tipo_sanguineo`; argumentos posicionais: `tipo_sanguineo`.


**Linha 125 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `Estoque.objects.filter(hemocentro=hemocentro, tipo_sanguineo=tipo).first`, que obtém o primeiro resultado ou None ao chamador.

### cadastrar_estoque — linhas 131 a 197

```python
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
```

**Explicação deste trecho:**

**Linha 131 — FunctionDef** (nível 0 do bloco).

Define `cadastrar_estoque(*, hemocentro, tipo_sanguineo, nivel_minimo, nivel_critico, quantidade_bolsas=0, request=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 131:

**Linha 140 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 145 — Expr** (nível 1 do bloco).

Executa a chamada `validar_publicacao_hemocentro`; argumentos posicionais: `hemocentro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 147 — Assign** (nível 1 do bloco).

Associa `tipo` a a chamada `normalizar_tipo_sanguineo`; argumentos posicionais: `tipo_sanguineo`.


**Linha 149 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `nivel_critico` maior que `nivel_minimo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 149:

**Linha 150 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `{'nivel_critico': 'O nivel critico deve ser menor ou igual ao nivel minimo.'}`.

**Linha 158 — If** (nível 1 do bloco).

Escolhe um caminho verificando a chamada `Estoque.objects.filter(hemocentro=hemocentro, tipo_sanguineo=tipo).exists`, que verifica se há pelo menos um resultado. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 158:

**Linha 162 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `f'Ja existe estoque cadastrado para o tipo {tipo} neste hemocentro.'`.

**Linha 166 — Assign** (nível 1 do bloco).

Associa `status_calculado` a a chamada `calcular_status_calculado`; argumentos nomeados: `quantidade_bolsas=quantidade_bolsas`, `nivel_minimo=nivel_minimo`, `nivel_critico=nivel_critico`.

- `quantidade_bolsas=quantidade_bolsas`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nivel_minimo=nivel_minimo`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nivel_critico=nivel_critico`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 172 — With** (nível 1 do bloco).

Executa sob os contextos `transaction.atomic()`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 172:

**Linha 173 — Assign** (nível 2 do bloco).

Associa `estoque` a a chamada `Estoque.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `hemocentro=hemocentro`, `tipo_sanguineo=tipo`, `quantidade_bolsas=quantidade_bolsas`, `nivel_minimo=nivel_minimo`, `nivel_critico=nivel_critico`, `status_calculado=status_calculado`.

- `hemocentro=hemocentro`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_sanguineo=tipo`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `quantidade_bolsas=quantidade_bolsas`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nivel_minimo=nivel_minimo`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nivel_critico=nivel_critico`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status_calculado=status_calculado`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 182 — Expr** (nível 2 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.CADASTRO_ESTOQUE`, `usuario=hemocentro`, `alvo=estoque`, `descricao='Cadastro da estrutura de estoque de um tipo sanguineo.'`, `request=request`, `metadados={'tipo_sanguineo': tipo, 'quantidade_bolsas': quantidade_bolsas, 'nivel_minimo': nivel_minimo, 'nivel_critico': nivel_critico, 'status_calculado': status_calculado}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 197 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `estoque` ao chamador.

### registrar_movimentacao_estoque — linhas 200 a 324

```python
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

    motivo_limpo = (motivo or "").strip()
    if not motivo_limpo:
        raise ValidationError(
            {"motivo": "Informe o motivo da movimentacao de estoque."}
        )

    motivo_limpo = (motivo or "").strip()

    if not motivo_limpo:
        raise ValidationError(
            {
                "motivo": (
                    "Informe o motivo da movimentacao de estoque."
                )
            }
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
            motivo=motivo_limpo,
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
```

**Explicação deste trecho:**

**Linha 200 — FunctionDef** (nível 0 do bloco).

Define `registrar_movimentacao_estoque(*, estoque, usuario_resp, tipo_movimento, quantidade, motivo='', request=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 200:

**Linha 209 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 214 — Expr** (nível 1 do bloco).

Executa a chamada `validar_responsavel_pelo_estoque`; argumentos nomeados: `estoque=estoque`, `usuario=usuario_resp`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 216 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `tipo_movimento` não contido em `EstoqueMovimentacao.TipoMovimento.values`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 216:

**Linha 217 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'Tipo de movimentacao invalido.'`.

**Linha 219 — If** (nível 1 do bloco).

Escolhe um caminho verificando todas as condições: `tipo_movimento in (EstoqueMovimentacao.TipoMovimento.ENTRADA, EstoqueMovimentacao.TipoMovimento.SAIDA)` ; `quantidade <= 0` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 219:

**Linha 223 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `{'quantidade': 'Informe uma quantidade maior que zero.'}`.

**Linha 227 — If** (nível 1 do bloco).

Escolhe um caminho verificando todas as condições: `tipo_movimento == EstoqueMovimentacao.TipoMovimento.AJUSTE` ; `quantidade < 0` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 227:

**Linha 228 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `{'quantidade': 'A quantidade ajustada nao pode ser negativa.'}`.

**Linha 232 — Assign** (nível 1 do bloco).

Associa `motivo_limpo` a a chamada `(motivo or '').strip`, que remove espaços nas extremidades do texto.


**Linha 233 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `motivo_limpo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 233:

**Linha 234 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `{'motivo': 'Informe o motivo da movimentacao de estoque.'}`.

**Linha 238 — Assign** (nível 1 do bloco).

Associa `motivo_limpo` a a chamada `(motivo or '').strip`, que remove espaços nas extremidades do texto.


**Linha 240 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `motivo_limpo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 240:

**Linha 241 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `{'motivo': 'Informe o motivo da movimentacao de estoque.'}`.

**Linha 248 — With** (nível 1 do bloco).

Executa sob os contextos `transaction.atomic()`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 248:

**Linha 249 — Assign** (nível 2 do bloco).

Associa `estoque_atual` a a chamada `Estoque.objects.select_for_update().get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `pk=estoque.pk`.

- `pk=estoque.pk`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 251 — Assign** (nível 2 do bloco).

Associa `quantidade_anterior` a o atributo `quantidade_bolsas` de `estoque_atual`.

**Linha 253 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `tipo_movimento` igual a `EstoqueMovimentacao.TipoMovimento.ENTRADA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 253:

**Linha 254 — Assign** (nível 3 do bloco).

Associa `quantidade_movimentada` a o valor associado ao nome `quantidade`.

**Linha 255 — Assign** (nível 3 do bloco).

Associa `quantidade_nova` a a expressão `quantidade_anterior + quantidade`; seus operadores determinam o cálculo.

Bloco `orelse` da linha 253:

**Linha 257 — If** (nível 3 do bloco).

Escolhe um caminho verificando a comparação `tipo_movimento` igual a `EstoqueMovimentacao.TipoMovimento.SAIDA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 257:

**Linha 258 — If** (nível 4 do bloco).

Escolhe um caminho verificando a comparação `quantidade` maior que `quantidade_anterior`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 258:

**Linha 259 — Raise** (nível 5 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `{'quantidade': f'Nao ha bolsas suficientes para esta saida. Quantidade atual: {quantidade_anterior}.'}`.

**Linha 268 — Assign** (nível 4 do bloco).

Associa `quantidade_movimentada` a o valor associado ao nome `quantidade`.

**Linha 269 — Assign** (nível 4 do bloco).

Associa `quantidade_nova` a a expressão `quantidade_anterior - quantidade`; seus operadores determinam o cálculo.

Bloco `orelse` da linha 257:

**Linha 272 — Assign** (nível 4 do bloco).

Associa `quantidade_nova` a o valor associado ao nome `quantidade`.

**Linha 273 — Assign** (nível 4 do bloco).

Associa `quantidade_movimentada` a a expressão `quantidade_nova - quantidade_anterior`; seus operadores determinam o cálculo.

**Linha 275 — Assign** (nível 2 do bloco).

Associa `status_calculado` a a chamada `calcular_status_calculado`; argumentos nomeados: `quantidade_bolsas=quantidade_nova`, `nivel_minimo=estoque_atual.nivel_minimo`, `nivel_critico=estoque_atual.nivel_critico`.

- `quantidade_bolsas=quantidade_nova`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nivel_minimo=estoque_atual.nivel_minimo`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nivel_critico=estoque_atual.nivel_critico`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 281 — Assign** (nível 2 do bloco).

Associa `estoque_atual.quantidade_bolsas` a o valor associado ao nome `quantidade_nova`.

**Linha 282 — Assign** (nível 2 do bloco).

Associa `estoque_atual.status_calculado` a o valor associado ao nome `status_calculado`.

**Linha 283 — Expr** (nível 2 do bloco).

Executa a chamada `estoque_atual.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['quantidade_bolsas', 'status_calculado', 'data_atualizacao']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 291 — Assign** (nível 2 do bloco).

Associa `movimentacao` a a chamada `EstoqueMovimentacao.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `estoque=estoque_atual`, `usuario_resp=usuario_resp`, `tipo_movimento=tipo_movimento`, `quantidade_anterior=quantidade_anterior`, `quantidade_movimentada=quantidade_movimentada`, `quantidade_nova=quantidade_nova`, `motivo=motivo_limpo`.

- `estoque=estoque_atual`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `usuario_resp=usuario_resp`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_movimento=tipo_movimento`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `quantidade_anterior=quantidade_anterior`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `quantidade_movimentada=quantidade_movimentada`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `quantidade_nova=quantidade_nova`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `motivo=motivo_limpo`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 301 — Assign** (nível 2 do bloco).

Associa `notificacoes_geradas` a a chamada `criar_notificacoes_para_doadores_compativeis`; argumentos nomeados: `estoque=estoque_atual`, `status_calculado=status_calculado`.

- `estoque=estoque_atual`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status_calculado=status_calculado`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 306 — Expr** (nível 2 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.ATUALIZACAO_ESTOQUE`, `usuario=usuario_resp`, `alvo=estoque_atual`, `descricao='Movimentacao de bolsas no estoque.'`, `request=request`, `metadados={'id_mov': movimentacao.pk, 'tipo_movimento': tipo_movimento, 'quantidade_anterior': quantidade_anterior, 'quantidade_movimentada': quantidade_movimentada, 'quantidade_nova': quantidade_nova, 'status_calculado': status_calculado, 'notificacoes_geradas': notificacoes_geradas, 'motivo': movimentacao.motivo}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 324 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `movimentacao` ao chamador.

### calcular_status_publico — linhas 327 a 344

```python
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
```

**Explicação deste trecho:**

**Linha 327 — FunctionDef** (nível 0 do bloco).

Define `calcular_status_publico(quantidade_bolsas, nivel_minimo, nivel_critico)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 327:

**Linha 328 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 335 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `quantidade_bolsas` menor ou igual a `nivel_critico`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 335:

**Linha 336 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `'CRITICO'` ao chamador.

**Linha 338 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `quantidade_bolsas` menor ou igual a `nivel_minimo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 338:

**Linha 339 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `'BAIXO'` ao chamador.

**Linha 341 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `quantidade_bolsas` maior que `nivel_minimo * 2`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 341:

**Linha 342 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `'ALTO'` ao chamador.

**Linha 344 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor literal `'ADEQUADO'` ao chamador.

### Assign — linhas 347 a 352

```python
STATUS_PUBLICO_LABEL = {
    "CRITICO": "Crítico",
    "BAIXO": "Baixo",
    "ADEQUADO": "Adequado",
    "ALTO": "Alto",
}
```

**Explicação deste trecho:**

**Linha 347 — Assign** (nível 0 do bloco).

Associa `STATUS_PUBLICO_LABEL` a um dicionário de 4 entradas; as chaves dão nome aos valores associados.

- Chave `'CRITICO'`: recebe o valor literal `'Crítico'`.
- Chave `'BAIXO'`: recebe o valor literal `'Baixo'`.
- Chave `'ADEQUADO'`: recebe o valor literal `'Adequado'`.
- Chave `'ALTO'`: recebe o valor literal `'Alto'`.

### obter_estoques_publicos — linhas 355 a 402

```python
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
        status_codigo = calcular_status_publico(
            estoque.quantidade_bolsas,
            estoque.nivel_minimo,
            estoque.nivel_critico,
        )
        resultado.append(
            {
                "nome": estoque.hemocentro.nome,
                "cidade": estoque.hemocentro.cidade,
                "estado": estoque.hemocentro.estado,
                "tipo_sanguineo": estoque.tipo_sanguineo,
                "quantidade_bolsas": estoque.quantidade_bolsas,
                # ``status`` permanece como código para compatibilidade com
                # integrações; os campos abaixo facilitam a exibição e os
                # filtros sem expor níveis internos.
                "status": status_codigo,
                "status_codigo": status_codigo,
                "status_label": STATUS_PUBLICO_LABEL[status_codigo],
                "data_atualizacao": estoque.data_atualizacao,
            }
        )

    return resultado
```

**Explicação deste trecho:**

**Linha 355 — FunctionDef** (nível 0 do bloco).

Define `obter_estoques_publicos()`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 355:

**Linha 356 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 361 — Assign** (nível 1 do bloco).

Associa `estoques` a a chamada `Estoque.objects.select_related('hemocentro').filter(hemocentro__perfil=Usuario.Perfil.HEMOCENTRO, hemocentro__status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO).order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'hemocentro__cidade'`, `'hemocentro__nome'`, `'tipo_sanguineo'`.


**Linha 377 — Assign** (nível 1 do bloco).

Associa `resultado` a uma coleção List com 0 itens, na expressão `[]`.

**Linha 379 — For** (nível 1 do bloco).

Percorre `estoques`; cada item é atribuído a `estoque` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 379:

**Linha 380 — Assign** (nível 2 do bloco).

Associa `status_codigo` a a chamada `calcular_status_publico`; argumentos posicionais: `estoque.quantidade_bolsas`, `estoque.nivel_minimo`, `estoque.nivel_critico`.


**Linha 385 — Expr** (nível 2 do bloco).

Executa a chamada `resultado.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `{'nome': estoque.hemocentro.nome, 'cidade': estoque.hemocentro.cidade, 'estado': estoque.hemocentro.estado, 'tipo_sanguineo': estoque.tipo_sanguineo, 'quantidade_bolsas': estoque.quantidade_bolsas, 'status': status_codigo, 'status_codigo': status_codigo, 'status_label': STATUS_PUBLICO_LABEL[status_codigo], 'data_atualizacao': estoque.data_atualizacao}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 402 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `resultado` ao chamador.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 51: `# Serializa as convocacoes por doador antes de conferir o limite conjunto.`
- Linha 392: `# ``status`` permanece como código para compatibilidade com`
- Linha 393: `# integrações; os campos abaixo facilitam a exibição e os`
- Linha 394: `# filtros sem expor níveis internos.`

