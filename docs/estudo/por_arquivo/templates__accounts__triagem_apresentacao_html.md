# templates/accounts/triagem_apresentacao.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/triagem_apresentacao.html](<C:/Users/lb119/Elo/templates/accounts/triagem_apresentacao.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% comment %}
Esta página é pública para que a pessoa entenda a triagem antes de entrar.
Somente os formulários abaixo iniciam um registro no histórico.
{% endcomment %}

{% block title %}Triagem para doação | Elo{% endblock %}

{% block content %}
<h1>Seu gesto de cuidado começa aqui.</h1>

<p>
    Esta triagem foi preparada para orientar você antes da doação, de forma
    simples, tranquila e cuidadosa. As perguntas ajudam a identificar situações
    que podem precisar de mais atenção ou que talvez façam com que a doação
    precise ser adiada.
</p>

<p>
    Para tornar esse processo mais adequado a cada pessoa, você poderá escolher
    entre <strong>duas formas de triagem</strong>. A
    <strong>triagem extensa</strong> é mais completa e indicada principalmente
    para quem nunca doou sangue, está fazendo essa avaliação pela primeira vez
    ou ainda tem dúvidas sobre alguma condição, procedimento, medicamento ou
    situação específica. Por ter mais perguntas e trazer mais detalhes, ela pode
    levar um pouco mais de tempo. Já a <strong>triagem simplificada</strong>
    possui perguntas mais diretas e resumidas, sendo uma opção mais ágil para
    quem já conhece essas informações e precisa apenas verificar se houve alguma
    mudança importante desde a última avaliação.
</p>

<p>
    Algumas questões envolvem sua saúde, seus hábitos e acontecimentos recentes.
    Responda com calma e sinceridade. Se não souber ou não se lembrar de alguma
    informação, tudo bem — basta indicar isso ao longo da triagem.
</p>

<p>
    É importante lembrar que esta triagem é <strong>somente orientativa</strong>.
    Ela não substitui a avaliação feita no hemocentro e não confirma se você pode
    ou não doar sangue. <strong>Quem dará a resposta final será sempre a equipe
    do hemocentro</strong>, após a entrevista e as avaliações realizadas no
    local.
</p>

<p>
    A ideia aqui é apenas ajudar você a chegar mais informado(a), seguro(a) e
    preparado(a) para esse momento.
</p>

<p>
    <strong>Quando estiver pronto(a), escolha a opção que mais combina com você
    e podemos começar.</strong>
</p>

<section>
    <h2>Triagem extensa</h2>
    <p>Questionário completo, indicado para a primeira avaliação ou para revisar todo o histórico.</p>

    {% if pode_iniciar %}
        <form method="post" action="{% url 'accounts:triagem_iniciar' modalidade='extensa' %}">
            {% csrf_token %}
            <label>
                <input type="checkbox" name="aceite_termo" required>
                Li e estou ciente de que a pré-triagem é orientativa e não
                substitui a avaliação clínica presencial do hemocentro.
            </label>
            {% if triagem_extensa_reutilizavel %}
                <label>
                    <input type="checkbox" name="reutilizar_respostas">
                    Reutilizar respostas da última triagem extensa concluída.
                </label>
            {% endif %}
            <button type="submit">Iniciar ou continuar triagem extensa</button>
        </form>
    {% elif not user.is_authenticated %}
        <form method="get" action="{% url 'accounts:cadastro' %}">
            <button type="submit">Criar conta para iniciar a triagem extensa</button>
        </form>
    {% endif %}
</section>

<section>
    <h2>Triagem simplificada</h2>
    <p>Verificação mais rápida para quem já concluiu a extensa e deseja informar mudanças.</p>

    {% if pode_simplificada %}
        <form method="post" action="{% url 'accounts:triagem_iniciar' modalidade='simplificada' %}">
            {% csrf_token %}
            <label>
                <input type="checkbox" name="aceite_termo" required>
                Li e estou ciente de que a pré-triagem é orientativa e não
                substitui a avaliação clínica presencial do hemocentro.
            </label>
            <button type="submit">Iniciar ou continuar triagem simplificada</button>
        </form>
    {% elif pode_iniciar %}
        <p>Conclua uma triagem extensa para liberar esta opção.</p>
    {% elif not user.is_authenticated %}
        <form method="get" action="{% url 'accounts:login' %}">
            <button type="submit">Entrar para continuar uma triagem</button>
        </form>
    {% endif %}
</section>

{% if pode_iniciar %}
    <p><a href="{% url 'accounts:triagem_historico' %}">Ver meu histórico de triagens</a></p>
{% elif user.is_authenticated %}
    <p>A triagem para doação está disponível para o perfil Doador.</p>
{% else %}
    <p>Para responder e salvar sua triagem, crie uma conta ou entre no sistema.</p>
{% endif %}

<p><a href="{% url 'accounts:inicio' %}">Voltar para a página inicial</a></p>
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
Esta página é pública para que a pessoa entenda a triagem antes de entrar.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 5

```html
Somente os formulários abaixo iniciam um registro no histórico.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 6

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 8

```html
{% block title %}Triagem para doação | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 10

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 11

```html
<h1>Seu gesto de cuidado começa aqui.</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 13

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 14

```html
    Esta triagem foi preparada para orientar você antes da doação, de forma
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 15

```html
    simples, tranquila e cuidadosa. As perguntas ajudam a identificar situações
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 16

```html
    que podem precisar de mais atenção ou que talvez façam com que a doação
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 17

```html
    precise ser adiada.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 18

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 20

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 21

```html
    Para tornar esse processo mais adequado a cada pessoa, você poderá escolher
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 22

```html
    entre <strong>duas formas de triagem</strong>. A
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 23

```html
    <strong>triagem extensa</strong> é mais completa e indicada principalmente
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 24

```html
    para quem nunca doou sangue, está fazendo essa avaliação pela primeira vez
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 25

```html
    ou ainda tem dúvidas sobre alguma condição, procedimento, medicamento ou
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 26

```html
    situação específica. Por ter mais perguntas e trazer mais detalhes, ela pode
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 27

```html
    levar um pouco mais de tempo. Já a <strong>triagem simplificada</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 28

```html
    possui perguntas mais diretas e resumidas, sendo uma opção mais ágil para
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 29

```html
    quem já conhece essas informações e precisa apenas verificar se houve alguma
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 30

```html
    mudança importante desde a última avaliação.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

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
    Algumas questões envolvem sua saúde, seus hábitos e acontecimentos recentes.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 35

```html
    Responda com calma e sinceridade. Se não souber ou não se lembrar de alguma
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 36

```html
    informação, tudo bem — basta indicar isso ao longo da triagem.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

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
    É importante lembrar que esta triagem é <strong>somente orientativa</strong>.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 41

```html
    Ela não substitui a avaliação feita no hemocentro e não confirma se você pode
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 42

```html
    ou não doar sangue. <strong>Quem dará a resposta final será sempre a equipe
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 43

```html
    do hemocentro</strong>, após a entrevista e as avaliações realizadas no
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 44

```html
    local.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 45

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 47

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 48

```html
    A ideia aqui é apenas ajudar você a chegar mais informado(a), seguro(a) e
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 49

```html
    preparado(a) para esse momento.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 50

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 52

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 53

```html
    <strong>Quando estiver pronto(a), escolha a opção que mais combina com você
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 54

```html
    e podemos começar.</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 55

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 57

```html
<section>
```

Agrupa uma seção temática da página.

### Linha 58

```html
    <h2>Triagem extensa</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 59

```html
    <p>Questionário completo, indicado para a primeira avaliação ou para revisar todo o histórico.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 61

```html
    {% if pode_iniciar %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 62

```html
        <form method="post" action="{% url 'accounts:triagem_iniciar' modalidade='extensa' %}">
```

Resolve a rota Django pelo nome indicado. Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 63

```html
            {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 64

```html
            <label>
```

Apresenta o rótulo de um campo; for liga ao id do controle.

### Linha 65

```html
                <input type="checkbox" name="aceite_termo" required>
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 66

```html
                Li e estou ciente de que a pré-triagem é orientativa e não
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 67

```html
                substitui a avaliação clínica presencial do hemocentro.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 68

```html
            </label>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 69

```html
            {% if triagem_extensa_reutilizavel %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 70

```html
                <label>
```

Apresenta o rótulo de um campo; for liga ao id do controle.

### Linha 71

```html
                    <input type="checkbox" name="reutilizar_respostas">
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 72

```html
                    Reutilizar respostas da última triagem extensa concluída.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 73

```html
                </label>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 74

```html
            {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 75

```html
            <button type="submit">Iniciar ou continuar triagem extensa</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 76

```html
        </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 77

```html
    {% elif not user.is_authenticated %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 78

```html
        <form method="get" action="{% url 'accounts:cadastro' %}">
```

Resolve a rota Django pelo nome indicado. Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 79

```html
            <button type="submit">Criar conta para iniciar a triagem extensa</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 80

```html
        </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 81

```html
    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 82

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 84

```html
<section>
```

Agrupa uma seção temática da página.

### Linha 85

```html
    <h2>Triagem simplificada</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 86

```html
    <p>Verificação mais rápida para quem já concluiu a extensa e deseja informar mudanças.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 88

```html
    {% if pode_simplificada %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 89

```html
        <form method="post" action="{% url 'accounts:triagem_iniciar' modalidade='simplificada' %}">
```

Resolve a rota Django pelo nome indicado. Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 90

```html
            {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 91

```html
            <label>
```

Apresenta o rótulo de um campo; for liga ao id do controle.

### Linha 92

```html
                <input type="checkbox" name="aceite_termo" required>
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 93

```html
                Li e estou ciente de que a pré-triagem é orientativa e não
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 94

```html
                substitui a avaliação clínica presencial do hemocentro.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 95

```html
            </label>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 96

```html
            <button type="submit">Iniciar ou continuar triagem simplificada</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 97

```html
        </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 98

```html
    {% elif pode_iniciar %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 99

```html
        <p>Conclua uma triagem extensa para liberar esta opção.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 100

```html
    {% elif not user.is_authenticated %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 101

```html
        <form method="get" action="{% url 'accounts:login' %}">
```

Resolve a rota Django pelo nome indicado. Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 102

```html
            <button type="submit">Entrar para continuar uma triagem</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 103

```html
        </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 104

```html
    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 105

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 107

```html
{% if pode_iniciar %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 108

```html
    <p><a href="{% url 'accounts:triagem_historico' %}">Ver meu histórico de triagens</a></p>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre. Agrupa conteúdo em um parágrafo.

### Linha 109

```html
{% elif user.is_authenticated %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 110

```html
    <p>A triagem para doação está disponível para o perfil Doador.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 111

```html
{% else %}
```

Inicia o caminho alternativo da condição anterior.

### Linha 112

```html
    <p>Para responder e salvar sua triagem, crie uma conta ou entre no sistema.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 113

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 115

```html
<p><a href="{% url 'accounts:inicio' %}">Voltar para a página inicial</a></p>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre. Agrupa conteúdo em um parágrafo.

### Linha 116

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

