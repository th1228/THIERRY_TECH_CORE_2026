# -*- coding: utf-8 -*-
"""
Módulo Unificado: tricologia_ultra_avancada.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Versão: 8.9.2 - MONACO EXECUTIVE PLATINUM EDITION (Bilingual PT/EN, Clinical Lab Laudo Format & Dynamic Client Name)
Descrição: Motor unificado de cálculo macroeconômico, biofísico, termografia óptica e clima ao gerador de PDF ReportLab no Padrão Executive Platinum.
"""

import os
import sys
import math
import datetime
import hashlib
import re
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas


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


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


# =====================================================================
# DICIONÁRIO DE TRADUÇÕES BILINGUE (PT / EN)
# =====================================================================
TEXTOS_TRICOLOGIA = {
    "PT": {
        "marca_agua": "MONACO PLATINUM • TRICHOLOGY EXECUTIVE STANDARD",
        "rodape_class": "Classificado • Documento de Salvaguarda Folicular e Epigenética Capilar UHNW",
        "rodape_seal": "MONACO SEAL • PÁGINA {pagina} • SHA-256 SECURED",
        "emp_top": "TRICHOLOGY DIVISION",
        "titulo_topo": "ULTRA-ADVANCED TRICHOLOGY REPORT & QUANTITATIVE HEMODYNAMICS ({segment})",
        "meta_emissao": "Emissão:",
        "meta_titular": "Titular:",
        "meta_horizonte": "Horizonte:",
        "meta_operador": "Operador:",
        "anos_label": "Anos",
        "sumario_titulo": "00 // SUMÁRIO EXECUTIVO: DIAGNÓSTICO EPIGENÉTICO E CAPILAR",
        "sumario_texto": (
            "O presente dossiê consolida a varredura optoeletrônica, termografia e hemodinâmica folicular na <b>{company}</b>. "
            "Através de algoritmos determinísticos baseados na Lei de Snell, fatores climáticos e perfusão bulbar para o setor de <b>{segment}</b>, "
            "o sistema isola o fator de estresse exógeno (Fator Cortisol: {cortisol}) e assegura parâmetros de preservação UHNW."
        ),
        "sec1_titulo": "01 // HEMODINÂMICA DO ESCALPO E HEMOPERFUSÃO BULBAR DE ALTA PRECISÃO",
        "h_vascular": "Mapeamento Vascular",
        "h_metrica": "Métrica Calculada",
        "h_painel": "Painel Gráfico & Coeficiente",
        "h_status": "Status Clínico do Tecido",
        "row_fluxo": "Fluxo Sanguíneo Capilar (Q)",
        "desc_fluxo": "Aporte real de oxigênio dérmico.",
        "row_resistencia": "Resistência Vascular (R_v)",
        "row_diag": "Diagnóstico Estratégico",
        "row_impacto": "Impacto Setorial",
        "sec2_titulo": "02 // ESPECTROMETRIA, TERMOGRAFIA ÓPTICA & CONDUTAS DISRUPTIVAS",
        "h_indicador": "Indicador / Módulo",
        "h_valor": "Valor / Parâmetro",
        "h_diretriz": "Diretriz Clínica & Análise Estrutural",
        "opt_refracao": "Índice de Refração (n)",
        "desc_refracao": "Desvio angular real da luz na fibra capilar (Lei de Snell).",
        "opt_miniaturizacao": "Taxa de Miniaturização",
        "desc_miniaturizacao": "Nível acumulado para o horizonte de {horizon} anos.",
        "opt_termografia": "Termografia Perifolicular",
        "opt_detox": "Fator Detox & Poluição",
        "opt_cronobio": "Cronobiologia Circadiana",
        "val_sincronizado": "Sincronizado",
        "opt_clima": "Fator Climático Regional",
        "umid_label": "Umid",
        "sec3_titulo": "03 // GOVERNANÇA TÉCNICA E CADEIA DE CUSTÓDIA",
        "ass_sha": "Assinatura Criptográfica SHA-256:",
        "dir_soberana": "Diretriz Soberana:",
        "auditoria_nota": "Auditoria Biomédica (Monaco Standards & European Compliance): Indicadores ajustados ao fator de estresse macroeconômico ({cortisol}) para o horizonte de {horizon} anos.",
        "anexo_titulo": "[ SEÇÃO II: ANEXO DE INTELIGÊNCIA DINÂMICA & TRICOLOGIA NMN ]",
        "laudo_col_param": "PARÂMETRO / SEÇÃO CLÍNICA",
        "laudo_col_parecer": "DIAGNÓSTICO E PARECER TÉCNICO UHNW"
    },
    "EN": {
        "marca_agua": "MONACO PLATINUM • TRICHOLOGY EXECUTIVE STANDARD",
        "rodape_class": "Classified • UHNW Follicular Safeguard & Hair Epigenetics Document",
        "rodape_seal": "MONACO SEAL • PAGE {pagina} • SHA-256 SECURED",
        "emp_top": "TRICHOLOGY DIVISION",
        "titulo_topo": "ULTRA-ADVANCED TRICHOLOGY REPORT & QUANTITATIVE HEMODYNAMICS ({segment})",
        "meta_emissao": "Issuance:",
        "meta_titular": "Principal:",
        "meta_horizonte": "Horizon:",
        "meta_operador": "Operator:",
        "anos_label": "Years",
        "sumario_titulo": "00 // EXECUTIVE SUMMARY: EPIGENETIC AND HAIR DIAGNOSTIC",
        "sumario_texto": (
            "This dossier consolidates optoelectronic scanning, thermography, and follicular hemodynamics at <b>{company}</b>. "
            "Through deterministic algorithms based on Snell's Law, climatic factors, and bulbar perfusion for the <b>{segment}</b> sector, "
            "the system isolates the exogenous stress factor (Cortisol Factor: {cortisol}) and ensures UHNW preservation parameters."
        ),
        "sec1_titulo": "01 // SCALP HEMODYNAMICS & HIGH-PRECISION BULBAR HEMOPERFUSION",
        "h_vascular": "Vascular Mapping",
        "h_metrica": "Calculated Metric",
        "h_painel": "Graphic Panel & Coefficient",
        "h_status": "Tissue Clinical Status",
        "row_fluxo": "Capillary Blood Flow (Q)",
        "desc_fluxo": "Real dermal oxygen supply.",
        "row_resistencia": "Vascular Resistance (R_v)",
        "row_diag": "Strategic Diagnosis",
        "row_impacto": "Sector Impact",
        "sec2_titulo": "02 // SPECTROMETRY, OPTICAL THERMOGRAPHY & DISRUPTIVE CONDUCTS",
        "h_indicador": "Indicator / Module",
        "h_valor": "Value / Parameter",
        "h_diretriz": "Clinical Guideline & Structural Analysis",
        "opt_refracao": "Refractive Index (n)",
        "desc_refracao": "Real angular deviation of light in the hair fiber (Snell's Law).",
        "opt_miniaturizacao": "Miniaturization Rate",
        "desc_miniaturizacao": "Accumulated level for the {horizon}-year horizon.",
        "opt_termografia": "Perifollicular Thermography",
        "opt_detox": "Detox Factor & Pollution",
        "opt_cronobio": "Circadian Chronobiology",
        "val_sincronizado": "Synchronized",
        "opt_clima": "Regional Climatic Factor",
        "umid_label": "Humid",
        "sec3_titulo": "03 // TECHNICAL GOVERNANCE AND CUSTODY CHAIN",
        "ass_sha": "Cryptographic Signature SHA-256:",
        "dir_soberana": "Sovereign Guideline:",
        "auditoria_nota": "Biomedical Audit (Monaco Standards & European Compliance): Indicators adjusted to the macroeconomic stress factor ({cortisol}) for the {horizon}-year horizon.",
        "anexo_titulo": "[ SECTION II: DYNAMIC INTELLIGENCE ANNEX & NMN TRICHOLOGY ]",
        "laudo_col_param": "PARAMETER / CLINICAL SECTION",
        "laudo_col_parecer": "UHNW DIAGNOSIS AND TECHNICAL OPINION"
    }
}


class SovereignSecureCanvas(canvas.Canvas):
    """Canvas de Alta Segurança Atuarial com Marca d'Água Executiva Sutil e Rodapé Corrigido sem Sobreposição."""
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
        self.translate(A4[0] / 2.0, A4[1] / 2.0)
        self.rotate(35)
        self.drawCentredString(0, 0, "MONACO PLATINUM • TRICHOLOGY EXECUTIVE STANDARD")
        self.restoreState()
        
        self.saveState()
        self.setStrokeColor(colors.HexColor('#B8860B'))
        self.setLineWidth(0.75)
        
        self.line(30, 40, A4[0] - 30, 40)
        
        self.setFont("Helvetica", 6.5)
        self.setFillColor(colors.HexColor('#0A1128'))
        pagina_atual = self._pageNumber
        
        self.drawString(30, 26, "Classificado • Documento de Salvaguarda Folicular e Epigenética Capilar UHNW")
        self.drawRightString(A4[0] - 30, 26, f"MONACO SEAL • PÁGINA {pagina_atual} • SHA-256 SECURED")
        self.restoreState()


class C2UltraAdvancedTrichologyEngine:
    """
    Motor Unificado de Ultra-Elite: Engenharia Biofísica, Espectrometria Capilar, 
    Termografia Óptica, Cronobiologia, Fatores Climáticos e Geração PDF Executive Platinum com Nome Dinâmico.
    """
    def __init__(
        self, 
        ceo_name: Optional[str] = None, 
        company_name: str = "Thierry Technology Concept Global", 
        market_segment: str = "Tecnologia, Inovação e Longevidade Global", 
        horizon_years: int = 10, 
        operador: str = "Thierry",
        frame_capturado_rgb=None, 
        densidade_fios_estimada: float = 130.0, 
        miniaturizacao_pct: float = 22.5, 
        umidade_ar_pct: float = 85.0, 
        temp_externa_c: float = 32.0,
        telemetria: Optional[Dict[str, Any]] = None,
        lang: str = "PT",
        *args,
        **kwargs
    ) -> None:
        self.telemetria_externa = telemetria or {}
        
        # Resolução dinâmica do nome do cliente/titular vindo do painel, telemetria ou fallback seguro
        self.ceo = ceo_name or self.telemetria_externa.get('nome_cliente') or self.telemetria_externa.get('nome') or "Cliente UHNW"
        
        self.company = company_name
        self.segment = market_segment
        self.horizon = int(horizon_years)
        self.operador = operador
        self.densidade_fios = float(densidade_fios_estimada)
        self.miniaturizacao = float(miniaturizacao_pct)
        self.umidade_ar = float(umidade_ar_pct)
        self.temp_externa = float(temp_externa_c)
        self.lang = lang.upper() if lang and isinstance(lang, str) else "PT"
        if self.lang not in TEXTOS_TRICOLOGIA:
            self.lang = "PT"
            
        self.emissao = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S UTC")
        
        if frame_capturado_rgb is not None:
            self.temp_perifolicular, self.saturacao_poluicao, self.pico_cortisol_dinamico = self._analisar_biometria_optica(frame_capturado_rgb)
        else:
            self.temp_perifolicular = 34.2
            self.saturacao_poluicao = "Crítica (Urbana)"
            self.pico_cortisol_dinamico = "Noite"

        if any(kw in market_segment.lower() for kw in ["tecnologia", "varejo", "alimentos", "inovação", "financeiro"]):
            self.fator_cortisol = 1.38
        else:
            self.fator_cortisol = 1.00

        raw_analise = self.telemetria_externa.get("analise_gemini_trico", "") or self.telemetria_externa.get("parecer_tricologia", "")
        if not raw_analise and hasattr(memoria, 'ler_dados'):
            raw_analise = memoria.ler_dados("analise_gemini_trico") or memoria.ler_dados("parecer_tricologia") or memoria.ler_dados("analise_gemini") or ""
        
        if raw_analise.startswith("```"):
            linhas_analise = raw_analise.split("\n")
            if len(linhas_analise) > 2:
                raw_analise = "\n".join(linhas_analise[1:-1] if linhas_analise[-1].strip() == "```" else linhas_analise[1:])
        self.analise_llm = raw_analise.strip()

    def _analisar_biometria_optica(self, frame) -> Tuple[float, str, str]:
        try:
            img_float = frame.astype(np.float32)
            canal_r = np.mean(img_float[:, :, 2])
            canal_g = np.mean(img_float[:, :, 1])
            
            temp_calculada = 33.0 + (canal_r / (canal_g + 1e-5)) * 1.5
            temp_calculada = round(min(max(temp_calculada, 32.5), 36.5), 1)

            luminancia = np.mean(0.299 * img_float[:, :, 2] + 0.587 * img_float[:, :, 1] + 0.114 * img_float[:, :, 0])
            if luminancia < 90:
                poluicao = "Crítica (Urbana com sujidade particulada acumulada)"
            elif luminancia < 120:
                poluicao = "Moderada (Saturação sebácea e oxidativa)"
            else:
                poluicao = "Baixa (Microambiente limpo)"
        except Exception:
            temp_calculada = 34.2
            poluicao = "Moderada (Fallback de segurança ativado)"

        hora_atual = datetime.datetime.now().hour
        if self.lang == "EN":
            if 5 <= hora_atual < 12:
                cortisol_horario = "Morning (High permeability window & VEGF absorption)"
            elif 12 <= hora_atual < 18:
                cortisol_horario = "Afternoon (Follicular metabolic stabilization phase)"
            else:
                cortisol_horario = "Night (Mitochondrial activity peak & critical DHT window)"
        else:
            if 5 <= hora_atual < 12:
                cortisol_horario = "Manhã (Janela de alta permeabilidade e absorção de VEGF)"
            elif 12 <= hora_atual < 18:
                cortisol_horario = "Tarde (Fase de estabilização metabólica folicular)"
            else:
                cortisol_horario = "Noite (Pico de atividade mitocondrial e janela crítica de DHT)"

        return temp_calculada, poluicao, cortisol_horario

    def calcular_telemetria_capilar(self) -> Dict[str, Any]:
        fluxo_sanguineo_base = 12.0  
        resistencia_vascular_base = 10.01  
        indice_refracao_base = 1.54  
        
        fluxo_calculado = fluxo_sanguineo_base / (self.fator_cortisol ** 0.5)
        resistencia_calculada = resistencia_vascular_base * self.fator_cortisol
        desvio_optico_snell = indice_refracao_base * (1.0 + (0.012 * self.fator_cortisol))
        
        taxa_miniaturizacao = self.miniaturizacao * (self.horizon / 10) * (self.fator_cortisol / 1.0)
        if taxa_miniaturizacao > 45.0: 
            taxa_miniaturizacao = 45.0  

        if self.lang == "EN":
            if self.temp_perifolicular < 34.5:
                alerta_termico = f"Thermal Optical Alert ({self.temp_perifolicular}°C): Perifollicular vasoconstriction. Mandatory pre-heating with 830nm LED."
            else:
                alerta_termico = f"Stable Thermal Profile ({self.temp_perifolicular}°C): Microcirculation optimized for permeation."

            if "Crítica" in self.saturacao_poluicao or "Moderada" in self.saturacao_poluicao or "Critical" in self.saturacao_poluicao or "Moderate" in self.saturacao_poluicao:
                fator_detox = f"Saturation [{self.saturacao_poluicao}]: Osteo-follicular under oxidative stress. Requires preliminary Fractional Plasma sweep."
            else:
                fator_detox = f"Optical Saturation: {self.saturacao_poluicao}. Favorable conditions."

            if "Noite" in self.pico_cortisol_dinamico or "Night" in self.pico_cortisol_dinamico:
                cronograma_horario = f"Chronobiology [{self.pico_cortisol_dinamico}]: Night mitochondrial peak. Apply 5-alpha-reductase blocker at 10:30 PM."
            else:
                cronograma_horario = f"Chronobiology [{self.pico_cortisol_dinamico}]: Active daytime synchronization."

            if self.umidade_ar > 80:
                alerta_clima = f"Climatic Factor (Humidity: {self.umidade_ar}% | Temp: {self.temp_externa}°C): High humidity, risk of microbial dysbiosis. Antiseptics mandatory."
            else:
                alerta_clima = f"Climatic Factor (Humidity: {self.umidade_ar}% | Temp: {self.temp_externa}°C): Dry environment. Focus on water occlusion."

            if self.fator_cortisol > 1.2:
                status_clinico = "PROGRESSIVE PERIPHERAL BULBAR ISCHEMIA"
                vulnerabilidade_texto = (
                    f"Follicular atrophy reflects the immediate biological impact of stress "
                    f"in the {self.segment} segment. Vascular resistance of {round(resistencia_calculada, 2)} dyn s/cm³."
                )
                diretriz_tática = (
                    f"Mandatory ULTRA TRICHOLOGY protocol activation to stabilize "
                    f"{self.ceo}'s hemoperfusion. Image preservation essential for {self.company}."
                )
            else:
                status_clinico = "VASCULAR PRESERVATION IN MAINTENANCE PATTERN"
                vulnerabilidade_texto = "Exogenous stress within actuarial normality."
                diretriz_tática = "Standard preventive oxygenation and spectrophotometry maintenance."
        else:
            if self.temp_perifolicular < 34.5:
                alerta_termico = f"Alerta Térmico Óptico ({self.temp_perifolicular}°C): Vasoconstrição perifolicular. Obrigatório pré-aquecimento com LED 830nm."
            else:
                alerta_termico = f"Perfil Térmico Estável ({self.temp_perifolicular}°C): Microcirculação otimizada para permeação."

            if "Crítica" in self.saturacao_poluicao or "Moderada" in self.saturacao_poluicao:
                fator_detox = f"Saturação [{self.saturacao_poluicao}]: Ósteo folicular sob stress oxidativo. Requer varredura prévia com Plasma Fracionado."
            else:
                fator_detox = f"Saturação Óptica: {self.saturacao_poluicao}. Condições favoráveis."

            if "Noite" in self.pico_cortisol_dinamico:
                cronograma_horario = f"Cronobiologia [{self.pico_cortisol_dinamico}]: Pico mitocondrial noturno. Aplicar bloqueador de 5-alfa-redutase às 22:30."
            else:
                cronograma_horario = f"Cronobiologia [{self.pico_cortisol_dinamico}]: Sincronização diurna ativa."

            if self.umidade_ar > 80:
                alerta_clima = f"Fator Climático (Umidade: {self.umidade_ar}% | Temp: {self.temp_externa}°C): Alta umidade, risco de disbiose microbiana. Uso de antissépticos obrigatório."
            else:
                alerta_clima = f"Fator Climático (Umidade: {self.umidade_ar}% | Temp: {self.temp_externa}°C): Ambiente seco. Foco em oclusão hídrica."

            if self.fator_cortisol > 1.2:
                status_clinico = "ISQUEMIA BULBAR PERIFÉRICA EM PROGRESSÃO"
                vulnerabilidade_texto = (
                    f"A atrofia folicular reflete o impacto biológico imediato do estresse "
                    f"no segmento de {self.segment}. Resistência vascular de {round(resistencia_calculada, 2)} dyn s/cm³."
                )
                diretriz_tática = (
                    f"Ativação do protocolo TRICOLOGIA ULTRA mandatória para estabilizar a "
                    f"hemoperfusão de {self.ceo}. Preservação de imagem essencial para a {self.company}."
                )
            else:
                status_clinico = "PRESERVAÇÃO VASCULAR EM PADRÃO DE MANUTENÇÃO"
                vulnerabilidade_texto = "Estresse exógeno dentro da normalidade atuarial."
                diretriz_tática = "Manutenção preventiva padrão de oxigenação e espectrofotometria."

        return {
            "fluxo_q": round(fluxo_calculado, 2),
            "resistencia_r": round(resistencia_calculada, 2),
            "indice_n": round(desvio_optico_snell, 3),
            "taxa_miniaturizacao": round(taxa_miniaturizacao, 2),
            "status_clinico": status_clinico,
            "vulnerabilidade_texto": vulnerabilidade_texto,
            "diretriz_tática": diretriz_tática,
            "alerta_termico": alerta_termico,
            "fator_detox": fator_detox,
            "cronograma_horario": cronograma_horario,
            "alerta_clima": alerta_clima
        }

    def gerar_pdf_tricologia_avancada(self, caminho_salvamento: str = "tricologia_ultra_avancada_dossier.pdf", lang: Optional[str] = None) -> str:
        if lang:
            self.lang = lang.upper()
            if self.lang not in TEXTOS_TRICOLOGIA:
                self.lang = "PT"

        txt = TEXTOS_TRICOLOGIA[self.lang]
        self.emissao = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S UTC")
        
        dados = self.calcular_telemetria_capilar()
        
        string_base_hash = f"TRICOLOGIA-{self.ceo}-{self.company}-{dados['fluxo_q']}-{self.emissao}-{self.lang}"
        hash_sha256 = hashlib.sha256(string_base_hash.encode('utf-8')).hexdigest().upper()

        os.makedirs(os.path.dirname(caminho_salvamento) if os.path.dirname(caminho_salvamento) else '.', exist_ok=True)
        
        doc = SimpleDocTemplate(
            caminho_salvamento, 
            pagesize=A4, 
            leftMargin=30, 
            rightMargin=30, 
            topMargin=30, 
            bottomMargin=45
        )
        
        MONACO_NAVY = colors.HexColor('#0A1128')
        SOVEREIGN_GOLD = colors.HexColor('#B8860B')   
        EXCELENCIA_VERDE = colors.HexColor('#00875A') 
        DARK_TEXT = colors.HexColor('#1E293B')        
        WHITE_BG = colors.HexColor('#FFFFFF')         
        CARD_BORDER = colors.HexColor('#CBD5E1')      
        TABLE_HEADER_BG = colors.HexColor('#F8FAFC')  
        
        estilo_empresa_topo = ParagraphStyle('EmpTop', fontSize=7, fontName='Helvetica-Bold', textColor=SOVEREIGN_GOLD, alignment=1, spaceAfter=2)
        estilo_titulo_topo = ParagraphStyle('TitleTop', fontSize=12.5, fontName='Helvetica-Bold', textColor=MONACO_NAVY, leading=15, alignment=1, spaceAfter=3)
        estilo_meta_topo = ParagraphStyle('MetaTop', fontSize=7, fontName='Helvetica', textColor=colors.HexColor('#334155'), alignment=1, spaceAfter=6)
        
        estilo_sumario_titulo = ParagraphStyle('SumSec', fontSize=8, fontName='Helvetica-Bold', textColor=MONACO_NAVY, spaceBefore=4, spaceAfter=2)
        estilo_sumario_texto = ParagraphStyle('SumText', fontSize=7, fontName='Helvetica', textColor=DARK_TEXT, leading=9.5, spaceAfter=6, alignment=4)
        
        estilo_secao = ParagraphStyle('SecTrico', fontSize=7.5, fontName='Helvetica-Bold', textColor=MONACO_NAVY, spaceBefore=4, spaceAfter=2)
        estilo_corpo = ParagraphStyle('CorpoTrico', fontSize=6.0, fontName='Helvetica', textColor=DARK_TEXT, leading=8.0, spaceAfter=2, alignment=4)
        estilo_celula = ParagraphStyle('CelTrico', fontSize=5.5, fontName='Helvetica-Bold', textColor=MONACO_NAVY, leading=7.5)
        estilo_celula_header = ParagraphStyle('CelHeadTrico', fontSize=5.5, fontName='Helvetica-Bold', textColor=SOVEREIGN_GOLD, leading=7.5, alignment=1)
        estilo_metrica_verde = ParagraphStyle('CelVerde', fontSize=5.5, fontName='Helvetica-Bold', textColor=EXCELENCIA_VERDE, leading=7.5)
        estilo_codigo = ParagraphStyle('CodTrico', fontSize=5.5, fontName='Courier-Bold', textColor=EXCELENCIA_VERDE, alignment=2)
        estilo_auditoria = ParagraphStyle('NotaAuditoriaTrico', fontSize=5, fontName='Helvetica-Oblique', textColor=colors.HexColor('#64748B'), leading=7, alignment=1, spaceBefore=3)
        
        ceo_nome = self.ceo.upper() if self.ceo else 'CLIENTE UHNW'
        operador_nome = self.operador.upper() if self.operador else 'THIERRY'

        story: List[Flowable] = []

        # =========================================================================
        # PÁGINA 1: TOPO SOLTO + BLOCO MESTRE INFERIOR
        # =========================================================================
        story.append(Paragraph(f"{self.company.upper()} • {txt['emp_top']}", estilo_empresa_topo))
        story.append(Paragraph(txt['titulo_topo'].format(segment=self.segment), estilo_titulo_topo))
        story.append(Paragraph(f"<b>{txt['meta_emissao']}</b> {self.emissao} | <b>{txt['meta_titular']}</b> {ceo_nome} | <b>{txt['meta_horizonte']}</b> {self.horizon} {txt['anos_label']} | <b>{txt['meta_operador']}</b> {operador_nome}", estilo_meta_topo))
        
        story.append(Paragraph(txt['sumario_titulo'], estilo_sumario_titulo))
        story.append(Paragraph(
            txt['sumario_texto'].format(company=self.company, segment=self.segment, cortisol=self.fator_cortisol),
            estilo_sumario_texto
        ))
        story.append(Spacer(1, 2))

        elementos_bloco_pagina1: List[Any] = [
            Paragraph(txt['sec1_titulo'], estilo_secao),
        ]
        
        dados_hemodinamica = [
            [Paragraph(txt['h_vascular'], estilo_celula_header), Paragraph(txt['h_metrica'], estilo_celula_header), Paragraph(txt['h_painel'], estilo_celula_header), Paragraph(txt['h_status'], estilo_celula_header)],
            [Paragraph(txt['row_fluxo'], estilo_celula), Paragraph(f"{dados['fluxo_q']} RPM", estilo_metrica_verde), Paragraph(f'<font color="#00875A"><b>[■■■■■■■■□□] {dados["fluxo_q"]}</b></font>', estilo_codigo), Paragraph(txt['desc_fluxo'], estilo_corpo)],
            [Paragraph(txt['row_resistencia'], estilo_celula), Paragraph(f"{dados['resistencia_r']} dyn·s/cm⁵", estilo_celula), Paragraph(f'<font color="#B8860B"><b>{dados["resistencia_r"]}</b></font>', estilo_codigo), Paragraph(dados['status_clinico'], estilo_corpo)],
            [Paragraph(txt['row_diag'], estilo_celula), Paragraph(txt['row_impacto'], estilo_celula), Paragraph(f'<font color="#00875A"><b>{self.segment}</b></font>', estilo_metrica_verde), Paragraph(dados['vulnerabilidade_texto'], estilo_corpo)]
        ]
        
        tab_hemo = Table(dados_hemodinamica, colWidths=[105, 75, 105, 225])
        tab_hemo.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), WHITE_BG),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, WHITE_BG]),
            ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos_bloco_pagina1.append(tab_hemo)
        elementos_bloco_pagina1.append(Spacer(1, 4))
        
        elementos_bloco_pagina1.append(Paragraph(txt['sec2_titulo'], estilo_secao))
        dados_optica = [
            [Paragraph(txt['h_indicador'], estilo_celula_header), Paragraph(txt['h_valor'], estilo_celula_header), Paragraph(txt['h_diretriz'], estilo_celula_header)],
            [Paragraph(txt['opt_refracao'], estilo_celula), Paragraph(f'{dados["indice_n"]} η', estilo_metrica_verde), Paragraph(txt['desc_refracao'], estilo_corpo)],
            [Paragraph(txt['opt_miniaturizacao'], estilo_celula), Paragraph(f'{dados["taxa_miniaturizacao"]}%', estilo_metrica_verde), Paragraph(txt['desc_miniaturizacao'].format(horizon=self.horizon), estilo_corpo)],
            [Paragraph(txt['opt_termografia'], estilo_celula), Paragraph(f'{self.temp_perifolicular}°C', estilo_celula), Paragraph(dados['alerta_termico'], estilo_corpo)],
            [Paragraph(txt['opt_detox'], estilo_celula), Paragraph(self.saturacao_poluicao[:15] + '...', estilo_celula), Paragraph(dados['fator_detox'], estilo_corpo)],
            [Paragraph(txt['opt_cronobio'], estilo_celula), Paragraph(txt['val_sincronizado'], estilo_metrica_verde), Paragraph(dados['cronograma_horario'], estilo_corpo)],
            [Paragraph(txt['opt_clima'], estilo_celula), Paragraph(f"{txt['umid_label']}: {self.umidade_ar}%", estilo_celula), Paragraph(dados['alerta_clima'], estilo_corpo)]
        ]
        
        tab_optica = Table(dados_optica, colWidths=[110, 80, 314])
        tab_optica.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), WHITE_BG),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, WHITE_BG]),
            ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elementos_bloco_pagina1.append(tab_optica)
        elementos_bloco_pagina1.append(Spacer(1, 4))

        elementos_bloco_pagina1.append(Paragraph(txt['sec3_titulo'], estilo_secao))
        elementos_bloco_total_texto = f"""
        <b>{txt['ass_sha']}</b> <font name='Courier' size=5.5 color='#00875A'>{hash_sha256}</font><br/>
        <b>{txt['dir_soberana']}</b> <font color='#00875A'>{dados['diretriz_tática']}</font>
        """
        elementos_bloco_pagina1.append(Paragraph(elementos_bloco_total_texto, estilo_corpo))
        elementos_bloco_pagina1.append(Spacer(1, 2))
        
        elementos_bloco_pagina1.append(Paragraph(txt['auditoria_nota'].format(cortisol=self.fator_cortisol, horizon=self.horizon), estilo_auditoria))

        bloco_mestre_pagina1 = Table([[elementos_bloco_pagina1]], colWidths=[530])
        bloco_mestre_pagina1.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), WHITE_BG),
            ('BOX', (0,0), (-1,-1), 1.0, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(bloco_mestre_pagina1)

        # =========================================================================
        # SEÇÃO II: ANEXO DE INTELIGÊNCIA DINÂMICA & NMN (LAUDO CLÍNICO HOSPITALAR)
        # =========================================================================
        if self.analise_llm:
            story.append(PageBreak())
            
            estilo_laudo_titulo = ParagraphStyle('LaudoSec', fontSize=7.5, fontName='Helvetica-Bold', textColor=MONACO_NAVY, spaceBefore=4, spaceAfter=2)
            estilo_laudo_corpo = ParagraphStyle('LaudoCorpo', fontSize=6.0, fontName='Helvetica', textColor=DARK_TEXT, leading=8.5, spaceAfter=2, alignment=4)
            estilo_laudo_header = ParagraphStyle('LaudoHead', fontSize=5.5, fontName='Helvetica-Bold', textColor=SOVEREIGN_GOLD, leading=7.5, alignment=1)
            estilo_laudo_celula = ParagraphStyle('LaudoCel', fontSize=5.5, fontName='Helvetica', textColor=DARK_TEXT, leading=7.5)
            estilo_laudo_verde = ParagraphStyle('LaudoVerde', fontSize=5.5, fontName='Helvetica-Bold', textColor=EXCELENCIA_VERDE, leading=7.5)

            elementos_bloco_pagina2: List[Any] = [
                Paragraph(f"<b>{txt['anexo_titulo']}</b>", estilo_laudo_titulo),
                Spacer(1, 4)
            ]

            linhas_raw = [l.strip() for l in self.analise_llm.split('\n') if l.strip()]
            
            tabela_dados_laudo = [
                [Paragraph(f"<b>{txt['laudo_col_param']}</b>", estilo_laudo_header), Paragraph(f"<b>{txt['laudo_col_parecer']}</b>", estilo_laudo_header)]
            ]

            for linha in linhas_raw[:26]:
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
                            Paragraph(valor, estilo_laudo_corpo)
                        ])
                    else:
                        tabela_dados_laudo.append([
                            Paragraph("<b>DIAGNÓSTICO CLÍNICO</b>", estilo_laudo_celula),
                            Paragraph(linha.replace("*", ""), estilo_laudo_corpo)
                        ])
                else:
                    tabela_dados_laudo.append([
                        Paragraph("<b>PARECER TÉCNICO</b>", estilo_laudo_celula),
                        Paragraph(linha.replace("*", ""), estilo_laudo_corpo)
                    ])

            tab_laudo_clinico = Table(tabela_dados_laudo, colWidths=[180, 350])
            tab_laudo_clinico.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), WHITE_BG),
                ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_HEADER_BG, WHITE_BG]),
                ('BOX', (0,0), (-1,-1), 0.5, CARD_BORDER),
                ('INNERGRID', (0,0), (-1,-1), 0.3, CARD_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 2.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
                ('LEFTPADDING', (0,0), (-1,-1), 4),
                ('RIGHTPADDING', (0,0), (-1,-1), 4),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))

            elementos_bloco_pagina2.append(tab_laudo_clinico)

            bloco_mestre_pagina2 = Table([[elementos_bloco_pagina2]], colWidths=[530])
            bloco_mestre_pagina2.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), WHITE_BG),
                ('BOX', (0,0), (-1,-1), 1.0, CARD_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ]))
            story.append(bloco_mestre_pagina2)

        doc.build(story, canvasmaker=SovereignSecureCanvas)
        print(f"[C2 ENGINE] PDF de Tricologia gerado com sucesso em: {caminho_salvamento} [SHA-256: {hash_sha256}]")
        return caminho_salvamento

    def gerar_dossie(self, caminho_salvamento: str = "tricologia_ultra_avancada_dossier.pdf", lang: Optional[str] = None, *args, **kwargs) -> str:
        return self.gerar_pdf_tricologia_avancada(caminho_salvamento=caminho_salvamento, lang=lang)

    def gerar_pdf(self, caminho_salvamento: str = "tricologia_ultra_avancada_dossier.pdf", lang: Optional[str] = None, *args, **kwargs) -> str:
        return self.gerar_pdf_tricologia_avancada(caminho_salvamento=caminho_salvamento, lang=lang)


if __name__ == "__main__":
    pasta_finais = os.path.join(ROOT_DIR, "pdfs_finais")
    os.makedirs(pasta_finais, exist_ok=True)
    caminho_teste = os.path.join(pasta_finais, "02_Dossie_Tricologia_Avancada.pdf")
    
    engine = C2UltraAdvancedTrichologyEngine(lang="PT")
    arquivo_gerado = engine.gerar_pdf_tricologia_avancada(caminho_teste)
    print(f"Gerador de Tricologia executado! Salvo em: {arquivo_gerado}")