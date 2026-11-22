# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the 
intellectual property of Thierry Technology Concept Global. Unauthorized 
distribution, reverse engineering, or usage without a signed NDA/License 
agreement is strictly prohibited under international copyright frameworks.
===========================================================================
"""

import os
from pathlib import Path
from datetime import datetime

def varrer_todos_os_pdfs():
    base_dir = Path(__file__).resolve().parent
    print(f"\n==================================================")
    print(f" VARREDURA UNIVERSAL DE PDFS NO PROJETO")
    print(f"==================================================")
    
    # Procura ficheiros PDF em todas as pastas e subpastas do projeto
    pdfs = list(base_dir.rglob("*.pdf"))
    
    if pdfs:
        print(f"\n[SUCESSO] Encontrados {len(pdfs)} relatórios PDF no total:\n")
        
        # Ordenar do mais recente para o mais antigo
        pdfs_ordenados = sorted(pdfs, key=os.path.getmtime, reverse=True)
        
        for i, pdf in enumerate(pdfs_ordenados, 1):
            data_mod = datetime.fromtimestamp(pdf.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            tamanho_kb = round(pdf.stat().st_size / 1024, 2)
            caminho_relativo = pdf.relative_to(base_dir)
            
            print(f"[{i}] Ficheiro: {caminho_relativo}")
            print(f"    Data/Hora: {data_mod}")
            print(f"    Tamanho: {tamanho_kb} KB")
            print(f"    ----------------------------------------------")
    else:
        print(f"\n[!] Nenhum ficheiro PDF foi encontrado nas pastas do projeto.")

if __name__ == "__main__":
    varrer_todos_os_pdfs()