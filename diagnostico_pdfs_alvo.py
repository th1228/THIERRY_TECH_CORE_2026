# -*- coding: utf-8 -*-
"""
Script diagnóstico rápido:
1. Varre arquivos .py / .json do projeto procurando 'herpes' ou 'simplex'.
2. Lê os PDFs finais de Tricologia e Carta Internacional para ver se a palavra aparece neles.
"""

import glob
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
TERMOS = re.compile(r"\b(?:herpes|simplex)\b", re.IGNORECASE)


def varrer_codigo_e_json() -> None:
    print("=== 1. VARREDURA EM ARQUIVOS .PY E .JSON ===")
    encontrou = False
    for padrao in ("**/*.py", "**/*.json"):
        for caminho in glob.glob(os.path.join(ROOT, padrao), recursive=True):
            if ".bak_" in caminho or "__pycache__" in caminho:
                continue
            try:
                with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                    for num_linha, linha in enumerate(f, start=1):
                        if TERMOS.search(linha):
                            encontrou = True
                            print(f"  [ARQUIVO] {caminho} (linha {num_linha}): {linha.strip()}")
            except Exception as e:
                print(f"  [ERRO LEITURA] {caminho}: {e}")
    if not encontrou:
        print("  -> Nenhuma ocorrência fixa encontrada nos .py/.json (confirma geração dinâmica/LLM/memória).")


def ler_texto_pdf(caminho_pdf: str) -> str:
    if not os.path.isfile(caminho_pdf):
        return ""
    try:
        from pypdf import PdfReader  # type: ignore
        reader = PdfReader(caminho_pdf)
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    except Exception:
        pass

    try:
        import fitz  # type: ignore
        doc = fitz.open(caminho_pdf)
        return "\n".join(page.get_text() for page in doc)
    except Exception:
        pass

    # Fallback simples caso não tenha biblioteca de PDF instalada
    with open(caminho_pdf, "rb") as f:
        bruto = f.read().decode("latin-1", errors="ignore")
    return bruto


def inspecionar_pdfs() -> None:
    print("\n=== 2. INSPEÇÃO DOS PDFs FINAIS (TRICOLOGIA E CARTA) ===")
    alvos = [
        ("Tricologia", os.path.join(ROOT, "pdfs_finais", "03_Dossie_Tricologia_Avancada.pdf")),
        ("Carta Internacional", os.path.join(ROOT, "pdfs_finais", "04_Carta_Internacional_UHNW.pdf")),
    ]
    for nome, caminho in alvos:
        if not os.path.exists(caminho):
            print(f"  [{nome}] Arquivo não encontrado: {caminho}")
            continue
        texto = ler_texto_pdf(caminho)
        matches = TERMOS.findall(texto)
        print(f"  [{nome}] {os.path.basename(caminho)} -> ocorrências de herpes/simplex: {len(matches)}")
        for linha in texto.splitlines():
            if TERMOS.search(linha):
                print(f"     Trecho: {linha.strip()}")


if __name__ == "__main__":
    varrer_codigo_e_json()
    inspecionar_pdfs()