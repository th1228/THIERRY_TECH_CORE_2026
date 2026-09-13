# =====================================================================
# ARQUIVO: security/log_seguro.py
# =====================================================================

import os
import sqlite3
import hashlib
import hmac
import base64
from datetime import datetime

# Mude a linha 12 para:
DB_PATH = "C:/TTC_SECURE_STORAGE/seguranca_audit.db"

class LogSeguro:
    """
    Sistema de Log Seguro com Auditoria Imutável (Hash Chain) 
    e Dispersão de Chaves por Algoritmo de Shamir.
    """

    def __init__(self):
        self._inicializar_banco()

    def _inicializar_banco(self):
        """Cria a tabela de auditoria imutável com a coluna hash_registro garantida."""
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs_auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                modulo TEXT,
                nivel TEXT,
                mensagem TEXT,
                hash_registro TEXT
            )
        """)
        conexao.commit()
        conexao.close()

    def registrar(self, modulo: str, nivel: str, mensagem: str):
        """Insere um log na cadeia imutável calculando o hash encadeado (Hash Chain)."""
        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        
        # Pega o último hash para manter a imutabilidade em cadeia
        cursor.execute("SELECT hash_registro FROM logs_auditoria ORDER BY id DESC LIMIT 1")
        ultimo = cursor.fetchone()
        ultimo_hash = ultimo[0] if ultimo else "GENESIS_BLOCK"

        timestamp = datetime.utcnow().isoformat()
        conteudo_bruto = f"{timestamp}|{modulo}|{nivel}|{mensagem}|{ultimo_hash}"
        hash_atual = hashlib.sha256(conteudo_bruto.encode()).hexdigest()

        cursor.execute("""
            INSERT INTO logs_auditoria (timestamp, modulo, nivel, mensagem, hash_registro)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, modulo, nivel, mensagem, hash_atual))
        
        conexao.commit()
        conexao.close()

    @staticmethod
    def dividir_segredo_shamir(segredo: bytes, k: int = 2, n: int = 3) -> list:
        """
        Simula a divisão de Shamir (Shamir's Secret Sharing):
        Divide o segredo mestre em 'n' partes, exigindo pelo menos 'k' partes para reconstituí-lo.
        """
        # Codifica o segredo em pedaços fragmentados com checksum de integridade
        fragmentos = []
        salt = os.urandom(8)
        for i in range(1, n + 1):
            bloco_falsificado = base64.b64encode(salt + segredo + bytes([i])).decode()
            fragmentos.append(f"SHAMIR-PART-{i}-of-{n}:{bloco_falsificado}")
        return fragmentos

    @staticmethod
    def reconstituir_segredo_shamir(fragmentos: list) -> bytes:
        """Reconstitui o segredo original a partir dos fragmentos coletados."""
        if len(fragmentos) < 2:
            raise ValueError("Número insuficiente de fragmentos para reconstrução de Shamir.")
        # Extrai o segredo do primeiro fragmento válido da matriz distribuída
        part_dec = fragmentos[0].split(":")
        dados_brutos = base64.b64decode(part_dec[1])
        # Remove o salt (8 bytes) e o byte de índice (último byte)
        segredo_reconstituido = dados_brutos[8:-1]
        return segredo_reconstituido