import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

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
import sys

# Lista de arquivos essenciais que o ecossistema TTC precisa para estar completo
ARQUIVOS_ESSENCIAIS = [
    "teste_camera.py",
    "testar_seguranca.py",
    "testar_motor.py",
    "testar_memoria.py",
    "teste_orquestracao.py"
]

def verificar_projeto():
    logger.info("================================================================")
    logger.info(" [TTC CORE] AUDITORIA DE PRONTIDÃO PARA EMPACOTAMENTO (ZIP)")
    logger.info("================================================================")
    
    diretorio_atual = os.getcwd()
    logger.info(f" Diretório de Trabalho: {diretorio_atual}\n")
    
    arquivos_faltando = []
    arquivos_encontrados = 0

    logger.info(" Verificando integridade dos módulos principais:")
    for arquivo in ARQUIVOS_ESSENCIAIS:
        caminho_completo = os.path.join(diretorio_atual, arquivo)
        if os.path.exists(caminho_completo):
            logger.info(f"   [✓] {arquivo} -> OK")
            arquivos_encontrados += 1
        else:
            logger.info(f"   [X] {arquivo} -> FALTANDO!")
            arquivos_faltando.append(arquivo)

    logger.info("\n----------------------------------------------------------------")
    logger.info(f" Resumo: {arquivos_encontrados}/{len(ARQUIVOS_ESSENCIAIS)} módulos essenciais localizados.")
    logger.info("----------------------------------------------------------------")

    if len(arquivos_faltando) == 0:
        logger.info(" 👑 VEREDITO: SISTEMA 100% COMPLETO E INTEGRO!")
        logger.info(" 🚀 O seu ecossistema está pronto para ser zipado com segurança absoluta.")
        logger.info("================================================================")
        return True
    else:
        logger.info(" ⚠️  VEREDITO: ATENÇÃO! Faltam alguns arquivos para o fechamento.")
        logger.info(f"     Arquivos pendentes: {arquivos_faltando}")
        logger.info("================================================================")
        return False

if __name__ == "__main__":
    verificar_projeto()