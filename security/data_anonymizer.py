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

import hashlib
import os


class DataAnonymizer:
    """
    Motor de anonimização irreversível via SHA-256 para dados sensíveis,
    identificadores e registros em ambiente 100% offline.
    """

    @staticmethod
    def anonimizar(dado, salt: bytes | str | None = None) -> str:
        """
        Transforma um dado sensível em um hash SHA-256 irreversível.
        Aceita str, bytes ou outros tipos básicos; aplica salt opcional (ou do ambiente).
        """
        if dado is None:
            texto = ""
        elif isinstance(dado, (bytes, bytearray, memoryview)):
            texto = bytes(dado).decode("utf-8", errors="replace")
        else:
            texto = str(dado)

        if salt is None:
            salt_env = os.getenv("MIBO_ANONIMIZER_SALT", "")
            salt_bytes = salt_env.encode("utf-8")
        elif isinstance(salt, (bytes, bytearray, memoryview)):
            salt_bytes = bytes(salt)
        else:
            salt_bytes = str(salt).encode("utf-8")

        hasher = hashlib.sha256()
        if salt_bytes:
            hasher.update(salt_bytes)
            hasher.update(b":")
        hasher.update(texto.encode("utf-8"))
        return hasher.hexdigest()