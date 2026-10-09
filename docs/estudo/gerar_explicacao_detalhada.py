"""Produz cadernos por arquivo com codigo original e leitura estrutural detalhada.

Nao importa o app, nao acessa banco e nao altera os arquivos estudados.
As explicacoes de fluxo e contexto devem ser lidas junto com GUIA_ELO.md.
"""
import ast
from pathlib import Path
import re

from gerar_referencia import ROOT, purpose

OUT = Path(__file__).resolve().parent
CADERNOS = OUT / 'por_arquivo'

METODOS = {
    'filter': 'restringe os resultados às condições informadas; não grava os registros',
    'exclude': 'retira resultados que correspondem às condições informadas',
    'get': 'obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave',
    'first': 'obtém o primeiro resultado ou None',
    'exists': 'verifica se há pelo menos um resultado',
    'count': 'conta os resultados',
    'create': 'cria e persiste um registro quando usado no manager do model',
    'save': 'persiste a instância; update_fields limita os campos gravados',
    'update': 'no QuerySet grava diretamente os campos dos resultados, sem chamar save de cada instância',
    'delete': 'remove o objeto/conjunto conforme o tipo e as relações envolvidas',
    'get_or_create': 'procura pelas chaves; se não existir, cria usando também defaults',
    'update_or_create': 'procura pelas chaves; atualiza defaults se existir ou cria se não existir',
    'bulk_create': 'grava uma coleção em lote, sem executar save de cada instância',
    'select_for_update': 'solicita bloqueio dos registros no banco durante a transação',
    'select_related': 'inclui relações simples na consulta para reduzir buscas adicionais',
    'prefetch_related': 'carrega relações por buscas adicionais coordenadas',
    'order_by': 'define a ordem; prefixo menos significa ordem descendente',
    'values_list': 'seleciona valores de campos; flat=True produz valores simples para um campo',
    'annotate': 'acrescenta expressões calculadas à consulta',
    'full_clean': 'executa validação explícita de campos, regras do model e integridade pertinente',
    'is_valid': 'valida o formulário e disponibiliza cleaned_data quando válido',
    'set_password': 'transforma a senha em hash para armazenamento',
    'check_password': 'compara a senha informada ao hash existente',
    'refresh_from_db': 'recarrega os valores persistidos para a instância em memória',
    'render': 'combina template e contexto e devolve uma resposta HTML',
    'redirect': 'devolve resposta para o navegador abrir outro endereço',
    'get_object_or_404': 'busca um objeto na consulta fornecida; ausência gera resposta 404',
    'reverse': 'resolve o endereço a partir do nome da rota',
    'now': 'obtém o instante atual; timezone.now respeita o tratamento de fuso do Django',
    'localdate': 'obtém a data no fuso local configurado',
    'atomic': 'cria uma fronteira de transação para gravações coordenadas',
    'assertEqual': 'o teste exige igualdade entre valor obtido e esperado',
    'assertTrue': 'o teste exige que a expressão seja verdadeira',
    'assertFalse': 'o teste exige que a expressão seja falsa',
    'assertContains': 'o teste exige texto na resposta HTTP',
    'assertNotContains': 'o teste exige ausência de texto na resposta HTTP',
    'assertRaises': 'o teste exige a exceção indicada durante o bloco',
    'force_login': 'autentica o cliente de teste sem testar a senha',
    'call_command': 'executa um comando de gerenciamento do Django',
    'append': 'acrescenta um item ao fim da lista',
    'strip': 'remove espaços nas extremidades do texto',
    'lower': 'converte texto para minúsculas',
    'upper': 'converte texto para maiúsculas',
}
OPCOES = {
    'default': 'valor inicial quando não é informado outro',
    'null': 'permite ou impede ausência SQL (NULL)',
    'blank': 'permite ou impede campo vazio na validação',
    'unique': 'exige valor único no banco',
    'primary_key': 'define o identificador principal do registro',
    'max_length': 'limite de comprimento do campo',
    'choices': 'alternativas declaradas para validação e apresentação',
    'related_name': 'nome usado ao consultar a relação pelo lado inverso',
    'on_delete': 'comportamento quando o registro relacionado é excluído',
    'db_column': 'nome da coluna no banco',
    'auto_now_add': 'preenche a data/hora na criação',
    'auto_now': 'atualiza a data/hora no save pertinente',
    'required': 'indica se o formulário exige preenchimento',
    'label': 'texto apresentado ao usuário',
    'help_text': 'orientação apresentada junto ao campo',
    'widget': 'componente de entrada utilizado na tela',
    'update_fields': 'campos específicos que serão persistidos',
    'defaults': 'valores adicionais usados na criação/atualização',
    'name': 'nome identificador desta configuração, rota ou restrição',
    'fields': 'campos usados nesta configuração, índice ou restrição',
}


def code(node):
    return ast.unparse(node)


def describe(value):
    if value is None:
        return 'nenhum valor explícito (None)'
    if isinstance(value, ast.Constant):
        return f'o valor literal `{value.value!r}`'
    if isinstance(value, ast.Name):
        return f'o valor associado ao nome `{value.id}`'
    if isinstance(value, ast.Attribute):
        return f'o atributo `{value.attr}` de `{code(value.value)}`'
    if isinstance(value, ast.Call):
        name = code(value.func)
        suffix = name.split('.')[-1]
        meaning = METODOS.get(suffix)
        explanation = f'a chamada `{name}`'
        if meaning:
            explanation += f', que {meaning}'
        if value.args:
            explanation += '; argumentos posicionais: ' + ', '.join(f'`{code(a)}`' for a in value.args)
        if value.keywords:
            explanation += '; argumentos nomeados: ' + ', '.join(f'`{k.arg or "**"}={code(k.value)}`' for k in value.keywords)
        return explanation
    if isinstance(value, ast.Compare):
        ops = {ast.Eq: 'igual a', ast.NotEq: 'diferente de', ast.Lt: 'menor que', ast.LtE: 'menor ou igual a',
               ast.Gt: 'maior que', ast.GtE: 'maior ou igual a', ast.In: 'contido em', ast.NotIn: 'não contido em',
               ast.Is: 'o mesmo objeto que', ast.IsNot: 'um objeto diferente de'}
        parts = [f'`{code(value.left)}`']
        for op, other in zip(value.ops, value.comparators):
            parts += [ops.get(type(op), code(op)), f'`{code(other)}`']
        return 'a comparação ' + ' '.join(parts)
    if isinstance(value, ast.BoolOp):
        return ('todas as condições' if isinstance(value.op, ast.And) else 'pelo menos uma das condições') + ': ' + ' ; '.join(f'`{code(v)}`' for v in value.values) + ' (com avaliação interrompida assim que o resultado é determinado)'
    if isinstance(value, ast.UnaryOp) and isinstance(value.op, ast.Not):
        return f'a negação de `{code(value.operand)}`'
    if isinstance(value, ast.IfExp):
        return f'`{code(value.body)}` se `{code(value.test)}` for verdadeiro; caso contrário, `{code(value.orelse)}`'
    if isinstance(value, (ast.List, ast.Tuple, ast.Set)):
        return f'uma coleção {type(value).__name__} com {len(value.elts)} itens, na expressão `{code(value)}`'
    if isinstance(value, ast.Dict):
        return f'um dicionário de {len(value.keys)} entradas; as chaves dão nome aos valores associados'
    if isinstance(value, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
        return f'uma coleção/gerador construído por compreensão em `{code(value)}`: percorre as fontes e aplica os filtros declarados'
    if isinstance(value, ast.Subscript):
        return f'o item ou recorte `{code(value.slice)}` de `{code(value.value)}`'
    if isinstance(value, ast.JoinedStr):
        return f'o texto formatado `{code(value)}`, inserindo valores nas partes entre chaves'
    return f'a expressão `{code(value)}`; seus operadores determinam o cálculo'


def stmt_explanation(node):
    if isinstance(node, ast.Import):
        return 'Importa módulos: ' + ', '.join(f'`{n.name}`' + (f' sob o nome `{n.asname}`' if n.asname else '') for n in node.names) + '.'
    if isinstance(node, ast.ImportFrom):
        return f'Importa de `{("." * node.level) + (node.module or "")}` os nomes ' + ', '.join(f'`{n.name}`' + (f' como `{n.asname}`' if n.asname else '') for n in node.names) + '. Pontos iniciais indicam importação relativa ao pacote.'
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        args = code(node.args)
        text = f'Define `{node.name}({args})`. O corpo só executa quando a função/método é chamado.'
        if node.name.startswith('test_'):
            text += ' Cenário do teste: ' + node.name[5:].replace('_', ' ') + '.'
        if node.decorator_list:
            text += ' Decoradores: ' + ', '.join(f'`{code(d)}`' for d in node.decorator_list) + '.'
        return text
    if isinstance(node, ast.ClassDef):
        return f'Define a classe `{node.name}`' + (' herdando de ' + ', '.join(f'`{code(b)}`' for b in node.bases) if node.bases else '') + '. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.'
    if isinstance(node, ast.Assign):
        return 'Associa ' + ', '.join(f'`{code(t)}`' for t in node.targets) + ' a ' + describe(node.value) + '.'
    if isinstance(node, ast.AnnAssign):
        return f'Declara `{code(node.target)}` com indicação de tipo `{code(node.annotation)}` e ' + describe(node.value) + '.'
    if isinstance(node, ast.AugAssign):
        return f'Atualiza `{code(node.target)}` pelo operador da expressão `{code(node)}`. O valor anterior participa do cálculo.'
    if isinstance(node, ast.If):
        return 'Escolhe um caminho verificando ' + describe(node.test) + '. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.'
    if isinstance(node, (ast.For, ast.AsyncFor)):
        return f'Percorre `{code(node.iter)}`; cada item é atribuído a `{code(node.target)}` e executa o corpo. Um else de laço executa quando termina sem break.'
    if isinstance(node, ast.While):
        return f'Repete o bloco enquanto `{code(node.test)}` for verdadeiro.'
    if isinstance(node, (ast.With, ast.AsyncWith)):
        return 'Executa sob os contextos ' + ', '.join(f'`{code(i.context_expr)}`' + (f' como `{code(i.optional_vars)}`' if i.optional_vars else '') for i in node.items) + '. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.'
    if isinstance(node, ast.Try):
        return 'Tenta executar o bloco; except trata os erros indicados, else executa se não houver erro e finally executa ao sair quando presente.'
    if isinstance(node, ast.Return):
        return 'Encerra esta chamada e devolve ' + describe(node.value) + ' ao chamador.'
    if isinstance(node, ast.Raise):
        return ('Interrompe o caminho levantando ' + describe(node.exc) + '.' if node.exc else 'Repropaga a exceção atual; não continua normalmente o bloco.')
    if isinstance(node, ast.Expr):
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            return 'Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.'
        return 'Executa ' + describe(node.value) + '. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.'
    if isinstance(node, ast.Continue):
        return 'Pula o restante da iteração atual e segue para o próximo item do laço.'
    if isinstance(node, ast.Break):
        return 'Encerra o laço atual imediatamente.'
    if isinstance(node, ast.Pass):
        return 'Não executa ação; mantém um bloco sintaticamente válido.'
    if isinstance(node, ast.Assert):
        return f'Exige `{code(node.test)}`; se falso, levanta AssertionError. Não deve substituir autorização em produção.'
    return f'Instrução `{type(node).__name__}`: leia a operação explícita no trecho `{code(node)}`.'


def walk_statements(nodes, result, depth=0):
    for n in nodes:
        result += [f'**Linha {n.lineno} — {type(n).__name__}** (nível {depth} do bloco).', '', stmt_explanation(n), '']
        if isinstance(n, (ast.Assign, ast.AnnAssign)):
            value = n.value
            if isinstance(value, ast.Call):
                for kw in value.keywords:
                    meaning = OPCOES.get(kw.arg, 'parâmetro nomeado passado à chamada; seu significado depende da função chamada')
                    result += [f'- `{kw.arg or "**"}={code(kw.value)}`: {meaning}.']
                result += ['']
            if isinstance(value, ast.Dict):
                for key, val in zip(value.keys, value.values):
                    result += [f'- Chave `{code(key) if key else "**"}`: recebe {describe(val)}.']
                result += ['']
        for attribute in ('body', 'orelse', 'finalbody'):
            children = getattr(n, attribute, None)
            if children:
                result += [f'Bloco `{attribute}` da linha {n.lineno}:', '']
                walk_statements(children, result, depth + 1)
        for handler in getattr(n, 'handlers', []):
            result += [f'Erro tratado: `{code(handler.type) if handler.type else "qualquer exceção"}`' + (f' sob o nome `{handler.name}`.' if handler.name else '.'), '']
            walk_statements(handler.body, result, depth + 1)


def html_explanation(line):
    parts = []
    if '{% extends' in line: parts.append('Herda a estrutura do template-base indicado.')
    if '{% block' in line: parts.append('Abre uma região que o template filho preenche.')
    if '{% endblock' in line: parts.append('Fecha a região de conteúdo do template.')
    if '{% csrf_token' in line: parts.append('Inclui o token de proteção da submissão POST; a view ainda precisa verificar autorização.')
    if '{% url' in line: parts.append('Resolve a rota Django pelo nome indicado.')
    if '{% static' in line: parts.append('Resolve o caminho do recurso estático, como imagem ou CSS.')
    if '{% if' in line or '{% elif' in line: parts.append('Exibe conteúdo conforme a condição. Isso organiza a tela e não protege sozinho a rota.')
    if '{% for' in line: parts.append('Repete a marcação para cada item da coleção recebida.')
    if '{% empty' in line: parts.append('Apresenta o caso em que a coleção do laço está vazia.')
    if '{{' in line: parts.append('Exibe os valores indicados pelo contexto; os filtros após | transformam a apresentação.')
    if '<form' in line: parts.append('Abre formulário: method define envio GET/POST e action define o destino; sem action usa a página atual.')
    if '<input' in line or '<select' in line or '<textarea' in line: parts.append('Define campo de entrada; name vira a chave recebida no servidor, type define o comportamento, value define o valor inicial/enviado.')
    if '<button' in line: parts.append('Define ação clicável; type=submit envia o formulário, type=button depende do comportamento do navegador/script.')
    if '<a ' in line: parts.append('Define link; href é o endereço ou âncora que o navegador abre.')
    if '<script' in line: parts.append('Inicia JavaScript executado no navegador, não no servidor Python.')
    if 'addEventListener' in line: parts.append('Conecta um evento do navegador à função indicada.')
    if 'querySelector' in line or 'getElementById' in line: parts.append('Seleciona elemento HTML para leitura ou alteração pelo script.')
    if 'classList' in line: parts.append('Altera classes CSS para atualizar a apresentação/interação.')
    if 'setAttribute' in line: parts.append('Atualiza um atributo do elemento, inclusive estados de acessibilidade quando indicado.')
    if '<link' in line: parts.append('Vincula recurso externo ao documento, como folha de estilos ou ícone.')
    if '<img' in line: parts.append('Exibe imagem; src aponta o arquivo e alt fornece texto alternativo.')
    if '<!--' in line or '{% comment' in line: parts.append('Inicia comentário/documentação que não é uma regra do servidor.')
    if '{% end' in line: parts.append('Encerra o bloco de template correspondente, como condição, laço ou comentário.')
    if '{% else' in line: parts.append('Inicia o caminho alternativo da condição anterior.')
    if '<h' in line and re.search(r'<h[1-6]\b', line): parts.append('Marca um título; o número determina seu nível na hierarquia do documento.')
    if '<p' in line: parts.append('Agrupa conteúdo em um parágrafo.')
    if '<section' in line: parts.append('Agrupa uma seção temática da página.')
    if '<div' in line: parts.append('Agrupa elementos para estrutura e aplicação de estilos; class/id permitem seleção por CSS e JavaScript.')
    if '<ul' in line or '<ol' in line: parts.append('Abre lista; ul é não numerada e ol é numerada.')
    if '<li' in line: parts.append('Define um item da lista.')
    if '<table' in line or '<tr' in line or '<td' in line or '<th' in line: parts.append('Organiza dados tabulares: table é a tabela, tr é linha, td é célula e th é cabeçalho.')
    if '<label' in line: parts.append('Apresenta o rótulo de um campo; for liga ao id do controle.')
    if 'const ' in line or 'let ' in line: parts.append('Declara uma variável JavaScript: const impede reatribuir o vínculo e let permite reatribuição.')
    if 'if (' in line: parts.append('Executa o bloco JavaScript apenas quando a condição indicada for verdadeira.')
    if 'return' in line and '{%' not in line: parts.append('Quando esta linha pertence ao script, return encerra a função e devolve o valor indicado.')
    if 'function' in line or '=>' in line: parts.append('Declara uma função JavaScript/callback; só executa quando chamada ou acionada pelo evento associado.')
    if line.strip().startswith('</'): parts.append('Fecha o elemento HTML aberto anteriormente, delimitando seu conteúdo.')
    return ' '.join(parts) or 'Marcação/texto ou continuação do bloco anterior. A posição, o fechamento das tags e os atributos conectam esta linha à estrutura exibida no trecho completo.'


def main():
    CADERNOS.mkdir(parents=True, exist_ok=True)
    reference = (OUT / 'REFERENCIA_CODIGO.md').read_text(encoding='utf-8')
    files = sorted(set(Path(p) for p in re.findall(r'\]\(<([^>]+)>\)', reference) if not re.search(r':\d+$', p)))
    index = ['# Elo explicado por arquivo e por bloco', '',
             'Material de 09/10/2026. Comece pelo [guia de arquitetura e fluxos](GUIA_ELO.md). '
             'Aqui cada arquivo tem seu caderno com código integral, trechos organizados e leitura de suas instruções.', '',
             'As explicações de instruções foram extraídas por análise estrutural: explicam operações visíveis no código, '
             'sem executar o sistema. A intenção dos fluxos é explicada no guia. Nomes de métodos iguais podem ter '
             'significados diferentes conforme o objeto; confirme o tipo e os chamadores na referência. '
             'Comentários antigos não prevalecem sobre o corpo executado.', '',
             'Nenhum arquivo do sistema foi alterado. .env real, banco, bibliotecas instaladas e arquivos binários não estão copiados.', '',
             '## Ordem de leitura', '',
             '1. Guia, Python básico e configuração.',
             '2. Models, cadastro, login e perfis.',
             '3. Rotas e views com seus templates.',
             '4. Serviços de hemocentros, pedidos, estoque e compatibilidade.',
             '5. Catálogos, formulários, serviço e motor da triagem.',
             '6. Auditoria, sinais, admin, notificações, CSS.',
             '7. Migrations, testes e comando de contas fictícias.', '',
             '## Todos os arquivos', '', '| Arquivo | Explicação detalhada |', '| --- | --- |']
    statements = 0
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        slug = rel.replace('/', '__').replace('.', '_') + '.md'
        text = path.read_text(encoding='utf-8-sig')
        lines = text.splitlines()
        result = [f'# {rel}: código e explicação', '',
                  '[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)', '',
                  f'**Responsabilidade:** {purpose(path)}', '',
                  f'**Arquivo original:** [{rel}](<{path.as_posix()}>). As linhas referem-se à cópia desta data.', '',
                  '## Código integral', '', '``````' + (path.suffix[1:] if path.suffix in {'.py', '.html', '.css'} else 'text'), text.rstrip(), '``````', '']
        if path.suffix == '.py':
            tree = ast.parse(text)
            result += ['## Leitura por partes', '',
                       'Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação '
                       'segue também os blocos internos de função, condição, repetição e tratamento de erros. '
                       'Nível indica profundidade, não ordem de execução entre caminhos alternativos.', '']
            for n in tree.body:
                label = getattr(n, 'name', None) or type(n).__name__
                start = min([n.lineno, *[d.lineno for d in getattr(n, 'decorator_list', [])]])
                result += [f'### {label} — linhas {start} a {n.end_lineno}', '', '```python',
                           '\n'.join(lines[start-1:n.end_lineno]), '```', '', '**Explicação deste trecho:**', '']
                walk_statements([n], result)
            statements += sum(isinstance(n, ast.stmt) for n in ast.walk(tree))
            comments = [(i, l.strip()) for i, l in enumerate(lines, 1) if l.lstrip().startswith('#')]
            if comments:
                result += ['## Comentários', '', 'Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.', '',
                           *[f'- Linha {i}: `{l}`' for i, l in comments], '']
        elif path.suffix == '.html':
            result += ['## Leitura da tela, linha por linha', '']
            for i, line in enumerate(lines, 1):
                if line.strip():
                    result += [f'### Linha {i}', '', '```html', line, '```', '', html_explanation(line), '']
        elif path.suffix == '.css':
            result += ['## Leitura das regras visuais', '',
                       'Seletores escolhem os elementos; declarações definem aparência. Regras posteriores e maior '
                       'especificidade podem prevalecer. @media limita regras ao tamanho/condição indicado.', '']
            for selector, body in re.findall(r'([^{}]+)\{([^{}]*)\}', re.sub(r'/\*.*?\*/', '', text, flags=re.S)):
                result += [f'### Seletor `{selector.strip()}`', '', '```css', selector.strip() + ' {' + body + '}', '```', '']
                for declaration in body.split(';'):
                    if ':' in declaration:
                        prop, val = declaration.split(':', 1)
                        meaning = {'display': 'modo de organização dos elementos', 'color': 'cor do texto', 'background': 'fundo',
                                   'background-color': 'cor de fundo', 'margin': 'espaço externo', 'padding': 'espaço interno',
                                   'gap': 'intervalo entre itens', 'font-size': 'tamanho das letras', 'font-weight': 'peso das letras',
                                   'border': 'borda', 'border-radius': 'arredondamento', 'width': 'largura', 'height': 'altura',
                                   'max-width': 'limite máximo de largura', 'position': 'modelo de posicionamento',
                                   'align-items': 'alinhamento no eixo transversal', 'justify-content': 'distribuição no eixo principal',
                                   'grid-template-columns': 'colunas da grade', 'flex-direction': 'direção dos itens flex',
                                   'transition': 'transição visual entre valores', 'box-shadow': 'sombra',
                                   'line-height': 'altura da linha de texto', 'z-index': 'ordem de sobreposição'}.get(prop.strip(), 'propriedade CSS aplicada ao seletor')
                        result += [f'- `{prop.strip()}: {val.strip()}`: define {meaning}.']
                result += ['']
        else:
            result += ['## Como interpretar este arquivo', '',
                       'Este arquivo contém documentação ou configuração textual. Leia as seções e os valores no bloco integral. '
                       'Documentação descreve intenção; compare ao código atual. Em requirements, cada pacote e versão determina '
                       'a instalação; em .gitignore, cada padrão controla o que Git ignora; em .env.example, os nomes mostram '
                       'as variáveis esperadas, sem precisar ler os segredos do .env real.', '']
        (CADERNOS / slug).write_text('\n'.join(result) + '\n', encoding='utf-8')
        index += [f'| `{rel}` | [Código e explicação](por_arquivo/{slug}) |']
    index += ['', '## Como conferir se entendeu um trecho', '',
              'Leia o código, acompanhe as linhas explicadas e volte à referência para localizar os chamadores. '
              'Depois responda: qual entrada recebe, o que valida, que dados altera, que valor devolve e qual teste demonstra o comportamento?', '',
              f'Cobertura: {len(files)} arquivos; {statements} instruções Python identificadas. '
              'Todos os arquivos têm sua cópia integral; Python tem leitura dos blocos, HTML tem leitura das linhas '
              'e CSS tem leitura das declarações. Arquivos vazios são marcadores de pacote. '
              'Exclusões: segredos, binários e código de dependências externas.']
    (OUT / 'LEIA_PRIMEIRO.md').write_text('\n'.join(index) + '\n', encoding='utf-8')
    print(f'{len(files)} cadernos gerados; {statements} instrucoes Python.')


if __name__ == '__main__':
    main()
