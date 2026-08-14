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


# Prefixo de URL reservado para futuros arquivos CSS, JS e imagens.
STATIC_URL = "static/"

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
