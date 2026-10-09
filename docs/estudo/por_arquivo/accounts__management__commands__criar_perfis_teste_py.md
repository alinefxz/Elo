# accounts/management/commands/criar_perfis_teste.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Comando local de contas ficticias preservando registros existentes.

**Arquivo original:** [accounts/management/commands/criar_perfis_teste.py](<C:/Users/lb119/Elo/accounts/management/commands/criar_perfis_teste.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""Prepara contas ficticias para testar os perfis no ambiente local."""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from accounts.models import ConsentimentoLGPD, Triagem, Usuario


class Command(BaseCommand):
    help = "Cria contas ficticias de cada perfil, sem substituir contas existentes."

    def add_arguments(self, parser):
        parser.add_argument('--senha', default='EloTeste2026!', help='Senha das novas contas de teste.')

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError('Este comando exige DEBUG=True no ambiente de desenvolvimento.')
        if len(options['senha']) < 8:
            raise CommandError('Use uma senha com pelo menos oito caracteres.')

        perfis = [
            ('doador', Usuario.Perfil.DOADOR, {}),
            ('doador-inapto', Usuario.Perfil.DOADOR, {}),
            ('doador-sem-consentimento', Usuario.Perfil.DOADOR, {}),
            ('receptor', Usuario.Perfil.RECEPTOR, {}),
            ('observador', Usuario.Perfil.OBSERVADOR, {}),
            ('administrador', Usuario.Perfil.ADMINISTRADOR, {'is_staff': True, 'is_superuser': True}),
        ]
        for status in Usuario.StatusValidacaoHemocentro.values:
            perfis.append((f'hemocentro-{status.lower()}', Usuario.Perfil.HEMOCENTRO,
                           {'status_validacao': status}))

        for nome, perfil, extras in perfis:
            email = f'{nome}@teste.elo.test'
            if Usuario.objects.filter(email=email).exists():
                self.stdout.write(f'Mantida sem alteracoes: {email}')
                continue
            usuario = Usuario.objects.create_user(
                email=email, password=options['senha'], nome=f'TESTE {nome}', perfil=perfil,
                cidade='Belo Horizonte', estado='MG',
                tipo_sanguineo='O-' if perfil == Usuario.Perfil.DOADOR else '',
                aceita_notificacoes_pedidos=perfil == Usuario.Perfil.DOADOR,
                **extras,
            )
            ConsentimentoLGPD.objects.create(
                usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL, aceito=True,
            )
            if perfil == Usuario.Perfil.DOADOR:
                Triagem.objects.create(
                    usuario=usuario, status=Triagem.Status.CONCLUIDA,
                    resultado=(Triagem.Resultado.INAPTO_TEMPORARIO if nome == 'doador-inapto'
                               else Triagem.Resultado.APTO),
                    finalizada_em=timezone.now(),
                )
                if nome != 'doador-sem-consentimento':
                    ConsentimentoLGPD.objects.create(
                        usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
                        versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO, aceito=True,
                    )
            self.stdout.write(self.style.SUCCESS(f'Criada: {email}'))
        self.stdout.write('Contas existentes e suas senhas foram preservadas. Veja TESTAR_PERFIS.md.')
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 1

```python
"""Prepara contas ficticias para testar os perfis no ambiente local."""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 3 a 3

```python
from django.conf import settings
```

**Explicação deste trecho:**

**Linha 3 — ImportFrom** (nível 0 do bloco).

Importa de `django.conf` os nomes `settings`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 4 a 4

```python
from django.core.management.base import BaseCommand, CommandError
```

**Explicação deste trecho:**

**Linha 4 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.management.base` os nomes `BaseCommand`, `CommandError`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 5 a 5

```python
from django.db import transaction
```

**Explicação deste trecho:**

**Linha 5 — ImportFrom** (nível 0 do bloco).

Importa de `django.db` os nomes `transaction`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 6 a 6

```python
from django.utils import timezone
```

**Explicação deste trecho:**

**Linha 6 — ImportFrom** (nível 0 do bloco).

Importa de `django.utils` os nomes `timezone`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 8 a 8

```python
from accounts.models import ConsentimentoLGPD, Triagem, Usuario
```

**Explicação deste trecho:**

**Linha 8 — ImportFrom** (nível 0 do bloco).

Importa de `accounts.models` os nomes `ConsentimentoLGPD`, `Triagem`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

### Command — linhas 11 a 64

```python
class Command(BaseCommand):
    help = "Cria contas ficticias de cada perfil, sem substituir contas existentes."

    def add_arguments(self, parser):
        parser.add_argument('--senha', default='EloTeste2026!', help='Senha das novas contas de teste.')

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError('Este comando exige DEBUG=True no ambiente de desenvolvimento.')
        if len(options['senha']) < 8:
            raise CommandError('Use uma senha com pelo menos oito caracteres.')

        perfis = [
            ('doador', Usuario.Perfil.DOADOR, {}),
            ('doador-inapto', Usuario.Perfil.DOADOR, {}),
            ('doador-sem-consentimento', Usuario.Perfil.DOADOR, {}),
            ('receptor', Usuario.Perfil.RECEPTOR, {}),
            ('observador', Usuario.Perfil.OBSERVADOR, {}),
            ('administrador', Usuario.Perfil.ADMINISTRADOR, {'is_staff': True, 'is_superuser': True}),
        ]
        for status in Usuario.StatusValidacaoHemocentro.values:
            perfis.append((f'hemocentro-{status.lower()}', Usuario.Perfil.HEMOCENTRO,
                           {'status_validacao': status}))

        for nome, perfil, extras in perfis:
            email = f'{nome}@teste.elo.test'
            if Usuario.objects.filter(email=email).exists():
                self.stdout.write(f'Mantida sem alteracoes: {email}')
                continue
            usuario = Usuario.objects.create_user(
                email=email, password=options['senha'], nome=f'TESTE {nome}', perfil=perfil,
                cidade='Belo Horizonte', estado='MG',
                tipo_sanguineo='O-' if perfil == Usuario.Perfil.DOADOR else '',
                aceita_notificacoes_pedidos=perfil == Usuario.Perfil.DOADOR,
                **extras,
            )
            ConsentimentoLGPD.objects.create(
                usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL, aceito=True,
            )
            if perfil == Usuario.Perfil.DOADOR:
                Triagem.objects.create(
                    usuario=usuario, status=Triagem.Status.CONCLUIDA,
                    resultado=(Triagem.Resultado.INAPTO_TEMPORARIO if nome == 'doador-inapto'
                               else Triagem.Resultado.APTO),
                    finalizada_em=timezone.now(),
                )
                if nome != 'doador-sem-consentimento':
                    ConsentimentoLGPD.objects.create(
                        usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
                        versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO, aceito=True,
                    )
            self.stdout.write(self.style.SUCCESS(f'Criada: {email}'))
        self.stdout.write('Contas existentes e suas senhas foram preservadas. Veja TESTAR_PERFIS.md.')
```

**Explicação deste trecho:**

**Linha 11 — ClassDef** (nível 0 do bloco).

Define a classe `Command` herdando de `BaseCommand`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 11:

**Linha 12 — Assign** (nível 1 do bloco).

Associa `help` a o valor literal `'Cria contas ficticias de cada perfil, sem substituir contas existentes.'`.

**Linha 14 — FunctionDef** (nível 1 do bloco).

Define `add_arguments(self, parser)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 14:

**Linha 15 — Expr** (nível 2 do bloco).

Executa a chamada `parser.add_argument`; argumentos posicionais: `'--senha'`; argumentos nomeados: `default='EloTeste2026!'`, `help='Senha das novas contas de teste.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 18 — FunctionDef** (nível 1 do bloco).

Define `handle(self, *args, **options)`. O corpo só executa quando a função/método é chamado. Decoradores: `transaction.atomic`.

Bloco `body` da linha 18:

**Linha 19 — If** (nível 2 do bloco).

Escolhe um caminho verificando a negação de `settings.DEBUG`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 19:

**Linha 20 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `CommandError`; argumentos posicionais: `'Este comando exige DEBUG=True no ambiente de desenvolvimento.'`.

**Linha 21 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `len(options['senha'])` menor que `8`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 21:

**Linha 22 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `CommandError`; argumentos posicionais: `'Use uma senha com pelo menos oito caracteres.'`.

**Linha 24 — Assign** (nível 2 do bloco).

Associa `perfis` a uma coleção List com 6 itens, na expressão `[('doador', Usuario.Perfil.DOADOR, {}), ('doador-inapto', Usuario.Perfil.DOADOR, {}), ('doador-sem-consentimento', Usuario.Perfil.DOADOR, {}), ('receptor', Usuario.Perfil.RECEPTOR, {}), ('observador', Usuario.Perfil.OBSERVADOR, {}), ('administrador', Usuario.Perfil.ADMINISTRADOR, {'is_staff': True, 'is_superuser': True})]`.

**Linha 32 — For** (nível 2 do bloco).

Percorre `Usuario.StatusValidacaoHemocentro.values`; cada item é atribuído a `status` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 32:

**Linha 33 — Expr** (nível 3 do bloco).

Executa a chamada `perfis.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `(f'hemocentro-{status.lower()}', Usuario.Perfil.HEMOCENTRO, {'status_validacao': status})`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 36 — For** (nível 2 do bloco).

Percorre `perfis`; cada item é atribuído a `(nome, perfil, extras)` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 36:

**Linha 37 — Assign** (nível 3 do bloco).

Associa `email` a o texto formatado `f'{nome}@teste.elo.test'`, inserindo valores nas partes entre chaves.

**Linha 38 — If** (nível 3 do bloco).

Escolhe um caminho verificando a chamada `Usuario.objects.filter(email=email).exists`, que verifica se há pelo menos um resultado. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 38:

**Linha 39 — Expr** (nível 4 do bloco).

Executa a chamada `self.stdout.write`; argumentos posicionais: `f'Mantida sem alteracoes: {email}'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 40 — Continue** (nível 4 do bloco).

Pula o restante da iteração atual e segue para o próximo item do laço.

**Linha 41 — Assign** (nível 3 do bloco).

Associa `usuario` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email=email`, `password=options['senha']`, `nome=f'TESTE {nome}'`, `perfil=perfil`, `cidade='Belo Horizonte'`, `estado='MG'`, `tipo_sanguineo='O-' if perfil == Usuario.Perfil.DOADOR else ''`, `aceita_notificacoes_pedidos=perfil == Usuario.Perfil.DOADOR`, `**=extras`.

- `email=email`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `password=options['senha']`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome=f'TESTE {nome}'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=perfil`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `cidade='Belo Horizonte'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `estado='MG'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_sanguineo='O-' if perfil == Usuario.Perfil.DOADOR else ''`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `aceita_notificacoes_pedidos=perfil == Usuario.Perfil.DOADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `**=extras`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 48 — Expr** (nível 3 do bloco).

Executa a chamada `ConsentimentoLGPD.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=usuario`, `tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL`, `aceito=True`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 51 — If** (nível 3 do bloco).

Escolhe um caminho verificando a comparação `perfil` igual a `Usuario.Perfil.DOADOR`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 51:

**Linha 52 — Expr** (nível 4 do bloco).

Executa a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=usuario`, `status=Triagem.Status.CONCLUIDA`, `resultado=Triagem.Resultado.INAPTO_TEMPORARIO if nome == 'doador-inapto' else Triagem.Resultado.APTO`, `finalizada_em=timezone.now()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 58 — If** (nível 4 do bloco).

Escolhe um caminho verificando a comparação `nome` diferente de `'doador-sem-consentimento'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 58:

**Linha 59 — Expr** (nível 5 do bloco).

Executa a chamada `ConsentimentoLGPD.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=usuario`, `tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES`, `versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO`, `aceito=True`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 63 — Expr** (nível 3 do bloco).

Executa a chamada `self.stdout.write`; argumentos posicionais: `self.style.SUCCESS(f'Criada: {email}')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 64 — Expr** (nível 2 do bloco).

Executa a chamada `self.stdout.write`; argumentos posicionais: `'Contas existentes e suas senhas foram preservadas. Veja TESTAR_PERFIS.md.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

