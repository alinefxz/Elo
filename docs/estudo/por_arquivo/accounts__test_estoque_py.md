# accounts/test_estoque.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

**Arquivo original:** [accounts/test_estoque.py](<C:/Users/lb119/Elo/accounts/test_estoque.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""
Testes automatizados do estoque (UC_29 - Cadastrar Estoque e
UC_30 - Atualizar Estoque).

Cobrem:
- calculo do status (critico/baixo/estavel);
- cadastro de estoque, incluindo bloqueios (nao aprovado, duplicado,
  niveis incoerentes);
- movimentacoes de entrada, saida e ajuste, incluindo bloqueios (saida
  maior que o disponivel, estoque de outro hemocentro);
- geracao de historico (EstoqueMovimentacao) e auditoria
  (AuditoriaAcaoCritica) a cada operacao;
- as views, por meio do client de testes do Django.

Execute com: ``python manage.py test accounts.test_estoque``.
"""

from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase
from django.urls import reverse

from .estoque import (
    calcular_status_calculado,
    cadastrar_estoque,
    registrar_movimentacao_estoque,
)
from .models import AuditoriaAcaoCritica, Estoque, EstoqueMovimentacao, Usuario
from .validacao_hemocentro import aprovar_hemocentro


class EstoqueTestsBase(TestCase):
    """Prepara um administrador e Hemocentros usados pelos testes."""

    def criar_usuario(self, *, email, nome, perfil):
        return Usuario.objects.create_user(
            email=email,
            password="SenhaForte123!",
            nome=nome,
            perfil=perfil,
        )

    def setUp(self):
        self.admin = self.criar_usuario(
            email="admin@elo.test",
            nome="Administrador Elo",
            perfil=Usuario.Perfil.ADMINISTRADOR,
        )

        self.hemocentro = self.criar_usuario(
            email="hemocentro@elo.test",
            nome="Hemocentro Elo",
            perfil=Usuario.Perfil.HEMOCENTRO,
        )
        aprovar_hemocentro(hemocentro=self.hemocentro, admin=self.admin)
        self.hemocentro.refresh_from_db()

        self.hemocentro_pendente = self.criar_usuario(
            email="pendente@elo.test",
            nome="Hemocentro Pendente",
            perfil=Usuario.Perfil.HEMOCENTRO,
        )

        self.doador = self.criar_usuario(
            email="doador@elo.test",
            nome="Doador Elo",
            perfil=Usuario.Perfil.DOADOR,
        )


class CalcularStatusCalculadoTests(TestCase):
    """Testa a regra pura de calculo de status, sem tocar o banco."""

    def test_quantidade_igual_ao_critico_e_critico(self):
        self.assertEqual(
            calcular_status_calculado(
                quantidade_bolsas=5, nivel_minimo=10, nivel_critico=5
            ),
            Estoque.StatusCalculado.CRITICO,
        )

    def test_quantidade_abaixo_do_critico_e_critico(self):
        self.assertEqual(
            calcular_status_calculado(
                quantidade_bolsas=0, nivel_minimo=10, nivel_critico=5
            ),
            Estoque.StatusCalculado.CRITICO,
        )

    def test_quantidade_igual_ao_minimo_e_baixo(self):
        self.assertEqual(
            calcular_status_calculado(
                quantidade_bolsas=10, nivel_minimo=10, nivel_critico=5
            ),
            Estoque.StatusCalculado.BAIXO,
        )

    def test_quantidade_acima_do_minimo_e_estavel(self):
        self.assertEqual(
            calcular_status_calculado(
                quantidade_bolsas=11, nivel_minimo=10, nivel_critico=5
            ),
            Estoque.StatusCalculado.ESTAVEL,
        )


class CadastrarEstoqueTests(EstoqueTestsBase):
    """Testes principais do UC_29."""

    def test_hemocentro_aprovado_cadastra_estoque(self):
        estoque = cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="o-",  # minusculo de proposito: deve normalizar
            quantidade_bolsas=8,
            nivel_minimo=10,
            nivel_critico=5,
        )

        self.assertEqual(estoque.tipo_sanguineo, "O-")
        self.assertEqual(estoque.status_calculado, Estoque.StatusCalculado.BAIXO)

        self.assertTrue(
            AuditoriaAcaoCritica.objects.filter(
                acao=AuditoriaAcaoCritica.Acao.CADASTRO_ESTOQUE,
                usuario=self.hemocentro,
                alvo_id=str(estoque.pk),
            ).exists()
        )

    def test_hemocentro_pendente_nao_pode_cadastrar_estoque(self):
        with self.assertRaises(PermissionDenied):
            cadastrar_estoque(
                hemocentro=self.hemocentro_pendente,
                tipo_sanguineo="O+",
                nivel_minimo=10,
                nivel_critico=5,
            )

    def test_nao_permite_cadastro_duplicado(self):
        cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="A+",
            nivel_minimo=10,
            nivel_critico=5,
        )

        with self.assertRaises(ValidationError):
            cadastrar_estoque(
                hemocentro=self.hemocentro,
                tipo_sanguineo="A+",
                nivel_minimo=20,
                nivel_critico=10,
            )

    def test_nivel_critico_maior_que_minimo_gera_erro(self):
        with self.assertRaises(ValidationError):
            cadastrar_estoque(
                hemocentro=self.hemocentro,
                tipo_sanguineo="B+",
                nivel_minimo=5,
                nivel_critico=10,
            )

    def test_tipo_sanguineo_invalido_gera_erro(self):
        with self.assertRaises(ValueError):
            cadastrar_estoque(
                hemocentro=self.hemocentro,
                tipo_sanguineo="C+",
                nivel_minimo=10,
                nivel_critico=5,
            )


class RegistrarMovimentacaoEstoqueTests(EstoqueTestsBase):
    """Testes principais do UC_30."""

    def setUp(self):
        super().setUp()

        self.estoque = cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="O-",
            quantidade_bolsas=10,
            nivel_minimo=10,
            nivel_critico=5,
        )

    def test_entrada_soma_quantidade_e_recalcula_status(self):
        movimentacao = registrar_movimentacao_estoque(
            estoque=self.estoque,
            usuario_resp=self.hemocentro,
            tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
            quantidade=15,
            motivo="Doação recebida em mutirão.",
        )

        self.estoque.refresh_from_db()

        self.assertEqual(movimentacao.quantidade_anterior, 10)
        self.assertEqual(movimentacao.quantidade_movimentada, 15)
        self.assertEqual(movimentacao.quantidade_nova, 25)
        self.assertEqual(self.estoque.quantidade_bolsas, 25)
        self.assertEqual(self.estoque.status_calculado, Estoque.StatusCalculado.ESTAVEL)

    def test_saida_subtrai_quantidade(self):
        movimentacao = registrar_movimentacao_estoque(
            estoque=self.estoque,
            usuario_resp=self.hemocentro,
            tipo_movimento=EstoqueMovimentacao.TipoMovimento.SAIDA,
            quantidade=6,
            motivo="Transfusão de emergência.",
        )

        self.estoque.refresh_from_db()

        self.assertEqual(movimentacao.quantidade_nova, 4)
        self.assertEqual(self.estoque.quantidade_bolsas, 4)
        self.assertEqual(self.estoque.status_calculado, Estoque.StatusCalculado.CRITICO)

    def test_saida_maior_que_estoque_gera_erro_e_nao_altera_nada(self):
        with self.assertRaises(ValidationError):
            registrar_movimentacao_estoque(
                estoque=self.estoque,
                usuario_resp=self.hemocentro,
                tipo_movimento=EstoqueMovimentacao.TipoMovimento.SAIDA,
                quantidade=999,
                motivo="Saída solicitada acima do estoque disponível.",
            )

        self.estoque.refresh_from_db()
        self.assertEqual(self.estoque.quantidade_bolsas, 10)
        self.assertEqual(
            EstoqueMovimentacao.objects.filter(estoque=self.estoque).count(), 0
        )

    def test_ajuste_define_quantidade_absoluta_e_aceita_delta_negativo(self):
        movimentacao = registrar_movimentacao_estoque(
            estoque=self.estoque,
            usuario_resp=self.hemocentro,
            tipo_movimento=EstoqueMovimentacao.TipoMovimento.AJUSTE,
            quantidade=3,
            motivo="Contagem física apontou divergência.",
        )

        self.estoque.refresh_from_db()

        self.assertEqual(movimentacao.quantidade_anterior, 10)
        self.assertEqual(movimentacao.quantidade_movimentada, -7)
        self.assertEqual(movimentacao.quantidade_nova, 3)
        self.assertEqual(self.estoque.quantidade_bolsas, 3)

    def test_motivo_e_obrigatorio_na_movimentacao(self):
        with self.assertRaises(ValidationError):
            registrar_movimentacao_estoque(
                estoque=self.estoque,
                usuario_resp=self.hemocentro,
                tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
                quantidade=2,
                motivo="   ",
            )

        self.estoque.refresh_from_db()
        self.assertEqual(self.estoque.quantidade_bolsas, 10)
        self.assertEqual(
            EstoqueMovimentacao.objects.filter(estoque=self.estoque).count(),
            0,
        )

    def test_movimentacao_gera_historico_e_auditoria(self):
        registrar_movimentacao_estoque(
            estoque=self.estoque,
            usuario_resp=self.hemocentro,
            tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
            quantidade=2,
            motivo="Reposição do estoque.",
        )

        self.assertEqual(
            EstoqueMovimentacao.objects.filter(estoque=self.estoque).count(), 1
        )
        self.assertTrue(
            AuditoriaAcaoCritica.objects.filter(
                acao=AuditoriaAcaoCritica.Acao.ATUALIZACAO_ESTOQUE,
                usuario=self.hemocentro,
                alvo_id=str(self.estoque.pk),
            ).exists()
        )

    def test_outro_hemocentro_nao_pode_movimentar_estoque_alheio(self):
        outro_hemocentro = self.criar_usuario(
            email="outro@elo.test",
            nome="Outro Hemocentro",
            perfil=Usuario.Perfil.HEMOCENTRO,
        )
        aprovar_hemocentro(hemocentro=outro_hemocentro, admin=self.admin)
        outro_hemocentro.refresh_from_db()

        with self.assertRaises(PermissionDenied):
            registrar_movimentacao_estoque(
                estoque=self.estoque,
                usuario_resp=outro_hemocentro,
                tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
                quantidade=1,
            )

    def test_doador_nao_pode_movimentar_estoque(self):
        with self.assertRaises(PermissionDenied):
            registrar_movimentacao_estoque(
                estoque=self.estoque,
                usuario_resp=self.doador,
                tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
                quantidade=1,
            )


class EstoqueViewsTests(EstoqueTestsBase):
    """Testes de ponta a ponta usando o client de testes do Django."""

    def test_painel_bloqueia_hemocentro_pendente(self):
        self.client.force_login(self.hemocentro_pendente)

        resposta = self.client.get(reverse("accounts:estoque_hemocentro"))

        self.assertEqual(resposta.status_code, 403)

    def test_post_cadastra_estoque_via_view(self):
        self.client.force_login(self.hemocentro)

        resposta = self.client.post(
            reverse("accounts:cadastrar_estoque"),
            {
                "tipo_sanguineo": "AB+",
                "quantidade_bolsas": 4,
                "nivel_minimo": 10,
                "nivel_critico": 5,
            },
        )

        self.assertRedirects(resposta, reverse("accounts:estoque_hemocentro"))
        self.assertTrue(
            Estoque.objects.filter(
                hemocentro=self.hemocentro, tipo_sanguineo="AB+"
            ).exists()
        )

    def test_post_movimenta_estoque_via_view(self):
        estoque = cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="B-",
            quantidade_bolsas=5,
            nivel_minimo=10,
            nivel_critico=5,
        )

        self.client.force_login(self.hemocentro)

        resposta = self.client.post(
            reverse("accounts:atualizar_estoque", kwargs={"id_estoque": estoque.pk}),
            {
                "tipo_movimento": EstoqueMovimentacao.TipoMovimento.ENTRADA,
                "quantidade": 5,
                "motivo": "Reposição semanal.",
            },
        )

        self.assertRedirects(resposta, reverse("accounts:estoque_hemocentro"))

        estoque.refresh_from_db()
        self.assertEqual(estoque.quantidade_bolsas, 10)

        painel = self.client.get(reverse("accounts:estoque_hemocentro"))
        self.assertContains(painel, "Reposição semanal.")
        self.assertContains(painel, "Hemocentro Elo")
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 16

```python
"""
Testes automatizados do estoque (UC_29 - Cadastrar Estoque e
UC_30 - Atualizar Estoque).

Cobrem:
- calculo do status (critico/baixo/estavel);
- cadastro de estoque, incluindo bloqueios (nao aprovado, duplicado,
  niveis incoerentes);
- movimentacoes de entrada, saida e ajuste, incluindo bloqueios (saida
  maior que o disponivel, estoque de outro hemocentro);
- geracao de historico (EstoqueMovimentacao) e auditoria
  (AuditoriaAcaoCritica) a cada operacao;
- as views, por meio do client de testes do Django.

Execute com: ``python manage.py test accounts.test_estoque``.
"""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 18 a 18

```python
from django.core.exceptions import PermissionDenied, ValidationError
```

**Explicação deste trecho:**

**Linha 18 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.exceptions` os nomes `PermissionDenied`, `ValidationError`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 19 a 19

```python
from django.test import TestCase
```

**Explicação deste trecho:**

**Linha 19 — ImportFrom** (nível 0 do bloco).

Importa de `django.test` os nomes `TestCase`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 20 a 20

```python
from django.urls import reverse
```

**Explicação deste trecho:**

**Linha 20 — ImportFrom** (nível 0 do bloco).

Importa de `django.urls` os nomes `reverse`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 22 a 26

```python
from .estoque import (
    calcular_status_calculado,
    cadastrar_estoque,
    registrar_movimentacao_estoque,
)
```

**Explicação deste trecho:**

**Linha 22 — ImportFrom** (nível 0 do bloco).

Importa de `.estoque` os nomes `calcular_status_calculado`, `cadastrar_estoque`, `registrar_movimentacao_estoque`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 27 a 27

```python
from .models import AuditoriaAcaoCritica, Estoque, EstoqueMovimentacao, Usuario
```

**Explicação deste trecho:**

**Linha 27 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `AuditoriaAcaoCritica`, `Estoque`, `EstoqueMovimentacao`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 28 a 28

```python
from .validacao_hemocentro import aprovar_hemocentro
```

**Explicação deste trecho:**

**Linha 28 — ImportFrom** (nível 0 do bloco).

Importa de `.validacao_hemocentro` os nomes `aprovar_hemocentro`. Pontos iniciais indicam importação relativa ao pacote.

### EstoqueTestsBase — linhas 31 a 67

```python
class EstoqueTestsBase(TestCase):
    """Prepara um administrador e Hemocentros usados pelos testes."""

    def criar_usuario(self, *, email, nome, perfil):
        return Usuario.objects.create_user(
            email=email,
            password="SenhaForte123!",
            nome=nome,
            perfil=perfil,
        )

    def setUp(self):
        self.admin = self.criar_usuario(
            email="admin@elo.test",
            nome="Administrador Elo",
            perfil=Usuario.Perfil.ADMINISTRADOR,
        )

        self.hemocentro = self.criar_usuario(
            email="hemocentro@elo.test",
            nome="Hemocentro Elo",
            perfil=Usuario.Perfil.HEMOCENTRO,
        )
        aprovar_hemocentro(hemocentro=self.hemocentro, admin=self.admin)
        self.hemocentro.refresh_from_db()

        self.hemocentro_pendente = self.criar_usuario(
            email="pendente@elo.test",
            nome="Hemocentro Pendente",
            perfil=Usuario.Perfil.HEMOCENTRO,
        )

        self.doador = self.criar_usuario(
            email="doador@elo.test",
            nome="Doador Elo",
            perfil=Usuario.Perfil.DOADOR,
        )
```

**Explicação deste trecho:**

**Linha 31 — ClassDef** (nível 0 do bloco).

Define a classe `EstoqueTestsBase` herdando de `TestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 31:

**Linha 32 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 34 — FunctionDef** (nível 1 do bloco).

Define `criar_usuario(self, *, email, nome, perfil)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 34:

**Linha 35 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `Usuario.objects.create_user`; argumentos nomeados: `email=email`, `password='SenhaForte123!'`, `nome=nome`, `perfil=perfil` ao chamador.

**Linha 42 — FunctionDef** (nível 1 do bloco).

Define `setUp(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 42:

**Linha 43 — Assign** (nível 2 do bloco).

Associa `self.admin` a a chamada `self.criar_usuario`; argumentos nomeados: `email='admin@elo.test'`, `nome='Administrador Elo'`, `perfil=Usuario.Perfil.ADMINISTRADOR`.

- `email='admin@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Administrador Elo'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.ADMINISTRADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 49 — Assign** (nível 2 do bloco).

Associa `self.hemocentro` a a chamada `self.criar_usuario`; argumentos nomeados: `email='hemocentro@elo.test'`, `nome='Hemocentro Elo'`, `perfil=Usuario.Perfil.HEMOCENTRO`.

- `email='hemocentro@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Hemocentro Elo'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.HEMOCENTRO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 54 — Expr** (nível 2 do bloco).

Executa a chamada `aprovar_hemocentro`; argumentos nomeados: `hemocentro=self.hemocentro`, `admin=self.admin`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 55 — Expr** (nível 2 do bloco).

Executa a chamada `self.hemocentro.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 57 — Assign** (nível 2 do bloco).

Associa `self.hemocentro_pendente` a a chamada `self.criar_usuario`; argumentos nomeados: `email='pendente@elo.test'`, `nome='Hemocentro Pendente'`, `perfil=Usuario.Perfil.HEMOCENTRO`.

- `email='pendente@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Hemocentro Pendente'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.HEMOCENTRO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 63 — Assign** (nível 2 do bloco).

Associa `self.doador` a a chamada `self.criar_usuario`; argumentos nomeados: `email='doador@elo.test'`, `nome='Doador Elo'`, `perfil=Usuario.Perfil.DOADOR`.

- `email='doador@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Doador Elo'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.DOADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

### CalcularStatusCalculadoTests — linhas 70 a 103

```python
class CalcularStatusCalculadoTests(TestCase):
    """Testa a regra pura de calculo de status, sem tocar o banco."""

    def test_quantidade_igual_ao_critico_e_critico(self):
        self.assertEqual(
            calcular_status_calculado(
                quantidade_bolsas=5, nivel_minimo=10, nivel_critico=5
            ),
            Estoque.StatusCalculado.CRITICO,
        )

    def test_quantidade_abaixo_do_critico_e_critico(self):
        self.assertEqual(
            calcular_status_calculado(
                quantidade_bolsas=0, nivel_minimo=10, nivel_critico=5
            ),
            Estoque.StatusCalculado.CRITICO,
        )

    def test_quantidade_igual_ao_minimo_e_baixo(self):
        self.assertEqual(
            calcular_status_calculado(
                quantidade_bolsas=10, nivel_minimo=10, nivel_critico=5
            ),
            Estoque.StatusCalculado.BAIXO,
        )

    def test_quantidade_acima_do_minimo_e_estavel(self):
        self.assertEqual(
            calcular_status_calculado(
                quantidade_bolsas=11, nivel_minimo=10, nivel_critico=5
            ),
            Estoque.StatusCalculado.ESTAVEL,
        )
```

**Explicação deste trecho:**

**Linha 70 — ClassDef** (nível 0 do bloco).

Define a classe `CalcularStatusCalculadoTests` herdando de `TestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 70:

**Linha 71 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 73 — FunctionDef** (nível 1 do bloco).

Define `test_quantidade_igual_ao_critico_e_critico(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: quantidade igual ao critico e critico.

Bloco `body` da linha 73:

**Linha 74 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calcular_status_calculado(quantidade_bolsas=5, nivel_minimo=10, nivel_critico=5)`, `Estoque.StatusCalculado.CRITICO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 81 — FunctionDef** (nível 1 do bloco).

Define `test_quantidade_abaixo_do_critico_e_critico(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: quantidade abaixo do critico e critico.

Bloco `body` da linha 81:

**Linha 82 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calcular_status_calculado(quantidade_bolsas=0, nivel_minimo=10, nivel_critico=5)`, `Estoque.StatusCalculado.CRITICO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 89 — FunctionDef** (nível 1 do bloco).

Define `test_quantidade_igual_ao_minimo_e_baixo(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: quantidade igual ao minimo e baixo.

Bloco `body` da linha 89:

**Linha 90 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calcular_status_calculado(quantidade_bolsas=10, nivel_minimo=10, nivel_critico=5)`, `Estoque.StatusCalculado.BAIXO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 97 — FunctionDef** (nível 1 do bloco).

Define `test_quantidade_acima_do_minimo_e_estavel(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: quantidade acima do minimo e estavel.

Bloco `body` da linha 97:

**Linha 98 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `calcular_status_calculado(quantidade_bolsas=11, nivel_minimo=10, nivel_critico=5)`, `Estoque.StatusCalculado.ESTAVEL`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

### CadastrarEstoqueTests — linhas 106 a 170

```python
class CadastrarEstoqueTests(EstoqueTestsBase):
    """Testes principais do UC_29."""

    def test_hemocentro_aprovado_cadastra_estoque(self):
        estoque = cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="o-",  # minusculo de proposito: deve normalizar
            quantidade_bolsas=8,
            nivel_minimo=10,
            nivel_critico=5,
        )

        self.assertEqual(estoque.tipo_sanguineo, "O-")
        self.assertEqual(estoque.status_calculado, Estoque.StatusCalculado.BAIXO)

        self.assertTrue(
            AuditoriaAcaoCritica.objects.filter(
                acao=AuditoriaAcaoCritica.Acao.CADASTRO_ESTOQUE,
                usuario=self.hemocentro,
                alvo_id=str(estoque.pk),
            ).exists()
        )

    def test_hemocentro_pendente_nao_pode_cadastrar_estoque(self):
        with self.assertRaises(PermissionDenied):
            cadastrar_estoque(
                hemocentro=self.hemocentro_pendente,
                tipo_sanguineo="O+",
                nivel_minimo=10,
                nivel_critico=5,
            )

    def test_nao_permite_cadastro_duplicado(self):
        cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="A+",
            nivel_minimo=10,
            nivel_critico=5,
        )

        with self.assertRaises(ValidationError):
            cadastrar_estoque(
                hemocentro=self.hemocentro,
                tipo_sanguineo="A+",
                nivel_minimo=20,
                nivel_critico=10,
            )

    def test_nivel_critico_maior_que_minimo_gera_erro(self):
        with self.assertRaises(ValidationError):
            cadastrar_estoque(
                hemocentro=self.hemocentro,
                tipo_sanguineo="B+",
                nivel_minimo=5,
                nivel_critico=10,
            )

    def test_tipo_sanguineo_invalido_gera_erro(self):
        with self.assertRaises(ValueError):
            cadastrar_estoque(
                hemocentro=self.hemocentro,
                tipo_sanguineo="C+",
                nivel_minimo=10,
                nivel_critico=5,
            )
```

**Explicação deste trecho:**

**Linha 106 — ClassDef** (nível 0 do bloco).

Define a classe `CadastrarEstoqueTests` herdando de `EstoqueTestsBase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 106:

**Linha 107 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 109 — FunctionDef** (nível 1 do bloco).

Define `test_hemocentro_aprovado_cadastra_estoque(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: hemocentro aprovado cadastra estoque.

Bloco `body` da linha 109:

**Linha 110 — Assign** (nível 2 do bloco).

Associa `estoque` a a chamada `cadastrar_estoque`; argumentos nomeados: `hemocentro=self.hemocentro`, `tipo_sanguineo='o-'`, `quantidade_bolsas=8`, `nivel_minimo=10`, `nivel_critico=5`.

- `hemocentro=self.hemocentro`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_sanguineo='o-'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `quantidade_bolsas=8`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nivel_minimo=10`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nivel_critico=5`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 118 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `estoque.tipo_sanguineo`, `'O-'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 119 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `estoque.status_calculado`, `Estoque.StatusCalculado.BAIXO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 121 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `AuditoriaAcaoCritica.objects.filter(acao=AuditoriaAcaoCritica.Acao.CADASTRO_ESTOQUE, usuario=self.hemocentro, alvo_id=str(estoque.pk)).exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 129 — FunctionDef** (nível 1 do bloco).

Define `test_hemocentro_pendente_nao_pode_cadastrar_estoque(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: hemocentro pendente nao pode cadastrar estoque.

Bloco `body` da linha 129:

**Linha 130 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(PermissionDenied)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 130:

**Linha 131 — Expr** (nível 3 do bloco).

Executa a chamada `cadastrar_estoque`; argumentos nomeados: `hemocentro=self.hemocentro_pendente`, `tipo_sanguineo='O+'`, `nivel_minimo=10`, `nivel_critico=5`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 138 — FunctionDef** (nível 1 do bloco).

Define `test_nao_permite_cadastro_duplicado(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: nao permite cadastro duplicado.

Bloco `body` da linha 138:

**Linha 139 — Expr** (nível 2 do bloco).

Executa a chamada `cadastrar_estoque`; argumentos nomeados: `hemocentro=self.hemocentro`, `tipo_sanguineo='A+'`, `nivel_minimo=10`, `nivel_critico=5`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 146 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(ValidationError)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 146:

**Linha 147 — Expr** (nível 3 do bloco).

Executa a chamada `cadastrar_estoque`; argumentos nomeados: `hemocentro=self.hemocentro`, `tipo_sanguineo='A+'`, `nivel_minimo=20`, `nivel_critico=10`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 154 — FunctionDef** (nível 1 do bloco).

Define `test_nivel_critico_maior_que_minimo_gera_erro(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: nivel critico maior que minimo gera erro.

Bloco `body` da linha 154:

**Linha 155 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(ValidationError)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 155:

**Linha 156 — Expr** (nível 3 do bloco).

Executa a chamada `cadastrar_estoque`; argumentos nomeados: `hemocentro=self.hemocentro`, `tipo_sanguineo='B+'`, `nivel_minimo=5`, `nivel_critico=10`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 163 — FunctionDef** (nível 1 do bloco).

Define `test_tipo_sanguineo_invalido_gera_erro(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: tipo sanguineo invalido gera erro.

Bloco `body` da linha 163:

**Linha 164 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(ValueError)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 164:

**Linha 165 — Expr** (nível 3 do bloco).

Executa a chamada `cadastrar_estoque`; argumentos nomeados: `hemocentro=self.hemocentro`, `tipo_sanguineo='C+'`, `nivel_minimo=10`, `nivel_critico=5`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

### RegistrarMovimentacaoEstoqueTests — linhas 173 a 312

```python
class RegistrarMovimentacaoEstoqueTests(EstoqueTestsBase):
    """Testes principais do UC_30."""

    def setUp(self):
        super().setUp()

        self.estoque = cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="O-",
            quantidade_bolsas=10,
            nivel_minimo=10,
            nivel_critico=5,
        )

    def test_entrada_soma_quantidade_e_recalcula_status(self):
        movimentacao = registrar_movimentacao_estoque(
            estoque=self.estoque,
            usuario_resp=self.hemocentro,
            tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
            quantidade=15,
            motivo="Doação recebida em mutirão.",
        )

        self.estoque.refresh_from_db()

        self.assertEqual(movimentacao.quantidade_anterior, 10)
        self.assertEqual(movimentacao.quantidade_movimentada, 15)
        self.assertEqual(movimentacao.quantidade_nova, 25)
        self.assertEqual(self.estoque.quantidade_bolsas, 25)
        self.assertEqual(self.estoque.status_calculado, Estoque.StatusCalculado.ESTAVEL)

    def test_saida_subtrai_quantidade(self):
        movimentacao = registrar_movimentacao_estoque(
            estoque=self.estoque,
            usuario_resp=self.hemocentro,
            tipo_movimento=EstoqueMovimentacao.TipoMovimento.SAIDA,
            quantidade=6,
            motivo="Transfusão de emergência.",
        )

        self.estoque.refresh_from_db()

        self.assertEqual(movimentacao.quantidade_nova, 4)
        self.assertEqual(self.estoque.quantidade_bolsas, 4)
        self.assertEqual(self.estoque.status_calculado, Estoque.StatusCalculado.CRITICO)

    def test_saida_maior_que_estoque_gera_erro_e_nao_altera_nada(self):
        with self.assertRaises(ValidationError):
            registrar_movimentacao_estoque(
                estoque=self.estoque,
                usuario_resp=self.hemocentro,
                tipo_movimento=EstoqueMovimentacao.TipoMovimento.SAIDA,
                quantidade=999,
                motivo="Saída solicitada acima do estoque disponível.",
            )

        self.estoque.refresh_from_db()
        self.assertEqual(self.estoque.quantidade_bolsas, 10)
        self.assertEqual(
            EstoqueMovimentacao.objects.filter(estoque=self.estoque).count(), 0
        )

    def test_ajuste_define_quantidade_absoluta_e_aceita_delta_negativo(self):
        movimentacao = registrar_movimentacao_estoque(
            estoque=self.estoque,
            usuario_resp=self.hemocentro,
            tipo_movimento=EstoqueMovimentacao.TipoMovimento.AJUSTE,
            quantidade=3,
            motivo="Contagem física apontou divergência.",
        )

        self.estoque.refresh_from_db()

        self.assertEqual(movimentacao.quantidade_anterior, 10)
        self.assertEqual(movimentacao.quantidade_movimentada, -7)
        self.assertEqual(movimentacao.quantidade_nova, 3)
        self.assertEqual(self.estoque.quantidade_bolsas, 3)

    def test_motivo_e_obrigatorio_na_movimentacao(self):
        with self.assertRaises(ValidationError):
            registrar_movimentacao_estoque(
                estoque=self.estoque,
                usuario_resp=self.hemocentro,
                tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
                quantidade=2,
                motivo="   ",
            )

        self.estoque.refresh_from_db()
        self.assertEqual(self.estoque.quantidade_bolsas, 10)
        self.assertEqual(
            EstoqueMovimentacao.objects.filter(estoque=self.estoque).count(),
            0,
        )

    def test_movimentacao_gera_historico_e_auditoria(self):
        registrar_movimentacao_estoque(
            estoque=self.estoque,
            usuario_resp=self.hemocentro,
            tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
            quantidade=2,
            motivo="Reposição do estoque.",
        )

        self.assertEqual(
            EstoqueMovimentacao.objects.filter(estoque=self.estoque).count(), 1
        )
        self.assertTrue(
            AuditoriaAcaoCritica.objects.filter(
                acao=AuditoriaAcaoCritica.Acao.ATUALIZACAO_ESTOQUE,
                usuario=self.hemocentro,
                alvo_id=str(self.estoque.pk),
            ).exists()
        )

    def test_outro_hemocentro_nao_pode_movimentar_estoque_alheio(self):
        outro_hemocentro = self.criar_usuario(
            email="outro@elo.test",
            nome="Outro Hemocentro",
            perfil=Usuario.Perfil.HEMOCENTRO,
        )
        aprovar_hemocentro(hemocentro=outro_hemocentro, admin=self.admin)
        outro_hemocentro.refresh_from_db()

        with self.assertRaises(PermissionDenied):
            registrar_movimentacao_estoque(
                estoque=self.estoque,
                usuario_resp=outro_hemocentro,
                tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
                quantidade=1,
            )

    def test_doador_nao_pode_movimentar_estoque(self):
        with self.assertRaises(PermissionDenied):
            registrar_movimentacao_estoque(
                estoque=self.estoque,
                usuario_resp=self.doador,
                tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA,
                quantidade=1,
            )
```

**Explicação deste trecho:**

**Linha 173 — ClassDef** (nível 0 do bloco).

Define a classe `RegistrarMovimentacaoEstoqueTests` herdando de `EstoqueTestsBase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 173:

**Linha 174 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 176 — FunctionDef** (nível 1 do bloco).

Define `setUp(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 176:

**Linha 177 — Expr** (nível 2 do bloco).

Executa a chamada `super().setUp`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 179 — Assign** (nível 2 do bloco).

Associa `self.estoque` a a chamada `cadastrar_estoque`; argumentos nomeados: `hemocentro=self.hemocentro`, `tipo_sanguineo='O-'`, `quantidade_bolsas=10`, `nivel_minimo=10`, `nivel_critico=5`.

- `hemocentro=self.hemocentro`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_sanguineo='O-'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `quantidade_bolsas=10`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nivel_minimo=10`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nivel_critico=5`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 187 — FunctionDef** (nível 1 do bloco).

Define `test_entrada_soma_quantidade_e_recalcula_status(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: entrada soma quantidade e recalcula status.

Bloco `body` da linha 187:

**Linha 188 — Assign** (nível 2 do bloco).

Associa `movimentacao` a a chamada `registrar_movimentacao_estoque`; argumentos nomeados: `estoque=self.estoque`, `usuario_resp=self.hemocentro`, `tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA`, `quantidade=15`, `motivo='Doação recebida em mutirão.'`.

- `estoque=self.estoque`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `usuario_resp=self.hemocentro`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `quantidade=15`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `motivo='Doação recebida em mutirão.'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 196 — Expr** (nível 2 do bloco).

Executa a chamada `self.estoque.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 198 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `movimentacao.quantidade_anterior`, `10`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 199 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `movimentacao.quantidade_movimentada`, `15`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 200 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `movimentacao.quantidade_nova`, `25`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 201 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.estoque.quantidade_bolsas`, `25`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 202 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.estoque.status_calculado`, `Estoque.StatusCalculado.ESTAVEL`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 204 — FunctionDef** (nível 1 do bloco).

Define `test_saida_subtrai_quantidade(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: saida subtrai quantidade.

Bloco `body` da linha 204:

**Linha 205 — Assign** (nível 2 do bloco).

Associa `movimentacao` a a chamada `registrar_movimentacao_estoque`; argumentos nomeados: `estoque=self.estoque`, `usuario_resp=self.hemocentro`, `tipo_movimento=EstoqueMovimentacao.TipoMovimento.SAIDA`, `quantidade=6`, `motivo='Transfusão de emergência.'`.

- `estoque=self.estoque`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `usuario_resp=self.hemocentro`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_movimento=EstoqueMovimentacao.TipoMovimento.SAIDA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `quantidade=6`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `motivo='Transfusão de emergência.'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 213 — Expr** (nível 2 do bloco).

Executa a chamada `self.estoque.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 215 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `movimentacao.quantidade_nova`, `4`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 216 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.estoque.quantidade_bolsas`, `4`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 217 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.estoque.status_calculado`, `Estoque.StatusCalculado.CRITICO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 219 — FunctionDef** (nível 1 do bloco).

Define `test_saida_maior_que_estoque_gera_erro_e_nao_altera_nada(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: saida maior que estoque gera erro e nao altera nada.

Bloco `body` da linha 219:

**Linha 220 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(ValidationError)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 220:

**Linha 221 — Expr** (nível 3 do bloco).

Executa a chamada `registrar_movimentacao_estoque`; argumentos nomeados: `estoque=self.estoque`, `usuario_resp=self.hemocentro`, `tipo_movimento=EstoqueMovimentacao.TipoMovimento.SAIDA`, `quantidade=999`, `motivo='Saída solicitada acima do estoque disponível.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 229 — Expr** (nível 2 do bloco).

Executa a chamada `self.estoque.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 230 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.estoque.quantidade_bolsas`, `10`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 231 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `EstoqueMovimentacao.objects.filter(estoque=self.estoque).count()`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 235 — FunctionDef** (nível 1 do bloco).

Define `test_ajuste_define_quantidade_absoluta_e_aceita_delta_negativo(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: ajuste define quantidade absoluta e aceita delta negativo.

Bloco `body` da linha 235:

**Linha 236 — Assign** (nível 2 do bloco).

Associa `movimentacao` a a chamada `registrar_movimentacao_estoque`; argumentos nomeados: `estoque=self.estoque`, `usuario_resp=self.hemocentro`, `tipo_movimento=EstoqueMovimentacao.TipoMovimento.AJUSTE`, `quantidade=3`, `motivo='Contagem física apontou divergência.'`.

- `estoque=self.estoque`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `usuario_resp=self.hemocentro`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_movimento=EstoqueMovimentacao.TipoMovimento.AJUSTE`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `quantidade=3`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `motivo='Contagem física apontou divergência.'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 244 — Expr** (nível 2 do bloco).

Executa a chamada `self.estoque.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 246 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `movimentacao.quantidade_anterior`, `10`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 247 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `movimentacao.quantidade_movimentada`, `-7`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 248 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `movimentacao.quantidade_nova`, `3`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 249 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.estoque.quantidade_bolsas`, `3`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 251 — FunctionDef** (nível 1 do bloco).

Define `test_motivo_e_obrigatorio_na_movimentacao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: motivo e obrigatorio na movimentacao.

Bloco `body` da linha 251:

**Linha 252 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(ValidationError)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 252:

**Linha 253 — Expr** (nível 3 do bloco).

Executa a chamada `registrar_movimentacao_estoque`; argumentos nomeados: `estoque=self.estoque`, `usuario_resp=self.hemocentro`, `tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA`, `quantidade=2`, `motivo='   '`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 261 — Expr** (nível 2 do bloco).

Executa a chamada `self.estoque.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 262 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.estoque.quantidade_bolsas`, `10`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 263 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `EstoqueMovimentacao.objects.filter(estoque=self.estoque).count()`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 268 — FunctionDef** (nível 1 do bloco).

Define `test_movimentacao_gera_historico_e_auditoria(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: movimentacao gera historico e auditoria.

Bloco `body` da linha 268:

**Linha 269 — Expr** (nível 2 do bloco).

Executa a chamada `registrar_movimentacao_estoque`; argumentos nomeados: `estoque=self.estoque`, `usuario_resp=self.hemocentro`, `tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA`, `quantidade=2`, `motivo='Reposição do estoque.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 277 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `EstoqueMovimentacao.objects.filter(estoque=self.estoque).count()`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 280 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `AuditoriaAcaoCritica.objects.filter(acao=AuditoriaAcaoCritica.Acao.ATUALIZACAO_ESTOQUE, usuario=self.hemocentro, alvo_id=str(self.estoque.pk)).exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 288 — FunctionDef** (nível 1 do bloco).

Define `test_outro_hemocentro_nao_pode_movimentar_estoque_alheio(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: outro hemocentro nao pode movimentar estoque alheio.

Bloco `body` da linha 288:

**Linha 289 — Assign** (nível 2 do bloco).

Associa `outro_hemocentro` a a chamada `self.criar_usuario`; argumentos nomeados: `email='outro@elo.test'`, `nome='Outro Hemocentro'`, `perfil=Usuario.Perfil.HEMOCENTRO`.

- `email='outro@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Outro Hemocentro'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.HEMOCENTRO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 294 — Expr** (nível 2 do bloco).

Executa a chamada `aprovar_hemocentro`; argumentos nomeados: `hemocentro=outro_hemocentro`, `admin=self.admin`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 295 — Expr** (nível 2 do bloco).

Executa a chamada `outro_hemocentro.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 297 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(PermissionDenied)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 297:

**Linha 298 — Expr** (nível 3 do bloco).

Executa a chamada `registrar_movimentacao_estoque`; argumentos nomeados: `estoque=self.estoque`, `usuario_resp=outro_hemocentro`, `tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA`, `quantidade=1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 305 — FunctionDef** (nível 1 do bloco).

Define `test_doador_nao_pode_movimentar_estoque(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: doador nao pode movimentar estoque.

Bloco `body` da linha 305:

**Linha 306 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(PermissionDenied)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 306:

**Linha 307 — Expr** (nível 3 do bloco).

Executa a chamada `registrar_movimentacao_estoque`; argumentos nomeados: `estoque=self.estoque`, `usuario_resp=self.doador`, `tipo_movimento=EstoqueMovimentacao.TipoMovimento.ENTRADA`, `quantidade=1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

### EstoqueViewsTests — linhas 315 a 372

```python
class EstoqueViewsTests(EstoqueTestsBase):
    """Testes de ponta a ponta usando o client de testes do Django."""

    def test_painel_bloqueia_hemocentro_pendente(self):
        self.client.force_login(self.hemocentro_pendente)

        resposta = self.client.get(reverse("accounts:estoque_hemocentro"))

        self.assertEqual(resposta.status_code, 403)

    def test_post_cadastra_estoque_via_view(self):
        self.client.force_login(self.hemocentro)

        resposta = self.client.post(
            reverse("accounts:cadastrar_estoque"),
            {
                "tipo_sanguineo": "AB+",
                "quantidade_bolsas": 4,
                "nivel_minimo": 10,
                "nivel_critico": 5,
            },
        )

        self.assertRedirects(resposta, reverse("accounts:estoque_hemocentro"))
        self.assertTrue(
            Estoque.objects.filter(
                hemocentro=self.hemocentro, tipo_sanguineo="AB+"
            ).exists()
        )

    def test_post_movimenta_estoque_via_view(self):
        estoque = cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="B-",
            quantidade_bolsas=5,
            nivel_minimo=10,
            nivel_critico=5,
        )

        self.client.force_login(self.hemocentro)

        resposta = self.client.post(
            reverse("accounts:atualizar_estoque", kwargs={"id_estoque": estoque.pk}),
            {
                "tipo_movimento": EstoqueMovimentacao.TipoMovimento.ENTRADA,
                "quantidade": 5,
                "motivo": "Reposição semanal.",
            },
        )

        self.assertRedirects(resposta, reverse("accounts:estoque_hemocentro"))

        estoque.refresh_from_db()
        self.assertEqual(estoque.quantidade_bolsas, 10)

        painel = self.client.get(reverse("accounts:estoque_hemocentro"))
        self.assertContains(painel, "Reposição semanal.")
        self.assertContains(painel, "Hemocentro Elo")
```

**Explicação deste trecho:**

**Linha 315 — ClassDef** (nível 0 do bloco).

Define a classe `EstoqueViewsTests` herdando de `EstoqueTestsBase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 315:

**Linha 316 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 318 — FunctionDef** (nível 1 do bloco).

Define `test_painel_bloqueia_hemocentro_pendente(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: painel bloqueia hemocentro pendente.

Bloco `body` da linha 318:

**Linha 319 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.hemocentro_pendente`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 321 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:estoque_hemocentro')`.


**Linha 323 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `403`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 325 — FunctionDef** (nível 1 do bloco).

Define `test_post_cadastra_estoque_via_view(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: post cadastra estoque via view.

Bloco `body` da linha 325:

**Linha 326 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.hemocentro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 328 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:cadastrar_estoque')`, `{'tipo_sanguineo': 'AB+', 'quantidade_bolsas': 4, 'nivel_minimo': 10, 'nivel_critico': 5}`.


**Linha 338 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:estoque_hemocentro')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 339 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `Estoque.objects.filter(hemocentro=self.hemocentro, tipo_sanguineo='AB+').exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 345 — FunctionDef** (nível 1 do bloco).

Define `test_post_movimenta_estoque_via_view(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: post movimenta estoque via view.

Bloco `body` da linha 345:

**Linha 346 — Assign** (nível 2 do bloco).

Associa `estoque` a a chamada `cadastrar_estoque`; argumentos nomeados: `hemocentro=self.hemocentro`, `tipo_sanguineo='B-'`, `quantidade_bolsas=5`, `nivel_minimo=10`, `nivel_critico=5`.

- `hemocentro=self.hemocentro`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_sanguineo='B-'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `quantidade_bolsas=5`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nivel_minimo=10`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nivel_critico=5`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 354 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.hemocentro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 356 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:atualizar_estoque', kwargs={'id_estoque': estoque.pk})`, `{'tipo_movimento': EstoqueMovimentacao.TipoMovimento.ENTRADA, 'quantidade': 5, 'motivo': 'Reposição semanal.'}`.


**Linha 365 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:estoque_hemocentro')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 367 — Expr** (nível 2 do bloco).

Executa a chamada `estoque.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 368 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `estoque.quantidade_bolsas`, `10`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 370 — Assign** (nível 2 do bloco).

Associa `painel` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:estoque_hemocentro')`.


**Linha 371 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `painel`, `'Reposição semanal.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 372 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `painel`, `'Hemocentro Elo'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

