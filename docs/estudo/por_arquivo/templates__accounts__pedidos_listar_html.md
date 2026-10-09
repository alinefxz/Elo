# templates/accounts/pedidos_listar.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/pedidos_listar.html](<C:/Users/lb119/Elo/templates/accounts/pedidos_listar.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% comment %}
Lista pública de pedidos de sangue que já foram aprovados.

A view envia:
- form: formulário de filtros;
- pedidos: somente pedidos publicados.

Pedidos pendentes, suspeitos ou recusados
não aparecem nesta página.
{% endcomment %}

{% block title %}Pedidos de sangue | Elo{% endblock %}

{% block content %}

<h1>Pedidos de sangue ativos</h1>

<form method="get">
    {{ form.as_p }}

    <button type="submit">
        Filtrar pedidos
    </button>

    <a href="{% url 'accounts:consultar_pedidos' %}">
        Limpar filtros
    </a>
</form>

<hr>

<h2>Pedidos encontrados</h2>

{% for pedido in pedidos %}

    <section>
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
            <strong>Descrição:</strong>
            {{ pedido.descricao }}
        </p>

        <p>
            <strong>Status:</strong>
            {{ pedido.get_status_display }}
        </p>

        <p>
            <strong>Publicado em:</strong>
            {{ pedido.publicado_em|default:pedido.data_criacao|date:"d/m/Y H:i" }}
        </p>
    </section>

{% empty %}

    <p>
        Nenhum pedido ativo encontrado.
    </p>

{% endfor %}

{% if user.is_authenticated %}
    {% if user.perfil == "RECEPTOR" %}
        <p>
            <a href="{% url 'accounts:criar_pedido_sangue' %}">
                Solicitar divulgação de necessidade
            </a>
        </p>
    {% endif %}
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
{% comment %}
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 4

```html
Lista pública de pedidos de sangue que já foram aprovados.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 6

```html
A view envia:
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 7

```html
- form: formulário de filtros;
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 8

```html
- pedidos: somente pedidos publicados.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 10

```html
Pedidos pendentes, suspeitos ou recusados
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 11

```html
não aparecem nesta página.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 12

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 14

```html
{% block title %}Pedidos de sangue | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 16

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 18

```html
<h1>Pedidos de sangue ativos</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 20

```html
<form method="get">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 21

```html
    {{ form.as_p }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 23

```html
    <button type="submit">
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 24

```html
        Filtrar pedidos
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 25

```html
    </button>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 27

```html
    <a href="{% url 'accounts:consultar_pedidos' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 28

```html
        Limpar filtros
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 29

```html
    </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 30

```html
</form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 32

```html
<hr>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 34

```html
<h2>Pedidos encontrados</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 36

```html
{% for pedido in pedidos %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 38

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 39

```html
        <h3>{{ pedido.titulo }}</h3>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 41

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 42

```html
            <strong>Tipo sanguíneo:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 43

```html
            {{ pedido.tipo_sanguineo }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 44

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 46

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 47

```html
            <strong>Urgência:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 48

```html
            {{ pedido.get_urgencia_display }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 49

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 51

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 52

```html
            <strong>Cidade:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 53

```html
            {{ pedido.cidade }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 54

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 56

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 57

```html
            <strong>Hemocentro:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 58

```html
            {{ pedido.hemocentro_destino.nome }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 59

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 61

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 62

```html
            <strong>Descrição:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 63

```html
            {{ pedido.descricao }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 64

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 66

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 67

```html
            <strong>Status:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 68

```html
            {{ pedido.get_status_display }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 69

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 71

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 72

```html
            <strong>Publicado em:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 73

```html
            {{ pedido.publicado_em|default:pedido.data_criacao|date:"d/m/Y H:i" }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 74

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 75

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 77

```html
{% empty %}
```

Apresenta o caso em que a coleção do laço está vazia.

### Linha 79

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 80

```html
        Nenhum pedido ativo encontrado.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 81

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 83

```html
{% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 85

```html
{% if user.is_authenticated %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 86

```html
    {% if user.perfil == "RECEPTOR" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 87

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 88

```html
            <a href="{% url 'accounts:criar_pedido_sangue' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 89

```html
                Solicitar divulgação de necessidade
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 90

```html
            </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 91

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 92

```html
    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 93

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 95

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 96

```html
    <a href="{% url 'accounts:dashboard' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 97

```html
        Voltar ao painel
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 98

```html
    </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 99

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 101

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

