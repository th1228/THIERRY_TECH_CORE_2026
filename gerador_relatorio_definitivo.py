import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def construir_pdf():
    # 1. Configuração do Nome do Arquivo e Destino
    nome_pdf = "Relatorio_TTC_Global.pdf"
    doc = SimpleDocTemplate(
        nome_pdf,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    story = []
    
    # 2. Resolução Dinâmica do Caminho da Imagem
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Nome exato do arquivo conforme visto na imagem do seu VS Code
    nome_imagem = "WhatsApp Image 2026-05-19 at 10.10.42 .jpeg"
    
    # Tenta procurar primeiro na pasta 'imagens' e depois na raiz do projeto
    caminho_imagens_pasta = os.path.join(diretorio_atual, "imagens", nome_imagem)
    caminho_raiz = os.path.join(diretorio_atual, nome_imagem)
    
    if os.path.exists(caminho_imagens_pasta):
        caminho_final_imagem = caminho_imagens_pasta
    elif os.path.exists(caminho_raiz):
        caminho_final_imagem = caminho_raiz
    else:
        caminho_final_imagem = None
        print(f"⚠️ AVISO: A imagem não foi encontrada em nenhuma das seguintes localizações:\n - {caminho_imagens_pasta}\n - {caminho_raiz}\nGerando PDF com marcador de posição.")

    # 3. Estilos de Texto (Customizados para uma identidade visual de luxo)
    styles = getSampleStyleSheet()
    
    estilo_titulo = ParagraphStyle(
        'TituloLuxo',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1A1A1A"),
        spaceAfter=6
    )
    
    estilo_subtitulo = ParagraphStyle(
        'SubtituloLuxo',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#555555"),
        spaceAfter=15
    )
    
    estilo_corpo = ParagraphStyle(
        'CorpoLuxo',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#333333")
    )

    # 4. # ----- HEADER DE LUXO (BANNER SUPERIOR) -----
    if caminho_final_imagem:
        try:
            # Mantém a proporção elegante para um banner de cabeçalho
            # Largura disponível no A4 com margens de 40 é aproximadamente 515 pontos
            banner = Image(caminho_final_imagem, width=515, height=140)
            story.append(banner)
            story.append(Spacer(1, 15))
        except Exception as e:
            print(f"Erro ao carregar a imagem com o ReportLab: {e}")
            # Marcador de posição caso o arquivo esteja corrompido
            story.append(Paragraph("<b>[ Espaço do Banner TTC Global ]</b>", estilo_titulo))
            story.append(Spacer(1, 20))
    else:
        # Se a imagem realmente não existir, desenha uma estrutura elegante em tabela para substituição
        dados_placeholder = [[Paragraph("<b>THIERRY TECHNOLOGY CONCEPT GLOBAL</b>", estilo_titulo)]]
        tabela_placeholder = Table(dados_placeholder, colWidths=[515], rowHeights=[100])
        tabela_placeholder.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F5F5F7")),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 20),
        ]))
        story.append(tabela_placeholder)
        story.append(Spacer(1, 15))

    # 5. Conteúdo do Relatório
    story.append(Paragraph("Relatório Técnico de Visagismo & Biometria", estilo_titulo))
    story.append(Paragraph("Módulo: BIOGEMIO_DIGITAL_2026 — Análise de Linhas e Proporções Forenses", estilo_subtitulo))
    
    # Linha divisória fina decorativa
    linha_decorativa = Table([[""]], colWidths=[515], rowHeights=[2])
    linha_decorativa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#D1D1D6")),
        ('TOPMARGIN', (0,0), (-1,-1), 0),
        ('BOTTOMMARGIN', (0,0), (-1,-1), 10),
    ]))
    story.append(linha_decorativa)
    story.append(Spacer(1, 10))
    
    texto_exemplo = (
        "Este documento contém a análise biométrica e estrutural baseada no mapeamento "
        "de malha facial (Facial Mesh) obtido através do ecossistema Thierry Technology. "
        "Os dados gerados destinam-se à aplicação prática dos conceitos de visagismo "
        "personalizado e análise de posicionamento de mercado de alto padrão."
    )
    story.append(Paragraph(texto_exemplo, estilo_corpo))
    
    # 6. Geração Final do Arquivo
    try:
        doc.build(story)
        print(f"✅ PDF gerado com sucesso em: {os.path.abspath(nome_pdf)}")
    except Exception as e:
        print(f"❌ Erro ao construir o PDF: {e}")

if __name__ == "__main__":
    construir_pdf()