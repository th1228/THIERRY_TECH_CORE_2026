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
# ARQUIVO: security/key_manager.py
# Gerenciador Local de Chaves, Seeds e Derivação (100% Offline)
# =====================================================================

import base64
import hashlib
import hmac
import json
import os
import secrets
import sys
from datetime import datetime, timezone
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

DEFAULT_KEYSTORE_PATH = SECURITY_DIR / "keystore_meta.json"


class KeyManager:
    """
    Gerencia sementes mestres em memória/ambiente, derivação de subchaves
    via PBKDF2-HMAC-SHA256 e registro de metadados de rotação sem rede.
    """

    def __init__(
        self,
        keystore_path: str | os.PathLike[str] | None = None,
        iteracoes_pbkdf2: int = 200_000,
    ) -> None:
        if iteracoes_pbkdf2 < 50_000:
            raise ValueError("Número de iterações PBKDF2 abaixo do mínimo recomendado.")

        self.keystore_path = Path(keystore_path) if keystore_path else DEFAULT_KEYSTORE_PATH
        self.iteracoes_pbkdf2 = iteracoes_pbkdf2
        self._seed_ativa: bytes = self._carregar_seed_inicial()
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
            self._logger.registrar("KEY_MANAGER", nivel, mensagem)
        except (OSError, RuntimeError):
            pass

    @staticmethod
    def _carregar_seed_inicial() -> bytes:
        """
        Carrega seed de ambiente (MIBO_MASTER_SEED em hex ou base64)
        ou gera uma entropia local segura de 64 bytes em memória.
        """
        seed_env = os.getenv("MIBO_MASTER_SEED", "").strip()
        if seed_env:
            try:
                return bytes.fromhex(seed_env)
            except ValueError:
                try:
                    return base64.b64decode(seed_env, validate=True)
                except (ValueError, TypeError):
                    return hashlib.sha512(seed_env.encode("utf-8")).digest()
        return secrets.token_bytes(64)

    def gerar_chave_aleatoria(self, tamanho_bytes: int = 32) -> bytes:
        """Gera uma chave criptográfica aleatória segura."""
        if tamanho_bytes < 16:
            raise ValueError("Tamanho mínimo da chave deve ser de 16 bytes.")
        return secrets.token_bytes(tamanho_bytes)

    def derivar_chave(
        self,
        contexto: str,
        salt: bytes | str | None = None,
        tamanho_bytes: int = 32,
    ) -> bytes:
        """Deriva uma subchave determinística para um contexto específico via PBKDF2."""
        if not isinstance(contexto, str) or not contexto.strip():
            raise ValueError("Contexto de derivação de chave não pode ser vazio.")
        if tamanho_bytes < 16:
            raise ValueError("Tamanho mínimo da subchave deve ser de 16 bytes.")

        if salt is None:
            salt_bytes = hashlib.sha256(contexto.strip().encode("utf-8")).digest()
        elif isinstance(salt, (bytes, bytearray, memoryview)):
            salt_bytes = bytes(salt)
        else:
            salt_bytes = str(salt).encode("utf-8")

        material = self._seed_ativa + b":" + contexto.strip().encode("utf-8")
        return hashlib.pbkdf2_hmac(
            "sha256",
            material,
            salt_bytes,
            self.iteracoes_pbkdf2,
            dklen=tamanho_bytes,
        )

    def rotacionar_seed(self, nova_seed: bytes | None = None) -> str:
        """
        Rotaciona a seed mestre ativa na memória e grava metadados de auditoria
        (sem gravar a chave em texto puro no disco).
        """
        if nova_seed is None:
            self._seed_ativa = secrets.token_bytes(64)
        else:
            if not isinstance(nova_seed, (bytes, bytearray, memoryview)) or len(nova_seed) < 32:
                raise ValueError("A nova seed deve conter pelo menos 32 bytes.")
            self._seed_ativa = bytes(nova_seed)

        fingerprint = hashlib.sha256(self._seed_ativa).hexdigest()[:16]
        self._salvar_metadado_rotacao(fingerprint)
        self._registrar("INFO", f"Seed mestre rotacionada. Fingerprint={fingerprint}.")
        return fingerprint

    def _salvar_metadado_rotacao(self, fingerprint: str) -> None:
        registro: dict[str, Any] = {
            "rotacionado_em_utc": datetime.now(timezone.utc).isoformat(),
            "fingerprint_sha256_prefixo": fingerprint,
            "iteracoes_pbkdf2": self.iteracoes_pbkdf2,
        }
        try:
            self.keystore_path.parent.mkdir(parents=True, exist_ok=True)
            with self.keystore_path.open("w", encoding="utf-8") as f:
                json.dump(registro, f, indent=2, ensure_ascii=False, sort_keys=True)
        except OSError as e:
            raise RuntimeError(f"Falha ao salvar metadado de rotação de chave: {e}") from e

    def assinar_hmac(self, mensagem: bytes | str, contexto: str = "assinatura_padrao") -> str:
        """Gera assinatura HMAC-SHA256 usando subchave derivada para o contexto."""
        chave = self.derivar_chave(contexto=contexto, tamanho_bytes=32)
        payload = mensagem.encode("utf-8") if isinstance(mensagem, str) else bytes(mensagem)
        return hmac.new(chave, payload, hashlib.sha256).hexdigest()

    def verificar_hmac(
        self,
        mensagem: bytes | str,
        assinatura_hex: str,
        contexto: str = "assinatura_padrao",
    ) -> bool:
        """Verifica assinatura HMAC-SHA256 em tempo constante."""
        if not isinstance(assinatura_hex, str) or not assinatura_hex.strip():
            return False
        esperada = self.assinar_hmac(mensagem=mensagem, contexto=contexto)
        return hmac.compare_digest(esperada, assinatura_hex.strip().lower())