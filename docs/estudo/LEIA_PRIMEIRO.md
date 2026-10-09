# Elo explicado por arquivo e por bloco

Material de 09/10/2026. Comece pelo [guia de arquitetura e fluxos](GUIA_ELO.md). Aqui cada arquivo tem seu caderno com código integral, trechos organizados e leitura de suas instruções.

As explicações de instruções foram extraídas por análise estrutural: explicam operações visíveis no código, sem executar o sistema. A intenção dos fluxos é explicada no guia. Nomes de métodos iguais podem ter significados diferentes conforme o objeto; confirme o tipo e os chamadores na referência. Comentários antigos não prevalecem sobre o corpo executado.

Nenhum arquivo do sistema foi alterado. .env real, banco, bibliotecas instaladas e arquivos binários não estão copiados.

## Ordem de leitura

1. Guia, Python básico e configuração.
2. Models, cadastro, login e perfis.
3. Rotas e views com seus templates.
4. Serviços de hemocentros, pedidos, estoque e compatibilidade.
5. Catálogos, formulários, serviço e motor da triagem.
6. Auditoria, sinais, admin, notificações, CSS.
7. Migrations, testes e comando de contas fictícias.

## Todos os arquivos

| Arquivo | Explicação detalhada |
| --- | --- |
| `.env.example` | [Código e explicação](por_arquivo/_env_example.md) |
| `.gitignore` | [Código e explicação](por_arquivo/_gitignore.md) |
| `accounts/__init__.py` | [Código e explicação](por_arquivo/accounts____init___py.md) |
| `accounts/admin.py` | [Código e explicação](por_arquivo/accounts__admin_py.md) |
| `accounts/apps.py` | [Código e explicação](por_arquivo/accounts__apps_py.md) |
| `accounts/auditoria.py` | [Código e explicação](por_arquivo/accounts__auditoria_py.md) |
| `accounts/compatibilidade.py` | [Código e explicação](por_arquivo/accounts__compatibilidade_py.md) |
| `accounts/estoque.py` | [Código e explicação](por_arquivo/accounts__estoque_py.md) |
| `accounts/forms.py` | [Código e explicação](por_arquivo/accounts__forms_py.md) |
| `accounts/management/__init__.py` | [Código e explicação](por_arquivo/accounts__management____init___py.md) |
| `accounts/management/commands/__init__.py` | [Código e explicação](por_arquivo/accounts__management__commands____init___py.md) |
| `accounts/management/commands/criar_perfis_teste.py` | [Código e explicação](por_arquivo/accounts__management__commands__criar_perfis_teste_py.md) |
| `accounts/migrations/0001_initial.py` | [Código e explicação](por_arquivo/accounts__migrations__0001_initial_py.md) |
| `accounts/migrations/0002_remove_usuario_cidade_remove_usuario_cnpj_and_more.py` | [Código e explicação](por_arquivo/accounts__migrations__0002_remove_usuario_cidade_remove_usuario_cnpj_and_more_py.md) |
| `accounts/migrations/0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more.py` | [Código e explicação](por_arquivo/accounts__migrations__0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more_py.md) |
| `accounts/migrations/0004_auditoriaacaocritica.py` | [Código e explicação](por_arquivo/accounts__migrations__0004_auditoriaacaocritica_py.md) |
| `accounts/migrations/0005_usuario_status_validacao_validacaohemocentro.py` | [Código e explicação](por_arquivo/accounts__migrations__0005_usuario_status_validacao_validacaohemocentro_py.md) |
| `accounts/migrations/0006_triagem_respostatriagem_and_more.py` | [Código e explicação](por_arquivo/accounts__migrations__0006_triagem_respostatriagem_and_more_py.md) |
| `accounts/migrations/0007_alter_auditoriaacaocritica_acao_estoque_and_more.py` | [Código e explicação](por_arquivo/accounts__migrations__0007_alter_auditoriaacaocritica_acao_estoque_and_more_py.md) |
| `accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py` | [Código e explicação](por_arquivo/accounts__migrations__0007_alter_respostatriagem_options_alter_triagem_options_and_more_py.md) |
| `accounts/migrations/0008_merge_triagem_estoque_branches.py` | [Código e explicação](por_arquivo/accounts__migrations__0008_merge_triagem_estoque_branches_py.md) |
| `accounts/migrations/0009_usuario_tipo_sanguineo_notificacao.py` | [Código e explicação](por_arquivo/accounts__migrations__0009_usuario_tipo_sanguineo_notificacao_py.md) |
| `accounts/migrations/0010_pedidosangue.py` | [Código e explicação](por_arquivo/accounts__migrations__0010_pedidosangue_py.md) |
| `accounts/migrations/0011_alinhar_pedidos_validacao.py` | [Código e explicação](por_arquivo/accounts__migrations__0011_alinhar_pedidos_validacao_py.md) |
| `accounts/migrations/0012_pedidosangue_contato_and_more.py` | [Código e explicação](por_arquivo/accounts__migrations__0012_pedidosangue_contato_and_more_py.md) |
| `accounts/migrations/0013_usuario_suspensa.py` | [Código e explicação](por_arquivo/accounts__migrations__0013_usuario_suspensa_py.md) |
| `accounts/migrations/0014_notificacao_pedido_and_more.py` | [Código e explicação](por_arquivo/accounts__migrations__0014_notificacao_pedido_and_more_py.md) |
| `accounts/migrations/0015_pedido_contato_email.py` | [Código e explicação](por_arquivo/accounts__migrations__0015_pedido_contato_email_py.md) |
| `accounts/migrations/__init__.py` | [Código e explicação](por_arquivo/accounts__migrations____init___py.md) |
| `accounts/migrations/README.md` | [Código e explicação](por_arquivo/accounts__migrations__README_md.md) |
| `accounts/models.py` | [Código e explicação](por_arquivo/accounts__models_py.md) |
| `accounts/pedidos.py` | [Código e explicação](por_arquivo/accounts__pedidos_py.md) |
| `accounts/signals.py` | [Código e explicação](por_arquivo/accounts__signals_py.md) |
| `accounts/test_estoque.py` | [Código e explicação](por_arquivo/accounts__test_estoque_py.md) |
| `accounts/test_fluxo_requisitos.py` | [Código e explicação](por_arquivo/accounts__test_fluxo_requisitos_py.md) |
| `accounts/test_pedidos.py` | [Código e explicação](por_arquivo/accounts__test_pedidos_py.md) |
| `accounts/test_perfis_teste.py` | [Código e explicação](por_arquivo/accounts__test_perfis_teste_py.md) |
| `accounts/test_triagem.py` | [Código e explicação](por_arquivo/accounts__test_triagem_py.md) |
| `accounts/test_triagem_catalogos.py` | [Código e explicação](por_arquivo/accounts__test_triagem_catalogos_py.md) |
| `accounts/test_triagem_forms.py` | [Código e explicação](por_arquivo/accounts__test_triagem_forms_py.md) |
| `accounts/test_triagem_models.py` | [Código e explicação](por_arquivo/accounts__test_triagem_models_py.md) |
| `accounts/test_triagem_motor.py` | [Código e explicação](por_arquivo/accounts__test_triagem_motor_py.md) |
| `accounts/test_triagem_servico.py` | [Código e explicação](por_arquivo/accounts__test_triagem_servico_py.md) |
| `accounts/test_triagem_views.py` | [Código e explicação](por_arquivo/accounts__test_triagem_views_py.md) |
| `accounts/test_visualizacao.py` | [Código e explicação](por_arquivo/accounts__test_visualizacao_py.md) |
| `accounts/tests.py` | [Código e explicação](por_arquivo/accounts__tests_py.md) |
| `accounts/triagem.py` | [Código e explicação](por_arquivo/accounts__triagem_py.md) |
| `accounts/triagem_catalogo.py` | [Código e explicação](por_arquivo/accounts__triagem_catalogo_py.md) |
| `accounts/triagem_catalogo_extensa.py` | [Código e explicação](por_arquivo/accounts__triagem_catalogo_extensa_py.md) |
| `accounts/triagem_catalogo_simplificada.py` | [Código e explicação](por_arquivo/accounts__triagem_catalogo_simplificada_py.md) |
| `accounts/triagem_forms.py` | [Código e explicação](por_arquivo/accounts__triagem_forms_py.md) |
| `accounts/triagem_motor.py` | [Código e explicação](por_arquivo/accounts__triagem_motor_py.md) |
| `accounts/triagem_servico.py` | [Código e explicação](por_arquivo/accounts__triagem_servico_py.md) |
| `accounts/urls.py` | [Código e explicação](por_arquivo/accounts__urls_py.md) |
| `accounts/validacao_hemocentro.py` | [Código e explicação](por_arquivo/accounts__validacao_hemocentro_py.md) |
| `accounts/validacao_pedido.py` | [Código e explicação](por_arquivo/accounts__validacao_pedido_py.md) |
| `accounts/views.py` | [Código e explicação](por_arquivo/accounts__views_py.md) |
| `config/__init__.py` | [Código e explicação](por_arquivo/config____init___py.md) |
| `config/asgi.py` | [Código e explicação](por_arquivo/config__asgi_py.md) |
| `config/settings.py` | [Código e explicação](por_arquivo/config__settings_py.md) |
| `config/settings_test.py` | [Código e explicação](por_arquivo/config__settings_test_py.md) |
| `config/urls.py` | [Código e explicação](por_arquivo/config__urls_py.md) |
| `config/wsgi.py` | [Código e explicação](por_arquivo/config__wsgi_py.md) |
| `docs/superpowers/plans/2026-09-04-triagem-completa.md` | [Código e explicação](por_arquivo/docs__superpowers__plans__2026-09-04-triagem-completa_md.md) |
| `docs/superpowers/specs/2026-09-04-triagem-completa-design.md` | [Código e explicação](por_arquivo/docs__superpowers__specs__2026-09-04-triagem-completa-design_md.md) |
| `elo_front/README-INSTALACAO.txt` | [Código e explicação](por_arquivo/elo_front__README-INSTALACAO_txt.md) |
| `elo_front/static/css/elo.css` | [Código e explicação](por_arquivo/elo_front__static__css__elo_css.md) |
| `elo_front/templates/accounts/inicio.html` | [Código e explicação](por_arquivo/elo_front__templates__accounts__inicio_html.md) |
| `elo_front/templates/base.html` | [Código e explicação](por_arquivo/elo_front__templates__base_html.md) |
| `manage.py` | [Código e explicação](por_arquivo/manage_py.md) |
| `README.md` | [Código e explicação](por_arquivo/README_md.md) |
| `requirements.txt` | [Código e explicação](por_arquivo/requirements_txt.md) |
| `templates/accounts/cadastro.html` | [Código e explicação](por_arquivo/templates__accounts__cadastro_html.md) |
| `templates/accounts/compatibilidade_sanguinea.html` | [Código e explicação](por_arquivo/templates__accounts__compatibilidade_sanguinea_html.md) |
| `templates/accounts/dashboard.html` | [Código e explicação](por_arquivo/templates__accounts__dashboard_html.md) |
| `templates/accounts/estoque_hemocentro.html` | [Código e explicação](por_arquivo/templates__accounts__estoque_hemocentro_html.md) |
| `templates/accounts/estoque_publico.html` | [Código e explicação](por_arquivo/templates__accounts__estoque_publico_html.md) |
| `templates/accounts/inicio.html` | [Código e explicação](por_arquivo/templates__accounts__inicio_html.md) |
| `templates/accounts/login.html` | [Código e explicação](por_arquivo/templates__accounts__login_html.md) |
| `templates/accounts/minhas_solicitacoes.html` | [Código e explicação](por_arquivo/templates__accounts__minhas_solicitacoes_html.md) |
| `templates/accounts/painel_aprovacao_hemocentros.html` | [Código e explicação](por_arquivo/templates__accounts__painel_aprovacao_hemocentros_html.md) |
| `templates/accounts/painel_moderacao_pedidos.html` | [Código e explicação](por_arquivo/templates__accounts__painel_moderacao_pedidos_html.md) |
| `templates/accounts/painel_validacao_pedidos.html` | [Código e explicação](por_arquivo/templates__accounts__painel_validacao_pedidos_html.md) |
| `templates/accounts/pedido_detalhe.html` | [Código e explicação](por_arquivo/templates__accounts__pedido_detalhe_html.md) |
| `templates/accounts/pedido_filtrar.html` | [Código e explicação](por_arquivo/templates__accounts__pedido_filtrar_html.md) |
| `templates/accounts/pedido_publicar.html` | [Código e explicação](por_arquivo/templates__accounts__pedido_publicar_html.md) |
| `templates/accounts/pedidos_listar.html` | [Código e explicação](por_arquivo/templates__accounts__pedidos_listar_html.md) |
| `templates/accounts/triagem_apresentacao.html` | [Código e explicação](por_arquivo/templates__accounts__triagem_apresentacao_html.md) |
| `templates/accounts/triagem_extensa.html` | [Código e explicação](por_arquivo/templates__accounts__triagem_extensa_html.md) |
| `templates/accounts/triagem_historico.html` | [Código e explicação](por_arquivo/templates__accounts__triagem_historico_html.md) |
| `templates/accounts/triagem_inicio.html` | [Código e explicação](por_arquivo/templates__accounts__triagem_inicio_html.md) |
| `templates/accounts/triagem_pergunta.html` | [Código e explicação](por_arquivo/templates__accounts__triagem_pergunta_html.md) |
| `templates/accounts/triagem_resultado.html` | [Código e explicação](por_arquivo/templates__accounts__triagem_resultado_html.md) |
| `templates/accounts/triagem_revisao.html` | [Código e explicação](por_arquivo/templates__accounts__triagem_revisao_html.md) |
| `templates/base.html` | [Código e explicação](por_arquivo/templates__base_html.md) |
| `TESTAR_PERFIS.md` | [Código e explicação](por_arquivo/TESTAR_PERFIS_md.md) |

## Como conferir se entendeu um trecho

Leia o código, acompanhe as linhas explicadas e volte à referência para localizar os chamadores. Depois responda: qual entrada recebe, o que valida, que dados altera, que valor devolve e qual teste demonstra o comportamento?

Cobertura: 96 arquivos; 3954 instruções Python identificadas. Todos os arquivos têm sua cópia integral; Python tem leitura dos blocos, HTML tem leitura das linhas e CSS tem leitura das declarações. Arquivos vazios são marcadores de pacote. Exclusões: segredos, binários e código de dependências externas.
