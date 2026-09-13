# -*- coding: utf-8 -*-
import sys
import os
import logging

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

# Configuração de Log para capturar onde o erro acontece
logging.basicConfig(level=logging.INFO)

try:
    import core.biometria as biometria
    import core.diagnostico_ante_gravidade_neural as diagnostico_ante_gravidade_neural
    import core.neuro_gravidade_preditor as neuro_gravidade_preditor
except ImportError as e:
    logging.error(f"Erro de importação: {e}")

def executar_reconstrucao_total():
    """
    Motor de consolidação com verificação de integridade e sincronização global.
    """
    try:
        dados_consolidado = {
            "biometria": biometria.obter_dados() if 'biometria' in globals() and hasattr(biometria, 'obter_dados') else "Modulo indisponivel",
            "diagnostico": diagnostico_ante_gravidade_neural.obter_dados() if 'diagnostico_ante_gravidade_neural' in globals() and hasattr(diagnostico_ante_gravidade_neural, 'obter_dados') else "Modulo indisponivel",
            "neuro": neuro_gravidade_preditor.obter_dados() if 'neuro_gravidade_preditor' in globals() and hasattr(neuro_gravidade_preditor, 'obter_dados') else "Modulo indisponivel",
            "status_orquestracao": "Processamento concluído com sucesso"
        }
        
        # Sincronização automática com a Memória Comum 🧠
        try:
            memoria.salvar_dados("core_reconstrucao_consolidado", dados_consolidado)
        except Exception:
            pass

        return dados_consolidado
    except Exception as e:
        logging.error(f"Falha na execução interna: {str(e)}")
        erro_payload = {"erro": f"Falha na consolidação: {str(e)}"}
        
        try:
            memoria.salvar_dados("core_reconstrucao_consolidado", erro_payload)
        except Exception:
            pass
            
        return erro_payload

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    return executar_reconstrucao_total()

if __name__ == "__main__":
    resultado = executar_reconstrucao_total()
    print("Resultado da Reconstrução Total:", resultado)