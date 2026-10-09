# templates/accounts/triagem_historico.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/triagem_historico.html](<C:/Users/lb119/Elo/templates/accounts/triagem_historico.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% comment %}
O queryset desta página já pertence ao usuário autenticado. A listagem mostra
somente o resumo; respostas individuais continuam protegidas no banco.
{% endcomment %}

{% block title %}Meu histórico de triagens | Elo{% endblock %}

{% block content %}
<h1>Meu histórico de triagens</h1>

{% if triagens %}
    <ul>
        {% for triagem in triagens %}
            <li>
                <strong>Triagem {{ triagem.id_triagem }} — {{ triagem.get_modalidade_display }}</strong><br>
                Iniciada em {{ triagem.iniciada_em|date:"d/m/Y H:i" }}<br>
                Situação: {{ triagem.get_status_display }}
                <br>Versão das regras: {{ triagem.regra_version }}

                {% if triagem.status == "CONCLUIDA" %}
                    <br>Orientação: {{ triagem.get_resultado_display }}
                    <br><a href="{% url 'accounts:triagem_resultado' id_triagem=triagem.id_triagem %}">Ver resultado</a>
                {% elif triagem.status == "EM_ANDAMENTO" %}
                    <br><a href="{% url 'accounts:triagem_pergunta' id_triagem=triagem.id_triagem %}">Continuar triagem</a>
                {% endif %}
            </li>
        {% endfor %}
    </ul>
{% else %}
    <p>Você ainda não iniciou uma triagem.</p>
{% endif %}

<p><a href="{% url 'accounts:triagem_apresentacao' %}">Escolher uma triagem</a></p>
<p><a href="{% url 'accounts:dashboard' %}">Voltar para o painel</a></p>
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
O queryset desta página já pertence ao usuário autenticado. A listagem mostra
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 5

```html
somente o resumo; respostas individuais continuam protegidas no banco.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 6

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 8

```html
{% block title %}Meu histórico de triagens | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 10

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 11

```html
<h1>Meu histórico de triagens</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 13

```html
{% if triagens %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 14

```html
    <ul>
```

Abre lista; ul é não numerada e ol é numerada.

### Linha 15

```html
        {% for triagem in triagens %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 16

```html
            <li>
```

Define um item da lista.

### Linha 17

```html
                <strong>Triagem {{ triagem.id_triagem }} — {{ triagem.get_modalidade_display }}</strong><br>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 18

```html
                Iniciada em {{ triagem.iniciada_em|date:"d/m/Y H:i" }}<br>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 19

```html
                Situação: {{ triagem.get_status_display }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 20

```html
                <br>Versão das regras: {{ triagem.regra_version }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 22

```html
                {% if triagem.status == "CONCLUIDA" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 23

```html
                    <br>Orientação: {{ triagem.get_resultado_display }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 24

```html
                    <br><a href="{% url 'accounts:triagem_resultado' id_triagem=triagem.id_triagem %}">Ver resultado</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 25

```html
                {% elif triagem.status == "EM_ANDAMENTO" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 26

```html
                    <br><a href="{% url 'accounts:triagem_pergunta' id_triagem=triagem.id_triagem %}">Continuar triagem</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 27

```html
                {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 28

```html
            </li>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 29

```html
        {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 30

```html
    </ul>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 31

```html
{% else %}
```

Inicia o caminho alternativo da condição anterior.

### Linha 32

```html
    <p>Você ainda não iniciou uma triagem.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 33

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 35

```html
<p><a href="{% url 'accounts:triagem_apresentacao' %}">Escolher uma triagem</a></p>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre. Agrupa conteúdo em um parágrafo.

### Linha 36

```html
<p><a href="{% url 'accounts:dashboard' %}">Voltar para o painel</a></p>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre. Agrupa conteúdo em um parágrafo.

### Linha 37

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

