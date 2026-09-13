# -*- coding: utf-8 -*-
import sys
import os
import json
from datetime import datetime
from fpdf import FPDF

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

def enviar_laudo(relatorio_dados=None, nome_arquivo_foto=None):
    try:
        # Se os dados não forem passados, busca automaticamente na Memória Comum 🧠
        if relatorio_dados is None:
            relatorio_dados = memoria.ler_dados("visagism_metrics") or {"status": "Dados não encontrados na memória"}

        agora = datetime.now()
        timestamp_str = agora.strftime("%Y-%m-%d %H:%M:%S")
        nome_arquivo_base = agora.strftime("Laudo_%Y%m%d_%H%M%S")
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="TTC GLOBAL - RELATORIO DE ANALISE FORENSE", ln=True, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Data e Hora: {timestamp_str}", ln=True)
        pdf.ln(5)
        
        pdf.set_font("Arial", size=10)
        texto_dados = json.dumps(relatorio_dados, indent=4)
        pdf.multi_cell(0, 10, txt=texto_dados)
        
        pdf_final = f"{nome_arquivo_base}.pdf"
        pdf.output(pdf_final)
        
        # Sincroniza o status do laudo gerado de volta na Memória Comum 🧠
        memoria.salvar_dados("status_laudo", {"arquivo": pdf_final, "timestamp": timestamp_str})

        print("--- TTC GLOBAL: INTEGRACAO EM EXECUCAO ---")
        print(f"Laudo gerado e salvo como: {pdf_final}")
        
        return True

    except Exception as e:
        print(f"Erro no modulo de integracao: {str(e)}")
        return False

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    return enviar_laudo()

if __name__ == "__main__":
    enviar_laudo()