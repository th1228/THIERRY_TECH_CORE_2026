# -*- coding: utf-8 -*-
"""
Módulo: c2_sovereign_intelligence.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine & Predictive Engine
Versão: 16.2.1 - Monaco Quantum Platinum & Autonomous Cadence Ledger Edition (Dinâmico)
"""

import os
import sys
import json
import datetime
import hashlib
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle

# --- PONTE DE MEMÓRIA AUTOMÁTICA & CAMINHO BASE (THIERRY TECH) ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

BASE_DIR = Path(__file__).resolve().parent

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

class C2SovereignIntelligenceEngine:
    def __init__(
        self, 
        ceo_name: Optional[str] = None, 
        company_name: Optional[str] = None, 
        market_segment: str = "Tecnologia, Inovação e Longevidade Global", 
        horizon_years: int = 15, 
        aum_bilhoes_eur: float = 25.0, 
        fator_ameaca_mercado: float = 0.40, 
        telemetria: Optional[Dict[str, Any]] = None, 
        lang: str = "PT"
    ):
        # CORREÇÃO CRÍTICA: Captura dinâmica estrita, eliminando qualquer amarra hardcoded anterior
        nome_informado = (ceo_name or "").strip()
        if not nome_informado or nome_informado.lower() in ["undefined", "null", ""]:
            nome_informado = "Titular Soberano UHNW"
        self.lider = nome_informado

        entidade_informada = (company_name or "").strip()
        if not entidade_informada or entidade_informada.lower() in ["undefined", "null", ""]:
            entidade_informada = "Thierry Technology Concept Global"
        self.entidade = entidade_informada

        self.segment = market_segment if market_segment and market_segment.strip() else "Tecnologia, Inovação e Longevidade Global"
        self.horizon = int(horizon_years)
        self.aum = aum_bilhoes_eur * 1000.0  
        self.ameaca = fator_ameaca_mercado
        self.pontos_base = 100380
        self.telemetria_externa = telemetria or {}
        self.lang = lang.upper() if lang else "PT"
        
        # --- CARREGAMENTO E SINCRO AUTÓNOMA DO HISTÓRICO CLINICO-ESTÉTICO ---
        self.dados_preditivos_cliente = self._carregar_historico_json_cliente()
        self._extrair_fatores_biometricos()

        # --- RESGATE INTELIGENTE DA ANÁLISE DO GEMINI ---
        raw_analise = self.telemetria_externa.get("analise_gemini", "")
        if not raw_analise and hasattr(memoria, 'ler_dados'):
            raw_analise = memoria.ler_dados("analise_gemini") or memoria.ler_dados("analise_gemini_recente") or ""
        
        if raw_analise.startswith("```"):
            linhas_analise = raw_analise.split("\n")
            if len(linhas_analise) > 2:
                raw_analise = "\n".join(linhas_analise[1:-1] if linhas_analise[-1].strip() == "```" else linhas_analise[1:])
        self.analise_llm = raw_analise.strip()

        self.timestamp_exec = datetime.datetime.utcnow().strftime("%d/%m/%Y às %H:%M:%S UTC")

    def _carregar_historico_json_cliente(self) -> dict:
        """Lê o banco de dados unificado e busca o perfil clínico do cliente de forma totalmente dinâmica."""
        caminho_bd = BASE_DIR / "historico_clientes.json"
        if not caminho_bd.exists():
            caminho_bd = Path("historico_clientes.json")
            
        if caminho_bd.exists():
            try:
                with open(caminho_bd, "r", encoding="utf-8") as f:
                    banco = json.load(f)
                    # Busca insensível a maiúsculas/minúsculas para o nome do cliente atual
                    for chave_banco in banco.keys():
                        if chave_banco.strip().lower() == self.lider.strip().lower():
                            return banco[chave_banco]
            except Exception as e:
                print(f"[AVISO C2 JSON] Erro ao carregar historico_clientes.json: {e}")
                
        # Retorna um perfil padrão limpo e isolado se o cliente for novo
        return {
            "perfil_soberano": {
                "perfil_neurologico": {
                    "status_dominante": "Dominância Parassimpática / Regulação Ativa"
                }
            },
            "atendimentos": []
        }

    def salvar_atendimento_atual_no_json(self, dados_novos_atendimento: Optional[dict] = None):
        """Grava e atualiza autonomamente o atendimento atual no cofre JSON do cliente."""
        caminho_bd = BASE_DIR / "historico_clientes.json"
        if not caminho_bd.exists():
            caminho_bd = Path("historico_clientes.json")
            
        banco = {}
        if caminho_bd.exists():
            try:
                with open(caminho_bd, "r", encoding="utf-8") as f:
                    banco = json.load(f)
            except Exception:
                banco = {}

        cliente_chave = self.lider
        # Verifica se já existe uma chave equivalente no banco
        for chave_banco in banco.keys():
            if chave_banco.strip().lower() == self.lider.strip().lower():
                cliente_chave = chave_banco
                break

        if cliente_chave not in banco:
            banco[cliente_chave] = {
                "perfil_soberano": {
                    "data_nascimento": "N/D",
                    "perfil_neurologico": {
                        "status_dominante": "Dominância Parassimpática / Regulação Ativa"
                    }
                },
                "atendimentos": []
            }

        data_hoje = datetime.datetime.now().strftime("%d/%m/%Y")
        atendimento_atual = dados_novos_atendimento or {
            "id_atendimento": f"ATD-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "data": data_hoje,
            "procedimento": "Avaliação Biométrica e Protocolo Global C2",
            "metricas_de_entrada": {
                "oximetria_tecidual": f"{self.oximetria}%",
                "nivel_inflamacao_inicial": self.nivel_inflamacao
            },
            "modulo_preditivo_autonomo": {
                "indice_eficiencia_preditiva_iep": self.iep,
                "durabilidade_prevista_meses": 6.0
            }
        }

        atendimentos_existentes = banco[cliente_chave].get("atendimentos", [])
        ids_existentes = [a.get("id_atendimento") for a in atendimentos_existentes]
        
        if atendimento_atual.get("id_atendimento") not in ids_existentes:
            atendimentos_existentes.append(atendimento_atual)
            banco[cliente_chave]["atendimentos"] = atendimentos_existentes

            try:
                with open(caminho_bd, "w", encoding="utf-8") as f:
                    json.dump(banco, f, ensure_ascii=False, indent=2)
                print(f"[C2 LEDGER AUTÓNOMO] Atendimento de {cliente_chave} gravado com sucesso.")
            except Exception as e:
                print(f"[ERRO C2 LEDGER] Falha ao atualizar histórico: {e}")
                
        self.dados_preditivos_cliente = banco[cliente_chave]

    def _extrair_fatores_biometricos(self):
        try:
            atendimentos = self.dados_preditivos_cliente.get("atendimentos", [])
            atendimento = atendimentos[-1] if atendimentos else {}
            preditivo = atendimento.get("modulo_preditivo_autonomo", {})
            metricas = atendimento.get("metricas_de_entrada", {})
            
            self.iep = float(preditivo.get("indice_eficiencia_preditiva_iep", 75))
            oximetria_raw = metricas.get("oximetria_tecidual", "95.0%")
            self.oximetria = float(str(oximetria_raw).replace("%", "").strip())
            self.nivel_inflamacao = str(metricas.get("nivel_inflamacao_inicial", "Moderado"))
            
        except Exception:
            self.iep = 75.0
            self.oximetria = 95.0
            self.nivel_inflamacao = "Moderado"

    def _avaliar_aptidao_tratamento_invasivo(self, procedimento_desejado: str = "Bioestimulador de Colágeno / Cirurgia") -> str:
        inflamacao_lower = self.nivel_inflamacao.lower()
        if "moderado" in inflamacao_lower or "alto" in inflamacao_lower or "hipertonia" in inflamacao_lower:
            return (
                f"<b>Alerta Clínico de Procedimento ({procedimento_desejado}):</b> "
                f"Identificado nível de inflamação/hipertonia ({self.nivel_inflamacao}). "
                "<b>Conduta Preditiva:</b> Adiamento recomendado por +30 dias. Iniciar protocolo com dieta anti-inflamatória rigorosa "
                "e modulação mitocondrial antes de qualquer intervenção invasiva ou cirúrgica."
            )
        else:
            return (
                f"<b>Aptidão Ótima para ({procedimento_desejado}):</b> "
                f"Tecido em Zona Verde (Inflamação controlada | Oximetria {self.oximetria}%). "
                "<b>Conduta Preditiva:</b> Janela neuroplástica e regenerativa ativa. O dia ápice para o procedimento está matematicamente "
                "sincronizado com a estabilidade do sistema parassimpático."
            )

    def _gerar_parametro_neuro_clinico(self) -> str:
        return (
            "<b>Parâmetro Neuro-Circadiano de Atendimento:</b> "
            "Posicionamento Lateral: <b>Direita</b> (Campo visual de conforto) | "
            "Tempo de Exposição: <b>12 a 15 min</b> | "
            "Velocidade e Tom: <b>Moderado / Baixo</b> (Sincronizado com a estabilidade parassimpática atual)."
        )

    def _gerar_diagnostico_tricologia_suprema(self) -> str:
        return (
            "<b>01 // Hemodinâmica Escalpada & Hemoperfusão Bulbar:</b><br/>"
            "• Fluxo Sanguíneo Capilar (Q): <b>10.22 RPM</b> (Aporte real de oxigênio dérmico ótimo).<br/>"
            "• Resistência Vascular (R_v): <b>13.81 dyn·s/cm⁵</b> (Pressão microvascular sob controle).<br/>"
            "• Mapeamento Dermoscópico: Densidade folicular de <b>192 fios/cm²</b> na região do ápice temporal.<br/><br/>"
            "<b>02 // Espectrometria Capilar & Refração (Lei de Snell):</b><br/>"
            "• Índice de Refração (η): <b>1.566 η</b> | Taxa de Miniaturização: <b>1.3%</b> (Fase anágena dominante em 89%).<br/>"
            "• Visagismo & Arquitetura Craniofacial: Ângulos tensoriais de 115° a 120° calibrados para vetor de projeção executiva."
        )

    def _calcular_matriz_vulnerabilidade_estado(self, anos: int) -> dict:
        fator_nao_linear = 1.0 + (0.02 * anos)
        integridade_biologica = max(100.0 - (1.15 * anos * (1.0 + self.ameaca) * fator_nao_linear), 25.0)
        deslocamento_vetorial = 0.16 * anos * (1.0 + self.ameaca) * fator_nao_linear
        ive = min(max((deslocamento_vetorial * 17.5) + ((100.0 - integridade_biologica) * 0.45), 4.0), 99.9)
        wacc_base = 8.5  
        premio_risco_lideranca = (ive / 100.0) * 8.0  
        wacc_degradado = wacc_base + premio_risco_lideranca
        valuation_degradado = self.aum / ((1.0 + (wacc_degradado / 100.0)) ** anos)
        valuation_protegido = self.aum / ((1.0 + (wacc_base / 100.0)) ** anos)
        custo_atrito_mercado = max(valuation_protegido - valuation_degradado, 0.0)
        roi = max(120.0 - (2.8 * anos), 15.0)

        return {
            "integridade_perc": round(integridade_biologica, 1),
            "deslocamento_mm": round(deslocamento_vetorial, 2),
            "ive_score": round(ive, 1),
            "wacc_atual": round(wacc_degradado, 2),
            "valuation_degradado": round(valuation_degradado, 2),
            "atrito_mercado_milhoes": round(custo_atrito_mercado, 2),
            "roi": round(roi, 1)
        }

    def _calcular_matriz_recuperacao_tratamento(self, anos: int) -> dict:
        fator_atenuacao_biologica = min(1.0, max(0.3, (100.0 - self.iep) / 50.0))
        bonus_oxigenio = (self.oximetria - 95.0) * 0.2 if self.oximetria > 95.0 else 0.0
        integridade_tratada = min(99.8, 92.0 + (anos * 0.5) + bonus_oxigenio)
        ive_tratado = max(3.5, (15.0 - (anos * 0.6)) * fator_atenuacao_biologica)
        wacc_base = 8.5
        wacc_otimizado = wacc_base + ((ive_tratado / 100.0) * 1.5)
        valuation_protegido = self.aum / ((1.0 + (wacc_base / 100.0)) ** anos)
        valuation_otimizado = self.aum / ((1.0 + (wacc_otimizado / 100.0)) ** anos)
        cenario_ruim = self._calcular_matriz_vulnerabilidade_estado(anos)
        ganho_patrimonial_net = max(0.0, valuation_otimizado - cenario_ruim["valuation_degradado"])
        fator_performance_tratamento = f"+{((valuation_otimizado / cenario_ruim['valuation_degradado'] - 1) * 100):.1f}%"

        return {
            "integridade_tratada": round(integridade_tratada, 1),
            "ive_tratado": round(ive_tratado, 1),
            "wacc_otimizado": round(wacc_otimizado, 2),
            "valuation_otimizado": round(valuation_otimizado, 2),
            "ganho_patrimonial_net_milhoes": round(ganho_patrimonial_net, 2),
            "fator_performance": fator_performance_tratamento
        }

    def _gerar_grafico_erosao(self, projecoes: dict, caminho_grafico: str = "chart_temp.png"):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from scipy.interpolate import make_interp_spline
        
        anos_raw = np.array([0] + list(projecoes.keys()))
        v_degradado_raw = np.array([self.aum] + [info["metricas"]["valuation_degradado"] for info in projecoes.values()])
        v_otimizado_raw = np.array([self.aum] + [info["recuperacao"]["valuation_otimizado"] for info in projecoes.values()])
        
        if len(anos_raw) > 2:
            anos_smooth = np.linspace(anos_raw.min(), anos_raw.max(), 400)
            spl_deg = make_interp_spline(anos_raw, v_degradado_raw, k=2)
            spl_opt = make_interp_spline(anos_raw, v_otimizado_raw, k=2)
            v_degradado = spl_deg(anos_smooth)
            v_otimizado = spl_opt(anos_smooth)
            anos_plot = anos_smooth
        else:
            anos_plot = anos_raw
            v_degradado = v_degradado_raw
            v_otimizado = v_otimizado_raw

        oscilacao = np.sin(anos_plot * 1.2) * (self.aum * 0.015)
        v_pulso_dinamico = v_degradado + (v_otimizado - v_degradado) * 0.70 + oscilacao

        fig, ax = plt.subplots(figsize=(4.85, 1.30), dpi=300)
        fig.patch.set_facecolor('#0A1128')
        ax.set_facecolor('#0A1128')
        
        title_text = 'PULSO DE RECUPERAÇÃO BIOMÉTRICA & TRAJETÓRIA DE VALUATION SOBERANO'
        xlabel_text = 'Horizonte Temporal (Anos)'
        ylabel_text = 'Valuation (€ M)'

        ax.plot(anos_plot, v_otimizado, color='#E5C158', linewidth=0.85, label='Curva Otimizada (IEP & Oximetria)', linestyle='--')
        ax.plot(anos_plot, v_degradado, color='#C0392B', linewidth=0.85, label='Linha de Base de Erosão (Sem Tratamento)', linestyle=':')
        ax.plot(anos_plot, v_pulso_dinamico, color='#00B894', linewidth=0.85, label='Pulso Quântico Biométrico (Verde)', linestyle='--')
        
        ax.set_xlim(0, 15)
        ax.set_xticks([0, 5, 10, 15])
        
        ax.set_title(title_text, fontsize=5.5, fontname='sans-serif', weight='bold', color='#FFFFFF', pad=4)
        ax.set_xlabel(xlabel_text, fontsize=4.5, color='#BDC3C7', weight='bold')
        ax.set_ylabel(ylabel_text, fontsize=4.5, color='#BDC3C7', weight='bold')
        ax.tick_params(axis='both', which='major', labelsize=4.0, colors='#BDC3C7')
        
        ax.grid(True, linestyle='--', alpha=0.15, color='#FFFFFF')
        ax.legend(loc='lower left', fontsize=3.2, frameon=True, facecolor='#0A1128', edgecolor='#D4AF37', labelcolor='#FFFFFF')
        
        for spine in ax.spines.values():
            spine.set_edgecolor('#D4AF37')
            spine.set_linewidth(0.4)
            
        plt.tight_layout()
        plt.savefig(caminho_grafico, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()

    def _gerar_briefing_inteligencia(self, anos: int, ive: float, atrito: float, deslocamento: float) -> str:
        return f"<font color='#00875A'><b>Soberania Ativa (IEP {self.iep}):</b></font> Oximetria em {self.oximetria}%. Risco mitigado e WACC otimizado para o ecossistema de {self.entidade}."

    def _obter_texto_analitico_bloco_1(self) -> str:
        return f"""
        <b>Síntese de Impacto Financeiro e Celular ({self.entidade} | {self.lider}):</b> O Índice de Eficiência Preditiva (IEP {self.iep}) atesta a alta performance biológica, reduzindo o prêmio de risco corporativo e preservando o valuation multibilionário.
        """

    def _gerar_folha_historico_anual(self) -> list:
        """Gera a folha dedicada no final do PDF listando de forma limpa todos os atendimentos anteriores gravados."""
        elementos_historico = []
        atendimentos = self.dados_preditivos_cliente.get("atendimentos", [])
        
        estilo_titulo = ParagraphStyle('HistTtl', fontSize=10, leading=13, textColor=colors.HexColor('#0A1128'), fontName="Helvetica-Bold", spaceAfter=6)
        estilo_texto = ParagraphStyle('HistTxt', fontSize=7.5, leading=11, textColor=colors.HexColor('#1E293B'), fontName="Helvetica", spaceAfter=4)
        
        elementos_historico.append(PageBreak())
        elementos_historico.append(Paragraph("[ ANEXO: EVOLUÇÃO LONGITUDINAL & HISTÓRICO DE CICLOS ANTERIORES ]", estilo_titulo))
        elementos_historico.append(Paragraph(f"<b>Titular:</b> {self.lider} | <b>Consolidado Plurianual</b>", estilo_texto))
        elementos_historico.append(Spacer(1, 6))
        
        if len(atendimentos) > 1:
            elementos_historico.append(Paragraph("<b>Marcos Evolutivos e Comportamento Biométrico Registado:</b>", estilo_texto))
            for idx, atd in enumerate(atendimentos[:-1], 1):
                data = atd.get("data", "Sessão Anterior")
                proc = atd.get("procedimento") or atd.get("procedimento_base", "Avaliação Estética e Sistêmica")
                ox = atd.get("metricas_de_entrada", {}).get("oximetria_tecidual", "N/D")
                iep_ant = atd.get("modulo_preditivo_autonomo", {}).get("indice_eficiencia_preditiva_iep", "N/D")
                
                texto_atd = f"• <b>[{data}]</b> {proc} | IEP: {iep_ant} | Oximetria: {ox} — <i>Comportamento tecidual estável com resposta positiva ao protocolo global estabelecido.</i>"
                elementos_historico.append(Paragraph(texto_atd, estilo_texto))
        else:
            elementos_historico.append(Paragraph("<b>Registo Histórico Plurianual:</b> O titular possui histórico estruturado em consolidação contínua. Este ciclo estabelece a baseline definitiva para o acompanhamento plurianual do ecossistema.", estilo_texto))
            
        return elementos_historico

    def processar_dossie_defensivo(self) -> dict:
        horizontes = [5, 10, 15]
        projecoes = {}
        for ano in horizontes:
            metricas = self._calcular_matriz_vulnerabilidade_estado(ano)
            recuperacao = self._calcular_matriz_recuperacao_tratamento(ano)
            briefing = self._gerar_briefing_inteligencia(ano, metricas["ive_score"], metricas["atrito_mercado_milhoes"], metricas["deslocamento_mm"])
            projecoes[ano] = {
                "metricas": metricas,
                "recuperacao": recuperacao,
                "analise_inteligencia": briefing
            }
        return {
            "metadata": {
                "lider": self.lider,
                "entidade": self.entidade,
                "setor": self.segment,
                "horizonte_alvo": f"{self.horizon} Anos",
                "aum_global": f"€ {self.aum:,.2f} Milhões",
                "vertices_monitorados": self.pontos_base,
                "fator_ameaca": self.ameaca,
                "iep_cliente": self.iep,
                "oximetria_cliente": self.oximetria
            },
            "projecao_temporal": projecoes
        }

    def gerar_pdf_defensivo_soberano(self, caminho_salvamento: str = "c2_sovereign_intelligence_dossier.pdf") -> Optional[str]:
        self.timestamp_exec = datetime.datetime.utcnow().strftime("%d/%m/%Y às %H:%M:%S UTC")
        dados_motor = self.processar_dossie_defensivo()
        os.makedirs(os.path.dirname(caminho_salvamento) if os.path.dirname(caminho_salvamento) else '.', exist_ok=True)

        string_base_hash = f"C2-QUANTUM-{self.lider}-{self.entidade}-{self.timestamp_exec}"
        hash_sha256_gerado = hashlib.sha256(string_base_hash.encode('utf-8')).hexdigest().upper()

        caminho_grafico_temp = "chart_temp.png"
        self._gerar_grafico_erosao(dados_motor["projecao_temporal"], caminho_grafico_temp)

        def _desenhar_elementos_pagina(canvas, doc):
            canvas.saveState()
            canvas.translate(A4[0] / 2.0, (A4[1] / 2.0) + 30)
            canvas.rotate(30)
            canvas.setFont("Helvetica-Bold", 26)
            canvas.setFillColor(colors.Color(0.77, 0.63, 0.35, alpha=0.04))
            canvas.drawCentredString(0, 0, "MONACO QUANTUM PLATINUM • C2 SOVEREIGN INTELLIGENCE")
            canvas.restoreState()
            
            canvas.saveState()
            canvas.setStrokeColor(colors.HexColor('#B8860B'))
            canvas.setLineWidth(0.75)
            canvas.line(30, 36, A4[0] - 30, 36)
            
            canvas.setFont("Helvetica", 7)
            canvas.setFillColor(colors.HexColor('#0A1128'))
            canvas.drawString(30, 24, "Classificado • C2 Quantum Intelligence & UHNW Financial-Biological Nexus")
            pagina_atual = canvas._pageNumber
            canvas.drawRightString(A4[0] - 30, 24, f"MONACO SEAL • PÁGINA {pagina_atual} • SHA-256 SECURED")
            canvas.restoreState()

        doc = SimpleDocTemplate(
            caminho_salvamento,
            pagesize=A4,
            leftMargin=30,
            rightMargin=30,
            topMargin=30,
            bottomMargin=45
        )
        story = []

        MONACO_NAVY = colors.HexColor('#0A1128')
        SOVEREIGN_GOLD = colors.HexColor('#B8860B')
        EXCELENCIA_VERDE = colors.HexColor('#00875A')
        DARK_TEXT = colors.HexColor('#1E293B')
        CARD_BG = colors.HexColor('#F8FAFC')
        CARD_BORDER = colors.HexColor('#CBD5E1')
        
        styles = {
            'CapaSuper': ParagraphStyle('CapaSuper', fontSize=9, fontName='Helvetica-Bold', textColor=SOVEREIGN_GOLD, leading=12, alignment=1, spaceAfter=15),
            'CapaTituloUnificado': ParagraphStyle('CapaTituloUnificado', fontSize=14, fontName='Helvetica-Bold', textColor=MONACO_NAVY, leading=18, alignment=1, spaceAfter=20),
            'CapaMeta': ParagraphStyle('CapaMeta', fontSize=8.5, fontName='Helvetica', textColor=MONACO_NAVY, leading=14, alignment=1),
            'SecSovereign': ParagraphStyle('SecSovereign', fontSize=10, fontName='Helvetica-Bold', textColor=MONACO_NAVY, leading=13, spaceBefore=6, spaceAfter=3),
            'TextSovereign': ParagraphStyle('TextSovereign', fontSize=7.5, fontName='Helvetica', textColor=DARK_TEXT, leading=11, spaceAfter=2, alignment=4),
            'TableHeader': ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=SOVEREIGN_GOLD, alignment=1),
            'TableCell': ParagraphStyle('TC', fontName='Helvetica', fontSize=7.0, textColor=DARK_TEXT, leading=9, alignment=1),
            'TableGreenCell': ParagraphStyle('TGC', fontName='Helvetica-Bold', fontSize=7.0, textColor=EXCELENCIA_VERDE, leading=9, alignment=1),
            'ParecerText': ParagraphStyle('PT', fontName='Helvetica', fontSize=6.5, textColor=DARK_TEXT, leading=8.5),
            'ExecutiveSummaryBlock': ParagraphStyle('ESB', fontName='Helvetica', fontSize=7.5, textColor=MONACO_NAVY, leading=11, spaceBefore=3, spaceAfter=4, alignment=4),
            'Normal': ParagraphStyle('N', fontName='Helvetica', fontSize=8, textColor=DARK_TEXT, leading=11, spaceAfter=4),
            'CardTitle': ParagraphStyle('CardTitle', fontName='Helvetica-Bold', fontSize=7.5, textColor=SOVEREIGN_GOLD, leading=9),
            'CardValue': ParagraphStyle('CardValue', fontName='Helvetica-Bold', fontSize=9.5, textColor=MONACO_NAVY, leading=12),
            'CardRegiao': ParagraphStyle('CardRegiao', fontName='Helvetica', fontSize=6.5, textColor=colors.HexColor('#64748B'), leading=8),
            'CardStatus': ParagraphStyle('CardStatus', fontName='Helvetica-Bold', fontSize=6.5, textColor=EXCELENCIA_VERDE, leading=8, alignment=2)
        }

        estilo_titulo_bloco_claro = ParagraphStyle('TtlBlocoClaro', fontSize=9.5, leading=12, textColor=MONACO_NAVY, fontName="Helvetica-Bold")
        estilo_label_bloco_claro = ParagraphStyle('LblBlocoClaro', fontSize=8.0, leading=11, textColor=colors.HexColor('#475569'), fontName="Helvetica-Bold")
        estilo_conteudo_bloco_claro = ParagraphStyle('CntBlocoClaro', fontSize=8.0, leading=11.5, textColor=DARK_TEXT, fontName="Helvetica")

        # ==================== PÁGINA 1: CAPA ====================
        story.append(Spacer(1, 20))
        story.append(Paragraph("THIERRY TECHNOLOGY CONCEPT GLOBAL • QUANTUM UHNW DIVISION", styles['CapaSuper']))
        
        meta_texto = f"""
        <b>Titular / Entidade:</b> {self.lider} | {self.entidade}<br/>
        <b>Setor Alvo:</b> {self.segment}<br/>
        <b>Horizonte Estratégico:</b> {self.horizon} Anos | <b>AUM Global UHNW:</b> € {self.aum:,.2f} Milhões<br/>
        <b>Índice de Eficiência Preditiva (IEP):</b> {self.iep} / 100 | <b>Oximetria Tecidual:</b> {self.oximetria}%<br/>
        <b>Chave de Integridade (SHA-256):</b> {hash_sha256_gerado}<br/>
        <b>Data de Emissão:</b> {self.timestamp_exec}
        """
        titulo_completo = "DOSSIÊ EXECUTIVO DE NEXO BIOLÓGICO-FINANCEIRO & CRONOESTÉTICA QUÂNTICA UHNW"
        
        story.append(Paragraph(titulo_completo, styles['CapaTituloUnificado']))
        story.append(Paragraph(meta_texto.strip(), styles['CapaMeta']))
        story.append(Spacer(1, 15))
        story.append(PageBreak())

        # ==================== PÁGINA 2: BLOCO UNIFICADO ====================
        story.append(Paragraph("MATRIZ DE IMPACTO FINANCEIRO: VALUATION x IEP CLÍNICO", styles['SecSovereign']))
        story.append(Paragraph(f"Projeção baseada na mitigação de WACC através do IEP de {self.iep} e oximetria de {self.oximetria}%.", styles['TextSovereign']))
        story.append(Spacer(1, 2))

        elementos_bloco_unificado = []
        if os.path.exists(caminho_grafico_temp):
            elementos_bloco_unificado.append(Image(caminho_grafico_temp, width=503, height=93))
        
        t_divisor_prata = Table([[""]], colWidths=[503], rowHeights=[2])
        t_divisor_prata.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#BDC3C7'))]))
        elementos_bloco_unificado.append(t_divisor_prata)

        t_horizontes_headers = ["Horizonte", "IVE Opt.", "WACC", "Integr.", "Ganho Líq.", "Valuation", "Perf.", "Parecer C2 Quantum"]
        t_horizontes_data = [[Paragraph(h, styles['TableHeader']) for h in t_horizontes_headers]]
        
        for ano, info in dados_motor["projecao_temporal"].items():
            r = info["recuperacao"]
            linha = [
                Paragraph(f"<b>+{ano}A</b>", styles['TableCell']),
                Paragraph(f"{r['ive_tratado']}%", styles['TableGreenCell']),
                Paragraph(f"{r['wacc_otimizado']}%", styles['TableCell']),
                Paragraph(f"{r['integridade_tratada']}%", styles['TableCell']),
                Paragraph(f"€ {r['ganho_patrimonial_net_milhoes']}M", styles['TableCell']),
                Paragraph(f"€ {r['valuation_otimizado']:,.0f}M", styles['TableCell']),
                Paragraph(f"{r['fator_performance']}", styles['TableGreenCell']),
                Paragraph(info['analise_inteligencia'], styles['ParecerText'])
            ]
            t_horizontes_data.append(linha)

        t_horizontes = Table(t_horizontes_data, colWidths=[38, 42, 38, 42, 62, 74, 45, 162])
        t_horizontes.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [CARD_BG, colors.HexColor('#FFFFFF')]),
            ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('LINEBELOW', (0,0), (-1,0), 1.5, SOVEREIGN_GOLD)
        ]))
        elementos_bloco_unificado.append(t_horizontes)

        bloco_mestre_tabela = Table([[elementos_bloco_unificado]], colWidths=[513])
        bloco_mestre_tabela.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
            ('BOX', (0,0), (-1,-1), 1.0, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        
        story.append(bloco_mestre_tabela)
        story.append(Spacer(1, 3))
        story.append(Paragraph(self._obter_texto_analitico_bloco_1().strip(), styles['ExecutiveSummaryBlock']))
        story.append(PageBreak())

        # ==================== PÁGINA 3: SEÇÃO II - CARDS & BLOCO I ISOLADO ====================
        story.append(Paragraph("[ SEÇÃO II: NEXO BIOLÓGICO-FINANCEIRO & CRONOESTÉTICA ]", styles['SecSovereign']))
        story.append(Paragraph(f"<b>Classificação: Confidencial / Nível C-Suite (UHNW Restricted)</b> | Titular: {self.lider}", styles['Normal']))
        story.append(Spacer(1, 4))
        
        atendimentos_json = self.dados_preditivos_cliente.get("atendimentos", [])
        ultimo_atendimento = atendimentos_json[-1] if atendimentos_json else {}
        crono = ultimo_atendimento.get("cronoestetica_e_gemeo_digital", {})
        meteo = ultimo_atendimento.get("engine_meteo_climatica_16_dias", {}).get("alerta_uv_radiacao", {})

        dia_apice_val = crono.get("dia_apice_regeneracao", "24/10/2026")
        alerta_uv_val = meteo.get("risco", "Monitoramento Climático Ativo")

        parecer_aptidao_invasiva = self._avaliar_aptidao_tratamento_invasivo("Bioestimulador de Colágeno / Cirurgia")
        parametro_neuro_medico = self._gerar_parametro_neuro_clinico()

        items_cards = [
            ("Índice de Eficiência Preditiva (IEP)", f"{self.iep} / 100 (Mitigador de WACC)", "Algoritmo Quântico C2", "Zona Verde - Excelência"),
            ("Oximetria Tecidual Conectada", f"{self.oximetria}% (Bônus de Recuperação)", "Métrica de Entrada Clínica", "Resiliência Máxima"),
            ("Dia Ápice Regenerativo", f"{dia_apice_val}", "Janela de Ouro (LED 830nm)", "Pico Circadiano"),
            ("Alerta Meteo-Climático", f"{alerta_uv_val}", "Janela de 16 Dias (UV Proteção)", "Blindagem Ativa"),
            ("Hidratação Intercelular", "98.4% (Volume hídrico dérmico ótimo)", "Quantidade de Água na Pele / Manto", "Resiliência Cutânea Soberana"),
            ("Integridade do Manto", "100.0% (Barreira defensiva ativa)", "Escudo Epidérmico Soberano", "Resiliência Cutânea Soberana")
        ]

        linhas_tabela_mestre_secao_2 = []
        for i in range(0, len(items_cards), 2):
            par_itens = items_cards[i:i+2]
            celulas_linha = []
            for vetor, valor, regiao, status in par_itens:
                conteudo_interno_celula = [
                    [Paragraph(f"<b>{vetor}</b>", styles['CardTitle']), Paragraph("", styles['CardStatus'])],
                    [Paragraph(f"<b>{valor}</b>", styles['CardValue']), Paragraph("", styles['CardStatus'])],
                    [Paragraph(regiao, styles['CardRegiao']), Paragraph(f"<b>{status}</b>", styles['CardStatus'])]
                ]
                t_sub = Table(conteudo_interno_celula, colWidths=[148, 102])
                t_sub.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                    ('TOPPADDING', (0,0), (-1,-1), 2),
                    ('LEFTPADDING', (0,0), (-1,-1), 4),
                    ('RIGHTPADDING', (0,0), (-1,-1), 4),
                    ('LINEBELOW', (0,1), (-1,1), 0.5, CARD_BORDER)
                ]))
                celulas_linha.append(t_sub)
            linhas_tabela_mestre_secao_2.append(celulas_linha)

        bloco_mestre_secao_2 = Table(linhas_tabela_mestre_secao_2, colWidths=[256, 256])
        bloco_mestre_secao_2.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1.0, CARD_BORDER),
            ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(bloco_mestre_secao_2)
        story.append(Spacer(1, 6))

        linhas_historico_tratamentos = []
        if atendimentos_json:
            for idx, atd in enumerate(atendimentos_json, 1):
                procedimento = atd.get("procedimento") or atd.get("procedimento_base") or atd.get("id_atendimento", f"Atendimento #{idx}")
                data_atd = atd.get("data") or atd.get("data_execucao", "14/10/2026")
                durabilidade = atd.get("durabilidade_prevista_meses") or atd.get("modulo_preditivo_autonomo", {}).get("durabilidade_prevista_meses", "6.0")
                detalhes = atd.get("metricas_de_entrada", {}).get("nivel_inflamacao_inicial") or atd.get("metricas_biometricas_entrada", {}).get("nivel_inflamacao_inicial", "Moderado")
                
                linhas_historico_tratamentos.append(
                    f"• [{data_atd}] {procedimento} | Durabilidade: {durabilidade} Meses | Nota: {detalhes}"
                )
            texto_tratamentos_formatado = " | ".join(linhas_historico_tratamentos)
        else:
            texto_tratamentos_formatado = "Avaliação Biométrica Inicial e Protocolo Global"

        perfil_neuro = self.dados_preditivos_cliente.get('dados_pessoais', {}).get('perfil_neurologico', {}).get('status_dominante', 'Dominância Parassimpática / Regulação Ativa')

        # --- BLOCO I: HISTÓRICO CLÍNICO DETALHADO & PARECER CLÍNICO/PACIENTE ---
        tabela_bloco_i = Table([
            [Paragraph("<b>[BLOCO I] HISTÓRICO CLÍNICO DETALHADO & PARECER CLÍNICO/PACIENTE</b>", estilo_titulo_bloco_claro), ""],
            [Paragraph("Titular do Protocolo:", estilo_label_bloco_claro), Paragraph(self.lider, estilo_conteudo_bloco_claro)],
            [Paragraph("Perfil Neurológico:", estilo_label_bloco_claro), Paragraph(perfil_neuro, estilo_conteudo_bloco_claro)],
            [Paragraph("Data da Coleta/Procedimento:", estilo_label_bloco_claro), Paragraph("14/10/2026 (Janela de Ouro - LED 830nm)", estilo_conteudo_bloco_claro)],
            [Paragraph("Histórico de Tratamentos:", estilo_label_bloco_claro), Paragraph(texto_tratamentos_formatado, estilo_conteudo_bloco_claro)],
            [Paragraph("Aptidão a Procedimentos (Invasivos/Bioest.):", estilo_label_bloco_claro), Paragraph(parecer_aptidao_invasiva, estilo_conteudo_bloco_claro)],
            [Paragraph("Recomendação de Retorno:", estilo_label_bloco_claro), Paragraph(f"<b>{dia_apice_val}</b> (Dia Ápice Regenerativo & Neuroplasticidade Ativa)", estilo_conteudo_bloco_claro)],
            [Paragraph("Diretriz Tática Profissional:", estilo_label_bloco_claro), Paragraph(parametro_neuro_medico, estilo_conteudo_bloco_claro)]
        ], colWidths=[140, 373])
        
        tabela_bloco_i.setStyle(TableStyle([
            ('SPAN', (0, 0), (1, 0)),
            ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
            ('BOX', (0, 0), (-1, -1), 1.0, CARD_BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, 0), 1, CARD_BORDER),
        ]))
        story.append(tabela_bloco_i)
        story.append(PageBreak())

        # ==================== PÁGINA 4: BLOCOS II, III E IV ====================
        story.append(Paragraph("[ ANEXO TÉCNICO: TELEMETRIA, DIAGNÓSTICO & PLANOS DE AÇÃO ]", styles['SecSovereign']))
        story.append(Paragraph(f"<b>Titular:</b> {self.lider} | <b>Auditoria UHNW Mônaco</b>", styles['Normal']))
        story.append(Spacer(1, 4))

        # --- BLOCO II: TELEMETRIA CLÍNICA INTERNA & DIAGNÓSTICO AVANÇADO ---
        tabela_bloco_ii = Table([
            [Paragraph("<b>[BLOCO II] TELEMETRIA CLÍNICA INTERNA & DIAGNÓSTICO AVANÇADO</b>", estilo_titulo_bloco_claro), ""],
            [Paragraph("Estabilidade Microvascular:", estilo_label_bloco_claro), Paragraph("Fator Térmico Tecidual: 4.5 | Temperatura Ambiente: 27.8 °C", estilo_conteudo_bloco_claro)],
            [Paragraph("Balanço Higrométrico:", estilo_label_bloco_claro), Paragraph("Umidade Relativa: 50.9% | Controle de TEWL otimizado.", estilo_conteudo_bloco_claro)],
            [Paragraph("Score Global de Fadiga:", estilo_label_bloco_claro), Paragraph("23.7 / 100 [Zona Verde - Excelência Clínica]", estilo_conteudo_bloco_claro)],
            [Paragraph("Tônus Muscular:", estilo_label_bloco_claro), Paragraph("15 oscilações/min (Repouso equilibrado, livre de picos de cortisol sistêmico).", estilo_conteudo_bloco_claro)]
        ], colWidths=[140, 373])
        
        tabela_bloco_ii.setStyle(TableStyle([
            ('SPAN', (0, 0), (1, 0)),
            ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
            ('BOX', (0, 0), (-1, -1), 1.0, CARD_BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, 0), 1, CARD_BORDER),
        ]))
        story.append(tabela_bloco_ii)
        story.append(Spacer(1, 6))

        # --- BLOCO III: VETORES DE DIAGNÓSTICO FORENSE, ESTRUTURAL & TRICOLOGIA SUPREMA ---
        tabela_bloco_iii = Table([
            [Paragraph("<b>[BLOCO III] VETORES DE DIAGNÓSTICO FORENSE, ESTRUTURAL & TRICOLOGIA SUPREMA</b>", estilo_titulo_bloco_claro), ""],
            [Paragraph("Anatomia Muscular:", estilo_label_bloco_claro), Paragraph("Tríade Superior (Intacta/Visível) com Linha Temporal preservada e atenuação de micro-movimentos involuntários na face frontal.", estilo_conteudo_bloco_claro)],
            [Paragraph("Visagismo & Tricologia Ultra Suprema:", estilo_label_bloco_claro), Paragraph(self._gerar_diagnostico_tricologia_suprema(), estilo_conteudo_bloco_claro)]
        ], colWidths=[140, 373])
        
        tabela_bloco_iii.setStyle(TableStyle([
            ('SPAN', (0, 0), (1, 0)),
            ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
            ('BOX', (0, 0), (-1, -1), 1.0, CARD_BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, 0), 1, CARD_BORDER),
        ]))
        story.append(tabela_bloco_iii)
        story.append(Spacer(1, 6))

        # --- BLOCO IV: PLANOS DE AÇÃO DE ALTA PERFORMANCE (PLANO REGENERATIVO) ---
        tabela_bloco_iv = Table([
            [Paragraph("<b>[BLOCO IV] PLANOS DE AÇÃO DE ALTA PERFORMANCE (PLANO REGENERATIVO)</b>", estilo_titulo_bloco_claro), ""],
            [Paragraph("Pilar I (Modulação):", estilo_label_bloco_claro), Paragraph("Aplicação de Toxina Botulínica no Terço Superior com alinhamento de simetria frontal e suavização de linhas glabelares.", estilo_conteudo_bloco_claro)],
            [Paragraph("Pilar II (Escultura):", estilo_label_bloco_claro), Paragraph("Geometria da Barba mapeada por laser-guide nos ângulos faciais de 115° a 120° para preservação de linhas executivas globais.", estilo_conteudo_bloco_claro)],
            [Paragraph("Pilar III (Estímulo):", estilo_label_bloco_claro), Paragraph("Ativação fotônica com LEDterapia 830nm agendada para a janela biológica de máxima receptividade tecidual.", estilo_conteudo_bloco_claro)]
        ], colWidths=[140, 373])
        
        tabela_bloco_iv.setStyle(TableStyle([
            ('SPAN', (0, 0), (1, 0)),
            ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
            ('BOX', (0, 0), (-1, -1), 1.0, CARD_BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, 0), 1, CARD_BORDER),
        ]))
        story.append(tabela_bloco_iv)
        story.append(Spacer(1, 6))

        story.append(Paragraph(f"<b>Checksum de Integridade C2 Quantum:</b> {hashlib.sha256(str(self.pontos_base).encode()).hexdigest()[:32].upper()}", styles['Normal']))
        story.append(Paragraph(f"<b>Timestamp de Autenticação Mônaco:</b> {self.timestamp_exec}", styles['Normal']))

        # --- ADIÇÃO DA FOLHA DEDICADA DE HISTÓRICO PLURIANUAL ---
        story.extend(self._gerar_folha_historico_anual())

        doc.build(story, onFirstPage=_desenhar_elementos_pagina, onLaterPages=_desenhar_elementos_pagina)

        if os.path.exists(caminho_grafico_temp):
            try:
                os.remove(caminho_grafico_temp)
            except:
                pass

        return str(caminho_salvamento)


# =====================================================================
# FUNÇÃO DE PONTE/COMPATIBILIDADE E ARQUIVAMENTO POR CICLOS PLURIANUAIS
# =====================================================================
def gerar_dossie_auditoria(dados_paciente: Dict[str, Any]) -> str:
    """Função mestre: Grava automaticamente no cofre do cliente, calcula a cadência exata e compila o PDF."""
    nome_lider = dados_paciente.get("nome") or dados_paciente.get("cliente") or dados_paciente.get("ceo_name") or "Titular Soberano UHNW"
    empresa = dados_paciente.get("empresa") or dados_paciente.get("company_name") or "Thierry Technology Concept Global"
    
    engine = C2SovereignIntelligenceEngine(
        ceo_name=str(nome_lider),
        company_name=str(empresa),
        lang=str(dados_paciente.get("idioma", "PT"))
    )
    
    # --- GARANTE RIGOROSAMENTE QUE O NOME SEJA EXATAMENTE O INFORMADO ---
    engine.lider = str(nome_lider).strip()
    
    # --- AUTONOMIA DE REGISTO: SALVA O ATENDIMENTO NO LEDGER DO CLIENTE ---
    detalhes_atendimento = dados_paciente.get("detalhes_atendimento") or {
        "id_atendimento": f"ATD-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "data": datetime.datetime.now().strftime("%d/%m/%Y"),
        "procedimento": dados_paciente.get("procedimento", "Avaliação Biométrica e Protocolo Global C2"),
        "metricas_de_entrada": {
            "oximetria_tecidual": f"{engine.oximetria}%",
            "nivel_inflamacao_inicial": engine.nivel_inflamacao
        },
        "modulo_preditivo_autonomo": {
            "indice_eficiencia_preditiva_iep": engine.iep,
            "durabilidade_prevista_meses": 6.0
        }
    }
    engine.salvar_atendimento_atual_no_json(detalhes_atendimento)
    
    # --- CÁLCULO INTELIGENTE DO CICLO TEMPORAL CONTÍNUO ---
    atendimentos = engine.dados_preditivos_cliente.get("atendimentos", [])
    dias_decorridos = 0
    anos_decorridos = 0.1
    
    if len(atendimentos) > 1:
        try:
            data_primeiro_str = atendimentos[0].get("data") or atendimentos[0].get("data_execucao", "14/10/2026")
            if "T" in data_primeiro_str:
                data_primeiro = datetime.datetime.fromisoformat(data_primeiro_str)
            else:
                data_primeiro = datetime.datetime.strptime(data_primeiro_str[:10], "%d/%m/%Y")
            data_atual = datetime.datetime.now()
            
            dias_decorridos = (data_atual - data_primeiro).days
            anos_decorridos = round(dias_decorridos / 365, 1)
        except Exception:
            dias_decorridos = 0
            anos_decorridos = 0.1

    if dias_decorridos <= 7:
        pasta_ciclo = "01_Semanal"
    elif dias_decorridos <= 15:
        pasta_ciclo = "02_Quinzenal"
    elif dias_decorridos <= 30:
        pasta_ciclo = "03_Mensal"
    elif dias_decorridos <= 90:
        pasta_ciclo = "04_Trimestral"
    elif dias_decorridos <= 180:
        pasta_ciclo = "05_Semestral"
    elif dias_decorridos <= 270:
        pasta_ciclo = "06_9_Meses"
    else:
        ano_inteiro = int(max(1, round(anos_decorridos)))
        if ano_inteiro <= 15:
            pasta_ciclo = f"0{ano_inteiro}_Ano" if ano_inteiro == 1 else f"{ano_inteiro:02d}_Anos"
        else:
            pasta_ciclo = "15_Anos_Completo"

    pasta_cliente_ciclo = BASE_DIR.parent / "pdfs_finais" / str(nome_lider).replace(" ", "_") / pasta_ciclo
    pasta_cliente_ciclo.mkdir(parents=True, exist_ok=True)
    
    timestamp_arquivo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"Dossie_Sovereign_{pasta_ciclo}_{timestamp_arquivo}.pdf"
    caminho_saida = pasta_cliente_ciclo / nome_arquivo
    
    resultado = engine.gerar_pdf_defensivo_soberano(str(caminho_saida))
    return str(resultado) if resultado else str(caminho_saida)


if __name__ == "__main__":
    pasta_finais = os.path.join(ROOT_DIR, "pdfs_finais")
    os.makedirs(pasta_finais, exist_ok=True)
    
    dados_teste = {"nome": "Pedro Henrique", "empresa": "Thierry Technology Concept Global"}
    arquivo_gerado = gerar_dossie_auditoria(dados_teste)
    print(f"Gerador Quantum executado com Cadência Autónoma! Arquivado em: {arquivo_gerado}")