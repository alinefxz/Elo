# templates/accounts/triagem_resultado.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/triagem_resultado.html](<C:/Users/lb119/Elo/templates/accounts/triagem_resultado.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% block title %}Resultado da triagem | Elo{% endblock %}

{% block content %}

<h1>Resultado da triagem</h1>

<p>
    <strong>Resultado:</strong>
    {{ triagem.get_resultado_display }}
</p>

<p>
    {{ triagem.mensagem_resultado }}
</p>

{% if triagem.data_liberacao %}
    <p>
        <strong>Data orientativa:</strong>
        {{ triagem.data_liberacao|date:"d/m/Y" }}
    </p>
{% endif %}

{% if triagem.achados %}

    <h2>Orientações identificadas</h2>

    <ul>
        {% for achado in triagem.achados %}
            <li>
                {{ achado.mensagem }}

                {% if achado.data_liberacao %}
                    Data orientativa:
                    {{ achado.data_liberacao }}
                {% endif %}
            </li>
        {% endfor %}
    </ul>

{% endif %}

<p>
    Esta orientação foi calculada com a versão:
    {{ triagem.regra_version }}
</p>

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
{% block title %}Resultado da triagem | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 5

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 7

```html
<h1>Resultado da triagem</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 9

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 10

```html
    <strong>Resultado:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 11

```html
    {{ triagem.get_resultado_display }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

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
    {{ triagem.mensagem_resultado }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 16

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 18

```html
{% if triagem.data_liberacao %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 19

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 20

```html
        <strong>Data orientativa:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 21

```html
        {{ triagem.data_liberacao|date:"d/m/Y" }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 22

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 23

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 25

```html
{% if triagem.achados %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 27

```html
    <h2>Orientações identificadas</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 29

```html
    <ul>
```

Abre lista; ul é não numerada e ol é numerada.

### Linha 30

```html
        {% for achado in triagem.achados %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 31

```html
            <li>
```

Define um item da lista.

### Linha 32

```html
                {{ achado.mensagem }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 34

```html
                {% if achado.data_liberacao %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 35

```html
                    Data orientativa:
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 36

```html
                    {{ achado.data_liberacao }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 37

```html
                {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 38

```html
            </li>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 39

```html
        {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 40

```html
    </ul>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 42

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 44

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 45

```html
    Esta orientação foi calculada com a versão:
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 46

```html
    {{ triagem.regra_version }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 47

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 49

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 50

```html
    <a href="{% url 'accounts:dashboard' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 51

```html
        Voltar para o painel
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 52

```html
    </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 53

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 55

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

