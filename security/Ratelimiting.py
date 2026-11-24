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

import os
import sqlite3
import threading
import time
from collections import defaultdict
from typing import Optional


class RateLimitError(Exception):
    """Exceção levantada quando o limite de requisições é excedido."""
    def __init__(self, identifier: str, retry_after: float):
        self.identifier = identifier
        self.retry_after = round(retry_after, 2)
        super().__init__(
            f"Limite excedido para '{identifier}'. Tente novamente em {self.retry_after}s."
        )


class RateLimiter:
    def __init__(
        self,
        max_calls: int = 5,
        period_seconds: float = 60.0,
        db_path: Optional[str] = "storage/rate_limit.db",
    ):
        self.max_calls = max_calls
        self.period = period_seconds
        self.db_path: Optional[str] = db_path
        self._lock = threading.Lock()
        self._memory_store: dict[str, list[float]] = defaultdict(list)

        if self.db_path is not None:
            self._init_db(self.db_path)

    def _connect(self, db_path: str) -> sqlite3.Connection:
        return sqlite3.connect(db_path, timeout=10.0)

    def _init_db(self, db_path: str) -> None:
        folder = os.path.dirname(db_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        conn = self._connect(db_path)
        try:
            with conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS rate_limits (
                        identifier TEXT NOT NULL,
                        timestamp REAL NOT NULL
                    )
                    """
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_rate_id ON rate_limits (identifier)"
                )
        finally:
            conn.close()

    def check(self, identifier: str) -> None:
        """Verifica e registra uma chamada. Levanta RateLimitError se bloquear."""
        if not identifier:
            raise ValueError("O identificador do rate limit não pode ser vazio.")

        now = time.time()
        window_start = now - self.period

        with self._lock:
            if self.db_path is not None:
                self._check_sqlite(self.db_path, identifier, now, window_start)
            else:
                self._check_memory(identifier, now, window_start)

    def _check_memory(self, identifier: str, now: float, window_start: float) -> None:
        timestamps = [t for t in self._memory_store[identifier] if t > window_start]
        if len(timestamps) >= self.max_calls:
            retry_after = (timestamps[0] + self.period) - now
            self._memory_store[identifier] = timestamps
            raise RateLimitError(identifier, max(0.0, retry_after))

        timestamps.append(now)
        self._memory_store[identifier] = timestamps

    def _check_sqlite(
        self, db_path: str, identifier: str, now: float, window_start: float
    ) -> None:
        conn = self._connect(db_path)
        try:
            with conn:
                conn.execute(
                    "DELETE FROM rate_limits WHERE identifier = ? AND timestamp <= ?",
                    (identifier, window_start),
                )
                cursor = conn.execute(
                    "SELECT timestamp FROM rate_limits WHERE identifier = ? ORDER BY timestamp ASC",
                    (identifier,),
                )
                timestamps = [float(row[0]) for row in cursor.fetchall()]

                if len(timestamps) >= self.max_calls:
                    retry_after = (timestamps[0] + self.period) - now
                    raise RateLimitError(identifier, max(0.0, retry_after))

                conn.execute(
                    "INSERT INTO rate_limits (identifier, timestamp) VALUES (?, ?)",
                    (identifier, now),
                )
        finally:
            conn.close()

    def reset(self, identifier: str) -> None:
        """Limpa o histórico de um identificador específico."""
        with self._lock:
            if self.db_path is not None:
                conn = self._connect(self.db_path)
                try:
                    with conn:
                        conn.execute(
                            "DELETE FROM rate_limits WHERE identifier = ?",
                            (identifier,),
                        )
                finally:
                    conn.close()
            else:
                self._memory_store.pop(identifier, None)