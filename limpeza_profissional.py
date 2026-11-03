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

def quarentena_arquivos():
    # Pasta onde jogaremos tudo o que está sobrando
    pasta_lixeira = "_LIXEIRA_SEGURA"
    os.makedirs(pasta_lixeira, exist_ok=True)
    
    # Lista de arquivos que DEVEM ficar na raiz para o sistema rodar
    arquivos_essenciais = [
        'gui_main.py', 'main.py', 'organizador_sistema.py', 
        'sentinela.py', 'limpeza_profissional.py'
    ]
    
    # Pastas que não devemos tocar
    pastas_protegidas = ['core', 'storage', 'laudos', 'ASSETS_MEDIA', '_LIXEIRA_SEGURA', '.git', '.env']

    for item in os.listdir("."):
        # Se for pasta protegida ou arquivo essencial, pula
        if item in arquivos_essenciais or item in pastas_protegidas:
            continue
            
        # Move para a quarentena
        shutil.move(item, os.path.join(pasta_lixeira, item))
        print(f"[QUARENTENA] {item} movido para segurança.")

    print("\n[LIMPEZA] Ambiente limpo. Apenas essenciais na raiz.")

if __name__ == "__main__":
    quarentena_arquivos()