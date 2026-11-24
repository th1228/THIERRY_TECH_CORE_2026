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
# ARQUIVO: security/payload_validator.py
# Validador Local de Payloads e Estruturas de Dados (100% Offline)
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


class PayloadValidator:
    """
    Valida payloads em formato dict, JSON ou bytes/str quanto a tamanho,
    profundidade de estrutura, campos obrigatórios e caracteres de controle
    em ambiente 100% offline.
    """

    def __init__(
        self,
        max_bytes: int = 1_048_576,
        max_profundidade: int = 8,
    ) -> None:
        if max_bytes <= 0:
            raise ValueError("O tamanho máximo do payload deve ser maior que zero.")
        if max_profundidade <= 0:
            raise ValueError("A profundidade máxima do payload deve ser maior que zero.")

        self.max_bytes = int(max_bytes)
        self.max_profundidade = int(max_profundidade)
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
            self._logger.registrar("PAYLOAD_VALIDATOR", nivel, mensagem)
        except (OSError, RuntimeError):
            pass

    def _medir_profundidade(self, dado: Any, nivel_atual: int = 1) -> int:
        if nivel_atual > self.max_profundidade:
            return nivel_atual

        if isinstance(dado, dict):
            if not dado:
                return nivel_atual
            return max(
                self._medir_profundidade(valor, nivel_atual + 1)
                for valor in dado.values()
            )
        if isinstance(dado, (list, tuple)):
            if not dado:
                return nivel_atual
            return max(
                self._medir_profundidade(item, nivel_atual + 1)
                for item in dado
            )
        return nivel_atual

    @staticmethod
    def _contem_byte_nulo(dado: Any) -> bool:
        if isinstance(dado, str):
            return "\x00" in dado
        if isinstance(dado, (bytes, bytearray, memoryview)):
            return b"\x00" in bytes(dado)
        if isinstance(dado, dict):
            return any(
                PayloadValidator._contem_byte_nulo(k) or PayloadValidator._contem_byte_nulo(v)
                for k, v in dado.items()
            )
        if isinstance(dado, (list, tuple)):
            return any(PayloadValidator._contem_byte_nulo(item) for item in dado)
        return False

    def validar_bruto(self, payload: bytes | str) -> bytes:
        """
        Valida tamanho, decodificação UTF-8 e ausência de byte nulo em payloads brutos.
        Retorna os bytes normalizados ou levanta ValueError/TypeError.
        """
        if isinstance(payload, (bytes, bytearray, memoryview)):
            dados_bytes = bytes(payload)
        elif isinstance(payload, str):
            dados_bytes = payload.encode("utf-8")
        else:
            raise TypeError("Payload bruto deve ser bytes, bytearray, memoryview ou str.")

        if not dados_bytes:
            raise ValueError("Payload não pode estar vazio.")

        if len(dados_bytes) > self.max_bytes:
            self._registrar(
                "ALERTA",
                f"Payload rejeitado por exceder limite de {self.max_bytes} bytes ({len(dados_bytes)}).",
            )
            raise ValueError(
                f"Tamanho do payload ({len(dados_bytes)} bytes) excede o limite de {self.max_bytes}."
            )

        if b"\x00" in dados_bytes:
            self._registrar("ALERTA", "Payload rejeitado por conter byte nulo (\\x00).")
            raise ValueError("Payload contém byte nulo inválido.")

        try:
            dados_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError(f"Payload com codificação UTF-8 inválida: {e}") from e

        return dados_bytes

    def parsear_json_seguro(self, payload_json: bytes | str) -> dict[str, Any]:
        """Valida e converte um JSON em dicionário respeitando limites de tamanho e profundidade."""
        dados_bytes = self.validar_bruto(payload_json)
        try:
            objeto = json.loads(dados_bytes.decode("utf-8"))
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"JSON inválido no payload: {e}") from e

        if not isinstance(objeto, dict):
            raise ValueError("O payload JSON deve representar um objeto (dict) na raiz.")

        return self.validar_estrutura(objeto)

    def validar_estrutura(
        self,
        dados: dict[str, Any],
        campos_obrigatorios: list[str] | tuple[str, ...] | None = None,
    ) -> dict[str, Any]:
        """
        Valida se 'dados' é um dict íntegro, com profundidade controlada,
        sem bytes nulos e contendo todos os campos obrigatórios.
        """
        if not isinstance(dados, dict):
            raise TypeError("A estrutura do payload deve ser um dicionário (dict).")

        if self._contem_byte_nulo(dados):
            self._registrar("ALERTA", "Estrutura de payload rejeitada por conter byte nulo.")
            raise ValueError("Estrutura contém byte nulo inválido.")

        profundidade = self._medir_profundidade(dados)
        if profundidade > self.max_profundidade:
            self._registrar(
                "ALERTA",
                f"Estrutura rejeitada por profundidade excessiva ({profundidade} > {self.max_profundidade}).",
            )
            raise ValueError(
                f"Profundidade do payload ({profundidade}) excede o limite de {self.max_profundidade}."
            )

        if campos_obrigatorios:
            ausentes = [
                campo for campo in campos_obrigatorios
                if campo not in dados or dados[campo] is None or (isinstance(dados[campo], str) and not dados[campo].strip())
            ]
            if ausentes:
                raise ValueError(f"Campos obrigatórios ausentes ou vazios: {', '.join(ausentes)}.")

        return dados