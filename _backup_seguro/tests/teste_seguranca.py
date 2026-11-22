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
# SCRIPT DE TESTE DE SEGURANÇA (CORRIGIDO)
# =====================================================================

from security.input_sanitizer import InputSanitizer
from database.db_manager import DBManager
# Importe aqui a sua classe de memória real, por exemplo:
# from security.memoria import instancia_memoria 

def rodar_testes():
    print("==================================================")
    print(" INICIANDO BATERIA DE TESTES DE SEGURANÇA")
    print("==================================================")

    # 1. TESTE DE SANITIZAÇÃO DE ENTRADA
    entrada_suja = "SCANNER_001; DROP TABLE permissao;--"
    entrada_limpa = InputSanitizer.limpar_string(entrada_suja)
    print(f"[TESTE 1] Sanitização de Entrada:")
    print(f"  - Entrada Original: {entrada_suja}")
    print(f"  - Entrada Limpa:    {entrada_limpa}")
    
    if ";" not in entrada_limpa and "--" not in entrada_limpa:
        print("  -> STATUS: PASSOU (Injeção neutralizada com sucesso)\n")
    else:
        print("  -> STATUS: FALHOU\n")

    # 2. TESTE DE RBAC (BANCO DE DADOS)
    scanner_autorizado = "THIERRY_ADMIN"
    scanner_nao_autorizado = "HACKER_INVASOR_999"

    liberado_adm = DBManager.verificar_permissao(scanner_autorizado)
    liberado_hacker = DBManager.verificar_permissao(scanner_nao_autorizado)

    print(f"[TESTE 2] Controle de Acesso (RBAC):")
    print(f"  - Scanner Admin ('{scanner_autorizado}'): {'LIBERADO' if liberado_adm else 'BLOQUEADO'}")
    print(f"  - Scanner Desconhecido ('{scanner_nao_autorizado}'): {'LIBERADO' if liberado_hacker else 'BLOQUEADO'}")

    if liberado_adm and not liberado_hacker:
        print("  -> STATUS: PASSOU (RBAC isolando acessos corretamente)\n")
    else:
        print("  -> STATUS: FALHOU\n")

    print("==================================================")
    print(" BATERIA DE TESTES FINALIZADA COM SUCESSO.")
    print("==================================================")

if __name__ == "__main__":
    rodar_testes()