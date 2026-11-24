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
# ARQUIVO: security/token_manager.py
# Gerenciador Local de Tokens Assinados e Revogação (100% Offline)
# =====================================================================

import base64
import hashlib
import hmac
import json
import os
import secrets
import sys
import time
from pathlib import Path
from typing import Any

SECURITY_DIR = Path(__file__).resolve().parent
RAIZ_PROJETO = SECURITY_DIR.parent
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.append(str(RAIZ_PROJETO))

try:
    from security.log_seguro import LogSeguro
except ImportError:
    from log_seguro import LogSeguro


class TokenManager:
    """
    Emite, valida e revoga tokens locais assinados com HMAC-SHA256
    sem dependência de rede ou serviços externos.
    """

    def __init__(
        self,
        chave_assinatura: bytes | str | None = None,
        ttl_padrao_segundos: int = 3600,
    ) -> None:
        if ttl_padrao_segundos <= 0:
            raise ValueError("O TTL padrão do token deve ser maior que zero.")

        self._chave_hmac: bytes = self._resolver_chave(chave_assinatura)
        self.ttl_padrao_segundos = int(ttl_padrao_segundos)
        self._revogados: set[str] = set()
        self._logger: LogSeguro | None = self._iniciar_logger()

    @staticmethod
    def _iniciar_logger() -> LogSeguro | None:
        try:
            return LogSeguro()
        except (OSError, RuntimeError):
            return None

    def _registrar(self, nivel: str, mensagem: str) -> None:
        if self._logger is None:
            return
        try:
            self._logger.registrar("TOKEN_MANAGER", nivel, mensagem)
        except (OSError, RuntimeError):
            pass

    @staticmethod
    def _resolver_chave(chave_assinatura: bytes | str | None) -> bytes:
        if isinstance(chave_assinatura, (bytes, bytearray, memoryview)):
            dados = bytes(chave_assinatura)
            if len(dados) < 16:
                raise ValueError("A chave de assinatura deve ter pelo menos 16 bytes.")
            return dados
        if isinstance(chave_assinatura, str) and chave_assinatura.strip():
            return hashlib.sha256(chave_assinatura.strip().encode("utf-8")).digest()

        chave_env = os.getenv("MIBO_TOKEN_SECRET", "").strip()
        if chave_env:
            return hashlib.sha256(chave_env.encode("utf-8")).digest()

        return secrets.token_bytes(32)

    @staticmethod
    def _b64_encode(dados: bytes) -> str:
        return base64.urlsafe_b64encode(dados).decode("ascii").rstrip("=")

    @staticmethod
    def _b64_decode(texto: str) -> bytes:
        padding = "=" * (-len(texto) % 4)
        return base64.urlsafe_b64decode((texto + padding).encode("ascii"))

    def _assinar(self, payload_b64: str) -> str:
        digest = hmac.new(
            self._chave_hmac,
            payload_b64.encode("ascii"),
            hashlib.sha256,
        ).digest()
        return self._b64_encode(digest)

    def emitir_token(
        self,
        sujeito: str,
        escopos: list[str] | None = None,
        ttl_segundos: int | None = None,
    ) -> str:
        """Gera um token local assinado contendo jti, sujeito, escopos e expiração."""
        if not isinstance(sujeito, str) or not sujeito.strip():
            raise ValueError("O sujeito do token não pode ser vazio.")

        ttl = self.ttl_padrao_segundos if ttl_segundos is None else int(ttl_segundos)
        if ttl <= 0:
            raise ValueError("O TTL do token deve ser maior que zero.")

        agora = int(time.time())
        payload: dict[str, Any] = {
            "jti": secrets.token_hex(16),
            "sub": sujeito.strip(),
            "scp": [str(s).strip().lower() for s in (escopos or []) if str(s).strip()],
            "iat": agora,
            "exp": agora + ttl,
        }

        payload_json = json.dumps(payload, separators=(",", ":"), ensure_ascii=False, sort_keys=True)
        payload_b64 = self._b64_encode(payload_json.encode("utf-8"))
        assinatura_b64 = self._assinar(payload_b64)
        token = f"{payload_b64}.{assinatura_b64}"
        self._registrar("INFO", f"Token emitido para sujeito='{payload['sub']}' (jti={payload['jti'][:8]}...).")
        return token

    def validar_token(self, token: str) -> dict[str, Any]:
        """
        Valida formato, assinatura HMAC, revogação e expiração do token.
        Retorna o payload decodificado em caso de sucesso ou levanta ValueError.
        """
        if not isinstance(token, str) or "." not in token:
            raise ValueError("Formato de token inválido.")

        partes = token.split(".")
        if len(partes) != 2:
            raise ValueError("Estrutura de token inválida.")

        payload_b64, assinatura_b64 = partes
        assinatura_esperada = self._assinar(payload_b64)
        if not hmac.compare_digest(assinatura_esperada, assinatura_b64):
            self._registrar("ALERTA", "Tentativa de uso de token com assinatura inválida.")
            raise ValueError("Assinatura do token inválida.")

        try:
            payload_bytes = self._b64_decode(payload_b64)
            payload = json.loads(payload_bytes.decode("utf-8"))
        except (ValueError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as e:
            raise ValueError(f"Payload do token corrompido: {e}") from e

        if not isinstance(payload, dict):
            raise ValueError("Payload do token não é um objeto JSON válido.")

        jti = str(payload.get("jti", ""))
        if not jti or jti in self._revogados:
            self._registrar("ALERTA", f"Tentativa de uso de token revogado ou sem jti ({jti[:8]}).")
            raise ValueError("Token revogado ou inválido.")

        exp = payload.get("exp")
        if not isinstance(exp, int) or int(time.time()) > exp:
            self._registrar("ALERTA", f"Token expirado (jti={jti[:8]}).")
            raise ValueError("Token expirado.")

        return payload

    def revogar_token(self, token: str) -> bool:
        """Adiciona o identificador (jti) de um token válido à lista de revogados."""
        payload = self.validar_token(token)
        jti = str(payload["jti"])
        self._revogados.add(jti)
        self._registrar("ALERTA", f"Token revogado com sucesso (jti={jti[:8]}...).")
        return True

    def esta_revogado(self, jti: str) -> bool:
        """Verifica se um jti já consta na lista local de tokens revogados."""
        return isinstance(jti, str) and jti in self._revogados