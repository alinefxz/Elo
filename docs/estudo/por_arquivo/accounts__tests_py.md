# accounts/tests.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Cenarios automatizados: preparacao, acao e resultado esperado nos asserts.

**Arquivo original:** [accounts/tests.py](<C:/Users/lb119/Elo/accounts/tests.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
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

from .models import AuditoriaAcaoCritica, Estoque, Usuario, ValidacaoHemocentro
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
        self.assertEqual(
            validacao.status,
            Usuario.StatusValidacaoHemocentro.APROVADO,
        )
        self.assertEqual(
            ValidacaoHemocentro.objects.filter(
                hemocentro=self.hemocentro
            ).count(),
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

        self.assertContains(
            resposta,
            "Status da validação institucional",
        )
        self.assertContains(resposta, "Pendente")
        self.assertNotContains(resposta, "Gestão de Hemocentros")
        self.assertNotContains(
            resposta,
            "Acessar aprovação de Hemocentros",
        )

    def test_admin_acessa_tela_de_validacao_e_ve_pendente(self):
        """Administrador deve receber a tela da aplicacao com os pendentes."""

        self.client.force_login(self.admin)

        resposta = self.client.get(reverse("accounts:dashboard"))

        self.assertContains(resposta, "Validação de Hemocentros")
        self.assertContains(
            resposta,
            "Acessar aprovação de Hemocentros",
        )
        self.assertContains(
            resposta,
            "<li>Aprovar Hemocentros.</li>",
            html=True,
        )
        self.assertContains(resposta, 'href="/admin/"')

        painel = self.client.get(
            reverse("accounts:painel_aprovacao_hemocentros")
        )

        self.assertEqual(painel.status_code, 200)
        self.assertContains(painel, self.hemocentro.nome)
        self.assertContains(painel, "Pendente")
        self.assertContains(painel, "Voltar ao painel")
        self.assertContains(painel, "Página inicial")
        self.assertContains(painel, "Estoques públicos")

    def test_admin_aprova_pelo_painel_e_libera_estoque(self):
        """A aprovacao feita na tela altera o status e libera o estoque."""

        self.client.force_login(self.admin)

        resposta = self.client.post(
            reverse(
                "accounts:aprovar_hemocentro",
                kwargs={"id_hemocentro": self.hemocentro.pk},
            ),
            {"parecer": "Documentacao conferida."},
        )

        self.assertRedirects(
            resposta,
            reverse("accounts:painel_aprovacao_hemocentros"),
        )

        self.hemocentro.refresh_from_db()

        self.assertEqual(
            self.hemocentro.status_validacao,
            Usuario.StatusValidacaoHemocentro.APROVADO,
        )

        self.client.force_login(self.hemocentro)

        estoque = self.client.get(
            reverse("accounts:estoque_hemocentro")
        )

        self.assertEqual(estoque.status_code, 200)
        self.assertContains(estoque, "Cadastrar novo estoque")

        cadastro_estoque = self.client.post(
            reverse("accounts:cadastrar_estoque"),
            {
                "tipo_sanguineo": "O+",
                "quantidade_bolsas": 8,
                "nivel_minimo": 10,
                "nivel_critico": 5,
            },
        )

        self.assertRedirects(
            cadastro_estoque,
            reverse("accounts:estoque_hemocentro"),
        )

        self.assertTrue(
            Estoque.objects.filter(
                hemocentro=self.hemocentro,
                tipo_sanguineo="O+",
            ).exists()
        )

    def test_usuario_comum_nao_acessa_tela_de_validacao(self):
        """A tela e suas acoes continuam restritas ao Administrador."""

        usuario_comum = self.criar_usuario(
            email="doador-tela@elo.test",
            nome="Doador",
            perfil=Usuario.Perfil.DOADOR,
        )

        self.client.force_login(usuario_comum)

        resposta = self.client.get(
            reverse("accounts:painel_aprovacao_hemocentros")
        )

        self.assertEqual(resposta.status_code, 403)

    def test_dashboard_admin_nao_mostra_publicacao_de_pedido(self):
        """Administrador não atua como Hemocentro na publicação."""

        self.client.force_login(self.admin)

        resposta = self.client.get(reverse("accounts:dashboard"))

        self.assertContains(resposta, "Pedidos ativos")
        self.assertNotContains(
            resposta,
            "Publicar pedido de sangue",
        )
        self.assertNotContains(
            resposta,
            "Solicitar divulgação de necessidade",
        )


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
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 25

```python
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
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 27 a 27

```python
from django.core.exceptions import PermissionDenied
```

**Explicação deste trecho:**

**Linha 27 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.exceptions` os nomes `PermissionDenied`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 28 a 28

```python
from django.test import TestCase
```

**Explicação deste trecho:**

**Linha 28 — ImportFrom** (nível 0 do bloco).

Importa de `django.test` os nomes `TestCase`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 29 a 29

```python
from django.urls import reverse
```

**Explicação deste trecho:**

**Linha 29 — ImportFrom** (nível 0 do bloco).

Importa de `django.urls` os nomes `reverse`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 31 a 31

```python
from .models import AuditoriaAcaoCritica, Estoque, Usuario, ValidacaoHemocentro
```

**Explicação deste trecho:**

**Linha 31 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `AuditoriaAcaoCritica`, `Estoque`, `Usuario`, `ValidacaoHemocentro`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 32 a 38

```python
from .validacao_hemocentro import (
    aprovar_hemocentro,
    hemocentro_aprovado,
    recusar_hemocentro,
    solicitar_correcao_hemocentro,
    validar_publicacao_hemocentro,
)
```

**Explicação deste trecho:**

**Linha 32 — ImportFrom** (nível 0 do bloco).

Importa de `.validacao_hemocentro` os nomes `aprovar_hemocentro`, `hemocentro_aprovado`, `recusar_hemocentro`, `solicitar_correcao_hemocentro`, `validar_publicacao_hemocentro`. Pontos iniciais indicam importação relativa ao pacote.

### ValidacaoHemocentroTests — linhas 41 a 332

```python
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
        self.assertEqual(
            validacao.status,
            Usuario.StatusValidacaoHemocentro.APROVADO,
        )
        self.assertEqual(
            ValidacaoHemocentro.objects.filter(
                hemocentro=self.hemocentro
            ).count(),
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

        self.assertContains(
            resposta,
            "Status da validação institucional",
        )
        self.assertContains(resposta, "Pendente")
        self.assertNotContains(resposta, "Gestão de Hemocentros")
        self.assertNotContains(
            resposta,
            "Acessar aprovação de Hemocentros",
        )

    def test_admin_acessa_tela_de_validacao_e_ve_pendente(self):
        """Administrador deve receber a tela da aplicacao com os pendentes."""

        self.client.force_login(self.admin)

        resposta = self.client.get(reverse("accounts:dashboard"))

        self.assertContains(resposta, "Validação de Hemocentros")
        self.assertContains(
            resposta,
            "Acessar aprovação de Hemocentros",
        )
        self.assertContains(
            resposta,
            "<li>Aprovar Hemocentros.</li>",
            html=True,
        )
        self.assertContains(resposta, 'href="/admin/"')

        painel = self.client.get(
            reverse("accounts:painel_aprovacao_hemocentros")
        )

        self.assertEqual(painel.status_code, 200)
        self.assertContains(painel, self.hemocentro.nome)
        self.assertContains(painel, "Pendente")
        self.assertContains(painel, "Voltar ao painel")
        self.assertContains(painel, "Página inicial")
        self.assertContains(painel, "Estoques públicos")

    def test_admin_aprova_pelo_painel_e_libera_estoque(self):
        """A aprovacao feita na tela altera o status e libera o estoque."""

        self.client.force_login(self.admin)

        resposta = self.client.post(
            reverse(
                "accounts:aprovar_hemocentro",
                kwargs={"id_hemocentro": self.hemocentro.pk},
            ),
            {"parecer": "Documentacao conferida."},
        )

        self.assertRedirects(
            resposta,
            reverse("accounts:painel_aprovacao_hemocentros"),
        )

        self.hemocentro.refresh_from_db()

        self.assertEqual(
            self.hemocentro.status_validacao,
            Usuario.StatusValidacaoHemocentro.APROVADO,
        )

        self.client.force_login(self.hemocentro)

        estoque = self.client.get(
            reverse("accounts:estoque_hemocentro")
        )

        self.assertEqual(estoque.status_code, 200)
        self.assertContains(estoque, "Cadastrar novo estoque")

        cadastro_estoque = self.client.post(
            reverse("accounts:cadastrar_estoque"),
            {
                "tipo_sanguineo": "O+",
                "quantidade_bolsas": 8,
                "nivel_minimo": 10,
                "nivel_critico": 5,
            },
        )

        self.assertRedirects(
            cadastro_estoque,
            reverse("accounts:estoque_hemocentro"),
        )

        self.assertTrue(
            Estoque.objects.filter(
                hemocentro=self.hemocentro,
                tipo_sanguineo="O+",
            ).exists()
        )

    def test_usuario_comum_nao_acessa_tela_de_validacao(self):
        """A tela e suas acoes continuam restritas ao Administrador."""

        usuario_comum = self.criar_usuario(
            email="doador-tela@elo.test",
            nome="Doador",
            perfil=Usuario.Perfil.DOADOR,
        )

        self.client.force_login(usuario_comum)

        resposta = self.client.get(
            reverse("accounts:painel_aprovacao_hemocentros")
        )

        self.assertEqual(resposta.status_code, 403)

    def test_dashboard_admin_nao_mostra_publicacao_de_pedido(self):
        """Administrador não atua como Hemocentro na publicação."""

        self.client.force_login(self.admin)

        resposta = self.client.get(reverse("accounts:dashboard"))

        self.assertContains(resposta, "Pedidos ativos")
        self.assertNotContains(
            resposta,
            "Publicar pedido de sangue",
        )
        self.assertNotContains(
            resposta,
            "Solicitar divulgação de necessidade",
        )
```

**Explicação deste trecho:**

**Linha 41 — ClassDef** (nível 0 do bloco).

Define a classe `ValidacaoHemocentroTests` herdando de `TestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 41:

**Linha 42 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 44 — FunctionDef** (nível 1 do bloco).

Define `criar_usuario(self, *, email, nome, perfil, is_staff=False, is_superuser=False)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 44:

**Linha 53 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 55 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `Usuario.objects.create_user`; argumentos nomeados: `email=email`, `password='SenhaForte123!'`, `nome=nome`, `perfil=perfil`, `is_staff=is_staff`, `is_superuser=is_superuser` ao chamador.

**Linha 64 — FunctionDef** (nível 1 do bloco).

Define `setUp(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 64:

**Linha 65 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 67 — Assign** (nível 2 do bloco).

Associa `self.admin` a a chamada `self.criar_usuario`; argumentos nomeados: `email='admin@elo.test'`, `nome='Administrador Elo'`, `perfil=Usuario.Perfil.ADMINISTRADOR`.

- `email='admin@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Administrador Elo'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.ADMINISTRADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 73 — Assign** (nível 2 do bloco).

Associa `self.hemocentro` a a chamada `self.criar_usuario`; argumentos nomeados: `email='hemocentro@elo.test'`, `nome='Hemocentro Elo'`, `perfil=Usuario.Perfil.HEMOCENTRO`.

- `email='hemocentro@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Hemocentro Elo'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.HEMOCENTRO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 79 — FunctionDef** (nível 1 do bloco).

Define `test_hemocentro_inicia_pendente(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: hemocentro inicia pendente.

Bloco `body` da linha 79:

**Linha 80 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 82 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.hemocentro.status_validacao`, `Usuario.StatusValidacaoHemocentro.PENDENTE`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 86 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `hemocentro_aprovado(self.hemocentro)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 88 — FunctionDef** (nível 1 do bloco).

Define `test_admin_aprova_e_cria_historico(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: admin aprova e cria historico.

Bloco `body` da linha 88:

**Linha 89 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 91 — Assign** (nível 2 do bloco).

Associa `validacao` a a chamada `aprovar_hemocentro`; argumentos nomeados: `hemocentro=self.hemocentro`, `admin=self.admin`.

- `hemocentro=self.hemocentro`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `admin=self.admin`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 96 — Expr** (nível 2 do bloco).

Executa a chamada `self.hemocentro.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 98 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.hemocentro.status_validacao`, `Usuario.StatusValidacaoHemocentro.APROVADO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 102 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `validacao.status`, `Usuario.StatusValidacaoHemocentro.APROVADO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 106 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `ValidacaoHemocentro.objects.filter(hemocentro=self.hemocentro).count()`, `1`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 112 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `AuditoriaAcaoCritica.objects.filter(acao=AuditoriaAcaoCritica.Acao.APROVACAO_HEMOCENTRO, usuario=self.admin, alvo_id=str(self.hemocentro.pk)).exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 120 — FunctionDef** (nível 1 do bloco).

Define `test_admin_recusa(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: admin recusa.

Bloco `body` da linha 120:

**Linha 121 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 123 — Assign** (nível 2 do bloco).

Associa `validacao` a a chamada `recusar_hemocentro`; argumentos nomeados: `hemocentro=self.hemocentro`, `admin=self.admin`, `parecer='CNPJ nao confere com os documentos enviados.'`.

- `hemocentro=self.hemocentro`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `admin=self.admin`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `parecer='CNPJ nao confere com os documentos enviados.'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 129 — Expr** (nível 2 do bloco).

Executa a chamada `self.hemocentro.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 131 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.hemocentro.status_validacao`, `Usuario.StatusValidacaoHemocentro.RECUSADO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 135 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `validacao.parecer`, `'CNPJ nao confere com os documentos enviados.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 140 — FunctionDef** (nível 1 do bloco).

Define `test_admin_solicita_correcao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: admin solicita correcao.

Bloco `body` da linha 140:

**Linha 141 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 143 — Expr** (nível 2 do bloco).

Executa a chamada `solicitar_correcao_hemocentro`; argumentos nomeados: `hemocentro=self.hemocentro`, `admin=self.admin`, `parecer='Atualize telefone e endereco.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 149 — Expr** (nível 2 do bloco).

Executa a chamada `self.hemocentro.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 151 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.hemocentro.status_validacao`, `Usuario.StatusValidacaoHemocentro.CORRECAO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 156 — FunctionDef** (nível 1 do bloco).

Define `test_usuario_comum_nao_pode_validar(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: usuario comum nao pode validar.

Bloco `body` da linha 156:

**Linha 157 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 159 — Assign** (nível 2 do bloco).

Associa `usuario_comum` a a chamada `self.criar_usuario`; argumentos nomeados: `email='doador@elo.test'`, `nome='Doador'`, `perfil=Usuario.Perfil.DOADOR`.

- `email='doador@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Doador'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.DOADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 165 — With** (nível 2 do bloco).

Executa sob os contextos `self.assertRaises(PermissionDenied)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 165:

**Linha 166 — Expr** (nível 3 do bloco).

Executa a chamada `aprovar_hemocentro`; argumentos nomeados: `hemocentro=self.hemocentro`, `admin=usuario_comum`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 171 — FunctionDef** (nível 1 do bloco).

Define `test_hemocentro_nao_aprovado_nao_publica(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: hemocentro nao aprovado nao publica.

Bloco `body` da linha 171:

**Linha 172 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 174 — For** (nível 2 do bloco).

Percorre `(Usuario.StatusValidacaoHemocentro.PENDENTE, Usuario.StatusValidacaoHemocentro.RECUSADO, Usuario.StatusValidacaoHemocentro.CORRECAO)`; cada item é atribuído a `status` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 174:

**Linha 179 — Assign** (nível 3 do bloco).

Associa `self.hemocentro.status_validacao` a o valor associado ao nome `status`.

**Linha 180 — Expr** (nível 3 do bloco).

Executa a chamada `self.hemocentro.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `update_fields=['status_validacao']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 182 — With** (nível 3 do bloco).

Executa sob os contextos `self.assertRaises(PermissionDenied)`. O contexto controla entrada e saída do bloco; pode representar transação, assert de exceção ou outra operação.

Bloco `body` da linha 182:

**Linha 183 — Expr** (nível 4 do bloco).

Executa a chamada `validar_publicacao_hemocentro`; argumentos posicionais: `self.hemocentro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 185 — FunctionDef** (nível 1 do bloco).

Define `test_hemocentro_aprovado_pode_publicar(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: hemocentro aprovado pode publicar.

Bloco `body` da linha 185:

**Linha 186 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 188 — Expr** (nível 2 do bloco).

Executa a chamada `aprovar_hemocentro`; argumentos nomeados: `hemocentro=self.hemocentro`, `admin=self.admin`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 192 — Expr** (nível 2 do bloco).

Executa a chamada `self.hemocentro.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 194 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `validar_publicacao_hemocentro(self.hemocentro)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 196 — FunctionDef** (nível 1 do bloco).

Define `test_dashboard_hemocentro_mostra_status_sem_link_de_aprovacao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: dashboard hemocentro mostra status sem link de aprovacao.

Bloco `body` da linha 196:

**Linha 197 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 199 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.hemocentro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 201 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:dashboard')`.


**Linha 203 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Status da validação institucional'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 207 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Pendente'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 208 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotContains`, que o teste exige ausência de texto na resposta HTTP; argumentos posicionais: `resposta`, `'Gestão de Hemocentros'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 209 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotContains`, que o teste exige ausência de texto na resposta HTTP; argumentos posicionais: `resposta`, `'Acessar aprovação de Hemocentros'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 214 — FunctionDef** (nível 1 do bloco).

Define `test_admin_acessa_tela_de_validacao_e_ve_pendente(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: admin acessa tela de validacao e ve pendente.

Bloco `body` da linha 214:

**Linha 215 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 217 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.admin`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 219 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:dashboard')`.


**Linha 221 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Validação de Hemocentros'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 222 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Acessar aprovação de Hemocentros'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 226 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'<li>Aprovar Hemocentros.</li>'`; argumentos nomeados: `html=True`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 231 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'href="/admin/"'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 233 — Assign** (nível 2 do bloco).

Associa `painel` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:painel_aprovacao_hemocentros')`.


**Linha 237 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `painel.status_code`, `200`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 238 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `painel`, `self.hemocentro.nome`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 239 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `painel`, `'Pendente'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 240 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `painel`, `'Voltar ao painel'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 241 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `painel`, `'Página inicial'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 242 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `painel`, `'Estoques públicos'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 244 — FunctionDef** (nível 1 do bloco).

Define `test_admin_aprova_pelo_painel_e_libera_estoque(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: admin aprova pelo painel e libera estoque.

Bloco `body` da linha 244:

**Linha 245 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 247 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.admin`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 249 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:aprovar_hemocentro', kwargs={'id_hemocentro': self.hemocentro.pk})`, `{'parecer': 'Documentacao conferida.'}`.


**Linha 257 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `resposta`, `reverse('accounts:painel_aprovacao_hemocentros')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 262 — Expr** (nível 2 do bloco).

Executa a chamada `self.hemocentro.refresh_from_db`, que recarrega os valores persistidos para a instância em memória. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 264 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `self.hemocentro.status_validacao`, `Usuario.StatusValidacaoHemocentro.APROVADO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 269 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.hemocentro`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 271 — Assign** (nível 2 do bloco).

Associa `estoque` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:estoque_hemocentro')`.


**Linha 275 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `estoque.status_code`, `200`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 276 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `estoque`, `'Cadastrar novo estoque'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 278 — Assign** (nível 2 do bloco).

Associa `cadastro_estoque` a a chamada `self.client.post`; argumentos posicionais: `reverse('accounts:cadastrar_estoque')`, `{'tipo_sanguineo': 'O+', 'quantidade_bolsas': 8, 'nivel_minimo': 10, 'nivel_critico': 5}`.


**Linha 288 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertRedirects`; argumentos posicionais: `cadastro_estoque`, `reverse('accounts:estoque_hemocentro')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 293 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `Estoque.objects.filter(hemocentro=self.hemocentro, tipo_sanguineo='O+').exists()`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 300 — FunctionDef** (nível 1 do bloco).

Define `test_usuario_comum_nao_acessa_tela_de_validacao(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: usuario comum nao acessa tela de validacao.

Bloco `body` da linha 300:

**Linha 301 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 303 — Assign** (nível 2 do bloco).

Associa `usuario_comum` a a chamada `self.criar_usuario`; argumentos nomeados: `email='doador-tela@elo.test'`, `nome='Doador'`, `perfil=Usuario.Perfil.DOADOR`.

- `email='doador-tela@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Doador'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.DOADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 309 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `usuario_comum`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 311 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:painel_aprovacao_hemocentros')`.


**Linha 315 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `403`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 317 — FunctionDef** (nível 1 do bloco).

Define `test_dashboard_admin_nao_mostra_publicacao_de_pedido(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: dashboard admin nao mostra publicacao de pedido.

Bloco `body` da linha 317:

**Linha 318 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 320 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.admin`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 322 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:dashboard')`.


**Linha 324 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertContains`, que o teste exige texto na resposta HTTP; argumentos posicionais: `resposta`, `'Pedidos ativos'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 325 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotContains`, que o teste exige ausência de texto na resposta HTTP; argumentos posicionais: `resposta`, `'Publicar pedido de sangue'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 329 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotContains`, que o teste exige ausência de texto na resposta HTTP; argumentos posicionais: `resposta`, `'Solicitar divulgação de necessidade'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

### AuditoriaTests — linhas 335 a 424

```python
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
```

**Explicação deste trecho:**

**Linha 335 — ClassDef** (nível 0 do bloco).

Define a classe `AuditoriaTests` herdando de `TestCase`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 335:

**Linha 337 — FunctionDef** (nível 1 do bloco).

Define `setUpTestData(cls)`. O corpo só executa quando a função/método é chamado. Decoradores: `classmethod`.

Bloco `body` da linha 337:

**Linha 338 — Assign** (nível 2 do bloco).

Associa `cls.admin` a a chamada `Usuario.objects.create_superuser`; argumentos nomeados: `email='auditoria.admin@elo.test'`, `password='SenhaForte123!'`, `nome='Administrador'`, `perfil=Usuario.Perfil.ADMINISTRADOR`.

- `email='auditoria.admin@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `password='SenhaForte123!'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Administrador'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.ADMINISTRADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 342 — Assign** (nível 2 do bloco).

Associa `cls.doador` a a chamada `Usuario.objects.create_user`; argumentos nomeados: `email='auditoria.doador@elo.test'`, `password='SenhaForte123!'`, `nome='Doador'`, `perfil=Usuario.Perfil.DOADOR`.

- `email='auditoria.doador@elo.test'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `password='SenhaForte123!'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `nome='Doador'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `perfil=Usuario.Perfil.DOADOR`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 347 — FunctionDef** (nível 1 do bloco).

Define `test_acesso_bloqueado_registrado(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: acesso bloqueado registrado.

Bloco `body` da linha 347:

**Linha 348 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.doador`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 349 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:painel_validacao_pedidos')`.


**Linha 350 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `403`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 351 — Assign** (nível 2 do bloco).

Associa `registro` a a chamada `AuditoriaAcaoCritica.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave.


**Linha 352 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.usuario`, `self.doador`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 353 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.resultado`, `AuditoriaAcaoCritica.Resultado.BLOQUEADO`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 354 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.metadados['evento']`, `'TENTATIVA_ACESSO'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 356 — FunctionDef** (nível 1 do bloco).

Define `test_acesso_a_triagem_registra_alvo_sem_respostas(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: acesso a triagem registra alvo sem respostas.

Bloco `body` da linha 356:

**Linha 357 — ImportFrom** (nível 2 do bloco).

Importa de `.models` os nomes `Triagem`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 358 — Assign** (nível 2 do bloco).

Associa `triagem` a a chamada `Triagem.objects.create`, que cria e persiste um registro quando usado no manager do model; argumentos nomeados: `usuario=self.doador`, `modalidade=Triagem.Modalidade.EXTENSA`, `status=Triagem.Status.CONCLUIDA`, `mensagem_resultado='CONTEUDO_CLINICO_PRIVADO'`.

- `usuario=self.doador`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `modalidade=Triagem.Modalidade.EXTENSA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `status=Triagem.Status.CONCLUIDA`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `mensagem_resultado='CONTEUDO_CLINICO_PRIVADO'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 361 — Expr** (nível 2 do bloco).

Executa a chamada `self.client.force_login`, que autentica o cliente de teste sem testar a senha; argumentos posicionais: `self.doador`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 362 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `self.client.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `reverse('accounts:triagem_resultado', kwargs={'id_triagem': triagem.pk})`.


**Linha 363 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `resposta.status_code`, `200`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 364 — Assign** (nível 2 do bloco).

Associa `registro` a a chamada `AuditoriaAcaoCritica.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave.


**Linha 365 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.acao`, `AuditoriaAcaoCritica.Acao.ACESSO_DADOS_SENSIVEIS`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 366 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.metadados['parametros']['id_triagem']`, `triagem.pk`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 367 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotIn`; argumentos posicionais: `'CONTEUDO_CLINICO_PRIVADO'`, `str(registro.metadados)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 369 — FunctionDef** (nível 1 do bloco).

Define `test_auditoria_exclusiva_administrador_e_somente_leitura(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: auditoria exclusiva administrador e somente leitura.

Bloco `body` da linha 369:

**Linha 370 — ImportFrom** (nível 2 do bloco).

Importa de `django.contrib` os nomes `admin`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 371 — ImportFrom** (nível 2 do bloco).

Importa de `django.test` os nomes `RequestFactory`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 372 — ImportFrom** (nível 2 do bloco).

Importa de `django.contrib.auth.models` os nomes `Permission`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 373 — Assign** (nível 2 do bloco).

Associa `modelo_admin` a o item ou recorte `AuditoriaAcaoCritica` de `admin.site._registry`.

**Linha 374 — Assign** (nível 2 do bloco).

Associa `request` a a chamada `RequestFactory().get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'/admin/'`.


**Linha 375 — Assign** (nível 2 do bloco).

Associa `request.user` a o atributo `admin` de `self`.

**Linha 376 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertTrue`, que o teste exige que a expressão seja verdadeira; argumentos posicionais: `modelo_admin.has_view_permission(request)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 377 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `modelo_admin.has_add_permission(request)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 378 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `modelo_admin.has_change_permission(request)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 379 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `modelo_admin.has_delete_permission(request)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 380 — Assign** (nível 2 do bloco).

Associa `self.doador.is_staff` a o valor literal `True`.

**Linha 381 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador.save`, que persiste a instância; update_fields limita os campos gravados. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 382 — Expr** (nível 2 do bloco).

Executa a chamada `self.doador.user_permissions.add`; argumentos posicionais: `Permission.objects.get(codename='view_auditoriaacaocritica')`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 383 — Assign** (nível 2 do bloco).

Associa `request.user` a a chamada `Usuario.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `pk=self.doador.pk`.

- `pk=self.doador.pk`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 384 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `modelo_admin.has_view_permission(request)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 385 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertFalse`, que o teste exige que a expressão seja falsa; argumentos posicionais: `modelo_admin.has_module_permission(request)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 387 — FunctionDef** (nível 1 do bloco).

Define `test_suspensao_registrada_sem_duplicar_dados_pessoais(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: suspensao registrada sem duplicar dados pessoais.

Bloco `body` da linha 387:

**Linha 388 — ImportFrom** (nível 2 do bloco).

Importa de `django.contrib` os nomes `admin`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 389 — ImportFrom** (nível 2 do bloco).

Importa de `django.test` os nomes `RequestFactory`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 390 — Assign** (nível 2 do bloco).

Associa `request` a a chamada `RequestFactory().post`; argumentos posicionais: `'/admin/'`.


**Linha 391 — Assign** (nível 2 do bloco).

Associa `request.user` a o atributo `admin` de `self`.

**Linha 392 — Assign** (nível 2 do bloco).

Associa `self.doador.is_active` a o valor literal `False`.

**Linha 393 — Assign** (nível 2 do bloco).

Associa `self.doador.nome` a o valor literal `'Nome atualizado'`.

**Linha 394 — Expr** (nível 2 do bloco).

Executa a chamada `admin.site._registry[Usuario].save_model`; argumentos posicionais: `request`, `self.doador`, `None`, `True`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 395 — Assign** (nível 2 do bloco).

Associa `registro` a a chamada `AuditoriaAcaoCritica.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave.


**Linha 396 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.metadados['evento']`, `'SUSPENSAO_USUARIO'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 397 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.metadados['alteracoes']['is_active']`, `{'antes': 'True', 'depois': 'False'}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 398 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIn`; argumentos posicionais: `'nome'`, `registro.metadados['campos_alterados']`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 399 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotIn`; argumentos posicionais: `'Nome atualizado'`, `str(registro.metadados)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 401 — FunctionDef** (nível 1 do bloco).

Define `test_login_suspeito_nao_afirma_bloqueio(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: login suspeito nao afirma bloqueio.

Bloco `body` da linha 401:

**Linha 402 — ImportFrom** (nível 2 do bloco).

Importa de `.signals` os nomes `auditar_login_falho`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 403 — ImportFrom** (nível 2 do bloco).

Importa de `django.test` os nomes `RequestFactory`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 404 — Assign** (nível 2 do bloco).

Associa `request` a a chamada `RequestFactory().post`; argumentos posicionais: `'/login/'`.


**Linha 405 — For** (nível 2 do bloco).

Percorre `range(5)`; cada item é atribuído a `_` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 405:

**Linha 406 — Expr** (nível 3 do bloco).

Executa a chamada `auditar_login_falho`; argumentos posicionais: `None`, `{'username': 'tentativa@elo.test', 'password': 'SEGREDO'}`, `request`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 407 — Assign** (nível 2 do bloco).

Associa `registro` a a chamada `AuditoriaAcaoCritica.objects.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.LOGIN_SUSPEITO`.

- `acao=AuditoriaAcaoCritica.Acao.LOGIN_SUSPEITO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 408 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.resultado`, `AuditoriaAcaoCritica.Resultado.FALHA`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 409 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotIn`; argumentos posicionais: `'SEGREDO'`, `str(registro.metadados)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 411 — FunctionDef** (nível 1 do bloco).

Define `test_sanitizacao_recursiva(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: sanitizacao recursiva.

Bloco `body` da linha 411:

**Linha 412 — ImportFrom** (nível 2 do bloco).

Importa de `.auditoria` os nomes `registrar_auditoria`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 413 — Assign** (nível 2 do bloco).

Associa `registro` a a chamada `registrar_auditoria`; argumentos nomeados: `acao=AuditoriaAcaoCritica.Acao.MODERACAO`, `metadados={'dados': [{'password': 'SEGREDO', 'TOKEN': 'SEGREDO', 'evento': 'teste'}]}`.

- `acao=AuditoriaAcaoCritica.Acao.MODERACAO`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `metadados={'dados': [{'password': 'SEGREDO', 'TOKEN': 'SEGREDO', 'evento': 'teste'}]}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 415 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertNotIn`; argumentos posicionais: `'SEGREDO'`, `str(registro.metadados)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 416 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `registro.metadados['dados'][0]['evento']`, `'teste'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 418 — FunctionDef** (nível 1 do bloco).

Define `test_ip_nao_confia_em_cabecalho_do_cliente(self)`. O corpo só executa quando a função/método é chamado. Cenário do teste: ip nao confia em cabecalho do cliente.

Bloco `body` da linha 418:

**Linha 419 — ImportFrom** (nível 2 do bloco).

Importa de `.auditoria` os nomes `obter_ip`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 420 — ImportFrom** (nível 2 do bloco).

Importa de `django.test` os nomes `RequestFactory`. Pontos iniciais indicam importação relativa ao pacote.

**Linha 421 — Assign** (nível 2 do bloco).

Associa `request` a a chamada `RequestFactory().get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'/login/'`; argumentos nomeados: `REMOTE_ADDR='127.0.0.1'`, `HTTP_X_FORWARDED_FOR='IP_FORJADO'`.

- `REMOTE_ADDR='127.0.0.1'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `HTTP_X_FORWARDED_FOR='IP_FORJADO'`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 422 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertEqual`, que o teste exige igualdade entre valor obtido e esperado; argumentos posicionais: `obter_ip(request)`, `'127.0.0.1'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 423 — Assign** (nível 2 do bloco).

Associa `request.META['REMOTE_ADDR']` a o valor literal `'IP_INVALIDO'`.

**Linha 424 — Expr** (nível 2 do bloco).

Executa a chamada `self.assertIsNone`; argumentos posicionais: `obter_ip(request)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

