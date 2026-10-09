# Codigo completo para estudo

Copia numerada em 09/10/2026. Leia a explicacao em [GUIA_ELO.md](GUIA_ELO.md) e o indice em [REFERENCIA_CODIGO.md](REFERENCIA_CODIGO.md). Os numeros antes de `|` sao linhas, nao fazem parte do codigo. Conteudo copiado nao deve ser executado diretamente. Nenhum segredo do .env real foi lido.

## .env.example

Original: [.env.example](<C:/Users/lb119/Elo/.env.example>).

``````text
    1 | # Copie este arquivo para .env e preencha os valores locais.
    2 | # Nunca coloque segredos reais neste arquivo de exemplo.
    3 | 
    4 | DJANGO_SECRET_KEY="COLE_AQUI_A_CHAVE_GERADA"
    5 | DJANGO_DEBUG=True
    6 | 
    7 | DB_NAME=elo_db
    8 | DB_USER=elo_user
    9 | DB_PASSWORD="SENHA_CRIADA_NO_POSTGRESQL"
   10 | DB_HOST=127.0.0.1
   11 | DB_PORT=5432
``````

## .gitignore

Original: [.gitignore](<C:/Users/lb119/Elo/.gitignore>).

``````text
    1 | # Ambiente virtual: contem pacotes instalados localmente e pode ser recriado.
    2 | .venv/
    3 | 
    4 | # Segredos locais, incluindo chave Django e senha do PostgreSQL.
    5 | .env
    6 | 
    7 | # Cache de bytecode gerado automaticamente pelo Python.
    8 | __pycache__/
    9 | *.pyc
   10 | 
   11 | # Banco SQLite padrao; este projeto usa PostgreSQL.
   12 | db.sqlite3
``````

## README.md

Original: [README.md](<C:/Users/lb119/Elo/README.md>).

``````text
    1 | # Elo
    2 | 
    3 | Sistema web desenvolvido para otimizar a captação de doadores e o controle de demandas hematológicas.
    4 | 
    5 | Repositório: <https://github.com/alinefxz/Elo.git>
    6 | 
    7 | ## Estado atual do projeto
    8 | 
    9 | O fluxo de cadastro, autenticação, triagem orientativa e solicitações de
   10 | divulgação de pedidos está implementado. Já estão disponíveis:
   11 | 
   12 | - projeto Django conectado ao PostgreSQL;
   13 | - acesso publico do Visitante para busca de postos, estoque geral e pedidos;
   14 | - cadastro de usuários;
   15 | - escolha entre Doador, Receptor/Solicitante, Hemocentro e Observador;
   16 | - dados iniciais de identificação e localização do usuário;
   17 | - login por e-mail e senha;
   18 | - logout seguro por requisição POST;
   19 | - usuário-base personalizado do Django;
   20 | - registro do consentimento LGPD no cadastro;
   21 | - painel protegido com conteudo particularizado por perfil;
   22 | - aprovação administrativa de Hemocentros;
   23 | - triagem extensa e simplificada com salvamento, retomada, revisão, resultado e histórico;
   24 | - formulário público de solicitação de divulgação de necessidade;
   25 | - análise, correção, recusa e publicação oficial pelo Hemocentro aprovado;
   26 | - filtros e ordenação de pedidos publicados;
   27 | - notificações de pedidos somente para doadores compatíveis, aptos e optantes;
   28 | - painel administrativo do Django;
   29 | - migrations versionadas do app `accounts`;
   30 | - testes básicos de cadastro, senha e login;
   31 | - templates HTML básicos, sem CSS ou Bootstrap.
   32 | 
   33 | As senhas não são armazenadas como texto comum. O Django gera e salva um hash seguro na coluna `senha_hash`.
   34 | 
   35 | O Visitante não possui conta e pode consultar informações públicas e enviar uma
   36 | solicitação de divulgação. Doador, Receptor e Observador também podem enviar
   37 | solicitações, mas nenhum deles publica pedidos. A publicação só ocorre após a
   38 | análise do Hemocentro aprovado de destino.
   39 | 
   40 | ## Tecnologias utilizadas
   41 | 
   42 | - Python 3.14.3;
   43 | - Django 5.2.17;
   44 | - PostgreSQL;
   45 | - psycopg 3.3.4;
   46 | - python-dotenv 1.2.2;
   47 | - HTML5;
   48 | - Git e GitHub.
   49 | 
   50 | ## Estrutura principal
   51 | 
   52 | ```text
   53 | Elo/
   54 | ├── accounts/
   55 | │   ├── migrations/       # Alterações versionadas do banco
   56 | │   ├── admin.py          # Configuração do painel administrativo
   57 | │   ├── forms.py          # Formulários e validações
   58 | │   ├── models.py         # Usuário-base e consentimento LGPD
   59 | │   ├── tests.py          # Testes automatizados
   60 | │   ├── urls.py           # Rotas de autenticação
   61 | │   └── views.py          # Regras do cadastro e dashboard
   62 | ├── config/
   63 | │   ├── settings.py       # Configurações do Django e PostgreSQL
   64 | │   └── urls.py           # Rotas gerais do projeto
   65 | ├── templates/
   66 | │   ├── base.html
   67 | │   └── accounts/
   68 | │       ├── cadastro.html
   69 | │       ├── dashboard.html
   70 | │       └── login.html
   71 | ├── .env.example          # Modelo das variáveis privadas
   72 | ├── .gitignore
   73 | ├── manage.py
   74 | └── requirements.txt
   75 | ```
   76 | 
   77 | ## Endereços disponíveis
   78 | 
   79 | Com o servidor executando:
   80 | 
   81 | - página inicial publica do Visitante: <http://127.0.0.1:8000/>;
   82 | - cadastro: <http://127.0.0.1:8000/cadastro/>;
   83 | - login: <http://127.0.0.1:8000/login/>;
   84 | - painel do usuário: <http://127.0.0.1:8000/dashboard/>;
   85 | - administração: <http://127.0.0.1:8000/admin/>.
   86 | 
   87 | A página inicial fica publica. O dashboard exige autenticação.
   88 | 
   89 | ## Como instalar em outro computador
   90 | 
   91 | ### 1. Instalar os programas necessários
   92 | 
   93 | Instale:
   94 | 
   95 | 1. Git;
   96 | 2. Python 3.14 ou versão compatível com Django 6.1;
   97 | 3. PostgreSQL e pgAdmin;
   98 | 4. VS Code, opcional, mas recomendado.
   99 | 
  100 | Confirme as instalações no terminal:
  101 | 
  102 | ```powershell
  103 | git --version
  104 | python --version
  105 | ```
  106 | 
  107 | ### 2. Obter acesso ao GitHub
  108 | 
  109 | Se o repositório for privado, a pessoa precisa:
  110 | 
  111 | 1. ter uma conta no GitHub;
  112 | 2. receber acesso como colaboradora do repositório;
  113 | 3. aceitar o convite enviado pelo GitHub;
  114 | 4. autenticar o Git no computador dela.
  115 | 
  116 | Depois, abra o PowerShell na pasta em que deseja guardar o projeto e execute:
  117 | 
  118 | ```powershell
  119 | git clone https://github.com/alinefxz/Elo.git
  120 | cd Elo
  121 | ```
  122 | 
  123 | Se o Git solicitar autenticação, use a janela do Git Credential Manager ou faça login pelo navegador. A senha comum da conta GitHub não deve ser usada como senha do Git.
  124 | 
  125 | ### 3. Criar o ambiente virtual
  126 | 
  127 | Dentro da pasta clonada:
  128 | 
  129 | ```powershell
  130 | python -m venv .venv
  131 | .\.venv\Scripts\Activate.ps1
  132 | ```
  133 | 
  134 | Quando o ambiente estiver ativo, o terminal mostrará `(.venv)` no início da linha.
  135 | 
  136 | Se o PowerShell bloquear a ativação, execute temporariamente:
  137 | 
  138 | ```powershell
  139 | Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  140 | .\.venv\Scripts\Activate.ps1
  141 | ```
  142 | 
  143 | No Prompt de Comando (`cmd`), a ativação é:
  144 | 
  145 | ```bat
  146 | .venv\Scripts\activate.bat
  147 | ```
  148 | 
  149 | ### 4. Instalar as dependências
  150 | 
  151 | ```powershell
  152 | python -m pip install --upgrade pip
  153 | python -m pip install -r requirements.txt
  154 | ```
  155 | 
  156 | ### 5. Criar o usuário e o banco PostgreSQL
  157 | 
  158 | Abra o pgAdmin e conecte ao servidor PostgreSQL com o usuário administrador `postgres`.
  159 | 
  160 | Crie um usuário para a aplicação:
  161 | 
  162 | 1. expanda `Login/Group Roles`;
  163 | 2. escolha `Create` > `Login/Group Role`;
  164 | 3. nome: `elo_user`;
  165 | 4. defina uma senha própria para aquele computador;
  166 | 5. em privilégios, habilite `Can login`;
  167 | 6. salve.
  168 | 
  169 | Crie o banco:
  170 | 
  171 | 1. clique com o botão direito em `Databases`;
  172 | 2. escolha `Create` > `Database`;
  173 | 3. nome: `elo_db`;
  174 | 4. proprietário: `elo_user`;
  175 | 5. codificação: `UTF8`;
  176 | 6. salve.
  177 | 
  178 | Não é necessário criar as tabelas manualmente. O Django fará isso pelas migrations.
  179 | 
  180 | ### 6. Criar o arquivo `.env`
  181 | 
  182 | Na raiz do projeto, no mesmo nível de `manage.py`, copie `.env.example` e renomeie a cópia para `.env`.
  183 | 
  184 | Gere uma chave secreta:
  185 | 
  186 | ```powershell
  187 | python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  188 | ```
  189 | 
  190 | Preencha o `.env`:
  191 | 
  192 | ```env
  193 | DJANGO_SECRET_KEY="COLE_AQUI_A_CHAVE_GERADA"
  194 | DJANGO_DEBUG=True
  195 | 
  196 | DB_NAME=elo_db
  197 | DB_USER=elo_user
  198 | DB_PASSWORD="SENHA_CRIADA_NO_POSTGRESQL"
  199 | DB_HOST=127.0.0.1
  200 | DB_PORT=5432
  201 | ```
  202 | 
  203 | O `.env` contém dados privados e está no `.gitignore`. Nunca envie esse arquivo ao GitHub ou compartilhe a senha do banco.
  204 | 
  205 | ### 7. Preparar as tabelas
  206 | 
  207 | Execute:
  208 | 
  209 | ```powershell
  210 | python manage.py check
  211 | python manage.py migrate
  212 | ```
  213 | 
  214 | Em um clone novo não é necessário executar `makemigrations`, porque as migrations numeradas do app `accounts` já fazem parte do repositório. Use `makemigrations` somente depois de alterar os modelos.
  215 | 
  216 | ### 8. Criar um administrador
  217 | 
  218 | ```powershell
  219 | python manage.py createsuperuser
  220 | ```
  221 | 
  222 | Informe nome, e-mail e senha. Esse usuário poderá acessar `/admin/`.
  223 | 
  224 | ### 9. Executar o sistema
  225 | 
  226 | ```powershell
  227 | python manage.py runserver
  228 | ```
  229 | 
  230 | Abra <http://127.0.0.1:8000/>. Para encerrar o servidor, pressione `Ctrl + C`.
  231 | 
  232 | Se a porta 8000 estiver ocupada:
  233 | 
  234 | ```powershell
  235 | python manage.py runserver 8001
  236 | ```
  237 | 
  238 | Nesse caso, acesse <http://127.0.0.1:8001/>.
  239 | 
  240 | ## Como trabalhar no projeto diariamente
  241 | 
  242 | Abra a pasta clonada e ative o ambiente:
  243 | 
  244 | ```powershell
  245 | cd CAMINHO\PARA\Elo
  246 | .\.venv\Scripts\Activate.ps1
  247 | git pull origin main
  248 | python manage.py runserver
  249 | ```
  250 | 
  251 | Antes de começar uma funcionalidade, recomenda-se criar uma branch:
  252 | 
  253 | ```powershell
  254 | git switch -c feature/nome-da-funcionalidade
  255 | ```
  256 | 
  257 | Depois das alterações:
  258 | 
  259 | ```powershell
  260 | git status
  261 | git add .
  262 | git commit -m "feat: descreva a alteracao"
  263 | git push -u origin feature/nome-da-funcionalidade
  264 | ```
  265 | 
  266 | Depois, abra um Pull Request no GitHub para revisar e unir a branch à `main`.
  267 | 
  268 | Para alterações pequenas feitas diretamente na `main`:
  269 | 
  270 | ```powershell
  271 | git pull origin main
  272 | git add .
  273 | git commit -m "descricao clara da alteracao"
  274 | git push origin main
  275 | ```
  276 | 
  277 | Sempre execute `git pull` antes de começar e evite editar o mesmo arquivo ao mesmo tempo que outra pessoa.
  278 | 
  279 | ## Alterações no banco de dados
  280 | 
  281 | Quando alguém alterar `accounts/models.py` ou criar novos modelos:
  282 | 
  283 | ```powershell
  284 | python manage.py makemigrations
  285 | python manage.py migrate
  286 | ```
  287 | 
  288 | O arquivo de migration gerado deve ser enviado ao GitHub junto com o código:
  289 | 
  290 | ```powershell
  291 | git add .
  292 | git commit -m "feat: atualiza estrutura do banco"
  293 | git push
  294 | ```
  295 | 
  296 | Não edite arquivos de migration já aplicados. Para novas mudanças, gere uma migration nova.
  297 | 
  298 | ## Testes e verificações
  299 | 
  300 | Antes de enviar alterações:
  301 | 
  302 | ```powershell
  303 | python manage.py check
  304 | python manage.py test
  305 | ```
  306 | 
  307 | O Django cria um banco temporário durante os testes. Se aparecer `permission denied to create database`, o administrador local do PostgreSQL pode conceder permissão de criação de banco ao usuário de desenvolvimento:
  308 | 
  309 | ```sql
  310 | ALTER ROLE elo_user CREATEDB;
  311 | ```
  312 | 
  313 | Essa permissão é apropriada apenas para desenvolvimento local, não para um servidor de produção.
  314 | 
  315 | ## Funcionamento do usuário, cadastro e login
  316 | 
  317 | - `accounts/models.py` define `Usuario` e `ConsentimentoLGPD`;
  318 | - o e-mail é o identificador usado no login;
  319 | - `accounts/forms.py` contém o formulário de cadastro e suas validações;
  320 | - o cadastro público permite escolher Doador, Receptor, Hemocentro ou Observador;
  321 | - Hemocentro informa CNPJ; os outros perfis informam CPF;
  322 | - CPF e CNPJ são salvos somente com números;
  323 | - a sigla do estado é salva em letras maiúsculas;
  324 | - a senha precisa ter pelo menos oito caracteres, letras e números;
  325 | - `set_password()` transforma a senha em hash antes de salvar;
  326 | - `accounts/views.py` grava usuário e consentimento na mesma transação;
  327 | - após o cadastro, o usuário entra automaticamente;
  328 | - `login_required` bloqueia o dashboard para visitantes;
  329 | - o logout usa `POST` e proteção CSRF;
  330 | - as sessões são administradas pelo próprio Django.
  331 | 
  332 | O objetivo desta entrega termina no cadastro e na autenticação da conta-base. A classificação inicial já existe no model e no formulário, mas ainda não altera permissões nem mostra painéis diferentes. A próxima pessoa deverá implementar, para cada tipo de usuário:
  333 | 
  334 | - campos adicionais necessários;
  335 | - permissões e restrições de acesso;
  336 | - formulários específicos;
  337 | - páginas e painéis próprios;
  338 | - validações e regras de negócio;
  339 | - relacionamento com tabelas como doadores e hemocentros.
  340 | 
  341 | ## Tabelas principais
  342 | 
  343 | - `usuarios`: dados da conta, documento, localização e perfil inicial;
  344 | - `consentimentos_lgpd`: aceite, versão do termo, data e IP;
  345 | - `django_session`: sessões de usuários autenticados;
  346 | - tabelas internas do Django: permissões, grupos, migrations e administração.
  347 | 
  348 | ## Arquivos que nunca devem ir ao GitHub
  349 | 
  350 | O `.gitignore` deve continuar ignorando:
  351 | 
  352 | ```gitignore
  353 | .venv/
  354 | .env
  355 | __pycache__/
  356 | *.pyc
  357 | db.sqlite3
  358 | ```
  359 | 
  360 | Nunca envie senhas, chaves secretas ou o conteúdo real do `.env`.
  361 | 
  362 | ## Problemas comuns
  363 | 
  364 | ### `KeyError: DJANGO_SECRET_KEY`
  365 | 
  366 | O `.env` não existe, está no local errado ou a primeira linha está inválida. Ele deve ficar ao lado de `manage.py`.
  367 | 
  368 | ### `password authentication failed for user elo_user`
  369 | 
  370 | A senha em `DB_PASSWORD` não corresponde à senha criada no PostgreSQL.
  371 | 
  372 | ### `connection refused`
  373 | 
  374 | O serviço PostgreSQL pode estar desligado ou usando outra porta. Confirme `DB_HOST` e `DB_PORT`.
  375 | 
  376 | ### `database elo_db does not exist`
  377 | 
  378 | Crie o banco `elo_db` pelo pgAdmin e defina `elo_user` como proprietário.
  379 | 
  380 | ### `relation does not exist`
  381 | 
  382 | Execute:
  383 | 
  384 | ```powershell
  385 | python manage.py migrate
  386 | ```
  387 | 
  388 | ### Erro ao ativar o ambiente virtual
  389 | 
  390 | Confirme que está na raiz do projeto e execute:
  391 | 
  392 | ```powershell
  393 | Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  394 | .\.venv\Scripts\Activate.ps1
  395 | ```
  396 | 
  397 | ## O que ainda não foi implementado
  398 | 
  399 | Esta é uma primeira entrega. Permanecem para etapas futuras:
  400 | 
  401 | - identidade visual e CSS;
  402 | - recuperação de senha;
  403 | - confirmação de e-mail;
  404 | - bloqueio após tentativas excessivas de login;
  405 | - edição e páginas específicas de cada perfil;
  406 | - mapas e localização;
  407 | - Supabase e recursos em tempo real;
  408 | - Gemini API;
  409 | - PWA.
  410 | 
  411 | Antes de iniciar uma dessas funcionalidades, crie uma branch e documente quaisquer novas variáveis no `.env.example`.
  412 | 
  413 | ## Situação verificada em 14/08/2026
  414 | 
  415 | - repositório local conectado a `https://github.com/alinefxz/Elo.git`;
  416 | - branch principal: `main`;
  417 | - migrations do app `accounts` aplicadas;
  418 | - `python manage.py check` executado sem erros;
  419 | - banco local: `elo_db`;
  420 | - usuário local do banco: `elo_user`.
``````

## TESTAR_PERFIS.md

Original: [TESTAR_PERFIS.md](<C:/Users/lb119/Elo/TESTAR_PERFIS.md>).

``````text
    1 | # Testar os perfis do Elo
    2 | 
    3 | No ambiente local com `DEBUG=True`, execute:
    4 | 
    5 | ```powershell
    6 | .\.venv\Scripts\python.exe manage.py criar_perfis_teste
    7 | ```
    8 | 
    9 | As novas contas usam a senha **EloTeste2026!**. Para escolher outra senha, use
   10 | `--senha 'SuaSenhaDeTeste'`. Repetir o comando preserva todas as contas existentes,
   11 | inclusive suas senhas, triagens, consentimentos e alteracoes feitas durante os testes.
   12 | O comando nao altera regras, nao cria estoque ou pedidos e nao envia notificacoes.
   13 | Nao exige uma nova migration; as migrations existentes devem estar aplicadas.
   14 | 
   15 | Abra o sistema no endereco do seu servidor local e entre com uma conta por vez.
   16 | Para testar dois perfis ao mesmo tempo, use navegadores diferentes ou janela anonima.
   17 | 
   18 | | Login | Situacao inicial e o que verificar |
   19 | | --- | --- |
   20 | | `doador@teste.elo.test` | O−, triagem apta e convocacao autorizada. Testar triagem e alertas compativeis. |
   21 | | `doador-inapto@teste.elo.test` | O−, ultima triagem inapta. Nao deve receber convocacoes. |
   22 | | `doador-sem-consentimento@teste.elo.test` | O−, apto, sem aceite de convocacao. Nao recebe alertas ate autorizar no painel. |
   23 | | `receptor@teste.elo.test` | Criar solicitacao e acompanhar seus pedidos. |
   24 | | `observador@teste.elo.test` | Consultar informacoes; verificar bloqueio das funcoes restritas. |
   25 | | `administrador@teste.elo.test` | Validar hemocentros, moderar pedidos e consultar auditoria em `/admin/`. Conta tecnica com permissoes completas somente para testes locais. |
   26 | | `hemocentro-pendente@teste.elo.test` | Aguardar analise; publicacao bloqueada. Use esta conta para testar aprovacao pelo administrador. |
   27 | | `hemocentro-aprovado@teste.elo.test` | Cadastrar e atualizar estoque; analisar pedidos destinados a ele. |
   28 | | `hemocentro-recusado@teste.elo.test` | Conferir mensagem de recusa e bloqueio de publicacao. |
   29 | | `hemocentro-correcao@teste.elo.test` | Conferir estado de correcao e bloqueio de publicacao. |
   30 | 
   31 | As triagens e consentimentos dessas contas sao dados sinteticos para testes,
   32 | nao avaliacoes ou aceites de pessoas reais. Os estados dos hemocentros sao definidos
   33 | diretamente pelo comando; o historico de validacao sera produzido ao executar as acoes reais.
   34 | 
   35 | ## Roteiro de alerta e notificacoes
   36 | 
   37 | 1. Entre como hemocentro aprovado. Cadastre estoque O− com minimo 10,
   38 |    critico 5 e quantidade inicial 12.
   39 | 2. Atualize a quantidade para 7: o estoque fica baixo, sem novo alerta.
   40 | 3. Atualize para 5: o estoque fica critico e deve notificar o doador apto autorizado.
   41 | 4. Entre com os tres doadores: apenas `doador@teste.elo.test` deve receber esse alerta.
   42 | 5. Na central, confira data, titulo, mensagem e **Ver estoque**. Clique em
   43 |    **Marcar como lida**; o aviso continua no historico como lido.
   44 | 6. Teste um pedido O−: Receptor solicita, Hemocentro responsavel publica.
   45 |    A convocacao compartilha com o estoque o limite configurado (padrao: uma em 24 horas),
   46 |    inclusive quando o alerta anterior foi lido. Nao espere outro aviso dentro desse limite.
   47 | 
   48 | Visitante e testado sem login. Nenhuma conta e necessaria.
``````

## accounts/__init__.py

Original: [accounts/__init__.py](<C:/Users/lb119/Elo/accounts/__init__.py>).

``````text
    1 | """
    2 | Marca a pasta ``accounts`` como um pacote Python.
    3 | 
    4 | O arquivo pode permanecer sem codigo executavel. Sua existencia permite
    5 | imports como ``from accounts.models import Usuario``.
    6 | """
``````

## accounts/admin.py

Original: [accounts/admin.py](<C:/Users/lb119/Elo/accounts/admin.py>).

``````text
    1 | """
    2 | RESUMO DO ARQUIVO
    3 | =================
    4 | 
    5 | Configura como Usuario, ConsentimentoLGPD e auditorias aparecem no /admin/.
    6 | 
    7 | O admin e uma ferramenta interna para pessoas autorizadas. Ele nao substitui
    8 | as telas normais do sistema. Os formularios abaixo garantem que uma senha
    9 | criada no painel tambem seja transformada em hash.
   10 | """
   11 | 
   12 | from django.contrib import admin, messages
   13 | from django.contrib.auth.admin import UserAdmin
   14 | from django.contrib.auth.forms import UserChangeForm, UserCreationForm
   15 | 
   16 | from .auditoria import campos_sensiveis_alterados, registrar_auditoria
   17 | from .models import (
   18 |     Usuario,
   19 |     ValidacaoHemocentro,
   20 |     ConsentimentoLGPD,
   21 |     AuditoriaAcaoCritica,
   22 |     Triagem,
   23 |     RespostaTriagem,
   24 |     Estoque,
   25 |     EstoqueMovimentacao,
   26 |     Notificacao,
   27 |     PedidoSangue,
   28 |     ValidacaoPedido,
   29 | )
   30 | 
   31 | from .validacao_hemocentro import (
   32 |     aprovar_hemocentro,
   33 |     recusar_hemocentro,
   34 |     solicitar_correcao_hemocentro,
   35 | )
   36 | 
   37 | 
   38 | class UsuarioAdminCreationForm(UserCreationForm):
   39 |     """Formulario usado quando o admin cria uma conta."""
   40 | 
   41 |     class Meta:
   42 |         model = Usuario
   43 | 
   44 |         # Estes sao os dados minimos pedidos na tela de criacao do admin.
   45 |         # Os outros dados podem ser completados depois na tela de edicao.
   46 |         fields = ("email", "nome", "perfil")
   47 | 
   48 | 
   49 | class UsuarioAdminChangeForm(UserChangeForm):
   50 |     """Formulario usado quando o admin edita uma conta existente."""
   51 | 
   52 |     class Meta:
   53 |         model = Usuario
   54 |         fields = "__all__"
   55 | 
   56 | 
   57 | @admin.register(Usuario)
   58 | class UsuarioAdmin(UserAdmin):
   59 |     """Define listagem, busca e organizacao dos campos de Usuario."""
   60 | 
   61 |     # UserAdmin foi criado pensando no usuario padrao. Estas atribuicoes dizem
   62 |     # a ele para usar os formularios e o model personalizados do Elo.
   63 |     add_form = UsuarioAdminCreationForm
   64 |     form = UsuarioAdminChangeForm
   65 |     model = Usuario
   66 | 
   67 |     # Colunas exibidas na lista principal de usuarios.
   68 |     list_display = (
   69 |         "email",
   70 |         "nome",
   71 |         "perfil",
   72 |         "tipo_sanguineo",
   73 |         "status_validacao",
   74 |         "is_active",
   75 |         "suspensa",
   76 |         "email_verificado",
   77 |         "is_staff",
   78 |     )
   79 | 
   80 |     # Filtros laterais e campos pesquisaveis no painel.
   81 |     list_filter = (
   82 |         "perfil",
   83 |         "tipo_sanguineo",
   84 |         "status_validacao",
   85 |         "is_active",
   86 |         "suspensa",
   87 |         "email_verificado",
   88 |         "is_staff",
   89 |     )
   90 | 
   91 |     search_fields = ("email", "nome", "cpf", "cnpj")
   92 |     ordering = ("nome",)
   93 | 
   94 |     actions = (
   95 |         "aprovar_hemocentros_selecionados",
   96 |         "recusar_hemocentros_selecionados",
   97 |         "solicitar_correcao_hemocentros_selecionados",
   98 |     )
   99 | 
  100 |     # Datas automaticas devem ser visualizadas, nao digitadas manualmente.
  101 |     readonly_fields = (
  102 |         "status_validacao",
  103 |         "last_login",
  104 |         "date_joined",
  105 |         "atualizado_em",
  106 |     )
  107 | 
  108 |     # fieldsets organiza a tela de EDICAO de uma conta existente.
  109 |     fieldsets = (
  110 |         (
  111 |             None,
  112 |             {
  113 |                 "fields": (
  114 |                     "email",
  115 |                     "password",
  116 |                 )
  117 |             },
  118 |         ),
  119 |         (
  120 |             "Dados da conta",
  121 |             {
  122 |                 "fields": (
  123 |                     "nome",
  124 |                     "perfil",
  125 |                     "cpf",
  126 |                     "cnpj",
  127 |                     "telefone",
  128 |                     "data_nascimento",
  129 |                     "sexo",
  130 |                     "tipo_sanguineo",
  131 |                     "tipo_sanguineo_confirmado",
  132 |                     "cidade",
  133 |                     "estado",
  134 |                     "status_validacao",
  135 |                     "email_verificado",
  136 |                 )
  137 |             },
  138 |         ),
  139 |         (
  140 |             "Permissoes internas do Django",
  141 |             {
  142 |                 "fields": (
  143 |                     "is_active",
  144 |                     "suspensa",
  145 |                     "is_staff",
  146 |                     "is_superuser",
  147 |                     "groups",
  148 |                     "user_permissions",
  149 |                 )
  150 |             },
  151 |         ),
  152 |         (
  153 |             "Datas",
  154 |             {
  155 |                 "fields": (
  156 |                     "last_login",
  157 |                     "date_joined",
  158 |                     "atualizado_em",
  159 |                 )
  160 |             },
  161 |         ),
  162 |     )
  163 | 
  164 |     # add_fieldsets organiza a tela de CRIACAO de uma conta no admin.
  165 |     add_fieldsets = (
  166 |         (
  167 |             None,
  168 |             {
  169 |                 "classes": ("wide",),
  170 |                 "fields": (
  171 |                     "email",
  172 |                     "nome",
  173 |                     "perfil",
  174 |                     "password1",
  175 |                     "password2",
  176 |                     "is_active",
  177 |                     "suspensa",
  178 |                     "is_staff",
  179 |                 ),
  180 |             },
  181 |         ),
  182 |     )
  183 | 
  184 |     def save_model(self, request, obj, form, change):
  185 |         """Audita mudancas administrativas em perfil e permissoes."""
  186 | 
  187 |         campos_auditados = [
  188 |             "perfil",
  189 |             "is_active",
  190 |             "is_staff",
  191 |             "is_superuser",
  192 |             "email_verificado",
  193 |             "suspensa",
  194 |             "nome",
  195 |             "email",
  196 |             "cpf",
  197 |             "cnpj",
  198 |             "cidade",
  199 |             "estado",
  200 |             "data_nascimento",
  201 |             "tipo_sanguineo",
  202 |         ]
  203 | 
  204 |         alteracoes = (
  205 |             campos_sensiveis_alterados(obj, campos_auditados)
  206 |             if change
  207 |             else {}
  208 |         )
  209 | 
  210 |         super().save_model(request, obj, form, change)
  211 | 
  212 |         if alteracoes:
  213 |             # Alteracoes cadastrais guardam apenas nomes de campos, sem
  214 |             # duplicar CPF, nascimento ou outros dados pessoais na auditoria.
  215 |             permissoes = {campo: valor for campo, valor in alteracoes.items()
  216 |                           if campo in {"perfil", "is_active", "is_staff", "is_superuser", "email_verificado", "suspensa"}}
  217 |             suspensao = (
  218 |                 "is_active" in permissoes and not obj.is_active
  219 |             ) or ("suspensa" in permissoes and obj.suspensa)
  220 |             registrar_auditoria(
  221 |                 acao=(AuditoriaAcaoCritica.Acao.ALTERACAO_PERMISSAO if permissoes
  222 |                       else AuditoriaAcaoCritica.Acao.MODERACAO),
  223 |                 usuario=request.user,
  224 |                 alvo=obj,
  225 |                 descricao="Desativacao administrativa de usuario." if suspensao
  226 |                 else "Alteracao administrativa de usuario.",
  227 |                 request=request,
  228 |                 metadados={"evento": "SUSPENSAO_USUARIO" if suspensao else "ALTERACAO_ADMINISTRATIVA",
  229 |                            "alteracoes": permissoes, "campos_alterados": sorted(alteracoes)},
  230 |             )
  231 |         elif not change:
  232 |             registrar_auditoria(
  233 |                 acao=AuditoriaAcaoCritica.Acao.MODERACAO,
  234 |                 usuario=request.user, alvo=obj, request=request,
  235 |                 descricao="Criacao administrativa de usuario.",
  236 |                 metadados={"evento": "ALTERACAO_ADMINISTRATIVA", "operacao": "CRIACAO_USUARIO"},
  237 |             )
  238 | 
  239 |     def _executar_acao_validacao(
  240 |         self,
  241 |         request,
  242 |         queryset,
  243 |         funcao,
  244 |         parecer,
  245 |     ):
  246 |         """Aplica uma decisao de validacao aos Hemocentros selecionados."""
  247 | 
  248 |         hemocentros = queryset.filter(
  249 |             perfil=Usuario.Perfil.HEMOCENTRO
  250 |         )
  251 | 
  252 |         ignorados = queryset.exclude(
  253 |             perfil=Usuario.Perfil.HEMOCENTRO
  254 |         ).count()
  255 | 
  256 |         total = 0
  257 | 
  258 |         for hemocentro in hemocentros:
  259 |             funcao(
  260 |                 hemocentro=hemocentro,
  261 |                 admin=request.user,
  262 |                 parecer=parecer,
  263 |                 request=request,
  264 |             )
  265 |             total += 1
  266 | 
  267 |         if total:
  268 |             self.message_user(
  269 |                 request,
  270 |                 f"{total} Hemocentro(s) atualizado(s) com sucesso.",
  271 |                 level=messages.SUCCESS,
  272 |             )
  273 | 
  274 |         if ignorados:
  275 |             self.message_user(
  276 |                 request,
  277 |                 f"{ignorados} usuario(s) ignorado(s) por nao serem Hemocentros.",
  278 |                 level=messages.WARNING,
  279 |             )
  280 | 
  281 |     @admin.action(description="Aprovar Hemocentros selecionados")
  282 |     def aprovar_hemocentros_selecionados(self, request, queryset):
  283 |         """Acao em lote que aprova Hemocentros e registra historico."""
  284 | 
  285 |         self._executar_acao_validacao(
  286 |             request,
  287 |             queryset,
  288 |             aprovar_hemocentro,
  289 |             "Hemocentro aprovado pelo painel administrativo.",
  290 |         )
  291 | 
  292 |     @admin.action(description="Recusar Hemocentros selecionados")
  293 |     def recusar_hemocentros_selecionados(self, request, queryset):
  294 |         """Acao em lote que recusa Hemocentros e registra historico."""
  295 | 
  296 |         self._executar_acao_validacao(
  297 |             request,
  298 |             queryset,
  299 |             recusar_hemocentro,
  300 |             "Hemocentro recusado pelo painel administrativo.",
  301 |         )
  302 | 
  303 |     @admin.action(
  304 |         description="Solicitar correcao dos Hemocentros selecionados"
  305 |     )
  306 |     def solicitar_correcao_hemocentros_selecionados(
  307 |         self,
  308 |         request,
  309 |         queryset,
  310 |     ):
  311 |         """Acao em lote que solicita correcao cadastral e registra historico."""
  312 | 
  313 |         self._executar_acao_validacao(
  314 |             request,
  315 |             queryset,
  316 |             solicitar_correcao_hemocentro,
  317 |             "Correcao cadastral solicitada pelo painel administrativo.",
  318 |         )
  319 | 
  320 |     def save_related(self, request, form, formsets, change):
  321 |         """Audita mudancas em grupos e permissoes diretas do usuario."""
  322 | 
  323 |         obj = form.instance
  324 | 
  325 |         grupos_antes = set()
  326 |         permissoes_antes = set()
  327 | 
  328 |         if change and obj.pk:
  329 |             usuario_atual = Usuario.objects.get(pk=obj.pk)
  330 | 
  331 |             grupos_antes = set(
  332 |                 usuario_atual.groups.values_list(
  333 |                     "name",
  334 |                     flat=True,
  335 |                 )
  336 |             )
  337 | 
  338 |             permissoes_antes = set(
  339 |                 usuario_atual.user_permissions.values_list(
  340 |                     "codename",
  341 |                     flat=True,
  342 |                 )
  343 |             )
  344 | 
  345 |         super().save_related(
  346 |             request,
  347 |             form,
  348 |             formsets,
  349 |             change,
  350 |         )
  351 | 
  352 |         if not change:
  353 |             return
  354 | 
  355 |         grupos_depois = set(
  356 |             obj.groups.values_list(
  357 |                 "name",
  358 |                 flat=True,
  359 |             )
  360 |         )
  361 | 
  362 |         permissoes_depois = set(
  363 |             obj.user_permissions.values_list(
  364 |                 "codename",
  365 |                 flat=True,
  366 |             )
  367 |         )
  368 | 
  369 |         alteracoes = {}
  370 | 
  371 |         if grupos_antes != grupos_depois:
  372 |             alteracoes["groups"] = {
  373 |                 "antes": sorted(grupos_antes),
  374 |                 "depois": sorted(grupos_depois),
  375 |             }
  376 | 
  377 |         if permissoes_antes != permissoes_depois:
  378 |             alteracoes["user_permissions"] = {
  379 |                 "antes": sorted(permissoes_antes),
  380 |                 "depois": sorted(permissoes_depois),
  381 |             }
  382 | 
  383 |         if alteracoes:
  384 |             registrar_auditoria(
  385 |                 acao=AuditoriaAcaoCritica.Acao.ALTERACAO_PERMISSAO,
  386 |                 usuario=request.user,
  387 |                 alvo=obj,
  388 |                 descricao="Alteracao administrativa de grupos ou permissoes.",
  389 |                 request=request,
  390 |                 metadados={"evento": "ALTERACAO_PERMISSAO", "alteracoes": alteracoes},
  391 |             )
  392 | 
  393 | 
  394 | @admin.register(ValidacaoHemocentro)
  395 | class ValidacaoHemocentroAdmin(admin.ModelAdmin):
  396 |     """Consulta somente leitura do historico institucional de Hemocentros."""
  397 | 
  398 |     list_display = (
  399 |         "data_analise",
  400 |         "hemocentro",
  401 |         "status",
  402 |         "admin",
  403 |         "parecer_resumido",
  404 |     )
  405 | 
  406 |     list_filter = (
  407 |         "status",
  408 |         "data_analise",
  409 |     )
  410 | 
  411 |     search_fields = (
  412 |         "hemocentro__email",
  413 |         "hemocentro__nome",
  414 |         "hemocentro__cnpj",
  415 |         "admin__email",
  416 |         "admin__nome",
  417 |         "parecer",
  418 |     )
  419 | 
  420 |     readonly_fields = (
  421 |         "id_validacao",
  422 |         "hemocentro",
  423 |         "admin",
  424 |         "status",
  425 |         "parecer",
  426 |         "data_analise",
  427 |     )
  428 | 
  429 |     date_hierarchy = "data_analise"
  430 |     ordering = ("-data_analise",)
  431 | 
  432 |     def parecer_resumido(self, obj):
  433 |         """Mostra um trecho curto do parecer na listagem."""
  434 | 
  435 |         if len(obj.parecer) <= 80:
  436 |             return obj.parecer
  437 | 
  438 |         return f"{obj.parecer[:77]}..."
  439 | 
  440 |     parecer_resumido.short_description = "Parecer"
  441 | 
  442 |     def has_add_permission(self, request):
  443 |         return False
  444 | 
  445 |     def has_change_permission(self, request, obj=None):
  446 |         return False
  447 | 
  448 |     def has_delete_permission(self, request, obj=None):
  449 |         return False
  450 | 
  451 | 
  452 | @admin.register(ConsentimentoLGPD)
  453 | class ConsentimentoLGPDAdmin(admin.ModelAdmin):
  454 |     """Permite consultar os aceites LGPD no painel administrativo."""
  455 | 
  456 |     def save_model(self, request, obj, form, change):
  457 |         super().save_model(request, obj, form, change)
  458 |         registrar_auditoria(
  459 |             acao=AuditoriaAcaoCritica.Acao.MODERACAO,
  460 |             usuario=request.user, alvo=obj, request=request,
  461 |             descricao="Alteracao administrativa de consentimento." if change
  462 |             else "Criacao administrativa de consentimento.",
  463 |             metadados={"evento": "ALTERACAO_ADMINISTRATIVA",
  464 |                        "campos_alterados": list(form.changed_data)},
  465 |         )
  466 | 
  467 |     list_display = (
  468 |         "usuario",
  469 |         "tipo_termo",
  470 |         "versao_termo",
  471 |         "aceito",
  472 |         "data_aceite",
  473 |     )
  474 | 
  475 |     list_filter = (
  476 |         "tipo_termo",
  477 |         "aceito",
  478 |         "versao_termo",
  479 |     )
  480 | 
  481 |     search_fields = (
  482 |         "usuario__email",
  483 |         "usuario__nome",
  484 |     )
  485 | 
  486 |     # A data representa um evento real e nao deve ser alterada pelo formulario.
  487 |     readonly_fields = (
  488 |         "data_aceite",
  489 |     )
  490 | 
  491 | 
  492 | @admin.register(AuditoriaAcaoCritica)
  493 | class AuditoriaAcaoCriticaAdmin(admin.ModelAdmin):
  494 |     """Consulta somente leitura das acoes criticas registradas."""
  495 | 
  496 |     def has_view_permission(self, request, obj=None):
  497 |         return (
  498 |             request.user.perfil == Usuario.Perfil.ADMINISTRADOR
  499 |             and super().has_view_permission(request, obj)
  500 |         )
  501 | 
  502 |     def has_module_permission(self, request):
  503 |         return self.has_view_permission(request)
  504 | 
  505 |     list_display = (
  506 |         "criado_em",
  507 |         "acao",
  508 |         "resultado",
  509 |         "usuario",
  510 |         "alvo_tipo",
  511 |         "alvo_id",
  512 |         "ip",
  513 |     )
  514 | 
  515 |     list_filter = (
  516 |         "acao",
  517 |         "resultado",
  518 |         "criado_em",
  519 |     )
  520 | 
  521 |     search_fields = (
  522 |         "usuario__email",
  523 |         "usuario__nome",
  524 |         "descricao",
  525 |         "metadados",
  526 |         "alvo_tipo",
  527 |         "alvo_id",
  528 |         "ip",
  529 |     )
  530 | 
  531 |     readonly_fields = (
  532 |         "id_auditoria",
  533 |         "usuario",
  534 |         "acao",
  535 |         "resultado",
  536 |         "alvo_tipo",
  537 |         "alvo_id",
  538 |         "descricao",
  539 |         "ip",
  540 |         "user_agent",
  541 |         "metadados",
  542 |         "criado_em",
  543 |     )
  544 | 
  545 |     date_hierarchy = "criado_em"
  546 |     ordering = ("-criado_em",)
  547 | 
  548 |     def has_add_permission(self, request):
  549 |         return False
  550 | 
  551 |     def has_change_permission(self, request, obj=None):
  552 |         return False
  553 | 
  554 |     def has_delete_permission(self, request, obj=None):
  555 |         return False
  556 | 
  557 | 
  558 | @admin.register(Estoque)
  559 | class EstoqueAdmin(admin.ModelAdmin):
  560 |     """
  561 |     Consulta administrativa do estoque de cada Hemocentro.
  562 | 
  563 |     status_calculado e data_atualizacao ficam somente leitura porque sao
  564 |     derivados automaticamente pela camada de servico (accounts/estoque.py)
  565 |     sempre que a quantidade de bolsas muda.
  566 |     """
  567 | 
  568 |     list_display = (
  569 |         "hemocentro",
  570 |         "tipo_sanguineo",
  571 |         "quantidade_bolsas",
  572 |         "nivel_minimo",
  573 |         "nivel_critico",
  574 |         "status_calculado",
  575 |         "data_atualizacao",
  576 |     )
  577 | 
  578 |     list_filter = (
  579 |         "status_calculado",
  580 |         "tipo_sanguineo",
  581 |     )
  582 | 
  583 |     search_fields = (
  584 |         "hemocentro__email",
  585 |         "hemocentro__nome",
  586 |     )
  587 | 
  588 |     ordering = (
  589 |         "hemocentro__nome",
  590 |         "tipo_sanguineo",
  591 |     )
  592 | 
  593 |     readonly_fields = (
  594 |         "status_calculado",
  595 |         "data_atualizacao",
  596 |     )
  597 | 
  598 | 
  599 | @admin.register(EstoqueMovimentacao)
  600 | class EstoqueMovimentacaoAdmin(admin.ModelAdmin):
  601 |     """
  602 |     Historico somente leitura das movimentacoes de estoque (UC_30).
  603 | 
  604 |     Assim como ValidacaoHemocentroAdmin, este historico nunca deve ser
  605 |     criado, editado ou apagado pelo admin: toda movimentacao precisa
  606 |     passar por registrar_movimentacao_estoque para manter a quantidade
  607 |     de bolsas e a auditoria consistentes.
  608 |     """
  609 | 
  610 |     list_display = (
  611 |         "data_hora",
  612 |         "estoque",
  613 |         "tipo_movimento",
  614 |         "quantidade_anterior",
  615 |         "quantidade_movimentada",
  616 |         "quantidade_nova",
  617 |         "usuario_resp",
  618 |     )
  619 | 
  620 |     list_filter = (
  621 |         "tipo_movimento",
  622 |         "data_hora",
  623 |     )
  624 | 
  625 |     search_fields = (
  626 |         "estoque__hemocentro__email",
  627 |         "estoque__hemocentro__nome",
  628 |         "usuario_resp__email",
  629 |         "usuario_resp__nome",
  630 |         "motivo",
  631 |     )
  632 | 
  633 |     readonly_fields = (
  634 |         "id_mov",
  635 |         "estoque",
  636 |         "usuario_resp",
  637 |         "tipo_movimento",
  638 |         "quantidade_anterior",
  639 |         "quantidade_movimentada",
  640 |         "quantidade_nova",
  641 |         "motivo",
  642 |         "data_hora",
  643 |     )
  644 | 
  645 |     date_hierarchy = "data_hora"
  646 |     ordering = ("-data_hora",)
  647 | 
  648 |     def has_add_permission(self, request):
  649 |         return False
  650 | 
  651 |     def has_change_permission(self, request, obj=None):
  652 |         return False
  653 | 
  654 |     def has_delete_permission(self, request, obj=None):
  655 |         return False
  656 | 
  657 | 
  658 | @admin.register(Triagem)
  659 | class TriagemAdmin(admin.ModelAdmin):
  660 |     """
  661 |     Permite ao administrador consultar as triagens realizadas.
  662 | 
  663 |     Os dados ficam somente para consulta no painel administrativo.
  664 |     """
  665 | 
  666 |     # Colunas exibidas na listagem de triagens.
  667 |     list_display = (
  668 |         "id_triagem",
  669 |         "usuario",
  670 |         "modalidade",
  671 |         "status",
  672 |         "resultado",
  673 |         "regra_version",
  674 |         "data_liberacao",
  675 |         "iniciada_em",
  676 |         "finalizada_em",
  677 |     )
  678 | 
  679 |     # Filtros disponíveis no lado direito do admin.
  680 |     list_filter = (
  681 |         "modalidade",
  682 |         "status",
  683 |         "resultado",
  684 |         "regra_version",
  685 |         "iniciada_em",
  686 |     )
  687 | 
  688 |     # Campos usados na busca.
  689 |     search_fields = (
  690 |         "usuario__nome",
  691 |         "usuario__email",
  692 |         "regra_version",
  693 |     )
  694 | 
  695 |     # Impede alteração manual de resultados médicos.
  696 |     readonly_fields = (
  697 |         "id_triagem",
  698 |         "usuario",
  699 |         "modalidade",
  700 |         "status",
  701 |         "pergunta_atual",
  702 |         "fluxo_perguntas",
  703 |         "triagem_base",
  704 |         "regra_version",
  705 |         "resultado",
  706 |         "mensagem_resultado",
  707 |         "data_liberacao",
  708 |         "achados",
  709 |         "iniciada_em",
  710 |         "finalizada_em",
  711 |         "atualizada_em",
  712 |     )
  713 | 
  714 |     # Mostra a navegação por data.
  715 |     date_hierarchy = "iniciada_em"
  716 | 
  717 |     # Ordena as triagens mais recentes primeiro.
  718 |     ordering = ("-iniciada_em",)
  719 | 
  720 |     # Impede criação manual pelo administrador.
  721 |     def has_add_permission(self, request):
  722 |         return False
  723 | 
  724 |     # Impede alteração pelo administrador.
  725 |     def has_change_permission(self, request, obj=None):
  726 |         return False
  727 | 
  728 |     # Impede exclusão pelo administrador.
  729 |     def has_delete_permission(self, request, obj=None):
  730 |         return False
  731 | 
  732 | 
  733 | @admin.register(RespostaTriagem)
  734 | class RespostaTriagemAdmin(admin.ModelAdmin):
  735 |     """
  736 |     Permite consultar as respostas individuais das triagens.
  737 |     """
  738 | 
  739 |     # Colunas exibidas na listagem.
  740 |     list_display = (
  741 |         "id_resposta",
  742 |         "triagem",
  743 |         "id_pergunta",
  744 |         "codigo_resposta",
  745 |         "resposta_label",
  746 |         "data_evento",
  747 |         "respondido_em",
  748 |     )
  749 | 
  750 |     # Filtros disponíveis.
  751 |     list_filter = (
  752 |         "id_pergunta",
  753 |         "rule_version",
  754 |         "respondido_em",
  755 |     )
  756 | 
  757 |     # Campos pesquisáveis.
  758 |     search_fields = (
  759 |         "triagem__usuario__nome",
  760 |         "triagem__usuario__email",
  761 |         "id_pergunta",
  762 |         "codigo_resposta",
  763 |         "resposta_label",
  764 |     )
  765 | 
  766 |     # Respostas não devem ser editadas manualmente.
  767 |     readonly_fields = (
  768 |         "id_resposta",
  769 |         "triagem",
  770 |         "id_pergunta",
  771 |         "codigo_resposta",
  772 |         "resposta_label",
  773 |         "data_evento",
  774 |         "metadata",
  775 |         "valor",
  776 |         "rule_version",
  777 |         "source_ref",
  778 |         "respondido_em",
  779 |     )
  780 | 
  781 |     # Ordena pelas respostas mais recentes.
  782 |     ordering = ("-respondido_em",)
  783 | 
  784 |     # Impede criação manual.
  785 |     def has_add_permission(self, request):
  786 |         return False
  787 | 
  788 |     # Impede alteração.
  789 |     def has_change_permission(self, request, obj=None):
  790 |         return False
  791 | 
  792 |     # Impede exclusão.
  793 |     def has_delete_permission(self, request, obj=None):
  794 |         return False
  795 | 
  796 | 
  797 | @admin.register(Notificacao)
  798 | class NotificacaoAdmin(admin.ModelAdmin):
  799 |     """Permite consultar os avisos internos enviados aos usuarios."""
  800 | 
  801 |     list_display = (
  802 |         "usuario",
  803 |         "tipo",
  804 |         "titulo",
  805 |         "lida",
  806 |         "criada_em",
  807 |     )
  808 | 
  809 |     list_filter = (
  810 |         "tipo",
  811 |         "lida",
  812 |         "criada_em",
  813 |     )
  814 | 
  815 |     search_fields = (
  816 |         "usuario__email",
  817 |         "usuario__nome",
  818 |         "titulo",
  819 |         "mensagem",
  820 |     )
  821 | 
  822 |     readonly_fields = (
  823 |         "criada_em",
  824 |         "lida_em",
  825 |     )
  826 | 
  827 |     ordering = ("-criada_em",)
  828 | 
  829 |     def has_add_permission(self, request):
  830 |         return False
  831 | 
  832 |     def has_change_permission(self, request, obj=None):
  833 |         return False
  834 | 
  835 |     def has_delete_permission(self, request, obj=None):
  836 |         return False
  837 | 
  838 | 
  839 | @admin.register(PedidoSangue)
  840 | class PedidoSangueAdmin(admin.ModelAdmin):
  841 |     """
  842 |     Consulta administrativa dos pedidos de sangue.
  843 | 
  844 |     A validacao deve acontecer pela camada de servico e pelo painel de
  845 |     validacao, nao editando status manualmente no admin.
  846 |     """
  847 | 
  848 |     list_display = (
  849 |         "id_pedido",
  850 |         "titulo",
  851 |         "solicitante",
  852 |         "contato",
  853 |         "hemocentro_destino",
  854 |         "tipo_sanguineo",
  855 |         "urgencia",
  856 |         "cidade",
  857 |         "status",
  858 |         "data_criacao",
  859 |     )
  860 | 
  861 |     list_filter = (
  862 |         "status",
  863 |         "urgencia",
  864 |         "tipo_sanguineo",
  865 |         "data_criacao",
  866 |     )
  867 | 
  868 |     search_fields = (
  869 |         "titulo",
  870 |         "cidade",
  871 |         "solicitante__email",
  872 |         "solicitante__nome",
  873 |         "hemocentro_destino__email",
  874 |         "hemocentro_destino__nome",
  875 |     )
  876 | 
  877 |     readonly_fields = (
  878 |         "id_pedido",
  879 |         "status",
  880 |         "data_criacao",
  881 |         "atualizado_em",
  882 |     )
  883 | 
  884 |     date_hierarchy = "data_criacao"
  885 |     ordering = ("-data_criacao",)
  886 | 
  887 |     def has_add_permission(self, request):
  888 |         return False
  889 | 
  890 |     def has_change_permission(self, request, obj=None):
  891 |         return False
  892 | 
  893 |     def has_delete_permission(self, request, obj=None):
  894 |         return False
  895 | 
  896 | 
  897 | @admin.register(ValidacaoPedido)
  898 | class ValidacaoPedidoAdmin(admin.ModelAdmin):
  899 |     """Historico somente leitura das validacoes de pedidos."""
  900 | 
  901 |     list_display = (
  902 |         "data_validacao",
  903 |         "pedido",
  904 |         "status_validacao",
  905 |         "moderador",
  906 |         "motivo_resumido",
  907 |     )
  908 | 
  909 |     list_filter = (
  910 |         "status_validacao",
  911 |         "data_validacao",
  912 |     )
  913 | 
  914 |     search_fields = (
  915 |         "pedido__titulo",
  916 |         "pedido__cidade",
  917 |         "moderador__email",
  918 |         "moderador__nome",
  919 |         "motivo",
  920 |     )
  921 | 
  922 |     readonly_fields = (
  923 |         "id_validacao",
  924 |         "pedido",
  925 |         "status_validacao",
  926 |         "motivo",
  927 |         "moderador",
  928 |         "data_validacao",
  929 |     )
  930 | 
  931 |     date_hierarchy = "data_validacao"
  932 |     ordering = ("-data_validacao",)
  933 | 
  934 |     def motivo_resumido(self, obj):
  935 |         if len(obj.motivo) <= 80:
  936 |             return obj.motivo
  937 | 
  938 |         return f"{obj.motivo[:77]}..."
  939 | 
  940 |     motivo_resumido.short_description = "Motivo"
  941 | 
  942 |     def has_add_permission(self, request):
  943 |         return False
  944 | 
  945 |     def has_change_permission(self, request, obj=None):
  946 |         return False
  947 | 
  948 |     def has_delete_permission(self, request, obj=None):
  949 |         return False
``````

## accounts/apps.py

Original: [accounts/apps.py](<C:/Users/lb119/Elo/accounts/apps.py>).

``````text
    1 | """
    2 | RESUMO DO ARQUIVO
    3 | =================
    4 | Define a configuracao do app accounts. O Django le esta classe durante a
    5 | inicializacao para registrar models, admin, migrations e outros componentes.
    6 | """
    7 | 
    8 | from django.apps import AppConfig
    9 | 
   10 | 
   11 | class AccountsConfig(AppConfig):
   12 |     """Metadados basicos do app de contas."""
   13 | 
   14 |     # BigAutoField e usado como padrao para chaves primarias nao declaradas.
   15 |     default_auto_field = "django.db.models.BigAutoField"
   16 | 
   17 |     # Deve ser igual ao nome da pasta Python do app.
   18 |     name = "accounts"
   19 | 
   20 |     # Nome amigavel exibido no painel administrativo.
   21 |     verbose_name = "Contas e autenticacao"
   22 | 
   23 |     def ready(self):
   24 |         """Carrega os sinais de auditoria quando o app inicia."""
   25 | 
   26 |         from . import signals  # noqa: F401
``````

## accounts/auditoria.py

Original: [accounts/auditoria.py](<C:/Users/lb119/Elo/accounts/auditoria.py>).

``````text
    1 | """
    2 | Funcoes centrais para registrar auditorias de acoes criticas.
    3 | 
    4 | As demais partes do sistema devem usar ``registrar_auditoria`` em vez de criar
    5 | AuditoriaAcaoCritica diretamente. Isso mantem saneamento de metadados,
    6 | captura de IP e regras de seguranca em um unico ponto.
    7 | """
    8 | 
    9 | from ipaddress import ip_address
   10 | 
   11 | from django.forms.models import model_to_dict
   12 | from django.utils.deprecation import MiddlewareMixin
   13 | 
   14 | from .models import AuditoriaAcaoCritica
   15 | 
   16 | 
   17 | CAMPOS_SENSIVEIS = {
   18 |     "password",
   19 |     "senha",
   20 |     "senha_hash",
   21 |     "token",
   22 |     "csrfmiddlewaretoken",
   23 |     "secret",
   24 |     "authorization",
   25 | }
   26 | 
   27 | """serve para identiifcar de onde a ação veio"""
   28 | def obter_ip(request):
   29 |     """Usa o endereco da conexao, sem confiar em cabecalhos enviados pelo cliente."""
   30 | 
   31 |     if not request:
   32 |         return None
   33 | 
   34 |     try:
   35 |         return str(ip_address(request.META.get("REMOTE_ADDR", "")))
   36 |     except ValueError:
   37 |         return None
   38 | 
   39 | 
   40 | def obter_user_agent(request):
   41 |     """Extrai o user agent sem obrigar chamadas internas a terem request."""
   42 | 
   43 |     if not request:
   44 |         return ""
   45 |     return request.META.get("HTTP_USER_AGENT", "")
   46 | 
   47 | 
   48 | def limpar_metadados(valor):
   49 |     """Remove dados sensiveis de estruturas simples antes de salvar auditoria."""
   50 | 
   51 |     if isinstance(valor, dict):
   52 |         metadados_limpos = {}
   53 |         for chave, item in valor.items():
   54 |             chave_texto = str(chave)
   55 |             if chave_texto.lower() in CAMPOS_SENSIVEIS:
   56 |                 metadados_limpos[chave_texto] = "[removido]"
   57 |             else:
   58 |                 metadados_limpos[chave_texto] = limpar_metadados(item)
   59 |         return metadados_limpos
   60 | 
   61 |     if isinstance(valor, (list, tuple, set)):
   62 |         return [limpar_metadados(item) for item in valor]
   63 | 
   64 |     return valor
   65 | 
   66 | 
   67 | def identificar_alvo(alvo):
   68 |     """Transforma um model ou valor simples em alvo_tipo e alvo_id."""
   69 | 
   70 |     if alvo is None:
   71 |         return "", ""
   72 | 
   73 |     if hasattr(alvo, "_meta"):
   74 |         alvo_tipo = alvo._meta.label
   75 |         chave_primaria = alvo.pk
   76 |         return alvo_tipo, str(chave_primaria or "")
   77 | 
   78 |     return alvo.__class__.__name__, str(alvo)
   79 | 
   80 | 
   81 | def registrar_auditoria(
   82 |     *,
   83 |     acao,
   84 |     usuario=None,
   85 |     resultado=AuditoriaAcaoCritica.Resultado.SUCESSO,
   86 |     alvo=None,
   87 |     alvo_tipo="",
   88 |     alvo_id="",
   89 |     descricao="",
   90 |     request=None,
   91 |     ip=None,
   92 |     user_agent="",
   93 |     metadados=None,
   94 | ):
   95 |     """Cria um registro de auditoria padronizado e sanitizado."""
   96 | 
   97 |     tipo_detectado, id_detectado = identificar_alvo(alvo)
   98 |     usuario_autenticado = getattr(usuario, "is_authenticated", False)
   99 | 
  100 |     if usuario is not None and not usuario_autenticado:
  101 |         usuario = None
  102 | 
  103 |     return AuditoriaAcaoCritica.objects.create(
  104 |         usuario=usuario,
  105 |         acao=acao,
  106 |         resultado=resultado,
  107 |         alvo_tipo=alvo_tipo or tipo_detectado,
  108 |         alvo_id=alvo_id or id_detectado,
  109 |         descricao=descricao,
  110 |         ip=ip or obter_ip(request),
  111 |         user_agent=user_agent or obter_user_agent(request),
  112 |         metadados=limpar_metadados(metadados or {}),
  113 |     )
  114 | 
  115 | 
  116 | def campos_sensiveis_alterados(objeto, campos):
  117 |     """Compara campos sensiveis de um model antes e depois da alteracao."""
  118 | 
  119 |     if not objeto.pk:
  120 |         return {}
  121 | 
  122 |     antigo = objeto.__class__.objects.filter(pk=objeto.pk).first()
  123 |     if not antigo:
  124 |         return {}
  125 | 
  126 |     alteracoes = {}
  127 |     for campo in campos:
  128 |         valor_antigo = getattr(antigo, campo)
  129 |         valor_novo = getattr(objeto, campo)
  130 |         if valor_antigo != valor_novo:
  131 |             alteracoes[campo] = {
  132 |                 "antes": str(valor_antigo),
  133 |                 "depois": str(valor_novo),
  134 |             }
  135 |     return alteracoes
  136 | 
  137 | 
  138 | def snapshot_campos(objeto, campos):
  139 |     """Retorna um dicionario com campos simples de um model."""
  140 | 
  141 |     dados = model_to_dict(objeto, fields=campos)
  142 |     return {campo: str(valor) for campo, valor in dados.items()}
  143 | 
  144 | 
  145 | class AuditoriaAcessosMiddleware(MiddlewareMixin):
  146 |     """Audita respostas protegidas sem copiar formularios ou dados clinicos."""
  147 | 
  148 |     ROTAS_SENSIVEIS = {
  149 |         "accounts:triagem_pergunta", "accounts:triagem_resultado",
  150 |         "accounts:triagem_historico", "accounts:painel_validacao_pedidos",
  151 |         "accounts:triagem_revisao", "accounts:minhas_solicitacoes",
  152 |         "accounts:painel_pedidos_hemocentro",
  153 |     }
  154 |     MODELOS_SENSIVEIS_ADMIN = {
  155 |         "usuario", "triagem", "respostatriagem", "consentimentolgpd",
  156 |         "pedidosangue", "validacaopedido", "validacaohemocentro",
  157 |         "notificacao", "auditoriaacaocritica",
  158 |     }
  159 | 
  160 |     def process_response(self, request, response):
  161 |         rota = getattr(request, "resolver_match", None)
  162 |         if rota is None:
  163 |             return response
  164 |         usuario = getattr(request, "user", None)
  165 |         autenticado = getattr(usuario, "is_authenticated", False)
  166 |         nome = rota.view_name
  167 |         protegido = nome.startswith("accounts:") and (
  168 |             nome in self.ROTAS_SENSIVEIS
  169 |             or any(parte in nome for parte in (
  170 |                 "triagem_iniciar", "estoque_hemocentro", "cadastrar_estoque",
  171 |                 "atualizar_estoque", "aprovar_pedido", "recusar_pedido",
  172 |                 "pedido_publicar", "criar_pedido_sangue",
  173 |                 "solicitar_correcao_pedido", "marcar_pedido_suspeito",
  174 |             ))
  175 |         )
  176 |         login_exigido = response.status_code == 302 and not autenticado and protegido
  177 |         bloqueado = response.status_code == 403 or (
  178 |             response.status_code == 404 and protegido and autenticado
  179 |         ) or login_exigido
  180 |         admin_sensivel = nome.startswith("admin:") and any(
  181 |             nome.startswith("admin:accounts_" + modelo + "_")
  182 |             for modelo in self.MODELOS_SENSIVEIS_ADMIN
  183 |         )
  184 |         dados_sensiveis = nome in self.ROTAS_SENSIVEIS or admin_sensivel or (
  185 |             nome == "accounts:dashboard" and getattr(usuario, "perfil", "") == "DOADOR"
  186 |         )
  187 |         if bloqueado:
  188 |             registrar_auditoria(
  189 |                 acao=AuditoriaAcaoCritica.Acao.MODERACAO,
  190 |                 resultado=AuditoriaAcaoCritica.Resultado.BLOQUEADO,
  191 |                 usuario=usuario, request=request,
  192 |                 descricao="Tentativa de acesso bloqueada.",
  193 |                 metadados={"evento": "TENTATIVA_ACESSO", "rota": nome,
  194 |                            "metodo": request.method, "status_http": response.status_code},
  195 |             )
  196 |         elif dados_sensiveis and request.method == "GET" and response.status_code == 200 and autenticado:
  197 |             registrar_auditoria(
  198 |                 acao=AuditoriaAcaoCritica.Acao.ACESSO_DADOS_SENSIVEIS,
  199 |                 usuario=usuario, request=request,
  200 |                 descricao="Consulta de dados sensiveis.",
  201 |                 metadados={"rota": nome, "parametros": rota.kwargs},
  202 |             )
  203 |         return response
``````

## accounts/compatibilidade.py

Original: [accounts/compatibilidade.py](<C:/Users/lb119/Elo/accounts/compatibilidade.py>).

``````text
    1 | TIPOS_SANGUINEOS = ("O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+")
    2 | 
    3 | COMPATIBILIDADE_RECEBIMENTO = {
    4 |     "O-": ("O-",),
    5 |     "O+": ("O-", "O+"),
    6 |     "A-": ("O-", "A-"),
    7 |     "A+": ("O-", "O+", "A-", "A+"),
    8 |     "B-": ("O-", "B-"),
    9 |     "B+": ("O-", "O+", "B-", "B+"),
   10 |     "AB-": ("O-", "A-", "B-", "AB-"),
   11 |     "AB+": TIPOS_SANGUINEOS,
   12 | }
   13 | 
   14 | POPULACAO_APROXIMADA = {
   15 |     "O-": "7%",
   16 |     "O+": "38%",
   17 |     "A-": "6%",
   18 |     "A+": "34%",
   19 |     "B-": "2%",
   20 |     "B+": "9%",
   21 |     "AB-": "1%",
   22 |     "AB+": "3%",
   23 | }
   24 | 
   25 | 
   26 | def normalizar_tipo_sanguineo(tipo_sanguineo):
   27 |     tipo = (tipo_sanguineo or "").strip().upper()
   28 |     if tipo not in TIPOS_SANGUINEOS:
   29 |         raise ValueError("Tipo sanguineo invalido.")
   30 |     return tipo
   31 | 
   32 | 
   33 | def doadores_compativeis_para(tipo_solicitado):
   34 |     tipo = normalizar_tipo_sanguineo(tipo_solicitado)
   35 |     return COMPATIBILIDADE_RECEBIMENTO[tipo]
   36 | 
   37 | 
   38 | def tipos_que_recebem_de(tipo_doador):
   39 |     tipo = normalizar_tipo_sanguineo(tipo_doador)
   40 |     return tuple(
   41 |         receptor
   42 |         for receptor, doadores in COMPATIBILIDADE_RECEBIMENTO.items()
   43 |         if tipo in doadores
   44 |     )
   45 | 
   46 | 
   47 | def tabela_de_compatibilidade():
   48 |     return [
   49 |         {
   50 |             "tipo": tipo,
   51 |             "doar_para": tipos_que_recebem_de(tipo),
   52 |             "receber_de": doadores_compativeis_para(tipo),
   53 |             "populacao": POPULACAO_APROXIMADA[tipo],
   54 |         }
   55 |         for tipo in TIPOS_SANGUINEOS
   56 |     ]
   57 | 
   58 | 
   59 | def doadores_aptos_para_convocacao(tipo_solicitado):
   60 |     """Aplica a mesma elegibilidade para os alertas de estoque e pedidos."""
   61 |     # Imports locais evitam o ciclo: models usa TIPOS_SANGUINEOS deste modulo.
   62 |     from django.conf import settings
   63 |     from django.db.models import Exists, OuterRef, Q, Subquery
   64 |     from django.utils import timezone
   65 |     from .models import ConsentimentoLGPD, Triagem, Usuario
   66 | 
   67 |     ultima_triagem = Triagem.objects.filter(
   68 |         usuario=OuterRef("pk"), status=Triagem.Status.CONCLUIDA,
   69 |     ).order_by("-finalizada_em", "-iniciada_em", "-id_triagem")
   70 |     consentimento = ConsentimentoLGPD.objects.filter(
   71 |         usuario=OuterRef("pk"),
   72 |         tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
   73 |         versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO,
   74 |         aceito=True, revogado_em__isnull=True,
   75 |     )
   76 |     return (
   77 |         Usuario.objects.filter(
   78 |             perfil=Usuario.Perfil.DOADOR, is_active=True, suspensa=False,
   79 |             aceita_notificacoes_pedidos=True,
   80 |             tipo_sanguineo__in=doadores_compativeis_para(tipo_solicitado),
   81 |         ).annotate(
   82 |             resultado_ultima_triagem=Subquery(ultima_triagem.values("resultado")[:1]),
   83 |             liberacao_ultima_triagem=Subquery(ultima_triagem.values("data_liberacao")[:1]),
   84 |             consentimento_convocacao=Exists(consentimento),
   85 |         ).filter(
   86 |             resultado_ultima_triagem=Triagem.Resultado.APTO,
   87 |             consentimento_convocacao=True,
   88 |         ).filter(
   89 |             Q(liberacao_ultima_triagem__isnull=True)
   90 |             | Q(liberacao_ultima_triagem__lte=timezone.localdate())
   91 |         ).order_by("pk")
   92 |     )
   93 | 
   94 | 
   95 | def limite_convocacao_atingido(usuario):
   96 |     """Soma os alertas de estoque e pedidos, mesmo os que ja foram lidos."""
   97 |     from datetime import timedelta
   98 |     from django.conf import settings
   99 |     from django.utils import timezone
  100 |     from .models import Notificacao
  101 | 
  102 |     inicio = timezone.now() - timedelta(hours=settings.CONVOCACAO_INTERVALO_HORAS)
  103 |     quantidade = Notificacao.objects.filter(
  104 |         usuario=usuario,
  105 |         tipo__in=[Notificacao.Tipo.ESTOQUE_BAIXO, Notificacao.Tipo.ESTOQUE_CRITICO,
  106 |                   Notificacao.Tipo.PEDIDO_COMPATIVEL],
  107 |         criada_em__gte=inicio,
  108 |     ).count()
  109 |     return quantidade >= settings.CONVOCACAO_LIMITE_NOTIFICACOES
  110 | 
  111 | 
  112 | def atualizar_preferencia_convocacao(usuario, aceita, request=None):
  113 |     """Registra a escolha explicita e sua revogacao nas tabelas existentes."""
  114 |     from django.conf import settings
  115 |     from django.core.exceptions import PermissionDenied
  116 |     from django.db import transaction
  117 |     from django.utils import timezone
  118 |     from .auditoria import obter_ip, registrar_auditoria
  119 |     from .models import AuditoriaAcaoCritica, ConsentimentoLGPD, Usuario
  120 | 
  121 |     if not usuario.is_authenticated or usuario.perfil != Usuario.Perfil.DOADOR:
  122 |         raise PermissionDenied("Somente Doadores podem configurar convocacoes.")
  123 |     with transaction.atomic():
  124 |         usuario = Usuario.objects.select_for_update().get(pk=usuario.pk)
  125 |         anterior = usuario.aceita_notificacoes_pedidos
  126 |         usuario.aceita_notificacoes_pedidos = bool(aceita)
  127 |         usuario.save(update_fields=["aceita_notificacoes_pedidos", "atualizado_em"])
  128 |         consentimento, criado = ConsentimentoLGPD.objects.get_or_create(
  129 |             usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
  130 |             versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO,
  131 |             defaults={"aceito": bool(aceita), "ip": obter_ip(request),
  132 |                       "revogado_em": None if aceita else timezone.now()},
  133 |         )
  134 |         if not criado:
  135 |             if aceita and (not consentimento.aceito or consentimento.revogado_em):
  136 |                 consentimento.data_aceite = timezone.now()
  137 |             consentimento.aceito = bool(aceita)
  138 |             consentimento.revogado_em = None if aceita else timezone.now()
  139 |             consentimento.ip = obter_ip(request)
  140 |             consentimento.save(update_fields=["aceito", "revogado_em", "data_aceite", "ip"])
  141 |         registrar_auditoria(
  142 |             acao=AuditoriaAcaoCritica.Acao.MODERACAO,
  143 |             usuario=usuario, alvo=consentimento, request=request,
  144 |             descricao="Preferencia de convocacao atualizada pelo doador.",
  145 |             metadados={"evento": "PREFERENCIA_CONVOCACAO", "antes": anterior,
  146 |                        "depois": bool(aceita), "versao_termo": consentimento.versao_termo},
  147 |         )
``````

## accounts/estoque.py

Original: [accounts/estoque.py](<C:/Users/lb119/Elo/accounts/estoque.py>).

``````text
    1 | """
    2 | Regras de negocio do estoque de sangue por Hemocentro.
    3 | 
    4 | UC_29 - Cadastrar Estoque:
    5 |     ``cadastrar_estoque`` cria a estrutura de estoque (quantidade, niveis
    6 |     de alerta e status calculado) para um par hemocentro + tipo sanguineo.
    7 | 
    8 | UC_30 - Atualizar Estoque:
    9 |     ``registrar_movimentacao_estoque`` aplica uma entrada, saida ou ajuste
   10 |     de bolsas, atualiza a quantidade do Estoque e grava o historico em
   11 |     EstoqueMovimentacao com o responsavel pela alteracao.
   12 | """
   13 | 
   14 | from django.core.exceptions import PermissionDenied, ValidationError
   15 | from django.db import transaction
   16 | from django.urls import reverse
   17 | 
   18 | from .auditoria import registrar_auditoria
   19 | from .compatibilidade import normalizar_tipo_sanguineo
   20 | from .compatibilidade import doadores_aptos_para_convocacao, limite_convocacao_atingido
   21 | from .models import (
   22 |     AuditoriaAcaoCritica,
   23 |     Estoque,
   24 |     EstoqueMovimentacao,
   25 |     Notificacao,
   26 |     Usuario,
   27 | )
   28 | from .validacao_hemocentro import validar_publicacao_hemocentro
   29 | 
   30 | 
   31 | STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA = {
   32 |     Estoque.StatusCalculado.CRITICO: Notificacao.Tipo.ESTOQUE_CRITICO,
   33 | }
   34 | 
   35 | 
   36 | @transaction.atomic
   37 | def criar_notificacoes_para_doadores_compativeis(*, estoque, status_calculado):
   38 |     """
   39 |     Cria notificacoes internas para doadores compativeis.
   40 | 
   41 |     Quando o estoque atualizado fica CRITICO, o sistema procura
   42 |     doadores compativeis e aptos que autorizaram convocacoes, respeitando
   43 |     o limite conjunto de notificacoes de estoque e pedidos.
   44 |     """
   45 | 
   46 |     if status_calculado not in STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA:
   47 |         return 0
   48 | 
   49 |     tipo_notificacao = STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA[status_calculado]
   50 | 
   51 |     # Serializa as convocacoes por doador antes de conferir o limite conjunto.
   52 |     doadores = doadores_aptos_para_convocacao(estoque.tipo_sanguineo).select_for_update()
   53 | 
   54 |     nivel = "critico"
   55 | 
   56 |     notificacoes = []
   57 | 
   58 |     for doador in doadores:
   59 |         if limite_convocacao_atingido(doador) or Notificacao.objects.filter(
   60 |             usuario=doador, estoque=estoque, tipo=tipo_notificacao, lida=False,
   61 |         ).exists():
   62 |             continue
   63 | 
   64 |         notificacoes.append(
   65 |             Notificacao(
   66 |                 usuario=doador,
   67 |                 estoque=estoque,
   68 |                 tipo=tipo_notificacao,
   69 |                 titulo=f"Estoque {nivel} para {estoque.tipo_sanguineo}",
   70 |                 mensagem=(
   71 |                     f"O estoque {estoque.tipo_sanguineo} do Hemocentro "
   72 |                     f"{estoque.hemocentro.nome} esta em nivel {nivel}. "
   73 |                     f"Seu tipo sanguineo ({doador.tipo_sanguineo}) "
   74 |                     "e compativel para doacao."
   75 |                 ),
   76 |                 url_destino=reverse("accounts:estoque_publico"),
   77 |             )
   78 |         )
   79 | 
   80 |     Notificacao.objects.bulk_create(notificacoes)
   81 | 
   82 |     return len(notificacoes)
   83 | 
   84 | 
   85 | def calcular_status_calculado(*, quantidade_bolsas, nivel_minimo, nivel_critico):
   86 |     """
   87 |     Deriva o status do estoque a partir da quantidade e dos niveis de alerta.
   88 | 
   89 |     Regra:
   90 |     - quantidade <= nivel_critico  -> CRITICO;
   91 |     - quantidade <= nivel_minimo   -> BAIXO;
   92 |     - caso contrario               -> ESTAVEL.
   93 |     """
   94 | 
   95 |     if quantidade_bolsas <= nivel_critico:
   96 |         return Estoque.StatusCalculado.CRITICO
   97 | 
   98 |     if quantidade_bolsas <= nivel_minimo:
   99 |         return Estoque.StatusCalculado.BAIXO
  100 | 
  101 |     return Estoque.StatusCalculado.ESTAVEL
  102 | 
  103 | 
  104 | def validar_responsavel_pelo_estoque(*, estoque, usuario):
  105 |     """
  106 |     Garante que somente o proprio Hemocentro aprovado, dono do estoque,
  107 |     possa gerenciar aquele registro.
  108 |     """
  109 | 
  110 |     validar_publicacao_hemocentro(usuario)
  111 | 
  112 |     if estoque is not None and estoque.hemocentro_id != usuario.pk:
  113 |         raise PermissionDenied(
  114 |             "Este estoque pertence a outro Hemocentro."
  115 |         )
  116 | 
  117 |     return True
  118 | 
  119 | 
  120 | def obter_estoque_do_hemocentro(*, hemocentro, tipo_sanguineo):
  121 |     """Busca um Estoque de um tipo sanguineo especifico."""
  122 | 
  123 |     tipo = normalizar_tipo_sanguineo(tipo_sanguineo)
  124 | 
  125 |     return Estoque.objects.filter(
  126 |         hemocentro=hemocentro,
  127 |         tipo_sanguineo=tipo,
  128 |     ).first()
  129 | 
  130 | 
  131 | def cadastrar_estoque(
  132 |     *,
  133 |     hemocentro,
  134 |     tipo_sanguineo,
  135 |     nivel_minimo,
  136 |     nivel_critico,
  137 |     quantidade_bolsas=0,
  138 |     request=None,
  139 | ):
  140 |     """
  141 |     UC_29 - Cria a estrutura de estoque de um tipo sanguineo para um
  142 |     Hemocentro aprovado.
  143 |     """
  144 | 
  145 |     validar_publicacao_hemocentro(hemocentro)
  146 | 
  147 |     tipo = normalizar_tipo_sanguineo(tipo_sanguineo)
  148 | 
  149 |     if nivel_critico > nivel_minimo:
  150 |         raise ValidationError(
  151 |             {
  152 |                 "nivel_critico": (
  153 |                     "O nivel critico deve ser menor ou igual ao nivel minimo."
  154 |                 )
  155 |             }
  156 |         )
  157 | 
  158 |     if Estoque.objects.filter(
  159 |         hemocentro=hemocentro,
  160 |         tipo_sanguineo=tipo,
  161 |     ).exists():
  162 |         raise ValidationError(
  163 |             f"Ja existe estoque cadastrado para o tipo {tipo} neste hemocentro."
  164 |         )
  165 | 
  166 |     status_calculado = calcular_status_calculado(
  167 |         quantidade_bolsas=quantidade_bolsas,
  168 |         nivel_minimo=nivel_minimo,
  169 |         nivel_critico=nivel_critico,
  170 |     )
  171 | 
  172 |     with transaction.atomic():
  173 |         estoque = Estoque.objects.create(
  174 |             hemocentro=hemocentro,
  175 |             tipo_sanguineo=tipo,
  176 |             quantidade_bolsas=quantidade_bolsas,
  177 |             nivel_minimo=nivel_minimo,
  178 |             nivel_critico=nivel_critico,
  179 |             status_calculado=status_calculado,
  180 |         )
  181 | 
  182 |         registrar_auditoria(
  183 |             acao=AuditoriaAcaoCritica.Acao.CADASTRO_ESTOQUE,
  184 |             usuario=hemocentro,
  185 |             alvo=estoque,
  186 |             descricao="Cadastro da estrutura de estoque de um tipo sanguineo.",
  187 |             request=request,
  188 |             metadados={
  189 |                 "tipo_sanguineo": tipo,
  190 |                 "quantidade_bolsas": quantidade_bolsas,
  191 |                 "nivel_minimo": nivel_minimo,
  192 |                 "nivel_critico": nivel_critico,
  193 |                 "status_calculado": status_calculado,
  194 |             },
  195 |         )
  196 | 
  197 |     return estoque
  198 | 
  199 | 
  200 | def registrar_movimentacao_estoque(
  201 |     *,
  202 |     estoque,
  203 |     usuario_resp,
  204 |     tipo_movimento,
  205 |     quantidade,
  206 |     motivo="",
  207 |     request=None,
  208 | ):
  209 |     """
  210 |     UC_30 - Aplica uma movimentacao de bolsas sobre um Estoque existente
  211 |     e grava o historico correspondente.
  212 |     """
  213 | 
  214 |     validar_responsavel_pelo_estoque(estoque=estoque, usuario=usuario_resp)
  215 | 
  216 |     if tipo_movimento not in EstoqueMovimentacao.TipoMovimento.values:
  217 |         raise ValidationError("Tipo de movimentacao invalido.")
  218 | 
  219 |     if tipo_movimento in (
  220 |         EstoqueMovimentacao.TipoMovimento.ENTRADA,
  221 |         EstoqueMovimentacao.TipoMovimento.SAIDA,
  222 |     ) and quantidade <= 0:
  223 |         raise ValidationError(
  224 |             {"quantidade": "Informe uma quantidade maior que zero."}
  225 |         )
  226 | 
  227 |     if tipo_movimento == EstoqueMovimentacao.TipoMovimento.AJUSTE and quantidade < 0:
  228 |         raise ValidationError(
  229 |             {"quantidade": "A quantidade ajustada nao pode ser negativa."}
  230 |         )
  231 | 
  232 |     motivo_limpo = (motivo or "").strip()
  233 |     if not motivo_limpo:
  234 |         raise ValidationError(
  235 |             {"motivo": "Informe o motivo da movimentacao de estoque."}
  236 |         )
  237 | 
  238 |     motivo_limpo = (motivo or "").strip()
  239 | 
  240 |     if not motivo_limpo:
  241 |         raise ValidationError(
  242 |             {
  243 |                 "motivo": (
  244 |                     "Informe o motivo da movimentacao de estoque."
  245 |                 )
  246 |             }
  247 |         )
  248 |     with transaction.atomic():
  249 |         estoque_atual = Estoque.objects.select_for_update().get(pk=estoque.pk)
  250 | 
  251 |         quantidade_anterior = estoque_atual.quantidade_bolsas
  252 | 
  253 |         if tipo_movimento == EstoqueMovimentacao.TipoMovimento.ENTRADA:
  254 |             quantidade_movimentada = quantidade
  255 |             quantidade_nova = quantidade_anterior + quantidade
  256 | 
  257 |         elif tipo_movimento == EstoqueMovimentacao.TipoMovimento.SAIDA:
  258 |             if quantidade > quantidade_anterior:
  259 |                 raise ValidationError(
  260 |                     {
  261 |                         "quantidade": (
  262 |                             "Nao ha bolsas suficientes para esta saida. "
  263 |                             f"Quantidade atual: {quantidade_anterior}."
  264 |                         )
  265 |                     }
  266 |                 )
  267 | 
  268 |             quantidade_movimentada = quantidade
  269 |             quantidade_nova = quantidade_anterior - quantidade
  270 | 
  271 |         else:
  272 |             quantidade_nova = quantidade
  273 |             quantidade_movimentada = quantidade_nova - quantidade_anterior
  274 | 
  275 |         status_calculado = calcular_status_calculado(
  276 |             quantidade_bolsas=quantidade_nova,
  277 |             nivel_minimo=estoque_atual.nivel_minimo,
  278 |             nivel_critico=estoque_atual.nivel_critico,
  279 |         )
  280 | 
  281 |         estoque_atual.quantidade_bolsas = quantidade_nova
  282 |         estoque_atual.status_calculado = status_calculado
  283 |         estoque_atual.save(
  284 |             update_fields=[
  285 |                 "quantidade_bolsas",
  286 |                 "status_calculado",
  287 |                 "data_atualizacao",
  288 |             ]
  289 |         )
  290 | 
  291 |         movimentacao = EstoqueMovimentacao.objects.create(
  292 |             estoque=estoque_atual,
  293 |             usuario_resp=usuario_resp,
  294 |             tipo_movimento=tipo_movimento,
  295 |             quantidade_anterior=quantidade_anterior,
  296 |             quantidade_movimentada=quantidade_movimentada,
  297 |             quantidade_nova=quantidade_nova,
  298 |             motivo=motivo_limpo,
  299 |     )
  300 | 
  301 |         notificacoes_geradas = criar_notificacoes_para_doadores_compativeis(
  302 |             estoque=estoque_atual,
  303 |             status_calculado=status_calculado,
  304 |         )
  305 | 
  306 |         registrar_auditoria(
  307 |             acao=AuditoriaAcaoCritica.Acao.ATUALIZACAO_ESTOQUE,
  308 |             usuario=usuario_resp,
  309 |             alvo=estoque_atual,
  310 |             descricao="Movimentacao de bolsas no estoque.",
  311 |             request=request,
  312 |             metadados={
  313 |                 "id_mov": movimentacao.pk,
  314 |                 "tipo_movimento": tipo_movimento,
  315 |                 "quantidade_anterior": quantidade_anterior,
  316 |                 "quantidade_movimentada": quantidade_movimentada,
  317 |                 "quantidade_nova": quantidade_nova,
  318 |                 "status_calculado": status_calculado,
  319 |                 "notificacoes_geradas": notificacoes_geradas,
  320 |                 "motivo": movimentacao.motivo,
  321 |             },
  322 |         )
  323 | 
  324 |     return movimentacao
  325 | 
  326 | 
  327 | def calcular_status_publico(quantidade_bolsas, nivel_minimo, nivel_critico):
  328 |     """
  329 |     Calcula o status que sera exibido publicamente.
  330 | 
  331 |     Os niveis minimo e critico sao utilizados apenas internamente
  332 |     para determinar a situacao do estoque.
  333 |     """
  334 | 
  335 |     if quantidade_bolsas <= nivel_critico:
  336 |         return "CRITICO"
  337 | 
  338 |     if quantidade_bolsas <= nivel_minimo:
  339 |         return "BAIXO"
  340 | 
  341 |     if quantidade_bolsas > nivel_minimo * 2:
  342 |         return "ALTO"
  343 | 
  344 |     return "ADEQUADO"
  345 | 
  346 | 
  347 | STATUS_PUBLICO_LABEL = {
  348 |     "CRITICO": "Crítico",
  349 |     "BAIXO": "Baixo",
  350 |     "ADEQUADO": "Adequado",
  351 |     "ALTO": "Alto",
  352 | }
  353 | 
  354 | 
  355 | def obter_estoques_publicos():
  356 |     """
  357 |     Busca os estoques dos Hemocentros aprovados e retorna somente
  358 |     os dados que podem ser exibidos publicamente.
  359 |     """
  360 | 
  361 |     estoques = (
  362 |         Estoque.objects
  363 |         .select_related("hemocentro")
  364 |         .filter(
  365 |             hemocentro__perfil=Usuario.Perfil.HEMOCENTRO,
  366 |             hemocentro__status_validacao=(
  367 |                 Usuario.StatusValidacaoHemocentro.APROVADO
  368 |             ),
  369 |         )
  370 |         .order_by(
  371 |             "hemocentro__cidade",
  372 |             "hemocentro__nome",
  373 |             "tipo_sanguineo",
  374 |         )
  375 |     )
  376 | 
  377 |     resultado = []
  378 | 
  379 |     for estoque in estoques:
  380 |         status_codigo = calcular_status_publico(
  381 |             estoque.quantidade_bolsas,
  382 |             estoque.nivel_minimo,
  383 |             estoque.nivel_critico,
  384 |         )
  385 |         resultado.append(
  386 |             {
  387 |                 "nome": estoque.hemocentro.nome,
  388 |                 "cidade": estoque.hemocentro.cidade,
  389 |                 "estado": estoque.hemocentro.estado,
  390 |                 "tipo_sanguineo": estoque.tipo_sanguineo,
  391 |                 "quantidade_bolsas": estoque.quantidade_bolsas,
  392 |                 # ``status`` permanece como código para compatibilidade com
  393 |                 # integrações; os campos abaixo facilitam a exibição e os
  394 |                 # filtros sem expor níveis internos.
  395 |                 "status": status_codigo,
  396 |                 "status_codigo": status_codigo,
  397 |                 "status_label": STATUS_PUBLICO_LABEL[status_codigo],
  398 |                 "data_atualizacao": estoque.data_atualizacao,
  399 |             }
  400 |         )
  401 | 
  402 |     return resultado
``````

## accounts/forms.py

Original: [accounts/forms.py](<C:/Users/lb119/Elo/accounts/forms.py>).

``````text
    1 | """
    2 | Formularios de cadastro e login do sistema Elo.
    3 | 
    4 | O formulario de cadastro:
    5 | 
    6 | - valida e-mail;
    7 | - valida CPF e CNPJ;
    8 | - exige CPF para Doador/Receptor;
    9 | - exige CNPJ para Hemocentro;
   10 | - exige data de nascimento para Doador/Receptor;
   11 | - valida senha;
   12 | - registra o aceite da LGPD por meio da view.
   13 | """
   14 | 
   15 | import re
   16 | from datetime import date
   17 | 
   18 | from django import forms
   19 | from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
   20 | 
   21 | from .compatibilidade import TIPOS_SANGUINEOS
   22 | from .models import EstoqueMovimentacao, PedidoSangue, Usuario
   23 | 
   24 | 
   25 | def apenas_digitos(valor):
   26 |     """Retira todos os caracteres que nao sejam numeros."""
   27 |     return re.sub(r"\D", "", valor or "")
   28 | 
   29 | 
   30 | class CadastroUsuarioForm(UserCreationForm):
   31 |     """Formulario publico utilizado para criar contas."""
   32 | 
   33 |     cpf = forms.CharField(
   34 |         label="CPF",
   35 |         required=False,
   36 |         max_length=14,
   37 |         help_text="Obrigatorio para Doador e Receptor/Solicitante.",
   38 |         widget=forms.TextInput(
   39 |             attrs={
   40 |                 "placeholder": "000.000.000-00",
   41 |                 "autocomplete": "off",
   42 |                 "inputmode": "numeric",
   43 |             }
   44 |         ),
   45 |     )
   46 | 
   47 |     cnpj = forms.CharField(
   48 |         label="CNPJ",
   49 |         required=False,
   50 |         max_length=18,
   51 |         help_text="Obrigatorio somente para Hemocentro.",
   52 |         widget=forms.TextInput(
   53 |             attrs={
   54 |                 "placeholder": "00.000.000/0000-00",
   55 |                 "autocomplete": "off",
   56 |                 "inputmode": "numeric",
   57 |             }
   58 |         ),
   59 |     )
   60 | 
   61 |     perfil = forms.ChoiceField(
   62 |         label="Tipo de perfil",
   63 |         choices=[
   64 |             (Usuario.Perfil.DOADOR, "Doador"),
   65 |             (Usuario.Perfil.RECEPTOR, "Receptor / Solicitante"),
   66 |             (Usuario.Perfil.HEMOCENTRO, "Hemocentro"),
   67 |             (Usuario.Perfil.OBSERVADOR, "Observador"),
   68 |         ],
   69 |         help_text=(
   70 |             "Escolha Hemocentro somente para uma instituicao que sera "
   71 |             "analisada por um administrador."
   72 |         ),
   73 |         widget=forms.RadioSelect,
   74 |     )
   75 | 
   76 |     data_nascimento = forms.DateField(
   77 |         label="Data de nascimento",
   78 |         required=False,
   79 |         help_text="Obrigatoria para Doador e Receptor/Solicitante.",
   80 |         widget=forms.DateInput(
   81 |             attrs={
   82 |                 "type": "date",
   83 |             }
   84 |         ),
   85 |     )
   86 | 
   87 |     aceite_lgpd = forms.BooleanField(
   88 |         label="Li e aceito os Termos de Uso e a Politica de Privacidade.",
   89 |         required=True,
   90 |     )
   91 | 
   92 |     aceita_notificacoes_pedidos = forms.BooleanField(
   93 |         label="Autorizo alertas internos de estoque e pedidos compativeis (para Doadores).",
   94 |         required=False,
   95 |         initial=False,
   96 |         help_text="Opcional. Posso cancelar a autorizacao no meu painel.",
   97 |     )
   98 | 
   99 |     class Meta:
  100 |         model = Usuario
  101 | 
  102 |         fields = [
  103 |             "nome",
  104 |             "email",
  105 |             "perfil",
  106 |             "cpf",
  107 |             "cnpj",
  108 |             "telefone",
  109 |             "data_nascimento",
  110 |             "sexo",
  111 |             "cidade",
  112 |             "estado",
  113 |             "password1",
  114 |             "password2",
  115 |             "aceite_lgpd",
  116 |             "aceita_notificacoes_pedidos",
  117 |         ]
  118 | 
  119 |         labels = {
  120 |             "nome": "Nome completo",
  121 |             "email": "E-mail",
  122 |             "telefone": "Telefone",
  123 |             "sexo": "Sexo",
  124 |             "cidade": "Cidade",
  125 |             "estado": "Estado (UF)",
  126 |         }
  127 | 
  128 |         widgets = {
  129 |             "email": forms.EmailInput(
  130 |                 attrs={
  131 |                     "autocomplete": "email",
  132 |                 }
  133 |             ),
  134 |             "telefone": forms.TextInput(
  135 |                 attrs={
  136 |                     "placeholder": "(00) 00000-0000",
  137 |                     "inputmode": "tel",
  138 |                 }
  139 |             ),
  140 |             "estado": forms.TextInput(
  141 |                 attrs={
  142 |                     "maxlength": 2,
  143 |                     "placeholder": "MG",
  144 |                     "style": "text-transform: uppercase;",
  145 |                 }
  146 |             ),
  147 |         }
  148 | 
  149 |     def __init__(self, *args, **kwargs):
  150 |         super().__init__(*args, **kwargs)
  151 | 
  152 |         self.fields["password1"].label = "Senha"
  153 |         self.fields["password1"].help_text = (
  154 |             "Use no minimo 8 caracteres, incluindo letras e numeros."
  155 |         )
  156 | 
  157 |         self.fields["password2"].label = "Confirme a senha"
  158 | 
  159 |     def clean_nome(self):
  160 |         """Remove espacos desnecessarios do nome."""
  161 |         nome = (self.cleaned_data.get("nome") or "").strip()
  162 | 
  163 |         if not nome:
  164 |             raise forms.ValidationError("Informe o nome completo.")
  165 | 
  166 |         return nome
  167 | 
  168 |     def clean_email(self):
  169 |         """Padroniza o e-mail e verifica duplicidade."""
  170 |         email = (self.cleaned_data.get("email") or "").strip().lower()
  171 | 
  172 |         if Usuario.objects.filter(email__iexact=email).exists():
  173 |             raise forms.ValidationError(
  174 |                 "Ja existe uma conta cadastrada com este e-mail."
  175 |             )
  176 | 
  177 |         return email
  178 | 
  179 |     def clean_cpf(self):
  180 |         """Limpa e valida o CPF."""
  181 |         cpf = apenas_digitos(self.cleaned_data.get("cpf"))
  182 | 
  183 |         if cpf and len(cpf) != 11:
  184 |             raise forms.ValidationError(
  185 |                 "O CPF deve conter exatamente 11 numeros."
  186 |             )
  187 | 
  188 |         if cpf and Usuario.objects.filter(cpf=cpf).exists():
  189 |             raise forms.ValidationError(
  190 |                 "Este CPF ja esta cadastrado."
  191 |             )
  192 | 
  193 |         return cpf or None
  194 | 
  195 |     def clean_cnpj(self):
  196 |         """Limpa e valida o CNPJ."""
  197 |         cnpj = apenas_digitos(self.cleaned_data.get("cnpj"))
  198 | 
  199 |         if cnpj and len(cnpj) != 14:
  200 |             raise forms.ValidationError(
  201 |                 "O CNPJ deve conter exatamente 14 numeros."
  202 |             )
  203 | 
  204 |         if cnpj and Usuario.objects.filter(cnpj=cnpj).exists():
  205 |             raise forms.ValidationError(
  206 |                 "Este CNPJ ja esta cadastrado."
  207 |             )
  208 | 
  209 |         return cnpj or None
  210 | 
  211 |     def clean_estado(self):
  212 |         """Padroniza a UF."""
  213 |         estado = (self.cleaned_data.get("estado") or "").strip().upper()
  214 | 
  215 |         if estado and len(estado) != 2:
  216 |             raise forms.ValidationError(
  217 |                 "Informe a UF com 2 letras, por exemplo: MG."
  218 |             )
  219 | 
  220 |         return estado
  221 | 
  222 |     def clean_password1(self):
  223 |         """Valida a senha."""
  224 |         senha = self.cleaned_data.get("password1", "")
  225 | 
  226 |         if not senha:
  227 |             return senha
  228 | 
  229 |         possui_letra = bool(re.search(r"[A-Za-z]", senha))
  230 |         possui_numero = bool(re.search(r"\d", senha))
  231 | 
  232 |         if len(senha) < 8:
  233 |             raise forms.ValidationError(
  234 |                 "A senha deve possuir pelo menos 8 caracteres."
  235 |             )
  236 | 
  237 |         if not possui_letra or not possui_numero:
  238 |             raise forms.ValidationError(
  239 |                 "A senha precisa conter pelo menos uma letra e um numero."
  240 |             )
  241 | 
  242 |         return senha
  243 | 
  244 |     def clean(self):
  245 |         """
  246 |         Faz as validacoes que dependem do tipo de perfil.
  247 | 
  248 |         Regras:
  249 | 
  250 |         - Hemocentro -> CNPJ obrigatorio.
  251 |         - Doador/Receptor -> CPF e data de nascimento obrigatorios.
  252 |         - Observador -> pode ficar sem CPF/CNPJ.
  253 |         """
  254 |         dados = super().clean()
  255 | 
  256 |         perfil = dados.get("perfil")
  257 |         if perfil != Usuario.Perfil.DOADOR:
  258 |             dados["aceita_notificacoes_pedidos"] = False
  259 |         cpf = dados.get("cpf")
  260 |         cnpj = dados.get("cnpj")
  261 |         data_nascimento = dados.get("data_nascimento")
  262 | 
  263 |         perfis_pessoa = (
  264 |             Usuario.Perfil.DOADOR,
  265 |             Usuario.Perfil.RECEPTOR,
  266 |         )
  267 | 
  268 |         if perfil == Usuario.Perfil.HEMOCENTRO:
  269 |             if not cnpj:
  270 |                 self.add_error(
  271 |                     "cnpj",
  272 |                     "Informe o CNPJ do hemocentro.",
  273 |                 )
  274 |             if cpf:
  275 |                 self.add_error(
  276 |                     "cpf",
  277 |                     "Hemocentro deve informar CNPJ, não CPF.",
  278 |                 )
  279 | 
  280 |         if perfil in perfis_pessoa:
  281 |             if not cpf:
  282 |                 self.add_error(
  283 |                     "cpf",
  284 |                     "Informe o CPF para este tipo de perfil.",
  285 |                 )
  286 | 
  287 |             if not data_nascimento:
  288 |                 self.add_error(
  289 |                     "data_nascimento",
  290 |                     "Informe a data de nascimento para este tipo de perfil.",
  291 |                 )
  292 |             if cnpj:
  293 |                 self.add_error(
  294 |                     "cnpj",
  295 |                     "Doador e Receptor devem informar CPF, não CNPJ.",
  296 |                 )
  297 | 
  298 |         if perfil == Usuario.Perfil.OBSERVADOR and (cpf or cnpj):
  299 |             self.add_error(
  300 |                 "cpf" if cpf else "cnpj",
  301 |                 "Observador não precisa informar CPF ou CNPJ.",
  302 |             )
  303 | 
  304 |         return dados
  305 | 
  306 | 
  307 | class PreferenciaConvocacaoForm(forms.Form):
  308 |     aceita_convocacoes = forms.BooleanField(
  309 |         label="Autorizo receber alertas internos de estoque e pedidos compativeis.",
  310 |         required=False,
  311 |         help_text="Opcional. Desmarque para cancelar futuras convocacoes.",
  312 |     )
  313 | 
  314 | 
  315 | class LoginUsuarioForm(AuthenticationForm):
  316 |     """Formulario de login usando e-mail."""
  317 | 
  318 |     def confirm_login_allowed(self, user):
  319 |         super().confirm_login_allowed(user)
  320 |         if getattr(user, "suspensa", False):
  321 |             raise forms.ValidationError(
  322 |                 "Esta conta está suspensa. Procure o administrador.",
  323 |                 code="inactive",
  324 |             )
  325 | 
  326 |     username = forms.EmailField(
  327 |         label="E-mail",
  328 |         widget=forms.EmailInput(
  329 |             attrs={
  330 |                 "autocomplete": "email",
  331 |                 "autofocus": True,
  332 |             }
  333 |         ),
  334 |     )
  335 | 
  336 |     password = forms.CharField(
  337 |         label="Senha",
  338 |         strip=False,
  339 |         widget=forms.PasswordInput(
  340 |             attrs={
  341 |                 "autocomplete": "current-password",
  342 |             }
  343 |         ),
  344 |     )
  345 | 
  346 | 
  347 | class TriagemExtensaForm(forms.Form):
  348 |     """
  349 |     Formulário inicial da triagem extensa.
  350 | 
  351 |     Esta primeira etapa utiliza as perguntas EXT-01 até EXT-05B
  352 |     da especificação.
  353 |     """
  354 | 
  355 |     entende_orientacao = forms.ChoiceField(
  356 |         label=(
  357 |             "Você entende que esta triagem é apenas uma orientação "
  358 |             "e que a decisão final será feita pela equipe do hemocentro?"
  359 |         ),
  360 |         choices=[
  361 |             ("SIM", "Sim, entendo e quero continuar."),
  362 |             ("NAO", "Não entendi ou quero receber a explicação novamente."),
  363 |         ],
  364 |         widget=forms.RadioSelect,
  365 |     )
  366 | 
  367 |     idade = forms.ChoiceField(
  368 |         label="Qual é a sua idade hoje?",
  369 |         choices=[
  370 |             ("MENOS_16", "Menos de 16 anos"),
  371 |             ("16_17", "16 ou 17 anos"),
  372 |             ("18_60", "18 a 60 anos"),
  373 |             ("61_69", "61 a 69 anos"),
  374 |             ("70_MAIS", "70 anos ou mais"),
  375 |         ],
  376 |         widget=forms.RadioSelect,
  377 |     )
  378 | 
  379 |     peso = forms.ChoiceField(
  380 |         label="Quanto você pesa aproximadamente?",
  381 |         choices=[
  382 |             ("MENOS_50", "Menos de 50 kg"),
  383 |             ("50_55_9", "De 50 a 55,9 kg"),
  384 |             ("56_129_9", "De 56 a 129,9 kg"),
  385 |             ("130_MAIS", "130 kg ou mais"),
  386 |             ("NAO_SEI", "Não sei meu peso atual"),
  387 |         ],
  388 |         widget=forms.RadioSelect,
  389 |     )
  390 | 
  391 |     sexo_biologico = forms.ChoiceField(
  392 |         label="Qual opção corresponde ao seu sexo biológico?",
  393 |         choices=[
  394 |             ("FEMININO", "Feminino"),
  395 |             ("MASCULINO", "Masculino"),
  396 |             ("OUTRO", "Outra situação ou não sei qual regra se aplica"),
  397 |             ("NAO_INFORMAR", "Prefiro não informar"),
  398 |         ],
  399 |         widget=forms.RadioSelect,
  400 |     )
  401 | 
  402 |     ja_doou = forms.ChoiceField(
  403 |         label="Você já doou sangue alguma vez?",
  404 |         choices=[
  405 |             ("NAO", "Nunca doei"),
  406 |             ("SIM", "Sim, já doei"),
  407 |             ("NAO_LEMBRO", "Não tenho certeza ou não lembro"),
  408 |         ],
  409 |         widget=forms.RadioSelect,
  410 |     )
  411 | 
  412 |     data_ultima_doacao = forms.DateField(
  413 |         label="Qual foi a data da sua última doação de sangue total?",
  414 |         required=False,
  415 |         widget=forms.DateInput(
  416 |             attrs={
  417 |                 "type": "date",
  418 |             }
  419 |         ),
  420 |     )
  421 | 
  422 |     doacoes_12_meses = forms.ChoiceField(
  423 |         label="Quantas doações de sangue total você fez nos últimos 12 meses?",
  424 |         required=False,
  425 |         choices=[
  426 |             ("0", "Nenhuma"),
  427 |             ("1", "1"),
  428 |             ("2", "2"),
  429 |             ("3", "3"),
  430 |             ("4_MAIS", "4 ou mais"),
  431 |             ("NAO_LEMBRO", "Não lembro"),
  432 |         ],
  433 |         widget=forms.RadioSelect,
  434 |     )
  435 | 
  436 |     def clean(self):
  437 |         """
  438 |         Exige data e quantidade de doações quando o usuário
  439 |         informa que já doou sangue.
  440 |         """
  441 |         dados = super().clean()
  442 | 
  443 |         ja_doou = dados.get("ja_doou")
  444 |         data_ultima_doacao = dados.get("data_ultima_doacao")
  445 |         doacoes_12_meses = dados.get("doacoes_12_meses")
  446 | 
  447 |         if ja_doou == "SIM" and not data_ultima_doacao:
  448 |             self.add_error(
  449 |                 "data_ultima_doacao",
  450 |                 "Informe a data da última doação.",
  451 |             )
  452 | 
  453 |         if ja_doou == "SIM" and not doacoes_12_meses:
  454 |             self.add_error(
  455 |                 "doacoes_12_meses",
  456 |                 "Informe a quantidade de doações.",
  457 |             )
  458 | 
  459 |         if data_ultima_doacao and data_ultima_doacao > date.today():
  460 |             self.add_error(
  461 |                 "data_ultima_doacao",
  462 |                 "A data da última doação não pode estar no futuro.",
  463 |             )
  464 | 
  465 |         return dados
  466 | 
  467 | 
  468 | class CadastrarEstoqueForm(forms.Form):
  469 |     """
  470 |     UC_29 - Formulario usado pelo Hemocentro para cadastrar a estrutura
  471 |     de estoque de um tipo sanguineo.
  472 | 
  473 |     A validacao de "ja existe estoque para este tipo" e de "hemocentro
  474 |     aprovado" fica na camada de servico (accounts/estoque.py), porque
  475 |     depende do usuario logado, que o form nao conhece sozinho.
  476 |     """
  477 | 
  478 |     tipo_sanguineo = forms.ChoiceField(
  479 |         label="Tipo sanguíneo",
  480 |         choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
  481 |     )
  482 | 
  483 |     quantidade_bolsas = forms.IntegerField(
  484 |         label="Quantidade atual de bolsas",
  485 |         min_value=0,
  486 |         initial=0,
  487 |         help_text="Quantidade de bolsas já disponíveis, se houver.",
  488 |     )
  489 | 
  490 |     nivel_minimo = forms.IntegerField(
  491 |         label="Nível mínimo",
  492 |         min_value=0,
  493 |         help_text=(
  494 |             "A partir de quantas bolsas o tipo passa a ser considerado baixo."
  495 |         ),
  496 |     )
  497 | 
  498 |     nivel_critico = forms.IntegerField(
  499 |         label="Nível crítico",
  500 |         min_value=0,
  501 |         help_text=(
  502 |             "A partir de quantas bolsas o tipo passa a ser considerado crítico."
  503 |         ),
  504 |     )
  505 | 
  506 |     def clean(self):
  507 |         """Garante que o nível crítico nunca seja maior que o mínimo."""
  508 | 
  509 |         dados = super().clean()
  510 | 
  511 |         nivel_minimo = dados.get("nivel_minimo")
  512 |         nivel_critico = dados.get("nivel_critico")
  513 | 
  514 |         if (
  515 |             nivel_minimo is not None
  516 |             and nivel_critico is not None
  517 |             and nivel_critico > nivel_minimo
  518 |         ):
  519 |             self.add_error(
  520 |                 "nivel_critico",
  521 |                 "O nível crítico deve ser menor ou igual ao nível mínimo.",
  522 |             )
  523 | 
  524 |         return dados
  525 | 
  526 | 
  527 | class MovimentarEstoqueForm(forms.Form):
  528 |     """
  529 |     Formulario usado pelo Hemocentro para registrar entrada,
  530 |     saída ou ajuste de bolsas em um estoque já cadastrado.
  531 |     """
  532 | 
  533 |     tipo_movimento = forms.ChoiceField(
  534 |         label="Tipo de movimentação",
  535 |         choices=EstoqueMovimentacao.TipoMovimento.choices,
  536 |         widget=forms.RadioSelect,
  537 |     )
  538 | 
  539 |     quantidade = forms.IntegerField(
  540 |         label="Quantidade",
  541 |         min_value=0,
  542 |         help_text=(
  543 |             "Para entrada/saída: quantidade a movimentar. "
  544 |             "Para ajuste: nova quantidade total de bolsas."
  545 |         ),
  546 |     )
  547 | 
  548 |     motivo = forms.CharField(
  549 |         label="Motivo",
  550 |         required=True,
  551 |         max_length=255,
  552 |         widget=forms.Textarea(attrs={"rows": 3}),
  553 |         help_text=(
  554 |             "Obrigatório. Ex.: doação recebida, transfusão realizada, "
  555 |             "contagem física."
  556 |         ),
  557 |     )
  558 | 
  559 |     def clean(self):
  560 |         dados = super().clean()
  561 | 
  562 |         tipo_movimento = dados.get("tipo_movimento")
  563 |         quantidade = dados.get("quantidade")
  564 | 
  565 |         movimentos_positivos = (
  566 |             EstoqueMovimentacao.TipoMovimento.ENTRADA,
  567 |             EstoqueMovimentacao.TipoMovimento.SAIDA,
  568 |         )
  569 | 
  570 |         if (
  571 |             tipo_movimento in movimentos_positivos
  572 |             and quantidade is not None
  573 |             and quantidade <= 0
  574 |         ):
  575 |             self.add_error(
  576 |                 "quantidade",
  577 |                 "Informe uma quantidade maior que zero.",
  578 |             )
  579 | 
  580 |         return dados
  581 | 
  582 | class PedidoSangueForm(forms.ModelForm):
  583 |     """
  584 |     Formulário para solicitar a divulgação de uma necessidade.
  585 | 
  586 |     As validacoes mais sensiveis ficam em validacao_pedido.py.
  587 |     Aqui ficam as validacoes de formulario.
  588 |     """
  589 | 
  590 |     contato = forms.EmailField(
  591 |         label="E-mail de contato",
  592 |         widget=forms.EmailInput(
  593 |             attrs={
  594 |                 "autocomplete": "email",
  595 |                 "placeholder": "seuemail@exemplo.com",
  596 |             }
  597 |         ),
  598 |     )
  599 | 
  600 |     class Meta:
  601 |         model = PedidoSangue
  602 | 
  603 |         fields = [
  604 |             "nome_solicitante",
  605 |             "contato",
  606 |             "para_quem",
  607 |             "hemocentro_destino",
  608 |             "titulo",
  609 |             "tipo_sanguineo",
  610 |             "urgencia",
  611 |             "cidade",
  612 |             "nome_paciente",
  613 |             "descricao",
  614 |             "justificativa_urgencia",
  615 |             "informacoes_complementares",
  616 |         ]
  617 | 
  618 |         labels = {
  619 |             "para_quem": "Para quem e este pedido?",
  620 |             "nome_solicitante": "Nome ou identificação do solicitante",
  621 |             "contato": "E-mail de contato",
  622 |             "hemocentro_destino": "Hemocentro de destino",
  623 |             "titulo": "Titulo do pedido",
  624 |             "tipo_sanguineo": "Tipo sanguineo",
  625 |             "urgencia": "Urgencia",
  626 |             "cidade": "Cidade",
  627 |             "nome_paciente": "Nome da pessoa (opcional)",
  628 |             "descricao": "Descricao",
  629 |             "justificativa_urgencia": "Justificativa da urgencia",
  630 |             "informacoes_complementares": "Informações complementares",
  631 |         }
  632 | 
  633 |         widgets = {
  634 |             "para_quem": forms.RadioSelect,
  635 |             "tipo_sanguineo": forms.RadioSelect,
  636 |             "urgencia": forms.RadioSelect,
  637 |             "descricao": forms.Textarea(attrs={"rows": 5}),
  638 |             "justificativa_urgencia": forms.Textarea(attrs={"rows": 4}),
  639 |             "informacoes_complementares": forms.Textarea(attrs={"rows": 4}),
  640 |         }
  641 | 
  642 |     def __init__(self, *args, **kwargs):
  643 |         super().__init__(*args, **kwargs)
  644 | 
  645 |         self.fields["hemocentro_destino"].queryset = (
  646 |             Usuario.objects
  647 |             .filter(
  648 |                 perfil=Usuario.Perfil.HEMOCENTRO,
  649 |                 status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO,
  650 |             )
  651 |             .order_by("nome")
  652 |         )
  653 | 
  654 |     def clean_nome_paciente(self):
  655 |         return (self.cleaned_data.get("nome_paciente") or "").strip()
  656 | 
  657 |     def clean_nome_solicitante(self):
  658 |         nome = (self.cleaned_data.get("nome_solicitante") or "").strip()
  659 |         if not nome:
  660 |             raise forms.ValidationError(
  661 |                 "Informe o nome ou uma identificação do solicitante."
  662 |             )
  663 |         return nome
  664 | 
  665 |     def clean_contato(self):
  666 |         contato = (self.cleaned_data.get("contato") or "").strip()
  667 |         if not contato:
  668 |             raise forms.ValidationError("Informe um e-mail para retorno.")
  669 |         return contato.lower()
  670 | 
  671 |     def clean_descricao(self):
  672 |         descricao = (self.cleaned_data.get("descricao") or "").strip()
  673 | 
  674 |         if len(descricao) < 10:
  675 |             raise forms.ValidationError(
  676 |                 "Descreva a necessidade com pelo menos 10 caracteres."
  677 |             )
  678 | 
  679 |         return descricao
  680 | 
  681 |     def clean(self):
  682 |         dados = super().clean()
  683 | 
  684 |         urgencia = dados.get("urgencia")
  685 |         justificativa = (
  686 |             dados.get("justificativa_urgencia") or ""
  687 |         ).strip()
  688 | 
  689 |         if urgencia in [
  690 |             PedidoSangue.Urgencia.ALTA,
  691 |             PedidoSangue.Urgencia.CRITICA,
  692 |         ]:
  693 |             if len(justificativa) < 20:
  694 |                 self.add_error(
  695 |                     "justificativa_urgencia",
  696 |                     (
  697 |                         "Pedidos de urgencia alta ou critica precisam "
  698 |                         "de justificativa com pelo menos 20 caracteres."
  699 |                     ),
  700 |                 )
  701 | 
  702 |         return dados
  703 | 
  704 | 
  705 | class FiltroPedidoSangueForm(forms.Form):
  706 |     """
  707 |     RF - Visualizar e filtrar pedidos.
  708 | 
  709 |     Filtros:
  710 | 
  711 |     - tipo sanguineo;
  712 |     - urgencia;
  713 |     - cidade;
  714 |     - hemocentro;
  715 |     - data.
  716 |     """
  717 | 
  718 |     tipo_sanguineo = forms.ChoiceField(
  719 |         label="Tipo sanguineo",
  720 |         required=False,
  721 |         choices=[
  722 |             ("", "Todos")
  723 |         ] + [(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
  724 |     )
  725 | 
  726 |     urgencia = forms.ChoiceField(
  727 |         label="Urgencia",
  728 |         required=False,
  729 |         choices=[("", "Todas")] + list(PedidoSangue.Urgencia.choices),
  730 |     )
  731 | 
  732 |     cidade = forms.CharField(
  733 |         label="Cidade",
  734 |         required=False,
  735 |     )
  736 | 
  737 |     hemocentro = forms.CharField(
  738 |         label="Hemocentro",
  739 |         required=False,
  740 |     )
  741 | 
  742 |     data = forms.DateField(
  743 |         label="Data",
  744 |         required=False,
  745 |         widget=forms.DateInput(attrs={"type": "date"}),
  746 |     )
  747 | 
  748 |     status = forms.ChoiceField(
  749 |         label="Status",
  750 |         required=False,
  751 |         choices=[("", "Todos")] + list(PedidoSangue.Status.choices),
  752 |     )
  753 | 
  754 | 
  755 | class FiltroEstoquePublicoForm(forms.Form):
  756 |     """Filtros da consulta pública de estoques.
  757 | 
  758 |     A situação usa os códigos calculados pelo sistema. Os níveis mínimo e
  759 |     crítico continuam ocultos, pois são parâmetros internos do Hemocentro.
  760 |     """
  761 | 
  762 |     tipo_sanguineo = forms.ChoiceField(
  763 |         label="Tipo sanguíneo",
  764 |         required=False,
  765 |         choices=[("", "Todos")] + [(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
  766 |     )
  767 | 
  768 |     cidade = forms.CharField(
  769 |         label="Cidade",
  770 |         required=False,
  771 |     )
  772 | 
  773 |     hemocentro = forms.CharField(
  774 |         label="Hemocentro",
  775 |         required=False,
  776 |     )
  777 | 
  778 |     situacao = forms.ChoiceField(
  779 |         label="Situação do estoque",
  780 |         required=False,
  781 |         choices=[
  782 |             ("", "Todas"),
  783 |             ("CRITICO", "Crítico"),
  784 |             ("BAIXO", "Baixo"),
  785 |             ("ADEQUADO", "Adequado"),
  786 |             ("ALTO", "Alto"),
  787 |         ],
  788 |     )
  789 | 
  790 |     busca = forms.CharField(
  791 |         label="Busca",
  792 |         required=False,
  793 |         help_text="Nome do Hemocentro, cidade, UF ou tipo sanguíneo.",
  794 |     )
``````

## accounts/management/__init__.py

Original: [accounts/management/__init__.py](<C:/Users/lb119/Elo/accounts/management/__init__.py>).

``````text
    1 | 
``````

## accounts/management/commands/__init__.py

Original: [accounts/management/commands/__init__.py](<C:/Users/lb119/Elo/accounts/management/commands/__init__.py>).

``````text
    1 | 
``````

## accounts/management/commands/criar_perfis_teste.py

Original: [accounts/management/commands/criar_perfis_teste.py](<C:/Users/lb119/Elo/accounts/management/commands/criar_perfis_teste.py>).

``````text
    1 | """Prepara contas ficticias para testar os perfis no ambiente local."""
    2 | 
    3 | from django.conf import settings
    4 | from django.core.management.base import BaseCommand, CommandError
    5 | from django.db import transaction
    6 | from django.utils import timezone
    7 | 
    8 | from accounts.models import ConsentimentoLGPD, Triagem, Usuario
    9 | 
   10 | 
   11 | class Command(BaseCommand):
   12 |     help = "Cria contas ficticias de cada perfil, sem substituir contas existentes."
   13 | 
   14 |     def add_arguments(self, parser):
   15 |         parser.add_argument('--senha', default='EloTeste2026!', help='Senha das novas contas de teste.')
   16 | 
   17 |     @transaction.atomic
   18 |     def handle(self, *args, **options):
   19 |         if not settings.DEBUG:
   20 |             raise CommandError('Este comando exige DEBUG=True no ambiente de desenvolvimento.')
   21 |         if len(options['senha']) < 8:
   22 |             raise CommandError('Use uma senha com pelo menos oito caracteres.')
   23 | 
   24 |         perfis = [
   25 |             ('doador', Usuario.Perfil.DOADOR, {}),
   26 |             ('doador-inapto', Usuario.Perfil.DOADOR, {}),
   27 |             ('doador-sem-consentimento', Usuario.Perfil.DOADOR, {}),
   28 |             ('receptor', Usuario.Perfil.RECEPTOR, {}),
   29 |             ('observador', Usuario.Perfil.OBSERVADOR, {}),
   30 |             ('administrador', Usuario.Perfil.ADMINISTRADOR, {'is_staff': True, 'is_superuser': True}),
   31 |         ]
   32 |         for status in Usuario.StatusValidacaoHemocentro.values:
   33 |             perfis.append((f'hemocentro-{status.lower()}', Usuario.Perfil.HEMOCENTRO,
   34 |                            {'status_validacao': status}))
   35 | 
   36 |         for nome, perfil, extras in perfis:
   37 |             email = f'{nome}@teste.elo.test'
   38 |             if Usuario.objects.filter(email=email).exists():
   39 |                 self.stdout.write(f'Mantida sem alteracoes: {email}')
   40 |                 continue
   41 |             usuario = Usuario.objects.create_user(
   42 |                 email=email, password=options['senha'], nome=f'TESTE {nome}', perfil=perfil,
   43 |                 cidade='Belo Horizonte', estado='MG',
   44 |                 tipo_sanguineo='O-' if perfil == Usuario.Perfil.DOADOR else '',
   45 |                 aceita_notificacoes_pedidos=perfil == Usuario.Perfil.DOADOR,
   46 |                 **extras,
   47 |             )
   48 |             ConsentimentoLGPD.objects.create(
   49 |                 usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL, aceito=True,
   50 |             )
   51 |             if perfil == Usuario.Perfil.DOADOR:
   52 |                 Triagem.objects.create(
   53 |                     usuario=usuario, status=Triagem.Status.CONCLUIDA,
   54 |                     resultado=(Triagem.Resultado.INAPTO_TEMPORARIO if nome == 'doador-inapto'
   55 |                                else Triagem.Resultado.APTO),
   56 |                     finalizada_em=timezone.now(),
   57 |                 )
   58 |                 if nome != 'doador-sem-consentimento':
   59 |                     ConsentimentoLGPD.objects.create(
   60 |                         usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
   61 |                         versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO, aceito=True,
   62 |                     )
   63 |             self.stdout.write(self.style.SUCCESS(f'Criada: {email}'))
   64 |         self.stdout.write('Contas existentes e suas senhas foram preservadas. Veja TESTAR_PERFIS.md.')
``````

## accounts/migrations/0001_initial.py

Original: [accounts/migrations/0001_initial.py](<C:/Users/lb119/Elo/accounts/migrations/0001_initial.py>).

``````text
    1 | # Generated by Django 6.1 on 2026-08-14 12:01
    2 | 
    3 | import accounts.models
    4 | import django.db.models.deletion
    5 | from django.conf import settings
    6 | from django.db import migrations, models
    7 | 
    8 | 
    9 | class Migration(migrations.Migration):
   10 | 
   11 |     initial = True
   12 | 
   13 |     dependencies = [
   14 |         ('auth', '0012_alter_user_first_name_max_length'),
   15 |     ]
   16 | 
   17 |     operations = [
   18 |         migrations.CreateModel(
   19 |             name='Usuario',
   20 |             fields=[
   21 |                 ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
   22 |                 ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
   23 |                 ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
   24 |                 ('id_usuario', models.BigAutoField(primary_key=True, serialize=False)),
   25 |                 ('nome', models.CharField(max_length=150)),
   26 |                 ('email', models.EmailField(max_length=254, unique=True)),
   27 |                 ('password', models.CharField(db_column='senha_hash', max_length=128)),
   28 |                 ('cpf', models.CharField(blank=True, max_length=11, null=True, unique=True)),
   29 |                 ('cnpj', models.CharField(blank=True, max_length=14, null=True, unique=True)),
   30 |                 ('telefone', models.CharField(blank=True, max_length=20)),
   31 |                 ('data_nascimento', models.DateField(blank=True, null=True)),
   32 |                 ('sexo', models.CharField(blank=True, choices=[('F', 'Feminino'), ('M', 'Masculino'), ('O', 'Outro'), ('N', 'Prefiro nao informar')], max_length=1)),
   33 |                 ('cidade', models.CharField(blank=True, max_length=100)),
   34 |                 ('estado', models.CharField(blank=True, max_length=2)),
   35 |                 ('perfil', models.CharField(choices=[('DOADOR', 'Doador'), ('RECEPTOR', 'Receptor'), ('HEMOCENTRO', 'Hemocentro'), ('OBSERVADOR', 'Observador'), ('ADMINISTRADOR', 'Administrador')], max_length=20)),
   36 |                 ('is_active', models.BooleanField(db_column='ativo', default=True)),
   37 |                 ('email_verificado', models.BooleanField(default=False)),
   38 |                 ('date_joined', models.DateTimeField(auto_now_add=True, db_column='data_cadastro')),
   39 |                 ('atualizado_em', models.DateTimeField(auto_now=True)),
   40 |                 ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
   41 |                 ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
   42 |             ],
   43 |             options={
   44 |                 'verbose_name': 'usuario',
   45 |                 'verbose_name_plural': 'usuarios',
   46 |                 'db_table': 'usuarios',
   47 |                 'ordering': ['nome'],
   48 |             },
   49 |             managers=[
   50 |                 ('objects', accounts.models.UsuarioManager()),
   51 |             ],
   52 |         ),
   53 |         migrations.CreateModel(
   54 |             name='ConsentimentoLGPD',
   55 |             fields=[
   56 |                 ('id_consentimento', models.BigAutoField(primary_key=True, serialize=False)),
   57 |                 ('tipo_termo', models.CharField(choices=[('GERAL', 'Termos gerais e politica de privacidade'), ('TRIAGEM', 'Termo de triagem'), ('NOTIFICACOES', 'Termo de notificacoes')], max_length=20)),
   58 |                 ('versao_termo', models.CharField(default='1.0', max_length=20)),
   59 |                 ('aceito', models.BooleanField(default=False)),
   60 |                 ('data_aceite', models.DateTimeField(auto_now_add=True)),
   61 |                 ('ip', models.GenericIPAddressField(blank=True, null=True)),
   62 |                 ('revogado_em', models.DateTimeField(blank=True, null=True)),
   63 |                 ('usuario', models.ForeignKey(db_column='id_usuario', on_delete=django.db.models.deletion.CASCADE, related_name='consentimentos_lgpd', to=settings.AUTH_USER_MODEL)),
   64 |             ],
   65 |             options={
   66 |                 'verbose_name': 'consentimento LGPD',
   67 |                 'verbose_name_plural': 'consentimentos LGPD',
   68 |                 'db_table': 'consentimentos_lgpd',
   69 |                 'ordering': ['-data_aceite'],
   70 |                 'constraints': [models.UniqueConstraint(fields=('usuario', 'tipo_termo', 'versao_termo'), name='consentimento_unico_por_versao')],
   71 |             },
   72 |         ),
   73 |     ]
``````

## accounts/migrations/0002_remove_usuario_cidade_remove_usuario_cnpj_and_more.py

Original: [accounts/migrations/0002_remove_usuario_cidade_remove_usuario_cnpj_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0002_remove_usuario_cidade_remove_usuario_cnpj_and_more.py>).

``````text
    1 | # Generated by Django 6.1 on 2026-08-14 14:53
    2 | 
    3 | from django.db import migrations, models
    4 | 
    5 | 
    6 | class Migration(migrations.Migration):
    7 | 
    8 |     dependencies = [
    9 |         ('accounts', '0001_initial'),
   10 |     ]
   11 | 
   12 |     operations = [
   13 |         migrations.RemoveField(
   14 |             model_name='usuario',
   15 |             name='cidade',
   16 |         ),
   17 |         migrations.RemoveField(
   18 |             model_name='usuario',
   19 |             name='cnpj',
   20 |         ),
   21 |         migrations.RemoveField(
   22 |             model_name='usuario',
   23 |             name='cpf',
   24 |         ),
   25 |         migrations.RemoveField(
   26 |             model_name='usuario',
   27 |             name='data_nascimento',
   28 |         ),
   29 |         migrations.RemoveField(
   30 |             model_name='usuario',
   31 |             name='estado',
   32 |         ),
   33 |         migrations.RemoveField(
   34 |             model_name='usuario',
   35 |             name='perfil',
   36 |         ),
   37 |         migrations.RemoveField(
   38 |             model_name='usuario',
   39 |             name='sexo',
   40 |         ),
   41 |         migrations.RemoveField(
   42 |             model_name='usuario',
   43 |             name='telefone',
   44 |         ),
   45 |         migrations.AlterField(
   46 |             model_name='consentimentolgpd',
   47 |             name='tipo_termo',
   48 |             field=models.CharField(choices=[('GERAL', 'Termos gerais e politica de privacidade')], default='GERAL', max_length=20),
   49 |         ),
   50 |     ]
``````

## accounts/migrations/0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more.py

Original: [accounts/migrations/0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more.py>).

``````text
    1 | # Generated by Django 6.1 on 2026-08-14 15:24
    2 | 
    3 | from django.db import migrations, models
    4 | 
    5 | 
    6 | class Migration(migrations.Migration):
    7 | 
    8 |     dependencies = [
    9 |         ('accounts', '0002_remove_usuario_cidade_remove_usuario_cnpj_and_more'),
   10 |     ]
   11 | 
   12 |     operations = [
   13 |         migrations.AddField(
   14 |             model_name='usuario',
   15 |             name='cidade',
   16 |             field=models.CharField(blank=True, default='', max_length=100),
   17 |         ),
   18 |         migrations.AddField(
   19 |             model_name='usuario',
   20 |             name='cnpj',
   21 |             field=models.CharField(blank=True, max_length=14, null=True, unique=True),
   22 |         ),
   23 |         migrations.AddField(
   24 |             model_name='usuario',
   25 |             name='cpf',
   26 |             field=models.CharField(blank=True, max_length=11, null=True, unique=True),
   27 |         ),
   28 |         migrations.AddField(
   29 |             model_name='usuario',
   30 |             name='data_nascimento',
   31 |             field=models.DateField(blank=True, null=True),
   32 |         ),
   33 |         migrations.AddField(
   34 |             model_name='usuario',
   35 |             name='estado',
   36 |             field=models.CharField(blank=True, default='', max_length=2),
   37 |         ),
   38 |         migrations.AddField(
   39 |             model_name='usuario',
   40 |             name='perfil',
   41 |             field=models.CharField(choices=[('DOADOR', 'Doador'), ('RECEPTOR', 'Receptor'), ('HEMOCENTRO', 'Hemocentro'), ('OBSERVADOR', 'Observador'), ('ADMINISTRADOR', 'Administrador')], default='OBSERVADOR', max_length=20),
   42 |         ),
   43 |         migrations.AddField(
   44 |             model_name='usuario',
   45 |             name='sexo',
   46 |             field=models.CharField(blank=True, choices=[('F', 'Feminino'), ('M', 'Masculino'), ('O', 'Outro'), ('N', 'Prefiro nao informar')], default='', max_length=1),
   47 |         ),
   48 |         migrations.AddField(
   49 |             model_name='usuario',
   50 |             name='telefone',
   51 |             field=models.CharField(blank=True, default='', max_length=20),
   52 |         ),
   53 |         migrations.AlterField(
   54 |             model_name='consentimentolgpd',
   55 |             name='tipo_termo',
   56 |             field=models.CharField(choices=[('GERAL', 'Termos gerais e politica de privacidade'), ('TRIAGEM', 'Termo de triagem'), ('NOTIFICACOES', 'Termo de notificacoes')], default='GERAL', max_length=20),
   57 |         ),
   58 |     ]
``````

## accounts/migrations/0004_auditoriaacaocritica.py

Original: [accounts/migrations/0004_auditoriaacaocritica.py](<C:/Users/lb119/Elo/accounts/migrations/0004_auditoriaacaocritica.py>).

``````text
    1 | # Generated by Django 5.2.17 on 2026-08-21 11:14
    2 | 
    3 | import django.db.models.deletion
    4 | from django.conf import settings
    5 | from django.db import migrations, models
    6 | 
    7 | 
    8 | class Migration(migrations.Migration):
    9 | 
   10 |     dependencies = [
   11 |         ('accounts', '0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more'),
   12 |     ]
   13 | 
   14 |     operations = [
   15 |         migrations.CreateModel(
   16 |             name='AuditoriaAcaoCritica',
   17 |             fields=[
   18 |                 ('id_auditoria', models.BigAutoField(primary_key=True, serialize=False)),
   19 |                 ('acao', models.CharField(choices=[('LOGIN_FALHO', 'Login falho'), ('LOGIN_SUSPEITO', 'Login suspeito'), ('ALTERACAO_PERMISSAO', 'Alteracao de permissao'), ('APROVACAO_HEMOCENTRO', 'Aprovacao de hemocentro'), ('ATUALIZACAO_ESTOQUE', 'Atualizacao de estoque'), ('MODERACAO', 'Moderacao'), ('ACESSO_DADOS_SENSIVEIS', 'Acesso a dados sensiveis'), ('CONFIRMACAO_DOACAO', 'Confirmacao de doacao')], max_length=40)),
   20 |                 ('resultado', models.CharField(choices=[('SUCESSO', 'Sucesso'), ('FALHA', 'Falha'), ('BLOQUEADO', 'Bloqueado')], default='SUCESSO', max_length=20)),
   21 |                 ('alvo_tipo', models.CharField(blank=True, default='', max_length=80)),
   22 |                 ('alvo_id', models.CharField(blank=True, default='', max_length=80)),
   23 |                 ('descricao', models.CharField(blank=True, default='', max_length=255)),
   24 |                 ('ip', models.GenericIPAddressField(blank=True, null=True)),
   25 |                 ('user_agent', models.TextField(blank=True, default='')),
   26 |                 ('metadados', models.JSONField(blank=True, default=dict)),
   27 |                 ('criado_em', models.DateTimeField(auto_now_add=True)),
   28 |                 ('usuario', models.ForeignKey(blank=True, db_column='id_usuario', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auditorias_acoes_criticas', to=settings.AUTH_USER_MODEL)),
   29 |             ],
   30 |             options={
   31 |                 'verbose_name': 'auditoria de acao critica',
   32 |                 'verbose_name_plural': 'auditorias de acoes criticas',
   33 |                 'db_table': 'auditorias_acoes_criticas',
   34 |                 'ordering': ['-criado_em'],
   35 |                 'indexes': [models.Index(fields=['acao', 'criado_em'], name='auditoria_acao_data_idx'), models.Index(fields=['usuario', 'criado_em'], name='auditoria_usuario_data_idx'), models.Index(fields=['ip', 'criado_em'], name='auditoria_ip_data_idx')],
   36 |             },
   37 |         ),
   38 |     ]
``````

## accounts/migrations/0005_usuario_status_validacao_validacaohemocentro.py

Original: [accounts/migrations/0005_usuario_status_validacao_validacaohemocentro.py](<C:/Users/lb119/Elo/accounts/migrations/0005_usuario_status_validacao_validacaohemocentro.py>).

``````text
    1 | # Generated by Django 5.2.17 on 2026-08-25 23:01
    2 | 
    3 | import django.db.models.deletion
    4 | from django.conf import settings
    5 | from django.db import migrations, models
    6 | 
    7 | 
    8 | class Migration(migrations.Migration):
    9 | 
   10 |     dependencies = [
   11 |         ('accounts', '0004_auditoriaacaocritica'),
   12 |     ]
   13 | 
   14 |     operations = [
   15 |         migrations.AddField(
   16 |             model_name='usuario',
   17 |             name='status_validacao',
   18 |             field=models.CharField(choices=[('PENDENTE', 'Pendente'), ('APROVADO', 'Aprovado'), ('RECUSADO', 'Recusado'), ('CORRECAO', 'Correcao necessaria')], default='PENDENTE', max_length=20),
   19 |         ),
   20 |         migrations.CreateModel(
   21 |             name='ValidacaoHemocentro',
   22 |             fields=[
   23 |                 ('id_validacao', models.BigAutoField(primary_key=True, serialize=False)),
   24 |                 ('status', models.CharField(choices=[('PENDENTE', 'Pendente'), ('APROVADO', 'Aprovado'), ('RECUSADO', 'Recusado'), ('CORRECAO', 'Correcao necessaria')], max_length=20)),
   25 |                 ('parecer', models.TextField(blank=True, default='')),
   26 |                 ('data_analise', models.DateTimeField(auto_now_add=True)),
   27 |                 ('admin', models.ForeignKey(blank=True, db_column='id_admin', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='validacoes_hemocentro_realizadas', to=settings.AUTH_USER_MODEL)),
   28 |                 ('hemocentro', models.ForeignKey(db_column='id_hemocentro', on_delete=django.db.models.deletion.CASCADE, related_name='validacoes_hemocentro', to=settings.AUTH_USER_MODEL)),
   29 |             ],
   30 |             options={
   31 |                 'verbose_name': 'validacao de hemocentro',
   32 |                 'verbose_name_plural': 'validacoes de hemocentros',
   33 |                 'db_table': 'validacoes_hemocentro',
   34 |                 'ordering': ['-data_analise'],
   35 |                 'indexes': [models.Index(fields=['hemocentro', '-data_analise'], name='validacao_hemo_data_idx'), models.Index(fields=['status', 'data_analise'], name='validacao_hemo_status_idx')],
   36 |             },
   37 |         ),
   38 |     ]
``````

## accounts/migrations/0006_triagem_respostatriagem_and_more.py

Original: [accounts/migrations/0006_triagem_respostatriagem_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0006_triagem_respostatriagem_and_more.py>).

``````text
    1 | # Generated by Django 6.1 on 2026-08-28 13:45
    2 | 
    3 | import django.db.models.deletion
    4 | from django.conf import settings
    5 | from django.db import migrations, models
    6 | 
    7 | 
    8 | class Migration(migrations.Migration):
    9 | 
   10 |     dependencies = [
   11 |         ('accounts', '0005_usuario_status_validacao_validacaohemocentro'),
   12 |     ]
   13 | 
   14 |     operations = [
   15 |         migrations.CreateModel(
   16 |             name='Triagem',
   17 |             fields=[
   18 |                 ('id_triagem', models.BigAutoField(primary_key=True, serialize=False)),
   19 |                 ('modalidade', models.CharField(choices=[('EXTENSA', 'Triagem extensa'), ('SIMPLIFICADA', 'Triagem simplificada')], default='EXTENSA', max_length=20)),
   20 |                 ('regra_version', models.CharField(default='HEMOMINAS_2026_08', max_length=40)),
   21 |                 ('resultado', models.CharField(choices=[('SEM_IMPEDIMENTO_IDENTIFICADO', 'Sem impedimento identificado'), ('INAPTIDAO_TEMPORARIA', 'Inaptidão temporária'), ('INAPTIDAO_DEFINITIVA', 'Inaptidão definitiva'), ('AVALIACAO_PRESENCIAL', 'Avaliação presencial'), ('DOCUMENTACAO_ESPECIAL', 'Documentação especial')], max_length=30)),
   22 |                 ('mensagem_resultado', models.TextField()),
   23 |                 ('data_liberacao', models.DateField(blank=True, null=True)),
   24 |                 ('achados', models.JSONField(blank=True, default=list)),
   25 |                 ('iniciada_em', models.DateTimeField(auto_now_add=True)),
   26 |                 ('finalizada_em', models.DateTimeField(blank=True, null=True)),
   27 |                 ('usuario', models.ForeignKey(db_column='id_usuario', on_delete=django.db.models.deletion.CASCADE, related_name='triagens', to=settings.AUTH_USER_MODEL)),
   28 |             ],
   29 |             options={
   30 |                 'db_table': 'triagens',
   31 |                 'ordering': ['-iniciada_em'],
   32 |             },
   33 |         ),
   34 |         migrations.CreateModel(
   35 |             name='RespostaTriagem',
   36 |             fields=[
   37 |                 ('id_resposta', models.BigAutoField(primary_key=True, serialize=False)),
   38 |                 ('id_pergunta', models.CharField(max_length=20)),
   39 |                 ('codigo_resposta', models.CharField(max_length=80)),
   40 |                 ('resposta_label', models.CharField(max_length=255)),
   41 |                 ('data_evento', models.DateField(blank=True, db_column='event_date', null=True)),
   42 |                 ('metadata', models.JSONField(blank=True, default=dict)),
   43 |                 ('rule_version', models.CharField(default='HEMOMINAS_2026_08', max_length=40)),
   44 |                 ('source_ref', models.CharField(blank=True, default='', max_length=255)),
   45 |                 ('respondido_em', models.DateTimeField(auto_now_add=True)),
   46 |                 ('triagem', models.ForeignKey(db_column='id_triagem', on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='accounts.triagem')),
   47 |             ],
   48 |             options={
   49 |                 'db_table': 'respostas_triagem',
   50 |                 'ordering': ['id_resposta'],
   51 |             },
   52 |         ),
   53 |         migrations.AddIndex(
   54 |             model_name='triagem',
   55 |             index=models.Index(fields=['usuario', '-iniciada_em'], name='triagem_usuario_data_idx'),
   56 |         ),
   57 |         migrations.AddIndex(
   58 |             model_name='triagem',
   59 |             index=models.Index(fields=['resultado', '-iniciada_em'], name='triagem_resultado_data_idx'),
   60 |         ),
   61 |         migrations.AddIndex(
   62 |             model_name='respostatriagem',
   63 |             index=models.Index(fields=['triagem', 'id_pergunta'], name='resposta_triagem_pergunta_idx'),
   64 |         ),
   65 |     ]
``````

## accounts/migrations/0007_alter_auditoriaacaocritica_acao_estoque_and_more.py

Original: [accounts/migrations/0007_alter_auditoriaacaocritica_acao_estoque_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0007_alter_auditoriaacaocritica_acao_estoque_and_more.py>).

``````text
    1 | # Generated by Django 5.2.17 on 2026-09-04 11:35
    2 | 
    3 | import django.db.models.deletion
    4 | from django.conf import settings
    5 | from django.db import migrations, models
    6 | 
    7 | 
    8 | class Migration(migrations.Migration):
    9 | 
   10 |     dependencies = [
   11 |         ('accounts', '0006_triagem_respostatriagem_and_more'),
   12 |     ]
   13 | 
   14 |     operations = [
   15 |         migrations.AlterField(
   16 |             model_name='auditoriaacaocritica',
   17 |             name='acao',
   18 |             field=models.CharField(choices=[('LOGIN_FALHO', 'Login falho'), ('LOGIN_SUSPEITO', 'Login suspeito'), ('ALTERACAO_PERMISSAO', 'Alteracao de permissao'), ('APROVACAO_HEMOCENTRO', 'Aprovacao de hemocentro'), ('CADASTRO_ESTOQUE', 'Cadastro de estoque'), ('ATUALIZACAO_ESTOQUE', 'Atualizacao de estoque'), ('MODERACAO', 'Moderacao'), ('ACESSO_DADOS_SENSIVEIS', 'Acesso a dados sensiveis'), ('CONFIRMACAO_DOACAO', 'Confirmacao de doacao')], max_length=40),
   19 |         ),
   20 |         migrations.CreateModel(
   21 |             name='Estoque',
   22 |             fields=[
   23 |                 ('id_estoque', models.BigAutoField(primary_key=True, serialize=False)),
   24 |                 ('tipo_sanguineo', models.CharField(choices=[('O-', 'O-'), ('O+', 'O+'), ('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('AB-', 'AB-'), ('AB+', 'AB+')], max_length=3)),
   25 |                 ('quantidade_bolsas', models.PositiveIntegerField(default=0)),
   26 |                 ('nivel_minimo', models.PositiveIntegerField()),
   27 |                 ('nivel_critico', models.PositiveIntegerField()),
   28 |                 ('status_calculado', models.CharField(choices=[('CRITICO', 'Crítico'), ('BAIXO', 'Baixo'), ('ESTAVEL', 'Estável')], default='ESTAVEL', max_length=10)),
   29 |                 ('data_atualizacao', models.DateTimeField(auto_now=True)),
   30 |                 ('hemocentro', models.ForeignKey(db_column='id_hemocentro', limit_choices_to={'perfil': 'HEMOCENTRO'}, on_delete=django.db.models.deletion.CASCADE, related_name='estoques', to=settings.AUTH_USER_MODEL)),
   31 |             ],
   32 |             options={
   33 |                 'verbose_name': 'estoque',
   34 |                 'verbose_name_plural': 'estoques',
   35 |                 'db_table': 'estoques',
   36 |                 'ordering': ['hemocentro__nome', 'tipo_sanguineo'],
   37 |             },
   38 |         ),
   39 |         migrations.CreateModel(
   40 |             name='EstoqueMovimentacao',
   41 |             fields=[
   42 |                 ('id_mov', models.BigAutoField(primary_key=True, serialize=False)),
   43 |                 ('tipo_movimento', models.CharField(choices=[('ENTRADA', 'Entrada'), ('SAIDA', 'Saída'), ('AJUSTE', 'Ajuste')], max_length=10)),
   44 |                 ('quantidade_anterior', models.PositiveIntegerField()),
   45 |                 ('quantidade_movimentada', models.IntegerField()),
   46 |                 ('quantidade_nova', models.PositiveIntegerField()),
   47 |                 ('motivo', models.CharField(blank=True, default='', max_length=255)),
   48 |                 ('data_hora', models.DateTimeField(auto_now_add=True)),
   49 |                 ('estoque', models.ForeignKey(db_column='id_estoque', on_delete=django.db.models.deletion.CASCADE, related_name='movimentacoes', to='accounts.estoque')),
   50 |                 ('usuario_resp', models.ForeignKey(blank=True, db_column='id_usuario_resp', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movimentacoes_estoque_realizadas', to=settings.AUTH_USER_MODEL)),
   51 |             ],
   52 |             options={
   53 |                 'verbose_name': 'movimentacao de estoque',
   54 |                 'verbose_name_plural': 'movimentacoes de estoque',
   55 |                 'db_table': 'movimentacoes_estoque',
   56 |                 'ordering': ['-data_hora'],
   57 |             },
   58 |         ),
   59 |         migrations.AddIndex(
   60 |             model_name='estoque',
   61 |             index=models.Index(fields=['hemocentro', 'tipo_sanguineo'], name='estoque_hemo_tipo_idx'),
   62 |         ),
   63 |         migrations.AddIndex(
   64 |             model_name='estoque',
   65 |             index=models.Index(fields=['status_calculado'], name='estoque_status_idx'),
   66 |         ),
   67 |         migrations.AddConstraint(
   68 |             model_name='estoque',
   69 |             constraint=models.UniqueConstraint(fields=('hemocentro', 'tipo_sanguineo'), name='estoque_unico_por_hemocentro_tipo'),
   70 |         ),
   71 |         migrations.AddIndex(
   72 |             model_name='estoquemovimentacao',
   73 |             index=models.Index(fields=['estoque', '-data_hora'], name='mov_estoque_data_idx'),
   74 |         ),
   75 |         migrations.AddIndex(
   76 |             model_name='estoquemovimentacao',
   77 |             index=models.Index(fields=['usuario_resp', '-data_hora'], name='mov_usuario_data_idx'),
   78 |         ),
   79 |     ]
``````

## accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py

Original: [accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0007_alter_respostatriagem_options_alter_triagem_options_and_more.py>).

``````text
    1 | # Generated by Django 6.1 on 2026-09-04 12:10
    2 | 
    3 | import django.db.models.deletion
    4 | from django.db import migrations, models
    5 | 
    6 | 
    7 | def preencher_dados_da_triagem(apps, schema_editor):
    8 |     """Converte os registros da versão inicial para os campos novos."""
    9 | 
   10 |     Triagem = apps.get_model("accounts", "Triagem")
   11 |     RespostaTriagem = apps.get_model("accounts", "RespostaTriagem")
   12 | 
   13 |     # Uma triagem antiga com data final já estava concluída.
   14 |     Triagem.objects.filter(
   15 |         finalizada_em__isnull=False,
   16 |     ).update(status="CONCLUIDA")
   17 | 
   18 |     for resposta in RespostaTriagem.objects.all().iterator():
   19 |         # O formato estruturado mantém os dados legados disponíveis.
   20 |         resposta.valor = {
   21 |             "codigos": (
   22 |                 [resposta.codigo_resposta]
   23 |                 if resposta.codigo_resposta
   24 |                 else []
   25 |             ),
   26 |             "data_evento": (
   27 |                 resposta.data_evento.isoformat()
   28 |                 if resposta.data_evento
   29 |                 else None
   30 |             ),
   31 |             "detalhes": resposta.metadata.get("detalhes", ""),
   32 |             "metadata": resposta.metadata,
   33 |         }
   34 |         resposta.save(update_fields=["valor"])
   35 | 
   36 | 
   37 | def limpar_dados_da_triagem(apps, schema_editor):
   38 |     """Permite reverter a migration sem alterar os campos legados."""
   39 | 
   40 |     Triagem = apps.get_model("accounts", "Triagem")
   41 |     RespostaTriagem = apps.get_model("accounts", "RespostaTriagem")
   42 | 
   43 |     Triagem.objects.update(status="EM_ANDAMENTO")
   44 |     RespostaTriagem.objects.update(valor={})
   45 | 
   46 | 
   47 | class Migration(migrations.Migration):
   48 | 
   49 |     dependencies = [
   50 |         ('accounts', '0006_triagem_respostatriagem_and_more'),
   51 |     ]
   52 | 
   53 |     operations = [
   54 |         migrations.AlterModelOptions(
   55 |             name='respostatriagem',
   56 |             options={'ordering': ['id_resposta'], 'verbose_name': 'Resposta triagem', 'verbose_name_plural': 'Respostas triagem'},
   57 |         ),
   58 |         migrations.AlterModelOptions(
   59 |             name='triagem',
   60 |             options={'ordering': ['-iniciada_em'], 'verbose_name': 'Triagem', 'verbose_name_plural': 'Triagens'},
   61 |         ),
   62 |         migrations.AddField(
   63 |             model_name='respostatriagem',
   64 |             name='valor',
   65 |             field=models.JSONField(blank=True, default=dict),
   66 |         ),
   67 |         migrations.AddField(
   68 |             model_name='triagem',
   69 |             name='atualizada_em',
   70 |             field=models.DateTimeField(auto_now=True),
   71 |         ),
   72 |         migrations.AddField(
   73 |             model_name='triagem',
   74 |             name='fluxo_perguntas',
   75 |             field=models.JSONField(blank=True, default=list),
   76 |         ),
   77 |         migrations.AddField(
   78 |             model_name='triagem',
   79 |             name='pergunta_atual',
   80 |             field=models.PositiveIntegerField(default=0),
   81 |         ),
   82 |         migrations.AddField(
   83 |             model_name='triagem',
   84 |             name='status',
   85 |             field=models.CharField(choices=[('EM_ANDAMENTO', 'Em andamento'), ('CONCLUIDA', 'Concluída'), ('CANCELADA', 'Cancelada')], default='EM_ANDAMENTO', max_length=20),
   86 |         ),
   87 |         migrations.AddField(
   88 |             model_name='triagem',
   89 |             name='triagem_base',
   90 |             field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verificacoes_simplificadas', to='accounts.triagem'),
   91 |         ),
   92 |         migrations.RunPython(
   93 |             preencher_dados_da_triagem,
   94 |             limpar_dados_da_triagem,
   95 |         ),
   96 |         migrations.AlterField(
   97 |             model_name='triagem',
   98 |             name='mensagem_resultado',
   99 |             field=models.TextField(blank=True, default=''),
  100 |         ),
  101 |         migrations.AlterField(
  102 |             model_name='triagem',
  103 |             name='resultado',
  104 |             field=models.CharField(blank=True, choices=[('SEM_IMPEDIMENTO_IDENTIFICADO', 'Sem impedimento identificado'), ('INAPTIDAO_TEMPORARIA', 'Inaptidão temporária'), ('INAPTIDAO_DEFINITIVA', 'Inaptidão definitiva'), ('AVALIACAO_PRESENCIAL', 'Avaliação presencial'), ('DOCUMENTACAO_ESPECIAL', 'Documentação especial')], default='', max_length=30),
  105 |         ),
  106 |         migrations.AddConstraint(
  107 |             model_name='respostatriagem',
  108 |             constraint=models.UniqueConstraint(fields=('triagem', 'id_pergunta'), name='resposta_unica_por_pergunta'),
  109 |         ),
  110 |     ]
``````

## accounts/migrations/0008_merge_triagem_estoque_branches.py

Original: [accounts/migrations/0008_merge_triagem_estoque_branches.py](<C:/Users/lb119/Elo/accounts/migrations/0008_merge_triagem_estoque_branches.py>).

``````text
    1 | # Generated manually to reconcile independent accounts migration branches.
    2 | 
    3 | from django.db import migrations
    4 | 
    5 | 
    6 | class Migration(migrations.Migration):
    7 | 
    8 |     dependencies = [
    9 |         (
   10 |             "accounts",
   11 |             "0007_alter_auditoriaacaocritica_acao_estoque_and_more",
   12 |         ),
   13 |         (
   14 |             "accounts",
   15 |             "0007_alter_respostatriagem_options_alter_triagem_options_and_more",
   16 |         ),
   17 |     ]
   18 | 
   19 |     operations = []
``````

## accounts/migrations/0009_usuario_tipo_sanguineo_notificacao.py

Original: [accounts/migrations/0009_usuario_tipo_sanguineo_notificacao.py](<C:/Users/lb119/Elo/accounts/migrations/0009_usuario_tipo_sanguineo_notificacao.py>).

``````text
    1 | # Generated by Django 5.2.17 on 2026-09-10 00:25
    2 | 
    3 | import django.db.models.deletion
    4 | from django.conf import settings
    5 | from django.db import migrations, models
    6 | 
    7 | 
    8 | class Migration(migrations.Migration):
    9 | 
   10 |     dependencies = [
   11 |         ('accounts', '0008_merge_triagem_estoque_branches'),
   12 |     ]
   13 | 
   14 |     operations = [
   15 |         migrations.AddField(
   16 |             model_name='usuario',
   17 |             name='tipo_sanguineo',
   18 |             field=models.CharField(blank=True, choices=[('O-', 'O-'), ('O+', 'O+'), ('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('AB-', 'AB-'), ('AB+', 'AB+')], default='', max_length=3),
   19 |         ),
   20 |         migrations.CreateModel(
   21 |             name='Notificacao',
   22 |             fields=[
   23 |                 ('id_notificacao', models.BigAutoField(primary_key=True, serialize=False)),
   24 |                 ('tipo', models.CharField(choices=[('ESTOQUE_BAIXO', 'Estoque baixo'), ('ESTOQUE_CRITICO', 'Estoque crítico'), ('GERAL', 'Aviso geral')], default='GERAL', max_length=30)),
   25 |                 ('titulo', models.CharField(max_length=120)),
   26 |                 ('mensagem', models.TextField()),
   27 |                 ('url_destino', models.CharField(blank=True, default='', max_length=255)),
   28 |                 ('lida', models.BooleanField(default=False)),
   29 |                 ('criada_em', models.DateTimeField(auto_now_add=True)),
   30 |                 ('lida_em', models.DateTimeField(blank=True, null=True)),
   31 |                 ('estoque', models.ForeignKey(blank=True, db_column='id_estoque', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notificacoes', to='accounts.estoque')),
   32 |                 ('usuario', models.ForeignKey(db_column='id_usuario', on_delete=django.db.models.deletion.CASCADE, related_name='notificacoes', to=settings.AUTH_USER_MODEL)),
   33 |             ],
   34 |             options={
   35 |                 'verbose_name': 'notificacao',
   36 |                 'verbose_name_plural': 'notificacoes',
   37 |                 'db_table': 'notificacoes',
   38 |                 'ordering': ['-criada_em'],
   39 |                 'indexes': [models.Index(fields=['usuario', 'lida', '-criada_em'], name='notificacao_usuario_lida_idx'), models.Index(fields=['tipo', '-criada_em'], name='notificacao_tipo_data_idx')],
   40 |             },
   41 |         ),
   42 |     ]
``````

## accounts/migrations/0010_pedidosangue.py

Original: [accounts/migrations/0010_pedidosangue.py](<C:/Users/lb119/Elo/accounts/migrations/0010_pedidosangue.py>).

``````text
    1 | # Generated by Django 6.1 on 2026-09-10
    2 | 
    3 | import django.db.models.deletion
    4 | from django.conf import settings
    5 | from django.db import migrations, models
    6 | 
    7 | 
    8 | class Migration(migrations.Migration):
    9 | 
   10 |     dependencies = [
   11 |         ("accounts", "0009_usuario_tipo_sanguineo_notificacao"),
   12 |     ]
   13 | 
   14 |     operations = [
   15 |         migrations.CreateModel(
   16 |             name="PedidoSangue",
   17 |             fields=[
   18 |                 (
   19 |                     "id_pedido",
   20 |                     models.BigAutoField(primary_key=True, serialize=False),
   21 |                 ),
   22 |                 (
   23 |                     "para_quem",
   24 |                     models.CharField(
   25 |                         choices=[
   26 |                             ("MIM", "Para mim"),
   27 |                             ("OUTRA_PESSOA", "Para outra pessoa"),
   28 |                         ],
   29 |                         max_length=20,
   30 |                     ),
   31 |                 ),
   32 |                 (
   33 |                     "tipo_sanguineo",
   34 |                     models.CharField(
   35 |                         choices=[
   36 |                             ("O-", "O-"),
   37 |                             ("O+", "O+"),
   38 |                             ("A-", "A-"),
   39 |                             ("A+", "A+"),
   40 |                             ("B-", "B-"),
   41 |                             ("B+", "B+"),
   42 |                             ("AB-", "AB-"),
   43 |                             ("AB+", "AB+"),
   44 |                         ],
   45 |                         max_length=3,
   46 |                     ),
   47 |                 ),
   48 |                 ("cidade", models.CharField(max_length=100)),
   49 |                 (
   50 |                     "urgencia",
   51 |                     models.CharField(
   52 |                         choices=[
   53 |                             ("NORMAL", "Normal"),
   54 |                             ("URGENTE", "Urgente"),
   55 |                             ("CRITICO", "Crítico"),
   56 |                         ],
   57 |                         max_length=10,
   58 |                     ),
   59 |                 ),
   60 |                 (
   61 |                     "nome_paciente",
   62 |                     models.CharField(
   63 |                         blank=True,
   64 |                         default="",
   65 |                         max_length=150,
   66 |                     ),
   67 |                 ),
   68 |                 ("descricao", models.TextField(max_length=500)),
   69 |                 (
   70 |                     "status",
   71 |                     models.CharField(
   72 |                         choices=[
   73 |                             ("PENDENTE", "Pendente"),
   74 |                             ("ATIVO", "Ativo"),
   75 |                             ("RECUSADO", "Recusado"),
   76 |                             ("ATENDIDO", "Atendido"),
   77 |                             ("EXPIRADO", "Expirado"),
   78 |                         ],
   79 |                         default="PENDENTE",
   80 |                         max_length=10,
   81 |                     ),
   82 |                 ),
   83 |                 ("data_criacao", models.DateTimeField(auto_now_add=True)),
   84 |                 ("data_fechamento", models.DateTimeField(blank=True, null=True)),
   85 |                 (
   86 |                     "hemocentro",
   87 |                     models.ForeignKey(
   88 |                         db_column="id_hemocentro",
   89 |                         limit_choices_to={"perfil": "HEMOCENTRO"},
   90 |                         on_delete=django.db.models.deletion.PROTECT,
   91 |                         related_name="pedidos_de_destino",
   92 |                         to=settings.AUTH_USER_MODEL,
   93 |                     ),
   94 |                 ),
   95 |                 (
   96 |                     "solicitante",
   97 |                     models.ForeignKey(
   98 |                         db_column="id_solicitante",
   99 |                         on_delete=django.db.models.deletion.PROTECT,
  100 |                         related_name="pedidos_publicados",
  101 |                         to=settings.AUTH_USER_MODEL,
  102 |                     ),
  103 |                 ),
  104 |             ],
  105 |             options={
  106 |                 "verbose_name": "pedido de sangue",
  107 |                 "verbose_name_plural": "pedidos de sangue",
  108 |                 "db_table": "pedidos_sangue",
  109 |                 "ordering": ["-data_criacao"],
  110 |                 "indexes": [
  111 |                     models.Index(
  112 |                         fields=["status", "-data_criacao"],
  113 |                         name="pedido_sangue_status_idx",
  114 |                     ),
  115 |                     models.Index(
  116 |                         fields=["cidade", "tipo_sanguineo"],
  117 |                         name="pedido_sangue_busca_idx",
  118 |                     ),
  119 |                 ],
  120 |             },
  121 |         ),
  122 |     ]
``````

## accounts/migrations/0011_alinhar_pedidos_validacao.py

Original: [accounts/migrations/0011_alinhar_pedidos_validacao.py](<C:/Users/lb119/Elo/accounts/migrations/0011_alinhar_pedidos_validacao.py>).

``````text
    1 | import django.db.models.deletion
    2 | import django.utils.timezone
    3 | from django.conf import settings
    4 | from django.db import migrations, models
    5 | 
    6 | 
    7 | def converter_valores_legados(apps, schema_editor):
    8 |     PedidoSangue = apps.get_model("accounts", "PedidoSangue")
    9 | 
   10 |     conversoes_urgencia = {
   11 |         "NORMAL": "BAIXA",
   12 |         "URGENTE": "ALTA",
   13 |         "CRITICO": "CRITICA",
   14 |     }
   15 |     conversoes_status = {
   16 |         "PENDENTE": "PENDENTE_VALIDACAO",
   17 |         "ATENDIDO": "ENCERRADO",
   18 |         "EXPIRADO": "ENCERRADO",
   19 |     }
   20 | 
   21 |     for valor_antigo, valor_novo in conversoes_urgencia.items():
   22 |         PedidoSangue.objects.filter(urgencia=valor_antigo).update(
   23 |             urgencia=valor_novo
   24 |         )
   25 | 
   26 |     for valor_antigo, valor_novo in conversoes_status.items():
   27 |         PedidoSangue.objects.filter(status=valor_antigo).update(
   28 |             status=valor_novo
   29 |         )
   30 | 
   31 | 
   32 | class Migration(migrations.Migration):
   33 | 
   34 |     dependencies = [
   35 |         ("accounts", "0010_pedidosangue"),
   36 |     ]
   37 | 
   38 |     operations = [
   39 |         migrations.RenameField(
   40 |             model_name="pedidosangue",
   41 |             old_name="hemocentro",
   42 |             new_name="hemocentro_destino",
   43 |         ),
   44 |         migrations.AlterField(
   45 |             model_name="pedidosangue",
   46 |             name="hemocentro_destino",
   47 |             field=models.ForeignKey(
   48 |                 db_column="id_hemocentro_destino",
   49 |                 limit_choices_to={"perfil": "HEMOCENTRO"},
   50 |                 on_delete=django.db.models.deletion.PROTECT,
   51 |                 related_name="pedidos_recebidos",
   52 |                 to=settings.AUTH_USER_MODEL,
   53 |             ),
   54 |         ),
   55 |         migrations.AddField(
   56 |             model_name="pedidosangue",
   57 |             name="titulo",
   58 |             field=models.CharField(
   59 |                 default="Pedido de sangue",
   60 |                 max_length=150,
   61 |             ),
   62 |         ),
   63 |         migrations.AddField(
   64 |             model_name="pedidosangue",
   65 |             name="justificativa_urgencia",
   66 |             field=models.TextField(blank=True, default=""),
   67 |         ),
   68 |         migrations.AddField(
   69 |             model_name="pedidosangue",
   70 |             name="atualizado_em",
   71 |             field=models.DateTimeField(
   72 |                 auto_now=True,
   73 |                 default=django.utils.timezone.now,
   74 |             ),
   75 |             preserve_default=False,
   76 |         ),
   77 |         migrations.AlterField(
   78 |             model_name="pedidosangue",
   79 |             name="descricao",
   80 |             field=models.TextField(),
   81 |         ),
   82 |         migrations.AlterField(
   83 |             model_name="pedidosangue",
   84 |             name="solicitante",
   85 |             field=models.ForeignKey(
   86 |                 db_column="id_solicitante",
   87 |                 on_delete=django.db.models.deletion.CASCADE,
   88 |                 related_name="pedidos_sangue",
   89 |                 to=settings.AUTH_USER_MODEL,
   90 |             ),
   91 |         ),
   92 |         migrations.AlterField(
   93 |             model_name="pedidosangue",
   94 |             name="urgencia",
   95 |             field=models.CharField(
   96 |                 choices=[
   97 |                     ("BAIXA", "Baixa"),
   98 |                     ("MEDIA", "Media"),
   99 |                     ("ALTA", "Alta"),
  100 |                     ("CRITICA", "Critica"),
  101 |                 ],
  102 |                 max_length=10,
  103 |             ),
  104 |         ),
  105 |         migrations.AlterField(
  106 |             model_name="pedidosangue",
  107 |             name="status",
  108 |             field=models.CharField(
  109 |                 choices=[
  110 |                     (
  111 |                         "PENDENTE_VALIDACAO",
  112 |                         "Pendente de validacao",
  113 |                     ),
  114 |                     ("ATIVO", "Ativo"),
  115 |                     ("SUSPEITO", "Suspeito"),
  116 |                     ("RECUSADO", "Recusado"),
  117 |                     ("ENCERRADO", "Encerrado"),
  118 |                 ],
  119 |                 default="PENDENTE_VALIDACAO",
  120 |                 max_length=30,
  121 |             ),
  122 |         ),
  123 |         migrations.RunPython(
  124 |             converter_valores_legados,
  125 |             migrations.RunPython.noop,
  126 |         ),
  127 |         migrations.RemoveIndex(
  128 |             model_name="pedidosangue",
  129 |             name="pedido_sangue_status_idx",
  130 |         ),
  131 |         migrations.RemoveIndex(
  132 |             model_name="pedidosangue",
  133 |             name="pedido_sangue_busca_idx",
  134 |         ),
  135 |         migrations.AddIndex(
  136 |             model_name="pedidosangue",
  137 |             index=models.Index(
  138 |                 fields=["status", "-data_criacao"],
  139 |                 name="pedido_status_data_idx",
  140 |             ),
  141 |         ),
  142 |         migrations.AddIndex(
  143 |             model_name="pedidosangue",
  144 |             index=models.Index(
  145 |                 fields=["tipo_sanguineo", "urgencia"],
  146 |                 name="pedido_tipo_urg_idx",
  147 |             ),
  148 |         ),
  149 |         migrations.AddIndex(
  150 |             model_name="pedidosangue",
  151 |             index=models.Index(
  152 |                 fields=["cidade"],
  153 |                 name="pedido_cidade_idx",
  154 |             ),
  155 |         ),
  156 |         migrations.CreateModel(
  157 |             name="ValidacaoPedido",
  158 |             fields=[
  159 |                 (
  160 |                     "id_validacao",
  161 |                     models.BigAutoField(
  162 |                         primary_key=True,
  163 |                         serialize=False,
  164 |                     ),
  165 |                 ),
  166 |                 (
  167 |                     "status_validacao",
  168 |                     models.CharField(
  169 |                         choices=[
  170 |                             ("APROVADO", "Aprovado"),
  171 |                             ("SUSPEITO", "Suspeito"),
  172 |                             ("RECUSADO", "Recusado"),
  173 |                         ],
  174 |                         max_length=20,
  175 |                     ),
  176 |                 ),
  177 |                 (
  178 |                     "motivo",
  179 |                     models.TextField(blank=True, default=""),
  180 |                 ),
  181 |                 (
  182 |                     "data_validacao",
  183 |                     models.DateTimeField(auto_now_add=True),
  184 |                 ),
  185 |                 (
  186 |                     "moderador",
  187 |                     models.ForeignKey(
  188 |                         blank=True,
  189 |                         db_column="id_moderador",
  190 |                         null=True,
  191 |                         on_delete=django.db.models.deletion.SET_NULL,
  192 |                         related_name="validacoes_pedido_realizadas",
  193 |                         to=settings.AUTH_USER_MODEL,
  194 |                     ),
  195 |                 ),
  196 |                 (
  197 |                     "pedido",
  198 |                     models.ForeignKey(
  199 |                         db_column="id_pedido",
  200 |                         on_delete=django.db.models.deletion.CASCADE,
  201 |                         related_name="validacoes",
  202 |                         to="accounts.pedidosangue",
  203 |                     ),
  204 |                 ),
  205 |             ],
  206 |             options={
  207 |                 "db_table": "validacoes_pedido",
  208 |                 "ordering": ["-data_validacao"],
  209 |             },
  210 |         ),
  211 |     ]
``````

## accounts/migrations/0012_pedidosangue_contato_and_more.py

Original: [accounts/migrations/0012_pedidosangue_contato_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0012_pedidosangue_contato_and_more.py>).

``````text
    1 | # Generated by Django 6.1 on 2026-10-07 17:25
    2 | 
    3 | import django.db.models.deletion
    4 | from django.conf import settings
    5 | from django.db import migrations, models
    6 | 
    7 | 
    8 | def alinhar_status_legados(apps, schema_editor):
    9 |     PedidoSangue = apps.get_model("accounts", "PedidoSangue")
   10 |     Triagem = apps.get_model("accounts", "Triagem")
   11 | 
   12 |     PedidoSangue.objects.filter(status="PENDENTE_VALIDACAO").update(
   13 |         status="ENVIADA"
   14 |     )
   15 |     PedidoSangue.objects.filter(status="ATIVO").update(status="PUBLICADA")
   16 |     PedidoSangue.objects.filter(status="SUSPEITO").update(status="EM_ANALISE")
   17 |     PedidoSangue.objects.filter(status="RECUSADO").update(status="RECUSADA")
   18 |     PedidoSangue.objects.filter(status="ENCERRADO").update(status="ENCERRADA")
   19 | 
   20 | 
   21 | 
   22 | class Migration(migrations.Migration):
   23 | 
   24 |     dependencies = [
   25 |         ('accounts', '0011_alinhar_pedidos_validacao'),
   26 |     ]
   27 | 
   28 |     operations = [
   29 |         migrations.RunPython(alinhar_status_legados, migrations.RunPython.noop),
   30 |         migrations.AddField(
   31 |             model_name='pedidosangue',
   32 |             name='contato',
   33 |             field=models.CharField(default='', max_length=120),
   34 |         ),
   35 |         migrations.AddField(
   36 |             model_name='pedidosangue',
   37 |             name='duplicidade_suspeita',
   38 |             field=models.BooleanField(default=False),
   39 |         ),
   40 |         migrations.AddField(
   41 |             model_name='pedidosangue',
   42 |             name='informacoes_complementares',
   43 |             field=models.TextField(blank=True, default=''),
   44 |         ),
   45 |         migrations.AddField(
   46 |             model_name='pedidosangue',
   47 |             name='nome_solicitante',
   48 |             field=models.CharField(default='', max_length=150),
   49 |         ),
   50 |         migrations.AddField(
   51 |             model_name='pedidosangue',
   52 |             name='publicado_em',
   53 |             field=models.DateTimeField(blank=True, null=True),
   54 |         ),
   55 |         migrations.AddField(
   56 |             model_name='pedidosangue',
   57 |             name='publicado_por',
   58 |             field=models.ForeignKey(blank=True, db_column='id_publicado_por', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pedidos_publicados', to=settings.AUTH_USER_MODEL),
   59 |         ),
   60 |         migrations.AddField(
   61 |             model_name='usuario',
   62 |             name='tipo_sanguineo_confirmado',
   63 |             field=models.BooleanField(default=False),
   64 |         ),
   65 |         migrations.AlterField(
   66 |             model_name='pedidosangue',
   67 |             name='solicitante',
   68 |             field=models.ForeignKey(blank=True, db_column='id_solicitante', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pedidos_sangue', to=settings.AUTH_USER_MODEL),
   69 |         ),
   70 |         migrations.AlterField(
   71 |             model_name='pedidosangue',
   72 |             name='status',
   73 |             field=models.CharField(choices=[('ENVIADA', 'Enviada'), ('EM_ANALISE', 'Em análise'), ('PUBLICADA', 'Publicada'), ('CORRECAO_SOLICITADA', 'Correção solicitada'), ('RECUSADA', 'Recusada'), ('ENCERRADA', 'Encerrada')], default='ENVIADA', max_length=30),
   74 |         ),
   75 |         migrations.AlterField(
   76 |             model_name='triagem',
   77 |             name='resultado',
   78 |             field=models.CharField(blank=True, choices=[('SEM_IMPEDIMENTO_IDENTIFICADO', 'Apto'), ('INAPTIDAO_TEMPORARIA', 'Inaptidão temporária'), ('INAPTIDAO_DEFINITIVA', 'Inaptidão definitiva'), ('AVALIACAO_PRESENCIAL', 'Avaliação presencial necessária'), ('DOCUMENTACAO_ESPECIAL', 'Documentação especial')], default='', max_length=40),
   79 |         ),
   80 |         migrations.AlterField(
   81 |             model_name='validacaopedido',
   82 |             name='status_validacao',
   83 |             field=models.CharField(choices=[('APROVADO', 'Aprovado'), ('CORRECAO_SOLICITADA', 'Correção solicitada'), ('SUSPEITO', 'Suspeito'), ('RECUSADO', 'Recusado')], max_length=20),
   84 |         ),
   85 |     ]
``````

## accounts/migrations/0013_usuario_suspensa.py

Original: [accounts/migrations/0013_usuario_suspensa.py](<C:/Users/lb119/Elo/accounts/migrations/0013_usuario_suspensa.py>).

``````text
    1 | # Generated by Django 6.1 on 2026-10-07 17:28
    2 | 
    3 | from django.db import migrations, models
    4 | 
    5 | 
    6 | class Migration(migrations.Migration):
    7 | 
    8 |     dependencies = [
    9 |         ('accounts', '0012_pedidosangue_contato_and_more'),
   10 |     ]
   11 | 
   12 |     operations = [
   13 |         migrations.AddField(
   14 |             model_name='usuario',
   15 |             name='suspensa',
   16 |             field=models.BooleanField(default=False),
   17 |         ),
   18 |     ]
``````

## accounts/migrations/0014_notificacao_pedido_and_more.py

Original: [accounts/migrations/0014_notificacao_pedido_and_more.py](<C:/Users/lb119/Elo/accounts/migrations/0014_notificacao_pedido_and_more.py>).

``````text
    1 | # Generated by Django 6.1 on 2026-10-07 17:29
    2 | 
    3 | import django.db.models.deletion
    4 | from django.db import migrations, models
    5 | 
    6 | 
    7 | class Migration(migrations.Migration):
    8 | 
    9 |     dependencies = [
   10 |         ('accounts', '0013_usuario_suspensa'),
   11 |     ]
   12 | 
   13 |     operations = [
   14 |         migrations.AddField(
   15 |             model_name='notificacao',
   16 |             name='pedido',
   17 |             field=models.ForeignKey(blank=True, db_column='id_pedido', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notificacoes', to='accounts.pedidosangue'),
   18 |         ),
   19 |         migrations.AddField(
   20 |             model_name='usuario',
   21 |             name='aceita_notificacoes_pedidos',
   22 |             field=models.BooleanField(default=True),
   23 |         ),
   24 |         migrations.AlterField(
   25 |             model_name='notificacao',
   26 |             name='tipo',
   27 |             field=models.CharField(choices=[('ESTOQUE_BAIXO', 'Estoque baixo'), ('ESTOQUE_CRITICO', 'Estoque crítico'), ('PEDIDO_COMPATIVEL', 'Pedido compatível'), ('GERAL', 'Aviso geral')], default='GERAL', max_length=30),
   28 |         ),
   29 |     ]
``````

## accounts/migrations/0015_pedido_contato_email.py

Original: [accounts/migrations/0015_pedido_contato_email.py](<C:/Users/lb119/Elo/accounts/migrations/0015_pedido_contato_email.py>).

``````text
    1 | # Generated by Django 6.1 on 2026-10-07 18:16
    2 | 
    3 | from django.db import migrations, models
    4 | 
    5 | 
    6 | class Migration(migrations.Migration):
    7 | 
    8 |     dependencies = [
    9 |         ('accounts', '0014_notificacao_pedido_and_more'),
   10 |     ]
   11 | 
   12 |     operations = [
   13 |         migrations.AlterField(
   14 |             model_name='pedidosangue',
   15 |             name='contato',
   16 |             field=models.EmailField(default='', max_length=120),
   17 |         ),
   18 |     ]
``````

## accounts/migrations/README.md

Original: [accounts/migrations/README.md](<C:/Users/lb119/Elo/accounts/migrations/README.md>).

``````text
    1 | # Como as migrations funcionam
    2 | 
    3 | Esta pasta guarda o historico da estrutura do banco de dados. Pense nela como
    4 | uma lista numerada de alteracoes que o Django executa na ordem.
    5 | 
    6 | ## Historico atual
    7 | 
    8 | - `0001_initial.py`: criou as tabelas iniciais, incluindo os campos completos
    9 |   do usuario e a tabela de consentimentos;
   10 | - `0002_remove_usuario_cidade_remove_usuario_cnpj_and_more.py`: registrou uma
   11 |   simplificacao temporaria do model;
   12 | - `0003_usuario_cidade_usuario_cnpj_usuario_cpf_and_more.py`: restaurou os
   13 |   campos completos quando ficou definido que a funcionalidade deveria ser
   14 |   mantida, mas explicada de maneira mais simples.
   15 | 
   16 | As migrations `0002` e `0003` devem continuar no projeto. Embora uma retire e a
   17 | outra recoloque campos, elas representam o que realmente aconteceu no banco.
   18 | Apagar ou reescrever uma migration ja aplicada pode deixar o codigo e o banco
   19 | em estados diferentes.
   20 | 
   21 | ## Comandos usados
   22 | 
   23 | Depois de alterar `models.py`, o fluxo correto e:
   24 | 
   25 | ```powershell
   26 | python manage.py makemigrations
   27 | python manage.py migrate
   28 | ```
   29 | 
   30 | `makemigrations` compara o model atual com o ultimo estado conhecido e cria um
   31 | novo arquivo numerado. Ele prepara a alteracao, mas ainda nao mexe nas tabelas.
   32 | 
   33 | `migrate` le os arquivos numerados e executa no PostgreSQL os comandos SQL
   34 | necessarios. O Django registra o que ja foi aplicado na tabela interna
   35 | `django_migrations`, evitando executar a mesma migration duas vezes.
   36 | 
   37 | Em outro computador, depois de clonar o repositorio e configurar o `.env`, a
   38 | pessoa precisa executar somente:
   39 | 
   40 | ```powershell
   41 | python manage.py migrate
   42 | ```
   43 | 
   44 | O Django aplicara automaticamente todas as migrations que ainda estiverem
   45 | pendentes.
   46 | 
   47 | ## Relacao com o codigo
   48 | 
   49 | - `models.py` descreve como as tabelas devem estar na versao atual;
   50 | - as migrations descrevem o caminho usado para chegar a essa versao;
   51 | - o PostgreSQL guarda as tabelas e os dados reais;
   52 | - o ORM do Django transforma chamadas Python em consultas SQL.
   53 | 
   54 | Exemplo: `Usuario.objects.filter(email=email)` vira uma consulta `SELECT` na
   55 | tabela `usuarios`. `usuario.save()` pode virar `INSERT` ou `UPDATE`, dependendo
   56 | de o objeto ser novo ou ja existir.
   57 | 
   58 | Operacoes comuns em uma migration:
   59 | 
   60 | - `CreateModel`: cria uma tabela;
   61 | - `AddField`: adiciona uma coluna;
   62 | - `RemoveField`: remove uma coluna;
   63 | - `AlterField`: altera uma coluna;
   64 | - `AddConstraint`: cria uma regra no banco, como uma combinacao unica.
   65 | 
   66 | Os arquivos numerados sao gerados pelo Django e normalmente nao devem receber
   67 | comentarios manuais. Este README explica a logica da pasta sem modificar o
   68 | historico executavel.
``````

## accounts/migrations/__init__.py

Original: [accounts/migrations/__init__.py](<C:/Users/lb119/Elo/accounts/migrations/__init__.py>).

``````text
    1 | """
    2 | Marca ``accounts.migrations`` como pacote Python.
    3 | 
    4 | Os arquivos numerados desta pasta sao gerados por ``makemigrations`` e guardam
    5 | o historico de alteracoes da estrutura do banco.
    6 | """
``````

## accounts/models.py

Original: [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py>).

``````text
    1 | """
    2 | Resumo Do Arquivo
    3 | =================
    4 | 
    5 | Este arquivo descreve os dados que o Django guarda no PostgreSQL.
    6 | 
    7 | - Usuario: guarda a conta, os dados basicos, o tipo de perfil escolhido e o
    8 |   status atual de validacao quando a conta e de Hemocentro.
    9 | 
   10 | - ValidacaoHemocentro: guarda o historico de analises feitas por administradores.
   11 | 
   12 | - ConsentimentoLGPD: guarda quando a pessoa aceitou cada termo.
   13 | 
   14 | - AuditoriaAcaoCritica: registra eventos sensiveis para rastreabilidade.
   15 | 
   16 | O usuario herda de AbstractUser para aproveitar senha segura, login, sessao,
   17 | grupos e permissoes do Django. Mesmo herdando de uma classe chamada
   18 | AbstractUser, a classe Usuario abaixo e concreta e cria a tabela ``usuarios``
   19 | porque nao foi marcado como abstrato.
   20 | 
   21 | O campo perfil identifica Doador, Receptor/Solicitante, Hemocentro,
   22 | Observador ou Administrador. As views usam esse valor para montar a experiencia
   23 | inicial de cada tipo de usuario no dashboard.
   24 | """
   25 | 
   26 | from django.conf import settings
   27 | from django.contrib.auth.base_user import BaseUserManager
   28 | from django.contrib.auth.models import AbstractUser
   29 | from django.core.exceptions import ValidationError
   30 | from django.db import models
   31 | 
   32 | # Reaproveita a mesma lista de tipos sanguineos usada em compatibilidade.py,
   33 | # para nao correr o risco de duas listas divergentes no projeto.
   34 | from .compatibilidade import TIPOS_SANGUINEOS
   35 | 
   36 | 
   37 | class UsuarioManager(BaseUserManager):
   38 |     """
   39 |     Centraliza a criacao das contas.
   40 | 
   41 |     O Django normalmente cria usuarios por username. O Elo usa e-mail, entao
   42 |     este manager ensina ``Usuario.objects`` a receber, padronizar e salvar o
   43 |     e-mail corretamente tanto para contas comuns quanto para administradores.
   44 |     """
   45 | 
   46 |     use_in_migrations = True
   47 | 
   48 |     def create_user(self, email, password=None, **extra_fields):
   49 |         """Cria uma conta comum e grava a senha de forma segura."""
   50 | 
   51 |         if not email:
   52 |             raise ValueError("O e-mail e obrigatorio.")
   53 | 
   54 |         # Padroniza o e-mail para evitar diferencas por letras maiusculas.
   55 |         # Exemplo: MARIA@EXAMPLE.COM e maria@example.com viram o mesmo padrao.
   56 |         email = self.normalize_email(email).lower()
   57 | 
   58 |         usuario = self.model(email=email, **extra_fields)
   59 |         usuario.set_password(password)
   60 |         usuario.save(using=self._db)
   61 | 
   62 |         return usuario
   63 | 
   64 |     def create_superuser(self, email, password=None, **extra_fields):
   65 |         """Cria a conta tecnica que pode acessar o painel /admin/."""
   66 | 
   67 |         extra_fields.setdefault("is_staff", True)
   68 |         extra_fields.setdefault("is_superuser", True)
   69 |         extra_fields.setdefault("is_active", True)
   70 |         extra_fields.setdefault("perfil", self.model.Perfil.ADMINISTRADOR)
   71 | 
   72 |         if extra_fields.get("is_staff") is not True:
   73 |             raise ValueError("O superusuario precisa ter is_staff=True.")
   74 | 
   75 |         if extra_fields.get("is_superuser") is not True:
   76 |             raise ValueError("O superusuario precisa ter is_superuser=True.")
   77 | 
   78 |         return self.create_user(email, password, **extra_fields)
   79 | 
   80 | 
   81 | class Usuario(AbstractUser):
   82 |     """
   83 |     Conta concreta do Elo, com login por e-mail.
   84 | 
   85 |     AbstractUser fornece recursos prontos e testados: hash de senha, ultimo
   86 |     login, grupos, permissoes e compatibilidade com o admin. A palavra
   87 |     "Abstract" pertence a classe de origem; ``Usuario`` e concreto e cria a
   88 |     tabela real ``usuarios`` porque nao foi marcado como abstrato.
   89 |     """
   90 | 
   91 |     class Perfil(models.TextChoices):
   92 |         """Tipos que podem ser escolhidos no cadastro."""
   93 | 
   94 |         DOADOR = "DOADOR", "Doador"
   95 |         RECEPTOR = "RECEPTOR", "Receptor"
   96 |         HEMOCENTRO = "HEMOCENTRO", "Hemocentro"
   97 |         OBSERVADOR = "OBSERVADOR", "Observador"
   98 |         ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
   99 | 
  100 |     class Sexo(models.TextChoices):
  101 |         """Opcoes fechadas para manter os dados padronizados."""
  102 | 
  103 |         FEMININO = "F", "Feminino"
  104 |         MASCULINO = "M", "Masculino"
  105 |         OUTRO = "O", "Outro"
  106 |         NAO_INFORMADO = "N", "Prefiro nao informar"
  107 | 
  108 |     class StatusValidacaoHemocentro(models.TextChoices):
  109 |         """Situacao institucional do Hemocentro dentro do Elo."""
  110 | 
  111 |         PENDENTE = "PENDENTE", "Pendente"
  112 |         APROVADO = "APROVADO", "Aprovado"
  113 |         RECUSADO = "RECUSADO", "Recusado"
  114 |         CORRECAO = "CORRECAO", "Correcao necessaria"
  115 | 
  116 |     username = None
  117 |     first_name = None
  118 |     last_name = None
  119 | 
  120 |     id_usuario = models.BigAutoField(primary_key=True)
  121 | 
  122 |     nome = models.CharField(max_length=150)
  123 |     email = models.EmailField(unique=True)
  124 |     password = models.CharField(max_length=128, db_column="senha_hash")
  125 | 
  126 |     cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
  127 |     cnpj = models.CharField(max_length=14, unique=True, null=True, blank=True)
  128 | 
  129 |     telefone = models.CharField(max_length=20, blank=True, default="")
  130 |     data_nascimento = models.DateField(null=True, blank=True)
  131 | 
  132 |     sexo = models.CharField(
  133 |         max_length=1,
  134 |         choices=Sexo.choices,
  135 |         blank=True,
  136 |         default="",
  137 |     )
  138 | 
  139 |     tipo_sanguineo = models.CharField(
  140 |         max_length=3,
  141 |         choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
  142 |         blank=True,
  143 |         default="",
  144 |     )
  145 | 
  146 |     # Quando um Hemocentro confirma o tipo, ele deixa de ser editável pela
  147 |     # triagem/autopreenchimento do usuário.
  148 |     tipo_sanguineo_confirmado = models.BooleanField(default=False)
  149 | 
  150 |     cidade = models.CharField(max_length=100, blank=True, default="")
  151 |     estado = models.CharField(max_length=2, blank=True, default="")
  152 | 
  153 |     perfil = models.CharField(
  154 |         max_length=20,
  155 |         choices=Perfil.choices,
  156 |         default=Perfil.OBSERVADOR,
  157 |     )
  158 | 
  159 |     status_validacao = models.CharField(
  160 |         max_length=20,
  161 |         choices=StatusValidacaoHemocentro.choices,
  162 |         default=StatusValidacaoHemocentro.PENDENTE,
  163 |     )
  164 | 
  165 |     is_active = models.BooleanField(default=True, db_column="ativo")
  166 |     suspensa = models.BooleanField(default=False)
  167 |     aceita_notificacoes_pedidos = models.BooleanField(default=True)
  168 |     email_verificado = models.BooleanField(default=False)
  169 | 
  170 |     date_joined = models.DateTimeField(
  171 |         auto_now_add=True,
  172 |         db_column="data_cadastro",
  173 |     )
  174 | 
  175 |     atualizado_em = models.DateTimeField(auto_now=True)
  176 |     objects = UsuarioManager()
  177 | 
  178 |     USERNAME_FIELD = "email"
  179 |     REQUIRED_FIELDS = ["nome"]
  180 | 
  181 |     class Meta:
  182 |         db_table = "usuarios"
  183 |         verbose_name = "usuario"
  184 |         verbose_name_plural = "usuarios"
  185 |         ordering = ["nome"]
  186 | 
  187 |     def clean(self):
  188 |         """Padroniza o e-mail quando o model e validado."""
  189 | 
  190 |         super().clean()
  191 | 
  192 |         if self.email:
  193 |             self.email = self.__class__.objects.normalize_email(self.email).lower()
  194 | 
  195 |     def get_full_name(self):
  196 |         """Devolve o nome completo no formato esperado pelo Django."""
  197 | 
  198 |         return self.nome
  199 | 
  200 |     def get_short_name(self):
  201 |         """Devolve o primeiro nome para saudacoes."""
  202 | 
  203 |         return self.nome.split()[0] if self.nome else self.email
  204 | 
  205 |     @property
  206 |     def is_hemocentro(self):
  207 |         """Informa se a conta representa um Hemocentro cadastrado."""
  208 | 
  209 |         return self.perfil == self.Perfil.HEMOCENTRO
  210 | 
  211 |     @property
  212 |     def hemocentro_aprovado(self):
  213 |         """Atalho usado pelas regras de publicacao de estoque e campanha."""
  214 | 
  215 |         return (
  216 |             self.is_hemocentro
  217 |             and self.status_validacao == self.StatusValidacaoHemocentro.APROVADO
  218 |         )
  219 | 
  220 |     def __str__(self):
  221 |         """Texto usado para representar o usuario no admin e no terminal."""
  222 | 
  223 |         return f"{self.nome} ({self.email})"
  224 | 
  225 | 
  226 | class ValidacaoHemocentro(models.Model):
  227 |     """
  228 |     Historico das analises institucionais de Hemocentros.
  229 | 
  230 |     A tabela registra cada decisao administrativa sem substituir as anteriores.
  231 |     O status atual continua em Usuario.status_validacao para consultas rapidas.
  232 |     """
  233 | 
  234 |     id_validacao = models.BigAutoField(primary_key=True)
  235 | 
  236 |     hemocentro = models.ForeignKey(
  237 |         settings.AUTH_USER_MODEL,
  238 |         on_delete=models.CASCADE,
  239 |         related_name="validacoes_hemocentro",
  240 |         db_column="id_hemocentro",
  241 |     )
  242 | 
  243 |     admin = models.ForeignKey(
  244 |         settings.AUTH_USER_MODEL,
  245 |         on_delete=models.SET_NULL,
  246 |         null=True,
  247 |         blank=True,
  248 |         related_name="validacoes_hemocentro_realizadas",
  249 |         db_column="id_admin",
  250 |     )
  251 | 
  252 |     status = models.CharField(
  253 |         max_length=20,
  254 |         choices=Usuario.StatusValidacaoHemocentro.choices,
  255 |     )
  256 | 
  257 |     parecer = models.TextField(blank=True, default="")
  258 |     data_analise = models.DateTimeField(auto_now_add=True)
  259 | 
  260 |     class Meta:
  261 |         db_table = "validacoes_hemocentro"
  262 |         verbose_name = "validacao de hemocentro"
  263 |         verbose_name_plural = "validacoes de hemocentros"
  264 |         ordering = ["-data_analise"]
  265 | 
  266 |         indexes = [
  267 |             models.Index(
  268 |                 fields=["hemocentro", "-data_analise"],
  269 |                 name="validacao_hemo_data_idx",
  270 |             ),
  271 |             models.Index(
  272 |                 fields=["status", "data_analise"],
  273 |                 name="validacao_hemo_status_idx",
  274 |             ),
  275 |         ]
  276 | 
  277 |     def clean(self):
  278 |         """Impede historico para conta que nao seja Hemocentro."""
  279 | 
  280 |         super().clean()
  281 | 
  282 |         hemocentro_nao_eh_valido = (
  283 |             self.hemocentro_id
  284 |             and self.hemocentro.perfil != Usuario.Perfil.HEMOCENTRO
  285 |         )
  286 | 
  287 |         if hemocentro_nao_eh_valido:
  288 |             raise ValidationError(
  289 |                 {
  290 |                     "hemocentro": (
  291 |                         "Somente usuarios com perfil Hemocentro podem ser validados."
  292 |                     )
  293 |                 }
  294 |             )
  295 | 
  296 |         admin_eh_valido = (
  297 |             self.admin_id
  298 |             and (
  299 |                 self.admin.is_staff
  300 |                 or self.admin.is_superuser
  301 |                 or self.admin.perfil == Usuario.Perfil.ADMINISTRADOR
  302 |             )
  303 |         )
  304 | 
  305 |         if self.admin_id and not admin_eh_valido:
  306 |             raise ValidationError(
  307 |                 {"admin": "A validacao deve ser registrada por um administrador."}
  308 |             )
  309 | 
  310 |     def __str__(self):
  311 |         return (
  312 |             f"{self.hemocentro.nome} - {self.get_status_display()} "
  313 |             f"em {self.data_analise:%d/%m/%Y %H:%M}"
  314 |         )
  315 | 
  316 | 
  317 | class ConsentimentoLGPD(models.Model):
  318 |     """
  319 |     Guarda a prova de cada aceite de termo.
  320 | 
  321 |     O consentimento fica separado de Usuario porque precisa guardar sua propria
  322 |     versao, data e Ip. Quando o texto do termo mudar, uma nova versao podera ser
  323 |     aceita sem apagar o registro da versao anterior.
  324 |     """
  325 | 
  326 |     class TipoTermo(models.TextChoices):
  327 |         GERAL = "GERAL", "Termos gerais e politica de privacidade"
  328 |         TRIAGEM = "TRIAGEM", "Termo de triagem"
  329 |         NOTIFICACOES = "NOTIFICACOES", "Termo de notificacoes"
  330 | 
  331 |     id_consentimento = models.BigAutoField(primary_key=True)
  332 | 
  333 |     usuario = models.ForeignKey(
  334 |         settings.AUTH_USER_MODEL,
  335 |         on_delete=models.CASCADE,
  336 |         related_name="consentimentos_lgpd",
  337 |         db_column="id_usuario",
  338 |     )
  339 | 
  340 |     tipo_termo = models.CharField(
  341 |         max_length=20,
  342 |         choices=TipoTermo.choices,
  343 |         default=TipoTermo.GERAL,
  344 |     )
  345 | 
  346 |     versao_termo = models.CharField(max_length=20, default="1.0")
  347 |     aceito = models.BooleanField(default=False)
  348 |     data_aceite = models.DateTimeField(auto_now_add=True)
  349 |     ip = models.GenericIPAddressField(null=True, blank=True)
  350 |     revogado_em = models.DateTimeField(null=True, blank=True)
  351 | 
  352 |     class Meta:
  353 |         db_table = "consentimentos_lgpd"
  354 |         verbose_name = "consentimento LGPD"
  355 |         verbose_name_plural = "consentimentos LGPD"
  356 |         ordering = ["-data_aceite"]
  357 | 
  358 |         constraints = [
  359 |             models.UniqueConstraint(
  360 |                 fields=["usuario", "tipo_termo", "versao_termo"],
  361 |                 name="consentimento_unico_por_versao",
  362 |             )
  363 |         ]
  364 | 
  365 |     def __str__(self):
  366 |         return f"{self.usuario.email} - {self.get_tipo_termo_display()}"
  367 | 
  368 | 
  369 | class AuditoriaAcaoCritica(models.Model):
  370 |     """
  371 |     Registro de eventos sensiveis do Elo, somente leitura no painel administrativo.
  372 | 
  373 |     A auditoria guarda o contexto da acao sem copiar senhas, tokens ou dados
  374 |     sensiveis completos. Cada tela ou rotina critica deve chamar a funcao
  375 |     central de auditoria em accounts/auditoria.py.
  376 |     """
  377 | 
  378 |     class Acao(models.TextChoices):
  379 |         LOGIN_FALHO = "LOGIN_FALHO", "Login falho"
  380 |         LOGIN_SUSPEITO = "LOGIN_SUSPEITO", "Login suspeito"
  381 |         ALTERACAO_PERMISSAO = "ALTERACAO_PERMISSAO", "Alteracao de permissao"
  382 |         APROVACAO_HEMOCENTRO = "APROVACAO_HEMOCENTRO", "Aprovacao de hemocentro"
  383 |         CADASTRO_ESTOQUE = "CADASTRO_ESTOQUE", "Cadastro de estoque"
  384 |         ATUALIZACAO_ESTOQUE = "ATUALIZACAO_ESTOQUE", "Atualizacao de estoque"
  385 |         MODERACAO = "MODERACAO", "Moderacao"
  386 |         ACESSO_DADOS_SENSIVEIS = (
  387 |             "ACESSO_DADOS_SENSIVEIS",
  388 |             "Acesso a dados sensiveis",
  389 |         )
  390 |         CONFIRMACAO_DOACAO = "CONFIRMACAO_DOACAO", "Confirmacao de doacao"
  391 | 
  392 |     class Resultado(models.TextChoices):
  393 |         SUCESSO = "SUCESSO", "Sucesso"
  394 |         FALHA = "FALHA", "Falha"
  395 |         BLOQUEADO = "BLOQUEADO", "Bloqueado"
  396 | 
  397 |     id_auditoria = models.BigAutoField(primary_key=True)
  398 | 
  399 |     usuario = models.ForeignKey(
  400 |         settings.AUTH_USER_MODEL,
  401 |         on_delete=models.SET_NULL,
  402 |         null=True,
  403 |         blank=True,
  404 |         related_name="auditorias_acoes_criticas",
  405 |         db_column="id_usuario",
  406 |     )
  407 | 
  408 |     acao = models.CharField(max_length=40, choices=Acao.choices)
  409 | 
  410 |     resultado = models.CharField(
  411 |         max_length=20,
  412 |         choices=Resultado.choices,
  413 |         default=Resultado.SUCESSO,
  414 |     )
  415 | 
  416 |     alvo_tipo = models.CharField(max_length=80, blank=True, default="")
  417 |     alvo_id = models.CharField(max_length=80, blank=True, default="")
  418 |     descricao = models.CharField(max_length=255, blank=True, default="")
  419 |     ip = models.GenericIPAddressField(null=True, blank=True)
  420 |     user_agent = models.TextField(blank=True, default="")
  421 |     metadados = models.JSONField(blank=True, default=dict)
  422 |     criado_em = models.DateTimeField(auto_now_add=True)
  423 | 
  424 |     class Meta:
  425 |         db_table = "auditorias_acoes_criticas"
  426 |         verbose_name = "auditoria de acao critica"
  427 |         verbose_name_plural = "auditorias de acoes criticas"
  428 |         ordering = ["-criado_em"]
  429 | 
  430 |         indexes = [
  431 |             models.Index(
  432 |                 fields=["acao", "criado_em"],
  433 |                 name="auditoria_acao_data_idx",
  434 |             ),
  435 |             models.Index(
  436 |                 fields=["usuario", "criado_em"],
  437 |                 name="auditoria_usuario_data_idx",
  438 |             ),
  439 |             models.Index(
  440 |                 fields=["ip", "criado_em"],
  441 |                 name="auditoria_ip_data_idx",
  442 |             ),
  443 |         ]
  444 | 
  445 |     def __str__(self):
  446 |         return f"{self.get_acao_display()} - {self.get_resultado_display()}"
  447 | 
  448 | 
  449 | class Triagem(models.Model):
  450 |     """
  451 |     Guarda uma triagem realizada por um usuário.
  452 | 
  453 |     O resultado é orientativo e nunca substitui a avaliação
  454 |     presencial feita pelo hemocentro.
  455 |     """
  456 | 
  457 |     class Modalidade(models.TextChoices):
  458 |         EXTENSA = "EXTENSA", "Triagem extensa"
  459 |         SIMPLIFICADA = "SIMPLIFICADA", "Triagem simplificada"
  460 | 
  461 |     class Status(models.TextChoices):
  462 |         """Representa em qual etapa do questionário a triagem está."""
  463 | 
  464 |         EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
  465 |         CONCLUIDA = "CONCLUIDA", "Concluída"
  466 |         CANCELADA = "CANCELADA", "Cancelada"
  467 | 
  468 |     class Resultado(models.TextChoices):
  469 |         SEM_IMPEDIMENTO = (
  470 |             "SEM_IMPEDIMENTO_IDENTIFICADO",
  471 |             "Apto",
  472 |         )
  473 |         TEMPORARIA = (
  474 |             "INAPTIDAO_TEMPORARIA",
  475 |             "Inaptidão temporária",
  476 |         )
  477 |         DEFINITIVA = (
  478 |             "INAPTIDAO_DEFINITIVA",
  479 |             "Inaptidão definitiva",
  480 |         )
  481 |         AVALIACAO = (
  482 |             "AVALIACAO_PRESENCIAL",
  483 |             "Avaliação presencial necessária",
  484 |         )
  485 |         DOCUMENTACAO = (
  486 |             "DOCUMENTACAO_ESPECIAL",
  487 |             "Documentação especial",
  488 |         )
  489 | 
  490 |     id_triagem = models.BigAutoField(primary_key=True)
  491 | 
  492 |     usuario = models.ForeignKey(
  493 |         settings.AUTH_USER_MODEL,
  494 |         on_delete=models.CASCADE,
  495 |         related_name="triagens",
  496 |         db_column="id_usuario",
  497 |     )
  498 | 
  499 |     modalidade = models.CharField(
  500 |         max_length=20,
  501 |         choices=Modalidade.choices,
  502 |         default=Modalidade.EXTENSA,
  503 |     )
  504 | 
  505 |     status = models.CharField(
  506 |         max_length=20,
  507 |         choices=Status.choices,
  508 |         default=Status.EM_ANDAMENTO,
  509 |     )
  510 | 
  511 |     pergunta_atual = models.PositiveIntegerField(default=0)
  512 |     fluxo_perguntas = models.JSONField(default=list, blank=True)
  513 | 
  514 |     triagem_base = models.ForeignKey(
  515 |         "self",
  516 |         on_delete=models.SET_NULL,
  517 |         null=True,
  518 |         blank=True,
  519 |         related_name="verificacoes_simplificadas",
  520 |     )
  521 | 
  522 |     regra_version = models.CharField(
  523 |         max_length=40,
  524 |         default="HEMOMINAS_2026_08",
  525 |     )
  526 | 
  527 |     resultado = models.CharField(
  528 |         max_length=40,
  529 |         choices=Resultado.choices,
  530 |         blank=True,
  531 |         default="",
  532 |     )
  533 | 
  534 |     mensagem_resultado = models.TextField(
  535 |         blank=True,
  536 |         default="",
  537 |     )
  538 | 
  539 |     data_liberacao = models.DateField(
  540 |         null=True,
  541 |         blank=True,
  542 |     )
  543 | 
  544 |     achados = models.JSONField(
  545 |         default=list,
  546 |         blank=True,
  547 |     )
  548 | 
  549 |     iniciada_em = models.DateTimeField(auto_now_add=True)
  550 | 
  551 |     finalizada_em = models.DateTimeField(
  552 |         null=True,
  553 |         blank=True,
  554 |     )
  555 | 
  556 |     atualizada_em = models.DateTimeField(auto_now=True)
  557 | 
  558 |     class Meta:
  559 |         db_table = "triagens"
  560 |         ordering = ["-iniciada_em"]
  561 | 
  562 |         indexes = [
  563 |             models.Index(
  564 |                 fields=["usuario", "-iniciada_em"],
  565 |                 name="triagem_usuario_data_idx",
  566 |             ),
  567 |             models.Index(
  568 |                 fields=["resultado", "-iniciada_em"],
  569 |                 name="triagem_resultado_data_idx",
  570 |             ),
  571 |         ]
  572 | 
  573 |         verbose_name = "Triagem"
  574 |         verbose_name_plural = "Triagens"
  575 | 
  576 |     def __str__(self):
  577 |         return (
  578 |             f"Triagem {self.id_triagem} - "
  579 |             f"{self.usuario.nome} - "
  580 |             f"{self.get_resultado_display()}"
  581 |         )
  582 | 
  583 | 
  584 | # Nomes legados continuam disponíveis para código já existente, mas apontam
  585 | # para os resultados oficiais usados pelo fluxo atual.
  586 | Triagem.Resultado.APTO = Triagem.Resultado.SEM_IMPEDIMENTO
  587 | Triagem.Resultado.INAPTO_TEMPORARIO = Triagem.Resultado.TEMPORARIA
  588 | Triagem.Resultado.INAPTO_PERMANENTE = Triagem.Resultado.DEFINITIVA
  589 | Triagem.Resultado.AVALIACAO_PRESENCIAL_NECESSARIA = Triagem.Resultado.AVALIACAO
  590 | 
  591 | 
  592 | class RespostaTriagem(models.Model):
  593 |     """
  594 |     Guarda uma resposta individual da triagem.
  595 | 
  596 |     As respostas são mantidas separadas para permitir auditoria,
  597 |     revisão das regras e futuras versões do questionário.
  598 |     """
  599 | 
  600 |     id_resposta = models.BigAutoField(primary_key=True)
  601 | 
  602 |     triagem = models.ForeignKey(
  603 |         Triagem,
  604 |         on_delete=models.CASCADE,
  605 |         related_name="respostas",
  606 |         db_column="id_triagem",
  607 |     )
  608 | 
  609 |     id_pergunta = models.CharField(max_length=20)
  610 |     codigo_resposta = models.CharField(max_length=80)
  611 |     resposta_label = models.CharField(max_length=255)
  612 | 
  613 |     data_evento = models.DateField(
  614 |         db_column="event_date",
  615 |         null=True,
  616 |         blank=True,
  617 |     )
  618 | 
  619 |     metadata = models.JSONField(
  620 |         default=dict,
  621 |         blank=True,
  622 |     )
  623 | 
  624 |     valor = models.JSONField(
  625 |         default=dict,
  626 |         blank=True,
  627 |     )
  628 | 
  629 |     rule_version = models.CharField(
  630 |         max_length=40,
  631 |         default="HEMOMINAS_2026_08",
  632 |     )
  633 | 
  634 |     source_ref = models.CharField(
  635 |         max_length=255,
  636 |         blank=True,
  637 |         default="",
  638 |     )
  639 | 
  640 |     respondido_em = models.DateTimeField(auto_now_add=True)
  641 | 
  642 |     class Meta:
  643 |         db_table = "respostas_triagem"
  644 |         ordering = ["id_resposta"]
  645 | 
  646 |         constraints = [
  647 |             models.UniqueConstraint(
  648 |                 fields=["triagem", "id_pergunta"],
  649 |                 name="resposta_unica_por_pergunta",
  650 |             ),
  651 |         ]
  652 | 
  653 |         indexes = [
  654 |             models.Index(
  655 |                 fields=["triagem", "id_pergunta"],
  656 |                 name="resposta_triagem_pergunta_idx",
  657 |             ),
  658 |         ]
  659 | 
  660 |         verbose_name = "Resposta triagem"
  661 |         verbose_name_plural = "Respostas triagem"
  662 | 
  663 |     def __str__(self):
  664 |         return (
  665 |             f"{self.triagem_id} - "
  666 |             f"{self.id_pergunta} - "
  667 |             f"{self.codigo_resposta}"
  668 |         )
  669 | 
  670 | 
  671 | class Estoque(models.Model):
  672 |     """
  673 |     Uc_29 - Cadastrar Estoque.
  674 | 
  675 |     Guarda a estrutura de estoque de um Hemocentro para um unico tipo
  676 |     sanguineo: quantidade atual de bolsas, os niveis de alerta definidos
  677 |     pelo proprio hemocentro e o status calculado a partir desses valores.
  678 | 
  679 |     So existe um registro de Estoque por combinacao de hemocentro e tipo
  680 |     sanguineo (garantido pela UniqueConstraint abaixo). Para mudar a
  681 |     quantidade de bolsas depois de criado, use as funcoes de
  682 |     ``accounts/estoque.py`` em vez de editar o campo diretamente: elas
  683 |     recalculam o status, criam o historico em EstoqueMovimentacao e
  684 |     registram a auditoria.
  685 |     """
  686 | 
  687 |     class StatusCalculado(models.TextChoices):
  688 |         """
  689 |         Situacao do estoque, sempre derivada da quantidade e dos niveis.
  690 | 
  691 |         Nunca deve ser digitada manualmente por quem usa o sistema: a
  692 |         camada de servico recalcula este campo toda vez que a quantidade
  693 |         de bolsas muda.
  694 |         """
  695 | 
  696 |         CRITICO = "CRITICO", "Crítico"
  697 |         BAIXO = "BAIXO", "Baixo"
  698 |         ESTAVEL = "ESTAVEL", "Estável"
  699 | 
  700 |     id_estoque = models.BigAutoField(primary_key=True)
  701 | 
  702 |     hemocentro = models.ForeignKey(
  703 |         settings.AUTH_USER_MODEL,
  704 |         on_delete=models.CASCADE,
  705 |         related_name="estoques",
  706 |         db_column="id_hemocentro",
  707 |         limit_choices_to={"perfil": "HEMOCENTRO"},
  708 |     )
  709 | 
  710 |     tipo_sanguineo = models.CharField(
  711 |         max_length=3,
  712 |         choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
  713 |     )
  714 | 
  715 |     quantidade_bolsas = models.PositiveIntegerField(default=0)
  716 |     nivel_minimo = models.PositiveIntegerField()
  717 |     nivel_critico = models.PositiveIntegerField()
  718 | 
  719 |     status_calculado = models.CharField(
  720 |         max_length=10,
  721 |         choices=StatusCalculado.choices,
  722 |         default=StatusCalculado.ESTAVEL,
  723 |     )
  724 | 
  725 |     data_atualizacao = models.DateTimeField(auto_now=True)
  726 | 
  727 |     class Meta:
  728 |         db_table = "estoques"
  729 |         verbose_name = "estoque"
  730 |         verbose_name_plural = "estoques"
  731 |         ordering = ["hemocentro__nome", "tipo_sanguineo"]
  732 | 
  733 |         constraints = [
  734 |             models.UniqueConstraint(
  735 |                 fields=["hemocentro", "tipo_sanguineo"],
  736 |                 name="estoque_unico_por_hemocentro_tipo",
  737 |             ),
  738 |         ]
  739 | 
  740 |         indexes = [
  741 |             models.Index(
  742 |                 fields=["hemocentro", "tipo_sanguineo"],
  743 |                 name="estoque_hemo_tipo_idx",
  744 |             ),
  745 |             models.Index(
  746 |                 fields=["status_calculado"],
  747 |                 name="estoque_status_idx",
  748 |             ),
  749 |         ]
  750 | 
  751 |     def clean(self):
  752 |         """Valida regras que dependem de mais de um campo."""
  753 | 
  754 |         super().clean()
  755 | 
  756 |         if (
  757 |             self.hemocentro_id
  758 |             and self.hemocentro.perfil != Usuario.Perfil.HEMOCENTRO
  759 |         ):
  760 |             raise ValidationError(
  761 |                 {
  762 |                     "hemocentro": (
  763 |                         "Somente contas com perfil Hemocentro podem ter estoque."
  764 |                     )
  765 |                 }
  766 |             )
  767 | 
  768 |         if (
  769 |             self.nivel_minimo is not None
  770 |             and self.nivel_critico is not None
  771 |             and self.nivel_critico > self.nivel_minimo
  772 |         ):
  773 |             raise ValidationError(
  774 |                 {
  775 |                     "nivel_critico": (
  776 |                         "O nivel critico deve ser menor ou igual ao nivel minimo."
  777 |                     )
  778 |                 }
  779 |             )
  780 | 
  781 |     def __str__(self):
  782 |         return (
  783 |             f"{self.hemocentro.nome} - {self.tipo_sanguineo} "
  784 |             f"({self.get_status_calculado_display()})"
  785 |         )
  786 | 
  787 | 
  788 | class EstoqueMovimentacao(models.Model):
  789 |     """
  790 |     Uc_30 - Atualizar Estoque.
  791 | 
  792 |     Historico imutavel de cada entrada, saida ou ajuste feito em um
  793 |     Estoque. Uma linha nunca e alterada ou apagada depois de criada: para
  794 |     corrigir um valor, registra-se uma nova movimentacao (do tipo Ajuste).
  795 | 
  796 |     Isso preserva o rastro completo exigido pela regra "toda alteracao
  797 |     deve gerar historico com responsavel".
  798 |     """
  799 | 
  800 |     class TipoMovimento(models.TextChoices):
  801 |         ENTRADA = "ENTRADA", "Entrada"
  802 |         SAIDA = "SAIDA", "Saída"
  803 |         AJUSTE = "AJUSTE", "Ajuste"
  804 | 
  805 |     id_mov = models.BigAutoField(primary_key=True)
  806 | 
  807 |     estoque = models.ForeignKey(
  808 |         Estoque,
  809 |         on_delete=models.CASCADE,
  810 |         related_name="movimentacoes",
  811 |         db_column="id_estoque",
  812 |     )
  813 | 
  814 |     usuario_resp = models.ForeignKey(
  815 |         settings.AUTH_USER_MODEL,
  816 |         on_delete=models.SET_NULL,
  817 |         null=True,
  818 |         blank=True,
  819 |         related_name="movimentacoes_estoque_realizadas",
  820 |         db_column="id_usuario_resp",
  821 |     )
  822 | 
  823 |     tipo_movimento = models.CharField(
  824 |         max_length=10,
  825 |         choices=TipoMovimento.choices,
  826 |     )
  827 | 
  828 |     quantidade_anterior = models.PositiveIntegerField()
  829 |     quantidade_movimentada = models.IntegerField()
  830 |     quantidade_nova = models.PositiveIntegerField()
  831 | 
  832 |     motivo = models.CharField(
  833 |         max_length=255,
  834 |         blank=True,
  835 |         default="",
  836 |     )
  837 | 
  838 |     data_hora = models.DateTimeField(auto_now_add=True)
  839 | 
  840 |     class Meta:
  841 |         db_table = "movimentacoes_estoque"
  842 |         verbose_name = "movimentacao de estoque"
  843 |         verbose_name_plural = "movimentacoes de estoque"
  844 |         ordering = ["-data_hora"]
  845 | 
  846 |         indexes = [
  847 |             models.Index(
  848 |                 fields=["estoque", "-data_hora"],
  849 |                 name="mov_estoque_data_idx",
  850 |             ),
  851 |             models.Index(
  852 |                 fields=["usuario_resp", "-data_hora"],
  853 |                 name="mov_usuario_data_idx",
  854 |             ),
  855 |         ]
  856 | 
  857 |     def __str__(self):
  858 |         return (
  859 |             f"{self.estoque.tipo_sanguineo} - "
  860 |             f"{self.get_tipo_movimento_display()} - "
  861 |             f"{self.quantidade_anterior} -> {self.quantidade_nova}"
  862 |         )
  863 | 
  864 | 
  865 | class Notificacao(models.Model):
  866 |     """
  867 |     Guarda avisos internos exibidos no dashboard do usuario.
  868 | 
  869 |     Nesta etapa, a notificacao sera usada para avisar doadores compativeis
  870 |     quando um estoque atualizado por Hemocentro ficar em nivel Baixo ou Critico.
  871 |     Futuramente a mesma tabela tambem pode receber outros avisos do sistema.
  872 |     """
  873 | 
  874 |     class Tipo(models.TextChoices):
  875 |         """Classificacao do aviso para facilitar filtros futuros."""
  876 | 
  877 |         ESTOQUE_BAIXO = "ESTOQUE_BAIXO", "Estoque baixo"
  878 |         ESTOQUE_CRITICO = "ESTOQUE_CRITICO", "Estoque crítico"
  879 |         PEDIDO_COMPATIVEL = "PEDIDO_COMPATIVEL", "Pedido compatível"
  880 |         GERAL = "GERAL", "Aviso geral"
  881 | 
  882 |     id_notificacao = models.BigAutoField(primary_key=True)
  883 | 
  884 |     usuario = models.ForeignKey(
  885 |         settings.AUTH_USER_MODEL,
  886 |         on_delete=models.CASCADE,
  887 |         related_name="notificacoes",
  888 |         db_column="id_usuario",
  889 |     )
  890 | 
  891 |     estoque = models.ForeignKey(
  892 |         Estoque,
  893 |         on_delete=models.SET_NULL,
  894 |         null=True,
  895 |         blank=True,
  896 |         related_name="notificacoes",
  897 |         db_column="id_estoque",
  898 |     )
  899 | 
  900 |     pedido = models.ForeignKey(
  901 |         "PedidoSangue",
  902 |         on_delete=models.SET_NULL,
  903 |         null=True,
  904 |         blank=True,
  905 |         related_name="notificacoes",
  906 |         db_column="id_pedido",
  907 |     )
  908 | 
  909 |     tipo = models.CharField(
  910 |         max_length=30,
  911 |         choices=Tipo.choices,
  912 |         default=Tipo.GERAL,
  913 |     )
  914 | 
  915 |     titulo = models.CharField(max_length=120)
  916 |     mensagem = models.TextField()
  917 |     url_destino = models.CharField(max_length=255, blank=True, default="")
  918 |     lida = models.BooleanField(default=False)
  919 |     criada_em = models.DateTimeField(auto_now_add=True)
  920 |     lida_em = models.DateTimeField(null=True, blank=True)
  921 | 
  922 |     class Meta:
  923 |         db_table = "notificacoes"
  924 |         verbose_name = "notificacao"
  925 |         verbose_name_plural = "notificacoes"
  926 |         ordering = ["-criada_em"]
  927 | 
  928 |         indexes = [
  929 |             models.Index(
  930 |                 fields=["usuario", "lida", "-criada_em"],
  931 |                 name="notificacao_usuario_lida_idx",
  932 |             ),
  933 |             models.Index(
  934 |                 fields=["tipo", "-criada_em"],
  935 |                 name="notificacao_tipo_data_idx",
  936 |             ),
  937 |         ]
  938 | 
  939 |     def __str__(self):
  940 |         """Texto usado no admin e no terminal."""
  941 | 
  942 |         return f"{self.usuario.nome} - {self.titulo}"
  943 | 
  944 | 
  945 | class PedidoSangue(models.Model):
  946 |     """
  947 |     Rf - Pedido de Sangue.
  948 | 
  949 |     Guarda solicitações de divulgação e os pedidos publicados oficialmente.
  950 | 
  951 |     Doador, Receptor, Observador e Visitante criam somente uma solicitação.
  952 |     A publicação oficial é feita pelo Hemocentro aprovado vinculado.
  953 |     """
  954 | 
  955 |     class ParaQuem(models.TextChoices):
  956 |         MIM = "MIM", "Para mim"
  957 |         OUTRA_PESSOA = "OUTRA_PESSOA", "Para outra pessoa"
  958 | 
  959 |     class Urgencia(models.TextChoices):
  960 |         BAIXA = "BAIXA", "Baixa"
  961 |         MEDIA = "MEDIA", "Media"
  962 |         ALTA = "ALTA", "Alta"
  963 |         CRITICA = "CRITICA", "Critica"
  964 | 
  965 |     class Status(models.TextChoices):
  966 |         ENVIADA = "ENVIADA", "Enviada"
  967 |         EM_ANALISE = "EM_ANALISE", "Em análise"
  968 |         PUBLICADA = "PUBLICADA", "Publicada"
  969 |         CORRECAO_SOLICITADA = "CORRECAO_SOLICITADA", "Correção solicitada"
  970 |         RECUSADA = "RECUSADA", "Recusada"
  971 |         ENCERRADA = "ENCERRADA", "Encerrada"
  972 | 
  973 |     id_pedido = models.BigAutoField(primary_key=True)
  974 | 
  975 |     solicitante = models.ForeignKey(
  976 |         settings.AUTH_USER_MODEL,
  977 |         on_delete=models.SET_NULL,
  978 |         null=True,
  979 |         blank=True,
  980 |         related_name="pedidos_sangue",
  981 |         db_column="id_solicitante",
  982 |     )
  983 | 
  984 |     nome_solicitante = models.CharField(max_length=150, default="")
  985 |     contato = models.EmailField(max_length=120, default="")
  986 | 
  987 |     hemocentro_destino = models.ForeignKey(
  988 |         settings.AUTH_USER_MODEL,
  989 |         on_delete=models.PROTECT,
  990 |         related_name="pedidos_recebidos",
  991 |         db_column="id_hemocentro_destino",
  992 |         limit_choices_to={"perfil": "HEMOCENTRO"},
  993 |     )
  994 | 
  995 |     para_quem = models.CharField(
  996 |         max_length=20,
  997 |         choices=ParaQuem.choices,
  998 |     )
  999 | 
 1000 |     titulo = models.CharField(
 1001 |         max_length=150,
 1002 |         default="Pedido de sangue",
 1003 |     )
 1004 | 
 1005 |     tipo_sanguineo = models.CharField(
 1006 |         max_length=3,
 1007 |         choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
 1008 |     )
 1009 | 
 1010 |     urgencia = models.CharField(
 1011 |         max_length=10,
 1012 |         choices=Urgencia.choices,
 1013 |     )
 1014 | 
 1015 |     cidade = models.CharField(max_length=100)
 1016 |     nome_paciente = models.CharField(
 1017 |         max_length=150,
 1018 |         blank=True,
 1019 |         default="",
 1020 |     )
 1021 |     descricao = models.TextField()
 1022 |     justificativa_urgencia = models.TextField(blank=True, default="")
 1023 |     informacoes_complementares = models.TextField(blank=True, default="")
 1024 | 
 1025 |     status = models.CharField(
 1026 |         max_length=30,
 1027 |         choices=Status.choices,
 1028 |         default=Status.ENVIADA,
 1029 |     )
 1030 | 
 1031 |     duplicidade_suspeita = models.BooleanField(default=False)
 1032 | 
 1033 |     publicado_por = models.ForeignKey(
 1034 |         settings.AUTH_USER_MODEL,
 1035 |         on_delete=models.SET_NULL,
 1036 |         null=True,
 1037 |         blank=True,
 1038 |         related_name="pedidos_publicados",
 1039 |         db_column="id_publicado_por",
 1040 |     )
 1041 |     publicado_em = models.DateTimeField(null=True, blank=True)
 1042 | 
 1043 |     data_criacao = models.DateTimeField(auto_now_add=True)
 1044 |     atualizado_em = models.DateTimeField(auto_now=True)
 1045 |     data_fechamento = models.DateTimeField(null=True, blank=True)
 1046 | 
 1047 |     class Meta:
 1048 |         db_table = "pedidos_sangue"
 1049 |         ordering = ["-data_criacao"]
 1050 |         verbose_name = "pedido de sangue"
 1051 |         verbose_name_plural = "pedidos de sangue"
 1052 | 
 1053 |         indexes = [
 1054 |             models.Index(
 1055 |                 fields=["status", "-data_criacao"],
 1056 |                 name="pedido_status_data_idx",
 1057 |             ),
 1058 |             models.Index(
 1059 |                 fields=["tipo_sanguineo", "urgencia"],
 1060 |                 name="pedido_tipo_urg_idx",
 1061 |             ),
 1062 |             models.Index(
 1063 |                 fields=["cidade"],
 1064 |                 name="pedido_cidade_idx",
 1065 |             ),
 1066 |         ]
 1067 | 
 1068 |     def clean(self):
 1069 |         super().clean()
 1070 | 
 1071 |         if self.solicitante_id and self.solicitante.perfil in {
 1072 |             Usuario.Perfil.HEMOCENTRO,
 1073 |             Usuario.Perfil.ADMINISTRADOR,
 1074 |         }:
 1075 |             raise ValidationError(
 1076 |                 {"solicitante": "Este perfil não pode enviar solicitações."}
 1077 |             )
 1078 | 
 1079 |         if self.status == self.Status.PUBLICADA:
 1080 |             if not self.publicado_por_id or not self.publicado_por:
 1081 |                 raise ValidationError(
 1082 |                     {"publicado_por": "A publicação precisa de um Hemocentro aprovado."}
 1083 |                 )
 1084 |             if not (
 1085 |                 self.publicado_por.perfil == Usuario.Perfil.HEMOCENTRO
 1086 |                 and self.publicado_por.status_validacao
 1087 |                 == Usuario.StatusValidacaoHemocentro.APROVADO
 1088 |             ):
 1089 |                 raise ValidationError(
 1090 |                     {"publicado_por": "Somente Hemocentro aprovado pode publicar."}
 1091 |                 )
 1092 | 
 1093 |         if (
 1094 |             self.hemocentro_destino_id
 1095 |             and self.hemocentro_destino.perfil != Usuario.Perfil.HEMOCENTRO
 1096 |         ):
 1097 |             raise ValidationError(
 1098 |                 {
 1099 |                     "hemocentro_destino": (
 1100 |                         "O destino precisa ser um Hemocentro cadastrado."
 1101 |                     )
 1102 |                 }
 1103 |             )
 1104 | 
 1105 |     def __str__(self):
 1106 |         return (
 1107 |             f"{self.titulo} - {self.tipo_sanguineo} - "
 1108 |             f"{self.get_status_display()}"
 1109 |         )
 1110 | 
 1111 | 
 1112 | # Compatibilidade de leitura para integrações antigas. Os valores novos são
 1113 | # os únicos gravados pelo fluxo atual.
 1114 | PedidoSangue.Status.PENDENTE_VALIDACAO = PedidoSangue.Status.ENVIADA
 1115 | PedidoSangue.Status.ATIVO = PedidoSangue.Status.PUBLICADA
 1116 | PedidoSangue.Status.SUSPEITO = PedidoSangue.Status.EM_ANALISE
 1117 | PedidoSangue.Status.RECUSADO = PedidoSangue.Status.RECUSADA
 1118 | PedidoSangue.Status.ENCERRADO = PedidoSangue.Status.ENCERRADA
 1119 | 
 1120 | 
 1121 | class ValidacaoPedido(models.Model):
 1122 |     """
 1123 |     Uc_17 - Validar Pedido.
 1124 | 
 1125 |     Guarda o historico das validacoes feitas automaticamente ou por moderador.
 1126 |     """
 1127 | 
 1128 |     class StatusValidacao(models.TextChoices):
 1129 |         APROVADO = "APROVADO", "Aprovado"
 1130 |         CORRECAO_SOLICITADA = "CORRECAO_SOLICITADA", "Correção solicitada"
 1131 |         SUSPEITO = "SUSPEITO", "Suspeito"
 1132 |         RECUSADO = "RECUSADO", "Recusado"
 1133 | 
 1134 |     id_validacao = models.BigAutoField(primary_key=True)
 1135 | 
 1136 |     pedido = models.ForeignKey(
 1137 |         PedidoSangue,
 1138 |         on_delete=models.CASCADE,
 1139 |         related_name="validacoes",
 1140 |         db_column="id_pedido",
 1141 |     )
 1142 | 
 1143 |     status_validacao = models.CharField(
 1144 |         max_length=20,
 1145 |         choices=StatusValidacao.choices,
 1146 |     )
 1147 | 
 1148 |     motivo = models.TextField(blank=True, default="")
 1149 | 
 1150 |     moderador = models.ForeignKey(
 1151 |         settings.AUTH_USER_MODEL,
 1152 |         on_delete=models.SET_NULL,
 1153 |         null=True,
 1154 |         blank=True,
 1155 |         related_name="validacoes_pedido_realizadas",
 1156 |         db_column="id_moderador",
 1157 |     )
 1158 | 
 1159 |     data_validacao = models.DateTimeField(auto_now_add=True)
 1160 | 
 1161 |     class Meta:
 1162 |         db_table = "validacoes_pedido"
 1163 |         ordering = ["-data_validacao"]
 1164 | 
 1165 |     def __str__(self):
 1166 |         return f"Pedido {self.pedido_id} - {self.get_status_validacao_display()}"
 1167 | 
 1168 | 
 1169 | ValidacaoPedido.StatusValidacao.CORRECAO = (
 1170 |     ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA
 1171 | )
``````

## accounts/pedidos.py

Original: [accounts/pedidos.py](<C:/Users/lb119/Elo/accounts/pedidos.py>).

``````text
    1 | """Operações de publicação de pedidos de sangue."""
    2 | 
    3 | from django.core.exceptions import PermissionDenied
    4 | from django.db import transaction
    5 | from django.urls import reverse
    6 | from django.utils import timezone
    7 | 
    8 | from .compatibilidade import doadores_aptos_para_convocacao, limite_convocacao_atingido
    9 | from .models import AuditoriaAcaoCritica, Notificacao, PedidoSangue, Usuario
   10 | from .auditoria import registrar_auditoria
   11 | 
   12 | 
   13 | def pode_publicar_pedido(usuario):
   14 |     """Somente o Hemocentro aprovado pode publicar oficialmente."""
   15 | 
   16 |     return (
   17 |         usuario.is_authenticated
   18 |         and usuario.perfil == Usuario.Perfil.HEMOCENTRO
   19 |         and usuario.status_validacao
   20 |         == Usuario.StatusValidacaoHemocentro.APROVADO
   21 |     )
   22 | 
   23 | 
   24 | @transaction.atomic
   25 | def publicar_pedido(usuario, form, request=None):
   26 |     """Publica um pedido já analisado pelo próprio Hemocentro."""
   27 | 
   28 |     if not pode_publicar_pedido(usuario):
   29 |         raise PermissionDenied(
   30 |             "Este perfil não pode publicar pedidos de sangue."
   31 |         )
   32 | 
   33 |     pedido = form.save(commit=False)
   34 |     if pedido.hemocentro_destino_id != usuario.pk:
   35 |         raise PermissionDenied("O pedido pertence a outro Hemocentro.")
   36 |     pedido.publicado_por = usuario
   37 |     pedido.publicado_em = timezone.now()
   38 |     pedido.status = PedidoSangue.Status.PUBLICADA
   39 |     pedido.cidade = pedido.hemocentro_destino.cidade
   40 |     pedido.full_clean()
   41 |     pedido.save()
   42 |     criar_notificacoes_para_pedido(pedido=pedido)
   43 |     registrar_auditoria(
   44 |         acao=AuditoriaAcaoCritica.Acao.MODERACAO, usuario=usuario, alvo=pedido, request=request,
   45 |         descricao="Publicacao institucional de pedido de sangue.",
   46 |         metadados={"evento": "PUBLICACAO_PEDIDO", "status_pedido": pedido.status},
   47 |     )
   48 |     return pedido
   49 | 
   50 | 
   51 | @transaction.atomic
   52 | def criar_notificacoes_para_pedido(*, pedido):
   53 |     """Notifica apenas doadores compatíveis e aptos para o pedido publicado."""
   54 | 
   55 |     if pedido.status != PedidoSangue.Status.PUBLICADA or not pode_publicar_pedido(pedido.hemocentro_destino):
   56 |         return 0
   57 |     doadores = doadores_aptos_para_convocacao(pedido.tipo_sanguineo).select_for_update()
   58 | 
   59 |     notificacoes = []
   60 |     for doador in doadores:
   61 |         if limite_convocacao_atingido(doador):
   62 |             continue
   63 |         if Notificacao.objects.filter(usuario=doador, pedido=pedido).exists():
   64 |             continue
   65 |         notificacoes.append(
   66 |             Notificacao(
   67 |                 usuario=doador,
   68 |                 pedido=pedido,
   69 |                 tipo=Notificacao.Tipo.PEDIDO_COMPATIVEL,
   70 |                 titulo=f"Pedido compatível: {pedido.tipo_sanguineo}",
   71 |                 mensagem=(
   72 |                     f"Há uma necessidade publicada pelo Hemocentro "
   73 |                     f"{pedido.hemocentro_destino.nome} em {pedido.cidade}."
   74 |                 ),
   75 |                 url_destino=reverse("accounts:consultar_pedidos"),
   76 |             )
   77 |         )
   78 | 
   79 |     Notificacao.objects.bulk_create(notificacoes)
   80 |     return len(notificacoes)
``````

## accounts/signals.py

Original: [accounts/signals.py](<C:/Users/lb119/Elo/accounts/signals.py>).

``````text
    1 | """
    2 | Sinais do Django usados para auditoria automatica.
    3 | 
    4 | Nesta etapa registramos falhas de login e marcamos como suspeito quando ha
    5 | muitas tentativas recentes para o mesmo e-mail ou IP.
    6 | """
    7 | 
    8 | from datetime import timedelta
    9 | 
   10 | from django.contrib.auth.signals import user_login_failed
   11 | from django.dispatch import receiver
   12 | from django.utils import timezone
   13 | 
   14 | from .auditoria import obter_ip, obter_user_agent, registrar_auditoria
   15 | from .models import AuditoriaAcaoCritica
   16 | 
   17 | 
   18 | LIMITE_LOGIN_SUSPEITO = 5
   19 | JANELA_LOGIN_SUSPEITO_MINUTOS = 10
   20 | 
   21 | 
   22 | @receiver(user_login_failed)
   23 | def auditar_login_falho(sender, credentials, request, **kwargs):
   24 |     """Registra falha e login suspeito sem guardar a senha enviada."""
   25 | 
   26 |     email = (credentials or {}).get("username") or (credentials or {}).get("email")
   27 |     email = (email or "").strip().lower()
   28 |     ip = obter_ip(request)
   29 |     user_agent = obter_user_agent(request)
   30 | 
   31 |     registrar_auditoria(
   32 |         acao=AuditoriaAcaoCritica.Acao.LOGIN_FALHO,
   33 |         resultado=AuditoriaAcaoCritica.Resultado.FALHA,
   34 |         descricao="Tentativa de login sem sucesso.",
   35 |         request=request,
   36 |         ip=ip,
   37 |         user_agent=user_agent,
   38 |         metadados={"email": email},
   39 |     )
   40 | 
   41 |     inicio_janela = timezone.now() - timedelta(minutes=JANELA_LOGIN_SUSPEITO_MINUTOS)
   42 |     falhas_recentes = AuditoriaAcaoCritica.objects.filter(
   43 |         acao=AuditoriaAcaoCritica.Acao.LOGIN_FALHO,
   44 |         criado_em__gte=inicio_janela,
   45 |     )
   46 | 
   47 |     if email:
   48 |         falhas_recentes = falhas_recentes.filter(metadados__email=email)
   49 |     elif ip:
   50 |         falhas_recentes = falhas_recentes.filter(ip=ip)
   51 | 
   52 |     if falhas_recentes.count() >= LIMITE_LOGIN_SUSPEITO:
   53 |         registrar_auditoria(
   54 |             acao=AuditoriaAcaoCritica.Acao.LOGIN_SUSPEITO,
   55 |             resultado=AuditoriaAcaoCritica.Resultado.FALHA,
   56 |             descricao="Muitas tentativas de login falhas em curto periodo.",
   57 |             request=request,
   58 |             ip=ip,
   59 |             user_agent=user_agent,
   60 |             metadados={
   61 |                 "email": email,
   62 |                 "falhas_recentes": falhas_recentes.count(),
   63 |                 "janela_minutos": JANELA_LOGIN_SUSPEITO_MINUTOS,
   64 |             },
   65 |         )
``````

## accounts/test_estoque.py

Original: [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py>).

``````text
    1 | """
    2 | Testes automatizados do estoque (UC_29 - Cadastrar Estoque e
    3 | UC_30 - Atualizar Estoque).
    4 | 
    5 | Cobrem:
    6 | - calculo do status (critico/baixo/estavel);
    7 | - cadastro de estoque, incluindo bloqueios (nao aprovado, duplicado,
    8 |   niveis incoerentes);
    9 | - movimentacoes de entrada, saida e ajuste, incluindo bloqueios (saida
   10 |   maior que o disponivel, estoque de outro hemocentro);
   11 | - geracao de historico (EstoqueMovimentacao) e auditoria
   12 |   (AuditoriaAcaoCritica) a cada operacao;
   13 | - as views, por meio do client de testes do Django.
   14 | 
   15 | Execute com: ``python manage.py test accounts.test_estoque``.
   16 | """
   17 | 
   18 | from django.core.exceptions import PermissionDenied, ValidationError
   19 | from django.test import TestCase
   20 | from django.urls import reverse
   21 | 
   22 | from .estoque import (
   23 |     calcular_status_calculado,
   24 |     cadastrar_estoque,
   25 |     registrar_movimentacao_estoque,
   26 | )
   27 | from .models import AuditoriaAcaoCritica, Estoque, EstoqueMovimentacao, Usuario
   28 | from .validacao_hemocentro import aprovar_hemocentro
   29 | 
   30 | 
   31 | class EstoqueTestsBase(TestCase):
   32 |     """Prepara um administrador e Hemocentros usados pelos testes."""
   33 | 
   34 |     def criar_usuario(self, *, email, nome, perfil):
   35 |         return Usuario.objects.create_user(
   36 |             email=email,
   37 |             password="SenhaForte123!",
   38 |             nome=nome,
   39 |             perfil=perfil,
   40 |         )
   41 | 
   42 |     def setUp(self):
   43 |         self.admin = self.criar_usuario(
   44 |             email="admin@elo.test",
   45 |             nome="Administrador Elo",
   46 |             perfil=Usuario.Perfil.ADMINISTRADOR,
   47 |         )
   48 | 
   49 |         self.hemocentro = self.criar_usuario(
   50 |             email="hemocentro@elo.test",
   51 |             nome="Hemocentro Elo",
   52 |             perfil=Usuario.Perfil.HEMOCENTRO,
   53 |         )
   54 |         aprovar_hemocentro(hemocentro=self.hemocentro, admin=self.admin)
   55 |         self.hemocentro.refresh_from_db()
   56 | 
   57 |         self.hemocentro_pendente = self.criar_usuario(
   58 |             email="pendente@elo.test",
   59 |             nome="Hemocentro Pendente",
   60 |             perfil=Usuario.Perfil.HEMOCENTRO,
   61 |         )
   62 | 
   63 |         self.doador = self.criar_usuario(
   64 |             email="doador@elo.test",
   65 |             nome="Doador Elo",
   66 |             perfil=Usuario.Perfil.DOADOR,
   67 |         )
   68 | 
   69 | 
   70 | class CalcularStatusCalculadoTests(TestCase):
   71 |     """Testa a regra pura de calculo de status, sem tocar o banco."""
   72 | 
   73 |     def test_quantidade_igual_ao_critico_e_critico(self):
   74 |         self.assertEqual(
   75 |             calcular_status_calculado(
   76 |                 quantidade_bolsas=5, nivel_minimo=10, nivel_critico=5
   77 |             ),
   78 |             Estoque.StatusCalculado.CRITICO,
   79 |         )
   80 | 
   81 |     def test_quantidade_abaixo_do_critico_e_critico(self):
   82 |         self.assertEqual(
   83 |             calcular_status_calculado(
   84 |                 quantidade_bolsas=0, nivel_minimo=10, nivel_critico=5
   85 |             ),
   86 |             Estoque.StatusCalculado.CRITICO,
   87 |         )
   88 | 
   89 |     def test_quantidade_igual_ao_minimo_e_baixo(self):
   90 |         self.assertEqual(
   91 |             calcular_status_calculado(
   92 |                 quantidade_bolsas=10, nivel_minimo=10, nivel_critico=5
   93 |             ),
   94 |             Estoque.StatusCalculado.BAIXO,
   95 |         )
   96 | 
   97 |     def test_quantidade_acima_do_minimo_e_estavel(self):
   98 |         self.assertEqual(
   99 |             calcular_status_calculado(
  100 |                 quantidade_bolsas=11, nivel_minimo=10, nivel_critico=5
  101 |             ),
  102 |             Estoque.StatusCalculado.ESTAVEL,
  103 |         )
  104 | 
  105 | 
  106 | class CadastrarEstoqueTests(EstoqueTestsBase):
  107 |     """Testes principais do UC_29."""
  108 | 
  109 |     def test_hemocentro_aprovado_cadastra_estoque(self):
  110 |         estoque = cadastrar_estoque(
  111 |             hemocentro=self.hemocentro,
  112 |             tipo_sanguineo="o-",  # minusculo de proposito: deve normalizar
  113 |             quantidade_bolsas=8,
  114 |             nivel_minimo=10,
  115 |             nivel_critico=5,
  116 |         )
  117 | 
  118 |         self.assertEqual(estoque.tipo_sanguineo, "O-")
  119 |         self.assertEqual(estoque.status_calculado, Estoque.StatusCalculado.BAIXO)
  120 | 
  121 |         self.assertTrue(
  122 |             AuditoriaAcaoCritica.objects.filter(
  123 |                 acao=AuditoriaAcaoCritica.Acao.CADASTRO_ESTOQUE,
  124 |                 usuario=self.hemocentro,
  125 |                 alvo_id=str(estoque.pk),
  126 |             ).exists()
  127 |         )
  128 | 
  129 |     def test_hemocentro_pendente_nao_pode_cadastrar_estoque(self):
  130 |         with self.assertRaises(PermissionDenied):
  131 |             cadastrar_estoque(
  132 |                 hemocentro=self.hemocentro_pendente,
  133 |                 tipo_sanguineo="O+",
  134 |                 nivel_minimo=10,
  135 |                 nivel_critico=5,
  136 |             )
  137 | 
  138 |     def test_nao_permite_cadastro_duplicado(self):
  139 |         cadastrar_estoque(
  140 |             hemocentro=self.hemocentro,
  141 |             tipo_sanguineo="A+",
  142 |             nivel_minimo=10,
  143 |             nivel_critico=5,
  144 |         )
  145 | 
  146 |         with self.assertRaises(ValidationError):
  147 |             cadastrar_estoque(
  148 |                 hemocentro=self.hemocentro,
  149 |                 tipo_sanguineo="A+",
  150 |                 nivel_minimo=20,
  151 |                 nivel_critico=10,
  152 |             )
  153 | 
  154 |     def test_nivel_critico_maior_que_minimo_gera_erro(self):
  155 |         with self.assertRaises(ValidationError):
  156 |             cadastrar_estoque(
  157 |                 hemocentro=self.hemocentro,
  158 |                 tipo_sanguineo="B+",
  159 |                 nivel_minimo=5,
  160 |                 nivel_critico=10,
  161 |             )
  162 | 
  163 |     def test_tipo_sanguineo_invalido_gera_erro(self):
  164 |         with self.assertRaises(ValueError):
  165 |             cadastrar_estoque(
  166 |                 hemocentro=self.hemocentro,
  167 |                 tipo_sanguineo="C+",
  168 |                 nivel_minimo=10,
  169 |                 nivel_critico=5,
  170 |             )
  171 | 
  172 | 
  173 | class RegistrarMovimentacaoEstoqueTests(EstoqueTestsBase):
  174 |     """Testes principais do UC_30."""
  175 | 
  176 |     def setUp(self):
  177 |         super().setUp()
  178 | 
  179 |         self.estoque = cadastrar_estoque(
  180 |             hemocentro=self.hemocentro,
  181 |             tipo_sanguineo="O-",
  182 |             quantidade_bolsas=10,
  183 |             nivel_minimo=10,
  184 |             nivel_critico=5,
  185 |         )
  186 | 
  187 |     def test_entrada_soma_quantidade_e_recalcula_status(self):
  188 |         movimentacao = registrar_movimentacao_estoque(
  189 |             estoque=self.estoque,
  190 |             usuario_resp=self.hemocentro,
  191 |             tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
  192 |             quantidade=15,
  193 |             motivo="Doação recebida em mutirão.",
  194 |         )
  195 | 
  196 |         self.estoque.refresh_from_db()
  197 | 
  198 |         self.assertEqual(movimentacao.quantidade_anterior, 10)
  199 |         self.assertEqual(movimentacao.quantidade_movimentada, 15)
  200 |         self.assertEqual(movimentacao.quantidade_nova, 25)
  201 |         self.assertEqual(self.estoque.quantidade_bolsas, 25)
  202 |         self.assertEqual(self.estoque.status_calculado, Estoque.StatusCalculado.ESTAVEL)
  203 | 
  204 |     def test_saida_subtrai_quantidade(self):
  205 |         movimentacao = registrar_movimentacao_estoque(
  206 |             estoque=self.estoque,
  207 |             usuario_resp=self.hemocentro,
  208 |             tipo_movimento=EstoqueMovimentacao.TipoMovimento.SAIDA,
  209 |             quantidade=6,
  210 |             motivo="Transfusão de emergência.",
  211 |         )
  212 | 
  213 |         self.estoque.refresh_from_db()
  214 | 
  215 |         self.assertEqual(movimentacao.quantidade_nova, 4)
  216 |         self.assertEqual(self.estoque.quantidade_bolsas, 4)
  217 |         self.assertEqual(self.estoque.status_calculado, Estoque.StatusCalculado.CRITICO)
  218 | 
  219 |     def test_saida_maior_que_estoque_gera_erro_e_nao_altera_nada(self):
  220 |         with self.assertRaises(ValidationError):
  221 |             registrar_movimentacao_estoque(
  222 |                 estoque=self.estoque,
  223 |                 usuario_resp=self.hemocentro,
  224 |                 tipo_movimento=EstoqueMovimentacao.TipoMovimento.SAIDA,
  225 |                 quantidade=999,
  226 |                 motivo="Saída solicitada acima do estoque disponível.",
  227 |             )
  228 | 
  229 |         self.estoque.refresh_from_db()
  230 |         self.assertEqual(self.estoque.quantidade_bolsas, 10)
  231 |         self.assertEqual(
  232 |             EstoqueMovimentacao.objects.filter(estoque=self.estoque).count(), 0
  233 |         )
  234 | 
  235 |     def test_ajuste_define_quantidade_absoluta_e_aceita_delta_negativo(self):
  236 |         movimentacao = registrar_movimentacao_estoque(
  237 |             estoque=self.estoque,
  238 |             usuario_resp=self.hemocentro,
  239 |             tipo_movimento=EstoqueMovimentacao.TipoMovimento.AJUSTE,
  240 |             quantidade=3,
  241 |             motivo="Contagem física apontou divergência.",
  242 |         )
  243 | 
  244 |         self.estoque.refresh_from_db()
  245 | 
  246 |         self.assertEqual(movimentacao.quantidade_anterior, 10)
  247 |         self.assertEqual(movimentacao.quantidade_movimentada, -7)
  248 |         self.assertEqual(movimentacao.quantidade_nova, 3)
  249 |         self.assertEqual(self.estoque.quantidade_bolsas, 3)
  250 | 
  251 |     def test_motivo_e_obrigatorio_na_movimentacao(self):
  252 |         with self.assertRaises(ValidationError):
  253 |             registrar_movimentacao_estoque(
  254 |                 estoque=self.estoque,
  255 |                 usuario_resp=self.hemocentro,
  256 |                 tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
  257 |                 quantidade=2,
  258 |                 motivo="   ",
  259 |             )
  260 | 
  261 |         self.estoque.refresh_from_db()
  262 |         self.assertEqual(self.estoque.quantidade_bolsas, 10)
  263 |         self.assertEqual(
  264 |             EstoqueMovimentacao.objects.filter(estoque=self.estoque).count(),
  265 |             0,
  266 |         )
  267 | 
  268 |     def test_movimentacao_gera_historico_e_auditoria(self):
  269 |         registrar_movimentacao_estoque(
  270 |             estoque=self.estoque,
  271 |             usuario_resp=self.hemocentro,
  272 |             tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
  273 |             quantidade=2,
  274 |             motivo="Reposição do estoque.",
  275 |         )
  276 | 
  277 |         self.assertEqual(
  278 |             EstoqueMovimentacao.objects.filter(estoque=self.estoque).count(), 1
  279 |         )
  280 |         self.assertTrue(
  281 |             AuditoriaAcaoCritica.objects.filter(
  282 |                 acao=AuditoriaAcaoCritica.Acao.ATUALIZACAO_ESTOQUE,
  283 |                 usuario=self.hemocentro,
  284 |                 alvo_id=str(self.estoque.pk),
  285 |             ).exists()
  286 |         )
  287 | 
  288 |     def test_outro_hemocentro_nao_pode_movimentar_estoque_alheio(self):
  289 |         outro_hemocentro = self.criar_usuario(
  290 |             email="outro@elo.test",
  291 |             nome="Outro Hemocentro",
  292 |             perfil=Usuario.Perfil.HEMOCENTRO,
  293 |         )
  294 |         aprovar_hemocentro(hemocentro=outro_hemocentro, admin=self.admin)
  295 |         outro_hemocentro.refresh_from_db()
  296 | 
  297 |         with self.assertRaises(PermissionDenied):
  298 |             registrar_movimentacao_estoque(
  299 |                 estoque=self.estoque,
  300 |                 usuario_resp=outro_hemocentro,
  301 |                 tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
  302 |                 quantidade=1,
  303 |             )
  304 | 
  305 |     def test_doador_nao_pode_movimentar_estoque(self):
  306 |         with self.assertRaises(PermissionDenied):
  307 |             registrar_movimentacao_estoque(
  308 |                 estoque=self.estoque,
  309 |                 usuario_resp=self.doador,
  310 |                 tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
  311 |                 quantidade=1,
  312 |             )
  313 | 
  314 | 
  315 | class EstoqueViewsTests(EstoqueTestsBase):
  316 |     """Testes de ponta a ponta usando o client de testes do Django."""
  317 | 
  318 |     def test_painel_bloqueia_hemocentro_pendente(self):
  319 |         self.client.force_login(self.hemocentro_pendente)
  320 | 
  321 |         resposta = self.client.get(reverse("accounts:estoque_hemocentro"))
  322 | 
  323 |         self.assertEqual(resposta.status_code, 403)
  324 | 
  325 |     def test_post_cadastra_estoque_via_view(self):
  326 |         self.client.force_login(self.hemocentro)
  327 | 
  328 |         resposta = self.client.post(
  329 |             reverse("accounts:cadastrar_estoque"),
  330 |             {
  331 |                 "tipo_sanguineo": "AB+",
  332 |                 "quantidade_bolsas": 4,
  333 |                 "nivel_minimo": 10,
  334 |                 "nivel_critico": 5,
  335 |             },
  336 |         )
  337 | 
  338 |         self.assertRedirects(resposta, reverse("accounts:estoque_hemocentro"))
  339 |         self.assertTrue(
  340 |             Estoque.objects.filter(
  341 |                 hemocentro=self.hemocentro, tipo_sanguineo="AB+"
  342 |             ).exists()
  343 |         )
  344 | 
  345 |     def test_post_movimenta_estoque_via_view(self):
  346 |         estoque = cadastrar_estoque(
  347 |             hemocentro=self.hemocentro,
  348 |             tipo_sanguineo="B-",
  349 |             quantidade_bolsas=5,
  350 |             nivel_minimo=10,
  351 |             nivel_critico=5,
  352 |         )
  353 | 
  354 |         self.client.force_login(self.hemocentro)
  355 | 
  356 |         resposta = self.client.post(
  357 |             reverse("accounts:atualizar_estoque", kwargs={"id_estoque": estoque.pk}),
  358 |             {
  359 |                 "tipo_movimento": EstoqueMovimentacao.TipoMovimento.ENTRADA,
  360 |                 "quantidade": 5,
  361 |                 "motivo": "Reposição semanal.",
  362 |             },
  363 |         )
  364 | 
  365 |         self.assertRedirects(resposta, reverse("accounts:estoque_hemocentro"))
  366 | 
  367 |         estoque.refresh_from_db()
  368 |         self.assertEqual(estoque.quantidade_bolsas, 10)
  369 | 
  370 |         painel = self.client.get(reverse("accounts:estoque_hemocentro"))
  371 |         self.assertContains(painel, "Reposição semanal.")
  372 |         self.assertContains(painel, "Hemocentro Elo")
``````

## accounts/test_fluxo_requisitos.py

Original: [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py>).

``````text
    1 | from django.core.exceptions import PermissionDenied
    2 | from django.test import TestCase
    3 | from django.urls import reverse
    4 | 
    5 | from .forms import CadastroUsuarioForm
    6 | from .models import (
    7 |     ConsentimentoLGPD,
    8 |     Notificacao,
    9 |     PedidoSangue,
   10 |     Triagem,
   11 |     Usuario,
   12 | )
   13 | from .triagem_servico import atualizar_tipo_sanguineo_do_usuario
   14 | from .validacao_hemocentro import aprovar_hemocentro
   15 | from .validacao_pedido import aprovar_pedido, criar_pedido_pendente
   16 | 
   17 | 
   18 | class FluxoCadastroTriagemPedidosTests(TestCase):
   19 |     def usuario(self, email, perfil, **extras):
   20 |         return Usuario.objects.create_user(
   21 |             email=email,
   22 |             password="SenhaForte123!",
   23 |             nome=extras.pop("nome", perfil.title()),
   24 |             perfil=perfil,
   25 |             **extras,
   26 |         )
   27 | 
   28 |     def setUp(self):
   29 |         self.admin = self.usuario(
   30 |             "admin@elo.test",
   31 |             Usuario.Perfil.ADMINISTRADOR,
   32 |         )
   33 |         self.doador = self.usuario(
   34 |             "doador@elo.test",
   35 |             Usuario.Perfil.DOADOR,
   36 |         )
   37 |         self.receptor = self.usuario(
   38 |             "receptor@elo.test",
   39 |             Usuario.Perfil.RECEPTOR,
   40 |         )
   41 |         self.observador = self.usuario(
   42 |             "observador@elo.test",
   43 |             Usuario.Perfil.OBSERVADOR,
   44 |         )
   45 |         self.hemocentro = self.usuario(
   46 |             "hemocentro@elo.test",
   47 |             Usuario.Perfil.HEMOCENTRO,
   48 |             cidade="Belo Horizonte",
   49 |         )
   50 | 
   51 |         aprovar_hemocentro(
   52 |             hemocentro=self.hemocentro,
   53 |             admin=self.admin,
   54 |         )
   55 |         self.hemocentro.refresh_from_db()
   56 | 
   57 |     def dados_solicitacao(self):
   58 |         return {
   59 |             "nome_solicitante": "Pessoa solicitante",
   60 |             "contato": "solicitante@elo.test",
   61 |             "para_quem": PedidoSangue.ParaQuem.MIM,
   62 |             "hemocentro_destino": self.hemocentro.pk,
   63 |             "titulo": "Necessidade de sangue",
   64 |             "tipo_sanguineo": "O-",
   65 |             "urgencia": PedidoSangue.Urgencia.MEDIA,
   66 |             "cidade": "Belo Horizonte",
   67 |             "nome_paciente": "Paciente",
   68 |             "descricao": (
   69 |                 "Necessidade de doadores para atendimento hospitalar."
   70 |             ),
   71 |             "justificativa_urgencia": "",
   72 |             "informacoes_complementares": (
   73 |                 "Retorno pelo contato informado."
   74 |             ),
   75 |         }
   76 | 
   77 |     def test_cadastro_nao_permite_admin_e_exige_consentimento(self):
   78 |         resposta = self.client.post(
   79 |             reverse("accounts:cadastro"),
   80 |             {
   81 |                 "nome": "Nova pessoa",
   82 |                 "email": "nova@elo.test",
   83 |                 "perfil": Usuario.Perfil.OBSERVADOR,
   84 |                 "password1": "SenhaForte123!",
   85 |                 "password2": "SenhaForte123!",
   86 |                 "aceite_lgpd": "",
   87 |             },
   88 |         )
   89 | 
   90 |         self.assertEqual(resposta.status_code, 200)
   91 |         self.assertFalse(
   92 |             Usuario.objects.filter(
   93 |                 email="nova@elo.test"
   94 |             ).exists()
   95 |         )
   96 | 
   97 |         self.assertNotIn(
   98 |             Usuario.Perfil.ADMINISTRADOR,
   99 |             dict(
  100 |                 CadastroUsuarioForm().fields["perfil"].choices
  101 |             ),
  102 |         )
  103 | 
  104 |     def test_cadastro_valido_grava_senha_hash_e_consentimento(self):
  105 |         resposta = self.client.post(
  106 |             reverse("accounts:cadastro"),
  107 |             {
  108 |                 "nome": "Doador cadastrado",
  109 |                 "email": "cadastro@elo.test",
  110 |                 "perfil": Usuario.Perfil.DOADOR,
  111 |                 "cpf": "12345678901",
  112 |                 "data_nascimento": "1990-01-01",
  113 |                 "password1": "SenhaForte123!",
  114 |                 "password2": "SenhaForte123!",
  115 |                 "aceite_lgpd": "on",
  116 |             },
  117 |         )
  118 | 
  119 |         self.assertRedirects(
  120 |             resposta,
  121 |             reverse("accounts:dashboard"),
  122 |         )
  123 | 
  124 |         usuario = Usuario.objects.get(
  125 |             email="cadastro@elo.test"
  126 |         )
  127 | 
  128 |         self.assertTrue(
  129 |             usuario.check_password("SenhaForte123!")
  130 |         )
  131 |         self.assertNotEqual(
  132 |             usuario.password,
  133 |             "SenhaForte123!",
  134 |         )
  135 | 
  136 |         self.assertTrue(
  137 |             ConsentimentoLGPD.objects.filter(
  138 |                 usuario=usuario,
  139 |                 tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL,
  140 |                 aceito=True,
  141 |             ).exists()
  142 |         )
  143 | 
  144 |     def test_cadastro_de_hemocentro_inicia_pendente_e_nao_libera_estoque(
  145 |         self,
  146 |     ):
  147 |         resposta = self.client.post(
  148 |             reverse("accounts:cadastro"),
  149 |             {
  150 |                 "nome": "Hemocentro cadastrado",
  151 |                 "email": "novo-hemocentro@elo.test",
  152 |                 "perfil": Usuario.Perfil.HEMOCENTRO,
  153 |                 "cnpj": "12345678000195",
  154 |                 "cidade": "Belo Horizonte",
  155 |                 "estado": "MG",
  156 |                 "password1": "SenhaForte123!",
  157 |                 "password2": "SenhaForte123!",
  158 |                 "aceite_lgpd": "on",
  159 |             },
  160 |         )
  161 | 
  162 |         self.assertRedirects(
  163 |             resposta,
  164 |             reverse("accounts:dashboard"),
  165 |         )
  166 | 
  167 |         hemocentro = Usuario.objects.get(
  168 |             email="novo-hemocentro@elo.test"
  169 |         )
  170 | 
  171 |         self.assertEqual(
  172 |             hemocentro.status_validacao,
  173 |             Usuario.StatusValidacaoHemocentro.PENDENTE,
  174 |         )
  175 | 
  176 |         estoque = self.client.get(
  177 |             reverse("accounts:estoque_hemocentro")
  178 |         )
  179 | 
  180 |         self.assertEqual(estoque.status_code, 403)
  181 | 
  182 |     def test_login_bloqueia_conta_suspensa(self):
  183 |         self.doador.suspensa = True
  184 |         self.doador.save(update_fields=["suspensa"])
  185 | 
  186 |         resposta = self.client.post(
  187 |             reverse("accounts:login"),
  188 |             {
  189 |                 "username": self.doador.email,
  190 |                 "password": "SenhaForte123!",
  191 |             },
  192 |         )
  193 | 
  194 |         self.assertEqual(resposta.status_code, 200)
  195 |         self.assertNotIn(
  196 |             "_auth_user_id",
  197 |             self.client.session,
  198 |         )
  199 | 
  200 |     def test_triagem_exige_aceite_explicito(self):
  201 |         self.client.force_login(self.doador)
  202 | 
  203 |         url = reverse(
  204 |             "accounts:triagem_iniciar",
  205 |             kwargs={"modalidade": "extensa"},
  206 |         )
  207 | 
  208 |         self.client.post(url)
  209 | 
  210 |         self.assertFalse(
  211 |             Triagem.objects.filter(
  212 |                 usuario=self.doador
  213 |             ).exists()
  214 |         )
  215 | 
  216 |         resposta = self.client.post(
  217 |             url,
  218 |             {"aceite_termo": "on"},
  219 |         )
  220 | 
  221 |         self.assertEqual(resposta.status_code, 302)
  222 | 
  223 |         self.assertTrue(
  224 |             ConsentimentoLGPD.objects.filter(
  225 |                 usuario=self.doador,
  226 |                 tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM,
  227 |             ).exists()
  228 |         )
  229 | 
  230 |     def test_solicitacao_nao_publica_e_hemocentro_publica(self):
  231 |         self.client.force_login(self.receptor)
  232 |         resposta = self.client.post(
  233 |             reverse("accounts:pedido_publicar"),
  234 |             self.dados_solicitacao(),
  235 |         )
  236 | 
  237 |         self.assertEqual(resposta.status_code, 302)
  238 | 
  239 |         pedido = PedidoSangue.objects.get()
  240 | 
  241 |         self.assertEqual(
  242 |             pedido.status,
  243 |             PedidoSangue.Status.ENVIADA,
  244 |         )
  245 | 
  246 |         with self.assertRaises(PermissionDenied):
  247 |             aprovar_pedido(
  248 |                 pedido=pedido,
  249 |                 moderador=self.admin,
  250 |             )
  251 | 
  252 |         aprovar_pedido(
  253 |             pedido=pedido,
  254 |             moderador=self.hemocentro,
  255 |         )
  256 | 
  257 |         pedido.refresh_from_db()
  258 | 
  259 |         self.assertEqual(
  260 |             pedido.status,
  261 |             PedidoSangue.Status.PUBLICADA,
  262 |         )
  263 |         self.assertEqual(
  264 |             pedido.publicado_por,
  265 |             self.hemocentro,
  266 |         )
  267 | 
  268 |     def test_observador_pode_solicitar_mas_nao_analisar(self):
  269 |         self.client.force_login(self.observador)
  270 | 
  271 |         resposta = self.client.get(
  272 |             reverse("accounts:painel_pedidos_hemocentro")
  273 |         )
  274 | 
  275 |         self.assertEqual(resposta.status_code, 403)
  276 | 
  277 |     def test_receptor_acompanha_somente_suas_solicitacoes(self):
  278 |         pedido = criar_pedido_pendente(
  279 |             dados={
  280 |                 **self.dados_solicitacao(),
  281 |                 "contato": "receptor@elo.test",
  282 |             },
  283 |             solicitante=self.receptor,
  284 |         )
  285 | 
  286 |         self.client.force_login(self.receptor)
  287 | 
  288 |         resposta = self.client.get(
  289 |             reverse("accounts:minhas_solicitacoes")
  290 |         )
  291 | 
  292 |         self.assertContains(resposta, str(pedido.pk))
  293 |         self.assertNotContains(resposta, "outra-pessoa")
  294 | 
  295 |     def test_tipo_sanguineo_confirmado_nao_e_sobrescrito_pela_triagem(
  296 |         self,
  297 |     ):
  298 |         self.doador.tipo_sanguineo = "A+"
  299 |         self.doador.tipo_sanguineo_confirmado = True
  300 |         self.doador.save(
  301 |             update_fields=[
  302 |                 "tipo_sanguineo",
  303 |                 "tipo_sanguineo_confirmado",
  304 |             ]
  305 |         )
  306 | 
  307 |         triagem = Triagem.objects.create(
  308 |             usuario=self.doador
  309 |         )
  310 | 
  311 |         atualizar_tipo_sanguineo_do_usuario(
  312 |             triagem,
  313 |             {"codigos": ["O+"]},
  314 |         )
  315 | 
  316 |         self.doador.refresh_from_db()
  317 | 
  318 |         self.assertEqual(
  319 |             self.doador.tipo_sanguineo,
  320 |             "A+",
  321 |         )
  322 | 
  323 |     def test_publicacao_notifica_somente_doador_apto_compativel(self):
  324 |         from .compatibilidade import atualizar_preferencia_convocacao
  325 |         atualizar_preferencia_convocacao(self.doador, True)
  326 |         self.doador.tipo_sanguineo = "O-"
  327 |         self.doador.save(
  328 |             update_fields=["tipo_sanguineo"]
  329 |         )
  330 | 
  331 |         Triagem.objects.create(
  332 |             usuario=self.doador,
  333 |             status=Triagem.Status.CONCLUIDA,
  334 |             resultado=Triagem.Resultado.APTO,
  335 |         )
  336 | 
  337 |         pedido = criar_pedido_pendente(
  338 |             dados=self.dados_solicitacao(),
  339 |             solicitante=self.receptor,
  340 |         )
  341 | 
  342 |         aprovar_pedido(
  343 |             pedido=pedido,
  344 |             moderador=self.hemocentro,
  345 |         )
  346 | 
  347 |         self.assertTrue(
  348 |             Notificacao.objects.filter(
  349 |                 usuario=self.doador,
  350 |                 pedido=pedido,
  351 |                 tipo=Notificacao.Tipo.PEDIDO_COMPATIVEL,
  352 |             ).exists()
  353 |         )
  354 | 
  355 | class ConvocacaoCompatibilidadeTests(TestCase):
  356 |     @classmethod
  357 |     def setUpTestData(cls):
  358 |         from .models import Estoque
  359 |         cls.hemocentro = Usuario.objects.create_user(
  360 |             email='hemo.convocacao@elo.test', nome='Hemocentro', perfil=Usuario.Perfil.HEMOCENTRO,
  361 |             status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO,
  362 |             cidade='Belo Horizonte',
  363 |         )
  364 |         cls.estoque = Estoque.objects.create(hemocentro=cls.hemocentro, tipo_sanguineo='O-',
  365 |             quantidade_bolsas=0, nivel_minimo=10, nivel_critico=5, status_calculado=Estoque.StatusCalculado.CRITICO)
  366 |         cls.pedido = PedidoSangue.objects.create(hemocentro_destino=cls.hemocentro,
  367 |             nome_solicitante='Solicitante', contato='contato@elo.test', para_quem=PedidoSangue.ParaQuem.MIM,
  368 |             tipo_sanguineo='O-', cidade='Belo Horizonte', urgencia=PedidoSangue.Urgencia.MEDIA,
  369 |             descricao='Pedido publicado para testar convocacao.', status=PedidoSangue.Status.PUBLICADA)
  370 | 
  371 |     def doador(self, nome, **extras):
  372 |         usuario = Usuario.objects.create_user(email=nome+'@convocacao.test', nome=nome,
  373 |             perfil=extras.pop('perfil', Usuario.Perfil.DOADOR), tipo_sanguineo=extras.pop('tipo_sanguineo', 'O-'),
  374 |             **extras)
  375 |         Triagem.objects.create(usuario=usuario, status=Triagem.Status.CONCLUIDA,
  376 |             resultado=Triagem.Resultado.APTO)
  377 |         ConsentimentoLGPD.objects.create(usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
  378 |             versao_termo='1.0', aceito=True)
  379 |         return usuario
  380 | 
  381 |     def emitir(self, origem):
  382 |         from .estoque import criar_notificacoes_para_doadores_compativeis
  383 |         from .pedidos import criar_notificacoes_para_pedido
  384 |         from .models import Estoque
  385 |         if origem == 'estoque':
  386 |             return criar_notificacoes_para_doadores_compativeis(estoque=self.estoque,
  387 |                 status_calculado=Estoque.StatusCalculado.CRITICO)
  388 |         return criar_notificacoes_para_pedido(pedido=self.pedido)
  389 | 
  390 |     def test_ambos_fluxos_exigem_todos_os_criterios(self):
  391 |         from django.utils import timezone
  392 |         from datetime import timedelta
  393 |         apto = self.doador('apto')
  394 |         self.doador('incompativel', tipo_sanguineo='A+')
  395 |         self.doador('suspenso', suspensa=True)
  396 |         self.doador('inativo', is_active=False)
  397 |         self.doador('preferencia_desativada', aceita_notificacoes_pedidos=False)
  398 |         self.doador('receptor', perfil=Usuario.Perfil.RECEPTOR)
  399 |         revogado = self.doador('revogado')
  400 |         revogado.consentimentos_lgpd.update(revogado_em=timezone.now())
  401 |         recusou = self.doador('recusou')
  402 |         recusou.consentimentos_lgpd.update(aceito=False)
  403 |         sem_consentimento = self.doador('sem_consentimento')
  404 |         sem_consentimento.consentimentos_lgpd.all().delete()
  405 |         versao_antiga = self.doador('versao_antiga')
  406 |         versao_antiga.consentimentos_lgpd.update(versao_termo='0.9')
  407 |         futuro = self.doador('futuro')
  408 |         futuro.triagens.update(data_liberacao=timezone.localdate()+timedelta(days=1))
  409 |         sem_triagem = self.doador('sem_triagem')
  410 |         sem_triagem.triagens.all().delete()
  411 |         inapto = self.doador('inapto')
  412 |         Triagem.objects.create(usuario=inapto, status=Triagem.Status.CONCLUIDA,
  413 |             resultado=Triagem.Resultado.INAPTO_TEMPORARIO, finalizada_em=timezone.now())
  414 |         for origem in ('estoque', 'pedido'):
  415 |             with self.subTest(origem=origem):
  416 |                 self.assertEqual(self.emitir(origem), 1)
  417 |                 self.assertEqual(list(Notificacao.objects.values_list('usuario_id', flat=True)), [apto.pk])
  418 |                 Notificacao.objects.all().delete()
  419 | 
  420 |     def test_limite_soma_estoque_e_pedido_mesmo_depois_de_lido(self):
  421 |         from datetime import timedelta
  422 |         from django.utils import timezone
  423 |         self.doador('frequencia')
  424 |         self.assertEqual(self.emitir('estoque'), 1)
  425 |         Notificacao.objects.update(lida=True)
  426 |         self.assertEqual(self.emitir('pedido'), 0)
  427 |         Notificacao.objects.update(criada_em=timezone.now()-timedelta(hours=25))
  428 |         self.assertEqual(self.emitir('pedido'), 1)
  429 |         self.assertEqual(self.emitir('pedido'), 0)
  430 | 
  431 |     def test_pedido_pendente_nao_convoca(self):
  432 |         self.doador('pendente')
  433 |         self.pedido.status = PedidoSangue.Status.ENVIADA
  434 |         self.assertEqual(self.emitir('pedido'), 0)
  435 | 
  436 |     def test_atualizacao_de_estoque_convoca_somente_quando_critico(self):
  437 |         from .estoque import registrar_movimentacao_estoque
  438 |         from .models import Estoque, EstoqueMovimentacao
  439 |         doador = self.doador('estoque_critico')
  440 |         for quantidade, status in (
  441 |             (7, Estoque.StatusCalculado.BAIXO),
  442 |             (12, Estoque.StatusCalculado.ESTAVEL),
  443 |             (5, Estoque.StatusCalculado.CRITICO),
  444 |         ):
  445 |             with self.subTest(status=status):
  446 |                 registrar_movimentacao_estoque(
  447 |                     estoque=self.estoque, usuario_resp=self.hemocentro,
  448 |                     tipo_movimento=EstoqueMovimentacao.TipoMovimento.AJUSTE,
  449 |                     quantidade=quantidade, motivo='Conferencia do estoque',
  450 |                 )
  451 |                 self.estoque.refresh_from_db()
  452 |                 self.assertEqual(self.estoque.status_calculado, status)
  453 |                 self.assertEqual(Notificacao.objects.count(), int(status == Estoque.StatusCalculado.CRITICO))
  454 |         notificacao = Notificacao.objects.get()
  455 |         self.assertEqual(notificacao.usuario_id, doador.pk)
  456 |         self.assertEqual(notificacao.tipo, Notificacao.Tipo.ESTOQUE_CRITICO)
  457 | 
  458 |     def test_preferencia_no_painel_registra_aceite_e_revogacao(self):
  459 |         from .models import AuditoriaAcaoCritica
  460 |         usuario = self.doador('painel')
  461 |         usuario.consentimentos_lgpd.all().delete()
  462 |         self.client.force_login(usuario)
  463 |         url = reverse('accounts:dashboard')
  464 |         self.assertContains(self.client.get(url), 'Alertas de doação')
  465 |         self.assertEqual(self.client.post(url, {'aceita_convocacoes': 'on'}).status_code, 302)
  466 |         consentimento = usuario.consentimentos_lgpd.get(tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES)
  467 |         self.assertTrue(consentimento.aceito)
  468 |         self.assertIsNone(consentimento.revogado_em)
  469 |         self.assertEqual(self.emitir('pedido'), 1)
  470 |         self.assertEqual(self.client.post(url, {}).status_code, 302)
  471 |         consentimento.refresh_from_db()
  472 |         usuario.refresh_from_db()
  473 |         self.assertFalse(usuario.aceita_notificacoes_pedidos)
  474 |         self.assertFalse(consentimento.aceito)
  475 |         self.assertIsNotNone(consentimento.revogado_em)
  476 |         self.assertTrue(AuditoriaAcaoCritica.objects.filter(metadados__evento='PREFERENCIA_CONVOCACAO').exists())
  477 |         Notificacao.objects.all().delete()
  478 |         self.assertEqual(self.emitir('estoque'), 0)
  479 | 
  480 |     def test_outro_perfil_nao_altera_preferencia(self):
  481 |         usuario = Usuario.objects.create_user(email='observador@convocacao.test', nome='Observador',
  482 |             perfil=Usuario.Perfil.OBSERVADOR)
  483 |         self.client.force_login(usuario)
  484 |         self.assertEqual(self.client.post(reverse('accounts:dashboard'), {'aceita_convocacoes': 'on'}).status_code, 403)
  485 |         self.assertFalse(usuario.consentimentos_lgpd.filter(tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES).exists())
  486 | 
  487 |     def test_cadastro_autorizacao_e_opcional_e_explicita(self):
  488 |         for aceita in (False, True):
  489 |             with self.subTest(aceita=aceita):
  490 |                 self.client.logout()
  491 |                 dados = {'nome': 'Doador', 'email': f'cadastro{int(aceita)}@convocacao.test',
  492 |                     'perfil': Usuario.Perfil.DOADOR, 'cpf': '12345678901' if not aceita else '12345678902', 'data_nascimento': '1990-01-01',
  493 |                     'password1': 'SenhaForte123!', 'password2': 'SenhaForte123!', 'aceite_lgpd': 'on'}
  494 |                 if aceita:
  495 |                     dados['aceita_notificacoes_pedidos'] = 'on'
  496 |                 self.assertEqual(self.client.post(reverse('accounts:cadastro'), dados).status_code, 302)
  497 |                 usuario = Usuario.objects.get(email=dados['email'])
  498 |                 self.assertEqual(usuario.aceita_notificacoes_pedidos, aceita)
  499 |                 self.assertEqual(usuario.consentimentos_lgpd.get(tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES).aceito, aceita)
  500 | 
  501 |     def test_publicacao_alternativa_tambem_convoca(self):
  502 |         from .forms import PedidoSangueForm
  503 |         from .pedidos import publicar_pedido
  504 |         self.doador('alternativa')
  505 |         form = PedidoSangueForm({'nome_solicitante': 'Solicitante', 'contato': 'contato@elo.test',
  506 |             'para_quem': PedidoSangue.ParaQuem.MIM, 'hemocentro_destino': self.hemocentro.pk,
  507 |             'titulo': 'Pedido alternativo', 'tipo_sanguineo': 'O-', 'urgencia': PedidoSangue.Urgencia.MEDIA,
  508 |             'cidade': 'Belo Horizonte', 'descricao': 'Precisamos de doadores para atendimento hospitalar.'})
  509 |         self.assertTrue(form.is_valid(), form.errors)
  510 |         pedido = publicar_pedido(self.hemocentro, form)
  511 |         self.assertTrue(Notificacao.objects.filter(pedido=pedido).exists())
  512 | 
  513 |     def test_compatibilidade_seleciona_os_tipos_da_tabela(self):
  514 |         from .compatibilidade import TIPOS_SANGUINEOS, COMPATIBILIDADE_RECEBIMENTO, doadores_aptos_para_convocacao
  515 |         for i, tipo in enumerate(TIPOS_SANGUINEOS):
  516 |             self.doador(f'tipo{i}', tipo_sanguineo=tipo)
  517 |         for solicitado, esperados in COMPATIBILIDADE_RECEBIMENTO.items():
  518 |             with self.subTest(tipo=solicitado):
  519 |                 encontrados = set(doadores_aptos_para_convocacao(solicitado).values_list('tipo_sanguineo', flat=True))
  520 |                 self.assertEqual(encontrados, set(esperados))
  521 | 
  522 |     def test_limite_e_compartilhado_tambem_quando_pedido_vem_primeiro(self):
  523 |         self.doador('pedido_primeiro')
  524 |         self.assertEqual(self.emitir('pedido'), 1)
  525 |         self.assertEqual(self.emitir('estoque'), 0)
  526 | 
  527 |     def test_limite_configuravel_nao_remove_protecao_contra_duplicatas(self):
  528 |         from django.test import override_settings
  529 |         self.doador('limite_configuravel')
  530 |         with override_settings(CONVOCACAO_LIMITE_NOTIFICACOES=3):
  531 |             self.assertEqual(self.emitir('pedido'), 1)
  532 |             self.assertEqual(self.emitir('pedido'), 0)
  533 |             self.assertEqual(self.emitir('estoque'), 1)
  534 |             self.assertEqual(self.emitir('estoque'), 0)
  535 | 
  536 | 
  537 | class CentralNotificacoesTests(TestCase):
  538 |     def setUp(self):
  539 |         self.usuario = Usuario.objects.create_user(
  540 |             email='central@elo.test', nome='Receptor', perfil=Usuario.Perfil.RECEPTOR,
  541 |         )
  542 |         self.outro = Usuario.objects.create_user(
  543 |             email='outra-central@elo.test', nome='Outro', perfil=Usuario.Perfil.RECEPTOR,
  544 |         )
  545 |         self.aviso = Notificacao.objects.create(
  546 |             usuario=self.usuario, titulo='Estoque urgente', mensagem='Precisamos de doadores.',
  547 |             tipo=Notificacao.Tipo.ESTOQUE_CRITICO, url_destino=reverse('accounts:estoque_publico'),
  548 |         )
  549 |         self.client.force_login(self.usuario)
  550 |         self.url = reverse('accounts:dashboard')
  551 | 
  552 |     def test_leitura_persiste_sem_apagar_historico_nem_regravar_data(self):
  553 |         dados = {'acao': 'marcar_notificacao_lida', 'id_notificacao': self.aviso.pk}
  554 |         self.assertEqual(self.client.post(self.url, dados).status_code, 302)
  555 |         self.aviso.refresh_from_db()
  556 |         self.assertTrue(self.aviso.lida)
  557 |         self.assertIsNotNone(self.aviso.lida_em)
  558 |         data_leitura = self.aviso.lida_em
  559 |         self.client.post(self.url, dados)
  560 |         self.aviso.refresh_from_db()
  561 |         self.assertEqual(self.aviso.lida_em, data_leitura)
  562 |         pagina = self.client.get(self.url)
  563 |         self.assertContains(pagina, 'Estoque urgente')
  564 |         self.assertContains(pagina, 'Ver estoque')
  565 |         self.assertContains(pagina, 'Lida')
  566 |         self.assertEqual(pagina.context['notificacoes_nao_lidas'], 0)
  567 | 
  568 |     def test_nao_permite_marcar_notificacao_de_outro_usuario(self):
  569 |         aviso = Notificacao.objects.create(usuario=self.outro, titulo='Privada', mensagem='Privada')
  570 |         self.assertEqual(self.client.post(self.url, {
  571 |             'acao': 'marcar_notificacao_lida', 'id_notificacao': aviso.pk,
  572 |         }).status_code, 404)
  573 |         aviso.refresh_from_db()
  574 |         self.assertFalse(aviso.lida)
  575 |         self.assertNotContains(self.client.get(self.url), 'Privada')
  576 | 
  577 |     def test_historico_paginado_mostra_notificacoes_mais_antigas(self):
  578 |         for numero in range(11):
  579 |             Notificacao.objects.create(usuario=self.usuario, titulo=f'Aviso {numero}', mensagem='Aviso')
  580 |         pagina = self.client.get(self.url)
  581 |         self.assertEqual(len(pagina.context['notificacoes_dashboard']), 10)
  582 |         self.assertContains(pagina, 'Próxima')
  583 |         self.assertContains(self.client.get(self.url, {'pagina_notificacoes': 2}), 'Estoque urgente')
  584 | 
  585 |     def test_identificador_invalido_e_anonimo_nao_marcam_leitura(self):
  586 |         self.assertEqual(self.client.post(self.url, {
  587 |             'acao': 'marcar_notificacao_lida', 'id_notificacao': 'invalido',
  588 |         }).status_code, 404)
  589 |         self.client.logout()
  590 |         self.assertEqual(self.client.post(self.url, {
  591 |             'acao': 'marcar_notificacao_lida', 'id_notificacao': self.aviso.pk,
  592 |         }).status_code, 302)
  593 |         self.aviso.refresh_from_db()
  594 |         self.assertFalse(self.aviso.lida)
``````

## accounts/test_pedidos.py

Original: [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py>).

``````text
    1 | from django.test import TestCase
    2 | from django.urls import reverse
    3 | 
    4 | from .forms import PedidoSangueForm
    5 | from .models import PedidoSangue, Usuario, ValidacaoPedido
    6 | from .validacao_hemocentro import aprovar_hemocentro
    7 | from .validacao_pedido import aprovar_pedido, criar_pedido_pendente, marcar_pedido_suspeito
    8 | 
    9 | 
   10 | class PedidoSangueTests(TestCase):
   11 |     def criar_usuario(self, *, email, nome, perfil, cidade="", estado=""):
   12 |         return Usuario.objects.create_user(
   13 |             email=email,
   14 |             password="SenhaForte123!",
   15 |             nome=nome,
   16 |             perfil=perfil,
   17 |             cidade=cidade,
   18 |             estado=estado,
   19 |         )
   20 | 
   21 |     def setUp(self):
   22 |         self.receptor = self.criar_usuario(
   23 |             email="receptor@elo.test",
   24 |             nome="Receptor Elo",
   25 |             perfil=Usuario.Perfil.RECEPTOR,
   26 |         )
   27 |         self.doador = self.criar_usuario(
   28 |             email="doador@elo.test",
   29 |             nome="Doador Elo",
   30 |             perfil=Usuario.Perfil.DOADOR,
   31 |         )
   32 |         self.administrador = self.criar_usuario(
   33 |             email="admin@elo.test",
   34 |             nome="Administrador Elo",
   35 |             perfil=Usuario.Perfil.ADMINISTRADOR,
   36 |         )
   37 |         self.hemocentro = self.criar_usuario(
   38 |             email="hemocentro@elo.test",
   39 |             nome="Hemocentro Muzambinho",
   40 |             perfil=Usuario.Perfil.HEMOCENTRO,
   41 |             cidade="Muzambinho",
   42 |             estado="MG",
   43 |         )
   44 |         aprovar_hemocentro(
   45 |             hemocentro=self.hemocentro,
   46 |             admin=self.administrador,
   47 |         )
   48 |         self.hemocentro.refresh_from_db()
   49 | 
   50 |         self.hemocentro_pendente = self.criar_usuario(
   51 |             email="pendente@elo.test",
   52 |             nome="Hemocentro Pendente",
   53 |             perfil=Usuario.Perfil.HEMOCENTRO,
   54 |             cidade="Alfenas",
   55 |             estado="MG",
   56 |         )
   57 | 
   58 |     def dados_validos(self, **alteracoes):
   59 |         dados = {
   60 |             "nome_solicitante": "Solicitante de exemplo",
   61 |             "contato": "receptor@elo.test",
   62 |             "para_quem": PedidoSangue.ParaQuem.OUTRA_PESSOA,
   63 |             "hemocentro_destino": self.hemocentro.pk,
   64 |             "titulo": "Doacao para paciente internado",
   65 |             "tipo_sanguineo": "O-",
   66 |             "urgencia": PedidoSangue.Urgencia.BAIXA,
   67 |             "cidade": "Muzambinho",
   68 |             "nome_paciente": "Paciente de exemplo",
   69 |             "descricao": (
   70 |                 "Precisamos de doadores para auxiliar um paciente internado."
   71 |             ),
   72 |             "justificativa_urgencia": "",
   73 |             "informacoes_complementares": "Retorno por telefone.",
   74 |         }
   75 |         dados.update(alteracoes)
   76 |         return dados
   77 | 
   78 |     def test_formulario_lista_apenas_hemocentros_aprovados(self):
   79 |         form = PedidoSangueForm()
   80 | 
   81 |         self.assertIn("para_quem", form.fields)
   82 |         self.assertIn("nome_paciente", form.fields)
   83 |         self.assertEqual(
   84 |             list(form.fields["hemocentro_destino"].queryset),
   85 |             [self.hemocentro],
   86 |         )
   87 | 
   88 |     def test_receptor_cria_solicitacao_enviada(self):
   89 |         self.client.force_login(self.receptor)
   90 | 
   91 |         resposta = self.client.post(
   92 |             reverse("accounts:pedido_publicar"),
   93 |             self.dados_validos(),
   94 |         )
   95 | 
   96 |         self.assertRedirects(resposta, reverse("accounts:minhas_solicitacoes"))
   97 |         pedido = PedidoSangue.objects.get()
   98 |         self.assertEqual(pedido.solicitante, self.receptor)
   99 |         self.assertEqual(pedido.hemocentro_destino, self.hemocentro)
  100 |         self.assertEqual(
  101 |             pedido.status,
  102 |             PedidoSangue.Status.ENVIADA,
  103 |         )
  104 | 
  105 |     def test_doador_nao_pode_enviar_solicitacao(self):
  106 |         self.client.force_login(self.doador)
  107 |         resposta = self.client.post(reverse("accounts:pedido_publicar"), self.dados_validos())
  108 |         self.assertRedirects(resposta, reverse("accounts:dashboard"))
  109 |         self.assertFalse(PedidoSangue.objects.exists())
  110 | 
  111 |     def test_visitante_precisa_entrar(self):
  112 |         url = reverse("accounts:pedido_publicar")
  113 |         resposta = self.client.get(url)
  114 |         self.assertRedirects(resposta, f"{reverse('accounts:login')}?next={url}")
  115 | 
  116 |     def test_formulario_rejeita_descricao_curta(self):
  117 |         form = PedidoSangueForm(self.dados_validos(descricao="Curto"))
  118 | 
  119 |         self.assertFalse(form.is_valid())
  120 |         self.assertIn("descricao", form.errors)
  121 | 
  122 |     def test_formulario_exige_email_no_contato(self):
  123 |         form_invalido = PedidoSangueForm(
  124 |             self.dados_validos(contato="(31) 99999-0000")
  125 |         )
  126 |         self.assertFalse(form_invalido.is_valid())
  127 |         self.assertIn("contato", form_invalido.errors)
  128 | 
  129 |         form_valido = PedidoSangueForm(
  130 |             self.dados_validos(contato="  Receptor@Elo.Test ")
  131 |         )
  132 |         self.assertTrue(form_valido.is_valid())
  133 |         self.assertEqual(
  134 |             form_valido.cleaned_data["contato"],
  135 |             "receptor@elo.test",
  136 |         )
  137 | 
  138 |     def test_formulario_rejeita_hemocentro_pendente(self):
  139 |         form = PedidoSangueForm(
  140 |             self.dados_validos(
  141 |                 hemocentro_destino=self.hemocentro_pendente.pk,
  142 |             )
  143 |         )
  144 | 
  145 |         self.assertFalse(form.is_valid())
  146 |         self.assertIn("hemocentro_destino", form.errors)
  147 | 
  148 |     def test_urgencia_critica_exige_justificativa(self):
  149 |         form = PedidoSangueForm(
  150 |             self.dados_validos(
  151 |                 urgencia=PedidoSangue.Urgencia.CRITICA,
  152 |                 justificativa_urgencia="Curta",
  153 |             )
  154 |         )
  155 | 
  156 |         self.assertFalse(form.is_valid())
  157 |         self.assertIn("justificativa_urgencia", form.errors)
  158 | 
  159 |     def test_hemocentro_aprova_pedido_e_registra_historico(self):
  160 |         self.client.force_login(self.receptor)
  161 |         self.client.post(
  162 |             reverse("accounts:pedido_publicar"),
  163 |             self.dados_validos(),
  164 |         )
  165 |         pedido = PedidoSangue.objects.get()
  166 | 
  167 |         validacao = aprovar_pedido(
  168 |             pedido=pedido,
  169 |             moderador=self.hemocentro,
  170 |             motivo="Dados conferidos pelo administrador.",
  171 |         )
  172 | 
  173 |         pedido.refresh_from_db()
  174 |         self.assertEqual(pedido.status, PedidoSangue.Status.PUBLICADA)
  175 |         self.assertEqual(
  176 |             validacao.status_validacao,
  177 |             ValidacaoPedido.StatusValidacao.APROVADO,
  178 |         )
  179 |         self.assertEqual(pedido.validacoes.count(), 1)
  180 | 
  181 |     def test_admin_moderar_pedido_nao_publica(self):
  182 |         pedido = criar_pedido_pendente(
  183 |             dados=self.dados_validos(),
  184 |             solicitante=self.receptor,
  185 |         )
  186 | 
  187 |         self.client.force_login(self.administrador)
  188 | 
  189 |         resposta = self.client.get(
  190 |             reverse("accounts:painel_validacao_pedidos")
  191 |         )
  192 | 
  193 |         self.assertEqual(resposta.status_code, 200)
  194 |         self.assertContains(resposta, str(pedido.pk))
  195 | 
  196 |         resposta = self.client.post(
  197 |             reverse(
  198 |                 "accounts:marcar_pedido_suspeito",
  199 |                 kwargs={"id_pedido": pedido.pk},
  200 |             ),
  201 |             {"motivo": "Há solicitação semelhante para o mesmo destino."},
  202 |         )
  203 | 
  204 |         self.assertRedirects(
  205 |             resposta,
  206 |             reverse("accounts:painel_validacao_pedidos"),
  207 |         )
  208 |         pedido.refresh_from_db()
  209 |         self.assertEqual(
  210 |             pedido.status,
  211 |             PedidoSangue.Status.EM_ANALISE,
  212 |         )
  213 |         self.assertFalse(pedido.publicado_por_id)
  214 |         self.assertEqual(
  215 |             pedido.validacoes.latest("data_validacao").status_validacao,
  216 |             ValidacaoPedido.StatusValidacao.SUSPEITO,
  217 |         )
  218 | 
  219 |     def test_hemocentro_nao_acessa_moderacao_administrativa(self):
  220 |         self.client.force_login(self.hemocentro)
  221 | 
  222 |         resposta = self.client.get(
  223 |             reverse("accounts:painel_validacao_pedidos")
  224 |         )
  225 | 
  226 |         self.assertEqual(resposta.status_code, 403)
  227 | 
  228 |     def test_publicacao_exclusiva_do_hemocentro_responsavel(self):
  229 |         from django.core.exceptions import PermissionDenied
  230 |         self.client.force_login(self.receptor)
  231 |         self.client.post(reverse('accounts:pedido_publicar'), self.dados_validos())
  232 |         pedido = PedidoSangue.objects.get()
  233 |         self.client.force_login(self.hemocentro_pendente)
  234 |         self.assertEqual(self.client.get(reverse('accounts:painel_pedidos_hemocentro')).status_code, 403)
  235 |         with self.assertRaises(PermissionDenied):
  236 |             aprovar_pedido(pedido=pedido, moderador=self.hemocentro_pendente)
  237 |         self.hemocentro_pendente.status_validacao = Usuario.StatusValidacaoHemocentro.APROVADO
  238 |         self.hemocentro_pendente.save()
  239 |         with self.assertRaises(PermissionDenied):
  240 |             aprovar_pedido(pedido=pedido, moderador=self.hemocentro_pendente)
  241 |         self.assertNotContains(self.client.get(reverse('accounts:painel_pedidos_hemocentro')), pedido.titulo)
  242 |         self.client.force_login(self.hemocentro)
  243 |         self.assertContains(self.client.get(reverse('accounts:painel_pedidos_hemocentro')), pedido.titulo)
  244 |         resposta = self.client.post(reverse('accounts:aprovar_pedido', kwargs={'id_pedido': pedido.pk}))
  245 |         self.assertEqual(resposta.status_code, 302)
  246 |         pedido.refresh_from_db()
  247 |         self.assertEqual(pedido.status, PedidoSangue.Status.PUBLICADA)
  248 | 
  249 |     def test_permissao_do_servico_de_publicacao(self):
  250 |         from .pedidos import pode_publicar_pedido
  251 |         for usuario in (self.receptor, self.doador, self.administrador, self.hemocentro_pendente):
  252 |             with self.subTest(perfil=usuario.perfil):
  253 |                 self.assertFalse(pode_publicar_pedido(usuario))
  254 |         self.assertTrue(pode_publicar_pedido(self.hemocentro))
  255 | 
  256 |     def test_auditoria_distingue_validacao_e_publicacao(self):
  257 |         from .models import AuditoriaAcaoCritica
  258 |         self.client.force_login(self.receptor)
  259 |         self.client.post(reverse('accounts:pedido_publicar'), self.dados_validos())
  260 |         pedido = PedidoSangue.objects.get()
  261 |         marcar_pedido_suspeito(pedido=pedido, moderador=self.administrador)
  262 |         registro = AuditoriaAcaoCritica.objects.filter(alvo_tipo='accounts.PedidoSangue').latest('id_auditoria')
  263 |         self.assertEqual(registro.metadados['evento'], 'VALIDACAO_PEDIDO')
  264 |         self.assertEqual(registro.metadados['status_anterior'], PedidoSangue.Status.ENVIADA)
  265 |         self.assertEqual(registro.metadados['status_pedido'], PedidoSangue.Status.EM_ANALISE)
  266 |         aprovar_pedido(pedido=pedido, moderador=self.hemocentro)
  267 |         registro = AuditoriaAcaoCritica.objects.filter(alvo_tipo='accounts.PedidoSangue').latest('id_auditoria')
  268 |         self.assertEqual(registro.usuario, self.hemocentro)
  269 |         self.assertEqual(registro.metadados['evento'], 'PUBLICACAO_PEDIDO')
  270 |         self.assertEqual(registro.metadados['status_pedido'], PedidoSangue.Status.PUBLICADA)
  271 |         self.assertNotIn('Paciente de exemplo', str(registro.metadados))
  272 | 
  273 |     def test_tentativa_de_publicacao_alheia_persiste_na_auditoria(self):
  274 |         from .models import AuditoriaAcaoCritica
  275 |         self.client.force_login(self.receptor)
  276 |         self.client.post(reverse('accounts:pedido_publicar'), self.dados_validos())
  277 |         pedido = PedidoSangue.objects.get()
  278 |         self.hemocentro_pendente.status_validacao = Usuario.StatusValidacaoHemocentro.APROVADO
  279 |         self.hemocentro_pendente.save()
  280 |         self.client.force_login(self.hemocentro_pendente)
  281 |         resposta = self.client.post(reverse('accounts:aprovar_pedido', kwargs={'id_pedido': pedido.pk}))
  282 |         self.assertEqual(resposta.status_code, 403)
  283 |         registro = AuditoriaAcaoCritica.objects.filter(usuario=self.hemocentro_pendente).latest('id_auditoria')
  284 |         self.assertEqual(registro.resultado, AuditoriaAcaoCritica.Resultado.BLOQUEADO)
  285 |         pedido.refresh_from_db()
  286 |         self.assertEqual(pedido.status, PedidoSangue.Status.ENVIADA)
``````

## accounts/test_perfis_teste.py

Original: [accounts/test_perfis_teste.py](<C:/Users/lb119/Elo/accounts/test_perfis_teste.py>).

``````text
    1 | from io import StringIO
    2 | 
    3 | from django.core.management import call_command
    4 | from django.core.management.base import CommandError
    5 | from django.test import TestCase, override_settings
    6 | 
    7 | from .compatibilidade import doadores_aptos_para_convocacao
    8 | from .models import ConsentimentoLGPD, Triagem, Usuario
    9 | 
   10 | 
   11 | @override_settings(DEBUG=True)
   12 | class PerfisTesteTests(TestCase):
   13 |     def test_cria_perfis_e_preserva_alteracoes_ao_repetir(self):
   14 |         call_command('criar_perfis_teste', stdout=StringIO())
   15 |         self.assertEqual(Usuario.objects.count(), 10)
   16 |         self.assertEqual(set(Usuario.objects.values_list('perfil', flat=True)), set(Usuario.Perfil.values))
   17 |         self.assertEqual(list(doadores_aptos_para_convocacao('O-').values_list('email', flat=True)),
   18 |                          ['doador@teste.elo.test'])
   19 |         usuario = Usuario.objects.get(email='receptor@teste.elo.test')
   20 |         self.assertTrue(usuario.check_password('EloTeste2026!'))
   21 |         usuario.nome = 'Nome alterado no teste'
   22 |         usuario.set_password('OutraSenha123!')
   23 |         usuario.save()
   24 |         contagens = (Triagem.objects.count(), ConsentimentoLGPD.objects.count())
   25 |         call_command('criar_perfis_teste', senha='NovaSenha123!', stdout=StringIO())
   26 |         usuario.refresh_from_db()
   27 |         self.assertEqual(usuario.nome, 'Nome alterado no teste')
   28 |         self.assertTrue(usuario.check_password('OutraSenha123!'))
   29 |         self.assertEqual(Usuario.objects.count(), 10)
   30 |         self.assertEqual(contagens, (Triagem.objects.count(), ConsentimentoLGPD.objects.count()))
   31 | 
   32 |     @override_settings(DEBUG=False)
   33 |     def test_nao_cria_contas_fora_do_ambiente_de_desenvolvimento(self):
   34 |         with self.assertRaises(CommandError):
   35 |             call_command('criar_perfis_teste', stdout=StringIO())
   36 |         self.assertFalse(Usuario.objects.exists())
``````

## accounts/test_triagem.py

Original: [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py>).

``````text
    1 | """
    2 | Testes automatizados da triagem extensa inicial.
    3 | 
    4 | Verificam o cálculo dos resultados para respostas básicas, a
    5 | classificação temporária para peso abaixo de 50 kg, o início da
    6 | triagem com registro do consentimento, o bloqueio de perfis não
    7 | autorizados (Observador e Receptor) e o acesso público à página
    8 | de apresentação da triagem.
    9 | """
   10 | 
   11 | from datetime import date
   12 | 
   13 | from django.test import TestCase
   14 | from django.urls import reverse
   15 | 
   16 | from .models import (
   17 |     ConsentimentoLGPD,
   18 |     RespostaTriagem,
   19 |     Triagem,
   20 |     Usuario,
   21 | )
   22 | from .triagem import calcular_resultado
   23 | 
   24 | 
   25 | class TriagemExtensaTests(TestCase):
   26 |     """
   27 |     Testa o cálculo e o salvamento da triagem inicial.
   28 |     """
   29 | 
   30 |     def criar_doador(self):
   31 |         """
   32 |         Cria um usuário Doador para os testes.
   33 |         """
   34 | 
   35 |         return Usuario.objects.create_user(
   36 |             email="doador@teste.com",
   37 |             password="SenhaForte123!",
   38 |             nome="Doador Teste",
   39 |             perfil=Usuario.Perfil.DOADOR,
   40 |         )
   41 | 
   42 |     def dados_sem_impedimento(self):
   43 |         """
   44 |         Retorna respostas básicas sem impedimento inicial.
   45 |         """
   46 | 
   47 |         return {
   48 |             "entende_orientacao": "SIM",
   49 |             "idade": "18_60",
   50 |             "peso": "56_129_9",
   51 |             "sexo_biologico": "MASCULINO",
   52 |             "ja_doou": "NAO",
   53 |         }
   54 | 
   55 |     def test_peso_abaixo_de_50_gera_inaptidao_temporaria(self):
   56 |         """
   57 |         Peso abaixo de 50 kg deve gerar resultado temporário.
   58 |         """
   59 | 
   60 |         respostas = self.dados_sem_impedimento()
   61 |         respostas["peso"] = "MENOS_50"
   62 | 
   63 |         resultado = calcular_resultado(
   64 |             respostas,
   65 |             hoje=date(2026, 8, 28),
   66 |         )
   67 | 
   68 |         self.assertEqual(
   69 |             resultado["resultado"],
   70 |             Triagem.Resultado.TEMPORARIA,
   71 |         )
   72 | 
   73 |     def test_respostas_basicas_sem_impedimento(self):
   74 |         """
   75 |         Respostas básicas devem gerar orientação sem impedimento identificado.
   76 |         """
   77 | 
   78 |         resultado = calcular_resultado(
   79 |             self.dados_sem_impedimento(),
   80 |             hoje=date(2026, 8, 28),
   81 |         )
   82 | 
   83 |         self.assertEqual(
   84 |             resultado["resultado"],
   85 |             Triagem.Resultado.SEM_IMPEDIMENTO,
   86 |         )
   87 | 
   88 |     def test_post_inicia_triagem_e_consentimento(self):
   89 |         """
   90 |         O clique inicial cria a triagem e o consentimento versionado.
   91 |         """
   92 | 
   93 |         usuario = self.criar_doador()
   94 |         self.client.force_login(usuario)
   95 | 
   96 |         resposta = self.client.post(
   97 |             reverse(
   98 |                 "accounts:triagem_iniciar",
   99 |                 kwargs={"modalidade": "extensa"},
  100 |             ),
  101 |             {"aceite_termo": "on"},
  102 |         )
  103 | 
  104 |         self.assertEqual(
  105 |             resposta.status_code,
  106 |             302,
  107 |         )
  108 | 
  109 |         triagem = Triagem.objects.get(
  110 |             usuario=usuario,
  111 |         )
  112 | 
  113 |         self.assertRedirects(
  114 |             resposta,
  115 |             reverse(
  116 |                 "accounts:triagem_pergunta",
  117 |                 kwargs={"id_triagem": triagem.pk},
  118 |             ),
  119 |         )
  120 | 
  121 |         self.assertEqual(
  122 |             RespostaTriagem.objects.filter(
  123 |                 triagem=triagem,
  124 |             ).count(),
  125 |             0,
  126 |         )
  127 | 
  128 |         self.assertTrue(
  129 |             ConsentimentoLGPD.objects.filter(
  130 |                 usuario=usuario,
  131 |                 tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM,
  132 |             ).exists()
  133 |         )
  134 | 
  135 |     def test_usuario_nao_doador_nao_acessa_triagem(self):
  136 |         """
  137 |         A primeira versão da triagem só aceita usuários Doador.
  138 |         """
  139 | 
  140 |         usuario = Usuario.objects.create_user(
  141 |             email="observador@teste.com",
  142 |             password="SenhaForte123!",
  143 |             nome="Observador Teste",
  144 |             perfil=Usuario.Perfil.OBSERVADOR,
  145 |         )
  146 | 
  147 |         self.client.force_login(usuario)
  148 | 
  149 |         resposta = self.client.post(
  150 |             reverse(
  151 |                 "accounts:triagem_iniciar",
  152 |                 kwargs={"modalidade": "extensa"},
  153 |             ),
  154 |             {"aceite_termo": "on"},
  155 |         )
  156 | 
  157 |         self.assertEqual(resposta.status_code, 403)
  158 | 
  159 |     def test_receptor_nao_pode_acessar_a_triagem(self):
  160 |         """
  161 |         Receptor nao pode responder a triagem para doacao.
  162 |         """
  163 | 
  164 |         usuario = Usuario.objects.create_user(
  165 |             email="receptor@teste.com",
  166 |             password="SenhaForte123!",
  167 |             nome="Receptor Teste",
  168 |             perfil=Usuario.Perfil.RECEPTOR,
  169 |         )
  170 | 
  171 |         self.client.force_login(usuario)
  172 | 
  173 |         resposta = self.client.post(
  174 |             reverse(
  175 |                 "accounts:triagem_iniciar",
  176 |                 kwargs={"modalidade": "extensa"},
  177 |             ),
  178 |             {"aceite_termo": "on"},
  179 |         )
  180 | 
  181 |         self.assertEqual(
  182 |             resposta.status_code,
  183 |             403,
  184 |         )
  185 | 
  186 |     def test_visitante_pode_ver_apresentacao_da_triagem(self):
  187 |         """
  188 |         Visitante pode conhecer a triagem sem estar autenticado.
  189 |         """
  190 | 
  191 |         resposta = self.client.get(
  192 |             reverse("accounts:triagem_apresentacao"),
  193 |         )
  194 | 
  195 |         self.assertEqual(
  196 |             resposta.status_code,
  197 |             200,
  198 |         )
  199 | 
  200 |         self.assertContains(
  201 |             resposta,
  202 |             "Seu gesto de cuidado começa aqui.",
  203 |         )
  204 | 
  205 |         self.assertContains(
  206 |             resposta,
  207 |             "Criar conta",
  208 |         )
``````

## accounts/test_triagem_catalogos.py

Original: [accounts/test_triagem_catalogos.py](<C:/Users/lb119/Elo/accounts/test_triagem_catalogos.py>).

``````text
    1 | """Testes que impedem perguntas ou alternativas de desaparecerem do catálogo."""
    2 | 
    3 | from django.test import SimpleTestCase
    4 | 
    5 | from .triagem_catalogo import (
    6 |     PERGUNTAS_EXTENSAS,
    7 |     PERGUNTAS_SIMPLIFICADAS,
    8 |     todas_as_perguntas,
    9 |     validar_catalogos,
   10 | )
   11 | 
   12 | 
   13 | IDS_EXTENSOS = {
   14 |     "EXT-01", "EXT-01A", "EXT-02", "EXT-03", "EXT-04", "EXT-05", "EXT-05A",
   15 |     "EXT-05B", "EXT-06", "EXT-07", "EXT-07A", "EXT-08", "EXT-09",
   16 |     "EXT-10", "EXT-11", "EXT-11A", "EXT-12", "EXT-13", "EXT-14",
   17 |     "EXT-15", "EXT-16", "EXT-17", "EXT-18", "EXT-19", "EXT-20",
   18 |     "EXT-21", "EXT-22", "EXT-23", "EXT-24", "EXT-25", "EXT-26",
   19 |     "EXT-27", "EXT-28", "EXT-29", "EXT-30", "EXT-31", "EXT-32",
   20 |     "EXT-33", "EXT-34", "EXT-35", "EXT-36", "EXT-37", "EXT-38",
   21 |     "EXT-39", "EXT-40", "EXT-41", "EXT-42", "EXT-43", "EXT-44",
   22 |     "EXT-45", "EXT-46", "EXT-47", "EXT-48", "EXT-49", "EXT-50",
   23 |     "EXT-51",
   24 | }
   25 | 
   26 | IDS_SIMPLIFICADOS = {
   27 |     f"SIM-{numero:02d}"
   28 |     for numero in range(1, 19)
   29 | }
   30 | 
   31 | 
   32 | class CatalogosTriagemTests(SimpleTestCase):
   33 |     """Valida a estrutura consumida pelo formulário, serviço e motor."""
   34 | 
   35 |     def test_catalogo_extenso_possui_todas_as_56_entradas(self):
   36 |         """Falha se qualquer pergunta extensa da especificação for omitida."""
   37 | 
   38 |         self.assertEqual(set(PERGUNTAS_EXTENSAS), IDS_EXTENSOS)
   39 | 
   40 |     def test_catalogo_simplificado_possui_todas_as_18_entradas(self):
   41 |         """Falha se a versão rápida ficar incompleta."""
   42 | 
   43 |         self.assertEqual(set(PERGUNTAS_SIMPLIFICADAS), IDS_SIMPLIFICADOS)
   44 | 
   45 |     def test_perguntas_possuem_conteudo_e_rastreabilidade(self):
   46 |         """Falha se uma pergunta não puder ser exibida ou auditada."""
   47 | 
   48 |         for pergunta in todas_as_perguntas():
   49 |             self.assertTrue(pergunta["titulo"], pergunta["id"])
   50 |             self.assertTrue(pergunta["texto"], pergunta["id"])
   51 |             self.assertTrue(pergunta["explicacao"], pergunta["id"])
   52 |             self.assertTrue(pergunta["fonte"], pergunta["id"])
   53 |             self.assertEqual(
   54 |                 pergunta["regra_version"],
   55 |                 "HEMOMINAS_2026_08",
   56 |                 pergunta["id"],
   57 |             )
   58 | 
   59 |             if pergunta["tipo"] not in {"data", "numero", "texto"}:
   60 |                 self.assertTrue(pergunta["opcoes"], pergunta["id"])
   61 | 
   62 |     def test_codigos_de_opcao_nao_se_repetem_na_mesma_pergunta(self):
   63 |         """Falha se dois rótulos diferentes forem salvos com o mesmo código."""
   64 | 
   65 |         for pergunta in todas_as_perguntas():
   66 |             codigos = [opcao["codigo"] for opcao in pergunta["opcoes"]]
   67 |             self.assertEqual(len(codigos), len(set(codigos)), pergunta["id"])
   68 | 
   69 |     def test_destinos_da_simplificada_existem_no_catalogo_extenso(self):
   70 |         """Falha se a versão rápida tentar abrir uma pergunta inexistente."""
   71 | 
   72 |         for pergunta in PERGUNTAS_SIMPLIFICADAS.values():
   73 |             for destinos in pergunta["abrir_extensa"].values():
   74 |                 for destino in destinos:
   75 |                     self.assertIn(destino, PERGUNTAS_EXTENSAS)
   76 | 
   77 |     def test_funcao_de_validacao_aceita_os_catalogos_oficiais(self):
   78 |         """Falha se o catálogo publicado violar seu próprio contrato."""
   79 | 
   80 |         self.assertIsNone(validar_catalogos())
``````

## accounts/test_triagem_forms.py

Original: [accounts/test_triagem_forms.py](<C:/Users/lb119/Elo/accounts/test_triagem_forms.py>).

``````text
    1 | """Testes do formulário construído a partir do catálogo."""
    2 | 
    3 | from django.test import SimpleTestCase
    4 | 
    5 | from .triagem_catalogo import obter_pergunta
    6 | from .triagem_forms import FormularioPergunta
    7 | 
    8 | 
    9 | class FormularioPerguntaTests(SimpleTestCase):
   10 |     """Protege a normalização usada para salvar respostas estruturadas."""
   11 | 
   12 |     def test_escolha_com_data_e_normalizada(self):
   13 |         """Falha se a data da alternativa não chegar ao motor com seu código."""
   14 | 
   15 |         form = FormularioPergunta(
   16 |             obter_pergunta("EXT-05A"),
   17 |             data={
   18 |                 "resposta": "DATA",
   19 |                 "data_DATA": "2026-08-01",
   20 |             },
   21 |         )
   22 | 
   23 |         self.assertTrue(form.is_valid(), form.errors)
   24 |         self.assertEqual(
   25 |             form.cleaned_data["valor"],
   26 |             {
   27 |                 "codigos": ["DATA"],
   28 |                 "datas": {"DATA": "2026-08-01"},
   29 |                 "detalhes": "",
   30 |             },
   31 |         )
   32 | 
   33 |     def test_selecao_multipla_preserva_uma_data_por_item(self):
   34 |         """Falha se duas vacinas diferentes compartilharem uma única data."""
   35 | 
   36 |         form = FormularioPergunta(
   37 |             obter_pergunta("EXT-48"),
   38 |             data={
   39 |                 "resposta": ["DENGUE", "FEBRE_AMARELA"],
   40 |                 "data_DENGUE": "2026-08-01",
   41 |                 "data_FEBRE_AMARELA": "2026-08-10",
   42 |             },
   43 |         )
   44 | 
   45 |         self.assertTrue(form.is_valid(), form.errors)
   46 |         self.assertEqual(
   47 |             form.cleaned_data["valor"]["datas"],
   48 |             {
   49 |                 "DENGUE": "2026-08-01",
   50 |                 "FEBRE_AMARELA": "2026-08-10",
   51 |             },
   52 |         )
   53 | 
   54 |     def test_data_futura_e_rejeitada(self):
   55 |         """Falha se uma data impossível produzir prazo de liberação."""
   56 | 
   57 |         form = FormularioPergunta(
   58 |             obter_pergunta("EXT-05A"),
   59 |             data={
   60 |                 "resposta": "DATA",
   61 |                 "data_DATA": "2999-01-01",
   62 |             },
   63 |         )
   64 | 
   65 |         self.assertFalse(form.is_valid())
   66 |         self.assertIn("data_DATA", form.errors)
   67 | 
   68 |     def test_alternativa_com_prazo_exige_sua_data(self):
   69 |         """Falha se uma vacina sem data for aceita pelo formulário."""
   70 | 
   71 |         form = FormularioPergunta(
   72 |             obter_pergunta("EXT-48"),
   73 |             data={"resposta": ["DENGUE"]},
   74 |         )
   75 | 
   76 |         self.assertFalse(form.is_valid())
   77 |         self.assertIn("data_DENGUE", form.errors)
   78 | 
   79 |     def test_nenhuma_nao_pode_ser_marcada_com_uma_condicao(self):
   80 |         """Falha se uma resposta contraditória for persistida."""
   81 | 
   82 |         form = FormularioPergunta(
   83 |             obter_pergunta("EXT-20"),
   84 |             data={
   85 |                 "resposta": ["NENHUMA", "ANEMIA_HEREDITARIA"],
   86 |             },
   87 |         )
   88 | 
   89 |         self.assertFalse(form.is_valid())
   90 |         self.assertIn("resposta", form.errors)
   91 | 
   92 |     def test_descricao_e_obrigatoria_quando_usuario_informa_outra_condicao(self):
   93 |         """Falha se EXT-50 aceitar uma condição sem qualquer descrição."""
   94 | 
   95 |         form = FormularioPergunta(
   96 |             obter_pergunta("EXT-50"),
   97 |             data={"resposta": "SIM", "detalhes": ""},
   98 |         )
   99 | 
  100 |         self.assertFalse(form.is_valid())
  101 |         self.assertIn("detalhes", form.errors)
  102 | 
  103 |     def test_procedimento_estetico_registra_seguranca_e_inflamacao(self):
  104 |         """Falha se os fatores que alteram o prazo estético forem perdidos."""
  105 | 
  106 |         form = FormularioPergunta(
  107 |             obter_pergunta("EXT-24"),
  108 |             data={
  109 |                 "resposta": ["BOTOX"],
  110 |                 "data_BOTOX": "2026-08-01",
  111 |                 "seguranca": "SIM",
  112 |                 "inflamacao": "NAO",
  113 |             },
  114 |         )
  115 | 
  116 |         self.assertTrue(form.is_valid(), form.errors)
  117 |         self.assertEqual(form.cleaned_data["valor"]["seguranca"], "SIM")
  118 |         self.assertEqual(form.cleaned_data["valor"]["inflamacao"], "NAO")
``````

## accounts/test_triagem_models.py

Original: [accounts/test_triagem_models.py](<C:/Users/lb119/Elo/accounts/test_triagem_models.py>).

``````text
    1 | """Testes da persistência das triagens e de suas respostas."""
    2 | 
    3 | from django.db import IntegrityError, transaction
    4 | from django.test import TestCase
    5 | 
    6 | from .models import RespostaTriagem, Triagem, Usuario
    7 | 
    8 | 
    9 | class TriagemModelTests(TestCase):
   10 |     """Garante que andamento e correções sejam persistidos sem duplicação."""
   11 | 
   12 |     def setUp(self):
   13 |         # Cada teste usa uma conta real do model personalizado do projeto.
   14 |         self.usuario = Usuario.objects.create_user(
   15 |             email="model-triagem@teste.com",
   16 |             password="SenhaForte123!",
   17 |             nome="Pessoa em Triagem",
   18 |             perfil=Usuario.Perfil.DOADOR,
   19 |         )
   20 | 
   21 |     def test_nova_triagem_comeca_em_andamento(self):
   22 |         """Falha se uma triagem nova nascer como concluída ou sem fluxo vazio."""
   23 | 
   24 |         triagem = Triagem.objects.create(
   25 |             usuario=self.usuario,
   26 |             modalidade=Triagem.Modalidade.EXTENSA,
   27 |         )
   28 | 
   29 |         self.assertEqual(
   30 |             triagem.status,
   31 |             Triagem.Status.EM_ANDAMENTO,
   32 |         )
   33 |         self.assertEqual(triagem.pergunta_atual, 0)
   34 |         self.assertEqual(triagem.fluxo_perguntas, [])
   35 |         self.assertEqual(triagem.resultado, "")
   36 | 
   37 |     def test_uma_pergunta_tem_uma_unica_resposta_por_triagem(self):
   38 |         """Falha se a mesma pergunta puder gerar respostas concorrentes."""
   39 | 
   40 |         triagem = Triagem.objects.create(
   41 |             usuario=self.usuario,
   42 |             modalidade=Triagem.Modalidade.EXTENSA,
   43 |         )
   44 |         RespostaTriagem.objects.create(
   45 |             triagem=triagem,
   46 |             id_pergunta="EXT-01",
   47 |             codigo_resposta="SIM",
   48 |             resposta_label="Sim",
   49 |             valor={"codigos": ["SIM"]},
   50 |         )
   51 | 
   52 |         # O bloco atomic mantém o TestCase utilizável após o IntegrityError.
   53 |         with self.assertRaises(IntegrityError), transaction.atomic():
   54 |             RespostaTriagem.objects.create(
   55 |                 triagem=triagem,
   56 |                 id_pergunta="EXT-01",
   57 |                 codigo_resposta="NAO",
   58 |                 resposta_label="Não",
   59 |                 valor={"codigos": ["NAO"]},
   60 |             )
   61 | 
   62 |     def test_triagem_simplificada_pode_apontar_para_extensa_base(self):
   63 |         """Falha se a checagem rápida perder a extensa usada como referência."""
   64 | 
   65 |         extensa = Triagem.objects.create(
   66 |             usuario=self.usuario,
   67 |             modalidade=Triagem.Modalidade.EXTENSA,
   68 |         )
   69 |         simplificada = Triagem.objects.create(
   70 |             usuario=self.usuario,
   71 |             modalidade=Triagem.Modalidade.SIMPLIFICADA,
   72 |             triagem_base=extensa,
   73 |         )
   74 | 
   75 |         self.assertEqual(simplificada.triagem_base, extensa)
   76 |         self.assertIn(simplificada, extensa.verificacoes_simplificadas.all())
``````

## accounts/test_triagem_motor.py

Original: [accounts/test_triagem_motor.py](<C:/Users/lb119/Elo/accounts/test_triagem_motor.py>).

``````text
    1 | """
    2 | Testes automatizados do motor de triagem orientativa.
    3 | 
    4 | Verificam a prioridade dos resultados, a preservação dos achados,
    5 | o cálculo de prazos e datas de liberação, a exigência de avaliação
    6 | quando faltam informações, as regras para procedimentos estéticos e
    7 | intervalos entre doações, os limites anuais de doação, a reutilização
    8 | segura de respostas na triagem simplificada e a apresentação de
    9 | mensagens que reforçam a necessidade de avaliação final pelo hemocentro.
   10 | """
   11 | 
   12 | from datetime import date
   13 | 
   14 | from django.test import SimpleTestCase
   15 | 
   16 | from .models import Triagem
   17 | from .triagem_motor import avaliar_triagem
   18 | 
   19 | 
   20 | class MotorTriagemTests(SimpleTestCase):
   21 |     """Exercita regras reais sem depender de banco, view ou formulário."""
   22 | 
   23 |     def test_resultado_prioriza_definitiva_e_preserva_todos_os_achados(self):
   24 |         """Falha se o motor parar no primeiro impedimento ou usar prioridade errada."""
   25 | 
   26 |         calculo = avaliar_triagem(
   27 |             Triagem.Modalidade.EXTENSA,
   28 |             {
   29 |                 "EXT-03": {"codigos": ["MENOS_50"]},
   30 |                 "EXT-20": {"codigos": ["ANEMIA_HEREDITARIA"]},
   31 |                 "EXT-46": {"codigos": ["OUTRO"]},
   32 |             },
   33 |             hoje=date(2026, 8, 28),
   34 |         )
   35 | 
   36 |         self.assertEqual(
   37 |             calculo["resultado"],
   38 |             Triagem.Resultado.DEFINITIVA,
   39 |         )
   40 |         self.assertEqual(len(calculo["achados"]), 3)
   41 | 
   42 |     def test_resultado_usa_a_maior_data_temporaria(self):
   43 |         """Falha se um prazo curto esconder uma espera mais longa."""
   44 | 
   45 |         calculo = avaliar_triagem(
   46 |             Triagem.Modalidade.EXTENSA,
   47 |             {
   48 |                 "EXT-13": {
   49 |                     "codigos": ["COVID_SINTOMATICO"],
   50 |                     "datas": {"COVID_SINTOMATICO": "2026-08-25"},
   51 |                 },
   52 |                 "EXT-48": {
   53 |                     "codigos": ["DENGUE"],
   54 |                     "datas": {"DENGUE": "2026-08-20"},
   55 |                 },
   56 |             },
   57 |             hoje=date(2026, 8, 28),
   58 |         )
   59 | 
   60 |         self.assertEqual(
   61 |             calculo["data_liberacao"],
   62 |             date(2026, 9, 19),
   63 |         )
   64 | 
   65 |     def test_prazo_em_meses_respeita_o_calendario(self):
   66 |         """Falha se um mês for tratado sempre como trinta dias."""
   67 | 
   68 |         calculo = avaliar_triagem(
   69 |             Triagem.Modalidade.EXTENSA,
   70 |             {
   71 |                 "EXT-47": {
   72 |                     "codigos": ["FINASTERIDA"],
   73 |                     "datas": {"FINASTERIDA": "2026-01-31"},
   74 |                 },
   75 |             },
   76 |             hoje=date(2026, 2, 1),
   77 |         )
   78 | 
   79 |         self.assertEqual(
   80 |             calculo["data_liberacao"],
   81 |             date(2026, 2, 28),
   82 |         )
   83 | 
   84 |     def test_regra_com_prazo_sem_data_exige_avaliacao(self):
   85 |         """Falha se o motor inventar a data de uma vacina não datada."""
   86 | 
   87 |         calculo = avaliar_triagem(
   88 |             Triagem.Modalidade.EXTENSA,
   89 |             {"EXT-48": {"codigos": ["DENGUE"]}},
   90 |             hoje=date(2026, 8, 28),
   91 |         )
   92 | 
   93 |         self.assertEqual(
   94 |             calculo["resultado"],
   95 |             Triagem.Resultado.AVALIACAO,
   96 |         )
   97 |         self.assertIsNone(calculo["data_liberacao"])
   98 | 
   99 |     def test_estetica_sem_seguranca_usa_doze_meses(self):
  100 |         """Falha se um procedimento inseguro receber apenas o prazo de três dias."""
  101 | 
  102 |         calculo = avaliar_triagem(
  103 |             Triagem.Modalidade.EXTENSA,
  104 |             {
  105 |                 "EXT-24": {
  106 |                     "codigos": ["BOTOX"],
  107 |                     "datas": {"BOTOX": "2026-08-01"},
  108 |                     "seguranca": "NAO_SEI",
  109 |                     "inflamacao": "NAO",
  110 |                 },
  111 |             },
  112 |             hoje=date(2026, 8, 28),
  113 |         )
  114 | 
  115 |         self.assertEqual(
  116 |             calculo["data_liberacao"],
  117 |             date(2027, 8, 1),
  118 |         )
  119 | 
  120 |     def test_estetica_com_inflamacao_exige_avaliacao(self):
  121 |         """Falha se uma complicação estética for tratada como recuperação simples."""
  122 | 
  123 |         calculo = avaliar_triagem(
  124 |             Triagem.Modalidade.EXTENSA,
  125 |             {
  126 |                 "EXT-24": {
  127 |                     "codigos": ["BOTOX"],
  128 |                     "datas": {"BOTOX": "2026-08-01"},
  129 |                     "seguranca": "SIM",
  130 |                     "inflamacao": "SIM",
  131 |                 },
  132 |             },
  133 |             hoje=date(2026, 8, 28),
  134 |         )
  135 | 
  136 |         self.assertEqual(
  137 |             calculo["resultado"],
  138 |             Triagem.Resultado.AVALIACAO,
  139 |         )
  140 | 
  141 |     def test_ultima_doacao_calcula_intervalo_feminino(self):
  142 |         """Falha se o intervalo feminino não usar noventa dias."""
  143 | 
  144 |         calculo = avaliar_triagem(
  145 |             Triagem.Modalidade.EXTENSA,
  146 |             {
  147 |                 "EXT-02": {"codigos": ["18_60"]},
  148 |                 "EXT-04": {"codigos": ["FEMININO"]},
  149 |                 "EXT-05A": {
  150 |                     "codigos": ["DATA"],
  151 |                     "datas": {"DATA": "2026-08-01"},
  152 |                 },
  153 |             },
  154 |             hoje=date(2026, 8, 28),
  155 |         )
  156 | 
  157 |         self.assertEqual(
  158 |             calculo["data_liberacao"],
  159 |             date(2026, 10, 30),
  160 |         )
  161 | 
  162 |     def test_ultima_doacao_acima_de_60_usa_seis_meses(self):
  163 |         """Falha se a regra especial de 61 a 69 anos for ignorada."""
  164 | 
  165 |         calculo = avaliar_triagem(
  166 |             Triagem.Modalidade.EXTENSA,
  167 |             {
  168 |                 "EXT-02": {"codigos": ["61_69"]},
  169 |                 "EXT-04": {"codigos": ["MASCULINO"]},
  170 |                 "EXT-05A": {
  171 |                     "codigos": ["DATA"],
  172 |                     "datas": {"DATA": "2026-08-01"},
  173 |                 },
  174 |             },
  175 |             hoje=date(2026, 8, 28),
  176 |         )
  177 | 
  178 |         self.assertEqual(
  179 |             calculo["data_liberacao"],
  180 |             date(2027, 2, 1),
  181 |         )
  182 | 
  183 |     def test_limite_anual_sem_datas_nao_inventa_liberacao(self):
  184 |         """Falha se somente a contagem gerar uma data fictícia."""
  185 | 
  186 |         calculo = avaliar_triagem(
  187 |             Triagem.Modalidade.EXTENSA,
  188 |             {
  189 |                 "EXT-04": {"codigos": ["FEMININO"]},
  190 |                 "EXT-05B": {"codigos": ["3"]},
  191 |             },
  192 |             hoje=date(2026, 8, 28),
  193 |         )
  194 | 
  195 |         self.assertEqual(
  196 |             calculo["resultado"],
  197 |             Triagem.Resultado.AVALIACAO,
  198 |         )
  199 |         self.assertIsNone(calculo["data_liberacao"])
  200 | 
  201 |     def test_simplificada_reutiliza_doenca_estavel_da_extensa(self):
  202 |         """Falha se uma condição permanente salva for esquecida na versão rápida."""
  203 | 
  204 |         calculo = avaliar_triagem(
  205 |             Triagem.Modalidade.SIMPLIFICADA,
  206 |             {"SIM-18": {"codigos": ["ENTENDO"]}},
  207 |             respostas_base={
  208 |                 "EXT-20": {"codigos": ["ANEMIA_HEREDITARIA"]},
  209 |             },
  210 |             hoje=date(2026, 8, 28),
  211 |         )
  212 | 
  213 |         self.assertEqual(
  214 |             calculo["resultado"],
  215 |             Triagem.Resultado.DEFINITIVA,
  216 |         )
  217 | 
  218 |     def test_simplificada_nao_reutiliza_estado_de_saude_antigo(self):
  219 |         """Falha se uma febre antiga for tratada como estado atual sem nova resposta."""
  220 | 
  221 |         calculo = avaliar_triagem(
  222 |             Triagem.Modalidade.SIMPLIFICADA,
  223 |             {"SIM-18": {"codigos": ["ENTENDO"]}},
  224 |             respostas_base={
  225 |                 "EXT-12": {"codigos": ["PERSISTENTE"]},
  226 |             },
  227 |             hoje=date(2026, 8, 28),
  228 |         )
  229 | 
  230 |         self.assertEqual(
  231 |             calculo["resultado"],
  232 |             Triagem.Resultado.SEM_IMPEDIMENTO,
  233 |         )
  234 | 
  235 |     def test_resultado_sem_achados_mantem_aviso_presencial(self):
  236 |         """Falha se a mensagem declarar que a pessoa está apta."""
  237 | 
  238 |         calculo = avaliar_triagem(
  239 |             Triagem.Modalidade.EXTENSA,
  240 |             {"EXT-51": {"codigos": ["CONFIRMAR"]}},
  241 |             hoje=date(2026, 8, 28),
  242 |         )
  243 | 
  244 |         self.assertEqual(
  245 |             calculo["resultado"],
  246 |             Triagem.Resultado.SEM_IMPEDIMENTO,
  247 |         )
  248 |         self.assertIn("decisão final", calculo["mensagem"])
  249 |         self.assertNotIn("apto", calculo["mensagem"].lower())
``````

## accounts/test_triagem_servico.py

Original: [accounts/test_triagem_servico.py](<C:/Users/lb119/Elo/accounts/test_triagem_servico.py>).

``````text
    1 | """
    2 | Testes automatizados do serviço de triagem.
    3 | 
    4 | Verificam o início e a retomada de triagens, o registro do consentimento,
    5 | a reutilização de respostas anteriores, as permissões de acesso, o fluxo
    6 | condicional das perguntas, o salvamento e a correção de respostas, a
    7 | remoção de respostas inválidas, o encaminhamento da triagem simplificada
    8 | para a extensa e a conclusão do processo, garantindo a integridade do
    9 | histórico e o bloqueio de alterações após a finalização.
   10 | """
   11 | 
   12 | from django.core.exceptions import PermissionDenied
   13 | from django.test import TestCase
   14 | 
   15 | from .models import ConsentimentoLGPD, RespostaTriagem, Triagem, Usuario
   16 | from .triagem_catalogo import obter_pergunta
   17 | from .triagem_servico import (
   18 |     TriagemConcluida,
   19 |     TriagemExtensaNecessaria,
   20 |     TriagemSimplificadaIndisponivel,
   21 |     concluir_triagem,
   22 |     iniciar_triagem,
   23 |     obter_pergunta_atual,
   24 |     salvar_resposta,
   25 |     voltar_pergunta,
   26 | )
   27 | 
   28 | 
   29 | class TriagemServicoTests(TestCase):
   30 |     """Protege transições de estado e vínculos entre as duas modalidades."""
   31 | 
   32 |     def setUp(self):
   33 |         self.usuario = Usuario.objects.create_user(
   34 |             email="servico@teste.com",
   35 |             password="SenhaForte123!",
   36 |             nome="Pessoa Serviço",
   37 |             perfil=Usuario.Perfil.DOADOR,
   38 |         )
   39 | 
   40 |     def test_inicio_extenso_cria_fluxo_e_consentimento(self):
   41 |         """Falha se uma triagem começar sem pergunta ou sem aceite versionado."""
   42 | 
   43 |         triagem = iniciar_triagem(
   44 |             self.usuario,
   45 |             Triagem.Modalidade.EXTENSA,
   46 |             ip="127.0.0.1",
   47 |         )
   48 | 
   49 |         self.assertEqual(triagem.fluxo_perguntas[0], "EXT-01")
   50 |         self.assertEqual(triagem.fluxo_perguntas[-1], "EXT-51")
   51 |         self.assertEqual(
   52 |             triagem.status,
   53 |             Triagem.Status.EM_ANDAMENTO,
   54 |         )
   55 |         self.assertTrue(
   56 |             ConsentimentoLGPD.objects.filter(
   57 |                 usuario=self.usuario,
   58 |                 tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM,
   59 |                 versao_termo="HEMOMINAS_2026_08",
   60 |                 aceito=True,
   61 |             ).exists()
   62 |         )
   63 | 
   64 |     def test_inicio_reutiliza_triagem_em_andamento(self):
   65 |         """Falha se cada clique em iniciar criar um histórico vazio duplicado."""
   66 | 
   67 |         primeira = iniciar_triagem(
   68 |             self.usuario,
   69 |             Triagem.Modalidade.EXTENSA,
   70 |             ip=None,
   71 |         )
   72 |         segunda = iniciar_triagem(
   73 |             self.usuario,
   74 |             Triagem.Modalidade.EXTENSA,
   75 |             ip=None,
   76 |         )
   77 | 
   78 |         self.assertEqual(primeira.pk, segunda.pk)
   79 |         self.assertEqual(self.usuario.triagens.count(), 1)
   80 | 
   81 |     def test_nova_extensa_pode_reutilizar_respostas_concluidas(self):
   82 |         """Copia respostas sem alterar a triagem concluída original."""
   83 | 
   84 |         origem = Triagem.objects.create(
   85 |             usuario=self.usuario,
   86 |             modalidade=Triagem.Modalidade.EXTENSA,
   87 |             status=Triagem.Status.CONCLUIDA,
   88 |             resultado=Triagem.Resultado.SEM_IMPEDIMENTO,
   89 |         )
   90 |         pergunta = obter_pergunta("EXT-01")
   91 |         RespostaTriagem.objects.create(
   92 |             triagem=origem,
   93 |             id_pergunta="EXT-01",
   94 |             codigo_resposta="SIM",
   95 |             resposta_label="Sim, entendo e quero continuar.",
   96 |             valor={"codigos": ["SIM"], "datas": {}, "detalhes": ""},
   97 |             rule_version=pergunta["regra_version"],
   98 |             source_ref=pergunta["fonte"],
   99 |         )
  100 | 
  101 |         nova = iniciar_triagem(
  102 |             self.usuario,
  103 |             Triagem.Modalidade.EXTENSA,
  104 |             ip=None,
  105 |             reutilizar_respostas=True,
  106 |         )
  107 | 
  108 |         self.assertNotEqual(nova.pk, origem.pk)
  109 |         self.assertEqual(
  110 |             nova.respostas.get(id_pergunta="EXT-01").codigo_resposta,
  111 |             "SIM",
  112 |         )
  113 |         self.assertEqual(origem.respostas.count(), 1)
  114 |         self.assertEqual(nova.pergunta_atual, 0)
  115 | 
  116 |     def test_simplificada_exige_extensa_concluida_do_mesmo_usuario(self):
  117 |         """Falha se a versão rápida puder ser usada sem histórico completo."""
  118 | 
  119 |         with self.assertRaises(TriagemSimplificadaIndisponivel):
  120 |             iniciar_triagem(
  121 |                 self.usuario,
  122 |                 Triagem.Modalidade.SIMPLIFICADA,
  123 |                 ip=None,
  124 |             )
  125 | 
  126 |     def test_simplificada_registra_a_extensa_base(self):
  127 |         """Falha se o resultado rápido perder a origem das respostas reutilizadas."""
  128 | 
  129 |         extensa = Triagem.objects.create(
  130 |             usuario=self.usuario,
  131 |             modalidade=Triagem.Modalidade.EXTENSA,
  132 |             status=Triagem.Status.CONCLUIDA,
  133 |             resultado=Triagem.Resultado.SEM_IMPEDIMENTO,
  134 |         )
  135 | 
  136 |         simplificada = iniciar_triagem(
  137 |             self.usuario,
  138 |             Triagem.Modalidade.SIMPLIFICADA,
  139 |             ip=None,
  140 |         )
  141 | 
  142 |         self.assertEqual(simplificada.triagem_base, extensa)
  143 |         self.assertEqual(simplificada.fluxo_perguntas[0], "SIM-01")
  144 | 
  145 |     def test_observador_nao_pode_iniciar_questionario(self):
  146 |         """Falha se um perfil fora de Doador responder à triagem."""
  147 | 
  148 |         observador = Usuario.objects.create_user(
  149 |             email="observador-servico@teste.com",
  150 |             password="SenhaForte123!",
  151 |             nome="Observador",
  152 |             perfil=Usuario.Perfil.OBSERVADOR,
  153 |         )
  154 | 
  155 |         with self.assertRaises(PermissionDenied):
  156 |             iniciar_triagem(
  157 |                 observador,
  158 |                 Triagem.Modalidade.EXTENSA,
  159 |                 ip=None,
  160 |             )
  161 | 
  162 |     def test_corrigir_resposta_substitui_sem_duplicar(self):
  163 |         """Falha se voltar e corrigir criar duas respostas para EXT-01."""
  164 | 
  165 |         triagem = iniciar_triagem(
  166 |             self.usuario,
  167 |             Triagem.Modalidade.EXTENSA,
  168 |             ip=None,
  169 |         )
  170 |         salvar_resposta(
  171 |             triagem,
  172 |             "EXT-01",
  173 |             {"codigos": ["SIM"], "datas": {}, "detalhes": ""},
  174 |         )
  175 |         voltar_pergunta(triagem)
  176 |         salvar_resposta(
  177 |             triagem,
  178 |             "EXT-01",
  179 |             {"codigos": ["NAO"], "datas": {}, "detalhes": ""},
  180 |         )
  181 | 
  182 |         self.assertEqual(triagem.respostas.count(), 1)
  183 |         self.assertEqual(
  184 |             triagem.respostas.get().codigo_resposta,
  185 |             "NAO",
  186 |         )
  187 | 
  188 |     def test_resposta_simplificada_insere_bloco_extenso_sem_duplicar(self):
  189 |         """Falha se uma mudança estética não abrir todas as perguntas detalhadas."""
  190 | 
  191 |         extensa = Triagem.objects.create(
  192 |             usuario=self.usuario,
  193 |             modalidade=Triagem.Modalidade.EXTENSA,
  194 |             status=Triagem.Status.CONCLUIDA,
  195 |             resultado=Triagem.Resultado.SEM_IMPEDIMENTO,
  196 |         )
  197 |         simplificada = iniciar_triagem(
  198 |             self.usuario,
  199 |             Triagem.Modalidade.SIMPLIFICADA,
  200 |             ip=None,
  201 |         )
  202 | 
  203 |         respostas_ate_sim_10 = {
  204 |             "SIM-01": "CORRETO",
  205 |             "SIM-02": "NAO",
  206 |             "SIM-03": "SIM",
  207 |             "SIM-04": "SIM",
  208 |             "SIM-05": "NAO",
  209 |             "SIM-06": "NAO",
  210 |             "SIM-07": "NAO",
  211 |             "SIM-08": "NAO",
  212 |             "SIM-09": "NAO",
  213 |             "SIM-10": "SIM",
  214 |         }
  215 |         for id_pergunta, codigo in respostas_ate_sim_10.items():
  216 |             self.assertEqual(
  217 |                 obter_pergunta_atual(simplificada)["id"],
  218 |                 id_pergunta,
  219 |             )
  220 |             salvar_resposta(
  221 |                 simplificada,
  222 |                 id_pergunta,
  223 |                 {"codigos": [codigo], "datas": {}, "detalhes": ""},
  224 |             )
  225 | 
  226 |         for id_pergunta in ("EXT-21", "EXT-22", "EXT-23", "EXT-24"):
  227 |             self.assertEqual(
  228 |                 simplificada.fluxo_perguntas.count(id_pergunta),
  229 |                 1,
  230 |             )
  231 |         self.assertLess(
  232 |             simplificada.fluxo_perguntas.index("EXT-24"),
  233 |             simplificada.fluxo_perguntas.index("SIM-17"),
  234 |         )
  235 |         self.assertEqual(simplificada.triagem_base, extensa)
  236 | 
  237 |     def test_conclusao_salva_resultado_e_bloqueia_nova_resposta(self):
  238 |         """Falha se uma triagem concluída puder ser reescrita."""
  239 | 
  240 |         triagem = iniciar_triagem(
  241 |             self.usuario,
  242 |             Triagem.Modalidade.EXTENSA,
  243 |             ip=None,
  244 |         )
  245 | 
  246 |         # Preenche o fluxo efetivo com alternativas neutras para isolar a
  247 |         # transição de conclusão que este teste protege.
  248 |         preferencias_neutras = (
  249 |             "NAO", "NENHUMA", "NENHUM", "NUNCA", "SIM", "18_60",
  250 |             "56_129_9", "MASCULINO", "ORIGINAL", "DESCANSADO",
  251 |             "LEVE", "NAO_MEDI", "NAO_SEI", "CONFIRMAR",
  252 |         )
  253 |         for id_pergunta in triagem.fluxo_perguntas:
  254 |             pergunta = obter_pergunta(id_pergunta)
  255 |             opcoes = {
  256 |                 item["codigo"]: item["rotulo"]
  257 |                 for item in pergunta["opcoes"]
  258 |             }
  259 |             # Algumas perguntas são escritas de forma positiva. Nelas, "SIM"
  260 |             # representa o cenário neutro; nas demais usamos a lista geral.
  261 |             codigo = (
  262 |                 "SIM"
  263 |                 if id_pergunta in {"EXT-01", "EXT-08", "EXT-11"}
  264 |                 else next(
  265 |                     candidato
  266 |                     for candidato in preferencias_neutras
  267 |                     if candidato in opcoes
  268 |                 )
  269 |             )
  270 |             RespostaTriagem.objects.create(
  271 |                 triagem=triagem,
  272 |                 id_pergunta=id_pergunta,
  273 |                 codigo_resposta=codigo,
  274 |                 resposta_label=opcoes[codigo],
  275 |                 valor={"codigos": [codigo], "datas": {}, "detalhes": ""},
  276 |                 rule_version=pergunta["regra_version"],
  277 |                 source_ref=pergunta["fonte"],
  278 |             )
  279 | 
  280 |         concluir_triagem(triagem)
  281 |         triagem.refresh_from_db()
  282 | 
  283 |         self.assertEqual(triagem.status, Triagem.Status.CONCLUIDA)
  284 |         self.assertTrue(triagem.finalizada_em)
  285 |         self.assertEqual(
  286 |             triagem.resultado,
  287 |             Triagem.Resultado.SEM_IMPEDIMENTO,
  288 |         )
  289 |         with self.assertRaises(TriagemConcluida):
  290 |             salvar_resposta(
  291 |                 triagem,
  292 |                 "EXT-51",
  293 |                 {"codigos": ["REVISAR"], "datas": {}, "detalhes": ""},
  294 |             )
  295 | 
  296 |     def test_resposta_mantem_campos_legados_e_valor_completo(self):
  297 |         """Falha se o admin antigo ou o novo motor perderem dados."""
  298 | 
  299 |         triagem = iniciar_triagem(
  300 |             self.usuario,
  301 |             Triagem.Modalidade.EXTENSA,
  302 |             ip=None,
  303 |         )
  304 |         salvar_resposta(
  305 |             triagem,
  306 |             "EXT-01",
  307 |             {"codigos": ["SIM"], "datas": {}, "detalhes": "Entendi."},
  308 |         )
  309 | 
  310 |         resposta = RespostaTriagem.objects.get(triagem=triagem)
  311 |         self.assertEqual(resposta.codigo_resposta, "SIM")
  312 |         self.assertEqual(
  313 |             resposta.resposta_label,
  314 |             "Sim, entendo e quero continuar.",
  315 |         )
  316 |         self.assertEqual(resposta.valor["detalhes"], "Entendi.")
  317 | 
  318 |     def test_nao_entendeu_permanece_na_primeira_pergunta(self):
  319 |         """Falha se EXT-01=NAO avançar sem repetir a explicação."""
  320 | 
  321 |         triagem = iniciar_triagem(
  322 |             self.usuario,
  323 |             Triagem.Modalidade.EXTENSA,
  324 |             ip=None,
  325 |         )
  326 | 
  327 |         salvar_resposta(
  328 |             triagem,
  329 |             "EXT-01",
  330 |             {"codigos": ["NAO"], "datas": {}, "detalhes": ""},
  331 |         )
  332 | 
  333 |         self.assertEqual(triagem.pergunta_atual, 0)
  334 | 
  335 |     def test_revisar_confirmacao_extensa_volta_ao_inicio(self):
  336 |         """Falha se EXT-51=REVISAR não permitir conferir as respostas."""
  337 | 
  338 |         triagem = iniciar_triagem(
  339 |             self.usuario,
  340 |             Triagem.Modalidade.EXTENSA,
  341 |             ip=None,
  342 |         )
  343 |         triagem.pergunta_atual = triagem.fluxo_perguntas.index("EXT-51")
  344 |         triagem.save(update_fields=["pergunta_atual"])
  345 | 
  346 |         salvar_resposta(
  347 |             triagem,
  348 |             "EXT-51",
  349 |             {"codigos": ["REVISAR"], "datas": {}, "detalhes": ""},
  350 |         )
  351 | 
  352 |         self.assertEqual(triagem.pergunta_atual, 0)
  353 | 
  354 |     def test_resumo_incorreto_cancela_rapida_e_exige_extensa(self):
  355 |         """Falha se dados antigos incorretos continuarem na versão rápida."""
  356 | 
  357 |         Triagem.objects.create(
  358 |             usuario=self.usuario,
  359 |             modalidade=Triagem.Modalidade.EXTENSA,
  360 |             status=Triagem.Status.CONCLUIDA,
  361 |             resultado=Triagem.Resultado.SEM_IMPEDIMENTO,
  362 |         )
  363 |         simplificada = iniciar_triagem(
  364 |             self.usuario,
  365 |             Triagem.Modalidade.SIMPLIFICADA,
  366 |             ip=None,
  367 |         )
  368 | 
  369 |         with self.assertRaises(TriagemExtensaNecessaria):
  370 |             salvar_resposta(
  371 |                 simplificada,
  372 |                 "SIM-01",
  373 |                 {
  374 |                     "codigos": ["INCORRETO"],
  375 |                     "datas": {},
  376 |                     "detalhes": "",
  377 |                 },
  378 |             )
  379 | 
  380 |         simplificada.refresh_from_db()
  381 |         self.assertEqual(simplificada.status, Triagem.Status.CANCELADA)
  382 | 
  383 |     def test_correcao_remove_resposta_de_subpergunta_oculta(self):
  384 |         """Falha se uma resposta escondida continuar alterando o resultado."""
  385 | 
  386 |         triagem = iniciar_triagem(
  387 |             self.usuario,
  388 |             Triagem.Modalidade.EXTENSA,
  389 |             ip=None,
  390 |         )
  391 |         salvar_resposta(
  392 |             triagem,
  393 |             "EXT-05",
  394 |             {"codigos": ["SIM"], "datas": {}, "detalhes": ""},
  395 |         )
  396 |         salvar_resposta(
  397 |             triagem,
  398 |             "EXT-05A",
  399 |             {
  400 |                 "codigos": ["DATA"],
  401 |                 "datas": {"DATA": "2026-08-01"},
  402 |                 "detalhes": "",
  403 |             },
  404 |         )
  405 | 
  406 |         # Ao corrigir EXT-05, EXT-05A e EXT-05B deixam de pertencer ao fluxo.
  407 |         salvar_resposta(
  408 |             triagem,
  409 |             "EXT-05",
  410 |             {"codigos": ["NAO"], "datas": {}, "detalhes": ""},
  411 |         )
  412 | 
  413 |         self.assertNotIn("EXT-05A", triagem.fluxo_perguntas)
  414 |         self.assertFalse(
  415 |             triagem.respostas.filter(id_pergunta="EXT-05A").exists()
  416 |         )
  417 | 
  418 |     def test_rapida_respeita_condicoes_das_perguntas_detalhadas(self):
  419 |         """Falha se a rápida mostrar data de doação antes de confirmar doação."""
  420 | 
  421 |         Triagem.objects.create(
  422 |             usuario=self.usuario,
  423 |             modalidade=Triagem.Modalidade.EXTENSA,
  424 |             status=Triagem.Status.CONCLUIDA,
  425 |             resultado=Triagem.Resultado.SEM_IMPEDIMENTO,
  426 |         )
  427 |         simplificada = iniciar_triagem(
  428 |             self.usuario,
  429 |             Triagem.Modalidade.SIMPLIFICADA,
  430 |             ip=None,
  431 |         )
  432 | 
  433 |         salvar_resposta(
  434 |             simplificada,
  435 |             "SIM-02",
  436 |             {"codigos": ["DOOU"], "datas": {}, "detalhes": ""},
  437 |         )
  438 | 
  439 |         self.assertIn("EXT-05", simplificada.fluxo_perguntas)
  440 |         self.assertNotIn("EXT-05A", simplificada.fluxo_perguntas)
  441 | 
  442 |         salvar_resposta(
  443 |             simplificada,
  444 |             "EXT-05",
  445 |             {"codigos": ["SIM"], "datas": {}, "detalhes": ""},
  446 |         )
  447 |         self.assertIn("EXT-05A", simplificada.fluxo_perguntas)
  448 |         self.assertIn("EXT-05B", simplificada.fluxo_perguntas)
``````

## accounts/test_triagem_views.py

Original: [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py>).

``````text
    1 | """
    2 | Testes automatizados das páginas e dos fluxos da triagem.
    3 | 
    4 | Verificam o acesso público e privado, as permissões dos perfis,
    5 | o início da triagem, o consentimento, o salvamento e a edição
    6 | das respostas, a privacidade do histórico, a conclusão da triagem
    7 | e o encaminhamento da versão simplificada para a extensa quando
    8 | as respostas indicam que o histórico anterior não é confiável.
    9 | """
   10 | 
   11 | from django.test import TestCase
   12 | from django.urls import reverse
   13 | 
   14 | from .models import RespostaTriagem, Triagem, Usuario
   15 | from .triagem_catalogo import obter_pergunta
   16 | 
   17 | 
   18 | class TriagemViewsTests(TestCase):
   19 |     """Protege navegação, permissões e privacidade do histórico."""
   20 | 
   21 |     @classmethod
   22 |     def setUpTestData(cls):
   23 |         cls.doador = Usuario.objects.create_user(
   24 |             email="doador.views@teste.com",
   25 |             password="SenhaForte123!",
   26 |             nome="Doador Views",
   27 |             perfil=Usuario.Perfil.DOADOR,
   28 |         )
   29 |         cls.receptor = Usuario.objects.create_user(
   30 |             email="receptor.views@teste.com",
   31 |             password="SenhaForte123!",
   32 |             nome="Receptor Views",
   33 |             perfil=Usuario.Perfil.RECEPTOR,
   34 |         )
   35 |         cls.observador = Usuario.objects.create_user(
   36 |             email="observador.views@teste.com",
   37 |             password="SenhaForte123!",
   38 |             nome="Observador Views",
   39 |             perfil=Usuario.Perfil.OBSERVADOR,
   40 |         )
   41 | 
   42 |     def _criar_extensa_concluida(self, usuario=None):
   43 |         """Cria somente o pré-requisito necessário para a versão rápida."""
   44 | 
   45 |         return Triagem.objects.create(
   46 |             usuario=usuario or self.doador,
   47 |             modalidade=Triagem.Modalidade.EXTENSA,
   48 |             status=Triagem.Status.CONCLUIDA,
   49 |             resultado=Triagem.Resultado.SEM_IMPEDIMENTO,
   50 |         )
   51 | 
   52 |     def _iniciar_pela_rota(self, modalidade="extensa", usuario=None):
   53 |         """Autentica e inicia uma modalidade usando a mesma rota da página."""
   54 | 
   55 |         self.client.force_login(usuario or self.doador)
   56 |         return self.client.post(
   57 |             reverse(
   58 |                 "accounts:triagem_iniciar",
   59 |                 kwargs={"modalidade": modalidade},
   60 |             ),
   61 |             {"aceite_termo": "on"},
   62 |         )
   63 | 
   64 |     def _preencher_ate_confirmacao(self, triagem):
   65 |         """Preenche respostas neutras para testar a conclusão pela view."""
   66 | 
   67 |         preferencias = (
   68 |             "NAO", "NAO_SEI", "NENHUMA", "NENHUM", "NUNCA", "SIM", "18_60",
   69 |             "56_129_9", "MASCULINO", "ORIGINAL", "DESCANSADO",
   70 |             "LEVE", "NAO_MEDI",
   71 |         )
   72 |         for id_pergunta in triagem.fluxo_perguntas[:-1]:
   73 |             pergunta = obter_pergunta(id_pergunta)
   74 |             opcoes = {
   75 |                 opcao["codigo"]: opcao["rotulo"]
   76 |                 for opcao in pergunta["opcoes"]
   77 |             }
   78 |             codigo = (
   79 |                 "SIM"
   80 |                 if id_pergunta in {"EXT-01", "EXT-08", "EXT-11"}
   81 |                 else next(item for item in preferencias if item in opcoes)
   82 |             )
   83 |             RespostaTriagem.objects.create(
   84 |                 triagem=triagem,
   85 |                 id_pergunta=id_pergunta,
   86 |                 codigo_resposta=codigo,
   87 |                 resposta_label=opcoes[codigo],
   88 |                 valor={"codigos": [codigo], "datas": {}, "detalhes": ""},
   89 |                 rule_version=pergunta["regra_version"],
   90 |                 source_ref=pergunta["fonte"],
   91 |             )
   92 |         triagem.pergunta_atual = len(triagem.fluxo_perguntas) - 1
   93 |         triagem.save(update_fields=["pergunta_atual"])
   94 | 
   95 |     def test_apresentacao_publica_mostra_texto_e_duas_modalidades(self):
   96 |         """Falha se o visitante não conhecer as opções antes de se cadastrar."""
   97 | 
   98 |         resposta = self.client.get(reverse("accounts:triagem_apresentacao"))
   99 | 
  100 |         self.assertEqual(resposta.status_code, 200)
  101 |         self.assertContains(resposta, "Seu gesto de cuidado começa aqui.")
  102 |         self.assertContains(resposta, "Triagem extensa")
  103 |         self.assertContains(resposta, "Triagem simplificada")
  104 |         self.assertContains(resposta, "Quem dará a resposta final será sempre")
  105 |         self.assertContains(resposta, "Criar conta")
  106 | 
  107 |     def test_visitante_ve_botoes_de_acao_na_apresentacao(self):
  108 |         """Falha se a apresentação não oferecer ações visíveis ao visitante."""
  109 | 
  110 |         resposta = self.client.get(reverse("accounts:triagem_apresentacao"))
  111 | 
  112 |         self.assertEqual(resposta.status_code, 200)
  113 |         self.assertContains(resposta, "Criar conta para iniciar a triagem extensa")
  114 |         self.assertContains(resposta, "Entrar para continuar uma triagem")
  115 | 
  116 |     def test_inicio_exige_post_e_login(self):
  117 |         """Falha se uma simples visita à URL criar registro no banco."""
  118 | 
  119 |         url = reverse(
  120 |             "accounts:triagem_iniciar",
  121 |             kwargs={"modalidade": "extensa"},
  122 |         )
  123 | 
  124 |         resposta = self.client.post(url)
  125 |         self.assertEqual(resposta.status_code, 302)
  126 |         self.assertIn(reverse("accounts:login"), resposta.url)
  127 | 
  128 |         # Depois de autenticado, GET continua proibido: iniciar exige clique no
  129 |         # formulário POST da apresentação.
  130 |         self.client.force_login(self.doador)
  131 |         self.assertEqual(self.client.get(url).status_code, 405)
  132 |         self.assertEqual(Triagem.objects.count(), 0)
  133 | 
  134 |     def test_doador_pode_iniciar_extensa(self):
  135 |         """Falha se um dos dois perfis autorizados não puder responder."""
  136 | 
  137 |         for usuario in (self.doador,):
  138 |             with self.subTest(perfil=usuario.perfil):
  139 |                 resposta = self._iniciar_pela_rota(usuario=usuario)
  140 |                 triagem = Triagem.objects.get(usuario=usuario)
  141 |                 self.assertRedirects(
  142 |                     resposta,
  143 |                     reverse(
  144 |                         "accounts:triagem_pergunta",
  145 |                         kwargs={"id_triagem": triagem.pk},
  146 |                     ),
  147 |                 )
  148 | 
  149 |     def test_apresentacao_oferece_reutilizar_extensa_concluida(self):
  150 |         """A apresentação oferece o preenchimento a partir do histórico."""
  151 | 
  152 |         self._criar_extensa_concluida()
  153 |         self.client.force_login(self.doador)
  154 | 
  155 |         resposta = self.client.get(reverse("accounts:triagem_apresentacao"))
  156 | 
  157 |         self.assertContains(
  158 |             resposta,
  159 |             "Reutilizar respostas da última triagem extensa concluída.",
  160 |         )
  161 | 
  162 |     def test_observador_nao_pode_iniciar(self):
  163 |         """Falha se um perfil não autorizado puder gravar dados de saúde."""
  164 | 
  165 |         resposta = self._iniciar_pela_rota(usuario=self.observador)
  166 | 
  167 |         self.assertEqual(resposta.status_code, 403)
  168 |         self.assertFalse(Triagem.objects.filter(usuario=self.observador).exists())
  169 | 
  170 |     def test_simplificada_exige_extensa_anterior(self):
  171 |         """Falha se a versão rápida for iniciada sem histórico completo."""
  172 | 
  173 |         resposta = self._iniciar_pela_rota("simplificada")
  174 | 
  175 |         self.assertRedirects(
  176 |             resposta,
  177 |             reverse("accounts:triagem_apresentacao"),
  178 |         )
  179 |         self.assertFalse(
  180 |             Triagem.objects.filter(
  181 |                 usuario=self.doador,
  182 |                 modalidade=Triagem.Modalidade.SIMPLIFICADA,
  183 |             ).exists()
  184 |         )
  185 | 
  186 |     def test_pagina_mostra_uma_pergunta_e_salva_resposta(self):
  187 |         """Falha se a tela não avançar uma pergunta por vez."""
  188 | 
  189 |         self._iniciar_pela_rota()
  190 |         triagem = Triagem.objects.get(usuario=self.doador)
  191 |         url = reverse(
  192 |             "accounts:triagem_pergunta",
  193 |             kwargs={"id_triagem": triagem.pk},
  194 |         )
  195 | 
  196 |         resposta_get = self.client.get(url)
  197 |         self.assertContains(resposta_get, "Você entende que esta pré-triagem")
  198 |         self.assertContains(resposta_get, "Pergunta 1 de")
  199 | 
  200 |         resposta_post = self.client.post(
  201 |             url,
  202 |             {"resposta": "SIM", "acao": "continuar"},
  203 |         )
  204 |         self.assertRedirects(resposta_post, url)
  205 |         triagem.refresh_from_db()
  206 |         self.assertEqual(triagem.pergunta_atual, 1)
  207 |         self.assertTrue(
  208 |             RespostaTriagem.objects.filter(
  209 |                 triagem=triagem,
  210 |                 id_pergunta="EXT-01",
  211 |             ).exists()
  212 |         )
  213 | 
  214 |     def test_salvar_e_sair_conserva_andamento(self):
  215 |         """Falha se a pessoa perder a resposta ao pausar a triagem."""
  216 | 
  217 |         self._iniciar_pela_rota()
  218 |         triagem = Triagem.objects.get(usuario=self.doador)
  219 |         url = reverse(
  220 |             "accounts:triagem_pergunta",
  221 |             kwargs={"id_triagem": triagem.pk},
  222 |         )
  223 | 
  224 |         resposta = self.client.post(
  225 |             url,
  226 |             {"resposta": "SIM", "acao": "salvar"},
  227 |         )
  228 | 
  229 |         self.assertRedirects(resposta, reverse("accounts:triagem_historico"))
  230 |         triagem.refresh_from_db()
  231 |         self.assertEqual(triagem.status, Triagem.Status.EM_ANDAMENTO)
  232 |         self.assertEqual(triagem.pergunta_atual, 1)
  233 | 
  234 |     def test_botao_anterior_retorna_sem_apagar_resposta(self):
  235 |         """Falha se voltar apagar informação já salva."""
  236 | 
  237 |         self._iniciar_pela_rota()
  238 |         triagem = Triagem.objects.get(usuario=self.doador)
  239 |         url = reverse(
  240 |             "accounts:triagem_pergunta",
  241 |             kwargs={"id_triagem": triagem.pk},
  242 |         )
  243 |         self.client.post(url, {"resposta": "SIM", "acao": "continuar"})
  244 | 
  245 |         resposta = self.client.post(url, {"acao": "anterior"})
  246 | 
  247 |         self.assertRedirects(resposta, url)
  248 |         triagem.refresh_from_db()
  249 |         self.assertEqual(triagem.pergunta_atual, 0)
  250 |         self.assertTrue(triagem.respostas.filter(id_pergunta="EXT-01").exists())
  251 | 
  252 |     def test_triagem_de_outro_usuario_retorna_404(self):
  253 |         """Falha se respostas de saúde puderem ser acessadas por outra conta."""
  254 | 
  255 |         triagem = Triagem.objects.create(
  256 |             usuario=self.receptor,
  257 |             modalidade=Triagem.Modalidade.EXTENSA,
  258 |         )
  259 |         self.client.force_login(self.doador)
  260 | 
  261 |         pergunta = self.client.get(
  262 |             reverse(
  263 |                 "accounts:triagem_pergunta",
  264 |                 kwargs={"id_triagem": triagem.pk},
  265 |             )
  266 |         )
  267 |         resultado = self.client.get(
  268 |             reverse(
  269 |                 "accounts:triagem_resultado",
  270 |                 kwargs={"id_triagem": triagem.pk},
  271 |             )
  272 |         )
  273 | 
  274 |         self.assertEqual(pergunta.status_code, 404)
  275 |         self.assertEqual(resultado.status_code, 404)
  276 | 
  277 |     def test_resultado_em_andamento_volta_para_pergunta(self):
  278 |         """Falha se um resultado vazio for mostrado antes da confirmação."""
  279 | 
  280 |         self._iniciar_pela_rota()
  281 |         triagem = Triagem.objects.get(usuario=self.doador)
  282 | 
  283 |         resposta = self.client.get(
  284 |             reverse(
  285 |                 "accounts:triagem_resultado",
  286 |                 kwargs={"id_triagem": triagem.pk},
  287 |             )
  288 |         )
  289 | 
  290 |         self.assertRedirects(
  291 |             resposta,
  292 |             reverse("accounts:triagem_revisao", kwargs={"id_triagem": triagem.pk}),
  293 |         )
  294 | 
  295 |     def test_confirmacao_final_conclui_e_mostra_resultado(self):
  296 |         """Falha se a última resposta não congelar a orientação calculada."""
  297 | 
  298 |         self._iniciar_pela_rota()
  299 |         triagem = Triagem.objects.get(usuario=self.doador)
  300 |         self._preencher_ate_confirmacao(triagem)
  301 |         url = reverse(
  302 |             "accounts:triagem_pergunta",
  303 |             kwargs={"id_triagem": triagem.pk},
  304 |         )
  305 | 
  306 |         resposta = self.client.post(
  307 |             url,
  308 |             {"resposta": "CONFIRMAR", "acao": "continuar"},
  309 |         )
  310 | 
  311 |         self.assertRedirects(
  312 |             resposta,
  313 |             reverse("accounts:triagem_revisao", kwargs={"id_triagem": triagem.pk}),
  314 |         )
  315 |         triagem.refresh_from_db()
  316 |         self.assertEqual(triagem.status, Triagem.Status.EM_ANDAMENTO)
  317 | 
  318 |         resposta_final = self.client.post(
  319 |             reverse("accounts:triagem_revisao", kwargs={"id_triagem": triagem.pk}),
  320 |             {"acao": "finalizar"},
  321 |         )
  322 |         self.assertRedirects(
  323 |             resposta_final,
  324 |             reverse("accounts:triagem_resultado", kwargs={"id_triagem": triagem.pk}),
  325 |         )
  326 |         triagem.refresh_from_db()
  327 |         self.assertEqual(triagem.status, Triagem.Status.CONCLUIDA)
  328 | 
  329 |     def test_resumo_incorreto_abre_nova_extensa(self):
  330 |         """Falha se a rápida continuar usando um histórico declarado incorreto."""
  331 | 
  332 |         self._criar_extensa_concluida()
  333 |         self._iniciar_pela_rota("simplificada")
  334 |         simplificada = Triagem.objects.get(
  335 |             usuario=self.doador,
  336 |             modalidade=Triagem.Modalidade.SIMPLIFICADA,
  337 |         )
  338 |         url = reverse(
  339 |             "accounts:triagem_pergunta",
  340 |             kwargs={"id_triagem": simplificada.pk},
  341 |         )
  342 | 
  343 |         resposta = self.client.post(
  344 |             url,
  345 |             {"resposta": "INCORRETO", "acao": "continuar"},
  346 |         )
  347 | 
  348 |         simplificada.refresh_from_db()
  349 |         nova_extensa = Triagem.objects.get(
  350 |             usuario=self.doador,
  351 |             modalidade=Triagem.Modalidade.EXTENSA,
  352 |             status=Triagem.Status.EM_ANDAMENTO,
  353 |         )
  354 |         self.assertEqual(simplificada.status, Triagem.Status.CANCELADA)
  355 |         self.assertRedirects(
  356 |             resposta,
  357 |             reverse(
  358 |                 "accounts:triagem_pergunta",
  359 |                 kwargs={"id_triagem": nova_extensa.pk},
  360 |             ),
  361 |         )
  362 | 
  363 |     def test_historico_lista_somente_triagens_do_usuario(self):
  364 |         """Falha se o histórico revelar registros de outra pessoa."""
  365 | 
  366 |         propria = self._criar_extensa_concluida(self.doador)
  367 |         alheia = self._criar_extensa_concluida(self.receptor)
  368 |         self.client.force_login(self.doador)
  369 | 
  370 |         resposta = self.client.get(reverse("accounts:triagem_historico"))
  371 | 
  372 |         self.assertEqual(resposta.status_code, 200)
  373 |         self.assertContains(resposta, f"Triagem {propria.pk}")
  374 |         self.assertNotContains(resposta, f"Triagem {alheia.pk}")
  375 | 
  376 |     def test_dashboard_doador_aponta_para_triagem(self):
  377 |         """Falha se um perfil autorizado não encontrar a triagem no painel."""
  378 | 
  379 |         for usuario in (self.doador,):
  380 |             with self.subTest(perfil=usuario.perfil):
  381 |                 self.client.force_login(usuario)
  382 |                 resposta = self.client.get(reverse("accounts:dashboard"))
  383 |                 self.assertContains(resposta, "Triagem para doação")
  384 |                 self.assertContains(
  385 |                     resposta,
  386 |                     reverse("accounts:triagem_apresentacao"),
  387 |                 )
  388 | 
  389 |     def test_receptor_bloqueado_inclusive_triagem_antiga(self):
  390 |         self.client.force_login(self.receptor)
  391 |         triagem = self._criar_extensa_concluida(self.receptor)
  392 |         for rota in ('triagem_pergunta', 'triagem_resultado'):
  393 |             resposta = self.client.get(reverse('accounts:' + rota, kwargs={'id_triagem': triagem.pk}))
  394 |             self.assertEqual(resposta.status_code, 403)
  395 |         self.assertEqual(self._iniciar_pela_rota(usuario=self.receptor).status_code, 403)
  396 |         self.assertNotContains(self.client.get(reverse('accounts:dashboard')), 'Triagem para doação')
``````

## accounts/test_visualizacao.py

Original: [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py>).

``````text
    1 | from datetime import date
    2 | 
    3 | from django.test import TestCase
    4 | from django.urls import reverse
    5 | from django.utils import timezone
    6 | 
    7 | from .estoque import cadastrar_estoque
    8 | from .models import Estoque, PedidoSangue, Usuario
    9 | from .validacao_hemocentro import aprovar_hemocentro
   10 | 
   11 | 
   12 | class VisualizacaoPublicaTests(TestCase):
   13 |     def criar_usuario(self, *, email, nome, perfil, cidade="", estado=""):
   14 |         return Usuario.objects.create_user(
   15 |             email=email,
   16 |             password="SenhaForte123!",
   17 |             nome=nome,
   18 |             perfil=perfil,
   19 |             cidade=cidade,
   20 |             estado=estado,
   21 |         )
   22 | 
   23 |     def setUp(self):
   24 |         self.admin = self.criar_usuario(
   25 |             email="admin@visualizacao.test",
   26 |             nome="Administrador",
   27 |             perfil=Usuario.Perfil.ADMINISTRADOR,
   28 |         )
   29 | 
   30 |         self.hemocentro = self.criar_usuario(
   31 |             email="hemocentro@visualizacao.test",
   32 |             nome="Hemocentro Central",
   33 |             perfil=Usuario.Perfil.HEMOCENTRO,
   34 |             cidade="Muzambinho",
   35 |             estado="MG",
   36 |         )
   37 | 
   38 |         aprovar_hemocentro(
   39 |             hemocentro=self.hemocentro,
   40 |             admin=self.admin,
   41 |         )
   42 | 
   43 |         self.hemocentro.refresh_from_db()
   44 | 
   45 |         self.hemocentro_pendente = self.criar_usuario(
   46 |             email="pendente@visualizacao.test",
   47 |             nome="Hemocentro Pendente",
   48 |             perfil=Usuario.Perfil.HEMOCENTRO,
   49 |             cidade="Alfenas",
   50 |             estado="MG",
   51 |         )
   52 | 
   53 |     def pedido(self, *, status, tipo="O-", urgencia="ALTA"):
   54 |         return PedidoSangue.objects.create(
   55 |             nome_solicitante="Solicitante",
   56 |             contato="solicitante@visualizacao.test",
   57 |             hemocentro_destino=self.hemocentro,
   58 |             para_quem=PedidoSangue.ParaQuem.MIM,
   59 |             titulo=f"Pedido urgente de sangue {tipo}",
   60 |             tipo_sanguineo=tipo,
   61 |             urgencia=urgencia,
   62 |             cidade="Muzambinho",
   63 |             descricao=(
   64 |                 "Necessidade de doadores para atendimento hospitalar."
   65 |             ),
   66 |             status=status,
   67 |             publicado_em=(
   68 |                 timezone.now()
   69 |                 if status == PedidoSangue.Status.PUBLICADA
   70 |                 else None
   71 |             ),
   72 |         )
   73 | 
   74 |     def test_consulta_de_pedidos_aplica_filtros_e_oculta_nao_publicados(
   75 |         self,
   76 |     ):
   77 |         publicado = self.pedido(
   78 |             status=PedidoSangue.Status.PUBLICADA,
   79 |         )
   80 | 
   81 |         pendente = self.pedido(
   82 |             status=PedidoSangue.Status.ENVIADA,
   83 |             tipo="A+",
   84 |         )
   85 | 
   86 |         resposta = self.client.get(
   87 |             reverse("accounts:consultar_pedidos"),
   88 |             {
   89 |                 "tipo_sanguineo": "O-",
   90 |                 "urgencia": "ALTA",
   91 |                 "cidade": "Muzambinho",
   92 |                 "hemocentro": "Central",
   93 |                 "data": date.today().isoformat(),
   94 |                 "status": "PUBLICADA",
   95 |             },
   96 |         )
   97 | 
   98 |         self.assertEqual(resposta.status_code, 200)
   99 |         self.assertContains(resposta, publicado.titulo)
  100 |         self.assertNotContains(resposta, pendente.titulo)
  101 | 
  102 |         resposta = self.client.get(
  103 |             reverse("accounts:consultar_pedidos"),
  104 |             {
  105 |                 "status": "ENVIADA",
  106 |             },
  107 |         )
  108 | 
  109 |         self.assertNotContains(resposta, publicado.titulo)
  110 | 
  111 |     def test_consulta_de_pedidos_nao_exibe_destino_nao_aprovado(self):
  112 |         pedido = PedidoSangue.objects.create(
  113 |             nome_solicitante="Solicitante",
  114 |             contato="solicitante@visualizacao.test",
  115 |             hemocentro_destino=self.hemocentro_pendente,
  116 |             para_quem=PedidoSangue.ParaQuem.MIM,
  117 |             titulo="Pedido de destino pendente",
  118 |             tipo_sanguineo="O-",
  119 |             urgencia=PedidoSangue.Urgencia.MEDIA,
  120 |             cidade="Alfenas",
  121 |             descricao=(
  122 |                 "Pedido que não deve aparecer na consulta pública."
  123 |             ),
  124 |             status=PedidoSangue.Status.PUBLICADA,
  125 |         )
  126 | 
  127 |         resposta = self.client.get(
  128 |             reverse("accounts:consultar_pedidos")
  129 |         )
  130 | 
  131 |         self.assertNotContains(resposta, pedido.titulo)
  132 | 
  133 |     def test_consulta_de_estoques_filtra_por_tipo_situacao_e_busca(
  134 |         self,
  135 |     ):
  136 |         cadastrar_estoque(
  137 |             hemocentro=self.hemocentro,
  138 |             tipo_sanguineo="O-",
  139 |             quantidade_bolsas=2,
  140 |             nivel_minimo=10,
  141 |             nivel_critico=5,
  142 |         )
  143 | 
  144 |         cadastrar_estoque(
  145 |             hemocentro=self.hemocentro,
  146 |             tipo_sanguineo="A+",
  147 |             quantidade_bolsas=20,
  148 |             nivel_minimo=10,
  149 |             nivel_critico=5,
  150 |         )
  151 | 
  152 |         Estoque.objects.create(
  153 |             hemocentro=self.hemocentro_pendente,
  154 |             tipo_sanguineo="B+",
  155 |             quantidade_bolsas=10,
  156 |             nivel_minimo=10,
  157 |             nivel_critico=5,
  158 |         )
  159 | 
  160 |         resposta = self.client.get(
  161 |             reverse("accounts:estoque_publico"),
  162 |             {
  163 |                 "tipo_sanguineo": "O-",
  164 |                 "situacao": "CRITICO",
  165 |                 "busca": "Central",
  166 |             },
  167 |         )
  168 | 
  169 |         self.assertEqual(resposta.status_code, 200)
  170 |         self.assertContains(resposta, "O-")
  171 |         self.assertContains(resposta, "Crítico")
  172 |         self.assertNotContains(resposta, "20 bolsas")
  173 |         self.assertNotContains(resposta, "Hemocentro Pendente")
  174 | 
  175 |     def test_consulta_de_estoques_preserva_parametros_antigos(self):
  176 |         cadastrar_estoque(
  177 |             hemocentro=self.hemocentro,
  178 |             tipo_sanguineo="O-",
  179 |             quantidade_bolsas=2,
  180 |             nivel_minimo=10,
  181 |             nivel_critico=5,
  182 |         )
  183 | 
  184 |         resposta = self.client.get(
  185 |             reverse("accounts:estoque_publico"),
  186 |             {
  187 |                 "q": "Muzambinho",
  188 |                 "tipo": "O-",
  189 |             },
  190 |         )
  191 | 
  192 |         self.assertContains(resposta, "O-")
``````

## accounts/tests.py

Original: [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py>).

``````text
    1 | """
    2 | RESUMO DO ARQUIVO
    3 | =================
    4 | Testes automatizados executam o fluxo sem abrir o navegador. Cada teste usa um
    5 | banco temporario e e isolado dos demais.
    6 | 
    7 | Os testes abaixo verificam o minimo mais importante desta entrega:
    8 | 
    9 | 1. cadastro cria conta, hash de senha e consentimento;
   10 | 2. login aceita e-mail e senha corretos;
   11 | 3. visitante acessa busca publica, estoque geral e pedidos ativos;
   12 | 4. dashboard redireciona visitantes para o login;
   13 | 5. perfis cadastrados recebem paineis proprios.
   14 | 
   15 | Execute com: ``python manage.py test``.
   16 | 
   17 | 
   18 | Os testes verificam:
   19 | - novo Hemocentro inicia como PENDENTE;
   20 | - administrador consegue aprovar, recusar ou solicitar correcao;
   21 | - cada decisao gera historico;
   22 | - usuario comum nao pode executar a decisao;
   23 | - Hemocentro nao aprovado nao consegue publicar;
   24 | - Hemocentro aprovado pode seguir para a rotina de publicacao.
   25 | """
   26 | 
   27 | from django.core.exceptions import PermissionDenied
   28 | from django.test import TestCase
   29 | from django.urls import reverse
   30 | 
   31 | from .models import AuditoriaAcaoCritica, Estoque, Usuario, ValidacaoHemocentro
   32 | from .validacao_hemocentro import (
   33 |     aprovar_hemocentro,
   34 |     hemocentro_aprovado,
   35 |     recusar_hemocentro,
   36 |     solicitar_correcao_hemocentro,
   37 |     validar_publicacao_hemocentro,
   38 | )
   39 | 
   40 | 
   41 | class ValidacaoHemocentroTests(TestCase):
   42 |     """Testes principais do UC_07."""
   43 | 
   44 |     def criar_usuario(
   45 |         self,
   46 |         *,
   47 |         email,
   48 |         nome,
   49 |         perfil,
   50 |         is_staff=False,
   51 |         is_superuser=False,
   52 |     ):
   53 |         """Cria usuario usando o manager real do projeto."""
   54 | 
   55 |         return Usuario.objects.create_user(
   56 |             email=email,
   57 |             password="SenhaForte123!",
   58 |             nome=nome,
   59 |             perfil=perfil,
   60 |             is_staff=is_staff,
   61 |             is_superuser=is_superuser,
   62 |         )
   63 | 
   64 |     def setUp(self):
   65 |         """Prepara um administrador e um Hemocentro para cada teste."""
   66 | 
   67 |         self.admin = self.criar_usuario(
   68 |             email="admin@elo.test",
   69 |             nome="Administrador Elo",
   70 |             perfil=Usuario.Perfil.ADMINISTRADOR,
   71 |         )
   72 | 
   73 |         self.hemocentro = self.criar_usuario(
   74 |             email="hemocentro@elo.test",
   75 |             nome="Hemocentro Elo",
   76 |             perfil=Usuario.Perfil.HEMOCENTRO,
   77 |         )
   78 | 
   79 |     def test_hemocentro_inicia_pendente(self):
   80 |         """Conta de Hemocentro nova deve aguardar analise."""
   81 | 
   82 |         self.assertEqual(
   83 |             self.hemocentro.status_validacao,
   84 |             Usuario.StatusValidacaoHemocentro.PENDENTE,
   85 |         )
   86 |         self.assertFalse(hemocentro_aprovado(self.hemocentro))
   87 | 
   88 |     def test_admin_aprova_e_cria_historico(self):
   89 |         """Aprovacao altera status, cria historico e gera auditoria."""
   90 | 
   91 |         validacao = aprovar_hemocentro(
   92 |             hemocentro=self.hemocentro,
   93 |             admin=self.admin,
   94 |         )
   95 | 
   96 |         self.hemocentro.refresh_from_db()
   97 | 
   98 |         self.assertEqual(
   99 |             self.hemocentro.status_validacao,
  100 |             Usuario.StatusValidacaoHemocentro.APROVADO,
  101 |         )
  102 |         self.assertEqual(
  103 |             validacao.status,
  104 |             Usuario.StatusValidacaoHemocentro.APROVADO,
  105 |         )
  106 |         self.assertEqual(
  107 |             ValidacaoHemocentro.objects.filter(
  108 |                 hemocentro=self.hemocentro
  109 |             ).count(),
  110 |             1,
  111 |         )
  112 |         self.assertTrue(
  113 |             AuditoriaAcaoCritica.objects.filter(
  114 |                 acao=AuditoriaAcaoCritica.Acao.APROVACAO_HEMOCENTRO,
  115 |                 usuario=self.admin,
  116 |                 alvo_id=str(self.hemocentro.pk),
  117 |             ).exists()
  118 |         )
  119 | 
  120 |     def test_admin_recusa(self):
  121 |         """Recusa altera o status e guarda o parecer."""
  122 | 
  123 |         validacao = recusar_hemocentro(
  124 |             hemocentro=self.hemocentro,
  125 |             admin=self.admin,
  126 |             parecer="CNPJ nao confere com os documentos enviados.",
  127 |         )
  128 | 
  129 |         self.hemocentro.refresh_from_db()
  130 | 
  131 |         self.assertEqual(
  132 |             self.hemocentro.status_validacao,
  133 |             Usuario.StatusValidacaoHemocentro.RECUSADO,
  134 |         )
  135 |         self.assertEqual(
  136 |             validacao.parecer,
  137 |             "CNPJ nao confere com os documentos enviados.",
  138 |         )
  139 | 
  140 |     def test_admin_solicita_correcao(self):
  141 |         """Solicitacao de correcao coloca o cadastro em CORRECAO."""
  142 | 
  143 |         solicitar_correcao_hemocentro(
  144 |             hemocentro=self.hemocentro,
  145 |             admin=self.admin,
  146 |             parecer="Atualize telefone e endereco.",
  147 |         )
  148 | 
  149 |         self.hemocentro.refresh_from_db()
  150 | 
  151 |         self.assertEqual(
  152 |             self.hemocentro.status_validacao,
  153 |             Usuario.StatusValidacaoHemocentro.CORRECAO,
  154 |         )
  155 | 
  156 |     def test_usuario_comum_nao_pode_validar(self):
  157 |         """Somente administrador pode registrar a decisao."""
  158 | 
  159 |         usuario_comum = self.criar_usuario(
  160 |             email="doador@elo.test",
  161 |             nome="Doador",
  162 |             perfil=Usuario.Perfil.DOADOR,
  163 |         )
  164 | 
  165 |         with self.assertRaises(PermissionDenied):
  166 |             aprovar_hemocentro(
  167 |                 hemocentro=self.hemocentro,
  168 |                 admin=usuario_comum,
  169 |             )
  170 | 
  171 |     def test_hemocentro_nao_aprovado_nao_publica(self):
  172 |         """Pendente, recusado e correcao devem bloquear publicacao."""
  173 | 
  174 |         for status in (
  175 |             Usuario.StatusValidacaoHemocentro.PENDENTE,
  176 |             Usuario.StatusValidacaoHemocentro.RECUSADO,
  177 |             Usuario.StatusValidacaoHemocentro.CORRECAO,
  178 |         ):
  179 |             self.hemocentro.status_validacao = status
  180 |             self.hemocentro.save(update_fields=["status_validacao"])
  181 | 
  182 |             with self.assertRaises(PermissionDenied):
  183 |                 validar_publicacao_hemocentro(self.hemocentro)
  184 | 
  185 |     def test_hemocentro_aprovado_pode_publicar(self):
  186 |         """Status aprovado libera a regra de publicacao."""
  187 | 
  188 |         aprovar_hemocentro(
  189 |             hemocentro=self.hemocentro,
  190 |             admin=self.admin,
  191 |         )
  192 |         self.hemocentro.refresh_from_db()
  193 | 
  194 |         self.assertTrue(validar_publicacao_hemocentro(self.hemocentro))
  195 | 
  196 |     def test_dashboard_hemocentro_mostra_status_sem_link_de_aprovacao(self):
  197 |         """Hemocentro ve seu status, mas nao acessa validacao administrativa."""
  198 | 
  199 |         self.client.force_login(self.hemocentro)
  200 | 
  201 |         resposta = self.client.get(reverse("accounts:dashboard"))
  202 | 
  203 |         self.assertContains(
  204 |             resposta,
  205 |             "Status da validação institucional",
  206 |         )
  207 |         self.assertContains(resposta, "Pendente")
  208 |         self.assertNotContains(resposta, "Gestão de Hemocentros")
  209 |         self.assertNotContains(
  210 |             resposta,
  211 |             "Acessar aprovação de Hemocentros",
  212 |         )
  213 | 
  214 |     def test_admin_acessa_tela_de_validacao_e_ve_pendente(self):
  215 |         """Administrador deve receber a tela da aplicacao com os pendentes."""
  216 | 
  217 |         self.client.force_login(self.admin)
  218 | 
  219 |         resposta = self.client.get(reverse("accounts:dashboard"))
  220 | 
  221 |         self.assertContains(resposta, "Validação de Hemocentros")
  222 |         self.assertContains(
  223 |             resposta,
  224 |             "Acessar aprovação de Hemocentros",
  225 |         )
  226 |         self.assertContains(
  227 |             resposta,
  228 |             "<li>Aprovar Hemocentros.</li>",
  229 |             html=True,
  230 |         )
  231 |         self.assertContains(resposta, 'href="/admin/"')
  232 | 
  233 |         painel = self.client.get(
  234 |             reverse("accounts:painel_aprovacao_hemocentros")
  235 |         )
  236 | 
  237 |         self.assertEqual(painel.status_code, 200)
  238 |         self.assertContains(painel, self.hemocentro.nome)
  239 |         self.assertContains(painel, "Pendente")
  240 |         self.assertContains(painel, "Voltar ao painel")
  241 |         self.assertContains(painel, "Página inicial")
  242 |         self.assertContains(painel, "Estoques públicos")
  243 | 
  244 |     def test_admin_aprova_pelo_painel_e_libera_estoque(self):
  245 |         """A aprovacao feita na tela altera o status e libera o estoque."""
  246 | 
  247 |         self.client.force_login(self.admin)
  248 | 
  249 |         resposta = self.client.post(
  250 |             reverse(
  251 |                 "accounts:aprovar_hemocentro",
  252 |                 kwargs={"id_hemocentro": self.hemocentro.pk},
  253 |             ),
  254 |             {"parecer": "Documentacao conferida."},
  255 |         )
  256 | 
  257 |         self.assertRedirects(
  258 |             resposta,
  259 |             reverse("accounts:painel_aprovacao_hemocentros"),
  260 |         )
  261 | 
  262 |         self.hemocentro.refresh_from_db()
  263 | 
  264 |         self.assertEqual(
  265 |             self.hemocentro.status_validacao,
  266 |             Usuario.StatusValidacaoHemocentro.APROVADO,
  267 |         )
  268 | 
  269 |         self.client.force_login(self.hemocentro)
  270 | 
  271 |         estoque = self.client.get(
  272 |             reverse("accounts:estoque_hemocentro")
  273 |         )
  274 | 
  275 |         self.assertEqual(estoque.status_code, 200)
  276 |         self.assertContains(estoque, "Cadastrar novo estoque")
  277 | 
  278 |         cadastro_estoque = self.client.post(
  279 |             reverse("accounts:cadastrar_estoque"),
  280 |             {
  281 |                 "tipo_sanguineo": "O+",
  282 |                 "quantidade_bolsas": 8,
  283 |                 "nivel_minimo": 10,
  284 |                 "nivel_critico": 5,
  285 |             },
  286 |         )
  287 | 
  288 |         self.assertRedirects(
  289 |             cadastro_estoque,
  290 |             reverse("accounts:estoque_hemocentro"),
  291 |         )
  292 | 
  293 |         self.assertTrue(
  294 |             Estoque.objects.filter(
  295 |                 hemocentro=self.hemocentro,
  296 |                 tipo_sanguineo="O+",
  297 |             ).exists()
  298 |         )
  299 | 
  300 |     def test_usuario_comum_nao_acessa_tela_de_validacao(self):
  301 |         """A tela e suas acoes continuam restritas ao Administrador."""
  302 | 
  303 |         usuario_comum = self.criar_usuario(
  304 |             email="doador-tela@elo.test",
  305 |             nome="Doador",
  306 |             perfil=Usuario.Perfil.DOADOR,
  307 |         )
  308 | 
  309 |         self.client.force_login(usuario_comum)
  310 | 
  311 |         resposta = self.client.get(
  312 |             reverse("accounts:painel_aprovacao_hemocentros")
  313 |         )
  314 | 
  315 |         self.assertEqual(resposta.status_code, 403)
  316 | 
  317 |     def test_dashboard_admin_nao_mostra_publicacao_de_pedido(self):
  318 |         """Administrador não atua como Hemocentro na publicação."""
  319 | 
  320 |         self.client.force_login(self.admin)
  321 | 
  322 |         resposta = self.client.get(reverse("accounts:dashboard"))
  323 | 
  324 |         self.assertContains(resposta, "Pedidos ativos")
  325 |         self.assertNotContains(
  326 |             resposta,
  327 |             "Publicar pedido de sangue",
  328 |         )
  329 |         self.assertNotContains(
  330 |             resposta,
  331 |             "Solicitar divulgação de necessidade",
  332 |         )
  333 | 
  334 | 
  335 | class AuditoriaTests(TestCase):
  336 |     @classmethod
  337 |     def setUpTestData(cls):
  338 |         cls.admin = Usuario.objects.create_superuser(
  339 |             email='auditoria.admin@elo.test', password='SenhaForte123!',
  340 |             nome='Administrador', perfil=Usuario.Perfil.ADMINISTRADOR,
  341 |         )
  342 |         cls.doador = Usuario.objects.create_user(
  343 |             email='auditoria.doador@elo.test', password='SenhaForte123!',
  344 |             nome='Doador', perfil=Usuario.Perfil.DOADOR,
  345 |         )
  346 | 
  347 |     def test_acesso_bloqueado_registrado(self):
  348 |         self.client.force_login(self.doador)
  349 |         resposta = self.client.get(reverse('accounts:painel_validacao_pedidos'))
  350 |         self.assertEqual(resposta.status_code, 403)
  351 |         registro = AuditoriaAcaoCritica.objects.get()
  352 |         self.assertEqual(registro.usuario, self.doador)
  353 |         self.assertEqual(registro.resultado, AuditoriaAcaoCritica.Resultado.BLOQUEADO)
  354 |         self.assertEqual(registro.metadados['evento'], 'TENTATIVA_ACESSO')
  355 | 
  356 |     def test_acesso_a_triagem_registra_alvo_sem_respostas(self):
  357 |         from .models import Triagem
  358 |         triagem = Triagem.objects.create(usuario=self.doador, modalidade=Triagem.Modalidade.EXTENSA,
  359 |                                         status=Triagem.Status.CONCLUIDA,
  360 |                                         mensagem_resultado='CONTEUDO_CLINICO_PRIVADO')
  361 |         self.client.force_login(self.doador)
  362 |         resposta = self.client.get(reverse('accounts:triagem_resultado', kwargs={'id_triagem': triagem.pk}))
  363 |         self.assertEqual(resposta.status_code, 200)
  364 |         registro = AuditoriaAcaoCritica.objects.get()
  365 |         self.assertEqual(registro.acao, AuditoriaAcaoCritica.Acao.ACESSO_DADOS_SENSIVEIS)
  366 |         self.assertEqual(registro.metadados['parametros']['id_triagem'], triagem.pk)
  367 |         self.assertNotIn('CONTEUDO_CLINICO_PRIVADO', str(registro.metadados))
  368 | 
  369 |     def test_auditoria_exclusiva_administrador_e_somente_leitura(self):
  370 |         from django.contrib import admin
  371 |         from django.test import RequestFactory
  372 |         from django.contrib.auth.models import Permission
  373 |         modelo_admin = admin.site._registry[AuditoriaAcaoCritica]
  374 |         request = RequestFactory().get('/admin/')
  375 |         request.user = self.admin
  376 |         self.assertTrue(modelo_admin.has_view_permission(request))
  377 |         self.assertFalse(modelo_admin.has_add_permission(request))
  378 |         self.assertFalse(modelo_admin.has_change_permission(request))
  379 |         self.assertFalse(modelo_admin.has_delete_permission(request))
  380 |         self.doador.is_staff = True
  381 |         self.doador.save()
  382 |         self.doador.user_permissions.add(Permission.objects.get(codename='view_auditoriaacaocritica'))
  383 |         request.user = Usuario.objects.get(pk=self.doador.pk)
  384 |         self.assertFalse(modelo_admin.has_view_permission(request))
  385 |         self.assertFalse(modelo_admin.has_module_permission(request))
  386 | 
  387 |     def test_suspensao_registrada_sem_duplicar_dados_pessoais(self):
  388 |         from django.contrib import admin
  389 |         from django.test import RequestFactory
  390 |         request = RequestFactory().post('/admin/')
  391 |         request.user = self.admin
  392 |         self.doador.is_active = False
  393 |         self.doador.nome = 'Nome atualizado'
  394 |         admin.site._registry[Usuario].save_model(request, self.doador, None, True)
  395 |         registro = AuditoriaAcaoCritica.objects.get()
  396 |         self.assertEqual(registro.metadados['evento'], 'SUSPENSAO_USUARIO')
  397 |         self.assertEqual(registro.metadados['alteracoes']['is_active'], {'antes': 'True', 'depois': 'False'})
  398 |         self.assertIn('nome', registro.metadados['campos_alterados'])
  399 |         self.assertNotIn('Nome atualizado', str(registro.metadados))
  400 | 
  401 |     def test_login_suspeito_nao_afirma_bloqueio(self):
  402 |         from .signals import auditar_login_falho
  403 |         from django.test import RequestFactory
  404 |         request = RequestFactory().post('/login/')
  405 |         for _ in range(5):
  406 |             auditar_login_falho(None, {'username': 'tentativa@elo.test', 'password': 'SEGREDO'}, request)
  407 |         registro = AuditoriaAcaoCritica.objects.get(acao=AuditoriaAcaoCritica.Acao.LOGIN_SUSPEITO)
  408 |         self.assertEqual(registro.resultado, AuditoriaAcaoCritica.Resultado.FALHA)
  409 |         self.assertNotIn('SEGREDO', str(registro.metadados))
  410 | 
  411 |     def test_sanitizacao_recursiva(self):
  412 |         from .auditoria import registrar_auditoria
  413 |         registro = registrar_auditoria(acao=AuditoriaAcaoCritica.Acao.MODERACAO,
  414 |             metadados={'dados': [{'password': 'SEGREDO', 'TOKEN': 'SEGREDO', 'evento': 'teste'}]})
  415 |         self.assertNotIn('SEGREDO', str(registro.metadados))
  416 |         self.assertEqual(registro.metadados['dados'][0]['evento'], 'teste')
  417 | 
  418 |     def test_ip_nao_confia_em_cabecalho_do_cliente(self):
  419 |         from .auditoria import obter_ip
  420 |         from django.test import RequestFactory
  421 |         request = RequestFactory().get('/login/', REMOTE_ADDR='127.0.0.1', HTTP_X_FORWARDED_FOR='IP_FORJADO')
  422 |         self.assertEqual(obter_ip(request), '127.0.0.1')
  423 |         request.META['REMOTE_ADDR'] = 'IP_INVALIDO'
  424 |         self.assertIsNone(obter_ip(request))
``````

## accounts/triagem.py

Original: [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py>).

``````text
    1 | # Este módulo calcula o resultado inicial da triagem extensa. A triagem é apenas orientativa e não substitui a avaliação do Hemocentro.
    2 | 
    3 | # TRIAGEM_RULE_VERSION: Identifica a versão das regras usadas no cálculo.
    4 | 
    5 | # QUESTION_FIELDS: Relaciona cada campo do formulário ao código da pergunta e à origem correspondente no documento oficial da triagem.
    6 | 
    7 | # adicionar_achado()
    8 | # --------------------
    9 | # Registra um problema, impedimento ou alerta encontrado durante a análise.
   10 | # O achado guarda:
   11 | # - código da pergunta;
   12 | # - resultado gerado;
   13 | # - mensagem explicativa;
   14 | # - data de liberação, quando existir.
   15 | # Nenhum achado anterior é apagado.
   16 | 
   17 | # escolher_resultado()
   18 | # --------------------
   19 | # Analisa todos os achados e escolhe o resultado mais restritivo.
   20 | # Ordem de prioridade:
   21 | # 1. DEFINITIVA;
   22 | # 2. AVALIACAO;
   23 | # 3. TEMPORARIA;
   24 | # 4. DOCUMENTACAO.
   25 | # Se não houver nenhum achado, o resultado será SEM_IMPEDIMENTO.
   26 | 
   27 | # mensagem_do_resultado()
   28 | # -----------------------
   29 | # Converte o resultado interno em uma mensagem segura para o usuário.
   30 | # A mensagem deixa claro que o sistema não libera definitivamente a doação.
   31 | 
   32 | # calcular_resultado()
   33 | # --------------------
   34 | # Executa as regras da triagem extensa:
   35 | 
   36 | # - EXT-01: se a pessoa não entender que a triagem é orientativa, exige avaliação.
   37 | # - EXT-02: menores de 16 anos e pessoas com 70 anos ou mais exigem avaliação. Pessoas de 16 ou 17 anos precisam de documentação específica.
   38 | # - EXT-03: peso abaixo de 50 kg gera condição temporária. Peso igual ou acima de 130 kg, ou não informado com certeza, exige confirmação e avaliação do Hemocentro.
   39 | # - EXT-05: histórico de doação desconhecido exige avaliação.
   40 | # - EXT-05A: quando a pessoa já doou, calcula o intervalo mínimo desde a última doação: 90 dias para sexo feminino e 60 dias para sexo masculino. Se o intervalo ainda não terminou, gera resultado temporário e calcula a data orientativa de liberação.
   41 | # - EXT-04: se o sexo necessário para calcular o intervalo não for informado de formaválida, o sistema não libera automaticamente e exige avaliação.
   42 | # - EXT-05B: verifica o limite orientativo de doações nos últimos 12 meses: 3 para sexo feminino e 4 para sexo masculino. Se a quantidade for desconhecida ou atingir o limite, pode gerar avaliação ou impedimento temporário.
   43 | 
   44 | # Depois de analisar todas as respostas:
   45 | # - escolhe o resultado mais restritivo;
   46 | # - procura todas as datas de liberação;
   47 | # - utiliza a data mais distante quando existem vários prazos;
   48 | # - retorna resultado, mensagem, data de liberação e todos os achados.
   49 | 
   50 | # preparar_respostas()
   51 | # --------------------
   52 | # Converte as respostas limpas do formulário para o formato salvo no banco.
   53 | # Para cada resposta, registra:
   54 | # - código da pergunta;
   55 | # - valor enviado;
   56 | # - texto apresentado ao usuário;
   57 | # - data relacionada, quando existir;
   58 | # - versão das regras;
   59 | # - referência da pergunta original.
   60 | # Campos opcionais vazios não geram registros.
   61 | # Datas são convertidas para o formato ISO no banco e exibidas no formato brasileiro para o usuário.
   62 | 
   63 | # FLUXO RESUMIDO
   64 | # --------------
   65 | # Formulário de triagem - Respostas limpas pelo formulário - calcular_resultado() - Todos os achados são registrados - O resultado mais restritivo é escolhido - Mensagem e data orientativa são retornadas - preparar_respostas() organiza os dados para o histórico
   66 | # A triagem não decide a liberação médica definitiva.
   67 | # A decisão final sempre pertence ao Hemocentro.
   68 | # =============================================================================
   69 | 
   70 | """
   71 | Regras iniciais da triagem extensa.
   72 | 
   73 | Estas regras são orientativas e não substituem a avaliação
   74 | clínica feita pelo hemocentro.
   75 | 
   76 | O arquivo triagem.py reúne as regras iniciais da triagem e calcula uma orientação preliminar com base nas respostas básicas do usuário.
   77 | """
   78 | 
   79 | from datetime import date, timedelta
   80 | 
   81 | from .models import Triagem
   82 | 
   83 | 
   84 | # Versão identificável das regras utilizadas.
   85 | TRIAGEM_RULE_VERSION = "HEMOMINAS_2026_08"
   86 | 
   87 | 
   88 | # Associação entre os campos do formulário e as perguntas do documento.
   89 | QUESTION_FIELDS = [
   90 |     (
   91 |         "entende_orientacao",
   92 |         "EXT-01",
   93 |         "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-01",
   94 |     ),
   95 |     (
   96 |         "idade",
   97 |         "EXT-02",
   98 |         "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-02",
   99 |     ),
  100 |     (
  101 |         "peso",
  102 |         "EXT-03",
  103 |         "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-03",
  104 |     ),
  105 |     (
  106 |         "sexo_biologico",
  107 |         "EXT-04",
  108 |         "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-04",
  109 |     ),
  110 |     (
  111 |         "ja_doou",
  112 |         "EXT-05",
  113 |         "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05",
  114 |     ),
  115 |     (
  116 |         "data_ultima_doacao",
  117 |         "EXT-05A",
  118 |         "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05A",
  119 |     ),
  120 |     (
  121 |         "doacoes_12_meses",
  122 |         "EXT-05B",
  123 |         "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05B",
  124 |     ),
  125 | ]
  126 | 
  127 | 
  128 | def adicionar_achado(
  129 |     achados,
  130 |     codigo,
  131 |     resultado,
  132 |     mensagem,
  133 |     data_liberacao=None,
  134 | ):
  135 |     """
  136 |     Adiciona um impedimento ou alerta sem apagar achados anteriores.
  137 |     """
  138 | 
  139 |     achado = {
  140 |         "codigo": codigo,
  141 |         "resultado": resultado,
  142 |         "mensagem": mensagem,
  143 |     }
  144 | 
  145 |     if data_liberacao:
  146 |         achado["data_liberacao"] = data_liberacao.isoformat()
  147 | 
  148 |     achados.append(achado)
  149 | 
  150 | 
  151 | def escolher_resultado(achados):
  152 |     """
  153 |     Escolhe o resultado mais restritivo entre todos os achados.
  154 | 
  155 |     A triagem não para no primeiro problema:
  156 |     todos os achados continuam registrados.
  157 |     """
  158 | 
  159 |     ordem = [
  160 |         Triagem.Resultado.DEFINITIVA,
  161 |         Triagem.Resultado.AVALIACAO,
  162 |         Triagem.Resultado.TEMPORARIA,
  163 |         Triagem.Resultado.DOCUMENTACAO,
  164 |     ]
  165 | 
  166 |     resultados = {
  167 |         achado["resultado"]
  168 |         for achado in achados
  169 |     }
  170 | 
  171 |     for resultado in ordem:
  172 |         if resultado in resultados:
  173 |             return resultado
  174 | 
  175 |     return Triagem.Resultado.SEM_IMPEDIMENTO
  176 | 
  177 | 
  178 | def mensagem_do_resultado(resultado):
  179 |     """
  180 |     Retorna a mensagem segura apresentada ao usuário.
  181 |     """
  182 | 
  183 |     mensagens = {
  184 |         Triagem.Resultado.SEM_IMPEDIMENTO: (
  185 |             "Com base no que você informou, não identificamos "
  186 |             "um impedimento nesta orientação. Isso não significa "
  187 |             "liberação para doar: a decisão final será tomada "
  188 |             "pela equipe do hemocentro."
  189 |         ),
  190 |         Triagem.Resultado.TEMPORARIA: (
  191 |             "Encontramos uma condição com prazo de espera. "
  192 |             "A data é apenas orientativa e só vale se não existir "
  193 |             "outro impedimento."
  194 |         ),
  195 |         Triagem.Resultado.DEFINITIVA: (
  196 |             "A condição informada foi classificada como impedimento "
  197 |             "pela regra consultada. Confirme a orientação com o "
  198 |             "hemocentro ou serviço oficial."
  199 |         ),
  200 |         Triagem.Resultado.AVALIACAO: (
  201 |             "Sua resposta depende de avaliação profissional, "
  202 |             "relatório, exame ou informação que o sistema não "
  203 |             "consegue confirmar com segurança."
  204 |         ),
  205 |         Triagem.Resultado.DOCUMENTACAO: (
  206 |             "Para continuar, será necessária documentação especial "
  207 |             "ou conferência presencial pelo hemocentro."
  208 |         ),
  209 |     }
  210 | 
  211 |     return mensagens[resultado]
  212 | 
  213 | 
  214 | def calcular_resultado(respostas, hoje=None):
  215 |     """
  216 |     Calcula o resultado inicial da triagem extensa.
  217 | 
  218 |     O parâmetro hoje existe para facilitar testes e garantir
  219 |     que o cálculo possa ser repetido com uma data conhecida.
  220 |     """
  221 | 
  222 |     hoje = hoje or date.today()
  223 |     achados = []
  224 | 
  225 |     # EXT-01: entendimento da finalidade da triagem.
  226 |     if respostas.get("entende_orientacao") != "SIM":
  227 |         adicionar_achado(
  228 |             achados,
  229 |             "EXT-01",
  230 |             Triagem.Resultado.AVALIACAO,
  231 |             (
  232 |                 "A triagem só pode continuar com o entendimento "
  233 |                 "de que ela é orientativa."
  234 |             ),
  235 |         )
  236 | 
  237 |     # EXT-02: idade.
  238 |     idade = respostas.get("idade")
  239 | 
  240 |     if idade == "MENOS_16":
  241 |         adicionar_achado(
  242 |             achados,
  243 |             "EXT-02",
  244 |             Triagem.Resultado.AVALIACAO,
  245 |             (
  246 |                 "A idade informada exige avaliação específica "
  247 |                 "do hemocentro."
  248 |             ),
  249 |         )
  250 | 
  251 |     elif idade == "16_17":
  252 |         adicionar_achado(
  253 |             achados,
  254 |             "EXT-06",
  255 |             Triagem.Resultado.DOCUMENTACAO,
  256 |             (
  257 |                 "Pessoas de 16 ou 17 anos precisam apresentar "
  258 |                 "autorização e documentação específica."
  259 |             ),
  260 |         )
  261 | 
  262 |     elif idade == "70_MAIS":
  263 |         adicionar_achado(
  264 |             achados,
  265 |             "EXT-02",
  266 |             Triagem.Resultado.AVALIACAO,
  267 |             (
  268 |                 "A idade informada não deve ser liberada pela "
  269 |                 "pré-triagem comum e exige avaliação do hemocentro."
  270 |             ),
  271 |         )
  272 | 
  273 |     # EXT-03: peso.
  274 |     peso = respostas.get("peso")
  275 | 
  276 |     if peso == "MENOS_50":
  277 |         adicionar_achado(
  278 |             achados,
  279 |             "EXT-03",
  280 |             Triagem.Resultado.TEMPORARIA,
  281 |             (
  282 |                 "O peso informado está abaixo do limite utilizado "
  283 |                 "nesta orientação."
  284 |             ),
  285 |         )
  286 | 
  287 |     elif peso in ("130_MAIS", "NAO_SEI"):
  288 |         adicionar_achado(
  289 |             achados,
  290 |             "EXT-03",
  291 |             Triagem.Resultado.AVALIACAO,
  292 |             (
  293 |                 "O peso informado precisa ser confirmado e avaliado "
  294 |                 "pela unidade de coleta."
  295 |             ),
  296 |         )
  297 | 
  298 |     # EXT-05: histórico de doação.
  299 |     ja_doou = respostas.get("ja_doou")
  300 | 
  301 |     if ja_doou == "NAO_LEMBRO":
  302 |         adicionar_achado(
  303 |             achados,
  304 |             "EXT-05",
  305 |             Triagem.Resultado.AVALIACAO,
  306 |             (
  307 |                 "Não foi possível confirmar o histórico da última "
  308 |                 "doação."
  309 |             ),
  310 |         )
  311 | 
  312 |     if ja_doou == "SIM":
  313 |         sexo = respostas.get("sexo_biologico")
  314 |         ultima_doacao = respostas.get("data_ultima_doacao")
  315 |         doacoes_12_meses = respostas.get("doacoes_12_meses")
  316 | 
  317 |         # Sexo desconhecido não deve gerar uma falsa liberação.
  318 |         if sexo not in ("FEMININO", "MASCULINO"):
  319 |             adicionar_achado(
  320 |                 achados,
  321 |                 "EXT-04",
  322 |                 Triagem.Resultado.AVALIACAO,
  323 |                 (
  324 |                     "Não foi possível aplicar com segurança a regra "
  325 |                     "do intervalo entre doações."
  326 |                 ),
  327 |             )
  328 | 
  329 |         # Calcula o intervalo mínimo desde a última doação.
  330 |         if ultima_doacao and sexo in ("FEMININO", "MASCULINO"):
  331 |             intervalo_dias = (
  332 |                 90
  333 |                 if sexo == "FEMININO"
  334 |                 else 60
  335 |             )
  336 | 
  337 |             data_intervalo = (
  338 |                 ultima_doacao
  339 |                 + timedelta(days=intervalo_dias)
  340 |             )
  341 | 
  342 |             if data_intervalo > hoje:
  343 |                 adicionar_achado(
  344 |                     achados,
  345 |                     "EXT-05A",
  346 |                     Triagem.Resultado.TEMPORARIA,
  347 |                     (
  348 |                         "Ainda não terminou o intervalo orientativo "
  349 |                         "desde a última doação."
  350 |                     ),
  351 |                     data_liberacao=data_intervalo,
  352 |                 )
  353 | 
  354 |         # Verifica o limite orientativo de doações em 12 meses.
  355 |         if doacoes_12_meses == "NAO_LEMBRO":
  356 |             adicionar_achado(
  357 |                 achados,
  358 |                 "EXT-05B",
  359 |                 Triagem.Resultado.AVALIACAO,
  360 |                 (
  361 |                     "Não foi possível confirmar a quantidade de "
  362 |                     "doações nos últimos 12 meses."
  363 |                 ),
  364 |             )
  365 | 
  366 |         elif ultima_doacao:
  367 |             limite = (
  368 |                 3
  369 |                 if sexo == "FEMININO"
  370 |                 else 4
  371 |             )
  372 | 
  373 |             quantidade_excedida = (
  374 |                 doacoes_12_meses == "4_MAIS"
  375 |                 or (
  376 |                     doacoes_12_meses.isdigit()
  377 |                     and int(doacoes_12_meses) >= limite
  378 |                 )
  379 |             )
  380 | 
  381 |             if quantidade_excedida:
  382 |                 # Data orientativa e conservadora para completar
  383 |                 # uma janela aproximada de 12 meses.
  384 |                 data_janela = (
  385 |                     ultima_doacao
  386 |                     + timedelta(days=365)
  387 |                 )
  388 | 
  389 |                 if data_janela > hoje:
  390 |                     adicionar_achado(
  391 |                         achados,
  392 |                         "EXT-05B",
  393 |                         Triagem.Resultado.TEMPORARIA,
  394 |                         (
  395 |                             "A quantidade informada atingiu o limite "
  396 |                             "orientativo de doações em 12 meses."
  397 |                         ),
  398 |                         data_liberacao=data_janela,
  399 |                     )
  400 | 
  401 |     # Escolhe o resultado final depois de analisar todos os achados.
  402 |     resultado = escolher_resultado(achados)
  403 | 
  404 |     # Usa a data mais distante quando existem vários prazos.
  405 |     datas_liberacao = []
  406 | 
  407 |     for achado in achados:
  408 |         data_texto = achado.get("data_liberacao")
  409 | 
  410 |         if data_texto:
  411 |             datas_liberacao.append(
  412 |                 date.fromisoformat(data_texto)
  413 |             )
  414 | 
  415 |     data_liberacao = (
  416 |         max(datas_liberacao)
  417 |         if datas_liberacao
  418 |         else None
  419 |     )
  420 | 
  421 |     return {
  422 |         "resultado": resultado,
  423 |         "mensagem": mensagem_do_resultado(resultado),
  424 |         "data_liberacao": data_liberacao,
  425 |         "achados": achados,
  426 |     }
  427 | 
  428 | 
  429 | def preparar_respostas(form):
  430 |     """
  431 |     Converte as respostas do formulário para os registros do banco.
  432 |     """
  433 | 
  434 |     respostas = []
  435 | 
  436 |     for campo, id_pergunta, source_ref in QUESTION_FIELDS:
  437 |         valor = form.cleaned_data.get(campo)
  438 | 
  439 |         # Não cria registro para campos opcionais vazios.
  440 |         if valor in (None, ""):
  441 |             continue
  442 | 
  443 |         if isinstance(valor, date):
  444 |             codigo_resposta = valor.isoformat()
  445 |             resposta_label = valor.strftime("%d/%m/%Y")
  446 |             data_evento = valor
  447 |         else:
  448 |             codigo_resposta = str(valor)
  449 |             opcoes = dict(form.fields[campo].choices)
  450 |             resposta_label = opcoes.get(
  451 |                 valor,
  452 |                 str(valor),
  453 |             )
  454 |             data_evento = None
  455 | 
  456 |         respostas.append(
  457 |             {
  458 |                 "id_pergunta": id_pergunta,
  459 |                 "codigo_resposta": codigo_resposta,
  460 |                 "resposta_label": resposta_label,
  461 |                 "data_evento": data_evento,
  462 |                 "metadata": {},
  463 |                 "rule_version": TRIAGEM_RULE_VERSION,
  464 |                 "source_ref": source_ref,
  465 |             }
  466 |         )
  467 | 
  468 |     return respostas
``````

## accounts/triagem_catalogo.py

Original: [accounts/triagem_catalogo.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo.py>).

``````text
    1 | """Acesso único aos catálogos extensa e simplificado da triagem."""
    2 | 
    3 | from .triagem_catalogo_extensa import PERGUNTAS_EXTENSAS, REGRA_VERSION
    4 | from .triagem_catalogo_simplificada import PERGUNTAS_SIMPLIFICADAS
    5 | 
    6 | 
    7 | def obter_catalogo(modalidade):
    8 |     """Retorna o catálogo adequado e rejeita modalidade desconhecida."""
    9 | 
   10 |     if modalidade == "EXTENSA":
   11 |         return PERGUNTAS_EXTENSAS
   12 |     if modalidade == "SIMPLIFICADA":
   13 |         return PERGUNTAS_SIMPLIFICADAS
   14 |     raise ValueError("Modalidade de triagem inválida.")
   15 | 
   16 | 
   17 | def obter_pergunta(id_pergunta):
   18 |     """Localiza uma pergunta pelo identificador estável."""
   19 | 
   20 |     pergunta = PERGUNTAS_EXTENSAS.get(id_pergunta)
   21 |     if pergunta is None:
   22 |         pergunta = PERGUNTAS_SIMPLIFICADAS.get(id_pergunta)
   23 |     if pergunta is None:
   24 |         raise KeyError(f"Pergunta inexistente: {id_pergunta}")
   25 |     return pergunta
   26 | 
   27 | 
   28 | def todas_as_perguntas():
   29 |     """Fornece todas as perguntas para validação e auditoria."""
   30 | 
   31 |     return [
   32 |         *PERGUNTAS_EXTENSAS.values(),
   33 |         *PERGUNTAS_SIMPLIFICADAS.values(),
   34 |     ]
   35 | 
   36 | 
   37 | def validar_catalogos():
   38 |     """Interrompe a inicialização de testes se o catálogo estiver incoerente."""
   39 | 
   40 |     for pergunta in todas_as_perguntas():
   41 |         if pergunta["id"] not in (
   42 |             PERGUNTAS_EXTENSAS | PERGUNTAS_SIMPLIFICADAS
   43 |         ):
   44 |             raise ValueError("O identificador interno não corresponde à chave.")
   45 | 
   46 |         codigos = [opcao["codigo"] for opcao in pergunta["opcoes"]]
   47 |         if len(codigos) != len(set(codigos)):
   48 |             raise ValueError(
   49 |                 f"Há alternativas duplicadas em {pergunta['id']}."
   50 |             )
   51 | 
   52 |         desconhecidos = set(pergunta["regras"]) - set(codigos)
   53 |         if desconhecidos:
   54 |             raise ValueError(
   55 |                 f"Há regras para alternativas inexistentes em {pergunta['id']}."
   56 |             )
   57 | 
   58 |         for destinos in pergunta["abrir_extensa"].values():
   59 |             for destino in destinos:
   60 |                 if destino not in PERGUNTAS_EXTENSAS:
   61 |                     raise ValueError(
   62 |                         f"Destino {destino} inexistente em {pergunta['id']}."
   63 |                     )
   64 | 
   65 |     return None
   66 | 
   67 | 
   68 | # Compatibilidade com o nome usado na primeira implementação.
   69 | TRIAGEM_RULE_VERSION = REGRA_VERSION
``````

## accounts/triagem_catalogo_extensa.py

Original: [accounts/triagem_catalogo_extensa.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_extensa.py>).

``````text
    1 | """Catálogo versionado da triagem extensa.
    2 | 
    3 | Cada código é estável e corresponde ao documento de especificação enviado para
    4 | o projeto. As regras ficam junto das alternativas para serem auditáveis e para
    5 | que o motor não dependa do texto mostrado na tela.
    6 | """
    7 | 
    8 | REGRA_VERSION = "HEMOMINAS_2026_08"
    9 | 
   10 | TEMPORARIA = "INAPTIDAO_TEMPORARIA"
   11 | DEFINITIVA = "INAPTIDAO_DEFINITIVA"
   12 | AVALIACAO = "AVALIACAO_PRESENCIAL"
   13 | DOCUMENTACAO = "DOCUMENTACAO_ESPECIAL"
   14 | 
   15 | 
   16 | def opcao(codigo, rotulo):
   17 |     """Cria uma alternativa com código próprio para persistência."""
   18 | 
   19 |     return {"codigo": codigo, "rotulo": rotulo}
   20 | 
   21 | 
   22 | def regra(resultado, mensagem, prazo=None, exige_relatorio=False):
   23 |     """Cria uma regra declarativa consumida pelo motor da triagem."""
   24 | 
   25 |     return {
   26 |         "resultado": resultado,
   27 |         "mensagem": mensagem,
   28 |         "prazo": prazo,
   29 |         "exige_relatorio": exige_relatorio,
   30 |     }
   31 | 
   32 | 
   33 | def pergunta(
   34 |     id_pergunta,
   35 |     titulo,
   36 |     texto,
   37 |     explicacao,
   38 |     opcoes,
   39 |     *,
   40 |     multipla=False,
   41 |     permite_data=False,
   42 |     exige_data_para=(),
   43 |     exige_detalhes_para=(),
   44 |     perguntar_seguranca=False,
   45 |     perguntar_inflamacao=False,
   46 |     mostrar_se=None,
   47 |     regras=None,
   48 |     fonte="Manual Elo; ref. [1]",
   49 | ):
   50 |     """Padroniza todos os campos esperados pelas demais camadas."""
   51 | 
   52 |     return {
   53 |         "id": id_pergunta,
   54 |         "titulo": titulo,
   55 |         "texto": texto,
   56 |         "explicacao": explicacao,
   57 |         "tipo": "escolha",
   58 |         "opcoes": [opcao(*item) for item in opcoes],
   59 |         "multipla": multipla,
   60 |         "permite_data": permite_data,
   61 |         "exige_data_para": list(exige_data_para),
   62 |         "exige_detalhes_para": list(exige_detalhes_para),
   63 |         "perguntar_seguranca": perguntar_seguranca,
   64 |         "perguntar_inflamacao": perguntar_inflamacao,
   65 |         "mostrar_se": mostrar_se,
   66 |         "abrir_extensa": {},
   67 |         "regras": regras or {},
   68 |         "fonte": fonte,
   69 |         "regra_version": REGRA_VERSION,
   70 |     }
   71 | 
   72 | 
   73 | def pergunta_tabela(
   74 |     id_pergunta,
   75 |     titulo,
   76 |     texto,
   77 |     explicacao,
   78 |     itens,
   79 |     *,
   80 |     permite_data=True,
   81 |     exige_detalhes_para=(),
   82 |     perguntar_seguranca=False,
   83 |     perguntar_inflamacao=False,
   84 |     fonte="Manual Elo; ref. [1]",
   85 | ):
   86 |     """Monta perguntas longas em que várias condições podem ser marcadas."""
   87 | 
   88 |     opcoes = []
   89 |     regras = {}
   90 |     exige_data = []
   91 | 
   92 |     for codigo, rotulo, resultado, mensagem, prazo in itens:
   93 |         opcoes.append((codigo, rotulo))
   94 |         if resultado:
   95 |             regras[codigo] = regra(resultado, mensagem, prazo)
   96 |         if prazo:
   97 |             exige_data.append(codigo)
   98 | 
   99 |     return pergunta(
  100 |         id_pergunta,
  101 |         titulo,
  102 |         texto,
  103 |         explicacao,
  104 |         opcoes,
  105 |         multipla=True,
  106 |         permite_data=permite_data,
  107 |         exige_data_para=exige_data,
  108 |         exige_detalhes_para=exige_detalhes_para,
  109 |         perguntar_seguranca=perguntar_seguranca,
  110 |         perguntar_inflamacao=perguntar_inflamacao,
  111 |         regras=regras,
  112 |         fonte=fonte,
  113 |     )
  114 | 
  115 | 
  116 | # Entrada, idade, peso e histórico de doação.
  117 | PERGUNTAS_EXTENSAS = {
  118 |     "EXT-01": pergunta(
  119 |         "EXT-01",
  120 |         "Consentimento e entendimento",
  121 |         "Você entende que esta pré-triagem é apenas uma orientação e que a decisão final será feita pela equipe do hemocentro?",
  122 |         "Antes das perguntas de saúde, é necessário compreender o limite desta ferramenta.",
  123 |         [
  124 |             ("SIM", "Sim, entendo e quero continuar."),
  125 |             ("NAO", "Não entendo / quero ler a explicação novamente."),
  126 |         ],
  127 |         regras={
  128 |             "NAO": regra(
  129 |                 AVALIACAO,
  130 |                 "Leia novamente a explicação; a triagem só prossegue após seu entendimento.",
  131 |             ),
  132 |         },
  133 |         fonte="Manual Elo, seções 1, 2 e 18; termo de triagem do projeto",
  134 |     ),
  135 |     "EXT-01A": pergunta(
  136 |         "EXT-01A",
  137 |         "Tipo sanguíneo",
  138 |         "Qual é o seu tipo sanguíneo?",
  139 |         (
  140 |             "Esta informação não altera o resultado da pré-triagem. "
  141 |             "Ela será usada para compatibilidade sanguínea e alertas internos "
  142 |             "quando algum estoque estiver baixo ou crítico."
  143 |         ),
  144 |         [
  145 |             ("O-", "O-"),
  146 |             ("O+", "O+"),
  147 |             ("A-", "A-"),
  148 |             ("A+", "A+"),
  149 |             ("B-", "B-"),
  150 |             ("B+", "B+"),
  151 |             ("AB-", "AB-"),
  152 |             ("AB+", "AB+"),
  153 |             ("NAO_SEI", "Não sei / prefiro informar depois."),
  154 |         ],
  155 |     ),
  156 |     "EXT-02": pergunta(
  157 |         "EXT-02",
  158 |         "Idade",
  159 |         "Qual é a sua idade hoje?",
  160 |         "A regra consultada usa a faixa de 16 a 69 anos e possui condições especiais.",
  161 |         [
  162 |             ("MENOS_16", "Menos de 16 anos."),
  163 |             ("16_17", "16 ou 17 anos."),
  164 |             ("18_60", "18 a 60 anos."),
  165 |             ("61_69", "61 a 69 anos."),
  166 |             ("70_MAIS", "70 anos ou mais."),
  167 |         ],
  168 |         regras={
  169 |             "MENOS_16": regra(AVALIACAO, "A idade informada exige avaliação específica do hemocentro."),
  170 |             "16_17": regra(DOCUMENTACAO, "Será necessária a documentação específica para doadores de 16 e 17 anos."),
  171 |             "70_MAIS": regra(AVALIACAO, "A regra consolidada em 28/08/2026 exige avaliação presencial para esta faixa etária."),
  172 |         },
  173 |         fonte="Manual Elo, seções 3, 4 e 19; refs. [1], [5], [10]-[12]",
  174 |     ),
  175 |     "EXT-03": pergunta(
  176 |         "EXT-03",
  177 |         "Peso",
  178 |         "Quanto você pesa aproximadamente?",
  179 |         "O peso informado é orientativo e será confirmado na unidade de coleta.",
  180 |         [
  181 |             ("MENOS_50", "Menos de 50 kg."),
  182 |             ("50_55_9", "50 a 55,9 kg."),
  183 |             ("56_129_9", "56 a 129,9 kg."),
  184 |             ("130_MAIS", "130 kg ou mais."),
  185 |             ("NAO_SEI", "Não sei meu peso atual."),
  186 |         ],
  187 |         regras={
  188 |             "MENOS_50": regra(TEMPORARIA, "A coleta convencional requer atingir pelo menos 50 kg; não há data automática."),
  189 |             "130_MAIS": regra(AVALIACAO, "Confirme com a unidade o limite estrutural da cadeira de coleta."),
  190 |             "NAO_SEI": regra(AVALIACAO, "O peso precisa ser confirmado antes de orientar o comparecimento."),
  191 |         },
  192 |         fonte="Manual Elo, seção 3; ref. [1]",
  193 |     ),
  194 |     "EXT-04": pergunta(
  195 |         "EXT-04",
  196 |         "Regra de intervalo por sexo",
  197 |         "Para calcular o intervalo de sangue total, qual opção corresponde ao seu sexo biológico informado para a triagem?",
  198 |         "A informação é sensível e usada somente nos limites de intervalo e hemoglobina.",
  199 |         [
  200 |             ("FEMININO", "Feminino."),
  201 |             ("MASCULINO", "Masculino."),
  202 |             ("OUTRA_SITUACAO", "Tenho uma situação diferente / não sei qual regra se aplica."),
  203 |             ("NAO_INFORMAR", "Prefiro não informar agora."),
  204 |         ],
  205 |         regras={
  206 |             "OUTRA_SITUACAO": regra(AVALIACAO, "O hemocentro deve definir presencialmente qual regra de intervalo se aplica."),
  207 |             "NAO_INFORMAR": regra(AVALIACAO, "Sem essa informação, os critérios dependentes dela serão confirmados presencialmente."),
  208 |         },
  209 |         fonte="Manual Elo, seções 3 e 5; refs. [1] e [5]",
  210 |     ),
  211 |     "EXT-05": pergunta(
  212 |         "EXT-05",
  213 |         "Doação anterior",
  214 |         "Você já doou sangue alguma vez?",
  215 |         "Quem já doou precisa informar o histórico recente para calcular os intervalos.",
  216 |         [
  217 |             ("NAO", "Nunca doei."),
  218 |             ("SIM", "Sim, já doei."),
  219 |             ("NAO_LEMBRO", "Não tenho certeza / não lembro."),
  220 |         ],
  221 |         regras={
  222 |             "NAO_LEMBRO": regra(AVALIACAO, "O histórico de doações precisa ser confirmado presencialmente."),
  223 |         },
  224 |         fonte="Manual Elo, seções 3 e 4; ref. [1]",
  225 |     ),
  226 |     "EXT-05A": pergunta(
  227 |         "EXT-05A",
  228 |         "Data da última doação",
  229 |         "Se você já doou, quando foi sua última doação de sangue total?",
  230 |         "A regra desta triagem é para sangue total; aférese possui critérios próprios.",
  231 |         [
  232 |             ("DATA", "Informarei a data."),
  233 |             ("NAO_LEMBRO", "Não lembro a data."),
  234 |             ("AFERESE", "Minha última doação foi por aférese / não foi sangue total."),
  235 |         ],
  236 |         permite_data=True,
  237 |         exige_data_para=("DATA",),
  238 |         mostrar_se={"EXT-05": ["SIM"]},
  239 |         regras={
  240 |             "NAO_LEMBRO": regra(AVALIACAO, "Sem a data não é seguro calcular o intervalo entre doações."),
  241 |             "AFERESE": regra(AVALIACAO, "A aférese exige um fluxo específico no hemocentro."),
  242 |         },
  243 |         fonte="Manual Elo, seções 3 e 4; ref. [1]",
  244 |     ),
  245 |     "EXT-05B": pergunta(
  246 |         "EXT-05B",
  247 |         "Quantidade de doações em 12 meses",
  248 |         "Quantas doações de sangue total você fez nos últimos 12 meses?",
  249 |         "Além do intervalo em dias, existe um limite em uma janela móvel de 12 meses.",
  250 |         [("0", "0."), ("1", "1."), ("2", "2."), ("3", "3."), ("4_MAIS", "4 ou mais."), ("NAO_LEMBRO", "Não lembro.")],
  251 |         mostrar_se={"EXT-05": ["SIM"]},
  252 |         regras={
  253 |             "NAO_LEMBRO": regra(AVALIACAO, "A quantidade e as datas das doações precisam ser confirmadas."),
  254 |         },
  255 |         fonte="Manual Elo, seção 3; refs. [1] e [5]",
  256 |     ),
  257 |     "EXT-06": pergunta(
  258 |         "EXT-06",
  259 |         "Documentação para 16 e 17 anos",
  260 |         "Se você tem 16 ou 17 anos, qual situação se aplica?",
  261 |         "A autorização e a documentação não substituem a avaliação clínica.",
  262 |         [
  263 |             ("ACOMPANHADO", "Estarei acompanhado(a) por responsável legal com documento."),
  264 |             ("AUTORIZACAO", "Levarei a autorização exigida e cópia do documento do responsável."),
  265 |             ("EMANCIPADO", "Sou emancipado(a) e tenho comprovação formal."),
  266 |             ("GUARDA_TUTELA", "Estou sob guarda/tutela e tenho os documentos correspondentes."),
  267 |             ("SEM_DOCUMENTOS", "Ainda não tenho a autorização/documentação necessária."),
  268 |         ],
  269 |         mostrar_se={"EXT-02": ["16_17"]},
  270 |         regras={
  271 |             codigo: regra(DOCUMENTACAO, mensagem)
  272 |             for codigo, mensagem in {
  273 |                 "ACOMPANHADO": "Leve o responsável e os documentos exigidos.",
  274 |                 "AUTORIZACAO": "Leve a autorização e a cópia do documento do responsável.",
  275 |                 "EMANCIPADO": "Leve a comprovação formal de emancipação.",
  276 |                 "GUARDA_TUTELA": "Leve os documentos de guarda ou tutela.",
  277 |                 "SEM_DOCUMENTOS": "Providencie a autorização e os documentos antes de comparecer.",
  278 |             }.items()
  279 |         },
  280 |         fonte="Manual Elo, seção 4.1; ref. [3]",
  281 |     ),
  282 |     "EXT-07": pergunta(
  283 |         "EXT-07",
  284 |         "Histórico para pessoas acima de 60 anos",
  285 |         "Se você tem de 61 a 69 anos, já havia doado sangue antes de completar 60 anos?",
  286 |         "A regra consultada também exige intervalo mínimo de seis meses nesta faixa.",
  287 |         [
  288 |             ("SIM_COMPROVA", "Sim, e consigo comprovar se necessário."),
  289 |             ("SIM_SEM_COMPROVANTE", "Sim, mas não tenho comprovante agora."),
  290 |             ("NAO", "Não, minha primeira doação seria depois dos 60."),
  291 |             ("NAO_SEI", "Não lembro / não sei."),
  292 |         ],
  293 |         mostrar_se={"EXT-02": ["61_69"]},
  294 |         regras={
  295 |             "SIM_SEM_COMPROVANTE": regra(DOCUMENTACAO, "Pode ser necessário comprovar a doação realizada antes dos 60 anos."),
  296 |             "NAO": regra(AVALIACAO, "A primeira doação após os 60 anos não deve ser liberada por esta pré-triagem."),
  297 |             "NAO_SEI": regra(AVALIACAO, "O histórico anterior aos 60 anos precisa ser confirmado."),
  298 |         },
  299 |         fonte="Manual Elo, seção 4.2; ref. [1]",
  300 |     ),
  301 |     "EXT-07A": pergunta(
  302 |         "EXT-07A",
  303 |         "Documento para comparecer à doação",
  304 |         "No dia da doação, você terá um documento oficial aceito e o seu CPF?",
  305 |         "A identificação oficial confirma quem está doando; documentos digitais precisam ser verificáveis.",
  306 |         [
  307 |             ("ORIGINAL", "Sim, tenho documento oficial original com foto e CPF."),
  308 |             ("DIGITAL", "Tenho documento digital oficial verificável e CPF."),
  309 |             ("DUVIDA", "Tenho documento, mas não sei se atende às exigências."),
  310 |             ("NAO_TENHO", "Não tenho no momento um documento aceito e/ou CPF disponível."),
  311 |         ],
  312 |         regras={
  313 |             "DIGITAL": regra(DOCUMENTACAO, "Confirme se a unidade aceita e consegue verificar o documento digital."),
  314 |             "DUVIDA": regra(DOCUMENTACAO, "Confirme a documentação com a unidade antes de se deslocar."),
  315 |             "NAO_TENHO": regra(DOCUMENTACAO, "Regularize o documento oficial e o CPF antes de comparecer."),
  316 |         },
  317 |         fonte="Manual Elo, seção 3; refs. [1] e [2]",
  318 |     ),
  319 | }
  320 | 
  321 | 
  322 | # Condições atuais e informações hematológicas.
  323 | PERGUNTAS_EXTENSAS.update({
  324 |     "EXT-08": pergunta(
  325 |         "EXT-08", "Estado geral", "Hoje você está se sentindo bem, sem mal-estar importante?",
  326 |         "A doação deve ocorrer quando a pessoa está em boas condições gerais.",
  327 |         [("SIM", "Sim, estou bem."), ("NAO", "Não, estou doente, indisposto(a) ou com algum sintoma."), ("NAO_SEI", "Não tenho certeza.")],
  328 |         regras={
  329 |             "NAO": regra(AVALIACAO, "Os sintomas atuais precisam ser esclarecidos nas próximas perguntas."),
  330 |             "NAO_SEI": regra(AVALIACAO, "O estado de saúde atual precisa ser confirmado presencialmente."),
  331 |         },
  332 |         fonte="Manual Elo, seções 3 e 6; ref. [1]",
  333 |     ),
  334 |     "EXT-09": pergunta(
  335 |         "EXT-09", "Sono e descanso", "Quantas horas você dormiu no último período de sono antes da doação?",
  336 |         "A regra consolidada usa pelo menos quatro horas e considera também se você está descansado(a).",
  337 |         [("MENOS_4H", "Menos de 4 horas."), ("DESCANSADO", "4 horas ou mais e estou descansado(a)."), ("TRABALHO_NOTURNO", "Trabalho à noite e vou doar depois do descanso diurno."), ("NAO_DESCANSADO", "Não sei / não me sinto descansado(a).")],
  338 |         regras={
  339 |             "MENOS_4H": regra(TEMPORARIA, "Adie até ter um período adequado de repouso."),
  340 |             "NAO_DESCANSADO": regra(TEMPORARIA, "Adie até estar descansado(a)."),
  341 |         },
  342 |         fonte="Manual Elo, seções 3 e 19.1; ref. [1]",
  343 |     ),
  344 |     "EXT-10": pergunta(
  345 |         "EXT-10", "Alimentação", "Qual opção descreve melhor sua alimentação antes da doação?",
  346 |         "Não é recomendado doar em jejum; refeições gordurosas exigem intervalo.",
  347 |         [("JEJUM", "Estou em jejum."), ("LEVE", "Fiz refeição leve há tempo suficiente."), ("GORDUROSA_3H", "Comi refeição gordurosa há menos de 3 horas."), ("COPIOSA_4H", "Comi refeição muito gordurosa/copiosa há menos de 4 horas."), ("EXTREMAMENTE_GORDUROSA", "Comi algo extremamente gorduroso e não sei se devo doar hoje.")],
  348 |         regras={
  349 |             "JEJUM": regra(TEMPORARIA, "Alimente-se adequadamente e aguarde estar bem antes da doação."),
  350 |             "GORDUROSA_3H": regra(TEMPORARIA, "Aguarde completar três horas após a refeição gordurosa.", {"valor": 3, "unidade": "horas", "referencia": "hoje"}),
  351 |             "COPIOSA_4H": regra(TEMPORARIA, "Aguarde completar quatro horas após a refeição copiosa.", {"valor": 4, "unidade": "horas", "referencia": "hoje"}),
  352 |             "EXTREMAMENTE_GORDUROSA": regra(TEMPORARIA, "Adie para outro momento ou dia conforme orientação do hemocentro."),
  353 |         },
  354 |         fonte="Manual Elo, seção 3; ref. [1]",
  355 |     ),
  356 |     "EXT-11": pergunta(
  357 |         "EXT-11", "Hidratação", "Hoje você está bem hidratado(a), sem sede intensa, tontura por falta de líquidos ou vômitos/diarreia recentes?",
  358 |         "A hidratação reduz o risco de mal-estar durante e depois da coleta.",
  359 |         [("SIM", "Sim."), ("NAO", "Não / estou desidratado(a)."), ("NAO_SEI", "Não sei.")],
  360 |         regras={
  361 |             "NAO": regra(TEMPORARIA, "Aguarde a hidratação e a resolução da causa."),
  362 |             "NAO_SEI": regra(AVALIACAO, "Sintomas de desidratação precisam ser esclarecidos."),
  363 |         },
  364 |         fonte="Manual Elo, seções 3, 6 e 15; ref. [1]",
  365 |     ),
  366 |     "EXT-11A": pergunta(
  367 |         "EXT-11A", "Sinais vitais que você já conhece", "Se você mediu recentemente temperatura, pulso ou pressão, alguma destas situações aconteceu?",
  368 |         "Não é necessário medir em casa; os valores oficiais serão aferidos no hemocentro.",
  369 |         [("NAO_MEDI", "Não medi / não sei os valores."), ("NORMAIS", "Medi e estavam dentro do meu padrão, sem sintomas."), ("TEMPERATURA_ALTA", "Minha temperatura estava acima de 37 °C."), ("PULSO_ALTERADO", "Meu pulso estava abaixo de 50, acima de 100 ou parecia irregular."), ("PRESSAO_ALTERADA", "Minha pressão estava muito alta, muito baixa ou tive mal-estar."), ("NAO_SEI_INTERPRETAR", "Tenho um valor alterado, mas não sei interpretá-lo.")],
  370 |         regras={
  371 |             "TEMPERATURA_ALTA": regra(AVALIACAO, "A febre precisa ser esclarecida antes da doação."),
  372 |             "PULSO_ALTERADO": regra(AVALIACAO, "O pulso deverá ser avaliado presencialmente."),
  373 |             "PRESSAO_ALTERADA": regra(AVALIACAO, "A pressão e o mal-estar deverão ser avaliados presencialmente."),
  374 |             "NAO_SEI_INTERPRETAR": regra(AVALIACAO, "Leve o valor informado para avaliação presencial."),
  375 |         },
  376 |         fonte="Manual Elo, seção 3; refs. [1] e [5]",
  377 |     ),
  378 |     "EXT-12": pergunta(
  379 |         "EXT-12", "Febre", "Você teve febre recentemente ou está com temperatura alta agora?",
  380 |         "Febre pode indicar infecção; a causa conhecida também deve ser informada.",
  381 |         [("NAO", "Não tive febre recentemente."), ("ISOLADA", "Tive febre isolada sem causa definida."), ("PERSISTENTE", "Tenho/tive febre persistente ou recorrente sem causa definida."), ("CAUSA_CONHECIDA", "Minha febre tinha um diagnóstico conhecido."), ("NAO_SEI", "Não sei.")],
  382 |         permite_data=True,
  383 |         exige_data_para=("ISOLADA", "CAUSA_CONHECIDA"),
  384 |         regras={
  385 |             "ISOLADA": regra(TEMPORARIA, "Aguarde dez dias após o último dia de febre/recuperação.", {"valor": 10, "unidade": "dias", "referencia": "evento"}),
  386 |             "PERSISTENTE": regra(AVALIACAO, "Febre persistente ou recorrente exige diagnóstico e avaliação presencial."),
  387 |             "CAUSA_CONHECIDA": regra(AVALIACAO, "A regra específica da doença deve ser aplicada junto ao prazo da febre."),
  388 |             "NAO_SEI": regra(AVALIACAO, "A presença e a causa da febre serão confirmadas no hemocentro."),
  389 |         },
  390 |         fonte="Manual Elo, seção 6.1; ref. [1]",
  391 |     ),
  392 |     "EXT-13": pergunta(
  393 |         "EXT-13", "Sintomas respiratórios, COVID-19 e influenza", "Nos últimos dias, você teve tosse, coriza, dor de garganta, sintomas de gripe, COVID-19 ou influenza?",
  394 |         "Marque todas as situações aplicáveis; será usado o maior prazo.",
  395 |         [("NAO", "Não."), ("SINTOMAS_SEM_TESTE", "Tive sintomas respiratórios e não fiz teste."), ("TESTE_NEGATIVO_5D", "Tive sintomas e teste negativo no 5º dia."), ("COVID_SINTOMATICO", "Tive COVID-19 com sintomas."), ("COVID_ASSINTOMATICO", "Tive teste positivo para COVID-19, sem sintomas."), ("INFLUENZA", "Tive influenza confirmada ou quadro compatível."), ("CONTATO_COVID", "Tive contato próximo com pessoa com COVID-19."), ("CONTATO_INFLUENZA", "Tive contato com caso suspeito/confirmado de influenza.")],
  396 |         multipla=True,
  397 |         permite_data=True,
  398 |         exige_data_para=("SINTOMAS_SEM_TESTE", "TESTE_NEGATIVO_5D", "COVID_SINTOMATICO", "COVID_ASSINTOMATICO", "INFLUENZA", "CONTATO_COVID", "CONTATO_INFLUENZA"),
  399 |         regras={
  400 |             "SINTOMAS_SEM_TESTE": regra(TEMPORARIA, "Aguarde 15 dias após o desaparecimento dos sintomas.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  401 |             "TESTE_NEGATIVO_5D": regra(TEMPORARIA, "Aguarde 24 horas sem sintomas e sem antitérmico.", {"valor": 24, "unidade": "horas", "referencia": "evento"}),
  402 |             "COVID_SINTOMATICO": regra(TEMPORARIA, "Aguarde dez dias após melhora completa.", {"valor": 10, "unidade": "dias", "referencia": "evento"}),
  403 |             "COVID_ASSINTOMATICO": regra(TEMPORARIA, "Aguarde dez dias após a coleta do exame positivo.", {"valor": 10, "unidade": "dias", "referencia": "evento"}),
  404 |             "INFLUENZA": regra(TEMPORARIA, "Aguarde 15 dias após desaparecimento dos sintomas.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  405 |             "CONTATO_COVID": regra(TEMPORARIA, "Aguarde sete dias após o último contato.", {"valor": 7, "unidade": "dias", "referencia": "evento"}),
  406 |             "CONTATO_INFLUENZA": regra(TEMPORARIA, "Aguarde 15 dias após o último contato.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  407 |         },
  408 |         fonte="Manual Elo, seção 6.1; ref. [1]",
  409 |     ),
  410 |     "EXT-14": pergunta(
  411 |         "EXT-14", "Diarreia", "Você teve diarreia recentemente?", "O prazo depende da causa e do tratamento.",
  412 |         [("NAO", "Não."), ("COMUM", "Sim, quadro curto e não usei antibiótico."), ("VIRAL", "Sim, a causa parecia/foi confirmada como viral."), ("BACTERIANA", "Sim, a causa parecia/foi confirmada como bacteriana."), ("PERSISTENTE", "Sim, é persistente/crônica ou não sei a causa.")],
  413 |         permite_data=True,
  414 |         exige_data_para=("COMUM", "VIRAL", "BACTERIANA"),
  415 |         regras={
  416 |             "COMUM": regra(TEMPORARIA, "Aguarde dez dias após a cura.", {"valor": 10, "unidade": "dias", "referencia": "evento"}),
  417 |             "VIRAL": regra(TEMPORARIA, "Aguarde sete dias após a cura.", {"valor": 7, "unidade": "dias", "referencia": "evento"}),
  418 |             "BACTERIANA": regra(TEMPORARIA, "Aguarde 15 dias após a cura.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  419 |             "PERSISTENTE": regra(AVALIACAO, "Diarreia persistente ou de causa desconhecida exige avaliação."),
  420 |         },
  421 |         fonte="Manual Elo, seções 6.1 e 10.2; ref. [1]",
  422 |     ),
  423 |     "EXT-15": pergunta(
  424 |         "EXT-15", "Alergias", "Você está com alergia ativa ou já teve uma reação alérgica grave?",
  425 |         "Anafilaxia pode causar falta de ar, queda de pressão ou necessidade de atendimento urgente.",
  426 |         [("NAO", "Não."), ("ATIVA", "Estou com alergia leve/moderada ativa ou em tratamento."), ("RINITE_SEM_TESTE", "Tenho rinite/sintomas sem teste que diferencie alergia de infecção."), ("DESSENSIBILIZACAO", "Faço dessensibilização por aplicações."), ("ANAFILAXIA", "Já tive anafilaxia."), ("OXIDO_ETILENO", "Tenho alergia conhecida ao óxido de etileno.")],
  427 |         permite_data=True,
  428 |         exige_data_para=("RINITE_SEM_TESTE", "DESSENSIBILIZACAO"),
  429 |         regras={
  430 |             "ATIVA": regra(TEMPORARIA, "Aguarde a resolução e o fim do tratamento."),
  431 |             "RINITE_SEM_TESTE": regra(TEMPORARIA, "Aguarde dez dias após a resolução.", {"valor": 10, "unidade": "dias", "referencia": "evento"}),
  432 |             "DESSENSIBILIZACAO": regra(TEMPORARIA, "Aguarde 72 horas após cada aplicação.", {"valor": 72, "unidade": "horas", "referencia": "evento"}),
  433 |             "ANAFILAXIA": regra(DEFINITIVA, "A anafilaxia prévia é impedimento definitivo na regra consultada."),
  434 |             "OXIDO_ETILENO": regra(DEFINITIVA, "A alergia ao óxido de etileno é impedimento definitivo na regra consultada."),
  435 |         },
  436 |         fonte="Manual Elo, seção 6.2; ref. [1]",
  437 |     ),
  438 |     "EXT-16": pergunta(
  439 |         "EXT-16", "Ferimentos e pontos", "Você tem ferida aberta, corte ainda não cicatrizado ou pontos?",
  440 |         "A pele deve estar íntegra para reduzir risco de infecção e permitir punção segura.",
  441 |         [("NAO", "Não."), ("ABERTO", "Tenho ferimento aberto."), ("PONTOS", "Tenho ferimento com pontos/sutura."), ("CICATRIZADO", "Já está completamente cicatrizado e sem complicações.")],
  442 |         regras={
  443 |             "ABERTO": regra(TEMPORARIA, "Aguarde a cicatrização completa e a ausência de complicações."),
  444 |             "PONTOS": regra(TEMPORARIA, "Aguarde a retirada dos pontos, cicatrização e ausência de complicações."),
  445 |         },
  446 |         fonte="Manual Elo, seção 6.3; ref. [1]",
  447 |     ),
  448 |     "EXT-17": pergunta(
  449 |         "EXT-17", "Atividade esportiva ou trabalho de risco", "Você fará atividade que pode ser perigosa se tiver tontura depois de doar?",
  450 |         "Algumas atividades exigem planejamento para a segurança do doador após a coleta.",
  451 |         [("NAO", "Não."), ("COMPETICAO", "Tenho competição esportiva importante nas próximas 24 horas."), ("ESPORTE_RISCO", "Faço mergulho, escalada, rapel, paraquedismo, automobilismo ou atividade semelhante."), ("TRABALHO_RISCO", "Piloto, dirijo veículo pesado, opero máquinas perigosas ou trabalho em altura."), ("LOCOMOCAO", "Uso equipamento de locomoção e posso precisar fazer esforço importante depois da coleta.")],
  452 |         regras={
  453 |             "COMPETICAO": regra(TEMPORARIA, "Não doe nas 24 horas anteriores à competição."),
  454 |             "ESPORTE_RISCO": regra(DOCUMENTACAO, "Planeje pelo menos 12 horas sem essa atividade depois da doação."),
  455 |             "TRABALHO_RISCO": regra(DOCUMENTACAO, "Planeje pelo menos 12 horas sem a atividade de risco depois da doação."),
  456 |             "LOCOMOCAO": regra(AVALIACAO, "A unidade deve avaliar segurança e eventual necessidade de acompanhante."),
  457 |         },
  458 |         fonte="Manual Elo, seção 6.3; ref. [1]",
  459 |     ),
  460 |     "EXT-18": pergunta(
  461 |         "EXT-18", "Perda rápida de peso", "Você perdeu mais de 10% do seu peso em pouco tempo?",
  462 |         "Perda importante de peso pode exigir estabilização ou investigação.",
  463 |         [("NAO", "Não."), ("CAUSA_CONHECIDA", "Sim, a causa é conhecida e meu peso já está estável."), ("INEXPLICADA", "Sim, não sei por que emagreci."), ("NAO_SEI", "Não sei se a perda chegou a 10%.")],
  464 |         permite_data=True,
  465 |         exige_data_para=("CAUSA_CONHECIDA",),
  466 |         regras={
  467 |             "CAUSA_CONHECIDA": regra(TEMPORARIA, "Aguarde três meses após a estabilização do peso.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
  468 |             "INEXPLICADA": regra(AVALIACAO, "A perda de peso sem explicação precisa ser investigada."),
  469 |             "NAO_SEI": regra(AVALIACAO, "Informe pesos anterior e atual ou confirme presencialmente."),
  470 |         },
  471 |         fonte="Manual Elo, seção 3; ref. [1]",
  472 |     ),
  473 |     "EXT-19": pergunta(
  474 |         "EXT-19", "Hemoglobina ou hematócrito conhecidos", "Alguma vez você foi impedido(a) de doar porque a hemoglobina/hematócrito estava baixa ou muito alta?",
  475 |         "Esses valores serão medidos novamente no hemocentro.",
  476 |         [("NAO", "Não."), ("BAIXA_FERRO_NORMAL", "Estava baixa e depois fiz exame mostrando ferro normal."), ("BAIXA_FERRO_BAIXO", "Estava baixa e o ferro estava baixo."), ("BAIXA_SEM_INVESTIGAR", "Estava baixa e não investiguei."), ("MUITO_ALTA", "Estava muito alta, como Hb ≥18 g/dL ou Ht ≥54%."), ("NAO_SEI", "Não sei / não lembro.")],
  477 |         permite_data=True,
  478 |         exige_data_para=("BAIXA_FERRO_NORMAL", "BAIXA_FERRO_BAIXO", "BAIXA_SEM_INVESTIGAR"),
  479 |         regras={
  480 |             "BAIXA_FERRO_NORMAL": regra(TEMPORARIA, "Aguarde 30 dias após a normalização indicada.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  481 |             "BAIXA_FERRO_BAIXO": regra(TEMPORARIA, "Aguarde seis meses após normalização e tratamento.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  482 |             "BAIXA_SEM_INVESTIGAR": regra(TEMPORARIA, "Aguarde seis meses e realize a investigação indicada.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  483 |             "MUITO_ALTA": regra(AVALIACAO, "Hemoglobina ou hematócrito muito altos exigem investigação."),
  484 |         },
  485 |         fonte="Manual Elo, seção 5; refs. [1] e [5]",
  486 |     ),
  487 |     "EXT-20": pergunta_tabela(
  488 |         "EXT-20", "Doenças hematológicas", "Você já recebeu algum destes diagnósticos relacionados ao sangue, medula ou coagulação?",
  489 |         "Marque somente diagnósticos informados por profissional de saúde.",
  490 |         [
  491 |             ("ANEMIA_CARENCIAL", "Anemia carencial.", TEMPORARIA, "Aguarde seis meses após exames normais e fim do tratamento.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  492 |             ("ANEMIA_HEREDITARIA", "Anemia hereditária.", DEFINITIVA, "A anemia hereditária é impedimento definitivo na regra consultada.", None),
  493 |             ("TRACO_FALCIFORME", "Traço falciforme.", None, "", None),
  494 |             ("AGRANULOCITOSE", "Agranulocitose medicamentosa.", TEMPORARIA, "Aguarde seis meses após recuperação.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  495 |             ("APLASIA_MEDULA", "Aplasia de medula.", DEFINITIVA, "A aplasia de medula é impedimento definitivo.", None),
  496 |             ("CID", "Coagulação intravascular disseminada (CID).", DEFINITIVA, "CID é impedimento definitivo.", None),
  497 |             ("COAGULOPATIA", "Coagulopatia.", DEFINITIVA, "Coagulopatia é impedimento definitivo.", None),
  498 |             ("ESPLENOMEGALIA", "Esplenomegalia idiopática.", DEFINITIVA, "Esplenomegalia idiopática é impedimento definitivo.", None),
  499 |             ("HEMOCROMATOSE", "Hemocromatose.", DEFINITIVA, "Hemocromatose é impedimento definitivo.", None),
  500 |             ("HEMOGLOBINA_VARIANTE", "Hemoglobina variante.", AVALIACAO, "É necessário confirmar quantas variantes existem.", None),
  501 |             ("HIPERFERRITINEMIA", "Hiperferritinemia.", AVALIACAO, "É necessário excluir hemocromatose ou lesão de órgão-alvo.", None),
  502 |             ("HISTIOCITOSE", "Histiocitose.", DEFINITIVA, "Histiocitose é impedimento definitivo.", None),
  503 |             ("LEUCEMIA", "Leucemia.", DEFINITIVA, "Leucemia é impedimento definitivo.", None),
  504 |             ("LEUCOPENIA", "Leucopenia.", AVALIACAO, "Leucopenia exige avaliação e relatório.", None),
  505 |             ("LINFOMA", "Linfoma.", DEFINITIVA, "Linfoma é impedimento definitivo.", None),
  506 |             ("MIELOMA", "Mieloma.", DEFINITIVA, "Mieloma é impedimento definitivo.", None),
  507 |             ("NEUTROPENIA_CRONICA", "Neutropenia crônica.", DEFINITIVA, "Neutropenia crônica é impedimento definitivo.", None),
  508 |             ("POLICITEMIA_PRIMARIA", "Policitemia / poliglobulia primária.", DEFINITIVA, "Policitemia primária é impedimento definitivo.", None),
  509 |             ("POLIGLOBULIA_SECUNDARIA", "Poliglobulia secundária.", AVALIACAO, "A causa e os valores precisam ser avaliados.", None),
  510 |             ("PORFIRIA", "Porfiria.", DEFINITIVA, "Porfiria é impedimento definitivo.", None),
  511 |             ("PTI_INFANCIA", "PTI ocorrida na infância, sem sequela.", None, "", None),
  512 |             ("PTI_ADULTO", "PTI ocorrida na vida adulta.", DEFINITIVA, "PTI em adulto é impedimento definitivo.", None),
  513 |             ("NENHUMA", "Nenhuma das anteriores.", None, "", None),
  514 |             ("OUTRA", "Outra doença do sangue / não sei o nome.", AVALIACAO, "Condição não listada ou incerta exige avaliação.", None),
  515 |         ],
  516 |         fonte="Manual Elo, seção 5; ref. [1]",
  517 |     ),
  518 | })
  519 | 
  520 | 
  521 | # Medicamentos, vacinas, viagens e confirmação final.
  522 | PERGUNTAS_EXTENSAS.update({
  523 |     "EXT-46": pergunta_tabela(
  524 |         "EXT-46", "Medicamentos comuns e especiais", "Você usa ou usou recentemente algum destes medicamentos?",
  525 |         "Nunca suspenda medicamento para doar; informe também o motivo do tratamento.",
  526 |         [
  527 |             ("ANALGESICO", "Analgésico comum.", AVALIACAO, "O medicamento em si geralmente não impede; a causa da dor precisa ser avaliada.", None),
  528 |             ("ANTITERMICO", "Antitérmico.", AVALIACAO, "A febre ou doença determina o prazo.", None),
  529 |             ("AAS_PIROXICAM", "AAS/aspirina ou piroxicam.", TEMPORARIA, "Aguarde 48 horas; doação de plaquetas pode ter regra própria.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  530 |             ("AINE", "Outro anti-inflamatório (AINE).", AVALIACAO, "Sangue total e plaquetas possuem regras diferentes; plaquetas podem exigir cinco dias.", None),
  531 |             ("ANOREXIGENO", "Anorexígeno anfetamínico.", AVALIACAO, "Aguarde sete dias após suspensão prescrita e avalie perda de peso.", None),
  532 |             ("ANTIPARASITARIO", "Antiparasitário comum.", AVALIACAO, "A doença tratada precisa ser considerada.", None),
  533 |             ("ANTIBIOTICO", "Antibiótico.", TEMPORARIA, "Aguarde ao menos 14 dias após o fim; prevalece o prazo maior da infecção.", {"valor": 14, "unidade": "dias", "referencia": "evento"}),
  534 |             ("CORTICOIDE_SISTEMICO", "Corticoide sistêmico.", AVALIACAO, "Aguarde pelo menos 48 horas após suspensão médica e avalie a doença.", None),
  535 |             ("CORTICOIDE_TOPICO", "Corticoide tópico.", AVALIACAO, "A doença de pele precisa ser avaliada.", None),
  536 |             ("ANTICOAGULANTE", "Anticoagulante.", AVALIACAO, "Somente após interrupção médica, aguarde 10 a 14 dias e avalie a doença de base.", None),
  537 |             ("CLOPIDOGREL", "Clopidogrel.", AVALIACAO, "Somente após suspensão médica, aguarde 14 dias.", None),
  538 |             ("PRASUGREL", "Prasugrel.", AVALIACAO, "Somente após suspensão médica, aguarde sete dias.", None),
  539 |             ("TICLOPIDINA", "Ticlopidina.", AVALIACAO, "Somente após suspensão médica, aguarde 14 dias.", None),
  540 |             ("ANTICONCEPCIONAL", "Anticoncepcional / hormônio feminino.", None, "", None),
  541 |             ("INDUCAO_OVULACAO", "Indução de ovulação.", TEMPORARIA, "Aguarde três meses após o fim e confirme ausência de gravidez.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
  542 |             ("GLP1", "GLP-1: semaglutida, tirzepatida, liraglutida e similares.", AVALIACAO, "Sintomas, mudança de dose e segurança da aplicação precisam ser avaliados.", None),
  543 |             ("ANTI_HIPERTENSIVO", "Anti-hipertensivo compatível.", AVALIACAO, "Pressão, lesão de órgão-alvo e tipo de doação precisam ser avaliados.", None),
  544 |             ("ANTI_HIPERTENSIVO_CENTRAL", "Anti-hipertensivo de ação central.", AVALIACAO, "Somente após suspensão médica, aguarde 48 horas e avalie caso a caso.", None),
  545 |             ("BETA_ALFA", "Betabloqueador, alfa-bloqueador ou vasodilatador.", AVALIACAO, "Somente após suspensão médica, aguarde cinco dias e avalie caso a caso.", None),
  546 |             ("HOMEOPATICO", "Homeopático/fitoterápico.", AVALIACAO, "Aguarde em geral 24 horas e avalie o motivo do uso.", None),
  547 |             ("CANABIDIOL", "Canabidiol.", AVALIACAO, "A doença de base precisa ser avaliada.", None),
  548 |             ("GH_RECOMBINANTE", "Hormônio de crescimento recombinante.", None, "", None),
  549 |             ("GH_HIPOFISARIO", "Hormônio de crescimento de origem hipofisária humana.", DEFINITIVA, "GH de origem hipofisária humana é impedimento definitivo.", None),
  550 |             ("PREP_PEP_ORAL", "PrEP/PEP oral.", TEMPORARIA, "Aguarde quatro meses após o uso; a exposição pode exigir prazo maior.", {"valor": 4, "unidade": "meses", "referencia": "evento"}),
  551 |             ("PREP_INJETAVEL", "PrEP injetável: cabotegravir/lenacapavir.", TEMPORARIA, "Aguarde dois anos após o uso.", {"valor": 2, "unidade": "anos", "referencia": "evento"}),
  552 |             ("TARV_HIV", "Tratamento antirretroviral para HIV.", DEFINITIVA, "O diagnóstico de HIV é impedimento definitivo.", None),
  553 |             ("IMUNOSSUPRESSOR", "Imunobiológico, anticorpo monoclonal ou imunossupressor.", AVALIACAO, "Muitos casos exigem seis meses após o fim e avaliação da doença de base.", None),
  554 |             ("NENHUM", "Nenhum medicamento relevante.", None, "", None),
  555 |             ("OUTRO", "Uso outro medicamento / não sei o nome.", AVALIACAO, "Não suspenda o medicamento; leve nome e receita para avaliação.", None),
  556 |         ],
  557 |         fonte="Manual Elo, seções 15.2 e atualização 2026; refs. [1], [4], [8], [9]",
  558 |     ),
  559 |     "EXT-47": pergunta_tabela(
  560 |         "EXT-47", "Medicamentos de eliminação prolongada", "Você usa ou já usou algum destes medicamentos?",
  561 |         "O prazo é contado da última dose válida; não interrompa tratamento para doar.",
  562 |         [
  563 |             ("ACITRETINA", "Acitretina.", TEMPORARIA, "Aguarde três anos após a última dose.", {"valor": 3, "unidade": "anos", "referencia": "evento"}),
  564 |             ("BARICITINIBE", "Baricitinibe.", AVALIACAO, "Aguarde seis meses e avalie a doença de base.", None),
  565 |             ("DANAZOL", "Danazol.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  566 |             ("DUTASTERIDA", "Dutasterida.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  567 |             ("ETRETINATO", "Etretinato.", DEFINITIVA, "Etretinato é impedimento definitivo independentemente do tempo.", None),
  568 |             ("FINASTERIDA", "Finasterida.", TEMPORARIA, "Aguarde um mês.", {"valor": 1, "unidade": "meses", "referencia": "evento"}),
  569 |             ("ISOTRETINOINA", "Isotretinoína.", TEMPORARIA, "Aguarde um mês após a última dose.", {"valor": 1, "unidade": "meses", "referencia": "evento"}),
  570 |             ("LEFLUNOMIDA", "Leflunomida.", TEMPORARIA, "Aguarde dois anos.", {"valor": 2, "unidade": "anos", "referencia": "evento"}),
  571 |             ("LENALIDOMIDA", "Lenalidomida.", TEMPORARIA, "Aguarde 30 dias.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  572 |             ("MICOFENOLATO", "Micofenolato de mofetila.", TEMPORARIA, "Aguarde seis semanas.", {"valor": 6, "unidade": "semanas", "referencia": "evento"}),
  573 |             ("SONIDEGIB", "Sonidegib.", TEMPORARIA, "Aguarde dois anos.", {"valor": 2, "unidade": "anos", "referencia": "evento"}),
  574 |             ("TACROLIMO_SISTEMICO", "Tacrolimo sistêmico/uso extenso por mais de três semanas.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  575 |             ("TACROLIMO_COLIRIO", "Tacrolimo em colírio.", AVALIACAO, "A doença ocular de base precisa ser avaliada.", None),
  576 |             ("TESTOSTERONA", "Testosterona/anabolizante prescrito.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  577 |             ("ANABOLIZANTE_INJETAVEL", "Anabolizante injetável sem prescrição.", TEMPORARIA, "Aguarde 12 meses.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  578 |             ("UPADACITINIBE", "Upadacitinibe.", TEMPORARIA, "Aguarde 30 dias.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  579 |             ("VISMODEGIB", "Vismodegib.", TEMPORARIA, "Aguarde dois anos.", {"valor": 2, "unidade": "anos", "referencia": "evento"}),
  580 |             ("NENHUM", "Nenhum.", None, "", None),
  581 |             ("OUTRO", "Não sei / outro semelhante.", AVALIACAO, "O medicamento precisa ser identificado presencialmente.", None),
  582 |         ],
  583 |         fonte="Manual Elo, seção 15.3; refs. [1] e [4]",
  584 |     ),
  585 |     "EXT-48": pergunta_tabela(
  586 |         "EXT-48", "Vacinação", "Você tomou alguma vacina recentemente?",
  587 |         "Marque todas as vacinas e informe a data de cada dose.",
  588 |         [
  589 |             ("RABICA_EXPOSICAO", "Antirrábica após exposição.", TEMPORARIA, "Aguarde um ano.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
  590 |             ("RABICA_PREVENTIVA", "Antirrábica preventiva.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  591 |             ("BCG", "BCG.", TEMPORARIA, "Aguarde quatro semanas.", {"valor": 4, "unidade": "semanas", "referencia": "evento"}),
  592 |             ("BRUCELOSE", "Brucelose.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  593 |             ("CAXUMBA", "Caxumba.", TEMPORARIA, "Aguarde quatro semanas.", {"valor": 4, "unidade": "semanas", "referencia": "evento"}),
  594 |             ("COLERA", "Cólera.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  595 |             ("COQUELUCHE", "Coqueluche.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  596 |             ("COVID_INATIVADA", "COVID-19 CoronaVac/Covaxin.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  597 |             ("COVID_OUTRAS", "COVID-19 AstraZeneca/Pfizer/Janssen/Sputnik/Moderna.", TEMPORARIA, "Aguarde sete dias.", {"valor": 7, "unidade": "dias", "referencia": "evento"}),
  598 |             ("DENGUE", "Dengue.", TEMPORARIA, "Aguarde 30 dias.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  599 |             ("DIFTERIA", "Difteria.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  600 |             ("FEBRE_AMARELA", "Febre amarela.", TEMPORARIA, "Aguarde quatro semanas.", {"valor": 4, "unidade": "semanas", "referencia": "evento"}),
  601 |             ("TIFOIDE_INJETAVEL", "Febre tifoide injetável.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  602 |             ("TIFOIDE_ORAL", "Febre tifoide oral.", TEMPORARIA, "Aguarde quatro semanas.", {"valor": 4, "unidade": "semanas", "referencia": "evento"}),
  603 |             ("INFLUENZA_ATENUADA", "Influenza atenuada.", TEMPORARIA, "Aguarde quatro semanas.", {"valor": 4, "unidade": "semanas", "referencia": "evento"}),
  604 |             ("INFLUENZA_INATIVADA", "Influenza inativada.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  605 |             ("H1N1_ATENUADA", "H1N1 atenuada.", TEMPORARIA, "Aguarde quatro semanas.", {"valor": 4, "unidade": "semanas", "referencia": "evento"}),
  606 |             ("H1N1_INATIVADA", "H1N1 inativada.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  607 |             ("HIB", "Haemophilus influenzae.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  608 |             ("HEPATITE_A", "Hepatite A.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  609 |             ("HEPATITE_B_PLASMA", "Hepatite B derivada de plasma.", TEMPORARIA, "Aguarde um ano.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
  610 |             ("HEPATITE_B_RECOMBINANTE", "Hepatite B recombinante.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  611 |             ("HPV", "HPV.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  612 |             ("MPOX", "Jynneos/Imvanex: mpox.", TEMPORARIA, "Aguarde quatro semanas.", {"valor": 4, "unidade": "semanas", "referencia": "evento"}),
  613 |             ("LEPTOSPIROSE", "Leptospirose.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  614 |             ("MENINGITE", "Meningite.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  615 |             ("PESTE", "Peste.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  616 |             ("PNEUMOCOCICA", "Pneumocócica.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  617 |             ("POLIO_SABIN", "Poliomielite Sabin.", TEMPORARIA, "Aguarde quatro semanas.", {"valor": 4, "unidade": "semanas", "referencia": "evento"}),
  618 |             ("POLIO_SALK", "Poliomielite Salk.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  619 |             ("ROTAVIRUS", "Rotavírus.", TEMPORARIA, "Aguarde quatro semanas.", {"valor": 4, "unidade": "semanas", "referencia": "evento"}),
  620 |             ("RUBEOLA", "Rubéola.", TEMPORARIA, "Aguarde quatro semanas.", {"valor": 4, "unidade": "semanas", "referencia": "evento"}),
  621 |             ("SARAMPO", "Sarampo.", TEMPORARIA, "Aguarde quatro semanas.", {"valor": 4, "unidade": "semanas", "referencia": "evento"}),
  622 |             ("TETANO", "Tétano.", TEMPORARIA, "Aguarde 48 horas.", {"valor": 48, "unidade": "horas", "referencia": "evento"}),
  623 |             ("VARICELA", "Varicela/zóster.", TEMPORARIA, "Aguarde quatro semanas.", {"valor": 4, "unidade": "semanas", "referencia": "evento"}),
  624 |             ("PLASMA_HUMANO", "Vacina derivada de plasma humano.", TEMPORARIA, "Aguarde um ano.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
  625 |             ("EXPERIMENTAL", "Vacina experimental.", TEMPORARIA, "Aguarde um ano após o fim do protocolo.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
  626 |             ("VARIOLA", "Vacina contra varíola.", AVALIACAO, "Crosta e complicações exigem regra específica presencial.", None),
  627 |             ("NENHUMA", "Nenhuma vacina recente.", None, "", None),
  628 |             ("NAO_SEI", "Tomei vacina, mas não sei qual.", AVALIACAO, "Verifique a carteira de vacinação ou confirme presencialmente.", None),
  629 |         ],
  630 |         fonte="Manual Elo, seção 16; ref. [1]",
  631 |     ),
  632 |     "EXT-49": pergunta_tabela(
  633 |         "EXT-49", "Viagens e residência", "Você morou ou viajou para algum dos locais ou situações abaixo?",
  634 |         "Informe destino e data de retorno; áreas de risco precisam de atualização frequente.",
  635 |         [
  636 |             ("REINO_UNIDO", "Reino Unido/Irlanda por mais de três meses entre 1980 e 1996.", DEFINITIVA, "Esta permanência histórica é impedimento definitivo.", None),
  637 |             ("EUROPA", "Europa por cinco anos ou mais desde 1980.", DEFINITIVA, "Esta permanência histórica é impedimento definitivo na regra atual.", None),
  638 |             ("CHIKUNGUNYA", "Retorno de área com transmissão sustentada de chikungunya.", TEMPORARIA, "Aguarde 30 dias após retorno.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  639 |             ("TRIATOMINEO", "Contato domiciliar com triatomíneo/barbeiro.", DEFINITIVA, "Contato domiciliar de risco para Chagas é impedimento definitivo na regra publicada.", None),
  640 |             ("MALARIA_RESIDIU", "Residia em área endêmica de malária.", TEMPORARIA, "Aguarde 30 dias após afastamento da área.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  641 |             ("MALARIA_VIAJOU", "Viajou para área endêmica de malária.", TEMPORARIA, "Aguarde 30 dias após retorno.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  642 |             ("MALARIA_SURTO", "Esteve em região com surto de malária.", AVALIACAO, "Consulte a autoridade sanitária e a avaliação presencial.", None),
  643 |             ("OESTE_NILO", "Retornou de área com vírus do Oeste do Nilo.", TEMPORARIA, "Aguarde 30 dias após retorno.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  644 |             ("NENHUMA", "Nenhuma.", None, "", None),
  645 |             ("NAO_SEI", "Viajei, mas não sei se era área de risco.", AVALIACAO, "Destino e alerta epidemiológico precisam ser verificados.", None),
  646 |         ],
  647 |         fonte="Manual Elo, seção 17; ref. [1]",
  648 |     ),
  649 |     "EXT-50": pergunta(
  650 |         "EXT-50", "Outra condição importante", "Existe doença, tratamento, internação, exame invasivo, transfusão, medicamento, exposição ou situação de saúde que não apareceu e que você acha importante informar?",
  651 |         "Esta pergunta evita falsa segurança quando algo não está nas listas públicas.",
  652 |         [("NAO", "Não."), ("SIM", "Sim, quero descrever."), ("NAO_SEI", "Não sei se algo que tive é relevante.")],
  653 |         exige_detalhes_para=("SIM",),
  654 |         regras={
  655 |             "SIM": regra(AVALIACAO, "A descrição precisa ser avaliada por profissional e regra validada."),
  656 |             "NAO_SEI": regra(AVALIACAO, "A situação incerta deve ser discutida presencialmente."),
  657 |         },
  658 |         fonte="Manual Elo, seções 1.2 e 20; ref. [1]",
  659 |     ),
  660 |     "EXT-51": pergunta(
  661 |         "EXT-51", "Confirmação final", "Você confirma que respondeu com o máximo de precisão possível e que qualquer mudança até o dia da doação será informada?",
  662 |         "Sua saúde pode mudar entre esta resposta e a chegada ao hemocentro.",
  663 |         [("CONFIRMAR", "Sim."), ("REVISAR", "Quero revisar minhas respostas.")],
  664 |         fonte="Manual Elo, seções 18.3 e 18.4",
  665 |     ),
  666 | })
  667 | 
  668 | 
  669 | # Infecções, exposições, álcool e drogas.
  670 | PERGUNTAS_EXTENSAS.update({
  671 |     "EXT-41": pergunta_tabela(
  672 |         "EXT-41", "Histórico de infecções", "Você já teve alguma destas infecções ou doenças parasitárias?",
  673 |         "Marque somente condições conhecidas e informe a data da cura, alta ou fim do tratamento.",
  674 |         [
  675 |             ("ACTINOMICOSE", "Actinomicose.", TEMPORARIA, "Aguarde 60 dias após cura.", {"valor": 60, "unidade": "dias", "referencia": "evento"}),
  676 |             ("AMEBIASE_INTESTINAL", "Amebíase intestinal.", TEMPORARIA, "Aguarde tratamento e ausência de sintomas.", None),
  677 |             ("AMEBIASE_VISCERAL", "Amebíase visceral.", AVALIACAO, "Aguarde seis meses e apresente sorologia negativa.", None),
  678 |             ("VERMINOSE", "Ancilostomíase / ascaridíase / oxiuríase.", None, "", None),
  679 |             ("BABESIOSE", "Babesiose.", DEFINITIVA, "Babesiose é impedimento definitivo.", None),
  680 |             ("BARTONELOSE", "Bartonelose.", TEMPORARIA, "Aguarde 15 dias após alta.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  681 |             ("BLASTOMICOSE_PULMONAR", "Blastomicose pulmonar.", TEMPORARIA, "Aguarde cinco anos.", {"valor": 5, "unidade": "anos", "referencia": "evento"}),
  682 |             ("BLASTOMICOSE_SISTEMICA", "Blastomicose sistêmica.", DEFINITIVA, "Blastomicose sistêmica é impedimento definitivo.", None),
  683 |             ("BORRELIOSE", "Borreliose / doença de Lyme.", TEMPORARIA, "Aguarde seis meses após cura.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  684 |             ("BOTULISMO", "Botulismo.", TEMPORARIA, "Aguarde três meses após cura.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
  685 |             ("BRUCELOSE_DOENCA", "Brucelose: teve a doença.", TEMPORARIA, "Aguarde um ano após tratamento.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
  686 |             ("BRUCELOSE_EXPOSICAO", "Brucelose: apenas exposição, sem doença.", TEMPORARIA, "Aguarde oito semanas.", {"valor": 8, "unidade": "semanas", "referencia": "evento"}),
  687 |             ("CANDIDIASE_ORAL", "Candidíase oral/esofágica.", AVALIACAO, "Aguarde 30 dias após alta e esclareça a causa.", None),
  688 |             ("CAXUMBA", "Caxumba.", TEMPORARIA, "Aguarde 21 dias após cura.", {"valor": 21, "unidade": "dias", "referencia": "evento"}),
  689 |             ("CHIKUNGUNYA", "Chikungunya.", TEMPORARIA, "Aguarde 30 dias após recuperação completa.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  690 |             ("CISTICERCOSE", "Cisticercose.", AVALIACAO, "Confirme tratamento e ausência de convulsões na forma neurológica.", None),
  691 |             ("EQUINOCOCOSE", "Cisto hidático / equinococose.", DEFINITIVA, "Equinococose é impedimento definitivo.", None),
  692 |             ("CITOMEGALOVIROSE", "Citomegalovirose.", TEMPORARIA, "Aguarde três meses após cura.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
  693 |             ("COVID_SINTOMATICO", "COVID-19 com sintomas.", TEMPORARIA, "Aguarde dez dias após melhora completa.", {"valor": 10, "unidade": "dias", "referencia": "evento"}),
  694 |             ("COVID_ASSINTOMATICO", "COVID-19 sem sintomas.", TEMPORARIA, "Aguarde dez dias desde o exame positivo.", {"valor": 10, "unidade": "dias", "referencia": "evento"}),
  695 |             ("COLERA", "Cólera.", TEMPORARIA, "Aguarde três meses após cura.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
  696 |             ("COQUELUCHE", "Coqueluche.", TEMPORARIA, "Aguarde 30 dias após cura.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  697 |             ("DENGUE", "Dengue clássica.", TEMPORARIA, "Aguarde 30 dias após cura.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  698 |             ("DENGUE_GRAVE", "Dengue grave/hemorrágica.", TEMPORARIA, "Aguarde seis meses após cura.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  699 |             ("DIFTERIA", "Difteria.", TEMPORARIA, "Aguarde 15 dias após cura.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  700 |             ("CHAGAS", "Doença de Chagas.", DEFINITIVA, "Doença de Chagas é impedimento definitivo.", None),
  701 |             ("CREUTZFELDT_JAKOB", "Doença de Creutzfeldt-Jakob.", DEFINITIVA, "Doença de Creutzfeldt-Jakob é impedimento definitivo.", None),
  702 |             ("OESTE_NILO", "Doença do Oeste do Nilo.", TEMPORARIA, "Aguarde seis meses após cura.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  703 |             ("ENCEFALITE_SEM_SEQUELA", "Encefalite viral sem sequela.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  704 |             ("ENCEFALITE_COM_SEQUELA", "Encefalite viral com sequela.", AVALIACAO, "A sequela exige avaliação especializada.", None),
  705 |             ("ENTEROVIROSE", "Enterovirose.", TEMPORARIA, "Aguarde três meses após cura.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
  706 |             ("ESCARLATINA", "Escarlatina.", TEMPORARIA, "Aguarde 15 dias após cura.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  707 |             ("ESQUISTOSSOMOSE_HEPATICA", "Esquistossomose hepática/hepatoesplênica.", DEFINITIVA, "Esta forma de esquistossomose é impedimento definitivo.", None),
  708 |             ("ESQUISTOSSOMOSE_INTESTINAL", "Esquistossomose intestinal/outra forma.", TEMPORARIA, "Aguarde tratamento e ausência de sequelas.", None),
  709 |             ("FEBRE_AMARELA", "Febre amarela: doença.", TEMPORARIA, "Aguarde seis meses após cura.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  710 |             ("FEBRE_TIFOIDE", "Febre tifoide/paratifoide.", TEMPORARIA, "Aguarde três meses após cura.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
  711 |             ("FEBRE_HEMORRAGICA", "Febre hemorrágica.", TEMPORARIA, "Aguarde seis meses após cura.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  712 |             ("FILARIOSE", "Filariose.", DEFINITIVA, "Filariose é impedimento definitivo.", None),
  713 |             ("HANSENIASE", "Hanseníase.", DEFINITIVA, "Hanseníase é impedimento definitivo.", None),
  714 |             ("HEPATITE_BCD", "Hepatite B, C ou D.", DEFINITIVA, "Hepatite B, C ou D é impedimento definitivo.", None),
  715 |             ("HEPATITE_A_ANTES_11", "Hepatite A antes dos 11 anos.", None, "", None),
  716 |             ("HEPATITE_A_DEPOIS_11", "Hepatite A após os 11 anos com comprovação IgM.", AVALIACAO, "A comprovação laboratorial da época deve ser avaliada.", None),
  717 |             ("HERPES_LABIAL", "Herpes labial.", TEMPORARIA, "Aguarde a cura das lesões.", None),
  718 |             ("HERPES_ZOSTER", "Herpes-zóster.", AVALIACAO, "Aguarde seis meses e avalie a imunidade.", None),
  719 |             ("HISTOPLASMOSE", "Histoplasmose.", TEMPORARIA, "Aguarde um ano após cura.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
  720 |             ("HIV", "HIV.", DEFINITIVA, "HIV é impedimento definitivo.", None),
  721 |             ("HTLV", "HTLV.", DEFINITIVA, "HTLV é impedimento definitivo.", None),
  722 |             ("LEISHMANIOSE_CUTANEA", "Leishmaniose cutânea.", TEMPORARIA, "Aguarde seis meses após o fim do tratamento.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  723 |             ("LEISHMANIOSE_VISCERAL", "Leishmaniose visceral.", DEFINITIVA, "Leishmaniose visceral é impedimento definitivo.", None),
  724 |             ("LEPTOSPIROSE", "Leptospirose.", TEMPORARIA, "Aguarde três meses após cura.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
  725 |             ("MALARIA_MALARIAE", "Malária por P. malariae.", DEFINITIVA, "Malária por P. malariae é impedimento definitivo.", None),
  726 |             ("MALARIA_TERCA", "Malária com febre terçã.", TEMPORARIA, "Aguarde três anos após cura.", {"valor": 3, "unidade": "anos", "referencia": "evento"}),
  727 |             ("MENINGITE_SEM_SEQUELA", "Meningite sem sequela.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  728 |             ("MENINGITE_COM_SEQUELA", "Meningite com sequela.", AVALIACAO, "A sequela exige avaliação especializada.", None),
  729 |             ("MICOBACTERIAS", "Micobactérias atípicas.", DEFINITIVA, "Micobactérias atípicas são impedimento definitivo.", None),
  730 |             ("MICOPLASMA", "Micoplasma.", TEMPORARIA, "Aguarde um ano após cura.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
  731 |             ("MICOSE_VISCERAL", "Micoses viscerais.", DEFINITIVA, "Micose visceral é impedimento definitivo.", None),
  732 |             ("MPOX", "Mpox / monkeypox.", TEMPORARIA, "Aguarde todas as lesões resolverem e pelo menos 21 dias desde o início.", {"valor": 21, "unidade": "dias", "referencia": "evento"}),
  733 |             ("MONONUCLEOSE", "Mononucleose.", TEMPORARIA, "Aguarde seis meses após cura.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  734 |             ("NOCARDIOSE", "Nocardiose.", TEMPORARIA, "Aguarde 60 dias após cura.", {"valor": 60, "unidade": "dias", "referencia": "evento"}),
  735 |             ("OROPOUCHE", "Oropouche.", TEMPORARIA, "Aguarde 30 dias após recuperação.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  736 |             ("PARVOVIROSE", "Parvovirose.", TEMPORARIA, "Aguarde seis meses após cura.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  737 |             ("PESTE", "Peste bubônica.", TEMPORARIA, "Aguarde seis meses após cura.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  738 |             ("RUBEOLA", "Rubéola: doença.", TEMPORARIA, "Aguarde 14 dias após cura.", {"valor": 14, "unidade": "dias", "referencia": "evento"}),
  739 |             ("SARAMPO", "Sarampo: doença.", AVALIACAO, "A recuperação e a regra vigente precisam ser avaliadas.", None),
  740 |             ("SIFILIS", "Sífilis.", TEMPORARIA, "Aguarde um ano após tratamento.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
  741 |             ("TETANO", "Tétano.", TEMPORARIA, "Aguarde seis meses após cura.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  742 |             ("TOXOPLASMOSE", "Toxoplasmose.", TEMPORARIA, "Aguarde um ano após cura.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
  743 |             ("TUBERCULOSE_EXTRAPULMONAR", "Tuberculose extrapulmonar.", DEFINITIVA, "Tuberculose extrapulmonar é impedimento definitivo.", None),
  744 |             ("TUBERCULOSE_PULMONAR", "Tuberculose pulmonar.", TEMPORARIA, "Aguarde cinco anos após tratamento, sem sequelas.", {"valor": 5, "unidade": "anos", "referencia": "evento"}),
  745 |             ("VARICELA", "Varicela / catapora: doença.", AVALIACAO, "A resolução e a regra vigente precisam ser avaliadas.", None),
  746 |             ("ZIKA", "Zika.", TEMPORARIA, "Aguarde 120 dias após cura.", {"valor": 120, "unidade": "dias", "referencia": "evento"}),
  747 |             ("NENHUMA", "Nenhuma.", None, "", None),
  748 |             ("OUTRA", "Outra infecção / não sei.", AVALIACAO, "Infecção não listada ou incerta exige avaliação.", None),
  749 |         ],
  750 |         fonte="Manual Elo, seção 13; ref. [1]",
  751 |     ),
  752 |     "EXT-42": pergunta(
  753 |         "EXT-42", "Detalhe sobre hepatite", "Se você já teve hepatite, qual situação descreve melhor?",
  754 |         "Tipo, idade e comprovação laboratorial mudam a regra.",
  755 |         [("NUNCA", "Nunca tive hepatite."), ("B", "Tive hepatite B."), ("C", "Tive hepatite C."), ("D", "Tive hepatite D."), ("A_ANTES_11", "Tive hepatite A antes dos 11 anos."), ("A_DEPOIS_11_COM_IGM", "Tive hepatite A depois dos 11 anos e tenho exame IgM da época."), ("DEPOIS_11_SEM_COMPROVAR", "Tive hepatite depois dos 11 anos sem comprovação de hepatite A."), ("NAO_SEI", "Não sei qual hepatite tive.")],
  756 |         regras={
  757 |             "B": regra(DEFINITIVA, "Hepatite B é impedimento definitivo."),
  758 |             "C": regra(DEFINITIVA, "Hepatite C é impedimento definitivo."),
  759 |             "D": regra(DEFINITIVA, "Hepatite D é impedimento definitivo."),
  760 |             "A_DEPOIS_11_COM_IGM": regra(DOCUMENTACAO, "Leve a comprovação laboratorial IgM da época para avaliação."),
  761 |             "DEPOIS_11_SEM_COMPROVAR": regra(AVALIACAO, "O tipo e a comprovação da hepatite precisam ser avaliados."),
  762 |             "NAO_SEI": regra(AVALIACAO, "Não é seguro classificar a hepatite sem confirmar o tipo."),
  763 |         },
  764 |         fonte="Manual Elo, seção 13; ref. [1]",
  765 |     ),
  766 |     "EXT-43": pergunta_tabela(
  767 |         "EXT-43", "Exposições pessoais e a sangue", "Nos períodos relevantes, você passou por alguma destas situações?",
  768 |         "A pergunta é confidencial, universal e baseada em exposições concretas; informe a data da última exposição.",
  769 |         [
  770 |             ("AUTO_HEMOTERAPIA", "Auto-hemoterapia.", TEMPORARIA, "Aguarde 12 meses desde a última aplicação.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  771 |             ("COMPARTILHOU_AGULHA", "Compartilhou agulha/seringa.", DEFINITIVA, "Compartilhamento de agulha é impedimento definitivo.", None),
  772 |             ("DROGA_INJETAVEL", "Usou droga ilícita injetável.", DEFINITIVA, "Uso de droga ilícita injetável é impedimento definitivo.", None),
  773 |             ("TRANSFUSAO_REINO_UNIDO", "Recebeu transfusão no Reino Unido desde 1980.", DEFINITIVA, "Esta transfusão é impedimento definitivo na regra histórica atual.", None),
  774 |             ("PARCEIRO_HEPATITE", "Relação sexual com pessoa com hepatite B/C.", TEMPORARIA, "Aguarde 12 meses desde a última exposição.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  775 |             ("MORA_HEPATITE", "Mora/morou com pessoa com hepatite B/C.", TEMPORARIA, "Aguarde três meses conforme a regra atual.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
  776 |             ("IST_RECORRENTE", "IST recorrente.", DEFINITIVA, "IST recorrente é impedimento definitivo na regra atual.", None),
  777 |             ("CONFINAMENTO", "Confinamento obrigatório por mais de 72 horas.", TEMPORARIA, "Aguarde 12 meses.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  778 |             ("VIOLENCIA_SEXUAL", "Violência sexual.", TEMPORARIA, "Aguarde 12 meses desde a exposição.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  779 |             ("PARCEIRO_HEMODIALISE", "Parceiro(a) em hemodiálise.", TEMPORARIA, "Aguarde 12 meses.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  780 |             ("PARCEIRO_TRANSFUSAO", "Parceiro(a) com transfusão recente.", TEMPORARIA, "Aguarde 12 meses.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  781 |             ("PARCEIRO_EVENTUAL", "Relação com parceiro eventual/desconhecido.", TEMPORARIA, "Aguarde 12 meses segundo a regra publicada.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  782 |             ("PARCEIRO_INFECCAO", "Parceiro com HBV/HCV/HIV ou outra infecção transmissível.", TEMPORARIA, "Aguarde 12 meses.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  783 |             ("ACIDENTE_BIOLOGICO", "Acidente com sangue/material biológico em mucosa ou pele lesionada.", TEMPORARIA, "Aguarde 12 meses.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  784 |             ("SEXO_TROCA", "Relação sexual em troca de dinheiro ou drogas.", TEMPORARIA, "Aguarde 12 meses.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  785 |             ("NENHUMA", "Nenhuma.", None, "", None),
  786 |             ("PRESENCIAL", "Não sei / prefiro discutir presencialmente.", AVALIACAO, "A situação será discutida em ambiente privado no hemocentro.", None),
  787 |         ],
  788 |         fonte="Manual Elo, seção 14; refs. [1] e [7]",
  789 |     ),
  790 |     "EXT-44": pergunta(
  791 |         "EXT-44", "Álcool", "Quando foi a última vez que você consumiu bebida alcoólica e em que quantidade?",
  792 |         "O álcool pode afetar hidratação, julgamento e resposta à coleta.",
  793 |         [("NAO", "Não bebi recentemente."), ("PEQUENA_12H", "Quantidade pequena/moderada há menos de 12 horas."), ("MAIOR_24H", "Quantidade maior há menos de 24 horas."), ("NAO_SEI", "Bebi, mas não sei estimar a quantidade."), ("CRONICO", "Tenho/tive alcoolismo crônico.")],
  794 |         regras={
  795 |             "PEQUENA_12H": regra(TEMPORARIA, "Aguarde completar 12 horas.", {"valor": 12, "unidade": "horas", "referencia": "hoje"}),
  796 |             "MAIOR_24H": regra(TEMPORARIA, "Aguarde completar 24 horas.", {"valor": 24, "unidade": "horas", "referencia": "hoje"}),
  797 |             "NAO_SEI": regra(AVALIACAO, "Sem estimar a quantidade, adote avaliação conservadora presencial."),
  798 |             "CRONICO": regra(DEFINITIVA, "Alcoolismo crônico é impedimento definitivo na regra atual."),
  799 |         },
  800 |         fonte="Manual Elo, seção 15.1; ref. [1]",
  801 |     ),
  802 |     "EXT-45": pergunta(
  803 |         "EXT-45", "Drogas recreativas ou ilícitas", "Você usou alguma destas substâncias?",
  804 |         "A pergunta é neutra e confidencial; tipo e via alteram a regra.",
  805 |         [("NAO", "Não."), ("MACONHA", "Maconha/cannabis nas últimas 12 horas."), ("COCAINA_NASAL", "Cocaína por via nasal nos últimos 12 meses."), ("CRACK", "Crack nos últimos 12 meses."), ("INJETAVEL", "Droga ilícita injetável em qualquer momento da vida."), ("OUTRA", "Outra droga não listada.")],
  806 |         permite_data=True,
  807 |         exige_data_para=("COCAINA_NASAL", "CRACK"),
  808 |         regras={
  809 |             "MACONHA": regra(TEMPORARIA, "Aguarde 12 horas.", {"valor": 12, "unidade": "horas", "referencia": "hoje"}),
  810 |             "COCAINA_NASAL": regra(TEMPORARIA, "Aguarde 12 meses desde o uso.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  811 |             "CRACK": regra(TEMPORARIA, "Aguarde 12 meses desde o uso.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  812 |             "INJETAVEL": regra(DEFINITIVA, "Uso de droga ilícita injetável é impedimento definitivo."),
  813 |             "OUTRA": regra(AVALIACAO, "A substância e a via precisam ser avaliadas presencialmente."),
  814 |         },
  815 |         fonte="Manual Elo, seção 15.1; ref. [1]",
  816 |     ),
  817 | })
  818 | 
  819 | 
  820 | # Doenças por sistemas do corpo.
  821 | PERGUNTAS_EXTENSAS.update({
  822 |     "EXT-31": pergunta_tabela(
  823 |         "EXT-31", "Digestivas", "Você tem ou teve alguma destas doenças do estômago, intestino, fígado ou pâncreas?",
  824 |         "Endoscopia, cirurgia, antibiótico e internação também devem ser informados nos blocos próprios.",
  825 |         [
  826 |             ("CIRROSE", "Cirrose hepática.", DEFINITIVA, "Cirrose hepática é impedimento definitivo.", None),
  827 |             ("COLITE_PSEUDOMEMBRANOSA", "Colite pseudomembranosa.", TEMPORARIA, "Aguarde 30 dias após o fim do tratamento.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  828 |             ("COLITE_ULCERATIVA", "Colite/retocolite ulcerativa.", DEFINITIVA, "Retocolite ulcerativa é impedimento definitivo.", None),
  829 |             ("DIARREIA_VIRAL", "Diarreia aguda viral.", TEMPORARIA, "Aguarde sete dias após a cura.", {"valor": 7, "unidade": "dias", "referencia": "evento"}),
  830 |             ("DIARREIA_BACTERIANA", "Diarreia aguda bacteriana.", TEMPORARIA, "Aguarde 15 dias após a cura.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  831 |             ("DIARREIA_CRONICA", "Diarreia crônica/persistente.", AVALIACAO, "A causa precisa ser avaliada.", None),
  832 |             ("DIVERTICULOSE", "Diverticulose sem sintomas.", None, "", None),
  833 |             ("DIVERTICULITE", "Diverticulite sem internação.", TEMPORARIA, "Aguarde 30 dias após o tratamento.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  834 |             ("DIVERTICULITE_INTERNACAO", "Diverticulite com internação.", TEMPORARIA, "Aguarde três meses.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
  835 |             ("CELIACA", "Doença celíaca.", AVALIACAO, "Pode ser aceita se controlada e sem sintomas.", None),
  836 |             ("CROHN", "Doença de Crohn.", DEFINITIVA, "Doença de Crohn é impedimento definitivo.", None),
  837 |             ("ESOFAGITE", "Esofagite crônica.", AVALIACAO, "Tratamento, sintomas e endoscopia precisam ser avaliados.", None),
  838 |             ("ESTENOSE_ESOFAGIANA", "Estenose esofagiana.", DEFINITIVA, "Estenose esofagiana é impedimento definitivo.", None),
  839 |             ("GASTRITE", "Gastrite aguda.", TEMPORARIA, "Aguarde 15 dias se não houve sangramento ou endoscopia.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  840 |             ("GASTROENTERITE", "Gastroenterite.", TEMPORARIA, "Aguarde 15 dias após cura.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  841 |             ("HEPATITE_MEDICAMENTOSA", "Hepatite medicamentosa.", TEMPORARIA, "Aguarde seis meses após cura e avalie procedimentos associados.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  842 |             ("HERNIA_HIATO", "Hérnia de hiato.", None, "", None),
  843 |             ("HIPERTENSAO_PORTAL", "Hipertensão portal.", DEFINITIVA, "Hipertensão portal é impedimento definitivo.", None),
  844 |             ("ICTERICIA_SEM_CAUSA", "Icterícia sem causa definida.", DEFINITIVA, "Icterícia sem causa definida é impedimento definitivo na regra compilada.", None),
  845 |             ("INFARTO_MESENTERICO", "Infarto mesentérico.", DEFINITIVA, "Infarto mesentérico é impedimento definitivo.", None),
  846 |             ("LITIASE_BILIAR", "Pedra na vesícula / litíase biliar.", TEMPORARIA, "Aguarde 30 dias após a última cólica.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  847 |             ("PANCREATITE_AGUDA", "Pancreatite aguda.", TEMPORARIA, "Aguarde seis meses após recuperação.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  848 |             ("PANCREATITE_CRONICA", "Pancreatite crônica.", DEFINITIVA, "Pancreatite crônica é impedimento definitivo.", None),
  849 |             ("ULCERA", "Úlcera gástrica/duodenal.", TEMPORARIA, "Aguarde 12 meses.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  850 |             ("NENHUMA", "Nenhuma.", None, "", None),
  851 |             ("OUTRA", "Outra / não sei.", AVALIACAO, "Condição não listada ou incerta exige avaliação.", None),
  852 |         ],
  853 |         fonte="Manual Elo, seção 10.2; ref. [1]",
  854 |     ),
  855 |     "EXT-32": pergunta_tabela(
  856 |         "EXT-32", "Osteomusculares e reumáticas", "Você tem ou já teve alguma destas doenças das articulações, ossos, músculos ou doenças reumáticas?",
  857 |         "Condições sistêmicas, sequelas e imunossupressores precisam ser considerados.",
  858 |         [
  859 |             ("ARTRITE_PSORIATICA", "Artrite psoriática.", DEFINITIVA, "Artrite psoriática é impedimento definitivo.", None),
  860 |             ("ARTRITE_REUMATOIDE", "Artrite reumatoide.", DEFINITIVA, "Artrite reumatoide é impedimento definitivo.", None),
  861 |             ("ARTROPATIA_INFECCIOSA", "Artropatia infecciosa.", TEMPORARIA, "Aguarde um ano após cura.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
  862 |             ("ARTROSE", "Artrose.", None, "", None),
  863 |             ("BEHCET", "Doença de Behçet.", DEFINITIVA, "Doença de Behçet é impedimento definitivo.", None),
  864 |             ("WEGENER", "Granulomatose com poliangiite.", DEFINITIVA, "Granulomatose com poliangiite é impedimento definitivo.", None),
  865 |             ("ESCLERODERMIA", "Esclerodermia.", DEFINITIVA, "Esclerodermia é impedimento definitivo.", None),
  866 |             ("ESPONDILITE", "Espondilite anquilosante.", DEFINITIVA, "Espondilite anquilosante é impedimento definitivo.", None),
  867 |             ("FEBRE_REUMATICA_SEM_SEQUELA", "Febre reumática sem sequela.", TEMPORARIA, "Aguarde dois anos após cura.", {"valor": 2, "unidade": "anos", "referencia": "evento"}),
  868 |             ("FEBRE_REUMATICA_COM_SEQUELA", "Febre reumática com sequela.", DEFINITIVA, "Febre reumática com sequela é impedimento definitivo.", None),
  869 |             ("FIBROMIALGIA", "Fibromialgia.", None, "", None),
  870 |             ("FRATURA", "Fratura sem cirurgia.", TEMPORARIA, "Aguarde 15 dias após alta médica.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  871 |             ("GOTA", "Gota.", AVALIACAO, "Pode ser aceita se estiver sem sintomas.", None),
  872 |             ("LUPUS", "Lúpus eritematoso sistêmico.", DEFINITIVA, "Lúpus sistêmico é impedimento definitivo.", None),
  873 |             ("OSTEOMIELITE_AGUDA", "Osteomielite aguda.", TEMPORARIA, "Aguarde dois meses após cura.", {"valor": 2, "unidade": "meses", "referencia": "evento"}),
  874 |             ("OSTEOMIELITE_CRONICA", "Osteomielite crônica.", DEFINITIVA, "Osteomielite crônica é impedimento definitivo.", None),
  875 |             ("OSTEOPOROSE_PRIMARIA", "Osteoporose primária.", None, "", None),
  876 |             ("OSTEOPOROSE_SECUNDARIA", "Osteoporose secundária.", AVALIACAO, "A doença de base precisa ser avaliada.", None),
  877 |             ("SARCOIDOSE", "Sarcoidose.", DEFINITIVA, "Sarcoidose é impedimento definitivo.", None),
  878 |             ("TENDINITE", "Tendinite.", AVALIACAO, "Aguarde alta e avalie a doença de base quando houver.", None),
  879 |             ("NENHUMA", "Nenhuma.", None, "", None),
  880 |             ("OUTRA", "Outra / não sei.", AVALIACAO, "Condição não listada ou incerta exige avaliação.", None),
  881 |         ],
  882 |         fonte="Manual Elo, seção 11.1; ref. [1]",
  883 |     ),
  884 |     "EXT-33": pergunta(
  885 |         "EXT-33", "Gravidez, parto, aborto e amamentação", "Alguma destas situações se aplica a você?",
  886 |         "Menstruação, por si só, não impede a doação.",
  887 |         [("NENHUMA", "Não estou grávida e não tive parto/aborto recente."), ("GRAVIDA", "Estou grávida."), ("PARTO_VAGINAL", "Tive parto vaginal há menos de 12 semanas."), ("CESAREA", "Tive cesárea há menos de 6 meses."), ("ABORTO", "Tive aborto há menos de 12 semanas."), ("AMAMENTANDO", "Estou amamentando."), ("PAROU_AMAMENTAR", "Parei de amamentar, mas o parto foi há menos de 12 meses."), ("ATRASO", "Menstruação atrasada com possibilidade de gravidez."), ("MENSTRUADA", "Estou menstruada normalmente."), ("MENOPAUSA", "Estou na menopausa/climatério.")],
  888 |         permite_data=True,
  889 |         exige_data_para=("PARTO_VAGINAL", "CESAREA", "ABORTO", "PAROU_AMAMENTAR"),
  890 |         regras={
  891 |             "GRAVIDA": regra(TEMPORARIA, "Aguarde o desfecho da gestação e o prazo correspondente."),
  892 |             "PARTO_VAGINAL": regra(TEMPORARIA, "Aguarde 12 semanas após o parto.", {"valor": 12, "unidade": "semanas", "referencia": "evento"}),
  893 |             "CESAREA": regra(TEMPORARIA, "Aguarde seis meses após a cesárea.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  894 |             "ABORTO": regra(TEMPORARIA, "Aguarde 12 semanas após o aborto.", {"valor": 12, "unidade": "semanas", "referencia": "evento"}),
  895 |             "AMAMENTANDO": regra(TEMPORARIA, "Aguarde a suspensão da amamentação ou 12 meses após o parto, usando a regra mais restritiva."),
  896 |             "PAROU_AMAMENTAR": regra(TEMPORARIA, "Aguarde completar 12 meses após o parto.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  897 |             "ATRASO": regra(TEMPORARIA, "Aguarde a exclusão de gravidez."),
  898 |         },
  899 |         fonte="Manual Elo, seção 11.2; ref. [1]",
  900 |     ),
  901 |     "EXT-34": pergunta_tabela(
  902 |         "EXT-34", "Doenças urinárias, renais e genitais", "Você tem ou teve alguma destas condições?",
  903 |         "Infecções costumam ter prazo; doenças renais crônicas podem ser definitivas.",
  904 |         [
  905 |             ("CANDIDIASE", "Candidíase genital.", TEMPORARIA, "Aguarde sete dias após o tratamento.", {"valor": 7, "unidade": "dias", "referencia": "evento"}),
  906 |             ("CISTITE", "Cistite.", TEMPORARIA, "Aguarde 15 dias após cura, sem sintomas.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  907 |             ("CISTO_RENAL", "Cisto renal isolado.", AVALIACAO, "É necessário confirmar ausência de suspeita de câncer.", None),
  908 |             ("CLAMIDIA", "Clamídia.", TEMPORARIA, "Aguarde 15 dias após tratamento.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  909 |             ("ENDOMETRIOSE", "Endometriose.", None, "", None),
  910 |             ("GLOMERULONEFRITE", "Glomerulonefrite aguda.", TEMPORARIA, "Aguarde 30 dias após tratamento e confirme ausência de sequelas.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  911 |             ("GONORREIA", "Gonorreia.", TEMPORARIA, "Aguarde um ano após tratamento.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
  912 |             ("HERPES_GENITAL", "Herpes genital.", TEMPORARIA, "Aguarde a cura das lesões.", None),
  913 |             ("HPV", "HPV genital.", TEMPORARIA, "Aguarde a cura das lesões.", None),
  914 |             ("RENAL_CRONICA", "Doença/insuficiência renal crônica.", DEFINITIVA, "Doença renal crônica é impedimento definitivo.", None),
  915 |             ("LITIASE_RENAL", "Litíase renal.", AVALIACAO, "Pode ser aceita se sem sintomas e sem medicamento impeditivo.", None),
  916 |             ("MALFORMACAO_RENAL", "Malformação renal.", AVALIACAO, "A função renal precisa estar normal.", None),
  917 |             ("NODULO_MAMARIO", "Nódulo mamário não investigado.", AVALIACAO, "É necessário excluir malignidade.", None),
  918 |             ("PIELONEFRITE", "Pielonefrite.", TEMPORARIA, "Aguarde 30 dias após cura e confirme ausência de sequelas.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  919 |             ("RINS_POLICISTICOS", "Rins policísticos.", DEFINITIVA, "Rins policísticos são impedimento definitivo.", None),
  920 |             ("SINDROME_RENAL_CRONICA", "Síndrome nefrítica/nefrótica crônica.", DEFINITIVA, "Síndrome renal crônica é impedimento definitivo.", None),
  921 |             ("SINDROME_RENAL_AGUDA", "Síndrome nefrítica/nefrótica aguda.", AVALIACAO, "A doença de base precisa ser avaliada.", None),
  922 |             ("URETRITE", "Uretrite.", TEMPORARIA, "Aguarde 30 dias após cura; gonocócica segue regra própria.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
  923 |             ("SALPINGITE", "Salpingite.", TEMPORARIA, "Aguarde três meses; gonocócica segue regra própria.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
  924 |             ("VAGINITE", "Vaginite/colpite.", TEMPORARIA, "Aguarde sete dias após tratamento.", {"valor": 7, "unidade": "dias", "referencia": "evento"}),
  925 |             ("NENHUMA", "Nenhuma.", None, "", None),
  926 |             ("OUTRA", "Outra / não sei.", AVALIACAO, "Condição não listada ou incerta exige avaliação.", None),
  927 |         ],
  928 |         fonte="Manual Elo, seção 11.2; ref. [1]",
  929 |     ),
  930 |     "EXT-35": pergunta_tabela(
  931 |         "EXT-35", "Coração e vasos", "Você tem ou já teve alguma destas condições do coração ou circulação?",
  932 |         "Sopro, arritmia e condições com exceção precisam de avaliação profissional.",
  933 |         [
  934 |             ("ANEURISMA_GRANDE", "Aneurisma de grande artéria.", DEFINITIVA, "Aneurisma de grande artéria é impedimento definitivo.", None),
  935 |             ("ANEURISMA_PEQUENO", "Aneurisma de pequena artéria tratado.", TEMPORARIA, "Aguarde 12 meses se não houver aneurisma remanescente.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
  936 |             ("ANGINA", "Angina.", DEFINITIVA, "Angina é impedimento definitivo.", None),
  937 |             ("ARRITMIA", "Arritmia relevante.", AVALIACAO, "O tipo de arritmia precisa ser confirmado.", None),
  938 |             ("BLOQUEIO_RAMOS", "Bloqueio de ramo direito isolado.", AVALIACAO, "Pode ser aceito se isolado e sem outras alterações.", None),
  939 |             ("BRADICARDIA_ATLETA", "Bradicardia de atleta.", AVALIACAO, "Exige avaliação do pulso e evidência de treinamento.", None),
  940 |             ("ENDOCARDITE", "Endocardite bacteriana sem sequela.", TEMPORARIA, "Aguarde dois anos sem sequelas.", {"valor": 2, "unidade": "anos", "referencia": "evento"}),
  941 |             ("EXTRASSISTOLES", "Extrassístoles.", AVALIACAO, "A frequência precisa ser avaliada.", None),
  942 |             ("HIPERTENSAO_ORGAO", "Hipertensão com lesão de órgão-alvo.", DEFINITIVA, "Hipertensão com lesão de órgão-alvo é impedimento definitivo.", None),
  943 |             ("INFARTO", "Infarto do miocárdio.", DEFINITIVA, "Infarto do miocárdio é impedimento definitivo.", None),
  944 |             ("INSUFICIENCIA_CARDIACA", "Insuficiência cardíaca.", DEFINITIVA, "Insuficiência cardíaca é impedimento definitivo.", None),
  945 |             ("MIOCARDITE_SEM_SEQUELA", "Miocardite/pericardite sem sequela.", TEMPORARIA, "Aguarde um ano.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
  946 |             ("MIOCARDITE_COM_SEQUELA", "Miocardite/pericardite com sequela.", DEFINITIVA, "Miocardite ou pericardite com sequela é impedimento definitivo.", None),
  947 |             ("PROLAPSO_MITRAL", "Prolapso da válvula mitral.", AVALIACAO, "Insuficiência valvar e arritmia precisam ser excluídas.", None),
  948 |             ("SOPRO", "Sopro cardíaco.", AVALIACAO, "O sopro precisa de avaliação cardiológica.", None),
  949 |             ("TROMBOFLEBITE", "Tromboflebite isolada.", TEMPORARIA, "Aguarde seis meses após tratamento.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  950 |             ("TVP_ISOLADA", "TVP isolada.", TEMPORARIA, "Aguarde seis meses após tratamento.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  951 |             ("TVP_RECORRENTE", "TVP recorrente / trombose arterial.", DEFINITIVA, "Trombose recorrente ou arterial é impedimento definitivo.", None),
  952 |             ("VALVULOPATIA", "Valvulopatia.", DEFINITIVA, "Valvulopatia é impedimento definitivo, salvo exceções avaliadas.", None),
  953 |             ("WPW_SEM_ABLACAO", "Wolff-Parkinson-White sem ablação bem-sucedida.", DEFINITIVA, "WPW é impedimento definitivo na ausência da exceção documentada.", None),
  954 |             ("WPW_ABLACAO", "Wolff-Parkinson-White após ablação bem-sucedida e com relatório.", AVALIACAO, "A exceção precisa ser confirmada por relatório.", None),
  955 |             ("NENHUMA", "Nenhuma.", None, "", None),
  956 |             ("OUTRA", "Outra / não sei.", AVALIACAO, "Condição cardíaca não listada ou incerta exige avaliação.", None),
  957 |         ],
  958 |         fonte="Manual Elo, seção 12.1; ref. [1]",
  959 |     ),
  960 |     "EXT-36": pergunta(
  961 |         "EXT-36", "Pressão alta e pressão conhecida", "Você tem hipertensão ou sabe que sua pressão está alterada?",
  962 |         "O valor oficial será medido no hemocentro.",
  963 |         [("NAO", "Não tenho hipertensão conhecida."), ("CONTROLADA", "Tenho hipertensão controlada, sem lesão de órgão-alvo e uso medicamento prescrito."), ("COM_LESAO", "Tenho hipertensão e lesão de órgão-alvo."), ("DESCONTROLADA", "Está descontrolada / não sei se está controlada."), ("SEM_DIAGNOSTICO", "Não tenho diagnóstico, mas já medi acima dos limites.")],
  964 |         regras={
  965 |             "CONTROLADA": regra(AVALIACAO, "A pressão, medicamentos e ausência de lesão devem ser confirmados no dia."),
  966 |             "COM_LESAO": regra(DEFINITIVA, "Hipertensão com lesão de órgão-alvo é impedimento definitivo."),
  967 |             "DESCONTROLADA": regra(AVALIACAO, "Pressão descontrolada ou incerta exige avaliação presencial."),
  968 |             "SEM_DIAGNOSTICO": regra(AVALIACAO, "A pressão elevada precisa ser aferida e investigada."),
  969 |         },
  970 |         fonte="Manual Elo, seções 3 e 12.1; ref. [1]",
  971 |     ),
  972 |     "EXT-37": pergunta_tabela(
  973 |         "EXT-37", "Pulmões e vias respiratórias", "Você tem ou já teve alguma destas doenças respiratórias?",
  974 |         "Sintomas atuais de gripe e COVID são tratados nas perguntas anteriores.",
  975 |         [
  976 |             ("ABSCESSO", "Abscesso pulmonar.", TEMPORARIA, "Aguarde um ano após cura.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
  977 |             ("ASMA_GRAVE", "Asma grave.", DEFINITIVA, "Asma grave é impedimento definitivo.", None),
  978 |             ("ASMA_LEVE", "Asma leve controlada.", TEMPORARIA, "Aguarde uma semana após crise e sem medicamentos.", {"valor": 1, "unidade": "semanas", "referencia": "evento"}),
  979 |             ("BRONQUITE", "Bronquite aguda.", TEMPORARIA, "Aguarde 15 dias após cura.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  980 |             ("DPOC", "DPOC.", DEFINITIVA, "DPOC é impedimento definitivo.", None),
  981 |             ("FIBROSE", "Fibrose pulmonar idiopática.", DEFINITIVA, "Fibrose pulmonar idiopática é impedimento definitivo.", None),
  982 |             ("HIPERTENSAO_PULMONAR", "Hipertensão pulmonar.", DEFINITIVA, "Hipertensão pulmonar é impedimento definitivo.", None),
  983 |             ("PNEUMONIA_AMBULATORIAL", "Pneumonia tratada fora do hospital.", TEMPORARIA, "Aguarde três meses após cura.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
  984 |             ("PNEUMONIA_INTERNADA", "Pneumonia com internação sem drenagem.", TEMPORARIA, "Aguarde três meses.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
  985 |             ("PNEUMONIA_DRENAGEM", "Pneumonia com drenagem.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
  986 |             ("PNEUMOTORAX", "Pneumotórax espontâneo.", TEMPORARIA, "Aguarde três meses.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
  987 |             ("SINUSITE_OTITE", "Sinusite/otite.", TEMPORARIA, "Aguarde 15 dias após cura.", {"valor": 15, "unidade": "dias", "referencia": "evento"}),
  988 |             ("TROMBOEMBOLISMO", "Tromboembolismo pulmonar.", DEFINITIVA, "Tromboembolismo pulmonar é impedimento definitivo.", None),
  989 |             ("TUBERCULOSE_MILIAR", "Tuberculose miliar.", DEFINITIVA, "Tuberculose miliar é impedimento definitivo.", None),
  990 |             ("TUBERCULOSE_PULMONAR", "Tuberculose pulmonar.", TEMPORARIA, "Aguarde cinco anos após tratamento, sem sequelas.", {"valor": 5, "unidade": "anos", "referencia": "evento"}),
  991 |             ("NENHUMA", "Nenhuma.", None, "", None),
  992 |             ("OUTRA", "Outra / não sei.", AVALIACAO, "Condição respiratória não listada ou incerta exige avaliação.", None),
  993 |         ],
  994 |         fonte="Manual Elo, seção 12.2; ref. [1]",
  995 |     ),
  996 |     "EXT-38": pergunta_tabela(
  997 |         "EXT-38", "Neurológicas e psiquiátricas", "Você tem ou já teve alguma destas condições neurológicas ou psiquiátricas?",
  998 |         "A avaliação deve ser respeitosa e nunca julgar a pessoa somente pelo diagnóstico.",
  999 |         [
 1000 |             ("AVC", "AVC.", DEFINITIVA, "AVC é impedimento definitivo.", None),
 1001 |             ("ANEURISMA", "Aneurisma intracraniano.", DEFINITIVA, "Aneurisma intracraniano é impedimento definitivo.", None),
 1002 |             ("CONVULSAO_SECUNDARIA", "Convulsão febril/metabólica/pós-trauma.", TEMPORARIA, "Aguarde dois anos sem crises após suspensão médica do tratamento.", {"valor": 2, "unidade": "anos", "referencia": "evento"}),
 1003 |             ("EPILEPSIA", "Epilepsia.", TEMPORARIA, "Aguarde três anos sem crises após suspensão médica do tratamento.", {"valor": 3, "unidade": "anos", "referencia": "evento"}),
 1004 |             ("DEPRESSAO", "Depressão controlada.", AVALIACAO, "Controle e medicamentos precisam ser avaliados.", None),
 1005 |             ("ALZHEIMER", "Doença de Alzheimer.", DEFINITIVA, "Doença de Alzheimer é impedimento definitivo.", None),
 1006 |             ("GUILLAIN_BARRE", "Síndrome de Guillain-Barré.", DEFINITIVA, "Guillain-Barré é impedimento definitivo na regra atual.", None),
 1007 |             ("PARKINSON", "Doença de Parkinson.", DEFINITIVA, "Doença de Parkinson é impedimento definitivo.", None),
 1008 |             ("ENXAQUECA", "Enxaqueca.", AVALIACAO, "Pode ser aceita se sem sintomas e sem medicamento impeditivo.", None),
 1009 |             ("ESCLEROSE_ELA", "Esclerose múltipla / ELA.", DEFINITIVA, "Esclerose múltipla ou ELA é impedimento definitivo.", None),
 1010 |             ("HEMATOMA_SEM_SEQUELA", "Hematoma subdural/epidural sem sequela.", TEMPORARIA, "Aguarde um ano.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
 1011 |             ("HEMATOMA_COM_SEQUELA", "Hematoma subdural/epidural com sequela.", AVALIACAO, "A sequela exige avaliação especializada.", None),
 1012 |             ("LABIRINTITE", "Labirintite.", TEMPORARIA, "Aguarde 30 dias após a crise e sem medicamentos.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
 1013 |             ("DESMAIOS", "Lipotímias/desmaios repetidos.", AVALIACAO, "A causa dos desmaios precisa ser esclarecida.", None),
 1014 |             ("MIASTENIA", "Miastenia gravis.", DEFINITIVA, "Miastenia gravis é impedimento definitivo.", None),
 1015 |             ("NEUROFIBROMATOSE", "Neurofibromatose.", AVALIACAO, "A forma clínica e o local de punção precisam ser avaliados.", None),
 1016 |             ("BELL", "Paralisia de Bell.", None, "", None),
 1017 |             ("PSICOSE", "Psicoses / esquizofrenia.", DEFINITIVA, "A regra publicada classifica esta condição como impedimento definitivo.", None),
 1018 |             ("TRAUMA_SEM_SEQUELA", "Traumatismo craniano sem sequela.", TEMPORARIA, "Aguarde um ano.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
 1019 |             ("TRAUMA_COM_SEQUELA", "Traumatismo craniano com sequela.", AVALIACAO, "A sequela exige avaliação especializada.", None),
 1020 |             ("NENHUMA", "Nenhuma.", None, "", None),
 1021 |             ("OUTRA", "Outra / não sei.", AVALIACAO, "Condição não listada ou incerta exige avaliação.", None),
 1022 |         ],
 1023 |         fonte="Manual Elo, seção 12.3; ref. [1]",
 1024 |     ),
 1025 |     "EXT-39": pergunta_tabela(
 1026 |         "EXT-39", "Doenças dos olhos", "Você tem ou teve alguma destas condições nos olhos?",
 1027 |         "A doença de base pode ser mais importante que a manifestação ocular.",
 1028 |         [
 1029 |             ("CONJUNTIVITE", "Conjuntivite / blefarite / terçol.", TEMPORARIA, "Aguarde uma semana após cura.", {"valor": 1, "unidade": "semanas", "referencia": "evento"}),
 1030 |             ("INFLAMACAO", "Episclerite / esclerite / irite / iridociclite.", AVALIACAO, "A doença de base precisa ser avaliada.", None),
 1031 |             ("GLAUCOMA", "Glaucoma.", AVALIACAO, "Controle e colírios precisam ser avaliados; não suspenda medicamento.", None),
 1032 |             ("NEURITE", "Neurite óptica.", AVALIACAO, "Tratamento e doença de base precisam ser avaliados.", None),
 1033 |             ("RETINOPATIA", "Retinopatia.", AVALIACAO, "A doença de base precisa ser avaliada.", None),
 1034 |             ("RETINOSE", "Retinose pigmentar.", None, "", None),
 1035 |             ("TRACOMA", "Tracoma.", TEMPORARIA, "Aguarde 12 meses após tratamento e cura.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
 1036 |             ("NENHUMA", "Nenhuma.", None, "", None),
 1037 |             ("OUTRA", "Outra / não sei.", AVALIACAO, "Condição ocular não listada ou incerta exige avaliação.", None),
 1038 |         ],
 1039 |         fonte="Manual Elo, seção 12.4; ref. [1]",
 1040 |     ),
 1041 |     "EXT-40": pergunta_tabela(
 1042 |         "EXT-40", "Intoxicações e doenças ocupacionais", "Você já teve doença ou intoxicação causada por substâncias do trabalho ou ambiente?",
 1043 |         "Não marque apenas pela profissão; informe diagnóstico ou exposição conhecida.",
 1044 |         [
 1045 |             ("ASBESTOSE", "Asbestose.", DEFINITIVA, "Asbestose é impedimento definitivo.", None),
 1046 |             ("BENZENO_HEMATOLOGICA", "Intoxicação por benzeno com alteração hematológica.", DEFINITIVA, "Esta intoxicação é impedimento definitivo.", None),
 1047 |             ("BENZENO_SEM_HEMATOLOGICA", "Intoxicação por benzeno sem alteração hematológica.", TEMPORARIA, "Aguarde seis meses após cura.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1048 |             ("BERILIO", "Intoxicação por berílio.", TEMPORARIA, "Aguarde seis meses após cura.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1049 |             ("CHUMBO", "Intoxicação por chumbo.", DEFINITIVA, "Intoxicação por chumbo é impedimento definitivo.", None),
 1050 |             ("CROMO", "Intoxicação por cromo.", DEFINITIVA, "Intoxicação por cromo é impedimento definitivo.", None),
 1051 |             ("METAIS", "Outros metais pesados.", AVALIACAO, "O agente e a manifestação precisam ser avaliados.", None),
 1052 |             ("PNEUMOCONIOSE", "Pneumoconiose / silicose / siderose.", DEFINITIVA, "Estas pneumoconioses são impedimento definitivo em geral.", None),
 1053 |             ("NENHUMA", "Nenhuma.", None, "", None),
 1054 |             ("OUTRA", "Outra exposição tóxica / não sei.", AVALIACAO, "Exposição não listada ou incerta exige avaliação.", None),
 1055 |         ],
 1056 |         fonte="Manual Elo, seção 12.5; ref. [1]",
 1057 |     ),
 1058 | })
 1059 | 
 1060 | 
 1061 | # Procedimentos, cirurgias, câncer e pele.
 1062 | PERGUNTAS_EXTENSAS.update({
 1063 |     "EXT-21": pergunta(
 1064 |         "EXT-21", "Tatuagem ou micropigmentação", "Você fez tatuagem, maquiagem definitiva ou micropigmentação recentemente?",
 1065 |         "O prazo depende da data e das condições de higiene e esterilização.",
 1066 |         [("NAO", "Não."), ("SEGURA", "Sim, em local regularizado e com material descartável/esterilizado."), ("SEM_SEGURANCA", "Sim, mas não consigo confirmar higiene/esterilização."), ("INFLAMOU", "Sim, e houve inflamação/infecção depois."), ("NAO_SEI", "Não sei avaliar se o local era seguro.")],
 1067 |         permite_data=True,
 1068 |         exige_data_para=("SEGURA", "SEM_SEGURANCA", "INFLAMOU", "NAO_SEI"),
 1069 |         regras={
 1070 |             "SEGURA": regra(TEMPORARIA, "Aguarde seis meses após o procedimento.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1071 |             "SEM_SEGURANCA": regra(TEMPORARIA, "Aguarde 12 meses quando a segurança não puder ser comprovada.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
 1072 |             "INFLAMOU": regra(AVALIACAO, "A infecção deve estar curada e seu prazo deve ser somado ao do procedimento."),
 1073 |             "NAO_SEI": regra(TEMPORARIA, "Sem comprovação de segurança, use o prazo orientativo de 12 meses.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
 1074 |         },
 1075 |         fonte="Manual Elo, seção 7; ref. [1]",
 1076 |     ),
 1077 |     "EXT-22": pergunta(
 1078 |         "EXT-22", "Piercing", "Você colocou piercing recentemente ou ainda usa piercing na boca ou nos genitais?",
 1079 |         "Piercings orais e genitais mantêm o risco enquanto estiverem no local.",
 1080 |         [("NAO", "Não."), ("SEGURA", "Coloquei piercing em condições adequadas."), ("SEM_SEGURANCA", "Não consigo confirmar as condições de higiene."), ("ORAL", "Tenho piercing oral."), ("GENITAL", "Tenho piercing genital."), ("RETIRADO", "Retirei piercing oral/genital recentemente.")],
 1081 |         permite_data=True,
 1082 |         exige_data_para=("SEGURA", "SEM_SEGURANCA", "RETIRADO"),
 1083 |         regras={
 1084 |             "SEGURA": regra(TEMPORARIA, "Aguarde seis meses após a colocação.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1085 |             "SEM_SEGURANCA": regra(TEMPORARIA, "Aguarde 12 meses após a colocação.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
 1086 |             "ORAL": regra(TEMPORARIA, "A liberação só pode ser contada 12 meses depois da retirada."),
 1087 |             "GENITAL": regra(TEMPORARIA, "A liberação só pode ser contada 12 meses depois da retirada."),
 1088 |             "RETIRADO": regra(TEMPORARIA, "Aguarde 12 meses desde a retirada.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
 1089 |         },
 1090 |         fonte="Manual Elo, seção 7; ref. [1]",
 1091 |     ),
 1092 |     "EXT-23": pergunta(
 1093 |         "EXT-23", "Acupuntura", "Você fez acupuntura recentemente?",
 1094 |         "O prazo muda conforme esterilidade, antissepsia e presença de inflamação.",
 1095 |         [("NAO", "Não."), ("SEGURA", "Sim, com serviço autorizado, agulhas adequadas e sem inflamação."), ("SEM_SEGURANCA", "Sim, mas não consigo confirmar esterilidade/material."), ("INFLAMOU", "Sim, e o local inflamou/infectou.")],
 1096 |         permite_data=True,
 1097 |         exige_data_para=("SEGURA", "SEM_SEGURANCA", "INFLAMOU"),
 1098 |         regras={
 1099 |             "SEGURA": regra(TEMPORARIA, "Aguarde 72 horas após a sessão.", {"valor": 72, "unidade": "horas", "referencia": "evento"}),
 1100 |             "SEM_SEGURANCA": regra(TEMPORARIA, "Aguarde 12 meses quando a segurança não puder ser comprovada.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
 1101 |             "INFLAMOU": regra(AVALIACAO, "A inflamação ou infecção deve ser curada e avaliada."),
 1102 |         },
 1103 |         fonte="Manual Elo, seção 7; ref. [1]",
 1104 |     ),
 1105 |     "EXT-24": pergunta_tabela(
 1106 |         "EXT-24", "Procedimentos estéticos invasivos", "Você fez algum destes procedimentos estéticos recentemente?",
 1107 |         "Marque todos; informe a data. Se a segurança não for conhecida, descreva nos detalhes.",
 1108 |         [
 1109 |             ("BOTOX", "Botox / toxina botulínica.", TEMPORARIA, "Aguarde três dias se foi seguro e sem inflamação.", {"valor": 3, "unidade": "dias", "referencia": "evento"}),
 1110 |             ("CARBOXITERAPIA", "Carboxiterapia.", TEMPORARIA, "Aguarde três dias se foi segura.", {"valor": 3, "unidade": "dias", "referencia": "evento"}),
 1111 |             ("CRIOLIPOLISE", "Criolipólise.", TEMPORARIA, "Aguarde três dias e ausência de reação inflamatória.", {"valor": 3, "unidade": "dias", "referencia": "evento"}),
 1112 |             ("ELETROLISE", "Eletrólise.", TEMPORARIA, "Aguarde três dias se foi segura.", {"valor": 3, "unidade": "dias", "referencia": "evento"}),
 1113 |             ("MESOTERAPIA", "Mesoterapia.", TEMPORARIA, "Aguarde três dias; material ou segurança incertos exigem avaliação.", {"valor": 3, "unidade": "dias", "referencia": "evento"}),
 1114 |             ("MICROAGULHAMENTO", "Microagulhamento.", TEMPORARIA, "Aguarde três dias se seguro e sem inflamação.", {"valor": 3, "unidade": "dias", "referencia": "evento"}),
 1115 |             ("PREENCHIMENTO", "Preenchimento dérmico.", TEMPORARIA, "Aguarde três dias; material humano/animal pode exigir 12 meses.", {"valor": 3, "unidade": "dias", "referencia": "evento"}),
 1116 |             ("OUTRO", "Outro procedimento estético invasivo.", AVALIACAO, "O procedimento, material e antissepsia precisam ser avaliados.", None),
 1117 |             ("NENHUM", "Nenhum procedimento invasivo recente.", None, "", None),
 1118 |         ],
 1119 |         perguntar_seguranca=True,
 1120 |         perguntar_inflamacao=True,
 1121 |         fonte="Manual Elo, seção 7; ref. [1]",
 1122 |     ),
 1123 |     "EXT-25": pergunta(
 1124 |         "EXT-25", "Endoscopia ou laparoscopia", "Você realizou endoscopia, colonoscopia, laparoscopia ou outro procedimento endoscópico nos últimos meses?",
 1125 |         "O motivo do procedimento também pode ter uma regra própria.",
 1126 |         [("NAO", "Não."), ("ENDOSCOPIA", "Sim, realizei endoscopia/colonoscopia/laparoscopia."), ("CIRURGIA_ENDOSCOPICA", "Sim, foi uma cirurgia endoscópica."), ("NAO_SEI", "Não sei qual foi o procedimento.")],
 1127 |         permite_data=True,
 1128 |         exige_data_para=("ENDOSCOPIA", "CIRURGIA_ENDOSCOPICA"),
 1129 |         regras={
 1130 |             "ENDOSCOPIA": regra(TEMPORARIA, "Aguarde seis meses após o procedimento.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1131 |             "CIRURGIA_ENDOSCOPICA": regra(TEMPORARIA, "Aguarde seis meses e avalie a doença que motivou a cirurgia.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1132 |             "NAO_SEI": regra(AVALIACAO, "O tipo e o motivo do procedimento precisam ser confirmados."),
 1133 |         },
 1134 |         fonte="Manual Elo, seções 7 e 8.2; ref. [1]",
 1135 |     ),
 1136 |     "EXT-26": pergunta_tabela(
 1137 |         "EXT-26", "Procedimentos odontológicos", "Você fez algum tratamento dentário recente?",
 1138 |         "Informe a data da última manipulação, cura ou término do tratamento.",
 1139 |         [
 1140 |             ("ABSCESSO", "Abscesso dentário.", TEMPORARIA, "Aguarde 30 dias após a cura.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
 1141 |             ("APARELHO_SEM_SANGRAMENTO", "Ajuste de aparelho sem sangramento.", TEMPORARIA, "Aguarde 24 horas.", {"valor": 24, "unidade": "horas", "referencia": "evento"}),
 1142 |             ("APARELHO_COM_SANGRAMENTO", "Ajuste de aparelho com sangramento.", TEMPORARIA, "Aguarde 72 horas.", {"valor": 72, "unidade": "horas", "referencia": "evento"}),
 1143 |             ("EXTRACAO", "Extração dentária.", TEMPORARIA, "Aguarde sete dias após tratamento e recuperação.", {"valor": 7, "unidade": "dias", "referencia": "evento"}),
 1144 |             ("GENGIVITE", "Gengivite.", TEMPORARIA, "Aguarde sete dias após a cura.", {"valor": 7, "unidade": "dias", "referencia": "evento"}),
 1145 |             ("IMPLANTE", "Implante dentário.", TEMPORARIA, "Aguarde 30 dias e ausência de sintomas.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
 1146 |             ("LIMPEZA", "Limpeza dentária.", TEMPORARIA, "Aguarde 72 horas.", {"valor": 72, "unidade": "horas", "referencia": "evento"}),
 1147 |             ("OBTURACAO_SIMPLES", "Obturação sem anestesia/sangramento.", TEMPORARIA, "Aguarde 24 horas.", {"valor": 24, "unidade": "horas", "referencia": "evento"}),
 1148 |             ("OBTURACAO_INVASIVA", "Obturação com anestesia ou sangramento.", TEMPORARIA, "Aguarde 72 horas.", {"valor": 72, "unidade": "horas", "referencia": "evento"}),
 1149 |             ("CANAL", "Tratamento de canal.", TEMPORARIA, "Aguarde sete dias após a última manipulação.", {"valor": 7, "unidade": "dias", "referencia": "evento"}),
 1150 |             ("ANESTESIA_GERAL", "Procedimento dentário com anestesia geral.", TEMPORARIA, "Aguarde 30 dias e considere os demais fatores.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
 1151 |             ("OUTRO", "Outro procedimento dentário.", AVALIACAO, "Consulte a regra específica do procedimento.", None),
 1152 |             ("NENHUM", "Nenhum procedimento recente.", None, "", None),
 1153 |         ],
 1154 |         fonte="Manual Elo, seção 8.1; ref. [1]",
 1155 |     ),
 1156 |     "EXT-27": pergunta_tabela(
 1157 |         "EXT-27", "Cirurgias e procedimentos médicos", "Você já fez recentemente ou no passado algum destes procedimentos que podem mudar a elegibilidade?",
 1158 |         "Marque todos e informe data, motivo, complicações, infecção, medicamentos e transfusão nos detalhes.",
 1159 |         [
 1160 |             ("ANESTESIA_GERAL", "Anestesia geral isolada.", TEMPORARIA, "Aguarde 30 dias; a cirurgia pode exigir prazo maior.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
 1161 |             ("AMIGDALECTOMIA", "Amigdalectomia.", TEMPORARIA, "Aguarde três meses.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
 1162 |             ("APENDICECTOMIA", "Apendicectomia.", TEMPORARIA, "Aguarde três meses.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
 1163 |             ("ARTRODESE", "Artrodese de coluna.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1164 |             ("ARTROSCOPIA", "Artroscopia.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1165 |             ("BALAO_INTRAGASTRICO", "Balão intragástrico após retirada.", TEMPORARIA, "Aguarde seis meses após retirada e estabilização do peso.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1166 |             ("CATETERISMO", "Cateterismo cardíaco.", AVALIACAO, "Aguarde pelo menos 30 dias e avalie a doença cardíaca.", None),
 1167 |             ("CINTILOGRAFIA", "Cintilografia / radioisótopos.", TEMPORARIA, "Aguarde sete dias por aplicação.", {"valor": 7, "unidade": "dias", "referencia": "evento"}),
 1168 |             ("VASCULAR_COMPLEXA", "Cirurgia vascular complexa.", DEFINITIVA, "Cirurgia vascular complexa é impedimento definitivo.", None),
 1169 |             ("CARDIACA", "Cirurgia cardíaca.", DEFINITIVA, "Cirurgia cardíaca é impedimento definitivo.", None),
 1170 |             ("HIPOFISE", "Cirurgia de hipófise.", DEFINITIVA, "Cirurgia de hipófise é impedimento definitivo.", None),
 1171 |             ("TIREOIDE", "Cirurgia de tireoide/paratireoide.", AVALIACAO, "Aguarde seis meses e avalie a doença de base.", None),
 1172 |             ("DERMATOLOGICA", "Cirurgia dermatológica pequena.", TEMPORARIA, "Aguarde cicatrização completa.", None),
 1173 |             ("ENDOSCOPICA", "Cirurgia endoscópica.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1174 |             ("GINECOLOGICA_PEQUENA", "Cirurgia ginecológica pequena.", TEMPORARIA, "Aguarde três meses após alta.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
 1175 |             ("GINECOLOGICA_GRANDE", "Cirurgia ginecológica grande.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1176 |             ("ORTOPEDICA", "Cirurgia ortopédica.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1177 |             ("PLASTICA_LOCAL", "Cirurgia plástica com anestesia local.", TEMPORARIA, "Aguarde três meses.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
 1178 |             ("PLASTICA_GERAL", "Cirurgia plástica com bloqueio/anestesia geral.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1179 |             ("UROLOGICA_PEQUENA", "Cirurgia urológica pequena.", TEMPORARIA, "Aguarde 30 dias após alta.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
 1180 |             ("VARIZES", "Cirurgia de varizes.", TEMPORARIA, "Aguarde três meses.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
 1181 |             ("COLECISTECTOMIA", "Colecistectomia.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1182 |             ("COLECTOMIA", "Colectomia.", TEMPORARIA, "Aguarde um ano.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
 1183 |             ("CURETAGEM", "Curetagem pós-aborto.", TEMPORARIA, "Aguarde 12 semanas.", {"valor": 12, "unidade": "semanas", "referencia": "evento"}),
 1184 |             ("ENTERECTOMIA", "Enterectomia.", DEFINITIVA, "Enterectomia é impedimento definitivo.", None),
 1185 |             ("ENXERTO_HETEROLOGO", "Enxerto heterólogo.", TEMPORARIA, "Aguarde um ano.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
 1186 |             ("ESPLENECTOMIA_DOENCA", "Esplenectomia por doença.", DEFINITIVA, "Esplenectomia por doença é impedimento definitivo.", None),
 1187 |             ("ESPLENECTOMIA_TRAUMA", "Esplenectomia por trauma.", TEMPORARIA, "A exceção por trauma exige espera de um ano.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
 1188 |             ("GASTRECTOMIA_BARIATRICA", "Gastrectomia / cirurgia bariátrica.", DEFINITIVA, "Gastrectomia ou cirurgia bariátrica é impedimento definitivo na regra atual.", None),
 1189 |             ("HERNIOPLASTIA", "Hernioplastia.", TEMPORARIA, "Aguarde três meses.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
 1190 |             ("HISTERECTOMIA", "Histerectomia.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1191 |             ("LAMINECTOMIA", "Laminectomia.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1192 |             ("LIPOASPIRACAO", "Lipoaspiração.", TEMPORARIA, "Aguarde seis meses.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1193 |             ("LITOTRIPSIA", "Litotripsia a laser.", TEMPORARIA, "Aguarde 30 dias.", {"valor": 30, "unidade": "dias", "referencia": "evento"}),
 1194 |             ("LOBECTOMIA", "Lobectomia pulmonar.", DEFINITIVA, "Lobectomia pulmonar é impedimento definitivo.", None),
 1195 |             ("NEFRECTOMIA_DOENCA", "Nefrectomia por doença.", DEFINITIVA, "Nefrectomia por doença é impedimento definitivo.", None),
 1196 |             ("NEFRECTOMIA_OUTRA", "Nefrectomia pós-trauma/doação/malformação.", TEMPORARIA, "Aguarde seis meses e confirme função renal.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1197 |             ("PNEUMONECTOMIA", "Pneumonectomia.", DEFINITIVA, "Pneumonectomia é impedimento definitivo.", None),
 1198 |             ("ANEURISMA", "Ressecção de aneurisma.", TEMPORARIA, "Aguarde 12 meses se não houver aneurisma remanescente.", {"valor": 12, "unidade": "meses", "referencia": "evento"}),
 1199 |             ("SIMPATECTOMIA", "Simpatectomia.", TEMPORARIA, "Aguarde um ano.", {"valor": 1, "unidade": "anos", "referencia": "evento"}),
 1200 |             ("TRANSPLANTE_CORNEA", "Transplante de córnea/dura-máter.", DEFINITIVA, "Este transplante é impedimento definitivo.", None),
 1201 |             ("TRANSPLANTE_ORGAO", "Transplante de órgão.", AVALIACAO, "Após um ano, doença e medicações ainda exigem avaliação.", None),
 1202 |             ("XENOTRANSPLANTE", "Xenotransplante de material vivo.", DEFINITIVA, "Há impedimento por tempo indeterminado na regra atual.", None),
 1203 |             ("MATERIAL_ANIMAL_NAO_VIVO", "Material animal não vivo.", AVALIACAO, "Pode ser aceito após um ano, conforme avaliação.", None),
 1204 |             ("OUTRA", "Outra cirurgia/procedimento não listado.", AVALIACAO, "O procedimento precisa de avaliação específica.", None),
 1205 |             ("NENHUMA", "Nenhuma cirurgia/procedimento relevante.", None, "", None),
 1206 |         ],
 1207 |         fonte="Manual Elo, seção 8.2; ref. [1]",
 1208 |     ),
 1209 |     "EXT-28": pergunta(
 1210 |         "EXT-28", "Histórico de câncer", "Você já teve diagnóstico de câncer maligno?",
 1211 |         "A regra geral possui exceções específicas e não se aplica automaticamente a tumores benignos.",
 1212 |         [("NAO", "Não."), ("COLO_IN_SITU", "Carcinoma in situ do colo do útero."), ("BASOCELULAR", "Carcinoma basocelular da pele."), ("OUTRO_MALIGNO", "Outro câncer maligno."), ("BENIGNO", "Tumor benigno / não maligno."), ("NAO_SEI", "Não sei se era benigno ou maligno.")],
 1213 |         regras={
 1214 |             "COLO_IN_SITU": regra(AVALIACAO, "A exceção exige avaliar tratamento, cirurgia e recuperação."),
 1215 |             "BASOCELULAR": regra(AVALIACAO, "A exceção exige avaliar tratamento, cirurgia e recuperação."),
 1216 |             "OUTRO_MALIGNO": regra(DEFINITIVA, "Outro câncer maligno é impedimento definitivo na regra consultada."),
 1217 |             "BENIGNO": regra(AVALIACAO, "O procedimento e a investigação do tumor benigno devem ser considerados."),
 1218 |             "NAO_SEI": regra(AVALIACAO, "O tipo do tumor precisa ser confirmado."),
 1219 |         },
 1220 |         fonte="Manual Elo, seção 9.1; ref. [1]",
 1221 |     ),
 1222 |     "EXT-29": pergunta_tabela(
 1223 |         "EXT-29", "Doenças da pele", "Você tem ou já teve alguma destas doenças da pele?",
 1224 |         "Nos detalhes, informe se está ativa, se atinge o local da punção e quais medicamentos usa.",
 1225 |         [
 1226 |             ("ABSCESSO", "Abscesso cutâneo.", TEMPORARIA, "Aguarde tratamento e cura.", None),
 1227 |             ("ECZEMA", "Eczema alérgico.", AVALIACAO, "Atividade, causa ocupacional e tratamento precisam ser avaliados.", None),
 1228 |             ("ERISIPELA", "Erisipela.", TEMPORARIA, "Aguarde cura e definição clínica do prazo.", None),
 1229 |             ("ERITEMA_NODOSO_INFECCIOSO", "Eritema nodoso infeccioso.", TEMPORARIA, "Aguarde três meses após cura.", {"valor": 3, "unidade": "meses", "referencia": "evento"}),
 1230 |             ("ERITEMA_NODOSO_NAO_INFECCIOSO", "Eritema nodoso não infeccioso.", AVALIACAO, "Aguarde seis meses e avalie a doença de base.", None),
 1231 |             ("ERITEMA_MEDICAMENTOSO", "Eritema polimorfo medicamentoso.", TEMPORARIA, "Aguarde seis meses após cura.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1232 |             ("ERITRODERMIA", "Eritrodermia.", TEMPORARIA, "Aguarde seis meses após cura.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1233 |             ("GANGRENA", "Gangrena.", AVALIACAO, "Aguarde pelo menos seis meses e avalie a doença de base.", None),
 1234 |             ("LESAO_PUNCAO", "Lesão no local da punção.", TEMPORARIA, "Aguarde a cura completa.", None),
 1235 |             ("LIQUEN", "Líquen plano.", TEMPORARIA, "Aguarde seis meses após cura.", {"valor": 6, "unidade": "meses", "referencia": "evento"}),
 1236 |             ("LUPUS_DISCOIDE", "Lúpus discoide.", AVALIACAO, "O controle clínico deve ser avaliado.", None),
 1237 |             ("MICOSE", "Micose superficial.", AVALIACAO, "Pode ser aceita se não atingir o local da punção.", None),
 1238 |             ("PENFIGO", "Pênfigo.", DEFINITIVA, "Pênfigo é impedimento definitivo.", None),
 1239 |             ("PSORIASE_LIMITADA", "Psoríase limitada à pele.", AVALIACAO, "Extensão, local da punção e medicamento precisam ser avaliados.", None),
 1240 |             ("PSORIASE_EXTENSA", "Psoríase extensa/sistêmica.", DEFINITIVA, "Psoríase extensa ou sistêmica é impedimento definitivo.", None),
 1241 |             ("PITIRIASE_ROSEA", "Pitiríase rósea.", None, "", None),
 1242 |             ("PITIRIASE_VERSICOLOR", "Pitiríase versicolor.", AVALIACAO, "Pode ser aceita se não atingir o local da punção.", None),
 1243 |             ("ULCERA_ARTERIAL", "Úlcera arterial.", DEFINITIVA, "Úlcera arterial é impedimento definitivo.", None),
 1244 |             ("VERRUGA", "Verruga comum.", None, "", None),
 1245 |             ("VITILIGO", "Vitiligo.", None, "", None),
 1246 |             ("OUTRA", "Outra doença de pele / não sei.", AVALIACAO, "Condição não listada ou incerta exige avaliação.", None),
 1247 |             ("NENHUMA", "Nenhuma.", None, "", None),
 1248 |         ],
 1249 |         fonte="Manual Elo, seção 9.2; ref. [1]",
 1250 |     ),
 1251 |     "EXT-30": pergunta_tabela(
 1252 |         "EXT-30", "Endócrinas e metabólicas", "Você tem algum destes diagnósticos hormonais, de tireoide, diabetes ou metabolismo?",
 1253 |         "Marque somente diagnósticos confirmados por profissional.",
 1254 |         [
 1255 |             ("ADENOMA_HIPOFISE", "Adenoma de hipófise.", AVALIACAO, "Controle, complicações e uso de GH precisam ser avaliados.", None),
 1256 |             ("BOCIO", "Bócio eutireoidiano.", None, "", None),
 1257 |             ("DIABETES_INSIPIDUS", "Diabetes insipidus.", DEFINITIVA, "Diabetes insipidus é impedimento definitivo.", None),
 1258 |             ("DIABETES_INSULINA", "Diabetes mellitus com insulina.", DEFINITIVA, "Diabetes com uso de insulina é impedimento definitivo na regra atual.", None),
 1259 |             ("DIABETES_TIPO2", "Diabetes tipo 2 sem insulina.", AVALIACAO, "Controle, rim, coração, medicamentos e relatório devem ser avaliados.", None),
 1260 |             ("DISLIPIDEMIA", "Dislipidemia.", AVALIACAO, "Pode ser aceita após controle.", None),
 1261 |             ("HIPERLIPIDEMIA_FAMILIAR", "Hiperlipidemia familiar.", DEFINITIVA, "Hiperlipidemia familiar é impedimento definitivo.", None),
 1262 |             ("FEOCROMOCITOMA", "Feocromocitoma.", DEFINITIVA, "Feocromocitoma é impedimento definitivo.", None),
 1263 |             ("HIPERALDOSTERONISMO", "Hiperaldosteronismo.", DEFINITIVA, "Hiperaldosteronismo é impedimento definitivo.", None),
 1264 |             ("HIPERPROLACTINEMIA", "Hiperprolactinemia.", AVALIACAO, "A causa precisa ser confirmada como benigna.", None),
 1265 |             ("HIPERTIREOIDISMO", "Hipertireoidismo.", DEFINITIVA, "Hipertireoidismo é impedimento definitivo.", None),
 1266 |             ("HIPOGLICEMIA", "Hipoglicemia.", AVALIACAO, "Pode ser aceita se estiver assintomático(a).", None),
 1267 |             ("HIPOPITUITARISMO", "Hipopituitarismo.", DEFINITIVA, "Hipopituitarismo é impedimento definitivo.", None),
 1268 |             ("HIPOTIREOIDISMO", "Hipotireoidismo / Hashimoto.", AVALIACAO, "Controle e eventual relatório precisam ser avaliados.", None),
 1269 |             ("INSUFICIENCIA_SUPRARRENAL", "Insuficiência suprarrenal.", DEFINITIVA, "Insuficiência suprarrenal é impedimento definitivo.", None),
 1270 |             ("PRE_DIABETES", "Intolerância à glicose / pré-diabetes.", None, "", None),
 1271 |             ("OBESIDADE_30_39", "Obesidade com IMC 30 a menor que 40.", AVALIACAO, "Comorbidades devem ser consideradas.", None),
 1272 |             ("OBESIDADE_40", "Obesidade com IMC igual ou maior que 40.", AVALIACAO, "Exige avaliação presencial e de comorbidades.", None),
 1273 |             ("NENHUMA", "Nenhuma.", None, "", None),
 1274 |             ("OUTRA", "Outra / não sei o diagnóstico.", AVALIACAO, "Condição não listada ou incerta exige avaliação.", None),
 1275 |         ],
 1276 |         fonte="Manual Elo, seção 10.1; ref. [1]",
 1277 |     ),
 1278 | })
``````

## accounts/triagem_catalogo_simplificada.py

Original: [accounts/triagem_catalogo_simplificada.py](<C:/Users/lb119/Elo/accounts/triagem_catalogo_simplificada.py>).

``````text
    1 | """Catálogo da triagem simplificada para quem já concluiu a extensa."""
    2 | 
    3 | from .triagem_catalogo_extensa import (
    4 |     AVALIACAO,
    5 |     PERGUNTAS_EXTENSAS,
    6 |     pergunta,
    7 |     regra,
    8 | )
    9 | 
   10 | 
   11 | def pergunta_simplificada(
   12 |     id_pergunta,
   13 |     titulo,
   14 |     texto,
   15 |     explicacao,
   16 |     opcoes,
   17 |     *,
   18 |     abrir_extensa=None,
   19 |     multipla=False,
   20 |     regras=None,
   21 |     fonte="Manual Elo, seção 18",
   22 | ):
   23 |     """Monta uma pergunta rápida e registra os aprofundamentos necessários."""
   24 | 
   25 |     item = pergunta(
   26 |         id_pergunta,
   27 |         titulo,
   28 |         texto,
   29 |         explicacao,
   30 |         opcoes,
   31 |         multipla=multipla,
   32 |         regras=regras,
   33 |         fonte=fonte,
   34 |     )
   35 |     item["abrir_extensa"] = abrir_extensa or {}
   36 |     return item
   37 | 
   38 | 
   39 | # A lista completa é usada quando a resposta invalida o resumo anterior.
   40 | TODAS_AS_EXTENSAS = list(PERGUNTAS_EXTENSAS)
   41 | 
   42 | 
   43 | PERGUNTAS_SIMPLIFICADAS = {
   44 |     "SIM-01": pergunta_simplificada(
   45 |         "SIM-01", "Pode usar a versão rápida?",
   46 |         "Você já fez a triagem extensa no Elo e consegue ver um resumo do seu histórico salvo?",
   47 |         "A triagem simplificada verifica mudanças e não cria um cadastro médico do zero.",
   48 |         [("CORRETO", "Sim, e o resumo continua correto."), ("INCORRETO", "Sim, mas algo antigo está errado/incompleto."), ("NAO_FIZ", "Não fiz a triagem extensa."), ("NAO_SEI", "Não tenho certeza.")],
   49 |         abrir_extensa={
   50 |             "INCORRETO": TODAS_AS_EXTENSAS,
   51 |             "NAO_FIZ": TODAS_AS_EXTENSAS,
   52 |             "NAO_SEI": TODAS_AS_EXTENSAS,
   53 |         },
   54 |         fonte="Manual Elo, seção 18.3; regra de segurança do projeto",
   55 |     ),
   56 |     "SIM-02": pergunta_simplificada(
   57 |         "SIM-02", "Idade, peso e última doação",
   58 |         "Desde a última triagem, houve mudança que afete idade, peso ou intervalo de doação?",
   59 |         "O intervalo desde a última doação sempre precisa usar dados atuais.",
   60 |         [("NAO", "Não; continuo na faixa e peso previstos e não doei desde então."), ("DOOU", "Doei sangue depois da última triagem."), ("PESO", "Meu peso ficou abaixo/próximo de 50 kg ou perdi muito peso."), ("IDADE", "Completei 61 ou 70 anos / mudei de faixa relevante."), ("NAO_SEI", "Não sei.")],
   61 |         abrir_extensa={
   62 |             "DOOU": ["EXT-04", "EXT-05", "EXT-05A", "EXT-05B"],
   63 |             "PESO": ["EXT-03", "EXT-18"],
   64 |             "IDADE": ["EXT-02", "EXT-06", "EXT-07"],
   65 |             "NAO_SEI": ["EXT-02", "EXT-03", "EXT-04", "EXT-05", "EXT-05A", "EXT-05B", "EXT-06", "EXT-07", "EXT-18"],
   66 |         },
   67 |         fonte="Manual Elo, seções 3, 4 e 18",
   68 |     ),
   69 |     "SIM-03": pergunta_simplificada(
   70 |         "SIM-03", "Como você está hoje?",
   71 |         "Hoje você está se sentindo totalmente bem, sem febre, gripe, COVID, diarreia, infecção ou mal-estar?",
   72 |         "Esta é a principal checagem do estado atual.",
   73 |         [("SIM", "Sim."), ("NAO", "Não, tive sintoma ou doença recente."), ("NAO_SEI", "Não tenho certeza.")],
   74 |         abrir_extensa={
   75 |             "NAO": ["EXT-08", "EXT-11", "EXT-11A", "EXT-12", "EXT-13", "EXT-14", "EXT-15", "EXT-16", "EXT-18", "EXT-41"],
   76 |             "NAO_SEI": ["EXT-08", "EXT-11", "EXT-11A", "EXT-12", "EXT-13", "EXT-14", "EXT-15", "EXT-16", "EXT-18", "EXT-41"],
   77 |         },
   78 |         fonte="Manual Elo, seções 3, 6 e 13",
   79 |     ),
   80 |     "SIM-04": pergunta_simplificada(
   81 |         "SIM-04", "Sono, alimentação e álcool",
   82 |         "Hoje você dormiu pelo menos quatro horas, não está em jejum e respeitou o intervalo após bebida ou refeição gordurosa?",
   83 |         "Esses fatores mudam de um dia para o outro e nunca são reutilizados.",
   84 |         [("SIM", "Sim, todas as três condições estão adequadas."), ("SONO", "Não dormi o suficiente."), ("ALIMENTACAO", "Estou em jejum / comi muito recentemente."), ("ALCOOL", "Bebi álcool recentemente."), ("NAO_SEI", "Não sei.")],
   85 |         multipla=True,
   86 |         abrir_extensa={
   87 |             "SONO": ["EXT-09"],
   88 |             "ALIMENTACAO": ["EXT-10"],
   89 |             "ALCOOL": ["EXT-44"],
   90 |             "NAO_SEI": ["EXT-09", "EXT-10", "EXT-44"],
   91 |         },
   92 |         fonte="Manual Elo, seções 3 e 15.1",
   93 |     ),
   94 |     "SIM-05": pergunta_simplificada(
   95 |         "SIM-05", "Gravidez, pós-parto ou amamentação",
   96 |         "Desde a última triagem, houve gravidez, parto, aborto, amamentação ou atraso menstrual com possibilidade de gravidez?",
   97 |         "Essas situações possuem prazos diferentes e precisam do bloco completo.",
   98 |         [("NAO", "Não."), ("SIM", "Sim."), ("NAO_SEI", "Não sei / prefiro responder na completa.")],
   99 |         abrir_extensa={"SIM": ["EXT-33"], "NAO_SEI": ["EXT-33"]},
  100 |         fonte="Manual Elo, seção 11.2",
  101 |     ),
  102 |     "SIM-06": pergunta_simplificada(
  103 |         "SIM-06", "Novo diagnóstico ou internação",
  104 |         "Desde a última triagem, você recebeu diagnóstico novo, foi internado(a), passou por emergência ou iniciou investigação médica importante?",
  105 |         "Uma condição nova pode mudar a orientação mesmo quando você se sente bem.",
  106 |         [("NAO", "Não."), ("SIM", "Sim, tive diagnóstico/internação."), ("INVESTIGANDO", "Estou investigando algo e ainda não tenho diagnóstico.")],
  107 |         abrir_extensa={
  108 |             "SIM": ["EXT-20", "EXT-27", "EXT-28", "EXT-29", "EXT-30", "EXT-31", "EXT-32", "EXT-34", "EXT-35", "EXT-36", "EXT-37", "EXT-38", "EXT-39", "EXT-40", "EXT-46", "EXT-47", "EXT-50"],
  109 |             "INVESTIGANDO": ["EXT-20", "EXT-27", "EXT-28", "EXT-29", "EXT-30", "EXT-31", "EXT-32", "EXT-34", "EXT-35", "EXT-36", "EXT-37", "EXT-38", "EXT-39", "EXT-40", "EXT-46", "EXT-47", "EXT-50"],
  110 |         },
  111 |         regras={"INVESTIGANDO": regra(AVALIACAO, "Uma investigação ainda sem diagnóstico exige avaliação presencial.")},
  112 |         fonte="Manual Elo, seções 1.2 e 18",
  113 |     ),
  114 |     "SIM-07": pergunta_simplificada(
  115 |         "SIM-07", "Infecções recentes",
  116 |         "Depois da última triagem, você teve COVID, influenza, dengue, chikungunya, Oropouche, mononucleose, hepatite, IST ou outra infecção?",
  117 |         "Os prazos variam de dias a impedimento definitivo.",
  118 |         [("NAO", "Não."), ("SIM", "Sim."), ("NAO_SEI", "Não sei qual infecção tive.")],
  119 |         abrir_extensa={"SIM": ["EXT-12", "EXT-13", "EXT-14", "EXT-41", "EXT-42"], "NAO_SEI": ["EXT-12", "EXT-13", "EXT-14", "EXT-41", "EXT-42"]},
  120 |         fonte="Manual Elo, seções 6 e 13",
  121 |     ),
  122 |     "SIM-08": pergunta_simplificada(
  123 |         "SIM-08", "Medicamentos novos ou alterados",
  124 |         "Desde a última triagem, você começou, terminou, trocou ou aumentou a dose de algum medicamento?",
  125 |         "Nunca interrompa medicamento para tentar doar.",
  126 |         [("NAO", "Não."), ("SIM", "Sim."), ("NAO_SEI", "Não sei o nome / não lembro.")],
  127 |         abrir_extensa={"SIM": ["EXT-46", "EXT-47"], "NAO_SEI": ["EXT-46", "EXT-47"]},
  128 |         regras={"NAO_SEI": regra(AVALIACAO, "O medicamento precisa ser identificado presencialmente.")},
  129 |         fonte="Manual Elo, seção 15; refs. [1], [4], [8], [9]",
  130 |     ),
  131 |     "SIM-09": pergunta_simplificada(
  132 |         "SIM-09", "Vacina recente", "Você tomou alguma vacina desde a última triagem?",
  133 |         "As vacinas têm prazos diferentes conforme o tipo.",
  134 |         [("NAO", "Não."), ("SIM", "Sim."), ("NAO_SEI", "Não lembro / não sei qual vacina.")],
  135 |         abrir_extensa={"SIM": ["EXT-48"], "NAO_SEI": ["EXT-48"]},
  136 |         regras={"NAO_SEI": regra(AVALIACAO, "Verifique a carteira de vacinação ou confirme presencialmente.")},
  137 |         fonte="Manual Elo, seção 16",
  138 |     ),
  139 |     "SIM-10": pergunta_simplificada(
  140 |         "SIM-10", "Tatuagem, piercing, acupuntura ou estética",
  141 |         "Desde a última triagem, você fez tatuagem, piercing, acupuntura, microagulhamento, botox, preenchimento ou outro procedimento com perfuração?",
  142 |         "O prazo muda conforme tipo, data e segurança.",
  143 |         [("NAO", "Não."), ("SIM", "Sim."), ("NAO_SEI", "Não sei se o procedimento conta.")],
  144 |         abrir_extensa={"SIM": ["EXT-21", "EXT-22", "EXT-23", "EXT-24"], "NAO_SEI": ["EXT-21", "EXT-22", "EXT-23", "EXT-24"]},
  145 |         fonte="Manual Elo, seção 7",
  146 |     ),
  147 |     "SIM-11": pergunta_simplificada(
  148 |         "SIM-11", "Endoscopia, dentista ou cirurgia",
  149 |         "Desde a última triagem, você fez endoscopia, tratamento dentário, cirurgia ou outro procedimento médico invasivo?",
  150 |         "Cada procedimento tem prazo próprio e pode exigir avaliação da doença que o motivou.",
  151 |         [("NAO", "Não."), ("DENTARIO", "Sim, dentário."), ("ENDOSCOPIA", "Sim, endoscopia/laparoscopia."), ("CIRURGIA", "Sim, cirurgia/procedimento médico."), ("NAO_SEI", "Não sei classificar.")],
  152 |         abrir_extensa={"DENTARIO": ["EXT-26"], "ENDOSCOPIA": ["EXT-25"], "CIRURGIA": ["EXT-27"], "NAO_SEI": ["EXT-25", "EXT-26", "EXT-27"]},
  153 |         fonte="Manual Elo, seções 7 e 8",
  154 |     ),
  155 |     "SIM-12": pergunta_simplificada(
  156 |         "SIM-12", "Feridas, alergia ou reação importante",
  157 |         "Hoje você tem ferida aberta/pontos, alergia ativa ou teve anafilaxia/reação grave desde a última triagem?",
  158 |         "Esses fatores podem impedir a doação ou exigir avaliação imediata.",
  159 |         [("NAO", "Não."), ("FERIDA", "Sim, ferida/pontos."), ("ALERGIA", "Sim, alergia ativa."), ("ANAFILAXIA", "Sim, tive anafilaxia ou reação grave."), ("NAO_SEI", "Não sei.")],
  160 |         abrir_extensa={"FERIDA": ["EXT-16"], "ALERGIA": ["EXT-15"], "ANAFILAXIA": ["EXT-15"], "NAO_SEI": ["EXT-15", "EXT-16"]},
  161 |         fonte="Manual Elo, seção 6",
  162 |     ),
  163 |     "SIM-13": pergunta_simplificada(
  164 |         "SIM-13", "Exposição a sangue ou situação de risco",
  165 |         "Desde a última triagem, aconteceu exposição a sangue/material biológico ou situação sexual/epidemiológica com risco aumentado?",
  166 |         "A resposta detalhada será feita em ambiente privado.",
  167 |         [("NAO", "Não."), ("SIM", "Sim."), ("PRESENCIAL", "Não quero responder nesta versão rápida / não sei.")],
  168 |         abrir_extensa={"SIM": ["EXT-43"]},
  169 |         regras={"PRESENCIAL": regra(AVALIACAO, "A situação será discutida em ambiente privado no hemocentro.")},
  170 |         fonte="Manual Elo, seção 14; ref. [7]",
  171 |     ),
  172 |     "SIM-14": pergunta_simplificada(
  173 |         "SIM-14", "Drogas", "Desde a última triagem, você usou maconha, cocaína, crack, droga injetável ou outra droga?",
  174 |         "A via e a substância mudam a regra.",
  175 |         [("NAO", "Não."), ("SIM", "Sim."), ("COMPLETA", "Prefiro responder na versão completa.")],
  176 |         abrir_extensa={"SIM": ["EXT-45"], "COMPLETA": ["EXT-45"]},
  177 |         fonte="Manual Elo, seção 15.1",
  178 |     ),
  179 |     "SIM-15": pergunta_simplificada(
  180 |         "SIM-15", "Viagem ou mudança de residência",
  181 |         "Desde a última triagem, você viajou ou morou em região com malária, chikungunya, Oeste do Nilo ou mudou histórico relevante no exterior?",
  182 |         "Áreas de risco podem mudar e precisam de atualização epidemiológica.",
  183 |         [("NAO", "Não."), ("SIM", "Sim."), ("NAO_SEI", "Não sei se a região era de risco.")],
  184 |         abrir_extensa={"SIM": ["EXT-49"], "NAO_SEI": ["EXT-49"]},
  185 |         fonte="Manual Elo, seção 17",
  186 |     ),
  187 |     "SIM-16": pergunta_simplificada(
  188 |         "SIM-16", "Mudança de peso ou saúde geral",
  189 |         "Desde a última triagem, você perdeu mais de 10% do peso, ficou desidratado(a) ou percebeu mudança importante na saúde?",
  190 |         "Perda importante de peso pode exigir espera ou investigação.",
  191 |         [("NAO", "Não."), ("SIM", "Sim."), ("NAO_SEI", "Não sei.")],
  192 |         abrir_extensa={"SIM": ["EXT-03", "EXT-11", "EXT-18", "EXT-50"], "NAO_SEI": ["EXT-03", "EXT-11", "EXT-18", "EXT-50"]},
  193 |         fonte="Manual Elo, seções 3 e 18",
  194 |     ),
  195 |     "SIM-17": pergunta_simplificada(
  196 |         "SIM-17", "Confirmação rápida",
  197 |         "Fora o que já foi perguntado, alguma informação da sua triagem extensa deixou de ser verdadeira ou ficou incompleta?",
  198 |         "Esta é uma barreira final contra reutilização indevida de informação antiga.",
  199 |         [("NAO", "Não, o restante continua correto."), ("SIM", "Sim."), ("NAO_SEI", "Não tenho certeza.")],
  200 |         abrir_extensa={"SIM": TODAS_AS_EXTENSAS, "NAO_SEI": TODAS_AS_EXTENSAS},
  201 |         fonte="Manual Elo, seção 18.3; regra de segurança do projeto",
  202 |     ),
  203 |     "SIM-18": pergunta_simplificada(
  204 |         "SIM-18", "Aceite do resultado orientativo",
  205 |         "Você entende que a versão rápida pode não detectar algo não informado e que ainda passará pela triagem presencial?",
  206 |         "A limitação da modalidade rápida deve ficar explícita.",
  207 |         [("ENTENDO", "Sim, entendo."), ("EXTENSA", "Quero fazer a triagem extensa em vez disso.")],
  208 |         abrir_extensa={"EXTENSA": TODAS_AS_EXTENSAS},
  209 |         fonte="Manual Elo, seções 1 e 18; regra de segurança do projeto",
  210 |     ),
  211 | }
``````

## accounts/triagem_forms.py

Original: [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py>).

``````text
    1 | # Este arquivo cria dinamicamente o formulário de cada pergunta da triagem.
    2 | 
    3 | # - Recebe uma pergunta do catálogo e monta os campos necessários.
    4 | # - Usa rádio para respostas únicas e checkbox para múltiplas respostas.
    5 | # - Reaproveita respostas anteriores quando a pergunta está sendo editada.
    6 | # - Cria campos de data para alternativas que exigem prazo.
    7 | # - Permite informar detalhes complementares.
    8 | # - Adiciona campos extras para segurança e inflamação quando necessários.
    9 | # - Impede combinações inválidas, como marcar "Nenhuma" junto com uma doença.
   10 | # - Exige datas e detalhes quando a alternativa selecionada precisar dessas informações.
   11 | # - Impede datas futuras.
   12 | # - Valida as condições de procedimentos e informações de segurança.
   13 | # - Organiza tudo no campo "valor", contendo códigos, datas, detalhes e dados complementares, para ser salvo pela camada de serviço.
   14 | 
   15 | # Este arquivo valida e organiza as respostas, mas não calcula o resultado médico da triagem. Essa responsabilidade pertence ao triagem_motor.py.
   16 | 
   17 | """Formulário dinâmico usado por todas as perguntas da triagem."""
   18 | 
   19 | from datetime import date
   20 | 
   21 | from django import forms
   22 | 
   23 | 
   24 | class FormularioPergunta(forms.Form):
   25 |     """Cria somente os campos necessários para uma pergunta do catálogo."""
   26 | 
   27 |     def __init__(self, pergunta, *args, **kwargs):
   28 |         self.pergunta = pergunta
   29 |         valor_inicial = kwargs.pop("valor_inicial", None) or {}
   30 |         super().__init__(*args, **kwargs)
   31 | 
   32 |         escolhas = [
   33 |             (opcao["codigo"], opcao["rotulo"])
   34 |             for opcao in pergunta["opcoes"]
   35 |         ]
   36 |         codigos_iniciais = valor_inicial.get("codigos") or []
   37 | 
   38 |         if pergunta["multipla"]:
   39 |             self.fields["resposta"] = forms.MultipleChoiceField(
   40 |                 label=pergunta["texto"],
   41 |                 choices=escolhas,
   42 |                 widget=forms.CheckboxSelectMultiple,
   43 |                 initial=codigos_iniciais,
   44 |             )
   45 |         else:
   46 |             self.fields["resposta"] = forms.ChoiceField(
   47 |                 label=pergunta["texto"],
   48 |                 choices=escolhas,
   49 |                 widget=forms.RadioSelect,
   50 |                 initial=(codigos_iniciais[0] if codigos_iniciais else None),
   51 |             )
   52 | 
   53 |         # Cada alternativa temporal recebe sua própria data.
   54 |         datas_iniciais = valor_inicial.get("datas") or {}
   55 |         rotulos = {
   56 |             opcao["codigo"]: opcao["rotulo"]
   57 |             for opcao in pergunta["opcoes"]
   58 |         }
   59 |         for codigo in pergunta["exige_data_para"]:
   60 |             self.fields[f"data_{codigo}"] = forms.DateField(
   61 |                 label=f"Data relacionada a: {rotulos[codigo]}",
   62 |                 required=False,
   63 |                 initial=datas_iniciais.get(codigo),
   64 |                 widget=forms.DateInput(attrs={"type": "date"}),
   65 |             )
   66 | 
   67 |         # O complemento permite explicar motivo, tratamento ou exceção.
   68 |         self.fields["detalhes"] = forms.CharField(
   69 |             label="Informações complementares",
   70 |             required=False,
   71 |             max_length=500,
   72 |             initial=valor_inicial.get("detalhes", ""),
   73 |             help_text=(
   74 |                 "Informe somente o necessário para esclarecer esta resposta."
   75 |             ),
   76 |             widget=forms.Textarea(attrs={"rows": 3}),
   77 |         )
   78 | 
   79 |         if pergunta["perguntar_seguranca"]:
   80 |             self.fields["seguranca"] = forms.ChoiceField(
   81 |                 label="As condições de higiene, antissepsia e material eram seguras?",
   82 |                 required=False,
   83 |                 choices=[
   84 |                     ("", "Selecione"),
   85 |                     ("SIM", "Sim."),
   86 |                     ("NAO", "Não."),
   87 |                     ("NAO_SEI", "Não sei confirmar."),
   88 |                 ],
   89 |                 initial=valor_inicial.get("seguranca", ""),
   90 |             )
   91 | 
   92 |         if pergunta["perguntar_inflamacao"]:
   93 |             self.fields["inflamacao"] = forms.ChoiceField(
   94 |                 label="Houve inflamação ou infecção depois do procedimento?",
   95 |                 required=False,
   96 |                 choices=[
   97 |                     ("", "Selecione"),
   98 |                     ("SIM", "Sim."),
   99 |                     ("NAO", "Não."),
  100 |                     ("NAO_SEI", "Não sei."),
  101 |                 ],
  102 |                 initial=valor_inicial.get("inflamacao", ""),
  103 |             )
  104 | 
  105 |     def clean(self):
  106 |         """Valida contradições e devolve um valor único para persistência."""
  107 | 
  108 |         dados = super().clean()
  109 |         resposta = dados.get("resposta")
  110 | 
  111 |         if self.pergunta["multipla"]:
  112 |             codigos = list(resposta or [])
  113 |         else:
  114 |             codigos = [resposta] if resposta else []
  115 | 
  116 |         # Alternativas negativas ou neutras não podem coexistir com doenças.
  117 |         exclusivos = {"NAO", "NENHUMA", "NENHUM", "SIM"}
  118 |         if len(codigos) > 1 and exclusivos.intersection(codigos):
  119 |             self.add_error(
  120 |                 "resposta",
  121 |                 "Escolha a alternativa neutra sozinha ou marque as condições.",
  122 |             )
  123 | 
  124 |         datas = {}
  125 |         for codigo in self.pergunta["exige_data_para"]:
  126 |             nome_campo = f"data_{codigo}"
  127 |             data_evento = dados.get(nome_campo)
  128 | 
  129 |             if codigo in codigos and not data_evento:
  130 |                 self.add_error(
  131 |                     nome_campo,
  132 |                     "Informe a data desta alternativa.",
  133 |                 )
  134 |             elif data_evento and data_evento > date.today():
  135 |                 self.add_error(
  136 |                     nome_campo,
  137 |                     "A data não pode estar no futuro.",
  138 |                 )
  139 |             elif codigo in codigos and data_evento:
  140 |                 datas[codigo] = data_evento.isoformat()
  141 | 
  142 |         detalhes = (dados.get("detalhes") or "").strip()
  143 |         if (
  144 |             set(codigos).intersection(
  145 |                 self.pergunta["exige_detalhes_para"]
  146 |             )
  147 |             and not detalhes
  148 |         ):
  149 |             self.add_error(
  150 |                 "detalhes",
  151 |                 "Descreva brevemente a situação informada.",
  152 |             )
  153 | 
  154 |         valor = {
  155 |             "codigos": codigos,
  156 |             "datas": datas,
  157 |             "detalhes": detalhes,
  158 |         }
  159 | 
  160 |         # Segurança e inflamação alteram o prazo do bloco de estética.
  161 |         for campo in ("seguranca", "inflamacao"):
  162 |             if campo not in self.fields:
  163 |                 continue
  164 | 
  165 |             resposta_extra = dados.get(campo) or ""
  166 |             marcou_procedimento = bool(
  167 |                 set(codigos) - {"NENHUM", "NENHUMA", "NAO"}
  168 |             )
  169 |             if marcou_procedimento and not resposta_extra:
  170 |                 self.add_error(
  171 |                     campo,
  172 |                     "Informe esta condição para o procedimento selecionado.",
  173 |                 )
  174 |             valor[campo] = resposta_extra
  175 | 
  176 |         dados["valor"] = valor
  177 |         return dados
``````

## accounts/triagem_motor.py

Original: [accounts/triagem_motor.py](<C:/Users/lb119/Elo/accounts/triagem_motor.py>).

``````text
    1 | #Este arquivo é o motor que calcula o resultado da triagem.
    2 | 
    3 | # - Recebe as respostas e não acessa diretamente o banco de dados.
    4 | # - Usa as regras declaradas no catálogo de perguntas.
    5 | # - Cria achados para cada condição identificada.
    6 | # - Calcula prazos em horas, dias, semanas, meses ou anos.
    7 | # - Solicita avaliação quando falta uma data necessária.
    8 | # - Aplica regras específicas de intervalo entre doações.
    9 | # - Verifica limites de doações nos últimos 12 meses.
   10 | # - Analisa procedimentos estéticos e prazos de segurança.
   11 | # - Na triagem simplificada, reutiliza somente respostas estáveis da extensa.
   12 | # - Mantém todos os achados encontrados.
   13 | # - Escolhe sempre o resultado mais restritivo.
   14 | # - Calcula a data de liberação mais distante, quando existir.
   15 | # - Retorna resultado, mensagem, achados, data e versão das regras.
   16 | 
   17 | # Este motor apenas calcula a orientação. O resultado não substitui a avaliação clínica final do Hemocentro.
   18 | 
   19 | """Motor puro que transforma respostas em orientação de triagem.
   20 | 
   21 | O módulo não acessa o banco. Isso torna os cálculos repetíveis e permite manter
   22 | o histórico antigo ligado à versão de regra que produziu cada resultado.
   23 | """
   24 | 
   25 | import calendar
   26 | import math
   27 | from datetime import date, datetime, timedelta
   28 | 
   29 | from .models import Triagem
   30 | from .triagem_catalogo import (
   31 |     TRIAGEM_RULE_VERSION,
   32 |     obter_pergunta,
   33 | )
   34 | 
   35 | 
   36 | # Um resultado mais restritivo sempre prevalece, mas nenhum achado é apagado.
   37 | PRIORIDADE_RESULTADOS = (
   38 |     Triagem.Resultado.DEFINITIVA,
   39 |     Triagem.Resultado.AVALIACAO,
   40 |     Triagem.Resultado.TEMPORARIA,
   41 |     Triagem.Resultado.DOCUMENTACAO,
   42 | )
   43 | 
   44 | 
   45 | # Estes dados mudam rapidamente e nunca são herdados pela versão simplificada.
   46 | PERGUNTAS_NAO_REUTILIZAVEIS = {
   47 |     "EXT-08",
   48 |     "EXT-09",
   49 |     "EXT-10",
   50 |     "EXT-11",
   51 |     "EXT-11A",
   52 |     "EXT-12",
   53 |     "EXT-13",
   54 |     "EXT-14",
   55 |     "EXT-15",
   56 |     "EXT-16",
   57 |     "EXT-17",
   58 |     "EXT-18",
   59 |     "EXT-19",
   60 |     "EXT-33",
   61 |     "EXT-44",
   62 | }
   63 | 
   64 | 
   65 | MENSAGENS_RESULTADO = {
   66 |     Triagem.Resultado.SEM_IMPEDIMENTO: (
   67 |         "Com base no que você informou, não identificamos um impedimento "
   68 |         "nesta orientação. Isso não significa liberação para doar: a decisão "
   69 |         "final será tomada pela equipe do hemocentro."
   70 |     ),
   71 |     Triagem.Resultado.TEMPORARIA: (
   72 |         "Encontramos uma condição com prazo de espera. A data apresentada é "
   73 |         "orientativa e só vale se você estiver recuperado(a) e não houver "
   74 |         "outro impedimento. A decisão final é do hemocentro."
   75 |     ),
   76 |     Triagem.Resultado.DEFINITIVA: (
   77 |         "Uma condição informada é classificada como impedimento definitivo "
   78 |         "pela regra consultada. Confirme a orientação com um serviço oficial, "
   79 |         "pois normas e diagnósticos podem precisar de atualização."
   80 |     ),
   81 |     Triagem.Resultado.AVALIACAO: (
   82 |         "Sua resposta depende de avaliação profissional, relatório, exame ou "
   83 |         "detalhe que o sistema não consegue confirmar com segurança. A decisão "
   84 |         "final será feita no hemocentro."
   85 |     ),
   86 |     Triagem.Resultado.DOCUMENTACAO: (
   87 |         "Existe uma exigência de documentação ou conferência presencial. Isso "
   88 |         "não substitui a avaliação clínica da equipe do hemocentro."
   89 |     ),
   90 | }
   91 | 
   92 | 
   93 | def escolher_resultado(achados):
   94 |     """Escolhe o estado principal sem descartar os demais achados."""
   95 | 
   96 |     encontrados = {achado["resultado"] for achado in achados}
   97 | 
   98 |     for resultado in PRIORIDADE_RESULTADOS:
   99 |         if resultado in encontrados:
  100 |             return resultado
  101 | 
  102 |     return Triagem.Resultado.SEM_IMPEDIMENTO
  103 | 
  104 | 
  105 | def _converter_data(valor):
  106 |     """Aceita data, datetime ou ISO; valor inválido volta como ausente."""
  107 | 
  108 |     if isinstance(valor, datetime):
  109 |         return valor.date()
  110 |     if isinstance(valor, date):
  111 |         return valor
  112 |     if not valor:
  113 |         return None
  114 | 
  115 |     try:
  116 |         return date.fromisoformat(str(valor))
  117 |     except ValueError:
  118 |         return None
  119 | 
  120 | 
  121 | def _somar_meses(data_base, quantidade):
  122 |     """Soma meses pelo calendário e ajusta dias como 31 de janeiro."""
  123 | 
  124 |     indice_mes = data_base.month - 1 + quantidade
  125 |     ano = data_base.year + indice_mes // 12
  126 |     mes = indice_mes % 12 + 1
  127 |     ultimo_dia = calendar.monthrange(ano, mes)[1]
  128 |     return date(ano, mes, min(data_base.day, ultimo_dia))
  129 | 
  130 | 
  131 | def calcular_data_liberacao(data_base, prazo):
  132 |     """Calcula a data final para horas, dias, semanas, meses ou anos."""
  133 | 
  134 |     unidade = prazo["unidade"]
  135 |     quantidade = prazo["valor"]
  136 | 
  137 |     if unidade == "horas":
  138 |         # Como o model guarda uma data, qualquer fração de dia é conservadora.
  139 |         return data_base + timedelta(days=math.ceil(quantidade / 24))
  140 |     if unidade == "dias":
  141 |         return data_base + timedelta(days=quantidade)
  142 |     if unidade == "semanas":
  143 |         return data_base + timedelta(weeks=quantidade)
  144 |     if unidade == "meses":
  145 |         return _somar_meses(data_base, quantidade)
  146 |     if unidade == "anos":
  147 |         return _somar_meses(data_base, quantidade * 12)
  148 | 
  149 |     raise ValueError(f"Unidade de prazo inválida: {unidade}")
  150 | 
  151 | 
  152 | def _data_da_resposta(valor, codigo):
  153 |     """Obtém a data específica da alternativa ou a data legada da resposta."""
  154 | 
  155 |     datas = valor.get("datas") or {}
  156 |     return _converter_data(
  157 |         datas.get(codigo) or valor.get("data_evento")
  158 |     )
  159 | 
  160 | 
  161 | def _novo_achado(
  162 |     pergunta,
  163 |     codigo,
  164 |     resultado,
  165 |     mensagem,
  166 |     *,
  167 |     data_liberacao=None,
  168 |     exige_relatorio=False,
  169 | ):
  170 |     """Padroniza a estrutura persistida no campo JSON de achados."""
  171 | 
  172 |     achado = {
  173 |         "id_pergunta": pergunta["id"],
  174 |         "codigo_regra": f"{pergunta['id']}:{codigo}",
  175 |         "categoria": pergunta["titulo"],
  176 |         "resultado": resultado,
  177 |         "mensagem": mensagem,
  178 |         "exige_relatorio": exige_relatorio,
  179 |         "fonte": pergunta["fonte"],
  180 |         "regra_version": TRIAGEM_RULE_VERSION,
  181 |     }
  182 | 
  183 |     if data_liberacao:
  184 |         achado["data_liberacao"] = data_liberacao.isoformat()
  185 | 
  186 |     return achado
  187 | 
  188 | 
  189 | def _avaliar_regra_declarada(pergunta, codigo, valor, hoje):
  190 |     """Avalia uma alternativa simples definida diretamente no catálogo."""
  191 | 
  192 |     item_regra = pergunta["regras"].get(codigo)
  193 |     if not item_regra:
  194 |         return None
  195 | 
  196 |     resultado = item_regra["resultado"]
  197 |     mensagem = item_regra["mensagem"]
  198 |     prazo = item_regra.get("prazo")
  199 |     data_final = None
  200 | 
  201 |     if prazo:
  202 |         if prazo.get("referencia") == "hoje":
  203 |             data_base = hoje
  204 |         else:
  205 |             data_base = _data_da_resposta(valor, codigo)
  206 | 
  207 |         # Prazos após cura, dose, alta ou procedimento precisam da data real.
  208 |         if data_base is None:
  209 |             return _novo_achado(
  210 |                 pergunta,
  211 |                 f"{codigo}_SEM_DATA",
  212 |                 Triagem.Resultado.AVALIACAO,
  213 |                 "Informe a data do evento ou confirme o prazo presencialmente.",
  214 |             )
  215 | 
  216 |         data_final = calcular_data_liberacao(data_base, prazo)
  217 | 
  218 |         # Um prazo já encerrado não é impedimento atual.
  219 |         if (
  220 |             resultado == Triagem.Resultado.TEMPORARIA
  221 |             and data_final <= hoje
  222 |         ):
  223 |             return None
  224 | 
  225 |     return _novo_achado(
  226 |         pergunta,
  227 |         codigo,
  228 |         resultado,
  229 |         mensagem,
  230 |         data_liberacao=data_final,
  231 |         exige_relatorio=item_regra.get("exige_relatorio", False),
  232 |     )
  233 | 
  234 | 
  235 | def _primeiro_codigo(respostas, id_pergunta):
  236 |     """Retorna a primeira alternativa quando a pergunta é de escolha única."""
  237 | 
  238 |     valor = respostas.get(id_pergunta) or {}
  239 |     codigos = valor.get("codigos") or []
  240 |     return codigos[0] if codigos else None
  241 | 
  242 | 
  243 | def _avaliar_intervalo_ultima_doacao(respostas, hoje):
  244 |     """Aplica 60/90 dias e a regra adicional de seis meses após os 60."""
  245 | 
  246 |     valor = respostas.get("EXT-05A") or {}
  247 |     if "DATA" not in (valor.get("codigos") or []):
  248 |         return None
  249 | 
  250 |     pergunta = obter_pergunta("EXT-05A")
  251 |     data_doacao = _data_da_resposta(valor, "DATA")
  252 |     if data_doacao is None:
  253 |         return _novo_achado(
  254 |             pergunta,
  255 |             "INTERVALO_SEM_DATA",
  256 |             Triagem.Resultado.AVALIACAO,
  257 |             "A data da última doação é necessária para calcular o intervalo.",
  258 |         )
  259 | 
  260 |     sexo = _primeiro_codigo(respostas, "EXT-04")
  261 |     idade = _primeiro_codigo(respostas, "EXT-02")
  262 |     datas = []
  263 | 
  264 |     if sexo == "FEMININO":
  265 |         datas.append(data_doacao + timedelta(days=90))
  266 |     elif sexo == "MASCULINO":
  267 |         datas.append(data_doacao + timedelta(days=60))
  268 | 
  269 |     if idade == "61_69":
  270 |         datas.append(_somar_meses(data_doacao, 6))
  271 | 
  272 |     if not datas:
  273 |         return None
  274 | 
  275 |     data_final = max(datas)
  276 |     if data_final <= hoje:
  277 |         return None
  278 | 
  279 |     return _novo_achado(
  280 |         pergunta,
  281 |         "INTERVALO_DOACAO",
  282 |         Triagem.Resultado.TEMPORARIA,
  283 |         "Ainda não terminou o intervalo orientativo desde a última doação.",
  284 |         data_liberacao=data_final,
  285 |     )
  286 | 
  287 | 
  288 | def _avaliar_limite_doacoes(respostas):
  289 |     """Sem datas históricas, sinaliza o limite sem inventar uma liberação."""
  290 | 
  291 |     codigo = _primeiro_codigo(respostas, "EXT-05B")
  292 |     sexo = _primeiro_codigo(respostas, "EXT-04")
  293 | 
  294 |     quantidades = {
  295 |         "0": 0,
  296 |         "1": 1,
  297 |         "2": 2,
  298 |         "3": 3,
  299 |         "4_MAIS": 4,
  300 |     }
  301 |     quantidade = quantidades.get(codigo)
  302 |     atingiu_limite = (
  303 |         quantidade is not None
  304 |         and (
  305 |             (sexo == "FEMININO" and quantidade >= 3)
  306 |             or (sexo == "MASCULINO" and quantidade >= 4)
  307 |         )
  308 |     )
  309 | 
  310 |     if not atingiu_limite:
  311 |         return None
  312 | 
  313 |     pergunta = obter_pergunta("EXT-05B")
  314 |     return _novo_achado(
  315 |         pergunta,
  316 |         "LIMITE_ANUAL_SEM_DATAS",
  317 |         Triagem.Resultado.AVALIACAO,
  318 |         "O limite anual foi alcançado; as datas históricas precisam ser conferidas.",
  319 |     )
  320 | 
  321 | 
  322 | def _avaliar_seguranca_estetica(respostas, hoje):
  323 |     """Aplica 12 meses quando a segurança estética não é comprovada."""
  324 | 
  325 |     valor = respostas.get("EXT-24") or {}
  326 |     codigos = set(valor.get("codigos") or []) - {"NENHUM"}
  327 |     if not codigos:
  328 |         return []
  329 | 
  330 |     pergunta = obter_pergunta("EXT-24")
  331 |     achados = []
  332 | 
  333 |     if valor.get("inflamacao") in {"SIM", "NAO_SEI"}:
  334 |         achados.append(
  335 |             _novo_achado(
  336 |                 pergunta,
  337 |                 "COM_INFLAMACAO",
  338 |                 Triagem.Resultado.AVALIACAO,
  339 |                 "Inflamação ou infecção precisa estar curada e ser avaliada.",
  340 |             )
  341 |         )
  342 | 
  343 |     seguranca = valor.get("seguranca")
  344 |     if seguranca == "SIM":
  345 |         return achados
  346 | 
  347 |     for codigo in codigos:
  348 |         data_evento = _data_da_resposta(valor, codigo)
  349 |         if data_evento is None:
  350 |             achados.append(
  351 |                 _novo_achado(
  352 |                     pergunta,
  353 |                     f"{codigo}_SEGURANCA_SEM_DATA",
  354 |                     Triagem.Resultado.AVALIACAO,
  355 |                     "Sem comprovação de segurança, informe a data ou confirme presencialmente.",
  356 |                 )
  357 |             )
  358 |             continue
  359 | 
  360 |         data_final = _somar_meses(data_evento, 12)
  361 |         if data_final > hoje:
  362 |             achados.append(
  363 |                 _novo_achado(
  364 |                     pergunta,
  365 |                     f"{codigo}_SEM_SEGURANCA",
  366 |                     Triagem.Resultado.TEMPORARIA,
  367 |                     "Sem comprovação de antissepsia ou material, aguarde 12 meses.",
  368 |                     data_liberacao=data_final,
  369 |                 )
  370 |             )
  371 | 
  372 |     return achados
  373 | 
  374 | 
  375 | def _respostas_para_avaliar(modalidade, respostas, respostas_base):
  376 |     """Combina somente dados estáveis da extensa com a checagem rápida."""
  377 | 
  378 |     if modalidade != Triagem.Modalidade.SIMPLIFICADA:
  379 |         return dict(respostas)
  380 | 
  381 |     combinadas = {
  382 |         id_pergunta: valor
  383 |         for id_pergunta, valor in (respostas_base or {}).items()
  384 |         if id_pergunta not in PERGUNTAS_NAO_REUTILIZAVEIS
  385 |     }
  386 |     combinadas.update(respostas)
  387 |     return combinadas
  388 | 
  389 | 
  390 | def avaliar_triagem(
  391 |     modalidade,
  392 |     respostas,
  393 |     *,
  394 |     hoje=None,
  395 |     respostas_base=None,
  396 | ):
  397 |     """Avalia todas as respostas e devolve resultado, mensagem e achados."""
  398 | 
  399 |     if modalidade not in {
  400 |         Triagem.Modalidade.EXTENSA,
  401 |         Triagem.Modalidade.SIMPLIFICADA,
  402 |     }:
  403 |         raise ValueError("Modalidade de triagem inválida.")
  404 | 
  405 |     hoje = hoje or date.today()
  406 |     respostas_atuais = _respostas_para_avaliar(
  407 |         modalidade,
  408 |         respostas,
  409 |         respostas_base,
  410 |     )
  411 |     achados = []
  412 | 
  413 |     for id_pergunta, valor in respostas_atuais.items():
  414 |         try:
  415 |             pergunta = obter_pergunta(id_pergunta)
  416 |         except KeyError:
  417 |             # O serviço rejeita IDs inválidos; o motor permanece tolerante a legado.
  418 |             continue
  419 | 
  420 |         for codigo in valor.get("codigos") or []:
  421 |             # EXT-24 usa a regra curta somente quando a segurança foi confirmada.
  422 |             if (
  423 |                 id_pergunta == "EXT-24"
  424 |                 and valor.get("seguranca") != "SIM"
  425 |             ):
  426 |                 continue
  427 | 
  428 |             achado = _avaliar_regra_declarada(
  429 |                 pergunta,
  430 |                 codigo,
  431 |                 valor,
  432 |                 hoje,
  433 |             )
  434 |             if achado:
  435 |                 achados.append(achado)
  436 | 
  437 |     # Regras que dependem de respostas de mais de uma pergunta ficam explícitas.
  438 |     achado_intervalo = _avaliar_intervalo_ultima_doacao(
  439 |         respostas_atuais,
  440 |         hoje,
  441 |     )
  442 |     if achado_intervalo:
  443 |         achados.append(achado_intervalo)
  444 | 
  445 |     achado_limite = _avaliar_limite_doacoes(respostas_atuais)
  446 |     if achado_limite:
  447 |         achados.append(achado_limite)
  448 | 
  449 |     achados.extend(
  450 |         _avaliar_seguranca_estetica(respostas_atuais, hoje)
  451 |     )
  452 | 
  453 |     resultado = escolher_resultado(achados)
  454 |     datas = [
  455 |         date.fromisoformat(achado["data_liberacao"])
  456 |         for achado in achados
  457 |         if achado.get("data_liberacao")
  458 |     ]
  459 | 
  460 |     return {
  461 |         "resultado": resultado,
  462 |         "mensagem": MENSAGENS_RESULTADO[resultado],
  463 |         "data_liberacao": max(datas) if datas else None,
  464 |         "achados": achados,
  465 |         "regra_version": TRIAGEM_RULE_VERSION,
  466 |     }
``````

## accounts/triagem_servico.py

Original: [accounts/triagem_servico.py](<C:/Users/lb119/Elo/accounts/triagem_servico.py>).

``````text
    1 | # Este arquivo controla o fluxo e o salvamento da triagem.
    2 | 
    3 | # - Permite triagem somente para Doadores e Receptores.
    4 | # - Inicia triagens extensas e simplificadas após o aceite do termo.
    5 | # - A simplificada utiliza uma triagem extensa concluída como base.
    6 | # - Organiza as perguntas conforme as respostas anteriores.
    7 | # - Mostra perguntas condicionais quando necessário.
    8 | # - Valida perguntas, alternativas e datas recebidas.
    9 | # - Salva, atualiza e reutiliza respostas anteriores quando solicitado.
   10 | # - Permite voltar ou editar enquanto a triagem está em andamento.
   11 | # - Remove respostas que deixam de ser válidas após uma alteração.
   12 | # - Impede alterações depois da conclusão.
   13 | # - Exige confirmação final antes de calcular o resultado.
   14 | # - Envia as respostas para o motor da triagem.
   15 | # - Salva resultado, mensagem, achados e data de liberação.
   16 | # - Usa transações para evitar dados incompletos ou alterações simultâneas.
   17 | 
   18 | # Os catálogos fornecem as perguntas, o motor aplica as regras e este arquivo controla o fluxo, as respostas e a persistência da triagem.
   19 | 
   20 | """Serviço transacional que controla o questionário e sua persistência."""
   21 | 
   22 | from datetime import date
   23 | 
   24 | from django.core.exceptions import PermissionDenied
   25 | from django.db import transaction
   26 | from django.utils import timezone
   27 | 
   28 | from .compatibilidade import normalizar_tipo_sanguineo
   29 | from .models import ConsentimentoLGPD, RespostaTriagem, Triagem, Usuario
   30 | from .triagem_catalogo import (
   31 |     PERGUNTAS_EXTENSAS,
   32 |     PERGUNTAS_SIMPLIFICADAS,
   33 |     TRIAGEM_RULE_VERSION,
   34 |     obter_pergunta,
   35 | )
   36 | from .triagem_motor import avaliar_triagem
   37 | 
   38 | 
   39 | class TriagemSimplificadaIndisponivel(Exception):
   40 |     """Indica que a pessoa ainda não concluiu uma triagem extensa."""
   41 | 
   42 | 
   43 | class TriagemConcluida(Exception):
   44 |     """Impede alteração de um resultado já registrado no histórico."""
   45 | 
   46 | 
   47 | class TriagemIncompleta(Exception):
   48 |     """Indica que existem perguntas obrigatórias ainda sem resposta."""
   49 | 
   50 | 
   51 | class TriagemExtensaNecessaria(Exception):
   52 |     """Indica que a versão rápida deixou de ser segura para o usuário."""
   53 | 
   54 | 
   55 | class PerguntaInvalida(Exception):
   56 |     """Impede códigos de pergunta ou alternativa fora do catálogo."""
   57 | 
   58 | 
   59 | PERFIS_COM_TRIAGEM = {
   60 |     Usuario.Perfil.DOADOR,
   61 | }
   62 | 
   63 | 
   64 | # A ordem explícita evita que a posição dependa da organização física do arquivo.
   65 | ORDEM_EXTENSA = [
   66 |     "EXT-01", "EXT-01A", "EXT-02", "EXT-03", "EXT-04", "EXT-05", "EXT-05A",
   67 |     "EXT-05B", "EXT-06", "EXT-07", "EXT-07A", "EXT-08", "EXT-09",
   68 |     "EXT-10", "EXT-11", "EXT-11A", "EXT-12", "EXT-13", "EXT-14",
   69 |     "EXT-15", "EXT-16", "EXT-17", "EXT-18", "EXT-19", "EXT-20",
   70 |     "EXT-21", "EXT-22", "EXT-23", "EXT-24", "EXT-25", "EXT-26",
   71 |     "EXT-27", "EXT-28", "EXT-29", "EXT-30", "EXT-31", "EXT-32",
   72 |     "EXT-33", "EXT-34", "EXT-35", "EXT-36", "EXT-37", "EXT-38",
   73 |     "EXT-39", "EXT-40", "EXT-41", "EXT-42", "EXT-43", "EXT-44",
   74 |     "EXT-45", "EXT-46", "EXT-47", "EXT-48", "EXT-49", "EXT-50",
   75 |     "EXT-51",
   76 | ]
   77 | 
   78 | ORDEM_SIMPLIFICADA = [
   79 |     f"SIM-{numero:02d}"
   80 |     for numero in range(1, 19)
   81 | ]
   82 | 
   83 | 
   84 | def pode_responder(usuario):
   85 |     """Diz se o perfil pode realizar uma triagem para doação."""
   86 | 
   87 |     return usuario.perfil in PERFIS_COM_TRIAGEM
   88 | 
   89 | 
   90 | def obter_extensa_base(usuario):
   91 |     """Retorna a extensa concluída mais recente do próprio usuário."""
   92 | 
   93 |     return (
   94 |         usuario.triagens.filter(
   95 |             modalidade=Triagem.Modalidade.EXTENSA,
   96 |             status=Triagem.Status.CONCLUIDA,
   97 |         )
   98 |         .order_by("-finalizada_em", "-iniciada_em")
   99 |         .first()
  100 |     )
  101 | 
  102 | 
  103 | def obter_extensa_reutilizavel(usuario):
  104 |     """Retorna a extensa concluída atual que pode preencher uma nova triagem."""
  105 | 
  106 |     return (
  107 |         usuario.triagens.filter(
  108 |             modalidade=Triagem.Modalidade.EXTENSA,
  109 |             status=Triagem.Status.CONCLUIDA,
  110 |             regra_version=TRIAGEM_RULE_VERSION,
  111 |         )
  112 |         .order_by("-finalizada_em", "-iniciada_em")
  113 |         .first()
  114 |     )
  115 | 
  116 | 
  117 | def _respostas_da_triagem(triagem):
  118 |     """Transforma registros do banco no mapa esperado pelo catálogo e motor."""
  119 | 
  120 |     return {
  121 |         resposta.id_pergunta: resposta.valor
  122 |         for resposta in triagem.respostas.all()
  123 |     }
  124 | 
  125 | 
  126 | def _condicao_atendida(pergunta, respostas):
  127 |     """Verifica as condições simples que mostram uma subpergunta."""
  128 | 
  129 |     condicao = pergunta.get("mostrar_se")
  130 |     if not condicao:
  131 |         return True
  132 | 
  133 |     for id_anterior, codigos_aceitos in condicao.items():
  134 |         valor = respostas.get(id_anterior) or {}
  135 |         codigos = set(valor.get("codigos") or [])
  136 |         if not codigos.intersection(codigos_aceitos):
  137 |             return False
  138 | 
  139 |     return True
  140 | 
  141 | 
  142 | def _copiar_respostas_para_nova_triagem(origem, destino):
  143 |     """Copia respostas para uma nova triagem sem alterar o histórico original."""
  144 | 
  145 |     RespostaTriagem.objects.bulk_create(
  146 |         [
  147 |             RespostaTriagem(
  148 |                 triagem=destino,
  149 |                 id_pergunta=resposta.id_pergunta,
  150 |                 codigo_resposta=resposta.codigo_resposta,
  151 |                 resposta_label=resposta.resposta_label,
  152 |                 data_evento=resposta.data_evento,
  153 |                 metadata=resposta.metadata,
  154 |                 valor=resposta.valor,
  155 |                 rule_version=resposta.rule_version,
  156 |                 source_ref=resposta.source_ref,
  157 |             )
  158 |             for resposta in origem.respostas.order_by("id_resposta")
  159 |         ]
  160 |     )
  161 | 
  162 | 
  163 | def calcular_fluxo(triagem):
  164 |     """Recalcula ramificações sem duplicar perguntas já adicionadas."""
  165 | 
  166 |     respostas = _respostas_da_triagem(triagem)
  167 | 
  168 |     if triagem.modalidade == Triagem.Modalidade.EXTENSA:
  169 |         return [
  170 |             id_pergunta
  171 |             for id_pergunta in ORDEM_EXTENSA
  172 |             if _condicao_atendida(
  173 |                 PERGUNTAS_EXTENSAS[id_pergunta],
  174 |                 respostas,
  175 |             )
  176 |         ]
  177 | 
  178 |     ids_abertos = set()
  179 |     for id_pergunta, valor in respostas.items():
  180 |         pergunta = PERGUNTAS_SIMPLIFICADAS.get(id_pergunta)
  181 |         if not pergunta:
  182 |             continue
  183 |         for codigo in valor.get("codigos") or []:
  184 |             ids_abertos.update(
  185 |                 pergunta["abrir_extensa"].get(codigo, [])
  186 |             )
  187 | 
  188 |     # Os blocos detalhados aparecem antes das confirmações rápidas finais.
  189 |     detalhadas = [
  190 |         id_pergunta
  191 |         for id_pergunta in ORDEM_EXTENSA
  192 |         if id_pergunta in ids_abertos
  193 |         and _condicao_atendida(
  194 |             PERGUNTAS_EXTENSAS[id_pergunta],
  195 |             respostas,
  196 |         )
  197 |     ]
  198 |     indice_confirmacao = ORDEM_SIMPLIFICADA.index("SIM-17")
  199 |     return [
  200 |         *ORDEM_SIMPLIFICADA[:indice_confirmacao],
  201 |         *detalhadas,
  202 |         *ORDEM_SIMPLIFICADA[indice_confirmacao:],
  203 |     ]
  204 | 
  205 | 
  206 | @transaction.atomic
  207 | def iniciar_triagem(
  208 |     usuario,
  209 |     modalidade,
  210 |     ip=None,
  211 |     aceite_termo=True,
  212 |     reutilizar_respostas=False,
  213 | ):
  214 |     """Cria/retoma a triagem após o aceite registrado pela camada de entrada.
  215 | 
  216 |     A view exige o checkbox explicitamente; o valor padrão preserva a API de
  217 |     serviço usada por integrações internas que já representam esse aceite.
  218 |     """
  219 | 
  220 |     if not pode_responder(usuario):
  221 |         raise PermissionDenied(
  222 |             "A triagem está disponível para Doadores."
  223 |         )
  224 | 
  225 |     if modalidade not in {
  226 |         Triagem.Modalidade.EXTENSA,
  227 |         Triagem.Modalidade.SIMPLIFICADA,
  228 |     }:
  229 |         raise ValueError("Modalidade de triagem inválida.")
  230 | 
  231 |     if not aceite_termo:
  232 |         raise PermissionDenied(
  233 |             "Confirme ciência do termo da pré-triagem antes de começar."
  234 |         )
  235 | 
  236 |     existente = (
  237 |         usuario.triagens.filter(
  238 |             modalidade=modalidade,
  239 |             status=Triagem.Status.EM_ANDAMENTO,
  240 |         )
  241 |         .order_by("-iniciada_em")
  242 |         .first()
  243 |     )
  244 |     if existente:
  245 |         return existente
  246 | 
  247 |     extensa_base = None
  248 |     if modalidade == Triagem.Modalidade.SIMPLIFICADA:
  249 |         extensa_base = obter_extensa_base(usuario)
  250 |         if extensa_base is None:
  251 |             raise TriagemSimplificadaIndisponivel(
  252 |                 "Conclua primeiro uma triagem extensa."
  253 |             )
  254 | 
  255 |     consentimento, _ = ConsentimentoLGPD.objects.get_or_create(
  256 |         usuario=usuario,
  257 |         tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM,
  258 |         versao_termo=TRIAGEM_RULE_VERSION,
  259 |         defaults={"aceito": True, "ip": ip},
  260 |     )
  261 |     if not consentimento.aceito:
  262 |         consentimento.aceito = True
  263 |         consentimento.revogado_em = None
  264 |         consentimento.ip = ip
  265 |         consentimento.save(
  266 |             update_fields=["aceito", "revogado_em", "ip"]
  267 |         )
  268 | 
  269 |     triagem = Triagem.objects.create(
  270 |         usuario=usuario,
  271 |         modalidade=modalidade,
  272 |         status=Triagem.Status.EM_ANDAMENTO,
  273 |         regra_version=TRIAGEM_RULE_VERSION,
  274 |         triagem_base=extensa_base,
  275 |     )
  276 | 
  277 |     if modalidade == Triagem.Modalidade.EXTENSA and reutilizar_respostas:
  278 |         origem = obter_extensa_reutilizavel(usuario)
  279 |         if origem is not None:
  280 |             _copiar_respostas_para_nova_triagem(origem, triagem)
  281 | 
  282 |     triagem.fluxo_perguntas = calcular_fluxo(triagem)
  283 |     triagem.save(update_fields=["fluxo_perguntas", "atualizada_em"])
  284 |     return triagem
  285 | 
  286 | 
  287 | def obter_pergunta_atual(triagem):
  288 |     """Retorna a pergunta apontada pelo andamento ou nada após o fim."""
  289 | 
  290 |     if triagem.status != Triagem.Status.EM_ANDAMENTO:
  291 |         return None
  292 |     if triagem.pergunta_atual >= len(triagem.fluxo_perguntas):
  293 |         return None
  294 | 
  295 |     return obter_pergunta(
  296 |         triagem.fluxo_perguntas[triagem.pergunta_atual]
  297 |     )
  298 | 
  299 | 
  300 | def _validar_valor(pergunta, valor):
  301 |     """Rejeita dados forjados mesmo quando não vieram do formulário Django."""
  302 | 
  303 |     codigos = valor.get("codigos") or []
  304 |     permitidos = {
  305 |         opcao["codigo"]
  306 |         for opcao in pergunta["opcoes"]
  307 |     }
  308 |     if not codigos or not set(codigos).issubset(permitidos):
  309 |         raise PerguntaInvalida(
  310 |             "A resposta não pertence às alternativas da pergunta."
  311 |         )
  312 |     if not pergunta["multipla"] and len(codigos) != 1:
  313 |         raise PerguntaInvalida(
  314 |             "Esta pergunta aceita somente uma alternativa."
  315 |         )
  316 | 
  317 | 
  318 | def _rotulo_resposta(pergunta, codigos):
  319 |     """Mantém no campo legado os rótulos visíveis ao usuário."""
  320 | 
  321 |     rotulos = {
  322 |         opcao["codigo"]: opcao["rotulo"]
  323 |         for opcao in pergunta["opcoes"]
  324 |     }
  325 |     return "; ".join(rotulos[codigo] for codigo in codigos)
  326 | 
  327 | 
  328 | def _primeira_data(valor):
  329 |     """Preenche o campo legado com a primeira data estruturada disponível."""
  330 | 
  331 |     datas = valor.get("datas") or {}
  332 |     if not datas:
  333 |         return None
  334 | 
  335 |     try:
  336 |         return date.fromisoformat(next(iter(datas.values())))
  337 |     except (TypeError, ValueError):
  338 |         raise PerguntaInvalida("A data da resposta é inválida.") from None
  339 | 
  340 | 
  341 | def _resposta_exige_extensa(id_pergunta, codigos):
  342 |     """Centraliza as respostas que invalidam o resumo da versão rápida."""
  343 | 
  344 |     escolhas = set(codigos)
  345 |     return (
  346 |         (
  347 |             id_pergunta == "SIM-01"
  348 |             and bool(escolhas & {"INCORRETO", "NAO_FIZ", "NAO_SEI"})
  349 |         )
  350 |         or (
  351 |             id_pergunta == "SIM-17"
  352 |             and bool(escolhas & {"SIM", "NAO_SEI"})
  353 |         )
  354 |         or (id_pergunta == "SIM-18" and "EXTENSA" in escolhas)
  355 |     )
  356 | 
  357 | 
  358 | def atualizar_tipo_sanguineo_do_usuario(triagem, valor):
  359 |     """
  360 |     Atualiza o tipo sanguineo do usuario a partir da pergunta informativa.
  361 | 
  362 |     Essa informacao nao interfere no resultado da triagem; ela apenas liga o
  363 |     usuario aos alertas internos de estoque e a compatibilidade sanguinea.
  364 |     """
  365 | 
  366 |     codigos = valor.get("codigos") or []
  367 |     if not codigos:
  368 |         return
  369 | 
  370 |     try:
  371 |         tipo_sanguineo = normalizar_tipo_sanguineo(codigos[0])
  372 |     except ValueError:
  373 |         return
  374 | 
  375 |     usuario = triagem.usuario
  376 |     if usuario.tipo_sanguineo_confirmado:
  377 |         return
  378 | 
  379 |     if usuario.tipo_sanguineo == tipo_sanguineo:
  380 |         return
  381 | 
  382 |     usuario.tipo_sanguineo = tipo_sanguineo
  383 |     usuario.save(update_fields=["tipo_sanguineo", "atualizado_em"])
  384 | 
  385 | 
  386 | def salvar_resposta(triagem, id_pergunta, valor):
  387 |     """Salva ou corrige uma resposta e avança o fluxo com segurança."""
  388 | 
  389 |     triagem_recebida = triagem
  390 |     exige_extensa = False
  391 | 
  392 |     # O bloco atômico termina antes da exceção de redirecionamento. Assim, a
  393 |     # tentativa rápida fica cancelada no histórico sem deixar dados pela metade.
  394 |     with transaction.atomic():
  395 |         registro = Triagem.objects.select_for_update().get(pk=triagem.pk)
  396 |         if registro.status != Triagem.Status.EM_ANDAMENTO:
  397 |             raise TriagemConcluida(
  398 |                 "Uma triagem concluída não pode ser alterada."
  399 |             )
  400 |         if id_pergunta not in registro.fluxo_perguntas:
  401 |             raise PerguntaInvalida("A pergunta não pertence a esta triagem.")
  402 | 
  403 |         pergunta = obter_pergunta(id_pergunta)
  404 |         _validar_valor(pergunta, valor)
  405 |         codigos = valor["codigos"]
  406 | 
  407 |         RespostaTriagem.objects.update_or_create(
  408 |             triagem=registro,
  409 |             id_pergunta=id_pergunta,
  410 |             defaults={
  411 |                 "codigo_resposta": codigos[0],
  412 |                 "resposta_label": _rotulo_resposta(pergunta, codigos),
  413 |                 "data_evento": _primeira_data(valor),
  414 |                 "metadata": {
  415 |                     chave: conteudo
  416 |                     for chave, conteudo in valor.items()
  417 |                     if chave not in {"codigos", "datas"}
  418 |                 },
  419 |                 "valor": valor,
  420 |                 "rule_version": pergunta["regra_version"],
  421 |                 "source_ref": pergunta["fonte"],
  422 |             },
  423 |         )
  424 | 
  425 |         if id_pergunta == "EXT-01A":
  426 |             atualizar_tipo_sanguineo_do_usuario(registro, valor)
  427 | 
  428 |         exige_extensa = (
  429 |             registro.modalidade == Triagem.Modalidade.SIMPLIFICADA
  430 |             and _resposta_exige_extensa(id_pergunta, codigos)
  431 |         )
  432 |         if exige_extensa:
  433 |             registro.status = Triagem.Status.CANCELADA
  434 |             registro.save(update_fields=["status", "atualizada_em"])
  435 |         else:
  436 |             fluxo = calcular_fluxo(registro)
  437 |             registro.fluxo_perguntas = fluxo
  438 | 
  439 |             # Se uma correção fechar uma ramificação, suas respostas antigas
  440 |             # deixam de ser válidas e não podem participar do cálculo final.
  441 |             registro.respostas.exclude(id_pergunta__in=fluxo).delete()
  442 | 
  443 |             # Estas respostas pedem revisão, portanto não avançam o cursor.
  444 |             if (
  445 |                 id_pergunta == "EXT-01"
  446 |                 and "NAO" in codigos
  447 |             ) or (
  448 |                 id_pergunta == "EXT-51"
  449 |                 and "REVISAR" in codigos
  450 |             ):
  451 |                 registro.pergunta_atual = 0
  452 |             else:
  453 |                 registro.pergunta_atual = min(
  454 |                     fluxo.index(id_pergunta) + 1,
  455 |                     len(fluxo),
  456 |                 )
  457 | 
  458 |             registro.save(
  459 |                 update_fields=[
  460 |                     "fluxo_perguntas",
  461 |                     "pergunta_atual",
  462 |                     "atualizada_em",
  463 |                 ]
  464 |             )
  465 | 
  466 |         # Mantém o objeto recebido sincronizado para a view usar imediatamente.
  467 |         triagem_recebida.fluxo_perguntas = registro.fluxo_perguntas
  468 |         triagem_recebida.pergunta_atual = registro.pergunta_atual
  469 |         triagem_recebida.status = registro.status
  470 |         triagem_recebida.atualizada_em = registro.atualizada_em
  471 | 
  472 |     if exige_extensa:
  473 |         raise TriagemExtensaNecessaria(
  474 |             "O resumo mudou; continue em uma nova triagem extensa."
  475 |         )
  476 | 
  477 |     return triagem_recebida
  478 | 
  479 | 
  480 | @transaction.atomic
  481 | def voltar_pergunta(triagem):
  482 |     """Move uma posição para trás sem apagar a resposta existente."""
  483 | 
  484 |     triagem_recebida = triagem
  485 |     registro = Triagem.objects.select_for_update().get(pk=triagem.pk)
  486 |     if registro.status != Triagem.Status.EM_ANDAMENTO:
  487 |         raise TriagemConcluida(
  488 |             "Uma triagem concluída não pode ser alterada."
  489 |         )
  490 | 
  491 |     registro.pergunta_atual = max(0, registro.pergunta_atual - 1)
  492 |     registro.save(update_fields=["pergunta_atual", "atualizada_em"])
  493 |     triagem_recebida.pergunta_atual = registro.pergunta_atual
  494 |     triagem_recebida.atualizada_em = registro.atualizada_em
  495 |     return triagem_recebida
  496 | 
  497 | 
  498 | @transaction.atomic
  499 | def editar_pergunta(triagem, id_pergunta):
  500 |     """Reposiciona uma triagem em andamento para uma resposta já salva."""
  501 | 
  502 |     registro = Triagem.objects.select_for_update().get(pk=triagem.pk)
  503 |     if registro.status != Triagem.Status.EM_ANDAMENTO:
  504 |         raise TriagemConcluida("Uma triagem concluída não pode ser alterada.")
  505 |     if id_pergunta not in registro.fluxo_perguntas:
  506 |         raise PerguntaInvalida("A pergunta não pertence a esta triagem.")
  507 | 
  508 |     registro.pergunta_atual = registro.fluxo_perguntas.index(id_pergunta)
  509 |     registro.save(update_fields=["pergunta_atual", "atualizada_em"])
  510 |     triagem.pergunta_atual = registro.pergunta_atual
  511 |     triagem.atualizada_em = registro.atualizada_em
  512 |     return triagem
  513 | 
  514 | 
  515 | @transaction.atomic
  516 | def concluir_triagem(triagem, hoje=None):
  517 |     """Calcula e congela o resultado depois da confirmação final."""
  518 | 
  519 |     triagem = Triagem.objects.select_for_update().get(pk=triagem.pk)
  520 |     if triagem.status != Triagem.Status.EM_ANDAMENTO:
  521 |         raise TriagemConcluida(
  522 |             "Uma triagem concluída não pode ser alterada."
  523 |         )
  524 | 
  525 |     respostas = _respostas_da_triagem(triagem)
  526 |     faltantes = set(triagem.fluxo_perguntas) - set(respostas)
  527 |     if faltantes:
  528 |         raise TriagemIncompleta(
  529 |             "Ainda existem perguntas sem resposta."
  530 |         )
  531 | 
  532 |     if triagem.modalidade == Triagem.Modalidade.EXTENSA:
  533 |         confirmacao = (
  534 |             respostas.get("EXT-51", {}).get("codigos") or []
  535 |         )
  536 |         if "CONFIRMAR" not in confirmacao:
  537 |             raise TriagemIncompleta("Revise e confirme a triagem extensa.")
  538 |         respostas_base = None
  539 |     else:
  540 |         confirmacao = (
  541 |             respostas.get("SIM-18", {}).get("codigos") or []
  542 |         )
  543 |         if "ENTENDO" not in confirmacao:
  544 |             raise TriagemIncompleta("Confirme a limitação da versão rápida.")
  545 |         respostas_base = _respostas_da_triagem(triagem.triagem_base)
  546 | 
  547 |     calculo = avaliar_triagem(
  548 |         triagem.modalidade,
  549 |         respostas,
  550 |         hoje=hoje,
  551 |         respostas_base=respostas_base,
  552 |     )
  553 |     triagem.resultado = calculo["resultado"]
  554 |     triagem.mensagem_resultado = calculo["mensagem"]
  555 |     triagem.data_liberacao = calculo["data_liberacao"]
  556 |     triagem.achados = calculo["achados"]
  557 |     triagem.status = Triagem.Status.CONCLUIDA
  558 |     triagem.finalizada_em = timezone.now()
  559 |     triagem.pergunta_atual = len(triagem.fluxo_perguntas)
  560 |     triagem.save(
  561 |         update_fields=[
  562 |             "resultado",
  563 |             "mensagem_resultado",
  564 |             "data_liberacao",
  565 |             "achados",
  566 |             "status",
  567 |             "finalizada_em",
  568 |             "pergunta_atual",
  569 |             "atualizada_em",
  570 |         ]
  571 |     )
  572 |     return triagem
``````

## accounts/urls.py

Original: [accounts/urls.py](<C:/Users/lb119/Elo/accounts/urls.py>).

``````text
    1 | """
    2 | RESUMO DO ARQUIVO
    3 | =================
    4 | 
    5 | Este arquivo associa cada endereco do app a uma view.
    6 | 
    7 | Exemplo: quando o navegador pede /cadastro/, o Django procura esta lista e
    8 | executa views.cadastro. Os nomes das rotas permitem gerar links sem escrever
    9 | enderecos manualmente nos templates.
   10 | """
   11 | 
   12 | from django.contrib.auth.views import LoginView, LogoutView
   13 | from django.urls import path
   14 | 
   15 | from . import views
   16 | from .forms import LoginUsuarioForm
   17 | 
   18 | 
   19 | app_name = "accounts"
   20 | 
   21 | 
   22 | urlpatterns = [
   23 | 
   24 |     # ==========================================================
   25 |     # ACESSO PUBLICO
   26 |     # ==========================================================
   27 | 
   28 |     path(
   29 |         "",
   30 |         views.inicio,
   31 |         name="inicio",
   32 |     ),
   33 | 
   34 |     # Cadastro.
   35 |     path(
   36 |         "cadastro/",
   37 |         views.cadastro,
   38 |         name="cadastro",
   39 |     ),
   40 | 
   41 |     # Login.
   42 |     path(
   43 |         "login/",
   44 |         LoginView.as_view(
   45 |             template_name="accounts/login.html",
   46 |             authentication_form=LoginUsuarioForm,
   47 |             redirect_authenticated_user=True,
   48 |         ),
   49 |         name="login",
   50 |     ),
   51 | 
   52 |     # Logout.
   53 |     path(
   54 |         "logout/",
   55 |         LogoutView.as_view(),
   56 |         name="logout",
   57 |     ),
   58 | 
   59 |     # Dashboard.
   60 |     path(
   61 |         "dashboard/",
   62 |         views.dashboard,
   63 |         name="dashboard",
   64 |     ),
   65 | 
   66 |     # Validacao administrativa de Hemocentros.
   67 |     # A tela e as acoes sao protegidas pelas views para que somente um
   68 |     # Administrador consiga consultar ou alterar os cadastros pendentes.
   69 |     path(
   70 |         "hemocentros/validacao/",
   71 |         views.painel_aprovacao_hemocentros,
   72 |         name="painel_aprovacao_hemocentros",
   73 |     ),
   74 |     path(
   75 |         "hemocentros/pendentes/",
   76 |         views.hemocentros_pendentes,
   77 |         name="hemocentros_pendentes",
   78 |     ),
   79 |     path(
   80 |         "hemocentros/<int:id_hemocentro>/aprovar/",
   81 |         views.aprovar_hemocentro,
   82 |         name="aprovar_hemocentro",
   83 |     ),
   84 |     path(
   85 |         "hemocentros/<int:id_hemocentro>/recusar/",
   86 |         views.recusar_hemocentro,
   87 |         name="recusar_hemocentro",
   88 |     ),
   89 |     path(
   90 |         "hemocentros/<int:id_hemocentro>/solicitar-correcao/",
   91 |         views.solicitar_correcao_hemocentro,
   92 |         name="solicitar_correcao_hemocentro",
   93 |     ),
   94 | 
   95 |     # ==========================================================
   96 |     # PEDIDOS DE SANGUE
   97 |     # ==========================================================
   98 | 
   99 |     # Publicacao de pedidos de sangue.
  100 |     path(
  101 |         "pedidos/publicar/",
  102 |         views.criar_pedido_sangue,
  103 |         name="pedido_publicar",
  104 |     ),
  105 | 
  106 |     path(
  107 |         "pedidos/",
  108 |         views.consultar_pedidos,
  109 |         name="consultar_pedidos",
  110 |     ),
  111 | 
  112 |     path(
  113 |         "pedidos/novo/",
  114 |         views.criar_pedido_sangue,
  115 |         name="criar_pedido_sangue",
  116 |     ),
  117 | 
  118 |     path(
  119 |         "pedidos/minhas-solicitacoes/",
  120 |         views.minhas_solicitacoes,
  121 |         name="minhas_solicitacoes",
  122 |     ),
  123 | 
  124 |     path(
  125 |         "pedidos/hemocentro/",
  126 |         views.painel_pedidos_hemocentro,
  127 |         name="painel_pedidos_hemocentro",
  128 |     ),
  129 | 
  130 |     path(
  131 |         "pedidos/validacao/",
  132 |         views.painel_validacao_pedidos,
  133 |         name="painel_validacao_pedidos",
  134 |     ),
  135 | 
  136 |     path(
  137 |         "pedidos/<int:id_pedido>/aprovar/",
  138 |         views.aprovar_pedido,
  139 |         name="aprovar_pedido",
  140 |     ),
  141 | 
  142 |     path(
  143 |         "pedidos/<int:id_pedido>/recusar/",
  144 |         views.recusar_pedido,
  145 |         name="recusar_pedido",
  146 |     ),
  147 | 
  148 |     path(
  149 |         "pedidos/<int:id_pedido>/correcao/",
  150 |         views.solicitar_correcao_pedido,
  151 |         name="solicitar_correcao_pedido",
  152 |     ),
  153 | 
  154 |     path(
  155 |         "pedidos/<int:id_pedido>/suspeito/",
  156 |         views.marcar_pedido_suspeito,
  157 |         name="marcar_pedido_suspeito",
  158 |     ),
  159 | 
  160 |     # ==========================================================
  161 |     # TRIAGEM
  162 |     # ==========================================================
  163 | 
  164 |     # Pagina publica que explica a triagem e apresenta as modalidades.
  165 |     path(
  166 |         "triagem/",
  167 |         views.triagem_apresentacao,
  168 |         name="triagem_apresentacao",
  169 |     ),
  170 | 
  171 |     # Inicia ou retoma a modalidade escolhida.
  172 |     path(
  173 |         "triagem/iniciar/<str:modalidade>/",
  174 |         views.triagem_iniciar,
  175 |         name="triagem_iniciar",
  176 |     ),
  177 | 
  178 |     # Pergunta atual da triagem.
  179 |     path(
  180 |         "triagem/<int:id_triagem>/pergunta/",
  181 |         views.triagem_pergunta,
  182 |         name="triagem_pergunta",
  183 |     ),
  184 | 
  185 |     # Resultado.
  186 |     path(
  187 |         "triagem/<int:id_triagem>/resultado/",
  188 |         views.triagem_resultado,
  189 |         name="triagem_resultado",
  190 |     ),
  191 | 
  192 |     path(
  193 |         "triagem/<int:id_triagem>/revisao/",
  194 |         views.triagem_revisao,
  195 |         name="triagem_revisao",
  196 |     ),
  197 | 
  198 |     # Historico do usuario.
  199 |     path(
  200 |         "triagens/historico/",
  201 |         views.triagem_historico,
  202 |         name="triagem_historico",
  203 |     ),
  204 | 
  205 |     # ==========================================================
  206 |     # COMPATIBILIDADE SANGUINEA
  207 |     # ==========================================================
  208 | 
  209 |     path(
  210 |         "compatibilidade-sanguinea/",
  211 |         views.compatibilidade_sanguinea,
  212 |         name="compatibilidade_sanguinea",
  213 |     ),
  214 | 
  215 |     # ==========================================================
  216 |     # ESTOQUE
  217 |     # ==========================================================
  218 | 
  219 |     # Publica. Visitantes e usuarios autenticados podem acessar.
  220 |     path(
  221 |         "estoque/",
  222 |         views.visualizacao_publica_estoque,
  223 |         name="estoque_publico",
  224 |     ),
  225 | 
  226 |     # Privadas do Hemocentro. O acesso e protegido dentro das views.
  227 |     path(
  228 |         "estoque/hemocentro/",
  229 |         views.estoque_hemocentro,
  230 |         name="estoque_hemocentro",
  231 |     ),
  232 | 
  233 |     path(
  234 |         "estoque/hemocentro/cadastrar/",
  235 |         views.cadastrar_estoque_view,
  236 |         name="cadastrar_estoque",
  237 |     ),
  238 | 
  239 |     path(
  240 |         "estoque/hemocentro/<int:id_estoque>/atualizar/",
  241 |         views.atualizar_estoque_view,
  242 |         name="atualizar_estoque",
  243 |     ),
  244 | ]
``````

## accounts/validacao_hemocentro.py

Original: [accounts/validacao_hemocentro.py](<C:/Users/lb119/Elo/accounts/validacao_hemocentro.py>).

``````text
    1 | from functools import wraps
    2 | 
    3 | from django.core.exceptions import PermissionDenied, ValidationError
    4 | from django.db import transaction
    5 | 
    6 | from .auditoria import registrar_auditoria
    7 | from .models import AuditoriaAcaoCritica, Usuario, ValidacaoHemocentro
    8 | 
    9 | 
   10 | PARECER_PADRAO = {
   11 |     Usuario.StatusValidacaoHemocentro.APROVADO: "Hemocentro aprovado pelo administrador.",
   12 |     Usuario.StatusValidacaoHemocentro.RECUSADO: "Cadastro de hemocentro recusado pelo administrador.",
   13 |     Usuario.StatusValidacaoHemocentro.CORRECAO: "Administrador solicitou correcao dos dados cadastrais.",
   14 | }
   15 | 
   16 | 
   17 | def usuario_e_administrador(usuario):
   18 |     return bool(
   19 |         getattr(usuario, "is_authenticated", False)
   20 |         and (
   21 |             usuario.is_superuser
   22 |             or usuario.perfil == Usuario.Perfil.ADMINISTRADOR
   23 |         )
   24 |     )
   25 | 
   26 | 
   27 | def usuario_e_hemocentro(usuario):
   28 |     return bool(
   29 |         getattr(usuario, "is_authenticated", False)
   30 |         and usuario.perfil == Usuario.Perfil.HEMOCENTRO
   31 |     )
   32 | 
   33 | 
   34 | def hemocentro_aprovado(usuario):
   35 |     return (
   36 |         usuario_e_hemocentro(usuario)
   37 |         and usuario.status_validacao == Usuario.StatusValidacaoHemocentro.APROVADO
   38 |     )
   39 | 
   40 | 
   41 | def validar_publicacao_hemocentro(usuario):
   42 |     if not getattr(usuario, "is_authenticated", False):
   43 |         raise PermissionDenied("Faca login para publicar estoque ou campanha.")
   44 | 
   45 |     if not usuario_e_hemocentro(usuario):
   46 |         raise PermissionDenied(
   47 |             "Somente usuarios com perfil Hemocentro podem publicar estoque ou campanha."
   48 |         )
   49 | 
   50 |     if not hemocentro_aprovado(usuario):
   51 |         raise PermissionDenied(
   52 |             "Hemocentro ainda nao aprovado. "
   53 |             f"Status atual: {usuario.get_status_validacao_display()}."
   54 |         )
   55 | 
   56 |     return True
   57 | 
   58 | 
   59 | def exigir_hemocentro_aprovado(view_func):
   60 |     @wraps(view_func)
   61 |     def wrapper(request, *args, **kwargs):
   62 |         validar_publicacao_hemocentro(request.user)
   63 |         return view_func(request, *args, **kwargs)
   64 | 
   65 |     return wrapper
   66 | 
   67 | 
   68 | def registrar_decisao_validacao_hemocentro(
   69 |     *,
   70 |     hemocentro,
   71 |     admin,
   72 |     status,
   73 |     parecer="",
   74 |     request=None,
   75 | ):
   76 |     if hemocentro.perfil != Usuario.Perfil.HEMOCENTRO:
   77 |         raise ValidationError(
   78 |             "Somente usuarios com perfil Hemocentro podem passar por validacao."
   79 |         )
   80 | 
   81 |     if not usuario_e_administrador(admin):
   82 |         raise PermissionDenied("Somente administradores podem validar Hemocentros.")
   83 | 
   84 |     if admin.perfil == Usuario.Perfil.HEMOCENTRO:
   85 |         raise PermissionDenied("Hemocentros nao podem validar cadastros institucionais.")
   86 | 
   87 |     parecer = (parecer or "").strip() or PARECER_PADRAO.get(status, "")
   88 | 
   89 |     with transaction.atomic():
   90 |         hemocentro_atualizado = Usuario.objects.select_for_update().get(
   91 |             pk=hemocentro.pk
   92 |         )
   93 | 
   94 |         status_anterior = hemocentro_atualizado.status_validacao
   95 |         hemocentro_atualizado.status_validacao = status
   96 |         hemocentro_atualizado.save(
   97 |             update_fields=["status_validacao", "atualizado_em"]
   98 |         )
   99 | 
  100 |         validacao = ValidacaoHemocentro.objects.create(
  101 |             hemocentro=hemocentro_atualizado,
  102 |             admin=admin,
  103 |             status=status,
  104 |             parecer=parecer,
  105 |         )
  106 | 
  107 |         registrar_auditoria(
  108 |             acao=AuditoriaAcaoCritica.Acao.APROVACAO_HEMOCENTRO,
  109 |             resultado=AuditoriaAcaoCritica.Resultado.SUCESSO,
  110 |             usuario=admin,
  111 |             alvo=hemocentro_atualizado,
  112 |             descricao="Validacao institucional de hemocentro.",
  113 |             request=request,
  114 |             metadados={
  115 |                 "id_validacao": validacao.pk,
  116 |                 "status_anterior": status_anterior,
  117 |                 "status_novo": status,
  118 |                 "parecer": parecer,
  119 |             },
  120 |         )
  121 | 
  122 |     return validacao
  123 | 
  124 | 
  125 | def aprovar_hemocentro(*, hemocentro, admin, parecer="", request=None):
  126 |     return registrar_decisao_validacao_hemocentro(
  127 |         hemocentro=hemocentro,
  128 |         admin=admin,
  129 |         status=Usuario.StatusValidacaoHemocentro.APROVADO,
  130 |         parecer=parecer,
  131 |         request=request,
  132 |     )
  133 | 
  134 | 
  135 | def recusar_hemocentro(*, hemocentro, admin, parecer="", request=None):
  136 |     return registrar_decisao_validacao_hemocentro(
  137 |         hemocentro=hemocentro,
  138 |         admin=admin,
  139 |         status=Usuario.StatusValidacaoHemocentro.RECUSADO,
  140 |         parecer=parecer,
  141 |         request=request,
  142 |     )
  143 | 
  144 | 
  145 | def solicitar_correcao_hemocentro(*, hemocentro, admin, parecer="", request=None):
  146 |     return registrar_decisao_validacao_hemocentro(
  147 |         hemocentro=hemocentro,
  148 |         admin=admin,
  149 |         status=Usuario.StatusValidacaoHemocentro.CORRECAO,
  150 |         parecer=parecer,
  151 |         request=request,
  152 |     )
``````

## accounts/validacao_pedido.py

Original: [accounts/validacao_pedido.py](<C:/Users/lb119/Elo/accounts/validacao_pedido.py>).

``````text
    1 | # Este módulo controla a criação e a validação dos pedidos de sangue.
    2 | 
    3 | # 1. validar_dados_pedido()
    4 | #    Confere título, tipo sanguíneo, urgência, cidade, descrição, solicitante, e-mail de contato e Hemocentro de destino aprovado.
    5 | 
    6 | # 2. criar_pedido_pendente()
    7 | #    Cria o pedido com status ENVIADA.
    8 | #    Administradores e Hemocentros não criam solicitações comuns.
    9 | #    O pedido não é publicado automaticamente.
   10 | #    Também verifica pedidos semelhantes nos últimos 7 dias e marca possíveis duplicidades apenas como alerta.
   11 | 
   12 | # 3. registrar_decisao_validacao_pedido()
   13 | #    Registra a decisão sobre o pedido dentro de uma transação segura.
   14 | #    Pedidos encerrados não podem ser alterados.
   15 | #    O Hemocentro aprovado de destino pode:
   16 | #    - aprovar e publicar;
   17 | #    - recusar;
   18 | #    - solicitar correção;
   19 | #    - marcar como suspeito.
   20 | #    O Administrador pode apenas marcar o pedido como suspeito para moderação e auditoria.
   21 | 
   22 | # 4. Quando o pedido é aprovado:
   23 | #    - seu status muda para PUBLICADA;
   24 | #    - o Hemocentro responsável e a data são registrados;
   25 | #    - notificações compatíveis são criadas;
   26 | #    - a decisão é salva no histórico;
   27 | #    - a ação é registrada na auditoria.
   28 | 
   29 | # 5. Funções auxiliares
   30 | #    aprovar_pedido(), recusar_pedido(), solicitar_correcao_pedido() e
   31 | #    marcar_pedido_suspeito() apenas chamam a função principal informando o
   32 | #    status correspondente.
   33 | 
   34 | # O formulário valida os dados na interface, este arquivo repete as validações importantes no servidor e o modelo protege a integridade final do banco.
   35 | 
   36 | from django.core.exceptions import PermissionDenied, ValidationError
   37 | from django.core.validators import validate_email
   38 | from datetime import timedelta
   39 | 
   40 | from django.db import transaction
   41 | from django.utils import timezone
   42 | 
   43 | from .auditoria import registrar_auditoria
   44 | from .models import (
   45 |     AuditoriaAcaoCritica,
   46 |     PedidoSangue,
   47 |     Usuario,
   48 |     ValidacaoPedido,
   49 | )
   50 | from .validacao_hemocentro import hemocentro_aprovado, usuario_e_administrador
   51 | 
   52 | 
   53 | def validar_dados_pedido(pedido):
   54 |     """
   55 |     Valida as informações básicas antes da decisão administrativa.
   56 |     """
   57 | 
   58 |     if not pedido.titulo.strip():
   59 |         raise ValidationError(
   60 |             "O pedido precisa possuir um título."
   61 |         )
   62 | 
   63 |     if not pedido.tipo_sanguineo:
   64 |         raise ValidationError(
   65 |             "Informe o tipo sanguíneo."
   66 |         )
   67 | 
   68 |     if not pedido.urgencia:
   69 |         raise ValidationError(
   70 |             "Informe a urgência."
   71 |         )
   72 | 
   73 |     if not pedido.cidade.strip():
   74 |         raise ValidationError(
   75 |             "Informe a cidade."
   76 |         )
   77 | 
   78 |     if not pedido.descricao.strip():
   79 |         raise ValidationError(
   80 |             "Informe a descrição do pedido."
   81 |         )
   82 | 
   83 |     if not pedido.nome_solicitante.strip():
   84 |         raise ValidationError("Informe o nome ou identificação do solicitante.")
   85 | 
   86 |     if not pedido.contato.strip():
   87 |         raise ValidationError("Informe um e-mail para retorno.")
   88 | 
   89 |     try:
   90 |         validate_email(pedido.contato.strip())
   91 |     except ValidationError as erro:
   92 |         raise ValidationError("Informe um e-mail válido para retorno.") from erro
   93 | 
   94 |     if not pedido.hemocentro_destino_id:
   95 |         raise ValidationError(
   96 |             "Informe o Hemocentro de destino."
   97 |         )
   98 | 
   99 |     if (
  100 |         pedido.hemocentro_destino.perfil
  101 |         != Usuario.Perfil.HEMOCENTRO
  102 |     ):
  103 |         raise ValidationError(
  104 |             "O destino precisa ser um Hemocentro."
  105 |         )
  106 | 
  107 |     if (
  108 |         pedido.hemocentro_destino.status_validacao
  109 |         != Usuario.StatusValidacaoHemocentro.APROVADO
  110 |     ):
  111 |         raise ValidationError(
  112 |             "O Hemocentro de destino precisa estar aprovado."
  113 |         )
  114 | 
  115 | 
  116 | def criar_pedido_pendente(
  117 |     *,
  118 |     dados,
  119 |     solicitante,
  120 | ):
  121 |     """
  122 |     Cria o pedido sem publicá-lo.
  123 |     """
  124 | 
  125 |     if not getattr(solicitante, "is_authenticated", False) or solicitante.perfil != Usuario.Perfil.RECEPTOR:
  126 |         raise PermissionDenied("Somente Receptor pode enviar solicitacao de pedido de sangue.")
  127 | 
  128 |     dados = dict(dados)
  129 |     hemocentro_destino = dados.get("hemocentro_destino")
  130 |     if hemocentro_destino and not hasattr(hemocentro_destino, "pk"):
  131 |         try:
  132 |             dados["hemocentro_destino"] = Usuario.objects.get(
  133 |                 pk=hemocentro_destino,
  134 |                 perfil=Usuario.Perfil.HEMOCENTRO,
  135 |             )
  136 |         except Usuario.DoesNotExist as erro:
  137 |             raise ValidationError("Hemocentro de destino inválido.") from erro
  138 | 
  139 |     pedido = PedidoSangue(
  140 |         solicitante=solicitante,
  141 |         status=PedidoSangue.Status.ENVIADA,
  142 |         **dados,
  143 |     )
  144 | 
  145 |     validar_dados_pedido(pedido)
  146 |     pedido.full_clean()
  147 | 
  148 |     pedido.save()
  149 | 
  150 |     # Semelhança é apenas um alerta para o Hemocentro; nunca bloqueia uma
  151 |     # necessidade legítima automaticamente.
  152 |     limite = timezone.now() - timedelta(days=7)
  153 |     duplicado = PedidoSangue.objects.filter(
  154 |         hemocentro_destino=pedido.hemocentro_destino,
  155 |         tipo_sanguineo=pedido.tipo_sanguineo,
  156 |         cidade__iexact=pedido.cidade,
  157 |         data_criacao__gte=limite,
  158 |     ).exclude(pk=pedido.pk).filter(
  159 |         status__in=[
  160 |             PedidoSangue.Status.ENVIADA,
  161 |             PedidoSangue.Status.EM_ANALISE,
  162 |             PedidoSangue.Status.PUBLICADA,
  163 |             PedidoSangue.Status.CORRECAO_SOLICITADA,
  164 |         ]
  165 |     ).exists()
  166 |     if duplicado:
  167 |         pedido.duplicidade_suspeita = True
  168 |         pedido.save(update_fields=["duplicidade_suspeita", "atualizado_em"])
  169 | 
  170 |     return pedido
  171 | 
  172 | 
  173 | @transaction.atomic
  174 | def registrar_decisao_validacao_pedido(
  175 |     *,
  176 |     pedido,
  177 |     moderador,
  178 |     status_validacao,
  179 |     motivo="",
  180 |     request=None,
  181 | ):
  182 |     """
  183 |     Registra a decisão administrativa e atualiza
  184 |     o status do pedido.
  185 |     """
  186 | 
  187 |     motivo = (motivo or "").strip()
  188 | 
  189 |     if status_validacao not in [
  190 |         ValidacaoPedido.StatusValidacao.APROVADO,
  191 |         ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA,
  192 |         ValidacaoPedido.StatusValidacao.RECUSADO,
  193 |         ValidacaoPedido.StatusValidacao.SUSPEITO,
  194 |     ]:
  195 |         raise ValidationError(
  196 |             "Status de validação inválido."
  197 |         )
  198 | 
  199 |     # A publicação, a recusa e a solicitação de correção pertencem somente
  200 |     # ao Hemocentro aprovado de destino. O Administrador apenas pode
  201 |     # registrar uma suspeita para fins de moderação/auditoria.
  202 |     administrador = usuario_e_administrador(moderador)
  203 |     hemocentro_do_destino = (
  204 |         hemocentro_aprovado(moderador)
  205 |         and pedido.hemocentro_destino_id == moderador.pk
  206 |     )
  207 | 
  208 |     if status_validacao == ValidacaoPedido.StatusValidacao.SUSPEITO:
  209 |         if not administrador and not hemocentro_do_destino:
  210 |             raise PermissionDenied(
  211 |                 "Somente o administrador ou o Hemocentro aprovado de destino "
  212 |                 "pode marcar um pedido como suspeito."
  213 |             )
  214 |     elif not hemocentro_do_destino:
  215 |         raise PermissionDenied(
  216 |             "Somente o Hemocentro aprovado de destino pode analisar e publicar "
  217 |             "pedidos."
  218 |         )
  219 | 
  220 |     # Não use select_related junto com select_for_update aqui. Como
  221 |     # solicitante é uma FK anulável, o Django gera LEFT OUTER JOIN e o
  222 |     # PostgreSQL não permite aplicar FOR UPDATE ao lado opcional da junção.
  223 |     # O bloqueio deve atingir somente a linha do pedido; as relações são
  224 |     # carregadas sob demanda quando as notificações forem criadas.
  225 |     pedido = PedidoSangue.objects.select_for_update().get(pk=pedido.pk)
  226 | 
  227 |     status_anterior = pedido.status
  228 |     institucional = hemocentro_do_destino
  229 | 
  230 |     if pedido.status == PedidoSangue.Status.ENCERRADA:
  231 |         raise ValidationError("Não é possível validar um pedido encerrado.")
  232 | 
  233 |     if status_validacao == (
  234 |         ValidacaoPedido.StatusValidacao.APROVADO
  235 |     ):
  236 |         validar_dados_pedido(pedido)
  237 |         novo_status = PedidoSangue.Status.PUBLICADA
  238 | 
  239 |         if not motivo:
  240 |             motivo = (
  241 |                 "Pedido aprovado pelo Hemocentro de destino."
  242 |             )
  243 | 
  244 |     elif status_validacao == (
  245 |         ValidacaoPedido.StatusValidacao.RECUSADO
  246 |     ):
  247 |         novo_status = PedidoSangue.Status.RECUSADA
  248 | 
  249 |         if not motivo:
  250 |             motivo = (
  251 |                 "Pedido recusado pelo Hemocentro de destino."
  252 |             )
  253 | 
  254 |     elif status_validacao == ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA:
  255 |         novo_status = PedidoSangue.Status.CORRECAO_SOLICITADA
  256 | 
  257 |         if not motivo:
  258 |             motivo = "O Hemocentro solicitou correção das informações."
  259 | 
  260 |     else:
  261 |         novo_status = PedidoSangue.Status.EM_ANALISE
  262 | 
  263 |         if not motivo:
  264 |             motivo = (
  265 |                 "Pedido marcado como suspeito "
  266 |                 "e mantido em análise."
  267 |             )
  268 | 
  269 |     pedido.status = novo_status
  270 | 
  271 |     if novo_status == PedidoSangue.Status.PUBLICADA:
  272 |         pedido.publicado_por = moderador
  273 |         pedido.publicado_em = timezone.now()
  274 | 
  275 |     pedido.save(
  276 |         update_fields=[
  277 |             "status",
  278 |             "atualizado_em",
  279 |             "publicado_por",
  280 |             "publicado_em",
  281 |         ]
  282 |     )
  283 | 
  284 |     notificacoes_geradas = 0
  285 |     if novo_status == PedidoSangue.Status.PUBLICADA:
  286 |         from .pedidos import criar_notificacoes_para_pedido
  287 | 
  288 |         notificacoes_geradas = criar_notificacoes_para_pedido(pedido=pedido)
  289 | 
  290 |     validacao = ValidacaoPedido.objects.create(
  291 |         pedido=pedido,
  292 |         status_validacao=status_validacao,
  293 |         motivo=motivo,
  294 |         moderador=moderador,
  295 |     )
  296 | 
  297 |     registrar_auditoria(
  298 |         acao=AuditoriaAcaoCritica.Acao.MODERACAO,
  299 |         resultado=AuditoriaAcaoCritica.Resultado.SUCESSO,
  300 |         usuario=moderador,
  301 |         alvo=pedido,
  302 |         descricao=(
  303 |             "Decisao institucional sobre pedido de sangue." if institucional
  304 |             else "Validacao administrativa de pedido de sangue."
  305 |         ),
  306 |         request=request,
  307 |         metadados={
  308 |             "evento": "PUBLICACAO_PEDIDO" if institucional and status_validacao == ValidacaoPedido.StatusValidacao.APROVADO else "VALIDACAO_PEDIDO",
  309 |             "status_anterior": status_anterior,
  310 |             "perfil_responsavel": moderador.perfil,
  311 |             "id_pedido": pedido.pk,
  312 |             "id_validacao": validacao.pk,
  313 |             "status_validacao": status_validacao,
  314 |             "status_pedido": novo_status,
  315 |             "motivo": motivo,
  316 |             "notificacoes_geradas": notificacoes_geradas,
  317 |         },
  318 |     )
  319 | 
  320 |     return validacao
  321 | 
  322 | 
  323 | def aprovar_pedido(
  324 |     *,
  325 |     pedido,
  326 |     moderador,
  327 |     motivo="",
  328 |     request=None,
  329 | ):
  330 |     return registrar_decisao_validacao_pedido(
  331 |         pedido=pedido,
  332 |         moderador=moderador,
  333 |         status_validacao=(
  334 |             ValidacaoPedido.StatusValidacao.APROVADO
  335 |         ),
  336 |         motivo=motivo,
  337 |         request=request,
  338 |     )
  339 | 
  340 | 
  341 | def recusar_pedido(
  342 |     *,
  343 |     pedido,
  344 |     moderador,
  345 |     motivo="",
  346 |     request=None,
  347 | ):
  348 |     return registrar_decisao_validacao_pedido(
  349 |         pedido=pedido,
  350 |         moderador=moderador,
  351 |         status_validacao=(
  352 |             ValidacaoPedido.StatusValidacao.RECUSADO
  353 |         ),
  354 |         motivo=motivo,
  355 |         request=request,
  356 |     )
  357 | 
  358 | 
  359 | def solicitar_correcao_pedido(
  360 |     *,
  361 |     pedido,
  362 |     moderador,
  363 |     motivo="",
  364 |     request=None,
  365 | ):
  366 |     return registrar_decisao_validacao_pedido(
  367 |         pedido=pedido,
  368 |         moderador=moderador,
  369 |         status_validacao=(
  370 |             ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA
  371 |         ),
  372 |         motivo=motivo,
  373 |         request=request,
  374 |     )
  375 | 
  376 | 
  377 | def marcar_pedido_suspeito(
  378 |     *,
  379 |     pedido,
  380 |     moderador,
  381 |     motivo="",
  382 |     request=None,
  383 | ):
  384 |     return registrar_decisao_validacao_pedido(
  385 |         pedido=pedido,
  386 |         moderador=moderador,
  387 |         status_validacao=(
  388 |             ValidacaoPedido.StatusValidacao.SUSPEITO
  389 |         ),
  390 |         motivo=motivo,
  391 |         request=request,
  392 |     )
``````

## accounts/views.py

Original: [accounts/views.py](<C:/Users/lb119/Elo/accounts/views.py>).

``````text
    1 | """
    2 | 
    3 | Views do aplicativo accounts.
    4 | 
    5 | As views recebem requisicoes do navegador, executam a regra da pagina
    6 | 
    7 | e devolvem uma resposta.
    8 | 
    9 | Fluxo do cadastro:
   10 | 
   11 | GET  -> mostra formulario vazio.
   12 | 
   13 | POST -> valida -> grava usuario + consentimento -> cria sessao -> dashboard.
   14 | 
   15 | O cadastro usa uma transacao para impedir que apenas metade da operacao
   16 | 
   17 | seja salva. O dashboard usa login_required para bloquear visitantes.
   18 | 
   19 | """
   20 | 
   21 | from django import forms
   22 | 
   23 | from django.contrib import messages
   24 | 
   25 | from django.contrib.auth import login
   26 | 
   27 | from django.contrib.auth.decorators import login_required
   28 | 
   29 | from django.core.exceptions import PermissionDenied, ValidationError
   30 | from django.core.paginator import Paginator
   31 | from django.utils import timezone
   32 | 
   33 | from django.db import transaction
   34 | 
   35 | from django.http import Http404, JsonResponse
   36 | 
   37 | from django.shortcuts import get_object_or_404, redirect, render
   38 | 
   39 | from django.views.decorators.http import require_POST
   40 | 
   41 | from django.db.models import Case, IntegerField, Prefetch, Value, When
   42 | 
   43 | from .forms import (
   44 |     CadastrarEstoqueForm,
   45 |     CadastroUsuarioForm,
   46 |     PreferenciaConvocacaoForm,
   47 |     MovimentarEstoqueForm,
   48 |     FiltroEstoquePublicoForm,
   49 |     PedidoSangueForm,
   50 |     FiltroPedidoSangueForm,
   51 | )
   52 | from .auditoria import registrar_auditoria
   53 | 
   54 | from .models import (
   55 |     ConsentimentoLGPD,
   56 |     Estoque,
   57 |     EstoqueMovimentacao,
   58 |     PedidoSangue,
   59 |     Triagem,
   60 |     Usuario,
   61 |     ValidacaoHemocentro,
   62 |     ValidacaoPedido,
   63 |     AuditoriaAcaoCritica,
   64 | )
   65 | 
   66 | from .estoque import (
   67 |     cadastrar_estoque,
   68 |     obter_estoques_publicos,
   69 |     registrar_movimentacao_estoque,
   70 | )
   71 | 
   72 | from .validacao_hemocentro import (
   73 |     aprovar_hemocentro as aprovar_hemocentro_servico,
   74 |     exigir_hemocentro_aprovado,
   75 |     validar_publicacao_hemocentro,
   76 |     hemocentro_aprovado,
   77 |     recusar_hemocentro as recusar_hemocentro_servico,
   78 |     solicitar_correcao_hemocentro as solicitar_correcao_hemocentro_servico,
   79 |     usuario_e_administrador,
   80 | )
   81 | 
   82 | from .compatibilidade import (
   83 |     TIPOS_SANGUINEOS,
   84 |     doadores_compativeis_para,
   85 |     tabela_de_compatibilidade,
   86 |     tipos_que_recebem_de,
   87 |     atualizar_preferencia_convocacao,
   88 | )
   89 | from django.conf import settings
   90 | 
   91 | from .triagem_servico import (
   92 |     TriagemExtensaNecessaria,
   93 |     TriagemIncompleta,
   94 |     PerguntaInvalida,
   95 |     TriagemSimplificadaIndisponivel,
   96 |     concluir_triagem,
   97 |     iniciar_triagem,
   98 |     obter_extensa_base,
   99 |     obter_extensa_reutilizavel,
  100 |     editar_pergunta,
  101 |     obter_pergunta_atual,
  102 |     pode_responder,
  103 |     salvar_resposta,
  104 |     voltar_pergunta,
  105 | )
  106 | 
  107 | from .triagem_forms import FormularioPergunta as FormularioPerguntaTriagem
  108 | from .triagem_catalogo import obter_pergunta
  109 | 
  110 | from .validacao_pedido import (
  111 |     aprovar_pedido as aprovar_pedido_servico,
  112 |     marcar_pedido_suspeito as marcar_pedido_suspeito_servico,
  113 |     recusar_pedido as recusar_pedido_servico,
  114 |     solicitar_correcao_pedido as solicitar_correcao_pedido_servico,
  115 |     criar_pedido_pendente,
  116 | )
  117 | 
  118 | 
  119 | class FormularioPergunta(forms.Form):
  120 |     """
  121 |     Formulario dinamico usado pela triagem por etapas.
  122 | 
  123 |     A pergunta vem da camada triagem_servico como um dicionario. O formulario
  124 |     aceita os formatos de resposta mais comuns do projeto sem obrigar cada
  125 |     pergunta a ter uma classe de formulario separada.
  126 |     """
  127 | 
  128 |     def __init__(self, pergunta, *args, valor_inicial=None, **kwargs):
  129 |         super().__init__(*args, **kwargs)
  130 | 
  131 |         self.pergunta = pergunta
  132 | 
  133 |         texto = (
  134 |             pergunta.get("texto")
  135 |             or pergunta.get("pergunta")
  136 |             or pergunta.get("label")
  137 |             or "Resposta"
  138 |         )
  139 | 
  140 |         ajuda = (
  141 |             pergunta.get("explicacao")
  142 |             or pergunta.get("ajuda")
  143 |             or pergunta.get("help_text")
  144 |             or ""
  145 |         )
  146 | 
  147 |         obrigatoria = pergunta.get("obrigatoria", True)
  148 | 
  149 |         tipo = str(
  150 |             pergunta.get("tipo_resposta")
  151 |             or pergunta.get("tipo")
  152 |             or pergunta.get("formato")
  153 |             or "ESCOLHA"
  154 |         ).strip().upper()
  155 | 
  156 |         opcoes = self._normalizar_opcoes(
  157 |             pergunta.get("opcoes")
  158 |             or pergunta.get("alternativas")
  159 |             or pergunta.get("choices")
  160 |             or []
  161 |         )
  162 | 
  163 |         initial = self._normalizar_valor_inicial(valor_inicial)
  164 | 
  165 |         if opcoes:
  166 |             if tipo in {
  167 |                 "MULTIPLAS",
  168 |                 "MULTIPLA_SELECAO",
  169 |                 "MULTIPLA_SELEÇÃO",
  170 |                 "CHECKBOX",
  171 |                 "CHECKBOXES",
  172 |             }:
  173 |                 campo = forms.MultipleChoiceField(
  174 |                     label=texto,
  175 |                     choices=opcoes,
  176 |                     required=obrigatoria,
  177 |                     initial=initial,
  178 |                     help_text=ajuda,
  179 |                     widget=forms.CheckboxSelectMultiple,
  180 |                 )
  181 |             else:
  182 |                 campo = forms.ChoiceField(
  183 |                     label=texto,
  184 |                     choices=opcoes,
  185 |                     required=obrigatoria,
  186 |                     initial=initial,
  187 |                     help_text=ajuda,
  188 |                     widget=forms.RadioSelect,
  189 |                 )
  190 | 
  191 |         elif tipo in {"SIM_NAO", "SIM/NÃO", "SIM/NAO", "BOOLEAN", "BOOL"}:
  192 |             campo = forms.ChoiceField(
  193 |                 label=texto,
  194 |                 choices=[
  195 |                     ("SIM", "Sim"),
  196 |                     ("NAO", "Não"),
  197 |                     ("NAO_SEI", "Não sei"),
  198 |                 ],
  199 |                 required=obrigatoria,
  200 |                 initial=initial,
  201 |                 help_text=ajuda,
  202 |                 widget=forms.RadioSelect,
  203 |             )
  204 | 
  205 |         elif tipo in {"DATA", "DATE"}:
  206 |             campo = forms.DateField(
  207 |                 label=texto,
  208 |                 required=obrigatoria,
  209 |                 initial=initial,
  210 |                 help_text=ajuda,
  211 |                 widget=forms.DateInput(attrs={"type": "date"}),
  212 |             )
  213 | 
  214 |         elif tipo in {
  215 |             "NUMERO",
  216 |             "NÚMERO",
  217 |             "NUMBER",
  218 |             "INTEIRO",
  219 |             "INTEGER",
  220 |             "DECIMAL",
  221 |         }:
  222 |             campo = forms.DecimalField(
  223 |                 label=texto,
  224 |                 required=obrigatoria,
  225 |                 initial=initial,
  226 |                 help_text=ajuda,
  227 |             )
  228 | 
  229 |         else:
  230 |             campo = forms.CharField(
  231 |                 label=texto,
  232 |                 required=obrigatoria,
  233 |                 initial=initial,
  234 |                 help_text=ajuda,
  235 |                 max_length=pergunta.get("max_length", 500),
  236 |                 widget=forms.Textarea(attrs={"rows": 3})
  237 |                 if tipo in {"TEXTO", "TEXT", "TEXTAREA"}
  238 |                 else forms.TextInput(),
  239 |             )
  240 | 
  241 |         self.fields["valor"] = campo
  242 | 
  243 |     @staticmethod
  244 |     def _primeiro_valor(dados, chaves):
  245 |         for chave in chaves:
  246 |             if chave in dados and dados[chave] is not None:
  247 |                 return dados[chave]
  248 | 
  249 |         return None
  250 | 
  251 |     @classmethod
  252 |     def _normalizar_opcoes(cls, opcoes):
  253 |         """
  254 |         Converte opcoes em pares (valor, rotulo).
  255 | 
  256 |         Aceita:
  257 | 
  258 |         - lista de dicionarios;
  259 | 
  260 |         - lista de tuplas;
  261 | 
  262 |         - lista de textos;
  263 | 
  264 |         - dicionario no formato codigo -> rotulo.
  265 |         """
  266 | 
  267 |         if isinstance(opcoes, dict):
  268 |             return [
  269 |                 (str(valor), str(rotulo))
  270 |                 for valor, rotulo in opcoes.items()
  271 |             ]
  272 | 
  273 |         resultado = []
  274 | 
  275 |         for opcao in opcoes:
  276 |             if isinstance(opcao, dict):
  277 |                 valor = cls._primeiro_valor(
  278 |                     opcao,
  279 |                     (
  280 |                         "codigo",
  281 |                         "codigo_resposta",
  282 |                         "valor",
  283 |                         "value",
  284 |                         "id",
  285 |                         "chave",
  286 |                     ),
  287 |                 )
  288 | 
  289 |                 rotulo = cls._primeiro_valor(
  290 |                     opcao,
  291 |                     (
  292 |                         "texto",
  293 |                         "resposta_label",
  294 |                         "label",
  295 |                         "rotulo",
  296 |                         "nome",
  297 |                     ),
  298 |                 )
  299 | 
  300 |                 if valor is None and rotulo is not None:
  301 |                     valor = rotulo
  302 | 
  303 |                 if valor is not None:
  304 |                     resultado.append(
  305 |                         (
  306 |                             str(valor),
  307 |                             str(rotulo if rotulo is not None else valor),
  308 |                         )
  309 |                     )
  310 | 
  311 |             elif isinstance(opcao, (list, tuple)) and len(opcao) >= 2:
  312 |                 resultado.append((str(opcao[0]), str(opcao[1])))
  313 | 
  314 |             else:
  315 |                 resultado.append((str(opcao), str(opcao)))
  316 | 
  317 |         return resultado
  318 | 
  319 |     @classmethod
  320 |     def _normalizar_valor_inicial(cls, valor):
  321 |         if not isinstance(valor, dict):
  322 |             return valor
  323 | 
  324 |         return cls._primeiro_valor(
  325 |             valor,
  326 |             (
  327 |                 "valor",
  328 |                 "codigo",
  329 |                 "codigo_resposta",
  330 |                 "resposta",
  331 |                 "opcao",
  332 |                 "data",
  333 |                 "numero",
  334 |                 "texto",
  335 |             ),
  336 |         )
  337 | 
  338 | 
  339 | POSTOS_COLETA = [
  340 |     {
  341 |         "nome": "Hemocentro Central Elo",
  342 |         "cidade": "Sao Paulo",
  343 |         "estado": "SP",
  344 |         "endereco": "Av. Paulista, 1000",
  345 |         "horario": "Segunda a sexta, 8h as 17h",
  346 |     },
  347 |     {
  348 |         "nome": "Banco de Sangue Vida",
  349 |         "cidade": "Campinas",
  350 |         "estado": "SP",
  351 |         "endereco": "Rua das Flores, 250",
  352 |         "horario": "Segunda a sabado, 7h as 13h",
  353 |     },
  354 |     {
  355 |         "nome": "Unidade Hematologica Norte",
  356 |         "cidade": "Santos",
  357 |         "estado": "SP",
  358 |         "endereco": "Rua do Porto, 75",
  359 |         "horario": "Terca a sexta, 9h as 16h",
  360 |     },
  361 | ]
  362 | 
  363 | 
  364 | ESTOQUE_GERAL = [
  365 |     {"tipo": "O-", "nivel": "Critico", "percentual": 18},
  366 |     {"tipo": "O+", "nivel": "Baixo", "percentual": 32},
  367 |     {"tipo": "A+", "nivel": "Estavel", "percentual": 64},
  368 |     {"tipo": "A-", "nivel": "Baixo", "percentual": 28},
  369 |     {"tipo": "B+", "nivel": "Estavel", "percentual": 58},
  370 |     {"tipo": "B-", "nivel": "Critico", "percentual": 16},
  371 |     {"tipo": "AB+", "nivel": "Estavel", "percentual": 70},
  372 |     {"tipo": "AB-", "nivel": "Baixo", "percentual": 25},
  373 | ]
  374 | 
  375 | 
  376 | CAMPANHAS_ATIVAS = [
  377 |     {
  378 |         "titulo": "Mutirao de inverno",
  379 |         "cidade": "Sao Paulo",
  380 |         "data": "24/08/2026",
  381 |     },
  382 |     {
  383 |         "titulo": "Semana do doador universitario",
  384 |         "cidade": "Campinas",
  385 |         "data": "29/08/2026",
  386 |     },
  387 | ]
  388 | 
  389 | 
  390 | PAINEIS_POR_PERFIL = {
  391 |     Usuario.Perfil.DOADOR: {
  392 |         "rotulo": "Doador",
  393 |         "titulo": "Painel do doador",
  394 |         "descricao": "Acompanhe sua jornada de doacao e encontre oportunidades para ajudar.",
  395 |         "acoes": [
  396 |             "Responder ou continuar a triagem de doacao.",
  397 |             "Ver campanhas de doacao ativas.",
  398 |             "Consultar pedidos de sangue em andamento.",
  399 |             "Consultar o estoque publico dos Hemocentros.",
  400 |             "Encontrar postos de coleta.",
  401 |             "Consultar a compatibilidade sanguinea.",
  402 |         ],
  403 |         "mostra_triagem": True,
  404 |         "mostra_campanhas": True,
  405 |         "mostra_pedidos": True,
  406 |         "mostra_estoque_publico": True,
  407 |         "mostra_postos": True,
  408 |     },
  409 |     Usuario.Perfil.RECEPTOR: {
  410 |         "rotulo": "Receptor / Solicitante",
  411 |         "titulo": "Painel do receptor",
  412 |         "descricao": "Acompanhe pedidos de sangue e consulte a disponibilidade publica.",
  413 |         "acoes": [
  414 |             "Ver estoque publico dos Hemocentros.",
  415 |             "Consultar pedidos de sangue ativos.",
  416 |             "Enviar solicitacao de pedido ao Hemocentro.",
  417 |             "Consultar a compatibilidade sanguinea.",
  418 |         ],
  419 |         "mostra_triagem": False,
  420 |         "mostra_campanhas": False,
  421 |         "mostra_pedidos": True,
  422 |         "mostra_estoque_publico": True,
  423 |         "mostra_postos": True,
  424 |     },
  425 |     Usuario.Perfil.OBSERVADOR: {
  426 |         "rotulo": "Observador",
  427 |         "titulo": "Painel do observador",
  428 |         "descricao": "Consulte informacoes publicas sobre campanhas, pedidos, postos e estoques.",
  429 |         "acoes": [
  430 |             "Ver estoque publico dos Hemocentros.",
  431 |             "Consultar postos de coleta.",
  432 |             "Acompanhar pedidos publicos.",
  433 |             "Acompanhar campanhas publicas.",
  434 |         ],
  435 |         "mostra_triagem": False,
  436 |         "mostra_campanhas": True,
  437 |         "mostra_pedidos": True,
  438 |         "mostra_estoque_publico": True,
  439 |         "mostra_postos": True,
  440 |     },
  441 |     Usuario.Perfil.HEMOCENTRO: {
  442 |         "rotulo": "Hemocentro",
  443 |         "titulo": "Painel do hemocentro",
  444 |         "descricao": "Acompanhe a validacao institucional e gerencie recursos liberados.",
  445 |         "acoes": [
  446 |             "Acompanhar o status da validacao institucional.",
  447 |             "Cadastrar estoque quando o cadastro estiver aprovado.",
  448 |             "Atualizar estoque quando o cadastro estiver aprovado.",
  449 |             "Consultar historico de movimentacoes de estoque.",
  450 |             "Analisar solicitações destinadas ao Hemocentro.",
  451 |         ],
  452 |         "mostra_triagem": False,
  453 |         "mostra_campanhas": False,
  454 |         "mostra_pedidos": True,
  455 |         "mostra_estoque_publico": False,
  456 |         "mostra_postos": False,
  457 |     },
  458 |     Usuario.Perfil.ADMINISTRADOR: {
  459 |         "rotulo": "Administrador",
  460 |         "titulo": "Painel administrativo",
  461 |         "descricao": "Gerencie validacoes institucionais e acompanhe operacoes sensiveis.",
  462 |         "acoes": [
  463 |             "Aprovar Hemocentros.",
  464 |             "Recusar Hemocentros.",
  465 |             "Solicitar correcao cadastral de Hemocentros.",
  466 |             "Acessar o painel administrativo do Django.",
  467 |         ],
  468 |         "mostra_triagem": False,
  469 |         "mostra_campanhas": True,
  470 |         "mostra_pedidos": True,
  471 |         "mostra_estoque_publico": True,
  472 |         "mostra_postos": False,
  473 |     },
  474 | }
  475 | 
  476 | 
  477 | def montar_visibilidade_dashboard(usuario, painel):
  478 |     """
  479 |     Centraliza a particularizacao do dashboard por perfil.
  480 | 
  481 |     O dicionario PAINEIS_POR_PERFIL define o que cada tipo de conta pode ver
  482 |     por padrao. Esta funcao acrescenta regras que dependem do estado atual do
  483 |     usuario, como Hemocentro aprovado e Administrador.
  484 |     """
  485 | 
  486 |     hemocentro_aprovado = (
  487 |         usuario.perfil == Usuario.Perfil.HEMOCENTRO
  488 |         and usuario.status_validacao == Usuario.StatusValidacaoHemocentro.APROVADO
  489 |     )
  490 | 
  491 |     administrador = usuario_e_administrador(usuario)
  492 | 
  493 |     return {
  494 |         "mostra_triagem": painel.get("mostra_triagem", False),
  495 |         "mostra_campanhas": painel.get("mostra_campanhas", False),
  496 |         "mostra_pedidos": painel.get("mostra_pedidos", False) and (
  497 |             usuario.perfil != Usuario.Perfil.HEMOCENTRO or hemocentro_aprovado
  498 |         ),
  499 |         "mostra_estoque_publico": painel.get("mostra_estoque_publico", False),
  500 |         "mostra_postos": painel.get("mostra_postos", False),
  501 |         "pode_solicitar_divulgacao": usuario.perfil == Usuario.Perfil.RECEPTOR,
  502 |         "mostra_status_hemocentro": usuario.perfil == Usuario.Perfil.HEMOCENTRO,
  503 |         "pode_solicitar_pedido": usuario.perfil == Usuario.Perfil.RECEPTOR,
  504 |         "pode_gerenciar_estoque": hemocentro_aprovado,
  505 |         "pode_analisar_pedidos": hemocentro_aprovado,
  506 |         "pode_aprovar_hemocentros": administrador,
  507 |         "pode_moderar_pedidos": administrador,
  508 |     }
  509 | 
  510 | 
  511 | def obter_ip(request):
  512 |     """Extrai o IP usado no registro do consentimento LGPD."""
  513 | 
  514 |     encaminhado = request.META.get("HTTP_X_FORWARDED_FOR")
  515 | 
  516 |     if encaminhado:
  517 |         return encaminhado.split(",")[0].strip()
  518 | 
  519 |     return request.META.get("REMOTE_ADDR")
  520 | 
  521 | 
  522 | def filtrar_postos(consulta):
  523 |     """Filtra a lista publica por nome, cidade, estado ou endereco."""
  524 | 
  525 |     termo = (consulta or "").strip().lower()
  526 | 
  527 |     if not termo:
  528 |         return POSTOS_COLETA
  529 | 
  530 |     return [
  531 |         posto
  532 |         for posto in POSTOS_COLETA
  533 |         if termo
  534 |         in " ".join(
  535 |             [
  536 |                 posto["nome"],
  537 |                 posto["cidade"],
  538 |                 posto["estado"],
  539 |                 posto["endereco"],
  540 |             ]
  541 |         ).lower()
  542 |     ]
  543 | 
  544 | 
  545 | def exigir_administrador(usuario):
  546 |     """Bloqueia acoes institucionais para quem nao e administrador."""
  547 | 
  548 |     if not usuario_e_administrador(usuario):
  549 |         raise PermissionDenied(
  550 |             "Somente administradores podem executar esta acao."
  551 |         )
  552 | 
  553 | 
  554 | def obter_hemocentro_ou_404(id_hemocentro):
  555 |     """Busca somente contas cadastradas com perfil Hemocentro."""
  556 | 
  557 |     return get_object_or_404(
  558 |         Usuario,
  559 |         pk=id_hemocentro,
  560 |         perfil=Usuario.Perfil.HEMOCENTRO,
  561 |     )
  562 | 
  563 | 
  564 | def inicio(request):
  565 |     """Mostra o acesso publico usado pelo ator Visitante."""
  566 | 
  567 |     consulta = request.GET.get("q", "")
  568 | 
  569 |     contexto = {
  570 |         "consulta": consulta,
  571 |         "postos": filtrar_postos(consulta),
  572 |         "estoque_geral": ESTOQUE_GERAL,
  573 |         "pedidos_ativos": (
  574 |             PedidoSangue.objects
  575 |             .select_related("hemocentro_destino")
  576 |             .filter(status=PedidoSangue.Status.PUBLICADA)
  577 |             .order_by("-data_criacao")[:10]
  578 |         ),
  579 |     }
  580 | 
  581 |     return render(
  582 |         request,
  583 |         "accounts/inicio.html",
  584 |         contexto,
  585 |     )
  586 | 
  587 | 
  588 | def cadastro(request):
  589 |     """
  590 |     Exibe e processa o cadastro de usuarios.
  591 | 
  592 |     Hemocentro:
  593 | 
  594 |     - cria a conta;
  595 | 
  596 |     - fica com status PENDENTE;
  597 | 
  598 |     - registra consentimento LGPD;
  599 | 
  600 |     - entra no sistema;
  601 | 
  602 |     - recebe a mensagem de aguardando aprovacao.
  603 |     """
  604 | 
  605 |     if request.user.is_authenticated:
  606 |         return redirect("accounts:dashboard")
  607 | 
  608 |     if request.method == "POST":
  609 |         form = CadastroUsuarioForm(request.POST)
  610 | 
  611 |         if form.is_valid():
  612 |             with transaction.atomic():
  613 |                 usuario = form.save()
  614 | 
  615 |                 # Todo Hemocentro novo deve comecar como PENDENTE.
  616 |                 if usuario.perfil == Usuario.Perfil.HEMOCENTRO:
  617 |                     usuario.status_validacao = (
  618 |                         Usuario.StatusValidacaoHemocentro.PENDENTE
  619 |                     )
  620 | 
  621 |                     usuario.save(
  622 |                         update_fields=["status_validacao"]
  623 |                     )
  624 | 
  625 |                 # Registro do aceite da LGPD.
  626 |                 ConsentimentoLGPD.objects.create(
  627 |                     usuario=usuario,
  628 |                     tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL,
  629 |                     versao_termo="1.0",
  630 |                     aceito=True,
  631 |                     ip=obter_ip(request),
  632 |                 )
  633 | 
  634 |                 if usuario.perfil == Usuario.Perfil.DOADOR:
  635 |                     atualizar_preferencia_convocacao(
  636 |                         usuario, form.cleaned_data["aceita_notificacoes_pedidos"], request,
  637 |                     )
  638 | 
  639 |             # Cria a sessao do usuario.
  640 |             login(request, usuario)
  641 | 
  642 |             # Mensagem especifica para Hemocentro.
  643 |             if usuario.perfil == Usuario.Perfil.HEMOCENTRO:
  644 |                 messages.success(
  645 |                     request,
  646 |                     (
  647 |                         "Cadastro realizado com sucesso! "
  648 |                         "Seu cadastro de Hemocentro esta aguardando "
  649 |                         "a aprovacao de um administrador."
  650 |                     ),
  651 |                 )
  652 | 
  653 |             else:
  654 |                 messages.success(
  655 |                     request,
  656 |                     "Cadastro realizado com sucesso.",
  657 |                 )
  658 | 
  659 |             return redirect("accounts:dashboard")
  660 | 
  661 |         # Se o formulario tiver erro, permanece na pagina
  662 |         # e o template podera exibir os erros de cada campo.
  663 |         messages.error(
  664 |             request,
  665 |             (
  666 |                 "O cadastro nao foi concluido. "
  667 |                 "Corrija os erros destacados no formulario."
  668 |             ),
  669 |         )
  670 | 
  671 |     else:
  672 |         form = CadastroUsuarioForm()
  673 | 
  674 |     return render(
  675 |         request,
  676 |         "accounts/cadastro.html",
  677 |         {"form": form},
  678 |     )
  679 | 
  680 | 
  681 | def compatibilidade_sanguinea(request):
  682 |     """Exibe a tabela e a consulta de compatibilidade sanguinea."""
  683 | 
  684 |     tipo_selecionado = request.GET.get("tipo", "")
  685 | 
  686 |     compatibilidade_selecionada = None
  687 |     tipo_invalido = False
  688 | 
  689 |     if tipo_selecionado:
  690 |         tipo_selecionado = tipo_selecionado.strip().upper()
  691 | 
  692 |         try:
  693 |             compatibilidade_selecionada = {
  694 |                 "tipo": tipo_selecionado,
  695 |                 "doar_para": tipos_que_recebem_de(
  696 |                     tipo_selecionado
  697 |                 ),
  698 |                 "receber_de": doadores_compativeis_para(
  699 |                     tipo_selecionado
  700 |                 ),
  701 |             }
  702 | 
  703 |         except ValueError:
  704 |             tipo_invalido = True
  705 | 
  706 |     return render(
  707 |         request,
  708 |         "accounts/compatibilidade_sanguinea.html",
  709 |         {
  710 |             "tipos_sanguineos": TIPOS_SANGUINEOS,
  711 |             "tipo_selecionado": tipo_selecionado,
  712 |             "compatibilidade_selecionada": compatibilidade_selecionada,
  713 |             "tipo_invalido": tipo_invalido,
  714 |             "tabela_compatibilidade": tabela_de_compatibilidade(),
  715 |         },
  716 |     )
  717 | 
  718 | 
  719 | @login_required
  720 | def dashboard(request):
  721 |     """Mostra o painel protegido particularizado pelo perfil do usuario."""
  722 | 
  723 |     if request.method == "POST":
  724 |         if request.POST.get("acao") == "marcar_notificacao_lida":
  725 |             try:
  726 |                 id_notificacao = int(request.POST.get("id_notificacao", ""))
  727 |             except (TypeError, ValueError):
  728 |                 raise Http404("Notificacao nao encontrada.")
  729 |             notificacao = get_object_or_404(
  730 |                 request.user.notificacoes, pk=id_notificacao,
  731 |             )
  732 |             request.user.notificacoes.filter(pk=notificacao.pk, lida=False).update(
  733 |                 lida=True, lida_em=timezone.now(),
  734 |             )
  735 |             return redirect("accounts:dashboard")
  736 |         if request.user.perfil != Usuario.Perfil.DOADOR:
  737 |             raise PermissionDenied("Somente Doadores podem configurar convocacoes.")
  738 |         form = PreferenciaConvocacaoForm(request.POST)
  739 |         if form.is_valid():
  740 |             atualizar_preferencia_convocacao(
  741 |                 request.user, form.cleaned_data["aceita_convocacoes"], request,
  742 |             )
  743 |             messages.success(request, "Preferencia de convocacao salva.")
  744 |             return redirect("accounts:dashboard")
  745 | 
  746 |     preferencia_convocacao = None
  747 |     if request.user.perfil == Usuario.Perfil.DOADOR:
  748 |         consentimento_vigente = request.user.consentimentos_lgpd.filter(
  749 |             tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
  750 |             versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO,
  751 |             aceito=True, revogado_em__isnull=True,
  752 |         ).exists()
  753 |         preferencia_convocacao = PreferenciaConvocacaoForm(initial={
  754 |             "aceita_convocacoes": request.user.aceita_notificacoes_pedidos and consentimento_vigente,
  755 |         })
  756 | 
  757 |     painel = PAINEIS_POR_PERFIL.get(
  758 |         request.user.perfil,
  759 |         PAINEIS_POR_PERFIL[Usuario.Perfil.OBSERVADOR],
  760 |     )
  761 | 
  762 |     if request.user.perfil == Usuario.Perfil.HEMOCENTRO and not hemocentro_aprovado(request.user):
  763 |         painel = {**painel, "acoes": ["Acompanhar o status da validacao institucional."]}
  764 |     elif hemocentro_aprovado(request.user):
  765 |         painel = {**painel, "acoes": [*painel["acoes"], "Analisar e publicar solicitacoes destinadas ao proprio Hemocentro."]}
  766 | 
  767 |     # Busca a ultima analise administrativa do Hemocentro.
  768 |     validacao_atual = None
  769 | 
  770 |     if request.user.perfil == Usuario.Perfil.HEMOCENTRO:
  771 |         validacao_atual = (
  772 |             ValidacaoHemocentro.objects
  773 |             .filter(
  774 |                 hemocentro=request.user
  775 |             )
  776 |             .order_by("-data_analise")
  777 |             .first()
  778 |         )
  779 | 
  780 |     # O resumo usa apenas registros do usuário autenticado. As respostas
  781 |     # detalhadas não são expostas no painel geral.
  782 |     ultima_triagem = None
  783 | 
  784 |     if pode_responder(request.user):
  785 |         ultima_triagem = request.user.triagens.order_by("-iniciada_em").first()
  786 | 
  787 |     visibilidade = montar_visibilidade_dashboard(
  788 |         request.user,
  789 |         painel,
  790 |     )
  791 | 
  792 |     notificacoes_usuario = request.user.notificacoes.order_by("-criada_em", "-pk")
  793 |     notificacoes_dashboard = Paginator(notificacoes_usuario, 10).get_page(
  794 |         request.GET.get("pagina_notificacoes"),
  795 |     )
  796 | 
  797 |     contexto = {
  798 |         "painel": painel,
  799 |         "visibilidade": visibilidade,
  800 |         "postos": POSTOS_COLETA,
  801 |         "estoque_geral": ESTOQUE_GERAL,
  802 |         "pedidos_ativos": (
  803 |             PedidoSangue.objects
  804 |             .select_related("hemocentro_destino")
  805 |             .filter(status=PedidoSangue.Status.PUBLICADA)
  806 |             .order_by("-data_criacao")[:10]
  807 |         ),
  808 |         "campanhas_ativas": CAMPANHAS_ATIVAS,
  809 |         "validacao_atual": validacao_atual,
  810 |         "ultima_triagem": ultima_triagem,
  811 |         "notificacoes_dashboard": notificacoes_dashboard,
  812 |         "notificacoes_nao_lidas": notificacoes_usuario.filter(lida=False).count(),
  813 |         "preferencia_convocacao": preferencia_convocacao,
  814 |         "convocacao_intervalo_horas": settings.CONVOCACAO_INTERVALO_HORAS,
  815 |         "convocacao_limite": settings.CONVOCACAO_LIMITE_NOTIFICACOES,
  816 |     }
  817 | 
  818 |     return render(
  819 |         request,
  820 |         "accounts/dashboard.html",
  821 |         contexto,
  822 |     )
  823 | 
  824 | 
  825 | @login_required
  826 | def painel_aprovacao_hemocentros(request):
  827 |     """Mostra a tela administrativa de aprovacao de Hemocentros."""
  828 | 
  829 |     exigir_administrador(request.user)
  830 | 
  831 |     hemocentros = (
  832 |         Usuario.objects
  833 |         .filter(
  834 |             perfil=Usuario.Perfil.HEMOCENTRO,
  835 |             status_validacao=(
  836 |                 Usuario.StatusValidacaoHemocentro.PENDENTE
  837 |             ),
  838 |         )
  839 |         .order_by("date_joined")
  840 |     )
  841 | 
  842 |     contexto = {
  843 |         "hemocentros": hemocentros,
  844 |     }
  845 | 
  846 |     return render(
  847 |         request,
  848 |         "accounts/painel_aprovacao_hemocentros.html",
  849 |         contexto,
  850 |     )
  851 | 
  852 | 
  853 | @login_required
  854 | def hemocentros_pendentes(request):
  855 |     """Retorna os Hemocentros que ainda aguardam decisao administrativa."""
  856 | 
  857 |     exigir_administrador(request.user)
  858 | 
  859 |     hemocentros = (
  860 |         Usuario.objects
  861 |         .filter(
  862 |             perfil=Usuario.Perfil.HEMOCENTRO,
  863 |             status_validacao=(
  864 |                 Usuario.StatusValidacaoHemocentro.PENDENTE
  865 |             ),
  866 |         )
  867 |         .order_by("date_joined")
  868 |     )
  869 | 
  870 |     dados = [
  871 |         {
  872 |             "id_hemocentro": hemocentro.pk,
  873 |             "nome": hemocentro.nome,
  874 |             "email": hemocentro.email,
  875 |             "cnpj": hemocentro.cnpj,
  876 |             "cidade": hemocentro.cidade,
  877 |             "estado": hemocentro.estado,
  878 |             "status_validacao": hemocentro.status_validacao,
  879 |             "data_cadastro": hemocentro.date_joined.isoformat(),
  880 |         }
  881 |         for hemocentro in hemocentros
  882 |     ]
  883 | 
  884 |     return JsonResponse(
  885 |         {
  886 |             "hemocentros": dados
  887 |         }
  888 |     )
  889 | 
  890 | 
  891 | @login_required
  892 | @require_POST
  893 | def aprovar_hemocentro(request, id_hemocentro):
  894 |     """Acao administrativa para aprovar um Hemocentro."""
  895 | 
  896 |     exigir_administrador(request.user)
  897 | 
  898 |     hemocentro = obter_hemocentro_ou_404(
  899 |         id_hemocentro
  900 |     )
  901 | 
  902 |     aprovar_hemocentro_servico(
  903 |         hemocentro=hemocentro,
  904 |         admin=request.user,
  905 |         parecer=request.POST.get("parecer", ""),
  906 |         request=request,
  907 |     )
  908 | 
  909 |     messages.success(
  910 |         request,
  911 |         "Hemocentro aprovado com sucesso.",
  912 |     )
  913 | 
  914 |     return redirect(
  915 |         "accounts:painel_aprovacao_hemocentros"
  916 |     )
  917 | 
  918 | 
  919 | @login_required
  920 | @require_POST
  921 | def recusar_hemocentro(request, id_hemocentro):
  922 |     """Acao administrativa para recusar um Hemocentro."""
  923 | 
  924 |     exigir_administrador(request.user)
  925 | 
  926 |     hemocentro = obter_hemocentro_ou_404(
  927 |         id_hemocentro
  928 |     )
  929 | 
  930 |     recusar_hemocentro_servico(
  931 |         hemocentro=hemocentro,
  932 |         admin=request.user,
  933 |         parecer=request.POST.get("parecer", ""),
  934 |         request=request,
  935 |     )
  936 | 
  937 |     messages.success(
  938 |         request,
  939 |         "Hemocentro recusado com sucesso.",
  940 |     )
  941 | 
  942 |     return redirect(
  943 |         "accounts:painel_aprovacao_hemocentros"
  944 |     )
  945 | 
  946 | 
  947 | @login_required
  948 | @require_POST
  949 | def solicitar_correcao_hemocentro(request, id_hemocentro):
  950 |     """Solicita correcao cadastral para um Hemocentro."""
  951 | 
  952 |     exigir_administrador(request.user)
  953 | 
  954 |     hemocentro = obter_hemocentro_ou_404(
  955 |         id_hemocentro
  956 |     )
  957 | 
  958 |     solicitar_correcao_hemocentro_servico(
  959 |         hemocentro=hemocentro,
  960 |         admin=request.user,
  961 |         parecer=request.POST.get("parecer", ""),
  962 |         request=request,
  963 |     )
  964 | 
  965 |     messages.success(
  966 |         request,
  967 |         "Solicitacao de correcao registrada com sucesso.",
  968 |     )
  969 | 
  970 |     return redirect(
  971 |         "accounts:painel_aprovacao_hemocentros"
  972 |     )
  973 | 
  974 | 
  975 | def triagem_apresentacao(request):
  976 |     """
  977 |     Exibe a apresentação pública da triagem.
  978 | 
  979 |     Somente usuários com perfil permitido podem iniciar a triagem.
  980 | 
  981 |     A modalidade simplificada é liberada quando existe uma triagem
  982 |     extensa concluída que possa ser utilizada como base.
  983 |     """
  984 | 
  985 |     pode_iniciar = False
  986 |     pode_simplificada = False
  987 |     triagem_em_andamento = None
  988 |     ultima_triagem = None
  989 |     extensa_base = None
  990 |     extensa_reutilizavel = None
  991 | 
  992 |     if request.user.is_authenticated:
  993 |         pode_iniciar = pode_responder(request.user)
  994 | 
  995 |         if pode_iniciar:
  996 |             triagens = (
  997 |                 request.user.triagens
  998 |                 .select_related("triagem_base")
  999 |                 .order_by("-iniciada_em")
 1000 |             )
 1001 | 
 1002 |             ultima_triagem = triagens.first()
 1003 | 
 1004 |             triagem_em_andamento = (
 1005 |                 triagens
 1006 |                 .filter(status=Triagem.Status.EM_ANDAMENTO)
 1007 |                 .first()
 1008 |             )
 1009 | 
 1010 |             extensa_base = obter_extensa_base(request.user)
 1011 |             extensa_reutilizavel = obter_extensa_reutilizavel(request.user)
 1012 | 
 1013 |             # A simplificada só fica disponível quando existe
 1014 |             # uma triagem extensa concluída válida como base.
 1015 |             pode_simplificada = extensa_base is not None
 1016 | 
 1017 |     return render(
 1018 |         request,
 1019 |         "accounts/triagem_apresentacao.html",
 1020 |         {
 1021 |             "pode_iniciar": pode_iniciar,
 1022 |             "pode_simplificada": pode_simplificada,
 1023 |             "triagem_em_andamento": triagem_em_andamento,
 1024 |             "ultima_triagem": ultima_triagem,
 1025 |             "triagem_extensa_base": extensa_base,
 1026 |             "triagem_extensa_reutilizavel": extensa_reutilizavel,
 1027 |         },
 1028 |     )
 1029 | 
 1030 | 
 1031 | @login_required
 1032 | def triagem_historico(request):
 1033 |     """
 1034 |     Lista somente as triagens pertencentes ao usuario autenticado.
 1035 | 
 1036 |     O historico mostra tanto triagens em andamento quanto concluidas e
 1037 |     canceladas, permitindo que o template ofereça continuar ou consultar
 1038 |     o resultado conforme o status.
 1039 |     """
 1040 | 
 1041 |     if not pode_responder(request.user):
 1042 |         messages.error(
 1043 |             request,
 1044 |             "A triagem de doacao nao esta disponivel para este perfil.",
 1045 |         )
 1046 | 
 1047 |         registrar_auditoria(
 1048 |             acao=AuditoriaAcaoCritica.Acao.MODERACAO,
 1049 |             resultado=AuditoriaAcaoCritica.Resultado.BLOQUEADO,
 1050 |             usuario=request.user, request=request,
 1051 |             descricao="Tentativa de acesso ao historico de triagens bloqueada.",
 1052 |             metadados={"evento": "TENTATIVA_ACESSO", "rota": "accounts:triagem_historico"},
 1053 |         )
 1054 | 
 1055 |         return redirect("accounts:dashboard")
 1056 | 
 1057 |     triagens = (
 1058 |         request.user.triagens
 1059 |         .select_related("triagem_base")
 1060 |         .order_by("-iniciada_em")
 1061 |     )
 1062 | 
 1063 |     return render(
 1064 |         request,
 1065 |         "accounts/triagem_historico.html",
 1066 |         {
 1067 |             "triagens": triagens,
 1068 |         },
 1069 |     )
 1070 | 
 1071 | 
 1072 | @login_required
 1073 | @require_POST
 1074 | def triagem_iniciar(request, modalidade):
 1075 |     """Inicia ou retoma uma triagem somente após clique explícito."""
 1076 | 
 1077 |     modalidades = {
 1078 |         "extensa": Triagem.Modalidade.EXTENSA,
 1079 |         "simplificada": Triagem.Modalidade.SIMPLIFICADA,
 1080 |     }
 1081 | 
 1082 |     if modalidade not in modalidades:
 1083 |         raise Http404("Modalidade de triagem inexistente.")
 1084 | 
 1085 |     if not pode_responder(request.user):
 1086 |         raise PermissionDenied(
 1087 |             "A triagem está disponível somente para Doador e Receptor."
 1088 |         )
 1089 | 
 1090 |     if request.POST.get("aceite_termo") not in {"on", "1", "true"}:
 1091 |         messages.error(
 1092 |             request,
 1093 |             "Leia e confirme o termo da pré-triagem para continuar.",
 1094 |         )
 1095 |         return redirect("accounts:triagem_apresentacao")
 1096 | 
 1097 |     try:
 1098 |         triagem = iniciar_triagem(
 1099 |             request.user,
 1100 |             modalidades[modalidade],
 1101 |             ip=obter_ip(request),
 1102 |             aceite_termo=True,
 1103 |             reutilizar_respostas=(
 1104 |                 modalidade == "extensa"
 1105 |                 and request.POST.get("reutilizar_respostas")
 1106 |                 in {"on", "1", "true"}
 1107 |             ),
 1108 |         )
 1109 | 
 1110 |     except TriagemSimplificadaIndisponivel:
 1111 |         messages.info(
 1112 |             request,
 1113 |             "Conclua primeiro a triagem extensa para usar a versão simplificada.",
 1114 |         )
 1115 | 
 1116 |         return redirect("accounts:triagem_apresentacao")
 1117 | 
 1118 |     return redirect(
 1119 |         "accounts:triagem_pergunta",
 1120 |         id_triagem=triagem.pk,
 1121 |     )
 1122 | 
 1123 | 
 1124 | def _triagem_do_usuario_ou_404(request, id_triagem):
 1125 |     """Evita que uma conta consulte o questionário privado de outra."""
 1126 | 
 1127 |     if not pode_responder(request.user):
 1128 |         raise PermissionDenied("Somente Doadores podem acessar a triagem.")
 1129 | 
 1130 |     return get_object_or_404(
 1131 |         Triagem,
 1132 |         pk=id_triagem,
 1133 |         usuario=request.user,
 1134 |     )
 1135 | 
 1136 | 
 1137 | @login_required
 1138 | def triagem_pergunta(request, id_triagem):
 1139 |     """Mostra, valida e salva uma única pergunta por página."""
 1140 | 
 1141 |     triagem = _triagem_do_usuario_ou_404(
 1142 |         request,
 1143 |         id_triagem,
 1144 |     )
 1145 | 
 1146 |     if triagem.status == Triagem.Status.CONCLUIDA:
 1147 |         return redirect(
 1148 |             "accounts:triagem_resultado",
 1149 |             id_triagem=triagem.pk,
 1150 |         )
 1151 | 
 1152 |     if triagem.status == Triagem.Status.CANCELADA:
 1153 |         return redirect("accounts:triagem_apresentacao")
 1154 | 
 1155 |     pergunta_para_editar = request.GET.get("pergunta")
 1156 |     if pergunta_para_editar:
 1157 |         try:
 1158 |             editar_pergunta(triagem, pergunta_para_editar)
 1159 |         except PerguntaInvalida as erro:
 1160 |             raise Http404("Pergunta de triagem inexistente.") from erro
 1161 | 
 1162 |     # O botão anterior muda apenas o cursor e não valida campos da página.
 1163 |     if request.method == "POST" and request.POST.get("acao") == "anterior":
 1164 |         voltar_pergunta(triagem)
 1165 | 
 1166 |         return redirect(
 1167 |             "accounts:triagem_pergunta",
 1168 |             id_triagem=triagem.pk,
 1169 |         )
 1170 | 
 1171 |     pergunta = obter_pergunta_atual(triagem)
 1172 | 
 1173 |     if pergunta is None:
 1174 |         return redirect("accounts:triagem_revisao", id_triagem=triagem.pk)
 1175 | 
 1176 |     resposta_anterior = triagem.respostas.filter(
 1177 |         id_pergunta=pergunta["id"]
 1178 |     ).first()
 1179 | 
 1180 |     valor_inicial = resposta_anterior.valor if resposta_anterior else None
 1181 | 
 1182 |     form = FormularioPerguntaTriagem(
 1183 |         pergunta,
 1184 |         request.POST or None,
 1185 |         valor_inicial=valor_inicial,
 1186 |     )
 1187 | 
 1188 |     if request.method == "POST" and form.is_valid():
 1189 |         try:
 1190 |             salvar_resposta(
 1191 |                 triagem,
 1192 |                 pergunta["id"],
 1193 |                 form.cleaned_data["valor"],
 1194 |             )
 1195 | 
 1196 |         except TriagemExtensaNecessaria:
 1197 |             # O serviço já cancelou a rápida antes de solicitar a troca.
 1198 |             nova_extensa = iniciar_triagem(
 1199 |                 request.user,
 1200 |                 Triagem.Modalidade.EXTENSA,
 1201 |                 ip=obter_ip(request),
 1202 |                 aceite_termo=True,
 1203 |             )
 1204 | 
 1205 |             messages.info(
 1206 |                 request,
 1207 |                 "Como o resumo mudou, continue pela triagem extensa.",
 1208 |             )
 1209 | 
 1210 |             return redirect(
 1211 |                 "accounts:triagem_pergunta",
 1212 |                 id_triagem=nova_extensa.pk,
 1213 |             )
 1214 | 
 1215 |         if request.POST.get("acao") == "salvar":
 1216 |             messages.success(request, "Andamento da triagem salvo.")
 1217 | 
 1218 |             return redirect("accounts:triagem_historico")
 1219 | 
 1220 |         # O serviço mantém o cursor na explicação quando a pessoa não entendeu
 1221 |         # e volta ao início quando ela escolhe revisar a confirmação final.
 1222 |         if triagem.pergunta_atual >= len(triagem.fluxo_perguntas):
 1223 |             return redirect("accounts:triagem_revisao", id_triagem=triagem.pk)
 1224 | 
 1225 |         return redirect(
 1226 |             "accounts:triagem_pergunta",
 1227 |             id_triagem=triagem.pk,
 1228 |         )
 1229 | 
 1230 |     return render(
 1231 |         request,
 1232 |         "accounts/triagem_pergunta.html",
 1233 |         {
 1234 |             "triagem": triagem,
 1235 |             "pergunta": pergunta,
 1236 |             "form": form,
 1237 |             "numero_pergunta": triagem.pergunta_atual + 1,
 1238 |             "total_perguntas": len(triagem.fluxo_perguntas),
 1239 |         },
 1240 |     )
 1241 | 
 1242 | 
 1243 | @login_required
 1244 | def triagem_revisao(request, id_triagem):
 1245 |     """Mostra todas as respostas antes do cálculo final."""
 1246 | 
 1247 |     triagem = _triagem_do_usuario_ou_404(request, id_triagem)
 1248 |     if triagem.status == Triagem.Status.CONCLUIDA:
 1249 |         return redirect("accounts:triagem_resultado", id_triagem=triagem.pk)
 1250 |     if triagem.status == Triagem.Status.CANCELADA:
 1251 |         return redirect("accounts:triagem_apresentacao")
 1252 | 
 1253 |     if request.method == "POST" and request.POST.get("acao") == "finalizar":
 1254 |         try:
 1255 |             triagem = concluir_triagem(triagem)
 1256 |         except TriagemIncompleta as erro:
 1257 |             messages.error(request, str(erro))
 1258 |         else:
 1259 |             return redirect("accounts:triagem_resultado", id_triagem=triagem.pk)
 1260 | 
 1261 |     respostas = []
 1262 |     registros = triagem.respostas.order_by("id_resposta")
 1263 |     for resposta in registros:
 1264 |         try:
 1265 |             pergunta = obter_pergunta(resposta.id_pergunta)
 1266 |         except KeyError:
 1267 |             continue
 1268 |         respostas.append(
 1269 |             {
 1270 |                 "id": resposta.id_pergunta,
 1271 |                 "titulo": pergunta["titulo"],
 1272 |                 "resposta": resposta.resposta_label,
 1273 |                 "detalhes": (resposta.valor or {}).get("detalhes", ""),
 1274 |             }
 1275 |         )
 1276 | 
 1277 |     return render(
 1278 |         request,
 1279 |         "accounts/triagem_revisao.html",
 1280 |         {"triagem": triagem, "respostas_revisao": respostas},
 1281 |     )
 1282 | 
 1283 | 
 1284 | @login_required
 1285 | def triagem_resultado(request, id_triagem):
 1286 |     """Mostra a orientação concluída somente ao dono da triagem."""
 1287 | 
 1288 |     triagem = _triagem_do_usuario_ou_404(
 1289 |         request,
 1290 |         id_triagem,
 1291 |     )
 1292 | 
 1293 |     if triagem.status == Triagem.Status.EM_ANDAMENTO:
 1294 |         return redirect(
 1295 |             "accounts:triagem_revisao",
 1296 |             id_triagem=triagem.pk,
 1297 |         )
 1298 | 
 1299 |     if triagem.status == Triagem.Status.CANCELADA:
 1300 |         return redirect("accounts:triagem_historico")
 1301 | 
 1302 |     return render(
 1303 |         request,
 1304 |         "accounts/triagem_resultado.html",
 1305 |         {
 1306 |             "triagem": triagem,
 1307 |         },
 1308 |     )
 1309 | 
 1310 | 
 1311 | def visualizacao_publica_estoque(request):
 1312 |     """
 1313 |     Exibe publicamente os estoques dos Hemocentros aprovados.
 1314 | 
 1315 |     A camada accounts.estoque devolve apenas os dados permitidos para
 1316 |     exibicao publica, sem expor os limites internos usados pelo Hemocentro.
 1317 |     """
 1318 | 
 1319 |     parametros = request.GET.copy()
 1320 |     # Mantém compatibilidade com os parâmetros antigos da tela (q e tipo).
 1321 |     if "q" in parametros and "busca" not in parametros:
 1322 |         parametros["busca"] = parametros.get("q", "")
 1323 |     if "tipo" in parametros and "tipo_sanguineo" not in parametros:
 1324 |         parametros["tipo_sanguineo"] = parametros.get("tipo", "")
 1325 |     if "status" in parametros and "situacao" not in parametros:
 1326 |         parametros["situacao"] = parametros.get("status", "")
 1327 | 
 1328 |     form = FiltroEstoquePublicoForm(parametros or None)
 1329 |     estoques = obter_estoques_publicos()
 1330 | 
 1331 |     if form.is_valid():
 1332 |         tipo = form.cleaned_data.get("tipo_sanguineo")
 1333 |         cidade = (form.cleaned_data.get("cidade") or "").strip().lower()
 1334 |         hemocentro = (form.cleaned_data.get("hemocentro") or "").strip().lower()
 1335 |         situacao = form.cleaned_data.get("situacao")
 1336 |         busca = (form.cleaned_data.get("busca") or "").strip().lower()
 1337 | 
 1338 |         if tipo:
 1339 |             estoques = [
 1340 |                 estoque for estoque in estoques
 1341 |                 if estoque["tipo_sanguineo"] == tipo
 1342 |             ]
 1343 | 
 1344 |         if cidade:
 1345 |             estoques = [
 1346 |                 estoque for estoque in estoques
 1347 |                 if cidade in estoque["cidade"].lower()
 1348 |             ]
 1349 | 
 1350 |         if hemocentro:
 1351 |             estoques = [
 1352 |                 estoque for estoque in estoques
 1353 |                 if hemocentro in estoque["nome"].lower()
 1354 |             ]
 1355 | 
 1356 |         if situacao:
 1357 |             estoques = [
 1358 |                 estoque for estoque in estoques
 1359 |                 if estoque["status_codigo"] == situacao
 1360 |             ]
 1361 | 
 1362 |         if busca:
 1363 |             estoques = [
 1364 |                 estoque for estoque in estoques
 1365 |                 if busca in " ".join(
 1366 |                     [
 1367 |                         estoque["nome"],
 1368 |                         estoque["cidade"],
 1369 |                         estoque["estado"],
 1370 |                         estoque["tipo_sanguineo"],
 1371 |                         estoque["status_label"],
 1372 |                     ]
 1373 |                 ).lower()
 1374 |             ]
 1375 | 
 1376 |     return render(
 1377 |         request,
 1378 |         "accounts/estoque_publico.html",
 1379 |         {
 1380 |             "estoques": estoques,
 1381 |             "form": form,
 1382 |         },
 1383 |     )
 1384 | 
 1385 | 
 1386 | def _formatar_erro_validacao(erro):
 1387 |     """Converte um ValidationError (string, lista ou dict) em texto legivel."""
 1388 | 
 1389 |     if hasattr(erro, "message_dict"):
 1390 |         return "; ".join(
 1391 |             f"{campo}: {', '.join(mensagens)}"
 1392 |             for campo, mensagens in erro.message_dict.items()
 1393 |         )
 1394 | 
 1395 |     return "; ".join(erro.messages)
 1396 | 
 1397 | 
 1398 | @login_required
 1399 | @exigir_hemocentro_aprovado
 1400 | def estoque_hemocentro(request):
 1401 |     """
 1402 |     UC_29 / UC_30 - Mostra o estoque do proprio Hemocentro logado e os
 1403 |     formularios para cadastrar um novo tipo sanguineo ou movimentar um
 1404 |     estoque ja existente.
 1405 |     """
 1406 | 
 1407 |     estoques = (
 1408 |         Estoque.objects
 1409 |         .filter(hemocentro=request.user)
 1410 |         .prefetch_related(
 1411 |             Prefetch(
 1412 |                 "movimentacoes",
 1413 |                 queryset=EstoqueMovimentacao.objects.select_related(
 1414 |                     "usuario_resp"
 1415 |                 ).order_by("-data_hora"),
 1416 |             )
 1417 |         )
 1418 |         .order_by("tipo_sanguineo")
 1419 |     )
 1420 | 
 1421 |     tipos_cadastrados = set(
 1422 |         estoques.values_list("tipo_sanguineo", flat=True)
 1423 |     )
 1424 | 
 1425 |     tipos_disponiveis = [
 1426 |         tipo
 1427 |         for tipo in TIPOS_SANGUINEOS
 1428 |         if tipo not in tipos_cadastrados
 1429 |     ]
 1430 | 
 1431 |     form_cadastro = CadastrarEstoqueForm()
 1432 | 
 1433 |     form_cadastro.fields["tipo_sanguineo"].choices = [
 1434 |         (tipo, tipo)
 1435 |         for tipo in tipos_disponiveis
 1436 |     ]
 1437 | 
 1438 |     return render(
 1439 |         request,
 1440 |         "accounts/estoque_hemocentro.html",
 1441 |         {
 1442 |             "estoques": estoques,
 1443 |             "tipos_disponiveis": tipos_disponiveis,
 1444 |             "form_cadastro": form_cadastro,
 1445 |             "form_movimentacao": MovimentarEstoqueForm(),
 1446 |         },
 1447 |     )
 1448 | 
 1449 | 
 1450 | @login_required
 1451 | @require_POST
 1452 | @exigir_hemocentro_aprovado
 1453 | def cadastrar_estoque_view(request):
 1454 |     """UC_29 - Cria a estrutura de estoque de um tipo sanguineo."""
 1455 | 
 1456 |     form = CadastrarEstoqueForm(request.POST)
 1457 | 
 1458 |     if form.is_valid():
 1459 |         try:
 1460 |             cadastrar_estoque(
 1461 |                 hemocentro=request.user,
 1462 |                 tipo_sanguineo=form.cleaned_data["tipo_sanguineo"],
 1463 |                 quantidade_bolsas=form.cleaned_data["quantidade_bolsas"],
 1464 |                 nivel_minimo=form.cleaned_data["nivel_minimo"],
 1465 |                 nivel_critico=form.cleaned_data["nivel_critico"],
 1466 |                 request=request,
 1467 |             )
 1468 | 
 1469 |         except ValidationError as erro:
 1470 |             messages.error(
 1471 |                 request,
 1472 |                 _formatar_erro_validacao(erro),
 1473 |             )
 1474 | 
 1475 |         else:
 1476 |             messages.success(
 1477 |                 request,
 1478 |                 "Estoque cadastrado com sucesso.",
 1479 |             )
 1480 | 
 1481 |     else:
 1482 |         messages.error(
 1483 |             request,
 1484 |             "Corrija os erros destacados no formulario de cadastro.",
 1485 |         )
 1486 | 
 1487 |     return redirect("accounts:estoque_hemocentro")
 1488 | 
 1489 | 
 1490 | @login_required
 1491 | @require_POST
 1492 | @exigir_hemocentro_aprovado
 1493 | def atualizar_estoque_view(request, id_estoque):
 1494 |     """UC_30 - Registra uma entrada, saida ou ajuste em um estoque existente."""
 1495 | 
 1496 |     estoque = get_object_or_404(
 1497 |         Estoque,
 1498 |         pk=id_estoque,
 1499 |     )
 1500 | 
 1501 |     form = MovimentarEstoqueForm(request.POST)
 1502 | 
 1503 |     if form.is_valid():
 1504 |         try:
 1505 |             registrar_movimentacao_estoque(
 1506 |                 estoque=estoque,
 1507 |                 usuario_resp=request.user,
 1508 |                 tipo_movimento=form.cleaned_data["tipo_movimento"],
 1509 |                 quantidade=form.cleaned_data["quantidade"],
 1510 |                 motivo=form.cleaned_data["motivo"],
 1511 |                 request=request,
 1512 |             )
 1513 | 
 1514 |         except PermissionDenied as erro:
 1515 |             messages.error(
 1516 |                 request,
 1517 |                 str(erro),
 1518 |             )
 1519 | 
 1520 |         except ValidationError as erro:
 1521 |             messages.error(
 1522 |                 request,
 1523 |                 _formatar_erro_validacao(erro),
 1524 |             )
 1525 | 
 1526 |         else:
 1527 |             messages.success(
 1528 |                 request,
 1529 |                 "Estoque atualizado com sucesso.",
 1530 |             )
 1531 | 
 1532 |     else:
 1533 |         messages.error(
 1534 |             request,
 1535 |             "Corrija os erros destacados no formulario de movimentacao.",
 1536 |         )
 1537 | 
 1538 |     return redirect("accounts:estoque_hemocentro")
 1539 | 
 1540 | 
 1541 | @login_required
 1542 | def criar_pedido_sangue(request):
 1543 |     """
 1544 |     Recebe uma solicitação de divulgação, sem publicá-la.
 1545 | 
 1546 |     Apenas Receptor/Solicitante pode enviar solicitacao de pedido.
 1547 | 
 1548 |     Ao salvar, a solicitacao aguarda analise do Hemocentro.
 1549 |     """
 1550 | 
 1551 |     if request.user.perfil != Usuario.Perfil.RECEPTOR:
 1552 |         registrar_auditoria(
 1553 |             acao=AuditoriaAcaoCritica.Acao.MODERACAO,
 1554 |             resultado=AuditoriaAcaoCritica.Resultado.BLOQUEADO,
 1555 |             usuario=request.user, request=request,
 1556 |             descricao="Tentativa de enviar solicitacao de pedido bloqueada.",
 1557 |             metadados={"evento": "TENTATIVA_ACESSO", "rota": "accounts:pedido_publicar"},
 1558 |         )
 1559 |         messages.error(
 1560 |             request,
 1561 |             "Este perfil não envia solicitações de divulgação.",
 1562 |         )
 1563 | 
 1564 |         return redirect("accounts:dashboard")
 1565 | 
 1566 |     if request.method == "POST":
 1567 |         form = PedidoSangueForm(request.POST)
 1568 | 
 1569 |         if form.is_valid():
 1570 |             try:
 1571 |                 pedido = criar_pedido_pendente(
 1572 |                     dados=form.cleaned_data,
 1573 |                     solicitante=(
 1574 |                         request.user if request.user.is_authenticated else None
 1575 |                     ),
 1576 |                 )
 1577 | 
 1578 |                 mensagem = (
 1579 |                     "Solicitação enviada para análise do Hemocentro. "
 1580 |                     f"Protocolo {pedido.pk}."
 1581 |                 )
 1582 |                 if pedido.duplicidade_suspeita:
 1583 |                     mensagem += " Há uma solicitação semelhante; ela será analisada."
 1584 |                 messages.success(request, mensagem)
 1585 | 
 1586 |                 if request.user.is_authenticated:
 1587 |                     return redirect("accounts:minhas_solicitacoes")
 1588 |                 return redirect("accounts:consultar_pedidos")
 1589 | 
 1590 |             except ValidationError as erro:
 1591 |                 form.add_error(None, erro)
 1592 | 
 1593 |     else:
 1594 |         form = PedidoSangueForm()
 1595 | 
 1596 |     return render(
 1597 |         request,
 1598 |         "accounts/pedido_publicar.html",
 1599 |         {
 1600 |             "form": form,
 1601 |         },
 1602 |     )
 1603 | 
 1604 | 
 1605 | @login_required
 1606 | def minhas_solicitacoes(request):
 1607 |     """Lista somente as solicitações enviadas pelo usuário autenticado."""
 1608 | 
 1609 |     solicitacoes = (
 1610 |         PedidoSangue.objects
 1611 |         .select_related("hemocentro_destino")
 1612 |         .prefetch_related(
 1613 |             Prefetch(
 1614 |                 "validacoes",
 1615 |                 queryset=ValidacaoPedido.objects.select_related("moderador"),
 1616 |             )
 1617 |         )
 1618 |         .filter(solicitante=request.user)
 1619 |         .order_by("-data_criacao")
 1620 |     )
 1621 | 
 1622 |     status = request.GET.get("status")
 1623 |     if status in dict(PedidoSangue.Status.choices):
 1624 |         solicitacoes = solicitacoes.filter(status=status)
 1625 | 
 1626 |     return render(
 1627 |         request,
 1628 |         "accounts/minhas_solicitacoes.html",
 1629 |         {
 1630 |             "solicitacoes": solicitacoes,
 1631 |             "status_opcoes": PedidoSangue.Status.choices,
 1632 |             "status_atual": status or "",
 1633 |         },
 1634 |     )
 1635 | 
 1636 | 
 1637 | @login_required
 1638 | @exigir_hemocentro_aprovado
 1639 | def painel_pedidos_hemocentro(request):
 1640 |     """Fila de solicitações destinadas ao Hemocentro aprovado logado."""
 1641 | 
 1642 |     PedidoSangue.objects.filter(
 1643 |         hemocentro_destino=request.user,
 1644 |         status=PedidoSangue.Status.ENVIADA,
 1645 |     ).update(status=PedidoSangue.Status.EM_ANALISE)
 1646 | 
 1647 |     solicitacoes = (
 1648 |         PedidoSangue.objects
 1649 |         .select_related("solicitante", "hemocentro_destino")
 1650 |         .filter(hemocentro_destino=request.user)
 1651 |         .exclude(status=PedidoSangue.Status.ENCERRADA)
 1652 |         .order_by("-data_criacao")
 1653 |     )
 1654 |     status = request.GET.get("status")
 1655 |     if status in dict(PedidoSangue.Status.choices):
 1656 |         solicitacoes = solicitacoes.filter(status=status)
 1657 | 
 1658 |     return render(
 1659 |         request,
 1660 |         "accounts/painel_validacao_pedidos.html",
 1661 |         {
 1662 |             "solicitacoes": solicitacoes,
 1663 |             "status_opcoes": PedidoSangue.Status.choices,
 1664 |         },
 1665 |     )
 1666 | 
 1667 | 
 1668 | def consultar_pedidos(request):
 1669 |     """
 1670 |     UC_18 - Consultar Pedidos.
 1671 | 
 1672 |     Exibe apenas pedidos ativos e aplica filtros por tipo sanguineo,
 1673 |     urgencia, cidade, hemocentro e data. A ordenacao prioriza urgencia
 1674 |     e depois os mais recentes.
 1675 |     """
 1676 | 
 1677 |     form = FiltroPedidoSangueForm(request.GET or None)
 1678 | 
 1679 |     pedidos = (
 1680 |         PedidoSangue.objects
 1681 |         .select_related("hemocentro_destino")
 1682 |         .filter(
 1683 |             status=PedidoSangue.Status.PUBLICADA,
 1684 |             hemocentro_destino__perfil=Usuario.Perfil.HEMOCENTRO,
 1685 |             hemocentro_destino__status_validacao=(
 1686 |                 Usuario.StatusValidacaoHemocentro.APROVADO
 1687 |             ),
 1688 |         )
 1689 |     )
 1690 | 
 1691 |     if form.is_valid():
 1692 |         tipo = form.cleaned_data.get("tipo_sanguineo")
 1693 |         urgencia = form.cleaned_data.get("urgencia")
 1694 |         cidade = form.cleaned_data.get("cidade")
 1695 |         hemocentro = form.cleaned_data.get("hemocentro")
 1696 |         data = form.cleaned_data.get("data")
 1697 |         status = form.cleaned_data.get("status")
 1698 | 
 1699 |         # A consulta pública nunca pode revelar solicitações em análise,
 1700 |         # recusadas ou dados ainda não publicados.
 1701 |         if status and status != PedidoSangue.Status.PUBLICADA:
 1702 |             pedidos = pedidos.none()
 1703 | 
 1704 |         if tipo:
 1705 |             pedidos = pedidos.filter(tipo_sanguineo=tipo)
 1706 | 
 1707 |         if urgencia:
 1708 |             pedidos = pedidos.filter(urgencia=urgencia)
 1709 | 
 1710 |         if cidade:
 1711 |             pedidos = pedidos.filter(cidade__icontains=cidade)
 1712 | 
 1713 |         if hemocentro:
 1714 |             pedidos = pedidos.filter(
 1715 |                 hemocentro_destino__nome__icontains=hemocentro
 1716 |             )
 1717 | 
 1718 |         if data:
 1719 |             pedidos = pedidos.filter(data_criacao__date=data)
 1720 | 
 1721 |     prioridade = Case(
 1722 |         When(
 1723 |             urgencia=PedidoSangue.Urgencia.CRITICA,
 1724 |             then=Value(1),
 1725 |         ),
 1726 |         When(
 1727 |             urgencia=PedidoSangue.Urgencia.ALTA,
 1728 |             then=Value(2),
 1729 |         ),
 1730 |         When(
 1731 |             urgencia=PedidoSangue.Urgencia.MEDIA,
 1732 |             then=Value(3),
 1733 |         ),
 1734 |         When(
 1735 |             urgencia=PedidoSangue.Urgencia.BAIXA,
 1736 |             then=Value(4),
 1737 |         ),
 1738 |         default=Value(5),
 1739 |         output_field=IntegerField(),
 1740 |     )
 1741 | 
 1742 |     pedidos = pedidos.annotate(
 1743 |         prioridade=prioridade
 1744 |     ).order_by(
 1745 |         "prioridade",
 1746 |         "-data_criacao",
 1747 |     )
 1748 | 
 1749 |     return render(
 1750 |         request,
 1751 |         "accounts/pedidos_listar.html",
 1752 |         {
 1753 |             "form": form,
 1754 |             "pedidos": pedidos,
 1755 |         },
 1756 |     )
 1757 | 
 1758 | 
 1759 | @login_required
 1760 | def painel_validacao_pedidos(request):
 1761 |     """Painel de moderação do Administrador, sem publicar pedidos."""
 1762 | 
 1763 |     exigir_administrador(request.user)
 1764 | 
 1765 |     pedidos = (
 1766 |         PedidoSangue.objects
 1767 |         .select_related("solicitante", "hemocentro_destino")
 1768 |         .prefetch_related(
 1769 |             Prefetch(
 1770 |                 "validacoes",
 1771 |                 queryset=ValidacaoPedido.objects.select_related("moderador"),
 1772 |             )
 1773 |         )
 1774 |         .filter(
 1775 |             status__in=[
 1776 |                 PedidoSangue.Status.ENVIADA,
 1777 |                 PedidoSangue.Status.EM_ANALISE,
 1778 |                 PedidoSangue.Status.CORRECAO_SOLICITADA,
 1779 |                 PedidoSangue.Status.PUBLICADA,
 1780 |             ]
 1781 |         )
 1782 |         .order_by("-duplicidade_suspeita", "-data_criacao")
 1783 |     )
 1784 | 
 1785 |     status = request.GET.get("status")
 1786 |     if status in dict(PedidoSangue.Status.choices):
 1787 |         pedidos = pedidos.filter(status=status)
 1788 | 
 1789 |     return render(
 1790 |         request,
 1791 |         "accounts/painel_moderacao_pedidos.html",
 1792 |         {
 1793 |             "pedidos": pedidos,
 1794 |             "status_opcoes": PedidoSangue.Status.choices,
 1795 |             "status_atual": status or "",
 1796 |         },
 1797 |     )
 1798 | 
 1799 | 
 1800 | @login_required
 1801 | @require_POST
 1802 | def aprovar_pedido(request, id_pedido):
 1803 |     """Publica uma solicitação após análise do Hemocentro de destino."""
 1804 | 
 1805 |     validar_publicacao_hemocentro(request.user)
 1806 | 
 1807 |     pedido = get_object_or_404(
 1808 |         PedidoSangue,
 1809 |         pk=id_pedido,
 1810 |     )
 1811 | 
 1812 |     aprovar_pedido_servico(
 1813 |         pedido=pedido,
 1814 |         moderador=request.user,
 1815 |         motivo=request.POST.get("motivo", ""),
 1816 |         request=request,
 1817 |     )
 1818 | 
 1819 |     messages.success(
 1820 |         request,
 1821 |         "Pedido publicado com sucesso." if hemocentro_aprovado(request.user)
 1822 |         else "Pedido validado sem publicacao.",
 1823 |     )
 1824 | 
 1825 |     return redirect("accounts:painel_pedidos_hemocentro")
 1826 | 
 1827 | 
 1828 | @login_required
 1829 | @require_POST
 1830 | def recusar_pedido(request, id_pedido):
 1831 |     """Recusa uma solicitação pelo Hemocentro de destino."""
 1832 | 
 1833 |     validar_publicacao_hemocentro(request.user)
 1834 | 
 1835 |     pedido = get_object_or_404(
 1836 |         PedidoSangue,
 1837 |         pk=id_pedido,
 1838 |     )
 1839 | 
 1840 |     recusar_pedido_servico(
 1841 |         pedido=pedido,
 1842 |         moderador=request.user,
 1843 |         motivo=request.POST.get("motivo", ""),
 1844 |         request=request,
 1845 |     )
 1846 | 
 1847 |     messages.success(
 1848 |         request,
 1849 |         "Pedido recusado com sucesso.",
 1850 |     )
 1851 | 
 1852 |     return redirect("accounts:painel_pedidos_hemocentro")
 1853 | 
 1854 | 
 1855 | @login_required
 1856 | @require_POST
 1857 | @exigir_hemocentro_aprovado
 1858 | def solicitar_correcao_pedido(request, id_pedido):
 1859 |     pedido = get_object_or_404(PedidoSangue, pk=id_pedido)
 1860 |     solicitar_correcao_pedido_servico(
 1861 |         pedido=pedido,
 1862 |         moderador=request.user,
 1863 |         motivo=request.POST.get("motivo", ""),
 1864 |         request=request,
 1865 |     )
 1866 |     messages.success(request, "Correção solicitada ao responsável.")
 1867 |     return redirect("accounts:painel_pedidos_hemocentro")
 1868 | 
 1869 | 
 1870 | @login_required
 1871 | @require_POST
 1872 | def marcar_pedido_suspeito(request, id_pedido):
 1873 |     """Registra uma suspeita para moderação, sem publicar o pedido."""
 1874 | 
 1875 |     pedido = get_object_or_404(PedidoSangue, pk=id_pedido)
 1876 |     marcar_pedido_suspeito_servico(
 1877 |         pedido=pedido,
 1878 |         moderador=request.user,
 1879 |         motivo=request.POST.get("motivo", ""),
 1880 |         request=request,
 1881 |     )
 1882 |     messages.success(request, "Pedido marcado para moderação como suspeito.")
 1883 | 
 1884 |     if usuario_e_administrador(request.user):
 1885 |         return redirect("accounts:painel_validacao_pedidos")
 1886 |     return redirect("accounts:painel_pedidos_hemocentro")
``````

## config/__init__.py

Original: [config/__init__.py](<C:/Users/lb119/Elo/config/__init__.py>).

``````text
    1 | """
    2 | Marca a pasta ``config`` como pacote Python.
    3 | 
    4 | Ela concentra configuracoes gerais do projeto, mas este arquivo nao precisa
    5 | executar nenhuma acao durante a inicializacao.
    6 | """
``````

## config/asgi.py

Original: [config/asgi.py](<C:/Users/lb119/Elo/config/asgi.py>).

``````text
    1 | """
    2 | RESUMO DO ARQUIVO
    3 | =================
    4 | Ponto de entrada ASGI para publicacao em servidores assincronos.
    5 | 
    6 | ASGI permite recursos como WebSockets e conexoes assincronas. O desenvolvimento
    7 | atual nao usa esses recursos diretamente, mas o Django gera este arquivo para
    8 | deixar o projeto preparado para um servidor compativel.
    9 | """
   10 | 
   11 | import os
   12 | 
   13 | from django.core.asgi import get_asgi_application
   14 | 
   15 | 
   16 | # Informa ao Django onde estao as configuracoes antes de criar a aplicacao.
   17 | os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
   18 | 
   19 | # Servidores ASGI importam esta variavel para encaminhar requisicoes ao Django.
   20 | application = get_asgi_application()
``````

## config/settings.py

Original: [config/settings.py](<C:/Users/lb119/Elo/config/settings.py>).

``````text
    1 | """
    2 | RESUMO DO ARQUIVO
    3 | =================
    4 | Este e o arquivo central de configuracao do projeto Django.
    5 | 
    6 | Ele informa quais apps estao ativos, como as requisicoes sao processadas, onde
    7 | ficam os templates, como conectar ao PostgreSQL, qual e o model de usuario e
    8 | para onde o login/logout deve redirecionar.
    9 | 
   10 | Dados secretos nao ficam escritos aqui. ``python-dotenv`` le o arquivo ``.env``
   11 | da raiz e disponibiliza seus valores por meio de ``os.environ``.
   12 | """
   13 | 
   14 | import os
   15 | from pathlib import Path
   16 | 
   17 | from dotenv import load_dotenv
   18 | 
   19 | 
   20 | # __file__ e o caminho deste settings.py. parent.parent sobe de config/ para a
   21 | # raiz do projeto, onde ficam manage.py, templates/ e .env.
   22 | BASE_DIR = Path(__file__).resolve().parent.parent
   23 | 
   24 | # Le o arquivo .env e coloca suas variaveis no ambiente deste processo Python.
   25 | # O .env real esta no .gitignore porque possui chave e senha locais.
   26 | load_dotenv(BASE_DIR / ".env")
   27 | 
   28 | 
   29 | # SECRET_KEY participa de assinaturas criptograficas do Django, inclusive de
   30 | # sessoes e tokens. os.environ[...] gera erro imediatamente se ela estiver
   31 | # ausente; isso e melhor do que executar o sistema com uma chave insegura.
   32 | SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
   33 | 
   34 | # getenv recebe texto. A comparacao converte "True" em booleano True.
   35 | # DEBUG mostra erros detalhados e deve ser False quando o sistema for publicado.
   36 | DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
   37 | 
   38 | # Hosts aceitos pelo Django. Estes dois cobrem o desenvolvimento local.
   39 | ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
   40 | 
   41 | 
   42 | # Cada item ativa um conjunto de recursos dentro do projeto.
   43 | INSTALLED_APPS = [
   44 |     # Painel administrativo em /admin/.
   45 |     "django.contrib.admin",
   46 |     # Autenticacao, hash de senha, grupos e permissoes.
   47 |     "django.contrib.auth",
   48 |     # Identifica models; e usado por permissoes e pelo admin.
   49 |     "django.contrib.contenttypes",
   50 |     # Salva sessoes de login no banco.
   51 |     "django.contrib.sessions",
   52 |     # Permite mensagens temporarias, como "Cadastro realizado".
   53 |     "django.contrib.messages",
   54 |     # Gerencia CSS, JavaScript e imagens quando forem adicionados.
   55 |     "django.contrib.staticfiles",
   56 |     # App criado pelo projeto: usuario, dados iniciais, cadastro, login e LGPD.
   57 |     "accounts",
   58 | ]
   59 | 
   60 | 
   61 | # Middlewares executam ao redor de cada requisicao e resposta, na ordem listada.
   62 | MIDDLEWARE = [
   63 |     # Adiciona protecoes e cabecalhos de seguranca.
   64 |     "django.middleware.security.SecurityMiddleware",
   65 |     # Carrega request.session; necessario para manter o login.
   66 |     "django.contrib.sessions.middleware.SessionMiddleware",
   67 |     # Comportamentos HTTP comuns, como normalizacao de URLs.
   68 |     "django.middleware.common.CommonMiddleware",
   69 |     # Verifica o token CSRF dos formularios POST.
   70 |     "django.middleware.csrf.CsrfViewMiddleware",
   71 |     # Usa a sessao para preencher request.user.
   72 |     "django.contrib.auth.middleware.AuthenticationMiddleware",
   73 |     "accounts.auditoria.AuditoriaAcessosMiddleware",
   74 |     # Disponibiliza mensagens temporarias nos templates.
   75 |     "django.contrib.messages.middleware.MessageMiddleware",
   76 |     # Ajuda a impedir que o site seja embutido em iframe malicioso.
   77 |     "django.middleware.clickjacking.XFrameOptionsMiddleware",
   78 | ]
   79 | 
   80 | 
   81 | # Primeiro arquivo de URLs consultado para qualquer endereco do projeto.
   82 | ROOT_URLCONF = "config.urls"
   83 | 
   84 | 
   85 | TEMPLATES = [
   86 |     {
   87 |         # Motor de templates nativo do Django.
   88 |         "BACKEND": "django.template.backends.django.DjangoTemplates",
   89 | 
   90 |         # Procura templates globais na pasta templates/ da raiz.
   91 |         "DIRS": [BASE_DIR / "templates"],
   92 | 
   93 |         # Tambem permite templates dentro da pasta de cada app.
   94 |         "APP_DIRS": True,
   95 |         "OPTIONS": {
   96 |             "context_processors": [
   97 |                 # Disponibiliza request no HTML.
   98 |                 "django.template.context_processors.request",
   99 |                 # Disponibiliza user e permissoes no HTML.
  100 |                 "django.contrib.auth.context_processors.auth",
  101 |                 # Disponibiliza a lista messages no HTML.
  102 |                 "django.contrib.messages.context_processors.messages",
  103 |             ],
  104 |         },
  105 |     },
  106 | ]
  107 | 
  108 | 
  109 | # Ponto de entrada usado por servidores web baseados em WSGI.
  110 | WSGI_APPLICATION = "config.wsgi.application"
  111 | 
  112 | 
  113 | # CONEXAO COM O POSTGRESQL
  114 | # -----------------------
  115 | # O Django ORM transforma operacoes Python em SQL. Exemplo:
  116 | # Usuario.objects.filter(email=...) vira um SELECT na tabela usuarios.
  117 | #
  118 | # Os valores abaixo correspondem ao banco e ao Login/Group Role criados no
  119 | # pgAdmin. Eles sao lidos do .env para que cada computador use sua propria senha.
  120 | DATABASES = {
  121 |     "default": {
  122 |         # Backend oficial do Django para PostgreSQL, usando psycopg.
  123 |         "ENGINE": "django.db.backends.postgresql",
  124 | 
  125 |         # Nome do banco criado no pgAdmin, normalmente elo_db.
  126 |         "NAME": os.environ["DB_NAME"],
  127 | 
  128 |         # Usuario do PostgreSQL que e proprietario do banco, normalmente elo_user.
  129 |         "USER": os.environ["DB_USER"],
  130 | 
  131 |         # Senha do elo_user. Nunca deve ser enviada ao GitHub.
  132 |         "PASSWORD": os.environ["DB_PASSWORD"],
  133 | 
  134 |         # 127.0.0.1 significa que o PostgreSQL esta no mesmo computador.
  135 |         "HOST": os.getenv("DB_HOST", "127.0.0.1"),
  136 | 
  137 |         # 5432 e a porta padrao do PostgreSQL.
  138 |         "PORT": os.getenv("DB_PORT", "5432"),
  139 |     }
  140 | }
  141 | 
  142 | 
  143 | # O UserCreationForm consulta estes validadores antes de aceitar uma senha.
  144 | AUTH_PASSWORD_VALIDATORS = [
  145 |     {
  146 |         # Evita senha muito parecida com nome ou e-mail.
  147 |         "NAME": (
  148 |             "django.contrib.auth.password_validation."
  149 |             "UserAttributeSimilarityValidator"
  150 |         ),
  151 |     },
  152 |     {
  153 |         # Exige o comprimento minimo definido pelo Django (8 por padrao).
  154 |         "NAME": (
  155 |             "django.contrib.auth.password_validation."
  156 |             "MinimumLengthValidator"
  157 |         ),
  158 |     },
  159 |     {
  160 |         # Bloqueia senhas conhecidas por serem muito comuns.
  161 |         "NAME": (
  162 |             "django.contrib.auth.password_validation."
  163 |             "CommonPasswordValidator"
  164 |         ),
  165 |     },
  166 |     {
  167 |         # Impede senha formada somente por numeros.
  168 |         "NAME": (
  169 |             "django.contrib.auth.password_validation."
  170 |             "NumericPasswordValidator"
  171 |         ),
  172 |     },
  173 | ]
  174 | 
  175 | 
  176 | # Traduz mensagens internas e define como datas sao apresentadas.
  177 | LANGUAGE_CODE = "pt-br"
  178 | TIME_ZONE = "America/Sao_Paulo"
  179 | USE_I18N = True
  180 | USE_TZ = True
  181 | 
  182 | # Limite conjunto de alertas internos de estoque e pedidos por doador.
  183 | CONVOCACAO_INTERVALO_HORAS = 24
  184 | CONVOCACAO_LIMITE_NOTIFICACOES = 1
  185 | CONVOCACAO_VERSAO_CONSENTIMENTO = "1.0"
  186 | 
  187 | 
  188 | # Prefixo de URL reservado para futuros arquivos CSS, JS e imagens.
  189 | STATIC_URL = "static/"
  190 | 
  191 | STATICFILES_DIRS = [
  192 |     BASE_DIR / "elo_front" / "static",
  193 | ]
  194 | 
  195 | # Enquanto nao existe servidor de e-mail, qualquer mensagem enviada pelo Django
  196 | # aparece no terminal. Isso evita disparos reais durante o desenvolvimento.
  197 | EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
  198 | 
  199 | # Tipo padrao de chave primaria quando um model nao declara a propria chave.
  200 | DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
  201 | 
  202 | 
  203 | # Substitui o auth.User padrao pelo Usuario concreto de accounts/models.py.
  204 | # Esta configuracao foi definida antes da primeira migration, como recomendado.
  205 | AUTH_USER_MODEL = "accounts.Usuario"
  206 | 
  207 | # Rotas usadas automaticamente por login_required, LoginView e LogoutView.
  208 | LOGIN_URL = "accounts:login"
  209 | LOGIN_REDIRECT_URL = "accounts:dashboard"
  210 | LOGOUT_REDIRECT_URL = "accounts:login"
``````

## config/settings_test.py

Original: [config/settings_test.py](<C:/Users/lb119/Elo/config/settings_test.py>).

``````text
    1 | """Configurações usadas somente pela suíte automatizada de testes.
    2 | 
    3 | O projeto continua usando PostgreSQL normalmente. Nos testes, o SQLite em
    4 | memória evita exigir a permissão CREATEDB do usuário local do PostgreSQL.
    5 | """
    6 | 
    7 | from .settings import *  # noqa: F403
    8 | 
    9 | 
   10 | # O banco em memória é criado no início dos testes e descartado ao final.
   11 | DATABASES = {
   12 |     "default": {
   13 |         "ENGINE": "django.db.backends.sqlite3",
   14 |         "NAME": ":memory:",
   15 |     }
   16 | }
``````

## config/urls.py

Original: [config/urls.py](<C:/Users/lb119/Elo/config/urls.py>).

``````text
    1 | """
    2 | RESUMO DO ARQUIVO
    3 | =================
    4 | Este e o roteador principal do projeto. Ele recebe a URL primeiro e encaminha
    5 | para o painel administrativo ou para o conjunto de rotas do app accounts.
    6 | """
    7 | 
    8 | from django.contrib import admin
    9 | from django.urls import include, path
   10 | 
   11 | 
   12 | urlpatterns = [
   13 |     # Todas as paginas internas do admin ficam abaixo de /admin/.
   14 |     path("admin/", admin.site.urls),
   15 | 
   16 |     # include transfere as demais URLs para accounts/urls.py. Como o prefixo e
   17 |     # vazio, rotas como cadastro/ ficam diretamente em /cadastro/.
   18 |     path("", include("accounts.urls")),
   19 | ]
``````

## config/wsgi.py

Original: [config/wsgi.py](<C:/Users/lb119/Elo/config/wsgi.py>).

``````text
    1 | """
    2 | RESUMO DO ARQUIVO
    3 | =================
    4 | Ponto de entrada WSGI para publicacao em servidores web tradicionais.
    5 | 
    6 | Servidores como Gunicorn ou uWSGI importam ``application`` deste modulo. Durante
    7 | o desenvolvimento, ``runserver`` cuida disso automaticamente.
    8 | """
    9 | 
   10 | import os
   11 | 
   12 | from django.core.wsgi import get_wsgi_application
   13 | 
   14 | 
   15 | # Informa ao Django onde estao as configuracoes do projeto.
   16 | os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
   17 | 
   18 | # Objeto chamado pelo servidor para processar cada requisicao HTTP.
   19 | application = get_wsgi_application()
``````

## docs/superpowers/plans/2026-09-04-triagem-completa.md

Original: [docs/superpowers/plans/2026-09-04-triagem-completa.md](<C:/Users/lb119/Elo/docs/superpowers/plans/2026-09-04-triagem-completa.md>).

``````text
    1 | # Triagem completa do Elo - Implementation Plan
    2 | 
    3 | > **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
    4 | 
    5 | **Goal:** Entregar as triagens extensa e simplificada completas, com perguntas versionadas, regras orientativas, salvamento de andamento, resultado e histórico privado no perfil.
    6 | 
    7 | **Architecture:** Os questionários serão catálogos Python imutáveis e versionados. Um motor puro avaliará respostas estruturadas sem acessar o banco; um serviço transacional cuidará de andamento, ramificações, conclusão e vínculo com a triagem extensa-base; views pequenas renderizarão uma pergunta por página e páginas privadas de resultado e histórico.
    8 | 
    9 | **Tech Stack:** Python 3.14, Django 6.1, PostgreSQL em produção, SQLite em memória para testes locais, templates Django sem CSS.
   10 | 
   11 | **Spec:** `docs/superpowers/specs/2026-09-04-triagem-completa-design.md`
   12 | 
   13 | ## Global Constraints
   14 | 
   15 | - A regra inicial é `HEMOMINAS_2026_08`, consolidada em 28/08/2026.
   16 | - A interface nunca declara aptidão clínica; usa somente os estados orientativos definidos no model `Triagem`.
   17 | - A decisão final pertence sempre à equipe do hemocentro.
   18 | - As 55 entradas extensas (`EXT-01` a `EXT-51`, incluindo `EXT-05A`, `EXT-05B`, `EXT-07A` e `EXT-11A`) e as 18 simplificadas (`SIM-01` a `SIM-18`) devem existir.
   19 | - A triagem simplificada somente pode começar depois de uma extensa concluída pelo mesmo usuário.
   20 | - Visitante visualiza a apresentação; Doador e Receptor respondem; Observador e Hemocentro não respondem; Administrador consulta no admin em modo somente leitura.
   21 | - Histórico, resultado e respostas são sempre filtrados pelo proprietário fora do admin.
   22 | - Não adicionar CSS.
   23 | - Todo código novo ou alterado recebe comentários didáticos, objetivos e verdadeiros.
   24 | - Não editar migrations já aplicadas; criar uma nova migration depois de alterar os models.
   25 | - Preservar alterações locais existentes e remover apenas a implementação inicial de triagem que for substituída pela nova solução.
   26 | 
   27 | ---
   28 | 
   29 | ## Mapa de arquivos
   30 | 
   31 | - `config/settings_test.py`: banco SQLite isolado para executar testes sem exigir `CREATEDB` no PostgreSQL local.
   32 | - `accounts/models.py`: ciclo de vida da triagem, fluxo persistido, referência da extensa-base e resposta estruturada.
   33 | - `accounts/migrations/0007_*.py`: campos novos, conversão segura dos dados de `0006` e restrição de unicidade.
   34 | - `accounts/triagem_catalogo.py`: tipos compartilhados, validação e busca de perguntas.
   35 | - `accounts/triagem_catalogo_extensa.py`: 55 entradas extensas, alternativas, condições de exibição, fontes e regras declarativas.
   36 | - `accounts/triagem_catalogo_simplificada.py`: 18 entradas rápidas e mapas para blocos extensos.
   37 | - `accounts/triagem_motor.py`: avaliação pura, prioridade, cálculo de prazos e mensagens.
   38 | - `accounts/triagem_forms.py`: formulário dinâmico de uma pergunta.
   39 | - `accounts/triagem_servico.py`: criação, retomada, navegação, respostas, conclusão e base da simplificada.
   40 | - `accounts/views.py`: apresentação, início, pergunta, histórico e resultado.
   41 | - `accounts/urls.py`: rotas únicas e sem duplicação.
   42 | - `accounts/admin.py`: novos campos somente leitura e aviso de sensibilidade.
   43 | - `templates/accounts/triagem_apresentacao.html`: texto integral aprovado e escolha das duas modalidades.
   44 | - `templates/accounts/triagem_pergunta.html`: uma pergunta por página.
   45 | - `templates/accounts/triagem_resultado.html`: resultado orientativo e achados.
   46 | - `templates/accounts/triagem_historico.html`: histórico do usuário.
   47 | - `templates/accounts/dashboard.html`: resumo não sensível da última triagem.
   48 | - `templates/accounts/inicio.html`: apontamento público para a apresentação.
   49 | - `accounts/test_triagem_models.py`: persistência e migration.
   50 | - `accounts/test_triagem_catalogos.py`: completude dos catálogos.
   51 | - `accounts/test_triagem_motor.py`: regras, exceções, prioridade e datas-limite.
   52 | - `accounts/test_triagem_forms.py`: validação de entradas.
   53 | - `accounts/test_triagem_servico.py`: estado, ramificações, retomada e simplificada.
   54 | - `accounts/test_triagem_views.py`: acesso, conteúdo, privacidade e navegação.
   55 | - `accounts/test_triagem.py`: adaptar os testes iniciais às interfaces novas, preservando o arquivo.
   56 | 
   57 | ---
   58 | 
   59 | ### Task 1: Infraestrutura de teste e ciclo de vida persistente
   60 | 
   61 | **Files:**
   62 | - Create: `config/settings_test.py`
   63 | - Modify: `accounts/models.py`
   64 | - Create: `accounts/test_triagem_models.py`
   65 | - Create: `accounts/migrations/0007_*.py`
   66 | 
   67 | **Interfaces:**
   68 | - Consumes: `accounts.models.Usuario`, `Triagem` e `RespostaTriagem` existentes na migration `0006`.
   69 | - Produces: `Triagem.Status`, `Triagem.status`, `pergunta_atual`, `fluxo_perguntas`, `triagem_base`, `atualizada_em`, `RespostaTriagem.valor` e unicidade `(triagem, id_pergunta)`.
   70 | 
   71 | - [ ] **Step 1: Criar configuração isolada de testes**
   72 | 
   73 | ```python
   74 | # config/settings_test.py
   75 | from .settings import *  # noqa: F403
   76 | 
   77 | # Os testes não dependem da permissão CREATEDB do PostgreSQL local.
   78 | DATABASES = {
   79 |     "default": {
   80 |         "ENGINE": "django.db.backends.sqlite3",
   81 |         "NAME": ":memory:",
   82 |     }
   83 | }
   84 | ```
   85 | 
   86 | - [ ] **Step 2: Escrever testes que descrevem os novos campos e a unicidade**
   87 | 
   88 | ```python
   89 | class TriagemModelTests(TestCase):
   90 |     def test_nova_triagem_comeca_em_andamento(self):
   91 |         triagem = Triagem.objects.create(
   92 |             usuario=self.usuario,
   93 |             modalidade=Triagem.Modalidade.EXTENSA,
   94 |         )
   95 |         self.assertEqual(triagem.status, Triagem.Status.EM_ANDAMENTO)
   96 |         self.assertEqual(triagem.fluxo_perguntas, [])
   97 |         self.assertEqual(triagem.resultado, "")
   98 | 
   99 |     def test_uma_pergunta_tem_uma_unica_resposta_por_triagem(self):
  100 |         RespostaTriagem.objects.create(
  101 |             triagem=self.triagem,
  102 |             id_pergunta="EXT-01",
  103 |             codigo_resposta="SIM",
  104 |             resposta_label="Sim",
  105 |             valor={"codigos": ["SIM"]},
  106 |         )
  107 |         with self.assertRaises(IntegrityError):
  108 |             RespostaTriagem.objects.create(
  109 |                 triagem=self.triagem,
  110 |                 id_pergunta="EXT-01",
  111 |                 codigo_resposta="NAO",
  112 |                 resposta_label="Não",
  113 |                 valor={"codigos": ["NAO"]},
  114 |             )
  115 | ```
  116 | 
  117 | - [ ] **Step 3: Executar os testes e confirmar a falha pelos campos ausentes**
  118 | 
  119 | Run: `py manage.py test accounts.test_triagem_models --settings=config.settings_test -v 2`
  120 | 
  121 | Expected: FAIL porque `Triagem.Status`, `status`, `fluxo_perguntas` e `valor` ainda não existem.
  122 | 
  123 | - [ ] **Step 4: Adicionar os campos aos models**
  124 | 
  125 | ```python
  126 | class Status(models.TextChoices):
  127 |     EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
  128 |     CONCLUIDA = "CONCLUIDA", "Concluída"
  129 |     CANCELADA = "CANCELADA", "Cancelada"
  130 | 
  131 | status = models.CharField(
  132 |     max_length=20,
  133 |     choices=Status.choices,
  134 |     default=Status.EM_ANDAMENTO,
  135 | )
  136 | pergunta_atual = models.PositiveIntegerField(default=0)
  137 | fluxo_perguntas = models.JSONField(default=list, blank=True)
  138 | triagem_base = models.ForeignKey(
  139 |     "self",
  140 |     on_delete=models.SET_NULL,
  141 |     null=True,
  142 |     blank=True,
  143 |     related_name="verificacoes_simplificadas",
  144 | )
  145 | atualizada_em = models.DateTimeField(auto_now=True)
  146 | ```
  147 | 
  148 | Alterar `resultado` para `blank=True, default=""`, `mensagem_resultado` para `blank=True, default=""` e adicionar em `RespostaTriagem`:
  149 | 
  150 | ```python
  151 | # Mantém seleção, data e complemento juntos sem perder os campos legados.
  152 | valor = models.JSONField(default=dict, blank=True)
  153 | 
  154 | constraints = [
  155 |     models.UniqueConstraint(
  156 |         fields=["triagem", "id_pergunta"],
  157 |         name="resposta_unica_por_pergunta",
  158 |     )
  159 | ]
  160 | ```
  161 | 
  162 | - [ ] **Step 5: Gerar a migration e acrescentar conversão dos registros antigos**
  163 | 
  164 | Run: `py manage.py makemigrations accounts`
  165 | 
  166 | Adicionar uma `RunPython` antes da restrição única. A função direta define `CONCLUIDA` quando `finalizada_em` existe e monta `valor` com `codigo_resposta`, `data_evento` e `metadata`; a reversa preserva os campos antigos e somente limpa os campos novos.
  167 | 
  168 | - [ ] **Step 6: Executar testes do model e verificar a migration**
  169 | 
  170 | Run: `py manage.py test accounts.test_triagem_models --settings=config.settings_test -v 2`
  171 | 
  172 | Expected: PASS.
  173 | 
  174 | Run: `py manage.py makemigrations --check --settings=config.settings_test`
  175 | 
  176 | Expected: `No changes detected`.
  177 | 
  178 | - [ ] **Step 7: Registrar a etapa**
  179 | 
  180 | ```bash
  181 | git add config/settings_test.py accounts/models.py accounts/migrations/0007_*.py accounts/test_triagem_models.py
  182 | git commit -m "feat: add triage lifecycle persistence"
  183 | ```
  184 | 
  185 | ---
  186 | 
  187 | ### Task 2: Catálogos completos e validados
  188 | 
  189 | **Files:**
  190 | - Create: `accounts/triagem_catalogo.py`
  191 | - Create: `accounts/triagem_catalogo_extensa.py`
  192 | - Create: `accounts/triagem_catalogo_simplificada.py`
  193 | - Create: `accounts/test_triagem_catalogos.py`
  194 | 
  195 | **Interfaces:**
  196 | - Consumes: códigos de resultado de `Triagem.Resultado` e a versão `HEMOMINAS_2026_08`.
  197 | - Produces: `PERGUNTAS_EXTENSAS`, `PERGUNTAS_SIMPLIFICADAS`, `obter_catalogo(modalidade)`, `obter_pergunta(id_pergunta)` e `validar_catalogos()`.
  198 | 
  199 | - [ ] **Step 1: Escrever testes de completude**
  200 | 
  201 | ```python
  202 | IDS_EXTENSOS = {
  203 |     "EXT-01", "EXT-02", "EXT-03", "EXT-04", "EXT-05", "EXT-05A",
  204 |     "EXT-05B", "EXT-06", "EXT-07", "EXT-07A", "EXT-08", "EXT-09",
  205 |     "EXT-10", "EXT-11", "EXT-11A", "EXT-12", "EXT-13", "EXT-14",
  206 |     "EXT-15", "EXT-16", "EXT-17", "EXT-18", "EXT-19", "EXT-20",
  207 |     "EXT-21", "EXT-22", "EXT-23", "EXT-24", "EXT-25", "EXT-26",
  208 |     "EXT-27", "EXT-28", "EXT-29", "EXT-30", "EXT-31", "EXT-32",
  209 |     "EXT-33", "EXT-34", "EXT-35", "EXT-36", "EXT-37", "EXT-38",
  210 |     "EXT-39", "EXT-40", "EXT-41", "EXT-42", "EXT-43", "EXT-44",
  211 |     "EXT-45", "EXT-46", "EXT-47", "EXT-48", "EXT-49", "EXT-50",
  212 |     "EXT-51",
  213 | }
  214 | 
  215 | IDS_SIMPLIFICADOS = {f"SIM-{numero:02d}" for numero in range(1, 19)}
  216 | 
  217 | def test_catalogos_possuem_todos_os_identificadores(self):
  218 |     self.assertEqual(set(PERGUNTAS_EXTENSAS), IDS_EXTENSOS)
  219 |     self.assertEqual(set(PERGUNTAS_SIMPLIFICADAS), IDS_SIMPLIFICADOS)
  220 | 
  221 | def test_toda_pergunta_tem_texto_opcoes_fonte_e_versao(self):
  222 |     for pergunta in [*PERGUNTAS_EXTENSAS.values(), *PERGUNTAS_SIMPLIFICADAS.values()]:
  223 |         self.assertTrue(pergunta["texto"])
  224 |         self.assertTrue(pergunta["opcoes"] or pergunta["tipo"] in {"data", "numero", "texto"})
  225 |         self.assertTrue(pergunta["fonte"])
  226 |         self.assertEqual(pergunta["regra_version"], "HEMOMINAS_2026_08")
  227 | ```
  228 | 
  229 | - [ ] **Step 2: Executar e confirmar a falha por módulos ausentes**
  230 | 
  231 | Run: `py manage.py test accounts.test_triagem_catalogos --settings=config.settings_test -v 2`
  232 | 
  233 | Expected: ERROR de importação de `accounts.triagem_catalogo`.
  234 | 
  235 | - [ ] **Step 3: Criar o contrato comum do catálogo**
  236 | 
  237 | Cada pergunta terá as chaves `id`, `titulo`, `texto`, `explicacao`, `tipo`, `opcoes`, `multipla`, `permite_data`, `exige_data_para`, `mostrar_se`, `abrir_extensa`, `regras`, `fonte` e `regra_version`. Cada opção terá `codigo` e `rotulo`; regras simples terão `resultado`, `mensagem`, `prazo` e `data_referencia`.
  238 | 
  239 | ```python
  240 | TRIAGEM_RULE_VERSION = "HEMOMINAS_2026_08"
  241 | 
  242 | def obter_catalogo(modalidade):
  243 |     if modalidade == "EXTENSA":
  244 |         return PERGUNTAS_EXTENSAS
  245 |     if modalidade == "SIMPLIFICADA":
  246 |         return PERGUNTAS_SIMPLIFICADAS
  247 |     raise ValueError("Modalidade de triagem inválida.")
  248 | 
  249 | def obter_pergunta(id_pergunta):
  250 |     pergunta = PERGUNTAS_EXTENSAS.get(id_pergunta)
  251 |     if pergunta is None:
  252 |         pergunta = PERGUNTAS_SIMPLIFICADAS.get(id_pergunta)
  253 |     if pergunta is None:
  254 |         raise KeyError(f"Pergunta inexistente: {id_pergunta}")
  255 |     return pergunta
  256 | ```
  257 | 
  258 | - [ ] **Step 4: Preencher o catálogo extenso**
  259 | 
  260 | Transcrever as 55 entradas do PDF sem abreviar alternativas. Declarar ramificações de `EXT-05A/05B`, `EXT-06`, `EXT-07`, `EXT-12` a `EXT-18` e `EXT-42` por `mostrar_se`. Perguntas sobre doenças, infecções, medicamentos, vacinas, viagens e exposições devem conter a alternativa explícita de dúvida ou resposta presencial prevista na fonte.
  261 | 
  262 | Exemplo integral do formato usado por todas as entradas:
  263 | 
  264 | ```python
  265 | "EXT-01": {
  266 |     "id": "EXT-01",
  267 |     "titulo": "Consentimento e entendimento",
  268 |     "texto": (
  269 |         "Você entende que esta pré-triagem é apenas uma orientação e que "
  270 |         "a decisão final será feita pela equipe do hemocentro?"
  271 |     ),
  272 |     "explicacao": (
  273 |         "Antes de qualquer pergunta de saúde, você precisa compreender "
  274 |         "o limite desta ferramenta."
  275 |     ),
  276 |     "tipo": "escolha",
  277 |     "opcoes": [
  278 |         {"codigo": "SIM", "rotulo": "Sim, entendo e quero continuar."},
  279 |         {"codigo": "NAO", "rotulo": "Não entendo / quero ler a explicação novamente."},
  280 |     ],
  281 |     "multipla": False,
  282 |     "permite_data": False,
  283 |     "exige_data_para": [],
  284 |     "mostrar_se": None,
  285 |     "abrir_extensa": {},
  286 |     "regras": {
  287 |         "NAO": {
  288 |             "resultado": "AVALIACAO_PRESENCIAL",
  289 |             "mensagem": "Leia novamente a explicação antes de continuar.",
  290 |         }
  291 |     },
  292 |     "fonte": "PDF, EXT-01; Manual Elo, seções 1, 2 e 18",
  293 |     "regra_version": "HEMOMINAS_2026_08",
  294 | },
  295 | ```
  296 | 
  297 | - [ ] **Step 5: Preencher o catálogo simplificado**
  298 | 
  299 | Transcrever `SIM-01` a `SIM-18` e declarar os blocos detalhados exatos: `SIM-02 -> EXT-02/03/05A/05B/07`, `SIM-03 -> EXT-08/12/13/14`, `SIM-04 -> EXT-09/10/44`, `SIM-05 -> EXT-33`, `SIM-06 -> blocos de doença/EXT-27/46`, `SIM-07 -> EXT-41/42`, `SIM-08 -> EXT-46/47`, `SIM-09 -> EXT-48`, `SIM-10 -> EXT-21/22/23/24`, `SIM-11 -> EXT-25/26/27`, `SIM-12 -> EXT-15/16`, `SIM-13 -> EXT-43`, `SIM-14 -> EXT-45`, `SIM-15 -> EXT-49`, `SIM-16 -> EXT-03/11/18/50`, `SIM-17 -> nova extensa completa`, `SIM-18 -> concluir ou iniciar extensa`.
  300 | 
  301 | - [ ] **Step 6: Executar testes e a validação do catálogo**
  302 | 
  303 | Run: `py manage.py test accounts.test_triagem_catalogos --settings=config.settings_test -v 2`
  304 | 
  305 | Expected: PASS, incluindo códigos de opção únicos e todos os destinos de `abrir_extensa` existentes no catálogo extenso.
  306 | 
  307 | - [ ] **Step 7: Registrar a etapa**
  308 | 
  309 | ```bash
  310 | git add accounts/triagem_catalogo.py accounts/triagem_catalogo_extensa.py accounts/triagem_catalogo_simplificada.py accounts/test_triagem_catalogos.py
  311 | git commit -m "feat: add complete triage question catalogs"
  312 | ```
  313 | 
  314 | ---
  315 | 
  316 | ### Task 3: Motor completo de regras orientativas
  317 | 
  318 | **Files:**
  319 | - Create: `accounts/triagem_motor.py`
  320 | - Create: `accounts/test_triagem_motor.py`
  321 | - Modify: `accounts/triagem.py` para manter somente importações de compatibilidade documentadas para o novo catálogo e motor.
  322 | 
  323 | **Interfaces:**
  324 | - Consumes: `obter_catalogo()`, respostas no formato `{id_pergunta: {"codigos": list[str], "data_evento": str | None, "detalhes": str}}` e respostas-base opcionais.
  325 | - Produces: `avaliar_triagem(modalidade, respostas, hoje=None, respostas_base=None) -> dict`, `escolher_resultado(achados) -> str` e `calcular_data_referencia(data_evento, prazo, hoje) -> date | None`.
  326 | 
  327 | - [ ] **Step 1: Escrever testes da prioridade e maior prazo**
  328 | 
  329 | ```python
  330 | def test_resultado_respeita_prioridade_e_preserva_todos_os_achados(self):
  331 |     resultado = avaliar_triagem(
  332 |         "EXTENSA",
  333 |         {
  334 |             "EXT-03": {"codigos": ["MENOS_50"]},
  335 |             "EXT-20": {"codigos": ["ANEMIA_FALCIFORME"]},
  336 |             "EXT-46": {"codigos": ["NAO_SEI"]},
  337 |         },
  338 |         hoje=date(2026, 8, 28),
  339 |     )
  340 |     self.assertEqual(resultado["resultado"], Triagem.Resultado.DEFINITIVA)
  341 |     self.assertEqual(len(resultado["achados"]), 3)
  342 | 
  343 | def test_maior_data_temporaria_e_a_data_principal(self):
  344 |     resultado = avaliar_triagem(
  345 |         "EXTENSA",
  346 |         {
  347 |             "EXT-44": {"codigos": ["ALCOOL_12H"], "data_evento": "2026-08-28"},
  348 |             "EXT-48": {"codigos": ["VACINA_30_DIAS"], "data_evento": "2026-08-20"},
  349 |         },
  350 |         hoje=date(2026, 8, 28),
  351 |     )
  352 |     self.assertEqual(resultado["data_liberacao"], date(2026, 9, 19))
  353 | ```
  354 | 
  355 | - [ ] **Step 2: Executar e confirmar a falha pelo motor ausente**
  356 | 
  357 | Run: `py manage.py test accounts.test_triagem_motor --settings=config.settings_test -v 2`
  358 | 
  359 | Expected: ERROR de importação de `accounts.triagem_motor`.
  360 | 
  361 | - [ ] **Step 3: Implementar achados declarativos e prioridade**
  362 | 
  363 | ```python
  364 | PRIORIDADE_RESULTADOS = (
  365 |     Triagem.Resultado.DEFINITIVA,
  366 |     Triagem.Resultado.AVALIACAO,
  367 |     Triagem.Resultado.TEMPORARIA,
  368 |     Triagem.Resultado.DOCUMENTACAO,
  369 | )
  370 | 
  371 | def escolher_resultado(achados):
  372 |     encontrados = {achado["resultado"] for achado in achados}
  373 |     for resultado in PRIORIDADE_RESULTADOS:
  374 |         if resultado in encontrados:
  375 |             return resultado
  376 |     return Triagem.Resultado.SEM_IMPEDIMENTO
  377 | ```
  378 | 
  379 | O avaliador genérico percorre todos os códigos respondidos, cria um achado por regra e nunca interrompe o laço no primeiro impedimento.
  380 | 
  381 | - [ ] **Step 4: Escrever a matriz de testes das regras simples**
  382 | 
  383 | Construir casos nomeados para cada opção que tenha `regras` no catálogo. O teste compara `id_pergunta`, `codigo_regra`, `resultado`, `exige_relatorio`, `fonte` e `regra_version`, garantindo que uma alternativa configurada não fique sem efeito.
  384 | 
  385 | ```python
  386 | def test_toda_regra_declarada_gera_achado_com_rastreabilidade(self):
  387 |     for pergunta in todas_as_perguntas():
  388 |         for codigo, regra in pergunta["regras"].items():
  389 |             resultado = avaliar_triagem(
  390 |                 "EXTENSA" if pergunta["id"].startswith("EXT") else "SIMPLIFICADA",
  391 |                 {pergunta["id"]: {"codigos": [codigo]}},
  392 |                 hoje=date(2026, 8, 28),
  393 |             )
  394 |             achado = next(
  395 |                 item for item in resultado["achados"]
  396 |                 if item["id_pergunta"] == pergunta["id"]
  397 |             )
  398 |             self.assertEqual(achado["resultado"], regra["resultado"])
  399 |             self.assertEqual(achado["regra_version"], "HEMOMINAS_2026_08")
  400 |             self.assertTrue(achado["fonte"])
  401 | ```
  402 | 
  403 | - [ ] **Step 5: Implementar prazos e datas de referência**
  404 | 
  405 | Aceitar `horas`, `dias`, `semanas`, `meses` e `anos`. Somar meses e anos por calendário, reduzindo o dia somente quando ele não existir no mês final. Regras que dependem de cura, alta, retirada ou fim do tratamento, sem `data_evento`, geram `AVALIACAO_PRESENCIAL` e não inventam data.
  406 | 
  407 | - [ ] **Step 6: Escrever testes das regras especiais**
  408 | 
  409 | Cobrir limites exatos de 48h, 72h, 7 dias, 30 dias, 6 meses, 12 meses, 1 ano, 3 anos e 5 anos; intervalos por sexo; faixa 61-69; contagem de doações sem datas; parto vaginal, cesárea, aborto e amamentação; hepatites; malária; vacinas; PrEP/PEP; GLP-1; anticoagulantes; procedimentos invasivos; exposição sexual/sangue; drogas; e exceções de esplenectomia por trauma, PTI infantil, hepatite A, cânceres excepcionados e WPW após ablação.
  410 | 
  411 | - [ ] **Step 7: Implementar avaliadores especiais e combinação com a extensa-base**
  412 | 
  413 | Criar um mapa explícito de handlers somente para regras que não cabem na declaração simples:
  414 | 
  415 | ```python
  416 | AVALIADORES_ESPECIAIS = {
  417 |     "EXT-02": avaliar_idade,
  418 |     "EXT-04": avaliar_regra_por_sexo,
  419 |     "EXT-05A": avaliar_intervalo_ultima_doacao,
  420 |     "EXT-05B": avaliar_limite_anual,
  421 |     "EXT-07": avaliar_doador_acima_60,
  422 |     "EXT-19": avaliar_hemoglobina,
  423 |     "EXT-20": avaliar_doencas_hematologicas,
  424 |     "EXT-27": avaliar_cirurgias,
  425 |     "EXT-28": avaliar_cancer,
  426 |     "EXT-33": avaliar_gestacao,
  427 |     "EXT-35": avaliar_coracao,
  428 |     "EXT-41": avaliar_infeccoes,
  429 |     "EXT-42": avaliar_hepatites,
  430 |     "EXT-46": avaliar_medicamentos,
  431 |     "EXT-47": avaliar_medicamentos_prolongados,
  432 |     "EXT-48": avaliar_vacinas,
  433 |     "EXT-49": avaliar_viagens,
  434 | }
  435 | ```
  436 | 
  437 | Na simplificada, mesclar respostas estáveis da extensa-base com respostas `EXT-*` coletadas nesta execução; nunca reutilizar sono, alimentação, hidratação, sinais vitais ou saúde atual.
  438 | 
  439 | - [ ] **Step 8: Executar todos os testes do motor**
  440 | 
  441 | Run: `py manage.py test accounts.test_triagem_motor --settings=config.settings_test -v 2`
  442 | 
  443 | Expected: PASS.
  444 | 
  445 | - [ ] **Step 9: Registrar a etapa**
  446 | 
  447 | ```bash
  448 | git add accounts/triagem_motor.py accounts/test_triagem_motor.py accounts/triagem.py
  449 | git commit -m "feat: evaluate complete triage rules"
  450 | ```
  451 | 
  452 | ---
  453 | 
  454 | ### Task 4: Formulário dinâmico de uma pergunta
  455 | 
  456 | **Files:**
  457 | - Create: `accounts/triagem_forms.py`
  458 | - Create: `accounts/test_triagem_forms.py`
  459 | - Modify: `accounts/forms.py`
  460 | 
  461 | **Interfaces:**
  462 | - Consumes: dicionário de pergunta retornado por `obter_pergunta()`.
  463 | - Produces: `FormularioPergunta(pergunta, *args, **kwargs)` com `cleaned_data["valor"]` estruturado.
  464 | 
  465 | - [ ] **Step 1: Escrever testes de escolha, múltipla, data e complemento**
  466 | 
  467 | ```python
  468 | def test_formulario_normaliza_resposta(self):
  469 |     pergunta = obter_pergunta("EXT-05A")
  470 |     form = FormularioPergunta(
  471 |         pergunta,
  472 |         data={"resposta": "DATA", "data_evento": "2026-08-01"},
  473 |     )
  474 |     self.assertTrue(form.is_valid())
  475 |     self.assertEqual(
  476 |         form.cleaned_data["valor"],
  477 |         {"codigos": ["DATA"], "data_evento": "2026-08-01", "detalhes": ""},
  478 |     )
  479 | 
  480 | def test_formulario_rejeita_data_futura(self):
  481 |     pergunta = obter_pergunta("EXT-05A")
  482 |     form = FormularioPergunta(
  483 |         pergunta,
  484 |         data={"resposta": "DATA", "data_evento": "2999-01-01"},
  485 |     )
  486 |     self.assertFalse(form.is_valid())
  487 | ```
  488 | 
  489 | - [ ] **Step 2: Executar e confirmar a falha pela classe ausente**
  490 | 
  491 | Run: `py manage.py test accounts.test_triagem_forms --settings=config.settings_test -v 2`
  492 | 
  493 | Expected: ERROR de importação de `FormularioPergunta`.
  494 | 
  495 | - [ ] **Step 3: Implementar campos e normalização**
  496 | 
  497 | Usar `ChoiceField`/`MultipleChoiceField`, `DateField` e `CharField` conforme o catálogo. A validação deve exigir data somente para códigos listados em `exige_data_para`, limitar complemento a 500 caracteres e rejeitar códigos que não pertencem à pergunta.
  498 | 
  499 | - [ ] **Step 4: Remover o formulário inicial substituído**
  500 | 
  501 | Remover somente `TriagemExtensaForm` de `accounts/forms.py`; manter formulários de cadastro e login intactos.
  502 | 
  503 | - [ ] **Step 5: Executar os testes**
  504 | 
  505 | Run: `py manage.py test accounts.test_triagem_forms --settings=config.settings_test -v 2`
  506 | 
  507 | Expected: PASS.
  508 | 
  509 | - [ ] **Step 6: Registrar a etapa**
  510 | 
  511 | ```bash
  512 | git add accounts/triagem_forms.py accounts/test_triagem_forms.py accounts/forms.py
  513 | git commit -m "feat: add dynamic triage question form"
  514 | ```
  515 | 
  516 | ---
  517 | 
  518 | ### Task 5: Serviço transacional, ramificações e retomada
  519 | 
  520 | **Files:**
  521 | - Create: `accounts/triagem_servico.py`
  522 | - Create: `accounts/test_triagem_servico.py`
  523 | 
  524 | **Interfaces:**
  525 | - Consumes: catálogos, `avaliar_triagem()`, `Triagem`, `RespostaTriagem`, `ConsentimentoLGPD`.
  526 | - Produces: `pode_responder(usuario)`, `obter_extensa_base(usuario)`, `iniciar_triagem(usuario, modalidade, ip)`, `obter_pergunta_atual(triagem)`, `salvar_resposta(triagem, id_pergunta, valor)`, `voltar_pergunta(triagem)`, `concluir_triagem(triagem, hoje=None)`.
  527 | 
  528 | - [ ] **Step 1: Escrever testes de acesso e início**
  529 | 
  530 | ```python
  531 | def test_simplificada_exige_extensa_concluida_do_mesmo_usuario(self):
  532 |     with self.assertRaises(TriagemSimplificadaIndisponivel):
  533 |         iniciar_triagem(
  534 |             self.usuario,
  535 |             Triagem.Modalidade.SIMPLIFICADA,
  536 |             ip="127.0.0.1",
  537 |         )
  538 | 
  539 | def test_inicio_extenso_cria_fluxo_e_consentimento(self):
  540 |     triagem = iniciar_triagem(
  541 |         self.usuario,
  542 |         Triagem.Modalidade.EXTENSA,
  543 |         ip="127.0.0.1",
  544 |     )
  545 |     self.assertEqual(triagem.fluxo_perguntas[0], "EXT-01")
  546 |     self.assertEqual(triagem.status, Triagem.Status.EM_ANDAMENTO)
  547 |     self.assertTrue(ConsentimentoLGPD.objects.filter(
  548 |         usuario=self.usuario,
  549 |         tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM,
  550 |         aceito=True,
  551 |     ).exists())
  552 | ```
  553 | 
  554 | - [ ] **Step 2: Executar e confirmar a falha pelo serviço ausente**
  555 | 
  556 | Run: `py manage.py test accounts.test_triagem_servico --settings=config.settings_test -v 2`
  557 | 
  558 | Expected: ERROR de importação de `accounts.triagem_servico`.
  559 | 
  560 | - [ ] **Step 3: Implementar início, base e consentimento**
  561 | 
  562 | O início extenso usa a ordem do catálogo. O início simplificado seleciona a extensa concluída mais recente do mesmo usuário, salva `triagem_base` e usa a ordem `SIM-01` a `SIM-18`. Doador e Receptor são aceitos; outros perfis geram `PermissionDenied`.
  563 | 
  564 | - [ ] **Step 4: Escrever testes de salvar, substituir, avançar e voltar**
  565 | 
  566 | ```python
  567 | def test_corrigir_resposta_substitui_sem_duplicar(self):
  568 |     salvar_resposta(self.triagem, "EXT-01", {"codigos": ["SIM"]})
  569 |     voltar_pergunta(self.triagem)
  570 |     salvar_resposta(self.triagem, "EXT-01", {"codigos": ["NAO"]})
  571 |     self.assertEqual(self.triagem.respostas.count(), 1)
  572 |     self.assertEqual(self.triagem.respostas.get().codigo_resposta, "NAO")
  573 | ```
  574 | 
  575 | - [ ] **Step 5: Implementar navegação e campos legados**
  576 | 
  577 | Usar `update_or_create` com `defaults` contendo `codigo_resposta`, `resposta_label`, `data_evento`, `metadata`, `valor`, `rule_version` e `source_ref`. `codigo_resposta` recebe o primeiro código, `resposta_label` reúne os rótulos selecionados, `data_evento` recebe a data estruturada e `valor` preserva todos os dados.
  578 | 
  579 | - [ ] **Step 6: Escrever testes das ramificações**
  580 | 
  581 | Verificar que `EXT-05A/05B` só aparecem após `EXT-05=SIM`; `EXT-06` só para 16-17; `EXT-07` só para 61-69; blocos de sintomas são mantidos quando `EXT-08` indica problema; e uma resposta positiva da simplificada insere os IDs `EXT-*` imediatamente antes de `SIM-17` sem duplicá-los.
  582 | 
  583 | - [ ] **Step 7: Implementar ramificações e conclusão imutável**
  584 | 
  585 | Recalcular o fluxo depois de cada resposta a partir do catálogo e das condições já respondidas. `concluir_triagem()` exige `EXT-51=CONFIRMAR` ou `SIM-18=ENTENDO`, chama o motor dentro de `transaction.atomic()`, salva todos os achados, resultado, data e `finalizada_em`, e muda o status para `CONCLUIDA`. Qualquer tentativa posterior de resposta gera `TriagemConcluida`.
  586 | 
  587 | - [ ] **Step 8: Executar os testes do serviço**
  588 | 
  589 | Run: `py manage.py test accounts.test_triagem_servico --settings=config.settings_test -v 2`
  590 | 
  591 | Expected: PASS.
  592 | 
  593 | - [ ] **Step 9: Registrar a etapa**
  594 | 
  595 | ```bash
  596 | git add accounts/triagem_servico.py accounts/test_triagem_servico.py
  597 | git commit -m "feat: add resumable triage workflow service"
  598 | ```
  599 | 
  600 | ---
  601 | 
  602 | ### Task 6: Views, rotas e páginas do questionário
  603 | 
  604 | **Files:**
  605 | - Modify: `accounts/views.py`
  606 | - Modify: `accounts/urls.py`
  607 | - Modify: `templates/accounts/triagem_apresentacao.html`
  608 | - Create: `templates/accounts/triagem_pergunta.html`
  609 | - Modify: `templates/accounts/triagem_resultado.html`
  610 | - Modify: `templates/accounts/triagem_extensa.html` somente se uma rota de compatibilidade ainda o utilizar.
  611 | - Preserve: `templates/accounts/triagem_inicio.html`, pois sua remoção não é necessária para o novo fluxo.
  612 | - Create: `accounts/test_triagem_views.py`
  613 | 
  614 | **Interfaces:**
  615 | - Consumes: `FormularioPergunta` e funções públicas de `triagem_servico`.
  616 | - Produces: rotas nomeadas `triagem_apresentacao`, `triagem_iniciar`, `triagem_pergunta` e `triagem_resultado`.
  617 | 
  618 | - [ ] **Step 1: Escrever testes da apresentação e perfis**
  619 | 
  620 | ```python
  621 | def test_apresentacao_publica_exibe_texto_e_duas_modalidades(self):
  622 |     resposta = self.client.get(reverse("accounts:triagem_apresentacao"))
  623 |     self.assertContains(resposta, "Seu gesto de cuidado começa aqui.")
  624 |     self.assertContains(resposta, "Triagem extensa")
  625 |     self.assertContains(resposta, "Triagem simplificada")
  626 |     self.assertContains(resposta, "Quem dará a resposta final será sempre a equipe do hemocentro")
  627 | 
  628 | def test_resultado_de_outro_usuario_retorna_404(self):
  629 |     self.client.force_login(self.outro_usuario)
  630 |     resposta = self.client.get(reverse(
  631 |         "accounts:triagem_resultado",
  632 |         kwargs={"id_triagem": self.triagem.pk},
  633 |     ))
  634 |     self.assertEqual(resposta.status_code, 404)
  635 | ```
  636 | 
  637 | - [ ] **Step 2: Executar e confirmar a falha de conteúdo e rotas**
  638 | 
  639 | Run: `py manage.py test accounts.test_triagem_views --settings=config.settings_test -v 2`
  640 | 
  641 | Expected: FAIL porque a apresentação atual não contém o texto integral e as novas rotas não existem.
  642 | 
  643 | - [ ] **Step 3: Implementar rotas únicas**
  644 | 
  645 | ```python
  646 | path("triagem/", views.triagem_apresentacao, name="triagem_apresentacao"),
  647 | path("triagem/iniciar/<str:modalidade>/", views.triagem_iniciar, name="triagem_iniciar"),
  648 | path("triagem/<int:id_triagem>/pergunta/", views.triagem_pergunta, name="triagem_pergunta"),
  649 | path("triagem/<int:id_triagem>/resultado/", views.triagem_resultado, name="triagem_resultado"),
  650 | ```
  651 | 
  652 | Remover as duplicações atuais de `triagem/` e de `triagem/<id>/resultado/`.
  653 | 
  654 | - [ ] **Step 4: Implementar views pequenas e seguras**
  655 | 
  656 | `triagem_iniciar` aceita somente POST e converte `extensa`/`simplificada` em `Triagem.Modalidade`. `triagem_pergunta` busca por `pk` e `usuario=request.user`, processa `acao=anterior`, `acao=salvar` ou `acao=continuar`; a conclusão redireciona ao resultado. `triagem_resultado` exige status concluído.
  657 | 
  658 | - [ ] **Step 5: Implementar templates sem CSS**
  659 | 
  660 | A apresentação reproduz integralmente o texto aprovado, usando `<strong>` nos trechos enfatizados. Cada modalidade possui formulário POST próprio. A página de pergunta exibe progresso, explicação, erros, `{{ form.as_p }}` e botões nomeados. O resultado mostra somente mensagem, estado, maior data, achados não íntimos e aviso final do hemocentro.
  661 | 
  662 | - [ ] **Step 6: Executar os testes de views**
  663 | 
  664 | Run: `py manage.py test accounts.test_triagem_views --settings=config.settings_test -v 2`
  665 | 
  666 | Expected: PASS.
  667 | 
  668 | - [ ] **Step 7: Registrar a etapa**
  669 | 
  670 | ```bash
  671 | git add accounts/views.py accounts/urls.py templates/accounts/triagem_apresentacao.html templates/accounts/triagem_pergunta.html templates/accounts/triagem_resultado.html templates/accounts/triagem_extensa.html accounts/test_triagem_views.py
  672 | git commit -m "feat: add complete triage web flow"
  673 | ```
  674 | 
  675 | ---
  676 | 
  677 | ### Task 7: Histórico privado, dashboard e admin
  678 | 
  679 | **Files:**
  680 | - Modify: `accounts/views.py`
  681 | - Modify: `accounts/urls.py`
  682 | - Create: `templates/accounts/triagem_historico.html`
  683 | - Modify: `templates/accounts/dashboard.html`
  684 | - Modify: `accounts/admin.py`
  685 | - Modify: `accounts/test_triagem_views.py`
  686 | 
  687 | **Interfaces:**
  688 | - Consumes: `Triagem` com status e proprietário.
  689 | - Produces: rota `triagem_historico`, contexto `ultima_triagem` no dashboard e admin integralmente somente leitura.
  690 | 
  691 | - [ ] **Step 1: Escrever testes do histórico e do resumo não sensível**
  692 | 
  693 | ```python
  694 | def test_historico_lista_somente_triagens_do_usuario(self):
  695 |     self.client.force_login(self.usuario)
  696 |     resposta = self.client.get(reverse("accounts:triagem_historico"))
  697 |     self.assertContains(resposta, f"Triagem {self.triagem.pk}")
  698 |     self.assertNotContains(resposta, f"Triagem {self.triagem_de_outro.pk}")
  699 | 
  700 | def test_dashboard_nao_exibe_respostas_intimas(self):
  701 |     RespostaTriagem.objects.create(
  702 |         triagem=self.triagem,
  703 |         id_pergunta="EXT-43",
  704 |         codigo_resposta="EXPOSICAO",
  705 |         resposta_label="Exposição íntima",
  706 |         valor={"codigos": ["EXPOSICAO"]},
  707 |     )
  708 |     self.client.force_login(self.usuario)
  709 |     resposta = self.client.get(reverse("accounts:dashboard"))
  710 |     self.assertNotContains(resposta, "Exposição íntima")
  711 | ```
  712 | 
  713 | - [ ] **Step 2: Executar e confirmar a falha pela rota ausente**
  714 | 
  715 | Run: `py manage.py test accounts.test_triagem_views --settings=config.settings_test -v 2`
  716 | 
  717 | Expected: FAIL em `triagem_historico`.
  718 | 
  719 | - [ ] **Step 3: Implementar histórico e dashboard**
  720 | 
  721 | `triagem_historico` usa `request.user.triagens.order_by("-iniciada_em")`. O dashboard recebe somente a triagem mais recente e nunca consulta `respostas`. Triagens em andamento exibem link de continuação; concluídas exibem link de resultado.
  722 | 
  723 | - [ ] **Step 4: Atualizar o admin**
  724 | 
  725 | Adicionar `status`, `triagem_base`, `pergunta_atual`, `fluxo_perguntas`, `atualizada_em` e `valor` a `readonly_fields`; incluir `status` em filtros/listagem. Manter `has_add_permission`, `has_change_permission` e `has_delete_permission` retornando `False`.
  726 | 
  727 | - [ ] **Step 5: Executar testes de privacidade e admin**
  728 | 
  729 | Run: `py manage.py test accounts.test_triagem_views accounts.test_triagem_models --settings=config.settings_test -v 2`
  730 | 
  731 | Expected: PASS.
  732 | 
  733 | - [ ] **Step 6: Registrar a etapa**
  734 | 
  735 | ```bash
  736 | git add accounts/views.py accounts/urls.py templates/accounts/triagem_historico.html templates/accounts/dashboard.html accounts/admin.py accounts/test_triagem_views.py
  737 | git commit -m "feat: add private triage history"
  738 | ```
  739 | 
  740 | ---
  741 | 
  742 | ### Task 8: Integração, limpeza e verificação completa
  743 | 
  744 | **Files:**
  745 | - Modify: `templates/accounts/inicio.html`
  746 | - Modify: `accounts/test_triagem.py`
  747 | - Modify: `accounts/migrations/README.md`
  748 | - Verify: todos os arquivos modificados pelas Tasks 1 a 7.
  749 | 
  750 | **Interfaces:**
  751 | - Consumes: fluxo completo implementado.
  752 | - Produces: projeto sem imports antigos, migrations sincronizadas e suíte verde.
  753 | 
  754 | - [ ] **Step 1: Escrever o teste de integração ponta a ponta**
  755 | 
  756 | O teste cria Doador, inicia extensa, responde o fluxo mínimo com códigos seguros, confirma `EXT-51`, verifica resultado concluído, inicia simplificada vinculada, responde `SIM-01` a `SIM-18`, confirma e verifica dois itens no histórico. Em outra execução, uma mudança em `SIM-10` deve inserir `EXT-21` a `EXT-24` antes da conclusão.
  757 | 
  758 | - [ ] **Step 2: Executar o teste e confirmar a primeira falha real**
  759 | 
  760 | Run: `py manage.py test accounts.test_triagem_views.TriagemFluxoCompletoTests --settings=config.settings_test -v 2`
  761 | 
  762 | Expected: FAIL no primeiro comportamento de integração ainda divergente.
  763 | 
  764 | - [ ] **Step 3: Corrigir somente as divergências observadas e remover código inicial substituído**
  765 | 
  766 | Remover imports de `TriagemExtensaForm`, `calcular_resultado` e `preparar_respostas` das views. Transformar `accounts/triagem.py` em um módulo de compatibilidade comentado que reexporta as novas interfaces, e adaptar `accounts/test_triagem.py` para não chamar o formulário único substituído. Corrigir o link público para `triagem_apresentacao` e manter toda a página inicial sem dados de saúde.
  767 | 
  768 | - [ ] **Step 4: Executar o teste de integração novamente**
  769 | 
  770 | Run: `py manage.py test accounts.test_triagem_views.TriagemFluxoCompletoTests --settings=config.settings_test -v 2`
  771 | 
  772 | Expected: PASS.
  773 | 
  774 | - [ ] **Step 5: Executar verificações estáticas e suíte completa**
  775 | 
  776 | Run: `py manage.py check --settings=config.settings_test`
  777 | 
  778 | Expected: `System check identified no issues`.
  779 | 
  780 | Run: `py manage.py makemigrations --check --settings=config.settings_test`
  781 | 
  782 | Expected: `No changes detected`.
  783 | 
  784 | Run: `py manage.py test --settings=config.settings_test -v 2`
  785 | 
  786 | Expected: PASS para toda a suíte.
  787 | 
  788 | Run: `git diff --check`
  789 | 
  790 | Expected: nenhuma saída de erro.
  791 | 
  792 | - [ ] **Step 6: Aplicar a migration no PostgreSQL local autorizado**
  793 | 
  794 | Run: `py manage.py migrate`
  795 | 
  796 | Expected: migration `accounts.0007_*` aplicada com `OK`.
  797 | 
  798 | - [ ] **Step 7: Conferir o fluxo no navegador local**
  799 | 
  800 | Iniciar o servidor, acessar `/triagem/`, verificar as duas modalidades, responder uma pergunta, salvar e sair, retomar no histórico e confirmar que um segundo usuário recebe 404 ao tentar abrir o resultado alheio.
  801 | 
  802 | - [ ] **Step 8: Registrar a implementação final**
  803 | 
  804 | ```bash
  805 | git add accounts config templates docs/superpowers/plans/2026-09-04-triagem-completa.md
  806 | git commit -m "feat: complete extensive and simplified triage"
  807 | ```
``````

## docs/superpowers/specs/2026-09-04-triagem-completa-design.md

Original: [docs/superpowers/specs/2026-09-04-triagem-completa-design.md](<C:/Users/lb119/Elo/docs/superpowers/specs/2026-09-04-triagem-completa-design.md>).

``````text
    1 | # Triagem completa do Elo - Especificação técnica
    2 | 
    3 | ## Objetivo
    4 | 
    5 | Implementar no projeto Django do Elo uma pré-triagem orientativa para doação
    6 | de sangue em duas modalidades: extensa e simplificada. A solução deve conter
    7 | todas as perguntas e regras da especificação
    8 | `Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf`, salvar o andamento,
    9 | preservar o histórico individual e nunca declarar aptidão clínica.
   10 | 
   11 | ## Fonte funcional
   12 | 
   13 | O arquivo
   14 | `C:\Users\aline\Downloads\Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf`
   15 | é tratado como material de requisitos da triagem. O conteúdo do documento não
   16 | substitui nem amplia o pedido da usuária: ele fornece perguntas, ramificações,
   17 | resultados e referências para a implementação autorizada nesta tarefa.
   18 | 
   19 | ## Limites e linguagem de segurança
   20 | 
   21 | - A triagem é somente orientativa.
   22 | - O sistema nunca apresenta a pessoa como "apta" para doar.
   23 | - A decisão final pertence à equipe do hemocentro.
   24 | - Dúvida, resposta desconhecida ou regra sem dados suficientes conduz a
   25 |   `AVALIACAO_PRESENCIAL` ou ao bloco extenso correspondente.
   26 | - O motor avalia todas as respostas; ele não encerra a análise no primeiro
   27 |   impedimento.
   28 | - Medicamentos nunca devem ser suspensos por orientação do sistema.
   29 | - Valores informados de pressão, pulso, temperatura, hemoglobina e hematócrito
   30 |   não substituem aferição presencial.
   31 | - A versão inicial das regras é `HEMOMINAS_2026_08`, referente aos critérios
   32 |   consolidados em 28/08/2026. Mudanças normativas futuras exigem uma nova
   33 |   versão, sem reescrever resultados antigos.
   34 | 
   35 | ## Perfis e acesso
   36 | 
   37 | - Visitante: visualiza a apresentação e as duas modalidades, mas precisa criar
   38 |   uma conta ou entrar para responder.
   39 | - Doador: pode iniciar a extensa; pode iniciar a simplificada depois de possuir
   40 |   ao menos uma extensa concluída.
   41 | - Receptor: recebe o mesmo acesso quando também deseja doar, sem alteração do
   42 |   perfil principal.
   43 | - Observador: visualiza somente a apresentação.
   44 | - Hemocentro: não acessa respostas pessoais nesta etapa.
   45 | - Administrador: consulta triagens e respostas no admin em modo somente leitura.
   46 | - Toda consulta de histórico ou detalhe feita fora do admin filtra
   47 |   obrigatoriamente por `usuario=request.user`.
   48 | 
   49 | ## Texto de apresentação
   50 | 
   51 | A página de escolha exibirá integralmente o texto fornecido pela usuária,
   52 | começando com "Seu gesto de cuidado começa aqui." e terminando com a chamada
   53 | para escolher a modalidade. A página não terá CSS nesta etapa.
   54 | 
   55 | As duas modalidades sempre aparecem. Quando a pessoa ainda não possui uma
   56 | triagem extensa concluída, a simplificada permanece visível, mas a tentativa de
   57 | iniciá-la explica a condição e direciona para a extensa.
   58 | 
   59 | ## Organização do código
   60 | 
   61 | ### Catálogos de perguntas
   62 | 
   63 | As perguntas ficam versionadas em código, e não em novas tabelas administrativas.
   64 | Isso mantém a implementação didática, revisável por Git e coerente com o tamanho
   65 | atual do projeto.
   66 | 
   67 | - `accounts/triagem_catalogo_extensa.py`: perguntas `EXT-01` a `EXT-51`,
   68 |   alternativas, explicações, categoria, tipo do campo, obrigatoriedade,
   69 |   ramificações, fonte e regras.
   70 | - `accounts/triagem_catalogo_simplificada.py`: perguntas `SIM-01` a `SIM-18`,
   71 |   alternativas, regras e blocos extensos acionados por mudança ou dúvida.
   72 | - Cada pergunta possui identificador estável; textos podem evoluir sem alterar
   73 |   a identidade da pergunta.
   74 | - Perguntas de seleção múltipla armazenam uma lista de códigos.
   75 | - Datas e detalhes complementares ficam no mesmo valor estruturado da resposta.
   76 | 
   77 | ### Motor de regras
   78 | 
   79 | `accounts/triagem_motor.py` será uma função pura: recebe modalidade, respostas,
   80 | data de referência e versão; devolve todos os achados, resultado principal,
   81 | data de liberação mais distante e mensagem segura.
   82 | 
   83 | Cada achado contém:
   84 | 
   85 | - `id_pergunta`;
   86 | - `codigo_regra`;
   87 | - `categoria`;
   88 | - `resultado`;
   89 | - `mensagem`;
   90 | - `data_liberacao`, quando calculável;
   91 | - `exige_relatorio`;
   92 | - `fonte`;
   93 | - `regra_version`.
   94 | 
   95 | A prioridade do resultado principal é:
   96 | 
   97 | 1. `INAPTIDAO_DEFINITIVA`;
   98 | 2. `AVALIACAO_PRESENCIAL`;
   99 | 3. `INAPTIDAO_TEMPORARIA`;
  100 | 4. `DOCUMENTACAO_ESPECIAL`;
  101 | 5. `SEM_IMPEDIMENTO_IDENTIFICADO`.
  102 | 
  103 | Quando existirem vários impedimentos temporários, a data principal será a mais
  104 | distante. Prazos dependentes de cura, alta, retirada ou término de tratamento
  105 | só serão calculados quando a respectiva data de referência for informada.
  106 | 
  107 | ### Formulário dinâmico
  108 | 
  109 | `accounts/triagem_forms.py` construirá um formulário Django para uma pergunta
  110 | por vez. Os tipos aceitos serão escolha única, escolha múltipla, data, número e
  111 | texto curto. A validação rejeitará datas futuras indevidas, respostas fora do
  112 | catálogo e ausência de complementos exigidos.
  113 | 
  114 | O HTML permanecerá simples e sem CSS. Cada tela mostrará:
  115 | 
  116 | - modalidade e progresso;
  117 | - código e texto da pergunta;
  118 | - explicação curta;
  119 | - alternativas ou campo complementar;
  120 | - botões "Anterior", "Salvar e sair" e "Continuar".
  121 | 
  122 | ### Serviço de aplicação
  123 | 
  124 | `accounts/triagem_servico.py` centralizará operações que alteram o banco:
  125 | 
  126 | - criar uma triagem em andamento;
  127 | - validar se a pessoa pode usar a modalidade;
  128 | - localizar a pergunta atual;
  129 | - salvar ou substituir a resposta da pergunta atual;
  130 | - avançar e voltar sem duplicar respostas;
  131 | - acrescentar blocos extensos acionados pela simplificada;
  132 | - concluir a triagem em uma transação;
  133 | - calcular e salvar resultado e achados;
  134 | - localizar a extensa-base usada pela simplificada.
  135 | 
  136 | As views apenas recebem a requisição, chamam o serviço e renderizam templates.
  137 | 
  138 | ## Persistência e migration
  139 | 
  140 | Os models `Triagem` e `RespostaTriagem` existentes serão preservados e
  141 | estendidos. Uma nova migration será necessária.
  142 | 
  143 | ### Alterações em `Triagem`
  144 | 
  145 | - `status`: `EM_ANDAMENTO`, `CONCLUIDA` ou `CANCELADA`;
  146 | - `pergunta_atual`: posição atual do fluxo;
  147 | - `fluxo_perguntas`: lista JSON com a ordem efetiva das perguntas;
  148 | - `triagem_base`: referência opcional à extensa anterior usada pela
  149 |   simplificada;
  150 | - `atualizada_em`: data da última resposta;
  151 | - resultado, achados e finalização continuam vazios enquanto estiver em
  152 |   andamento.
  153 | 
  154 | ### Alterações em `RespostaTriagem`
  155 | 
  156 | - `valor`: JSON com o valor completo e estruturado da resposta;
  157 | - restrição única por `triagem` e `id_pergunta`, para que voltar e corrigir
  158 |   substitua a resposta em vez de criar duplicatas.
  159 | 
  160 | Os campos antigos serão mantidos para compatibilidade e leitura no admin.
  161 | 
  162 | ## Fluxo extenso
  163 | 
  164 | 1. A pessoa lê a apresentação e escolhe a extensa.
  165 | 2. O sistema cria uma `Triagem` em andamento e registra o termo de triagem.
  166 | 3. A pessoa responde `EXT-01` a `EXT-51` respeitando as ramificações descritas
  167 |    na especificação.
  168 | 4. Respostas "não" em blocos principais pulam subperguntas que não se aplicam.
  169 | 5. Seleções de condição abrem seus complementos de data, tratamento,
  170 |    complicação, medicamento, documento ou relatório quando exigidos.
  171 | 6. `EXT-51` permite revisar; somente a confirmação conclui.
  172 | 7. O motor gera todos os achados e salva o resultado imutável daquela execução.
  173 | 
  174 | ## Fluxo simplificado
  175 | 
  176 | 1. O sistema exige uma extensa concluída do mesmo usuário.
  177 | 2. A pessoa confirma que o resumo anterior continua correto em `SIM-01`.
  178 | 3. Responde `SIM-02` a `SIM-18` sobre mudanças desde a extensa.
  179 | 4. Respostas sem mudança reutilizam apenas o contexto necessário da extensa,
  180 |    sem duplicar detalhes íntimos na interface.
  181 | 5. Respostas positivas ou desconhecidas inserem na fila os blocos extensos
  182 |    indicados pela especificação.
  183 | 6. Se a base estiver incorreta ou incompleta, a pessoa é direcionada para uma
  184 |    nova extensa.
  185 | 7. O resultado registra a extensa-base, a versão das regras e todas as novas
  186 |    respostas.
  187 | 
  188 | ## Histórico no perfil
  189 | 
  190 | O dashboard exibirá somente informações não íntimas da triagem mais recente:
  191 | 
  192 | - modalidade;
  193 | - resultado orientativo;
  194 | - data de conclusão;
  195 | - data orientativa de liberação, quando existir;
  196 | - botão para abrir o detalhe privado;
  197 | - link para "Meu histórico de triagens".
  198 | 
  199 | A página de histórico lista todas as triagens do usuário, inclusive as em
  200 | andamento, com opção de continuar. Nenhum resultado anterior é sobrescrito.
  201 | O detalhe completo e as respostas só podem ser visualizados pelo dono da
  202 | triagem. O admin permanece somente leitura.
  203 | 
  204 | ## Templates e rotas
  205 | 
  206 | Serão criadas ou atualizadas as seguintes páginas:
  207 | 
  208 | - `/triagem/`: apresentação e escolha da modalidade;
  209 | - `/triagem/extensa/iniciar/`;
  210 | - `/triagem/simplificada/iniciar/`;
  211 | - `/triagem/<id>/pergunta/`;
  212 | - `/triagem/<id>/historico/` ou ação equivalente para voltar;
  213 | - `/triagem/<id>/resultado/`;
  214 | - `/triagens/historico/`.
  215 | 
  216 | Os templates serão:
  217 | 
  218 | - `triagem_apresentacao.html`;
  219 | - `triagem_pergunta.html`;
  220 | - `triagem_resultado.html`;
  221 | - `triagem_historico.html`.
  222 | 
  223 | Os links serão incluídos na página pública e nos dashboards de Doador e
  224 | Receptor. Hemocentro e Observador verão apenas a apresentação pública.
  225 | 
  226 | ## Privacidade
  227 | 
  228 | - Dados de saúde não aparecem em estoque, pedidos, campanhas, ranking ou
  229 |   notificações genéricas.
  230 | - O dashboard não exibe diagnósticos, uso de drogas, vida sexual, HIV, hepatite
  231 |   ou outras respostas íntimas.
  232 | - Objetos são buscados sempre com verificação de proprietário.
  233 | - O admin exibe aviso de dado sensível e bloqueia criação, edição e exclusão.
  234 | - Histórico não é compartilhado com Hemocentro nesta etapa.
  235 | - O consentimento de triagem continua versionado em `ConsentimentoLGPD`.
  236 | 
  237 | ## Compatibilidade com dados existentes
  238 | 
  239 | - A migration `0006` e as triagens já salvas permanecem válidas.
  240 | - Registros antigos sem `status` recebem `CONCLUIDA` quando possuem
  241 |   `finalizada_em`; caso contrário recebem `EM_ANDAMENTO` por migration de dados.
  242 | - As respostas antigas serão convertidas para o novo campo `valor` usando
  243 |   `codigo_resposta`, `resposta_label`, `data_evento` e `metadata`.
  244 | - Nenhum arquivo de migration já aplicado será editado.
  245 | 
  246 | ## Tratamento de erros
  247 | 
  248 | - ID de triagem inexistente ou pertencente a outro usuário retorna 404.
  249 | - Modalidade simplificada sem extensa-base redireciona para a apresentação com
  250 |   mensagem explicativa.
  251 | - Pergunta ou alternativa inválida não é persistida.
  252 | - Falha ao concluir reverte resultado e respostas da operação pela transação.
  253 | - Triagem concluída não aceita novas respostas; revisão cria uma nova execução
  254 |   ou ocorre antes da confirmação final.
  255 | 
  256 | ## Testes
  257 | 
  258 | Os testes automatizados cobrirão:
  259 | 
  260 | - catálogo com as 55 entradas extensas (`EXT-01` a `EXT-51`, incluindo as quatro subperguntas) e todos os IDs `SIM-01` a `SIM-18`;
  261 | - alternativas e fontes obrigatórias;
  262 | - ramificações principais e retorno à pergunta anterior;
  263 | - cálculo de 48h, 72h, dias, semanas, meses e anos;
  264 | - escolha da data temporária mais distante;
  265 | - prioridade entre definitiva, avaliação, temporária e documentação;
  266 | - exceções descritas no PDF;
  267 | - comportamento de "não sei";
  268 | - simplificada bloqueada sem extensa;
  269 | - abertura de blocos extensos pela simplificada;
  270 | - histórico isolado por usuário;
  271 | - retomada de triagem em andamento;
  272 | - imutabilidade após conclusão;
  273 | - acesso de Visitante, Doador, Receptor, Observador, Hemocentro e Administrador;
  274 | - não exposição de respostas sensíveis no dashboard e nas páginas públicas;
  275 | - compatibilidade da migration com registros da versão inicial.
  276 | 
  277 | ## Critério de conclusão
  278 | 
  279 | A funcionalidade estará concluída quando as 55 entradas extensas e as 18
  280 | simplificadas estiverem representadas no catálogo, as ramificações e regras
  281 | estiverem cobertas por testes, cada resultado permanecer no histórico privado,
  282 | as duas modalidades estiverem apontadas no site e `python manage.py check`,
  283 | `python manage.py makemigrations --check` e `python manage.py test` passarem.
``````

## elo_front/README-INSTALACAO.txt

Original: [elo_front/README-INSTALACAO.txt](<C:/Users/lb119/Elo/elo_front/README-INSTALACAO.txt>).

``````text
    1 | ELO — FRONTEND VISUAL
    2 | 
    3 | Arquivos incluídos:
    4 | - templates/base.html
    5 | - templates/accounts/inicio.html
    6 | - static/css/elo.css
    7 | 
    8 | Como instalar:
    9 | 1. Faça backup dos arquivos atuais.
   10 | 2. Copie base.html para:
   11 |    templates/base.html
   12 | 3. Copie inicio.html para:
   13 |    templates/accounts/inicio.html
   14 | 4. Copie elo.css para:
   15 |    static/css/elo.css
   16 | 5. Execute:
   17 |    python manage.py runserver
   18 | 
   19 | Observações:
   20 | - O frontend usa as URLs existentes do app accounts.
   21 | - Não altera models.py, views.py ou urls.py.
   22 | - A seção de estoque usa estoque_geral que já é enviado pela view inicio.
   23 | - O CSS também fornece estilo base para formulários das outras telas.
``````

## elo_front/static/css/elo.css

Original: [elo_front/static/css/elo.css](<C:/Users/lb119/Elo/elo_front/static/css/elo.css>).

``````text
    1 | @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600;1,700&display=swap');
    2 | 
    3 | :root {
    4 |     --red: #bd1026;
    5 |     --red-dark: #a20d20;
    6 |     --red-light: #d64a59;
    7 |     --black: #17181b;
    8 |     --text: #37383d;
    9 |     --muted: #6f7076;
   10 |     --line: #e8e8e8;
   11 |     --soft: #f7f7f7;
   12 |     --white: #ffffff;
   13 |     --success: #177245;
   14 |     --warning: #bd1026;
   15 |     --shadow: 0 16px 40px rgba(20, 20, 20, .06);
   16 | }
   17 | 
   18 | * {
   19 |     box-sizing: border-box;
   20 | }
   21 | 
   22 | html {
   23 |     scroll-behavior: smooth;
   24 | }
   25 | 
   26 | body {
   27 |     margin: 0;
   28 |     color: var(--text);
   29 |     background: var(--white);
   30 |     font-family: "DM Sans", Arial, sans-serif;
   31 |     font-size: 16px;
   32 |     line-height: 1.6;
   33 | }
   34 | 
   35 | a {
   36 |     color: inherit;
   37 |     text-decoration: none;
   38 | }
   39 | 
   40 | button,
   41 | input,
   42 | select,
   43 | textarea {
   44 |     font: inherit;
   45 | }
   46 | 
   47 | .container {
   48 |     width: min(1160px, calc(100% - 80px));
   49 |     margin: 0 auto;
   50 | }
   51 | 
   52 | /* HEADER */
   53 | 
   54 | .site-header {
   55 |     height: 112px;
   56 |     background: var(--white);
   57 |     border-bottom: 1px solid var(--line);
   58 |     display: flex;
   59 |     align-items: center;
   60 | }
   61 | 
   62 | .header-inner {
   63 |     width: min(1160px, calc(100% - 80px));
   64 |     margin: 0 auto;
   65 |     display: flex;
   66 |     align-items: center;
   67 |     justify-content: space-between;
   68 |     gap: 40px;
   69 | }
   70 | 
   71 | .brand {
   72 |     display: inline-flex;
   73 |     align-items: center;
   74 |     gap: 10px;
   75 |     color: var(--red);
   76 |     flex-shrink: 0;
   77 | }
   78 | 
   79 | .brand-mark {
   80 |     display: inline-block;
   81 |     flex-shrink: 0;
   82 | }
   83 | 
   84 | .site-header .brand-mark {
   85 |     width: 42px;
   86 |     height: 42px;
   87 |     background: url("logo-gota.png") center / contain no-repeat;
   88 | }
   89 | 
   90 | .brand-name {
   91 |     font-family: "Playfair Display", Georgia, serif;
   92 |     font-size: 36px;
   93 |     font-style: italic;
   94 |     font-weight: 700;
   95 |     line-height: 1;
   96 |     letter-spacing: 0;
   97 | }
   98 | 
   99 | .main-nav {
  100 |     display: flex;
  101 |     align-items: center;
  102 |     gap: 46px;
  103 | }
  104 | 
  105 | .main-nav > a {
  106 |     min-height: 44px;
  107 |     display: inline-flex;
  108 |     align-items: center;
  109 |     justify-content: center;
  110 |     font-size: 15px;
  111 |     font-weight: 500;
  112 |     line-height: 1.2;
  113 |     text-align: center;
  114 |     color: #292a2d;
  115 |     transition: color .2s ease;
  116 | }
  117 | 
  118 | .main-nav > a:hover {
  119 |     color: var(--red);
  120 | }
  121 | 
  122 | .main-nav .nav-cta {
  123 |     color: var(--white);
  124 |     background: var(--red);
  125 |     border-radius: 5px;
  126 |     padding: 12px 25px;
  127 |     font-weight: 700;
  128 | }
  129 | 
  130 | .main-nav .nav-cta:hover {
  131 |     color: var(--white);
  132 |     background: var(--red-dark);
  133 | }
  134 | 
  135 | .menu-toggle {
  136 |     display: none;
  137 |     width: 44px;
  138 |     height: 44px;
  139 |     border: 0;
  140 |     background: transparent;
  141 |     cursor: pointer;
  142 | }
  143 | 
  144 | .menu-toggle span {
  145 |     display: block;
  146 |     width: 25px;
  147 |     height: 2px;
  148 |     background: var(--black);
  149 |     margin: 5px auto;
  150 | }
  151 | 
  152 | /* HERO */
  153 | 
  154 | .hero {
  155 |     min-height: 594px;
  156 |     background: var(--white);
  157 |     display: flex;
  158 |     align-items: center;
  159 | }
  160 | 
  161 | .hero-inner {
  162 |     padding: 78px 0 76px;
  163 | }
  164 | 
  165 | .hero-copy {
  166 |     max-width: 610px;
  167 | }
  168 | 
  169 | .eyebrow {
  170 |     margin: 0 0 22px;
  171 |     color: var(--red);
  172 |     font-size: 13px;
  173 |     line-height: 1.2;
  174 |     letter-spacing: 1.7px;
  175 |     font-weight: 700;
  176 | }
  177 | 
  178 | .hero h1 {
  179 |     margin: 0;
  180 |     color: var(--black);
  181 |     font-family: "Playfair Display", Georgia, serif;
  182 |     font-size: clamp(58px, 6.1vw, 82px);
  183 |     line-height: .99;
  184 |     letter-spacing: -3px;
  185 |     font-weight: 700;
  186 | }
  187 | 
  188 | .hero h1 em {
  189 |     color: var(--red);
  190 |     font-weight: 600;
  191 | }
  192 | 
  193 | .hero-text {
  194 |     max-width: 570px;
  195 |     margin: 32px 0 44px;
  196 |     color: #55565b;
  197 |     font-size: 17px;
  198 |     line-height: 1.7;
  199 | }
  200 | 
  201 | .hero-actions {
  202 |     display: flex;
  203 |     align-items: center;
  204 |     flex-wrap: wrap;
  205 |     gap: 25px;
  206 | }
  207 | 
  208 | .button {
  209 |     min-height: 50px;
  210 |     padding: 13px 26px;
  211 |     border-radius: 5px;
  212 |     display: inline-flex;
  213 |     justify-content: center;
  214 |     align-items: center;
  215 |     border: 1px solid transparent;
  216 |     font-weight: 700;
  217 |     font-size: 15px;
  218 |     line-height: 1.2;
  219 |     text-align: center;
  220 |     transition: .2s ease;
  221 | }
  222 | 
  223 | .button-primary {
  224 |     color: var(--white);
  225 |     background: var(--red);
  226 | }
  227 | 
  228 | .button-primary:hover {
  229 |     background: var(--red-dark);
  230 |     transform: translateY(-1px);
  231 | }
  232 | 
  233 | .button-outline {
  234 |     color: var(--red);
  235 |     background: transparent;
  236 |     border-color: var(--red);
  237 | }
  238 | 
  239 | .button-outline:hover {
  240 |     background: #fff5f6;
  241 | }
  242 | 
  243 | .button-small {
  244 |     min-width: 260px;
  245 | }
  246 | 
  247 | /* ESTOQUE */
  248 | 
  249 | .stock-section {
  250 |     background: #f6f6f6;
  251 |     padding: 64px 0 58px;
  252 | }
  253 | 
  254 | .section-heading h2,
  255 | .info-section h2,
  256 | .faq-section h2 {
  257 |     margin: 0;
  258 |     color: var(--black);
  259 |     font-family: "Playfair Display", Georgia, serif;
  260 |     font-size: 31px;
  261 |     line-height: 1.15;
  262 |     letter-spacing: -.5px;
  263 | }
  264 | 
  265 | .section-heading p {
  266 |     max-width: 640px;
  267 |     margin: 8px auto 0;
  268 |     color: #4c4d51;
  269 |     font-size: 16px;
  270 |     text-align: center;
  271 | }
  272 | 
  273 | .section-heading {
  274 |     text-align: center;
  275 | }
  276 | 
  277 | .blood-grid {
  278 |     display: grid;
  279 |     grid-template-columns: repeat(4, 1fr);
  280 |     gap: 58px 40px;
  281 |     margin: 42px 35px 48px;
  282 | }
  283 | 
  284 | .blood-card {
  285 |     min-height: 112px;
  286 |     text-align: center;
  287 |     display: flex;
  288 |     flex-direction: column;
  289 |     align-items: center;
  290 |     justify-content: center;
  291 | }
  292 | 
  293 | .blood-type {
  294 |     color: #202125;
  295 |     font-size: 31px;
  296 |     line-height: 1;
  297 |     font-weight: 500;
  298 | }
  299 | 
  300 | .blood-line {
  301 |     width: 86px;
  302 |     height: 2px;
  303 |     background: var(--red-light);
  304 |     margin: 20px 0 11px;
  305 | }
  306 | 
  307 | .blood-status {
  308 |     font-size: 19px;
  309 |     line-height: 1.2;
  310 |     font-weight: 700;
  311 | }
  312 | 
  313 | .status-critical,
  314 | .status-alert {
  315 |     color: var(--red);
  316 | }
  317 | 
  318 | .status-stable {
  319 |     color: var(--red);
  320 | }
  321 | 
  322 | .center-action {
  323 |     display: flex;
  324 |     justify-content: center;
  325 |     text-align: center;
  326 | }
  327 | 
  328 | /* INFO */
  329 | 
  330 | .info-section {
  331 |     padding: 100px 0;
  332 |     border-bottom: 1px solid var(--line);
  333 | }
  334 | 
  335 | .info-grid {
  336 |     display: grid;
  337 |     grid-template-columns: 1fr 1fr;
  338 |     gap: 80px;
  339 |     align-items: center;
  340 | }
  341 | 
  342 | .info-section h2 {
  343 |     max-width: 520px;
  344 |     font-size: 42px;
  345 | }
  346 | 
  347 | .info-text {
  348 |     max-width: 500px;
  349 |     color: var(--muted);
  350 |     font-size: 17px;
  351 | }
  352 | 
  353 | .text-link {
  354 |     color: var(--red);
  355 |     font-weight: 700;
  356 | }
  357 | 
  358 | .text-link:hover {
  359 |     text-decoration: underline;
  360 | }
  361 | 
  362 | /* DÚVIDAS */
  363 | 
  364 | .faq-section {
  365 |     padding: 90px 0;
  366 | }
  367 | 
  368 | .faq-section > .container > h2 {
  369 |     margin-top: 4px;
  370 |     margin-bottom: 35px;
  371 | }
  372 | 
  373 | .faq-grid {
  374 |     display: grid;
  375 |     grid-template-columns: repeat(3, 1fr);
  376 |     gap: 20px;
  377 | }
  378 | 
  379 | .faq-grid details {
  380 |     background: var(--soft);
  381 |     border: 1px solid var(--line);
  382 |     padding: 22px;
  383 |     border-radius: 6px;
  384 | }
  385 | 
  386 | .faq-grid summary {
  387 |     cursor: pointer;
  388 |     color: var(--black);
  389 |     font-weight: 700;
  390 | }
  391 | 
  392 | .faq-grid p {
  393 |     color: var(--muted);
  394 |     margin-bottom: 0;
  395 | }
  396 | 
  397 | /* MENSAGENS */
  398 | 
  399 | .messages-wrap {
  400 |     width: min(1160px, calc(100% - 80px));
  401 |     margin: 20px auto 0;
  402 | }
  403 | 
  404 | .message {
  405 |     padding: 13px 16px;
  406 |     border: 1px solid var(--line);
  407 |     border-left: 4px solid var(--red);
  408 |     background: #fff8f8;
  409 |     border-radius: 4px;
  410 | }
  411 | 
  412 | /* FOOTER */
  413 | 
  414 | .site-footer {
  415 |     background: #17181b;
  416 |     color: #d9d9dc;
  417 |     padding: 44px 0;
  418 | }
  419 | 
  420 | .footer-inner {
  421 |     width: min(1160px, calc(100% - 80px));
  422 |     margin: 0 auto;
  423 |     display: grid;
  424 |     grid-template-columns: auto 1fr auto;
  425 |     gap: 30px;
  426 |     align-items: center;
  427 | }
  428 | 
  429 | .brand-footer .brand-name {
  430 |     font-size: 31px;
  431 | }
  432 | 
  433 | .brand-footer .brand-mark {
  434 |     display: none;
  435 | }
  436 | 
  437 | .footer-inner p {
  438 |     margin: 0;
  439 |     color: #a9aaae;
  440 | }
  441 | 
  442 | .footer-links {
  443 |     display: flex;
  444 |     gap: 20px;
  445 |     flex-wrap: wrap;
  446 | }
  447 | 
  448 | .footer-links a {
  449 |     font-size: 14px;
  450 |     color: #d9d9dc;
  451 | }
  452 | 
  453 | .footer-links a:hover {
  454 |     color: var(--white);
  455 | }
  456 | 
  457 | /* FORMULÁRIOS / OUTRAS PÁGINAS */
  458 | 
  459 | main form:not(.plain-form) {
  460 |     max-width: 760px;
  461 | }
  462 | 
  463 | main input,
  464 | main select,
  465 | main textarea {
  466 |     border: 1px solid #d8d8db;
  467 |     border-radius: 5px;
  468 |     padding: 11px 13px;
  469 |     background: var(--white);
  470 |     color: var(--black);
  471 | }
  472 | 
  473 | main input:focus,
  474 | main select:focus,
  475 | main textarea:focus {
  476 |     outline: 2px solid rgba(189, 16, 38, .14);
  477 |     border-color: var(--red);
  478 | }
  479 | 
  480 | main button[type="submit"] {
  481 |     min-height: 48px;
  482 |     border: 0;
  483 |     border-radius: 5px;
  484 |     padding: 12px 22px;
  485 |     display: inline-flex;
  486 |     align-items: center;
  487 |     justify-content: center;
  488 |     background: var(--red);
  489 |     color: var(--white);
  490 |     font-weight: 700;
  491 |     line-height: 1.2;
  492 |     text-align: center;
  493 |     cursor: pointer;
  494 | }
  495 | 
  496 | main button[type="submit"]:hover {
  497 |     background: var(--red-dark);
  498 | }
  499 | 
  500 | .empty-state {
  501 |     grid-column: 1 / -1;
  502 |     color: var(--muted);
  503 |     text-align: center;
  504 | }
  505 | 
  506 | /* RESPONSIVO */
  507 | 
  508 | @media (max-width: 900px) {
  509 |     .container,
  510 |     .header-inner,
  511 |     .footer-inner,
  512 |     .messages-wrap {
  513 |         width: min(100% - 40px, 720px);
  514 |     }
  515 | 
  516 |     .site-header {
  517 |         height: 84px;
  518 |     }
  519 | 
  520 |     .menu-toggle {
  521 |         display: block;
  522 |     }
  523 | 
  524 |     .main-nav {
  525 |         position: absolute;
  526 |         left: 20px;
  527 |         right: 20px;
  528 |         top: 84px;
  529 |         z-index: 20;
  530 |         display: none;
  531 |         flex-direction: column;
  532 |         align-items: stretch;
  533 |         gap: 0;
  534 |         background: var(--white);
  535 |         border: 1px solid var(--line);
  536 |         box-shadow: var(--shadow);
  537 |     }
  538 | 
  539 |     .main-nav.is-open {
  540 |         display: flex;
  541 |     }
  542 | 
  543 |     .main-nav > a {
  544 |         padding: 15px 18px;
  545 |         border-bottom: 1px solid var(--line);
  546 |     }
  547 | 
  548 |     .main-nav .nav-cta {
  549 |         margin: 12px;
  550 |         text-align: center;
  551 |         border-bottom: 0;
  552 |     }
  553 | 
  554 |     .hero {
  555 |         min-height: auto;
  556 |     }
  557 | 
  558 |     .hero-copy {
  559 |         margin: 0 auto;
  560 |         text-align: center;
  561 |     }
  562 | 
  563 |     .hero-inner {
  564 |         padding: 65px 0 70px;
  565 |     }
  566 | 
  567 |     .hero-actions {
  568 |         justify-content: center;
  569 |     }
  570 | 
  571 |     .hero h1 {
  572 |         font-size: clamp(52px, 12vw, 72px);
  573 |     }
  574 | 
  575 |     .blood-grid {
  576 |         grid-template-columns: repeat(2, 1fr);
  577 |         gap: 35px 20px;
  578 |         margin-left: 0;
  579 |         margin-right: 0;
  580 |     }
  581 | 
  582 |     .info-grid,
  583 |     .faq-grid {
  584 |         grid-template-columns: 1fr;
  585 |         gap: 35px;
  586 |     }
  587 | 
  588 |     .footer-inner {
  589 |         grid-template-columns: 1fr;
  590 |     }
  591 | }
  592 | 
  593 | @media (max-width: 520px) {
  594 |     .container,
  595 |     .header-inner,
  596 |     .footer-inner,
  597 |     .messages-wrap {
  598 |         width: calc(100% - 32px);
  599 |     }
  600 | 
  601 |     .brand-name {
  602 |         font-size: 31px;
  603 |     }
  604 | 
  605 |     .brand-mark {
  606 |         width: 36px;
  607 |         height: 36px;
  608 |     }
  609 | 
  610 |     .site-header .brand-mark {
  611 |         width: 36px;
  612 |         height: 36px;
  613 |     }
  614 | 
  615 |     .hero h1 {
  616 |         font-size: 51px;
  617 |         letter-spacing: -2px;
  618 |     }
  619 | 
  620 |     .hero-text {
  621 |         font-size: 16px;
  622 |     }
  623 | 
  624 |     .hero-actions {
  625 |         flex-direction: column;
  626 |         align-items: stretch;
  627 |     }
  628 | 
  629 |     .button {
  630 |         width: 100%;
  631 |     }
  632 | 
  633 |     .blood-grid {
  634 |         grid-template-columns: repeat(2, 1fr);
  635 |     }
  636 | 
  637 |     .blood-type {
  638 |         font-size: 27px;
  639 |     }
  640 | 
  641 |     .info-section h2 {
  642 |         font-size: 34px;
  643 |     }
  644 | 
  645 |     .footer-links {
  646 |         flex-direction: column;
  647 |         gap: 8px;
  648 |     }
  649 | }
``````

## elo_front/templates/accounts/inicio.html

Original: [elo_front/templates/accounts/inicio.html](<C:/Users/lb119/Elo/elo_front/templates/accounts/inicio.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% block title %}Elo - Cada gota e um elo de vida{% endblock %}
    4 | 
    5 | {% block content %}
    6 | 
    7 | <section class="hero" id="sobre">
    8 |     <div class="container hero-inner">
    9 |         <div class="hero-copy">
   10 |             <p class="eyebrow">SISTEMA DE DOACAO DE SANGUE</p>
   11 | 
   12 |             <h1>
   13 |                 Cada gota<br>
   14 |                 e um <em>elo</em><br>
   15 |                 de vida.
   16 |             </h1>
   17 | 
   18 |             <p class="hero-text">
   19 |                 Conectamos doadores, hemocentros e pacientes
   20 |                 em um unico sistema, com inteligencia,
   21 |                 cuidado e a urgencia que salvar vidas exige.
   22 |             </p>
   23 | 
   24 |             <div class="hero-actions">
   25 |                 <a class="button button-primary" href="{% url 'accounts:triagem_apresentacao' %}">
   26 |                     Quero ser doador
   27 |                 </a>
   28 |                 <a class="button button-outline" href="{% url 'accounts:cadastro' %}">
   29 |                     Sou do hemocentro
   30 |                 </a>
   31 |             </div>
   32 |         </div>
   33 |     </div>
   34 | </section>
   35 | 
   36 | <section class="stock-section" id="estoques">
   37 |     <div class="container">
   38 |         <div class="section-heading">
   39 |             <h2>Situacao dos estoques</h2>
   40 |             <p>Sul de Minas</p>
   41 |         </div>
   42 | 
   43 |         <div class="blood-grid">
   44 |             {% for item in estoque_geral %}
   45 |                 <article class="blood-card">
   46 |                     <strong class="blood-type">{{ item.tipo }}</strong>
   47 |                     <span class="blood-line"></span>
   48 |                     <span class="blood-status
   49 |                         {% if item.nivel == 'Critico' %}status-critical
   50 |                         {% elif item.nivel == 'Alerta' or item.nivel == 'Baixo' %}status-alert
   51 |                         {% else %}status-stable{% endif %}">
   52 |                         {{ item.nivel }}
   53 |                     </span>
   54 |                 </article>
   55 |             {% empty %}
   56 |                 <p class="empty-state">Nenhuma informacao de estoque disponivel no momento.</p>
   57 |             {% endfor %}
   58 |         </div>
   59 | 
   60 |         <div class="center-action">
   61 |             <a class="button button-outline button-small" href="{% url 'accounts:estoque_publico' %}">
   62 |                 Ver detalhes por cidade
   63 |             </a>
   64 |         </div>
   65 |     </div>
   66 | </section>
   67 | 
   68 | <section class="info-section" id="como-doar">
   69 |     <div class="container info-grid">
   70 |         <div>
   71 |             <p class="eyebrow">COMO FUNCIONA</p>
   72 |             <h2>Doar sangue e um gesto simples que pode fazer diferenca.</h2>
   73 |         </div>
   74 | 
   75 |         <div class="info-text">
   76 |             <p>
   77 |                 O Elo ajuda voce a encontrar informacoes, consultar estoques
   78 |                 e acompanhar oportunidades de doacao.
   79 |             </p>
   80 |             <a class="text-link" href="{% url 'accounts:triagem_apresentacao' %}">
   81 |                 Conhecer a triagem
   82 |             </a>
   83 |         </div>
   84 |     </div>
   85 | </section>
   86 | 
   87 | <section class="faq-section" id="duvidas">
   88 |     <div class="container">
   89 |         <p class="eyebrow">DUVIDAS</p>
   90 |         <h2>Perguntas frequentes</h2>
   91 | 
   92 |         <div class="faq-grid">
   93 |             <details>
   94 |                 <summary>Onde posso consultar os estoques?</summary>
   95 |                 <p>
   96 |                     A pagina de estoques publicos permite consultar as informacoes
   97 |                     disponibilizadas pelos hemocentros.
   98 |                 </p>
   99 |             </details>
  100 | 
  101 |             <details>
  102 |                 <summary>Como comeco o processo para doar?</summary>
  103 |                 <p>
  104 |                     Acesse a area de triagem para conhecer as etapas iniciais
  105 |                     e verificar como continuar.
  106 |                 </p>
  107 |             </details>
  108 | 
  109 |             <details>
  110 |                 <summary>Hemocentros podem participar do Elo?</summary>
  111 |                 <p>
  112 |                     Sim. O cadastro de Hemocentro passa pelo processo de validacao
  113 |                     administrativa antes do acesso as funcoes institucionais.
  114 |                 </p>
  115 |             </details>
  116 |         </div>
  117 |     </div>
  118 | </section>
  119 | 
  120 | {% endblock %}
``````

## elo_front/templates/base.html

Original: [elo_front/templates/base.html](<C:/Users/lb119/Elo/elo_front/templates/base.html>).

``````text
    1 | {% load static %}
    2 | <!doctype html>
    3 | <html lang="pt-br">
    4 | <head>
    5 |     <meta charset="utf-8">
    6 |     <meta name="viewport" content="width=device-width, initial-scale=1">
    7 |     <meta name="description" content="Elo — sistema de doação de sangue.">
    8 |     <title>{% block title %}Elo{% endblock %}</title>
    9 |     <link rel="stylesheet" href="{% static 'css/elo.css' %}">
   10 | </head>
   11 | 
   12 | <body>
   13 |     <header class="site-header">
   14 |         <div class="header-inner">
   15 |             <a class="brand" href="{% url 'accounts:inicio' %}" aria-label="Elo - página inicial">
   16 |                 <span class="brand-mark" aria-hidden="true"></span>
   17 |                 <span class="brand-name">elo</span>
   18 |             </a>
   19 | 
   20 |             <button class="menu-toggle" type="button" aria-label="Abrir menu" aria-expanded="false">
   21 |                 <span></span><span></span><span></span>
   22 |             </button>
   23 | 
   24 |             <nav class="main-nav" aria-label="Navegação principal">
   25 |                 <a href="{% url 'accounts:inicio' %}#sobre">Sobre o elo</a>
   26 |                 <a href="{% url 'accounts:inicio' %}#como-doar">Como doar</a>
   27 |                 <a href="{% url 'accounts:estoque_publico' %}">Hemocentro</a>
   28 |                 <a href="{% url 'accounts:inicio' %}#duvidas">Dúvidas</a>
   29 |                 <a class="nav-cta" href="{% url 'accounts:cadastro' %}">Sou hemocentro</a>
   30 |             </nav>
   31 |         </div>
   32 |     </header>
   33 | 
   34 |     {% if messages %}
   35 |         <div class="messages-wrap">
   36 |             {% for message in messages %}
   37 |                 <div class="message message-{{ message.tags|default:'info' }}">
   38 |                     {{ message }}
   39 |                 </div>
   40 |             {% endfor %}
   41 |         </div>
   42 |     {% endif %}
   43 | 
   44 |     <main>
   45 |         {% block content %}{% endblock %}
   46 |     </main>
   47 | 
   48 |     <footer class="site-footer">
   49 |         <div class="footer-inner">
   50 |             <a class="brand brand-footer" href="{% url 'accounts:inicio' %}">
   51 |                 <span class="brand-mark" aria-hidden="true"></span>
   52 |                 <span class="brand-name">elo</span>
   53 |             </a>
   54 |             <p>Conectando pessoas, hemocentros e vidas.</p>
   55 |             <div class="footer-links">
   56 |                 <a href="{% url 'accounts:inicio' %}#sobre">Sobre o elo</a>
   57 |                 <a href="{% url 'accounts:triagem_apresentacao' %}">Como doar</a>
   58 |                 <a href="{% url 'accounts:estoque_publico' %}">Estoques</a>
   59 |                 {% if user.is_authenticated %}
   60 |                     <a href="{% url 'accounts:dashboard' %}">Meu painel</a>
   61 |                 {% else %}
   62 |                     <a href="{% url 'accounts:login' %}">Entrar</a>
   63 |                 {% endif %}
   64 |             </div>
   65 |         </div>
   66 |     </footer>
   67 | 
   68 |     <script>
   69 |         const menuToggle = document.querySelector(".menu-toggle");
   70 |         const mainNav = document.querySelector(".main-nav");
   71 | 
   72 |         if (menuToggle && mainNav) {
   73 |             menuToggle.addEventListener("click", () => {
   74 |                 const opened = mainNav.classList.toggle("is-open");
   75 |                 menuToggle.setAttribute("aria-expanded", opened ? "true" : "false");
   76 |             });
   77 |         }
   78 |     </script>
   79 | </body>
   80 | </html>
``````

## manage.py

Original: [manage.py](<C:/Users/lb119/Elo/manage.py>).

``````text
    1 | #!/usr/bin/env python
    2 | """
    3 | RESUMO DO ARQUIVO
    4 | =================
    5 | Ponto de entrada dos comandos administrativos executados no terminal.
    6 | 
    7 | Exemplos: ``runserver``, ``check``, ``makemigrations``, ``migrate``, ``test`` e
    8 | ``createsuperuser``. Normalmente este arquivo nao precisa ser alterado.
    9 | """
   10 | 
   11 | import os
   12 | import sys
   13 | 
   14 | 
   15 | def main():
   16 |     """Configura o projeto e entrega o comando ao Django."""
   17 | 
   18 |     # Indica que config/settings.py contem as configuracoes deste projeto.
   19 |     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
   20 | 
   21 |     try:
   22 |         # A importacao acontece aqui para gerar uma mensagem mais clara quando
   23 |         # Django nao foi instalado ou o ambiente virtual nao esta ativo.
   24 |         from django.core.management import execute_from_command_line
   25 |     except ImportError as exc:
   26 |         raise ImportError(
   27 |             "Nao foi possivel importar o Django. Confirme a instalacao e "
   28 |             "a ativacao do ambiente virtual .venv."
   29 |         ) from exc
   30 | 
   31 |     # sys.argv contem tudo que veio depois de python manage.py.
   32 |     execute_from_command_line(sys.argv)
   33 | 
   34 | 
   35 | # Impede que main execute apenas por este arquivo ser importado em outro modulo.
   36 | if __name__ == "__main__":
   37 |     main()
``````

## requirements.txt

Original: [requirements.txt](<C:/Users/lb119/Elo/requirements.txt>).

``````text
    1 | # RESUMO
    2 | # Cada linha fixa uma dependencia e sua versao. O comando
    3 | # ``python -m pip install -r requirements.txt`` recria o mesmo ambiente.
    4 | 
    5 | # Dependencia interna usada pelo Django para recursos assincronos.
    6 | asgiref==3.12.1
    7 | 
    8 | # Framework principal: rotas, ORM, formularios, autenticacao e admin.
    9 | Django==5.2.17
   10 | 
   11 | # Driver que permite ao Python conversar com PostgreSQL.
   12 | psycopg==3.3.4
   13 | 
   14 | # Componentes compilados do psycopg para facilitar a instalacao no Windows.
   15 | psycopg-binary==3.3.4
   16 | 
   17 | # Le as variaveis privadas do arquivo .env.
   18 | python-dotenv==1.2.2
   19 | 
   20 | # Utilitario usado pelo Django para formatar e separar comandos SQL.
   21 | sqlparse==0.6.0
   22 | 
   23 | # Base de fusos horarios usada no Windows.
   24 | tzdata==2026.3
``````

## templates/accounts/cadastro.html

Original: [templates/accounts/cadastro.html](<C:/Users/lb119/Elo/templates/accounts/cadastro.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% block title %}Criar conta | Elo{% endblock %}
    4 | 
    5 | {% block content %}
    6 | 
    7 | <h1>Criar conta</h1>
    8 | 
    9 | <p>
   10 |     Escolha Doador, Receptor/Solicitante, Observador ou Hemocentro.
   11 | </p>
   12 | 
   13 | <form method="post">
   14 | 
   15 |     {% csrf_token %}
   16 | 
   17 |     {{ form.non_field_errors }}
   18 | 
   19 |     {% for campo in form %}
   20 | 
   21 |         {% if campo.name != "aceite_lgpd" %}
   22 | 
   23 |             <p>
   24 |                 <label for="{{ campo.id_for_label }}">
   25 |                     {{ campo.label }}
   26 |                 </label>
   27 | 
   28 |                 {{ campo }}
   29 | 
   30 |                 {{ campo.errors }}
   31 | 
   32 |                 {% if campo.help_text %}
   33 |                     <small>{{ campo.help_text }}</small>
   34 |                 {% endif %}
   35 |             </p>
   36 | 
   37 |         {% endif %}
   38 | 
   39 |     {% endfor %}
   40 | 
   41 |     <!-- O usuário clica diretamente nas palavras para ler os documentos -->
   42 |     <p>
   43 |         <input
   44 |             type="checkbox"
   45 |             id="{{ form.aceite_lgpd.id_for_label }}"
   46 |             name="{{ form.aceite_lgpd.html_name }}"
   47 |             required
   48 |             {% if form.aceite_lgpd.value %}checked{% endif %}
   49 |         >
   50 | 
   51 |         <label for="{{ form.aceite_lgpd.id_for_label }}">
   52 |             Li e aceito os
   53 | 
   54 |             <a
   55 |                 href="#"
   56 |                 onclick="document.getElementById('modal-termos').showModal(); return false;"
   57 |             >
   58 |                 Termos de Uso
   59 |             </a>
   60 | 
   61 |             e a
   62 | 
   63 |             <a
   64 |                 href="#"
   65 |                 onclick="document.getElementById('modal-privacidade').showModal(); return false;"
   66 |             >
   67 |                 Política de Privacidade
   68 |             </a>.
   69 |         </label>
   70 | 
   71 |         {{ form.aceite_lgpd.errors }}
   72 |     </p>
   73 | 
   74 |     <button type="submit">
   75 |         Criar conta
   76 |     </button>
   77 | 
   78 | </form>
   79 | 
   80 | <!-- Janela dos Termos de Uso. Fica escondida até clicar na palavra. -->
   81 | <dialog id="modal-termos">
   82 | 
   83 |     <h2>Termos de Uso</h2>
   84 | 
   85 |     <p>
   86 |         Ao criar uma conta no Elo, o usuário concorda em utilizar
   87 |         o sistema de maneira correta, legal e respeitosa.
   88 |     </p>
   89 | 
   90 |     <p>
   91 |         O usuário é responsável pelas informações fornecidas no cadastro,
   92 |         pela segurança da sua senha e pelas atividades realizadas em sua conta.
   93 |     </p>
   94 | 
   95 |     <p>
   96 |         O sistema poderá suspender ou encerrar contas que violem as regras
   97 |         de utilização ou a legislação aplicável.
   98 |     </p>
   99 | 
  100 |     <button
  101 |         type="button"
  102 |         onclick="document.getElementById('modal-termos').close();"
  103 |     >
  104 |         Fechar
  105 |     </button>
  106 | 
  107 | </dialog>
  108 | 
  109 | <!-- Janela da Política de Privacidade. Fica escondida até clicar na palavra. -->
  110 | <dialog id="modal-privacidade">
  111 | 
  112 |     <h2>Política de Privacidade</h2>
  113 | 
  114 |     <p>
  115 |         Os dados informados no cadastro poderão ser utilizados para criar,
  116 |         administrar e proteger a conta do usuário.
  117 |     </p>
  118 | 
  119 |     <p>
  120 |         As informações devem ser tratadas de acordo com a legislação aplicável,
  121 |         incluindo a Lei Geral de Proteção de Dados.
  122 |     </p>
  123 | 
  124 |     <p>
  125 |         O usuário poderá solicitar informações sobre o uso dos seus dados
  126 |         pelos canais oficiais do sistema.
  127 |     </p>
  128 | 
  129 |     <button
  130 |         type="button"
  131 |         onclick="document.getElementById('modal-privacidade').close();"
  132 |     >
  133 |         Fechar
  134 |     </button>
  135 | 
  136 | </dialog>
  137 | 
  138 | <p>
  139 |     Já possui cadastro?
  140 |     <a href="{% url 'accounts:login' %}">Entrar</a>
  141 | </p>
  142 | 
  143 | {% endblock %}
``````

## templates/accounts/compatibilidade_sanguinea.html

Original: [templates/accounts/compatibilidade_sanguinea.html](<C:/Users/lb119/Elo/templates/accounts/compatibilidade_sanguinea.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% block title %}Compatibilidade sanguinea | Elo{% endblock %}
    4 | 
    5 | {% block content %}
    6 | <h1>Compatibilidade sanguinea</h1>
    7 | 
    8 | <p>
    9 |     Consulte quais tipos sanguineos podem doar e receber sangue entre si,
   10 |     considerando o sistema ABO e o fator Rh.
   11 | </p>
   12 | 
   13 | <section>
   14 |     <h2>Consultar por tipo</h2>
   15 | 
   16 |     <form method="get">
   17 |         <label for="tipo">Tipo sanguineo</label>
   18 |         <select id="tipo" name="tipo">
   19 |             <option value="">Selecione um tipo</option>
   20 |             {% for tipo in tipos_sanguineos %}
   21 |                 <option value="{{ tipo }}" {% if tipo == tipo_selecionado %}selected{% endif %}>
   22 |                     {{ tipo }}
   23 |                 </option>
   24 |             {% endfor %}
   25 |         </select>
   26 |         <button type="submit">Consultar</button>
   27 |     </form>
   28 | 
   29 |     {% if tipo_invalido %}
   30 |         <p>Tipo sanguineo invalido. Selecione uma das opcoes da tabela.</p>
   31 |     {% endif %}
   32 | 
   33 |     {% if compatibilidade_selecionada %}
   34 |         <h3>Resultado para {{ compatibilidade_selecionada.tipo }}</h3>
   35 |         <p><strong>Pode doar para:</strong> {{ compatibilidade_selecionada.doar_para|join:", " }}</p>
   36 |         <p><strong>Pode receber de:</strong> {{ compatibilidade_selecionada.receber_de|join:", " }}</p>
   37 |     {% endif %}
   38 | </section>
   39 | 
   40 | <section>
   41 |     <h2>Tabela de compatibilidade</h2>
   42 | 
   43 |     <table border="1" cellpadding="12" cellspacing="0" width="100%">
   44 |         <caption>
   45 |             Compatibilidade sanguinea considerando sistema ABO e fator Rh
   46 |         </caption>
   47 | 
   48 |         <thead>
   49 |             <tr>
   50 |                 <th scope="col" width="10%">Tipo</th>
   51 |                 <th scope="col" width="35%">Pode doar para</th>
   52 |                 <th scope="col" width="35%">Pode receber de</th>
   53 |                 <th scope="col" width="20%">Populacao aproximada</th>
   54 |             </tr>
   55 |         </thead>
   56 | 
   57 |         <tbody>
   58 |             {% for item in tabela_compatibilidade %}
   59 |                 <tr>
   60 |                     <th scope="row">{{ item.tipo }}</th>
   61 |                     <td>{{ item.doar_para|join:", " }}</td>
   62 |                     <td>{{ item.receber_de|join:", " }}</td>
   63 |                     <td>{{ item.populacao }}</td>
   64 |                 </tr>
   65 |             {% endfor %}
   66 |         </tbody>
   67 |     </table>
   68 | </section>
   69 | 
   70 | <section>
   71 |     <h2>Informacoes importantes</h2>
   72 |     <ul>
   73 |         <li>O tipo O- pode doar hemacias para todos os tipos sanguineos.</li>
   74 |         <li>O tipo AB+ pode receber hemacias de todos os tipos sanguineos.</li>
   75 |         <li>Enquanto a triagem nao estiver implementada, esta tela e apenas informativa.</li>
   76 |         <li>A compatibilidade real deve sempre ser confirmada por profissionais de saude e exames laboratoriais.</li>
   77 |     </ul>
   78 | </section>
   79 | {% endblock %}
``````

## templates/accounts/dashboard.html

Original: [templates/accounts/dashboard.html](<C:/Users/lb119/Elo/templates/accounts/dashboard.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% comment %}
    4 | RESUMO DO ARQUIVO
    5 | =================
    6 | Painel protegido do usuario cadastrado.
    7 | 
    8 | A view envia dois dicionarios principais:
    9 | - painel: textos gerais do perfil logado;
   10 | - visibilidade: regras que dizem quais blocos cada usuario pode enxergar.
   11 | 
   12 | Assim, a particularizacao fica centralizada na view e o template apenas mostra
   13 | ou esconde as secoes correspondentes.
   14 | {% endcomment %}
   15 | 
   16 | {% block title %}Painel | Elo{% endblock %}
   17 | 
   18 | {% block content %}
   19 | 
   20 | <!-- get_short_name retorna o primeiro nome ou, se vazio, o e-mail. -->
   21 | <h1>Ola, {{ user.get_short_name }}!</h1>
   22 | 
   23 | <p>
   24 |     <strong>{{ painel.rotulo }}</strong>
   25 | </p>
   26 | 
   27 | {% if preferencia_convocacao %}
   28 |     <section>
   29 |         <h2>Alertas de doação</h2>
   30 |         <p>Receba até {{ convocacao_limite }} alerta(s) a cada {{ convocacao_intervalo_horas }} horas,
   31 |             quando houver compatibilidade e sua última triagem concluída permitir.</p>
   32 |         <form method="post">
   33 |             {% csrf_token %}
   34 |             {{ preferencia_convocacao.as_p }}
   35 |             <button type="submit">Salvar preferência</button>
   36 |         </form>
   37 |     </section>
   38 | {% endif %}
   39 | 
   40 |     <section id="notificacoes">
   41 |         <h2>Notificações</h2>
   42 |         <p>{{ notificacoes_nao_lidas }} não lida(s).</p>
   43 | 
   44 |         <ul>
   45 |             {% for notificacao in notificacoes_dashboard %}
   46 |                 <li>
   47 |                     <strong>{{ notificacao.titulo }}</strong><br>
   48 |                     <span>{{ notificacao.get_tipo_display }} · {{ notificacao.criada_em|date:"d/m/Y H:i" }}</span><br>
   49 |                     <span>{% if notificacao.lida %}Lida{% else %}Não lida{% endif %}</span><br>
   50 |                     {{ notificacao.mensagem }}
   51 | 
   52 |                     {% if notificacao.url_destino %}
   53 |                         <br>
   54 |                         <a href="{{ notificacao.url_destino }}">
   55 |                             {% if notificacao.tipo == "ESTOQUE_CRITICO" or notificacao.tipo == "ESTOQUE_BAIXO" %}Ver estoque{% elif notificacao.tipo == "PEDIDO_COMPATIVEL" %}Ver pedido{% else %}Ver detalhes{% endif %}
   56 |                         </a>
   57 |                     {% endif %}
   58 |                     {% if not notificacao.lida %}
   59 |                         <form method="post">
   60 |                             {% csrf_token %}
   61 |                             <input type="hidden" name="acao" value="marcar_notificacao_lida">
   62 |                             <input type="hidden" name="id_notificacao" value="{{ notificacao.pk }}">
   63 |                             <button type="submit">Marcar como lida</button>
   64 |                         </form>
   65 |                     {% endif %}
   66 |                 </li>
   67 |             {% empty %}
   68 |                 <li>Você ainda não tem notificações.</li>
   69 |             {% endfor %}
   70 |         </ul>
   71 |         {% if notificacoes_dashboard.has_other_pages %}
   72 |             <nav aria-label="Páginas de notificações">
   73 |                 {% if notificacoes_dashboard.has_previous %}
   74 |                     <a href="?pagina_notificacoes={{ notificacoes_dashboard.previous_page_number }}#notificacoes">Anterior</a>
   75 |                 {% endif %}
   76 |                 <span>Página {{ notificacoes_dashboard.number }} de {{ notificacoes_dashboard.paginator.num_pages }}</span>
   77 |                 {% if notificacoes_dashboard.has_next %}
   78 |                     <a href="?pagina_notificacoes={{ notificacoes_dashboard.next_page_number }}#notificacoes">Próxima</a>
   79 |                 {% endif %}
   80 |             </nav>
   81 |         {% endif %}
   82 |     </section>
   83 | 
   84 | <section>
   85 |     <h2>{{ painel.titulo }}</h2>
   86 |     <p>{{ painel.descricao }}</p>
   87 | 
   88 |     <ul>
   89 |         {% for acao in painel.acoes %}
   90 |             <li>{{ acao }}</li>
   91 |         {% endfor %}
   92 |     </ul>
   93 | </section>
   94 | 
   95 | 
   96 | {% comment %}
   97 | =================================================================
   98 | TRIAGEM
   99 | =================================================================
  100 | Doador e Receptor/Solicitante podem acessar a triagem. Outros perfis nao
  101 | devem ver esse bloco no dashboard.
  102 | {% endcomment %}
  103 | 
  104 | {% if visibilidade.mostra_triagem %}
  105 | 
  106 |     <section>
  107 |         <h2>Triagem para doação</h2>
  108 | 
  109 |         {% if user.perfil == "DOADOR" %}
  110 | 
  111 |             <p>
  112 |                 Responda à triagem inicial antes de procurar um posto de coleta.
  113 |             </p>
  114 | 
  115 |         {% elif user.perfil == "RECEPTOR" %}
  116 | 
  117 |             <p>
  118 |                 Mesmo sendo Receptor, você pode responder à triagem
  119 |                 caso também queira doar sangue.
  120 |             </p>
  121 | 
  122 |         {% endif %}
  123 | 
  124 |         <p>
  125 |             <a href="{% url 'accounts:triagem_apresentacao' %}">
  126 |                 Escolher ou continuar uma triagem
  127 |             </a>
  128 |         </p>
  129 | 
  130 |         <p>
  131 |             <a href="{% url 'accounts:triagem_historico' %}">
  132 |                 Ver meu histórico de triagens
  133 |             </a>
  134 |         </p>
  135 | 
  136 |         {% if ultima_triagem %}
  137 |             <p>
  138 |                 <strong>Última triagem:</strong>
  139 |                 {{ ultima_triagem.get_modalidade_display }} -
  140 |                 {{ ultima_triagem.get_status_display }}
  141 |             </p>
  142 |         {% endif %}
  143 |     </section>
  144 | 
  145 | {% endif %}
  146 | 
  147 | 
  148 | {% comment %}
  149 | =================================================================
  150 | CAMPANHAS
  151 | =================================================================
  152 | Doador e Observador veem campanhas publicas. Hemocentro pendente nao publica
  153 | campanha; Hemocentro aprovado pode ganhar uma tela propria futuramente.
  154 | {% endcomment %}
  155 | 
  156 | {% if visibilidade.mostra_campanhas %}
  157 | 
  158 |     <section>
  159 |         <h2>Campanhas e mutiroes</h2>
  160 | 
  161 |         <ul>
  162 |             {% for campanha in campanhas_ativas %}
  163 |                 <li>
  164 |                     <strong>{{ campanha.titulo }}</strong><br>
  165 |                     {{ campanha.cidade }} - {{ campanha.data }}
  166 |                 </li>
  167 |             {% empty %}
  168 |                 <li>Nenhuma campanha ativa no momento.</li>
  169 |             {% endfor %}
  170 |         </ul>
  171 |     </section>
  172 | 
  173 | {% endif %}
  174 | 
  175 | 
  176 | {% comment %}
  177 | =================================================================
  178 | ESTOQUE PUBLICO
  179 | =================================================================
  180 | Doador, Receptor e Observador podem consultar a situacao publica dos estoques.
  181 | Gerenciar estoque e diferente de consultar estoque publico.
  182 | {% endcomment %}
  183 | 
  184 | {% if visibilidade.mostra_estoque_publico %}
  185 | 
  186 |     <section>
  187 |         <h2>Estoque público</h2>
  188 | 
  189 |         <p>
  190 |             Consulte os estoques informados pelos Hemocentros aprovados.
  191 |         </p>
  192 | 
  193 |         <p>
  194 |             <a href="{% url 'accounts:estoque_publico' %}">
  195 |                 Ver estoque público completo
  196 |             </a>
  197 |         </p>
  198 | 
  199 |         <table>
  200 |             <thead>
  201 |                 <tr>
  202 |                     <th>Tipo sanguineo</th>
  203 |                     <th>Nivel</th>
  204 |                     <th>Ocupacao</th>
  205 |                 </tr>
  206 |             </thead>
  207 | 
  208 |             <tbody>
  209 |                 {% for item in estoque_geral %}
  210 |                     <tr>
  211 |                         <td>{{ item.tipo }}</td>
  212 |                         <td>{{ item.nivel }}</td>
  213 |                         <td>{{ item.percentual }}%</td>
  214 |                     </tr>
  215 |                 {% empty %}
  216 |                     <tr>
  217 |                         <td colspan="3">
  218 |                             Nenhum dado de estoque disponivel.
  219 |                         </td>
  220 |                     </tr>
  221 |                 {% endfor %}
  222 |             </tbody>
  223 |         </table>
  224 |     </section>
  225 | 
  226 | {% endif %}
  227 | 
  228 | 
  229 | {% comment %}
  230 | =================================================================
  231 | PEDIDOS
  232 | =================================================================
  233 | Doador, Receptor, Observador e Hemocentro podem ver pedidos ativos. O
  234 | Administrador nao precisa receber essa lista no painel administrativo.
  235 | {% endcomment %}
  236 | 
  237 | {% if visibilidade.mostra_pedidos %}
  238 | 
  239 |     <section>
  240 |         <h2>Pedidos ativos</h2>
  241 |         <p><a href="{% url 'accounts:consultar_pedidos' %}">Consultar pedidos ativos</a></p>
  242 | 
  243 |         {% if visibilidade.pode_solicitar_divulgacao %}
  244 |             <p>
  245 |                 <a href="{% url 'accounts:pedido_publicar' %}">
  246 |                     Solicitar divulgação de necessidade
  247 |                 </a>
  248 |             </p>
  249 |             <p>
  250 |                 <a href="{% url 'accounts:minhas_solicitacoes' %}">
  251 |                     Acompanhar minhas solicitações
  252 |                 </a>
  253 |             </p>
  254 |         {% endif %}
  255 | 
  256 |         <ul>
  257 |             {% for pedido in pedidos_ativos %}
  258 |                 <li>
  259 |                     <strong>{{ pedido.titulo }}</strong><br>
  260 |                     {{ pedido.tipo_sanguineo }} -
  261 |                     {{ pedido.cidade }} -
  262 |                     Urgencia {{ pedido.urgencia }}
  263 |                 </li>
  264 |             {% empty %}
  265 |                 <li>Nenhum pedido ativo no momento.</li>
  266 |             {% endfor %}
  267 |         </ul>
  268 |     </section>
  269 | 
  270 | {% endif %}
  271 | 
  272 | {% if visibilidade.pode_analisar_pedidos %}
  273 |     <section>
  274 |         <h2>Análise de solicitações</h2>
  275 |         <p>Somente o Hemocentro aprovado pode decidir pela publicação.</p>
  276 |         <p>
  277 |             <a href="{% url 'accounts:painel_pedidos_hemocentro' %}">
  278 |                 Analisar solicitações recebidas
  279 |             </a>
  280 |         </p>
  281 |     </section>
  282 | {% endif %}
  283 | 
  284 | 
  285 | {% comment %}
  286 | =================================================================
  287 | POSTOS DE COLETA
  288 | =================================================================
  289 | Doador e Observador recebem a lista de postos no dashboard. Outros perfis
  290 | podem acessar informacoes publicas pela pagina inicial quando necessario.
  291 | {% endcomment %}
  292 | 
  293 | {% if visibilidade.mostra_postos %}
  294 | 
  295 |     <section>
  296 |         <h2>Postos de coleta</h2>
  297 | 
  298 |         <ul>
  299 |             {% for posto in postos %}
  300 |                 <li>
  301 |                     <strong>{{ posto.nome }}</strong><br>
  302 |                     {{ posto.cidade }}/{{ posto.estado }} -
  303 |                     {{ posto.horario }}
  304 |                 </li>
  305 |             {% empty %}
  306 |                 <li>Nenhum posto de coleta cadastrado.</li>
  307 |             {% endfor %}
  308 |         </ul>
  309 |     </section>
  310 | 
  311 | {% endif %}
  312 | 
  313 | 
  314 | {% comment %}
  315 | =================================================================
  316 | STATUS DA VALIDACAO DO HEMOCENTRO
  317 | =================================================================
  318 | Mostra para o Hemocentro a situacao atual do cadastro institucional.
  319 | Somente Hemocentro aprovado recebe o link para gerenciar estoque.
  320 | {% endcomment %}
  321 | 
  322 | {% if visibilidade.mostra_status_hemocentro %}
  323 | 
  324 |     <section>
  325 | 
  326 |         <h2>Status da validação institucional</h2>
  327 | 
  328 |         {% if request.user.status_validacao == "PENDENTE" %}
  329 | 
  330 |             <h3>Pendente</h3>
  331 | 
  332 |             <p>
  333 |                 Seu cadastro de Hemocentro está aguardando análise
  334 |                 de um administrador.
  335 |             </p>
  336 | 
  337 |             <p>
  338 |                 Enquanto a análise não for concluída, a publicação
  339 |                 de estoques e campanhas permanece bloqueada.
  340 |             </p>
  341 | 
  342 |         {% elif request.user.status_validacao == "APROVADO" %}
  343 | 
  344 |             <h3>Aprovado</h3>
  345 | 
  346 |             <p>
  347 |                 Seu Hemocentro foi aprovado pelo administrador.
  348 |             </p>
  349 | 
  350 |             <p>
  351 |                 O Hemocentro está autorizado a cadastrar e atualizar estoques.
  352 |             </p>
  353 | 
  354 |             {% if visibilidade.pode_gerenciar_estoque %}
  355 |                 <p>
  356 |                     <a href="{% url 'accounts:estoque_hemocentro' %}">
  357 |                         Cadastrar e atualizar estoque
  358 |                     </a>
  359 |                 </p>
  360 |             {% endif %}
  361 | 
  362 |         {% elif request.user.status_validacao == "RECUSADO" %}
  363 | 
  364 |             <h3>Cadastro recusado</h3>
  365 | 
  366 |             <p>
  367 |                 O cadastro do Hemocentro foi recusado.
  368 |             </p>
  369 | 
  370 |             {% if validacao_atual and validacao_atual.parecer %}
  371 | 
  372 |                 <p>
  373 |                     <strong>Parecer do administrador:</strong>
  374 |                     {{ validacao_atual.parecer }}
  375 |                 </p>
  376 | 
  377 |                 <p>
  378 |                     <strong>Data da análise:</strong>
  379 |                     {{ validacao_atual.data_analise|date:"d/m/Y H:i" }}
  380 |                 </p>
  381 | 
  382 |             {% endif %}
  383 | 
  384 |         {% elif request.user.status_validacao == "CORRECAO" %}
  385 | 
  386 |             <h3>Correção necessária</h3>
  387 | 
  388 |             <p>
  389 |                 O administrador solicitou alterações no cadastro
  390 |                 do Hemocentro.
  391 |             </p>
  392 | 
  393 |             {% if validacao_atual and validacao_atual.parecer %}
  394 | 
  395 |                 <p>
  396 |                     <strong>Orientação do administrador:</strong>
  397 |                     {{ validacao_atual.parecer }}
  398 |                 </p>
  399 | 
  400 |                 <p>
  401 |                     <strong>Data da análise:</strong>
  402 |                     {{ validacao_atual.data_analise|date:"d/m/Y H:i" }}
  403 |                 </p>
  404 | 
  405 |             {% endif %}
  406 | 
  407 |         {% endif %}
  408 | 
  409 |     </section>
  410 | 
  411 | {% endif %}
  412 | 
  413 | 
  414 | {% comment %}
  415 | =================================================================
  416 | ACESSO DO ADMINISTRADOR
  417 | =================================================================
  418 | Mostra o link para a tela de aprovação quando o usuário é administrador.
  419 | Administrador nao e tratado como Hemocentro.
  420 | {% endcomment %}
  421 | 
  422 | {% if visibilidade.pode_aprovar_hemocentros %}
  423 |     <section>
  424 |         <h2>Validação de Hemocentros</h2>
  425 | 
  426 |         <p>
  427 |             Analise cadastros pendentes e libere o acesso institucional
  428 |             somente depois da aprovação.
  429 |         </p>
  430 | 
  431 |         <p>
  432 |             <a href="{% url 'accounts:painel_aprovacao_hemocentros' %}">
  433 |                 Acessar aprovação de Hemocentros
  434 |             </a>
  435 |         </p>
  436 |     </section>
  437 | {% endif %}
  438 | 
  439 | {% if visibilidade.pode_moderar_pedidos %}
  440 |     <section>
  441 |         <h2>Moderação de pedidos</h2>
  442 |         <p>Analise pedidos suspeitos ou pendentes sem publicar em nome do Hemocentro.</p>
  443 |         <p><a href="{% url 'accounts:painel_validacao_pedidos' %}">Acessar moderação de pedidos</a></p>
  444 |     </section>
  445 | {% endif %}
  446 | {% endblock %}
``````

## templates/accounts/estoque_hemocentro.html

Original: [templates/accounts/estoque_hemocentro.html](<C:/Users/lb119/Elo/templates/accounts/estoque_hemocentro.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% block title %}Meu Estoque | Elo{% endblock %}
    4 | 
    5 | {% block content %}
    6 | 
    7 | <section class="estoque-hemocentro">
    8 | 
    9 |     <h1>Meu Estoque</h1>
   10 | 
   11 |     <p>
   12 |         Gerencie a quantidade de bolsas disponíveis por tipo sanguíneo.
   13 |     </p>
   14 | 
   15 |     <section>
   16 |         <h2>Estoques cadastrados</h2>
   17 | 
   18 |         {% if estoques %}
   19 | 
   20 |             <div class="estoques-grid">
   21 | 
   22 |                 {% for estoque in estoques %}
   23 | 
   24 |                     <article class="estoque-card">
   25 | 
   26 |                         <h3>{{ estoque.tipo_sanguineo }}</h3>
   27 | 
   28 |                         <p>
   29 |                             <strong>Quantidade:</strong>
   30 |                             {{ estoque.quantidade_bolsas }} bolsas
   31 |                         </p>
   32 | 
   33 |                         <p>
   34 |                             <strong>Status:</strong>
   35 |                             {{ estoque.get_status_calculado_display }}
   36 |                         </p>
   37 | 
   38 |                         <p>
   39 |                             <strong>Última atualização:</strong>
   40 |                             {{ estoque.data_atualizacao|date:"d/m/Y H:i" }}
   41 |                         </p>
   42 | 
   43 |                         <p>
   44 |                             <strong>Nível mínimo:</strong>
   45 |                             {{ estoque.nivel_minimo }} bolsas
   46 |                             <br>
   47 |                             <strong>Nível crítico:</strong>
   48 |                             {{ estoque.nivel_critico }} bolsas
   49 |                         </p>
   50 | 
   51 | 
   52 |                         <h4>Atualizar estoque</h4>
   53 | 
   54 |                         <form
   55 |                             method="post"
   56 |                             action="{% url 'accounts:atualizar_estoque' estoque.id_estoque %}"
   57 |                         >
   58 |                             {% csrf_token %}
   59 | 
   60 |                             <div>
   61 |                                 {{ form_movimentacao.tipo_movimento.label_tag }}
   62 |                                 {{ form_movimentacao.tipo_movimento }}
   63 |                             </div>
   64 | 
   65 |                             <div>
   66 |                                 {{ form_movimentacao.quantidade.label_tag }}
   67 |                                 {{ form_movimentacao.quantidade }}
   68 | 
   69 |                                 {% if form_movimentacao.quantidade.help_text %}
   70 |                                     <small>
   71 |                                         {{ form_movimentacao.quantidade.help_text }}
   72 |                                     </small>
   73 |                                 {% endif %}
   74 |                             </div>
   75 | 
   76 |                             <div>
   77 |                                 {{ form_movimentacao.motivo.label_tag }}
   78 |                                 {{ form_movimentacao.motivo }}
   79 |                                 {% if form_movimentacao.motivo.help_text %}
   80 |                                     <small>
   81 |                                         {{ form_movimentacao.motivo.help_text }}
   82 |                                     </small>
   83 |                                 {% endif %}
   84 |                             </div>
   85 | 
   86 |                             <button type="submit">
   87 |                                 Atualizar estoque
   88 |                             </button>
   89 |                         </form>
   90 | 
   91 |                         <h4>Histórico de movimentações</h4>
   92 | 
   93 |                         {% with movimentacoes=estoque.movimentacoes.all %}
   94 |                             {% if movimentacoes %}
   95 |                                 <table>
   96 |                                     <thead>
   97 |                                         <tr>
   98 |                                             <th>Data</th>
   99 |                                             <th>Movimentação</th>
  100 |                                             <th>Anterior</th>
  101 |                                             <th>Nova</th>
  102 |                                             <th>Responsável</th>
  103 |                                             <th>Motivo</th>
  104 |                                         </tr>
  105 |                                     </thead>
  106 |                                     <tbody>
  107 |                                         {% for movimentacao in movimentacoes %}
  108 |                                             <tr>
  109 |                                                 <td>
  110 |                                                     {{ movimentacao.data_hora|date:"d/m/Y H:i" }}
  111 |                                                 </td>
  112 |                                                 <td>
  113 |                                                     {{ movimentacao.get_tipo_movimento_display }}
  114 |                                                 </td>
  115 |                                                 <td>{{ movimentacao.quantidade_anterior }}</td>
  116 |                                                 <td>{{ movimentacao.quantidade_nova }}</td>
  117 |                                                 <td>
  118 |                                                     {% if movimentacao.usuario_resp %}
  119 |                                                         {{ movimentacao.usuario_resp.nome }}
  120 |                                                     {% else %}
  121 |                                                         Usuário removido
  122 |                                                     {% endif %}
  123 |                                                 </td>
  124 |                                                 <td>{{ movimentacao.motivo }}</td>
  125 |                                             </tr>
  126 |                                         {% endfor %}
  127 |                                     </tbody>
  128 |                                 </table>
  129 |                             {% else %}
  130 |                                 <p>Nenhuma movimentação registrada.</p>
  131 |                             {% endif %}
  132 |                         {% endwith %}
  133 | 
  134 |                     </article>
  135 | 
  136 |                 {% endfor %}
  137 | 
  138 |             </div>
  139 | 
  140 |         {% else %}
  141 | 
  142 |             <p>
  143 |                 Nenhum estoque foi cadastrado ainda.
  144 |             </p>
  145 | 
  146 |         {% endif %}
  147 |     </section>
  148 | 
  149 | 
  150 |     {% if tipos_disponiveis %}
  151 | 
  152 |         <section>
  153 |             <h2>Cadastrar novo estoque</h2>
  154 | 
  155 |             <p>
  156 |                 Cadastre os tipos sanguíneos que ainda não possuem estoque.
  157 |             </p>
  158 | 
  159 |             <form
  160 |                 method="post"
  161 |                 action="{% url 'accounts:cadastrar_estoque' %}"
  162 |             >
  163 |                 {% csrf_token %}
  164 | 
  165 |                 <div>
  166 |                     {{ form_cadastro.tipo_sanguineo.label_tag }}
  167 |                     {{ form_cadastro.tipo_sanguineo }}
  168 |                 </div>
  169 | 
  170 |                 <div>
  171 |                     {{ form_cadastro.quantidade_bolsas.label_tag }}
  172 |                     {{ form_cadastro.quantidade_bolsas }}
  173 | 
  174 |                     {% if form_cadastro.quantidade_bolsas.help_text %}
  175 |                         <small>
  176 |                             {{ form_cadastro.quantidade_bolsas.help_text }}
  177 |                         </small>
  178 |                     {% endif %}
  179 |                 </div>
  180 | 
  181 |                 <div>
  182 |                     {{ form_cadastro.nivel_minimo.label_tag }}
  183 |                     {{ form_cadastro.nivel_minimo }}
  184 | 
  185 |                     {% if form_cadastro.nivel_minimo.help_text %}
  186 |                         <small>
  187 |                             {{ form_cadastro.nivel_minimo.help_text }}
  188 |                         </small>
  189 |                     {% endif %}
  190 |                 </div>
  191 | 
  192 |                 <div>
  193 |                     {{ form_cadastro.nivel_critico.label_tag }}
  194 |                     {{ form_cadastro.nivel_critico }}
  195 | 
  196 |                     {% if form_cadastro.nivel_critico.help_text %}
  197 |                         <small>
  198 |                             {{ form_cadastro.nivel_critico.help_text }}
  199 |                         </small>
  200 |                     {% endif %}
  201 |                 </div>
  202 | 
  203 |                 <button type="submit">
  204 |                     Cadastrar estoque
  205 |                 </button>
  206 |             </form>
  207 |         </section>
  208 | 
  209 |     {% endif %}
  210 | 
  211 | </section>
  212 | 
  213 | {% endblock %}
``````

## templates/accounts/estoque_publico.html

Original: [templates/accounts/estoque_publico.html](<C:/Users/lb119/Elo/templates/accounts/estoque_publico.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% comment %}
    4 | RF 32 - Visualização pública de estoques
    5 | 
    6 | Esta página pode ser acessada por visitantes e usuários autenticados.
    7 | 
    8 | São exibidos somente dados públicos:
    9 | - Nome do Hemocentro
   10 | - Cidade e estado
   11 | - Tipo sanguíneo
   12 | - Quantidade de bolsas
   13 | - Situação do estoque
   14 | - Última atualização
   15 | 
   16 | Não são exibidos dados internos, como:
   17 | - CPF
   18 | - CNPJ
   19 | - E-mail
   20 | - Responsável pelas movimentações
   21 | - Histórico
   22 | - Nível mínimo
   23 | - Nível crítico
   24 | - Auditorias
   25 | {% endcomment %}
   26 | 
   27 | {% block title %}Estoques de Sangue | Elo{% endblock %}
   28 | 
   29 | {% block content %}
   30 | 
   31 | <h1>Estoques de Sangue</h1>
   32 | 
   33 | <p>
   34 |     Consulte a situação dos estoques disponíveis nos Hemocentros cadastrados e aprovados no Elo.
   35 | </p>
   36 | 
   37 | <form method="get">
   38 |     {{ form.as_p }}
   39 | 
   40 |     <button type="submit">
   41 |         Filtrar estoque
   42 |     </button>
   43 | 
   44 |     <a href="{% url 'accounts:estoque_publico' %}">
   45 |         Limpar filtros
   46 |     </a>
   47 | </form>
   48 | 
   49 | <section>
   50 |     <h2>Indicadores</h2>
   51 | 
   52 |     <ul>
   53 |         <li>
   54 |             <strong>Crítico</strong> - estoque em situação crítica.
   55 |         </li>
   56 | 
   57 |         <li>
   58 |             <strong>Baixo</strong> - estoque abaixo do nível esperado.
   59 |         </li>
   60 | 
   61 |         <li>
   62 |             <strong>Adequado</strong> - estoque dentro da faixa esperada.
   63 |         </li>
   64 | 
   65 |         <li>
   66 |             <strong>Alto</strong> - estoque acima da faixa adequada.
   67 |         </li>
   68 |     </ul>
   69 | </section>
   70 | 
   71 | <section>
   72 |     <h2>Estoques por Hemocentro</h2>
   73 | 
   74 |     {% if estoques %}
   75 | 
   76 |         {% regroup estoques by nome as hemocentros %}
   77 | 
   78 |         {% for hemocentro in hemocentros %}
   79 | 
   80 |             <article>
   81 |                 <h3>{{ hemocentro.grouper }}</h3>
   82 | 
   83 |                 <table>
   84 |                     <thead>
   85 |                         <tr>
   86 |                             <th>Tipo sanguíneo</th>
   87 |                             <th>Quantidade</th>
   88 |                             <th>Situação</th>
   89 |                             <th>Última atualização</th>
   90 |                         </tr>
   91 |                     </thead>
   92 | 
   93 |                     <tbody>
   94 |                         {% for item in hemocentro.list %}
   95 |                             <tr>
   96 |                                 <td>
   97 |                                     <strong>
   98 |                                         {{ item.tipo_sanguineo }}
   99 |                                     </strong>
  100 |                                 </td>
  101 | 
  102 |                                 <td>
  103 |                                     {{ item.quantidade_bolsas }} bolsas
  104 |                                 </td>
  105 | 
  106 |                                 <td>
  107 |                                     {{ item.status_label }}
  108 |                                 </td>
  109 | 
  110 |                                 <td>
  111 |                                     {{ item.data_atualizacao|date:"d/m/Y H:i" }}
  112 |                                 </td>
  113 |                             </tr>
  114 |                         {% endfor %}
  115 |                     </tbody>
  116 |                 </table>
  117 | 
  118 |                 <p>
  119 |                     <strong>Localização:</strong>
  120 |                     {{ hemocentro.list.0.cidade }}/{{ hemocentro.list.0.estado }}
  121 |                 </p>
  122 |             </article>
  123 | 
  124 |             <hr>
  125 | 
  126 |         {% endfor %}
  127 | 
  128 |     {% else %}
  129 | 
  130 |         <p>
  131 |             Nenhum estoque público disponível no momento.
  132 |         </p>
  133 | 
  134 |     {% endif %}
  135 | </section>
  136 | 
  137 | <section>
  138 |     <p>
  139 |         <strong>Importante:</strong>
  140 |         os dados apresentados têm finalidade informativa.
  141 |         A disponibilidade real das bolsas deve ser confirmada diretamente
  142 |         com o Hemocentro.
  143 |     </p>
  144 | </section>
  145 | 
  146 | {% endblock %}
``````

## templates/accounts/inicio.html

Original: [templates/accounts/inicio.html](<C:/Users/lb119/Elo/templates/accounts/inicio.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% comment %}
    4 | RESUMO DO ARQUIVO
    5 | =================
    6 | Tela publica do ator Visitante. Ela permite pesquisar postos de coleta,
    7 | consultar estoque geral e ver pedidos ativos sem exigir cadastro ou login.
    8 | {% endcomment %}
    9 | 
   10 | {% block title %}Acesso visitante | Elo{% endblock %}
   11 | 
   12 | {% block content %}
   13 | <h1>Acesso visitante</h1>
   14 | <p>Pesquise postos de coleta, consulte o estoque geral e acompanhe pedidos ativos.</p>
   15 | 
   16 | <section>
   17 |     <h2>Triagem para doação</h2>
   18 | 
   19 |     <p>
   20 |         Quer saber como funciona a orientação inicial para doação de sangue?
   21 |     </p>
   22 | 
   23 |     <p>
   24 |         <a href="{% url 'accounts:triagem_apresentacao' %}">
   25 |             Conhecer a triagem
   26 |         </a>
   27 |     </p>
   28 | </section>
   29 | 
   30 | <section>
   31 |     <h2>Postos de coleta</h2>
   32 | 
   33 |     <form method="get">
   34 |         <label for="q">Pesquisar por posto, cidade, UF ou endereco</label>
   35 |         <input
   36 |             type="search"
   37 |             id="q"
   38 |             name="q"
   39 |             value="{{ consulta }}"
   40 |             placeholder="Ex.: Campinas, SP ou Hemocentro"
   41 |         >
   42 |         <button type="submit">Pesquisar</button>
   43 |     </form>
   44 | 
   45 |     {% if postos %}
   46 |         <ul>
   47 |             {% for posto in postos %}
   48 |                 <li>
   49 |                     <strong>{{ posto.nome }}</strong><br>
   50 |                     {{ posto.endereco }} - {{ posto.cidade }}/{{ posto.estado }}<br>
   51 |                     {{ posto.horario }}
   52 |                 </li>
   53 |             {% endfor %}
   54 |         </ul>
   55 |     {% else %}
   56 |         <p>Nenhum posto encontrado para "{{ consulta }}".</p>
   57 |     {% endif %}
   58 | </section>
   59 | 
   60 | <section>
   61 |     <h2>Estoque geral</h2>
   62 | 
   63 |     <table>
   64 |         <thead>
   65 |             <tr>
   66 |                 <th>Tipo sanguineo</th>
   67 |                 <th>Nivel</th>
   68 |                 <th>Ocupacao</th>
   69 |             </tr>
   70 |         </thead>
   71 |         <tbody>
   72 |             {% for item in estoque_geral %}
   73 |                 <tr>
   74 |                     <td>{{ item.tipo }}</td>
   75 |                     <td>{{ item.nivel }}</td>
   76 |                     <td>{{ item.percentual }}%</td>
   77 |                 </tr>
   78 |             {% endfor %}
   79 |         </tbody>
   80 |     </table>
   81 | </section>
   82 | 
   83 | <section>
   84 |     <h2>Pedidos ativos</h2>
   85 | 
   86 |     <ul>
   87 |         {% for pedido in pedidos_ativos %}
   88 |             <li>
   89 |                 <strong>{{ pedido.titulo }}</strong><br>
   90 |                 {{ pedido.tipo_sanguineo }} - {{ pedido.cidade }} - Urgencia {{ pedido.urgencia }}
   91 |             </li>
   92 |         {% endfor %}
   93 |     </ul>
   94 | </section>
   95 | 
   96 | <p>
   97 |     <a href="{% url 'accounts:cadastro' %}">Criar conta</a>
   98 |     <a href="{% url 'accounts:login' %}">Entrar</a>
   99 |     <a href="{% url 'admin:index' %}">Admin</a>
  100 |     
  101 | </p>
  102 | {% endblock %}
``````

## templates/accounts/login.html

Original: [templates/accounts/login.html](<C:/Users/lb119/Elo/templates/accounts/login.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% comment %}
    4 | RESUMO DO ARQUIVO
    5 | =================
    6 | Tela de login por e-mail e senha. LoginView fornece o objeto ``form`` e processa
    7 | a autenticacao usando o model configurado em AUTH_USER_MODEL.
    8 | {% endcomment %}
    9 | 
   10 | {% block title %}Entrar | Elo{% endblock %}
   11 | 
   12 | {% block content %}
   13 | <h1>Entrar</h1>
   14 | 
   15 | <form method="post">
   16 |     {% csrf_token %}
   17 | 
   18 |     <!-- Exibe e-mail, senha e eventuais erros de autenticacao. -->
   19 |     {{ form.as_p }}
   20 | 
   21 |     {% if next %}
   22 |         <!-- Quando login_required enviou a pessoa para o login, next guarda a
   23 |              pagina original para que ela possa retornar depois de entrar. -->
   24 |         <input type="hidden" name="next" value="{{ next }}">
   25 |     {% endif %}
   26 | 
   27 |     <button type="submit">Entrar</button>
   28 | </form>
   29 | 
   30 | <p>
   31 |     Ainda nao tem conta?
   32 |     <a href="{% url 'accounts:cadastro' %}">Criar conta</a>
   33 | </p>
   34 | <p>
   35 |     <a href="{% url 'accounts:inicio' %}">Continuar como visitante</a>
   36 | </p>
   37 | {% endblock %}
``````

## templates/accounts/minhas_solicitacoes.html

Original: [templates/accounts/minhas_solicitacoes.html](<C:/Users/lb119/Elo/templates/accounts/minhas_solicitacoes.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% block title %}Minhas solicitações | Elo{% endblock %}
    4 | 
    5 | {% block content %}
    6 | <h1>Minhas solicitações de divulgação</h1>
    7 | 
    8 | <form method="get">
    9 |     <label for="status">Filtrar por status:</label>
   10 |     <select id="status" name="status">
   11 |         <option value="">Todos</option>
   12 |         {% for codigo, nome in status_opcoes %}
   13 |             <option value="{{ codigo }}" {% if status_atual == codigo %}selected{% endif %}>
   14 |                 {{ nome }}
   15 |             </option>
   16 |         {% endfor %}
   17 |     </select>
   18 |     <button type="submit">Filtrar</button>
   19 | </form>
   20 | 
   21 | {% for solicitacao in solicitacoes %}
   22 |     <section>
   23 |         <h2>{{ solicitacao.titulo }}</h2>
   24 |         <p><strong>Protocolo:</strong> {{ solicitacao.id_pedido }}</p>
   25 |         <p><strong>Tipo:</strong> {{ solicitacao.tipo_sanguineo }}</p>
   26 |         <p><strong>Cidade:</strong> {{ solicitacao.cidade }}</p>
   27 |         <p><strong>Hemocentro:</strong> {{ solicitacao.hemocentro_destino.nome }}</p>
   28 |         <p><strong>Status:</strong> {{ solicitacao.get_status_display }}</p>
   29 |        <p><strong>Enviada em:</strong> {{ solicitacao.data_criacao|date:"d/m/Y H:i" }}</p>
   30 | 
   31 |         {% with ultima_validacao=solicitacao.validacoes.all.0 %}
   32 |             {% if ultima_validacao %}
   33 |                 <p>
   34 |                     <strong>Última análise:</strong>
   35 |                     {{ ultima_validacao.get_status_validacao_display }}
   36 |                 </p>
   37 |                 {% if ultima_validacao.motivo %}
   38 |                     <p><strong>Orientação:</strong> {{ ultima_validacao.motivo }}</p>
   39 |                 {% endif %}
   40 |             {% endif %}
   41 |         {% endwith %}
   42 |     </section>
   43 | {% empty %}
   44 |     <p>Você ainda não enviou uma solicitação.</p>
   45 | {% endfor %}
   46 | 
   47 | <p><a href="{% url 'accounts:pedido_publicar' %}">Enviar nova solicitação</a></p>
   48 | <p><a href="{% url 'accounts:dashboard' %}">Voltar ao painel</a></p>
   49 | {% endblock %}
``````

## templates/accounts/painel_aprovacao_hemocentros.html

Original: [templates/accounts/painel_aprovacao_hemocentros.html](<C:/Users/lb119/Elo/templates/accounts/painel_aprovacao_hemocentros.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% block title %}Aprovação de Hemocentros | Elo{% endblock %}
    4 | 
    5 | {% block content %}
    6 | 
    7 | <section>
    8 |     <h1>Aprovação de Hemocentros</h1>
    9 | 
   10 |     <p>
   11 |         Analise os cadastros institucionais antes de liberar
   12 |         a publicação e a alteração de estoques.
   13 |     </p>
   14 | 
   15 |     <p>
   16 |         <a href="{% url 'accounts:dashboard' %}">Voltar ao painel</a>
   17 |         · <a href="{% url 'accounts:inicio' %}">Página inicial</a>
   18 |         · <a href="{% url 'accounts:estoque_publico' %}">Estoques públicos</a>
   19 |         · <a href="{% url 'accounts:painel_validacao_pedidos' %}">Moderar pedidos</a>
   20 |     </p>
   21 | 
   22 |     <p>
   23 |         Hemocentros pendentes:
   24 |         <strong>{{ hemocentros|length }}</strong>
   25 |     </p>
   26 | 
   27 |     {% if hemocentros %}
   28 |         {% for hemocentro in hemocentros %}
   29 |             <article>
   30 |                 <hr>
   31 | 
   32 |                 <h2>{{ hemocentro.nome }}</h2>
   33 | 
   34 |                 <p>
   35 |                     <strong>Status:</strong>
   36 |                     {{ hemocentro.get_status_validacao_display }}
   37 |                 </p>
   38 | 
   39 |                 <p>
   40 |                     <strong>E-mail:</strong>
   41 |                     {{ hemocentro.email }}
   42 |                 </p>
   43 | 
   44 |                 <p>
   45 |                     <strong>CNPJ:</strong>
   46 |                     {{ hemocentro.cnpj|default:"Não informado" }}
   47 |                 </p>
   48 | 
   49 |                 <p>
   50 |                     <strong>Telefone:</strong>
   51 |                     {{ hemocentro.telefone|default:"Não informado" }}
   52 |                 </p>
   53 | 
   54 |                 <p>
   55 |                     <strong>Cidade:</strong>
   56 |                     {{ hemocentro.cidade|default:"Não informado" }}
   57 |                 </p>
   58 | 
   59 |                 <p>
   60 |                     <strong>Estado:</strong>
   61 |                     {{ hemocentro.estado|default:"Não informado" }}
   62 |                 </p>
   63 | 
   64 |                 <p>
   65 |                     <strong>Data do cadastro:</strong>
   66 |                     {{ hemocentro.date_joined|date:"d/m/Y H:i" }}
   67 |                 </p>
   68 | 
   69 |                 <h3>Decisão administrativa</h3>
   70 | 
   71 |                 <form
   72 |                     method="post"
   73 |                     action="{% url 'accounts:aprovar_hemocentro' hemocentro.pk %}"
   74 |                 >
   75 |                     {% csrf_token %}
   76 | 
   77 |                     <label for="parecer-aprovar-{{ hemocentro.pk }}">
   78 |                         Parecer da aprovação:
   79 |                     </label>
   80 |                     <br>
   81 | 
   82 |                     <textarea
   83 |                         id="parecer-aprovar-{{ hemocentro.pk }}"
   84 |                         name="parecer"
   85 |                         rows="4"
   86 |                         cols="60"
   87 |                         placeholder="Digite o parecer da aprovação..."
   88 |                     ></textarea>
   89 | 
   90 |                     <br>
   91 | 
   92 |                     <button type="submit">
   93 |                         Aprovar Hemocentro
   94 |                     </button>
   95 |                 </form>
   96 | 
   97 |                 <br>
   98 | 
   99 |                 <form
  100 |                     method="post"
  101 |                     action="{% url 'accounts:recusar_hemocentro' hemocentro.pk %}"
  102 |                 >
  103 |                     {% csrf_token %}
  104 | 
  105 |                     <label for="parecer-recusar-{{ hemocentro.pk }}">
  106 |                         Motivo da recusa:
  107 |                     </label>
  108 |                     <br>
  109 | 
  110 |                     <textarea
  111 |                         id="parecer-recusar-{{ hemocentro.pk }}"
  112 |                         name="parecer"
  113 |                         rows="4"
  114 |                         cols="60"
  115 |                         placeholder="Informe o motivo da recusa..."
  116 |                     ></textarea>
  117 | 
  118 |                     <br>
  119 | 
  120 |                     <button type="submit">
  121 |                         Recusar Hemocentro
  122 |                     </button>
  123 |                 </form>
  124 | 
  125 |                 <br>
  126 | 
  127 |                 <form
  128 |                     method="post"
  129 |                     action="{% url 'accounts:solicitar_correcao_hemocentro' hemocentro.pk %}"
  130 |                 >
  131 |                     {% csrf_token %}
  132 | 
  133 |                     <label for="parecer-correcao-{{ hemocentro.pk }}">
  134 |                         Orientação para correção:
  135 |                     </label>
  136 |                     <br>
  137 | 
  138 |                     <textarea
  139 |                         id="parecer-correcao-{{ hemocentro.pk }}"
  140 |                         name="parecer"
  141 |                         rows="4"
  142 |                         cols="60"
  143 |                         placeholder="Informe o que precisa ser corrigido..."
  144 |                     ></textarea>
  145 | 
  146 |                     <br>
  147 | 
  148 |                     <button type="submit">
  149 |                         Solicitar correção
  150 |                     </button>
  151 |                 </form>
  152 |             </article>
  153 |         {% endfor %}
  154 |     {% else %}
  155 |         <hr>
  156 | 
  157 |         <h2>Nenhum Hemocentro pendente</h2>
  158 | 
  159 |         <p>
  160 |             Não existem cadastros aguardando análise.
  161 |         </p>
  162 |     {% endif %}
  163 | </section>
  164 | 
  165 | {% endblock %}
``````

## templates/accounts/painel_moderacao_pedidos.html

Original: [templates/accounts/painel_moderacao_pedidos.html](<C:/Users/lb119/Elo/templates/accounts/painel_moderacao_pedidos.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% block title %}Moderação de pedidos | Elo{% endblock %}
    4 | 
    5 | {% block content %}
    6 | <h1>Moderação de pedidos de sangue</h1>
    7 | <p>
    8 |     O Administrador acompanha validações e suspeitas. A publicação oficial
    9 |     continua sendo responsabilidade exclusiva do Hemocentro aprovado.
   10 | </p>
   11 | 
   12 | <form method="get">
   13 |     <label for="status">Filtrar por status:</label>
   14 |     <select id="status" name="status">
   15 |         <option value="">Todos</option>
   16 |         {% for codigo, nome in status_opcoes %}
   17 |             <option value="{{ codigo }}" {% if status_atual == codigo %}selected{% endif %}>
   18 |                 {{ nome }}
   19 |             </option>
   20 |         {% endfor %}
   21 |     </select>
   22 |     <button type="submit">Filtrar</button>
   23 | </form>
   24 | 
   25 | <p>
   26 |     <a href="{% url 'accounts:dashboard' %}">Voltar ao painel</a>
   27 |     · <a href="{% url 'accounts:painel_aprovacao_hemocentros' %}">Validar Hemocentros</a>
   28 | </p>
   29 | 
   30 | {% for pedido in pedidos %}
   31 |     <section>
   32 |         <h2>{{ pedido.titulo }}</h2>
   33 |         <p><strong>Protocolo:</strong> {{ pedido.id_pedido }}</p>
   34 |         <p><strong>Solicitante:</strong> {{ pedido.nome_solicitante }}</p>
   35 |         <p><strong>Contato:</strong> {{ pedido.contato }}</p>
   36 |         <p><strong>Hemocentro:</strong> {{ pedido.hemocentro_destino.nome }}</p>
   37 |         <p><strong>Tipo:</strong> {{ pedido.tipo_sanguineo }}</p>
   38 |         <p><strong>Cidade:</strong> {{ pedido.cidade }}</p>
   39 |         <p><strong>Urgência:</strong> {{ pedido.get_urgencia_display }}</p>
   40 |         <p><strong>Status:</strong> {{ pedido.get_status_display }}</p>
   41 |         <p><strong>Descrição:</strong> {{ pedido.descricao }}</p>
   42 | 
   43 |         {% if pedido.duplicidade_suspeita %}
   44 |             <p><strong>Atenção:</strong> foi encontrada solicitação semelhante no período de validação.</p>
   45 |         {% endif %}
   46 | 
   47 |         {% with ultima_validacao=pedido.validacoes.all.0 %}
   48 |             {% if ultima_validacao %}
   49 |                 <p>
   50 |                     <strong>Última moderação:</strong>
   51 |                     {{ ultima_validacao.get_status_validacao_display }}
   52 |                     — {{ ultima_validacao.motivo }}
   53 |                 </p>
   54 |             {% endif %}
   55 |         {% endwith %}
   56 | 
   57 |         {% if pedido.status != "ENCERRADA" %}
   58 |             <form method="post" action="{% url 'accounts:marcar_pedido_suspeito' pedido.id_pedido %}">
   59 |                 {% csrf_token %}
   60 |                 <textarea name="motivo" rows="2" required placeholder="Explique o motivo da suspeita ou da auditoria"></textarea>
   61 |                 <button type="submit">Marcar como suspeito</button>
   62 |             </form>
   63 |         {% endif %}
   64 |     </section>
   65 | {% empty %}
   66 |     <p>Nenhum pedido pendente ou suspeito para moderação.</p>
   67 | {% endfor %}
   68 | {% endblock %}
``````

## templates/accounts/painel_validacao_pedidos.html

Original: [templates/accounts/painel_validacao_pedidos.html](<C:/Users/lb119/Elo/templates/accounts/painel_validacao_pedidos.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% block title %}Análise de solicitações | Elo{% endblock %}
    4 | 
    5 | {% block content %}
    6 | <h1>Solicitações recebidas</h1>
    7 | <p>Somente após sua análise uma necessidade será publicada oficialmente.</p>
    8 | 
    9 | <form method="get">
   10 |     <label for="status">Filtrar por status:</label>
   11 |     <select id="status" name="status">
   12 |         <option value="">Todos</option>
   13 |         {% for codigo, nome in status_opcoes %}
   14 |             <option value="{{ codigo }}">{{ nome }}</option>
   15 |         {% endfor %}
   16 |     </select>
   17 |     <button type="submit">Filtrar</button>
   18 | </form>
   19 | 
   20 | <p>
   21 |     <a href="{% url 'accounts:dashboard' %}">Voltar ao painel</a>
   22 |     · <a href="{% url 'accounts:estoque_hemocentro' %}">Meu estoque</a>
   23 | </p>
   24 | 
   25 | {% for pedido in solicitacoes %}
   26 | 
   27 |     <section>
   28 |         <h2>{{ pedido.titulo }}</h2>
   29 | 
   30 |         <p><strong>Solicitante:</strong> {{ pedido.nome_solicitante }}</p>
   31 |         <p><strong>Contato:</strong> {{ pedido.contato }}</p>
   32 |         <p><strong>Tipo:</strong> {{ pedido.tipo_sanguineo }}</p>
   33 |         <p><strong>Cidade:</strong> {{ pedido.cidade }}</p>
   34 |         <p><strong>Urgência:</strong> {{ pedido.get_urgencia_display }}</p>
   35 |         <p><strong>Hemocentro:</strong> {{ pedido.hemocentro_destino.nome }}</p>
   36 |         <p><strong>Status:</strong> {{ pedido.get_status_display }}</p>
   37 |         <p><strong>Descrição:</strong> {{ pedido.descricao }}</p>
   38 | 
   39 |         {% if pedido.informacoes_complementares %}
   40 |             <p><strong>Informações complementares:</strong> {{ pedido.informacoes_complementares }}</p>
   41 |         {% endif %}
   42 | 
   43 |         {% if pedido.duplicidade_suspeita %}
   44 |             <p><strong>Atenção:</strong> há solicitação semelhante em análise.</p>
   45 |         {% endif %}
   46 | 
   47 |         {% if pedido.status != "PUBLICADA" and pedido.status != "RECUSADA" %}
   48 |             <form method="post" action="{% url 'accounts:aprovar_pedido' pedido.id_pedido %}">
   49 |                 {% csrf_token %}
   50 |                 <textarea name="motivo" rows="2" placeholder="Observação da análise"></textarea>
   51 |                 <button type="submit">Aprovar e publicar</button>
   52 |             </form>
   53 |             <form method="post" action="{% url 'accounts:solicitar_correcao_pedido' pedido.id_pedido %}">
   54 |                 {% csrf_token %}
   55 |                 <textarea name="motivo" rows="2" required placeholder="O que deve ser corrigido?"></textarea>
   56 |                 <button type="submit">Solicitar correção</button>
   57 |             </form>
   58 |             <form method="post" action="{% url 'accounts:recusar_pedido' pedido.id_pedido %}">
   59 |                 {% csrf_token %}
   60 |                 <textarea name="motivo" rows="2" placeholder="Motivo da recusa"></textarea>
   61 |                 <button type="submit">Recusar</button>
   62 |   </form>
   63 |             <form method="post" action="{% url 'accounts:marcar_pedido_suspeito' pedido.id_pedido %}">
   64 |                 {% csrf_token %}
   65 |                 <textarea name="motivo" rows="2" required placeholder="Explique por que o pedido parece suspeito"></textarea>
   66 |                 <button type="submit">Marcar como suspeito</button>
   67 |             </form>
   68 |         {% endif %}
   69 |     </section>
   70 | {% empty %}
   71 |     <p>Nenhuma solicitação aguardando análise.</p>
   72 | {% endfor %}
   73 | 
   74 | {% endblock %}
``````

## templates/accounts/pedido_detalhe.html

Original: [templates/accounts/pedido_detalhe.html](<C:/Users/lb119/Elo/templates/accounts/pedido_detalhe.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% block title %}Pedido de sangue registrado | Elo{% endblock %}
    4 | 
    5 | {% block content %}
    6 | <h1>Pedido de sangue registrado</h1>
    7 | 
    8 | <p>
    9 |     Seu pedido foi registrado e está aguardando validação.
   10 | </p>
   11 | 
   12 | <dl>
   13 |     <dt>Para quem</dt>
   14 |     <dd>{{ pedido.get_para_quem_display }}</dd>
   15 | 
   16 |     <dt>Tipo solicitado</dt>
   17 |     <dd>{{ pedido.tipo_sanguineo }}</dd>
   18 | 
   19 |     <dt>Hemocentro</dt>
   20 |     <dd>{{ pedido.hemocentro.nome }}</dd>
   21 | 
   22 |     <dt>Cidade</dt>
   23 |     <dd>{{ pedido.cidade }}{% if pedido.hemocentro.estado %} - {{ pedido.hemocentro.estado }}{% endif %}</dd>
   24 | 
   25 |     <dt>Urgência</dt>
   26 |     <dd>{{ pedido.get_urgencia_display }}</dd>
   27 | 
   28 |     {% if pedido.nome_paciente %}
   29 |         <dt>Nome da pessoa</dt>
   30 |         <dd>{{ pedido.nome_paciente }}</dd>
   31 |     {% endif %}
   32 | 
   33 |     <dt>Descrição</dt>
   34 |     <dd>{{ pedido.descricao }}</dd>
   35 | 
   36 |     <dt>Status</dt>
   37 |     <dd>{{ pedido.get_status_display }}</dd>
   38 | 
   39 |     <dt>Data</dt>
   40 |     <dd>{{ pedido.data_criacao|date:"d/m/Y H:i" }}</dd>
   41 | </dl>
   42 | 
   43 | <p><a href="{% url 'accounts:dashboard' %}">Voltar ao início</a></p>
   44 | {% endblock %}
``````

## templates/accounts/pedido_filtrar.html

Original: [templates/accounts/pedido_filtrar.html](<C:/Users/lb119/Elo/templates/accounts/pedido_filtrar.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% block title %}Consultar pedidos de sangue | Elo{% endblock %}
    4 | 
    5 | {% block content %}
    6 | 
    7 | <h1>Consultar pedidos de sangue</h1>
    8 | 
    9 | <p>
   10 |     Utilize os filtros abaixo para encontrar pedidos de sangue ativos.
   11 | </p>
   12 | 
   13 | <form method="get">
   14 | 
   15 |     {{ form.non_field_errors }}
   16 | 
   17 |     <p>
   18 |         {{ form.tipo_sanguineo.label_tag }}
   19 |         {{ form.tipo_sanguineo }}
   20 |         {{ form.tipo_sanguineo.errors }}
   21 |     </p>
   22 | 
   23 |     <p>
   24 |         {{ form.urgencia.label_tag }}
   25 |         {{ form.urgencia }}
   26 |         {{ form.urgencia.errors }}
   27 |     </p>
   28 | 
   29 |     <p>
   30 |         {{ form.cidade.label_tag }}
   31 |         {{ form.cidade }}
   32 |         {{ form.cidade.errors }}
   33 |     </p>
   34 | 
   35 |     <p>
   36 |         {{ form.hemocentro.label_tag }}
   37 |         {{ form.hemocentro }}
   38 |         {{ form.hemocentro.errors }}
   39 |     </p>
   40 | 
   41 |     <p>
   42 |         {{ form.data.label_tag }}
   43 |         {{ form.data }}
   44 |         {{ form.data.errors }}
   45 |     </p>
   46 | 
   47 |     <p>
   48 |         {{ form.status.label_tag }}
   49 |         {{ form.status }}
   50 |         {{ form.status.errors }}
   51 |     </p>
   52 | 
   53 |     <button type="submit">
   54 |         Filtrar pedidos
   55 |     </button>
   56 | 
   57 |     <a href="{% url 'accounts:consultar_pedidos' %}">
   58 |         Limpar filtros
   59 |     </a>
   60 | 
   61 | </form>
   62 | 
   63 | <hr>
   64 | 
   65 | <h2>Pedidos encontrados</h2>
   66 | 
   67 | {% if pedidos %}
   68 | 
   69 |     {% for pedido in pedidos %}
   70 | 
   71 |         <article>
   72 |             <h3>{{ pedido.titulo }}</h3>
   73 | 
   74 |             <p>
   75 |                 <strong>Tipo sanguíneo:</strong>
   76 |                 {{ pedido.tipo_sanguineo }}
   77 |             </p>
   78 | 
   79 |             <p>
   80 |                 <strong>Urgência:</strong>
   81 |                 {{ pedido.get_urgencia_display }}
   82 |             </p>
   83 | 
   84 |             <p>
   85 |                 <strong>Cidade:</strong>
   86 |                 {{ pedido.cidade }}
   87 |             </p>
   88 | 
   89 |             <p>
   90 |                 <strong>Hemocentro:</strong>
   91 |                 {{ pedido.hemocentro_destino.nome }}
   92 |             </p>
   93 | 
   94 |             <p>
   95 |                 <strong>Status:</strong>
   96 |                 {{ pedido.get_status_display }}
   97 |             </p>
   98 | 
   99 |             <p>
  100 |                 <strong>Publicado em:</strong>
  101 |                 {{ pedido.publicado_em|default:pedido.data_criacao|date:"d/m/Y H:i" }}
  102 |             </p>
  103 | 
  104 |             <p>
  105 |                 <strong>Descrição:</strong>
  106 |                 {{ pedido.descricao }}
  107 |             </p>
  108 |         </article>
  109 | 
  110 |         <hr>
  111 | 
  112 |     {% endfor %}
  113 | 
  114 | {% else %}
  115 | 
  116 |     <p>
  117 |         Nenhum pedido de sangue encontrado.
  118 |     </p>
  119 | 
  120 | {% endif %}
  121 | 
  122 | <p>
  123 |     <a href="{% url 'accounts:dashboard' %}">
  124 |         Voltar ao painel
  125 |     </a>
  126 | </p>
  127 | 
  128 | {% endblock %}
``````

## templates/accounts/pedido_publicar.html

Original: [templates/accounts/pedido_publicar.html](<C:/Users/lb119/Elo/templates/accounts/pedido_publicar.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% block title %}Solicitar divulgação | Elo{% endblock %}
    4 | 
    5 | {% block content %}
    6 | <h1>Solicitar divulgação de necessidade</h1>
    7 | 
    8 | <p>
    9 |     O envio cria uma solicitação. Ela só se torna um pedido público depois da
   10 |     análise do Hemocentro de referência.
   11 | </p>
   12 | 
   13 | <form method="post">
   14 |     {% csrf_token %}
   15 |     {{ form.non_field_errors }}
   16 |     {{ form.as_p }}
   17 |     <button type="submit">Enviar para análise</button>
   18 | </form>
   19 | 
   20 | <p><a href="{% url 'accounts:dashboard' %}">Voltar ao painel</a></p>
   21 | {% endblock %}
``````

## templates/accounts/pedidos_listar.html

Original: [templates/accounts/pedidos_listar.html](<C:/Users/lb119/Elo/templates/accounts/pedidos_listar.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% comment %}
    4 | Lista pública de pedidos de sangue que já foram aprovados.
    5 | 
    6 | A view envia:
    7 | - form: formulário de filtros;
    8 | - pedidos: somente pedidos publicados.
    9 | 
   10 | Pedidos pendentes, suspeitos ou recusados
   11 | não aparecem nesta página.
   12 | {% endcomment %}
   13 | 
   14 | {% block title %}Pedidos de sangue | Elo{% endblock %}
   15 | 
   16 | {% block content %}
   17 | 
   18 | <h1>Pedidos de sangue ativos</h1>
   19 | 
   20 | <form method="get">
   21 |     {{ form.as_p }}
   22 | 
   23 |     <button type="submit">
   24 |         Filtrar pedidos
   25 |     </button>
   26 | 
   27 |     <a href="{% url 'accounts:consultar_pedidos' %}">
   28 |         Limpar filtros
   29 |     </a>
   30 | </form>
   31 | 
   32 | <hr>
   33 | 
   34 | <h2>Pedidos encontrados</h2>
   35 | 
   36 | {% for pedido in pedidos %}
   37 | 
   38 |     <section>
   39 |         <h3>{{ pedido.titulo }}</h3>
   40 | 
   41 |         <p>
   42 |             <strong>Tipo sanguíneo:</strong>
   43 |             {{ pedido.tipo_sanguineo }}
   44 |         </p>
   45 | 
   46 |         <p>
   47 |             <strong>Urgência:</strong>
   48 |             {{ pedido.get_urgencia_display }}
   49 |         </p>
   50 | 
   51 |         <p>
   52 |             <strong>Cidade:</strong>
   53 |             {{ pedido.cidade }}
   54 |         </p>
   55 | 
   56 |         <p>
   57 |             <strong>Hemocentro:</strong>
   58 |             {{ pedido.hemocentro_destino.nome }}
   59 |         </p>
   60 | 
   61 |         <p>
   62 |             <strong>Descrição:</strong>
   63 |             {{ pedido.descricao }}
   64 |         </p>
   65 | 
   66 |         <p>
   67 |             <strong>Status:</strong>
   68 |             {{ pedido.get_status_display }}
   69 |         </p>
   70 | 
   71 |         <p>
   72 |             <strong>Publicado em:</strong>
   73 |             {{ pedido.publicado_em|default:pedido.data_criacao|date:"d/m/Y H:i" }}
   74 |         </p>
   75 |     </section>
   76 | 
   77 | {% empty %}
   78 | 
   79 |     <p>
   80 |         Nenhum pedido ativo encontrado.
   81 |     </p>
   82 | 
   83 | {% endfor %}
   84 | 
   85 | {% if user.is_authenticated %}
   86 |     {% if user.perfil == "RECEPTOR" %}
   87 |         <p>
   88 |             <a href="{% url 'accounts:criar_pedido_sangue' %}">
   89 |                 Solicitar divulgação de necessidade
   90 |             </a>
   91 |         </p>
   92 |     {% endif %}
   93 | {% endif %}
   94 | 
   95 | <p>
   96 |     <a href="{% url 'accounts:dashboard' %}">
   97 |         Voltar ao painel
   98 |     </a>
   99 | </p>
  100 | 
  101 | {% endblock %}
``````

## templates/accounts/triagem_apresentacao.html

Original: [templates/accounts/triagem_apresentacao.html](<C:/Users/lb119/Elo/templates/accounts/triagem_apresentacao.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% comment %}
    4 | Esta página é pública para que a pessoa entenda a triagem antes de entrar.
    5 | Somente os formulários abaixo iniciam um registro no histórico.
    6 | {% endcomment %}
    7 | 
    8 | {% block title %}Triagem para doação | Elo{% endblock %}
    9 | 
   10 | {% block content %}
   11 | <h1>Seu gesto de cuidado começa aqui.</h1>
   12 | 
   13 | <p>
   14 |     Esta triagem foi preparada para orientar você antes da doação, de forma
   15 |     simples, tranquila e cuidadosa. As perguntas ajudam a identificar situações
   16 |     que podem precisar de mais atenção ou que talvez façam com que a doação
   17 |     precise ser adiada.
   18 | </p>
   19 | 
   20 | <p>
   21 |     Para tornar esse processo mais adequado a cada pessoa, você poderá escolher
   22 |     entre <strong>duas formas de triagem</strong>. A
   23 |     <strong>triagem extensa</strong> é mais completa e indicada principalmente
   24 |     para quem nunca doou sangue, está fazendo essa avaliação pela primeira vez
   25 |     ou ainda tem dúvidas sobre alguma condição, procedimento, medicamento ou
   26 |     situação específica. Por ter mais perguntas e trazer mais detalhes, ela pode
   27 |     levar um pouco mais de tempo. Já a <strong>triagem simplificada</strong>
   28 |     possui perguntas mais diretas e resumidas, sendo uma opção mais ágil para
   29 |     quem já conhece essas informações e precisa apenas verificar se houve alguma
   30 |     mudança importante desde a última avaliação.
   31 | </p>
   32 | 
   33 | <p>
   34 |     Algumas questões envolvem sua saúde, seus hábitos e acontecimentos recentes.
   35 |     Responda com calma e sinceridade. Se não souber ou não se lembrar de alguma
   36 |     informação, tudo bem — basta indicar isso ao longo da triagem.
   37 | </p>
   38 | 
   39 | <p>
   40 |     É importante lembrar que esta triagem é <strong>somente orientativa</strong>.
   41 |     Ela não substitui a avaliação feita no hemocentro e não confirma se você pode
   42 |     ou não doar sangue. <strong>Quem dará a resposta final será sempre a equipe
   43 |     do hemocentro</strong>, após a entrevista e as avaliações realizadas no
   44 |     local.
   45 | </p>
   46 | 
   47 | <p>
   48 |     A ideia aqui é apenas ajudar você a chegar mais informado(a), seguro(a) e
   49 |     preparado(a) para esse momento.
   50 | </p>
   51 | 
   52 | <p>
   53 |     <strong>Quando estiver pronto(a), escolha a opção que mais combina com você
   54 |     e podemos começar.</strong>
   55 | </p>
   56 | 
   57 | <section>
   58 |     <h2>Triagem extensa</h2>
   59 |     <p>Questionário completo, indicado para a primeira avaliação ou para revisar todo o histórico.</p>
   60 | 
   61 |     {% if pode_iniciar %}
   62 |         <form method="post" action="{% url 'accounts:triagem_iniciar' modalidade='extensa' %}">
   63 |             {% csrf_token %}
   64 |             <label>
   65 |                 <input type="checkbox" name="aceite_termo" required>
   66 |                 Li e estou ciente de que a pré-triagem é orientativa e não
   67 |                 substitui a avaliação clínica presencial do hemocentro.
   68 |             </label>
   69 |             {% if triagem_extensa_reutilizavel %}
   70 |                 <label>
   71 |                     <input type="checkbox" name="reutilizar_respostas">
   72 |                     Reutilizar respostas da última triagem extensa concluída.
   73 |                 </label>
   74 |             {% endif %}
   75 |             <button type="submit">Iniciar ou continuar triagem extensa</button>
   76 |         </form>
   77 |     {% elif not user.is_authenticated %}
   78 |         <form method="get" action="{% url 'accounts:cadastro' %}">
   79 |             <button type="submit">Criar conta para iniciar a triagem extensa</button>
   80 |         </form>
   81 |     {% endif %}
   82 | </section>
   83 | 
   84 | <section>
   85 |     <h2>Triagem simplificada</h2>
   86 |     <p>Verificação mais rápida para quem já concluiu a extensa e deseja informar mudanças.</p>
   87 | 
   88 |     {% if pode_simplificada %}
   89 |         <form method="post" action="{% url 'accounts:triagem_iniciar' modalidade='simplificada' %}">
   90 |             {% csrf_token %}
   91 |             <label>
   92 |                 <input type="checkbox" name="aceite_termo" required>
   93 |                 Li e estou ciente de que a pré-triagem é orientativa e não
   94 |                 substitui a avaliação clínica presencial do hemocentro.
   95 |             </label>
   96 |             <button type="submit">Iniciar ou continuar triagem simplificada</button>
   97 |         </form>
   98 |     {% elif pode_iniciar %}
   99 |         <p>Conclua uma triagem extensa para liberar esta opção.</p>
  100 |     {% elif not user.is_authenticated %}
  101 |         <form method="get" action="{% url 'accounts:login' %}">
  102 |             <button type="submit">Entrar para continuar uma triagem</button>
  103 |         </form>
  104 |     {% endif %}
  105 | </section>
  106 | 
  107 | {% if pode_iniciar %}
  108 |     <p><a href="{% url 'accounts:triagem_historico' %}">Ver meu histórico de triagens</a></p>
  109 | {% elif user.is_authenticated %}
  110 |     <p>A triagem para doação está disponível para o perfil Doador.</p>
  111 | {% else %}
  112 |     <p>Para responder e salvar sua triagem, crie uma conta ou entre no sistema.</p>
  113 | {% endif %}
  114 | 
  115 | <p><a href="{% url 'accounts:inicio' %}">Voltar para a página inicial</a></p>
  116 | {% endblock %}
``````

## templates/accounts/triagem_extensa.html

Original: [templates/accounts/triagem_extensa.html](<C:/Users/lb119/Elo/templates/accounts/triagem_extensa.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% block title %}Triagem extensa | Elo{% endblock %}
    4 | 
    5 | {% block content %}
    6 | 
    7 | <h1>Triagem extensa</h1>
    8 | 
    9 | <p>
   10 |     Esta triagem é apenas orientativa e não substitui a entrevista,
   11 |     os exames ou a decisão da equipe do hemocentro.
   12 | </p>
   13 | 
   14 | <p>
   15 |     Responda com o máximo de precisão possível.
   16 |     Quando não souber uma resposta, informe que não sabe.
   17 | </p>
   18 | 
   19 | <form method="post">
   20 | 
   21 |     {% csrf_token %}
   22 | 
   23 |     {{ form.non_field_errors }}
   24 | 
   25 |     {{ form.as_p }}
   26 | 
   27 |     <button type="submit">
   28 |         Calcular orientação
   29 |     </button>
   30 | 
   31 | </form>
   32 | 
   33 | <p>
   34 |     <a href="{% url 'accounts:dashboard' %}">
   35 |         Voltar para o painel
   36 |     </a>
   37 | </p>
   38 | 
   39 | {% endblock %}
``````

## templates/accounts/triagem_historico.html

Original: [templates/accounts/triagem_historico.html](<C:/Users/lb119/Elo/templates/accounts/triagem_historico.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% comment %}
    4 | O queryset desta página já pertence ao usuário autenticado. A listagem mostra
    5 | somente o resumo; respostas individuais continuam protegidas no banco.
    6 | {% endcomment %}
    7 | 
    8 | {% block title %}Meu histórico de triagens | Elo{% endblock %}
    9 | 
   10 | {% block content %}
   11 | <h1>Meu histórico de triagens</h1>
   12 | 
   13 | {% if triagens %}
   14 |     <ul>
   15 |         {% for triagem in triagens %}
   16 |             <li>
   17 |                 <strong>Triagem {{ triagem.id_triagem }} — {{ triagem.get_modalidade_display }}</strong><br>
   18 |                 Iniciada em {{ triagem.iniciada_em|date:"d/m/Y H:i" }}<br>
   19 |                 Situação: {{ triagem.get_status_display }}
   20 |                 <br>Versão das regras: {{ triagem.regra_version }}
   21 | 
   22 |                 {% if triagem.status == "CONCLUIDA" %}
   23 |                     <br>Orientação: {{ triagem.get_resultado_display }}
   24 |                     <br><a href="{% url 'accounts:triagem_resultado' id_triagem=triagem.id_triagem %}">Ver resultado</a>
   25 |                 {% elif triagem.status == "EM_ANDAMENTO" %}
   26 |                     <br><a href="{% url 'accounts:triagem_pergunta' id_triagem=triagem.id_triagem %}">Continuar triagem</a>
   27 |                 {% endif %}
   28 |             </li>
   29 |         {% endfor %}
   30 |     </ul>
   31 | {% else %}
   32 |     <p>Você ainda não iniciou uma triagem.</p>
   33 | {% endif %}
   34 | 
   35 | <p><a href="{% url 'accounts:triagem_apresentacao' %}">Escolher uma triagem</a></p>
   36 | <p><a href="{% url 'accounts:dashboard' %}">Voltar para o painel</a></p>
   37 | {% endblock %}
``````

## templates/accounts/triagem_inicio.html

Original: [templates/accounts/triagem_inicio.html](<C:/Users/lb119/Elo/templates/accounts/triagem_inicio.html>).

``````text
``````

## templates/accounts/triagem_pergunta.html

Original: [templates/accounts/triagem_pergunta.html](<C:/Users/lb119/Elo/templates/accounts/triagem_pergunta.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% comment %}
    4 | Uma pergunta por página deixa o formulário legível. O Django cria os campos
    5 | de data e complemento somente quando a regra da pergunta precisa deles.
    6 | {% endcomment %}
    7 | 
    8 | {% block title %}Pergunta da triagem | Elo{% endblock %}
    9 | 
   10 | {% block content %}
   11 | <h1>{{ triagem.get_modalidade_display }}</h1>
   12 | 
   13 | <p>Triagem {{ triagem.id_triagem }} — Pergunta {{ numero_pergunta }} de {{ total_perguntas }}</p>
   14 | 
   15 | <h2>{{ pergunta.titulo }}</h2>
   16 | <p>{{ pergunta.explicacao }}</p>
   17 | 
   18 | <form method="post">
   19 |     {% csrf_token %}
   20 |     {{ form.non_field_errors }}
   21 | 
   22 |     {% for field in form %}
   23 |         <p>
   24 |             {{ field.label_tag }}<br>
   25 |             {{ field }}
   26 |             {% if field.help_text %}<br><small>{{ field.help_text }}</small>{% endif %}
   27 |             {% for error in field.errors %}<br>{{ error }}{% endfor %}
   28 |         </p>
   29 |     {% endfor %}
   30 | 
   31 |     {% if numero_pergunta > 1 %}
   32 |         <button type="submit" name="acao" value="anterior">Anterior</button>
   33 |     {% endif %}
   34 |     <button type="submit" name="acao" value="salvar">Salvar e sair</button>
   35 |     <button type="submit" name="acao" value="continuar">Continuar</button>
   36 | </form>
   37 | 
   38 | <p><a href="{% url 'accounts:triagem_historico' %}">Meu histórico de triagens</a></p>
   39 | {% endblock %}
``````

## templates/accounts/triagem_resultado.html

Original: [templates/accounts/triagem_resultado.html](<C:/Users/lb119/Elo/templates/accounts/triagem_resultado.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% block title %}Resultado da triagem | Elo{% endblock %}
    4 | 
    5 | {% block content %}
    6 | 
    7 | <h1>Resultado da triagem</h1>
    8 | 
    9 | <p>
   10 |     <strong>Resultado:</strong>
   11 |     {{ triagem.get_resultado_display }}
   12 | </p>
   13 | 
   14 | <p>
   15 |     {{ triagem.mensagem_resultado }}
   16 | </p>
   17 | 
   18 | {% if triagem.data_liberacao %}
   19 |     <p>
   20 |         <strong>Data orientativa:</strong>
   21 |         {{ triagem.data_liberacao|date:"d/m/Y" }}
   22 |     </p>
   23 | {% endif %}
   24 | 
   25 | {% if triagem.achados %}
   26 | 
   27 |     <h2>Orientações identificadas</h2>
   28 | 
   29 |     <ul>
   30 |         {% for achado in triagem.achados %}
   31 |             <li>
   32 |                 {{ achado.mensagem }}
   33 | 
   34 |                 {% if achado.data_liberacao %}
   35 |                     Data orientativa:
   36 |                     {{ achado.data_liberacao }}
   37 |                 {% endif %}
   38 |             </li>
   39 |         {% endfor %}
   40 |     </ul>
   41 | 
   42 | {% endif %}
   43 | 
   44 | <p>
   45 |     Esta orientação foi calculada com a versão:
   46 |     {{ triagem.regra_version }}
   47 | </p>
   48 | 
   49 | <p>
   50 |     <a href="{% url 'accounts:dashboard' %}">
   51 |         Voltar para o painel
   52 |     </a>
   53 | </p>
   54 | 
   55 | {% endblock %}
``````

## templates/accounts/triagem_revisao.html

Original: [templates/accounts/triagem_revisao.html](<C:/Users/lb119/Elo/templates/accounts/triagem_revisao.html>).

``````text
    1 | {% extends "base.html" %}
    2 | 
    3 | {% block title %}Revisão da triagem | Elo{% endblock %}
    4 | 
    5 | {% block content %}
    6 | <h1>Revise suas respostas</h1>
    7 | <p>
    8 |     Confira as informações antes de finalizar. O resultado será calculado
    9 |     somente após sua confirmação.
   10 | </p>
   11 | <p><strong>Importante:</strong> esta pré-triagem é orientativa e não substitui a avaliação clínica presencial.</p>
   12 | 
   13 | {% for item in respostas_revisao %}
   14 |     <section>
   15 |         <h2>{{ item.titulo }}</h2>
   16 |         <p>{{ item.resposta }}</p>
   17 |         {% if item.detalhes %}<p>{{ item.detalhes }}</p>{% endif %}
   18 |         <a href="{% url 'accounts:triagem_pergunta' triagem.id_triagem %}?pergunta={{ item.id }}">Editar resposta</a>
   19 |     </section>
   20 | {% empty %}
   21 |     <p>Nenhuma resposta foi salva ainda.</p>
   22 | {% endfor %}
   23 | 
   24 | <form method="post">
   25 |     {% csrf_token %}
   26 |     <button type="submit" name="acao" value="finalizar">Finalizar e calcular resultado</button>
   27 | </form>
   28 | <p><a href="{% url 'accounts:triagem_pergunta' triagem.id_triagem %}">Voltar à triagem</a></p>
   29 | {% endblock %}
``````

## templates/base.html

Original: [templates/base.html](<C:/Users/lb119/Elo/templates/base.html>).

``````text
    1 | {% load static %}
    2 | {% comment %}
    3 | RESUMO DO ARQUIVO
    4 | =================
    5 | Template-base reutilizado pelas paginas do sistema.
    6 | 
    7 | Ele define a estrutura HTML, a navegacao, as mensagens temporarias e dois blocos
    8 | que as paginas filhas substituem: title e content.
    9 | 
   10 | A navegacao tambem respeita a particularizacao por perfil:
   11 | - todos podem acessar paginas publicas;
   12 | - usuarios autenticados acessam o painel;
   13 | - Hemocentro aprovado recebe atalho para gerenciar o proprio estoque;
   14 | - Administrador recebe atalhos de validacao e painel administrativo.
   15 | {% endcomment %}
   16 | <!doctype html>
   17 | <html lang="pt-br">
   18 | <head>
   19 |     <meta charset="utf-8">
   20 | 
   21 |     <meta name="viewport" content="width=device-width, initial-scale=1">
   22 |     <meta name="description" content="Elo - sistema de doacao de sangue.">
   23 | 
   24 |     <title>{% block title %}Elo{% endblock %}</title>
   25 |     <link rel="stylesheet" href="{% static 'css/elo.css' %}">
   26 |     <link rel="icon" type="image/png" href="{% static 'css/favicon.png' %}">
   27 | </head>
   28 | <body>
   29 |     <header class="site-header">
   30 |         <div class="header-inner">
   31 |             <a class="brand" href="{% url 'accounts:inicio' %}" aria-label="Elo - pagina inicial">
   32 |                 <img class="brand-mark" src="{% static 'css/favicon.png' %}" alt="" aria-hidden="true">
   33 |                 <span class="brand-name">elo</span>
   34 |             </a>
   35 | 
   36 |             <button class="menu-toggle" type="button" aria-label="Abrir menu" aria-expanded="false">
   37 |                 <span></span>
   38 |                 <span></span>
   39 |                 <span></span>
   40 |             </button>
   41 | 
   42 |             <nav class="main-nav" aria-label="Navegacao principal">
   43 |                 {% if user.is_authenticated %}
   44 |                     <a href="{% url 'accounts:dashboard' %}">Painel</a>
   45 |                     <a href="{% url 'accounts:inicio' %}">Início</a>
   46 |                     <a href="{% url 'accounts:compatibilidade_sanguinea' %}">Compatibilidade sanguinea</a>
   47 |                     <a href="{% url 'accounts:estoque_publico' %}">Estoques publicos</a>
   48 | 
   49 |                     {% if user.perfil == "RECEPTOR" %}
   50 |                         <a href="{% url 'accounts:pedido_publicar' %}">Solicitar necessidade</a>
   51 |                     {% endif %}
   52 | 
   53 |                     {% if user.perfil == "HEMOCENTRO" and user.status_validacao == "APROVADO" %}
   54 |                         <a href="{% url 'accounts:painel_pedidos_hemocentro' %}">Analisar solicitações</a>
   55 |                         <a href="{% url 'accounts:estoque_hemocentro' %}">Meu estoque</a>
   56 |                     {% endif %}
   57 | 
   58 |                     {% if user.is_staff or user.is_superuser or user.perfil == "ADMINISTRADOR" %}
   59 |                         <a href="{% url 'accounts:painel_aprovacao_hemocentros' %}">Validar Hemocentros</a>
   60 |                         <a href="{% url 'accounts:painel_validacao_pedidos' %}">Moderar pedidos</a>
   61 |                         <a href="/admin/">Admin</a>
   62 |                     {% endif %}
   63 | 
   64 |                     <span>{{ user.get_short_name }}</span>
   65 | 
   66 |                     <form method="post" action="{% url 'accounts:logout' %}">
   67 |                         {% csrf_token %}
   68 |                         <button type="submit">Sair</button>
   69 |                     </form>
   70 |                 {% else %}
   71 |                     <a href="{% url 'accounts:inicio' %}#sobre">Sobre o elo</a>
   72 |                     <a href="{% url 'accounts:compatibilidade_sanguinea' %}">Compatibilidade sanguinea</a>
   73 |                     <a href="{% url 'accounts:estoque_publico' %}">Estoques publicos</a>
   74 |                     <a href="{% url 'accounts:pedido_publicar' %}">Solicitar necessidade</a>
   75 |                     <a href="{% url 'accounts:login' %}">Entrar</a>
   76 |                     <a class="nav-cta" href="{% url 'accounts:cadastro' %}">Criar conta</a>
   77 |                 {% endif %}
   78 |             </nav>
   79 |         </div>
   80 |     </header>
   81 | 
   82 |     <main>
   83 |         {% if messages %}
   84 |             <div class="messages-wrap">
   85 |                 {% for message in messages %}
   86 |                     <div class="message message-{{ message.tags|default:'info' }}">
   87 |                         {{ message }}
   88 |                     </div>
   89 |                 {% endfor %}
   90 |             </div>
   91 |         {% endif %}
   92 | 
   93 |         {% block content %}{% endblock %}
   94 |     </main>
   95 | 
   96 |     <footer class="site-footer">
   97 |         <div class="footer-inner">
   98 |             <a class="brand brand-footer" href="{% url 'accounts:inicio' %}">
   99 |                 <span class="brand-name">elo</span>
  100 |             </a>
  101 | 
  102 |             <p>Conectando pessoas, hemocentros e vidas.</p>
  103 | 
  104 |             <div class="footer-links">
  105 |                 <a href="{% url 'accounts:inicio' %}#sobre">Sobre o elo</a>
  106 |                 <a href="{% url 'accounts:triagem_apresentacao' %}">Como doar</a>
  107 |                 <a href="{% url 'accounts:estoque_publico' %}">Estoques</a>
  108 |                 {% if user.is_authenticated %}
  109 |                     <a href="{% url 'accounts:dashboard' %}">Meu painel</a>
  110 |                 {% else %}
  111 |                     <a href="{% url 'accounts:login' %}">Entrar</a>
  112 |                 {% endif %}
  113 |             </div>
  114 |         </div>
  115 |     </footer>
  116 | 
  117 |     <script>
  118 |         const menuToggle = document.querySelector(".menu-toggle");
  119 |         const mainNav = document.querySelector(".main-nav");
  120 | 
  121 |         if (menuToggle && mainNav) {
  122 |             menuToggle.addEventListener("click", () => {
  123 |                 const opened = mainNav.classList.toggle("is-open");
  124 |                 menuToggle.setAttribute("aria-expanded", opened ? "true" : "false");
  125 |             });
  126 |         }
  127 |     </script>
  128 | </body>
  129 | </html>
``````

