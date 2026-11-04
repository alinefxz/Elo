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

