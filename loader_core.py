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

# -*- coding: utf-8 -*-
import os
import subprocess

def carregar_core():
    # Define o caminho da pasta core a partir da UI
    pasta_core = os.path.join(os.path.dirname(os.path.dirname(__file__)), "core")
    
    # Lista de arquivos que devem ser carregados da core
    arquivos_core = [
        "biogenio_scanner.py",
        "verificador_nuvem.py",
        "analise_cabelo.py"
    ]
    
    print("--- INICIANDO CARGA DE MÓDULOS CORE ---")
    for arquivo in arquivos_core:
        caminho = os.path.join(pasta_core, arquivo)
        if os.path.exists(caminho):
            print(f">>> Iniciando {arquivo}")
            subprocess.run(["python", caminho])
        else:
            print(f"!!! ERRO: {arquivo} não encontrado em {caminho}")