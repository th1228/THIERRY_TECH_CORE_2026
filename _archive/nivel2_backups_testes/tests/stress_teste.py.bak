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

# --- PONTE DE MEMÓRIA AUTOMÁTICA (THIERRY TECH) ---
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:
        class MemoriaMock:
            def salvar_dados(self, chave, valor): pass
            def registrar(self, chave, valor): pass
            def ler_dados(self, chave): return None
        memoria = MemoriaMock()
# ---------------------------------------------------

import time
import sys
import os

# Adiciona o diretório atual ao path para garantir que o Python encontre os módulos
sys.path.append(os.getcwd())

from security.Ratelimiting import RateLimiting

def simular_ataque():
    print("--- INICIANDO TESTE DE ESTRESSE: RATE LIMITER ---")
    print("Regra: 5 requisições permitidas por janela.\n")
    
    for i in range(1, 11):
        try:
            # Tenta realizar a requisição usando o método estático do seu RateLimiting
            RateLimiting.verificar_vazao(identificador="teste_ataque")
            print(f"Requisição {i}: PERMITIDA ✅")
        except (PermissionError, RuntimeError, ConnectionRefusedError) as e:
            print(f"Requisição {i}: BLOQUEADA PELO RATE LIMITER ❌ ({e})")
        
        # Intervalo curto entre as requisições para estourar o limite
        time.sleep(0.1)

    print("\n--- TESTE FINALIZADO ---")

if __name__ == "__main__":
    simular_ataque()
