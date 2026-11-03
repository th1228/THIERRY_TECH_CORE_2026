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

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import shutil

def organizar_definitivamente():
    # Define os destinos
    categorias = {
        'UI': ['.py'], # Vamos ajustar isso no próximo passo para separar o resto
        'CORE_LOGIC': ['biometria', 'scanner', 'analise', 'engine', 'motor', 'seguranca'],
        'STORAGE_DATA': ['.db', '.json', '.sqbpro', '.txt'],
        'LAUDOS_DOCS': ['.pdf', 'Dossie', 'RELATORIO', 'laudo'],
        'ASSETS_MEDIA': ['.jpg', '.png', '.wav']
    }
    
    for pasta in categorias.keys():
        os.makedirs(pasta, exist_ok=True)

    for arquivo in os.listdir("."):
        if arquivo in ["limpeza_profissional.py", "gui_main.py", "organizador_sistema.py", ".git", "__pycache__"] or os.path.isdir(arquivo):
            continue

        movido = False
        # Regra especial: Mover arquivos por categoria
        for pasta, extensao_ou_nome in categorias.items():
            if any(ext in arquivo.lower() for ext in extensao_ou_nome):
                shutil.move(arquivo, os.path.join(pasta, arquivo))
                print(f"[ORGANIZANDO] {arquivo} -> {pasta}/")
                movido = True
                break
        
        if not movido:
            print(f"[IGNORADO] {arquivo}")

if __name__ == "__main__":
    organizar_definitivamente()