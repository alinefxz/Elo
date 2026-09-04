"""
RESUMO DO ARQUIVO
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

    class StatusValidacaoHemocentro(models.TextChoices):
        """Situacao institucional do Hemocentro dentro do Elo."""

        PENDENTE = "PENDENTE", "Pendente"
        APROVADO = "APROVADO", "Aprovado"
        RECUSADO = "RECUSADO", "Recusado"
        CORRECAO = "CORRECAO", "Correcao necessaria"

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

    # Para contas de Hemocentro, este campo guarda a situacao atual analisada
    # pelo administrador. O historico completo fica em ValidacaoHemocentro.
    status_validacao = models.CharField(
        max_length=20,
        choices=StatusValidacaoHemocentro.choices,
        default=StatusValidacaoHemocentro.PENDENTE,
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
            models.Index(fields=["acao", "criado_em"], name="auditoria_acao_data_idx"),
            models.Index(
                fields=["usuario", "criado_em"],
                name="auditoria_usuario_data_idx",
            ),
            models.Index(fields=["ip", "criado_em"], name="auditoria_ip_data_idx"),
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

    # Identificador da triagem.
    id_triagem = models.BigAutoField(primary_key=True)

    # Usuário que respondeu à triagem.
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="triagens",
        db_column="id_usuario",
    )

    # Informa se é extensa ou simplificada.
    modalidade = models.CharField(
        max_length=20,
        choices=Modalidade.choices,
        default=Modalidade.EXTENSA,
    )

    # Versão das regras utilizadas no cálculo.
    regra_version = models.CharField(
        max_length=40,
        default="HEMOMINAS_2026_08",
    )

    # Resultado final calculado pelo sistema.
    resultado = models.CharField(
        max_length=30,
        choices=Resultado.choices,
    )

    # Explicação apresentada ao usuário.
    mensagem_resultado = models.TextField()

    # Data orientativa para liberação, quando existir.
    data_liberacao = models.DateField(
        null=True,
        blank=True,
    )

    # Guarda todos os achados sem apagar respostas anteriores.
    achados = models.JSONField(
        default=list,
        blank=True,
    )

    # Datas do ciclo da triagem.
    iniciada_em = models.DateTimeField(auto_now_add=True)
    finalizada_em = models.DateTimeField(
        null=True,
        blank=True,
    )

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

    # Identificador da resposta.
    id_resposta = models.BigAutoField(primary_key=True)

    # Triagem à qual a resposta pertence.
    triagem = models.ForeignKey(
        Triagem,
        on_delete=models.CASCADE,
        related_name="respostas",
        db_column="id_triagem",
    )

    # Código da pergunta, como EXT-01 ou EXT-05A.
    id_pergunta = models.CharField(max_length=20)

    # Código interno da resposta.
    codigo_resposta = models.CharField(max_length=80)

    # Texto apresentado ao usuário.
    resposta_label = models.CharField(max_length=255)

    # Data associada ao evento, quando existir.
    data_evento = models.DateField(
        db_column="event_date",
        null=True,
        blank=True,
    )

    # Informações complementares da resposta.
    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    # Versão das regras usada na resposta.
    rule_version = models.CharField(
        max_length=40,
        default="HEMOMINAS_2026_08",
    )

    # Referência da especificação utilizada.
    source_ref = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    # Momento em que a resposta foi salva.
    respondido_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "respostas_triagem"
        ordering = ["id_resposta"]
        indexes = [
            models.Index(
                fields=["triagem", "id_pergunta"],
                name="resposta_triagem_pergunta_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.triagem_id} - "
            f"{self.id_pergunta} - "
            f"{self.codigo_resposta}"
        )


class Estoque(models.Model):
    """
    UC_29 - Cadastrar Estoque.

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

    # Somente contas com perfil Hemocentro podem ter um Estoque. A
    # validacao completa (inclusive "esta aprovado?") fica em clean() e na
    # camada de servico; limit_choices_to so ajuda a limpar o admin.
    hemocentro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="estoques",
        db_column="id_hemocentro",
        limit_choices_to={"perfil": "HEMOCENTRO"},
    )

    # As opcoes vem de TIPOS_SANGUINEOS (compatibilidade.py), entao um
    # tipo invalido como "C+" nunca passa nem pela validacao do form nem
    # pela validacao do model.
    tipo_sanguineo = models.CharField(
        max_length=3,
        choices=[(tipo, tipo) for tipo in TIPOS_SANGUINEOS],
    )

    # Quantidade atual de bolsas. PositiveIntegerField ja impede valores
    # negativos no nivel do banco (CHECK constraint) e do Python.
    quantidade_bolsas = models.PositiveIntegerField(default=0)

    # A partir de qual quantidade o hemocentro considera o tipo "baixo".
    nivel_minimo = models.PositiveIntegerField()

    # A partir de qual quantidade o hemocentro considera o tipo "critico".
    # Precisa ser menor ou igual ao nivel_minimo (validado em clean()).
    nivel_critico = models.PositiveIntegerField()

    status_calculado = models.CharField(
        max_length=10,
        choices=StatusCalculado.choices,
        default=StatusCalculado.ESTAVEL,
    )

    # auto_now grava a data automaticamente a cada save(), inclusive nas
    # atualizacoes feitas pelas movimentacoes de estoque.
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "estoques"
        verbose_name = "estoque"
        verbose_name_plural = "estoques"
        ordering = ["hemocentro__nome", "tipo_sanguineo"]
        constraints = [
            # Impede dois registros de estoque para o mesmo tipo sanguineo
            # no mesmo hemocentro, mesmo se dois cadastros chegarem quase
            # ao mesmo tempo (a regra tambem existe no PostgreSQL).
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
    UC_30 - Atualizar Estoque.

    Historico imutavel de cada entrada, saida ou ajuste feito em um
    Estoque. Uma linha nunca e alterada ou apagada depois de criada: para
    corrigir um valor, registra-se uma nova movimentacao (do tipo AJUSTE).
    Isso preserva o rastro completo exigido pela regra "toda alteracao
    deve gerar historico com responsavel".
    """

    class TipoMovimento(models.TextChoices):
        # Entrada de bolsas (doacao recebida, transferencia recebida etc).
        ENTRADA = "ENTRADA", "Entrada"
        # Saida de bolsas (transfusao, transferencia enviada, descarte).
        SAIDA = "SAIDA", "Saída"
        # Correcao direta da quantidade (ex.: apos uma contagem fisica).
        AJUSTE = "AJUSTE", "Ajuste"

    id_mov = models.BigAutoField(primary_key=True)

    estoque = models.ForeignKey(
        Estoque,
        on_delete=models.CASCADE,
        related_name="movimentacoes",
        db_column="id_estoque",
    )

    # SET_NULL preserva a movimentacao mesmo se a conta do responsavel for
    # removida futuramente; o historico de quantidades continua correto.
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

    # Quantidade de bolsas antes da movimentacao (copia da foto do
    # Estoque no momento em que a movimentacao foi registrada).
    quantidade_anterior = models.PositiveIntegerField()

    # Para ENTRADA/SAIDA: quantidade informada pelo usuario (sempre >= 1).
    # Para AJUSTE: diferenca entre quantidade_nova e quantidade_anterior,
    # podendo ser negativa quando o ajuste reduz o estoque.
    quantidade_movimentada = models.IntegerField()

    # Quantidade de bolsas depois da movimentacao. Sempre
    # quantidade_anterior +/- quantidade_movimentada, calculado pela
    # camada de servico, nunca digitado pelo usuario.
    quantidade_nova = models.PositiveIntegerField()

    motivo = models.CharField(max_length=255, blank=True, default="")

    # auto_now_add preenche uma unica vez, no momento da criacao. Como a
    # linha e imutavel, esta data representa o momento real do evento.
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