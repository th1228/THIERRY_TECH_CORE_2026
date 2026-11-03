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
from pathlib import Path
import shutil

def organizar_scripts_auditoria():
    print("=" * 65)
    print("ORGANIZADOR SEGURO DE SCRIPTS DE AUDITORIA - TTC GLOBAL")
    print("=" * 65)
    
    raiz = Path(".")
    pasta_destino = raiz / "auditorias_anteriores"
    pasta_destino.mkdir(exist_ok=True)
    
    # Arquivos intocáveis que NUNCA devem ser movidos de jeito nenhum
    arquivos_protegidos = {
        "audit_global_financeiro.py", # O oficial atual que estamos usando
        "app.py",
        "api_server.py",
        "c2_sovereign_intelligence.py",
        "monaco_modelagem_engine.py"
    }
    
    movidos = 0
    
    # Varre a raiz procurando por arquivos que comecem com audit ou auditar
    for arquivo in raiz.iterdir():
        if arquivo.is_file():
            nome_lower = arquivo.name.lower()
            
            # Se for um arquivo protegido, pula imediatamente
            if arquivo.name in arquivos_protegidos:
                print(f"  [PROTEGIDO] Mantido na raiz: {arquivo.name}")
                continue
                
            # Identifica se é um script de auditoria antigo/avulso
            if nome_lower.startswith("audit") or nome_lower.startswith("auditar") or nome_lower.startswith("auditor"):
                destino_final = pasta_destino / arquivo.name
                shutil.move(str(arquivo), str(destino_final))
                print(f"  [MOVIDO] {arquivo.name} -> auditorias_anteriores/")
                movidos += 1

    print("=" * 65)
    print(f"ORGANIZAÇÃO CONCLUÍDA: {movidos} arquivo(s) isolado(s) com segurança.")
    print("=" * 65)

if __name__ == "__main__":
    organizar_scripts_auditoria()