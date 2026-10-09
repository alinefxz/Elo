# config/settings.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Configuracao de apps, banco, middleware, templates e autenticacao.

**Arquivo original:** [config/settings.py](<C:/Users/lb119/Elo/config/settings.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""
RESUMO DO ARQUIVO
=================
Este e o arquivo central de configuracao do projeto Django.

Ele informa quais apps estao ativos, como as requisicoes sao processadas, onde
ficam os templates, como conectar ao PostgreSQL, qual e o model de usuario e
para onde o login/logout deve redirecionar.

Dados secretos nao ficam escritos aqui. ``python-dotenv`` le o arquivo ``.env``
da raiz e disponibiliza seus valores por meio de ``os.environ``.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# __file__ e o caminho deste settings.py. parent.parent sobe de config/ para a
# raiz do projeto, onde ficam manage.py, templates/ e .env.
BASE_DIR = Path(__file__).resolve().parent.parent

# Le o arquivo .env e coloca suas variaveis no ambiente deste processo Python.
# O .env real esta no .gitignore porque possui chave e senha locais.
load_dotenv(BASE_DIR / ".env")


# SECRET_KEY participa de assinaturas criptograficas do Django, inclusive de
# sessoes e tokens. os.environ[...] gera erro imediatamente se ela estiver
# ausente; isso e melhor do que executar o sistema com uma chave insegura.
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# getenv recebe texto. A comparacao converte "True" em booleano True.
# DEBUG mostra erros detalhados e deve ser False quando o sistema for publicado.
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"

# Hosts aceitos pelo Django. Estes dois cobrem o desenvolvimento local.
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Cada item ativa um conjunto de recursos dentro do projeto.
INSTALLED_APPS = [
    # Painel administrativo em /admin/.
    "django.contrib.admin",
    # Autenticacao, hash de senha, grupos e permissoes.
    "django.contrib.auth",
    # Identifica models; e usado por permissoes e pelo admin.
    "django.contrib.contenttypes",
    # Salva sessoes de login no banco.
    "django.contrib.sessions",
    # Permite mensagens temporarias, como "Cadastro realizado".
    "django.contrib.messages",
    # Gerencia CSS, JavaScript e imagens quando forem adicionados.
    "django.contrib.staticfiles",
    # App criado pelo projeto: usuario, dados iniciais, cadastro, login e LGPD.
    "accounts",
]


# Middlewares executam ao redor de cada requisicao e resposta, na ordem listada.
MIDDLEWARE = [
    # Adiciona protecoes e cabecalhos de seguranca.
    "django.middleware.security.SecurityMiddleware",
    # Carrega request.session; necessario para manter o login.
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Comportamentos HTTP comuns, como normalizacao de URLs.
    "django.middleware.common.CommonMiddleware",
    # Verifica o token CSRF dos formularios POST.
    "django.middleware.csrf.CsrfViewMiddleware",
    # Usa a sessao para preencher request.user.
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "accounts.auditoria.AuditoriaAcessosMiddleware",
    # Disponibiliza mensagens temporarias nos templates.
    "django.contrib.messages.middleware.MessageMiddleware",
    # Ajuda a impedir que o site seja embutido em iframe malicioso.
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Primeiro arquivo de URLs consultado para qualquer endereco do projeto.
ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        # Motor de templates nativo do Django.
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        # Procura templates globais na pasta templates/ da raiz.
        "DIRS": [BASE_DIR / "templates"],

        # Tambem permite templates dentro da pasta de cada app.
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # Disponibiliza request no HTML.
                "django.template.context_processors.request",
                # Disponibiliza user e permissoes no HTML.
                "django.contrib.auth.context_processors.auth",
                # Disponibiliza a lista messages no HTML.
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# Ponto de entrada usado por servidores web baseados em WSGI.
WSGI_APPLICATION = "config.wsgi.application"


# CONEXAO COM O POSTGRESQL
# -----------------------
# O Django ORM transforma operacoes Python em SQL. Exemplo:
# Usuario.objects.filter(email=...) vira um SELECT na tabela usuarios.
#
# Os valores abaixo correspondem ao banco e ao Login/Group Role criados no
# pgAdmin. Eles sao lidos do .env para que cada computador use sua propria senha.
DATABASES = {
    "default": {
        # Backend oficial do Django para PostgreSQL, usando psycopg.
        "ENGINE": "django.db.backends.postgresql",

        # Nome do banco criado no pgAdmin, normalmente elo_db.
        "NAME": os.environ["DB_NAME"],

        # Usuario do PostgreSQL que e proprietario do banco, normalmente elo_user.
        "USER": os.environ["DB_USER"],

        # Senha do elo_user. Nunca deve ser enviada ao GitHub.
        "PASSWORD": os.environ["DB_PASSWORD"],

        # 127.0.0.1 significa que o PostgreSQL esta no mesmo computador.
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),

        # 5432 e a porta padrao do PostgreSQL.
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}


# O UserCreationForm consulta estes validadores antes de aceitar uma senha.
AUTH_PASSWORD_VALIDATORS = [
    {
        # Evita senha muito parecida com nome ou e-mail.
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        # Exige o comprimento minimo definido pelo Django (8 por padrao).
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        # Bloqueia senhas conhecidas por serem muito comuns.
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        # Impede senha formada somente por numeros.
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# Traduz mensagens internas e define como datas sao apresentadas.
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Limite conjunto de alertas internos de estoque e pedidos por doador.
CONVOCACAO_INTERVALO_HORAS = 24
CONVOCACAO_LIMITE_NOTIFICACOES = 1
CONVOCACAO_VERSAO_CONSENTIMENTO = "1.0"


# Prefixo de URL reservado para futuros arquivos CSS, JS e imagens.
STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "elo_front" / "static",
]

# Enquanto nao existe servidor de e-mail, qualquer mensagem enviada pelo Django
# aparece no terminal. Isso evita disparos reais durante o desenvolvimento.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Tipo padrao de chave primaria quando um model nao declara a propria chave.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Substitui o auth.User padrao pelo Usuario concreto de accounts/models.py.
# Esta configuracao foi definida antes da primeira migration, como recomendado.
AUTH_USER_MODEL = "accounts.Usuario"

# Rotas usadas automaticamente por login_required, LoginView e LogoutView.
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:dashboard"
LOGOUT_REDIRECT_URL = "accounts:login"
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 12

```python
"""
RESUMO DO ARQUIVO
=================
Este e o arquivo central de configuracao do projeto Django.

Ele informa quais apps estao ativos, como as requisicoes sao processadas, onde
ficam os templates, como conectar ao PostgreSQL, qual e o model de usuario e
para onde o login/logout deve redirecionar.

Dados secretos nao ficam escritos aqui. ``python-dotenv`` le o arquivo ``.env``
da raiz e disponibiliza seus valores por meio de ``os.environ``.
"""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### Import — linhas 14 a 14

```python
import os
```

**Explicação deste trecho:**

**Linha 14 — Import** (nível 0 do bloco).

Importa módulos: `os`.

### ImportFrom — linhas 15 a 15

```python
from pathlib import Path
```

**Explicação deste trecho:**

**Linha 15 — ImportFrom** (nível 0 do bloco).

Importa de `pathlib` os nomes `Path`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 17 a 17

```python
from dotenv import load_dotenv
```

**Explicação deste trecho:**

**Linha 17 — ImportFrom** (nível 0 do bloco).

Importa de `dotenv` os nomes `load_dotenv`. Pontos iniciais indicam importação relativa ao pacote.

### Assign — linhas 22 a 22

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```

**Explicação deste trecho:**

**Linha 22 — Assign** (nível 0 do bloco).

Associa `BASE_DIR` a o atributo `parent` de `Path(__file__).resolve().parent`.

### Expr — linhas 26 a 26

```python
load_dotenv(BASE_DIR / ".env")
```

**Explicação deste trecho:**

**Linha 26 — Expr** (nível 0 do bloco).

Executa a chamada `load_dotenv`; argumentos posicionais: `BASE_DIR / '.env'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

### Assign — linhas 32 a 32

```python
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
```

**Explicação deste trecho:**

**Linha 32 — Assign** (nível 0 do bloco).

Associa `SECRET_KEY` a o item ou recorte `'DJANGO_SECRET_KEY'` de `os.environ`.

### Assign — linhas 36 a 36

```python
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
```

**Explicação deste trecho:**

**Linha 36 — Assign** (nível 0 do bloco).

Associa `DEBUG` a a comparação `os.getenv('DJANGO_DEBUG', 'False').lower()` igual a `'true'`.

### Assign — linhas 39 a 39

```python
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
```

**Explicação deste trecho:**

**Linha 39 — Assign** (nível 0 do bloco).

Associa `ALLOWED_HOSTS` a uma coleção List com 2 itens, na expressão `['127.0.0.1', 'localhost']`.

### Assign — linhas 43 a 58

```python
INSTALLED_APPS = [
    # Painel administrativo em /admin/.
    "django.contrib.admin",
    # Autenticacao, hash de senha, grupos e permissoes.
    "django.contrib.auth",
    # Identifica models; e usado por permissoes e pelo admin.
    "django.contrib.contenttypes",
    # Salva sessoes de login no banco.
    "django.contrib.sessions",
    # Permite mensagens temporarias, como "Cadastro realizado".
    "django.contrib.messages",
    # Gerencia CSS, JavaScript e imagens quando forem adicionados.
    "django.contrib.staticfiles",
    # App criado pelo projeto: usuario, dados iniciais, cadastro, login e LGPD.
    "accounts",
]
```

**Explicação deste trecho:**

**Linha 43 — Assign** (nível 0 do bloco).

Associa `INSTALLED_APPS` a uma coleção List com 7 itens, na expressão `['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'accounts']`.

### Assign — linhas 62 a 78

```python
MIDDLEWARE = [
    # Adiciona protecoes e cabecalhos de seguranca.
    "django.middleware.security.SecurityMiddleware",
    # Carrega request.session; necessario para manter o login.
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Comportamentos HTTP comuns, como normalizacao de URLs.
    "django.middleware.common.CommonMiddleware",
    # Verifica o token CSRF dos formularios POST.
    "django.middleware.csrf.CsrfViewMiddleware",
    # Usa a sessao para preencher request.user.
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "accounts.auditoria.AuditoriaAcessosMiddleware",
    # Disponibiliza mensagens temporarias nos templates.
    "django.contrib.messages.middleware.MessageMiddleware",
    # Ajuda a impedir que o site seja embutido em iframe malicioso.
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

**Explicação deste trecho:**

**Linha 62 — Assign** (nível 0 do bloco).

Associa `MIDDLEWARE` a uma coleção List com 8 itens, na expressão `['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'accounts.auditoria.AuditoriaAcessosMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware']`.

### Assign — linhas 82 a 82

```python
ROOT_URLCONF = "config.urls"
```

**Explicação deste trecho:**

**Linha 82 — Assign** (nível 0 do bloco).

Associa `ROOT_URLCONF` a o valor literal `'config.urls'`.

### Assign — linhas 85 a 106

```python
TEMPLATES = [
    {
        # Motor de templates nativo do Django.
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        # Procura templates globais na pasta templates/ da raiz.
        "DIRS": [BASE_DIR / "templates"],

        # Tambem permite templates dentro da pasta de cada app.
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # Disponibiliza request no HTML.
                "django.template.context_processors.request",
                # Disponibiliza user e permissoes no HTML.
                "django.contrib.auth.context_processors.auth",
                # Disponibiliza a lista messages no HTML.
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

**Explicação deste trecho:**

**Linha 85 — Assign** (nível 0 do bloco).

Associa `TEMPLATES` a uma coleção List com 1 itens, na expressão `[{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]`.

### Assign — linhas 110 a 110

```python
WSGI_APPLICATION = "config.wsgi.application"
```

**Explicação deste trecho:**

**Linha 110 — Assign** (nível 0 do bloco).

Associa `WSGI_APPLICATION` a o valor literal `'config.wsgi.application'`.

### Assign — linhas 120 a 140

```python
DATABASES = {
    "default": {
        # Backend oficial do Django para PostgreSQL, usando psycopg.
        "ENGINE": "django.db.backends.postgresql",

        # Nome do banco criado no pgAdmin, normalmente elo_db.
        "NAME": os.environ["DB_NAME"],

        # Usuario do PostgreSQL que e proprietario do banco, normalmente elo_user.
        "USER": os.environ["DB_USER"],

        # Senha do elo_user. Nunca deve ser enviada ao GitHub.
        "PASSWORD": os.environ["DB_PASSWORD"],

        # 127.0.0.1 significa que o PostgreSQL esta no mesmo computador.
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),

        # 5432 e a porta padrao do PostgreSQL.
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}
```

**Explicação deste trecho:**

**Linha 120 — Assign** (nível 0 do bloco).

Associa `DATABASES` a um dicionário de 1 entradas; as chaves dão nome aos valores associados.

- Chave `'default'`: recebe um dicionário de 6 entradas; as chaves dão nome aos valores associados.

### Assign — linhas 144 a 173

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        # Evita senha muito parecida com nome ou e-mail.
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        # Exige o comprimento minimo definido pelo Django (8 por padrao).
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        # Bloqueia senhas conhecidas por serem muito comuns.
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        # Impede senha formada somente por numeros.
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]
```

**Explicação deste trecho:**

**Linha 144 — Assign** (nível 0 do bloco).

Associa `AUTH_PASSWORD_VALIDATORS` a uma coleção List com 4 itens, na expressão `[{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}, {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]`.

### Assign — linhas 177 a 177

```python
LANGUAGE_CODE = "pt-br"
```

**Explicação deste trecho:**

**Linha 177 — Assign** (nível 0 do bloco).

Associa `LANGUAGE_CODE` a o valor literal `'pt-br'`.

### Assign — linhas 178 a 178

```python
TIME_ZONE = "America/Sao_Paulo"
```

**Explicação deste trecho:**

**Linha 178 — Assign** (nível 0 do bloco).

Associa `TIME_ZONE` a o valor literal `'America/Sao_Paulo'`.

### Assign — linhas 179 a 179

```python
USE_I18N = True
```

**Explicação deste trecho:**

**Linha 179 — Assign** (nível 0 do bloco).

Associa `USE_I18N` a o valor literal `True`.

### Assign — linhas 180 a 180

```python
USE_TZ = True
```

**Explicação deste trecho:**

**Linha 180 — Assign** (nível 0 do bloco).

Associa `USE_TZ` a o valor literal `True`.

### Assign — linhas 183 a 183

```python
CONVOCACAO_INTERVALO_HORAS = 24
```

**Explicação deste trecho:**

**Linha 183 — Assign** (nível 0 do bloco).

Associa `CONVOCACAO_INTERVALO_HORAS` a o valor literal `24`.

### Assign — linhas 184 a 184

```python
CONVOCACAO_LIMITE_NOTIFICACOES = 1
```

**Explicação deste trecho:**

**Linha 184 — Assign** (nível 0 do bloco).

Associa `CONVOCACAO_LIMITE_NOTIFICACOES` a o valor literal `1`.

### Assign — linhas 185 a 185

```python
CONVOCACAO_VERSAO_CONSENTIMENTO = "1.0"
```

**Explicação deste trecho:**

**Linha 185 — Assign** (nível 0 do bloco).

Associa `CONVOCACAO_VERSAO_CONSENTIMENTO` a o valor literal `'1.0'`.

### Assign — linhas 189 a 189

```python
STATIC_URL = "static/"
```

**Explicação deste trecho:**

**Linha 189 — Assign** (nível 0 do bloco).

Associa `STATIC_URL` a o valor literal `'static/'`.

### Assign — linhas 191 a 193

```python
STATICFILES_DIRS = [
    BASE_DIR / "elo_front" / "static",
]
```

**Explicação deste trecho:**

**Linha 191 — Assign** (nível 0 do bloco).

Associa `STATICFILES_DIRS` a uma coleção List com 1 itens, na expressão `[BASE_DIR / 'elo_front' / 'static']`.

### Assign — linhas 197 a 197

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

**Explicação deste trecho:**

**Linha 197 — Assign** (nível 0 do bloco).

Associa `EMAIL_BACKEND` a o valor literal `'django.core.mail.backends.console.EmailBackend'`.

### Assign — linhas 200 a 200

```python
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

**Explicação deste trecho:**

**Linha 200 — Assign** (nível 0 do bloco).

Associa `DEFAULT_AUTO_FIELD` a o valor literal `'django.db.models.BigAutoField'`.

### Assign — linhas 205 a 205

```python
AUTH_USER_MODEL = "accounts.Usuario"
```

**Explicação deste trecho:**

**Linha 205 — Assign** (nível 0 do bloco).

Associa `AUTH_USER_MODEL` a o valor literal `'accounts.Usuario'`.

### Assign — linhas 208 a 208

```python
LOGIN_URL = "accounts:login"
```

**Explicação deste trecho:**

**Linha 208 — Assign** (nível 0 do bloco).

Associa `LOGIN_URL` a o valor literal `'accounts:login'`.

### Assign — linhas 209 a 209

```python
LOGIN_REDIRECT_URL = "accounts:dashboard"
```

**Explicação deste trecho:**

**Linha 209 — Assign** (nível 0 do bloco).

Associa `LOGIN_REDIRECT_URL` a o valor literal `'accounts:dashboard'`.

### Assign — linhas 210 a 210

```python
LOGOUT_REDIRECT_URL = "accounts:login"
```

**Explicação deste trecho:**

**Linha 210 — Assign** (nível 0 do bloco).

Associa `LOGOUT_REDIRECT_URL` a o valor literal `'accounts:login'`.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 20: `# __file__ e o caminho deste settings.py. parent.parent sobe de config/ para a`
- Linha 21: `# raiz do projeto, onde ficam manage.py, templates/ e .env.`
- Linha 24: `# Le o arquivo .env e coloca suas variaveis no ambiente deste processo Python.`
- Linha 25: `# O .env real esta no .gitignore porque possui chave e senha locais.`
- Linha 29: `# SECRET_KEY participa de assinaturas criptograficas do Django, inclusive de`
- Linha 30: `# sessoes e tokens. os.environ[...] gera erro imediatamente se ela estiver`
- Linha 31: `# ausente; isso e melhor do que executar o sistema com uma chave insegura.`
- Linha 34: `# getenv recebe texto. A comparacao converte "True" em booleano True.`
- Linha 35: `# DEBUG mostra erros detalhados e deve ser False quando o sistema for publicado.`
- Linha 38: `# Hosts aceitos pelo Django. Estes dois cobrem o desenvolvimento local.`
- Linha 42: `# Cada item ativa um conjunto de recursos dentro do projeto.`
- Linha 44: `# Painel administrativo em /admin/.`
- Linha 46: `# Autenticacao, hash de senha, grupos e permissoes.`
- Linha 48: `# Identifica models; e usado por permissoes e pelo admin.`
- Linha 50: `# Salva sessoes de login no banco.`
- Linha 52: `# Permite mensagens temporarias, como "Cadastro realizado".`
- Linha 54: `# Gerencia CSS, JavaScript e imagens quando forem adicionados.`
- Linha 56: `# App criado pelo projeto: usuario, dados iniciais, cadastro, login e LGPD.`
- Linha 61: `# Middlewares executam ao redor de cada requisicao e resposta, na ordem listada.`
- Linha 63: `# Adiciona protecoes e cabecalhos de seguranca.`
- Linha 65: `# Carrega request.session; necessario para manter o login.`
- Linha 67: `# Comportamentos HTTP comuns, como normalizacao de URLs.`
- Linha 69: `# Verifica o token CSRF dos formularios POST.`
- Linha 71: `# Usa a sessao para preencher request.user.`
- Linha 74: `# Disponibiliza mensagens temporarias nos templates.`
- Linha 76: `# Ajuda a impedir que o site seja embutido em iframe malicioso.`
- Linha 81: `# Primeiro arquivo de URLs consultado para qualquer endereco do projeto.`
- Linha 87: `# Motor de templates nativo do Django.`
- Linha 90: `# Procura templates globais na pasta templates/ da raiz.`
- Linha 93: `# Tambem permite templates dentro da pasta de cada app.`
- Linha 97: `# Disponibiliza request no HTML.`
- Linha 99: `# Disponibiliza user e permissoes no HTML.`
- Linha 101: `# Disponibiliza a lista messages no HTML.`
- Linha 109: `# Ponto de entrada usado por servidores web baseados em WSGI.`
- Linha 113: `# CONEXAO COM O POSTGRESQL`
- Linha 114: `# -----------------------`
- Linha 115: `# O Django ORM transforma operacoes Python em SQL. Exemplo:`
- Linha 116: `# Usuario.objects.filter(email=...) vira um SELECT na tabela usuarios.`
- Linha 117: `#`
- Linha 118: `# Os valores abaixo correspondem ao banco e ao Login/Group Role criados no`
- Linha 119: `# pgAdmin. Eles sao lidos do .env para que cada computador use sua propria senha.`
- Linha 122: `# Backend oficial do Django para PostgreSQL, usando psycopg.`
- Linha 125: `# Nome do banco criado no pgAdmin, normalmente elo_db.`
- Linha 128: `# Usuario do PostgreSQL que e proprietario do banco, normalmente elo_user.`
- Linha 131: `# Senha do elo_user. Nunca deve ser enviada ao GitHub.`
- Linha 134: `# 127.0.0.1 significa que o PostgreSQL esta no mesmo computador.`
- Linha 137: `# 5432 e a porta padrao do PostgreSQL.`
- Linha 143: `# O UserCreationForm consulta estes validadores antes de aceitar uma senha.`
- Linha 146: `# Evita senha muito parecida com nome ou e-mail.`
- Linha 153: `# Exige o comprimento minimo definido pelo Django (8 por padrao).`
- Linha 160: `# Bloqueia senhas conhecidas por serem muito comuns.`
- Linha 167: `# Impede senha formada somente por numeros.`
- Linha 176: `# Traduz mensagens internas e define como datas sao apresentadas.`
- Linha 182: `# Limite conjunto de alertas internos de estoque e pedidos por doador.`
- Linha 188: `# Prefixo de URL reservado para futuros arquivos CSS, JS e imagens.`
- Linha 195: `# Enquanto nao existe servidor de e-mail, qualquer mensagem enviada pelo Django`
- Linha 196: `# aparece no terminal. Isso evita disparos reais durante o desenvolvimento.`
- Linha 199: `# Tipo padrao de chave primaria quando um model nao declara a propria chave.`
- Linha 203: `# Substitui o auth.User padrao pelo Usuario concreto de accounts/models.py.`
- Linha 204: `# Esta configuracao foi definida antes da primeira migration, como recomendado.`
- Linha 207: `# Rotas usadas automaticamente por login_required, LoginView e LogoutView.`

