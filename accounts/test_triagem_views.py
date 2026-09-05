"""Testes das páginas públicas e privadas da triagem."""

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
            )
        )

    def _preencher_ate_confirmacao(self, triagem):
        """Preenche respostas neutras para testar a conclusão pela view."""

        preferencias = (
            "NAO", "NENHUMA", "NENHUM", "NUNCA", "SIM", "18_60",
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

    def test_doador_e_receptor_podem_iniciar_extensa(self):
        """Falha se um dos dois perfis autorizados não puder responder."""

        for usuario in (self.doador, self.receptor):
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
            reverse(
                "accounts:triagem_pergunta",
                kwargs={"id_triagem": triagem.pk},
            ),
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
            reverse(
                "accounts:triagem_resultado",
                kwargs={"id_triagem": triagem.pk},
            ),
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

    def test_dashboard_doador_e_receptor_aponta_para_triagem(self):
        """Falha se um perfil autorizado não encontrar a triagem no painel."""

        for usuario in (self.doador, self.receptor):
            with self.subTest(perfil=usuario.perfil):
                self.client.force_login(usuario)
                resposta = self.client.get(reverse("accounts:dashboard"))
                self.assertContains(resposta, "Triagem para doação")
                self.assertContains(
                    resposta,
                    reverse("accounts:triagem_apresentacao"),
                )
