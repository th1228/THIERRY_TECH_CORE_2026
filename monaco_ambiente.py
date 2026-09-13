# -*- coding: utf-8 -*-
import sys
import os

# --- CORREÇÃO DE PATH PARA AUDITORIA PROFUNDA ---
# Adiciona a raiz do projeto ao path para garantir que 'core' seja encontrado
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Agora que o path está correto, os imports funcionam sem conflito
from core.memoria_comum import instancia_memoria as memoria
from core.script_clima import obter_dados 

def rodar():
    """
    Módulo Oficial: Mônaco Ambiente
    Responsável pela leitura e formatação dos dados climáticos e vinculação à Memória.
    """
    try:
        dados = obter_dados()
        
        if dados.get("status") == "sucesso":
            # Extração dos dados
            info_ambiente = {
                "regiao": dados.get("regiao", "Desconhecido"),
                "clima": dados.get("clima_agora", "Indisponível"),
                "data": dados.get("data_processamento", "---"),
                "hora": dados.get("hora_processamento", "---")
            }
            
            # --- INTEGRAÇÃO COM MEMÓRIA COMUM ---
            # Salva no hub central para o Mônaco Plan ler depois
            memoria.salvar_dados("ambiente", info_ambiente)
            
            # Feedback no terminal
            print(f"\n--- [MÔNACO AMBIENTE ATIVO] ---")
            for k, v in info_ambiente.items():
                print(f"{k.capitalize()}: {v}")
            print(f"Status: Dados registrados na Memória Comum.")
            print(f"----------------------------")
            
            return f"Condição: {info_ambiente['clima']}"
        else:
            return f"[MÔNACO AMBIENTE] Alerta: {dados.get('mensagem', 'Erro no sensor')}"
            
    except Exception as e:
        return f"[MÔNACO AMBIENTE] Erro crítico no motor: {str(e)}"

def iniciar():
    """Ponte de comando para a Central."""
    return rodar()

if __name__ == "__main__":
    print(rodar())