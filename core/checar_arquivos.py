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

# Lista dos arquivos que o seu projeto está procurando
arquivos_procurados = [
    "voz_perfeita.mp3",
    "voz_perfeita_en.mp3",
    "mapeamento_pt.mp3",
    "mapeamento_en.mp3",
    "camera_click.wav"
]

print(f"📁 Pasta atual de execução: {os.getcwd()}\n")
print("Verificando arquivos...")

for arquivo in arquivos_procurados:
    if os.path.exists(arquivo):
        tamanho = os.path.getsize(arquivo)
        print(f" [ENCONTRADO] {arquivo} (Tamanho: {tamanho} bytes)")
    else:
        print(f"❌ [NÃO ENCONTRADO] {arquivo} - Atenção: O programa vai dar erro 404 para este arquivo!")