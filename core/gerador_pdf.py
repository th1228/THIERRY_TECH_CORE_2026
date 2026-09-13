# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

class SovereignCanvas(canvas.Canvas):
    """
    Canvas customizado para desenhar o fundo escuro (Dark Mode Executivo),
    as molduras de segurança e o rodapé criptografado em todas as páginas.
    """
    def __init__(self, *args, **kwargs):
        super(SovereignCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super(SovereignCanvas, self).showPage()
        super(SovereignCanvas, self).save()

    def draw_page_elements(self, page_count):
        self.saveState()
        c_gold = colors.HexColor("#A38044")
        
        # Fundo totalmente escuro/carbono de alta fidelidade
        self.setFillColor(colors.HexColor("#08080C"))
        self.rect(0, 0, 612, 792, fill=1, stroke=0)
        
        # Molduras e linhas de segurança estilo papel-moeda internacional
        self.setStrokeColor(c_gold)
        self.setLineWidth(1.2)
        self.rect(18, 18, 576, 756)
        
        self.setStrokeColor(colors.HexColor("#1A1A24"))
        self.setLineWidth(0.5)
        self.rect(22, 22, 568, 748)
        
        # Rodapé Institucional
        self.setFont("Helvetica-Bold", 6.5)
        self.setFillColor(colors.HexColor("#666677"))
        self.drawString(32, 28, "THIERRY TECHNOLOGY CONCEPT | BIO GEN ENGINE - COMPUTAÇÃO SOBERANA")
        
        self.setFont("Helvetica", 5.5)
        self.setFillColor(colors.HexColor("#444455"))
        self.drawString(32, 20, "Os dados contidos neste dossiê refletem a telemetria sênior protegida sob os termos da jurisdição ativa.")
        
        page_text = f"MASTER DOSSIER UHNW | PÁGINA {self._pageNumber} DE {page_count}"
        self.drawRightString(580, 20, page_text)
        
        self.restoreState()

def gerar_dossie_pdf(filename, dados):
    """
    Função principal geradora de PDF. 
    Monta a estrutura visual de duas colunas baseada no dicionário de dados injetado.
    """
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=28,
        rightMargin=28,
        topMargin=28,
        bottomMargin=45
    )
    
    styles = getSampleStyleSheet()
    
    c_secondary = colors.HexColor("#4A1525") # Vinho Borgonha Executivo
    c_gold = colors.HexColor("#A38044")
    
    # Definição de Estilos Tipográficos
    style_top_left = ParagraphStyle('TopLeft', fontName='Helvetica-Bold', fontSize=12, textColor=colors.white, leading=14)
    style_top_right = ParagraphStyle('TopRight', fontName='Helvetica-Bold', fontSize=9, textColor=c_gold, leading=11, alignment=TA_RIGHT)
    style_meta = ParagraphStyle('Meta', fontName='Helvetica', fontSize=6.5, textColor=colors.HexColor("#D1D1D6"), leading=9)
    style_title = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=8, textColor=c_gold, leading=10)
    style_label = ParagraphStyle('Label', fontName='Helvetica', fontSize=7, textColor=colors.HexColor("#B0B0B5"), leading=9)
    style_val = ParagraphStyle('Val', fontName='Helvetica-Bold', fontSize=7, textColor=colors.white, leading=9)
    style_alert = ParagraphStyle('Alert', fontName='Helvetica-Bold', fontSize=7, textColor=colors.white, alignment=TA_CENTER, leading=10)
    style_parecer = ParagraphStyle('Parecer', fontName='Helvetica', fontSize=7, textColor=colors.HexColor("#FF5252"), leading=10)
    
    story = []
    
    # =========================================================================
    # 1. TARJA DE CABEÇALHO SOBERANO
    # =========================================================================
    t_header_data = [
        [Paragraph("THIERRY TECHNOLOGY CONCEPT | BIO GEN ENGINE UHNW", style_top_left),
         Paragraph("SOVEREIGN INTERNATIONAL<br/>MONACO & BR AUDIT", style_top_right)]
    ]
    t_header = Table(t_header_data, colWidths=[380, 176])
    t_header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_secondary),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 4))
    
    # Metadados Dinâmicos do Cliente e Operador
    meta_html = (
        f"<b>Engine Biogênico Consolidado</b> | Jurisdição: Mônaco & Brasil | "
        f"Operador: {dados.get('operador', 'Thierry (TCC SOBERANO)')} | "
        f"Timestamp: {dados.get('timestamp', '')} | "
        f"Cliente Alvo: <b>{dados.get('cliente_alvo', '')}</b> | "
        f"Credencial: {dados.get('credencial_alta', '')}"
    )
    story.append(Paragraph(meta_html, style_meta))
    story.append(Spacer(1, 10))
    
    # =========================================================================
    # 2. COLUNA ESQUERDA (Perfis de Arquitetura Sênior & Biomarcadores)
    # =========================================================================
    col_esq_story = [
        Paragraph("Perfis de Arquitetura Sênior (Morphological Analysis)", style_title),
        Spacer(1, 3),
        Table([
            [Paragraph("Perfil Principal:", style_label), Paragraph(dados.get('perfil_lideranca', ''), style_val)],
            [Paragraph("Vitalidade Celular:", style_label), Paragraph(dados.get('perfil_vitalidade', ''), style_val)],
            [Paragraph("Poder Soberano:", style_label), Paragraph(dados.get('perfil_poder', ''), style_val)],
            [Paragraph("Autonomia Estável:", style_label), Paragraph(dados.get('perfil_autonomia', ''), style_val)],
        ], colWidths=[110, 160], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 3.5), ('TOPPADDING', (0,0), (-1,-1), 3.5)]),
        
        Spacer(1, 12),
        Paragraph("Regenerative & Structural - Postura de Comando", style_title),
        Spacer(1, 3),
        Table([
            [Paragraph("Retração Mandibular:", style_label), Paragraph(dados.get('retracao_mandibular', ''), style_val)],
            [Paragraph("Tonicidade Média:", style_label), Paragraph(dados.get('tonicidade_media', ''), style_val)],
            [Paragraph("Contração Derme-Subcutânea:", style_label), Paragraph(dados.get('contracao_derme', ''), style_val)],
            [Paragraph("Integridade Estrutural (Turgor):", style_label), Paragraph(dados.get('integridade_estrutural', ''), style_val)],
        ], colWidths=[110, 160], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 3.5), ('TOPPADDING', (0,0), (-1,-1), 3.5)]),
        
        Spacer(1, 12),
        Paragraph("Clínica Médica, Epigenética e Biomarcadores", style_title),
        Spacer(1, 3),
        Table([
            [Paragraph("Idade Biológica Celular:", style_label), Paragraph(dados.get('idade_celular', ''), style_val)],
            [Paragraph("Idade Epigenética (Metilação):", style_label), Paragraph(dados.get('idade_epigenetica', ''), style_val)],
            [Paragraph("Taxa de Regeneração Celular:", style_label), Paragraph(dados.get('taxa_regeneracao', ''), style_val)],
            [Paragraph("Ápice da Regeneração:", style_label), Paragraph(dados.get('apice_regeneracao', ''), style_val)],
            [Paragraph("Volume de Água Cutânea:", style_label), Paragraph(dados.get('agua_cutanea', ''), style_val)],
            [Paragraph("Escore de Colágeno e Elastina:", style_label), Paragraph(dados.get('escore_colageno', ''), style_val)],
        ], colWidths=[110, 160], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 3), ('TOPPADDING', (0,0), (-1,-1), 3)])
    ]
    
    # =========================================================================
    # 3. COLUNA DIREITA (Vocabulário Técnico, Sensores e Governança)
    # =========================================================================
    col_dir_story = [
        Paragraph("Vocabulário Técnico e Lexicon Soberano", style_title),
        Spacer(1, 3),
        Table([
            [Paragraph("Termo / Conceito:", style_label), Paragraph(dados.get('vocab_termo', ''), style_val)],
            [Paragraph("Definição Operacional:", style_label), Paragraph(dados.get('vocab_definicao', ''), style_val)],
            [Paragraph("Modulação Tônica:", style_label), Paragraph(dados.get('vocab_modulacao', ''), style_val)],
            [Paragraph("Índice Lexical:", style_label), Paragraph(dados.get('vocab_indice', ''), style_val)],
        ], colWidths=[110, 160], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 3.5), ('TOPPADDING', (0,0), (-1,-1), 3.5)]),
        
        Spacer(1, 12),
        Paragraph("Telemetria Avançada & Sensores Bio-Gen", style_title),
        Spacer(1, 3),
        Table([
            [Paragraph("Mapeamento Facial Landmark:", style_label), Paragraph(dados.get('mapping_facial', ''), style_val)],
            [Paragraph("Filtro Espectral de Poluição:", style_label), Paragraph(dados.get('filtro_espectral', ''), style_val)],
            [Paragraph("Modulação Neuro-Gravidade:", style_label), Paragraph(dados.get('neuro_gravidade', ''), style_val)],
            [Paragraph("Credencial Ativa:", style_label), Paragraph(dados.get('credencial_alta', ''), style_val)],
            [Paragraph("Blindagem PQC (Pós-Quântica):", style_label), Paragraph(dados.get('blindagem_pqc', ''), style_val)],
        ], colWidths=[110, 160], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 3.5), ('TOPPADDING', (0,0), (-1,-1), 3.5)]),
        
        Spacer(1, 12),
        Paragraph("Projeções Biogênicas e Governança UHNW", style_title),
        Spacer(1, 3),
        Table([
            [Paragraph("Índice de Soberania Ativa:", style_label), Paragraph(dados.get('indice_soberania', ''), style_val)],
            [Paragraph("Retardamento Cronológico:", style_label), Paragraph(dados.get('retardamento_cronologico', ''), style_val)],
            [Paragraph("Margem Operacional Global:", style_label), Paragraph(dados.get('margem_operacional', ''), style_val)],
            [Paragraph("Ciclo de Payback Estrutural:", style_label), Paragraph(dados.get('payback_estrutural', ''), style_val)],
        ], colWidths=[110, 160], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 3.5), ('TOPPADDING', (0,0), (-1,-1), 3.5)]),
        
        Spacer(1, 14),
        # Bloco de Parecer Técnico Oficial
        Table([
            [Paragraph("PARECER BIO GEN ENGINE: REVITALIZAÇÃO VALIDADA", style_alert)],
            [Paragraph("Perfis de liderança e comando ativados com sucesso. Tonicidade e parâmetros estruturais alinhados ao padrão Monaco Sovereign Pass v3.", style_parecer)]
        ], colWidths=[270], style=[
            ('BACKGROUND', (0,0), (-1,0), c_secondary),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#14141C")),
            ('PADDING', (0,0), (-1,-1), 6),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ])
    ]
    
    # Layout de duas colunas paralelas
    t_master_layout = Table([[col_esq_story, col_dir_story]], colWidths=[278, 278])
    t_master_layout.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LINEAFTER', (0,0), (0,0), 0.5, colors.HexColor("#2A2A3A")),
    ]))
    
    story.append(t_master_layout)
    doc.build(story, canvasmaker=SovereignCanvas)
    return filename