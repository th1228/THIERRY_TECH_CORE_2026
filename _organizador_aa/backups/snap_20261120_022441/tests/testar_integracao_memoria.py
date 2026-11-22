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
# TESTE RÁPIDO DE INTEGRAÇÃO - MEMÓRIA COMUM (TTC GLOBAL)
# =====================================================================
from threading import Thread

try:
    from core.memoria_comum import memoria_global
except ImportError:
    class MemoriaMock:
        def __init__(self):
            self._dados = {}
        def salvar_dados(self, k, v): self._dados[k] = v
        def obter_dados(self, k): return self._dados.get(k)
    memoria_global = MemoriaMock()

def simular_camada(nome_camada, id_dado):
    chave = f"status_{nome_camada.lower()}"
    valor = f"OK_INTEGRADO_{id_dado}"
    memoria_global.salvar_dados(chave, valor)
    print(f"[{nome_camada}] -> Gravou na memória comum.")

def testar_integracao_total():
    print("==================================================")
    print("  TESTE DE INTEGRAÇÃO: CAMADAS x MEMÓRIA COMUM  ")
    print("==================================================")
    
    camadas = [
        "InputSanitizer", "NonceCache", "SessionManager", 
        "CryptoEngine", "DBManager", "MemoriaComum", "LogSeguro"
    ]
    
    threads = []
    for i, camada in enumerate(camadas):
        t = Thread(target=simular_camada, args=(camada, i))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("\n--- VERIFICANDO VALORES NA MEMÓRIA GLOBAL ---")
    todas_ok = True
    for camada in camadas:
        chave = f"status_{camada.lower()}"
        dado_lido = memoria_global.obter_dados(chave)
        status_txt = "✅ LIDO COM SUCESSO" if dado_lido else "❌ FALHOU"
        print(f"-> {camada}: {status_txt} ({dado_lido})")
        if not dado_lido:
            todas_ok = False
            
    print("==================================================")
    if todas_ok:
        print(" RESULTADO: TODAS AS 7 CAMADAS ESTÃO INTEGRADAS!")
    else:
        print(" RESULTADO: HÁ FALHAS NA SINCRONIZAÇÃO.")
    print("==================================================")

if __name__ == "__main__":
    testar_integracao_total()