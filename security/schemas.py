# =====================================================================
# ARQUIVO: security/schemas.py
# =====================================================================

from pydantic import BaseModel, Field, field_validator
from typing import Optional
import time

class PayloadSeguro(BaseModel):
    id_scanner: str = Field(..., min_length=5)
    payload_biometrico: str  # Hash SHA-256 ou dados cifrados
    timestamp: float         # Unix timestamp
    nonce: str               # Chave única para evitar ataque de replay
    assinatura: str          # Assinatura digital (Ed25519 ou PQC)

    @field_validator('timestamp')
    @classmethod
    def validar_janela_tempo(cls, v: float) -> float:
        """
        Rejeita pacotes com mais de 30 segundos de atraso.
        Isso impede que um ataque de 'replay' seja aceito.
        """
        if abs(time.time() - v) > 30:
            raise ValueError("Pacote expirado: Risco de ataque de Replay.")
        return v