
# --- PONTE DE MEMÓRIA AUTOMÁTICA (THIERRY TECH) ---
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:
        class MemoriaMock:
            def salvar_dados(self, chave, valor): pass
            def registrar(self, chave, valor): pass
            def ler_dados(self, chave): return None
        memoria = MemoriaMock()
# ---------------------------------------------------

import sys, os

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys, os

import sqlite3
import os

def ler_banco():
    # Define o diretório atual do script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Constrói o caminho para o banco dentro da pasta 'storage'
    db_path = os.path.join(base_dir, '..', 'storage', 'thierry_tech_global.db')
    
    if not os.path.exists(db_path):
        print(f"[ERRO] Banco não encontrado em: {db_path}")
        return

    # Conecta ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Busca todos os registros
    cursor.execute("SELECT * FROM clientes")
    registros = cursor.fetchall()
    
    print(f"--- Registros encontrados no banco: {len(registros)} ---")
    for linha in registros:
        print(linha)
        
    conn.close()

if __name__ == "__main__":
    ler_banco()