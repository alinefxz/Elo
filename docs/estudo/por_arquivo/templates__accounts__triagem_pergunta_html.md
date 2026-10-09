# templates/accounts/triagem_pergunta.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/triagem_pergunta.html](<C:/Users/lb119/Elo/templates/accounts/triagem_pergunta.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% comment %}
Uma pergunta por página deixa o formulário legível. O Django cria os campos
de data e complemento somente quando a regra da pergunta precisa deles.
{% endcomment %}

{% block title %}Pergunta da triagem | Elo{% endblock %}

{% block content %}
<h1>{{ triagem.get_modalidade_display }}</h1>

<p>Triagem {{ triagem.id_triagem }} — Pergunta {{ numero_pergunta }} de {{ total_perguntas }}</p>

<h2>{{ pergunta.titulo }}</h2>
<p>{{ pergunta.explicacao }}</p>

<form method="post">
    {% csrf_token %}
    {{ form.non_field_errors }}

    {% for field in form %}
        <p>
            {{ field.label_tag }}<br>
            {{ field }}
            {% if field.help_text %}<br><small>{{ field.help_text }}</small>{% endif %}
            {% for error in field.errors %}<br>{{ error }}{% endfor %}
        </p>
    {% endfor %}

    {% if numero_pergunta > 1 %}
        <button type="submit" name="acao" value="anterior">Anterior</button>
    {% endif %}
    <button type="submit" name="acao" value="salvar">Salvar e sair</button>
    <button type="submit" name="acao" value="continuar">Continuar</button>
</form>

<p><a href="{% url 'accounts:triagem_historico' %}">Meu histórico de triagens</a></p>
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
Uma pergunta por página deixa o formulário legível. O Django cria os campos
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 5

```html
de data e complemento somente quando a regra da pergunta precisa deles.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 6

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 8

```html
{% block title %}Pergunta da triagem | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 10

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 11

```html
<h1>{{ triagem.get_modalidade_display }}</h1>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 13

```html
<p>Triagem {{ triagem.id_triagem }} — Pergunta {{ numero_pergunta }} de {{ total_perguntas }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 15

```html
<h2>{{ pergunta.titulo }}</h2>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 16

```html
<p>{{ pergunta.explicacao }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 18

```html
<form method="post">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 19

```html
    {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 20

```html
    {{ form.non_field_errors }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 22

```html
    {% for field in form %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 23

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 24

```html
            {{ field.label_tag }}<br>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 25

```html
            {{ field }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 26

```html
            {% if field.help_text %}<br><small>{{ field.help_text }}</small>{% endif %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota. Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 27

```html
            {% for error in field.errors %}<br>{{ error }}{% endfor %}
```

Repete a marcação para cada item da coleção recebida. Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 28

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 29

```html
    {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 31

```html
    {% if numero_pergunta > 1 %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 32

```html
        <button type="submit" name="acao" value="anterior">Anterior</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 33

```html
    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 34

```html
    <button type="submit" name="acao" value="salvar">Salvar e sair</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 35

```html
    <button type="submit" name="acao" value="continuar">Continuar</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 36

```html
</form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 38

```html
<p><a href="{% url 'accounts:triagem_historico' %}">Meu histórico de triagens</a></p>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre. Agrupa conteúdo em um parágrafo.

### Linha 39

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

