# accounts/signals.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Registro automatico das falhas de autenticacao.

**Arquivo original:** [accounts/signals.py](<C:/Users/lb119/Elo/accounts/signals.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""
Sinais do Django usados para auditoria automatica.

Nesta etapa registramos falhas de login e marcamos como suspeito quando ha
muitas tentativas recentes para o mesmo e-mail ou IP.
"""

from datetime import timedelta

from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver
from django.utils import timezone

from .auditoria import obter_ip, obter_user_agent, registrar_auditoria
from .models import AuditoriaAcaoCritica


LIMITE_LOGIN_SUSPEITO = 5
JANELA_LOGIN_SUSPEITO_MINUTOS = 10


@receiver(user_login_failed)
def auditar_login_falho(sender, credentials, request, **kwargs):
    """Registra falha e login suspeito sem guardar a senha enviada."""

    email = (credentials or {}).get("username") or (credentials or {}).get("email")
    email = (email or "").strip().lower()
    ip = obter_ip(request)
    user_agent = obter_user_agent(request)

    registrar_auditoria(
        acao=AuditoriaAcaoCritica.Acao.LOGIN_FALHO,
        resultado=AuditoriaAcaoCritica.Resultado.FALHA,
        descricao="Tentativa de login sem sucesso.",
        request=request,
        ip=ip,
        user_agent=user_agent,
        metadados={"email": email},
    )

    inicio_janela = timezone.now() - timedelta(minutes=JANELA_LOGIN_SUSPEITO_MINUTOS)
    falhas_recentes = AuditoriaAcaoCritica.objects.filter(
        acao=AuditoriaAcaoCritica.Acao.LOGIN_FALHO,
        criado_em__gte=inicio_janela,
    )

    if email:
        falhas_recentes = falhas_recentes.filter(metadados__email=email)
    elif ip:
        falhas_recentes = falhas_recentes.filter(ip=ip)

    if falhas_recentes.count() >= LIMITE_LOGIN_SUSPEITO:
        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.LOGIN_SUSPEITO,
            resultado=AuditoriaAcaoCritica.Resultado.FALHA,
            descricao="Muitas tentativas de login falhas em curto periodo.",
            request=request,
            ip=ip,
            user_agent=user_agent,
            metadados={
                "email": email,
                "falhas_recentes": falhas_recentes.count(),
                "janela_minutos": JANELA_LOGIN_SUSPEITO_MINUTOS,
            },
        )
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 6

```python
"""
Sinais do Django usados para auditoria automatica.

Nesta etapa registramos falhas de login e marcamos como suspeito quando ha
muitas tentativas recentes para o mesmo e-mail ou IP.
"""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 8 a 8

```python
from datetime import timedelta
```

**Explicação deste trecho:**

**Linha 8 — ImportFrom** (nível 0 do bloco).

Importa de `datetime` os nomes `timedelta`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 10 a 10

```python
from django.contrib.auth.signals import user_login_failed
```

**Explicação deste trecho:**

**Linha 10 — ImportFrom** (nível 0 do bloco).

Importa de `django.contrib.auth.signals` os nomes `user_login_failed`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 11 a 11

```python
from django.dispatch import receiver
```

**Explicação deste trecho:**

**Linha 11 — ImportFrom** (nível 0 do bloco).

Importa de `django.dispatch` os nomes `receiver`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 12 a 12

```python
from django.utils import timezone
```

**Explicação deste trecho:**

**Linha 12 — ImportFrom** (nível 0 do bloco).

Importa de `django.utils` os nomes `timezone`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 14 a 14

```python
from .auditoria import obter_ip, obter_user_agent, registrar_auditoria
```

**Explicação deste trecho:**

**Linha 14 — ImportFrom** (nível 0 do bloco).

Importa de `.auditoria` os nomes `obter_ip`, `obter_user_agent`, `registrar_auditoria`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 15 a 15

```python
from .models import AuditoriaAcaoCritica
```

**Explicação deste trecho:**

**Linha 15 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `AuditoriaAcaoCritica`. Pontos iniciais indicam importação relativa ao pacote.

### Assign — linhas 18 a 18

```python
LIMITE_LOGIN_SUSPEITO = 5
```

**Explicação deste trecho:**

**Linha 18 — Assign** (nível 0 do bloco).

Associa `LIMITE_LOGIN_SUSPEITO` a o valor literal `5`.

### Assign — linhas 19 a 19

```python
JANELA_LOGIN_SUSPEITO_MINUTOS = 10
```

**Explicação deste trecho:**

**Linha 19 — Assign** (nível 0 do bloco).

Associa `JANELA_LOGIN_SUSPEITO_MINUTOS` a o valor literal `10`.

### auditar_login_falho — linhas 22 a 65

```python
@receiver(user_login_failed)
def auditar_login_falho(sender, credentials, request, **kwargs):
    """Registra falha e login suspeito sem guardar a senha enviada."""

    email = (credentials or {}).get("username") or (credentials or {}).get("email")
    email = (email or "").strip().lower()
    ip = obter_ip(request)
    user_agent = obter_user_agent(request)

    registrar_auditoria(
        acao=AuditoriaAcaoCritica.Acao.LOGIN_FALHO,
        resultado=AuditoriaAcaoCritica.Resultado.FALHA,
        descricao="Tentativa de login sem sucesso.",
        request=request,
        ip=ip,
        user_agent=user_agent,
        metadados={"email": email},
    )

    inicio_janela = timezone.now() - timedelta(minutes=JANELA_LOGIN_SUSPEITO_MINUTOS)
    falhas_recentes = AuditoriaAcaoCritica.objects.filter(
        acao=AuditoriaAcaoCritica.Acao.LOGIN_FALHO,
        criado_em__gte=inicio_janela,
    )

    if email:
        falhas_recentes = falhas_recentes.filter(metadados__email=email)
    elif ip:
        falhas_recentes = falhas_recentes.filter(ip=ip)

    if falhas_recentes.count() >= LIMITE_LOGIN_SUSPEITO:
        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.LOGIN_SUSPEITO,
            resultado=AuditoriaAcaoCritica.Resultado.FALHA,
            descricao="Muitas tentativas de login falhas em curto periodo.",
            request=request,
            ip=ip,
            user_agent=user_agent,
            metadados={
                "email": email,
                "falhas_recentes": falhas_recentes.count(),
                "janela_minutos": JANELA_LOGIN_SUSPEITO_MINUTOS,
            },
        )
```

**Explicação deste trecho:**

**Linha 23 — FunctionDef** (nível 0 do bloco).

Define `auditar_login_falho(sender, credentials, request, **kwargs)`. O corpo só executa quando a função/método é chamado. Decoradores: `receiver(user_login_failed)`.

Bloco `body` da linha 23:

**Linha 24 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 26 — Assign** (nível 1 do bloco).

Associa `email` a pelo menos uma das condições: `(credentials or {}).get('username')` ; `(credentials or {}).get('email')` (com avaliação interrompida assim que o resultado é determinado).

**Linha 27 — Assign** (nível 1 do bloco).

Associa `email` a a chamada `(email or '').strip().lower`, que converte texto para minúsculas.


**Linha 28 — Assign** (nível 1 do bloco).

Associa `ip` a a chamada `obter_ip`; argumentos posicionais: `request`.


**Linha 29 — Assign** (nível 1 do bloco).

Associa `user_agent` a a chamada `obter_user_agent`; argumentos posicionais: `request`.


**Linha 31 — Expr** (nível 1 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.LOGIN_FALHO`, `resultado=AuditoriaAcaoCritica.Resultado.FALHA`, `descricao='Tentativa de login sem sucesso.'`, `request=request`, `ip=ip`, `user_agent=user_agent`, `metadados={'email': email}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 41 — Assign** (nível 1 do bloco).

Associa `inicio_janela` a a expressão `timezone.now() - timedelta(minutes=JANELA_LOGIN_SUSPEITO_MINUTOS)`; seus operadores determinam o cálculo.

**Linha 42 — Assign** (nível 1 do bloco).

Associa `falhas_recentes` a a chamada `AuditoriaAcaoCritica.objects.filter`, que restringe os resultados às condições informadas; não grava os registros; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.LOGIN_FALHO`, `criado_em__gte=inicio_janela`.

- `acao=AuditoriaAcaoCritica.Acao.LOGIN_FALHO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `criado_em__gte=inicio_janela`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 47 — If** (nível 1 do bloco).

Escolhe um caminho verificando o valor associado ao nome `email`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 47:

**Linha 48 — Assign** (nível 2 do bloco).

Associa `falhas_recentes` a a chamada `falhas_recentes.filter`, que restringe os resultados às condições informadas; não grava os registros; argumentos nomeados: `metadados__email=email`.

- `metadados__email=email`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

Bloco `orelse` da linha 47:

**Linha 49 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `ip`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 49:

**Linha 50 — Assign** (nível 3 do bloco).

Associa `falhas_recentes` a a chamada `falhas_recentes.filter`, que restringe os resultados às condições informadas; não grava os registros; argumentos nomeados: `ip=ip`.

- `ip=ip`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 52 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `falhas_recentes.count()` maior ou igual a `LIMITE_LOGIN_SUSPEITO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 52:

**Linha 53 — Expr** (nível 2 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.LOGIN_SUSPEITO`, `resultado=AuditoriaAcaoCritica.Resultado.FALHA`, `descricao='Muitas tentativas de login falhas em curto periodo.'`, `request=request`, `ip=ip`, `user_agent=user_agent`, `metadados={'email': email, 'falhas_recentes': falhas_recentes.count(), 'janela_minutos': JANELA_LOGIN_SUSPEITO_MINUTOS}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

