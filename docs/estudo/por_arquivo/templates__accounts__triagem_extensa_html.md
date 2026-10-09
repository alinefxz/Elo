# templates/accounts/triagem_extensa.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/triagem_extensa.html](<C:/Users/lb119/Elo/templates/accounts/triagem_extensa.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% block title %}Triagem extensa | Elo{% endblock %}

{% block content %}

<h1>Triagem extensa</h1>

<p>
    Esta triagem é apenas orientativa e não substitui a entrevista,
    os exames ou a decisão da equipe do hemocentro.
</p>

<p>
    Responda com o máximo de precisão possível.
    Quando não souber uma resposta, informe que não sabe.
</p>

<form method="post">

    {% csrf_token %}

    {{ form.non_field_errors }}

    {{ form.as_p }}

    <button type="submit">
        Calcular orientação
    </button>

</form>

<p>
    <a href="{% url 'accounts:dashboard' %}">
        Voltar para o painel
    </a>
</p>

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
{% block title %}Triagem extensa | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 5

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 7

```html
<h1>Triagem extensa</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 9

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 10

```html
    Esta triagem é apenas orientativa e não substitui a entrevista,
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 11

```html
    os exames ou a decisão da equipe do hemocentro.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 12

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 14

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 15

```html
    Responda com o máximo de precisão possível.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 16

```html
    Quando não souber uma resposta, informe que não sabe.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 17

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 19

```html
<form method="post">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 21

```html
    {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 23

```html
    {{ form.non_field_errors }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 25

```html
    {{ form.as_p }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 27

```html
    <button type="submit">
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 28

```html
        Calcular orientação
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 29

```html
    </button>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 31

```html
</form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 33

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 34

```html
    <a href="{% url 'accounts:dashboard' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 35

```html
        Voltar para o painel
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 36

```html
    </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 37

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 39

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

