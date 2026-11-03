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
import sys

# Garante o diretório atual no path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

print("--- INICIANDO TESTE DO GERADOR MASTER ---")
try:
    from core.gerador_dossies_master import compilar_dossies_master
    print("Módulo importado com sucesso!")
    
    # Tenta executar o lote passando o nome do titular
    resultado = compilar_dossies_master(ceo_name="Genilson Rodrigues", operador="Thierry")
    print("Resultado da compilação:", resultado)
    
except Exception as e:
    import traceback
    print("ERRO CRÍTICO CAPTURADO:")
    traceback.print_exc()