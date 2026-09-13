import jwt
import datetime
import hashlib

class SessionManager:
    # Em um sistema real, a SECRET_KEY deve vir de uma variável de ambiente (nunca hardcoded)
    SECRET_KEY = "CHAVE_SECRETA_SUPER_BLINDADA_2026"

    @staticmethod
    def gerar_token(usuario_id, ip_origem, hardware_fingerprint):
        """Gera um token vinculado ao usuário e ao seu dispositivo/rede."""
        payload = {
            "sub": usuario_id,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            # Bind de segurança: O token só é válido para este IP e este Hardware
            "context_hash": hashlib.sha256(f"{ip_origem}{hardware_fingerprint}".encode()).hexdigest()
        }
        return jwt.encode(payload, SessionManager.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def validar_token(token, ip_atual, hardware_fingerprint_atual):
        """Valida o token e verifica se o contexto atual coincide com o de origem."""
        try:
            payload = jwt.decode(token, SessionManager.SECRET_KEY, algorithms=["HS256"])
            
            # Recalcula o hash do contexto atual para comparar
            hash_atual = hashlib.sha256(f"{ip_atual}{hardware_fingerprint_atual}".encode()).hexdigest()
            
            if payload["context_hash"] != hash_atual:
                return {"valido": False, "erro": "Sequestro de Sessão Detectado"}
                
            return {"valido": True, "usuario_id": payload["sub"]}
            
        except jwt.ExpiredSignatureError:
            return {"valido": False, "erro": "Sessão Expirada"}
        except Exception as e:
            return {"valido": False, "erro": str(e)}