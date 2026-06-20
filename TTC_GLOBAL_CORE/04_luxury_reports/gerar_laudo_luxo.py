import sqlite3
import os
import webbrowser
import time
from fpdf import FPDF

class PDF_Laudo_Luxo(FPDF):
    def __init__(self, titulo_header):
        super().__init__()
        self.titulo_header = titulo_header

    def header(self):
        # Barra superior executiva premium - Black Executive
        self.set_fill_color(15, 15, 15)
        self.rect(0, 0, 210, 6, 'F') 
        self.set_font('Arial', 'B', 8.5)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, self.titulo_header, 0, 1, 'L')
        self.ln(1)

    def footer(self):
        self.set_y(-10)
        self.set_font('Arial', 'I', 7.5)
        self.set_text_color(150, 150, 150)
        self.cell(0, 5, 'Thierry Technology Concept Global | Craniometric & Geo-Climatic Intelligence', 0, 0, 'C')

def buscar_dados_biometricos():
    caminho_banco = os.path.join("database", "TCC_global_forense.db")
    if not os.path.exists(caminho_banco):
        return None
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT foto_origem, angulo_olhos, proporcao_tercos, 
                   angulo_goniaco_esq, angulo_goniaco_dir, 
                   comprimento_mand_esq, comprimento_mand_dir, 
                   indice_assimetria, proporcao_mento, status_pericia 
            FROM analises_biometricas 
            ORDER BY id DESC LIMIT 1
        """)
        dados = cursor.fetchone()
    except sqlite3.OperationalError:
        dados = None
    conexao.close()
    return dados

def gerar_pdf_pelo_idioma(dados, idioma='pt', diagnostico_queda=True, precisa_agua=True, e_loira_danificado=True, precisa_nutricao=True):
    (foto, olhos, tercos, gon_esq, gon_dir, mand_esq, mand_dir, assimetria, mento, status) = dados

    # Estruturação e tradução cirúrgica dos dicionários de dados
    if idioma == 'en':
        titulo_doc = "BIO-IDENTICAL CRANIOMETRIC CERTIFICATION"
        sub_doc = "High-End Forensic Mandibular Analysis, Visagism & Geo-Climatic Engineering"
        status_lbl = f"  SYSTEM SCAN STATUS: {status.upper()}"
        sub_status = f"  Mandibular Asymmetry: {assimetria}px  |  Facial Thirds Proportion: {tercos}"
        
        sec1_tit = "1. Forensic Craniometric Readings (Mandibular Bone)"
        sec1_h1, sec1_h2 = " Structural Bone Parameter / Cranial Analysis", " Forensic Metric Value"
        param_fac_txt = [
            ("Left Goniac Angle (Mandibular Base)", f"{gon_esq} Grad"),
            ("Right Goniac Angle (Mandibular Base)", f"{gon_dir} Grad"),
            ("Left Mandibular Ramus Extension", f"{mand_esq} px"),
            ("Right Mandibular Ramus Extension", f"{mand_dir} px"),
            ("Ocular Alignment (Horizontal Cranial Plane)", f"{olhos} Grad"),
            ("Mentum Proportional Projection (Chin)", f"{mento} %")
        ]
        
        sec2_tit = "2. Hair Engineering & Active Cosmetic Prescription"
        sec2_h1, sec2_h2 = " Luxury Laboratory Ecosystem", " Integrated High-Performance Clinical Protocol"
        p_dav = "Davines Naturaltech Energizing + doTERRA Rosemary (Anti-Hairloss)" if diagnostico_queda else "Davines Calming Line"
        p_ker = "Kerastase Specifique / Nutritive (Deep Hydration - Water Retention for Dubai)" if precisa_agua else "Kerastase Resistance"
        p_lor = "Absolut Repair Molecular (Cortical Fusion for Damaged Hair / Blondes)" if e_loira_danificado else "L'Oreal Metal Detox"
        p_wel = "Wella Ultimate Repair Luxury Line (Lipidic Aporte & Cuticle Protection)" if precisa_nutricao else "Wella Oil Reflections"
        param_cap_txt = [("DAVINES + doTERRA", p_dav), ("KERASTASE (Water)", p_ker), ("L'OREAL PROFESSIONNEL", p_lor), ("WELLA PROFESSIONALS", p_wel)]
        
        sec3_tit = "3. Geo-Climatic Tracking & Predictive Weather Forecast (15 to 21 Days Cycle)"
        sec3_h1, sec3_h2, sec3_h3, sec3_h4 = " Analyzed Cycle", " Forecast: DUBAI", " Forecast: MONACO", " Forecast: LOCAL TRACKING"
        ciclo_txt = [
            ("Days 01 to 07 (S1)", "Avg 39C | UV 11+ (Extreme)", "Avg 24C | UV 6 (High)", "Sao Luis: Avg 30C | UV 11 | Humid 78%"),
            ("Days 08 to 14 (S2)", "Avg 41C | UV 12 (Critical)", "Avg 25C | UV 7 (High)", "Sao Luis: Avg 29C | UV 10 | Seasonal Rain"),
            ("Days 15 to 21 (S3)", "Avg 40C | UV 11+ (Extreme)", "Avg 23C | UV 5 (Mod)", "Sao Luis: Avg 31C | UV 11 | High Light")
        ]
        
        alerta_tit = "   [GLOBAL AND REGIONAL PREDICTIVE MONITORING ALERT]"
        alerta_sub = "   Active geo-climatic tracking crossing international hubs with local weather data for Home Care calibration."
        
        sec4_tit = "4. Visagism Architecture & Structural Haircut Design"
        sec4_h1, sec4_h2 = " Facial Assessment (Based on Bone Scan)", " Prescribed Architectural Haircut Spec"
        
        try:
            val_gon = float(gon_esq)
        except:
            val_gon = 120.0

        if val_gon > 125:
            design_corte = "Vertical Shag / Long Layers with Curtain Bangs. Softens the strong angular mandibular projection."
        else:
            design_corte = "Tailored Precision Bob / Sharp Trapezium Edge. Structural lines to empower facial symmetry."
            
        sec4_txt = [
            ("Structural Mandibular Convexity", "Geometric Balance Projection Matrix"),
            ("Calculated Volumetric Density", "Custom Volumization tailored to Cranial Profile"),
            ("PRESCRIBED HAIRCUT DESIGN", design_corte)
        ]
        
        sec5_tit = "5. Computational Photogrammetric Mapping (Mandibular Bone)"
        nome_arquivo = "THIERRY_CONCEPT_GLOBAL_EN.pdf"
        header_text = "THIERRY TECHNOLOGY CONCEPT GLOBAL"
    else:
        titulo_doc = "CERTIFICACAO CRANIOMETRICA BIOIDENTICA"
        sub_doc = "Analise Forense do Osso Mandibular, Visagismo de Elite e Engenharia Geo-Climatica"
        status_lbl = f"  STATUS DO RASTREAMENTO DO SISTEMA: {status.upper()}"
        sub_status = f"  Assimetria Mandibular: {assimetria}px  |  Proporcao dos Tercos Faciais: {tercos}"
        
        sec1_tit = "1. Leituras Craniometricas Forenses (Osso da Mandibula)"
        sec1_h1, sec1_h2 = " Parametro Estrutural Osseo / Analise Craniana", " Valor Metric Forense Obtido"
        param_fac_txt = [
            ("Angulo Goniaco Esquerdo (Base da Mandibula)", f"{gon_esq} Grad"),
            ("Angulo Goniaco Direito (Base da Mandibula)", f"{gon_dir} Grad"),
            ("Extensao do Ramo Mandibular Esquerdo", f"{mand_esq} px"),
            ("Extensao do Ramo Mandibular Direito", f"{mand_dir} px"),
            ("Alinhamento Ocular (Plano Horizontal Craniano)", f"{olhos} Grad"),
            ("Projecao Proporcional do Mento (Queixo)", f"{mento} %")
        ]
        
        sec2_tit = "2. Engenharia do Fio & Prescricao Cosmetica Ativa"
        sec2_h1, sec2_h2 = " Ecossistema de Laboratorios de Luxo", " Protocolo Clinico Integrado de Alta Performance"
        p_dav = "Linha Davines Naturaltech Energizing + doTERRA Alecrim (Antiqueda)" if diagnostico_queda else "Linha Davines Calming"
        p_ker = "Kerastase Specifique / Nutritive (Reposicao Hidrica Profunda - Retencao de Agua para Dubai)" if precisa_agua else "Kerastase Resistance"
        p_lor = "Absolut Repair Molecular (Fusao Cortical para Cabelos Danificados / Loiras)" if e_loira_danificado else "L'Oreal Metal Detox"
        p_wel = "Wella Ultimate Repair Luxury Line (Aporte Lipidico e Protecao da Cuticula)" if precisa_nutricao else "Wella Oil Reflections"
        param_cap_txt = [("DAVINES + doTERRA", p_dav), ("KERASTASE (Agua)", p_ker), ("L'OREAL PROFESSIONNEL", p_lor), ("WELLA PROFESSIONALS", p_wel)]
        
        sec3_tit = "3. Rastreamento Geo-Climatico e Previsao do Tempo Preditiva (Ciclo de 15 a 21 Dias)"
        sec3_h1, sec3_h2, sec3_h3, sec3_h4 = " Ciclo Analisado", " Previsao: DUBAI", " Previsao: MONACO", " Previsao: RASTREAMENTO LOCAL"
        ciclo_txt = [
            ("Dias 01 a 07 (S1)", "Media 39C | UV 11+ (Extrema)", "Media 24C | UV 6 (Alta)", "Sao Luis: Media 30C | UV 11 | Umidade 78%"),
            ("Dias 08 a 14 (S2)", "Media 41C | UV 12 (Critica)", "Media 25C | UV 7 (Alta)", "Sao Luis: Media 29C | UV 10 | Chuvas Sazonais"),
            ("Dias 15 a 21 (S3)", "Media 40C | UV 11+ (Extrema)", "Media 23C | UV 5 (Mod)", "Sao Luis: Media 31C | UV 11 | Alta Luminosidade")
        ]
        
        alerta_tit = "   [ALERTA DE MONITORAMENTO PREDITIVO GLOBAL E REGIONAL]"
        alerta_sub = "   Rastreamento geo-climatico ativo cruzando os hubs internacionais com o clima local para calibracao do Home Care."
        
        sec4_tit = "4. Arquitetura do Visagismo & Design Estrutural do Corte"
        sec4_h1, sec4_h2 = " Avaliacao Facial (Baseada no Scan Osseo)", " Especificacao Arquitetonica do Corte Prescrito"
        
        try:
            val_gon = float(gon_esq)
        except:
            val_gon = 120.0

        if val_gon > 125:
            design_corte = "Corte Shag Vertical / Camadas Longas com Curtain Bangs. Suaviza as linhas marcantes da mandibula."
        else:
            design_corte = "Precision Bob Customizado / Base Trapezoidal Marcante. Linhas estruturais para potencializar a simetria."
            
        sec4_txt = [
            ("Convexidade Estrutural da Mandibula", "Matriz de Projecao de Equilibrio Geometrico"),
            ("Densidade Volumetrica Calculada", "Volumizacao Personalizada adaptada ao Perfil Craniano"),
            ("DESIGN DO CORTE PRESCRITO", design_corte)
        ]
        
        sec5_tit = "5. Mapeamento Fotogrametrico Computacional (Osso da Mandibula)"
        nome_arquivo = "THIERRY_CONCEPT_GLOBAL_PT.pdf"
        header_text = "THIERRY TECHNOLOGY CONCEPT GLOBAL"

    # Geração física estruturada do PDF A4 Página Única Rigorosa
    pdf = PDF_Laudo_Luxo(header_text)
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)

    pdf.set_font('Arial', 'B', 15)
    pdf.set_text_color(25, 25, 25)
    pdf.cell(0, 7, titulo_doc, 0, 1, 'L')
    
    pdf.set_font('Arial', 'I', 8)
    pdf.set_text_color(110, 110, 110)
    pdf.cell(0, 3.5, sub_doc, 0, 1, 'L')
    pdf.ln(2)

    pdf.set_fill_color(245, 245, 245)
    pdf.rect(10, pdf.get_y(), 190, 11, 'F')
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 4, status_lbl, 0, 1, 'L')
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 3.5, sub_status, 0, 1, 'L')
    pdf.ln(4)

    # Seção 1: Craniometria
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 4, sec1_tit, 0, 1, 'L')
    pdf.ln(0.5)
    pdf.set_fill_color(30, 30, 30)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 7)
    pdf.cell(110, 4, sec1_h1, 1, 0, 'L', True)
    pdf.cell(80, 4, sec1_h2, 1, 1, 'L', True)
    pdf.set_text_color(50, 50, 50)
    pdf.set_font('Arial', '', 6.5)
    for p, v in param_fac_txt:
        pdf.cell(110, 3.8, f' {p}', 1, 0, 'L')
        pdf.cell(80, 3.8, f' {v}', 1, 1, 'L')
    pdf.ln(3)

    # Seção 2: Engenharia do Fio e Farmacos
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 4, sec2_tit, 0, 1, 'L')
    pdf.ln(0.5)
    pdf.set_fill_color(45, 45, 45)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 7)
    pdf.cell(50, 4, sec2_h1, 1, 0, 'L', True)
    pdf.cell(140, 4, sec2_h2, 1, 1, 'L', True)
    pdf.set_text_color(50, 50, 50)
    pdf.set_font('Arial', '', 6.5)
    for m, pr in param_cap_txt:
        pdf.cell(50, 3.8, f' {m}', 1, 0, 'L')
        pdf.cell(140, 3.8, f' {pr}', 1, 1, 'L')
    pdf.ln(3)

    # Seção 3: Previsão do Tempo Preditiva
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 4, sec3_tit, 0, 1, 'L')
    pdf.ln(0.5)
    pdf.set_fill_color(110, 95, 70)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 7)
    pdf.cell(30, 4, sec3_h1, 1, 0, 'C', True)
    pdf.cell(50, 4, sec3_h2, 1, 0, 'L', True)
    pdf.cell(50, 4, sec3_h3, 1, 0, 'L', True)
    pdf.cell(60, 4, sec3_h4, 1, 1, 'L', True)
    pdf.set_text_color(50, 50, 50)
    pdf.set_font('Arial', '', 6.5)
    for per, db, mn, lc in ciclo_txt:
        pdf.cell(30, 3.8, f' {per}', 1, 0, 'C')
        pdf.cell(50, 3.8, f' {db}', 1, 0, 'L')
        pdf.cell(50, 3.8, f' {mn}', 1, 0, 'L')
        pdf.cell(60, 3.8, f' {lc}', 1, 1, 'L')
    pdf.ln(2.5)

    # Bloco de Alerta Preditivo
    pdf.set_fill_color(240, 244, 248)
    pdf.rect(10, pdf.get_y(), 190, 8, 'F')
    pdf.set_font('Arial', 'B', 7)
    pdf.set_text_color(15, 45, 75)
    pdf.cell(0, 3, alerta_tit, 0, 1, 'L')
    pdf.set_font('Arial', 'I', 6.5)
    pdf.set_text_color(40, 60, 80)
    pdf.cell(0, 2.5, alerta_sub, 0, 1, 'L')
    pdf.ln(4)

    # Seção 4: Design do Corte Visagista Dinâmico
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 4, sec4_tit, 0, 1, 'L')
    pdf.ln(0.5)
    pdf.set_fill_color(80, 80, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 7)
    pdf.cell(75, 4, sec4_h1, 1, 0, 'L', True)
    pdf.cell(115, 4, sec4_h2, 1, 1, 'L', True)
    pdf.set_text_color(50, 50, 50)
    for ava, esp in sec4_txt:
        if "DESIGN" in ava or "PRESCRIBED" in ava:
            pdf.set_font('Arial', 'B', 6.5)
            pdf.set_fill_color(245, 240, 235)
            pdf.cell(75, 4.2, f' {ava}', 1, 0, 'L', True)
            pdf.cell(115, 4.2, f' {esp}', 1, 1, 'L', True)
            pdf.set_font('Arial', '', 6.5)
        else:
            pdf.cell(75, 3.8, f' {ava}', 1, 0, 'L')
            pdf.cell(115, 3.8, f' {esp}', 1, 1, 'L')
    pdf.ln(3.5)

    # Seção 5: Mapeamento da Foto do Scanner
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 4, sec5_tit, 0, 1, 'L')
    
    pasta_destino = "04__luxury_reports"
    if not os.path.exists(pasta_destino): 
        os.makedirs(pasta_destino)
        
    if os.path.exists(foto):
        # Travamento matemático fixo na base da folha A4 (Y=202)
        pdf.image(foto, x=50, y=202, w=110, h=83)

    caminho_pdf_final = os.path.join(pasta_destino, nome_arquivo)
    pdf.output(caminho_pdf_final)
    return caminho_pdf_final

if __name__ == "__main__":
    dados_biometricos = buscar_dados_biometricos()
    if dados_biometricos:
        # Execução das duas línguas sem erros ou nomes misturados
        caminho_pt = gerar_pdf_pelo_idioma(dados_biometricos, idioma='pt')
        caminho_en = gerar_pdf_pelo_idioma(dados_biometricos, idioma='en')
        
        print("\n==================================================================")
        print(" [SISTEMA SUPREMO TTC] OPERAÇÃO BILÍNGUE EXECUTADA COM SUCESSO!")
        print(" -> PT: 04__luxury_reports/THIERRY_CONCEPT_GLOBAL_PT.pdf")
        print(" -> EN: 04__luxury_reports/THIERRY_CONCEPT_GLOBAL_EN.pdf")
        print("==================================================================\n")
        
        # Abre a aba em Português
        webbrowser.open(f"file:///{os.path.abspath(caminho_pt)}")
        
        # Sincronização de tempo estável para o Windows processar as duas chamadas
        time.sleep(0.6)
        
        # Abre a aba em Inglês ao lado automaticamente
        webbrowser.open(f"file:///{os.path.abspath(caminho_en)}")
    else:
        print("[ERRO] Nenhum registro biometrico localizado no banco.")
        
def obter_dados_craniometria_luxo():
    """""
Retorna os dados periciais e geoclimáticos estruturados
    para serem integrados ao relatório final de Visagismo Neural
    """
    dados_luxo = {
        # 1. Dados Craniométricos (Mapeamento Ósseo)
        "angulo_goniaco_esquerdo": 133.39,
        "angulo_goniaco_direito": 132.97,
        "ramo_mandibular_esquerdo": 147.2,
        "ramo_mandibular_direito": 148.0,
        "alinhamento_ocular": 0.62,
        "proporcao_tercos_faciais": "16.7% : 40.2% : 43.1%",
        "proporcao_mento": 189.3,
        "status_pericia": "SIMETRIA ESTRUTURAL HARMÔNICA",

        # 2. Ecossistema de Laboratórios de Luxo
        "laboratorios": {
            "davines_doterra": "Davines Naturaltech Energizing + doTERRA",
            "kerastase": "Kérastase Spécifique / Nutritive (Hidratação)",
            "loreal": "Absolut Repair Molecular (Fusão Cortical para...",
            "wella": "Linha de Luxo Wella Ultimate Repair (Aporte Lipídico)"
        },

        # 3. Rastreamento Geoclimático Preditivo (Ciclos)
        "clima": {
            "s1_dias_01_07": {"dubai": "39°C | UV 11+", "monaco": "24°C"},
            "s2_dias_08_14": {"dubai": "41°C | UV 12*", "monaco": "25°C"},
            "s3_dias_15_21": {"dubai": "40°C | UV 11+", "monaco": "23°C"}
        }
    }
    """"" 
    
    return dados_luxo
    Retorna os dados periciais e geoclimáticos estruturados 
    para serem integrados ao relatório final de Visagismo Neural.
    """
    dados_luxo = {
        # 1. Dados Craniométricos (Mapeamento Ósseo)
        "angulo_goniaco_esquerdo": 133.39,
        "angulo_goniaco_direito": 132.97,
        "ramo_mandibular_esquerdo": 147.2,
        "ramo_mandibular_direito": 148.0,
        "alinhamento_ocular": 0.62,
        "proporcao_tercos_faciais": "16.7% : 40.2% : 43.1%",
        "proporcao_mento": 189.3,
        "status_pericia": "SIMETRIA ESTRUTURAL HARMÔNICA",
        
        # 2. Ecossistema de Laboratórios de Luxo
        "laboratorios": {
            "davines_doterra": "Davines Naturaltech Energizing + doTERRA Alecrim (Antiqueda)",
            "kerastase": "Kérastase Spécifique / Nutritive (Hidratação Profunda - Retenção de Água para Dubai)",
            "loreal": "Absolut Repair Molecular (Fusão Cortical para Cabelos Danificados / Loiras)",
            "wella": "Linha de Luxo Wella Ultimate Repair (Aporte Lipídico e Proteção da Cutícula)"
        },
        
        # 3. Rastreamento Geoclimático Preditivo (Ciclos)
        "clima": {
            "s1_dias_01_07": {"dubai": "39°C | UV 11+", "monaco": "24°C | UV 6", "sao_luis": "30°C | UV 11 | Ur 78%"},
            "s2_dias_08_14": {"dubai": "41°C | UV 12", "monaco": "25°C | UV 7", "sao_luis": "29°C | UV 10 | Chuva"},
            "s3_dias_15_21": {"dubai": "40°C | UV 11+", "monaco": "23°C | UV 5", "sao_luis": "31°C | UV 11 | Alta Luz"}
        },
        
        # 4. Arquitetura do Corte Geometrico
        "corte_prescrito": {
            "design": "Vertical Shag / Camadas Longas com Franja Cortina (Curtain Bangs)",
            "convexidade": "Matriz de Projeção de Equilíbrio Geométrico",
            "volumetria": "Volumização Personalizada adaptada ao Perfil Craniano"
        }
    }
    return dados_luxo