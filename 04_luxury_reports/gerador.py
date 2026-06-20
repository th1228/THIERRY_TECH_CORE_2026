import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def gerar_primeira_pagina_pdf(caminho_imagem, caminho_saida="relatorio_luxo.pdf"):
    """
    Gera um relatório PDF de alto padrão corrigindo o erro de caminhos locais.
    """
    # 1. Tratamento Inteligente e Seguro do Caminho da Imagem
    caminho_foto = os.path.abspath(caminho_imagem)
    
    # Se não encontrar no caminho direto, busca em relação ao diretório do script
    if not os.path.exists(caminho_foto):
        diretorio_script = os.path.dirname(os.path.abspath(__file__))
        caminho_alternativo = os.path.join(diretorio_script, caminho_imagem)
        if os.path.exists(caminho_alternativo):
            caminho_foto = caminho_alternativo
        else:
            # Tenta buscar subindo um nível (caso imagens esteja na raiz do projeto)
            caminho_raiz_projeto = os.path.dirname(diretorio_script)
            caminho_raiz_imagens = os.path.join(caminho_raiz_projeto, caminho_imagem)
            if os.path.exists(caminho_raiz_imagens):
                caminho_foto = caminho_raiz_imagens

    print(f"[DEBUG] Tentando carregar imagem de: {caminho_foto}")

    # Validação defensiva para evitar o travamento do ReportLab
    if not os.path.exists(caminho_foto):
        print(f"⚠️ AVISO: Imagem não encontrada em '{caminho_foto}'. Gerando PDF com marcador de posição.")
        tem_imagem = False
    else:
        tem_imagem = True

    # 2. Configuração do Documento PDF (Padrão de Alto Luxo)
    doc = SimpleDocTemplate(
        caminho_saida,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos Personalizados - Paleta Minimalista e Sofisticada
    style_title = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1A1A1A"),
        alignment=1, # Centralizado
        spaceAfter=20
    )
    
    style_subtitle = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#555555"),
        alignment=1,
        spaceAfter=30
    )
    
    # Elementos do cabeçalho
    story.append(Paragraph("THIERRY TECHNOLOGY CONCEPT GLOBAL", style_title))
    story.append(Paragraph("BIOMETRIC PLATFORM & LUXURY ANALYSIS REPORT", style_subtitle))
    story.append(Spacer(1, 15))
    
    # 3. Inserção Segura da Imagem Corrigida
    if tem_imagem:
        try:
            # Renderiza a imagem com dimensões proporcionais e seguras
            img = Image(caminho_foto, width=280, height=280)
            img.hAlign = 'CENTER'
            story.append(img)
            story.append(Spacer(1, 20))
        except Exception as e:
            story.append(Paragraph(f"<i>[Erro ao renderizar imagem: {str(e)}]</i>", styles['Normal']))
    else:
        # Caixa cinza elegante de placeholder caso a imagem mude de lugar, impedindo o erro fatal
        dados_placeholder = [["IMAGEM NÃO LOCALIZADA", ""], [f"Verifique se o arquivo existe em:\n{caminho_imagem}", ""]]
        t_placeholder = Table(dados_placeholder, colWidths=[350, 5], rowHeights=[40, 60])
        t_placeholder.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F9F9F9")),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#777777")),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (0,0), 11),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EAEAEA")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#DDDDDD")),
        ]))
        t_placeholder.hAlign = 'CENTER'
        story.append(t_placeholder)
        story.append(Spacer(1, 20))

    # Conteúdo Adicional do Relatório
    style_body = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#333333")
    )
    story.append(Paragraph("<b>Análise Biométrica Executada:</b> Mapeamento de malha facial e persistência estrutural de visagismo avançado concluída com sucesso.", style_body))
    
    # Construção final do arquivo
    doc.build(story)
    print(f"✅ PDF gerado com sucesso em: {caminho_saida}")

if __name__ == "__main__":
    # Caminho exato que estava gerando o erro no seu sistema
    caminho_imagem_erro = "imagens/WhatsApp Image 2026-05-19 at 10.10.42.jpeg"
    gerar_primeira_pagina_pdf(caminho_imagem_erro, "Relatorio_TTC_Global.pdf")