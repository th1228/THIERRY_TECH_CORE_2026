 # =====================================================================
# ARQUIVO: security/portaria.py
# =====================================================================

import sys
import os
import time
import threading
from typing import Optional

# TÉCNICA DE BLINDAGEM DE PATH: Garante que o Python encontre os módulos na raiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from security.schemas import PayloadSeguro
from security.crypto_engine import CryptoEngine
from security.log_seguro import LogSeguro
from security.session_manager import SessionManager
from security.input_sanitizer import InputSanitizer
from database.db_manager import DBManager  # <--- NOSSO NOVO GUARDIÃO
from nacl.signing import VerifyKey

logger = LogSeguro()

class NonceCache:
    def __init__(self, ttl_seconds: int = 30, teto_maximo: int = 50000):
        self.cache = {}
        self.ttl = ttl_seconds
        self.teto_maximo = teto_maximo
        self._lock = threading.Lock()

    def validar_e_registrar(self, nonce: str) -> bool:
        with self._lock:
            agora = time.time()
            expirados = [k for k, v in self.cache.items() if agora - v > self.ttl]
            for k in expirados:
                del self.cache[k]
            if len(self.cache) >= self.teto_maximo or nonce in self.cache:
                return False
            self.cache[nonce] = agora
            return True

nonce_cache = NonceCache(ttl_seconds=30, teto_maximo=50000)

def verificar_acesso(dados_json: dict, 
                     verify_key: VerifyKey, 
                     token: Optional[str] = None, 
                     ip: str = "0.0.0.0", 
                     hardware_id: str = "unknown") -> bool:
    try:
        # 1. Sanitização
        if 'id_scanner' in dados_json:
            dados_json['id_scanner'] = InputSanitizer.limpar_string(str(dados_json['id_scanner']))

        # 2. Validação de Sessão
        if token:
            validacao_sessao = SessionManager.validar_token(token, ip, hardware_id)
            if not validacao_sessao["valido"]:
                logger.registrar("SISTEMA", "SEQUESTRO_SESSAO", f"Bloqueio: {validacao_sessao.get('erro', 'Erro')}")
                return False

        # 3. Validação do Contrato
        payload = PayloadSeguro(**dados_json)
        
        # 4. Validação Anti-Replay
        nonce_str = getattr(payload, 'nonce', str(payload.payload_biometrico[:12]))
        if not nonce_cache.validar_e_registrar(nonce_str):
            logger.registrar(payload.id_scanner, "FALHA_SECURITY", "Tentativa de Replay.")
            return False

        # 5. Validação Criptográfica (Assinatura)
        if CryptoEngine.validar_assinatura(verify_key, payload.payload_biometrico, payload.assinatura):
            
            # 6. VERIFICAÇÃO DE PERMISSÃO RBAC (O PASSO FINAL)
            if DBManager.verificar_permissao(payload.id_scanner):
                logger.registrar(payload.id_scanner, "SUCESSO", "Acesso liberado com autorização RBAC.")
                return True
            else:
                logger.registrar(payload.id_scanner, "FALHA_PERMISSAO", "Assinatura OK, mas scanner não autorizado.")
                return False
        else:
            logger.registrar(payload.id_scanner, "FALHA", "Assinatura inválida.")
            return False

    except Exception as e:
        logger.registrar("SISTEMA", "ERRO", f"Erro crítico: {str(e)}")
        return False