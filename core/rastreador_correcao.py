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

# Lista dos arquivos que o auditor não encontrou
arquivos_faltantes = [
    "dashboard_global.py", "generator.py", "gerador_faturamento.py", 
    "gerenciador_global.py", "motor_biometrico.py", "processador_inteligente.py", 
    "sentinela_fisio.py", "autodestruicao.py", "interface_layout.py"
]

correcao = "import sys, os\nsys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n\n"

# Este script vai procurar em todas as subpastas
for raiz, pastas, arquivos in os.walk("."):
    for nome_arquivo in arquivos:
        if nome_arquivo in arquivos_faltantes:
            caminho_completo = os.path.join(raiz, nome_arquivo)
            with open(caminho_completo, 'r+', encoding='utf-8') as f:
                conteudo = f.read()
                if "sys.path.append" not in conteudo:
                    f.seek(0, 0)
                    f.write(correcao + conteudo)
                    print(f"[SUCESSO] Corrigido em: {caminho_completo}")
                else:
                    print(f"[OK] Já estava corrigido: {caminho_completo}")

print("\n--- Varredura e correção profunda concluídas. Pode dormir! ---")