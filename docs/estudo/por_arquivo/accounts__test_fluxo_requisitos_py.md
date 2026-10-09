# accounts/test_fluxo_requisitos.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

**Arquivo original:** [accounts/test_fluxo_requisitos.py](<C:/Users/lb119/Elo/accounts/test_fluxo_requisitos.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
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

    def test_atualizacao_de_estoque_convoca_somente_quando_critico(self):
        from .estoque import registrar_movimentacao_estoque
        from .models import Estoque, EstoqueMovimentacao
        doador = self.doador('estoque_critico')
        for quantidade, status in (
            (7, Estoque.StatusCalculado.BAIXO),
            (12, Estoque.StatusCalculado.ESTAVEL),
            (5, Estoque.StatusCalculado.CRITICO),
        ):
            with self.subTest(status=status):
                registrar_movimentacao_estoque(
                    estoque=self.estoque, usuario_resp=self.hemocentro,
                    tipo_movimento=EstoqueMovimentacao.TipoMovimento.AJUSTE,
                    quantidade=quantidade, motivo='Conferencia do estoque',
                )
                self.estoque.refresh_from_db()
                self.assertEqual(self.estoque.status_calculado, status)
                self.assertEqual(Notificacao.objects.count(), int(status == Estoque.StatusCalculado.CRITICO))
        notificacao = Notificacao.objects.get()
        self.assertEqual(notificacao.usuario_id, doador.pk)
        self.assertEqual(notificacao.tipo, Notificacao.Tipo.ESTOQUE_CRITICO)

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


class CentralNotificacoesTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email='central@elo.test', nome='Receptor', perfil=Usuario.Perfil.RECEPTOR,
        )
        self.outro = Usuario.objects.create_user(
            email='outra-central@elo.test', nome='Outro', perfil=Usuario.Perfil.RECEPTOR,
        )
        self.aviso = Notificacao.objects.create(
            usuario=self.usuario, titulo='Estoque urgente', mensagem='Precisamos de doadores.',
            tipo=Notificacao.Tipo.ESTOQUE_CRITICO, url_destino=reverse('accounts:estoque_publico'),
        )
        self.client.force_login(self.usuario)
        self.url = reverse('accounts:dashboard')

    def test_leitura_persiste_sem_apagar_historico_nem_regravar_data(self):
        dados = {'acao': 'marcar_notificacao_lida', 'id_notificacao': self.aviso.pk}
        self.assertEqual(self.client.post(self.url, dados).status_code, 302)
        self.aviso.refresh_from_db()
        self.assertTrue(self.aviso.lida)
        self.assertIsNotNone(self.aviso.lida_em)
        data_leitura = self.aviso.lida_em
        self.client.post(self.url, dados)
        self.aviso.refresh_from_db()
        self.assertEqual(self.aviso.lida_em, data_leitura)
        pagina = self.client.get(self.url)
        self.assertContains(pagina, 'Estoque urgente')
        self.assertContains(pagina, 'Ver estoque')
        self.assertContains(pagina, 'Lida')
        self.assertEqual(pagina.context['notificacoes_nao_lidas'], 0)

    def test_nao_permite_marcar_notificacao_de_outro_usuario(self):
        aviso = Notificacao.objects.create(usuario=self.outro, titulo='Privada', mensagem='Privada')
        self.assertEqual(self.client.post(self.url, {
            'acao': 'marcar_notificacao_lida', 'id_notificacao': aviso.pk,
        }).status_code, 404)
        aviso.refresh_from_db()
        self.assertFalse(aviso.lida)
        self.assertNotContains(self.client.get(self.url), 'Privada')

    def test_historico_paginado_mostra_notificacoes_mais_antigas(self):
        for numero in range(11):
            Notificacao.objects.create(usuario=self.usuario, titulo=f'Aviso {numero}', mensagem='Aviso')
        pagina = self.client.get(self.url)
        self.assertEqual(len(pagina.context['notificacoes_dashboard']), 10)
        self.assertContains(pagina, 'Próxima')
        self.assertContains(self.client.get(self.url, {'pagina_notificacoes': 2}), 'Estoque urgente')

    def test_identificador_invalido_e_anonimo_nao_marcam_leitura(self):
        self.assertEqual(self.client.post(self.url, {
            'acao': 'marcar_notificacao_lida', 'id_notificacao': 'invalido',
        }).status_code, 404)
        self.client.logout()
        self.assertEqual(self.client.post(self.url, {
            'acao': 'marcar_notificacao_lida', 'id_notificacao': self.aviso.pk,
        }).status_code, 302)
        self.aviso.refresh_from_db()
        self.assertFalse(self.aviso.lida)
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### ImportFrom — linhas 1 a 1

```python
from django.core.exceptions import PermissionDenied
```

**Explicação deste trecho:**

**Linha 1 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.exceptions` os nomes `PermissionDenied`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 2 a 2

```python
from django.test import TestCase
```

**Explicação deste trecho:**

**Linha 2 — ImportFrom** (nível 0 do bloco).

Importa de `django.test` os nomes `TestCase`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 3 a 3

```python
from django.urls import reverse
```

**Explicação deste trecho:**

**Linha 3 — ImportFrom** (nível 0 do bloco).

Importa de `django.urls` os nomes `reverse`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 5 a 5

```python
from .forms import CadastroUsuarioForm
```

**Explicação deste trecho:**

**Linha 5 — ImportFrom** (nível 0 do bloco).

Importa de `.forms` os nomes `CadastroUsuarioForm`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 6 a 12

```python
from .models import (
    ConsentimentoLGPD,
    Notificacao,
    PedidoSangue,
    Triagem,
    Usuario,
)
```

**Explicação deste trecho:**

**Linha 6 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `ConsentimentoLGPD`, `Notificacao`, `PedidoSangue`, `Triagem`, `Usuario`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 13 a 13

```python
from .triagem_servico import atualizar_tipo_sanguineo_do_usuario
```

**Explicação deste trecho:**

**Linha 13 — ImportFrom** (nível 0 do bloco).

Importa de `.triagem_servico` os nomes `atualizar_tipo_sanguineo_do_usuario`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 14 a 14

```python
from .validacao_hemocentro import aprovar_hemocentro
```

**Explicação deste trecho:**

**Linha 14 — ImportFrom** (nível 0 do bloco).

Importa de `.validacao_hemocentro` os nomes `aprovar_hemocentro`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 15 a 15

```python
from .validacao_pedido import aprovar_pedido, criar_pedido_pendente
```

**Explicação deste trecho:**

**Linha 15 — ImportFrom** (nível 0 do bloco).

Importa de `.validacao_pedido` os nomes `aprovar_pedido`, `criar_pedido_pendente`. Pontos iniciais indicam importação relativa ao pacote.

### FluxoCadastroTriagemPedidosTests — linhas 18 a 353

```python
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
```

**Explicação deste trecho:**

**Linha 18 — ClassDef** (nível 0 do bloco).

Define a classe `FluxoCadastroTriagemPedidosTests` herdando de `TestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 18:

**Linha 19 — FunctionDef** (nível 1 do bloco).

Define `usuario(self, email, perfil, **extras)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 19:

**Linha 20 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `Usuario.objects.create_user`; argumentos nomeados: `email=email`, `password='SenhaForte123!'`, `nome=extras.pop('nome', perfil.title())`, `perfil=perfil`, `**=extras` ao chamador.

**Linha 28 — FunctionDef** (nível 1 do bloco).

Define `setUp(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 28:

**Linha 29 — Assign** (nível 2 do bloco).

Associa `self.admin` a a chamada `self.usuario`; argumentos posicionais: `'admin@elo.test'`, `Usuario.Perfil.ADMINISTRADOR`.


**Linha 33 — Assign** (nível 2 do bloco).

Associa `self.doador` a a chamada `self.usuario`; argumentos posicionais: `'doador@elo.test'`, `Usuario.Perfil.DOADOR`.


**Linha 37 — Assign** (nível 2 do bloco).

Associa `self.receptor` a a chamada `self.usuario`; argumentos posicionais: `'receptor@elo.test'`, `Usuario.Perfil.RECEPTOR`.


**Linha 41 — Assign** (nível 2 do bloco).

Associa `self.observador` a a chamada `self.usuario`; argumentos posicionais: `'observador@elo.test'`, `Usuario.Perfil.OBSERVADOR`.


**Linha 45 — Assign** (nível 2 do bloco).

Associa `self.hemocentro` a a chamada `self.usuario`; argumentos posicionais: `'hemocentro@elo.test'`, `Usuario.Perfil.HEMOCENTRO`; argumentos nomeados: `cidade='Belo Horizonte'`.

- `cidade='Belo Horizonte'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 51 — Expr** (nível 2 do bloco).

Executa a chamada `aprovar_hemocentro`; argumentos nomeados: `hemocentro=self.hemocentro`, `admin=self.admin`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 55 — Expr** (nível 2 do bloco).

Executa a chamada `self.hemocentro.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 57 — FunctionDef** (nível 1 do bloco).

Define `dados_solicitacao(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 57:

**Linha 58 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve um dicionário de 12 entradas; as chaves dão nome aos valores associados ao chamador.

**Linha 77 — FunctionDef** (nível 1 do bloco).

Define `test_cadastro_nao_permite_admin_e_exige_consentimento(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: cadastro nao permite admin e exige consentimento.

Bloco `body` da linha 77:

**Linha 78 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:cadastro')`, `{'nome': 'Nova pessoa', 'email': 'nova@elo.test', 'perfil': Usuario.Perfil.OBSERVADOR, 'password1': 'SenhaForte123!', 'password2': 'SenhaForte123!', 'aceite_lgpd': ''}`.


**Linha 90 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `200`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 91 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `Usuario.objects.filter(email='nova@elo.test').exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 97 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotIn`; argumentos posicionais: `Usuario.Perfil.ADMINISTRADOR`, `dict(CadastroUsuarioForm().fields['perfil'].choices)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 104 — FunctionDef** (nível 1 do bloco).

Define `test_cadastro_valido_grava_senha_hash_e_consentimento(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: cadastro valido grava senha hash e consentimento.

Bloco `body` da linha 104:

**Linha 105 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:cadastro')`, `{'nome': 'Doador cadastrado', 'email': 'cadastro@elo.test', 'perfil': Usuario.Perfil.DOADOR, 'cpf': '12345678901', 'data_nascimento': '1990-01-01', 'password1': 'SenhaForte123!', 'password2': 'SenhaForte123!', 'aceite_lgpd': 'on'}`.


**Linha 119 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:dashboard')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 124 — Assign** (nível 2 do bloco).

Associa `usuario` a a chamada `Usuario.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `email='cadastro@elo.test'`.

- `email='cadastro@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 128 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `usuario.check_password('SenhaForte123!')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 131 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotEqual`; argumentos posicionais: `usuario.password`, `'SenhaForte123!'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 136 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `ConsentimentoLGPD.objects.filter(usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL, aceito=True).exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 144 — FunctionDef** (nível 1 do bloco).

Define `test_cadastro_de_hemocentro_inicia_pendente_e_nao_libera_estoque(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: cadastro de hemocentro inicia pendente e nao libera estoque.

Bloco `body` da linha 144:

**Linha 147 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:cadastro')`, `{'nome': 'Hemocentro cadastrado', 'email': 'novo-hemocentro@elo.test', 'perfil': Usuario.Perfil.HEMOCENTRO, 'cnpj': '12345678000195', 'cidade': 'Belo Horizonte', 'estado': 'MG', 'password1': 'SenhaForte123!', 'password2': 'SenhaForte123!', 'aceite_lgpd': 'on'}`.


**Linha 162 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:dashboard')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 167 — Assign** (nível 2 do bloco).

Associa `hemocentro` a a chamada `Usuario.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `email='novo-hemocentro@elo.test'`.

- `email='novo-hemocentro@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 171 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `hemocentro.status_validacao`, `Usuario.StatusValidacaoHemocentro.PENDENTE`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 176 — Assign** (nível 2 do bloco).

Associa `estoque` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:estoque_hemocentro')`.


**Linha 180 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `estoque.status_code`, `403`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 182 — FunctionDef** (nível 1 do bloco).

Define `test_login_bloqueia_conta_suspensa(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: login bloqueia conta suspensa.

Bloco `body` da linha 182:

**Linha 183 — Assign** (nível 2 do bloco).

Associa `self.doador.suspensa` a o valor literal `True`.

**Linha 184 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['suspensa']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 186 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:login')`, `{'username': self.doador.email, 'password': 'SenhaForte123!'}`.


**Linha 194 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `200`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 195 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotIn`; argumentos posicionais: `'_auth_user_id'`, `self.client.session`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 200 — FunctionDef** (nível 1 do bloco).

Define `test_triagem_exige_aceite_explicito(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: triagem exige aceite explicito.

Bloco `body` da linha 200:

**Linha 201 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.doador`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 203 — Assign** (nível 2 do bloco).

Associa `url` a a chamada `reverse`, que resolve o endereço a partir do nome da rota; argumentos posicionais: `'accounts:triagem_iniciar'`; argumentos nomeados: `kwargs={'modalidade': 'extensa'}`.

- `kwargs={'modalidade': 'extensa'}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 208 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.post`; argumentos posicionais: `url`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 210 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `Triagem.objects.filter(usuario=self.doador).exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 216 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `url`, `{'aceite_termo': 'on'}`.


**Linha 221 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `302`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 223 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `ConsentimentoLGPD.objects.filter(usuario=self.doador, tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM).exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 230 — FunctionDef** (nível 1 do bloco).

Define `test_solicitacao_nao_publica_e_hemocentro_publica(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: solicitacao nao publica e hemocentro publica.

Bloco `body` da linha 230:

**Linha 231 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.receptor`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 232 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:pedido_publicar')`, `self.dados_solicitacao()`.


**Linha 237 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `302`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 239 — Assign** (nível 2 do bloco).

Associa `pedido` a a chamada `PedidoSangue.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave.


**Linha 241 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pedido.status`, `PedidoSangue.Status.ENVIADA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 246 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(PermissionDenied)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 246:

**Linha 247 — Expr** (nível 3 do bloco).

Executa a chamada `aprovar_pedido`; argumentos nomeados: `pedido=pedido`, `moderador=self.admin`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 252 — Expr** (nível 2 do bloco).

Executa a chamada `aprovar_pedido`; argumentos nomeados: `pedido=pedido`, `moderador=self.hemocentro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 257 — Expr** (nível 2 do bloco).

Executa a chamada `pedido.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 259 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pedido.status`, `PedidoSangue.Status.PUBLICADA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 263 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pedido.publicado_por`, `self.hemocentro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 268 — FunctionDef** (nível 1 do bloco).

Define `test_observador_pode_solicitar_mas_nao_analisar(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: observador pode solicitar mas nao analisar.

Bloco `body` da linha 268:

**Linha 269 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.observador`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 271 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:painel_pedidos_hemocentro')`.


**Linha 275 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `403`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 277 — FunctionDef** (nível 1 do bloco).

Define `test_receptor_acompanha_somente_suas_solicitacoes(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: receptor acompanha somente suas solicitacoes.

Bloco `body` da linha 277:

**Linha 278 — Assign** (nível 2 do bloco).

Associa `pedido` a a chamada `criar_pedido_pendente`; argumentos nomeados: `dados={**self.dados_solicitacao(), 'contato': 'receptor@elo.test'}`, `solicitante=self.receptor`.

- `dados={**self.dados_solicitacao(), 'contato': 'receptor@elo.test'}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `solicitante=self.receptor`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 286 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.receptor`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 288 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:minhas_solicitacoes')`.


**Linha 292 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `str(pedido.pk)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 293 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotContains`, que o teste exige ausência de texto na resposta HTTP; argumentos posicionais: `resposta`, `'outra-pessoa'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 295 — FunctionDef** (nível 1 do bloco).

Define `test_tipo_sanguineo_confirmado_nao_e_sobrescrito_pela_triagem(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: tipo sanguineo confirmado nao e sobrescrito pela triagem.

Bloco `body` da linha 295:

**Linha 298 — Assign** (nível 2 do bloco).

Associa `self.doador.tipo_sanguineo` a o valor literal `'A+'`.

**Linha 299 — Assign** (nível 2 do bloco).

Associa `self.doador.tipo_sanguineo_confirmado` a o valor literal `True`.

**Linha 300 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['tipo_sanguineo', 'tipo_sanguineo_confirmado']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 307 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.doador`.

- `usuario=self.doador`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 311 — Expr** (nível 2 do bloco).

Executa a chamada `atualizar_tipo_sanguineo_do_usuario`; argumentos posicionais: `triagem`, `{'codigos': ['O+']}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 316 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 318 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.doador.tipo_sanguineo`, `'A+'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 323 — FunctionDef** (nível 1 do bloco).

Define `test_publicacao_notifica_somente_doador_apto_compativel(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: publicacao notifica somente doador apto compativel.

Bloco `body` da linha 323:

**Linha 324 — ImportFrom** (nível 2 do bloco).

Importa de `.compatibilidade` os nomes `atualizar_preferencia_convocacao`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 325 — Expr** (nível 2 do bloco).

Executa a chamada `atualizar_preferencia_convocacao`; argumentos posicionais: `self.doador`, `True`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 326 — Assign** (nível 2 do bloco).

Associa `self.doador.tipo_sanguineo` a o valor literal `'O-'`.

**Linha 327 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['tipo_sanguineo']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 331 — Expr** (nível 2 do bloco).

Executa a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.doador`, `status=Triagem.Status.CONCLUIDA`, `resultado=Triagem.Resultado.APTO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 337 — Assign** (nível 2 do bloco).

Associa `pedido` a a chamada `criar_pedido_pendente`; argumentos nomeados: `dados=self.dados_solicitacao()`, `solicitante=self.receptor`.

- `dados=self.dados_solicitacao()`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `solicitante=self.receptor`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 342 — Expr** (nível 2 do bloco).

Executa a chamada `aprovar_pedido`; argumentos nomeados: `pedido=pedido`, `moderador=self.hemocentro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 347 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `Notificacao.objects.filter(usuario=self.doador, pedido=pedido, tipo=Notificacao.Tipo.PEDIDO_COMPATIVEL).exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

### ConvocacaoCompatibilidadeTests — linhas 355 a 534

```python
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

    def test_atualizacao_de_estoque_convoca_somente_quando_critico(self):
        from .estoque import registrar_movimentacao_estoque
        from .models import Estoque, EstoqueMovimentacao
        doador = self.doador('estoque_critico')
        for quantidade, status in (
            (7, Estoque.StatusCalculado.BAIXO),
            (12, Estoque.StatusCalculado.ESTAVEL),
            (5, Estoque.StatusCalculado.CRITICO),
        ):
            with self.subTest(status=status):
                registrar_movimentacao_estoque(
                    estoque=self.estoque, usuario_resp=self.hemocentro,
                    tipo_movimento=EstoqueMovimentacao.TipoMovimento.AJUSTE,
                    quantidade=quantidade, motivo='Conferencia do estoque',
                )
                self.estoque.refresh_from_db()
                self.assertEqual(self.estoque.status_calculado, status)
                self.assertEqual(Notificacao.objects.count(), int(status == Estoque.StatusCalculado.CRITICO))
        notificacao = Notificacao.objects.get()
        self.assertEqual(notificacao.usuario_id, doador.pk)
        self.assertEqual(notificacao.tipo, Notificacao.Tipo.ESTOQUE_CRITICO)

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
```

**Explicação deste trecho:**

**Linha 355 — ClassDef** (nível 0 do bloco).

Define a classe `ConvocacaoCompatibilidadeTests` herdando de `TestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 355:

**Linha 357 — FunctionDef** (nível 1 do bloco).

Define `setUpTestData(cls)`. O corpo só executa quando a função/método é chamado. Decoradores: `classmethod`.

Bloco `body` da linha 357:

**Linha 358 — ImportFrom** (nível 2 do bloco).

Importa de `.models` os nomes `Estoque`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 359 — Assign** (nível 2 do bloco).

Associa `cls.hemocentro` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email='hemo.convocacao@elo.test'`, `nome='Hemocentro'`, `perfil=Usuario.Perfil.HEMOCENTRO`, `status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO`, `cidade='Belo Horizonte'`.

- `email='hemo.convocacao@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Hemocentro'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.HEMOCENTRO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `cidade='Belo Horizonte'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 364 — Assign** (nível 2 do bloco).

Associa `cls.estoque` a a chamada `Estoque.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `hemocentro=cls.hemocentro`, `tipo_sanguineo='O-'`, `quantidade_bolsas=0`, `nivel_minimo=10`, `nivel_critico=5`, `status_calculado=Estoque.StatusCalculado.CRITICO`.

- `hemocentro=cls.hemocentro`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_sanguineo='O-'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `quantidade_bolsas=0`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nivel_minimo=10`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nivel_critico=5`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status_calculado=Estoque.StatusCalculado.CRITICO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 366 — Assign** (nível 2 do bloco).

Associa `cls.pedido` a a chamada `PedidoSangue.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `hemocentro_destino=cls.hemocentro`, `nome_solicitante='Solicitante'`, `contato='contato@elo.test'`, `para_quem=PedidoSangue.ParaQuem.MIM`, `tipo_sanguineo='O-'`, `cidade='Belo Horizonte'`, `urgencia=PedidoSangue.Urgencia.MEDIA`, `descricao='Pedido publicado para testar convocacao.'`, `status=PedidoSangue.Status.PUBLICADA`.

- `hemocentro_destino=cls.hemocentro`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome_solicitante='Solicitante'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `contato='contato@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `para_quem=PedidoSangue.ParaQuem.MIM`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_sanguineo='O-'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `cidade='Belo Horizonte'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `urgencia=PedidoSangue.Urgencia.MEDIA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `descricao='Pedido publicado para testar convocacao.'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status=PedidoSangue.Status.PUBLICADA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 371 — FunctionDef** (nível 1 do bloco).

Define `doador(self, nome, **extras)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 371:

**Linha 372 — Assign** (nível 2 do bloco).

Associa `usuario` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email=nome + '@convocacao.test'`, `nome=nome`, `perfil=extras.pop('perfil', Usuario.Perfil.DOADOR)`, `tipo_sanguineo=extras.pop('tipo_sanguineo', 'O-')`, `**=extras`.

- `email=nome + '@convocacao.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome=nome`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=extras.pop('perfil', Usuario.Perfil.DOADOR)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo_sanguineo=extras.pop('tipo_sanguineo', 'O-')`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `**=extras`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 375 — Expr** (nível 2 do bloco).

Executa a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=usuario`, `status=Triagem.Status.CONCLUIDA`, `resultado=Triagem.Resultado.APTO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 377 — Expr** (nível 2 do bloco).

Executa a chamada `ConsentimentoLGPD.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=usuario`, `tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES`, `versao_termo='1.0'`, `aceito=True`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 379 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `usuario` ao chamador.

**Linha 381 — FunctionDef** (nível 1 do bloco).

Define `emitir(self, origem)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 381:

**Linha 382 — ImportFrom** (nível 2 do bloco).

Importa de `.estoque` os nomes `criar_notificacoes_para_doadores_compativeis`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 383 — ImportFrom** (nível 2 do bloco).

Importa de `.pedidos` os nomes `criar_notificacoes_para_pedido`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 384 — ImportFrom** (nível 2 do bloco).

Importa de `.models` os nomes `Estoque`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 385 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `origem` igual a `'estoque'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 385:

**Linha 386 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve a chamada `criar_notificacoes_para_doadores_compativeis`; argumentos nomeados: `estoque=self.estoque`, `status_calculado=Estoque.StatusCalculado.CRITICO` ao chamador.

**Linha 388 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `criar_notificacoes_para_pedido`; argumentos nomeados: `pedido=self.pedido` ao chamador.

**Linha 390 — FunctionDef** (nível 1 do bloco).

Define `test_ambos_fluxos_exigem_todos_os_criterios(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: ambos fluxos exigem todos os criterios.

Bloco `body` da linha 390:

**Linha 391 — ImportFrom** (nível 2 do bloco).

Importa de `django.utils` os nomes `timezone`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 392 — ImportFrom** (nível 2 do bloco).

Importa de `datetime` os nomes `timedelta`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 393 — Assign** (nível 2 do bloco).

Associa `apto` a a chamada `self.doador`; argumentos posicionais: `'apto'`.


**Linha 394 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador`; argumentos posicionais: `'incompativel'`; argumentos nomeados: `tipo_sanguineo='A+'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 395 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador`; argumentos posicionais: `'suspenso'`; argumentos nomeados: `suspensa=True`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 396 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador`; argumentos posicionais: `'inativo'`; argumentos nomeados: `is_active=False`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 397 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador`; argumentos posicionais: `'preferencia_desativada'`; argumentos nomeados: `aceita_notificacoes_pedidos=False`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 398 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador`; argumentos posicionais: `'receptor'`; argumentos nomeados: `perfil=Usuario.Perfil.RECEPTOR`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 399 — Assign** (nível 2 do bloco).

Associa `revogado` a a chamada `self.doador`; argumentos posicionais: `'revogado'`.


**Linha 400 — Expr** (nível 2 do bloco).

Executa a chamada `revogado.consentimentos_lgpd.update`, que no QuerySet grava diretamente os campos dos resultados, sem chamar save de cada instância; argumentos nomeados: `revogado_em=timezone.now()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 401 — Assign** (nível 2 do bloco).

Associa `recusou` a a chamada `self.doador`; argumentos posicionais: `'recusou'`.


**Linha 402 — Expr** (nível 2 do bloco).

Executa a chamada `recusou.consentimentos_lgpd.update`, que no QuerySet grava diretamente os campos dos resultados, sem chamar save de cada instância; argumentos nomeados: `aceito=False`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 403 — Assign** (nível 2 do bloco).

Associa `sem_consentimento` a a chamada `self.doador`; argumentos posicionais: `'sem_consentimento'`.


**Linha 404 — Expr** (nível 2 do bloco).

Executa a chamada `sem_consentimento.consentimentos_lgpd.all().delete`, que remove o objeto/conjunto conforme o tipo e as relações envolvidas. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 405 — Assign** (nível 2 do bloco).

Associa `versao_antiga` a a chamada `self.doador`; argumentos posicionais: `'versao_antiga'`.


**Linha 406 — Expr** (nível 2 do bloco).

Executa a chamada `versao_antiga.consentimentos_lgpd.update`, que no QuerySet grava diretamente os campos dos resultados, sem chamar save de cada instância; argumentos nomeados: `versao_termo='0.9'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 407 — Assign** (nível 2 do bloco).

Associa `futuro` a a chamada `self.doador`; argumentos posicionais: `'futuro'`.


**Linha 408 — Expr** (nível 2 do bloco).

Executa a chamada `futuro.triagens.update`, que no QuerySet grava diretamente os campos dos resultados, sem chamar save de cada instância; argumentos nomeados: `data_liberacao=timezone.localdate() + timedelta(days=1)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 409 — Assign** (nível 2 do bloco).

Associa `sem_triagem` a a chamada `self.doador`; argumentos posicionais: `'sem_triagem'`.


**Linha 410 — Expr** (nível 2 do bloco).

Executa a chamada `sem_triagem.triagens.all().delete`, que remove o objeto/conjunto conforme o tipo e as relações envolvidas. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 411 — Assign** (nível 2 do bloco).

Associa `inapto` a a chamada `self.doador`; argumentos posicionais: `'inapto'`.


**Linha 412 — Expr** (nível 2 do bloco).

Executa a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=inapto`, `status=Triagem.Status.CONCLUIDA`, `resultado=Triagem.Resultado.INAPTO_TEMPORARIO`, `finalizada_em=timezone.now()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 414 — For** (nível 2 do bloco).

Percorre `('estoque', 'pedido')`; cada item é atribuído a `origem` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 414:

**Linha 415 — With** (nível 3 do bloco).

Executa sob os contextos `self.subTest(origem=origem)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 415:

**Linha 416 — Expr** (nível 4 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.emitir(origem)`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 417 — Expr** (nível 4 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `list(Notificacao.objects.values_list('usuario_id', flat=True))`, `[apto.pk]`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 418 — Expr** (nível 4 do bloco).

Executa a chamada `Notificacao.objects.all().delete`, que remove o objeto/conjunto conforme o tipo e as relações envolvidas. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 420 — FunctionDef** (nível 1 do bloco).

Define `test_limite_soma_estoque_e_pedido_mesmo_depois_de_lido(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: limite soma estoque e pedido mesmo depois de lido.

Bloco `body` da linha 420:

**Linha 421 — ImportFrom** (nível 2 do bloco).

Importa de `datetime` os nomes `timedelta`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 422 — ImportFrom** (nível 2 do bloco).

Importa de `django.utils` os nomes `timezone`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 423 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador`; argumentos posicionais: `'frequencia'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 424 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.emitir('estoque')`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 425 — Expr** (nível 2 do bloco).

Executa a chamada `Notificacao.objects.update`, que no QuerySet grava diretamente os campos dos resultados, sem chamar save de cada instância; argumentos nomeados: `lida=True`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 426 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.emitir('pedido')`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 427 — Expr** (nível 2 do bloco).

Executa a chamada `Notificacao.objects.update`, que no QuerySet grava diretamente os campos dos resultados, sem chamar save de cada instância; argumentos nomeados: `criada_em=timezone.now() - timedelta(hours=25)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 428 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.emitir('pedido')`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 429 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.emitir('pedido')`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 431 — FunctionDef** (nível 1 do bloco).

Define `test_pedido_pendente_nao_convoca(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: pedido pendente nao convoca.

Bloco `body` da linha 431:

**Linha 432 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador`; argumentos posicionais: `'pendente'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 433 — Assign** (nível 2 do bloco).

Associa `self.pedido.status` a o atributo `ENVIADA` de `PedidoSangue.Status`.

**Linha 434 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.emitir('pedido')`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 436 — FunctionDef** (nível 1 do bloco).

Define `test_atualizacao_de_estoque_convoca_somente_quando_critico(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: atualizacao de estoque convoca somente quando critico.

Bloco `body` da linha 436:

**Linha 437 — ImportFrom** (nível 2 do bloco).

Importa de `.estoque` os nomes `registrar_movimentacao_estoque`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 438 — ImportFrom** (nível 2 do bloco).

Importa de `.models` os nomes `Estoque`, `EstoqueMovimentacao`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 439 — Assign** (nível 2 do bloco).

Associa `doador` a a chamada `self.doador`; argumentos posicionais: `'estoque_critico'`.


**Linha 440 — For** (nível 2 do bloco).

Percorre `((7, Estoque.StatusCalculado.BAIXO), (12, Estoque.StatusCalculado.ESTAVEL), (5, Estoque.StatusCalculado.CRITICO))`; cada item é atribuído a `(quantidade, status)` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 440:

**Linha 445 — With** (nível 3 do bloco).

Executa sob os contextos `self.subTest(status=status)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 445:

**Linha 446 — Expr** (nível 4 do bloco).

Executa a chamada `registrar_movimentacao_estoque`; argumentos nomeados: `estoque=self.estoque`, `usuario_resp=self.hemocentro`, `tipo_movimento=EstoqueMovimentacao.TipoMovimento.AJUSTE`, `quantidade=quantidade`, `motivo='Conferencia do estoque'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 451 — Expr** (nível 4 do bloco).

Executa a chamada `self.estoque.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 452 — Expr** (nível 4 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.estoque.status_calculado`, `status`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 453 — Expr** (nível 4 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `Notificacao.objects.count()`, `int(status == Estoque.StatusCalculado.CRITICO)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 454 — Assign** (nível 2 do bloco).

Associa `notificacao` a a chamada `Notificacao.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave.


**Linha 455 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `notificacao.usuario_id`, `doador.pk`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 456 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `notificacao.tipo`, `Notificacao.Tipo.ESTOQUE_CRITICO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 458 — FunctionDef** (nível 1 do bloco).

Define `test_preferencia_no_painel_registra_aceite_e_revogacao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: preferencia no painel registra aceite e revogacao.

Bloco `body` da linha 458:

**Linha 459 — ImportFrom** (nível 2 do bloco).

Importa de `.models` os nomes `AuditoriaAcaoCritica`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 460 — Assign** (nível 2 do bloco).

Associa `usuario` a a chamada `self.doador`; argumentos posicionais: `'painel'`.


**Linha 461 — Expr** (nível 2 do bloco).

Executa a chamada `usuario.consentimentos_lgpd.all().delete`, que remove o objeto/conjunto conforme o tipo e as relações envolvidas. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 462 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `usuario`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 463 — Assign** (nível 2 do bloco).

Associa `url` a a chamada `reverse`, que resolve o endereço a partir do nome da rota; argumentos posicionais: `'accounts:dashboard'`.


**Linha 464 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `self.client.get(url)`, `'Alertas de doação'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 465 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.client.post(url, {'aceita_convocacoes': 'on'}).status_code`, `302`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 466 — Assign** (nível 2 do bloco).

Associa `consentimento` a a chamada `usuario.consentimentos_lgpd.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES`.

- `tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 467 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `consentimento.aceito`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 468 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIsNone`; argumentos posicionais: `consentimento.revogado_em`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 469 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.emitir('pedido')`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 470 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.client.post(url, {}).status_code`, `302`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 471 — Expr** (nível 2 do bloco).

Executa a chamada `consentimento.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 472 — Expr** (nível 2 do bloco).

Executa a chamada `usuario.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 473 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `usuario.aceita_notificacoes_pedidos`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 474 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `consentimento.aceito`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 475 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIsNotNone`; argumentos posicionais: `consentimento.revogado_em`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 476 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `AuditoriaAcaoCritica.objects.filter(metadados__evento='PREFERENCIA_CONVOCACAO').exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 477 — Expr** (nível 2 do bloco).

Executa a chamada `Notificacao.objects.all().delete`, que remove o objeto/conjunto conforme o tipo e as relações envolvidas. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 478 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.emitir('estoque')`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 480 — FunctionDef** (nível 1 do bloco).

Define `test_outro_perfil_nao_altera_preferencia(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: outro perfil nao altera preferencia.

Bloco `body` da linha 480:

**Linha 481 — Assign** (nível 2 do bloco).

Associa `usuario` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email='observador@convocacao.test'`, `nome='Observador'`, `perfil=Usuario.Perfil.OBSERVADOR`.

- `email='observador@convocacao.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Observador'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.OBSERVADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 483 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `usuario`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 484 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.client.post(reverse('accounts:dashboard'), {'aceita_convocacoes': 'on'}).status_code`, `403`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 485 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `usuario.consentimentos_lgpd.filter(tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES).exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 487 — FunctionDef** (nível 1 do bloco).

Define `test_cadastro_autorizacao_e_opcional_e_explicita(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: cadastro autorizacao e opcional e explicita.

Bloco `body` da linha 487:

**Linha 488 — For** (nível 2 do bloco).

Percorre `(False, True)`; cada item é atribuído a `aceita` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 488:

**Linha 489 — With** (nível 3 do bloco).

Executa sob os contextos `self.subTest(aceita=aceita)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 489:

**Linha 490 — Expr** (nível 4 do bloco).

Executa a chamada `self.client.logout`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 491 — Assign** (nível 4 do bloco).

Associa `dados` a um dicionário de 8 entradas; as chaves dão nome aos valores associados.

- Chave `'nome'`: recebe o valor literal `'Doador'`.
- Chave `'email'`: recebe o texto formatado `f'cadastro{int(aceita)}@convocacao.test'`, inserindo valores nas partes entre chaves.
- Chave `'perfil'`: recebe o atributo `DOADOR` de `Usuario.Perfil`.
- Chave `'cpf'`: recebe `'12345678901'` se `not aceita` for verdadeiro; caso contrário, `'12345678902'`.
- Chave `'data_nascimento'`: recebe o valor literal `'1990-01-01'`.
- Chave `'password1'`: recebe o valor literal `'SenhaForte123!'`.
- Chave `'password2'`: recebe o valor literal `'SenhaForte123!'`.
- Chave `'aceite_lgpd'`: recebe o valor literal `'on'`.

**Linha 494 — If** (nível 4 do bloco).

Escolhe um caminho verificando o valor associado ao nome `aceita`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 494:

**Linha 495 — Assign** (nível 5 do bloco).

Associa `dados['aceita_notificacoes_pedidos']` a o valor literal `'on'`.

**Linha 496 — Expr** (nível 4 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.client.post(reverse('accounts:cadastro'), dados).status_code`, `302`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 497 — Assign** (nível 4 do bloco).

Associa `usuario` a a chamada `Usuario.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `email=dados['email']`.

- `email=dados['email']`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 498 — Expr** (nível 4 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `usuario.aceita_notificacoes_pedidos`, `aceita`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 499 — Expr** (nível 4 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `usuario.consentimentos_lgpd.get(tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES).aceito`, `aceita`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 501 — FunctionDef** (nível 1 do bloco).

Define `test_publicacao_alternativa_tambem_convoca(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: publicacao alternativa tambem convoca.

Bloco `body` da linha 501:

**Linha 502 — ImportFrom** (nível 2 do bloco).

Importa de `.forms` os nomes `PedidoSangueForm`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 503 — ImportFrom** (nível 2 do bloco).

Importa de `.pedidos` os nomes `publicar_pedido`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 504 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador`; argumentos posicionais: `'alternativa'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 505 — Assign** (nível 2 do bloco).

Associa `form` a a chamada `PedidoSangueForm`; argumentos posicionais: `{'nome_solicitante': 'Solicitante', 'contato': 'contato@elo.test', 'para_quem': PedidoSangue.ParaQuem.MIM, 'hemocentro_destino': self.hemocentro.pk, 'titulo': 'Pedido alternativo', 'tipo_sanguineo': 'O-', 'urgencia': PedidoSangue.Urgencia.MEDIA, 'cidade': 'Belo Horizonte', 'descricao': 'Precisamos de doadores para atendimento hospitalar.'}`.


**Linha 509 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `form.is_valid()`, `form.errors`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 510 — Assign** (nível 2 do bloco).

Associa `pedido` a a chamada `publicar_pedido`; argumentos posicionais: `self.hemocentro`, `form`.


**Linha 511 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `Notificacao.objects.filter(pedido=pedido).exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 513 — FunctionDef** (nível 1 do bloco).

Define `test_compatibilidade_seleciona_os_tipos_da_tabela(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: compatibilidade seleciona os tipos da tabela.

Bloco `body` da linha 513:

**Linha 514 — ImportFrom** (nível 2 do bloco).

Importa de `.compatibilidade` os nomes `TIPOS_SANGUINEOS`, `COMPATIBILIDADE_RECEBIMENTO`, `doadores_aptos_para_convocacao`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 515 — For** (nível 2 do bloco).

Percorre `enumerate(TIPOS_SANGUINEOS)`; cada item é atribuído a `(i, tipo)` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 515:

**Linha 516 — Expr** (nível 3 do bloco).

Executa a chamada `self.doador`; argumentos posicionais: `f'tipo{i}'`; argumentos nomeados: `tipo_sanguineo=tipo`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 517 — For** (nível 2 do bloco).

Percorre `COMPATIBILIDADE_RECEBIMENTO.items()`; cada item é atribuído a `(solicitado, esperados)` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 517:

**Linha 518 — With** (nível 3 do bloco).

Executa sob os contextos `self.subTest(tipo=solicitado)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 518:

**Linha 519 — Assign** (nível 4 do bloco).

Associa `encontrados` a a chamada `set`; argumentos posicionais: `doadores_aptos_para_convocacao(solicitado).values_list('tipo_sanguineo', flat=True)`.


**Linha 520 — Expr** (nível 4 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `encontrados`, `set(esperados)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 522 — FunctionDef** (nível 1 do bloco).

Define `test_limite_e_compartilhado_tambem_quando_pedido_vem_primeiro(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: limite e compartilhado tambem quando pedido vem primeiro.

Bloco `body` da linha 522:

**Linha 523 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador`; argumentos posicionais: `'pedido_primeiro'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 524 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.emitir('pedido')`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 525 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.emitir('estoque')`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 527 — FunctionDef** (nível 1 do bloco).

Define `test_limite_configuravel_nao_remove_protecao_contra_duplicatas(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: limite configuravel nao remove protecao contra duplicatas.

Bloco `body` da linha 527:

**Linha 528 — ImportFrom** (nível 2 do bloco).

Importa de `django.test` os nomes `override_settings`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 529 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador`; argumentos posicionais: `'limite_configuravel'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 530 — With** (nível 2 do bloco).

Executa sob os contextos `override_settings(CONVOCACAO_LIMITE_NOTIFICACOES=3)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 530:

**Linha 531 — Expr** (nível 3 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.emitir('pedido')`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 532 — Expr** (nível 3 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.emitir('pedido')`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 533 — Expr** (nível 3 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.emitir('estoque')`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 534 — Expr** (nível 3 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.emitir('estoque')`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

### CentralNotificacoesTests — linhas 537 a 594

```python
class CentralNotificacoesTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email='central@elo.test', nome='Receptor', perfil=Usuario.Perfil.RECEPTOR,
        )
        self.outro = Usuario.objects.create_user(
            email='outra-central@elo.test', nome='Outro', perfil=Usuario.Perfil.RECEPTOR,
        )
        self.aviso = Notificacao.objects.create(
            usuario=self.usuario, titulo='Estoque urgente', mensagem='Precisamos de doadores.',
            tipo=Notificacao.Tipo.ESTOQUE_CRITICO, url_destino=reverse('accounts:estoque_publico'),
        )
        self.client.force_login(self.usuario)
        self.url = reverse('accounts:dashboard')

    def test_leitura_persiste_sem_apagar_historico_nem_regravar_data(self):
        dados = {'acao': 'marcar_notificacao_lida', 'id_notificacao': self.aviso.pk}
        self.assertEqual(self.client.post(self.url, dados).status_code, 302)
        self.aviso.refresh_from_db()
        self.assertTrue(self.aviso.lida)
        self.assertIsNotNone(self.aviso.lida_em)
        data_leitura = self.aviso.lida_em
        self.client.post(self.url, dados)
        self.aviso.refresh_from_db()
        self.assertEqual(self.aviso.lida_em, data_leitura)
        pagina = self.client.get(self.url)
        self.assertContains(pagina, 'Estoque urgente')
        self.assertContains(pagina, 'Ver estoque')
        self.assertContains(pagina, 'Lida')
        self.assertEqual(pagina.context['notificacoes_nao_lidas'], 0)

    def test_nao_permite_marcar_notificacao_de_outro_usuario(self):
        aviso = Notificacao.objects.create(usuario=self.outro, titulo='Privada', mensagem='Privada')
        self.assertEqual(self.client.post(self.url, {
            'acao': 'marcar_notificacao_lida', 'id_notificacao': aviso.pk,
        }).status_code, 404)
        aviso.refresh_from_db()
        self.assertFalse(aviso.lida)
        self.assertNotContains(self.client.get(self.url), 'Privada')

    def test_historico_paginado_mostra_notificacoes_mais_antigas(self):
        for numero in range(11):
            Notificacao.objects.create(usuario=self.usuario, titulo=f'Aviso {numero}', mensagem='Aviso')
        pagina = self.client.get(self.url)
        self.assertEqual(len(pagina.context['notificacoes_dashboard']), 10)
        self.assertContains(pagina, 'Próxima')
        self.assertContains(self.client.get(self.url, {'pagina_notificacoes': 2}), 'Estoque urgente')

    def test_identificador_invalido_e_anonimo_nao_marcam_leitura(self):
        self.assertEqual(self.client.post(self.url, {
            'acao': 'marcar_notificacao_lida', 'id_notificacao': 'invalido',
        }).status_code, 404)
        self.client.logout()
        self.assertEqual(self.client.post(self.url, {
            'acao': 'marcar_notificacao_lida', 'id_notificacao': self.aviso.pk,
        }).status_code, 302)
        self.aviso.refresh_from_db()
        self.assertFalse(self.aviso.lida)
```

**Explicação deste trecho:**

**Linha 537 — ClassDef** (nível 0 do bloco).

Define a classe `CentralNotificacoesTests` herdando de `TestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 537:

**Linha 538 — FunctionDef** (nível 1 do bloco).

Define `setUp(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 538:

**Linha 539 — Assign** (nível 2 do bloco).

Associa `self.usuario` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email='central@elo.test'`, `nome='Receptor'`, `perfil=Usuario.Perfil.RECEPTOR`.

- `email='central@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Receptor'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.RECEPTOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 542 — Assign** (nível 2 do bloco).

Associa `self.outro` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email='outra-central@elo.test'`, `nome='Outro'`, `perfil=Usuario.Perfil.RECEPTOR`.

- `email='outra-central@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Outro'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.RECEPTOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 545 — Assign** (nível 2 do bloco).

Associa `self.aviso` a a chamada `Notificacao.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.usuario`, `titulo='Estoque urgente'`, `mensagem='Precisamos de doadores.'`, `tipo=Notificacao.Tipo.ESTOQUE_CRITICO`, `url_destino=reverse('accounts:estoque_publico')`.

- `usuario=self.usuario`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `titulo='Estoque urgente'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `mensagem='Precisamos de doadores.'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `tipo=Notificacao.Tipo.ESTOQUE_CRITICO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `url_destino=reverse('accounts:estoque_publico')`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 549 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.usuario`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 550 — Assign** (nível 2 do bloco).

Associa `self.url` a a chamada `reverse`, que resolve o endereço a partir do nome da rota; argumentos posicionais: `'accounts:dashboard'`.


**Linha 552 — FunctionDef** (nível 1 do bloco).

Define `test_leitura_persiste_sem_apagar_historico_nem_regravar_data(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: leitura persiste sem apagar historico nem regravar data.

Bloco `body` da linha 552:

**Linha 553 — Assign** (nível 2 do bloco).

Associa `dados` a um dicionário de 2 entradas; as chaves dão nome aos valores associados.

- Chave `'acao'`: recebe o valor literal `'marcar_notificacao_lida'`.
- Chave `'id_notificacao'`: recebe o atributo `pk` de `self.aviso`.

**Linha 554 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.client.post(self.url, dados).status_code`, `302`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 555 — Expr** (nível 2 do bloco).

Executa a chamada `self.aviso.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 556 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `self.aviso.lida`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 557 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIsNotNone`; argumentos posicionais: `self.aviso.lida_em`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 558 — Assign** (nível 2 do bloco).

Associa `data_leitura` a o atributo `lida_em` de `self.aviso`.

**Linha 559 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.post`; argumentos posicionais: `self.url`, `dados`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 560 — Expr** (nível 2 do bloco).

Executa a chamada `self.aviso.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 561 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.aviso.lida_em`, `data_leitura`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 562 — Assign** (nível 2 do bloco).

Associa `pagina` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `self.url`.


**Linha 563 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `pagina`, `'Estoque urgente'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 564 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `pagina`, `'Ver estoque'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 565 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `pagina`, `'Lida'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 566 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `pagina.context['notificacoes_nao_lidas']`, `0`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 568 — FunctionDef** (nível 1 do bloco).

Define `test_nao_permite_marcar_notificacao_de_outro_usuario(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: nao permite marcar notificacao de outro usuario.

Bloco `body` da linha 568:

**Linha 569 — Assign** (nível 2 do bloco).

Associa `aviso` a a chamada `Notificacao.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.outro`, `titulo='Privada'`, `mensagem='Privada'`.

- `usuario=self.outro`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `titulo='Privada'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `mensagem='Privada'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 570 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.client.post(self.url, {'acao': 'marcar_notificacao_lida', 'id_notificacao': aviso.pk}).status_code`, `404`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 573 — Expr** (nível 2 do bloco).

Executa a chamada `aviso.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 574 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `aviso.lida`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 575 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotContains`, que o teste exige ausência de texto na resposta HTTP; argumentos posicionais: `self.client.get(self.url)`, `'Privada'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 577 — FunctionDef** (nível 1 do bloco).

Define `test_historico_paginado_mostra_notificacoes_mais_antigas(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: historico paginado mostra notificacoes mais antigas.

Bloco `body` da linha 577:

**Linha 578 — For** (nível 2 do bloco).

Percorre `range(11)`; cada item é atribuído a `numero` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 578:

**Linha 579 — Expr** (nível 3 do bloco).

Executa a chamada `Notificacao.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.usuario`, `titulo=f'Aviso {numero}'`, `mensagem='Aviso'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 580 — Assign** (nível 2 do bloco).

Associa `pagina` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `self.url`.


**Linha 581 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `len(pagina.context['notificacoes_dashboard'])`, `10`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 582 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `pagina`, `'Próxima'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 583 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `self.client.get(self.url, {'pagina_notificacoes': 2})`, `'Estoque urgente'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 585 — FunctionDef** (nível 1 do bloco).

Define `test_identificador_invalido_e_anonimo_nao_marcam_leitura(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: identificador invalido e anonimo nao marcam leitura.

Bloco `body` da linha 585:

**Linha 586 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.client.post(self.url, {'acao': 'marcar_notificacao_lida', 'id_notificacao': 'invalido'}).status_code`, `404`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 589 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.logout`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 590 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.client.post(self.url, {'acao': 'marcar_notificacao_lida', 'id_notificacao': self.aviso.pk}).status_code`, `302`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 593 — Expr** (nível 2 do bloco).

Executa a chamada `self.aviso.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 594 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `self.aviso.lida`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

