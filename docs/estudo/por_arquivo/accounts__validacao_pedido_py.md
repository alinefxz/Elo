# accounts/validacao_pedido.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Solicitacao, decisao, historico e autorizacao de pedidos.

**Arquivo original:** [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
# Este módulo controla a criação e a validação dos pedidos de sangue.

# 1. validar_dados_pedido()
#    Confere título, tipo sanguíneo, urgência, cidade, descrição, solicitante, e-mail de contato e Hemocentro de destino aprovado.

# 2. criar_pedido_pendente()
#    Cria o pedido com status ENVIADA.
#    Administradores e Hemocentros não criam solicitações comuns.
#    O pedido não é publicado automaticamente.
#    Também verifica pedidos semelhantes nos últimos 7 dias e marca possíveis duplicidades apenas como alerta.

# 3. registrar_decisao_validacao_pedido()
#    Registra a decisão sobre o pedido dentro de uma transação segura.
#    Pedidos encerrados não podem ser alterados.
#    O Hemocentro aprovado de destino pode:
#    - aprovar e publicar;
#    - recusar;
#    - solicitar correção;
#    - marcar como suspeito.
#    O Administrador pode apenas marcar o pedido como suspeito para moderação e auditoria.

# 4. Quando o pedido é aprovado:
#    - seu status muda para PUBLICADA;
#    - o Hemocentro responsável e a data são registrados;
#    - notificações compatíveis são criadas;
#    - a decisão é salva no histórico;
#    - a ação é registrada na auditoria.

# 5. Funções auxiliares
#    aprovar_pedido(), recusar_pedido(), solicitar_correcao_pedido() e
#    marcar_pedido_suspeito() apenas chamam a função principal informando o
#    status correspondente.

# O formulário valida os dados na interface, este arquivo repete as validações importantes no servidor e o modelo protege a integridade final do banco.

from django.core.exceptions import PermissionDenied, ValidationError
from django.core.validators import validate_email
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .auditoria import registrar_auditoria
from .models import (
    AuditoriaAcaoCritica,
    PedidoSangue,
    Usuario,
    ValidacaoPedido,
)
from .validacao_hemocentro import hemocentro_aprovado, usuario_e_administrador


def validar_dados_pedido(pedido):
    """
    Valida as informações básicas antes da decisão administrativa.
    """

    if not pedido.titulo.strip():
        raise ValidationError(
            "O pedido precisa possuir um título."
        )

    if not pedido.tipo_sanguineo:
        raise ValidationError(
            "Informe o tipo sanguíneo."
        )

    if not pedido.urgencia:
        raise ValidationError(
            "Informe a urgência."
        )

    if not pedido.cidade.strip():
        raise ValidationError(
            "Informe a cidade."
        )

    if not pedido.descricao.strip():
        raise ValidationError(
            "Informe a descrição do pedido."
        )

    if not pedido.nome_solicitante.strip():
        raise ValidationError("Informe o nome ou identificação do solicitante.")

    if not pedido.contato.strip():
        raise ValidationError("Informe um e-mail para retorno.")

    try:
        validate_email(pedido.contato.strip())
    except ValidationError as erro:
        raise ValidationError("Informe um e-mail válido para retorno.") from erro

    if not pedido.hemocentro_destino_id:
        raise ValidationError(
            "Informe o Hemocentro de destino."
        )

    if (
        pedido.hemocentro_destino.perfil
        != Usuario.Perfil.HEMOCENTRO
    ):
        raise ValidationError(
            "O destino precisa ser um Hemocentro."
        )

    if (
        pedido.hemocentro_destino.status_validacao
        != Usuario.StatusValidacaoHemocentro.APROVADO
    ):
        raise ValidationError(
            "O Hemocentro de destino precisa estar aprovado."
        )


def criar_pedido_pendente(
    *,
    dados,
    solicitante,
):
    """
    Cria o pedido sem publicá-lo.
    """

    if not getattr(solicitante, "is_authenticated", False) or solicitante.perfil != Usuario.Perfil.RECEPTOR:
        raise PermissionDenied("Somente Receptor pode enviar solicitacao de pedido de sangue.")

    dados = dict(dados)
    hemocentro_destino = dados.get("hemocentro_destino")
    if hemocentro_destino and not hasattr(hemocentro_destino, "pk"):
        try:
            dados["hemocentro_destino"] = Usuario.objects.get(
                pk=hemocentro_destino,
                perfil=Usuario.Perfil.HEMOCENTRO,
            )
        except Usuario.DoesNotExist as erro:
            raise ValidationError("Hemocentro de destino inválido.") from erro

    pedido = PedidoSangue(
        solicitante=solicitante,
        status=PedidoSangue.Status.ENVIADA,
        **dados,
    )

    validar_dados_pedido(pedido)
    pedido.full_clean()

    pedido.save()

    # Semelhança é apenas um alerta para o Hemocentro; nunca bloqueia uma
    # necessidade legítima automaticamente.
    limite = timezone.now() - timedelta(days=7)
    duplicado = PedidoSangue.objects.filter(
        hemocentro_destino=pedido.hemocentro_destino,
        tipo_sanguineo=pedido.tipo_sanguineo,
        cidade__iexact=pedido.cidade,
        data_criacao__gte=limite,
    ).exclude(pk=pedido.pk).filter(
        status__in=[
            PedidoSangue.Status.ENVIADA,
            PedidoSangue.Status.EM_ANALISE,
            PedidoSangue.Status.PUBLICADA,
            PedidoSangue.Status.CORRECAO_SOLICITADA,
        ]
    ).exists()
    if duplicado:
        pedido.duplicidade_suspeita = True
        pedido.save(update_fields=["duplicidade_suspeita", "atualizado_em"])

    return pedido


@transaction.atomic
def registrar_decisao_validacao_pedido(
    *,
    pedido,
    moderador,
    status_validacao,
    motivo="",
    request=None,
):
    """
    Registra a decisão administrativa e atualiza
    o status do pedido.
    """

    motivo = (motivo or "").strip()

    if status_validacao not in [
        ValidacaoPedido.StatusValidacao.APROVADO,
        ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA,
        ValidacaoPedido.StatusValidacao.RECUSADO,
        ValidacaoPedido.StatusValidacao.SUSPEITO,
    ]:
        raise ValidationError(
            "Status de validação inválido."
        )

    # A publicação, a recusa e a solicitação de correção pertencem somente
    # ao Hemocentro aprovado de destino. O Administrador apenas pode
    # registrar uma suspeita para fins de moderação/auditoria.
    administrador = usuario_e_administrador(moderador)
    hemocentro_do_destino = (
        hemocentro_aprovado(moderador)
        and pedido.hemocentro_destino_id == moderador.pk
    )

    if status_validacao == ValidacaoPedido.StatusValidacao.SUSPEITO:
        if not administrador and not hemocentro_do_destino:
            raise PermissionDenied(
                "Somente o administrador ou o Hemocentro aprovado de destino "
                "pode marcar um pedido como suspeito."
            )
    elif not hemocentro_do_destino:
        raise PermissionDenied(
            "Somente o Hemocentro aprovado de destino pode analisar e publicar "
            "pedidos."
        )

    # Não use select_related junto com select_for_update aqui. Como
    # solicitante é uma FK anulável, o Django gera LEFT OUTER JOIN e o
    # PostgreSQL não permite aplicar FOR UPDATE ao lado opcional da junção.
    # O bloqueio deve atingir somente a linha do pedido; as relações são
    # carregadas sob demanda quando as notificações forem criadas.
    pedido = PedidoSangue.objects.select_for_update().get(pk=pedido.pk)

    status_anterior = pedido.status
    institucional = hemocentro_do_destino

    if pedido.status == PedidoSangue.Status.ENCERRADA:
        raise ValidationError("Não é possível validar um pedido encerrado.")

    if status_validacao == (
        ValidacaoPedido.StatusValidacao.APROVADO
    ):
        validar_dados_pedido(pedido)
        novo_status = PedidoSangue.Status.PUBLICADA

        if not motivo:
            motivo = (
                "Pedido aprovado pelo Hemocentro de destino."
            )

    elif status_validacao == (
        ValidacaoPedido.StatusValidacao.RECUSADO
    ):
        novo_status = PedidoSangue.Status.RECUSADA

        if not motivo:
            motivo = (
                "Pedido recusado pelo Hemocentro de destino."
            )

    elif status_validacao == ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA:
        novo_status = PedidoSangue.Status.CORRECAO_SOLICITADA

        if not motivo:
            motivo = "O Hemocentro solicitou correção das informações."

    else:
        novo_status = PedidoSangue.Status.EM_ANALISE

        if not motivo:
            motivo = (
                "Pedido marcado como suspeito "
                "e mantido em análise."
            )

    pedido.status = novo_status

    if novo_status == PedidoSangue.Status.PUBLICADA:
        pedido.publicado_por = moderador
        pedido.publicado_em = timezone.now()

    pedido.save(
        update_fields=[
            "status",
            "atualizado_em",
            "publicado_por",
            "publicado_em",
        ]
    )

    notificacoes_geradas = 0
    if novo_status == PedidoSangue.Status.PUBLICADA:
        from .pedidos import criar_notificacoes_para_pedido

        notificacoes_geradas = criar_notificacoes_para_pedido(pedido=pedido)

    validacao = ValidacaoPedido.objects.create(
        pedido=pedido,
        status_validacao=status_validacao,
        motivo=motivo,
        moderador=moderador,
    )

    registrar_auditoria(
        acao=AuditoriaAcaoCritica.Acao.MODERACAO,
        resultado=AuditoriaAcaoCritica.Resultado.SUCESSO,
        usuario=moderador,
        alvo=pedido,
        descricao=(
            "Decisao institucional sobre pedido de sangue." if institucional
            else "Validacao administrativa de pedido de sangue."
        ),
        request=request,
        metadados={
            "evento": "PUBLICACAO_PEDIDO" if institucional and status_validacao == ValidacaoPedido.StatusValidacao.APROVADO else "VALIDACAO_PEDIDO",
            "status_anterior": status_anterior,
            "perfil_responsavel": moderador.perfil,
            "id_pedido": pedido.pk,
            "id_validacao": validacao.pk,
            "status_validacao": status_validacao,
            "status_pedido": novo_status,
            "motivo": motivo,
            "notificacoes_geradas": notificacoes_geradas,
        },
    )

    return validacao


def aprovar_pedido(
    *,
    pedido,
    moderador,
    motivo="",
    request=None,
):
    return registrar_decisao_validacao_pedido(
        pedido=pedido,
        moderador=moderador,
        status_validacao=(
            ValidacaoPedido.StatusValidacao.APROVADO
        ),
        motivo=motivo,
        request=request,
    )


def recusar_pedido(
    *,
    pedido,
    moderador,
    motivo="",
    request=None,
):
    return registrar_decisao_validacao_pedido(
        pedido=pedido,
        moderador=moderador,
        status_validacao=(
            ValidacaoPedido.StatusValidacao.RECUSADO
        ),
        motivo=motivo,
        request=request,
    )


def solicitar_correcao_pedido(
    *,
    pedido,
    moderador,
    motivo="",
    request=None,
):
    return registrar_decisao_validacao_pedido(
        pedido=pedido,
        moderador=moderador,
        status_validacao=(
            ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA
        ),
        motivo=motivo,
        request=request,
    )


def marcar_pedido_suspeito(
    *,
    pedido,
    moderador,
    motivo="",
    request=None,
):
    return registrar_decisao_validacao_pedido(
        pedido=pedido,
        moderador=moderador,
        status_validacao=(
            ValidacaoPedido.StatusValidacao.SUSPEITO
        ),
        motivo=motivo,
        request=request,
    )
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### ImportFrom — linhas 36 a 36

```python
from django.core.exceptions import PermissionDenied, ValidationError
```

**Explicação deste trecho:**

**Linha 36 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.exceptions` os nomes `PermissionDenied`, `ValidationError`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 37 a 37

```python
from django.core.validators import validate_email
```

**Explicação deste trecho:**

**Linha 37 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.validators` os nomes `validate_email`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 38 a 38

```python
from datetime import timedelta
```

**Explicação deste trecho:**

**Linha 38 — ImportFrom** (nível 0 do bloco).

Importa de `datetime` os nomes `timedelta`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 40 a 40

```python
from django.db import transaction
```

**Explicação deste trecho:**

**Linha 40 — ImportFrom** (nível 0 do bloco).

Importa de `django.db` os nomes `transaction`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 41 a 41

```python
from django.utils import timezone
```

**Explicação deste trecho:**

**Linha 41 — ImportFrom** (nível 0 do bloco).

Importa de `django.utils` os nomes `timezone`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 43 a 43

```python
from .auditoria import registrar_auditoria
```

**Explicação deste trecho:**

**Linha 43 — ImportFrom** (nível 0 do bloco).

Importa de `.auditoria` os nomes `registrar_auditoria`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 44 a 49

```python
from .models import (
    AuditoriaAcaoCritica,
    PedidoSangue,
    Usuario,
    ValidacaoPedido,
)
```

**Explicação deste trecho:**

**Linha 44 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `AuditoriaAcaoCritica`, `PedidoSangue`, `Usuario`, `ValidacaoPedido`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 50 a 50

```python
from .validacao_hemocentro import hemocentro_aprovado, usuario_e_administrador
```

**Explicação deste trecho:**

**Linha 50 — ImportFrom** (nível 0 do bloco).

Importa de `.validacao_hemocentro` os nomes `hemocentro_aprovado`, `usuario_e_administrador`. Pontos iniciais indicam importação relativa ao pacote.

### validar_dados_pedido — linhas 53 a 113

```python
def validar_dados_pedido(pedido):
    """
    Valida as informações básicas antes da decisão administrativa.
    """

    if not pedido.titulo.strip():
        raise ValidationError(
            "O pedido precisa possuir um título."
        )

    if not pedido.tipo_sanguineo:
        raise ValidationError(
            "Informe o tipo sanguíneo."
        )

    if not pedido.urgencia:
        raise ValidationError(
            "Informe a urgência."
        )

    if not pedido.cidade.strip():
        raise ValidationError(
            "Informe a cidade."
        )

    if not pedido.descricao.strip():
        raise ValidationError(
            "Informe a descrição do pedido."
        )

    if not pedido.nome_solicitante.strip():
        raise ValidationError("Informe o nome ou identificação do solicitante.")

    if not pedido.contato.strip():
        raise ValidationError("Informe um e-mail para retorno.")

    try:
        validate_email(pedido.contato.strip())
    except ValidationError as erro:
        raise ValidationError("Informe um e-mail válido para retorno.") from erro

    if not pedido.hemocentro_destino_id:
        raise ValidationError(
            "Informe o Hemocentro de destino."
        )

    if (
        pedido.hemocentro_destino.perfil
        != Usuario.Perfil.HEMOCENTRO
    ):
        raise ValidationError(
            "O destino precisa ser um Hemocentro."
        )

    if (
        pedido.hemocentro_destino.status_validacao
        != Usuario.StatusValidacaoHemocentro.APROVADO
    ):
        raise ValidationError(
            "O Hemocentro de destino precisa estar aprovado."
        )
```

**Explicação deste trecho:**

**Linha 53 — FunctionDef** (nível 0 do bloco).

Define `validar_dados_pedido(pedido)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 53:

**Linha 54 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 58 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `pedido.titulo.strip()`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 58:

**Linha 59 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'O pedido precisa possuir um título.'`.

**Linha 63 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `pedido.tipo_sanguineo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 63:

**Linha 64 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'Informe o tipo sanguíneo.'`.

**Linha 68 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `pedido.urgencia`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 68:

**Linha 69 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'Informe a urgência.'`.

**Linha 73 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `pedido.cidade.strip()`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 73:

**Linha 74 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'Informe a cidade.'`.

**Linha 78 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `pedido.descricao.strip()`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 78:

**Linha 79 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'Informe a descrição do pedido.'`.

**Linha 83 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `pedido.nome_solicitante.strip()`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 83:

**Linha 84 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'Informe o nome ou identificação do solicitante.'`.

**Linha 86 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `pedido.contato.strip()`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 86:

**Linha 87 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'Informe um e-mail para retorno.'`.

**Linha 89 — Try** (nível 1 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 89:

**Linha 90 — Expr** (nível 2 do bloco).

Executa a chamada `validate_email`; argumentos posicionais: `pedido.contato.strip()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Erro tratado: `ValidationError` sob o nome `erro`.

**Linha 92 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'Informe um e-mail válido para retorno.'`.

**Linha 94 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `pedido.hemocentro_destino_id`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 94:

**Linha 95 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'Informe o Hemocentro de destino.'`.

**Linha 99 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `pedido.hemocentro_destino.perfil` diferente de `Usuario.Perfil.HEMOCENTRO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 99:

**Linha 103 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'O destino precisa ser um Hemocentro.'`.

**Linha 107 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `pedido.hemocentro_destino.status_validacao` diferente de `Usuario.StatusValidacaoHemocentro.APROVADO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 107:

**Linha 111 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'O Hemocentro de destino precisa estar aprovado.'`.

### criar_pedido_pendente — linhas 116 a 170

```python
def criar_pedido_pendente(
    *,
    dados,
    solicitante,
):
    """
    Cria o pedido sem publicá-lo.
    """

    if not getattr(solicitante, "is_authenticated", False) or solicitante.perfil != Usuario.Perfil.RECEPTOR:
        raise PermissionDenied("Somente Receptor pode enviar solicitacao de pedido de sangue.")

    dados = dict(dados)
    hemocentro_destino = dados.get("hemocentro_destino")
    if hemocentro_destino and not hasattr(hemocentro_destino, "pk"):
        try:
            dados["hemocentro_destino"] = Usuario.objects.get(
                pk=hemocentro_destino,
                perfil=Usuario.Perfil.HEMOCENTRO,
            )
        except Usuario.DoesNotExist as erro:
            raise ValidationError("Hemocentro de destino inválido.") from erro

    pedido = PedidoSangue(
        solicitante=solicitante,
        status=PedidoSangue.Status.ENVIADA,
        **dados,
    )

    validar_dados_pedido(pedido)
    pedido.full_clean()

    pedido.save()

    # Semelhança é apenas um alerta para o Hemocentro; nunca bloqueia uma
    # necessidade legítima automaticamente.
    limite = timezone.now() - timedelta(days=7)
    duplicado = PedidoSangue.objects.filter(
        hemocentro_destino=pedido.hemocentro_destino,
        tipo_sanguineo=pedido.tipo_sanguineo,
        cidade__iexact=pedido.cidade,
        data_criacao__gte=limite,
    ).exclude(pk=pedido.pk).filter(
        status__in=[
            PedidoSangue.Status.ENVIADA,
            PedidoSangue.Status.EM_ANALISE,
            PedidoSangue.Status.PUBLICADA,
            PedidoSangue.Status.CORRECAO_SOLICITADA,
        ]
    ).exists()
    if duplicado:
        pedido.duplicidade_suspeita = True
        pedido.save(update_fields=["duplicidade_suspeita", "atualizado_em"])

    return pedido
```

**Explicação deste trecho:**

**Linha 116 — FunctionDef** (nível 0 do bloco).

Define `criar_pedido_pendente(*, dados, solicitante)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 116:

**Linha 121 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 125 — If** (nível 1 do bloco).

Escolhe um caminho verificando pelo menos uma das condições: `not getattr(solicitante, 'is_authenticated', False)` ; `solicitante.perfil != Usuario.Perfil.RECEPTOR` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 125:

**Linha 126 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'Somente Receptor pode enviar solicitacao de pedido de sangue.'`.

**Linha 128 — Assign** (nível 1 do bloco).

Associa `dados` a a chamada `dict`; argumentos posicionais: `dados`.


**Linha 129 — Assign** (nível 1 do bloco).

Associa `hemocentro_destino` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'hemocentro_destino'`.


**Linha 130 — If** (nível 1 do bloco).

Escolhe um caminho verificando todas as condições: `hemocentro_destino` ; `not hasattr(hemocentro_destino, 'pk')` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 130:

**Linha 131 — Try** (nível 2 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 131:

**Linha 132 — Assign** (nível 3 do bloco).

Associa `dados['hemocentro_destino']` a a chamada `Usuario.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `pk=hemocentro_destino`, `perfil=Usuario.Perfil.HEMOCENTRO`.

- `pk=hemocentro_destino`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.HEMOCENTRO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

Erro tratado: `Usuario.DoesNotExist` sob o nome `erro`.

**Linha 137 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'Hemocentro de destino inválido.'`.

**Linha 139 — Assign** (nível 1 do bloco).

Associa `pedido` a a chamada `PedidoSangue`; argumentos nomeados: `solicitante=solicitante`, `status=PedidoSangue.Status.ENVIADA`, `**=dados`.

- `solicitante=solicitante`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status=PedidoSangue.Status.ENVIADA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `**=dados`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 145 — Expr** (nível 1 do bloco).

Executa a chamada `validar_dados_pedido`; argumentos posicionais: `pedido`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 146 — Expr** (nível 1 do bloco).

Executa a chamada `pedido.full_clean`, que executa validação explícita de campos, regras do model e integridade pertinente. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 148 — Expr** (nível 1 do bloco).

Executa a chamada `pedido.save`, que persiste a instância; update_fields limita os campos gravados. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 152 — Assign** (nível 1 do bloco).

Associa `limite` a a expressão `timezone.now() - timedelta(days=7)`; seus operadores determinam o cálculo.

**Linha 153 — Assign** (nível 1 do bloco).

Associa `duplicado` a a chamada `PedidoSangue.objects.filter(hemocentro_destino=pedido.hemocentro_destino, tipo_sanguineo=pedido.tipo_sanguineo, cidade__iexact=pedido.cidade, data_criacao__gte=limite).exclude(pk=pedido.pk).filter(status__in=[PedidoSangue.Status.ENVIADA, PedidoSangue.Status.EM_ANALISE, PedidoSangue.Status.PUBLICADA, PedidoSangue.Status.CORRECAO_SOLICITADA]).exists`, que verifica se há pelo menos um resultado.


**Linha 166 — If** (nível 1 do bloco).

Escolhe um caminho verificando o valor associado ao nome `duplicado`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 166:

**Linha 167 — Assign** (nível 2 do bloco).

Associa `pedido.duplicidade_suspeita` a o valor literal `True`.

**Linha 168 — Expr** (nível 2 do bloco).

Executa a chamada `pedido.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['duplicidade_suspeita', 'atualizado_em']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 170 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `pedido` ao chamador.

### registrar_decisao_validacao_pedido — linhas 173 a 320

```python
@transaction.atomic
def registrar_decisao_validacao_pedido(
    *,
    pedido,
    moderador,
    status_validacao,
    motivo="",
    request=None,
):
    """
    Registra a decisão administrativa e atualiza
    o status do pedido.
    """

    motivo = (motivo or "").strip()

    if status_validacao not in [
        ValidacaoPedido.StatusValidacao.APROVADO,
        ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA,
        ValidacaoPedido.StatusValidacao.RECUSADO,
        ValidacaoPedido.StatusValidacao.SUSPEITO,
    ]:
        raise ValidationError(
            "Status de validação inválido."
        )

    # A publicação, a recusa e a solicitação de correção pertencem somente
    # ao Hemocentro aprovado de destino. O Administrador apenas pode
    # registrar uma suspeita para fins de moderação/auditoria.
    administrador = usuario_e_administrador(moderador)
    hemocentro_do_destino = (
        hemocentro_aprovado(moderador)
        and pedido.hemocentro_destino_id == moderador.pk
    )

    if status_validacao == ValidacaoPedido.StatusValidacao.SUSPEITO:
        if not administrador and not hemocentro_do_destino:
            raise PermissionDenied(
                "Somente o administrador ou o Hemocentro aprovado de destino "
                "pode marcar um pedido como suspeito."
            )
    elif not hemocentro_do_destino:
        raise PermissionDenied(
            "Somente o Hemocentro aprovado de destino pode analisar e publicar "
            "pedidos."
        )

    # Não use select_related junto com select_for_update aqui. Como
    # solicitante é uma FK anulável, o Django gera LEFT OUTER JOIN e o
    # PostgreSQL não permite aplicar FOR UPDATE ao lado opcional da junção.
    # O bloqueio deve atingir somente a linha do pedido; as relações são
    # carregadas sob demanda quando as notificações forem criadas.
    pedido = PedidoSangue.objects.select_for_update().get(pk=pedido.pk)

    status_anterior = pedido.status
    institucional = hemocentro_do_destino

    if pedido.status == PedidoSangue.Status.ENCERRADA:
        raise ValidationError("Não é possível validar um pedido encerrado.")

    if status_validacao == (
        ValidacaoPedido.StatusValidacao.APROVADO
    ):
        validar_dados_pedido(pedido)
        novo_status = PedidoSangue.Status.PUBLICADA

        if not motivo:
            motivo = (
                "Pedido aprovado pelo Hemocentro de destino."
            )

    elif status_validacao == (
        ValidacaoPedido.StatusValidacao.RECUSADO
    ):
        novo_status = PedidoSangue.Status.RECUSADA

        if not motivo:
            motivo = (
                "Pedido recusado pelo Hemocentro de destino."
            )

    elif status_validacao == ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA:
        novo_status = PedidoSangue.Status.CORRECAO_SOLICITADA

        if not motivo:
            motivo = "O Hemocentro solicitou correção das informações."

    else:
        novo_status = PedidoSangue.Status.EM_ANALISE

        if not motivo:
            motivo = (
                "Pedido marcado como suspeito "
                "e mantido em análise."
            )

    pedido.status = novo_status

    if novo_status == PedidoSangue.Status.PUBLICADA:
        pedido.publicado_por = moderador
        pedido.publicado_em = timezone.now()

    pedido.save(
        update_fields=[
            "status",
            "atualizado_em",
            "publicado_por",
            "publicado_em",
        ]
    )

    notificacoes_geradas = 0
    if novo_status == PedidoSangue.Status.PUBLICADA:
        from .pedidos import criar_notificacoes_para_pedido

        notificacoes_geradas = criar_notificacoes_para_pedido(pedido=pedido)

    validacao = ValidacaoPedido.objects.create(
        pedido=pedido,
        status_validacao=status_validacao,
        motivo=motivo,
        moderador=moderador,
    )

    registrar_auditoria(
        acao=AuditoriaAcaoCritica.Acao.MODERACAO,
        resultado=AuditoriaAcaoCritica.Resultado.SUCESSO,
        usuario=moderador,
        alvo=pedido,
        descricao=(
            "Decisao institucional sobre pedido de sangue." if institucional
            else "Validacao administrativa de pedido de sangue."
        ),
        request=request,
        metadados={
            "evento": "PUBLICACAO_PEDIDO" if institucional and status_validacao == ValidacaoPedido.StatusValidacao.APROVADO else "VALIDACAO_PEDIDO",
            "status_anterior": status_anterior,
            "perfil_responsavel": moderador.perfil,
            "id_pedido": pedido.pk,
            "id_validacao": validacao.pk,
            "status_validacao": status_validacao,
            "status_pedido": novo_status,
            "motivo": motivo,
            "notificacoes_geradas": notificacoes_geradas,
        },
    )

    return validacao
```

**Explicação deste trecho:**

**Linha 174 — FunctionDef** (nível 0 do bloco).

Define `registrar_decisao_validacao_pedido(*, pedido, moderador, status_validacao, motivo='', request=None)`. O corpo só executa quando a função/método é chamado. Decoradores: `transaction.atomic`.

Bloco `body` da linha 174:

**Linha 182 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 187 — Assign** (nível 1 do bloco).

Associa `motivo` a a chamada `(motivo or '').strip`, que remove espaços nas extremidades do texto.


**Linha 189 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `status_validacao` não contido em `[ValidacaoPedido.StatusValidacao.APROVADO, ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA, ValidacaoPedido.StatusValidacao.RECUSADO, ValidacaoPedido.StatusValidacao.SUSPEITO]`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 189:

**Linha 195 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'Status de validação inválido.'`.

**Linha 202 — Assign** (nível 1 do bloco).

Associa `administrador` a a chamada `usuario_e_administrador`; argumentos posicionais: `moderador`.


**Linha 203 — Assign** (nível 1 do bloco).

Associa `hemocentro_do_destino` a todas as condições: `hemocentro_aprovado(moderador)` ; `pedido.hemocentro_destino_id == moderador.pk` (com avaliação interrompida assim que o resultado é determinado).

**Linha 208 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `status_validacao` igual a `ValidacaoPedido.StatusValidacao.SUSPEITO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 208:

**Linha 209 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `not administrador` ; `not hemocentro_do_destino` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 209:

**Linha 210 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'Somente o administrador ou o Hemocentro aprovado de destino pode marcar um pedido como suspeito.'`.

Bloco `orelse` da linha 208:

**Linha 214 — If** (nível 2 do bloco).

Escolhe um caminho verificando a negação de `hemocentro_do_destino`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 214:

**Linha 215 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'Somente o Hemocentro aprovado de destino pode analisar e publicar pedidos.'`.

**Linha 225 — Assign** (nível 1 do bloco).

Associa `pedido` a a chamada `PedidoSangue.objects.select_for_update().get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `pk=pedido.pk`.

- `pk=pedido.pk`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 227 — Assign** (nível 1 do bloco).

Associa `status_anterior` a o atributo `status` de `pedido`.

**Linha 228 — Assign** (nível 1 do bloco).

Associa `institucional` a o valor associado ao nome `hemocentro_do_destino`.

**Linha 230 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `pedido.status` igual a `PedidoSangue.Status.ENCERRADA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 230:

**Linha 231 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'Não é possível validar um pedido encerrado.'`.

**Linha 233 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `status_validacao` igual a `ValidacaoPedido.StatusValidacao.APROVADO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 233:

**Linha 236 — Expr** (nível 2 do bloco).

Executa a chamada `validar_dados_pedido`; argumentos posicionais: `pedido`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 237 — Assign** (nível 2 do bloco).

Associa `novo_status` a o atributo `PUBLICADA` de `PedidoSangue.Status`.

**Linha 239 — If** (nível 2 do bloco).

Escolhe um caminho verificando a negação de `motivo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 239:

**Linha 240 — Assign** (nível 3 do bloco).

Associa `motivo` a o valor literal `'Pedido aprovado pelo Hemocentro de destino.'`.

Bloco `orelse` da linha 233:

**Linha 244 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `status_validacao` igual a `ValidacaoPedido.StatusValidacao.RECUSADO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 244:

**Linha 247 — Assign** (nível 3 do bloco).

Associa `novo_status` a o atributo `RECUSADA` de `PedidoSangue.Status`.

**Linha 249 — If** (nível 3 do bloco).

Escolhe um caminho verificando a negação de `motivo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 249:

**Linha 250 — Assign** (nível 4 do bloco).

Associa `motivo` a o valor literal `'Pedido recusado pelo Hemocentro de destino.'`.

Bloco `orelse` da linha 244:

**Linha 254 — If** (nível 3 do bloco).

Escolhe um caminho verificando a comparação `status_validacao` igual a `ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 254:

**Linha 255 — Assign** (nível 4 do bloco).

Associa `novo_status` a o atributo `CORRECAO_SOLICITADA` de `PedidoSangue.Status`.

**Linha 257 — If** (nível 4 do bloco).

Escolhe um caminho verificando a negação de `motivo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 257:

**Linha 258 — Assign** (nível 5 do bloco).

Associa `motivo` a o valor literal `'O Hemocentro solicitou correção das informações.'`.

Bloco `orelse` da linha 254:

**Linha 261 — Assign** (nível 4 do bloco).

Associa `novo_status` a o atributo `EM_ANALISE` de `PedidoSangue.Status`.

**Linha 263 — If** (nível 4 do bloco).

Escolhe um caminho verificando a negação de `motivo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 263:

**Linha 264 — Assign** (nível 5 do bloco).

Associa `motivo` a o valor literal `'Pedido marcado como suspeito e mantido em análise.'`.

**Linha 269 — Assign** (nível 1 do bloco).

Associa `pedido.status` a o valor associado ao nome `novo_status`.

**Linha 271 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `novo_status` igual a `PedidoSangue.Status.PUBLICADA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 271:

**Linha 272 — Assign** (nível 2 do bloco).

Associa `pedido.publicado_por` a o valor associado ao nome `moderador`.

**Linha 273 — Assign** (nível 2 do bloco).

Associa `pedido.publicado_em` a a chamada `timezone.now`, que obtém o instante atual; timezone.now respeita o tratamento de fuso do Django.


**Linha 275 — Expr** (nível 1 do bloco).

Executa a chamada `pedido.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['status', 'atualizado_em', 'publicado_por', 'publicado_em']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 284 — Assign** (nível 1 do bloco).

Associa `notificacoes_geradas` a o valor literal `0`.

**Linha 285 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `novo_status` igual a `PedidoSangue.Status.PUBLICADA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 285:

**Linha 286 — ImportFrom** (nível 2 do bloco).

Importa de `.pedidos` os nomes `criar_notificacoes_para_pedido`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 288 — Assign** (nível 2 do bloco).

Associa `notificacoes_geradas` a a chamada `criar_notificacoes_para_pedido`; argumentos nomeados: `pedido=pedido`.

- `pedido=pedido`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 290 — Assign** (nível 1 do bloco).

Associa `validacao` a a chamada `ValidacaoPedido.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `pedido=pedido`, `status_validacao=status_validacao`, `motivo=motivo`, `moderador=moderador`.

- `pedido=pedido`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status_validacao=status_validacao`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `motivo=motivo`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `moderador=moderador`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 297 — Expr** (nível 1 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.MODERACAO`, `resultado=AuditoriaAcaoCritica.Resultado.SUCESSO`, `usuario=moderador`, `alvo=pedido`, `descricao='Decisao institucional sobre pedido de sangue.' if institucional else 'Validacao administrativa de pedido de sangue.'`, `request=request`, `metadados={'evento': 'PUBLICACAO_PEDIDO' if institucional and status_validacao == ValidacaoPedido.StatusValidacao.APROVADO else 'VALIDACAO_PEDIDO', 'status_anterior': status_anterior, 'perfil_responsavel': moderador.perfil, 'id_pedido': pedido.pk, 'id_validacao': validacao.pk, 'status_validacao': status_validacao, 'status_pedido': novo_status, 'motivo': motivo, 'notificacoes_geradas': notificacoes_geradas}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 320 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `validacao` ao chamador.

### aprovar_pedido — linhas 323 a 338

```python
def aprovar_pedido(
    *,
    pedido,
    moderador,
    motivo="",
    request=None,
):
    return registrar_decisao_validacao_pedido(
        pedido=pedido,
        moderador=moderador,
        status_validacao=(
            ValidacaoPedido.StatusValidacao.APROVADO
        ),
        motivo=motivo,
        request=request,
    )
```

**Explicação deste trecho:**

**Linha 323 — FunctionDef** (nível 0 do bloco).

Define `aprovar_pedido(*, pedido, moderador, motivo='', request=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 323:

**Linha 330 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `registrar_decisao_validacao_pedido`; argumentos nomeados: `pedido=pedido`, `moderador=moderador`, `status_validacao=ValidacaoPedido.StatusValidacao.APROVADO`, `motivo=motivo`, `request=request` ao chamador.

### recusar_pedido — linhas 341 a 356

```python
def recusar_pedido(
    *,
    pedido,
    moderador,
    motivo="",
    request=None,
):
    return registrar_decisao_validacao_pedido(
        pedido=pedido,
        moderador=moderador,
        status_validacao=(
            ValidacaoPedido.StatusValidacao.RECUSADO
        ),
        motivo=motivo,
        request=request,
    )
```

**Explicação deste trecho:**

**Linha 341 — FunctionDef** (nível 0 do bloco).

Define `recusar_pedido(*, pedido, moderador, motivo='', request=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 341:

**Linha 348 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `registrar_decisao_validacao_pedido`; argumentos nomeados: `pedido=pedido`, `moderador=moderador`, `status_validacao=ValidacaoPedido.StatusValidacao.RECUSADO`, `motivo=motivo`, `request=request` ao chamador.

### solicitar_correcao_pedido — linhas 359 a 374

```python
def solicitar_correcao_pedido(
    *,
    pedido,
    moderador,
    motivo="",
    request=None,
):
    return registrar_decisao_validacao_pedido(
        pedido=pedido,
        moderador=moderador,
        status_validacao=(
            ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA
        ),
        motivo=motivo,
        request=request,
    )
```

**Explicação deste trecho:**

**Linha 359 — FunctionDef** (nível 0 do bloco).

Define `solicitar_correcao_pedido(*, pedido, moderador, motivo='', request=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 359:

**Linha 366 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `registrar_decisao_validacao_pedido`; argumentos nomeados: `pedido=pedido`, `moderador=moderador`, `status_validacao=ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA`, `motivo=motivo`, `request=request` ao chamador.

### marcar_pedido_suspeito — linhas 377 a 392

```python
def marcar_pedido_suspeito(
    *,
    pedido,
    moderador,
    motivo="",
    request=None,
):
    return registrar_decisao_validacao_pedido(
        pedido=pedido,
        moderador=moderador,
        status_validacao=(
            ValidacaoPedido.StatusValidacao.SUSPEITO
        ),
        motivo=motivo,
        request=request,
    )
```

**Explicação deste trecho:**

**Linha 377 — FunctionDef** (nível 0 do bloco).

Define `marcar_pedido_suspeito(*, pedido, moderador, motivo='', request=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 377:

**Linha 384 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `registrar_decisao_validacao_pedido`; argumentos nomeados: `pedido=pedido`, `moderador=moderador`, `status_validacao=ValidacaoPedido.StatusValidacao.SUSPEITO`, `motivo=motivo`, `request=request` ao chamador.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 1: `# Este módulo controla a criação e a validação dos pedidos de sangue.`
- Linha 3: `# 1. validar_dados_pedido()`
- Linha 4: `#    Confere título, tipo sanguíneo, urgência, cidade, descrição, solicitante, e-mail de contato e Hemocentro de destino aprovado.`
- Linha 6: `# 2. criar_pedido_pendente()`
- Linha 7: `#    Cria o pedido com status ENVIADA.`
- Linha 8: `#    Administradores e Hemocentros não criam solicitações comuns.`
- Linha 9: `#    O pedido não é publicado automaticamente.`
- Linha 10: `#    Também verifica pedidos semelhantes nos últimos 7 dias e marca possíveis duplicidades apenas como alerta.`
- Linha 12: `# 3. registrar_decisao_validacao_pedido()`
- Linha 13: `#    Registra a decisão sobre o pedido dentro de uma transação segura.`
- Linha 14: `#    Pedidos encerrados não podem ser alterados.`
- Linha 15: `#    O Hemocentro aprovado de destino pode:`
- Linha 16: `#    - aprovar e publicar;`
- Linha 17: `#    - recusar;`
- Linha 18: `#    - solicitar correção;`
- Linha 19: `#    - marcar como suspeito.`
- Linha 20: `#    O Administrador pode apenas marcar o pedido como suspeito para moderação e auditoria.`
- Linha 22: `# 4. Quando o pedido é aprovado:`
- Linha 23: `#    - seu status muda para PUBLICADA;`
- Linha 24: `#    - o Hemocentro responsável e a data são registrados;`
- Linha 25: `#    - notificações compatíveis são criadas;`
- Linha 26: `#    - a decisão é salva no histórico;`
- Linha 27: `#    - a ação é registrada na auditoria.`
- Linha 29: `# 5. Funções auxiliares`
- Linha 30: `#    aprovar_pedido(), recusar_pedido(), solicitar_correcao_pedido() e`
- Linha 31: `#    marcar_pedido_suspeito() apenas chamam a função principal informando o`
- Linha 32: `#    status correspondente.`
- Linha 34: `# O formulário valida os dados na interface, este arquivo repete as validações importantes no servidor e o modelo protege a integridade final do banco.`
- Linha 150: `# Semelhança é apenas um alerta para o Hemocentro; nunca bloqueia uma`
- Linha 151: `# necessidade legítima automaticamente.`
- Linha 199: `# A publicação, a recusa e a solicitação de correção pertencem somente`
- Linha 200: `# ao Hemocentro aprovado de destino. O Administrador apenas pode`
- Linha 201: `# registrar uma suspeita para fins de moderação/auditoria.`
- Linha 220: `# Não use select_related junto com select_for_update aqui. Como`
- Linha 221: `# solicitante é uma FK anulável, o Django gera LEFT OUTER JOIN e o`
- Linha 222: `# PostgreSQL não permite aplicar FOR UPDATE ao lado opcional da junção.`
- Linha 223: `# O bloqueio deve atingir somente a linha do pedido; as relações são`
- Linha 224: `# carregadas sob demanda quando as notificações forem criadas.`

