# Design: organização da experiência Elo e fluxos guiados

## Intenção

Tornar o Elo mais claro e confiável para quem chega pela primeira vez e para
quem já usa a plataforma: a página inicial deve explicar o propósito do
sistema, os formulários devem aceitar somente localidades conhecidas, os
avisos precisam ser percebidos, a triagem deve ser menos rígida na entrada e a
navegação deve permitir avançar, voltar e revisar perguntas sem perder o
andamento.

## Objetivos

- Substituir os campos livres de estado e cidade usados no cadastro e nos
  fluxos públicos por seleções controladas, com validação também no backend.
- Padronizar avisos de sucesso, informação, erro e atenção com a paleta visual
  do site, sem depender somente de texto corrido.
- Permitir iniciar a triagem simplificada sem uma triagem extensa anterior;
  quando uma resposta exigir investigação detalhada, encaminhar para uma nova
  triagem extensa explicando o motivo.
- Exibir a triagem como um fluxo de uma pergunta por página com progresso
  visível e botões de navegação para perguntas já respondidas, mantendo a
  segurança de só persistir respostas validadas.
- Criar uma home pública que explique por que o Elo existe, como ele conecta
  doadores, receptores e hemocentros e quais ações podem ser feitas.
- Organizar o menu, botões, cartões, espaçamentos, responsividade e estados de
  foco dentro de um sistema CSS simples e consistente.
- Fazer os links de Termos de Uso e Política de Privacidade do rodapé abrirem
  modais funcionais em qualquer página que use o layout base.

## Não objetivos

- Não transformar o projeto em uma SPA nem introduzir um framework de frontend.
- Não substituir o motor de regras médicas da triagem ou alterar seus critérios
  clínicos; a mudança é de acesso, navegação e persistência do fluxo.
- Não cadastrar automaticamente todas as cidades brasileiras sem uma fonte
  de dados mantida pelo projeto. A primeira versão usará a lista de localidades
  atendidas pelo catálogo atual, com uma opção de extensão explícita quando o
  negócio fornecer novos municípios.
- Não modificar as alterações já staged em `accounts/views.py`,
  `accounts/validacao_pedido.py` e `templates/base.html` além do que for
  necessário para integrar a entrega; conflitos serão preservados e tratados
  separadamente.

## Restrições e decisões

- A aplicação continuará sendo Django com templates server-rendered e o CSS
  existente em `elo_front/static/css/elo.css`.
- O layout base canônico será `templates/base.html`; o template duplicado em
  `elo_front/templates/base.html` será alinhado somente se ainda for usado no
  carregamento do projeto.
- A localidade terá uma fonte única em módulo Python reutilizável pelos forms
  e pelas views. Estado será um `ChoiceField`; cidade será um `ChoiceField`
  filtrado pelo estado no navegador e validado como par estado/cidade no
  servidor. O valor salvo continuará sendo texto compatível com os modelos
  atuais, evitando migração desnecessária.
- Para pedidos, será incluído estado como campo controlado apenas se o modelo
  atual não conseguir inferi-lo de forma segura; a compatibilidade de dados
  existentes será mantida. O filtro de pedidos também adotará a mesma fonte.
- A triagem simplificada começará com seu próprio fluxo e sem `triagem_base`.
  O cálculo final deverá continuar distinguindo uma base extensa ausente; se o
  resultado depender de histórico detalhado, a triagem simplificada será
  preservada como cancelada no histórico e uma extensa nova começará do início,
  com mensagem explicando o encaminhamento. As respostas não serão copiadas
  entre catálogos com IDs diferentes, evitando transportar informação de forma
  ambígua.
- Os botões de progresso só permitirão saltar para perguntas respondidas ou
  para a pergunta atual. O salto não contornará campos obrigatórios: a pessoa
  poderá voltar e editar, e a conclusão continuará exigindo todas as respostas
  do fluxo calculado.
- Os modais legais ficarão no layout base, com `dialog`, fechamento por botão,
  tecla Escape e clique no backdrop, para que os links do rodapé funcionem em
  todas as telas. O cadastro continuará exibindo os mesmos documentos, sem
  duplicar conteúdo em cada página.
- Os avisos usarão classes derivadas das tags do Django, ícone/contraste visual
  via CSS e `role="status"` ou `role="alert"` conforme o tipo.

## Abordagens consideradas

### A. Evolução integrada do Django atual — escolhida

Adicionar componentes de template, uma fonte de localidades, pequenas
melhorias no serviço de triagem e CSS/JavaScript progressivo. Aproveita as
rotas, modelos, testes e o fluxo de uma pergunta por página já existentes,
reduzindo risco e mantendo o projeto fácil de operar.

### B. Reforma ampla para uma SPA

Mover estado de formulários e triagem para JavaScript. Daria uma navegação mais
fluida, mas duplicaria validação, aumentaria a superfície de segurança e
exigiria uma mudança maior do que a necessidade atual.

### C. Somente ajustes visuais e JavaScript de tela

Resolveria aparência, modais e botões, mas não garantiria a integridade das
localidades no backend nem liberaria corretamente a triagem simplificada.
Também deixaria o banco dependente de textos livres.

A abordagem A foi escolhida porque atende todos os objetivos sem abandonar as
garantias de validação e autorização já presentes.

## Desenho funcional

### Localidade

Criar um catálogo pequeno e explícito de UF/cidades suportadas pelo Elo,
derivado das localidades presentes hoje no catálogo de postos/estoque e dos
hemocentros aprovados pelos testes. O formulário renderiza o estado primeiro e
a cidade depois; um script de poucos linhas desabilita e filtra as cidades
conforme a UF selecionada. No servidor, `clean()` rejeita uma combinação que
não existe no catálogo, inclusive quando a requisição é forjada. Os textos
atuais dos registros antigos continuarão sendo aceitos na leitura e nos
filtros, mas não serão adicionados artificialmente às novas escolhas.

### Triagem

O serviço deixa de bloquear `SIMPLIFICADA` por falta de extensa anterior. A
triagem simplificada começa com fluxo próprio e os mesmos controles de
pergunta/retorno/revisão. A tela de pergunta passa a mostrar uma trilha de
progresso com estados atual, respondido e disponível; cada item respondido
funciona como botão de edição. Ao iniciar, a apresentação informa que a versão
rápida pode pedir uma avaliação detalhada caso a resposta não seja suficiente.

### Home, menu e rodapé

A home terá hero com propósito e CTA principal, seção de como o Elo ajuda,
ações rápidas para triagem/estoques/pedidos, explicação de confiança e uma
FAQ curta. O menu terá agrupamento visual, CTA destacado e comportamento
responsivo sem links duplicados ou quebrados por perfil. O rodapé terá links
organizados e os dois diálogos legais globais.

### CSS e mensagens

Consolidar tokens de cor, tipografia, bordas, sombra e espaçamento em `:root`;
usar cartões, grids e ações com estados hover/focus/disabled; e tratar mobile
com poucos breakpoints. As mensagens aparecerão em uma faixa destacada e
consistente, mantendo o texto acessível e sem esconder erros de validação.

## Arquivos prováveis

- `accounts/localidades.py`: catálogo e validação de UF/cidade.
- `accounts/forms.py`: campos controlados e validação dos pares.
- `accounts/triagem_servico.py`: entrada independente da simplificada e
  cálculo seguro quando não há triagem base.
- `accounts/views.py`: contexto da home, navegação de perguntas e mensagens.
- `accounts/test_*`: testes de localidade, triagem simplificada e renderização.
- `templates/base.html`: menu, mensagens e modais legais globais.
- `templates/accounts/inicio.html`: nova home pública.
- `templates/accounts/cadastro.html`, `pedido_publicar.html` e templates de
  estoque/filtros: selects e layout consistente.
- `templates/accounts/triagem_apresentacao.html` e
  `templates/accounts/triagem_pergunta.html`: entrada e progresso da triagem.
- `elo_front/static/css/elo.css`: sistema visual, estados e responsividade.
- `elo_front/static/js/elo.js` (se necessário): menu, modais e filtro
  dependente de cidades, sem lógica de negócio.

## Critérios de aceitação

- Uma combinação de cidade/UF válida é salva; uma combinação inexistente não é
  aceita pelo form mesmo via POST manual.
- A simplificada pode ser iniciada por um doador sem extensa anterior; respostas
  que exigem detalhes redirecionam para a extensa com mensagem compreensível.
- A triagem mostra progresso e permite voltar a perguntas respondidas por
  botões, sem apagar respostas nem permitir acesso a outro usuário.
- A home explica propósito e oferece caminhos claros para triagem, pedidos e
  estoques; o menu permanece utilizável em desktop e mobile.
- Avisos de erro/sucesso/informação ficam visualmente destacados e coerentes
  com a paleta.
- Os dois links legais do rodapé abrem seus respectivos modais em uma página
  pública e em uma página autenticada, com fechamento acessível.
- A suíte de testes roda com `config.settings_test`; quando o banco PostgreSQL
  local não estiver disponível, isso será reportado separadamente do resultado
  dos testes SQLite.
