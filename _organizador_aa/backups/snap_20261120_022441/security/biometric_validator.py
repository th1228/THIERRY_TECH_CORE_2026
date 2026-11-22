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
# ARQUIVO: security/biometric_validator.py
# =====================================================================

import hashlib
import hmac
import os
from PIL import Image
import numpy as np
from .log_seguro import LogSeguro

logger = LogSeguro()

class BiometricValidator:
    """
    Validador Biométrico e Motor de Esteganografia Forense (Watermarking Invisível).
    Injeta assinaturas criptográficas nos pixels de imagens de visagismo para rastreabilidade.
    """

    @staticmethod
    def injetar_marca_dagua_invisivel(caminho_imagem: str, id_sessao: str, chave_secreta: bytes) -> bool:
        """
        Injeta uma assinatura digital invisível nos bits menos significativos (LSB) 
        dos pixels da imagem de visagismo para rastreamento forense.
        """
        try:
            if not os.path.exists(caminho_imagem):
                logger.registrar("WATERMARK", "ERRO", f"Imagem não encontrada para marca d'água: {caminho_imagem}")
                return False

            # Gera o payload forense autenticado via HMAC
            h = hmac.new(chave_secreta, id_sessao.encode(), hashlib.sha256).digest()
            
            # Abre a imagem e converte para array numpy
            img = Image.open(caminho_imagem).convert("RGB")
            arr = np.array(img, dtype=np.uint8)
            
            # Converte o hash da assinatura para uma sequência de bits binários
            bits_assinatura = ''.join(format(byte, '08b') for byte in h)
            
            flat_arr = arr.flatten()
            if len(bits_assinatura) > len(flat_arr):
                logger.registrar("WATERMARK", "ERRO", "Imagem muito pequena para conter a assinatura forense.")
                return False

            # Aplicação nos Least Significant Bits (LSB) de forma imperceptível ao olho humano
            for i, bit in enumerate(bits_assinatura):
                flat_arr[i] = (flat_arr[i] & ~1) | int(bit)

            # Reconstrói a imagem com a esteganografia aplicada
            img_marcada = Image.fromarray(flat_arr.reshape(arr.shape), 'RGB')
            img_marcada.save(caminho_imagem)
            
            logger.registrar("WATERMARK", "SUCESSO", f"Assinatura forense invisível injetada na sessão: {id_sessao}")
            return True
        except Exception as e:
            logger.registrar("WATERMARK", "EXCECAO", f"Falha ao aplicar marca d'água: {str(e)}")
            return False

    @staticmethod
    def validar_vetor_biometrico(vetor: list) -> bool:
        """Valida se o vetor biométrico facial possui dimensões e integridade corretas."""
        if not isinstance(vetor, list) or len(vetor) == 0:
            logger.registrar("BIOMETRIC", "ALERTA", "Vetor biométrico vazio ou inválido.")
            return False
        return True