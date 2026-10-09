# Referencia integral do codigo do Elo

Complemento de [GUIA_ELO.md](GUIA_ELO.md). Extracao estrutural dos arquivos locais em 09/10/2026.

Cada chamada listada existe no corpo; isso nao significa que todos os ramos executem juntos. Chamadores sao candidatos por nome, nao um resolvedor completo de tipos: metodos com nomes iguais podem pertencer a classes diferentes. Docstrings sao do proprio codigo e podem estar antigas.

Nao inclui .env real, banco, ambiente virtual, arquivos binarios ou codigo das dependencias. Arquivos de suporte vazios tambem estao no inventario. A copia completa esta em [CODIGO_COMPLETO.md](CODIGO_COMPLETO.md).

## Inventario de arquivos

| Arquivo | Linhas | Papel |
| --- | ---: | --- |
| [.env.example](<C:/Users/lb119/Elo/.env.example>) | 11 | Documento/configuracao complementar; consulte o conteudo integral. |
| [.gitignore](<C:/Users/lb119/Elo/.gitignore>) | 12 | Documento/configuracao complementar; consulte o conteudo integral. |
| [README.md](<C:/Users/lb119/Elo/README.md>) | 420 | Documento/configuracao complementar; consulte o conteudo integral. |
| [TESTAR_PERFIS.md](<C:/Users/lb119/Elo/TESTAR_PERFIS.md>) | 48 | Documento/configuracao complementar; consulte o conteudo integral. |
| [accounts/__init__.py](<C:/Users/lb119/Elo/accounts/__init__.py>) | 6 | Marcador de pacote Python; pode nao executar nenhuma instrucao. |
| [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py>) | 949 | Telas do Django admin, autorizacoes e auditoria de operacoes. |
| [accounts/apps.py](<C:/Users/lb119/Elo/accounts/apps.py>) | 26 | Inicializacao do app e conexao dos sinais. |
| [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py>) | 203 | Registro de eventos e observacao de acessos sensiveis. |
| [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py>) | 147 | Tabela, normalizacao, elegibilidade, frequencia e preferencia de convocacao. |
| [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py>) | 402 | Cadastro, movimentacao, estado publico e alertas de estoque. |
| [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py>) | 794 | Campos e validacoes de cadastro, login, estoque, pedidos e filtros. |
| [accounts/management/__init__.py](<C:/Users/lb119/Elo/accounts/management/__init__.py>) | 1 | Marcador de pacote Python; pode nao executar nenhuma instrucao. |
| [accounts/management/commands/__init__.py](<C:/Users/lb119/Elo/accounts/management/commands/__init__.py>) | 1 | Marcador de pacote Python; pode nao executar nenhuma instrucao. |
| [accounts/management/commands/criar_perfis_teste.py](<C:/Users/lb119/Elo/accounts/management/commands/criar_perfis_teste.py>) | 64 | Comando local de contas ficticias preservando registros existentes. |
| [accounts/migrations/0001_initial.py](<C:/Users/lb119/Elo/accounts/migrations/0001_initial.py>) | 73 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0002_remove_usuario_cidade_remove_usuario_cnpj_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0002_remove_usuario_cidade_remove_usuario_cnpj_and_more.py>) | 50 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more.py>) | 58 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0004_auditoriaacaocritica.py](<C:/Users/lb119/Elo/accounts/migrations/0004_auditoriaacaocritica.py>) | 38 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0005_usuario_status_validacao_validacaohemocentro.py](<C:/Users/lb119/Elo/accounts/migrations/0005_usuario_status_validacao_validacaohemocentro.py>) | 38 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0006_triagem_respostatriagem_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0006_triagem_respostatriagem_and_more.py>) | 65 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0007_alter_auditoriaacaocritica_acao_estoque_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0007_alter_auditoriaacaocritica_acao_estoque_and_more.py>) | 79 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py>) | 110 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0008_merge_triagem_estoque_branches.py](<C:/Users/lb119/Elo/accounts/migrations/0008_merge_triagem_estoque_branches.py>) | 19 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0009_usuario_tipo_sanguineo_notificacao.py](<C:/Users/lb119/Elo/accounts/migrations/0009_usuario_tipo_sanguineo_notificacao.py>) | 42 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0010_pedidosangue.py](<C:/Users/lb119/Elo/accounts/migrations/0010_pedidosangue.py>) | 122 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0011_alinhar_pedidos_validacao.py](<C:/Users/lb119/Elo/accounts/migrations/0011_alinhar_pedidos_validacao.py>) | 211 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0012_pedidosangue_contato_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0012_pedidosangue_contato_and_more.py>) | 85 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0013_usuario_suspensa.py](<C:/Users/lb119/Elo/accounts/migrations/0013_usuario_suspensa.py>) | 18 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0014_notificacao_pedido_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0014_notificacao_pedido_and_more.py>) | 29 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/0015_pedido_contato_email.py](<C:/Users/lb119/Elo/accounts/migrations/0015_pedido_contato_email.py>) | 18 | Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo. |
| [accounts/migrations/README.md](<C:/Users/lb119/Elo/accounts/migrations/README.md>) | 68 | Documento/configuracao complementar; consulte o conteudo integral. |
| [accounts/migrations/__init__.py](<C:/Users/lb119/Elo/accounts/migrations/__init__.py>) | 6 | Marcador de pacote Python; pode nao executar nenhuma instrucao. |
| [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py>) | 1171 | Entidades persistidas, relacionamentos, estados e integridade do banco. |
| [accounts/pedidos.py](<C:/Users/lb119/Elo/accounts/pedidos.py>) | 80 | Publicacao institucional e alertas de pedidos compativeis. |
| [accounts/signals.py](<C:/Users/lb119/Elo/accounts/signals.py>) | 65 | Registro automatico das falhas de autenticacao. |
| [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py>) | 372 | Cenarios automatizados: preparacao, acao e resultado esperado nos asserts. |
| [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py>) | 594 | Cenarios automatizados: preparacao, acao e resultado esperado nos asserts. |
| [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py>) | 286 | Cenarios automatizados: preparacao, acao e resultado esperado nos asserts. |
| [accounts/test_perfis_teste.py](<C:/Users/lb119/Elo/accounts/test_perfis_teste.py>) | 36 | Cenarios automatizados: preparacao, acao e resultado esperado nos asserts. |
| [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py>) | 208 | Cenarios automatizados: preparacao, acao e resultado esperado nos asserts. |
| [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py>) | 80 | Cenarios automatizados: preparacao, acao e resultado esperado nos asserts. |
| [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py>) | 118 | Cenarios automatizados: preparacao, acao e resultado esperado nos asserts. |
| [accounts/test_triagem_models.py](<C:/Users/lb119/Elo/accounts/test_triagem_models.py>) | 76 | Cenarios automatizados: preparacao, acao e resultado esperado nos asserts. |
| [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py>) | 249 | Cenarios automatizados: preparacao, acao e resultado esperado nos asserts. |
| [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py>) | 448 | Cenarios automatizados: preparacao, acao e resultado esperado nos asserts. |
| [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py>) | 396 | Cenarios automatizados: preparacao, acao e resultado esperado nos asserts. |
| [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py>) | 192 | Cenarios automatizados: preparacao, acao e resultado esperado nos asserts. |
| [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py>) | 424 | Cenarios automatizados: preparacao, acao e resultado esperado nos asserts. |
| [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py>) | 468 | Calculos iniciais da triagem; compare seus chamadores ao motor atual. |
| [accounts/triagem_catalogo.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo.py>) | 69 | Acesso e validacao dos catalogos versionados. |
| [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py>) | 1278 | Declaracoes de todas as perguntas e regras da extensa. |
| [accounts/triagem_catalogo_simplificada.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_simplificada.py>) | 211 | Declaracoes das perguntas rapidas e abertura de detalhes. |
| [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py>) | 177 | Formulario dinamico correspondente a cada pergunta. |
| [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py>) | 466 | Calculo da orientacao a partir das respostas e regras dos catalogos. |
| [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py>) | 572 | Andamento, respostas, revisao, persistencia e conclusao de triagem. |
| [accounts/urls.py](<C:/Users/lb119/Elo/accounts/urls.py>) | 244 | Associacao entre endereco, view e nome de rota. |
| [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py>) | 152 | Estados institucionais, decisao e historico de hemocentros. |
| [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py>) | 392 | Solicitacao, decisao, historico e autorizacao de pedidos. |
| [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py>) | 1886 | Entrada HTTP: permissoes, formularios, chamadas de servico e respostas/telas. |
| [config/__init__.py](<C:/Users/lb119/Elo/config/__init__.py>) | 6 | Marcador de pacote Python; pode nao executar nenhuma instrucao. |
| [config/asgi.py](<C:/Users/lb119/Elo/config/asgi.py>) | 20 | Entrada de servidor pelo protocolo ASGI. |
| [config/settings.py](<C:/Users/lb119/Elo/config/settings.py>) | 210 | Configuracao de apps, banco, middleware, templates e autenticacao. |
| [config/settings_test.py](<C:/Users/lb119/Elo/config/settings_test.py>) | 16 | Configuracao de banco temporario para os testes. |
| [config/urls.py](<C:/Users/lb119/Elo/config/urls.py>) | 19 | Associacao entre endereco, view e nome de rota. |
| [config/wsgi.py](<C:/Users/lb119/Elo/config/wsgi.py>) | 19 | Entrada de servidor pelo protocolo WSGI. |
| [docs/superpowers/plans/2026-09-04-triagem-completa.md](<C:/Users/lb119/Elo/docs/superpowers/plans/2026-09-04-triagem-completa.md>) | 807 | Documento/configuracao complementar; consulte o conteudo integral. |
| [docs/superpowers/specs/2026-09-04-triagem-completa-design.md](<C:/Users/lb119/Elo/docs/superpowers/specs/2026-09-04-triagem-completa-design.md>) | 283 | Documento/configuracao complementar; consulte o conteudo integral. |
| [elo_front/README-INSTALACAO.txt](<C:/Users/lb119/Elo/elo_front/README-INSTALACAO.txt>) | 23 | Documento/configuracao complementar; consulte o conteudo integral. |
| [elo_front/static/css/elo.css](<C:/Users/lb119/Elo/elo_front/static/css/elo.css>) | 649 | Regras visuais de seletores, componentes e tamanhos de tela. |
| [elo_front/templates/accounts/inicio.html](<C:/Users/lb119/Elo/elo_front/templates/accounts/inicio.html>) | 120 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [elo_front/templates/base.html](<C:/Users/lb119/Elo/elo_front/templates/base.html>) | 80 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [manage.py](<C:/Users/lb119/Elo/manage.py>) | 37 | Entrada dos comandos do Django. |
| [requirements.txt](<C:/Users/lb119/Elo/requirements.txt>) | 24 | Documento/configuracao complementar; consulte o conteudo integral. |
| [templates/accounts/cadastro.html](<C:/Users/lb119/Elo/templates/accounts/cadastro.html>) | 143 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/compatibilidade_sanguinea.html](<C:/Users/lb119/Elo/templates/accounts/compatibilidade_sanguinea.html>) | 79 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/dashboard.html](<C:/Users/lb119/Elo/templates/accounts/dashboard.html>) | 446 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/estoque_hemocentro.html](<C:/Users/lb119/Elo/templates/accounts/estoque_hemocentro.html>) | 213 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/estoque_publico.html](<C:/Users/lb119/Elo/templates/accounts/estoque_publico.html>) | 146 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/inicio.html](<C:/Users/lb119/Elo/templates/accounts/inicio.html>) | 102 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/login.html](<C:/Users/lb119/Elo/templates/accounts/login.html>) | 37 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/minhas_solicitacoes.html](<C:/Users/lb119/Elo/templates/accounts/minhas_solicitacoes.html>) | 49 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/painel_aprovacao_hemocentros.html](<C:/Users/lb119/Elo/templates/accounts/painel_aprovacao_hemocentros.html>) | 165 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/painel_moderacao_pedidos.html](<C:/Users/lb119/Elo/templates/accounts/painel_moderacao_pedidos.html>) | 68 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/painel_validacao_pedidos.html](<C:/Users/lb119/Elo/templates/accounts/painel_validacao_pedidos.html>) | 74 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/pedido_detalhe.html](<C:/Users/lb119/Elo/templates/accounts/pedido_detalhe.html>) | 44 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/pedido_filtrar.html](<C:/Users/lb119/Elo/templates/accounts/pedido_filtrar.html>) | 128 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/pedido_publicar.html](<C:/Users/lb119/Elo/templates/accounts/pedido_publicar.html>) | 21 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/pedidos_listar.html](<C:/Users/lb119/Elo/templates/accounts/pedidos_listar.html>) | 101 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/triagem_apresentacao.html](<C:/Users/lb119/Elo/templates/accounts/triagem_apresentacao.html>) | 116 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/triagem_extensa.html](<C:/Users/lb119/Elo/templates/accounts/triagem_extensa.html>) | 39 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/triagem_historico.html](<C:/Users/lb119/Elo/templates/accounts/triagem_historico.html>) | 37 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/triagem_inicio.html](<C:/Users/lb119/Elo/templates/accounts/triagem_inicio.html>) | 0 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/triagem_pergunta.html](<C:/Users/lb119/Elo/templates/accounts/triagem_pergunta.html>) | 39 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/triagem_resultado.html](<C:/Users/lb119/Elo/templates/accounts/triagem_resultado.html>) | 55 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/accounts/triagem_revisao.html](<C:/Users/lb119/Elo/templates/accounts/triagem_revisao.html>) | 29 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |
| [templates/base.html](<C:/Users/lb119/Elo/templates/base.html>) | 129 | Template de apresentacao; compare variaveis recebidas e view que o renderiza. |

## .env.example

Documento/configuracao complementar; consulte o conteudo integral.

Original: [.env.example](<C:/Users/lb119/Elo/.env.example>).


## .gitignore

Documento/configuracao complementar; consulte o conteudo integral.

Original: [.gitignore](<C:/Users/lb119/Elo/.gitignore>).


## README.md

Documento/configuracao complementar; consulte o conteudo integral.

Original: [README.md](<C:/Users/lb119/Elo/README.md>).


## TESTAR_PERFIS.md

Documento/configuracao complementar; consulte o conteudo integral.

Original: [TESTAR_PERFIS.md](<C:/Users/lb119/Elo/TESTAR_PERFIS.md>).


## accounts/__init__.py

Marcador de pacote Python; pode nao executar nenhuma instrucao.

Original: [accounts/__init__.py](<C:/Users/lb119/Elo/accounts/__init__.py>).


## accounts/admin.py

Telas do Django admin, autorizacoes e auditoria de operacoes.

Original: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py>).

**Dependencias importadas:**

```python
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .auditoria import campos_sensiveis_alterados, registrar_auditoria
from .models import Usuario, ValidacaoHemocentro, ConsentimentoLGPD, AuditoriaAcaoCritica, Triagem, RespostaTriagem, Estoque, EstoqueMovimentacao, Notificacao, PedidoSangue, ValidacaoPedido
from .validacao_hemocentro import aprovar_hemocentro, recusar_hemocentro, solicitar_correcao_hemocentro
```

### UsuarioAdminCreationForm

Linha 38: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:38>).

Classe; herda de: UserCreationForm.

**Explicacao presente no codigo:**

> Formulario usado quando o admin cria uma conta.

### UsuarioAdminCreationForm.Meta

Linha 41: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:41>).

Classe; herda de: nenhuma classe declarada.

**Atributos/campos declarados diretamente:**

```python
model = Usuario
fields = ('email', 'nome', 'perfil')
```

### UsuarioAdminChangeForm

Linha 49: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:49>).

Classe; herda de: UserChangeForm.

**Explicacao presente no codigo:**

> Formulario usado quando o admin edita uma conta existente.

### UsuarioAdminChangeForm.Meta

Linha 52: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:52>).

Classe; herda de: nenhuma classe declarada.

**Atributos/campos declarados diretamente:**

```python
model = Usuario
fields = '__all__'
```

### UsuarioAdmin

Linha 58: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:58>).

Classe; herda de: UserAdmin.

**Explicacao presente no codigo:**

> Define listagem, busca e organizacao dos campos de Usuario.

**Decoradores:** `admin.register(Usuario)`.

**Atributos/campos declarados diretamente:**

```python
add_form = UsuarioAdminCreationForm
form = UsuarioAdminChangeForm
model = Usuario
list_display = ('email', 'nome', 'perfil', 'tipo_sanguineo', 'status_validacao', 'is_active', 'suspensa', 'email_verificado', 'is_staff')
list_filter = ('perfil', 'tipo_sanguineo', 'status_validacao', 'is_active', 'suspensa', 'email_verificado', 'is_staff')
search_fields = ('email', 'nome', 'cpf', 'cnpj')
ordering = ('nome',)
actions = ('aprovar_hemocentros_selecionados', 'recusar_hemocentros_selecionados', 'solicitar_correcao_hemocentros_selecionados')
readonly_fields = ('status_validacao', 'last_login', 'date_joined', 'atualizado_em')
fieldsets = ((None, {'fields': ('email', 'password')}), ('Dados da conta', {'fields': ('nome', 'perfil', 'cpf', 'cnpj', 'telefone', 'data_nascimento', 'sexo', 'tipo_sanguineo', 'tipo_sanguineo_confirmado', 'cidade', 'estado', 'status_validacao', 'email_verificado')}), ('Permissoes internas do Django', {'fields': ('is_active', 'suspensa', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), ('Datas', {'fields': ('last_login', 'date_joined', 'atualizado_em')}))
add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'nome', 'perfil', 'password1', 'password2', 'is_active', 'suspensa', 'is_staff')}),)
```

### UsuarioAdmin.save_model

Linha 184: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:184>).

```python
def save_model(self, request, obj, form, change):
```

**Explicacao presente no codigo:**

> Audita mudancas administrativas em perfil e permissoes.

**Chamadas utilizadas no corpo:** `alteracoes.items`, `campos_sensiveis_alterados`, `registrar_auditoria`, `sorted`, `super`, `super().save_model`.

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `ConsentimentoLGPDAdmin.save_model` em [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:456>).
- `AuditoriaTests.test_suspensao_registrada_sem_duplicar_dados_pessoais` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:387>).

### UsuarioAdmin._executar_acao_validacao

Linha 239: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:239>).

```python
def _executar_acao_validacao(self, request, queryset, funcao, parecer):
```

**Explicacao presente no codigo:**

> Aplica uma decisao de validacao aos Hemocentros selecionados.

**Chamadas utilizadas no corpo:** `funcao`, `queryset.exclude`, `queryset.exclude(perfil=Usuario.Perfil.HEMOCENTRO).count`, `queryset.filter`, `self.message_user`.

**Estrutura de controle:** For: 1, If: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `UsuarioAdmin.aprovar_hemocentros_selecionados` em [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:282>).
- `UsuarioAdmin.recusar_hemocentros_selecionados` em [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:293>).
- `UsuarioAdmin.solicitar_correcao_hemocentros_selecionados` em [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:306>).

### UsuarioAdmin.aprovar_hemocentros_selecionados

Linha 282: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:282>).

```python
def aprovar_hemocentros_selecionados(self, request, queryset):
```

**Explicacao presente no codigo:**

> Acao em lote que aprova Hemocentros e registra historico.

**Decoradores:** `admin.action(description='Aprovar Hemocentros selecionados')`.

**Chamadas utilizadas no corpo:** `self._executar_acao_validacao`.

### UsuarioAdmin.recusar_hemocentros_selecionados

Linha 293: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:293>).

```python
def recusar_hemocentros_selecionados(self, request, queryset):
```

**Explicacao presente no codigo:**

> Acao em lote que recusa Hemocentros e registra historico.

**Decoradores:** `admin.action(description='Recusar Hemocentros selecionados')`.

**Chamadas utilizadas no corpo:** `self._executar_acao_validacao`.

### UsuarioAdmin.solicitar_correcao_hemocentros_selecionados

Linha 306: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:306>).

```python
def solicitar_correcao_hemocentros_selecionados(self, request, queryset):
```

**Explicacao presente no codigo:**

> Acao em lote que solicita correcao cadastral e registra historico.

**Decoradores:** `admin.action(description='Solicitar correcao dos Hemocentros selecionados')`.

**Chamadas utilizadas no corpo:** `self._executar_acao_validacao`.

### UsuarioAdmin.save_related

Linha 320: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:320>).

```python
def save_related(self, request, form, formsets, change):
```

**Explicacao presente no codigo:**

> Audita mudancas em grupos e permissoes diretas do usuario.

**Chamadas utilizadas no corpo:** `Usuario.objects.get`, `obj.groups.values_list`, `obj.user_permissions.values_list`, `registrar_auditoria`, `set`, `sorted`, `super`, `super().save_related`, `usuario_atual.groups.values_list`, `usuario_atual.user_permissions.values_list`.

**Expressoes de retorno (dependem do caminho):**

- `None`

**Estrutura de controle:** If: 5. Abra o original para seguir as condicoes na ordem.

### ValidacaoHemocentroAdmin

Linha 395: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:395>).

Classe; herda de: admin.ModelAdmin.

**Explicacao presente no codigo:**

> Consulta somente leitura do historico institucional de Hemocentros.

**Decoradores:** `admin.register(ValidacaoHemocentro)`.

**Atributos/campos declarados diretamente:**

```python
list_display = ('data_analise', 'hemocentro', 'status', 'admin', 'parecer_resumido')
list_filter = ('status', 'data_analise')
search_fields = ('hemocentro__email', 'hemocentro__nome', 'hemocentro__cnpj', 'admin__email', 'admin__nome', 'parecer')
readonly_fields = ('id_validacao', 'hemocentro', 'admin', 'status', 'parecer', 'data_analise')
date_hierarchy = 'data_analise'
ordering = ('-data_analise',)
parecer_resumido.short_description = 'Parecer'
```

### ValidacaoHemocentroAdmin.parecer_resumido

Linha 432: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:432>).

```python
def parecer_resumido(self, obj):
```

**Explicacao presente no codigo:**

> Mostra um trecho curto do parecer na listagem.

**Chamadas utilizadas no corpo:** `len`.

**Expressoes de retorno (dependem do caminho):**

- `f'{obj.parecer[:77]}...'`
- `obj.parecer`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

### ValidacaoHemocentroAdmin.has_add_permission

Linha 442: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:442>).

```python
def has_add_permission(self, request):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### ValidacaoHemocentroAdmin.has_change_permission

Linha 445: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:445>).

```python
def has_change_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### ValidacaoHemocentroAdmin.has_delete_permission

Linha 448: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:448>).

```python
def has_delete_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### ConsentimentoLGPDAdmin

Linha 453: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:453>).

Classe; herda de: admin.ModelAdmin.

**Explicacao presente no codigo:**

> Permite consultar os aceites LGPD no painel administrativo.

**Decoradores:** `admin.register(ConsentimentoLGPD)`.

**Atributos/campos declarados diretamente:**

```python
list_display = ('usuario', 'tipo_termo', 'versao_termo', 'aceito', 'data_aceite')
list_filter = ('tipo_termo', 'aceito', 'versao_termo')
search_fields = ('usuario__email', 'usuario__nome')
readonly_fields = ('data_aceite',)
```

### ConsentimentoLGPDAdmin.save_model

Linha 456: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:456>).

```python
def save_model(self, request, obj, form, change):
```

**Chamadas utilizadas no corpo:** `list`, `registrar_auditoria`, `super`, `super().save_model`.

**Onde aparece uma chamada com este nome:**

- `UsuarioAdmin.save_model` em [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:184>).
- `AuditoriaTests.test_suspensao_registrada_sem_duplicar_dados_pessoais` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:387>).

### AuditoriaAcaoCriticaAdmin

Linha 493: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:493>).

Classe; herda de: admin.ModelAdmin.

**Explicacao presente no codigo:**

> Consulta somente leitura das acoes criticas registradas.

**Decoradores:** `admin.register(AuditoriaAcaoCritica)`.

**Atributos/campos declarados diretamente:**

```python
list_display = ('criado_em', 'acao', 'resultado', 'usuario', 'alvo_tipo', 'alvo_id', 'ip')
list_filter = ('acao', 'resultado', 'criado_em')
search_fields = ('usuario__email', 'usuario__nome', 'descricao', 'metadados', 'alvo_tipo', 'alvo_id', 'ip')
readonly_fields = ('id_auditoria', 'usuario', 'acao', 'resultado', 'alvo_tipo', 'alvo_id', 'descricao', 'ip', 'user_agent', 'metadados', 'criado_em')
date_hierarchy = 'criado_em'
ordering = ('-criado_em',)
```

### AuditoriaAcaoCriticaAdmin.has_view_permission

Linha 496: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:496>).

```python
def has_view_permission(self, request, obj=None):
```

**Chamadas utilizadas no corpo:** `super`, `super().has_view_permission`.

**Expressoes de retorno (dependem do caminho):**

- `request.user.perfil == Usuario.Perfil.ADMINISTRADOR and super().has_view_permission(request, obj)`

**Onde aparece uma chamada com este nome:**

- `AuditoriaAcaoCriticaAdmin.has_module_permission` em [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:502>).
- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### AuditoriaAcaoCriticaAdmin.has_module_permission

Linha 502: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:502>).

```python
def has_module_permission(self, request):
```

**Chamadas utilizadas no corpo:** `self.has_view_permission`.

**Expressoes de retorno (dependem do caminho):**

- `self.has_view_permission(request)`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### AuditoriaAcaoCriticaAdmin.has_add_permission

Linha 548: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:548>).

```python
def has_add_permission(self, request):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### AuditoriaAcaoCriticaAdmin.has_change_permission

Linha 551: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:551>).

```python
def has_change_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### AuditoriaAcaoCriticaAdmin.has_delete_permission

Linha 554: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:554>).

```python
def has_delete_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### EstoqueAdmin

Linha 559: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:559>).

Classe; herda de: admin.ModelAdmin.

**Explicacao presente no codigo:**

> Consulta administrativa do estoque de cada Hemocentro.
> 
> status_calculado e data_atualizacao ficam somente leitura porque sao
> derivados automaticamente pela camada de servico (accounts/estoque.py)
> sempre que a quantidade de bolsas muda.

**Decoradores:** `admin.register(Estoque)`.

**Atributos/campos declarados diretamente:**

```python
list_display = ('hemocentro', 'tipo_sanguineo', 'quantidade_bolsas', 'nivel_minimo', 'nivel_critico', 'status_calculado', 'data_atualizacao')
list_filter = ('status_calculado', 'tipo_sanguineo')
search_fields = ('hemocentro__email', 'hemocentro__nome')
ordering = ('hemocentro__nome', 'tipo_sanguineo')
readonly_fields = ('status_calculado', 'data_atualizacao')
```

### EstoqueMovimentacaoAdmin

Linha 600: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:600>).

Classe; herda de: admin.ModelAdmin.

**Explicacao presente no codigo:**

> Historico somente leitura das movimentacoes de estoque (UC_30).
> 
> Assim como ValidacaoHemocentroAdmin, este historico nunca deve ser
> criado, editado ou apagado pelo admin: toda movimentacao precisa
> passar por registrar_movimentacao_estoque para manter a quantidade
> de bolsas e a auditoria consistentes.

**Decoradores:** `admin.register(EstoqueMovimentacao)`.

**Atributos/campos declarados diretamente:**

```python
list_display = ('data_hora', 'estoque', 'tipo_movimento', 'quantidade_anterior', 'quantidade_movimentada', 'quantidade_nova', 'usuario_resp')
list_filter = ('tipo_movimento', 'data_hora')
search_fields = ('estoque__hemocentro__email', 'estoque__hemocentro__nome', 'usuario_resp__email', 'usuario_resp__nome', 'motivo')
readonly_fields = ('id_mov', 'estoque', 'usuario_resp', 'tipo_movimento', 'quantidade_anterior', 'quantidade_movimentada', 'quantidade_nova', 'motivo', 'data_hora')
date_hierarchy = 'data_hora'
ordering = ('-data_hora',)
```

### EstoqueMovimentacaoAdmin.has_add_permission

Linha 648: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:648>).

```python
def has_add_permission(self, request):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### EstoqueMovimentacaoAdmin.has_change_permission

Linha 651: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:651>).

```python
def has_change_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### EstoqueMovimentacaoAdmin.has_delete_permission

Linha 654: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:654>).

```python
def has_delete_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### TriagemAdmin

Linha 659: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:659>).

Classe; herda de: admin.ModelAdmin.

**Explicacao presente no codigo:**

> Permite ao administrador consultar as triagens realizadas.
> 
> Os dados ficam somente para consulta no painel administrativo.

**Decoradores:** `admin.register(Triagem)`.

**Atributos/campos declarados diretamente:**

```python
list_display = ('id_triagem', 'usuario', 'modalidade', 'status', 'resultado', 'regra_version', 'data_liberacao', 'iniciada_em', 'finalizada_em')
list_filter = ('modalidade', 'status', 'resultado', 'regra_version', 'iniciada_em')
search_fields = ('usuario__nome', 'usuario__email', 'regra_version')
readonly_fields = ('id_triagem', 'usuario', 'modalidade', 'status', 'pergunta_atual', 'fluxo_perguntas', 'triagem_base', 'regra_version', 'resultado', 'mensagem_resultado', 'data_liberacao', 'achados', 'iniciada_em', 'finalizada_em', 'atualizada_em')
date_hierarchy = 'iniciada_em'
ordering = ('-iniciada_em',)
```

### TriagemAdmin.has_add_permission

Linha 721: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:721>).

```python
def has_add_permission(self, request):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### TriagemAdmin.has_change_permission

Linha 725: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:725>).

```python
def has_change_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### TriagemAdmin.has_delete_permission

Linha 729: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:729>).

```python
def has_delete_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### RespostaTriagemAdmin

Linha 734: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:734>).

Classe; herda de: admin.ModelAdmin.

**Explicacao presente no codigo:**

> Permite consultar as respostas individuais das triagens.

**Decoradores:** `admin.register(RespostaTriagem)`.

**Atributos/campos declarados diretamente:**

```python
list_display = ('id_resposta', 'triagem', 'id_pergunta', 'codigo_resposta', 'resposta_label', 'data_evento', 'respondido_em')
list_filter = ('id_pergunta', 'rule_version', 'respondido_em')
search_fields = ('triagem__usuario__nome', 'triagem__usuario__email', 'id_pergunta', 'codigo_resposta', 'resposta_label')
readonly_fields = ('id_resposta', 'triagem', 'id_pergunta', 'codigo_resposta', 'resposta_label', 'data_evento', 'metadata', 'valor', 'rule_version', 'source_ref', 'respondido_em')
ordering = ('-respondido_em',)
```

### RespostaTriagemAdmin.has_add_permission

Linha 785: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:785>).

```python
def has_add_permission(self, request):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### RespostaTriagemAdmin.has_change_permission

Linha 789: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:789>).

```python
def has_change_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### RespostaTriagemAdmin.has_delete_permission

Linha 793: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:793>).

```python
def has_delete_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### NotificacaoAdmin

Linha 798: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:798>).

Classe; herda de: admin.ModelAdmin.

**Explicacao presente no codigo:**

> Permite consultar os avisos internos enviados aos usuarios.

**Decoradores:** `admin.register(Notificacao)`.

**Atributos/campos declarados diretamente:**

```python
list_display = ('usuario', 'tipo', 'titulo', 'lida', 'criada_em')
list_filter = ('tipo', 'lida', 'criada_em')
search_fields = ('usuario__email', 'usuario__nome', 'titulo', 'mensagem')
readonly_fields = ('criada_em', 'lida_em')
ordering = ('-criada_em',)
```

### NotificacaoAdmin.has_add_permission

Linha 829: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:829>).

```python
def has_add_permission(self, request):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### NotificacaoAdmin.has_change_permission

Linha 832: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:832>).

```python
def has_change_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### NotificacaoAdmin.has_delete_permission

Linha 835: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:835>).

```python
def has_delete_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### PedidoSangueAdmin

Linha 840: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:840>).

Classe; herda de: admin.ModelAdmin.

**Explicacao presente no codigo:**

> Consulta administrativa dos pedidos de sangue.
> 
> A validacao deve acontecer pela camada de servico e pelo painel de
> validacao, nao editando status manualmente no admin.

**Decoradores:** `admin.register(PedidoSangue)`.

**Atributos/campos declarados diretamente:**

```python
list_display = ('id_pedido', 'titulo', 'solicitante', 'contato', 'hemocentro_destino', 'tipo_sanguineo', 'urgencia', 'cidade', 'status', 'data_criacao')
list_filter = ('status', 'urgencia', 'tipo_sanguineo', 'data_criacao')
search_fields = ('titulo', 'cidade', 'solicitante__email', 'solicitante__nome', 'hemocentro_destino__email', 'hemocentro_destino__nome')
readonly_fields = ('id_pedido', 'status', 'data_criacao', 'atualizado_em')
date_hierarchy = 'data_criacao'
ordering = ('-data_criacao',)
```

### PedidoSangueAdmin.has_add_permission

Linha 887: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:887>).

```python
def has_add_permission(self, request):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### PedidoSangueAdmin.has_change_permission

Linha 890: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:890>).

```python
def has_change_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### PedidoSangueAdmin.has_delete_permission

Linha 893: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:893>).

```python
def has_delete_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### ValidacaoPedidoAdmin

Linha 898: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:898>).

Classe; herda de: admin.ModelAdmin.

**Explicacao presente no codigo:**

> Historico somente leitura das validacoes de pedidos.

**Decoradores:** `admin.register(ValidacaoPedido)`.

**Atributos/campos declarados diretamente:**

```python
list_display = ('data_validacao', 'pedido', 'status_validacao', 'moderador', 'motivo_resumido')
list_filter = ('status_validacao', 'data_validacao')
search_fields = ('pedido__titulo', 'pedido__cidade', 'moderador__email', 'moderador__nome', 'motivo')
readonly_fields = ('id_validacao', 'pedido', 'status_validacao', 'motivo', 'moderador', 'data_validacao')
date_hierarchy = 'data_validacao'
ordering = ('-data_validacao',)
motivo_resumido.short_description = 'Motivo'
```

### ValidacaoPedidoAdmin.motivo_resumido

Linha 934: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:934>).

```python
def motivo_resumido(self, obj):
```

**Chamadas utilizadas no corpo:** `len`.

**Expressoes de retorno (dependem do caminho):**

- `f'{obj.motivo[:77]}...'`
- `obj.motivo`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

### ValidacaoPedidoAdmin.has_add_permission

Linha 942: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:942>).

```python
def has_add_permission(self, request):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### ValidacaoPedidoAdmin.has_change_permission

Linha 945: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:945>).

```python
def has_change_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

### ValidacaoPedidoAdmin.has_delete_permission

Linha 948: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:948>).

```python
def has_delete_permission(self, request, obj=None):
```

**Expressoes de retorno (dependem do caminho):**

- `False`

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).


## accounts/apps.py

Inicializacao do app e conexao dos sinais.

Original: [accounts/apps.py](<C:/Users/lb119/Elo/accounts/apps.py>).

**Dependencias importadas:**

```python
from django.apps import AppConfig
```

### AccountsConfig

Linha 11: [accounts/apps.py](<C:/Users/lb119/Elo/accounts/apps.py:11>).

Classe; herda de: AppConfig.

**Explicacao presente no codigo:**

> Metadados basicos do app de contas.

**Atributos/campos declarados diretamente:**

```python
default_auto_field = 'django.db.models.BigAutoField'
name = 'accounts'
verbose_name = 'Contas e autenticacao'
```

### AccountsConfig.ready

Linha 23: [accounts/apps.py](<C:/Users/lb119/Elo/accounts/apps.py:23>).

```python
def ready(self):
```

**Explicacao presente no codigo:**

> Carrega os sinais de auditoria quando o app inicia.


## accounts/auditoria.py

Registro de eventos e observacao de acessos sensiveis.

Original: [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py>).

**Dependencias importadas:**

```python
from ipaddress import ip_address
from django.forms.models import model_to_dict
from django.utils.deprecation import MiddlewareMixin
from .models import AuditoriaAcaoCritica
```

### obter_ip

Linha 28: [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:28>).

```python
def obter_ip(request):
```

**Explicacao presente no codigo:**

> Usa o endereco da conexao, sem confiar em cabecalhos enviados pelo cliente.

**Chamadas utilizadas no corpo:** `ip_address`, `request.META.get`, `str`.

**Expressoes de retorno (dependem do caminho):**

- `None`
- `str(ip_address(request.META.get('REMOTE_ADDR', '')))`

**Estrutura de controle:** If: 1, Try: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `registrar_auditoria` em [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:81>).
- `atualizar_preferencia_convocacao` em [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:112>).
- `auditar_login_falho` em [accounts/signals.py](<C:/Users/lb119/Elo/accounts/signals.py:23>).
- `AuditoriaTests.test_ip_nao_confia_em_cabecalho_do_cliente` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:418>).
- `cadastro` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:588>).
- `triagem_iniciar` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1074>).
- `triagem_pergunta` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1138>).

### obter_user_agent

Linha 40: [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:40>).

```python
def obter_user_agent(request):
```

**Explicacao presente no codigo:**

> Extrai o user agent sem obrigar chamadas internas a terem request.

**Chamadas utilizadas no corpo:** `request.META.get`.

**Expressoes de retorno (dependem do caminho):**

- `''`
- `request.META.get('HTTP_USER_AGENT', '')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `registrar_auditoria` em [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:81>).
- `auditar_login_falho` em [accounts/signals.py](<C:/Users/lb119/Elo/accounts/signals.py:23>).

### limpar_metadados

Linha 48: [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:48>).

```python
def limpar_metadados(valor):
```

**Explicacao presente no codigo:**

> Remove dados sensiveis de estruturas simples antes de salvar auditoria.

**Chamadas utilizadas no corpo:** `chave_texto.lower`, `isinstance`, `limpar_metadados`, `str`, `valor.items`.

**Expressoes de retorno (dependem do caminho):**

- `[limpar_metadados(item) for item in valor]`
- `metadados_limpos`
- `valor`

**Estrutura de controle:** If: 3, For: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `registrar_auditoria` em [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:81>).

### identificar_alvo

Linha 67: [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:67>).

```python
def identificar_alvo(alvo):
```

**Explicacao presente no codigo:**

> Transforma um model ou valor simples em alvo_tipo e alvo_id.

**Chamadas utilizadas no corpo:** `hasattr`, `str`.

**Expressoes de retorno (dependem do caminho):**

- `('', '')`
- `(alvo.__class__.__name__, str(alvo))`
- `(alvo_tipo, str(chave_primaria or ''))`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `registrar_auditoria` em [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:81>).

### registrar_auditoria

Linha 81: [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:81>).

```python
def registrar_auditoria(*, acao, usuario=None, resultado=AuditoriaAcaoCritica.Resultado.SUCESSO, alvo=None, alvo_tipo='', alvo_id='', descricao='', request=None, ip=None, user_agent='', metadados=None):
```

**Explicacao presente no codigo:**

> Cria um registro de auditoria padronizado e sanitizado.

**Chamadas utilizadas no corpo:** `AuditoriaAcaoCritica.objects.create`, `getattr`, `identificar_alvo`, `limpar_metadados`, `obter_ip`, `obter_user_agent`.

**Expressoes de retorno (dependem do caminho):**

- `AuditoriaAcaoCritica.objects.create(usuario=usuario, acao=acao, resultado=resultado, alvo_tipo=alvo_tipo or tipo_detectado, alvo_id=alvo_id or id_detectado, descricao=descricao, ip=ip or obter_ip(request), user_agent=user_agent or obter_user_agent(request), metadados=limpar_metadados(metadados or {}))`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `UsuarioAdmin.save_model` em [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:184>).
- `UsuarioAdmin.save_related` em [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:320>).
- `ConsentimentoLGPDAdmin.save_model` em [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:456>).
- `AuditoriaAcessosMiddleware.process_response` em [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:160>).
- `atualizar_preferencia_convocacao` em [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:112>).
- `cadastrar_estoque` em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:131>).
- `registrar_movimentacao_estoque` em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:200>).
- `publicar_pedido` em [accounts/pedidos.py](<C:/Users/lb119/Elo/accounts/pedidos.py:25>).
- `auditar_login_falho` em [accounts/signals.py](<C:/Users/lb119/Elo/accounts/signals.py:23>).
- `AuditoriaTests.test_sanitizacao_recursiva` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:411>).
- `registrar_decisao_validacao_hemocentro` em [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:68>).
- `registrar_decisao_validacao_pedido` em [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:174>).
- `triagem_historico` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1032>).
- `criar_pedido_sangue` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1542>).

### campos_sensiveis_alterados

Linha 116: [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:116>).

```python
def campos_sensiveis_alterados(objeto, campos):
```

**Explicacao presente no codigo:**

> Compara campos sensiveis de um model antes e depois da alteracao.

**Chamadas utilizadas no corpo:** `getattr`, `objeto.__class__.objects.filter`, `objeto.__class__.objects.filter(pk=objeto.pk).first`, `str`.

**Expressoes de retorno (dependem do caminho):**

- `alteracoes`
- `{}`

**Estrutura de controle:** If: 3, For: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `UsuarioAdmin.save_model` em [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py:184>).

### snapshot_campos

Linha 138: [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:138>).

```python
def snapshot_campos(objeto, campos):
```

**Explicacao presente no codigo:**

> Retorna um dicionario com campos simples de um model.

**Chamadas utilizadas no corpo:** `dados.items`, `model_to_dict`, `str`.

**Expressoes de retorno (dependem do caminho):**

- `{campo: str(valor) for campo, valor in dados.items()}`

### AuditoriaAcessosMiddleware

Linha 145: [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:145>).

Classe; herda de: MiddlewareMixin.

**Explicacao presente no codigo:**

> Audita respostas protegidas sem copiar formularios ou dados clinicos.

**Atributos/campos declarados diretamente:**

```python
ROTAS_SENSIVEIS = {'accounts:triagem_pergunta', 'accounts:triagem_resultado', 'accounts:triagem_historico', 'accounts:painel_validacao_pedidos', 'accounts:triagem_revisao', 'accounts:minhas_solicitacoes', 'accounts:painel_pedidos_hemocentro'}
MODELOS_SENSIVEIS_ADMIN = {'usuario', 'triagem', 'respostatriagem', 'consentimentolgpd', 'pedidosangue', 'validacaopedido', 'validacaohemocentro', 'notificacao', 'auditoriaacaocritica'}
```

### AuditoriaAcessosMiddleware.process_response

Linha 160: [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:160>).

```python
def process_response(self, request, response):
```

**Chamadas utilizadas no corpo:** `any`, `getattr`, `nome.startswith`, `registrar_auditoria`.

**Expressoes de retorno (dependem do caminho):**

- `response`

**Estrutura de controle:** If: 3. Abra o original para seguir as condicoes na ordem.

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `CAMPOS_SENSIVEIS`: linha 17; valor declarado em [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:17>).

## accounts/compatibilidade.py

Tabela, normalizacao, elegibilidade, frequencia e preferencia de convocacao.

Original: [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py>).

### normalizar_tipo_sanguineo

Linha 26: [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:26>).

```python
def normalizar_tipo_sanguineo(tipo_sanguineo):
```

**Chamadas utilizadas no corpo:** `(tipo_sanguineo or '').strip`, `(tipo_sanguineo or '').strip().upper`, `ValueError`.

**Expressoes de retorno (dependem do caminho):**

- `tipo`

**Excecoes levantadas:**

- `ValueError('Tipo sanguineo invalido.')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `doadores_compativeis_para` em [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:33>).
- `tipos_que_recebem_de` em [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:38>).
- `obter_estoque_do_hemocentro` em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:120>).
- `cadastrar_estoque` em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:131>).
- `atualizar_tipo_sanguineo_do_usuario` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:358>).

### doadores_compativeis_para

Linha 33: [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:33>).

```python
def doadores_compativeis_para(tipo_solicitado):
```

**Chamadas utilizadas no corpo:** `normalizar_tipo_sanguineo`.

**Expressoes de retorno (dependem do caminho):**

- `COMPATIBILIDADE_RECEBIMENTO[tipo]`

**Onde aparece uma chamada com este nome:**

- `tabela_de_compatibilidade` em [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:47>).
- `doadores_aptos_para_convocacao` em [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:59>).
- `compatibilidade_sanguinea` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:681>).

### tipos_que_recebem_de

Linha 38: [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:38>).

```python
def tipos_que_recebem_de(tipo_doador):
```

**Chamadas utilizadas no corpo:** `COMPATIBILIDADE_RECEBIMENTO.items`, `normalizar_tipo_sanguineo`, `tuple`.

**Expressoes de retorno (dependem do caminho):**

- `tuple((receptor for receptor, doadores in COMPATIBILIDADE_RECEBIMENTO.items() if tipo in doadores))`

**Onde aparece uma chamada com este nome:**

- `tabela_de_compatibilidade` em [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:47>).
- `compatibilidade_sanguinea` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:681>).

### tabela_de_compatibilidade

Linha 47: [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:47>).

```python
def tabela_de_compatibilidade():
```

**Chamadas utilizadas no corpo:** `doadores_compativeis_para`, `tipos_que_recebem_de`.

**Expressoes de retorno (dependem do caminho):**

- `[{'tipo': tipo, 'doar_para': tipos_que_recebem_de(tipo), 'receber_de': doadores_compativeis_para(tipo), 'populacao': POPULACAO_APROXIMADA[tipo]} for tipo in TIPOS_SANGUINEOS]`

**Onde aparece uma chamada com este nome:**

- `compatibilidade_sanguinea` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:681>).

### doadores_aptos_para_convocacao

Linha 59: [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:59>).

```python
def doadores_aptos_para_convocacao(tipo_solicitado):
```

**Explicacao presente no codigo:**

> Aplica a mesma elegibilidade para os alertas de estoque e pedidos.

**Chamadas utilizadas no corpo:** `ConsentimentoLGPD.objects.filter`, `Exists`, `OuterRef`, `Q`, `Subquery`, `Triagem.objects.filter`, `Triagem.objects.filter(usuario=OuterRef('pk'), status=Triagem.Status.CONCLUIDA).order_by`, `Usuario.objects.filter`, `Usuario.objects.filter(perfil=Usuario.Perfil.DOADOR, is_active=True, suspensa=False, aceita_notificacoes_pedidos=True, tipo_sanguineo__in=doadores_compativeis_para(tipo_solicitado)).annotate`, `Usuario.objects.filter(perfil=Usuario.Perfil.DOADOR, is_active=True, suspensa=False, aceita_notificacoes_pedidos=True, tipo_sanguineo__in=doadores_compativeis_para(tipo_solicitado)).annotate(resultado_ultima_triagem=Subquery(ultima_triagem.values('resultado')[:1]), liberacao_ultima_triagem=Subquery(ultima_triagem.values('data_liberacao')[:1]), consentimento_convocacao=Exists(consentimento)).filter`, `Usuario.objects.filter(perfil=Usuario.Perfil.DOADOR, is_active=True, suspensa=False, aceita_notificacoes_pedidos=True, tipo_sanguineo__in=doadores_compativeis_para(tipo_solicitado)).annotate(resultado_ultima_triagem=Subquery(ultima_triagem.values('resultado')[:1]), liberacao_ultima_triagem=Subquery(ultima_triagem.values('data_liberacao')[:1]), consentimento_convocacao=Exists(consentimento)).filter(resultado_ultima_triagem=Triagem.Resultado.APTO, consentimento_convocacao=True).filter`, `Usuario.objects.filter(perfil=Usuario.Perfil.DOADOR, is_active=True, suspensa=False, aceita_notificacoes_pedidos=True, tipo_sanguineo__in=doadores_compativeis_para(tipo_solicitado)).annotate(resultado_ultima_triagem=Subquery(ultima_triagem.values('resultado')[:1]), liberacao_ultima_triagem=Subquery(ultima_triagem.values('data_liberacao')[:1]), consentimento_convocacao=Exists(consentimento)).filter(resultado_ultima_triagem=Triagem.Resultado.APTO, consentimento_convocacao=True).filter(Q(liberacao_ultima_triagem__isnull=True) | Q(liberacao_ultima_triagem__lte=timezone.localdate())).order_by`, `doadores_compativeis_para`, `timezone.localdate`, `ultima_triagem.values`.

**Expressoes de retorno (dependem do caminho):**

- `Usuario.objects.filter(perfil=Usuario.Perfil.DOADOR, is_active=True, suspensa=False, aceita_notificacoes_pedidos=True, tipo_sanguineo__in=doadores_compativeis_para(tipo_solicitado)).annotate(resultado_ultima_triagem=Subquery(ultima_triagem.values('resultado')[:1]), liberacao_ultima_triagem=Subquery(ultima_triagem.values('data_liberacao')[:1]), consentimento_convocacao=Exists(consentimento)).filter(resultado_ultima_triagem=Triagem.Resultado.APTO, consentimento_convocacao=True).filter(Q(liberacao_ultima_triagem__isnull=True) | Q(liberacao_ultima_triagem__lte=timezone.localdate())).order_by('pk')`

**Onde aparece uma chamada com este nome:**

- `criar_notificacoes_para_doadores_compativeis` em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:37>).
- `criar_notificacoes_para_pedido` em [accounts/pedidos.py](<C:/Users/lb119/Elo/accounts/pedidos.py:52>).
- `ConvocacaoCompatibilidadeTests.test_compatibilidade_seleciona_os_tipos_da_tabela` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:513>).
- `PerfisTesteTests.test_cria_perfis_e_preserva_alteracoes_ao_repetir` em [accounts/test_perfis_teste.py](<C:/Users/lb119/Elo/accounts/test_perfis_teste.py:13>).

### limite_convocacao_atingido

Linha 95: [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:95>).

```python
def limite_convocacao_atingido(usuario):
```

**Explicacao presente no codigo:**

> Soma os alertas de estoque e pedidos, mesmo os que ja foram lidos.

**Chamadas utilizadas no corpo:** `Notificacao.objects.filter`, `Notificacao.objects.filter(usuario=usuario, tipo__in=[Notificacao.Tipo.ESTOQUE_BAIXO, Notificacao.Tipo.ESTOQUE_CRITICO, Notificacao.Tipo.PEDIDO_COMPATIVEL], criada_em__gte=inicio).count`, `timedelta`, `timezone.now`.

**Expressoes de retorno (dependem do caminho):**

- `quantidade >= settings.CONVOCACAO_LIMITE_NOTIFICACOES`

**Onde aparece uma chamada com este nome:**

- `criar_notificacoes_para_doadores_compativeis` em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:37>).
- `criar_notificacoes_para_pedido` em [accounts/pedidos.py](<C:/Users/lb119/Elo/accounts/pedidos.py:52>).

### atualizar_preferencia_convocacao

Linha 112: [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:112>).

```python
def atualizar_preferencia_convocacao(usuario, aceita, request=None):
```

**Explicacao presente no codigo:**

> Registra a escolha explicita e sua revogacao nas tabelas existentes.

**Chamadas utilizadas no corpo:** `ConsentimentoLGPD.objects.get_or_create`, `PermissionDenied`, `Usuario.objects.select_for_update`, `Usuario.objects.select_for_update().get`, `bool`, `consentimento.save`, `obter_ip`, `registrar_auditoria`, `timezone.now`, `transaction.atomic`, `usuario.save`.

**Excecoes levantadas:**

- `PermissionDenied('Somente Doadores podem configurar convocacoes.')`

**Estrutura de controle:** If: 3, With: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `FluxoCadastroTriagemPedidosTests.test_publicacao_notifica_somente_doador_apto_compativel` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:323>).
- `cadastro` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:588>).
- `dashboard` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:720>).

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `TIPOS_SANGUINEOS`: linha 1; valor declarado em [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:1>).
- `COMPATIBILIDADE_RECEBIMENTO`: linha 3; valor declarado em [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:3>).
- `POPULACAO_APROXIMADA`: linha 14; valor declarado em [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:14>).

## accounts/estoque.py

Cadastro, movimentacao, estado publico e alertas de estoque.

Original: [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py>).

**Dependencias importadas:**

```python
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.urls import reverse
from .auditoria import registrar_auditoria
from .compatibilidade import normalizar_tipo_sanguineo
from .compatibilidade import doadores_aptos_para_convocacao, limite_convocacao_atingido
from .models import AuditoriaAcaoCritica, Estoque, EstoqueMovimentacao, Notificacao, Usuario
from .validacao_hemocentro import validar_publicacao_hemocentro
```

### criar_notificacoes_para_doadores_compativeis

Linha 37: [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:37>).

```python
def criar_notificacoes_para_doadores_compativeis(*, estoque, status_calculado):
```

**Explicacao presente no codigo:**

> Cria notificacoes internas para doadores compativeis.
> 
> Quando o estoque atualizado fica CRITICO, o sistema procura
> doadores compativeis e aptos que autorizaram convocacoes, respeitando
> o limite conjunto de notificacoes de estoque e pedidos.

**Decoradores:** `transaction.atomic`.

**Chamadas utilizadas no corpo:** `Notificacao`, `Notificacao.objects.bulk_create`, `Notificacao.objects.filter`, `Notificacao.objects.filter(usuario=doador, estoque=estoque, tipo=tipo_notificacao, lida=False).exists`, `doadores_aptos_para_convocacao`, `doadores_aptos_para_convocacao(estoque.tipo_sanguineo).select_for_update`, `len`, `limite_convocacao_atingido`, `notificacoes.append`, `reverse`.

**Expressoes de retorno (dependem do caminho):**

- `0`
- `len(notificacoes)`

**Estrutura de controle:** If: 2, For: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `registrar_movimentacao_estoque` em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:200>).
- `ConvocacaoCompatibilidadeTests.emitir` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:381>).

### calcular_status_calculado

Linha 85: [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:85>).

```python
def calcular_status_calculado(*, quantidade_bolsas, nivel_minimo, nivel_critico):
```

**Explicacao presente no codigo:**

> Deriva o status do estoque a partir da quantidade e dos niveis de alerta.
> 
> Regra:
> - quantidade <= nivel_critico  -> CRITICO;
> - quantidade <= nivel_minimo   -> BAIXO;
> - caso contrario               -> ESTAVEL.

**Expressoes de retorno (dependem do caminho):**

- `Estoque.StatusCalculado.BAIXO`
- `Estoque.StatusCalculado.CRITICO`
- `Estoque.StatusCalculado.ESTAVEL`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `cadastrar_estoque` em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:131>).
- `registrar_movimentacao_estoque` em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:200>).
- `CalcularStatusCalculadoTests.test_quantidade_igual_ao_critico_e_critico` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:73>).
- `CalcularStatusCalculadoTests.test_quantidade_abaixo_do_critico_e_critico` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:81>).
- `CalcularStatusCalculadoTests.test_quantidade_igual_ao_minimo_e_baixo` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:89>).
- `CalcularStatusCalculadoTests.test_quantidade_acima_do_minimo_e_estavel` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:97>).

### validar_responsavel_pelo_estoque

Linha 104: [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:104>).

```python
def validar_responsavel_pelo_estoque(*, estoque, usuario):
```

**Explicacao presente no codigo:**

> Garante que somente o proprio Hemocentro aprovado, dono do estoque,
> possa gerenciar aquele registro.

**Chamadas utilizadas no corpo:** `PermissionDenied`, `validar_publicacao_hemocentro`.

**Expressoes de retorno (dependem do caminho):**

- `True`

**Excecoes levantadas:**

- `PermissionDenied('Este estoque pertence a outro Hemocentro.')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `registrar_movimentacao_estoque` em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:200>).

### obter_estoque_do_hemocentro

Linha 120: [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:120>).

```python
def obter_estoque_do_hemocentro(*, hemocentro, tipo_sanguineo):
```

**Explicacao presente no codigo:**

> Busca um Estoque de um tipo sanguineo especifico.

**Chamadas utilizadas no corpo:** `Estoque.objects.filter`, `Estoque.objects.filter(hemocentro=hemocentro, tipo_sanguineo=tipo).first`, `normalizar_tipo_sanguineo`.

**Expressoes de retorno (dependem do caminho):**

- `Estoque.objects.filter(hemocentro=hemocentro, tipo_sanguineo=tipo).first()`

### cadastrar_estoque

Linha 131: [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:131>).

```python
def cadastrar_estoque(*, hemocentro, tipo_sanguineo, nivel_minimo, nivel_critico, quantidade_bolsas=0, request=None):
```

**Explicacao presente no codigo:**

> UC_29 - Cria a estrutura de estoque de um tipo sanguineo para um
> Hemocentro aprovado.

**Chamadas utilizadas no corpo:** `Estoque.objects.create`, `Estoque.objects.filter`, `Estoque.objects.filter(hemocentro=hemocentro, tipo_sanguineo=tipo).exists`, `ValidationError`, `calcular_status_calculado`, `normalizar_tipo_sanguineo`, `registrar_auditoria`, `transaction.atomic`, `validar_publicacao_hemocentro`.

**Expressoes de retorno (dependem do caminho):**

- `estoque`

**Excecoes levantadas:**

- `ValidationError(f'Ja existe estoque cadastrado para o tipo {tipo} neste hemocentro.')`
- `ValidationError({'nivel_critico': 'O nivel critico deve ser menor ou igual ao nivel minimo.'})`

**Estrutura de controle:** If: 2, With: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `CadastrarEstoqueTests.test_hemocentro_aprovado_cadastra_estoque` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:109>).
- `CadastrarEstoqueTests.test_hemocentro_pendente_nao_pode_cadastrar_estoque` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:129>).
- `CadastrarEstoqueTests.test_nao_permite_cadastro_duplicado` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:138>).
- `CadastrarEstoqueTests.test_nivel_critico_maior_que_minimo_gera_erro` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:154>).
- `CadastrarEstoqueTests.test_tipo_sanguineo_invalido_gera_erro` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:163>).
- `RegistrarMovimentacaoEstoqueTests.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:176>).
- `EstoqueViewsTests.test_post_movimenta_estoque_via_view` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:345>).
- `VisualizacaoPublicaTests.test_consulta_de_estoques_filtra_por_tipo_situacao_e_busca` em [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:133>).
- `VisualizacaoPublicaTests.test_consulta_de_estoques_preserva_parametros_antigos` em [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:175>).
- `cadastrar_estoque_view` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1453>).

### registrar_movimentacao_estoque

Linha 200: [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:200>).

```python
def registrar_movimentacao_estoque(*, estoque, usuario_resp, tipo_movimento, quantidade, motivo='', request=None):
```

**Explicacao presente no codigo:**

> UC_30 - Aplica uma movimentacao de bolsas sobre um Estoque existente
> e grava o historico correspondente.

**Chamadas utilizadas no corpo:** `(motivo or '').strip`, `Estoque.objects.select_for_update`, `Estoque.objects.select_for_update().get`, `EstoqueMovimentacao.objects.create`, `ValidationError`, `calcular_status_calculado`, `criar_notificacoes_para_doadores_compativeis`, `estoque_atual.save`, `registrar_auditoria`, `transaction.atomic`, `validar_responsavel_pelo_estoque`.

**Expressoes de retorno (dependem do caminho):**

- `movimentacao`

**Excecoes levantadas:**

- `ValidationError('Tipo de movimentacao invalido.')`
- `ValidationError({'motivo': 'Informe o motivo da movimentacao de estoque.'})`
- `ValidationError({'quantidade': 'A quantidade ajustada nao pode ser negativa.'})`
- `ValidationError({'quantidade': 'Informe uma quantidade maior que zero.'})`
- `ValidationError({'quantidade': f'Nao ha bolsas suficientes para esta saida. Quantidade atual: {quantidade_anterior}.'})`

**Estrutura de controle:** If: 8, With: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `RegistrarMovimentacaoEstoqueTests.test_entrada_soma_quantidade_e_recalcula_status` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:187>).
- `RegistrarMovimentacaoEstoqueTests.test_saida_subtrai_quantidade` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:204>).
- `RegistrarMovimentacaoEstoqueTests.test_saida_maior_que_estoque_gera_erro_e_nao_altera_nada` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:219>).
- `RegistrarMovimentacaoEstoqueTests.test_ajuste_define_quantidade_absoluta_e_aceita_delta_negativo` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:235>).
- `RegistrarMovimentacaoEstoqueTests.test_motivo_e_obrigatorio_na_movimentacao` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:251>).
- `RegistrarMovimentacaoEstoqueTests.test_movimentacao_gera_historico_e_auditoria` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:268>).
- `RegistrarMovimentacaoEstoqueTests.test_outro_hemocentro_nao_pode_movimentar_estoque_alheio` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:288>).
- `RegistrarMovimentacaoEstoqueTests.test_doador_nao_pode_movimentar_estoque` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:305>).
- `ConvocacaoCompatibilidadeTests.test_atualizacao_de_estoque_convoca_somente_quando_critico` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:436>).
- `atualizar_estoque_view` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1493>).

### calcular_status_publico

Linha 327: [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:327>).

```python
def calcular_status_publico(quantidade_bolsas, nivel_minimo, nivel_critico):
```

**Explicacao presente no codigo:**

> Calcula o status que sera exibido publicamente.
> 
> Os niveis minimo e critico sao utilizados apenas internamente
> para determinar a situacao do estoque.

**Expressoes de retorno (dependem do caminho):**

- `'ADEQUADO'`
- `'ALTO'`
- `'BAIXO'`
- `'CRITICO'`

**Estrutura de controle:** If: 3. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `obter_estoques_publicos` em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:355>).

### obter_estoques_publicos

Linha 355: [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:355>).

```python
def obter_estoques_publicos():
```

**Explicacao presente no codigo:**

> Busca os estoques dos Hemocentros aprovados e retorna somente
> os dados que podem ser exibidos publicamente.

**Chamadas utilizadas no corpo:** `Estoque.objects.select_related`, `Estoque.objects.select_related('hemocentro').filter`, `Estoque.objects.select_related('hemocentro').filter(hemocentro__perfil=Usuario.Perfil.HEMOCENTRO, hemocentro__status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO).order_by`, `calcular_status_publico`, `resultado.append`.

**Expressoes de retorno (dependem do caminho):**

- `resultado`

**Estrutura de controle:** For: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `visualizacao_publica_estoque` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1311>).

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA`: linha 31; valor declarado em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:31>).
- `STATUS_PUBLICO_LABEL`: linha 347; valor declarado em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:347>).

## accounts/forms.py

Campos e validacoes de cadastro, login, estoque, pedidos e filtros.

Original: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py>).

**Dependencias importadas:**

```python
import re
from datetime import date
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .compatibilidade import TIPOS_SANGUINEOS
from .models import EstoqueMovimentacao, PedidoSangue, Usuario
```

### apenas_digitos

Linha 25: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:25>).

```python
def apenas_digitos(valor):
```

**Explicacao presente no codigo:**

> Retira todos os caracteres que nao sejam numeros.

**Chamadas utilizadas no corpo:** `re.sub`.

**Expressoes de retorno (dependem do caminho):**

- `re.sub('\\D', '', valor or '')`

**Onde aparece uma chamada com este nome:**

- `CadastroUsuarioForm.clean_cpf` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:179>).
- `CadastroUsuarioForm.clean_cnpj` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:195>).

### CadastroUsuarioForm

Linha 30: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:30>).

Classe; herda de: UserCreationForm.

**Explicacao presente no codigo:**

> Formulario publico utilizado para criar contas.

**Chamadas utilizadas no corpo:** `forms.BooleanField`, `forms.CharField`, `forms.ChoiceField`, `forms.DateField`, `forms.DateInput`, `forms.TextInput`.

**Atributos/campos declarados diretamente:**

```python
cpf = forms.CharField(label='CPF', required=False, max_length=14, help_text='Obrigatorio para Doador e Receptor/Solicitante.', widget=forms.TextInput(attrs={'placeholder': '000.000.000-00', 'autocomplete': 'off', 'inputmode': 'numeric'}))
cnpj = forms.CharField(label='CNPJ', required=False, max_length=18, help_text='Obrigatorio somente para Hemocentro.', widget=forms.TextInput(attrs={'placeholder': '00.000.000/0000-00', 'autocomplete': 'off', 'inputmode': 'numeric'}))
perfil = forms.ChoiceField(label='Tipo de perfil', choices=[(Usuario.Perfil.DOADOR, 'Doador'), (Usuario.Perfil.RECEPTOR, 'Receptor / Solicitante'), (Usuario.Perfil.HEMOCENTRO, 'Hemocentro'), (Usuario.Perfil.OBSERVADOR, 'Observador')], help_text='Escolha Hemocentro somente para uma instituicao que sera analisada por um administrador.', widget=forms.RadioSelect)
data_nascimento = forms.DateField(label='Data de nascimento', required=False, help_text='Obrigatoria para Doador e Receptor/Solicitante.', widget=forms.DateInput(attrs={'type': 'date'}))
aceite_lgpd = forms.BooleanField(label='Li e aceito os Termos de Uso e a Politica de Privacidade.', required=True)
aceita_notificacoes_pedidos = forms.BooleanField(label='Autorizo alertas internos de estoque e pedidos compativeis (para Doadores).', required=False, initial=False, help_text='Opcional. Posso cancelar a autorizacao no meu painel.')
```

**Onde aparece uma chamada com este nome:**

- `FluxoCadastroTriagemPedidosTests.test_cadastro_nao_permite_admin_e_exige_consentimento` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:77>).
- `cadastro` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:588>).

### CadastroUsuarioForm.Meta

Linha 99: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:99>).

Classe; herda de: nenhuma classe declarada.

**Chamadas utilizadas no corpo:** `forms.EmailInput`, `forms.TextInput`.

**Atributos/campos declarados diretamente:**

```python
model = Usuario
fields = ['nome', 'email', 'perfil', 'cpf', 'cnpj', 'telefone', 'data_nascimento', 'sexo', 'cidade', 'estado', 'password1', 'password2', 'aceite_lgpd', 'aceita_notificacoes_pedidos']
labels = {'nome': 'Nome completo', 'email': 'E-mail', 'telefone': 'Telefone', 'sexo': 'Sexo', 'cidade': 'Cidade', 'estado': 'Estado (UF)'}
widgets = {'email': forms.EmailInput(attrs={'autocomplete': 'email'}), 'telefone': forms.TextInput(attrs={'placeholder': '(00) 00000-0000', 'inputmode': 'tel'}), 'estado': forms.TextInput(attrs={'maxlength': 2, 'placeholder': 'MG', 'style': 'text-transform: uppercase;'})}
```

### CadastroUsuarioForm.__init__

Linha 149: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:149>).

```python
def __init__(self, *args, **kwargs):
```

**Chamadas utilizadas no corpo:** `super`, `super().__init__`.

**Onde aparece uma chamada com este nome:**

- `PedidoSangueForm.__init__` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:642>).
- `FormularioPergunta.__init__` em [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:27>).
- `FormularioPergunta.__init__` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:128>).

### CadastroUsuarioForm.clean_nome

Linha 159: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:159>).

```python
def clean_nome(self):
```

**Explicacao presente no codigo:**

> Remove espacos desnecessarios do nome.

**Chamadas utilizadas no corpo:** `(self.cleaned_data.get('nome') or '').strip`, `forms.ValidationError`, `self.cleaned_data.get`.

**Expressoes de retorno (dependem do caminho):**

- `nome`

**Excecoes levantadas:**

- `forms.ValidationError('Informe o nome completo.')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

### CadastroUsuarioForm.clean_email

Linha 168: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:168>).

```python
def clean_email(self):
```

**Explicacao presente no codigo:**

> Padroniza o e-mail e verifica duplicidade.

**Chamadas utilizadas no corpo:** `(self.cleaned_data.get('email') or '').strip`, `(self.cleaned_data.get('email') or '').strip().lower`, `Usuario.objects.filter`, `Usuario.objects.filter(email__iexact=email).exists`, `forms.ValidationError`, `self.cleaned_data.get`.

**Expressoes de retorno (dependem do caminho):**

- `email`

**Excecoes levantadas:**

- `forms.ValidationError('Ja existe uma conta cadastrada com este e-mail.')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

### CadastroUsuarioForm.clean_cpf

Linha 179: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:179>).

```python
def clean_cpf(self):
```

**Explicacao presente no codigo:**

> Limpa e valida o CPF.

**Chamadas utilizadas no corpo:** `Usuario.objects.filter`, `Usuario.objects.filter(cpf=cpf).exists`, `apenas_digitos`, `forms.ValidationError`, `len`, `self.cleaned_data.get`.

**Expressoes de retorno (dependem do caminho):**

- `cpf or None`

**Excecoes levantadas:**

- `forms.ValidationError('Este CPF ja esta cadastrado.')`
- `forms.ValidationError('O CPF deve conter exatamente 11 numeros.')`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

### CadastroUsuarioForm.clean_cnpj

Linha 195: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:195>).

```python
def clean_cnpj(self):
```

**Explicacao presente no codigo:**

> Limpa e valida o CNPJ.

**Chamadas utilizadas no corpo:** `Usuario.objects.filter`, `Usuario.objects.filter(cnpj=cnpj).exists`, `apenas_digitos`, `forms.ValidationError`, `len`, `self.cleaned_data.get`.

**Expressoes de retorno (dependem do caminho):**

- `cnpj or None`

**Excecoes levantadas:**

- `forms.ValidationError('Este CNPJ ja esta cadastrado.')`
- `forms.ValidationError('O CNPJ deve conter exatamente 14 numeros.')`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

### CadastroUsuarioForm.clean_estado

Linha 211: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:211>).

```python
def clean_estado(self):
```

**Explicacao presente no codigo:**

> Padroniza a UF.

**Chamadas utilizadas no corpo:** `(self.cleaned_data.get('estado') or '').strip`, `(self.cleaned_data.get('estado') or '').strip().upper`, `forms.ValidationError`, `len`, `self.cleaned_data.get`.

**Expressoes de retorno (dependem do caminho):**

- `estado`

**Excecoes levantadas:**

- `forms.ValidationError('Informe a UF com 2 letras, por exemplo: MG.')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

### CadastroUsuarioForm.clean_password1

Linha 222: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:222>).

```python
def clean_password1(self):
```

**Explicacao presente no codigo:**

> Valida a senha.

**Chamadas utilizadas no corpo:** `bool`, `forms.ValidationError`, `len`, `re.search`, `self.cleaned_data.get`.

**Expressoes de retorno (dependem do caminho):**

- `senha`

**Excecoes levantadas:**

- `forms.ValidationError('A senha deve possuir pelo menos 8 caracteres.')`
- `forms.ValidationError('A senha precisa conter pelo menos uma letra e um numero.')`

**Estrutura de controle:** If: 3. Abra o original para seguir as condicoes na ordem.

### CadastroUsuarioForm.clean

Linha 244: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:244>).

```python
def clean(self):
```

**Explicacao presente no codigo:**

> Faz as validacoes que dependem do tipo de perfil.
> 
> Regras:
> 
> - Hemocentro -> CNPJ obrigatorio.
> - Doador/Receptor -> CPF e data de nascimento obrigatorios.
> - Observador -> pode ficar sem CPF/CNPJ.

**Chamadas utilizadas no corpo:** `dados.get`, `self.add_error`, `super`, `super().clean`.

**Expressoes de retorno (dependem do caminho):**

- `dados`

**Estrutura de controle:** If: 9. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `TriagemExtensaForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:436>).
- `CadastrarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:506>).
- `MovimentarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:559>).
- `PedidoSangueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:681>).
- `Usuario.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:187>).
- `ValidacaoHemocentro.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:277>).
- `Estoque.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:751>).
- `PedidoSangue.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1068>).
- `FormularioPergunta.clean` em [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:105>).

### PreferenciaConvocacaoForm

Linha 307: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:307>).

Classe; herda de: forms.Form.

**Chamadas utilizadas no corpo:** `forms.BooleanField`.

**Atributos/campos declarados diretamente:**

```python
aceita_convocacoes = forms.BooleanField(label='Autorizo receber alertas internos de estoque e pedidos compativeis.', required=False, help_text='Opcional. Desmarque para cancelar futuras convocacoes.')
```

**Onde aparece uma chamada com este nome:**

- `dashboard` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:720>).

### LoginUsuarioForm

Linha 315: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:315>).

Classe; herda de: AuthenticationForm.

**Explicacao presente no codigo:**

> Formulario de login usando e-mail.

**Chamadas utilizadas no corpo:** `forms.CharField`, `forms.EmailField`, `forms.EmailInput`, `forms.PasswordInput`.

**Atributos/campos declarados diretamente:**

```python
username = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'autocomplete': 'email', 'autofocus': True}))
password = forms.CharField(label='Senha', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
```

### LoginUsuarioForm.confirm_login_allowed

Linha 318: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:318>).

```python
def confirm_login_allowed(self, user):
```

**Chamadas utilizadas no corpo:** `forms.ValidationError`, `getattr`, `super`, `super().confirm_login_allowed`.

**Excecoes levantadas:**

- `forms.ValidationError('Esta conta está suspensa. Procure o administrador.', code='inactive')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

### TriagemExtensaForm

Linha 347: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:347>).

Classe; herda de: forms.Form.

**Explicacao presente no codigo:**

> Formulário inicial da triagem extensa.
> 
> Esta primeira etapa utiliza as perguntas EXT-01 até EXT-05B
> da especificação.

**Chamadas utilizadas no corpo:** `forms.ChoiceField`, `forms.DateField`, `forms.DateInput`.

**Atributos/campos declarados diretamente:**

```python
entende_orientacao = forms.ChoiceField(label='Você entende que esta triagem é apenas uma orientação e que a decisão final será feita pela equipe do hemocentro?', choices=[('SIM', 'Sim, entendo e quero continuar.'), ('NAO', 'Não entendi ou quero receber a explicação novamente.')], widget=forms.RadioSelect)
idade = forms.ChoiceField(label='Qual é a sua idade hoje?', choices=[('MENOS_16', 'Menos de 16 anos'), ('16_17', '16 ou 17 anos'), ('18_60', '18 a 60 anos'), ('61_69', '61 a 69 anos'), ('70_MAIS', '70 anos ou mais')], widget=forms.RadioSelect)
peso = forms.ChoiceField(label='Quanto você pesa aproximadamente?', choices=[('MENOS_50', 'Menos de 50 kg'), ('50_55_9', 'De 50 a 55,9 kg'), ('56_129_9', 'De 56 a 129,9 kg'), ('130_MAIS', '130 kg ou mais'), ('NAO_SEI', 'Não sei meu peso atual')], widget=forms.RadioSelect)
sexo_biologico = forms.ChoiceField(label='Qual opção corresponde ao seu sexo biológico?', choices=[('FEMININO', 'Feminino'), ('MASCULINO', 'Masculino'), ('OUTRO', 'Outra situação ou não sei qual regra se aplica'), ('NAO_INFORMAR', 'Prefiro não informar')], widget=forms.RadioSelect)
ja_doou = forms.ChoiceField(label='Você já doou sangue alguma vez?', choices=[('NAO', 'Nunca doei'), ('SIM', 'Sim, já doei'), ('NAO_LEMBRO', 'Não tenho certeza ou não lembro')], widget=forms.RadioSelect)
data_ultima_doacao = forms.DateField(label='Qual foi a data da sua última doação de sangue total?', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
doacoes_12_meses = forms.ChoiceField(label='Quantas doações de sangue total você fez nos últimos 12 meses?', required=False, choices=[('0', 'Nenhuma'), ('1', '1'), ('2', '2'), ('3', '3'), ('4_MAIS', '4 ou mais'), ('NAO_LEMBRO', 'Não lembro')], widget=forms.RadioSelect)
```

### TriagemExtensaForm.clean

Linha 436: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:436>).

```python
def clean(self):
```

**Explicacao presente no codigo:**

> Exige data e quantidade de doações quando o usuário
> informa que já doou sangue.

**Chamadas utilizadas no corpo:** `dados.get`, `date.today`, `self.add_error`, `super`, `super().clean`.

**Expressoes de retorno (dependem do caminho):**

- `dados`

**Estrutura de controle:** If: 3. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `CadastroUsuarioForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:244>).
- `CadastrarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:506>).
- `MovimentarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:559>).
- `PedidoSangueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:681>).
- `Usuario.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:187>).
- `ValidacaoHemocentro.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:277>).
- `Estoque.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:751>).
- `PedidoSangue.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1068>).
- `FormularioPergunta.clean` em [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:105>).

### CadastrarEstoqueForm

Linha 468: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:468>).

Classe; herda de: forms.Form.

**Explicacao presente no codigo:**

> UC_29 - Formulario usado pelo Hemocentro para cadastrar a estrutura
> de estoque de um tipo sanguineo.
> 
> A validacao de "ja existe estoque para este tipo" e de "hemocentro
> aprovado" fica na camada de servico (accounts/estoque.py), porque
> depende do usuario logado, que o form nao conhece sozinho.

**Chamadas utilizadas no corpo:** `forms.ChoiceField`, `forms.IntegerField`.

**Atributos/campos declarados diretamente:**

```python
tipo_sanguineo = forms.ChoiceField(label='Tipo sanguíneo', choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS])
quantidade_bolsas = forms.IntegerField(label='Quantidade atual de bolsas', min_value=0, initial=0, help_text='Quantidade de bolsas já disponíveis, se houver.')
nivel_minimo = forms.IntegerField(label='Nível mínimo', min_value=0, help_text='A partir de quantas bolsas o tipo passa a ser considerado baixo.')
nivel_critico = forms.IntegerField(label='Nível crítico', min_value=0, help_text='A partir de quantas bolsas o tipo passa a ser considerado crítico.')
```

**Onde aparece uma chamada com este nome:**

- `estoque_hemocentro` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1400>).
- `cadastrar_estoque_view` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1453>).

### CadastrarEstoqueForm.clean

Linha 506: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:506>).

```python
def clean(self):
```

**Explicacao presente no codigo:**

> Garante que o nível crítico nunca seja maior que o mínimo.

**Chamadas utilizadas no corpo:** `dados.get`, `self.add_error`, `super`, `super().clean`.

**Expressoes de retorno (dependem do caminho):**

- `dados`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `CadastroUsuarioForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:244>).
- `TriagemExtensaForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:436>).
- `MovimentarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:559>).
- `PedidoSangueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:681>).
- `Usuario.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:187>).
- `ValidacaoHemocentro.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:277>).
- `Estoque.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:751>).
- `PedidoSangue.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1068>).
- `FormularioPergunta.clean` em [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:105>).

### MovimentarEstoqueForm

Linha 527: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:527>).

Classe; herda de: forms.Form.

**Explicacao presente no codigo:**

> Formulario usado pelo Hemocentro para registrar entrada,
> saída ou ajuste de bolsas em um estoque já cadastrado.

**Chamadas utilizadas no corpo:** `forms.CharField`, `forms.ChoiceField`, `forms.IntegerField`, `forms.Textarea`.

**Atributos/campos declarados diretamente:**

```python
tipo_movimento = forms.ChoiceField(label='Tipo de movimentação', choices=EstoqueMovimentacao.TipoMovimento.choices, widget=forms.RadioSelect)
quantidade = forms.IntegerField(label='Quantidade', min_value=0, help_text='Para entrada/saída: quantidade a movimentar. Para ajuste: nova quantidade total de bolsas.')
motivo = forms.CharField(label='Motivo', required=True, max_length=255, widget=forms.Textarea(attrs={'rows': 3}), help_text='Obrigatório. Ex.: doação recebida, transfusão realizada, contagem física.')
```

**Onde aparece uma chamada com este nome:**

- `estoque_hemocentro` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1400>).
- `atualizar_estoque_view` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1493>).

### MovimentarEstoqueForm.clean

Linha 559: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:559>).

```python
def clean(self):
```

**Chamadas utilizadas no corpo:** `dados.get`, `self.add_error`, `super`, `super().clean`.

**Expressoes de retorno (dependem do caminho):**

- `dados`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `CadastroUsuarioForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:244>).
- `TriagemExtensaForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:436>).
- `CadastrarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:506>).
- `PedidoSangueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:681>).
- `Usuario.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:187>).
- `ValidacaoHemocentro.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:277>).
- `Estoque.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:751>).
- `PedidoSangue.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1068>).
- `FormularioPergunta.clean` em [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:105>).

### PedidoSangueForm

Linha 582: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:582>).

Classe; herda de: forms.ModelForm.

**Explicacao presente no codigo:**

> Formulário para solicitar a divulgação de uma necessidade.
> 
> As validacoes mais sensiveis ficam em validacao_pedido.py.
> Aqui ficam as validacoes de formulario.

**Chamadas utilizadas no corpo:** `forms.EmailField`, `forms.EmailInput`.

**Atributos/campos declarados diretamente:**

```python
contato = forms.EmailField(label='E-mail de contato', widget=forms.EmailInput(attrs={'autocomplete': 'email', 'placeholder': 'seuemail@exemplo.com'}))
```

**Onde aparece uma chamada com este nome:**

- `ConvocacaoCompatibilidadeTests.test_publicacao_alternativa_tambem_convoca` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:501>).
- `PedidoSangueTests.test_formulario_lista_apenas_hemocentros_aprovados` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:78>).
- `PedidoSangueTests.test_formulario_rejeita_descricao_curta` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:116>).
- `PedidoSangueTests.test_formulario_exige_email_no_contato` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:122>).
- `PedidoSangueTests.test_formulario_rejeita_hemocentro_pendente` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:138>).
- `PedidoSangueTests.test_urgencia_critica_exige_justificativa` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:148>).
- `criar_pedido_sangue` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1542>).

### PedidoSangueForm.Meta

Linha 600: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:600>).

Classe; herda de: nenhuma classe declarada.

**Chamadas utilizadas no corpo:** `forms.Textarea`.

**Atributos/campos declarados diretamente:**

```python
model = PedidoSangue
fields = ['nome_solicitante', 'contato', 'para_quem', 'hemocentro_destino', 'titulo', 'tipo_sanguineo', 'urgencia', 'cidade', 'nome_paciente', 'descricao', 'justificativa_urgencia', 'informacoes_complementares']
labels = {'para_quem': 'Para quem e este pedido?', 'nome_solicitante': 'Nome ou identificação do solicitante', 'contato': 'E-mail de contato', 'hemocentro_destino': 'Hemocentro de destino', 'titulo': 'Titulo do pedido', 'tipo_sanguineo': 'Tipo sanguineo', 'urgencia': 'Urgencia', 'cidade': 'Cidade', 'nome_paciente': 'Nome da pessoa (opcional)', 'descricao': 'Descricao', 'justificativa_urgencia': 'Justificativa da urgencia', 'informacoes_complementares': 'Informações complementares'}
widgets = {'para_quem': forms.RadioSelect, 'tipo_sanguineo': forms.RadioSelect, 'urgencia': forms.RadioSelect, 'descricao': forms.Textarea(attrs={'rows': 5}), 'justificativa_urgencia': forms.Textarea(attrs={'rows': 4}), 'informacoes_complementares': forms.Textarea(attrs={'rows': 4})}
```

### PedidoSangueForm.__init__

Linha 642: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:642>).

```python
def __init__(self, *args, **kwargs):
```

**Chamadas utilizadas no corpo:** `Usuario.objects.filter`, `Usuario.objects.filter(perfil=Usuario.Perfil.HEMOCENTRO, status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO).order_by`, `super`, `super().__init__`.

**Onde aparece uma chamada com este nome:**

- `CadastroUsuarioForm.__init__` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:149>).
- `FormularioPergunta.__init__` em [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:27>).
- `FormularioPergunta.__init__` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:128>).

### PedidoSangueForm.clean_nome_paciente

Linha 654: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:654>).

```python
def clean_nome_paciente(self):
```

**Chamadas utilizadas no corpo:** `(self.cleaned_data.get('nome_paciente') or '').strip`, `self.cleaned_data.get`.

**Expressoes de retorno (dependem do caminho):**

- `(self.cleaned_data.get('nome_paciente') or '').strip()`

### PedidoSangueForm.clean_nome_solicitante

Linha 657: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:657>).

```python
def clean_nome_solicitante(self):
```

**Chamadas utilizadas no corpo:** `(self.cleaned_data.get('nome_solicitante') or '').strip`, `forms.ValidationError`, `self.cleaned_data.get`.

**Expressoes de retorno (dependem do caminho):**

- `nome`

**Excecoes levantadas:**

- `forms.ValidationError('Informe o nome ou uma identificação do solicitante.')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

### PedidoSangueForm.clean_contato

Linha 665: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:665>).

```python
def clean_contato(self):
```

**Chamadas utilizadas no corpo:** `(self.cleaned_data.get('contato') or '').strip`, `contato.lower`, `forms.ValidationError`, `self.cleaned_data.get`.

**Expressoes de retorno (dependem do caminho):**

- `contato.lower()`

**Excecoes levantadas:**

- `forms.ValidationError('Informe um e-mail para retorno.')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

### PedidoSangueForm.clean_descricao

Linha 671: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:671>).

```python
def clean_descricao(self):
```

**Chamadas utilizadas no corpo:** `(self.cleaned_data.get('descricao') or '').strip`, `forms.ValidationError`, `len`, `self.cleaned_data.get`.

**Expressoes de retorno (dependem do caminho):**

- `descricao`

**Excecoes levantadas:**

- `forms.ValidationError('Descreva a necessidade com pelo menos 10 caracteres.')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

### PedidoSangueForm.clean

Linha 681: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:681>).

```python
def clean(self):
```

**Chamadas utilizadas no corpo:** `(dados.get('justificativa_urgencia') or '').strip`, `dados.get`, `len`, `self.add_error`, `super`, `super().clean`.

**Expressoes de retorno (dependem do caminho):**

- `dados`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `CadastroUsuarioForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:244>).
- `TriagemExtensaForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:436>).
- `CadastrarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:506>).
- `MovimentarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:559>).
- `Usuario.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:187>).
- `ValidacaoHemocentro.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:277>).
- `Estoque.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:751>).
- `PedidoSangue.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1068>).
- `FormularioPergunta.clean` em [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:105>).

### FiltroPedidoSangueForm

Linha 705: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:705>).

Classe; herda de: forms.Form.

**Explicacao presente no codigo:**

> RF - Visualizar e filtrar pedidos.
> 
> Filtros:
> 
> - tipo sanguineo;
> - urgencia;
> - cidade;
> - hemocentro;
> - data.

**Chamadas utilizadas no corpo:** `forms.CharField`, `forms.ChoiceField`, `forms.DateField`, `forms.DateInput`, `list`.

**Atributos/campos declarados diretamente:**

```python
tipo_sanguineo = forms.ChoiceField(label='Tipo sanguineo', required=False, choices=[('', 'Todos')] + [(tipo, tipo) for tipo in TIPOS_SANGUINEOS])
urgencia = forms.ChoiceField(label='Urgencia', required=False, choices=[('', 'Todas')] + list(PedidoSangue.Urgencia.choices))
cidade = forms.CharField(label='Cidade', required=False)
hemocentro = forms.CharField(label='Hemocentro', required=False)
data = forms.DateField(label='Data', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
status = forms.ChoiceField(label='Status', required=False, choices=[('', 'Todos')] + list(PedidoSangue.Status.choices))
```

**Onde aparece uma chamada com este nome:**

- `consultar_pedidos` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1668>).

### FiltroEstoquePublicoForm

Linha 755: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:755>).

Classe; herda de: forms.Form.

**Explicacao presente no codigo:**

> Filtros da consulta pública de estoques.
> 
> A situação usa os códigos calculados pelo sistema. Os níveis mínimo e
> crítico continuam ocultos, pois são parâmetros internos do Hemocentro.

**Chamadas utilizadas no corpo:** `forms.CharField`, `forms.ChoiceField`.

**Atributos/campos declarados diretamente:**

```python
tipo_sanguineo = forms.ChoiceField(label='Tipo sanguíneo', required=False, choices=[('', 'Todos')] + [(tipo, tipo) for tipo in TIPOS_SANGUINEOS])
cidade = forms.CharField(label='Cidade', required=False)
hemocentro = forms.CharField(label='Hemocentro', required=False)
situacao = forms.ChoiceField(label='Situação do estoque', required=False, choices=[('', 'Todas'), ('CRITICO', 'Crítico'), ('BAIXO', 'Baixo'), ('ADEQUADO', 'Adequado'), ('ALTO', 'Alto')])
busca = forms.CharField(label='Busca', required=False, help_text='Nome do Hemocentro, cidade, UF ou tipo sanguíneo.')
```

**Onde aparece uma chamada com este nome:**

- `visualizacao_publica_estoque` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1311>).


## accounts/management/__init__.py

Marcador de pacote Python; pode nao executar nenhuma instrucao.

Original: [accounts/management/__init__.py](<C:/Users/lb119/Elo/accounts/management/__init__.py>).


## accounts/management/commands/__init__.py

Marcador de pacote Python; pode nao executar nenhuma instrucao.

Original: [accounts/management/commands/__init__.py](<C:/Users/lb119/Elo/accounts/management/commands/__init__.py>).


## accounts/management/commands/criar_perfis_teste.py

Comando local de contas ficticias preservando registros existentes.

Original: [accounts/management/commands/criar_perfis_teste.py](<C:/Users/lb119/Elo/accounts/management/commands/criar_perfis_teste.py>).

**Dependencias importadas:**

```python
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from accounts.models import ConsentimentoLGPD, Triagem, Usuario
```

### Command

Linha 11: [accounts/management/commands/criar_perfis_teste.py](<C:/Users/lb119/Elo/accounts/management/commands/criar_perfis_teste.py:11>).

Classe; herda de: BaseCommand.

**Atributos/campos declarados diretamente:**

```python
help = 'Cria contas ficticias de cada perfil, sem substituir contas existentes.'
```

### Command.add_arguments

Linha 14: [accounts/management/commands/criar_perfis_teste.py](<C:/Users/lb119/Elo/accounts/management/commands/criar_perfis_teste.py:14>).

```python
def add_arguments(self, parser):
```

**Chamadas utilizadas no corpo:** `parser.add_argument`.

### Command.handle

Linha 18: [accounts/management/commands/criar_perfis_teste.py](<C:/Users/lb119/Elo/accounts/management/commands/criar_perfis_teste.py:18>).

```python
def handle(self, *args, **options):
```

**Decoradores:** `transaction.atomic`.

**Chamadas utilizadas no corpo:** `CommandError`, `ConsentimentoLGPD.objects.create`, `Triagem.objects.create`, `Usuario.objects.create_user`, `Usuario.objects.filter`, `Usuario.objects.filter(email=email).exists`, `len`, `perfis.append`, `self.stdout.write`, `self.style.SUCCESS`, `status.lower`, `timezone.now`.

**Excecoes levantadas:**

- `CommandError('Este comando exige DEBUG=True no ambiente de desenvolvimento.')`
- `CommandError('Use uma senha com pelo menos oito caracteres.')`

**Estrutura de controle:** If: 5, For: 2. Abra o original para seguir as condicoes na ordem.


## accounts/migrations/0001_initial.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0001_initial.py](<C:/Users/lb119/Elo/accounts/migrations/0001_initial.py>).

**Dependencias importadas:**

```python
import accounts.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
```

### Migration

Linha 9: [accounts/migrations/0001_initial.py](<C:/Users/lb119/Elo/accounts/migrations/0001_initial.py:9>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `accounts.models.UsuarioManager`, `migrations.CreateModel`, `models.BigAutoField`, `models.BooleanField`, `models.CharField`, `models.DateField`, `models.DateTimeField`, `models.EmailField`, `models.ForeignKey`, `models.GenericIPAddressField`, `models.ManyToManyField`, `models.UniqueConstraint`.

**Atributos/campos declarados diretamente:**

```python
initial = True
dependencies = [('auth', '0012_alter_user_first_name_max_length')]
operations = [migrations.CreateModel(name='Usuario', fields=[('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')), ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')), ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')), ('id_usuario', models.BigAutoField(primary_key=True, serialize=False)), ('nome', models.CharField(max_length=150)), ('email', models.EmailField(max_length=254, unique=True)), ('password', models.CharField(db_column='senha_hash', max_length=128)), ('cpf', models.CharField(blank=True, max_length=11, null=True, unique=True)), ('cnpj', models.CharField(blank=True, max_length=14, null=True, unique=True)), ('telefone', models.CharField(blank=True, max_length=20)), ('data_nascimento', models.DateField(blank=True, null=True)), ('sexo', models.CharField(blank=True, choices=[('F', 'Feminino'), ('M', 'Masculino'), ('O', 'Outro'), ('N', 'Prefiro nao informar')], max_length=1)), ('cidade', models.CharField(blank=True, max_length=100)), ('estado', models.CharField(blank=True, max_length=2)), ('perfil', models.CharField(choices=[('DOADOR', 'Doador'), ('RECEPTOR', 'Receptor'), ('HEMOCENTRO', 'Hemocentro'), ('OBSERVADOR', 'Observador'), ('ADMINISTRADOR', 'Administrador')], max_length=20)), ('is_active', models.BooleanField(db_column='ativo', default=True)), ('email_verificado', models.BooleanField(default=False)), ('date_joined', models.DateTimeField(auto_now_add=True, db_column='data_cadastro')), ('atualizado_em', models.DateTimeField(auto_now=True)), ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')), ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'))], options={'verbose_name': 'usuario', 'verbose_name_plural': 'usuarios', 'db_table': 'usuarios', 'ordering': ['nome']}, managers=[('objects', accounts.models.UsuarioManager())]), migrations.CreateModel(name='ConsentimentoLGPD', fields=[('id_consentimento', models.BigAutoField(primary_key=True, serialize=False)), ('tipo_termo', models.CharField(choices=[('GERAL', 'Termos gerais e politica de privacidade'), ('TRIAGEM', 'Termo de triagem'), ('NOTIFICACOES', 'Termo de notificacoes')], max_length=20)), ('versao_termo', models.CharField(default='1.0', max_length=20)), ('aceito', models.BooleanField(default=False)), ('data_aceite', models.DateTimeField(auto_now_add=True)), ('ip', models.GenericIPAddressField(blank=True, null=True)), ('revogado_em', models.DateTimeField(blank=True, null=True)), ('usuario', models.ForeignKey(db_column='id_usuario', on_delete=django.db.models.deletion.CASCADE, related_name='consentimentos_lgpd', to=settings.AUTH_USER_MODEL))], options={'verbose_name': 'consentimento LGPD', 'verbose_name_plural': 'consentimentos LGPD', 'db_table': 'consentimentos_lgpd', 'ordering': ['-data_aceite'], 'constraints': [models.UniqueConstraint(fields=('usuario', 'tipo_termo', 'versao_termo'), name='consentimento_unico_por_versao')]})]
```


## accounts/migrations/0002_remove_usuario_cidade_remove_usuario_cnpj_and_more.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0002_remove_usuario_cidade_remove_usuario_cnpj_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0002_remove_usuario_cidade_remove_usuario_cnpj_and_more.py>).

**Dependencias importadas:**

```python
from django.db import migrations, models
```

### Migration

Linha 6: [accounts/migrations/0002_remove_usuario_cidade_remove_usuario_cnpj_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0002_remove_usuario_cidade_remove_usuario_cnpj_and_more.py:6>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `migrations.AlterField`, `migrations.RemoveField`, `models.CharField`.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0001_initial')]
operations = [migrations.RemoveField(model_name='usuario', name='cidade'), migrations.RemoveField(model_name='usuario', name='cnpj'), migrations.RemoveField(model_name='usuario', name='cpf'), migrations.RemoveField(model_name='usuario', name='data_nascimento'), migrations.RemoveField(model_name='usuario', name='estado'), migrations.RemoveField(model_name='usuario', name='perfil'), migrations.RemoveField(model_name='usuario', name='sexo'), migrations.RemoveField(model_name='usuario', name='telefone'), migrations.AlterField(model_name='consentimentolgpd', name='tipo_termo', field=models.CharField(choices=[('GERAL', 'Termos gerais e politica de privacidade')], default='GERAL', max_length=20))]
```


## accounts/migrations/0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more.py>).

**Dependencias importadas:**

```python
from django.db import migrations, models
```

### Migration

Linha 6: [accounts/migrations/0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more.py:6>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `migrations.AddField`, `migrations.AlterField`, `models.CharField`, `models.DateField`.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0002_remove_usuario_cidade_remove_usuario_cnpj_and_more')]
operations = [migrations.AddField(model_name='usuario', name='cidade', field=models.CharField(blank=True, default='', max_length=100)), migrations.AddField(model_name='usuario', name='cnpj', field=models.CharField(blank=True, max_length=14, null=True, unique=True)), migrations.AddField(model_name='usuario', name='cpf', field=models.CharField(blank=True, max_length=11, null=True, unique=True)), migrations.AddField(model_name='usuario', name='data_nascimento', field=models.DateField(blank=True, null=True)), migrations.AddField(model_name='usuario', name='estado', field=models.CharField(blank=True, default='', max_length=2)), migrations.AddField(model_name='usuario', name='perfil', field=models.CharField(choices=[('DOADOR', 'Doador'), ('RECEPTOR', 'Receptor'), ('HEMOCENTRO', 'Hemocentro'), ('OBSERVADOR', 'Observador'), ('ADMINISTRADOR', 'Administrador')], default='OBSERVADOR', max_length=20)), migrations.AddField(model_name='usuario', name='sexo', field=models.CharField(blank=True, choices=[('F', 'Feminino'), ('M', 'Masculino'), ('O', 'Outro'), ('N', 'Prefiro nao informar')], default='', max_length=1)), migrations.AddField(model_name='usuario', name='telefone', field=models.CharField(blank=True, default='', max_length=20)), migrations.AlterField(model_name='consentimentolgpd', name='tipo_termo', field=models.CharField(choices=[('GERAL', 'Termos gerais e politica de privacidade'), ('TRIAGEM', 'Termo de triagem'), ('NOTIFICACOES', 'Termo de notificacoes')], default='GERAL', max_length=20))]
```


## accounts/migrations/0004_auditoriaacaocritica.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0004_auditoriaacaocritica.py](<C:/Users/lb119/Elo/accounts/migrations/0004_auditoriaacaocritica.py>).

**Dependencias importadas:**

```python
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
```

### Migration

Linha 8: [accounts/migrations/0004_auditoriaacaocritica.py](<C:/Users/lb119/Elo/accounts/migrations/0004_auditoriaacaocritica.py:8>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `migrations.CreateModel`, `models.BigAutoField`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.GenericIPAddressField`, `models.Index`, `models.JSONField`, `models.TextField`.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more')]
operations = [migrations.CreateModel(name='AuditoriaAcaoCritica', fields=[('id_auditoria', models.BigAutoField(primary_key=True, serialize=False)), ('acao', models.CharField(choices=[('LOGIN_FALHO', 'Login falho'), ('LOGIN_SUSPEITO', 'Login suspeito'), ('ALTERACAO_PERMISSAO', 'Alteracao de permissao'), ('APROVACAO_HEMOCENTRO', 'Aprovacao de hemocentro'), ('ATUALIZACAO_ESTOQUE', 'Atualizacao de estoque'), ('MODERACAO', 'Moderacao'), ('ACESSO_DADOS_SENSIVEIS', 'Acesso a dados sensiveis'), ('CONFIRMACAO_DOACAO', 'Confirmacao de doacao')], max_length=40)), ('resultado', models.CharField(choices=[('SUCESSO', 'Sucesso'), ('FALHA', 'Falha'), ('BLOQUEADO', 'Bloqueado')], default='SUCESSO', max_length=20)), ('alvo_tipo', models.CharField(blank=True, default='', max_length=80)), ('alvo_id', models.CharField(blank=True, default='', max_length=80)), ('descricao', models.CharField(blank=True, default='', max_length=255)), ('ip', models.GenericIPAddressField(blank=True, null=True)), ('user_agent', models.TextField(blank=True, default='')), ('metadados', models.JSONField(blank=True, default=dict)), ('criado_em', models.DateTimeField(auto_now_add=True)), ('usuario', models.ForeignKey(blank=True, db_column='id_usuario', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auditorias_acoes_criticas', to=settings.AUTH_USER_MODEL))], options={'verbose_name': 'auditoria de acao critica', 'verbose_name_plural': 'auditorias de acoes criticas', 'db_table': 'auditorias_acoes_criticas', 'ordering': ['-criado_em'], 'indexes': [models.Index(fields=['acao', 'criado_em'], name='auditoria_acao_data_idx'), models.Index(fields=['usuario', 'criado_em'], name='auditoria_usuario_data_idx'), models.Index(fields=['ip', 'criado_em'], name='auditoria_ip_data_idx')]})]
```


## accounts/migrations/0005_usuario_status_validacao_validacaohemocentro.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0005_usuario_status_validacao_validacaohemocentro.py](<C:/Users/lb119/Elo/accounts/migrations/0005_usuario_status_validacao_validacaohemocentro.py>).

**Dependencias importadas:**

```python
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
```

### Migration

Linha 8: [accounts/migrations/0005_usuario_status_validacao_validacaohemocentro.py](<C:/Users/lb119/Elo/accounts/migrations/0005_usuario_status_validacao_validacaohemocentro.py:8>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `migrations.AddField`, `migrations.CreateModel`, `models.BigAutoField`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.Index`, `models.TextField`.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0004_auditoriaacaocritica')]
operations = [migrations.AddField(model_name='usuario', name='status_validacao', field=models.CharField(choices=[('PENDENTE', 'Pendente'), ('APROVADO', 'Aprovado'), ('RECUSADO', 'Recusado'), ('CORRECAO', 'Correcao necessaria')], default='PENDENTE', max_length=20)), migrations.CreateModel(name='ValidacaoHemocentro', fields=[('id_validacao', models.BigAutoField(primary_key=True, serialize=False)), ('status', models.CharField(choices=[('PENDENTE', 'Pendente'), ('APROVADO', 'Aprovado'), ('RECUSADO', 'Recusado'), ('CORRECAO', 'Correcao necessaria')], max_length=20)), ('parecer', models.TextField(blank=True, default='')), ('data_analise', models.DateTimeField(auto_now_add=True)), ('admin', models.ForeignKey(blank=True, db_column='id_admin', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='validacoes_hemocentro_realizadas', to=settings.AUTH_USER_MODEL)), ('hemocentro', models.ForeignKey(db_column='id_hemocentro', on_delete=django.db.models.deletion.CASCADE, related_name='validacoes_hemocentro', to=settings.AUTH_USER_MODEL))], options={'verbose_name': 'validacao de hemocentro', 'verbose_name_plural': 'validacoes de hemocentros', 'db_table': 'validacoes_hemocentro', 'ordering': ['-data_analise'], 'indexes': [models.Index(fields=['hemocentro', '-data_analise'], name='validacao_hemo_data_idx'), models.Index(fields=['status', 'data_analise'], name='validacao_hemo_status_idx')]})]
```


## accounts/migrations/0006_triagem_respostatriagem_and_more.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0006_triagem_respostatriagem_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0006_triagem_respostatriagem_and_more.py>).

**Dependencias importadas:**

```python
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
```

### Migration

Linha 8: [accounts/migrations/0006_triagem_respostatriagem_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0006_triagem_respostatriagem_and_more.py:8>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `migrations.AddIndex`, `migrations.CreateModel`, `models.BigAutoField`, `models.CharField`, `models.DateField`, `models.DateTimeField`, `models.ForeignKey`, `models.Index`, `models.JSONField`, `models.TextField`.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0005_usuario_status_validacao_validacaohemocentro')]
operations = [migrations.CreateModel(name='Triagem', fields=[('id_triagem', models.BigAutoField(primary_key=True, serialize=False)), ('modalidade', models.CharField(choices=[('EXTENSA', 'Triagem extensa'), ('SIMPLIFICADA', 'Triagem simplificada')], default='EXTENSA', max_length=20)), ('regra_version', models.CharField(default='HEMOMINAS_2026_08', max_length=40)), ('resultado', models.CharField(choices=[('SEM_IMPEDIMENTO_IDENTIFICADO', 'Sem impedimento identificado'), ('INAPTIDAO_TEMPORARIA', 'Inaptidão temporária'), ('INAPTIDAO_DEFINITIVA', 'Inaptidão definitiva'), ('AVALIACAO_PRESENCIAL', 'Avaliação presencial'), ('DOCUMENTACAO_ESPECIAL', 'Documentação especial')], max_length=30)), ('mensagem_resultado', models.TextField()), ('data_liberacao', models.DateField(blank=True, null=True)), ('achados', models.JSONField(blank=True, default=list)), ('iniciada_em', models.DateTimeField(auto_now_add=True)), ('finalizada_em', models.DateTimeField(blank=True, null=True)), ('usuario', models.ForeignKey(db_column='id_usuario', on_delete=django.db.models.deletion.CASCADE, related_name='triagens', to=settings.AUTH_USER_MODEL))], options={'db_table': 'triagens', 'ordering': ['-iniciada_em']}), migrations.CreateModel(name='RespostaTriagem', fields=[('id_resposta', models.BigAutoField(primary_key=True, serialize=False)), ('id_pergunta', models.CharField(max_length=20)), ('codigo_resposta', models.CharField(max_length=80)), ('resposta_label', models.CharField(max_length=255)), ('data_evento', models.DateField(blank=True, db_column='event_date', null=True)), ('metadata', models.JSONField(blank=True, default=dict)), ('rule_version', models.CharField(default='HEMOMINAS_2026_08', max_length=40)), ('source_ref', models.CharField(blank=True, default='', max_length=255)), ('respondido_em', models.DateTimeField(auto_now_add=True)), ('triagem', models.ForeignKey(db_column='id_triagem', on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='accounts.triagem'))], options={'db_table': 'respostas_triagem', 'ordering': ['id_resposta']}), migrations.AddIndex(model_name='triagem', index=models.Index(fields=['usuario', '-iniciada_em'], name='triagem_usuario_data_idx')), migrations.AddIndex(model_name='triagem', index=models.Index(fields=['resultado', '-iniciada_em'], name='triagem_resultado_data_idx')), migrations.AddIndex(model_name='respostatriagem', index=models.Index(fields=['triagem', 'id_pergunta'], name='resposta_triagem_pergunta_idx'))]
```


## accounts/migrations/0007_alter_auditoriaacaocritica_acao_estoque_and_more.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0007_alter_auditoriaacaocritica_acao_estoque_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0007_alter_auditoriaacaocritica_acao_estoque_and_more.py>).

**Dependencias importadas:**

```python
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
```

### Migration

Linha 8: [accounts/migrations/0007_alter_auditoriaacaocritica_acao_estoque_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0007_alter_auditoriaacaocritica_acao_estoque_and_more.py:8>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `migrations.AddConstraint`, `migrations.AddIndex`, `migrations.AlterField`, `migrations.CreateModel`, `models.BigAutoField`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.Index`, `models.IntegerField`, `models.PositiveIntegerField`, `models.UniqueConstraint`.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0006_triagem_respostatriagem_and_more')]
operations = [migrations.AlterField(model_name='auditoriaacaocritica', name='acao', field=models.CharField(choices=[('LOGIN_FALHO', 'Login falho'), ('LOGIN_SUSPEITO', 'Login suspeito'), ('ALTERACAO_PERMISSAO', 'Alteracao de permissao'), ('APROVACAO_HEMOCENTRO', 'Aprovacao de hemocentro'), ('CADASTRO_ESTOQUE', 'Cadastro de estoque'), ('ATUALIZACAO_ESTOQUE', 'Atualizacao de estoque'), ('MODERACAO', 'Moderacao'), ('ACESSO_DADOS_SENSIVEIS', 'Acesso a dados sensiveis'), ('CONFIRMACAO_DOACAO', 'Confirmacao de doacao')], max_length=40)), migrations.CreateModel(name='Estoque', fields=[('id_estoque', models.BigAutoField(primary_key=True, serialize=False)), ('tipo_sanguineo', models.CharField(choices=[('O-', 'O-'), ('O+', 'O+'), ('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('AB-', 'AB-'), ('AB+', 'AB+')], max_length=3)), ('quantidade_bolsas', models.PositiveIntegerField(default=0)), ('nivel_minimo', models.PositiveIntegerField()), ('nivel_critico', models.PositiveIntegerField()), ('status_calculado', models.CharField(choices=[('CRITICO', 'Crítico'), ('BAIXO', 'Baixo'), ('ESTAVEL', 'Estável')], default='ESTAVEL', max_length=10)), ('data_atualizacao', models.DateTimeField(auto_now=True)), ('hemocentro', models.ForeignKey(db_column='id_hemocentro', limit_choices_to={'perfil': 'HEMOCENTRO'}, on_delete=django.db.models.deletion.CASCADE, related_name='estoques', to=settings.AUTH_USER_MODEL))], options={'verbose_name': 'estoque', 'verbose_name_plural': 'estoques', 'db_table': 'estoques', 'ordering': ['hemocentro__nome', 'tipo_sanguineo']}), migrations.CreateModel(name='EstoqueMovimentacao', fields=[('id_mov', models.BigAutoField(primary_key=True, serialize=False)), ('tipo_movimento', models.CharField(choices=[('ENTRADA', 'Entrada'), ('SAIDA', 'Saída'), ('AJUSTE', 'Ajuste')], max_length=10)), ('quantidade_anterior', models.PositiveIntegerField()), ('quantidade_movimentada', models.IntegerField()), ('quantidade_nova', models.PositiveIntegerField()), ('motivo', models.CharField(blank=True, default='', max_length=255)), ('data_hora', models.DateTimeField(auto_now_add=True)), ('estoque', models.ForeignKey(db_column='id_estoque', on_delete=django.db.models.deletion.CASCADE, related_name='movimentacoes', to='accounts.estoque')), ('usuario_resp', models.ForeignKey(blank=True, db_column='id_usuario_resp', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movimentacoes_estoque_realizadas', to=settings.AUTH_USER_MODEL))], options={'verbose_name': 'movimentacao de estoque', 'verbose_name_plural': 'movimentacoes de estoque', 'db_table': 'movimentacoes_estoque', 'ordering': ['-data_hora']}), migrations.AddIndex(model_name='estoque', index=models.Index(fields=['hemocentro', 'tipo_sanguineo'], name='estoque_hemo_tipo_idx')), migrations.AddIndex(model_name='estoque', index=models.Index(fields=['status_calculado'], name='estoque_status_idx')), migrations.AddConstraint(model_name='estoque', constraint=models.UniqueConstraint(fields=('hemocentro', 'tipo_sanguineo'), name='estoque_unico_por_hemocentro_tipo')), migrations.AddIndex(model_name='estoquemovimentacao', index=models.Index(fields=['estoque', '-data_hora'], name='mov_estoque_data_idx')), migrations.AddIndex(model_name='estoquemovimentacao', index=models.Index(fields=['usuario_resp', '-data_hora'], name='mov_usuario_data_idx'))]
```


## accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py>).

**Dependencias importadas:**

```python
import django.db.models.deletion
from django.db import migrations, models
```

### preencher_dados_da_triagem

Linha 7: [accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py:7>).

```python
def preencher_dados_da_triagem(apps, schema_editor):
```

**Explicacao presente no codigo:**

> Converte os registros da versão inicial para os campos novos.

**Chamadas utilizadas no corpo:** `RespostaTriagem.objects.all`, `RespostaTriagem.objects.all().iterator`, `Triagem.objects.filter`, `Triagem.objects.filter(finalizada_em__isnull=False).update`, `apps.get_model`, `resposta.data_evento.isoformat`, `resposta.metadata.get`, `resposta.save`.

**Estrutura de controle:** For: 1. Abra o original para seguir as condicoes na ordem.

### limpar_dados_da_triagem

Linha 37: [accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py:37>).

```python
def limpar_dados_da_triagem(apps, schema_editor):
```

**Explicacao presente no codigo:**

> Permite reverter a migration sem alterar os campos legados.

**Chamadas utilizadas no corpo:** `RespostaTriagem.objects.update`, `Triagem.objects.update`, `apps.get_model`.

### Migration

Linha 47: [accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py:47>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `migrations.AddConstraint`, `migrations.AddField`, `migrations.AlterField`, `migrations.AlterModelOptions`, `migrations.RunPython`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.JSONField`, `models.PositiveIntegerField`, `models.TextField`, `models.UniqueConstraint`.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0006_triagem_respostatriagem_and_more')]
operations = [migrations.AlterModelOptions(name='respostatriagem', options={'ordering': ['id_resposta'], 'verbose_name': 'Resposta triagem', 'verbose_name_plural': 'Respostas triagem'}), migrations.AlterModelOptions(name='triagem', options={'ordering': ['-iniciada_em'], 'verbose_name': 'Triagem', 'verbose_name_plural': 'Triagens'}), migrations.AddField(model_name='respostatriagem', name='valor', field=models.JSONField(blank=True, default=dict)), migrations.AddField(model_name='triagem', name='atualizada_em', field=models.DateTimeField(auto_now=True)), migrations.AddField(model_name='triagem', name='fluxo_perguntas', field=models.JSONField(blank=True, default=list)), migrations.AddField(model_name='triagem', name='pergunta_atual', field=models.PositiveIntegerField(default=0)), migrations.AddField(model_name='triagem', name='status', field=models.CharField(choices=[('EM_ANDAMENTO', 'Em andamento'), ('CONCLUIDA', 'Concluída'), ('CANCELADA', 'Cancelada')], default='EM_ANDAMENTO', max_length=20)), migrations.AddField(model_name='triagem', name='triagem_base', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verificacoes_simplificadas', to='accounts.triagem')), migrations.RunPython(preencher_dados_da_triagem, limpar_dados_da_triagem), migrations.AlterField(model_name='triagem', name='mensagem_resultado', field=models.TextField(blank=True, default='')), migrations.AlterField(model_name='triagem', name='resultado', field=models.CharField(blank=True, choices=[('SEM_IMPEDIMENTO_IDENTIFICADO', 'Sem impedimento identificado'), ('INAPTIDAO_TEMPORARIA', 'Inaptidão temporária'), ('INAPTIDAO_DEFINITIVA', 'Inaptidão definitiva'), ('AVALIACAO_PRESENCIAL', 'Avaliação presencial'), ('DOCUMENTACAO_ESPECIAL', 'Documentação especial')], default='', max_length=30)), migrations.AddConstraint(model_name='respostatriagem', constraint=models.UniqueConstraint(fields=('triagem', 'id_pergunta'), name='resposta_unica_por_pergunta'))]
```


## accounts/migrations/0008_merge_triagem_estoque_branches.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0008_merge_triagem_estoque_branches.py](<C:/Users/lb119/Elo/accounts/migrations/0008_merge_triagem_estoque_branches.py>).

**Dependencias importadas:**

```python
from django.db import migrations
```

### Migration

Linha 6: [accounts/migrations/0008_merge_triagem_estoque_branches.py](<C:/Users/lb119/Elo/accounts/migrations/0008_merge_triagem_estoque_branches.py:6>).

Classe; herda de: migrations.Migration.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0007_alter_auditoriaacaocritica_acao_estoque_and_more'), ('accounts', '0007_alter_respostatriagem_options_alter_triagem_options_and_more')]
operations = []
```


## accounts/migrations/0009_usuario_tipo_sanguineo_notificacao.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0009_usuario_tipo_sanguineo_notificacao.py](<C:/Users/lb119/Elo/accounts/migrations/0009_usuario_tipo_sanguineo_notificacao.py>).

**Dependencias importadas:**

```python
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
```

### Migration

Linha 8: [accounts/migrations/0009_usuario_tipo_sanguineo_notificacao.py](<C:/Users/lb119/Elo/accounts/migrations/0009_usuario_tipo_sanguineo_notificacao.py:8>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `migrations.AddField`, `migrations.CreateModel`, `models.BigAutoField`, `models.BooleanField`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.Index`, `models.TextField`.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0008_merge_triagem_estoque_branches')]
operations = [migrations.AddField(model_name='usuario', name='tipo_sanguineo', field=models.CharField(blank=True, choices=[('O-', 'O-'), ('O+', 'O+'), ('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('AB-', 'AB-'), ('AB+', 'AB+')], default='', max_length=3)), migrations.CreateModel(name='Notificacao', fields=[('id_notificacao', models.BigAutoField(primary_key=True, serialize=False)), ('tipo', models.CharField(choices=[('ESTOQUE_BAIXO', 'Estoque baixo'), ('ESTOQUE_CRITICO', 'Estoque crítico'), ('GERAL', 'Aviso geral')], default='GERAL', max_length=30)), ('titulo', models.CharField(max_length=120)), ('mensagem', models.TextField()), ('url_destino', models.CharField(blank=True, default='', max_length=255)), ('lida', models.BooleanField(default=False)), ('criada_em', models.DateTimeField(auto_now_add=True)), ('lida_em', models.DateTimeField(blank=True, null=True)), ('estoque', models.ForeignKey(blank=True, db_column='id_estoque', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notificacoes', to='accounts.estoque')), ('usuario', models.ForeignKey(db_column='id_usuario', on_delete=django.db.models.deletion.CASCADE, related_name='notificacoes', to=settings.AUTH_USER_MODEL))], options={'verbose_name': 'notificacao', 'verbose_name_plural': 'notificacoes', 'db_table': 'notificacoes', 'ordering': ['-criada_em'], 'indexes': [models.Index(fields=['usuario', 'lida', '-criada_em'], name='notificacao_usuario_lida_idx'), models.Index(fields=['tipo', '-criada_em'], name='notificacao_tipo_data_idx')]})]
```


## accounts/migrations/0010_pedidosangue.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0010_pedidosangue.py](<C:/Users/lb119/Elo/accounts/migrations/0010_pedidosangue.py>).

**Dependencias importadas:**

```python
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
```

### Migration

Linha 8: [accounts/migrations/0010_pedidosangue.py](<C:/Users/lb119/Elo/accounts/migrations/0010_pedidosangue.py:8>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `migrations.CreateModel`, `models.BigAutoField`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.Index`, `models.TextField`.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0009_usuario_tipo_sanguineo_notificacao')]
operations = [migrations.CreateModel(name='PedidoSangue', fields=[('id_pedido', models.BigAutoField(primary_key=True, serialize=False)), ('para_quem', models.CharField(choices=[('MIM', 'Para mim'), ('OUTRA_PESSOA', 'Para outra pessoa')], max_length=20)), ('tipo_sanguineo', models.CharField(choices=[('O-', 'O-'), ('O+', 'O+'), ('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('AB-', 'AB-'), ('AB+', 'AB+')], max_length=3)), ('cidade', models.CharField(max_length=100)), ('urgencia', models.CharField(choices=[('NORMAL', 'Normal'), ('URGENTE', 'Urgente'), ('CRITICO', 'Crítico')], max_length=10)), ('nome_paciente', models.CharField(blank=True, default='', max_length=150)), ('descricao', models.TextField(max_length=500)), ('status', models.CharField(choices=[('PENDENTE', 'Pendente'), ('ATIVO', 'Ativo'), ('RECUSADO', 'Recusado'), ('ATENDIDO', 'Atendido'), ('EXPIRADO', 'Expirado')], default='PENDENTE', max_length=10)), ('data_criacao', models.DateTimeField(auto_now_add=True)), ('data_fechamento', models.DateTimeField(blank=True, null=True)), ('hemocentro', models.ForeignKey(db_column='id_hemocentro', limit_choices_to={'perfil': 'HEMOCENTRO'}, on_delete=django.db.models.deletion.PROTECT, related_name='pedidos_de_destino', to=settings.AUTH_USER_MODEL)), ('solicitante', models.ForeignKey(db_column='id_solicitante', on_delete=django.db.models.deletion.PROTECT, related_name='pedidos_publicados', to=settings.AUTH_USER_MODEL))], options={'verbose_name': 'pedido de sangue', 'verbose_name_plural': 'pedidos de sangue', 'db_table': 'pedidos_sangue', 'ordering': ['-data_criacao'], 'indexes': [models.Index(fields=['status', '-data_criacao'], name='pedido_sangue_status_idx'), models.Index(fields=['cidade', 'tipo_sanguineo'], name='pedido_sangue_busca_idx')]})]
```


## accounts/migrations/0011_alinhar_pedidos_validacao.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0011_alinhar_pedidos_validacao.py](<C:/Users/lb119/Elo/accounts/migrations/0011_alinhar_pedidos_validacao.py>).

**Dependencias importadas:**

```python
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models
```

### converter_valores_legados

Linha 7: [accounts/migrations/0011_alinhar_pedidos_validacao.py](<C:/Users/lb119/Elo/accounts/migrations/0011_alinhar_pedidos_validacao.py:7>).

```python
def converter_valores_legados(apps, schema_editor):
```

**Chamadas utilizadas no corpo:** `PedidoSangue.objects.filter`, `PedidoSangue.objects.filter(status=valor_antigo).update`, `PedidoSangue.objects.filter(urgencia=valor_antigo).update`, `apps.get_model`, `conversoes_status.items`, `conversoes_urgencia.items`.

**Estrutura de controle:** For: 2. Abra o original para seguir as condicoes na ordem.

### Migration

Linha 32: [accounts/migrations/0011_alinhar_pedidos_validacao.py](<C:/Users/lb119/Elo/accounts/migrations/0011_alinhar_pedidos_validacao.py:32>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `migrations.AddField`, `migrations.AddIndex`, `migrations.AlterField`, `migrations.CreateModel`, `migrations.RemoveIndex`, `migrations.RenameField`, `migrations.RunPython`, `models.BigAutoField`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.Index`, `models.TextField`.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0010_pedidosangue')]
operations = [migrations.RenameField(model_name='pedidosangue', old_name='hemocentro', new_name='hemocentro_destino'), migrations.AlterField(model_name='pedidosangue', name='hemocentro_destino', field=models.ForeignKey(db_column='id_hemocentro_destino', limit_choices_to={'perfil': 'HEMOCENTRO'}, on_delete=django.db.models.deletion.PROTECT, related_name='pedidos_recebidos', to=settings.AUTH_USER_MODEL)), migrations.AddField(model_name='pedidosangue', name='titulo', field=models.CharField(default='Pedido de sangue', max_length=150)), migrations.AddField(model_name='pedidosangue', name='justificativa_urgencia', field=models.TextField(blank=True, default='')), migrations.AddField(model_name='pedidosangue', name='atualizado_em', field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now), preserve_default=False), migrations.AlterField(model_name='pedidosangue', name='descricao', field=models.TextField()), migrations.AlterField(model_name='pedidosangue', name='solicitante', field=models.ForeignKey(db_column='id_solicitante', on_delete=django.db.models.deletion.CASCADE, related_name='pedidos_sangue', to=settings.AUTH_USER_MODEL)), migrations.AlterField(model_name='pedidosangue', name='urgencia', field=models.CharField(choices=[('BAIXA', 'Baixa'), ('MEDIA', 'Media'), ('ALTA', 'Alta'), ('CRITICA', 'Critica')], max_length=10)), migrations.AlterField(model_name='pedidosangue', name='status', field=models.CharField(choices=[('PENDENTE_VALIDACAO', 'Pendente de validacao'), ('ATIVO', 'Ativo'), ('SUSPEITO', 'Suspeito'), ('RECUSADO', 'Recusado'), ('ENCERRADO', 'Encerrado')], default='PENDENTE_VALIDACAO', max_length=30)), migrations.RunPython(converter_valores_legados, migrations.RunPython.noop), migrations.RemoveIndex(model_name='pedidosangue', name='pedido_sangue_status_idx'), migrations.RemoveIndex(model_name='pedidosangue', name='pedido_sangue_busca_idx'), migrations.AddIndex(model_name='pedidosangue', index=models.Index(fields=['status', '-data_criacao'], name='pedido_status_data_idx')), migrations.AddIndex(model_name='pedidosangue', index=models.Index(fields=['tipo_sanguineo', 'urgencia'], name='pedido_tipo_urg_idx')), migrations.AddIndex(model_name='pedidosangue', index=models.Index(fields=['cidade'], name='pedido_cidade_idx')), migrations.CreateModel(name='ValidacaoPedido', fields=[('id_validacao', models.BigAutoField(primary_key=True, serialize=False)), ('status_validacao', models.CharField(choices=[('APROVADO', 'Aprovado'), ('SUSPEITO', 'Suspeito'), ('RECUSADO', 'Recusado')], max_length=20)), ('motivo', models.TextField(blank=True, default='')), ('data_validacao', models.DateTimeField(auto_now_add=True)), ('moderador', models.ForeignKey(blank=True, db_column='id_moderador', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='validacoes_pedido_realizadas', to=settings.AUTH_USER_MODEL)), ('pedido', models.ForeignKey(db_column='id_pedido', on_delete=django.db.models.deletion.CASCADE, related_name='validacoes', to='accounts.pedidosangue'))], options={'db_table': 'validacoes_pedido', 'ordering': ['-data_validacao']})]
```


## accounts/migrations/0012_pedidosangue_contato_and_more.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0012_pedidosangue_contato_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0012_pedidosangue_contato_and_more.py>).

**Dependencias importadas:**

```python
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
```

### alinhar_status_legados

Linha 8: [accounts/migrations/0012_pedidosangue_contato_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0012_pedidosangue_contato_and_more.py:8>).

```python
def alinhar_status_legados(apps, schema_editor):
```

**Chamadas utilizadas no corpo:** `PedidoSangue.objects.filter`, `PedidoSangue.objects.filter(status='ATIVO').update`, `PedidoSangue.objects.filter(status='ENCERRADO').update`, `PedidoSangue.objects.filter(status='PENDENTE_VALIDACAO').update`, `PedidoSangue.objects.filter(status='RECUSADO').update`, `PedidoSangue.objects.filter(status='SUSPEITO').update`, `apps.get_model`.

### Migration

Linha 22: [accounts/migrations/0012_pedidosangue_contato_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0012_pedidosangue_contato_and_more.py:22>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `migrations.AddField`, `migrations.AlterField`, `migrations.RunPython`, `models.BooleanField`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.TextField`.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0011_alinhar_pedidos_validacao')]
operations = [migrations.RunPython(alinhar_status_legados, migrations.RunPython.noop), migrations.AddField(model_name='pedidosangue', name='contato', field=models.CharField(default='', max_length=120)), migrations.AddField(model_name='pedidosangue', name='duplicidade_suspeita', field=models.BooleanField(default=False)), migrations.AddField(model_name='pedidosangue', name='informacoes_complementares', field=models.TextField(blank=True, default='')), migrations.AddField(model_name='pedidosangue', name='nome_solicitante', field=models.CharField(default='', max_length=150)), migrations.AddField(model_name='pedidosangue', name='publicado_em', field=models.DateTimeField(blank=True, null=True)), migrations.AddField(model_name='pedidosangue', name='publicado_por', field=models.ForeignKey(blank=True, db_column='id_publicado_por', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pedidos_publicados', to=settings.AUTH_USER_MODEL)), migrations.AddField(model_name='usuario', name='tipo_sanguineo_confirmado', field=models.BooleanField(default=False)), migrations.AlterField(model_name='pedidosangue', name='solicitante', field=models.ForeignKey(blank=True, db_column='id_solicitante', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pedidos_sangue', to=settings.AUTH_USER_MODEL)), migrations.AlterField(model_name='pedidosangue', name='status', field=models.CharField(choices=[('ENVIADA', 'Enviada'), ('EM_ANALISE', 'Em análise'), ('PUBLICADA', 'Publicada'), ('CORRECAO_SOLICITADA', 'Correção solicitada'), ('RECUSADA', 'Recusada'), ('ENCERRADA', 'Encerrada')], default='ENVIADA', max_length=30)), migrations.AlterField(model_name='triagem', name='resultado', field=models.CharField(blank=True, choices=[('SEM_IMPEDIMENTO_IDENTIFICADO', 'Apto'), ('INAPTIDAO_TEMPORARIA', 'Inaptidão temporária'), ('INAPTIDAO_DEFINITIVA', 'Inaptidão definitiva'), ('AVALIACAO_PRESENCIAL', 'Avaliação presencial necessária'), ('DOCUMENTACAO_ESPECIAL', 'Documentação especial')], default='', max_length=40)), migrations.AlterField(model_name='validacaopedido', name='status_validacao', field=models.CharField(choices=[('APROVADO', 'Aprovado'), ('CORRECAO_SOLICITADA', 'Correção solicitada'), ('SUSPEITO', 'Suspeito'), ('RECUSADO', 'Recusado')], max_length=20))]
```


## accounts/migrations/0013_usuario_suspensa.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0013_usuario_suspensa.py](<C:/Users/lb119/Elo/accounts/migrations/0013_usuario_suspensa.py>).

**Dependencias importadas:**

```python
from django.db import migrations, models
```

### Migration

Linha 6: [accounts/migrations/0013_usuario_suspensa.py](<C:/Users/lb119/Elo/accounts/migrations/0013_usuario_suspensa.py:6>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `migrations.AddField`, `models.BooleanField`.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0012_pedidosangue_contato_and_more')]
operations = [migrations.AddField(model_name='usuario', name='suspensa', field=models.BooleanField(default=False))]
```


## accounts/migrations/0014_notificacao_pedido_and_more.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0014_notificacao_pedido_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0014_notificacao_pedido_and_more.py>).

**Dependencias importadas:**

```python
import django.db.models.deletion
from django.db import migrations, models
```

### Migration

Linha 7: [accounts/migrations/0014_notificacao_pedido_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0014_notificacao_pedido_and_more.py:7>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `migrations.AddField`, `migrations.AlterField`, `models.BooleanField`, `models.CharField`, `models.ForeignKey`.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0013_usuario_suspensa')]
operations = [migrations.AddField(model_name='notificacao', name='pedido', field=models.ForeignKey(blank=True, db_column='id_pedido', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notificacoes', to='accounts.pedidosangue')), migrations.AddField(model_name='usuario', name='aceita_notificacoes_pedidos', field=models.BooleanField(default=True)), migrations.AlterField(model_name='notificacao', name='tipo', field=models.CharField(choices=[('ESTOQUE_BAIXO', 'Estoque baixo'), ('ESTOQUE_CRITICO', 'Estoque crítico'), ('PEDIDO_COMPATIVEL', 'Pedido compatível'), ('GERAL', 'Aviso geral')], default='GERAL', max_length=30))]
```


## accounts/migrations/0015_pedido_contato_email.py

Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.

Original: [accounts/migrations/0015_pedido_contato_email.py](<C:/Users/lb119/Elo/accounts/migrations/0015_pedido_contato_email.py>).

**Dependencias importadas:**

```python
from django.db import migrations, models
```

### Migration

Linha 6: [accounts/migrations/0015_pedido_contato_email.py](<C:/Users/lb119/Elo/accounts/migrations/0015_pedido_contato_email.py:6>).

Classe; herda de: migrations.Migration.

**Chamadas utilizadas no corpo:** `migrations.AlterField`, `models.EmailField`.

**Atributos/campos declarados diretamente:**

```python
dependencies = [('accounts', '0014_notificacao_pedido_and_more')]
operations = [migrations.AlterField(model_name='pedidosangue', name='contato', field=models.EmailField(default='', max_length=120))]
```


## accounts/migrations/README.md

Documento/configuracao complementar; consulte o conteudo integral.

Original: [accounts/migrations/README.md](<C:/Users/lb119/Elo/accounts/migrations/README.md>).


## accounts/migrations/__init__.py

Marcador de pacote Python; pode nao executar nenhuma instrucao.

Original: [accounts/migrations/__init__.py](<C:/Users/lb119/Elo/accounts/migrations/__init__.py>).


## accounts/models.py

Entidades persistidas, relacionamentos, estados e integridade do banco.

Original: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py>).

**Dependencias importadas:**

```python
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from .compatibilidade import TIPOS_SANGUINEOS
```

### UsuarioManager

Linha 37: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:37>).

Classe; herda de: BaseUserManager.

**Explicacao presente no codigo:**

> Centraliza a criacao das contas.
> 
> O Django normalmente cria usuarios por username. O Elo usa e-mail, entao
> este manager ensina ``Usuario.objects`` a receber, padronizar e salvar o
> e-mail corretamente tanto para contas comuns quanto para administradores.

**Atributos/campos declarados diretamente:**

```python
use_in_migrations = True
```

### UsuarioManager.create_user

Linha 48: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:48>).

```python
def create_user(self, email, password=None, **extra_fields):
```

**Explicacao presente no codigo:**

> Cria uma conta comum e grava a senha de forma segura.

**Chamadas utilizadas no corpo:** `ValueError`, `self.model`, `self.normalize_email`, `self.normalize_email(email).lower`, `usuario.save`, `usuario.set_password`.

**Expressoes de retorno (dependem do caminho):**

- `usuario`

**Excecoes levantadas:**

- `ValueError('O e-mail e obrigatorio.')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `Command.handle` em [accounts/management/commands/criar_perfis_teste.py](<C:/Users/lb119/Elo/accounts/management/commands/criar_perfis_teste.py:18>).
- `UsuarioManager.create_superuser` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:64>).
- `EstoqueTestsBase.criar_usuario` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:34>).
- `FluxoCadastroTriagemPedidosTests.usuario` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:19>).
- `ConvocacaoCompatibilidadeTests.setUpTestData` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:357>).
- `ConvocacaoCompatibilidadeTests.doador` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:371>).
- `ConvocacaoCompatibilidadeTests.test_outro_perfil_nao_altera_preferencia` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:480>).
- `CentralNotificacoesTests.setUp` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:538>).
- `PedidoSangueTests.criar_usuario` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:11>).
- `TriagemExtensaTests.criar_doador` em [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:30>).
- `TriagemExtensaTests.test_usuario_nao_doador_nao_acessa_triagem` em [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:135>).
- `TriagemExtensaTests.test_receptor_nao_pode_acessar_a_triagem` em [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:159>).
- `TriagemModelTests.setUp` em [accounts/test_triagem_models.py](<C:/Users/lb119/Elo/accounts/test_triagem_models.py:12>).
- `TriagemServicoTests.setUp` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:32>).
- `TriagemServicoTests.test_observador_nao_pode_iniciar_questionario` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:145>).
- `TriagemViewsTests.setUpTestData` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:22>).
- `VisualizacaoPublicaTests.criar_usuario` em [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:13>).
- `ValidacaoHemocentroTests.criar_usuario` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:44>).
- `AuditoriaTests.setUpTestData` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:337>).

### UsuarioManager.create_superuser

Linha 64: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:64>).

```python
def create_superuser(self, email, password=None, **extra_fields):
```

**Explicacao presente no codigo:**

> Cria a conta tecnica que pode acessar o painel /admin/.

**Chamadas utilizadas no corpo:** `ValueError`, `extra_fields.get`, `extra_fields.setdefault`, `self.create_user`.

**Expressoes de retorno (dependem do caminho):**

- `self.create_user(email, password, **extra_fields)`

**Excecoes levantadas:**

- `ValueError('O superusuario precisa ter is_staff=True.')`
- `ValueError('O superusuario precisa ter is_superuser=True.')`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.setUpTestData` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:337>).

### Usuario

Linha 81: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:81>).

Classe; herda de: AbstractUser.

**Explicacao presente no codigo:**

> Conta concreta do Elo, com login por e-mail.
> 
> AbstractUser fornece recursos prontos e testados: hash de senha, ultimo
> login, grupos, permissoes e compatibilidade com o admin. A palavra
> "Abstract" pertence a classe de origem; ``Usuario`` e concreto e cria a
> tabela real ``usuarios`` porque nao foi marcado como abstrato.

**Chamadas utilizadas no corpo:** `UsuarioManager`, `models.BigAutoField`, `models.BooleanField`, `models.CharField`, `models.DateField`, `models.DateTimeField`, `models.EmailField`.

**Atributos/campos declarados diretamente:**

```python
username = None
first_name = None
last_name = None
id_usuario = models.BigAutoField(primary_key=True)
nome = models.CharField(max_length=150)
email = models.EmailField(unique=True)
password = models.CharField(max_length=128, db_column='senha_hash')
cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
cnpj = models.CharField(max_length=14, unique=True, null=True, blank=True)
telefone = models.CharField(max_length=20, blank=True, default='')
data_nascimento = models.DateField(null=True, blank=True)
sexo = models.CharField(max_length=1, choices=Sexo.choices, blank=True, default='')
tipo_sanguineo = models.CharField(max_length=3, choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS], blank=True, default='')
tipo_sanguineo_confirmado = models.BooleanField(default=False)
cidade = models.CharField(max_length=100, blank=True, default='')
estado = models.CharField(max_length=2, blank=True, default='')
perfil = models.CharField(max_length=20, choices=Perfil.choices, default=Perfil.OBSERVADOR)
status_validacao = models.CharField(max_length=20, choices=StatusValidacaoHemocentro.choices, default=StatusValidacaoHemocentro.PENDENTE)
is_active = models.BooleanField(default=True, db_column='ativo')
suspensa = models.BooleanField(default=False)
aceita_notificacoes_pedidos = models.BooleanField(default=True)
email_verificado = models.BooleanField(default=False)
date_joined = models.DateTimeField(auto_now_add=True, db_column='data_cadastro')
atualizado_em = models.DateTimeField(auto_now=True)
objects = UsuarioManager()
USERNAME_FIELD = 'email'
REQUIRED_FIELDS = ['nome']
```

### Usuario.Perfil

Linha 91: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:91>).

Classe; herda de: models.TextChoices.

**Explicacao presente no codigo:**

> Tipos que podem ser escolhidos no cadastro.

**Atributos/campos declarados diretamente:**

```python
DOADOR = ('DOADOR', 'Doador')
RECEPTOR = ('RECEPTOR', 'Receptor')
HEMOCENTRO = ('HEMOCENTRO', 'Hemocentro')
OBSERVADOR = ('OBSERVADOR', 'Observador')
ADMINISTRADOR = ('ADMINISTRADOR', 'Administrador')
```

### Usuario.Sexo

Linha 100: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:100>).

Classe; herda de: models.TextChoices.

**Explicacao presente no codigo:**

> Opcoes fechadas para manter os dados padronizados.

**Atributos/campos declarados diretamente:**

```python
FEMININO = ('F', 'Feminino')
MASCULINO = ('M', 'Masculino')
OUTRO = ('O', 'Outro')
NAO_INFORMADO = ('N', 'Prefiro nao informar')
```

### Usuario.StatusValidacaoHemocentro

Linha 108: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:108>).

Classe; herda de: models.TextChoices.

**Explicacao presente no codigo:**

> Situacao institucional do Hemocentro dentro do Elo.

**Atributos/campos declarados diretamente:**

```python
PENDENTE = ('PENDENTE', 'Pendente')
APROVADO = ('APROVADO', 'Aprovado')
RECUSADO = ('RECUSADO', 'Recusado')
CORRECAO = ('CORRECAO', 'Correcao necessaria')
```

### Usuario.Meta

Linha 181: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:181>).

Classe; herda de: nenhuma classe declarada.

**Atributos/campos declarados diretamente:**

```python
db_table = 'usuarios'
verbose_name = 'usuario'
verbose_name_plural = 'usuarios'
ordering = ['nome']
```

### Usuario.clean

Linha 187: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:187>).

```python
def clean(self):
```

**Explicacao presente no codigo:**

> Padroniza o e-mail quando o model e validado.

**Chamadas utilizadas no corpo:** `self.__class__.objects.normalize_email`, `self.__class__.objects.normalize_email(self.email).lower`, `super`, `super().clean`.

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `CadastroUsuarioForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:244>).
- `TriagemExtensaForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:436>).
- `CadastrarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:506>).
- `MovimentarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:559>).
- `PedidoSangueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:681>).
- `ValidacaoHemocentro.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:277>).
- `Estoque.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:751>).
- `PedidoSangue.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1068>).
- `FormularioPergunta.clean` em [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:105>).

### Usuario.get_full_name

Linha 195: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:195>).

```python
def get_full_name(self):
```

**Explicacao presente no codigo:**

> Devolve o nome completo no formato esperado pelo Django.

**Expressoes de retorno (dependem do caminho):**

- `self.nome`

### Usuario.get_short_name

Linha 200: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:200>).

```python
def get_short_name(self):
```

**Explicacao presente no codigo:**

> Devolve o primeiro nome para saudacoes.

**Chamadas utilizadas no corpo:** `self.nome.split`.

**Expressoes de retorno (dependem do caminho):**

- `self.nome.split()[0] if self.nome else self.email`

### Usuario.is_hemocentro

Linha 206: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:206>).

```python
def is_hemocentro(self):
```

**Explicacao presente no codigo:**

> Informa se a conta representa um Hemocentro cadastrado.

**Decoradores:** `property`.

**Expressoes de retorno (dependem do caminho):**

- `self.perfil == self.Perfil.HEMOCENTRO`

### Usuario.hemocentro_aprovado

Linha 212: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:212>).

```python
def hemocentro_aprovado(self):
```

**Explicacao presente no codigo:**

> Atalho usado pelas regras de publicacao de estoque e campanha.

**Decoradores:** `property`.

**Expressoes de retorno (dependem do caminho):**

- `self.is_hemocentro and self.status_validacao == self.StatusValidacaoHemocentro.APROVADO`

**Onde aparece uma chamada com este nome:**

- `ValidacaoHemocentroTests.test_hemocentro_inicia_pendente` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:79>).
- `validar_publicacao_hemocentro` em [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:41>).
- `registrar_decisao_validacao_pedido` em [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:174>).
- `dashboard` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:720>).
- `aprovar_pedido` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1802>).

### Usuario.__str__

Linha 220: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:220>).

```python
def __str__(self):
```

**Explicacao presente no codigo:**

> Texto usado para representar o usuario no admin e no terminal.

**Expressoes de retorno (dependem do caminho):**

- `f'{self.nome} ({self.email})'`

### ValidacaoHemocentro

Linha 226: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:226>).

Classe; herda de: models.Model.

**Explicacao presente no codigo:**

> Historico das analises institucionais de Hemocentros.
> 
> A tabela registra cada decisao administrativa sem substituir as anteriores.
> O status atual continua em Usuario.status_validacao para consultas rapidas.

**Chamadas utilizadas no corpo:** `models.BigAutoField`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.TextField`.

**Atributos/campos declarados diretamente:**

```python
id_validacao = models.BigAutoField(primary_key=True)
hemocentro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='validacoes_hemocentro', db_column='id_hemocentro')
admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='validacoes_hemocentro_realizadas', db_column='id_admin')
status = models.CharField(max_length=20, choices=Usuario.StatusValidacaoHemocentro.choices)
parecer = models.TextField(blank=True, default='')
data_analise = models.DateTimeField(auto_now_add=True)
```

### ValidacaoHemocentro.Meta

Linha 260: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:260>).

Classe; herda de: nenhuma classe declarada.

**Chamadas utilizadas no corpo:** `models.Index`.

**Atributos/campos declarados diretamente:**

```python
db_table = 'validacoes_hemocentro'
verbose_name = 'validacao de hemocentro'
verbose_name_plural = 'validacoes de hemocentros'
ordering = ['-data_analise']
indexes = [models.Index(fields=['hemocentro', '-data_analise'], name='validacao_hemo_data_idx'), models.Index(fields=['status', 'data_analise'], name='validacao_hemo_status_idx')]
```

### ValidacaoHemocentro.clean

Linha 277: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:277>).

```python
def clean(self):
```

**Explicacao presente no codigo:**

> Impede historico para conta que nao seja Hemocentro.

**Chamadas utilizadas no corpo:** `ValidationError`, `super`, `super().clean`.

**Excecoes levantadas:**

- `ValidationError({'admin': 'A validacao deve ser registrada por um administrador.'})`
- `ValidationError({'hemocentro': 'Somente usuarios com perfil Hemocentro podem ser validados.'})`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `CadastroUsuarioForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:244>).
- `TriagemExtensaForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:436>).
- `CadastrarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:506>).
- `MovimentarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:559>).
- `PedidoSangueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:681>).
- `Usuario.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:187>).
- `Estoque.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:751>).
- `PedidoSangue.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1068>).
- `FormularioPergunta.clean` em [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:105>).

### ValidacaoHemocentro.__str__

Linha 310: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:310>).

```python
def __str__(self):
```

**Chamadas utilizadas no corpo:** `self.get_status_display`.

**Expressoes de retorno (dependem do caminho):**

- `f'{self.hemocentro.nome} - {self.get_status_display()} em {self.data_analise:%d/%m/%Y %H:%M}'`

### ConsentimentoLGPD

Linha 317: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:317>).

Classe; herda de: models.Model.

**Explicacao presente no codigo:**

> Guarda a prova de cada aceite de termo.
> 
> O consentimento fica separado de Usuario porque precisa guardar sua propria
> versao, data e Ip. Quando o texto do termo mudar, uma nova versao podera ser
> aceita sem apagar o registro da versao anterior.

**Chamadas utilizadas no corpo:** `models.BigAutoField`, `models.BooleanField`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.GenericIPAddressField`.

**Atributos/campos declarados diretamente:**

```python
id_consentimento = models.BigAutoField(primary_key=True)
usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consentimentos_lgpd', db_column='id_usuario')
tipo_termo = models.CharField(max_length=20, choices=TipoTermo.choices, default=TipoTermo.GERAL)
versao_termo = models.CharField(max_length=20, default='1.0')
aceito = models.BooleanField(default=False)
data_aceite = models.DateTimeField(auto_now_add=True)
ip = models.GenericIPAddressField(null=True, blank=True)
revogado_em = models.DateTimeField(null=True, blank=True)
```

### ConsentimentoLGPD.TipoTermo

Linha 326: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:326>).

Classe; herda de: models.TextChoices.

**Atributos/campos declarados diretamente:**

```python
GERAL = ('GERAL', 'Termos gerais e politica de privacidade')
TRIAGEM = ('TRIAGEM', 'Termo de triagem')
NOTIFICACOES = ('NOTIFICACOES', 'Termo de notificacoes')
```

### ConsentimentoLGPD.Meta

Linha 352: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:352>).

Classe; herda de: nenhuma classe declarada.

**Chamadas utilizadas no corpo:** `models.UniqueConstraint`.

**Atributos/campos declarados diretamente:**

```python
db_table = 'consentimentos_lgpd'
verbose_name = 'consentimento LGPD'
verbose_name_plural = 'consentimentos LGPD'
ordering = ['-data_aceite']
constraints = [models.UniqueConstraint(fields=['usuario', 'tipo_termo', 'versao_termo'], name='consentimento_unico_por_versao')]
```

### ConsentimentoLGPD.__str__

Linha 365: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:365>).

```python
def __str__(self):
```

**Chamadas utilizadas no corpo:** `self.get_tipo_termo_display`.

**Expressoes de retorno (dependem do caminho):**

- `f'{self.usuario.email} - {self.get_tipo_termo_display()}'`

### AuditoriaAcaoCritica

Linha 369: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:369>).

Classe; herda de: models.Model.

**Explicacao presente no codigo:**

> Registro de eventos sensiveis do Elo, somente leitura no painel administrativo.
> 
> A auditoria guarda o contexto da acao sem copiar senhas, tokens ou dados
> sensiveis completos. Cada tela ou rotina critica deve chamar a funcao
> central de auditoria em accounts/auditoria.py.

**Chamadas utilizadas no corpo:** `models.BigAutoField`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.GenericIPAddressField`, `models.JSONField`, `models.TextField`.

**Atributos/campos declarados diretamente:**

```python
id_auditoria = models.BigAutoField(primary_key=True)
usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='auditorias_acoes_criticas', db_column='id_usuario')
acao = models.CharField(max_length=40, choices=Acao.choices)
resultado = models.CharField(max_length=20, choices=Resultado.choices, default=Resultado.SUCESSO)
alvo_tipo = models.CharField(max_length=80, blank=True, default='')
alvo_id = models.CharField(max_length=80, blank=True, default='')
descricao = models.CharField(max_length=255, blank=True, default='')
ip = models.GenericIPAddressField(null=True, blank=True)
user_agent = models.TextField(blank=True, default='')
metadados = models.JSONField(blank=True, default=dict)
criado_em = models.DateTimeField(auto_now_add=True)
```

### AuditoriaAcaoCritica.Acao

Linha 378: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:378>).

Classe; herda de: models.TextChoices.

**Atributos/campos declarados diretamente:**

```python
LOGIN_FALHO = ('LOGIN_FALHO', 'Login falho')
LOGIN_SUSPEITO = ('LOGIN_SUSPEITO', 'Login suspeito')
ALTERACAO_PERMISSAO = ('ALTERACAO_PERMISSAO', 'Alteracao de permissao')
APROVACAO_HEMOCENTRO = ('APROVACAO_HEMOCENTRO', 'Aprovacao de hemocentro')
CADASTRO_ESTOQUE = ('CADASTRO_ESTOQUE', 'Cadastro de estoque')
ATUALIZACAO_ESTOQUE = ('ATUALIZACAO_ESTOQUE', 'Atualizacao de estoque')
MODERACAO = ('MODERACAO', 'Moderacao')
ACESSO_DADOS_SENSIVEIS = ('ACESSO_DADOS_SENSIVEIS', 'Acesso a dados sensiveis')
CONFIRMACAO_DOACAO = ('CONFIRMACAO_DOACAO', 'Confirmacao de doacao')
```

### AuditoriaAcaoCritica.Resultado

Linha 392: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:392>).

Classe; herda de: models.TextChoices.

**Atributos/campos declarados diretamente:**

```python
SUCESSO = ('SUCESSO', 'Sucesso')
FALHA = ('FALHA', 'Falha')
BLOQUEADO = ('BLOQUEADO', 'Bloqueado')
```

### AuditoriaAcaoCritica.Meta

Linha 424: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:424>).

Classe; herda de: nenhuma classe declarada.

**Chamadas utilizadas no corpo:** `models.Index`.

**Atributos/campos declarados diretamente:**

```python
db_table = 'auditorias_acoes_criticas'
verbose_name = 'auditoria de acao critica'
verbose_name_plural = 'auditorias de acoes criticas'
ordering = ['-criado_em']
indexes = [models.Index(fields=['acao', 'criado_em'], name='auditoria_acao_data_idx'), models.Index(fields=['usuario', 'criado_em'], name='auditoria_usuario_data_idx'), models.Index(fields=['ip', 'criado_em'], name='auditoria_ip_data_idx')]
```

### AuditoriaAcaoCritica.__str__

Linha 445: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:445>).

```python
def __str__(self):
```

**Chamadas utilizadas no corpo:** `self.get_acao_display`, `self.get_resultado_display`.

**Expressoes de retorno (dependem do caminho):**

- `f'{self.get_acao_display()} - {self.get_resultado_display()}'`

### Triagem

Linha 449: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:449>).

Classe; herda de: models.Model.

**Explicacao presente no codigo:**

> Guarda uma triagem realizada por um usuário.
> 
> O resultado é orientativo e nunca substitui a avaliação
> presencial feita pelo hemocentro.

**Chamadas utilizadas no corpo:** `models.BigAutoField`, `models.CharField`, `models.DateField`, `models.DateTimeField`, `models.ForeignKey`, `models.JSONField`, `models.PositiveIntegerField`, `models.TextField`.

**Atributos/campos declarados diretamente:**

```python
id_triagem = models.BigAutoField(primary_key=True)
usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='triagens', db_column='id_usuario')
modalidade = models.CharField(max_length=20, choices=Modalidade.choices, default=Modalidade.EXTENSA)
status = models.CharField(max_length=20, choices=Status.choices, default=Status.EM_ANDAMENTO)
pergunta_atual = models.PositiveIntegerField(default=0)
fluxo_perguntas = models.JSONField(default=list, blank=True)
triagem_base = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='verificacoes_simplificadas')
regra_version = models.CharField(max_length=40, default='HEMOMINAS_2026_08')
resultado = models.CharField(max_length=40, choices=Resultado.choices, blank=True, default='')
mensagem_resultado = models.TextField(blank=True, default='')
data_liberacao = models.DateField(null=True, blank=True)
achados = models.JSONField(default=list, blank=True)
iniciada_em = models.DateTimeField(auto_now_add=True)
finalizada_em = models.DateTimeField(null=True, blank=True)
atualizada_em = models.DateTimeField(auto_now=True)
```

### Triagem.Modalidade

Linha 457: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:457>).

Classe; herda de: models.TextChoices.

**Atributos/campos declarados diretamente:**

```python
EXTENSA = ('EXTENSA', 'Triagem extensa')
SIMPLIFICADA = ('SIMPLIFICADA', 'Triagem simplificada')
```

### Triagem.Status

Linha 461: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:461>).

Classe; herda de: models.TextChoices.

**Explicacao presente no codigo:**

> Representa em qual etapa do questionário a triagem está.

**Atributos/campos declarados diretamente:**

```python
EM_ANDAMENTO = ('EM_ANDAMENTO', 'Em andamento')
CONCLUIDA = ('CONCLUIDA', 'Concluída')
CANCELADA = ('CANCELADA', 'Cancelada')
```

### Triagem.Resultado

Linha 468: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:468>).

Classe; herda de: models.TextChoices.

**Atributos/campos declarados diretamente:**

```python
SEM_IMPEDIMENTO = ('SEM_IMPEDIMENTO_IDENTIFICADO', 'Apto')
TEMPORARIA = ('INAPTIDAO_TEMPORARIA', 'Inaptidão temporária')
DEFINITIVA = ('INAPTIDAO_DEFINITIVA', 'Inaptidão definitiva')
AVALIACAO = ('AVALIACAO_PRESENCIAL', 'Avaliação presencial necessária')
DOCUMENTACAO = ('DOCUMENTACAO_ESPECIAL', 'Documentação especial')
```

### Triagem.Meta

Linha 558: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:558>).

Classe; herda de: nenhuma classe declarada.

**Chamadas utilizadas no corpo:** `models.Index`.

**Atributos/campos declarados diretamente:**

```python
db_table = 'triagens'
ordering = ['-iniciada_em']
indexes = [models.Index(fields=['usuario', '-iniciada_em'], name='triagem_usuario_data_idx'), models.Index(fields=['resultado', '-iniciada_em'], name='triagem_resultado_data_idx')]
verbose_name = 'Triagem'
verbose_name_plural = 'Triagens'
```

### Triagem.__str__

Linha 576: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:576>).

```python
def __str__(self):
```

**Chamadas utilizadas no corpo:** `self.get_resultado_display`.

**Expressoes de retorno (dependem do caminho):**

- `f'Triagem {self.id_triagem} - {self.usuario.nome} - {self.get_resultado_display()}'`

### RespostaTriagem

Linha 592: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:592>).

Classe; herda de: models.Model.

**Explicacao presente no codigo:**

> Guarda uma resposta individual da triagem.
> 
> As respostas são mantidas separadas para permitir auditoria,
> revisão das regras e futuras versões do questionário.

**Chamadas utilizadas no corpo:** `models.BigAutoField`, `models.CharField`, `models.DateField`, `models.DateTimeField`, `models.ForeignKey`, `models.JSONField`.

**Atributos/campos declarados diretamente:**

```python
id_resposta = models.BigAutoField(primary_key=True)
triagem = models.ForeignKey(Triagem, on_delete=models.CASCADE, related_name='respostas', db_column='id_triagem')
id_pergunta = models.CharField(max_length=20)
codigo_resposta = models.CharField(max_length=80)
resposta_label = models.CharField(max_length=255)
data_evento = models.DateField(db_column='event_date', null=True, blank=True)
metadata = models.JSONField(default=dict, blank=True)
valor = models.JSONField(default=dict, blank=True)
rule_version = models.CharField(max_length=40, default='HEMOMINAS_2026_08')
source_ref = models.CharField(max_length=255, blank=True, default='')
respondido_em = models.DateTimeField(auto_now_add=True)
```

**Onde aparece uma chamada com este nome:**

- `_copiar_respostas_para_nova_triagem` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:142>).

### RespostaTriagem.Meta

Linha 642: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:642>).

Classe; herda de: nenhuma classe declarada.

**Chamadas utilizadas no corpo:** `models.Index`, `models.UniqueConstraint`.

**Atributos/campos declarados diretamente:**

```python
db_table = 'respostas_triagem'
ordering = ['id_resposta']
constraints = [models.UniqueConstraint(fields=['triagem', 'id_pergunta'], name='resposta_unica_por_pergunta')]
indexes = [models.Index(fields=['triagem', 'id_pergunta'], name='resposta_triagem_pergunta_idx')]
verbose_name = 'Resposta triagem'
verbose_name_plural = 'Respostas triagem'
```

### RespostaTriagem.__str__

Linha 663: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:663>).

```python
def __str__(self):
```

**Expressoes de retorno (dependem do caminho):**

- `f'{self.triagem_id} - {self.id_pergunta} - {self.codigo_resposta}'`

### Estoque

Linha 671: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:671>).

Classe; herda de: models.Model.

**Explicacao presente no codigo:**

> Uc_29 - Cadastrar Estoque.
> 
> Guarda a estrutura de estoque de um Hemocentro para um unico tipo
> sanguineo: quantidade atual de bolsas, os niveis de alerta definidos
> pelo proprio hemocentro e o status calculado a partir desses valores.
> 
> So existe um registro de Estoque por combinacao de hemocentro e tipo
> sanguineo (garantido pela UniqueConstraint abaixo). Para mudar a
> quantidade de bolsas depois de criado, use as funcoes de
> ``accounts/estoque.py`` em vez de editar o campo diretamente: elas
> recalculam o status, criam o historico em EstoqueMovimentacao e
> registram a auditoria.

**Chamadas utilizadas no corpo:** `models.BigAutoField`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.PositiveIntegerField`.

**Atributos/campos declarados diretamente:**

```python
id_estoque = models.BigAutoField(primary_key=True)
hemocentro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='estoques', db_column='id_hemocentro', limit_choices_to={'perfil': 'HEMOCENTRO'})
tipo_sanguineo = models.CharField(max_length=3, choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS])
quantidade_bolsas = models.PositiveIntegerField(default=0)
nivel_minimo = models.PositiveIntegerField()
nivel_critico = models.PositiveIntegerField()
status_calculado = models.CharField(max_length=10, choices=StatusCalculado.choices, default=StatusCalculado.ESTAVEL)
data_atualizacao = models.DateTimeField(auto_now=True)
```

### Estoque.StatusCalculado

Linha 687: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:687>).

Classe; herda de: models.TextChoices.

**Explicacao presente no codigo:**

> Situacao do estoque, sempre derivada da quantidade e dos niveis.
> 
> Nunca deve ser digitada manualmente por quem usa o sistema: a
> camada de servico recalcula este campo toda vez que a quantidade
> de bolsas muda.

**Atributos/campos declarados diretamente:**

```python
CRITICO = ('CRITICO', 'Crítico')
BAIXO = ('BAIXO', 'Baixo')
ESTAVEL = ('ESTAVEL', 'Estável')
```

### Estoque.Meta

Linha 727: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:727>).

Classe; herda de: nenhuma classe declarada.

**Chamadas utilizadas no corpo:** `models.Index`, `models.UniqueConstraint`.

**Atributos/campos declarados diretamente:**

```python
db_table = 'estoques'
verbose_name = 'estoque'
verbose_name_plural = 'estoques'
ordering = ['hemocentro__nome', 'tipo_sanguineo']
constraints = [models.UniqueConstraint(fields=['hemocentro', 'tipo_sanguineo'], name='estoque_unico_por_hemocentro_tipo')]
indexes = [models.Index(fields=['hemocentro', 'tipo_sanguineo'], name='estoque_hemo_tipo_idx'), models.Index(fields=['status_calculado'], name='estoque_status_idx')]
```

### Estoque.clean

Linha 751: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:751>).

```python
def clean(self):
```

**Explicacao presente no codigo:**

> Valida regras que dependem de mais de um campo.

**Chamadas utilizadas no corpo:** `ValidationError`, `super`, `super().clean`.

**Excecoes levantadas:**

- `ValidationError({'hemocentro': 'Somente contas com perfil Hemocentro podem ter estoque.'})`
- `ValidationError({'nivel_critico': 'O nivel critico deve ser menor ou igual ao nivel minimo.'})`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `CadastroUsuarioForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:244>).
- `TriagemExtensaForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:436>).
- `CadastrarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:506>).
- `MovimentarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:559>).
- `PedidoSangueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:681>).
- `Usuario.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:187>).
- `ValidacaoHemocentro.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:277>).
- `PedidoSangue.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1068>).
- `FormularioPergunta.clean` em [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:105>).

### Estoque.__str__

Linha 781: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:781>).

```python
def __str__(self):
```

**Chamadas utilizadas no corpo:** `self.get_status_calculado_display`.

**Expressoes de retorno (dependem do caminho):**

- `f'{self.hemocentro.nome} - {self.tipo_sanguineo} ({self.get_status_calculado_display()})'`

### EstoqueMovimentacao

Linha 788: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:788>).

Classe; herda de: models.Model.

**Explicacao presente no codigo:**

> Uc_30 - Atualizar Estoque.
> 
> Historico imutavel de cada entrada, saida ou ajuste feito em um
> Estoque. Uma linha nunca e alterada ou apagada depois de criada: para
> corrigir um valor, registra-se uma nova movimentacao (do tipo Ajuste).
> 
> Isso preserva o rastro completo exigido pela regra "toda alteracao
> deve gerar historico com responsavel".

**Chamadas utilizadas no corpo:** `models.BigAutoField`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.IntegerField`, `models.PositiveIntegerField`.

**Atributos/campos declarados diretamente:**

```python
id_mov = models.BigAutoField(primary_key=True)
estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='movimentacoes', db_column='id_estoque')
usuario_resp = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimentacoes_estoque_realizadas', db_column='id_usuario_resp')
tipo_movimento = models.CharField(max_length=10, choices=TipoMovimento.choices)
quantidade_anterior = models.PositiveIntegerField()
quantidade_movimentada = models.IntegerField()
quantidade_nova = models.PositiveIntegerField()
motivo = models.CharField(max_length=255, blank=True, default='')
data_hora = models.DateTimeField(auto_now_add=True)
```

### EstoqueMovimentacao.TipoMovimento

Linha 800: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:800>).

Classe; herda de: models.TextChoices.

**Atributos/campos declarados diretamente:**

```python
ENTRADA = ('ENTRADA', 'Entrada')
SAIDA = ('SAIDA', 'Saída')
AJUSTE = ('AJUSTE', 'Ajuste')
```

### EstoqueMovimentacao.Meta

Linha 840: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:840>).

Classe; herda de: nenhuma classe declarada.

**Chamadas utilizadas no corpo:** `models.Index`.

**Atributos/campos declarados diretamente:**

```python
db_table = 'movimentacoes_estoque'
verbose_name = 'movimentacao de estoque'
verbose_name_plural = 'movimentacoes de estoque'
ordering = ['-data_hora']
indexes = [models.Index(fields=['estoque', '-data_hora'], name='mov_estoque_data_idx'), models.Index(fields=['usuario_resp', '-data_hora'], name='mov_usuario_data_idx')]
```

### EstoqueMovimentacao.__str__

Linha 857: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:857>).

```python
def __str__(self):
```

**Chamadas utilizadas no corpo:** `self.get_tipo_movimento_display`.

**Expressoes de retorno (dependem do caminho):**

- `f'{self.estoque.tipo_sanguineo} - {self.get_tipo_movimento_display()} - {self.quantidade_anterior} -> {self.quantidade_nova}'`

### Notificacao

Linha 865: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:865>).

Classe; herda de: models.Model.

**Explicacao presente no codigo:**

> Guarda avisos internos exibidos no dashboard do usuario.
> 
> Nesta etapa, a notificacao sera usada para avisar doadores compativeis
> quando um estoque atualizado por Hemocentro ficar em nivel Baixo ou Critico.
> Futuramente a mesma tabela tambem pode receber outros avisos do sistema.

**Chamadas utilizadas no corpo:** `models.BigAutoField`, `models.BooleanField`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.TextField`.

**Atributos/campos declarados diretamente:**

```python
id_notificacao = models.BigAutoField(primary_key=True)
usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificacoes', db_column='id_usuario')
estoque = models.ForeignKey(Estoque, on_delete=models.SET_NULL, null=True, blank=True, related_name='notificacoes', db_column='id_estoque')
pedido = models.ForeignKey('PedidoSangue', on_delete=models.SET_NULL, null=True, blank=True, related_name='notificacoes', db_column='id_pedido')
tipo = models.CharField(max_length=30, choices=Tipo.choices, default=Tipo.GERAL)
titulo = models.CharField(max_length=120)
mensagem = models.TextField()
url_destino = models.CharField(max_length=255, blank=True, default='')
lida = models.BooleanField(default=False)
criada_em = models.DateTimeField(auto_now_add=True)
lida_em = models.DateTimeField(null=True, blank=True)
```

**Onde aparece uma chamada com este nome:**

- `criar_notificacoes_para_doadores_compativeis` em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:37>).
- `criar_notificacoes_para_pedido` em [accounts/pedidos.py](<C:/Users/lb119/Elo/accounts/pedidos.py:52>).

### Notificacao.Tipo

Linha 874: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:874>).

Classe; herda de: models.TextChoices.

**Explicacao presente no codigo:**

> Classificacao do aviso para facilitar filtros futuros.

**Atributos/campos declarados diretamente:**

```python
ESTOQUE_BAIXO = ('ESTOQUE_BAIXO', 'Estoque baixo')
ESTOQUE_CRITICO = ('ESTOQUE_CRITICO', 'Estoque crítico')
PEDIDO_COMPATIVEL = ('PEDIDO_COMPATIVEL', 'Pedido compatível')
GERAL = ('GERAL', 'Aviso geral')
```

### Notificacao.Meta

Linha 922: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:922>).

Classe; herda de: nenhuma classe declarada.

**Chamadas utilizadas no corpo:** `models.Index`.

**Atributos/campos declarados diretamente:**

```python
db_table = 'notificacoes'
verbose_name = 'notificacao'
verbose_name_plural = 'notificacoes'
ordering = ['-criada_em']
indexes = [models.Index(fields=['usuario', 'lida', '-criada_em'], name='notificacao_usuario_lida_idx'), models.Index(fields=['tipo', '-criada_em'], name='notificacao_tipo_data_idx')]
```

### Notificacao.__str__

Linha 939: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:939>).

```python
def __str__(self):
```

**Explicacao presente no codigo:**

> Texto usado no admin e no terminal.

**Expressoes de retorno (dependem do caminho):**

- `f'{self.usuario.nome} - {self.titulo}'`

### PedidoSangue

Linha 945: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:945>).

Classe; herda de: models.Model.

**Explicacao presente no codigo:**

> Rf - Pedido de Sangue.
> 
> Guarda solicitações de divulgação e os pedidos publicados oficialmente.
> 
> Doador, Receptor, Observador e Visitante criam somente uma solicitação.
> A publicação oficial é feita pelo Hemocentro aprovado vinculado.

**Chamadas utilizadas no corpo:** `models.BigAutoField`, `models.BooleanField`, `models.CharField`, `models.DateTimeField`, `models.EmailField`, `models.ForeignKey`, `models.TextField`.

**Atributos/campos declarados diretamente:**

```python
id_pedido = models.BigAutoField(primary_key=True)
solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_sangue', db_column='id_solicitante')
nome_solicitante = models.CharField(max_length=150, default='')
contato = models.EmailField(max_length=120, default='')
hemocentro_destino = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='pedidos_recebidos', db_column='id_hemocentro_destino', limit_choices_to={'perfil': 'HEMOCENTRO'})
para_quem = models.CharField(max_length=20, choices=ParaQuem.choices)
titulo = models.CharField(max_length=150, default='Pedido de sangue')
tipo_sanguineo = models.CharField(max_length=3, choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS])
urgencia = models.CharField(max_length=10, choices=Urgencia.choices)
cidade = models.CharField(max_length=100)
nome_paciente = models.CharField(max_length=150, blank=True, default='')
descricao = models.TextField()
justificativa_urgencia = models.TextField(blank=True, default='')
informacoes_complementares = models.TextField(blank=True, default='')
status = models.CharField(max_length=30, choices=Status.choices, default=Status.ENVIADA)
duplicidade_suspeita = models.BooleanField(default=False)
publicado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_publicados', db_column='id_publicado_por')
publicado_em = models.DateTimeField(null=True, blank=True)
data_criacao = models.DateTimeField(auto_now_add=True)
atualizado_em = models.DateTimeField(auto_now=True)
data_fechamento = models.DateTimeField(null=True, blank=True)
```

**Onde aparece uma chamada com este nome:**

- `criar_pedido_pendente` em [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:116>).

### PedidoSangue.ParaQuem

Linha 955: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:955>).

Classe; herda de: models.TextChoices.

**Atributos/campos declarados diretamente:**

```python
MIM = ('MIM', 'Para mim')
OUTRA_PESSOA = ('OUTRA_PESSOA', 'Para outra pessoa')
```

### PedidoSangue.Urgencia

Linha 959: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:959>).

Classe; herda de: models.TextChoices.

**Atributos/campos declarados diretamente:**

```python
BAIXA = ('BAIXA', 'Baixa')
MEDIA = ('MEDIA', 'Media')
ALTA = ('ALTA', 'Alta')
CRITICA = ('CRITICA', 'Critica')
```

### PedidoSangue.Status

Linha 965: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:965>).

Classe; herda de: models.TextChoices.

**Atributos/campos declarados diretamente:**

```python
ENVIADA = ('ENVIADA', 'Enviada')
EM_ANALISE = ('EM_ANALISE', 'Em análise')
PUBLICADA = ('PUBLICADA', 'Publicada')
CORRECAO_SOLICITADA = ('CORRECAO_SOLICITADA', 'Correção solicitada')
RECUSADA = ('RECUSADA', 'Recusada')
ENCERRADA = ('ENCERRADA', 'Encerrada')
```

### PedidoSangue.Meta

Linha 1047: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1047>).

Classe; herda de: nenhuma classe declarada.

**Chamadas utilizadas no corpo:** `models.Index`.

**Atributos/campos declarados diretamente:**

```python
db_table = 'pedidos_sangue'
ordering = ['-data_criacao']
verbose_name = 'pedido de sangue'
verbose_name_plural = 'pedidos de sangue'
indexes = [models.Index(fields=['status', '-data_criacao'], name='pedido_status_data_idx'), models.Index(fields=['tipo_sanguineo', 'urgencia'], name='pedido_tipo_urg_idx'), models.Index(fields=['cidade'], name='pedido_cidade_idx')]
```

### PedidoSangue.clean

Linha 1068: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1068>).

```python
def clean(self):
```

**Chamadas utilizadas no corpo:** `ValidationError`, `super`, `super().clean`.

**Excecoes levantadas:**

- `ValidationError({'hemocentro_destino': 'O destino precisa ser um Hemocentro cadastrado.'})`
- `ValidationError({'publicado_por': 'A publicação precisa de um Hemocentro aprovado.'})`
- `ValidationError({'publicado_por': 'Somente Hemocentro aprovado pode publicar.'})`
- `ValidationError({'solicitante': 'Este perfil não pode enviar solicitações.'})`

**Estrutura de controle:** If: 5. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `CadastroUsuarioForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:244>).
- `TriagemExtensaForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:436>).
- `CadastrarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:506>).
- `MovimentarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:559>).
- `PedidoSangueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:681>).
- `Usuario.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:187>).
- `ValidacaoHemocentro.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:277>).
- `Estoque.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:751>).
- `FormularioPergunta.clean` em [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:105>).

### PedidoSangue.__str__

Linha 1105: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1105>).

```python
def __str__(self):
```

**Chamadas utilizadas no corpo:** `self.get_status_display`.

**Expressoes de retorno (dependem do caminho):**

- `f'{self.titulo} - {self.tipo_sanguineo} - {self.get_status_display()}'`

### ValidacaoPedido

Linha 1121: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1121>).

Classe; herda de: models.Model.

**Explicacao presente no codigo:**

> Uc_17 - Validar Pedido.
> 
> Guarda o historico das validacoes feitas automaticamente ou por moderador.

**Chamadas utilizadas no corpo:** `models.BigAutoField`, `models.CharField`, `models.DateTimeField`, `models.ForeignKey`, `models.TextField`.

**Atributos/campos declarados diretamente:**

```python
id_validacao = models.BigAutoField(primary_key=True)
pedido = models.ForeignKey(PedidoSangue, on_delete=models.CASCADE, related_name='validacoes', db_column='id_pedido')
status_validacao = models.CharField(max_length=20, choices=StatusValidacao.choices)
motivo = models.TextField(blank=True, default='')
moderador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='validacoes_pedido_realizadas', db_column='id_moderador')
data_validacao = models.DateTimeField(auto_now_add=True)
```

### ValidacaoPedido.StatusValidacao

Linha 1128: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1128>).

Classe; herda de: models.TextChoices.

**Atributos/campos declarados diretamente:**

```python
APROVADO = ('APROVADO', 'Aprovado')
CORRECAO_SOLICITADA = ('CORRECAO_SOLICITADA', 'Correção solicitada')
SUSPEITO = ('SUSPEITO', 'Suspeito')
RECUSADO = ('RECUSADO', 'Recusado')
```

### ValidacaoPedido.Meta

Linha 1161: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1161>).

Classe; herda de: nenhuma classe declarada.

**Atributos/campos declarados diretamente:**

```python
db_table = 'validacoes_pedido'
ordering = ['-data_validacao']
```

### ValidacaoPedido.__str__

Linha 1165: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1165>).

```python
def __str__(self):
```

**Chamadas utilizadas no corpo:** `self.get_status_validacao_display`.

**Expressoes de retorno (dependem do caminho):**

- `f'Pedido {self.pedido_id} - {self.get_status_validacao_display()}'`


## accounts/pedidos.py

Publicacao institucional e alertas de pedidos compativeis.

Original: [accounts/pedidos.py](<C:/Users/lb119/Elo/accounts/pedidos.py>).

**Dependencias importadas:**

```python
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from .compatibilidade import doadores_aptos_para_convocacao, limite_convocacao_atingido
from .models import AuditoriaAcaoCritica, Notificacao, PedidoSangue, Usuario
from .auditoria import registrar_auditoria
```

### pode_publicar_pedido

Linha 13: [accounts/pedidos.py](<C:/Users/lb119/Elo/accounts/pedidos.py:13>).

```python
def pode_publicar_pedido(usuario):
```

**Explicacao presente no codigo:**

> Somente o Hemocentro aprovado pode publicar oficialmente.

**Expressoes de retorno (dependem do caminho):**

- `usuario.is_authenticated and usuario.perfil == Usuario.Perfil.HEMOCENTRO and (usuario.status_validacao == Usuario.StatusValidacaoHemocentro.APROVADO)`

**Onde aparece uma chamada com este nome:**

- `publicar_pedido` em [accounts/pedidos.py](<C:/Users/lb119/Elo/accounts/pedidos.py:25>).
- `criar_notificacoes_para_pedido` em [accounts/pedidos.py](<C:/Users/lb119/Elo/accounts/pedidos.py:52>).
- `PedidoSangueTests.test_permissao_do_servico_de_publicacao` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:249>).

### publicar_pedido

Linha 25: [accounts/pedidos.py](<C:/Users/lb119/Elo/accounts/pedidos.py:25>).

```python
def publicar_pedido(usuario, form, request=None):
```

**Explicacao presente no codigo:**

> Publica um pedido já analisado pelo próprio Hemocentro.

**Decoradores:** `transaction.atomic`.

**Chamadas utilizadas no corpo:** `PermissionDenied`, `criar_notificacoes_para_pedido`, `form.save`, `pedido.full_clean`, `pedido.save`, `pode_publicar_pedido`, `registrar_auditoria`, `timezone.now`.

**Expressoes de retorno (dependem do caminho):**

- `pedido`

**Excecoes levantadas:**

- `PermissionDenied('Este perfil não pode publicar pedidos de sangue.')`
- `PermissionDenied('O pedido pertence a outro Hemocentro.')`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `ConvocacaoCompatibilidadeTests.test_publicacao_alternativa_tambem_convoca` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:501>).

### criar_notificacoes_para_pedido

Linha 52: [accounts/pedidos.py](<C:/Users/lb119/Elo/accounts/pedidos.py:52>).

```python
def criar_notificacoes_para_pedido(*, pedido):
```

**Explicacao presente no codigo:**

> Notifica apenas doadores compatíveis e aptos para o pedido publicado.

**Decoradores:** `transaction.atomic`.

**Chamadas utilizadas no corpo:** `Notificacao`, `Notificacao.objects.bulk_create`, `Notificacao.objects.filter`, `Notificacao.objects.filter(usuario=doador, pedido=pedido).exists`, `doadores_aptos_para_convocacao`, `doadores_aptos_para_convocacao(pedido.tipo_sanguineo).select_for_update`, `len`, `limite_convocacao_atingido`, `notificacoes.append`, `pode_publicar_pedido`, `reverse`.

**Expressoes de retorno (dependem do caminho):**

- `0`
- `len(notificacoes)`

**Estrutura de controle:** If: 3, For: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `publicar_pedido` em [accounts/pedidos.py](<C:/Users/lb119/Elo/accounts/pedidos.py:25>).
- `ConvocacaoCompatibilidadeTests.emitir` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:381>).
- `registrar_decisao_validacao_pedido` em [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:174>).


## accounts/signals.py

Registro automatico das falhas de autenticacao.

Original: [accounts/signals.py](<C:/Users/lb119/Elo/accounts/signals.py>).

**Dependencias importadas:**

```python
from datetime import timedelta
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver
from django.utils import timezone
from .auditoria import obter_ip, obter_user_agent, registrar_auditoria
from .models import AuditoriaAcaoCritica
```

### auditar_login_falho

Linha 23: [accounts/signals.py](<C:/Users/lb119/Elo/accounts/signals.py:23>).

```python
def auditar_login_falho(sender, credentials, request, **kwargs):
```

**Explicacao presente no codigo:**

> Registra falha e login suspeito sem guardar a senha enviada.

**Decoradores:** `receiver(user_login_failed)`.

**Chamadas utilizadas no corpo:** `(credentials or {}).get`, `(email or '').strip`, `(email or '').strip().lower`, `AuditoriaAcaoCritica.objects.filter`, `falhas_recentes.count`, `falhas_recentes.filter`, `obter_ip`, `obter_user_agent`, `registrar_auditoria`, `timedelta`, `timezone.now`.

**Estrutura de controle:** If: 3. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `AuditoriaTests.test_login_suspeito_nao_afirma_bloqueio` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:401>).

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `LIMITE_LOGIN_SUSPEITO`: linha 18; valor declarado em [accounts/signals.py](<C:/Users/lb119/Elo/accounts/signals.py:18>).
- `JANELA_LOGIN_SUSPEITO_MINUTOS`: linha 19; valor declarado em [accounts/signals.py](<C:/Users/lb119/Elo/accounts/signals.py:19>).

## accounts/test_estoque.py

Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

Original: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py>).

**Dependencias importadas:**

```python
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase
from django.urls import reverse
from .estoque import calcular_status_calculado, cadastrar_estoque, registrar_movimentacao_estoque
from .models import AuditoriaAcaoCritica, Estoque, EstoqueMovimentacao, Usuario
from .validacao_hemocentro import aprovar_hemocentro
```

### EstoqueTestsBase

Linha 31: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:31>).

Classe; herda de: TestCase.

**Explicacao presente no codigo:**

> Prepara um administrador e Hemocentros usados pelos testes.

### EstoqueTestsBase.criar_usuario

Linha 34: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:34>).

```python
def criar_usuario(self, *, email, nome, perfil):
```

**Chamadas utilizadas no corpo:** `Usuario.objects.create_user`.

**Expressoes de retorno (dependem do caminho):**

- `Usuario.objects.create_user(email=email, password='SenhaForte123!', nome=nome, perfil=perfil)`

**Onde aparece uma chamada com este nome:**

- `EstoqueTestsBase.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:42>).
- `RegistrarMovimentacaoEstoqueTests.test_outro_hemocentro_nao_pode_movimentar_estoque_alheio` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:288>).
- `PedidoSangueTests.setUp` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:21>).
- `VisualizacaoPublicaTests.setUp` em [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:23>).
- `ValidacaoHemocentroTests.setUp` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:64>).
- `ValidacaoHemocentroTests.test_usuario_comum_nao_pode_validar` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:156>).
- `ValidacaoHemocentroTests.test_usuario_comum_nao_acessa_tela_de_validacao` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:300>).

### EstoqueTestsBase.setUp

Linha 42: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:42>).

```python
def setUp(self):
```

**Chamadas utilizadas no corpo:** `aprovar_hemocentro`, `self.criar_usuario`, `self.hemocentro.refresh_from_db`.

**Onde aparece uma chamada com este nome:**

- `RegistrarMovimentacaoEstoqueTests.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:176>).

### CalcularStatusCalculadoTests

Linha 70: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:70>).

Classe; herda de: TestCase.

**Explicacao presente no codigo:**

> Testa a regra pura de calculo de status, sem tocar o banco.

### CalcularStatusCalculadoTests.test_quantidade_igual_ao_critico_e_critico

Linha 73: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:73>).

```python
def test_quantidade_igual_ao_critico_e_critico(self):
```

Cenario descrito pelo nome: quantidade igual ao critico e critico.

**Chamadas utilizadas no corpo:** `calcular_status_calculado`, `self.assertEqual`.

### CalcularStatusCalculadoTests.test_quantidade_abaixo_do_critico_e_critico

Linha 81: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:81>).

```python
def test_quantidade_abaixo_do_critico_e_critico(self):
```

Cenario descrito pelo nome: quantidade abaixo do critico e critico.

**Chamadas utilizadas no corpo:** `calcular_status_calculado`, `self.assertEqual`.

### CalcularStatusCalculadoTests.test_quantidade_igual_ao_minimo_e_baixo

Linha 89: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:89>).

```python
def test_quantidade_igual_ao_minimo_e_baixo(self):
```

Cenario descrito pelo nome: quantidade igual ao minimo e baixo.

**Chamadas utilizadas no corpo:** `calcular_status_calculado`, `self.assertEqual`.

### CalcularStatusCalculadoTests.test_quantidade_acima_do_minimo_e_estavel

Linha 97: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:97>).

```python
def test_quantidade_acima_do_minimo_e_estavel(self):
```

Cenario descrito pelo nome: quantidade acima do minimo e estavel.

**Chamadas utilizadas no corpo:** `calcular_status_calculado`, `self.assertEqual`.

### CadastrarEstoqueTests

Linha 106: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:106>).

Classe; herda de: EstoqueTestsBase.

**Explicacao presente no codigo:**

> Testes principais do UC_29.

### CadastrarEstoqueTests.test_hemocentro_aprovado_cadastra_estoque

Linha 109: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:109>).

```python
def test_hemocentro_aprovado_cadastra_estoque(self):
```

Cenario descrito pelo nome: hemocentro aprovado cadastra estoque.

**Chamadas utilizadas no corpo:** `AuditoriaAcaoCritica.objects.filter`, `AuditoriaAcaoCritica.objects.filter(acao=AuditoriaAcaoCritica.Acao.CADASTRO_ESTOQUE, usuario=self.hemocentro, alvo_id=str(estoque.pk)).exists`, `cadastrar_estoque`, `self.assertEqual`, `self.assertTrue`, `str`.

### CadastrarEstoqueTests.test_hemocentro_pendente_nao_pode_cadastrar_estoque

Linha 129: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:129>).

```python
def test_hemocentro_pendente_nao_pode_cadastrar_estoque(self):
```

Cenario descrito pelo nome: hemocentro pendente nao pode cadastrar estoque.

**Chamadas utilizadas no corpo:** `cadastrar_estoque`, `self.assertRaises`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### CadastrarEstoqueTests.test_nao_permite_cadastro_duplicado

Linha 138: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:138>).

```python
def test_nao_permite_cadastro_duplicado(self):
```

Cenario descrito pelo nome: nao permite cadastro duplicado.

**Chamadas utilizadas no corpo:** `cadastrar_estoque`, `self.assertRaises`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### CadastrarEstoqueTests.test_nivel_critico_maior_que_minimo_gera_erro

Linha 154: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:154>).

```python
def test_nivel_critico_maior_que_minimo_gera_erro(self):
```

Cenario descrito pelo nome: nivel critico maior que minimo gera erro.

**Chamadas utilizadas no corpo:** `cadastrar_estoque`, `self.assertRaises`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### CadastrarEstoqueTests.test_tipo_sanguineo_invalido_gera_erro

Linha 163: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:163>).

```python
def test_tipo_sanguineo_invalido_gera_erro(self):
```

Cenario descrito pelo nome: tipo sanguineo invalido gera erro.

**Chamadas utilizadas no corpo:** `cadastrar_estoque`, `self.assertRaises`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### RegistrarMovimentacaoEstoqueTests

Linha 173: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:173>).

Classe; herda de: EstoqueTestsBase.

**Explicacao presente no codigo:**

> Testes principais do UC_30.

### RegistrarMovimentacaoEstoqueTests.setUp

Linha 176: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:176>).

```python
def setUp(self):
```

**Chamadas utilizadas no corpo:** `cadastrar_estoque`, `super`, `super().setUp`.

### RegistrarMovimentacaoEstoqueTests.test_entrada_soma_quantidade_e_recalcula_status

Linha 187: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:187>).

```python
def test_entrada_soma_quantidade_e_recalcula_status(self):
```

Cenario descrito pelo nome: entrada soma quantidade e recalcula status.

**Chamadas utilizadas no corpo:** `registrar_movimentacao_estoque`, `self.assertEqual`, `self.estoque.refresh_from_db`.

### RegistrarMovimentacaoEstoqueTests.test_saida_subtrai_quantidade

Linha 204: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:204>).

```python
def test_saida_subtrai_quantidade(self):
```

Cenario descrito pelo nome: saida subtrai quantidade.

**Chamadas utilizadas no corpo:** `registrar_movimentacao_estoque`, `self.assertEqual`, `self.estoque.refresh_from_db`.

### RegistrarMovimentacaoEstoqueTests.test_saida_maior_que_estoque_gera_erro_e_nao_altera_nada

Linha 219: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:219>).

```python
def test_saida_maior_que_estoque_gera_erro_e_nao_altera_nada(self):
```

Cenario descrito pelo nome: saida maior que estoque gera erro e nao altera nada.

**Chamadas utilizadas no corpo:** `EstoqueMovimentacao.objects.filter`, `EstoqueMovimentacao.objects.filter(estoque=self.estoque).count`, `registrar_movimentacao_estoque`, `self.assertEqual`, `self.assertRaises`, `self.estoque.refresh_from_db`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### RegistrarMovimentacaoEstoqueTests.test_ajuste_define_quantidade_absoluta_e_aceita_delta_negativo

Linha 235: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:235>).

```python
def test_ajuste_define_quantidade_absoluta_e_aceita_delta_negativo(self):
```

Cenario descrito pelo nome: ajuste define quantidade absoluta e aceita delta negativo.

**Chamadas utilizadas no corpo:** `registrar_movimentacao_estoque`, `self.assertEqual`, `self.estoque.refresh_from_db`.

### RegistrarMovimentacaoEstoqueTests.test_motivo_e_obrigatorio_na_movimentacao

Linha 251: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:251>).

```python
def test_motivo_e_obrigatorio_na_movimentacao(self):
```

Cenario descrito pelo nome: motivo e obrigatorio na movimentacao.

**Chamadas utilizadas no corpo:** `EstoqueMovimentacao.objects.filter`, `EstoqueMovimentacao.objects.filter(estoque=self.estoque).count`, `registrar_movimentacao_estoque`, `self.assertEqual`, `self.assertRaises`, `self.estoque.refresh_from_db`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### RegistrarMovimentacaoEstoqueTests.test_movimentacao_gera_historico_e_auditoria

Linha 268: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:268>).

```python
def test_movimentacao_gera_historico_e_auditoria(self):
```

Cenario descrito pelo nome: movimentacao gera historico e auditoria.

**Chamadas utilizadas no corpo:** `AuditoriaAcaoCritica.objects.filter`, `AuditoriaAcaoCritica.objects.filter(acao=AuditoriaAcaoCritica.Acao.ATUALIZACAO_ESTOQUE, usuario=self.hemocentro, alvo_id=str(self.estoque.pk)).exists`, `EstoqueMovimentacao.objects.filter`, `EstoqueMovimentacao.objects.filter(estoque=self.estoque).count`, `registrar_movimentacao_estoque`, `self.assertEqual`, `self.assertTrue`, `str`.

### RegistrarMovimentacaoEstoqueTests.test_outro_hemocentro_nao_pode_movimentar_estoque_alheio

Linha 288: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:288>).

```python
def test_outro_hemocentro_nao_pode_movimentar_estoque_alheio(self):
```

Cenario descrito pelo nome: outro hemocentro nao pode movimentar estoque alheio.

**Chamadas utilizadas no corpo:** `aprovar_hemocentro`, `outro_hemocentro.refresh_from_db`, `registrar_movimentacao_estoque`, `self.assertRaises`, `self.criar_usuario`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### RegistrarMovimentacaoEstoqueTests.test_doador_nao_pode_movimentar_estoque

Linha 305: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:305>).

```python
def test_doador_nao_pode_movimentar_estoque(self):
```

Cenario descrito pelo nome: doador nao pode movimentar estoque.

**Chamadas utilizadas no corpo:** `registrar_movimentacao_estoque`, `self.assertRaises`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### EstoqueViewsTests

Linha 315: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:315>).

Classe; herda de: EstoqueTestsBase.

**Explicacao presente no codigo:**

> Testes de ponta a ponta usando o client de testes do Django.

### EstoqueViewsTests.test_painel_bloqueia_hemocentro_pendente

Linha 318: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:318>).

```python
def test_painel_bloqueia_hemocentro_pendente(self):
```

Cenario descrito pelo nome: painel bloqueia hemocentro pendente.

**Chamadas utilizadas no corpo:** `reverse`, `self.assertEqual`, `self.client.force_login`, `self.client.get`.

### EstoqueViewsTests.test_post_cadastra_estoque_via_view

Linha 325: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:325>).

```python
def test_post_cadastra_estoque_via_view(self):
```

Cenario descrito pelo nome: post cadastra estoque via view.

**Chamadas utilizadas no corpo:** `Estoque.objects.filter`, `Estoque.objects.filter(hemocentro=self.hemocentro, tipo_sanguineo='AB+').exists`, `reverse`, `self.assertRedirects`, `self.assertTrue`, `self.client.force_login`, `self.client.post`.

### EstoqueViewsTests.test_post_movimenta_estoque_via_view

Linha 345: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:345>).

```python
def test_post_movimenta_estoque_via_view(self):
```

Cenario descrito pelo nome: post movimenta estoque via view.

**Chamadas utilizadas no corpo:** `cadastrar_estoque`, `estoque.refresh_from_db`, `reverse`, `self.assertContains`, `self.assertEqual`, `self.assertRedirects`, `self.client.force_login`, `self.client.get`, `self.client.post`.


## accounts/test_fluxo_requisitos.py

Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

Original: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py>).

**Dependencias importadas:**

```python
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse
from .forms import CadastroUsuarioForm
from .models import ConsentimentoLGPD, Notificacao, PedidoSangue, Triagem, Usuario
from .triagem_servico import atualizar_tipo_sanguineo_do_usuario
from .validacao_hemocentro import aprovar_hemocentro
from .validacao_pedido import aprovar_pedido, criar_pedido_pendente
```

### FluxoCadastroTriagemPedidosTests

Linha 18: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:18>).

Classe; herda de: TestCase.

### FluxoCadastroTriagemPedidosTests.usuario

Linha 19: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:19>).

```python
def usuario(self, email, perfil, **extras):
```

**Chamadas utilizadas no corpo:** `Usuario.objects.create_user`, `extras.pop`, `perfil.title`.

**Expressoes de retorno (dependem do caminho):**

- `Usuario.objects.create_user(email=email, password='SenhaForte123!', nome=extras.pop('nome', perfil.title()), perfil=perfil, **extras)`

**Onde aparece uma chamada com este nome:**

- `FluxoCadastroTriagemPedidosTests.setUp` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:28>).

### FluxoCadastroTriagemPedidosTests.setUp

Linha 28: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:28>).

```python
def setUp(self):
```

**Chamadas utilizadas no corpo:** `aprovar_hemocentro`, `self.hemocentro.refresh_from_db`, `self.usuario`.

**Onde aparece uma chamada com este nome:**

- `RegistrarMovimentacaoEstoqueTests.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:176>).

### FluxoCadastroTriagemPedidosTests.dados_solicitacao

Linha 57: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:57>).

```python
def dados_solicitacao(self):
```

**Expressoes de retorno (dependem do caminho):**

- `{'nome_solicitante': 'Pessoa solicitante', 'contato': 'solicitante@elo.test', 'para_quem': PedidoSangue.ParaQuem.MIM, 'hemocentro_destino': self.hemocentro.pk, 'titulo': 'Necessidade de sangue', 'tipo_sanguineo': 'O-', 'urgencia': PedidoSangue.Urgencia.MEDIA, 'cidade': 'Belo Horizonte', 'nome_paciente': 'Paciente', 'descricao': 'Necessidade de doadores para atendimento hospitalar.', 'justificativa_urgencia': '', 'informacoes_complementares': 'Retorno pelo contato informado.'}`

**Onde aparece uma chamada com este nome:**

- `FluxoCadastroTriagemPedidosTests.test_solicitacao_nao_publica_e_hemocentro_publica` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:230>).
- `FluxoCadastroTriagemPedidosTests.test_receptor_acompanha_somente_suas_solicitacoes` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:277>).
- `FluxoCadastroTriagemPedidosTests.test_publicacao_notifica_somente_doador_apto_compativel` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:323>).

### FluxoCadastroTriagemPedidosTests.test_cadastro_nao_permite_admin_e_exige_consentimento

Linha 77: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:77>).

```python
def test_cadastro_nao_permite_admin_e_exige_consentimento(self):
```

Cenario descrito pelo nome: cadastro nao permite admin e exige consentimento.

**Chamadas utilizadas no corpo:** `CadastroUsuarioForm`, `Usuario.objects.filter`, `Usuario.objects.filter(email='nova@elo.test').exists`, `dict`, `reverse`, `self.assertEqual`, `self.assertFalse`, `self.assertNotIn`, `self.client.post`.

### FluxoCadastroTriagemPedidosTests.test_cadastro_valido_grava_senha_hash_e_consentimento

Linha 104: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:104>).

```python
def test_cadastro_valido_grava_senha_hash_e_consentimento(self):
```

Cenario descrito pelo nome: cadastro valido grava senha hash e consentimento.

**Chamadas utilizadas no corpo:** `ConsentimentoLGPD.objects.filter`, `ConsentimentoLGPD.objects.filter(usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL, aceito=True).exists`, `Usuario.objects.get`, `reverse`, `self.assertNotEqual`, `self.assertRedirects`, `self.assertTrue`, `self.client.post`, `usuario.check_password`.

### FluxoCadastroTriagemPedidosTests.test_cadastro_de_hemocentro_inicia_pendente_e_nao_libera_estoque

Linha 144: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:144>).

```python
def test_cadastro_de_hemocentro_inicia_pendente_e_nao_libera_estoque(self):
```

Cenario descrito pelo nome: cadastro de hemocentro inicia pendente e nao libera estoque.

**Chamadas utilizadas no corpo:** `Usuario.objects.get`, `reverse`, `self.assertEqual`, `self.assertRedirects`, `self.client.get`, `self.client.post`.

### FluxoCadastroTriagemPedidosTests.test_login_bloqueia_conta_suspensa

Linha 182: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:182>).

```python
def test_login_bloqueia_conta_suspensa(self):
```

Cenario descrito pelo nome: login bloqueia conta suspensa.

**Chamadas utilizadas no corpo:** `reverse`, `self.assertEqual`, `self.assertNotIn`, `self.client.post`, `self.doador.save`.

### FluxoCadastroTriagemPedidosTests.test_triagem_exige_aceite_explicito

Linha 200: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:200>).

```python
def test_triagem_exige_aceite_explicito(self):
```

Cenario descrito pelo nome: triagem exige aceite explicito.

**Chamadas utilizadas no corpo:** `ConsentimentoLGPD.objects.filter`, `ConsentimentoLGPD.objects.filter(usuario=self.doador, tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM).exists`, `Triagem.objects.filter`, `Triagem.objects.filter(usuario=self.doador).exists`, `reverse`, `self.assertEqual`, `self.assertFalse`, `self.assertTrue`, `self.client.force_login`, `self.client.post`.

### FluxoCadastroTriagemPedidosTests.test_solicitacao_nao_publica_e_hemocentro_publica

Linha 230: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:230>).

```python
def test_solicitacao_nao_publica_e_hemocentro_publica(self):
```

Cenario descrito pelo nome: solicitacao nao publica e hemocentro publica.

**Chamadas utilizadas no corpo:** `PedidoSangue.objects.get`, `aprovar_pedido`, `pedido.refresh_from_db`, `reverse`, `self.assertEqual`, `self.assertRaises`, `self.client.force_login`, `self.client.post`, `self.dados_solicitacao`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### FluxoCadastroTriagemPedidosTests.test_observador_pode_solicitar_mas_nao_analisar

Linha 268: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:268>).

```python
def test_observador_pode_solicitar_mas_nao_analisar(self):
```

Cenario descrito pelo nome: observador pode solicitar mas nao analisar.

**Chamadas utilizadas no corpo:** `reverse`, `self.assertEqual`, `self.client.force_login`, `self.client.get`.

### FluxoCadastroTriagemPedidosTests.test_receptor_acompanha_somente_suas_solicitacoes

Linha 277: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:277>).

```python
def test_receptor_acompanha_somente_suas_solicitacoes(self):
```

Cenario descrito pelo nome: receptor acompanha somente suas solicitacoes.

**Chamadas utilizadas no corpo:** `criar_pedido_pendente`, `reverse`, `self.assertContains`, `self.assertNotContains`, `self.client.force_login`, `self.client.get`, `self.dados_solicitacao`, `str`.

### FluxoCadastroTriagemPedidosTests.test_tipo_sanguineo_confirmado_nao_e_sobrescrito_pela_triagem

Linha 295: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:295>).

```python
def test_tipo_sanguineo_confirmado_nao_e_sobrescrito_pela_triagem(self):
```

Cenario descrito pelo nome: tipo sanguineo confirmado nao e sobrescrito pela triagem.

**Chamadas utilizadas no corpo:** `Triagem.objects.create`, `atualizar_tipo_sanguineo_do_usuario`, `self.assertEqual`, `self.doador.refresh_from_db`, `self.doador.save`.

### FluxoCadastroTriagemPedidosTests.test_publicacao_notifica_somente_doador_apto_compativel

Linha 323: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:323>).

```python
def test_publicacao_notifica_somente_doador_apto_compativel(self):
```

Cenario descrito pelo nome: publicacao notifica somente doador apto compativel.

**Chamadas utilizadas no corpo:** `Notificacao.objects.filter`, `Notificacao.objects.filter(usuario=self.doador, pedido=pedido, tipo=Notificacao.Tipo.PEDIDO_COMPATIVEL).exists`, `Triagem.objects.create`, `aprovar_pedido`, `atualizar_preferencia_convocacao`, `criar_pedido_pendente`, `self.assertTrue`, `self.dados_solicitacao`, `self.doador.save`.

### ConvocacaoCompatibilidadeTests

Linha 355: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:355>).

Classe; herda de: TestCase.

### ConvocacaoCompatibilidadeTests.setUpTestData

Linha 357: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:357>).

```python
def setUpTestData(cls):
```

**Decoradores:** `classmethod`.

**Chamadas utilizadas no corpo:** `Estoque.objects.create`, `PedidoSangue.objects.create`, `Usuario.objects.create_user`.

### ConvocacaoCompatibilidadeTests.doador

Linha 371: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:371>).

```python
def doador(self, nome, **extras):
```

**Chamadas utilizadas no corpo:** `ConsentimentoLGPD.objects.create`, `Triagem.objects.create`, `Usuario.objects.create_user`, `extras.pop`.

**Expressoes de retorno (dependem do caminho):**

- `usuario`

**Onde aparece uma chamada com este nome:**

- `ConvocacaoCompatibilidadeTests.test_ambos_fluxos_exigem_todos_os_criterios` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:390>).
- `ConvocacaoCompatibilidadeTests.test_limite_soma_estoque_e_pedido_mesmo_depois_de_lido` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:420>).
- `ConvocacaoCompatibilidadeTests.test_pedido_pendente_nao_convoca` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:431>).
- `ConvocacaoCompatibilidadeTests.test_atualizacao_de_estoque_convoca_somente_quando_critico` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:436>).
- `ConvocacaoCompatibilidadeTests.test_preferencia_no_painel_registra_aceite_e_revogacao` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:458>).
- `ConvocacaoCompatibilidadeTests.test_publicacao_alternativa_tambem_convoca` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:501>).
- `ConvocacaoCompatibilidadeTests.test_compatibilidade_seleciona_os_tipos_da_tabela` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:513>).
- `ConvocacaoCompatibilidadeTests.test_limite_e_compartilhado_tambem_quando_pedido_vem_primeiro` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:522>).
- `ConvocacaoCompatibilidadeTests.test_limite_configuravel_nao_remove_protecao_contra_duplicatas` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:527>).

### ConvocacaoCompatibilidadeTests.emitir

Linha 381: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:381>).

```python
def emitir(self, origem):
```

**Chamadas utilizadas no corpo:** `criar_notificacoes_para_doadores_compativeis`, `criar_notificacoes_para_pedido`.

**Expressoes de retorno (dependem do caminho):**

- `criar_notificacoes_para_doadores_compativeis(estoque=self.estoque, status_calculado=Estoque.StatusCalculado.CRITICO)`
- `criar_notificacoes_para_pedido(pedido=self.pedido)`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `ConvocacaoCompatibilidadeTests.test_ambos_fluxos_exigem_todos_os_criterios` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:390>).
- `ConvocacaoCompatibilidadeTests.test_limite_soma_estoque_e_pedido_mesmo_depois_de_lido` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:420>).
- `ConvocacaoCompatibilidadeTests.test_pedido_pendente_nao_convoca` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:431>).
- `ConvocacaoCompatibilidadeTests.test_preferencia_no_painel_registra_aceite_e_revogacao` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:458>).
- `ConvocacaoCompatibilidadeTests.test_limite_e_compartilhado_tambem_quando_pedido_vem_primeiro` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:522>).
- `ConvocacaoCompatibilidadeTests.test_limite_configuravel_nao_remove_protecao_contra_duplicatas` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:527>).

### ConvocacaoCompatibilidadeTests.test_ambos_fluxos_exigem_todos_os_criterios

Linha 390: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:390>).

```python
def test_ambos_fluxos_exigem_todos_os_criterios(self):
```

Cenario descrito pelo nome: ambos fluxos exigem todos os criterios.

**Chamadas utilizadas no corpo:** `Notificacao.objects.all`, `Notificacao.objects.all().delete`, `Notificacao.objects.values_list`, `Triagem.objects.create`, `futuro.triagens.update`, `list`, `recusou.consentimentos_lgpd.update`, `revogado.consentimentos_lgpd.update`, `self.assertEqual`, `self.doador`, `self.emitir`, `self.subTest`, `sem_consentimento.consentimentos_lgpd.all`, `sem_consentimento.consentimentos_lgpd.all().delete`, `sem_triagem.triagens.all`, `sem_triagem.triagens.all().delete`, `timedelta`, `timezone.localdate`, `timezone.now`, `versao_antiga.consentimentos_lgpd.update`.

**Estrutura de controle:** For: 1, With: 1. Abra o original para seguir as condicoes na ordem.

### ConvocacaoCompatibilidadeTests.test_limite_soma_estoque_e_pedido_mesmo_depois_de_lido

Linha 420: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:420>).

```python
def test_limite_soma_estoque_e_pedido_mesmo_depois_de_lido(self):
```

Cenario descrito pelo nome: limite soma estoque e pedido mesmo depois de lido.

**Chamadas utilizadas no corpo:** `Notificacao.objects.update`, `self.assertEqual`, `self.doador`, `self.emitir`, `timedelta`, `timezone.now`.

### ConvocacaoCompatibilidadeTests.test_pedido_pendente_nao_convoca

Linha 431: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:431>).

```python
def test_pedido_pendente_nao_convoca(self):
```

Cenario descrito pelo nome: pedido pendente nao convoca.

**Chamadas utilizadas no corpo:** `self.assertEqual`, `self.doador`, `self.emitir`.

### ConvocacaoCompatibilidadeTests.test_atualizacao_de_estoque_convoca_somente_quando_critico

Linha 436: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:436>).

```python
def test_atualizacao_de_estoque_convoca_somente_quando_critico(self):
```

Cenario descrito pelo nome: atualizacao de estoque convoca somente quando critico.

**Chamadas utilizadas no corpo:** `Notificacao.objects.count`, `Notificacao.objects.get`, `int`, `registrar_movimentacao_estoque`, `self.assertEqual`, `self.doador`, `self.estoque.refresh_from_db`, `self.subTest`.

**Estrutura de controle:** For: 1, With: 1. Abra o original para seguir as condicoes na ordem.

### ConvocacaoCompatibilidadeTests.test_preferencia_no_painel_registra_aceite_e_revogacao

Linha 458: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:458>).

```python
def test_preferencia_no_painel_registra_aceite_e_revogacao(self):
```

Cenario descrito pelo nome: preferencia no painel registra aceite e revogacao.

**Chamadas utilizadas no corpo:** `AuditoriaAcaoCritica.objects.filter`, `AuditoriaAcaoCritica.objects.filter(metadados__evento='PREFERENCIA_CONVOCACAO').exists`, `Notificacao.objects.all`, `Notificacao.objects.all().delete`, `consentimento.refresh_from_db`, `reverse`, `self.assertContains`, `self.assertEqual`, `self.assertFalse`, `self.assertIsNone`, `self.assertIsNotNone`, `self.assertTrue`, `self.client.force_login`, `self.client.get`, `self.client.post`, `self.doador`, `self.emitir`, `usuario.consentimentos_lgpd.all`, `usuario.consentimentos_lgpd.all().delete`, `usuario.consentimentos_lgpd.get`, `usuario.refresh_from_db`.

### ConvocacaoCompatibilidadeTests.test_outro_perfil_nao_altera_preferencia

Linha 480: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:480>).

```python
def test_outro_perfil_nao_altera_preferencia(self):
```

Cenario descrito pelo nome: outro perfil nao altera preferencia.

**Chamadas utilizadas no corpo:** `Usuario.objects.create_user`, `reverse`, `self.assertEqual`, `self.assertFalse`, `self.client.force_login`, `self.client.post`, `usuario.consentimentos_lgpd.filter`, `usuario.consentimentos_lgpd.filter(tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES).exists`.

### ConvocacaoCompatibilidadeTests.test_cadastro_autorizacao_e_opcional_e_explicita

Linha 487: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:487>).

```python
def test_cadastro_autorizacao_e_opcional_e_explicita(self):
```

Cenario descrito pelo nome: cadastro autorizacao e opcional e explicita.

**Chamadas utilizadas no corpo:** `Usuario.objects.get`, `int`, `reverse`, `self.assertEqual`, `self.client.logout`, `self.client.post`, `self.subTest`, `usuario.consentimentos_lgpd.get`.

**Estrutura de controle:** For: 1, With: 1, If: 1. Abra o original para seguir as condicoes na ordem.

### ConvocacaoCompatibilidadeTests.test_publicacao_alternativa_tambem_convoca

Linha 501: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:501>).

```python
def test_publicacao_alternativa_tambem_convoca(self):
```

Cenario descrito pelo nome: publicacao alternativa tambem convoca.

**Chamadas utilizadas no corpo:** `Notificacao.objects.filter`, `Notificacao.objects.filter(pedido=pedido).exists`, `PedidoSangueForm`, `form.is_valid`, `publicar_pedido`, `self.assertTrue`, `self.doador`.

### ConvocacaoCompatibilidadeTests.test_compatibilidade_seleciona_os_tipos_da_tabela

Linha 513: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:513>).

```python
def test_compatibilidade_seleciona_os_tipos_da_tabela(self):
```

Cenario descrito pelo nome: compatibilidade seleciona os tipos da tabela.

**Chamadas utilizadas no corpo:** `COMPATIBILIDADE_RECEBIMENTO.items`, `doadores_aptos_para_convocacao`, `doadores_aptos_para_convocacao(solicitado).values_list`, `enumerate`, `self.assertEqual`, `self.doador`, `self.subTest`, `set`.

**Estrutura de controle:** For: 2, With: 1. Abra o original para seguir as condicoes na ordem.

### ConvocacaoCompatibilidadeTests.test_limite_e_compartilhado_tambem_quando_pedido_vem_primeiro

Linha 522: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:522>).

```python
def test_limite_e_compartilhado_tambem_quando_pedido_vem_primeiro(self):
```

Cenario descrito pelo nome: limite e compartilhado tambem quando pedido vem primeiro.

**Chamadas utilizadas no corpo:** `self.assertEqual`, `self.doador`, `self.emitir`.

### ConvocacaoCompatibilidadeTests.test_limite_configuravel_nao_remove_protecao_contra_duplicatas

Linha 527: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:527>).

```python
def test_limite_configuravel_nao_remove_protecao_contra_duplicatas(self):
```

Cenario descrito pelo nome: limite configuravel nao remove protecao contra duplicatas.

**Chamadas utilizadas no corpo:** `override_settings`, `self.assertEqual`, `self.doador`, `self.emitir`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### CentralNotificacoesTests

Linha 537: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:537>).

Classe; herda de: TestCase.

### CentralNotificacoesTests.setUp

Linha 538: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:538>).

```python
def setUp(self):
```

**Chamadas utilizadas no corpo:** `Notificacao.objects.create`, `Usuario.objects.create_user`, `reverse`, `self.client.force_login`.

**Onde aparece uma chamada com este nome:**

- `RegistrarMovimentacaoEstoqueTests.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:176>).

### CentralNotificacoesTests.test_leitura_persiste_sem_apagar_historico_nem_regravar_data

Linha 552: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:552>).

```python
def test_leitura_persiste_sem_apagar_historico_nem_regravar_data(self):
```

Cenario descrito pelo nome: leitura persiste sem apagar historico nem regravar data.

**Chamadas utilizadas no corpo:** `self.assertContains`, `self.assertEqual`, `self.assertIsNotNone`, `self.assertTrue`, `self.aviso.refresh_from_db`, `self.client.get`, `self.client.post`.

### CentralNotificacoesTests.test_nao_permite_marcar_notificacao_de_outro_usuario

Linha 568: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:568>).

```python
def test_nao_permite_marcar_notificacao_de_outro_usuario(self):
```

Cenario descrito pelo nome: nao permite marcar notificacao de outro usuario.

**Chamadas utilizadas no corpo:** `Notificacao.objects.create`, `aviso.refresh_from_db`, `self.assertEqual`, `self.assertFalse`, `self.assertNotContains`, `self.client.get`, `self.client.post`.

### CentralNotificacoesTests.test_historico_paginado_mostra_notificacoes_mais_antigas

Linha 577: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:577>).

```python
def test_historico_paginado_mostra_notificacoes_mais_antigas(self):
```

Cenario descrito pelo nome: historico paginado mostra notificacoes mais antigas.

**Chamadas utilizadas no corpo:** `Notificacao.objects.create`, `len`, `range`, `self.assertContains`, `self.assertEqual`, `self.client.get`.

**Estrutura de controle:** For: 1. Abra o original para seguir as condicoes na ordem.

### CentralNotificacoesTests.test_identificador_invalido_e_anonimo_nao_marcam_leitura

Linha 585: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:585>).

```python
def test_identificador_invalido_e_anonimo_nao_marcam_leitura(self):
```

Cenario descrito pelo nome: identificador invalido e anonimo nao marcam leitura.

**Chamadas utilizadas no corpo:** `self.assertEqual`, `self.assertFalse`, `self.aviso.refresh_from_db`, `self.client.logout`, `self.client.post`.


## accounts/test_pedidos.py

Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

Original: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py>).

**Dependencias importadas:**

```python
from django.test import TestCase
from django.urls import reverse
from .forms import PedidoSangueForm
from .models import PedidoSangue, Usuario, ValidacaoPedido
from .validacao_hemocentro import aprovar_hemocentro
from .validacao_pedido import aprovar_pedido, criar_pedido_pendente, marcar_pedido_suspeito
```

### PedidoSangueTests

Linha 10: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:10>).

Classe; herda de: TestCase.

### PedidoSangueTests.criar_usuario

Linha 11: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:11>).

```python
def criar_usuario(self, *, email, nome, perfil, cidade='', estado=''):
```

**Chamadas utilizadas no corpo:** `Usuario.objects.create_user`.

**Expressoes de retorno (dependem do caminho):**

- `Usuario.objects.create_user(email=email, password='SenhaForte123!', nome=nome, perfil=perfil, cidade=cidade, estado=estado)`

**Onde aparece uma chamada com este nome:**

- `EstoqueTestsBase.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:42>).
- `RegistrarMovimentacaoEstoqueTests.test_outro_hemocentro_nao_pode_movimentar_estoque_alheio` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:288>).
- `PedidoSangueTests.setUp` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:21>).
- `VisualizacaoPublicaTests.setUp` em [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:23>).
- `ValidacaoHemocentroTests.setUp` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:64>).
- `ValidacaoHemocentroTests.test_usuario_comum_nao_pode_validar` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:156>).
- `ValidacaoHemocentroTests.test_usuario_comum_nao_acessa_tela_de_validacao` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:300>).

### PedidoSangueTests.setUp

Linha 21: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:21>).

```python
def setUp(self):
```

**Chamadas utilizadas no corpo:** `aprovar_hemocentro`, `self.criar_usuario`, `self.hemocentro.refresh_from_db`.

**Onde aparece uma chamada com este nome:**

- `RegistrarMovimentacaoEstoqueTests.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:176>).

### PedidoSangueTests.dados_validos

Linha 58: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:58>).

```python
def dados_validos(self, **alteracoes):
```

**Chamadas utilizadas no corpo:** `dados.update`.

**Expressoes de retorno (dependem do caminho):**

- `dados`

**Onde aparece uma chamada com este nome:**

- `PedidoSangueTests.test_receptor_cria_solicitacao_enviada` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:88>).
- `PedidoSangueTests.test_doador_nao_pode_enviar_solicitacao` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:105>).
- `PedidoSangueTests.test_formulario_rejeita_descricao_curta` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:116>).
- `PedidoSangueTests.test_formulario_exige_email_no_contato` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:122>).
- `PedidoSangueTests.test_formulario_rejeita_hemocentro_pendente` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:138>).
- `PedidoSangueTests.test_urgencia_critica_exige_justificativa` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:148>).
- `PedidoSangueTests.test_hemocentro_aprova_pedido_e_registra_historico` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:159>).
- `PedidoSangueTests.test_admin_moderar_pedido_nao_publica` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:181>).
- `PedidoSangueTests.test_publicacao_exclusiva_do_hemocentro_responsavel` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:228>).
- `PedidoSangueTests.test_auditoria_distingue_validacao_e_publicacao` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:256>).
- `PedidoSangueTests.test_tentativa_de_publicacao_alheia_persiste_na_auditoria` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:273>).

### PedidoSangueTests.test_formulario_lista_apenas_hemocentros_aprovados

Linha 78: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:78>).

```python
def test_formulario_lista_apenas_hemocentros_aprovados(self):
```

Cenario descrito pelo nome: formulario lista apenas hemocentros aprovados.

**Chamadas utilizadas no corpo:** `PedidoSangueForm`, `list`, `self.assertEqual`, `self.assertIn`.

### PedidoSangueTests.test_receptor_cria_solicitacao_enviada

Linha 88: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:88>).

```python
def test_receptor_cria_solicitacao_enviada(self):
```

Cenario descrito pelo nome: receptor cria solicitacao enviada.

**Chamadas utilizadas no corpo:** `PedidoSangue.objects.get`, `reverse`, `self.assertEqual`, `self.assertRedirects`, `self.client.force_login`, `self.client.post`, `self.dados_validos`.

### PedidoSangueTests.test_doador_nao_pode_enviar_solicitacao

Linha 105: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:105>).

```python
def test_doador_nao_pode_enviar_solicitacao(self):
```

Cenario descrito pelo nome: doador nao pode enviar solicitacao.

**Chamadas utilizadas no corpo:** `PedidoSangue.objects.exists`, `reverse`, `self.assertFalse`, `self.assertRedirects`, `self.client.force_login`, `self.client.post`, `self.dados_validos`.

### PedidoSangueTests.test_visitante_precisa_entrar

Linha 111: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:111>).

```python
def test_visitante_precisa_entrar(self):
```

Cenario descrito pelo nome: visitante precisa entrar.

**Chamadas utilizadas no corpo:** `reverse`, `self.assertRedirects`, `self.client.get`.

### PedidoSangueTests.test_formulario_rejeita_descricao_curta

Linha 116: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:116>).

```python
def test_formulario_rejeita_descricao_curta(self):
```

Cenario descrito pelo nome: formulario rejeita descricao curta.

**Chamadas utilizadas no corpo:** `PedidoSangueForm`, `form.is_valid`, `self.assertFalse`, `self.assertIn`, `self.dados_validos`.

### PedidoSangueTests.test_formulario_exige_email_no_contato

Linha 122: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:122>).

```python
def test_formulario_exige_email_no_contato(self):
```

Cenario descrito pelo nome: formulario exige email no contato.

**Chamadas utilizadas no corpo:** `PedidoSangueForm`, `form_invalido.is_valid`, `form_valido.is_valid`, `self.assertEqual`, `self.assertFalse`, `self.assertIn`, `self.assertTrue`, `self.dados_validos`.

### PedidoSangueTests.test_formulario_rejeita_hemocentro_pendente

Linha 138: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:138>).

```python
def test_formulario_rejeita_hemocentro_pendente(self):
```

Cenario descrito pelo nome: formulario rejeita hemocentro pendente.

**Chamadas utilizadas no corpo:** `PedidoSangueForm`, `form.is_valid`, `self.assertFalse`, `self.assertIn`, `self.dados_validos`.

### PedidoSangueTests.test_urgencia_critica_exige_justificativa

Linha 148: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:148>).

```python
def test_urgencia_critica_exige_justificativa(self):
```

Cenario descrito pelo nome: urgencia critica exige justificativa.

**Chamadas utilizadas no corpo:** `PedidoSangueForm`, `form.is_valid`, `self.assertFalse`, `self.assertIn`, `self.dados_validos`.

### PedidoSangueTests.test_hemocentro_aprova_pedido_e_registra_historico

Linha 159: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:159>).

```python
def test_hemocentro_aprova_pedido_e_registra_historico(self):
```

Cenario descrito pelo nome: hemocentro aprova pedido e registra historico.

**Chamadas utilizadas no corpo:** `PedidoSangue.objects.get`, `aprovar_pedido`, `pedido.refresh_from_db`, `pedido.validacoes.count`, `reverse`, `self.assertEqual`, `self.client.force_login`, `self.client.post`, `self.dados_validos`.

### PedidoSangueTests.test_admin_moderar_pedido_nao_publica

Linha 181: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:181>).

```python
def test_admin_moderar_pedido_nao_publica(self):
```

Cenario descrito pelo nome: admin moderar pedido nao publica.

**Chamadas utilizadas no corpo:** `criar_pedido_pendente`, `pedido.refresh_from_db`, `pedido.validacoes.latest`, `reverse`, `self.assertContains`, `self.assertEqual`, `self.assertFalse`, `self.assertRedirects`, `self.client.force_login`, `self.client.get`, `self.client.post`, `self.dados_validos`, `str`.

### PedidoSangueTests.test_hemocentro_nao_acessa_moderacao_administrativa

Linha 219: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:219>).

```python
def test_hemocentro_nao_acessa_moderacao_administrativa(self):
```

Cenario descrito pelo nome: hemocentro nao acessa moderacao administrativa.

**Chamadas utilizadas no corpo:** `reverse`, `self.assertEqual`, `self.client.force_login`, `self.client.get`.

### PedidoSangueTests.test_publicacao_exclusiva_do_hemocentro_responsavel

Linha 228: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:228>).

```python
def test_publicacao_exclusiva_do_hemocentro_responsavel(self):
```

Cenario descrito pelo nome: publicacao exclusiva do hemocentro responsavel.

**Chamadas utilizadas no corpo:** `PedidoSangue.objects.get`, `aprovar_pedido`, `pedido.refresh_from_db`, `reverse`, `self.assertContains`, `self.assertEqual`, `self.assertNotContains`, `self.assertRaises`, `self.client.force_login`, `self.client.get`, `self.client.post`, `self.dados_validos`, `self.hemocentro_pendente.save`.

**Estrutura de controle:** With: 2. Abra o original para seguir as condicoes na ordem.

### PedidoSangueTests.test_permissao_do_servico_de_publicacao

Linha 249: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:249>).

```python
def test_permissao_do_servico_de_publicacao(self):
```

Cenario descrito pelo nome: permissao do servico de publicacao.

**Chamadas utilizadas no corpo:** `pode_publicar_pedido`, `self.assertFalse`, `self.assertTrue`, `self.subTest`.

**Estrutura de controle:** For: 1, With: 1. Abra o original para seguir as condicoes na ordem.

### PedidoSangueTests.test_auditoria_distingue_validacao_e_publicacao

Linha 256: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:256>).

```python
def test_auditoria_distingue_validacao_e_publicacao(self):
```

Cenario descrito pelo nome: auditoria distingue validacao e publicacao.

**Chamadas utilizadas no corpo:** `AuditoriaAcaoCritica.objects.filter`, `AuditoriaAcaoCritica.objects.filter(alvo_tipo='accounts.PedidoSangue').latest`, `PedidoSangue.objects.get`, `aprovar_pedido`, `marcar_pedido_suspeito`, `reverse`, `self.assertEqual`, `self.assertNotIn`, `self.client.force_login`, `self.client.post`, `self.dados_validos`, `str`.

### PedidoSangueTests.test_tentativa_de_publicacao_alheia_persiste_na_auditoria

Linha 273: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:273>).

```python
def test_tentativa_de_publicacao_alheia_persiste_na_auditoria(self):
```

Cenario descrito pelo nome: tentativa de publicacao alheia persiste na auditoria.

**Chamadas utilizadas no corpo:** `AuditoriaAcaoCritica.objects.filter`, `AuditoriaAcaoCritica.objects.filter(usuario=self.hemocentro_pendente).latest`, `PedidoSangue.objects.get`, `pedido.refresh_from_db`, `reverse`, `self.assertEqual`, `self.client.force_login`, `self.client.post`, `self.dados_validos`, `self.hemocentro_pendente.save`.


## accounts/test_perfis_teste.py

Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

Original: [accounts/test_perfis_teste.py](<C:/Users/lb119/Elo/accounts/test_perfis_teste.py>).

**Dependencias importadas:**

```python
from io import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from .compatibilidade import doadores_aptos_para_convocacao
from .models import ConsentimentoLGPD, Triagem, Usuario
```

### PerfisTesteTests

Linha 12: [accounts/test_perfis_teste.py](<C:/Users/lb119/Elo/accounts/test_perfis_teste.py:12>).

Classe; herda de: TestCase.

**Decoradores:** `override_settings(DEBUG=True)`.

### PerfisTesteTests.test_cria_perfis_e_preserva_alteracoes_ao_repetir

Linha 13: [accounts/test_perfis_teste.py](<C:/Users/lb119/Elo/accounts/test_perfis_teste.py:13>).

```python
def test_cria_perfis_e_preserva_alteracoes_ao_repetir(self):
```

Cenario descrito pelo nome: cria perfis e preserva alteracoes ao repetir.

**Chamadas utilizadas no corpo:** `ConsentimentoLGPD.objects.count`, `StringIO`, `Triagem.objects.count`, `Usuario.objects.count`, `Usuario.objects.get`, `Usuario.objects.values_list`, `call_command`, `doadores_aptos_para_convocacao`, `doadores_aptos_para_convocacao('O-').values_list`, `list`, `self.assertEqual`, `self.assertTrue`, `set`, `usuario.check_password`, `usuario.refresh_from_db`, `usuario.save`, `usuario.set_password`.

### PerfisTesteTests.test_nao_cria_contas_fora_do_ambiente_de_desenvolvimento

Linha 33: [accounts/test_perfis_teste.py](<C:/Users/lb119/Elo/accounts/test_perfis_teste.py:33>).

```python
def test_nao_cria_contas_fora_do_ambiente_de_desenvolvimento(self):
```

Cenario descrito pelo nome: nao cria contas fora do ambiente de desenvolvimento.

**Decoradores:** `override_settings(DEBUG=False)`.

**Chamadas utilizadas no corpo:** `StringIO`, `Usuario.objects.exists`, `call_command`, `self.assertFalse`, `self.assertRaises`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.


## accounts/test_triagem.py

Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

Original: [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py>).

**Dependencias importadas:**

```python
from datetime import date
from django.test import TestCase
from django.urls import reverse
from .models import ConsentimentoLGPD, RespostaTriagem, Triagem, Usuario
from .triagem import calcular_resultado
```

### TriagemExtensaTests

Linha 25: [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:25>).

Classe; herda de: TestCase.

**Explicacao presente no codigo:**

> Testa o cálculo e o salvamento da triagem inicial.

### TriagemExtensaTests.criar_doador

Linha 30: [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:30>).

```python
def criar_doador(self):
```

**Explicacao presente no codigo:**

> Cria um usuário Doador para os testes.

**Chamadas utilizadas no corpo:** `Usuario.objects.create_user`.

**Expressoes de retorno (dependem do caminho):**

- `Usuario.objects.create_user(email='doador@teste.com', password='SenhaForte123!', nome='Doador Teste', perfil=Usuario.Perfil.DOADOR)`

**Onde aparece uma chamada com este nome:**

- `TriagemExtensaTests.test_post_inicia_triagem_e_consentimento` em [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:88>).

### TriagemExtensaTests.dados_sem_impedimento

Linha 42: [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:42>).

```python
def dados_sem_impedimento(self):
```

**Explicacao presente no codigo:**

> Retorna respostas básicas sem impedimento inicial.

**Expressoes de retorno (dependem do caminho):**

- `{'entende_orientacao': 'SIM', 'idade': '18_60', 'peso': '56_129_9', 'sexo_biologico': 'MASCULINO', 'ja_doou': 'NAO'}`

**Onde aparece uma chamada com este nome:**

- `TriagemExtensaTests.test_peso_abaixo_de_50_gera_inaptidao_temporaria` em [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:55>).
- `TriagemExtensaTests.test_respostas_basicas_sem_impedimento` em [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:73>).

### TriagemExtensaTests.test_peso_abaixo_de_50_gera_inaptidao_temporaria

Linha 55: [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:55>).

```python
def test_peso_abaixo_de_50_gera_inaptidao_temporaria(self):
```

Cenario descrito pelo nome: peso abaixo de 50 gera inaptidao temporaria.

**Explicacao presente no codigo:**

> Peso abaixo de 50 kg deve gerar resultado temporário.

**Chamadas utilizadas no corpo:** `calcular_resultado`, `date`, `self.assertEqual`, `self.dados_sem_impedimento`.

### TriagemExtensaTests.test_respostas_basicas_sem_impedimento

Linha 73: [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:73>).

```python
def test_respostas_basicas_sem_impedimento(self):
```

Cenario descrito pelo nome: respostas basicas sem impedimento.

**Explicacao presente no codigo:**

> Respostas básicas devem gerar orientação sem impedimento identificado.

**Chamadas utilizadas no corpo:** `calcular_resultado`, `date`, `self.assertEqual`, `self.dados_sem_impedimento`.

### TriagemExtensaTests.test_post_inicia_triagem_e_consentimento

Linha 88: [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:88>).

```python
def test_post_inicia_triagem_e_consentimento(self):
```

Cenario descrito pelo nome: post inicia triagem e consentimento.

**Explicacao presente no codigo:**

> O clique inicial cria a triagem e o consentimento versionado.

**Chamadas utilizadas no corpo:** `ConsentimentoLGPD.objects.filter`, `ConsentimentoLGPD.objects.filter(usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM).exists`, `RespostaTriagem.objects.filter`, `RespostaTriagem.objects.filter(triagem=triagem).count`, `Triagem.objects.get`, `reverse`, `self.assertEqual`, `self.assertRedirects`, `self.assertTrue`, `self.client.force_login`, `self.client.post`, `self.criar_doador`.

### TriagemExtensaTests.test_usuario_nao_doador_nao_acessa_triagem

Linha 135: [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:135>).

```python
def test_usuario_nao_doador_nao_acessa_triagem(self):
```

Cenario descrito pelo nome: usuario nao doador nao acessa triagem.

**Explicacao presente no codigo:**

> A primeira versão da triagem só aceita usuários Doador.

**Chamadas utilizadas no corpo:** `Usuario.objects.create_user`, `reverse`, `self.assertEqual`, `self.client.force_login`, `self.client.post`.

### TriagemExtensaTests.test_receptor_nao_pode_acessar_a_triagem

Linha 159: [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:159>).

```python
def test_receptor_nao_pode_acessar_a_triagem(self):
```

Cenario descrito pelo nome: receptor nao pode acessar a triagem.

**Explicacao presente no codigo:**

> Receptor nao pode responder a triagem para doacao.

**Chamadas utilizadas no corpo:** `Usuario.objects.create_user`, `reverse`, `self.assertEqual`, `self.client.force_login`, `self.client.post`.

### TriagemExtensaTests.test_visitante_pode_ver_apresentacao_da_triagem

Linha 186: [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:186>).

```python
def test_visitante_pode_ver_apresentacao_da_triagem(self):
```

Cenario descrito pelo nome: visitante pode ver apresentacao da triagem.

**Explicacao presente no codigo:**

> Visitante pode conhecer a triagem sem estar autenticado.

**Chamadas utilizadas no corpo:** `reverse`, `self.assertContains`, `self.assertEqual`, `self.client.get`.


## accounts/test_triagem_catalogos.py

Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

Original: [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py>).

**Dependencias importadas:**

```python
from django.test import SimpleTestCase
from .triagem_catalogo import PERGUNTAS_EXTENSAS, PERGUNTAS_SIMPLIFICADAS, todas_as_perguntas, validar_catalogos
```

### CatalogosTriagemTests

Linha 32: [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py:32>).

Classe; herda de: SimpleTestCase.

**Explicacao presente no codigo:**

> Valida a estrutura consumida pelo formulário, serviço e motor.

### CatalogosTriagemTests.test_catalogo_extenso_possui_todas_as_56_entradas

Linha 35: [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py:35>).

```python
def test_catalogo_extenso_possui_todas_as_56_entradas(self):
```

Cenario descrito pelo nome: catalogo extenso possui todas as 56 entradas.

**Explicacao presente no codigo:**

> Falha se qualquer pergunta extensa da especificação for omitida.

**Chamadas utilizadas no corpo:** `self.assertEqual`, `set`.

### CatalogosTriagemTests.test_catalogo_simplificado_possui_todas_as_18_entradas

Linha 40: [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py:40>).

```python
def test_catalogo_simplificado_possui_todas_as_18_entradas(self):
```

Cenario descrito pelo nome: catalogo simplificado possui todas as 18 entradas.

**Explicacao presente no codigo:**

> Falha se a versão rápida ficar incompleta.

**Chamadas utilizadas no corpo:** `self.assertEqual`, `set`.

### CatalogosTriagemTests.test_perguntas_possuem_conteudo_e_rastreabilidade

Linha 45: [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py:45>).

```python
def test_perguntas_possuem_conteudo_e_rastreabilidade(self):
```

Cenario descrito pelo nome: perguntas possuem conteudo e rastreabilidade.

**Explicacao presente no codigo:**

> Falha se uma pergunta não puder ser exibida ou auditada.

**Chamadas utilizadas no corpo:** `self.assertEqual`, `self.assertTrue`, `todas_as_perguntas`.

**Estrutura de controle:** For: 1, If: 1. Abra o original para seguir as condicoes na ordem.

### CatalogosTriagemTests.test_codigos_de_opcao_nao_se_repetem_na_mesma_pergunta

Linha 62: [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py:62>).

```python
def test_codigos_de_opcao_nao_se_repetem_na_mesma_pergunta(self):
```

Cenario descrito pelo nome: codigos de opcao nao se repetem na mesma pergunta.

**Explicacao presente no codigo:**

> Falha se dois rótulos diferentes forem salvos com o mesmo código.

**Chamadas utilizadas no corpo:** `len`, `self.assertEqual`, `set`, `todas_as_perguntas`.

**Estrutura de controle:** For: 1. Abra o original para seguir as condicoes na ordem.

### CatalogosTriagemTests.test_destinos_da_simplificada_existem_no_catalogo_extenso

Linha 69: [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py:69>).

```python
def test_destinos_da_simplificada_existem_no_catalogo_extenso(self):
```

Cenario descrito pelo nome: destinos da simplificada existem no catalogo extenso.

**Explicacao presente no codigo:**

> Falha se a versão rápida tentar abrir uma pergunta inexistente.

**Chamadas utilizadas no corpo:** `PERGUNTAS_SIMPLIFICADAS.values`, `pergunta['abrir_extensa'].values`, `self.assertIn`.

**Estrutura de controle:** For: 3. Abra o original para seguir as condicoes na ordem.

### CatalogosTriagemTests.test_funcao_de_validacao_aceita_os_catalogos_oficiais

Linha 77: [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py:77>).

```python
def test_funcao_de_validacao_aceita_os_catalogos_oficiais(self):
```

Cenario descrito pelo nome: funcao de validacao aceita os catalogos oficiais.

**Explicacao presente no codigo:**

> Falha se o catálogo publicado violar seu próprio contrato.

**Chamadas utilizadas no corpo:** `self.assertIsNone`, `validar_catalogos`.

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `IDS_EXTENSOS`: linha 13; valor declarado em [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py:13>).
- `IDS_SIMPLIFICADOS`: linha 26; valor declarado em [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py:26>).

## accounts/test_triagem_forms.py

Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

Original: [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py>).

**Dependencias importadas:**

```python
from django.test import SimpleTestCase
from .triagem_catalogo import obter_pergunta
from .triagem_forms import FormularioPergunta
```

### FormularioPerguntaTests

Linha 9: [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:9>).

Classe; herda de: SimpleTestCase.

**Explicacao presente no codigo:**

> Protege a normalização usada para salvar respostas estruturadas.

### FormularioPerguntaTests.test_escolha_com_data_e_normalizada

Linha 12: [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:12>).

```python
def test_escolha_com_data_e_normalizada(self):
```

Cenario descrito pelo nome: escolha com data e normalizada.

**Explicacao presente no codigo:**

> Falha se a data da alternativa não chegar ao motor com seu código.

**Chamadas utilizadas no corpo:** `FormularioPergunta`, `form.is_valid`, `obter_pergunta`, `self.assertEqual`, `self.assertTrue`.

### FormularioPerguntaTests.test_selecao_multipla_preserva_uma_data_por_item

Linha 33: [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:33>).

```python
def test_selecao_multipla_preserva_uma_data_por_item(self):
```

Cenario descrito pelo nome: selecao multipla preserva uma data por item.

**Explicacao presente no codigo:**

> Falha se duas vacinas diferentes compartilharem uma única data.

**Chamadas utilizadas no corpo:** `FormularioPergunta`, `form.is_valid`, `obter_pergunta`, `self.assertEqual`, `self.assertTrue`.

### FormularioPerguntaTests.test_data_futura_e_rejeitada

Linha 54: [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:54>).

```python
def test_data_futura_e_rejeitada(self):
```

Cenario descrito pelo nome: data futura e rejeitada.

**Explicacao presente no codigo:**

> Falha se uma data impossível produzir prazo de liberação.

**Chamadas utilizadas no corpo:** `FormularioPergunta`, `form.is_valid`, `obter_pergunta`, `self.assertFalse`, `self.assertIn`.

### FormularioPerguntaTests.test_alternativa_com_prazo_exige_sua_data

Linha 68: [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:68>).

```python
def test_alternativa_com_prazo_exige_sua_data(self):
```

Cenario descrito pelo nome: alternativa com prazo exige sua data.

**Explicacao presente no codigo:**

> Falha se uma vacina sem data for aceita pelo formulário.

**Chamadas utilizadas no corpo:** `FormularioPergunta`, `form.is_valid`, `obter_pergunta`, `self.assertFalse`, `self.assertIn`.

### FormularioPerguntaTests.test_nenhuma_nao_pode_ser_marcada_com_uma_condicao

Linha 79: [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:79>).

```python
def test_nenhuma_nao_pode_ser_marcada_com_uma_condicao(self):
```

Cenario descrito pelo nome: nenhuma nao pode ser marcada com uma condicao.

**Explicacao presente no codigo:**

> Falha se uma resposta contraditória for persistida.

**Chamadas utilizadas no corpo:** `FormularioPergunta`, `form.is_valid`, `obter_pergunta`, `self.assertFalse`, `self.assertIn`.

### FormularioPerguntaTests.test_descricao_e_obrigatoria_quando_usuario_informa_outra_condicao

Linha 92: [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:92>).

```python
def test_descricao_e_obrigatoria_quando_usuario_informa_outra_condicao(self):
```

Cenario descrito pelo nome: descricao e obrigatoria quando usuario informa outra condicao.

**Explicacao presente no codigo:**

> Falha se EXT-50 aceitar uma condição sem qualquer descrição.

**Chamadas utilizadas no corpo:** `FormularioPergunta`, `form.is_valid`, `obter_pergunta`, `self.assertFalse`, `self.assertIn`.

### FormularioPerguntaTests.test_procedimento_estetico_registra_seguranca_e_inflamacao

Linha 103: [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:103>).

```python
def test_procedimento_estetico_registra_seguranca_e_inflamacao(self):
```

Cenario descrito pelo nome: procedimento estetico registra seguranca e inflamacao.

**Explicacao presente no codigo:**

> Falha se os fatores que alteram o prazo estético forem perdidos.

**Chamadas utilizadas no corpo:** `FormularioPergunta`, `form.is_valid`, `obter_pergunta`, `self.assertEqual`, `self.assertTrue`.


## accounts/test_triagem_models.py

Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

Original: [accounts/test_triagem_models.py](<C:/Users/lb119/Elo/accounts/test_triagem_models.py>).

**Dependencias importadas:**

```python
from django.db import IntegrityError, transaction
from django.test import TestCase
from .models import RespostaTriagem, Triagem, Usuario
```

### TriagemModelTests

Linha 9: [accounts/test_triagem_models.py](<C:/Users/lb119/Elo/accounts/test_triagem_models.py:9>).

Classe; herda de: TestCase.

**Explicacao presente no codigo:**

> Garante que andamento e correções sejam persistidos sem duplicação.

### TriagemModelTests.setUp

Linha 12: [accounts/test_triagem_models.py](<C:/Users/lb119/Elo/accounts/test_triagem_models.py:12>).

```python
def setUp(self):
```

**Chamadas utilizadas no corpo:** `Usuario.objects.create_user`.

**Onde aparece uma chamada com este nome:**

- `RegistrarMovimentacaoEstoqueTests.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:176>).

### TriagemModelTests.test_nova_triagem_comeca_em_andamento

Linha 21: [accounts/test_triagem_models.py](<C:/Users/lb119/Elo/accounts/test_triagem_models.py:21>).

```python
def test_nova_triagem_comeca_em_andamento(self):
```

Cenario descrito pelo nome: nova triagem comeca em andamento.

**Explicacao presente no codigo:**

> Falha se uma triagem nova nascer como concluída ou sem fluxo vazio.

**Chamadas utilizadas no corpo:** `Triagem.objects.create`, `self.assertEqual`.

### TriagemModelTests.test_uma_pergunta_tem_uma_unica_resposta_por_triagem

Linha 37: [accounts/test_triagem_models.py](<C:/Users/lb119/Elo/accounts/test_triagem_models.py:37>).

```python
def test_uma_pergunta_tem_uma_unica_resposta_por_triagem(self):
```

Cenario descrito pelo nome: uma pergunta tem uma unica resposta por triagem.

**Explicacao presente no codigo:**

> Falha se a mesma pergunta puder gerar respostas concorrentes.

**Chamadas utilizadas no corpo:** `RespostaTriagem.objects.create`, `Triagem.objects.create`, `self.assertRaises`, `transaction.atomic`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### TriagemModelTests.test_triagem_simplificada_pode_apontar_para_extensa_base

Linha 62: [accounts/test_triagem_models.py](<C:/Users/lb119/Elo/accounts/test_triagem_models.py:62>).

```python
def test_triagem_simplificada_pode_apontar_para_extensa_base(self):
```

Cenario descrito pelo nome: triagem simplificada pode apontar para extensa base.

**Explicacao presente no codigo:**

> Falha se a checagem rápida perder a extensa usada como referência.

**Chamadas utilizadas no corpo:** `Triagem.objects.create`, `extensa.verificacoes_simplificadas.all`, `self.assertEqual`, `self.assertIn`.


## accounts/test_triagem_motor.py

Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

Original: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py>).

**Dependencias importadas:**

```python
from datetime import date
from django.test import SimpleTestCase
from .models import Triagem
from .triagem_motor import avaliar_triagem
```

### MotorTriagemTests

Linha 20: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:20>).

Classe; herda de: SimpleTestCase.

**Explicacao presente no codigo:**

> Exercita regras reais sem depender de banco, view ou formulário.

### MotorTriagemTests.test_resultado_prioriza_definitiva_e_preserva_todos_os_achados

Linha 23: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:23>).

```python
def test_resultado_prioriza_definitiva_e_preserva_todos_os_achados(self):
```

Cenario descrito pelo nome: resultado prioriza definitiva e preserva todos os achados.

**Explicacao presente no codigo:**

> Falha se o motor parar no primeiro impedimento ou usar prioridade errada.

**Chamadas utilizadas no corpo:** `avaliar_triagem`, `date`, `len`, `self.assertEqual`.

### MotorTriagemTests.test_resultado_usa_a_maior_data_temporaria

Linha 42: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:42>).

```python
def test_resultado_usa_a_maior_data_temporaria(self):
```

Cenario descrito pelo nome: resultado usa a maior data temporaria.

**Explicacao presente no codigo:**

> Falha se um prazo curto esconder uma espera mais longa.

**Chamadas utilizadas no corpo:** `avaliar_triagem`, `date`, `self.assertEqual`.

### MotorTriagemTests.test_prazo_em_meses_respeita_o_calendario

Linha 65: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:65>).

```python
def test_prazo_em_meses_respeita_o_calendario(self):
```

Cenario descrito pelo nome: prazo em meses respeita o calendario.

**Explicacao presente no codigo:**

> Falha se um mês for tratado sempre como trinta dias.

**Chamadas utilizadas no corpo:** `avaliar_triagem`, `date`, `self.assertEqual`.

### MotorTriagemTests.test_regra_com_prazo_sem_data_exige_avaliacao

Linha 84: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:84>).

```python
def test_regra_com_prazo_sem_data_exige_avaliacao(self):
```

Cenario descrito pelo nome: regra com prazo sem data exige avaliacao.

**Explicacao presente no codigo:**

> Falha se o motor inventar a data de uma vacina não datada.

**Chamadas utilizadas no corpo:** `avaliar_triagem`, `date`, `self.assertEqual`, `self.assertIsNone`.

### MotorTriagemTests.test_estetica_sem_seguranca_usa_doze_meses

Linha 99: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:99>).

```python
def test_estetica_sem_seguranca_usa_doze_meses(self):
```

Cenario descrito pelo nome: estetica sem seguranca usa doze meses.

**Explicacao presente no codigo:**

> Falha se um procedimento inseguro receber apenas o prazo de três dias.

**Chamadas utilizadas no corpo:** `avaliar_triagem`, `date`, `self.assertEqual`.

### MotorTriagemTests.test_estetica_com_inflamacao_exige_avaliacao

Linha 120: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:120>).

```python
def test_estetica_com_inflamacao_exige_avaliacao(self):
```

Cenario descrito pelo nome: estetica com inflamacao exige avaliacao.

**Explicacao presente no codigo:**

> Falha se uma complicação estética for tratada como recuperação simples.

**Chamadas utilizadas no corpo:** `avaliar_triagem`, `date`, `self.assertEqual`.

### MotorTriagemTests.test_ultima_doacao_calcula_intervalo_feminino

Linha 141: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:141>).

```python
def test_ultima_doacao_calcula_intervalo_feminino(self):
```

Cenario descrito pelo nome: ultima doacao calcula intervalo feminino.

**Explicacao presente no codigo:**

> Falha se o intervalo feminino não usar noventa dias.

**Chamadas utilizadas no corpo:** `avaliar_triagem`, `date`, `self.assertEqual`.

### MotorTriagemTests.test_ultima_doacao_acima_de_60_usa_seis_meses

Linha 162: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:162>).

```python
def test_ultima_doacao_acima_de_60_usa_seis_meses(self):
```

Cenario descrito pelo nome: ultima doacao acima de 60 usa seis meses.

**Explicacao presente no codigo:**

> Falha se a regra especial de 61 a 69 anos for ignorada.

**Chamadas utilizadas no corpo:** `avaliar_triagem`, `date`, `self.assertEqual`.

### MotorTriagemTests.test_limite_anual_sem_datas_nao_inventa_liberacao

Linha 183: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:183>).

```python
def test_limite_anual_sem_datas_nao_inventa_liberacao(self):
```

Cenario descrito pelo nome: limite anual sem datas nao inventa liberacao.

**Explicacao presente no codigo:**

> Falha se somente a contagem gerar uma data fictícia.

**Chamadas utilizadas no corpo:** `avaliar_triagem`, `date`, `self.assertEqual`, `self.assertIsNone`.

### MotorTriagemTests.test_simplificada_reutiliza_doenca_estavel_da_extensa

Linha 201: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:201>).

```python
def test_simplificada_reutiliza_doenca_estavel_da_extensa(self):
```

Cenario descrito pelo nome: simplificada reutiliza doenca estavel da extensa.

**Explicacao presente no codigo:**

> Falha se uma condição permanente salva for esquecida na versão rápida.

**Chamadas utilizadas no corpo:** `avaliar_triagem`, `date`, `self.assertEqual`.

### MotorTriagemTests.test_simplificada_nao_reutiliza_estado_de_saude_antigo

Linha 218: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:218>).

```python
def test_simplificada_nao_reutiliza_estado_de_saude_antigo(self):
```

Cenario descrito pelo nome: simplificada nao reutiliza estado de saude antigo.

**Explicacao presente no codigo:**

> Falha se uma febre antiga for tratada como estado atual sem nova resposta.

**Chamadas utilizadas no corpo:** `avaliar_triagem`, `date`, `self.assertEqual`.

### MotorTriagemTests.test_resultado_sem_achados_mantem_aviso_presencial

Linha 235: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:235>).

```python
def test_resultado_sem_achados_mantem_aviso_presencial(self):
```

Cenario descrito pelo nome: resultado sem achados mantem aviso presencial.

**Explicacao presente no codigo:**

> Falha se a mensagem declarar que a pessoa está apta.

**Chamadas utilizadas no corpo:** `avaliar_triagem`, `calculo['mensagem'].lower`, `date`, `self.assertEqual`, `self.assertIn`, `self.assertNotIn`.


## accounts/test_triagem_servico.py

Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

Original: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py>).

**Dependencias importadas:**

```python
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from .models import ConsentimentoLGPD, RespostaTriagem, Triagem, Usuario
from .triagem_catalogo import obter_pergunta
from .triagem_servico import TriagemConcluida, TriagemExtensaNecessaria, TriagemSimplificadaIndisponivel, concluir_triagem, iniciar_triagem, obter_pergunta_atual, salvar_resposta, voltar_pergunta
```

### TriagemServicoTests

Linha 29: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:29>).

Classe; herda de: TestCase.

**Explicacao presente no codigo:**

> Protege transições de estado e vínculos entre as duas modalidades.

### TriagemServicoTests.setUp

Linha 32: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:32>).

```python
def setUp(self):
```

**Chamadas utilizadas no corpo:** `Usuario.objects.create_user`.

**Onde aparece uma chamada com este nome:**

- `RegistrarMovimentacaoEstoqueTests.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:176>).

### TriagemServicoTests.test_inicio_extenso_cria_fluxo_e_consentimento

Linha 40: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:40>).

```python
def test_inicio_extenso_cria_fluxo_e_consentimento(self):
```

Cenario descrito pelo nome: inicio extenso cria fluxo e consentimento.

**Explicacao presente no codigo:**

> Falha se uma triagem começar sem pergunta ou sem aceite versionado.

**Chamadas utilizadas no corpo:** `ConsentimentoLGPD.objects.filter`, `ConsentimentoLGPD.objects.filter(usuario=self.usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM, versao_termo='HEMOMINAS_2026_08', aceito=True).exists`, `iniciar_triagem`, `self.assertEqual`, `self.assertTrue`.

### TriagemServicoTests.test_inicio_reutiliza_triagem_em_andamento

Linha 64: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:64>).

```python
def test_inicio_reutiliza_triagem_em_andamento(self):
```

Cenario descrito pelo nome: inicio reutiliza triagem em andamento.

**Explicacao presente no codigo:**

> Falha se cada clique em iniciar criar um histórico vazio duplicado.

**Chamadas utilizadas no corpo:** `iniciar_triagem`, `self.assertEqual`, `self.usuario.triagens.count`.

### TriagemServicoTests.test_nova_extensa_pode_reutilizar_respostas_concluidas

Linha 81: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:81>).

```python
def test_nova_extensa_pode_reutilizar_respostas_concluidas(self):
```

Cenario descrito pelo nome: nova extensa pode reutilizar respostas concluidas.

**Explicacao presente no codigo:**

> Copia respostas sem alterar a triagem concluída original.

**Chamadas utilizadas no corpo:** `RespostaTriagem.objects.create`, `Triagem.objects.create`, `iniciar_triagem`, `nova.respostas.get`, `obter_pergunta`, `origem.respostas.count`, `self.assertEqual`, `self.assertNotEqual`.

### TriagemServicoTests.test_simplificada_exige_extensa_concluida_do_mesmo_usuario

Linha 116: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:116>).

```python
def test_simplificada_exige_extensa_concluida_do_mesmo_usuario(self):
```

Cenario descrito pelo nome: simplificada exige extensa concluida do mesmo usuario.

**Explicacao presente no codigo:**

> Falha se a versão rápida puder ser usada sem histórico completo.

**Chamadas utilizadas no corpo:** `iniciar_triagem`, `self.assertRaises`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### TriagemServicoTests.test_simplificada_registra_a_extensa_base

Linha 126: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:126>).

```python
def test_simplificada_registra_a_extensa_base(self):
```

Cenario descrito pelo nome: simplificada registra a extensa base.

**Explicacao presente no codigo:**

> Falha se o resultado rápido perder a origem das respostas reutilizadas.

**Chamadas utilizadas no corpo:** `Triagem.objects.create`, `iniciar_triagem`, `self.assertEqual`.

### TriagemServicoTests.test_observador_nao_pode_iniciar_questionario

Linha 145: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:145>).

```python
def test_observador_nao_pode_iniciar_questionario(self):
```

Cenario descrito pelo nome: observador nao pode iniciar questionario.

**Explicacao presente no codigo:**

> Falha se um perfil fora de Doador responder à triagem.

**Chamadas utilizadas no corpo:** `Usuario.objects.create_user`, `iniciar_triagem`, `self.assertRaises`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### TriagemServicoTests.test_corrigir_resposta_substitui_sem_duplicar

Linha 162: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:162>).

```python
def test_corrigir_resposta_substitui_sem_duplicar(self):
```

Cenario descrito pelo nome: corrigir resposta substitui sem duplicar.

**Explicacao presente no codigo:**

> Falha se voltar e corrigir criar duas respostas para EXT-01.

**Chamadas utilizadas no corpo:** `iniciar_triagem`, `salvar_resposta`, `self.assertEqual`, `triagem.respostas.count`, `triagem.respostas.get`, `voltar_pergunta`.

### TriagemServicoTests.test_resposta_simplificada_insere_bloco_extenso_sem_duplicar

Linha 188: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:188>).

```python
def test_resposta_simplificada_insere_bloco_extenso_sem_duplicar(self):
```

Cenario descrito pelo nome: resposta simplificada insere bloco extenso sem duplicar.

**Explicacao presente no codigo:**

> Falha se uma mudança estética não abrir todas as perguntas detalhadas.

**Chamadas utilizadas no corpo:** `Triagem.objects.create`, `iniciar_triagem`, `obter_pergunta_atual`, `respostas_ate_sim_10.items`, `salvar_resposta`, `self.assertEqual`, `self.assertLess`, `simplificada.fluxo_perguntas.count`, `simplificada.fluxo_perguntas.index`.

**Estrutura de controle:** For: 2. Abra o original para seguir as condicoes na ordem.

### TriagemServicoTests.test_conclusao_salva_resultado_e_bloqueia_nova_resposta

Linha 237: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:237>).

```python
def test_conclusao_salva_resultado_e_bloqueia_nova_resposta(self):
```

Cenario descrito pelo nome: conclusao salva resultado e bloqueia nova resposta.

**Explicacao presente no codigo:**

> Falha se uma triagem concluída puder ser reescrita.

**Chamadas utilizadas no corpo:** `RespostaTriagem.objects.create`, `concluir_triagem`, `iniciar_triagem`, `next`, `obter_pergunta`, `salvar_resposta`, `self.assertEqual`, `self.assertRaises`, `self.assertTrue`, `triagem.refresh_from_db`.

**Estrutura de controle:** For: 1, With: 1. Abra o original para seguir as condicoes na ordem.

### TriagemServicoTests.test_resposta_mantem_campos_legados_e_valor_completo

Linha 296: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:296>).

```python
def test_resposta_mantem_campos_legados_e_valor_completo(self):
```

Cenario descrito pelo nome: resposta mantem campos legados e valor completo.

**Explicacao presente no codigo:**

> Falha se o admin antigo ou o novo motor perderem dados.

**Chamadas utilizadas no corpo:** `RespostaTriagem.objects.get`, `iniciar_triagem`, `salvar_resposta`, `self.assertEqual`.

### TriagemServicoTests.test_nao_entendeu_permanece_na_primeira_pergunta

Linha 318: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:318>).

```python
def test_nao_entendeu_permanece_na_primeira_pergunta(self):
```

Cenario descrito pelo nome: nao entendeu permanece na primeira pergunta.

**Explicacao presente no codigo:**

> Falha se EXT-01=NAO avançar sem repetir a explicação.

**Chamadas utilizadas no corpo:** `iniciar_triagem`, `salvar_resposta`, `self.assertEqual`.

### TriagemServicoTests.test_revisar_confirmacao_extensa_volta_ao_inicio

Linha 335: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:335>).

```python
def test_revisar_confirmacao_extensa_volta_ao_inicio(self):
```

Cenario descrito pelo nome: revisar confirmacao extensa volta ao inicio.

**Explicacao presente no codigo:**

> Falha se EXT-51=REVISAR não permitir conferir as respostas.

**Chamadas utilizadas no corpo:** `iniciar_triagem`, `salvar_resposta`, `self.assertEqual`, `triagem.fluxo_perguntas.index`, `triagem.save`.

### TriagemServicoTests.test_resumo_incorreto_cancela_rapida_e_exige_extensa

Linha 354: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:354>).

```python
def test_resumo_incorreto_cancela_rapida_e_exige_extensa(self):
```

Cenario descrito pelo nome: resumo incorreto cancela rapida e exige extensa.

**Explicacao presente no codigo:**

> Falha se dados antigos incorretos continuarem na versão rápida.

**Chamadas utilizadas no corpo:** `Triagem.objects.create`, `iniciar_triagem`, `salvar_resposta`, `self.assertEqual`, `self.assertRaises`, `simplificada.refresh_from_db`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### TriagemServicoTests.test_correcao_remove_resposta_de_subpergunta_oculta

Linha 383: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:383>).

```python
def test_correcao_remove_resposta_de_subpergunta_oculta(self):
```

Cenario descrito pelo nome: correcao remove resposta de subpergunta oculta.

**Explicacao presente no codigo:**

> Falha se uma resposta escondida continuar alterando o resultado.

**Chamadas utilizadas no corpo:** `iniciar_triagem`, `salvar_resposta`, `self.assertFalse`, `self.assertNotIn`, `triagem.respostas.filter`, `triagem.respostas.filter(id_pergunta='EXT-05A').exists`.

### TriagemServicoTests.test_rapida_respeita_condicoes_das_perguntas_detalhadas

Linha 418: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:418>).

```python
def test_rapida_respeita_condicoes_das_perguntas_detalhadas(self):
```

Cenario descrito pelo nome: rapida respeita condicoes das perguntas detalhadas.

**Explicacao presente no codigo:**

> Falha se a rápida mostrar data de doação antes de confirmar doação.

**Chamadas utilizadas no corpo:** `Triagem.objects.create`, `iniciar_triagem`, `salvar_resposta`, `self.assertIn`, `self.assertNotIn`.


## accounts/test_triagem_views.py

Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

Original: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py>).

**Dependencias importadas:**

```python
from django.test import TestCase
from django.urls import reverse
from .models import RespostaTriagem, Triagem, Usuario
from .triagem_catalogo import obter_pergunta
```

### TriagemViewsTests

Linha 18: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:18>).

Classe; herda de: TestCase.

**Explicacao presente no codigo:**

> Protege navegação, permissões e privacidade do histórico.

### TriagemViewsTests.setUpTestData

Linha 22: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:22>).

```python
def setUpTestData(cls):
```

**Decoradores:** `classmethod`.

**Chamadas utilizadas no corpo:** `Usuario.objects.create_user`.

### TriagemViewsTests._criar_extensa_concluida

Linha 42: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:42>).

```python
def _criar_extensa_concluida(self, usuario=None):
```

**Explicacao presente no codigo:**

> Cria somente o pré-requisito necessário para a versão rápida.

**Chamadas utilizadas no corpo:** `Triagem.objects.create`.

**Expressoes de retorno (dependem do caminho):**

- `Triagem.objects.create(usuario=usuario or self.doador, modalidade=Triagem.Modalidade.EXTENSA, status=Triagem.Status.CONCLUIDA, resultado=Triagem.Resultado.SEM_IMPEDIMENTO)`

**Onde aparece uma chamada com este nome:**

- `TriagemViewsTests.test_apresentacao_oferece_reutilizar_extensa_concluida` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:149>).
- `TriagemViewsTests.test_resumo_incorreto_abre_nova_extensa` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:329>).
- `TriagemViewsTests.test_historico_lista_somente_triagens_do_usuario` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:363>).
- `TriagemViewsTests.test_receptor_bloqueado_inclusive_triagem_antiga` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:389>).

### TriagemViewsTests._iniciar_pela_rota

Linha 52: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:52>).

```python
def _iniciar_pela_rota(self, modalidade='extensa', usuario=None):
```

**Explicacao presente no codigo:**

> Autentica e inicia uma modalidade usando a mesma rota da página.

**Chamadas utilizadas no corpo:** `reverse`, `self.client.force_login`, `self.client.post`.

**Expressoes de retorno (dependem do caminho):**

- `self.client.post(reverse('accounts:triagem_iniciar', kwargs={'modalidade': modalidade}), {'aceite_termo': 'on'})`

**Onde aparece uma chamada com este nome:**

- `TriagemViewsTests.test_doador_pode_iniciar_extensa` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:134>).
- `TriagemViewsTests.test_observador_nao_pode_iniciar` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:162>).
- `TriagemViewsTests.test_simplificada_exige_extensa_anterior` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:170>).
- `TriagemViewsTests.test_pagina_mostra_uma_pergunta_e_salva_resposta` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:186>).
- `TriagemViewsTests.test_salvar_e_sair_conserva_andamento` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:214>).
- `TriagemViewsTests.test_botao_anterior_retorna_sem_apagar_resposta` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:234>).
- `TriagemViewsTests.test_resultado_em_andamento_volta_para_pergunta` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:277>).
- `TriagemViewsTests.test_confirmacao_final_conclui_e_mostra_resultado` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:295>).
- `TriagemViewsTests.test_resumo_incorreto_abre_nova_extensa` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:329>).
- `TriagemViewsTests.test_receptor_bloqueado_inclusive_triagem_antiga` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:389>).

### TriagemViewsTests._preencher_ate_confirmacao

Linha 64: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:64>).

```python
def _preencher_ate_confirmacao(self, triagem):
```

**Explicacao presente no codigo:**

> Preenche respostas neutras para testar a conclusão pela view.

**Chamadas utilizadas no corpo:** `RespostaTriagem.objects.create`, `len`, `next`, `obter_pergunta`, `triagem.save`.

**Estrutura de controle:** For: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `TriagemViewsTests.test_confirmacao_final_conclui_e_mostra_resultado` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:295>).

### TriagemViewsTests.test_apresentacao_publica_mostra_texto_e_duas_modalidades

Linha 95: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:95>).

```python
def test_apresentacao_publica_mostra_texto_e_duas_modalidades(self):
```

Cenario descrito pelo nome: apresentacao publica mostra texto e duas modalidades.

**Explicacao presente no codigo:**

> Falha se o visitante não conhecer as opções antes de se cadastrar.

**Chamadas utilizadas no corpo:** `reverse`, `self.assertContains`, `self.assertEqual`, `self.client.get`.

### TriagemViewsTests.test_visitante_ve_botoes_de_acao_na_apresentacao

Linha 107: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:107>).

```python
def test_visitante_ve_botoes_de_acao_na_apresentacao(self):
```

Cenario descrito pelo nome: visitante ve botoes de acao na apresentacao.

**Explicacao presente no codigo:**

> Falha se a apresentação não oferecer ações visíveis ao visitante.

**Chamadas utilizadas no corpo:** `reverse`, `self.assertContains`, `self.assertEqual`, `self.client.get`.

### TriagemViewsTests.test_inicio_exige_post_e_login

Linha 116: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:116>).

```python
def test_inicio_exige_post_e_login(self):
```

Cenario descrito pelo nome: inicio exige post e login.

**Explicacao presente no codigo:**

> Falha se uma simples visita à URL criar registro no banco.

**Chamadas utilizadas no corpo:** `Triagem.objects.count`, `reverse`, `self.assertEqual`, `self.assertIn`, `self.client.force_login`, `self.client.get`, `self.client.post`.

### TriagemViewsTests.test_doador_pode_iniciar_extensa

Linha 134: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:134>).

```python
def test_doador_pode_iniciar_extensa(self):
```

Cenario descrito pelo nome: doador pode iniciar extensa.

**Explicacao presente no codigo:**

> Falha se um dos dois perfis autorizados não puder responder.

**Chamadas utilizadas no corpo:** `Triagem.objects.get`, `reverse`, `self._iniciar_pela_rota`, `self.assertRedirects`, `self.subTest`.

**Estrutura de controle:** For: 1, With: 1. Abra o original para seguir as condicoes na ordem.

### TriagemViewsTests.test_apresentacao_oferece_reutilizar_extensa_concluida

Linha 149: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:149>).

```python
def test_apresentacao_oferece_reutilizar_extensa_concluida(self):
```

Cenario descrito pelo nome: apresentacao oferece reutilizar extensa concluida.

**Explicacao presente no codigo:**

> A apresentação oferece o preenchimento a partir do histórico.

**Chamadas utilizadas no corpo:** `reverse`, `self._criar_extensa_concluida`, `self.assertContains`, `self.client.force_login`, `self.client.get`.

### TriagemViewsTests.test_observador_nao_pode_iniciar

Linha 162: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:162>).

```python
def test_observador_nao_pode_iniciar(self):
```

Cenario descrito pelo nome: observador nao pode iniciar.

**Explicacao presente no codigo:**

> Falha se um perfil não autorizado puder gravar dados de saúde.

**Chamadas utilizadas no corpo:** `Triagem.objects.filter`, `Triagem.objects.filter(usuario=self.observador).exists`, `self._iniciar_pela_rota`, `self.assertEqual`, `self.assertFalse`.

### TriagemViewsTests.test_simplificada_exige_extensa_anterior

Linha 170: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:170>).

```python
def test_simplificada_exige_extensa_anterior(self):
```

Cenario descrito pelo nome: simplificada exige extensa anterior.

**Explicacao presente no codigo:**

> Falha se a versão rápida for iniciada sem histórico completo.

**Chamadas utilizadas no corpo:** `Triagem.objects.filter`, `Triagem.objects.filter(usuario=self.doador, modalidade=Triagem.Modalidade.SIMPLIFICADA).exists`, `reverse`, `self._iniciar_pela_rota`, `self.assertFalse`, `self.assertRedirects`.

### TriagemViewsTests.test_pagina_mostra_uma_pergunta_e_salva_resposta

Linha 186: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:186>).

```python
def test_pagina_mostra_uma_pergunta_e_salva_resposta(self):
```

Cenario descrito pelo nome: pagina mostra uma pergunta e salva resposta.

**Explicacao presente no codigo:**

> Falha se a tela não avançar uma pergunta por vez.

**Chamadas utilizadas no corpo:** `RespostaTriagem.objects.filter`, `RespostaTriagem.objects.filter(triagem=triagem, id_pergunta='EXT-01').exists`, `Triagem.objects.get`, `reverse`, `self._iniciar_pela_rota`, `self.assertContains`, `self.assertEqual`, `self.assertRedirects`, `self.assertTrue`, `self.client.get`, `self.client.post`, `triagem.refresh_from_db`.

### TriagemViewsTests.test_salvar_e_sair_conserva_andamento

Linha 214: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:214>).

```python
def test_salvar_e_sair_conserva_andamento(self):
```

Cenario descrito pelo nome: salvar e sair conserva andamento.

**Explicacao presente no codigo:**

> Falha se a pessoa perder a resposta ao pausar a triagem.

**Chamadas utilizadas no corpo:** `Triagem.objects.get`, `reverse`, `self._iniciar_pela_rota`, `self.assertEqual`, `self.assertRedirects`, `self.client.post`, `triagem.refresh_from_db`.

### TriagemViewsTests.test_botao_anterior_retorna_sem_apagar_resposta

Linha 234: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:234>).

```python
def test_botao_anterior_retorna_sem_apagar_resposta(self):
```

Cenario descrito pelo nome: botao anterior retorna sem apagar resposta.

**Explicacao presente no codigo:**

> Falha se voltar apagar informação já salva.

**Chamadas utilizadas no corpo:** `Triagem.objects.get`, `reverse`, `self._iniciar_pela_rota`, `self.assertEqual`, `self.assertRedirects`, `self.assertTrue`, `self.client.post`, `triagem.refresh_from_db`, `triagem.respostas.filter`, `triagem.respostas.filter(id_pergunta='EXT-01').exists`.

### TriagemViewsTests.test_triagem_de_outro_usuario_retorna_404

Linha 252: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:252>).

```python
def test_triagem_de_outro_usuario_retorna_404(self):
```

Cenario descrito pelo nome: triagem de outro usuario retorna 404.

**Explicacao presente no codigo:**

> Falha se respostas de saúde puderem ser acessadas por outra conta.

**Chamadas utilizadas no corpo:** `Triagem.objects.create`, `reverse`, `self.assertEqual`, `self.client.force_login`, `self.client.get`.

### TriagemViewsTests.test_resultado_em_andamento_volta_para_pergunta

Linha 277: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:277>).

```python
def test_resultado_em_andamento_volta_para_pergunta(self):
```

Cenario descrito pelo nome: resultado em andamento volta para pergunta.

**Explicacao presente no codigo:**

> Falha se um resultado vazio for mostrado antes da confirmação.

**Chamadas utilizadas no corpo:** `Triagem.objects.get`, `reverse`, `self._iniciar_pela_rota`, `self.assertRedirects`, `self.client.get`.

### TriagemViewsTests.test_confirmacao_final_conclui_e_mostra_resultado

Linha 295: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:295>).

```python
def test_confirmacao_final_conclui_e_mostra_resultado(self):
```

Cenario descrito pelo nome: confirmacao final conclui e mostra resultado.

**Explicacao presente no codigo:**

> Falha se a última resposta não congelar a orientação calculada.

**Chamadas utilizadas no corpo:** `Triagem.objects.get`, `reverse`, `self._iniciar_pela_rota`, `self._preencher_ate_confirmacao`, `self.assertEqual`, `self.assertRedirects`, `self.client.post`, `triagem.refresh_from_db`.

### TriagemViewsTests.test_resumo_incorreto_abre_nova_extensa

Linha 329: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:329>).

```python
def test_resumo_incorreto_abre_nova_extensa(self):
```

Cenario descrito pelo nome: resumo incorreto abre nova extensa.

**Explicacao presente no codigo:**

> Falha se a rápida continuar usando um histórico declarado incorreto.

**Chamadas utilizadas no corpo:** `Triagem.objects.get`, `reverse`, `self._criar_extensa_concluida`, `self._iniciar_pela_rota`, `self.assertEqual`, `self.assertRedirects`, `self.client.post`, `simplificada.refresh_from_db`.

### TriagemViewsTests.test_historico_lista_somente_triagens_do_usuario

Linha 363: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:363>).

```python
def test_historico_lista_somente_triagens_do_usuario(self):
```

Cenario descrito pelo nome: historico lista somente triagens do usuario.

**Explicacao presente no codigo:**

> Falha se o histórico revelar registros de outra pessoa.

**Chamadas utilizadas no corpo:** `reverse`, `self._criar_extensa_concluida`, `self.assertContains`, `self.assertEqual`, `self.assertNotContains`, `self.client.force_login`, `self.client.get`.

### TriagemViewsTests.test_dashboard_doador_aponta_para_triagem

Linha 376: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:376>).

```python
def test_dashboard_doador_aponta_para_triagem(self):
```

Cenario descrito pelo nome: dashboard doador aponta para triagem.

**Explicacao presente no codigo:**

> Falha se um perfil autorizado não encontrar a triagem no painel.

**Chamadas utilizadas no corpo:** `reverse`, `self.assertContains`, `self.client.force_login`, `self.client.get`, `self.subTest`.

**Estrutura de controle:** For: 1, With: 1. Abra o original para seguir as condicoes na ordem.

### TriagemViewsTests.test_receptor_bloqueado_inclusive_triagem_antiga

Linha 389: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:389>).

```python
def test_receptor_bloqueado_inclusive_triagem_antiga(self):
```

Cenario descrito pelo nome: receptor bloqueado inclusive triagem antiga.

**Chamadas utilizadas no corpo:** `reverse`, `self._criar_extensa_concluida`, `self._iniciar_pela_rota`, `self.assertEqual`, `self.assertNotContains`, `self.client.force_login`, `self.client.get`.

**Estrutura de controle:** For: 1. Abra o original para seguir as condicoes na ordem.


## accounts/test_visualizacao.py

Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

Original: [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py>).

**Dependencias importadas:**

```python
from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .estoque import cadastrar_estoque
from .models import Estoque, PedidoSangue, Usuario
from .validacao_hemocentro import aprovar_hemocentro
```

### VisualizacaoPublicaTests

Linha 12: [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:12>).

Classe; herda de: TestCase.

### VisualizacaoPublicaTests.criar_usuario

Linha 13: [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:13>).

```python
def criar_usuario(self, *, email, nome, perfil, cidade='', estado=''):
```

**Chamadas utilizadas no corpo:** `Usuario.objects.create_user`.

**Expressoes de retorno (dependem do caminho):**

- `Usuario.objects.create_user(email=email, password='SenhaForte123!', nome=nome, perfil=perfil, cidade=cidade, estado=estado)`

**Onde aparece uma chamada com este nome:**

- `EstoqueTestsBase.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:42>).
- `RegistrarMovimentacaoEstoqueTests.test_outro_hemocentro_nao_pode_movimentar_estoque_alheio` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:288>).
- `PedidoSangueTests.setUp` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:21>).
- `VisualizacaoPublicaTests.setUp` em [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:23>).
- `ValidacaoHemocentroTests.setUp` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:64>).
- `ValidacaoHemocentroTests.test_usuario_comum_nao_pode_validar` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:156>).
- `ValidacaoHemocentroTests.test_usuario_comum_nao_acessa_tela_de_validacao` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:300>).

### VisualizacaoPublicaTests.setUp

Linha 23: [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:23>).

```python
def setUp(self):
```

**Chamadas utilizadas no corpo:** `aprovar_hemocentro`, `self.criar_usuario`, `self.hemocentro.refresh_from_db`.

**Onde aparece uma chamada com este nome:**

- `RegistrarMovimentacaoEstoqueTests.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:176>).

### VisualizacaoPublicaTests.pedido

Linha 53: [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:53>).

```python
def pedido(self, *, status, tipo='O-', urgencia='ALTA'):
```

**Chamadas utilizadas no corpo:** `PedidoSangue.objects.create`, `timezone.now`.

**Expressoes de retorno (dependem do caminho):**

- `PedidoSangue.objects.create(nome_solicitante='Solicitante', contato='solicitante@visualizacao.test', hemocentro_destino=self.hemocentro, para_quem=PedidoSangue.ParaQuem.MIM, titulo=f'Pedido urgente de sangue {tipo}', tipo_sanguineo=tipo, urgencia=urgencia, cidade='Muzambinho', descricao='Necessidade de doadores para atendimento hospitalar.', status=status, publicado_em=timezone.now() if status == PedidoSangue.Status.PUBLICADA else None)`

**Onde aparece uma chamada com este nome:**

- `VisualizacaoPublicaTests.test_consulta_de_pedidos_aplica_filtros_e_oculta_nao_publicados` em [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:74>).

### VisualizacaoPublicaTests.test_consulta_de_pedidos_aplica_filtros_e_oculta_nao_publicados

Linha 74: [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:74>).

```python
def test_consulta_de_pedidos_aplica_filtros_e_oculta_nao_publicados(self):
```

Cenario descrito pelo nome: consulta de pedidos aplica filtros e oculta nao publicados.

**Chamadas utilizadas no corpo:** `date.today`, `date.today().isoformat`, `reverse`, `self.assertContains`, `self.assertEqual`, `self.assertNotContains`, `self.client.get`, `self.pedido`.

### VisualizacaoPublicaTests.test_consulta_de_pedidos_nao_exibe_destino_nao_aprovado

Linha 111: [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:111>).

```python
def test_consulta_de_pedidos_nao_exibe_destino_nao_aprovado(self):
```

Cenario descrito pelo nome: consulta de pedidos nao exibe destino nao aprovado.

**Chamadas utilizadas no corpo:** `PedidoSangue.objects.create`, `reverse`, `self.assertNotContains`, `self.client.get`.

### VisualizacaoPublicaTests.test_consulta_de_estoques_filtra_por_tipo_situacao_e_busca

Linha 133: [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:133>).

```python
def test_consulta_de_estoques_filtra_por_tipo_situacao_e_busca(self):
```

Cenario descrito pelo nome: consulta de estoques filtra por tipo situacao e busca.

**Chamadas utilizadas no corpo:** `Estoque.objects.create`, `cadastrar_estoque`, `reverse`, `self.assertContains`, `self.assertEqual`, `self.assertNotContains`, `self.client.get`.

### VisualizacaoPublicaTests.test_consulta_de_estoques_preserva_parametros_antigos

Linha 175: [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:175>).

```python
def test_consulta_de_estoques_preserva_parametros_antigos(self):
```

Cenario descrito pelo nome: consulta de estoques preserva parametros antigos.

**Chamadas utilizadas no corpo:** `cadastrar_estoque`, `reverse`, `self.assertContains`, `self.client.get`.


## accounts/tests.py

Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

Original: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py>).

**Dependencias importadas:**

```python
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse
from .models import AuditoriaAcaoCritica, Estoque, Usuario, ValidacaoHemocentro
from .validacao_hemocentro import aprovar_hemocentro, hemocentro_aprovado, recusar_hemocentro, solicitar_correcao_hemocentro, validar_publicacao_hemocentro
```

### ValidacaoHemocentroTests

Linha 41: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:41>).

Classe; herda de: TestCase.

**Explicacao presente no codigo:**

> Testes principais do UC_07.

### ValidacaoHemocentroTests.criar_usuario

Linha 44: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:44>).

```python
def criar_usuario(self, *, email, nome, perfil, is_staff=False, is_superuser=False):
```

**Explicacao presente no codigo:**

> Cria usuario usando o manager real do projeto.

**Chamadas utilizadas no corpo:** `Usuario.objects.create_user`.

**Expressoes de retorno (dependem do caminho):**

- `Usuario.objects.create_user(email=email, password='SenhaForte123!', nome=nome, perfil=perfil, is_staff=is_staff, is_superuser=is_superuser)`

**Onde aparece uma chamada com este nome:**

- `EstoqueTestsBase.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:42>).
- `RegistrarMovimentacaoEstoqueTests.test_outro_hemocentro_nao_pode_movimentar_estoque_alheio` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:288>).
- `PedidoSangueTests.setUp` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:21>).
- `VisualizacaoPublicaTests.setUp` em [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:23>).
- `ValidacaoHemocentroTests.setUp` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:64>).
- `ValidacaoHemocentroTests.test_usuario_comum_nao_pode_validar` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:156>).
- `ValidacaoHemocentroTests.test_usuario_comum_nao_acessa_tela_de_validacao` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:300>).

### ValidacaoHemocentroTests.setUp

Linha 64: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:64>).

```python
def setUp(self):
```

**Explicacao presente no codigo:**

> Prepara um administrador e um Hemocentro para cada teste.

**Chamadas utilizadas no corpo:** `self.criar_usuario`.

**Onde aparece uma chamada com este nome:**

- `RegistrarMovimentacaoEstoqueTests.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:176>).

### ValidacaoHemocentroTests.test_hemocentro_inicia_pendente

Linha 79: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:79>).

```python
def test_hemocentro_inicia_pendente(self):
```

Cenario descrito pelo nome: hemocentro inicia pendente.

**Explicacao presente no codigo:**

> Conta de Hemocentro nova deve aguardar analise.

**Chamadas utilizadas no corpo:** `hemocentro_aprovado`, `self.assertEqual`, `self.assertFalse`.

### ValidacaoHemocentroTests.test_admin_aprova_e_cria_historico

Linha 88: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:88>).

```python
def test_admin_aprova_e_cria_historico(self):
```

Cenario descrito pelo nome: admin aprova e cria historico.

**Explicacao presente no codigo:**

> Aprovacao altera status, cria historico e gera auditoria.

**Chamadas utilizadas no corpo:** `AuditoriaAcaoCritica.objects.filter`, `AuditoriaAcaoCritica.objects.filter(acao=AuditoriaAcaoCritica.Acao.APROVACAO_HEMOCENTRO, usuario=self.admin, alvo_id=str(self.hemocentro.pk)).exists`, `ValidacaoHemocentro.objects.filter`, `ValidacaoHemocentro.objects.filter(hemocentro=self.hemocentro).count`, `aprovar_hemocentro`, `self.assertEqual`, `self.assertTrue`, `self.hemocentro.refresh_from_db`, `str`.

### ValidacaoHemocentroTests.test_admin_recusa

Linha 120: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:120>).

```python
def test_admin_recusa(self):
```

Cenario descrito pelo nome: admin recusa.

**Explicacao presente no codigo:**

> Recusa altera o status e guarda o parecer.

**Chamadas utilizadas no corpo:** `recusar_hemocentro`, `self.assertEqual`, `self.hemocentro.refresh_from_db`.

### ValidacaoHemocentroTests.test_admin_solicita_correcao

Linha 140: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:140>).

```python
def test_admin_solicita_correcao(self):
```

Cenario descrito pelo nome: admin solicita correcao.

**Explicacao presente no codigo:**

> Solicitacao de correcao coloca o cadastro em CORRECAO.

**Chamadas utilizadas no corpo:** `self.assertEqual`, `self.hemocentro.refresh_from_db`, `solicitar_correcao_hemocentro`.

### ValidacaoHemocentroTests.test_usuario_comum_nao_pode_validar

Linha 156: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:156>).

```python
def test_usuario_comum_nao_pode_validar(self):
```

Cenario descrito pelo nome: usuario comum nao pode validar.

**Explicacao presente no codigo:**

> Somente administrador pode registrar a decisao.

**Chamadas utilizadas no corpo:** `aprovar_hemocentro`, `self.assertRaises`, `self.criar_usuario`.

**Estrutura de controle:** With: 1. Abra o original para seguir as condicoes na ordem.

### ValidacaoHemocentroTests.test_hemocentro_nao_aprovado_nao_publica

Linha 171: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:171>).

```python
def test_hemocentro_nao_aprovado_nao_publica(self):
```

Cenario descrito pelo nome: hemocentro nao aprovado nao publica.

**Explicacao presente no codigo:**

> Pendente, recusado e correcao devem bloquear publicacao.

**Chamadas utilizadas no corpo:** `self.assertRaises`, `self.hemocentro.save`, `validar_publicacao_hemocentro`.

**Estrutura de controle:** For: 1, With: 1. Abra o original para seguir as condicoes na ordem.

### ValidacaoHemocentroTests.test_hemocentro_aprovado_pode_publicar

Linha 185: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:185>).

```python
def test_hemocentro_aprovado_pode_publicar(self):
```

Cenario descrito pelo nome: hemocentro aprovado pode publicar.

**Explicacao presente no codigo:**

> Status aprovado libera a regra de publicacao.

**Chamadas utilizadas no corpo:** `aprovar_hemocentro`, `self.assertTrue`, `self.hemocentro.refresh_from_db`, `validar_publicacao_hemocentro`.

### ValidacaoHemocentroTests.test_dashboard_hemocentro_mostra_status_sem_link_de_aprovacao

Linha 196: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:196>).

```python
def test_dashboard_hemocentro_mostra_status_sem_link_de_aprovacao(self):
```

Cenario descrito pelo nome: dashboard hemocentro mostra status sem link de aprovacao.

**Explicacao presente no codigo:**

> Hemocentro ve seu status, mas nao acessa validacao administrativa.

**Chamadas utilizadas no corpo:** `reverse`, `self.assertContains`, `self.assertNotContains`, `self.client.force_login`, `self.client.get`.

### ValidacaoHemocentroTests.test_admin_acessa_tela_de_validacao_e_ve_pendente

Linha 214: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:214>).

```python
def test_admin_acessa_tela_de_validacao_e_ve_pendente(self):
```

Cenario descrito pelo nome: admin acessa tela de validacao e ve pendente.

**Explicacao presente no codigo:**

> Administrador deve receber a tela da aplicacao com os pendentes.

**Chamadas utilizadas no corpo:** `reverse`, `self.assertContains`, `self.assertEqual`, `self.client.force_login`, `self.client.get`.

### ValidacaoHemocentroTests.test_admin_aprova_pelo_painel_e_libera_estoque

Linha 244: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:244>).

```python
def test_admin_aprova_pelo_painel_e_libera_estoque(self):
```

Cenario descrito pelo nome: admin aprova pelo painel e libera estoque.

**Explicacao presente no codigo:**

> A aprovacao feita na tela altera o status e libera o estoque.

**Chamadas utilizadas no corpo:** `Estoque.objects.filter`, `Estoque.objects.filter(hemocentro=self.hemocentro, tipo_sanguineo='O+').exists`, `reverse`, `self.assertContains`, `self.assertEqual`, `self.assertRedirects`, `self.assertTrue`, `self.client.force_login`, `self.client.get`, `self.client.post`, `self.hemocentro.refresh_from_db`.

### ValidacaoHemocentroTests.test_usuario_comum_nao_acessa_tela_de_validacao

Linha 300: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:300>).

```python
def test_usuario_comum_nao_acessa_tela_de_validacao(self):
```

Cenario descrito pelo nome: usuario comum nao acessa tela de validacao.

**Explicacao presente no codigo:**

> A tela e suas acoes continuam restritas ao Administrador.

**Chamadas utilizadas no corpo:** `reverse`, `self.assertEqual`, `self.client.force_login`, `self.client.get`, `self.criar_usuario`.

### ValidacaoHemocentroTests.test_dashboard_admin_nao_mostra_publicacao_de_pedido

Linha 317: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:317>).

```python
def test_dashboard_admin_nao_mostra_publicacao_de_pedido(self):
```

Cenario descrito pelo nome: dashboard admin nao mostra publicacao de pedido.

**Explicacao presente no codigo:**

> Administrador não atua como Hemocentro na publicação.

**Chamadas utilizadas no corpo:** `reverse`, `self.assertContains`, `self.assertNotContains`, `self.client.force_login`, `self.client.get`.

### AuditoriaTests

Linha 335: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:335>).

Classe; herda de: TestCase.

### AuditoriaTests.setUpTestData

Linha 337: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:337>).

```python
def setUpTestData(cls):
```

**Decoradores:** `classmethod`.

**Chamadas utilizadas no corpo:** `Usuario.objects.create_superuser`, `Usuario.objects.create_user`.

### AuditoriaTests.test_acesso_bloqueado_registrado

Linha 347: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:347>).

```python
def test_acesso_bloqueado_registrado(self):
```

Cenario descrito pelo nome: acesso bloqueado registrado.

**Chamadas utilizadas no corpo:** `AuditoriaAcaoCritica.objects.get`, `reverse`, `self.assertEqual`, `self.client.force_login`, `self.client.get`.

### AuditoriaTests.test_acesso_a_triagem_registra_alvo_sem_respostas

Linha 356: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:356>).

```python
def test_acesso_a_triagem_registra_alvo_sem_respostas(self):
```

Cenario descrito pelo nome: acesso a triagem registra alvo sem respostas.

**Chamadas utilizadas no corpo:** `AuditoriaAcaoCritica.objects.get`, `Triagem.objects.create`, `reverse`, `self.assertEqual`, `self.assertNotIn`, `self.client.force_login`, `self.client.get`, `str`.

### AuditoriaTests.test_auditoria_exclusiva_administrador_e_somente_leitura

Linha 369: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:369>).

```python
def test_auditoria_exclusiva_administrador_e_somente_leitura(self):
```

Cenario descrito pelo nome: auditoria exclusiva administrador e somente leitura.

**Chamadas utilizadas no corpo:** `Permission.objects.get`, `RequestFactory`, `RequestFactory().get`, `Usuario.objects.get`, `modelo_admin.has_add_permission`, `modelo_admin.has_change_permission`, `modelo_admin.has_delete_permission`, `modelo_admin.has_module_permission`, `modelo_admin.has_view_permission`, `self.assertFalse`, `self.assertTrue`, `self.doador.save`, `self.doador.user_permissions.add`.

### AuditoriaTests.test_suspensao_registrada_sem_duplicar_dados_pessoais

Linha 387: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:387>).

```python
def test_suspensao_registrada_sem_duplicar_dados_pessoais(self):
```

Cenario descrito pelo nome: suspensao registrada sem duplicar dados pessoais.

**Chamadas utilizadas no corpo:** `AuditoriaAcaoCritica.objects.get`, `RequestFactory`, `RequestFactory().post`, `admin.site._registry[Usuario].save_model`, `self.assertEqual`, `self.assertIn`, `self.assertNotIn`, `str`.

### AuditoriaTests.test_login_suspeito_nao_afirma_bloqueio

Linha 401: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:401>).

```python
def test_login_suspeito_nao_afirma_bloqueio(self):
```

Cenario descrito pelo nome: login suspeito nao afirma bloqueio.

**Chamadas utilizadas no corpo:** `AuditoriaAcaoCritica.objects.get`, `RequestFactory`, `RequestFactory().post`, `auditar_login_falho`, `range`, `self.assertEqual`, `self.assertNotIn`, `str`.

**Estrutura de controle:** For: 1. Abra o original para seguir as condicoes na ordem.

### AuditoriaTests.test_sanitizacao_recursiva

Linha 411: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:411>).

```python
def test_sanitizacao_recursiva(self):
```

Cenario descrito pelo nome: sanitizacao recursiva.

**Chamadas utilizadas no corpo:** `registrar_auditoria`, `self.assertEqual`, `self.assertNotIn`, `str`.

### AuditoriaTests.test_ip_nao_confia_em_cabecalho_do_cliente

Linha 418: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:418>).

```python
def test_ip_nao_confia_em_cabecalho_do_cliente(self):
```

Cenario descrito pelo nome: ip nao confia em cabecalho do cliente.

**Chamadas utilizadas no corpo:** `RequestFactory`, `RequestFactory().get`, `obter_ip`, `self.assertEqual`, `self.assertIsNone`.


## accounts/triagem.py

Calculos iniciais da triagem; compare seus chamadores ao motor atual.

Original: [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py>).

**Dependencias importadas:**

```python
from datetime import date, timedelta
from .models import Triagem
```

### adicionar_achado

Linha 128: [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py:128>).

```python
def adicionar_achado(achados, codigo, resultado, mensagem, data_liberacao=None):
```

**Explicacao presente no codigo:**

> Adiciona um impedimento ou alerta sem apagar achados anteriores.

**Chamadas utilizadas no corpo:** `achados.append`, `data_liberacao.isoformat`.

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `calcular_resultado` em [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py:214>).

### escolher_resultado

Linha 151: [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py:151>).

```python
def escolher_resultado(achados):
```

**Explicacao presente no codigo:**

> Escolhe o resultado mais restritivo entre todos os achados.
> 
> A triagem não para no primeiro problema:
> todos os achados continuam registrados.

**Expressoes de retorno (dependem do caminho):**

- `Triagem.Resultado.SEM_IMPEDIMENTO`
- `resultado`

**Estrutura de controle:** For: 1, If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `calcular_resultado` em [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py:214>).
- `avaliar_triagem` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:390>).

### mensagem_do_resultado

Linha 178: [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py:178>).

```python
def mensagem_do_resultado(resultado):
```

**Explicacao presente no codigo:**

> Retorna a mensagem segura apresentada ao usuário.

**Expressoes de retorno (dependem do caminho):**

- `mensagens[resultado]`

**Onde aparece uma chamada com este nome:**

- `calcular_resultado` em [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py:214>).

### calcular_resultado

Linha 214: [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py:214>).

```python
def calcular_resultado(respostas, hoje=None):
```

**Explicacao presente no codigo:**

> Calcula o resultado inicial da triagem extensa.
> 
> O parâmetro hoje existe para facilitar testes e garantir
> que o cálculo possa ser repetido com uma data conhecida.

**Chamadas utilizadas no corpo:** `achado.get`, `adicionar_achado`, `datas_liberacao.append`, `date.fromisoformat`, `date.today`, `doacoes_12_meses.isdigit`, `escolher_resultado`, `int`, `max`, `mensagem_do_resultado`, `respostas.get`, `timedelta`.

**Expressoes de retorno (dependem do caminho):**

- `{'resultado': resultado, 'mensagem': mensagem_do_resultado(resultado), 'data_liberacao': data_liberacao, 'achados': achados}`

**Estrutura de controle:** If: 16, For: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `TriagemExtensaTests.test_peso_abaixo_de_50_gera_inaptidao_temporaria` em [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:55>).
- `TriagemExtensaTests.test_respostas_basicas_sem_impedimento` em [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py:73>).

### preparar_respostas

Linha 429: [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py:429>).

```python
def preparar_respostas(form):
```

**Explicacao presente no codigo:**

> Converte as respostas do formulário para os registros do banco.

**Chamadas utilizadas no corpo:** `dict`, `form.cleaned_data.get`, `isinstance`, `opcoes.get`, `respostas.append`, `str`, `valor.isoformat`, `valor.strftime`.

**Expressoes de retorno (dependem do caminho):**

- `respostas`

**Estrutura de controle:** For: 1, If: 2. Abra o original para seguir as condicoes na ordem.

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `TRIAGEM_RULE_VERSION`: linha 85; valor declarado em [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py:85>).
- `QUESTION_FIELDS`: linha 89; valor declarado em [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py:89>).

## accounts/triagem_catalogo.py

Acesso e validacao dos catalogos versionados.

Original: [accounts/triagem_catalogo.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo.py>).

**Dependencias importadas:**

```python
from .triagem_catalogo_extensa import PERGUNTAS_EXTENSAS, REGRA_VERSION
from .triagem_catalogo_simplificada import PERGUNTAS_SIMPLIFICADAS
```

### obter_catalogo

Linha 7: [accounts/triagem_catalogo.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo.py:7>).

```python
def obter_catalogo(modalidade):
```

**Explicacao presente no codigo:**

> Retorna o catálogo adequado e rejeita modalidade desconhecida.

**Chamadas utilizadas no corpo:** `ValueError`.

**Expressoes de retorno (dependem do caminho):**

- `PERGUNTAS_EXTENSAS`
- `PERGUNTAS_SIMPLIFICADAS`

**Excecoes levantadas:**

- `ValueError('Modalidade de triagem inválida.')`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

### obter_pergunta

Linha 17: [accounts/triagem_catalogo.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo.py:17>).

```python
def obter_pergunta(id_pergunta):
```

**Explicacao presente no codigo:**

> Localiza uma pergunta pelo identificador estável.

**Chamadas utilizadas no corpo:** `KeyError`, `PERGUNTAS_EXTENSAS.get`, `PERGUNTAS_SIMPLIFICADAS.get`.

**Expressoes de retorno (dependem do caminho):**

- `pergunta`

**Excecoes levantadas:**

- `KeyError(f'Pergunta inexistente: {id_pergunta}')`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `FormularioPerguntaTests.test_escolha_com_data_e_normalizada` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:12>).
- `FormularioPerguntaTests.test_selecao_multipla_preserva_uma_data_por_item` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:33>).
- `FormularioPerguntaTests.test_data_futura_e_rejeitada` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:54>).
- `FormularioPerguntaTests.test_alternativa_com_prazo_exige_sua_data` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:68>).
- `FormularioPerguntaTests.test_nenhuma_nao_pode_ser_marcada_com_uma_condicao` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:79>).
- `FormularioPerguntaTests.test_descricao_e_obrigatoria_quando_usuario_informa_outra_condicao` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:92>).
- `FormularioPerguntaTests.test_procedimento_estetico_registra_seguranca_e_inflamacao` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:103>).
- `TriagemServicoTests.test_nova_extensa_pode_reutilizar_respostas_concluidas` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:81>).
- `TriagemServicoTests.test_conclusao_salva_resultado_e_bloqueia_nova_resposta` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:237>).
- `TriagemViewsTests._preencher_ate_confirmacao` em [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py:64>).
- `_avaliar_intervalo_ultima_doacao` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:243>).
- `_avaliar_limite_doacoes` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:288>).
- `_avaliar_seguranca_estetica` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:322>).
- `avaliar_triagem` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:390>).
- `obter_pergunta_atual` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:287>).
- `salvar_resposta` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:386>).
- `triagem_revisao` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1244>).

### todas_as_perguntas

Linha 28: [accounts/triagem_catalogo.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo.py:28>).

```python
def todas_as_perguntas():
```

**Explicacao presente no codigo:**

> Fornece todas as perguntas para validação e auditoria.

**Chamadas utilizadas no corpo:** `PERGUNTAS_EXTENSAS.values`, `PERGUNTAS_SIMPLIFICADAS.values`.

**Expressoes de retorno (dependem do caminho):**

- `[*PERGUNTAS_EXTENSAS.values(), *PERGUNTAS_SIMPLIFICADAS.values()]`

**Onde aparece uma chamada com este nome:**

- `CatalogosTriagemTests.test_perguntas_possuem_conteudo_e_rastreabilidade` em [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py:45>).
- `CatalogosTriagemTests.test_codigos_de_opcao_nao_se_repetem_na_mesma_pergunta` em [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py:62>).
- `validar_catalogos` em [accounts/triagem_catalogo.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo.py:37>).

### validar_catalogos

Linha 37: [accounts/triagem_catalogo.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo.py:37>).

```python
def validar_catalogos():
```

**Explicacao presente no codigo:**

> Interrompe a inicialização de testes se o catálogo estiver incoerente.

**Chamadas utilizadas no corpo:** `ValueError`, `len`, `pergunta['abrir_extensa'].values`, `set`, `todas_as_perguntas`.

**Expressoes de retorno (dependem do caminho):**

- `None`

**Excecoes levantadas:**

- `ValueError('O identificador interno não corresponde à chave.')`
- `ValueError(f"Destino {destino} inexistente em {pergunta['id']}.")`
- `ValueError(f"Há alternativas duplicadas em {pergunta['id']}.")`
- `ValueError(f"Há regras para alternativas inexistentes em {pergunta['id']}.")`

**Estrutura de controle:** For: 3, If: 4. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `CatalogosTriagemTests.test_funcao_de_validacao_aceita_os_catalogos_oficiais` em [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py:77>).

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `TRIAGEM_RULE_VERSION`: linha 69; valor declarado em [accounts/triagem_catalogo.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo.py:69>).

## accounts/triagem_catalogo_extensa.py

Declaracoes de todas as perguntas e regras da extensa.

Original: [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py>).

### opcao

Linha 16: [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py:16>).

```python
def opcao(codigo, rotulo):
```

**Explicacao presente no codigo:**

> Cria uma alternativa com código próprio para persistência.

**Expressoes de retorno (dependem do caminho):**

- `{'codigo': codigo, 'rotulo': rotulo}`

**Onde aparece uma chamada com este nome:**

- `pergunta` em [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py:33>).

### regra

Linha 22: [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py:22>).

```python
def regra(resultado, mensagem, prazo=None, exige_relatorio=False):
```

**Explicacao presente no codigo:**

> Cria uma regra declarativa consumida pelo motor da triagem.

**Expressoes de retorno (dependem do caminho):**

- `{'resultado': resultado, 'mensagem': mensagem, 'prazo': prazo, 'exige_relatorio': exige_relatorio}`

**Onde aparece uma chamada com este nome:**

- `pergunta_tabela` em [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py:73>).

### pergunta

Linha 33: [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py:33>).

```python
def pergunta(id_pergunta, titulo, texto, explicacao, opcoes, *, multipla=False, permite_data=False, exige_data_para=(), exige_detalhes_para=(), perguntar_seguranca=False, perguntar_inflamacao=False, mostrar_se=None, regras=None, fonte='Manual Elo; ref. [1]'):
```

**Explicacao presente no codigo:**

> Padroniza todos os campos esperados pelas demais camadas.

**Chamadas utilizadas no corpo:** `list`, `opcao`.

**Expressoes de retorno (dependem do caminho):**

- `{'id': id_pergunta, 'titulo': titulo, 'texto': texto, 'explicacao': explicacao, 'tipo': 'escolha', 'opcoes': [opcao(*item) for item in opcoes], 'multipla': multipla, 'permite_data': permite_data, 'exige_data_para': list(exige_data_para), 'exige_detalhes_para': list(exige_detalhes_para), 'perguntar_seguranca': perguntar_seguranca, 'perguntar_inflamacao': perguntar_inflamacao, 'mostrar_se': mostrar_se, 'abrir_extensa': {}, 'regras': regras or {}, 'fonte': fonte, 'regra_version': REGRA_VERSION}`

**Onde aparece uma chamada com este nome:**

- `pergunta_tabela` em [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py:73>).
- `pergunta_simplificada` em [accounts/triagem_catalogo_simplificada.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_simplificada.py:11>).

### pergunta_tabela

Linha 73: [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py:73>).

```python
def pergunta_tabela(id_pergunta, titulo, texto, explicacao, itens, *, permite_data=True, exige_detalhes_para=(), perguntar_seguranca=False, perguntar_inflamacao=False, fonte='Manual Elo; ref. [1]'):
```

**Explicacao presente no codigo:**

> Monta perguntas longas em que várias condições podem ser marcadas.

**Chamadas utilizadas no corpo:** `exige_data.append`, `opcoes.append`, `pergunta`, `regra`.

**Expressoes de retorno (dependem do caminho):**

- `pergunta(id_pergunta, titulo, texto, explicacao, opcoes, multipla=True, permite_data=permite_data, exige_data_para=exige_data, exige_detalhes_para=exige_detalhes_para, perguntar_seguranca=perguntar_seguranca, perguntar_inflamacao=perguntar_inflamacao, regras=regras, fonte=fonte)`

**Estrutura de controle:** For: 1, If: 2. Abra o original para seguir as condicoes na ordem.

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `REGRA_VERSION`: linha 8; valor declarado em [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py:8>).
- `TEMPORARIA`: linha 10; valor declarado em [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py:10>).
- `DEFINITIVA`: linha 11; valor declarado em [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py:11>).
- `AVALIACAO`: linha 12; valor declarado em [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py:12>).
- `DOCUMENTACAO`: linha 13; valor declarado em [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py:13>).
- `PERGUNTAS_EXTENSAS`: linha 117; valor declarado em [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py:117>).

## accounts/triagem_catalogo_simplificada.py

Declaracoes das perguntas rapidas e abertura de detalhes.

Original: [accounts/triagem_catalogo_simplificada.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_simplificada.py>).

**Dependencias importadas:**

```python
from .triagem_catalogo_extensa import AVALIACAO, PERGUNTAS_EXTENSAS, pergunta, regra
```

### pergunta_simplificada

Linha 11: [accounts/triagem_catalogo_simplificada.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_simplificada.py:11>).

```python
def pergunta_simplificada(id_pergunta, titulo, texto, explicacao, opcoes, *, abrir_extensa=None, multipla=False, regras=None, fonte='Manual Elo, seção 18'):
```

**Explicacao presente no codigo:**

> Monta uma pergunta rápida e registra os aprofundamentos necessários.

**Chamadas utilizadas no corpo:** `pergunta`.

**Expressoes de retorno (dependem do caminho):**

- `item`

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `TODAS_AS_EXTENSAS`: linha 40; valor declarado em [accounts/triagem_catalogo_simplificada.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_simplificada.py:40>).
- `PERGUNTAS_SIMPLIFICADAS`: linha 43; valor declarado em [accounts/triagem_catalogo_simplificada.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_simplificada.py:43>).

## accounts/triagem_forms.py

Formulario dinamico correspondente a cada pergunta.

Original: [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py>).

**Dependencias importadas:**

```python
from datetime import date
from django import forms
```

### FormularioPergunta

Linha 24: [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:24>).

Classe; herda de: forms.Form.

**Explicacao presente no codigo:**

> Cria somente os campos necessários para uma pergunta do catálogo.

**Onde aparece uma chamada com este nome:**

- `FormularioPerguntaTests.test_escolha_com_data_e_normalizada` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:12>).
- `FormularioPerguntaTests.test_selecao_multipla_preserva_uma_data_por_item` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:33>).
- `FormularioPerguntaTests.test_data_futura_e_rejeitada` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:54>).
- `FormularioPerguntaTests.test_alternativa_com_prazo_exige_sua_data` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:68>).
- `FormularioPerguntaTests.test_nenhuma_nao_pode_ser_marcada_com_uma_condicao` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:79>).
- `FormularioPerguntaTests.test_descricao_e_obrigatoria_quando_usuario_informa_outra_condicao` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:92>).
- `FormularioPerguntaTests.test_procedimento_estetico_registra_seguranca_e_inflamacao` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:103>).

### FormularioPergunta.__init__

Linha 27: [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:27>).

```python
def __init__(self, pergunta, *args, **kwargs):
```

**Chamadas utilizadas no corpo:** `datas_iniciais.get`, `forms.CharField`, `forms.ChoiceField`, `forms.DateField`, `forms.DateInput`, `forms.MultipleChoiceField`, `forms.Textarea`, `kwargs.pop`, `super`, `super().__init__`, `valor_inicial.get`.

**Estrutura de controle:** If: 3, For: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `CadastroUsuarioForm.__init__` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:149>).
- `PedidoSangueForm.__init__` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:642>).
- `FormularioPergunta.__init__` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:128>).

### FormularioPergunta.clean

Linha 105: [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:105>).

```python
def clean(self):
```

**Explicacao presente no codigo:**

> Valida contradições e devolve um valor único para persistência.

**Chamadas utilizadas no corpo:** `(dados.get('detalhes') or '').strip`, `bool`, `dados.get`, `data_evento.isoformat`, `date.today`, `exclusivos.intersection`, `len`, `list`, `self.add_error`, `set`, `set(codigos).intersection`, `super`, `super().clean`.

**Expressoes de retorno (dependem do caminho):**

- `dados`

**Estrutura de controle:** If: 8, For: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `CadastroUsuarioForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:244>).
- `TriagemExtensaForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:436>).
- `CadastrarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:506>).
- `MovimentarEstoqueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:559>).
- `PedidoSangueForm.clean` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:681>).
- `Usuario.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:187>).
- `ValidacaoHemocentro.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:277>).
- `Estoque.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:751>).
- `PedidoSangue.clean` em [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py:1068>).


## accounts/triagem_motor.py

Calculo da orientacao a partir das respostas e regras dos catalogos.

Original: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py>).

**Dependencias importadas:**

```python
import calendar
import math
from datetime import date, datetime, timedelta
from .models import Triagem
from .triagem_catalogo import TRIAGEM_RULE_VERSION, obter_pergunta
```

### escolher_resultado

Linha 93: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:93>).

```python
def escolher_resultado(achados):
```

**Explicacao presente no codigo:**

> Escolhe o estado principal sem descartar os demais achados.

**Expressoes de retorno (dependem do caminho):**

- `Triagem.Resultado.SEM_IMPEDIMENTO`
- `resultado`

**Estrutura de controle:** For: 1, If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `calcular_resultado` em [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py:214>).
- `avaliar_triagem` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:390>).

### _converter_data

Linha 105: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:105>).

```python
def _converter_data(valor):
```

**Explicacao presente no codigo:**

> Aceita data, datetime ou ISO; valor inválido volta como ausente.

**Chamadas utilizadas no corpo:** `date.fromisoformat`, `isinstance`, `str`, `valor.date`.

**Expressoes de retorno (dependem do caminho):**

- `None`
- `date.fromisoformat(str(valor))`
- `valor`
- `valor.date()`

**Estrutura de controle:** If: 3, Try: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `_data_da_resposta` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:152>).

### _somar_meses

Linha 121: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:121>).

```python
def _somar_meses(data_base, quantidade):
```

**Explicacao presente no codigo:**

> Soma meses pelo calendário e ajusta dias como 31 de janeiro.

**Chamadas utilizadas no corpo:** `calendar.monthrange`, `date`, `min`.

**Expressoes de retorno (dependem do caminho):**

- `date(ano, mes, min(data_base.day, ultimo_dia))`

**Onde aparece uma chamada com este nome:**

- `calcular_data_liberacao` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:131>).
- `_avaliar_intervalo_ultima_doacao` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:243>).
- `_avaliar_seguranca_estetica` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:322>).

### calcular_data_liberacao

Linha 131: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:131>).

```python
def calcular_data_liberacao(data_base, prazo):
```

**Explicacao presente no codigo:**

> Calcula a data final para horas, dias, semanas, meses ou anos.

**Chamadas utilizadas no corpo:** `ValueError`, `_somar_meses`, `math.ceil`, `timedelta`.

**Expressoes de retorno (dependem do caminho):**

- `_somar_meses(data_base, quantidade * 12)`
- `_somar_meses(data_base, quantidade)`
- `data_base + timedelta(days=math.ceil(quantidade / 24))`
- `data_base + timedelta(days=quantidade)`
- `data_base + timedelta(weeks=quantidade)`

**Excecoes levantadas:**

- `ValueError(f'Unidade de prazo inválida: {unidade}')`

**Estrutura de controle:** If: 5. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `_avaliar_regra_declarada` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:189>).

### _data_da_resposta

Linha 152: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:152>).

```python
def _data_da_resposta(valor, codigo):
```

**Explicacao presente no codigo:**

> Obtém a data específica da alternativa ou a data legada da resposta.

**Chamadas utilizadas no corpo:** `_converter_data`, `datas.get`, `valor.get`.

**Expressoes de retorno (dependem do caminho):**

- `_converter_data(datas.get(codigo) or valor.get('data_evento'))`

**Onde aparece uma chamada com este nome:**

- `_avaliar_regra_declarada` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:189>).
- `_avaliar_intervalo_ultima_doacao` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:243>).
- `_avaliar_seguranca_estetica` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:322>).

### _novo_achado

Linha 161: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:161>).

```python
def _novo_achado(pergunta, codigo, resultado, mensagem, *, data_liberacao=None, exige_relatorio=False):
```

**Explicacao presente no codigo:**

> Padroniza a estrutura persistida no campo JSON de achados.

**Chamadas utilizadas no corpo:** `data_liberacao.isoformat`.

**Expressoes de retorno (dependem do caminho):**

- `achado`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `_avaliar_regra_declarada` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:189>).
- `_avaliar_intervalo_ultima_doacao` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:243>).
- `_avaliar_limite_doacoes` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:288>).
- `_avaliar_seguranca_estetica` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:322>).

### _avaliar_regra_declarada

Linha 189: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:189>).

```python
def _avaliar_regra_declarada(pergunta, codigo, valor, hoje):
```

**Explicacao presente no codigo:**

> Avalia uma alternativa simples definida diretamente no catálogo.

**Chamadas utilizadas no corpo:** `_data_da_resposta`, `_novo_achado`, `calcular_data_liberacao`, `item_regra.get`, `pergunta['regras'].get`, `prazo.get`.

**Expressoes de retorno (dependem do caminho):**

- `None`
- `_novo_achado(pergunta, codigo, resultado, mensagem, data_liberacao=data_final, exige_relatorio=item_regra.get('exige_relatorio', False))`
- `_novo_achado(pergunta, f'{codigo}_SEM_DATA', Triagem.Resultado.AVALIACAO, 'Informe a data do evento ou confirme o prazo presencialmente.')`

**Estrutura de controle:** If: 5. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `avaliar_triagem` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:390>).

### _primeiro_codigo

Linha 235: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:235>).

```python
def _primeiro_codigo(respostas, id_pergunta):
```

**Explicacao presente no codigo:**

> Retorna a primeira alternativa quando a pergunta é de escolha única.

**Chamadas utilizadas no corpo:** `respostas.get`, `valor.get`.

**Expressoes de retorno (dependem do caminho):**

- `codigos[0] if codigos else None`

**Onde aparece uma chamada com este nome:**

- `_avaliar_intervalo_ultima_doacao` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:243>).
- `_avaliar_limite_doacoes` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:288>).

### _avaliar_intervalo_ultima_doacao

Linha 243: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:243>).

```python
def _avaliar_intervalo_ultima_doacao(respostas, hoje):
```

**Explicacao presente no codigo:**

> Aplica 60/90 dias e a regra adicional de seis meses após os 60.

**Chamadas utilizadas no corpo:** `_data_da_resposta`, `_novo_achado`, `_primeiro_codigo`, `_somar_meses`, `datas.append`, `max`, `obter_pergunta`, `respostas.get`, `timedelta`, `valor.get`.

**Expressoes de retorno (dependem do caminho):**

- `None`
- `_novo_achado(pergunta, 'INTERVALO_DOACAO', Triagem.Resultado.TEMPORARIA, 'Ainda não terminou o intervalo orientativo desde a última doação.', data_liberacao=data_final)`
- `_novo_achado(pergunta, 'INTERVALO_SEM_DATA', Triagem.Resultado.AVALIACAO, 'A data da última doação é necessária para calcular o intervalo.')`

**Estrutura de controle:** If: 7. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `avaliar_triagem` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:390>).

### _avaliar_limite_doacoes

Linha 288: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:288>).

```python
def _avaliar_limite_doacoes(respostas):
```

**Explicacao presente no codigo:**

> Sem datas históricas, sinaliza o limite sem inventar uma liberação.

**Chamadas utilizadas no corpo:** `_novo_achado`, `_primeiro_codigo`, `obter_pergunta`, `quantidades.get`.

**Expressoes de retorno (dependem do caminho):**

- `None`
- `_novo_achado(pergunta, 'LIMITE_ANUAL_SEM_DATAS', Triagem.Resultado.AVALIACAO, 'O limite anual foi alcançado; as datas históricas precisam ser conferidas.')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `avaliar_triagem` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:390>).

### _avaliar_seguranca_estetica

Linha 322: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:322>).

```python
def _avaliar_seguranca_estetica(respostas, hoje):
```

**Explicacao presente no codigo:**

> Aplica 12 meses quando a segurança estética não é comprovada.

**Chamadas utilizadas no corpo:** `_data_da_resposta`, `_novo_achado`, `_somar_meses`, `achados.append`, `obter_pergunta`, `respostas.get`, `set`, `valor.get`.

**Expressoes de retorno (dependem do caminho):**

- `[]`
- `achados`

**Estrutura de controle:** If: 5, For: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `avaliar_triagem` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:390>).

### _respostas_para_avaliar

Linha 375: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:375>).

```python
def _respostas_para_avaliar(modalidade, respostas, respostas_base):
```

**Explicacao presente no codigo:**

> Combina somente dados estáveis da extensa com a checagem rápida.

**Chamadas utilizadas no corpo:** `(respostas_base or {}).items`, `combinadas.update`, `dict`.

**Expressoes de retorno (dependem do caminho):**

- `combinadas`
- `dict(respostas)`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `avaliar_triagem` em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:390>).

### avaliar_triagem

Linha 390: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:390>).

```python
def avaliar_triagem(modalidade, respostas, *, hoje=None, respostas_base=None):
```

**Explicacao presente no codigo:**

> Avalia todas as respostas e devolve resultado, mensagem e achados.

**Chamadas utilizadas no corpo:** `ValueError`, `_avaliar_intervalo_ultima_doacao`, `_avaliar_limite_doacoes`, `_avaliar_regra_declarada`, `_avaliar_seguranca_estetica`, `_respostas_para_avaliar`, `achado.get`, `achados.append`, `achados.extend`, `date.fromisoformat`, `date.today`, `escolher_resultado`, `max`, `obter_pergunta`, `respostas_atuais.items`, `valor.get`.

**Expressoes de retorno (dependem do caminho):**

- `{'resultado': resultado, 'mensagem': MENSAGENS_RESULTADO[resultado], 'data_liberacao': max(datas) if datas else None, 'achados': achados, 'regra_version': TRIAGEM_RULE_VERSION}`

**Excecoes levantadas:**

- `ValueError('Modalidade de triagem inválida.')`

**Estrutura de controle:** If: 5, For: 2, Try: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `MotorTriagemTests.test_resultado_prioriza_definitiva_e_preserva_todos_os_achados` em [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:23>).
- `MotorTriagemTests.test_resultado_usa_a_maior_data_temporaria` em [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:42>).
- `MotorTriagemTests.test_prazo_em_meses_respeita_o_calendario` em [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:65>).
- `MotorTriagemTests.test_regra_com_prazo_sem_data_exige_avaliacao` em [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:84>).
- `MotorTriagemTests.test_estetica_sem_seguranca_usa_doze_meses` em [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:99>).
- `MotorTriagemTests.test_estetica_com_inflamacao_exige_avaliacao` em [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:120>).
- `MotorTriagemTests.test_ultima_doacao_calcula_intervalo_feminino` em [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:141>).
- `MotorTriagemTests.test_ultima_doacao_acima_de_60_usa_seis_meses` em [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:162>).
- `MotorTriagemTests.test_limite_anual_sem_datas_nao_inventa_liberacao` em [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:183>).
- `MotorTriagemTests.test_simplificada_reutiliza_doenca_estavel_da_extensa` em [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:201>).
- `MotorTriagemTests.test_simplificada_nao_reutiliza_estado_de_saude_antigo` em [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:218>).
- `MotorTriagemTests.test_resultado_sem_achados_mantem_aviso_presencial` em [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py:235>).
- `concluir_triagem` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:516>).

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `PRIORIDADE_RESULTADOS`: linha 37; valor declarado em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:37>).
- `PERGUNTAS_NAO_REUTILIZAVEIS`: linha 46; valor declarado em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:46>).
- `MENSAGENS_RESULTADO`: linha 65; valor declarado em [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py:65>).

## accounts/triagem_servico.py

Andamento, respostas, revisao, persistencia e conclusao de triagem.

Original: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py>).

**Dependencias importadas:**

```python
from datetime import date
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone
from .compatibilidade import normalizar_tipo_sanguineo
from .models import ConsentimentoLGPD, RespostaTriagem, Triagem, Usuario
from .triagem_catalogo import PERGUNTAS_EXTENSAS, PERGUNTAS_SIMPLIFICADAS, TRIAGEM_RULE_VERSION, obter_pergunta
from .triagem_motor import avaliar_triagem
```

### TriagemSimplificadaIndisponivel

Linha 39: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:39>).

Classe; herda de: Exception.

**Explicacao presente no codigo:**

> Indica que a pessoa ainda não concluiu uma triagem extensa.

**Onde aparece uma chamada com este nome:**

- `iniciar_triagem` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:207>).

### TriagemConcluida

Linha 43: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:43>).

Classe; herda de: Exception.

**Explicacao presente no codigo:**

> Impede alteração de um resultado já registrado no histórico.

**Onde aparece uma chamada com este nome:**

- `salvar_resposta` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:386>).
- `voltar_pergunta` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:481>).
- `editar_pergunta` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:499>).
- `concluir_triagem` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:516>).

### TriagemIncompleta

Linha 47: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:47>).

Classe; herda de: Exception.

**Explicacao presente no codigo:**

> Indica que existem perguntas obrigatórias ainda sem resposta.

**Onde aparece uma chamada com este nome:**

- `concluir_triagem` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:516>).

### TriagemExtensaNecessaria

Linha 51: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:51>).

Classe; herda de: Exception.

**Explicacao presente no codigo:**

> Indica que a versão rápida deixou de ser segura para o usuário.

**Onde aparece uma chamada com este nome:**

- `salvar_resposta` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:386>).

### PerguntaInvalida

Linha 55: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:55>).

Classe; herda de: Exception.

**Explicacao presente no codigo:**

> Impede códigos de pergunta ou alternativa fora do catálogo.

**Onde aparece uma chamada com este nome:**

- `_validar_valor` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:300>).
- `_primeira_data` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:328>).
- `salvar_resposta` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:386>).
- `editar_pergunta` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:499>).

### pode_responder

Linha 84: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:84>).

```python
def pode_responder(usuario):
```

**Explicacao presente no codigo:**

> Diz se o perfil pode realizar uma triagem para doação.

**Expressoes de retorno (dependem do caminho):**

- `usuario.perfil in PERFIS_COM_TRIAGEM`

**Onde aparece uma chamada com este nome:**

- `iniciar_triagem` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:207>).
- `dashboard` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:720>).
- `triagem_apresentacao` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:975>).
- `triagem_historico` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1032>).
- `triagem_iniciar` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1074>).
- `_triagem_do_usuario_ou_404` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1124>).

### obter_extensa_base

Linha 90: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:90>).

```python
def obter_extensa_base(usuario):
```

**Explicacao presente no codigo:**

> Retorna a extensa concluída mais recente do próprio usuário.

**Chamadas utilizadas no corpo:** `usuario.triagens.filter`, `usuario.triagens.filter(modalidade=Triagem.Modalidade.EXTENSA, status=Triagem.Status.CONCLUIDA).order_by`, `usuario.triagens.filter(modalidade=Triagem.Modalidade.EXTENSA, status=Triagem.Status.CONCLUIDA).order_by('-finalizada_em', '-iniciada_em').first`.

**Expressoes de retorno (dependem do caminho):**

- `usuario.triagens.filter(modalidade=Triagem.Modalidade.EXTENSA, status=Triagem.Status.CONCLUIDA).order_by('-finalizada_em', '-iniciada_em').first()`

**Onde aparece uma chamada com este nome:**

- `iniciar_triagem` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:207>).
- `triagem_apresentacao` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:975>).

### obter_extensa_reutilizavel

Linha 103: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:103>).

```python
def obter_extensa_reutilizavel(usuario):
```

**Explicacao presente no codigo:**

> Retorna a extensa concluída atual que pode preencher uma nova triagem.

**Chamadas utilizadas no corpo:** `usuario.triagens.filter`, `usuario.triagens.filter(modalidade=Triagem.Modalidade.EXTENSA, status=Triagem.Status.CONCLUIDA, regra_version=TRIAGEM_RULE_VERSION).order_by`, `usuario.triagens.filter(modalidade=Triagem.Modalidade.EXTENSA, status=Triagem.Status.CONCLUIDA, regra_version=TRIAGEM_RULE_VERSION).order_by('-finalizada_em', '-iniciada_em').first`.

**Expressoes de retorno (dependem do caminho):**

- `usuario.triagens.filter(modalidade=Triagem.Modalidade.EXTENSA, status=Triagem.Status.CONCLUIDA, regra_version=TRIAGEM_RULE_VERSION).order_by('-finalizada_em', '-iniciada_em').first()`

**Onde aparece uma chamada com este nome:**

- `iniciar_triagem` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:207>).
- `triagem_apresentacao` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:975>).

### _respostas_da_triagem

Linha 117: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:117>).

```python
def _respostas_da_triagem(triagem):
```

**Explicacao presente no codigo:**

> Transforma registros do banco no mapa esperado pelo catálogo e motor.

**Chamadas utilizadas no corpo:** `triagem.respostas.all`.

**Expressoes de retorno (dependem do caminho):**

- `{resposta.id_pergunta: resposta.valor for resposta in triagem.respostas.all()}`

**Onde aparece uma chamada com este nome:**

- `calcular_fluxo` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:163>).
- `concluir_triagem` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:516>).

### _condicao_atendida

Linha 126: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:126>).

```python
def _condicao_atendida(pergunta, respostas):
```

**Explicacao presente no codigo:**

> Verifica as condições simples que mostram uma subpergunta.

**Chamadas utilizadas no corpo:** `codigos.intersection`, `condicao.items`, `pergunta.get`, `respostas.get`, `set`, `valor.get`.

**Expressoes de retorno (dependem do caminho):**

- `False`
- `True`

**Estrutura de controle:** If: 2, For: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `calcular_fluxo` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:163>).

### _copiar_respostas_para_nova_triagem

Linha 142: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:142>).

```python
def _copiar_respostas_para_nova_triagem(origem, destino):
```

**Explicacao presente no codigo:**

> Copia respostas para uma nova triagem sem alterar o histórico original.

**Chamadas utilizadas no corpo:** `RespostaTriagem`, `RespostaTriagem.objects.bulk_create`, `origem.respostas.order_by`.

**Onde aparece uma chamada com este nome:**

- `iniciar_triagem` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:207>).

### calcular_fluxo

Linha 163: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:163>).

```python
def calcular_fluxo(triagem):
```

**Explicacao presente no codigo:**

> Recalcula ramificações sem duplicar perguntas já adicionadas.

**Chamadas utilizadas no corpo:** `ORDEM_SIMPLIFICADA.index`, `PERGUNTAS_SIMPLIFICADAS.get`, `_condicao_atendida`, `_respostas_da_triagem`, `ids_abertos.update`, `pergunta['abrir_extensa'].get`, `respostas.items`, `set`, `valor.get`.

**Expressoes de retorno (dependem do caminho):**

- `[*ORDEM_SIMPLIFICADA[:indice_confirmacao], *detalhadas, *ORDEM_SIMPLIFICADA[indice_confirmacao:]]`
- `[id_pergunta for id_pergunta in ORDEM_EXTENSA if _condicao_atendida(PERGUNTAS_EXTENSAS[id_pergunta], respostas)]`

**Estrutura de controle:** If: 2, For: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `iniciar_triagem` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:207>).
- `salvar_resposta` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:386>).

### iniciar_triagem

Linha 207: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:207>).

```python
def iniciar_triagem(usuario, modalidade, ip=None, aceite_termo=True, reutilizar_respostas=False):
```

**Explicacao presente no codigo:**

> Cria/retoma a triagem após o aceite registrado pela camada de entrada.
> 
> A view exige o checkbox explicitamente; o valor padrão preserva a API de
> serviço usada por integrações internas que já representam esse aceite.

**Decoradores:** `transaction.atomic`.

**Chamadas utilizadas no corpo:** `ConsentimentoLGPD.objects.get_or_create`, `PermissionDenied`, `Triagem.objects.create`, `TriagemSimplificadaIndisponivel`, `ValueError`, `_copiar_respostas_para_nova_triagem`, `calcular_fluxo`, `consentimento.save`, `obter_extensa_base`, `obter_extensa_reutilizavel`, `pode_responder`, `triagem.save`, `usuario.triagens.filter`, `usuario.triagens.filter(modalidade=modalidade, status=Triagem.Status.EM_ANDAMENTO).order_by`, `usuario.triagens.filter(modalidade=modalidade, status=Triagem.Status.EM_ANDAMENTO).order_by('-iniciada_em').first`.

**Expressoes de retorno (dependem do caminho):**

- `existente`
- `triagem`

**Excecoes levantadas:**

- `PermissionDenied('A triagem está disponível para Doadores.')`
- `PermissionDenied('Confirme ciência do termo da pré-triagem antes de começar.')`
- `TriagemSimplificadaIndisponivel('Conclua primeiro uma triagem extensa.')`
- `ValueError('Modalidade de triagem inválida.')`

**Estrutura de controle:** If: 9. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `TriagemServicoTests.test_inicio_extenso_cria_fluxo_e_consentimento` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:40>).
- `TriagemServicoTests.test_inicio_reutiliza_triagem_em_andamento` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:64>).
- `TriagemServicoTests.test_nova_extensa_pode_reutilizar_respostas_concluidas` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:81>).
- `TriagemServicoTests.test_simplificada_exige_extensa_concluida_do_mesmo_usuario` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:116>).
- `TriagemServicoTests.test_simplificada_registra_a_extensa_base` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:126>).
- `TriagemServicoTests.test_observador_nao_pode_iniciar_questionario` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:145>).
- `TriagemServicoTests.test_corrigir_resposta_substitui_sem_duplicar` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:162>).
- `TriagemServicoTests.test_resposta_simplificada_insere_bloco_extenso_sem_duplicar` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:188>).
- `TriagemServicoTests.test_conclusao_salva_resultado_e_bloqueia_nova_resposta` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:237>).
- `TriagemServicoTests.test_resposta_mantem_campos_legados_e_valor_completo` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:296>).
- `TriagemServicoTests.test_nao_entendeu_permanece_na_primeira_pergunta` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:318>).
- `TriagemServicoTests.test_revisar_confirmacao_extensa_volta_ao_inicio` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:335>).
- `TriagemServicoTests.test_resumo_incorreto_cancela_rapida_e_exige_extensa` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:354>).
- `TriagemServicoTests.test_correcao_remove_resposta_de_subpergunta_oculta` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:383>).
- `TriagemServicoTests.test_rapida_respeita_condicoes_das_perguntas_detalhadas` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:418>).
- `triagem_iniciar` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1074>).
- `triagem_pergunta` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1138>).

### obter_pergunta_atual

Linha 287: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:287>).

```python
def obter_pergunta_atual(triagem):
```

**Explicacao presente no codigo:**

> Retorna a pergunta apontada pelo andamento ou nada após o fim.

**Chamadas utilizadas no corpo:** `len`, `obter_pergunta`.

**Expressoes de retorno (dependem do caminho):**

- `None`
- `obter_pergunta(triagem.fluxo_perguntas[triagem.pergunta_atual])`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `TriagemServicoTests.test_resposta_simplificada_insere_bloco_extenso_sem_duplicar` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:188>).
- `triagem_pergunta` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1138>).

### _validar_valor

Linha 300: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:300>).

```python
def _validar_valor(pergunta, valor):
```

**Explicacao presente no codigo:**

> Rejeita dados forjados mesmo quando não vieram do formulário Django.

**Chamadas utilizadas no corpo:** `PerguntaInvalida`, `len`, `set`, `set(codigos).issubset`, `valor.get`.

**Excecoes levantadas:**

- `PerguntaInvalida('A resposta não pertence às alternativas da pergunta.')`
- `PerguntaInvalida('Esta pergunta aceita somente uma alternativa.')`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `salvar_resposta` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:386>).

### _rotulo_resposta

Linha 318: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:318>).

```python
def _rotulo_resposta(pergunta, codigos):
```

**Explicacao presente no codigo:**

> Mantém no campo legado os rótulos visíveis ao usuário.

**Chamadas utilizadas no corpo:** `'; '.join`.

**Expressoes de retorno (dependem do caminho):**

- `'; '.join((rotulos[codigo] for codigo in codigos))`

**Onde aparece uma chamada com este nome:**

- `salvar_resposta` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:386>).

### _primeira_data

Linha 328: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:328>).

```python
def _primeira_data(valor):
```

**Explicacao presente no codigo:**

> Preenche o campo legado com a primeira data estruturada disponível.

**Chamadas utilizadas no corpo:** `PerguntaInvalida`, `datas.values`, `date.fromisoformat`, `iter`, `next`, `valor.get`.

**Expressoes de retorno (dependem do caminho):**

- `None`
- `date.fromisoformat(next(iter(datas.values())))`

**Excecoes levantadas:**

- `PerguntaInvalida('A data da resposta é inválida.')`

**Estrutura de controle:** If: 1, Try: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `salvar_resposta` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:386>).

### _resposta_exige_extensa

Linha 341: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:341>).

```python
def _resposta_exige_extensa(id_pergunta, codigos):
```

**Explicacao presente no codigo:**

> Centraliza as respostas que invalidam o resumo da versão rápida.

**Chamadas utilizadas no corpo:** `bool`, `set`.

**Expressoes de retorno (dependem do caminho):**

- `id_pergunta == 'SIM-01' and bool(escolhas & {'INCORRETO', 'NAO_FIZ', 'NAO_SEI'}) or (id_pergunta == 'SIM-17' and bool(escolhas & {'SIM', 'NAO_SEI'})) or (id_pergunta == 'SIM-18' and 'EXTENSA' in escolhas)`

**Onde aparece uma chamada com este nome:**

- `salvar_resposta` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:386>).

### atualizar_tipo_sanguineo_do_usuario

Linha 358: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:358>).

```python
def atualizar_tipo_sanguineo_do_usuario(triagem, valor):
```

**Explicacao presente no codigo:**

> Atualiza o tipo sanguineo do usuario a partir da pergunta informativa.
> 
> Essa informacao nao interfere no resultado da triagem; ela apenas liga o
> usuario aos alertas internos de estoque e a compatibilidade sanguinea.

**Chamadas utilizadas no corpo:** `normalizar_tipo_sanguineo`, `usuario.save`, `valor.get`.

**Expressoes de retorno (dependem do caminho):**

- `None`

**Estrutura de controle:** If: 3, Try: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `FluxoCadastroTriagemPedidosTests.test_tipo_sanguineo_confirmado_nao_e_sobrescrito_pela_triagem` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:295>).
- `salvar_resposta` em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:386>).

### salvar_resposta

Linha 386: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:386>).

```python
def salvar_resposta(triagem, id_pergunta, valor):
```

**Explicacao presente no codigo:**

> Salva ou corrige uma resposta e avança o fluxo com segurança.

**Chamadas utilizadas no corpo:** `PerguntaInvalida`, `RespostaTriagem.objects.update_or_create`, `Triagem.objects.select_for_update`, `Triagem.objects.select_for_update().get`, `TriagemConcluida`, `TriagemExtensaNecessaria`, `_primeira_data`, `_resposta_exige_extensa`, `_rotulo_resposta`, `_validar_valor`, `atualizar_tipo_sanguineo_do_usuario`, `calcular_fluxo`, `fluxo.index`, `len`, `min`, `obter_pergunta`, `registro.respostas.exclude`, `registro.respostas.exclude(id_pergunta__in=fluxo).delete`, `registro.save`, `transaction.atomic`, `valor.items`.

**Expressoes de retorno (dependem do caminho):**

- `triagem_recebida`

**Excecoes levantadas:**

- `PerguntaInvalida('A pergunta não pertence a esta triagem.')`
- `TriagemConcluida('Uma triagem concluída não pode ser alterada.')`
- `TriagemExtensaNecessaria('O resumo mudou; continue em uma nova triagem extensa.')`

**Estrutura de controle:** With: 1, If: 6. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `TriagemServicoTests.test_corrigir_resposta_substitui_sem_duplicar` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:162>).
- `TriagemServicoTests.test_resposta_simplificada_insere_bloco_extenso_sem_duplicar` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:188>).
- `TriagemServicoTests.test_conclusao_salva_resultado_e_bloqueia_nova_resposta` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:237>).
- `TriagemServicoTests.test_resposta_mantem_campos_legados_e_valor_completo` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:296>).
- `TriagemServicoTests.test_nao_entendeu_permanece_na_primeira_pergunta` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:318>).
- `TriagemServicoTests.test_revisar_confirmacao_extensa_volta_ao_inicio` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:335>).
- `TriagemServicoTests.test_resumo_incorreto_cancela_rapida_e_exige_extensa` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:354>).
- `TriagemServicoTests.test_correcao_remove_resposta_de_subpergunta_oculta` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:383>).
- `TriagemServicoTests.test_rapida_respeita_condicoes_das_perguntas_detalhadas` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:418>).
- `triagem_pergunta` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1138>).

### voltar_pergunta

Linha 481: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:481>).

```python
def voltar_pergunta(triagem):
```

**Explicacao presente no codigo:**

> Move uma posição para trás sem apagar a resposta existente.

**Decoradores:** `transaction.atomic`.

**Chamadas utilizadas no corpo:** `Triagem.objects.select_for_update`, `Triagem.objects.select_for_update().get`, `TriagemConcluida`, `max`, `registro.save`.

**Expressoes de retorno (dependem do caminho):**

- `triagem_recebida`

**Excecoes levantadas:**

- `TriagemConcluida('Uma triagem concluída não pode ser alterada.')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `TriagemServicoTests.test_corrigir_resposta_substitui_sem_duplicar` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:162>).
- `triagem_pergunta` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1138>).

### editar_pergunta

Linha 499: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:499>).

```python
def editar_pergunta(triagem, id_pergunta):
```

**Explicacao presente no codigo:**

> Reposiciona uma triagem em andamento para uma resposta já salva.

**Decoradores:** `transaction.atomic`.

**Chamadas utilizadas no corpo:** `PerguntaInvalida`, `Triagem.objects.select_for_update`, `Triagem.objects.select_for_update().get`, `TriagemConcluida`, `registro.fluxo_perguntas.index`, `registro.save`.

**Expressoes de retorno (dependem do caminho):**

- `triagem`

**Excecoes levantadas:**

- `PerguntaInvalida('A pergunta não pertence a esta triagem.')`
- `TriagemConcluida('Uma triagem concluída não pode ser alterada.')`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `triagem_pergunta` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1138>).

### concluir_triagem

Linha 516: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:516>).

```python
def concluir_triagem(triagem, hoje=None):
```

**Explicacao presente no codigo:**

> Calcula e congela o resultado depois da confirmação final.

**Decoradores:** `transaction.atomic`.

**Chamadas utilizadas no corpo:** `Triagem.objects.select_for_update`, `Triagem.objects.select_for_update().get`, `TriagemConcluida`, `TriagemIncompleta`, `_respostas_da_triagem`, `avaliar_triagem`, `len`, `respostas.get`, `respostas.get('EXT-51', {}).get`, `respostas.get('SIM-18', {}).get`, `set`, `timezone.now`, `triagem.save`.

**Expressoes de retorno (dependem do caminho):**

- `triagem`

**Excecoes levantadas:**

- `TriagemConcluida('Uma triagem concluída não pode ser alterada.')`
- `TriagemIncompleta('Ainda existem perguntas sem resposta.')`
- `TriagemIncompleta('Confirme a limitação da versão rápida.')`
- `TriagemIncompleta('Revise e confirme a triagem extensa.')`

**Estrutura de controle:** If: 5. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `TriagemServicoTests.test_conclusao_salva_resultado_e_bloqueia_nova_resposta` em [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py:237>).
- `triagem_revisao` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1244>).

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `PERFIS_COM_TRIAGEM`: linha 59; valor declarado em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:59>).
- `ORDEM_EXTENSA`: linha 65; valor declarado em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:65>).
- `ORDEM_SIMPLIFICADA`: linha 78; valor declarado em [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py:78>).

## accounts/urls.py

Associacao entre endereco, view e nome de rota.

Original: [accounts/urls.py](<C:/Users/lb119/Elo/accounts/urls.py>).

**Dependencias importadas:**

```python
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .forms import LoginUsuarioForm
```

### Rotas declaradas

```python
path('', views.inicio, name='inicio')
path('cadastro/', views.cadastro, name='cadastro')
path('login/', LoginView.as_view(template_name='accounts/login.html', authentication_form=LoginUsuarioForm, redirect_authenticated_user=True), name='login')
path('logout/', LogoutView.as_view(), name='logout')
path('dashboard/', views.dashboard, name='dashboard')
path('hemocentros/validacao/', views.painel_aprovacao_hemocentros, name='painel_aprovacao_hemocentros')
path('hemocentros/pendentes/', views.hemocentros_pendentes, name='hemocentros_pendentes')
path('hemocentros/<int:id_hemocentro>/aprovar/', views.aprovar_hemocentro, name='aprovar_hemocentro')
path('hemocentros/<int:id_hemocentro>/recusar/', views.recusar_hemocentro, name='recusar_hemocentro')
path('hemocentros/<int:id_hemocentro>/solicitar-correcao/', views.solicitar_correcao_hemocentro, name='solicitar_correcao_hemocentro')
path('pedidos/publicar/', views.criar_pedido_sangue, name='pedido_publicar')
path('pedidos/', views.consultar_pedidos, name='consultar_pedidos')
path('pedidos/novo/', views.criar_pedido_sangue, name='criar_pedido_sangue')
path('pedidos/minhas-solicitacoes/', views.minhas_solicitacoes, name='minhas_solicitacoes')
path('pedidos/hemocentro/', views.painel_pedidos_hemocentro, name='painel_pedidos_hemocentro')
path('pedidos/validacao/', views.painel_validacao_pedidos, name='painel_validacao_pedidos')
path('pedidos/<int:id_pedido>/aprovar/', views.aprovar_pedido, name='aprovar_pedido')
path('pedidos/<int:id_pedido>/recusar/', views.recusar_pedido, name='recusar_pedido')
path('pedidos/<int:id_pedido>/correcao/', views.solicitar_correcao_pedido, name='solicitar_correcao_pedido')
path('pedidos/<int:id_pedido>/suspeito/', views.marcar_pedido_suspeito, name='marcar_pedido_suspeito')
path('triagem/', views.triagem_apresentacao, name='triagem_apresentacao')
path('triagem/iniciar/<str:modalidade>/', views.triagem_iniciar, name='triagem_iniciar')
path('triagem/<int:id_triagem>/pergunta/', views.triagem_pergunta, name='triagem_pergunta')
path('triagem/<int:id_triagem>/resultado/', views.triagem_resultado, name='triagem_resultado')
path('triagem/<int:id_triagem>/revisao/', views.triagem_revisao, name='triagem_revisao')
path('triagens/historico/', views.triagem_historico, name='triagem_historico')
path('compatibilidade-sanguinea/', views.compatibilidade_sanguinea, name='compatibilidade_sanguinea')
path('estoque/', views.visualizacao_publica_estoque, name='estoque_publico')
path('estoque/hemocentro/', views.estoque_hemocentro, name='estoque_hemocentro')
path('estoque/hemocentro/cadastrar/', views.cadastrar_estoque_view, name='cadastrar_estoque')
path('estoque/hemocentro/<int:id_estoque>/atualizar/', views.atualizar_estoque_view, name='atualizar_estoque')
```


## accounts/validacao_hemocentro.py

Estados institucionais, decisao e historico de hemocentros.

Original: [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py>).

**Dependencias importadas:**

```python
from functools import wraps
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from .auditoria import registrar_auditoria
from .models import AuditoriaAcaoCritica, Usuario, ValidacaoHemocentro
```

### usuario_e_administrador

Linha 17: [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:17>).

```python
def usuario_e_administrador(usuario):
```

**Chamadas utilizadas no corpo:** `bool`, `getattr`.

**Expressoes de retorno (dependem do caminho):**

- `bool(getattr(usuario, 'is_authenticated', False) and (usuario.is_superuser or usuario.perfil == Usuario.Perfil.ADMINISTRADOR))`

**Onde aparece uma chamada com este nome:**

- `registrar_decisao_validacao_hemocentro` em [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:68>).
- `registrar_decisao_validacao_pedido` em [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:174>).
- `montar_visibilidade_dashboard` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:477>).
- `exigir_administrador` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:545>).
- `marcar_pedido_suspeito` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1872>).

### usuario_e_hemocentro

Linha 27: [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:27>).

```python
def usuario_e_hemocentro(usuario):
```

**Chamadas utilizadas no corpo:** `bool`, `getattr`.

**Expressoes de retorno (dependem do caminho):**

- `bool(getattr(usuario, 'is_authenticated', False) and usuario.perfil == Usuario.Perfil.HEMOCENTRO)`

**Onde aparece uma chamada com este nome:**

- `hemocentro_aprovado` em [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:34>).
- `validar_publicacao_hemocentro` em [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:41>).

### hemocentro_aprovado

Linha 34: [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:34>).

```python
def hemocentro_aprovado(usuario):
```

**Chamadas utilizadas no corpo:** `usuario_e_hemocentro`.

**Expressoes de retorno (dependem do caminho):**

- `usuario_e_hemocentro(usuario) and usuario.status_validacao == Usuario.StatusValidacaoHemocentro.APROVADO`

**Onde aparece uma chamada com este nome:**

- `ValidacaoHemocentroTests.test_hemocentro_inicia_pendente` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:79>).
- `validar_publicacao_hemocentro` em [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:41>).
- `registrar_decisao_validacao_pedido` em [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:174>).
- `dashboard` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:720>).
- `aprovar_pedido` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1802>).

### validar_publicacao_hemocentro

Linha 41: [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:41>).

```python
def validar_publicacao_hemocentro(usuario):
```

**Chamadas utilizadas no corpo:** `PermissionDenied`, `getattr`, `hemocentro_aprovado`, `usuario.get_status_validacao_display`, `usuario_e_hemocentro`.

**Expressoes de retorno (dependem do caminho):**

- `True`

**Excecoes levantadas:**

- `PermissionDenied('Faca login para publicar estoque ou campanha.')`
- `PermissionDenied('Somente usuarios com perfil Hemocentro podem publicar estoque ou campanha.')`
- `PermissionDenied(f'Hemocentro ainda nao aprovado. Status atual: {usuario.get_status_validacao_display()}.')`

**Estrutura de controle:** If: 3. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `validar_responsavel_pelo_estoque` em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:104>).
- `cadastrar_estoque` em [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py:131>).
- `ValidacaoHemocentroTests.test_hemocentro_nao_aprovado_nao_publica` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:171>).
- `ValidacaoHemocentroTests.test_hemocentro_aprovado_pode_publicar` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:185>).
- `exigir_hemocentro_aprovado.wrapper` em [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:61>).
- `aprovar_pedido` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1802>).
- `recusar_pedido` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1830>).

### exigir_hemocentro_aprovado

Linha 59: [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:59>).

```python
def exigir_hemocentro_aprovado(view_func):
```

**Expressoes de retorno (dependem do caminho):**

- `wrapper`

### exigir_hemocentro_aprovado.wrapper

Linha 61: [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:61>).

```python
def wrapper(request, *args, **kwargs):
```

**Decoradores:** `wraps(view_func)`.

**Chamadas utilizadas no corpo:** `validar_publicacao_hemocentro`, `view_func`.

**Expressoes de retorno (dependem do caminho):**

- `view_func(request, *args, **kwargs)`

### registrar_decisao_validacao_hemocentro

Linha 68: [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:68>).

```python
def registrar_decisao_validacao_hemocentro(*, hemocentro, admin, status, parecer='', request=None):
```

**Chamadas utilizadas no corpo:** `(parecer or '').strip`, `PARECER_PADRAO.get`, `PermissionDenied`, `Usuario.objects.select_for_update`, `Usuario.objects.select_for_update().get`, `ValidacaoHemocentro.objects.create`, `ValidationError`, `hemocentro_atualizado.save`, `registrar_auditoria`, `transaction.atomic`, `usuario_e_administrador`.

**Expressoes de retorno (dependem do caminho):**

- `validacao`

**Excecoes levantadas:**

- `PermissionDenied('Hemocentros nao podem validar cadastros institucionais.')`
- `PermissionDenied('Somente administradores podem validar Hemocentros.')`
- `ValidationError('Somente usuarios com perfil Hemocentro podem passar por validacao.')`

**Estrutura de controle:** If: 3, With: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `aprovar_hemocentro` em [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:125>).
- `recusar_hemocentro` em [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:135>).
- `solicitar_correcao_hemocentro` em [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:145>).

### aprovar_hemocentro

Linha 125: [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:125>).

```python
def aprovar_hemocentro(*, hemocentro, admin, parecer='', request=None):
```

**Chamadas utilizadas no corpo:** `registrar_decisao_validacao_hemocentro`.

**Expressoes de retorno (dependem do caminho):**

- `registrar_decisao_validacao_hemocentro(hemocentro=hemocentro, admin=admin, status=Usuario.StatusValidacaoHemocentro.APROVADO, parecer=parecer, request=request)`

**Onde aparece uma chamada com este nome:**

- `EstoqueTestsBase.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:42>).
- `RegistrarMovimentacaoEstoqueTests.test_outro_hemocentro_nao_pode_movimentar_estoque_alheio` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:288>).
- `FluxoCadastroTriagemPedidosTests.setUp` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:28>).
- `PedidoSangueTests.setUp` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:21>).
- `VisualizacaoPublicaTests.setUp` em [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:23>).
- `ValidacaoHemocentroTests.test_admin_aprova_e_cria_historico` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:88>).
- `ValidacaoHemocentroTests.test_usuario_comum_nao_pode_validar` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:156>).
- `ValidacaoHemocentroTests.test_hemocentro_aprovado_pode_publicar` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:185>).

### recusar_hemocentro

Linha 135: [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:135>).

```python
def recusar_hemocentro(*, hemocentro, admin, parecer='', request=None):
```

**Chamadas utilizadas no corpo:** `registrar_decisao_validacao_hemocentro`.

**Expressoes de retorno (dependem do caminho):**

- `registrar_decisao_validacao_hemocentro(hemocentro=hemocentro, admin=admin, status=Usuario.StatusValidacaoHemocentro.RECUSADO, parecer=parecer, request=request)`

**Onde aparece uma chamada com este nome:**

- `ValidacaoHemocentroTests.test_admin_recusa` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:120>).

### solicitar_correcao_hemocentro

Linha 145: [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:145>).

```python
def solicitar_correcao_hemocentro(*, hemocentro, admin, parecer='', request=None):
```

**Chamadas utilizadas no corpo:** `registrar_decisao_validacao_hemocentro`.

**Expressoes de retorno (dependem do caminho):**

- `registrar_decisao_validacao_hemocentro(hemocentro=hemocentro, admin=admin, status=Usuario.StatusValidacaoHemocentro.CORRECAO, parecer=parecer, request=request)`

**Onde aparece uma chamada com este nome:**

- `ValidacaoHemocentroTests.test_admin_solicita_correcao` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:140>).

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `PARECER_PADRAO`: linha 10; valor declarado em [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py:10>).

## accounts/validacao_pedido.py

Solicitacao, decisao, historico e autorizacao de pedidos.

Original: [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py>).

**Dependencias importadas:**

```python
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.validators import validate_email
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from .auditoria import registrar_auditoria
from .models import AuditoriaAcaoCritica, PedidoSangue, Usuario, ValidacaoPedido
from .validacao_hemocentro import hemocentro_aprovado, usuario_e_administrador
```

### validar_dados_pedido

Linha 53: [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:53>).

```python
def validar_dados_pedido(pedido):
```

**Explicacao presente no codigo:**

> Valida as informações básicas antes da decisão administrativa.

**Chamadas utilizadas no corpo:** `ValidationError`, `pedido.cidade.strip`, `pedido.contato.strip`, `pedido.descricao.strip`, `pedido.nome_solicitante.strip`, `pedido.titulo.strip`, `validate_email`.

**Excecoes levantadas:**

- `ValidationError('Informe a cidade.')`
- `ValidationError('Informe a descrição do pedido.')`
- `ValidationError('Informe a urgência.')`
- `ValidationError('Informe o Hemocentro de destino.')`
- `ValidationError('Informe o nome ou identificação do solicitante.')`
- `ValidationError('Informe o tipo sanguíneo.')`
- `ValidationError('Informe um e-mail para retorno.')`
- `ValidationError('Informe um e-mail válido para retorno.')`
- `ValidationError('O Hemocentro de destino precisa estar aprovado.')`
- `ValidationError('O destino precisa ser um Hemocentro.')`
- `ValidationError('O pedido precisa possuir um título.')`

**Estrutura de controle:** If: 10, Try: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `criar_pedido_pendente` em [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:116>).
- `registrar_decisao_validacao_pedido` em [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:174>).

### criar_pedido_pendente

Linha 116: [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:116>).

```python
def criar_pedido_pendente(*, dados, solicitante):
```

**Explicacao presente no codigo:**

> Cria o pedido sem publicá-lo.

**Chamadas utilizadas no corpo:** `PedidoSangue`, `PedidoSangue.objects.filter`, `PedidoSangue.objects.filter(hemocentro_destino=pedido.hemocentro_destino, tipo_sanguineo=pedido.tipo_sanguineo, cidade__iexact=pedido.cidade, data_criacao__gte=limite).exclude`, `PedidoSangue.objects.filter(hemocentro_destino=pedido.hemocentro_destino, tipo_sanguineo=pedido.tipo_sanguineo, cidade__iexact=pedido.cidade, data_criacao__gte=limite).exclude(pk=pedido.pk).filter`, `PedidoSangue.objects.filter(hemocentro_destino=pedido.hemocentro_destino, tipo_sanguineo=pedido.tipo_sanguineo, cidade__iexact=pedido.cidade, data_criacao__gte=limite).exclude(pk=pedido.pk).filter(status__in=[PedidoSangue.Status.ENVIADA, PedidoSangue.Status.EM_ANALISE, PedidoSangue.Status.PUBLICADA, PedidoSangue.Status.CORRECAO_SOLICITADA]).exists`, `PermissionDenied`, `Usuario.objects.get`, `ValidationError`, `dados.get`, `dict`, `getattr`, `hasattr`, `pedido.full_clean`, `pedido.save`, `timedelta`, `timezone.now`, `validar_dados_pedido`.

**Expressoes de retorno (dependem do caminho):**

- `pedido`

**Excecoes levantadas:**

- `PermissionDenied('Somente Receptor pode enviar solicitacao de pedido de sangue.')`
- `ValidationError('Hemocentro de destino inválido.')`

**Estrutura de controle:** If: 3, Try: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `FluxoCadastroTriagemPedidosTests.test_receptor_acompanha_somente_suas_solicitacoes` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:277>).
- `FluxoCadastroTriagemPedidosTests.test_publicacao_notifica_somente_doador_apto_compativel` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:323>).
- `PedidoSangueTests.test_admin_moderar_pedido_nao_publica` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:181>).
- `criar_pedido_sangue` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1542>).

### registrar_decisao_validacao_pedido

Linha 174: [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:174>).

```python
def registrar_decisao_validacao_pedido(*, pedido, moderador, status_validacao, motivo='', request=None):
```

**Explicacao presente no codigo:**

> Registra a decisão administrativa e atualiza
> o status do pedido.

**Decoradores:** `transaction.atomic`.

**Chamadas utilizadas no corpo:** `(motivo or '').strip`, `PedidoSangue.objects.select_for_update`, `PedidoSangue.objects.select_for_update().get`, `PermissionDenied`, `ValidacaoPedido.objects.create`, `ValidationError`, `criar_notificacoes_para_pedido`, `hemocentro_aprovado`, `pedido.save`, `registrar_auditoria`, `timezone.now`, `usuario_e_administrador`, `validar_dados_pedido`.

**Expressoes de retorno (dependem do caminho):**

- `validacao`

**Excecoes levantadas:**

- `PermissionDenied('Somente o Hemocentro aprovado de destino pode analisar e publicar pedidos.')`
- `PermissionDenied('Somente o administrador ou o Hemocentro aprovado de destino pode marcar um pedido como suspeito.')`
- `ValidationError('Não é possível validar um pedido encerrado.')`
- `ValidationError('Status de validação inválido.')`

**Estrutura de controle:** If: 14. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `aprovar_pedido` em [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:323>).
- `recusar_pedido` em [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:341>).
- `solicitar_correcao_pedido` em [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:359>).
- `marcar_pedido_suspeito` em [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:377>).

### aprovar_pedido

Linha 323: [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:323>).

```python
def aprovar_pedido(*, pedido, moderador, motivo='', request=None):
```

**Chamadas utilizadas no corpo:** `registrar_decisao_validacao_pedido`.

**Expressoes de retorno (dependem do caminho):**

- `registrar_decisao_validacao_pedido(pedido=pedido, moderador=moderador, status_validacao=ValidacaoPedido.StatusValidacao.APROVADO, motivo=motivo, request=request)`

**Onde aparece uma chamada com este nome:**

- `FluxoCadastroTriagemPedidosTests.test_solicitacao_nao_publica_e_hemocentro_publica` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:230>).
- `FluxoCadastroTriagemPedidosTests.test_publicacao_notifica_somente_doador_apto_compativel` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:323>).
- `PedidoSangueTests.test_hemocentro_aprova_pedido_e_registra_historico` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:159>).
- `PedidoSangueTests.test_publicacao_exclusiva_do_hemocentro_responsavel` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:228>).
- `PedidoSangueTests.test_auditoria_distingue_validacao_e_publicacao` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:256>).

### recusar_pedido

Linha 341: [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:341>).

```python
def recusar_pedido(*, pedido, moderador, motivo='', request=None):
```

**Chamadas utilizadas no corpo:** `registrar_decisao_validacao_pedido`.

**Expressoes de retorno (dependem do caminho):**

- `registrar_decisao_validacao_pedido(pedido=pedido, moderador=moderador, status_validacao=ValidacaoPedido.StatusValidacao.RECUSADO, motivo=motivo, request=request)`

### solicitar_correcao_pedido

Linha 359: [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:359>).

```python
def solicitar_correcao_pedido(*, pedido, moderador, motivo='', request=None):
```

**Chamadas utilizadas no corpo:** `registrar_decisao_validacao_pedido`.

**Expressoes de retorno (dependem do caminho):**

- `registrar_decisao_validacao_pedido(pedido=pedido, moderador=moderador, status_validacao=ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA, motivo=motivo, request=request)`

### marcar_pedido_suspeito

Linha 377: [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py:377>).

```python
def marcar_pedido_suspeito(*, pedido, moderador, motivo='', request=None):
```

**Chamadas utilizadas no corpo:** `registrar_decisao_validacao_pedido`.

**Expressoes de retorno (dependem do caminho):**

- `registrar_decisao_validacao_pedido(pedido=pedido, moderador=moderador, status_validacao=ValidacaoPedido.StatusValidacao.SUSPEITO, motivo=motivo, request=request)`

**Onde aparece uma chamada com este nome:**

- `PedidoSangueTests.test_auditoria_distingue_validacao_e_publicacao` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:256>).


## accounts/views.py

Entrada HTTP: permissoes, formularios, chamadas de servico e respostas/telas.

Original: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py>).

**Dependencias importadas:**

```python
from django import forms
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.utils import timezone
from django.db import transaction
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Case, IntegerField, Prefetch, Value, When
from .forms import CadastrarEstoqueForm, CadastroUsuarioForm, PreferenciaConvocacaoForm, MovimentarEstoqueForm, FiltroEstoquePublicoForm, PedidoSangueForm, FiltroPedidoSangueForm
from .auditoria import registrar_auditoria
from .models import ConsentimentoLGPD, Estoque, EstoqueMovimentacao, PedidoSangue, Triagem, Usuario, ValidacaoHemocentro, ValidacaoPedido, AuditoriaAcaoCritica
from .estoque import cadastrar_estoque, obter_estoques_publicos, registrar_movimentacao_estoque
from .validacao_hemocentro import aprovar_hemocentro as aprovar_hemocentro_servico, exigir_hemocentro_aprovado, validar_publicacao_hemocentro, hemocentro_aprovado, recusar_hemocentro as recusar_hemocentro_servico, solicitar_correcao_hemocentro as solicitar_correcao_hemocentro_servico, usuario_e_administrador
from .compatibilidade import TIPOS_SANGUINEOS, doadores_compativeis_para, tabela_de_compatibilidade, tipos_que_recebem_de, atualizar_preferencia_convocacao
from django.conf import settings
from .triagem_servico import TriagemExtensaNecessaria, TriagemIncompleta, PerguntaInvalida, TriagemSimplificadaIndisponivel, concluir_triagem, iniciar_triagem, obter_extensa_base, obter_extensa_reutilizavel, editar_pergunta, obter_pergunta_atual, pode_responder, salvar_resposta, voltar_pergunta
from .triagem_forms import FormularioPergunta as FormularioPerguntaTriagem
from .triagem_catalogo import obter_pergunta
from .validacao_pedido import aprovar_pedido as aprovar_pedido_servico, marcar_pedido_suspeito as marcar_pedido_suspeito_servico, recusar_pedido as recusar_pedido_servico, solicitar_correcao_pedido as solicitar_correcao_pedido_servico, criar_pedido_pendente
```

### FormularioPergunta

Linha 119: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:119>).

Classe; herda de: forms.Form.

**Explicacao presente no codigo:**

> Formulario dinamico usado pela triagem por etapas.
> 
> A pergunta vem da camada triagem_servico como um dicionario. O formulario
> aceita os formatos de resposta mais comuns do projeto sem obrigar cada
> pergunta a ter uma classe de formulario separada.

**Onde aparece uma chamada com este nome:**

- `FormularioPerguntaTests.test_escolha_com_data_e_normalizada` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:12>).
- `FormularioPerguntaTests.test_selecao_multipla_preserva_uma_data_por_item` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:33>).
- `FormularioPerguntaTests.test_data_futura_e_rejeitada` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:54>).
- `FormularioPerguntaTests.test_alternativa_com_prazo_exige_sua_data` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:68>).
- `FormularioPerguntaTests.test_nenhuma_nao_pode_ser_marcada_com_uma_condicao` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:79>).
- `FormularioPerguntaTests.test_descricao_e_obrigatoria_quando_usuario_informa_outra_condicao` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:92>).
- `FormularioPerguntaTests.test_procedimento_estetico_registra_seguranca_e_inflamacao` em [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py:103>).

### FormularioPergunta.__init__

Linha 128: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:128>).

```python
def __init__(self, pergunta, *args, valor_inicial=None, **kwargs):
```

**Chamadas utilizadas no corpo:** `forms.CharField`, `forms.ChoiceField`, `forms.DateField`, `forms.DateInput`, `forms.DecimalField`, `forms.MultipleChoiceField`, `forms.TextInput`, `forms.Textarea`, `pergunta.get`, `self._normalizar_opcoes`, `self._normalizar_valor_inicial`, `str`, `str(pergunta.get('tipo_resposta') or pergunta.get('tipo') or pergunta.get('formato') or 'ESCOLHA').strip`, `str(pergunta.get('tipo_resposta') or pergunta.get('tipo') or pergunta.get('formato') or 'ESCOLHA').strip().upper`, `super`, `super().__init__`.

**Estrutura de controle:** If: 5. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `CadastroUsuarioForm.__init__` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:149>).
- `PedidoSangueForm.__init__` em [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py:642>).
- `FormularioPergunta.__init__` em [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py:27>).

### FormularioPergunta._primeiro_valor

Linha 244: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:244>).

```python
def _primeiro_valor(dados, chaves):
```

**Decoradores:** `staticmethod`.

**Expressoes de retorno (dependem do caminho):**

- `None`
- `dados[chave]`

**Estrutura de controle:** For: 1, If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `FormularioPergunta._normalizar_opcoes` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:252>).
- `FormularioPergunta._normalizar_valor_inicial` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:320>).

### FormularioPergunta._normalizar_opcoes

Linha 252: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:252>).

```python
def _normalizar_opcoes(cls, opcoes):
```

**Explicacao presente no codigo:**

> Converte opcoes em pares (valor, rotulo).
> 
> Aceita:
> 
> - lista de dicionarios;
> 
> - lista de tuplas;
> 
> - lista de textos;
> 
> - dicionario no formato codigo -> rotulo.

**Decoradores:** `classmethod`.

**Chamadas utilizadas no corpo:** `cls._primeiro_valor`, `isinstance`, `len`, `opcoes.items`, `resultado.append`, `str`.

**Expressoes de retorno (dependem do caminho):**

- `[(str(valor), str(rotulo)) for valor, rotulo in opcoes.items()]`
- `resultado`

**Estrutura de controle:** If: 5, For: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `FormularioPergunta.__init__` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:128>).

### FormularioPergunta._normalizar_valor_inicial

Linha 320: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:320>).

```python
def _normalizar_valor_inicial(cls, valor):
```

**Decoradores:** `classmethod`.

**Chamadas utilizadas no corpo:** `cls._primeiro_valor`, `isinstance`.

**Expressoes de retorno (dependem do caminho):**

- `cls._primeiro_valor(valor, ('valor', 'codigo', 'codigo_resposta', 'resposta', 'opcao', 'data', 'numero', 'texto'))`
- `valor`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `FormularioPergunta.__init__` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:128>).

### montar_visibilidade_dashboard

Linha 477: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:477>).

```python
def montar_visibilidade_dashboard(usuario, painel):
```

**Explicacao presente no codigo:**

> Centraliza a particularizacao do dashboard por perfil.
> 
> O dicionario PAINEIS_POR_PERFIL define o que cada tipo de conta pode ver
> por padrao. Esta funcao acrescenta regras que dependem do estado atual do
> usuario, como Hemocentro aprovado e Administrador.

**Chamadas utilizadas no corpo:** `painel.get`, `usuario_e_administrador`.

**Expressoes de retorno (dependem do caminho):**

- `{'mostra_triagem': painel.get('mostra_triagem', False), 'mostra_campanhas': painel.get('mostra_campanhas', False), 'mostra_pedidos': painel.get('mostra_pedidos', False) and (usuario.perfil != Usuario.Perfil.HEMOCENTRO or hemocentro_aprovado), 'mostra_estoque_publico': painel.get('mostra_estoque_publico', False), 'mostra_postos': painel.get('mostra_postos', False), 'pode_solicitar_divulgacao': usuario.perfil == Usuario.Perfil.RECEPTOR, 'mostra_status_hemocentro': usuario.perfil == Usuario.Perfil.HEMOCENTRO, 'pode_solicitar_pedido': usuario.perfil == Usuario.Perfil.RECEPTOR, 'pode_gerenciar_estoque': hemocentro_aprovado, 'pode_analisar_pedidos': hemocentro_aprovado, 'pode_aprovar_hemocentros': administrador, 'pode_moderar_pedidos': administrador}`

**Onde aparece uma chamada com este nome:**

- `dashboard` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:720>).

### obter_ip

Linha 511: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:511>).

```python
def obter_ip(request):
```

**Explicacao presente no codigo:**

> Extrai o IP usado no registro do consentimento LGPD.

**Chamadas utilizadas no corpo:** `encaminhado.split`, `encaminhado.split(',')[0].strip`, `request.META.get`.

**Expressoes de retorno (dependem do caminho):**

- `encaminhado.split(',')[0].strip()`
- `request.META.get('REMOTE_ADDR')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `registrar_auditoria` em [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py:81>).
- `atualizar_preferencia_convocacao` em [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py:112>).
- `auditar_login_falho` em [accounts/signals.py](<C:/Users/lb119/Elo/accounts/signals.py:23>).
- `AuditoriaTests.test_ip_nao_confia_em_cabecalho_do_cliente` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:418>).
- `cadastro` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:588>).
- `triagem_iniciar` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1074>).
- `triagem_pergunta` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1138>).

### filtrar_postos

Linha 522: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:522>).

```python
def filtrar_postos(consulta):
```

**Explicacao presente no codigo:**

> Filtra a lista publica por nome, cidade, estado ou endereco.

**Chamadas utilizadas no corpo:** `' '.join`, `' '.join([posto['nome'], posto['cidade'], posto['estado'], posto['endereco']]).lower`, `(consulta or '').strip`, `(consulta or '').strip().lower`.

**Expressoes de retorno (dependem do caminho):**

- `POSTOS_COLETA`
- `[posto for posto in POSTOS_COLETA if termo in ' '.join([posto['nome'], posto['cidade'], posto['estado'], posto['endereco']]).lower()]`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `inicio` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:564>).

### exigir_administrador

Linha 545: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:545>).

```python
def exigir_administrador(usuario):
```

**Explicacao presente no codigo:**

> Bloqueia acoes institucionais para quem nao e administrador.

**Chamadas utilizadas no corpo:** `PermissionDenied`, `usuario_e_administrador`.

**Excecoes levantadas:**

- `PermissionDenied('Somente administradores podem executar esta acao.')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `painel_aprovacao_hemocentros` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:826>).
- `hemocentros_pendentes` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:854>).
- `aprovar_hemocentro` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:893>).
- `recusar_hemocentro` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:921>).
- `solicitar_correcao_hemocentro` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:949>).
- `painel_validacao_pedidos` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1760>).

### obter_hemocentro_ou_404

Linha 554: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:554>).

```python
def obter_hemocentro_ou_404(id_hemocentro):
```

**Explicacao presente no codigo:**

> Busca somente contas cadastradas com perfil Hemocentro.

**Chamadas utilizadas no corpo:** `get_object_or_404`.

**Expressoes de retorno (dependem do caminho):**

- `get_object_or_404(Usuario, pk=id_hemocentro, perfil=Usuario.Perfil.HEMOCENTRO)`

**Onde aparece uma chamada com este nome:**

- `aprovar_hemocentro` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:893>).
- `recusar_hemocentro` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:921>).
- `solicitar_correcao_hemocentro` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:949>).

### inicio

Linha 564: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:564>).

```python
def inicio(request):
```

**Explicacao presente no codigo:**

> Mostra o acesso publico usado pelo ator Visitante.

**Chamadas utilizadas no corpo:** `PedidoSangue.objects.select_related`, `PedidoSangue.objects.select_related('hemocentro_destino').filter`, `PedidoSangue.objects.select_related('hemocentro_destino').filter(status=PedidoSangue.Status.PUBLICADA).order_by`, `filtrar_postos`, `render`, `request.GET.get`.

**Expressoes de retorno (dependem do caminho):**

- `render(request, 'accounts/inicio.html', contexto)`

### cadastro

Linha 588: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:588>).

```python
def cadastro(request):
```

**Explicacao presente no codigo:**

> Exibe e processa o cadastro de usuarios.
> 
> Hemocentro:
> 
> - cria a conta;
> 
> - fica com status PENDENTE;
> 
> - registra consentimento LGPD;
> 
> - entra no sistema;
> 
> - recebe a mensagem de aguardando aprovacao.

**Chamadas utilizadas no corpo:** `CadastroUsuarioForm`, `ConsentimentoLGPD.objects.create`, `atualizar_preferencia_convocacao`, `form.is_valid`, `form.save`, `login`, `messages.error`, `messages.success`, `obter_ip`, `redirect`, `render`, `transaction.atomic`, `usuario.save`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:dashboard')`
- `render(request, 'accounts/cadastro.html', {'form': form})`

**Estrutura de controle:** If: 6, With: 1. Abra o original para seguir as condicoes na ordem.

### compatibilidade_sanguinea

Linha 681: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:681>).

```python
def compatibilidade_sanguinea(request):
```

**Explicacao presente no codigo:**

> Exibe a tabela e a consulta de compatibilidade sanguinea.

**Chamadas utilizadas no corpo:** `doadores_compativeis_para`, `render`, `request.GET.get`, `tabela_de_compatibilidade`, `tipo_selecionado.strip`, `tipo_selecionado.strip().upper`, `tipos_que_recebem_de`.

**Expressoes de retorno (dependem do caminho):**

- `render(request, 'accounts/compatibilidade_sanguinea.html', {'tipos_sanguineos': TIPOS_SANGUINEOS, 'tipo_selecionado': tipo_selecionado, 'compatibilidade_selecionada': compatibilidade_selecionada, 'tipo_invalido': tipo_invalido, 'tabela_compatibilidade': tabela_de_compatibilidade()})`

**Estrutura de controle:** If: 1, Try: 1. Abra o original para seguir as condicoes na ordem.

### dashboard

Linha 720: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:720>).

```python
def dashboard(request):
```

**Explicacao presente no codigo:**

> Mostra o painel protegido particularizado pelo perfil do usuario.

**Decoradores:** `login_required`.

**Chamadas utilizadas no corpo:** `Http404`, `PAINEIS_POR_PERFIL.get`, `Paginator`, `Paginator(notificacoes_usuario, 10).get_page`, `PedidoSangue.objects.select_related`, `PedidoSangue.objects.select_related('hemocentro_destino').filter`, `PedidoSangue.objects.select_related('hemocentro_destino').filter(status=PedidoSangue.Status.PUBLICADA).order_by`, `PermissionDenied`, `PreferenciaConvocacaoForm`, `ValidacaoHemocentro.objects.filter`, `ValidacaoHemocentro.objects.filter(hemocentro=request.user).order_by`, `ValidacaoHemocentro.objects.filter(hemocentro=request.user).order_by('-data_analise').first`, `atualizar_preferencia_convocacao`, `form.is_valid`, `get_object_or_404`, `hemocentro_aprovado`, `int`, `messages.success`, `montar_visibilidade_dashboard`, `notificacoes_usuario.filter`, `notificacoes_usuario.filter(lida=False).count`, `pode_responder`, `redirect`, `render`, `request.GET.get`, `request.POST.get`, `request.user.consentimentos_lgpd.filter`, `request.user.consentimentos_lgpd.filter(tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES, versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO, aceito=True, revogado_em__isnull=True).exists`, `request.user.notificacoes.filter`, `request.user.notificacoes.filter(pk=notificacao.pk, lida=False).update`, `request.user.notificacoes.order_by`, `request.user.triagens.order_by`, `request.user.triagens.order_by('-iniciada_em').first`, `timezone.now`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:dashboard')`
- `render(request, 'accounts/dashboard.html', contexto)`

**Excecoes levantadas:**

- `Http404('Notificacao nao encontrada.')`
- `PermissionDenied('Somente Doadores podem configurar convocacoes.')`

**Estrutura de controle:** If: 9, Try: 1. Abra o original para seguir as condicoes na ordem.

### painel_aprovacao_hemocentros

Linha 826: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:826>).

```python
def painel_aprovacao_hemocentros(request):
```

**Explicacao presente no codigo:**

> Mostra a tela administrativa de aprovacao de Hemocentros.

**Decoradores:** `login_required`.

**Chamadas utilizadas no corpo:** `Usuario.objects.filter`, `Usuario.objects.filter(perfil=Usuario.Perfil.HEMOCENTRO, status_validacao=Usuario.StatusValidacaoHemocentro.PENDENTE).order_by`, `exigir_administrador`, `render`.

**Expressoes de retorno (dependem do caminho):**

- `render(request, 'accounts/painel_aprovacao_hemocentros.html', contexto)`

### hemocentros_pendentes

Linha 854: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:854>).

```python
def hemocentros_pendentes(request):
```

**Explicacao presente no codigo:**

> Retorna os Hemocentros que ainda aguardam decisao administrativa.

**Decoradores:** `login_required`.

**Chamadas utilizadas no corpo:** `JsonResponse`, `Usuario.objects.filter`, `Usuario.objects.filter(perfil=Usuario.Perfil.HEMOCENTRO, status_validacao=Usuario.StatusValidacaoHemocentro.PENDENTE).order_by`, `exigir_administrador`, `hemocentro.date_joined.isoformat`.

**Expressoes de retorno (dependem do caminho):**

- `JsonResponse({'hemocentros': dados})`

### aprovar_hemocentro

Linha 893: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:893>).

```python
def aprovar_hemocentro(request, id_hemocentro):
```

**Explicacao presente no codigo:**

> Acao administrativa para aprovar um Hemocentro.

**Decoradores:** `login_required`, `require_POST`.

**Chamadas utilizadas no corpo:** `aprovar_hemocentro_servico`, `exigir_administrador`, `messages.success`, `obter_hemocentro_ou_404`, `redirect`, `request.POST.get`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:painel_aprovacao_hemocentros')`

**Onde aparece uma chamada com este nome:**

- `EstoqueTestsBase.setUp` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:42>).
- `RegistrarMovimentacaoEstoqueTests.test_outro_hemocentro_nao_pode_movimentar_estoque_alheio` em [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py:288>).
- `FluxoCadastroTriagemPedidosTests.setUp` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:28>).
- `PedidoSangueTests.setUp` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:21>).
- `VisualizacaoPublicaTests.setUp` em [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py:23>).
- `ValidacaoHemocentroTests.test_admin_aprova_e_cria_historico` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:88>).
- `ValidacaoHemocentroTests.test_usuario_comum_nao_pode_validar` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:156>).
- `ValidacaoHemocentroTests.test_hemocentro_aprovado_pode_publicar` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:185>).

### recusar_hemocentro

Linha 921: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:921>).

```python
def recusar_hemocentro(request, id_hemocentro):
```

**Explicacao presente no codigo:**

> Acao administrativa para recusar um Hemocentro.

**Decoradores:** `login_required`, `require_POST`.

**Chamadas utilizadas no corpo:** `exigir_administrador`, `messages.success`, `obter_hemocentro_ou_404`, `recusar_hemocentro_servico`, `redirect`, `request.POST.get`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:painel_aprovacao_hemocentros')`

**Onde aparece uma chamada com este nome:**

- `ValidacaoHemocentroTests.test_admin_recusa` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:120>).

### solicitar_correcao_hemocentro

Linha 949: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:949>).

```python
def solicitar_correcao_hemocentro(request, id_hemocentro):
```

**Explicacao presente no codigo:**

> Solicita correcao cadastral para um Hemocentro.

**Decoradores:** `login_required`, `require_POST`.

**Chamadas utilizadas no corpo:** `exigir_administrador`, `messages.success`, `obter_hemocentro_ou_404`, `redirect`, `request.POST.get`, `solicitar_correcao_hemocentro_servico`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:painel_aprovacao_hemocentros')`

**Onde aparece uma chamada com este nome:**

- `ValidacaoHemocentroTests.test_admin_solicita_correcao` em [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py:140>).

### triagem_apresentacao

Linha 975: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:975>).

```python
def triagem_apresentacao(request):
```

**Explicacao presente no codigo:**

> Exibe a apresentação pública da triagem.
> 
> Somente usuários com perfil permitido podem iniciar a triagem.
> 
> A modalidade simplificada é liberada quando existe uma triagem
> extensa concluída que possa ser utilizada como base.

**Chamadas utilizadas no corpo:** `obter_extensa_base`, `obter_extensa_reutilizavel`, `pode_responder`, `render`, `request.user.triagens.select_related`, `request.user.triagens.select_related('triagem_base').order_by`, `triagens.filter`, `triagens.filter(status=Triagem.Status.EM_ANDAMENTO).first`, `triagens.first`.

**Expressoes de retorno (dependem do caminho):**

- `render(request, 'accounts/triagem_apresentacao.html', {'pode_iniciar': pode_iniciar, 'pode_simplificada': pode_simplificada, 'triagem_em_andamento': triagem_em_andamento, 'ultima_triagem': ultima_triagem, 'triagem_extensa_base': extensa_base, 'triagem_extensa_reutilizavel': extensa_reutilizavel})`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

### triagem_historico

Linha 1032: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1032>).

```python
def triagem_historico(request):
```

**Explicacao presente no codigo:**

> Lista somente as triagens pertencentes ao usuario autenticado.
> 
> O historico mostra tanto triagens em andamento quanto concluidas e
> canceladas, permitindo que o template ofereça continuar ou consultar
> o resultado conforme o status.

**Decoradores:** `login_required`.

**Chamadas utilizadas no corpo:** `messages.error`, `pode_responder`, `redirect`, `registrar_auditoria`, `render`, `request.user.triagens.select_related`, `request.user.triagens.select_related('triagem_base').order_by`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:dashboard')`
- `render(request, 'accounts/triagem_historico.html', {'triagens': triagens})`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

### triagem_iniciar

Linha 1074: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1074>).

```python
def triagem_iniciar(request, modalidade):
```

**Explicacao presente no codigo:**

> Inicia ou retoma uma triagem somente após clique explícito.

**Decoradores:** `login_required`, `require_POST`.

**Chamadas utilizadas no corpo:** `Http404`, `PermissionDenied`, `iniciar_triagem`, `messages.error`, `messages.info`, `obter_ip`, `pode_responder`, `redirect`, `request.POST.get`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:triagem_apresentacao')`
- `redirect('accounts:triagem_pergunta', id_triagem=triagem.pk)`

**Excecoes levantadas:**

- `Http404('Modalidade de triagem inexistente.')`
- `PermissionDenied('A triagem está disponível somente para Doador e Receptor.')`

**Estrutura de controle:** If: 3, Try: 1. Abra o original para seguir as condicoes na ordem.

### _triagem_do_usuario_ou_404

Linha 1124: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1124>).

```python
def _triagem_do_usuario_ou_404(request, id_triagem):
```

**Explicacao presente no codigo:**

> Evita que uma conta consulte o questionário privado de outra.

**Chamadas utilizadas no corpo:** `PermissionDenied`, `get_object_or_404`, `pode_responder`.

**Expressoes de retorno (dependem do caminho):**

- `get_object_or_404(Triagem, pk=id_triagem, usuario=request.user)`

**Excecoes levantadas:**

- `PermissionDenied('Somente Doadores podem acessar a triagem.')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `triagem_pergunta` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1138>).
- `triagem_revisao` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1244>).
- `triagem_resultado` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1285>).

### triagem_pergunta

Linha 1138: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1138>).

```python
def triagem_pergunta(request, id_triagem):
```

**Explicacao presente no codigo:**

> Mostra, valida e salva uma única pergunta por página.

**Decoradores:** `login_required`.

**Chamadas utilizadas no corpo:** `FormularioPerguntaTriagem`, `Http404`, `_triagem_do_usuario_ou_404`, `editar_pergunta`, `form.is_valid`, `iniciar_triagem`, `len`, `messages.info`, `messages.success`, `obter_ip`, `obter_pergunta_atual`, `redirect`, `render`, `request.GET.get`, `request.POST.get`, `salvar_resposta`, `triagem.respostas.filter`, `triagem.respostas.filter(id_pergunta=pergunta['id']).first`, `voltar_pergunta`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:triagem_apresentacao')`
- `redirect('accounts:triagem_historico')`
- `redirect('accounts:triagem_pergunta', id_triagem=nova_extensa.pk)`
- `redirect('accounts:triagem_pergunta', id_triagem=triagem.pk)`
- `redirect('accounts:triagem_resultado', id_triagem=triagem.pk)`
- `redirect('accounts:triagem_revisao', id_triagem=triagem.pk)`
- `render(request, 'accounts/triagem_pergunta.html', {'triagem': triagem, 'pergunta': pergunta, 'form': form, 'numero_pergunta': triagem.pergunta_atual + 1, 'total_perguntas': len(triagem.fluxo_perguntas)})`

**Excecoes levantadas:**

- `Http404('Pergunta de triagem inexistente.')`

**Estrutura de controle:** If: 8, Try: 2. Abra o original para seguir as condicoes na ordem.

### triagem_revisao

Linha 1244: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1244>).

```python
def triagem_revisao(request, id_triagem):
```

**Explicacao presente no codigo:**

> Mostra todas as respostas antes do cálculo final.

**Decoradores:** `login_required`.

**Chamadas utilizadas no corpo:** `(resposta.valor or {}).get`, `_triagem_do_usuario_ou_404`, `concluir_triagem`, `messages.error`, `obter_pergunta`, `redirect`, `render`, `request.POST.get`, `respostas.append`, `str`, `triagem.respostas.order_by`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:triagem_apresentacao')`
- `redirect('accounts:triagem_resultado', id_triagem=triagem.pk)`
- `render(request, 'accounts/triagem_revisao.html', {'triagem': triagem, 'respostas_revisao': respostas})`

**Estrutura de controle:** If: 3, Try: 2, For: 1. Abra o original para seguir as condicoes na ordem.

### triagem_resultado

Linha 1285: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1285>).

```python
def triagem_resultado(request, id_triagem):
```

**Explicacao presente no codigo:**

> Mostra a orientação concluída somente ao dono da triagem.

**Decoradores:** `login_required`.

**Chamadas utilizadas no corpo:** `_triagem_do_usuario_ou_404`, `redirect`, `render`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:triagem_historico')`
- `redirect('accounts:triagem_revisao', id_triagem=triagem.pk)`
- `render(request, 'accounts/triagem_resultado.html', {'triagem': triagem})`

**Estrutura de controle:** If: 2. Abra o original para seguir as condicoes na ordem.

### visualizacao_publica_estoque

Linha 1311: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1311>).

```python
def visualizacao_publica_estoque(request):
```

**Explicacao presente no codigo:**

> Exibe publicamente os estoques dos Hemocentros aprovados.
> 
> A camada accounts.estoque devolve apenas os dados permitidos para
> exibicao publica, sem expor os limites internos usados pelo Hemocentro.

**Chamadas utilizadas no corpo:** `' '.join`, `' '.join([estoque['nome'], estoque['cidade'], estoque['estado'], estoque['tipo_sanguineo'], estoque['status_label']]).lower`, `(form.cleaned_data.get('busca') or '').strip`, `(form.cleaned_data.get('busca') or '').strip().lower`, `(form.cleaned_data.get('cidade') or '').strip`, `(form.cleaned_data.get('cidade') or '').strip().lower`, `(form.cleaned_data.get('hemocentro') or '').strip`, `(form.cleaned_data.get('hemocentro') or '').strip().lower`, `FiltroEstoquePublicoForm`, `estoque['cidade'].lower`, `estoque['nome'].lower`, `form.cleaned_data.get`, `form.is_valid`, `obter_estoques_publicos`, `parametros.get`, `render`, `request.GET.copy`.

**Expressoes de retorno (dependem do caminho):**

- `render(request, 'accounts/estoque_publico.html', {'estoques': estoques, 'form': form})`

**Estrutura de controle:** If: 9. Abra o original para seguir as condicoes na ordem.

### _formatar_erro_validacao

Linha 1386: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1386>).

```python
def _formatar_erro_validacao(erro):
```

**Explicacao presente no codigo:**

> Converte um ValidationError (string, lista ou dict) em texto legivel.

**Chamadas utilizadas no corpo:** `', '.join`, `'; '.join`, `erro.message_dict.items`, `hasattr`.

**Expressoes de retorno (dependem do caminho):**

- `'; '.join((f"{campo}: {', '.join(mensagens)}" for campo, mensagens in erro.message_dict.items()))`
- `'; '.join(erro.messages)`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `cadastrar_estoque_view` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1453>).
- `atualizar_estoque_view` em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1493>).

### estoque_hemocentro

Linha 1400: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1400>).

```python
def estoque_hemocentro(request):
```

**Explicacao presente no codigo:**

> UC_29 / UC_30 - Mostra o estoque do proprio Hemocentro logado e os
> formularios para cadastrar um novo tipo sanguineo ou movimentar um
> estoque ja existente.

**Decoradores:** `login_required`, `exigir_hemocentro_aprovado`.

**Chamadas utilizadas no corpo:** `CadastrarEstoqueForm`, `Estoque.objects.filter`, `Estoque.objects.filter(hemocentro=request.user).prefetch_related`, `Estoque.objects.filter(hemocentro=request.user).prefetch_related(Prefetch('movimentacoes', queryset=EstoqueMovimentacao.objects.select_related('usuario_resp').order_by('-data_hora'))).order_by`, `EstoqueMovimentacao.objects.select_related`, `EstoqueMovimentacao.objects.select_related('usuario_resp').order_by`, `MovimentarEstoqueForm`, `Prefetch`, `estoques.values_list`, `render`, `set`.

**Expressoes de retorno (dependem do caminho):**

- `render(request, 'accounts/estoque_hemocentro.html', {'estoques': estoques, 'tipos_disponiveis': tipos_disponiveis, 'form_cadastro': form_cadastro, 'form_movimentacao': MovimentarEstoqueForm()})`

### cadastrar_estoque_view

Linha 1453: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1453>).

```python
def cadastrar_estoque_view(request):
```

**Explicacao presente no codigo:**

> UC_29 - Cria a estrutura de estoque de um tipo sanguineo.

**Decoradores:** `login_required`, `require_POST`, `exigir_hemocentro_aprovado`.

**Chamadas utilizadas no corpo:** `CadastrarEstoqueForm`, `_formatar_erro_validacao`, `cadastrar_estoque`, `form.is_valid`, `messages.error`, `messages.success`, `redirect`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:estoque_hemocentro')`

**Estrutura de controle:** If: 1, Try: 1. Abra o original para seguir as condicoes na ordem.

### atualizar_estoque_view

Linha 1493: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1493>).

```python
def atualizar_estoque_view(request, id_estoque):
```

**Explicacao presente no codigo:**

> UC_30 - Registra uma entrada, saida ou ajuste em um estoque existente.

**Decoradores:** `login_required`, `require_POST`, `exigir_hemocentro_aprovado`.

**Chamadas utilizadas no corpo:** `MovimentarEstoqueForm`, `_formatar_erro_validacao`, `form.is_valid`, `get_object_or_404`, `messages.error`, `messages.success`, `redirect`, `registrar_movimentacao_estoque`, `str`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:estoque_hemocentro')`

**Estrutura de controle:** If: 1, Try: 1. Abra o original para seguir as condicoes na ordem.

### criar_pedido_sangue

Linha 1542: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1542>).

```python
def criar_pedido_sangue(request):
```

**Explicacao presente no codigo:**

> Recebe uma solicitação de divulgação, sem publicá-la.
> 
> Apenas Receptor/Solicitante pode enviar solicitacao de pedido.
> 
> Ao salvar, a solicitacao aguarda analise do Hemocentro.

**Decoradores:** `login_required`.

**Chamadas utilizadas no corpo:** `PedidoSangueForm`, `criar_pedido_pendente`, `form.add_error`, `form.is_valid`, `messages.error`, `messages.success`, `redirect`, `registrar_auditoria`, `render`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:consultar_pedidos')`
- `redirect('accounts:dashboard')`
- `redirect('accounts:minhas_solicitacoes')`
- `render(request, 'accounts/pedido_publicar.html', {'form': form})`

**Estrutura de controle:** If: 5, Try: 1. Abra o original para seguir as condicoes na ordem.

### minhas_solicitacoes

Linha 1606: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1606>).

```python
def minhas_solicitacoes(request):
```

**Explicacao presente no codigo:**

> Lista somente as solicitações enviadas pelo usuário autenticado.

**Decoradores:** `login_required`.

**Chamadas utilizadas no corpo:** `PedidoSangue.objects.select_related`, `PedidoSangue.objects.select_related('hemocentro_destino').prefetch_related`, `PedidoSangue.objects.select_related('hemocentro_destino').prefetch_related(Prefetch('validacoes', queryset=ValidacaoPedido.objects.select_related('moderador'))).filter`, `PedidoSangue.objects.select_related('hemocentro_destino').prefetch_related(Prefetch('validacoes', queryset=ValidacaoPedido.objects.select_related('moderador'))).filter(solicitante=request.user).order_by`, `Prefetch`, `ValidacaoPedido.objects.select_related`, `dict`, `render`, `request.GET.get`, `solicitacoes.filter`.

**Expressoes de retorno (dependem do caminho):**

- `render(request, 'accounts/minhas_solicitacoes.html', {'solicitacoes': solicitacoes, 'status_opcoes': PedidoSangue.Status.choices, 'status_atual': status or ''})`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

### painel_pedidos_hemocentro

Linha 1639: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1639>).

```python
def painel_pedidos_hemocentro(request):
```

**Explicacao presente no codigo:**

> Fila de solicitações destinadas ao Hemocentro aprovado logado.

**Decoradores:** `login_required`, `exigir_hemocentro_aprovado`.

**Chamadas utilizadas no corpo:** `PedidoSangue.objects.filter`, `PedidoSangue.objects.filter(hemocentro_destino=request.user, status=PedidoSangue.Status.ENVIADA).update`, `PedidoSangue.objects.select_related`, `PedidoSangue.objects.select_related('solicitante', 'hemocentro_destino').filter`, `PedidoSangue.objects.select_related('solicitante', 'hemocentro_destino').filter(hemocentro_destino=request.user).exclude`, `PedidoSangue.objects.select_related('solicitante', 'hemocentro_destino').filter(hemocentro_destino=request.user).exclude(status=PedidoSangue.Status.ENCERRADA).order_by`, `dict`, `render`, `request.GET.get`, `solicitacoes.filter`.

**Expressoes de retorno (dependem do caminho):**

- `render(request, 'accounts/painel_validacao_pedidos.html', {'solicitacoes': solicitacoes, 'status_opcoes': PedidoSangue.Status.choices})`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

### consultar_pedidos

Linha 1668: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1668>).

```python
def consultar_pedidos(request):
```

**Explicacao presente no codigo:**

> UC_18 - Consultar Pedidos.
> 
> Exibe apenas pedidos ativos e aplica filtros por tipo sanguineo,
> urgencia, cidade, hemocentro e data. A ordenacao prioriza urgencia
> e depois os mais recentes.

**Chamadas utilizadas no corpo:** `Case`, `FiltroPedidoSangueForm`, `IntegerField`, `PedidoSangue.objects.select_related`, `PedidoSangue.objects.select_related('hemocentro_destino').filter`, `Value`, `When`, `form.cleaned_data.get`, `form.is_valid`, `pedidos.annotate`, `pedidos.annotate(prioridade=prioridade).order_by`, `pedidos.filter`, `pedidos.none`, `render`.

**Expressoes de retorno (dependem do caminho):**

- `render(request, 'accounts/pedidos_listar.html', {'form': form, 'pedidos': pedidos})`

**Estrutura de controle:** If: 7. Abra o original para seguir as condicoes na ordem.

### painel_validacao_pedidos

Linha 1760: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1760>).

```python
def painel_validacao_pedidos(request):
```

**Explicacao presente no codigo:**

> Painel de moderação do Administrador, sem publicar pedidos.

**Decoradores:** `login_required`.

**Chamadas utilizadas no corpo:** `PedidoSangue.objects.select_related`, `PedidoSangue.objects.select_related('solicitante', 'hemocentro_destino').prefetch_related`, `PedidoSangue.objects.select_related('solicitante', 'hemocentro_destino').prefetch_related(Prefetch('validacoes', queryset=ValidacaoPedido.objects.select_related('moderador'))).filter`, `PedidoSangue.objects.select_related('solicitante', 'hemocentro_destino').prefetch_related(Prefetch('validacoes', queryset=ValidacaoPedido.objects.select_related('moderador'))).filter(status__in=[PedidoSangue.Status.ENVIADA, PedidoSangue.Status.EM_ANALISE, PedidoSangue.Status.CORRECAO_SOLICITADA, PedidoSangue.Status.PUBLICADA]).order_by`, `Prefetch`, `ValidacaoPedido.objects.select_related`, `dict`, `exigir_administrador`, `pedidos.filter`, `render`, `request.GET.get`.

**Expressoes de retorno (dependem do caminho):**

- `render(request, 'accounts/painel_moderacao_pedidos.html', {'pedidos': pedidos, 'status_opcoes': PedidoSangue.Status.choices, 'status_atual': status or ''})`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

### aprovar_pedido

Linha 1802: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1802>).

```python
def aprovar_pedido(request, id_pedido):
```

**Explicacao presente no codigo:**

> Publica uma solicitação após análise do Hemocentro de destino.

**Decoradores:** `login_required`, `require_POST`.

**Chamadas utilizadas no corpo:** `aprovar_pedido_servico`, `get_object_or_404`, `hemocentro_aprovado`, `messages.success`, `redirect`, `request.POST.get`, `validar_publicacao_hemocentro`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:painel_pedidos_hemocentro')`

**Onde aparece uma chamada com este nome:**

- `FluxoCadastroTriagemPedidosTests.test_solicitacao_nao_publica_e_hemocentro_publica` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:230>).
- `FluxoCadastroTriagemPedidosTests.test_publicacao_notifica_somente_doador_apto_compativel` em [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py:323>).
- `PedidoSangueTests.test_hemocentro_aprova_pedido_e_registra_historico` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:159>).
- `PedidoSangueTests.test_publicacao_exclusiva_do_hemocentro_responsavel` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:228>).
- `PedidoSangueTests.test_auditoria_distingue_validacao_e_publicacao` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:256>).

### recusar_pedido

Linha 1830: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1830>).

```python
def recusar_pedido(request, id_pedido):
```

**Explicacao presente no codigo:**

> Recusa uma solicitação pelo Hemocentro de destino.

**Decoradores:** `login_required`, `require_POST`.

**Chamadas utilizadas no corpo:** `get_object_or_404`, `messages.success`, `recusar_pedido_servico`, `redirect`, `request.POST.get`, `validar_publicacao_hemocentro`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:painel_pedidos_hemocentro')`

### solicitar_correcao_pedido

Linha 1858: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1858>).

```python
def solicitar_correcao_pedido(request, id_pedido):
```

**Decoradores:** `login_required`, `require_POST`, `exigir_hemocentro_aprovado`.

**Chamadas utilizadas no corpo:** `get_object_or_404`, `messages.success`, `redirect`, `request.POST.get`, `solicitar_correcao_pedido_servico`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:painel_pedidos_hemocentro')`

### marcar_pedido_suspeito

Linha 1872: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1872>).

```python
def marcar_pedido_suspeito(request, id_pedido):
```

**Explicacao presente no codigo:**

> Registra uma suspeita para moderação, sem publicar o pedido.

**Decoradores:** `login_required`, `require_POST`.

**Chamadas utilizadas no corpo:** `get_object_or_404`, `marcar_pedido_suspeito_servico`, `messages.success`, `redirect`, `request.POST.get`, `usuario_e_administrador`.

**Expressoes de retorno (dependem do caminho):**

- `redirect('accounts:painel_pedidos_hemocentro')`
- `redirect('accounts:painel_validacao_pedidos')`

**Estrutura de controle:** If: 1. Abra o original para seguir as condicoes na ordem.

**Onde aparece uma chamada com este nome:**

- `PedidoSangueTests.test_auditoria_distingue_validacao_e_publicacao` em [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py:256>).

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `POSTOS_COLETA`: linha 339; valor declarado em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:339>).
- `ESTOQUE_GERAL`: linha 364; valor declarado em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:364>).
- `CAMPANHAS_ATIVAS`: linha 376; valor declarado em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:376>).
- `PAINEIS_POR_PERFIL`: linha 390; valor declarado em [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:390>).

## config/__init__.py

Marcador de pacote Python; pode nao executar nenhuma instrucao.

Original: [config/__init__.py](<C:/Users/lb119/Elo/config/__init__.py>).


## config/asgi.py

Entrada de servidor pelo protocolo ASGI.

Original: [config/asgi.py](<C:/Users/lb119/Elo/config/asgi.py>).

**Dependencias importadas:**

```python
import os
from django.core.asgi import get_asgi_application
```


## config/settings.py

Configuracao de apps, banco, middleware, templates e autenticacao.

Original: [config/settings.py](<C:/Users/lb119/Elo/config/settings.py>).

**Dependencias importadas:**

```python
import os
from pathlib import Path
from dotenv import load_dotenv
```

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `BASE_DIR`: linha 22; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:22>).
- `SECRET_KEY`: linha 32; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:32>).
- `DEBUG`: linha 36; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:36>).
- `ALLOWED_HOSTS`: linha 39; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:39>).
- `INSTALLED_APPS`: linha 43; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:43>).
- `MIDDLEWARE`: linha 62; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:62>).
- `ROOT_URLCONF`: linha 82; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:82>).
- `TEMPLATES`: linha 85; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:85>).
- `WSGI_APPLICATION`: linha 110; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:110>).
- `DATABASES`: linha 120; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:120>).
- `AUTH_PASSWORD_VALIDATORS`: linha 144; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:144>).
- `LANGUAGE_CODE`: linha 177; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:177>).
- `TIME_ZONE`: linha 178; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:178>).
- `USE_I18N`: linha 179; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:179>).
- `USE_TZ`: linha 180; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:180>).
- `CONVOCACAO_INTERVALO_HORAS`: linha 183; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:183>).
- `CONVOCACAO_LIMITE_NOTIFICACOES`: linha 184; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:184>).
- `CONVOCACAO_VERSAO_CONSENTIMENTO`: linha 185; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:185>).
- `STATIC_URL`: linha 189; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:189>).
- `STATICFILES_DIRS`: linha 191; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:191>).
- `EMAIL_BACKEND`: linha 197; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:197>).
- `DEFAULT_AUTO_FIELD`: linha 200; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:200>).
- `AUTH_USER_MODEL`: linha 205; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:205>).
- `LOGIN_URL`: linha 208; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:208>).
- `LOGIN_REDIRECT_URL`: linha 209; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:209>).
- `LOGOUT_REDIRECT_URL`: linha 210; valor declarado em [config/settings.py](<C:/Users/lb119/Elo/config/settings.py:210>).

## config/settings_test.py

Configuracao de banco temporario para os testes.

Original: [config/settings_test.py](<C:/Users/lb119/Elo/config/settings_test.py>).

**Dependencias importadas:**

```python
from .settings import *
```

### Constantes e dados declarados

Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.

- `DATABASES`: linha 11; valor declarado em [config/settings_test.py](<C:/Users/lb119/Elo/config/settings_test.py:11>).

## config/urls.py

Associacao entre endereco, view e nome de rota.

Original: [config/urls.py](<C:/Users/lb119/Elo/config/urls.py>).

**Dependencias importadas:**

```python
from django.contrib import admin
from django.urls import include, path
```

### Rotas declaradas

```python
path('admin/', admin.site.urls)
path('', include('accounts.urls'))
```


## config/wsgi.py

Entrada de servidor pelo protocolo WSGI.

Original: [config/wsgi.py](<C:/Users/lb119/Elo/config/wsgi.py>).

**Dependencias importadas:**

```python
import os
from django.core.wsgi import get_wsgi_application
```


## docs/superpowers/plans/2026-09-04-triagem-completa.md

Documento/configuracao complementar; consulte o conteudo integral.

Original: [docs/superpowers/plans/2026-09-04-triagem-completa.md](<C:/Users/lb119/Elo/docs/superpowers/plans/2026-09-04-triagem-completa.md>).


## docs/superpowers/specs/2026-09-04-triagem-completa-design.md

Documento/configuracao complementar; consulte o conteudo integral.

Original: [docs/superpowers/specs/2026-09-04-triagem-completa-design.md](<C:/Users/lb119/Elo/docs/superpowers/specs/2026-09-04-triagem-completa-design.md>).


## elo_front/README-INSTALACAO.txt

Documento/configuracao complementar; consulte o conteudo integral.

Original: [elo_front/README-INSTALACAO.txt](<C:/Users/lb119/Elo/elo_front/README-INSTALACAO.txt>).


## elo_front/static/css/elo.css

Regras visuais de seletores, componentes e tamanhos de tela.

Original: [elo_front/static/css/elo.css](<C:/Users/lb119/Elo/elo_front/static/css/elo.css>).

**Seletores/blocos visuais declarados:**

- `@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600;1,700&display=swap');

:root`
- `*`
- `html`
- `body`
- `a`
- `button,
input,
select,
textarea`
- `.container`
- `.site-header`
- `.header-inner`
- `.brand`
- `.brand-mark`
- `.site-header .brand-mark`
- `.brand-name`
- `.main-nav`
- `.main-nav > a`
- `.main-nav > a:hover`
- `.main-nav .nav-cta`
- `.main-nav .nav-cta:hover`
- `.menu-toggle`
- `.menu-toggle span`
- `.hero`
- `.hero-inner`
- `.hero-copy`
- `.eyebrow`
- `.hero h1`
- `.hero h1 em`
- `.hero-text`
- `.hero-actions`
- `.button`
- `.button-primary`
- `.button-primary:hover`
- `.button-outline`
- `.button-outline:hover`
- `.button-small`
- `.stock-section`
- `.section-heading h2,
.info-section h2,
.faq-section h2`
- `.section-heading p`
- `.section-heading`
- `.blood-grid`
- `.blood-card`
- `.blood-type`
- `.blood-line`
- `.blood-status`
- `.status-critical,
.status-alert`
- `.status-stable`
- `.center-action`
- `.info-section`
- `.info-grid`
- `.info-section h2`
- `.info-text`
- `.text-link`
- `.text-link:hover`
- `.faq-section`
- `.faq-section > .container > h2`
- `.faq-grid`
- `.faq-grid details`
- `.faq-grid summary`
- `.faq-grid p`
- `.messages-wrap`
- `.message`
- `.site-footer`
- `.footer-inner`
- `.brand-footer .brand-name`
- `.brand-footer .brand-mark`
- `.footer-inner p`
- `.footer-links`
- `.footer-links a`
- `.footer-links a:hover`
- `main form:not(.plain-form)`
- `main input,
main select,
main textarea`
- `main input:focus,
main select:focus,
main textarea:focus`
- `main button[type="submit"]`
- `main button[type="submit"]:hover`
- `.empty-state`
- `@media (max-width: 900px)`
- `.container,
    .header-inner,
    .footer-inner,
    .messages-wrap`
- `.site-header`
- `.menu-toggle`
- `.main-nav`
- `.main-nav.is-open`
- `.main-nav > a`
- `.main-nav .nav-cta`
- `.hero`
- `.hero-copy`
- `.hero-inner`
- `.hero-actions`
- `.hero h1`
- `.blood-grid`
- `.info-grid,
    .faq-grid`
- `.footer-inner`
- `@media (max-width: 520px)`
- `.container,
    .header-inner,
    .footer-inner,
    .messages-wrap`
- `.brand-name`
- `.brand-mark`
- `.site-header .brand-mark`
- `.hero h1`
- `.hero-text`
- `.hero-actions`
- `.button`
- `.blood-grid`
- `.blood-type`
- `.info-section h2`
- `.footer-links`

Leia propriedades dentro de cada bloco: layout, cores, espacos, tipografia e regras responsivas. A copia integral preserva todos os valores.


## elo_front/templates/accounts/inicio.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [elo_front/templates/accounts/inicio.html](<C:/Users/lb119/Elo/elo_front/templates/accounts/inicio.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `elif item.nivel == 'Alerta' or item.nivel == 'Baixo'`
- `else`
- `empty`
- `endblock`
- `endfor`
- `endif`
- `extends "base.html"`
- `for item in estoque_geral`
- `if item.nivel == 'Critico'`
- `url 'accounts:cadastro'`
- `url 'accounts:estoque_publico'`
- `url 'accounts:triagem_apresentacao'`

**Valores exibidos:**

- `item.nivel`
- `item.tipo`


## elo_front/templates/base.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [elo_front/templates/base.html](<C:/Users/lb119/Elo/elo_front/templates/base.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `else`
- `endblock`
- `endfor`
- `endif`
- `for message in messages`
- `if messages`
- `if user.is_authenticated`
- `load static`
- `static 'css/elo.css'`
- `url 'accounts:cadastro'`
- `url 'accounts:dashboard'`
- `url 'accounts:estoque_publico'`
- `url 'accounts:inicio'`
- `url 'accounts:login'`
- `url 'accounts:triagem_apresentacao'`

**Valores exibidos:**

- `message`
- `message.tags|default:'info'`

**JavaScript embutido:** leia os eventos e seletores na copia integral; ele organiza interacao no navegador, sem substituir autorizacao no servidor.


## manage.py

Entrada dos comandos do Django.

Original: [manage.py](<C:/Users/lb119/Elo/manage.py>).

**Dependencias importadas:**

```python
import os
import sys
```

### main

Linha 15: [manage.py](<C:/Users/lb119/Elo/manage.py:15>).

```python
def main():
```

**Explicacao presente no codigo:**

> Configura o projeto e entrega o comando ao Django.

**Chamadas utilizadas no corpo:** `ImportError`, `execute_from_command_line`, `os.environ.setdefault`.

**Excecoes levantadas:**

- `ImportError('Nao foi possivel importar o Django. Confirme a instalacao e a ativacao do ambiente virtual .venv.')`

**Estrutura de controle:** Try: 1. Abra o original para seguir as condicoes na ordem.


## requirements.txt

Documento/configuracao complementar; consulte o conteudo integral.

Original: [requirements.txt](<C:/Users/lb119/Elo/requirements.txt>).


## templates/accounts/cadastro.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/cadastro.html](<C:/Users/lb119/Elo/templates/accounts/cadastro.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `csrf_token`
- `endblock`
- `endfor`
- `endif`
- `extends "base.html"`
- `for campo in form`
- `if campo.help_text`
- `if campo.name != "aceite_lgpd"`
- `if form.aceite_lgpd.value`
- `url 'accounts:login'`

**Valores exibidos:**

- `campo`
- `campo.errors`
- `campo.help_text`
- `campo.id_for_label`
- `campo.label`
- `form.aceite_lgpd.errors`
- `form.aceite_lgpd.html_name`
- `form.aceite_lgpd.id_for_label`
- `form.non_field_errors`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:676>)


## templates/accounts/compatibilidade_sanguinea.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/compatibilidade_sanguinea.html](<C:/Users/lb119/Elo/templates/accounts/compatibilidade_sanguinea.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `endblock`
- `endfor`
- `endif`
- `extends "base.html"`
- `for item in tabela_compatibilidade`
- `for tipo in tipos_sanguineos`
- `if compatibilidade_selecionada`
- `if tipo == tipo_selecionado`
- `if tipo_invalido`

**Valores exibidos:**

- `compatibilidade_selecionada.doar_para|join:", "`
- `compatibilidade_selecionada.receber_de|join:", "`
- `compatibilidade_selecionada.tipo`
- `item.doar_para|join:", "`
- `item.populacao`
- `item.receber_de|join:", "`
- `item.tipo`
- `tipo`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:708>)


## templates/accounts/dashboard.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/dashboard.html](<C:/Users/lb119/Elo/templates/accounts/dashboard.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `comment`
- `csrf_token`
- `elif notificacao.tipo == "PEDIDO_COMPATIVEL"`
- `elif request.user.status_validacao == "APROVADO"`
- `elif request.user.status_validacao == "CORRECAO"`
- `elif request.user.status_validacao == "RECUSADO"`
- `elif user.perfil == "RECEPTOR"`
- `else`
- `empty`
- `endblock`
- `endcomment`
- `endfor`
- `endif`
- `extends "base.html"`
- `for acao in painel.acoes`
- `for campanha in campanhas_ativas`
- `for item in estoque_geral`
- `for notificacao in notificacoes_dashboard`
- `for pedido in pedidos_ativos`
- `for posto in postos`
- `if not notificacao.lida`
- `if notificacao.lida`
- `if notificacao.tipo == "ESTOQUE_CRITICO" or notificacao.tipo == "ESTOQUE_BAIXO"`
- `if notificacao.url_destino`
- `if notificacoes_dashboard.has_next`
- `if notificacoes_dashboard.has_other_pages`
- `if notificacoes_dashboard.has_previous`
- `if preferencia_convocacao`
- `if request.user.status_validacao == "PENDENTE"`
- `if ultima_triagem`
- `if user.perfil == "DOADOR"`
- `if validacao_atual and validacao_atual.parecer`
- `if visibilidade.mostra_campanhas`
- `if visibilidade.mostra_estoque_publico`
- `if visibilidade.mostra_pedidos`
- `if visibilidade.mostra_postos`
- `if visibilidade.mostra_status_hemocentro`
- `if visibilidade.mostra_triagem`
- `if visibilidade.pode_analisar_pedidos`
- `if visibilidade.pode_aprovar_hemocentros`
- `if visibilidade.pode_gerenciar_estoque`
- `if visibilidade.pode_moderar_pedidos`
- `if visibilidade.pode_solicitar_divulgacao`
- `url 'accounts:consultar_pedidos'`
- `url 'accounts:estoque_hemocentro'`
- `url 'accounts:estoque_publico'`
- `url 'accounts:minhas_solicitacoes'`
- `url 'accounts:painel_aprovacao_hemocentros'`
- `url 'accounts:painel_pedidos_hemocentro'`
- `url 'accounts:painel_validacao_pedidos'`
- `url 'accounts:pedido_publicar'`
- `url 'accounts:triagem_apresentacao'`
- `url 'accounts:triagem_historico'`

**Valores exibidos:**

- `acao`
- `campanha.cidade`
- `campanha.data`
- `campanha.titulo`
- `convocacao_intervalo_horas`
- `convocacao_limite`
- `item.nivel`
- `item.percentual`
- `item.tipo`
- `notificacao.criada_em|date:"d/m/Y H:i"`
- `notificacao.get_tipo_display`
- `notificacao.mensagem`
- `notificacao.pk`
- `notificacao.titulo`
- `notificacao.url_destino`
- `notificacoes_dashboard.next_page_number`
- `notificacoes_dashboard.number`
- `notificacoes_dashboard.paginator.num_pages`
- `notificacoes_dashboard.previous_page_number`
- `notificacoes_nao_lidas`
- `painel.descricao`
- `painel.rotulo`
- `painel.titulo`
- `pedido.cidade`
- `pedido.tipo_sanguineo`
- `pedido.titulo`
- `pedido.urgencia`
- `posto.cidade`
- `posto.estado`
- `posto.horario`
- `posto.nome`
- `preferencia_convocacao.as_p`
- `ultima_triagem.get_modalidade_display`
- `ultima_triagem.get_status_display`
- `user.get_short_name`
- `validacao_atual.data_analise|date:"d/m/Y H:i"`
- `validacao_atual.parecer`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:820>)


## templates/accounts/estoque_hemocentro.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/estoque_hemocentro.html](<C:/Users/lb119/Elo/templates/accounts/estoque_hemocentro.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `csrf_token`
- `else`
- `endblock`
- `endfor`
- `endif`
- `endwith`
- `extends "base.html"`
- `for estoque in estoques`
- `for movimentacao in movimentacoes`
- `if estoques`
- `if form_cadastro.nivel_critico.help_text`
- `if form_cadastro.nivel_minimo.help_text`
- `if form_cadastro.quantidade_bolsas.help_text`
- `if form_movimentacao.motivo.help_text`
- `if form_movimentacao.quantidade.help_text`
- `if movimentacao.usuario_resp`
- `if movimentacoes`
- `if tipos_disponiveis`
- `url 'accounts:atualizar_estoque' estoque.id_estoque`
- `url 'accounts:cadastrar_estoque'`
- `with movimentacoes=estoque.movimentacoes.all`

**Valores exibidos:**

- `estoque.data_atualizacao|date:"d/m/Y H:i"`
- `estoque.get_status_calculado_display`
- `estoque.nivel_critico`
- `estoque.nivel_minimo`
- `estoque.quantidade_bolsas`
- `estoque.tipo_sanguineo`
- `form_cadastro.nivel_critico`
- `form_cadastro.nivel_critico.help_text`
- `form_cadastro.nivel_critico.label_tag`
- `form_cadastro.nivel_minimo`
- `form_cadastro.nivel_minimo.help_text`
- `form_cadastro.nivel_minimo.label_tag`
- `form_cadastro.quantidade_bolsas`
- `form_cadastro.quantidade_bolsas.help_text`
- `form_cadastro.quantidade_bolsas.label_tag`
- `form_cadastro.tipo_sanguineo`
- `form_cadastro.tipo_sanguineo.label_tag`
- `form_movimentacao.motivo`
- `form_movimentacao.motivo.help_text`
- `form_movimentacao.motivo.label_tag`
- `form_movimentacao.quantidade`
- `form_movimentacao.quantidade.help_text`
- `form_movimentacao.quantidade.label_tag`
- `form_movimentacao.tipo_movimento`
- `form_movimentacao.tipo_movimento.label_tag`
- `movimentacao.data_hora|date:"d/m/Y H:i"`
- `movimentacao.get_tipo_movimento_display`
- `movimentacao.motivo`
- `movimentacao.quantidade_anterior`
- `movimentacao.quantidade_nova`
- `movimentacao.usuario_resp.nome`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1440>)


## templates/accounts/estoque_publico.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/estoque_publico.html](<C:/Users/lb119/Elo/templates/accounts/estoque_publico.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `comment`
- `else`
- `endblock`
- `endcomment`
- `endfor`
- `endif`
- `extends "base.html"`
- `for hemocentro in hemocentros`
- `for item in hemocentro.list`
- `if estoques`
- `regroup estoques by nome as hemocentros`
- `url 'accounts:estoque_publico'`

**Valores exibidos:**

- `form.as_p`
- `hemocentro.grouper`
- `hemocentro.list.0.cidade`
- `hemocentro.list.0.estado`
- `item.data_atualizacao|date:"d/m/Y H:i"`
- `item.quantidade_bolsas`
- `item.status_label`
- `item.tipo_sanguineo`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1378>)


## templates/accounts/inicio.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/inicio.html](<C:/Users/lb119/Elo/templates/accounts/inicio.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `comment`
- `else`
- `endblock`
- `endcomment`
- `endfor`
- `endif`
- `extends "base.html"`
- `for item in estoque_geral`
- `for pedido in pedidos_ativos`
- `for posto in postos`
- `if postos`
- `url 'accounts:cadastro'`
- `url 'accounts:login'`
- `url 'accounts:triagem_apresentacao'`
- `url 'admin:index'`

**Valores exibidos:**

- `consulta`
- `item.nivel`
- `item.percentual`
- `item.tipo`
- `pedido.cidade`
- `pedido.tipo_sanguineo`
- `pedido.titulo`
- `pedido.urgencia`
- `posto.cidade`
- `posto.endereco`
- `posto.estado`
- `posto.horario`
- `posto.nome`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:583>)


## templates/accounts/login.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/login.html](<C:/Users/lb119/Elo/templates/accounts/login.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `comment`
- `csrf_token`
- `endblock`
- `endcomment`
- `endif`
- `extends "base.html"`
- `if next`
- `url 'accounts:cadastro'`
- `url 'accounts:inicio'`

**Valores exibidos:**

- `form.as_p`
- `next`

**Referencias ao caminho do template no Python:**

- [accounts/urls.py](<C:/Users/lb119/Elo/accounts/urls.py:45>)


## templates/accounts/minhas_solicitacoes.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/minhas_solicitacoes.html](<C:/Users/lb119/Elo/templates/accounts/minhas_solicitacoes.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `empty`
- `endblock`
- `endfor`
- `endif`
- `endwith`
- `extends "base.html"`
- `for codigo, nome in status_opcoes`
- `for solicitacao in solicitacoes`
- `if status_atual == codigo`
- `if ultima_validacao`
- `if ultima_validacao.motivo`
- `url 'accounts:dashboard'`
- `url 'accounts:pedido_publicar'`
- `with ultima_validacao=solicitacao.validacoes.all.0`

**Valores exibidos:**

- `codigo`
- `nome`
- `solicitacao.cidade`
- `solicitacao.data_criacao|date:"d/m/Y H:i"`
- `solicitacao.get_status_display`
- `solicitacao.hemocentro_destino.nome`
- `solicitacao.id_pedido`
- `solicitacao.tipo_sanguineo`
- `solicitacao.titulo`
- `ultima_validacao.get_status_validacao_display`
- `ultima_validacao.motivo`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1628>)


## templates/accounts/painel_aprovacao_hemocentros.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/painel_aprovacao_hemocentros.html](<C:/Users/lb119/Elo/templates/accounts/painel_aprovacao_hemocentros.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `csrf_token`
- `else`
- `endblock`
- `endfor`
- `endif`
- `extends "base.html"`
- `for hemocentro in hemocentros`
- `if hemocentros`
- `url 'accounts:aprovar_hemocentro' hemocentro.pk`
- `url 'accounts:dashboard'`
- `url 'accounts:estoque_publico'`
- `url 'accounts:inicio'`
- `url 'accounts:painel_validacao_pedidos'`
- `url 'accounts:recusar_hemocentro' hemocentro.pk`
- `url 'accounts:solicitar_correcao_hemocentro' hemocentro.pk`

**Valores exibidos:**

- `hemocentro.cidade|default:"Não informado"`
- `hemocentro.cnpj|default:"Não informado"`
- `hemocentro.date_joined|date:"d/m/Y H:i"`
- `hemocentro.email`
- `hemocentro.estado|default:"Não informado"`
- `hemocentro.get_status_validacao_display`
- `hemocentro.nome`
- `hemocentro.pk`
- `hemocentro.telefone|default:"Não informado"`
- `hemocentros|length`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:848>)


## templates/accounts/painel_moderacao_pedidos.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/painel_moderacao_pedidos.html](<C:/Users/lb119/Elo/templates/accounts/painel_moderacao_pedidos.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `csrf_token`
- `empty`
- `endblock`
- `endfor`
- `endif`
- `endwith`
- `extends "base.html"`
- `for codigo, nome in status_opcoes`
- `for pedido in pedidos`
- `if pedido.duplicidade_suspeita`
- `if pedido.status != "ENCERRADA"`
- `if status_atual == codigo`
- `if ultima_validacao`
- `url 'accounts:dashboard'`
- `url 'accounts:marcar_pedido_suspeito' pedido.id_pedido`
- `url 'accounts:painel_aprovacao_hemocentros'`
- `with ultima_validacao=pedido.validacoes.all.0`

**Valores exibidos:**

- `codigo`
- `nome`
- `pedido.cidade`
- `pedido.contato`
- `pedido.descricao`
- `pedido.get_status_display`
- `pedido.get_urgencia_display`
- `pedido.hemocentro_destino.nome`
- `pedido.id_pedido`
- `pedido.nome_solicitante`
- `pedido.tipo_sanguineo`
- `pedido.titulo`
- `ultima_validacao.get_status_validacao_display`
- `ultima_validacao.motivo`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1791>)


## templates/accounts/painel_validacao_pedidos.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/painel_validacao_pedidos.html](<C:/Users/lb119/Elo/templates/accounts/painel_validacao_pedidos.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `csrf_token`
- `empty`
- `endblock`
- `endfor`
- `endif`
- `extends "base.html"`
- `for codigo, nome in status_opcoes`
- `for pedido in solicitacoes`
- `if pedido.duplicidade_suspeita`
- `if pedido.informacoes_complementares`
- `if pedido.status != "PUBLICADA" and pedido.status != "RECUSADA"`
- `url 'accounts:aprovar_pedido' pedido.id_pedido`
- `url 'accounts:dashboard'`
- `url 'accounts:estoque_hemocentro'`
- `url 'accounts:marcar_pedido_suspeito' pedido.id_pedido`
- `url 'accounts:recusar_pedido' pedido.id_pedido`
- `url 'accounts:solicitar_correcao_pedido' pedido.id_pedido`

**Valores exibidos:**

- `codigo`
- `nome`
- `pedido.cidade`
- `pedido.contato`
- `pedido.descricao`
- `pedido.get_status_display`
- `pedido.get_urgencia_display`
- `pedido.hemocentro_destino.nome`
- `pedido.informacoes_complementares`
- `pedido.nome_solicitante`
- `pedido.tipo_sanguineo`
- `pedido.titulo`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1660>)


## templates/accounts/pedido_detalhe.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/pedido_detalhe.html](<C:/Users/lb119/Elo/templates/accounts/pedido_detalhe.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `endblock`
- `endif`
- `extends "base.html"`
- `if pedido.hemocentro.estado`
- `if pedido.nome_paciente`
- `url 'accounts:dashboard'`

**Valores exibidos:**

- `pedido.cidade`
- `pedido.data_criacao|date:"d/m/Y H:i"`
- `pedido.descricao`
- `pedido.get_para_quem_display`
- `pedido.get_status_display`
- `pedido.get_urgencia_display`
- `pedido.hemocentro.estado`
- `pedido.hemocentro.nome`
- `pedido.nome_paciente`
- `pedido.tipo_sanguineo`


## templates/accounts/pedido_filtrar.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/pedido_filtrar.html](<C:/Users/lb119/Elo/templates/accounts/pedido_filtrar.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `else`
- `endblock`
- `endfor`
- `endif`
- `extends "base.html"`
- `for pedido in pedidos`
- `if pedidos`
- `url 'accounts:consultar_pedidos'`
- `url 'accounts:dashboard'`

**Valores exibidos:**

- `form.cidade`
- `form.cidade.errors`
- `form.cidade.label_tag`
- `form.data`
- `form.data.errors`
- `form.data.label_tag`
- `form.hemocentro`
- `form.hemocentro.errors`
- `form.hemocentro.label_tag`
- `form.non_field_errors`
- `form.status`
- `form.status.errors`
- `form.status.label_tag`
- `form.tipo_sanguineo`
- `form.tipo_sanguineo.errors`
- `form.tipo_sanguineo.label_tag`
- `form.urgencia`
- `form.urgencia.errors`
- `form.urgencia.label_tag`
- `pedido.cidade`
- `pedido.descricao`
- `pedido.get_status_display`
- `pedido.get_urgencia_display`
- `pedido.hemocentro_destino.nome`
- `pedido.publicado_em|default:pedido.data_criacao|date:"d/m/Y H:i"`
- `pedido.tipo_sanguineo`
- `pedido.titulo`


## templates/accounts/pedido_publicar.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/pedido_publicar.html](<C:/Users/lb119/Elo/templates/accounts/pedido_publicar.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `csrf_token`
- `endblock`
- `extends "base.html"`
- `url 'accounts:dashboard'`

**Valores exibidos:**

- `form.as_p`
- `form.non_field_errors`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1598>)


## templates/accounts/pedidos_listar.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/pedidos_listar.html](<C:/Users/lb119/Elo/templates/accounts/pedidos_listar.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `comment`
- `empty`
- `endblock`
- `endcomment`
- `endfor`
- `endif`
- `extends "base.html"`
- `for pedido in pedidos`
- `if user.is_authenticated`
- `if user.perfil == "RECEPTOR"`
- `url 'accounts:consultar_pedidos'`
- `url 'accounts:criar_pedido_sangue'`
- `url 'accounts:dashboard'`

**Valores exibidos:**

- `form.as_p`
- `pedido.cidade`
- `pedido.descricao`
- `pedido.get_status_display`
- `pedido.get_urgencia_display`
- `pedido.hemocentro_destino.nome`
- `pedido.publicado_em|default:pedido.data_criacao|date:"d/m/Y H:i"`
- `pedido.tipo_sanguineo`
- `pedido.titulo`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1751>)


## templates/accounts/triagem_apresentacao.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/triagem_apresentacao.html](<C:/Users/lb119/Elo/templates/accounts/triagem_apresentacao.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `comment`
- `csrf_token`
- `elif not user.is_authenticated`
- `elif pode_iniciar`
- `elif user.is_authenticated`
- `else`
- `endblock`
- `endcomment`
- `endif`
- `extends "base.html"`
- `if pode_iniciar`
- `if pode_simplificada`
- `if triagem_extensa_reutilizavel`
- `url 'accounts:cadastro'`
- `url 'accounts:inicio'`
- `url 'accounts:login'`
- `url 'accounts:triagem_historico'`
- `url 'accounts:triagem_iniciar' modalidade='extensa'`
- `url 'accounts:triagem_iniciar' modalidade='simplificada'`

**Valores exibidos:**


**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1019>)


## templates/accounts/triagem_extensa.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/triagem_extensa.html](<C:/Users/lb119/Elo/templates/accounts/triagem_extensa.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `csrf_token`
- `endblock`
- `extends "base.html"`
- `url 'accounts:dashboard'`

**Valores exibidos:**

- `form.as_p`
- `form.non_field_errors`


## templates/accounts/triagem_historico.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/triagem_historico.html](<C:/Users/lb119/Elo/templates/accounts/triagem_historico.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `comment`
- `elif triagem.status == "EM_ANDAMENTO"`
- `else`
- `endblock`
- `endcomment`
- `endfor`
- `endif`
- `extends "base.html"`
- `for triagem in triagens`
- `if triagem.status == "CONCLUIDA"`
- `if triagens`
- `url 'accounts:dashboard'`
- `url 'accounts:triagem_apresentacao'`
- `url 'accounts:triagem_pergunta' id_triagem=triagem.id_triagem`
- `url 'accounts:triagem_resultado' id_triagem=triagem.id_triagem`

**Valores exibidos:**

- `triagem.get_modalidade_display`
- `triagem.get_resultado_display`
- `triagem.get_status_display`
- `triagem.id_triagem`
- `triagem.iniciada_em|date:"d/m/Y H:i"`
- `triagem.regra_version`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1065>)


## templates/accounts/triagem_inicio.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/triagem_inicio.html](<C:/Users/lb119/Elo/templates/accounts/triagem_inicio.html>).

Arquivo vazio: organiza o pacote, sem algoritmo para estudar.
**Instrucoes Django no HTML:**


**Valores exibidos:**



## templates/accounts/triagem_pergunta.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/triagem_pergunta.html](<C:/Users/lb119/Elo/templates/accounts/triagem_pergunta.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `comment`
- `csrf_token`
- `endblock`
- `endcomment`
- `endfor`
- `endif`
- `extends "base.html"`
- `for error in field.errors`
- `for field in form`
- `if field.help_text`
- `if numero_pergunta > 1`
- `url 'accounts:triagem_historico'`

**Valores exibidos:**

- `error`
- `field`
- `field.help_text`
- `field.label_tag`
- `form.non_field_errors`
- `numero_pergunta`
- `pergunta.explicacao`
- `pergunta.titulo`
- `total_perguntas`
- `triagem.get_modalidade_display`
- `triagem.id_triagem`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1232>)


## templates/accounts/triagem_resultado.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/triagem_resultado.html](<C:/Users/lb119/Elo/templates/accounts/triagem_resultado.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `endblock`
- `endfor`
- `endif`
- `extends "base.html"`
- `for achado in triagem.achados`
- `if achado.data_liberacao`
- `if triagem.achados`
- `if triagem.data_liberacao`
- `url 'accounts:dashboard'`

**Valores exibidos:**

- `achado.data_liberacao`
- `achado.mensagem`
- `triagem.data_liberacao|date:"d/m/Y"`
- `triagem.get_resultado_display`
- `triagem.mensagem_resultado`
- `triagem.regra_version`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1304>)


## templates/accounts/triagem_revisao.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/accounts/triagem_revisao.html](<C:/Users/lb119/Elo/templates/accounts/triagem_revisao.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `csrf_token`
- `empty`
- `endblock`
- `endfor`
- `endif`
- `extends "base.html"`
- `for item in respostas_revisao`
- `if item.detalhes`
- `url 'accounts:triagem_pergunta' triagem.id_triagem`

**Valores exibidos:**

- `item.detalhes`
- `item.id`
- `item.resposta`
- `item.titulo`

**Referencias ao caminho do template no Python:**

- [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py:1279>)


## templates/base.html

Template de apresentacao; compare variaveis recebidas e view que o renderiza.

Original: [templates/base.html](<C:/Users/lb119/Elo/templates/base.html>).

**Instrucoes Django no HTML:**

- `block content`
- `block title`
- `comment`
- `csrf_token`
- `else`
- `endblock`
- `endcomment`
- `endfor`
- `endif`
- `for message in messages`
- `if messages`
- `if user.is_authenticated`
- `if user.is_staff or user.is_superuser or user.perfil == "ADMINISTRADOR"`
- `if user.perfil == "HEMOCENTRO" and user.status_validacao == "APROVADO"`
- `if user.perfil == "RECEPTOR"`
- `load static`
- `static 'css/elo.css'`
- `static 'css/favicon.png'`
- `url 'accounts:cadastro'`
- `url 'accounts:compatibilidade_sanguinea'`
- `url 'accounts:dashboard'`
- `url 'accounts:estoque_hemocentro'`
- `url 'accounts:estoque_publico'`
- `url 'accounts:inicio'`
- `url 'accounts:login'`
- `url 'accounts:logout'`
- `url 'accounts:painel_aprovacao_hemocentros'`
- `url 'accounts:painel_pedidos_hemocentro'`
- `url 'accounts:painel_validacao_pedidos'`
- `url 'accounts:pedido_publicar'`
- `url 'accounts:triagem_apresentacao'`

**Valores exibidos:**

- `message`
- `message.tags|default:'info'`
- `user.get_short_name`

**JavaScript embutido:** leia os eventos e seletores na copia integral; ele organiza interacao no navegador, sem substituir autorizacao no servidor.


## Cobertura desta referencia

96 arquivos de texto e 502 definicoes de classes/funcoes/metodos foram indexados. A copia completa contem todos os arquivos do inventario, incluindo arquivos sem definicoes Python. Nao foram lidos .env real, Git interno ou dependencias instaladas.
