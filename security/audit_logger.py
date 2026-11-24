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
# ARQUIVO: security/audit_logger.py
# Registrador de Auditoria Imutável (Hash Chain) em SQLite Local
# =====================================================================

import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_AUDIT_DB = Path("C:/TTC_SECURE_STORAGE/audit_trail.db")


class AuditLogger:
    """
    Registra eventos de auditoria em banco SQLite local com encadeamento
    SHA-256 (Hash Chain) para detecção de adulteração em ambiente offline.
    """

    def __init__(self, db_path: str | os.PathLike[str] | None = None) -> None:
        caminho_env = os.getenv("MIBO_AUDIT_DB_PATH")
        escolhido = db_path or caminho_env or DEFAULT_AUDIT_DB
        self.db_path = Path(escolhido)
        self._inicializar_banco()

    def _conectar(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conexao = sqlite3.connect(str(self.db_path), timeout=10.0)
        conexao.row_factory = sqlite3.Row
        return conexao

    def _inicializar_banco(self) -> None:
        """Cria a tabela de eventos de auditoria caso ainda não exista."""
        try:
            with self._conectar() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS audit_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp_utc TEXT NOT NULL,
                        categoria TEXT NOT NULL,
                        severidade TEXT NOT NULL,
                        ator TEXT NOT NULL,
                        detalhes_json TEXT NOT NULL,
                        hash_anterior TEXT NOT NULL,
                        hash_atual TEXT NOT NULL
                    )
                    """
                )
                conexao.commit()
        except (OSError, sqlite3.Error) as e:
            raise RuntimeError(f"Falha ao inicializar banco de auditoria: {e}") from e

    @staticmethod
    def _serializar_detalhes(detalhes: dict[str, Any] | str | None) -> str:
        if detalhes is None:
            return "{}"
        if isinstance(detalhes, str):
            return json.dumps({"mensagem": detalhes}, ensure_ascii=False, sort_keys=True)
        try:
            return json.dumps(detalhes, ensure_ascii=False, sort_keys=True, default=str)
        except (TypeError, ValueError):
            return json.dumps({"mensagem": str(detalhes)}, ensure_ascii=False, sort_keys=True)

    @staticmethod
    def _calcular_hash(
        timestamp_utc: str,
        categoria: str,
        severidade: str,
        ator: str,
        detalhes_json: str,
        hash_anterior: str,
    ) -> str:
        payload = (
            f"{timestamp_utc}|{categoria}|{severidade}|"
            f"{ator}|{detalhes_json}|{hash_anterior}"
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def registrar_evento(
        self,
        categoria: str,
        severidade: str = "INFO",
        ator: str = "SISTEMA_LOCAL",
        detalhes: dict[str, Any] | str | None = None,
    ) -> str:
        """
        Grava um novo evento encadeado na trilha de auditoria e retorna
        o hash SHA-256 gerado para o registro.
        """
        cat_limpa = (categoria or "GERAL").strip().upper()
        sev_limpa = (severidade or "INFO").strip().upper()
        ator_limpo = (ator or "SISTEMA_LOCAL").strip()
        detalhes_json = self._serializar_detalhes(detalhes)
        timestamp_utc = datetime.now(timezone.utc).isoformat()

        try:
            with self._conectar() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    "SELECT hash_atual FROM audit_events ORDER BY id DESC LIMIT 1"
                )
                ultimo = cursor.fetchone()
                hash_anterior = ultimo["hash_atual"] if ultimo else "GENESIS_AUDIT_BLOCK"

                hash_atual = self._calcular_hash(
                    timestamp_utc=timestamp_utc,
                    categoria=cat_limpa,
                    severidade=sev_limpa,
                    ator=ator_limpo,
                    detalhes_json=detalhes_json,
                    hash_anterior=hash_anterior,
                )

                cursor.execute(
                    """
                    INSERT INTO audit_events (
                        timestamp_utc,
                        categoria,
                        severidade,
                        ator,
                        detalhes_json,
                        hash_anterior,
                        hash_atual
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        timestamp_utc,
                        cat_limpa,
                        sev_limpa,
                        ator_limpo,
                        detalhes_json,
                        hash_anterior,
                        hash_atual,
                    ),
                )
                conexao.commit()
                return hash_atual
        except (OSError, sqlite3.Error) as e:
            raise RuntimeError(f"Falha ao registrar evento de auditoria: {e}") from e

    def verificar_integridade(self) -> tuple[bool, str]:
        """
        Confere toda a cadeia de hashes da tabela audit_events.
        Retorna (True, mensagem) se estiver íntegra ou (False, detalhe) se houver adulteração.
        """
        try:
            with self._conectar() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    """
                    SELECT
                        id,
                        timestamp_utc,
                        categoria,
                        severidade,
                        ator,
                        detalhes_json,
                        hash_anterior,
                        hash_atual
                    FROM audit_events
                    ORDER BY id ASC
                    """
                )
                linhas = cursor.fetchall()
        except (OSError, sqlite3.Error) as e:
            return False, f"Erro de acesso ao banco de auditoria: {e}"

        hash_esperado_anterior = "GENESIS_AUDIT_BLOCK"
        for linha in linhas:
            if linha["hash_anterior"] != hash_esperado_anterior:
                return (
                    False,
                    f"Quebra de encadeamento no registro id={linha['id']}.",
                )

            hash_recalculado = self._calcular_hash(
                timestamp_utc=linha["timestamp_utc"],
                categoria=linha["categoria"],
                severidade=linha["severidade"],
                ator=linha["ator"],
                detalhes_json=linha["detalhes_json"],
                hash_anterior=linha["hash_anterior"],
            )
            if hash_recalculado != linha["hash_atual"]:
                return (
                    False,
                    f"Hash divergente no registro id={linha['id']}.",
                )

            hash_esperado_anterior = linha["hash_atual"]

        return True, f"Trilha íntegra ({len(linhas)} registro(s) validado(s))."