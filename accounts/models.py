"""
Resumo Do Arquivo
=================

Este arquivo descreve os dados que o Django guarda no PostgreSQL.

- Usuario: guarda a conta, os dados basicos, o tipo de perfil escolhido e o
  status atual de validacao quando a conta e de Hemocentro.

- ValidacaoHemocentro: guarda o historico de analises feitas por administradores.

- ConsentimentoLGPD: guarda quando a pessoa aceitou cada termo.

- AuditoriaAcaoCritica: registra eventos sensiveis para rastreabilidade.

O usuario herda de AbstractUser para aproveitar senha segura, login, sessao,
grupos e permissoes do Django. Mesmo herdando de uma classe chamada
AbstractUser, a classe Usuario abaixo e concreta e cria a tabela ``usuarios``
porque nao foi marcado como abstrato.

O campo perfil identifica Doador, Receptor/Solicitante, Hemocentro,
Observador ou Administrador. As views usam esse valor para montar a experiencia
inicial de cada tipo de usuario no dashboard.
"""

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

# Reaproveita a mesma lista de tipos sanguineos usada em compatibilidade.py,
# para nao correr o risco de duas listas divergentes no projeto.
from .compatibilidade import TIPOS_SANGUINEOS


class UsuarioManager(BaseUserManager):
    """
    Centraliza a criacao das contas.

    O Django normalmente cria usuarios por username. O Elo usa e-mail, entao
    este manager ensina ``Usuario.objects`` a receber, padronizar e salvar o
    e-mail corretamente tanto para contas comuns quanto para administradores.
    """

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Cria uma conta comum e grava a senha de forma segura."""

        if not email:
            raise ValueError("O e-mail e obrigatorio.")

        # Padroniza o e-mail para evitar diferencas por letras maiusculas.
        # Exemplo: MARIA@EXAMPLE.COM e maria@example.com viram o mesmo padrao.
        email = self.normalize_email(email).lower()

        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        """Cria a conta tecnica que pode acessar o painel /admin/."""

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

    class StatusValidacaoHemocentro(models.TextChoices):
        """Situacao institucional do Hemocentro dentro do Elo."""

        PENDENTE = "PENDENTE", "Pendente"
        APROVADO = "APROVADO", "Aprovado"
        RECUSADO = "RECUSADO", "Recusado"
        CORRECAO = "CORRECAO", "Correcao necessaria"

    username = None
    first_name = None
    last_name = None

    id_usuario = models.BigAutoField(primary_key=True)

    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, db_column="senha_hash")

    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    cnpj = models.CharField(max_length=14, unique=True, null=True, blank=True)

    telefone = models.CharField(max_length=20, blank=True, default="")
    data_nascimento = models.DateField(null=True, blank=True)

    sexo = models.CharField(
        max_length=1,
        choices=Sexo.choices,
        blank=True,
        default="",
    )

    tipo_sanguineo = models.CharField(
        max_length=3,
        choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
        blank=True,
        default="",
    )

    cidade = models.CharField(max_length=100, blank=True, default="")
    estado = models.CharField(max_length=2, blank=True, default="")

    perfil = models.CharField(
        max_length=20,
        choices=Perfil.choices,
        default=Perfil.OBSERVADOR,
    )

    status_validacao = models.CharField(
        max_length=20,
        choices=StatusValidacaoHemocentro.choices,
        default=StatusValidacaoHemocentro.PENDENTE,
    )

    is_active = models.BooleanField(default=True, db_column="ativo")
    email_verificado = models.BooleanField(default=False)

    date_joined = models.DateTimeField(
        auto_now_add=True,
        db_column="data_cadastro",
    )

    atualizado_em = models.DateTimeField(auto_now=True)
    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome"]

    class Meta:
        db_table = "usuarios"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ["nome"]

    def clean(self):
        """Padroniza o e-mail quando o model e validado."""

        super().clean()

        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email).lower()

    def get_full_name(self):
        """Devolve o nome completo no formato esperado pelo Django."""

        return self.nome

    def get_short_name(self):
        """Devolve o primeiro nome para saudacoes."""

        return self.nome.split()[0] if self.nome else self.email

    @property
    def is_hemocentro(self):
        """Informa se a conta representa um Hemocentro cadastrado."""

        return self.perfil == self.Perfil.HEMOCENTRO

    @property
    def hemocentro_aprovado(self):
        """Atalho usado pelas regras de publicacao de estoque e campanha."""

        return (
            self.is_hemocentro
            and self.status_validacao == self.StatusValidacaoHemocentro.APROVADO
        )

    def __str__(self):
        """Texto usado para representar o usuario no admin e no terminal."""

        return f"{self.nome} ({self.email})"


class ValidacaoHemocentro(models.Model):
    """
    Historico das analises institucionais de Hemocentros.

    A tabela registra cada decisao administrativa sem substituir as anteriores.
    O status atual continua em Usuario.status_validacao para consultas rapidas.
    """

    id_validacao = models.BigAutoField(primary_key=True)

    hemocentro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="validacoes_hemocentro",
        db_column="id_hemocentro",
    )

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validacoes_hemocentro_realizadas",
        db_column="id_admin",
    )

    status = models.CharField(
        max_length=20,
        choices=Usuario.StatusValidacaoHemocentro.choices,
    )

    parecer = models.TextField(blank=True, default="")
    data_analise = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "validacoes_hemocentro"
        verbose_name = "validacao de hemocentro"
        verbose_name_plural = "validacoes de hemocentros"
        ordering = ["-data_analise"]

        indexes = [
            models.Index(
                fields=["hemocentro", "-data_analise"],
                name="validacao_hemo_data_idx",
            ),
            models.Index(
                fields=["status", "data_analise"],
                name="validacao_hemo_status_idx",
            ),
        ]

    def clean(self):
        """Impede historico para conta que nao seja Hemocentro."""

        super().clean()

        hemocentro_nao_eh_valido = (
            self.hemocentro_id
            and self.hemocentro.perfil != Usuario.Perfil.HEMOCENTRO
        )

        if hemocentro_nao_eh_valido:
            raise ValidationError(
                {
                    "hemocentro": (
                        "Somente usuarios com perfil Hemocentro podem ser validados."
                    )
                }
            )

        admin_eh_valido = (
            self.admin_id
            and (
                self.admin.is_staff
                or self.admin.is_superuser
                or self.admin.perfil == Usuario.Perfil.ADMINISTRADOR
            )
        )

        if self.admin_id and not admin_eh_valido:
            raise ValidationError(
                {"admin": "A validacao deve ser registrada por um administrador."}
            )

    def __str__(self):
        return (
            f"{self.hemocentro.nome} - {self.get_status_display()} "
            f"em {self.data_analise:%d/%m/%Y %H:%M}"
        )


class PedidoSangue(models.Model):
    """Pedido de sangue criado por uma conta autenticada."""

    class ParaQuem(models.TextChoices):
        MIM = "MIM", "Para mim"
        OUTRA_PESSOA = "OUTRA_PESSOA", "Para outra pessoa"

    class Urgencia(models.TextChoices):
        NORMAL = "NORMAL", "Normal"
        URGENTE = "URGENTE", "Urgente"
        CRITICO = "CRITICO", "Crítico"

    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        ATIVO = "ATIVO", "Ativo"
        RECUSADO = "RECUSADO", "Recusado"
        ATENDIDO = "ATENDIDO", "Atendido"
        EXPIRADO = "EXPIRADO", "Expirado"

    id_pedido = models.BigAutoField(primary_key=True)

    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pedidos_publicados",
        db_column="id_solicitante",
    )

    hemocentro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pedidos_de_destino",
        db_column="id_hemocentro",
        limit_choices_to={"perfil": Usuario.Perfil.HEMOCENTRO},
    )

    para_quem = models.CharField(
        max_length=20,
        choices=ParaQuem.choices,
    )

    tipo_sanguineo = models.CharField(
        max_length=3,
        choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
    )

    cidade = models.CharField(max_length=100)

    urgencia = models.CharField(
        max_length=10,
        choices=Urgencia.choices,
    )

    nome_paciente = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    descricao = models.TextField(max_length=500)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDENTE,
    )

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_fechamento = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "pedidos_sangue"
        ordering = ["-data_criacao"]

        indexes = [
            models.Index(
                fields=["status", "-data_criacao"],
                name="pedido_sangue_status_idx",
            ),
            models.Index(
                fields=["cidade", "tipo_sanguineo"],
                name="pedido_sangue_busca_idx",
            ),
        ]

        verbose_name = "pedido de sangue"
        verbose_name_plural = "pedidos de sangue"

    def clean(self):
        """Garante que o destino escolhido seja uma conta de Hemocentro."""

        super().clean()

        if (
            self.hemocentro_id
            and self.hemocentro.perfil != Usuario.Perfil.HEMOCENTRO
        ):
            raise ValidationError(
                {
                    "hemocentro": (
                        "O destino deve ser uma conta com perfil Hemocentro."
                    )
                }
            )

    def __str__(self):
        return (
            f"Pedido {self.id_pedido} - {self.tipo_sanguineo} - "
            f"{self.get_status_display()}"
        )


class ConsentimentoLGPD(models.Model):
    """
    Guarda a prova de cada aceite de termo.

    O consentimento fica separado de Usuario porque precisa guardar sua propria
    versao, data e Ip. Quando o texto do termo mudar, uma nova versao podera ser
    aceita sem apagar o registro da versao anterior.
    """

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

    tipo_termo = models.CharField(
        max_length=20,
        choices=TipoTermo.choices,
        default=TipoTermo.GERAL,
    )

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
        CADASTRO_ESTOQUE = "CADASTRO_ESTOQUE", "Cadastro de estoque"
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
            models.Index(
                fields=["acao", "criado_em"],
                name="auditoria_acao_data_idx",
            ),
            models.Index(
                fields=["usuario", "criado_em"],
                name="auditoria_usuario_data_idx",
            ),
            models.Index(
                fields=["ip", "criado_em"],
                name="auditoria_ip_data_idx",
            ),
        ]

    def __str__(self):
        return f"{self.get_acao_display()} - {self.get_resultado_display()}"


class Triagem(models.Model):
    """
    Guarda uma triagem realizada por um usuário.

    O resultado é orientativo e nunca substitui a avaliação
    presencial feita pelo hemocentro.
    """

    class Modalidade(models.TextChoices):
        EXTENSA = "EXTENSA", "Triagem extensa"
        SIMPLIFICADA = "SIMPLIFICADA", "Triagem simplificada"

    class Status(models.TextChoices):
        """Representa em qual etapa do questionário a triagem está."""

        EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
        CONCLUIDA = "CONCLUIDA", "Concluída"
        CANCELADA = "CANCELADA", "Cancelada"

    class Resultado(models.TextChoices):
        SEM_IMPEDIMENTO = (
            "SEM_IMPEDIMENTO_IDENTIFICADO",
            "Sem impedimento identificado",
        )
        TEMPORARIA = (
            "INAPTIDAO_TEMPORARIA",
            "Inaptidão temporária",
        )
        DEFINITIVA = (
            "INAPTIDAO_DEFINITIVA",
            "Inaptidão definitiva",
        )
        AVALIACAO = (
            "AVALIACAO_PRESENCIAL",
            "Avaliação presencial",
        )
        DOCUMENTACAO = (
            "DOCUMENTACAO_ESPECIAL",
            "Documentação especial",
        )

    id_triagem = models.BigAutoField(primary_key=True)

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="triagens",
        db_column="id_usuario",
    )

    modalidade = models.CharField(
        max_length=20,
        choices=Modalidade.choices,
        default=Modalidade.EXTENSA,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.EM_ANDAMENTO,
    )

    pergunta_atual = models.PositiveIntegerField(default=0)
    fluxo_perguntas = models.JSONField(default=list, blank=True)

    triagem_base = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verificacoes_simplificadas",
    )

    regra_version = models.CharField(
        max_length=40,
        default="HEMOMINAS_2026_08",
    )

    resultado = models.CharField(
        max_length=30,
        choices=Resultado.choices,
        blank=True,
        default="",
    )

    mensagem_resultado = models.TextField(
        blank=True,
        default="",
    )

    data_liberacao = models.DateField(
        null=True,
        blank=True,
    )

    achados = models.JSONField(
        default=list,
        blank=True,
    )

    iniciada_em = models.DateTimeField(auto_now_add=True)

    finalizada_em = models.DateTimeField(
        null=True,
        blank=True,
    )

    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "triagens"
        ordering = ["-iniciada_em"]

        indexes = [
            models.Index(
                fields=["usuario", "-iniciada_em"],
                name="triagem_usuario_data_idx",
            ),
            models.Index(
                fields=["resultado", "-iniciada_em"],
                name="triagem_resultado_data_idx",
            ),
        ]

        verbose_name = "Triagem"
        verbose_name_plural = "Triagens"

    def __str__(self):
        return (
            f"Triagem {self.id_triagem} - "
            f"{self.usuario.nome} - "
            f"{self.get_resultado_display()}"
        )


class RespostaTriagem(models.Model):
    """
    Guarda uma resposta individual da triagem.

    As respostas são mantidas separadas para permitir auditoria,
    revisão das regras e futuras versões do questionário.
    """

    id_resposta = models.BigAutoField(primary_key=True)

    triagem = models.ForeignKey(
        Triagem,
        on_delete=models.CASCADE,
        related_name="respostas",
        db_column="id_triagem",
    )

    id_pergunta = models.CharField(max_length=20)
    codigo_resposta = models.CharField(max_length=80)
    resposta_label = models.CharField(max_length=255)

    data_evento = models.DateField(
        db_column="event_date",
        null=True,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    valor = models.JSONField(
        default=dict,
        blank=True,
    )

    rule_version = models.CharField(
        max_length=40,
        default="HEMOMINAS_2026_08",
    )

    source_ref = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    respondido_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "respostas_triagem"
        ordering = ["id_resposta"]

        constraints = [
            models.UniqueConstraint(
                fields=["triagem", "id_pergunta"],
                name="resposta_unica_por_pergunta",
            ),
        ]

        indexes = [
            models.Index(
                fields=["triagem", "id_pergunta"],
                name="resposta_triagem_pergunta_idx",
            ),
        ]

        verbose_name = "Resposta triagem"
        verbose_name_plural = "Respostas triagem"

    def __str__(self):
        return (
            f"{self.triagem_id} - "
            f"{self.id_pergunta} - "
            f"{self.codigo_resposta}"
        )


class Estoque(models.Model):
    """
    Uc_29 - Cadastrar Estoque.

    Guarda a estrutura de estoque de um Hemocentro para um unico tipo
    sanguineo: quantidade atual de bolsas, os niveis de alerta definidos
    pelo proprio hemocentro e o status calculado a partir desses valores.

    So existe um registro de Estoque por combinacao de hemocentro e tipo
    sanguineo (garantido pela UniqueConstraint abaixo). Para mudar a
    quantidade de bolsas depois de criado, use as funcoes de
    ``accounts/estoque.py`` em vez de editar o campo diretamente: elas
    recalculam o status, criam o historico em EstoqueMovimentacao e
    registram a auditoria.
    """

    class StatusCalculado(models.TextChoices):
        """
        Situacao do estoque, sempre derivada da quantidade e dos niveis.

        Nunca deve ser digitada manualmente por quem usa o sistema: a
        camada de servico recalcula este campo toda vez que a quantidade
        de bolsas muda.
        """

        CRITICO = "CRITICO", "Crítico"
        BAIXO = "BAIXO", "Baixo"
        ESTAVEL = "ESTAVEL", "Estável"

    id_estoque = models.BigAutoField(primary_key=True)

    hemocentro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="estoques",
        db_column="id_hemocentro",
        limit_choices_to={"perfil": "HEMOCENTRO"},
    )

    tipo_sanguineo = models.CharField(
        max_length=3,
        choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
    )

    quantidade_bolsas = models.PositiveIntegerField(default=0)
    nivel_minimo = models.PositiveIntegerField()
    nivel_critico = models.PositiveIntegerField()

    status_calculado = models.CharField(
        max_length=10,
        choices=StatusCalculado.choices,
        default=StatusCalculado.ESTAVEL,
    )

    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "estoques"
        verbose_name = "estoque"
        verbose_name_plural = "estoques"
        ordering = ["hemocentro__nome", "tipo_sanguineo"]

        constraints = [
            models.UniqueConstraint(
                fields=["hemocentro", "tipo_sanguineo"],
                name="estoque_unico_por_hemocentro_tipo",
            ),
        ]

        indexes = [
            models.Index(
                fields=["hemocentro", "tipo_sanguineo"],
                name="estoque_hemo_tipo_idx",
            ),
            models.Index(
                fields=["status_calculado"],
                name="estoque_status_idx",
            ),
        ]

    def clean(self):
        """Valida regras que dependem de mais de um campo."""

        super().clean()

        if (
            self.hemocentro_id
            and self.hemocentro.perfil != Usuario.Perfil.HEMOCENTRO
        ):
            raise ValidationError(
                {
                    "hemocentro": (
                        "Somente contas com perfil Hemocentro podem ter estoque."
                    )
                }
            )

        if (
            self.nivel_minimo is not None
            and self.nivel_critico is not None
            and self.nivel_critico > self.nivel_minimo
        ):
            raise ValidationError(
                {
                    "nivel_critico": (
                        "O nivel critico deve ser menor ou igual ao nivel minimo."
                    )
                }
            )

    def __str__(self):
        return (
            f"{self.hemocentro.nome} - {self.tipo_sanguineo} "
            f"({self.get_status_calculado_display()})"
        )


class EstoqueMovimentacao(models.Model):
    """
    Uc_30 - Atualizar Estoque.

    Historico imutavel de cada entrada, saida ou ajuste feito em um
    Estoque. Uma linha nunca e alterada ou apagada depois de criada: para
    corrigir um valor, registra-se uma nova movimentacao (do tipo Ajuste).

    Isso preserva o rastro completo exigido pela regra "toda alteracao
    deve gerar historico com responsavel".
    """

    class TipoMovimento(models.TextChoices):
        ENTRADA = "ENTRADA", "Entrada"
        SAIDA = "SAIDA", "Saída"
        AJUSTE = "AJUSTE", "Ajuste"

    id_mov = models.BigAutoField(primary_key=True)

    estoque = models.ForeignKey(
        Estoque,
        on_delete=models.CASCADE,
        related_name="movimentacoes",
        db_column="id_estoque",
    )

    usuario_resp = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movimentacoes_estoque_realizadas",
        db_column="id_usuario_resp",
    )

    tipo_movimento = models.CharField(
        max_length=10,
        choices=TipoMovimento.choices,
    )

    quantidade_anterior = models.PositiveIntegerField()
    quantidade_movimentada = models.IntegerField()
    quantidade_nova = models.PositiveIntegerField()

    motivo = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    data_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "movimentacoes_estoque"
        verbose_name = "movimentacao de estoque"
        verbose_name_plural = "movimentacoes de estoque"
        ordering = ["-data_hora"]

        indexes = [
            models.Index(
                fields=["estoque", "-data_hora"],
                name="mov_estoque_data_idx",
            ),
            models.Index(
                fields=["usuario_resp", "-data_hora"],
                name="mov_usuario_data_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.estoque.tipo_sanguineo} - "
            f"{self.get_tipo_movimento_display()} - "
            f"{self.quantidade_anterior} -> {self.quantidade_nova}"
        )


class Notificacao(models.Model):
    """
    Guarda avisos internos exibidos no dashboard do usuario.

    Nesta etapa, a notificacao sera usada para avisar doadores compativeis
    quando um estoque atualizado por Hemocentro ficar em nivel Baixo ou Critico.
    Futuramente a mesma tabela tambem pode receber outros avisos do sistema.
    """

    class Tipo(models.TextChoices):
        """Classificacao do aviso para facilitar filtros futuros."""

        ESTOQUE_BAIXO = "ESTOQUE_BAIXO", "Estoque baixo"
        ESTOQUE_CRITICO = "ESTOQUE_CRITICO", "Estoque crítico"
        GERAL = "GERAL", "Aviso geral"

    id_notificacao = models.BigAutoField(primary_key=True)

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notificacoes",
        db_column="id_usuario",
    )

    estoque = models.ForeignKey(
        Estoque,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notificacoes",
        db_column="id_estoque",
    )

    tipo = models.CharField(
        max_length=30,
        choices=Tipo.choices,
        default=Tipo.GERAL,
    )

    titulo = models.CharField(max_length=120)
    mensagem = models.TextField()
    url_destino = models.CharField(max_length=255, blank=True, default="")
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)
    lida_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "notificacoes"
        verbose_name = "notificacao"
        verbose_name_plural = "notificacoes"
        ordering = ["-criada_em"]

        indexes = [
            models.Index(
                fields=["usuario", "lida", "-criada_em"],
                name="notificacao_usuario_lida_idx",
            ),
            models.Index(
                fields=["tipo", "-criada_em"],
                name="notificacao_tipo_data_idx",
            ),
        ]

    def __str__(self):
        """Texto usado no admin e no terminal."""

        return f"{self.usuario.nome} - {self.titulo}"


class PedidoSangue(models.Model):
    """
    Rf - Pedido de Sangue.

    Guarda pedidos publicados por Receptor/Solicitante.

    O status permite que o pedido fique pendente, ativo, suspeito,
    recusado ou encerrado.
    """

    class Urgencia(models.TextChoices):
        BAIXA = "BAIXA", "Baixa"
        MEDIA = "MEDIA", "Media"
        ALTA = "ALTA", "Alta"
        CRITICA = "CRITICA", "Critica"

    class Status(models.TextChoices):
        PENDENTE_VALIDACAO = "PENDENTE_VALIDACAO", "Pendente de validacao"
        ATIVO = "ATIVO", "Ativo"
        SUSPEITO = "SUSPEITO", "Suspeito"
        RECUSADO = "RECUSADO", "Recusado"
        ENCERRADO = "ENCERRADO", "Encerrado"

    id_pedido = models.BigAutoField(primary_key=True)

    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pedidos_sangue",
        db_column="id_solicitante",
    )

    hemocentro_destino = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pedidos_recebidos",
        db_column="id_hemocentro_destino",
        limit_choices_to={"perfil": "HEMOCENTRO"},
    )

    titulo = models.CharField(max_length=150)

    tipo_sanguineo = models.CharField(
        max_length=3,
        choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
    )

    urgencia = models.CharField(
        max_length=10,
        choices=Urgencia.choices,
    )

    cidade = models.CharField(max_length=100)
    descricao = models.TextField()
    justificativa_urgencia = models.TextField(blank=True, default="")

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDENTE_VALIDACAO,
    )

    data_criacao = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pedidos_sangue"
        ordering = ["-data_criacao"]

        indexes = [
            models.Index(
                fields=["status", "-data_criacao"],
                name="pedido_status_data_idx",
            ),
            models.Index(
                fields=["tipo_sanguineo", "urgencia"],
                name="pedido_tipo_urg_idx",
            ),
            models.Index(
                fields=["cidade"],
                name="pedido_cidade_idx",
            ),
        ]

    def clean(self):
        super().clean()

        if (
            self.hemocentro_destino_id
            and self.hemocentro_destino.perfil != Usuario.Perfil.HEMOCENTRO
        ):
            raise ValidationError(
                {
                    "hemocentro_destino": (
                        "O destino precisa ser um Hemocentro cadastrado."
                    )
                }
            )

    def __str__(self):
        return (
            f"{self.titulo} - {self.tipo_sanguineo} - "
            f"{self.get_status_display()}"
        )


class ValidacaoPedido(models.Model):
    """
    Uc_17 - Validar Pedido.

    Guarda o historico das validacoes feitas automaticamente ou por moderador.
    """

    class StatusValidacao(models.TextChoices):
        APROVADO = "APROVADO", "Aprovado"
        SUSPEITO = "SUSPEITO", "Suspeito"
        RECUSADO = "RECUSADO", "Recusado"

    id_validacao = models.BigAutoField(primary_key=True)

    pedido = models.ForeignKey(
        PedidoSangue,
        on_delete=models.CASCADE,
        related_name="validacoes",
        db_column="id_pedido",
    )

    status_validacao = models.CharField(
        max_length=20,
        choices=StatusValidacao.choices,
    )

    motivo = models.TextField(blank=True, default="")

    moderador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validacoes_pedido_realizadas",
        db_column="id_moderador",
    )

    data_validacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "validacoes_pedido"
        ordering = ["-data_validacao"]

    def __str__(self):
        return f"Pedido {self.pedido_id} - {self.get_status_validacao_display()}"