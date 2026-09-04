# Triagem completa do Elo - Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar as triagens extensa e simplificada completas, com perguntas versionadas, regras orientativas, salvamento de andamento, resultado e histórico privado no perfil.

**Architecture:** Os questionários serão catálogos Python imutáveis e versionados. Um motor puro avaliará respostas estruturadas sem acessar o banco; um serviço transacional cuidará de andamento, ramificações, conclusão e vínculo com a triagem extensa-base; views pequenas renderizarão uma pergunta por página e páginas privadas de resultado e histórico.

**Tech Stack:** Python 3.14, Django 6.1, PostgreSQL em produção, SQLite em memória para testes locais, templates Django sem CSS.

**Spec:** `docs/superpowers/specs/2026-09-04-triagem-completa-design.md`

## Global Constraints

- A regra inicial é `HEMOMINAS_2026_08`, consolidada em 28/08/2026.
- A interface nunca declara aptidão clínica; usa somente os estados orientativos definidos no model `Triagem`.
- A decisão final pertence sempre à equipe do hemocentro.
- As 55 entradas extensas (`EXT-01` a `EXT-51`, incluindo `EXT-05A`, `EXT-05B`, `EXT-07A` e `EXT-11A`) e as 18 simplificadas (`SIM-01` a `SIM-18`) devem existir.
- A triagem simplificada somente pode começar depois de uma extensa concluída pelo mesmo usuário.
- Visitante visualiza a apresentação; Doador e Receptor respondem; Observador e Hemocentro não respondem; Administrador consulta no admin em modo somente leitura.
- Histórico, resultado e respostas são sempre filtrados pelo proprietário fora do admin.
- Não adicionar CSS.
- Todo código novo ou alterado recebe comentários didáticos, objetivos e verdadeiros.
- Não editar migrations já aplicadas; criar uma nova migration depois de alterar os models.
- Preservar alterações locais existentes e remover apenas a implementação inicial de triagem que for substituída pela nova solução.

---

## Mapa de arquivos

- `config/settings_test.py`: banco SQLite isolado para executar testes sem exigir `CREATEDB` no PostgreSQL local.
- `accounts/models.py`: ciclo de vida da triagem, fluxo persistido, referência da extensa-base e resposta estruturada.
- `accounts/migrations/0007_*.py`: campos novos, conversão segura dos dados de `0006` e restrição de unicidade.
- `accounts/triagem_catalogo.py`: tipos compartilhados, validação e busca de perguntas.
- `accounts/triagem_catalogo_extensa.py`: 55 entradas extensas, alternativas, condições de exibição, fontes e regras declarativas.
- `accounts/triagem_catalogo_simplificada.py`: 18 entradas rápidas e mapas para blocos extensos.
- `accounts/triagem_motor.py`: avaliação pura, prioridade, cálculo de prazos e mensagens.
- `accounts/triagem_forms.py`: formulário dinâmico de uma pergunta.
- `accounts/triagem_servico.py`: criação, retomada, navegação, respostas, conclusão e base da simplificada.
- `accounts/views.py`: apresentação, início, pergunta, histórico e resultado.
- `accounts/urls.py`: rotas únicas e sem duplicação.
- `accounts/admin.py`: novos campos somente leitura e aviso de sensibilidade.
- `templates/accounts/triagem_apresentacao.html`: texto integral aprovado e escolha das duas modalidades.
- `templates/accounts/triagem_pergunta.html`: uma pergunta por página.
- `templates/accounts/triagem_resultado.html`: resultado orientativo e achados.
- `templates/accounts/triagem_historico.html`: histórico do usuário.
- `templates/accounts/dashboard.html`: resumo não sensível da última triagem.
- `templates/accounts/inicio.html`: apontamento público para a apresentação.
- `accounts/test_triagem_models.py`: persistência e migration.
- `accounts/test_triagem_catalogos.py`: completude dos catálogos.
- `accounts/test_triagem_motor.py`: regras, exceções, prioridade e datas-limite.
- `accounts/test_triagem_forms.py`: validação de entradas.
- `accounts/test_triagem_servico.py`: estado, ramificações, retomada e simplificada.
- `accounts/test_triagem_views.py`: acesso, conteúdo, privacidade e navegação.
- `accounts/test_triagem.py`: adaptar os testes iniciais às interfaces novas, preservando o arquivo.

---

### Task 1: Infraestrutura de teste e ciclo de vida persistente

**Files:**
- Create: `config/settings_test.py`
- Modify: `accounts/models.py`
- Create: `accounts/test_triagem_models.py`
- Create: `accounts/migrations/0007_*.py`

**Interfaces:**
- Consumes: `accounts.models.Usuario`, `Triagem` e `RespostaTriagem` existentes na migration `0006`.
- Produces: `Triagem.Status`, `Triagem.status`, `pergunta_atual`, `fluxo_perguntas`, `triagem_base`, `atualizada_em`, `RespostaTriagem.valor` e unicidade `(triagem, id_pergunta)`.

- [ ] **Step 1: Criar configuração isolada de testes**

```python
# config/settings_test.py
from .settings import *  # noqa: F403

# Os testes não dependem da permissão CREATEDB do PostgreSQL local.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
```

- [ ] **Step 2: Escrever testes que descrevem os novos campos e a unicidade**

```python
class TriagemModelTests(TestCase):
    def test_nova_triagem_comeca_em_andamento(self):
        triagem = Triagem.objects.create(
            usuario=self.usuario,
            modalidade=Triagem.Modalidade.EXTENSA,
        )
        self.assertEqual(triagem.status, Triagem.Status.EM_ANDAMENTO)
        self.assertEqual(triagem.fluxo_perguntas, [])
        self.assertEqual(triagem.resultado, "")

    def test_uma_pergunta_tem_uma_unica_resposta_por_triagem(self):
        RespostaTriagem.objects.create(
            triagem=self.triagem,
            id_pergunta="EXT-01",
            codigo_resposta="SIM",
            resposta_label="Sim",
            valor={"codigos": ["SIM"]},
        )
        with self.assertRaises(IntegrityError):
            RespostaTriagem.objects.create(
                triagem=self.triagem,
                id_pergunta="EXT-01",
                codigo_resposta="NAO",
                resposta_label="Não",
                valor={"codigos": ["NAO"]},
            )
```

- [ ] **Step 3: Executar os testes e confirmar a falha pelos campos ausentes**

Run: `py manage.py test accounts.test_triagem_models --settings=config.settings_test -v 2`

Expected: FAIL porque `Triagem.Status`, `status`, `fluxo_perguntas` e `valor` ainda não existem.

- [ ] **Step 4: Adicionar os campos aos models**

```python
class Status(models.TextChoices):
    EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
    CONCLUIDA = "CONCLUIDA", "Concluída"
    CANCELADA = "CANCELADA", "Cancelada"

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
atualizada_em = models.DateTimeField(auto_now=True)
```

Alterar `resultado` para `blank=True, default=""`, `mensagem_resultado` para `blank=True, default=""` e adicionar em `RespostaTriagem`:

```python
# Mantém seleção, data e complemento juntos sem perder os campos legados.
valor = models.JSONField(default=dict, blank=True)

constraints = [
    models.UniqueConstraint(
        fields=["triagem", "id_pergunta"],
        name="resposta_unica_por_pergunta",
    )
]
```

- [ ] **Step 5: Gerar a migration e acrescentar conversão dos registros antigos**

Run: `py manage.py makemigrations accounts`

Adicionar uma `RunPython` antes da restrição única. A função direta define `CONCLUIDA` quando `finalizada_em` existe e monta `valor` com `codigo_resposta`, `data_evento` e `metadata`; a reversa preserva os campos antigos e somente limpa os campos novos.

- [ ] **Step 6: Executar testes do model e verificar a migration**

Run: `py manage.py test accounts.test_triagem_models --settings=config.settings_test -v 2`

Expected: PASS.

Run: `py manage.py makemigrations --check --settings=config.settings_test`

Expected: `No changes detected`.

- [ ] **Step 7: Registrar a etapa**

```bash
git add config/settings_test.py accounts/models.py accounts/migrations/0007_*.py accounts/test_triagem_models.py
git commit -m "feat: add triage lifecycle persistence"
```

---

### Task 2: Catálogos completos e validados

**Files:**
- Create: `accounts/triagem_catalogo.py`
- Create: `accounts/triagem_catalogo_extensa.py`
- Create: `accounts/triagem_catalogo_simplificada.py`
- Create: `accounts/test_triagem_catalogos.py`

**Interfaces:**
- Consumes: códigos de resultado de `Triagem.Resultado` e a versão `HEMOMINAS_2026_08`.
- Produces: `PERGUNTAS_EXTENSAS`, `PERGUNTAS_SIMPLIFICADAS`, `obter_catalogo(modalidade)`, `obter_pergunta(id_pergunta)` e `validar_catalogos()`.

- [ ] **Step 1: Escrever testes de completude**

```python
IDS_EXTENSOS = {
    "EXT-01", "EXT-02", "EXT-03", "EXT-04", "EXT-05", "EXT-05A",
    "EXT-05B", "EXT-06", "EXT-07", "EXT-07A", "EXT-08", "EXT-09",
    "EXT-10", "EXT-11", "EXT-11A", "EXT-12", "EXT-13", "EXT-14",
    "EXT-15", "EXT-16", "EXT-17", "EXT-18", "EXT-19", "EXT-20",
    "EXT-21", "EXT-22", "EXT-23", "EXT-24", "EXT-25", "EXT-26",
    "EXT-27", "EXT-28", "EXT-29", "EXT-30", "EXT-31", "EXT-32",
    "EXT-33", "EXT-34", "EXT-35", "EXT-36", "EXT-37", "EXT-38",
    "EXT-39", "EXT-40", "EXT-41", "EXT-42", "EXT-43", "EXT-44",
    "EXT-45", "EXT-46", "EXT-47", "EXT-48", "EXT-49", "EXT-50",
    "EXT-51",
}

IDS_SIMPLIFICADOS = {f"SIM-{numero:02d}" for numero in range(1, 19)}

def test_catalogos_possuem_todos_os_identificadores(self):
    self.assertEqual(set(PERGUNTAS_EXTENSAS), IDS_EXTENSOS)
    self.assertEqual(set(PERGUNTAS_SIMPLIFICADAS), IDS_SIMPLIFICADOS)

def test_toda_pergunta_tem_texto_opcoes_fonte_e_versao(self):
    for pergunta in [*PERGUNTAS_EXTENSAS.values(), *PERGUNTAS_SIMPLIFICADAS.values()]:
        self.assertTrue(pergunta["texto"])
        self.assertTrue(pergunta["opcoes"] or pergunta["tipo"] in {"data", "numero", "texto"})
        self.assertTrue(pergunta["fonte"])
        self.assertEqual(pergunta["regra_version"], "HEMOMINAS_2026_08")
```

- [ ] **Step 2: Executar e confirmar a falha por módulos ausentes**

Run: `py manage.py test accounts.test_triagem_catalogos --settings=config.settings_test -v 2`

Expected: ERROR de importação de `accounts.triagem_catalogo`.

- [ ] **Step 3: Criar o contrato comum do catálogo**

Cada pergunta terá as chaves `id`, `titulo`, `texto`, `explicacao`, `tipo`, `opcoes`, `multipla`, `permite_data`, `exige_data_para`, `mostrar_se`, `abrir_extensa`, `regras`, `fonte` e `regra_version`. Cada opção terá `codigo` e `rotulo`; regras simples terão `resultado`, `mensagem`, `prazo` e `data_referencia`.

```python
TRIAGEM_RULE_VERSION = "HEMOMINAS_2026_08"

def obter_catalogo(modalidade):
    if modalidade == "EXTENSA":
        return PERGUNTAS_EXTENSAS
    if modalidade == "SIMPLIFICADA":
        return PERGUNTAS_SIMPLIFICADAS
    raise ValueError("Modalidade de triagem inválida.")

def obter_pergunta(id_pergunta):
    pergunta = PERGUNTAS_EXTENSAS.get(id_pergunta)
    if pergunta is None:
        pergunta = PERGUNTAS_SIMPLIFICADAS.get(id_pergunta)
    if pergunta is None:
        raise KeyError(f"Pergunta inexistente: {id_pergunta}")
    return pergunta
```

- [ ] **Step 4: Preencher o catálogo extenso**

Transcrever as 55 entradas do PDF sem abreviar alternativas. Declarar ramificações de `EXT-05A/05B`, `EXT-06`, `EXT-07`, `EXT-12` a `EXT-18` e `EXT-42` por `mostrar_se`. Perguntas sobre doenças, infecções, medicamentos, vacinas, viagens e exposições devem conter a alternativa explícita de dúvida ou resposta presencial prevista na fonte.

Exemplo integral do formato usado por todas as entradas:

```python
"EXT-01": {
    "id": "EXT-01",
    "titulo": "Consentimento e entendimento",
    "texto": (
        "Você entende que esta pré-triagem é apenas uma orientação e que "
        "a decisão final será feita pela equipe do hemocentro?"
    ),
    "explicacao": (
        "Antes de qualquer pergunta de saúde, você precisa compreender "
        "o limite desta ferramenta."
    ),
    "tipo": "escolha",
    "opcoes": [
        {"codigo": "SIM", "rotulo": "Sim, entendo e quero continuar."},
        {"codigo": "NAO", "rotulo": "Não entendo / quero ler a explicação novamente."},
    ],
    "multipla": False,
    "permite_data": False,
    "exige_data_para": [],
    "mostrar_se": None,
    "abrir_extensa": {},
    "regras": {
        "NAO": {
            "resultado": "AVALIACAO_PRESENCIAL",
            "mensagem": "Leia novamente a explicação antes de continuar.",
        }
    },
    "fonte": "PDF, EXT-01; Manual Elo, seções 1, 2 e 18",
    "regra_version": "HEMOMINAS_2026_08",
},
```

- [ ] **Step 5: Preencher o catálogo simplificado**

Transcrever `SIM-01` a `SIM-18` e declarar os blocos detalhados exatos: `SIM-02 -> EXT-02/03/05A/05B/07`, `SIM-03 -> EXT-08/12/13/14`, `SIM-04 -> EXT-09/10/44`, `SIM-05 -> EXT-33`, `SIM-06 -> blocos de doença/EXT-27/46`, `SIM-07 -> EXT-41/42`, `SIM-08 -> EXT-46/47`, `SIM-09 -> EXT-48`, `SIM-10 -> EXT-21/22/23/24`, `SIM-11 -> EXT-25/26/27`, `SIM-12 -> EXT-15/16`, `SIM-13 -> EXT-43`, `SIM-14 -> EXT-45`, `SIM-15 -> EXT-49`, `SIM-16 -> EXT-03/11/18/50`, `SIM-17 -> nova extensa completa`, `SIM-18 -> concluir ou iniciar extensa`.

- [ ] **Step 6: Executar testes e a validação do catálogo**

Run: `py manage.py test accounts.test_triagem_catalogos --settings=config.settings_test -v 2`

Expected: PASS, incluindo códigos de opção únicos e todos os destinos de `abrir_extensa` existentes no catálogo extenso.

- [ ] **Step 7: Registrar a etapa**

```bash
git add accounts/triagem_catalogo.py accounts/triagem_catalogo_extensa.py accounts/triagem_catalogo_simplificada.py accounts/test_triagem_catalogos.py
git commit -m "feat: add complete triage question catalogs"
```

---

### Task 3: Motor completo de regras orientativas

**Files:**
- Create: `accounts/triagem_motor.py`
- Create: `accounts/test_triagem_motor.py`
- Modify: `accounts/triagem.py` para manter somente importações de compatibilidade documentadas para o novo catálogo e motor.

**Interfaces:**
- Consumes: `obter_catalogo()`, respostas no formato `{id_pergunta: {"codigos": list[str], "data_evento": str | None, "detalhes": str}}` e respostas-base opcionais.
- Produces: `avaliar_triagem(modalidade, respostas, hoje=None, respostas_base=None) -> dict`, `escolher_resultado(achados) -> str` e `calcular_data_referencia(data_evento, prazo, hoje) -> date | None`.

- [ ] **Step 1: Escrever testes da prioridade e maior prazo**

```python
def test_resultado_respeita_prioridade_e_preserva_todos_os_achados(self):
    resultado = avaliar_triagem(
        "EXTENSA",
        {
            "EXT-03": {"codigos": ["MENOS_50"]},
            "EXT-20": {"codigos": ["ANEMIA_FALCIFORME"]},
            "EXT-46": {"codigos": ["NAO_SEI"]},
        },
        hoje=date(2026, 8, 28),
    )
    self.assertEqual(resultado["resultado"], Triagem.Resultado.DEFINITIVA)
    self.assertEqual(len(resultado["achados"]), 3)

def test_maior_data_temporaria_e_a_data_principal(self):
    resultado = avaliar_triagem(
        "EXTENSA",
        {
            "EXT-44": {"codigos": ["ALCOOL_12H"], "data_evento": "2026-08-28"},
            "EXT-48": {"codigos": ["VACINA_30_DIAS"], "data_evento": "2026-08-20"},
        },
        hoje=date(2026, 8, 28),
    )
    self.assertEqual(resultado["data_liberacao"], date(2026, 9, 19))
```

- [ ] **Step 2: Executar e confirmar a falha pelo motor ausente**

Run: `py manage.py test accounts.test_triagem_motor --settings=config.settings_test -v 2`

Expected: ERROR de importação de `accounts.triagem_motor`.

- [ ] **Step 3: Implementar achados declarativos e prioridade**

```python
PRIORIDADE_RESULTADOS = (
    Triagem.Resultado.DEFINITIVA,
    Triagem.Resultado.AVALIACAO,
    Triagem.Resultado.TEMPORARIA,
    Triagem.Resultado.DOCUMENTACAO,
)

def escolher_resultado(achados):
    encontrados = {achado["resultado"] for achado in achados}
    for resultado in PRIORIDADE_RESULTADOS:
        if resultado in encontrados:
            return resultado
    return Triagem.Resultado.SEM_IMPEDIMENTO
```

O avaliador genérico percorre todos os códigos respondidos, cria um achado por regra e nunca interrompe o laço no primeiro impedimento.

- [ ] **Step 4: Escrever a matriz de testes das regras simples**

Construir casos nomeados para cada opção que tenha `regras` no catálogo. O teste compara `id_pergunta`, `codigo_regra`, `resultado`, `exige_relatorio`, `fonte` e `regra_version`, garantindo que uma alternativa configurada não fique sem efeito.

```python
def test_toda_regra_declarada_gera_achado_com_rastreabilidade(self):
    for pergunta in todas_as_perguntas():
        for codigo, regra in pergunta["regras"].items():
            resultado = avaliar_triagem(
                "EXTENSA" if pergunta["id"].startswith("EXT") else "SIMPLIFICADA",
                {pergunta["id"]: {"codigos": [codigo]}},
                hoje=date(2026, 8, 28),
            )
            achado = next(
                item for item in resultado["achados"]
                if item["id_pergunta"] == pergunta["id"]
            )
            self.assertEqual(achado["resultado"], regra["resultado"])
            self.assertEqual(achado["regra_version"], "HEMOMINAS_2026_08")
            self.assertTrue(achado["fonte"])
```

- [ ] **Step 5: Implementar prazos e datas de referência**

Aceitar `horas`, `dias`, `semanas`, `meses` e `anos`. Somar meses e anos por calendário, reduzindo o dia somente quando ele não existir no mês final. Regras que dependem de cura, alta, retirada ou fim do tratamento, sem `data_evento`, geram `AVALIACAO_PRESENCIAL` e não inventam data.

- [ ] **Step 6: Escrever testes das regras especiais**

Cobrir limites exatos de 48h, 72h, 7 dias, 30 dias, 6 meses, 12 meses, 1 ano, 3 anos e 5 anos; intervalos por sexo; faixa 61-69; contagem de doações sem datas; parto vaginal, cesárea, aborto e amamentação; hepatites; malária; vacinas; PrEP/PEP; GLP-1; anticoagulantes; procedimentos invasivos; exposição sexual/sangue; drogas; e exceções de esplenectomia por trauma, PTI infantil, hepatite A, cânceres excepcionados e WPW após ablação.

- [ ] **Step 7: Implementar avaliadores especiais e combinação com a extensa-base**

Criar um mapa explícito de handlers somente para regras que não cabem na declaração simples:

```python
AVALIADORES_ESPECIAIS = {
    "EXT-02": avaliar_idade,
    "EXT-04": avaliar_regra_por_sexo,
    "EXT-05A": avaliar_intervalo_ultima_doacao,
    "EXT-05B": avaliar_limite_anual,
    "EXT-07": avaliar_doador_acima_60,
    "EXT-19": avaliar_hemoglobina,
    "EXT-20": avaliar_doencas_hematologicas,
    "EXT-27": avaliar_cirurgias,
    "EXT-28": avaliar_cancer,
    "EXT-33": avaliar_gestacao,
    "EXT-35": avaliar_coracao,
    "EXT-41": avaliar_infeccoes,
    "EXT-42": avaliar_hepatites,
    "EXT-46": avaliar_medicamentos,
    "EXT-47": avaliar_medicamentos_prolongados,
    "EXT-48": avaliar_vacinas,
    "EXT-49": avaliar_viagens,
}
```

Na simplificada, mesclar respostas estáveis da extensa-base com respostas `EXT-*` coletadas nesta execução; nunca reutilizar sono, alimentação, hidratação, sinais vitais ou saúde atual.

- [ ] **Step 8: Executar todos os testes do motor**

Run: `py manage.py test accounts.test_triagem_motor --settings=config.settings_test -v 2`

Expected: PASS.

- [ ] **Step 9: Registrar a etapa**

```bash
git add accounts/triagem_motor.py accounts/test_triagem_motor.py accounts/triagem.py
git commit -m "feat: evaluate complete triage rules"
```

---

### Task 4: Formulário dinâmico de uma pergunta

**Files:**
- Create: `accounts/triagem_forms.py`
- Create: `accounts/test_triagem_forms.py`
- Modify: `accounts/forms.py`

**Interfaces:**
- Consumes: dicionário de pergunta retornado por `obter_pergunta()`.
- Produces: `FormularioPergunta(pergunta, *args, **kwargs)` com `cleaned_data["valor"]` estruturado.

- [ ] **Step 1: Escrever testes de escolha, múltipla, data e complemento**

```python
def test_formulario_normaliza_resposta(self):
    pergunta = obter_pergunta("EXT-05A")
    form = FormularioPergunta(
        pergunta,
        data={"resposta": "DATA", "data_evento": "2026-08-01"},
    )
    self.assertTrue(form.is_valid())
    self.assertEqual(
        form.cleaned_data["valor"],
        {"codigos": ["DATA"], "data_evento": "2026-08-01", "detalhes": ""},
    )

def test_formulario_rejeita_data_futura(self):
    pergunta = obter_pergunta("EXT-05A")
    form = FormularioPergunta(
        pergunta,
        data={"resposta": "DATA", "data_evento": "2999-01-01"},
    )
    self.assertFalse(form.is_valid())
```

- [ ] **Step 2: Executar e confirmar a falha pela classe ausente**

Run: `py manage.py test accounts.test_triagem_forms --settings=config.settings_test -v 2`

Expected: ERROR de importação de `FormularioPergunta`.

- [ ] **Step 3: Implementar campos e normalização**

Usar `ChoiceField`/`MultipleChoiceField`, `DateField` e `CharField` conforme o catálogo. A validação deve exigir data somente para códigos listados em `exige_data_para`, limitar complemento a 500 caracteres e rejeitar códigos que não pertencem à pergunta.

- [ ] **Step 4: Remover o formulário inicial substituído**

Remover somente `TriagemExtensaForm` de `accounts/forms.py`; manter formulários de cadastro e login intactos.

- [ ] **Step 5: Executar os testes**

Run: `py manage.py test accounts.test_triagem_forms --settings=config.settings_test -v 2`

Expected: PASS.

- [ ] **Step 6: Registrar a etapa**

```bash
git add accounts/triagem_forms.py accounts/test_triagem_forms.py accounts/forms.py
git commit -m "feat: add dynamic triage question form"
```

---

### Task 5: Serviço transacional, ramificações e retomada

**Files:**
- Create: `accounts/triagem_servico.py`
- Create: `accounts/test_triagem_servico.py`

**Interfaces:**
- Consumes: catálogos, `avaliar_triagem()`, `Triagem`, `RespostaTriagem`, `ConsentimentoLGPD`.
- Produces: `pode_responder(usuario)`, `obter_extensa_base(usuario)`, `iniciar_triagem(usuario, modalidade, ip)`, `obter_pergunta_atual(triagem)`, `salvar_resposta(triagem, id_pergunta, valor)`, `voltar_pergunta(triagem)`, `concluir_triagem(triagem, hoje=None)`.

- [ ] **Step 1: Escrever testes de acesso e início**

```python
def test_simplificada_exige_extensa_concluida_do_mesmo_usuario(self):
    with self.assertRaises(TriagemSimplificadaIndisponivel):
        iniciar_triagem(
            self.usuario,
            Triagem.Modalidade.SIMPLIFICADA,
            ip="127.0.0.1",
        )

def test_inicio_extenso_cria_fluxo_e_consentimento(self):
    triagem = iniciar_triagem(
        self.usuario,
        Triagem.Modalidade.EXTENSA,
        ip="127.0.0.1",
    )
    self.assertEqual(triagem.fluxo_perguntas[0], "EXT-01")
    self.assertEqual(triagem.status, Triagem.Status.EM_ANDAMENTO)
    self.assertTrue(ConsentimentoLGPD.objects.filter(
        usuario=self.usuario,
        tipo_termo=ConsentimentoLGPD.TipoTermo.TRIAGEM,
        aceito=True,
    ).exists())
```

- [ ] **Step 2: Executar e confirmar a falha pelo serviço ausente**

Run: `py manage.py test accounts.test_triagem_servico --settings=config.settings_test -v 2`

Expected: ERROR de importação de `accounts.triagem_servico`.

- [ ] **Step 3: Implementar início, base e consentimento**

O início extenso usa a ordem do catálogo. O início simplificado seleciona a extensa concluída mais recente do mesmo usuário, salva `triagem_base` e usa a ordem `SIM-01` a `SIM-18`. Doador e Receptor são aceitos; outros perfis geram `PermissionDenied`.

- [ ] **Step 4: Escrever testes de salvar, substituir, avançar e voltar**

```python
def test_corrigir_resposta_substitui_sem_duplicar(self):
    salvar_resposta(self.triagem, "EXT-01", {"codigos": ["SIM"]})
    voltar_pergunta(self.triagem)
    salvar_resposta(self.triagem, "EXT-01", {"codigos": ["NAO"]})
    self.assertEqual(self.triagem.respostas.count(), 1)
    self.assertEqual(self.triagem.respostas.get().codigo_resposta, "NAO")
```

- [ ] **Step 5: Implementar navegação e campos legados**

Usar `update_or_create` com `defaults` contendo `codigo_resposta`, `resposta_label`, `data_evento`, `metadata`, `valor`, `rule_version` e `source_ref`. `codigo_resposta` recebe o primeiro código, `resposta_label` reúne os rótulos selecionados, `data_evento` recebe a data estruturada e `valor` preserva todos os dados.

- [ ] **Step 6: Escrever testes das ramificações**

Verificar que `EXT-05A/05B` só aparecem após `EXT-05=SIM`; `EXT-06` só para 16-17; `EXT-07` só para 61-69; blocos de sintomas são mantidos quando `EXT-08` indica problema; e uma resposta positiva da simplificada insere os IDs `EXT-*` imediatamente antes de `SIM-17` sem duplicá-los.

- [ ] **Step 7: Implementar ramificações e conclusão imutável**

Recalcular o fluxo depois de cada resposta a partir do catálogo e das condições já respondidas. `concluir_triagem()` exige `EXT-51=CONFIRMAR` ou `SIM-18=ENTENDO`, chama o motor dentro de `transaction.atomic()`, salva todos os achados, resultado, data e `finalizada_em`, e muda o status para `CONCLUIDA`. Qualquer tentativa posterior de resposta gera `TriagemConcluida`.

- [ ] **Step 8: Executar os testes do serviço**

Run: `py manage.py test accounts.test_triagem_servico --settings=config.settings_test -v 2`

Expected: PASS.

- [ ] **Step 9: Registrar a etapa**

```bash
git add accounts/triagem_servico.py accounts/test_triagem_servico.py
git commit -m "feat: add resumable triage workflow service"
```

---

### Task 6: Views, rotas e páginas do questionário

**Files:**
- Modify: `accounts/views.py`
- Modify: `accounts/urls.py`
- Modify: `templates/accounts/triagem_apresentacao.html`
- Create: `templates/accounts/triagem_pergunta.html`
- Modify: `templates/accounts/triagem_resultado.html`
- Modify: `templates/accounts/triagem_extensa.html` somente se uma rota de compatibilidade ainda o utilizar.
- Preserve: `templates/accounts/triagem_inicio.html`, pois sua remoção não é necessária para o novo fluxo.
- Create: `accounts/test_triagem_views.py`

**Interfaces:**
- Consumes: `FormularioPergunta` e funções públicas de `triagem_servico`.
- Produces: rotas nomeadas `triagem_apresentacao`, `triagem_iniciar`, `triagem_pergunta` e `triagem_resultado`.

- [ ] **Step 1: Escrever testes da apresentação e perfis**

```python
def test_apresentacao_publica_exibe_texto_e_duas_modalidades(self):
    resposta = self.client.get(reverse("accounts:triagem_apresentacao"))
    self.assertContains(resposta, "Seu gesto de cuidado começa aqui.")
    self.assertContains(resposta, "Triagem extensa")
    self.assertContains(resposta, "Triagem simplificada")
    self.assertContains(resposta, "Quem dará a resposta final será sempre a equipe do hemocentro")

def test_resultado_de_outro_usuario_retorna_404(self):
    self.client.force_login(self.outro_usuario)
    resposta = self.client.get(reverse(
        "accounts:triagem_resultado",
        kwargs={"id_triagem": self.triagem.pk},
    ))
    self.assertEqual(resposta.status_code, 404)
```

- [ ] **Step 2: Executar e confirmar a falha de conteúdo e rotas**

Run: `py manage.py test accounts.test_triagem_views --settings=config.settings_test -v 2`

Expected: FAIL porque a apresentação atual não contém o texto integral e as novas rotas não existem.

- [ ] **Step 3: Implementar rotas únicas**

```python
path("triagem/", views.triagem_apresentacao, name="triagem_apresentacao"),
path("triagem/iniciar/<str:modalidade>/", views.triagem_iniciar, name="triagem_iniciar"),
path("triagem/<int:id_triagem>/pergunta/", views.triagem_pergunta, name="triagem_pergunta"),
path("triagem/<int:id_triagem>/resultado/", views.triagem_resultado, name="triagem_resultado"),
```

Remover as duplicações atuais de `triagem/` e de `triagem/<id>/resultado/`.

- [ ] **Step 4: Implementar views pequenas e seguras**

`triagem_iniciar` aceita somente POST e converte `extensa`/`simplificada` em `Triagem.Modalidade`. `triagem_pergunta` busca por `pk` e `usuario=request.user`, processa `acao=anterior`, `acao=salvar` ou `acao=continuar`; a conclusão redireciona ao resultado. `triagem_resultado` exige status concluído.

- [ ] **Step 5: Implementar templates sem CSS**

A apresentação reproduz integralmente o texto aprovado, usando `<strong>` nos trechos enfatizados. Cada modalidade possui formulário POST próprio. A página de pergunta exibe progresso, explicação, erros, `{{ form.as_p }}` e botões nomeados. O resultado mostra somente mensagem, estado, maior data, achados não íntimos e aviso final do hemocentro.

- [ ] **Step 6: Executar os testes de views**

Run: `py manage.py test accounts.test_triagem_views --settings=config.settings_test -v 2`

Expected: PASS.

- [ ] **Step 7: Registrar a etapa**

```bash
git add accounts/views.py accounts/urls.py templates/accounts/triagem_apresentacao.html templates/accounts/triagem_pergunta.html templates/accounts/triagem_resultado.html templates/accounts/triagem_extensa.html accounts/test_triagem_views.py
git commit -m "feat: add complete triage web flow"
```

---

### Task 7: Histórico privado, dashboard e admin

**Files:**
- Modify: `accounts/views.py`
- Modify: `accounts/urls.py`
- Create: `templates/accounts/triagem_historico.html`
- Modify: `templates/accounts/dashboard.html`
- Modify: `accounts/admin.py`
- Modify: `accounts/test_triagem_views.py`

**Interfaces:**
- Consumes: `Triagem` com status e proprietário.
- Produces: rota `triagem_historico`, contexto `ultima_triagem` no dashboard e admin integralmente somente leitura.

- [ ] **Step 1: Escrever testes do histórico e do resumo não sensível**

```python
def test_historico_lista_somente_triagens_do_usuario(self):
    self.client.force_login(self.usuario)
    resposta = self.client.get(reverse("accounts:triagem_historico"))
    self.assertContains(resposta, f"Triagem {self.triagem.pk}")
    self.assertNotContains(resposta, f"Triagem {self.triagem_de_outro.pk}")

def test_dashboard_nao_exibe_respostas_intimas(self):
    RespostaTriagem.objects.create(
        triagem=self.triagem,
        id_pergunta="EXT-43",
        codigo_resposta="EXPOSICAO",
        resposta_label="Exposição íntima",
        valor={"codigos": ["EXPOSICAO"]},
    )
    self.client.force_login(self.usuario)
    resposta = self.client.get(reverse("accounts:dashboard"))
    self.assertNotContains(resposta, "Exposição íntima")
```

- [ ] **Step 2: Executar e confirmar a falha pela rota ausente**

Run: `py manage.py test accounts.test_triagem_views --settings=config.settings_test -v 2`

Expected: FAIL em `triagem_historico`.

- [ ] **Step 3: Implementar histórico e dashboard**

`triagem_historico` usa `request.user.triagens.order_by("-iniciada_em")`. O dashboard recebe somente a triagem mais recente e nunca consulta `respostas`. Triagens em andamento exibem link de continuação; concluídas exibem link de resultado.

- [ ] **Step 4: Atualizar o admin**

Adicionar `status`, `triagem_base`, `pergunta_atual`, `fluxo_perguntas`, `atualizada_em` e `valor` a `readonly_fields`; incluir `status` em filtros/listagem. Manter `has_add_permission`, `has_change_permission` e `has_delete_permission` retornando `False`.

- [ ] **Step 5: Executar testes de privacidade e admin**

Run: `py manage.py test accounts.test_triagem_views accounts.test_triagem_models --settings=config.settings_test -v 2`

Expected: PASS.

- [ ] **Step 6: Registrar a etapa**

```bash
git add accounts/views.py accounts/urls.py templates/accounts/triagem_historico.html templates/accounts/dashboard.html accounts/admin.py accounts/test_triagem_views.py
git commit -m "feat: add private triage history"
```

---

### Task 8: Integração, limpeza e verificação completa

**Files:**
- Modify: `templates/accounts/inicio.html`
- Modify: `accounts/test_triagem.py`
- Modify: `accounts/migrations/README.md`
- Verify: todos os arquivos modificados pelas Tasks 1 a 7.

**Interfaces:**
- Consumes: fluxo completo implementado.
- Produces: projeto sem imports antigos, migrations sincronizadas e suíte verde.

- [ ] **Step 1: Escrever o teste de integração ponta a ponta**

O teste cria Doador, inicia extensa, responde o fluxo mínimo com códigos seguros, confirma `EXT-51`, verifica resultado concluído, inicia simplificada vinculada, responde `SIM-01` a `SIM-18`, confirma e verifica dois itens no histórico. Em outra execução, uma mudança em `SIM-10` deve inserir `EXT-21` a `EXT-24` antes da conclusão.

- [ ] **Step 2: Executar o teste e confirmar a primeira falha real**

Run: `py manage.py test accounts.test_triagem_views.TriagemFluxoCompletoTests --settings=config.settings_test -v 2`

Expected: FAIL no primeiro comportamento de integração ainda divergente.

- [ ] **Step 3: Corrigir somente as divergências observadas e remover código inicial substituído**

Remover imports de `TriagemExtensaForm`, `calcular_resultado` e `preparar_respostas` das views. Transformar `accounts/triagem.py` em um módulo de compatibilidade comentado que reexporta as novas interfaces, e adaptar `accounts/test_triagem.py` para não chamar o formulário único substituído. Corrigir o link público para `triagem_apresentacao` e manter toda a página inicial sem dados de saúde.

- [ ] **Step 4: Executar o teste de integração novamente**

Run: `py manage.py test accounts.test_triagem_views.TriagemFluxoCompletoTests --settings=config.settings_test -v 2`

Expected: PASS.

- [ ] **Step 5: Executar verificações estáticas e suíte completa**

Run: `py manage.py check --settings=config.settings_test`

Expected: `System check identified no issues`.

Run: `py manage.py makemigrations --check --settings=config.settings_test`

Expected: `No changes detected`.

Run: `py manage.py test --settings=config.settings_test -v 2`

Expected: PASS para toda a suíte.

Run: `git diff --check`

Expected: nenhuma saída de erro.

- [ ] **Step 6: Aplicar a migration no PostgreSQL local autorizado**

Run: `py manage.py migrate`

Expected: migration `accounts.0007_*` aplicada com `OK`.

- [ ] **Step 7: Conferir o fluxo no navegador local**

Iniciar o servidor, acessar `/triagem/`, verificar as duas modalidades, responder uma pergunta, salvar e sair, retomar no histórico e confirmar que um segundo usuário recebe 404 ao tentar abrir o resultado alheio.

- [ ] **Step 8: Registrar a implementação final**

```bash
git add accounts config templates docs/superpowers/plans/2026-09-04-triagem-completa.md
git commit -m "feat: complete extensive and simplified triage"
```
