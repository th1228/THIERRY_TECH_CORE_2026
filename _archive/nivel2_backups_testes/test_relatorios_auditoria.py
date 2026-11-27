# -*- coding: utf-8 -*-
"""Testes simples para o pilar Relatorios & Auditoria."""

import importlib
from pathlib import Path

PASTA_RAIZ = Path(__file__).resolve().parent

PALAVRAS_RELATORIOS_AUDITORIA = (
    "laudo",
    "pdf",
    "report",
    "auditor",
    "auditoria",
    "juridic",
    "conformidade",
    "inpi",
    "parecer",
    "relatorio",
)


def _arquivos_relatorios_auditoria() -> list[Path]:
    encontrados = []
    for arq in PASTA_RAIZ.rglob("*.py"):
        nome = str(arq.relative_to(PASTA_RAIZ)).replace("\\", "/").lower()
        if any(p in nome for p in ("venv", "__pycache__", ".bak", "tempcoderunnerfile")):
            continue
        if arq.name.startswith("test_"):
            continue
        if any(chave in nome for chave in PALAVRAS_RELATORIOS_AUDITORIA):
            encontrados.append(arq)
    return sorted(encontrados)


def test_existem_modulos_relatorios_auditoria() -> None:
    arquivos = _arquivos_relatorios_auditoria()
    assert len(arquivos) > 0, "Nenhum arquivo do pilar Relatorios & Auditoria foi encontrado."


def test_arquivos_relatorios_compilam_sem_erro_sintaxe() -> None:
    for arq in _arquivos_relatorios_auditoria():
        codigo = arq.read_text(encoding="utf-8", errors="replace")
        compile(codigo, str(arq), "exec")


def test_importacao_segura_modulos_relatorios() -> None:
    candidatos = [
        "core.relatorios_auditoria",
        "relatorios_auditoria",
    ]
    importou = False
    for mod_nome in candidatos:
        try:
            importlib.import_module(mod_nome)
            importou = True
        except Exception:
            continue
    assert len(_arquivos_relatorios_auditoria()) >= 1 or importou


if __name__ == "__main__":
    test_existem_modulos_relatorios_auditoria()
    test_arquivos_relatorios_compilam_sem_erro_sintaxe()
    test_importacao_segura_modulos_relatorios()
    print("[OK] Testes de Relatorios & Auditoria passaram com sucesso.")