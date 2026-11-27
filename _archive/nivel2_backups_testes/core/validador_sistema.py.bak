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

import sys, os

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys, os

import hashlib
import os

class ValidadorSistema:
    def __init__(self, lang: str = "PT"):
        # Localiza a pasta raiz do projeto (THIERRY_TECH_CORE_2026)
        # O validador está em 'core', então subimos um nível para achar a raiz
        self.diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        self.raiz = os.path.dirname(self.diretorio_atual)
        
        # Mapeamento exato de onde cada arquivo mora
        self.mapa = {
            'main.py': self.raiz,
            'monaco_plan.py': self.raiz,
            'monaco_blindagem.py': self.raiz,
            'monaco_comunicacao.py': self.raiz,
            'monaco_consciencia.py': self.raiz,
            'monaco_eminencia.py': self.raiz,
            'monaco_integrador.py': self.raiz,
            'monaco_nucleo_acesso.py': self.raiz,
            'monaco_ressonancia.py': self.raiz,
            'motor_sincronia.py': self.diretorio_atual # Este mora no CORE
        }

    def rodar_validacao(self):
        print(f"\n--- [SISTEMA] Auditoria Híbrida: Iniciada ---")
        falha = False
        
        for arquivo, pasta in self.mapa.items():
            caminho_real = os.path.join(pasta, arquivo)
            
            if os.path.exists(caminho_real):
                print(f"[OK] {arquivo} encontrado.")
            else:
                print(f"[ERRO CRÍTICO] {arquivo} NÃO encontrado em: {pasta}")
                falha = True
        
        if falha:
            print("\n>>> STATUS: INTEGRIDADE FALHOU. BLOQUEANDO ACESSO. <<<")
            return False
        
        print("\n>>> STATUS: SISTEMA TOTALMENTE BLINDADO E OPERACIONAL <<<")
        return True

if __name__ == "__main__":
    validador = ValidadorSistema()
    if not validador.rodar_validacao():
        exit(1)