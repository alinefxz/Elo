"""Prepara contas ficticias para testar os perfis no ambiente local."""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from accounts.models import ConsentimentoLGPD, Triagem, Usuario


class Command(BaseCommand):
    help = "Cria contas ficticias de cada perfil, sem substituir contas existentes."

    def add_arguments(self, parser):
        parser.add_argument('--senha', default='EloTeste2026!', help='Senha das novas contas de teste.')

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError('Este comando exige DEBUG=True no ambiente de desenvolvimento.')
        if len(options['senha']) < 8:
            raise CommandError('Use uma senha com pelo menos oito caracteres.')

        perfis = [
            ('doador', Usuario.Perfil.DOADOR, {}),
            ('doador-inapto', Usuario.Perfil.DOADOR, {}),
            ('doador-sem-consentimento', Usuario.Perfil.DOADOR, {}),
            ('receptor', Usuario.Perfil.RECEPTOR, {}),
            ('observador', Usuario.Perfil.OBSERVADOR, {}),
            ('administrador', Usuario.Perfil.ADMINISTRADOR, {'is_staff': True, 'is_superuser': True}),
        ]
        for status in Usuario.StatusValidacaoHemocentro.values:
            perfis.append((f'hemocentro-{status.lower()}', Usuario.Perfil.HEMOCENTRO,
                           {'status_validacao': status}))

        for nome, perfil, extras in perfis:
            email = f'{nome}@teste.elo.test'
            if Usuario.objects.filter(email=email).exists():
                self.stdout.write(f'Mantida sem alteracoes: {email}')
                continue
            usuario = Usuario.objects.create_user(
                email=email, password=options['senha'], nome=f'TESTE {nome}', perfil=perfil,
                cidade='Belo Horizonte', estado='MG',
                tipo_sanguineo='O-' if perfil == Usuario.Perfil.DOADOR else '',
                aceita_notificacoes_pedidos=perfil == Usuario.Perfil.DOADOR,
                **extras,
            )
            ConsentimentoLGPD.objects.create(
                usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.GERAL, aceito=True,
            )
            if perfil == Usuario.Perfil.DOADOR:
                Triagem.objects.create(
                    usuario=usuario, status=Triagem.Status.CONCLUIDA,
                    resultado=(Triagem.Resultado.INAPTO_TEMPORARIO if nome == 'doador-inapto'
                               else Triagem.Resultado.APTO),
                    finalizada_em=timezone.now(),
                )
                if nome != 'doador-sem-consentimento':
                    ConsentimentoLGPD.objects.create(
                        usuario=usuario, tipo_termo=ConsentimentoLGPD.TipoTermo.NOTIFICACOES,
                        versao_termo=settings.CONVOCACAO_VERSAO_CONSENTIMENTO, aceito=True,
                    )
            self.stdout.write(self.style.SUCCESS(f'Criada: {email}'))
        self.stdout.write('Contas existentes e suas senhas foram preservadas. Veja TESTAR_PERFIS.md.')
