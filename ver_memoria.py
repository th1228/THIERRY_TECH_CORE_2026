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

# -*- coding: utf-8 -*-
import os
import sys

# Garante que o python encontre o diretório core
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
  from core.memoria_comum import instancia_memoria as memoria

  print("=== [INSPEÇÃO DA MEMÓRIA COMUM // TTC GLOBAL] ===")

  # Tenta puxar os dados principais dependendo de como a sua classe foi estruturada
  if hasattr(memoria, "dados") and isinstance(memoria.dados, dict):
    print(f"Total de chaves na memória: {len(memoria.dados)}")
    for chave, valor in memoria.dados.items():
      print(f" -> [{chave}]: {valor}")
  else:
    # Caso ela use métodos de leitura padrão
    print("Buscando chaves conhecidas no ecossistema:")
    chaves_comuns = [
        "NOME_PACIENTE",
        "CLIENTE_ATUAL",
        "DADOS_CLIENTE",
        "ULTIMA_BIOMETRIA_PROCESSADA",
        "SCANNER_OSTEOMETRIA",
    ]
    for chave in chaves_comuns:
      val = memoria.ler_dados(chave)
      print(f" -> [{chave}]: {val}")

except Exception as e:
  print(f"[ERRO] Não foi possível ler a memória comum: {e}")