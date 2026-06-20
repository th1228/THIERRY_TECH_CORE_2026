import sys
import os
from fpdf import FPDF

# --- CORREÇÃO DE IMPORTAÇÃO (Garante que o Python ache seus arquivos) ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from biometria import ThierryLuxuryCore
from sentinela import SentinelaFisio

def gerar_diagnostico_final():
    # 1. Inicializa os módulos
    sentinela = SentinelaFisio()
    engine = ThierryLuxuryCore()

    # 2. Executa a captura (Aguardando interação do usuário)
    print("--- INICIANDO CAPTURA FISIOGNÔMICA TTC GLOBAL ---")
    engine.rodar_biometria_premium(sentinela)
    
    # 3. Extrai o diagnóstico processado pelo Sentinela
    # O sentinela já calculou o estado dentro da rodar_biometria_premium
    estado_neuro = sentinela.estado_atual
    
    # 4. Início da Geração do PDF
    pdf = FPDF()
    pdf.set_margins(10, 10, 10)
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "BESPOKE VISUAL DIAGNOSIS: TTC GLOBAL", ln=True, align='C')
    pdf.ln(10)
    
    # Resultados Fisiognômicos
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, "ANALISE NEURO-FISIOGNOMICA:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(190, 10, f"ESTADO DETECTADO: {estado_neuro}", align='L')
    pdf.ln(5)

    # 5. Integração com o Laudo da Mão (Biogene)
    if os.path.exists("ultimo_laudo.txt"):
        try:
            with open("ultimo_laudo.txt", "r") as f:
                nome_foto = f.read().strip()
            
            if os.path.exists(nome_foto):
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(190, 10, "REGISTRO DE DENSIDADE (BIOGENE):", ln=True)
                pdf.image(nome_foto, x=10, w=80)
                pdf.ln(85)
        except Exception as e:
            print(f"Erro ao integrar imagem da mão: {e}")

    # 6. Salvamento do Relatório Definitivo
    pasta_destino = r"c:\projetos python\THIERRY_TECHNOLOGY_CORE"
    os.makedirs(pasta_destino, exist_ok=True)
    caminho_final = os.path.join(pasta_destino, "Relatorio_Definitivo_TTC.pdf")
    
    pdf.output(caminho_final)
    
    print("-" * 60)
    print(f"SUCESSO! RELATÓRIO GERADO EM:")
    print(f"-> {caminho_final}")
    print("-" * 60)

if __name__ == "__main__":
    gerar_diagnostico_final()