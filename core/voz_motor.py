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
            def __init__(self):
                self._dados = {}

            def salvar_dados(self, chave, valor):
                self._dados[chave] = valor
                return True

            def registrar(self, chave, valor):
                self._dados[chave] = valor
                return True

            def ler_dados(self, chave):
                return self._dados.get(chave)
        memoria = MemoriaMock()
# ---------------------------------------------------

# -*- coding: utf-8 -*-

def falar(texto):
    """
    Motor de voz desativado permanentemente a pedido do operador.
    """
    payload = {
        "status": "desativado_permanente",
        "motivo": "desativado a pedido do operador",
        "tamanho_texto": len(texto) if texto is not None else 0,
    }
    if hasattr(memoria, "registrar"):
        memoria.registrar("voz_motor_ultimo_evento", payload)
    elif hasattr(memoria, "salvar_dados"):
        memoria.salvar_dados("voz_motor_ultimo_evento", payload)
    return payload