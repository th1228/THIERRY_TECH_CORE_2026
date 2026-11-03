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

pasta_core = 'core'
# As linhas que identificam a "ponte" que injetamos
identificador_ponte = "sys.path.insert"

for nome_arquivo in os.listdir(pasta_core):
    if nome_arquivo.endswith('.py') and nome_arquivo != '__init__.py':
        caminho = os.path.join(pasta_core, nome_arquivo)
        
        with open(caminho, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        # Filtra mantendo apenas as linhas que NÃO contêm a nossa "ponte"
        novas_linhas = [l for l in linhas if identificador_ponte not in l]
        
        # Remove também a linha "import sys, os" se ela estiver logo no início (opcional, mas recomendado)
        # Se você quiser ser mais cuidadoso, remova apenas a linha da ponte mesmo.
        
        with open(caminho, 'w', encoding='utf-8') as f:
            f.writelines(novas_linhas)
        
        print(f"[LIMPO] Ponte removida de: {nome_arquivo}")

print("--- Limpeza concluída com sucesso ---")