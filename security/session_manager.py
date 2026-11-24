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

import os
import jwt
import secrets
import datetime
import hashlib


def _obter_secret_key() -> str:
    chave_env = os.environ.get("SECRET_KEY", "").strip()
    if chave_env:
        return chave_env
    if not hasattr(_obter_secret_key, "_chave_efemera"):
        setattr(_obter_secret_key, "_chave_efemera", secrets.token_hex(32))
    return getattr(_obter_secret_key, "_chave_efemera")


class SessionManager:
    # A SECRET_KEY é carregada da variável de ambiente SECRET_KEY (com fallback efêmero em memória)
    SECRET_KEY = _obter_secret_key()

    @staticmethod
    def gerar_token(usuario_id, ip_origem, hardware_fingerprint):
        """Gera um token vinculado ao usuário e ao seu dispositivo/rede."""
        chave = _obter_secret_key()
        payload = {
            "sub": usuario_id,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            # Bind de segurança: O token só é válido para este IP e este Hardware
            "context_hash": hashlib.sha256(f"{ip_origem}{hardware_fingerprint}".encode()).hexdigest()
        }
        return jwt.encode(payload, chave, algorithm="HS256")

    @staticmethod
    def validar_token(token, ip_atual, hardware_fingerprint_atual):
        """Valida o token e verifica se o contexto atual coincide com o de origem."""
        chave = _obter_secret_key()
        try:
            payload = jwt.decode(token, chave, algorithms=["HS256"])

            # Recalcula o hash do contexto atual para comparar
            hash_atual = hashlib.sha256(f"{ip_atual}{hardware_fingerprint_atual}".encode()).hexdigest()

            if payload["context_hash"] != hash_atual:
                return {"valido": False, "erro": "Sequestro de Sessão Detectado"}

            return {"valido": True, "usuario_id": payload["sub"]}

        except jwt.ExpiredSignatureError:
            return {"valido": False, "erro": "Sessão Expirada"}
        except (jwt.PyJWTError, KeyError, TypeError, ValueError) as e:
            return {"valido": False, "erro": str(e)}