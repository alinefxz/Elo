# templates/accounts/login.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/login.html](<C:/Users/lb119/Elo/templates/accounts/login.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% comment %}
RESUMO DO ARQUIVO
=================
Tela de login por e-mail e senha. LoginView fornece o objeto ``form`` e processa
a autenticacao usando o model configurado em AUTH_USER_MODEL.
{% endcomment %}

{% block title %}Entrar | Elo{% endblock %}

{% block content %}
<h1>Entrar</h1>

<form method="post">
    {% csrf_token %}

    <!-- Exibe e-mail, senha e eventuais erros de autenticacao. -->
    {{ form.as_p }}

    {% if next %}
        <!-- Quando login_required enviou a pessoa para o login, next guarda a
             pagina original para que ela possa retornar depois de entrar. -->
        <input type="hidden" name="next" value="{{ next }}">
    {% endif %}

    <button type="submit">Entrar</button>
</form>

<p>
    Ainda nao tem conta?
    <a href="{% url 'accounts:cadastro' %}">Criar conta</a>
</p>
<p>
    <a href="{% url 'accounts:inicio' %}">Continuar como visitante</a>
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
RESUMO DO ARQUIVO
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 5

```html
=================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 6

```html
Tela de login por e-mail e senha. LoginView fornece o objeto ``form`` e processa
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 7

```html
a autenticacao usando o model configurado em AUTH_USER_MODEL.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 8

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 10

```html
{% block title %}Entrar | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 12

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 13

```html
<h1>Entrar</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 15

```html
<form method="post">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 16

```html
    {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 18

```html
    <!-- Exibe e-mail, senha e eventuais erros de autenticacao. -->
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 19

```html
    {{ form.as_p }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 21

```html
    {% if next %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 22

```html
        <!-- Quando login_required enviou a pessoa para o login, next guarda a
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 23

```html
             pagina original para que ela possa retornar depois de entrar. -->
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 24

```html
        <input type="hidden" name="next" value="{{ next }}">
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 25

```html
    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 27

```html
    <button type="submit">Entrar</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 28

```html
</form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 30

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 31

```html
    Ainda nao tem conta?
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 32

```html
    <a href="{% url 'accounts:cadastro' %}">Criar conta</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 33

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 34

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 35

```html
    <a href="{% url 'accounts:inicio' %}">Continuar como visitante</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 36

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 37

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

