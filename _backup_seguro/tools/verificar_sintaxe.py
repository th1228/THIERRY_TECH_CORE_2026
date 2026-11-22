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
import pathlib

print("🔍 A verificar a sintaxe de todos os ficheiros Python do projeto...\n")
erros_encontrados = 0

pastas_ignoradas = {".git", ".venv", "venv", "__pycache__", ".idea", "build", "dist"}

for caminho in pathlib.Path(".").rglob("*.py"):
    if any(ign in caminho.parts for ign in pastas_ignoradas):
        continue
    
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            codigo = f.read()
        # Tenta compilar o código em memória para detetar erros de sintaxe
        compile(codigo, str(caminho), "exec")
    except SyntaxError as e:
        erros_encontrados += 1
        print(f"❌ Erro de sintaxe em: {caminho}")
        print(f"   -> Linha {e.lineno}: {e.msg}")
        print(f"   -> Texto: {e.text.strip() if e.text else 'N/A'}\n")
    except Exception:
        pass

print("=" * 60)
if erros_encontrados == 0:
    print("✅ Parabéns! Nenhum outro erro de sintaxe detetado no projeto.")
else:
    print(f"⚠️ Atenção: Foram encontrados erros em {erros_encontrados} ficheiro(s).")