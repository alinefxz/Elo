# templates/base.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/base.html](<C:/Users/lb119/Elo/templates/base.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% load static %}
{% comment %}
RESUMO DO ARQUIVO
=================
Template-base reutilizado pelas paginas do sistema.

Ele define a estrutura HTML, a navegacao, as mensagens temporarias e dois blocos
que as paginas filhas substituem: title e content.

A navegacao tambem respeita a particularizacao por perfil:
- todos podem acessar paginas publicas;
- usuarios autenticados acessam o painel;
- Hemocentro aprovado recebe atalho para gerenciar o proprio estoque;
- Administrador recebe atalhos de validacao e painel administrativo.
{% endcomment %}
<!doctype html>
<html lang="pt-br">
<head>
    <meta charset="utf-8">

    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Elo - sistema de doacao de sangue.">

    <title>{% block title %}Elo{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/elo.css' %}">
    <link rel="icon" type="image/png" href="{% static 'css/favicon.png' %}">
</head>
<body>
    <header class="site-header">
        <div class="header-inner">
            <a class="brand" href="{% url 'accounts:inicio' %}" aria-label="Elo - pagina inicial">
                <img class="brand-mark" src="{% static 'css/favicon.png' %}" alt="" aria-hidden="true">
                <span class="brand-name">elo</span>
            </a>

            <button class="menu-toggle" type="button" aria-label="Abrir menu" aria-expanded="false">
                <span></span>
                <span></span>
                <span></span>
            </button>

            <nav class="main-nav" aria-label="Navegacao principal">
                {% if user.is_authenticated %}
                    <a href="{% url 'accounts:dashboard' %}">Painel</a>
                    <a href="{% url 'accounts:inicio' %}">Início</a>
                    <a href="{% url 'accounts:compatibilidade_sanguinea' %}">Compatibilidade sanguinea</a>
                    <a href="{% url 'accounts:estoque_publico' %}">Estoques publicos</a>

                    {% if user.perfil == "RECEPTOR" %}
                        <a href="{% url 'accounts:pedido_publicar' %}">Solicitar necessidade</a>
                    {% endif %}

                    {% if user.perfil == "HEMOCENTRO" and user.status_validacao == "APROVADO" %}
                        <a href="{% url 'accounts:painel_pedidos_hemocentro' %}">Analisar solicitações</a>
                        <a href="{% url 'accounts:estoque_hemocentro' %}">Meu estoque</a>
                    {% endif %}

                    {% if user.is_staff or user.is_superuser or user.perfil == "ADMINISTRADOR" %}
                        <a href="{% url 'accounts:painel_aprovacao_hemocentros' %}">Validar Hemocentros</a>
                        <a href="{% url 'accounts:painel_validacao_pedidos' %}">Moderar pedidos</a>
                        <a href="/admin/">Admin</a>
                    {% endif %}

                    <span>{{ user.get_short_name }}</span>

                    <form method="post" action="{% url 'accounts:logout' %}">
                        {% csrf_token %}
                        <button type="submit">Sair</button>
                    </form>
                {% else %}
                    <a href="{% url 'accounts:inicio' %}#sobre">Sobre o elo</a>
                    <a href="{% url 'accounts:compatibilidade_sanguinea' %}">Compatibilidade sanguinea</a>
                    <a href="{% url 'accounts:estoque_publico' %}">Estoques publicos</a>
                    <a href="{% url 'accounts:pedido_publicar' %}">Solicitar necessidade</a>
                    <a href="{% url 'accounts:login' %}">Entrar</a>
                    <a class="nav-cta" href="{% url 'accounts:cadastro' %}">Criar conta</a>
                {% endif %}
            </nav>
        </div>
    </header>

    <main>
        {% if messages %}
            <div class="messages-wrap">
                {% for message in messages %}
                    <div class="message message-{{ message.tags|default:'info' }}">
                        {{ message }}
                    </div>
                {% endfor %}
            </div>
        {% endif %}

        {% block content %}{% endblock %}
    </main>

    <footer class="site-footer">
        <div class="footer-inner">
            <a class="brand brand-footer" href="{% url 'accounts:inicio' %}">
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
{% comment %}
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 3

```html
RESUMO DO ARQUIVO
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 4

```html
=================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 5

```html
Template-base reutilizado pelas paginas do sistema.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 7

```html
Ele define a estrutura HTML, a navegacao, as mensagens temporarias e dois blocos
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 8

```html
que as paginas filhas substituem: title e content.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 10

```html
A navegacao tambem respeita a particularizacao por perfil:
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 11

```html
- todos podem acessar paginas publicas;
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 12

```html
- usuarios autenticados acessam o painel;
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 13

```html
- Hemocentro aprovado recebe atalho para gerenciar o proprio estoque;
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 14

```html
- Administrador recebe atalhos de validacao e painel administrativo.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 15

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 16

```html
<!doctype html>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 17

```html
<html lang="pt-br">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 18

```html
<head>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 19

```html
    <meta charset="utf-8">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 21

```html
    <meta name="viewport" content="width=device-width, initial-scale=1">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 22

```html
    <meta name="description" content="Elo - sistema de doacao de sangue.">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 24

```html
    <title>{% block title %}Elo{% endblock %}</title>
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 25

```html
    <link rel="stylesheet" href="{% static 'css/elo.css' %}">
```

Resolve o caminho do recurso estático, como imagem ou CSS. Vincula recurso externo ao documento, como folha de estilos ou ícone. Define um item da lista.

### Linha 26

```html
    <link rel="icon" type="image/png" href="{% static 'css/favicon.png' %}">
```

Resolve o caminho do recurso estático, como imagem ou CSS. Vincula recurso externo ao documento, como folha de estilos ou ícone. Define um item da lista.

### Linha 27

```html
</head>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 28

```html
<body>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 29

```html
    <header class="site-header">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 30

```html
        <div class="header-inner">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 31

```html
            <a class="brand" href="{% url 'accounts:inicio' %}" aria-label="Elo - pagina inicial">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 32

```html
                <img class="brand-mark" src="{% static 'css/favicon.png' %}" alt="" aria-hidden="true">
```

Resolve o caminho do recurso estático, como imagem ou CSS. Exibe imagem; src aponta o arquivo e alt fornece texto alternativo.

### Linha 33

```html
                <span class="brand-name">elo</span>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 34

```html
            </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 36

```html
            <button class="menu-toggle" type="button" aria-label="Abrir menu" aria-expanded="false">
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 37

```html
                <span></span>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 38

```html
                <span></span>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 39

```html
                <span></span>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 40

```html
            </button>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 42

```html
            <nav class="main-nav" aria-label="Navegacao principal">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 43

```html
                {% if user.is_authenticated %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 44

```html
                    <a href="{% url 'accounts:dashboard' %}">Painel</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 45

```html
                    <a href="{% url 'accounts:inicio' %}">Início</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 46

```html
                    <a href="{% url 'accounts:compatibilidade_sanguinea' %}">Compatibilidade sanguinea</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 47

```html
                    <a href="{% url 'accounts:estoque_publico' %}">Estoques publicos</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 49

```html
                    {% if user.perfil == "RECEPTOR" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 50

```html
                        <a href="{% url 'accounts:pedido_publicar' %}">Solicitar necessidade</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 51

```html
                    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 53

```html
                    {% if user.perfil == "HEMOCENTRO" and user.status_validacao == "APROVADO" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 54

```html
                        <a href="{% url 'accounts:painel_pedidos_hemocentro' %}">Analisar solicitações</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 55

```html
                        <a href="{% url 'accounts:estoque_hemocentro' %}">Meu estoque</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 56

```html
                    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 58

```html
                    {% if user.is_staff or user.is_superuser or user.perfil == "ADMINISTRADOR" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 59

```html
                        <a href="{% url 'accounts:painel_aprovacao_hemocentros' %}">Validar Hemocentros</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 60

```html
                        <a href="{% url 'accounts:painel_validacao_pedidos' %}">Moderar pedidos</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 61

```html
                        <a href="/admin/">Admin</a>
```

Define link; href é o endereço ou âncora que o navegador abre.

### Linha 62

```html
                    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 64

```html
                    <span>{{ user.get_short_name }}</span>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 66

```html
                    <form method="post" action="{% url 'accounts:logout' %}">
```

Resolve a rota Django pelo nome indicado. Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 67

```html
                        {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 68

```html
                        <button type="submit">Sair</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 69

```html
                    </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 70

```html
                {% else %}
```

Inicia o caminho alternativo da condição anterior.

### Linha 71

```html
                    <a href="{% url 'accounts:inicio' %}#sobre">Sobre o elo</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 72

```html
                    <a href="{% url 'accounts:compatibilidade_sanguinea' %}">Compatibilidade sanguinea</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 73

```html
                    <a href="{% url 'accounts:estoque_publico' %}">Estoques publicos</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 74

```html
                    <a href="{% url 'accounts:pedido_publicar' %}">Solicitar necessidade</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 75

```html
                    <a href="{% url 'accounts:login' %}">Entrar</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 76

```html
                    <a class="nav-cta" href="{% url 'accounts:cadastro' %}">Criar conta</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 77

```html
                {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 78

```html
            </nav>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 79

```html
        </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 80

```html
    </header>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 82

```html
    <main>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 83

```html
        {% if messages %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 84

```html
            <div class="messages-wrap">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 85

```html
                {% for message in messages %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 86

```html
                    <div class="message message-{{ message.tags|default:'info' }}">
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 87

```html
                        {{ message }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 88

```html
                    </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 89

```html
                {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 90

```html
            </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 91

```html
        {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 93

```html
        {% block content %}{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 94

```html
    </main>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 96

```html
    <footer class="site-footer">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 97

```html
        <div class="footer-inner">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 98

```html
            <a class="brand brand-footer" href="{% url 'accounts:inicio' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 99

```html
                <span class="brand-name">elo</span>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 100

```html
            </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 102

```html
            <p>Conectando pessoas, hemocentros e vidas.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 104

```html
            <div class="footer-links">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 105

```html
                <a href="{% url 'accounts:inicio' %}#sobre">Sobre o elo</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 106

```html
                <a href="{% url 'accounts:triagem_apresentacao' %}">Como doar</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 107

```html
                <a href="{% url 'accounts:estoque_publico' %}">Estoques</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 108

```html
                {% if user.is_authenticated %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 109

```html
                    <a href="{% url 'accounts:dashboard' %}">Meu painel</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 110

```html
                {% else %}
```

Inicia o caminho alternativo da condição anterior.

### Linha 111

```html
                    <a href="{% url 'accounts:login' %}">Entrar</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 112

```html
                {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 113

```html
            </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 114

```html
        </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 115

```html
    </footer>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 117

```html
    <script>
```

Inicia JavaScript executado no navegador, não no servidor Python.

### Linha 118

```html
        const menuToggle = document.querySelector(".menu-toggle");
```

Seleciona elemento HTML para leitura ou alteração pelo script. Declara uma variável JavaScript: const impede reatribuir o vínculo e let permite reatribuição.

### Linha 119

```html
        const mainNav = document.querySelector(".main-nav");
```

Seleciona elemento HTML para leitura ou alteração pelo script. Declara uma variável JavaScript: const impede reatribuir o vínculo e let permite reatribuição.

### Linha 121

```html
        if (menuToggle && mainNav) {
```

Executa o bloco JavaScript apenas quando a condição indicada for verdadeira.

### Linha 122

```html
            menuToggle.addEventListener("click", () => {
```

Conecta um evento do navegador à função indicada. Declara uma função JavaScript/callback; só executa quando chamada ou acionada pelo evento associado.

### Linha 123

```html
                const opened = mainNav.classList.toggle("is-open");
```

Altera classes CSS para atualizar a apresentação/interação. Declara uma variável JavaScript: const impede reatribuir o vínculo e let permite reatribuição.

### Linha 124

```html
                menuToggle.setAttribute("aria-expanded", opened ? "true" : "false");
```

Atualiza um atributo do elemento, inclusive estados de acessibilidade quando indicado.

### Linha 125

```html
            });
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 126

```html
        }
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 127

```html
    </script>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 128

```html
</body>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 129

```html
</html>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

