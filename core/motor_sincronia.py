# -*- coding: utf-8 -*-
import sys
import os

# --- BLOCO DE CONEXÃO ESTRUTURAL (NÃO MEXER) ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from memoria_comum import instancia_memoria
except ImportError:
    # Fallback caso rode isolado sem a raiz configurada
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    instancia_memoria = MemoriaMock()
# -----------------------------------------------

"""
MOTOR SINCRONIA
Responsável pela harmonização dos dados entre os sensores e a malha central.
"""

def executar_coleta_inicial():
    """
    Função principal de sincronização. 
    Esta é a função que o seu main.py espera encontrar.
    """
    print("[MOTOR SINCRONIA] Iniciando fase de sincronização...")
    
    try:
        # Lógica de coleta
        dados = coleta_dados_sensores()
        verificar_integridade_malha()
        
        # AQUI A CONEXÃO: Salva o status na Memória Comum
        instancia_memoria.salvar_dados("STATUS_SINCRONIA", "CONCLUIDO")
        instancia_memoria.salvar_dados("DADOS_SINCRONIZADOS", dados)
        
        print("[MOTOR SINCRONIA] Sincronia concluída com sucesso.")
        return True
        
    except Exception as e:
        instancia_memoria.salvar_dados("STATUS_SINCRONIA", f"ERRO: {e}")
        print(f"[ERRO NO MOTOR SINCRONIA] Falha durante a sincronia: {e}")
        return False

def coleta_dados_sensores():
    """Simula a coleta de dados da rede de sensores."""
    return {"sensores": "ativos", "latencia": "baixa", "integridade": 100}

def verificar_integridade_malha():
    """Simula a verificação da integridade da malha de dados."""
    pass

def processar(frame=None):
    """
    Função de compatibilidade direta com o orquestrador (main.py).
    Executa a coleta e adiciona HUD visual opcional se houver frame.
    """
    sucesso = executar_coleta_inicial()
    
    if frame is not None:
        import cv2
        status_txt = "SUCESSO" if sucesso else "FALHA"
        cv2.putText(frame, "TTC GLOBAL // MOTOR SINCRONIA [ACTIVE]", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 102), 2, cv2.LINE_AA)
        cv2.putText(frame, f"STATUS SINCRONIA: {status_txt}", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (212, 175, 55), 1, cv2.LINE_AA)
        return frame
        
    return sucesso

# Permite rodar direto no terminal: python core/motor_sincronia.py
if __name__ == "__main__":
    executar_coleta_inicial()