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
Módulo Unificado: tricologia_ultra_avancada.py
Sistema: Thierry Technology Concept Global - Trichology & Longevity Engine
Versão: 19.1.0 - DETERMINISTIC TELEMETRY & REPORT EDITION
Descrição: Motor unificado de telemetria capilar determinística, projeção de risco,
           estimativa de custo de inação (COA) e geração de dossiê PDF em PT/EN.
"""

import os
import sys
import datetime
import hashlib
import re
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


# --- PONTE DE MEMÓRIA AUTOMÁTICA (THIERRY TECH) ---
MEMORIA_TRICO_DISPONIVEL = True
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:
        MEMORIA_TRICO_DISPONIVEL = False

        class MemoriaMock:
            modo_fallback = True

            def salvar_dados(self, chave, valor):
                print(f"[AVISO TRICOLOGIA MEMÓRIA FALLBACK] Persistência indisponível ao salvar '{chave}'.")

            def registrar(self, chave, valor):
                print(f"[AVISO TRICOLOGIA MEMÓRIA FALLBACK] Persistência indisponível ao registrar '{chave}'.")

            def ler_dados(self, chave):
                return None

        memoria = MemoriaMock()
# ---------------------------------------------------



# === [REPARADOR TTC] PONTE LEITURA MEMORIA TRICOLOGIA ===
MAPA_SECOES_TRICOLOGIA = {
    "diagnostico": ("diagnostico", "diagnostico_capilar"),
    "reconstrucao": ("reconstrucao", "protocolo_reconstrucao"),
    "plasma_fadiga": ("plasma_fadiga", "protocolo_plasma_fadiga"),
    "queda": ("queda", "queda_capilar", "detector_queda_capilar"),
    "fibra": ("fibra", "fibra_capilar"),
    "minerais_impurezas": ("minerais_impurezas", "minerais_impurezas_quelacao"),
    "eletricidade_volume": ("eletricidade_volume", "eletricidade_volume_densidade"),
    "projecao_clima_rosto": ("projecao_clima_rosto", "clima_rosto_couro_projecao"),
    "cronograma": ("cronograma", "cronograma_capilar"),
}


def _ttc_extrair_numero(valor):
    if valor is None or isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        num = float(valor)
        return num if np.isfinite(num) else None
    if isinstance(valor, str):
        match = re.search(r"-?\d+(?:[\.,]\d+)?", valor.strip())
        if match:
            try:
                num = float(match.group(0).replace(",", "."))
                return num if np.isfinite(num) else None
            except ValueError:
                return None
    return None


def _ttc_buscar_numero(d, chaves):
    if not isinstance(d, dict):
        return None
    for chave in chaves:
        if chave in d:
            num = _ttc_extrair_numero(d[chave])
            if num is not None:
                return num
    for sub in d.values():
        if isinstance(sub, dict):
            num = _ttc_buscar_numero(sub, chaves)
            if num is not None:
                return num
    return None


def puxar_dados_tricologia_memoria(cliente=None, dados_iniciais=None, memoria_instancia=None):
    mem_alvo = memoria_instancia if memoria_instancia is not None else memoria
    dossie = dict(dados_iniciais) if isinstance(dados_iniciais, dict) else {}
    secoes_saida = dict(dossie["secoes"]) if isinstance(dossie.get("secoes"), dict) else {}

    for caminho_helper in (
        "core.tricologia_saude.memoria_tricologia_helper",
        "tricologia_saude.memoria_tricologia_helper",
        "memoria_tricologia_helper",
    ):
        try:
            mod_helper = __import__(caminho_helper, fromlist=["ler_dossie_tricologia_memoria"])
            fn_ler = getattr(mod_helper, "ler_dossie_tricologia_memoria", None)
            if callable(fn_ler):
                lido = fn_ler(cliente=cliente, memoria_instancia=mem_alvo)
                if isinstance(lido, dict):
                    if lido.get("cliente") and not dossie.get("cliente"):
                        dossie["cliente"] = lido["cliente"]
                    if lido.get("atualizado_em_utc"):
                        dossie["atualizado_em_utc"] = lido["atualizado_em_utc"]
                    if isinstance(lido.get("secoes"), dict):
                        secoes_saida.update(lido["secoes"])
                    for k, v in lido.items():
                        if k not in {"secoes", "cliente", "atualizado_em_utc"} and isinstance(v, dict):
                            dossie[k] = v
                break
        except Exception:
            continue

    if mem_alvo is not None and hasattr(mem_alvo, "ler_dados"):
        try:
            consolidado_raw = mem_alvo.ler_dados("tricologia_dossie_consolidado")
            if isinstance(consolidado_raw, dict):
                if consolidado_raw.get("cliente") and not dossie.get("cliente"):
                    dossie["cliente"] = consolidado_raw["cliente"]
                if isinstance(consolidado_raw.get("secoes"), dict):
                    for chave_sec, valor_sec in consolidado_raw["secoes"].items():
                        if isinstance(valor_sec, dict) and chave_sec not in secoes_saida:
                            secoes_saida[chave_sec] = valor_sec
        except Exception:
            pass

        for chave_canonica, aliases in MAPA_SECOES_TRICOLOGIA.items():
            if chave_canonica in secoes_saida and isinstance(secoes_saida[chave_canonica], dict):
                continue
            for alias in aliases:
                candidato = None
                try:
                    if cliente:
                        candidato = mem_alvo.ler_dados(f"tricologia_{alias}_{cliente}")
                    if candidato is None:
                        candidato = mem_alvo.ler_dados(f"tricologia_{alias}")
                except Exception:
                    candidato = None
                if isinstance(candidato, dict):
                    secoes_saida[chave_canonica] = candidato
                    break

    for chave_canonica, valor_sec in secoes_saida.items():
        if isinstance(valor_sec, dict):
            dossie[chave_canonica] = valor_sec

    dossie["secoes"] = secoes_saida
    if cliente:
        dossie["cliente"] = cliente
    elif not dossie.get("cliente"):
        dossie["cliente"] = "Cliente UHNW"
    return dossie
# === [/REPARADOR TTC] PONTE LEITURA MEMORIA TRICOLOGIA ===


TEXTOS_TRICOLOGIA = {
    "PT": {
        "marca_agua": "MONACO PRIVATE BANKING • TRICHOLOGY APEX",
        "rodape_class": "Classificado • Documento de Salvaguarda Folicular, Acidez Celular e Conversão UHNW",
        "rodape_seal": "MONACO SEAL • PÁGINA {pagina} • SHA-256 SECURED",
        "emp_top": "TRICHOLOGY & FINANCIAL LONGEVITY DIVISION",
        "titulo_topo": "ULTRA-ADVANCED TRICHOLOGY REPORT & STOCHASTIC COLLAPSE MATRIX ({segment})",
        "meta_emissao": "Emissão:",
        "meta_titular": "Titular:",
        "meta_horizonte": "Horizonte:",
        "meta_operador": "Operador:",
        "anos_label": "Anos",
        "sumario_titulo": "00 // SUMÁRIO EXECUTIVO APEX: DIAGNÓSTICO E PROJEÇÃO DE VALUATION",
        "sumario_texto": (
            "O presente dossiê consolida a varredura optoeletrônica, termografia de alta precisão e modelagem de risco folicular na <b>{company}</b>. "
            "Através de algoritmos determinísticos baseados na Lei de Snell e no fator de estresse sistêmico para o setor de <b>{segment}</b> (Fator Cortisol: {cortisol}), "
            "o sistema projeta a 'Linha do Tempo do Medo', o Custo de Inação (COA) e a neutralização absoluta da corrosão biológica."
        ),
        "sec1_titulo": "01 // LINHA DO TEMPO DO MEDO: PROJEÇÃO DE COLAPSO FOLICULAR E ALOCAÇÃO",
        "h_mes": "Horizonte",
        "h_densidade": "Densidade Projetada",
        "h_status_colapso": "Status Biológico do Tecido",
        "h_investimento": "Investimento (€) - NAD+/VEGF",
        "sec2_titulo": "02 // ESPECTROMETRIA, TERMOGRAFIA ÓPTICA & CONDUTAS DISRUPTIVAS",
        "h_indicador": "Indicador / Módulo",
        "h_valor": "Valor / Parâmetro",
        "h_diretriz": "Diretriz Clínica & Análise Estrutural",
        "opt_refracao": "Índice de Refração (n)",
        "desc_refracao": "Desvio angular real da luz na fibra capilar (Lei de Snell).",
        "opt_miniaturizacao": "Taxa de Miniaturização",
        "desc_miniaturizacao": "Nível acumulado projetado para o horizonte de {horizon} anos.",
        "opt_termografia": "Termografia Perifolicular",
        "opt_detox": "Fator Detox & Poluição",
        "opt_cronobio": "Cronobiologia Circadiana",
        "val_sincronizado": "Sincronizado Apex",
        "opt_clima": "Fator Climático Regional",
        "umid_label": "Umid",
        "sec3_titulo": "03 // GOVERNANÇA TÉCNICA E CADEIA DE CUSTÓDIA SHA-256",
        "ass_sha": "Assinatura de Integridade SHA-256:",
        "dir_soberana": "Diretriz Soberana:",
        "auditoria_nota": "Auditoria Biomédica (Monaco Standards & European Compliance): Indicadores ajustados ao fator de estresse macroeconômico ({cortisol}) para o horizonte de {horizon} anos.",
        "sec4_trico_titulo": "04 // MATRIZ NUTRACÊUTICA HIPER-PERSONALIZADA DINÂMICA",
        "t4_tr_l1_nome": "Fator de Crescimento VEGF Celular",
        "t4_tr_l1_st": "Urgente",
        "t4_tr_l1_desc": "Estímulo direto à neovascularização profunda periférica para reverter a miniaturização.",
        "t4_tr_l2_nome": "Precursores de NAD+",
        "t4_tr_l2_desc": "Restauração da energia mitocondrial do bulbo e bloqueio ativo do envelhecimento celular.",
        "t4_tr_l3_nome": "Bloqueador Enzimático 5-Alfa-Redutase",
        "t4_tr_l3_st": "Sincronizado",
        "t4_tr_l3_desc": "Proteção sistêmica e tópica contra a degradação induzida por DHT sob estresse oxidativo.",
        "sec5_trico_titulo": "05 // ENGENHARIA DE PRECIFICAÇÃO E ALOCAÇÃO DO ECOSSISTEMA APEX",
        "t5_tr_l1_nome": "Módulo I: Estabilização e Detox Urbano",
        "t5_tr_l1_desc": "Remoção de metais pesados e readequação do microambiente folicular imediato.",
        "t5_tr_l2_nome": "Módulo II: Blindagem Ativa Platinum (Recomendado)",
        "t5_tr_l2_desc": "Protocolo completo de terapia celular regenerativa + engenharia circadiana.",
        "t5_tr_l3_nome": "Módulo III: Governança Perpétua Suíça",
        "t5_tr_l3_desc": "Monitoramento preditivo 24/7 com inteligência artificial e recalibração.",
        "sec6_trico_titulo": "06 // DEPRECIAÇÃO REPUTACIONAL E COA (CUSTO DE INAÇÃO EM TEMPO REAL)",
        "t6_l1_nome": "Erosão Volátil de Imagem (24M)",
        "t6_l1_desc": "Prejuízo intangível projetado sobre o valor de mercado do executivo.",
        "t6_l2_nome": "Custo de Inação Mensal (COA)",
        "t6_l2_desc": "O custo financeiro real de adiar a decisão de blindagem por 30 dias.",
        "t6_l3_nome": "Taxa de Retorno de Ativo (ROI)",
        "t6_l3_desc": "Retorno líquido sobre o capital aplicado em relação à perda mitigada.",
        "sec7_trico_titulo": "07 // A FALÁCIA DO IMPLANTE E A DISTORÇÃO FACIAL",
        "t7_tr_l1_nome": "Inviabilidade Biológica do Transplante",
        "t7_tr_l1_st": "Inviável Biologicamente",
        "t7_tr_l1_desc": "Redistribuição cirúrgica sobre derme fibrótica sem ancoragem nativa ou suporte vascular.",
        "t7_tr_l2_nome": "Índice de Distorção de Feição",
        "t7_tr_l2_st": "Distorção Feição -24%",
        "t7_tr_l2_desc": "Distorção geométrica e envelhecimento visual permanente (-24% harmonia visagista).",
        "t7_tr_l3_nome": "Custo Oculto de Downtime",
        "t7_tr_l3_st": "Downtime Crítico",
        "t7_tr_l3_desc": "Exposição pública e prejuízo reputacional durante o período de cicatrização visível.",
        "sec8_trico_titulo": "08 // ACIDEZ CELULAR E MOTOR DE BIOGÊMEOS (LINHA DO TEMPO)",
        "t8_tr_l1_nome": "Colapso por Desidratação Crônica",
        "t8_tr_l1_st": "Desidratação Severa",
        "t8_tr_l1_desc": "Erosão contínua da umidade interna e destruição absoluta da elasticidade da fibra.",
        "t8_tr_l2_nome": "Estabilização Hidráulica Platinum",
        "t8_tr_l2_st": "Platinum Ativa",
        "t8_tr_l2_desc": "Contraponto imediato com protocolo de alta retenção hídrica e blindagem molecular.",
        "t8_tr_l3_nome": "Congelamento de Simulação de Risco",
        "t8_tr_l3_st": "Risco Congelado C2",
        "t8_tr_l3_desc": "Travamento do terminal C2 na progressão da necrose perifolicular ácida.",
        "sec9_trico_titulo": "09 // GATEWAY DE CONFORMIDADE FINANCEIRA E SALVAGUARDA",
        "t9_tr_l1_nome": "Gateway de Aporte Executivo",
        "t9_tr_l1_st": "Gateway Seguro",
        "t9_tr_l1_desc": "Canal criptografado de alta conformidade para liquidação imediata do protocolo.",
        "t9_tr_l2_nome": "Aporte de Salvaguarda Biológica",
        "t9_tr_l2_desc": "Investimento apresentado como decisão matemática irrelevante frente ao patrimônio protegido.",
        "t9_tr_l3_nome": "Validação SHA-256",
        "t9_tr_l3_st": "SHA-256",
        "t9_tr_l3_desc": "Segurança máxima e imutabilidade no registro do contrato de blindagem.",
        "sec10_trico_titulo": "10 // O XEQUE-MATE PSICOLÓGICO: INTERROMPER CORROSÃO (CTA)",
        "t10_tr_l1_nome": "Botão de Interromper Corrosão",
        "t10_tr_l1_st": "INTERROMPER CORROSÃO",
        "t10_tr_l1_desc": "Comando direto que elimina a sensação de custo e ativa a urgência implacável de defesa.",
        "t10_tr_l2_nome": "Eliminação de Ineficiência Financeira",
        "t10_tr_l2_st": "Zero Ineficiência",
        "t10_tr_l2_desc": "O cliente percebe que se sente financeiramente estúpido se não autorizar a transação.",
        "t10_tr_l3_nome": "Homologação e Autorização Imediata",
        "t10_tr_l3_st": "Homologado",
        "t10_tr_l3_desc": "Assinatura instantânea do protocolo executivo na mesa do decisor sem hesitação.",
        "anexo_titulo": "[ SEÇÃO II: ANEXO DE INTELIGÊNCIA DINÂMICA & PROTOCOLO NMN / PEPTÍDEOS ]",
        "laudo_col_param": "PARÂMETRO / SEÇÃO CLÍNICA",
        "laudo_col_parecer": "DIAGNÓSTICO E PARECER TÉCNICO UHNW",
        "laudo_status_homologado": "STATUS: HOMOLOGADO // APEX UHNW",
        "laudo_diag_clinico": "DIAGNÓSTICO CLÍNICO",
        "laudo_parecer_tec": "PARECER TÉCNICO",
    },
    "EN": {
        "marca_agua": "MONACO PRIVATE BANKING • TRICHOLOGY APEX",
        "rodape_class": "Classified • Follicular Safeguard, Cellular Acidity & UHNW Conversion Document",
        "rodape_seal": "MONACO SEAL • PAGE {pagina} • SHA-256 SECURED",
        "emp_top": "TRICHOLOGY & LONGEVITY DIVISION",
        "titulo_topo": "ULTRA-ADVANCED TRICHOLOGY REPORT & STOCHASTIC COLLAPSE MATRIX ({segment})",
        "meta_emissao": "Issuance:",
        "meta_titular": "Principal:",
        "meta_horizonte": "Horizon:",
        "meta_operador": "Operator:",
        "anos_label": "Years",
        "sumario_titulo": "00 // APEX EXECUTIVE SUMMARY: DIAGNOSTIC & VALUATION PROJECTION",
        "sumario_texto": (
            "This dossier consolidates optoelectronic scanning, high-precision thermography, and follicular risk modeling at <b>{company}</b>. "
            "Through deterministic algorithms based on Snell's Law and systemic stress for the <b>{segment}</b> sector (Cortisol Factor: {cortisol}), "
            "the system projects the 'Timeline of Fear', Cost of Inaction (COA), and absolute biological neutralization."
        ),
        "sec1_titulo": "01 // TIMELINE OF FEAR: FOLLICULAR COLLAPSE PROJECTION & ALLOCATION",
        "h_mes": "Horizon",
        "h_densidade": "Projected Density",
        "h_status_colapso": "Biological Tissue Status",
        "h_investimento": "Euros (€) - NAD+/VEGF Protocol",
        "sec2_titulo": "02 // SPECTROMETRY, OPTICAL THERMOGRAPHY & DISRUPTIVE CONDUCTS",
        "h_indicador": "Indicator / Module",
        "h_valor": "Value / Parameter",
        "h_diretriz": "Clinical Guideline & Structural Analysis",
        "opt_refracao": "Refractive Index (n)",
        "desc_refracao": "Real angular deviation of light in the hair fiber (Snell's Law).",
        "opt_miniaturizacao": "Miniaturization Rate",
        "desc_miniaturizacao": "Accumulated level projected for the {horizon}-year horizon.",
        "opt_termografia": "Perifollicular Thermography",
        "opt_detox": "Detox Factor & Pollution",
        "opt_cronobio": "Circadian Chronobiology",
        "val_sincronizado": "Apex Synchronized",
        "opt_clima": "Regional Climatic Factor",
        "umid_label": "Humid",
        "sec3_titulo": "03 // TECHNICAL GOVERNANCE AND SHA-256 CUSTODY CHAIN",
        "ass_sha": "Integrity Signature SHA-256:",
        "dir_soberana": "Sovereign Guideline:",
        "auditoria_nota": "Biomedical Audit (Monaco Standards & European Compliance): Indicators adjusted to the macroeconomic stress factor ({cortisol}) for the {horizon}-year horizon.",
        "sec4_trico_titulo": "04 // DYNAMIC HYPER-PERSONALIZED NUTRACEUTICAL MATRIX",
        "t4_tr_l1_nome": "Cellular VEGF Growth Factor",
        "t4_tr_l1_st": "Urgent",
        "t4_tr_l1_desc": "Direct stimulus to deep peripheral neovascularization to reverse miniaturization.",
        "t4_tr_l2_nome": "NAD+ Precursors",
        "t4_tr_l2_desc": "Restoration of bulb mitochondrial energy and active blocking of cellular aging.",
        "t4_tr_l3_nome": "5-Alpha-Redutase Enzymatic Blocker",
        "t4_tr_l3_st": "Synchronized",
        "t4_tr_l3_desc": "Systemic and topical protection against DHT-induced degradation under oxidative stress.",
        "sec5_trico_titulo": "05 // PRICING ENGINEERING & APEX ECOSYSTEM ALLOCATION",
        "t5_tr_l1_nome": "Module I: Stabilization & Urban Detox",
        "t5_tr_l1_desc": "Heavy metal removal and immediate follicular microenvironment readjustment.",
        "t5_tr_l2_nome": "Module II: Active Platinum Shielding (Recommended)",
        "t5_tr_l2_desc": "Complete protocol of regenerative cell therapy + personalized circadian engineering.",
        "t5_tr_l3_nome": "Module III: Swiss Perpetual Governance",
        "t5_tr_l3_desc": "24/7 predictive AI monitoring with semi-annual recalibration.",
        "sec6_trico_titulo": "06 // REPUTATIONAL DEPRECIATION & COA (COST OF INACTION IN REAL TIME)",
        "t6_l1_nome": "Volatile Image Erosion (24M)",
        "t6_l1_desc": "Projected intangible loss on executive market valuation.",
        "t6_l2_nome": "Monthly Cost of Inaction (COA)",
        "t6_l2_desc": "Real financial cost of postponing the shielding decision by 30 days.",
        "t6_l3_nome": "Asset Return Rate (ROI)",
        "t6_l3_desc": "Net return on deployed capital relative to mitigated loss.",
        "sec7_trico_titulo": "07 // THE TRANSPLANT FALLACY & FACIAL DISTORTION MATHEMATICS",
        "t7_tr_l1_nome": "Transplant Biological Infeasibility",
        "t7_tr_l1_st": "Biologically Infeasible",
        "t7_tr_l1_desc": "Surgical redistribution over fibrotic dermis without native anchorage or vascular support.",
        "t7_tr_l2_nome": "Feature Distortion Index",
        "t7_tr_l2_st": "Feature Distortion -24%",
        "t7_tr_l2_desc": "Geometric distortion and permanent visual aging (-24% visagist harmony).",
        "t7_tr_l3_nome": "Hidden Downtime Cost",
        "t7_tr_l3_st": "Critical Downtime",
        "t7_tr_l3_desc": "Public exposure and reputational damage during the visible healing period.",
        "sec8_trico_titulo": "08 // CELLULAR ACIDITY & BIOGEMINI ENGINE (TIMELINE)",
        "t8_tr_l1_nome": "Chronic Dehydration Collapse",
        "t8_tr_l1_st": "Severe Dehydration",
        "t8_tr_l1_desc": "Continuous internal moisture erosion and absolute destruction of fiber elasticity.",
        "t8_tr_l2_nome": "Platinum Hydraulic Stabilization",
        "t8_tr_l2_st": "Platinum Active",
        "t8_tr_l2_desc": "Immediate counterpoint with high water retention and molecular shielding protocol.",
        "t8_tr_l3_nome": "Risk Simulation Freezing",
        "t8_tr_l3_st": "Risk Frozen C2",
        "t8_tr_l3_desc": "C2 terminal lock on the progression of acidic perifollicular necrosis.",
        "sec9_trico_titulo": "09 // FINANCIAL COMPLIANCE GATEWAY & BIOLOGICAL SAFEGUARD",
        "t9_tr_l1_nome": "Executive Contribution Gateway",
        "t9_tr_l1_st": "Secure Gateway",
        "t9_tr_l1_desc": "Encrypted high-compliance channel for immediate protocol settlement.",
        "t9_tr_l2_nome": "Biological Safeguard Contribution",
        "t9_tr_l2_desc": "Investment presented as irrelevant math compared to protected equity value.",
        "t9_tr_l3_nome": "SHA-256 Validation",
        "t9_tr_l3_st": "SHA-256",
        "t9_tr_l3_desc": "Maximum security and immutability in shielding contract registration.",
        "sec10_trico_titulo": "10 // THE PSYCHOLOGICAL CHECKMATE: STOP CORROSION (CTA)",
        "t10_tr_l1_nome": "Stop Corrosion Button",
        "t10_tr_l1_st": "STOP CORROSION",
        "t10_tr_l1_desc": "Direct command eliminating cost perception and activating relentless defense urgency.",
        "t10_tr_l2_nome": "Financial Inefficiency Elimination",
        "t10_tr_l2_st": "Zero Inefficiency",
        "t10_tr_l2_desc": "Client realizes they feel financially inefficient if they do not authorize immediately.",
        "t10_tr_l3_nome": "Immediate Homologation & Authorization",
        "t10_tr_l3_st": "Homologated",
        "t10_tr_l3_desc": "Instantaneous signature of the executive protocol on the decision-maker's desk.",
        "anexo_titulo": "[ SECTION II: DYNAMIC INTELLIGENCE ANNEX & NMN / PEPTIDES PROTOCOL ]",
        "laudo_col_param": "PARAMETER / CLINICAL SECTION",
        "laudo_col_parecer": "UHNW DIAGNOSIS AND TECHNICAL OPINION",
        "laudo_status_homologado": "STATUS: HOMOLOGATED // APEX UHNW",
        "laudo_diag_clinico": "CLINICAL DIAGNOSIS",
        "laudo_parecer_tec": "TECHNICAL OPINION",
    },
}


class SovereignSecureCanvas(canvas.Canvas):
    """Canvas de Alta Segurança Atuarial com Marca d'Água Executiva Sutil e Rodapé SHA-256."""

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
        lang_atual = getattr(self, "_trico_lang", "PT")
        txt = TEXTOS_TRICOLOGIA.get(lang_atual, TEXTOS_TRICOLOGIA["PT"])

        self.saveState()
        self.setFont("Helvetica-Bold", 36)
        self.setFillColor(colors.HexColor("#B8860B"), alpha=0.03)
        self.translate(A4[0] / 2.0, A4[1] / 2.0)
        self.rotate(35)
        self.drawCentredString(0, 0, txt["marca_agua"])
        self.restoreState()

        self.saveState()
        self.setStrokeColor(colors.HexColor("#B8860B"))
        self.setLineWidth(0.75)

        self.line(30, 40, A4[0] - 30, 40)

        self.setFont("Helvetica", 6.5)
        self.setFillColor(colors.HexColor("#0A1128"))
        pagina_atual = self._pageNumber

        self.drawString(30, 26, txt["rodape_class"])
        self.drawRightString(A4[0] - 30, 26, txt["rodape_seal"].format(pagina=pagina_atual))
        self.restoreState()


class C2UltraAdvancedTrichologyEngine:
    """
    Motor Unificado de Telemetria Capilar, Projeção de Risco, Estimativa de COA e Dossiê PDF.
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
        net_worth_eur: float = 2500000.0,
        fator_estresse_biologico: Optional[float] = None,
        telemetria: Optional[Dict[str, Any]] = None,
        lang: str = "PT",
        *args,
        **kwargs,
    ) -> None:
        self.telemetria_externa = telemetria or {}

        self.ceo = (
            ceo_name
            or self.telemetria_externa.get("nome_cliente")
            or self.telemetria_externa.get("nome")
            or "Cliente UHNW"
        )
        self.company = company_name
        self.segment = market_segment
        self.horizon = max(1, int(horizon_years))
        self.operador = operador
        self.densidade_fios = float(densidade_fios_estimada)
        self.miniaturizacao = max(0.0, float(miniaturizacao_pct))
        self.umidade_ar = max(0.0, min(100.0, float(umidade_ar_pct)))
        self.temp_externa = float(temp_externa_c)
        self.net_worth = max(0.0, float(net_worth_eur))
        self.custo_setup = 15000.0

        self.lang = lang.upper() if lang and isinstance(lang, str) else "PT"
        if self.lang not in TEXTOS_TRICOLOGIA:
            self.lang = "PT"

        self.emissao = datetime.datetime.now(datetime.timezone.utc).strftime("%d/%m/%Y às %H:%M:%S UTC")

        dados_fadiga_memoria = memoria.ler_dados("dados_fadiga") or {}
        if fator_estresse_biologico is not None:
            self.estresse = min(1.0, max(0.0, float(fator_estresse_biologico)))
        else:
            score_sensor = (
                dados_fadiga_memoria.get("score_fadiga", 72.0)
                if isinstance(dados_fadiga_memoria, dict)
                else 72.0
            )
            self.estresse = min(1.0, max(0.0, float(score_sensor) / 100.0))

        if frame_capturado_rgb is not None:
            (
                self.temp_perifolicular,
                self.saturacao_poluicao,
                self.pico_cortisol_dinamico,
            ) = self._analisar_biometria_optica(frame_capturado_rgb)
        else:
            self.temp_perifolicular = round(31.5 + (self.temp_externa * 0.08) + (self.estresse * 0.5), 1)
            if self.umidade_ar > 80 or self.estresse >= 0.72:
                self.saturacao_poluicao = "Crítica (Urbana)"
            elif self.umidade_ar >= 55 or self.estresse >= 0.45:
                self.saturacao_poluicao = "Moderada (Saturação sebácea)"
            else:
                self.saturacao_poluicao = "Baixa (Microambiente controlado)"
            self.pico_cortisol_dinamico = "Noite"

        if any(kw in market_segment.lower() for kw in ["tecnologia", "varejo", "alimentos", "inovação", "financeiro"]):
            base_setor = 1.38
        else:
            base_setor = 1.00

        # Ajusta o fator de estresse/cortisol também ao estresse informado e à miniaturização
        ajuste_estresse = 0.85 + (self.estresse * 0.35) + min(0.25, self.miniaturizacao / 120.0)
        self.fator_cortisol = round(base_setor * (ajuste_estresse / 1.10), 2)

        raw_analise = (
            self.telemetria_externa.get("analise_gemini_trico", "")
            or self.telemetria_externa.get("parecer_tricologia", "")
        )
        if not raw_analise and hasattr(memoria, "ler_dados"):
            raw_analise = (
                memoria.ler_dados("analise_gemini_trico")
                or memoria.ler_dados("parecer_tricologia")
                or memoria.ler_dados("analise_gemini")
                or ""
            )

        texto_analise = str(raw_analise).strip()
        if texto_analise.startswith("```"):
            linhas_analise = texto_analise.split("\n")
            if len(linhas_analise) > 2:
                texto_analise = "\n".join(
                    linhas_analise[1:-1] if linhas_analise[-1].strip() == "```" else linhas_analise[1:]
                )
        self.analise_llm = texto_analise.strip()

        # === [REPARADOR TTC] CRUZAMENTO MEMORIA INIT ===
        _cliente_mem_alvo = ceo_name or self.telemetria_externa.get("nome_cliente") or self.telemetria_externa.get("nome")
        self.dossie_memoria = puxar_dados_tricologia_memoria(
            cliente=_cliente_mem_alvo,
            dados_iniciais=self.telemetria_externa,
            memoria_instancia=memoria,
        )
        _secoes_mem = self.dossie_memoria.get("secoes") if isinstance(self.dossie_memoria.get("secoes"), dict) else {}
        if not ceo_name and not self.telemetria_externa.get("nome_cliente") and not self.telemetria_externa.get("nome"):
            if self.dossie_memoria.get("cliente") and self.dossie_memoria.get("cliente") != "Cliente UHNW":
                self.ceo = self.dossie_memoria["cliente"]
        _dens_mem = _ttc_buscar_numero(_secoes_mem, ("densidade_fios_estimada", "densidade_fios", "densidade_cm2", "densidade"))
        _mini_mem = _ttc_buscar_numero(_secoes_mem, ("miniaturizacao_pct", "taxa_miniaturizacao", "miniaturizacao"))
        _umid_mem = _ttc_buscar_numero(_secoes_mem, ("umidade_ar_pct", "umidade_ar", "umidade_relativa", "umidade"))
        _temp_mem = _ttc_buscar_numero(_secoes_mem, ("temp_externa_c", "temperatura_externa", "temperatura_c", "temperatura"))
        if _dens_mem is not None and abs(self.densidade_fios - 130.0) < 1e-6:
            self.densidade_fios = float(_dens_mem)
        if _mini_mem is not None and abs(self.miniaturizacao - 22.5) < 1e-6:
            self.miniaturizacao = max(0.0, float(_mini_mem))
        if _umid_mem is not None and abs(self.umidade_ar - 85.0) < 1e-6:
            self.umidade_ar = max(0.0, min(100.0, float(_umid_mem)))
        if _temp_mem is not None and abs(self.temp_externa - 32.0) < 1e-6:
            self.temp_externa = float(_temp_mem)
        if not self.analise_llm and _secoes_mem:
            _linhas_sec = []
            for _nsec, _csec in _secoes_mem.items():
                if isinstance(_csec, dict) and _csec:
                    _itens = [f"{k}: {v}" for k, v in list(_csec.items())[:4] if v is not None and v != ""]
                    if _itens:
                        _linhas_sec.append(f"• {_nsec}: " + " | ".join(_itens))
            if _linhas_sec:
                self.analise_llm = "\n".join(_linhas_sec)
        # === [/REPARADOR TTC] CRUZAMENTO MEMORIA INIT ===

    def formatar_moeda_eur(self, valor: float) -> str:
        return f"€ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def _analisar_biometria_optica(self, frame) -> Tuple[float, str, str]:
        try:
            img_float = np.asarray(frame, dtype=np.float32)
            canal_r = float(np.mean(img_float[:, :, 2]))
            canal_g = float(np.mean(img_float[:, :, 1]))

            temp_calculada = 33.0 + (canal_r / (canal_g + 1e-5)) * 1.5
            temp_calculada = round(min(max(temp_calculada, 32.5), 36.5), 1)

            luminancia = float(
                np.mean(0.299 * img_float[:, :, 2] + 0.587 * img_float[:, :, 1] + 0.114 * img_float[:, :, 0])
            )
            if luminancia < 90:
                poluicao = "Crítica (Urbana com sujidade particulada)"
            elif luminancia < 120:
                poluicao = "Moderada (Saturação sebácea)"
            else:
                poluicao = "Baixa (Microambiente limpo)"
        except Exception:
            temp_calculada = 34.2
            poluicao = "Moderada (Fallback ativado)"

        hora_atual = datetime.datetime.now(datetime.timezone.utc).hour
        if self.lang == "EN":
            if 5 <= hora_atual < 12:
                cortisol_horario = "Morning (High permeability & VEGF absorption)"
            elif 12 <= hora_atual < 18:
                cortisol_horario = "Afternoon (Metabolic stabilization phase)"
            else:
                cortisol_horario = "Night (Mitochondrial peak & critical DHT window)"
        else:
            if 5 <= hora_atual < 12:
                cortisol_horario = "Manhã (Janela de alta permeabilidade e VEGF)"
            elif 12 <= hora_atual < 18:
                cortisol_horario = "Tarde (Estabilização metabólica folicular)"
            else:
                cortisol_horario = "Noite (Pico mitocondrial e janela crítica DHT)"

        return temp_calculada, poluicao, cortisol_horario

    def calcular_telemetria_capilar(self) -> Dict[str, Any]:
        fluxo_sanguineo_base = 12.0
        resistencia_vascular_base = 10.01
        indice_refracao_base = 1.54

        fator_termico = 1.0 + max(-0.08, min(0.12, (self.temp_perifolicular - 34.2) * 0.04))
        fluxo_calculado = (fluxo_sanguineo_base / (max(0.5, self.fator_cortisol) ** 0.5)) * fator_termico
        resistencia_calculada = resistencia_vascular_base * self.fator_cortisol * (1.0 + (self.miniaturizacao / 250.0))
        desvio_optico_snell = indice_refracao_base * (1.0 + (0.012 * self.fator_cortisol))

        taxa_miniaturizacao = self.miniaturizacao * (self.horizon / 10.0) * (self.fator_cortisol / 1.25)
        if taxa_miniaturizacao > 45.0:
            taxa_miniaturizacao = 45.0

        if self.lang == "EN":
            if self.temp_perifolicular < 34.5:
                alerta_termico = f"Thermal Alert ({self.temp_perifolicular}°C): Perifollicular vasoconstriction. Use 830nm LED."
            else:
                alerta_termico = f"Stable Thermal ({self.temp_perifolicular}°C): Microcirculation optimized."

            if any(k in self.saturacao_poluicao for k in ["Crítica", "Moderada", "Critical", "Moderate"]):
                fator_detox = f"Saturation [{self.saturacao_poluicao}]: Oxidative stress. Fractional Plasma sweep required."
            else:
                fator_detox = f"Optical Saturation: {self.saturacao_poluicao}."

            if "Noite" in self.pico_cortisol_dinamico or "Night" in self.pico_cortisol_dinamico:
                cronograma_horario = f"Chronobiology [{self.pico_cortisol_dinamico}]: Apply DHT blocker at 10:30 PM."
            else:
                cronograma_horario = f"Chronobiology [{self.pico_cortisol_dinamico}]: Active daytime sync."

            if self.umidade_ar > 80:
                alerta_clima = f"Climatic (Humidity: {self.umidade_ar}%): High humidity, risk of dysbiosis."
            elif self.umidade_ar < 45:
                alerta_clima = f"Climatic (Humidity: {self.umidade_ar}%): Low humidity, hydration occlusion advised."
            else:
                alerta_clima = f"Climatic (Humidity: {self.umidade_ar}%): Balanced ambient humidity."

            if self.fator_cortisol > 1.2 or taxa_miniaturizacao >= 25.0:
                status_clinico = "PROGRESSIVE PERIPHERAL BULBAR ISCHEMIA"
                vulnerabilidade_texto = (
                    f"Follicular atrophy risk in {self.segment} ({round(taxa_miniaturizacao, 1)}%). "
                    f"Resistance: {round(resistencia_calculada, 2)} dyn·s/cm⁵."
                )
                diretriz_tatica = f"Protocol activation for {self.ceo} recommended to support hemoperfusion."
            else:
                status_clinico = "VASCULAR PRESERVATION MAINTENANCE"
                vulnerabilidade_texto = "Exogenous stress within controlled parameters."
                diretriz_tatica = "Standard preventive spectrophotometry maintenance."
        else:
            if self.temp_perifolicular < 34.5:
                alerta_termico = f"Alerta Térmico ({self.temp_perifolicular}°C): Vasoconstrição. Obrigatório LED 830nm."
            else:
                alerta_termico = f"Perfil Estável ({self.temp_perifolicular}°C): Microcirculação otimizada."

            if "Crítica" in self.saturacao_poluicao or "Moderada" in self.saturacao_poluicao:
                fator_detox = f"Saturação [{self.saturacao_poluicao}]: Estresse oxidativo. Requer Plasma Fracionado."
            else:
                fator_detox = f"Saturação Óptica: {self.saturacao_poluicao}."

            if "Noite" in self.pico_cortisol_dinamico:
                cronograma_horario = f"Cronobiologia [{self.pico_cortisol_dinamico}]: Aplicar bloqueador de DHT às 22:30."
            else:
                cronograma_horario = f"Cronobiologia [{self.pico_cortisol_dinamico}]: Sincronização diurna."

            if self.umidade_ar > 80:
                alerta_clima = f"Clima (Umidade: {self.umidade_ar}%): Risco de disbiose. Antisséptico obrigatório."
            elif self.umidade_ar < 45:
                alerta_clima = f"Clima (Umidade: {self.umidade_ar}%): Ambiente seco. Oclusão hídrica recomendada."
            else:
                alerta_clima = f"Clima (Umidade: {self.umidade_ar}%): Umidade em faixa moderada."

            if self.fator_cortisol > 1.2 or taxa_miniaturizacao >= 25.0:
                status_clinico = "ISQUEMIA BULBAR PERIFÉRICA EM PROGRESSÃO"
                vulnerabilidade_texto = (
                    f"Atrofia folicular no setor de {self.segment} (miniaturização {round(taxa_miniaturizacao, 1)}%). "
                    f"Resistência: {round(resistencia_calculada, 2)} dyn·s/cm⁵."
                )
                diretriz_tatica = f"Ativação de protocolo para estabilizar hemoperfusão de {self.ceo}."
            else:
                status_clinico = "PRESERVAÇÃO VASCULAR EM MANUTENÇÃO"
                vulnerabilidade_texto = "Estresse exógeno dentro da normalidade."
                diretriz_tatica = "Manutenção preventiva padrão de oxigenação."

        return {
            "fluxo_q": round(fluxo_calculado, 2),
            "resistencia_r": round(resistencia_calculada, 2),
            "indice_n": round(desvio_optico_snell, 3),
            "taxa_miniaturizacao": round(taxa_miniaturizacao, 2),
            "status_clinico": status_clinico,
            "vulnerabilidade_texto": vulnerabilidade_texto,
            "diretriz_tatica": diretriz_tatica,
            "alerta_termico": alerta_termico,
            "fator_detox": fator_detox,
            "cronograma_horario": cronograma_horario,
            "alerta_clima": alerta_clima,
        }

    def _calcular_linha_tempo_medo(self) -> List[Dict[str, Any]]:
        setup_base_eur = 12500.0
        fator_severidade = self.fator_cortisol * (max(1.0, self.miniaturizacao) / 20.0)

        timeline = []
        meses = [6, 12, 18, 24]
        densidade_atual = self.densidade_fios

        for m in meses:
            perda_acumulada = (m / 12.0) * 4.2 * fator_severidade
            densidade_projetada = max(35.0, densidade_atual - perda_acumulada)
            custo_protocolo_eur = setup_base_eur * (1.0 + (m / 24.0) * 0.4) * self.fator_cortisol

            if m >= 18:
                status_colapso = "Colapso Acelerado (Urgência)" if self.lang == "PT" else "Accelerated Collapse (Urgency)"
            else:
                status_colapso = "Degradação Contínua" if self.lang == "PT" else "Continuous Degradation"

            valor_formatado = f"€ {custo_protocolo_eur:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            rotulo_mes = f"Mês +{m}" if self.lang == "PT" else f"Month +{m}"

            timeline.append(
                {
                    "mes": rotulo_mes,
                    "densidade": f"{round(densidade_projetada, 1)} f/cm²",
                    "status": status_colapso,
                    "investimento": valor_formatado,
                }
            )
        return timeline

    def gerar_pdf_tricologia_avancada(
        self,
        caminho_salvamento: str = "tricologia_ultra_avancada_dossier.pdf",
        lang: Optional[str] = None,
    ) -> str:
        if lang:
            self.lang = lang.upper()
            if self.lang not in TEXTOS_TRICOLOGIA:
                self.lang = "PT"

        txt = TEXTOS_TRICOLOGIA[self.lang]
        self.emissao = datetime.datetime.now(datetime.timezone.utc).strftime("%d/%m/%Y às %H:%M:%S UTC")

        dados = self.calcular_telemetria_capilar()
        timeline_medo = self._calcular_linha_tempo_medo()

        string_base_hash = (
            f"TRICOLOGIA-10TABLES-{self.ceo}-{self.company}-{dados['fluxo_q']}-"
            f"{dados['taxa_miniaturizacao']}-{self.emissao}-{self.lang}"
        )
        hash_sha256 = hashlib.sha256(string_base_hash.encode("utf-8")).hexdigest().upper()

        os.makedirs(os.path.dirname(caminho_salvamento) if os.path.dirname(caminho_salvamento) else ".", exist_ok=True)

        doc = SimpleDocTemplate(
            caminho_salvamento,
            pagesize=A4,
            leftMargin=30,
            rightMargin=30,
            topMargin=30,
            bottomMargin=45,
        )

        MONACO_NAVY = colors.HexColor("#0A1128")
        SOVEREIGN_GOLD = colors.HexColor("#B8860B")
        EXCELENCIA_VERDE = colors.HexColor("#00875A")
        ALERTA_VERMELHO = colors.HexColor("#C0392B")
        DARK_TEXT = colors.HexColor("#1E293B")
        WHITE_BG = colors.HexColor("#FFFFFF")
        CARD_BORDER = colors.HexColor("#CBD5E1")
        TABLE_HEADER_BG = colors.HexColor("#F8FAFC")

        estilo_empresa_topo = ParagraphStyle(
            "EmpTop", fontSize=6.5, fontName="Helvetica-Bold", textColor=SOVEREIGN_GOLD, alignment=1, spaceAfter=1
        )
        estilo_titulo_topo = ParagraphStyle(
            "TitleTop",
            fontSize=10.5,
            fontName="Helvetica-Bold",
            textColor=MONACO_NAVY,
            leading=12.0,
            alignment=1,
            spaceAfter=1,
        )
        estilo_meta_topo = ParagraphStyle(
            "MetaTop", fontSize=5.5, fontName="Helvetica", textColor=colors.HexColor("#334155"), alignment=1, spaceAfter=2
        )

        estilo_sumario_titulo = ParagraphStyle(
            "SumSec", fontSize=6.5, fontName="Helvetica-Bold", textColor=MONACO_NAVY, spaceBefore=1, spaceAfter=1
        )
        estilo_sumario_texto = ParagraphStyle(
            "SumText", fontSize=5.0, fontName="Helvetica", textColor=DARK_TEXT, leading=6.5, spaceAfter=2, alignment=4
        )

        estilo_secao = ParagraphStyle(
            "SecTrico", fontSize=6.0, fontName="Helvetica-Bold", textColor=MONACO_NAVY, spaceBefore=1.5, spaceAfter=0.5
        )
        estilo_corpo = ParagraphStyle(
            "CorpoTrico", fontSize=4.5, fontName="Helvetica", textColor=DARK_TEXT, leading=5.5, spaceAfter=0.5, alignment=4
        )
        estilo_celula = ParagraphStyle(
            "CelTrico", fontSize=4.5, fontName="Helvetica-Bold", textColor=MONACO_NAVY, leading=5.5
        )
        estilo_celula_header = ParagraphStyle(
            "CelHeadTrico", fontSize=4.5, fontName="Helvetica-Bold", textColor=SOVEREIGN_GOLD, leading=5.5, alignment=1
        )
        estilo_tabela_bold = ParagraphStyle(
            "TabBold", fontSize=4.5, fontName="Helvetica-Bold", textColor=MONACO_NAVY, leading=5.5
        )
        estilo_tabela = ParagraphStyle("TabReg", fontSize=4.5, fontName="Helvetica", textColor=DARK_TEXT, leading=5.5)
        estilo_metrica_verde = ParagraphStyle(
            "CelVerde", fontSize=4.5, fontName="Helvetica-Bold", textColor=EXCELENCIA_VERDE, leading=5.5
        )
        estilo_metrica_vermelha = ParagraphStyle(
            "CelRed", fontSize=4.5, fontName="Helvetica-Bold", textColor=ALERTA_VERMELHO, leading=5.5
        )
        estilo_auditoria = ParagraphStyle(
            "NotaAuditoriaTrico",
            fontSize=3.8,
            fontName="Helvetica-Oblique",
            textColor=colors.HexColor("#64748B"),
            leading=5.0,
            alignment=1,
            spaceBefore=1.5,
        )

        ceo_nome = self.ceo.upper() if self.ceo else "CLIENTE UHNW"
        operador_nome = self.operador.upper() if self.operador else "THIERRY"

        story: List[Flowable] = []

        if self.estresse > 0.70:
            ativo_urgente = (
                "NAD+ Precursors (Ultra-Concentrated Swiss Injectable NMN Tier-1)"
                if self.lang == "EN"
                else "Precursores de NAD+ (NMN Suíço Injetável Ultra Concentrado Tier-1)"
            )
            status_fator = "CRITICAL COLLAPSE" if self.lang == "EN" else "COLAPSO CRÍTICO"
            fator_multiplicador_preco = 1.65
        else:
            ativo_urgente = (
                "NAD+ Precursors (Oral Cellular NMN Maintenance)"
                if self.lang == "EN"
                else "Precursores de NAD+ (NMN Celular Oral de Manutenção)"
            )
            status_fator = "Active Erosion" if self.lang == "EN" else "Erosão Ativa"
            fator_multiplicador_preco = 1.0

        preco_trico_standard = self.custo_setup * 0.55
        preco_trico_platinum = self.custo_setup * fator_multiplicador_preco
        preco_trico_sovereign = self.custo_setup * 3.2 * fator_multiplicador_preco

        perda_reputacional_24m = self.net_worth * 0.035 * (1.0 + self.estresse)
        custo_de_inatividade_mensal = perda_reputacional_24m / 24.0
        roi_preservacao_imagem = (
            ((perda_reputacional_24m - preco_trico_platinum) / preco_trico_platinum) * 100.0
            if preco_trico_platinum > 0
            else 0.0
        )

        story.append(Paragraph(f"{self.company.upper()} • {txt['emp_top']}", estilo_empresa_topo))
        story.append(Paragraph(txt["titulo_topo"].format(segment=self.segment), estilo_titulo_topo))
        story.append(
            Paragraph(
                f"<b>{txt['meta_emissao']}</b> {self.emissao} | <b>{txt['meta_titular']}</b> {ceo_nome} | "
                f"<b>{txt['meta_horizonte']}</b> {self.horizon} {txt['anos_label']} | <b>{txt['meta_operador']}</b> {operador_nome}",
                estilo_meta_topo,
            )
        )

        story.append(Paragraph(txt["sumario_titulo"], estilo_sumario_titulo))
        story.append(
            Paragraph(
                txt["sumario_texto"].format(company=self.company, segment=self.segment, cortisol=self.fator_cortisol),
                estilo_sumario_texto,
            )
        )
        story.append(Spacer(1, 1))

        elementos_bloco_pagina1: List[Any] = []

        elementos_bloco_pagina1.append(Paragraph(txt["sec1_titulo"], estilo_secao))
        tabela_medo_data = [
            [
                Paragraph(txt["h_mes"], estilo_celula_header),
                Paragraph(txt["h_densidade"], estilo_celula_header),
                Paragraph(txt["h_status_colapso"], estilo_celula_header),
                Paragraph(txt["h_investimento"], estilo_celula_header),
            ]
        ]
        for item in timeline_medo:
            is_colapso = ("Colapso" in item["status"]) or ("Collapse" in item["status"])
            tabela_medo_data.append(
                [
                    Paragraph(f"<b>{item['mes']}</b>", estilo_celula),
                    Paragraph(item["densidade"], estilo_metrica_vermelha if is_colapso else estilo_celula),
                    Paragraph(item["status"], estilo_corpo),
                    Paragraph(f"<b><font color='#00875A'>{item['investimento']}</font></b>", estilo_metrica_verde),
                ]
            )
        tab_medo = Table(tabela_medo_data, colWidths=[45, 75, 235, 145])
        tab_medo.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE_BG),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [TABLE_HEADER_BG, WHITE_BG]),
                    ("BOX", (0, 0), (-1, -1), 0.5, CARD_BORDER),
                    ("INNERGRID", (0, 0), (-1, -1), 0.3, CARD_BORDER),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        elementos_bloco_pagina1.append(tab_medo)
        elementos_bloco_pagina1.append(Spacer(1, 1))

        elementos_bloco_pagina1.append(Paragraph(txt["sec2_titulo"], estilo_secao))
        dados_optica = [
            [
                Paragraph(txt["h_indicador"], estilo_celula_header),
                Paragraph(txt["h_valor"], estilo_celula_header),
                Paragraph(txt["h_diretriz"], estilo_celula_header),
            ],
            [
                Paragraph(txt["opt_refracao"], estilo_celula),
                Paragraph(f"{dados['indice_n']} η", estilo_metrica_verde),
                Paragraph(txt["desc_refracao"], estilo_corpo),
            ],
            [
                Paragraph(txt["opt_miniaturizacao"], estilo_celula),
                Paragraph(f"{dados['taxa_miniaturizacao']}%", estilo_metrica_verde),
                Paragraph(txt["desc_miniaturizacao"].format(horizon=self.horizon), estilo_corpo),
            ],
            [
                Paragraph(txt["opt_termografia"], estilo_celula),
                Paragraph(f"{self.temp_perifolicular}°C", estilo_celula),
                Paragraph(dados["alerta_termico"], estilo_corpo),
            ],
            [
                Paragraph(txt["opt_detox"], estilo_celula),
                Paragraph(self.saturacao_poluicao[:15] + "...", estilo_celula),
                Paragraph(dados["fator_detox"], estilo_corpo),
            ],
            [
                Paragraph(txt["opt_cronobio"], estilo_celula),
                Paragraph(txt["val_sincronizado"], estilo_metrica_verde),
                Paragraph(dados["cronograma_horario"], estilo_corpo),
            ],
            [
                Paragraph(txt["opt_clima"], estilo_celula),
                Paragraph(f"{txt['umid_label']}: {self.umidade_ar}%", estilo_celula),
                Paragraph(dados["alerta_clima"], estilo_corpo),
            ],
        ]
        tab_optica = Table(dados_optica, colWidths=[100, 65, 335])
        tab_optica.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE_BG),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [TABLE_HEADER_BG, WHITE_BG]),
                    ("BOX", (0, 0), (-1, -1), 0.5, CARD_BORDER),
                    ("INNERGRID", (0, 0), (-1, -1), 0.3, CARD_BORDER),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        elementos_bloco_pagina1.append(tab_optica)
        elementos_bloco_pagina1.append(Spacer(1, 1))

        elementos_bloco_pagina1.append(Paragraph(txt["sec3_titulo"], estilo_secao))
        elementos_bloco_total_texto = f"""
        <b>{txt['ass_sha']}</b> <font name='Courier' size=4.0 color='#00875A'>{hash_sha256}</font><br/>
        <b>{txt['dir_soberana']}</b> <font color='#00875A'>{dados['diretriz_tatica']}</font>
        """
        elementos_bloco_pagina1.append(Paragraph(elementos_bloco_total_texto, estilo_corpo))
        elementos_bloco_pagina1.append(Spacer(1, 1))

        elementos_bloco_pagina1.append(Paragraph(txt["sec4_trico_titulo"], estilo_secao))
        t4_data = [
            [
                Paragraph(txt["t4_tr_l1_nome"], estilo_tabela_bold),
                Paragraph(txt["t4_tr_l1_st"], estilo_metrica_verde),
                Paragraph(txt["t4_tr_l1_desc"], estilo_tabela),
            ],
            [
                Paragraph(txt["t4_tr_l2_nome"], estilo_tabela_bold),
                Paragraph(
                    status_fator, estilo_metrica_verde if self.estresse <= 0.70 else estilo_metrica_vermelha
                ),
                Paragraph(ativo_urgente, estilo_tabela),
            ],
            [
                Paragraph(txt["t4_tr_l3_nome"], estilo_tabela_bold),
                Paragraph(txt["t4_tr_l3_st"], estilo_tabela),
                Paragraph(txt["t4_tr_l3_desc"], estilo_tabela),
            ],
        ]
        tab_nutra = Table(t4_data, colWidths=[120, 85, 295])
        tab_nutra.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE_BG),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [TABLE_HEADER_BG, WHITE_BG]),
                    ("BOX", (0, 0), (-1, -1), 0.5, CARD_BORDER),
                    ("INNERGRID", (0, 0), (-1, -1), 0.3, CARD_BORDER),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        elementos_bloco_pagina1.append(tab_nutra)
        elementos_bloco_pagina1.append(Spacer(1, 1))

        elementos_bloco_pagina1.append(Paragraph(txt["sec5_trico_titulo"], estilo_secao))
        t5_data = [
            [
                Paragraph(txt["t5_tr_l1_nome"], estilo_tabela_bold),
                Paragraph(self.formatar_moeda_eur(preco_trico_standard), estilo_tabela),
                Paragraph(txt["t5_tr_l1_desc"], estilo_tabela),
            ],
            [
                Paragraph(txt["t5_tr_l2_nome"], estilo_tabela_bold),
                Paragraph(self.formatar_moeda_eur(preco_trico_platinum), estilo_metrica_verde),
                Paragraph(txt["t5_tr_l2_desc"], estilo_tabela),
            ],
            [
                Paragraph(txt["t5_tr_l3_nome"], estilo_tabela_bold),
                Paragraph(self.formatar_moeda_eur(preco_trico_sovereign), estilo_tabela),
                Paragraph(txt["t5_tr_l3_desc"], estilo_tabela),
            ],
        ]
        tab_preco = Table(t5_data, colWidths=[120, 75, 305])
        tab_preco.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE_BG),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [TABLE_HEADER_BG, WHITE_BG]),
                    ("BOX", (0, 0), (-1, -1), 0.5, CARD_BORDER),
                    ("INNERGRID", (0, 0), (-1, -1), 0.3, CARD_BORDER),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        elementos_bloco_pagina1.append(tab_preco)
        elementos_bloco_pagina1.append(Spacer(1, 1))

        elementos_bloco_pagina1.append(Paragraph(txt["sec6_trico_titulo"], estilo_secao))
        sufixo_mensal = "/m"
        t6_data = [
            [
                Paragraph(txt["t6_l1_nome"], estilo_tabela_bold),
                Paragraph(self.formatar_moeda_eur(perda_reputacional_24m), estilo_tabela),
                Paragraph(txt["t6_l1_desc"], estilo_tabela),
            ],
            [
                Paragraph(txt["t6_l2_nome"], estilo_tabela_bold),
                Paragraph(
                    f"<font color='#910000'>{self.formatar_moeda_eur(custo_de_inatividade_mensal)} {sufixo_mensal}</font>",
                    estilo_tabela_bold,
                ),
                Paragraph(txt["t6_l2_desc"], estilo_tabela),
            ],
            [
                Paragraph(txt["t6_l3_nome"], estilo_tabela_bold),
                Paragraph(f"{roi_preservacao_imagem:.1f}% ROI", estilo_metrica_verde),
                Paragraph(txt["t6_l3_desc"], estilo_tabela),
            ],
        ]
        tab_coadata = Table(t6_data, colWidths=[120, 90, 290])
        tab_coadata.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE_BG),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [TABLE_HEADER_BG, WHITE_BG]),
                    ("BOX", (0, 0), (-1, -1), 0.5, CARD_BORDER),
                    ("INNERGRID", (0, 0), (-1, -1), 0.3, CARD_BORDER),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        elementos_bloco_pagina1.append(tab_coadata)
        elementos_bloco_pagina1.append(Spacer(1, 1))

        elementos_bloco_pagina1.append(Paragraph(txt["sec7_trico_titulo"], estilo_secao))
        t7_data = [
            [
                Paragraph(txt["t7_tr_l1_nome"], estilo_tabela_bold),
                Paragraph(txt["t7_tr_l1_st"], estilo_metrica_vermelha),
                Paragraph(txt["t7_tr_l1_desc"], estilo_tabela),
            ],
            [
                Paragraph(txt["t7_tr_l2_nome"], estilo_tabela_bold),
                Paragraph(txt["t7_tr_l2_st"], estilo_metrica_vermelha),
                Paragraph(txt["t7_tr_l2_desc"], estilo_tabela),
            ],
            [
                Paragraph(txt["t7_tr_l3_nome"], estilo_tabela_bold),
                Paragraph(txt["t7_tr_l3_st"], estilo_tabela),
                Paragraph(txt["t7_tr_l3_desc"], estilo_tabela),
            ],
        ]
        tab_sla = Table(t7_data, colWidths=[120, 80, 300])
        tab_sla.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE_BG),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [TABLE_HEADER_BG, WHITE_BG]),
                    ("BOX", (0, 0), (-1, -1), 0.5, CARD_BORDER),
                    ("INNERGRID", (0, 0), (-1, -1), 0.3, CARD_BORDER),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        elementos_bloco_pagina1.append(tab_sla)
        elementos_bloco_pagina1.append(Spacer(1, 1))

        elementos_bloco_pagina1.append(Paragraph(txt["sec8_trico_titulo"], estilo_secao))
        t8_data = [
            [
                Paragraph(txt["t8_tr_l1_nome"], estilo_tabela_bold),
                Paragraph(txt["t8_tr_l1_st"], estilo_metrica_vermelha),
                Paragraph(txt["t8_tr_l1_desc"], estilo_tabela),
            ],
            [
                Paragraph(txt["t8_tr_l2_nome"], estilo_tabela_bold),
                Paragraph(txt["t8_tr_l2_st"], estilo_metrica_verde),
                Paragraph(txt["t8_tr_l2_desc"], estilo_tabela),
            ],
            [
                Paragraph(txt["t8_tr_l3_nome"], estilo_tabela_bold),
                Paragraph(txt["t8_tr_l3_st"], estilo_metrica_verde),
                Paragraph(txt["t8_tr_l3_desc"], estilo_tabela),
            ],
        ]
        tab_cta = Table(t8_data, colWidths=[120, 90, 290])
        tab_cta.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE_BG),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [TABLE_HEADER_BG, WHITE_BG]),
                    ("BOX", (0, 0), (-1, -1), 0.5, CARD_BORDER),
                    ("INNERGRID", (0, 0), (-1, -1), 0.3, CARD_BORDER),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        elementos_bloco_pagina1.append(tab_cta)
        elementos_bloco_pagina1.append(Spacer(1, 1))

        elementos_bloco_pagina1.append(Paragraph(txt["sec9_trico_titulo"], estilo_secao))
        t9_data = [
            [
                Paragraph(txt["t9_tr_l1_nome"], estilo_tabela_bold),
                Paragraph(txt["t9_tr_l1_st"], estilo_metrica_verde),
                Paragraph(txt["t9_tr_l1_desc"], estilo_tabela),
            ],
            [
                Paragraph(txt["t9_tr_l2_nome"], estilo_tabela_bold),
                Paragraph(self.formatar_moeda_eur(preco_trico_platinum), estilo_metrica_verde),
                Paragraph(txt["t9_tr_l2_desc"], estilo_tabela),
            ],
            [
                Paragraph(txt["t9_tr_l3_nome"], estilo_tabela_bold),
                Paragraph(txt["t9_tr_l3_st"], estilo_tabela),
                Paragraph(txt["t9_tr_l3_desc"], estilo_tabela),
            ],
        ]
        tab_swiss = Table(t9_data, colWidths=[120, 85, 295])
        tab_swiss.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE_BG),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [TABLE_HEADER_BG, WHITE_BG]),
                    ("BOX", (0, 0), (-1, -1), 0.5, CARD_BORDER),
                    ("INNERGRID", (0, 0), (-1, -1), 0.3, CARD_BORDER),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        elementos_bloco_pagina1.append(tab_swiss)
        elementos_bloco_pagina1.append(Spacer(1, 1))

        elementos_bloco_pagina1.append(Paragraph(txt["sec10_trico_titulo"], estilo_secao))
        t10_data = [
            [
                Paragraph(txt["t10_tr_l1_nome"], estilo_tabela_bold),
                Paragraph(txt["t10_tr_l1_st"], estilo_metrica_verde),
                Paragraph(txt["t10_tr_l1_desc"], estilo_tabela),
            ],
            [
                Paragraph(txt["t10_tr_l2_nome"], estilo_tabela_bold),
                Paragraph(txt["t10_tr_l2_st"], estilo_metrica_verde),
                Paragraph(txt["t10_tr_l2_desc"], estilo_tabela),
            ],
            [
                Paragraph(txt["t10_tr_l3_nome"], estilo_tabela_bold),
                Paragraph(txt["t10_tr_l3_st"], estilo_metrica_verde),
                Paragraph(txt["t10_tr_l3_desc"], estilo_tabela),
            ],
        ]
        tab_genom = Table(t10_data, colWidths=[120, 85, 295])
        tab_genom.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE_BG),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [TABLE_HEADER_BG, WHITE_BG]),
                    ("BOX", (0, 0), (-1, -1), 0.5, CARD_BORDER),
                    ("INNERGRID", (0, 0), (-1, -1), 0.3, CARD_BORDER),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        elementos_bloco_pagina1.append(tab_genom)
        elementos_bloco_pagina1.append(Spacer(1, 1))

        elementos_bloco_pagina1.append(
            Paragraph(txt["auditoria_nota"].format(cortisol=self.fator_cortisol, horizon=self.horizon), estilo_auditoria)
        )

        bloco_mestre_pagina1 = Table([[elementos_bloco_pagina1]], colWidths=[530])
        bloco_mestre_pagina1.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE_BG),
                    ("BOX", (0, 0), (-1, -1), 1.0, CARD_BORDER),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ("LEFTPADDING", (0, 0), (-1, -1), 3),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )
        story.append(bloco_mestre_pagina1)

        if self.analise_llm:
            story.append(PageBreak())

            estilo_laudo_titulo = ParagraphStyle(
                "LaudoSec", fontSize=7.5, fontName="Helvetica-Bold", textColor=MONACO_NAVY, spaceBefore=4, spaceAfter=2
            )
            estilo_laudo_corpo = ParagraphStyle(
                "LaudoCorpo", fontSize=6.0, fontName="Helvetica", textColor=DARK_TEXT, leading=8.5, spaceAfter=2, alignment=4
            )
            estilo_laudo_header = ParagraphStyle(
                "LaudoHead", fontSize=5.5, fontName="Helvetica-Bold", textColor=SOVEREIGN_GOLD, leading=7.5, alignment=1
            )
            estilo_laudo_celula = ParagraphStyle(
                "LaudoCel", fontSize=5.5, fontName="Helvetica", textColor=DARK_TEXT, leading=7.5
            )
            estilo_laudo_verde = ParagraphStyle(
                "LaudoVerde", fontSize=5.5, fontName="Helvetica-Bold", textColor=EXCELENCIA_VERDE, leading=7.5
            )

            elementos_bloco_pagina2: List[Any] = [
                Paragraph(f"<b>{txt['anexo_titulo']}</b>", estilo_laudo_titulo),
                Spacer(1, 4),
            ]

            linhas_raw = [l.strip() for l in self.analise_llm.split("\n") if l.strip()]

            tabela_dados_laudo = [
                [
                    Paragraph(f"<b>{txt['laudo_col_param']}</b>", estilo_laudo_header),
                    Paragraph(f"<b>{txt['laudo_col_parecer']}</b>", estilo_laudo_header),
                ]
            ]

            for linha in linhas_raw[:26]:
                if linha.startswith("---") or linha.startswith("===") or linha.startswith("+"):
                    continue

                if linha.startswith("#") or (linha.startswith("**") and ":" not in linha[:15]):
                    titulo_limpo = re.sub(r"^#+\s*", "", linha).replace("**", "")
                    tabela_dados_laudo.append(
                        [
                            Paragraph(f"<b>{titulo_limpo.upper()}</b>", estilo_laudo_verde),
                            Paragraph(f"<b>{txt['laudo_status_homologado']}</b>", estilo_laudo_verde),
                        ]
                    )
                elif "•" in linha or "|" in linha or ":" in linha:
                    partes = linha.replace("•", "").split(":", 1)
                    if len(partes) == 2:
                        chave = partes[0].strip().replace("*", "")
                        valor = partes[1].strip().replace("*", "")
                        tabela_dados_laudo.append(
                            [
                                Paragraph(f"<b>{chave}</b>", estilo_laudo_celula),
                                Paragraph(valor, estilo_laudo_corpo),
                            ]
                        )
                    else:
                        tabela_dados_laudo.append(
                            [
                                Paragraph(f"<b>{txt['laudo_diag_clinico']}</b>", estilo_laudo_celula),
                                Paragraph(linha.replace("*", ""), estilo_laudo_corpo),
                            ]
                        )
                else:
                    tabela_dados_laudo.append(
                        [
                            Paragraph(f"<b>{txt['laudo_parecer_tec']}</b>", estilo_laudo_celula),
                            Paragraph(linha.replace("*", ""), estilo_laudo_corpo),
                        ]
                    )

            tab_laudo_clinico = Table(tabela_dados_laudo, colWidths=[170, 344])
            tab_laudo_clinico.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), WHITE_BG),
                        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [TABLE_HEADER_BG, WHITE_BG]),
                        ("BOX", (0, 0), (-1, -1), 0.5, CARD_BORDER),
                        ("INNERGRID", (0, 0), (-1, -1), 0.3, CARD_BORDER),
                        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                        ("LEFTPADDING", (0, 0), (-1, -1), 4),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ]
                )
            )

            elementos_bloco_pagina2.append(tab_laudo_clinico)

            bloco_mestre_pagina2 = Table([[elementos_bloco_pagina2]], colWidths=[530])
            bloco_mestre_pagina2.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), WHITE_BG),
                        ("BOX", (0, 0), (-1, -1), 1.0, CARD_BORDER),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ]
                )
            )
            story.append(bloco_mestre_pagina2)

        idioma_canvas = self.lang

        class _CanvasIdioma(SovereignSecureCanvas):
            def __init__(self, *c_args, **c_kwargs):
                super().__init__(*c_args, **c_kwargs)
                self._trico_lang = idioma_canvas

        doc.build(story, canvasmaker=_CanvasIdioma)
        print(f"[TRICOLOGIA ENGINE] PDF gerado com sucesso em: {caminho_salvamento} [SHA-256: {hash_sha256}]")
        return caminho_salvamento

    def gerar_dossie(
        self,
        caminho_salvamento: str = "tricologia_ultra_avancada_dossier.pdf",
        lang: Optional[str] = None,
        *args,
        **kwargs,
    ) -> str:
        return self.gerar_pdf_tricologia_avancada(caminho_salvamento=caminho_salvamento, lang=lang)

    def gerar_pdf(
        self,
        caminho_salvamento: str = "tricologia_ultra_avancada_dossier.pdf",
        lang: Optional[str] = None,
        *args,
        **kwargs,
    ) -> str:
        return self.gerar_pdf_tricologia_avancada(caminho_salvamento=caminho_salvamento, lang=lang)


if __name__ == "__main__":
    pasta_finais = os.path.join(ROOT_DIR, "pdfs_finais")
    os.makedirs(pasta_finais, exist_ok=True)
    caminho_teste = os.path.join(pasta_finais, "02_Dossie_Tricologia_PrivateBanking_CheckmateComplete.pdf")

    engine = C2UltraAdvancedTrichologyEngine(
        ceo_name="José Carlos Executive",
        market_segment="Tecnologia",
        net_worth_eur=4500000.0,
        lang="PT",
    )
    arquivo_gerado = engine.gerar_pdf_tricologia_avancada(caminho_teste)
    print(f"Gerador executado! Salvo em: {arquivo_gerado}")
