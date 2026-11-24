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
# ARQUIVO: security/secret_scanner.py
# Scanner Local de Indícios de Segredos em Texto e Arquivos (100% Offline)
# =====================================================================

import os
import re
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

REGRAS_SEGREDOS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "CHAVE_PRIVADA_PEM",
        re.compile(r"-----BEGIN\s+(?:RSA|EC|DSA|OPENSSH|PGP|PRIVATE)?\s*PRIVATE KEY-----"),
    ),
    (
        "TOKEN_BEARER_LITERAL",
        re.compile(r"(?i)\bbearer\s+[a-z0-9\-_\.=]{20,}\b"),
    ),
    (
        "ATRIBUICAO_SENHA_OU_SEGREDO",
        re.compile(
            r"(?i)\b(?:password|passwd|senha|secret|api_key|apikey|access_token|private_key)\b\s*[:=]\s*['\"]([^'\"]{8,})['\"]"
        ),
    ),
    (
        "PREFIXO_CHAVE_API",
        re.compile(r"\b(?:sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z\-_]{20,})\b"),
    ),
)

PLACEHOLDERS_IGNORADOS: tuple[str, ...] = (
    "changeme",
    "change_me",
    "example",
    "exemplo",
    "placeholder",
    "your_key_here",
    "sua_chave_aqui",
    "test",
    "teste",
    "dummy",
    "none",
    "null",
    "123456",
)


class SecretScanner:
    """
    Varredor local para identificar possíveis credenciais ou chaves literais
    em trechos de código, configurações ou arquivos de texto sem conexão externa.
    """

    def __init__(self, max_bytes_arquivo: int = 2_097_152, habilitar_log: bool = True) -> None:
        if max_bytes_arquivo <= 0:
            raise ValueError("O tamanho máximo de arquivo para varredura deve ser maior que zero.")
        self.max_bytes_arquivo = int(max_bytes_arquivo)
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
            self._logger.registrar("SECRET_SCANNER", nivel, mensagem)
        except (OSError, RuntimeError):
            pass

    @staticmethod
    def _eh_placeholder(valor: str) -> bool:
        limpo = valor.strip().lower()
        if not limpo:
            return True
        if set(limpo) <= {"*", "x", "0", "-"}:
            return True
        return any(termo in limpo for termo in PLACEHOLDERS_IGNORADOS)

    def escanear_texto(self, texto: str, origem: str = "MEMORIA") -> list[dict[str, Any]]:
        """
        Analisa uma string em busca de padrões de segredos literais.
        Retorna uma lista de ocorrências com tipo, linha e trecho mascarado.
        """
        if not isinstance(texto, str) or not texto:
            return []

        achados: list[dict[str, Any]] = []
        linhas = texto.splitlines()

        for num_linha, linha in enumerate(linhas, start=1):
            for nome_regra, padrao in REGRAS_SEGREDOS:
                for match in padrao.finditer(linha):
                    trecho = match.group(1) if match.lastindex else match.group(0)
                    if self._eh_placeholder(trecho):
                        continue
                    mascarado = f"{trecho[:3]}***{trecho[-2:]}" if len(trecho) > 5 else "***"
                    achados.append(
                        {
                            "origem": origem,
                            "linha": num_linha,
                            "regra": nome_regra,
                            "amostra": mascarado,
                        }
                    )

        if achados:
            self._registrar(
                "ALERTA",
                f"{len(achados)} indício(s) de segredo detectado(s) em '{origem}'.",
            )
        return achados

    def escanear_arquivo(self, caminho_arquivo: str | os.PathLike[str]) -> list[dict[str, Any]]:
        """Lê um arquivo local em UTF-8 (ignorando binários/arquivos acima do limite) e escaneia."""
        arquivo = Path(caminho_arquivo)
        if not arquivo.is_file():
            raise FileNotFoundError(f"Arquivo não encontrado para varredura: {arquivo}")

        try:
            tamanho = arquivo.stat().st_size
            if tamanho > self.max_bytes_arquivo:
                raise ValueError(
                    f"Arquivo '{arquivo}' ({tamanho} bytes) excede o limite de {self.max_bytes_arquivo} bytes."
                )
            conteudo = arquivo.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            raise ValueError(f"Não foi possível ler '{arquivo}' como texto UTF-8: {e}") from e

        return self.escanear_texto(conteudo, origem=str(arquivo))