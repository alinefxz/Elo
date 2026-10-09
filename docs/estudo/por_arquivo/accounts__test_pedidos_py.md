# accounts/test_pedidos.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

**Arquivo original:** [accounts/test_pedidos.py](<C:/Users/lb119/Elo/accounts/test_pedidos.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
from django.test import TestCase
from django.urls import reverse

from .forms import PedidoSangueForm
from .models import PedidoSangue, Usuario, ValidacaoPedido
from .validacao_hemocentro import aprovar_hemocentro
from .validacao_pedido import aprovar_pedido, criar_pedido_pendente, marcar_pedido_suspeito


class PedidoSangueTests(TestCase):
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
        self.receptor = self.criar_usuario(
            email="receptor@elo.test",
            nome="Receptor Elo",
            perfil=Usuario.Perfil.RECEPTOR,
        )
        self.doador = self.criar_usuario(
            email="doador@elo.test",
            nome="Doador Elo",
            perfil=Usuario.Perfil.DOADOR,
        )
        self.administrador = self.criar_usuario(
            email="admin@elo.test",
            nome="Administrador Elo",
            perfil=Usuario.Perfil.ADMINISTRADOR,
        )
        self.hemocentro = self.criar_usuario(
            email="hemocentro@elo.test",
            nome="Hemocentro Muzambinho",
            perfil=Usuario.Perfil.HEMOCENTRO,
            cidade="Muzambinho",
            estado="MG",
        )
        aprovar_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.administrador,
        )
        self.hemocentro.refresh_from_db()

        self.hemocentro_pendente = self.criar_usuario(
            email="pendente@elo.test",
            nome="Hemocentro Pendente",
            perfil=Usuario.Perfil.HEMOCENTRO,
            cidade="Alfenas",
            estado="MG",
        )

    def dados_validos(self, **alteracoes):
        dados = {
            "nome_solicitante": "Solicitante de exemplo",
            "contato": "receptor@elo.test",
            "para_quem": PedidoSangue.ParaQuem.OUTRA_PESSOA,
            "hemocentro_destino": self.hemocentro.pk,
            "titulo": "Doacao para paciente internado",
            "tipo_sanguineo": "O-",
            "urgencia": PedidoSangue.Urgencia.BAIXA,
            "cidade": "Muzambinho",
            "nome_paciente": "Paciente de exemplo",
            "descricao": (
                "Precisamos de doadores para auxiliar um paciente internado."
            ),
            "justificativa_urgencia": "",
            "informacoes_complementares": "Retorno por telefone.",
        }
        dados.update(alteracoes)
        return dados

    def test_formulario_lista_apenas_hemocentros_aprovados(self):
        form = PedidoSangueForm()

        self.assertIn("para_quem", form.fields)
        self.assertIn("nome_paciente", form.fields)
        self.assertEqual(
            list(form.fields["hemocentro_destino"].queryset),
            [self.hemocentro],
        )

    def test_receptor_cria_solicitacao_enviada(self):
        self.client.force_login(self.receptor)

        resposta = self.client.post(
            reverse("accounts:pedido_publicar"),
            self.dados_validos(),
        )

        self.assertRedirects(resposta, reverse("accounts:minhas_solicitacoes"))
        pedido = PedidoSangue.objects.get()
        self.assertEqual(pedido.solicitante, self.receptor)
        self.assertEqual(pedido.hemocentro_destino, self.hemocentro)
        self.assertEqual(
            pedido.status,
            PedidoSangue.Status.ENVIADA,
        )

    def test_doador_nao_pode_enviar_solicitacao(self):
        self.client.force_login(self.doador)
        resposta = self.client.post(reverse("accounts:pedido_publicar"), self.dados_validos())
        self.assertRedirects(resposta, reverse("accounts:dashboard"))
        self.assertFalse(PedidoSangue.objects.exists())

    def test_visitante_precisa_entrar(self):
        url = reverse("accounts:pedido_publicar")
        resposta = self.client.get(url)
        self.assertRedirects(resposta, f"{reverse('accounts:login')}?next={url}")

    def test_formulario_rejeita_descricao_curta(self):
        form = PedidoSangueForm(self.dados_validos(descricao="Curto"))

        self.assertFalse(form.is_valid())
        self.assertIn("descricao", form.errors)

    def test_formulario_exige_email_no_contato(self):
        form_invalido = PedidoSangueForm(
            self.dados_validos(contato="(31) 99999-0000")
        )
        self.assertFalse(form_invalido.is_valid())
        self.assertIn("contato", form_invalido.errors)

        form_valido = PedidoSangueForm(
            self.dados_validos(contato="  Receptor@Elo.Test ")
        )
        self.assertTrue(form_valido.is_valid())
        self.assertEqual(
            form_valido.cleaned_data["contato"],
            "receptor@elo.test",
        )

    def test_formulario_rejeita_hemocentro_pendente(self):
        form = PedidoSangueForm(
            self.dados_validos(
                hemocentro_destino=self.hemocentro_pendente.pk,
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn("hemocentro_destino", form.errors)

    def test_urgencia_critica_exige_justificativa(self):
        form = PedidoSangueForm(
            self.dados_validos(
                urgencia=PedidoSangue.Urgencia.CRITICA,
                justificativa_urgencia="Curta",
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn("justificativa_urgencia", form.errors)

    def test_hemocentro_aprova_pedido_e_registra_historico(self):
        self.client.force_login(self.receptor)
        self.client.post(
            reverse("accounts:pedido_publicar"),
            self.dados_validos(),
        )
        pedido = PedidoSangue.objects.get()

        validacao = aprovar_pedido(
            pedido=pedido,
            moderador=self.hemocentro,
            motivo="Dados conferidos pelo administrador.",
        )

        pedido.refresh_from_db()
        self.assertEqual(pedido.status, PedidoSangue.Status.PUBLICADA)
        self.assertEqual(
            validacao.status_validacao,
            ValidacaoPedido.StatusValidacao.APROVADO,
        )
        self.assertEqual(pedido.validacoes.count(), 1)

    def test_admin_moderar_pedido_nao_publica(self):
        pedido = criar_pedido_pendente(
            dados=self.dados_validos(),
            solicitante=self.receptor,
        )

        self.client.force_login(self.administrador)

        resposta = self.client.get(
            reverse("accounts:painel_validacao_pedidos")
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, str(pedido.pk))

        resposta = self.client.post(
            reverse(
                "accounts:marcar_pedido_suspeito",
                kwargs={"id_pedido": pedido.pk},
            ),
            {"motivo": "Há solicitação semelhante para o mesmo destino."},
        )

        self.assertRedirects(
            resposta,
            reverse("accounts:painel_validacao_pedidos"),
        )
        pedido.refresh_from_db()
        self.assertEqual(
            pedido.status,
            PedidoSangue.Status.EM_ANALISE,
        )
        self.assertFalse(pedido.publicado_por_id)
        self.assertEqual(
            pedido.validacoes.latest("data_validacao").status_validacao,
            ValidacaoPedido.StatusValidacao.SUSPEITO,
        )

    def test_hemocentro_nao_acessa_moderacao_administrativa(self):
        self.client.force_login(self.hemocentro)

        resposta = self.client.get(
            reverse("accounts:painel_validacao_pedidos")
        )

        self.assertEqual(resposta.status_code, 403)

    def test_publicacao_exclusiva_do_hemocentro_responsavel(self):
        from django.core.exceptions import PermissionDenied
        self.client.force_login(self.receptor)
        self.client.post(reverse('accounts:pedido_publicar'), self.dados_validos())
        pedido = PedidoSangue.objects.get()
        self.client.force_login(self.hemocentro_pendente)
        self.assertEqual(self.client.get(reverse('accounts:painel_pedidos_hemocentro')).status_code, 403)
        with self.assertRaises(PermissionDenied):
            aprovar_pedido(pedido=pedido, moderador=self.hemocentro_pendente)
        self.hemocentro_pendente.status_validacao = Usuario.StatusValidacaoHemocentro.APROVADO
        self.hemocentro_pendente.save()
        with self.assertRaises(PermissionDenied):
            aprovar_pedido(pedido=pedido, moderador=self.hemocentro_pendente)
        self.assertNotContains(self.client.get(reverse('accounts:painel_pedidos_hemocentro')), pedido.titulo)
        self.client.force_login(self.hemocentro)
        self.assertContains(self.client.get(reverse('accounts:painel_pedidos_hemocentro')), pedido.titulo)
        resposta = self.client.post(reverse('accounts:aprovar_pedido', kwargs={'id_pedido': pedido.pk}))
        self.assertEqual(resposta.status_code, 302)
        pedido.refresh_from_db()
        self.assertEqual(pedido.status, PedidoSangue.Status.PUBLICADA)

    def test_permissao_do_servico_de_publicacao(self):
        from .pedidos import pode_publicar_pedido
        for usuario in (self.receptor, self.doador, self.administrador, self.hemocentro_pendente):
            with self.subTest(perfil=usuario.perfil):
                self.assertFalse(pode_publicar_pedido(usuario))
        self.assertTrue(pode_publicar_pedido(self.hemocentro))

    def test_auditoria_distingue_validacao_e_publicacao(self):
        from .models import AuditoriaAcaoCritica
        self.client.force_login(self.receptor)
        self.client.post(reverse('accounts:pedido_publicar'), self.dados_validos())
        pedido = PedidoSangue.objects.get()
        marcar_pedido_suspeito(pedido=pedido, moderador=self.administrador)
        registro = AuditoriaAcaoCritica.objects.filter(alvo_tipo='accounts.PedidoSangue').latest('id_auditoria')
        self.assertEqual(registro.metadados['evento'], 'VALIDACAO_PEDIDO')
        self.assertEqual(registro.metadados['status_anterior'], PedidoSangue.Status.ENVIADA)
        self.assertEqual(registro.metadados['status_pedido'], PedidoSangue.Status.EM_ANALISE)
        aprovar_pedido(pedido=pedido, moderador=self.hemocentro)
        registro = AuditoriaAcaoCritica.objects.filter(alvo_tipo='accounts.PedidoSangue').latest('id_auditoria')
        self.assertEqual(registro.usuario, self.hemocentro)
        self.assertEqual(registro.metadados['evento'], 'PUBLICACAO_PEDIDO')
        self.assertEqual(registro.metadados['status_pedido'], PedidoSangue.Status.PUBLICADA)
        self.assertNotIn('Paciente de exemplo', str(registro.metadados))

    def test_tentativa_de_publicacao_alheia_persiste_na_auditoria(self):
        from .models import AuditoriaAcaoCritica
        self.client.force_login(self.receptor)
        self.client.post(reverse('accounts:pedido_publicar'), self.dados_validos())
        pedido = PedidoSangue.objects.get()
        self.hemocentro_pendente.status_validacao = Usuario.StatusValidacaoHemocentro.APROVADO
        self.hemocentro_pendente.save()
        self.client.force_login(self.hemocentro_pendente)
        resposta = self.client.post(reverse('accounts:aprovar_pedido', kwargs={'id_pedido': pedido.pk}))
        self.assertEqual(resposta.status_code, 403)
        registro = AuditoriaAcaoCritica.objects.filter(usuario=self.hemocentro_pendente).latest('id_auditoria')
        self.assertEqual(registro.resultado, AuditoriaAcaoCritica.Resultado.BLOQUEADO)
        pedido.refresh_from_db()
        self.assertEqual(pedido.status, PedidoSangue.Status.ENVIADA)
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### ImportFrom — linhas 1 a 1

```python
from django.test import TestCase
```

**Explicação deste trecho:**

**Linha 1 — ImportFrom** (nível 0 do bloco).

Importa de `django.test` os nomes `TestCase`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 2 a 2

```python
from django.urls import reverse
```

**Explicação deste trecho:**

**Linha 2 — ImportFrom** (nível 0 do bloco).

Importa de `django.urls` os nomes `reverse`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 4 a 4

```python
from .forms import PedidoSangueForm
```

**Explicação deste trecho:**

**Linha 4 — ImportFrom** (nível 0 do bloco).

Importa de `.forms` os nomes `PedidoSangueForm`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 5 a 5

```python
from .models import PedidoSangue, Usuario, ValidacaoPedido
```

**Explicação deste trecho:**

**Linha 5 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `PedidoSangue`, `Usuario`, `ValidacaoPedido`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 6 a 6

```python
from .validacao_hemocentro import aprovar_hemocentro
```

**Explicação deste trecho:**

**Linha 6 — ImportFrom** (nível 0 do bloco).

Importa de `.validacao_hemocentro` os nomes `aprovar_hemocentro`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 7 a 7

```python
from .validacao_pedido import aprovar_pedido, criar_pedido_pendente, marcar_pedido_suspeito
```

**Explicação deste trecho:**

**Linha 7 — ImportFrom** (nível 0 do bloco).

Importa de `.validacao_pedido` os nomes `aprovar_pedido`, `criar_pedido_pendente`, `marcar_pedido_suspeito`. Pontos iniciais indicam importação relativa ao pacote.

### PedidoSangueTests — linhas 10 a 286

```python
class PedidoSangueTests(TestCase):
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
        self.receptor = self.criar_usuario(
            email="receptor@elo.test",
            nome="Receptor Elo",
            perfil=Usuario.Perfil.RECEPTOR,
        )
        self.doador = self.criar_usuario(
            email="doador@elo.test",
            nome="Doador Elo",
            perfil=Usuario.Perfil.DOADOR,
        )
        self.administrador = self.criar_usuario(
            email="admin@elo.test",
            nome="Administrador Elo",
            perfil=Usuario.Perfil.ADMINISTRADOR,
        )
        self.hemocentro = self.criar_usuario(
            email="hemocentro@elo.test",
            nome="Hemocentro Muzambinho",
            perfil=Usuario.Perfil.HEMOCENTRO,
            cidade="Muzambinho",
            estado="MG",
        )
        aprovar_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.administrador,
        )
        self.hemocentro.refresh_from_db()

        self.hemocentro_pendente = self.criar_usuario(
            email="pendente@elo.test",
            nome="Hemocentro Pendente",
            perfil=Usuario.Perfil.HEMOCENTRO,
            cidade="Alfenas",
            estado="MG",
        )

    def dados_validos(self, **alteracoes):
        dados = {
            "nome_solicitante": "Solicitante de exemplo",
            "contato": "receptor@elo.test",
            "para_quem": PedidoSangue.ParaQuem.OUTRA_PESSOA,
            "hemocentro_destino": self.hemocentro.pk,
            "titulo": "Doacao para paciente internado",
            "tipo_sanguineo": "O-",
            "urgencia": PedidoSangue.Urgencia.BAIXA,
            "cidade": "Muzambinho",
            "nome_paciente": "Paciente de exemplo",
            "descricao": (
                "Precisamos de doadores para auxiliar um paciente internado."
            ),
            "justificativa_urgencia": "",
            "informacoes_complementares": "Retorno por telefone.",
        }
        dados.update(alteracoes)
        return dados

    def test_formulario_lista_apenas_hemocentros_aprovados(self):
        form = PedidoSangueForm()

        self.assertIn("para_quem", form.fields)
        self.assertIn("nome_paciente", form.fields)
        self.assertEqual(
            list(form.fields["hemocentro_destino"].queryset),
            [self.hemocentro],
        )

    def test_receptor_cria_solicitacao_enviada(self):
        self.client.force_login(self.receptor)

        resposta = self.client.post(
            reverse("accounts:pedido_publicar"),
            self.dados_validos(),
        )

        self.assertRedirects(resposta, reverse("accounts:minhas_solicitacoes"))
        pedido = PedidoSangue.objects.get()
        self.assertEqual(pedido.solicitante, self.receptor)
        self.assertEqual(pedido.hemocentro_destino, self.hemocentro)
        self.assertEqual(
            pedido.status,
            PedidoSangue.Status.ENVIADA,
        )

    def test_doador_nao_pode_enviar_solicitacao(self):
        self.client.force_login(self.doador)
        resposta = self.client.post(reverse("accounts:pedido_publicar"), self.dados_validos())
        self.assertRedirects(resposta, reverse("accounts:dashboard"))
        self.assertFalse(PedidoSangue.objects.exists())

    def test_visitante_precisa_entrar(self):
        url = reverse("accounts:pedido_publicar")
        resposta = self.client.get(url)
        self.assertRedirects(resposta, f"{reverse('accounts:login')}?next={url}")

    def test_formulario_rejeita_descricao_curta(self):
        form = PedidoSangueForm(self.dados_validos(descricao="Curto"))

        self.assertFalse(form.is_valid())
        self.assertIn("descricao", form.errors)

    def test_formulario_exige_email_no_contato(self):
        form_invalido = PedidoSangueForm(
            self.dados_validos(contato="(31) 99999-0000")
        )
        self.assertFalse(form_invalido.is_valid())
        self.assertIn("contato", form_invalido.errors)

        form_valido = PedidoSangueForm(
            self.dados_validos(contato="  Receptor@Elo.Test ")
        )
        self.assertTrue(form_valido.is_valid())
        self.assertEqual(
            form_valido.cleaned_data["contato"],
            "receptor@elo.test",
        )

    def test_formulario_rejeita_hemocentro_pendente(self):
        form = PedidoSangueForm(
            self.dados_validos(
                hemocentro_destino=self.hemocentro_pendente.pk,
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn("hemocentro_destino", form.errors)

    def test_urgencia_critica_exige_justificativa(self):
        form = PedidoSangueForm(
            self.dados_validos(
                urgencia=PedidoSangue.Urgencia.CRITICA,
                justificativa_urgencia="Curta",
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn("justificativa_urgencia", form.errors)

    def test_hemocentro_aprova_pedido_e_registra_historico(self):
        self.client.force_login(self.receptor)
        self.client.post(
            reverse("accounts:pedido_publicar"),
            self.dados_validos(),
        )
        pedido = PedidoSangue.objects.get()

        validacao = aprovar_pedido(
            pedido=pedido,
            moderador=self.hemocentro,
            motivo="Dados conferidos pelo administrador.",
        )

        pedido.refresh_from_db()
        self.assertEqual(pedido.status, PedidoSangue.Status.PUBLICADA)
        self.assertEqual(
            validacao.status_validacao,
            ValidacaoPedido.StatusValidacao.APROVADO,
        )
        self.assertEqual(pedido.validacoes.count(), 1)

    def test_admin_moderar_pedido_nao_publica(self):
        pedido = criar_pedido_pendente(
            dados=self.dados_validos(),
            solicitante=self.receptor,
        )

        self.client.force_login(self.administrador)

        resposta = self.client.get(
            reverse("accounts:painel_validacao_pedidos")
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, str(pedido.pk))

        resposta = self.client.post(
            reverse(
                "accounts:marcar_pedido_suspeito",
                kwargs={"id_pedido": pedido.pk},
            ),
            {"motivo": "Há solicitação semelhante para o mesmo destino."},
        )

        self.assertRedirects(
            resposta,
            reverse("accounts:painel_validacao_pedidos"),
        )
        pedido.refresh_from_db()
        self.assertEqual(
            pedido.status,
            PedidoSangue.Status.EM_ANALISE,
        )
        self.assertFalse(pedido.publicado_por_id)
        self.assertEqual(
            pedido.validacoes.latest("data_validacao").status_validacao,
            ValidacaoPedido.StatusValidacao.SUSPEITO,
        )

    def test_hemocentro_nao_acessa_moderacao_administrativa(self):
        self.client.force_login(self.hemocentro)

        resposta = self.client.get(
            reverse("accounts:painel_validacao_pedidos")
        )

        self.assertEqual(resposta.status_code, 403)

    def test_publicacao_exclusiva_do_hemocentro_responsavel(self):
        from django.core.exceptions import PermissionDenied
        self.client.force_login(self.receptor)
        self.client.post(reverse('accounts:pedido_publicar'), self.dados_validos())
        pedido = PedidoSangue.objects.get()
        self.client.force_login(self.hemocentro_pendente)
        self.assertEqual(self.client.get(reverse('accounts:painel_pedidos_hemocentro')).status_code, 403)
        with self.assertRaises(PermissionDenied):
            aprovar_pedido(pedido=pedido, moderador=self.hemocentro_pendente)
        self.hemocentro_pendente.status_validacao = Usuario.StatusValidacaoHemocentro.APROVADO
        self.hemocentro_pendente.save()
        with self.assertRaises(PermissionDenied):
            aprovar_pedido(pedido=pedido, moderador=self.hemocentro_pendente)
        self.assertNotContains(self.client.get(reverse('accounts:painel_pedidos_hemocentro')), pedido.titulo)
        self.client.force_login(self.hemocentro)
        self.assertContains(self.client.get(reverse('accounts:painel_pedidos_hemocentro')), pedido.titulo)
        resposta = self.client.post(reverse('accounts:aprovar_pedido', kwargs={'id_pedido': pedido.pk}))
        self.assertEqual(resposta.status_code, 302)
        pedido.refresh_from_db()
        self.assertEqual(pedido.status, PedidoSangue.Status.PUBLICADA)

    def test_permissao_do_servico_de_publicacao(self):
        from .pedidos import pode_publicar_pedido
        for usuario in (self.receptor, self.doador, self.administrador, self.hemocentro_pendente):
            with self.subTest(perfil=usuario.perfil):
                self.assertFalse(pode_publicar_pedido(usuario))
        self.assertTrue(pode_publicar_pedido(self.hemocentro))

    def test_auditoria_distingue_validacao_e_publicacao(self):
        from .models import AuditoriaAcaoCritica
        self.client.force_login(self.receptor)
        self.client.post(reverse('accounts:pedido_publicar'), self.dados_validos())
        pedido = PedidoSangue.objects.get()
        marcar_pedido_suspeito(pedido=pedido, moderador=self.administrador)
        registro = AuditoriaAcaoCritica.objects.filter(alvo_tipo='accounts.PedidoSangue').latest('id_auditoria')
        self.assertEqual(registro.metadados['evento'], 'VALIDACAO_PEDIDO')
        self.assertEqual(registro.metadados['status_anterior'], PedidoSangue.Status.ENVIADA)
        self.assertEqual(registro.metadados['status_pedido'], PedidoSangue.Status.EM_ANALISE)
        aprovar_pedido(pedido=pedido, moderador=self.hemocentro)
        registro = AuditoriaAcaoCritica.objects.filter(alvo_tipo='accounts.PedidoSangue').latest('id_auditoria')
        self.assertEqual(registro.usuario, self.hemocentro)
        self.assertEqual(registro.metadados['evento'], 'PUBLICACAO_PEDIDO')
        self.assertEqual(registro.metadados['status_pedido'], PedidoSangue.Status.PUBLICADA)
        self.assertNotIn('Paciente de exemplo', str(registro.metadados))

    def test_tentativa_de_publicacao_alheia_persiste_na_auditoria(self):
        from .models import AuditoriaAcaoCritica
        self.client.force_login(self.receptor)
        self.client.post(reverse('accounts:pedido_publicar'), self.dados_validos())
        pedido = PedidoSangue.objects.get()
        self.hemocentro_pendente.status_validacao = Usuario.StatusValidacaoHemocentro.APROVADO
        self.hemocentro_pendente.save()
        self.client.force_login(self.hemocentro_pendente)
        resposta = self.client.post(reverse('accounts:aprovar_pedido', kwargs={'id_pedido': pedido.pk}))
        self.assertEqual(resposta.status_code, 403)
        registro = AuditoriaAcaoCritica.objects.filter(usuario=self.hemocentro_pendente).latest('id_auditoria')
        self.assertEqual(registro.resultado, AuditoriaAcaoCritica.Resultado.BLOQUEADO)
        pedido.refresh_from_db()
        self.assertEqual(pedido.status, PedidoSangue.Status.ENVIADA)
```

**Explicação deste trecho:**

**Linha 10 — ClassDef** (nível 0 do bloco).

Define a classe `PedidoSangueTests` herdando de `TestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 10:

**Linha 11 — FunctionDef** (nível 1 do bloco).

Define `criar_usuario(self, *, email, nome, perfil, cidade='', estado='')`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 11:

**Linha 12 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `Usuario.objects.create_user`; argumentos nomeados: `email=email`, `password='SenhaForte123!'`, `nome=nome`, `perfil=perfil`, `cidade=cidade`, `estado=estado` ao chamador.

**Linha 21 — FunctionDef** (nível 1 do bloco).

Define `setUp(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 21:

**Linha 22 — Assign** (nível 2 do bloco).

Associa `self.receptor` a a chamada `self.criar_usuario`; argumentos nomeados: `email='receptor@elo.test'`, `nome='Receptor Elo'`, `perfil=Usuario.Perfil.RECEPTOR`.

- `email='receptor@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Receptor Elo'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.RECEPTOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 27 — Assign** (nível 2 do bloco).

Associa `self.doador` a a chamada `self.criar_usuario`; argumentos nomeados: `email='doador@elo.test'`, `nome='Doador Elo'`, `perfil=Usuario.Perfil.DOADOR`.

- `email='doador@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Doador Elo'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.DOADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 32 — Assign** (nível 2 do bloco).

Associa `self.administrador` a a chamada `self.criar_usuario`; argumentos nomeados: `email='admin@elo.test'`, `nome='Administrador Elo'`, `perfil=Usuario.Perfil.ADMINISTRADOR`.

- `email='admin@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Administrador Elo'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.ADMINISTRADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 37 — Assign** (nível 2 do bloco).

Associa `self.hemocentro` a a chamada `self.criar_usuario`; argumentos nomeados: `email='hemocentro@elo.test'`, `nome='Hemocentro Muzambinho'`, `perfil=Usuario.Perfil.HEMOCENTRO`, `cidade='Muzambinho'`, `estado='MG'`.

- `email='hemocentro@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Hemocentro Muzambinho'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.HEMOCENTRO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `cidade='Muzambinho'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `estado='MG'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 44 — Expr** (nível 2 do bloco).

Executa a chamada `aprovar_hemocentro`; argumentos nomeados: `hemocentro=self.hemocentro`, `admin=self.administrador`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 48 — Expr** (nível 2 do bloco).

Executa a chamada `self.hemocentro.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 50 — Assign** (nível 2 do bloco).

Associa `self.hemocentro_pendente` a a chamada `self.criar_usuario`; argumentos nomeados: `email='pendente@elo.test'`, `nome='Hemocentro Pendente'`, `perfil=Usuario.Perfil.HEMOCENTRO`, `cidade='Alfenas'`, `estado='MG'`.

- `email='pendente@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Hemocentro Pendente'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.HEMOCENTRO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `cidade='Alfenas'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `estado='MG'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 58 — FunctionDef** (nível 1 do bloco).

Define `dados_validos(self, **alteracoes)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 58:

**Linha 59 — Assign** (nível 2 do bloco).

Associa `dados` a um dicionário de 12 entradas; as chaves dão nome aos valores associados.

- Chave `'nome_solicitante'`: recebe o valor literal `'Solicitante de exemplo'`.
- Chave `'contato'`: recebe o valor literal `'receptor@elo.test'`.
- Chave `'para_quem'`: recebe o atributo `OUTRA_PESSOA` de `PedidoSangue.ParaQuem`.
- Chave `'hemocentro_destino'`: recebe o atributo `pk` de `self.hemocentro`.
- Chave `'titulo'`: recebe o valor literal `'Doacao para paciente internado'`.
- Chave `'tipo_sanguineo'`: recebe o valor literal `'O-'`.
- Chave `'urgencia'`: recebe o atributo `BAIXA` de `PedidoSangue.Urgencia`.
- Chave `'cidade'`: recebe o valor literal `'Muzambinho'`.
- Chave `'nome_paciente'`: recebe o valor literal `'Paciente de exemplo'`.
- Chave `'descricao'`: recebe o valor literal `'Precisamos de doadores para auxiliar um paciente internado.'`.
- Chave `'justificativa_urgencia'`: recebe o valor literal `''`.
- Chave `'informacoes_complementares'`: recebe o valor literal `'Retorno por telefone.'`.

**Linha 75 — Expr** (nível 2 do bloco).

Executa a chamada `dados.update`, que no QuerySet grava diretamente os campos dos resultados, sem chamar save de cada instância; argumentos posicionais: `alteracoes`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 76 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `dados` ao chamador.

**Linha 78 — FunctionDef** (nível 1 do bloco).

Define `test_formulario_lista_apenas_hemocentros_aprovados(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: formulario lista apenas hemocentros aprovados.

Bloco `body` da linha 78:

**Linha 79 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `PedidoSangueForm`.


**Linha 81 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'para_quem'`, `form.fields`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 82 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'nome_paciente'`, `form.fields`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 83 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `list(form.fields['hemocentro_destino'].queryset)`, `[self.hemocentro]`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 88 — FunctionDef** (nível 1 do bloco).

Define `test_receptor_cria_solicitacao_enviada(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: receptor cria solicitacao enviada.

Bloco `body` da linha 88:

**Linha 89 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.receptor`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 91 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:pedido_publicar')`, `self.dados_validos()`.


**Linha 96 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:minhas_solicitacoes')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 97 — Assign** (nível 2 do bloco).

Associa `pedido` a a chamada `PedidoSangue.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave.


**Linha 98 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pedido.solicitante`, `self.receptor`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 99 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pedido.hemocentro_destino`, `self.hemocentro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 100 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pedido.status`, `PedidoSangue.Status.ENVIADA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 105 — FunctionDef** (nível 1 do bloco).

Define `test_doador_nao_pode_enviar_solicitacao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: doador nao pode enviar solicitacao.

Bloco `body` da linha 105:

**Linha 106 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.doador`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 107 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:pedido_publicar')`, `self.dados_validos()`.


**Linha 108 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:dashboard')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 109 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `PedidoSangue.objects.exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 111 — FunctionDef** (nível 1 do bloco).

Define `test_visitante_precisa_entrar(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: visitante precisa entrar.

Bloco `body` da linha 111:

**Linha 112 — Assign** (nível 2 do bloco).

Associa `url` a a chamada `reverse`, que resolve o endereço a partir do nome da rota; argumentos posicionais: `'accounts:pedido_publicar'`.


**Linha 113 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `url`.


**Linha 114 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `f"{reverse('accounts:login')}?next={url}"`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 116 — FunctionDef** (nível 1 do bloco).

Define `test_formulario_rejeita_descricao_curta(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: formulario rejeita descricao curta.

Bloco `body` da linha 116:

**Linha 117 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `PedidoSangueForm`; argumentos posicionais: `self.dados_validos(descricao='Curto')`.


**Linha 119 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `form.is_valid()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 120 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'descricao'`, `form.errors`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 122 — FunctionDef** (nível 1 do bloco).

Define `test_formulario_exige_email_no_contato(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: formulario exige email no contato.

Bloco `body` da linha 122:

**Linha 123 — Assign** (nível 2 do bloco).

Associa `form_invalido` a a chamada `PedidoSangueForm`; argumentos posicionais: `self.dados_validos(contato='(31) 99999-0000')`.


**Linha 126 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `form_invalido.is_valid()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 127 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'contato'`, `form_invalido.errors`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 129 — Assign** (nível 2 do bloco).

Associa `form_valido` a a chamada `PedidoSangueForm`; argumentos posicionais: `self.dados_validos(contato='  Receptor@Elo.Test ')`.


**Linha 132 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `form_valido.is_valid()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 133 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `form_valido.cleaned_data['contato']`, `'receptor@elo.test'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 138 — FunctionDef** (nível 1 do bloco).

Define `test_formulario_rejeita_hemocentro_pendente(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: formulario rejeita hemocentro pendente.

Bloco `body` da linha 138:

**Linha 139 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `PedidoSangueForm`; argumentos posicionais: `self.dados_validos(hemocentro_destino=self.hemocentro_pendente.pk)`.


**Linha 145 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `form.is_valid()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 146 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'hemocentro_destino'`, `form.errors`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 148 — FunctionDef** (nível 1 do bloco).

Define `test_urgencia_critica_exige_justificativa(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: urgencia critica exige justificativa.

Bloco `body` da linha 148:

**Linha 149 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `PedidoSangueForm`; argumentos posicionais: `self.dados_validos(urgencia=PedidoSangue.Urgencia.CRITICA, justificativa_urgencia='Curta')`.


**Linha 156 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `form.is_valid()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 157 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'justificativa_urgencia'`, `form.errors`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 159 — FunctionDef** (nível 1 do bloco).

Define `test_hemocentro_aprova_pedido_e_registra_historico(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: hemocentro aprova pedido e registra historico.

Bloco `body` da linha 159:

**Linha 160 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.receptor`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 161 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:pedido_publicar')`, `self.dados_validos()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 165 — Assign** (nível 2 do bloco).

Associa `pedido` a a chamada `PedidoSangue.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave.


**Linha 167 — Assign** (nível 2 do bloco).

Associa `validacao` a a chamada `aprovar_pedido`; argumentos nomeados: `pedido=pedido`, `moderador=self.hemocentro`, `motivo='Dados conferidos pelo administrador.'`.

- `pedido=pedido`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `moderador=self.hemocentro`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `motivo='Dados conferidos pelo administrador.'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 173 — Expr** (nível 2 do bloco).

Executa a chamada `pedido.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 174 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pedido.status`, `PedidoSangue.Status.PUBLICADA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 175 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `validacao.status_validacao`, `ValidacaoPedido.StatusValidacao.APROVADO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 179 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pedido.validacoes.count()`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 181 — FunctionDef** (nível 1 do bloco).

Define `test_admin_moderar_pedido_nao_publica(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: admin moderar pedido nao publica.

Bloco `body` da linha 181:

**Linha 182 — Assign** (nível 2 do bloco).

Associa `pedido` a a chamada `criar_pedido_pendente`; argumentos nomeados: `dados=self.dados_validos()`, `solicitante=self.receptor`.

- `dados=self.dados_validos()`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `solicitante=self.receptor`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 187 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.administrador`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 189 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:painel_validacao_pedidos')`.


**Linha 193 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `200`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 194 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `str(pedido.pk)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 196 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:marcar_pedido_suspeito', kwargs={'id_pedido': pedido.pk})`, `{'motivo': 'Há solicitação semelhante para o mesmo destino.'}`.


**Linha 204 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:painel_validacao_pedidos')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 208 — Expr** (nível 2 do bloco).

Executa a chamada `pedido.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 209 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pedido.status`, `PedidoSangue.Status.EM_ANALISE`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 213 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `pedido.publicado_por_id`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 214 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pedido.validacoes.latest('data_validacao').status_validacao`, `ValidacaoPedido.StatusValidacao.SUSPEITO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 219 — FunctionDef** (nível 1 do bloco).

Define `test_hemocentro_nao_acessa_moderacao_administrativa(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: hemocentro nao acessa moderacao administrativa.

Bloco `body` da linha 219:

**Linha 220 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.hemocentro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 222 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:painel_validacao_pedidos')`.


**Linha 226 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `403`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 228 — FunctionDef** (nível 1 do bloco).

Define `test_publicacao_exclusiva_do_hemocentro_responsavel(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: publicacao exclusiva do hemocentro responsavel.

Bloco `body` da linha 228:

**Linha 229 — ImportFrom** (nível 2 do bloco).

Importa de `django.core.exceptions` os nomes `PermissionDenied`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 230 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.receptor`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 231 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:pedido_publicar')`, `self.dados_validos()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 232 — Assign** (nível 2 do bloco).

Associa `pedido` a a chamada `PedidoSangue.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave.


**Linha 233 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.hemocentro_pendente`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 234 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.client.get(reverse('accounts:painel_pedidos_hemocentro')).status_code`, `403`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 235 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(PermissionDenied)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 235:

**Linha 236 — Expr** (nível 3 do bloco).

Executa a chamada `aprovar_pedido`; argumentos nomeados: `pedido=pedido`, `moderador=self.hemocentro_pendente`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 237 — Assign** (nível 2 do bloco).

Associa `self.hemocentro_pendente.status_validacao` a o atributo `APROVADO` de `Usuario.StatusValidacaoHemocentro`.

**Linha 238 — Expr** (nível 2 do bloco).

Executa a chamada `self.hemocentro_pendente.save`, que persiste a instância; update_fields limita os campos gravados. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 239 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(PermissionDenied)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 239:

**Linha 240 — Expr** (nível 3 do bloco).

Executa a chamada `aprovar_pedido`; argumentos nomeados: `pedido=pedido`, `moderador=self.hemocentro_pendente`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 241 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotContains`, que o teste exige ausência de texto na resposta HTTP; argumentos posicionais: `self.client.get(reverse('accounts:painel_pedidos_hemocentro'))`, `pedido.titulo`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 242 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.hemocentro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 243 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `self.client.get(reverse('accounts:painel_pedidos_hemocentro'))`, `pedido.titulo`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 244 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:aprovar_pedido', kwargs={'id_pedido': pedido.pk})`.


**Linha 245 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `302`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 246 — Expr** (nível 2 do bloco).

Executa a chamada `pedido.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 247 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pedido.status`, `PedidoSangue.Status.PUBLICADA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 249 — FunctionDef** (nível 1 do bloco).

Define `test_permissao_do_servico_de_publicacao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: permissao do servico de publicacao.

Bloco `body` da linha 249:

**Linha 250 — ImportFrom** (nível 2 do bloco).

Importa de `.pedidos` os nomes `pode_publicar_pedido`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 251 — For** (nível 2 do bloco).

Percorre `(self.receptor, self.doador, self.administrador, self.hemocentro_pendente)`; cada item é atribuído a `usuario` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 251:

**Linha 252 — With** (nível 3 do bloco).

Executa sob os contextos `self.subTest(perfil=usuario.perfil)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 252:

**Linha 253 — Expr** (nível 4 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `pode_publicar_pedido(usuario)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 254 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `pode_publicar_pedido(self.hemocentro)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 256 — FunctionDef** (nível 1 do bloco).

Define `test_auditoria_distingue_validacao_e_publicacao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: auditoria distingue validacao e publicacao.

Bloco `body` da linha 256:

**Linha 257 — ImportFrom** (nível 2 do bloco).

Importa de `.models` os nomes `AuditoriaAcaoCritica`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 258 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.receptor`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 259 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:pedido_publicar')`, `self.dados_validos()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 260 — Assign** (nível 2 do bloco).

Associa `pedido` a a chamada `PedidoSangue.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave.


**Linha 261 — Expr** (nível 2 do bloco).

Executa a chamada `marcar_pedido_suspeito`; argumentos nomeados: `pedido=pedido`, `moderador=self.administrador`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 262 — Assign** (nível 2 do bloco).

Associa `registro` a a chamada `AuditoriaAcaoCritica.objects.filter(alvo_tipo='accounts.PedidoSangue').latest`; argumentos posicionais: `'id_auditoria'`.


**Linha 263 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.metadados['evento']`, `'VALIDACAO_PEDIDO'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 264 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.metadados['status_anterior']`, `PedidoSangue.Status.ENVIADA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 265 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.metadados['status_pedido']`, `PedidoSangue.Status.EM_ANALISE`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 266 — Expr** (nível 2 do bloco).

Executa a chamada `aprovar_pedido`; argumentos nomeados: `pedido=pedido`, `moderador=self.hemocentro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 267 — Assign** (nível 2 do bloco).

Associa `registro` a a chamada `AuditoriaAcaoCritica.objects.filter(alvo_tipo='accounts.PedidoSangue').latest`; argumentos posicionais: `'id_auditoria'`.


**Linha 268 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.usuario`, `self.hemocentro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 269 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.metadados['evento']`, `'PUBLICACAO_PEDIDO'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 270 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.metadados['status_pedido']`, `PedidoSangue.Status.PUBLICADA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 271 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotIn`; argumentos posicionais: `'Paciente de exemplo'`, `str(registro.metadados)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 273 — FunctionDef** (nível 1 do bloco).

Define `test_tentativa_de_publicacao_alheia_persiste_na_auditoria(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: tentativa de publicacao alheia persiste na auditoria.

Bloco `body` da linha 273:

**Linha 274 — ImportFrom** (nível 2 do bloco).

Importa de `.models` os nomes `AuditoriaAcaoCritica`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 275 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.receptor`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 276 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:pedido_publicar')`, `self.dados_validos()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 277 — Assign** (nível 2 do bloco).

Associa `pedido` a a chamada `PedidoSangue.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave.


**Linha 278 — Assign** (nível 2 do bloco).

Associa `self.hemocentro_pendente.status_validacao` a o atributo `APROVADO` de `Usuario.StatusValidacaoHemocentro`.

**Linha 279 — Expr** (nível 2 do bloco).

Executa a chamada `self.hemocentro_pendente.save`, que persiste a instância; update_fields limita os campos gravados. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 280 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.hemocentro_pendente`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 281 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:aprovar_pedido', kwargs={'id_pedido': pedido.pk})`.


**Linha 282 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `403`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 283 — Assign** (nível 2 do bloco).

Associa `registro` a a chamada `AuditoriaAcaoCritica.objects.filter(usuario=self.hemocentro_pendente).latest`; argumentos posicionais: `'id_auditoria'`.


**Linha 284 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.resultado`, `AuditoriaAcaoCritica.Resultado.BLOQUEADO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 285 — Expr** (nível 2 do bloco).

Executa a chamada `pedido.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 286 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pedido.status`, `PedidoSangue.Status.ENVIADA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

