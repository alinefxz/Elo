# accounts/models.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Entidades persistidas, relacionamentos, estados e integridade do banco.

**Arquivo original:** [accounts/models.py](<C:/Users/lb119/Elo/accounts/models.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
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

    # Quando um Hemocentro confirma o tipo, ele deixa de ser editável pela
    # triagem/autopreenchimento do usuário.
    tipo_sanguineo_confirmado = models.BooleanField(default=False)

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
    suspensa = models.BooleanField(default=False)
    aceita_notificacoes_pedidos = models.BooleanField(default=True)
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
    Registro de eventos sensiveis do Elo, somente leitura no painel administrativo.

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
            "Apto",
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
            "Avaliação presencial necessária",
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
        max_length=40,
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


# Nomes legados continuam disponíveis para código já existente, mas apontam
# para os resultados oficiais usados pelo fluxo atual.
Triagem.Resultado.APTO = Triagem.Resultado.SEM_IMPEDIMENTO
Triagem.Resultado.INAPTO_TEMPORARIO = Triagem.Resultado.TEMPORARIA
Triagem.Resultado.INAPTO_PERMANENTE = Triagem.Resultado.DEFINITIVA
Triagem.Resultado.AVALIACAO_PRESENCIAL_NECESSARIA = Triagem.Resultado.AVALIACAO


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
        PEDIDO_COMPATIVEL = "PEDIDO_COMPATIVEL", "Pedido compatível"
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

    pedido = models.ForeignKey(
        "PedidoSangue",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notificacoes",
        db_column="id_pedido",
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

    Guarda solicitações de divulgação e os pedidos publicados oficialmente.

    Doador, Receptor, Observador e Visitante criam somente uma solicitação.
    A publicação oficial é feita pelo Hemocentro aprovado vinculado.
    """

    class ParaQuem(models.TextChoices):
        MIM = "MIM", "Para mim"
        OUTRA_PESSOA = "OUTRA_PESSOA", "Para outra pessoa"

    class Urgencia(models.TextChoices):
        BAIXA = "BAIXA", "Baixa"
        MEDIA = "MEDIA", "Media"
        ALTA = "ALTA", "Alta"
        CRITICA = "CRITICA", "Critica"

    class Status(models.TextChoices):
        ENVIADA = "ENVIADA", "Enviada"
        EM_ANALISE = "EM_ANALISE", "Em análise"
        PUBLICADA = "PUBLICADA", "Publicada"
        CORRECAO_SOLICITADA = "CORRECAO_SOLICITADA", "Correção solicitada"
        RECUSADA = "RECUSADA", "Recusada"
        ENCERRADA = "ENCERRADA", "Encerrada"

    id_pedido = models.BigAutoField(primary_key=True)

    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pedidos_sangue",
        db_column="id_solicitante",
    )

    nome_solicitante = models.CharField(max_length=150, default="")
    contato = models.EmailField(max_length=120, default="")

    hemocentro_destino = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pedidos_recebidos",
        db_column="id_hemocentro_destino",
        limit_choices_to={"perfil": "HEMOCENTRO"},
    )

    para_quem = models.CharField(
        max_length=20,
        choices=ParaQuem.choices,
    )

    titulo = models.CharField(
        max_length=150,
        default="Pedido de sangue",
    )

    tipo_sanguineo = models.CharField(
        max_length=3,
        choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
    )

    urgencia = models.CharField(
        max_length=10,
        choices=Urgencia.choices,
    )

    cidade = models.CharField(max_length=100)
    nome_paciente = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )
    descricao = models.TextField()
    justificativa_urgencia = models.TextField(blank=True, default="")
    informacoes_complementares = models.TextField(blank=True, default="")

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.ENVIADA,
    )

    duplicidade_suspeita = models.BooleanField(default=False)

    publicado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pedidos_publicados",
        db_column="id_publicado_por",
    )
    publicado_em = models.DateTimeField(null=True, blank=True)

    data_criacao = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    data_fechamento = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "pedidos_sangue"
        ordering = ["-data_criacao"]
        verbose_name = "pedido de sangue"
        verbose_name_plural = "pedidos de sangue"

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

        if self.solicitante_id and self.solicitante.perfil in {
            Usuario.Perfil.HEMOCENTRO,
            Usuario.Perfil.ADMINISTRADOR,
        }:
            raise ValidationError(
                {"solicitante": "Este perfil não pode enviar solicitações."}
            )

        if self.status == self.Status.PUBLICADA:
            if not self.publicado_por_id or not self.publicado_por:
                raise ValidationError(
                    {"publicado_por": "A publicação precisa de um Hemocentro aprovado."}
                )
            if not (
                self.publicado_por.perfil == Usuario.Perfil.HEMOCENTRO
                and self.publicado_por.status_validacao
                == Usuario.StatusValidacaoHemocentro.APROVADO
            ):
                raise ValidationError(
                    {"publicado_por": "Somente Hemocentro aprovado pode publicar."}
                )

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


# Compatibilidade de leitura para integrações antigas. Os valores novos são
# os únicos gravados pelo fluxo atual.
PedidoSangue.Status.PENDENTE_VALIDACAO = PedidoSangue.Status.ENVIADA
PedidoSangue.Status.ATIVO = PedidoSangue.Status.PUBLICADA
PedidoSangue.Status.SUSPEITO = PedidoSangue.Status.EM_ANALISE
PedidoSangue.Status.RECUSADO = PedidoSangue.Status.RECUSADA
PedidoSangue.Status.ENCERRADO = PedidoSangue.Status.ENCERRADA


class ValidacaoPedido(models.Model):
    """
    Uc_17 - Validar Pedido.

    Guarda o historico das validacoes feitas automaticamente ou por moderador.
    """

    class StatusValidacao(models.TextChoices):
        APROVADO = "APROVADO", "Aprovado"
        CORRECAO_SOLICITADA = "CORRECAO_SOLICITADA", "Correção solicitada"
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


ValidacaoPedido.StatusValidacao.CORRECAO = (
    ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA
)
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 1 a 24

```python
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
```

**Explicação deste trecho:**

**Linha 1 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 26 a 26

```python
from django.conf import settings
```

**Explicação deste trecho:**

**Linha 26 — ImportFrom** (nível 0 do bloco).

Importa de `django.conf` os nomes `settings`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 27 a 27

```python
from django.contrib.auth.base_user import BaseUserManager
```

**Explicação deste trecho:**

**Linha 27 — ImportFrom** (nível 0 do bloco).

Importa de `django.contrib.auth.base_user` os nomes `BaseUserManager`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 28 a 28

```python
from django.contrib.auth.models import AbstractUser
```

**Explicação deste trecho:**

**Linha 28 — ImportFrom** (nível 0 do bloco).

Importa de `django.contrib.auth.models` os nomes `AbstractUser`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 29 a 29

```python
from django.core.exceptions import ValidationError
```

**Explicação deste trecho:**

**Linha 29 — ImportFrom** (nível 0 do bloco).

Importa de `django.core.exceptions` os nomes `ValidationError`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 30 a 30

```python
from django.db import models
```

**Explicação deste trecho:**

**Linha 30 — ImportFrom** (nível 0 do bloco).

Importa de `django.db` os nomes `models`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 34 a 34

```python
from .compatibilidade import TIPOS_SANGUINEOS
```

**Explicação deste trecho:**

**Linha 34 — ImportFrom** (nível 0 do bloco).

Importa de `.compatibilidade` os nomes `TIPOS_SANGUINEOS`. Pontos iniciais indicam importação relativa ao pacote.

### UsuarioManager — linhas 37 a 78

```python
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
```

**Explicação deste trecho:**

**Linha 37 — ClassDef** (nível 0 do bloco).

Define a classe `UsuarioManager` herdando de `BaseUserManager`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 37:

**Linha 38 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 46 — Assign** (nível 1 do bloco).

Associa `use_in_migrations` a o valor literal `True`.

**Linha 48 — FunctionDef** (nível 1 do bloco).

Define `create_user(self, email, password=None, **extra_fields)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 48:

**Linha 49 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 51 — If** (nível 2 do bloco).

Escolhe um caminho verificando a negação de `email`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 51:

**Linha 52 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `ValueError`; argumentos posicionais: `'O e-mail e obrigatorio.'`.

**Linha 56 — Assign** (nível 2 do bloco).

Associa `email` a a chamada `self.normalize_email(email).lower`, que converte texto para minúsculas.


**Linha 58 — Assign** (nível 2 do bloco).

Associa `usuario` a a chamada `self.model`; argumentos nomeados: `email=email`, `**=extra_fields`.

- `email=email`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `**=extra_fields`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 59 — Expr** (nível 2 do bloco).

Executa a chamada `usuario.set_password`, que transforma a senha em hash para armazenamento; argumentos posicionais: `password`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 60 — Expr** (nível 2 do bloco).

Executa a chamada `usuario.save`, que persiste a instância; update_fields limita os campos gravados; argumentos nomeados: `using=self._db`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 62 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `usuario` ao chamador.

**Linha 64 — FunctionDef** (nível 1 do bloco).

Define `create_superuser(self, email, password=None, **extra_fields)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 64:

**Linha 65 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 67 — Expr** (nível 2 do bloco).

Executa a chamada `extra_fields.setdefault`; argumentos posicionais: `'is_staff'`, `True`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 68 — Expr** (nível 2 do bloco).

Executa a chamada `extra_fields.setdefault`; argumentos posicionais: `'is_superuser'`, `True`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 69 — Expr** (nível 2 do bloco).

Executa a chamada `extra_fields.setdefault`; argumentos posicionais: `'is_active'`, `True`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 70 — Expr** (nível 2 do bloco).

Executa a chamada `extra_fields.setdefault`; argumentos posicionais: `'perfil'`, `self.model.Perfil.ADMINISTRADOR`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 72 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `extra_fields.get('is_staff')` um objeto diferente de `True`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 72:

**Linha 73 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `ValueError`; argumentos posicionais: `'O superusuario precisa ter is_staff=True.'`.

**Linha 75 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `extra_fields.get('is_superuser')` um objeto diferente de `True`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 75:

**Linha 76 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `ValueError`; argumentos posicionais: `'O superusuario precisa ter is_superuser=True.'`.

**Linha 78 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a chamada `self.create_user`; argumentos posicionais: `email`, `password`; argumentos nomeados: `**=extra_fields` ao chamador.

### Usuario — linhas 81 a 223

```python
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

    # Quando um Hemocentro confirma o tipo, ele deixa de ser editável pela
    # triagem/autopreenchimento do usuário.
    tipo_sanguineo_confirmado = models.BooleanField(default=False)

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
    suspensa = models.BooleanField(default=False)
    aceita_notificacoes_pedidos = models.BooleanField(default=True)
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
```

**Explicação deste trecho:**

**Linha 81 — ClassDef** (nível 0 do bloco).

Define a classe `Usuario` herdando de `AbstractUser`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 81:

**Linha 82 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 91 — ClassDef** (nível 1 do bloco).

Define a classe `Perfil` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 91:

**Linha 92 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 94 — Assign** (nível 2 do bloco).

Associa `DOADOR` a uma coleção Tuple com 2 itens, na expressão `('DOADOR', 'Doador')`.

**Linha 95 — Assign** (nível 2 do bloco).

Associa `RECEPTOR` a uma coleção Tuple com 2 itens, na expressão `('RECEPTOR', 'Receptor')`.

**Linha 96 — Assign** (nível 2 do bloco).

Associa `HEMOCENTRO` a uma coleção Tuple com 2 itens, na expressão `('HEMOCENTRO', 'Hemocentro')`.

**Linha 97 — Assign** (nível 2 do bloco).

Associa `OBSERVADOR` a uma coleção Tuple com 2 itens, na expressão `('OBSERVADOR', 'Observador')`.

**Linha 98 — Assign** (nível 2 do bloco).

Associa `ADMINISTRADOR` a uma coleção Tuple com 2 itens, na expressão `('ADMINISTRADOR', 'Administrador')`.

**Linha 100 — ClassDef** (nível 1 do bloco).

Define a classe `Sexo` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 100:

**Linha 101 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 103 — Assign** (nível 2 do bloco).

Associa `FEMININO` a uma coleção Tuple com 2 itens, na expressão `('F', 'Feminino')`.

**Linha 104 — Assign** (nível 2 do bloco).

Associa `MASCULINO` a uma coleção Tuple com 2 itens, na expressão `('M', 'Masculino')`.

**Linha 105 — Assign** (nível 2 do bloco).

Associa `OUTRO` a uma coleção Tuple com 2 itens, na expressão `('O', 'Outro')`.

**Linha 106 — Assign** (nível 2 do bloco).

Associa `NAO_INFORMADO` a uma coleção Tuple com 2 itens, na expressão `('N', 'Prefiro nao informar')`.

**Linha 108 — ClassDef** (nível 1 do bloco).

Define a classe `StatusValidacaoHemocentro` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 108:

**Linha 109 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 111 — Assign** (nível 2 do bloco).

Associa `PENDENTE` a uma coleção Tuple com 2 itens, na expressão `('PENDENTE', 'Pendente')`.

**Linha 112 — Assign** (nível 2 do bloco).

Associa `APROVADO` a uma coleção Tuple com 2 itens, na expressão `('APROVADO', 'Aprovado')`.

**Linha 113 — Assign** (nível 2 do bloco).

Associa `RECUSADO` a uma coleção Tuple com 2 itens, na expressão `('RECUSADO', 'Recusado')`.

**Linha 114 — Assign** (nível 2 do bloco).

Associa `CORRECAO` a uma coleção Tuple com 2 itens, na expressão `('CORRECAO', 'Correcao necessaria')`.

**Linha 116 — Assign** (nível 1 do bloco).

Associa `username` a o valor literal `None`.

**Linha 117 — Assign** (nível 1 do bloco).

Associa `first_name` a o valor literal `None`.

**Linha 118 — Assign** (nível 1 do bloco).

Associa `last_name` a o valor literal `None`.

**Linha 120 — Assign** (nível 1 do bloco).

Associa `id_usuario` a a chamada `models.BigAutoField`; argumentos nomeados: `primary_key=True`.

- `primary_key=True`: define o identificador principal do registro.

**Linha 122 — Assign** (nível 1 do bloco).

Associa `nome` a a chamada `models.CharField`; argumentos nomeados: `max_length=150`.

- `max_length=150`: limite de comprimento do campo.

**Linha 123 — Assign** (nível 1 do bloco).

Associa `email` a a chamada `models.EmailField`; argumentos nomeados: `unique=True`.

- `unique=True`: exige valor único no banco.

**Linha 124 — Assign** (nível 1 do bloco).

Associa `password` a a chamada `models.CharField`; argumentos nomeados: `max_length=128`, `db_column='senha_hash'`.

- `max_length=128`: limite de comprimento do campo.
- `db_column='senha_hash'`: nome da coluna no banco.

**Linha 126 — Assign** (nível 1 do bloco).

Associa `cpf` a a chamada `models.CharField`; argumentos nomeados: `max_length=11`, `unique=True`, `null=True`, `blank=True`.

- `max_length=11`: limite de comprimento do campo.
- `unique=True`: exige valor único no banco.
- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 127 — Assign** (nível 1 do bloco).

Associa `cnpj` a a chamada `models.CharField`; argumentos nomeados: `max_length=14`, `unique=True`, `null=True`, `blank=True`.

- `max_length=14`: limite de comprimento do campo.
- `unique=True`: exige valor único no banco.
- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 129 — Assign** (nível 1 do bloco).

Associa `telefone` a a chamada `models.CharField`; argumentos nomeados: `max_length=20`, `blank=True`, `default=''`.

- `max_length=20`: limite de comprimento do campo.
- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 130 — Assign** (nível 1 do bloco).

Associa `data_nascimento` a a chamada `models.DateField`; argumentos nomeados: `null=True`, `blank=True`.

- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 132 — Assign** (nível 1 do bloco).

Associa `sexo` a a chamada `models.CharField`; argumentos nomeados: `max_length=1`, `choices=Sexo.choices`, `blank=True`, `default=''`.

- `max_length=1`: limite de comprimento do campo.
- `choices=Sexo.choices`: alternativas declaradas para validação e apresentação.
- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 139 — Assign** (nível 1 do bloco).

Associa `tipo_sanguineo` a a chamada `models.CharField`; argumentos nomeados: `max_length=3`, `choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS]`, `blank=True`, `default=''`.

- `max_length=3`: limite de comprimento do campo.
- `choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS]`: alternativas declaradas para validação e apresentação.
- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 148 — Assign** (nível 1 do bloco).

Associa `tipo_sanguineo_confirmado` a a chamada `models.BooleanField`; argumentos nomeados: `default=False`.

- `default=False`: valor inicial quando não é informado outro.

**Linha 150 — Assign** (nível 1 do bloco).

Associa `cidade` a a chamada `models.CharField`; argumentos nomeados: `max_length=100`, `blank=True`, `default=''`.

- `max_length=100`: limite de comprimento do campo.
- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 151 — Assign** (nível 1 do bloco).

Associa `estado` a a chamada `models.CharField`; argumentos nomeados: `max_length=2`, `blank=True`, `default=''`.

- `max_length=2`: limite de comprimento do campo.
- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 153 — Assign** (nível 1 do bloco).

Associa `perfil` a a chamada `models.CharField`; argumentos nomeados: `max_length=20`, `choices=Perfil.choices`, `default=Perfil.OBSERVADOR`.

- `max_length=20`: limite de comprimento do campo.
- `choices=Perfil.choices`: alternativas declaradas para validação e apresentação.
- `default=Perfil.OBSERVADOR`: valor inicial quando não é informado outro.

**Linha 159 — Assign** (nível 1 do bloco).

Associa `status_validacao` a a chamada `models.CharField`; argumentos nomeados: `max_length=20`, `choices=StatusValidacaoHemocentro.choices`, `default=StatusValidacaoHemocentro.PENDENTE`.

- `max_length=20`: limite de comprimento do campo.
- `choices=StatusValidacaoHemocentro.choices`: alternativas declaradas para validação e apresentação.
- `default=StatusValidacaoHemocentro.PENDENTE`: valor inicial quando não é informado outro.

**Linha 165 — Assign** (nível 1 do bloco).

Associa `is_active` a a chamada `models.BooleanField`; argumentos nomeados: `default=True`, `db_column='ativo'`.

- `default=True`: valor inicial quando não é informado outro.
- `db_column='ativo'`: nome da coluna no banco.

**Linha 166 — Assign** (nível 1 do bloco).

Associa `suspensa` a a chamada `models.BooleanField`; argumentos nomeados: `default=False`.

- `default=False`: valor inicial quando não é informado outro.

**Linha 167 — Assign** (nível 1 do bloco).

Associa `aceita_notificacoes_pedidos` a a chamada `models.BooleanField`; argumentos nomeados: `default=True`.

- `default=True`: valor inicial quando não é informado outro.

**Linha 168 — Assign** (nível 1 do bloco).

Associa `email_verificado` a a chamada `models.BooleanField`; argumentos nomeados: `default=False`.

- `default=False`: valor inicial quando não é informado outro.

**Linha 170 — Assign** (nível 1 do bloco).

Associa `date_joined` a a chamada `models.DateTimeField`; argumentos nomeados: `auto_now_add=True`, `db_column='data_cadastro'`.

- `auto_now_add=True`: preenche a data/hora na criação.
- `db_column='data_cadastro'`: nome da coluna no banco.

**Linha 175 — Assign** (nível 1 do bloco).

Associa `atualizado_em` a a chamada `models.DateTimeField`; argumentos nomeados: `auto_now=True`.

- `auto_now=True`: atualiza a data/hora no save pertinente.

**Linha 176 — Assign** (nível 1 do bloco).

Associa `objects` a a chamada `UsuarioManager`.


**Linha 178 — Assign** (nível 1 do bloco).

Associa `USERNAME_FIELD` a o valor literal `'email'`.

**Linha 179 — Assign** (nível 1 do bloco).

Associa `REQUIRED_FIELDS` a uma coleção List com 1 itens, na expressão `['nome']`.

**Linha 181 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 181:

**Linha 182 — Assign** (nível 2 do bloco).

Associa `db_table` a o valor literal `'usuarios'`.

**Linha 183 — Assign** (nível 2 do bloco).

Associa `verbose_name` a o valor literal `'usuario'`.

**Linha 184 — Assign** (nível 2 do bloco).

Associa `verbose_name_plural` a o valor literal `'usuarios'`.

**Linha 185 — Assign** (nível 2 do bloco).

Associa `ordering` a uma coleção List com 1 itens, na expressão `['nome']`.

**Linha 187 — FunctionDef** (nível 1 do bloco).

Define `clean(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 187:

**Linha 188 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 190 — Expr** (nível 2 do bloco).

Executa a chamada `super().clean`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 192 — If** (nível 2 do bloco).

Escolhe um caminho verificando o atributo `email` de `self`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 192:

**Linha 193 — Assign** (nível 3 do bloco).

Associa `self.email` a a chamada `self.__class__.objects.normalize_email(self.email).lower`, que converte texto para minúsculas.


**Linha 195 — FunctionDef** (nível 1 do bloco).

Define `get_full_name(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 195:

**Linha 196 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 198 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o atributo `nome` de `self` ao chamador.

**Linha 200 — FunctionDef** (nível 1 do bloco).

Define `get_short_name(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 200:

**Linha 201 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 203 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve `self.nome.split()[0]` se `self.nome` for verdadeiro; caso contrário, `self.email` ao chamador.

**Linha 206 — FunctionDef** (nível 1 do bloco).

Define `is_hemocentro(self)`. O corpo só executa quando a função/método é chamado. Decoradores: `property`.

Bloco `body` da linha 206:

**Linha 207 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 209 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve a comparação `self.perfil` igual a `self.Perfil.HEMOCENTRO` ao chamador.

**Linha 212 — FunctionDef** (nível 1 do bloco).

Define `hemocentro_aprovado(self)`. O corpo só executa quando a função/método é chamado. Decoradores: `property`.

Bloco `body` da linha 212:

**Linha 213 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 215 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve todas as condições: `self.is_hemocentro` ; `self.status_validacao == self.StatusValidacaoHemocentro.APROVADO` (com avaliação interrompida assim que o resultado é determinado) ao chamador.

**Linha 220 — FunctionDef** (nível 1 do bloco).

Define `__str__(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 220:

**Linha 221 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 223 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o texto formatado `f'{self.nome} ({self.email})'`, inserindo valores nas partes entre chaves ao chamador.

### ValidacaoHemocentro — linhas 226 a 314

```python
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
```

**Explicação deste trecho:**

**Linha 226 — ClassDef** (nível 0 do bloco).

Define a classe `ValidacaoHemocentro` herdando de `models.Model`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 226:

**Linha 227 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 234 — Assign** (nível 1 do bloco).

Associa `id_validacao` a a chamada `models.BigAutoField`; argumentos nomeados: `primary_key=True`.

- `primary_key=True`: define o identificador principal do registro.

**Linha 236 — Assign** (nível 1 do bloco).

Associa `hemocentro` a a chamada `models.ForeignKey`; argumentos posicionais: `settings.AUTH_USER_MODEL`; argumentos nomeados: `on_delete=models.CASCADE`, `related_name='validacoes_hemocentro'`, `db_column='id_hemocentro'`.

- `on_delete=models.CASCADE`: comportamento quando o registro relacionado é excluído.
- `related_name='validacoes_hemocentro'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_hemocentro'`: nome da coluna no banco.

**Linha 243 — Assign** (nível 1 do bloco).

Associa `admin` a a chamada `models.ForeignKey`; argumentos posicionais: `settings.AUTH_USER_MODEL`; argumentos nomeados: `on_delete=models.SET_NULL`, `null=True`, `blank=True`, `related_name='validacoes_hemocentro_realizadas'`, `db_column='id_admin'`.

- `on_delete=models.SET_NULL`: comportamento quando o registro relacionado é excluído.
- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.
- `related_name='validacoes_hemocentro_realizadas'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_admin'`: nome da coluna no banco.

**Linha 252 — Assign** (nível 1 do bloco).

Associa `status` a a chamada `models.CharField`; argumentos nomeados: `max_length=20`, `choices=Usuario.StatusValidacaoHemocentro.choices`.

- `max_length=20`: limite de comprimento do campo.
- `choices=Usuario.StatusValidacaoHemocentro.choices`: alternativas declaradas para validação e apresentação.

**Linha 257 — Assign** (nível 1 do bloco).

Associa `parecer` a a chamada `models.TextField`; argumentos nomeados: `blank=True`, `default=''`.

- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 258 — Assign** (nível 1 do bloco).

Associa `data_analise` a a chamada `models.DateTimeField`; argumentos nomeados: `auto_now_add=True`.

- `auto_now_add=True`: preenche a data/hora na criação.

**Linha 260 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 260:

**Linha 261 — Assign** (nível 2 do bloco).

Associa `db_table` a o valor literal `'validacoes_hemocentro'`.

**Linha 262 — Assign** (nível 2 do bloco).

Associa `verbose_name` a o valor literal `'validacao de hemocentro'`.

**Linha 263 — Assign** (nível 2 do bloco).

Associa `verbose_name_plural` a o valor literal `'validacoes de hemocentros'`.

**Linha 264 — Assign** (nível 2 do bloco).

Associa `ordering` a uma coleção List com 1 itens, na expressão `['-data_analise']`.

**Linha 266 — Assign** (nível 2 do bloco).

Associa `indexes` a uma coleção List com 2 itens, na expressão `[models.Index(fields=['hemocentro', '-data_analise'], name='validacao_hemo_data_idx'), models.Index(fields=['status', 'data_analise'], name='validacao_hemo_status_idx')]`.

**Linha 277 — FunctionDef** (nível 1 do bloco).

Define `clean(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 277:

**Linha 278 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 280 — Expr** (nível 2 do bloco).

Executa a chamada `super().clean`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 282 — Assign** (nível 2 do bloco).

Associa `hemocentro_nao_eh_valido` a todas as condições: `self.hemocentro_id` ; `self.hemocentro.perfil != Usuario.Perfil.HEMOCENTRO` (com avaliação interrompida assim que o resultado é determinado).

**Linha 287 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `hemocentro_nao_eh_valido`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 287:

**Linha 288 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `{'hemocentro': 'Somente usuarios com perfil Hemocentro podem ser validados.'}`.

**Linha 296 — Assign** (nível 2 do bloco).

Associa `admin_eh_valido` a todas as condições: `self.admin_id` ; `self.admin.is_staff or self.admin.is_superuser or self.admin.perfil == Usuario.Perfil.ADMINISTRADOR` (com avaliação interrompida assim que o resultado é determinado).

**Linha 305 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `self.admin_id` ; `not admin_eh_valido` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 305:

**Linha 306 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `{'admin': 'A validacao deve ser registrada por um administrador.'}`.

**Linha 310 — FunctionDef** (nível 1 do bloco).

Define `__str__(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 310:

**Linha 311 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o texto formatado `f'{self.hemocentro.nome} - {self.get_status_display()} em {self.data_analise:%d/%m/%Y %H:%M}'`, inserindo valores nas partes entre chaves ao chamador.

### ConsentimentoLGPD — linhas 317 a 366

```python
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
```

**Explicação deste trecho:**

**Linha 317 — ClassDef** (nível 0 do bloco).

Define a classe `ConsentimentoLGPD` herdando de `models.Model`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 317:

**Linha 318 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 326 — ClassDef** (nível 1 do bloco).

Define a classe `TipoTermo` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 326:

**Linha 327 — Assign** (nível 2 do bloco).

Associa `GERAL` a uma coleção Tuple com 2 itens, na expressão `('GERAL', 'Termos gerais e politica de privacidade')`.

**Linha 328 — Assign** (nível 2 do bloco).

Associa `TRIAGEM` a uma coleção Tuple com 2 itens, na expressão `('TRIAGEM', 'Termo de triagem')`.

**Linha 329 — Assign** (nível 2 do bloco).

Associa `NOTIFICACOES` a uma coleção Tuple com 2 itens, na expressão `('NOTIFICACOES', 'Termo de notificacoes')`.

**Linha 331 — Assign** (nível 1 do bloco).

Associa `id_consentimento` a a chamada `models.BigAutoField`; argumentos nomeados: `primary_key=True`.

- `primary_key=True`: define o identificador principal do registro.

**Linha 333 — Assign** (nível 1 do bloco).

Associa `usuario` a a chamada `models.ForeignKey`; argumentos posicionais: `settings.AUTH_USER_MODEL`; argumentos nomeados: `on_delete=models.CASCADE`, `related_name='consentimentos_lgpd'`, `db_column='id_usuario'`.

- `on_delete=models.CASCADE`: comportamento quando o registro relacionado é excluído.
- `related_name='consentimentos_lgpd'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_usuario'`: nome da coluna no banco.

**Linha 340 — Assign** (nível 1 do bloco).

Associa `tipo_termo` a a chamada `models.CharField`; argumentos nomeados: `max_length=20`, `choices=TipoTermo.choices`, `default=TipoTermo.GERAL`.

- `max_length=20`: limite de comprimento do campo.
- `choices=TipoTermo.choices`: alternativas declaradas para validação e apresentação.
- `default=TipoTermo.GERAL`: valor inicial quando não é informado outro.

**Linha 346 — Assign** (nível 1 do bloco).

Associa `versao_termo` a a chamada `models.CharField`; argumentos nomeados: `max_length=20`, `default='1.0'`.

- `max_length=20`: limite de comprimento do campo.
- `default='1.0'`: valor inicial quando não é informado outro.

**Linha 347 — Assign** (nível 1 do bloco).

Associa `aceito` a a chamada `models.BooleanField`; argumentos nomeados: `default=False`.

- `default=False`: valor inicial quando não é informado outro.

**Linha 348 — Assign** (nível 1 do bloco).

Associa `data_aceite` a a chamada `models.DateTimeField`; argumentos nomeados: `auto_now_add=True`.

- `auto_now_add=True`: preenche a data/hora na criação.

**Linha 349 — Assign** (nível 1 do bloco).

Associa `ip` a a chamada `models.GenericIPAddressField`; argumentos nomeados: `null=True`, `blank=True`.

- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 350 — Assign** (nível 1 do bloco).

Associa `revogado_em` a a chamada `models.DateTimeField`; argumentos nomeados: `null=True`, `blank=True`.

- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 352 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 352:

**Linha 353 — Assign** (nível 2 do bloco).

Associa `db_table` a o valor literal `'consentimentos_lgpd'`.

**Linha 354 — Assign** (nível 2 do bloco).

Associa `verbose_name` a o valor literal `'consentimento LGPD'`.

**Linha 355 — Assign** (nível 2 do bloco).

Associa `verbose_name_plural` a o valor literal `'consentimentos LGPD'`.

**Linha 356 — Assign** (nível 2 do bloco).

Associa `ordering` a uma coleção List com 1 itens, na expressão `['-data_aceite']`.

**Linha 358 — Assign** (nível 2 do bloco).

Associa `constraints` a uma coleção List com 1 itens, na expressão `[models.UniqueConstraint(fields=['usuario', 'tipo_termo', 'versao_termo'], name='consentimento_unico_por_versao')]`.

**Linha 365 — FunctionDef** (nível 1 do bloco).

Define `__str__(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 365:

**Linha 366 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o texto formatado `f'{self.usuario.email} - {self.get_tipo_termo_display()}'`, inserindo valores nas partes entre chaves ao chamador.

### AuditoriaAcaoCritica — linhas 369 a 446

```python
class AuditoriaAcaoCritica(models.Model):
    """
    Registro de eventos sensiveis do Elo, somente leitura no painel administrativo.

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
```

**Explicação deste trecho:**

**Linha 369 — ClassDef** (nível 0 do bloco).

Define a classe `AuditoriaAcaoCritica` herdando de `models.Model`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 369:

**Linha 370 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 378 — ClassDef** (nível 1 do bloco).

Define a classe `Acao` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 378:

**Linha 379 — Assign** (nível 2 do bloco).

Associa `LOGIN_FALHO` a uma coleção Tuple com 2 itens, na expressão `('LOGIN_FALHO', 'Login falho')`.

**Linha 380 — Assign** (nível 2 do bloco).

Associa `LOGIN_SUSPEITO` a uma coleção Tuple com 2 itens, na expressão `('LOGIN_SUSPEITO', 'Login suspeito')`.

**Linha 381 — Assign** (nível 2 do bloco).

Associa `ALTERACAO_PERMISSAO` a uma coleção Tuple com 2 itens, na expressão `('ALTERACAO_PERMISSAO', 'Alteracao de permissao')`.

**Linha 382 — Assign** (nível 2 do bloco).

Associa `APROVACAO_HEMOCENTRO` a uma coleção Tuple com 2 itens, na expressão `('APROVACAO_HEMOCENTRO', 'Aprovacao de hemocentro')`.

**Linha 383 — Assign** (nível 2 do bloco).

Associa `CADASTRO_ESTOQUE` a uma coleção Tuple com 2 itens, na expressão `('CADASTRO_ESTOQUE', 'Cadastro de estoque')`.

**Linha 384 — Assign** (nível 2 do bloco).

Associa `ATUALIZACAO_ESTOQUE` a uma coleção Tuple com 2 itens, na expressão `('ATUALIZACAO_ESTOQUE', 'Atualizacao de estoque')`.

**Linha 385 — Assign** (nível 2 do bloco).

Associa `MODERACAO` a uma coleção Tuple com 2 itens, na expressão `('MODERACAO', 'Moderacao')`.

**Linha 386 — Assign** (nível 2 do bloco).

Associa `ACESSO_DADOS_SENSIVEIS` a uma coleção Tuple com 2 itens, na expressão `('ACESSO_DADOS_SENSIVEIS', 'Acesso a dados sensiveis')`.

**Linha 390 — Assign** (nível 2 do bloco).

Associa `CONFIRMACAO_DOACAO` a uma coleção Tuple com 2 itens, na expressão `('CONFIRMACAO_DOACAO', 'Confirmacao de doacao')`.

**Linha 392 — ClassDef** (nível 1 do bloco).

Define a classe `Resultado` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 392:

**Linha 393 — Assign** (nível 2 do bloco).

Associa `SUCESSO` a uma coleção Tuple com 2 itens, na expressão `('SUCESSO', 'Sucesso')`.

**Linha 394 — Assign** (nível 2 do bloco).

Associa `FALHA` a uma coleção Tuple com 2 itens, na expressão `('FALHA', 'Falha')`.

**Linha 395 — Assign** (nível 2 do bloco).

Associa `BLOQUEADO` a uma coleção Tuple com 2 itens, na expressão `('BLOQUEADO', 'Bloqueado')`.

**Linha 397 — Assign** (nível 1 do bloco).

Associa `id_auditoria` a a chamada `models.BigAutoField`; argumentos nomeados: `primary_key=True`.

- `primary_key=True`: define o identificador principal do registro.

**Linha 399 — Assign** (nível 1 do bloco).

Associa `usuario` a a chamada `models.ForeignKey`; argumentos posicionais: `settings.AUTH_USER_MODEL`; argumentos nomeados: `on_delete=models.SET_NULL`, `null=True`, `blank=True`, `related_name='auditorias_acoes_criticas'`, `db_column='id_usuario'`.

- `on_delete=models.SET_NULL`: comportamento quando o registro relacionado é excluído.
- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.
- `related_name='auditorias_acoes_criticas'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_usuario'`: nome da coluna no banco.

**Linha 408 — Assign** (nível 1 do bloco).

Associa `acao` a a chamada `models.CharField`; argumentos nomeados: `max_length=40`, `choices=Acao.choices`.

- `max_length=40`: limite de comprimento do campo.
- `choices=Acao.choices`: alternativas declaradas para validação e apresentação.

**Linha 410 — Assign** (nível 1 do bloco).

Associa `resultado` a a chamada `models.CharField`; argumentos nomeados: `max_length=20`, `choices=Resultado.choices`, `default=Resultado.SUCESSO`.

- `max_length=20`: limite de comprimento do campo.
- `choices=Resultado.choices`: alternativas declaradas para validação e apresentação.
- `default=Resultado.SUCESSO`: valor inicial quando não é informado outro.

**Linha 416 — Assign** (nível 1 do bloco).

Associa `alvo_tipo` a a chamada `models.CharField`; argumentos nomeados: `max_length=80`, `blank=True`, `default=''`.

- `max_length=80`: limite de comprimento do campo.
- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 417 — Assign** (nível 1 do bloco).

Associa `alvo_id` a a chamada `models.CharField`; argumentos nomeados: `max_length=80`, `blank=True`, `default=''`.

- `max_length=80`: limite de comprimento do campo.
- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 418 — Assign** (nível 1 do bloco).

Associa `descricao` a a chamada `models.CharField`; argumentos nomeados: `max_length=255`, `blank=True`, `default=''`.

- `max_length=255`: limite de comprimento do campo.
- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 419 — Assign** (nível 1 do bloco).

Associa `ip` a a chamada `models.GenericIPAddressField`; argumentos nomeados: `null=True`, `blank=True`.

- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 420 — Assign** (nível 1 do bloco).

Associa `user_agent` a a chamada `models.TextField`; argumentos nomeados: `blank=True`, `default=''`.

- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 421 — Assign** (nível 1 do bloco).

Associa `metadados` a a chamada `models.JSONField`; argumentos nomeados: `blank=True`, `default=dict`.

- `blank=True`: permite ou impede campo vazio na validação.
- `default=dict`: valor inicial quando não é informado outro.

**Linha 422 — Assign** (nível 1 do bloco).

Associa `criado_em` a a chamada `models.DateTimeField`; argumentos nomeados: `auto_now_add=True`.

- `auto_now_add=True`: preenche a data/hora na criação.

**Linha 424 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 424:

**Linha 425 — Assign** (nível 2 do bloco).

Associa `db_table` a o valor literal `'auditorias_acoes_criticas'`.

**Linha 426 — Assign** (nível 2 do bloco).

Associa `verbose_name` a o valor literal `'auditoria de acao critica'`.

**Linha 427 — Assign** (nível 2 do bloco).

Associa `verbose_name_plural` a o valor literal `'auditorias de acoes criticas'`.

**Linha 428 — Assign** (nível 2 do bloco).

Associa `ordering` a uma coleção List com 1 itens, na expressão `['-criado_em']`.

**Linha 430 — Assign** (nível 2 do bloco).

Associa `indexes` a uma coleção List com 3 itens, na expressão `[models.Index(fields=['acao', 'criado_em'], name='auditoria_acao_data_idx'), models.Index(fields=['usuario', 'criado_em'], name='auditoria_usuario_data_idx'), models.Index(fields=['ip', 'criado_em'], name='auditoria_ip_data_idx')]`.

**Linha 445 — FunctionDef** (nível 1 do bloco).

Define `__str__(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 445:

**Linha 446 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o texto formatado `f'{self.get_acao_display()} - {self.get_resultado_display()}'`, inserindo valores nas partes entre chaves ao chamador.

### Triagem — linhas 449 a 581

```python
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
            "Apto",
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
            "Avaliação presencial necessária",
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
        max_length=40,
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
```

**Explicação deste trecho:**

**Linha 449 — ClassDef** (nível 0 do bloco).

Define a classe `Triagem` herdando de `models.Model`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 449:

**Linha 450 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 457 — ClassDef** (nível 1 do bloco).

Define a classe `Modalidade` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 457:

**Linha 458 — Assign** (nível 2 do bloco).

Associa `EXTENSA` a uma coleção Tuple com 2 itens, na expressão `('EXTENSA', 'Triagem extensa')`.

**Linha 459 — Assign** (nível 2 do bloco).

Associa `SIMPLIFICADA` a uma coleção Tuple com 2 itens, na expressão `('SIMPLIFICADA', 'Triagem simplificada')`.

**Linha 461 — ClassDef** (nível 1 do bloco).

Define a classe `Status` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 461:

**Linha 462 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 464 — Assign** (nível 2 do bloco).

Associa `EM_ANDAMENTO` a uma coleção Tuple com 2 itens, na expressão `('EM_ANDAMENTO', 'Em andamento')`.

**Linha 465 — Assign** (nível 2 do bloco).

Associa `CONCLUIDA` a uma coleção Tuple com 2 itens, na expressão `('CONCLUIDA', 'Concluída')`.

**Linha 466 — Assign** (nível 2 do bloco).

Associa `CANCELADA` a uma coleção Tuple com 2 itens, na expressão `('CANCELADA', 'Cancelada')`.

**Linha 468 — ClassDef** (nível 1 do bloco).

Define a classe `Resultado` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 468:

**Linha 469 — Assign** (nível 2 do bloco).

Associa `SEM_IMPEDIMENTO` a uma coleção Tuple com 2 itens, na expressão `('SEM_IMPEDIMENTO_IDENTIFICADO', 'Apto')`.

**Linha 473 — Assign** (nível 2 do bloco).

Associa `TEMPORARIA` a uma coleção Tuple com 2 itens, na expressão `('INAPTIDAO_TEMPORARIA', 'Inaptidão temporária')`.

**Linha 477 — Assign** (nível 2 do bloco).

Associa `DEFINITIVA` a uma coleção Tuple com 2 itens, na expressão `('INAPTIDAO_DEFINITIVA', 'Inaptidão definitiva')`.

**Linha 481 — Assign** (nível 2 do bloco).

Associa `AVALIACAO` a uma coleção Tuple com 2 itens, na expressão `('AVALIACAO_PRESENCIAL', 'Avaliação presencial necessária')`.

**Linha 485 — Assign** (nível 2 do bloco).

Associa `DOCUMENTACAO` a uma coleção Tuple com 2 itens, na expressão `('DOCUMENTACAO_ESPECIAL', 'Documentação especial')`.

**Linha 490 — Assign** (nível 1 do bloco).

Associa `id_triagem` a a chamada `models.BigAutoField`; argumentos nomeados: `primary_key=True`.

- `primary_key=True`: define o identificador principal do registro.

**Linha 492 — Assign** (nível 1 do bloco).

Associa `usuario` a a chamada `models.ForeignKey`; argumentos posicionais: `settings.AUTH_USER_MODEL`; argumentos nomeados: `on_delete=models.CASCADE`, `related_name='triagens'`, `db_column='id_usuario'`.

- `on_delete=models.CASCADE`: comportamento quando o registro relacionado é excluído.
- `related_name='triagens'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_usuario'`: nome da coluna no banco.

**Linha 499 — Assign** (nível 1 do bloco).

Associa `modalidade` a a chamada `models.CharField`; argumentos nomeados: `max_length=20`, `choices=Modalidade.choices`, `default=Modalidade.EXTENSA`.

- `max_length=20`: limite de comprimento do campo.
- `choices=Modalidade.choices`: alternativas declaradas para validação e apresentação.
- `default=Modalidade.EXTENSA`: valor inicial quando não é informado outro.

**Linha 505 — Assign** (nível 1 do bloco).

Associa `status` a a chamada `models.CharField`; argumentos nomeados: `max_length=20`, `choices=Status.choices`, `default=Status.EM_ANDAMENTO`.

- `max_length=20`: limite de comprimento do campo.
- `choices=Status.choices`: alternativas declaradas para validação e apresentação.
- `default=Status.EM_ANDAMENTO`: valor inicial quando não é informado outro.

**Linha 511 — Assign** (nível 1 do bloco).

Associa `pergunta_atual` a a chamada `models.PositiveIntegerField`; argumentos nomeados: `default=0`.

- `default=0`: valor inicial quando não é informado outro.

**Linha 512 — Assign** (nível 1 do bloco).

Associa `fluxo_perguntas` a a chamada `models.JSONField`; argumentos nomeados: `default=list`, `blank=True`.

- `default=list`: valor inicial quando não é informado outro.
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 514 — Assign** (nível 1 do bloco).

Associa `triagem_base` a a chamada `models.ForeignKey`; argumentos posicionais: `'self'`; argumentos nomeados: `on_delete=models.SET_NULL`, `null=True`, `blank=True`, `related_name='verificacoes_simplificadas'`.

- `on_delete=models.SET_NULL`: comportamento quando o registro relacionado é excluído.
- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.
- `related_name='verificacoes_simplificadas'`: nome usado ao consultar a relação pelo lado inverso.

**Linha 522 — Assign** (nível 1 do bloco).

Associa `regra_version` a a chamada `models.CharField`; argumentos nomeados: `max_length=40`, `default='HEMOMINAS_2026_08'`.

- `max_length=40`: limite de comprimento do campo.
- `default='HEMOMINAS_2026_08'`: valor inicial quando não é informado outro.

**Linha 527 — Assign** (nível 1 do bloco).

Associa `resultado` a a chamada `models.CharField`; argumentos nomeados: `max_length=40`, `choices=Resultado.choices`, `blank=True`, `default=''`.

- `max_length=40`: limite de comprimento do campo.
- `choices=Resultado.choices`: alternativas declaradas para validação e apresentação.
- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 534 — Assign** (nível 1 do bloco).

Associa `mensagem_resultado` a a chamada `models.TextField`; argumentos nomeados: `blank=True`, `default=''`.

- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 539 — Assign** (nível 1 do bloco).

Associa `data_liberacao` a a chamada `models.DateField`; argumentos nomeados: `null=True`, `blank=True`.

- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 544 — Assign** (nível 1 do bloco).

Associa `achados` a a chamada `models.JSONField`; argumentos nomeados: `default=list`, `blank=True`.

- `default=list`: valor inicial quando não é informado outro.
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 549 — Assign** (nível 1 do bloco).

Associa `iniciada_em` a a chamada `models.DateTimeField`; argumentos nomeados: `auto_now_add=True`.

- `auto_now_add=True`: preenche a data/hora na criação.

**Linha 551 — Assign** (nível 1 do bloco).

Associa `finalizada_em` a a chamada `models.DateTimeField`; argumentos nomeados: `null=True`, `blank=True`.

- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 556 — Assign** (nível 1 do bloco).

Associa `atualizada_em` a a chamada `models.DateTimeField`; argumentos nomeados: `auto_now=True`.

- `auto_now=True`: atualiza a data/hora no save pertinente.

**Linha 558 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 558:

**Linha 559 — Assign** (nível 2 do bloco).

Associa `db_table` a o valor literal `'triagens'`.

**Linha 560 — Assign** (nível 2 do bloco).

Associa `ordering` a uma coleção List com 1 itens, na expressão `['-iniciada_em']`.

**Linha 562 — Assign** (nível 2 do bloco).

Associa `indexes` a uma coleção List com 2 itens, na expressão `[models.Index(fields=['usuario', '-iniciada_em'], name='triagem_usuario_data_idx'), models.Index(fields=['resultado', '-iniciada_em'], name='triagem_resultado_data_idx')]`.

**Linha 573 — Assign** (nível 2 do bloco).

Associa `verbose_name` a o valor literal `'Triagem'`.

**Linha 574 — Assign** (nível 2 do bloco).

Associa `verbose_name_plural` a o valor literal `'Triagens'`.

**Linha 576 — FunctionDef** (nível 1 do bloco).

Define `__str__(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 576:

**Linha 577 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o texto formatado `f'Triagem {self.id_triagem} - {self.usuario.nome} - {self.get_resultado_display()}'`, inserindo valores nas partes entre chaves ao chamador.

### Assign — linhas 586 a 586

```python
Triagem.Resultado.APTO = Triagem.Resultado.SEM_IMPEDIMENTO
```

**Explicação deste trecho:**

**Linha 586 — Assign** (nível 0 do bloco).

Associa `Triagem.Resultado.APTO` a o atributo `SEM_IMPEDIMENTO` de `Triagem.Resultado`.

### Assign — linhas 587 a 587

```python
Triagem.Resultado.INAPTO_TEMPORARIO = Triagem.Resultado.TEMPORARIA
```

**Explicação deste trecho:**

**Linha 587 — Assign** (nível 0 do bloco).

Associa `Triagem.Resultado.INAPTO_TEMPORARIO` a o atributo `TEMPORARIA` de `Triagem.Resultado`.

### Assign — linhas 588 a 588

```python
Triagem.Resultado.INAPTO_PERMANENTE = Triagem.Resultado.DEFINITIVA
```

**Explicação deste trecho:**

**Linha 588 — Assign** (nível 0 do bloco).

Associa `Triagem.Resultado.INAPTO_PERMANENTE` a o atributo `DEFINITIVA` de `Triagem.Resultado`.

### Assign — linhas 589 a 589

```python
Triagem.Resultado.AVALIACAO_PRESENCIAL_NECESSARIA = Triagem.Resultado.AVALIACAO
```

**Explicação deste trecho:**

**Linha 589 — Assign** (nível 0 do bloco).

Associa `Triagem.Resultado.AVALIACAO_PRESENCIAL_NECESSARIA` a o atributo `AVALIACAO` de `Triagem.Resultado`.

### RespostaTriagem — linhas 592 a 668

```python
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
```

**Explicação deste trecho:**

**Linha 592 — ClassDef** (nível 0 do bloco).

Define a classe `RespostaTriagem` herdando de `models.Model`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 592:

**Linha 593 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 600 — Assign** (nível 1 do bloco).

Associa `id_resposta` a a chamada `models.BigAutoField`; argumentos nomeados: `primary_key=True`.

- `primary_key=True`: define o identificador principal do registro.

**Linha 602 — Assign** (nível 1 do bloco).

Associa `triagem` a a chamada `models.ForeignKey`; argumentos posicionais: `Triagem`; argumentos nomeados: `on_delete=models.CASCADE`, `related_name='respostas'`, `db_column='id_triagem'`.

- `on_delete=models.CASCADE`: comportamento quando o registro relacionado é excluído.
- `related_name='respostas'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_triagem'`: nome da coluna no banco.

**Linha 609 — Assign** (nível 1 do bloco).

Associa `id_pergunta` a a chamada `models.CharField`; argumentos nomeados: `max_length=20`.

- `max_length=20`: limite de comprimento do campo.

**Linha 610 — Assign** (nível 1 do bloco).

Associa `codigo_resposta` a a chamada `models.CharField`; argumentos nomeados: `max_length=80`.

- `max_length=80`: limite de comprimento do campo.

**Linha 611 — Assign** (nível 1 do bloco).

Associa `resposta_label` a a chamada `models.CharField`; argumentos nomeados: `max_length=255`.

- `max_length=255`: limite de comprimento do campo.

**Linha 613 — Assign** (nível 1 do bloco).

Associa `data_evento` a a chamada `models.DateField`; argumentos nomeados: `db_column='event_date'`, `null=True`, `blank=True`.

- `db_column='event_date'`: nome da coluna no banco.
- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 619 — Assign** (nível 1 do bloco).

Associa `metadata` a a chamada `models.JSONField`; argumentos nomeados: `default=dict`, `blank=True`.

- `default=dict`: valor inicial quando não é informado outro.
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 624 — Assign** (nível 1 do bloco).

Associa `valor` a a chamada `models.JSONField`; argumentos nomeados: `default=dict`, `blank=True`.

- `default=dict`: valor inicial quando não é informado outro.
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 629 — Assign** (nível 1 do bloco).

Associa `rule_version` a a chamada `models.CharField`; argumentos nomeados: `max_length=40`, `default='HEMOMINAS_2026_08'`.

- `max_length=40`: limite de comprimento do campo.
- `default='HEMOMINAS_2026_08'`: valor inicial quando não é informado outro.

**Linha 634 — Assign** (nível 1 do bloco).

Associa `source_ref` a a chamada `models.CharField`; argumentos nomeados: `max_length=255`, `blank=True`, `default=''`.

- `max_length=255`: limite de comprimento do campo.
- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 640 — Assign** (nível 1 do bloco).

Associa `respondido_em` a a chamada `models.DateTimeField`; argumentos nomeados: `auto_now_add=True`.

- `auto_now_add=True`: preenche a data/hora na criação.

**Linha 642 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 642:

**Linha 643 — Assign** (nível 2 do bloco).

Associa `db_table` a o valor literal `'respostas_triagem'`.

**Linha 644 — Assign** (nível 2 do bloco).

Associa `ordering` a uma coleção List com 1 itens, na expressão `['id_resposta']`.

**Linha 646 — Assign** (nível 2 do bloco).

Associa `constraints` a uma coleção List com 1 itens, na expressão `[models.UniqueConstraint(fields=['triagem', 'id_pergunta'], name='resposta_unica_por_pergunta')]`.

**Linha 653 — Assign** (nível 2 do bloco).

Associa `indexes` a uma coleção List com 1 itens, na expressão `[models.Index(fields=['triagem', 'id_pergunta'], name='resposta_triagem_pergunta_idx')]`.

**Linha 660 — Assign** (nível 2 do bloco).

Associa `verbose_name` a o valor literal `'Resposta triagem'`.

**Linha 661 — Assign** (nível 2 do bloco).

Associa `verbose_name_plural` a o valor literal `'Respostas triagem'`.

**Linha 663 — FunctionDef** (nível 1 do bloco).

Define `__str__(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 663:

**Linha 664 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o texto formatado `f'{self.triagem_id} - {self.id_pergunta} - {self.codigo_resposta}'`, inserindo valores nas partes entre chaves ao chamador.

### Estoque — linhas 671 a 785

```python
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
```

**Explicação deste trecho:**

**Linha 671 — ClassDef** (nível 0 do bloco).

Define a classe `Estoque` herdando de `models.Model`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 671:

**Linha 672 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 687 — ClassDef** (nível 1 do bloco).

Define a classe `StatusCalculado` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 687:

**Linha 688 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 696 — Assign** (nível 2 do bloco).

Associa `CRITICO` a uma coleção Tuple com 2 itens, na expressão `('CRITICO', 'Crítico')`.

**Linha 697 — Assign** (nível 2 do bloco).

Associa `BAIXO` a uma coleção Tuple com 2 itens, na expressão `('BAIXO', 'Baixo')`.

**Linha 698 — Assign** (nível 2 do bloco).

Associa `ESTAVEL` a uma coleção Tuple com 2 itens, na expressão `('ESTAVEL', 'Estável')`.

**Linha 700 — Assign** (nível 1 do bloco).

Associa `id_estoque` a a chamada `models.BigAutoField`; argumentos nomeados: `primary_key=True`.

- `primary_key=True`: define o identificador principal do registro.

**Linha 702 — Assign** (nível 1 do bloco).

Associa `hemocentro` a a chamada `models.ForeignKey`; argumentos posicionais: `settings.AUTH_USER_MODEL`; argumentos nomeados: `on_delete=models.CASCADE`, `related_name='estoques'`, `db_column='id_hemocentro'`, `limit_choices_to={'perfil': 'HEMOCENTRO'}`.

- `on_delete=models.CASCADE`: comportamento quando o registro relacionado é excluído.
- `related_name='estoques'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_hemocentro'`: nome da coluna no banco.
- `limit_choices_to={'perfil': 'HEMOCENTRO'}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 710 — Assign** (nível 1 do bloco).

Associa `tipo_sanguineo` a a chamada `models.CharField`; argumentos nomeados: `max_length=3`, `choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS]`.

- `max_length=3`: limite de comprimento do campo.
- `choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS]`: alternativas declaradas para validação e apresentação.

**Linha 715 — Assign** (nível 1 do bloco).

Associa `quantidade_bolsas` a a chamada `models.PositiveIntegerField`; argumentos nomeados: `default=0`.

- `default=0`: valor inicial quando não é informado outro.

**Linha 716 — Assign** (nível 1 do bloco).

Associa `nivel_minimo` a a chamada `models.PositiveIntegerField`.


**Linha 717 — Assign** (nível 1 do bloco).

Associa `nivel_critico` a a chamada `models.PositiveIntegerField`.


**Linha 719 — Assign** (nível 1 do bloco).

Associa `status_calculado` a a chamada `models.CharField`; argumentos nomeados: `max_length=10`, `choices=StatusCalculado.choices`, `default=StatusCalculado.ESTAVEL`.

- `max_length=10`: limite de comprimento do campo.
- `choices=StatusCalculado.choices`: alternativas declaradas para validação e apresentação.
- `default=StatusCalculado.ESTAVEL`: valor inicial quando não é informado outro.

**Linha 725 — Assign** (nível 1 do bloco).

Associa `data_atualizacao` a a chamada `models.DateTimeField`; argumentos nomeados: `auto_now=True`.

- `auto_now=True`: atualiza a data/hora no save pertinente.

**Linha 727 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 727:

**Linha 728 — Assign** (nível 2 do bloco).

Associa `db_table` a o valor literal `'estoques'`.

**Linha 729 — Assign** (nível 2 do bloco).

Associa `verbose_name` a o valor literal `'estoque'`.

**Linha 730 — Assign** (nível 2 do bloco).

Associa `verbose_name_plural` a o valor literal `'estoques'`.

**Linha 731 — Assign** (nível 2 do bloco).

Associa `ordering` a uma coleção List com 2 itens, na expressão `['hemocentro__nome', 'tipo_sanguineo']`.

**Linha 733 — Assign** (nível 2 do bloco).

Associa `constraints` a uma coleção List com 1 itens, na expressão `[models.UniqueConstraint(fields=['hemocentro', 'tipo_sanguineo'], name='estoque_unico_por_hemocentro_tipo')]`.

**Linha 740 — Assign** (nível 2 do bloco).

Associa `indexes` a uma coleção List com 2 itens, na expressão `[models.Index(fields=['hemocentro', 'tipo_sanguineo'], name='estoque_hemo_tipo_idx'), models.Index(fields=['status_calculado'], name='estoque_status_idx')]`.

**Linha 751 — FunctionDef** (nível 1 do bloco).

Define `clean(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 751:

**Linha 752 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 754 — Expr** (nível 2 do bloco).

Executa a chamada `super().clean`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 756 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `self.hemocentro_id` ; `self.hemocentro.perfil != Usuario.Perfil.HEMOCENTRO` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 756:

**Linha 760 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `{'hemocentro': 'Somente contas com perfil Hemocentro podem ter estoque.'}`.

**Linha 768 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `self.nivel_minimo is not None` ; `self.nivel_critico is not None` ; `self.nivel_critico > self.nivel_minimo` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 768:

**Linha 773 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `{'nivel_critico': 'O nivel critico deve ser menor ou igual ao nivel minimo.'}`.

**Linha 781 — FunctionDef** (nível 1 do bloco).

Define `__str__(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 781:

**Linha 782 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o texto formatado `f'{self.hemocentro.nome} - {self.tipo_sanguineo} ({self.get_status_calculado_display()})'`, inserindo valores nas partes entre chaves ao chamador.

### EstoqueMovimentacao — linhas 788 a 862

```python
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
```

**Explicação deste trecho:**

**Linha 788 — ClassDef** (nível 0 do bloco).

Define a classe `EstoqueMovimentacao` herdando de `models.Model`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 788:

**Linha 789 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 800 — ClassDef** (nível 1 do bloco).

Define a classe `TipoMovimento` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 800:

**Linha 801 — Assign** (nível 2 do bloco).

Associa `ENTRADA` a uma coleção Tuple com 2 itens, na expressão `('ENTRADA', 'Entrada')`.

**Linha 802 — Assign** (nível 2 do bloco).

Associa `SAIDA` a uma coleção Tuple com 2 itens, na expressão `('SAIDA', 'Saída')`.

**Linha 803 — Assign** (nível 2 do bloco).

Associa `AJUSTE` a uma coleção Tuple com 2 itens, na expressão `('AJUSTE', 'Ajuste')`.

**Linha 805 — Assign** (nível 1 do bloco).

Associa `id_mov` a a chamada `models.BigAutoField`; argumentos nomeados: `primary_key=True`.

- `primary_key=True`: define o identificador principal do registro.

**Linha 807 — Assign** (nível 1 do bloco).

Associa `estoque` a a chamada `models.ForeignKey`; argumentos posicionais: `Estoque`; argumentos nomeados: `on_delete=models.CASCADE`, `related_name='movimentacoes'`, `db_column='id_estoque'`.

- `on_delete=models.CASCADE`: comportamento quando o registro relacionado é excluído.
- `related_name='movimentacoes'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_estoque'`: nome da coluna no banco.

**Linha 814 — Assign** (nível 1 do bloco).

Associa `usuario_resp` a a chamada `models.ForeignKey`; argumentos posicionais: `settings.AUTH_USER_MODEL`; argumentos nomeados: `on_delete=models.SET_NULL`, `null=True`, `blank=True`, `related_name='movimentacoes_estoque_realizadas'`, `db_column='id_usuario_resp'`.

- `on_delete=models.SET_NULL`: comportamento quando o registro relacionado é excluído.
- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.
- `related_name='movimentacoes_estoque_realizadas'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_usuario_resp'`: nome da coluna no banco.

**Linha 823 — Assign** (nível 1 do bloco).

Associa `tipo_movimento` a a chamada `models.CharField`; argumentos nomeados: `max_length=10`, `choices=TipoMovimento.choices`.

- `max_length=10`: limite de comprimento do campo.
- `choices=TipoMovimento.choices`: alternativas declaradas para validação e apresentação.

**Linha 828 — Assign** (nível 1 do bloco).

Associa `quantidade_anterior` a a chamada `models.PositiveIntegerField`.


**Linha 829 — Assign** (nível 1 do bloco).

Associa `quantidade_movimentada` a a chamada `models.IntegerField`.


**Linha 830 — Assign** (nível 1 do bloco).

Associa `quantidade_nova` a a chamada `models.PositiveIntegerField`.


**Linha 832 — Assign** (nível 1 do bloco).

Associa `motivo` a a chamada `models.CharField`; argumentos nomeados: `max_length=255`, `blank=True`, `default=''`.

- `max_length=255`: limite de comprimento do campo.
- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 838 — Assign** (nível 1 do bloco).

Associa `data_hora` a a chamada `models.DateTimeField`; argumentos nomeados: `auto_now_add=True`.

- `auto_now_add=True`: preenche a data/hora na criação.

**Linha 840 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 840:

**Linha 841 — Assign** (nível 2 do bloco).

Associa `db_table` a o valor literal `'movimentacoes_estoque'`.

**Linha 842 — Assign** (nível 2 do bloco).

Associa `verbose_name` a o valor literal `'movimentacao de estoque'`.

**Linha 843 — Assign** (nível 2 do bloco).

Associa `verbose_name_plural` a o valor literal `'movimentacoes de estoque'`.

**Linha 844 — Assign** (nível 2 do bloco).

Associa `ordering` a uma coleção List com 1 itens, na expressão `['-data_hora']`.

**Linha 846 — Assign** (nível 2 do bloco).

Associa `indexes` a uma coleção List com 2 itens, na expressão `[models.Index(fields=['estoque', '-data_hora'], name='mov_estoque_data_idx'), models.Index(fields=['usuario_resp', '-data_hora'], name='mov_usuario_data_idx')]`.

**Linha 857 — FunctionDef** (nível 1 do bloco).

Define `__str__(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 857:

**Linha 858 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o texto formatado `f'{self.estoque.tipo_sanguineo} - {self.get_tipo_movimento_display()} - {self.quantidade_anterior} -> {self.quantidade_nova}'`, inserindo valores nas partes entre chaves ao chamador.

### Notificacao — linhas 865 a 942

```python
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
        PEDIDO_COMPATIVEL = "PEDIDO_COMPATIVEL", "Pedido compatível"
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

    pedido = models.ForeignKey(
        "PedidoSangue",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notificacoes",
        db_column="id_pedido",
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
```

**Explicação deste trecho:**

**Linha 865 — ClassDef** (nível 0 do bloco).

Define a classe `Notificacao` herdando de `models.Model`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 865:

**Linha 866 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 874 — ClassDef** (nível 1 do bloco).

Define a classe `Tipo` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 874:

**Linha 875 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 877 — Assign** (nível 2 do bloco).

Associa `ESTOQUE_BAIXO` a uma coleção Tuple com 2 itens, na expressão `('ESTOQUE_BAIXO', 'Estoque baixo')`.

**Linha 878 — Assign** (nível 2 do bloco).

Associa `ESTOQUE_CRITICO` a uma coleção Tuple com 2 itens, na expressão `('ESTOQUE_CRITICO', 'Estoque crítico')`.

**Linha 879 — Assign** (nível 2 do bloco).

Associa `PEDIDO_COMPATIVEL` a uma coleção Tuple com 2 itens, na expressão `('PEDIDO_COMPATIVEL', 'Pedido compatível')`.

**Linha 880 — Assign** (nível 2 do bloco).

Associa `GERAL` a uma coleção Tuple com 2 itens, na expressão `('GERAL', 'Aviso geral')`.

**Linha 882 — Assign** (nível 1 do bloco).

Associa `id_notificacao` a a chamada `models.BigAutoField`; argumentos nomeados: `primary_key=True`.

- `primary_key=True`: define o identificador principal do registro.

**Linha 884 — Assign** (nível 1 do bloco).

Associa `usuario` a a chamada `models.ForeignKey`; argumentos posicionais: `settings.AUTH_USER_MODEL`; argumentos nomeados: `on_delete=models.CASCADE`, `related_name='notificacoes'`, `db_column='id_usuario'`.

- `on_delete=models.CASCADE`: comportamento quando o registro relacionado é excluído.
- `related_name='notificacoes'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_usuario'`: nome da coluna no banco.

**Linha 891 — Assign** (nível 1 do bloco).

Associa `estoque` a a chamada `models.ForeignKey`; argumentos posicionais: `Estoque`; argumentos nomeados: `on_delete=models.SET_NULL`, `null=True`, `blank=True`, `related_name='notificacoes'`, `db_column='id_estoque'`.

- `on_delete=models.SET_NULL`: comportamento quando o registro relacionado é excluído.
- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.
- `related_name='notificacoes'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_estoque'`: nome da coluna no banco.

**Linha 900 — Assign** (nível 1 do bloco).

Associa `pedido` a a chamada `models.ForeignKey`; argumentos posicionais: `'PedidoSangue'`; argumentos nomeados: `on_delete=models.SET_NULL`, `null=True`, `blank=True`, `related_name='notificacoes'`, `db_column='id_pedido'`.

- `on_delete=models.SET_NULL`: comportamento quando o registro relacionado é excluído.
- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.
- `related_name='notificacoes'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_pedido'`: nome da coluna no banco.

**Linha 909 — Assign** (nível 1 do bloco).

Associa `tipo` a a chamada `models.CharField`; argumentos nomeados: `max_length=30`, `choices=Tipo.choices`, `default=Tipo.GERAL`.

- `max_length=30`: limite de comprimento do campo.
- `choices=Tipo.choices`: alternativas declaradas para validação e apresentação.
- `default=Tipo.GERAL`: valor inicial quando não é informado outro.

**Linha 915 — Assign** (nível 1 do bloco).

Associa `titulo` a a chamada `models.CharField`; argumentos nomeados: `max_length=120`.

- `max_length=120`: limite de comprimento do campo.

**Linha 916 — Assign** (nível 1 do bloco).

Associa `mensagem` a a chamada `models.TextField`.


**Linha 917 — Assign** (nível 1 do bloco).

Associa `url_destino` a a chamada `models.CharField`; argumentos nomeados: `max_length=255`, `blank=True`, `default=''`.

- `max_length=255`: limite de comprimento do campo.
- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 918 — Assign** (nível 1 do bloco).

Associa `lida` a a chamada `models.BooleanField`; argumentos nomeados: `default=False`.

- `default=False`: valor inicial quando não é informado outro.

**Linha 919 — Assign** (nível 1 do bloco).

Associa `criada_em` a a chamada `models.DateTimeField`; argumentos nomeados: `auto_now_add=True`.

- `auto_now_add=True`: preenche a data/hora na criação.

**Linha 920 — Assign** (nível 1 do bloco).

Associa `lida_em` a a chamada `models.DateTimeField`; argumentos nomeados: `null=True`, `blank=True`.

- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 922 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 922:

**Linha 923 — Assign** (nível 2 do bloco).

Associa `db_table` a o valor literal `'notificacoes'`.

**Linha 924 — Assign** (nível 2 do bloco).

Associa `verbose_name` a o valor literal `'notificacao'`.

**Linha 925 — Assign** (nível 2 do bloco).

Associa `verbose_name_plural` a o valor literal `'notificacoes'`.

**Linha 926 — Assign** (nível 2 do bloco).

Associa `ordering` a uma coleção List com 1 itens, na expressão `['-criada_em']`.

**Linha 928 — Assign** (nível 2 do bloco).

Associa `indexes` a uma coleção List com 2 itens, na expressão `[models.Index(fields=['usuario', 'lida', '-criada_em'], name='notificacao_usuario_lida_idx'), models.Index(fields=['tipo', '-criada_em'], name='notificacao_tipo_data_idx')]`.

**Linha 939 — FunctionDef** (nível 1 do bloco).

Define `__str__(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 939:

**Linha 940 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 942 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o texto formatado `f'{self.usuario.nome} - {self.titulo}'`, inserindo valores nas partes entre chaves ao chamador.

### PedidoSangue — linhas 945 a 1109

```python
class PedidoSangue(models.Model):
    """
    Rf - Pedido de Sangue.

    Guarda solicitações de divulgação e os pedidos publicados oficialmente.

    Doador, Receptor, Observador e Visitante criam somente uma solicitação.
    A publicação oficial é feita pelo Hemocentro aprovado vinculado.
    """

    class ParaQuem(models.TextChoices):
        MIM = "MIM", "Para mim"
        OUTRA_PESSOA = "OUTRA_PESSOA", "Para outra pessoa"

    class Urgencia(models.TextChoices):
        BAIXA = "BAIXA", "Baixa"
        MEDIA = "MEDIA", "Media"
        ALTA = "ALTA", "Alta"
        CRITICA = "CRITICA", "Critica"

    class Status(models.TextChoices):
        ENVIADA = "ENVIADA", "Enviada"
        EM_ANALISE = "EM_ANALISE", "Em análise"
        PUBLICADA = "PUBLICADA", "Publicada"
        CORRECAO_SOLICITADA = "CORRECAO_SOLICITADA", "Correção solicitada"
        RECUSADA = "RECUSADA", "Recusada"
        ENCERRADA = "ENCERRADA", "Encerrada"

    id_pedido = models.BigAutoField(primary_key=True)

    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pedidos_sangue",
        db_column="id_solicitante",
    )

    nome_solicitante = models.CharField(max_length=150, default="")
    contato = models.EmailField(max_length=120, default="")

    hemocentro_destino = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pedidos_recebidos",
        db_column="id_hemocentro_destino",
        limit_choices_to={"perfil": "HEMOCENTRO"},
    )

    para_quem = models.CharField(
        max_length=20,
        choices=ParaQuem.choices,
    )

    titulo = models.CharField(
        max_length=150,
        default="Pedido de sangue",
    )

    tipo_sanguineo = models.CharField(
        max_length=3,
        choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
    )

    urgencia = models.CharField(
        max_length=10,
        choices=Urgencia.choices,
    )

    cidade = models.CharField(max_length=100)
    nome_paciente = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )
    descricao = models.TextField()
    justificativa_urgencia = models.TextField(blank=True, default="")
    informacoes_complementares = models.TextField(blank=True, default="")

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.ENVIADA,
    )

    duplicidade_suspeita = models.BooleanField(default=False)

    publicado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pedidos_publicados",
        db_column="id_publicado_por",
    )
    publicado_em = models.DateTimeField(null=True, blank=True)

    data_criacao = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    data_fechamento = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "pedidos_sangue"
        ordering = ["-data_criacao"]
        verbose_name = "pedido de sangue"
        verbose_name_plural = "pedidos de sangue"

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

        if self.solicitante_id and self.solicitante.perfil in {
            Usuario.Perfil.HEMOCENTRO,
            Usuario.Perfil.ADMINISTRADOR,
        }:
            raise ValidationError(
                {"solicitante": "Este perfil não pode enviar solicitações."}
            )

        if self.status == self.Status.PUBLICADA:
            if not self.publicado_por_id or not self.publicado_por:
                raise ValidationError(
                    {"publicado_por": "A publicação precisa de um Hemocentro aprovado."}
                )
            if not (
                self.publicado_por.perfil == Usuario.Perfil.HEMOCENTRO
                and self.publicado_por.status_validacao
                == Usuario.StatusValidacaoHemocentro.APROVADO
            ):
                raise ValidationError(
                    {"publicado_por": "Somente Hemocentro aprovado pode publicar."}
                )

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
```

**Explicação deste trecho:**

**Linha 945 — ClassDef** (nível 0 do bloco).

Define a classe `PedidoSangue` herdando de `models.Model`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 945:

**Linha 946 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 955 — ClassDef** (nível 1 do bloco).

Define a classe `ParaQuem` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 955:

**Linha 956 — Assign** (nível 2 do bloco).

Associa `MIM` a uma coleção Tuple com 2 itens, na expressão `('MIM', 'Para mim')`.

**Linha 957 — Assign** (nível 2 do bloco).

Associa `OUTRA_PESSOA` a uma coleção Tuple com 2 itens, na expressão `('OUTRA_PESSOA', 'Para outra pessoa')`.

**Linha 959 — ClassDef** (nível 1 do bloco).

Define a classe `Urgencia` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 959:

**Linha 960 — Assign** (nível 2 do bloco).

Associa `BAIXA` a uma coleção Tuple com 2 itens, na expressão `('BAIXA', 'Baixa')`.

**Linha 961 — Assign** (nível 2 do bloco).

Associa `MEDIA` a uma coleção Tuple com 2 itens, na expressão `('MEDIA', 'Media')`.

**Linha 962 — Assign** (nível 2 do bloco).

Associa `ALTA` a uma coleção Tuple com 2 itens, na expressão `('ALTA', 'Alta')`.

**Linha 963 — Assign** (nível 2 do bloco).

Associa `CRITICA` a uma coleção Tuple com 2 itens, na expressão `('CRITICA', 'Critica')`.

**Linha 965 — ClassDef** (nível 1 do bloco).

Define a classe `Status` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 965:

**Linha 966 — Assign** (nível 2 do bloco).

Associa `ENVIADA` a uma coleção Tuple com 2 itens, na expressão `('ENVIADA', 'Enviada')`.

**Linha 967 — Assign** (nível 2 do bloco).

Associa `EM_ANALISE` a uma coleção Tuple com 2 itens, na expressão `('EM_ANALISE', 'Em análise')`.

**Linha 968 — Assign** (nível 2 do bloco).

Associa `PUBLICADA` a uma coleção Tuple com 2 itens, na expressão `('PUBLICADA', 'Publicada')`.

**Linha 969 — Assign** (nível 2 do bloco).

Associa `CORRECAO_SOLICITADA` a uma coleção Tuple com 2 itens, na expressão `('CORRECAO_SOLICITADA', 'Correção solicitada')`.

**Linha 970 — Assign** (nível 2 do bloco).

Associa `RECUSADA` a uma coleção Tuple com 2 itens, na expressão `('RECUSADA', 'Recusada')`.

**Linha 971 — Assign** (nível 2 do bloco).

Associa `ENCERRADA` a uma coleção Tuple com 2 itens, na expressão `('ENCERRADA', 'Encerrada')`.

**Linha 973 — Assign** (nível 1 do bloco).

Associa `id_pedido` a a chamada `models.BigAutoField`; argumentos nomeados: `primary_key=True`.

- `primary_key=True`: define o identificador principal do registro.

**Linha 975 — Assign** (nível 1 do bloco).

Associa `solicitante` a a chamada `models.ForeignKey`; argumentos posicionais: `settings.AUTH_USER_MODEL`; argumentos nomeados: `on_delete=models.SET_NULL`, `null=True`, `blank=True`, `related_name='pedidos_sangue'`, `db_column='id_solicitante'`.

- `on_delete=models.SET_NULL`: comportamento quando o registro relacionado é excluído.
- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.
- `related_name='pedidos_sangue'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_solicitante'`: nome da coluna no banco.

**Linha 984 — Assign** (nível 1 do bloco).

Associa `nome_solicitante` a a chamada `models.CharField`; argumentos nomeados: `max_length=150`, `default=''`.

- `max_length=150`: limite de comprimento do campo.
- `default=''`: valor inicial quando não é informado outro.

**Linha 985 — Assign** (nível 1 do bloco).

Associa `contato` a a chamada `models.EmailField`; argumentos nomeados: `max_length=120`, `default=''`.

- `max_length=120`: limite de comprimento do campo.
- `default=''`: valor inicial quando não é informado outro.

**Linha 987 — Assign** (nível 1 do bloco).

Associa `hemocentro_destino` a a chamada `models.ForeignKey`; argumentos posicionais: `settings.AUTH_USER_MODEL`; argumentos nomeados: `on_delete=models.PROTECT`, `related_name='pedidos_recebidos'`, `db_column='id_hemocentro_destino'`, `limit_choices_to={'perfil': 'HEMOCENTRO'}`.

- `on_delete=models.PROTECT`: comportamento quando o registro relacionado é excluído.
- `related_name='pedidos_recebidos'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_hemocentro_destino'`: nome da coluna no banco.
- `limit_choices_to={'perfil': 'HEMOCENTRO'}`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 995 — Assign** (nível 1 do bloco).

Associa `para_quem` a a chamada `models.CharField`; argumentos nomeados: `max_length=20`, `choices=ParaQuem.choices`.

- `max_length=20`: limite de comprimento do campo.
- `choices=ParaQuem.choices`: alternativas declaradas para validação e apresentação.

**Linha 1000 — Assign** (nível 1 do bloco).

Associa `titulo` a a chamada `models.CharField`; argumentos nomeados: `max_length=150`, `default='Pedido de sangue'`.

- `max_length=150`: limite de comprimento do campo.
- `default='Pedido de sangue'`: valor inicial quando não é informado outro.

**Linha 1005 — Assign** (nível 1 do bloco).

Associa `tipo_sanguineo` a a chamada `models.CharField`; argumentos nomeados: `max_length=3`, `choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS]`.

- `max_length=3`: limite de comprimento do campo.
- `choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS]`: alternativas declaradas para validação e apresentação.

**Linha 1010 — Assign** (nível 1 do bloco).

Associa `urgencia` a a chamada `models.CharField`; argumentos nomeados: `max_length=10`, `choices=Urgencia.choices`.

- `max_length=10`: limite de comprimento do campo.
- `choices=Urgencia.choices`: alternativas declaradas para validação e apresentação.

**Linha 1015 — Assign** (nível 1 do bloco).

Associa `cidade` a a chamada `models.CharField`; argumentos nomeados: `max_length=100`.

- `max_length=100`: limite de comprimento do campo.

**Linha 1016 — Assign** (nível 1 do bloco).

Associa `nome_paciente` a a chamada `models.CharField`; argumentos nomeados: `max_length=150`, `blank=True`, `default=''`.

- `max_length=150`: limite de comprimento do campo.
- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 1021 — Assign** (nível 1 do bloco).

Associa `descricao` a a chamada `models.TextField`.


**Linha 1022 — Assign** (nível 1 do bloco).

Associa `justificativa_urgencia` a a chamada `models.TextField`; argumentos nomeados: `blank=True`, `default=''`.

- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 1023 — Assign** (nível 1 do bloco).

Associa `informacoes_complementares` a a chamada `models.TextField`; argumentos nomeados: `blank=True`, `default=''`.

- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 1025 — Assign** (nível 1 do bloco).

Associa `status` a a chamada `models.CharField`; argumentos nomeados: `max_length=30`, `choices=Status.choices`, `default=Status.ENVIADA`.

- `max_length=30`: limite de comprimento do campo.
- `choices=Status.choices`: alternativas declaradas para validação e apresentação.
- `default=Status.ENVIADA`: valor inicial quando não é informado outro.

**Linha 1031 — Assign** (nível 1 do bloco).

Associa `duplicidade_suspeita` a a chamada `models.BooleanField`; argumentos nomeados: `default=False`.

- `default=False`: valor inicial quando não é informado outro.

**Linha 1033 — Assign** (nível 1 do bloco).

Associa `publicado_por` a a chamada `models.ForeignKey`; argumentos posicionais: `settings.AUTH_USER_MODEL`; argumentos nomeados: `on_delete=models.SET_NULL`, `null=True`, `blank=True`, `related_name='pedidos_publicados'`, `db_column='id_publicado_por'`.

- `on_delete=models.SET_NULL`: comportamento quando o registro relacionado é excluído.
- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.
- `related_name='pedidos_publicados'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_publicado_por'`: nome da coluna no banco.

**Linha 1041 — Assign** (nível 1 do bloco).

Associa `publicado_em` a a chamada `models.DateTimeField`; argumentos nomeados: `null=True`, `blank=True`.

- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 1043 — Assign** (nível 1 do bloco).

Associa `data_criacao` a a chamada `models.DateTimeField`; argumentos nomeados: `auto_now_add=True`.

- `auto_now_add=True`: preenche a data/hora na criação.

**Linha 1044 — Assign** (nível 1 do bloco).

Associa `atualizado_em` a a chamada `models.DateTimeField`; argumentos nomeados: `auto_now=True`.

- `auto_now=True`: atualiza a data/hora no save pertinente.

**Linha 1045 — Assign** (nível 1 do bloco).

Associa `data_fechamento` a a chamada `models.DateTimeField`; argumentos nomeados: `null=True`, `blank=True`.

- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.

**Linha 1047 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 1047:

**Linha 1048 — Assign** (nível 2 do bloco).

Associa `db_table` a o valor literal `'pedidos_sangue'`.

**Linha 1049 — Assign** (nível 2 do bloco).

Associa `ordering` a uma coleção List com 1 itens, na expressão `['-data_criacao']`.

**Linha 1050 — Assign** (nível 2 do bloco).

Associa `verbose_name` a o valor literal `'pedido de sangue'`.

**Linha 1051 — Assign** (nível 2 do bloco).

Associa `verbose_name_plural` a o valor literal `'pedidos de sangue'`.

**Linha 1053 — Assign** (nível 2 do bloco).

Associa `indexes` a uma coleção List com 3 itens, na expressão `[models.Index(fields=['status', '-data_criacao'], name='pedido_status_data_idx'), models.Index(fields=['tipo_sanguineo', 'urgencia'], name='pedido_tipo_urg_idx'), models.Index(fields=['cidade'], name='pedido_cidade_idx')]`.

**Linha 1068 — FunctionDef** (nível 1 do bloco).

Define `clean(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 1068:

**Linha 1069 — Expr** (nível 2 do bloco).

Executa a chamada `super().clean`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 1071 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `self.solicitante_id` ; `self.solicitante.perfil in {Usuario.Perfil.HEMOCENTRO, Usuario.Perfil.ADMINISTRADOR}` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1071:

**Linha 1075 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `{'solicitante': 'Este perfil não pode enviar solicitações.'}`.

**Linha 1079 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `self.status` igual a `self.Status.PUBLICADA`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1079:

**Linha 1080 — If** (nível 3 do bloco).

Escolhe um caminho verificando pelo menos uma das condições: `not self.publicado_por_id` ; `not self.publicado_por` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1080:

**Linha 1081 — Raise** (nível 4 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `{'publicado_por': 'A publicação precisa de um Hemocentro aprovado.'}`.

**Linha 1084 — If** (nível 3 do bloco).

Escolhe um caminho verificando a negação de `self.publicado_por.perfil == Usuario.Perfil.HEMOCENTRO and self.publicado_por.status_validacao == Usuario.StatusValidacaoHemocentro.APROVADO`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1084:

**Linha 1089 — Raise** (nível 4 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `{'publicado_por': 'Somente Hemocentro aprovado pode publicar.'}`.

**Linha 1093 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `self.hemocentro_destino_id` ; `self.hemocentro_destino.perfil != Usuario.Perfil.HEMOCENTRO` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 1093:

**Linha 1097 — Raise** (nível 3 do bloco).

Interrompe o caminho levantando a chamada `ValidationError`; argumentos posicionais: `{'hemocentro_destino': 'O destino precisa ser um Hemocentro cadastrado.'}`.

**Linha 1105 — FunctionDef** (nível 1 do bloco).

Define `__str__(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 1105:

**Linha 1106 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o texto formatado `f'{self.titulo} - {self.tipo_sanguineo} - {self.get_status_display()}'`, inserindo valores nas partes entre chaves ao chamador.

### Assign — linhas 1114 a 1114

```python
PedidoSangue.Status.PENDENTE_VALIDACAO = PedidoSangue.Status.ENVIADA
```

**Explicação deste trecho:**

**Linha 1114 — Assign** (nível 0 do bloco).

Associa `PedidoSangue.Status.PENDENTE_VALIDACAO` a o atributo `ENVIADA` de `PedidoSangue.Status`.

### Assign — linhas 1115 a 1115

```python
PedidoSangue.Status.ATIVO = PedidoSangue.Status.PUBLICADA
```

**Explicação deste trecho:**

**Linha 1115 — Assign** (nível 0 do bloco).

Associa `PedidoSangue.Status.ATIVO` a o atributo `PUBLICADA` de `PedidoSangue.Status`.

### Assign — linhas 1116 a 1116

```python
PedidoSangue.Status.SUSPEITO = PedidoSangue.Status.EM_ANALISE
```

**Explicação deste trecho:**

**Linha 1116 — Assign** (nível 0 do bloco).

Associa `PedidoSangue.Status.SUSPEITO` a o atributo `EM_ANALISE` de `PedidoSangue.Status`.

### Assign — linhas 1117 a 1117

```python
PedidoSangue.Status.RECUSADO = PedidoSangue.Status.RECUSADA
```

**Explicação deste trecho:**

**Linha 1117 — Assign** (nível 0 do bloco).

Associa `PedidoSangue.Status.RECUSADO` a o atributo `RECUSADA` de `PedidoSangue.Status`.

### Assign — linhas 1118 a 1118

```python
PedidoSangue.Status.ENCERRADO = PedidoSangue.Status.ENCERRADA
```

**Explicação deste trecho:**

**Linha 1118 — Assign** (nível 0 do bloco).

Associa `PedidoSangue.Status.ENCERRADO` a o atributo `ENCERRADA` de `PedidoSangue.Status`.

### ValidacaoPedido — linhas 1121 a 1166

```python
class ValidacaoPedido(models.Model):
    """
    Uc_17 - Validar Pedido.

    Guarda o historico das validacoes feitas automaticamente ou por moderador.
    """

    class StatusValidacao(models.TextChoices):
        APROVADO = "APROVADO", "Aprovado"
        CORRECAO_SOLICITADA = "CORRECAO_SOLICITADA", "Correção solicitada"
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
```

**Explicação deste trecho:**

**Linha 1121 — ClassDef** (nível 0 do bloco).

Define a classe `ValidacaoPedido` herdando de `models.Model`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 1121:

**Linha 1122 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 1128 — ClassDef** (nível 1 do bloco).

Define a classe `StatusValidacao` herdando de `models.TextChoices`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 1128:

**Linha 1129 — Assign** (nível 2 do bloco).

Associa `APROVADO` a uma coleção Tuple com 2 itens, na expressão `('APROVADO', 'Aprovado')`.

**Linha 1130 — Assign** (nível 2 do bloco).

Associa `CORRECAO_SOLICITADA` a uma coleção Tuple com 2 itens, na expressão `('CORRECAO_SOLICITADA', 'Correção solicitada')`.

**Linha 1131 — Assign** (nível 2 do bloco).

Associa `SUSPEITO` a uma coleção Tuple com 2 itens, na expressão `('SUSPEITO', 'Suspeito')`.

**Linha 1132 — Assign** (nível 2 do bloco).

Associa `RECUSADO` a uma coleção Tuple com 2 itens, na expressão `('RECUSADO', 'Recusado')`.

**Linha 1134 — Assign** (nível 1 do bloco).

Associa `id_validacao` a a chamada `models.BigAutoField`; argumentos nomeados: `primary_key=True`.

- `primary_key=True`: define o identificador principal do registro.

**Linha 1136 — Assign** (nível 1 do bloco).

Associa `pedido` a a chamada `models.ForeignKey`; argumentos posicionais: `PedidoSangue`; argumentos nomeados: `on_delete=models.CASCADE`, `related_name='validacoes'`, `db_column='id_pedido'`.

- `on_delete=models.CASCADE`: comportamento quando o registro relacionado é excluído.
- `related_name='validacoes'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_pedido'`: nome da coluna no banco.

**Linha 1143 — Assign** (nível 1 do bloco).

Associa `status_validacao` a a chamada `models.CharField`; argumentos nomeados: `max_length=20`, `choices=StatusValidacao.choices`.

- `max_length=20`: limite de comprimento do campo.
- `choices=StatusValidacao.choices`: alternativas declaradas para validação e apresentação.

**Linha 1148 — Assign** (nível 1 do bloco).

Associa `motivo` a a chamada `models.TextField`; argumentos nomeados: `blank=True`, `default=''`.

- `blank=True`: permite ou impede campo vazio na validação.
- `default=''`: valor inicial quando não é informado outro.

**Linha 1150 — Assign** (nível 1 do bloco).

Associa `moderador` a a chamada `models.ForeignKey`; argumentos posicionais: `settings.AUTH_USER_MODEL`; argumentos nomeados: `on_delete=models.SET_NULL`, `null=True`, `blank=True`, `related_name='validacoes_pedido_realizadas'`, `db_column='id_moderador'`.

- `on_delete=models.SET_NULL`: comportamento quando o registro relacionado é excluído.
- `null=True`: permite ou impede ausência SQL (NULL).
- `blank=True`: permite ou impede campo vazio na validação.
- `related_name='validacoes_pedido_realizadas'`: nome usado ao consultar a relação pelo lado inverso.
- `db_column='id_moderador'`: nome da coluna no banco.

**Linha 1159 — Assign** (nível 1 do bloco).

Associa `data_validacao` a a chamada `models.DateTimeField`; argumentos nomeados: `auto_now_add=True`.

- `auto_now_add=True`: preenche a data/hora na criação.

**Linha 1161 — ClassDef** (nível 1 do bloco).

Define a classe `Meta`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 1161:

**Linha 1162 — Assign** (nível 2 do bloco).

Associa `db_table` a o valor literal `'validacoes_pedido'`.

**Linha 1163 — Assign** (nível 2 do bloco).

Associa `ordering` a uma coleção List com 1 itens, na expressão `['-data_validacao']`.

**Linha 1165 — FunctionDef** (nível 1 do bloco).

Define `__str__(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 1165:

**Linha 1166 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o texto formatado `f'Pedido {self.pedido_id} - {self.get_status_validacao_display()}'`, inserindo valores nas partes entre chaves ao chamador.

### Assign — linhas 1169 a 1171

```python
ValidacaoPedido.StatusValidacao.CORRECAO = (
    ValidacaoPedido.StatusValidacao.CORRECAO_SOLICITADA
)
```

**Explicação deste trecho:**

**Linha 1169 — Assign** (nível 0 do bloco).

Associa `ValidacaoPedido.StatusValidacao.CORRECAO` a o atributo `CORRECAO_SOLICITADA` de `ValidacaoPedido.StatusValidacao`.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 32: `# Reaproveita a mesma lista de tipos sanguineos usada em compatibilidade.py,`
- Linha 33: `# para nao correr o risco de duas listas divergentes no projeto.`
- Linha 54: `# Padroniza o e-mail para evitar diferencas por letras maiusculas.`
- Linha 55: `# Exemplo: MARIA@EXAMPLE.COM e maria@example.com viram o mesmo padrao.`
- Linha 146: `# Quando um Hemocentro confirma o tipo, ele deixa de ser editável pela`
- Linha 147: `# triagem/autopreenchimento do usuário.`
- Linha 584: `# Nomes legados continuam disponíveis para código já existente, mas apontam`
- Linha 585: `# para os resultados oficiais usados pelo fluxo atual.`
- Linha 1112: `# Compatibilidade de leitura para integrações antigas. Os valores novos são`
- Linha 1113: `# os únicos gravados pelo fluxo atual.`

