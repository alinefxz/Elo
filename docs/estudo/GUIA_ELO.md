# Estudo do Elo: do navegador ao banco

Material preparado em 09/10/2026 a partir do código local. Este guia explica a arquitetura e os fluxos; a referência complementar indexa cada arquivo, classe, função e método. Não houve alteração no código executável para produzir este material.

## Como usar este material

Leia este guia na ordem. Depois abra [REFERENCIA_CODIGO.md](REFERENCIA_CODIGO.md) no capítulo do arquivo que estiver estudando. Cada símbolo tem um link para sua linha original, documentação existente, chamadas e retornos observáveis no código. [CODIGO_COMPLETO.md](CODIGO_COMPLETO.md) reúne uma cópia numerada dos arquivos para consulta, inclusive testes, migrations, HTML e CSS. As cópias representam esta data; depois de alterações, o arquivo original passa a ser a fonte atual.

Esses três materiais têm papéis diferentes: o guia explica o funcionamento; a referência ajuda a localizar e seguir cada função; a cópia permite consultar o conteúdo integral. A referência estrutural foi extraída automaticamente e não deve ser confundida com uma comprovação de que toda função é executada em todos os fluxos. Docstrings e comentários também podem estar antigos: confirme o corpo da função e quem a chama.

As explicações mostram de onde vêm os dados, como o sistema os confere, o que é salvo e qual resultado aparece para o usuário. Não é necessário decorar os nomes: eles foram mantidos para facilitar a localização nos arquivos.

## 1. O que é o sistema

Elo é uma aplicação web Django. O usuário abre páginas pelo navegador, preenche formulários e executa ações. Python processa essas ações; PostgreSQL guarda os dados; HTML apresenta o resultado; CSS define a aparência. Não há necessidade de o navegador conhecer a senha do banco ou executar a regra de compatibilidade.

O app `accounts` concentra mais que contas: autenticação, perfis, hemocentros, triagem, estoque, pedidos, notificações e auditoria. O nome da pasta não limita sua responsabilidade real.

O fluxo geral é:

```text
Navegador → middleware → rota → view → formulário/serviço → modelos/ORM → banco
                                ↓
                       contexto + template → HTML → navegador
```

Nem toda requisição acessa todas essas camadas. Uma consulta pode apenas ler; um POST pode validar, salvar e redirecionar para uma nova consulta.

## 2. Python que você precisa reconhecer

Antes dos códigos, estes nomes ajudam a entender as explicações:

| Nome no código ou na explicação | O que significa |
| --- | --- |
| Variável | Um nome usado para guardar um valor, como uma quantidade ou um e-mail. |
| Função | Uma parte do programa que faz uma tarefa quando é chamada. |
| Classe | Um molde que reúne informações e ações. A classe Usuario define como uma conta é representada. |
| Objeto | Uma representação criada usando esse molde, como uma conta específica. |
| Método | Uma função que pertence a uma classe ou a um objeto. |
| Parâmetro | Um dado que a função recebe para fazer seu trabalho. |
| Retorno | O resultado que a função entrega à parte que a chamou. |
| Banco de dados | O lugar onde as contas, estoques, pedidos e outros registros ficam guardados. |
| Model | A classe que descreve um tipo de registro do banco. |
| ORM | A ferramenta do Django que permite buscar e salvar no banco usando Python. |
| View | A função que recebe o pedido do navegador e prepara a resposta. |
| Template | O arquivo que organiza o conteúdo da tela. |
| Rota | O endereço ligado a uma ação do sistema, como /dashboard/. |
| Validação | A conferência dos dados antes de aceitá-los ou salvá-los. |
| Permissão | A regra que define quem pode executar uma ação. |
| Exceção | Um aviso de erro que interrompe o caminho normal do programa. |
| Transação | Um grupo de alterações no banco que precisam dar certo juntas. Se houver uma falha que saia desse grupo, suas alterações são desfeitas. |
| Migration | Um arquivo que registra uma mudança na estrutura do banco. |
| Decorador | Uma regra colocada antes da função, como exigir login para executá-la. |

`import` traz nomes de outros módulos. `from .models import Usuario` usa o ponto para indicar um módulo do mesmo pacote. Não significa copiar a tabela: importa a classe Python que representa os usuários.

`def` declara função; os parâmetros recebem dados; `return` entrega o resultado ao chamador. `class` declara uma classe. Em métodos, `self` é a instância; `cls` é a classe. Herança permite reaproveitar comportamento: `Usuario(AbstractUser)` recebe recursos de autenticação do Django.

`if/elif/else` escolhe caminhos. `for` percorre uma coleção. Uma compreensão, como `[x for x in itens if ...]`, monta uma lista. Dicionários ligam chaves a valores: `dados['email']`. `.get('email')` permite obter uma chave ausente sem `KeyError`.

`None` representa ausência; não é igual à string vazia `''`. `True` e `False` são booleanos. Datas não são textos comuns: o projeto converte formatos quando necessário.

`raise PermissionDenied(...)` interrompe uma ação sem permissão. `ValidationError` informa dados inválidos; `Http404` indica recurso não encontrado. `try/except` trata uma falha prevista. Não confunda validação de dados com autorização: e-mail válido não concede acesso.

O `*` em parâmetros, como `def cadastrar_estoque(*, hemocentro, ...)`, exige argumentos pelo nome. `**kwargs` reúne argumentos adicionais. F-strings, como `f'Estoque {nivel}'`, inserem valores no texto.

`@login_required`, `@require_POST` e `@transaction.atomic` são decoradores: adicionam comportamento ao executar a função. O nome do decorador importa tanto quanto o corpo.

## 3. Inicialização e configuração

`manage.py` é a entrada dos comandos: define as configurações e delega ao Django. `runserver` inicia o servidor local; `check` verifica configuração; `test` executa testes; `migrate` aplica mudanças versionadas no banco. Esses comandos fazem coisas diferentes.

`config/settings.py` define apps, middlewares, templates, PostgreSQL, autenticação, fuso, arquivos estáticos e limites de convocação. `BASE_DIR` localiza a raiz. `load_dotenv` lê o `.env`. O `.env` real contém segredos e não foi incluído no material de estudo. Não é necessário conhecer seus valores para entender como a configuração funciona.

`AUTH_USER_MODEL = 'accounts.Usuario'` troca o usuário padrão pela classe do projeto. `INSTALLED_APPS` ativa componentes; `MIDDLEWARE` define a sequência de processamento; `TEMPLATES['DIRS']` aponta para `templates/`; `STATICFILES_DIRS` inclui os estilos de `elo_front/static`.

`CONVOCACAO_INTERVALO_HORAS`, `CONVOCACAO_LIMITE_NOTIFICACOES` e `CONVOCACAO_VERSAO_CONSENTIMENTO` são configurações consumidas pelas regras. Os valores atuais são 24 horas, uma notificação e versão `1.0`.

`config/settings_test.py` importa a configuração base e substitui o banco por SQLite em memória. Isso permite testes sem criar banco PostgreSQL de testes. Não muda o banco utilizado pelo servidor normal. Um teste SQLite também não demonstra o comportamento real de bloqueios concorrentes no PostgreSQL.

`config/urls.py` inclui as rotas do app e `/admin/`. `wsgi.py` e `asgi.py` são entradas para servidores compatíveis com esses protocolos. `__init__.py` identifica pacotes; alguns arquivos são vazios porque não precisam executar código.

`requirements.txt` fixa dependências: Django, driver PostgreSQL, leitura do `.env` e bibliotecas auxiliares. As versões declaradas são instruções de instalação, não prova da versão efetivamente instalada em qualquer computador. Neste arquivo, Django está fixado em `5.2.17`.

## 4. URLs, views e templates

Uma declaração `path('dashboard/', views.dashboard, name='dashboard')` liga endereço, função e nome. `app_name = 'accounts'` cria o namespace. `reverse('accounts:dashboard')` e `{% url 'accounts:dashboard' %}` montam endereços a partir do nome, evitando repetições de strings.

O `request` contém método, usuário, parâmetros e corpo. `request.GET` contém consulta da URL; `request.POST` contém dados submetidos; `request.user` representa quem está autenticado. O ID recebido na URL identifica um objeto, mas não garante que o usuário possa acessá-lo.

Uma view coordena a requisição. `render(request, template, contexto)` produz HTML. `redirect(...)` envia o navegador para outro endereço. `get_object_or_404` procura um registro e responde 404 se não o encontra. Restringir a busca ao usuário ou hemocentro atual protege a propriedade dos dados.

Templates usam `{{ valor }}` para apresentar dados, `{% if %}` para condições e `{% for %}` para listas. `{% extends 'base.html' %}` reaproveita a estrutura geral; `{% block content %}` preenche a área da página. `{% csrf_token %}` protege formulários contra submissões indevidas de outro site, mas não substitui verificações de perfil.

`templates/base.html` contém navegação, mensagens, estrutura comum e script de menu. `elo_front/static/css/elo.css` controla a apresentação. Os arquivos HTML em `elo_front/templates` são um conjunto visual alternativo: a configuração atual aponta para `templates/` na raiz, não para essa pasta de cópias. Ter dois arquivos com o mesmo nome não significa usar os dois.

Leia todos os templates na referência: cada um está associado ao seu objetivo, às views que o mencionam, aos formulários e links encontrados. Alguns templates não são referenciados diretamente pelas views atuais; isso não permite presumir sozinho que possam ser apagados.

## 5. Modelos e ORM: onde os dados vivem

`accounts/models.py` descreve as entidades persistidas. `CharField` guarda texto; `BooleanField` guarda sim/não; `DateField` guarda dia; `DateTimeField` inclui horário; `JSONField` armazena estruturas; `ForeignKey` relaciona registros. `choices` define alternativas; `default` define valor inicial; `null` diz se o banco admite ausência; `blank` diz se a validação permite campo vazio.

`primary_key` identifica um registro. `unique=True` impede repetição. `Meta.db_table` define o nome SQL; `ordering` define ordenação padrão; `indexes` favorece consultas; `constraints` protege combinações de dados. Índice não concede permissão e não valida todas as regras.

`related_name` dá acesso pelo lado oposto de uma relação. `request.user.notificacoes` consulta avisos daquele usuário. `on_delete=CASCADE` apaga dependentes quando o pai é apagado; `SET_NULL` preserva o registro e remove o vínculo.

| Modelo | Para que serve |
| --- | --- |
| `UsuarioManager` | Cria contas e transforma a senha em hash; configura criação de superusuário. Não é uma tabela separada. |
| `Usuario` | Conta, e-mail de login, perfil, documentos, cidade, tipo sanguíneo, suspensão e estado do hemocentro. |
| `ValidacaoHemocentro` | Histórico das análises institucionais, responsável e parecer. |
| `ConsentimentoLGPD` | Tipo de termo, versão, aceite, revogação, data e IP. |
| `AuditoriaAcaoCritica` | Eventos relevantes, autor, alvo, resultado e metadados. |
| `Triagem` | Modalidade, progresso, versão da regra, resultado, achados e data orientativa. |
| `RespostaTriagem` | Respostas vinculadas à triagem, códigos, valores estruturados e referência da regra. |
| `Estoque` | Quantidade e limiares por hemocentro e tipo sanguíneo. |
| `EstoqueMovimentacao` | Histórico de entradas, saídas e ajustes, com responsável. |
| `Notificacao` | Aviso interno, destinatário, conteúdo, destino, leitura e datas. |
| `PedidoSangue` | Solicitação, destino, tipo, urgência, conteúdo, estado e publicação. |
| `ValidacaoPedido` | Histórico das decisões sobre um pedido. |

Exemplo: `Usuario.objects.filter(perfil=Usuario.Perfil.DOADOR)` produz uma consulta, não uma lista de todos os usuários já carregada. QuerySets são normalmente avaliados quando usados. `.get()` espera um único registro; `.first()` retorna o primeiro ou `None`; `.exists()` verifica existência; `.count()` conta; `.create()` grava; `.update()` altera em lote; `.save()` persiste uma instância.

`full_clean()` valida a instância explicitamente. Um `save()` simples não chama automaticamente todas as validações de `full_clean()`. `select_related()` traz relações na mesma consulta; `prefetch_related()` busca relações em consultas adicionais coordenadas. `select_for_update()` pede bloqueio de registros durante uma transação. `Subquery`, `OuterRef` e `Exists` permitem consultar, por exemplo, a última triagem e o consentimento sem carregar todos os históricos em Python.

`transaction.atomic()` agrupa gravações: uma falha que escape do bloco provoca rollback das operações daquele bloco. O momento em que uma exceção é tratada também importa. Na triagem, há cuidado específico para registrar cancelamento antes da exceção que orienta o redirecionamento.

## 6. Cadastro, login e perfis

`CadastroUsuarioForm` reutiliza `UserCreationForm`. Métodos `clean_nome`, `clean_email`, `clean_cpf`, `clean_cnpj`, `clean_estado` e `clean_password1` tratam campos; `clean()` combina regras entre campos. `apenas_digitos` remove formatação. Limpeza e validação de comprimento não devem ser confundidas com uma comprovação externa de autenticidade de documentos.

A view `cadastro` recebe POST, valida, salva conta e consentimento geral dentro de transação, registra a preferência opcional de convocação do doador e inicia sua sessão. `set_password()` armazena hash, não a senha em texto comum.

`LoginView` usa `LoginUsuarioForm`; o identificador é e-mail porque `USERNAME_FIELD = 'email'`. O formulário verifica se a conta pode entrar, incluindo suspensão. Sessão conserva a autenticação entre requisições. Logout ocorre por POST.

O perfil é uma regra do Elo. `is_staff` e `is_superuser` são propriedades administrativas do Django. Não significam a mesma coisa. Os serviços e views verificam o perfil conforme a operação; o admin também utiliza permissões próprias.

| Perfil | Fluxo principal atual |
| --- | --- |
| Visitante | Consulta pública; sem conta. |
| Doador | Triagem própria, preferência de convocação e alertas elegíveis. |
| Receptor | Solicita divulgação e acompanha suas solicitações. |
| Hemocentro | Quando aprovado, controla seu estoque e analisa os pedidos destinados a ele. |
| Observador | Consulta informações conforme as áreas públicas e seu painel. |
| Administrador | Valida instituições, modera pedidos e consulta auditoria com permissões apropriadas. |

`PAINEIS_POR_PERFIL` fornece textos e ações; `montar_visibilidade_dashboard` calcula os blocos visíveis. Esconder um botão não protege uma rota. A segurança depende das verificações do servidor, mesmo se alguém digitar a URL diretamente.

`validacao_hemocentro.py` concentra aprovação, recusa, correção e verificações institucionais. O estado atual fica em `Usuario`; o histórico fica em `ValidacaoHemocentro`. O estado atual permite consulta rápida; o histórico explica como se chegou a ele.

## 7. Triagem: catálogo, formulário, serviço e motor

Esta área é grande porque separa quatro responsabilidades. Os catálogos descrevem perguntas; o formulário recebe respostas; o serviço controla andamento e persistência; o motor calcula orientação.

`triagem_catalogo_extensa.py` declara perguntas e regras com códigos estáveis, textos, alternativas, condições, exigências de data e fonte. Os construtores `opcao`, `regra`, `pergunta` e `pergunta_tabela` padronizam os dicionários. Estude uma pergunta inteira: entrada da alternativa → regra correspondente → resultado → prazo → fonte. Repita para os blocos diferentes, não apenas para o primeiro.

`triagem_catalogo_simplificada.py` define perguntas rápidas e situações que abrem detalhes da extensa. `triagem_catalogo.py` fornece acesso uniforme e valida consistência, incluindo alternativas e destinos inexistentes. Versão de regra permite relacionar um resultado histórico à lógica usada.

`FormularioPergunta` em `triagem_forms.py` monta campos a partir da pergunta escolhida. Algumas exigem uma alternativa; outras várias; certas respostas exigem data ou detalhes. A validação produz valores que o serviço pode salvar.

`triagem_servico.py` permite iniciar ou retomar, exige perfil e aceite, encontra uma extensa de base para a simplificada, calcula quais perguntas precisam aparecer, valida códigos, salva respostas, permite revisão e conclui. A busca das views limita triagens ao próprio usuário.

`salvar_resposta` usa bloqueio e `update_or_create` para corrigir uma pergunta sem duplicar sua resposta. Uma resposta pode mudar o fluxo futuro. Algumas escolhas cancelam a simplificada e exigem uma extensa. Respostas instáveis não são simplesmente herdadas como se fossem atuais.

`triagem_motor.py` recebe as respostas e aplica regras. Não grava banco, embora importe os nomes de resultados do model. Converte datas, calcula prazos, verifica condições, preserva achados e escolhe o resultado mais restritivo. A data final considera os prazos encontrados. Os resultados descrevem orientação e não substituem a decisão presencial.

`triagem.py` contém o cálculo inicial e funções usadas na evolução do projeto. Não confunda automaticamente esse módulo com o motor atual. Na referência, use a lista de chamadas para localizar qual função a view ou serviço realmente utiliza. `TriagemExtensaForm` em `forms.py` também pertence a esse conjunto inicial.

Fluxo de estudo: `triagem_iniciar` → `iniciar_triagem` → `calcular_fluxo` → `triagem_pergunta` → `FormularioPergunta` → `salvar_resposta` → revisão/conclusão → `avaliar_triagem` → resultado/histórico. A rota exata e os retornos de cada etapa estão na referência.

## 8. Estoque e alerta crítico

`CadastrarEstoqueForm` valida dados iniciais. `MovimentarEstoqueForm` trata entradas, saídas e ajustes. `estoque.py` verifica se o responsável é o hemocentro aprovado dono daquele estoque.

Entrada soma bolsas; saída subtrai; ajuste define a quantidade informada. `registrar_movimentacao_estoque` valida, grava a mudança, registra histórico, calcula estado, tenta criar notificações e registra auditoria. O cálculo é:

```python
if quantidade_bolsas <= nivel_critico:
    return Estoque.StatusCalculado.CRITICO
if quantidade_bolsas <= nivel_minimo:
    return Estoque.StatusCalculado.BAIXO
return Estoque.StatusCalculado.ESTAVEL
```

Exemplo com mínimo 10 e crítico 5: 12 é estável, 7 é baixo, 5 é crítico. A igualdade pertence ao estado mais restritivo porque usa `<=`.

O mapa `STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA` atualmente contém somente crítico. A função retorna zero quando o estado não gera convocação. O cadastro inicial de estoque não chama o mesmo disparo; a atualização chama. Não existe uma rotina automática de reenvio apenas porque o tempo passou.

`visualizacao_publica_estoque` e `FiltroEstoquePublicoForm` atendem consulta pública. `obter_estoques_publicos` organiza o conjunto público. Separe a quantidade real dos registros do banco de `ESTOQUE_GERAL`, uma lista de exemplos na view usada em partes da apresentação.

## 9. Compatibilidade, aptidão e consentimento

`COMPATIBILIDADE_RECEBIMENTO` relaciona o tipo solicitado aos tipos de doadores aceitos pela tabela do sistema. A interface informativa e a seleção de candidatos compartilham essa tabela. `normalizar_tipo_sanguineo` limpa o texto e rejeita tipo desconhecido; `tipos_que_recebem_de` percorre o sentido inverso.

`doadores_aptos_para_convocacao` combina perfil, conta ativa, ausência de suspensão, sangue compatível, preferência de receber avisos, consentimento válido da versão configurada e resultado da última triagem concluída. Também verifica a data de liberação quando existe.

Não basta existir uma triagem antiga apta: a consulta seleciona a última concluída. O alias `APTO` corresponde ao resultado orientativo definido no model; isso não representa autorização clínica definitiva. Não há uma regra de vencimento por idade da triagem nessa seleção, além das condições explicitamente presentes no código.

`limite_convocacao_atingido` conta avisos de estoque e pedido dentro de uma janela móvel. Ler o aviso não remove a contagem. Tipos antigos de estoque baixo continuam contando se já existirem no histórico e estiverem dentro da janela; retirar o novo disparo não apaga histórico.

`atualizar_preferencia_convocacao` salva a preferência e o consentimento/revogação de forma coordenada e registra auditoria. Um booleano `True` sozinho não é prova suficiente de aceite: por isso a seleção também verifica `ConsentimentoLGPD`.

Exemplo técnico: pedido O− → tabela devolve O− → consulta busca doadores desse tipo → exclui quem não satisfaz aptidão/consentimento → função verifica frequência e duplicidade → salva notificações internas.

## 10. Pedidos e decisões

`PedidoSangueForm` recebe a solicitação. `criar_pedido_pendente` valida novamente dados importantes e exige Receptor autenticado. Cria estado `ENVIADA`, sem publicar. Verifica semelhanças recentes e marca possível duplicidade como alerta, não como conclusão de fraude.

`validacao_pedido.py` concentra decisões e autorização. O hemocentro aprovado de destino publica, recusa ou solicita correção conforme a ação. O administrador tem a moderação prevista no serviço; não substitui a publicação institucional. Uma decisão cria `ValidacaoPedido` e auditoria.

Os estados incluem enviada, em análise, publicada, correção solicitada, recusada e encerrada. Leia os estados e aliases em `models.py`: nomes antigos podem apontar a valores atuais para preservar compatibilidade de código.

`pedidos.py` contém verificação de publicação, caminho alternativo de publicação e criação dos alertas. `criar_notificacoes_para_pedido` só atua para pedido publicado e hemocentro aprovado. Usa os mesmos candidatos e limite da convocação de estoque. A existência de uma notificação anterior daquele pedido impede duplicação mesmo depois de lida.

`consultar_pedidos` lista publicados e aplica filtros/ordenação. `minhas_solicitacoes` limita ao solicitante. `painel_pedidos_hemocentro` limita à instituição de destino. `painel_validacao_pedidos` atende moderação administrativa. Não confunda telas semelhantes com acesso ao mesmo conjunto de dados.

## 11. Central de notificações

`Notificacao` já tinha campos de conteúdo, destino e leitura. A organização recente aproveita esses campos no dashboard: lista paginada de dez itens, data, tipo, lida/não lida, contador e ação.

Quando recebe POST com `acao='marcar_notificacao_lida'`, a view valida o identificador, busca dentro de `request.user.notificacoes` e atualiza somente se ainda não estava lida. `lida_em` usa `timezone.now()`. Repetir a ação não regrava a primeira data. A busca por dono impede marcar o aviso de outra pessoa.

Esse POST é separado do formulário de preferência, que já usa o mesmo dashboard. A decisão é feita antes da restrição do formulário de doador, permitindo que outros perfis leiam seus próprios avisos.

No template, estoque mostra **Ver estoque**, pedido mostra **Ver pedido**; outros avisos com destino mostram **Ver detalhes**. O link usa a URL guardada. Histórico lido não é apagado. Um clique no destino, sozinho, não marca leitura; há botão específico.

Atualmente os geradores implementados são estoque crítico e pedido compatível. Os seis eventos adicionais discutidos — campanha, confirmação de doação, futura aptidão, alteração de pedido, validação de hemocentro e ações administrativas — não ganharam geradores nessa organização. O enum inclui também tipos legado/geral. Não confunda capacidade de guardar um aviso com existência de uma regra que o cria.

## 12. Auditoria e administração

`auditoria.py` centraliza IP, navegador, identificação do alvo, limpeza de metadados e gravação de eventos. Estude `limpar_metadados`: a proteção é baseada nas regras que o código implementa, não uma garantia de que qualquer texto livre jamais conterá dado sensível.

`AuditoriaAcessosMiddleware.process_response` observa resposta e rota. Registra tentativas bloqueadas e consultas sensíveis de rotas/modelos definidos. Isso é cobertura explícita, não monitoramento irrestrito de toda operação no banco.

`signals.py` escuta `user_login_failed`. Uma falha gera registro; repetição na janela configurada gera evento suspeito. O código atual prioriza e-mail quando disponível e usa IP no caminho alternativo. Não implementa bloqueio automático de login por excesso de tentativas. `AccountsConfig.ready` importa o módulo para conectar o sinal.

`admin.py` registra modelos e personaliza `/admin/`. `list_display`, `search_fields`, `list_filter`, `readonly_fields` e `fieldsets` organizam a tela. `has_add_permission`, `has_change_permission`, `has_delete_permission` e `has_view_permission` definem operações permitidas. `save_model` e `save_related` interceptam gravações para auditar alterações pertinentes, incluindo permissões e suspensão.

O histórico de auditoria é protegido contra edição pela interface administrativa, mas isso não constitui imutabilidade no banco. Uma pessoa com acesso direto ao banco ou código privilegiado tem outro nível de acesso. Leia o método de cada classe admin: não presuma as mesmas permissões para todos os modelos.

## 13. Migrations e evolução

Migrations descrevem como chegar de uma estrutura anterior à seguinte. Dependências formam um grafo, não apenas uma lista numérica. Há duas migrations `0007`; `0008_merge_triagem_estoque_branches` une caminhos. Não renumere para parecer uma sequência simples.

`CreateModel`, `AddField`, `AlterField`, `RenameField` e `AddConstraint` alteram o esquema. `RunPython` transforma dados históricos. Nessas funções, `apps.get_model` usa a versão histórica do model, não necessariamente a classe atual.

Leia cada migration na referência, com suas dependências e operações. `0001` inicia contas e consentimentos; as seguintes evoluem documentos, auditoria, validação institucional, triagem, estoque, notificações e pedidos. Algumas removem e outras restauram campos: o model atual é o resultado da evolução, não a cópia da primeira migration.

`makemigrations` gera arquivos ao detectar mudanças dos models; `migrate` aplica arquivos; `showmigrations --plan` informa pendências. Uma mudança apenas na tela ou no serviço normalmente não exige migration. Não edite migration já aplicada para mudar silenciosamente o passado.

## 14. Testes: como entender a intenção de uma regra

Testes são código executável que monta cenário, executa ação e compara resultado. `TestCase` isola dados; `setUp` prepara cada teste; `setUpTestData` prepara dados da classe; `assertEqual`, `assertTrue`, `assertContains` e similares expressam expectativas. `self.client` simula HTTP; `force_login` inicia sessão sem testar senha; um POST de login testa outro caminho.

Um teste que passa comprova aquele cenário, não todos os casos possíveis. Ao estudar, associe cada regra ao seu teste e identifique o que ainda não foi coberto. Na referência estão listados todos os métodos `test_*`, suas chamadas e asserts.

| Arquivo/grupo | Foco |
| --- | --- |
| `tests.py` | Cadastro, autenticação, perfis e regras gerais presentes nas classes do arquivo. |
| `test_estoque.py` | Cálculo, movimentação, validação e permissões de estoque. |
| `test_pedidos.py` | Solicitações, consulta, decisões e publicação. |
| `test_visualizacao.py` | Visualização e consultas públicas de estoque. |
| `test_triagem*.py` | Catálogos, formulários, modelos, serviço, motor e views de triagem, separados por responsabilidade. |
| `test_fluxo_requisitos.py` | Integração de perfis, compatibilidade, consentimento, limites de alertas e central. |
| `test_perfis_teste.py` | Criação repetível de contas fictícias e bloqueio fora de DEBUG. |

Execução local:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test --settings=config.settings_test --noinput
.\.venv\Scripts\python.exe manage.py test accounts.test_estoque --settings=config.settings_test --noinput
```

Os comandos acima são instruções de estudo; a suíte completa não foi reexecutada só para escrever este guia.

## 15. Contas fictícias e comandos

`management/commands/criar_perfis_teste.py` é descoberto pelo Django como `manage.py criar_perfis_teste`. `BaseCommand` fornece a estrutura; `add_arguments` declara `--senha`; `handle` executa. O comando exige `DEBUG=True`, agrupa criação em transação e preserva contas de e-mail já existente.

As contas servem para testar perfil, estado de hemocentro e elegibilidade dos doadores. A conta administrativa fictícia é superusuário; portanto seu acesso amplo não demonstra as permissões mínimas de um administrador sem esse atributo. Triagens e aceites são sintéticos. [TESTAR_PERFIS.md](../../TESTAR_PERFIS.md) oferece o roteiro prático.

## 16. Dados de exemplo, código ativo e documentos antigos

As constantes `POSTOS_COLETA`, `ESTOQUE_GERAL` e `CAMPANHAS_ATIVAS` em `views.py` são listas declaradas no código. Não devem ser confundidas com um módulo completo de cadastro de campanhas ou integração externa. Há fluxos que usam modelos reais e outros que exibem esses exemplos.

O README contém descrições antigas: afirma em trechos que perfis ainda não mudam permissões, enquanto o código já verifica perfis; descreve solicitação pública ampla, enquanto `criar_pedido_pendente` exige Receptor autenticado; cita ausência de CSS, mas `base.html` carrega o CSS atual. Use essas diferenças para aprender a confirmar implementação por chamada, não apenas por comentário.

Documentos em `docs/superpowers` registram planejamento da triagem. São contexto histórico e devem ser comparados à implementação. Um requisito no documento não é automaticamente uma função pronta.

A auditoria não oferece todos os eventos possíveis só porque tem um enum. A central não envia todos os tipos só porque existe uma tabela. A compatibilidade não implica aptidão. Uma página renderizada não prova permissão correta. Esses são exemplos de perguntas úteis na leitura do sistema.
