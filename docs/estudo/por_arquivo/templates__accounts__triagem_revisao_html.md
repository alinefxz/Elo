# templates/accounts/triagem_revisao.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/triagem_revisao.html](<C:/Users/lb119/Elo/templates/accounts/triagem_revisao.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% block title %}Revisão da triagem | Elo{% endblock %}

{% block content %}
<h1>Revise suas respostas</h1>
<p>
    Confira as informações antes de finalizar. O resultado será calculado
    somente após sua confirmação.
</p>
<p><strong>Importante:</strong> esta pré-triagem é orientativa e não substitui a avaliação clínica presencial.</p>

{% for item in respostas_revisao %}
    <section>
        <h2>{{ item.titulo }}</h2>
        <p>{{ item.resposta }}</p>
        {% if item.detalhes %}<p>{{ item.detalhes }}</p>{% endif %}
        <a href="{% url 'accounts:triagem_pergunta' triagem.id_triagem %}?pergunta={{ item.id }}">Editar resposta</a>
    </section>
{% empty %}
    <p>Nenhuma resposta foi salva ainda.</p>
{% endfor %}

<form method="post">
    {% csrf_token %}
    <button type="submit" name="acao" value="finalizar">Finalizar e calcular resultado</button>
</form>
<p><a href="{% url 'accounts:triagem_pergunta' triagem.id_triagem %}">Voltar à triagem</a></p>
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
{% block title %}Revisão da triagem | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 5

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 6

```html
<h1>Revise suas respostas</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 7

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 8

```html
    Confira as informações antes de finalizar. O resultado será calculado
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 9

```html
    somente após sua confirmação.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 10

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 11

```html
<p><strong>Importante:</strong> esta pré-triagem é orientativa e não substitui a avaliação clínica presencial.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 13

```html
{% for item in respostas_revisao %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 14

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 15

```html
        <h2>{{ item.titulo }}</h2>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 16

```html
        <p>{{ item.resposta }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 17

```html
        {% if item.detalhes %}<p>{{ item.detalhes }}</p>{% endif %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota. Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Encerra o bloco de template correspondente, como condição, laço ou comentário. Agrupa conteúdo em um parágrafo.

### Linha 18

```html
        <a href="{% url 'accounts:triagem_pergunta' triagem.id_triagem %}?pergunta={{ item.id }}">Editar resposta</a>
```

Resolve a rota Django pelo nome indicado. Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 19

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 20

```html
{% empty %}
```

Apresenta o caso em que a coleção do laço está vazia.

### Linha 21

```html
    <p>Nenhuma resposta foi salva ainda.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 22

```html
{% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 24

```html
<form method="post">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 25

```html
    {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 26

```html
    <button type="submit" name="acao" value="finalizar">Finalizar e calcular resultado</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 27

```html
</form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 28

```html
<p><a href="{% url 'accounts:triagem_pergunta' triagem.id_triagem %}">Voltar à triagem</a></p>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre. Agrupa conteúdo em um parágrafo.

### Linha 29

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

