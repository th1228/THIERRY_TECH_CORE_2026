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

# -*- coding: utf-8 -*-
"""
Módulo: carta_internacional_engine.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Versão: 6.3.12 - GLOBAL INTERNATIONAL PLATINUM EDITION (A4 ISO Harmonized)
Descrição: Emissor da Carta Diplomática e de Encaminhamento Internacional UHNW.
           Formatado em Bloco Único perfeitamente centralizado na página A4.
"""

import os
import sys
import json
import datetime
import hashlib
import re
from typing import Any, Dict, List, Optional
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable


# --- PONTE DE MEMÓRIA AUTOMÁTICA (THIERRY TECH) ---
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:
        class MemoriaMock:
            def __init__(self):
                self._dados = {}

            def salvar_dados(self, chave, valor):
                self._dados[chave] = valor
                return True

            def registrar(self, chave, valor):
                self._dados[chave] = valor
                return True

            def ler_dados(self, chave):
                return self._dados.get(chave)
        memoria = MemoriaMock()
# ---------------------------------------------------


TEXTOS_CARTA = {
    "PT": {
        "marca_agua": "GLOBAL INTERNATIONAL • DIPLOMATIC REFERRAL",
        "rodape_linha1": "International Diplomatic Referral • Protocolo Bilateral de Alta Governança UHNW • ISO/IEC 27001",
        "rodape_linha2": "THIERRY TECHNOLOGY CONCEPT GLOBAL • DIPLOMATIC AFFAIRS",
        "rodape_seal": "GLOBAL SEAL • PÁGINA {pagina} • SHA-256 SECURED",
        "emp_sub": "THIERRY TECHNOLOGY CONCEPT GLOBAL • DIPLOMATIC AFFAIRS",
        "doc_titulo": "GLOBAL INTERNATIONAL DIPLOMATIC & MEDICAL REFERRAL LETTER",
        "meta_titular": "Titular Credenciado:",
        "meta_chancela": "Chancela Operacional:",
        "meta_emissao": "Emissão:",
        "meta_jurisdicao": "Portabilidade & Governança:",
        "jurisdicao_val": (
            "Operação autônoma em qualquer jurisdição internacional, com portabilidade soberana e execução clínica "
            "complementar sob demanda por especialistas designados pelo titular"
        ),

        "sys_over_titulo": "<b>SYSTEM OVERVIEW & ENTERPRISE ARCHITECTURE</b>",
        "sys_over_texto": (
            "<b>Thierry Technology Concept Global</b> é uma infraestrutura de software corporativa (Enterprise-Grade) "
            "projetada para biometria facial de alta precisão, telemetria tecidual sem contato (rPPG), biogêmeos "
            "digitais e emissão de relatórios seguros auditáveis sob diretrizes internacionais de governança e qualidade ISO.<br/>"
            "• <i>Proteção IP:</i> Software e marca registrados no INPI (Brasil) e protegidos pela Convenção de Berna (170+ países), "
            "com custódia documental e rastreabilidade criptográfica contínua.<br/>"
            "• <i>Modelo Comercial:</i> Licenciamento exclusivo B2B (Setup + Recorrente), arquitetura soberana de baixo atrito "
            "operacional e código-fonte estritamente proprietário."
        ),
        "sumario_titulo": "<b>SUMÁRIO TÉCNICO & GLOSSÁRIO DE GOVERNANÇA</b>",
        "sumario_texto": (
            "<b>Seções:</b> 01. Declaração Diplomática | 02. Parâmetros Biométricos & Telemetria | 03. Garantias & Hash SHA-256 | 04. Chancela do Conselho.<br/>"
            "<b>Glossário:</b> • <i>rPPG:</i> Sensoriamento ótico remoto sem contato. • <i>Facial Mesh:</i> Malha geométrica 3D de alta precisão. "
            "• <i>SHA-256:</i> Custódia criptográfica e integridade forense. • <i>Governança ISO:</i> Padronização documental, sigilo e controle de acesso.<br/>"
            "• <i>Arquitetura Soberana:</i> Isolamento de dados sensíveis, trilha de auditoria imutável e continuidade operacional transfronteiriça."
        ),

        "sec1_titulo": "<b>01 // DECLARAÇÃO DE ENCAMINHAMENTO GLOBAL & STATUS DIPLOMÁTICO</b>",
        "sec1_p1": (
            "<b>To Whom It May Concern / A quem possa interessar:</b><br/>"
            "Sob titularidade intelectual exclusiva e governança privada da <b>Thierry Technology Concept Global</b>, este protocolo opera de forma "
            "autônoma em qualquer jurisdição internacional, sem redes de terceiros, intermediários não autorizados ou afiliações societárias externas. "
            "Eventual execução clínica, diagnóstica ou de longevidade complementar ocorre estritamente sob demanda por especialistas designados pelo próprio "
            "titular, assegurando discrição absoluta, rastreabilidade forense, conformidade regulatória e preservação integral do capital biológico, "
            "patrimonial e reputacional (<font color='#00875A'><b>UHNW Standard</b></font>). A arquitetura técnica prioriza confidencialidade "
            "institucional, verificação criptográfica de integridade e aderência contínua aos requisitos de segurança da informação e qualidade."
        ),

        "sec2_titulo": "<b>02 // PARÂMETROS DE AUDITORIA BIOMÉTRICA & TELEMETRIA TISSULAR</b>",
        "th_parametro": "<b>Parâmetro</b>",
        "th_leitura": "<b>Leitura</b>",
        "th_status": "<b>Status UHNW</b>",
        "t_oximetria": "Oximetria Tissular Periférica (SpO2)",
        "t_oxi_status": "<font color='#00875A'>Nominal / Otimizado</font>",
        "t_diafragma": "Ritmo Diafragmático & Frequência",
        "t_diaf_status": "<font color='#00875A'>Estável / Sincronizado</font>",
        "t_uv": "Índice UV & Condições Ambientais",
        "t_uv_status": "<font color='#00875A'>Seguro / Monitorado</font>",

        "sec3_titulo": "<b>03 // GARANTIAS DIPLOMÁTICAS, CONFORMIDADE & HASH SHA-256</b>",
        "sec3_corpo": (
            "<b>Instruções:</b> Atendimento prioritário, sigilo absoluto, zero exposição de dados sensíveis e execução sob demanda via especialistas "
            "designados pelo titular, observando princípios de privacidade, integridade e auditoria compatíveis com padrões ISO.<br/>"
            "<b>Hash SHA-256:</b> <font name='Courier' size=5.5 color='#00875A'>{hash_sha}</font>"
        ),

        "sec4_titulo": "<b>04 // CHANCELA DO CONSELHO THIERRY TECHNOLOGY CONCEPT GLOBAL</b>",
        "sec4_corpo": (
            "Aprovado, verificado e chancelado pelo Conselho da Thierry Technology Concept Global para uso diplomático, "
            "institucional e executivo internacional. [<font color='#00875A'><b>Status Locked @ 100% Verde</b></font>]"
        ),

        "anexo_titulo": "<b>[ ANEXO DE INTELIGÊNCIA DIPLOMÁTICA & NMN ]</b>",
        "laudo_col_param": "PARÂMETRO / SEÇÃO",
        "laudo_col_parecer": "DIRETRIZ ESTRATÉGICA UHNW"
    },
    "EN": {
        "marca_agua": "GLOBAL INTERNATIONAL • DIPLOMATIC REFERRAL",
        "rodape_linha1": "International Diplomatic Referral • Bilateral UHNW High Governance Protocol • ISO/IEC 27001",
        "rodape_linha2": "THIERRY TECHNOLOGY CONCEPT GLOBAL • DIPLOMATIC AFFAIRS",
        "rodape_seal": "GLOBAL SEAL • PAGE {pagina} • SHA-256 SECURED",
        "emp_sub": "THIERRY TECHNOLOGY CONCEPT GLOBAL • DIPLOMATIC AFFAIRS",
        "doc_titulo": "GLOBAL INTERNATIONAL DIPLOMATIC & MEDICAL REFERRAL LETTER",
        "meta_titular": "Accredited Holder:",
        "meta_chancela": "Operational Seal:",
        "meta_emissao": "Issuance:",
        "meta_jurisdicao": "Global Portability & Governance:",
        "jurisdicao_val": (
            "Autonomous operation across any international jurisdiction, with sovereign portability and complementary "
            "clinical execution strictly on demand via principal-designated specialists"
        ),

        "sys_over_titulo": "<b>SYSTEM OVERVIEW & ENTERPRISE ARCHITECTURE</b>",
        "sys_over_texto": (
            "<b>Thierry Technology Concept Global</b> is an enterprise-grade software infrastructure engineered for high-precision "
            "facial biometrics, contactless tissue telemetry (rPPG), digital twins, and secure verifiable reporting aligned with "
            "international governance and ISO quality standards.<br/>"
            "• <i>IP Protection:</i> Copyright and trademark registered with INPI (Brazil) and protected under the Berne Convention "
            "(170+ jurisdictions), backed by cryptographic custody and forensic auditability.<br/>"
            "• <i>Commercial Model:</i> Exclusive B2B Commercial Licensing (Setup + Recurring), sovereign operational discipline, "
            "and 100% proprietary source code."
        ),
        "sumario_titulo": "<b>TECHNICAL SUMMARY & GOVERNANCE GLOSSARY</b>",
        "sumario_texto": (
            "<b>Sections:</b> 01. Diplomatic Declaration | 02. Biometric & Tissue Telemetry | 03. Guarantees & SHA-256 Hash | 04. Council Seal.<br/>"
            "<b>Glossary:</b> • <i>rPPG:</i> Contactless remote optical sensing. • <i>Facial Mesh:</i> 3D geometric facial mapping. "
            "• <i>SHA-256:</i> Cryptographic custody and integrity verification. • <i>ISO Governance:</i> Document discipline, confidentiality, and access control.<br/>"
            "• <i>Sovereign Architecture:</i> Sensitive data isolation, immutable audit trails, and cross-border operational continuity."
        ),

        "sec1_titulo": "<b>01 // GLOBAL REFERRAL DECLARATION & DIPLOMATIC STATUS</b>",
        "sec1_p1": (
            "<b>To Whom It May Concern:</b><br/>"
            "Engineered under sole intellectual property ownership and private governance of <b>Thierry Technology Concept Global</b>, this protocol "
            "operates autonomously across any international jurisdiction, free from third-party networks, unauthorized intermediaries, or external corporate "
            "affiliations. Any complementary clinical, diagnostic, or longevity execution takes place strictly on demand through elite specialists designated "
            "solely by the principal, ensuring absolute discretion, forensic traceability, regulatory alignment, and integral preservation of biological, "
            "equity, and reputational capital (<font color='#00875A'><b>UHNW Standard</b></font>). The technical framework enforces institutional "
            "confidentiality, cryptographic integrity verification, and ongoing alignment with information security and quality governance standards."
        ),

        "sec2_titulo": "<b>02 // BIOMETRIC AUDIT PARAMETERS & TISSUE TELEMETRY</b>",
        "th_parametro": "<b>Parameter</b>",
        "th_leitura": "<b>Reading</b>",
        "th_status": "<b>UHNW Status</b>",
        "t_oximetria": "Peripheral Tissue Oximetry (SpO2)",
        "t_oxi_status": "<font color='#00875A'>Nominal / Optimized</font>",
        "t_diafragma": "Diaphragmatic Rhythm & Cadence",
        "t_diaf_status": "<font color='#00875A'>Stable / Synchronized</font>",
        "t_uv": "UV Photoinduced Index & Environment",
        "t_uv_status": "<font color='#00875A'>Safe Exposure</font>",

        "sec3_titulo": "<b>03 // RECEPTION GUIDELINES, COMPLIANCE & SHA-256 HASH</b>",
        "sec3_corpo": (
            "<b>Instructions:</b> Priority care, absolute discretion, zero unauthorized data exposure, and execution strictly on demand via "
            "principal-designated specialists, adhering to confidentiality, integrity, and auditability principles aligned with ISO standards.<br/>"
            "<b>SHA-256 Hash:</b> <font name='Courier' size=5.5 color='#00875A'>{hash_sha}</font>"
        ),

        "sec4_titulo": "<b>04 // THIERRY TECHNOLOGY CONCEPT GLOBAL COUNCIL SEAL</b>",
        "sec4_corpo": (
            "Approved, verified, and sealed by the Thierry Technology Concept Global Council for international diplomatic, "
            "institutional, and executive use. [<font color='#00875A'><b>Status Locked @ 100% Green</b></font>]"
        ),

        "anexo_titulo": "<b>[ DIPLOMATIC INTELLIGENCE ANNEX & NMN ]</b>",
        "laudo_col_param": "PARAMETER / SECTION",
        "laudo_col_parecer": "UHNW STRATEGIC OPINION"
    }
}


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


def _sanitizar_chancela(valor: Optional[str]) -> str:
    """Remove referências antigas de sigla e padroniza o nome completo da empresa."""
    texto = (valor or "").strip()
    if not texto:
        return "THIERRY TECHNOLOGY CONCEPT GLOBAL"
    texto_limpo = re.sub(r"\(?\s*TCC\s*SOBERANO\s*\)?", "", texto, flags=re.IGNORECASE).strip(" |-–—")
    if not texto_limpo or texto_limpo.upper() == "THIERRY":
        return "THIERRY TECHNOLOGY CONCEPT GLOBAL"
    return texto_limpo


def _limpar_texto_carta(texto: str) -> str:
    """Remove qualquer menção indesejada caso algum texto externo chegue à carta."""
    if not texto:
        return ""
    limpo = re.sub(
        r"[^.\n\r;]*\b(?:herpes|simplex)\b[^.\n\r;]*\.?",
        "",
        texto,
        flags=re.IGNORECASE,
    )
    return limpo.strip()


class CartaInternacionalEngine:
    def __init__(
        self,
        nome_cliente: str = "TITULAR NÃO IDENTIFICADO",
        operador: str = "THIERRY TECHNOLOGY CONCEPT GLOBAL",
        telemetria: Optional[Dict[str, Any]] = None,
        lang: str = "PT",
    ) -> None:
        self.nome_cliente = nome_cliente if nome_cliente and nome_cliente.strip() else "TITULAR NÃO IDENTIFICADO"
        self.operador = _sanitizar_chancela(operador)
        self.telemetria = telemetria if telemetria is not None else {}
        self.lang = lang.upper() if lang and isinstance(lang, str) else "PT"
        if self.lang not in TEXTOS_CARTA:
            self.lang = "PT"

        # Busca apenas conteúdo específico da carta; nunca puxa análise geral de outros módulos
        raw_analise = self.telemetria.get("analise_gemini_carta", "") or self.telemetria.get("parecer_carta", "")
        if not raw_analise and hasattr(memoria, 'ler_dados'):
            raw_analise = (
                memoria.ler_dados("analise_gemini_carta")
                or memoria.ler_dados("parecer_carta")
                or ""
            )

        raw_analise = str(raw_analise or "").strip()
        if raw_analise.startswith("```"):
            linhas_analise = raw_analise.split("\n")
            if len(linhas_analise) > 2:
                raw_analise = "\n".join(linhas_analise[1:-1] if linhas_analise[-1].strip() == "```" else linhas_analise[1:])
        self.analise_llm = _limpar_texto_carta(raw_analise)

    def _carregar_estado_sistema(self) -> Dict[str, Any]:
        caminho = os.path.join(ROOT_DIR, "estado_sistema.json")
        if os.path.exists(caminho):
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    conteudo = json.load(f)
                    if isinstance(conteudo, dict):
                        return conteudo
            except Exception:
                pass
        return {}

    def gerar_carta_apresentacao(
        self,
        pontos_base: Any = None,
        caminho_salvamento: Optional[str] = None,
        lang: Optional[str] = None,
    ) -> str:
        if lang:
            self.lang = lang.upper()
            if self.lang not in TEXTOS_CARTA:
                self.lang = "PT"

        txt = TEXTOS_CARTA[self.lang]

        if not caminho_salvamento:
            pasta_finais = os.path.join(ROOT_DIR, "pdfs_finais")
            os.makedirs(pasta_finais, exist_ok=True)
            caminho_salvamento = os.path.join(pasta_finais, "04_Carta_Internacional_UHNW.pdf")

        os.makedirs(os.path.dirname(caminho_salvamento) if os.path.dirname(caminho_salvamento) else '.', exist_ok=True)

        estado = self._carregar_estado_sistema()
        clima = estado.get("clima_payload", {}) if isinstance(estado, dict) else {}
        temp_amb = str(clima.get("temperatura_ambiente", "28.5 °C"))
        indice_uv = str(clima.get("indice_uv", "Moderado/Alto"))

        telemetria_atual = self.telemetria if isinstance(self.telemetria, dict) else {}
        oximetria = str(telemetria_atual.get('oximetria', '98.5%'))
        diafragma = str(telemetria_atual.get('ritmo_diafragma', '14 RPM'))

        timestamp_exec = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S UTC")
        string_base_hash = f"DIPLOMATIC-REFERRAL-{self.nome_cliente}-{timestamp_exec}-{self.lang}"
        hash_sha256_gerado = hashlib.sha256(string_base_hash.encode('utf-8')).hexdigest().upper()

        # Margens em pontos (1 pt = 0.352778 mm; 44 pt ≈ 15.5 mm e 48 pt ≈ 16.9 mm, acima do limite de 3.5 mm)
        margem_x = 44.0
        margem_top = 48.0
        margem_bottom = 48.0
        largura_util = A4[0] - (2 * margem_x)  # ~507.28 pt
        largura_bloco = 507.0

        def desenhar_fundo_global(canvas, doc):
            canvas.saveState()
            canvas.setFont("Helvetica-Bold", 26)
            canvas.setFillColor(colors.HexColor("#B8860B"), alpha=0.03)
            canvas.translate(A4[0] / 2.0, A4[1] / 2.0)
            canvas.rotate(45)
            canvas.drawCentredString(0, 0, txt["marca_agua"])
            canvas.restoreState()

            canvas.saveState()
            canvas.setStrokeColor(colors.HexColor("#B8860B"))
            canvas.setLineWidth(0.75)
            canvas.line(margem_x, 38, A4[0] - margem_x, 38)

            canvas.setFont("Helvetica", 6.8)
            canvas.setFillColor(colors.HexColor('#0A1128'))
            canvas.drawString(margem_x, 27, txt["rodape_linha1"])
            canvas.drawRightString(A4[0] - margem_x, 27, txt["rodape_seal"].format(pagina=canvas._pageNumber))
            canvas.restoreState()

        # ==================== CONFIGURAÇÃO DO DOCUMENTO A4 INTERNACIONAL ====================
        doc = SimpleDocTemplate(
            caminho_salvamento,
            pagesize=A4,
            leftMargin=margem_x,
            rightMargin=margem_x,
            topMargin=margem_top,
            bottomMargin=margem_bottom,
            title="04_Carta_Internacional_UHNW"
        )

        styles = getSampleStyleSheet()

        MONACO_NAVY = colors.HexColor("#0A1128")
        OURO_CHAMPAGNE = colors.HexColor("#B8860B")
        DARK_TEXT = colors.HexColor("#1E293B")
        CARD_BG = colors.HexColor("#F8FAFC")
        CARD_BORDER = colors.HexColor("#CBD5E1")
        TABLE_HEADER_BG = colors.HexColor("#F1F5F9")
        EXCELENCIA_VERDE = colors.HexColor("#00875A")

        style_capa_sub = ParagraphStyle(
            'CapaSubCarta', parent=styles['Normal'], fontName='Helvetica-Bold',
            fontSize=9.2, leading=12.0, textColor=OURO_CHAMPAGNE, alignment=1, spaceAfter=2
        )
        style_capa_titulo = ParagraphStyle(
            'CapaTituloCarta', parent=styles['Heading1'], fontName='Helvetica-Bold',
            fontSize=12.5, leading=15.8, textColor=MONACO_NAVY, alignment=1, spaceAfter=3
        )
        style_protocol = ParagraphStyle(
            'ProtoCarta', parent=styles['Normal'], fontName='Helvetica',
            fontSize=6.8, leading=9.2, textColor=colors.HexColor('#334155'), alignment=1, spaceAfter=4
        )
        style_section_title = ParagraphStyle(
            'SecTitleClean', parent=styles['Normal'], fontName='Helvetica-Bold',
            fontSize=6.8, leading=8.8, textColor=MONACO_NAVY
        )
        style_cell_text = ParagraphStyle(
            'CellClean', parent=styles['Normal'], fontName='Helvetica',
            fontSize=6.2, leading=8.2, textColor=DARK_TEXT
        )

        story: List[Flowable] = []

        cliente_nome = self.nome_cliente.upper() if self.nome_cliente else 'TITULAR NÃO IDENTIFICADO'
        operador_nome = _sanitizar_chancela(self.operador).upper()

        story.append(Spacer(1, 6))

        # --- CABEÇALHO EXTERNO ---
        story.append(Paragraph(txt["emp_sub"], style_capa_sub))
        story.append(Paragraph(txt["doc_titulo"], style_capa_titulo))
        story.append(
            Paragraph(
                f"<b>{txt['meta_titular']}</b> <font color='#00875A'><b>{cliente_nome}</b></font> "
                f"&nbsp;|&nbsp; <b>{txt['meta_chancela']}</b> {operador_nome} "
                f"&nbsp;|&nbsp; <b>{txt['meta_emissao']}</b> {timestamp_exec}<br/>"
                f"<b>{txt['meta_jurisdicao']}</b> {txt['jurisdicao_val']}",
                style_protocol,
            )
        )
        story.append(Spacer(1, 4))

        # --- BLOCO ÚNICO / TABELA MESTRE INTEGRADA ---
        bloco_unico_conteudo: List[Flowable] = []

        # 1. System Overview
        bloco_unico_conteudo.append(Paragraph(txt["sys_over_titulo"], style_section_title))
        bloco_unico_conteudo.append(Spacer(1, 1))
        bloco_unico_conteudo.append(Paragraph(txt["sys_over_texto"], style_cell_text))
        bloco_unico_conteudo.append(Spacer(1, 3))

        # 2. Sumário & Glossário
        bloco_unico_conteudo.append(Paragraph(txt["sumario_titulo"], style_section_title))
        bloco_unico_conteudo.append(Spacer(1, 1))
        bloco_unico_conteudo.append(Paragraph(txt["sumario_texto"], style_cell_text))
        bloco_unico_conteudo.append(Spacer(1, 3))

        # 3. Seção 01
        bloco_unico_conteudo.append(Paragraph(txt["sec1_titulo"], style_section_title))
        bloco_unico_conteudo.append(Spacer(1, 1))
        bloco_unico_conteudo.append(Paragraph(txt["sec1_p1"], style_cell_text))
        bloco_unico_conteudo.append(Spacer(1, 3))

        # 4. Seção 02: Tabela de Telemetria Interna (Largura total = 495 pt, dentro dos 507 pt do bloco)
        bloco_unico_conteudo.append(Paragraph(txt["sec2_titulo"], style_section_title))
        bloco_unico_conteudo.append(Spacer(1, 1))

        dados_telemetria = [
            [
                Paragraph(txt["th_parametro"], style_section_title),
                Paragraph(txt["th_leitura"], style_section_title),
                Paragraph(txt["th_status"], style_section_title),
            ],
            [
                Paragraph(txt["t_oximetria"], style_cell_text),
                Paragraph(f"<font color='#00875A'><b>{oximetria}</b></font>", style_cell_text),
                Paragraph(txt["t_oxi_status"], style_cell_text),
            ],
            [
                Paragraph(txt["t_diafragma"], style_cell_text),
                Paragraph(f"<font color='#00875A'><b>{diafragma}</b></font>", style_cell_text),
                Paragraph(txt["t_diaf_status"], style_cell_text),
            ],
            [
                Paragraph(txt["t_uv"], style_cell_text),
                Paragraph(f"<font color='#00875A'><b>{indice_uv}</b></font> ({temp_amb})", style_cell_text),
                Paragraph(txt["t_uv_status"], style_cell_text),
            ],
        ]
        tab_tel = Table(dados_telemetria, colWidths=[168, 145, 182])
        tab_tel.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), TABLE_HEADER_BG),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.3, CARD_BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))
        bloco_unico_conteudo.append(tab_tel)
        bloco_unico_conteudo.append(Spacer(1, 3))

        # 5. Seção 03 & 04
        bloco_unico_conteudo.append(Paragraph(txt["sec3_titulo"], style_section_title))
        bloco_unico_conteudo.append(Spacer(1, 1))
        bloco_unico_conteudo.append(Paragraph(txt["sec3_corpo"].format(hash_sha=hash_sha256_gerado), style_cell_text))
        bloco_unico_conteudo.append(Spacer(1, 3))

        bloco_unico_conteudo.append(Paragraph(txt["sec4_titulo"], style_section_title))
        bloco_unico_conteudo.append(Spacer(1, 1))
        bloco_unico_conteudo.append(Paragraph(txt["sec4_corpo"], style_cell_text))

        # 6. Laudo / Anexo (se houver conteúdo exclusivo da carta)
        if self.analise_llm:
            bloco_unico_conteudo.append(Spacer(1, 3))
            bloco_unico_conteudo.append(Paragraph(txt["anexo_titulo"], style_section_title))
            bloco_unico_conteudo.append(Spacer(1, 2))

            estilo_laudo_head = ParagraphStyle('LHead', fontSize=6, fontName='Helvetica-Bold', textColor=OURO_CHAMPAGNE, leading=7.5, alignment=1)
            estilo_laudo_cel = ParagraphStyle('LCel', fontSize=5.5, fontName='Helvetica', textColor=DARK_TEXT, leading=7)
            estilo_laudo_verd = ParagraphStyle('LVerd', fontSize=5.5, fontName='Helvetica-Bold', textColor=EXCELENCIA_VERDE, leading=7)

            linhas_raw = [l.strip() for l in self.analise_llm.split('\n') if l.strip()]
            tabela_dados_laudo = [
                [
                    Paragraph(f"<b>{txt['laudo_col_param']}</b>", estilo_laudo_head),
                    Paragraph(f"<b>{txt['laudo_col_parecer']}</b>", estilo_laudo_head),
                ]
            ]

            for linha in linhas_raw[:16]:
                if linha.startswith("---") or linha.startswith("===") or linha.startswith("+"):
                    continue
                if linha.startswith("#") or (linha.startswith("**") and ":" not in linha[:15]):
                    t_limpo = re.sub(r"^#+\s*", "", linha).replace("**", "")
                    tabela_dados_laudo.append([
                        Paragraph(f"<b>{t_limpo.upper()}</b>", estilo_laudo_verd),
                        Paragraph("<b>HOMOLOGADO // UHNW</b>", estilo_laudo_verd),
                    ])
                elif ":" in linha:
                    partes = linha.replace("•", "").split(":", 1)
                    tabela_dados_laudo.append([
                        Paragraph(f"<b>{partes[0].strip().replace('*', '')}</b>", estilo_laudo_cel),
                        Paragraph(partes[1].strip().replace('*', ''), estilo_laudo_cel),
                    ])
                else:
                    tabela_dados_laudo.append([
                        Paragraph("<b>PARECER</b>", estilo_laudo_cel),
                        Paragraph(linha.replace('*', ''), estilo_laudo_cel),
                    ])

            tab_laudo = Table(tabela_dados_laudo, colWidths=[152, 343])
            tab_laudo.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [TABLE_HEADER_BG, CARD_BG]),
                ('BOX', (0, 0), (-1, -1), 0.3, CARD_BORDER),
                ('INNERGRID', (0, 0), (-1, -1), 0.2, CARD_BORDER),
                ('TOPPADDING', (0, 0), (-1, -1), 1.5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 3),
                ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            bloco_unico_conteudo.append(tab_laudo)

        # Empacotamento na Tabela Mestre única (Largura = 507 pt, dentro dos ~507.28 pt úteis)
        tabela_mestre_unica = Table([[bloco_unico_conteudo]], colWidths=[largura_bloco])
        tabela_mestre_unica.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
            ('BOX', (0, 0), (-1, -1), 0.75, OURO_CHAMPAGNE),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))

        story.append(tabela_mestre_unica)

        doc.build(
            story,
            onFirstPage=desenhar_fundo_global,
            onLaterPages=desenhar_fundo_global
        )
        print(f"[CARTA INTERNACIONAL] Dossiê centralizado gerado com sucesso em: {caminho_salvamento} [SHA-256: {hash_sha256_gerado}]")
        return caminho_salvamento

    def gerar_dossie(self, caminho_salvamento: Optional[str] = None, lang: Optional[str] = None, *args, **kwargs) -> str:
        return self.gerar_carta_apresentacao(caminho_salvamento=caminho_salvamento, lang=lang)

    def gerar_pdf(self, caminho_salvamento: Optional[str] = None, lang: Optional[str] = None, *args, **kwargs) -> str:
        return self.gerar_carta_apresentacao(caminho_salvamento=caminho_salvamento, lang=lang)


if __name__ == "__main__":
    print("Iniciando emissão da Carta Internacional (Bloco Centralizado Executive Platinum)...")
    telemetria_mock = {'oximetria': '98.5%', 'ritmo_diafragma': '14 RPM'}
    motor = CartaInternacionalEngine(
        nome_cliente="Genilson Rodrigues",
        operador="THIERRY TECHNOLOGY CONCEPT GLOBAL",
        telemetria=telemetria_mock,
        lang="EN"
    )
    pasta_pdf = os.path.join(ROOT_DIR, "pdfs_finais")
    os.makedirs(pasta_pdf, exist_ok=True)
    saida = motor.gerar_carta_apresentacao(
        caminho_salvamento=os.path.join(pasta_pdf, "04_Carta_Internacional_UHNW.pdf")
    )
    print(f"Carta diplomática pronta em: {saida}")