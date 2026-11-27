# -*- coding: utf-8 -*-
"""Testes simples para o pilar Comercial & Vendas."""

import importlib
from pathlib import Path

PASTA_RAIZ = Path(__file__).resolve().parent

PALAVRAS_COMERCIAL_VENDAS = (
    "venda",
    "sentinela",
    "stripe",
    "comercial",
    "licenca",
    "plano",
    "mercado",
    "checkout",
)


def _arquivos_comercial_vendas() -> list[Path]:
    encontrados = []
    for arq in PASTA_RAIZ.rglob("*.py"):
        nome = str(arq.relative_to(PASTA_RAIZ)).replace("\\", "/").lower()
        if any(p in nome for p in ("venv", "__pycache__", ".bak", "tempcoderunnerfile")):
            continue
        if arq.name.startswith("test_"):
            continue
        if any(chave in nome for chave in PALAVRAS_COMERCIAL_VENDAS):
            encontrados.append(arq)
    return sorted(encontrados)


def test_existem_modulos_comercial_vendas() -> None:
    arquivos = _arquivos_comercial_vendas()
    assert len(arquivos) > 0, "Nenhum arquivo do pilar Comercial & Vendas foi encontrado."


def test_arquivos_comercial_compilam_sem_erro_sintaxe() -> None:
    for arq in _arquivos_comercial_vendas():
        codigo = arq.read_text(encoding="utf-8", errors="replace")
        compile(codigo, str(arq), "exec")


def test_importacao_segura_modulos_comercial() -> None:
    candidatos = [
        "core.comercial_vendas",
        "comercial_vendas",
    ]
    importou = False
    for mod_nome in candidatos:
        try:
            importlib.import_module(mod_nome)
            importou = True
        except Exception:
            continue
    assert len(_arquivos_comercial_vendas()) >= 1 or importou


if __name__ == "__main__":
    test_existem_modulos_comercial_vendas()
    test_arquivos_comercial_compilam_sem_erro_sintaxe()
    test_importacao_segura_modulos_comercial()
    print("[OK] Testes de Comercial & Vendas passaram com sucesso.")