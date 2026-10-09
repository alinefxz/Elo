# templates/accounts/painel_aprovacao_hemocentros.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/painel_aprovacao_hemocentros.html](<C:/Users/lb119/Elo/templates/accounts/painel_aprovacao_hemocentros.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% block title %}Aprovação de Hemocentros | Elo{% endblock %}

{% block content %}

<section>
    <h1>Aprovação de Hemocentros</h1>

    <p>
        Analise os cadastros institucionais antes de liberar
        a publicação e a alteração de estoques.
    </p>

    <p>
        <a href="{% url 'accounts:dashboard' %}">Voltar ao painel</a>
        · <a href="{% url 'accounts:inicio' %}">Página inicial</a>
        · <a href="{% url 'accounts:estoque_publico' %}">Estoques públicos</a>
        · <a href="{% url 'accounts:painel_validacao_pedidos' %}">Moderar pedidos</a>
    </p>

    <p>
        Hemocentros pendentes:
        <strong>{{ hemocentros|length }}</strong>
    </p>

    {% if hemocentros %}
        {% for hemocentro in hemocentros %}
            <article>
                <hr>

                <h2>{{ hemocentro.nome }}</h2>

                <p>
                    <strong>Status:</strong>
                    {{ hemocentro.get_status_validacao_display }}
                </p>

                <p>
                    <strong>E-mail:</strong>
                    {{ hemocentro.email }}
                </p>

                <p>
                    <strong>CNPJ:</strong>
                    {{ hemocentro.cnpj|default:"Não informado" }}
                </p>

                <p>
                    <strong>Telefone:</strong>
                    {{ hemocentro.telefone|default:"Não informado" }}
                </p>

                <p>
                    <strong>Cidade:</strong>
                    {{ hemocentro.cidade|default:"Não informado" }}
                </p>

                <p>
                    <strong>Estado:</strong>
                    {{ hemocentro.estado|default:"Não informado" }}
                </p>

                <p>
                    <strong>Data do cadastro:</strong>
                    {{ hemocentro.date_joined|date:"d/m/Y H:i" }}
                </p>

                <h3>Decisão administrativa</h3>

                <form
                    method="post"
                    action="{% url 'accounts:aprovar_hemocentro' hemocentro.pk %}"
                >
                    {% csrf_token %}

                    <label for="parecer-aprovar-{{ hemocentro.pk }}">
                        Parecer da aprovação:
                    </label>
                    <br>

                    <textarea
                        id="parecer-aprovar-{{ hemocentro.pk }}"
                        name="parecer"
                        rows="4"
                        cols="60"
                        placeholder="Digite o parecer da aprovação..."
                    ></textarea>

                    <br>

                    <button type="submit">
                        Aprovar Hemocentro
                    </button>
                </form>

                <br>

                <form
                    method="post"
                    action="{% url 'accounts:recusar_hemocentro' hemocentro.pk %}"
                >
                    {% csrf_token %}

                    <label for="parecer-recusar-{{ hemocentro.pk }}">
                        Motivo da recusa:
                    </label>
                    <br>

                    <textarea
                        id="parecer-recusar-{{ hemocentro.pk }}"
                        name="parecer"
                        rows="4"
                        cols="60"
                        placeholder="Informe o motivo da recusa..."
                    ></textarea>

                    <br>

                    <button type="submit">
                        Recusar Hemocentro
                    </button>
                </form>

                <br>

                <form
                    method="post"
                    action="{% url 'accounts:solicitar_correcao_hemocentro' hemocentro.pk %}"
                >
                    {% csrf_token %}

                    <label for="parecer-correcao-{{ hemocentro.pk }}">
                        Orientação para correção:
                    </label>
                    <br>

                    <textarea
                        id="parecer-correcao-{{ hemocentro.pk }}"
                        name="parecer"
                        rows="4"
                        cols="60"
                        placeholder="Informe o que precisa ser corrigido..."
                    ></textarea>

                    <br>

                    <button type="submit">
                        Solicitar correção
                    </button>
                </form>
            </article>
        {% endfor %}
    {% else %}
        <hr>

        <h2>Nenhum Hemocentro pendente</h2>

        <p>
            Não existem cadastros aguardando análise.
        </p>
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
{% block title %}Aprovação de Hemocentros | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 5

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 7

```html
<section>
```

Agrupa uma seção temática da página.

### Linha 8

```html
    <h1>Aprovação de Hemocentros</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 10

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 11

```html
        Analise os cadastros institucionais antes de liberar
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 12

```html
        a publicação e a alteração de estoques.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 13

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 15

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 16

```html
        <a href="{% url 'accounts:dashboard' %}">Voltar ao painel</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 17

```html
        · <a href="{% url 'accounts:inicio' %}">Página inicial</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 18

```html
        · <a href="{% url 'accounts:estoque_publico' %}">Estoques públicos</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 19

```html
        · <a href="{% url 'accounts:painel_validacao_pedidos' %}">Moderar pedidos</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 20

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 22

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 23

```html
        Hemocentros pendentes:
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 24

```html
        <strong>{{ hemocentros|length }}</strong>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 25

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 27

```html
    {% if hemocentros %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 28

```html
        {% for hemocentro in hemocentros %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 29

```html
            <article>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 30

```html
                <hr>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 32

```html
                <h2>{{ hemocentro.nome }}</h2>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 34

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 35

```html
                    <strong>Status:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 36

```html
                    {{ hemocentro.get_status_validacao_display }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 37

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 39

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 40

```html
                    <strong>E-mail:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 41

```html
                    {{ hemocentro.email }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 42

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 44

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 45

```html
                    <strong>CNPJ:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 46

```html
                    {{ hemocentro.cnpj|default:"Não informado" }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 47

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 49

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 50

```html
                    <strong>Telefone:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 51

```html
                    {{ hemocentro.telefone|default:"Não informado" }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 52

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 54

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 55

```html
                    <strong>Cidade:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 56

```html
                    {{ hemocentro.cidade|default:"Não informado" }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 57

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 59

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 60

```html
                    <strong>Estado:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 61

```html
                    {{ hemocentro.estado|default:"Não informado" }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 62

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 64

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 65

```html
                    <strong>Data do cadastro:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 66

```html
                    {{ hemocentro.date_joined|date:"d/m/Y H:i" }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 67

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 69

```html
                <h3>Decisão administrativa</h3>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 71

```html
                <form
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 72

```html
                    method="post"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 73

```html
                    action="{% url 'accounts:aprovar_hemocentro' hemocentro.pk %}"
```

Resolve a rota Django pelo nome indicado.

### Linha 74

```html
                >
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 75

```html
                    {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 77

```html
                    <label for="parecer-aprovar-{{ hemocentro.pk }}">
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Apresenta o rótulo de um campo; for liga ao id do controle.

### Linha 78

```html
                        Parecer da aprovação:
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 79

```html
                    </label>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 80

```html
                    <br>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 82

```html
                    <textarea
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 83

```html
                        id="parecer-aprovar-{{ hemocentro.pk }}"
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 84

```html
                        name="parecer"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 85

```html
                        rows="4"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 86

```html
                        cols="60"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 87

```html
                        placeholder="Digite o parecer da aprovação..."
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 88

```html
                    ></textarea>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 90

```html
                    <br>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 92

```html
                    <button type="submit">
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 93

```html
                        Aprovar Hemocentro
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 94

```html
                    </button>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 95

```html
                </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 97

```html
                <br>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 99

```html
                <form
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 100

```html
                    method="post"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 101

```html
                    action="{% url 'accounts:recusar_hemocentro' hemocentro.pk %}"
```

Resolve a rota Django pelo nome indicado.

### Linha 102

```html
                >
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 103

```html
                    {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 105

```html
                    <label for="parecer-recusar-{{ hemocentro.pk }}">
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Apresenta o rótulo de um campo; for liga ao id do controle.

### Linha 106

```html
                        Motivo da recusa:
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 107

```html
                    </label>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 108

```html
                    <br>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 110

```html
                    <textarea
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 111

```html
                        id="parecer-recusar-{{ hemocentro.pk }}"
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 112

```html
                        name="parecer"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 113

```html
                        rows="4"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 114

```html
                        cols="60"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 115

```html
                        placeholder="Informe o motivo da recusa..."
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 116

```html
                    ></textarea>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 118

```html
                    <br>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 120

```html
                    <button type="submit">
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 121

```html
                        Recusar Hemocentro
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 122

```html
                    </button>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 123

```html
                </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 125

```html
                <br>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 127

```html
                <form
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 128

```html
                    method="post"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 129

```html
                    action="{% url 'accounts:solicitar_correcao_hemocentro' hemocentro.pk %}"
```

Resolve a rota Django pelo nome indicado.

### Linha 130

```html
                >
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 131

```html
                    {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 133

```html
                    <label for="parecer-correcao-{{ hemocentro.pk }}">
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Apresenta o rótulo de um campo; for liga ao id do controle.

### Linha 134

```html
                        Orientação para correção:
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 135

```html
                    </label>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 136

```html
                    <br>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 138

```html
                    <textarea
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 139

```html
                        id="parecer-correcao-{{ hemocentro.pk }}"
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 140

```html
                        name="parecer"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 141

```html
                        rows="4"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 142

```html
                        cols="60"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 143

```html
                        placeholder="Informe o que precisa ser corrigido..."
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 144

```html
                    ></textarea>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 146

```html
                    <br>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 148

```html
                    <button type="submit">
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 149

```html
                        Solicitar correção
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 150

```html
                    </button>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 151

```html
                </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 152

```html
            </article>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 153

```html
        {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 154

```html
    {% else %}
```

Inicia o caminho alternativo da condição anterior.

### Linha 155

```html
        <hr>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 157

```html
        <h2>Nenhum Hemocentro pendente</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 159

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 160

```html
            Não existem cadastros aguardando análise.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 161

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 162

```html
    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 163

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 165

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

