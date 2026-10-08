"""

RESUMO DO ARQUIVO
=================
Testes automatizados executam o fluxo sem abrir o navegador. Cada teste usa um
banco temporario e e isolado dos demais.

Os testes abaixo verificam o minimo mais importante desta entrega:

1. cadastro cria conta, hash de senha e consentimento;
2. login aceita e-mail e senha corretos;
3. visitante acessa busca publica, estoque geral e pedidos ativos;
4. dashboard redireciona visitantes para o login;
5. perfis cadastrados recebem paineis proprios.

Execute com: ``python manage.py test``.


Os testes verificam:
- novo Hemocentro inicia como PENDENTE;
- administrador consegue aprovar, recusar ou solicitar correcao;
- cada decisao gera historico;
- usuario comum nao pode executar a decisao;
- Hemocentro nao aprovado nao consegue publicar;
- Hemocentro aprovado pode seguir para a rotina de publicacao.
"""

from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse

from .models import AuditoriaAcaoCritica, Usuario, ValidacaoHemocentro
from .validacao_hemocentro import (
    aprovar_hemocentro,
    hemocentro_aprovado,
    recusar_hemocentro,
    solicitar_correcao_hemocentro,
    validar_publicacao_hemocentro,
)


class ValidacaoHemocentroTests(TestCase):
    """Testes principais do UC_07."""

    def criar_usuario(
        self,
        *,
        email,
        nome,
        perfil,
        is_staff=False,
        is_superuser=False,
    ):
        """Cria usuario usando o manager real do projeto."""

        return Usuario.objects.create_user(
            email=email,
            password="SenhaForte123!",
            nome=nome,
            perfil=perfil,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )

    def setUp(self):
        """Prepara um administrador e um Hemocentro para cada teste."""

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

    def test_hemocentro_inicia_pendente(self):
        """Conta de Hemocentro nova deve aguardar analise."""

        self.assertEqual(
            self.hemocentro.status_validacao,
            Usuario.StatusValidacaoHemocentro.PENDENTE,
        )
        self.assertFalse(hemocentro_aprovado(self.hemocentro))

    def test_admin_aprova_e_cria_historico(self):
        """Aprovacao altera status, cria historico e gera auditoria."""

        validacao = aprovar_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.admin,
        )

        self.hemocentro.refresh_from_db()

        self.assertEqual(
            self.hemocentro.status_validacao,
            Usuario.StatusValidacaoHemocentro.APROVADO,
        )
        self.assertEqual(validacao.status, Usuario.StatusValidacaoHemocentro.APROVADO)
        self.assertEqual(
            ValidacaoHemocentro.objects.filter(hemocentro=self.hemocentro).count(),
            1,
        )
        self.assertTrue(
            AuditoriaAcaoCritica.objects.filter(
                acao=AuditoriaAcaoCritica.Acao.APROVACAO_HEMOCENTRO,
                usuario=self.admin,
                alvo_id=str(self.hemocentro.pk),
            ).exists()
        )

    def test_admin_recusa(self):
        """Recusa altera o status e guarda o parecer."""

        validacao = recusar_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.admin,
            parecer="CNPJ nao confere com os documentos enviados.",
        )

        self.hemocentro.refresh_from_db()

        self.assertEqual(
            self.hemocentro.status_validacao,
            Usuario.StatusValidacaoHemocentro.RECUSADO,
        )
        self.assertEqual(
            validacao.parecer,
            "CNPJ nao confere com os documentos enviados.",
        )

    def test_admin_solicita_correcao(self):
        """Solicitacao de correcao coloca o cadastro em CORRECAO."""

        solicitar_correcao_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.admin,
            parecer="Atualize telefone e endereco.",
        )

        self.hemocentro.refresh_from_db()

        self.assertEqual(
            self.hemocentro.status_validacao,
            Usuario.StatusValidacaoHemocentro.CORRECAO,
        )

    def test_usuario_comum_nao_pode_validar(self):
        """Somente administrador pode registrar a decisao."""

        usuario_comum = self.criar_usuario(
            email="doador@elo.test",
            nome="Doador",
            perfil=Usuario.Perfil.DOADOR,
        )

        with self.assertRaises(PermissionDenied):
            aprovar_hemocentro(
                hemocentro=self.hemocentro,
                admin=usuario_comum,
            )

    def test_hemocentro_nao_aprovado_nao_publica(self):
        """Pendente, recusado e correcao devem bloquear publicacao."""

        for status in (
            Usuario.StatusValidacaoHemocentro.PENDENTE,
            Usuario.StatusValidacaoHemocentro.RECUSADO,
            Usuario.StatusValidacaoHemocentro.CORRECAO,
        ):
            self.hemocentro.status_validacao = status
            self.hemocentro.save(update_fields=["status_validacao"])

            with self.assertRaises(PermissionDenied):
                validar_publicacao_hemocentro(self.hemocentro)

    def test_hemocentro_aprovado_pode_publicar(self):
        """Status aprovado libera a regra de publicacao."""

        aprovar_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.admin,
        )
        self.hemocentro.refresh_from_db()

        self.assertTrue(validar_publicacao_hemocentro(self.hemocentro))

    def test_dashboard_hemocentro_mostra_status_sem_link_de_aprovacao(self):
        """Hemocentro ve seu status, mas nao acessa validacao administrativa."""

        self.client.force_login(self.hemocentro)

        resposta = self.client.get(reverse("accounts:dashboard"))

        self.assertContains(resposta, "Status da validação institucional")
        self.assertContains(resposta, "Pendente")
        self.assertNotContains(resposta, "Gestão de Hemocentros")
        self.assertNotContains(resposta, "Acessar aprovação de Hemocentros")

    def test_dashboard_admin_nao_mostra_validacao_fora_do_admin(self):
        """Aprovacao de Hemocentro deve ficar somente dentro do Django Admin."""

        self.client.force_login(self.admin)

        resposta = self.client.get(reverse("accounts:dashboard"))

        self.assertNotContains(resposta, "Gestão de Hemocentros")
        self.assertNotContains(resposta, "Acessar aprovação de Hemocentros")

    def test_dashboard_receptor_mostra_publicacao_de_pedido(self):
        """Receptor/Solicitante deve ter acesso ao atalho de publicar pedido."""

        receptor = self.criar_usuario(
            email="receptor@elo.test",
            nome="Receptor Elo",
            perfil=Usuario.Perfil.RECEPTOR,
        )

        self.client.force_login(receptor)

        resposta = self.client.get(reverse("accounts:dashboard"))

        self.assertContains(resposta, "Pedidos ativos")
        self.assertContains(resposta, "Consultar pedidos ativos")
        self.assertContains(resposta, "Solicitar pedido de sangue")

    def test_dashboard_admin_mostra_validacao_de_pedidos_sem_publicacao(self):
        """Administrador valida pedidos, mas nao publica como solicitante."""

        self.client.force_login(self.admin)

        resposta = self.client.get(reverse("accounts:dashboard"))

        self.assertContains(resposta, "Pedidos ativos")
        self.assertContains(resposta, "Gestao de pedidos")
        self.assertContains(resposta, "Acessar validacao de pedidos")
        self.assertNotContains(resposta, "Solicitar pedido de sangue")

    def test_urls_comuns_de_validacao_foram_removidas(self):
        """Links diretos antigos de validacao nao devem funcionar no site comum."""

        self.client.force_login(self.admin)

        resposta = self.client.get("/hemocentros/validacao/")

        self.assertEqual(resposta.status_code, 404)


class AuditoriaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = Usuario.objects.create_superuser(
            email='auditoria.admin@elo.test', password='SenhaForte123!',
            nome='Administrador', perfil=Usuario.Perfil.ADMINISTRADOR,
        )
        cls.doador = Usuario.objects.create_user(
            email='auditoria.doador@elo.test', password='SenhaForte123!',
            nome='Doador', perfil=Usuario.Perfil.DOADOR,
        )

    def test_acesso_bloqueado_registrado(self):
        self.client.force_login(self.doador)
        resposta = self.client.get(reverse('accounts:painel_validacao_pedidos'))
        self.assertEqual(resposta.status_code, 403)
        registro = AuditoriaAcaoCritica.objects.get()
        self.assertEqual(registro.usuario, self.doador)
        self.assertEqual(registro.resultado, AuditoriaAcaoCritica.Resultado.BLOQUEADO)
        self.assertEqual(registro.metadados['evento'], 'TENTATIVA_ACESSO')

    def test_acesso_a_triagem_registra_alvo_sem_respostas(self):
        from .models import Triagem
        triagem = Triagem.objects.create(usuario=self.doador, modalidade=Triagem.Modalidade.EXTENSA,
                                        status=Triagem.Status.CONCLUIDA,
                                        mensagem_resultado='CONTEUDO_CLINICO_PRIVADO')
        self.client.force_login(self.doador)
        resposta = self.client.get(reverse('accounts:triagem_resultado', kwargs={'id_triagem': triagem.pk}))
        self.assertEqual(resposta.status_code, 200)
        registro = AuditoriaAcaoCritica.objects.get()
        self.assertEqual(registro.acao, AuditoriaAcaoCritica.Acao.ACESSO_DADOS_SENSIVEIS)
        self.assertEqual(registro.metadados['parametros']['id_triagem'], triagem.pk)
        self.assertNotIn('CONTEUDO_CLINICO_PRIVADO', str(registro.metadados))

    def test_auditoria_exclusiva_administrador_e_somente_leitura(self):
        from django.contrib import admin
        from django.test import RequestFactory
        from django.contrib.auth.models import Permission
        modelo_admin = admin.site._registry[AuditoriaAcaoCritica]
        request = RequestFactory().get('/admin/')
        request.user = self.admin
        self.assertTrue(modelo_admin.has_view_permission(request))
        self.assertFalse(modelo_admin.has_add_permission(request))
        self.assertFalse(modelo_admin.has_change_permission(request))
        self.assertFalse(modelo_admin.has_delete_permission(request))
        self.doador.is_staff = True
        self.doador.save()
        self.doador.user_permissions.add(Permission.objects.get(codename='view_auditoriaacaocritica'))
        request.user = Usuario.objects.get(pk=self.doador.pk)
        self.assertFalse(modelo_admin.has_view_permission(request))
        self.assertFalse(modelo_admin.has_module_permission(request))

    def test_suspensao_registrada_sem_duplicar_dados_pessoais(self):
        from django.contrib import admin
        from django.test import RequestFactory
        request = RequestFactory().post('/admin/')
        request.user = self.admin
        self.doador.is_active = False
        self.doador.nome = 'Nome atualizado'
        admin.site._registry[Usuario].save_model(request, self.doador, None, True)
        registro = AuditoriaAcaoCritica.objects.get()
        self.assertEqual(registro.metadados['evento'], 'SUSPENSAO_USUARIO')
        self.assertEqual(registro.metadados['alteracoes']['is_active'], {'antes': 'True', 'depois': 'False'})
        self.assertIn('nome', registro.metadados['campos_alterados'])
        self.assertNotIn('Nome atualizado', str(registro.metadados))

    def test_login_suspeito_nao_afirma_bloqueio(self):
        from .signals import auditar_login_falho
        from django.test import RequestFactory
        request = RequestFactory().post('/login/')
        for _ in range(5):
            auditar_login_falho(None, {'username': 'tentativa@elo.test', 'password': 'SEGREDO'}, request)
        registro = AuditoriaAcaoCritica.objects.get(acao=AuditoriaAcaoCritica.Acao.LOGIN_SUSPEITO)
        self.assertEqual(registro.resultado, AuditoriaAcaoCritica.Resultado.FALHA)
        self.assertNotIn('SEGREDO', str(registro.metadados))

    def test_sanitizacao_recursiva(self):
        from .auditoria import registrar_auditoria
        registro = registrar_auditoria(acao=AuditoriaAcaoCritica.Acao.MODERACAO,
            metadados={'dados': [{'password': 'SEGREDO', 'TOKEN': 'SEGREDO', 'evento': 'teste'}]})
        self.assertNotIn('SEGREDO', str(registro.metadados))
        self.assertEqual(registro.metadados['dados'][0]['evento'], 'teste')

    def test_ip_nao_confia_em_cabecalho_do_cliente(self):
        from .auditoria import obter_ip
        from django.test import RequestFactory
        request = RequestFactory().get('/login/', REMOTE_ADDR='127.0.0.1', HTTP_X_FORWARDED_FOR='IP_FORJADO')
        self.assertEqual(obter_ip(request), '127.0.0.1')
        request.META['REMOTE_ADDR'] = 'IP_INVALIDO'
        self.assertIsNone(obter_ip(request))
