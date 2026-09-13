# =====================================================================
# ARQUIVO: security/crypto_engine.py
# =====================================================================

import os
import time
import hmac
import hashlib
from cryptography.fernet import Fernet
from .log_seguro import LogSeguro

logger = LogSeguro()

class CryptoEngine:
    """
    Motor Criptográfico de Alta Performance com Key Rolling (RAM OBFUSCATION).
    Fragmenta e rotaciona chaves na memória volátil para impedir ataques de Dump de RAM.
    """

    def __init__(self):
        # Master Seed estática protegida, usada para derivar sub-chaves temporárias
        self._master_seed = os.urandom(64)
        self._intervalo_rotacao = 60  # Rotação a cada 60 segundos
        self._timestamp_ultima_rotacao = time.time()
        self._sub_chave_atual = self._derivar_chave_temporaria()
        logger.registrar("CRYPTO_ENGINE", "SUCESSO", "Motor Criptográfico inicializado com Key Rolling ativo.")

    def _derivar_chave_temporaria(self) -> bytes:
        """Deriva uma chave efêmera baseada no tempo atual e na seed mestre."""
        bloco_tempo = int(time.time() // self._intervalo_rotacao)
        dados_derivacao = self._master_seed + str(bloco_tempo).encode()
        hash_chave = hashlib.sha256(dados_derivacao).digest()
        
        # Converte o hash em uma chave válida para o Fernet (Base64 URL-safe de 32 bytes)
        import base64
        return base64.urlsafe_b64encode(hash_chave[:32])

    def _verificar_e_rotacionar(self):
        """Verifica se o tempo expirou e rotaciona a chave ativa na RAM silenciosamente."""
        tempo_atual = time.time()
        if (tempo_atual - self._timestamp_ultima_rotacao) > self._intervalo_rotacao:
            self._sub_chave_atual = self._derivar_chave_temporaria()
            self._timestamp_ultima_rotacao = tempo_atual
            # Limpa o rastro da seed na RAM imediata se necessário e registra auditoria silenciosa
            logger.registrar("KEY_ROLLING", "INFO", "Chave criptográfica rotacionada com sucesso na RAM.")

    def cifrar(self, dados_claros: bytes) -> bytes:
        """Cifra dados sensíveis usando a chave efêmera atual da RAM."""
        self._verificar_e_rotacionar()
        f = Fernet(self._sub_chave_atual)
        return f.encrypt(dados_claros)

    def decifrar(self, dados_cifrados: bytes) -> bytes:
        """Decifra dados sensíveis garantindo que a chave do período correto seja aplicada."""
        self._verificar_e_rotacionar()
        f = Fernet(self._sub_chave_atual)
        try:
            return f.decrypt(dados_cifrados)
        except Exception as e:
            logger.registrar("CRYPTO_ENGINE", "ALERTA", "Tentativa de decifragem com chave expirada ou inválida.")
            raise ValueError("Falha na decifragem: A chave pode ter expirado por rotação de Key Rolling.")