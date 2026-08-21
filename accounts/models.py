"""
RESUMO DO ARQUIVO
=================
Este arquivo descreve os dados que o Django guarda no PostgreSQL.

- Usuario: guarda a conta, os dados basicos e o tipo de perfil escolhido.
- ConsentimentoLGPD: guarda quando a pessoa aceitou cada termo.
- AuditoriaAcaoCritica: registra eventos sensiveis para rastreabilidade.

O usuario herda de AbstractUser para aproveitar senha segura, login, sessao,
grupos e permissoes do Django. Mesmo herdando de uma classe chamada
AbstractUser, a classe Usuario abaixo e concreta e cria a tabela ``usuarios``.

O campo perfil identifica Doador, Receptor/Solicitante, Hemocentro,
Observador ou Administrador. As views usam esse valor para montar a experiencia
inicial de cada tipo de usuario no dashboard.
"""

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UsuarioManager(BaseUserManager):
    """
    Centraliza a criacao das contas.

    O Django normalmente cria usuarios por username. O Elo usa e-mail, entao
    este manager ensina ``Usuario.objects`` a receber, padronizar e salvar o
    e-mail corretamente tanto para contas comuns quanto para administradores.
    """

    # Permite que o Django conheca este manager durante as migrations.
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Cria uma conta comum e grava a senha de forma segura."""

        if not email:
            raise ValueError("O e-mail e obrigatorio.")

        # Padroniza o e-mail para evitar diferencas por letras maiusculas.
        # Exemplo: MARIA@EXAMPLE.COM e maria@example.com viram o mesmo padrao.
        email = self.normalize_email(email).lower()

        # self.model representa Usuario. extra_fields carrega os outros dados,
        # como nome, perfil e documento, sem repetir todos os parametros aqui.
        usuario = self.model(email=email, **extra_fields)

        # Gera o hash da senha. A senha original nunca vai para o banco.
        usuario.set_password(password)

        # Executa o INSERT no banco configurado em settings.py. self._db deixa
        # o metodo compativel caso o projeto use mais de um banco no futuro.
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        """Cria a conta tecnica que pode acessar o painel /admin/."""

        # setdefault preenche o valor somente quando ele nao foi informado.
        # is_staff permite entrar no admin. is_superuser libera todas as
        # permissoes internas do Django. perfil registra a classificacao do Elo.
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
    """
    Conta concreta do Elo, com login por e-mail.

    AbstractUser fornece recursos prontos e testados: hash de senha, ultimo
    login, grupos, permissoes e compatibilidade com o admin. A palavra
    "Abstract" pertence a classe de origem; ``Usuario`` e concreto e cria a
    tabela real ``usuarios`` porque nao foi marcado como abstrato.
    """

    class Perfil(models.TextChoices):
        """Tipos que podem ser escolhidos no cadastro."""

        DOADOR = "DOADOR", "Doador"
        RECEPTOR = "RECEPTOR", "Receptor"
        HEMOCENTRO = "HEMOCENTRO", "Hemocentro"
        OBSERVADOR = "OBSERVADOR", "Observador"
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"

    class Sexo(models.TextChoices):
        """Opcoes fechadas para manter os dados padronizados."""

        FEMININO = "F", "Feminino"
        MASCULINO = "M", "Masculino"
        OUTRO = "O", "Outro"
        NAO_INFORMADO = "N", "Prefiro nao informar"

    # O Elo usa um nome completo e e-mail. Por isso, estes tres campos do
    # usuario original do Django sao retirados. Escrever None diz ao ORM que
    # eles nao devem virar colunas da tabela usuarios.
    username = None
    first_name = None
    last_name = None

    # Chave primaria: numero unico de cada usuario.
    id_usuario = models.BigAutoField(primary_key=True)

    # Dados principais da conta.
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    # No Python o campo continua chamado password, como o Django espera.
    # No PostgreSQL a coluna se chama senha_hash, como definido no documento.
    password = models.CharField(max_length=128, db_column="senha_hash")

    # CPF e CNPJ podem ficar vazios, pois o formulario escolhe quando exigir:
    # Doador e Receptor/Solicitante usam CPF; Hemocentro usa CNPJ; Observador
    # tem um cadastro simples e pode ficar sem documento nesta etapa.
    # null=True grava NULL quando vazio. Isso permite varias contas sem CNPJ,
    # enquanto unique=True ainda impede repetir um documento preenchido.
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    cnpj = models.CharField(max_length=14, unique=True, null=True, blank=True)

    # Dados adicionais do cadastro. blank=True aceita o campo vazio durante a
    # validacao do model. O formulario publico pode ser mais exigente: nele a
    # data de nascimento e obrigatoria.
    telefone = models.CharField(max_length=20, blank=True, default="")
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(
        max_length=1,
        choices=Sexo.choices,
        blank=True,
        default="",
    )
    cidade = models.CharField(max_length=100, blank=True, default="")
    estado = models.CharField(max_length=2, blank=True, default="")

    # Guarda a classificacao inicial. choices limita os valores aceitos e cria
    # get_perfil_display(), usado no dashboard para mostrar um nome amigavel.
    # O valor padrao OBSERVADOR tambem protege criacoes internas que nao enviem
    # explicitamente um perfil.
    perfil = models.CharField(
        max_length=20,
        choices=Perfil.choices,
        default=Perfil.OBSERVADOR,
    )

    # Conta inativa permanece no banco, mas nao consegue fazer login.
    is_active = models.BooleanField(default=True, db_column="ativo")

    # O envio do e-mail de verificacao ainda sera implementado.
    email_verificado = models.BooleanField(default=False)

    # date_joined e preenchido uma vez na criacao. atualizado_em muda sempre
    # que save() atualiza o usuario.
    date_joined = models.DateTimeField(
        auto_now_add=True,
        db_column="data_cadastro",
    )
    atualizado_em = models.DateTimeField(auto_now=True)

    # Usa o manager personalizado definido acima.
    objects = UsuarioManager()

    # Define o e-mail como identificador de login.
    USERNAME_FIELD = "email"

    # O comando createsuperuser tambem perguntara o nome.
    REQUIRED_FIELDS = ["nome"]

    class Meta:
        # Sem db_table, o nome automatico seria accounts_usuario.
        db_table = "usuarios"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ["nome"]

    def clean(self):
        """Padroniza o e-mail quando o model e validado."""

        # Mantem primeiro as validacoes herdadas de AbstractUser.
        super().clean()
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email).lower()

    def get_full_name(self):
        """Devolve o nome completo no formato esperado pelo Django."""

        return self.nome

    def get_short_name(self):
        """Devolve o primeiro nome para saudacoes."""

        return self.nome.split()[0] if self.nome else self.email

    def __str__(self):
        """Texto usado para representar o usuario no admin e no terminal."""

        return f"{self.nome} ({self.email})"


class ConsentimentoLGPD(models.Model):
    """
    Guarda a prova de cada aceite de termo.

    O consentimento fica separado de Usuario porque precisa guardar sua propria
    versao, data e IP. Quando o texto do termo mudar, uma nova versao podera ser
    aceita sem apagar o registro da versao anterior.
    """

    class TipoTermo(models.TextChoices):
        GERAL = "GERAL", "Termos gerais e politica de privacidade"
        TRIAGEM = "TRIAGEM", "Termo de triagem"
        NOTIFICACOES = "NOTIFICACOES", "Termo de notificacoes"

    id_consentimento = models.BigAutoField(primary_key=True)

    # ForeignKey liga muitos consentimentos a um usuario. related_name permite
    # consultar no sentido contrario com usuario.consentimentos_lgpd.all().
    # CASCADE remove esses registros se a conta for removida.
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
    versao_termo = models.CharField(max_length=20, default="1.0")
    aceito = models.BooleanField(default=False)

    # auto_now_add preenche a data uma unica vez, no momento da criacao.
    data_aceite = models.DateTimeField(auto_now_add=True)

    # O IP pode ficar vazio em testes ou tarefas internas.
    ip = models.GenericIPAddressField(null=True, blank=True)

    # Fica vazio enquanto o consentimento continuar valido.
    revogado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "consentimentos_lgpd"
        verbose_name = "consentimento LGPD"
        verbose_name_plural = "consentimentos LGPD"
        ordering = ["-data_aceite"]

        # Esta regra tambem existe no PostgreSQL. Assim, mesmo que outro codigo
        # esqueca de validar, o banco nao aceita a mesma versao do mesmo termo
        # duas vezes para o mesmo usuario. Uma versao nova continua permitida.
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "tipo_termo", "versao_termo"],
                name="consentimento_unico_por_versao",
            )
        ]

    def __str__(self):
        return f"{self.usuario.email} - {self.get_tipo_termo_display()}"


class AuditoriaAcaoCritica(models.Model):
    """
    Registro imutavel de eventos sensiveis do Elo.

    A auditoria guarda o contexto da acao sem copiar senhas, tokens ou dados
    sensiveis completos. Cada tela ou rotina critica deve chamar a funcao
    central de auditoria em accounts/auditoria.py.
    """

    class Acao(models.TextChoices):
        LOGIN_FALHO = "LOGIN_FALHO", "Login falho"
        LOGIN_SUSPEITO = "LOGIN_SUSPEITO", "Login suspeito"
        ALTERACAO_PERMISSAO = "ALTERACAO_PERMISSAO", "Alteracao de permissao"
        APROVACAO_HEMOCENTRO = "APROVACAO_HEMOCENTRO", "Aprovacao de hemocentro"
        ATUALIZACAO_ESTOQUE = "ATUALIZACAO_ESTOQUE", "Atualizacao de estoque"
        MODERACAO = "MODERACAO", "Moderacao"
        ACESSO_DADOS_SENSIVEIS = (
            "ACESSO_DADOS_SENSIVEIS",
            "Acesso a dados sensiveis",
        )
        CONFIRMACAO_DOACAO = "CONFIRMACAO_DOACAO", "Confirmacao de doacao"

    class Resultado(models.TextChoices):
        SUCESSO = "SUCESSO", "Sucesso"
        FALHA = "FALHA", "Falha"
        BLOQUEADO = "BLOQUEADO", "Bloqueado"

    id_auditoria = models.BigAutoField(primary_key=True)

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="auditorias_acoes_criticas",
        db_column="id_usuario",
    )
    acao = models.CharField(max_length=40, choices=Acao.choices)
    resultado = models.CharField(
        max_length=20,
        choices=Resultado.choices,
        default=Resultado.SUCESSO,
    )

    alvo_tipo = models.CharField(max_length=80, blank=True, default="")
    alvo_id = models.CharField(max_length=80, blank=True, default="")
    descricao = models.CharField(max_length=255, blank=True, default="")

    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default="")
    metadados = models.JSONField(blank=True, default=dict)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auditorias_acoes_criticas"
        verbose_name = "auditoria de acao critica"
        verbose_name_plural = "auditorias de acoes criticas"
        ordering = ["-criado_em"]
        indexes = [
            models.Index(fields=["acao", "criado_em"], name="auditoria_acao_data_idx"),
            models.Index(
                fields=["usuario", "criado_em"],
                name="auditoria_usuario_data_idx",
            ),
            models.Index(fields=["ip", "criado_em"], name="auditoria_ip_data_idx"),
        ]

    def __str__(self):
        return f"{self.get_acao_display()} - {self.get_resultado_display()}"
