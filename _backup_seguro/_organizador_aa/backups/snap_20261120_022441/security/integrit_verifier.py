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

# /security/integrity_verifier.py
import hashlib
import os

class IntegrityVerifier:
    @staticmethod
    def calcular_hash(caminho_arquivo):
        """Calcula o hash SHA-256 de um arquivo crítico."""
        sha256 = hashlib.sha256()
        try:
            with open(caminho_arquivo, "rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except FileNotFoundError:
            return None

    @staticmethod
    def verificar_arquivo(caminho_arquivo, hash_esperado):
        """Compara o hash atual com o hash 'dourado' (original)."""
        hash_atual = IntegrityVerifier.calcular_hash(caminho_arquivo)
        return hash_atual == hash_esperado