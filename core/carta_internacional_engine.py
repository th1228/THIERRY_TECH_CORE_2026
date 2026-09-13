# -*- coding: utf-8 -*-
import sys
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

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

def gerar_carta_apresentacao():
    dir_destino = os.path.join(ROOT_DIR, "core", "pdfs_finais")
    os.makedirs(dir_destino, exist_ok=True)
    
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamp_legivel = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Paleta de Cores de Luxo (Preto Onix, Dourado Nobre e Cinza Executivo)
    COR_PRETO = colors.HexColor("#0B0B0B")
    COR_DOURADO = colors.HexColor("#C5A059")
    COR_CINZA = colors.HexColor("#333333")

    path_pdf = os.path.join(dir_destino, f"CARTA_APRESENTACAO_EXECUTIVA_{timestamp_str}.pdf")
    
    doc = SimpleDocTemplate(
        path_pdf,
        pagesize=letter,
        rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    style_titulo = ParagraphStyle(
        'TituloCarta', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=11, leading=14,
        textColor=COR_PRETO, alignment=1, spaceAfter=2
    )
    style_sub = ParagraphStyle(
        'SubCarta', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=7, leading=9,
        textColor=COR_DOURADO, alignment=1, spaceAfter=10
    )
    style_corpo = ParagraphStyle(
        'CorpoCarta', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=11,
        textColor=COR_CINZA, spaceAfter=6, alignment=4 # Justificado
    )
    style_assinatura = ParagraphStyle(
        'AssinaturaCarta', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=10.5,
        textColor=COR_PRETO, spaceBefore=6
    )

    story = [
        Paragraph("CARTA DE APRESENTAÇÃO EXECUTIVA (CONFIDENCIAL)", style_titulo),
        Paragraph(f"TTC Global — Enterprise Division | Emitido em: {timestamp_legivel}", style_sub),
        HRFlowable(width="100%", thickness=1, color=COR_DOURADO, spaceAfter=8),

        Paragraph("Prezado(a) [Nome do Diretor, Investidor ou Nome da Clínica AAA],", style_corpo),
        
        Paragraph("É com grande satisfação que apresentamos uma oportunidade exclusiva de licenciamento tecnológico voltada ao mercado de altíssimo padrão: o <b>Ecossistema TTC Global — Enterprise Division</b>.", style_corpo),

        Paragraph("O mercado global de estética médica regenerativa e consultoria de imagem movimentou bilhões no último ano. Contudo, o grande gargalo das operações de luxo continua sendo a subjetividade no diagnóstico inicial. Erros de percepção humana afastam clientes exigentes e limitam o potencial de faturamento de tratamentos de alto ticket.", style_corpo),

        Paragraph("Nossa tecnologia elimina essa barreira ao converter o visagismo tradicional e a análise de subtom cutâneo em ciência exata. Através de inteligência artificial e visão computacional avançada, o TTC Global Core Engine mapeia a volumetria facial e calibra a leitura cromática da epiderme em tempo real, gerando um diagnóstico irrefutável que eleva drasticamente a confiança do paciente e a conversão de procedimentos na clínica.", style_corpo),

        Paragraph("Por se tratar de um ativo de alta exclusividade, operamos sob um modelo rígido de escassez de mercado, garantindo cláusula de exclusividade geográfica para um número estritamente limitado de parceiros em polos econômicos estratégicos.", style_corpo),

        Paragraph("O documento anexo detalha a arquitetura técnica, as garantias de segurança cibernética e o estudo de viabilidade financeira que sustenta o valuation desta tecnologia. Estamos à disposição para agendar uma demonstração técnica restrita e discutir os termos de reserva de território para a sua região.", style_corpo),

        Paragraph("Cordialmente,<br/><br/><b>Thierry</b><br/>Diretor de Desenvolvimento de Negócios<br/>TTC Global — Enterprise Division<br/>contato@ttcglobal.tech | +55 (98) 99999-9999", style_assinatura)
    ]

    doc.build(story)
    caminho_absoluto = os.path.abspath(path_pdf)
    
    # Sincronização automática com a Memória Comum 🧠
    try:
        memoria.salvar_dados("carta_apresentacao_pdf", {
            "caminho": caminho_absoluto,
            "status": "GERADO_COM_SUCESSO",
            "timestamp": timestamp_legivel
        })
    except Exception:
        pass

    print(f"[ENGINE] Carta de Apresentação Executiva gerada com sucesso em: {caminho_absoluto}")
    return caminho_absoluto

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    return gerar_carta_apresentacao()

if __name__ == "__main__":
    gerar_carta_apresentacao()