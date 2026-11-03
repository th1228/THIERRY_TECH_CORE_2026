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
import shutil

# O caminho exato onde o arquivo está agora
ARQUIVO_ORIGEM = os.path.join("security", "seguranca_audit.db")
PASTA_DESTINO = "C:/TTC_SECURE_STORAGE"
DESTINO_FINAL = os.path.join(PASTA_DESTINO, "seguranca_audit.db")

def mover_agora():
    if not os.path.exists(ARQUIVO_ORIGEM):
        print(f"ERRO: Não encontrei o arquivo em: {os.path.abspath(ARQUIVO_ORIGEM)}")
        return

    if not os.path.exists(PASTA_DESTINO):
        os.makedirs(PASTA_DESTINO)
    
    shutil.move(ARQUIVO_ORIGEM, DESTINO_FINAL)
    
    # Cria o arquivo de configuração
    with open("db_config.py", "w") as f:
        f.write(f"PATH_DB = '{DESTINO_FINAL.replace(chr(92), '/')}'")
    
    print(f"SUCESSO! O banco foi movido para: {DESTINO_FINAL}")

if __name__ == "__main__":
    mover_agora()