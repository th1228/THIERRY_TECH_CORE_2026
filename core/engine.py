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
import glob
import cv2
import logging
import metrics 

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

# --- DICIONÁRIO DE SUPORTE BILÍGUE AUTOMÁTICO (APEX GATE) ---
DICIONARIO_IDIOMAS = {
    "PT": {
        "FUNDAMENTACAO": "FUNDAMENTAÇÃO ESTRATÉGICA E ANÁLISE DE LIDERANÇA FACIAL",
        "CLÁUSULA": "CLÁUSULA PRIMEIRA: DA ESCASSEZ MUNDIAL DE 10 VAGAS",
        "DEPRECIAÇÃO": "ANÁLISE DE DEPRECIAÇÃO E VALUATION DO CAPITAL DE IMAGEM",
        "ENGENHARIA": "ENGENHARIA DE VALUATION E RETORNO DE BLINDAGEM ATIVA",
    },
    "EN": {
        "FUNDAMENTACAO": "STRATEGIC FOUNDATION AND FACIAL LEADERSHIP ANALYSIS",
        "CLÁUSULA": "FIRST CLAUSE: WORLDWIDE SCARCITY OF 10 EXCLUSIVE SLOTS",
        "DEPRECIAÇÃO": "DEPRECIATION ANALYSIS AND IMAGE CAPITAL VALUATION",
        "ENGENHARIA": "VALUATION ENGINEERING AND ACTIVE SHIELDING RETURN",
    }
}
# -----------------------------------------------

# Configuração de auditoria
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def processar_ultima_pericia():
    """
    Motor central (Engine) de processamento de perícia.
    Lê a última imagem capturada e executa a extração de métricas.
    """
    try:
        # 1. Localiza a última perícia
        lista_arquivos = glob.glob("pericia_*.png")
        if not lista_arquivos:
            logging.error("Nenhuma perícia encontrada para processamento.")
            return {"status": "erro", "mensagem": "Sistema Sincronizado"}

        ultimo_arquivo = max(lista_arquivos, key=os.path.getctime)
        logging.info(f"Engine iniciada. Processando: {ultimo_arquivo}")

        # 2. Carrega a imagem com verificação de integridade
        frame = cv2.imread(ultimo_arquivo)
        if frame is None:
            logging.error("Falha na leitura da imagem: arquivo corrompido.")
            return {"status": "erro", "mensagem": "Imagem corrompida"}

        # Log de status operacional
        altura, largura = frame.shape[:2]
        logging.info(f"Leitura bem-sucedida: {largura}x{altura}px.")

        # 3. Execução da análise de métricas
        if hasattr(metrics, 'calculate_visagism_metrics'):
            logging.info("Iniciando extração de métricas de alta precisão...")
            resultado = metrics.calculate_visagism_metrics(frame)
            
            resposta_final = {"status": "sucesso", "dados": resultado}
            
            # Sincronização automática com a Memória Comum 🧠
            try:
                memoria.salvar_dados("pericia_engine", resposta_final)
            except Exception:
                pass

            logging.info("Processamento concluído com sucesso.")
            return resposta_final
        
        else:
            logging.warning("Módulo de métricas não respondeu.")
            return {"status": "erro", "mensagem": "Módulo de métricas indisponível"}

    except Exception as e:
        logging.error(f"Falha crítica no Engine: {e}")
        return {"status": "falha_critica", "mensagem": str(e)}

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    return processar_ultima_pericia()

if __name__ == "__main__":
    resultado = processar_ultima_pericia()
    print(resultado)