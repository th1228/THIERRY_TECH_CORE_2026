# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
Módulo: reparador_pdf_iso.py
Descrição: Restaura e centraliza exclusivamente o Super Retorno Financeiro
           e o Dossiê de Modelagem Computacional em ISO A4 (12mm) sem cortes.
"""

import os
import shutil
import pymupdf as fitz

ALVOS_ESPECIFICOS = [
    "02_Super_Retorno_Financeiro.pdf",
    "05_Dossie_Modelagem_Computacional.pdf",
]


def encontrar_pasta_pdfs(nome_alvo: str = "pdfs_finais") -> str | None:
    base_dir = os.getcwd()
    for raiz, diretorios, _ in os.walk(base_dir):
        for dir_name in diretorios:
            if dir_name.lower() == nome_alvo.lower():
                return os.path.join(raiz, dir_name)

    caminho_direto = os.path.join(base_dir, nome_alvo)
    return caminho_direto if os.path.exists(caminho_direto) else None


def centralizar_sem_corte(caminho_pdf: str, pasta_backup: str) -> bool:
    largura_a4, altura_a4 = 595.28, 841.89
    margem_pt = 12.0 / 0.352778  # 12 mm exatos de respiro nas 4 bordas

    nome_arquivo = os.path.basename(caminho_pdf)
    caminho_backup = os.path.join(pasta_backup, nome_arquivo)
    os.makedirs(pasta_backup, exist_ok=True)

    # Restaura o original intacto do backup antes de centralizar
    if os.path.exists(caminho_backup):
        shutil.copy2(caminho_backup, caminho_pdf)
    else:
        shutil.copy2(caminho_pdf, caminho_backup)

    caminho_temp = caminho_pdf + ".tmp.pdf"
    doc_origem = None
    doc_novo = None

    try:
        doc_origem = fitz.open(caminho_pdf)
        total_paginas = len(doc_origem)
        doc_novo = fitz.open()

        # Garante metadados ISO 14289
        meta = dict(doc_origem.metadata or {})
        if not (meta.get("title") or "").strip():
            nome_sem_ext = os.path.splitext(nome_arquivo)[0]
            meta["title"] = nome_sem_ext.replace("_", " ").strip()
        doc_novo.set_metadata(meta)

        # Caixa centralizada dentro do A4
        area_destino = fitz.Rect(
            margem_pt,
            margem_pt,
            largura_a4 - margem_pt,
            altura_a4 - margem_pt,
        )

        for i in range(total_paginas):
            pag_orig = doc_origem[i]
            # Usa mediabox completo para impedir qualquer corte na margem esquerda
            caixa_real = pag_orig.mediabox

            nova_pagina = doc_novo.new_page(width=largura_a4, height=altura_a4)
            nova_pagina.show_pdf_page(
                area_destino,
                doc_origem,
                i,
                clip=caixa_real,
                keep_proportion=True,
            )

        doc_novo.save(caminho_temp, garbage=4, deflate=True)
        doc_novo.close()
        doc_novo = None
        doc_origem.close()
        doc_origem = None

        doc_teste = fitz.open(caminho_temp)
        integro = len(doc_teste) == total_paginas
        doc_teste.close()

        if integro:
            os.replace(caminho_temp, caminho_pdf)
            return True

        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)
        return False

    except Exception as exc:
        print(f"   └── ❌ Erro ao processar '{nome_arquivo}': {exc}")
        if doc_novo is not None:
            try:
                doc_novo.close()
            except Exception:
                pass
        if doc_origem is not None:
            try:
                doc_origem.close()
            except Exception:
                pass
        if os.path.exists(caminho_temp):
            try:
                os.remove(caminho_temp)
            except Exception:
                pass
        return False


def executar_reparo_cirurgico() -> None:
    pasta = encontrar_pasta_pdfs("pdfs_finais")
    if not pasta:
        print("❌ Pasta 'pdfs_finais' não encontrada.")
        return

    pasta_backup = os.path.join(os.path.dirname(pasta), "_backup_pdfs_originais")

    print("\n" + "=" * 70)
    print(" REPARO CIRÚRGICO ISO A4 - ALVOS ESPECÍFICOS")
    print("=" * 70)

    # Restaura também qualquer outro arquivo do backup caso tenha sido alterado antes
    if os.path.exists(pasta_backup):
        for f_bkp in os.listdir(pasta_backup):
            if f_bkp not in ALVOS_ESPECIFICOS:
                destino = os.path.join(pasta, f_bkp)
                if os.path.exists(destino):
                    shutil.copy2(os.path.join(pasta_backup, f_bkp), destino)
                    print(f"♻️ Original restaurado intacto: {f_bkp}")

    reparados = 0
    for alvo in ALVOS_ESPECIFICOS:
        caminho = os.path.join(pasta, alvo)
        if os.path.exists(caminho):
            print(f"🔧 Centralizando com mediabox completo: {alvo}...")
            if centralizar_sem_corte(caminho, pasta_backup):
                print("   └── ✅ Concluído: Margens de 12mm aplicadas sem cortar texto.")
                reparados += 1
        else:
            print(f"⚠️ Arquivo não encontrado na pasta: {alvo}")

    print("-" * 70)
    print(f"Total de arquivos alvo normalizados: {reparados}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    executar_reparo_cirurgico()