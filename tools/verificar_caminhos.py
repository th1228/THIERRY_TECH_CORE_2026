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

import sys
import os

print(f"Diretório atual: {os.getcwd()}")
print("\nCaminhos de busca do Python (sys.path):")
for path in sys.path:
    print(path)

# Verifica se o arquivo existe na pasta atual
arquivo = "Monaco_nucleo_acesso.py"
if os.path.exists(arquivo):
    print(f"\n[OK] O arquivo {arquivo} foi encontrado na pasta raiz.")
else:
    print(f"\n[ERRO] O arquivo {arquivo} não foi encontrado na pasta raiz.")