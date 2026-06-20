import os
import json
from datetime import datetime
from fpdf import FPDF

def enviar_laudo(relatorio_dados, nome_arquivo_foto):
    try:
        # 1. Carimbo de data e hora para o nome do arquivo
        agora = datetime.now()
        timestamp_str = agora.strftime("%Y-%m-%d %H:%M:%S")
        nome_arquivo_base = agora.strftime("Laudo_%Y%m%d_%H%M%S")
        
        # 2. Geração do PDF Forense
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="TTC GLOBAL - RELATORIO DE ANALISE FORENSE", ln=True, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Data e Hora: {timestamp_str}", ln=True)
        pdf.ln(5)
        
        # Adiciona os dados do laudo no PDF
        pdf.set_font("Arial", size=10)
        texto_dados = json.dumps(relatorio_dados, indent=4)
        pdf.multi_cell(0, 10, txt=texto_dados)
        
        # Salva o PDF
        pdf_final = f"{nome_arquivo_base}.pdf"
        pdf.output(pdf_final)
        
        # 3. Log no terminal
        print("--- TTC GLOBAL: INTEGRACAO EM EXECUCAO ---")
        print(f"Laudo gerado e salvo como: {pdf_final}")
        print(f"Timestamp: {timestamp_str}")
        
        return True

    except Exception as e:
        print(f"Erro no modulo de integracao: {str(e)}")
        return False

if __name__ == "__main__":
    print("Modulo de integracao carregado corretamente no Core.")