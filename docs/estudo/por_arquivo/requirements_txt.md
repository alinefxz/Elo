# requirements.txt: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Documento/configuracao complementar; consulte o conteudo integral.

**Arquivo original:** [requirements.txt](<C:/Users/lb119/Elo/requirements.txt>). As linhas referem-se à cópia desta data.

## Código integral

``````text
# RESUMO
# Cada linha fixa uma dependencia e sua versao. O comando
# ``python -m pip install -r requirements.txt`` recria o mesmo ambiente.

# Dependencia interna usada pelo Django para recursos assincronos.
asgiref==3.12.1

# Framework principal: rotas, ORM, formularios, autenticacao e admin.
Django==5.2.17

# Driver que permite ao Python conversar com PostgreSQL.
psycopg==3.3.4

# Componentes compilados do psycopg para facilitar a instalacao no Windows.
psycopg-binary==3.3.4

# Le as variaveis privadas do arquivo .env.
python-dotenv==1.2.2

# Utilitario usado pelo Django para formatar e separar comandos SQL.
sqlparse==0.6.0

# Base de fusos horarios usada no Windows.
tzdata==2026.3
``````

## Como interpretar este arquivo

Este arquivo contém documentação ou configuração textual. Leia as seções e os valores no bloco integral. Documentação descreve intenção; compare ao código atual. Em requirements, cada pacote e versão determina a instalação; em .gitignore, cada padrão controla o que Git ignora; em .env.example, os nomes mostram as variáveis esperadas, sem precisar ler os segredos do .env real.

