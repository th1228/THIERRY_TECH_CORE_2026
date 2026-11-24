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
# ARQUIVO: security/integrity_guard.py
# Guarda de Integridade Local (Manifesto SHA-256 e Travas Operacionais)
# =====================================================================

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SECURITY_DIR = Path(__file__).resolve().parent
DEFAULT_MANIFEST_PATH = SECURITY_DIR / "integrity_manifest.json"
DEFAULT_LOCK_PATH = SECURITY_DIR / "system.lock"


class IntegrityGuard:
    """
    Monitora a integridade de arquivos críticos via manifesto SHA-256 local
    e controla estados de bloqueio operacional em ambiente 100% offline.
    """

    def __init__(
        self,
        manifest_path: str | os.PathLike[str] | None = None,
        lock_path: str | os.PathLike[str] | None = None,
    ) -> None:
        self.manifest_path = Path(manifest_path) if manifest_path else DEFAULT_MANIFEST_PATH
        self.lock_path = Path(lock_path) if lock_path else DEFAULT_LOCK_PATH

    @staticmethod
    def calcular_hash_arquivo(caminho: str | os.PathLike[str]) -> str:
        """Calcula o SHA-256 de um arquivo em blocos."""
        arquivo = Path(caminho)
        hasher = hashlib.sha256()
        with arquivo.open("rb") as f:
            for bloco in iter(lambda: f.read(65536), b""):
                hasher.update(bloco)
        return hasher.hexdigest()

    def gerar_manifesto(self, arquivos: list[str | os.PathLike[str]]) -> dict[str, Any]:
        """Gera e salva um manifesto JSON com hashes SHA-256 dos arquivos informados."""
        registros: dict[str, str] = {}
        for item in arquivos:
            caminho_resolvido = Path(item).resolve()
            if not caminho_resolvido.is_file():
                raise FileNotFoundError(f"Arquivo não encontrado para o manifesto: {caminho_resolvido}")
            registros[str(caminho_resolvido)] = self.calcular_hash_arquivo(caminho_resolvido)

        manifesto = {
            "gerado_em_utc": datetime.now(timezone.utc).isoformat(),
            "arquivos": registros,
        }

        try:
            self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
            with self.manifest_path.open("w", encoding="utf-8") as f:
                json.dump(manifesto, f, indent=2, ensure_ascii=False, sort_keys=True)
        except OSError as e:
            raise RuntimeError(f"Falha ao salvar manifesto de integridade: {e}") from e

        return manifesto

    def verificar_manifesto(self) -> tuple[bool, list[str]]:
        """
        Compara os arquivos listados no manifesto contra o estado atual no disco.
        Retorna (True, []) se tudo estiver íntegro, ou (False, divergencias).
        """
        if not self.manifest_path.is_file():
            return False, [f"Manifesto inexistente: {self.manifest_path}"]

        try:
            with self.manifest_path.open("r", encoding="utf-8") as f:
                dados = json.load(f)
        except (OSError, json.JSONDecodeError, ValueError) as e:
            return False, [f"Falha ao ler manifesto: {e}"]

        arquivos_esperados = dados.get("arquivos")
        if not isinstance(arquivos_esperados, dict):
            return False, ["Estrutura de manifesto inválida: campo 'arquivos' ausente."]

        divergencias: list[str] = []
        for caminho_str, hash_esperado in arquivos_esperados.items():
            caminho = Path(caminho_str)
            if not caminho.is_file():
                divergencias.append(f"Arquivo ausente: {caminho}")
                continue

            try:
                hash_atual = self.calcular_hash_arquivo(caminho)
            except OSError as e:
                divergencias.append(f"Erro de leitura em {caminho}: {e}")
                continue

            if hash_atual != hash_esperado:
                divergencias.append(f"Hash alterado em {caminho}")

        return len(divergencias) == 0, divergencias

    def esta_bloqueado(self) -> bool:
        """Indica se o arquivo de trava operacional (system.lock) está ativo."""
        return self.lock_path.exists()

    def ativar_bloqueio(self, motivo: str = "BLOQUEIO_INTEGRIDADE") -> None:
        """Cria o arquivo de trava operacional com o motivo e timestamp UTC."""
        payload = {
            "bloqueado_em_utc": datetime.now(timezone.utc).isoformat(),
            "motivo": motivo,
        }
        try:
            self.lock_path.parent.mkdir(parents=True, exist_ok=True)
            with self.lock_path.open("w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False)
        except OSError as e:
            raise RuntimeError(f"Falha ao ativar trava de segurança: {e}") from e

    def liberar_bloqueio(self) -> bool:
        """Remove a trava operacional se existir."""
        if not self.lock_path.exists():
            return False
        try:
            self.lock_path.unlink()
            return True
        except OSError as e:
            raise RuntimeError(f"Falha ao remover trava de segurança: {e}") from e