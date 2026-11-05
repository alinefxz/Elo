<<<<<<< HEAD
from django.test import TestCase
from django.urls import reverse

from .forms import CadastroUsuarioForm, FiltroEstoquePublicoForm, FiltroPedidoSangueForm
from .models import Estoque, PedidoSangue, Usuario


class LocalidadesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.minas = Usuario.objects.create_user(
            email='hemo-mg@local.test', nome='Hemocentro MG', perfil=Usuario.Perfil.HEMOCENTRO,
            status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO,
            cidade='Pouso Alegre', estado='MG',
        )
        cls.outro_estado = Usuario.objects.create_user(
            email='hemo-sp@local.test', nome='Hemocentro SP', perfil=Usuario.Perfil.HEMOCENTRO,
            status_validacao=Usuario.StatusValidacaoHemocentro.APROVADO,
            cidade='Campinas', estado='SP',
        )
        Usuario.objects.create_user(
            email='privado@local.test', nome='Pendente', perfil=Usuario.Perfil.HEMOCENTRO,
            cidade='Cidade privada', estado='MG',
        )
        for hemo in (cls.minas, cls.outro_estado):
            Estoque.objects.create(hemocentro=hemo, tipo_sanguineo='O-', quantidade_bolsas=12,
                                   nivel_minimo=10, nivel_critico=5, status_calculado='ESTAVEL')
            PedidoSangue.objects.create(
                hemocentro_destino=hemo, nome_solicitante='Solicitante', contato='contato@local.test',
                para_quem=PedidoSangue.ParaQuem.MIM, titulo='Pedido publicado', tipo_sanguineo='O-',
                cidade=hemo.cidade, descricao='Pedido de sangue para atendimento.',
                urgencia=PedidoSangue.Urgencia.MEDIA, status=PedidoSangue.Status.PUBLICADA,
            )

    def test_cadastro_aceita_pessoa_de_fora_da_regiao_e_cidade_fora_da_lista(self):
        dados = {'nome': 'Pessoa de outra região', 'email': 'pessoa@local.test',
                 'perfil': Usuario.Perfil.OBSERVADOR, 'estado': 'SP', 'cidade': 'Santos',
                 'password1': 'SenhaForteLocal123!', 'password2': 'SenhaForteLocal123!', 'aceite_lgpd': True}
        form = CadastroUsuarioForm(dados)
        self.assertTrue(form.is_valid(), form.errors)
        usuario = form.save()
        self.assertEqual((usuario.estado, usuario.cidade), ('SP', 'Santos'))

    def test_cadastro_mostra_ufs_e_sugestoes_publicas_sem_expor_cadastros_pendentes(self):
        html = str(CadastroUsuarioForm()['cidade'])
        self.assertIn('<datalist', html)
        self.assertIn('Pouso Alegre', html)
        self.assertIn('Campinas', html)
        self.assertNotIn('Cidade privada', html)
        self.assertEqual(len(CadastroUsuarioForm().fields['estado'].choices), 28)

    def test_filtros_oferecem_cidades_e_preservam_busca_parcial(self):
        for classe in (FiltroEstoquePublicoForm, FiltroPedidoSangueForm):
            with self.subTest(formulario=classe.__name__):
                form = classe({'cidade': 'Pouso', 'estado': 'MG'})
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data['cidade'], 'Pouso')
                self.assertIn('Pouso Alegre', str(form['cidade']))
                self.assertNotIn('Cidade privada', str(form['cidade']))
                self.assertIn('<select', str(form['cidade']))

    def test_filtro_estoque_por_estado(self):
        response = self.client.get(reverse('accounts:estoque_publico'), {'estado': 'SP'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hemocentro SP')
        self.assertNotContains(response, 'Hemocentro MG')

    def test_filtro_pedidos_por_estado(self):
        response = self.client.get(reverse('accounts:consultar_pedidos'), {'estado': 'MG'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hemocentro MG')
        self.assertNotContains(response, 'Hemocentro SP')

    def test_estado_inexistente_rejeitado_no_formulario(self):
        self.assertFalse(FiltroEstoquePublicoForm({'estado': 'XX'}).is_valid())

=======
"""Contratos para localidades controladas nos formulários públicos."""

from django import forms
from django.test import TestCase
from django.urls import reverse

from .forms import CadastroUsuarioForm, FiltroPedidoSangueForm, PedidoSangueForm
from .localidades import CIDADES_POR_ESTADO, ESTADOS_CHOICES
from .models import PedidoSangue, Usuario


class CatalogoLocalidadesTests(TestCase):
    """Protege as localidades disponíveis para novas submissões."""

    def dados_cadastro(self, **alteracoes):
        dados = {
            "nome": "Pessoa de teste",
            "email": "pessoa@elo.test",
            "perfil": Usuario.Perfil.OBSERVADOR,
            "telefone": "",
            "data_nascimento": "",
            "sexo": "",
            "estado": "SP",
            "cidade": "São Paulo",
            "password1": "SenhaForte123!",
            "password2": "SenhaForte123!",
            "aceite_lgpd": "on",
        }
        dados.update(alteracoes)
        return dados

    def test_catalogo_expoe_localidades_operacionais_de_sao_paulo(self):
        """Falha se uma nova submissão puder usar catálogo diferente do operacional."""

        self.assertEqual(
            CIDADES_POR_ESTADO,
            {"SP": ("São Paulo", "Campinas", "Santos")},
        )
        self.assertEqual(ESTADOS_CHOICES, [("SP", "SP")])

    def test_cadastro_renderiza_estado_e_cidade_como_seletores(self):
        """Falha se cadastro voltar a aceitar UF/cidade livres no navegador."""

        form = CadastroUsuarioForm()

        self.assertIsInstance(form.fields["estado"], forms.ChoiceField)
        self.assertIsInstance(form.fields["cidade"], forms.ChoiceField)
        self.assertEqual(form.fields["cidade"].widget.attrs["data-estado"], "estado")

    def test_cadastro_aceita_par_operacional_de_uf_e_cidade(self):
        """Falha se o par SP/São Paulo deixar de ser aceito no servidor."""

        form = CadastroUsuarioForm(self.dados_cadastro())

        self.assertTrue(form.is_valid(), form.errors)

    def test_cadastro_rejeita_cidade_de_outra_uf(self):
        """Falha se a validação deixar passar uma cidade que não pertence à UF."""

        form = CadastroUsuarioForm(self.dados_cadastro(cidade="Belo Horizonte"))

        self.assertFalse(form.is_valid())
        self.assertIn("cidade", form.errors)

    def test_pedido_tem_estado_aditivo_e_seletores_controlados(self):
        """Falha se pedido novo não registrar UF junto à cidade escolhida."""

        form = PedidoSangueForm()

        self.assertEqual(PedidoSangue._meta.get_field("estado").max_length, 2)
        self.assertIsInstance(form.fields["estado"], forms.ChoiceField)
        self.assertIsInstance(form.fields["cidade"], forms.ChoiceField)

    def test_paginas_de_submissao_carregam_filtro_de_cidade_no_navegador(self):
        """Falha se o seletor de cidade não reagir à UF sem novo POST."""

        for rota in ("accounts:cadastro", "accounts:pedido_publicar"):
            with self.subTest(rota=rota):
                resposta = self.client.get(reverse(rota))

                self.assertContains(resposta, "js/localidades.js")

    def test_filtro_de_pedidos_mantem_busca_textual_legada_por_cidade(self):
        """Falha se a consulta histórica deixar de aceitar cidades fora do catálogo."""

        form = FiltroPedidoSangueForm({"cidade": "Muzambinho"})

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["cidade"], "Muzambinho")
>>>>>>> fix/unboundlocal-form-pedido-2026-10-09
