# .gitignore: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Documento/configuracao complementar; consulte o conteudo integral.

**Arquivo original:** [.gitignore](<C:/Users/lb119/Elo/.gitignore>). As linhas referem-se à cópia desta data.

## Código integral

``````text
# Ambiente virtual: contem pacotes instalados localmente e pode ser recriado.
.venv/

# Segredos locais, incluindo chave Django e senha do PostgreSQL.
.env

# Cache de bytecode gerado automaticamente pelo Python.
__pycache__/
*.pyc

# Banco SQLite padrao; este projeto usa PostgreSQL.
db.sqlite3
``````

## Como interpretar este arquivo

Este arquivo contém documentação ou configuração textual. Leia as seções e os valores no bloco integral. Documentação descreve intenção; compare ao código atual. Em requirements, cada pacote e versão determina a instalação; em .gitignore, cada padrão controla o que Git ignora; em .env.example, os nomes mostram as variáveis esperadas, sem precisar ler os segredos do .env real.

