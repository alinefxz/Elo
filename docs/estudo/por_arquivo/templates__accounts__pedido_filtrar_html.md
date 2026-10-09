# templates/accounts/pedido_filtrar.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/pedido_filtrar.html](<C:/Users/lb119/Elo/templates/accounts/pedido_filtrar.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% block title %}Consultar pedidos de sangue | Elo{% endblock %}

{% block content %}

<h1>Consultar pedidos de sangue</h1>

<p>
    Utilize os filtros abaixo para encontrar pedidos de sangue ativos.
</p>

<form method="get">

    {{ form.non_field_errors }}

    <p>
        {{ form.tipo_sanguineo.label_tag }}
        {{ form.tipo_sanguineo }}
        {{ form.tipo_sanguineo.errors }}
    </p>

    <p>
        {{ form.urgencia.label_tag }}
        {{ form.urgencia }}
        {{ form.urgencia.errors }}
    </p>

    <p>
        {{ form.cidade.label_tag }}
        {{ form.cidade }}
        {{ form.cidade.errors }}
    </p>

    <p>
        {{ form.hemocentro.label_tag }}
        {{ form.hemocentro }}
        {{ form.hemocentro.errors }}
    </p>

    <p>
        {{ form.data.label_tag }}
        {{ form.data }}
        {{ form.data.errors }}
    </p>

    <p>
        {{ form.status.label_tag }}
        {{ form.status }}
        {{ form.status.errors }}
    </p>

    <button type="submit">
        Filtrar pedidos
    </button>

    <a href="{% url 'accounts:consultar_pedidos' %}">
        Limpar filtros
    </a>

</form>

<hr>

<h2>Pedidos encontrados</h2>

{% if pedidos %}

    {% for pedido in pedidos %}

        <article>
            <h3>{{ pedido.titulo }}</h3>

            <p>
                <strong>Tipo sanguíneo:</strong>
                {{ pedido.tipo_sanguineo }}
            </p>

            <p>
                <strong>Urgência:</strong>
                {{ pedido.get_urgencia_display }}
            </p>

            <p>
                <strong>Cidade:</strong>
                {{ pedido.cidade }}
            </p>

            <p>
                <strong>Hemocentro:</strong>
                {{ pedido.hemocentro_destino.nome }}
            </p>

            <p>
                <strong>Status:</strong>
                {{ pedido.get_status_display }}
            </p>

            <p>
                <strong>Publicado em:</strong>
                {{ pedido.publicado_em|default:pedido.data_criacao|date:"d/m/Y H:i" }}
            </p>

            <p>
                <strong>Descrição:</strong>
                {{ pedido.descricao }}
            </p>
        </article>

        <hr>

    {% endfor %}

{% else %}

    <p>
        Nenhum pedido de sangue encontrado.
    </p>

{% endif %}

<p>
    <a href="{% url 'accounts:dashboard' %}">
        Voltar ao painel
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
{% block title %}Consultar pedidos de sangue | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 5

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 7

```html
<h1>Consultar pedidos de sangue</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 9

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 10

```html
    Utilize os filtros abaixo para encontrar pedidos de sangue ativos.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 11

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 13

```html
<form method="get">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 15

```html
    {{ form.non_field_errors }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 17

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 18

```html
        {{ form.tipo_sanguineo.label_tag }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 19

```html
        {{ form.tipo_sanguineo }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 20

```html
        {{ form.tipo_sanguineo.errors }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 21

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 23

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 24

```html
        {{ form.urgencia.label_tag }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 25

```html
        {{ form.urgencia }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 26

```html
        {{ form.urgencia.errors }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 27

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 29

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 30

```html
        {{ form.cidade.label_tag }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 31

```html
        {{ form.cidade }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 32

```html
        {{ form.cidade.errors }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 33

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 35

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 36

```html
        {{ form.hemocentro.label_tag }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 37

```html
        {{ form.hemocentro }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 38

```html
        {{ form.hemocentro.errors }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 39

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 41

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 42

```html
        {{ form.data.label_tag }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 43

```html
        {{ form.data }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 44

```html
        {{ form.data.errors }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 45

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 47

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 48

```html
        {{ form.status.label_tag }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 49

```html
        {{ form.status }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 50

```html
        {{ form.status.errors }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 51

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 53

```html
    <button type="submit">
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 54

```html
        Filtrar pedidos
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 55

```html
    </button>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 57

```html
    <a href="{% url 'accounts:consultar_pedidos' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 58

```html
        Limpar filtros
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 59

```html
    </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 61

```html
</form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 63

```html
<hr>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 65

```html
<h2>Pedidos encontrados</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 67

```html
{% if pedidos %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 69

```html
    {% for pedido in pedidos %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 71

```html
        <article>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 72

```html
            <h3>{{ pedido.titulo }}</h3>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 74

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 75

```html
                <strong>Tipo sanguíneo:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 76

```html
                {{ pedido.tipo_sanguineo }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 77

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 79

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 80

```html
                <strong>Urgência:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 81

```html
                {{ pedido.get_urgencia_display }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 82

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 84

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 85

```html
                <strong>Cidade:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 86

```html
                {{ pedido.cidade }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 87

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 89

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 90

```html
                <strong>Hemocentro:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 91

```html
                {{ pedido.hemocentro_destino.nome }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 92

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 94

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 95

```html
                <strong>Status:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 96

```html
                {{ pedido.get_status_display }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 97

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 99

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 100

```html
                <strong>Publicado em:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 101

```html
                {{ pedido.publicado_em|default:pedido.data_criacao|date:"d/m/Y H:i" }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 102

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 104

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 105

```html
                <strong>Descrição:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 106

```html
                {{ pedido.descricao }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 107

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 108

```html
        </article>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 110

```html
        <hr>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 112

```html
    {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 114

```html
{% else %}
```

Inicia o caminho alternativo da condição anterior.

### Linha 116

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 117

```html
        Nenhum pedido de sangue encontrado.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 118

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 120

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 122

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 123

```html
    <a href="{% url 'accounts:dashboard' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 124

```html
        Voltar ao painel
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 125

```html
    </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 126

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 128

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

