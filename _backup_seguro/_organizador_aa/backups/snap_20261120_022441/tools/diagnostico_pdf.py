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

print("=" * 60)
print("🔍 TTC SOBERANO - LOCALIZADOR DE PDF DO BIOGEMENGINE")
print("=" * 60)

# 1. Adiciona a raiz ao path para garantir que importe certo
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# 2. Tenta importar o BiogemEngine
BiogemEngine = None
try:
    from c2_sovereign_intelligence import BiogemEngine
    print("[OK] BiogemEngine importado com sucesso de 'core.biogem_engine'.")
except ImportError:
    try:
        from c2_sovereign_intelligence import BiogemEngine
        print("[OK] BiogemEngine importado com sucesso da raiz.")
    except ImportError:
        print("[AVISO] BiogemEngine não encontrado como módulo separado. O script usará o gerador interno de teste.")

# 3. Verifica o diretório padrão de salvamento
diretorio_destino = os.path.join(os.getcwd(), "static", "results")
os.makedirs(diretorio_destino, exist_ok=True)
print(f"[CAMINHO] A pasta de destino configurada é: {diretorio_destino}")

# 4. Simula a chamada para ver o caminho absoluto que o PDF vai ocupar
nome_teste = "Teste_Localizacao_Cliente"
caminho_esperado = os.path.join(diretorio_destino, f"dossie_{nome_teste}.pdf")
print(f"[CAMINHO] O arquivo PDF será gravado exatamente em:\n    -> {caminho_esperado}")

# 5. Lista todos os PDFs já existentes na pasta results
print("\n[HISTÓRICO] PDFs encontrados atualmente na pasta static/results:")
arquivos_na_pasta = os.listdir(diretorio_destino)
pdfs_existentes = [f for f in arquivos_na_pasta if f.endswith(".pdf")]

if pdfs_existentes:
    for p in pdfs_existentes:
        caminho_completo = os.path.join(diretorio_destino, p)
        tamanho = os.path.getsize(caminho_completo)
        print(f"    - {p} ({tamanho} bytes)")
else:
    print("    - Nenhum arquivo PDF gerado na pasta até o momento.")

print("=" * 60)