# accounts/test_visualizacao.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

**Arquivo original:** [accounts/test_visualizacao.py](<C:/Users/lb119/Elo/accounts/test_visualizacao.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .estoque import cadastrar_estoque
from .models import Estoque, PedidoSangue, Usuario
from .validacao_hemocentro import aprovar_hemocentro


class VisualizacaoPublicaTests(TestCase):
    def criar_usuario(self, *, email, nome, perfil, cidade="", estado=""):
        return Usuario.objects.create_user(
            email=email,
            password="SenhaForte123!",
            nome=nome,
            perfil=perfil,
            cidade=cidade,
            estado=estado,
        )

    def setUp(self):
        self.admin = self.criar_usuario(
            email="admin@visualizacao.test",
            nome="Administrador",
            perfil=Usuario.Perfil.ADMINISTRADOR,
        )

        self.hemocentro = self.criar_usuario(
            email="hemocentro@visualizacao.test",
            nome="Hemocentro Central",
            perfil=Usuario.Perfil.HEMOCENTRO,
            cidade="Muzambinho",
            estado="MG",
        )

        aprovar_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.admin,
        )

        self.hemocentro.refresh_from_db()

        self.hemocentro_pendente = self.criar_usuario(
            email="pendente@visualizacao.test",
            nome="Hemocentro Pendente",
            perfil=Usuario.Perfil.HEMOCENTRO,
            cidade="Alfenas",
            estado="MG",
        )

    def pedido(self, *, status, tipo="O-", urgencia="ALTA"):
        return PedidoSangue.objects.create(
            nome_solicitante="Solicitante",
            contato="solicitante@visualizacao.test",
            hemocentro_destino=self.hemocentro,
            para_quem=PedidoSangue.ParaQuem.MIM,
            titulo=f"Pedido urgente de sangue {tipo}",
            tipo_sanguineo=tipo,
            urgencia=urgencia,
            cidade="Muzambinho",
            descricao=(
                "Necessidade de doadores para atendimento hospitalar."
            ),
            status=status,
            publicado_em=(
                timezone.now()
                if status == PedidoSangue.Status.PUBLICADA
                else None
            ),
        )

    def test_consulta_de_pedidos_aplica_filtros_e_oculta_nao_publicados(
        self,
    ):
        publicado = self.pedido(
            status=PedidoSangue.Status.PUBLICADA,
        )

        pendente = self.pedido(
            status=PedidoSangue.Status.ENVIADA,
            tipo="A+",
        )

        resposta = self.client.get(
            reverse("accounts:consultar_pedidos"),
            {
                "tipo_sanguineo": "O-",
                "urgencia": "ALTA",
                "cidade": "Muzambinho",
                "hemocentro": "Central",
                "data": date.today().isoformat(),
                "status": "PUBLICADA",
            },
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, publicado.titulo)
        self.assertNotContains(resposta, pendente.titulo)

        resposta = self.client.get(
            reverse("accounts:consultar_pedidos"),
            {
                "status": "ENVIADA",
            },
        )

        self.assertNotContains(resposta, publicado.titulo)

    def test_consulta_de_pedidos_nao_exibe_destino_nao_aprovado(self):
        pedido = PedidoSangue.objects.create(
            nome_solicitante="Solicitante",
            contato="solicitante@visualizacao.test",
            hemocentro_destino=self.hemocentro_pendente,
            para_quem=PedidoSangue.ParaQuem.MIM,
            titulo="Pedido de destino pendente",
            tipo_sanguineo="O-",
            urgencia=PedidoSangue.Urgencia.MEDIA,
            cidade="Alfenas",
            descricao=(
                "Pedido que não deve aparecer na consulta pública."
            ),
            status=PedidoSangue.Status.PUBLICADA,
        )

        resposta = self.client.get(
            reverse("accounts:consultar_pedidos")
        )

        self.assertNotContains(resposta, pedido.titulo)

    def test_consulta_de_estoques_filtra_por_tipo_situacao_e_busca(
        self,
    ):
        cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="O-",
            quantidade_bolsas=2,
            nivel_minimo=10,
            nivel_critico=5,
        )

        cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="A+",
            quantidade_bolsas=20,
            nivel_minimo=10,
            nivel_critico=5,
        )

        Estoque.objects.create(
            hemocentro=self.hemocentro_pendente,
            tipo_sanguineo="B+",
            quantidade_bolsas=10,
            nivel_minimo=10,
            nivel_critico=5,
        )

        resposta = self.client.get(
            reverse("accounts:estoque_publico"),
            {
                "tipo_sanguineo": "O-",
                "situacao": "CRITICO",
                "busca": "Central",
            },
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "O-")
        self.assertContains(resposta, "Crítico")
        self.assertNotContains(resposta, "20 bolsas")
        self.assertNotContains(resposta, "Hemocentro Pendente")

    def test_consulta_de_estoques_preserva_parametros_antigos(self):
        cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="O-",
            quantidade_bolsas=2,
            nivel_minimo=10,
            nivel_critico=5,
        )

        resposta = self.client.get(
            reverse("accounts:estoque_publico"),
            {
                "q": "Muzambinho",
                "tipo": "O-",
            },
        )

        self.assertContains(resposta, "O-")
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### ImportFrom — linhas 1 a 1

```python
from datetime import date
```

**Explicação deste trecho:**

**Linha 1 — ImportFrom** (nível 0 do bloco).

Importa de `datetime` os nomes `date`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 3 a 3

```python
from django.test import TestCase
```

**Explicação deste trecho:**

**Linha 3 — ImportFrom** (nível 0 do bloco).

Importa de `django.test` os nomes `TestCase`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 4 a 4

```python
from django.urls import reverse
```

**Explicação deste trecho:**

**Linha 4 — ImportFrom** (nível 0 do bloco).

Importa de `django.urls` os nomes `reverse`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 5 a 5

```python
from django.utils import timezone
```

**Explicação deste trecho:**

**Linha 5 — ImportFrom** (nível 0 do bloco).

Importa de `django.utils` os nomes `timezone`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 7 a 7

```python
from .estoque import cadastrar_estoque
```

**Explicação deste trecho:**

**Linha 7 — ImportFrom** (nível 0 do bloco).

Importa de `.estoque` os nomes `cadastrar_estoque`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 8 a 8

```python
from .models import Estoque, PedidoSangue, Usuario
```

**Explicação deste trecho:**

**Linha 8 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `Estoque`, `PedidoSangue`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 9 a 9

```python
from .validacao_hemocentro import aprovar_hemocentro
```

**Explicação deste trecho:**

**Linha 9 — ImportFrom** (nível 0 do bloco).

Importa de `.validacao_hemocentro` os nomes `aprovar_hemocentro`. Pontos iniciais indicam importação relativa ao pacote.

### VisualizacaoPublicaTests — linhas 12 a 192

```python
class VisualizacaoPublicaTests(TestCase):
    def criar_usuario(self, *, email, nome, perfil, cidade="", estado=""):
        return Usuario.objects.create_user(
            email=email,
            password="SenhaForte123!",
            nome=nome,
            perfil=perfil,
            cidade=cidade,
            estado=estado,
        )

    def setUp(self):
        self.admin = self.criar_usuario(
            email="admin@visualizacao.test",
            nome="Administrador",
            perfil=Usuario.Perfil.ADMINISTRADOR,
        )

        self.hemocentro = self.criar_usuario(
            email="hemocentro@visualizacao.test",
            nome="Hemocentro Central",
            perfil=Usuario.Perfil.HEMOCENTRO,
            cidade="Muzambinho",
            estado="MG",
        )

        aprovar_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.admin,
        )

        self.hemocentro.refresh_from_db()

        self.hemocentro_pendente = self.criar_usuario(
            email="pendente@visualizacao.test",
            nome="Hemocentro Pendente",
            perfil=Usuario.Perfil.HEMOCENTRO,
            cidade="Alfenas",
            estado="MG",
        )

    def pedido(self, *, status, tipo="O-", urgencia="ALTA"):
        return PedidoSangue.objects.create(
            nome_solicitante="Solicitante",
            contato="solicitante@visualizacao.test",
            hemocentro_destino=self.hemocentro,
            para_quem=PedidoSangue.ParaQuem.MIM,
            titulo=f"Pedido urgente de sangue {tipo}",
            tipo_sanguineo=tipo,
            urgencia=urgencia,
            cidade="Muzambinho",
            descricao=(
                "Necessidade de doadores para atendimento hospitalar."
            ),
            status=status,
            publicado_em=(
                timezone.now()
                if status == PedidoSangue.Status.PUBLICADA
                else None
            ),
        )

    def test_consulta_de_pedidos_aplica_filtros_e_oculta_nao_publicados(
        self,
    ):
        publicado = self.pedido(
            status=PedidoSangue.Status.PUBLICADA,
        )

        pendente = self.pedido(
            status=PedidoSangue.Status.ENVIADA,
            tipo="A+",
        )

        resposta = self.client.get(
            reverse("accounts:consultar_pedidos"),
            {
                "tipo_sanguineo": "O-",
                "urgencia": "ALTA",
                "cidade": "Muzambinho",
                "hemocentro": "Central",
                "data": date.today().isoformat(),
                "status": "PUBLICADA",
            },
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, publicado.titulo)
        self.assertNotContains(resposta, pendente.titulo)

        resposta = self.client.get(
            reverse("accounts:consultar_pedidos"),
            {
                "status": "ENVIADA",
            },
        )

        self.assertNotContains(resposta, publicado.titulo)

    def test_consulta_de_pedidos_nao_exibe_destino_nao_aprovado(self):
        pedido = PedidoSangue.objects.create(
            nome_solicitante="Solicitante",
            contato="solicitante@visualizacao.test",
            hemocentro_destino=self.hemocentro_pendente,
            para_quem=PedidoSangue.ParaQuem.MIM,
            titulo="Pedido de destino pendente",
            tipo_sanguineo="O-",
            urgencia=PedidoSangue.Urgencia.MEDIA,
            cidade="Alfenas",
            descricao=(
                "Pedido que não deve aparecer na consulta pública."
            ),
            status=PedidoSangue.Status.PUBLICADA,
        )

        resposta = self.client.get(
            reverse("accounts:consultar_pedidos")
        )

        self.assertNotContains(resposta, pedido.titulo)

    def test_consulta_de_estoques_filtra_por_tipo_situacao_e_busca(
        self,
    ):
        cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="O-",
            quantidade_bolsas=2,
            nivel_minimo=10,
            nivel_critico=5,
        )

        cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="A+",
            quantidade_bolsas=20,
            nivel_minimo=10,
            nivel_critico=5,
        )

        Estoque.objects.create(
            hemocentro=self.hemocentro_pendente,
            tipo_sanguineo="B+",
            quantidade_bolsas=10,
            nivel_minimo=10,
            nivel_critico=5,
        )

        resposta = self.client.get(
            reverse("accounts:estoque_publico"),
            {
                "tipo_sanguineo": "O-",
                "situacao": "CRITICO",
                "busca": "Central",
            },
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "O-")
        self.assertContains(resposta, "Crítico")
        self.assertNotContains(resposta, "20 bolsas")
        self.assertNotContains(resposta, "Hemocentro Pendente")

    def test_consulta_de_estoques_preserva_parametros_antigos(self):
        cadastrar_estoque(
            hemocentro=self.hemocentro,
            tipo_sanguineo="O-",
            quantidade_bolsas=2,
            nivel_minimo=10,
            nivel_critico=5,
        )

        resposta = self.client.get(
            reverse("accounts:estoque_publico"),
            {
                "q": "Muzambinho",
                "tipo": "O-",
            },
        )

        self.assertContains(resposta, "O-")
```

**Explicação deste trecho:**

**Linha 12 — ClassDef** (nível 0 do bloco).

Define a classe `VisualizacaoPublicaTests` herdando de `TestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 12:

**Linha 13 — FunctionDef** (nível 1 do bloco).

Define `criar_usuario(self, *, email, nome, perfil, cidade='', estado='')`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 13:

**Linha 14 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `Usuario.objects.create_user`; argumentos nomeados: `email=email`, `password='SenhaForte123!'`, `nome=nome`, `perfil=perfil`, `cidade=cidade`, `estado=estado` ao chamador.

**Linha 23 — FunctionDef** (nível 1 do bloco).

Define `setUp(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 23:

**Linha 24 — Assign** (nível 2 do bloco).

Associa `self.admin` a a chamada `self.criar_usuario`; argumentos nomeados: `email='admin@visualizacao.test'`, `nome='Administrador'`, `perfil=Usuario.Perfil.ADMINISTRADOR`.

- `email='admin@visualizacao.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Administrador'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.ADMINISTRADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 30 — Assign** (nível 2 do bloco).

Associa `self.hemocentro` a a chamada `self.criar_usuario`; argumentos nomeados: `email='hemocentro@visualizacao.test'`, `nome='Hemocentro Central'`, `perfil=Usuario.Perfil.HEMOCENTRO`, `cidade='Muzambinho'`, `estado='MG'`.

- `email='hemocentro@visualizacao.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Hemocentro Central'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.HEMOCENTRO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `cidade='Muzambinho'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `estado='MG'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 38 — Expr** (nível 2 do bloco).

Executa a chamada `aprovar_hemocentro`; argumentos nomeados: `hemocentro=self.hemocentro`, `admin=self.admin`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 43 — Expr** (nível 2 do bloco).

Executa a chamada `self.hemocentro.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 45 — Assign** (nível 2 do bloco).

Associa `self.hemocentro_pendente` a a chamada `self.criar_usuario`; argumentos nomeados: `email='pendente@visualizacao.test'`, `nome='Hemocentro Pendente'`, `perfil=Usuario.Perfil.HEMOCENTRO`, `cidade='Alfenas'`, `estado='MG'`.

- `email='pendente@visualizacao.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Hemocentro Pendente'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.HEMOCENTRO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `cidade='Alfenas'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `estado='MG'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 53 — FunctionDef** (nível 1 do bloco).

Define `pedido(self, *, status, tipo='O-', urgencia='ALTA')`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 53:

**Linha 54 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `PedidoSangue.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `nome_solicitante='Solicitante'`, `contato='solicitante@visualizacao.test'`, `hemocentro_destino=self.hemocentro`, `para_quem=PedidoSangue.ParaQuem.MIM`, `titulo=f'Pedido urgente de sangue {tipo}'`, `tipo_sanguineo=tipo`, `urgencia=urgencia`, `cidade='Muzambinho'`, `descricao='Necessidade de doadores para atendimento hospitalar.'`, `status=status`, `publicado_em=timezone.now() if status == PedidoSangue.Status.PUBLICADA else None` ao chamador.

**Linha 74 — FunctionDef** (nível 1 do bloco).

Define `test_consulta_de_pedidos_aplica_filtros_e_oculta_nao_publicados(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: consulta de pedidos aplica filtros e oculta nao publicados.

Bloco `body` da linha 74:

**Linha 77 — Assign** (nível 2 do bloco).

Associa `publicado` a a chamada `self.pedido`; argumentos nomeados: `status=PedidoSangue.Status.PUBLICADA`.

- `status=PedidoSangue.Status.PUBLICADA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 81 — Assign** (nível 2 do bloco).

Associa `pendente` a a chamada `self.pedido`; argumentos nomeados: `status=PedidoSangue.Status.ENVIADA`, `tipo='A+'`.

- `status=PedidoSangue.Status.ENVIADA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo='A+'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 86 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:consultar_pedidos')`, `{'tipo_sanguineo': 'O-', 'urgencia': 'ALTA', 'cidade': 'Muzambinho', 'hemocentro': 'Central', 'data': date.today().isoformat(), 'status': 'PUBLICADA'}`.


**Linha 98 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `200`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 99 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `publicado.titulo`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 100 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotContains`, que o teste exige ausência de texto na resposta HTTP; argumentos posicionais: `resposta`, `pendente.titulo`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 102 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:consultar_pedidos')`, `{'status': 'ENVIADA'}`.


**Linha 109 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotContains`, que o teste exige ausência de texto na resposta HTTP; argumentos posicionais: `resposta`, `publicado.titulo`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 111 — FunctionDef** (nível 1 do bloco).

Define `test_consulta_de_pedidos_nao_exibe_destino_nao_aprovado(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: consulta de pedidos nao exibe destino nao aprovado.

Bloco `body` da linha 111:

**Linha 112 — Assign** (nível 2 do bloco).

Associa `pedido` a a chamada `PedidoSangue.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `nome_solicitante='Solicitante'`, `contato='solicitante@visualizacao.test'`, `hemocentro_destino=self.hemocentro_pendente`, `para_quem=PedidoSangue.ParaQuem.MIM`, `titulo='Pedido de destino pendente'`, `tipo_sanguineo='O-'`, `urgencia=PedidoSangue.Urgencia.MEDIA`, `cidade='Alfenas'`, `descricao='Pedido que não deve aparecer na consulta pública.'`, `status=PedidoSangue.Status.PUBLICADA`.

- `nome_solicitante='Solicitante'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `contato='solicitante@visualizacao.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `hemocentro_destino=self.hemocentro_pendente`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `para_quem=PedidoSangue.ParaQuem.MIM`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `titulo='Pedido de destino pendente'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_sanguineo='O-'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `urgencia=PedidoSangue.Urgencia.MEDIA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `cidade='Alfenas'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `descricao='Pedido que não deve aparecer na consulta pública.'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status=PedidoSangue.Status.PUBLICADA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 127 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:consultar_pedidos')`.


**Linha 131 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotContains`, que o teste exige ausência de texto na resposta HTTP; argumentos posicionais: `resposta`, `pedido.titulo`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 133 — FunctionDef** (nível 1 do bloco).

Define `test_consulta_de_estoques_filtra_por_tipo_situacao_e_busca(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: consulta de estoques filtra por tipo situacao e busca.

Bloco `body` da linha 133:

**Linha 136 — Expr** (nível 2 do bloco).

Executa a chamada `cadastrar_estoque`; argumentos nomeados: `hemocentro=self.hemocentro`, `tipo_sanguineo='O-'`, `quantidade_bolsas=2`, `nivel_minimo=10`, `nivel_critico=5`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 144 — Expr** (nível 2 do bloco).

Executa a chamada `cadastrar_estoque`; argumentos nomeados: `hemocentro=self.hemocentro`, `tipo_sanguineo='A+'`, `quantidade_bolsas=20`, `nivel_minimo=10`, `nivel_critico=5`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 152 — Expr** (nível 2 do bloco).

Executa a chamada `Estoque.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `hemocentro=self.hemocentro_pendente`, `tipo_sanguineo='B+'`, `quantidade_bolsas=10`, `nivel_minimo=10`, `nivel_critico=5`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 160 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:estoque_publico')`, `{'tipo_sanguineo': 'O-', 'situacao': 'CRITICO', 'busca': 'Central'}`.


**Linha 169 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `200`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 170 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'O-'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 171 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Crítico'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 172 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotContains`, que o teste exige ausência de texto na resposta HTTP; argumentos posicionais: `resposta`, `'20 bolsas'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 173 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotContains`, que o teste exige ausência de texto na resposta HTTP; argumentos posicionais: `resposta`, `'Hemocentro Pendente'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 175 — FunctionDef** (nível 1 do bloco).

Define `test_consulta_de_estoques_preserva_parametros_antigos(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: consulta de estoques preserva parametros antigos.

Bloco `body` da linha 175:

**Linha 176 — Expr** (nível 2 do bloco).

Executa a chamada `cadastrar_estoque`; argumentos nomeados: `hemocentro=self.hemocentro`, `tipo_sanguineo='O-'`, `quantidade_bolsas=2`, `nivel_minimo=10`, `nivel_critico=5`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 184 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:estoque_publico')`, `{'q': 'Muzambinho', 'tipo': 'O-'}`.


**Linha 192 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'O-'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

