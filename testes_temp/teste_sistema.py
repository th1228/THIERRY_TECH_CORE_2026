import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import webbrowser
from datetime import datetime, timedelta
from fpdf import FPDF

# --- MOTOR DE PROGNÓSTICO (ESTÁ TUDO AQUI DENTRO) ---
class MotorPrognostico:
    def __init__(self, cliente_nome):
        self.cliente = cliente_nome
        self.tratamentos = ["ABS. MOLECULAR", "NUTRIÇÃO WELLA", "ACIDIFICAÇÃO", "HIDRAT. INTENSIVA", "SELAGEM KERASTASE"]
        self.marcas = ["L'OREAL", "WELLA", "DAVINES", "KERASTASE", "DAVINES"]
        self.terapias = ["OZONIOTERAPIA", "AQUATERAPIA", "LUMINOTERAPIA", "ARGILOTERAPIA"]

    # Esta função garante que, mesmo sem sensores, o motor rode
    def processar(self, paciente, sensores=None):
        return "OK"

    def calcular_cronograma_detalhado(self, cor_identidade, sensores=None):
        matriz = []
        data_inicio = datetime.now()
        for i in range(16):
            data_atual = data_inicio + timedelta(days=i)
            matriz.append({
                "DATA": data_atual.strftime("%d/%m"),
                "CLIMA": "SECO" if i % 2 == 0 else "ÚMIDO",
                "TRATAM": self.tratamentos[i % len(self.tratamentos)],
                "MARCA": self.marcas[i % len(self.marcas)],
                "TERAPIA": self.terapias[i % len(self.terapias)],
                "DECISÃO": ["TÁTICA", "ASSERTIVA", "METÓDICA", "CAUTELOSA"][i % 4],
                "COR": cor_identidade,
                "ÓLEO": ["GERÂNIO", "OLÍBANO", "LAVANDA"][i % 3],
                "ÁPICE": "ÁPICE" if i == 15 else "-"
            })
        return matriz

# --- GERADOR DE RELATÓRIO (NÃO PRECISA DE MAIS NADA) ---
def gerar_relatorio():
    motor = MotorPrognostico("THIERRY")
    dados = motor.calcular_cronograma_detalhado("DOURADO")
    
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "ENGENHARIA DA ALMA | MATRIZ DE SINCRONIA", ln=True, align='C')
    
    # Tabela
    headers = ["DATA", "CLIMA", "TRATAM", "MARCA", "TERAPIA", "DECISÃO", "COR", "ÓLEO", "ÁPICE"]
    pdf.set_font("Arial", 'B', 7)
    for h in headers: pdf.cell(30, 6, h, border=1)
    pdf.ln()
    
    # Dados
    pdf.set_font("Arial", '', 7)
    for row in dados:
        for h in headers:
            pdf.cell(30, 6, str(row.get(h, "-")), border=1)
        pdf.ln()
        
    arquivo = "RELATORIO_FINAL.pdf"
    pdf.output(arquivo, 'F')
    
    caminho = os.path.abspath(arquivo)
    print(f"Sucesso! PDF gerado em: {caminho}")
    webbrowser.open('file://' + caminho)

if __name__ == "__main__":
    gerar_relatorio()