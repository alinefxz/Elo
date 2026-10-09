"""Resumo curto das funcionalidades com trechos do codigo local."""
import ast
from pathlib import Path
from html import escape
import textwrap
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Preformatted, PageBreak, Spacer

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'output/pdf/Elo_Codigo_Explicado.pdf'
pdfmetrics.registerFont(TTFont('Resumo', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ResumoB', 'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Codigo', 'C:/Windows/Fonts/consola.ttf'))
body = ParagraphStyle('Texto', fontName='Resumo', fontSize=10, leading=13, spaceAfter=6)
title = ParagraphStyle('Titulo', fontName='ResumoB', fontSize=18, leading=23, spaceAfter=12,
                       textColor=colors.HexColor('#124E68'))
heading = ParagraphStyle('Topico', fontName='ResumoB', fontSize=12, leading=16, spaceBefore=9, spaceAfter=5,
                         textColor=colors.HexColor('#124E68'), keepWithNext=True)
small = ParagraphStyle('Arquivo', fontName='Resumo', fontSize=8.2, leading=11, spaceAfter=5,
                       textColor=colors.HexColor('#536879'))
mono = ParagraphStyle('Codigo', fontName='Codigo', fontSize=8, leading=10.3, spaceAfter=8,
                      backColor=colors.HexColor('#F2F5F7'), borderPadding=4)


def source(file):
    return (ROOT / file).read_text(encoding='utf-8-sig')


def function(file, name):
    text = source(file)
    return text, next(n for n in ast.walk(ast.parse(text)) if isinstance(n, ast.FunctionDef) and n.name == name)


def excerpt(file, name, indices=None):
    text, node = function(file, name)
    nodes = [n for n in node.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)
                                        and isinstance(n.value.value, str))]
    if indices is not None:
        nodes = [nodes[i] for i in indices]
    return '\n'.join(textwrap.dedent(ast.get_source_segment(text, n)) for n in nodes)


def containing(file, name, needle, kind=ast.If):
    text, node = function(file, name)
    found = next(n for n in ast.walk(node) if isinstance(n, kind) and needle in ast.get_source_segment(text, n))
    return textwrap.dedent(ast.get_source_segment(text, found))


def text(value, style=body):
    return Paragraph(escape(value), style)


DETALHES = {
    'Conta e senha': 'email e extra_fields fornecem os dados usados para montar Usuario. A variável usuario representa a nova conta. A senha original é usada por set_password para gerar o hash, que permite conferir futuros logins. Exemplo: a mesma conta criada aqui passa a ser reconhecida nas telas protegidas.',
    'Acesso ao painel': 'O símbolo @ coloca uma regra antes da função. Quando alguém abre /dashboard/, essa regra confere se existe uma sessão autenticada. Depois, a função usa request.user para identificar o perfil e preparar os blocos e avisos daquele usuário.',
    'Quem pode solicitar pedidos': 'getattr consulta is_authenticated; False é o valor usado se essa informação estiver ausente. O operador or significa que basta uma das situações para recusar: estar sem login ou ter outro perfil. != significa diferente. A mensagem explica ao usuário por que a ação foi interrompida.',
    'Hemocentro aprovado': 'and significa que as duas verificações precisam ser atendidas ao mesmo tempo. usuario_e_hemocentro confere o tipo de conta; status_validacao confere a situação institucional. O resultado é True ou False, usado por outras funções para decidir se a publicação pode continuar.',
    'Solicitar não é publicar': 'solicitante liga o pedido à conta que o enviou. **dados distribui os dados recebidos nos campos do pedido, como tipo sanguíneo e destino. O estado ENVIADA representa o início da análise. A decisão posterior fica registrada no histórico, junto de quem a tomou.',
    'Publicação e aviso compatível': 'A primeira condição confere o estado do pedido; a segunda confere o Hemocentro. tipo_sanguineo fornece o tipo necessário para a busca de candidatos. select_for_update solicita o bloqueio dos registros durante a transação, coordenando a conferência do limite quando mais de uma convocação acontece ao mesmo tempo.',
    'Quem pode responder': 'Essa verificação faz parte das regras de acesso à triagem. O catálogo fornece as perguntas, e o serviço cuida de iniciar, retomar, salvar respostas e concluir. Assim, as perguntas da tela e o resultado calculado ficam ligados à conta do Doador que respondeu.',
    'Versão simplificada': 'modalidade indica qual versão foi escolhida. obter_extensa_base busca a extensa que pode servir de referência. None significa que nenhuma foi encontrada. Quando existe uma base, o fluxo rápido aproveita as informações permitidas e faz as perguntas necessárias para a situação atual.',
    'Escolha do resultado': 'A primeira linha reúne os resultados presentes nos achados. O for percorre PRIORIDADE_RESULTADOS na ordem definida pelo sistema. O primeiro resultado encontrado encerra a função com return. Os demais achados continuam guardados, permitindo mostrar os motivos que levaram à orientação.',
    'Situação do estoque': 'A ordem dos if é importante: o código verifica crítico antes de baixo, porque uma quantidade crítica também poderia estar abaixo do mínimo. A primeira condição atendida encerra o cálculo. Entrada soma bolsas, saída retira e ajuste define a quantidade informada; depois disso, o estado é recalculado.',
    'Disparo somente no crítico': 'O dicionário liga um estado do estoque a um tipo de notificação. not in significa que o estado não aparece entre as chaves desse dicionário. Quando está crítico, o fluxo segue para buscar os doadores e preparar os avisos. A quantidade de avisos criados é devolvida para o fluxo da movimentação.',
    'Evitar excesso e repetição': 'exists verifica se já há registro com o mesmo doador, estoque e tipo, ainda não lido. O operador or permite impedir o novo aviso por frequência ou repetição. continue atua dentro do for: pula apenas aquele candidato e permite conferir os próximos.',
    'Tipo compatível': 'tipo_solicitado é o sangue necessário no estoque ou pedido. normalizar_tipo_sanguineo padroniza o texto e rejeita valores desconhecidos. Os colchetes consultam a tabela pela chave escolhida. Essa mesma regra alimenta a tela informativa e a seleção dos candidatos aos alertas.',
    'Quem pode receber convocação': 'Cada linha do filter acrescenta uma exigência. is_active=True mantém contas ativas; suspensa=False exclui suspensas; aceita_notificacoes_pedidos=True exige a preferência ligada. __in significa pertencer ao conjunto de tipos compatíveis. As conferências seguintes combinam essas condições com triagem e consentimento.',
    'Limite compartilhado': 'As três constantes são configurações usadas pelas funções, não dados de um único usuário. A contagem considera a janela das últimas 24 horas a partir do momento da busca. Exemplo: quem já recebeu um alerta de estoque nessa janela pode atingir o limite antes da convocação de um pedido.',
    'Conteúdo do aviso': 'CharField guarda texto curto; TextField guarda a mensagem; BooleanField guarda sim ou não; DateTimeField guarda data e hora. default=False faz o aviso começar não lido. auto_now_add=True preenche a criação automaticamente. null=True permite que a data de leitura fique vazia até a leitura acontecer.',
    'Marcar como lida': 'get_object_or_404 procura o identificador dentro dos avisos do usuário atual. Se o aviso não está nesse conjunto, a ação é interrompida. O filtro lida=False faz a atualização somente na primeira leitura; timezone.now fornece o instante registrado. O aviso permanece disponível no histórico.',
    'Registrar uma ação crítica': 'acao classifica o evento; usuario informa o responsável; alvo aponta o registro afetado; request fornece contexto do acesso. descricao apresenta o que aconteceu em texto. metadados guarda detalhes organizados por nome, como evento e status_pedido, para ajudar na consulta administrativa.',
    'Falhas de login': 'O sinal é um aviso interno do Django de que a autenticação falhou. A função registra a falha e conta as recentes para o e-mail informado, ou por IP no caminho alternativo previsto. Ao atingir o limite, acrescenta o evento LOGIN_SUSPEITO à auditoria.',
    'Acessos sensíveis': 'Middleware é uma camada que acompanha o processamento das páginas. Aqui ele observa a resposta já produzida: uma consulta autorizada a uma rota sensível pode gerar registro de acesso; uma tentativa recusada pode gerar registro de bloqueio. A auditoria guarda o evento sem copiar o formulário clínico inteiro.',
}

story = []
chapter_index = 0


def aprofundar(index):
    story.append(PageBreak())
    story.append(text('ELO | COMO A FUNCIONALIDADE FOI IMPLEMENTADA', small))
    if index == 1:
        story.append(text('Cadastro e perfis: o fluxo completo', title))
        block('Como o perfil é representado', 'Os perfis são alternativas definidas na conta, usadas para decidir quais ações cada pessoa pode executar.',
              'accounts/models.py', '\n'.join(source('accounts/models.py').splitlines()[90:98]),
              'models.TextChoices reúne o valor que o sistema salva e o nome apresentado na tela. DOADOR é o valor usado nas verificações; Doador é o texto legível. Cada conta tem um perfil, e as views e serviços consultam esse valor.')
        story.append(text('Do formulário à conta', heading))
        story.append(text('O formulário recebe nome, e-mail, senha, perfil e os demais dados solicitados. Os métodos clean conferem campos e combinações: documento apropriado, e-mail, senha e preenchimentos exigidos. Quando os dados estão válidos, a view cria a conta e registra o consentimento geral.'))
        story.append(text('O salvamento usa uma transação: as gravações agrupadas precisam terminar juntas. Depois do cadastro, o Django inicia a sessão. Nas próximas páginas, request.user identifica a conta dessa sessão. Isso permite montar o painel e filtrar os dados do próprio usuário.'))
        story.append(text('Como as permissões são aplicadas', heading))
        story.append(text('O template escolhe os botões que aparecem. A view e o serviço conferem se a ação pode ser executada. Essas verificações se complementam: mesmo quando alguém abre uma rota diretamente, o servidor decide pelo perfil e pelas condições da operação. O acesso administrativo do Django também usa is_staff, is_superuser e permissões próprias.'))
        story.append(text('Perfis: Doador faz triagem; Receptor solicita; Observador consulta; Hemocentro aprovado gerencia sua instituição; Administrador valida e modera. Visitante usa as consultas públicas.'))
    elif index == 2:
        story.append(text('Instituições e pedidos: decisões registradas', title))
        src, node = function('accounts/validacao_hemocentro.py','registrar_decisao_validacao_hemocentro')
        group = next(n for n in node.body if isinstance(n,ast.With))
        snippet = '\n'.join(textwrap.dedent(ast.get_source_segment(src,n)) for n in group.body[1:5])
        block('Estado atual e histórico', 'Na decisão institucional, o sistema atualiza o cadastro e cria um registro separado da análise.',
              'accounts/validacao_hemocentro.py', snippet,
              'status_anterior guarda o estado antes da decisão. status_validacao recebe o novo estado e save grava os campos indicados. ValidacaoHemocentro.objects.create acrescenta o histórico, relacionando instituição, administrador, decisão e parecer.')
        story.append(text('Como o pedido percorre o sistema', heading))
        story.append(text('O Receptor preenche a solicitação e escolhe um Hemocentro aprovado de destino. O servidor confere título, tipo sanguíneo, urgência, cidade, descrição, identificação do solicitante e e-mail para retorno. A solicitação salva começa como ENVIADA e fica disponível para análise da instituição responsável.'))
        story.append(text('Ao publicar, o sistema registra quem publicou e quando, muda o estado para PUBLICADA e prepara notificações compatíveis. Recusa e solicitação de correção também ficam no histórico. As decisões são auditadas. Possíveis pedidos semelhantes são sinalizados para ajudar a análise, sem afirmar automaticamente que são ilegítimos.'))
        story.append(text('Separação dos dados', heading))
        story.append(text('O Receptor vê suas solicitações; o Hemocentro vê as destinadas a ele; a consulta pública vê os pedidos publicados. Essa separação vem dos filtros da consulta. O identificador do pedido escolhe o registro, e as regras do servidor conferem se a conta pode agir sobre ele.'))
    elif index == 3:
        story.append(text('Triagem: da resposta ao histórico', title))
        snippet = containing('accounts/triagem_servico.py','salvar_resposta','RespostaTriagem.objects.update_or_create',ast.Expr)
        block('Salvar ou corrigir uma resposta', 'Uma pergunta fica identificada por seu código dentro da triagem.',
              'accounts/triagem_servico.py', snippet,
              'update_or_create procura a combinação triagem e id_pergunta. Quando existe, atualiza a resposta; quando não existe, cria. defaults contém o que será salvo. O código guarda a alternativa, o texto, datas, valores organizados e a referência da regra.')
        story.append(text('Papel de cada parte', heading))
        story.append(text('O catálogo descreve perguntas e alternativas. O formulário monta os campos e confere o preenchimento. O serviço confirma que a pergunta pertence ao fluxo, confere os códigos escolhidos e salva a resposta. O motor lê esses dados para aplicar regras e calcular a orientação.'))
        story.append(text('Na extensa, o fluxo pode incluir perguntas condicionais conforme as respostas. A simplificada usa uma extensa de base e pode abrir blocos detalhados. Algumas escolhas levam ao cancelamento da tentativa rápida e à orientação de fazer a extensa. Esses estados ajudam a preservar o histórico do que aconteceu.'))
        story.append(text('Resultado e prazo', heading))
        story.append(text('Os achados guardam as condições identificadas. O resultado principal segue a prioridade das regras; os achados continuam disponíveis para explicar os motivos. Quando há mais de um prazo, o cálculo considera a data mais distante. A versão da regra salva permite entender qual conjunto de regras produziu aquele resultado.'))
    elif index == 4:
        story.append(text('Estoque: quantidade, histórico e convocação', title))
        src, node = function('accounts/estoque.py','registrar_movimentacao_estoque')
        assigns = [n for n in ast.walk(node) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('movimentacao','notificacoes_geradas') for t in n.targets)]
        block('Registro da movimentação', 'Depois de salvar quantidade e situação, a função guarda o histórico e chama a geração de avisos.',
              'accounts/estoque.py', '\n'.join(textwrap.dedent(ast.get_source_segment(src,n)) for n in assigns),
              'O histórico liga estoque e responsável e guarda quantidade anterior, mudança, quantidade nova e motivo. notificacoes_geradas recebe quantos avisos foram criados. Esse número também compõe o contexto registrado na auditoria.')
        story.append(text('Como a quantidade muda', heading))
        story.append(text('Entrada adiciona bolsas ao total; saída retira; ajuste define o novo total informado. O serviço confere tipo de movimento, quantidade, motivo e autorização. A quantidade final é usada para calcular o estado. O estado salvo alimenta a consulta do estoque e o fluxo de alerta.'))
        story.append(text('Como o aviso é preparado', heading))
        story.append(text('Quando o resultado é crítico, o sistema seleciona os doadores elegíveis e confere cada candidato. Para os aprovados nessas conferências, monta Notificacao com usuário, estoque, tipo, título, mensagem e destino. bulk_create salva os avisos preparados em lote.'))
        story.append(text('A seleção e a conferência de frequência acontecem em transação, com bloqueio solicitado por doador. Isso coordena convocação de estoque e pedido quando ambos tentam usar o limite do mesmo usuário. A proteção contra aviso igual não lido também evita repetição desnecessária para o mesmo estoque.'))
    elif index == 5:
        story.append(text('Convocação: as conferências combinadas', title))
        src,node=function('accounts/compatibilidade.py','doadores_aptos_para_convocacao')
        assigns=[n for n in node.body if isinstance(n,ast.Assign)]
        block('Última triagem e consentimento', 'A busca prepara duas verificações ligadas ao Doador candidato.',
              'accounts/compatibilidade.py', '\n'.join(textwrap.dedent(ast.get_source_segment(src,n)) for n in assigns),
              'OuterRef("pk") liga a busca ao usuário que está sendo analisado. A triagem é ordenada da mais recente para a mais antiga. O consentimento precisa ser do termo NOTIFICACOES, na versão configurada, aceito e sem data de revogação.')
        story.append(text('Por que consultar a última triagem', heading))
        story.append(text('A busca não usa apenas a existência de uma triagem antiga apta. Subquery seleciona o resultado e a data de liberação da última concluída. A consulta exige resultado APTO e aceita liberação vazia ou já alcançada. Exists indica se o consentimento válido foi encontrado. Tudo isso se soma ao perfil, sangue compatível, preferência, conta ativa e ausência de suspensão.'))
        story.append(text('Preferência e frequência', heading))
        story.append(text('No cadastro, o Doador pode autorizar convocação; no painel, pode mudar a escolha. O helper atualiza a preferência e o registro de consentimento/revogação e audita a mudança. A frequência soma avisos de estoque e pedido dentro da janela configurada, inclusive os lidos. Cada fluxo também aplica sua proteção contra duplicatas.'))
        story.append(text('Exemplo de execução', heading))
        story.append(text('Em uma necessidade O-, a tabela define os tipos compatíveis. A busca seleciona apenas contas que passam por todas as conferências. Depois, o limite e a repetição são verificados antes de criar cada aviso. Assim, a convocação combina necessidade, compatibilidade, aptidão e autorização.'))
    elif index == 6:
        story.append(text('Notificações: do botão ao banco', title))
        html=source('templates/accounts/dashboard.html')
        start=html.index('                        <form method="post">',html.index('{% if not notificacao.lida %}'))
        end=html.index('</form>',start)+len('</form>')
        block('O formulário de leitura', 'O botão envia a ação e o identificador do aviso ao dashboard.',
              'templates/accounts/dashboard.html', textwrap.dedent(html[start:end]),
              'method="post" envia a mudança ao servidor. csrf_token inclui a proteção do formulário. Os campos hidden são enviados sem aparecer como entradas editáveis. acao distingue a leitura do formulário de preferência; id_notificacao indica qual aviso será tratado.')
        story.append(text('O processamento no servidor', heading))
        story.append(text('A view recebe os dados, converte o identificador para número e trata valores inválidos. Depois procura o aviso dentro de request.user.notificacoes. Esse detalhe aplica a propriedade do registro: o usuário não ganha acesso ao aviso de outra conta só por conhecer seu número.'))
        story.append(text('A atualização usa lida=False para agir apenas sobre avisos ainda não lidos. Ela grava lida=True e lida_em com o instante atual. Uma nova tentativa não substitui a primeira data de leitura. O redirecionamento abre o painel novamente com o estado atualizado.'))
        story.append(text('O que a central apresenta', heading))
        story.append(text('A lista é ordenada da notificação mais recente para a mais antiga, com dez por página. Mostra contador de não lidas, tipo, título, mensagem e data. A ação usa url_destino: avisos de estoque mostram Ver estoque; pedidos mostram Ver pedido. O histórico mantém os lidos e permite navegar pelas páginas anteriores.'))
    elif index == 7:
        story.append(text('Auditoria: como o evento é salvo', title))
        block('Registro padronizado', 'As funções do sistema usam um helper para gravar os eventos no mesmo formato.',
              'accounts/auditoria.py', excerpt('accounts/auditoria.py','registrar_auditoria'),
              'identificar_alvo obtém tipo e identificador do registro afetado. A função considera se o usuário está autenticado. O create grava o evento com ação, resultado, alvo, descrição e informações do acesso. Valores passados diretamente podem complementar os detectados.')
        story.append(text('Dados do acesso e proteção do conteúdo', heading))
        story.append(text('IP e user_agent ajudam a identificar o contexto da ação. limpar_metadados aplica as regras de limpeza antes da gravação. O objetivo é registrar o acontecimento e informações necessárias para a análise, evitando guardar senhas e outros valores protegidos nos campos tratados pelo helper.'))
        story.append(text('Eventos e consulta administrativa', heading))
        story.append(text('Os serviços registram ações críticas nos pontos em que elas acontecem. O sinal de login registra falhas. O middleware acompanha respostas e registra consultas sensíveis ou tentativas bloqueadas conforme as rotas definidas. No admin, permissões controlam a consulta e protegem o histórico contra alteração pela interface.'))


def chapter(name):
    global chapter_index
    if story:
        aprofundar(chapter_index)
        story.append(PageBreak())
    chapter_index += 1
    story.extend([text('ELO | FUNCIONALIDADES COM CODIGO', small), text(name, title)])


def block(name, what, file, snippet, why):
    story.extend([text(name, heading), text(what), text('Arquivo: ' + file, small)])
    lines = []
    for line in snippet.expandtabs(4).splitlines():
        lines.extend(textwrap.wrap(line, width=99, subsequent_indent='    ', replace_whitespace=False,
                                   drop_whitespace=False, break_on_hyphens=False) if len(line)>99 else [line])
    story.extend([Preformatted('\n'.join(lines), mono), text(why)])
    if name in DETALHES:
        story.append(text(DETALHES[name]))
    termos = {
        'set_password': 'gera o hash da senha',
        'save': 'grava as informações no banco',
        'update_fields': 'indica quais campos devem ser gravados',
        'create': 'cria e salva um novo registro',
        'update_or_create': 'atualiza o registro encontrado ou cria um novo',
        'defaults': 'contém os valores usados na criação ou atualização',
        'filter': 'seleciona registros pelas condições informadas',
        'exists': 'responde se há algum registro correspondente',
        'update': 'altera os campos dos registros selecionados',
        'get_object_or_404': 'busca o registro e interrompe com 404 se ele não existir na busca permitida',
        'getattr': 'lê uma informação do objeto e aceita um valor padrão se ela estiver ausente',
        'select_for_update': 'solicita bloqueio dos registros durante a transação',
        'order_by': 'ordena os resultados; menos antes do campo coloca os mais recentes primeiro',
        'OuterRef': 'liga a busca interna ao identificador do usuário da busca principal',
        'objects': 'dá acesso às operações de busca e gravação do model',
        'CharField': 'define um campo de texto com limite de tamanho',
        'TextField': 'define um campo para texto mais longo',
        'BooleanField': 'define um campo de sim ou não',
        'DateTimeField': 'define um campo de data e horário',
        'max_length': 'define o tamanho máximo do texto',
        'auto_now_add': 'preenche a data na criação do registro',
        'null': 'permite ausência de valor no banco quando está True',
        'csrf_token': 'inclui o token de proteção do formulário',
        'hidden': 'envia um dado do formulário sem exibir uma caixa de preenchimento',
        'request': 'reúne as informações do pedido enviado pelo navegador',
        'pk': 'é o identificador principal de um registro',
        'metadados': 'guarda detalhes adicionais do evento por nome',
        'limpar_metadados': 'aplica as regras de limpeza aos detalhes antes de gravar',
        'quantidade_anterior': 'é o total de bolsas antes da movimentação',
        'quantidade_nova': 'é o total depois da movimentação',
        'tipo_sanguineo__in': 'exige que o sangue pertença ao conjunto informado',
        'revogado_em__isnull': 'confere se a data de revogação está vazia',
        'status_validacao': 'guarda a situação institucional atual',
        'PRIORIDADE_RESULTADOS': 'define a ordem dos resultados mais restritivos',
        'PermissionDenied': 'interrompe uma ação que a conta não pode executar',
        'return': 'encerra a função e entrega o resultado',
        'continue': 'pula para o próximo item da repetição',
        'for': 'percorre os itens um por um',
        'if': 'executa o bloco quando a condição é atendida',
        'and': 'exige que as condições ligadas sejam atendidas juntas',
        'or': 'aceita que pelo menos uma das condições ligadas seja atendida',
        'None': 'representa ausência de valor',
        'True': 'representa uma condição verdadeira ou ligada',
        'False': 'representa uma condição falsa ou desligada',
    }
    encontrados = [(term, meaning) for term,meaning in termos.items()
                   if re.search(r'(?<!\w)' + re.escape(term) + r'(?!\w)', snippet)]
    if encontrados:
        story.append(Paragraph('<b>Para ler esse código:</b> ' + ' · '.join(
            '<b>' + escape(term) + '</b>: ' + escape(meaning) for term,meaning in encontrados[:5]) + '.', body))


chapter('1. Cadastro, login e perfis')
story.append(text('Resumo com trechos principais dos códigos, sem exercícios. Os trechos são recortes: não representam arquivos completos. As regras descritas correspondem ao código local analisado em 09/10/2026.'))
block('Conta e senha', 'O sistema usa e-mail para entrar e guarda a senha de forma protegida.',
      'accounts/models.py', excerpt('accounts/models.py','create_user',[-4,-3,-2,-1]),
      'create_user monta a conta. set_password transforma a senha em hash; save grava a conta. return entrega a conta criada.')
block('Acesso ao painel', 'O usuário precisa entrar para abrir seu painel.', 'accounts/views.py',
      '@login_required\ndef dashboard(request):\n    """Mostra o painel protegido particularizado pelo perfil do usuario."""',
      'login_required exige login. request contém o pedido do navegador e identifica o usuário atual. O restante da função prepara o painel.')
block('Quem pode solicitar pedidos', 'Somente Receptor autenticado pode enviar uma solicitação.',
      'accounts/validacao_pedido.py', excerpt('accounts/validacao_pedido.py','criar_pedido_pendente',[0]),
      'A condição confere login e perfil. Se não forem permitidos, PermissionDenied interrompe a ação. Esconder um botão não substitui essa conferência.')

chapter('2. Hemocentros e pedidos')
block('Hemocentro aprovado', 'A instituição só publica quando seu cadastro está aprovado.',
      'accounts/validacao_hemocentro.py', excerpt('accounts/validacao_hemocentro.py','hemocentro_aprovado'),
      'As duas condições precisam ser verdadeiras: ser Hemocentro e ter estado APROVADO. O Administrador aprova, recusa ou pede correção; o histórico guarda a decisão.')
block('Solicitar não é publicar', 'A solicitação começa como ENVIADA. O Hemocentro aprovado de destino analisa antes da publicação.',
      'accounts/validacao_pedido.py', containing('accounts/validacao_pedido.py','criar_pedido_pendente','status=PedidoSangue.Status.ENVIADA',ast.Assign),
      'PedidoSangue reúne o solicitante e os dados do formulário. ENVIADA mantém o pedido fora da lista pública. As etapas seguintes conferem os dados e salvam.')
block('Publicação e aviso compatível', 'Um pedido só gera convocação quando está publicado e seu Hemocentro está aprovado.',
      'accounts/pedidos.py', excerpt('accounts/pedidos.py','criar_notificacoes_para_pedido',[0,1]),
      'return 0 encerra sem aviso quando uma condição falha. Caso permitido, a mesma busca de doadores usada no estoque seleciona os candidatos. Depois são conferidos frequência e duplicidade.')
story.append(text('O Receptor acompanha suas solicitações. O Hemocentro acompanha apenas as destinadas a ele. A consulta pública lista publicados e permite filtros. O Administrador atua na moderação prevista, sem substituir a publicação institucional.'))

chapter('3. Triagem e resultado')
block('Quem pode responder', 'A triagem pertence ao Doador e é uma orientação, não uma liberação médica.',
      'accounts/triagem_servico.py', excerpt('accounts/triagem_servico.py','pode_responder'),
      'A função decide se o perfil pode responder. As telas também limitam o acesso às triagens do próprio usuário.')
block('Versão simplificada', 'A versão rápida usa uma triagem extensa concluída como base.',
      'accounts/triagem_servico.py', containing('accounts/triagem_servico.py','iniciar_triagem','Conclua primeiro uma triagem extensa.'),
      'Se o usuário escolher SIMPLIFICADA, o sistema procura a extensa de base. Sem essa base, interrompe o início e orienta a concluir a extensa.')
block('Escolha do resultado', 'O motor mantém os problemas encontrados e escolhe o resultado de maior restrição.',
      'accounts/triagem_motor.py', excerpt('accounts/triagem_motor.py','escolher_resultado'),
      'achados são as condições encontradas nas respostas. O sistema percorre a ordem de prioridade e devolve a primeira presente. Sem impedimento encontrado, devolve SEM_IMPEDIMENTO.')
story.append(text('Os catálogos definem perguntas e regras; o formulário recebe respostas; o serviço salva, retoma e revisa; o motor calcula resultado e prazos. O histórico guarda respostas, resultado e versão da regra.'))

chapter('4. Estoque e alerta crítico')
block('Situação do estoque', 'O Hemocentro aprovado registra entrada, saída ou ajuste. O sistema calcula a situação pela quantidade.',
      'accounts/estoque.py', excerpt('accounts/estoque.py','calcular_status_calculado'),
      'Com mínimo 10 e crítico 5: quantidade 12 é estável, 7 é baixa e 5 é crítica. O sinal <= inclui o limite na situação indicada.')
block('Disparo somente no crítico', 'A atualização de estoque crítico pode criar convocação; estoque baixo não gera novos avisos.',
      'accounts/estoque.py', 'STATUS_DE_ESTOQUE_QUE_GERAM_ALERTA = {\n    Estoque.StatusCalculado.CRITICO: Notificacao.Tipo.ESTOQUE_CRITICO,\n}\n\n' + excerpt('accounts/estoque.py','criar_notificacoes_para_doadores_compativeis',[0]),
      'O mapa contém apenas CRITICO. Quando o estado não está no mapa, return 0 encerra a geração de avisos.')
block('Evitar excesso e repetição', 'Antes de criar o aviso, o sistema confere frequência e se há aviso igual ainda não lido.',
      'accounts/estoque.py', containing('accounts/estoque.py','criar_notificacoes_para_doadores_compativeis','limite_convocacao_atingido'),
      'Se uma dessas condições acontecer, continue pula esse doador. A movimentação também grava histórico e auditoria.')

chapter('5. Compatibilidade, aptidão e consentimento')
block('Tipo compatível', 'A tabela liga o tipo solicitado aos tipos de doadores aceitos pelo sistema.',
      'accounts/compatibilidade.py', excerpt('accounts/compatibilidade.py','doadores_compativeis_para'),
      'A primeira linha limpa e confere o tipo informado. A segunda busca os tipos compatíveis na tabela. Para O-, a tabela seleciona O-.')
text_src, node = function('accounts/compatibilidade.py','doadores_aptos_para_convocacao')
ret = next(n for n in node.body if isinstance(n,ast.Return))
chain = ast.get_source_segment(text_src,ret)
snippet = chain[chain.index('Usuario.objects.filter'):chain.index(').annotate')] + ')'
block('Quem pode receber convocação', 'Não basta ter sangue compatível: a conta precisa estar ativa, sem suspensão e com a preferência ligada.',
      'accounts/compatibilidade.py', snippet,
      'filter restringe os candidatos a Doadores. A consulta completa também exige a última triagem concluída apta, data de liberação permitida e consentimento aceito, não revogado e da versão configurada.')
block('Limite compartilhado', 'Estoque e pedidos compartilham o limite padrão de um aviso em 24 horas.',
      'config/settings.py', 'CONVOCACAO_INTERVALO_HORAS = 24\nCONVOCACAO_LIMITE_NOTIFICACOES = 1\nCONVOCACAO_VERSAO_CONSENTIMENTO = "1.0"',
      'O sistema conta os avisos da janela de tempo, inclusive lidos. A preferência pode ser autorizada ou revogada pelo Doador no painel; somente a preferência ligada não substitui o consentimento registrado.')

chapter('6. Central de notificações')
block('Conteúdo do aviso', 'A central mostra título, mensagem, data, tipo, ação e estado lida/não lida.',
      'accounts/models.py', '\n'.join(line.strip() for line in source('accounts/models.py').splitlines() if line.strip().startswith(('titulo = models.CharField(max_length=120)', 'mensagem = models.TextField()', 'url_destino = models.CharField', 'lida = models.BooleanField', 'criada_em = models.DateTimeField', 'lida_em = models.DateTimeField'))),
      'titulo e mensagem são o conteúdo. url_destino aponta a ação. lida indica o estado; criada_em e lida_em guardam as datas. O painel conserva o histórico em páginas de dez avisos.')
snippet = '\n'.join(source('accounts/views.py').splitlines()[729:737])
# Locate the exact owner lookup and update instead of depending on a moving line number.
src, dashboard = function('accounts/views.py','dashboard')
post = dashboard.body[1]
read = next(n for n in ast.walk(dashboard) if isinstance(n,ast.If) and isinstance(n.test,ast.Compare)
            and 'marcar_notificacao_lida' in ast.unparse(n.test))
snippet = '\n'.join(textwrap.dedent(ast.get_source_segment(src,n)) for n in read.body[1:])
block('Marcar como lida', 'Cada usuário marca somente seus próprios avisos.',
      'accounts/views.py', snippet,
      'request.user.notificacoes limita a busca ao dono. update marca lida e registra a data apenas se ainda não estava lida. redirect volta ao painel. O código anterior a esse trecho confere o identificador recebido.')
story.append(text('Os botões levam a Ver estoque ou Ver pedido. Abrir o destino não marca leitura sozinho: há uma ação específica. Ler o aviso não remove a contagem de frequência.'))

chapter('7. Auditoria das ações do sistema')
block('Registrar uma ação crítica', 'A auditoria guarda autor, ação, alvo e contexto das operações instrumentadas.',
      'accounts/pedidos.py', containing('accounts/pedidos.py','publicar_pedido','registrar_auditoria',ast.Expr),
      'Neste exemplo, a publicação do pedido cria um registro de auditoria. usuario identifica quem agiu; alvo indica o pedido; metadados acrescenta evento e estado. O helper central trata os metadados antes de gravar.')
block('Falhas de login', 'O sistema registra falhas e identifica repetição como suspeita.',
      'accounts/signals.py', 'LIMITE_LOGIN_SUSPEITO = 5\nJANELA_LOGIN_SUSPEITO_MINUTOS = 10',
      'Cinco falhas na janela de dez minutos geram evento suspeito. O sinal do Django avisa quando o login falha e a função auditar_login_falho grava o evento.')
block('Acessos sensíveis', 'Foi incluído o registro das consultas a dados sensíveis nas rotas definidas.',
      'accounts/auditoria.py',
      'ROTAS_SENSIVEIS = {\n    "accounts:triagem_pergunta", "accounts:triagem_resultado",\n    "accounts:triagem_historico", "accounts:painel_validacao_pedidos",\n    "accounts:triagem_revisao", "accounts:minhas_solicitacoes",\n    "accounts:painel_pedidos_hemocentro",\n}',
      'Essa lista identifica as telas acompanhadas pelo middleware. Ao terminar a resposta, ele confere rota, usuário e resultado do acesso para registrar consultas sensíveis ou tentativas bloqueadas. O painel administrativo permite consultar os registros com a autorização exigida.')


def footer(canvas, doc):
    canvas.setFont('Resumo',8.5)
    canvas.setFillColor(colors.HexColor('#536879'))
    canvas.drawString(42,24,'Elo | Funcionalidades e trechos de código | 09/10/2026')
    canvas.drawRightString(A4[0]-42,24,str(doc.page))


aprofundar(chapter_index)
SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=36,bottomMargin=42,
                  title='Elo - Funcionalidades com códigos').build(story,onFirstPage=footer,onLaterPages=footer)
from pypdf import PdfReader
print('PDF gerado:', len(PdfReader(str(OUT)).pages), 'paginas')
