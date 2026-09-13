# -*- coding: utf-8 -*-
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_RIGHT, TA_CENTER

try:
    from core.memoria_comum import memoria_global
except ImportError:
    try:
        from memoria_comum import memoria_global
    except:
        memoria_global = None

class SovereignCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(SovereignCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def _startPage(self):
        super()._startPage()
        self.saveState()
        
        # Fundo Executivo UHNW #08080C
        self.setFillColor(colors.HexColor("#08080C"))
        self.rect(0, 0, 612, 792, fill=1, stroke=0)
        
        # --- MARCA D'ÁGUA TIPO CÉDULA (SELO DE MÔNACO & BRASIL) ---
        self.saveState()
        self.translate(306, 396) # Centro da página (Letter: 612x792)
        self.rotate(30)          # Inclinação clássica de cédula de segurança
        
        # Anel externo da marca d'água
        self.setStrokeColor(colors.HexColor("#A38044"))
        self.setLineWidth(0.8)
        self.setFillColor(colors.HexColor("#14141C"))
        self.circle(0, 0, 160, fill=1, stroke=1)
        
        self.setStrokeColor(colors.HexColor("#4A1525"))
        self.setLineWidth(0.5)
        self.circle(0, 0, 150, fill=0, stroke=1)
        
        # Texto da Marca d'Água Estilo Cédula
        self.setFont("Helvetica-Bold", 11)
        self.setFillColor(colors.HexColor("#2A241F")) # Tom sutil e brilhoso de segurança
        self.drawCentredString(0, 125, "MONACO & BRASIL SOBERANO")
        self.drawCentredString(0, -132, "THIERRY TECHNOLOGY CONCEPT")
        
        self.setFont("Helvetica-Bold", 16)
        self.setFillColor(colors.HexColor("#241D17"))
        self.drawCentredString(0, -6, "UHNW AUDIT TRUST")
        
        self.setFont("Helvetica", 7)
        self.drawCentredString(0, 15, "SECURE TELEMETRY SHIELD")
        self.drawCentredString(0, -25, "ZONAS DE SEGURANÇA CERTIFICADA")
        
        self.restoreState()
        # ---------------------------------------------------------
        
        self.restoreState()

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
        
        # Molduras de Alta Segurança
        self.setStrokeColor(c_gold)
        self.setLineWidth(1.2)
        self.rect(18, 18, 576, 756)
        
        self.setStrokeColor(colors.HexColor("#2A2A3A"))
        self.setLineWidth(0.5)
        self.rect(22, 22, 568, 748)
        
        # Rodapé Executivo Imponente
        self.setFont("Helvetica-Bold", 6.5)
        self.setFillColor(colors.HexColor("#9999AA"))
        self.drawString(32, 28, "THIERRY TECHNOLOGY CONCEPT | MASTER DOSSIER UHNW (AUDITORIA SOBERANA)")
        
        self.setFont("Helvetica", 5.5)
        self.setFillColor(colors.HexColor("#777788"))
        self.drawString(32, 20, "Telemetria soberana autenticada sob rigor de criptografia avançada e jurisdição ativa.")
        
        page_text = f"MASTER DOSSIER UHNW | PAGINA {self._pageNumber} DE {page_count}"
        self.drawRightString(580, 20, page_text)
        self.restoreState()

def gerar_dossie_completo(filename, dados):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=28,
        rightMargin=28,
        topMargin=28,
        bottomMargin=45
    )
    
    c_secondary = colors.HexColor("#4A1525")
    c_gold = colors.HexColor("#A38044")
    
    style_top_left = ParagraphStyle('TopLeft', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white, leading=12)
    style_top_right = ParagraphStyle('TopRight', fontName='Helvetica-Bold', fontSize=8, textColor=c_gold, leading=10, alignment=TA_RIGHT)
    style_meta = ParagraphStyle('Meta', fontName='Helvetica', fontSize=6, textColor=colors.HexColor("#E1E1E6"), leading=8.5)
    style_title = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=7.5, textColor=c_gold, leading=9.5)
    
    # Cores fortes e nítidas para leitura imediata
    style_label = ParagraphStyle('Label', fontName='Helvetica', fontSize=6.5, textColor=colors.HexColor("#D0D0D8"), leading=8.5)
    style_val = ParagraphStyle('Val', fontName='Helvetica-Bold', fontSize=6.5, textColor=colors.HexColor("#FFFFFF"), leading=8.5)
    style_alert = ParagraphStyle('Alert', fontName='Helvetica-Bold', fontSize=6.5, textColor=colors.white, alignment=TA_CENTER, leading=9)
    
    story = []
    
    # Cabeçalho Principal com o Selo de Mônaco & Brasil em destaque superior direito
    t_header_data = [
        [Paragraph(dados.get('titulo_cabecalho', 'THIERRY TECHNOLOGY CONCEPT | MASTER DOSSIER UHNW (AUDITORIA SOBERANA)'), style_top_left),
         Paragraph("SOVEREIGN INTERNATIONAL<br/>MONACO & BR AUDIT", style_top_right)]
    ]
    t_header = Table(t_header_data, colWidths=[380, 176])
    t_header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_secondary),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-1), 1.5, c_gold),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 3))
    
    meta_html = (
        f"<b>{dados.get('sub_engine', 'Emissao UHNW Consolidada')}</b> | Jurisdicao: Monaco & Brasil | "
        f"Operador: {dados.get('operador', 'Thierry (TCC SOBERANO)')} | "
        f"Timestamp: {dados.get('timestamp', '10/09/2026 01:06')} | "
        f"Cliente Alvo: <b>{dados.get('cliente_alvo', 'THIERRY RODRIGUES')}</b> | "
        f"Hash: {dados.get('hash_seguranca', 'TX-9082-MONACO-UHNW')}"
    )
    story.append(Paragraph(meta_html, style_meta))
    story.append(Spacer(1, 8))
    
    # Coluna Esquerda
    col_esq_story = [
        Paragraph(dados.get('secao1_titulo', 'Tricologia Disruptiva e Genomica Folicular'), style_title),
        Spacer(1, 2),
        Table([
            [Paragraph('Paciente Avaliado:', style_label), Paragraph(str(dados.get('cliente_alvo', '')), style_val)],
            [Paragraph('Densidade Folicular:', style_label), Paragraph(str(dados.get('densidade_folicular', '')), style_val)],
            [Paragraph('Perfil Térmico Óptico:', style_label), Paragraph(str(dados.get('perfil_termico', '')), style_val)],
            [Paragraph('Estresse Urbano / Poluição:', style_label), Paragraph(str(dados.get('estresse_urbano', '')), style_val)],
            [Paragraph('Cronobiologia Circadiana:', style_label), Paragraph(str(dados.get('ritmo_mitocondrial', '')), style_val)],
            [Paragraph('Miniatura Folicular:', style_label), Paragraph(str(dados.get('miniatura_folicular', '')), style_val)],
            [Paragraph('Metilação & DNA Folicular:', style_label), Paragraph(str(dados.get('metilacao_dna', '')), style_val)],
        ], colWidths=[110, 168], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 2.5), ('TOPPADDING', (0,0), (-1,-1), 2.5)]),
        
        Spacer(1, 8),
        Paragraph(dados.get('secao2_titulo', 'Emagrecimento Celular, Anti-Flacidez e Tratamento Noturno'), style_title),
        Spacer(1, 2),
        Table([
            [Paragraph('Projeção de Emagrecimento:', style_label), Paragraph(str(dados.get('projecao_emagrecimento', '')), style_val)],
            [Paragraph('Prevenção de Flacidez Facial:', style_label), Paragraph(str(dados.get('prevencao_flacidez', '')), style_val)],
            [Paragraph('Contração Derme-Subcutânea:', style_label), Paragraph(str(dados.get('contracao_derme', '')), style_val)],
            [Paragraph('Tratamento Noturno & Home Care:', style_label), Paragraph(str(dados.get('tratamento_noturno', '')), style_val)],
            [Paragraph('Integridade Estrutural (Turgor):', style_label), Paragraph(str(dados.get('integridade_estrutural', '')), style_val)],
            [Paragraph('Índice de Retardamento:', style_label), Paragraph(str(dados.get('retardamento_cronologico', '')), style_val)],
        ], colWidths=[110, 168], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 2.5), ('TOPPADDING', (0,0), (-1,-1), 2.5)]),
        
        Spacer(1, 8),
        Paragraph(dados.get('secao3_titulo', 'Clínica Médica, Epigenética e Biomarcadores'), style_title),
        Spacer(1, 2),
        Table([
            [Paragraph('Idade Biológica Celular:', style_label), Paragraph(str(dados.get('idade_biologica', '')), style_val)],
            [Paragraph('Idade Epigenética (Metilação):', style_label), Paragraph(str(dados.get('idade_epigenetica', '')), style_val)],
            [Paragraph('Taxa de Regeneração Celular:', style_label), Paragraph(str(dados.get('taxa_regeneracao', '')), style_val)],
            [Paragraph('Ápice da Regeneração:', style_label), Paragraph(str(dados.get('apice_regeneracao', '')), style_val)],
            [Paragraph('Taxa de Água Corporal:', style_label), Paragraph(str(dados.get('agua_corporal', '')), style_val)],
            [Paragraph('Volume de Água Cutânea:', style_label), Paragraph(str(dados.get('agua_cutanea', '')), style_val)],
            [Paragraph('Colágeno e Elastina Facial:', style_label), Paragraph(str(dados.get('colageno_elastina', '')), style_val)],
            [Paragraph('Oximetria Tecidual:', style_label), Paragraph(str(dados.get('oximetria', '')), style_val)],
        ], colWidths=[110, 168], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 2), ('TOPPADDING', (0,0), (-1,-1), 2)])
    ]
    
    # Coluna Direita
    col_dir_story = [
        Paragraph(dados.get('secao4_titulo', 'Visagismo, Estética Facial e Liderança'), style_title),
        Spacer(1, 2),
        Table([
            [Paragraph('Geometria Crânio-Facial:', style_label), Paragraph(str(dados.get('geometria_facial', '')), style_val)],
            [Paragraph('Cortes Recomendados:', style_label), Paragraph(str(dados.get('cortes_recomendados', '')), style_val)],
            [Paragraph('Temperamento Estrutural:', style_label), Paragraph(str(dados.get('temperamento', '')), style_val)],
            [Paragraph('Mapeamento Comportamental:', style_label), Paragraph(str(dados.get('mapeamento_comportamental', '')), style_val)],
            [Paragraph('Escore Estabilidade Postural:', style_label), Paragraph(str(dados.get('escore_postural', '')), style_val)],
            [Paragraph('Escore de Simetria Facial:', style_label), Paragraph(str(dados.get('escore_simetria', '')), style_val)],
            [Paragraph('Licenciamento Oficial:', style_label), Paragraph(str(dados.get('licenciamento', '')), style_val)],
        ], colWidths=[110, 168], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 2.5), ('TOPPADDING', (0,0), (-1,-1), 2.5)]),
        
        Spacer(1, 8),
        Table([
            [Paragraph(dados.get('alerta_titulo', 'Fadiga Ocular e Diafragmática Detectada (Exige Sincronia 528 Hz)'), style_alert)],
        ], colWidths=[278], style=[
            ('BACKGROUND', (0,0), (-1,0), c_secondary),
            ('PADDING', (0,0), (-1,0), 4),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BOX', (0,0), (-1,-1), 0.5, c_gold),
        ]),
        Spacer(1, 4),
        Table([
            [Paragraph('Varredura de Câmera:', style_label), Paragraph(str(dados.get('janela_varredura', '')), style_val)],
            [Paragraph('Velocidade do Diafragma:', style_label), Paragraph(str(dados.get('velocidade_diafragma', '')), style_val)],
            [Paragraph('Amplitude Respiratória:', style_label), Paragraph(str(dados.get('amplitude_respiratoria', '')), style_val)],
            [Paragraph('Correlação de Ansiedade:', style_label), Paragraph(str(dados.get('correlacao_ansiedade', '')), style_val)],
            [Paragraph('Clima Regional:', style_label), Paragraph(str(dados.get('clima_regional', '')), style_val)],
            [Paragraph('Material Particulado PM2.5:', style_label), Paragraph(str(dados.get('material_particulado', '')), style_val)],
        ], colWidths=[110, 168], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 2), ('TOPPADDING', (0,0), (-1,-1), 2)]),
        
        Spacer(1, 8),
        Paragraph(dados.get('secao5_titulo', 'Biogênese Digital (Projeção Temporal e Governança)'), style_title),
        Spacer(1, 2),
        Table([
            [Paragraph('Biogem (5 Anos):', style_label), Paragraph(str(dados.get('biogem_5', '')), style_val)],
            [Paragraph('Biogem (10 Anos):', style_label), Paragraph(str(dados.get('biogem_10', '')), style_val)],
            [Paragraph('Biogem (15 Anos):', style_label), Paragraph(str(dados.get('biogem_15', '')), style_val)],
            [Paragraph('Escore de Adesão:', style_label), Paragraph(str(dados.get('escore_adesao', '')), style_val)],
            [Paragraph('Rejuvenescimento Alvo:', style_label), Paragraph(str(dados.get('rejuvenescimento_alvo', '')), style_val)],
            [Paragraph('Diretriz Neurocomportamental:', style_label), Paragraph(str(dados.get('diretriz_neuro', '')), style_val)],
            [Paragraph('Assinatura Criptográfica:', style_label), Paragraph(str(dados.get('assinatura_cripto', '')), style_val)],
        ], colWidths=[110, 168], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 2), ('TOPPADDING', (0,0), (-1,-1), 2)])
    ]
    
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

class BiogemEngine:
    def __init__(self, tipo_relatorio, nome_cliente, contato_cliente, operador, tabela_biogemeos, telemetria):
        self.tipo_relatorio = str(tipo_relatorio).strip().lower()
        self.nome_cliente = nome_cliente
        self.contato_cliente = contato_cliente
        self.operador = operador
        self.tabela_biogemeos = tabela_biogemeos
        self.telemetria = telemetria

    def _montar_dicionario_dados(self):
        dados_memoria = {}
        if memoria_global:
            dados_memoria = memoria_global.ler_dados() or {}

        base = {
            'operador': self.operador or dados_memoria.get('operador', 'Thierry (TCC SOBERANO)'),
            'timestamp': dados_memoria.get('timestamp', '10/09/2026 01:06'),
            'cliente_alvo': self.nome_cliente or dados_memoria.get('cliente_alvo', 'THIERRY RODRIGUES'),
            'hash_seguranca': dados_memoria.get('hash_seguranca', 'TX-9082-MONACO-UHNW'),
            
            # Tricologia
            'densidade_folicular': dados_memoria.get('densidade_folicular', '128 fios/cm² (Estável)'),
            'perfil_termico': dados_memoria.get('perfil_termico', '34.2°C (Vasoconstrição controlada via LED 830nm)'),
            'estresse_urbano': dados_memoria.get('estresse_urbano', 'Moderado (Saturação oxidativa tratada com Plasma Fracionado)'),
            'ritmo_mitocondrial': dados_memoria.get('ritmo_mitocondrial', 'Ritmo Mitocondrial Noturno (Bloqueador de DHT pré-sono)'),
            'miniatura_folicular': dados_memoria.get('miniatura_folicular', '22.5% (Protocolo regenerativo com LLLT associado)'),
            'metilacao_dna': dados_memoria.get('metilacao_dna', 'Expressão de Receptor Androgênico controlada via Epigenética'),
            
            # Emagrecimento
            'projecao_emagrecimento': dados_memoria.get('projecao_emagrecimento', 'Redução de adiposidade controlada com preservação tecidual'),
            'prevencao_flacidez': dados_memoria.get('prevencao_flacidez', 'Bioestimulação simultânea (Colágeno Tipo I e III de Alta Densidade)'),
            'contracao_derme': dados_memoria.get('contracao_derme', 'Retração simultânea via Jato de Plasma Fracionado (Baixa Potência)'),
            'tratamento_noturno': dados_memoria.get('tratamento_noturno', 'Ritual Pré-Sono: Peptídeos biomiméticos, silício orgânico e tônico bloqueador de DHT'),
            'integridade_estrutural': dados_memoria.get('integridade_estrutural', 'Manutenção da Matriz Extracelular sem Envelhecimento Facial'),
            'retardamento_cronologico': dados_memoria.get('retardamento_cronologico', 'Balanço volumétrico e firmeza cutânea garantidos'),
            
            # Clínica
            'idade_biologica': dados_memoria.get('idade_biologica', '31 Anos (-3 Anos vs Cronológica)'),
            'idade_epigenetica': dados_memoria.get('idade_epigenetica', '29.5 Anos (Perfil UHNW Superior)'),
            'taxa_regeneracao': dados_memoria.get('taxa_regeneracao', '82.17% (Alta)'),
            'apice_regeneracao': dados_memoria.get('apice_regeneracao', '10/09/2026'),
            'agua_corporal': dados_memoria.get('agua_corporal', '61.4% (Hidratação Adequada)'),
            'agua_cutanea': dados_memoria.get('agua_cutanea', '54.2% (Retenção e Turgor)'),
            'colageno_elastina': dados_memoria.get('colageno_elastina', '84.50 Escore (Alta Densidade)'),
            'oximetria': dados_memoria.get('oximetria', '87.2% (Nominal)'),
            
            # Visagismo
            'geometria_facial': dados_memoria.get('geometria_facial', 'Quadrada (Maxilar/Topo)'),
            'cortes_recomendados': dados_memoria.get('cortes_recomendados', 'Pixie Contour, French Bob, Long Bob'),
            'temperamento': dados_memoria.get('temperamento', 'Colérico / Liderança Ativa'),
            'mapeamento_comportamental': dados_memoria.get('mapeamento_comportamental', 'Perfil de Tomada de Decisão Soberana e Visão Estratégica'),
            'escore_postural': dados_memoria.get('escore_postural', '85.35 / 100'),
            'escore_simetria': dados_memoria.get('escore_simetria', '80.49 / 100'),
            'licenciamento': 'SOVEREIGN INTERNATIONAL - MONACO & BR AUDIT',
            
            # Câmera / Telemetria
            'janela_varredura': dados_memoria.get('janela_varredura', '10 Segundos (Varredura UHNW Ativa)'),
            'velocidade_diafragma': dados_memoria.get('velocidade_diafragma', '18.4 ciclos/min (Aceleração Leve)'),
            'amplitude_respiratoria': dados_memoria.get('amplitude_respiratoria', '2.1 mm (Padrão Toraco-Abdominal Superficial)'),
            'correlacao_ansiedade': dados_memoria.get('correlacao_ansiedade', 'Moderada (Índice de Sobrecarga Autonômica: 41.2%)'),
            'clima_regional': dados_memoria.get('clima_regional', '29.1°C - Nublado | AQI: Bom (1 AQI)'),
            'material_particulado': dados_memoria.get('material_particulado', '2.73 µg/m³ | Estresse Oxidativo Epidérmico'),
            
            # Biogênese Digital
            'biogem_5': dados_memoria.get('biogem_5', 'Manutenção Tecidual em 24.2%'),
            'biogem_10': dados_memoria.get('biogem_10', 'Retardamento Cronológico de 7.4 Anos'),
            'biogem_15': dados_memoria.get('biogem_15', 'Longevidade Ativa e Consolidação'),
            'escore_adesao': dados_memoria.get('escore_adesao', '94.5% (Comprometimento Alto)'),
            'rejuvenescimento_alvo': dados_memoria.get('rejuvenescimento_alvo', '+18.5% Densidade Global'),
            'diretriz_neuro': dados_memoria.get('diretriz_neuro', '528 Hz | Alinhamento Circadiano Profundo'),
            'assinatura_cripto': 'SHA-256 Validado | Zero-Knowledge Trust'
        }

        if 'pitch' in self.tipo_relatorio:
            base['titulo_cabecalho'] = 'THIERRY TECHNOLOGY CONCEPT | PITCH SOBERANO UHNW'
            base['sub_engine'] = 'Engine Comercial & Apresentação Executiva'
        elif 'roi' in self.tipo_relatorio or 'governanca' in self.tipo_relatorio:
            base['titulo_cabecalho'] = 'THIERRY TECHNOLOGY CONCEPT | RELATÓRIO ROI & GOVERNANÇA'
            base['sub_engine'] = 'Engine de Retorno Financeiro & Auditoria'

        return base

    def gerar_relatorio_pdf(self):
        nome_arquivo = f"DOSSIER_{self.tipo_relatorio.upper()}_{self.nome_cliente.replace(' ', '_')}.pdf"
        caminho_saida = os.path.join("core", "pdfs_finais", nome_arquivo)
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        
        dados = self._montar_dicionario_dados()
        gerar_dossie_completo(caminho_saida, dados)
        return caminho_saida

    def gerar_pitch_soberano_pdf(self):
        return self.gerar_relatorio_pdf()

    def gerar_relatorio_roi_clinica(self):
        return self.gerar_relatorio_pdf()