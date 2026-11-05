"""Regressões do catálogo oficial, da edição de perfis e de envios legados."""

from datetime import date

from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import CadastroUsuarioForm, PedidoSangueForm
from .localidades import CIDADES_POR_ESTADO, ESTADOS
from .models import PedidoSangue, Usuario
from .perfil_forms import PerfilUsuarioForm


CAPITAIS = {
    'AC': 'Rio Branco', 'AL': 'Maceió', 'AP': 'Macapá', 'AM': 'Manaus',
    'BA': 'Salvador', 'CE': 'Fortaleza', 'DF': 'Brasília', 'ES': 'Vitória',
    'GO': 'Goiânia', 'MA': 'São Luís', 'MT': 'Cuiabá', 'MS': 'Campo Grande',
    'MG': 'Belo Horizonte', 'PA': 'Belém', 'PB': 'João Pessoa', 'PR': 'Curitiba',
    'PE': 'Recife', 'PI': 'Teresina', 'RJ': 'Rio de Janeiro', 'RN': 'Natal',
    'RS': 'Porto Alegre', 'RO': 'Porto Velho', 'RR': 'Boa Vista',
    'SC': 'Florianópolis', 'SP': 'São Paulo', 'SE': 'Aracaju', 'TO': 'Palmas',
}


@override_settings(PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher'])
class LocalidadesPerfilTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuarios = {}
        for papel in Usuario.Perfil.values:
            cls.usuarios[papel] = Usuario.objects.create_user(
                email=f'{papel.lower()}@localidades-perfil.test', nome=f'Conta {papel}',
                password='SenhaLocalidades2026!', perfil=papel, estado='SP', cidade='Santos',
                data_nascimento=None if papel == Usuario.Perfil.HEMOCENTRO else date(1990, 1, 1),
            )
        cls.hemocentro = cls.usuarios[Usuario.Perfil.HEMOCENTRO]
        cls.hemocentro.status_validacao = Usuario.StatusValidacaoHemocentro.APROVADO
        cls.hemocentro.save(update_fields=['status_validacao'])
        cls.privado = Usuario.objects.create_user(
            email='EMAIL_PRIVADO@localidades-perfil.test', nome='NOME_PRIVADO_NAO_CATALOGAR',
            perfil=Usuario.Perfil.HEMOCENTRO, estado='MG', cidade='CIDADE_PRIVADA_NAO_CATALOGAR',
            cnpj='98765432000198', telefone='35999999999',
        )

    def dados_perfil(self, usuario, **alteracoes):
        dados = {
            'nome': usuario.nome, 'email': usuario.email, 'telefone': usuario.telefone,
            'estado': usuario.estado, 'cidade': usuario.cidade,
            'data_nascimento': usuario.data_nascimento.isoformat() if usuario.data_nascimento else '',
            'sexo': usuario.sexo, 'tipo_sanguineo': usuario.tipo_sanguineo,
            'endereco': usuario.endereco, 'horario_funcionamento': usuario.horario_funcionamento,
        }
        return {**dados, **alteracoes}

    def dados_cadastro(self, estado='MG', cidade='Muzambinho', **alteracoes):
        return {
            'nome': 'Pessoa de outra região', 'email': f'pessoa-{estado.lower()}@localidades-perfil.test',
            'perfil': Usuario.Perfil.OBSERVADOR, 'estado': estado, 'cidade': cidade,
            'password1': 'SenhaCadastroLocal2026!', 'password2': 'SenhaCadastroLocal2026!',
            'aceite_lgpd': 'on', **alteracoes,
        }

    def dados_pedido(self, **alteracoes):
        return {
            'nome_solicitante': 'Pessoa solicitante', 'contato': 'pessoa@localidades-perfil.test',
            'para_quem': PedidoSangue.ParaQuem.MIM, 'hemocentro_destino': self.hemocentro.pk,
            'titulo': 'Necessidade registrada', 'tipo_sanguineo': 'O-',
            'urgencia': PedidoSangue.Urgencia.BAIXA, 'estado': 'MG', 'cidade': 'Belo Horizonte',
            'descricao': 'Solicitação para atendimento de uma necessidade de sangue.',
            **alteracoes,
        }

    def test_catalogo_e_formularios_oferecem_as_27_ufs(self):
        self.assertEqual(len(ESTADOS), 27)
        self.assertEqual(set(CIDADES_POR_ESTADO), set(CAPITAIS))
        self.assertGreaterEqual(sum(len(cidades) for cidades in CIDADES_POR_ESTADO.values()), 5500)
        for papel, usuario in self.usuarios.items():
            with self.subTest(papel=papel):
                escolhas = dict(PerfilUsuarioForm(instance=usuario).fields['estado'].choices)
                self.assertEqual(set(escolhas) - {''}, set(CAPITAIS))
        self.assertEqual(set(dict(CadastroUsuarioForm().fields['estado'].choices)) - {''}, set(CAPITAIS))

    def test_endpoint_publico_de_todas_as_ufs_inclui_capitais(self):
        url = reverse('accounts:localidades_cidades')
        for uf, capital in CAPITAIS.items():
            with self.subTest(uf=uf):
                resposta = self.client.get(url, {'estado': uf})
                self.assertEqual(resposta.status_code, 200)
                dados = resposta.json()
                self.assertEqual(set(dados), {'estado', 'cidades'})
                self.assertEqual(dados['estado'], uf)
                self.assertIn(capital, dados['cidades'])
                self.assertTrue(all(isinstance(cidade, str) for cidade in dados['cidades']))
                self.assertEqual(len(dados['cidades']), len(set(dados['cidades'])))

    def test_endpoint_inclui_interior_e_municipios_fora_da_regiao(self):
        amostras = {
            'MG': ('Muzambinho', 'Alfenas', 'Pouso Alegre'),
            'SP': ('Campinas', 'Santos', 'Ribeirão Preto'),
            'PA': ('Ananindeua',), 'MS': ('Dourados',),
            'PB': ('Campina Grande',), 'SC': ('Joinville',),
        }
        for estado, cidades in amostras.items():
            dados = self.client.get(reverse('accounts:localidades_cidades'), {'estado': estado}).json()
            for cidade in cidades:
                with self.subTest(estado=estado, cidade=cidade):
                    self.assertIn(cidade, dados['cidades'])

    def test_endpoint_filtra_uf_sem_consultar_nem_expor_contas_privadas(self):
        url = reverse('accounts:localidades_cidades')
        with self.assertNumQueries(0):
            resposta = self.client.get(url, {'estado': 'mg'})
        self.assertEqual(resposta.status_code, 200)
        cidades = resposta.json()['cidades']
        self.assertIn('Belo Horizonte', cidades)
        self.assertNotIn('São Paulo', cidades)
        for privado in (self.privado.nome, self.privado.email, self.privado.cidade, self.privado.cnpj, self.privado.telefone):
            self.assertNotContains(resposta, privado)
        self.client.force_login(self.usuarios[Usuario.Perfil.DOADOR])
        autenticado = self.client.get(url, {'estado': 'MG'})
        self.assertEqual(autenticado.json(), resposta.json())

    def test_endpoint_rejeita_uf_ausente_invalida_e_metodos_de_escrita(self):
        url = reverse('accounts:localidades_cidades')
        for parametros in ({}, {'estado': ''}, {'estado': 'XX'}, {'estado': 'MG,SP'}):
            with self.subTest(parametros=parametros):
                resposta = self.client.get(url, parametros)
                self.assertEqual(resposta.status_code, 400)
                self.assertIn('erro', resposta.json())
        self.assertEqual(self.client.post(url, {'estado': 'MG'}).status_code, 405)

    def test_cinco_perfis_persistem_localidade_valida_de_outra_regiao(self):
        for papel, usuario in self.usuarios.items():
            with self.subTest(papel=papel):
                self.client.force_login(usuario)
                resposta = self.client.post(reverse('accounts:perfil_editar'), self.dados_perfil(
                    usuario, estado='AC', cidade='Rio Branco',
                ))
                self.assertRedirects(resposta, reverse('accounts:perfil'))
                usuario.refresh_from_db()
                self.assertEqual((usuario.estado, usuario.cidade), ('AC', 'Rio Branco'))

    def test_cinco_perfis_rejeitam_municipio_de_outra_uf_sem_alterar_banco(self):
        for papel, usuario in self.usuarios.items():
            with self.subTest(papel=papel):
                self.client.force_login(usuario)
                resposta = self.client.post(reverse('accounts:perfil_editar'), self.dados_perfil(
                    usuario, estado='MG', cidade='São Paulo',
                ))
                self.assertEqual(resposta.status_code, 200)
                self.assertIn('cidade', resposta.context['form'].errors)
                usuario.refresh_from_db()
                self.assertEqual((usuario.estado, usuario.cidade), ('SP', 'Santos'))

    def test_perfil_preserva_localizacao_legada_desconhecida_ao_editar_outro_campo(self):
        for papel, usuario in self.usuarios.items():
            for uf in ('MG', 'ZZ'):
                with self.subTest(papel=papel, uf=uf):
                    usuario.estado = uf
                    usuario.cidade = 'Município legado desconhecido'
                    usuario.save(update_fields=['estado', 'cidade'])
                    form = PerfilUsuarioForm(self.dados_perfil(usuario, nome=f'Nome atualizado {papel}'), instance=usuario)
                    self.assertTrue(form.is_valid(), form.errors)
                    form.save()
                    usuario.refresh_from_db()
                    self.assertEqual((usuario.estado, usuario.cidade), (uf, 'Município legado desconhecido'))

    def test_perfil_rejeita_localizacao_legada_se_usuario_alterar_o_par(self):
        usuario = self.usuarios[Usuario.Perfil.DOADOR]
        usuario.estado = 'MG'
        usuario.cidade = 'Município legado desconhecido'
        usuario.save(update_fields=['estado', 'cidade'])
        form = PerfilUsuarioForm(self.dados_perfil(usuario, estado='SP'), instance=usuario)
        self.assertFalse(form.is_valid())
        self.assertIn('cidade', form.errors)

    def test_cadastro_aceita_e_persiste_localidades_de_varias_regioes(self):
        for uf, cidade in (
            ('MG', 'Muzambinho'), ('SP', 'Santos'), ('AM', 'Manaus'), ('BA', 'Salvador'),
            ('RS', 'Porto Alegre'), ('SC', 'Joinville'), ('DF', 'Brasília'), ('AC', 'Rio Branco'),
        ):
            with self.subTest(uf=uf, cidade=cidade):
                form = CadastroUsuarioForm(self.dados_cadastro(uf, cidade))
                self.assertTrue(form.is_valid(), form.errors)
                usuario = form.save()
                self.assertEqual((usuario.estado, usuario.cidade), (uf, cidade))

    def test_cadastro_exige_par_oficial_quando_localizacao_for_informada(self):
        for uf, cidade in (('MG', 'São Paulo'), ('MG', ''), ('', 'Santos'), ('XX', 'Santos')):
            with self.subTest(uf=uf, cidade=cidade):
                form = CadastroUsuarioForm(self.dados_cadastro(uf, cidade))
                self.assertFalse(form.is_valid())
                self.assertTrue({'cidade', 'estado'}.intersection(form.errors))
        form = CadastroUsuarioForm(self.dados_cadastro('', '', email='sem-localidade@localidades-perfil.test'))
        self.assertTrue(form.is_valid(), form.errors)

    def test_pedido_legado_sem_uf_informa_uf_de_municipio_univoco(self):
        for cidade, uf in (('Belo Horizonte', 'MG'), ('São Paulo', 'SP'), ('Manaus', 'AM')):
            for modo in ('ausente', 'vazio'):
                with self.subTest(cidade=cidade, modo=modo):
                    dados = self.dados_pedido(cidade=cidade, estado='')
                    if modo == 'ausente':
                        dados.pop('estado')
                    form = PedidoSangueForm(dados)
                    self.assertTrue(form.is_valid(), form.errors)
                    self.assertEqual(form.cleaned_data['estado'], uf)
                    self.assertEqual(form.cleaned_data['cidade'], cidade)

    def test_pedido_sem_uf_rejeita_cidade_ambigua_e_aceita_com_uf_explicita(self):
        dados = self.dados_pedido(estado='', cidade='Bom Jesus')
        form = PedidoSangueForm(dados)
        self.assertFalse(form.is_valid())
        self.assertIn('estado', form.errors)
        for uf in ('PI', 'RS'):
            with self.subTest(uf=uf):
                form = PedidoSangueForm({**dados, 'estado': uf})
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data['estado'], uf)

    def test_pedido_rejeita_localidade_inexistente_e_par_incompativel(self):
        for uf, cidade in (('', 'Município inventado'), ('MG', 'São Paulo'), ('SP', 'Belo Horizonte')):
            with self.subTest(uf=uf, cidade=cidade):
                form = PedidoSangueForm(self.dados_pedido(estado=uf, cidade=cidade))
                self.assertFalse(form.is_valid())
                self.assertTrue({'estado', 'cidade'}.intersection(form.errors))
