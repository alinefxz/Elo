# accounts/triagem_forms.py: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Formulario dinamico correspondente a cada pergunta.

**Arquivo original:** [accounts/triagem_forms.py](<C:/Users/lb119/Elo/accounts/triagem_forms.py>). As linhas referem-se à cópia desta data.

## Código integral

``````py
# Este arquivo cria dinamicamente o formulário de cada pergunta da triagem.

# - Recebe uma pergunta do catálogo e monta os campos necessários.
# - Usa rádio para respostas únicas e checkbox para múltiplas respostas.
# - Reaproveita respostas anteriores quando a pergunta está sendo editada.
# - Cria campos de data para alternativas que exigem prazo.
# - Permite informar detalhes complementares.
# - Adiciona campos extras para segurança e inflamação quando necessários.
# - Impede combinações inválidas, como marcar "Nenhuma" junto com uma doença.
# - Exige datas e detalhes quando a alternativa selecionada precisar dessas informações.
# - Impede datas futuras.
# - Valida as condições de procedimentos e informações de segurança.
# - Organiza tudo no campo "valor", contendo códigos, datas, detalhes e dados complementares, para ser salvo pela camada de serviço.

# Este arquivo valida e organiza as respostas, mas não calcula o resultado médico da triagem. Essa responsabilidade pertence ao triagem_motor.py.

"""Formulário dinâmico usado por todas as perguntas da triagem."""

from datetime import date

from django import forms


class FormularioPergunta(forms.Form):
    """Cria somente os campos necessários para uma pergunta do catálogo."""

    def __init__(self, pergunta, *args, **kwargs):
        self.pergunta = pergunta
        valor_inicial = kwargs.pop("valor_inicial", None) or {}
        super().__init__(*args, **kwargs)

        escolhas = [
            (opcao["codigo"], opcao["rotulo"])
            for opcao in pergunta["opcoes"]
        ]
        codigos_iniciais = valor_inicial.get("codigos") or []

        if pergunta["multipla"]:
            self.fields["resposta"] = forms.MultipleChoiceField(
                label=pergunta["texto"],
                choices=escolhas,
                widget=forms.CheckboxSelectMultiple,
                initial=codigos_iniciais,
            )
        else:
            self.fields["resposta"] = forms.ChoiceField(
                label=pergunta["texto"],
                choices=escolhas,
                widget=forms.RadioSelect,
                initial=(codigos_iniciais[0] if codigos_iniciais else None),
            )

        # Cada alternativa temporal recebe sua própria data.
        datas_iniciais = valor_inicial.get("datas") or {}
        rotulos = {
            opcao["codigo"]: opcao["rotulo"]
            for opcao in pergunta["opcoes"]
        }
        for codigo in pergunta["exige_data_para"]:
            self.fields[f"data_{codigo}"] = forms.DateField(
                label=f"Data relacionada a: {rotulos[codigo]}",
                required=False,
                initial=datas_iniciais.get(codigo),
                widget=forms.DateInput(attrs={"type": "date"}),
            )

        # O complemento permite explicar motivo, tratamento ou exceção.
        self.fields["detalhes"] = forms.CharField(
            label="Informações complementares",
            required=False,
            max_length=500,
            initial=valor_inicial.get("detalhes", ""),
            help_text=(
                "Informe somente o necessário para esclarecer esta resposta."
            ),
            widget=forms.Textarea(attrs={"rows": 3}),
        )

        if pergunta["perguntar_seguranca"]:
            self.fields["seguranca"] = forms.ChoiceField(
                label="As condições de higiene, antissepsia e material eram seguras?",
                required=False,
                choices=[
                    ("", "Selecione"),
                    ("SIM", "Sim."),
                    ("NAO", "Não."),
                    ("NAO_SEI", "Não sei confirmar."),
                ],
                initial=valor_inicial.get("seguranca", ""),
            )

        if pergunta["perguntar_inflamacao"]:
            self.fields["inflamacao"] = forms.ChoiceField(
                label="Houve inflamação ou infecção depois do procedimento?",
                required=False,
                choices=[
                    ("", "Selecione"),
                    ("SIM", "Sim."),
                    ("NAO", "Não."),
                    ("NAO_SEI", "Não sei."),
                ],
                initial=valor_inicial.get("inflamacao", ""),
            )

    def clean(self):
        """Valida contradições e devolve um valor único para persistência."""

        dados = super().clean()
        resposta = dados.get("resposta")

        if self.pergunta["multipla"]:
            codigos = list(resposta or [])
        else:
            codigos = [resposta] if resposta else []

        # Alternativas negativas ou neutras não podem coexistir com doenças.
        exclusivos = {"NAO", "NENHUMA", "NENHUM", "SIM"}
        if len(codigos) > 1 and exclusivos.intersection(codigos):
            self.add_error(
                "resposta",
                "Escolha a alternativa neutra sozinha ou marque as condições.",
            )

        datas = {}
        for codigo in self.pergunta["exige_data_para"]:
            nome_campo = f"data_{codigo}"
            data_evento = dados.get(nome_campo)

            if codigo in codigos and not data_evento:
                self.add_error(
                    nome_campo,
                    "Informe a data desta alternativa.",
                )
            elif data_evento and data_evento > date.today():
                self.add_error(
                    nome_campo,
                    "A data não pode estar no futuro.",
                )
            elif codigo in codigos and data_evento:
                datas[codigo] = data_evento.isoformat()

        detalhes = (dados.get("detalhes") or "").strip()
        if (
            set(codigos).intersection(
                self.pergunta["exige_detalhes_para"]
            )
            and not detalhes
        ):
            self.add_error(
                "detalhes",
                "Descreva brevemente a situação informada.",
            )

        valor = {
            "codigos": codigos,
            "datas": datas,
            "detalhes": detalhes,
        }

        # Segurança e inflamação alteram o prazo do bloco de estética.
        for campo in ("seguranca", "inflamacao"):
            if campo not in self.fields:
                continue

            resposta_extra = dados.get(campo) or ""
            marcou_procedimento = bool(
                set(codigos) - {"NENHUM", "NENHUMA", "NAO"}
            )
            if marcou_procedimento and not resposta_extra:
                self.add_error(
                    campo,
                    "Informe esta condição para o procedimento selecionado.",
                )
            valor[campo] = resposta_extra

        dados["valor"] = valor
        return dados
``````

## Leitura por partes

Os trechos abaixo são os blocos do arquivo na ordem original. Dentro de cada trecho, a explicação segue também os blocos internos de função, condição, repetição e tratamento de erros. Nível indica profundidade, não ordem de execução entre caminhos alternativos.

### Expr — linhas 17 a 17

```python
"""Formulário dinâmico usado por todas as perguntas da triagem."""
```

**Explicação deste trecho:**

**Linha 17 — Expr** (nível 0 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

### ImportFrom — linhas 19 a 19

```python
from datetime import date
```

**Explicação deste trecho:**

**Linha 19 — ImportFrom** (nível 0 do bloco).

Importa de `datetime` os nomes `date`. Pontos iniciais indicam importação relativa ao pacote.

### ImportFrom — linhas 21 a 21

```python
from django import forms
```

**Explicação deste trecho:**

**Linha 21 — ImportFrom** (nível 0 do bloco).

Importa de `django` os nomes `forms`. Pontos iniciais indicam importação relativa ao pacote.

### FormularioPergunta — linhas 24 a 177

```python
class FormularioPergunta(forms.Form):
    """Cria somente os campos necessários para uma pergunta do catálogo."""

    def __init__(self, pergunta, *args, **kwargs):
        self.pergunta = pergunta
        valor_inicial = kwargs.pop("valor_inicial", None) or {}
        super().__init__(*args, **kwargs)

        escolhas = [
            (opcao["codigo"], opcao["rotulo"])
            for opcao in pergunta["opcoes"]
        ]
        codigos_iniciais = valor_inicial.get("codigos") or []

        if pergunta["multipla"]:
            self.fields["resposta"] = forms.MultipleChoiceField(
                label=pergunta["texto"],
                choices=escolhas,
                widget=forms.CheckboxSelectMultiple,
                initial=codigos_iniciais,
            )
        else:
            self.fields["resposta"] = forms.ChoiceField(
                label=pergunta["texto"],
                choices=escolhas,
                widget=forms.RadioSelect,
                initial=(codigos_iniciais[0] if codigos_iniciais else None),
            )

        # Cada alternativa temporal recebe sua própria data.
        datas_iniciais = valor_inicial.get("datas") or {}
        rotulos = {
            opcao["codigo"]: opcao["rotulo"]
            for opcao in pergunta["opcoes"]
        }
        for codigo in pergunta["exige_data_para"]:
            self.fields[f"data_{codigo}"] = forms.DateField(
                label=f"Data relacionada a: {rotulos[codigo]}",
                required=False,
                initial=datas_iniciais.get(codigo),
                widget=forms.DateInput(attrs={"type": "date"}),
            )

        # O complemento permite explicar motivo, tratamento ou exceção.
        self.fields["detalhes"] = forms.CharField(
            label="Informações complementares",
            required=False,
            max_length=500,
            initial=valor_inicial.get("detalhes", ""),
            help_text=(
                "Informe somente o necessário para esclarecer esta resposta."
            ),
            widget=forms.Textarea(attrs={"rows": 3}),
        )

        if pergunta["perguntar_seguranca"]:
            self.fields["seguranca"] = forms.ChoiceField(
                label="As condições de higiene, antissepsia e material eram seguras?",
                required=False,
                choices=[
                    ("", "Selecione"),
                    ("SIM", "Sim."),
                    ("NAO", "Não."),
                    ("NAO_SEI", "Não sei confirmar."),
                ],
                initial=valor_inicial.get("seguranca", ""),
            )

        if pergunta["perguntar_inflamacao"]:
            self.fields["inflamacao"] = forms.ChoiceField(
                label="Houve inflamação ou infecção depois do procedimento?",
                required=False,
                choices=[
                    ("", "Selecione"),
                    ("SIM", "Sim."),
                    ("NAO", "Não."),
                    ("NAO_SEI", "Não sei."),
                ],
                initial=valor_inicial.get("inflamacao", ""),
            )

    def clean(self):
        """Valida contradições e devolve um valor único para persistência."""

        dados = super().clean()
        resposta = dados.get("resposta")

        if self.pergunta["multipla"]:
            codigos = list(resposta or [])
        else:
            codigos = [resposta] if resposta else []

        # Alternativas negativas ou neutras não podem coexistir com doenças.
        exclusivos = {"NAO", "NENHUMA", "NENHUM", "SIM"}
        if len(codigos) > 1 and exclusivos.intersection(codigos):
            self.add_error(
                "resposta",
                "Escolha a alternativa neutra sozinha ou marque as condições.",
            )

        datas = {}
        for codigo in self.pergunta["exige_data_para"]:
            nome_campo = f"data_{codigo}"
            data_evento = dados.get(nome_campo)

            if codigo in codigos and not data_evento:
                self.add_error(
                    nome_campo,
                    "Informe a data desta alternativa.",
                )
            elif data_evento and data_evento > date.today():
                self.add_error(
                    nome_campo,
                    "A data não pode estar no futuro.",
                )
            elif codigo in codigos and data_evento:
                datas[codigo] = data_evento.isoformat()

        detalhes = (dados.get("detalhes") or "").strip()
        if (
            set(codigos).intersection(
                self.pergunta["exige_detalhes_para"]
            )
            and not detalhes
        ):
            self.add_error(
                "detalhes",
                "Descreva brevemente a situação informada.",
            )

        valor = {
            "codigos": codigos,
            "datas": datas,
            "detalhes": detalhes,
        }

        # Segurança e inflamação alteram o prazo do bloco de estética.
        for campo in ("seguranca", "inflamacao"):
            if campo not in self.fields:
                continue

            resposta_extra = dados.get(campo) or ""
            marcou_procedimento = bool(
                set(codigos) - {"NENHUM", "NENHUMA", "NAO"}
            )
            if marcou_procedimento and not resposta_extra:
                self.add_error(
                    campo,
                    "Informe esta condição para o procedimento selecionado.",
                )
            valor[campo] = resposta_extra

        dados["valor"] = valor
        return dados
```

**Explicação deste trecho:**

**Linha 24 — ClassDef** (nível 0 do bloco).

Define a classe `FormularioPergunta` herdando de `forms.Form`. Atributos ficam no corpo; métodos representam operações das instâncias ou da classe.

Bloco `body` da linha 24:

**Linha 25 — Expr** (nível 1 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 27 — FunctionDef** (nível 1 do bloco).

Define `__init__(self, pergunta, *args, **kwargs)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 27:

**Linha 28 — Assign** (nível 2 do bloco).

Associa `self.pergunta` a o valor associado ao nome `pergunta`.

**Linha 29 — Assign** (nível 2 do bloco).

Associa `valor_inicial` a pelo menos uma das condições: `kwargs.pop('valor_inicial', None)` ; `{}` (com avaliação interrompida assim que o resultado é determinado).

**Linha 30 — Expr** (nível 2 do bloco).

Executa a chamada `super().__init__`; argumentos posicionais: `*args`; argumentos nomeados: `**=kwargs`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 32 — Assign** (nível 2 do bloco).

Associa `escolhas` a uma coleção/gerador construído por compreensão em `[(opcao['codigo'], opcao['rotulo']) for opcao in pergunta['opcoes']]`: percorre as fontes e aplica os filtros declarados.

**Linha 36 — Assign** (nível 2 do bloco).

Associa `codigos_iniciais` a pelo menos uma das condições: `valor_inicial.get('codigos')` ; `[]` (com avaliação interrompida assim que o resultado é determinado).

**Linha 38 — If** (nível 2 do bloco).

Escolhe um caminho verificando o item ou recorte `'multipla'` de `pergunta`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 38:

**Linha 39 — Assign** (nível 3 do bloco).

Associa `self.fields['resposta']` a a chamada `forms.MultipleChoiceField`; argumentos nomeados: `label=pergunta['texto']`, `choices=escolhas`, `widget=forms.CheckboxSelectMultiple`, `initial=codigos_iniciais`.

- `label=pergunta['texto']`: texto apresentado ao usuário.
- `choices=escolhas`: alternativas declaradas para validação e apresentação.
- `widget=forms.CheckboxSelectMultiple`: componente de entrada utilizado na tela.
- `initial=codigos_iniciais`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

Bloco `orelse` da linha 38:

**Linha 46 — Assign** (nível 3 do bloco).

Associa `self.fields['resposta']` a a chamada `forms.ChoiceField`; argumentos nomeados: `label=pergunta['texto']`, `choices=escolhas`, `widget=forms.RadioSelect`, `initial=codigos_iniciais[0] if codigos_iniciais else None`.

- `label=pergunta['texto']`: texto apresentado ao usuário.
- `choices=escolhas`: alternativas declaradas para validação e apresentação.
- `widget=forms.RadioSelect`: componente de entrada utilizado na tela.
- `initial=codigos_iniciais[0] if codigos_iniciais else None`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 54 — Assign** (nível 2 do bloco).

Associa `datas_iniciais` a pelo menos uma das condições: `valor_inicial.get('datas')` ; `{}` (com avaliação interrompida assim que o resultado é determinado).

**Linha 55 — Assign** (nível 2 do bloco).

Associa `rotulos` a uma coleção/gerador construído por compreensão em `{opcao['codigo']: opcao['rotulo'] for opcao in pergunta['opcoes']}`: percorre as fontes e aplica os filtros declarados.

**Linha 59 — For** (nível 2 do bloco).

Percorre `pergunta['exige_data_para']`; cada item é atribuído a `codigo` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 59:

**Linha 60 — Assign** (nível 3 do bloco).

Associa `self.fields[f'data_{codigo}']` a a chamada `forms.DateField`; argumentos nomeados: `label=f'Data relacionada a: {rotulos[codigo]}'`, `required=False`, `initial=datas_iniciais.get(codigo)`, `widget=forms.DateInput(attrs={'type': 'date'})`.

- `label=f'Data relacionada a: {rotulos[codigo]}'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `initial=datas_iniciais.get(codigo)`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `widget=forms.DateInput(attrs={'type': 'date'})`: componente de entrada utilizado na tela.

**Linha 68 — Assign** (nível 2 do bloco).

Associa `self.fields['detalhes']` a a chamada `forms.CharField`; argumentos nomeados: `label='Informações complementares'`, `required=False`, `max_length=500`, `initial=valor_inicial.get('detalhes', '')`, `help_text='Informe somente o necessário para esclarecer esta resposta.'`, `widget=forms.Textarea(attrs={'rows': 3})`.

- `label='Informações complementares'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `max_length=500`: limite de comprimento do campo.
- `initial=valor_inicial.get('detalhes', '')`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.
- `help_text='Informe somente o necessário para esclarecer esta resposta.'`: orientação apresentada junto ao campo.
- `widget=forms.Textarea(attrs={'rows': 3})`: componente de entrada utilizado na tela.

**Linha 79 — If** (nível 2 do bloco).

Escolhe um caminho verificando o item ou recorte `'perguntar_seguranca'` de `pergunta`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 79:

**Linha 80 — Assign** (nível 3 do bloco).

Associa `self.fields['seguranca']` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='As condições de higiene, antissepsia e material eram seguras?'`, `required=False`, `choices=[('', 'Selecione'), ('SIM', 'Sim.'), ('NAO', 'Não.'), ('NAO_SEI', 'Não sei confirmar.')]`, `initial=valor_inicial.get('seguranca', '')`.

- `label='As condições de higiene, antissepsia e material eram seguras?'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `choices=[('', 'Selecione'), ('SIM', 'Sim.'), ('NAO', 'Não.'), ('NAO_SEI', 'Não sei confirmar.')]`: alternativas declaradas para validação e apresentação.
- `initial=valor_inicial.get('seguranca', '')`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 92 — If** (nível 2 do bloco).

Escolhe um caminho verificando o item ou recorte `'perguntar_inflamacao'` de `pergunta`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 92:

**Linha 93 — Assign** (nível 3 do bloco).

Associa `self.fields['inflamacao']` a a chamada `forms.ChoiceField`; argumentos nomeados: `label='Houve inflamação ou infecção depois do procedimento?'`, `required=False`, `choices=[('', 'Selecione'), ('SIM', 'Sim.'), ('NAO', 'Não.'), ('NAO_SEI', 'Não sei.')]`, `initial=valor_inicial.get('inflamacao', '')`.

- `label='Houve inflamação ou infecção depois do procedimento?'`: texto apresentado ao usuário.
- `required=False`: indica se o formulário exige preenchimento.
- `choices=[('', 'Selecione'), ('SIM', 'Sim.'), ('NAO', 'Não.'), ('NAO_SEI', 'Não sei.')]`: alternativas declaradas para validação e apresentação.
- `initial=valor_inicial.get('inflamacao', '')`: parâmetro nomeado passado à chamada; seu significado depende da função chamada.

**Linha 105 — FunctionDef** (nível 1 do bloco).

Define `clean(self)`. O corpo só executa quando a função/método é chamado.

Bloco `body` da linha 105:

**Linha 106 — Expr** (nível 2 do bloco).

Texto de documentação quando é o primeiro item do módulo/classe/função; não é uma regra executada nem prova de implementação.

**Linha 108 — Assign** (nível 2 do bloco).

Associa `dados` a a chamada `super().clean`.


**Linha 109 — Assign** (nível 2 do bloco).

Associa `resposta` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `'resposta'`.


**Linha 111 — If** (nível 2 do bloco).

Escolhe um caminho verificando o item ou recorte `'multipla'` de `self.pergunta`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 111:

**Linha 112 — Assign** (nível 3 do bloco).

Associa `codigos` a a chamada `list`; argumentos posicionais: `resposta or []`.


Bloco `orelse` da linha 111:

**Linha 114 — Assign** (nível 3 do bloco).

Associa `codigos` a `[resposta]` se `resposta` for verdadeiro; caso contrário, `[]`.

**Linha 117 — Assign** (nível 2 do bloco).

Associa `exclusivos` a uma coleção Set com 4 itens, na expressão `{'NAO', 'NENHUMA', 'NENHUM', 'SIM'}`.

**Linha 118 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `len(codigos) > 1` ; `exclusivos.intersection(codigos)` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 118:

**Linha 119 — Expr** (nível 3 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `'resposta'`, `'Escolha a alternativa neutra sozinha ou marque as condições.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 124 — Assign** (nível 2 do bloco).

Associa `datas` a um dicionário de 0 entradas; as chaves dão nome aos valores associados.


**Linha 125 — For** (nível 2 do bloco).

Percorre `self.pergunta['exige_data_para']`; cada item é atribuído a `codigo` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 125:

**Linha 126 — Assign** (nível 3 do bloco).

Associa `nome_campo` a o texto formatado `f'data_{codigo}'`, inserindo valores nas partes entre chaves.

**Linha 127 — Assign** (nível 3 do bloco).

Associa `data_evento` a a chamada `dados.get`, que obtém um item; no ORM exige exatamente um resultado, mas em dicionários lê uma chave; argumentos posicionais: `nome_campo`.


**Linha 129 — If** (nível 3 do bloco).

Escolhe um caminho verificando todas as condições: `codigo in codigos` ; `not data_evento` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 129:

**Linha 130 — Expr** (nível 4 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `nome_campo`, `'Informe a data desta alternativa.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 129:

**Linha 134 — If** (nível 4 do bloco).

Escolhe um caminho verificando todas as condições: `data_evento` ; `data_evento > date.today()` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 134:

**Linha 135 — Expr** (nível 5 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `nome_campo`, `'A data não pode estar no futuro.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

Bloco `orelse` da linha 134:

**Linha 139 — If** (nível 5 do bloco).

Escolhe um caminho verificando todas as condições: `codigo in codigos` ; `data_evento` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 139:

**Linha 140 — Assign** (nível 6 do bloco).

Associa `datas[codigo]` a a chamada `data_evento.isoformat`.


**Linha 142 — Assign** (nível 2 do bloco).

Associa `detalhes` a a chamada `(dados.get('detalhes') or '').strip`, que remove espaços nas extremidades do texto.


**Linha 143 — If** (nível 2 do bloco).

Escolhe um caminho verificando todas as condições: `set(codigos).intersection(self.pergunta['exige_detalhes_para'])` ; `not detalhes` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 143:

**Linha 149 — Expr** (nível 3 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `'detalhes'`, `'Descreva brevemente a situação informada.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 154 — Assign** (nível 2 do bloco).

Associa `valor` a um dicionário de 3 entradas; as chaves dão nome aos valores associados.

- Chave `'codigos'`: recebe o valor associado ao nome `codigos`.
- Chave `'datas'`: recebe o valor associado ao nome `datas`.
- Chave `'detalhes'`: recebe o valor associado ao nome `detalhes`.

**Linha 161 — For** (nível 2 do bloco).

Percorre `('seguranca', 'inflamacao')`; cada item é atribuído a `campo` e executa o corpo. Um else de laço executa quando termina sem break.

Bloco `body` da linha 161:

**Linha 162 — If** (nível 3 do bloco).

Escolhe um caminho verificando a comparação `campo` não contido em `self.fields`. Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 162:

**Linha 163 — Continue** (nível 4 do bloco).

Pula o restante da iteração atual e segue para o próximo item do laço.

**Linha 165 — Assign** (nível 3 do bloco).

Associa `resposta_extra` a pelo menos uma das condições: `dados.get(campo)` ; `''` (com avaliação interrompida assim que o resultado é determinado).

**Linha 166 — Assign** (nível 3 do bloco).

Associa `marcou_procedimento` a a chamada `bool`; argumentos posicionais: `set(codigos) - {'NENHUM', 'NENHUMA', 'NAO'}`.


**Linha 169 — If** (nível 3 do bloco).

Escolhe um caminho verificando todas as condições: `marcou_procedimento` ; `not resposta_extra` (com avaliação interrompida assim que o resultado é determinado). Se verdadeiro, executa o bloco principal; caso contrário, passa ao bloco alternativo quando existe.

Bloco `body` da linha 169:

**Linha 170 — Expr** (nível 4 do bloco).

Executa a chamada `self.add_error`; argumentos posicionais: `campo`, `'Informe esta condição para o procedimento selecionado.'`. Não há atribuição explícita nesta instrução; verifique os efeitos da chamada.

**Linha 174 — Assign** (nível 3 do bloco).

Associa `valor[campo]` a o valor associado ao nome `resposta_extra`.

**Linha 176 — Assign** (nível 2 do bloco).

Associa `dados['valor']` a o valor associado ao nome `valor`.

**Linha 177 — Return** (nível 2 do bloco).

Encerra esta chamada e devolve o valor associado ao nome `dados` ao chamador.

## Comentários

Comentários não executam. Descrevem intenção ou contexto; podem estar desatualizados.

- Linha 1: `# Este arquivo cria dinamicamente o formulário de cada pergunta da triagem.`
- Linha 3: `# - Recebe uma pergunta do catálogo e monta os campos necessários.`
- Linha 4: `# - Usa rádio para respostas únicas e checkbox para múltiplas respostas.`
- Linha 5: `# - Reaproveita respostas anteriores quando a pergunta está sendo editada.`
- Linha 6: `# - Cria campos de data para alternativas que exigem prazo.`
- Linha 7: `# - Permite informar detalhes complementares.`
- Linha 8: `# - Adiciona campos extras para segurança e inflamação quando necessários.`
- Linha 9: `# - Impede combinações inválidas, como marcar "Nenhuma" junto com uma doença.`
- Linha 10: `# - Exige datas e detalhes quando a alternativa selecionada precisar dessas informações.`
- Linha 11: `# - Impede datas futuras.`
- Linha 12: `# - Valida as condições de procedimentos e informações de segurança.`
- Linha 13: `# - Organiza tudo no campo "valor", contendo códigos, datas, detalhes e dados complementares, para ser salvo pela camada de serviço.`
- Linha 15: `# Este arquivo valida e organiza as respostas, mas não calcula o resultado médico da triagem. Essa responsabilidade pertence ao triagem_motor.py.`
- Linha 53: `# Cada alternativa temporal recebe sua própria data.`
- Linha 67: `# O complemento permite explicar motivo, tratamento ou exceção.`
- Linha 116: `# Alternativas negativas ou neutras não podem coexistir com doenças.`
- Linha 160: `# Segurança e inflamação alteram o prazo do bloco de estética.`

