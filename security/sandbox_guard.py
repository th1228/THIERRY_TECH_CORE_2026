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
# ARQUIVO: security/sandbox_guard.py
# Guarda de Isolamento de Caminhos e Diretórios Permitidos (100% Offline)
# =====================================================================

import os
import sys
from pathlib import Path

SECURITY_DIR = Path(__file__).resolve().parent
RAIZ_PROJETO = SECURITY_DIR.parent
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.append(str(RAIZ_PROJETO))

try:
    from security.log_seguro import LogSeguro
except ImportError:
    from log_seguro import LogSeguro


class SandboxGuard:
    """
    Garante que operações com arquivos fiquem restritas a diretórios-base
    autorizados, impedindo escape de diretório (path traversal) e extensões
    não permitidas em ambiente 100% offline.
    """

    def __init__(
        self,
        diretorios_permitidos: list[str | os.PathLike[str]] | None = None,
        extensoes_permitidas: set[str] | list[str] | None = None,
        habilitar_log: bool = True,
    ) -> None:
        bases = diretorios_permitidos if diretorios_permitidos else [RAIZ_PROJETO]
        self._raizes_resolvidas: list[Path] = [Path(p).resolve() for p in bases]

        if extensoes_permitidas is not None:
            self._extensoes_permitidas: set[str] | None = {
                (ext if ext.startswith(".") else f".{ext}").lower()
                for ext in extensoes_permitidas
            }
        else:
            self._extensoes_permitidas = None

        self._logger: LogSeguro | None = self._iniciar_logger() if habilitar_log else None

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
            self._logger.registrar("SANDBOX_GUARD", nivel, mensagem)
        except (OSError, RuntimeError):
            pass

    def _esta_dentro_de_raiz(self, caminho_resolvido: Path) -> bool:
        for raiz in self._raizes_resolvidas:
            try:
                caminho_resolvido.relative_to(raiz)
                return True
            except ValueError:
                continue
        return False

    def resolver_caminho_seguro(
        self,
        caminho_alvo: str | os.PathLike[str],
        base_relativa: str | os.PathLike[str] | None = None,
    ) -> Path:
        """
        Resolve o caminho absoluto e garante que ele permaneça dentro de pelo menos
        um diretório permitido e respeite as extensões autorizadas (se configuradas).
        Levanta PermissionError ou ValueError se violar a sandbox.
        """
        if not isinstance(caminho_alvo, (str, os.PathLike)) or not str(caminho_alvo).strip():
            raise ValueError("Caminho alvo não pode ser vazio.")

        texto_bruto = str(caminho_alvo)
        if "\x00" in texto_bruto:
            raise ValueError("Caminho contém byte nulo inválido.")

        candidato = Path(texto_bruto)
        if not candidato.is_absolute() and base_relativa is not None:
            candidato = Path(base_relativa) / candidato

        caminho_resolvido = candidato.resolve()

        if not self._esta_dentro_de_raiz(caminho_resolvido):
            self._registrar(
                "ALERTA",
                f"Bloqueio de fuga de sandbox para caminho fora da raiz: '{caminho_resolvido}'.",
            )
            raise PermissionError(
                f"Acesso bloqueado: '{caminho_resolvido}' está fora dos diretórios permitidos."
            )

        if self._extensoes_permitidas is not None:
            ext = caminho_resolvido.suffix.lower()
            if ext not in self._extensoes_permitidas:
                self._registrar(
                    "ALERTA",
                    f"Bloqueio de extensão não autorizada ('{ext}') em '{caminho_resolvido}'.",
                )
                raise ValueError(
                    f"Extensão de arquivo '{ext}' não permitida na sandbox para '{caminho_resolvido}'."
                )

        return caminho_resolvido