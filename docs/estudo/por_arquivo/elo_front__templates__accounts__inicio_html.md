# elo_front/templates/accounts/inicio.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [elo_front/templates/accounts/inicio.html](<C:/Users/lb119/Elo/elo_front/templates/accounts/inicio.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% block title %}Elo - Cada gota e um elo de vida{% endblock %}

{% block content %}

<section class="hero" id="sobre">
    <div class="container hero-inner">
        <div class="hero-copy">
            <p class="eyebrow">SISTEMA DE DOACAO DE SANGUE</p>

            <h1>
                Cada gota<br>
                e um <em>elo</em><br>
                de vida.
            </h1>

            <p class="hero-text">
                Conectamos doadores, hemocentros e pacientes
                em um unico sistema, com inteligencia,
                cuidado e a urgencia que salvar vidas exige.
            </p>

            <div class="hero-actions">
                <a class="button button-primary" href="{% url 'accounts:triagem_apresentacao' %}">
                    Quero ser doador
                </a>
                <a class="button button-outline" href="{% url 'accounts:cadastro' %}">
                    Sou do hemocentro
                </a>
            </div>
        </div>
    </div>
</section>

<section class="stock-section" id="estoques">
    <div class="container">
        <div class="section-heading">
            <h2>Situacao dos estoques</h2>
            <p>Sul de Minas</p>
        </div>

        <div class="blood-grid">
            {% for item in estoque_geral %}
                <article class="blood-card">
                    <strong class="blood-type">{{ item.tipo }}</strong>
                    <span class="blood-line"></span>
                    <span class="blood-status
                        {% if item.nivel == 'Critico' %}status-critical
                        {% elif item.nivel == 'Alerta' or item.nivel == 'Baixo' %}status-alert
                        {% else %}status-stable{% endif %}">
                        {{ item.nivel }}
                    </span>
                </article>
            {% empty %}
                <p class="empty-state">Nenhuma informacao de estoque disponivel no momento.</p>
            {% endfor %}
        </div>

        <div class="center-action">
            <a class="button button-outline button-small" href="{% url 'accounts:estoque_publico' %}">
                Ver detalhes por cidade
            </a>
        </div>
    </div>
</section>

<section class="info-section" id="como-doar">
    <div class="container info-grid">
        <div>
            <p class="eyebrow">COMO FUNCIONA</p>
            <h2>Doar sangue e um gesto simples que pode fazer diferenca.</h2>
        </div>

        <div class="info-text">
            <p>
                O Elo ajuda voce a encontrar informacoes, consultar estoques
                e acompanhar oportunidades de doacao.
            </p>
            <a class="text-link" href="{% url 'accounts:triagem_apresentacao' %}">
                Conhecer a triagem
            </a>
        </div>
    </div>
</section>

<section class="faq-section" id="duvidas">
    <div class="container">
        <p class="eyebrow">DUVIDAS</p>
        <h2>Perguntas frequentes</h2>

        <div class="faq-grid">
            <details>
                <summary>Onde posso consultar os estoques?</summary>
                <p>
                    A pagina de estoques publicos permite consultar as informacoes
                    disponibilizadas pelos hemocentros.
                </p>
            </details>

            <details>
                <summary>Como comeco o processo para doar?</summary>
                <p>
                    Acesse a area de triagem para conhecer as etapas iniciais
                    e verificar como continuar.
                </p>
            </details>

            <details>
                <summary>Hemocentros podem participar do Elo?</summary>
                <p>
                    Sim. O cadastro de Hemocentro passa pelo processo de validacao
                    administrativa antes do acesso as funcoes institucionais.
                </p>
            </details>
        </div>
    </div>
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
{% block title %}Elo - Cada gota e um elo de vida{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 5

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 7

```html
<section class="hero" id="sobre">
```

Agrupa uma seção temática da página.

### Linha 8

```html
    <div class="container hero-inner">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 9

```html
        <div class="hero-copy">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 10

```html
            <p class="eyebrow">SISTEMA DE DOACAO DE SANGUE</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 12

```html
            <h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 13

```html
                Cada gota<br>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 14

```html
                e um <em>elo</em><br>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 15

```html
                de vida.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 16

```html
            </h1>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 18

```html
            <p class="hero-text">
```

Agrupa conteúdo em um parágrafo.

### Linha 19

```html
                Conectamos doadores, hemocentros e pacientes
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 20

```html
                em um unico sistema, com inteligencia,
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 21

```html
                cuidado e a urgencia que salvar vidas exige.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 22

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 24

```html
            <div class="hero-actions">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 25

```html
                <a class="button button-primary" href="{% url 'accounts:triagem_apresentacao' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 26

```html
                    Quero ser doador
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 27

```html
                </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 28

```html
                <a class="button button-outline" href="{% url 'accounts:cadastro' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 29

```html
                    Sou do hemocentro
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 30

```html
                </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 31

```html
            </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 32

```html
        </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 33

```html
    </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 34

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 36

```html
<section class="stock-section" id="estoques">
```

Agrupa uma seção temática da página.

### Linha 37

```html
    <div class="container">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 38

```html
        <div class="section-heading">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 39

```html
            <h2>Situacao dos estoques</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 40

```html
            <p>Sul de Minas</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 41

```html
        </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 43

```html
        <div class="blood-grid">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 44

```html
            {% for item in estoque_geral %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 45

```html
                <article class="blood-card">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 46

```html
                    <strong class="blood-type">{{ item.tipo }}</strong>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 47

```html
                    <span class="blood-line"></span>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 48

```html
                    <span class="blood-status
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 49

```html
                        {% if item.nivel == 'Critico' %}status-critical
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 50

```html
                        {% elif item.nivel == 'Alerta' or item.nivel == 'Baixo' %}status-alert
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 51

```html
                        {% else %}status-stable{% endif %}">
```

Encerra o bloco de template correspondente, como condição, laço ou comentário. Inicia o caminho alternativo da condição anterior.

### Linha 52

```html
                        {{ item.nivel }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 53

```html
                    </span>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 54

```html
                </article>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 55

```html
            {% empty %}
```

Apresenta o caso em que a coleção do laço está vazia.

### Linha 56

```html
                <p class="empty-state">Nenhuma informacao de estoque disponivel no momento.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 57

```html
            {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 58

```html
        </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 60

```html
        <div class="center-action">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 61

```html
            <a class="button button-outline button-small" href="{% url 'accounts:estoque_publico' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 62

```html
                Ver detalhes por cidade
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 63

```html
            </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

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
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 68

```html
<section class="info-section" id="como-doar">
```

Agrupa uma seção temática da página.

### Linha 69

```html
    <div class="container info-grid">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 70

```html
        <div>
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 71

```html
            <p class="eyebrow">COMO FUNCIONA</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 72

```html
            <h2>Doar sangue e um gesto simples que pode fazer diferenca.</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 73

```html
        </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 75

```html
        <div class="info-text">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 76

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 77

```html
                O Elo ajuda voce a encontrar informacoes, consultar estoques
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 78

```html
                e acompanhar oportunidades de doacao.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 79

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 80

```html
            <a class="text-link" href="{% url 'accounts:triagem_apresentacao' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 81

```html
                Conhecer a triagem
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 82

```html
            </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 83

```html
        </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 84

```html
    </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 85

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 87

```html
<section class="faq-section" id="duvidas">
```

Agrupa uma seção temática da página.

### Linha 88

```html
    <div class="container">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 89

```html
        <p class="eyebrow">DUVIDAS</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 90

```html
        <h2>Perguntas frequentes</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 92

```html
        <div class="faq-grid">
```

Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.

### Linha 93

```html
            <details>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 94

```html
                <summary>Onde posso consultar os estoques?</summary>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 95

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 96

```html
                    A pagina de estoques publicos permite consultar as informacoes
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 97

```html
                    disponibilizadas pelos hemocentros.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 98

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 99

```html
            </details>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 101

```html
            <details>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 102

```html
                <summary>Como comeco o processo para doar?</summary>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 103

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 104

```html
                    Acesse a area de triagem para conhecer as etapas iniciais
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 105

```html
                    e verificar como continuar.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 106

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 107

```html
            </details>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 109

```html
            <details>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 110

```html
                <summary>Hemocentros podem participar do Elo?</summary>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 111

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 112

```html
                    Sim. O cadastro de Hemocentro passa pelo processo de validacao
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 113

```html
                    administrativa antes do acesso as funcoes institucionais.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 114

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 115

```html
            </details>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 116

```html
        </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 117

```html
    </div>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 118

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 120

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

