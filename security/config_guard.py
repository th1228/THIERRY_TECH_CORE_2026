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
# ARQUIVO: security/config_guard.py
# Guarda Local de Configuração e Parâmetros Seguros (100% Offline)
# =====================================================================

import json
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

CHAVES_SENSIVEIS: tuple[str, ...] = (
    "password",
    "senha",
    "secret",
    "token",
    "api_key",
    "apikey",
    "private_key",
    "master_seed",
)


class ConfigGuard:
    """
    Valida dicionários e arquivos JSON de configuração em ambiente 100% offline,
    alertando sobre segredos em texto claro, tipos inválidos ou valores fora de faixa.
    """

    def __init__(self, habilitar_log: bool = True) -> None:
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
            self._logger.registrar("CONFIG_GUARD", nivel, mensagem)
        except (OSError, RuntimeError):
            pass

    def carregar_json_seguro(self, caminho_arquivo: str | os.PathLike[str]) -> dict[str, Any]:
        """Carrega e valida um arquivo JSON de configuração a partir do disco local."""
        arquivo = Path(caminho_arquivo)
        if not arquivo.is_file():
            raise FileNotFoundError(f"Arquivo de configuração não encontrado: {arquivo}")

        try:
            with arquivo.open("r", encoding="utf-8") as f:
                dados = json.load(f)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as e:
            self._registrar("ERRO", f"Falha ao ler configuração em '{arquivo}': {e}")
            raise ValueError(f"Configuração inválida em '{arquivo}': {e}") from e

        if not isinstance(dados, dict):
            raise ValueError("O arquivo de configuração deve conter um objeto JSON na raiz.")

        return dados

    def auditar_segredos_em_config(self, config: dict[str, Any]) -> list[str]:
        """
        Verifica se há campos com nomes sensíveis preenchidos com strings não vazias
        diretamente na configuração (em vez de virem via variável de ambiente/cofre).
        Retorna a lista de chaves sinalizadas.
        """
        if not isinstance(config, dict):
            raise TypeError("A configuração deve ser um dicionário (dict).")

        alertas: list[str] = []

        def _varrer(obj: Any, prefixo: str = "") -> None:
            if isinstance(obj, dict):
                for chave, valor in obj.items():
                    chave_str = str(chave)
                    caminho_chave = f"{prefixo}.{chave_str}" if prefixo else chave_str
                    nome_lower = chave_str.lower()

                    if isinstance(valor, str) and valor.strip():
                        if any(termo in nome_lower for termo in CHAVES_SENSIVEIS):
                            alertas.append(caminho_chave)

                    if isinstance(valor, (dict, list, tuple)):
                        _varrer(valor, caminho_chave)
            elif isinstance(obj, (list, tuple)):
                for idx, item in enumerate(obj):
                    caminho_item = f"{prefixo}[{idx}]"
                    if isinstance(item, (dict, list, tuple)):
                        _varrer(item, caminho_item)

        _varrer(config)
        if alertas:
            self._registrar(
                "ALERTA",
                f"Possíveis segredos literais encontrados na configuração: {', '.join(alertas)}.",
            )
        return alertas

    def validar_intervalo_numerico(
        self,
        config: dict[str, Any],
        chave: str,
        minimo: float,
        maximo: float,
        permitir_bool: bool = False,
    ) -> float:
        """
        Garante que um parâmetro numérico exista em 'config', tenha tipo válido
        e esteja dentro de [minimo, maximo].
        """
        if not isinstance(config, dict):
            raise TypeError("A configuração deve ser um dicionário (dict).")
        if chave not in config:
            raise KeyError(f"Parâmetro obrigatório ausente na configuração: '{chave}'.")

        valor = config[chave]
        if isinstance(valor, bool) and not permitir_bool:
            raise TypeError(f"Parâmetro '{chave}' não pode ser booleano.")
        if not isinstance(valor, (int, float)):
            raise TypeError(f"Parâmetro '{chave}' deve ser numérico.")

        numero = float(valor)
        if numero < minimo or numero > maximo:
            raise ValueError(
                f"Parâmetro '{chave}' ({numero}) fora do intervalo permitido [{minimo}, {maximo}]."
            )

        return numero

    def exigir_modo_offline(self, config: dict[str, Any], chave_offline: str = "modo_offline") -> bool:
        """Valida que a flag de operação offline esteja explicitamente habilitada (True)."""
        if not isinstance(config, dict):
            raise TypeError("A configuração deve ser um dicionário (dict).")
        valor = config.get(chave_offline)
        if valor is not True:
            self._registrar("CRITICO", f"Flag '{chave_offline}' não está habilitada como True.")
            raise ValueError(f"A configuração exige '{chave_offline}=True' para operação segura.")
        return True