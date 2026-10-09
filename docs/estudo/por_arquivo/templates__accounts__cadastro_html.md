# templates/accounts/cadastro.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/cadastro.html](<C:/Users/lb119/Elo/templates/accounts/cadastro.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% block title %}Criar conta | Elo{% endblock %}

{% block content %}

<h1>Criar conta</h1>

<p>
    Escolha Doador, Receptor/Solicitante, Observador ou Hemocentro.
</p>

<form method="post">

    {% csrf_token %}

    {{ form.non_field_errors }}

    {% for campo in form %}

        {% if campo.name != "aceite_lgpd" %}

            <p>
                <label for="{{ campo.id_for_label }}">
                    {{ campo.label }}
                </label>

                {{ campo }}

                {{ campo.errors }}

                {% if campo.help_text %}
                    <small>{{ campo.help_text }}</small>
                {% endif %}
            </p>

        {% endif %}

    {% endfor %}

    <!-- O usuário clica diretamente nas palavras para ler os documentos -->
    <p>
        <input
            type="checkbox"
            id="{{ form.aceite_lgpd.id_for_label }}"
            name="{{ form.aceite_lgpd.html_name }}"
            required
            {% if form.aceite_lgpd.value %}checked{% endif %}
        >

        <label for="{{ form.aceite_lgpd.id_for_label }}">
            Li e aceito os

            <a
                href="#"
                onclick="document.getElementById('modal-termos').showModal(); return false;"
            >
                Termos de Uso
            </a>

            e a

            <a
                href="#"
                onclick="document.getElementById('modal-privacidade').showModal(); return false;"
            >
                Política de Privacidade
            </a>.
        </label>

        {{ form.aceite_lgpd.errors }}
    </p>

    <button type="submit">
        Criar conta
    </button>

</form>

<!-- Janela dos Termos de Uso. Fica escondida até clicar na palavra. -->
<dialog id="modal-termos">

    <h2>Termos de Uso</h2>

    <p>
        Ao criar uma conta no Elo, o usuário concorda em utilizar
        o sistema de maneira correta, legal e respeitosa.
    </p>

    <p>
        O usuário é responsável pelas informações fornecidas no cadastro,
        pela segurança da sua senha e pelas atividades realizadas em sua conta.
    </p>

    <p>
        O sistema poderá suspender ou encerrar contas que violem as regras
        de utilização ou a legislação aplicável.
    </p>

    <button
        type="button"
        onclick="document.getElementById('modal-termos').close();"
    >
        Fechar
    </button>

</dialog>

<!-- Janela da Política de Privacidade. Fica escondida até clicar na palavra. -->
<dialog id="modal-privacidade">

    <h2>Política de Privacidade</h2>

    <p>
        Os dados informados no cadastro poderão ser utilizados para criar,
        administrar e proteger a conta do usuário.
    </p>

    <p>
        As informações devem ser tratadas de acordo com a legislação aplicável,
        incluindo a Lei Geral de Proteção de Dados.
    </p>

    <p>
        O usuário poderá solicitar informações sobre o uso dos seus dados
        pelos canais oficiais do sistema.
    </p>

    <button
        type="button"
        onclick="document.getElementById('modal-privacidade').close();"
    >
        Fechar
    </button>

</dialog>

<p>
    Já possui cadastro?
    <a href="{% url 'accounts:login' %}">Entrar</a>
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
{% block title %}Criar conta | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 5

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 7

```html
<h1>Criar conta</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 9

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 10

```html
    Escolha Doador, Receptor/Solicitante, Observador ou Hemocentro.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 11

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 13

```html
<form method="post">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 15

```html
    {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 17

```html
    {{ form.non_field_errors }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 19

```html
    {% for campo in form %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 21

```html
        {% if campo.name != "aceite_lgpd" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 23

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 24

```html
                <label for="{{ campo.id_for_label }}">
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Apresenta o rótulo de um campo; for liga ao id do controle.

### Linha 25

```html
                    {{ campo.label }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 26

```html
                </label>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 28

```html
                {{ campo }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 30

```html
                {{ campo.errors }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 32

```html
                {% if campo.help_text %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 33

```html
                    <small>{{ campo.help_text }}</small>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 34

```html
                {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 35

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 37

```html
        {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 39

```html
    {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 41

```html
    <!-- O usuário clica diretamente nas palavras para ler os documentos -->
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 42

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 43

```html
        <input
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 44

```html
            type="checkbox"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 45

```html
            id="{{ form.aceite_lgpd.id_for_label }}"
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 46

```html
            name="{{ form.aceite_lgpd.html_name }}"
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 47

```html
            required
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 48

```html
            {% if form.aceite_lgpd.value %}checked{% endif %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 49

```html
        >
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 51

```html
        <label for="{{ form.aceite_lgpd.id_for_label }}">
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Apresenta o rótulo de um campo; for liga ao id do controle.

### Linha 52

```html
            Li e aceito os
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 54

```html
            <a
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 55

```html
                href="#"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 56

```html
                onclick="document.getElementById('modal-termos').showModal(); return false;"
```

Seleciona elemento HTML para leitura ou alteração pelo script. Quando esta linha pertence ao script, return encerra a função e devolve o valor indicado.

### Linha 57

```html
            >
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 58

```html
                Termos de Uso
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 59

```html
            </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 61

```html
            e a
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 63

```html
            <a
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 64

```html
                href="#"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 65

```html
                onclick="document.getElementById('modal-privacidade').showModal(); return false;"
```

Seleciona elemento HTML para leitura ou alteração pelo script. Quando esta linha pertence ao script, return encerra a função e devolve o valor indicado.

### Linha 66

```html
            >
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 67

```html
                Política de Privacidade
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 68

```html
            </a>.
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 69

```html
        </label>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 71

```html
        {{ form.aceite_lgpd.errors }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 72

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 74

```html
    <button type="submit">
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 75

```html
        Criar conta
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 76

```html
    </button>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 78

```html
</form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 80

```html
<!-- Janela dos Termos de Uso. Fica escondida até clicar na palavra. -->
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 81

```html
<dialog id="modal-termos">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 83

```html
    <h2>Termos de Uso</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 85

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 86

```html
        Ao criar uma conta no Elo, o usuário concorda em utilizar
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 87

```html
        o sistema de maneira correta, legal e respeitosa.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 88

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 90

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 91

```html
        O usuário é responsável pelas informações fornecidas no cadastro,
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 92

```html
        pela segurança da sua senha e pelas atividades realizadas em sua conta.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 93

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 95

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 96

```html
        O sistema poderá suspender ou encerrar contas que violem as regras
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 97

```html
        de utilização ou a legislação aplicável.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 98

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 100

```html
    <button
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 101

```html
        type="button"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 102

```html
        onclick="document.getElementById('modal-termos').close();"
```

Seleciona elemento HTML para leitura ou alteração pelo script.

### Linha 103

```html
    >
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 104

```html
        Fechar
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 105

```html
    </button>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 107

```html
</dialog>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 109

```html
<!-- Janela da Política de Privacidade. Fica escondida até clicar na palavra. -->
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 110

```html
<dialog id="modal-privacidade">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 112

```html
    <h2>Política de Privacidade</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 114

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 115

```html
        Os dados informados no cadastro poderão ser utilizados para criar,
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 116

```html
        administrar e proteger a conta do usuário.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 117

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 119

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 120

```html
        As informações devem ser tratadas de acordo com a legislação aplicável,
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 121

```html
        incluindo a Lei Geral de Proteção de Dados.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 122

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 124

```html
    <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 125

```html
        O usuário poderá solicitar informações sobre o uso dos seus dados
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 126

```html
        pelos canais oficiais do sistema.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 127

```html
    </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 129

```html
    <button
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 130

```html
        type="button"
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 131

```html
        onclick="document.getElementById('modal-privacidade').close();"
```

Seleciona elemento HTML para leitura ou alteração pelo script.

### Linha 132

```html
    >
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 133

```html
        Fechar
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 134

```html
    </button>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 136

```html
</dialog>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 138

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 139

```html
    Já possui cadastro?
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 140

```html
    <a href="{% url 'accounts:login' %}">Entrar</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 141

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 143

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

