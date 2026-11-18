# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the 
intellectual property of Thierry Technology Concept Global. Unauthorized 
distribution, reverse engineering, or usage without a signed NDA/License 
agreement is strictly prohibited under international copyright frameworks.
===========================================================================
"""

"""
Módulo: super_retorno_financeiro.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Versão: 6.8.6 - MONACO EXECUTIVE PLATINUM EDITION (Alinhamento Geométrico Perfeito)
Descrição: Motor de Alta Performance de Auditoria Preditiva e Valuation de Ativos Biométricos.
           Aplica Geometria Diferencial, Amortização Exponencial e Bloco Mestre Platina Clean.
"""

import os
import datetime
import hashlib
import math
from reportlab.lib.pagesizes import A4
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
# DICIONÁRIO DE TRADUÇÕES BILINGUE (PT / EN) - TÓPICOS 1 A 8
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
        
        "sec1_titulo": "1. INPUTS DE TELEMETRIA FISIOLÓGICA E FADIGA (REAL-TIME C2)",
        "t1_l1_nome": "Score de Fadiga CDE (Sensor)",
        "t1_l1_desc": "Índice dinâmico acoplado à cronobiologia, temperatura e micro-movimentos faciais.",
        "t1_l2_nome": "Modulador Circadiano / Estresse",
        "t1_l2_desc": "Fator multiplicador exógeno extraído diretamente do motor de fadiga Tier-1.",
        "t1_l3_nome": "Condições Ambientais (Temp / UR)",
        "t1_l3_desc": "Telemetria térmica e higrométrica recolhida em tempo real pelo ecossistema.",
        
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
        "t4_l3_desc": "Retorno financeiro líquido gerado pela preservação soberana do capital de imagem.",

        "sec5_titulo": "5. ANÁLISE DE SENSIBILIDADE E TESTE DE ESTRESSE PATRIMONIAL (STOCHASTIC RISK)",
        "sec5_desc": "Simulação algorítmica em tempo real da volatilidade do capital de imagem sob vetores de estresse circadiano.",
        "t5_l1_nome": "Cenário Amortecido (Blindagem C2)",
        "t5_l1_desc": "Preservação máxima de ativos intangíveis decorrente da estabilização celular imediata.",
        "t5_l2_nome": "Cenário Projetado (Caso Base)",
        "t5_l2_desc": "Erosão patrimonial padrão calculada com base na telemetria atual.",
        "t5_l3_nome": "Estresse Crítico (Colapso Biológico)",
        "t5_l3_desc": "Degradação severa e acelerada por privação de sono e pico inflamatório de cortisol.",

        "sec6_titulo": "6. DIRETIVAS DE GOVERNANÇA INTEGRADA E CRONOGRAMA DE ALOCAÇÃO TIER-1",
        "sec6_desc": "Valores de ativação imediata para retenção de valor reputacional e mitigação de perdas atuarial.",
        "t6_l1_nome": "Módulo I: Calibração Circadiana Base",
        "t6_l1_desc": "Estabilização inicial dos vetores de ptose e fadiga microvascular em tempo real.",
        "t6_l2_nome": "Módulo II: Blindagem Ativa Platinum",
        "t6_l2_desc": "Protocolo Premium de engenharia celular profunda e otimização mitocondrial Tier-1.",
        "t6_l3_nome": "Módulo III: Governança Perpétua C2",
        "t6_l3_desc": "Monitoramento computacional contínuo 24/7 com proteção algorítmica de integridade.",

        "sec7_titulo": "7. ANCORAGEM DE SEGURANÇA E GARANTIAS ATUARIAIS (SLAS)",
        "sec7_desc": "Níveis de serviço garantidos contratualmente para preservação da estabilidade biométrica.",
        "t7_l1_nome": "SLA de Retenção Estrutural",
        "t7_l1_desc": "Garantia matemática de ancoragem elástica e prevenção de ptose avançada.",
        "t7_l2_nome": "Valor Total Assegurado (15 Anos)",
        "t7_l2_desc": "Montante global sob apólice preditiva soberana Tier-1.",
        "t7_l3_nome": "Indedutível de Criptografia PQC",
        "t7_l3_desc": "Segurança de dados e imutabilidade de registros em padrão pós-quântico.",

        "sec8_titulo": "8. PRÓXIMOS PASSOS E CALL TO ACTION OPERACIONAL",
        "sec8_desc": "Diretrizes imediatas para ativação do protocolo executivo UHNW.",
        "t8_l1_nome": "Homologação de Identidade C2",
        "t8_l1_desc": "Confirmação de credenciais soberanas e liberação de acesso ao dashboard.",
        "t8_l2_nome": "Setup da Infraestrutura Local",
        "t8_l2_desc": "Instalamento dos módulos offline e calibragem de sensores térmicos.",
        "t8_l3_nome": "Ratificação Executiva",
        "t8_l3_desc": "Assinatura digital e início imediato do monitoramento 24/7."
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
        
        "sec1_titulo": "1. PHYSIOLOGICAL TELEMETRY & FATIGUE INPUTS (REAL-TIME C2)",
        "t1_l1_nome": "CDE Fatigue Score (Sensor)",
        "t1_l1_desc": "Dynamic index coupled with chronobiology, temperature, and facial micro-movements.",
        "t1_l2_nome": "Circadian Modulator / Stress",
        "t1_l2_desc": "Exogenous multiplying factor extracted directly from the Tier-1 fatigue engine.",
        "t1_l3_nome": "Environmental Conditions (Temp / RH)",
        "t1_l3_desc": "Thermal and hygrometric telemetry collected in real time by the ecosystem.",
        
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
        "t4_l3_desc": "Net financial return generated by the sovereign preservation of image capital.",

        "sec5_titulo": "5. SENSITIVITY ANALYSIS & PATRIMONIAL STRESS TESTING (STOCHASTIC RISK)",
        "sec5_desc": "Real-time algorithmic simulation of image capital volatility under circadian stress vectors.",
        "t5_l1_nome": "Buffered Scenario (C2 Shielding)",
        "t5_l1_desc": "Maximum preservation of intangible assets resulting from immediate cellular stabilization.",
        "t5_l2_nome": "Projected Scenario (Base Case)",
        "t5_l2_desc": "Standard asset erosion computed based on current telemetry data.",
        "t5_l3_nome": "Critical Stress (Biological Collapse)",
        "t5_l3_desc": "Severe accelerated degradation driven by sleep deprivation and cortisol inflammatory peaks.",

        "sec6_titulo": "6. INTEGRATED GOVERNANCE DIRECTIVES & TIER-1 ALLOCATION SCHEDULE",
        "sec6_desc": "Immediate activation values for reputational asset retention and actuarial loss mitigation.",
        "t6_l1_nome": "Module I: Base Circadian Calibration",
        "t6_l1_desc": "Initial stabilization of ptosis vectors and microvascular fatigue in real time.",
        "t6_l2_nome": "Module II: Active Platinum Shielding",
        "t6_l2_desc": "Premium deep cellular engineering protocol and Tier-1 mitochondrial optimization.",
        "t6_l3_nome": "Module III: Perpetual C2 Governance",
        "t6_l3_desc": "Continuous 24/7 computational monitoring with cryptographic integrity protection.",

        "sec7_titulo": "7. SECURITY ANCHORING & ACTUARIAL GUARANTEES (SLAS)",
        "sec7_desc": "Contractually guaranteed service levels for biometric stability preservation.",
        "t7_l1_nome": "Structural Retention SLA",
        "t7_l1_desc": "Mathematical guarantee of elastic anchoring and advanced ptosis prevention.",
        "t7_l2_nome": "Total Insured Value (15 Years)",
        "t7_l2_desc": "Global amount under Tier-1 sovereign predictive policy.",
        "t7_l3_nome": "PQC Cryptography Indeductible",
        "t7_l3_desc": "Data security and record immutability in post-quantum standard.",

        "sec8_titulo": "8. PRÓXIMOS PASSOS E CALL TO ACTION OPERACIONAL",
        "sec8_desc": "Immediate guidelines for activating the UHNW executive protocol.",
        "t8_l1_nome": "C2 Identity Homologation",
        "t8_l1_desc": "Confirmation of sovereign credentials and dashboard access release.",
        "t8_l2_nome": "Setup da Infraestrutura Local",
        "t8_l2_desc": "Installation of offline modules and thermal sensor calibration.",
        "t8_l3_nome": "Executive Ratification",
        "t8_l3_desc": "Digital signature and immediate start of 24/7 monitoring."
    }
}


class SovereignSecureCanvas(canvas.Canvas):
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
    def __init__(self, 
                 chave_publica_sistema: str = "TTC-KEY-MONACO-SECURE-9948", 
                 titular: Optional[str] = None, 
                 idade: int = 35, 
                 patrimonio_liquido_eur: float = 1000000.0, 
                 fator_estresse_biologico: Optional[float] = None, 
                 custo_setup_estrutura_eur: float = 75000.0,
                 auditor_lider: str = "THIERRY TCC",
                 market_segment: str = "Tecnologia e Inovação",
                 horizon_years: int = 10,
                 telemetria: Optional[dict] = None,
                 lang: str = "PT"):
        
        self.telemetria_externa = telemetria or {}
        
        resolvedor_nome = titular or self.telemetria_externa.get('nome_cliente') or self.telemetria_externa.get('nome') or memoria.ler_dados("nome_cliente") or memoria.ler_dados("titular") or "CLIENTE UHNW"
        self.titular = resolvedor_nome.upper()
        
        self.auditor = auditor_lider.upper()
        self.public_key = chave_publica_sistema
        self.idade = idade
        self.net_worth = patrimonio_liquido_eur
        self.custo_setup = custo_setup_estrutura_eur
        self.market_segment = market_segment
        self.horizon_years = horizon_years
        self.lang = lang.upper() if lang and isinstance(lang, str) else "PT"
        if self.lang not in TEXTOS_ROI:
            self.lang = "PT"
            
        dados_fadiga_memoria = memoria.ler_dados("dados_fadiga") or memoria.ler_dados(f"historico_fadiga_{self.titular}") or {}
        
        if fator_estresse_biologico is not None:
            self.estresse = min(1.0, max(0.0, fator_estresse_biologico))
            self.score_fadiga_sensor = dados_fadiga_memoria.get("score_fadiga", self.estresse * 100.0)
            self.fator_circadiano = dados_fadiga_memoria.get("fator_circadiano", 1.0)
        else:
            score_sensor = dados_fadiga_memoria.get("score_fadiga", 25.0)
            self.score_fadiga_sensor = score_sensor
            self.estresse = min(1.0, max(0.0, score_sensor / 100.0))
            self.fator_circadiano = dados_fadiga_memoria.get("fator_circadiano", 1.0)
            
        self.temp_ambiente = dados_fadiga_memoria.get("clima_referencia", {}).get("temp", 27.0)
        self.umi_ambiente = dados_fadiga_memoria.get("clima_referencia", {}).get("umi", 60.0)
        self.hash_fadiga_sensor = dados_fadiga_memoria.get("integrity_hash", "PENDING-SYNC")

        self.timestamp = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S UTC")
        
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
        if self.lang == "EN":
            return f"""
            <b>Comparative Executive Audit Summary ({self.titular}):</b> Integrating real-time biometric fatigue telemetry (Score: {self.score_fadiga_sensor:.1f}%, Circadian Factor: {self.fator_circadiano}x) and complete Tier-1 governance, the compliance framework deployed for <i>{self.titular}</i> secures multi-faceted capital preservation across <i>{self.market_segment}</i>, guaranteeing absolute market dominance.
            """
        else:
            return f"""
            <b>Síntese Comparativa de Auditoria Executiva ({self.titular}):</b> Integrando a telemetria de fadiga em tempo real (Score: {self.score_fadiga_sensor:.1f}%, Fator Circadiano: {self.fator_circadiano}x) e a governança Tier-1 completa, o modelo aplicado a <i>{self.titular}</i> assegura uma blindagem patrimonial sem precedentes no setor de <i>{self.market_segment}</i>, consolidando liderança perpétua.
            """

    def gerar_relatorio_roi(self, caminho_pdf: str, lang: str = "PT") -> str:
        if lang:
            self.lang = lang.upper()
            if self.lang not in TEXTOS_ROI:
                self.lang = "PT"

        txt = TEXTOS_ROI[self.lang]
        
        # Margens otimizadas de 45pt para dar folga exata na folha A4
        doc = SimpleDocTemplate(
            caminho_pdf,
            pagesize=A4,
            rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45
        )
        
        styles = getSampleStyleSheet()
        
        MONACO_NAVY = colors.HexColor('#0A1128')
        SOVEREIGN_GOLD = colors.HexColor('#B8860B')   
        EXCELENCIA_VERDE = colors.HexColor('#00875A') 
        DARK_TEXT = colors.HexColor('#1E293B')        
        CARD_BG = colors.HexColor('#F8FAFC')          
        CARD_BORDER = colors.HexColor('#CBD5E1')      
        TABLE_HEADER_BG = colors.HexColor('#F1F5F9')  
        
        estilo_titulo_solto = ParagraphStyle('MaxTitleSolto', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=12, leading=14, textColor=MONACO_NAVY, alignment=1, spaceAfter=2)
        estilo_sub_solto = ParagraphStyle('MaxSubSolto', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=SOVEREIGN_GOLD, alignment=1, spaceAfter=2)
        estilo_meta_solto = ParagraphStyle('MaxMetaSolto', parent=styles['Normal'], fontName='Helvetica', fontSize=6.5, leading=8.5, textColor=colors.HexColor('#333333'), alignment=1, spaceAfter=4)
        
        estilo_secao = ParagraphStyle('MaxSec', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=7, textColor=MONACO_NAVY, spaceBefore=3, spaceAfter=2)
        estilo_texto = ParagraphStyle('MaxText', parent=styles['Normal'], fontName='Helvetica', fontSize=5.5, leading=7.5, textColor=DARK_TEXT, spaceAfter=2)
        
        # Estilos de texto com fonte reduzida cirurgicamente para não estourar as caixas
        estilo_tabela = ParagraphStyle('MaxTab', parent=styles['Normal'], fontName='Helvetica', fontSize=4.8, textColor=DARK_TEXT, leading=6.5)
        estilo_tabela_bold = ParagraphStyle('MaxTabBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=4.8, textColor=MONACO_NAVY, leading=6.5)
        estilo_tabela_verde = ParagraphStyle('MaxTabGreen', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=4.8, textColor=EXCELENCIA_VERDE, leading=6.5)
        estilo_comparativo = ParagraphStyle('MaxComp', parent=styles['Normal'], fontName='Helvetica', fontSize=5.8, textColor=DARK_TEXT, leading=8, spaceBefore=3, spaceAfter=2)

        story: List[Flowable] = []

        story.append(Paragraph(txt["doc_titulo"], estilo_titulo_solto))
        story.append(Paragraph(txt["doc_subtitulo"], estilo_sub_solto))
        story.append(Paragraph(f"<b>{txt['meta_emissao']}</b> {self.timestamp} | <b>{txt['meta_titular']}</b> {self.titular} ({txt['meta_idade']} {self.idade}) | <b>{txt['meta_auditor']}</b> {self.auditor}", estilo_meta_solto))
        story.append(Spacer(1, 2))

        elementos_bloco_total = [
            Paragraph(f"<b>{txt['block_auth']}</b> SYSTEM_SEC_C2_PREDICTIVE_V4 // <b>{txt['integrity_hash']}</b> <font color='#00875A'>{self.audit_hash}</font><br/>"
                      f"<b>{txt['public_key']}</b> {self.public_key} // <b>Sensor Hash:</b> {self.hash_fadiga_sensor[:16]}...", 
                      ParagraphStyle('CryptoLight', parent=styles['Normal'], fontName='Courier-Bold', fontSize=4.5, textColor=MONACO_NAVY, leading=6, spaceAfter=2)),
            Spacer(1, 2),
            
            Paragraph(txt["sec1_titulo"], estilo_secao),
        ]
        
        # LARGURAS GEOMETRICAMENTE CALIBRADAS: 120 + 75 + 285 = 480 pt (Encaixe perfeito na caixa de 485 pt)
        COL_W1, COL_W2, COL_W3 = 120, 75, 285

        tabela_1_data = [
            [Paragraph(txt["t1_l1_nome"], estilo_tabela_bold), Paragraph(f"{self.score_fadiga_sensor:.1f}%", estilo_tabela_verde), Paragraph(txt["t1_l1_desc"], estilo_tabela)],
            [Paragraph(txt["t1_l2_nome"], estilo_tabela_bold), Paragraph(f"{self.fator_circadiano}x (Estresse: {self.estresse*100:.1f}%)", estilo_tabela), Paragraph(txt["t1_l2_desc"], estilo_tabela)],
            [Paragraph(txt["t1_l3_nome"], estilo_tabela_bold), Paragraph(f"{self.temp_ambiente}°C | UR {self.umi_ambiente}%", estilo_tabela), Paragraph(txt["t1_l3_desc"], estilo_tabela)]
        ]
        t1 = Table(tabela_1_data, colWidths=[COL_W1, COL_W2, COL_W3])
        t1.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, CARD_BG]),
            ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2.0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
            ('LEFTPADDING', (0,0), (-1,-1), 4.0),
            ('RIGHTPADDING', (0,0), (-1,-1), 4.0),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos_bloco_total.append(t1)
        
        elementos_bloco_total.append(Paragraph(txt["sec2_titulo"], estilo_secao))
        elementos_bloco_total.append(Paragraph(txt["sec2_desc"], estilo_texto))
        
        tabela_2_data = [
            [Paragraph(txt["t2_l1_nome"], estilo_tabela_bold), Paragraph("78.2624 mm", estilo_tabela), Paragraph(txt["t2_l1_desc"], estilo_tabela)],
            [Paragraph(txt["t2_l2_nome"], estilo_tabela_bold), Paragraph(f"{self.cde:.2f}%", estilo_tabela_verde), Paragraph(txt["t2_l2_desc"], estilo_tabela)],
            [Paragraph(txt["t2_l3_nome"], estilo_tabela_bold), Paragraph(f"<font color='#00875A'>{self.deficit_sustentacao:.2f}%</font>", estilo_tabela), Paragraph(txt["t2_l3_desc"], estilo_tabela)]
        ]
        t2 = Table(tabela_2_data, colWidths=[COL_W1, COL_W2, COL_W3])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, CARD_BG]),
            ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2.0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
            ('LEFTPADDING', (0,0), (-1,-1), 4.0),
            ('RIGHTPADDING', (0,0), (-1,-1), 4.0),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos_bloco_total.append(t2)

        elementos_bloco_total.append(Paragraph(txt["sec3_titulo"], estilo_secao))
        elementos_bloco_total.append(Paragraph(txt["sec3_desc"], estilo_texto))
        
        tabela_3_data = [
            [Paragraph(txt["t3_l1_nome"], estilo_tabela_bold), Paragraph(f"<font color='#00875A'>{self.asset_decay_rate:.2f}% a.a.</font>", estilo_tabela), Paragraph(txt["t3_l1_desc"], estilo_tabela)],
            [Paragraph(txt["t3_l2_nome"], estilo_tabela_bold), Paragraph(f"<font color='#00875A'>{self.formatar_moeda_eur(self.image_capital)}</font>", estilo_tabela), Paragraph(txt["t3_l2_desc"], estilo_tabela)],
            [Paragraph(txt["t3_l3_nome"], estilo_tabela_bold), Paragraph(f"<font color='#00875A'>{self.formatar_moeda_eur(self.perda_capital_15_anos)}</font>", estilo_tabela), Paragraph(txt["t3_l3_desc"], estilo_tabela)]
        ]
        t3 = Table(tabela_3_data, colWidths=[COL_W1, COL_W2, COL_W3])
        t3.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, CARD_BG]),
            ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2.0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
            ('LEFTPADDING', (0,0), (-1,-1), 4.0),
            ('RIGHTPADDING', (0,0), (-1,-1), 4.0),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos_bloco_total.append(t3)

        elementos_bloco_total.append(Paragraph(txt["sec4_titulo"], estilo_secao))
        
        tabela_4_data = [
            [Paragraph(txt["t4_l1_nome"], estilo_tabela_bold), Paragraph(self.formatar_moeda_eur(self.custo_setup), estilo_tabela), Paragraph(txt["t4_l1_desc"], estilo_tabela)],
            [Paragraph(txt["t4_l2_nome"], estilo_tabela_bold), Paragraph(f"<font color='#00875A'>{self.formatar_moeda_eur(self.perda_mitigada_evitada)}</font>", estilo_tabela), Paragraph(txt["t4_l2_desc"], estilo_tabela)],
            [Paragraph(txt["t4_l3_nome"], estilo_tabela_bold), Paragraph(f"{self.roi_absoluto:.2f}%", estilo_tabela_verde), Paragraph(txt["t4_l3_desc"], estilo_tabela)]
        ]
        t4 = Table(tabela_4_data, colWidths=[COL_W1, COL_W2, COL_W3])
        t4.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, CARD_BG]),
            ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2.0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
            ('LEFTPADDING', (0,0), (-1,-1), 4.0),
            ('RIGHTPADDING', (0,0), (-1,-1), 4.0),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos_bloco_total.append(t4)

        elementos_bloco_total.append(Paragraph(txt["sec5_titulo"], estilo_secao))
        elementos_bloco_total.append(Paragraph(txt["sec5_desc"], estilo_texto))
        
        tabela_5_data = [
            [Paragraph(txt["t5_l1_nome"], estilo_tabela_bold), Paragraph(f"<font color='#00875A'>Perda Reduzida (8%)</font>", estilo_tabela_verde), Paragraph(txt["t5_l1_desc"], estilo_tabela)],
            [Paragraph(txt["t5_l2_nome"], estilo_tabela_bold), Paragraph(f"Perda Projetada (40%)", estilo_tabela), Paragraph(txt["t5_l2_desc"], estilo_tabela)],
            [Paragraph(txt["t5_l3_nome"], estilo_tabela_bold), Paragraph(f"<font color='#C0392B'>Colapso Severo (75%)</font>", estilo_tabela), Paragraph(txt["t5_l3_desc"], estilo_tabela)]
        ]
        t5 = Table(tabela_5_data, colWidths=[COL_W1, COL_W2, COL_W3])
        t5.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, CARD_BG]),
            ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2.0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
            ('LEFTPADDING', (0,0), (-1,-1), 4.0),
            ('RIGHTPADDING', (0,0), (-1,-1), 4.0),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos_bloco_total.append(t5)

        elementos_bloco_total.append(Paragraph(txt["sec6_titulo"], estilo_secao))
        elementos_bloco_total.append(Paragraph(txt["sec6_desc"], estilo_texto))
        
        tabela_6_data = [
            [Paragraph(txt["t6_l1_nome"], estilo_tabela_bold), Paragraph("€ 25.000,00", estilo_tabela), Paragraph(txt["t6_l1_desc"], estilo_tabela)],
            [Paragraph(txt["t6_l2_nome"], estilo_tabela_bold), Paragraph(self.formatar_moeda_eur(self.custo_setup), estilo_tabela_verde), Paragraph(txt["t6_l2_desc"], estilo_tabela)],
            [Paragraph(txt["t6_l3_nome"], estilo_tabela_bold), Paragraph("€ 12.500,00 / a.a.", estilo_tabela), Paragraph(txt["t6_l3_desc"], estilo_tabela)]
        ]
        t6 = Table(tabela_6_data, colWidths=[COL_W1, COL_W2, COL_W3])
        t6.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, CARD_BG]),
            ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2.0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
            ('LEFTPADDING', (0,0), (-1,-1), 4.0),
            ('RIGHTPADDING', (0,0), (-1,-1), 4.0),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos_bloco_total.append(t6)

        sla_retencao = max(85.0, 100.0 - (self.deficit_sustentacao * 0.15))
        valor_total_protegido = self.perda_mitigada_evitada

        elementos_bloco_total.append(Paragraph(txt["sec7_titulo"], estilo_secao))
        tabela_7_data = [
            [Paragraph(txt["t7_l1_nome"], estilo_tabela_bold), Paragraph(f"{sla_retencao:.2f}% SLA", estilo_tabela_verde), Paragraph(txt["t7_l1_desc"], estilo_tabela)],
            [Paragraph(txt["t7_l2_nome"], estilo_tabela_bold), Paragraph(self.formatar_moeda_eur(valor_total_protegido), estilo_tabela), Paragraph(txt["t7_l2_desc"], estilo_tabela)],
            [Paragraph(txt["t7_l3_nome"], estilo_tabela_bold), Paragraph("99.9999%", estilo_tabela), Paragraph(txt["t7_l3_desc"], estilo_tabela)]
        ]
        t7 = Table(tabela_7_data, colWidths=[COL_W1, COL_W2, COL_W3])
        t7.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, CARD_BG]),
            ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2.0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
            ('LEFTPADDING', (0,0), (-1,-1), 4.0),
            ('RIGHTPADDING', (0,0), (-1,-1), 4.0),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos_bloco_total.append(t7)

        elementos_bloco_total.append(Paragraph(txt["sec8_titulo"], estilo_secao))
        tabela_8_data = [
            [Paragraph(txt["t8_l1_nome"], estilo_tabela_bold), Paragraph("Imediato", estilo_tabela), Paragraph(txt["t8_l1_desc"], estilo_tabela)],
            [Paragraph(txt["t8_l2_nome"], estilo_tabela_bold), Paragraph("D+1 Técnico", estilo_tabela), Paragraph(txt["t8_l2_desc"], estilo_tabela)],
            [Paragraph(txt["t8_l3_nome"], estilo_tabela_bold), Paragraph("Aprovação", estilo_tabela_verde), Paragraph(txt["t8_l3_desc"], estilo_tabela)]
        ]
        t8 = Table(tabela_8_data, colWidths=[COL_W1, COL_W2, COL_W3])
        t8.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, CARD_BG]),
            ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2.0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
            ('LEFTPADDING', (0,0), (-1,-1), 4.0),
            ('RIGHTPADDING', (0,0), (-1,-1), 4.0),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos_bloco_total.append(t8)
        elementos_bloco_total.append(Spacer(1, 3))

        elementos_bloco_total.append(Paragraph(self._obter_texto_comparativo_final().strip(), estilo_comparativo))

        # BLOCO MESTRE TOTAL COM LARGURA EXATA DE 485 pt (Alinhado com as margens de 45pt da página A4)
        bloco_mestre_total = Table([[elementos_bloco_total]], colWidths=[485])
        bloco_mestre_total.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('BOX', (0,0), (-1,-1), 1.0, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))

        story.append(bloco_mestre_total)
        
        doc.build(story, canvasmaker=SovereignSecureCanvas)
        return caminho_pdf

    def gerar_dossie(self, caminho_pdf: str, lang: str = "PT") -> str:
        return self.gerar_relatorio_roi(caminho_pdf, lang)

    def gerar_pdf(self, caminho_pdf: str, lang: str = "PT") -> str:
        return self.gerar_relatorio_roi(caminho_pdf, lang)


if __name__ == "__main__":
    print("Testando motor Super Retorno Financeiro com Tópicos 1 a 8 integrados perfeitamente...")
    engine = C2SovereignROIEngine(lang="PT")
    saida = engine.gerar_pdf("super_retorno_financeiro_clean.pdf")
    print(f"Relatório gerado com sucesso em: {saida}")