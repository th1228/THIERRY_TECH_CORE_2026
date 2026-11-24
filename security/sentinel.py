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
# ARQUIVO: security/sentinel.py
# Sentinela Local de Monitoramento de Integridade e Arquivos (100% Offline)
# =====================================================================

import hashlib
import os
import sys
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


class Sentinel:
    """
    Monitora arquivos críticos do projeto localmente (calculando SHA-256)
    e registra eventos de integridade sem dependência de rede.
    """

    def __init__(
        self,
        alvos: list[str | os.PathLike[str]] | None = None,
        habilitar_log: bool = True,
    ) -> None:
        self.alvos: list[Path] = [
            Path(alvo).resolve()
            for alvo in (alvos or [RAIZ_PROJETO / "main.py", SECURITY_DIR / "log_seguro.py"])
        ]
        self._logger: LogSeguro | None = self._iniciar_logger() if habilitar_log else None
        self._baseline: dict[str, str] = {}

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
            self._logger.registrar("SENTINEL", nivel, mensagem)
        except (OSError, RuntimeError):
            pass

    @staticmethod
    def _calcular_sha256(arquivo: Path) -> str:
        hasher = hashlib.sha256()
        with arquivo.open("rb") as f:
            for bloco in iter(lambda: f.read(65536), b""):
                hasher.update(bloco)
        return hasher.hexdigest()

    def capturar_baseline(self) -> dict[str, str]:
        """Registra os hashes SHA-256 iniciais dos arquivos monitorados."""
        snapshot: dict[str, str] = {}
        for caminho in self.alvos:
            if caminho.is_file():
                try:
                    snapshot[str(caminho)] = self._calcular_sha256(caminho)
                except (OSError, ValueError) as e:
                    self._registrar("ALERTA", f"Falha ao ler '{caminho}' para baseline: {e}")
        self._baseline = snapshot
        self._registrar("INFO", f"Baseline capturado para {len(snapshot)} arquivo(s).")
        return dict(self._baseline)

    def verificar_integridade(self) -> dict[str, Any]:
        """Compara os arquivos atuais com o baseline capturado."""
        if not self._baseline:
            self.capturar_baseline()

        alterados: list[str] = []
        ausentes: list[str] = []

        for caminho_str, hash_esperado in self._baseline.items():
            caminho = Path(caminho_str)
            if not caminho.is_file():
                ausentes.append(caminho_str)
                continue
            try:
                hash_atual = self._calcular_sha256(caminho)
                if hash_atual != hash_esperado:
                    alterados.append(caminho_str)
            except (OSError, ValueError) as e:
                alterados.append(caminho_str)
                self._registrar("ALERTA", f"Falha ao verificar '{caminho_str}': {e}")

        integros = not alterados and not ausentes
        if not integros:
            self._registrar(
                "ALERTA",
                f"Divergência detetada — alterados: {len(alterados)}, ausentes: {len(ausentes)}.",
            )

        return {
            "integro": integros,
            "alterados": alterados,
            "ausentes": ausentes,
        }


class TTCSentinel(Sentinel):
    """Compatibilidade com o main.py para inicialização com licença e log forense."""

    def __init__(
        self,
        license_filename: str | os.PathLike[str] | None = None,
        audit_log: str | os.PathLike[str] | None = None,
        alvos: list[str | os.PathLike[str]] | None = None,
        habilitar_log: bool = True,
    ) -> None:
        super().__init__(alvos=alvos, habilitar_log=habilitar_log)
        self.license_filename = Path(license_filename).resolve() if license_filename else None
        self.audit_log = Path(audit_log).resolve() if audit_log else None
        self.capturar_baseline()


if __name__ == "__main__":
    sentinela = Sentinel()
    sentinela.capturar_baseline()
    resultado = sentinela.verificar_integridade()
    print("Status Sentinel:", resultado)