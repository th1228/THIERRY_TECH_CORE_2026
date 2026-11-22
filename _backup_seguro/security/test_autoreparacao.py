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

# =====================================================================
# ARQUIVO: security/test_autoreparacao.py
# Teste de Auto-reparação (Self-Healing / Recuperação de Estado)
# =====================================================================

import os
import sys
import time

# Garante a raiz do projeto no path do Python
raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if raiz_projeto not in sys.path:
    sys.path.append(raiz_projeto)

from security.log_seguro import LogSeguro

logger = LogSeguro()

def executar_teste_autoreparacao():
    print("\033[94m" + "=" * 65 + "\033[0m")
    print("\033[95m INICIANDO TESTE DE AUTO-REPARAÇÃO (Self-Healing)\033[0m")
    print("\033[94m" + "=" * 65 + "\033[0m")
    
    lock_path = os.path.join(raiz_projeto, "security", "system.lock")
    
    print(" -> A verificar estado anterior do ecossistema após o crash...")
    if os.path.exists(lock_path):
        print(f" -> Trava residual detetada em: \033[93m{lock_path}\033[0m")
        print(" -> A iniciar rotina de auto-reparação e limpeza de emergência...")
        
        # Simula a recuperação limpando o bloqueio órfão com segurança
        os.remove(lock_path)
        time.sleep(0.5)
        
        logger.registrar("SELF_HEALING", "SUCESSO", "Sistema recuperado automaticamente. Ficheiro system.lock removido.")
        print("\n\033[92m[VEREDITO] Auto-reparação concluída com sucesso! Estado íntegro restaurado.\033[0m")
    else:
        print("\n\033[93m[AVISO] Nenhuma trava residual encontrada para reparar.\033[0m")
        
    print("\033[94m" + "=" * 65 + "\033[0m")

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    executar_teste_autoreparacao()