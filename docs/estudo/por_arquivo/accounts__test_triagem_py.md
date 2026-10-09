# accounts/test_triagem.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

**Arquivo original:** [accounts/test_triagem.py](<C:/Users/lb119/Elo/accounts/test_triagem.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""
Testes automatizados da triagem extensa inicial.

Verificam o cálculo dos resultados para respostas básicas, a
classificação temporária para peso abaixo de 50 kg, o início da
triagem com registro do consentimento, o bloqueio de perfis não
autorizados (Observador e Receptor) e o acesso público à página
de apresentação da triagem.
"""

from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import (
    ConsentimentoLGPD,
    RespostaTriagem,
    Triagem,
    Usuario,
)
from .triagem import calcular_resultado


class TriagemExtensaTests(TestCase):
    """
    Testa o cálculo e o salvamento da triagem inicial.
    """

    def criar_doador(self):
        """
        Cria um usuário Doador para os testes.
        """

        return Usuario.objects.create_user(
            email="doador@teste.com",
            password="SenhaForte123!",
            nome="Doador Teste",
            perfil=Usuario.Perfil.DOADOR,
        )

    def dados_sem_impedimento(self):
        """
        Retorna respostas básicas sem impedimento inicial.
        """

        return {
            "entende_orientacao": "SIM",
            "idade": "18_60",
            "peso": "56_129_9",
            "sexo_biologico": "MASCULINO",
            "ja_doou": "NAO",
        }

    def test_peso_abaixo_de_50_gera_inaptidao_temporaria(self):
        """
        Peso abaixo de 50 kg deve gerar resultado temporário.
        """

        respostas = self.dados_sem_impedimento()
        respostas["peso"] = "MENOS_50"

        resultado = calcular_resultado(
            respostas,
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            resultado["resultado"],
            Triagem.Resultado.TEMPORARIA,
        )

    def test_respostas_basicas_sem_impedimento(self):
        """
        Respostas básicas devem gerar orientação sem impedimento identificado.
        """

        resultado = calcular_resultado(
            self.dados_sem_impedimento(),
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            resultado["resultado"],
            Triagem.Resultado.SEM_IMPEDIMENTO,
        )

    def test_post_inicia_triagem_e_consentimento(self):
        """
        O clique inicial cria a triagem e o consentimento versionado.
        """

        usuario = self.criar_doador()
        self.client.force_login(usuario)

        resposta = self.client.post(
            reverse(
                "accounts:triagem_iniciar",
                kwargs={"modalidade": "extensa"},
            ),
            {"aceite_termo": "on"},
        )

        self.assertEqual(
            resposta.status_code,
            302,
        )

        triagem = Triagem.objects.get(
            usuario=usuario,
        )

        self.assertRedirects(
            resposta,
            reverse(
                "accounts:triagem_pergunta",
                kwargs={"id_triagem": triagem.pk},
            ),
        )

        self.assertEqual(
            RespostaTriagem.objects.filter(
                triagem=triagem,
            ).count(),
            0,
        )

        self.assertTrue(
            ConsentimentoLGPD.objects.filter(
                usuario=usuario,
                tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM,
            ).exists()
        )

    def test_usuario_nao_doador_nao_acessa_triagem(self):
        """
        A primeira versão da triagem só aceita usuários Doador.
        """

        usuario = Usuario.objects.create_user(
            email="observador@teste.com",
            password="SenhaForte123!",
            nome="Observador Teste",
            perfil=Usuario.Perfil.OBSERVADOR,
        )

        self.client.force_login(usuario)

        resposta = self.client.post(
            reverse(
                "accounts:triagem_iniciar",
                kwargs={"modalidade": "extensa"},
            ),
            {"aceite_termo": "on"},
        )

        self.assertEqual(resposta.status_code, 403)

    def test_receptor_nao_pode_acessar_a_triagem(self):
        """
        Receptor nao pode responder a triagem para doacao.
        """

        usuario = Usuario.objects.create_user(
            email="receptor@teste.com",
            password="SenhaForte123!",
            nome="Receptor Teste",
            perfil=Usuario.Perfil.RECEPTOR,
        )

        self.client.force_login(usuario)

        resposta = self.client.post(
            reverse(
                "accounts:triagem_iniciar",
                kwargs={"modalidade": "extensa"},
            ),
            {"aceite_termo": "on"},
        )

        self.assertEqual(
            resposta.status_code,
            403,
        )

    def test_visitante_pode_ver_apresentacao_da_triagem(self):
        """
        Visitante pode conhecer a triagem sem estar autenticado.
        """

        resposta = self.client.get(
            reverse("accounts:triagem_apresentacao"),
        )

        self.assertEqual(
            resposta.status_code,
            200,
        )

        self.assertContains(
            resposta,
            "Seu gesto de cuidado começa aqui.",
        )

        self.assertContains(
            resposta,
            "Criar conta",
        )
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 9

```python
"""
Testes automatizados da triagem extensa inicial.

Verificam o cálculo dos resultados para respostas básicas, a
classificação temporária para peso abaixo de 50 kg, o início da
triagem com registro do consentimento, o bloqueio de perfis não
autorizados (Observador e Receptor) e o acesso público à página
de apresentação da triagem.
"""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 11 a 11

```python
from datetime import date
```

**Explicação deste trecho:**

**Linha 11 — ImportFrom** (nível 0 do bloco).

Importa de `datetime` os nomes `date`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 13 a 13

```python
from django.test import TestCase
```

**Explicação deste trecho:**

**Linha 13 — ImportFrom** (nível 0 do bloco).

Importa de `django.test` os nomes `TestCase`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 14 a 14

```python
from django.urls import reverse
```

**Explicação deste trecho:**

**Linha 14 — ImportFrom** (nível 0 do bloco).

Importa de `django.urls` os nomes `reverse`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 16 a 21

```python
from .models import (
    ConsentimentoLGPD,
    RespostaTriagem,
    Triagem,
    Usuario,
)
```

**Explicação deste trecho:**

**Linha 16 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `ConsentimentoLGPD`, `RespostaTriagem`, `Triagem`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 22 a 22

```python
from .triagem import calcular_resultado
```

**Explicação deste trecho:**

**Linha 22 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem` os nomes `calcular_resultado`. Pontos iniciais indicam importação relativa ao pacote.

### TriagemExtensaTests — linhas 25 a 208

```python
class TriagemExtensaTests(TestCase):
    """
    Testa o cálculo e o salvamento da triagem inicial.
    """

    def criar_doador(self):
        """
        Cria um usuário Doador para os testes.
        """

        return Usuario.objects.create_user(
            email="doador@teste.com",
            password="SenhaForte123!",
            nome="Doador Teste",
            perfil=Usuario.Perfil.DOADOR,
        )

    def dados_sem_impedimento(self):
        """
        Retorna respostas básicas sem impedimento inicial.
        """

        return {
            "entende_orientacao": "SIM",
            "idade": "18_60",
            "peso": "56_129_9",
            "sexo_biologico": "MASCULINO",
            "ja_doou": "NAO",
        }

    def test_peso_abaixo_de_50_gera_inaptidao_temporaria(self):
        """
        Peso abaixo de 50 kg deve gerar resultado temporário.
        """

        respostas = self.dados_sem_impedimento()
        respostas["peso"] = "MENOS_50"

        resultado = calcular_resultado(
            respostas,
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            resultado["resultado"],
            Triagem.Resultado.TEMPORARIA,
        )

    def test_respostas_basicas_sem_impedimento(self):
        """
        Respostas básicas devem gerar orientação sem impedimento identificado.
        """

        resultado = calcular_resultado(
            self.dados_sem_impedimento(),
            hoje=date(2026, 8, 28),
        )

        self.assertEqual(
            resultado["resultado"],
            Triagem.Resultado.SEM_IMPEDIMENTO,
        )

    def test_post_inicia_triagem_e_consentimento(self):
        """
        O clique inicial cria a triagem e o consentimento versionado.
        """

        usuario = self.criar_doador()
        self.client.force_login(usuario)

        resposta = self.client.post(
            reverse(
                "accounts:triagem_iniciar",
                kwargs={"modalidade": "extensa"},
            ),
            {"aceite_termo": "on"},
        )

        self.assertEqual(
            resposta.status_code,
            302,
        )

        triagem = Triagem.objects.get(
            usuario=usuario,
        )

        self.assertRedirects(
            resposta,
            reverse(
                "accounts:triagem_pergunta",
                kwargs={"id_triagem": triagem.pk},
            ),
        )

        self.assertEqual(
            RespostaTriagem.objects.filter(
                triagem=triagem,
            ).count(),
            0,
        )

        self.assertTrue(
            ConsentimentoLGPD.objects.filter(
                usuario=usuario,
                tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM,
            ).exists()
        )

    def test_usuario_nao_doador_nao_acessa_triagem(self):
        """
        A primeira versão da triagem só aceita usuários Doador.
        """

        usuario = Usuario.objects.create_user(
            email="observador@teste.com",
            password="SenhaForte123!",
            nome="Observador Teste",
            perfil=Usuario.Perfil.OBSERVADOR,
        )

        self.client.force_login(usuario)

        resposta = self.client.post(
            reverse(
                "accounts:triagem_iniciar",
                kwargs={"modalidade": "extensa"},
            ),
            {"aceite_termo": "on"},
        )

        self.assertEqual(resposta.status_code, 403)

    def test_receptor_nao_pode_acessar_a_triagem(self):
        """
        Receptor nao pode responder a triagem para doacao.
        """

        usuario = Usuario.objects.create_user(
            email="receptor@teste.com",
            password="SenhaForte123!",
            nome="Receptor Teste",
            perfil=Usuario.Perfil.RECEPTOR,
        )

        self.client.force_login(usuario)

        resposta = self.client.post(
            reverse(
                "accounts:triagem_iniciar",
                kwargs={"modalidade": "extensa"},
            ),
            {"aceite_termo": "on"},
        )

        self.assertEqual(
            resposta.status_code,
            403,
        )

    def test_visitante_pode_ver_apresentacao_da_triagem(self):
        """
        Visitante pode conhecer a triagem sem estar autenticado.
        """

        resposta = self.client.get(
            reverse("accounts:triagem_apresentacao"),
        )

        self.assertEqual(
            resposta.status_code,
            200,
        )

        self.assertContains(
            resposta,
            "Seu gesto de cuidado começa aqui.",
        )

        self.assertContains(
            resposta,
            "Criar conta",
        )
```

**Explicação deste trecho:**

**Linha 25 — ClassDef** (nível 0 do bloco).

Define a classe `TriagemExtensaTests` herdando de `TestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 25:

**Linha 26 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 30 — FunctionDef** (nível 1 do bloco).

Define `criar_doador(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 30:

**Linha 31 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 35 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `Usuario.objects.create_user`; argumentos nomeados: `email='doador@teste.com'`, `password='SenhaForte123!'`, `nome='Doador Teste'`, `perfil=Usuario.Perfil.DOADOR` ao chamador.

**Linha 42 — FunctionDef** (nível 1 do bloco).

Define `dados_sem_impedimento(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 42:

**Linha 43 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 47 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve um dicionário de 5 entradas; as chaves dão nome aos valores associados ao chamador.

**Linha 55 — FunctionDef** (nível 1 do bloco).

Define `test_peso_abaixo_de_50_gera_inaptidao_temporaria(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: peso abaixo de 50 gera inaptidao temporaria.

Bloco `body` da linha 55:

**Linha 56 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 60 — Assign** (nível 2 do bloco).

Associa `respostas` a a chamada `self.dados_sem_impedimento`.


**Linha 61 — Assign** (nível 2 do bloco).

Associa `respostas['peso']` a o valor literal `'MENOS_50'`.

**Linha 63 — Assign** (nível 2 do bloco).

Associa `resultado` a a chamada `calcular_resultado`; argumentos posicionais: `respostas`; argumentos nomeados: `hoje=date(2026, 8, 28)`.

- `hoje=date(2026, 8, 28)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 68 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resultado['resultado']`, `Triagem.Resultado.TEMPORARIA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 73 — FunctionDef** (nível 1 do bloco).

Define `test_respostas_basicas_sem_impedimento(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: respostas basicas sem impedimento.

Bloco `body` da linha 73:

**Linha 74 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 78 — Assign** (nível 2 do bloco).

Associa `resultado` a a chamada `calcular_resultado`; argumentos posicionais: `self.dados_sem_impedimento()`; argumentos nomeados: `hoje=date(2026, 8, 28)`.

- `hoje=date(2026, 8, 28)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 83 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resultado['resultado']`, `Triagem.Resultado.SEM_IMPEDIMENTO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 88 — FunctionDef** (nível 1 do bloco).

Define `test_post_inicia_triagem_e_consentimento(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: post inicia triagem e consentimento.

Bloco `body` da linha 88:

**Linha 89 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 93 — Assign** (nível 2 do bloco).

Associa `usuario` a a chamada `self.criar_doador`.


**Linha 94 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `usuario`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 96 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:triagem_iniciar', kwargs={'modalidade': 'extensa'})`, `{'aceite_termo': 'on'}`.


**Linha 104 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `302`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 109 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `Triagem.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `usuario=usuario`.

- `usuario=usuario`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 113 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:triagem_pergunta', kwargs={'id_triagem': triagem.pk})`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 121 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `RespostaTriagem.objects.filter(triagem=triagem).count()`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 128 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `ConsentimentoLGPD.objects.filter(usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM).exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 135 — FunctionDef** (nível 1 do bloco).

Define `test_usuario_nao_doador_nao_acessa_triagem(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: usuario nao doador nao acessa triagem.

Bloco `body` da linha 135:

**Linha 136 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 140 — Assign** (nível 2 do bloco).

Associa `usuario` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email='observador@teste.com'`, `password='SenhaForte123!'`, `nome='Observador Teste'`, `perfil=Usuario.Perfil.OBSERVADOR`.

- `email='observador@teste.com'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `password='SenhaForte123!'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Observador Teste'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.OBSERVADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 147 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `usuario`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 149 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:triagem_iniciar', kwargs={'modalidade': 'extensa'})`, `{'aceite_termo': 'on'}`.


**Linha 157 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `403`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 159 — FunctionDef** (nível 1 do bloco).

Define `test_receptor_nao_pode_acessar_a_triagem(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: receptor nao pode acessar a triagem.

Bloco `body` da linha 159:

**Linha 160 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 164 — Assign** (nível 2 do bloco).

Associa `usuario` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email='receptor@teste.com'`, `password='SenhaForte123!'`, `nome='Receptor Teste'`, `perfil=Usuario.Perfil.RECEPTOR`.

- `email='receptor@teste.com'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `password='SenhaForte123!'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Receptor Teste'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.RECEPTOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 171 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `usuario`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 173 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:triagem_iniciar', kwargs={'modalidade': 'extensa'})`, `{'aceite_termo': 'on'}`.


**Linha 181 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `403`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 186 — FunctionDef** (nível 1 do bloco).

Define `test_visitante_pode_ver_apresentacao_da_triagem(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: visitante pode ver apresentacao da triagem.

Bloco `body` da linha 186:

**Linha 187 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 191 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:triagem_apresentacao')`.


**Linha 195 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `200`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 200 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Seu gesto de cuidado começa aqui.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 205 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Criar conta'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

