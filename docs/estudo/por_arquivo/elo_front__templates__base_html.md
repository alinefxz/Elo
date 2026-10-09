# elo_front/templates/base.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [elo_front/templates/base.html](<C:/Users/lb119/Elo/elo_front/templates/base.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% load static %}
<!doctype html>
<html lang="pt-br">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Elo — sistema de doação de sangue.">
    <title>{% block title %}Elo{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/elo.css' %}">
</head>

<body>
    <header class="site-header">
        <div class="header-inner">
            <a class="brand" href="{% url 'accounts:inicio' %}" aria-label="Elo - página inicial">
                <span class="brand-mark" aria-hidden="true"></span>
                <span class="brand-name">elo</span>
            </a>

            <button class="menu-toggle" type="button" aria-label="Abrir menu" aria-expanded="false">
                <span></span><span></span><span></span>
            </button>

            <nav class="main-nav" aria-label="Navegação principal">
                <a href="{% url 'accounts:inicio' %}#sobre">Sobre o elo</a>
                <a href="{% url 'accounts:inicio' %}#como-doar">Como doar</a>
                <a href="{% url 'accounts:estoque_publico' %}">Hemocentro</a>
                <a href="{% url 'accounts:inicio' %}#duvidas">Dúvidas</a>
                <a class="nav-cta" href="{% url 'accounts:cadastro' %}">Sou hemocentro</a>
            </nav>
        </div>
    </header>

    {% if messages %}
        <div class="messages-wrap">
            {% for message in messages %}
                <div class="message message-{{ message.tags|default:'info' }}">
                    {{ message }}
                </div>
            {% endfor %}
        </div>
    {% endif %}

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer class="site-footer">
        <div class="footer-inner">
            <a class="brand brand-footer" href="{% url 'accounts:inicio' %}">
                <span class="brand-mark" aria-hidden="true"></span>
                <span class="brand-name">elo</span>
            </a>
            <p>Conectando pessoas, hemocentros e vidas.</p>
            <div class="footer-links">
                <a href="{% url 'accounts:inicio' %}#sobre">Sobre o elo</a>
                <a href="{% url 'accounts:triagem_apresentacao' %}">Como doar</a>
                <a href="{% url 'accounts:estoque_publico' %}">Estoques</a>
                {% if user.is_authenticated %}
                    <a href="{% url 'accounts:dashboard' %}">Meu painel</a>
                {% else %}
                    <a href="{% url 'accounts:login' %}">Entrar</a>
                {% endif %}
            </div>
        </div>
    </footer>

    <script>
        const menuToggle = document.querySelector(".menu-toggle");
        const mainNav = document.querySelector(".main-nav");

        if (menuToggle && mainNav) {
            menuToggle.addEventListener("click", () => {
                const opened = mainNav.classList.toggle("is-open");
                menuToggle.setAttribute("aria-expanded", opened ? "true" : "false");
            });
        }
    </script>
</body>
</html>
``````

## Leitura da tela, linha por linha

### Linha 1

```html
{% load static %}
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 2

```html
<!doctype html>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 3

```html
<html lang="pt-br">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 4

```html
<head>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 5

```html
    <meta charset="utf-8">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 6

```html
    <meta name="viewport" content="width=device-width, initial-scale=1">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 7

```html
    <meta name="description" content="Elo — sistema de doação de sangue.">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 8

```html
    <title>{% block title %}Elo{% endblock %}</title>
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 9

```html
    <link rel="stylesheet" href="{% static 'css/elo.css' %}">
```

Resolve o caminho do recurso estático, como imagem ou CSS. Vincula recurso externo ao documento, como folha de estilos ou ícone. Define um item da lista.

### Linha 10

```html
</head>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 12

```html
<body>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 13

```html
    <header class="site-header">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 14

```html
        <div class="header-inner">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 15

```html
            <a class="brand" href="{% url 'accounts:inicio' %}" aria-label="Elo - página inicial">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 16

```html
                <span class="brand-mark" aria-hidden="true"></span>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 17

```html
                <span class="brand-name">elo</span>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 18

```html
            </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 20

```html
            <button class="menu-toggle" type="button" aria-label="Abrir menu" aria-expanded="false">
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 21

```html
                <span></span><span></span><span></span>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 22

```html
            </button>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 24

```html
            <nav class="main-nav" aria-label="Navegação principal">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 25

```html
                <a href="{% url 'accounts:inicio' %}#sobre">Sobre o elo</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 26

```html
                <a href="{% url 'accounts:inicio' %}#como-doar">Como doar</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 27

```html
                <a href="{% url 'accounts:estoque_publico' %}">Hemocentro</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 28

```html
                <a href="{% url 'accounts:inicio' %}#duvidas">Dúvidas</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 29

```html
                <a class="nav-cta" href="{% url 'accounts:cadastro' %}">Sou hemocentro</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 30

```html
            </nav>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 31

```html
        </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 32

```html
    </header>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 34

```html
    {% if messages %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 35

```html
        <div class="messages-wrap">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 36

```html
            {% for message in messages %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 37

```html
                <div class="message message-{{ message.tags|default:'info' }}">
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 38

```html
                    {{ message }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 39

```html
                </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 40

```html
            {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 41

```html
        </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 42

```html
    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 44

```html
    <main>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 45

```html
        {% block content %}{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 46

```html
    </main>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 48

```html
    <footer class="site-footer">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 49

```html
        <div class="footer-inner">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 50

```html
            <a class="brand brand-footer" href="{% url 'accounts:inicio' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 51

```html
                <span class="brand-mark" aria-hidden="true"></span>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 52

```html
                <span class="brand-name">elo</span>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 53

```html
            </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 54

```html
            <p>Conectando pessoas, hemocentros e vidas.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 55

```html
            <div class="footer-links">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 56

```html
                <a href="{% url 'accounts:inicio' %}#sobre">Sobre o elo</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 57

```html
                <a href="{% url 'accounts:triagem_apresentacao' %}">Como doar</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 58

```html
                <a href="{% url 'accounts:estoque_publico' %}">Estoques</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 59

```html
                {% if user.is_authenticated %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 60

```html
                    <a href="{% url 'accounts:dashboard' %}">Meu painel</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 61

```html
                {% else %}
```

Inicia o caminho alternativo da condição anterior.

### Linha 62

```html
                    <a href="{% url 'accounts:login' %}">Entrar</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 63

```html
                {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 64

```html
            </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 65

```html
        </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 66

```html
    </footer>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 68

```html
    <script>
```

Inicia JavaScript executado no navegador, não no servidor Python.

### Linha 69

```html
        const menuToggle = document.querySelector(".menu-toggle");
```

Seleciona elemento HTML para leitura ou alteração pelo script. Declara uma variável JavaScript: const impede reatribuir o vínculo e let permite reatribuição.

### Linha 70

```html
        const mainNav = document.querySelector(".main-nav");
```

Seleciona elemento HTML para leitura ou alteração pelo script. Declara uma variável JavaScript: const impede reatribuir o vínculo e let permite reatribuição.

### Linha 72

```html
        if (menuToggle && mainNav) {
```

Executa o bloco JavaScript apenas quando a condição indicada for verdadeira.

### Linha 73

```html
            menuToggle.addEventListener("click", () => {
```

Conecta um evento do navegador à função indicada. Declara uma função JavaScript/callback; só executa quando chamada ou acionada pelo evento associado.

### Linha 74

```html
                const opened = mainNav.classList.toggle("is-open");
```

Altera classes CSS para atualizar a apresentação/interação. Declara uma variável JavaScript: const impede reatribuir o vínculo e let permite reatribuição.

### Linha 75

```html
                menuToggle.setAttribute("aria-expanded", opened ? "true" : "false");
```

Atualiza um atributo do elemento, inclusive estados de acessibilidade quando indicado.

### Linha 76

```html
            });
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 77

```html
        }
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 78

```html
    </script>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 79

```html
</body>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 80

```html
</html>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

