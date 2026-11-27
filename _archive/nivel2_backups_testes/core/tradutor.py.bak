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

# -*- coding: utf-8 -*-

TRADUCOES = {
    "PT": {
        "protocolo_ativo": "Protocolo Ativo",
        "total": "Total",
        "reposicao": "Vitamina C e Minerais Inclusos",
        "ghk_desc": "Protocolo GHK",
        "glow_desc": "Protocolo GLOW",
    },
    "EN": {
        "protocolo_ativo": "Active Protocol",
        "total": "Total",
        "reposicao": "Vitamin C and Minerals Included",
        "ghk_desc": "GHK Protocol",
        "glow_desc": "GLOW Protocol",
    },
}

# Idioma atual do sistema (pode ser alterado dinamicamente pelo gerente geográfico ou configuração)
IDIOMA_ATUAL = "PT"


def definir_idioma(sigla):
  global IDIOMA_ATUAL
  if sigla.upper() in TRADUCOES:
    IDIOMA_ATUAL = sigla.upper()


def t(chave):
  return TRADUCOES.get(IDIOMA_ATUAL, TRADUCOES["PT"]).get(chave, chave)