import sqlite3
import os
from datetime import datetime

def criar_estrutura_forense(caminho_banco):
    """import os  # Esse import vai bem no topo do arquivo .py, junto com os outros
import sqlite3


def criar_estrutura_forense(caminho_banco):
    # --- VOCÊ COLA ESSA PARTE AQUI (ANTES DE CONECTAR) ---
    diretorio = os.path.dirname(caminho_banco)
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio, exist_ok=True)
    # -----------------------------------------------------

    # Aqui é a linha onde dava o erro, agora ela está protegida:
    conn = sqlite3.connect(caminho_banco)

    # ... resto do seu código que cria as tabelas
    """
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pericias_mandibulares (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        ramo_direito REAL,
        ramo_esquerdo REAL,
        indice_simetria REAL
    )
    """)
    
    conn.commit()
    conn.close()
    print("[DATABASE] Estrutura de Bioperícia Facial inicializada com sucesso.")

def salvar_pericia(caminho_banco, ramo_direito, ramo_esquerdo, indice_simetria):
    """
    Insere os dados métricos reais do laudo diretamente no banco de dados.
    """
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()
    
    timestamp_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    sql = """
    INSERT INTO pericias_mandibulares (timestamp, ramo_direito, ramo_esquerdo, indice_simetria)
    VALUES (?, ?, ?, ?)
    """
    
    dados = (timestamp_atual, ramo_direito, ramo_esquerdo, indice_simetria)
    
    try:
        cursor.execute(sql, dados)
        conn.commit()
        print("[DATABASE] Métricas de simetria salvas com sucesso no banco global!")
    except sqlite3.Error as e:
        print(f"[ERRO] Falha ao salvar no banco: {e}")
    finally:
        conn.close()

# TESTE AUTOMÁTICO SEGURO (Descobre a pasta atual sozinho)
if __name__ == "__main__":
    # Pega a pasta onde este arquivo database.py está guardado
    PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
    BANCO_TESTE = os.path.join(PASTA_ATUAL, "TCC_global_forense.db")
    
    criar_estrutura_forense(BANCO_TESTE)