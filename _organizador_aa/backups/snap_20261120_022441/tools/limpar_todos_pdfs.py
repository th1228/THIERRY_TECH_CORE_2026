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

import glob
import os

# Define o caminho para a pasta storage
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_storage = os.path.join(diretorio_atual, "storage")

# Busca por todos os arquivos de dossiê na pasta storage
padrao_busca = os.path.join(caminho_storage, "Dossie_*.pdf")
arquivos_dossie = glob.glob(padrao_busca)

print(f"Encontrados {len(arquivos_dossie)} dossiês antigos na pasta storage.\n")

contador = 0
for arquivo in arquivos_dossie:
  try:
    os.remove(arquivo)
    print(f"[REMOVIDO] {os.path.basename(arquivo)}")
    contador += 1
  except Exception as e:
    print(f"[ERRO] Não foi possível apagar o arquivo: {e}")

print("\n--- LIMPEZA DE DOSSIÊS CONCLUÍDA ---")
print(f"Total de arquivos removidos: {contador}")