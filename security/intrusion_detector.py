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
# ARQUIVO: security/intrusion_detector.py
# Detector Local de Anomalias e Tentativas Suspeitas (100% Offline)
# =====================================================================

import os
import re
import sys
import threading
import time
from collections import defaultdict, deque
from pathlib import Path

SECURITY_DIR = Path(__file__).resolve().parent
RAIZ_PROJETO = SECURITY_DIR.parent
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.append(str(RAIZ_PROJETO))

try:
    from security.log_seguro import LogSeguro
except ImportError:
    from log_seguro import LogSeguro

PADROES_SUSPEITOS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(\bUNION\b\s+\bSELECT\b|\bDROP\s+TABLE\b|\bOR\s+1\s*=\s*1\b)", re.IGNORECASE),
    re.compile(r"(\.\./|\.\.\\|%2e%2e)", re.IGNORECASE),
    re.compile(r"(<script\b|javascript:|onerror\s*=|onload\s*=)", re.IGNORECASE),
    re.compile(r"(os\.system\(|subprocess\.|eval\(|exec\(|__import__\()", re.IGNORECASE),
)


class IntrusionDetector:
    """
    Monitora falhas repetidas por origem/ator, bloqueia temporariamente
    origens reincidentes e sinaliza padrões de entrada suspeitos em ambiente local.
    """

    def __init__(
        self,
        max_falhas: int = 5,
        janela_segundos: float = 60.0,
        duracao_bloqueio_segundos: float = 300.0,
    ) -> None:
        if max_falhas <= 0:
            raise ValueError("O limite máximo de falhas deve ser maior que zero.")
        if janela_segundos <= 0:
            raise ValueError("A janela de tempo deve ser maior que zero.")
        if duracao_bloqueio_segundos <= 0:
            raise ValueError("A duração do bloqueio deve ser maior que zero.")

        self.max_falhas = int(max_falhas)
        self.janela_segundos = float(janela_segundos)
        self.duracao_bloqueio_segundos = float(duracao_bloqueio_segundos)

        self._lock = threading.Lock()
        self._falhas_por_origem: dict[str, deque[float]] = defaultdict(deque)
        self._bloqueios_ate: dict[str, float] = {}
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
            self._logger.registrar("INTRUSION_DETECTOR", nivel, mensagem)
        except (OSError, RuntimeError):
            pass

    @staticmethod
    def _normalizar_origem(origem: str) -> str:
        if not isinstance(origem, str) or not origem.strip():
            raise ValueError("A origem/identificador não pode ser vazia.")
        return origem.strip()

    def esta_bloqueado(self, origem: str) -> bool:
        """Verifica se a origem está atualmente sob bloqueio temporário."""
        chave = self._normalizar_origem(origem)
        agora = time.monotonic()

        with self._lock:
            expira_em = self._bloqueios_ate.get(chave)
            if expira_em is None:
                return False
            if agora >= expira_em:
                del self._bloqueios_ate[chave]
                return False
            return True

    def bloquear_origem(self, origem: str, duracao_segundos: float | None = None) -> float:
        """Bloqueia manualmente uma origem por tempo determinado e retorna o prazo."""
        chave = self._normalizar_origem(origem)
        duracao = (
            self.duracao_bloqueio_segundos
            if duracao_segundos is None
            else float(duracao_segundos)
        )
        if duracao <= 0:
            raise ValueError("A duração do bloqueio deve ser maior que zero.")

        agora = time.monotonic()
        expira_em = agora + duracao

        with self._lock:
            self._bloqueios_ate[chave] = expira_em

        self._registrar("CRITICO", f"Origem '{chave}' bloqueada por {duracao:.1f}s.")
        return duracao

    def liberar_origem(self, origem: str) -> bool:
        """Remove bloqueio ativo e limpa histórico de falhas da origem."""
        chave = self._normalizar_origem(origem)
        with self._lock:
            bloqueado = self._bloqueios_ate.pop(chave, None) is not None
            self._falhas_por_origem.pop(chave, None)
        if bloqueado:
            self._registrar("INFO", f"Bloqueio liberado para origem '{chave}'.")
        return bloqueado

    def registrar_falha(self, origem: str, motivo: str = "FALHA_ACESSO") -> bool:
        """
        Registra uma tentativa falha para a origem.
        Retorna True se o limite foi atingido e a origem passou a ficar bloqueada.
        """
        chave = self._normalizar_origem(origem)
        motivo_limpo = (motivo or "FALHA_ACESSO").strip()
        agora = time.monotonic()
        limite_janela = agora - self.janela_segundos

        with self._lock:
            fila = self._falhas_por_origem[chave]
            while fila and fila[0] < limite_janela:
                fila.popleft()
            fila.append(agora)

            if len(fila) >= self.max_falhas:
                fila.clear()
                self._bloqueios_ate[chave] = agora + self.duracao_bloqueio_segundos
                self._registrar(
                    "CRITICO",
                    f"Intrusão/força bruta detectada em '{chave}' ({motivo_limpo}). Bloqueio ativado.",
                )
                return True

        self._registrar("ALERTA", f"Falha registrada para '{chave}': {motivo_limpo}.")
        return False

    def inspecionar_entrada(self, conteudo: str, origem: str = "LOCAL") -> tuple[bool, list[str]]:
        """
        Analisa um texto/comando em busca de padrões suspeitos conhecidos.
        Retorna (True, []) se seguro ou (False, [motivos]) se houver suspeita.
        """
        if not isinstance(conteudo, str) or not conteudo:
            return True, []

        achados: list[str] = []
        for idx, padrao in enumerate(PADROES_SUSPEITOS, start=1):
            if padrao.search(conteudo):
                achados.append(f"PADRAO_SUSPEITO_{idx}")

        if achados:
            self._registrar(
                "ALERTA",
                f"Entrada suspeita de '{origem}' detectada: {', '.join(achados)}.",
            )
            return False, achados

        return True, []