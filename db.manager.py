import sqlite3

# Caminho para o seu banco de dados
DB_PATH = r"C:\projetos python\THIERRY_T.db" # Ajuste se o caminho for outro

def salvar_analise(id_cliente, metrics):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = """
    INSERT INTO analises_visagismo 
    (id_cliente, proporcao_facial, indice_interpupilar, forca_mandibula, codigo_vetor_corte)
    VALUES (?, ?, ?, ?, ?)
    """
    
    try:
        cursor.execute(query, (
            id_cliente, 
            metrics['proporcao'], 
            metrics['dip'], 
            metrics['mandibula'], 
            metrics['vetor_corte']
        ))
        conn.commit()
        print("Dados inseridos com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar: {e}")
    finally:
        conn.close()