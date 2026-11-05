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
