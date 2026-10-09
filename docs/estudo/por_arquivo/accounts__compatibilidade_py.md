# accounts/compatibilidade.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Tabela, normalizacao, elegibilidade, frequencia e preferencia de convocacao.

**Arquivo original:** [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
TIPOS_SANGUINEOS = ("O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+")

COMPATIBILIDADE_RECEBIMENTO = {
    "O-": ("O-",),
    "O+": ("O-", "O+"),
    "A-": ("O-", "A-"),
    "A+": ("O-", "O+", "A-", "A+"),
    "B-": ("O-", "B-"),
    "B+": ("O-", "O+", "B-", "B+"),
    "AB-": ("O-", "A-", "B-", "AB-"),
    "AB+": TIPOS_SANGUINEOS,
}

POPULACAO_APROXIMADA = {
    "O-": "7%",
    "O+": "38%",
    "A-": "6%",
    "A+": "34%",
    "B-": "2%",
    "B+": "9%",
    "AB-": "1%",
    "AB+": "3%",
}


def normalizar_tipo_sanguineo(tipo_sanguineo):
    tipo = (tipo_sanguineo or "").strip().upper()
    if tipo not in TIPOS_SANGUINEOS:
        raise ValueError("Tipo sanguineo invalido.")
    return tipo


def doadores_compativeis_para(tipo_solicitado):
    tipo = normalizar_tipo_sanguineo(tipo_solicitado)
    return COMPATIBILIDADE_RECEBIMENTO[tipo]


def tipos_que_recebem_de(tipo_doador):
    tipo = normalizar_tipo_sanguineo(tipo_doador)
    return tuple(
        receptor
        for receptor, doadores in COMPATIBILIDADE_RECEBIMENTO.items()
        if tipo in doadores
    )


def tabela_de_compatibilidade():
    return [
        {
            "tipo": tipo,
            "doar_para": tipos_que_recebem_de(tipo),
            "receber_de": doadores_compativeis_para(tipo),
            "populacao": POPULACAO_APROXIMADA[tipo],
        }
        for tipo in TIPOS_SANGUINEOS
    ]


def doadores_aptos_para_convocacao(tipo_solicitado):
    """Aplica a mesma elegibilidade para os alertas de estoque e pedidos."""
    # Imports locais evitam o ciclo: models usa TIPOS_SANGUINEOS deste modulo.
    from django.conf import settings
    from django.db.models import Exists, OuterRef, Q, Subquery
    from django.utils import timezone
    from .models import ConsentimentoLGPD, Triagem, Usuario

    ultima_triagem = Triagem.objects.filter(
        usuario=OuterRef("pk"), status=Triagem.Status.CONCLUIDA,
    ).order_by("-finalizada_em", "-iniciada_em", "-id_triagem")
    consentimento = ConsentimentoLGPD.objects.filter(
        usuario=OuterRef("pk"),
        tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
        versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO,
        aceito=True, revogado_em__isnull=True,
    )
    return (
        Usuario.objects.filter(
            perfil=Usuario.Perfil.DOADOR, is_active=True, suspensa=False,
            aceita_notificacoes_pedidos=True,
            tipo_sanguineo__in=doadores_compativeis_para(tipo_solicitado),
        ).annotate(
            resultado_ultima_triagem=Subquery(ultima_triagem.values("resultado")[:1]),
            liberacao_ultima_triagem=Subquery(ultima_triagem.values("data_liberacao")[:1]),
            consentimento_convocacao=Exists(consentimento),
        ).filter(
            resultado_ultima_triagem=Triagem.Resultado.APTO,
            consentimento_convocacao=True,
        ).filter(
            Q(liberacao_ultima_triagem__isnull=True)
            | Q(liberacao_ultima_triagem__lte=timezone.localdate())
        ).order_by("pk")
    )


def limite_convocacao_atingido(usuario):
    """Soma os alertas de estoque e pedidos, mesmo os que ja foram lidos."""
    from datetime import timedelta
    from django.conf import settings
    from django.utils import timezone
    from .models import Notificacao

    inicio = timezone.now() - timedelta(hours=settings.CONVOCACAO_INTERVALO_HORAS)
    quantidade = Notificacao.objects.filter(
        usuario=usuario,
        tipo__in=[Notificacao.Tipo.ESTOQUE_BAIXO, Notificacao.Tipo.ESTOQUE_CRITICO,
                  Notificacao.Tipo.PEDIDO_COMPATIVEL],
        criada_em__gte=inicio,
    ).count()
    return quantidade >= settings.CONVOCACAO_LIMITE_NOTIFICACOES


def atualizar_preferencia_convocacao(usuario, aceita, request=None):
    """Registra a escolha explicita e sua revogacao nas tabelas existentes."""
    from django.conf import settings
    from django.core.exceptions import PermissionDenied
    from django.db import transaction
    from django.utils import timezone
    from .auditoria import obter_ip, registrar_auditoria
    from .models import AuditoriaAcaoCritica, ConsentimentoLGPD, Usuario

    if not usuario.is_authenticated or usuario.perfil != Usuario.Perfil.DOADOR:
        raise PermissionDenied("Somente Doadores podem configurar convocacoes.")
    with transaction.atomic():
        usuario = Usuario.objects.select_for_update().get(pk=usuario.pk)
        anterior = usuario.aceita_notificacoes_pedidos
        usuario.aceita_notificacoes_pedidos = bool(aceita)
        usuario.save(update_fields=["aceita_notificacoes_pedidos", "atualizado_em"])
        consentimento, criado = ConsentimentoLGPD.objects.get_or_create(
            usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
            versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO,
            defaults={"aceito": bool(aceita), "ip": obter_ip(request),
                      "revogado_em": None if aceita else timezone.now()},
        )
        if not criado:
            if aceita and (not consentimento.aceito or consentimento.revogado_em):
                consentimento.data_aceite = timezone.now()
            consentimento.aceito = bool(aceita)
            consentimento.revogado_em = None if aceita else timezone.now()
            consentimento.ip = obter_ip(request)
            consentimento.save(update_fields=["aceito", "revogado_em", "data_aceite", "ip"])
        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.MODERACAO,
            usuario=usuario, alvo=consentimento, request=request,
            descricao="Preferencia de convocacao atualizada pelo doador.",
            metadados={"evento": "PREFERENCIA_CONVOCACAO", "antes": anterior,
                       "depois": bool(aceita), "versao_termo": consentimento.versao_termo},
        )
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Assign — linhas 1 a 1

```python
TIPOS_SANGUINEOS = ("O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+")
```

**Explicação deste trecho:**

**Linha 1 — Assign** (nível 0 do bloco).

Associa `TIPOS_SANGUINEOS` a uma coleção Tuple com 8 itens, na expressão `('O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+')`.

### Assign — linhas 3 a 12

```python
COMPATIBILIDADE_RECEBIMENTO = {
    "O-": ("O-",),
    "O+": ("O-", "O+"),
    "A-": ("O-", "A-"),
    "A+": ("O-", "O+", "A-", "A+"),
    "B-": ("O-", "B-"),
    "B+": ("O-", "O+", "B-", "B+"),
    "AB-": ("O-", "A-", "B-", "AB-"),
    "AB+": TIPOS_SANGUINEOS,
}
```

**Explicação deste trecho:**

**Linha 3 — Assign** (nível 0 do bloco).

Associa `COMPATIBILIDADE_RECEBIMENTO` a um dicionário de 8 entradas; as chaves dão nome aos valores associados.

- Chave `'O-'`: recebe uma coleção Tuple com 1 itens, na expressão `('O-',)`.
- Chave `'O+'`: recebe uma coleção Tuple com 2 itens, na expressão `('O-', 'O+')`.
- Chave `'A-'`: recebe uma coleção Tuple com 2 itens, na expressão `('O-', 'A-')`.
- Chave `'A+'`: recebe uma coleção Tuple com 4 itens, na expressão `('O-', 'O+', 'A-', 'A+')`.
- Chave `'B-'`: recebe uma coleção Tuple com 2 itens, na expressão `('O-', 'B-')`.
- Chave `'B+'`: recebe uma coleção Tuple com 4 itens, na expressão `('O-', 'O+', 'B-', 'B+')`.
- Chave `'AB-'`: recebe uma coleção Tuple com 4 itens, na expressão `('O-', 'A-', 'B-', 'AB-')`.
- Chave `'AB+'`: recebe o valor associado ao nome `TIPOS_SANGUINEOS`.

### Assign — linhas 14 a 23

```python
POPULACAO_APROXIMADA = {
    "O-": "7%",
    "O+": "38%",
    "A-": "6%",
    "A+": "34%",
    "B-": "2%",
    "B+": "9%",
    "AB-": "1%",
    "AB+": "3%",
}
```

**Explicação deste trecho:**

**Linha 14 — Assign** (nível 0 do bloco).

Associa `POPULACAO_APROXIMADA` a um dicionário de 8 entradas; as chaves dão nome aos valores associados.

- Chave `'O-'`: recebe o valor literal `'7%'`.
- Chave `'O+'`: recebe o valor literal `'38%'`.
- Chave `'A-'`: recebe o valor literal `'6%'`.
- Chave `'A+'`: recebe o valor literal `'34%'`.
- Chave `'B-'`: recebe o valor literal `'2%'`.
- Chave `'B+'`: recebe o valor literal `'9%'`.
- Chave `'AB-'`: recebe o valor literal `'1%'`.
- Chave `'AB+'`: recebe o valor literal `'3%'`.

### normalizar_tipo_sanguineo — linhas 26 a 30

```python
def normalizar_tipo_sanguineo(tipo_sanguineo):
    tipo = (tipo_sanguineo or "").strip().upper()
    if tipo not in TIPOS_SANGUINEOS:
        raise ValueError("Tipo sanguineo invalido.")
    return tipo
```

**Explicação deste trecho:**

**Linha 26 — FunctionDef** (nível 0 do bloco).

Define `normalizar_tipo_sanguineo(tipo_sanguineo)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 26:

**Linha 27 — Assign** (nível 1 do bloco).

Associa `tipo` a a chamada `(tipo_sanguineo or '').strip().upper`, que converte texto para maiúsculas.


**Linha 28 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `tipo` não contido em `TIPOS_SANGUINEOS`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 28:

**Linha 29 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `ValueError`; argumentos posicionais: `'Tipo sanguineo invalido.'`.

**Linha 30 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `tipo` ao chamador.

### doadores_compativeis_para — linhas 33 a 35

```python
def doadores_compativeis_para(tipo_solicitado):
    tipo = normalizar_tipo_sanguineo(tipo_solicitado)
    return COMPATIBILIDADE_RECEBIMENTO[tipo]
```

**Explicação deste trecho:**

**Linha 33 — FunctionDef** (nível 0 do bloco).

Define `doadores_compativeis_para(tipo_solicitado)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 33:

**Linha 34 — Assign** (nível 1 do bloco).

Associa `tipo` a a chamada `normalizar_tipo_sanguineo`; argumentos posicionais: `tipo_solicitado`.


**Linha 35 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o item ou recorte `tipo` de `COMPATIBILIDADE_RECEBIMENTO` ao chamador.

### tipos_que_recebem_de — linhas 38 a 44

```python
def tipos_que_recebem_de(tipo_doador):
    tipo = normalizar_tipo_sanguineo(tipo_doador)
    return tuple(
        receptor
        for receptor, doadores in COMPATIBILIDADE_RECEBIMENTO.items()
        if tipo in doadores
    )
```

**Explicação deste trecho:**

**Linha 38 — FunctionDef** (nível 0 do bloco).

Define `tipos_que_recebem_de(tipo_doador)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 38:

**Linha 39 — Assign** (nível 1 do bloco).

Associa `tipo` a a chamada `normalizar_tipo_sanguineo`; argumentos posicionais: `tipo_doador`.


**Linha 40 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `tuple`; argumentos posicionais: `(receptor for receptor, doadores in COMPATIBILIDADE_RECEBIMENTO.items() if tipo in doadores)` ao chamador.

### tabela_de_compatibilidade — linhas 47 a 56

```python
def tabela_de_compatibilidade():
    return [
        {
            "tipo": tipo,
            "doar_para": tipos_que_recebem_de(tipo),
            "receber_de": doadores_compativeis_para(tipo),
            "populacao": POPULACAO_APROXIMADA[tipo],
        }
        for tipo in TIPOS_SANGUINEOS
    ]
```

**Explicação deste trecho:**

**Linha 47 — FunctionDef** (nível 0 do bloco).

Define `tabela_de_compatibilidade()`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 47:

**Linha 48 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve uma coleção/gerador construído por compreensão em `[{'tipo': tipo, 'doar_para': tipos_que_recebem_de(tipo), 'receber_de': doadores_compativeis_para(tipo), 'populacao': POPULACAO_APROXIMADA[tipo]} for tipo in TIPOS_SANGUINEOS]`: percorre as fontes e aplica os filtros declarados ao chamador.

### doadores_aptos_para_convocacao — linhas 59 a 92

```python
def doadores_aptos_para_convocacao(tipo_solicitado):
    """Aplica a mesma elegibilidade para os alertas de estoque e pedidos."""
    # Imports locais evitam o ciclo: models usa TIPOS_SANGUINEOS deste modulo.
    from django.conf import settings
    from django.db.models import Exists, OuterRef, Q, Subquery
    from django.utils import timezone
    from .models import ConsentimentoLGPD, Triagem, Usuario

    ultima_triagem = Triagem.objects.filter(
        usuario=OuterRef("pk"), status=Triagem.Status.CONCLUIDA,
    ).order_by("-finalizada_em", "-iniciada_em", "-id_triagem")
    consentimento = ConsentimentoLGPD.objects.filter(
        usuario=OuterRef("pk"),
        tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
        versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO,
        aceito=True, revogado_em__isnull=True,
    )
    return (
        Usuario.objects.filter(
            perfil=Usuario.Perfil.DOADOR, is_active=True, suspensa=False,
            aceita_notificacoes_pedidos=True,
            tipo_sanguineo__in=doadores_compativeis_para(tipo_solicitado),
        ).annotate(
            resultado_ultima_triagem=Subquery(ultima_triagem.values("resultado")[:1]),
            liberacao_ultima_triagem=Subquery(ultima_triagem.values("data_liberacao")[:1]),
            consentimento_convocacao=Exists(consentimento),
        ).filter(
            resultado_ultima_triagem=Triagem.Resultado.APTO,
            consentimento_convocacao=True,
        ).filter(
            Q(liberacao_ultima_triagem__isnull=True)
            | Q(liberacao_ultima_triagem__lte=timezone.localdate())
        ).order_by("pk")
    )
```

**Explicação deste trecho:**

**Linha 59 — FunctionDef** (nível 0 do bloco).

Define `doadores_aptos_para_convocacao(tipo_solicitado)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 59:

**Linha 60 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 62 — ImportFrom** (nível 1 do bloco).

Importa de `django.conf` os nomes `settings`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 63 — ImportFrom** (nível 1 do bloco).

Importa de `django.db.models` os nomes `Exists`, `OuterRef`, `Q`, `Subquery`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 64 — ImportFrom** (nível 1 do bloco).

Importa de `django.utils` os nomes `timezone`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 65 — ImportFrom** (nível 1 do bloco).

Importa de `.models` os nomes `ConsentimentoLGPD`, `Triagem`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 67 — Assign** (nível 1 do bloco).

Associa `ultima_triagem` a a chamada `Triagem.objects.filter(usuario=OuterRef('pk'), status=Triagem.Status.CONCLUIDA).order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'-finalizada_em'`, `'-iniciada_em'`, `'-id_triagem'`.


**Linha 70 — Assign** (nível 1 do bloco).

Associa `consentimento` a a chamada `ConsentimentoLGPD.objects.filter`, que restringe os resultados às condições informadas; não grava os registros; argumentos nomeados: `usuario=OuterRef('pk')`, `tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES`, `versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO`, `aceito=True`, `revogado_em__isnull=True`.

- `usuario=OuterRef('pk')`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `aceito=True`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `revogado_em__isnull=True`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 76 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a chamada `Usuario.objects.filter(perfil=Usuario.Perfil.DOADOR, is_active=True, suspensa=False, aceita_notificacoes_pedidos=True, tipo_sanguineo__in=doadores_compativeis_para(tipo_solicitado)).annotate(resultado_ultima_triagem=Subquery(ultima_triagem.values('resultado')[:1]), liberacao_ultima_triagem=Subquery(ultima_triagem.values('data_liberacao')[:1]), consentimento_convocacao=Exists(consentimento)).filter(resultado_ultima_triagem=Triagem.Resultado.APTO, consentimento_convocacao=True).filter(Q(liberacao_ultima_triagem__isnull=True) | Q(liberacao_ultima_triagem__lte=timezone.localdate())).order_by`, que define a ordem; prefixo menos significa ordem descendente; argumentos posicionais: `'pk'` ao chamador.

### limite_convocacao_atingido — linhas 95 a 109

```python
def limite_convocacao_atingido(usuario):
    """Soma os alertas de estoque e pedidos, mesmo os que ja foram lidos."""
    from datetime import timedelta
    from django.conf import settings
    from django.utils import timezone
    from .models import Notificacao

    inicio = timezone.now() - timedelta(hours=settings.CONVOCACAO_INTERVALO_HORAS)
    quantidade = Notificacao.objects.filter(
        usuario=usuario,
        tipo__in=[Notificacao.Tipo.ESTOQUE_BAIXO, Notificacao.Tipo.ESTOQUE_CRITICO,
                  Notificacao.Tipo.PEDIDO_COMPATIVEL],
        criada_em__gte=inicio,
    ).count()
    return quantidade >= settings.CONVOCACAO_LIMITE_NOTIFICACOES
```

**Explicação deste trecho:**

**Linha 95 — FunctionDef** (nível 0 do bloco).

Define `limite_convocacao_atingido(usuario)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 95:

**Linha 96 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 97 — ImportFrom** (nível 1 do bloco).

Importa de `datetime` os nomes `timedelta`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 98 — ImportFrom** (nível 1 do bloco).

Importa de `django.conf` os nomes `settings`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 99 — ImportFrom** (nível 1 do bloco).

Importa de `django.utils` os nomes `timezone`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 100 — ImportFrom** (nível 1 do bloco).

Importa de `.models` os nomes `Notificacao`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 102 — Assign** (nível 1 do bloco).

Associa `inicio` a a expressão `timezone.now() - timedelta(hours=settings.CONVOCACAO_INTERVALO_HORAS)`; seus operadores determinam o cálculo.

**Linha 103 — Assign** (nível 1 do bloco).

Associa `quantidade` a a chamada `Notificacao.objects.filter(usuario=usuario, tipo__in=[Notificacao.Tipo.ESTOQUE_BAIXO, Notificacao.Tipo.ESTOQUE_CRITICO, Notificacao.Tipo.PEDIDO_COMPATIVEL], criada_em__gte=inicio).count`, que conta os resultados.


**Linha 109 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve a comparação `quantidade` maior ou igual a `settings.CONVOCACAO_LIMITE_NOTIFICACOES` ao chamador.

### atualizar_preferencia_convocacao — linhas 112 a 147

```python
def atualizar_preferencia_convocacao(usuario, aceita, request=None):
    """Registra a escolha explicita e sua revogacao nas tabelas existentes."""
    from django.conf import settings
    from django.core.exceptions import PermissionDenied
    from django.db import transaction
    from django.utils import timezone
    from .auditoria import obter_ip, registrar_auditoria
    from .models import AuditoriaAcaoCritica, ConsentimentoLGPD, Usuario

    if not usuario.is_authenticated or usuario.perfil != Usuario.Perfil.DOADOR:
        raise PermissionDenied("Somente Doadores podem configurar convocacoes.")
    with transaction.atomic():
        usuario = Usuario.objects.select_for_update().get(pk=usuario.pk)
        anterior = usuario.aceita_notificacoes_pedidos
        usuario.aceita_notificacoes_pedidos = bool(aceita)
        usuario.save(update_fields=["aceita_notificacoes_pedidos", "atualizado_em"])
        consentimento, criado = ConsentimentoLGPD.objects.get_or_create(
            usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
            versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO,
            defaults={"aceito": bool(aceita), "ip": obter_ip(request),
                      "revogado_em": None if aceita else timezone.now()},
        )
        if not criado:
            if aceita and (not consentimento.aceito or consentimento.revogado_em):
                consentimento.data_aceite = timezone.now()
            consentimento.aceito = bool(aceita)
            consentimento.revogado_em = None if aceita else timezone.now()
            consentimento.ip = obter_ip(request)
            consentimento.save(update_fields=["aceito", "revogado_em", "data_aceite", "ip"])
        registrar_auditoria(
            acao=AuditoriaAcaoCritica.Acao.MODERACAO,
            usuario=usuario, alvo=consentimento, request=request,
            descricao="Preferencia de convocacao atualizada pelo doador.",
            metadados={"evento": "PREFERENCIA_CONVOCACAO", "antes": anterior,
                       "depois": bool(aceita), "versao_termo": consentimento.versao_termo},
        )
```

**Explicação deste trecho:**

**Linha 112 — FunctionDef** (nível 0 do bloco).

Define `atualizar_preferencia_convocacao(usuario, aceita, request=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 112:

**Linha 113 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 114 — ImportFrom** (nível 1 do bloco).

Importa de `django.conf` os nomes `settings`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 115 — ImportFrom** (nível 1 do bloco).

Importa de `django.core.exceptions` os nomes `PermissionDenied`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 116 — ImportFrom** (nível 1 do bloco).

Importa de `django.db` os nomes `transaction`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 117 — ImportFrom** (nível 1 do bloco).

Importa de `django.utils` os nomes `timezone`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 118 — ImportFrom** (nível 1 do bloco).

Importa de `.auditoria` os nomes `obter_ip`, `registrar_auditoria`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 119 — ImportFrom** (nível 1 do bloco).

Importa de `.models` os nomes `AuditoriaAcaoCritica`, `ConsentimentoLGPD`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 121 — If** (nível 1 do bloco).

Escolhe um caminho verificando pelo menos uma das condições: `not usuario.is_authenticated` ; `usuario.perfil != Usuario.Perfil.DOADOR` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 121:

**Linha 122 — Raise** (nível 2 do bloco).

Interrompe o caminho levantando a chamada `PermissionDenied`; argumentos posicionais: `'Somente Doadores podem configurar convocacoes.'`.

**Linha 123 — With** (nível 1 do bloco).

Executa sob os contextos `transaction.atomic()`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 123:

**Linha 124 — Assign** (nível 2 do bloco).

Associa `usuario` a a chamada `Usuario.objects.select_for_update().get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `pk=usuario.pk`.

- `pk=usuario.pk`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 125 — Assign** (nível 2 do bloco).

Associa `anterior` a o atributo `aceita_notificacoes_pedidos` de `usuario`.

**Linha 126 — Assign** (nível 2 do bloco).

Associa `usuario.aceita_notificacoes_pedidos` a a chamada `bool`; argumentos posicionais: `aceita`.


**Linha 127 — Expr** (nível 2 do bloco).

Executa a chamada `usuario.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['aceita_notificacoes_pedidos', 'atualizado_em']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 128 — Assign** (nível 2 do bloco).

Associa `(consentimento, criado)` a a chamada `ConsentimentoLGPD.objects.get_or_create`, que procura pelas chaves; se não existir, cria usando também defaults; argumentos nomeados: `usuario=usuario`, `tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES`, `versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO`, `defaults={'aceito': bool(aceita), 'ip': obter_ip(request), 'revogado_em': None if aceita else timezone.now()}`.

- `usuario=usuario`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `defaults={'aceito': bool(aceita), 'ip': obter_ip(request), 'revogado_em': None if aceita else timezone.now()}`: valores adicionais usados na criação/atualização.

**Linha 134 — If** (nível 2 do bloco).

Escolhe um caminho verificando a negação de `criado`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 134:

**Linha 135 — If** (nível 3 do bloco).

Escolhe um caminho verificando todas as condições: `aceita` ; `not consentimento.aceito or consentimento.revogado_em` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 135:

**Linha 136 — Assign** (nível 4 do bloco).

Associa `consentimento.data_aceite` a a chamada `timezone.now`, que obtém o instante atual; timezone.now respeita o tratamento de fuso do Django.


**Linha 137 — Assign** (nível 3 do bloco).

Associa `consentimento.aceito` a a chamada `bool`; argumentos posicionais: `aceita`.


**Linha 138 — Assign** (nível 3 do bloco).

Associa `consentimento.revogado_em` a `None` se `aceita` for verdadeiro; caso contrário, `timezone.now()`.

**Linha 139 — Assign** (nível 3 do bloco).

Associa `consentimento.ip` a a chamada `obter_ip`; argumentos posicionais: `request`.


**Linha 140 — Expr** (nível 3 do bloco).

Executa a chamada `consentimento.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['aceito', 'revogado_em', 'data_aceite', 'ip']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 141 — Expr** (nível 2 do bloco).

Executa a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.MODERACAO`, `usuario=usuario`, `alvo=consentimento`, `request=request`, `descricao='Preferencia de convocacao atualizada pelo doador.'`, `metadados={'evento': 'PREFERENCIA_CONVOCACAO', 'antes': anterior, 'depois': bool(aceita), 'versao_termo': consentimento.versao_termo}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 61: `# Imports locais evitam o ciclo: models usa TIPOS_SANGUINEOS deste modulo.`

