from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UsuarioManager(BaseUserManager):
    """Cria usuarios usando o e-mail como identificador de acesso."""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail e obrigatorio.")

        # Normaliza o dominio do e-mail e evita duplicidades por maiusculas.
        email = self.normalize_email(email).lower()
        usuario = self.model(email=email, **extra_fields)

        # set_password nunca salva a senha pura: ele gera um hash seguro.
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        # Um superusuario precisa das permissoes administrativas do Django.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("perfil", self.model.Perfil.ADMINISTRADOR)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("O superusuario precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("O superusuario precisa ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    """Usuario do Elo, autenticado por e-mail em vez de username."""

    class Perfil(models.TextChoices):
        DOADOR = "DOADOR", "Doador"
        RECEPTOR = "RECEPTOR", "Receptor"
        HEMOCENTRO = "HEMOCENTRO", "Hemocentro"
        OBSERVADOR = "OBSERVADOR", "Observador"
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"

    class Sexo(models.TextChoices):
        FEMININO = "F", "Feminino"
        MASCULINO = "M", "Masculino"
        OUTRO = "O", "Outro"
        NAO_INFORMADO = "N", "Prefiro nao informar"

    # Estes campos do AbstractUser nao sao usados, pois o Elo usa nome e e-mail.
    username = None
    first_name = None
    last_name = None

    id_usuario = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    # O nome da coluna segue a documentacao; o Django continua gerando o hash.
    password = models.CharField(max_length=128, db_column="senha_hash")

    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    cnpj = models.CharField(max_length=14, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=Sexo.choices, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    perfil = models.CharField(max_length=20, choices=Perfil.choices)

    # is_active e usado automaticamente pelo Django para permitir ou bloquear login.
    is_active = models.BooleanField(default=True, db_column="ativo")
    email_verificado = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, db_column="data_cadastro")
    atualizado_em = models.DateTimeField(auto_now=True)

    objects = UsuarioManager()

    # O campo informado no login sera o e-mail.
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome"]

    class Meta:
        db_table = "usuarios"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ["nome"]

    def clean(self):
        super().clean()
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email).lower()

    def get_full_name(self):
        return self.nome

    def get_short_name(self):
        return self.nome.split()[0] if self.nome else self.email

    def __str__(self):
        return f"{self.nome} ({self.email})"


class ConsentimentoLGPD(models.Model):
    """Registra quando e de onde o usuario aceitou um termo do sistema."""

    class TipoTermo(models.TextChoices):
        GERAL = "GERAL", "Termos gerais e politica de privacidade"
        TRIAGEM = "TRIAGEM", "Termo de triagem"
        NOTIFICACOES = "NOTIFICACOES", "Termo de notificacoes"

    id_consentimento = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consentimentos_lgpd",
        db_column="id_usuario",
    )
    tipo_termo = models.CharField(max_length=20, choices=TipoTermo.choices)
    versao_termo = models.CharField(max_length=20, default="1.0")
    aceito = models.BooleanField(default=False)
    data_aceite = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    revogado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "consentimentos_lgpd"
        verbose_name = "consentimento LGPD"
        verbose_name_plural = "consentimentos LGPD"
        ordering = ["-data_aceite"]
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "tipo_termo", "versao_termo"],
                name="consentimento_unico_por_versao",
            )
        ]

    def __str__(self):
        return f"{self.usuario.email} - {self.get_tipo_termo_display()}"