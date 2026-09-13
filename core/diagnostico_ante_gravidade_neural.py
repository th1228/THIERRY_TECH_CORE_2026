# -*- coding: utf-8 -*-
import sys
import os
import subprocess

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

def executar_leitura_anti_gravidade():
    # 1. Integrar Dados Climáticos com CAMINHO ABSOLUTO
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_clima = os.path.join(diretorio_atual, "script_clima.py")
    
    try:
        if os.path.exists(caminho_clima):
            subprocess.run([sys.executable, caminho_clima], check=True)
        else:
            print(f"Aviso: Módulo de clima não encontrado em: {caminho_clima}")
    except Exception as e:
        print(f"Aviso: Erro ao executar módulo de clima: {e}")

    # 2. Estrutura de Dicionário Forense
    dados = {
        'simetria_mandibula': "Calculando...",
        'leitura_zigomatico': "Calculando...",
        'ancestralidade': "Misto-Forense",
        'quentura_pele': "Leitura via Termografia Infraroja",
        'densidade_mao': "Análise via Hand Landmark",
        'parecer': "Análise Anti-Gravidade em Processamento"
    }
    
    # Sincronização automática com a Memória Comum 🧠
    try:
        memoria.salvar_dados("leitura_anti_gravidade", dados)
    except Exception:
        pass

    return dados

def obter_dados():
    return executar_leitura_anti_gravidade()

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    return obter_dados()

if __name__ == "__main__":
    print(obter_dados())