# templates/accounts/pedido_detalhe.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/pedido_detalhe.html](<C:/Users/lb119/Elo/templates/accounts/pedido_detalhe.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% block title %}Pedido de sangue registrado | Elo{% endblock %}

{% block content %}
<h1>Pedido de sangue registrado</h1>

<p>
    Seu pedido foi registrado e está aguardando validação.
</p>

<dl>
    <dt>Para quem</dt>
    <dd>{{ pedido.get_para_quem_display }}</dd>

    <dt>Tipo solicitado</dt>
    <dd>{{ pedido.tipo_sanguineo }}</dd>

    <dt>Hemocentro</dt>
    <dd>{{ pedido.hemocentro.nome }}</dd>

    <dt>Cidade</dt>
    <dd>{{ pedido.cidade }}{% if pedido.hemocentro.estado %} - {{ pedido.hemocentro.estado }}{% endif %}</dd>

    <dt>Urgência</dt>
    <dd>{{ pedido.get_urgencia_display }}</dd>

    {% if pedido.nome_paciente %}
        <dt>Nome da pessoa</dt>
        <dd>{{ pedido.nome_paciente }}</dd>
    {% endif %}

    <dt>Descrição</dt>
    <dd>{{ pedido.descricao }}</dd>

    <dt>Status</dt>
    <dd>{{ pedido.get_status_display }}</dd>

    <dt>Data</dt>
    <dd>{{ pedido.data_criacao|date:"d/m/Y H:i" }}</dd>
</dl>

<p><a href="{% url 'accounts:dashboard' %}">Voltar ao início</a></p>
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
{% block title %}Pedido de sangue registrado | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 5

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 6

```html
<h1>Pedido de sangue registrado</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 8

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 9

```html
    Seu pedido foi registrado e está aguardando validação.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 10

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 12

```html
<dl>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 13

```html
    <dt>Para quem</dt>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 14

```html
    <dd>{{ pedido.get_para_quem_display }}</dd>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 16

```html
    <dt>Tipo solicitado</dt>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 17

```html
    <dd>{{ pedido.tipo_sanguineo }}</dd>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 19

```html
    <dt>Hemocentro</dt>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 20

```html
    <dd>{{ pedido.hemocentro.nome }}</dd>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 22

```html
    <dt>Cidade</dt>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 23

```html
    <dd>{{ pedido.cidade }}{% if pedido.hemocentro.estado %} - {{ pedido.hemocentro.estado }}{% endif %}</dd>
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota. Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 25

```html
    <dt>Urgência</dt>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 26

```html
    <dd>{{ pedido.get_urgencia_display }}</dd>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 28

```html
    {% if pedido.nome_paciente %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 29

```html
        <dt>Nome da pessoa</dt>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 30

```html
        <dd>{{ pedido.nome_paciente }}</dd>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 31

```html
    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 33

```html
    <dt>Descrição</dt>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 34

```html
    <dd>{{ pedido.descricao }}</dd>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 36

```html
    <dt>Status</dt>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 37

```html
    <dd>{{ pedido.get_status_display }}</dd>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 39

```html
    <dt>Data</dt>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 40

```html
    <dd>{{ pedido.data_criacao|date:"d/m/Y H:i" }}</dd>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 41

```html
</dl>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 43

```html
<p><a href="{% url 'accounts:dashboard' %}">Voltar ao início</a></p>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre. Agrupa conteúdo em um parágrafo.

### Linha 44

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

