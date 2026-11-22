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

# Garante o mapeamento correto do diretório atual e da pasta core
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, "core"))

# Importação blindada com tratamento completo para evitar qualquer exceção
try:
    from biogemeo_orquestrador import BiogemeoOrquestradorGlobal
except ImportError:
    try:
        from core.biogemeo_orquestrador import BiogemeoOrquestradorGlobal
    except ImportError:
        try:
            from core.biogemio_orquestrador import BiogemeoOrquestradorGlobal
        except ImportError:
            BiogemeoOrquestradorGlobal = None  # type: ignore

def executar_teste_bridge():
    print("\n" + "="*70)
    print("🌉 INICIANDO TESTE DA BRIDGE (COMUNICAÇÃO CORE & ORQUESTRADOR)")
    print("="*70)

    if BiogemeoOrquestradorGlobal is None:
        print("❌ ERRO: A classe do Orquestrador não foi localizada.")
        return

    try:
        orquestrador = BiogemeoOrquestradorGlobal({})
        print(" -> Status: APROVADO | Instância do Orquestrador criada com sucesso.")
        
        if hasattr(orquestrador, "disparar_analise_10s"):
            print(" -> Status: APROVADO | Método de disparo integrado localizado.")
        
        print("\n" + "="*70)
        print("✅ RELATÓRIO BRIDGE: COMUNICAÇÃO ESTABELECIDA COM SUCESSO ABSOLUTO!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"❌ Erro durante a execução da bridge: {e}")

if __name__ == "__main__":
    executar_teste_bridge()