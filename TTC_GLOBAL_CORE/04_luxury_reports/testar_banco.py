import sqlite3
import json

# 1. Conexão com o Banco
def conectar_banco():
    nome_banco = 'TCC_global_forense.db'
    try:
        conn = sqlite3.connect(nome_banco)
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None

# 2. Criação Automática da Tabela de Visagismo/Biometria
def inicializar_estrutura_banco(conexao):
    cursor = conexao.cursor()
    
    # Criando a tabela com campos robustos para os relatórios e mesh facial
    query_tabela = """
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        alias TEXT,
        data_nascimento TEXT,
        analise_facial TEXT,  -- Aqui vai o JSON do MediaPipe/OpenCV
        status_plano TEXT
    );
    """
    try:
        cursor.execute(query_tabela)
        conexao.commit()
        print("🏛️ Estrutura do banco validada/criada com sucesso (Tabela 'clientes' pronta)!")
    except Exception as e:
        print(f"❌ Erro ao criar a estrutura da tabela: {e}")

# 3. Dados fictícios da análise
dados_faciais_ficticios = {
    "proporcao_aurea": 1.618,
    "formato_rosto": "Oval",
    "analise_luxo_status": "Premium",
    "landmarks_principais": [
        {"id": 1, "x": 0.52, "y": 0.61},
        {"id": 33, "x": 0.45, "y": 0.55}
    ]
}
facial_json = json.dumps(dados_faciais_ficticios)

# 4. Inserção do Teste
def inserir_cliente_teste(conexao):
    cursor = conexao.cursor()
    query_insert = """
    INSERT INTO clientes (nome, alias, data_nascimento, analise_facial, status_plano)
    VALUES (?, ?, ?, ?, ?)
    """
    valores = ("Elena Rostova", "Elena Luxo", "1995-04-12", facial_json, "Mônaco VIP")
    
    try:
        cursor.execute(query_insert, valores)
        conexao.commit()
        print("🎉 Sucesso: Dados fictícios salvos no banco!")
        return cursor.lastrowid
    except Exception as e:
        conexao.rollback()
        print(f"❌ Erro ao salvar dados: {e}")
        return None

# 5. Validação da Leitura
def verificar_dados_salvos(conexao, cliente_id):
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
        resultado = cursor.fetchone()
        
        if resultado:
            print("\n--- Verificação de Persistência no Banco ---")
            print(f"📌 ID do Registro: {resultado[0]}")
            print(f"👤 Nome Cadastrado: {resultado[1]}")
            print(f"💎 Plano Atribuído: {resultado[5]}")
            print("✨ Leitura e escrita funcionando 100%!")
        else:
            print("⚠️ Erro: Registro não localizado após inserção.")
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")

if __name__ == "__main__":
    print("Iniciando teste completo de persistência...")
    conexao = conectar_banco()
    
    if conexao:
        # Primeiro cria a tabela se não houver
        inicializar_estrutura_banco(conexao)
        
        # Depois insere os dados
        id_gerado = inserir_cliente_teste(conexao)
        
        # Por fim, valida a leitura
        if id_gerado:
            verificar_dados_salvos(conexao, id_gerado)
            
        conexao.close()