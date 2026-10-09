# templates/accounts/painel_moderacao_pedidos.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/painel_moderacao_pedidos.html](<C:/Users/lb119/Elo/templates/accounts/painel_moderacao_pedidos.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% block title %}Moderação de pedidos | Elo{% endblock %}

{% block content %}
<h1>Moderação de pedidos de sangue</h1>
<p>
    O Administrador acompanha validações e suspeitas. A publicação oficial
    continua sendo responsabilidade exclusiva do Hemocentro aprovado.
</p>

<form method="get">
    <label for="status">Filtrar por status:</label>
    <select id="status" name="status">
        <option value="">Todos</option>
        {% for codigo, nome in status_opcoes %}
            <option value="{{ codigo }}" {% if status_atual == codigo %}selected{% endif %}>
                {{ nome }}
            </option>
        {% endfor %}
    </select>
    <button type="submit">Filtrar</button>
</form>

<p>
    <a href="{% url 'accounts:dashboard' %}">Voltar ao painel</a>
    · <a href="{% url 'accounts:painel_aprovacao_hemocentros' %}">Validar Hemocentros</a>
</p>

{% for pedido in pedidos %}
    <section>
        <h2>{{ pedido.titulo }}</h2>
        <p><strong>Protocolo:</strong> {{ pedido.id_pedido }}</p>
        <p><strong>Solicitante:</strong> {{ pedido.nome_solicitante }}</p>
        <p><strong>Contato:</strong> {{ pedido.contato }}</p>
        <p><strong>Hemocentro:</strong> {{ pedido.hemocentro_destino.nome }}</p>
        <p><strong>Tipo:</strong> {{ pedido.tipo_sanguineo }}</p>
        <p><strong>Cidade:</strong> {{ pedido.cidade }}</p>
        <p><strong>Urgência:</strong> {{ pedido.get_urgencia_display }}</p>
        <p><strong>Status:</strong> {{ pedido.get_status_display }}</p>
        <p><strong>Descrição:</strong> {{ pedido.descricao }}</p>

        {% if pedido.duplicidade_suspeita %}
            <p><strong>Atenção:</strong> foi encontrada solicitação semelhante no período de validação.</p>
        {% endif %}

        {% with ultima_validacao=pedido.validacoes.all.0 %}
            {% if ultima_validacao %}
                <p>
                    <strong>Última moderação:</strong>
                    {{ ultima_validacao.get_status_validacao_display }}
                    — {{ ultima_validacao.motivo }}
                </p>
            {% endif %}
        {% endwith %}

        {% if pedido.status != "ENCERRADA" %}
            <form method="post" action="{% url 'accounts:marcar_pedido_suspeito' pedido.id_pedido %}">
                {% csrf_token %}
                <textarea name="motivo" rows="2" required placeholder="Explique o motivo da suspeita ou da auditoria"></textarea>
                <button type="submit">Marcar como suspeito</button>
            </form>
        {% endif %}
    </section>
{% empty %}
    <p>Nenhum pedido pendente ou suspeito para moderação.</p>
{% endfor %}
{% endblock %}
``````

## Leitura da tela, linha por linha

### Linha 1

```html
{% extends "base.html" %}
```

Herda a estrutura do template-base indicado.

### Linha 3

```html
{% block title %}Moderação de pedidos | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 5

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 6

```html
<h1>Moderação de pedidos de sangue</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 7

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 8

```html
    O Administrador acompanha validações e suspeitas. A publicação oficial
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 9

```html
    continua sendo responsabilidade exclusiva do Hemocentro aprovado.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 10

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 12

```html
<form method="get">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 13

```html
    <label for="status">Filtrar por status:</label>
```

Apresenta o rótulo de um campo; for liga ao id do controle.

### Linha 14

```html
    <select id="status" name="status">
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 15

```html
        <option value="">Todos</option>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 16

```html
        {% for codigo, nome in status_opcoes %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 17

```html
            <option value="{{ codigo }}" {% if status_atual == codigo %}selected{% endif %}>
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota. Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 18

```html
                {{ nome }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 19

```html
            </option>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 20

```html
        {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 21

```html
    </select>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 22

```html
    <button type="submit">Filtrar</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 23

```html
</form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 25

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 26

```html
    <a href="{% url 'accounts:dashboard' %}">Voltar ao painel</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 27

```html
    · <a href="{% url 'accounts:painel_aprovacao_hemocentros' %}">Validar Hemocentros</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 28

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 30

```html
{% for pedido in pedidos %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 31

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 32

```html
        <h2>{{ pedido.titulo }}</h2>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 33

```html
        <p><strong>Protocolo:</strong> {{ pedido.id_pedido }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 34

```html
        <p><strong>Solicitante:</strong> {{ pedido.nome_solicitante }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 35

```html
        <p><strong>Contato:</strong> {{ pedido.contato }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 36

```html
        <p><strong>Hemocentro:</strong> {{ pedido.hemocentro_destino.nome }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 37

```html
        <p><strong>Tipo:</strong> {{ pedido.tipo_sanguineo }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 38

```html
        <p><strong>Cidade:</strong> {{ pedido.cidade }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 39

```html
        <p><strong>Urgência:</strong> {{ pedido.get_urgencia_display }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 40

```html
        <p><strong>Status:</strong> {{ pedido.get_status_display }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 41

```html
        <p><strong>Descrição:</strong> {{ pedido.descricao }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 43

```html
        {% if pedido.duplicidade_suspeita %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 44

```html
            <p><strong>Atenção:</strong> foi encontrada solicitação semelhante no período de validação.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 45

```html
        {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 47

```html
        {% with ultima_validacao=pedido.validacoes.all.0 %}
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 48

```html
            {% if ultima_validacao %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 49

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 50

```html
                    <strong>Última moderação:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 51

```html
                    {{ ultima_validacao.get_status_validacao_display }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 52

```html
                    — {{ ultima_validacao.motivo }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 53

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 54

```html
            {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 55

```html
        {% endwith %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 57

```html
        {% if pedido.status != "ENCERRADA" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 58

```html
            <form method="post" action="{% url 'accounts:marcar_pedido_suspeito' pedido.id_pedido %}">
```

Resolve a rota Django pelo nome indicado. Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 59

```html
                {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 60

```html
                <textarea name="motivo" rows="2" required placeholder="Explique o motivo da suspeita ou da auditoria"></textarea>
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 61

```html
                <button type="submit">Marcar como suspeito</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 62

```html
            </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 63

```html
        {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 64

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 65

```html
{% empty %}
```

Apresenta o caso em que a coleção do laço está vazia.

### Linha 66

```html
    <p>Nenhum pedido pendente ou suspeito para moderação.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 67

```html
{% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 68

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

