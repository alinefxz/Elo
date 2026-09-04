"""Testes que impedem perguntas ou alternativas de desaparecerem do catálogo."""

from django.test import SimpleTestCase

from .triagem_catalogo import (
    PERGUNTAS_EXTENSAS,
    PERGUNTAS_SIMPLIFICADAS,
    todas_as_perguntas,
    validar_catalogos,
)


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

IDS_SIMPLIFICADOS = {
    f"SIM-{numero:02d}"
    for numero in range(1, 19)
}


class CatalogosTriagemTests(SimpleTestCase):
    """Valida a estrutura consumida pelo formulário, serviço e motor."""

    def test_catalogo_extenso_possui_todas_as_55_entradas(self):
        """Falha se qualquer pergunta extensa da especificação for omitida."""

        self.assertEqual(set(PERGUNTAS_EXTENSAS), IDS_EXTENSOS)

    def test_catalogo_simplificado_possui_todas_as_18_entradas(self):
        """Falha se a versão rápida ficar incompleta."""

        self.assertEqual(set(PERGUNTAS_SIMPLIFICADAS), IDS_SIMPLIFICADOS)

    def test_perguntas_possuem_conteudo_e_rastreabilidade(self):
        """Falha se uma pergunta não puder ser exibida ou auditada."""

        for pergunta in todas_as_perguntas():
            self.assertTrue(pergunta["titulo"], pergunta["id"])
            self.assertTrue(pergunta["texto"], pergunta["id"])
            self.assertTrue(pergunta["explicacao"], pergunta["id"])
            self.assertTrue(pergunta["fonte"], pergunta["id"])
            self.assertEqual(
                pergunta["regra_version"],
                "HEMOMINAS_2026_08",
                pergunta["id"],
            )

            if pergunta["tipo"] not in {"data", "numero", "texto"}:
                self.assertTrue(pergunta["opcoes"], pergunta["id"])

    def test_codigos_de_opcao_nao_se_repetem_na_mesma_pergunta(self):
        """Falha se dois rótulos diferentes forem salvos com o mesmo código."""

        for pergunta in todas_as_perguntas():
            codigos = [opcao["codigo"] for opcao in pergunta["opcoes"]]
            self.assertEqual(len(codigos), len(set(codigos)), pergunta["id"])

    def test_destinos_da_simplificada_existem_no_catalogo_extenso(self):
        """Falha se a versão rápida tentar abrir uma pergunta inexistente."""

        for pergunta in PERGUNTAS_SIMPLIFICADAS.values():
            for destinos in pergunta["abrir_extensa"].values():
                for destino in destinos:
                    self.assertIn(destino, PERGUNTAS_EXTENSAS)

    def test_funcao_de_validacao_aceita_os_catalogos_oficiais(self):
        """Falha se o catálogo publicado violar seu próprio contrato."""

        self.assertIsNone(validar_catalogos())
