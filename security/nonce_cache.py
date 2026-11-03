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
# ARQUIVO: security/nonce_cache.py
# =====================================================================

import time
import threading

class NonceCache:
    """Cache em memória RAM para bloqueio Anti-Replay"""
    def __init__(self, ttl_seconds: int = 30, teto_maximo: int = 50000):
        self.cache = {}
        self.ttl = ttl_seconds
        self.teto_maximo = teto_maximo
        self._lock = threading.Lock()

    def validar_e_registrar(self, nonce: str) -> bool:
        with self._lock:
            agora = time.time()
            expirados = [k for k, v in self.cache.items() if agora - v > self.ttl]
            for k in expirados:
                del self.cache[k]
            if len(self.cache) >= self.teto_maximo or nonce in self.cache:
                return False
            self.cache[nonce] = agora
            return True