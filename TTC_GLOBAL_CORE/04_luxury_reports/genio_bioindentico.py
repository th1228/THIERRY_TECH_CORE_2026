from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

class LuxuryReport(FPDF):
    def header(self):
        # Configuração do cabeçalho alinhada ao TTC Global
        self.set_font("Helvetica", "B", 12)
        # Substituição do ln=True por new_x e new_y para evitar o Warning
        self.cell(0, 5, "THIERRY TECHNOLOGY CONCEPT GLOBAL", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(10)

    def footer(self):
        # Rodapé posicionado a 1.5 cm do fim da página
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def gerar_laudo_genio():
    # Garante que a pasta de relatórios de luxo exista
    output_dir = "04__luxury_reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    pdf = LuxuryReport()
    pdf.add_page()
    
    # Corpo do documento
    pdf.set_font("Helvetica", "", 11)
    
    # Exemplo de bloco de texto estruturado para o laudo
    pdf.cell(0, 10, "LAUDO GÊNIO BIOIDÊNTICO", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
    pdf.ln(5)
    
    # Adicione aqui os dados dinâmicos ou resultados da bioperícia/análise
    pdf.multi_cell(0, 6, "Análise biométrica e facial avançada executada com sucesso. Os parâmetros estruturais e de visagismo tecnológico foram processados e armazenados conforme o padrão de excelência TTC.")

    # Caminho final do arquivo
    file_path = os.path.join(output_dir, "LAUDO_GENIO_BIOIDENTICO.pdf")
    pdf.output(file_path)
    
    # Mensagem de sucesso limpa no terminal
    print("💎 SUCESSO! PDF Gênio Bioidêntico gerado em:", file_path)

if __name__ == "__main__":
    gerar_laudo_genio()