import sqlite3

# Conecta no mesmo arquivo
conn = sqlite3.connect('thierry_tech_biogenio.db')
cursor = conn.cursor()

# Busca tudo o que foi gravado
cursor.execute("SELECT * FROM analises")
registros = cursor.fetchall()

print("--- REGISTROS DO BIOGÊNIO ---")
for reg in registros:
    print(f"ID: {reg[0]} | Data: {reg[1]} | Score: {reg[2]:.2f}")

conn.close()