# accounts/auditoria.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Registro de eventos e observacao de acessos sensiveis.

**Arquivo original:** [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""
Funcoes centrais para registrar auditorias de acoes criticas.

As demais partes do sistema devem usar ``registrar_auditoria`` em vez de criar
AuditoriaAcaoCritica diretamente. Isso mantem saneamento de metadados,
captura de IP e regras de seguranca em um unico ponto.
"""

from ipaddress import ip_address

from django.forms.models import model_to_dict
from django.utils.deprecation import MiddlewareMixin

from .models import AuditoriaAcaoCritica


CAMPOS_SENSIVEIS = {
    "password",
    "senha",
    "senha_hash",
    "token",
    "csrfmiddlewaretoken",
    "secret",
    "authorization",
}

"""serve para identiifcar de onde a ação veio"""
def obter_ip(request):
    """Usa o endereco da conexao, sem confiar em cabecalhos enviados pelo cliente."""

    if not request:
        return None

    try:
        return str(ip_address(request.META.get("REMOTE_ADDR", "")))
    except ValueError:
        return None


def obter_user_agent(request):
    """Extrai o user agent sem obrigar chamadas internas a terem request."""

    if not request:
        return ""
    return request.META.get("HTTP_USER_AGENT", "")


def limpar_metadados(valor):
    """Remove dados sensiveis de estruturas simples antes de salvar auditoria."""

    if isinstance(valor, dict):
        metadados_limpos = {}
        for chave, item in valor.items():
            chave_texto = str(chave)
            if chave_texto.lower() in CAMPOS_SENSIVEIS:
                metadados_limpos[chave_texto] = "[removido]"
            else:
                metadados_limpos[chave_texto] = limpar_metadados(item)
        return metadados_limpos

    if isinstance(valor, (list, tuple, set)):
        return [limpar_metadados(item) for item in valor]

    return valor


def identificar_alvo(alvo):
    """Transforma um model ou valor simples em alvo_tipo e alvo_id."""

    if alvo is None:
        return "", ""

    if hasattr(alvo, "_meta"):
        alvo_tipo = alvo._meta.label
        chave_primaria = alvo.pk
        return alvo_tipo, str(chave_primaria or "")

    return alvo.__class__.__name__, str(alvo)


def registrar_auditoria(
    *,
    acao,
    usuario=None,
    resultado=AuditoriaAcaoCritica.Resultado.SUCESSO,
    alvo=None,
    alvo_tipo="",
    alvo_id="",
    descricao="",
    request=None,
    ip=None,
    user_agent="",
    metadados=None,
):
    """Cria um registro de auditoria padronizado e sanitizado."""

    tipo_detectado, id_detectado = identificar_alvo(alvo)
    usuario_autenticado = getattr(usuario, "is_authenticated", False)

    if usuario is not None and not usuario_autenticado:
        usuario = None

    return AuditoriaAcaoCritica.objects.create(
        usuario=usuario,
        acao=acao,
        resultado=resultado,
        alvo_tipo=alvo_tipo or tipo_detectado,
        alvo_id=alvo_id or id_detectado,
        descricao=descricao,
        ip=ip or obter_ip(request),
        user_agent=user_agent or obter_user_agent(request),
        metadados=limpar_metadados(metadados or {}),
    )


def campos_sensiveis_alterados(objeto, campos):
    """Compara campos sensiveis de um model antes e depois da alteracao."""

    if not objeto.pk:
        return {}

    antigo = objeto.__class__.objects.filter(pk=objeto.pk).first()
    if not antigo:
        return {}

    alteracoes = {}
    for campo in campos:
        valor_antigo = getattr(antigo, campo)
        valor_novo = getattr(objeto, campo)
        if valor_antigo != valor_novo:
            alteracoes[campo] = {
                "antes": str(valor_antigo),
                "depois": str(valor_novo),
            }
    return alteracoes


def snapshot_campos(objeto, campos):
    """Retorna um dicionario com campos simples de um model."""

    dados = model_to_dict(objeto, fields=campos)
    return {campo: str(valor) for campo, valor in dados.items()}


class AuditoriaAcessosMiddleware(MiddlewareMixin):
    """Audita respostas protegidas sem copiar formularios ou dados clinicos."""

    ROTAS_SENSIVEIS = {
        "accounts:triagem_pergunta", "accounts:triagem_resultado",
        "accounts:triagem_historico", "accounts:painel_validacao_pedidos",
        "accounts:triagem_revisao", "accounts:minhas_solicitacoes",
        "accounts:painel_pedidos_hemocentro",
    }
    MODELOS_SENSIVEIS_ADMIN = {
        "usuario", "triagem", "respostatriagem", "consentimentolgpd",
        "pedidosangue", "validacaopedido", "validacaohemocentro",
        "notificacao", "auditoriaacaocritica",
    }

    def process_response(self, request, response):
        rota = getattr(request, "resolver_match", None)
        if rota is None:
            return response
        usuario = getattr(request, "user", None)
        autenticado = getattr(usuario, "is_authenticated", False)
        nome = rota.view_name
        protegido = nome.startswith("accounts:") and (
            nome in self.ROTAS_SENSIVEIS
            or any(parte in nome for parte in (
                "triagem_iniciar", "estoque_hemocentro", "cadastrar_estoque",
                "atualizar_estoque", "aprovar_pedido", "recusar_pedido",
                "pedido_publicar", "criar_pedido_sangue",
                "solicitar_correcao_pedido", "marcar_pedido_suspeito",
            ))
        )
        login_exigido = response.status_code == 302 and not autenticado and protegido
        bloqueado = response.status_code == 403 or (
            response.status_code == 404 and protegido and autenticado
        ) or login_exigido
        admin_sensivel = nome.startswith("admin:") and any(
            nome.startswith("admin:accounts_" + modelo + "_")
            for modelo in self.MODELOS_SENSIVEIS_ADMIN
        )
        dados_sensiveis = nome in self.ROTAS_SENSIVEIS or admin_sensivel or (
            nome == "accounts:dashboard" and getattr(usuario, "perfil", "") == "DOADOR"
        )
        if bloqueado:
            registrar_auditoria(
                acao=AuditoriaAcaoCritica.Acao.MODERACAO,
                resultado=AuditoriaAcaoCritica.Resultado.BLOQUEADO,
                usuario=usuario, request=request,
                descricao="Tentativa de acesso bloqueada.",
                metadados={"evento": "TENTATIVA_ACESSO", "rota": nome,
                           "metodo": request.method, "status_http": response.status_code},
            )
        elif dados_sensiveis and request.method == "GET" and response.status_code == 200 and autenticado:
            registrar_auditoria(
                acao=AuditoriaAcaoCritica.Acao.ACESSO_DADOS_SENSIVEIS,
                usuario=usuario, request=request,
                descricao="Consulta de dados sensiveis.",
                metadados={"rota": nome, "parametros": rota.kwargs},
            )
        return response
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 7

```python
"""
Funcoes centrais para registrar auditorias de acoes criticas.

As demais partes do sistema devem usar ``registrar_auditoria`` em vez de criar
AuditoriaAcaoCritica diretamente. Isso mantem saneamento de metadados,
captura de IP e regras de seguranca em um unico ponto.
"""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 9 a 9

```python
from ipaddress import ip_address
```

**Explicação deste trecho:**

**Linha 9 — ImportFrom** (nível 0 do bloco).

Importa de `ipaddress` os nomes `ip_address`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 11 a 11

```python
from django.forms.models import model_to_dict
```

**Explicação deste trecho:**

**Linha 11 — ImportFrom** (nível 0 do bloco).

Importa de `django.forms.models` os nomes `model_to_dict`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 12 a 12

```python
from django.utils.deprecation import MiddlewareMixin
```

**Explicação deste trecho:**

**Linha 12 — ImportFrom** (nível 0 do bloco).

Importa de `django.utils.deprecation` os nomes `MiddlewareMixin`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 14 a 14

```python
from .models import AuditoriaAcaoCritica
```

**Explicação deste trecho:**

**Linha 14 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `AuditoriaAcaoCritica`. Pontos iniciais indicam importação relativa ao pacote.

### Assign — linhas 17 a 25

```python
CAMPOS_SENSIVEIS = {
    "password",
    "senha",
    "senha_hash",
    "token",
    "csrfmiddlewaretoken",
    "secret",
    "authorization",
}
```

**Explicação deste trecho:**

**Linha 17 — Assign** (nível 0 do bloco).

Associa `CAMPOS_SENSIVEIS` a uma coleção Set com 7 itens, na expressão `{'password', 'senha', 'senha_hash', 'token', 'csrfmiddlewaretoken', 'secret', 'authorization'}`.

### Expr — linhas 27 a 27

```python
"""serve para identiifcar de onde a ação veio"""
```

**Explicação deste trecho:**

**Linha 27 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### obter_ip — linhas 28 a 37

```python
def obter_ip(request):
    """Usa o endereco da conexao, sem confiar em cabecalhos enviados pelo cliente."""

    if not request:
        return None

    try:
        return str(ip_address(request.META.get("REMOTE_ADDR", "")))
    except ValueError:
        return None
```

**Explicação deste trecho:**

**Linha 28 — FunctionDef** (nível 0 do bloco).

Define `obter_ip(request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 28:

**Linha 29 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 31 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `request`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 31:

**Linha 32 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

**Linha 34 — Try** (nível 1 do bloco).

Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.

Bloco `body` da linha 34:

**Linha 35 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `str`; argumentos posicionais: `ip_address(request.META.get('REMOTE_ADDR', ''))` ao chamador.

Erro tratado: `ValueError`.

**Linha 37 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `None` ao chamador.

### obter_user_agent — linhas 40 a 45

```python
def obter_user_agent(request):
    """Extrai o user agent sem obrigar chamadas internas a terem request."""

    if not request:
        return ""
    return request.META.get("HTTP_USER_AGENT", "")
```

**Explicação deste trecho:**

**Linha 40 — FunctionDef** (nível 0 do bloco).

Define `obter_user_agent(request)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 40:

**Linha 41 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 43 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `request`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 43:

**Linha 44 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor literal `''` ao chamador.

**Linha 45 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `request.META.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'HTTP_USER_AGENT'`, `''` ao chamador.

### limpar_metadados — linhas 48 a 64

```python
def limpar_metadados(valor):
    """Remove dados sensiveis de estruturas simples antes de salvar auditoria."""

    if isinstance(valor, dict):
        metadados_limpos = {}
        for chave, item in valor.items():
            chave_texto = str(chave)
            if chave_texto.lower() in CAMPOS_SENSIVEIS:
                metadados_limpos[chave_texto] = "[removido]"
            else:
                metadados_limpos[chave_texto] = limpar_metadados(item)
        return metadados_limpos

    if isinstance(valor, (list, tuple, set)):
        return [limpar_metadados(item) for item in valor]

    return valor
```

**Explicação deste trecho:**

**Linha 48 — FunctionDef** (nível 0 do bloco).

Define `limpar_metadados(valor)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 48:

**Linha 49 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 51 — If** (nível 1 do bloco).

Escolhe um caminho verificando a chamada `isinstance`; argumentos posicionais: `valor`, `dict`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 51:

**Linha 52 — Assign** (nível 2 do bloco).

Associa `metadados_limpos` a um dicionário de 0 entradas; as chaves dão nome aos valores associados.


**Linha 53 — For** (nível 2 do bloco).

Percorre `valor.items()`; cada item é atribuído a `(chave, item)` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 53:

**Linha 54 — Assign** (nível 3 do bloco).

Associa `chave_texto` a a chamada `str`; argumentos posicionais: `chave`.


**Linha 55 — If** (nível 3 do bloco).

Escolhe um caminho verificando a comparação `chave_texto.lower()` contido em `CAMPOS_SENSIVEIS`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 55:

**Linha 56 — Assign** (nível 4 do bloco).

Associa `metadados_limpos[chave_texto]` a o valor literal `'[removido]'`.

Bloco `orelse` da linha 55:

**Linha 58 — Assign** (nível 4 do bloco).

Associa `metadados_limpos[chave_texto]` a a chamada `limpar_metadados`; argumentos posicionais: `item`.


**Linha 59 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `metadados_limpos` ao chamador.

**Linha 61 — If** (nível 1 do bloco).

Escolhe um caminho verificando a chamada `isinstance`; argumentos posicionais: `valor`, `(list, tuple, set)`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 61:

**Linha 62 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve uma coleção/gerador construído por compreensão em `[limpar_metadados(item) for item in valor]`: percorre as fontes e aplica os filtros declarados ao chamador.

**Linha 64 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `valor` ao chamador.

### identificar_alvo — linhas 67 a 78

```python
def identificar_alvo(alvo):
    """Transforma um model ou valor simples em alvo_tipo e alvo_id."""

    if alvo is None:
        return "", ""

    if hasattr(alvo, "_meta"):
        alvo_tipo = alvo._meta.label
        chave_primaria = alvo.pk
        return alvo_tipo, str(chave_primaria or "")

    return alvo.__class__.__name__, str(alvo)
```

**Explicação deste trecho:**

**Linha 67 — FunctionDef** (nível 0 do bloco).

Define `identificar_alvo(alvo)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 67:

**Linha 68 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 70 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `alvo` o mesmo objeto que `None`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 70:

**Linha 71 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve uma coleção Tuple com 2 itens, na expressão `('', '')` ao chamador.

**Linha 73 — If** (nível 1 do bloco).

Escolhe um caminho verificando a chamada `hasattr`; argumentos posicionais: `alvo`, `'_meta'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 73:

**Linha 74 — Assign** (nível 2 do bloco).

Associa `alvo_tipo` a o atributo `label` de `alvo._meta`.

**Linha 75 — Assign** (nível 2 do bloco).

Associa `chave_primaria` a o atributo `pk` de `alvo`.

**Linha 76 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve uma coleção Tuple com 2 itens, na expressão `(alvo_tipo, str(chave_primaria or ''))` ao chamador.

**Linha 78 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve uma coleção Tuple com 2 itens, na expressão `(alvo.__class__.__name__, str(alvo))` ao chamador.

### registrar_auditoria — linhas 81 a 113

```python
def registrar_auditoria(
    *,
    acao,
    usuario=None,
    resultado=AuditoriaAcaoCritica.Resultado.SUCESSO,
    alvo=None,
    alvo_tipo="",
    alvo_id="",
    descricao="",
    request=None,
    ip=None,
    user_agent="",
    metadados=None,
):
    """Cria um registro de auditoria padronizado e sanitizado."""

    tipo_detectado, id_detectado = identificar_alvo(alvo)
    usuario_autenticado = getattr(usuario, "is_authenticated", False)

    if usuario is not None and not usuario_autenticado:
        usuario = None

    return AuditoriaAcaoCritica.objects.create(
        usuario=usuario,
        acao=acao,
        resultado=resultado,
        alvo_tipo=alvo_tipo or tipo_detectado,
        alvo_id=alvo_id or id_detectado,
        descricao=descricao,
        ip=ip or obter_ip(request),
        user_agent=user_agent or obter_user_agent(request),
        metadados=limpar_metadados(metadados or {}),
    )
```

**Explicação deste trecho:**

**Linha 81 — FunctionDef** (nível 0 do bloco).

Define `registrar_auditoria(*, acao, usuario=None, resultado=AuditoriaAcaoCritica.Resultado.SUCESSO, alvo=None, alvo_tipo='', alvo_id='', descricao='', request=None, ip=None, user_agent='', metadados=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 81:

**Linha 95 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 97 — Assign** (nível 1 do bloco).

Associa `(tipo_detectado, id_detectado)` a a chamada `identificar_alvo`; argumentos posicionais: `alvo`.


**Linha 98 — Assign** (nível 1 do bloco).

Associa `usuario_autenticado` a a chamada `getattr`; argumentos posicionais: `usuario`, `'is_authenticated'`, `False`.


**Linha 100 — If** (nível 1 do bloco).

Escolhe um caminho verificando todas as condições: `usuario is not None` ; `not usuario_autenticado` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 100:

**Linha 101 — Assign** (nível 2 do bloco).

Associa `usuario` a o valor literal `None`.

**Linha 103 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `AuditoriaAcaoCritica.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=usuario`, `acao=acao`, `resultado=resultado`, `alvo_tipo=alvo_tipo or tipo_detectado`, `alvo_id=alvo_id or id_detectado`, `descricao=descricao`, `ip=ip or obter_ip(request)`, `user_agent=user_agent or obter_user_agent(request)`, `metadados=limpar_metadados(metadados or {})` ao chamador.

### campos_sensiveis_alterados — linhas 116 a 135

```python
def campos_sensiveis_alterados(objeto, campos):
    """Compara campos sensiveis de um model antes e depois da alteracao."""

    if not objeto.pk:
        return {}

    antigo = objeto.__class__.objects.filter(pk=objeto.pk).first()
    if not antigo:
        return {}

    alteracoes = {}
    for campo in campos:
        valor_antigo = getattr(antigo, campo)
        valor_novo = getattr(objeto, campo)
        if valor_antigo != valor_novo:
            alteracoes[campo] = {
                "antes": str(valor_antigo),
                "depois": str(valor_novo),
            }
    return alteracoes
```

**Explicação deste trecho:**

**Linha 116 — FunctionDef** (nível 0 do bloco).

Define `campos_sensiveis_alterados(objeto, campos)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 116:

**Linha 117 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 119 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `objeto.pk`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 119:

**Linha 120 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve um dicionário de 0 entradas; as chaves dão nome aos valores associados ao chamador.

**Linha 122 — Assign** (nível 1 do bloco).

Associa `antigo` a a chamada `objeto.__class__.objects.filter(pk=objeto.pk).first`, que obtém o primeiro resultado ou None.


**Linha 123 — If** (nível 1 do bloco).

Escolhe um caminho verificando a negação de `antigo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 123:

**Linha 124 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve um dicionário de 0 entradas; as chaves dão nome aos valores associados ao chamador.

**Linha 126 — Assign** (nível 1 do bloco).

Associa `alteracoes` a um dicionário de 0 entradas; as chaves dão nome aos valores associados.


**Linha 127 — For** (nível 1 do bloco).

Percorre `campos`; cada item é atribuído a `campo` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 127:

**Linha 128 — Assign** (nível 2 do bloco).

Associa `valor_antigo` a a chamada `getattr`; argumentos posicionais: `antigo`, `campo`.


**Linha 129 — Assign** (nível 2 do bloco).

Associa `valor_novo` a a chamada `getattr`; argumentos posicionais: `objeto`, `campo`.


**Linha 130 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `valor_antigo` diferente de `valor_novo`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 130:

**Linha 131 — Assign** (nível 3 do bloco).

Associa `alteracoes[campo]` a um dicionário de 2 entradas; as chaves dão nome aos valores associados.

- Chave `'antes'`: recebe a chamada `str`; argumentos posicionais: `valor_antigo`.
- Chave `'depois'`: recebe a chamada `str`; argumentos posicionais: `valor_novo`.

**Linha 135 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `alteracoes` ao chamador.

### snapshot_campos — linhas 138 a 142

```python
def snapshot_campos(objeto, campos):
    """Retorna um dicionario com campos simples de um model."""

    dados = model_to_dict(objeto, fields=campos)
    return {campo: str(valor) for campo, valor in dados.items()}
```

**Explicação deste trecho:**

**Linha 138 — FunctionDef** (nível 0 do bloco).

Define `snapshot_campos(objeto, campos)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 138:

**Linha 139 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 141 — Assign** (nível 1 do bloco).

Associa `dados` a a chamada `model_to_dict`; argumentos posicionais: `objeto`; argumentos nomeados: `fields=campos`.

- `fields=campos`: campos usados nesta configuração, índice ou restrição.

**Linha 142 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve uma coleção/gerador construído por compreensão em `{campo: str(valor) for campo, valor in dados.items()}`: percorre as fontes e aplica os filtros declarados ao chamador.

### AuditoriaAcessosMiddleware — linhas 145 a 203

```python
class AuditoriaAcessosMiddleware(MiddlewareMixin):
    """Audita respostas protegidas sem copiar formularios ou dados clinicos."""

    ROTAS_SENSIVEIS = {
        "accounts:triagem_pergunta", "accounts:triagem_resultado",
        "accounts:triagem_historico", "accounts:painel_validacao_pedidos",
        "accounts:triagem_revisao", "accounts:minhas_solicitacoes",
        "accounts:painel_pedidos_hemocentro",
    }
    MODELOS_SENSIVEIS_ADMIN = {
        "usuario", "triagem", "respostatriagem", "consentimentolgpd",
        "pedidosangue", "validacaopedido", "validacaohemocentro",
        "notificacao", "auditoriaacaocritica",
    }

    def process_response(self, request, response):
        rota = getattr(request, "resolver_match", None)
        if rota is None:
            return response
        usuario = getattr(request, "user", None)
        autenticado = getattr(usuario, "is_authenticated", False)
        nome = rota.view_name
        protegido = nome.startswith("accounts:") and (
            nome in self.ROTAS_SENSIVEIS
            or any(parte in nome for parte in (
                "triagem_iniciar", "estoque_hemocentro", "cadastrar_estoque",
                "atualizar_estoque", "aprovar_pedido", "recusar_pedido",
                "pedido_publicar", "criar_pedido_sangue",
                "solicitar_correcao_pedido", "marcar_pedido_suspeito",
            ))
        )
        login_exigido = response.status_code == 302 and not autenticado and protegido
        bloqueado = response.status_code == 403 or (
            response.status_code == 404 and protegido and autenticado
        ) or login_exigido
        admin_sensivel = nome.startswith("admin:") and any(
            nome.startswith("admin:accounts_" + modelo + "_")
            for modelo in self.MODELOS_SENSIVEIS_ADMIN
        )
        dados_sensiveis = nome in self.ROTAS_SENSIVEIS or admin_sensivel or (
            nome == "accounts:dashboard" and getattr(usuario, "perfil", "") == "DOADOR"
        )
        if bloqueado:
            registrar_auditoria(
                acao=AuditoriaAcaoCritica.Acao.MODERACAO,
                resultado=AuditoriaAcaoCritica.Resultado.BLOQUEADO,
                usuario=usuario, request=request,
                descricao="Tentativa de acesso bloqueada.",
                metadados={"evento": "TENTATIVA_ACESSO", "rota": nome,
                           "metodo": request.method, "status_http": response.status_code},
            )
        elif dados_sensiveis and request.method == "GET" and response.status_code == 200 and autenticado:
            registrar_auditoria(
                acao=AuditoriaAcaoCritica.Acao.ACESSO_DADOS_SENSIVEIS,
                usuario=usuario, request=request,
                descricao="Consulta de dados sensiveis.",
                metadados={"rota": nome, "parametros": rota.kwargs},
            )
        return response
```

**Explicação deste trecho:**

**Linha 145 — ClassDef** (nível 0 do bloco).

Define a classe `AuditoriaAcessosMiddleware` herdando de `MiddlewareMixin`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 145:

**Linha 146 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 148 — Assign** (nível 1 do bloco).

Associa `ROTAS_SENSIVEIS` a uma coleção Set com 7 itens, na expressão `{'accounts:triagem_pergunta', 'accounts:triagem_resultado', 'accounts:triagem_historico', 'accounts:painel_validacao_pedidos', 'accounts:triagem_revisao', 'accounts:minhas_solicitacoes', 'accounts:painel_pedidos_hemocentro'}`.

**Linha 154 — Assign** (nível 1 do bloco).

Associa `MODELOS_SENSIVEIS_ADMIN` a uma coleção Set com 9 itens, na expressão `{'usuario', 'triagem', 'respostatriagem', 'consentimentolgpd', 'pedidosangue', 'validacaopedido', 'validacaohemocentro', 'notificacao', 'auditoriaacaocritica'}`.

**Linha 160 — FunctionDef** (nível 1 do bloco).

Define `process_response(self, request, response)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 160:

**Linha 161 — Assign** (nível 2 do bloco).

Associa `rota` a a chamada `getattr`; argumentos posicionais: `request`, `'resolver_match'`, `None`.


**Linha 162 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `rota` o mesmo objeto que `None`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 162:

**Linha 163 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `response` ao chamador.

**Linha 164 — Assign** (nível 2 do bloco).

Associa `usuario` a a chamada `getattr`; argumentos posicionais: `request`, `'user'`, `None`.


**Linha 165 — Assign** (nível 2 do bloco).

Associa `autenticado` a a chamada `getattr`; argumentos posicionais: `usuario`, `'is_authenticated'`, `False`.


**Linha 166 — Assign** (nível 2 do bloco).

Associa `nome` a o atributo `view_name` de `rota`.

**Linha 167 — Assign** (nível 2 do bloco).

Associa `protegido` a todas as condições: `nome.startswith('accounts:')` ; `nome in self.ROTAS_SENSIVEIS or any((parte in nome for parte in ('triagem_iniciar', 'estoque_hemocentro', 'cadastrar_estoque', 'atualizar_estoque', 'aprovar_pedido', 'recusar_pedido', 'pedido_publicar', 'criar_pedido_sangue', 'solicitar_correcao_pedido', 'marcar_pedido_suspeito')))` (com avaliação interrompida assim que o resultado é determinado).

**Linha 176 — Assign** (nível 2 do bloco).

Associa `login_exigido` a todas as condições: `response.status_code == 302` ; `not autenticado` ; `protegido` (com avaliação interrompida assim que o resultado é determinado).

**Linha 177 — Assign** (nível 2 do bloco).

Associa `bloqueado` a pelo menos uma das condições: `response.status_code == 403` ; `response.status_code == 404 and protegido and autenticado` ; `login_exigido` (com avaliação interrompida assim que o resultado é determinado).

**Linha 180 — Assign** (nível 2 do bloco).

Associa `admin_sensivel` a todas as condições: `nome.startswith('admin:')` ; `any((nome.startswith('admin:accounts_' + modelo + '_') for modelo in self.MODELOS_SENSIVEIS_ADMIN))` (com avaliação interrompida assim que o resultado é determinado).

**Linha 184 — Assign** (nível 2 do bloco).

Associa `dados_sensiveis` a pelo menos uma das condições: `nome in self.ROTAS_SENSIVEIS` ; `admin_sensivel` ; `nome == 'accounts:dashboard' and getattr(usuario, 'perfil', '') == 'DOADOR'` (com avaliação interrompida assim que o resultado é determinado).

**Linha 187 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `bloqueado`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 187:

**Linha 188 — Expr** (nível 3 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.MODERACAO`, `resultado=AuditoriaAcaoCritica.Resultado.BLOQUEADO`, `usuario=usuario`, `request=request`, `descricao='Tentativa de acesso bloqueada.'`, `metadados={'evento': 'TENTATIVA_ACESSO', 'rota': nome, 'metodo': request.method, 'status_http': response.status_code}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 187:

**Linha 196 — If** (nível 3 do bloco).

Escolhe um caminho verificando todas as condições: `dados_sensiveis` ; `request.method == 'GET'` ; `response.status_code == 200` ; `autenticado` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 196:

**Linha 197 — Expr** (nível 4 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.ACESSO_DADOS_SENSIVEIS`, `usuario=usuario`, `request=request`, `descricao='Consulta de dados sensiveis.'`, `metadados={'rota': nome, 'parametros': rota.kwargs}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 203 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `response` ao chamador.

