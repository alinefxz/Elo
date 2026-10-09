from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from .compatibilidade import doadores_aptos_para_convocacao
from .models import ConsentimentoLGPD, Triagem, Usuario


@override_settings(DEBUG=True)
class PerfisTesteTests(TestCase):
    def test_cria_perfis_e_preserva_alteracoes_ao_repetir(self):
        call_command('criar_perfis_teste', stdout=StringIO())
        self.assertEqual(Usuario.objects.count(), 10)
        self.assertEqual(set(Usuario.objects.values_list('perfil', flat=True)), set(Usuario.Perfil.values))
        self.assertEqual(list(doadores_aptos_para_convocacao('O-').values_list('email', flat=True)),
                         ['doador@teste.elo.test'])
        usuario = Usuario.objects.get(email='receptor@teste.elo.test')
        self.assertTrue(usuario.check_password('EloTeste2026!'))
        usuario.nome = 'Nome alterado no teste'
        usuario.set_password('OutraSenha123!')
        usuario.save()
        contagens = (Triagem.objects.count(), ConsentimentoLGPD.objects.count())
        call_command('criar_perfis_teste', senha='NovaSenha123!', stdout=StringIO())
        usuario.refresh_from_db()
        self.assertEqual(usuario.nome, 'Nome alterado no teste')
        self.assertTrue(usuario.check_password('OutraSenha123!'))
        self.assertEqual(Usuario.objects.count(), 10)
        self.assertEqual(contagens, (Triagem.objects.count(), ConsentimentoLGPD.objects.count()))

    @override_settings(DEBUG=False)
    def test_nao_cria_contas_fora_do_ambiente_de_desenvolvimento(self):
        with self.assertRaises(CommandError):
            call_command('criar_perfis_teste', stdout=StringIO())
        self.assertFalse(Usuario.objects.exists())
