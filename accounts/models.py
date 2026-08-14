"""
RESUMO DO ARQUIVO
=================
Este arquivo descreve os dados que o Django guarda no PostgreSQL.

Ele possui dois modelos concretos:

1. ``Usuario``: conta comum usada para cadastro e login por e-mail.
2. ``ConsentimentoLGPD``: comprovante de que o usuario aceitou os termos.

``Usuario`` herda recursos prontos de ``AbstractUser`` (senha segura, sessoes,
permissoes e acesso ao admin), mas a classe deste arquivo NAO e abstrata. Ela
gera a tabela real ``usuarios`` no banco.

Esta etapa nao define Doador, Receptor, Hemocentro ou outros perfis. Esses
modelos e regras poderao ser relacionados ao usuario comum em outra etapa.
"""

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UsuarioManager(BaseUserManager):
    """
    Responsavel por criar contas corretamente.

    Um manager e a interface usada em chamadas como
    ``Usuario.objects.create_user(...)``. Como o projeto retirou o ``username``
    padrao e usa e-mail no login, o manager tambem precisa trabalhar com e-mail.
    """

    # Permite que o Django registre este manager nos arquivos de migration.
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        Cria uma conta comum.

        ``extra_fields`` recebe campos adicionais, como ``nome`` ou
        ``is_active``, sem obrigar o metodo a declarar cada campo separadamente.
        """

        # Uma conta sem e-mail nao poderia ser identificada no login.
        if not email:
            raise ValueError("O e-mail e obrigatorio.")

        # normalize_email ajusta o dominio; lower evita diferenca entre
        # Pessoa@Email.com e pessoa@email.com no uso pratico do sistema.
        email = self.normalize_email(email).lower()

        # self.model representa a classe Usuario associada a este manager.
        # O objeto ainda existe apenas na memoria neste momento.
        usuario = self.model(email=email, **extra_fields)

        # Nunca se deve fazer usuario.password = password.
        # set_password gera um hash com salt usando o sistema seguro do Django.
        usuario.set_password(password)

        # save executa o INSERT no banco configurado em settings.py.
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Cria a conta tecnica que pode acessar ``/admin/``.

        Isso nao representa um perfil de negocio do Elo. ``is_staff`` e
        ``is_superuser`` sao permissoes internas do painel administrativo.
        """

        # setdefault preenche apenas quando o valor nao foi informado.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # As verificacoes impedem a criacao acidental de um superusuario sem
        # as permissoes que o proprio comando createsuperuser exige.
        if extra_fields.get("is_staff") is not True:
            raise ValueError("O superusuario precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("O superusuario precisa ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    """
    Conta comum do Elo, autenticada por e-mail.

    ``AbstractUser`` fornece campos e metodos de autenticacao, mas permite que
    o projeto adapte a conta. Aqui retiramos username/first_name/last_name e
    usamos ``nome`` e ``email``. Como ``Meta.abstract`` nao foi definido, esta
    classe e concreta e cria uma tabela no PostgreSQL.
    """

    # Esses campos pertenciam ao usuario padrao do Django. O Elo usa um unico
    # nome completo e o e-mail como identificador, portanto nao precisa deles.
    username = None
    first_name = None
    last_name = None

    # Chave primaria: identifica cada linha da tabela de forma unica.
    id_usuario = models.BigAutoField(primary_key=True)

    # Dados comuns a qualquer pessoa que tenha uma conta no sistema.
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    # AbstractUser ja trabalha com um atributo chamado password. A redefinicao
    # abaixo preserva esse nome no Python, mas usa ``senha_hash`` no PostgreSQL.
    # O valor gravado e o hash produzido por set_password, nunca a senha pura.
    password = models.CharField(max_length=128, db_column="senha_hash")

    # is_active e consultado automaticamente pelo backend de autenticacao.
    # Uma conta inativa continua no banco, mas nao consegue entrar no sistema.
    is_active = models.BooleanField(default=True, db_column="ativo")

    # Campo preparado para uma futura confirmacao por e-mail. Nesta entrega ele
    # comeca como False, pois o envio e a confirmacao ainda nao foram criados.
    email_verificado = models.BooleanField(default=False)

    # auto_now_add grava a data somente no INSERT. auto_now atualiza a data a
    # cada save posterior. USE_TZ=True faz o Django tratar datas com fuso.
    date_joined = models.DateTimeField(
        auto_now_add=True,
        db_column="data_cadastro",
    )
    atualizado_em = models.DateTimeField(auto_now=True)

    # Substitui o manager herdado pelo manager que entende login por e-mail.
    objects = UsuarioManager()

    # USERNAME_FIELD nao precisa ser um username literal. Ele informa ao Django
    # qual campo unico sera usado pelo authenticate() e pelo formulario de login.
    USERNAME_FIELD = "email"

    # createsuperuser sempre pede USERNAME_FIELD e senha. REQUIRED_FIELDS inclui
    # os outros dados que tambem devem ser solicitados pelo comando.
    REQUIRED_FIELDS = ["nome"]

    class Meta:
        """Opcoes de banco e nomes exibidos pelo Django."""

        # Sem db_table, o nome automatico seria accounts_usuario.
        db_table = "usuarios"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

        # Afeta consultas sem order_by explicito, principalmente no admin.
        ordering = ["nome"]

    def clean(self):
        """Normaliza o e-mail quando o model passa por validacao completa."""

        # Mantem as validacoes que AbstractUser ja conhece.
        super().clean()
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email).lower()

    def get_full_name(self):
        """Retorna o nome completo no formato esperado pelo Django."""

        return self.nome

    def get_short_name(self):
        """Retorna o primeiro nome; usa o e-mail como alternativa."""

        return self.nome.split()[0] if self.nome else self.email

    def __str__(self):
        """Representacao legivel no admin, logs e terminal do Django."""

        return f"{self.nome} ({self.email})"


class ConsentimentoLGPD(models.Model):
    """
    Guarda a prova do aceite dos termos por uma conta.

    O consentimento fica em tabela separada para possuir data, versao e IP
    proprios. Isso tambem permite registrar novas versoes no futuro sem apagar
    o historico anterior.
    """

    class TipoTermo(models.TextChoices):
        """Tipos disponiveis nesta entrega basica."""

        GERAL = "GERAL", "Termos gerais e politica de privacidade"

    id_consentimento = models.BigAutoField(primary_key=True)

    # ForeignKey cria a coluna id_usuario e relaciona o aceite a uma conta.
    # settings.AUTH_USER_MODEL evita importar Usuario diretamente e e a forma
    # recomendada quando o projeto usa um modelo de autenticacao personalizado.
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consentimentos_lgpd",
        db_column="id_usuario",
    )

    tipo_termo = models.CharField(
        max_length=20,
        choices=TipoTermo.choices,
        default=TipoTermo.GERAL,
    )

    # A versao identifica exatamente qual texto foi aceito.
    versao_termo = models.CharField(max_length=20, default="1.0")
    aceito = models.BooleanField(default=False)

    # A data e preenchida automaticamente apenas na criacao do registro.
    data_aceite = models.DateTimeField(auto_now_add=True)

    # IP pode ser IPv4 ou IPv6. null/blank permitem uso em ambientes onde o IP
    # nao esteja disponivel, como alguns testes ou tarefas administrativas.
    ip = models.GenericIPAddressField(null=True, blank=True)

    # Enquanto o consentimento estiver valido, revogado_em permanece NULL.
    revogado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "consentimentos_lgpd"
        verbose_name = "consentimento LGPD"
        verbose_name_plural = "consentimentos LGPD"
        ordering = ["-data_aceite"]

        # Impede duplicar o mesmo termo e a mesma versao para o mesmo usuario.
        # Uma nova versao continua permitida e preserva o historico.
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "tipo_termo", "versao_termo"],
                name="consentimento_unico_por_versao",
            )
        ]

    def __str__(self):
        return f"{self.usuario.email} - {self.get_tipo_termo_display()}"
