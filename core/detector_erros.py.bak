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
import traceback
from datetime import datetime

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

class DetectorErrosTTC:
    def __init__(self, nome_arquivo_log="ttc_diagnostico_erros.log", lang: str = "PT"):
        self.caminho_log = nome_arquivo_log

    def registrar_falha(self, modulo, excecao):
        """Captura o erro, a linha e o motivo exato, salvando no log, console e Memória Comum 🧠."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tracelist = traceback.format_exc()
        
        mensagem_erro = (
            f"\n[DIAGNÓSTICO DE ERRO TTC] ============================\n"
            f"DATA/HORA: {timestamp}\n"
            f"MÓDULO AFETADO: {modulo}\n"
            f"ERRO CAPTURADO: {str(excecao)}\n"
            f"RASTREAMENTO COMPLETO (TRACEBACK):\n{tracelist}"
            f"=====================================================\n"
        )
        
        print(mensagem_erro)
        
        # Sincroniza o último erro ocorrido na Memória Comum 🧠
        try:
            memoria.salvar_dados("ultimo_erro_sistema", {
                "modulo": modulo,
                "erro": str(excecao),
                "timestamp": timestamp
            })
        except Exception:
            pass

        try:
            with open(self.caminho_log, "a", encoding="utf-8") as f:
                f.write(mensagem_erro + "\n")
        except Exception as e:
            print(f"[ERRO CRÍTICO] Não foi possível escrever no log de erros: {e}")

# Instância global para uso no projeto
monitor_erros = DetectorErrosTTC()

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    return {"status": "Detector de erros ativo e monitorando", "log": monitor_erros.caminho_log}

if __name__ == "__main__":
    print("Módulo de Detector de Erros carregado corretamente.")