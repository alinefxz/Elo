# elo_front/README-INSTALACAO.txt: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Documento/configuracao complementar; consulte o conteudo integral.

**Arquivo original:** [elo_front/README-INSTALACAO.txt](<C:/Users/lb119/Elo/elo_front/README-INSTALACAO.txt>). As linhas referem-se à cópia desta data.

## Código integral

``````text
ELO — FRONTEND VISUAL

Arquivos incluídos:
- templates/base.html
- templates/accounts/inicio.html
- static/css/elo.css

Como instalar:
1. Faça backup dos arquivos atuais.
2. Copie base.html para:
   templates/base.html
3. Copie inicio.html para:
   templates/accounts/inicio.html
4. Copie elo.css para:
   static/css/elo.css
5. Execute:
   python manage.py runserver

Observações:
- O frontend usa as URLs existentes do app accounts.
- Não altera models.py, views.py ou urls.py.
- A seção de estoque usa estoque_geral que já é enviado pela view inicio.
- O CSS também fornece estilo base para formulários das outras telas.
``````

## Como interpretar este arquivo

Este arquivo contém documentação ou configuração textual. Leia as seções e os valores no bloco integral. Documentação descreve intenção; compare ao código atual. Em requirements, cada pacote e versão determina a instalação; em .gitignore, cada padrão controla o que Git ignora; em .env.example, os nomes mostram as variáveis esperadas, sem precisar ler os segredos do .env real.

