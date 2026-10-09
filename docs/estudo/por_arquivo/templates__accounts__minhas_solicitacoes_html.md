# templates/accounts/minhas_solicitacoes.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/minhas_solicitacoes.html](<C:/Users/lb119/Elo/templates/accounts/minhas_solicitacoes.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% block title %}Minhas solicitações | Elo{% endblock %}

{% block content %}
<h1>Minhas solicitações de divulgação</h1>

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

{% for solicitacao in solicitacoes %}
    <section>
        <h2>{{ solicitacao.titulo }}</h2>
        <p><strong>Protocolo:</strong> {{ solicitacao.id_pedido }}</p>
        <p><strong>Tipo:</strong> {{ solicitacao.tipo_sanguineo }}</p>
        <p><strong>Cidade:</strong> {{ solicitacao.cidade }}</p>
        <p><strong>Hemocentro:</strong> {{ solicitacao.hemocentro_destino.nome }}</p>
        <p><strong>Status:</strong> {{ solicitacao.get_status_display }}</p>
       <p><strong>Enviada em:</strong> {{ solicitacao.data_criacao|date:"d/m/Y H:i" }}</p>

        {% with ultima_validacao=solicitacao.validacoes.all.0 %}
            {% if ultima_validacao %}
                <p>
                    <strong>Última análise:</strong>
                    {{ ultima_validacao.get_status_validacao_display }}
                </p>
                {% if ultima_validacao.motivo %}
                    <p><strong>Orientação:</strong> {{ ultima_validacao.motivo }}</p>
                {% endif %}
            {% endif %}
        {% endwith %}
    </section>
{% empty %}
    <p>Você ainda não enviou uma solicitação.</p>
{% endfor %}

<p><a href="{% url 'accounts:pedido_publicar' %}">Enviar nova solicitação</a></p>
<p><a href="{% url 'accounts:dashboard' %}">Voltar ao painel</a></p>
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
{% block title %}Minhas solicitações | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 5

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 6

```html
<h1>Minhas solicitações de divulgação</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 8

```html
<form method="get">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 9

```html
    <label for="status">Filtrar por status:</label>
```

Apresenta o rótulo de um campo; for liga ao id do controle.

### Linha 10

```html
    <select id="status" name="status">
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 11

```html
        <option value="">Todos</option>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 12

```html
        {% for codigo, nome in status_opcoes %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 13

```html
            <option value="{{ codigo }}" {% if status_atual == codigo %}selected{% endif %}>
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota. Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 14

```html
                {{ nome }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 15

```html
            </option>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 16

```html
        {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 17

```html
    </select>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 18

```html
    <button type="submit">Filtrar</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 19

```html
</form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 21

```html
{% for solicitacao in solicitacoes %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 22

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 23

```html
        <h2>{{ solicitacao.titulo }}</h2>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 24

```html
        <p><strong>Protocolo:</strong> {{ solicitacao.id_pedido }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 25

```html
        <p><strong>Tipo:</strong> {{ solicitacao.tipo_sanguineo }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 26

```html
        <p><strong>Cidade:</strong> {{ solicitacao.cidade }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 27

```html
        <p><strong>Hemocentro:</strong> {{ solicitacao.hemocentro_destino.nome }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 28

```html
        <p><strong>Status:</strong> {{ solicitacao.get_status_display }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 29

```html
       <p><strong>Enviada em:</strong> {{ solicitacao.data_criacao|date:"d/m/Y H:i" }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 31

```html
        {% with ultima_validacao=solicitacao.validacoes.all.0 %}
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 32

```html
            {% if ultima_validacao %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 33

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 34

```html
                    <strong>Última análise:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 35

```html
                    {{ ultima_validacao.get_status_validacao_display }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 36

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 37

```html
                {% if ultima_validacao.motivo %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 38

```html
                    <p><strong>Orientação:</strong> {{ ultima_validacao.motivo }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 39

```html
                {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 40

```html
            {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 41

```html
        {% endwith %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 42

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 43

```html
{% empty %}
```

Apresenta o caso em que a coleção do laço está vazia.

### Linha 44

```html
    <p>Você ainda não enviou uma solicitação.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 45

```html
{% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 47

```html
<p><a href="{% url 'accounts:pedido_publicar' %}">Enviar nova solicitação</a></p>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre. Agrupa conteúdo em um parágrafo.

### Linha 48

```html
<p><a href="{% url 'accounts:dashboard' %}">Voltar ao painel</a></p>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre. Agrupa conteúdo em um parágrafo.

### Linha 49

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

