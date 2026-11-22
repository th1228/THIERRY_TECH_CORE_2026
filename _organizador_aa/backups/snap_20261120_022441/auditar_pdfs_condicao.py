# -*- coding: utf-8 -*-
"""
Script: auditar_pdfs_condicao.py
Finalidade: Conferência rápida da condição física, contagem de páginas e
            dimensões (A4 vs. fora do padrão) dos PDFs em pdfs_finais.
"""

import os
from typing import List, Tuple

LARGURA_A4, ALTURA_A4 = 595.28, 841.89
TOLERANCIA_PT = 1.5


def inspecionar_pdf_com_pypdf(caminho: str) -> Tuple[bool, int, List[str], str]:
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError:
        try:
            from PyPDF2 import PdfReader  # type: ignore
        except ImportError:
            return False, 0, [], "Instale 'pypdf' para leitura detalhada de páginas."

    try:
        reader = PdfReader(caminho)
        total_pag = len(reader.pages)
        fora_a4: List[str] = []

        for idx, page in enumerate(reader.pages, start=1):
            w = float(page.mediabox.width)
            h = float(page.mediabox.height)
            ok_w = abs(w - LARGURA_A4) <= TOLERANCIA_PT
            ok_h = abs(h - ALTURA_A4) <= TOLERANCIA_PT
            if not (ok_w and ok_h):
                fora_a4.append(f"p.{idx} ({w:.1f}x{h:.1f} pt)")

        return True, total_pag, fora_a4, "OK"
    except Exception as exc:
        return False, 0, [], f"Falha ao ler PDF: {exc}"


def auditar_pasta_pdfs(pasta_pdfs: str = "pdfs_finais") -> None:
    print("=" * 70)
    print(f"INSPEÇÃO RÁPIDA DE PDFS — PASTA: {os.path.abspath(pasta_pdfs)}")
    print("=" * 70)

    if not os.path.isdir(pasta_pdfs):
        print(f"[AVISO] Pasta '{pasta_pdfs}' não encontrada.")
        return

    arquivos = sorted(f for f in os.listdir(pasta_pdfs) if f.lower().endswith(".pdf"))
    if not arquivos:
        print("[AVISO] Nenhum arquivo .pdf encontrado na pasta.")
        return

    total_ok = 0
    total_fora_a4 = 0

    for nome in arquivos:
        caminho = os.path.join(pasta_pdfs, nome)
        tamanho_kb = os.path.getsize(caminho) / 1024.0
        legivel, pags, fora_a4, status = inspecionar_pdf_com_pypdf(caminho)

        if legivel and pags > 0 and tamanho_kb > 0:
            total_ok += 1
            if not fora_a4:
                print(f"[OK • A4] {nome} | {tamanho_kb:.2f} KB | {pags} pág(s)")
            else:
                total_fora_a4 += len(fora_a4)
                print(
                    f"[ATENÇÃO • NÃO-A4] {nome} | {tamanho_kb:.2f} KB | "
                    f"{pags} pág(s) | Fora do A4: {', '.join(fora_a4)}"
                )
        else:
            print(f"[ERRO] {nome} | {tamanho_kb:.2f} KB | {status}")

    print("-" * 70)
    print(f"Resumo: {total_ok}/{len(arquivos)} PDF(s) íntegros | Páginas fora do A4: {total_fora_a4}")
    print("=" * 70)


if __name__ == "__main__":
    auditar_pasta_pdfs()