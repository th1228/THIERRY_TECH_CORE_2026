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

# Adiciona o diretório da pasta 'security' ao path para garantir os imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from security import portaria, detector, honeypot

protecao_ativa = False

def ativar_protecao():
    """Inicializa as camadas de segurança de forma centralizada."""
    global protecao_ativa
    if not protecao_ativa:
        print("[BLINDAGEM] Iniciando escudos de proteção...")
        try:
            portaria.iniciar()
            detector.iniciar_monitoramento()
            honeypot.armar()
            protecao_ativa = True
            print("[BLINDAGEM] Escudo de proteção ATIVADO com sucesso.")
        except Exception as e:
            print(f"[ERRO CRÍTICO] Falha na blindagem: {e}")
    # Se já estiver ativa, apenas segue o fluxo sem poluir o terminal
    return True

def rodar(frame):
    """
    Ponte de segurança: Garante que a proteção esteja ativa 
    antes de qualquer processamento e retorna o frame intacto.
    """
    ativar_protecao()
    return frame