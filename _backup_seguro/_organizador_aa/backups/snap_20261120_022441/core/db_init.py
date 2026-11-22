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

import sqlite3
import os

# Caminho para o banco dentro da pasta 'database' que você já tem
db_path = os.path.join('database', 'sistema_seguro.db')

def configurar_banco():
    # Garante que a pasta existe (só por segurança)
    if not os.path.exists('database'):
        os.makedirs('database')
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Cria a tabela de permissões (RBAC)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissao_scanner (
            id_scanner TEXT PRIMARY KEY,
            permissao_nivel TEXT,
            liberado INTEGER
        )
    ''')
    
    # Insere um scanner de teste (o seu admin)
    cursor.execute("INSERT OR IGNORE INTO permissao_scanner VALUES ('THIERRY_ADMIN', 'ADMIN', 1)")
    
    conn.commit()
    conn.close()
    print("Banco de dados configurado com sucesso!")

if __name__ == "__main__":
    configurar_banco()