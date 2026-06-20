import sqlite3
import datetime

def testar_conexao_biogenio():
    print("--- INICIANDO TESTE DO MÓDULO BIOGÊNIO ---")
    
    try:
        # Conecta ao seu banco principal
        conn = sqlite3.connect('thierry_tech_biogenio.db')
        cursor = conn.cursor()
        
        # 1. Verifica se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='analises'")
        tabela = cursor.fetchone()
        
        if tabela:
            print("Status: Conexão com a tabela 'analises' estabelecida com sucesso.")
            # 2. Testa uma leitura rápida
            cursor.execute("SELECT COUNT(*) FROM analises")
            contagem = cursor.fetchone()[0]
            print(f"Status: O banco contém {contagem} registros processados.")
        else:
            print("ERRO: A tabela 'analises' não foi encontrada. Verifique o schema do seu banco.")
            
        conn.close()
    except Exception as e:
        print(f"ERRO CRÍTICO NO TESTE: {e}")

if __name__ == "__main__":
    testar_conexao_biogenio()