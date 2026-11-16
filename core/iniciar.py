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

import sys
import os

# Correção automática de caminho
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from monaco_integrador import MonacoIntegrador

def executar_sistema():
    print("--- INICIANDO SISTEMA MONACO ---")
    try:
        sistema = MonacoIntegrador()
        print(sistema.processar())
    except (ConnectionError, TimeoutError, OSError, ValueError, KeyError, RuntimeError) as e:
        print(f"Erro ao iniciar motor: {e}")
    print("--- SISTEMA OPERACIONAL ---")

if __name__ == "__main__":
    executar_sistema()
