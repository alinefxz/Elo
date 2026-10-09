"""Compila o guia e os cadernos em um PDF navegavel para estudo."""
from pathlib import Path
from html import escape
import json
import re
import textwrap

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                PageBreak, Preformatted, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[2]
STUDY = Path(__file__).resolve().parent
DEST = ROOT / 'output' / 'pdf' / 'Elo_Codigo_Explicado.pdf'
DEST.parent.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont('Study', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('StudyBold', 'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Code', 'C:/Windows/Fonts/consola.ttf'))
pdfmetrics.registerFontFamily('Study', normal='Study', bold='StudyBold', italic='Study', boldItalic='StudyBold')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle('TextStudy', fontName='Study', fontSize=9.4, leading=13.3, spaceAfter=6,
                          textColor=colors.HexColor('#243447'), splitLongWords=True))
styles.add(ParagraphStyle('Chapter', fontName='StudyBold', fontSize=19, leading=24, spaceBefore=10,
                          spaceAfter=13, textColor=colors.HexColor('#113E59'), keepWithNext=True))
styles.add(ParagraphStyle('SubStudy', fontName='StudyBold', fontSize=13, leading=17, spaceBefore=12,
                          spaceAfter=7, textColor=colors.HexColor('#155F79'), keepWithNext=True))
styles.add(ParagraphStyle('BlockStudy', fontName='StudyBold', fontSize=10.5, leading=14, spaceBefore=10,
                          spaceAfter=5, keepWithNext=True, splitLongWords=True))
styles.add(ParagraphStyle('SmallStudy', parent=styles['TextStudy'], fontSize=8, leading=10.5))
styles.add(ParagraphStyle('CodeStudy', fontName='Code', fontSize=7.8, leading=10.1,
                          backColor=colors.HexColor('#F2F5F7'), borderPadding=5, spaceAfter=6))


def rich(text):
    text = re.sub(r'\[([^\]]*)\]\(<[^>]*>\)', r'\1', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = text.replace('\u2011', '-').replace('\u2013', '-').replace('\u2014', '-')
    pieces = re.split(r'(`[^`]*`)', text)
    rendered = ''
    for piece in pieces:
        if piece.startswith('`') and piece.endswith('`'):
            rendered += '<font name="Code" size="8.3">' + escape(piece[1:-1]) + '</font>'
        else:
            for old, new in {
                'leitura estrutural': 'explicação do que cada parte do código faz',
                'operações observáveis': 'ações que aparecem no código',
                'instruções': 'comandos',
                'argumentos posicionais': 'dados enviados à função, na ordem indicada',
                'argumentos nomeados': 'dados enviados à função com seus nomes',
                'atribuição explícita': 'guardar o resultado em uma variável',
                'Associa ': 'Guarda ',
                'atributo': 'informação ou configuração',
                'persiste': 'salva no banco',
                'persistidos': 'salvos no banco',
                'persistência': 'salvamento dos dados',
                'persistidas': 'salvas no banco',
                'persistir': 'salvar no banco',
                'instância': 'cópia criada a partir da classe',
                'ao chamador': 'à parte do programa que chamou a função',
                'pelo chamador': 'pela parte do programa que chamou a função',
                'chamadores': 'partes do programa que chamam a função',
                'literal': 'escrito diretamente no código',
                'negação de': 'o contrário de',
                'coleção': 'conjunto de itens',
                'coleções': 'conjuntos de itens',
                'iteração': 'repetição',
                'laço': 'repetição',
                'Repropaga a exceção atual': 'Passa adiante o erro que já aconteceu',
                'levantando': 'informando o erro',
                'sintaticamente válido': 'aceito pelas regras da linguagem',
                'fronteira de transação': 'grupo de alterações no banco que devem ser concluídas juntas',
                'transação': 'operação que agrupa alterações no banco',
                'rollback': 'cancelamento das alterações do grupo',
                'requisição': 'pedido enviado pelo navegador ao servidor',
                'renderiza': 'monta e mostra',
                'renderizada': 'montada e exibida',
                'renderização': 'montagem da página',
                'docstrings': 'textos explicativos dentro do código',
                'aliases': 'nomes alternativos',
                'alias': 'nome alternativo',
                'integridade': 'consistência dos dados',
                'elegibilidade': 'condições para receber a convocação',
                'querysets': 'conjuntos de resultados de uma busca no banco',
                'parâmetro nomeado passado à chamada; seu significado depende da função chamada': 'dado enviado com um nome; a função chamada define como ele será usado',
                'nível': 'posição dentro',
                'ImportFrom': 'Trazer recursos de outro arquivo',
                'Import -': 'Importação -',
                'FunctionDef': 'Função',
                'AsyncFunctionDef': 'Função assíncrona',
                'ClassDef': 'Classe',
                'AnnAssign': 'Variável com tipo indicado',
                'AugAssign': 'Atualizar uma variável',
                'Assign': 'Guardar um valor',
                'Expr': 'Texto explicativo ou chamada',
                'Return': 'Devolver resultado',
                'Raise': 'Informar um erro',
                'Continue': 'Passar ao próximo item',
                'Break': 'Encerrar a repetição',
                'Pass': 'Bloco sem ação',
                'Try': 'Tratar possíveis erros',
                'While': 'Repetir enquanto a condição for atendida',
                'For': 'Percorrer os itens',
                'With': 'Executar dentro de uma operação controlada',
                'If': 'Verificar uma condição',
            }.items():
                if old[0].isupper() and old.isalpha():
                    piece = re.sub(r'\b' + re.escape(old) + r'\b', lambda match: new, piece)
                else:
                    piece = piece.replace(old, new)
            value = escape(piece)
            value = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', value)
            rendered += value
    return rendered


class StudyDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(str(filename), pagesize=A4, rightMargin=40, leftMargin=40,
                         topMargin=48, bottomMargin=44, title='Elo - Codigo explicado, parte por parte',
                         author='Material de estudo do projeto Elo', pageCompression=1)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='main',
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='study', frames=frame, onPage=self.page_header))

    def beforeDocument(self):
        self.heading_number = 0
        self.chapter = 'Elo - estudo do codigo'

    def page_header(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Study', 8)
        canvas.setFillColor(colors.HexColor('#536879'))
        canvas.drawString(40, A4[1]-29, 'ELO | CODIGO EXPLICADO')
        canvas.drawRightString(A4[0]-40, A4[1]-29, '09/10/2026')
        canvas.setStrokeColor(colors.HexColor('#DDE5EA'))
        canvas.line(40, A4[1]-35, A4[0]-40, A4[1]-35)
        canvas.drawString(40, 24, 'Guia + codigo + leitura por partes | Projeto local')
        canvas.drawRightString(A4[0]-40, 24, str(doc.page))
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in ('Chapter', 'SubStudy'):
            level = 0 if flowable.style.name == 'Chapter' else 1
            # Only guide subsections enter the TOC; file internals remain in chapters.
            if level == 1 and not getattr(flowable, 'toc_entry', False):
                return
            key = f'heading_{self.heading_number}'
            self.heading_number += 1
            title = flowable.getPlainText()
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title, key, level=level, closed=True)
            self.notify('TOCEntry', (level, title, self.page, key))


def code_block(lines, story):
    wrapped = []
    for line in lines:
        # Wrap long display lines rather than clip; never changes original source files.
        line = line.expandtabs(4)
        if len(line) <= 108:
            wrapped.append(line)
        else:
            indent = ' ' * min(18, len(line)-len(line.lstrip()) + 4)
            wrapped.extend(textwrap.wrap(line, width=108, subsequent_indent=indent,
                                        replace_whitespace=False, drop_whitespace=False,
                                        break_long_words=True, break_on_hyphens=False))
    for i in range(0, len(wrapped), 28):
        story.append(Preformatted('\n'.join(wrapped[i:i+28]), styles['CodeStudy']))


def parse_markdown(text, story, guide=False):
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        fence = re.match(r'^(`{3,})', line)
        if fence:
            token = fence.group(1)
            body = []
            i += 1
            while i < len(lines) and not lines[i].startswith(token):
                body.append(lines[i])
                i += 1
            code_block(body, story)
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+', c) for c in cells):
                    rows.append([Paragraph(rich(c), styles['SmallStudy']) for c in cells])
                i += 1
            if rows:
                columns = max(len(r) for r in rows)
                for row in rows:
                    row.extend([Paragraph('', styles['SmallStudy'])] * (columns-len(row)))
                table = Table(rows, colWidths=[(A4[0]-80)/columns]*columns, repeatRows=1, hAlign='LEFT')
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2EDF2')),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('LINEBELOW', (0,0), (-1,0), .5, colors.HexColor('#B0C6D0')),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                ]))
                story += [table, Spacer(1,8)]
            continue
        heading = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading:
            level = len(heading.group(1))
            style = styles['Chapter'] if level == 1 else styles['SubStudy'] if level == 2 else styles['BlockStudy']
            para = Paragraph(rich(heading.group(2)), style)
            para.toc_entry = guide
            story.append(para)
            i += 1
            continue
        bullet = re.match(r'^([-*]|\d+\.)\s+(.*)', line)
        if bullet:
            label = '-' if bullet.group(1) in ('-', '*') else bullet.group(1)
            story.append(Paragraph(rich(bullet.group(2)), styles['TextStudy'], bulletText=label))
            i += 1
            continue
        paragraph = []
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,6}\s|`{3,}|\||[-*]\s|\d+\.\s)', lines[i]):
            paragraph.append(lines[i].lstrip('> '))
            i += 1
        if paragraph:
            story.append(Paragraph(rich(' '.join(paragraph)), styles['TextStudy']))


def main():
    story = [Spacer(1,95), Paragraph('ELO', styles['Chapter']),
             Paragraph('Código explicado<br/>parte por parte', ParagraphStyle('Cover', parent=styles['Chapter'], fontSize=29, leading=35)),
             Spacer(1,22), Paragraph('Da configuração às telas, do banco às regras de negócio.', styles['SubStudy']),
             Paragraph('Guia de estudo com código Python, HTML e CSS, leitura dos blocos, modelos, migrations e testes.', styles['TextStudy']),
             Spacer(1,28), Paragraph('Base: código local em 09/10/2026.<br/>96 arquivos de projeto e 3.954 instruções Python identificadas.', styles['TextStudy']),
             Paragraph('Cada capítulo apresenta os códigos e explica o que eles fazem. O guia inicial mostra como as partes se conectam e para que cada uma serve.', styles['SmallStudy']),
             PageBreak(), Paragraph('Como estudar este documento', styles['Chapter']),
             Paragraph('Leia o guia inicial para entender o sistema. Depois escolha o arquivo no sumário, leia o trecho de código e acompanhe a explicação imediatamente abaixo. Use as linhas indicadas para conferir no arquivo original. O sumário e os marcadores laterais permitem navegar pelos capítulos.', styles['TextStudy']),
             Paragraph('Código longo pode continuar na linha seguinte apenas para caber na página; o arquivo original não foi modificado. A numeração de linha nas explicações corresponde ao original. Contas, banco, .env real e bibliotecas externas não foram incluídos. Documentos antigos são apresentados como contexto e podem divergir das regras atuais.', styles['TextStudy']),
             Paragraph('Os nomes técnicos do código foram mantidos para você conseguir encontrá-los nos arquivos. As explicações usam palavras mais simples. Comentários antigos podem descrever algo diferente do funcionamento atual.', styles['TextStudy']),
             PageBreak(), Paragraph('Sumário', styles['Chapter'])]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle('TOC0', fontName='Study', fontSize=9, leading=12, spaceBefore=5),
                       ParagraphStyle('TOC1', fontName='Study', fontSize=8.4, leading=11, leftIndent=13, spaceBefore=2)]
    story += [toc, PageBreak()]
    parse_markdown((STUDY / 'GUIA_ELO.md').read_text(encoding='utf-8'), story, guide=True)
    files = sorted((STUDY / 'por_arquivo').glob('*.md'))
    for path in files:
        story.append(PageBreak())
        text = path.read_text(encoding='utf-8')
        # Python code is already repeated adjacent to block explanations; omit the redundant integral copy.
        if ': código e explicação' in text.splitlines()[0] and '_py.md' in path.name:
            start = text.index('## Código integral')
            end = text.find('## Leitura por partes', start)
            if end >= 0:
                text = text[:start] + text[end:]
        text = re.sub(r'^\[Voltar ao índice\].*$', 'Capítulo do arquivo original. Consulte o sumário e os marcadores do PDF.', text, flags=re.M)
        parse_markdown(text, story)
    doc = StudyDoc(DEST)
    doc.multiBuild(story)
    from pypdf import PdfReader
    reader = PdfReader(str(DEST))
    result = {'pdf': str(DEST), 'pages': len(reader.pages), 'chapters': len(files), 'bytes': DEST.stat().st_size}
    (STUDY / 'pdf_verificacao.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
