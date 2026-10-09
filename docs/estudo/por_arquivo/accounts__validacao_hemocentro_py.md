# accounts/validacao_hemocentro.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Estados institucionais, decisao e historico de hemocentros.

**Arquivo original:** [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
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
            usuario.is_superuser
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

    if admin.perfil == Usuario.Perfil.HEMOCENTRO:
        raise PermissionDenied("Hemocentros nao podem validar cadastros institucionais.")

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
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### ImportFrom — linhas 1 a 1

```python
from functools import wraps
```

**Explicação deste trecho:**

**Linha 1 — ImportFrom** (nível 0 do bloco).

Importa de `functools` os nomes `wraps`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 3 a 3

```python
from django.core.exceptions import PermissionDenied, ValidationError
```

**Explicação deste trecho:**

**Linha 3 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.exceptions` os nomes `PermissionDenied`, `ValidationError`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 4 a 4

```python
from django.db import transaction
```

**Explicação deste trecho:**

**Linha 4 — ImportFrom** (nível 0 do bloco).

Importa de `django.db` os nomes `transaction`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 6 a 6

```python
from .auditoria import registrar_auditoria
```

**Explicação deste trecho:**

**Linha 6 — ImportFrom** (nível 0 do bloco).

Importa de `.auditoria` os nomes `registrar_auditoria`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 7 a 7

```python
from .models import AuditoriaAcaoCritica, Usuario, ValidacaoHemocentro
```

**Explicação deste trecho:**

**Linha 7 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `AuditoriaAcaoCritica`, `Usuario`, `ValidacaoHemocentro`. Pontos iniciais indicam importação relativa ao pacote.

### Assign — linhas 10 a 14

```python
PARECER_PADRAO = {
    Usuario.StatusValidacaoHemocentro.APROVADO: "Hemocentro aprovado pelo administrador.",
    Usuario.StatusValidacaoHemocentro.RECUSADO: "Cadastro de hemocentro recusado pelo administrador.",
    Usuario.StatusValidacaoHemocentro.CORRECAO: "Administrador solicitou correcao dos dados cadastrais.",
}
```

**Explicação deste trecho:**

**Linha 10 — Assign** (nível 0 do bloco).

Associa `PARECER_PADRAO` a um dicionário de 3 entradas; as chaves dão nome aos valores associados.

- Chave `Usuario.StatusValidacaoHemocentro.APROVADO`: recebe o valor literal `'Hemocentro aprovado pelo administrador.'`.
- Chave `Usuario.StatusValidacaoHemocentro.RECUSADO`: recebe o valor literal `'Cadastro de hemocentro recusado pelo administrador.'`.
- Chave `Usuario.StatusValidacaoHemocentro.CORRECAO`: recebe o valor literal `'Administrador solicitou correcao dos dados cadastrais.'`.

### usuario_e_administrador — linhas 17 a 24

```python
def usuario_e_administrador(usuario):
    return bool(
        getattr(usuario, "is_authenticated", False)
        and (
            usuario.is_superuser
            or usuario.perfil == Usuario.Perfil.ADMINISTRADOR
        )
    )
```

**Explicação deste trecho:**

**Linha 17 — FunctionDef** (nível 0 do bloco).

Define `usuario_e_administrador(usuario)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 17:

**Linha 18 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `bool`; argumentos posicionais: `getattr(usuario, 'is_authenticated', False) and (usuario.is_superuser or usuario.perfil == Usuario.Perfil.ADMINISTRADOR)` ao chamador.

### usuario_e_hemocentro — linhas 27 a 31

```python
def usuario_e_hemocentro(usuario):
    return bool(
        getattr(usuario, "is_authenticated", False)
        and usuario.perfil == Usuario.Perfil.HEMOCENTRO
    )
```

**Explicação deste trecho:**

**Linha 27 — FunctionDef** (nível 0 do bloco).

Define `usuario_e_hemocentro(usuario)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 27:

**Linha 28 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `bool`; argumentos posicionais: `getattr(usuario, 'is_authenticated', False) and usuario.perfil == Usuario.Perfil.HEMOCENTRO` ao chamador.

### hemocentro_aprovado — linhas 34 a 38

```python
def hemocentro_aprovado(usuario):
    return (
        usuario_e_hemocentro(usuario)
        and usuario.status_validacao == Usuario.StatusValidacaoHemocentro.APROVADO
    )
```

**Explicação deste trecho:**

**Linha 34 — FunctionDef** (nível 0 do bloco).

Define `hemocentro_aprovado(usuario)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 34:

**Linha 35 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve todas as condições: `usuario_e_hemocentro(usuario)` ; `usuario.status_validacao == Usuario.StatusValidacaoHemocentro.APROVADO` (com avaliação interrompida assim que o resultado é determinado) ao chamador.

### validar_publicacao_hemocentro — linhas 41 a 56

```python
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
```

**Explicação deste trecho:**

**Linha 41 — FunctionDef** (nível 0 do bloco).

Define `validar_publicacao_hemocentro(usuario)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 41:

**Linha 42 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `getattr(usuario, 'is_authenticated', False)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 42:

**Linha 43 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'Faca login para publicar estoque ou campanha.'`.

**Linha 45 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `usuario_e_hemocentro(usuario)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 45:

**Linha 46 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'Somente usuarios com perfil Hemocentro podem publicar estoque ou campanha.'`.

**Linha 50 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `hemocentro_aprovado(usuario)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 50:

**Linha 51 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `f'Hemocentro ainda nao aprovado. Status atual: {usuario.get_status_validacao_display()}.'`.

**Linha 56 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor literal `True` ao chamador.

### exigir_hemocentro_aprovado — linhas 59 a 65

```python
def exigir_hemocentro_aprovado(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        validar_publicacao_hemocentro(request.user)
        return view_func(request, *args, **kwargs)

    return wrapper
```

**Explicação deste trecho:**

**Linha 59 — FunctionDef** (nível 0 do bloco).

Define `exigir_hemocentro_aprovado(view_func)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 59:

**Linha 61 — FunctionDef** (nível 1 do bloco).

Define `wrapper(request, *args, **kwargs)`. O corpo só executa quando a função/método é chamado. Decoradores: `wraps(view_func)`.

Bloco `body` da linha 61:

**Linha 62 — Expr** (nível 2 do bloco).

Executa a chamada `validar_publicacao_hemocentro`; argumentos posicionais: `request.user`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 63 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `view_func`; argumentos posicionais: `request`, `*args`; argumentos nomeados: `**=kwargs` ao chamador.

**Linha 65 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `wrapper` ao chamador.

### registrar_decisao_validacao_hemocentro — linhas 68 a 122

```python
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

    if admin.perfil == Usuario.Perfil.HEMOCENTRO:
        raise PermissionDenied("Hemocentros nao podem validar cadastros institucionais.")

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
```

**Explicação deste trecho:**

**Linha 68 — FunctionDef** (nível 0 do bloco).

Define `registrar_decisao_validacao_hemocentro(*, hemocentro, admin, status, parecer='', request=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 68:

**Linha 76 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `hemocentro.perfil` diferente de `Usuario.Perfil.HEMOCENTRO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 76:

**Linha 77 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `'Somente usuarios com perfil Hemocentro podem passar por validacao.'`.

**Linha 81 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `usuario_e_administrador(admin)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 81:

**Linha 82 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'Somente administradores podem validar Hemocentros.'`.

**Linha 84 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `admin.perfil` igual a `Usuario.Perfil.HEMOCENTRO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 84:

**Linha 85 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'Hemocentros nao podem validar cadastros institucionais.'`.

**Linha 87 — Assign** (nível 1 do bloco).

Associa `parecer` a pelo menos uma das condições: `(parecer or '').strip()` ; `PARECER_PADRAO.get(status, '')` (com avaliação interrompida assim que o resultado é determinado).

**Linha 89 — With** (nível 1 do bloco).

Executa sob os contextos `transaction.atomic()`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 89:

**Linha 90 — Assign** (nível 2 do bloco).

Associa `hemocentro_atualizado` a a chamada `Usuario.objects.select_for_update().get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `pk=hemocentro.pk`.

- `pk=hemocentro.pk`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 94 — Assign** (nível 2 do bloco).

Associa `status_anterior` a o atributo `status_validacao` de `hemocentro_atualizado`.

**Linha 95 — Assign** (nível 2 do bloco).

Associa `hemocentro_atualizado.status_validacao` a o valor associado ao nome `status`.

**Linha 96 — Expr** (nível 2 do bloco).

Executa a chamada `hemocentro_atualizado.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['status_validacao', 'atualizado_em']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 100 — Assign** (nível 2 do bloco).

Associa `validacao` a a chamada `ValidacaoHemocentro.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `hemocentro=hemocentro_atualizado`, `admin=admin`, `status=status`, `parecer=parecer`.

- `hemocentro=hemocentro_atualizado`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `admin=admin`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status=status`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `parecer=parecer`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 107 — Expr** (nível 2 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.APROVACAO_HEMOCENTRO`, `resultado=AuditoriaAcaoCritica.Resultado.SUCESSO`, `usuario=admin`, `alvo=hemocentro_atualizado`, `descricao='Validacao institucional de hemocentro.'`, `request=request`, `metadados={'id_validacao': validacao.pk, 'status_anterior': status_anterior, 'status_novo': status, 'parecer': parecer}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 122 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `validacao` ao chamador.

### aprovar_hemocentro — linhas 125 a 132

```python
def aprovar_hemocentro(*, hemocentro, admin, parecer="", request=None):
    return registrar_decisao_validacao_hemocentro(
        hemocentro=hemocentro,
        admin=admin,
        status=Usuario.StatusValidacaoHemocentro.APROVADO,
        parecer=parecer,
        request=request,
    )
```

**Explicação deste trecho:**

**Linha 125 — FunctionDef** (nível 0 do bloco).

Define `aprovar_hemocentro(*, hemocentro, admin, parecer='', request=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 125:

**Linha 126 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `registrar_decisao_validacao_hemocentro`; argumentos nomeados: `hemocentro=hemocentro`, `admin=admin`, `status=Usuario.StatusValidacaoHemocentro.APROVADO`, `parecer=parecer`, `request=request` ao chamador.

### recusar_hemocentro — linhas 135 a 142

```python
def recusar_hemocentro(*, hemocentro, admin, parecer="", request=None):
    return registrar_decisao_validacao_hemocentro(
        hemocentro=hemocentro,
        admin=admin,
        status=Usuario.StatusValidacaoHemocentro.RECUSADO,
        parecer=parecer,
        request=request,
    )
```

**Explicação deste trecho:**

**Linha 135 — FunctionDef** (nível 0 do bloco).

Define `recusar_hemocentro(*, hemocentro, admin, parecer='', request=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 135:

**Linha 136 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `registrar_decisao_validacao_hemocentro`; argumentos nomeados: `hemocentro=hemocentro`, `admin=admin`, `status=Usuario.StatusValidacaoHemocentro.RECUSADO`, `parecer=parecer`, `request=request` ao chamador.

### solicitar_correcao_hemocentro — linhas 145 a 152

```python
def solicitar_correcao_hemocentro(*, hemocentro, admin, parecer="", request=None):
    return registrar_decisao_validacao_hemocentro(
        hemocentro=hemocentro,
        admin=admin,
        status=Usuario.StatusValidacaoHemocentro.CORRECAO,
        parecer=parecer,
        request=request,
    )
```

**Explicação deste trecho:**

**Linha 145 — FunctionDef** (nível 0 do bloco).

Define `solicitar_correcao_hemocentro(*, hemocentro, admin, parecer='', request=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 145:

**Linha 146 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `registrar_decisao_validacao_hemocentro`; argumentos nomeados: `hemocentro=hemocentro`, `admin=admin`, `status=Usuario.StatusValidacaoHemocentro.CORRECAO`, `parecer=parecer`, `request=request` ao chamador.

