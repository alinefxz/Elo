# .env.example: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Documento/configuracao complementar; consulte o conteudo integral.

**Arquivo original:** [.env.example](<C:/Users/lb119/Elo/.env.example>). As linhas referem-se à cópia desta data.

## Código integral

``````text
# Copie este arquivo para .env e preencha os valores locais.
# Nunca coloque segredos reais neste arquivo de exemplo.

DJANGO_SECRET_KEY="COLE_AQUI_A_CHAVE_GERADA"
DJANGO_DEBUG=True

DB_NAME=elo_db
DB_USER=elo_user
DB_PASSWORD="SENHA_CRIADA_NO_POSTGRESQL"
DB_HOST=127.0.0.1
DB_PORT=5432
``````

## Como interpretar este arquivo

Este arquivo contém documentação ou configuração textual. Leia as seções e os valores no bloco integral. Documentação descreve intenção; compare ao código atual. Em requirements, cada pacote e versão determina a instalação; em .gitignore, cada padrão controla o que Git ignora; em .env.example, os nomes mostram as variáveis esperadas, sem precisar ler os segredos do .env real.

