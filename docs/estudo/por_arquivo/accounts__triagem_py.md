# accounts/triagem.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Calculos iniciais da triagem; compare seus chamadores ao motor atual.

**Arquivo original:** [accounts/triagem.py](<C:/Users/lb119/Elo/accounts/triagem.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
# Este módulo calcula o resultado inicial da triagem extensa. A triagem é apenas orientativa e não substitui a avaliação do Hemocentro.

# TRIAGEM_RULE_VERSION: Identifica a versão das regras usadas no cálculo.

# QUESTION_FIELDS: Relaciona cada campo do formulário ao código da pergunta e à origem correspondente no documento oficial da triagem.

# adicionar_achado()
# --------------------
# Registra um problema, impedimento ou alerta encontrado durante a análise.
# O achado guarda:
# - código da pergunta;
# - resultado gerado;
# - mensagem explicativa;
# - data de liberação, quando existir.
# Nenhum achado anterior é apagado.

# escolher_resultado()
# --------------------
# Analisa todos os achados e escolhe o resultado mais restritivo.
# Ordem de prioridade:
# 1. DEFINITIVA;
# 2. AVALIACAO;
# 3. TEMPORARIA;
# 4. DOCUMENTACAO.
# Se não houver nenhum achado, o resultado será SEM_IMPEDIMENTO.

# mensagem_do_resultado()
# -----------------------
# Converte o resultado interno em uma mensagem segura para o usuário.
# A mensagem deixa claro que o sistema não libera definitivamente a doação.

# calcular_resultado()
# --------------------
# Executa as regras da triagem extensa:

# - EXT-01: se a pessoa não entender que a triagem é orientativa, exige avaliação.
# - EXT-02: menores de 16 anos e pessoas com 70 anos ou mais exigem avaliação. Pessoas de 16 ou 17 anos precisam de documentação específica.
# - EXT-03: peso abaixo de 50 kg gera condição temporária. Peso igual ou acima de 130 kg, ou não informado com certeza, exige confirmação e avaliação do Hemocentro.
# - EXT-05: histórico de doação desconhecido exige avaliação.
# - EXT-05A: quando a pessoa já doou, calcula o intervalo mínimo desde a última doação: 90 dias para sexo feminino e 60 dias para sexo masculino. Se o intervalo ainda não terminou, gera resultado temporário e calcula a data orientativa de liberação.
# - EXT-04: se o sexo necessário para calcular o intervalo não for informado de formaválida, o sistema não libera automaticamente e exige avaliação.
# - EXT-05B: verifica o limite orientativo de doações nos últimos 12 meses: 3 para sexo feminino e 4 para sexo masculino. Se a quantidade for desconhecida ou atingir o limite, pode gerar avaliação ou impedimento temporário.

# Depois de analisar todas as respostas:
# - escolhe o resultado mais restritivo;
# - procura todas as datas de liberação;
# - utiliza a data mais distante quando existem vários prazos;
# - retorna resultado, mensagem, data de liberação e todos os achados.

# preparar_respostas()
# --------------------
# Converte as respostas limpas do formulário para o formato salvo no banco.
# Para cada resposta, registra:
# - código da pergunta;
# - valor enviado;
# - texto apresentado ao usuário;
# - data relacionada, quando existir;
# - versão das regras;
# - referência da pergunta original.
# Campos opcionais vazios não geram registros.
# Datas são convertidas para o formato ISO no banco e exibidas no formato brasileiro para o usuário.

# FLUXO RESUMIDO
# --------------
# Formulário de triagem - Respostas limpas pelo formulário - calcular_resultado() - Todos os achados são registrados - O resultado mais restritivo é escolhido - Mensagem e data orientativa são retornadas - preparar_respostas() organiza os dados para o histórico
# A triagem não decide a liberação médica definitiva.
# A decisão final sempre pertence ao Hemocentro.
# =============================================================================

"""
Regras iniciais da triagem extensa.

Estas regras são orientativas e não substituem a avaliação
clínica feita pelo hemocentro.

O arquivo triagem.py reúne as regras iniciais da triagem e calcula uma orientação preliminar com base nas respostas básicas do usuário.
"""

from datetime import date, timedelta

from .models import Triagem


# Versão identificável das regras utilizadas.
TRIAGEM_RULE_VERSION = "HEMOMINAS_2026_08"


# Associação entre os campos do formulário e as perguntas do documento.
QUESTION_FIELDS = [
    (
        "entende_orientacao",
        "EXT-01",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-01",
    ),
    (
        "idade",
        "EXT-02",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-02",
    ),
    (
        "peso",
        "EXT-03",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-03",
    ),
    (
        "sexo_biologico",
        "EXT-04",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-04",
    ),
    (
        "ja_doou",
        "EXT-05",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05",
    ),
    (
        "data_ultima_doacao",
        "EXT-05A",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05A",
    ),
    (
        "doacoes_12_meses",
        "EXT-05B",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05B",
    ),
]


def adicionar_achado(
    achados,
    codigo,
    resultado,
    mensagem,
    data_liberacao=None,
):
    """
    Adiciona um impedimento ou alerta sem apagar achados anteriores.
    """

    achado = {
        "codigo": codigo,
        "resultado": resultado,
        "mensagem": mensagem,
    }

    if data_liberacao:
        achado["data_liberacao"] = data_liberacao.isoformat()

    achados.append(achado)


def escolher_resultado(achados):
    """
    Escolhe o resultado mais restritivo entre todos os achados.

    A triagem não para no primeiro problema:
    todos os achados continuam registrados.
    """

    ordem = [
        Triagem.Resultado.DEFINITIVA,
        Triagem.Resultado.AVALIACAO,
        Triagem.Resultado.TEMPORARIA,
        Triagem.Resultado.DOCUMENTACAO,
    ]

    resultados = {
        achado["resultado"]
        for achado in achados
    }

    for resultado in ordem:
        if resultado in resultados:
            return resultado

    return Triagem.Resultado.SEM_IMPEDIMENTO


def mensagem_do_resultado(resultado):
    """
    Retorna a mensagem segura apresentada ao usuário.
    """

    mensagens = {
        Triagem.Resultado.SEM_IMPEDIMENTO: (
            "Com base no que você informou, não identificamos "
            "um impedimento nesta orientação. Isso não significa "
            "liberação para doar: a decisão final será tomada "
            "pela equipe do hemocentro."
        ),
        Triagem.Resultado.TEMPORARIA: (
            "Encontramos uma condição com prazo de espera. "
            "A data é apenas orientativa e só vale se não existir "
            "outro impedimento."
        ),
        Triagem.Resultado.DEFINITIVA: (
            "A condição informada foi classificada como impedimento "
            "pela regra consultada. Confirme a orientação com o "
            "hemocentro ou serviço oficial."
        ),
        Triagem.Resultado.AVALIACAO: (
            "Sua resposta depende de avaliação profissional, "
            "relatório, exame ou informação que o sistema não "
            "consegue confirmar com segurança."
        ),
        Triagem.Resultado.DOCUMENTACAO: (
            "Para continuar, será necessária documentação especial "
            "ou conferência presencial pelo hemocentro."
        ),
    }

    return mensagens[resultado]


def calcular_resultado(respostas, hoje=None):
    """
    Calcula o resultado inicial da triagem extensa.

    O parâmetro hoje existe para facilitar testes e garantir
    que o cálculo possa ser repetido com uma data conhecida.
    """

    hoje = hoje or date.today()
    achados = []

    # EXT-01: entendimento da finalidade da triagem.
    if respostas.get("entende_orientacao") != "SIM":
        adicionar_achado(
            achados,
            "EXT-01",
            Triagem.Resultado.AVALIACAO,
            (
                "A triagem só pode continuar com o entendimento "
                "de que ela é orientativa."
            ),
        )

    # EXT-02: idade.
    idade = respostas.get("idade")

    if idade == "MENOS_16":
        adicionar_achado(
            achados,
            "EXT-02",
            Triagem.Resultado.AVALIACAO,
            (
                "A idade informada exige avaliação específica "
                "do hemocentro."
            ),
        )

    elif idade == "16_17":
        adicionar_achado(
            achados,
            "EXT-06",
            Triagem.Resultado.DOCUMENTACAO,
            (
                "Pessoas de 16 ou 17 anos precisam apresentar "
                "autorização e documentação específica."
            ),
        )

    elif idade == "70_MAIS":
        adicionar_achado(
            achados,
            "EXT-02",
            Triagem.Resultado.AVALIACAO,
            (
                "A idade informada não deve ser liberada pela "
                "pré-triagem comum e exige avaliação do hemocentro."
            ),
        )

    # EXT-03: peso.
    peso = respostas.get("peso")

    if peso == "MENOS_50":
        adicionar_achado(
            achados,
            "EXT-03",
            Triagem.Resultado.TEMPORARIA,
            (
                "O peso informado está abaixo do limite utilizado "
                "nesta orientação."
            ),
        )

    elif peso in ("130_MAIS", "NAO_SEI"):
        adicionar_achado(
            achados,
            "EXT-03",
            Triagem.Resultado.AVALIACAO,
            (
                "O peso informado precisa ser confirmado e avaliado "
                "pela unidade de coleta."
            ),
        )

    # EXT-05: histórico de doação.
    ja_doou = respostas.get("ja_doou")

    if ja_doou == "NAO_LEMBRO":
        adicionar_achado(
            achados,
            "EXT-05",
            Triagem.Resultado.AVALIACAO,
            (
                "Não foi possível confirmar o histórico da última "
                "doação."
            ),
        )

    if ja_doou == "SIM":
        sexo = respostas.get("sexo_biologico")
        ultima_doacao = respostas.get("data_ultima_doacao")
        doacoes_12_meses = respostas.get("doacoes_12_meses")

        # Sexo desconhecido não deve gerar uma falsa liberação.
        if sexo not in ("FEMININO", "MASCULINO"):
            adicionar_achado(
                achados,
                "EXT-04",
                Triagem.Resultado.AVALIACAO,
                (
                    "Não foi possível aplicar com segurança a regra "
                    "do intervalo entre doações."
                ),
            )

        # Calcula o intervalo mínimo desde a última doação.
        if ultima_doacao and sexo in ("FEMININO", "MASCULINO"):
            intervalo_dias = (
                90
                if sexo == "FEMININO"
                else 60
            )

            data_intervalo = (
                ultima_doacao
                + timedelta(days=intervalo_dias)
            )

            if data_intervalo > hoje:
                adicionar_achado(
                    achados,
                    "EXT-05A",
                    Triagem.Resultado.TEMPORARIA,
                    (
                        "Ainda não terminou o intervalo orientativo "
                        "desde a última doação."
                    ),
                    data_liberacao=data_intervalo,
                )

        # Verifica o limite orientativo de doações em 12 meses.
        if doacoes_12_meses == "NAO_LEMBRO":
            adicionar_achado(
                achados,
                "EXT-05B",
                Triagem.Resultado.AVALIACAO,
                (
                    "Não foi possível confirmar a quantidade de "
                    "doações nos últimos 12 meses."
                ),
            )

        elif ultima_doacao:
            limite = (
                3
                if sexo == "FEMININO"
                else 4
            )

            quantidade_excedida = (
                doacoes_12_meses == "4_MAIS"
                or (
                    doacoes_12_meses.isdigit()
                    and int(doacoes_12_meses) >= limite
                )
            )

            if quantidade_excedida:
                # Data orientativa e conservadora para completar
                # uma janela aproximada de 12 meses.
                data_janela = (
                    ultima_doacao
                    + timedelta(days=365)
                )

                if data_janela > hoje:
                    adicionar_achado(
                        achados,
                        "EXT-05B",
                        Triagem.Resultado.TEMPORARIA,
                        (
                            "A quantidade informada atingiu o limite "
                            "orientativo de doações em 12 meses."
                        ),
                        data_liberacao=data_janela,
                    )

    # Escolhe o resultado final depois de analisar todos os achados.
    resultado = escolher_resultado(achados)

    # Usa a data mais distante quando existem vários prazos.
    datas_liberacao = []

    for achado in achados:
        data_texto = achado.get("data_liberacao")

        if data_texto:
            datas_liberacao.append(
                date.fromisoformat(data_texto)
            )

    data_liberacao = (
        max(datas_liberacao)
        if datas_liberacao
        else None
    )

    return {
        "resultado": resultado,
        "mensagem": mensagem_do_resultado(resultado),
        "data_liberacao": data_liberacao,
        "achados": achados,
    }


def preparar_respostas(form):
    """
    Converte as respostas do formulário para os registros do banco.
    """

    respostas = []

    for campo, id_pergunta, source_ref in QUESTION_FIELDS:
        valor = form.cleaned_data.get(campo)

        # Não cria registro para campos opcionais vazios.
        if valor in (None, ""):
            continue

        if isinstance(valor, date):
            codigo_resposta = valor.isoformat()
            resposta_label = valor.strftime("%d/%m/%Y")
            data_evento = valor
        else:
            codigo_resposta = str(valor)
            opcoes = dict(form.fields[campo].choices)
            resposta_label = opcoes.get(
                valor,
                str(valor),
            )
            data_evento = None

        respostas.append(
            {
                "id_pergunta": id_pergunta,
                "codigo_resposta": codigo_resposta,
                "resposta_label": resposta_label,
                "data_evento": data_evento,
                "metadata": {},
                "rule_version": TRIAGEM_RULE_VERSION,
                "source_ref": source_ref,
            }
        )

    return respostas
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 70 a 77

```python
"""
Regras iniciais da triagem extensa.

Estas regras são orientativas e não substituem a avaliação
clínica feita pelo hemocentro.

O arquivo triagem.py reúne as regras iniciais da triagem e calcula uma orientação preliminar com base nas respostas básicas do usuário.
"""
```

**Explicação deste trecho:**

**Linha 70 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 79 a 79

```python
from datetime import date, timedelta
```

**Explicação deste trecho:**

**Linha 79 — ImportFrom** (nível 0 do bloco).

Importa de `datetime` os nomes `date`, `timedelta`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 81 a 81

```python
from .models import Triagem
```

**Explicação deste trecho:**

**Linha 81 — ImportFrom** (nível 0 do bloco).

Importa de `.models` os nomes `Triagem`. Pontos iniciais indicam importação relativa ao pacote.

### Assign — linhas 85 a 85

```python
TRIAGEM_RULE_VERSION = "HEMOMINAS_2026_08"
```

**Explicação deste trecho:**

**Linha 85 — Assign** (nível 0 do bloco).

Associa `TRIAGEM_RULE_VERSION` a o valor literal `'HEMOMINAS_2026_08'`.

### Assign — linhas 89 a 125

```python
QUESTION_FIELDS = [
    (
        "entende_orientacao",
        "EXT-01",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-01",
    ),
    (
        "idade",
        "EXT-02",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-02",
    ),
    (
        "peso",
        "EXT-03",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-03",
    ),
    (
        "sexo_biologico",
        "EXT-04",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-04",
    ),
    (
        "ja_doou",
        "EXT-05",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05",
    ),
    (
        "data_ultima_doacao",
        "EXT-05A",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05A",
    ),
    (
        "doacoes_12_meses",
        "EXT-05B",
        "Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05B",
    ),
]
```

**Explicação deste trecho:**

**Linha 89 — Assign** (nível 0 do bloco).

Associa `QUESTION_FIELDS` a uma coleção List com 7 itens, na expressão `[('entende_orientacao', 'EXT-01', 'Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-01'), ('idade', 'EXT-02', 'Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-02'), ('peso', 'EXT-03', 'Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-03'), ('sexo_biologico', 'EXT-04', 'Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-04'), ('ja_doou', 'EXT-05', 'Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05'), ('data_ultima_doacao', 'EXT-05A', 'Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05A'), ('doacoes_12_meses', 'EXT-05B', 'Especificacao_Triagem_Elo_Completa_e_Simplificada.pdf - EXT-05B')]`.

### adicionar_achado — linhas 128 a 148

```python
def adicionar_achado(
    achados,
    codigo,
    resultado,
    mensagem,
    data_liberacao=None,
):
    """
    Adiciona um impedimento ou alerta sem apagar achados anteriores.
    """

    achado = {
        "codigo": codigo,
        "resultado": resultado,
        "mensagem": mensagem,
    }

    if data_liberacao:
        achado["data_liberacao"] = data_liberacao.isoformat()

    achados.append(achado)
```

**Explicação deste trecho:**

**Linha 128 — FunctionDef** (nível 0 do bloco).

Define `adicionar_achado(achados, codigo, resultado, mensagem, data_liberacao=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 128:

**Linha 135 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 139 — Assign** (nível 1 do bloco).

Associa `achado` a um dicionário de 3 entradas; as chaves dão nome aos valores associados.

- Chave `'codigo'`: recebe o valor associado ao nome `codigo`.
- Chave `'resultado'`: recebe o valor associado ao nome `resultado`.
- Chave `'mensagem'`: recebe o valor associado ao nome `mensagem`.

**Linha 145 — If** (nível 1 do bloco).

Escolhe um caminho verificando o valor associado ao nome `data_liberacao`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 145:

**Linha 146 — Assign** (nível 2 do bloco).

Associa `achado['data_liberacao']` a a chamada `data_liberacao.isoformat`.


**Linha 148 — Expr** (nível 1 do bloco).

Executa a chamada `achados.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `achado`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

### escolher_resultado — linhas 151 a 175

```python
def escolher_resultado(achados):
    """
    Escolhe o resultado mais restritivo entre todos os achados.

    A triagem não para no primeiro problema:
    todos os achados continuam registrados.
    """

    ordem = [
        Triagem.Resultado.DEFINITIVA,
        Triagem.Resultado.AVALIACAO,
        Triagem.Resultado.TEMPORARIA,
        Triagem.Resultado.DOCUMENTACAO,
    ]

    resultados = {
        achado["resultado"]
        for achado in achados
    }

    for resultado in ordem:
        if resultado in resultados:
            return resultado

    return Triagem.Resultado.SEM_IMPEDIMENTO
```

**Explicação deste trecho:**

**Linha 151 — FunctionDef** (nível 0 do bloco).

Define `escolher_resultado(achados)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 151:

**Linha 152 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 159 — Assign** (nível 1 do bloco).

Associa `ordem` a uma coleção List com 4 itens, na expressão `[Triagem.Resultado.DEFINITIVA, Triagem.Resultado.AVALIACAO, Triagem.Resultado.TEMPORARIA, Triagem.Resultado.DOCUMENTACAO]`.

**Linha 166 — Assign** (nível 1 do bloco).

Associa `resultados` a uma coleção/gerador construído por compreensão em `{achado['resultado'] for achado in achados}`: percorre as fontes e aplica os filtros declarados.

**Linha 171 — For** (nível 1 do bloco).

Percorre `ordem`; cada item é atribuído a `resultado` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 171:

**Linha 172 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `resultado` contido em `resultados`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 172:

**Linha 173 — Return** (nível 3 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `resultado` ao chamador.

**Linha 175 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o atributo `SEM_IMPEDIMENTO` de `Triagem.Resultado` ao chamador.

### mensagem_do_resultado — linhas 178 a 211

```python
def mensagem_do_resultado(resultado):
    """
    Retorna a mensagem segura apresentada ao usuário.
    """

    mensagens = {
        Triagem.Resultado.SEM_IMPEDIMENTO: (
            "Com base no que você informou, não identificamos "
            "um impedimento nesta orientação. Isso não significa "
            "liberação para doar: a decisão final será tomada "
            "pela equipe do hemocentro."
        ),
        Triagem.Resultado.TEMPORARIA: (
            "Encontramos uma condição com prazo de espera. "
            "A data é apenas orientativa e só vale se não existir "
            "outro impedimento."
        ),
        Triagem.Resultado.DEFINITIVA: (
            "A condição informada foi classificada como impedimento "
            "pela regra consultada. Confirme a orientação com o "
            "hemocentro ou serviço oficial."
        ),
        Triagem.Resultado.AVALIACAO: (
            "Sua resposta depende de avaliação profissional, "
            "relatório, exame ou informação que o sistema não "
            "consegue confirmar com segurança."
        ),
        Triagem.Resultado.DOCUMENTACAO: (
            "Para continuar, será necessária documentação especial "
            "ou conferência presencial pelo hemocentro."
        ),
    }

    return mensagens[resultado]
```

**Explicação deste trecho:**

**Linha 178 — FunctionDef** (nível 0 do bloco).

Define `mensagem_do_resultado(resultado)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 178:

**Linha 179 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 183 — Assign** (nível 1 do bloco).

Associa `mensagens` a um dicionário de 5 entradas; as chaves dão nome aos valores associados.

- Chave `Triagem.Resultado.SEM_IMPEDIMENTO`: recebe o valor literal `'Com base no que você informou, não identificamos um impedimento nesta orientação. Isso não significa liberação para doar: a decisão final será tomada pela equipe do hemocentro.'`.
- Chave `Triagem.Resultado.TEMPORARIA`: recebe o valor literal `'Encontramos uma condição com prazo de espera. A data é apenas orientativa e só vale se não existir outro impedimento.'`.
- Chave `Triagem.Resultado.DEFINITIVA`: recebe o valor literal `'A condição informada foi classificada como impedimento pela regra consultada. Confirme a orientação com o hemocentro ou serviço oficial.'`.
- Chave `Triagem.Resultado.AVALIACAO`: recebe o valor literal `'Sua resposta depende de avaliação profissional, relatório, exame ou informação que o sistema não consegue confirmar com segurança.'`.
- Chave `Triagem.Resultado.DOCUMENTACAO`: recebe o valor literal `'Para continuar, será necessária documentação especial ou conferência presencial pelo hemocentro.'`.

**Linha 211 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o item ou recorte `resultado` de `mensagens` ao chamador.

### calcular_resultado — linhas 214 a 426

```python
def calcular_resultado(respostas, hoje=None):
    """
    Calcula o resultado inicial da triagem extensa.

    O parâmetro hoje existe para facilitar testes e garantir
    que o cálculo possa ser repetido com uma data conhecida.
    """

    hoje = hoje or date.today()
    achados = []

    # EXT-01: entendimento da finalidade da triagem.
    if respostas.get("entende_orientacao") != "SIM":
        adicionar_achado(
            achados,
            "EXT-01",
            Triagem.Resultado.AVALIACAO,
            (
                "A triagem só pode continuar com o entendimento "
                "de que ela é orientativa."
            ),
        )

    # EXT-02: idade.
    idade = respostas.get("idade")

    if idade == "MENOS_16":
        adicionar_achado(
            achados,
            "EXT-02",
            Triagem.Resultado.AVALIACAO,
            (
                "A idade informada exige avaliação específica "
                "do hemocentro."
            ),
        )

    elif idade == "16_17":
        adicionar_achado(
            achados,
            "EXT-06",
            Triagem.Resultado.DOCUMENTACAO,
            (
                "Pessoas de 16 ou 17 anos precisam apresentar "
                "autorização e documentação específica."
            ),
        )

    elif idade == "70_MAIS":
        adicionar_achado(
            achados,
            "EXT-02",
            Triagem.Resultado.AVALIACAO,
            (
                "A idade informada não deve ser liberada pela "
                "pré-triagem comum e exige avaliação do hemocentro."
            ),
        )

    # EXT-03: peso.
    peso = respostas.get("peso")

    if peso == "MENOS_50":
        adicionar_achado(
            achados,
            "EXT-03",
            Triagem.Resultado.TEMPORARIA,
            (
                "O peso informado está abaixo do limite utilizado "
                "nesta orientação."
            ),
        )

    elif peso in ("130_MAIS", "NAO_SEI"):
        adicionar_achado(
            achados,
            "EXT-03",
            Triagem.Resultado.AVALIACAO,
            (
                "O peso informado precisa ser confirmado e avaliado "
                "pela unidade de coleta."
            ),
        )

    # EXT-05: histórico de doação.
    ja_doou = respostas.get("ja_doou")

    if ja_doou == "NAO_LEMBRO":
        adicionar_achado(
            achados,
            "EXT-05",
            Triagem.Resultado.AVALIACAO,
            (
                "Não foi possível confirmar o histórico da última "
                "doação."
            ),
        )

    if ja_doou == "SIM":
        sexo = respostas.get("sexo_biologico")
        ultima_doacao = respostas.get("data_ultima_doacao")
        doacoes_12_meses = respostas.get("doacoes_12_meses")

        # Sexo desconhecido não deve gerar uma falsa liberação.
        if sexo not in ("FEMININO", "MASCULINO"):
            adicionar_achado(
                achados,
                "EXT-04",
                Triagem.Resultado.AVALIACAO,
                (
                    "Não foi possível aplicar com segurança a regra "
                    "do intervalo entre doações."
                ),
            )

        # Calcula o intervalo mínimo desde a última doação.
        if ultima_doacao and sexo in ("FEMININO", "MASCULINO"):
            intervalo_dias = (
                90
                if sexo == "FEMININO"
                else 60
            )

            data_intervalo = (
                ultima_doacao
                + timedelta(days=intervalo_dias)
            )

            if data_intervalo > hoje:
                adicionar_achado(
                    achados,
                    "EXT-05A",
                    Triagem.Resultado.TEMPORARIA,
                    (
                        "Ainda não terminou o intervalo orientativo "
                        "desde a última doação."
                    ),
                    data_liberacao=data_intervalo,
                )

        # Verifica o limite orientativo de doações em 12 meses.
        if doacoes_12_meses == "NAO_LEMBRO":
            adicionar_achado(
                achados,
                "EXT-05B",
                Triagem.Resultado.AVALIACAO,
                (
                    "Não foi possível confirmar a quantidade de "
                    "doações nos últimos 12 meses."
                ),
            )

        elif ultima_doacao:
            limite = (
                3
                if sexo == "FEMININO"
                else 4
            )

            quantidade_excedida = (
                doacoes_12_meses == "4_MAIS"
                or (
                    doacoes_12_meses.isdigit()
                    and int(doacoes_12_meses) >= limite
                )
            )

            if quantidade_excedida:
                # Data orientativa e conservadora para completar
                # uma janela aproximada de 12 meses.
                data_janela = (
                    ultima_doacao
                    + timedelta(days=365)
                )

                if data_janela > hoje:
                    adicionar_achado(
                        achados,
                        "EXT-05B",
                        Triagem.Resultado.TEMPORARIA,
                        (
                            "A quantidade informada atingiu o limite "
                            "orientativo de doações em 12 meses."
                        ),
                        data_liberacao=data_janela,
                    )

    # Escolhe o resultado final depois de analisar todos os achados.
    resultado = escolher_resultado(achados)

    # Usa a data mais distante quando existem vários prazos.
    datas_liberacao = []

    for achado in achados:
        data_texto = achado.get("data_liberacao")

        if data_texto:
            datas_liberacao.append(
                date.fromisoformat(data_texto)
            )

    data_liberacao = (
        max(datas_liberacao)
        if datas_liberacao
        else None
    )

    return {
        "resultado": resultado,
        "mensagem": mensagem_do_resultado(resultado),
        "data_liberacao": data_liberacao,
        "achados": achados,
    }
```

**Explicação deste trecho:**

**Linha 214 — FunctionDef** (nível 0 do bloco).

Define `calcular_resultado(respostas, hoje=None)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 214:

**Linha 215 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 222 — Assign** (nível 1 do bloco).

Associa `hoje` a pelo menos uma das condições: `hoje` ; `date.today()` (com avaliação interrompida assim que o resultado é determinado).

**Linha 223 — Assign** (nível 1 do bloco).

Associa `achados` a uma coleção List com 0 itens, na expressão `[]`.

**Linha 226 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `respostas.get('entende_orientacao')` diferente de `'SIM'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 226:

**Linha 227 — Expr** (nível 2 do bloco).

Executa a chamada `adicionar_achado`; argumentos posicionais: `achados`, `'EXT-01'`, `Triagem.Resultado.AVALIACAO`, `'A triagem só pode continuar com o entendimento de que ela é orientativa.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 238 — Assign** (nível 1 do bloco).

Associa `idade` a a chamada `respostas.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'idade'`.


**Linha 240 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `idade` igual a `'MENOS_16'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 240:

**Linha 241 — Expr** (nível 2 do bloco).

Executa a chamada `adicionar_achado`; argumentos posicionais: `achados`, `'EXT-02'`, `Triagem.Resultado.AVALIACAO`, `'A idade informada exige avaliação específica do hemocentro.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 240:

**Linha 251 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `idade` igual a `'16_17'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 251:

**Linha 252 — Expr** (nível 3 do bloco).

Executa a chamada `adicionar_achado`; argumentos posicionais: `achados`, `'EXT-06'`, `Triagem.Resultado.DOCUMENTACAO`, `'Pessoas de 16 ou 17 anos precisam apresentar autorização e documentação específica.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 251:

**Linha 262 — If** (nível 3 do bloco).

Escolhe um caminho verificando a comparação `idade` igual a `'70_MAIS'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 262:

**Linha 263 — Expr** (nível 4 do bloco).

Executa a chamada `adicionar_achado`; argumentos posicionais: `achados`, `'EXT-02'`, `Triagem.Resultado.AVALIACAO`, `'A idade informada não deve ser liberada pela pré-triagem comum e exige avaliação do hemocentro.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 274 — Assign** (nível 1 do bloco).

Associa `peso` a a chamada `respostas.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'peso'`.


**Linha 276 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `peso` igual a `'MENOS_50'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 276:

**Linha 277 — Expr** (nível 2 do bloco).

Executa a chamada `adicionar_achado`; argumentos posicionais: `achados`, `'EXT-03'`, `Triagem.Resultado.TEMPORARIA`, `'O peso informado está abaixo do limite utilizado nesta orientação.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 276:

**Linha 287 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `peso` contido em `('130_MAIS', 'NAO_SEI')`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 287:

**Linha 288 — Expr** (nível 3 do bloco).

Executa a chamada `adicionar_achado`; argumentos posicionais: `achados`, `'EXT-03'`, `Triagem.Resultado.AVALIACAO`, `'O peso informado precisa ser confirmado e avaliado pela unidade de coleta.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 299 — Assign** (nível 1 do bloco).

Associa `ja_doou` a a chamada `respostas.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'ja_doou'`.


**Linha 301 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `ja_doou` igual a `'NAO_LEMBRO'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 301:

**Linha 302 — Expr** (nível 2 do bloco).

Executa a chamada `adicionar_achado`; argumentos posicionais: `achados`, `'EXT-05'`, `Triagem.Resultado.AVALIACAO`, `'Não foi possível confirmar o histórico da última doação.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 312 — If** (nível 1 do bloco).

Escolhe um caminho verificando a comparação `ja_doou` igual a `'SIM'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 312:

**Linha 313 — Assign** (nível 2 do bloco).

Associa `sexo` a a chamada `respostas.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'sexo_biologico'`.


**Linha 314 — Assign** (nível 2 do bloco).

Associa `ultima_doacao` a a chamada `respostas.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'data_ultima_doacao'`.


**Linha 315 — Assign** (nível 2 do bloco).

Associa `doacoes_12_meses` a a chamada `respostas.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'doacoes_12_meses'`.


**Linha 318 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `sexo` não contido em `('FEMININO', 'MASCULINO')`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 318:

**Linha 319 — Expr** (nível 3 do bloco).

Executa a chamada `adicionar_achado`; argumentos posicionais: `achados`, `'EXT-04'`, `Triagem.Resultado.AVALIACAO`, `'Não foi possível aplicar com segurança a regra do intervalo entre doações.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 330 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `ultima_doacao` ; `sexo in ('FEMININO', 'MASCULINO')` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 330:

**Linha 331 — Assign** (nível 3 do bloco).

Associa `intervalo_dias` a `90` se `sexo == 'FEMININO'` for verdadeiro; caso contrário, `60`.

**Linha 337 — Assign** (nível 3 do bloco).

Associa `data_intervalo` a a expressão `ultima_doacao + timedelta(days=intervalo_dias)`; seus operadores determinam o cálculo.

**Linha 342 — If** (nível 3 do bloco).

Escolhe um caminho verificando a comparação `data_intervalo` maior que `hoje`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 342:

**Linha 343 — Expr** (nível 4 do bloco).

Executa a chamada `adicionar_achado`; argumentos posicionais: `achados`, `'EXT-05A'`, `Triagem.Resultado.TEMPORARIA`, `'Ainda não terminou o intervalo orientativo desde a última doação.'`; argumentos nomeados: `data_liberacao=data_intervalo`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 355 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `doacoes_12_meses` igual a `'NAO_LEMBRO'`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 355:

**Linha 356 — Expr** (nível 3 do bloco).

Executa a chamada `adicionar_achado`; argumentos posicionais: `achados`, `'EXT-05B'`, `Triagem.Resultado.AVALIACAO`, `'Não foi possível confirmar a quantidade de doações nos últimos 12 meses.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 355:

**Linha 366 — If** (nível 3 do bloco).

Escolhe um caminho verificando o valor associado ao nome `ultima_doacao`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 366:

**Linha 367 — Assign** (nível 4 do bloco).

Associa `limite` a `3` se `sexo == 'FEMININO'` for verdadeiro; caso contrário, `4`.

**Linha 373 — Assign** (nível 4 do bloco).

Associa `quantidade_excedida` a pelo menos uma das condições: `doacoes_12_meses == '4_MAIS'` ; `doacoes_12_meses.isdigit() and int(doacoes_12_meses) >= limite` (com avaliação interrompida assim que o resultado é determinado).

**Linha 381 — If** (nível 4 do bloco).

Escolhe um caminho verificando o valor associado ao nome `quantidade_excedida`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 381:

**Linha 384 — Assign** (nível 5 do bloco).

Associa `data_janela` a a expressão `ultima_doacao + timedelta(days=365)`; seus operadores determinam o cálculo.

**Linha 389 — If** (nível 5 do bloco).

Escolhe um caminho verificando a comparação `data_janela` maior que `hoje`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 389:

**Linha 390 — Expr** (nível 6 do bloco).

Executa a chamada `adicionar_achado`; argumentos posicionais: `achados`, `'EXT-05B'`, `Triagem.Resultado.TEMPORARIA`, `'A quantidade informada atingiu o limite orientativo de doações em 12 meses.'`; argumentos nomeados: `data_liberacao=data_janela`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 402 — Assign** (nível 1 do bloco).

Associa `resultado` a a chamada `escolher_resultado`; argumentos posicionais: `achados`.


**Linha 405 — Assign** (nível 1 do bloco).

Associa `datas_liberacao` a uma coleção List com 0 itens, na expressão `[]`.

**Linha 407 — For** (nível 1 do bloco).

Percorre `achados`; cada item é atribuído a `achado` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 407:

**Linha 408 — Assign** (nível 2 do bloco).

Associa `data_texto` a a chamada `achado.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'data_liberacao'`.


**Linha 410 — If** (nível 2 do bloco).

Escolhe um caminho verificando o valor associado ao nome `data_texto`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 410:

**Linha 411 — Expr** (nível 3 do bloco).

Executa a chamada `datas_liberacao.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `date.fromisoformat(data_texto)`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 415 — Assign** (nível 1 do bloco).

Associa `data_liberacao` a `max(datas_liberacao)` se `datas_liberacao` for verdadeiro; caso contrário, `None`.

**Linha 421 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve um dicionário de 4 entradas; as chaves dão nome aos valores associados ao chamador.

### preparar_respostas — linhas 429 a 468

```python
def preparar_respostas(form):
    """
    Converte as respostas do formulário para os registros do banco.
    """

    respostas = []

    for campo, id_pergunta, source_ref in QUESTION_FIELDS:
        valor = form.cleaned_data.get(campo)

        # Não cria registro para campos opcionais vazios.
        if valor in (None, ""):
            continue

        if isinstance(valor, date):
            codigo_resposta = valor.isoformat()
            resposta_label = valor.strftime("%d/%m/%Y")
            data_evento = valor
        else:
            codigo_resposta = str(valor)
            opcoes = dict(form.fields[campo].choices)
            resposta_label = opcoes.get(
                valor,
                str(valor),
            )
            data_evento = None

        respostas.append(
            {
                "id_pergunta": id_pergunta,
                "codigo_resposta": codigo_resposta,
                "resposta_label": resposta_label,
                "data_evento": data_evento,
                "metadata": {},
                "rule_version": TRIAGEM_RULE_VERSION,
                "source_ref": source_ref,
            }
        )

    return respostas
```

**Explicação deste trecho:**

**Linha 429 — FunctionDef** (nível 0 do bloco).

Define `preparar_respostas(form)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 429:

**Linha 430 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 434 — Assign** (nível 1 do bloco).

Associa `respostas` a uma coleção List com 0 itens, na expressão `[]`.

**Linha 436 — For** (nível 1 do bloco).

Percorre `QUESTION_FIELDS`; cada item é atribuído a `(campo, id_pergunta, source_ref)` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 436:

**Linha 437 — Assign** (nível 2 do bloco).

Associa `valor` a a chamada `form.cleaned_data.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `campo`.


**Linha 440 — If** (nível 2 do bloco).

Escolhe um caminho verificando a comparação `valor` contido em `(None, '')`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 440:

**Linha 441 — Continue** (nível 3 do bloco).

Pula o restante da iteração atual e segue para o próximo item do laço.

**Linha 443 — If** (nível 2 do bloco).

Escolhe um caminho verificando a chamada `isinstance`; argumentos posicionais: `valor`, `date`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 443:

**Linha 444 — Assign** (nível 3 do bloco).

Associa `codigo_resposta` a a chamada `valor.isoformat`.


**Linha 445 — Assign** (nível 3 do bloco).

Associa `resposta_label` a a chamada `valor.strftime`; argumentos posicionais: `'%d/%m/%Y'`.


**Linha 446 — Assign** (nível 3 do bloco).

Associa `data_evento` a o valor associado ao nome `valor`.

Bloco `orelse` da linha 443:

**Linha 448 — Assign** (nível 3 do bloco).

Associa `codigo_resposta` a a chamada `str`; argumentos posicionais: `valor`.


**Linha 449 — Assign** (nível 3 do bloco).

Associa `opcoes` a a chamada `dict`; argumentos posicionais: `form.fields[campo].choices`.


**Linha 450 — Assign** (nível 3 do bloco).

Associa `resposta_label` a a chamada `opcoes.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `valor`, `str(valor)`.


**Linha 454 — Assign** (nível 3 do bloco).

Associa `data_evento` a o valor literal `None`.

**Linha 456 — Expr** (nível 2 do bloco).

Executa a chamada `respostas.append`, que acrescenta um item ao fim da lista; argumentos posicionais: `{'id_pergunta': id_pergunta, 'codigo_resposta': codigo_resposta, 'resposta_label': resposta_label, 'data_evento': data_evento, 'metadata': {}, 'rule_version': TRIAGEM_RULE_VERSION, 'source_ref': source_ref}`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 468 — Return** (nível 1 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `respostas` ao chamador.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 1: `# Este módulo calcula o resultado inicial da triagem extensa. A triagem é apenas orientativa e não substitui a avaliação do Hemocentro.`
- Linha 3: `# TRIAGEM_RULE_VERSION: Identifica a versão das regras usadas no cálculo.`
- Linha 5: `# QUESTION_FIELDS: Relaciona cada campo do formulário ao código da pergunta e à origem correspondente no documento oficial da triagem.`
- Linha 7: `# adicionar_achado()`
- Linha 8: `# --------------------`
- Linha 9: `# Registra um problema, impedimento ou alerta encontrado durante a análise.`
- Linha 10: `# O achado guarda:`
- Linha 11: `# - código da pergunta;`
- Linha 12: `# - resultado gerado;`
- Linha 13: `# - mensagem explicativa;`
- Linha 14: `# - data de liberação, quando existir.`
- Linha 15: `# Nenhum achado anterior é apagado.`
- Linha 17: `# escolher_resultado()`
- Linha 18: `# --------------------`
- Linha 19: `# Analisa todos os achados e escolhe o resultado mais restritivo.`
- Linha 20: `# Ordem de prioridade:`
- Linha 21: `# 1. DEFINITIVA;`
- Linha 22: `# 2. AVALIACAO;`
- Linha 23: `# 3. TEMPORARIA;`
- Linha 24: `# 4. DOCUMENTACAO.`
- Linha 25: `# Se não houver nenhum achado, o resultado será SEM_IMPEDIMENTO.`
- Linha 27: `# mensagem_do_resultado()`
- Linha 28: `# -----------------------`
- Linha 29: `# Converte o resultado interno em uma mensagem segura para o usuário.`
- Linha 30: `# A mensagem deixa claro que o sistema não libera definitivamente a doação.`
- Linha 32: `# calcular_resultado()`
- Linha 33: `# --------------------`
- Linha 34: `# Executa as regras da triagem extensa:`
- Linha 36: `# - EXT-01: se a pessoa não entender que a triagem é orientativa, exige avaliação.`
- Linha 37: `# - EXT-02: menores de 16 anos e pessoas com 70 anos ou mais exigem avaliação. Pessoas de 16 ou 17 anos precisam de documentação específica.`
- Linha 38: `# - EXT-03: peso abaixo de 50 kg gera condição temporária. Peso igual ou acima de 130 kg, ou não informado com certeza, exige confirmação e avaliação do Hemocentro.`
- Linha 39: `# - EXT-05: histórico de doação desconhecido exige avaliação.`
- Linha 40: `# - EXT-05A: quando a pessoa já doou, calcula o intervalo mínimo desde a última doação: 90 dias para sexo feminino e 60 dias para sexo masculino. Se o intervalo ainda não terminou, gera resultado temporário e calcula a data orientativa de liberação.`
- Linha 41: `# - EXT-04: se o sexo necessário para calcular o intervalo não for informado de formaválida, o sistema não libera automaticamente e exige avaliação.`
- Linha 42: `# - EXT-05B: verifica o limite orientativo de doações nos últimos 12 meses: 3 para sexo feminino e 4 para sexo masculino. Se a quantidade for desconhecida ou atingir o limite, pode gerar avaliação ou impedimento temporário.`
- Linha 44: `# Depois de analisar todas as respostas:`
- Linha 45: `# - escolhe o resultado mais restritivo;`
- Linha 46: `# - procura todas as datas de liberação;`
- Linha 47: `# - utiliza a data mais distante quando existem vários prazos;`
- Linha 48: `# - retorna resultado, mensagem, data de liberação e todos os achados.`
- Linha 50: `# preparar_respostas()`
- Linha 51: `# --------------------`
- Linha 52: `# Converte as respostas limpas do formulário para o formato salvo no banco.`
- Linha 53: `# Para cada resposta, registra:`
- Linha 54: `# - código da pergunta;`
- Linha 55: `# - valor enviado;`
- Linha 56: `# - texto apresentado ao usuário;`
- Linha 57: `# - data relacionada, quando existir;`
- Linha 58: `# - versão das regras;`
- Linha 59: `# - referência da pergunta original.`
- Linha 60: `# Campos opcionais vazios não geram registros.`
- Linha 61: `# Datas são convertidas para o formato ISO no banco e exibidas no formato brasileiro para o usuário.`
- Linha 63: `# FLUXO RESUMIDO`
- Linha 64: `# --------------`
- Linha 65: `# Formulário de triagem - Respostas limpas pelo formulário - calcular_resultado() - Todos os achados são registrados - O resultado mais restritivo é escolhido - Mensagem e data orientativa são retornadas - preparar_respostas() organiza os dados para o histórico`
- Linha 66: `# A triagem não decide a liberação médica definitiva.`
- Linha 67: `# A decisão final sempre pertence ao Hemocentro.`
- Linha 68: `# =============================================================================`
- Linha 84: `# Versão identificável das regras utilizadas.`
- Linha 88: `# Associação entre os campos do formulário e as perguntas do documento.`
- Linha 225: `# EXT-01: entendimento da finalidade da triagem.`
- Linha 237: `# EXT-02: idade.`
- Linha 273: `# EXT-03: peso.`
- Linha 298: `# EXT-05: histórico de doação.`
- Linha 317: `# Sexo desconhecido não deve gerar uma falsa liberação.`
- Linha 329: `# Calcula o intervalo mínimo desde a última doação.`
- Linha 354: `# Verifica o limite orientativo de doações em 12 meses.`
- Linha 382: `# Data orientativa e conservadora para completar`
- Linha 383: `# uma janela aproximada de 12 meses.`
- Linha 401: `# Escolhe o resultado final depois de analisar todos os achados.`
- Linha 404: `# Usa a data mais distante quando existem vários prazos.`
- Linha 439: `# Não cria registro para campos opcionais vazios.`

