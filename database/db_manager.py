import sqlite3
import os

class DBManager:
    # Aponta para o arquivo que criamos no passo anterior
    DB_PATH = os.path.join('database', 'sistema_seguro.db')

    @staticmethod
    def verificar_permissao(id_scanner):
        """Consulta segura ao banco de dados usando consulta parametrizada."""
        try:
            conn = sqlite3.connect(DBManager.DB_PATH)
            cursor = conn.cursor()
            
            # Consulta protegida contra SQL Injection
            query = "SELECT liberado FROM permissao_scanner WHERE id_scanner = ?"
            cursor.execute(query, (id_scanner,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            # Se encontrar o scanner e ele estiver marcado como '1' (liberado)
            return resultado is not None and resultado[0] == 1
        except Exception as e:
            print(f"[DB] Erro ao consultar permissões: {e}")
            return False