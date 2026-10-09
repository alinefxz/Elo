"""Gera material de consulta sem importar Django nem ler o .env real.

Execute com Python a partir de qualquer pasta. A extracao descreve estrutura
do codigo; a explicacao dos fluxos esta em GUIA_ELO.md.
"""

import ast
from collections import Counter
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
DESCRICOES = {
    'models.py': 'Entidades persistidas, relacionamentos, estados e integridade do banco.',
    'views.py': 'Entrada HTTP: permissoes, formularios, chamadas de servico e respostas/telas.',
    'forms.py': 'Campos e validacoes de cadastro, login, estoque, pedidos e filtros.',
    'urls.py': 'Associacao entre endereco, view e nome de rota.',
    'settings.py': 'Configuracao de apps, banco, middleware, templates e autenticacao.',
    'settings_test.py': 'Configuracao de banco temporario para os testes.',
    'admin.py': 'Telas do Django admin, autorizacoes e auditoria de operacoes.',
    'auditoria.py': 'Registro de eventos e observacao de acessos sensiveis.',
    'signals.py': 'Registro automatico das falhas de autenticacao.',
    'apps.py': 'Inicializacao do app e conexao dos sinais.',
    'estoque.py': 'Cadastro, movimentacao, estado publico e alertas de estoque.',
    'compatibilidade.py': 'Tabela, normalizacao, elegibilidade, frequencia e preferencia de convocacao.',
    'pedidos.py': 'Publicacao institucional e alertas de pedidos compativeis.',
    'validacao_pedido.py': 'Solicitacao, decisao, historico e autorizacao de pedidos.',
    'validacao_hemocentro.py': 'Estados institucionais, decisao e historico de hemocentros.',
    'triagem.py': 'Calculos iniciais da triagem; compare seus chamadores ao motor atual.',
    'triagem_motor.py': 'Calculo da orientacao a partir das respostas e regras dos catalogos.',
    'triagem_servico.py': 'Andamento, respostas, revisao, persistencia e conclusao de triagem.',
    'triagem_forms.py': 'Formulario dinamico correspondente a cada pergunta.',
    'triagem_catalogo.py': 'Acesso e validacao dos catalogos versionados.',
    'triagem_catalogo_extensa.py': 'Declaracoes de todas as perguntas e regras da extensa.',
    'triagem_catalogo_simplificada.py': 'Declaracoes das perguntas rapidas e abertura de detalhes.',
    'criar_perfis_teste.py': 'Comando local de contas ficticias preservando registros existentes.',
    'manage.py': 'Entrada dos comandos do Django.',
    'wsgi.py': 'Entrada de servidor pelo protocolo WSGI.',
    'asgi.py': 'Entrada de servidor pelo protocolo ASGI.',
}


def link(path, line=None):
    target = path.as_posix() + (f':{line}' if line else '')
    return f'[{path.relative_to(ROOT).as_posix()}](<{target}>)'


def expr(node):
    return ast.unparse(node)


def own_nodes(node):
    """Percorre o corpo sem atribuir chamadas de metodos internos a classe pai."""
    def visit(item):
        yield item
        for child in ast.iter_child_nodes(item):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            yield from visit(child)
    for statement in node.body:
        if not isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            yield from visit(statement)


def symbols(node, prefix=''):
    for child in getattr(node, 'body', []):
        if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            name = prefix + child.name
            yield name, child
            yield from symbols(child, name + '.')


def purpose(path):
    if 'migrations' in path.parts and path.suffix == '.py' and path.name != '__init__.py':
        return 'Etapa versionada da evolucao do banco; veja dependencias e operacoes abaixo.'
    if path.name.startswith('test') and path.suffix == '.py':
        return 'Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.'
    if path.name == '__init__.py':
        return 'Marcador de pacote Python; pode nao executar nenhuma instrucao.'
    if path.suffix == '.html':
        return 'Template de apresentacao; compare variaveis recebidas e view que o renderiza.'
    if path.suffix == '.css':
        return 'Regras visuais de seletores, componentes e tamanhos de tela.'
    return DESCRICOES.get(path.name, 'Documento/configuracao complementar; consulte o conteudo integral.')


def main():
    files = set()
    for directory in ('accounts', 'config', 'templates', 'elo_front', 'docs/superpowers'):
        for path in (ROOT / directory).rglob('*'):
            if path.is_file() and path.suffix.lower() in {'.py', '.html', '.css', '.md', '.txt'}:
                if '__pycache__' not in path.parts:
                    files.add(path)
    for name in ('manage.py', 'requirements.txt', 'README.md', 'TESTAR_PERFIS.md', '.gitignore', '.env.example'):
        path = ROOT / name
        if path.exists():
            files.add(path)
    files = sorted(files, key=lambda p: p.relative_to(ROOT).as_posix())
    contents = {p: p.read_text(encoding='utf-8-sig') for p in files}
    parsed = {p: ast.parse(text) for p, text in contents.items() if p.suffix == '.py'}
    callers = {}
    for path, tree in parsed.items():
        for qualified, node in symbols(tree):
            if not isinstance(node, ast.ClassDef):
                for item in own_nodes(node):
                    if isinstance(item, ast.Call):
                        target = expr(item.func).split('.')[-1]
                        callers.setdefault(target, set()).add((path, qualified, node.lineno))

    ref = ['# Referencia integral do codigo do Elo', '',
           'Complemento de [GUIA_ELO.md](GUIA_ELO.md). Extracao estrutural dos arquivos locais em 09/10/2026.', '',
           'Cada chamada listada existe no corpo; isso nao significa que todos os ramos executem juntos. '
           'Chamadores sao candidatos por nome, nao um resolvedor completo de tipos: metodos com nomes '
           'iguais podem pertencer a classes diferentes. Docstrings sao do proprio codigo e podem estar antigas.', '',
           'Nao inclui .env real, banco, ambiente virtual, arquivos binarios ou codigo das dependencias. '
           'Arquivos de suporte vazios tambem estao no inventario. A copia completa esta em [CODIGO_COMPLETO.md](CODIGO_COMPLETO.md).', '',
           '## Inventario de arquivos', '', '| Arquivo | Linhas | Papel |', '| --- | ---: | --- |']
    snapshot = ['# Codigo completo para estudo', '',
                'Copia numerada em 09/10/2026. Leia a explicacao em [GUIA_ELO.md](GUIA_ELO.md) e o indice em '
                '[REFERENCIA_CODIGO.md](REFERENCIA_CODIGO.md). Os numeros antes de `|` sao linhas, nao fazem parte do codigo. '
                'Conteudo copiado nao deve ser executado diretamente. Nenhum segredo do .env real foi lido.', '']
    for path in files:
        lines = contents[path].splitlines()
        ref.append(f'| {link(path)} | {len(lines)} | {purpose(path)} |')
    total_symbols = 0
    for path in files:
        text = contents[path]
        lines = text.splitlines()
        ref += ['', f'## {path.relative_to(ROOT).as_posix()}', '', purpose(path), '', f'Original: {link(path)}.', '']
        snapshot += [f'## {path.relative_to(ROOT).as_posix()}', '', f'Original: {link(path)}.', '', '``````text']
        snapshot += [f'{i:5} | {line}' for i, line in enumerate(lines, 1)]
        snapshot += ['``````', '']
        if not lines:
            ref.append('Arquivo vazio: organiza o pacote, sem algoritmo para estudar.')
        if path in parsed:
            tree = parsed[path]
            imports = [expr(n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
            if imports:
                ref += ['**Dependencias importadas:**', '', '```python', *imports, '```', '']
            definitions = list(symbols(tree))
            total_symbols += len(definitions)
            for qualified, node in definitions:
                isclass = isinstance(node, ast.ClassDef)
                ref += [f'### {qualified}', '', f'Linha {node.lineno}: {link(path, node.lineno)}.', '']
                if isclass:
                    ref += [f"Classe; herda de: {', '.join(expr(b) for b in node.bases) or 'nenhuma classe declarada'}.", '']
                else:
                    ref += ['```python', f'def {node.name}({expr(node.args)}):', '```', '']
                    if node.name.startswith('test_'):
                        ref += ['Cenario descrito pelo nome: ' + node.name[5:].replace('_', ' ') + '.', '']
                doc = ast.get_docstring(node)
                if doc:
                    ref += ['**Explicacao presente no codigo:**', '', *['> ' + s for s in doc.splitlines()], '']
                if node.decorator_list:
                    ref += ['**Decoradores:** ' + ', '.join(f'`{expr(d)}`' for d in node.decorator_list) + '.', '']
                direct = list(own_nodes(node))
                calls = sorted(set(expr(n.func) for n in direct if isinstance(n, ast.Call)))
                returns = sorted(set(expr(n.value) if n.value else 'None' for n in direct if isinstance(n, ast.Return)))
                errors = sorted(set(expr(n.exc) for n in direct if isinstance(n, ast.Raise) and n.exc))
                if calls:
                    ref += ['**Chamadas utilizadas no corpo:** ' + ', '.join(f'`{c}`' for c in calls) + '.', '']
                if returns:
                    ref += ['**Expressoes de retorno (dependem do caminho):**', '', *[f'- `{r}`' for r in returns], '']
                if errors:
                    ref += ['**Excecoes levantadas:**', '', *[f'- `{r}`' for r in errors], '']
                branches = Counter(type(n).__name__ for n in direct if isinstance(n, (ast.If, ast.For, ast.While, ast.Try, ast.With)))
                if branches:
                    ref += ['**Estrutura de controle:** ' + ', '.join(f'{kind}: {qty}' for kind, qty in branches.items()) + '. Abra o original para seguir as condicoes na ordem.', '']
                if isclass:
                    assigns = [n for n in node.body if isinstance(n, (ast.Assign, ast.AnnAssign))]
                    if assigns:
                        ref += ['**Atributos/campos declarados diretamente:**', '', '```python', *[expr(n) for n in assigns], '```', '']
                matches = sorted(callers.get(node.name, set()), key=lambda r: (str(r[0]), r[2]))
                matches = [(p, q, l) for p, q, l in matches if not (p == path and q == qualified)]
                if matches:
                    ref += ['**Onde aparece uma chamada com este nome:**', '', *[f'- `{q}` em {link(p, l)}.' for p, q, l in matches], '']
            routes = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and expr(n.func) == 'path']
            if routes:
                ref += ['### Rotas declaradas', '', '```python', *[expr(n) for n in routes], '```', '']
            constants = [expr(n) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id.isupper() for t in n.targets)]
            if constants:
                ref += ['### Constantes e dados declarados', '',
                        'Estas atribuicoes sao parte da regra/configuracao. Catalogos grandes ficam integrais na copia do codigo.', '']
                for n in tree.body:
                    if isinstance(n, ast.Assign):
                        for target in n.targets:
                            if isinstance(target, ast.Name) and target.id.isupper():
                                ref += [f'- `{target.id}`: linha {n.lineno}; valor declarado em {link(path, n.lineno)}.']
        elif path.suffix == '.html':
            tags = sorted(set(re.findall(r'{%\s*(.*?)\s*%}', text, re.S)))
            variables = sorted(set(re.findall(r'{{\s*(.*?)\s*}}', text, re.S)))
            views = [(p, i) for p, content in contents.items() if p.suffix == '.py' for i, line in enumerate(content.splitlines(), 1)
                     if (path.relative_to(ROOT / 'templates').as_posix() if 'templates' in path.parts and path.is_relative_to(ROOT / 'templates') else 'not-a-template-reference') in line]
            ref += ['**Instrucoes Django no HTML:**', '', *[f'- `{t}`' for t in tags], '',
                    '**Valores exibidos:**', '', *[f'- `{v}`' for v in variables], '']
            if views:
                ref += ['**Referencias ao caminho do template no Python:**', '', *[f'- {link(p, i)}' for p, i in views], '']
            scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', text, re.S)
            if scripts:
                ref += ['**JavaScript embutido:** leia os eventos e seletores na copia integral; ele organiza interacao no navegador, sem substituir autorizacao no servidor.', '']
        elif path.suffix == '.css':
            selectors = [s.strip() for s in re.findall(r'([^{}]+)\{', re.sub(r'/\*.*?\*/', '', text, flags=re.S))]
            ref += ['**Seletores/blocos visuais declarados:**', '', *[f'- `{s}`' for s in selectors], '',
                    'Leia propriedades dentro de cada bloco: layout, cores, espacos, tipografia e regras responsivas. A copia integral preserva todos os valores.', '']
    ref += ['', '## Cobertura desta referencia', '',
            f'{len(files)} arquivos de texto e {total_symbols} definicoes de classes/funcoes/metodos foram indexados. '
            'A copia completa contem todos os arquivos do inventario, incluindo arquivos sem definicoes Python. '
            'Nao foram lidos .env real, Git interno ou dependencias instaladas.']
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'REFERENCIA_CODIGO.md').write_text('\n'.join(ref) + '\n', encoding='utf-8')
    (OUT / 'CODIGO_COMPLETO.md').write_text('\n'.join(snapshot) + '\n', encoding='utf-8')
    print(f'{len(files)} arquivos; {total_symbols} definicoes; {sum(len(t.splitlines()) for t in contents.values())} linhas originais.')


if __name__ == '__main__':
    main()
