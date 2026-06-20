import sqlite3

# Define o nome do arquivo do banco de dados (ficará na mesma pasta)
DB_NAME = "thierry_tech_global.db"

def inicializar_banco():
    """Cria a tabela de clientes se ela ainda não existir."""
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    
    # Criando a estrutura da tabela
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            bio_age REAL,
            osteometria TEXT,
            data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conexao.commit()
    conexao.close()
    print("Banco de dados Thierry Technology Concept Global inicializado com sucesso.")

# Ao rodar este script, ele já cria o banco
if __name__ == "__main__":
    inicializar_banco()