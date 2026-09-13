# /security/integrity_verifier.py
import hashlib
import os

class IntegrityVerifier:
    @staticmethod
    def calcular_hash(caminho_arquivo):
        """Calcula o hash SHA-256 de um arquivo crítico."""
        sha256 = hashlib.sha256()
        try:
            with open(caminho_arquivo, "rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except FileNotFoundError:
            return None

    @staticmethod
    def verificar_arquivo(caminho_arquivo, hash_esperado):
        """Compara o hash atual com o hash 'dourado' (original)."""
        hash_atual = IntegrityVerifier.calcular_hash(caminho_arquivo)
        return hash_atual == hash_esperado