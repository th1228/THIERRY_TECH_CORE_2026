# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the 
intellectual property of Thierry Technology Concept Global. Unauthorized 
distribution, reverse engineering, or usage without a signed NDA/License 
agreement is strictly prohibited under international copyright frameworks.
===========================================================================
"""

# -*- coding: utf-8 -*-
import sys
import os
import sqlite3

# --- BLOCO DE CONEXÃO ESTRUTURAL ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

DB_NAME = "thierry_tech_core.db"

def inicializar_banco():
    """Cria a tabela de clientes se ela não existir."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                umidade_pele REAL,
                protocolo TEXT,
                data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        memoria.salvar_dados("STATUS_BANCO", "INICIALIZADO")
    except Exception as e:
        print(f"[ERRO BANCO DE DADOS] Falha na inicialização: {e}")

def inserir_cliente(nome, umidade, protocolo):
    """Insere um novo registro de cliente no banco e atualiza a Memória Comum."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nome, umidade_pele, protocolo)
            VALUES (?, ?, ?)
        ''', (nome, umidade, protocolo))
        conn.commit()
        conn.close()
        
        # Sincronização com a Memória Comum 🧠
        dados_cliente = {"nome": nome, "umidade": umidade, "protocolo": protocolo}
        memoria.salvar_dados("ULTIMO_CLIENTE_REGISTRADO", dados_cliente)
        print(f"[BANCO] Cliente '{nome}' registrado com sucesso.")
    except Exception as e:
        print(f"[ERRO BANCO DE DADOS] Falha ao inserir cliente: {e}")

def processar(frame=None, nome="Paciente_Padrao", umidade=25.5, protocolo="PROTOCOLO_TTC"):
    """
    Função de compatibilidade direta com o orquestrador (main.py).
    """
    inicializar_banco()
    inserir_cliente(nome, umidade, protocolo)
    
    if frame is not None:
        import cv2
        cv2.putText(frame, "TTC GLOBAL // MOTOR DADOS [ACTIVE]", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 102), 2, cv2.LINE_AA)
        cv2.putText(frame, f"DB: CONECTADO | CLIENTE: {nome}", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (212, 175, 55), 1, cv2.LINE_AA)
        return frame
        
    return True

if __name__ == "__main__":
    print("[TESTE] Inicializando banco...")
    inicializar_banco()
    inserir_cliente("Teste_Integracao", 25.5, "PROTOCOLO_TESTE")
    print("[TESTE] Operação concluída.")