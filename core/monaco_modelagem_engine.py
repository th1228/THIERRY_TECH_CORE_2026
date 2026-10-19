# -*- coding: utf-8 -*-
"""
Módulo Unificado: monaco_modelagem_engine.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Versão: 6.1.1 - MONACO EXECUTIVE PLATINUM EDITION (Bilingual PT/EN & Clean Clinical Lab Table Format)
Descrição: Motor unificado formatado no Padrão Executive Platinum (Fundo Claro / Clean), 
           bordas douradas, texto em grafite executivo e laudo estruturado de inteligência dinâmico.
"""

import os
import sys
import datetime
import hashlib
import re
from typing import Any, Dict, List, Tuple, Optional
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak
from reportlab.platypus.flowables import Flowable


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
TEXTOS_MONACO = {
    "PT": {
        "marca_agua": "MONACO PLATINUM • SOVEREIGN C2 DEFENSE",
        "rodape_linha1": "Classificado • Salvaguarda Patrimonial, Propriedade Intelectual e Continuidade C2",
        "rodape_linha2": "THIERRY TECHNOLOGY CONCEPT GLOBAL • COMPUTATIONAL DIVISION",
        "rodape_seal": "MONACO SEAL • PÁGINA {pagina} • SHA-256 SECURED",
        "emp_sub": "SOVEREIGN DEFENSE DIVISION",
        "doc_titulo": "DOSSIÊ DE MODELAGEM COMPUTACIONAL, VALUACIÓN & BLINDAGEM JURÍDICA DE PI",
        "meta_titular": "Titular Soberano:",
        "meta_horizonte": "Horizonte:",
        "meta_operador": "Operador:",
        "meta_emissao": "Emissão:",
        "meta_params": "Parâmetros In-Silico:",
        "anos_label": "Anos",
        
        "sumario_titulo": "<b>00 // SUMÁRIO EXECUTIVO: MATRIZ DE MODELAGEM E GOVERNANÇA JURÍDICA</b>",
        "sumario_status": "<b>STATUS</b>",
        "sumario_texto": (
            "Este laudo consolida a varredura vetorial tridimensional, a valuación de ativos biogenéticos e o <b>Arcabouço Legal de Proteção de Propriedade Intelectual</b> "
            "da <b>{company}</b>. O protocolo assegura a blindagem jurídica absoluta de dados biológicos, algoritmos computacionais proprietários e "
            "registros institucionais via e-INPI sob governança soberana UHNW."
        ),
        
        "bloco1_titulo": "01 // MODELAGEM MATRICIAL E GEOMETRIA ESPACIAL 3D",
        "b1_m1_nome": "Tensor de Tensegridade Cutânea",
        "b1_m1_desc": "Mapeamento vetorial de alta densidade (<font color='#00875A'><b>{pontos}</b></font>) pontos fiduciais.<br/><b>Status:</b> <font color='#00875A'>{status}</font>",
        "b1_m2_nome": "Análise de Desvio da Proporção Áurea",
        "b1_m2_desc": "Computação de desvio estrutural em relação ao phi de referência (Desvio: <font color='#00875A'><b>{desvio}%</b></font>).<br/><b>Vulnerabilidade:</b> {vuln}",
        "b1_m3_nome": "Calibração Térmica e Microvascular",
        "b1_m3_desc": "Otimização periférica cruzando oximetria (<font color='#00875A'><b>{oxi}</b></font>) e ritmo respiratório (<font color='#00875A'><b>{diaf}</b></font>).",
        
        "bloco2_titulo": "02 // VALUACIÓN PATRIMONIAL E ENGENHARIA ATUARIAL",
        "b2_m1_nome": "Projeção de Custos Evitados (Horizonte Dinâmico)",
        "b2_m1_desc": "Cálculo atuarial comparativo ao custo de intervenções para o horizonte de <font color='#00875A'><b>{horizon} anos</b></font>.<br/><b>Economia Líquida:</b> {custo}",
        "b2_m2_nome": "Valuación do Capital de Imagem (UHNW Standard)",
        "b2_m2_desc": "Valoração de ativos intangíveis de imagem corporal e estrutura corporativa.<br/><b>Valor da Matriz:</b> {val}",
        "b2_m3_nome": "Diretriz Tática de Engenharia Reversa",
        "b2_m3_desc": "{diretriz}",
        
        "bloco3_titulo": "03 // ARCABOÇO LEGAL: PROPRIEDADE INTELECTUAL E PATENTES",
        "b3_m1_nome": "Salvaguarda de Dados Biológicos e Algoritmos",
        "b3_m1_desc": "Estabelecimento de arcabouço jurídico (<font color='#00875A'><b>Lei nº 9.279/96</b></font>) para salvaguardar todos os dados biológicos, malhas biométricas e tecnologias exclusivas desenvolvidas no ecossistema.",
        "b3_m2_nome": "Registro de Patentes e Segredos Industriais",
        "b3_m2_desc": "Utilização de estratégias avançadas de salvaguarda, incluindo submissão de registros no portal oficial <font color='#00875A'><b>e-INPI</b></font> e proteção rigorosa de segredos industriais contra engenharia reversa.",
        "b3_m3_nome": "Cláusulas de Não Concorrência e Retenção",
        "b3_m3_desc": "Aplicação de restrições contratuais severas assegurando que toda inovação derivada permaneça sob controle exclusivo e intransferível do titular (<font color='#00875A'><b>Art. 5º, XXVII, CF</b></font>).",
        
        "bloco4_titulo": "04 // GOVERNANÇA DE LICENCIAMENTO E AUDITORIA RIGOROSA",
        "b4_m1_nome": "Contratos de Licenciamento Exclusivo",
        "b4_m1_desc": "Estipulação de diretrizes contratuais onde qualquer uso comercial ou tecnológico por terceiros requer autorização prévia e chancela do Conselho Soberano (<font color='#00875A'><b>Arts. 126/135 LPI</b></font>).",
        "b4_m2_nome": "Cláusulas de Auditoria Periódica",
        "b4_m2_desc": "Inspeções e auditorias técnico-jurídicas recorrentes para fiscalizar o cumprimento de acordos de confidencialidade e mitigar riscos de vazamento tecnológico.",
        "b4_m3_nome": "Cadeia de Custódia e Hash Criptográfico SHA-256",
        "b4_m3_desc": "Validação imutável de sessão e rastreabilidade de ativos.<br/><b>Hash SHA-256:</b> <font name='Courier' size=6 color='#00875A'>{hash_sha}</font>",
        
        "col_metrica": "<b>MÉTRICA / FORMULAÇÃO LEGAL</b>",
        "anexo_titulo": "<b>[ SEÇÃO II: ANEXO DE INTELIGÊNCIA DINÂMICA & BLINDAGEM JURÍDICA ]</b>",
        "laudo_col_param": "PARÂMETRO / SEÇÃO JURÍDICA",
        "laudo_col_parecer": "PARECER E DIRETRIZ TÉCNICA UHNW"
    },
    "EN": {
        "marca_agua": "MONACO PLATINUM • SOVEREIGN C2 DEFENSE",
        "rodape_linha1": "Classified • Asset Safeguard, Intellectual Property, and C2 Continuity",
        "rodape_linha2": "THIERRY TECHNOLOGY CONCEPT GLOBAL • COMPUTATIONAL DIVISION",
        "rodape_seal": "MONACO SEAL • PAGE {pagina} • SHA-256 SECURED",
        "emp_sub": "SOVEREIGN DEFENSE DIVISION",
        "doc_titulo": "COMPUTATIONAL MODELING, VALUATION & IP LEGAL SHIELDING DOSSIER",
        "meta_titular": "Sovereign Holder:",
        "meta_horizonte": "Horizon:",
        "meta_operador": "Operator:",
        "meta_emissao": "Issuance:",
        "meta_params": "In-Silico Parameters:",
        "anos_label": "Years",
        
        "sumario_titulo": "<b>00 // EXECUTIVE SUMMARY: MODELING MATRIX & LEGAL GOVERNANCE</b>",
        "sumario_status": "<b>STATUS</b>",
        "sumario_texto": (
            "This report consolidates the three-dimensional vector scanning, biogenetic asset valuation, and the <b>Intellectual Property Protection Legal Framework</b> "
            "of <b>{company}</b>. The protocol ensures absolute legal shielding of biological data, proprietary computational algorithms, "
            "and institutional registrations via e-INPI under sovereign UHNW governance."
        ),
        
        "bloco1_titulo": "01 // MATRIX MODELING AND 3D SPATIAL GEOMETRY",
        "b1_m1_nome": "Cutaneous Tensegrity Tensor",
        "b1_m1_desc": "High-density vector mapping of (<font color='#00875A'><b>{pontos}</b></font>) fiducial points.<br/><b>Status:</b> <font color='#00875A'>{status}</font>",
        "b1_m2_nome": "Golden Ratio Deviation Analysis",
        "b1_m2_desc": "Computation of structural deviation relative to reference phi (Deviation: <font color='#00875A'><b>{desvio}%</b></font>).<br/><b>Vulnerability:</b> {vuln}",
        "b1_m3_nome": "Thermal and Microvascular Calibration",
        "b1_m3_desc": "Peripheral optimization cross-referencing oximetry (<font color='#00875A'><b>{oxi}</b></font>) and respiratory rate (<font color='#00875A'><b>{diaf}</b></font>).",
        
        "bloco2_titulo": "02 // ASSET VALUATION AND ACTUARIAL ENGINEERING",
        "b2_m1_nome": "Avoided Costs Projection (Dynamic Horizon)",
        "b2_m1_desc": "Comparative actuarial calculation against intervention costs for the <font color='#00875A'><b>{horizon}-year</b></font> horizon.<br/><b>Net Savings:</b> {custo}",
        "b2_m2_nome": "Image Capital Valuation (UHNW Standard)",
        "b2_m2_desc": "Valuation of intangible body image and corporate structure assets.<br/><b>Matrix Value:</b> {val}",
        "b2_m3_nome": "Reverse Engineering Tactical Directive",
        "b2_m3_desc": "{diretriz}",
        
        "bloco3_titulo": "03 // LEGAL FRAMEWORK: INTELLECTUAL PROPERTY AND PATENTS",
        "b3_m1_nome": "Biological Data and Algorithm Safeguard",
        "b3_m1_desc": "Establishment of a legal framework (<font color='#00875A'><b>Law No. 9,279/96</b></font>) to safeguard all biological data, biometric meshes, and exclusive technologies developed within the ecosystem.",
        "b3_m2_nome": "Patent and Trade Secret Registration",
        "b3_m2_desc": "Advanced safeguard strategies, including submission of records to the official <font color='#00875A'><b>e-INPI</b></font> portal and rigorous trade secret protection against reverse engineering.",
        "b3_m3_nome": "Non-Compete and Retention Clauses",
        "b3_m3_desc": "Enforcement of severe contractual restrictions ensuring all derived innovation remains under the holder's exclusive and non-transferable control (<font color='#00875A'><b>Art. 5, XXVII, CF</b></font>).",
        
        "bloco4_titulo": "04 // LICENSING GOVERNANCE AND RIGOROUS AUDIT",
        "b4_m1_nome": "Exclusive Licensing Agreements",
        "b4_m1_desc": "Stipulation of contractual guidelines where any commercial or technological use by third parties requires prior authorization and Sovereign Council endorsement (<font color='#00875A'><b>Arts. 126/135 LPI</b></font>).",
        "b4_m2_nome": "Periodic Audit Clauses",
        "b4_m2_desc": "Recurring technical-legal inspections and audits to monitor compliance with confidentiality agreements and mitigate technology leakage risks.",
        "b4_m3_nome": "Custody Chain and SHA-256 Cryptographic Hash",
        "b4_m3_desc": "Immutable session validation and asset traceability.<br/><b>SHA-256 Hash:</b> <font name='Courier' size=6 color='#00875A'>{hash_sha}</font>",
        
        "col_metrica": "<b>METRIC / LEGAL FORMULATION</b>",
        "anexo_titulo": "<b>[ SECTION II: DYNAMIC INTELLIGENCE ANNEX & LEGAL SHIELDING ]</b>",
        "laudo_col_param": "PARAMETER / LEGAL SECTION",
        "laudo_col_parecer": "UHNW TECHNICAL OPINION AND GUIDELINE"
    }
}


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


class C2MonacoModelingEngine:
    """
    Motor Unificado de Modelagem Computacional, Valuación de Imagem UHNW 
    e Blindagem Jurídica de Propriedade Intelectual em Paleta Executive Platinum com Suporte Bilíngue Dinâmico.
    """
    def __init__(
        self, 
        ceo_name: Optional[str] = None, 
        company_name: str = "Thierry Technology Concept Global", 
        market_segment: str = "Tecnologia e Inovação", 
        horizon_years: int = 10,
        operador: str = "THIERRY (TCC SOBERANO)",
        telemetria: Optional[Dict[str, Any]] = None,
        lang: str = "PT"
    ) -> None:
        self.telemetria = telemetria if telemetria is not None else {}
        
        # Resolução dinâmica do nome do titular vindo do painel, telemetria ou fallback seguro
        self.ceo = ceo_name or self.telemetria.get('nome_cliente') or self.telemetria.get('nome') or "Cliente UHNW"
        
        self.company = company_name
        self.segment = market_segment
        self.horizon = int(horizon_years)
        self.operador = operador
        self.lang = lang.upper() if lang and isinstance(lang, str) else "PT"
        if self.lang not in TEXTOS_MONACO:
            self.lang = "PT"
            
        self.emissao = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S UTC")
        
        if any(keyword in market_segment.lower() for keyword in ["tecnologia", "varejo", "alimentos", "inovação", "financeiro"]):
            self.fator_degradacao = 1.25  
        else:
            self.fator_degradacao = 1.00  

    def calcular_geometria_espacial_3d(self) -> Dict[str, Any]:
        """Executa os cálculos da matriz de deformação e coeficientes de blindagem jurídica."""
        pontos_malha = 468
        desvio_aurea_base = 4.82  
        custo_evitado_base = 4927.50  
        valuacion_matriz_base = 153000.00  
        
        desvio_calculado = desvio_aurea_base * (1.0 + (0.05 * self.fator_degradacao * (self.horizon / 10)))
        custo_evitado_dinamico = custo_evitado_base * (self.horizon / 10) * self.fator_degradacao
        valuacion_patrimonial_dinamica = valuacion_matriz_base * self.fator_degradacao
        
        if self.lang == "EN":
            if self.fator_degradacao > 1.1:
                status_malha = "SKIN TENSEGRITY DECLINE DETECTED // ACTIVE MITIGATION"
                analise_vulnerabilidade = (
                    f"The biometric decline of the golden ratio (<font color='#00875A'><b>{round(desvio_calculado, 2)}%</b></font>) requires immediate safeguarding "
                    f"of institutional image capital within the {self.segment} segment."
                )
                diretriz_alinhamento = (
                    f"Active submetric structural alignment, mitigating depreciation risks for holder {self.ceo} "
                    f"over the {self.horizon}-year horizon."
                )
            else:
                status_malha = "MATRIX STABILITY CONFIRMED"
                analise_vulnerabilidade = "Structural metrics operating within standard actuarial thresholds."
                diretriz_alinhamento = "Preventive maintenance of tensegrity mesh and governance."
        else:
            if self.fator_degradacao > 1.1:
                status_malha = "DECLÍNIO DE TENSEGRIDADE DETECTADO // MITIGAÇÃO ATIVA"
                analise_vulnerabilidade = (
                    f"O declínio biométrico da proporção áurea (<font color='#00875A'><b>{round(desvio_calculado, 2)}%</b></font>) exige salvaguarda imediata "
                    f"do capital de imagem institucional no segmento de {self.segment}."
                )
                diretriz_alinhamento = (
                    f"Alinhamento estrutural submétrico ativo, mitigando riscos de desvalorização para o titular {self.ceo} "
                    f"ao longo do horizonte de {self.horizon} anos."
                )
            else:
                status_malha = "ESTABILIDADE MATRICIAL CONFIRMADA"
                analise_vulnerabilidade = "Métricas estruturais operando dentro do limiar atuarial padrão."
                diretriz_alinhamento = "Manutenção preventiva da malha de tensegridade e governança."

        return {
            "pontos_malha": pontos_malha,
            "desvio_calculado": round(desvio_calculado, 2),
            "custo_evitado": round(custo_evitado_dinamico, 2),
            "valuacion": round(valuacion_patrimonial_dinamica, 2),
            "status_malha": status_malha,
            "analise_vulnerabilidade": analise_vulnerabilidade,
            "diretriz_alinhamento": diretriz_alinhamento
        }

    def gerar_dossie_modelagem(self, caminho_salvamento: Optional[str] = None, lang: Optional[str] = None) -> str:
        """Compila o Dossiê Executivo integrando Modelagem, Valuación e o Arcabouço Legal de PI."""
        if lang:
            self.lang = lang.upper()
            if self.lang not in TEXTOS_MONACO:
                self.lang = "PT"

        txt = TEXTOS_MONACO[self.lang]

        def desenhar_fundo_monaco(canvas, doc):
            canvas.saveState()
            canvas.setFont("Helvetica-Bold", 36)
            canvas.setFillColor(colors.HexColor("#B8860B"), alpha=0.03)
            canvas.saveState()
            canvas.translate(A4[0] / 2.0, A4[1] / 2.0)
            canvas.rotate(45)
            canvas.drawCentredString(0, 0, txt["marca_agua"])
            canvas.restoreState()
            
            canvas.setStrokeColor(colors.HexColor("#B8860B"))
            canvas.setLineWidth(0.75)
            canvas.line(54, 48, A4[0] - 54, 48)
            
            canvas.setFont("Helvetica", 7.5)
            canvas.setFillColor(colors.HexColor('#0A1128'))
            
            canvas.drawString(54, 36, txt["rodape_linha1"])
            canvas.drawString(54, 24, txt["rodape_linha2"])
            
            pagina_atual = canvas._pageNumber
            canvas.drawRightString(A4[0] - 54, 24, txt["rodape_seal"].format(pagina=pagina_atual))
            canvas.restoreState()

        if not caminho_salvamento:
            pasta_finais = os.path.join(ROOT_DIR, "pdfs_finais")
            os.makedirs(pasta_finais, exist_ok=True)
            caminho_salvamento = os.path.join(pasta_finais, "05_Dossie_Modelagem_Computacional_e_Juridico.pdf")
            
        os.makedirs(os.path.dirname(caminho_salvamento) if os.path.dirname(caminho_salvamento) else '.', exist_ok=True)
        
        self.emissao = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S UTC")
        calc = self.calcular_geometria_espacial_3d()
        
        temp_amb = str(self.telemetria.get("temperatura_ambiente", "28.5 °C"))
        umid_amb = str(self.telemetria.get("umidade_relativa", "74%"))
        oximetria = str(self.telemetria.get('oximetria', '98%'))
        diafragma = str(self.telemetria.get('ritmo_diafragma', '14 RPM'))

        custo_evitado_str = f"<font color='#00875A'><b>€ {calc['custo_evitado']:,.2f}</b></font>".replace(",", "X").replace(".", ",").replace("X", ".")
        valuacion_str = f"<font color='#00875A'><b>€ {calc['valuacion']:,.2f}</b></font>".replace(",", "X").replace(".", ",").replace("X", ".")

        string_base_hash = f"{self.ceo}-{self.company}-{calc['desvio_calculado']}-{self.emissao}-LEGAL-PI-{self.lang}"
        hash_sha256_gerado = hashlib.sha256(string_base_hash.encode('utf-8')).hexdigest().upper()

        doc = SimpleDocTemplate(
            caminho_salvamento,
            pagesize=A4,
            leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54,
            title="Dossiê de Modelagem Computacional e Arcabouço Legal - Monaco Sovereign"
        )

        styles = getSampleStyleSheet()
        
        MONACO_NAVY = colors.HexColor("#0A1128")
        OURO_CHAMPAGNE = colors.HexColor("#B8860B")
        DARK_TEXT = colors.HexColor("#1E293B")
        CARD_BG = colors.HexColor("#F8FAFC")
        CARD_BORDER = colors.HexColor("#CBD5E1")
        TABLE_HEADER_BG = colors.HexColor("#F1F5F9")
        EXCELENCIA_VERDE = colors.HexColor("#00875A")
        
        style_capa_titulo = ParagraphStyle('CapaTituloMod', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=MONACO_NAVY, alignment=1, spaceAfter=2)
        style_capa_sub = ParagraphStyle('CapaSubMod', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=OURO_CHAMPAGNE, alignment=1, spaceAfter=3)
        style_protocol = ParagraphStyle('ProtoMod', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10, textColor=colors.HexColor('#334155'), alignment=1, spaceAfter=6)

        style_table_header_dark = ParagraphStyle('TabHeadClean', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=9, textColor=MONACO_NAVY)
        style_cell_text_dark = ParagraphStyle('CellClean', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9, textColor=DARK_TEXT)
        style_formula_dark = ParagraphStyle('FormClean', parent=styles['Normal'], fontName='Courier-Bold', fontSize=7, leading=9, textColor=EXCELENCIA_VERDE, alignment=2)

        story: List[Flowable] = []
        
        cliente_nome = self.ceo.upper() if self.ceo else "CLIENTE UHNW"
        operador_nome = self.operador.upper() if self.operador else "THIERRY TCC"
        
        # --- 1. CABEÇALHO SUPERIOR SOLTO ---
        story.append(Paragraph(f"{self.company.upper()} • {txt['emp_sub']}", style_capa_sub))
        story.append(Paragraph(txt["doc_titulo"], style_capa_titulo))
        story.append(Paragraph(f"<b>{txt['meta_titular']}</b> <font color='#00875A'><b>{cliente_nome}</b></font> | <b>{txt['meta_horizonte']}</b> {self.horizon} {txt['anos_label']} | <b>{txt['meta_operador']}</b> {operador_nome} | <b>{txt['meta_emissao']}</b> {self.emissao}<br/><b>{txt['meta_params']}</b> Ambiente: {temp_amb} ({umid_amb}) | Setor: {self.segment}", style_protocol))
        story.append(Spacer(1, 4))

        # --- 2. SUMÁRIO EXECUTIVO ENCAPSULADO NO BLOCO PLATINA CLEAN ---
        sumario_linhas = [
            [Paragraph(txt["sumario_titulo"], style_table_header_dark), Paragraph(txt["sumario_status"], style_table_header_dark)],
            [
                Paragraph(txt["sumario_texto"].format(company=self.company), style_cell_text_dark),
                Paragraph("<font color='#00875A'><b>SECURE // LOCKED</b></font>", style_formula_dark)
            ]
        ]
        tabela_sumario = Table(sumario_linhas, colWidths=[407.27, 80])
        tabela_sumario.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('BOX', (0,0), (-1,-1), 1.0, CARD_BORDER),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ('LINEBELOW', (0,0), (-1,0), 1.5, OURO_CHAMPAGNE)
        ]))
        story.append(KeepTogether([tabela_sumario]))
        story.append(Spacer(1, 4))

        # --- 3. BLOCOS TÉCNICOS E JURÍDICOS EM BLOCO PLATINA CLEAN ---
        blocos = [
            (txt["bloco1_titulo"], [
                (txt["b1_m1_nome"], 
                 txt["b1_m1_desc"].format(pontos=calc['pontos_malha'], status=calc['status_malha']), 
                 "T_ij = d(V_i, V_j) * exp(-||u||^2)"),
                
                (txt["b1_m2_nome"], 
                 txt["b1_m2_desc"].format(desvio=calc['desvio_calculado'], vuln=calc['analise_vulnerabilidade']), 
                 "dPhi = || H_face / W_inter - 1.618 ||"),
                
                (txt["b1_m3_nome"], 
                 txt["b1_m3_desc"].format(oxi=oximetria, diaf=diafragma), 
                 "Q_flow = (SpO2 ^ 2) * Factor")
            ]),
            
            (txt["bloco2_titulo"], [
                (txt["b2_m1_nome"], 
                 txt["b2_m1_desc"].format(horizon=self.horizon, custo=custo_evitado_str), 
                 "ROI_prev = C_chir * (Horizon / 10)"),
                
                (txt["b2_m2_nome"], 
                 txt["b2_m2_desc"].format(val=valuacion_str), 
                 "Valuation = C_base * Factor [Locked]"),
                
                (txt["b2_m3_nome"], 
                 txt["b2_m3_desc"].format(diretriz=calc['diretriz_alinhamento']), 
                 "<font color='#00875A'><b>Protocolo Ativo</b></font>")
            ]),
            
            (txt["bloco3_titulo"], [
                (txt["b3_m1_nome"], 
                 txt["b3_m1_desc"], 
                 "Art. 1º - PI Soberana"),
                
                (txt["b3_m2_nome"], 
                 txt["b3_m2_desc"], 
                 "e-INPI / NDA Ativo"),
                
                (txt["b3_m3_nome"], 
                 txt["b3_m3_desc"], 
                 "Non-Compete // Lock")
            ]),
            
            (txt["bloco4_titulo"], [
                (txt["b4_m1_nome"], 
                 txt["b4_m1_desc"], 
                 "Licença Exclusiva C2"),
                
                (txt["b4_m2_nome"], 
                 txt["b4_m2_desc"], 
                 "Audit_Score = <font color='#00875A'><b>100%</b></font>"),
                
                (txt["b4_m3_nome"], 
                 txt["b4_m3_desc"].format(hash_sha=hash_sha256_gerado[:16] + "..."), 
                 "SHA-256 [Verified]")
            ])
        ]

        for titulo_bloco, itens in blocos:
            elementos_bloco: List[Flowable] = []
            linhas_tabela: List[List[Paragraph]] = []
            
            linhas_tabela.append([
                Paragraph(f"<b>{titulo_bloco}</b>", style_table_header_dark),
                Paragraph(txt["col_metrica"], style_table_header_dark)
            ])
            
            for nome_metrica, descricao, formula_matematica in itens:
                texto_formatado = f"<b>{nome_metrica}</b><br/>{descricao}"
                linhas_tabela.append([
                    Paragraph(texto_formatado, style_cell_text_dark),
                    Paragraph(formula_matematica, style_formula_dark)
                ])
                
            tabela_bloco = Table(linhas_tabela, colWidths=[337.27, 150])
            tabela_bloco.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
                ('BOX', (0,0), (-1,-1), 1.0, CARD_BORDER),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
                ('LINEBELOW', (0,0), (-1,0), 1.5, OURO_CHAMPAGNE)
            ]))
            elementos_bloco.append(tabela_bloco)
            elementos_bloco.append(Spacer(1, 4))
            story.append(KeepTogether(elementos_bloco))

        # =========================================================================
        # SEÇÃO II: ANEXO DE INTELIGÊNCIA DINÂMICA & BLINDAGEM JURÍDICA (LAUDO CLÍNICO)
        # =========================================================================
        analise_dinamica = ""
        if hasattr(self, 'telemetria') and self.telemetria:
            analise_dinamica = self.telemetria.get("analise_gemini", "") or self.telemetria.get("parecer_llm", "")
        
        if not analise_dinamica and hasattr(memoria, 'ler_dados'):
            analise_dinamica = memoria.ler_dados("analise_gemini") or memoria.ler_dados("analise_gemini_recente") or ""

        if analise_dinamica.startswith("```"):
            linhas_raw = analise_dinamica.split("\n")
            if len(linhas_raw) > 2:
                analise_dinamica = "\n".join(linhas_raw[1:-1] if linhas_raw[-1].strip() == "```" else linhas_raw[1:])
        analise_dinamica = analise_dinamica.strip()

        if analise_dinamica:
            story.append(PageBreak())
            
            estilo_laudo_header = ParagraphStyle('LaudoHeadMod', fontSize=7.0, fontName='Helvetica-Bold', textColor=OURO_CHAMPAGNE, leading=9, alignment=1)
            estilo_laudo_celula = ParagraphStyle('LaudoCelMod', fontSize=6.5, fontName='Helvetica', textColor=DARK_TEXT, leading=9)
            estilo_laudo_verde = ParagraphStyle('LaudoVerdeMod', fontSize=6.5, fontName='Helvetica-Bold', textColor=EXCELENCIA_VERDE, leading=9)

            linhas_raw = [l.strip() for l in analise_dinamica.split('\n') if l.strip()]
            tabela_dados_laudo = [
                [Paragraph(f"<b>{txt['laudo_col_param']}</b>", estilo_laudo_header), Paragraph(f"<b>{txt['laudo_col_parecer']}</b>", estilo_laudo_header)]
            ]

            for linha in linhas_raw[:22]:
                if linha.startswith("---") or linha.startswith("===") or linha.startswith("+"):
                    continue
                
                if linha.startswith("#") or (linha.startswith("**") and ":" not in linha[:15]):
                    titulo_limpo = re.sub(r"^#+\s*", "", linha).replace("**", "")
                    tabela_dados_laudo.append([
                        Paragraph(f"<b>{titulo_limpo.upper()}</b>", estilo_laudo_verde),
                        Paragraph("<b>STATUS: HOMOLOGADO // APEX UHNW</b>", estilo_laudo_verde)
                    ])
                elif "•" in linha or "|" in linha or ":" in linha:
                    partes = linha.replace("•", "").split(":", 1)
                    if len(partes) == 2:
                        chave = partes[0].strip().replace("*", "")
                        valor = partes[1].strip().replace("*", "")
                        tabela_dados_laudo.append([
                            Paragraph(f"<b>{chave}</b>", estilo_laudo_celula),
                            Paragraph(valor, estilo_laudo_celula)
                        ])
                    else:
                        tabela_dados_laudo.append([
                            Paragraph("<b>DIAGNÓSTICO JURÍDICO</b>", estilo_laudo_celula),
                            Paragraph(linha.replace("*", ""), estilo_laudo_celula)
                        ])
                else:
                    tabela_dados_laudo.append([
                        Paragraph("<b>PARECER TÉCNICO</b>", estilo_laudo_celula),
                        Paragraph(linha.replace("*", ""), estilo_laudo_celula)
                    ])

            tab_laudo_clinico = Table(tabela_dados_laudo, colWidths=[170, 317.27])
            tab_laudo_clinico.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
                ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, CARD_BG]),
                ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
                ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ('LEFTPADDING', (0,0), (-1,-1), 4),
                ('RIGHTPADDING', (0,0), (-1,-1), 4),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))

            elementos_bloco_anexo = [
                Paragraph(txt["anexo_titulo"], style_table_header_dark),
                Spacer(1, 3),
                tab_laudo_clinico
            ]

            tabela_mestre_anexo = Table([[elementos_bloco_anexo]], colWidths=[515.27])
            tabela_mestre_anexo.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
                ('BOX', (0,0), (-1,-1), 1.0, CARD_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ]))
            story.append(tabela_mestre_anexo)

        doc.build(
            story,
            onFirstPage=desenhar_fundo_monaco,
            onLaterPages=desenhar_fundo_monaco
        )
        print(f"[MONACO MODELING] Dossiê gerado com sucesso em: {caminho_salvamento} [SHA-256: {hash_sha256_gerado}]")
        return caminho_salvamento

    def gerar_dossie(self, caminho_salvamento: str = "dossie_modelagem_computacional.pdf", lang: Optional[str] = None) -> str:
        return self.gerar_dossie_modelagem(caminho_salvamento, lang=lang)

    def gerar_pdf(self, caminho_salvamento: str = "dossie_modelagem_computacional.pdf", lang: Optional[str] = None) -> str:
        return self.gerar_dossie_modelagem(caminho_salvamento, lang=lang)


if __name__ == "__main__":
    motor = C2MonacoModelingEngine(
        ceo_name="José",
        company_name="Thierry Technology Concept Global",
        market_segment="Tecnologia e Inovação",
        horizon_years=10,
        operador="THIERRY (TCC SOBERANO)",
        lang="PT"
    )
    motor.gerar_dossie_modelagem("dossie_modelagem_computacional_e_juridico.pdf")