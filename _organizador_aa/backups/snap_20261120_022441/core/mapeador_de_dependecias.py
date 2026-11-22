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
import re

def mapear_importacoes():
    dependencias = {}
    
    # Lista todos os .py
    arquivos = [f for f in os.listdir('.') if f.endswith('.py')]
    # Adiciona também os da pasta core se existirem
    if os.path.exists('core'):
        for f in os.listdir('core'):
            if f.endswith('.py'):
                arquivos.append(os.path.join('core', f))

    for arquivo in arquivos:
        try:
            with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                conteudo = f.read()
                # Procura por linhas "import X" ou "from X import Y"
                imports = re.findall(r'from\s+([\w\.]+)\s+import|import\s+([\w\.]+)', conteudo)
                # Limpa os resultados
                lista_imports = [i[0] or i[1] for i in imports]
                dependencias[arquivo] = [imp.split('.')[0] for imp in lista_imports if imp]
        except:
            continue

    print(f"{'ARQUIVO (QUEM CHAMA)':<35} | {'IMPORTA (O QUE PRECISA)'}")
    print("-" * 80)
    for arq, deps in dependencias.items():
        if deps:
            print(f"{arq:<35} | {', '.join(set(deps))}")

if __name__ == "__main__":
    mapear_importacoes()