import sqlite3
import os

# --- MÓDULO DE TESTE E VALIDAÇÃO BIOGÊNIO ---
def verificar_ambiente():
    print(f"\n--- PASTA ATUAL: {os.getcwd()} ---")
    
    # Lista arquivos para você ver o que tem na pasta
    arquivos = os.listdir('.')
    print("Arquivos encontrados na pasta:")
    for arq in arquivos:
        print(f"-> {arq}")

    db_path = 'thierry_tech_biogenio.db'
    if os.path.exists(db_path):
        print(f"\n[OK] Banco de dados '{db_path}' detectado.")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Conta registros
        cursor.execute("SELECT COUNT(*) FROM analises")
        total = cursor.fetchone()[0]
        print(f"[STATUS] Total de registros: {total}")
        conn.close()
    else:
        print(f"\n[ERRO] O arquivo '{db_path}' não está nesta pasta!")

if __name__ == "__main__":
    verificar_ambiente()