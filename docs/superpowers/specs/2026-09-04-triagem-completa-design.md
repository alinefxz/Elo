# Triagem completa do Elo - Especificação técnica

## Objetivo

Implementar no projeto Django do Elo uma pré-triagem orientativa para doação
de sangue em duas modalidades: extensa e simplificada. A solução deve conter
todas as perguntas e regras da especificação
`Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf`, salvar o andamento,
preservar o histórico individual e nunca declarar aptidão clínica.

## Fonte funcional

O arquivo
`C:\Users\aline\Downloads\Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf`
é tratado como material de requisitos da triagem. O conteúdo do documento não
substitui nem amplia o pedido da usuária: ele fornece perguntas, ramificações,
resultados e referências para a implementação autorizada nesta tarefa.

## Limites e linguagem de segurança

- A triagem é somente orientativa.
- O sistema nunca apresenta a pessoa como "apta" para doar.
- A decisão final pertence à equipe do hemocentro.
- Dúvida, resposta desconhecida ou regra sem dados suficientes conduz a
  `AVALIACAO_PRESENCIAL` ou ao bloco extenso correspondente.
- O motor avalia todas as respostas; ele não encerra a análise no primeiro
  impedimento.
- Medicamentos nunca devem ser suspensos por orientação do sistema.
- Valores informados de pressão, pulso, temperatura, hemoglobina e hematócrito
  não substituem aferição presencial.
- A versão inicial das regras é `HEMOMINAS_2026_08`, referente aos critérios
  consolidados em 28/08/2026. Mudanças normativas futuras exigem uma nova
  versão, sem reescrever resultados antigos.

## Perfis e acesso

- Visitante: visualiza a apresentação e as duas modalidades, mas precisa criar
  uma conta ou entrar para responder.
- Doador: pode iniciar a extensa; pode iniciar a simplificada depois de possuir
  ao menos uma extensa concluída.
- Receptor: recebe o mesmo acesso quando também deseja doar, sem alteração do
  perfil principal.
- Observador: visualiza somente a apresentação.
- Hemocentro: não acessa respostas pessoais nesta etapa.
- Administrador: consulta triagens e respostas no admin em modo somente leitura.
- Toda consulta de histórico ou detalhe feita fora do admin filtra
  obrigatoriamente por `usuario=request.user`.

## Texto de apresentação

A página de escolha exibirá integralmente o texto fornecido pela usuária,
começando com "Seu gesto de cuidado começa aqui." e terminando com a chamada
para escolher a modalidade. A página não terá CSS nesta etapa.

As duas modalidades sempre aparecem. Quando a pessoa ainda não possui uma
triagem extensa concluída, a simplificada permanece visível, mas a tentativa de
iniciá-la explica a condição e direciona para a extensa.

## Organização do código

### Catálogos de perguntas

As perguntas ficam versionadas em código, e não em novas tabelas administrativas.
Isso mantém a implementação didática, revisável por Git e coerente com o tamanho
atual do projeto.

- `accounts/triagem_catalogo_extensa.py`: perguntas `EXT-01` a `EXT-51`,
  alternativas, explicações, categoria, tipo do campo, obrigatoriedade,
  ramificações, fonte e regras.
- `accounts/triagem_catalogo_simplificada.py`: perguntas `SIM-01` a `SIM-18`,
  alternativas, regras e blocos extensos acionados por mudança ou dúvida.
- Cada pergunta possui identificador estável; textos podem evoluir sem alterar
  a identidade da pergunta.
- Perguntas de seleção múltipla armazenam uma lista de códigos.
- Datas e detalhes complementares ficam no mesmo valor estruturado da resposta.

### Motor de regras

`accounts/triagem_motor.py` será uma função pura: recebe modalidade, respostas,
data de referência e versão; devolve todos os achados, resultado principal,
data de liberação mais distante e mensagem segura.

Cada achado contém:

- `id_pergunta`;
- `codigo_regra`;
- `categoria`;
- `resultado`;
- `mensagem`;
- `data_liberacao`, quando calculável;
- `exige_relatorio`;
- `fonte`;
- `regra_version`.

A prioridade do resultado principal é:

1. `INAPTIDAO_DEFINITIVA`;
2. `AVALIACAO_PRESENCIAL`;
3. `INAPTIDAO_TEMPORARIA`;
4. `DOCUMENTACAO_ESPECIAL`;
5. `SEM_IMPEDIMENTO_IDENTIFICADO`.

Quando existirem vários impedimentos temporários, a data principal será a mais
distante. Prazos dependentes de cura, alta, retirada ou término de tratamento
só serão calculados quando a respectiva data de referência for informada.

### Formulário dinâmico

`accounts/triagem_forms.py` construirá um formulário Django para uma pergunta
por vez. Os tipos aceitos serão escolha única, escolha múltipla, data, número e
texto curto. A validação rejeitará datas futuras indevidas, respostas fora do
catálogo e ausência de complementos exigidos.

O HTML permanecerá simples e sem CSS. Cada tela mostrará:

- modalidade e progresso;
- código e texto da pergunta;
- explicação curta;
- alternativas ou campo complementar;
- botões "Anterior", "Salvar e sair" e "Continuar".

### Serviço de aplicação

`accounts/triagem_servico.py` centralizará operações que alteram o banco:

- criar uma triagem em andamento;
- validar se a pessoa pode usar a modalidade;
- localizar a pergunta atual;
- salvar ou substituir a resposta da pergunta atual;
- avançar e voltar sem duplicar respostas;
- acrescentar blocos extensos acionados pela simplificada;
- concluir a triagem em uma transação;
- calcular e salvar resultado e achados;
- localizar a extensa-base usada pela simplificada.

As views apenas recebem a requisição, chamam o serviço e renderizam templates.

## Persistência e migration

Os models `Triagem` e `RespostaTriagem` existentes serão preservados e
estendidos. Uma nova migration será necessária.

### Alterações em `Triagem`

- `status`: `EM_ANDAMENTO`, `CONCLUIDA` ou `CANCELADA`;
- `pergunta_atual`: posição atual do fluxo;
- `fluxo_perguntas`: lista JSON com a ordem efetiva das perguntas;
- `triagem_base`: referência opcional à extensa anterior usada pela
  simplificada;
- `atualizada_em`: data da última resposta;
- resultado, achados e finalização continuam vazios enquanto estiver em
  andamento.

### Alterações em `RespostaTriagem`

- `valor`: JSON com o valor completo e estruturado da resposta;
- restrição única por `triagem` e `id_pergunta`, para que voltar e corrigir
  substitua a resposta em vez de criar duplicatas.

Os campos antigos serão mantidos para compatibilidade e leitura no admin.

## Fluxo extenso

1. A pessoa lê a apresentação e escolhe a extensa.
2. O sistema cria uma `Triagem` em andamento e registra o termo de triagem.
3. A pessoa responde `EXT-01` a `EXT-51` respeitando as ramificações descritas
   na especificação.
4. Respostas "não" em blocos principais pulam subperguntas que não se aplicam.
5. Seleções de condição abrem seus complementos de data, tratamento,
   complicação, medicamento, documento ou relatório quando exigidos.
6. `EXT-51` permite revisar; somente a confirmação conclui.
7. O motor gera todos os achados e salva o resultado imutável daquela execução.

## Fluxo simplificado

1. O sistema exige uma extensa concluída do mesmo usuário.
2. A pessoa confirma que o resumo anterior continua correto em `SIM-01`.
3. Responde `SIM-02` a `SIM-18` sobre mudanças desde a extensa.
4. Respostas sem mudança reutilizam apenas o contexto necessário da extensa,
   sem duplicar detalhes íntimos na interface.
5. Respostas positivas ou desconhecidas inserem na fila os blocos extensos
   indicados pela especificação.
6. Se a base estiver incorreta ou incompleta, a pessoa é direcionada para uma
   nova extensa.
7. O resultado registra a extensa-base, a versão das regras e todas as novas
   respostas.

## Histórico no perfil

O dashboard exibirá somente informações não íntimas da triagem mais recente:

- modalidade;
- resultado orientativo;
- data de conclusão;
- data orientativa de liberação, quando existir;
- botão para abrir o detalhe privado;
- link para "Meu histórico de triagens".

A página de histórico lista todas as triagens do usuário, inclusive as em
andamento, com opção de continuar. Nenhum resultado anterior é sobrescrito.
O detalhe completo e as respostas só podem ser visualizados pelo dono da
triagem. O admin permanece somente leitura.

## Templates e rotas

Serão criadas ou atualizadas as seguintes páginas:

- `/triagem/`: apresentação e escolha da modalidade;
- `/triagem/extensa/iniciar/`;
- `/triagem/simplificada/iniciar/`;
- `/triagem/<id>/pergunta/`;
- `/triagem/<id>/historico/` ou ação equivalente para voltar;
- `/triagem/<id>/resultado/`;
- `/triagens/historico/`.

Os templates serão:

- `triagem_apresentacao.html`;
- `triagem_pergunta.html`;
- `triagem_resultado.html`;
- `triagem_historico.html`.

Os links serão incluídos na página pública e nos dashboards de Doador e
Receptor. Hemocentro e Observador verão apenas a apresentação pública.

## Privacidade

- Dados de saúde não aparecem em estoque, pedidos, campanhas, ranking ou
  notificações genéricas.
- O dashboard não exibe diagnósticos, uso de drogas, vida sexual, HIV, hepatite
  ou outras respostas íntimas.
- Objetos são buscados sempre com verificação de proprietário.
- O admin exibe aviso de dado sensível e bloqueia criação, edição e exclusão.
- Histórico não é compartilhado com Hemocentro nesta etapa.
- O consentimento de triagem continua versionado em `ConsentimentoLGPD`.

## Compatibilidade com dados existentes

- A migration `0006` e as triagens já salvas permanecem válidas.
- Registros antigos sem `status` recebem `CONCLUIDA` quando possuem
  `finalizada_em`; caso contrário recebem `EM_ANDAMENTO` por migration de dados.
- As respostas antigas serão convertidas para o novo campo `valor` usando
  `codigo_resposta`, `resposta_label`, `data_evento` e `metadata`.
- Nenhum arquivo de migration já aplicado será editado.

## Tratamento de erros

- ID de triagem inexistente ou pertencente a outro usuário retorna 404.
- Modalidade simplificada sem extensa-base redireciona para a apresentação com
  mensagem explicativa.
- Pergunta ou alternativa inválida não é persistida.
- Falha ao concluir reverte resultado e respostas da operação pela transação.
- Triagem concluída não aceita novas respostas; revisão cria uma nova execução
  ou ocorre antes da confirmação final.

## Testes

Os testes automatizados cobrirão:

- catálogo com todos os IDs `EXT-01` a `EXT-51` e `SIM-01` a `SIM-18`;
- alternativas e fontes obrigatórias;
- ramificações principais e retorno à pergunta anterior;
- cálculo de 48h, 72h, dias, semanas, meses e anos;
- escolha da data temporária mais distante;
- prioridade entre definitiva, avaliação, temporária e documentação;
- exceções descritas no PDF;
- comportamento de "não sei";
- simplificada bloqueada sem extensa;
- abertura de blocos extensos pela simplificada;
- histórico isolado por usuário;
- retomada de triagem em andamento;
- imutabilidade após conclusão;
- acesso de Visitante, Doador, Receptor, Observador, Hemocentro e Administrador;
- não exposição de respostas sensíveis no dashboard e nas páginas públicas;
- compatibilidade da migration com registros da versão inicial.

## Critério de conclusão

A funcionalidade estará concluída quando as 51 perguntas extensas e as 18
simplificadas estiverem representadas no catálogo, as ramificações e regras
estiverem cobertas por testes, cada resultado permanecer no histórico privado,
as duas modalidades estiverem apontadas no site e `python manage.py check`,
`python manage.py makemigrations --check` e `python manage.py test` passarem.
