from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse

from .forms import CadastroUsuarioForm
from .models import (
    ConsentimentoLGPD,
    Notificacao,
    PedidoSangue,
    Triagem,
    Usuario,
)
from .triagem_servico import atualizar_tipo_sanguineo_do_usuario
from .validacao_hemocentro import aprovar_hemocentro
from .validacao_pedido import aprovar_pedido, criar_pedido_pendente


class FluxoCadastroTriagemPedidosTests(TestCase):
    def usuario(self, email, perfil, **extras):
        return Usuario.objects.create_user(
            email=email,
            password="SenhaForte123!",
            nome=extras.pop("nome", perfil.title()),
            perfil=perfil,
            **extras,
        )

    def setUp(self):
        self.admin = self.usuario(
            "admin@elo.test",
            Usuario.Perfil.ADMINISTRADOR,
        )
        self.doador = self.usuario(
            "doador@elo.test",
            Usuario.Perfil.DOADOR,
        )
        self.receptor = self.usuario(
            "receptor@elo.test",
            Usuario.Perfil.RECEPTOR,
        )
        self.observador = self.usuario(
            "observador@elo.test",
            Usuario.Perfil.OBSERVADOR,
        )
        self.hemocentro = self.usuario(
            "hemocentro@elo.test",
            Usuario.Perfil.HEMOCENTRO,
            cidade="Belo Horizonte",
        )

        aprovar_hemocentro(
            hemocentro=self.hemocentro,
            admin=self.admin,
        )
        self.hemocentro.refresh_from_db()

    def dados_solicitacao(self):
        return {
            "nome_solicitante": "Pessoa solicitante",
            "contato": "solicitante@elo.test",
            "para_quem": PedidoSangue.ParaQuem.MIM,
            "hemocentro_destino": self.hemocentro.pk,
            "titulo": "Necessidade de sangue",
            "tipo_sanguineo": "O-",
            "urgencia": PedidoSangue.Urgencia.MEDIA,
            "cidade": "Belo Horizonte",
            "nome_paciente": "Paciente",
            "descricao": (
                "Necessidade de doadores para atendimento hospitalar."
            ),
            "justificativa_urgencia": "",
            "informacoes_complementares": (
                "Retorno pelo contato informado."
            ),
        }

    def test_cadastro_nao_permite_admin_e_exige_consentimento(self):
        resposta = self.client.post(
            reverse("accounts:cadastro"),
            {
                "nome": "Nova pessoa",
                "email": "nova@elo.test",
                "perfil": Usuario.Perfil.OBSERVADOR,
                "password1": "SenhaForte123!",
                "password2": "SenhaForte123!",
                "aceite_lgpd": "",
            },
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(
            Usuario.objects.filter(
                email="nova@elo.test"
            ).exists()
        )

        self.assertNotIn(
            Usuario.Perfil.ADMINISTRADOR,
            dict(
                CadastroUsuarioForm().fields["perfil"].choices
            ),
        )

    def test_cadastro_valido_grava_senha_hash_e_consentimento(self):
        resposta = self.client.post(
            reverse("accounts:cadastro"),
            {
                "nome": "Doador cadastrado",
                "email": "cadastro@elo.test",
                "perfil": Usuario.Perfil.DOADOR,
                "cpf": "12345678901",
                "data_nascimento": "1990-01-01",
                "password1": "SenhaForte123!",
                "password2": "SenhaForte123!",
                "aceite_lgpd": "on",
            },
        )

        self.assertRedirects(
            resposta,
            reverse("accounts:dashboard"),
        )

        usuario = Usuario.objects.get(
            email="cadastro@elo.test"
        )

        self.assertTrue(
            usuario.check_password("SenhaForte123!")
        )
        self.assertNotEqual(
            usuario.password,
            "SenhaForte123!",
        )

        self.assertTrue(
            ConsentimentoLGPD.objects.filter(
                usuario=usuario,
                tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL,
                aceito=True,
            ).exists()
        )

    def test_cadastro_de_hemocentro_inicia_pendente_e_nao_libera_estoque(
        self,
    ):
        resposta = self.client.post(
            reverse("accounts:cadastro"),
            {
                "nome": "Hemocentro cadastrado",
                "email": "novo-hemocentro@elo.test",
                "perfil": Usuario.Perfil.HEMOCENTRO,
                "cnpj": "12345678000195",
                "cidade": "Belo Horizonte",
                "estado": "MG",
                "password1": "SenhaForte123!",
                "password2": "SenhaForte123!",
                "aceite_lgpd": "on",
            },
        )

        self.assertRedirects(
            resposta,
            reverse("accounts:dashboard"),
        )

        hemocentro = Usuario.objects.get(
            email="novo-hemocentro@elo.test"
        )

        self.assertEqual(
            hemocentro.status_validacao,
            Usuario.StatusValidacaoHemocentro.PENDENTE,
        )

        estoque = self.client.get(
            reverse("accounts:estoque_hemocentro")
        )

        self.assertEqual(estoque.status_code, 403)

    def test_login_bloqueia_conta_suspensa(self):
        self.doador.suspensa = True
        self.doador.save(update_fields=["suspensa"])

        resposta = self.client.post(
            reverse("accounts:login"),
            {
                "username": self.doador.email,
                "password": "SenhaForte123!",
            },
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertNotIn(
            "_auth_user_id",
            self.client.session,
        )

    def test_triagem_exige_aceite_explicito(self):
        self.client.force_login(self.doador)

        url = reverse(
            "accounts:triagem_iniciar",
            kwargs={"modalidade": "extensa"},
        )

        self.client.post(url)

        self.assertFalse(
            Triagem.objects.filter(
                usuario=self.doador
            ).exists()
        )

        resposta = self.client.post(
            url,
            {"aceite_termo": "on"},
        )

        self.assertEqual(resposta.status_code, 302)

        self.assertTrue(
            ConsentimentoLGPD.objects.filter(
                usuario=self.doador,
                tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM,
            ).exists()
        )

    def test_solicitacao_nao_publica_e_hemocentro_publica(self):
        self.client.force_login(self.receptor)
        resposta = self.client.post(
            reverse("accounts:pedido_publicar"),
            self.dados_solicitacao(),
        )

        self.assertEqual(resposta.status_code, 302)

        pedido = PedidoSangue.objects.get()

        self.assertEqual(
            pedido.status,
            PedidoSangue.Status.ENVIADA,
        )

        with self.assertRaises(PermissionDenied):
            aprovar_pedido(
                pedido=pedido,
                moderador=self.admin,
            )

        aprovar_pedido(
            pedido=pedido,
            moderador=self.hemocentro,
        )

        pedido.refresh_from_db()

        self.assertEqual(
            pedido.status,
            PedidoSangue.Status.PUBLICADA,
        )
        self.assertEqual(
            pedido.publicado_por,
            self.hemocentro,
        )

    def test_observador_pode_solicitar_mas_nao_analisar(self):
        self.client.force_login(self.observador)

        resposta = self.client.get(
            reverse("accounts:painel_pedidos_hemocentro")
        )

        self.assertEqual(resposta.status_code, 403)

    def test_receptor_acompanha_somente_suas_solicitacoes(self):
        pedido = criar_pedido_pendente(
            dados={
                **self.dados_solicitacao(),
                "contato": "receptor@elo.test",
            },
            solicitante=self.receptor,
        )

        self.client.force_login(self.receptor)

        resposta = self.client.get(
            reverse("accounts:minhas_solicitacoes")
        )

        self.assertContains(resposta, str(pedido.pk))
        self.assertNotContains(resposta, "outra-pessoa")

    def test_tipo_sanguineo_confirmado_nao_e_sobrescrito_pela_triagem(
        self,
    ):
        self.doador.tipo_sanguineo = "A+"
        self.doador.tipo_sanguineo_confirmado = True
        self.doador.save(
            update_fields=[
                "tipo_sanguineo",
                "tipo_sanguineo_confirmado",
            ]
        )

        triagem = Triagem.objects.create(
            usuario=self.doador
        )

        atualizar_tipo_sanguineo_do_usuario(
            triagem,
            {"codigos": ["O+"]},
        )

        self.doador.refresh_from_db()

        self.assertEqual(
            self.doador.tipo_sanguineo,
            "A+",
        )

    def test_publicacao_notifica_somente_doador_apto_compativel(self):
        from .compatibilidade import atualizar_preferencia_convocacao
        atualizar_preferencia_convocacao(self.doador, True)
        self.doador.tipo_sanguineo = "O-"
        self.doador.save(
            update_fields=["tipo_sanguineo"]
        )

        Triagem.objects.create(
            usuario=self.doador,
            status=Triagem.Status.CONCLUIDA,
            resultado=Triagem.Resultado.APTO,
        )

        pedido = criar_pedido_pendente(
            dados=self.dados_solicitacao(),
            solicitante=self.receptor,
        )

        aprovar_pedido(
            pedido=pedido,
            moderador=self.hemocentro,
        )

        self.assertTrue(
            Notificacao.objects.filter(
                usuario=self.doador,
                pedido=pedido,
                tipo=Notificacao.Tipo.PEDIDO_COMPATIVEL,
            ).exists()
        )

class ConvocacaoCompatibilidadeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        from .models import Estoque
        cls.hemocentro = Usuario.objects.create_user(
            email='hemo.convocacao@elo.test', nome='Hemocentro', perfil=Usuario.Perfil.HEMOCENTRO,
            status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO,
            cidade='Belo Horizonte',
        )
        cls.estoque = Estoque.objects.create(hemocentro=cls.hemocentro, tipo_sanguineo='O-',
            quantidade_bolsas=0, nivel_minimo=10, nivel_critico=5, status_calculado=Estoque.StatusCalculado.CRITICO)
        cls.pedido = PedidoSangue.objects.create(hemocentro_destino=cls.hemocentro,
            nome_solicitante='Solicitante', contato='contato@elo.test', para_quem=PedidoSangue.ParaQuem.MIM,
            tipo_sanguineo='O-', cidade='Belo Horizonte', urgencia=PedidoSangue.Urgencia.MEDIA,
            descricao='Pedido publicado para testar convocacao.', status=PedidoSangue.Status.PUBLICADA)

    def doador(self, nome, **extras):
        usuario = Usuario.objects.create_user(email=nome+'@convocacao.test', nome=nome,
            perfil=extras.pop('perfil', Usuario.Perfil.DOADOR), tipo_sanguineo=extras.pop('tipo_sanguineo', 'O-'),
            **extras)
        Triagem.objects.create(usuario=usuario, status=Triagem.Status.CONCLUIDA,
            resultado=Triagem.Resultado.APTO)
        ConsentimentoLGPD.objects.create(usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
            versao_termo='1.0', aceito=True)
        return usuario

    def emitir(self, origem):
        from .estoque import criar_notificacoes_para_doadores_compativeis
        from .pedidos import criar_notificacoes_para_pedido
        from .models import Estoque
        if origem == 'estoque':
            return criar_notificacoes_para_doadores_compativeis(estoque=self.estoque,
                status_calculado=Estoque.StatusCalculado.CRITICO)
        return criar_notificacoes_para_pedido(pedido=self.pedido)

    def test_ambos_fluxos_exigem_todos_os_criterios(self):
        from django.utils import timezone
        from datetime import timedelta
        apto = self.doador('apto')
        self.doador('incompativel', tipo_sanguineo='A+')
        self.doador('suspenso', suspensa=True)
        self.doador('inativo', is_active=False)
        self.doador('preferencia_desativada', aceita_notificacoes_pedidos=False)
        self.doador('receptor', perfil=Usuario.Perfil.RECEPTOR)
        revogado = self.doador('revogado')
        revogado.consentimentos_lgpd.update(revogado_em=timezone.now())
        recusou = self.doador('recusou')
        recusou.consentimentos_lgpd.update(aceito=False)
        sem_consentimento = self.doador('sem_consentimento')
        sem_consentimento.consentimentos_lgpd.all().delete()
        versao_antiga = self.doador('versao_antiga')
        versao_antiga.consentimentos_lgpd.update(versao_termo='0.9')
        futuro = self.doador('futuro')
        futuro.triagens.update(data_liberacao=timezone.localdate()+timedelta(days=1))
        sem_triagem = self.doador('sem_triagem')
        sem_triagem.triagens.all().delete()
        inapto = self.doador('inapto')
        Triagem.objects.create(usuario=inapto, status=Triagem.Status.CONCLUIDA,
            resultado=Triagem.Resultado.INAPTO_TEMPORARIO, finalizada_em=timezone.now())
        for origem in ('estoque', 'pedido'):
            with self.subTest(origem=origem):
                self.assertEqual(self.emitir(origem), 1)
                self.assertEqual(list(Notificacao.objects.values_list('usuario_id', flat=True)), [apto.pk])
                Notificacao.objects.all().delete()

    def test_limite_soma_estoque_e_pedido_mesmo_depois_de_lido(self):
        from datetime import timedelta
        from django.utils import timezone
        self.doador('frequencia')
        self.assertEqual(self.emitir('estoque'), 1)
        Notificacao.objects.update(lida=True)
        self.assertEqual(self.emitir('pedido'), 0)
        Notificacao.objects.update(criada_em=timezone.now()-timedelta(hours=25))
        self.assertEqual(self.emitir('pedido'), 1)
        self.assertEqual(self.emitir('pedido'), 0)

    def test_pedido_pendente_nao_convoca(self):
        self.doador('pendente')
        self.pedido.status = PedidoSangue.Status.ENVIADA
        self.assertEqual(self.emitir('pedido'), 0)

    def test_preferencia_no_painel_registra_aceite_e_revogacao(self):
        from .models import AuditoriaAcaoCritica
        usuario = self.doador('painel')
        usuario.consentimentos_lgpd.all().delete()
        self.client.force_login(usuario)
        url = reverse('accounts:dashboard')
        self.assertContains(self.client.get(url), 'Alertas de doação')
        self.assertEqual(self.client.post(url, {'aceita_convocacoes': 'on'}).status_code, 302)
        consentimento = usuario.consentimentos_lgpd.get(tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES)
        self.assertTrue(consentimento.aceito)
        self.assertIsNone(consentimento.revogado_em)
        self.assertEqual(self.emitir('pedido'), 1)
        self.assertEqual(self.client.post(url, {}).status_code, 302)
        consentimento.refresh_from_db()
        usuario.refresh_from_db()
        self.assertFalse(usuario.aceita_notificacoes_pedidos)
        self.assertFalse(consentimento.aceito)
        self.assertIsNotNone(consentimento.revogado_em)
        self.assertTrue(AuditoriaAcaoCritica.objects.filter(metadados__evento='PREFERENCIA_CONVOCACAO').exists())
        Notificacao.objects.all().delete()
        self.assertEqual(self.emitir('estoque'), 0)

    def test_outro_perfil_nao_altera_preferencia(self):
        usuario = Usuario.objects.create_user(email='observador@convocacao.test', nome='Observador',
            perfil=Usuario.Perfil.OBSERVADOR)
        self.client.force_login(usuario)
        self.assertEqual(self.client.post(reverse('accounts:dashboard'), {'aceita_convocacoes': 'on'}).status_code, 403)
        self.assertFalse(usuario.consentimentos_lgpd.filter(tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES).exists())

    def test_cadastro_autorizacao_e_opcional_e_explicita(self):
        for aceita in (False, True):
            with self.subTest(aceita=aceita):
                self.client.logout()
                dados = {'nome': 'Doador', 'email': f'cadastro{int(aceita)}@convocacao.test',
                    'perfil': Usuario.Perfil.DOADOR, 'cpf': '12345678901' if not aceita else '12345678902', 'data_nascimento': '1990-01-01',
                    'password1': 'SenhaForte123!', 'password2': 'SenhaForte123!', 'aceite_lgpd': 'on'}
                if aceita:
                    dados['aceita_notificacoes_pedidos'] = 'on'
                self.assertEqual(self.client.post(reverse('accounts:cadastro'), dados).status_code, 302)
                usuario = Usuario.objects.get(email=dados['email'])
                self.assertEqual(usuario.aceita_notificacoes_pedidos, aceita)
                self.assertEqual(usuario.consentimentos_lgpd.get(tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES).aceito, aceita)

    def test_publicacao_alternativa_tambem_convoca(self):
        from .forms import PedidoSangueForm
        from .pedidos import publicar_pedido
        self.doador('alternativa')
        form = PedidoSangueForm({'nome_solicitante': 'Solicitante', 'contato': 'contato@elo.test',
            'para_quem': PedidoSangue.ParaQuem.MIM, 'hemocentro_destino': self.hemocentro.pk,
            'titulo': 'Pedido alternativo', 'tipo_sanguineo': 'O-', 'urgencia': PedidoSangue.Urgencia.MEDIA,
            'cidade': 'Belo Horizonte', 'descricao': 'Precisamos de doadores para atendimento hospitalar.'})
        self.assertTrue(form.is_valid(), form.errors)
        pedido = publicar_pedido(self.hemocentro, form)
        self.assertTrue(Notificacao.objects.filter(pedido=pedido).exists())

    def test_compatibilidade_seleciona_os_tipos_da_tabela(self):
        from .compatibilidade import TIPOS_SANGUINEOS, COMPATIBILIDADE_RECEBIMENTO, doadores_aptos_para_convocacao
        for i, tipo in enumerate(TIPOS_SANGUINEOS):
            self.doador(f'tipo{i}', tipo_sanguineo=tipo)
        for solicitado, esperados in COMPATIBILIDADE_RECEBIMENTO.items():
            with self.subTest(tipo=solicitado):
                encontrados = set(doadores_aptos_para_convocacao(solicitado).values_list('tipo_sanguineo', flat=True))
                self.assertEqual(encontrados, set(esperados))

    def test_limite_e_compartilhado_tambem_quando_pedido_vem_primeiro(self):
        self.doador('pedido_primeiro')
        self.assertEqual(self.emitir('pedido'), 1)
        self.assertEqual(self.emitir('estoque'), 0)

    def test_limite_configuravel_nao_remove_protecao_contra_duplicatas(self):
        from django.test import override_settings
        self.doador('limite_configuravel')
        with override_settings(CONVOCACAO_LIMITE_NOTIFICACOES=3):
            self.assertEqual(self.emitir('pedido'), 1)
            self.assertEqual(self.emitir('pedido'), 0)
            self.assertEqual(self.emitir('estoque'), 1)
            self.assertEqual(self.emitir('estoque'), 0)
