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
"""
Script de Auditoria Rápida da Memória e do Orquestrador
Sistema: Thierry Technology Concept Global
"""

import os
import sys

# Garante o escopo da raiz
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

try:
    from memoria_comum import instancia_memoria as memoria
    print(" [OK] Módulo 'memoria_comum' importado com sucesso.")
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
        print(" [OK] Módulo 'core.memoria_comum' importado com sucesso.")
    except ImportError:
        print(" [ERRO] Não foi possível importar 'memoria_comum'.")
        memoria = None

def auditar():
    print("=" * 60)
    print(" AUDITORIA DE DADOS E TELEMETRIA DA MEMÓRIA COMUM")
    print("=" * 60)
    
    if not memoria:
        print(" Objeto de memória indisponível.")
        return

    # Tenta ler as chaves mais comuns usadas pelo orquestrador e motores
    chaves_para_testar = [
        "analise_gemini_recente",
        "analise_gemini",
        "telemetria_dinamica",
        "sessao_atual",
        "ultimo_resultado_llm"
    ]

    encontrou_algo = False
    for chave in chaves_para_testar:
        valor = None
        if hasattr(memoria, 'ler_dados'):
            valor = memoria.ler_dados(chave)
        elif hasattr(memoria, 'obter'):
            valor = memoria.obter(chave)
        
        if valor:
            encontrou_algo = True
            print(f" 📂 CHAVE ENCONTRADA: [{chave}]")
            print(f"    Conteúdo: {str(valor)[:300]}...\n")
        else:
            print(f" ⚪ Chave vazia ou inexistente: [{chave}]")

    print("-" * 60)
    if not encontrou_algo:
        print(" ⚠️ NENHUM DADO DINÂMICO FOI ENCONTRADO NA MEMÓRIA.")
        print(" Isso explica por que os PDFs saem iguais: o orquestrador ainda não salvou")
        print(" os dados na memória ou está usando uma chave diferente.")
    else:
        print(" ✅ Dados encontrados! A ponte está funcionando.")
    print("=" * 60)

if __name__ == "__main__":
    auditar()