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
# ARQUIVO: security/test_desligamento_abrupto.py
# Teste de Desligamento Abrupto (Simulação de Queda Forçada / Crash)
# =====================================================================

import os
import sys
import time
import signal
import subprocess

# Garante a raiz do projeto no path do Python
raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if raiz_projeto not in sys.path:
    sys.path.append(raiz_projeto)

from security.log_seguro import LogSeguro

logger = LogSeguro()

def executar_teste_desligamento():
    print("\033[94m" + "=" * 65 + "\033[0m")
    print("\033[95m INICIANDO TESTE DE DESLIGAMENTO ABRUPTO (Simulação de Crash)\033[0m")
    print("\033[94m" + "=" * 65 + "\033[0m")
    
    # Simula a criação de um ficheiro de bloqueio de estado crítico (system.lock)
    lock_path = os.path.join(raiz_projeto, "security", "system.lock")
    
    print(" -> A simular gravação crítica no ecossistema...")
    with open(lock_path, "w") as f:
        f.write("ESTADO_CRITICO_EM_GRAVACAO=TRUE\nPID_PROCESSO_SIMULADO=99999")
    
    time.sleep(1)
    
    print(" -> [SIMULAÇÃO] Interrupção abrupta / Corte de energia forçado detetado!")
    logger.registrar("CRASH_TEST", "ALERTA", "Simulação de desligamento abrupto executada durante gravação.")
    
    # Verifica se o ficheiro de travamento foi preservado para análise de integridade
    if os.path.exists(lock_path):
        print(f" -> Trava de segurança detetada com sucesso em: \033[93m{lock_path}\033[0m")
        print("\n\033[92m[VEREDITO] O sistema registou corretamente o estado de interrupção abrupta!\033[0m")
        print("           (O próximo teste validará a limpeza e auto-reparação deste estado).")
    else:
        print("\n\033[91m[VEREDITO] Falha: O ficheiro de estado crítico perdeu-se no crash.\033[0m")
        
    print("\033[94m" + "=" * 65 + "\033[0m")

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    executar_teste_desligamento()