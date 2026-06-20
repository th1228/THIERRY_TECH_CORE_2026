# -*- coding: utf-8 -*-
import sys
import os
import datetime
import locale
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# --- CORREÇÃO DE ROTA PARA INTEGRAÇÃO ---
raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if raiz_projeto not in sys.path:
    sys.path.insert(0, raiz_projeto)

import motor_dados 

try: 
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except: 
    locale.setlocale(locale.LC_TIME, '')

def ler_laudo_psiquico():
    dados_psi = {"temperamento": "Não analisado", "lado": "Não detectado", "emocional": "Pendente"}
    if os.path.exists("laudo_psiquico.txt"):
        with open("laudo_psiquico.txt", "r", encoding="utf-8") as f:
            for linha in f:
                if ":" in linha:
                    chave, valor = linha.split(":", 1)
                    dados_psi[chave.strip().lower()] = valor.strip()
    return dados_psi

def ler_dados_biometricos():
    if not os.path.exists("log_performance.txt"):
        return {"fadiga": 5, "assimetria": 0, "densidade": 5, "hidratacao": 5}
    with open("log_performance.txt", "r", encoding="utf-8") as f:
        linhas = [l for l in f.readlines() if l.strip()]
        try:
            p = linhas[-1].split(" | ")
            return {"fadiga": int(p[1].split(":")[1]), "assimetria": int(p[2].split(":")[1]),
                    "densidade": int(p[3].split(":")[1]), "hidratacao": int(p[4].split(":")[1])}
        except: return {"fadiga": 5, "assimetria": 0, "densidade": 5, "hidratacao": 5}

def obter_recomendacao_visagismo():
    formato = "Triangular (Base Afunilada)"
    cortes = ["Mid-Fade c/ Volume", "Texturizado Lateral", "Pompadour Lateral", "Side Part c/ Franja", "Undercut Gradual", "Long Fringe", "Messy Quiff", "Buzz Cut c/ Degrade", "Man Bun", "Taper Fade"]
    paleta = ["Castanho Acobreado", "Terracota Profundo", "Mel Dourado", "Bronze Tabaco"]
    return formato, cortes, paleta

def gerar_pdf_final(linhas, nome_cliente):
    arquivo = f"Relatorio_Engenharia_Alma_{nome_cliente.replace(' ', '_')}.pdf"
    c = canvas.Canvas(arquivo, pagesize=A4)
    w, h = A4
    
    # Marca d'água
    c.saveState()
    c.setFillAlpha(0.12)
    c.setFillColor(HexColor("#D4AF37"))
    c.setFont("Helvetica-Bold", 80)
    c.translate(w/2, h/2)
    c.rotate(45)
    c.drawCentredString(0, 0, "THIERRY TECH")
    c.restoreState()
    
    # Conteúdo principal
    c.setFillColor(HexColor("#000000"))
    c.setFont("Courier", 5.2)
    y = h - 30
    for linha in linhas:
        c.drawString(20, y, linha)
        y -= 9
        
    # --- RODAPÉ COM ASSINATURA DE AUTORIDADE ATUALIZADA ---
    c.setLineWidth(0.5)
    c.line(20, 50, w - 20, 50)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(20, 40, "FOUNDER: THIÊRRY | ESTRATEGISTA E ARQUITECT EM FENOTIPAGEM GENOMIC E NEURO COMPORTAMENTAL")
    c.drawString(20, 32, "BIOGEMIO - Bioarquitetura Neural e Comportamental")
    c.setFont("Helvetica-Oblique", 6)
    c.drawRightString(w - 20, 40, f"Gerado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
    c.drawRightString(w - 20, 32, "Propriedade Intelectual Privada - Uso Restrito")
    
    c.save()
    print(f"\n[OK] Relatório Gerado: {arquivo}")

def gerar_relatorio_definitivo():
    dados = ler_dados_biometricos()
    laudo_psi = ler_laudo_psiquico()
    formato, cortes, paleta = obter_recomendacao_visagismo()
    nome_cliente = motor_dados.ler("cliente_nome") or "CLIENTE THIERRY"
    hoje = datetime