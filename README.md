# Elo

Sistema web desenvolvido para otimizar a captação de doadores e o controle de demandas hematológicas.

Repositório: <https://github.com/alinefxz/Elo.git>

## Estado atual do projeto

Esta entrega contém o ambiente inicial do sistema e um MVP de autenticação. Já foram implementados:

- projeto Django conectado ao PostgreSQL;
- acesso publico do Visitante para busca de postos, estoque geral e pedidos;
- cadastro de usuários;
- escolha entre Doador, Receptor/Solicitante, Hemocentro e Observador;
- dados iniciais de identificação e localização do usuário;
- login por e-mail e senha;
- logout seguro por requisição POST;
- usuário-base personalizado do Django;
- registro do consentimento LGPD no cadastro;
- painel protegido com conteudo particularizado por perfil;
- painel administrativo do Django;
- migrations versionadas do app `accounts`;
- testes básicos de cadastro, senha e login;
- templates HTML básicos, sem CSS ou Bootstrap.

As senhas não são armazenadas como texto comum. O Django gera e salva um hash seguro na coluna `senha_hash`.

Esta etapa implementa uma conta-base completa, com o perfil escolhido no cadastro. O sistema já guarda CPF ou CNPJ, telefone, nascimento, sexo, cidade e estado. O campo `perfil` já particulariza o painel de Doador, Receptor/Solicitante, Hemocentro, Observador e Administrador. O Visitante nao possui conta: ele usa a pagina inicial publica para consultar postos, estoque geral e pedidos ativos.

## Tecnologias utilizadas

- Python 3.14.3;
- Django 5.2.17;
- PostgreSQL;
- psycopg 3.3.4;
- python-dotenv 1.2.2;
- HTML5;
- Git e GitHub.

## Estrutura principal

```text
Elo/
├── accounts/
│   ├── migrations/       # Alterações versionadas do banco
│   ├── admin.py          # Configuração do painel administrativo
│   ├── forms.py          # Formulários e validações
│   ├── models.py         # Usuário-base e consentimento LGPD
│   ├── tests.py          # Testes automatizados
│   ├── urls.py           # Rotas de autenticação
│   └── views.py          # Regras do cadastro e dashboard
├── config/
│   ├── settings.py       # Configurações do Django e PostgreSQL
│   └── urls.py           # Rotas gerais do projeto
├── templates/
│   ├── base.html
│   └── accounts/
│       ├── cadastro.html
│       ├── dashboard.html
│       └── login.html
├── .env.example          # Modelo das variáveis privadas
├── .gitignore
├── manage.py
└── requirements.txt
```

## Endereços disponíveis

Com o servidor executando:

- página inicial publica do Visitante: <http://127.0.0.1:8000/>;
- cadastro: <http://127.0.0.1:8000/cadastro/>;
- login: <http://127.0.0.1:8000/login/>;
- painel do usuário: <http://127.0.0.1:8000/dashboard/>;
- administração: <http://127.0.0.1:8000/admin/>.

A página inicial fica publica. O dashboard exige autenticação.

## Como instalar em outro computador

### 1. Instalar os programas necessários

Instale:

1. Git;
2. Python 3.14 ou versão compatível com Django 6.1;
3. PostgreSQL e pgAdmin;
4. VS Code, opcional, mas recomendado.

Confirme as instalações no terminal:

```powershell
git --version
python --version
```

### 2. Obter acesso ao GitHub

Se o repositório for privado, a pessoa precisa:

1. ter uma conta no GitHub;
2. receber acesso como colaboradora do repositório;
3. aceitar o convite enviado pelo GitHub;
4. autenticar o Git no computador dela.

Depois, abra o PowerShell na pasta em que deseja guardar o projeto e execute:

```powershell
git clone https://github.com/alinefxz/Elo.git
cd Elo
```

Se o Git solicitar autenticação, use a janela do Git Credential Manager ou faça login pelo navegador. A senha comum da conta GitHub não deve ser usada como senha do Git.

### 3. Criar o ambiente virtual

Dentro da pasta clonada:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Quando o ambiente estiver ativo, o terminal mostrará `(.venv)` no início da linha.

Se o PowerShell bloquear a ativação, execute temporariamente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

No Prompt de Comando (`cmd`), a ativação é:

```bat
.venv\Scripts\activate.bat
```

### 4. Instalar as dependências

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Criar o usuário e o banco PostgreSQL

Abra o pgAdmin e conecte ao servidor PostgreSQL com o usuário administrador `postgres`.

Crie um usuário para a aplicação:

1. expanda `Login/Group Roles`;
2. escolha `Create` > `Login/Group Role`;
3. nome: `elo_user`;
4. defina uma senha própria para aquele computador;
5. em privilégios, habilite `Can login`;
6. salve.

Crie o banco:

1. clique com o botão direito em `Databases`;
2. escolha `Create` > `Database`;
3. nome: `elo_db`;
4. proprietário: `elo_user`;
5. codificação: `UTF8`;
6. salve.

Não é necessário criar as tabelas manualmente. O Django fará isso pelas migrations.

### 6. Criar o arquivo `.env`

Na raiz do projeto, no mesmo nível de `manage.py`, copie `.env.example` e renomeie a cópia para `.env`.

Gere uma chave secreta:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Preencha o `.env`:

```env
DJANGO_SECRET_KEY="COLE_AQUI_A_CHAVE_GERADA"
DJANGO_DEBUG=True

DB_NAME=elo_db
DB_USER=elo_user
DB_PASSWORD="SENHA_CRIADA_NO_POSTGRESQL"
DB_HOST=127.0.0.1
DB_PORT=5432
```

O `.env` contém dados privados e está no `.gitignore`. Nunca envie esse arquivo ao GitHub ou compartilhe a senha do banco.

### 7. Preparar as tabelas

Execute:

```powershell
python manage.py check
python manage.py migrate
```

Em um clone novo não é necessário executar `makemigrations`, porque as migrations numeradas do app `accounts` já fazem parte do repositório. Use `makemigrations` somente depois de alterar os modelos.

### 8. Criar um administrador

```powershell
python manage.py createsuperuser
```

Informe nome, e-mail e senha. Esse usuário poderá acessar `/admin/`.

### 9. Executar o sistema

```powershell
python manage.py runserver
```

Abra <http://127.0.0.1:8000/>. Para encerrar o servidor, pressione `Ctrl + C`.

Se a porta 8000 estiver ocupada:

```powershell
python manage.py runserver 8001
```

Nesse caso, acesse <http://127.0.0.1:8001/>.

## Como trabalhar no projeto diariamente

Abra a pasta clonada e ative o ambiente:

```powershell
cd CAMINHO\PARA\Elo
.\.venv\Scripts\Activate.ps1
git pull origin main
python manage.py runserver
```

Antes de começar uma funcionalidade, recomenda-se criar uma branch:

```powershell
git switch -c feature/nome-da-funcionalidade
```

Depois das alterações:

```powershell
git status
git add .
git commit -m "feat: descreva a alteracao"
git push -u origin feature/nome-da-funcionalidade
```

Depois, abra um Pull Request no GitHub para revisar e unir a branch à `main`.

Para alterações pequenas feitas diretamente na `main`:

```powershell
git pull origin main
git add .
git commit -m "descricao clara da alteracao"
git push origin main
```

Sempre execute `git pull` antes de começar e evite editar o mesmo arquivo ao mesmo tempo que outra pessoa.

## Alterações no banco de dados

Quando alguém alterar `accounts/models.py` ou criar novos modelos:

```powershell
python manage.py makemigrations
python manage.py migrate
```

O arquivo de migration gerado deve ser enviado ao GitHub junto com o código:

```powershell
git add .
git commit -m "feat: atualiza estrutura do banco"
git push
```

Não edite arquivos de migration já aplicados. Para novas mudanças, gere uma migration nova.

## Testes e verificações

Antes de enviar alterações:

```powershell
python manage.py check
python manage.py test
```

O Django cria um banco temporário durante os testes. Se aparecer `permission denied to create database`, o administrador local do PostgreSQL pode conceder permissão de criação de banco ao usuário de desenvolvimento:

```sql
ALTER ROLE elo_user CREATEDB;
```

Essa permissão é apropriada apenas para desenvolvimento local, não para um servidor de produção.

## Funcionamento do usuário, cadastro e login

- `accounts/models.py` define `Usuario` e `ConsentimentoLGPD`;
- o e-mail é o identificador usado no login;
- `accounts/forms.py` contém o formulário de cadastro e suas validações;
- o cadastro público permite escolher Doador, Receptor, Hemocentro ou Observador;
- Hemocentro informa CNPJ; os outros perfis informam CPF;
- CPF e CNPJ são salvos somente com números;
- a sigla do estado é salva em letras maiúsculas;
- a senha precisa ter pelo menos oito caracteres, letras e números;
- `set_password()` transforma a senha em hash antes de salvar;
- `accounts/views.py` grava usuário e consentimento na mesma transação;
- após o cadastro, o usuário entra automaticamente;
- `login_required` bloqueia o dashboard para visitantes;
- o logout usa `POST` e proteção CSRF;
- as sessões são administradas pelo próprio Django.

O objetivo desta entrega termina no cadastro e na autenticação da conta-base. A classificação inicial já existe no model e no formulário, mas ainda não altera permissões nem mostra painéis diferentes. A próxima pessoa deverá implementar, para cada tipo de usuário:

- campos adicionais necessários;
- permissões e restrições de acesso;
- formulários específicos;
- páginas e painéis próprios;
- validações e regras de negócio;
- relacionamento com tabelas como doadores e hemocentros.

## Tabelas principais

- `usuarios`: dados da conta, documento, localização e perfil inicial;
- `consentimentos_lgpd`: aceite, versão do termo, data e IP;
- `django_session`: sessões de usuários autenticados;
- tabelas internas do Django: permissões, grupos, migrations e administração.

## Arquivos que nunca devem ir ao GitHub

O `.gitignore` deve continuar ignorando:

```gitignore
.venv/
.env
__pycache__/
*.pyc
db.sqlite3
```

Nunca envie senhas, chaves secretas ou o conteúdo real do `.env`.

## Problemas comuns

### `KeyError: DJANGO_SECRET_KEY`

O `.env` não existe, está no local errado ou a primeira linha está inválida. Ele deve ficar ao lado de `manage.py`.

### `password authentication failed for user elo_user`

A senha em `DB_PASSWORD` não corresponde à senha criada no PostgreSQL.

### `connection refused`

O serviço PostgreSQL pode estar desligado ou usando outra porta. Confirme `DB_HOST` e `DB_PORT`.

### `database elo_db does not exist`

Crie o banco `elo_db` pelo pgAdmin e defina `elo_user` como proprietário.

### `relation does not exist`

Execute:

```powershell
python manage.py migrate
```

### Erro ao ativar o ambiente virtual

Confirme que está na raiz do projeto e execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## O que ainda não foi implementado

Esta é uma primeira entrega. Permanecem para etapas futuras:

- identidade visual e CSS;
- recuperação de senha;
- confirmação de e-mail;
- bloqueio após tentativas excessivas de login;
- regras e permissões completas dos perfis Doador, Receptor, Hemocentro, Observador e Administrador;
- edição e páginas específicas de cada perfil;
- cadastro e aprovação completa de hemocentros;
- triagem;
- estoque de sangue;
- pedidos e demandas;
- notificações;
- mapas e localização;
- Supabase e recursos em tempo real;
- Gemini API;
- PWA.

Antes de iniciar uma dessas funcionalidades, crie uma branch e documente quaisquer novas variáveis no `.env.example`.

## Situação verificada em 14/08/2026

- repositório local conectado a `https://github.com/alinefxz/Elo.git`;
- branch principal: `main`;
- migrations do app `accounts` aplicadas;
- `python manage.py check` executado sem erros;
- banco local: `elo_db`;
- usuário local do banco: `elo_user`.
