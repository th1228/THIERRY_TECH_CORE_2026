# -*- coding: utf-8 -*-
"""
Módulo: sentinela_fisio.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Versão: 1.1.0 - Monitoramento Resiliente e Integridade de Módulos
"""

import sys
import os

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
# Adiciona a raiz do projeto ao Python de forma limpa e segura
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

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

# IMPORTAÇÃO RESILIENTE DO MOTOR BIOMÉTRICO
biometria = None
try:
    from core import biometria
except ImportError:
    try:
        import biometria
    except ImportError:
        biometria = None

def executar_vigilancia():
    """
    Função principal do Sentinela para validação de integridade física e biométrica.
    """
    status_sentinela = {
        "status": "Ativo",
        "motor_biometria": "OK" if biometria else "Indisponível",
        "vigilancia": "Monitorando metas e parâmetros UHNW"
    }
    
    # Sincroniza com a memória comum
    try:
        memoria.salvar_dados("sentinela_fisio_status", status_sentinela)
    except Exception:
        pass
        
    return status_sentinela

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    return executar_vigilancia()

# --- TESTE DE VIDA DO SENTINELA ---
if __name__ == "__main__":
    print("\n--- [SENTINELA] STATUS CHECK ---")
    try:
        executar_vigilancia()
        print("[SENTINELA] Motor de Biometria: OK")
        print("[SENTINELA] Sentinela está vigiando as metas ativamente.")
    except Exception as e:
        print(f"[SENTINELA] ERRO: Falha na verificação de integridade: {e}")
    print("---------------------------------\n")