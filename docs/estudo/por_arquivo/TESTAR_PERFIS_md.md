# TESTAR_PERFIS.md: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Documento/configuracao complementar; consulte o conteudo integral.

**Arquivo original:** [TESTAR_PERFIS.md](<C:/Users/lb119/Elo/TESTAR_PERFIS.md>). As linhas referem-se à cópia desta data.

## Código integral

``````text
# Testar os perfis do Elo

No ambiente local com `DEBUG=True`, execute:

```powershell
.\.venv\Scripts\python.exe manage.py criar_perfis_teste
```

As novas contas usam a senha **EloTeste2026!**. Para escolher outra senha, use
`--senha 'SuaSenhaDeTeste'`. Repetir o comando preserva todas as contas existentes,
inclusive suas senhas, triagens, consentimentos e alteracoes feitas durante os testes.
O comando nao altera regras, nao cria estoque ou pedidos e nao envia notificacoes.
Nao exige uma nova migration; as migrations existentes devem estar aplicadas.

Abra o sistema no endereco do seu servidor local e entre com uma conta por vez.
Para testar dois perfis ao mesmo tempo, use navegadores diferentes ou janela anonima.

| Login | Situacao inicial e o que verificar |
| --- | --- |
| `doador@teste.elo.test` | O−, triagem apta e convocacao autorizada. Testar triagem e alertas compativeis. |
| `doador-inapto@teste.elo.test` | O−, ultima triagem inapta. Nao deve receber convocacoes. |
| `doador-sem-consentimento@teste.elo.test` | O−, apto, sem aceite de convocacao. Nao recebe alertas ate autorizar no painel. |
| `receptor@teste.elo.test` | Criar solicitacao e acompanhar seus pedidos. |
| `observador@teste.elo.test` | Consultar informacoes; verificar bloqueio das funcoes restritas. |
| `administrador@teste.elo.test` | Validar hemocentros, moderar pedidos e consultar auditoria em `/admin/`. Conta tecnica com permissoes completas somente para testes locais. |
| `hemocentro-pendente@teste.elo.test` | Aguardar analise; publicacao bloqueada. Use esta conta para testar aprovacao pelo administrador. |
| `hemocentro-aprovado@teste.elo.test` | Cadastrar e atualizar estoque; analisar pedidos destinados a ele. |
| `hemocentro-recusado@teste.elo.test` | Conferir mensagem de recusa e bloqueio de publicacao. |
| `hemocentro-correcao@teste.elo.test` | Conferir estado de correcao e bloqueio de publicacao. |

As triagens e consentimentos dessas contas sao dados sinteticos para testes,
nao avaliacoes ou aceites de pessoas reais. Os estados dos hemocentros sao definidos
diretamente pelo comando; o historico de validacao sera produzido ao executar as acoes reais.

## Roteiro de alerta e notificacoes

1. Entre como hemocentro aprovado. Cadastre estoque O− com minimo 10,
   critico 5 e quantidade inicial 12.
2. Atualize a quantidade para 7: o estoque fica baixo, sem novo alerta.
3. Atualize para 5: o estoque fica critico e deve notificar o doador apto autorizado.
4. Entre com os tres doadores: apenas `doador@teste.elo.test` deve receber esse alerta.
5. Na central, confira data, titulo, mensagem e **Ver estoque**. Clique em
   **Marcar como lida**; o aviso continua no historico como lido.
6. Teste um pedido O−: Receptor solicita, Hemocentro responsavel publica.
   A convocacao compartilha com o estoque o limite configurado (padrao: uma em 24 horas),
   inclusive quando o alerta anterior foi lido. Nao espere outro aviso dentro desse limite.

Visitante e testado sem login. Nenhuma conta e necessaria.
``````

## Como interpretar este arquivo

Este arquivo contém documentação ou configuração textual. Leia as seções e os valores no bloco integral. Documentação descreve intenção; compare ao código atual. Em requirements, cada pacote e versão determina a instalação; em .gitignore, cada padrão controla o que Git ignora; em .env.example, os nomes mostram as variáveis esperadas, sem precisar ler os segredos do .env real.

