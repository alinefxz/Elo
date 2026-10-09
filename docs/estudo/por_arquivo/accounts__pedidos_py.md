# accounts/pedidos.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Publicacao institucional e alertas de pedidos compativeis.

**Arquivo original:** [accounts/pedidos.py](<C:/Users/lb119/Elo/accounts/pedidos.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""Operações de publicação de pedidos de sangue."""

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.urls import reverse
from django.utils import timezone

from .compatibilidade import doadores_aptos_para_convocacao, limite_convocacao_atingido
from .models import AuditoriaAcaoCritica, Notificacao, PedidoSangue, Usuario
from .auditoria import registrar_auditoria


def pode_publicar_pedido(usuario):
    """Somente o Hemocentro aprovado pode publicar oficialmente."""

    return (
        usuario.is_authenticated
        and usuario.perfil == Usuario.Perfil.HEMOCENTRO
        and usuario.status_validacao
        == Usuario.StatusValidacaoHemocentro.APROVADO
    )


@transaction.atomic
def publicar_pedido(usuario, form, request=None):
    """Publica um pedido já analisado pelo próprio Hemocentro."""

    if not pode_publicar_pedido(usuario):
        raise PermissionDenied(
            "Este perfil não pode publicar pedidos de sangue."
        )

    pedido = form.save(commit=False)
    if pedido.hemocentro_destino_id != usuario.pk:
        raise PermissionDenied("O pedido pertence a outro Hemocentro.")
    pedido.publicado_por = usuario
    pedido.publicado_em = timezone.now()
    pedido.status = PedidoSangue.Status.PUBLICADA
    pedido.cidade = pedido.hemocentro_destino.cidade
    pedido.full_clean()
    pedido.save()
    criar_notificacoes_para_pedido(pedido=pedido)
    registrar_auditoria(
        acao=AuditoriaAcaoCritica.Acao.MODERACAO, usuario=usuario, alvo=pedido, request=request,
        descricao="Publicacao institucional de pedido de sangue.",
        metadados={"evento": "PUBLICACAO_PEDIDO", "status_pedido": pedido.status},
    )
    return pedido


@transaction.atomic
def criar_notificacoes_para_pedido(*, pedido):
    """Notifica apenas doadores compatíveis e aptos para o pedido publicado."""

    if pedido.status != PedidoSangue.Status.PUBLICADA or not pode_publicar_pedido(pedido.hemocentro_destino):
        return 0
    doadores = doadores_aptos_para_convocacao(pedido.tipo_sanguineo).select_for_update()

    notificacoes = []
    for doador in doadores:
        if limite_convocacao_atingido(doador):
            continue
        if Notificacao.objects.filter(usuario=doador, pedido=pedido).exists():
            continue
        notificacoes.append(
            Notificacao(
                usuario=doador,
                pedido=pedido,
                tipo=Notificacao.Tipo.PEDIDO_COMPATIVEL,
                titulo=f"Pedido compatível: {pedido.tipo_sanguineo}",
                mensagem=(
                    f"Há uma necessidade publicada pelo Hemocentro "
                    f"{pedido.hemocentro_destino.nome} em {pedido.cidade}."
                ),
                url_destino=reverse("accounts:consultar_pedidos"),
            )
        )

    Notificacao.objects.bulk_create(notificacoes)
    return len(notificacoes)
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 1

```python
"""Operações de publicação de pedidos de sangue."""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 3 a 3

```python
from django.core.exceptions import PermissionDenied
```

**Explicação deste trecho:**

**Linha 3 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.exceptions` os nomes `PermissionDenied`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 4 a 4

```python
from django.db import transaction
```

**Explicação deste trecho:**

**Linha 4 — ImportFrom** (nível 0 do bloco).

Importa de `django.db` os nomes `transaction`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 5 a 5

```python
from django.urls import reverse
```

**Explicação deste trecho:**

**Linha 5 — ImportFrom** (nível 0 do bloco).

Importa de `django.urls` os nomes `reverse`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 6 a 6

```python
from django.utils import timezone
```

**Explicação deste trecho:**

**Linha 6 — ImportFrom** (nível 0 do bloco).

Importa de `django.utils` os nomes `timezone`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 8 a 8

```python
from .compatibilidade import doadores_aptos_para_convocacao, limite_convocacao_atingido
```

**Explicação deste trecho:**

**Linha 8 — ImportFrom** (nível 0 do bloco).

Importa de `.compatibilidade` os nomes `doadores_aptos_para_convocacao`, `limite_convocacao_atingido`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 9 a 9

```python
from .models import AuditoriaAcaoCritica, Notificacao, PedidoSangue, Usuario
```

**Explicação deste trecho:**

**Linha 9 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `AuditoriaAcaoCritica`, `Notificacao`, `PedidoSangue`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 10 a 10

```python
from .auditoria import registrar_auditoria
```

**Explicação deste trecho:**

**Linha 10 — ImportFrom** (nível 0 do bloco).

Importa de `.auditoria` os nomes `registrar_auditoria`. Pontos iniciais indicam importação relativa ao pacote.

### pode_publicar_pedido — linhas 13 a 21

```python
def pode_publicar_pedido(usuario):
    """Somente o Hemocentro aprovado pode publicar oficialmente."""

    return (
        usuario.is_authenticated
        and usuario.perfil == Usuario.Perfil.HEMOCENTRO
        and usuario.status_validacao
        == Usuario.StatusValidacaoHemocentro.APROVADO
    )
```

**Explicação deste trecho:**

**Linha 13 — FunctionDef** (nível 0 do bloco).

Define `pode_publicar_pedido(usuario)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 13:

**Linha 14 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 16 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve todas as condições: `usuario.is_authenticated` ; `usuario.perfil == Usuario.Perfil.HEMOCENTRO` ; `usuario.status_validacao == Usuario.StatusValidacaoHemocentro.APROVADO` (com avaliação interrompida assim que o resultado é determinado) ao chamador.

### publicar_pedido — linhas 24 a 48

```python
@transaction.atomic
def publicar_pedido(usuario, form, request=None):
    """Publica um pedido já analisado pelo próprio Hemocentro."""

    if not pode_publicar_pedido(usuario):
        raise PermissionDenied(
            "Este perfil não pode publicar pedidos de sangue."
        )

    pedido = form.save(commit=False)
    if pedido.hemocentro_destino_id != usuario.pk:
        raise PermissionDenied("O pedido pertence a outro Hemocentro.")
    pedido.publicado_por = usuario
    pedido.publicado_em = timezone.now()
    pedido.status = PedidoSangue.Status.PUBLICADA
    pedido.cidade = pedido.hemocentro_destino.cidade
    pedido.full_clean()
    pedido.save()
    criar_notificacoes_para_pedido(pedido=pedido)
    registrar_auditoria(
        acao=AuditoriaAcaoCritica.Acao.MODERACAO, usuario=usuario, alvo=pedido, request=request,
        descricao="Publicacao institucional de pedido de sangue.",
        metadados={"evento": "PUBLICACAO_PEDIDO", "status_pedido": pedido.status},
    )
    return pedido
```

**Explicação deste trecho:**

**Linha 25 — FunctionDef** (nível 0 do bloco).

Define `publicar_pedido(usuario, form, request=None)`. O corpo só executa quando a função/método é chamado. Decoradores: `transaction.atomic`.

Bloco `body` da linha 25:

**Linha 26 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 28 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `pode_publicar_pedido(usuario)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 28:

**Linha 29 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'Este perfil não pode publicar pedidos de sangue.'`.

**Linha 33 — Assign** (nível 1 do bloco).

Associa `pedido` a a chamada `form.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `commit=False`.

- `commit=False`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 34 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `pedido.hemocentro_destino_id` diferente de `usuario.pk`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 34:

**Linha 35 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'O pedido pertence a outro Hemocentro.'`.

**Linha 36 — Assign** (nível 1 do bloco).

Associa `pedido.publicado_por` a o valor associado ao nome `usuario`.

**Linha 37 — Assign** (nível 1 do bloco).

Associa `pedido.publicado_em` a a chamada `timezone.now`, que obtém o instante atual; timezone.now respeita o tratamento de fuso do Django.


**Linha 38 — Assign** (nível 1 do bloco).

Associa `pedido.status` a o atributo `PUBLICADA` de `PedidoSangue.Status`.

**Linha 39 — Assign** (nível 1 do bloco).

Associa `pedido.cidade` a o atributo `cidade` de `pedido.hemocentro_destino`.

**Linha 40 — Expr** (nível 1 do bloco).

Executa a chamada `pedido.full_clean`, que executa validação explícita de campos, regras do model e integridade pertinente. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 41 — Expr** (nível 1 do bloco).

Executa a chamada `pedido.save`, que persiste a instância; update_fields limita os campos gravados. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 42 — Expr** (nível 1 do bloco).

Executa a chamada `criar_notificacoes_para_pedido`; argumentos nomeados: `pedido=pedido`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 43 — Expr** (nível 1 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.MODERACAO`, `usuario=usuario`, `alvo=pedido`, `request=request`, `descricao='Publicacao institucional de pedido de sangue.'`, `metadados={'evento': 'PUBLICACAO_PEDIDO', 'status_pedido': pedido.status}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 48 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `pedido` ao chamador.

### criar_notificacoes_para_pedido — linhas 51 a 80

```python
@transaction.atomic
def criar_notificacoes_para_pedido(*, pedido):
    """Notifica apenas doadores compatíveis e aptos para o pedido publicado."""

    if pedido.status != PedidoSangue.Status.PUBLICADA or not pode_publicar_pedido(pedido.hemocentro_destino):
        return 0
    doadores = doadores_aptos_para_convocacao(pedido.tipo_sanguineo).select_for_update()

    notificacoes = []
    for doador in doadores:
        if limite_convocacao_atingido(doador):
            continue
        if Notificacao.objects.filter(usuario=doador, pedido=pedido).exists():
            continue
        notificacoes.append(
            Notificacao(
                usuario=doador,
                pedido=pedido,
                tipo=Notificacao.Tipo.PEDIDO_COMPATIVEL,
                titulo=f"Pedido compatível: {pedido.tipo_sanguineo}",
                mensagem=(
                    f"Há uma necessidade publicada pelo Hemocentro "
                    f"{pedido.hemocentro_destino.nome} em {pedido.cidade}."
                ),
                url_destino=reverse("accounts:consultar_pedidos"),
            )
        )

    Notificacao.objects.bulk_create(notificacoes)
    return len(notificacoes)
```

**Explicação deste trecho:**

**Linha 52 — FunctionDef** (nível 0 do bloco).

Define `criar_notificacoes_para_pedido(*, pedido)`. O corpo só executa quando a função/método é chamado. Decoradores: `transaction.atomic`.

Bloco `body` da linha 52:

**Linha 53 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 55 — If** (nível 1 do bloco).

Escolhe um caminho verificando pelo menos uma das condições: `pedido.status != PedidoSangue.Status.PUBLICADA` ; `not pode_publicar_pedido(pedido.hemocentro_destino)` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 55:

**Linha 56 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `0` ao chamador.

**Linha 57 — Assign** (nível 1 do bloco).

Associa `doadores` a a chamada `doadores_aptos_para_convocacao(pedido.tipo_sanguineo).select_for_update`, que solicita bloqueio dos registros no banco durante a transação.


**Linha 59 — Assign** (nível 1 do bloco).

Associa `notificacoes` a uma coleção List com 0 itens, na expressão `[]`.

**Linha 60 — For** (nível 1 do bloco).

Percorre `doadores`; cada item é atribuído a `doador` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 60:

**Linha 61 — If** (nível 2 do bloco).

Escolhe um caminho verificando a chamada `limite_convocacao_atingido`; argumentos posicionais: `doador`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 61:

**Linha 62 — Continue** (nível 3 do bloco).

Pula o restante da iteração atual e segue para o próximo item do laço.

**Linha 63 — If** (nível 2 do bloco).

Escolhe um caminho verificando a chamada `Notificacao.objects.filter(usuario=doador, pedido=pedido).exists`, que verifica se há pelo menos um resultado. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 63:

**Linha 64 — Continue** (nível 3 do bloco).

Pula o restante da iteração atual e segue para o próximo item do laço.

**Linha 65 — Expr** (nível 2 do bloco).

Executa a chamada `notificacoes.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `Notificacao(usuario=doador, pedido=pedido, tipo=Notificacao.Tipo.PEDIDO_COMPATIVEL, titulo=f'Pedido compatível: {pedido.tipo_sanguineo}', mensagem=f'Há uma necessidade publicada pelo Hemocentro {pedido.hemocentro_destino.nome} em {pedido.cidade}.', url_destino=reverse('accounts:consultar_pedidos'))`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 79 — Expr** (nível 1 do bloco).

Executa a chamada `Notificacao.objects.bulk_create`, que grava uma coleção em lote, sem executar save de cada instância; argumentos posicionais: `notificacoes`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 80 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `len`; argumentos posicionais: `notificacoes` ao chamador.

