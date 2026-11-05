# Elo UX e fluxos guiados Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Organizar a experiência pública e autenticada do Elo, controlar localidades, liberar a triagem simplificada com segurança e melhorar navegação, avisos, menu e documentos legais.

**Architecture:** Manter Django server-rendered, usando uma fonte Python única para localidades, validação no backend e JavaScript pequeno apenas para interação progressiva (menu, modais e filtro dependente de cidade). A triagem continuará persistindo respostas no modelo existente e ganhará navegação explícita para perguntas respondidas, sem mover regras médicas para o frontend.

**Tech Stack:** Django, templates HTML, CSS existente em `elo_front/static/css/elo.css`, JavaScript vanilla, suíte `django.test` com `config.settings_test`/SQLite em memória.

**Spec:** `docs/superpowers/specs/2026-11-04-elo-ux-fluxos-design.md`

## Global Constraints

- A aplicação continuará sendo Django com templates server-rendered e o CSS existente em `elo_front/static/css/elo.css`.
- O layout base canônico será `templates/base.html`.
- Estado será um `ChoiceField`; cidade será filtrada pelo estado no navegador e validada como par estado/cidade no servidor.
- A triagem simplificada começará sem `triagem_base`; quando exigir investigação detalhada, será preservada como cancelada e uma extensa nova começará do início.
- Os botões de progresso só permitirão saltar para perguntas respondidas ou para a pergunta atual.
- Os modais legais ficarão no layout base e funcionarão em todas as telas que o estendem.
- As alterações já staged em `accounts/views.py`, `accounts/validacao_pedido.py` e `templates/base.html` pertencem ao usuário e não podem ser descartadas.

## Review Focus

- POST forjado com cidade válida e UF incompatível deve ser rejeitado pelo backend; teste em Task 1.
- Usuário com triagem simplificada sem extensa anterior deve iniciar e concluir uma resposta segura sem erro de `triagem_base`; testes em Task 2.
- Acesso a botão de progresso de outra triagem/usuário ou a pergunta não respondida deve continuar bloqueado; testes em Task 3.
- Rodapé deve abrir o modal correto em uma página que não seja cadastro, e Escape/backdrop devem fechar; teste em Task 4.
- Menu e home devem manter CTAs e links válidos para visitante e usuário autenticado sem alterar as autorizações existentes; testes em Tasks 4 e 5.

---

### Task 1: Catálogo controlado de localidades e pedidos com UF

**Files:**
- Create: `accounts/localidades.py`
- Create: `accounts/migrations/0016_pedidosangue_estado.py` (nomear conforme a última migração real)
- Modify: `accounts/models.py`
- Modify: `accounts/forms.py`
- Modify: `accounts/test_triagem_forms.py` ou novo `accounts/test_localidades.py`
- Modify: `accounts/test_pedidos.py` para o campo de pedido, se necessário

**Interfaces:**
- Produces `CIDADES_POR_ESTADO: dict[str, tuple[str, ...]]`, `ESTADOS_CHOICES` e helpers de validação reutilizáveis pelos forms.
- Produces `PedidoSangue.estado`, `blank=True`, `default=""`, `max_length=2`, preservando registros existentes.

- [ ] **Step 1: Escrever testes que falham para o catálogo e os pares UF/cidade**

Adicionar testes para: cadastro renderizar `estado` como select; cadastro aceitar `SP` + `São Paulo` (ou o valor canônico definido pelo catálogo); cadastro rejeitar `SP` + cidade de outra UF; `PedidoSangueForm` renderizar estado/cidade como selects; e POST com par incompatível ser inválido.

- [ ] **Step 2: Rodar os testes e confirmar a falha correta**

Run: `$env:DJANGO_SETTINGS_MODULE='config.settings_test'; .venv\Scripts\python.exe manage.py test accounts.test_localidades accounts.test_triagem_forms accounts.test_pedidos`

Expected: FAIL porque o catálogo, o select e/ou `PedidoSangue.estado` ainda não existem.

- [ ] **Step 3: Implementar `accounts/localidades.py` e o campo de modelo**

Definir a lista inicial a partir das localidades operacionais atuais (SP: São Paulo, Campinas e Santos), manter a UF derivada da mesma fonte e criar a migração aditiva para `PedidoSangue.estado`. Não alterar nem apagar valores legados.

- [ ] **Step 4: Atualizar `CadastroUsuarioForm`, `PedidoSangueForm` e filtros**

Usar choices controlados, atributos `data-estado` nas opções de cidade e `clean()` compartilhado para validar a combinação. O filtro deve continuar aceitando buscas textuais legadas, mas novas submissões devem usar as escolhas controladas.

- [ ] **Step 5: Rodar os testes da tarefa**

Run: `$env:DJANGO_SETTINGS_MODULE='config.settings_test'; .venv\Scripts\python.exe manage.py test accounts.test_localidades accounts.test_triagem_forms accounts.test_pedidos`

Expected: PASS, sem regressões nos testes de forms e pedidos.

- [ ] **Step 6: Commitar**

```powershell
git add accounts/localidades.py accounts/models.py accounts/forms.py accounts/migrations accounts/test_localidades.py accounts/test_triagem_forms.py accounts/test_pedidos.py
git commit --only accounts/localidades.py accounts/models.py accounts/forms.py accounts/migrations/0016_pedidosangue_estado.py accounts/test_localidades.py accounts/test_triagem_forms.py accounts/test_pedidos.py -m "feat: controlar localidades nos formularios"
```

### Task 2: Triagem simplificada independente e encaminhamento seguro

**Files:**
- Modify: `accounts/triagem_servico.py`
- Modify: `accounts/triagem_motor.py`
- Modify: `accounts/test_triagem_servico.py`
- Modify: `accounts/test_triagem_motor.py`
- Modify: `accounts/test_triagem_views.py`

**Interfaces:**
- Consumes `CIDADES_POR_ESTADO` only indirectly through the completed form work; no coupling with the frontend.
- Produces `iniciar_triagem(usuario, modalidade, ip=None, aceite_termo=True, reutilizar_respostas=False)` accepting simplified mode without a base.
- Preserves `TriagemExtensaNecessaria` behavior for unsafe/insufficient quick answers.

- [ ] **Step 1: Escrever testes vermelhos para iniciar simplificada sem extensa**

Adicionar testes de serviço e view provando que um Doador sem triagem extensa pode iniciar a simplificada, recebe `triagem_base is None`, é redirecionado para a primeira pergunta e vê a explicação adequada na apresentação.

- [ ] **Step 2: Rodar os testes e confirmar a falha correta**

Run: `$env:DJANGO_SETTINGS_MODULE='config.settings_test'; .venv\Scripts\python.exe manage.py test accounts.test_triagem_servico accounts.test_triagem_views`

Expected: FAIL com `TriagemSimplificadaIndisponivel` ou com a página escondendo a ação.

- [ ] **Step 3: Implementar a entrada independente no serviço**

Remover apenas a exigência de `obter_extensa_base` para criar a simplificada; deixar o vínculo nulo. Manter o bloqueio de perfis, aceite, consentimento e retomada de andamento.

- [ ] **Step 4: Ajustar o motor para base opcional**

Quando a modalidade for simplificada e não houver base, avaliar somente respostas atuais e produzir orientação explicitamente limitada/presencial, sem tentar acessar `triagem_base.respostas`.

- [ ] **Step 5: Testar o encaminhamento**

Adicionar teste que responde uma alternativa que exige extensa, verifica a simplificada cancelada, cria uma extensa em andamento e confirma a mensagem de encaminhamento. Garantir que a extensa começa sem copiar IDs `SIM-*` para `EXT-*`.

- [ ] **Step 6: Rodar a suíte da tarefa**

Run: `$env:DJANGO_SETTINGS_MODULE='config.settings_test'; .venv\Scripts\python.exe manage.py test accounts.test_triagem_servico accounts.test_triagem_motor accounts.test_triagem_views`

Expected: PASS, incluindo os testes antigos que ainda cobrem simplificada com base.

- [ ] **Step 7: Commitar**

```powershell
git add accounts/triagem_servico.py accounts/triagem_motor.py accounts/test_triagem_servico.py accounts/test_triagem_motor.py accounts/test_triagem_views.py
git commit --only accounts/triagem_servico.py accounts/triagem_motor.py accounts/test_triagem_servico.py accounts/test_triagem_motor.py accounts/test_triagem_views.py -m "feat: liberar triagem simplificada independente"
```

### Task 3: Navegação visual e botões de progresso da triagem

**Files:**
- Modify: `accounts/views.py`
- Modify: `templates/accounts/triagem_pergunta.html`
- Modify: `templates/accounts/triagem_revisao.html` se necessário
- Modify: `accounts/test_triagem_views.py`
- Modify: `elo_front/static/css/elo.css`

**Interfaces:**
- Consumes `editar_pergunta(triagem, id_pergunta)` e o fluxo persistido da Task 2.
- Produces contexto `progresso_triagem` com id, índice, estado (`respondida`, `atual`, `disponivel`) e URL de edição somente para perguntas respondidas/atual.

- [ ] **Step 1: Escrever teste vermelho para a trilha e salto seguro**

Testar que a página atual exibe botões de progresso; depois de responder a primeira pergunta, o botão dela leva de volta à mesma triagem com `?pergunta=...`; e uma pergunta ainda não respondida não vira link de edição.

- [ ] **Step 2: Rodar o teste e confirmar a falha**

Run: `$env:DJANGO_SETTINGS_MODULE='config.settings_test'; .venv\Scripts\python.exe manage.py test accounts.test_triagem_views.TriagemViewsTests.test_pagina_mostra_uma_pergunta_e_salva_resposta`

Expected: FAIL porque a tela ainda não contém a navegação visual.

- [ ] **Step 3: Implementar o contexto de progresso na view**

Derivar o progresso do `fluxo_perguntas`, respostas persistidas e `pergunta_atual`; nunca incluir ids fora da triagem do usuário. Preservar o comportamento existente de POST, anterior, salvar e revisão.

- [ ] **Step 4: Implementar os botões no template e estilos**

Renderizar uma sequência compacta, acessível por teclado e responsiva; usar `<a>` somente para perguntas editáveis e `<span>`/botão desabilitado para as demais. Destacar a etapa atual e manter CTA de anterior, salvar e continuar.

- [ ] **Step 5: Rodar testes da tarefa**

Run: `$env:DJANGO_SETTINGS_MODULE='config.settings_test'; .venv\Scripts\python.exe manage.py test accounts.test_triagem_views accounts.test_triagem_servico`

Expected: PASS, inclusive privacidade entre usuários e edição sem duplicar respostas.

- [ ] **Step 6: Commitar**

```powershell
git add accounts/views.py templates/accounts/triagem_pergunta.html templates/accounts/triagem_revisao.html accounts/test_triagem_views.py elo_front/static/css/elo.css
git commit --only accounts/views.py templates/accounts/triagem_pergunta.html templates/accounts/triagem_revisao.html accounts/test_triagem_views.py elo_front/static/css/elo.css -m "feat: adicionar progresso navegavel na triagem"
```

### Task 4: Layout base, avisos, menu e modais legais globais

**Files:**
- Create: `elo_front/static/js/elo.js` se a lógica hoje inline for extraída
- Modify: `templates/base.html`
- Modify: `elo_front/templates/base.html` somente se o loader ainda o utilizar
- Modify: `elo_front/static/css/elo.css`
- Modify: `templates/accounts/cadastro.html`
- Create/modify: `accounts/test_visualizacao.py` ou `accounts/test_layout.py`

**Interfaces:**
- Produces um layout base com navegação responsiva, mensagens com classes `message-success`, `message-info`, `message-warning`, `message-error`, e dois `<dialog>` globais com ids `modal-termos` e `modal-privacidade`.

- [ ] **Step 1: Escrever testes vermelhos de renderização do shell**

Testar uma página pública e uma autenticada para presença dos links do menu, classes/roles dos avisos e dos dois diálogos legais; verificar que o cadastro não precisa duplicar os diálogos.

- [ ] **Step 2: Rodar testes para confirmar a falha**

Run: `$env:DJANGO_SETTINGS_MODULE='config.settings_test'; .venv\Scripts\python.exe manage.py test accounts.test_layout`

Expected: FAIL porque os diálogos ainda não são globais e o shell não possui a nova estrutura testada.

- [ ] **Step 3: Consolidar o layout base**

Organizar o menu por contexto, manter as autorizações existentes por perfil, deixar CTAs visíveis e adicionar os modais legais uma única vez no final do body. Normalizar texto e atributos ARIA.

- [ ] **Step 4: Extrair o JavaScript mínimo**

Implementar abertura por `data-open-modal`, fechamento por `data-close-modal`, Escape/backdrop, menu mobile com `aria-expanded` e fechamento ao selecionar um link. Não colocar regra de negócio no JS.

- [ ] **Step 5: Estilizar avisos, modais e shell**

Usar tokens já existentes da paleta, contrastes claros para estados, foco visível, botões destacados, layout do rodapé e breakpoints mobile; remover CSS duplicado apenas quando não alterar telas existentes.

- [ ] **Step 6: Rodar testes da tarefa**

Run: `$env:DJANGO_SETTINGS_MODULE='config.settings_test'; .venv\Scripts\python.exe manage.py test accounts.test_layout accounts.test_visualizacao accounts.test_triagem_views`

Expected: PASS, com links legais funcionais em páginas diferentes.

- [ ] **Step 7: Commitar**

```powershell
git add templates/base.html elo_front/templates/base.html elo_front/static/css/elo.css elo_front/static/js/elo.js templates/accounts/cadastro.html accounts/test_layout.py accounts/test_visualizacao.py
git commit --only templates/base.html elo_front/templates/base.html elo_front/static/css/elo.css elo_front/static/js/elo.js templates/accounts/cadastro.html accounts/test_layout.py accounts/test_visualizacao.py -m "feat: organizar shell avisos e documentos legais"
```

### Task 5: Nova página inicial e organização dos conteúdos públicos

**Files:**
- Modify: `accounts/views.py`
- Modify: `templates/accounts/inicio.html`
- Modify: `elo_front/static/css/elo.css`
- Modify: `accounts/test_visualizacao.py` ou `accounts/test_home.py`
- Modify: `templates/accounts/triagem_apresentacao.html`, `estoque_publico.html` e `pedidos_listar.html` somente para aplicar componentes compartilhados

**Interfaces:**
- Consumes o shell visual e os modais da Task 4.
- Produces a rota `accounts:inicio` como home pública com hero, propósito, ações rápidas, explicação do fluxo Elo, estoque/pedidos e FAQ/links sem quebrar URLs atuais.

- [ ] **Step 1: Escrever testes vermelhos da home**

Testar título/propósito, CTA de triagem, CTA de estoque/pedidos, seção `sobre`, FAQ e renderização de pedidos ativos sem login.

- [ ] **Step 2: Rodar testes e confirmar a falha**

Run: `$env:DJANGO_SETTINGS_MODULE='config.settings_test'; .venv\Scripts\python.exe manage.py test accounts.test_home`

Expected: FAIL porque a tela atual é apenas “Acesso visitante” e não possui a estrutura de landing page.

- [ ] **Step 3: Implementar o template da home**

Criar uma composição clara com conteúdo em português, CTA primário destacado e ações secundárias; reaproveitar `postos`, `estoque_geral` e `pedidos_ativos` do contexto existente.

- [ ] **Step 4: Ajustar o CSS da home e dos componentes públicos**

Usar grids/cards que colapsem no mobile, hierarquia tipográfica consistente, estados de hover/focus e espaçamento alinhado ao shell.

- [ ] **Step 5: Rodar testes da tarefa**

Run: `$env:DJANGO_SETTINGS_MODULE='config.settings_test'; .venv\Scripts\python.exe manage.py test accounts.test_home accounts.test_visualizacao`

Expected: PASS.

- [ ] **Step 6: Commitar**

```powershell
git add accounts/views.py templates/accounts/inicio.html elo_front/static/css/elo.css accounts/test_home.py accounts/test_visualizacao.py templates/accounts/triagem_apresentacao.html templates/accounts/estoque_publico.html templates/accounts/pedidos_listar.html
git commit --only accounts/views.py templates/accounts/inicio.html elo_front/static/css/elo.css accounts/test_home.py accounts/test_visualizacao.py templates/accounts/triagem_apresentacao.html templates/accounts/estoque_publico.html templates/accounts/pedidos_listar.html -m "feat: criar home publica do Elo"
```

### Task 6: Integração, validação visual e verificação final

**Files:**
- Modify: qualquer arquivo necessário após os testes; não alterar mudanças staged do usuário sem motivo registrado
- Test: suíte completa existente

- [ ] **Step 1: Rodar lint estrutural e checagem de migrações**

Run: `$env:DJANGO_SETTINGS_MODULE='config.settings_test'; .venv\Scripts\python.exe manage.py check; .venv\Scripts\python.exe manage.py makemigrations --check --dry-run`

Expected: `System check identified no issues` e nenhuma migração pendente.

- [ ] **Step 2: Rodar a suíte completa com SQLite de testes**

Run: `$env:DJANGO_SETTINGS_MODULE='config.settings_test'; .venv\Scripts\python.exe manage.py test`

Expected: todos os testes passam. Se a tentativa padrão com PostgreSQL continuar bloqueada por permissão/servidor, registrar essa limitação e usar o resultado SQLite como verificação automatizada do código.

- [ ] **Step 3: Fazer inspeção visual da aplicação**

Iniciar o servidor com o ambiente do projeto, abrir home, cadastro, triagem, pedidos e uma página autenticada; conferir desktop/mobile, navegação do menu, avisos, selects dependentes, progresso e modais. Registrar qualquer ajuste visual como novo ciclo TDD quando tocar em comportamento.

- [ ] **Step 4: Fazer revisão final do diff e do estado staged**

Run: `git diff --stat; git diff --check; git status --short`

Expected: apenas arquivos da entrega foram alterados além dos três arquivos staged pré-existentes; sem whitespace errors ou exclusões acidentais.

- [ ] **Step 5: Commitar somente ajustes finais explicitamente listados**

Se a revisão produzir ajustes novos, adicionar somente os arquivos desses
ajustes e usar `git commit --only <arquivos-explicitos> -m "chore: verificar
experiencia completa do Elo"`. Não usar diretórios como pathspec e não incluir
as alterações staged pré-existentes do usuário por acidente.

