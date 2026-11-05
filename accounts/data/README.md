# Municípios brasileiros

`municipios_ibge.json` é um snapshot da API oficial de localidades do IBGE,
consultada em **05/11/2026**. A resposta contém 5.571 municípios nas 27 UFs.
Cada município aparece exclusivamente em sua UF; nomes iguais em estados
diferentes são preservados. Brasília é incluída conforme retornada pela API.

Fonte: <https://servicodados.ibge.gov.br/api/v1/localidades/municipios?orderBy=nome>

Documentação: <https://servicodados.ibge.gov.br/api/docs/localidades>

O JSON guarda a origem e o instante da consulta em UTC, além do agrupamento
`municipios_por_estado`. O carregamento é local e não depende de rede ou de
informações das contas cadastradas. A aplicação não faz consultas externas
durante o preenchimento de formulários.

Para atualizar, baixe novamente a resposta oficial em
`tmp/municipios_ibge_original.json` e execute `python scripts/importar_municipios_ibge.py`.
O normalizador utiliza `microrregiao.mesorregiao.UF.sigla` ou, para municípios
mais recentes, `regiao-imediata.regiao-intermediaria.UF.sigla`. Ele rejeita
respostas incompletas, municípios sem UF e identificadores ou nomes duplicados
na mesma UF antes de substituir o catálogo versionado.
