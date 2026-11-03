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
# CAMADA 8: RATE LIMITING / THROTTLING - TTC GLOBAL
# =====================================================================
import time

class RateLimiting:
    _historico = {}
    _limite_requisicoes = 5  # Limite máximo
    _janela_tempo = 60       # Janela em segundos

    @staticmethod
    def verificar_vazao(identificador="default"):
        agora = time.time()
        
        if identificador not in RateLimiting._historico:
            RateLimiting._historico[identificador] = []
            
        # Filtra requisições dentro da janela de tempo
        tempos = RateLimiting._historico[identificador]
        tempos = [t for t in tempos if agora - t < RateLimiting._janela_tempo]
        
        if len(tempos) >= RateLimiting._limite_requisicoes:
            raise Exception("RateLimitExceeded: Muitas requisições em pouco tempo. Bloqueio temporário.")
            
        tempos.append(agora)
        RateLimiting._historico[identificador] = tempos
        print("[Camada 8] RateLimiting OK: Vazão dentro do limite permitido.")
        return True