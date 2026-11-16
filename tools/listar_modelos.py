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
from google import genai

API_KEY_REGISTADA = "AQ.Ab8RN6IMGtFG1bmmtrqu_o6mLlkviTwUTkdA2ctfdD3HNqELyQ"
chave_final = os.environ.get("GEMINI_API_KEY", API_KEY_REGISTADA)

client = genai.Client(api_key=chave_final)

print("=" * 60)
print("LISTA COMPLETA DE MODELOS:")
print("=" * 60)

try:
  for m in client.models.list():
    # Imprime o identificador direto do modelo
    print(f"-> {m.name}")
except Exception as e:
  print(f"Erro ao listar: {e}")

print("=" * 60)