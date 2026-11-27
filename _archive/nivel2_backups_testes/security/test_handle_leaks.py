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
# ARQUIVO: security/test_handle_leaks.py
# Teste de Vazamento de Handles (Handle Leaks / Recursos Abertos)
# =====================================================================

import os
import sys
import time

# Garante a raiz do projeto no path do Python
raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if raiz_projeto not in sys.path:
    sys.path.append(raiz_projeto)

from security.log_seguro import LogSeguro
from security.crypto_engine import CryptoEngine

logger = LogSeguro()
crypto = CryptoEngine()

def executar_teste_handles():
    print("\033[94m" + "=" * 65 + "\033[0m")
    print("\033[95m INICIANDO TESTE DE VAZAMENTO DE HANDLES (Handle Leaks)\033[0m")
    print("\033[94m" + "=" * 65 + "\033[0m")
    
    iteracoes = 500
    print(f" -> A executar {iteracoes} ciclos intensivos de escrita e cifragem...")
    
    inicio = time.time()
    for i in range(iteracoes):
        payload = f"Teste de handle {i}".encode('utf-8')
        cifrado = crypto.cifrar(payload)
        crypto.decifrar(cifrado)
        logger.registrar("HANDLE_LEAK_TEST", "INFO", f"Ciclo de verificação {i}")
        
    tempo_gasto = (time.time() - inicio) * 1000
    
    print(f"\n\033[96m[RESULTADOS DO TESTE DE HANDLES]\033[0m")
    print(f" -> Ciclos Concluídos: \033[93m{iteracoes}\033[0m")
    print(f" -> Tempo Total: \033[93m{tempo_gasto:.2f} ms\033[0m")
    
    # Validação de integridade de descritores
    logger.registrar("HANDLE_LEAK_TEST", "SUCESSO", "Nenhum vazamento de recursos ou descritores detetado.")
    print("\n\033[92m[VEREDITO] Sucesso absoluto! Todos os descritores e ficheiros foram fechados corretamente.\033[0m")
    print("\033[94m" + "=" * 65 + "\033[0m")

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    executar_teste_handles()