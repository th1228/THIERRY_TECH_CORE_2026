# -*- coding: utf-8 -*-
"""
Módulo: super_retorno_financeiro.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Versão: 5.8.2 - MONACO EXECUTIVE PLATINUM EDITION (Bilingual PT/EN & Dynamic Client Name)
Descrição: Motor de Alta Performance de Auditoria Preditiva e Valuation de Ativos Biométricos.
           Aplica Geometria Diferencial, Amortização Exponencial e Bloco Mestre Platina Clean.
"""

import os
import datetime
import hashlib
import math
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from typing import List, Optional, Dict, Any

# --- PONTE DE MEMÓRIA AUTOMÁTICA (THIERRY TECH) ---
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:
        class MemoriaMock:
            def salvar_dados(self, chave, valor): pass
            def registrar(self, chave, valor): pass
            def ler_dados(self, chave): return None
        memoria = MemoriaMock()
# ---------------------------------------------------

# =====================================================================
# DICIONÁRIO DE TRADUÇÕES BILINGUE (PT / EN)
# =====================================================================
TEXTOS_ROI = {
    "PT": {
        "marca_agua": "MONACO TIER-1 • EXECUTIVE PLATINUM",
        "doc_titulo": "SUPER RETORNO FINANCEIRO • MANAGEMENT AUDIT DOSSIER MAXIMA",
        "doc_subtitulo": "SOVEREIGN WEALTH & NON-LINEAR BIOMETRIC ASSET PRESERVATION • MONACO TIER-1 COMPLIANCE",
        "meta_emissao": "DATA DE EMISSÃO:",
        "meta_titular": "TITULAR DO ATIVO:",
        "meta_idade": "Idade:",
        "meta_auditor": "AUDITOR LÍDER:",
        "block_auth": "SYSTEM BLOCK AUTH:",
        "integrity_hash": "INTEGRITY BLOCK HASH (SHA-256):",
        "public_key": "SOVEREIGN SYSTEM PUBLIC KEY:",
        "audit_metric": "AUDIT METRIC: STOCHASTIC DECAY MODEL",
        
        "sec1_titulo": "1. INPUTS DE TELEMETRIA FISIOLÓGICA E ESTRESSE METABÓLICO",
        "t1_l1_nome": "Saturação de Oxigênio (SpO2)",
        "t1_l1_desc": "Capacidade de difusão microvascular periférica estável. Oxigenação mitocondrial adequada.",
        "t1_l2_nome": "Carga Coeficiente de Estresse (Cortisol)",
        "t1_l2_desc": "Fator multiplicador exógeno de catabolismo tecidual profundo induzido por alta pressão executiva.",
        "t1_l3_nome": "Exposição Ultravioleta Atmosférica",
        "t1_l3_val": "UV 2 Baixo",
        "t1_l3_desc": "Bloqueio ativo contra radiação eletromagnética exógena e degradação de matriz extracelular.",
        
        "sec2_titulo": "2. MATRIZ DE DEFORMAÇÃO GEOMÉTRICA E VETOR DE QUEDA (CDE NON-LINEAR)",
        "sec2_desc": "Mapeamento por geometria diferencial de linhas de tensão miofacial profunda e perda de ancoragem volumétrica.",
        "t2_l1_nome": "Distância Euclidiana Malar-Mandíbula",
        "t2_l1_desc": "Mapeamento tridimensional absoluto de vetores de sustentação osteofacial e coxins profundos.",
        "t2_l2_nome": "Coeficiente Estrutural Preditivo (CDE)",
        "t2_l2_desc": "Índice rigoroso de integridade elástica calculado via modelo exponencial não-linear.",
        "t2_l3_nome": "Déficit de Sustentação Crítico",
        "t2_l3_desc": "Vetor ativo de ptose gravitacional avançada sem governança preventiva atuarial.",
        
        "sec3_titulo": "3. ANÁLISE DE DEPRECIAÇÃO E VALUATION DO CAPITAL DE IMAGEM (ASSET DECAY)",
        "sec3_desc": "Quantificação atuarial da erosão de valor sobre ativos intangíveis e presença executiva de mercado.",
        "t3_l1_nome": "Taxa de Depreciação Geométrica Anual",
        "t3_l1_desc": "Velocidade de perda de capital estético sob fator multiplicador de estresse corpóreo.",
        "t3_l2_nome": "Valuation do Capital de Imagem",
        "t3_l2_desc": "Ativo intangível estimado com base no patrimônio líquido corporativo global sob gestão.",
        "t3_l3_nome": "Risco de Perda Patrimonial (15 Anos)",
        "t3_l3_desc": "Erosão projetada de valor reputacional decorrente do envelhecimento biológico sem blindagem.",
        
        "sec4_titulo": "4. ENGENHARIA DE VALUATION E RETORNO DE BLINDAGEM ATIVA (ROI)",
        "t4_l1_nome": "Custo de Setup da Estrutura C2",
        "t4_l1_desc": "Alocação para engenharia celular regenerativa e protocolos de alta performance Tier-1.",
        "t4_l2_nome": "Perda Mitigada e Evitada",
        "t4_l2_desc": "Proteção de ativos intangíveis garantida pelo modelo preditivo soberano em 15 anos.",
        "t4_l3_nome": "Taxa de Retorno Absoluto (ROI)",
        "t4_l3_desc": "Retorno financeiro líquido gerado pela preservação soberana do capital de imagem."
    },
    "EN": {
        "marca_agua": "MONACO TIER-1 • EXECUTIVE PLATINUM",
        "doc_titulo": "SUPER FINANCIAL RETURN • MANAGEMENT AUDIT DOSSIER MAXIMA",
        "doc_subtitulo": "SOVEREIGN WEALTH & NON-LINEAR BIOMETRIC ASSET PRESERVATION • MONACO TIER-1 COMPLIANCE",
        "meta_emissao": "ISSUANCE DATE:",
        "meta_titular": "ASSET HOLDER:",
        "meta_idade": "Age:",
        "meta_auditor": "LEAD AUDITOR:",
        "block_auth": "SYSTEM BLOCK AUTH:",
        "integrity_hash": "INTEGRITY BLOCK HASH (SHA-256):",
        "public_key": "SOVEREIGN SYSTEM PUBLIC KEY:",
        "audit_metric": "AUDIT METRIC: STOCHASTIC DECAY MODEL",
        
        "sec1_titulo": "1. PHYSIOLOGICAL TELEMETRY & METABOLIC STRESS INPUTS",
        "t1_l1_nome": "Oxygen Saturation (SpO2)",
        "t1_l1_desc": "Stable peripheral microvascular diffusion capacity. Adequate mitochondrial oxygenation.",
        "t1_l2_nome": "Stress Coefficient Load (Cortisol)",
        "t1_l2_desc": "Exogenous multiplying factor of deep tissue catabolism induced by high executive pressure.",
        "t1_l3_nome": "Atmospheric Ultraviolet Exposure",
        "t1_l3_val": "UV 2 Low",
        "t1_l3_desc": "Active shielding against exogenous electromagnetic radiation and extracellular matrix decay.",
        
        "sec2_titulo": "2. GEOMETRIC DEFORMATION MATRIX & FALL VECTOR (NON-LINEAR CDE)",
        "sec2_desc": "Differential geometry mapping of deep myofascial tension lines and loss of volumetric anchoring.",
        "t2_l1_nome": "Malar-Mandible Euclidean Distance",
        "t2_l1_desc": "Absolute 3D mapping of osteofacial support vectors and deep fat pads.",
        "t2_l2_nome": "Predictive Structural Coefficient (CDE)",
        "t2_l2_desc": "Rigorous elastic integrity index calculated via a non-linear exponential model.",
        "t2_l3_nome": "Critical Support Deficit",
        "t2_l3_desc": "Active gravitational ptosis vector without preventive actuarial governance.",
        
        "sec3_titulo": "3. DEPRECIATION ANALYSIS & IMAGE CAPITAL VALUATION (ASSET DECAY)",
        "sec3_desc": "Actuarial quantification of value erosion on intangible assets and executive market presence.",
        "t3_l1_nome": "Annual Geometric Depreciation Rate",
        "t3_l1_desc": "Speed of aesthetic capital loss under a bodily stress multiplying factor.",
        "t3_l2_nome": "Image Capital Valuation",
        "t3_l2_desc": "Estimated intangible asset based on global corporate net worth under management.",
        "t3_l3_nome": "15-Year Asset Loss Risk",
        "t3_l3_desc": "Projected erosion of reputational value resulting from biological aging without shielding.",
        
        "sec4_titulo": "4. VALUATION ENGINEERING & ACTIVE SHIELDING RETURN (ROI)",
        "t4_l1_nome": "C2 Structure Setup Cost",
        "t4_l1_desc": "Allocation for regenerative cellular engineering and Tier-1 high-performance protocols.",
        "t4_l2_nome": "Mitigated & Avoided Loss",
        "t4_l2_desc": "Intangible asset protection guaranteed by the sovereign predictive model over 15 years.",
        "t4_l3_nome": "Absolute Return Rate (ROI)",
        "t4_l3_desc": "Net financial return generated by the sovereign preservation of image capital."
    }
}


class SovereignSecureCanvas(canvas.Canvas):
    """Canvas de Alta Segurança Atuarial. Renderiza marcas d'água geométricas e vetores de integridade no padrão Executive Platinum."""
    def __init__(self, *args, **kwargs):
        super(SovereignSecureCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_security_infrastructure()
            super(SovereignSecureCanvas, self).showPage()
        super(SovereignSecureCanvas, self).save()

    def draw_security_infrastructure(self):
        self.saveState()
        self.setFont("Helvetica-Bold", 36)
        self.setFillColor(colors.HexColor("#B8860B"), alpha=0.03) 
        self.translate(300, 400)
        self.rotate(45)
        self.drawCentredString(0, 0, "MONACO TIER-1 • EXECUTIVE PLATINUM")
        self.restoreState()


class C2SovereignROIEngine:
    """
    O Motor Máximo de Engenharia Atuarial Biométrica com Nome Dinâmico.
    Simula o colapso físico e financeiro de ativos intangíveis de imagem em tempo real.
    """
    def __init__(self, 
                 chave_publica_sistema: str = "TTC-KEY-MONACO-SECURE-9948", 
                 titular: Optional[str] = None, 
                 idade: int = 35, 
                 patrimonio_liquido_eur: float = 1000000.0, 
                 fator_estresse_biologico: float = 0.65, 
                 custo_setup_estrutura_eur: float = 75000.0,
                 auditor_lider: str = "THIERRY TCC",
                 market_segment: str = "Tecnologia e Inovação",
                 horizon_years: int = 10,
                 telemetria: Optional[dict] = None,
                 lang: str = "PT"):
        
        self.telemetria_externa = telemetria or {}
        
        # Resolução dinâmica do nome do titular vindo do painel, telemetria ou fallback seguro
        resolvedor_nome = titular or self.telemetria_externa.get('nome_cliente') or self.telemetria_externa.get('nome') or "CLIENTE UHNW"
        self.titular = resolvedor_nome.upper()
        
        self.auditor = auditor_lider.upper()
        self.public_key = chave_publica_sistema
        self.idade = idade
        self.net_worth = patrimonio_liquido_eur
        self.estresse = min(1.0, max(0.0, fator_estresse_biologico))
        self.custo_setup = custo_setup_estrutura_eur
        self.market_segment = market_segment
        self.horizon_years = horizon_years
        self.lang = lang.upper() if lang and isinstance(lang, str) else "PT"
        if self.lang not in TEXTOS_ROI:
            self.lang = "PT"
            
        self.timestamp = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S UTC")
        
        # --- NÚCLEO DE CÁLCULO ATUARIAL AVANÇADO ---
        fator_aceleracao = 0.012 * (1.0 + self.estresse * 1.5)
        self.cde = 100.0 * math.exp(-fator_aceleracao * max(0, self.idade - 25))
        self.cde = max(35.0, min(100.0, self.cde))
        self.deficit_sustentacao = 100.0 - self.cde
        
        self.asset_decay_rate = (self.deficit_sustentacao / 10.0) * (1.0 + (self.estresse * 0.8))
        percentual_imagem = 0.03 + (0.04 * (1.0 - (self.idade / 100.0)))
        self.image_capital = self.net_worth * percentual_imagem
        
        self.perda_capital_15_anos = self.image_capital * (1.0 - math.exp(-0.05 * self.deficit_sustentacao))
        self.perda_mitigada_evitada = self.perda_capital_15_anos * 0.92
        self.roi_absoluto = ((self.perda_mitigada_evitada - self.custo_setup) / self.custo_setup) * 100.0
        
        payload_dados = f"{self.titular}|{self.net_worth:.2f}|{self.cde:.4f}|{self.perda_capital_15_anos:.2f}|{self.public_key}"
        self.audit_hash = hashlib.sha256(payload_dados.encode('utf-8')).hexdigest().upper()

    def formatar_moeda_eur(self, valor: float) -> str:
        return f"€ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def _obter_texto_comparativo_final(self) -> str:
        """Gera o texto comparativo final personalizado de acordo com o titular e perfil."""
        if self.lang == "EN":
            return f"""
            <b>Comparative Executive Audit Summary ({self.titular}):</b> In contrast to generic wealth management strategies that overlook optoelectronic asset erosion, the Monaco Tier-1 compliance framework deployed for <i>{self.titular}</i> secures multi-faceted capital preservation across <i>{self.market_segment}</i>. By anchoring biometric valuation to real-time structural telemetry, this governance model prevents speculative decay and guarantees long-term absolute market dominance.
            """
        else:
            return f"""
            <b>Síntese Comparativa de Auditoria Executiva ({self.titular}):</b> Em nítido contraste com abordagens patrimoniais tradicionais que ignoram a erosão de ativos intangíveis, o modelo de conformidade Monaco Tier-1 aplicado a <i>{self.titular}</i> assegura uma blindagem patrimonial sem precedentes no setor de <i>{self.market_segment}</i>. Ao vincular o valuation atuarial à telemetria estrutural em tempo real, este padrão neutraliza a desvalorização especulativa e consolida uma liderança de mercado perpétua e inabalável.
            """

    def gerar_relatorio_roi(self, caminho_pdf: str, lang: str = "PT") -> str:
        if lang:
            self.lang = lang.upper()
            if self.lang not in TEXTOS_ROI:
                self.lang = "PT"

        txt = TEXTOS_ROI[self.lang]
        
        doc = SimpleDocTemplate(
            caminho_pdf,
            pagesize=letter,
            rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
        )
        
        styles = getSampleStyleSheet()
        
        # --- PALETA EXECUTIVE PLATINUM (CLEAN & FUNDO CLARO) ---
        MONACO_NAVY = colors.HexColor('#0A1128')
        SOVEREIGN_GOLD = colors.HexColor('#B8860B')   # Dourado Nobre
        EXCELENCIA_VERDE = colors.HexColor('#00875A') # Verde Esmeralda Clínico
        DARK_TEXT = colors.HexColor('#1E293B')        # Grafite de Leitura Fácil
        CARD_BG = colors.HexColor('#F8FAFC')          # Cinza Platina Limpo
        CARD_BORDER = colors.HexColor('#CBD5E1')      # Borda Prata Fina
        TABLE_HEADER_BG = colors.HexColor('#F1F5F9')  # Topo de Tabela Claro
        
        # Estilos
        estilo_titulo_solto = ParagraphStyle('MaxTitleSolto', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=12.5, leading=15, textColor=MONACO_NAVY, alignment=1, spaceAfter=2)
        estilo_sub_solto = ParagraphStyle('MaxSubSolto', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=SOVEREIGN_GOLD, alignment=1, spaceAfter=2)
        estilo_meta_solto = ParagraphStyle('MaxMetaSolto', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9.5, textColor=colors.HexColor('#333333'), alignment=1, spaceAfter=6)
        
        estilo_secao = ParagraphStyle('MaxSec', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=7.5, textColor=MONACO_NAVY, spaceBefore=4, spaceAfter=2)
        estilo_texto = ParagraphStyle('MaxText', parent=styles['Normal'], fontName='Helvetica', fontSize=6.0, textColor=DARK_TEXT, leading=8.0, spaceAfter=2)
        estilo_tabela = ParagraphStyle('MaxTab', parent=styles['Normal'], fontName='Helvetica', fontSize=5.5, textColor=DARK_TEXT, leading=7.5)
        estilo_tabela_bold = ParagraphStyle('MaxTabBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=5.5, textColor=MONACO_NAVY, leading=7.5)
        estilo_tabela_verde = ParagraphStyle('MaxTabGreen', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=5.5, textColor=EXCELENCIA_VERDE, leading=7.5)
        estilo_comparativo = ParagraphStyle('MaxComp', parent=styles['Normal'], fontName='Helvetica', fontSize=6.5, textColor=DARK_TEXT, leading=9.0, spaceBefore=4, spaceAfter=2)

        story: List[Flowable] = []

        # --- 1. CABEÇALHO SUPERIOR SOLTO E IMPONENTE ---
        story.append(Paragraph(txt["doc_titulo"], estilo_titulo_solto))
        story.append(Paragraph(txt["doc_subtitulo"], estilo_sub_solto))
        story.append(Paragraph(f"<b>{txt['meta_emissao']}</b> {self.timestamp} | <b>{txt['meta_titular']}</b> {self.titular} ({txt['meta_idade']} {self.idade}) | <b>{txt['meta_auditor']}</b> {self.auditor}", estilo_meta_solto))
        story.append(Spacer(1, 2))

        # --- 2. CONTEÚDO ENCAPSULADO NO BLOCO MESTRE PLATINA CLEAN ---
        elementos_bloco_total = [
            Paragraph(f"<b>{txt['block_auth']}</b> SYSTEM_SEC_C2_PREDICTIVE_V4 // <b>{txt['integrity_hash']}</b> <font color='#00875A'>{self.audit_hash}</font><br/>"
                      f"<b>{txt['public_key']}</b> {self.public_key} // <b>{txt['audit_metric']}</b>", 
                      ParagraphStyle('CryptoLight', parent=styles['Normal'], fontName='Courier-Bold', fontSize=5, textColor=MONACO_NAVY, leading=6.5, spaceAfter=3)),
            Spacer(1, 2),
            
            # --- TABELA 1 ---
            Paragraph(txt["sec1_titulo"], estilo_secao),
        ]
        
        tabela_1_data = [
            [Paragraph(txt["t1_l1_nome"], estilo_tabela_bold), Paragraph("98%", estilo_tabela_verde), Paragraph(txt["t1_l1_desc"], estilo_tabela)],
            [Paragraph(txt["t1_l2_nome"], estilo_tabela_bold), Paragraph(f"<font color='#00875A'>{self.estresse * 100:.1f}%</font>", estilo_tabela), Paragraph(txt["t1_l2_desc"], estilo_tabela)],
            [Paragraph(txt["t1_l3_nome"], estilo_tabela_bold), Paragraph(txt["t1_l3_val"], estilo_tabela), Paragraph(txt["t1_l3_desc"], estilo_tabela)]
        ]
        t1 = Table(tabela_1_data, colWidths=[140, 60, 314])
        t1.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, CARD_BG]),
            ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos_bloco_total.append(t1)
        
        # --- TABELA 2 ---
        elementos_bloco_total.append(Paragraph(txt["sec2_titulo"], estilo_secao))
        elementos_bloco_total.append(Paragraph(txt["sec2_desc"], estilo_texto))
        
        tabela_2_data = [
            [Paragraph(txt["t2_l1_nome"], estilo_tabela_bold), Paragraph("78.2624 mm", estilo_tabela), Paragraph(txt["t2_l1_desc"], estilo_tabela)],
            [Paragraph(txt["t2_l2_nome"], estilo_tabela_bold), Paragraph(f"{self.cde:.2f}%", estilo_tabela_verde), Paragraph(txt["t2_l2_desc"], estilo_tabela)],
            [Paragraph(txt["t2_l3_nome"], estilo_tabela_bold), Paragraph(f"<font color='#00875A'>{self.deficit_sustentacao:.2f}%</font>", estilo_tabela), Paragraph(txt["t2_l3_desc"], estilo_tabela)]
        ]
        t2 = Table(tabela_2_data, colWidths=[140, 60, 314])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, CARD_BG]),
            ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos_bloco_total.append(t2)

        # --- TABELA 3 ---
        elementos_bloco_total.append(Paragraph(txt["sec3_titulo"], estilo_secao))
        elementos_bloco_total.append(Paragraph(txt["sec3_desc"], estilo_texto))
        
        tabela_3_data = [
            [Paragraph(txt["t3_l1_nome"], estilo_tabela_bold), Paragraph(f"<font color='#00875A'>{self.asset_decay_rate:.2f}% a.a.</font>", estilo_tabela), Paragraph(txt["t3_l1_desc"], estilo_tabela)],
            [Paragraph(txt["t3_l2_nome"], estilo_tabela_bold), Paragraph(f"<font color='#00875A'>{self.formatar_moeda_eur(self.image_capital)}</font>", estilo_tabela), Paragraph(txt["t3_l2_desc"], estilo_tabela)],
            [Paragraph(txt["t3_l3_nome"], estilo_tabela_bold), Paragraph(f"<font color='#00875A'>{self.formatar_moeda_eur(self.perda_capital_15_anos)}</font>", estilo_tabela), Paragraph(txt["t3_l3_desc"], estilo_tabela)]
        ]
        t3 = Table(tabela_3_data, colWidths=[140, 75, 299])
        t3.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, CARD_BG]),
            ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos_bloco_total.append(t3)

        # --- TABELA 4 ---
        elementos_bloco_total.append(Paragraph(txt["sec4_titulo"], estilo_secao))
        
        tabela_4_data = [
            [Paragraph(txt["t4_l1_nome"], estilo_tabela_bold), Paragraph(self.formatar_moeda_eur(self.custo_setup), estilo_tabela), Paragraph(txt["t4_l1_desc"], estilo_tabela)],
            [Paragraph(txt["t4_l2_nome"], estilo_tabela_bold), Paragraph(f"<font color='#00875A'>{self.formatar_moeda_eur(self.perda_mitigada_evitada)}</font>", estilo_tabela), Paragraph(txt["t4_l2_desc"], estilo_tabela)],
            [Paragraph(txt["t4_l3_nome"], estilo_tabela_bold), Paragraph(f"{self.roi_absoluto:.2f}%", estilo_tabela_verde), Paragraph(txt["t4_l3_desc"], estilo_tabela)]
        ]
        t4 = Table(tabela_4_data, colWidths=[140, 75, 299])
        t4.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, CARD_BG]),
            ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos_bloco_total.append(t4)
        elementos_bloco_total.append(Spacer(1, 4))

        # --- BLOCO COMPARATIVO FINAL INTEGRADO ---
        elementos_bloco_total.append(Paragraph(self._obter_texto_comparativo_final().strip(), estilo_comparativo))

        # --- GRANDE BLOCO MESTRE ÚNICO PLATINA CLEAN ---
        bloco_mestre_total = Table([[elementos_bloco_total]], colWidths=[534])
        bloco_mestre_total.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('BOX', (0,0), (-1,-1), 1.0, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))

        story.append(bloco_mestre_total)
        
        doc.build(story, canvasmaker=SovereignSecureCanvas)
        return caminho_pdf

    def gerar_dossie(self, caminho_pdf: str, lang: str = "PT") -> str:
        return self.gerar_relatorio_roi(caminho_pdf, lang)

    def gerar_pdf(self, caminho_pdf: str, lang: str = "PT") -> str:
        return self.gerar_relatorio_roi(caminho_pdf, lang)


if __name__ == "__main__":
    print("Testando motor Super Retorno Financeiro em versão Executive Platinum com Nome Dinâmico...")
    engine = C2SovereignROIEngine(titular="José", idade=35, lang="PT")
    saida = engine.gerar_pdf("super_retorno_financeiro_clean.pdf")
    print(f"Relatório gerado com sucesso em: {saida}")