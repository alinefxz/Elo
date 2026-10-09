# accounts/urls.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Associacao entre endereco, view e nome de rota.

**Arquivo original:** [accounts/urls.py](<C:/Users/lb119/Elo/accounts/urls.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""
RESUMO DO ARQUIVO
=================

Este arquivo associa cada endereco do app a uma view.

Exemplo: quando o navegador pede /cadastro/, o Django procura esta lista e
executa views.cadastro. Os nomes das rotas permitem gerar links sem escrever
enderecos manualmente nos templates.
"""

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from .forms import LoginUsuarioForm


app_name = "accounts"


urlpatterns = [

    # ==========================================================
    # ACESSO PUBLICO
    # ==========================================================

    path(
        "",
        views.inicio,
        name="inicio",
    ),

    # Cadastro.
    path(
        "cadastro/",
        views.cadastro,
        name="cadastro",
    ),

    # Login.
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=LoginUsuarioForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),

    # Logout.
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    # Dashboard.
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    # Validacao administrativa de Hemocentros.
    # A tela e as acoes sao protegidas pelas views para que somente um
    # Administrador consiga consultar ou alterar os cadastros pendentes.
    path(
        "hemocentros/validacao/",
        views.painel_aprovacao_hemocentros,
        name="painel_aprovacao_hemocentros",
    ),
    path(
        "hemocentros/pendentes/",
        views.hemocentros_pendentes,
        name="hemocentros_pendentes",
    ),
    path(
        "hemocentros/<int:id_hemocentro>/aprovar/",
        views.aprovar_hemocentro,
        name="aprovar_hemocentro",
    ),
    path(
        "hemocentros/<int:id_hemocentro>/recusar/",
        views.recusar_hemocentro,
        name="recusar_hemocentro",
    ),
    path(
        "hemocentros/<int:id_hemocentro>/solicitar-correcao/",
        views.solicitar_correcao_hemocentro,
        name="solicitar_correcao_hemocentro",
    ),

    # ==========================================================
    # PEDIDOS DE SANGUE
    # ==========================================================

    # Publicacao de pedidos de sangue.
    path(
        "pedidos/publicar/",
        views.criar_pedido_sangue,
        name="pedido_publicar",
    ),

    path(
        "pedidos/",
        views.consultar_pedidos,
        name="consultar_pedidos",
    ),

    path(
        "pedidos/novo/",
        views.criar_pedido_sangue,
        name="criar_pedido_sangue",
    ),

    path(
        "pedidos/minhas-solicitacoes/",
        views.minhas_solicitacoes,
        name="minhas_solicitacoes",
    ),

    path(
        "pedidos/hemocentro/",
        views.painel_pedidos_hemocentro,
        name="painel_pedidos_hemocentro",
    ),

    path(
        "pedidos/validacao/",
        views.painel_validacao_pedidos,
        name="painel_validacao_pedidos",
    ),

    path(
        "pedidos/<int:id_pedido>/aprovar/",
        views.aprovar_pedido,
        name="aprovar_pedido",
    ),

    path(
        "pedidos/<int:id_pedido>/recusar/",
        views.recusar_pedido,
        name="recusar_pedido",
    ),

    path(
        "pedidos/<int:id_pedido>/correcao/",
        views.solicitar_correcao_pedido,
        name="solicitar_correcao_pedido",
    ),

    path(
        "pedidos/<int:id_pedido>/suspeito/",
        views.marcar_pedido_suspeito,
        name="marcar_pedido_suspeito",
    ),

    # ==========================================================
    # TRIAGEM
    # ==========================================================

    # Pagina publica que explica a triagem e apresenta as modalidades.
    path(
        "triagem/",
        views.triagem_apresentacao,
        name="triagem_apresentacao",
    ),

    # Inicia ou retoma a modalidade escolhida.
    path(
        "triagem/iniciar/<str:modalidade>/",
        views.triagem_iniciar,
        name="triagem_iniciar",
    ),

    # Pergunta atual da triagem.
    path(
        "triagem/<int:id_triagem>/pergunta/",
        views.triagem_pergunta,
        name="triagem_pergunta",
    ),

    # Resultado.
    path(
        "triagem/<int:id_triagem>/resultado/",
        views.triagem_resultado,
        name="triagem_resultado",
    ),

    path(
        "triagem/<int:id_triagem>/revisao/",
        views.triagem_revisao,
        name="triagem_revisao",
    ),

    # Historico do usuario.
    path(
        "triagens/historico/",
        views.triagem_historico,
        name="triagem_historico",
    ),

    # ==========================================================
    # COMPATIBILIDADE SANGUINEA
    # ==========================================================

    path(
        "compatibilidade-sanguinea/",
        views.compatibilidade_sanguinea,
        name="compatibilidade_sanguinea",
    ),

    # ==========================================================
    # ESTOQUE
    # ==========================================================

    # Publica. Visitantes e usuarios autenticados podem acessar.
    path(
        "estoque/",
        views.visualizacao_publica_estoque,
        name="estoque_publico",
    ),

    # Privadas do Hemocentro. O acesso e protegido dentro das views.
    path(
        "estoque/hemocentro/",
        views.estoque_hemocentro,
        name="estoque_hemocentro",
    ),

    path(
        "estoque/hemocentro/cadastrar/",
        views.cadastrar_estoque_view,
        name="cadastrar_estoque",
    ),

    path(
        "estoque/hemocentro/<int:id_estoque>/atualizar/",
        views.atualizar_estoque_view,
        name="atualizar_estoque",
    ),
]
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 10

```python
"""
RESUMO DO ARQUIVO
=================

Este arquivo associa cada endereco do app a uma view.

Exemplo: quando o navegador pede /cadastro/, o Django procura esta lista e
executa views.cadastro. Os nomes das rotas permitem gerar links sem escrever
enderecos manualmente nos templates.
"""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 12 a 12

```python
from django.contrib.auth.views import LoginView, LogoutView
```

**Explicação deste trecho:**

**Linha 12 — ImportFrom** (nível 0 do bloco).

Importa de `django.contrib.auth.views` os nomes `LoginView`, `LogoutView`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 13 a 13

```python
from django.urls import path
```

**Explicação deste trecho:**

**Linha 13 — ImportFrom** (nível 0 do bloco).

Importa de `django.urls` os nomes `path`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 15 a 15

```python
from . import views
```

**Explicação deste trecho:**

**Linha 15 — ImportFrom** (nível 0 do bloco).

Importa de `.` os nomes `views`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 16 a 16

```python
from .forms import LoginUsuarioForm
```

**Explicação deste trecho:**

**Linha 16 — ImportFrom** (nível 0 do bloco).

Importa de `.forms` os nomes `LoginUsuarioForm`. Pontos iniciais indicam importação relativa ao pacote.

### Assign — linhas 19 a 19

```python
app_name = "accounts"
```

**Explicação deste trecho:**

**Linha 19 — Assign** (nível 0 do bloco).

Associa `app_name` a o valor literal `'accounts'`.

### Assign — linhas 22 a 244

```python
urlpatterns = [

    # ==========================================================
    # ACESSO PUBLICO
    # ==========================================================

    path(
        "",
        views.inicio,
        name="inicio",
    ),

    # Cadastro.
    path(
        "cadastro/",
        views.cadastro,
        name="cadastro",
    ),

    # Login.
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=LoginUsuarioForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),

    # Logout.
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    # Dashboard.
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    # Validacao administrativa de Hemocentros.
    # A tela e as acoes sao protegidas pelas views para que somente um
    # Administrador consiga consultar ou alterar os cadastros pendentes.
    path(
        "hemocentros/validacao/",
        views.painel_aprovacao_hemocentros,
        name="painel_aprovacao_hemocentros",
    ),
    path(
        "hemocentros/pendentes/",
        views.hemocentros_pendentes,
        name="hemocentros_pendentes",
    ),
    path(
        "hemocentros/<int:id_hemocentro>/aprovar/",
        views.aprovar_hemocentro,
        name="aprovar_hemocentro",
    ),
    path(
        "hemocentros/<int:id_hemocentro>/recusar/",
        views.recusar_hemocentro,
        name="recusar_hemocentro",
    ),
    path(
        "hemocentros/<int:id_hemocentro>/solicitar-correcao/",
        views.solicitar_correcao_hemocentro,
        name="solicitar_correcao_hemocentro",
    ),

    # ==========================================================
    # PEDIDOS DE SANGUE
    # ==========================================================

    # Publicacao de pedidos de sangue.
    path(
        "pedidos/publicar/",
        views.criar_pedido_sangue,
        name="pedido_publicar",
    ),

    path(
        "pedidos/",
        views.consultar_pedidos,
        name="consultar_pedidos",
    ),

    path(
        "pedidos/novo/",
        views.criar_pedido_sangue,
        name="criar_pedido_sangue",
    ),

    path(
        "pedidos/minhas-solicitacoes/",
        views.minhas_solicitacoes,
        name="minhas_solicitacoes",
    ),

    path(
        "pedidos/hemocentro/",
        views.painel_pedidos_hemocentro,
        name="painel_pedidos_hemocentro",
    ),

    path(
        "pedidos/validacao/",
        views.painel_validacao_pedidos,
        name="painel_validacao_pedidos",
    ),

    path(
        "pedidos/<int:id_pedido>/aprovar/",
        views.aprovar_pedido,
        name="aprovar_pedido",
    ),

    path(
        "pedidos/<int:id_pedido>/recusar/",
        views.recusar_pedido,
        name="recusar_pedido",
    ),

    path(
        "pedidos/<int:id_pedido>/correcao/",
        views.solicitar_correcao_pedido,
        name="solicitar_correcao_pedido",
    ),

    path(
        "pedidos/<int:id_pedido>/suspeito/",
        views.marcar_pedido_suspeito,
        name="marcar_pedido_suspeito",
    ),

    # ==========================================================
    # TRIAGEM
    # ==========================================================

    # Pagina publica que explica a triagem e apresenta as modalidades.
    path(
        "triagem/",
        views.triagem_apresentacao,
        name="triagem_apresentacao",
    ),

    # Inicia ou retoma a modalidade escolhida.
    path(
        "triagem/iniciar/<str:modalidade>/",
        views.triagem_iniciar,
        name="triagem_iniciar",
    ),

    # Pergunta atual da triagem.
    path(
        "triagem/<int:id_triagem>/pergunta/",
        views.triagem_pergunta,
        name="triagem_pergunta",
    ),

    # Resultado.
    path(
        "triagem/<int:id_triagem>/resultado/",
        views.triagem_resultado,
        name="triagem_resultado",
    ),

    path(
        "triagem/<int:id_triagem>/revisao/",
        views.triagem_revisao,
        name="triagem_revisao",
    ),

    # Historico do usuario.
    path(
        "triagens/historico/",
        views.triagem_historico,
        name="triagem_historico",
    ),

    # ==========================================================
    # COMPATIBILIDADE SANGUINEA
    # ==========================================================

    path(
        "compatibilidade-sanguinea/",
        views.compatibilidade_sanguinea,
        name="compatibilidade_sanguinea",
    ),

    # ==========================================================
    # ESTOQUE
    # ==========================================================

    # Publica. Visitantes e usuarios autenticados podem acessar.
    path(
        "estoque/",
        views.visualizacao_publica_estoque,
        name="estoque_publico",
    ),

    # Privadas do Hemocentro. O acesso e protegido dentro das views.
    path(
        "estoque/hemocentro/",
        views.estoque_hemocentro,
        name="estoque_hemocentro",
    ),

    path(
        "estoque/hemocentro/cadastrar/",
        views.cadastrar_estoque_view,
        name="cadastrar_estoque",
    ),

    path(
        "estoque/hemocentro/<int:id_estoque>/atualizar/",
        views.atualizar_estoque_view,
        name="atualizar_estoque",
    ),
]
```

**Explicação deste trecho:**

**Linha 22 — Assign** (nível 0 do bloco).

Associa `urlpatterns` a uma coleção List com 31 itens, na expressão `[path('', views.inicio, name='inicio'), path('cadastro/', views.cadastro, name='cadastro'), path('login/', LoginView.as_view(template_name='accounts/login.html', authentication_form=LoginUsuarioForm, redirect_authenticated_user=True), name='login'), path('logout/', LogoutView.as_view(), name='logout'), path('dashboard/', views.dashboard, name='dashboard'), path('hemocentros/validacao/', views.painel_aprovacao_hemocentros, name='painel_aprovacao_hemocentros'), path('hemocentros/pendentes/', views.hemocentros_pendentes, name='hemocentros_pendentes'), path('hemocentros/<int:id_hemocentro>/aprovar/', views.aprovar_hemocentro, name='aprovar_hemocentro'), path('hemocentros/<int:id_hemocentro>/recusar/', views.recusar_hemocentro, name='recusar_hemocentro'), path('hemocentros/<int:id_hemocentro>/solicitar-correcao/', views.solicitar_correcao_hemocentro, name='solicitar_correcao_hemocentro'), path('pedidos/publicar/', views.criar_pedido_sangue, name='pedido_publicar'), path('pedidos/', views.consultar_pedidos, name='consultar_pedidos'), path('pedidos/novo/', views.criar_pedido_sangue, name='criar_pedido_sangue'), path('pedidos/minhas-solicitacoes/', views.minhas_solicitacoes, name='minhas_solicitacoes'), path('pedidos/hemocentro/', views.painel_pedidos_hemocentro, name='painel_pedidos_hemocentro'), path('pedidos/validacao/', views.painel_validacao_pedidos, name='painel_validacao_pedidos'), path('pedidos/<int:id_pedido>/aprovar/', views.aprovar_pedido, name='aprovar_pedido'), path('pedidos/<int:id_pedido>/recusar/', views.recusar_pedido, name='recusar_pedido'), path('pedidos/<int:id_pedido>/correcao/', views.solicitar_correcao_pedido, name='solicitar_correcao_pedido'), path('pedidos/<int:id_pedido>/suspeito/', views.marcar_pedido_suspeito, name='marcar_pedido_suspeito'), path('triagem/', views.triagem_apresentacao, name='triagem_apresentacao'), path('triagem/iniciar/<str:modalidade>/', views.triagem_iniciar, name='triagem_iniciar'), path('triagem/<int:id_triagem>/pergunta/', views.triagem_pergunta, name='triagem_pergunta'), path('triagem/<int:id_triagem>/resultado/', views.triagem_resultado, name='triagem_resultado'), path('triagem/<int:id_triagem>/revisao/', views.triagem_revisao, name='triagem_revisao'), path('triagens/historico/', views.triagem_historico, name='triagem_historico'), path('compatibilidade-sanguinea/', views.compatibilidade_sanguinea, name='compatibilidade_sanguinea'), path('estoque/', views.visualizacao_publica_estoque, name='estoque_publico'), path('estoque/hemocentro/', views.estoque_hemocentro, name='estoque_hemocentro'), path('estoque/hemocentro/cadastrar/', views.cadastrar_estoque_view, name='cadastrar_estoque'), path('estoque/hemocentro/<int:id_estoque>/atualizar/', views.atualizar_estoque_view, name='atualizar_estoque')]`.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 24: `# ==========================================================`
- Linha 25: `# ACESSO PUBLICO`
- Linha 26: `# ==========================================================`
- Linha 34: `# Cadastro.`
- Linha 41: `# Login.`
- Linha 52: `# Logout.`
- Linha 59: `# Dashboard.`
- Linha 66: `# Validacao administrativa de Hemocentros.`
- Linha 67: `# A tela e as acoes sao protegidas pelas views para que somente um`
- Linha 68: `# Administrador consiga consultar ou alterar os cadastros pendentes.`
- Linha 95: `# ==========================================================`
- Linha 96: `# PEDIDOS DE SANGUE`
- Linha 97: `# ==========================================================`
- Linha 99: `# Publicacao de pedidos de sangue.`
- Linha 160: `# ==========================================================`
- Linha 161: `# TRIAGEM`
- Linha 162: `# ==========================================================`
- Linha 164: `# Pagina publica que explica a triagem e apresenta as modalidades.`
- Linha 171: `# Inicia ou retoma a modalidade escolhida.`
- Linha 178: `# Pergunta atual da triagem.`
- Linha 185: `# Resultado.`
- Linha 198: `# Historico do usuario.`
- Linha 205: `# ==========================================================`
- Linha 206: `# COMPATIBILIDADE SANGUINEA`
- Linha 207: `# ==========================================================`
- Linha 215: `# ==========================================================`
- Linha 216: `# ESTOQUE`
- Linha 217: `# ==========================================================`
- Linha 219: `# Publica. Visitantes e usuarios autenticados podem acessar.`
- Linha 226: `# Privadas do Hemocentro. O acesso e protegido dentro das views.`

