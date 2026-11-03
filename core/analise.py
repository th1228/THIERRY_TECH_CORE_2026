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
import sys
import os

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

def executar_analise_geral(dados_entrada=None):
    """
    Motor central de análise que consolida o status da Memória Comum 🧠.
    """
    print("📁 [ANALISE] Motor analítico central acionado.")
    
    # Busca diagnósticos salvos na memória comum
    rosto = memoria.ler_dados("ROSTO_STATUS") or {}
    cabelo = memoria.ler_dados("CABELO_DIAGNOSTICO") or {}
    
    resultado = {
        "status": "ANALISE_CONCLUIDA",
        "rosto_detectado": rosto.get("FORMATO", "NAO_ANALISADO"),
        "saude_cabelo": cabelo.get("VITALIDADE_SCORE", "NAO_ANALISADO")
    }
    
    try:
        memoria.salvar_dados("ULTIMA_ANALISE_GERAL", resultado)
    except Exception:
        pass
        
    return resultado

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    return executar_analise_geral(frame)

if __name__ == "__main__":
    executar_analise_geral()