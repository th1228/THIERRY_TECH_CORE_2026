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

# --- BANCO DE DADOS DE ÓLEOS (ADICIONAL) ---
BD_OLEOS = {
    "01": {"nome": "Lavanda + Sândalo", "foco": "Estabilização Emocional", "hex": "#8A2BE2"},
    "02": {"nome": "Gerânio + Olíbano", "foco": "Regeneração Celular", "hex": "#FFD700"},
    "03": {"nome": "Alecrim + Hortelã", "foco": "Foco Cognitivo", "hex": "#00FF00"},
    "04": {"nome": "Bergamota + Ylang", "foco": "Elevação de Humor", "hex": "#FF8C00"},
    "05": {"nome": "Melaleuca + Capim", "foco": "Purificação", "hex": "#00FFFF"},
    "06": {"nome": "Laranja + Litsea", "foco": "Aroma da Felicidade", "hex": "#FFD700"},
    "07": {"nome": "Cedro + Vetiver", "foco": "Silêncio Profundo", "hex": "#2F4F4F"}
}

def obter_prescricao_oleo(dados):
    if dados['fadiga'] > 7: return BD_OLEOS["07"]
    if dados['hidratacao'] < 4: return BD_OLEOS["02"]
    if dados['assimetria'] > 5: return BD_OLEOS["01"]
    return BD_OLEOS["06"]

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
    
    c.saveState()
    c.setFillAlpha(0.12)
    c.setFillColor(HexColor("#D4AF37"))
    c.setFont("Helvetica-Bold", 80)
    c.translate(w/2, h/2)
    c.rotate(45)
    c.drawCentredString(0, 0, "THIERRY TECH")
    c.restoreState()
    
    c.setFillColor(HexColor("#000000"))
    c.setFont("Courier", 5.2)
    y = h - 30
    for linha in linhas:
        c.drawString(20, y, linha)
        y -= 9
        
    c.setLineWidth(0.5)
    c.line(20, 50, w - 20, 50)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(20, 40, "FOUNDER: THIÊRRY | ESTRATEGISTA E ARQUITECT EM FENOTIPAGEM GENOMIC E NEURO COMPORTAMENTAL")
    c.drawString(20, 32, "BIOGEMIO - Bioarquitetura Neural e Comportamental")
    c.setFont("Helvetica-Oblique", 6)
    c.drawRightString(w - 20, 40, f"Gerado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    c.drawRightString(w - 20, 32, "Propriedade Intelectual Privada - Uso Restrito")
    
    c.save()
    print(f"\n[OK] Relatório Gerado: {arquivo}")

def gerar_relatorio_definitivo():
    dados = ler_dados_biometricos()
    laudo_psi = ler_laudo_psiquico()
    formato, cortes, paleta = obter_recomendacao_visagismo()
    prescricao = obter_prescricao_oleo(dados) # <-- ADICIONAL DE ÓLEOS
    
    nome_cliente = motor_dados.ler("cliente_nome") or "CLIENTE THIERRY"
    hoje = datetime.datetime.now()
    
    cabecalho_tabela = f"{'DATA':<6} | {'CLIMA':<8} | {'SHAMPOO':<14} | {'TRATAMENTO':<18} | {'DECISÃO':<8} | {'COR (VIBE)':<10} | {'MÚSICA'}"
    
    linhas = [
        "=======================================================================================================",
        "ENGENHARIA DA ALMA | BIOARQUITETURA NEURAL E FENOTIPAGEM COMPORTAMENTAL",
        "=======================================================================================================",
        f"CLIENTE: {nome_cliente} | DATA: {hoje.strftime('%d/%m/%Y')}",
        f"PRESCRICAO OLEO: {prescricao['nome']} | FOCO: {prescricao['foco']}", # <-- INJETADO AQUI
        f"Biometria: Fadiga:{dados['fadiga']} | Assimetria:{dados['assimetria']} | Hidrat:{dados['hidratacao']}",
        f"Laudo Psíquico: {laudo_psi.get('temperamento')} | Lado: {laudo_psi.get('lado')} | Status: {laudo_psi.get('emocional')}",
        f"Estrutura: {formato} | Paleta: {', '.join(paleta)}",
        "Cortes (1-5): " + ", ".join(cortes[:5]),
        "Cortes (6-10): " + ", ".join(cortes[5:]),
        "", "--- AGENDA DE SINTONIA (16 DIAS) ---",
        cabecalho_tabela, "-" * 125
    ]
    
    ultima_cor = ""
    for i in range(16):
        data = hoje + datetime.timedelta(days=i)
        d = (i % 15) + 1 
        
        if d == 1 or d == 15: prep, trat, dec, clima, music = "Metal Detox", "Absolut Molecular", "Prime", "Seco", "Deep House 432Hz"
        elif d % 5 == 0: prep, trat, dec, clima, music = "Shampoo Calmante", "CPR (Senscience)", "Crítico", "Seco", "Ambient Chill"
        elif d % 3 == 0: prep, trat, dec, clima, music = "Davines MOMO", "MOMO Potion", "Cautelosa", "Úmido", "Jazz Lounge"
        elif d % 2 == 0: prep, trat, dec, clima, music = "Chronologiste", "Reposição Lip.", "Estrat.", "Instável", "Minimal Techno"
        else: prep, trat, dec, clima, music = "Davines NOUNOU", "OI All In One", "Tática", "Normal", "Lo-Fi Beats"
        
        cores_disponiveis = ["Dourado", "Azul Real", "Vermelho", "Verde Esmeralda", "Violeta"]
        cor = [c for c in cores_disponiveis if c != ultima_cor][0]
        ultima_cor = cor
            
        linhas.append(f"{data.strftime('%d/%m'):<6} | {clima:<8} | {prep:<14} | {trat:<20} | {dec:<8} | {cor:<10} | {music}")

    for linha in linhas: print(linha)
    gerar_pdf_final(linhas, nome_cliente)

if __name__ == "__main__":
    gerar_relatorio_definitivo()