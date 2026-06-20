import os
import sqlite3

# Definição correta do caminho para o banco de dados (sem o 03_)
DB_NAME = "database_sql/TCC_GLOBAL_forense.db"

def iniciar_banco_dados():
    """Garante a criação do cofre digital e das tabelas forenses."""
    # Garante que a pasta database_sql exista no computador
    pasta = os.path.dirname(DB_NAME)
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta)
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Criação da tabela com rigor científico e métricas exatas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pericias_mandibulares (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        largura_zigomatica REAL NOT NULL,
        altura_maxilar REAL NOT NULL,
        angulo_goniaco REAL NOT NULL,
        profundidade_mento REAL NOT NULL,
        indice_simetria REAL NOT NULL,
        operador TEXT DEFAULT 'Thierry Rodrigues'
    )
    """)
    
    conn.commit()
    conn.close()
    print("[DATABASE] Estrutura forense inicializada com sucesso.")

def salvar_registro_forense(dados):
    """Insere os dados calculados em tempo real diretamente no cofre .db"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO pericias_mandibulares 
        (timestamp, largura_zigomatica, altura_maxilar, angulo_goniaco, profundidade_mento, indice_simetria, operador)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, dados)
        
        conn.commit()
        conn.close()
        print("[DATABASE] Registro forense VIP salvo com sucesso.")
    except Exception as e:
        print(f"[ERRO] Falha ao salvar no banco de dados: {e}")

# Executa a inicialização do banco ao rodar o arquivo
if __name__ == "__main__":
    iniciar_banco_dados()
    import sqlite3
from datetime import datetime

def salvar_pericia(caminho_banco, largura_zigomatico, largura_goniaco, altura_mento, angulo_goniaco):
    """
    Insere os dados métricos da perícia mandibular no banco de dados.
    """
    # 1. Conecta ao banco de dados
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()
    
    # 2. Captura o timestamp atual da análise
    timestamp_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 3. Comando SQL para inserção (omitindo o ID pois ele é AUTOINCREMENT)
    sql = """
    INSERT INTO pericias_mandibulares (timestamp, largura_zigomatico, largura_goniaco, altura_mento, angulo_goniaco)
    VALUES (?, ?, ?, ?, ?)
    """
    
    # 4. Dados que preencherão as interrogações (?) acima
    dados = (timestamp_atual, largura_zigomatico, largura_goniaco, altura_mento, angulo_goniaco)
    
    try:
        # 5. Executa e salva as alterações
        cursor.execute(sql, dados)
        conn.commit()
        print("[DATABASE] Métricas forenses salvas com sucesso no banco!")
    except sqlite3.Error as e:
        print(f"[ERRO] Falha ao salvar no banco: {e}")
    finally:
        # 6. Fecha a conexão para não travar o arquivo .db
        conn.close()