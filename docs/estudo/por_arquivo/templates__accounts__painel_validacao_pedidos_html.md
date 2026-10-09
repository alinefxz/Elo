# templates/accounts/painel_validacao_pedidos.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/painel_validacao_pedidos.html](<C:/Users/lb119/Elo/templates/accounts/painel_validacao_pedidos.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% block title %}Análise de solicitações | Elo{% endblock %}

{% block content %}
<h1>Solicitações recebidas</h1>
<p>Somente após sua análise uma necessidade será publicada oficialmente.</p>

<form method="get">
    <label for="status">Filtrar por status:</label>
    <select id="status" name="status">
        <option value="">Todos</option>
        {% for codigo, nome in status_opcoes %}
            <option value="{{ codigo }}">{{ nome }}</option>
        {% endfor %}
    </select>
    <button type="submit">Filtrar</button>
</form>

<p>
    <a href="{% url 'accounts:dashboard' %}">Voltar ao painel</a>
    · <a href="{% url 'accounts:estoque_hemocentro' %}">Meu estoque</a>
</p>

{% for pedido in solicitacoes %}

    <section>
        <h2>{{ pedido.titulo }}</h2>

        <p><strong>Solicitante:</strong> {{ pedido.nome_solicitante }}</p>
        <p><strong>Contato:</strong> {{ pedido.contato }}</p>
        <p><strong>Tipo:</strong> {{ pedido.tipo_sanguineo }}</p>
        <p><strong>Cidade:</strong> {{ pedido.cidade }}</p>
        <p><strong>Urgência:</strong> {{ pedido.get_urgencia_display }}</p>
        <p><strong>Hemocentro:</strong> {{ pedido.hemocentro_destino.nome }}</p>
        <p><strong>Status:</strong> {{ pedido.get_status_display }}</p>
        <p><strong>Descrição:</strong> {{ pedido.descricao }}</p>

        {% if pedido.informacoes_complementares %}
            <p><strong>Informações complementares:</strong> {{ pedido.informacoes_complementares }}</p>
        {% endif %}

        {% if pedido.duplicidade_suspeita %}
            <p><strong>Atenção:</strong> há solicitação semelhante em análise.</p>
        {% endif %}

        {% if pedido.status != "PUBLICADA" and pedido.status != "RECUSADA" %}
            <form method="post" action="{% url 'accounts:aprovar_pedido' pedido.id_pedido %}">
                {% csrf_token %}
                <textarea name="motivo" rows="2" placeholder="Observação da análise"></textarea>
                <button type="submit">Aprovar e publicar</button>
            </form>
            <form method="post" action="{% url 'accounts:solicitar_correcao_pedido' pedido.id_pedido %}">
                {% csrf_token %}
                <textarea name="motivo" rows="2" required placeholder="O que deve ser corrigido?"></textarea>
                <button type="submit">Solicitar correção</button>
            </form>
            <form method="post" action="{% url 'accounts:recusar_pedido' pedido.id_pedido %}">
                {% csrf_token %}
                <textarea name="motivo" rows="2" placeholder="Motivo da recusa"></textarea>
                <button type="submit">Recusar</button>
  </form>
            <form method="post" action="{% url 'accounts:marcar_pedido_suspeito' pedido.id_pedido %}">
                {% csrf_token %}
                <textarea name="motivo" rows="2" required placeholder="Explique por que o pedido parece suspeito"></textarea>
                <button type="submit">Marcar como suspeito</button>
            </form>
        {% endif %}
    </section>
{% empty %}
    <p>Nenhuma solicitação aguardando análise.</p>
{% endfor %}

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
{% block title %}Análise de solicitações | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 5

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 6

```html
<h1>Solicitações recebidas</h1>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 7

```html
<p>Somente após sua análise uma necessidade será publicada oficialmente.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 9

```html
<form method="get">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 10

```html
    <label for="status">Filtrar por status:</label>
```

Apresenta o rótulo de um campo; for liga ao id do controle.

### Linha 11

```html
    <select id="status" name="status">
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 12

```html
        <option value="">Todos</option>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 13

```html
        {% for codigo, nome in status_opcoes %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 14

```html
            <option value="{{ codigo }}">{{ nome }}</option>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 15

```html
        {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 16

```html
    </select>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 17

```html
    <button type="submit">Filtrar</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 18

```html
</form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 20

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 21

```html
    <a href="{% url 'accounts:dashboard' %}">Voltar ao painel</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 22

```html
    · <a href="{% url 'accounts:estoque_hemocentro' %}">Meu estoque</a>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 23

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 25

```html
{% for pedido in solicitacoes %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 27

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 28

```html
        <h2>{{ pedido.titulo }}</h2>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 30

```html
        <p><strong>Solicitante:</strong> {{ pedido.nome_solicitante }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 31

```html
        <p><strong>Contato:</strong> {{ pedido.contato }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 32

```html
        <p><strong>Tipo:</strong> {{ pedido.tipo_sanguineo }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 33

```html
        <p><strong>Cidade:</strong> {{ pedido.cidade }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 34

```html
        <p><strong>Urgência:</strong> {{ pedido.get_urgencia_display }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 35

```html
        <p><strong>Hemocentro:</strong> {{ pedido.hemocentro_destino.nome }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 36

```html
        <p><strong>Status:</strong> {{ pedido.get_status_display }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 37

```html
        <p><strong>Descrição:</strong> {{ pedido.descricao }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 39

```html
        {% if pedido.informacoes_complementares %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 40

```html
            <p><strong>Informações complementares:</strong> {{ pedido.informacoes_complementares }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 41

```html
        {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 43

```html
        {% if pedido.duplicidade_suspeita %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 44

```html
            <p><strong>Atenção:</strong> há solicitação semelhante em análise.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 45

```html
        {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 47

```html
        {% if pedido.status != "PUBLICADA" and pedido.status != "RECUSADA" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 48

```html
            <form method="post" action="{% url 'accounts:aprovar_pedido' pedido.id_pedido %}">
```

Resolve a rota Django pelo nome indicado. Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 49

```html
                {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 50

```html
                <textarea name="motivo" rows="2" placeholder="Observação da análise"></textarea>
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 51

```html
                <button type="submit">Aprovar e publicar</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 52

```html
            </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 53

```html
            <form method="post" action="{% url 'accounts:solicitar_correcao_pedido' pedido.id_pedido %}">
```

Resolve a rota Django pelo nome indicado. Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 54

```html
                {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 55

```html
                <textarea name="motivo" rows="2" required placeholder="O que deve ser corrigido?"></textarea>
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 56

```html
                <button type="submit">Solicitar correção</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 57

```html
            </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 58

```html
            <form method="post" action="{% url 'accounts:recusar_pedido' pedido.id_pedido %}">
```

Resolve a rota Django pelo nome indicado. Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 59

```html
                {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 60

```html
                <textarea name="motivo" rows="2" placeholder="Motivo da recusa"></textarea>
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 61

```html
                <button type="submit">Recusar</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 62

```html
  </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 63

```html
            <form method="post" action="{% url 'accounts:marcar_pedido_suspeito' pedido.id_pedido %}">
```

Resolve a rota Django pelo nome indicado. Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 64

```html
                {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 65

```html
                <textarea name="motivo" rows="2" required placeholder="Explique por que o pedido parece suspeito"></textarea>
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 66

```html
                <button type="submit">Marcar como suspeito</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 67

```html
            </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 68

```html
        {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 69

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 70

```html
{% empty %}
```

Apresenta o caso em que a coleção do laço está vazia.

### Linha 71

```html
    <p>Nenhuma solicitação aguardando análise.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 72

```html
{% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 74

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

