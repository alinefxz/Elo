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
