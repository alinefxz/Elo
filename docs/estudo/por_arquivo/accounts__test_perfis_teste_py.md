# accounts/test_perfis_teste.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

**Arquivo original:** [accounts/test_perfis_teste.py](<C:/Users/lb119/Elo/accounts/test_perfis_teste.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from .compatibilidade import doadores_aptos_para_convocacao
from .models import ConsentimentoLGPD, Triagem, Usuario


@override_settings(DEBUG=True)
class PerfisTesteTests(TestCase):
    def test_cria_perfis_e_preserva_alteracoes_ao_repetir(self):
        call_command('criar_perfis_teste', stdout=StringIO())
        self.assertEqual(Usuario.objects.count(), 10)
        self.assertEqual(set(Usuario.objects.values_list('perfil', flat=True)), set(Usuario.Perfil.values))
        self.assertEqual(list(doadores_aptos_para_convocacao('O-').values_list('email', flat=True)),
                         ['doador@teste.elo.test'])
        usuario = Usuario.objects.get(email='receptor@teste.elo.test')
        self.assertTrue(usuario.check_password('EloTeste2026!'))
        usuario.nome = 'Nome alterado no teste'
        usuario.set_password('OutraSenha123!')
        usuario.save()
        contagens = (Triagem.objects.count(), ConsentimentoLGPD.objects.count())
        call_command('criar_perfis_teste', senha='NovaSenha123!', stdout=StringIO())
        usuario.refresh_from_db()
        self.assertEqual(usuario.nome, 'Nome alterado no teste')
        self.assertTrue(usuario.check_password('OutraSenha123!'))
        self.assertEqual(Usuario.objects.count(), 10)
        self.assertEqual(contagens, (Triagem.objects.count(), ConsentimentoLGPD.objects.count()))

    @override_settings(DEBUG=False)
    def test_nao_cria_contas_fora_do_ambiente_de_desenvolvimento(self):
        with self.assertRaises(CommandError):
            call_command('criar_perfis_teste', stdout=StringIO())
        self.assertFalse(Usuario.objects.exists())
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### ImportFrom — linhas 1 a 1

```python
from io import StringIO
```

**Explicação deste trecho:**

**Linha 1 — ImportFrom** (nível 0 do bloco).

Importa de `io` os nomes `StringIO`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 3 a 3

```python
from django.core.management import call_command
```

**Explicação deste trecho:**

**Linha 3 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.management` os nomes `call_command`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 4 a 4

```python
from django.core.management.base import CommandError
```

**Explicação deste trecho:**

**Linha 4 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.management.base` os nomes `CommandError`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 5 a 5

```python
from django.test import TestCase, override_settings
```

**Explicação deste trecho:**

**Linha 5 — ImportFrom** (nível 0 do bloco).

Importa de `django.test` os nomes `TestCase`, `override_settings`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 7 a 7

```python
from .compatibilidade import doadores_aptos_para_convocacao
```

**Explicação deste trecho:**

**Linha 7 — ImportFrom** (nível 0 do bloco).

Importa de `.compatibilidade` os nomes `doadores_aptos_para_convocacao`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 8 a 8

```python
from .models import ConsentimentoLGPD, Triagem, Usuario
```

**Explicação deste trecho:**

**Linha 8 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `ConsentimentoLGPD`, `Triagem`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

### PerfisTesteTests — linhas 11 a 36

```python
@override_settings(DEBUG=True)
class PerfisTesteTests(TestCase):
    def test_cria_perfis_e_preserva_alteracoes_ao_repetir(self):
        call_command('criar_perfis_teste', stdout=StringIO())
        self.assertEqual(Usuario.objects.count(), 10)
        self.assertEqual(set(Usuario.objects.values_list('perfil', flat=True)), set(Usuario.Perfil.values))
        self.assertEqual(list(doadores_aptos_para_convocacao('O-').values_list('email', flat=True)),
                         ['doador@teste.elo.test'])
        usuario = Usuario.objects.get(email='receptor@teste.elo.test')
        self.assertTrue(usuario.check_password('EloTeste2026!'))
        usuario.nome = 'Nome alterado no teste'
        usuario.set_password('OutraSenha123!')
        usuario.save()
        contagens = (Triagem.objects.count(), ConsentimentoLGPD.objects.count())
        call_command('criar_perfis_teste', senha='NovaSenha123!', stdout=StringIO())
        usuario.refresh_from_db()
        self.assertEqual(usuario.nome, 'Nome alterado no teste')
        self.assertTrue(usuario.check_password('OutraSenha123!'))
        self.assertEqual(Usuario.objects.count(), 10)
        self.assertEqual(contagens, (Triagem.objects.count(), ConsentimentoLGPD.objects.count()))

    @override_settings(DEBUG=False)
    def test_nao_cria_contas_fora_do_ambiente_de_desenvolvimento(self):
        with self.assertRaises(CommandError):
            call_command('criar_perfis_teste', stdout=StringIO())
        self.assertFalse(Usuario.objects.exists())
```

**Explicação deste trecho:**

**Linha 12 — ClassDef** (nível 0 do bloco).

Define a classe `PerfisTesteTests` herdando de `TestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 12:

**Linha 13 — FunctionDef** (nível 1 do bloco).

Define `test_cria_perfis_e_preserva_alteracoes_ao_repetir(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: cria perfis e preserva alteracoes ao repetir.

Bloco `body` da linha 13:

**Linha 14 — Expr** (nível 2 do bloco).

Executa a chamada `call_command`, que executa um comando de gerenciamento do Django; argumentos posicionais: `'criar_perfis_teste'`; argumentos nomeados: `stdout=StringIO()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 15 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `Usuario.objects.count()`, `10`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 16 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `set(Usuario.objects.values_list('perfil', flat=True))`, `set(Usuario.Perfil.values)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 17 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `list(doadores_aptos_para_convocacao('O-').values_list('email', flat=True))`, `['doador@teste.elo.test']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 19 — Assign** (nível 2 do bloco).

Associa `usuario` a a chamada `Usuario.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `email='receptor@teste.elo.test'`.

- `email='receptor@teste.elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 20 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `usuario.check_password('EloTeste2026!')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 21 — Assign** (nível 2 do bloco).

Associa `usuario.nome` a o valor literal `'Nome alterado no teste'`.

**Linha 22 — Expr** (nível 2 do bloco).

Executa a chamada `usuario.set_password`, que transforma a senha em hash para armazenamento; argumentos posicionais: `'OutraSenha123!'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 23 — Expr** (nível 2 do bloco).

Executa a chamada `usuario.save`, que persiste a instância; update_fields limita os campos gravados. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 24 — Assign** (nível 2 do bloco).

Associa `contagens` a uma coleção Tuple com 2 itens, na expressão `(Triagem.objects.count(), ConsentimentoLGPD.objects.count())`.

**Linha 25 — Expr** (nível 2 do bloco).

Executa a chamada `call_command`, que executa um comando de gerenciamento do Django; argumentos posicionais: `'criar_perfis_teste'`; argumentos nomeados: `senha='NovaSenha123!'`, `stdout=StringIO()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 26 — Expr** (nível 2 do bloco).

Executa a chamada `usuario.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 27 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `usuario.nome`, `'Nome alterado no teste'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 28 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `usuario.check_password('OutraSenha123!')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 29 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `Usuario.objects.count()`, `10`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 30 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `contagens`, `(Triagem.objects.count(), ConsentimentoLGPD.objects.count())`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 33 — FunctionDef** (nível 1 do bloco).

Define `test_nao_cria_contas_fora_do_ambiente_de_desenvolvimento(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: nao cria contas fora do ambiente de desenvolvimento. Decoradores: `override_settings(DEBUG=False)`.

Bloco `body` da linha 33:

**Linha 34 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(CommandError)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 34:

**Linha 35 — Expr** (nível 3 do bloco).

Executa a chamada `call_command`, que executa um comando de gerenciamento do Django; argumentos posicionais: `'criar_perfis_teste'`; argumentos nomeados: `stdout=StringIO()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 36 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `Usuario.objects.exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

