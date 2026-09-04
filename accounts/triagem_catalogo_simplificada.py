"""Catálogo da triagem simplificada para quem já concluiu a extensa."""

from .triagem_catalogo_extensa import (
    AVALIACAO,
    PERGUNTAS_EXTENSAS,
    pergunta,
    regra,
)


def pergunta_simplificada(
    id_pergunta,
    titulo,
    texto,
    explicacao,
    opcoes,
    *,
    abrir_extensa=None,
    multipla=False,
    regras=None,
    fonte="Manual Elo, seção 18",
):
    """Monta uma pergunta rápida e registra os aprofundamentos necessários."""

    item = pergunta(
        id_pergunta,
        titulo,
        texto,
        explicacao,
        opcoes,
        multipla=multipla,
        regras=regras,
        fonte=fonte,
    )
    item["abrir_extensa"] = abrir_extensa or {}
    return item


# A lista completa é usada quando a resposta invalida o resumo anterior.
TODAS_AS_EXTENSAS = list(PERGUNTAS_EXTENSAS)


PERGUNTAS_SIMPLIFICADAS = {
    "SIM-01": pergunta_simplificada(
        "SIM-01", "Pode usar a versão rápida?",
        "Você já fez a triagem extensa no Elo e consegue ver um resumo do seu histórico salvo?",
        "A triagem simplificada verifica mudanças e não cria um cadastro médico do zero.",
        [("CORRETO", "Sim, e o resumo continua correto."), ("INCORRETO", "Sim, mas algo antigo está errado/incompleto."), ("NAO_FIZ", "Não fiz a triagem extensa."), ("NAO_SEI", "Não tenho certeza.")],
        abrir_extensa={
            "INCORRETO": TODAS_AS_EXTENSAS,
            "NAO_FIZ": TODAS_AS_EXTENSAS,
            "NAO_SEI": TODAS_AS_EXTENSAS,
        },
        fonte="Manual Elo, seção 18.3; regra de segurança do projeto",
    ),
    "SIM-02": pergunta_simplificada(
        "SIM-02", "Idade, peso e última doação",
        "Desde a última triagem, houve mudança que afete idade, peso ou intervalo de doação?",
        "O intervalo desde a última doação sempre precisa usar dados atuais.",
        [("NAO", "Não; continuo na faixa e peso previstos e não doei desde então."), ("DOOU", "Doei sangue depois da última triagem."), ("PESO", "Meu peso ficou abaixo/próximo de 50 kg ou perdi muito peso."), ("IDADE", "Completei 61 ou 70 anos / mudei de faixa relevante."), ("NAO_SEI", "Não sei.")],
        abrir_extensa={
            "DOOU": ["EXT-04", "EXT-05", "EXT-05A", "EXT-05B"],
            "PESO": ["EXT-03", "EXT-18"],
            "IDADE": ["EXT-02", "EXT-06", "EXT-07"],
            "NAO_SEI": ["EXT-02", "EXT-03", "EXT-04", "EXT-05", "EXT-05A", "EXT-05B", "EXT-06", "EXT-07", "EXT-18"],
        },
        fonte="Manual Elo, seções 3, 4 e 18",
    ),
    "SIM-03": pergunta_simplificada(
        "SIM-03", "Como você está hoje?",
        "Hoje você está se sentindo totalmente bem, sem febre, gripe, COVID, diarreia, infecção ou mal-estar?",
        "Esta é a principal checagem do estado atual.",
        [("SIM", "Sim."), ("NAO", "Não, tive sintoma ou doença recente."), ("NAO_SEI", "Não tenho certeza.")],
        abrir_extensa={
            "NAO": ["EXT-08", "EXT-11", "EXT-11A", "EXT-12", "EXT-13", "EXT-14", "EXT-15", "EXT-16", "EXT-18", "EXT-41"],
            "NAO_SEI": ["EXT-08", "EXT-11", "EXT-11A", "EXT-12", "EXT-13", "EXT-14", "EXT-15", "EXT-16", "EXT-18", "EXT-41"],
        },
        fonte="Manual Elo, seções 3, 6 e 13",
    ),
    "SIM-04": pergunta_simplificada(
        "SIM-04", "Sono, alimentação e álcool",
        "Hoje você dormiu pelo menos quatro horas, não está em jejum e respeitou o intervalo após bebida ou refeição gordurosa?",
        "Esses fatores mudam de um dia para o outro e nunca são reutilizados.",
        [("SIM", "Sim, todas as três condições estão adequadas."), ("SONO", "Não dormi o suficiente."), ("ALIMENTACAO", "Estou em jejum / comi muito recentemente."), ("ALCOOL", "Bebi álcool recentemente."), ("NAO_SEI", "Não sei.")],
        multipla=True,
        abrir_extensa={
            "SONO": ["EXT-09"],
            "ALIMENTACAO": ["EXT-10"],
            "ALCOOL": ["EXT-44"],
            "NAO_SEI": ["EXT-09", "EXT-10", "EXT-44"],
        },
        fonte="Manual Elo, seções 3 e 15.1",
    ),
    "SIM-05": pergunta_simplificada(
        "SIM-05", "Gravidez, pós-parto ou amamentação",
        "Desde a última triagem, houve gravidez, parto, aborto, amamentação ou atraso menstrual com possibilidade de gravidez?",
        "Essas situações possuem prazos diferentes e precisam do bloco completo.",
        [("NAO", "Não."), ("SIM", "Sim."), ("NAO_SEI", "Não sei / prefiro responder na completa.")],
        abrir_extensa={"SIM": ["EXT-33"], "NAO_SEI": ["EXT-33"]},
        fonte="Manual Elo, seção 11.2",
    ),
    "SIM-06": pergunta_simplificada(
        "SIM-06", "Novo diagnóstico ou internação",
        "Desde a última triagem, você recebeu diagnóstico novo, foi internado(a), passou por emergência ou iniciou investigação médica importante?",
        "Uma condição nova pode mudar a orientação mesmo quando você se sente bem.",
        [("NAO", "Não."), ("SIM", "Sim, tive diagnóstico/internação."), ("INVESTIGANDO", "Estou investigando algo e ainda não tenho diagnóstico.")],
        abrir_extensa={
            "SIM": ["EXT-20", "EXT-27", "EXT-28", "EXT-29", "EXT-30", "EXT-31", "EXT-32", "EXT-34", "EXT-35", "EXT-36", "EXT-37", "EXT-38", "EXT-39", "EXT-40", "EXT-46", "EXT-47", "EXT-50"],
            "INVESTIGANDO": ["EXT-20", "EXT-27", "EXT-28", "EXT-29", "EXT-30", "EXT-31", "EXT-32", "EXT-34", "EXT-35", "EXT-36", "EXT-37", "EXT-38", "EXT-39", "EXT-40", "EXT-46", "EXT-47", "EXT-50"],
        },
        regras={"INVESTIGANDO": regra(AVALIACAO, "Uma investigação ainda sem diagnóstico exige avaliação presencial.")},
        fonte="Manual Elo, seções 1.2 e 18",
    ),
    "SIM-07": pergunta_simplificada(
        "SIM-07", "Infecções recentes",
        "Depois da última triagem, você teve COVID, influenza, dengue, chikungunya, Oropouche, mononucleose, hepatite, IST ou outra infecção?",
        "Os prazos variam de dias a impedimento definitivo.",
        [("NAO", "Não."), ("SIM", "Sim."), ("NAO_SEI", "Não sei qual infecção tive.")],
        abrir_extensa={"SIM": ["EXT-12", "EXT-13", "EXT-14", "EXT-41", "EXT-42"], "NAO_SEI": ["EXT-12", "EXT-13", "EXT-14", "EXT-41", "EXT-42"]},
        fonte="Manual Elo, seções 6 e 13",
    ),
    "SIM-08": pergunta_simplificada(
        "SIM-08", "Medicamentos novos ou alterados",
        "Desde a última triagem, você começou, terminou, trocou ou aumentou a dose de algum medicamento?",
        "Nunca interrompa medicamento para tentar doar.",
        [("NAO", "Não."), ("SIM", "Sim."), ("NAO_SEI", "Não sei o nome / não lembro.")],
        abrir_extensa={"SIM": ["EXT-46", "EXT-47"], "NAO_SEI": ["EXT-46", "EXT-47"]},
        regras={"NAO_SEI": regra(AVALIACAO, "O medicamento precisa ser identificado presencialmente.")},
        fonte="Manual Elo, seção 15; refs. [1], [4], [8], [9]",
    ),
    "SIM-09": pergunta_simplificada(
        "SIM-09", "Vacina recente", "Você tomou alguma vacina desde a última triagem?",
        "As vacinas têm prazos diferentes conforme o tipo.",
        [("NAO", "Não."), ("SIM", "Sim."), ("NAO_SEI", "Não lembro / não sei qual vacina.")],
        abrir_extensa={"SIM": ["EXT-48"], "NAO_SEI": ["EXT-48"]},
        regras={"NAO_SEI": regra(AVALIACAO, "Verifique a carteira de vacinação ou confirme presencialmente.")},
        fonte="Manual Elo, seção 16",
    ),
    "SIM-10": pergunta_simplificada(
        "SIM-10", "Tatuagem, piercing, acupuntura ou estética",
        "Desde a última triagem, você fez tatuagem, piercing, acupuntura, microagulhamento, botox, preenchimento ou outro procedimento com perfuração?",
        "O prazo muda conforme tipo, data e segurança.",
        [("NAO", "Não."), ("SIM", "Sim."), ("NAO_SEI", "Não sei se o procedimento conta.")],
        abrir_extensa={"SIM": ["EXT-21", "EXT-22", "EXT-23", "EXT-24"], "NAO_SEI": ["EXT-21", "EXT-22", "EXT-23", "EXT-24"]},
        fonte="Manual Elo, seção 7",
    ),
    "SIM-11": pergunta_simplificada(
        "SIM-11", "Endoscopia, dentista ou cirurgia",
        "Desde a última triagem, você fez endoscopia, tratamento dentário, cirurgia ou outro procedimento médico invasivo?",
        "Cada procedimento tem prazo próprio e pode exigir avaliação da doença que o motivou.",
        [("NAO", "Não."), ("DENTARIO", "Sim, dentário."), ("ENDOSCOPIA", "Sim, endoscopia/laparoscopia."), ("CIRURGIA", "Sim, cirurgia/procedimento médico."), ("NAO_SEI", "Não sei classificar.")],
        abrir_extensa={"DENTARIO": ["EXT-26"], "ENDOSCOPIA": ["EXT-25"], "CIRURGIA": ["EXT-27"], "NAO_SEI": ["EXT-25", "EXT-26", "EXT-27"]},
        fonte="Manual Elo, seções 7 e 8",
    ),
    "SIM-12": pergunta_simplificada(
        "SIM-12", "Feridas, alergia ou reação importante",
        "Hoje você tem ferida aberta/pontos, alergia ativa ou teve anafilaxia/reação grave desde a última triagem?",
        "Esses fatores podem impedir a doação ou exigir avaliação imediata.",
        [("NAO", "Não."), ("FERIDA", "Sim, ferida/pontos."), ("ALERGIA", "Sim, alergia ativa."), ("ANAFILAXIA", "Sim, tive anafilaxia ou reação grave."), ("NAO_SEI", "Não sei.")],
        abrir_extensa={"FERIDA": ["EXT-16"], "ALERGIA": ["EXT-15"], "ANAFILAXIA": ["EXT-15"], "NAO_SEI": ["EXT-15", "EXT-16"]},
        fonte="Manual Elo, seção 6",
    ),
    "SIM-13": pergunta_simplificada(
        "SIM-13", "Exposição a sangue ou situação de risco",
        "Desde a última triagem, aconteceu exposição a sangue/material biológico ou situação sexual/epidemiológica com risco aumentado?",
        "A resposta detalhada será feita em ambiente privado.",
        [("NAO", "Não."), ("SIM", "Sim."), ("PRESENCIAL", "Não quero responder nesta versão rápida / não sei.")],
        abrir_extensa={"SIM": ["EXT-43"]},
        regras={"PRESENCIAL": regra(AVALIACAO, "A situação será discutida em ambiente privado no hemocentro.")},
        fonte="Manual Elo, seção 14; ref. [7]",
    ),
    "SIM-14": pergunta_simplificada(
        "SIM-14", "Drogas", "Desde a última triagem, você usou maconha, cocaína, crack, droga injetável ou outra droga?",
        "A via e a substância mudam a regra.",
        [("NAO", "Não."), ("SIM", "Sim."), ("COMPLETA", "Prefiro responder na versão completa.")],
        abrir_extensa={"SIM": ["EXT-45"], "COMPLETA": ["EXT-45"]},
        fonte="Manual Elo, seção 15.1",
    ),
    "SIM-15": pergunta_simplificada(
        "SIM-15", "Viagem ou mudança de residência",
        "Desde a última triagem, você viajou ou morou em região com malária, chikungunya, Oeste do Nilo ou mudou histórico relevante no exterior?",
        "Áreas de risco podem mudar e precisam de atualização epidemiológica.",
        [("NAO", "Não."), ("SIM", "Sim."), ("NAO_SEI", "Não sei se a região era de risco.")],
        abrir_extensa={"SIM": ["EXT-49"], "NAO_SEI": ["EXT-49"]},
        fonte="Manual Elo, seção 17",
    ),
    "SIM-16": pergunta_simplificada(
        "SIM-16", "Mudança de peso ou saúde geral",
        "Desde a última triagem, você perdeu mais de 10% do peso, ficou desidratado(a) ou percebeu mudança importante na saúde?",
        "Perda importante de peso pode exigir espera ou investigação.",
        [("NAO", "Não."), ("SIM", "Sim."), ("NAO_SEI", "Não sei.")],
        abrir_extensa={"SIM": ["EXT-03", "EXT-11", "EXT-18", "EXT-50"], "NAO_SEI": ["EXT-03", "EXT-11", "EXT-18", "EXT-50"]},
        fonte="Manual Elo, seções 3 e 18",
    ),
    "SIM-17": pergunta_simplificada(
        "SIM-17", "Confirmação rápida",
        "Fora o que já foi perguntado, alguma informação da sua triagem extensa deixou de ser verdadeira ou ficou incompleta?",
        "Esta é uma barreira final contra reutilização indevida de informação antiga.",
        [("NAO", "Não, o restante continua correto."), ("SIM", "Sim."), ("NAO_SEI", "Não tenho certeza.")],
        abrir_extensa={"SIM": TODAS_AS_EXTENSAS, "NAO_SEI": TODAS_AS_EXTENSAS},
        fonte="Manual Elo, seção 18.3; regra de segurança do projeto",
    ),
    "SIM-18": pergunta_simplificada(
        "SIM-18", "Aceite do resultado orientativo",
        "Você entende que a versão rápida pode não detectar algo não informado e que ainda passará pela triagem presencial?",
        "A limitação da modalidade rápida deve ficar explícita.",
        [("ENTENDO", "Sim, entendo."), ("EXTENSA", "Quero fazer a triagem extensa em vez disso.")],
        abrir_extensa={"EXTENSA": TODAS_AS_EXTENSAS},
        fonte="Manual Elo, seções 1 e 18; regra de segurança do projeto",
    ),
}
