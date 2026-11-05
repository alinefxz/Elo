"""Normaliza a resposta oficial do IBGE sem produzir catálogos incompletos.

Entrada: tmp/municipios_ibge_original.json, baixado de FONTE.
Saída: accounts/data/municipios_ibge.json, sem acesso de rede em runtime.
Executar da raiz: python scripts/importar_municipios_ibge.py
"""

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


FONTE = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios?orderBy=nome"
UFS = frozenset("AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split())
RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "tmp" / "municipios_ibge_original.json"
SAIDA = RAIZ / "accounts" / "data" / "municipios_ibge.json"


def uf_municipio(item):
    antiga = ((item.get("microrregiao") or {}).get("mesorregiao") or {}).get("UF") or {}
    atual = ((item.get("regiao-imediata") or {}).get("regiao-intermediaria") or {}).get("UF") or {}
    return antiga.get("sigla") or atual.get("sigla")


def main():
    if not ENTRADA.is_file():
        raise SystemExit(f"Resposta oficial ausente: {ENTRADA}. Baixe a API do IBGE antes de normalizar.")
    try:
        registros = json.loads(ENTRADA.read_text(encoding="utf-8-sig"))
    except (ValueError, UnicodeError) as erro:
        raise SystemExit(f"Resposta do IBGE não é JSON UTF-8 válido: {erro}") from erro
    if not isinstance(registros, list):
        raise SystemExit("Resposta do IBGE deve ser uma lista de municípios; nenhum catálogo foi gravado.")

    por_uf = defaultdict(list)
    ids = set()
    duplicados = []
    sem_uf = []
    for item in registros:
        if not isinstance(item, dict) or not item.get("id") or not isinstance(item.get("nome"), str):
            raise SystemExit("Registro municipal inválido na resposta oficial; nenhum catálogo foi gravado.")
        uf = uf_municipio(item)
        nome = item["nome"].strip()
        if uf not in UFS:
            sem_uf.append({"id": item["id"], "nome": nome, "uf": uf})
        if item["id"] in ids or nome in por_uf[uf]:
            duplicados.append({"id": item["id"], "nome": nome, "uf": uf})
        ids.add(item["id"])
        por_uf[uf].append(nome)

    if sem_uf or duplicados or set(por_uf) != UFS or len(ids) < 5500:
        raise SystemExit(json.dumps({
            "erro": "Catálogo incompleto ou inconsistente; arquivo final não foi alterado.",
            "total": len(registros), "ufs": len(por_uf),
            "ufs_ausentes": sorted(UFS - set(por_uf)),
            "sem_uf": sem_uf, "duplicados": duplicados,
        }, ensure_ascii=False))

    por_uf = {uf: sorted(por_uf[uf], key=str.casefold) for uf in sorted(UFS)}
    documento = {
        "fonte": FONTE,
        "consultado_em": datetime.fromtimestamp(ENTRADA.stat().st_mtime, timezone.utc).isoformat(),
        "municipios_por_estado": por_uf,
    }
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    temporario = SAIDA.with_suffix(".tmp")
    temporario.write_text(json.dumps(documento, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporario.replace(SAIDA)
    print(json.dumps({
        "total_municipios": len(registros), "ufs": len(por_uf),
        "municipios_sem_uf": len(sem_uf), "duplicados_mesma_uf_ou_id": len(duplicados),
        "nomes_distintos": len({nome for nomes in por_uf.values() for nome in nomes}),
        "contagem_por_uf": {uf: len(nomes) for uf, nomes in por_uf.items()},
        "fonte": FONTE, "consultado_em": documento["consultado_em"], "arquivo": str(SAIDA),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
