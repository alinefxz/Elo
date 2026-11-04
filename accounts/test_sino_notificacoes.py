from django.test import Client, TestCase
from django.urls import reverse

from .models import Notificacao, Usuario


class SinoNotificacoesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = Usuario.objects.create_user(
            email='sino@teste.local', nome='Pessoa', perfil=Usuario.Perfil.RECEPTOR,
        )
        cls.outro = Usuario.objects.create_user(
            email='outro-sino@teste.local', nome='Outro', perfil=Usuario.Perfil.DOADOR,
        )

    def setUp(self):
        self.client.force_login(self.usuario)
        self.api = reverse('accounts:notificacoes_atualizacoes')
        self.central = reverse('accounts:notificacoes')

    def aviso(self, **extras):
        return Notificacao.objects.create(
            usuario=extras.pop('usuario', self.usuario), titulo=extras.pop('titulo', 'Aviso de teste'),
            mensagem='Existe uma necessidade de sangue.', **extras,
        )

    def test_sino_em_pagina_publica_para_autenticado_e_oculto_para_visitante(self):
        self.aviso()
        pagina = self.client.get(reverse('accounts:compatibilidade_sanguinea'))
        self.assertContains(pagina, 'data-notificacoes')
        self.assertContains(pagina, 'Notificações: 1 não lidas')
        self.assertContains(pagina, 'js/notificacoes.js')
        self.client.logout()
        pagina = self.client.get(reverse('accounts:compatibilidade_sanguinea'))
        self.assertNotContains(pagina, 'data-notificacoes')
        self.assertNotContains(pagina, 'js/notificacoes.js')

    def test_feed_expoe_apenas_avisos_do_proprio_usuario(self):
        meu = self.aviso()
        self.aviso(usuario=self.outro, titulo='Privado de outro')
        resposta = self.client.get(self.api)
        self.assertEqual(resposta.status_code, 200)
        dados = resposta.json()
        self.assertEqual(dados['nao_lidas'], 1)
        self.assertEqual([n['id'] for n in dados['itens']], [meu.pk])
        self.assertEqual(dados['novas'], [])
        self.assertIn('no-store', resposta['Cache-Control'])

    def test_novo_aviso_e_identificado_sem_recarregar_pagina(self):
        anterior = self.aviso()
        self.assertEqual(self.client.get(self.api, {'depois': anterior.pk}).json()['novas'], [])
        novo = self.aviso(titulo='Chegou agora')
        self.aviso(usuario=self.outro, titulo='Privado')
        dados = self.client.get(self.api, {'depois': anterior.pk}).json()
        self.assertEqual([n['id'] for n in dados['novas']], [novo.pk])
        self.assertEqual(dados['ultimo_id'], novo.pk)
        self.assertEqual(dados['nao_lidas'], 2)

    def test_marcar_lida_atualiza_contador_e_preserva_primeira_data(self):
        aviso = self.aviso()
        url = reverse('accounts:notificacao_ler', args=[aviso.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        resposta = self.client.post(url, HTTP_ACCEPT='application/json')
        self.assertEqual(resposta.json(), {'id': aviso.pk, 'lida': True})
        aviso.refresh_from_db()
        data = aviso.lida_em
        self.assertTrue(aviso.lida)
        self.assertIsNotNone(data)
        self.client.post(url, HTTP_ACCEPT='application/json')
        aviso.refresh_from_db()
        self.assertEqual(aviso.lida_em, data)
        self.assertEqual(self.client.get(self.api).json()['nao_lidas'], 0)
        self.assertContains(self.client.get(self.central), 'Aviso de teste')

    def test_aviso_de_outro_usuario_nao_pode_ser_marcado(self):
        aviso = self.aviso(usuario=self.outro)
        self.assertEqual(self.client.post(reverse('accounts:notificacao_ler', args=[aviso.pk])).status_code, 404)
        aviso.refresh_from_db()
        self.assertFalse(aviso.lida)
        self.assertIsNone(aviso.lida_em)

    def test_fallback_sem_javascript_volta_para_central(self):
        aviso = self.aviso()
        self.assertRedirects(self.client.post(reverse('accounts:notificacao_ler', args=[aviso.pk])), self.central)

    def test_endpoints_exigem_login(self):
        aviso = self.aviso()
        self.client.logout()
        self.assertEqual(self.client.get(self.api).status_code, 401)
        self.assertEqual(self.client.get(self.central).status_code, 302)
        self.assertEqual(self.client.post(reverse('accounts:notificacao_ler', args=[aviso.pk])).status_code, 302)
        aviso.refresh_from_db()
        self.assertFalse(aviso.lida)

    def test_post_de_leitura_exige_csrf(self):
        aviso = self.aviso()
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.usuario)
        url = reverse('accounts:notificacao_ler', args=[aviso.pk])
        self.assertEqual(cliente.post(url).status_code, 403)
        cliente.get(self.central)
        token = cliente.cookies['csrftoken'].value
        self.assertEqual(cliente.post(url, {'csrfmiddlewaretoken': token}).status_code, 302)

    def test_cursor_invalido_e_metodos_nao_permitidos(self):
        for cursor in ('abc', '-1', str(2**64)):
            self.assertEqual(self.client.get(self.api, {'depois': cursor}).status_code, 400)
        self.assertEqual(self.client.post(self.api).status_code, 405)
        self.assertEqual(self.client.post(self.central).status_code, 405)

    def test_url_externa_ou_javascript_nao_e_exibida_como_acao(self):
        for url in ('javascript:alert(1)', 'https://outro.site/privado', '//outro.site/'):
            aviso = self.aviso(url_destino=url)
            dados = self.client.get(self.api).json()
            self.assertEqual(next(n['url'] for n in dados['itens'] if n['id'] == aviso.pk), '')
            self.assertNotContains(self.client.get(self.central), f'href="{url}"')

    def test_url_interna_e_conteudo_html_escapado(self):
        aviso = self.aviso(titulo='<img src=x onerror=alert(1)>', url_destino=reverse('accounts:estoque_publico'),
                           tipo=Notificacao.Tipo.ESTOQUE_CRITICO)
        dados = self.client.get(self.api).json()['itens'][0]
        self.assertEqual(dados['acao'], 'Ver estoque')
        self.assertEqual(dados['url'], reverse('accounts:estoque_publico'))
        resposta = self.client.get(self.central)
        self.assertContains(resposta, '&lt;img')
        self.assertNotContains(resposta, aviso.titulo)

    def test_central_paginada_e_previa_limitada_com_contagem_total(self):
        for numero in range(12):
            self.aviso(titulo=f'Aviso {numero}')
        dados = self.client.get(self.api).json()
        self.assertEqual(dados['nao_lidas'], 12)
        self.assertEqual(len(dados['itens']), 8)
        self.assertEqual(len(self.client.get(self.central).context['pagina_notificacoes']), 10)
        self.assertEqual(len(self.client.get(self.central, {'pagina': 2}).context['pagina_notificacoes']), 2)
