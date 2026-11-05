"""Apresentação e histórico privado, construídos somente com registros reais."""

from heapq import merge
from itertools import islice

from django.urls import reverse
from django.utils.functional import cached_property

from .models import AuditoriaAcaoCritica, EstoqueMovimentacao, Triagem, Usuario
from .permissoes import acessos_usuario


PERFIS = {
    Usuario.Perfil.OBSERVADOR: ("Usuário comum", "Meu perfil", "Seus dados, suas solicitações e as atividades da sua conta."),
    Usuario.Perfil.DOADOR: ("Doador", "Perfil do doador", "Cuide dos seus dados e acompanhe sua jornada de doação."),
    Usuario.Perfil.RECEPTOR: ("Receptor", "Perfil do receptor", "Acompanhe suas solicitações e as atualizações dos hemocentros."),
    Usuario.Perfil.HEMOCENTRO: ("Hemocentro", "Perfil institucional", "As informações da instituição e suas operações autorizadas no Elo."),
    Usuario.Perfil.ADMINISTRADOR: ("Administrador", "Perfil administrativo", "Sua conta e suas atividades administrativas em um só lugar."),
}


def apresentar_perfil(usuario):
    rotulo, titulo, descricao = PERFIS.get(usuario.perfil, PERFIS[Usuario.Perfil.OBSERVADOR])
    return {
        "rotulo": rotulo, "titulo": titulo, "descricao": descricao,
        "comum": usuario.perfil == Usuario.Perfil.OBSERVADOR,
        "doador": usuario.perfil == Usuario.Perfil.DOADOR,
        "receptor": usuario.perfil == Usuario.Perfil.RECEPTOR,
        "institucional": usuario.perfil == Usuario.Perfil.HEMOCENTRO,
        "administrador": usuario.perfil == Usuario.Perfil.ADMINISTRADOR,
    }


def acoes_usuario(usuario):
    acessos = acessos_usuario(usuario)
    opcoes = [
        ("responder_triagem", "Minhas triagens", "Inicie uma modalidade ou retome seu progresso.", "accounts:triagem_apresentacao"),
        ("solicitar_pedido", "Minhas solicitações", "Consulte o andamento e os retornos do hemocentro.", "accounts:minhas_solicitacoes"),
        ("gerenciar_estoque", "Gerenciar estoque", "Cadastre e atualize o estoque da instituição.", "accounts:estoque_hemocentro"),
        ("analisar_pedidos", "Analisar solicitações", "Gerencie os pedidos destinados a esta instituição.", "accounts:painel_pedidos_hemocentro"),
        ("validar_hemocentros", "Validar hemocentros", "Analise os cadastros institucionais.", "accounts:painel_aprovacao_hemocentros"),
        ("moderar_pedidos", "Moderar pedidos", "Acompanhe solicitações que precisam de moderação.", "accounts:painel_validacao_pedidos"),
        ("gerenciar_usuarios", "Gerenciar usuários", "Abra a administração de contas conforme suas permissões.", "admin:accounts_usuario_changelist"),
        ("consultar_auditoria", "Atividades do sistema", "Consulte os registros de auditoria autorizados.", "admin:accounts_auditoriaacaocritica_changelist"),
        ("painel_django", "Painel administrativo", "Acesse as ferramentas de gerenciamento autorizadas.", "admin:index"),
    ]
    return [
        {"titulo": titulo, "descricao": descricao, "url": reverse(rota)}
        for capacidade, titulo, descricao, rota in opcoes if acessos[capacidade]
    ]


class HistoricoUsuario:
    """Combina fontes privadas com paginação sem carregar todo o histórico."""

    def __init__(self, usuario):
        self.fontes = []
        acessos = acessos_usuario(usuario)
        if acessos["responder_triagem"]:
            self.fontes.append((usuario.triagens.order_by("-iniciada_em", "-pk"), "iniciada_em", self._triagem))
        if acessos["solicitar_pedido"]:
            self.fontes.append((usuario.pedidos_sangue.select_related("hemocentro_destino").order_by("-data_criacao", "-pk"), "data_criacao", self._solicitacao))
        if usuario.perfil == Usuario.Perfil.HEMOCENTRO:
            self.fontes.append((usuario.validacoes_hemocentro.order_by("-data_analise", "-pk"), "data_analise", self._instituicao))
            if acessos["analisar_pedidos"]:
                self.fontes.append((usuario.pedidos_recebidos.order_by("-data_criacao", "-pk"), "data_criacao", self._pedido_institucional))
                self.fontes.append((EstoqueMovimentacao.objects.filter(estoque__hemocentro=usuario).select_related("estoque").order_by("-data_hora", "-pk"), "data_hora", self._estoque))
        if acessos["validar_hemocentros"]:
            self.fontes.append((usuario.auditorias_acoes_criticas.exclude(acao=AuditoriaAcaoCritica.Acao.ACESSO_DADOS_SENSIVEIS).order_by("-criado_em", "-pk"), "criado_em", self._auditoria))

    @cached_property
    def total(self):
        return sum(consulta.count() for consulta, _, _ in self.fontes)

    def count(self):
        return self.total

    def __len__(self):
        return self.total

    def __getitem__(self, fatia):
        inicio, fim = fatia.start or 0, fatia.stop
        fluxos = [map(apresentar, consulta[:fim]) for consulta, _, apresentar in self.fontes]
        return list(islice(merge(*fluxos, key=lambda item: item["data"], reverse=True), inicio, fim))

    @staticmethod
    def _triagem(item):
        rota = "accounts:triagem_resultado" if item.status == Triagem.Status.CONCLUIDA else "accounts:triagem_pergunta"
        return {"titulo": f"Triagem {item.get_modalidade_display()}", "descricao": "Registro orientativo de triagem para doação.", "status": item.get_status_display(), "data": item.iniciada_em, "url": reverse(rota, args=[item.pk])}

    @staticmethod
    def _solicitacao(item):
        return {"titulo": item.titulo, "descricao": item.hemocentro_destino.nome, "status": item.get_status_display(), "data": item.data_criacao, "url": reverse("accounts:minhas_solicitacoes")}

    @staticmethod
    def _instituicao(item):
        return {"titulo": "Validação institucional", "descricao": item.parecer, "status": item.get_status_display(), "data": item.data_analise, "url": ""}

    @staticmethod
    def _pedido_institucional(item):
        return {"titulo": item.titulo, "descricao": "Solicitação destinada à instituição.", "status": item.get_status_display(), "data": item.data_criacao, "url": reverse("accounts:painel_pedidos_hemocentro")}

    @staticmethod
    def _estoque(item):
        return {"titulo": f"{item.get_tipo_movimento_display()} de estoque · {item.estoque.tipo_sanguineo}", "descricao": f"Quantidade registrada: {item.quantidade_anterior} → {item.quantidade_nova} bolsas.", "status": "Registrada", "data": item.data_hora, "url": reverse("accounts:estoque_hemocentro")}

    @staticmethod
    def _auditoria(item):
        return {"titulo": item.get_acao_display(), "descricao": "Atividade registrada pela sua conta administrativa.", "status": item.get_resultado_display(), "data": item.criado_em, "url": ""}


def resumo_usuario(usuario):
    if usuario.perfil == Usuario.Perfil.HEMOCENTRO:
        return [
            {"rotulo": "Validação", "valor": usuario.get_status_validacao_display()},
            {"rotulo": "Solicitações recebidas", "valor": usuario.pedidos_recebidos.count()},
            {"rotulo": "Tipos em estoque", "valor": usuario.estoques.count()},
        ]
    if usuario.perfil == Usuario.Perfil.ADMINISTRADOR:
        return [
            {"rotulo": "Validações realizadas", "valor": usuario.validacoes_hemocentro_realizadas.count()},
            {"rotulo": "Moderações realizadas", "valor": usuario.validacoes_pedido_realizadas.count()},
        ]
    resumo = [{"rotulo": "Solicitações enviadas", "valor": usuario.pedidos_sangue.count()}]
    if acessos_usuario(usuario)["responder_triagem"]:
        resumo.insert(0, {"rotulo": "Triagens realizadas", "valor": usuario.triagens.count()})
    return resumo
