# templates/accounts/compatibilidade_sanguinea.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/compatibilidade_sanguinea.html](<C:/Users/lb119/Elo/templates/accounts/compatibilidade_sanguinea.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% block title %}Compatibilidade sanguinea | Elo{% endblock %}

{% block content %}
<h1>Compatibilidade sanguinea</h1>

<p>
    Consulte quais tipos sanguineos podem doar e receber sangue entre si,
    considerando o sistema ABO e o fator Rh.
</p>

<section>
    <h2>Consultar por tipo</h2>

    <form method="get">
        <label for="tipo">Tipo sanguineo</label>
        <select id="tipo" name="tipo">
            <option value="">Selecione um tipo</option>
            {% for tipo in tipos_sanguineos %}
                <option value="{{ tipo }}" {% if tipo == tipo_selecionado %}selected{% endif %}>
                    {{ tipo }}
                </option>
            {% endfor %}
        </select>
        <button type="submit">Consultar</button>
    </form>

    {% if tipo_invalido %}
        <p>Tipo sanguineo invalido. Selecione uma das opcoes da tabela.</p>
    {% endif %}

    {% if compatibilidade_selecionada %}
        <h3>Resultado para {{ compatibilidade_selecionada.tipo }}</h3>
        <p><strong>Pode doar para:</strong> {{ compatibilidade_selecionada.doar_para|join:", " }}</p>
        <p><strong>Pode receber de:</strong> {{ compatibilidade_selecionada.receber_de|join:", " }}</p>
    {% endif %}
</section>

<section>
    <h2>Tabela de compatibilidade</h2>

    <table border="1" cellpadding="12" cellspacing="0" width="100%">
        <caption>
            Compatibilidade sanguinea considerando sistema ABO e fator Rh
        </caption>

        <thead>
            <tr>
                <th scope="col" width="10%">Tipo</th>
                <th scope="col" width="35%">Pode doar para</th>
                <th scope="col" width="35%">Pode receber de</th>
                <th scope="col" width="20%">Populacao aproximada</th>
            </tr>
        </thead>

        <tbody>
            {% for item in tabela_compatibilidade %}
                <tr>
                    <th scope="row">{{ item.tipo }}</th>
                    <td>{{ item.doar_para|join:", " }}</td>
                    <td>{{ item.receber_de|join:", " }}</td>
                    <td>{{ item.populacao }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</section>

<section>
    <h2>Informacoes importantes</h2>
    <ul>
        <li>O tipo O- pode doar hemacias para todos os tipos sanguineos.</li>
        <li>O tipo AB+ pode receber hemacias de todos os tipos sanguineos.</li>
        <li>Enquanto a triagem nao estiver implementada, esta tela e apenas informativa.</li>
        <li>A compatibilidade real deve sempre ser confirmada por profissionais de saude e exames laboratoriais.</li>
    </ul>
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
{% block title %}Compatibilidade sanguinea | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 5

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 6

```html
<h1>Compatibilidade sanguinea</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 8

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 9

```html
    Consulte quais tipos sanguineos podem doar e receber sangue entre si,
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 10

```html
    considerando o sistema ABO e o fator Rh.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 11

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 13

```html
<section>
```

Agrupa uma seção temática da página.

### Linha 14

```html
    <h2>Consultar por tipo</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 16

```html
    <form method="get">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 17

```html
        <label for="tipo">Tipo sanguineo</label>
```

Apresenta o rótulo de um campo; for liga ao id do controle.

### Linha 18

```html
        <select id="tipo" name="tipo">
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 19

```html
            <option value="">Selecione um tipo</option>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 20

```html
            {% for tipo in tipos_sanguineos %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 21

```html
                <option value="{{ tipo }}" {% if tipo == tipo_selecionado %}selected{% endif %}>
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota. Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 22

```html
                    {{ tipo }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 23

```html
                </option>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 24

```html
            {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 25

```html
        </select>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 26

```html
        <button type="submit">Consultar</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 27

```html
    </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 29

```html
    {% if tipo_invalido %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 30

```html
        <p>Tipo sanguineo invalido. Selecione uma das opcoes da tabela.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 31

```html
    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 33

```html
    {% if compatibilidade_selecionada %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 34

```html
        <h3>Resultado para {{ compatibilidade_selecionada.tipo }}</h3>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 35

```html
        <p><strong>Pode doar para:</strong> {{ compatibilidade_selecionada.doar_para|join:", " }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 36

```html
        <p><strong>Pode receber de:</strong> {{ compatibilidade_selecionada.receber_de|join:", " }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 37

```html
    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 38

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 40

```html
<section>
```

Agrupa uma seção temática da página.

### Linha 41

```html
    <h2>Tabela de compatibilidade</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 43

```html
    <table border="1" cellpadding="12" cellspacing="0" width="100%">
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 44

```html
        <caption>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 45

```html
            Compatibilidade sanguinea considerando sistema ABO e fator Rh
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 46

```html
        </caption>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 48

```html
        <thead>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 49

```html
            <tr>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 50

```html
                <th scope="col" width="10%">Tipo</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 51

```html
                <th scope="col" width="35%">Pode doar para</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 52

```html
                <th scope="col" width="35%">Pode receber de</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 53

```html
                <th scope="col" width="20%">Populacao aproximada</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 54

```html
            </tr>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 55

```html
        </thead>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 57

```html
        <tbody>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 58

```html
            {% for item in tabela_compatibilidade %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 59

```html
                <tr>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 60

```html
                    <th scope="row">{{ item.tipo }}</th>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 61

```html
                    <td>{{ item.doar_para|join:", " }}</td>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 62

```html
                    <td>{{ item.receber_de|join:", " }}</td>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 63

```html
                    <td>{{ item.populacao }}</td>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 64

```html
                </tr>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 65

```html
            {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 66

```html
        </tbody>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 67

```html
    </table>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 68

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 70

```html
<section>
```

Agrupa uma seção temática da página.

### Linha 71

```html
    <h2>Informacoes importantes</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 72

```html
    <ul>
```

Abre lista; ul é não numerada e ol é numerada.

### Linha 73

```html
        <li>O tipo O- pode doar hemacias para todos os tipos sanguineos.</li>
```

Define um item da lista.

### Linha 74

```html
        <li>O tipo AB+ pode receber hemacias de todos os tipos sanguineos.</li>
```

Define um item da lista.

### Linha 75

```html
        <li>Enquanto a triagem nao estiver implementada, esta tela e apenas informativa.</li>
```

Define um item da lista.

### Linha 76

```html
        <li>A compatibilidade real deve sempre ser confirmada por profissionais de saude e exames laboratoriais.</li>
```

Define um item da lista.

### Linha 77

```html
    </ul>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 78

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 79

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

