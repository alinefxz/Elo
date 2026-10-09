# templates/accounts/pedido_publicar.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/pedido_publicar.html](<C:/Users/lb119/Elo/templates/accounts/pedido_publicar.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% block title %}Solicitar divulgação | Elo{% endblock %}

{% block content %}
<h1>Solicitar divulgação de necessidade</h1>

<p>
    O envio cria uma solicitação. Ela só se torna um pedido público depois da
    análise do Hemocentro de referência.
</p>

<form method="post">
    {% csrf_token %}
    {{ form.non_field_errors }}
    {{ form.as_p }}
    <button type="submit">Enviar para análise</button>
</form>

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
{% block title %}Solicitar divulgação | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 5

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 6

```html
<h1>Solicitar divulgação de necessidade</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 8

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 9

```html
    O envio cria uma solicitação. Ela só se torna um pedido público depois da
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 10

```html
    análise do Hemocentro de referência.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 11

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 13

```html
<form method="post">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 14

```html
    {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 15

```html
    {{ form.non_field_errors }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 16

```html
    {{ form.as_p }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 17

```html
    <button type="submit">Enviar para análise</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 18

```html
</form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 20

```html
<p><a href="{% url 'accounts:dashboard' %}">Voltar ao painel</a></p>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre. Agrupa conteúdo em um parágrafo.

### Linha 21

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

