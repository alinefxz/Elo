# templates/accounts/estoque_publico.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/estoque_publico.html](<C:/Users/lb119/Elo/templates/accounts/estoque_publico.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% comment %}
RF 32 - Visualização pública de estoques

Esta página pode ser acessada por visitantes e usuários autenticados.

São exibidos somente dados públicos:
- Nome do Hemocentro
- Cidade e estado
- Tipo sanguíneo
- Quantidade de bolsas
- Situação do estoque
- Última atualização

Não são exibidos dados internos, como:
- CPF
- CNPJ
- E-mail
- Responsável pelas movimentações
- Histórico
- Nível mínimo
- Nível crítico
- Auditorias
{% endcomment %}

{% block title %}Estoques de Sangue | Elo{% endblock %}

{% block content %}

<h1>Estoques de Sangue</h1>

<p>
    Consulte a situação dos estoques disponíveis nos Hemocentros cadastrados e aprovados no Elo.
</p>

<form method="get">
    {{ form.as_p }}

    <button type="submit">
        Filtrar estoque
    </button>

    <a href="{% url 'accounts:estoque_publico' %}">
        Limpar filtros
    </a>
</form>

<section>
    <h2>Indicadores</h2>

    <ul>
        <li>
            <strong>Crítico</strong> - estoque em situação crítica.
        </li>

        <li>
            <strong>Baixo</strong> - estoque abaixo do nível esperado.
        </li>

        <li>
            <strong>Adequado</strong> - estoque dentro da faixa esperada.
        </li>

        <li>
            <strong>Alto</strong> - estoque acima da faixa adequada.
        </li>
    </ul>
</section>

<section>
    <h2>Estoques por Hemocentro</h2>

    {% if estoques %}

        {% regroup estoques by nome as hemocentros %}

        {% for hemocentro in hemocentros %}

            <article>
                <h3>{{ hemocentro.grouper }}</h3>

                <table>
                    <thead>
                        <tr>
                            <th>Tipo sanguíneo</th>
                            <th>Quantidade</th>
                            <th>Situação</th>
                            <th>Última atualização</th>
                        </tr>
                    </thead>

                    <tbody>
                        {% for item in hemocentro.list %}
                            <tr>
                                <td>
                                    <strong>
                                        {{ item.tipo_sanguineo }}
                                    </strong>
                                </td>

                                <td>
                                    {{ item.quantidade_bolsas }} bolsas
                                </td>

                                <td>
                                    {{ item.status_label }}
                                </td>

                                <td>
                                    {{ item.data_atualizacao|date:"d/m/Y H:i" }}
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>

                <p>
                    <strong>Localização:</strong>
                    {{ hemocentro.list.0.cidade }}/{{ hemocentro.list.0.estado }}
                </p>
            </article>

            <hr>

        {% endfor %}

    {% else %}

        <p>
            Nenhum estoque público disponível no momento.
        </p>

    {% endif %}
</section>

<section>
    <p>
        <strong>Importante:</strong>
        os dados apresentados têm finalidade informativa.
        A disponibilidade real das bolsas deve ser confirmada diretamente
        com o Hemocentro.
    </p>
</section>

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
RF 32 - Visualização pública de estoques
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 6

```html
Esta página pode ser acessada por visitantes e usuários autenticados.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 8

```html
São exibidos somente dados públicos:
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 9

```html
- Nome do Hemocentro
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 10

```html
- Cidade e estado
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 11

```html
- Tipo sanguíneo
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 12

```html
- Quantidade de bolsas
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 13

```html
- Situação do estoque
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 14

```html
- Última atualização
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 16

```html
Não são exibidos dados internos, como:
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 17

```html
- CPF
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 18

```html
- CNPJ
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 19

```html
- E-mail
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 20

```html
- Responsável pelas movimentações
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 21

```html
- Histórico
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 22

```html
- Nível mínimo
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 23

```html
- Nível crítico
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 24

```html
- Auditorias
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 25

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 27

```html
{% block title %}Estoques de Sangue | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 29

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 31

```html
<h1>Estoques de Sangue</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 33

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 34

```html
    Consulte a situação dos estoques disponíveis nos Hemocentros cadastrados e aprovados no Elo.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 35

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 37

```html
<form method="get">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 38

```html
    {{ form.as_p }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 40

```html
    <button type="submit">
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 41

```html
        Filtrar estoque
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 42

```html
    </button>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 44

```html
    <a href="{% url 'accounts:estoque_publico' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 45

```html
        Limpar filtros
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 46

```html
    </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 47

```html
</form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 49

```html
<section>
```

Agrupa uma seção temática da página.

### Linha 50

```html
    <h2>Indicadores</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 52

```html
    <ul>
```

Abre lista; ul é não numerada e ol é numerada.

### Linha 53

```html
        <li>
```

Define um item da lista.

### Linha 54

```html
            <strong>Crítico</strong> - estoque em situação crítica.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 55

```html
        </li>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 57

```html
        <li>
```

Define um item da lista.

### Linha 58

```html
            <strong>Baixo</strong> - estoque abaixo do nível esperado.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 59

```html
        </li>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 61

```html
        <li>
```

Define um item da lista.

### Linha 62

```html
            <strong>Adequado</strong> - estoque dentro da faixa esperada.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 63

```html
        </li>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 65

```html
        <li>
```

Define um item da lista.

### Linha 66

```html
            <strong>Alto</strong> - estoque acima da faixa adequada.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 67

```html
        </li>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 68

```html
    </ul>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 69

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 71

```html
<section>
```

Agrupa uma seção temática da página.

### Linha 72

```html
    <h2>Estoques por Hemocentro</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 74

```html
    {% if estoques %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 76

```html
        {% regroup estoques by nome as hemocentros %}
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 78

```html
        {% for hemocentro in hemocentros %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 80

```html
            <article>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 81

```html
                <h3>{{ hemocentro.grouper }}</h3>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 83

```html
                <table>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 84

```html
                    <thead>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 85

```html
                        <tr>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 86

```html
                            <th>Tipo sanguíneo</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 87

```html
                            <th>Quantidade</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 88

```html
                            <th>Situação</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 89

```html
                            <th>Última atualização</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 90

```html
                        </tr>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 91

```html
                    </thead>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 93

```html
                    <tbody>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 94

```html
                        {% for item in hemocentro.list %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 95

```html
                            <tr>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 96

```html
                                <td>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 97

```html
                                    <strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 98

```html
                                        {{ item.tipo_sanguineo }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 99

```html
                                    </strong>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 100

```html
                                </td>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 102

```html
                                <td>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 103

```html
                                    {{ item.quantidade_bolsas }} bolsas
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 104

```html
                                </td>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 106

```html
                                <td>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 107

```html
                                    {{ item.status_label }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 108

```html
                                </td>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 110

```html
                                <td>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 111

```html
                                    {{ item.data_atualizacao|date:"d/m/Y H:i" }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 112

```html
                                </td>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 113

```html
                            </tr>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 114

```html
                        {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 115

```html
                    </tbody>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 116

```html
                </table>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 118

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 119

```html
                    <strong>Localização:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 120

```html
                    {{ hemocentro.list.0.cidade }}/{{ hemocentro.list.0.estado }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 121

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 122

```html
            </article>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 124

```html
            <hr>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 126

```html
        {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 128

```html
    {% else %}
```

Inicia o caminho alternativo da condição anterior.

### Linha 130

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 131

```html
            Nenhum estoque público disponível no momento.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 132

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 134

```html
    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 135

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 137

```html
<section>
```

Agrupa uma seção temática da página.

### Linha 138

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 139

```html
        <strong>Importante:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 140

```html
        os dados apresentados têm finalidade informativa.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 141

```html
        A disponibilidade real das bolsas deve ser confirmada diretamente
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 142

```html
        com o Hemocentro.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 143

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 144

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 146

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

