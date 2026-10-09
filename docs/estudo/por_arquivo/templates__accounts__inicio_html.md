# templates/accounts/inicio.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/inicio.html](<C:/Users/lb119/Elo/templates/accounts/inicio.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% comment %}
RESUMO DO ARQUIVO
=================
Tela publica do ator Visitante. Ela permite pesquisar postos de coleta,
consultar estoque geral e ver pedidos ativos sem exigir cadastro ou login.
{% endcomment %}

{% block title %}Acesso visitante | Elo{% endblock %}

{% block content %}
<h1>Acesso visitante</h1>
<p>Pesquise postos de coleta, consulte o estoque geral e acompanhe pedidos ativos.</p>

<section>
    <h2>Triagem para doação</h2>

    <p>
        Quer saber como funciona a orientação inicial para doação de sangue?
    </p>

    <p>
        <a href="{% url 'accounts:triagem_apresentacao' %}">
            Conhecer a triagem
        </a>
    </p>
</section>

<section>
    <h2>Postos de coleta</h2>

    <form method="get">
        <label for="q">Pesquisar por posto, cidade, UF ou endereco</label>
        <input
            type="search"
            id="q"
            name="q"
            value="{{ consulta }}"
            placeholder="Ex.: Campinas, SP ou Hemocentro"
        >
        <button type="submit">Pesquisar</button>
    </form>

    {% if postos %}
        <ul>
            {% for posto in postos %}
                <li>
                    <strong>{{ posto.nome }}</strong><br>
                    {{ posto.endereco }} - {{ posto.cidade }}/{{ posto.estado }}<br>
                    {{ posto.horario }}
                </li>
            {% endfor %}
        </ul>
    {% else %}
        <p>Nenhum posto encontrado para "{{ consulta }}".</p>
    {% endif %}
</section>

<section>
    <h2>Estoque geral</h2>

    <table>
        <thead>
            <tr>
                <th>Tipo sanguineo</th>
                <th>Nivel</th>
                <th>Ocupacao</th>
            </tr>
        </thead>
        <tbody>
            {% for item in estoque_geral %}
                <tr>
                    <td>{{ item.tipo }}</td>
                    <td>{{ item.nivel }}</td>
                    <td>{{ item.percentual }}%</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</section>

<section>
    <h2>Pedidos ativos</h2>

    <ul>
        {% for pedido in pedidos_ativos %}
            <li>
                <strong>{{ pedido.titulo }}</strong><br>
                {{ pedido.tipo_sanguineo }} - {{ pedido.cidade }} - Urgencia {{ pedido.urgencia }}
            </li>
        {% endfor %}
    </ul>
</section>

<p>
    <a href="{% url 'accounts:cadastro' %}">Criar conta</a>
    <a href="{% url 'accounts:login' %}">Entrar</a>
    <a href="{% url 'admin:index' %}">Admin</a>
    
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
Tela publica do ator Visitante. Ela permite pesquisar postos de coleta,
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 7

```html
consultar estoque geral e ver pedidos ativos sem exigir cadastro ou login.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 8

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 10

```html
{% block title %}Acesso visitante | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 12

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 13

```html
<h1>Acesso visitante</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 14

```html
<p>Pesquise postos de coleta, consulte o estoque geral e acompanhe pedidos ativos.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 16

```html
<section>
```

Agrupa uma seção temática da página.

### Linha 17

```html
    <h2>Triagem para doação</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 19

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 20

```html
        Quer saber como funciona a orientação inicial para doação de sangue?
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

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
        <a href="{% url 'accounts:triagem_apresentacao' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 25

```html
            Conhecer a triagem
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 26

```html
        </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 27

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 28

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 30

```html
<section>
```

Agrupa uma seção temática da página.

### Linha 31

```html
    <h2>Postos de coleta</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 33

```html
    <form method="get">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 34

```html
        <label for="q">Pesquisar por posto, cidade, UF ou endereco</label>
```

Apresenta o rótulo de um campo; for liga ao id do controle.

### Linha 35

```html
        <input
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 36

```html
            type="search"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 37

```html
            id="q"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 38

```html
            name="q"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 39

```html
            value="{{ consulta }}"
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 40

```html
            placeholder="Ex.: Campinas, SP ou Hemocentro"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 41

```html
        >
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 42

```html
        <button type="submit">Pesquisar</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 43

```html
    </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 45

```html
    {% if postos %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 46

```html
        <ul>
```

Abre lista; ul é não numerada e ol é numerada.

### Linha 47

```html
            {% for posto in postos %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 48

```html
                <li>
```

Define um item da lista.

### Linha 49

```html
                    <strong>{{ posto.nome }}</strong><br>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 50

```html
                    {{ posto.endereco }} - {{ posto.cidade }}/{{ posto.estado }}<br>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 51

```html
                    {{ posto.horario }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 52

```html
                </li>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 53

```html
            {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 54

```html
        </ul>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 55

```html
    {% else %}
```

Inicia o caminho alternativo da condição anterior.

### Linha 56

```html
        <p>Nenhum posto encontrado para "{{ consulta }}".</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 57

```html
    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 58

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 60

```html
<section>
```

Agrupa uma seção temática da página.

### Linha 61

```html
    <h2>Estoque geral</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 63

```html
    <table>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 64

```html
        <thead>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 65

```html
            <tr>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 66

```html
                <th>Tipo sanguineo</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 67

```html
                <th>Nivel</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 68

```html
                <th>Ocupacao</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 69

```html
            </tr>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 70

```html
        </thead>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 71

```html
        <tbody>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 72

```html
            {% for item in estoque_geral %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 73

```html
                <tr>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 74

```html
                    <td>{{ item.tipo }}</td>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 75

```html
                    <td>{{ item.nivel }}</td>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 76

```html
                    <td>{{ item.percentual }}%</td>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 77

```html
                </tr>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 78

```html
            {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 79

```html
        </tbody>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 80

```html
    </table>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 81

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 83

```html
<section>
```

Agrupa uma seção temática da página.

### Linha 84

```html
    <h2>Pedidos ativos</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 86

```html
    <ul>
```

Abre lista; ul é não numerada e ol é numerada.

### Linha 87

```html
        {% for pedido in pedidos_ativos %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 88

```html
            <li>
```

Define um item da lista.

### Linha 89

```html
                <strong>{{ pedido.titulo }}</strong><br>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 90

```html
                {{ pedido.tipo_sanguineo }} - {{ pedido.cidade }} - Urgencia {{ pedido.urgencia }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 91

```html
            </li>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 92

```html
        {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 93

```html
    </ul>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 94

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 96

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 97

```html
    <a href="{% url 'accounts:cadastro' %}">Criar conta</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 98

```html
    <a href="{% url 'accounts:login' %}">Entrar</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 99

```html
    <a href="{% url 'admin:index' %}">Admin</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 101

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 102

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

