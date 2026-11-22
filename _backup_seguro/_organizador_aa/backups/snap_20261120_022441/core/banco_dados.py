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

# -*- coding: utf-8 -*-
import sys
import os
import sqlite3

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

# Caminho do banco de dados centralizado na pasta 'storage'
DB_PATH = os.path.join(ROOT_DIR, 'storage', 'thierry_tech_global.db')

def inicializar_banco():
    """Cria a estrutura da tabela se ela não existir e sincroniza com a memória 🧠."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    nome TEXT, 
                    bio_age REAL, 
                    osteometria TEXT, 
                    status TEXT DEFAULT 'ativo')''')
    conn.commit()
    conn.close()
    
    try:
        memoria.salvar_dados("banco_status", {"status": "inicializado", "path": DB_PATH})
    except Exception:
        pass

def salvar_cliente(nome, bio_age, osteometria):
    """Salva um novo registro no banco e atualiza a Memória Comum 🧠."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('INSERT INTO clientes (nome, bio_age, osteometria) VALUES (?, ?, ?)', 
                 (nome, bio_age, osteometria))
    conn.commit()
    conn.close()
    print(f"[BANCO] {nome} registrado com sucesso.")
    
    try:
        memoria.salvar_dados("ultimo_cliente_salvo", {
            "nome": nome, 
            "bio_age": bio_age, 
            "osteometria": osteometria
        })
    except Exception:
        pass

def buscar_cliente(nome):
    """Busca um cliente específico pelo nome."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE nome = ?', (nome,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def listar_todos():
    """Retorna todos os clientes cadastrados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    todos = cursor.fetchall()
    conn.close()
    return todos

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    inicializar_banco()
    clientes = listar_todos()
    return {
        "status": "Banco operacional",
        "total_clientes": len(clientes),
        "clientes": clientes
    }

if __name__ == "__main__":
    inicializar_banco()
    print("Banco de dados configurado e integrado com sucesso.")