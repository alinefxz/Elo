# templates/accounts/dashboard.html: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Template de apresentacao; compare variaveis recebidas e view que o renderiza.

**Arquivo original:** [templates/accounts/dashboard.html](<C:/Users/lb119/Elo/templates/accounts/dashboard.html>). As linhas referem-se à cópia desta data.

## Código integral

``````html
{% extends "base.html" %}

{% comment %}
RESUMO DO ARQUIVO
=================
Painel protegido do usuario cadastrado.

A view envia dois dicionarios principais:
- painel: textos gerais do perfil logado;
- visibilidade: regras que dizem quais blocos cada usuario pode enxergar.

Assim, a particularizacao fica centralizada na view e o template apenas mostra
ou esconde as secoes correspondentes.
{% endcomment %}

{% block title %}Painel | Elo{% endblock %}

{% block content %}

<!-- get_short_name retorna o primeiro nome ou, se vazio, o e-mail. -->
<h1>Ola, {{ user.get_short_name }}!</h1>

<p>
    <strong>{{ painel.rotulo }}</strong>
</p>

{% if preferencia_convocacao %}
    <section>
        <h2>Alertas de doação</h2>
        <p>Receba até {{ convocacao_limite }} alerta(s) a cada {{ convocacao_intervalo_horas }} horas,
            quando houver compatibilidade e sua última triagem concluída permitir.</p>
        <form method="post">
            {% csrf_token %}
            {{ preferencia_convocacao.as_p }}
            <button type="submit">Salvar preferência</button>
        </form>
    </section>
{% endif %}

    <section id="notificacoes">
        <h2>Notificações</h2>
        <p>{{ notificacoes_nao_lidas }} não lida(s).</p>

        <ul>
            {% for notificacao in notificacoes_dashboard %}
                <li>
                    <strong>{{ notificacao.titulo }}</strong><br>
                    <span>{{ notificacao.get_tipo_display }} · {{ notificacao.criada_em|date:"d/m/Y H:i" }}</span><br>
                    <span>{% if notificacao.lida %}Lida{% else %}Não lida{% endif %}</span><br>
                    {{ notificacao.mensagem }}

                    {% if notificacao.url_destino %}
                        <br>
                        <a href="{{ notificacao.url_destino }}">
                            {% if notificacao.tipo == "ESTOQUE_CRITICO" or notificacao.tipo == "ESTOQUE_BAIXO" %}Ver estoque{% elif notificacao.tipo == "PEDIDO_COMPATIVEL" %}Ver pedido{% else %}Ver detalhes{% endif %}
                        </a>
                    {% endif %}
                    {% if not notificacao.lida %}
                        <form method="post">
                            {% csrf_token %}
                            <input type="hidden" name="acao" value="marcar_notificacao_lida">
                            <input type="hidden" name="id_notificacao" value="{{ notificacao.pk }}">
                            <button type="submit">Marcar como lida</button>
                        </form>
                    {% endif %}
                </li>
            {% empty %}
                <li>Você ainda não tem notificações.</li>
            {% endfor %}
        </ul>
        {% if notificacoes_dashboard.has_other_pages %}
            <nav aria-label="Páginas de notificações">
                {% if notificacoes_dashboard.has_previous %}
                    <a href="?pagina_notificacoes={{ notificacoes_dashboard.previous_page_number }}#notificacoes">Anterior</a>
                {% endif %}
                <span>Página {{ notificacoes_dashboard.number }} de {{ notificacoes_dashboard.paginator.num_pages }}</span>
                {% if notificacoes_dashboard.has_next %}
                    <a href="?pagina_notificacoes={{ notificacoes_dashboard.next_page_number }}#notificacoes">Próxima</a>
                {% endif %}
            </nav>
        {% endif %}
    </section>

<section>
    <h2>{{ painel.titulo }}</h2>
    <p>{{ painel.descricao }}</p>

    <ul>
        {% for acao in painel.acoes %}
            <li>{{ acao }}</li>
        {% endfor %}
    </ul>
</section>


{% comment %}
=================================================================
TRIAGEM
=================================================================
Doador e Receptor/Solicitante podem acessar a triagem. Outros perfis nao
devem ver esse bloco no dashboard.
{% endcomment %}

{% if visibilidade.mostra_triagem %}

    <section>
        <h2>Triagem para doação</h2>

        {% if user.perfil == "DOADOR" %}

            <p>
                Responda à triagem inicial antes de procurar um posto de coleta.
            </p>

        {% elif user.perfil == "RECEPTOR" %}

            <p>
                Mesmo sendo Receptor, você pode responder à triagem
                caso também queira doar sangue.
            </p>

        {% endif %}

        <p>
            <a href="{% url 'accounts:triagem_apresentacao' %}">
                Escolher ou continuar uma triagem
            </a>
        </p>

        <p>
            <a href="{% url 'accounts:triagem_historico' %}">
                Ver meu histórico de triagens
            </a>
        </p>

        {% if ultima_triagem %}
            <p>
                <strong>Última triagem:</strong>
                {{ ultima_triagem.get_modalidade_display }} -
                {{ ultima_triagem.get_status_display }}
            </p>
        {% endif %}
    </section>

{% endif %}


{% comment %}
=================================================================
CAMPANHAS
=================================================================
Doador e Observador veem campanhas publicas. Hemocentro pendente nao publica
campanha; Hemocentro aprovado pode ganhar uma tela propria futuramente.
{% endcomment %}

{% if visibilidade.mostra_campanhas %}

    <section>
        <h2>Campanhas e mutiroes</h2>

        <ul>
            {% for campanha in campanhas_ativas %}
                <li>
                    <strong>{{ campanha.titulo }}</strong><br>
                    {{ campanha.cidade }} - {{ campanha.data }}
                </li>
            {% empty %}
                <li>Nenhuma campanha ativa no momento.</li>
            {% endfor %}
        </ul>
    </section>

{% endif %}


{% comment %}
=================================================================
ESTOQUE PUBLICO
=================================================================
Doador, Receptor e Observador podem consultar a situacao publica dos estoques.
Gerenciar estoque e diferente de consultar estoque publico.
{% endcomment %}

{% if visibilidade.mostra_estoque_publico %}

    <section>
        <h2>Estoque público</h2>

        <p>
            Consulte os estoques informados pelos Hemocentros aprovados.
        </p>

        <p>
            <a href="{% url 'accounts:estoque_publico' %}">
                Ver estoque público completo
            </a>
        </p>

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
                {% empty %}
                    <tr>
                        <td colspan="3">
                            Nenhum dado de estoque disponivel.
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </section>

{% endif %}


{% comment %}
=================================================================
PEDIDOS
=================================================================
Doador, Receptor, Observador e Hemocentro podem ver pedidos ativos. O
Administrador nao precisa receber essa lista no painel administrativo.
{% endcomment %}

{% if visibilidade.mostra_pedidos %}

    <section>
        <h2>Pedidos ativos</h2>
        <p><a href="{% url 'accounts:consultar_pedidos' %}">Consultar pedidos ativos</a></p>

        {% if visibilidade.pode_solicitar_divulgacao %}
            <p>
                <a href="{% url 'accounts:pedido_publicar' %}">
                    Solicitar divulgação de necessidade
                </a>
            </p>
            <p>
                <a href="{% url 'accounts:minhas_solicitacoes' %}">
                    Acompanhar minhas solicitações
                </a>
            </p>
        {% endif %}

        <ul>
            {% for pedido in pedidos_ativos %}
                <li>
                    <strong>{{ pedido.titulo }}</strong><br>
                    {{ pedido.tipo_sanguineo }} -
                    {{ pedido.cidade }} -
                    Urgencia {{ pedido.urgencia }}
                </li>
            {% empty %}
                <li>Nenhum pedido ativo no momento.</li>
            {% endfor %}
        </ul>
    </section>

{% endif %}

{% if visibilidade.pode_analisar_pedidos %}
    <section>
        <h2>Análise de solicitações</h2>
        <p>Somente o Hemocentro aprovado pode decidir pela publicação.</p>
        <p>
            <a href="{% url 'accounts:painel_pedidos_hemocentro' %}">
                Analisar solicitações recebidas
            </a>
        </p>
    </section>
{% endif %}


{% comment %}
=================================================================
POSTOS DE COLETA
=================================================================
Doador e Observador recebem a lista de postos no dashboard. Outros perfis
podem acessar informacoes publicas pela pagina inicial quando necessario.
{% endcomment %}

{% if visibilidade.mostra_postos %}

    <section>
        <h2>Postos de coleta</h2>

        <ul>
            {% for posto in postos %}
                <li>
                    <strong>{{ posto.nome }}</strong><br>
                    {{ posto.cidade }}/{{ posto.estado }} -
                    {{ posto.horario }}
                </li>
            {% empty %}
                <li>Nenhum posto de coleta cadastrado.</li>
            {% endfor %}
        </ul>
    </section>

{% endif %}


{% comment %}
=================================================================
STATUS DA VALIDACAO DO HEMOCENTRO
=================================================================
Mostra para o Hemocentro a situacao atual do cadastro institucional.
Somente Hemocentro aprovado recebe o link para gerenciar estoque.
{% endcomment %}

{% if visibilidade.mostra_status_hemocentro %}

    <section>

        <h2>Status da validação institucional</h2>

        {% if request.user.status_validacao == "PENDENTE" %}

            <h3>Pendente</h3>

            <p>
                Seu cadastro de Hemocentro está aguardando análise
                de um administrador.
            </p>

            <p>
                Enquanto a análise não for concluída, a publicação
                de estoques e campanhas permanece bloqueada.
            </p>

        {% elif request.user.status_validacao == "APROVADO" %}

            <h3>Aprovado</h3>

            <p>
                Seu Hemocentro foi aprovado pelo administrador.
            </p>

            <p>
                O Hemocentro está autorizado a cadastrar e atualizar estoques.
            </p>

            {% if visibilidade.pode_gerenciar_estoque %}
                <p>
                    <a href="{% url 'accounts:estoque_hemocentro' %}">
                        Cadastrar e atualizar estoque
                    </a>
                </p>
            {% endif %}

        {% elif request.user.status_validacao == "RECUSADO" %}

            <h3>Cadastro recusado</h3>

            <p>
                O cadastro do Hemocentro foi recusado.
            </p>

            {% if validacao_atual and validacao_atual.parecer %}

                <p>
                    <strong>Parecer do administrador:</strong>
                    {{ validacao_atual.parecer }}
                </p>

                <p>
                    <strong>Data da análise:</strong>
                    {{ validacao_atual.data_analise|date:"d/m/Y H:i" }}
                </p>

            {% endif %}

        {% elif request.user.status_validacao == "CORRECAO" %}

            <h3>Correção necessária</h3>

            <p>
                O administrador solicitou alterações no cadastro
                do Hemocentro.
            </p>

            {% if validacao_atual and validacao_atual.parecer %}

                <p>
                    <strong>Orientação do administrador:</strong>
                    {{ validacao_atual.parecer }}
                </p>

                <p>
                    <strong>Data da análise:</strong>
                    {{ validacao_atual.data_analise|date:"d/m/Y H:i" }}
                </p>

            {% endif %}

        {% endif %}

    </section>

{% endif %}


{% comment %}
=================================================================
ACESSO DO ADMINISTRADOR
=================================================================
Mostra o link para a tela de aprovação quando o usuário é administrador.
Administrador nao e tratado como Hemocentro.
{% endcomment %}

{% if visibilidade.pode_aprovar_hemocentros %}
    <section>
        <h2>Validação de Hemocentros</h2>

        <p>
            Analise cadastros pendentes e libere o acesso institucional
            somente depois da aprovação.
        </p>

        <p>
            <a href="{% url 'accounts:painel_aprovacao_hemocentros' %}">
                Acessar aprovação de Hemocentros
            </a>
        </p>
    </section>
{% endif %}

{% if visibilidade.pode_moderar_pedidos %}
    <section>
        <h2>Moderação de pedidos</h2>
        <p>Analise pedidos suspeitos ou pendentes sem publicar em nome do Hemocentro.</p>
        <p><a href="{% url 'accounts:painel_validacao_pedidos' %}">Acessar moderação de pedidos</a></p>
    </section>
{% endif %}
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
Painel protegido do usuario cadastrado.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 8

```html
A view envia dois dicionarios principais:
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 9

```html
- painel: textos gerais do perfil logado;
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 10

```html
- visibilidade: regras que dizem quais blocos cada usuario pode enxergar.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 12

```html
Assim, a particularizacao fica centralizada na view e o template apenas mostra
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 13

```html
ou esconde as secoes correspondentes.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 14

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 16

```html
{% block title %}Painel | Elo{% endblock %}
```

Abre uma região que o template filho preenche. Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 18

```html
{% block content %}
```

Abre uma região que o template filho preenche.

### Linha 20

```html
<!-- get_short_name retorna o primeiro nome ou, se vazio, o e-mail. -->
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 21

```html
<h1>Ola, {{ user.get_short_name }}!</h1>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 23

```html
<p>
```

Agrupa conteúdo em um parágrafo.

### Linha 24

```html
    <strong>{{ painel.rotulo }}</strong>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 25

```html
</p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 27

```html
{% if preferencia_convocacao %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 28

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 29

```html
        <h2>Alertas de doação</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 30

```html
        <p>Receba até {{ convocacao_limite }} alerta(s) a cada {{ convocacao_intervalo_horas }} horas,
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 31

```html
            quando houver compatibilidade e sua última triagem concluída permitir.</p>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 32

```html
        <form method="post">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 33

```html
            {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 34

```html
            {{ preferencia_convocacao.as_p }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 35

```html
            <button type="submit">Salvar preferência</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 36

```html
        </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 37

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 38

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 40

```html
    <section id="notificacoes">
```

Agrupa uma seção temática da página.

### Linha 41

```html
        <h2>Notificações</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 42

```html
        <p>{{ notificacoes_nao_lidas }} não lida(s).</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 44

```html
        <ul>
```

Abre lista; ul é não numerada e ol é numerada.

### Linha 45

```html
            {% for notificacao in notificacoes_dashboard %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 46

```html
                <li>
```

Define um item da lista.

### Linha 47

```html
                    <strong>{{ notificacao.titulo }}</strong><br>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 48

```html
                    <span>{{ notificacao.get_tipo_display }} · {{ notificacao.criada_em|date:"d/m/Y H:i" }}</span><br>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 49

```html
                    <span>{% if notificacao.lida %}Lida{% else %}Não lida{% endif %}</span><br>
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota. Encerra o bloco de template correspondente, como condição, laço ou comentário. Inicia o caminho alternativo da condição anterior.

### Linha 50

```html
                    {{ notificacao.mensagem }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 52

```html
                    {% if notificacao.url_destino %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 53

```html
                        <br>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 54

```html
                        <a href="{{ notificacao.url_destino }}">
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 55

```html
                            {% if notificacao.tipo == "ESTOQUE_CRITICO" or notificacao.tipo == "ESTOQUE_BAIXO" %}Ver estoque{% elif notificacao.tipo == "PEDIDO_COMPATIVEL" %}Ver pedido{% else %}Ver detalhes{% endif %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota. Encerra o bloco de template correspondente, como condição, laço ou comentário. Inicia o caminho alternativo da condição anterior.

### Linha 56

```html
                        </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 57

```html
                    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 58

```html
                    {% if not notificacao.lida %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 59

```html
                        <form method="post">
```

Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.

### Linha 60

```html
                            {% csrf_token %}
```

Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.

### Linha 61

```html
                            <input type="hidden" name="acao" value="marcar_notificacao_lida">
```

Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 62

```html
                            <input type="hidden" name="id_notificacao" value="{{ notificacao.pk }}">
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.

### Linha 63

```html
                            <button type="submit">Marcar como lida</button>
```

Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.

### Linha 64

```html
                        </form>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 65

```html
                    {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 66

```html
                </li>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 67

```html
            {% empty %}
```

Apresenta o caso em que a coleção do laço está vazia.

### Linha 68

```html
                <li>Você ainda não tem notificações.</li>
```

Define um item da lista.

### Linha 69

```html
            {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 70

```html
        </ul>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 71

```html
        {% if notificacoes_dashboard.has_other_pages %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 72

```html
            <nav aria-label="Páginas de notificações">
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 73

```html
                {% if notificacoes_dashboard.has_previous %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 74

```html
                    <a href="?pagina_notificacoes={{ notificacoes_dashboard.previous_page_number }}#notificacoes">Anterior</a>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 75

```html
                {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 76

```html
                <span>Página {{ notificacoes_dashboard.number }} de {{ notificacoes_dashboard.paginator.num_pages }}</span>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 77

```html
                {% if notificacoes_dashboard.has_next %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 78

```html
                    <a href="?pagina_notificacoes={{ notificacoes_dashboard.next_page_number }}#notificacoes">Próxima</a>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 79

```html
                {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 80

```html
            </nav>
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
    <h2>{{ painel.titulo }}</h2>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 86

```html
    <p>{{ painel.descricao }}</p>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Agrupa conteúdo em um parágrafo.

### Linha 88

```html
    <ul>
```

Abre lista; ul é não numerada e ol é numerada.

### Linha 89

```html
        {% for acao in painel.acoes %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 90

```html
            <li>{{ acao }}</li>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Define um item da lista.

### Linha 91

```html
        {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 92

```html
    </ul>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 93

```html
</section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 96

```html
{% comment %}
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 97

```html
=================================================================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 98

```html
TRIAGEM
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 99

```html
=================================================================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 100

```html
Doador e Receptor/Solicitante podem acessar a triagem. Outros perfis nao
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 101

```html
devem ver esse bloco no dashboard.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 102

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 104

```html
{% if visibilidade.mostra_triagem %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 106

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 107

```html
        <h2>Triagem para doação</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 109

```html
        {% if user.perfil == "DOADOR" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 111

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 112

```html
                Responda à triagem inicial antes de procurar um posto de coleta.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 113

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 115

```html
        {% elif user.perfil == "RECEPTOR" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 117

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 118

```html
                Mesmo sendo Receptor, você pode responder à triagem
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 119

```html
                caso também queira doar sangue.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 120

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 122

```html
        {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 124

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 125

```html
            <a href="{% url 'accounts:triagem_apresentacao' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 126

```html
                Escolher ou continuar uma triagem
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 127

```html
            </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 128

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 130

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 131

```html
            <a href="{% url 'accounts:triagem_historico' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 132

```html
                Ver meu histórico de triagens
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 133

```html
            </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 134

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 136

```html
        {% if ultima_triagem %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 137

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 138

```html
                <strong>Última triagem:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 139

```html
                {{ ultima_triagem.get_modalidade_display }} -
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 140

```html
                {{ ultima_triagem.get_status_display }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 141

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 142

```html
        {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 143

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 145

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 148

```html
{% comment %}
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 149

```html
=================================================================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 150

```html
CAMPANHAS
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 151

```html
=================================================================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 152

```html
Doador e Observador veem campanhas publicas. Hemocentro pendente nao publica
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 153

```html
campanha; Hemocentro aprovado pode ganhar uma tela propria futuramente.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 154

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 156

```html
{% if visibilidade.mostra_campanhas %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 158

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 159

```html
        <h2>Campanhas e mutiroes</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 161

```html
        <ul>
```

Abre lista; ul é não numerada e ol é numerada.

### Linha 162

```html
            {% for campanha in campanhas_ativas %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 163

```html
                <li>
```

Define um item da lista.

### Linha 164

```html
                    <strong>{{ campanha.titulo }}</strong><br>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 165

```html
                    {{ campanha.cidade }} - {{ campanha.data }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 166

```html
                </li>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 167

```html
            {% empty %}
```

Apresenta o caso em que a coleção do laço está vazia.

### Linha 168

```html
                <li>Nenhuma campanha ativa no momento.</li>
```

Define um item da lista.

### Linha 169

```html
            {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 170

```html
        </ul>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 171

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 173

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 176

```html
{% comment %}
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 177

```html
=================================================================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 178

```html
ESTOQUE PUBLICO
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 179

```html
=================================================================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 180

```html
Doador, Receptor e Observador podem consultar a situacao publica dos estoques.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 181

```html
Gerenciar estoque e diferente de consultar estoque publico.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 182

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 184

```html
{% if visibilidade.mostra_estoque_publico %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 186

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 187

```html
        <h2>Estoque público</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 189

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 190

```html
            Consulte os estoques informados pelos Hemocentros aprovados.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 191

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 193

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 194

```html
            <a href="{% url 'accounts:estoque_publico' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 195

```html
                Ver estoque público completo
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 196

```html
            </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 197

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 199

```html
        <table>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 200

```html
            <thead>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 201

```html
                <tr>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 202

```html
                    <th>Tipo sanguineo</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 203

```html
                    <th>Nivel</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 204

```html
                    <th>Ocupacao</th>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 205

```html
                </tr>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 206

```html
            </thead>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 208

```html
            <tbody>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 209

```html
                {% for item in estoque_geral %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 210

```html
                    <tr>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 211

```html
                        <td>{{ item.tipo }}</td>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 212

```html
                        <td>{{ item.nivel }}</td>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 213

```html
                        <td>{{ item.percentual }}%</td>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação. Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 214

```html
                    </tr>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 215

```html
                {% empty %}
```

Apresenta o caso em que a coleção do laço está vazia.

### Linha 216

```html
                    <tr>
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 217

```html
                        <td colspan="3">
```

Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.

### Linha 218

```html
                            Nenhum dado de estoque disponivel.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 219

```html
                        </td>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 220

```html
                    </tr>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 221

```html
                {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 222

```html
            </tbody>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 223

```html
        </table>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 224

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 226

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 229

```html
{% comment %}
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 230

```html
=================================================================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 231

```html
PEDIDOS
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 232

```html
=================================================================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 233

```html
Doador, Receptor, Observador e Hemocentro podem ver pedidos ativos. O
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 234

```html
Administrador nao precisa receber essa lista no painel administrativo.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 235

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 237

```html
{% if visibilidade.mostra_pedidos %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 239

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 240

```html
        <h2>Pedidos ativos</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 241

```html
        <p><a href="{% url 'accounts:consultar_pedidos' %}">Consultar pedidos ativos</a></p>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre. Agrupa conteúdo em um parágrafo.

### Linha 243

```html
        {% if visibilidade.pode_solicitar_divulgacao %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 244

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 245

```html
                <a href="{% url 'accounts:pedido_publicar' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 246

```html
                    Solicitar divulgação de necessidade
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 247

```html
                </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 248

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 249

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 250

```html
                <a href="{% url 'accounts:minhas_solicitacoes' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 251

```html
                    Acompanhar minhas solicitações
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 252

```html
                </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 253

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 254

```html
        {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 256

```html
        <ul>
```

Abre lista; ul é não numerada e ol é numerada.

### Linha 257

```html
            {% for pedido in pedidos_ativos %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 258

```html
                <li>
```

Define um item da lista.

### Linha 259

```html
                    <strong>{{ pedido.titulo }}</strong><br>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 260

```html
                    {{ pedido.tipo_sanguineo }} -
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 261

```html
                    {{ pedido.cidade }} -
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 262

```html
                    Urgencia {{ pedido.urgencia }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 263

```html
                </li>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 264

```html
            {% empty %}
```

Apresenta o caso em que a coleção do laço está vazia.

### Linha 265

```html
                <li>Nenhum pedido ativo no momento.</li>
```

Define um item da lista.

### Linha 266

```html
            {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 267

```html
        </ul>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 268

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 270

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 272

```html
{% if visibilidade.pode_analisar_pedidos %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 273

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 274

```html
        <h2>Análise de solicitações</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 275

```html
        <p>Somente o Hemocentro aprovado pode decidir pela publicação.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 276

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 277

```html
            <a href="{% url 'accounts:painel_pedidos_hemocentro' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 278

```html
                Analisar solicitações recebidas
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 279

```html
            </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 280

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 281

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 282

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 285

```html
{% comment %}
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 286

```html
=================================================================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 287

```html
POSTOS DE COLETA
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 288

```html
=================================================================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 289

```html
Doador e Observador recebem a lista de postos no dashboard. Outros perfis
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 290

```html
podem acessar informacoes publicas pela pagina inicial quando necessario.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 291

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 293

```html
{% if visibilidade.mostra_postos %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 295

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 296

```html
        <h2>Postos de coleta</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 298

```html
        <ul>
```

Abre lista; ul é não numerada e ol é numerada.

### Linha 299

```html
            {% for posto in postos %}
```

Repete a marcação para cada item da coleção recebida.

### Linha 300

```html
                <li>
```

Define um item da lista.

### Linha 301

```html
                    <strong>{{ posto.nome }}</strong><br>
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 302

```html
                    {{ posto.cidade }}/{{ posto.estado }} -
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 303

```html
                    {{ posto.horario }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 304

```html
                </li>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 305

```html
            {% empty %}
```

Apresenta o caso em que a coleção do laço está vazia.

### Linha 306

```html
                <li>Nenhum posto de coleta cadastrado.</li>
```

Define um item da lista.

### Linha 307

```html
            {% endfor %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 308

```html
        </ul>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 309

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 311

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 314

```html
{% comment %}
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 315

```html
=================================================================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 316

```html
STATUS DA VALIDACAO DO HEMOCENTRO
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 317

```html
=================================================================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 318

```html
Mostra para o Hemocentro a situacao atual do cadastro institucional.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 319

```html
Somente Hemocentro aprovado recebe o link para gerenciar estoque.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 320

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 322

```html
{% if visibilidade.mostra_status_hemocentro %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 324

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 326

```html
        <h2>Status da validação institucional</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 328

```html
        {% if request.user.status_validacao == "PENDENTE" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 330

```html
            <h3>Pendente</h3>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 332

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 333

```html
                Seu cadastro de Hemocentro está aguardando análise
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 334

```html
                de um administrador.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 335

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 337

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 338

```html
                Enquanto a análise não for concluída, a publicação
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 339

```html
                de estoques e campanhas permanece bloqueada.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 340

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 342

```html
        {% elif request.user.status_validacao == "APROVADO" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 344

```html
            <h3>Aprovado</h3>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 346

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 347

```html
                Seu Hemocentro foi aprovado pelo administrador.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 348

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 350

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 351

```html
                O Hemocentro está autorizado a cadastrar e atualizar estoques.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 352

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 354

```html
            {% if visibilidade.pode_gerenciar_estoque %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 355

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 356

```html
                    <a href="{% url 'accounts:estoque_hemocentro' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 357

```html
                        Cadastrar e atualizar estoque
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 358

```html
                    </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 359

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 360

```html
            {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 362

```html
        {% elif request.user.status_validacao == "RECUSADO" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 364

```html
            <h3>Cadastro recusado</h3>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 366

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 367

```html
                O cadastro do Hemocentro foi recusado.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 368

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 370

```html
            {% if validacao_atual and validacao_atual.parecer %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 372

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 373

```html
                    <strong>Parecer do administrador:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 374

```html
                    {{ validacao_atual.parecer }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 375

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 377

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 378

```html
                    <strong>Data da análise:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 379

```html
                    {{ validacao_atual.data_analise|date:"d/m/Y H:i" }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 380

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 382

```html
            {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 384

```html
        {% elif request.user.status_validacao == "CORRECAO" %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 386

```html
            <h3>Correção necessária</h3>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 388

```html
            <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 389

```html
                O administrador solicitou alterações no cadastro
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 390

```html
                do Hemocentro.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 391

```html
            </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 393

```html
            {% if validacao_atual and validacao_atual.parecer %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 395

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 396

```html
                    <strong>Orientação do administrador:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 397

```html
                    {{ validacao_atual.parecer }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 398

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 400

```html
                <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 401

```html
                    <strong>Data da análise:</strong>
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 402

```html
                    {{ validacao_atual.data_analise|date:"d/m/Y H:i" }}
```

Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.

### Linha 403

```html
                </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 405

```html
            {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 407

```html
        {% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 409

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 411

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 414

```html
{% comment %}
```

Inicia comentário/documentação que não é uma regra do servidor.

### Linha 415

```html
=================================================================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 416

```html
ACESSO DO ADMINISTRADOR
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 417

```html
=================================================================
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 418

```html
Mostra o link para a tela de aprovação quando o usuário é administrador.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 419

```html
Administrador nao e tratado como Hemocentro.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 420

```html
{% endcomment %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 422

```html
{% if visibilidade.pode_aprovar_hemocentros %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 423

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 424

```html
        <h2>Validação de Hemocentros</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 426

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 427

```html
            Analise cadastros pendentes e libere o acesso institucional
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 428

```html
            somente depois da aprovação.
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 429

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 431

```html
        <p>
```

Agrupa conteúdo em um parágrafo.

### Linha 432

```html
            <a href="{% url 'accounts:painel_aprovacao_hemocentros' %}">
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre.

### Linha 433

```html
                Acessar aprovação de Hemocentros
```

Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.

### Linha 434

```html
            </a>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 435

```html
        </p>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 436

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 437

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 439

```html
{% if visibilidade.pode_moderar_pedidos %}
```

Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.

### Linha 440

```html
    <section>
```

Agrupa uma seção temática da página.

### Linha 441

```html
        <h2>Moderação de pedidos</h2>
```

Marca um título; o número determina seu nível na hierarquia do documento.

### Linha 442

```html
        <p>Analise pedidos suspeitos ou pendentes sem publicar em nome do Hemocentro.</p>
```

Agrupa conteúdo em um parágrafo.

### Linha 443

```html
        <p><a href="{% url 'accounts:painel_validacao_pedidos' %}">Acessar moderação de pedidos</a></p>
```

Resolve a rota Django pelo nome indicado. Define link; href é o endereço ou âncora que o navegador abre. Agrupa conteúdo em um parágrafo.

### Linha 444

```html
    </section>
```

Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.

### Linha 445

```html
{% endif %}
```

Encerra o bloco de template correspondente, como condição, laço ou comentário.

### Linha 446

```html
{% endblock %}
```

Fecha a região de conteúdo do template. Encerra o bloco de template correspondente, como condição, laço ou comentário.

