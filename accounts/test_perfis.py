"""Regressões dos cinco perfis, das permissões e dos dados privados."""

from datetime import date, timedelta
import re
from unittest.mock import patch

from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import (
    AuditoriaAcaoCritica, ConsentimentoLGPD, Estoque, EstoqueMovimentacao,
    Notificacao, PedidoSangue, Triagem, Usuario, ValidacaoHemocentro,
)
from .perfil_forms import PerfilUsuarioForm
from .validacao_hemocentro import aprovar_hemocentro, recusar_hemocentro, solicitar_correcao_hemocentro
from .validacao_pedido import aprovar_pedido, criar_pedido_pendente, recusar_pedido, solicitar_correcao_pedido


@override_settings(PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher'])
class PerfisTests(TestCase):
    senha = 'SenhaPerfil2026!'
    papeis = (
        (Usuario.Perfil.OBSERVADOR, 'comum'),
        (Usuario.Perfil.DOADOR, 'doador'),
        (Usuario.Perfil.RECEPTOR, 'receptor'),
        (Usuario.Perfil.HEMOCENTRO, 'institucional'),
        (Usuario.Perfil.ADMINISTRADOR, 'administrador'),
    )

    @classmethod
    def setUpTestData(cls):
        cls.usuarios = {}
        for indice, (papel, flag) in enumerate(cls.papeis, 1):
            cls.usuarios[papel] = Usuario.objects.create_user(
                email=f'{flag}@perfis.test', password=cls.senha,
                nome=f'Conta {flag}', perfil=papel, telefone='35999999999',
                cidade='Pouso Alegre', estado='MG',
                data_nascimento=None if flag == 'institucional' else date(1990, 1, 1),
                cpf=None if flag == 'institucional' else f'{indice:011}',
                cnpj='12345678000199' if flag == 'institucional' else None,
                status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO,
                is_staff=flag == 'administrador', is_superuser=flag == 'administrador',
            )
        cls.outro = Usuario.objects.create_user(
            email='outro@perfis.test', password=cls.senha,
            nome='PESSOA_PRIVADA_ALHEIA', perfil=Usuario.Perfil.DOADOR,
        )
        cls.outro_hemo = Usuario.objects.create_user(
            email='outra-instituicao@perfis.test', nome='INSTITUICAO_PRIVADA_ALHEIA',
            perfil=Usuario.Perfil.HEMOCENTRO,
            status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO,
        )

    def usuario(self, papel):
        return self.usuarios[papel]

    def autenticar(self, papel):
        usuario = self.usuario(papel)
        self.client.force_login(usuario)
        return usuario

    def dados(self, usuario, **extras):
        dados = {
            'nome': usuario.nome, 'email': usuario.email, 'telefone': usuario.telefone,
            'estado': usuario.estado, 'cidade': usuario.cidade,
            'data_nascimento': usuario.data_nascimento.isoformat() if usuario.data_nascimento else '',
            'sexo': usuario.sexo, 'tipo_sanguineo': usuario.tipo_sanguineo,
            'endereco': getattr(usuario, 'endereco', ''),
            'horario_funcionamento': getattr(usuario, 'horario_funcionamento', ''),
        }
        return {**dados, **extras}

    def pedido(self, solicitante, hemocentro=None, titulo='Solicitação do próprio usuário'):
        return PedidoSangue.objects.create(
            solicitante=solicitante, hemocentro_destino=hemocentro or self.usuario(Usuario.Perfil.HEMOCENTRO),
            nome_solicitante=solicitante.nome, contato=solicitante.email,
            para_quem=PedidoSangue.ParaQuem.MIM, titulo=titulo, tipo_sanguineo='O-',
            urgencia=PedidoSangue.Urgencia.MEDIA, cidade='Pouso Alegre', estado='MG',
            descricao='Solicitação registrada para teste de privacidade.',
        )

    def notificacao(self, usuario, titulo='Notificação do próprio usuário'):
        return Notificacao.objects.create(usuario=usuario, titulo=titulo, mensagem='Evento real da conta.')

    def menu(self, response):
        html = response.content.decode()
        return re.search(r'<nav\b[^>]*class="main-nav"[^>]*>(.*?)</nav>', html, re.S).group(1)

    def test_login_dos_cinco_papeis_abre_perfil_correspondente(self):
        for papel, flag in self.papeis:
            with self.subTest(papel=papel):
                self.client.logout()
                resposta = self.client.post(reverse('accounts:login'), {
                    'username': self.usuario(papel).email, 'password': self.senha,
                })
                self.assertRedirects(resposta, reverse('accounts:perfil'))
                perfil = self.client.get(reverse('accounts:perfil'))
                self.assertTrue(perfil.context['perfil'][flag])
                self.assertContains(perfil, self.usuario(papel).nome)

    def test_login_respeita_next_local_e_rejeita_destino_externo(self):
        usuario = self.usuario(Usuario.Perfil.DOADOR)
        destino = reverse('accounts:triagem_apresentacao')
        for next_url, esperado in ((destino, destino), ('https://externo.test/roubar', reverse('accounts:perfil'))):
            with self.subTest(next_url=next_url):
                self.client.logout()
                resposta = self.client.post(reverse('accounts:login'), {
                    'username': usuario.email, 'password': self.senha, 'next': next_url,
                })
                self.assertRedirects(resposta, esperado)

    def test_perfis_privados_exigem_login(self):
        for rota in ('perfil', 'perfil_editar', 'perfil_senha'):
            with self.subTest(rota=rota):
                resposta = self.client.get(reverse('accounts:' + rota))
                self.assertEqual(resposta.status_code, 302)
                self.assertIn(reverse('accounts:login'), resposta.url)

    def test_cinco_papeis_editam_e_recuperam_dados_persistidos(self):
        for papel, _ in self.papeis:
            with self.subTest(papel=papel):
                usuario = self.autenticar(papel)
                self.assertEqual(self.client.get(reverse('accounts:perfil_editar')).status_code, 200)
                nome = f'Nome atualizado {papel}'
                resposta = self.client.post(reverse('accounts:perfil_editar'), self.dados(
                    usuario, nome=nome, telefone='(35) 98888-7777',
                ))
                self.assertEqual(resposta.status_code, 302)
                usuario.refresh_from_db()
                self.assertEqual(usuario.nome, nome)
                self.assertEqual(re.sub(r'\D', '', usuario.telefone), '35988887777')
                self.assertContains(self.client.get(reverse('accounts:perfil')), nome)

    def test_formulario_apresenta_campos_especificos_sem_permissoes_editaveis(self):
        proibidos = {
            'perfil', 'cpf', 'cnpj', 'status_validacao', 'is_staff', 'is_superuser',
            'is_active', 'suspensa', 'groups', 'user_permissions', 'email_verificado',
            'tipo_sanguineo_confirmado', 'aceita_notificacoes_pedidos',
        }
        for papel, _ in self.papeis:
            with self.subTest(papel=papel):
                campos = PerfilUsuarioForm(instance=self.usuario(papel)).fields
                self.assertFalse(proibidos.intersection(campos))
                self.assertTrue({'nome', 'email', 'telefone', 'estado', 'cidade'}.issubset(campos))
                if papel == Usuario.Perfil.HEMOCENTRO:
                    self.assertTrue({'endereco', 'horario_funcionamento'}.issubset(campos))
                    self.assertNotIn('data_nascimento', campos)
                    self.assertNotIn('tipo_sanguineo', campos)
                else:
                    self.assertNotIn('endereco', campos)
                    self.assertNotIn('horario_funcionamento', campos)

    def test_post_forjado_nao_altera_papel_documentos_permissoes_nem_outro_usuario(self):
        campos_imutaveis = (
            'perfil', 'cpf', 'cnpj', 'status_validacao', 'is_staff', 'is_superuser',
            'is_active', 'suspensa', 'email_verificado', 'tipo_sanguineo_confirmado',
        )
        for papel, _ in self.papeis:
            with self.subTest(papel=papel):
                usuario = self.autenticar(papel)
                antes = {campo: getattr(usuario, campo) for campo in campos_imutaveis}
                resposta = self.client.post(reverse('accounts:perfil_editar'), self.dados(
                    usuario, nome='Minha edição autorizada', usuario_id=self.outro.pk, id_usuario=self.outro.pk,
                    perfil=Usuario.Perfil.ADMINISTRADOR, cpf='99999999999', cnpj='99999999999999',
                    status_validacao='RECUSADO', is_staff='on', is_superuser='on', is_active='',
                    suspensa='on', email_verificado='on', tipo_sanguineo_confirmado='on',
                    groups=[1], user_permissions=[1],
                ))
                self.assertEqual(resposta.status_code, 302)
                usuario.refresh_from_db()
                self.assertEqual({campo: getattr(usuario, campo) for campo in campos_imutaveis}, antes)
                self.assertEqual(usuario.nome, 'Minha edição autorizada')
                self.outro.refresh_from_db()
                self.assertEqual(self.outro.nome, 'PESSOA_PRIVADA_ALHEIA')
                self.assertFalse(usuario.groups.exists())
                self.assertFalse(usuario.user_permissions.exists())

    def test_perfil_ignora_identificador_alheio_e_nao_possui_rota_por_id(self):
        for papel, _ in self.papeis:
            with self.subTest(papel=papel):
                usuario = self.autenticar(papel)
                resposta = self.client.get(reverse('accounts:perfil'), {'usuario_id': self.outro.pk, 'id_usuario': self.outro.pk})
                self.assertContains(resposta, usuario.nome)
                self.assertNotContains(resposta, 'PESSOA_PRIVADA_ALHEIA')
                self.assertEqual(self.client.get(f'/perfil/{self.outro.pk}/').status_code, 404)

    def test_hemocentro_persiste_dados_institucionais_e_preserva_validacao(self):
        usuario = self.autenticar(Usuario.Perfil.HEMOCENTRO)
        validacao = ValidacaoHemocentro.objects.create(
            hemocentro=usuario, admin=self.usuario(Usuario.Perfil.ADMINISTRADOR),
            status=usuario.status_validacao, parecer='Cadastro analisado.',
        )
        resposta = self.client.post(reverse('accounts:perfil_editar'), self.dados(
            usuario, endereco='Rua da Solidariedade, 100', horario_funcionamento='Segunda a sexta, 8h às 16h',
        ))
        self.assertEqual(resposta.status_code, 302)
        usuario.refresh_from_db()
        self.assertEqual(usuario.endereco, 'Rua da Solidariedade, 100')
        self.assertEqual(usuario.horario_funcionamento, 'Segunda a sexta, 8h às 16h')
        self.assertEqual(usuario.status_validacao, Usuario.StatusValidacaoHemocentro.APROVADO)
        self.assertTrue(ValidacaoHemocentro.objects.filter(pk=validacao.pk, hemocentro=usuario).exists())
        perfil = self.client.get(reverse('accounts:perfil'))
        self.assertContains(perfil, usuario.endereco)
        self.assertContains(perfil, usuario.horario_funcionamento)
        self.assertContains(perfil, usuario.cnpj)

    def test_sangue_confirmado_nao_pode_ser_sobrescrito(self):
        usuario = self.autenticar(Usuario.Perfil.DOADOR)
        usuario.tipo_sanguineo = 'O-'
        usuario.tipo_sanguineo_confirmado = True
        usuario.save(update_fields=['tipo_sanguineo', 'tipo_sanguineo_confirmado'])
        form = PerfilUsuarioForm(instance=usuario)
        if 'tipo_sanguineo' in form.fields:
            self.assertTrue(form.fields['tipo_sanguineo'].disabled)
        self.client.post(reverse('accounts:perfil_editar'), self.dados(usuario, tipo_sanguineo='AB+'))
        usuario.refresh_from_db()
        self.assertEqual(usuario.tipo_sanguineo, 'O-')
        self.assertTrue(usuario.tipo_sanguineo_confirmado)

    def test_email_normalizado_e_duplicidade_sem_diferenca_de_caixa(self):
        usuario = self.usuario(Usuario.Perfil.DOADOR)
        form = PerfilUsuarioForm(self.dados(usuario, email='  NOVO@PERFIS.TEST  '), instance=usuario)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        usuario.refresh_from_db()
        self.assertEqual(usuario.email, 'novo@perfis.test')
        form = PerfilUsuarioForm(self.dados(usuario, email=self.outro.email.upper()), instance=usuario)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_validacao_de_nome_nascimento_telefone_estado_e_localizacao(self):
        usuario = self.usuario(Usuario.Perfil.DOADOR)
        invalidos = (
            ('nome', ''), ('data_nascimento', (timezone.localdate() + timedelta(days=1)).isoformat()),
            ('telefone', '1234567'), ('telefone', '1234567890123456'), ('estado', 'XX'),
        )
        for campo, valor in invalidos:
            with self.subTest(campo=campo, valor=valor):
                form = PerfilUsuarioForm(self.dados(usuario, **{campo: valor}), instance=usuario)
                self.assertFalse(form.is_valid())
                self.assertIn(campo, form.errors)
        form = PerfilUsuarioForm(self.dados(usuario, estado='SP', cidade='Santos'), instance=usuario)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        usuario.refresh_from_db()
        self.assertEqual((usuario.estado, usuario.cidade), ('SP', 'Santos'))

    def test_formulario_invalido_nao_grava_alteracoes_parciais(self):
        usuario = self.autenticar(Usuario.Perfil.RECEPTOR)
        nome_original = usuario.nome
        resposta = self.client.post(reverse('accounts:perfil_editar'), self.dados(
            usuario, nome='Não deve persistir', email='email-invalido',
        ))
        self.assertEqual(resposta.status_code, 200)
        usuario.refresh_from_db()
        self.assertEqual(usuario.nome, nome_original)
        self.assertContains(resposta, 'Não deve persistir')

    def test_notificacoes_dos_cinco_papeis_sao_privadas_e_leitura_persistente(self):
        alheia = self.notificacao(self.outro, 'AVISO_PRIVADO_ALHEIO')
        for papel, _ in self.papeis:
            with self.subTest(papel=papel):
                usuario = self.autenticar(papel)
                minha = self.notificacao(usuario, f'Aviso específico {papel}')
                resposta = self.client.get(reverse('accounts:perfil'))
                self.assertContains(resposta, minha.titulo)
                self.assertNotContains(resposta, alheia.titulo)
                self.assertEqual({n.usuario_id for n in resposta.context['notificacoes_perfil']}, {usuario.pk})
                feed = self.client.get(reverse('accounts:notificacoes_atualizacoes')).json()
                self.assertIn(minha.pk, [item['id'] for item in feed['itens']])
                self.assertNotIn(alheia.pk, [item['id'] for item in feed['itens']])
                self.assertEqual(self.client.post(reverse('accounts:notificacao_ler', args=[alheia.pk])).status_code, 404)
                self.assertEqual(self.client.post(reverse('accounts:notificacao_ler', args=[minha.pk])).status_code, 302)
                minha.refresh_from_db()
                self.assertTrue(minha.lida)
                self.assertIsNotNone(minha.lida_em)
                self.assertContains(self.client.get(reverse('accounts:notificacoes')), minha.titulo)
        alheia.refresh_from_db()
        self.assertFalse(alheia.lida)

    def test_historico_de_solicitacoes_do_comum_doador_e_receptor_e_privado(self):
        self.pedido(self.outro, titulo='SOLICITACAO_PRIVADA_ALHEIA')
        for papel in (Usuario.Perfil.OBSERVADOR, Usuario.Perfil.DOADOR, Usuario.Perfil.RECEPTOR):
            with self.subTest(papel=papel):
                usuario = self.autenticar(papel)
                pedido = self.pedido(usuario, titulo=f'Solicitação registrada {papel}')
                resposta = self.client.get(reverse('accounts:perfil'))
                self.assertContains(resposta, pedido.titulo)
                self.assertNotContains(resposta, 'SOLICITACAO_PRIVADA_ALHEIA')
                self.assertTrue(resposta.context['historico'])

    def test_historico_de_triagens_do_doador_individualiza_modalidades_e_status(self):
        usuario = self.autenticar(Usuario.Perfil.DOADOR)
        minha = Triagem.objects.create(usuario=usuario, modalidade=Triagem.Modalidade.SIMPLIFICADA)
        concluida = Triagem.objects.create(
            usuario=usuario, modalidade=Triagem.Modalidade.EXTENSA, status=Triagem.Status.CONCLUIDA,
            finalizada_em=timezone.now(), mensagem_resultado='RESULTADO_PRIVADO_PROPRIO',
        )
        alheia = Triagem.objects.create(
            usuario=self.outro, modalidade=Triagem.Modalidade.EXTENSA, status=Triagem.Status.CONCLUIDA,
            mensagem_resultado='RESULTADO_CLINICO_ALHEIO',
        )
        resposta = self.client.get(reverse('accounts:perfil'))
        historico = list(resposta.context['historico'])
        urls = [item['url'] for item in historico]
        self.assertIn(reverse('accounts:triagem_pergunta', args=[minha.pk]), urls)
        self.assertIn(reverse('accounts:triagem_resultado', args=[concluida.pk]), urls)
        self.assertNotIn(reverse('accounts:triagem_resultado', args=[alheia.pk]), urls)
        self.assertNotContains(resposta, 'RESULTADO_CLINICO_ALHEIO')
        self.assertContains(resposta, 'simplificada')
        self.assertContains(resposta, 'extensa')

    def test_historico_institucional_nao_inclui_outra_instituicao(self):
        usuario = self.autenticar(Usuario.Perfil.HEMOCENTRO)
        meu = self.pedido(self.usuario(Usuario.Perfil.RECEPTOR), hemocentro=usuario, titulo='Solicitação destinada à instituição')
        self.pedido(self.outro, hemocentro=self.outro_hemo, titulo='PEDIDO_DE_OUTRA_INSTITUICAO')
        resposta = self.client.get(reverse('accounts:perfil'))
        self.assertContains(resposta, meu.titulo)
        self.assertNotContains(resposta, 'PEDIDO_DE_OUTRA_INSTITUICAO')
        self.assertNotContains(resposta, self.outro_hemo.email)

    def test_historico_de_estoque_e_limitado_a_instituicao_responsavel(self):
        usuario = self.autenticar(Usuario.Perfil.HEMOCENTRO)
        for instituicao, tipo in ((usuario, 'O-'), (self.outro_hemo, 'AB+')):
            estoque = Estoque.objects.create(
                hemocentro=instituicao, tipo_sanguineo=tipo, quantidade_bolsas=12,
                nivel_minimo=10, nivel_critico=5,
            )
            EstoqueMovimentacao.objects.create(
                estoque=estoque, usuario_resp=instituicao, tipo_movimento='ENTRADA',
                quantidade_anterior=10, quantidade_movimentada=2, quantidade_nova=12,
                motivo='MOTIVO_INTERNO_NAO_EXIBIR',
            )
        resposta = self.client.get(reverse('accounts:perfil'))
        historico = list(resposta.context['historico'])
        self.assertEqual(len(historico), 1)
        self.assertIn('O-', historico[0]['titulo'])
        self.assertEqual(historico[0]['url'], reverse('accounts:estoque_hemocentro'))
        self.assertNotIn('AB+', str(historico))
        self.assertNotContains(resposta, 'MOTIVO_INTERNO_NAO_EXIBIR')

    def test_historico_misto_paginado_mantem_ordem_e_isolamento(self):
        usuario = self.autenticar(Usuario.Perfil.DOADOR)
        for numero in range(6):
            self.pedido(usuario, titulo=f'Meu pedido histórico {numero}')
            Triagem.objects.create(usuario=usuario, modalidade=Triagem.Modalidade.SIMPLIFICADA)
        self.pedido(self.outro, titulo='PEDIDO_ALHEIO_FORA_DA_PAGINACAO')
        primeira = self.client.get(reverse('accounts:perfil'))
        pagina = primeira.context['historico']
        self.assertEqual(pagina.paginator.count, 12)
        self.assertEqual(len(pagina), 10)
        self.assertTrue(pagina.has_next())
        segunda = self.client.get(reverse('accounts:perfil'), {'pagina': 2})
        self.assertEqual(len(segunda.context['historico']), 2)
        registros = list(pagina) + list(segunda.context['historico'])
        datas = [registro['data'] for registro in registros]
        self.assertEqual(datas, sorted(datas, reverse=True))
        self.assertNotContains(primeira, 'PEDIDO_ALHEIO_FORA_DA_PAGINACAO')
        self.assertNotContains(segunda, 'PEDIDO_ALHEIO_FORA_DA_PAGINACAO')

    def test_historico_administrativo_apresenta_atividade_real_sem_respostas_clinicas(self):
        usuario = self.autenticar(Usuario.Perfil.ADMINISTRADOR)
        registro = AuditoriaAcaoCritica.objects.create(
            usuario=usuario, acao=AuditoriaAcaoCritica.Acao.MODERACAO,
            descricao='DESCRICAO_SENSIVEL_NAO_EXIBIR', metadados={'evento': 'REVISAO', 'privado': 'METADADO_SENSIVEL'},
        )
        AuditoriaAcaoCritica.objects.create(
            usuario=self.outro, acao=AuditoriaAcaoCritica.Acao.MODERACAO,
            descricao='ATIVIDADE_DE_OUTRA_CONTA_ADMINISTRATIVA',
        )
        Triagem.objects.create(usuario=self.outro, mensagem_resultado='SEGREDO_CLINICO_INACESSIVEL')
        resposta = self.client.get(reverse('accounts:perfil'))
        historico = list(resposta.context['historico'])
        self.assertEqual(len(historico), 1)
        self.assertEqual(historico[0]['titulo'], registro.get_acao_display())
        self.assertEqual(historico[0]['status'], registro.get_resultado_display())
        self.assertEqual(historico[0]['data'], registro.criado_em)
        self.assertNotContains(resposta, 'DESCRICAO_SENSIVEL_NAO_EXIBIR')
        self.assertNotContains(resposta, 'METADADO_SENSIVEL')
        self.assertNotContains(resposta, 'ATIVIDADE_DE_OUTRA_CONTA_ADMINISTRATIVA')
        self.assertNotContains(resposta, 'SEGREDO_CLINICO_INACESSIVEL')

    def test_menus_refletem_permissoes_dos_cinco_papeis(self):
        for papel, _ in self.papeis:
            with self.subTest(papel=papel):
                self.autenticar(papel)
                menu = self.menu(self.client.get(reverse('accounts:perfil')))
                self.assertIn(reverse('accounts:perfil'), menu)
                self.assertEqual(reverse('accounts:triagem_apresentacao') in menu, papel == Usuario.Perfil.DOADOR)
                self.assertEqual(reverse('accounts:pedido_publicar') in menu, papel in {
                    Usuario.Perfil.OBSERVADOR, Usuario.Perfil.DOADOR, Usuario.Perfil.RECEPTOR,
                })
                self.assertEqual(reverse('accounts:estoque_hemocentro') in menu, papel == Usuario.Perfil.HEMOCENTRO)
                self.assertEqual(reverse('accounts:painel_aprovacao_hemocentros') in menu, papel == Usuario.Perfil.ADMINISTRADOR)

    def test_hemocentro_sem_aprovacao_tem_perfil_mas_nao_gerencia_estoque_ou_pedidos(self):
        usuario = self.autenticar(Usuario.Perfil.HEMOCENTRO)
        for status in ('PENDENTE', 'RECUSADO', 'CORRECAO'):
            with self.subTest(status=status):
                usuario.status_validacao = status
                usuario.save(update_fields=['status_validacao'])
                resposta = self.client.get(reverse('accounts:perfil'))
                self.assertEqual(resposta.status_code, 200)
                menu = self.menu(resposta)
                self.assertNotIn(reverse('accounts:estoque_hemocentro'), menu)
                self.assertNotIn(reverse('accounts:painel_pedidos_hemocentro'), menu)
                self.assertEqual(self.client.get(reverse('accounts:estoque_hemocentro')).status_code, 403)
                self.assertEqual(self.client.get(reverse('accounts:painel_pedidos_hemocentro')).status_code, 403)

    def test_triagens_somente_doador_e_modalidades_independentes(self):
        for papel, _ in self.papeis:
            usuario = self.autenticar(papel)
            for modalidade in ('simplificada', 'extensa'):
                with self.subTest(papel=papel, modalidade=modalidade):
                    resposta = self.client.post(reverse('accounts:triagem_iniciar', args=[modalidade]), {'aceite_termo': 'on'})
                    if papel == Usuario.Perfil.DOADOR:
                        self.assertEqual(resposta.status_code, 302)
                        registro = Triagem.objects.get(usuario=usuario, modalidade=modalidade.upper())
                        if modalidade == 'simplificada':
                            self.assertIsNone(registro.triagem_base_id)
                    else:
                        self.assertEqual(resposta.status_code, 403)
                        self.assertFalse(Triagem.objects.filter(usuario=usuario).exists())
        self.assertEqual(Triagem.objects.filter(usuario=self.usuario(Usuario.Perfil.DOADOR)).count(), 2)

    def test_nenhum_papel_consulta_triagem_alheia_pelas_rotas_privadas(self):
        triagem = Triagem.objects.create(usuario=self.outro)
        for papel, _ in self.papeis:
            self.autenticar(papel)
            for rota in ('triagem_pergunta', 'triagem_revisao', 'triagem_resultado'):
                with self.subTest(papel=papel, rota=rota):
                    resposta = self.client.get(reverse('accounts:' + rota, args=[triagem.pk]))
                    self.assertIn(resposta.status_code, (403, 404))

    def test_papeis_nao_institucionais_nao_acessam_estoque_privado(self):
        for papel, _ in self.papeis:
            if papel != Usuario.Perfil.HEMOCENTRO:
                with self.subTest(papel=papel):
                    self.autenticar(papel)
                    self.assertEqual(self.client.get(reverse('accounts:estoque_hemocentro')).status_code, 403)

    def test_validacao_institucional_bloqueada_para_os_quatro_papeis_nao_admin(self):
        for papel, _ in self.papeis:
            self.autenticar(papel)
            resposta = self.client.get(reverse('accounts:painel_aprovacao_hemocentros'))
            with self.subTest(papel=papel):
                self.assertEqual(resposta.status_code, 200 if papel == Usuario.Perfil.ADMINISTRADOR else 403)

    def test_preferencia_convocacao_somente_doador_e_consentimento_persistente(self):
        rota = reverse('accounts:perfil_preferencias')
        for papel, _ in self.papeis:
            usuario = self.autenticar(papel)
            resposta = self.client.post(rota, {'aceita_convocacoes': 'on'})
            with self.subTest(papel=papel):
                self.assertEqual(resposta.status_code, 302 if papel == Usuario.Perfil.DOADOR else 403)
                usuario.refresh_from_db()
                if papel == Usuario.Perfil.DOADOR:
                    self.assertTrue(usuario.aceita_notificacoes_pedidos)
                    self.assertTrue(usuario.consentimentos_lgpd.filter(
                        tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES, aceito=True,
                        revogado_em__isnull=True,
                    ).exists())
        self.autenticar(Usuario.Perfil.DOADOR)
        self.assertEqual(self.client.get(rota).status_code, 405)
        self.client.post(rota, {})
        doador = self.usuario(Usuario.Perfil.DOADOR)
        doador.refresh_from_db()
        self.assertFalse(doador.aceita_notificacoes_pedidos)

    def test_alteracao_de_senha_dos_cinco_papeis_mantem_sessao(self):
        nova_senha = 'OutraSenhaSegura2026!'
        for papel, _ in self.papeis:
            with self.subTest(papel=papel):
                usuario = self.autenticar(papel)
                resposta = self.client.post(reverse('accounts:perfil_senha'), {
                    'old_password': self.senha, 'new_password1': nova_senha, 'new_password2': nova_senha,
                })
                self.assertEqual(resposta.status_code, 302)
                usuario.refresh_from_db()
                self.assertTrue(usuario.check_password(nova_senha))
                self.assertEqual(self.client.get(reverse('accounts:perfil')).status_code, 200)
                self.assertEqual(int(self.client.session['_auth_user_id']), usuario.pk)

    def test_senha_atual_incorreta_nao_altera_credencial(self):
        usuario = self.autenticar(Usuario.Perfil.DOADOR)
        resposta = self.client.post(reverse('accounts:perfil_senha'), {
            'old_password': 'Incorreta123!', 'new_password1': 'NovaSenha2026!', 'new_password2': 'NovaSenha2026!',
        })
        self.assertEqual(resposta.status_code, 200)
        usuario.refresh_from_db()
        self.assertTrue(usuario.check_password(self.senha))

    def test_edicao_e_senha_exigem_csrf(self):
        usuario = self.usuario(Usuario.Perfil.DOADOR)
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(usuario)
        for rota in ('perfil_editar', 'perfil_senha', 'perfil_preferencias'):
            with self.subTest(rota=rota):
                self.assertEqual(cliente.post(reverse('accounts:' + rota), {}).status_code, 403)

    def test_staff_sem_papel_admin_nao_recebe_validacao_administrativa(self):
        usuario = self.usuario(Usuario.Perfil.OBSERVADOR)
        usuario.is_staff = True
        usuario.save(update_fields=['is_staff'])
        self.client.force_login(usuario)
        menu = self.menu(self.client.get(reverse('accounts:perfil')))
        self.assertNotIn(reverse('accounts:painel_aprovacao_hemocentros'), menu)
        self.assertEqual(self.client.get(reverse('accounts:painel_aprovacao_hemocentros')).status_code, 403)

    def test_staff_observador_com_permissao_de_auditoria_nao_recebe_atalho_restrito(self):
        usuario = self.usuario(Usuario.Perfil.OBSERVADOR)
        usuario.is_staff = True
        usuario.save(update_fields=['is_staff'])
        usuario.user_permissions.add(Permission.objects.get(
            content_type__app_label='accounts', codename='view_auditoriaacaocritica',
        ))
        self.client.force_login(usuario)
        url_auditoria = reverse('admin:accounts_auditoriaacaocritica_changelist')
        resposta = self.client.get(reverse('accounts:perfil'))
        self.assertNotContains(resposta, f'href="{url_auditoria}"')
        self.assertFalse(resposta.context['acessos']['consultar_auditoria'])
        self.assertEqual(self.client.get(url_auditoria).status_code, 403)

    def test_admin_com_permissao_change_auditoria_pode_consultar_sem_permissao_view(self):
        usuario = self.usuario(Usuario.Perfil.ADMINISTRADOR)
        usuario.is_superuser = False
        usuario.save(update_fields=['is_superuser'])
        usuario.user_permissions.add(Permission.objects.get(
            content_type__app_label='accounts', codename='change_auditoriaacaocritica',
        ))
        self.client.force_login(usuario)
        url_auditoria = reverse('admin:accounts_auditoriaacaocritica_changelist')
        resposta = self.client.get(reverse('accounts:perfil'))
        self.assertContains(resposta, f'href="{url_auditoria}"')
        self.assertTrue(resposta.context['acessos']['consultar_auditoria'])
        self.assertFalse(usuario.has_perm('accounts.view_auditoriaacaocritica'))
        self.assertEqual(self.client.get(url_auditoria).status_code, 200)

    def test_admin_sem_staff_tem_perfil_administrativo_sem_prometer_acesso_django(self):
        usuario = self.usuario(Usuario.Perfil.ADMINISTRADOR)
        usuario.is_staff = False
        usuario.is_superuser = False
        usuario.save(update_fields=['is_staff', 'is_superuser'])
        self.client.force_login(usuario)
        resposta = self.client.get(reverse('accounts:perfil'))
        self.assertTrue(resposta.context['perfil']['administrador'])
        self.assertEqual(self.client.get(reverse('accounts:painel_aprovacao_hemocentros')).status_code, 200)
        self.assertNotIn(f'href="{reverse("admin:index")}"', self.menu(resposta))

    def test_atalhos_django_admin_respeitam_permissoes_de_modelo(self):
        usuario = self.usuario(Usuario.Perfil.ADMINISTRADOR)
        usuario.is_superuser = False
        usuario.save(update_fields=['is_superuser'])
        self.client.force_login(usuario)
        url_usuarios = reverse('admin:accounts_usuario_changelist')
        url_auditoria = reverse('admin:accounts_auditoriaacaocritica_changelist')
        resposta = self.client.get(reverse('accounts:perfil'))
        self.assertNotContains(resposta, f'href="{url_usuarios}"')
        self.assertNotContains(resposta, f'href="{url_auditoria}"')
        usuario.user_permissions.add(Permission.objects.get(content_type__app_label='accounts', codename='view_usuario'))
        resposta = self.client.get(reverse('accounts:perfil'))
        self.assertContains(resposta, f'href="{url_usuarios}"')
        self.assertNotContains(resposta, f'href="{url_auditoria}"')
        self.assertEqual(self.client.get(url_usuarios).status_code, 200)
        usuario.user_permissions.add(Permission.objects.get(content_type__app_label='accounts', codename='view_auditoriaacaocritica'))
        resposta = self.client.get(reverse('accounts:perfil'))
        self.assertContains(resposta, f'href="{url_auditoria}"')
        self.assertEqual(self.client.get(url_auditoria).status_code, 200)

    def test_trocar_email_revoga_verificacao_e_editar_nome_preserva_verificacao(self):
        usuario = self.usuario(Usuario.Perfil.DOADOR)
        usuario.email_verificado = True
        usuario.save(update_fields=['email_verificado'])
        form = PerfilUsuarioForm(self.dados(usuario, nome='Somente o nome'), instance=usuario)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        usuario.refresh_from_db()
        self.assertTrue(usuario.email_verificado)
        form = PerfilUsuarioForm(self.dados(usuario, email='novo-verificar@perfis.test'), instance=usuario)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        usuario.refresh_from_db()
        self.assertFalse(usuario.email_verificado)

    def test_edicao_preserva_decisao_institucional_concorrente(self):
        usuario = self.usuario(Usuario.Perfil.HEMOCENTRO)
        form = PerfilUsuarioForm(self.dados(usuario, telefone='35988887777'), instance=usuario)
        self.assertTrue(form.is_valid(), form.errors)
        Usuario.objects.filter(pk=usuario.pk).update(status_validacao='CORRECAO')
        form.save()
        usuario.refresh_from_db()
        self.assertEqual(usuario.status_validacao, 'CORRECAO')
        self.assertEqual(usuario.telefone, '35988887777')

    def test_edicao_preserva_tipo_sanguineo_confirmado_apos_abrir_formulario(self):
        usuario = self.usuario(Usuario.Perfil.DOADOR)
        form = PerfilUsuarioForm(self.dados(usuario, tipo_sanguineo='AB+', nome='Nome atualizado'), instance=usuario)
        self.assertTrue(form.is_valid(), form.errors)
        Usuario.objects.filter(pk=usuario.pk).update(tipo_sanguineo='O-', tipo_sanguineo_confirmado=True)
        form.save()
        usuario.refresh_from_db()
        self.assertEqual(usuario.tipo_sanguineo, 'O-')
        self.assertTrue(usuario.tipo_sanguineo_confirmado)
        self.assertEqual(usuario.nome, 'Nome atualizado')

    def dados_pedido_real(self):
        solicitante = self.usuario(Usuario.Perfil.RECEPTOR)
        return {
            'nome_solicitante': solicitante.nome, 'contato': solicitante.email,
            'hemocentro_destino': self.usuario(Usuario.Perfil.HEMOCENTRO),
            'para_quem': PedidoSangue.ParaQuem.MIM, 'titulo': 'Solicitação registrada pelo serviço',
            'tipo_sanguineo': 'O-', 'urgencia': PedidoSangue.Urgencia.MEDIA,
            'cidade': 'Pouso Alegre', 'estado': 'MG', 'nome_paciente': 'PACIENTE_NAO_NOTIFICAR',
            'descricao': 'DESCRICAO_CLINICA_NAO_NOTIFICAR',
        }

    def cadastro_hemo_real(self, email='novo-hemocentro@perfis.test'):
        return {
            'nome': 'Hemocentro cadastrado', 'email': email, 'perfil': Usuario.Perfil.HEMOCENTRO,
            'cnpj': '12345678000270', 'estado': 'MG', 'cidade': 'Pouso Alegre',
            'password1': self.senha, 'password2': self.senha, 'aceite_lgpd': 'on',
        }

    def test_cadastro_real_de_hemo_notifica_apenas_administradores_ativos(self):
        admin_inativo = Usuario.objects.create_user(
            email='admin-inativo@perfis.test', nome='Admin inativo', perfil=Usuario.Perfil.ADMINISTRADOR,
            is_active=False,
        )
        admin_papel = Usuario.objects.create_user(
            email='admin-papel@perfis.test', nome='Admin papel', perfil=Usuario.Perfil.ADMINISTRADOR,
        )
        resposta = self.client.post(reverse('accounts:cadastro'), self.cadastro_hemo_real())
        self.assertEqual(resposta.status_code, 302)
        novo = Usuario.objects.get(email='novo-hemocentro@perfis.test')
        self.assertEqual(novo.status_validacao, Usuario.StatusValidacaoHemocentro.PENDENTE)
        self.assertEqual(set(Notificacao.objects.values_list('usuario_id', flat=True)), {
            self.usuario(Usuario.Perfil.ADMINISTRADOR).pk, admin_papel.pk,
        })
        self.assertFalse(admin_inativo.notificacoes.exists())
        self.assertFalse(novo.notificacoes.exists())
        self.assertTrue(all(aviso.url_destino == reverse('accounts:painel_aprovacao_hemocentros')
                            for aviso in Notificacao.objects.all()))

    def test_falha_no_cadastro_reverte_conta_consentimento_e_notificacoes(self):
        with patch('accounts.views.ConsentimentoLGPD.objects.create', side_effect=RuntimeError('falha simulada')):
            with self.assertRaises(RuntimeError):
                self.client.post(reverse('accounts:cadastro'), self.cadastro_hemo_real())
        self.assertFalse(Usuario.objects.filter(email='novo-hemocentro@perfis.test').exists())
        self.assertFalse(Notificacao.objects.exists())
        self.assertFalse(ConsentimentoLGPD.objects.exists())

    def test_solicitacao_real_notifica_so_hemocentro_destino_sem_dados_clinicos(self):
        pedido = criar_pedido_pendente(dados=self.dados_pedido_real(), solicitante=self.usuario(Usuario.Perfil.RECEPTOR))
        aviso = Notificacao.objects.get()
        self.assertEqual(aviso.usuario_id, pedido.hemocentro_destino_id)
        self.assertEqual(aviso.pedido_id, pedido.pk)
        self.assertEqual(aviso.url_destino, reverse('accounts:painel_pedidos_hemocentro'))
        self.assertNotIn('PACIENTE_NAO_NOTIFICAR', aviso.mensagem)
        self.assertNotIn('DESCRICAO_CLINICA_NAO_NOTIFICAR', aviso.mensagem)
        self.assertFalse(self.outro_hemo.notificacoes.exists())
        self.assertFalse(pedido.solicitante.notificacoes.exists())

    def test_decisoes_reais_notificam_solicitante_correto_e_preservam_privacidade(self):
        pedido = criar_pedido_pendente(dados=self.dados_pedido_real(), solicitante=self.usuario(Usuario.Perfil.RECEPTOR))
        hemo = self.usuario(Usuario.Perfil.HEMOCENTRO)
        for decidir in (solicitar_correcao_pedido, recusar_pedido, aprovar_pedido):
            with self.subTest(decisao=decidir.__name__):
                anteriores = pedido.solicitante.notificacoes.count()
                decidir(pedido=pedido, moderador=hemo, motivo='MOTIVO_CLINICO_NAO_NOTIFICAR')
                pedido.refresh_from_db()
                self.assertEqual(pedido.solicitante.notificacoes.count(), anteriores + 1)
                aviso = pedido.solicitante.notificacoes.latest('pk')
                self.assertEqual(aviso.pedido_id, pedido.pk)
                self.assertIn(pedido.get_status_display(), aviso.mensagem)
                self.assertEqual(aviso.url_destino, reverse('accounts:minhas_solicitacoes'))
                self.assertNotIn('MOTIVO_CLINICO_NAO_NOTIFICAR', aviso.mensagem)
                self.assertFalse(self.outro.notificacoes.exists())

    def test_decisao_nao_autorizada_nao_muda_pedido_nem_emite_aviso(self):
        pedido = criar_pedido_pendente(dados=self.dados_pedido_real(), solicitante=self.usuario(Usuario.Perfil.RECEPTOR))
        contagem = Notificacao.objects.count()
        with self.assertRaises(PermissionDenied):
            aprovar_pedido(pedido=pedido, moderador=self.outro_hemo)
        pedido.refresh_from_db()
        self.assertEqual(pedido.status, PedidoSangue.Status.ENVIADA)
        self.assertEqual(Notificacao.objects.count(), contagem)
        self.assertFalse(pedido.validacoes.exists())

    def test_falha_na_decisao_reverte_status_historico_e_aviso(self):
        pedido = criar_pedido_pendente(dados=self.dados_pedido_real(), solicitante=self.usuario(Usuario.Perfil.RECEPTOR))
        contagem = Notificacao.objects.count()
        with patch('accounts.validacao_pedido.registrar_auditoria', side_effect=RuntimeError('falha simulada')):
            with self.assertRaises(RuntimeError):
                aprovar_pedido(pedido=pedido, moderador=self.usuario(Usuario.Perfil.HEMOCENTRO))
        pedido.refresh_from_db()
        self.assertEqual(pedido.status, PedidoSangue.Status.ENVIADA)
        self.assertIsNone(pedido.publicado_por_id)
        self.assertEqual(Notificacao.objects.count(), contagem)
        self.assertFalse(pedido.validacoes.exists())

    def test_validacoes_institucionais_reais_notificam_so_instituicao_analisada(self):
        hemo = self.usuario(Usuario.Perfil.HEMOCENTRO)
        admin = self.usuario(Usuario.Perfil.ADMINISTRADOR)
        for decidir in (solicitar_correcao_hemocentro, recusar_hemocentro, aprovar_hemocentro):
            with self.subTest(decisao=decidir.__name__):
                anteriores = hemo.notificacoes.count()
                validacao = decidir(hemocentro=hemo, admin=admin, parecer='PARECER_PRIVADO_NAO_NOTIFICAR')
                self.assertEqual(hemo.notificacoes.count(), anteriores + 1)
                aviso = hemo.notificacoes.latest('pk')
                self.assertIn(validacao.get_status_display(), aviso.mensagem)
                self.assertNotIn('PARECER_PRIVADO_NAO_NOTIFICAR', aviso.mensagem)
                self.assertEqual(aviso.url_destino, reverse('accounts:perfil'))
                self.assertFalse(self.outro_hemo.notificacoes.exists())

    def test_falha_na_validacao_institucional_reverte_status_historico_e_aviso(self):
        hemo = self.usuario(Usuario.Perfil.HEMOCENTRO)
        status_original = hemo.status_validacao
        with patch('accounts.validacao_hemocentro.registrar_auditoria', side_effect=RuntimeError('falha simulada')):
            with self.assertRaises(RuntimeError):
                recusar_hemocentro(hemocentro=hemo, admin=self.usuario(Usuario.Perfil.ADMINISTRADOR))
        hemo.refresh_from_db()
        self.assertEqual(hemo.status_validacao, status_original)
        self.assertFalse(hemo.validacoes_hemocentro.exists())
        self.assertFalse(hemo.notificacoes.exists())
