# =====================================================================
# ARQUIVO: security/homomorphic_biometrics.py
# =====================================================================

import tenseal as ts
import numpy as np
from .log_seguro import LogSeguro

logger = LogSeguro()

class HomomorphicBiometrics:
    """
    Motor de Criptografia Homomórfica para Vetores Biométricos.
    Permite calcular a similaridade de vetores sem nunca descriptografá-los na RAM.
    """

    def __init__(self):
        # Inicializa o contexto CKKS (esquema ideal para números reais / vetores de keypoints)
        # Parâmetros de segurança de nível corporativo (Poly modulus degree 8192)
        self.context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192,
            coeff_mod_bit_sizes=[60, 40, 40, 60]
        )
        self.context.global_scale = 2.40
        self.context.generate_galois_keys()

    def exportar_contexto_publico(self) -> bytes:
        """Exporta apenas a chave pública para que os terminais criptografem os dados na origem."""
        return self.context.serialize(save_secret_key=False)

    def criptografar_vetor(self, vetor_keypoints: list) -> bytes:
        """Criptografa o vetor de keypoints do cliente antes de enviá-lo para o servidor."""
        vetor_f64 = [float(x) for x in vetor_keypoints]
        encrypted_vector = ts.ckks_vector(self.context, vetor_f64)
        return encrypted_vector.serialize()

    def calcular_similaridade_homomorfica(self, vetor_cifrado_bytes: bytes, vetor_referencia_cifrado_bytes: bytes) -> float:
        """
        Calcula o produto interno (similaridade) diretamente com os dados 100% cifrados.
        O servidor processa a matemática sem saber quais são os números reais.
        """
        try:
            # Reconstituir os vetores cifrados no contexto de segurança
            v1 = ts.ckks_vector_from(self.context, vetor_cifrado_bytes)
            v2 = ts.ckks_vector_from(self.context, vetor_referencia_cifrado_bytes)

            # Operação homomórfica: Multiplicação direta na matriz cifrada
            resultado_cifrado = v1.dot(v2)
            
            # Descriptografa apenas o resultado final da pontuação (opcional, ou mantido cifrado)
            pontuacao_final = resultado_cifrado.decrypt()[0]
            
            return float(pontuacao_final)

        except Exception as e:
            logger.registrar("SISTEMA_HOMOMORFICO", "ERRO", f"Falha no cálculo cifrado: {str(e)}")
            raise RuntimeError(f"Erro crítico em criptografia homomórfica: {e}")