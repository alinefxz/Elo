# templates/accounts/estoque_hemocentro.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/estoque_hemocentro.html](<C:/Users/lb119/Elo/templates/accounts/estoque_hemocentro.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% block title %}Meu Estoque | Elo{% endblock %}

{% block content %}

<section class="estoque-hemocentro">

    <h1>Meu Estoque</h1>

    <p>
        Gerencie a quantidade de bolsas disponíveis por tipo sanguíneo.
    </p>

    <section>
        <h2>Estoques cadastrados</h2>

        {% if estoques %}

            <div class="estoques-grid">

                {% for estoque in estoques %}

                    <article class="estoque-card">

                        <h3>{{ estoque.tipo_sanguineo }}</h3>

                        <p>
                            <strong>Quantidade:</strong>
                            {{ estoque.quantidade_bolsas }} bolsas
                        </p>

                        <p>
                            <strong>Status:</strong>
                            {{ estoque.get_status_calculado_display }}
                        </p>

                        <p>
                            <strong>Última atualização:</strong>
                            {{ estoque.data_atualizacao|date:"d/m/Y H:i" }}
                        </p>

                        <p>
                            <strong>Nível mínimo:</strong>
                            {{ estoque.nivel_minimo }} bolsas
                            <br>
                            <strong>Nível crítico:</strong>
                            {{ estoque.nivel_critico }} bolsas
                        </p>


                        <h4>Atualizar estoque</h4>

                        <form
                            method="post"
                            action="{% url 'accounts:atualizar_estoque' estoque.id_estoque %}"
                        >
                            {% csrf_token %}

                            <div>
                                {{ form_movimentacao.tipo_movimento.label_tag }}
                                {{ form_movimentacao.tipo_movimento }}
                            </div>

                            <div>
                                {{ form_movimentacao.quantidade.label_tag }}
                                {{ form_movimentacao.quantidade }}

                                {% if form_movimentacao.quantidade.help_text %}
                                    <small>
                                        {{ form_movimentacao.quantidade.help_text }}
                                    </small>
                                {% endif %}
                            </div>

                            <div>
                                {{ form_movimentacao.motivo.label_tag }}
                                {{ form_movimentacao.motivo }}
                                {% if form_movimentacao.motivo.help_text %}
                                    <small>
                                        {{ form_movimentacao.motivo.help_text }}
                                    </small>
                                {% endif %}
                            </div>

                            <button type="submit">
                                Atualizar estoque
                            </button>
                        </form>

                        <h4>Histórico de movimentações</h4>

                        {% with movimentacoes=estoque.movimentacoes.all %}
                            {% if movimentacoes %}
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Data</th>
                                            <th>Movimentação</th>
                                            <th>Anterior</th>
                                            <th>Nova</th>
                                            <th>Responsável</th>
                                            <th>Motivo</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for movimentacao in movimentacoes %}
                                            <tr>
                                                <td>
                                                    {{ movimentacao.data_hora|date:"d/m/Y H:i" }}
                                                </td>
                                                <td>
                                                    {{ movimentacao.get_tipo_movimento_display }}
                                                </td>
                                                <td>{{ movimentacao.quantidade_anterior }}</td>
                                                <td>{{ movimentacao.quantidade_nova }}</td>
                                                <td>
                                                    {% if movimentacao.usuario_resp %}
                                                        {{ movimentacao.usuario_resp.nome }}
                                                    {% else %}
                                                        Usuário removido
                                                    {% endif %}
                                                </td>
                                                <td>{{ movimentacao.motivo }}</td>
                                            </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            {% else %}
                                <p>Nenhuma movimentação registrada.</p>
                            {% endif %}
                        {% endwith %}

                    </article>

                {% endfor %}

            </div>

        {% else %}

            <p>
                Nenhum estoque foi cadastrado ainda.
            </p>

        {% endif %}
    </section>


    {% if tipos_disponiveis %}

        <section>
            <h2>Cadastrar novo estoque</h2>

            <p>
                Cadastre os tipos sanguíneos que ainda não possuem estoque.
            </p>

            <form
                method="post"
                action="{% url 'accounts:cadastrar_estoque' %}"
            >
                {% csrf_token %}

                <div>
                    {{ form_cadastro.tipo_sanguineo.label_tag }}
                    {{ form_cadastro.tipo_sanguineo }}
                </div>

                <div>
                    {{ form_cadastro.quantidade_bolsas.label_tag }}
                    {{ form_cadastro.quantidade_bolsas }}

                    {% if form_cadastro.quantidade_bolsas.help_text %}
                        <small>
                            {{ form_cadastro.quantidade_bolsas.help_text }}
                        </small>
                    {% endif %}
                </div>

                <div>
                    {{ form_cadastro.nivel_minimo.label_tag }}
                    {{ form_cadastro.nivel_minimo }}

                    {% if form_cadastro.nivel_minimo.help_text %}
                        <small>
                            {{ form_cadastro.nivel_minimo.help_text }}
                        </small>
                    {% endif %}
                </div>

                <div>
                    {{ form_cadastro.nivel_critico.label_tag }}
                    {{ form_cadastro.nivel_critico }}

                    {% if form_cadastro.nivel_critico.help_text %}
                        <small>
                            {{ form_cadastro.nivel_critico.help_text }}
                        </small>
                    {% endif %}
                </div>

                <button type="submit">
                    Cadastrar estoque
                </button>
            </form>
        </section>

    {% endif %}

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
{% block title %}Meu Estoque | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 5

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 7

```html
<section class="estoque-hemocentro">
```

Agrupa uma seção temática da página.

### Linha 9

```html
    <h1>Meu Estoque</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 11

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 12

```html
        Gerencie a quantidade de bolsas disponíveis por tipo sanguíneo.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 13

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 15

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 16

```html
        <h2>Estoques cadastrados</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 18

```html
        {% if estoques %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 20

```html
            <div class="estoques-grid">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 22

```html
                {% for estoque in estoques %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 24

```html
                    <article class="estoque-card">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 26

```html
                        <h3>{{ estoque.tipo_sanguineo }}</h3>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 28

```html
                        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 29

```html
                            <strong>Quantidade:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 30

```html
                            {{ estoque.quantidade_bolsas }} bolsas
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 31

```html
                        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 33

```html
                        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 34

```html
                            <strong>Status:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 35

```html
                            {{ estoque.get_status_calculado_display }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 36

```html
                        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 38

```html
                        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 39

```html
                            <strong>Última atualização:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 40

```html
                            {{ estoque.data_atualizacao|date:"d/m/Y H:i" }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 41

```html
                        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 43

```html
                        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 44

```html
                            <strong>Nível mínimo:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 45

```html
                            {{ estoque.nivel_minimo }} bolsas
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 46

```html
                            <br>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 47

```html
                            <strong>Nível crítico:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 48

```html
                            {{ estoque.nivel_critico }} bolsas
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 49

```html
                        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 52

```html
                        <h4>Atualizar estoque</h4>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 54

```html
                        <form
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 55

```html
                            method="post"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 56

```html
                            action="{% url 'accounts:atualizar_estoque' estoque.id_estoque %}"
```

Resolve a rota Django pelo nome indicado.

### Linha 57

```html
                        >
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 58

```html
                            {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 60

```html
                            <div>
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 61

```html
                                {{ form_movimentacao.tipo_movimento.label_tag }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 62

```html
                                {{ form_movimentacao.tipo_movimento }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 63

```html
                            </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 65

```html
                            <div>
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 66

```html
                                {{ form_movimentacao.quantidade.label_tag }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 67

```html
                                {{ form_movimentacao.quantidade }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 69

```html
                                {% if form_movimentacao.quantidade.help_text %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 70

```html
                                    <small>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 71

```html
                                        {{ form_movimentacao.quantidade.help_text }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 72

```html
                                    </small>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 73

```html
                                {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 74

```html
                            </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 76

```html
                            <div>
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 77

```html
                                {{ form_movimentacao.motivo.label_tag }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 78

```html
                                {{ form_movimentacao.motivo }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 79

```html
                                {% if form_movimentacao.motivo.help_text %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 80

```html
                                    <small>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 81

```html
                                        {{ form_movimentacao.motivo.help_text }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 82

```html
                                    </small>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 83

```html
                                {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 84

```html
                            </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 86

```html
                            <button type="submit">
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 87

```html
                                Atualizar estoque
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 88

```html
                            </button>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 89

```html
                        </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 91

```html
                        <h4>Histórico de movimentações</h4>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 93

```html
                        {% with movimentacoes=estoque.movimentacoes.all %}
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 94

```html
                            {% if movimentacoes %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 95

```html
                                <table>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 96

```html
                                    <thead>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 97

```html
                                        <tr>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 98

```html
                                            <th>Data</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 99

```html
                                            <th>Movimentação</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 100

```html
                                            <th>Anterior</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 101

```html
                                            <th>Nova</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 102

```html
                                            <th>Responsável</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 103

```html
                                            <th>Motivo</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 104

```html
                                        </tr>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 105

```html
                                    </thead>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 106

```html
                                    <tbody>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 107

```html
                                        {% for movimentacao in movimentacoes %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 108

```html
                                            <tr>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 109

```html
                                                <td>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 110

```html
                                                    {{ movimentacao.data_hora|date:"d/m/Y H:i" }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 111

```html
                                                </td>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 112

```html
                                                <td>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 113

```html
                                                    {{ movimentacao.get_tipo_movimento_display }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 114

```html
                                                </td>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 115

```html
                                                <td>{{ movimentacao.quantidade_anterior }}</td>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 116

```html
                                                <td>{{ movimentacao.quantidade_nova }}</td>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 117

```html
                                                <td>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 118

```html
                                                    {% if movimentacao.usuario_resp %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 119

```html
                                                        {{ movimentacao.usuario_resp.nome }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 120

```html
                                                    {% else %}
```

Inicia o caminho alternativo da condição anterior.

### Linha 121

```html
                                                        Usuário removido
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 122

```html
                                                    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 123

```html
                                                </td>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 124

```html
                                                <td>{{ movimentacao.motivo }}</td>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 125

```html
                                            </tr>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 126

```html
                                        {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 127

```html
                                    </tbody>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 128

```html
                                </table>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 129

```html
                            {% else %}
```

Inicia o caminho alternativo da condição anterior.

### Linha 130

```html
                                <p>Nenhuma movimentação registrada.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 131

```html
                            {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 132

```html
                        {% endwith %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 134

```html
                    </article>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 136

```html
                {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 138

```html
            </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 140

```html
        {% else %}
```

Inicia o caminho alternativo da condição anterior.

### Linha 142

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 143

```html
                Nenhum estoque foi cadastrado ainda.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 144

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 146

```html
        {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 147

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 150

```html
    {% if tipos_disponiveis %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 152

```html
        <section>
```

Agrupa uma seção temática da página.

### Linha 153

```html
            <h2>Cadastrar novo estoque</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 155

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 156

```html
                Cadastre os tipos sanguíneos que ainda não possuem estoque.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 157

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 159

```html
            <form
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 160

```html
                method="post"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 161

```html
                action="{% url 'accounts:cadastrar_estoque' %}"
```

Resolve a rota Django pelo nome indicado.

### Linha 162

```html
            >
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 163

```html
                {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 165

```html
                <div>
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 166

```html
                    {{ form_cadastro.tipo_sanguineo.label_tag }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 167

```html
                    {{ form_cadastro.tipo_sanguineo }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 168

```html
                </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 170

```html
                <div>
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 171

```html
                    {{ form_cadastro.quantidade_bolsas.label_tag }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 172

```html
                    {{ form_cadastro.quantidade_bolsas }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 174

```html
                    {% if form_cadastro.quantidade_bolsas.help_text %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 175

```html
                        <small>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 176

```html
                            {{ form_cadastro.quantidade_bolsas.help_text }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 177

```html
                        </small>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 178

```html
                    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 179

```html
                </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 181

```html
                <div>
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 182

```html
                    {{ form_cadastro.nivel_minimo.label_tag }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 183

```html
                    {{ form_cadastro.nivel_minimo }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 185

```html
                    {% if form_cadastro.nivel_minimo.help_text %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 186

```html
                        <small>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 187

```html
                            {{ form_cadastro.nivel_minimo.help_text }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 188

```html
                        </small>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 189

```html
                    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 190

```html
                </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 192

```html
                <div>
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 193

```html
                    {{ form_cadastro.nivel_critico.label_tag }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 194

```html
                    {{ form_cadastro.nivel_critico }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 196

```html
                    {% if form_cadastro.nivel_critico.help_text %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 197

```html
                        <small>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 198

```html
                            {{ form_cadastro.nivel_critico.help_text }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 199

```html
                        </small>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 200

```html
                    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 201

```html
                </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 203

```html
                <button type="submit">
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 204

```html
                    Cadastrar estoque
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 205

```html
                </button>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 206

```html
            </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 207

```html
        </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 209

```html
    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 211

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 213

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

