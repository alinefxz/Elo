# accounts/test_triagem_views.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

**Arquivo original:** [accounts/test_triagem_views.py](<C:/Users/lb119/Elo/accounts/test_triagem_views.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
"""
Testes automatizados das páginas e dos fluxos da triagem.

Verificam o acesso público e privado, as permissões dos perfis,
o início da triagem, o consentimento, o salvamento e a edição
das respostas, a privacidade do histórico, a conclusão da triagem
e o encaminhamento da versão simplificada para a extensa quando
as respostas indicam que o histórico anterior não é confiável.
"""

from django.test import TestCase
from django.urls import reverse

from .models import RespostaTriagem, Triagem, Usuario
from .triagem_catalogo import obter_pergunta


class TriagemViewsTests(TestCase):
    """Protege navegação, permissões e privacidade do histórico."""

    @classmethod
    def setUpTestData(cls):
        cls.doador = Usuario.objects.create_user(
            email="doador.views@teste.com",
            password="SenhaForte123!",
            nome="Doador Views",
            perfil=Usuario.Perfil.DOADOR,
        )
        cls.receptor = Usuario.objects.create_user(
            email="receptor.views@teste.com",
            password="SenhaForte123!",
            nome="Receptor Views",
            perfil=Usuario.Perfil.RECEPTOR,
        )
        cls.observador = Usuario.objects.create_user(
            email="observador.views@teste.com",
            password="SenhaForte123!",
            nome="Observador Views",
            perfil=Usuario.Perfil.OBSERVADOR,
        )

    def _criar_extensa_concluida(self, usuario=None):
        """Cria somente o pré-requisito necessário para a versão rápida."""

        return Triagem.objects.create(
            usuario=usuario or self.doador,
            modalidade=Triagem.Modalidade.EXTENSA,
            status=Triagem.Status.CONCLUIDA,
            resultado=Triagem.Resultado.SEM_IMPEDIMENTO,
        )

    def _iniciar_pela_rota(self, modalidade="extensa", usuario=None):
        """Autentica e inicia uma modalidade usando a mesma rota da página."""

        self.client.force_login(usuario or self.doador)
        return self.client.post(
            reverse(
                "accounts:triagem_iniciar",
                kwargs={"modalidade": modalidade},
            ),
            {"aceite_termo": "on"},
        )

    def _preencher_ate_confirmacao(self, triagem):
        """Preenche respostas neutras para testar a conclusão pela view."""

        preferencias = (
            "NAO", "NAO_SEI", "NENHUMA", "NENHUM", "NUNCA", "SIM", "18_60",
            "56_129_9", "MASCULINO", "ORIGINAL", "DESCANSADO",
            "LEVE", "NAO_MEDI",
        )
        for id_pergunta in triagem.fluxo_perguntas[:-1]:
            pergunta = obter_pergunta(id_pergunta)
            opcoes = {
                opcao["codigo"]: opcao["rotulo"]
                for opcao in pergunta["opcoes"]
            }
            codigo = (
                "SIM"
                if id_pergunta in {"EXT-01", "EXT-08", "EXT-11"}
                else next(item for item in preferencias if item in opcoes)
            )
            RespostaTriagem.objects.create(
                triagem=triagem,
                id_pergunta=id_pergunta,
                codigo_resposta=codigo,
                resposta_label=opcoes[codigo],
                valor={"codigos": [codigo], "datas": {}, "detalhes": ""},
                rule_version=pergunta["regra_version"],
                source_ref=pergunta["fonte"],
            )
        triagem.pergunta_atual = len(triagem.fluxo_perguntas) - 1
        triagem.save(update_fields=["pergunta_atual"])

    def test_apresentacao_publica_mostra_texto_e_duas_modalidades(self):
        """Falha se o visitante não conhecer as opções antes de se cadastrar."""

        resposta = self.client.get(reverse("accounts:triagem_apresentacao"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Seu gesto de cuidado começa aqui.")
        self.assertContains(resposta, "Triagem extensa")
        self.assertContains(resposta, "Triagem simplificada")
        self.assertContains(resposta, "Quem dará a resposta final será sempre")
        self.assertContains(resposta, "Criar conta")

    def test_visitante_ve_botoes_de_acao_na_apresentacao(self):
        """Falha se a apresentação não oferecer ações visíveis ao visitante."""

        resposta = self.client.get(reverse("accounts:triagem_apresentacao"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Criar conta para iniciar a triagem extensa")
        self.assertContains(resposta, "Entrar para continuar uma triagem")

    def test_inicio_exige_post_e_login(self):
        """Falha se uma simples visita à URL criar registro no banco."""

        url = reverse(
            "accounts:triagem_iniciar",
            kwargs={"modalidade": "extensa"},
        )

        resposta = self.client.post(url)
        self.assertEqual(resposta.status_code, 302)
        self.assertIn(reverse("accounts:login"), resposta.url)

        # Depois de autenticado, GET continua proibido: iniciar exige clique no
        # formulário POST da apresentação.
        self.client.force_login(self.doador)
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(Triagem.objects.count(), 0)

    def test_doador_pode_iniciar_extensa(self):
        """Falha se um dos dois perfis autorizados não puder responder."""

        for usuario in (self.doador,):
            with self.subTest(perfil=usuario.perfil):
                resposta = self._iniciar_pela_rota(usuario=usuario)
                triagem = Triagem.objects.get(usuario=usuario)
                self.assertRedirects(
                    resposta,
                    reverse(
                        "accounts:triagem_pergunta",
                        kwargs={"id_triagem": triagem.pk},
                    ),
                )

    def test_apresentacao_oferece_reutilizar_extensa_concluida(self):
        """A apresentação oferece o preenchimento a partir do histórico."""

        self._criar_extensa_concluida()
        self.client.force_login(self.doador)

        resposta = self.client.get(reverse("accounts:triagem_apresentacao"))

        self.assertContains(
            resposta,
            "Reutilizar respostas da última triagem extensa concluída.",
        )

    def test_observador_nao_pode_iniciar(self):
        """Falha se um perfil não autorizado puder gravar dados de saúde."""

        resposta = self._iniciar_pela_rota(usuario=self.observador)

        self.assertEqual(resposta.status_code, 403)
        self.assertFalse(Triagem.objects.filter(usuario=self.observador).exists())

    def test_simplificada_exige_extensa_anterior(self):
        """Falha se a versão rápida for iniciada sem histórico completo."""

        resposta = self._iniciar_pela_rota("simplificada")

        self.assertRedirects(
            resposta,
            reverse("accounts:triagem_apresentacao"),
        )
        self.assertFalse(
            Triagem.objects.filter(
                usuario=self.doador,
                modalidade=Triagem.Modalidade.SIMPLIFICADA,
            ).exists()
        )

    def test_pagina_mostra_uma_pergunta_e_salva_resposta(self):
        """Falha se a tela não avançar uma pergunta por vez."""

        self._iniciar_pela_rota()
        triagem = Triagem.objects.get(usuario=self.doador)
        url = reverse(
            "accounts:triagem_pergunta",
            kwargs={"id_triagem": triagem.pk},
        )

        resposta_get = self.client.get(url)
        self.assertContains(resposta_get, "Você entende que esta pré-triagem")
        self.assertContains(resposta_get, "Pergunta 1 de")

        resposta_post = self.client.post(
            url,
            {"resposta": "SIM", "acao": "continuar"},
        )
        self.assertRedirects(resposta_post, url)
        triagem.refresh_from_db()
        self.assertEqual(triagem.pergunta_atual, 1)
        self.assertTrue(
            RespostaTriagem.objects.filter(
                triagem=triagem,
                id_pergunta="EXT-01",
            ).exists()
        )

    def test_salvar_e_sair_conserva_andamento(self):
        """Falha se a pessoa perder a resposta ao pausar a triagem."""

        self._iniciar_pela_rota()
        triagem = Triagem.objects.get(usuario=self.doador)
        url = reverse(
            "accounts:triagem_pergunta",
            kwargs={"id_triagem": triagem.pk},
        )

        resposta = self.client.post(
            url,
            {"resposta": "SIM", "acao": "salvar"},
        )

        self.assertRedirects(resposta, reverse("accounts:triagem_historico"))
        triagem.refresh_from_db()
        self.assertEqual(triagem.status, Triagem.Status.EM_ANDAMENTO)
        self.assertEqual(triagem.pergunta_atual, 1)

    def test_botao_anterior_retorna_sem_apagar_resposta(self):
        """Falha se voltar apagar informação já salva."""

        self._iniciar_pela_rota()
        triagem = Triagem.objects.get(usuario=self.doador)
        url = reverse(
            "accounts:triagem_pergunta",
            kwargs={"id_triagem": triagem.pk},
        )
        self.client.post(url, {"resposta": "SIM", "acao": "continuar"})

        resposta = self.client.post(url, {"acao": "anterior"})

        self.assertRedirects(resposta, url)
        triagem.refresh_from_db()
        self.assertEqual(triagem.pergunta_atual, 0)
        self.assertTrue(triagem.respostas.filter(id_pergunta="EXT-01").exists())

    def test_triagem_de_outro_usuario_retorna_404(self):
        """Falha se respostas de saúde puderem ser acessadas por outra conta."""

        triagem = Triagem.objects.create(
            usuario=self.receptor,
            modalidade=Triagem.Modalidade.EXTENSA,
        )
        self.client.force_login(self.doador)

        pergunta = self.client.get(
            reverse(
                "accounts:triagem_pergunta",
                kwargs={"id_triagem": triagem.pk},
            )
        )
        resultado = self.client.get(
            reverse(
                "accounts:triagem_resultado",
                kwargs={"id_triagem": triagem.pk},
            )
        )

        self.assertEqual(pergunta.status_code, 404)
        self.assertEqual(resultado.status_code, 404)

    def test_resultado_em_andamento_volta_para_pergunta(self):
        """Falha se um resultado vazio for mostrado antes da confirmação."""

        self._iniciar_pela_rota()
        triagem = Triagem.objects.get(usuario=self.doador)

        resposta = self.client.get(
            reverse(
                "accounts:triagem_resultado",
                kwargs={"id_triagem": triagem.pk},
            )
        )

        self.assertRedirects(
            resposta,
            reverse("accounts:triagem_revisao", kwargs={"id_triagem": triagem.pk}),
        )

    def test_confirmacao_final_conclui_e_mostra_resultado(self):
        """Falha se a última resposta não congelar a orientação calculada."""

        self._iniciar_pela_rota()
        triagem = Triagem.objects.get(usuario=self.doador)
        self._preencher_ate_confirmacao(triagem)
        url = reverse(
            "accounts:triagem_pergunta",
            kwargs={"id_triagem": triagem.pk},
        )

        resposta = self.client.post(
            url,
            {"resposta": "CONFIRMAR", "acao": "continuar"},
        )

        self.assertRedirects(
            resposta,
            reverse("accounts:triagem_revisao", kwargs={"id_triagem": triagem.pk}),
        )
        triagem.refresh_from_db()
        self.assertEqual(triagem.status, Triagem.Status.EM_ANDAMENTO)

        resposta_final = self.client.post(
            reverse("accounts:triagem_revisao", kwargs={"id_triagem": triagem.pk}),
            {"acao": "finalizar"},
        )
        self.assertRedirects(
            resposta_final,
            reverse("accounts:triagem_resultado", kwargs={"id_triagem": triagem.pk}),
        )
        triagem.refresh_from_db()
        self.assertEqual(triagem.status, Triagem.Status.CONCLUIDA)

    def test_resumo_incorreto_abre_nova_extensa(self):
        """Falha se a rápida continuar usando um histórico declarado incorreto."""

        self._criar_extensa_concluida()
        self._iniciar_pela_rota("simplificada")
        simplificada = Triagem.objects.get(
            usuario=self.doador,
            modalidade=Triagem.Modalidade.SIMPLIFICADA,
        )
        url = reverse(
            "accounts:triagem_pergunta",
            kwargs={"id_triagem": simplificada.pk},
        )

        resposta = self.client.post(
            url,
            {"resposta": "INCORRETO", "acao": "continuar"},
        )

        simplificada.refresh_from_db()
        nova_extensa = Triagem.objects.get(
            usuario=self.doador,
            modalidade=Triagem.Modalidade.EXTENSA,
            status=Triagem.Status.EM_ANDAMENTO,
        )
        self.assertEqual(simplificada.status, Triagem.Status.CANCELADA)
        self.assertRedirects(
            resposta,
            reverse(
                "accounts:triagem_pergunta",
                kwargs={"id_triagem": nova_extensa.pk},
            ),
        )

    def test_historico_lista_somente_triagens_do_usuario(self):
        """Falha se o histórico revelar registros de outra pessoa."""

        propria = self._criar_extensa_concluida(self.doador)
        alheia = self._criar_extensa_concluida(self.receptor)
        self.client.force_login(self.doador)

        resposta = self.client.get(reverse("accounts:triagem_historico"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, f"Triagem {propria.pk}")
        self.assertNotContains(resposta, f"Triagem {alheia.pk}")

    def test_dashboard_doador_aponta_para_triagem(self):
        """Falha se um perfil autorizado não encontrar a triagem no painel."""

        for usuario in (self.doador,):
            with self.subTest(perfil=usuario.perfil):
                self.client.force_login(usuario)
                resposta = self.client.get(reverse("accounts:dashboard"))
                self.assertContains(resposta, "Triagem para doação")
                self.assertContains(
                    resposta,
                    reverse("accounts:triagem_apresentacao"),
                )

    def test_receptor_bloqueado_inclusive_triagem_antiga(self):
        self.client.force_login(self.receptor)
        triagem = self._criar_extensa_concluida(self.receptor)
        for rota in ('triagem_pergunta', 'triagem_resultado'):
            resposta = self.client.get(reverse('accounts:' + rota, kwargs={'id_triagem': triagem.pk}))
            self.assertEqual(resposta.status_code, 403)
        self.assertEqual(self._iniciar_pela_rota(usuario=self.receptor).status_code, 403)
        self.assertNotContains(self.client.get(reverse('accounts:dashboard')), 'Triagem para doação')
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 9

```python
"""
Testes automatizados das páginas e dos fluxos da triagem.

Verificam o acesso público e privado, as permissões dos perfis,
o início da triagem, o consentimento, o salvamento e a edição
das respostas, a privacidade do histórico, a conclusão da triagem
e o encaminhamento da versão simplificada para a extensa quando
as respostas indicam que o histórico anterior não é confiável.
"""
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 11 a 11

```python
from django.test import TestCase
```

**Explicação deste trecho:**

**Linha 11 — ImportFrom** (nível 0 do bloco).

Importa de `django.test` os nomes `TestCase`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 12 a 12

```python
from django.urls import reverse
```

**Explicação deste trecho:**

**Linha 12 — ImportFrom** (nível 0 do bloco).

Importa de `django.urls` os nomes `reverse`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 14 a 14

```python
from .models import RespostaTriagem, Triagem, Usuario
```

**Explicação deste trecho:**

**Linha 14 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `RespostaTriagem`, `Triagem`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 15 a 15

```python
from .triagem_catalogo import obter_pergunta
```

**Explicação deste trecho:**

**Linha 15 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_catalogo` os nomes `obter_pergunta`. Pontos iniciais indicam importação relativa ao pacote.

### TriagemViewsTests — linhas 18 a 396

```python
class TriagemViewsTests(TestCase):
    """Protege navegação, permissões e privacidade do histórico."""

    @classmethod
    def setUpTestData(cls):
        cls.doador = Usuario.objects.create_user(
            email="doador.views@teste.com",
            password="SenhaForte123!",
            nome="Doador Views",
            perfil=Usuario.Perfil.DOADOR,
        )
        cls.receptor = Usuario.objects.create_user(
            email="receptor.views@teste.com",
            password="SenhaForte123!",
            nome="Receptor Views",
            perfil=Usuario.Perfil.RECEPTOR,
        )
        cls.observador = Usuario.objects.create_user(
            email="observador.views@teste.com",
            password="SenhaForte123!",
            nome="Observador Views",
            perfil=Usuario.Perfil.OBSERVADOR,
        )

    def _criar_extensa_concluida(self, usuario=None):
        """Cria somente o pré-requisito necessário para a versão rápida."""

        return Triagem.objects.create(
            usuario=usuario or self.doador,
            modalidade=Triagem.Modalidade.EXTENSA,
            status=Triagem.Status.CONCLUIDA,
            resultado=Triagem.Resultado.SEM_IMPEDIMENTO,
        )

    def _iniciar_pela_rota(self, modalidade="extensa", usuario=None):
        """Autentica e inicia uma modalidade usando a mesma rota da página."""

        self.client.force_login(usuario or self.doador)
        return self.client.post(
            reverse(
                "accounts:triagem_iniciar",
                kwargs={"modalidade": modalidade},
            ),
            {"aceite_termo": "on"},
        )

    def _preencher_ate_confirmacao(self, triagem):
        """Preenche respostas neutras para testar a conclusão pela view."""

        preferencias = (
            "NAO", "NAO_SEI", "NENHUMA", "NENHUM", "NUNCA", "SIM", "18_60",
            "56_129_9", "MASCULINO", "ORIGINAL", "DESCANSADO",
            "LEVE", "NAO_MEDI",
        )
        for id_pergunta in triagem.fluxo_perguntas[:-1]:
            pergunta = obter_pergunta(id_pergunta)
            opcoes = {
                opcao["codigo"]: opcao["rotulo"]
                for opcao in pergunta["opcoes"]
            }
            codigo = (
                "SIM"
                if id_pergunta in {"EXT-01", "EXT-08", "EXT-11"}
                else next(item for item in preferencias if item in opcoes)
            )
            RespostaTriagem.objects.create(
                triagem=triagem,
                id_pergunta=id_pergunta,
                codigo_resposta=codigo,
                resposta_label=opcoes[codigo],
                valor={"codigos": [codigo], "datas": {}, "detalhes": ""},
                rule_version=pergunta["regra_version"],
                source_ref=pergunta["fonte"],
            )
        triagem.pergunta_atual = len(triagem.fluxo_perguntas) - 1
        triagem.save(update_fields=["pergunta_atual"])

    def test_apresentacao_publica_mostra_texto_e_duas_modalidades(self):
        """Falha se o visitante não conhecer as opções antes de se cadastrar."""

        resposta = self.client.get(reverse("accounts:triagem_apresentacao"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Seu gesto de cuidado começa aqui.")
        self.assertContains(resposta, "Triagem extensa")
        self.assertContains(resposta, "Triagem simplificada")
        self.assertContains(resposta, "Quem dará a resposta final será sempre")
        self.assertContains(resposta, "Criar conta")

    def test_visitante_ve_botoes_de_acao_na_apresentacao(self):
        """Falha se a apresentação não oferecer ações visíveis ao visitante."""

        resposta = self.client.get(reverse("accounts:triagem_apresentacao"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Criar conta para iniciar a triagem extensa")
        self.assertContains(resposta, "Entrar para continuar uma triagem")

    def test_inicio_exige_post_e_login(self):
        """Falha se uma simples visita à URL criar registro no banco."""

        url = reverse(
            "accounts:triagem_iniciar",
            kwargs={"modalidade": "extensa"},
        )

        resposta = self.client.post(url)
        self.assertEqual(resposta.status_code, 302)
        self.assertIn(reverse("accounts:login"), resposta.url)

        # Depois de autenticado, GET continua proibido: iniciar exige clique no
        # formulário POST da apresentação.
        self.client.force_login(self.doador)
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(Triagem.objects.count(), 0)

    def test_doador_pode_iniciar_extensa(self):
        """Falha se um dos dois perfis autorizados não puder responder."""

        for usuario in (self.doador,):
            with self.subTest(perfil=usuario.perfil):
                resposta = self._iniciar_pela_rota(usuario=usuario)
                triagem = Triagem.objects.get(usuario=usuario)
                self.assertRedirects(
                    resposta,
                    reverse(
                        "accounts:triagem_pergunta",
                        kwargs={"id_triagem": triagem.pk},
                    ),
                )

    def test_apresentacao_oferece_reutilizar_extensa_concluida(self):
        """A apresentação oferece o preenchimento a partir do histórico."""

        self._criar_extensa_concluida()
        self.client.force_login(self.doador)

        resposta = self.client.get(reverse("accounts:triagem_apresentacao"))

        self.assertContains(
            resposta,
            "Reutilizar respostas da última triagem extensa concluída.",
        )

    def test_observador_nao_pode_iniciar(self):
        """Falha se um perfil não autorizado puder gravar dados de saúde."""

        resposta = self._iniciar_pela_rota(usuario=self.observador)

        self.assertEqual(resposta.status_code, 403)
        self.assertFalse(Triagem.objects.filter(usuario=self.observador).exists())

    def test_simplificada_exige_extensa_anterior(self):
        """Falha se a versão rápida for iniciada sem histórico completo."""

        resposta = self._iniciar_pela_rota("simplificada")

        self.assertRedirects(
            resposta,
            reverse("accounts:triagem_apresentacao"),
        )
        self.assertFalse(
            Triagem.objects.filter(
                usuario=self.doador,
                modalidade=Triagem.Modalidade.SIMPLIFICADA,
            ).exists()
        )

    def test_pagina_mostra_uma_pergunta_e_salva_resposta(self):
        """Falha se a tela não avançar uma pergunta por vez."""

        self._iniciar_pela_rota()
        triagem = Triagem.objects.get(usuario=self.doador)
        url = reverse(
            "accounts:triagem_pergunta",
            kwargs={"id_triagem": triagem.pk},
        )

        resposta_get = self.client.get(url)
        self.assertContains(resposta_get, "Você entende que esta pré-triagem")
        self.assertContains(resposta_get, "Pergunta 1 de")

        resposta_post = self.client.post(
            url,
            {"resposta": "SIM", "acao": "continuar"},
        )
        self.assertRedirects(resposta_post, url)
        triagem.refresh_from_db()
        self.assertEqual(triagem.pergunta_atual, 1)
        self.assertTrue(
            RespostaTriagem.objects.filter(
                triagem=triagem,
                id_pergunta="EXT-01",
            ).exists()
        )

    def test_salvar_e_sair_conserva_andamento(self):
        """Falha se a pessoa perder a resposta ao pausar a triagem."""

        self._iniciar_pela_rota()
        triagem = Triagem.objects.get(usuario=self.doador)
        url = reverse(
            "accounts:triagem_pergunta",
            kwargs={"id_triagem": triagem.pk},
        )

        resposta = self.client.post(
            url,
            {"resposta": "SIM", "acao": "salvar"},
        )

        self.assertRedirects(resposta, reverse("accounts:triagem_historico"))
        triagem.refresh_from_db()
        self.assertEqual(triagem.status, Triagem.Status.EM_ANDAMENTO)
        self.assertEqual(triagem.pergunta_atual, 1)

    def test_botao_anterior_retorna_sem_apagar_resposta(self):
        """Falha se voltar apagar informação já salva."""

        self._iniciar_pela_rota()
        triagem = Triagem.objects.get(usuario=self.doador)
        url = reverse(
            "accounts:triagem_pergunta",
            kwargs={"id_triagem": triagem.pk},
        )
        self.client.post(url, {"resposta": "SIM", "acao": "continuar"})

        resposta = self.client.post(url, {"acao": "anterior"})

        self.assertRedirects(resposta, url)
        triagem.refresh_from_db()
        self.assertEqual(triagem.pergunta_atual, 0)
        self.assertTrue(triagem.respostas.filter(id_pergunta="EXT-01").exists())

    def test_triagem_de_outro_usuario_retorna_404(self):
        """Falha se respostas de saúde puderem ser acessadas por outra conta."""

        triagem = Triagem.objects.create(
            usuario=self.receptor,
            modalidade=Triagem.Modalidade.EXTENSA,
        )
        self.client.force_login(self.doador)

        pergunta = self.client.get(
            reverse(
                "accounts:triagem_pergunta",
                kwargs={"id_triagem": triagem.pk},
            )
        )
        resultado = self.client.get(
            reverse(
                "accounts:triagem_resultado",
                kwargs={"id_triagem": triagem.pk},
            )
        )

        self.assertEqual(pergunta.status_code, 404)
        self.assertEqual(resultado.status_code, 404)

    def test_resultado_em_andamento_volta_para_pergunta(self):
        """Falha se um resultado vazio for mostrado antes da confirmação."""

        self._iniciar_pela_rota()
        triagem = Triagem.objects.get(usuario=self.doador)

        resposta = self.client.get(
            reverse(
                "accounts:triagem_resultado",
                kwargs={"id_triagem": triagem.pk},
            )
        )

        self.assertRedirects(
            resposta,
            reverse("accounts:triagem_revisao", kwargs={"id_triagem": triagem.pk}),
        )

    def test_confirmacao_final_conclui_e_mostra_resultado(self):
        """Falha se a última resposta não congelar a orientação calculada."""

        self._iniciar_pela_rota()
        triagem = Triagem.objects.get(usuario=self.doador)
        self._preencher_ate_confirmacao(triagem)
        url = reverse(
            "accounts:triagem_pergunta",
            kwargs={"id_triagem": triagem.pk},
        )

        resposta = self.client.post(
            url,
            {"resposta": "CONFIRMAR", "acao": "continuar"},
        )

        self.assertRedirects(
            resposta,
            reverse("accounts:triagem_revisao", kwargs={"id_triagem": triagem.pk}),
        )
        triagem.refresh_from_db()
        self.assertEqual(triagem.status, Triagem.Status.EM_ANDAMENTO)

        resposta_final = self.client.post(
            reverse("accounts:triagem_revisao", kwargs={"id_triagem": triagem.pk}),
            {"acao": "finalizar"},
        )
        self.assertRedirects(
            resposta_final,
            reverse("accounts:triagem_resultado", kwargs={"id_triagem": triagem.pk}),
        )
        triagem.refresh_from_db()
        self.assertEqual(triagem.status, Triagem.Status.CONCLUIDA)

    def test_resumo_incorreto_abre_nova_extensa(self):
        """Falha se a rápida continuar usando um histórico declarado incorreto."""

        self._criar_extensa_concluida()
        self._iniciar_pela_rota("simplificada")
        simplificada = Triagem.objects.get(
            usuario=self.doador,
            modalidade=Triagem.Modalidade.SIMPLIFICADA,
        )
        url = reverse(
            "accounts:triagem_pergunta",
            kwargs={"id_triagem": simplificada.pk},
        )

        resposta = self.client.post(
            url,
            {"resposta": "INCORRETO", "acao": "continuar"},
        )

        simplificada.refresh_from_db()
        nova_extensa = Triagem.objects.get(
            usuario=self.doador,
            modalidade=Triagem.Modalidade.EXTENSA,
            status=Triagem.Status.EM_ANDAMENTO,
        )
        self.assertEqual(simplificada.status, Triagem.Status.CANCELADA)
        self.assertRedirects(
            resposta,
            reverse(
                "accounts:triagem_pergunta",
                kwargs={"id_triagem": nova_extensa.pk},
            ),
        )

    def test_historico_lista_somente_triagens_do_usuario(self):
        """Falha se o histórico revelar registros de outra pessoa."""

        propria = self._criar_extensa_concluida(self.doador)
        alheia = self._criar_extensa_concluida(self.receptor)
        self.client.force_login(self.doador)

        resposta = self.client.get(reverse("accounts:triagem_historico"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, f"Triagem {propria.pk}")
        self.assertNotContains(resposta, f"Triagem {alheia.pk}")

    def test_dashboard_doador_aponta_para_triagem(self):
        """Falha se um perfil autorizado não encontrar a triagem no painel."""

        for usuario in (self.doador,):
            with self.subTest(perfil=usuario.perfil):
                self.client.force_login(usuario)
                resposta = self.client.get(reverse("accounts:dashboard"))
                self.assertContains(resposta, "Triagem para doação")
                self.assertContains(
                    resposta,
                    reverse("accounts:triagem_apresentacao"),
                )

    def test_receptor_bloqueado_inclusive_triagem_antiga(self):
        self.client.force_login(self.receptor)
        triagem = self._criar_extensa_concluida(self.receptor)
        for rota in ('triagem_pergunta', 'triagem_resultado'):
            resposta = self.client.get(reverse('accounts:' + rota, kwargs={'id_triagem': triagem.pk}))
            self.assertEqual(resposta.status_code, 403)
        self.assertEqual(self._iniciar_pela_rota(usuario=self.receptor).status_code, 403)
        self.assertNotContains(self.client.get(reverse('accounts:dashboard')), 'Triagem para doação')
```

**Explicação deste trecho:**

**Linha 18 — ClassDef** (nível 0 do bloco).

Define a classe `TriagemViewsTests` herdando de `TestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 18:

**Linha 19 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 22 — FunctionDef** (nível 1 do bloco).

Define `setUpTestData(cls)`. O corpo só executa quando a função/método é chamado. Decoradores: `classmethod`.

Bloco `body` da linha 22:

**Linha 23 — Assign** (nível 2 do bloco).

Associa `cls.doador` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email='doador.views@teste.com'`, `password='SenhaForte123!'`, `nome='Doador Views'`, `perfil=Usuario.Perfil.DOADOR`.

- `email='doador.views@teste.com'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `password='SenhaForte123!'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Doador Views'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.DOADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 29 — Assign** (nível 2 do bloco).

Associa `cls.receptor` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email='receptor.views@teste.com'`, `password='SenhaForte123!'`, `nome='Receptor Views'`, `perfil=Usuario.Perfil.RECEPTOR`.

- `email='receptor.views@teste.com'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `password='SenhaForte123!'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Receptor Views'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.RECEPTOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 35 — Assign** (nível 2 do bloco).

Associa `cls.observador` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email='observador.views@teste.com'`, `password='SenhaForte123!'`, `nome='Observador Views'`, `perfil=Usuario.Perfil.OBSERVADOR`.

- `email='observador.views@teste.com'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `password='SenhaForte123!'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Observador Views'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.OBSERVADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 42 — FunctionDef** (nível 1 do bloco).

Define `_criar_extensa_concluida(self, usuario=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 42:

**Linha 43 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 45 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=usuario or self.doador`, `modalidade=Triagem.Modalidade.EXTENSA`, `status=Triagem.Status.CONCLUIDA`, `resultado=Triagem.Resultado.SEM_IMPEDIMENTO` ao chamador.

**Linha 52 — FunctionDef** (nível 1 do bloco).

Define `_iniciar_pela_rota(self, modalidade='extensa', usuario=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 52:

**Linha 53 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 55 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `usuario or self.doador`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 56 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:triagem_iniciar', kwargs={'modalidade': modalidade})`, `{'aceite_termo': 'on'}` ao chamador.

**Linha 64 — FunctionDef** (nível 1 do bloco).

Define `_preencher_ate_confirmacao(self, triagem)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 64:

**Linha 65 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 67 — Assign** (nível 2 do bloco).

Associa `preferencias` a uma coleção Tuple com 13 itens, na expressão `('NAO', 'NAO_SEI', 'NENHUMA', 'NENHUM', 'NUNCA', 'SIM', '18_60', '56_129_9', 'MASCULINO', 'ORIGINAL', 'DESCANSADO', 'LEVE', 'NAO_MEDI')`.

**Linha 72 — For** (nível 2 do bloco).

Percorre `triagem.fluxo_perguntas[:-1]`; cada item é atribuído a `id_pergunta` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 72:

**Linha 73 — Assign** (nível 3 do bloco).

Associa `pergunta` a a chamada `obter_pergunta`; argumentos posicionais: `id_pergunta`.


**Linha 74 — Assign** (nível 3 do bloco).

Associa `opcoes` a uma coleção/gerador construído por compreensão em `{opcao['codigo']: opcao['rotulo'] for opcao in pergunta['opcoes']}`: percorre as fontes e aplica os filtros declarados.

**Linha 78 — Assign** (nível 3 do bloco).

Associa `codigo` a `'SIM'` se `id_pergunta in {'EXT-01', 'EXT-08', 'EXT-11'}` for verdadeiro; caso contrário, `next((item for item in preferencias if item in opcoes))`.

**Linha 83 — Expr** (nível 3 do bloco).

Executa a chamada `RespostaTriagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `triagem=triagem`, `id_pergunta=id_pergunta`, `codigo_resposta=codigo`, `resposta_label=opcoes[codigo]`, `valor={'codigos': [codigo], 'datas': {}, 'detalhes': ''}`, `rule_version=pergunta['regra_version']`, `source_ref=pergunta['fonte']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 92 — Assign** (nível 2 do bloco).

Associa `triagem.pergunta_atual` a a expressão `len(triagem.fluxo_perguntas) - 1`; seus operadores determinam o cálculo.

**Linha 93 — Expr** (nível 2 do bloco).

Executa a chamada `triagem.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['pergunta_atual']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 95 — FunctionDef** (nível 1 do bloco).

Define `test_apresentacao_publica_mostra_texto_e_duas_modalidades(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: apresentacao publica mostra texto e duas modalidades.

Bloco `body` da linha 95:

**Linha 96 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 98 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:triagem_apresentacao')`.


**Linha 100 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `200`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 101 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Seu gesto de cuidado começa aqui.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 102 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Triagem extensa'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 103 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Triagem simplificada'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 104 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Quem dará a resposta final será sempre'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 105 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Criar conta'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 107 — FunctionDef** (nível 1 do bloco).

Define `test_visitante_ve_botoes_de_acao_na_apresentacao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: visitante ve botoes de acao na apresentacao.

Bloco `body` da linha 107:

**Linha 108 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 110 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:triagem_apresentacao')`.


**Linha 112 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `200`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 113 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Criar conta para iniciar a triagem extensa'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 114 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Entrar para continuar uma triagem'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 116 — FunctionDef** (nível 1 do bloco).

Define `test_inicio_exige_post_e_login(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: inicio exige post e login.

Bloco `body` da linha 116:

**Linha 117 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 119 — Assign** (nível 2 do bloco).

Associa `url` a a chamada `reverse`, que resolve o endereço a partir do nome da rota; argumentos posicionais: `'accounts:triagem_iniciar'`; argumentos nomeados: `kwargs={'modalidade': 'extensa'}`.

- `kwargs={'modalidade': 'extensa'}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 124 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `url`.


**Linha 125 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `302`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 126 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `reverse('accounts:login')`, `resposta.url`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 130 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.doador`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 131 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.client.get(url).status_code`, `405`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 132 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `Triagem.objects.count()`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 134 — FunctionDef** (nível 1 do bloco).

Define `test_doador_pode_iniciar_extensa(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: doador pode iniciar extensa.

Bloco `body` da linha 134:

**Linha 135 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 137 — For** (nível 2 do bloco).

Percorre `(self.doador,)`; cada item é atribuído a `usuario` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 137:

**Linha 138 — With** (nível 3 do bloco).

Executa sob os contextos `self.subTest(perfil=usuario.perfil)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 138:

**Linha 139 — Assign** (nível 4 do bloco).

Associa `resposta` a a chamada `self._iniciar_pela_rota`; argumentos nomeados: `usuario=usuario`.

- `usuario=usuario`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 140 — Assign** (nível 4 do bloco).

Associa `triagem` a a chamada `Triagem.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `usuario=usuario`.

- `usuario=usuario`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 141 — Expr** (nível 4 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:triagem_pergunta', kwargs={'id_triagem': triagem.pk})`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 149 — FunctionDef** (nível 1 do bloco).

Define `test_apresentacao_oferece_reutilizar_extensa_concluida(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: apresentacao oferece reutilizar extensa concluida.

Bloco `body` da linha 149:

**Linha 150 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 152 — Expr** (nível 2 do bloco).

Executa a chamada `self._criar_extensa_concluida`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 153 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.doador`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 155 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:triagem_apresentacao')`.


**Linha 157 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Reutilizar respostas da última triagem extensa concluída.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 162 — FunctionDef** (nível 1 do bloco).

Define `test_observador_nao_pode_iniciar(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: observador nao pode iniciar.

Bloco `body` da linha 162:

**Linha 163 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 165 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self._iniciar_pela_rota`; argumentos nomeados: `usuario=self.observador`.

- `usuario=self.observador`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 167 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `403`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 168 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `Triagem.objects.filter(usuario=self.observador).exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 170 — FunctionDef** (nível 1 do bloco).

Define `test_simplificada_exige_extensa_anterior(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: simplificada exige extensa anterior.

Bloco `body` da linha 170:

**Linha 171 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 173 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self._iniciar_pela_rota`; argumentos posicionais: `'simplificada'`.


**Linha 175 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:triagem_apresentacao')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 179 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `Triagem.objects.filter(usuario=self.doador, modalidade=Triagem.Modalidade.SIMPLIFICADA).exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 186 — FunctionDef** (nível 1 do bloco).

Define `test_pagina_mostra_uma_pergunta_e_salva_resposta(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: pagina mostra uma pergunta e salva resposta.

Bloco `body` da linha 186:

**Linha 187 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 189 — Expr** (nível 2 do bloco).

Executa a chamada `self._iniciar_pela_rota`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 190 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `Triagem.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `usuario=self.doador`.

- `usuario=self.doador`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 191 — Assign** (nível 2 do bloco).

Associa `url` a a chamada `reverse`, que resolve o endereço a partir do nome da rota; argumentos posicionais: `'accounts:triagem_pergunta'`; argumentos nomeados: `kwargs={'id_triagem': triagem.pk}`.

- `kwargs={'id_triagem': triagem.pk}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 196 — Assign** (nível 2 do bloco).

Associa `resposta_get` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `url`.


**Linha 197 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta_get`, `'Você entende que esta pré-triagem'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 198 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta_get`, `'Pergunta 1 de'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 200 — Assign** (nível 2 do bloco).

Associa `resposta_post` a a chamada `self.client.post`; argumentos posicionais: `url`, `{'resposta': 'SIM', 'acao': 'continuar'}`.


**Linha 204 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta_post`, `url`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 205 — Expr** (nível 2 do bloco).

Executa a chamada `triagem.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 206 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.pergunta_atual`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 207 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `RespostaTriagem.objects.filter(triagem=triagem, id_pergunta='EXT-01').exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 214 — FunctionDef** (nível 1 do bloco).

Define `test_salvar_e_sair_conserva_andamento(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: salvar e sair conserva andamento.

Bloco `body` da linha 214:

**Linha 215 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 217 — Expr** (nível 2 do bloco).

Executa a chamada `self._iniciar_pela_rota`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 218 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `Triagem.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `usuario=self.doador`.

- `usuario=self.doador`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 219 — Assign** (nível 2 do bloco).

Associa `url` a a chamada `reverse`, que resolve o endereço a partir do nome da rota; argumentos posicionais: `'accounts:triagem_pergunta'`; argumentos nomeados: `kwargs={'id_triagem': triagem.pk}`.

- `kwargs={'id_triagem': triagem.pk}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 224 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `url`, `{'resposta': 'SIM', 'acao': 'salvar'}`.


**Linha 229 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:triagem_historico')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 230 — Expr** (nível 2 do bloco).

Executa a chamada `triagem.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 231 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.status`, `Triagem.Status.EM_ANDAMENTO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 232 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.pergunta_atual`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 234 — FunctionDef** (nível 1 do bloco).

Define `test_botao_anterior_retorna_sem_apagar_resposta(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: botao anterior retorna sem apagar resposta.

Bloco `body` da linha 234:

**Linha 235 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 237 — Expr** (nível 2 do bloco).

Executa a chamada `self._iniciar_pela_rota`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 238 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `Triagem.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `usuario=self.doador`.

- `usuario=self.doador`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 239 — Assign** (nível 2 do bloco).

Associa `url` a a chamada `reverse`, que resolve o endereço a partir do nome da rota; argumentos posicionais: `'accounts:triagem_pergunta'`; argumentos nomeados: `kwargs={'id_triagem': triagem.pk}`.

- `kwargs={'id_triagem': triagem.pk}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 243 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.post`; argumentos posicionais: `url`, `{'resposta': 'SIM', 'acao': 'continuar'}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 245 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `url`, `{'acao': 'anterior'}`.


**Linha 247 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `url`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 248 — Expr** (nível 2 do bloco).

Executa a chamada `triagem.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 249 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.pergunta_atual`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 250 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `triagem.respostas.filter(id_pergunta='EXT-01').exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 252 — FunctionDef** (nível 1 do bloco).

Define `test_triagem_de_outro_usuario_retorna_404(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: triagem de outro usuario retorna 404.

Bloco `body` da linha 252:

**Linha 253 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 255 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.receptor`, `modalidade=Triagem.Modalidade.EXTENSA`.

- `usuario=self.receptor`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `modalidade=Triagem.Modalidade.EXTENSA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 259 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.doador`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 261 — Assign** (nível 2 do bloco).

Associa `pergunta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:triagem_pergunta', kwargs={'id_triagem': triagem.pk})`.


**Linha 267 — Assign** (nível 2 do bloco).

Associa `resultado` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:triagem_resultado', kwargs={'id_triagem': triagem.pk})`.


**Linha 274 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pergunta.status_code`, `404`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 275 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resultado.status_code`, `404`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 277 — FunctionDef** (nível 1 do bloco).

Define `test_resultado_em_andamento_volta_para_pergunta(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: resultado em andamento volta para pergunta.

Bloco `body` da linha 277:

**Linha 278 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 280 — Expr** (nível 2 do bloco).

Executa a chamada `self._iniciar_pela_rota`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 281 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `Triagem.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `usuario=self.doador`.

- `usuario=self.doador`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 283 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:triagem_resultado', kwargs={'id_triagem': triagem.pk})`.


**Linha 290 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:triagem_revisao', kwargs={'id_triagem': triagem.pk})`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 295 — FunctionDef** (nível 1 do bloco).

Define `test_confirmacao_final_conclui_e_mostra_resultado(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: confirmacao final conclui e mostra resultado.

Bloco `body` da linha 295:

**Linha 296 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 298 — Expr** (nível 2 do bloco).

Executa a chamada `self._iniciar_pela_rota`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 299 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `Triagem.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `usuario=self.doador`.

- `usuario=self.doador`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 300 — Expr** (nível 2 do bloco).

Executa a chamada `self._preencher_ate_confirmacao`; argumentos posicionais: `triagem`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 301 — Assign** (nível 2 do bloco).

Associa `url` a a chamada `reverse`, que resolve o endereço a partir do nome da rota; argumentos posicionais: `'accounts:triagem_pergunta'`; argumentos nomeados: `kwargs={'id_triagem': triagem.pk}`.

- `kwargs={'id_triagem': triagem.pk}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 306 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `url`, `{'resposta': 'CONFIRMAR', 'acao': 'continuar'}`.


**Linha 311 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:triagem_revisao', kwargs={'id_triagem': triagem.pk})`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 315 — Expr** (nível 2 do bloco).

Executa a chamada `triagem.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 316 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.status`, `Triagem.Status.EM_ANDAMENTO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 318 — Assign** (nível 2 do bloco).

Associa `resposta_final` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:triagem_revisao', kwargs={'id_triagem': triagem.pk})`, `{'acao': 'finalizar'}`.


**Linha 322 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta_final`, `reverse('accounts:triagem_resultado', kwargs={'id_triagem': triagem.pk})`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 326 — Expr** (nível 2 do bloco).

Executa a chamada `triagem.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 327 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `triagem.status`, `Triagem.Status.CONCLUIDA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 329 — FunctionDef** (nível 1 do bloco).

Define `test_resumo_incorreto_abre_nova_extensa(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: resumo incorreto abre nova extensa.

Bloco `body` da linha 329:

**Linha 330 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 332 — Expr** (nível 2 do bloco).

Executa a chamada `self._criar_extensa_concluida`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 333 — Expr** (nível 2 do bloco).

Executa a chamada `self._iniciar_pela_rota`; argumentos posicionais: `'simplificada'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 334 — Assign** (nível 2 do bloco).

Associa `simplificada` a a chamada `Triagem.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `usuario=self.doador`, `modalidade=Triagem.Modalidade.SIMPLIFICADA`.

- `usuario=self.doador`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `modalidade=Triagem.Modalidade.SIMPLIFICADA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 338 — Assign** (nível 2 do bloco).

Associa `url` a a chamada `reverse`, que resolve o endereço a partir do nome da rota; argumentos posicionais: `'accounts:triagem_pergunta'`; argumentos nomeados: `kwargs={'id_triagem': simplificada.pk}`.

- `kwargs={'id_triagem': simplificada.pk}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 343 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `url`, `{'resposta': 'INCORRETO', 'acao': 'continuar'}`.


**Linha 348 — Expr** (nível 2 do bloco).

Executa a chamada `simplificada.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 349 — Assign** (nível 2 do bloco).

Associa `nova_extensa` a a chamada `Triagem.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `usuario=self.doador`, `modalidade=Triagem.Modalidade.EXTENSA`, `status=Triagem.Status.EM_ANDAMENTO`.

- `usuario=self.doador`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `modalidade=Triagem.Modalidade.EXTENSA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status=Triagem.Status.EM_ANDAMENTO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 354 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `simplificada.status`, `Triagem.Status.CANCELADA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 355 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:triagem_pergunta', kwargs={'id_triagem': nova_extensa.pk})`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 363 — FunctionDef** (nível 1 do bloco).

Define `test_historico_lista_somente_triagens_do_usuario(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: historico lista somente triagens do usuario.

Bloco `body` da linha 363:

**Linha 364 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 366 — Assign** (nível 2 do bloco).

Associa `propria` a a chamada `self._criar_extensa_concluida`; argumentos posicionais: `self.doador`.


**Linha 367 — Assign** (nível 2 do bloco).

Associa `alheia` a a chamada `self._criar_extensa_concluida`; argumentos posicionais: `self.receptor`.


**Linha 368 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.doador`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 370 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:triagem_historico')`.


**Linha 372 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `200`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 373 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `f'Triagem {propria.pk}'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 374 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotContains`, que o teste exige ausência de texto na resposta HTTP; argumentos posicionais: `resposta`, `f'Triagem {alheia.pk}'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 376 — FunctionDef** (nível 1 do bloco).

Define `test_dashboard_doador_aponta_para_triagem(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: dashboard doador aponta para triagem.

Bloco `body` da linha 376:

**Linha 377 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 379 — For** (nível 2 do bloco).

Percorre `(self.doador,)`; cada item é atribuído a `usuario` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 379:

**Linha 380 — With** (nível 3 do bloco).

Executa sob os contextos `self.subTest(perfil=usuario.perfil)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 380:

**Linha 381 — Expr** (nível 4 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `usuario`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 382 — Assign** (nível 4 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:dashboard')`.


**Linha 383 — Expr** (nível 4 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Triagem para doação'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 384 — Expr** (nível 4 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `reverse('accounts:triagem_apresentacao')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 389 — FunctionDef** (nível 1 do bloco).

Define `test_receptor_bloqueado_inclusive_triagem_antiga(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: receptor bloqueado inclusive triagem antiga.

Bloco `body` da linha 389:

**Linha 390 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.receptor`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 391 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `self._criar_extensa_concluida`; argumentos posicionais: `self.receptor`.


**Linha 392 — For** (nível 2 do bloco).

Percorre `('triagem_pergunta', 'triagem_resultado')`; cada item é atribuído a `rota` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 392:

**Linha 393 — Assign** (nível 3 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:' + rota, kwargs={'id_triagem': triagem.pk})`.


**Linha 394 — Expr** (nível 3 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `403`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 395 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self._iniciar_pela_rota(usuario=self.receptor).status_code`, `403`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 396 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotContains`, que o teste exige ausência de texto na resposta HTTP; argumentos posicionais: `self.client.get(reverse('accounts:dashboard'))`, `'Triagem para doação'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 128: `# Depois de autenticado, GET continua proibido: iniciar exige clique no`
- Linha 129: `# formulário POST da apresentação.`

