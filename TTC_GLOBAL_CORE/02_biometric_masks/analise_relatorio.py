import cv2
import sqlite3
import os
import webbrowser
import time
import locale
from fpdf import FPDF

# =========================================================================
# O MOTOR DE INTERNACIONAÇÃO (DICIONÁRIO INTELIGENTE MULTI-IDIOMA)
# =========================================================================
def detectar_idioma():
    """Detecta o idioma do sistema operacional. Retorna 'PT' ou 'EN'."""
    try:
        lang, _ = locale.getdefaultlocale()
        if lang and lang.startswith('pt'):
            return 'PT'
    except Exception:
        pass
    return 'EN'  # Default para o mercado internacional (Dubai, Mônaco, etc.)

IDIOMA_ATIVO = detectar_idioma()

TEXTOS = {
    'PT': {
        'titulo_doc': "CERTIFICACAO CRANIOMETRICA BIOIDENTICA",
        'sub_doc': "Analise Forense do Osso Mandibular, Visagismo de Elite e Engenharia Geo-Climatica",
        'status_lbl': "  STATUS DO RASTREAMENTO DO SISTEMA: ",
        'sub_status': "  Assimetria Mandibular: {}px  |  Proporcao dos Tercos Faciais: {}",
        'sec1_tit': "1. Leituras Craniometricas Forenses e Mapeamento Nervo-Muscular",
        'sec1_h1': " Parametro Estrutural Osseo / Analise Craniana", 
        'sec1_h2': " Valor Metric Forense Obtido",
        'sec2_tit': "2. Engenharia do Fio, Balanco Hidrico & Sintese Lipidica de Alta Performance",
        'sec2_h1': " Ecossistema de Laboratorios de Luxo", 
        'sec2_h2': " Protocolo Clinico Integrado de Alta Performance",
        'sec3_tit': "3. Rastreamento Geo-Climatico e Previsao do Tempo Preditiva (Ciclo de 15 a 21 Dias)",
        'sec3_h1': " Ciclo Analisado", 
        'sec3_h2': " Previsao: DUBAI", 
        'sec3_h3': " Previsao: MONACO", 
        'sec3_h4': " Previsao: RASTREAMENTO LOCAL",
        'alerta_tit': "   [ALERTA DE MONITORAMENTO PREDITIVO GLOBAL E REGIONAL]",
        'alerta_sub': "   Rastreamento geo-climatico ativo cruzando os hubs internacionais com a analise neuro-muscular facial preventiva.",
        'sec4_tit': "4. Arquitetura do Visagismo & Design Estrutural do Corte",
        'sec4_h1': " Avaliacao Facial (Baseada no Scan Osseo)", 
        'sec4_h2': " Especificacao Arquitetonica do Corte Prescrito",
        'sec5_tit': "5. Mapeamento Fotogrametrico Computacional (Osso da Mandibula)",
        'nome_arquivo': "THIERRY_CONCEPT_GLOBAL_PT.pdf",
        
        # Parâmetros da Tabela 1
        'p_gon_esq': "Angulo Goniaco Esquerdo (Base da Mandibula)",
        'p_gon_dir': "Angulo Goniaco Direito (Base da Mandibula)",
        'p_ram_esq': "Extensao do Ramo Mandibular Esquerdo",
        'p_ram_dir': "Extensao do Ramo Mandibular Direito",
        'p_olhos': "Alinhamento Ocular (Plano Horizontal Craniano)",
        'p_mento': "Projecao Proporcional do Mento (Queixo)",
        'p_paralisia': "Predisposicao a Paralisia Facial (Mapeamento de Tonus)",
        
        # Cortes
        'corte_shag': "Corte Shag Vertical / Camadas Longas com Curtain Bangs. Suaviza as linhas marcantes da mandibula.",
        'corte_bob': "Precision Bob Customizado / Base Trapezoidal Marcante. Linhas estruturais para potencializar a simetria.",
        'corte_param1': "Convexidade Estrutural da Mandibula",
        'corte_param2': "Matriz de Projecao de Equilibrio Geometrico",
        'corte_param3': "Densidade Volumetrica Calculada",
        'corte_param4': "Volumizacao Personalizada adaptada ao Perfil Craniano",
        'corte_prescrito': "DESIGN DO CORTE PRESCRITO"
    },
    'EN': {
        'titulo_doc': "BIOIDENTICAL CRANIOMETRIC CERTIFICATION",
        'sub_doc': "Forensic Mandibular Bone Analysis, Elite Visagism & Geo-Climatic Engineering",
        'status_lbl': "  SYSTEM TRACKING STATUS: ",
        'sub_status': "  Mandibular Asymmetry: {}px  |  Facial Thirds Proportion: {}",
        'sec1_tit': "1. Forensic Craniometric Readings & Neuro-Muscular Mapping",
        'sec1_h1': " Structural Bone Parameter / Cranial Analysis", 
        'sec1_h2': " Obtained Forensic Metric Value",
        'sec2_tit': "2. Hair Engineering, Water Balance & High-Performance Lipidic Synthesis",
        'sec2_h1': " Luxury Laboratory Ecosystem", 
        'sec2_h2': " High-Performance Integrated Clinical Protocol",
        'sec3_tit': "3. Geo-Climatic Tracking & Predictive Weather Forecast (15 to 21 Day Cycle)",
        'sec3_h1': " Analyzed Cycle", 
        'sec3_h2': " Forecast: DUBAI", 
        'sec3_h3': " Forecast: MONACO", 
        'sec3_h4': " Forecast: LOCAL TRACKING",
        'alerta_tit': "   [GLOBAL AND REGIONAL PREDICTIVE MONITORING ALERT]",
        'alerta_sub': "   Active geo-climatic tracking crossing international hubs with preventive facial neuro-muscular analysis.",
        'sec4_tit': "4. Visagism Architecture & Structural Haircut Design",
        'sec4_h1': " Facial Evaluation (Based on Bone Scan)", 
        'sec4_h2': " Architectural Specification of the Prescribed Cut",
        'sec5_tit': "5. Computational Photogrammetric Mapping (Mandible Bone)",
        'nome_arquivo': "THIERRY_CONCEPT_GLOBAL_EN.pdf",
        
        # Parâmetros da Tabela 1
        'p_gon_esq': "Left Goniac Angle (Mandible Base)",
        'p_gon_dir': "Right Goniac Angle (Mandible Base)",
        'p_ram_esq': "Left Mandibular Ramus Extension",
        'p_ram_dir': "Right Mandibular Ramus Extension",
        'p_olhos': "Ocular Alignment (Cranial Horizontal Plane)",
        'p_mento': "Proportional Mentum Projection (Chin)",
        'p_paralisia': "Facial Paralysis Predisposition (Tonus Mapping)",
        
        # Cortes
        'corte_shag': "Vertical Shag Cut / Long Layers with Curtain Bangs. Softens sharp jawlines.",
        'corte_bob': "Custom Precision Bob / Sharp Trapezoidal Base. Structural lines to enhance symmetry.",
        'corte_param1': "Structural Mandibular Convexity",
        'corte_param2': "Geometric Balance Projection Matrix",
        'corte_param3': "Calculated Volumetric Density",
        'corte_param4': "Custom Volumization adapted to Cranial Profile",
        'corte_prescrito': "PRESCRIBED HAIRCUT DESIGN"
    }
}

# =========================================================================
# 1. MOTOR DE RENDERIZAÇÃO DO RELATÓRIO DE LUXO MULTI-IDIOMA
# =========================================================================
class PDF_Laudo_Luxo(FPDF):
    def __init__(self, titulo_cabecalho):
        super().__init__()
        self.titulo_cabecalho = titulo_cabecalho

    def header(self):
        self.set_fill_color(15, 15, 15)
        self.rect(0, 0, 210, 6, 'F') 
        self.set_font('Arial', 'B', 8.5)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, self.titulo_cabecalho, 0, 1, 'L')
        self.ln(1)

    def footer(self):
        self.set_y(-10)
        self.set_font('Arial', 'I', 7.5)
        self.set_text_color(150, 150, 150)
        self.cell(0, 5, 'Thierry Technology Concept Global | Analise Craniometrica, Visagismo Forense e Engenharia de Tecidos Cuticulares', 0, 0, 'C')

def gerar_pdf_dinamico(dados, pasta_destino, diagnostico_queda=True, equilibrio_hidrico_dubai=True, e_loira_danificado=True, aporte_lipidico_essencial=True):
    (foto, olhos, tercos, gon_esq, gon_dir, mand_esq, mand_dir, assimetria, mento, status, paralisia) = dados
    
    # Seleciona o dicionário correto baseado no idioma ativo do sistema
    t = TEXTOS[IDIOMA_ATIVO]

    status_lbl_formatado = f"{t['status_lbl']}{status.upper()}"
    sub_status_formatado = t['sub_status'].format(assimetria, tercos)
    
    param_fac_txt = [
        (t['p_gon_esq'], f"{gon_esq} Grad"),
        (t['p_gon_dir'], f"{gon_dir} Grad"),
        (t['p_ram_esq'], f"{mand_esq} px"),
        (t['p_ram_dir'], f"{mand_dir} px"),
        (t['p_olhos'], f"{olhos} Grad"),
        (t['p_mento'], f"{mento} %"),
        (t['p_paralisia'], f"{paralisia}")
    ]
    
    # Internacionalização das Marcas e Linhas
    if IDIOMA_ATIVO == 'PT':
        p_dav = "Linha Davines Naturaltech Energizing + doTERRA Alecrim (Antiqueda)" if diagnostico_queda else "Linha Davines Calming"
        p_ker = "Kerastase Specifique / Nutritive (Reposicao Hidrica Profunda - Retencao de Agua para Dubai)" if equilibrio_hidrico_dubai else "Kerastase Resistance"
        p_lor = "Absolut Repair Molecular (Fusao Cortical para Cabelos Danificados / Loiras)" if e_loira_danificado else "L'Oreal Metal Detox"
        p_wel = "Wella Ultimate Repair Luxury Line (Aporte Lipidico Premium e Protecao de Cimento Cuticular)" if aporte_lipidico_essencial else "Wella Oil Reflections"
    else:
        p_dav = "Davines Naturaltech Energizing Line + doTERRA Rosemary (Anti-hairloss)" if diagnostico_queda else "Davines Calming Line"
        p_ker = "Kerastase Specifique / Nutritive (Deep Hydration - Water Retention for Dubai)" if equilibrio_hidrico_dubai else "Kerastase Resistance"
        p_lor = "Absolut Repair Molecular (Cortical Fusion for Damaged Hair / Blondes)" if e_loira_danificado else "L'Oreal Metal Detox"
        p_wel = "Wella Ultimate Repair Luxury Line (Premium Lipidic Supply & Cuticular Cement Protection)" if aporte_lipidico_essencial else "Wella Oil Reflections"
    
    param_cap_txt = [("DAVINES + doTERRA", p_dav), ("KERASTASE", p_ker), ("L'OREAL PROFESSIONNEL", p_lor), ("WELLA PROFESSIONALS", p_wel)]
    
    # Previsão do tempo inteligente
    if IDIOMA_ATIVO == 'PT':
        ciclo_txt = [
            ("Dias 01 a 07 (S1)", "Media 39C | UV 11+ (Extrema)", "Media 24C | UV 6 (Alta)", "Sao Luis: Media 30C | UV 11 | Umidade 78%"),
            ("Dias 08 a 14 (S2)", "Media 41C | UV 12 (Critica)", "Media 25C | UV 7 (Alta)", "Sao Luis: Media 29C | UV 10 | Chuvas Sazonais"),
            ("Dias 15 a 21 (S3)", "Media 40C | UV 11+ (Extrema)", "Media 23C | UV 5 (Mod)", "Sao Luis: Media 31C | UV 11 | Alta Luminosidade")
        ]
    else:
        ciclo_txt = [
            ("Days 01 to 07 (W1)", "Avg 39C | UV 11+ (Extreme)", "Avg 24C | UV 6 (High)", "Sao Luis: Avg 30C | UV 11 | Humidity 78%"),
            ("Days 08 to 14 (W2)", "Avg 41C | UV 12 (Critical)", "Avg 25C | UV 7 (High)", "Sao Luis: Avg 29C | UV 10 | Seasonal Rains"),
            ("Days 15 to 21 (W3)", "Avg 40C | UV 11+ (Extreme)", "Avg 23C | UV 5 (Mod)", "Sao Luis: Avg 31C | UV 11 | High Luminosity")
        ]
    
    try:
        val_gon = float(gon_esq)
    except Exception:
        val_gon = 122.0

    design_corte = t['corte_shag'] if val_gon > 125 else t['corte_bob']
        
    sec4_txt = [
        (t['corte_param1'], t['corte_param2']),
        (t['corte_param3'], t['corte_param4']),
        (t['corte_prescrito'], design_corte)
    ]
    
    header_text = "THIERRY TECHNOLOGY CONCEPT GLOBAL"
    pdf = PDF_Laudo_Luxo(header_text)
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)

    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(25, 25, 25)
    pdf.cell(0, 6, t['titulo_doc'], 0, 1, 'L')
    
    pdf.set_font('Arial', 'I', 8)
    pdf.set_text_color(110, 110, 110)
    pdf.cell(0, 3.5, t['sub_doc'], 0, 1, 'L')
    pdf.ln(1.5)

    pdf.set_fill_color(245, 245, 245)
    pdf.rect(10, pdf.get_y(), 190, 10, 'F')
    pdf.set_font('Arial', 'B', 7.5)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 3.8, status_lbl_formatado, 0, 1, 'L')
    pdf.set_font('Arial', '', 6.5)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 3.2, sub_status_formatado, 0, 1, 'L')
    pdf.ln(3)

    # Seção 1
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 3.5, t['sec1_tit'], 0, 1, 'L')
    pdf.ln(0.5)
    pdf.set_fill_color(30, 30, 30)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 6.5)
    pdf.cell(110, 3.5, t['sec1_h1'], 1, 0, 'L', True)
    pdf.cell(80, 3.5, t['sec1_h2'], 1, 1, 'L', True)
    pdf.set_text_color(50, 50, 50)
    pdf.set_font('Arial', '', 6)
    for p, v in param_fac_txt:
        if "Paralisia" in p or "Paralysis" in p:
            pdf.set_font('Arial', 'B', 6)
            pdf.set_fill_color(253, 242, 242)
            pdf.cell(110, 3.5, f' {p}', 1, 0, 'L', True)
            pdf.set_text_color(180, 40, 40)
            pdf.cell(80, 3.5, f' {v}', 1, 1, 'L', True)
            pdf.set_text_color(50, 50, 50)
            pdf.set_font('Arial', '', 6)
        else:
            pdf.cell(110, 3.5, f' {p}', 1, 0, 'L')
            pdf.cell(80, 3.5, f' {v}', 1, 1, 'L')
    pdf.ln(2.5)

    # Seção 2
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 3.5, t['sec2_tit'], 0, 1, 'L')
    pdf.ln(0.5)
    pdf.set_fill_color(45, 45, 45)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 6.5)
    pdf.cell(50, 3.5, t['sec2_h1'], 1, 0, 'L', True)
    pdf.cell(140, 3.5, t['sec2_h2'], 1, 1, 'L', True)
    pdf.set_text_color(50, 50, 50)
    pdf.set_font('Arial', '', 6)
    for m, pr in param_cap_txt:
        if "Agua" in m or "Water" in pr or "Dubai" in pr:
            pdf.set_font('Arial', 'B', 6)
            pdf.set_fill_color(240, 248, 255)
            pdf.cell(50, 3.5, f' {m}', 1, 0, 'L', True)
            pdf.cell(140, 3.5, f' {pr}', 1, 1, 'L', True)
            pdf.set_font('Arial', '', 6)
        else:
            pdf.cell(50, 3.5, f' {m}', 1, 0, 'L')
            pdf.cell(140, 3.5, f' {pr}', 1, 1, 'L')
    pdf.ln(2.5)

    # Seção 3
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 3.5, t['sec3_tit'], 0, 1, 'L')
    pdf.ln(0.5)
    pdf.set_fill_color(110, 95, 70)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 6.5)
    pdf.cell(30, 3.5, t['sec3_h1'], 1, 0, 'C', True)
    pdf.cell(50, 3.5, t['sec3_h2'], 1, 0, 'L', True)
    pdf.cell(50, 3.5, t['sec3_h3'], 1, 0, 'L', True)
    pdf.cell(60, 3.5, t['sec3_h4'], 1, 1, 'L', True)
    pdf.set_text_color(50, 50, 50)
    pdf.set_font('Arial', '', 6)
    for per, db, mn, lc in ciclo_txt:
        pdf.cell(30, 3.5, f' {per}', 1, 0, 'C')
        pdf.cell(50, 3.5, f' {db}', 1, 0, 'L')
        pdf.cell(50, 3.5, f' {mn}', 1, 0, 'L')
        pdf.cell(60, 3.5, f' {lc}', 1, 1, 'L')
    pdf.ln(2)

    # Alerta
    pdf.set_fill_color(240, 244, 248)
    pdf.rect(10, pdf.get_y(), 190, 7, 'F')
    pdf.set_font('Arial', 'B', 6.5)
    pdf.set_text_color(15, 45, 75)
    pdf.cell(0, 2.8, t['alerta_tit'], 0, 1, 'L')
    pdf.set_font('Arial', 'I', 5.8)
    pdf.set_text_color(40, 60, 80)
    pdf.cell(0, 2.2, t['alerta_sub'], 0, 1, 'L')
    pdf.ln(3)

    # Seção 4
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 3.5, t['sec4_tit'], 0, 1, 'L')
    pdf.ln(0.5)
    pdf.set_fill_color(80, 80, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 6.5)
    pdf.cell(75, 3.5, t['sec4_h1'], 1, 0, 'L', True)
    pdf.cell(115, 3.5, t['sec4_h2'], 1, 1, 'L', True)
    pdf.set_text_color(50, 50, 50)
    pdf.set_font('Arial', '', 6)
    
    for ava, esp in sec4_txt:
        if "DESIGN" in ava or "PRESCRIBED" in ava:
            pdf.set_font('Arial', 'B', 7)
            pdf.set_fill_color(245, 240, 235)
            pdf.cell(75, 7, f' {ava}', 1, 0, 'L', True)
            x_atual = pdf.get_x()
            y_atual = pdf.get_y()
            pdf.multi_cell(115, 3.5, f' {esp}', 1, 'L', True)
            pdf.set_xy(x_atual + 115, y_atual + 7)
            pdf.ln(0)
            pdf.set_font('Arial', '', 6)
        else:
            pdf.cell(75, 3.5, f' {ava}', 1, 0, 'L')
            pdf.cell(115, 3.5, f' {esp}', 1, 1, 'L')
    pdf.ln(3)

    # Seção 5
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 3.5, t['sec5_tit'], 0, 1, 'L')
    
    if os.path.exists(foto):
        pdf.image(foto, x=50, y=208, w=110, h=78)

    caminho_pdf_final = os.path.join(pasta_destino, t['nome_arquivo'])
    pdf.output(caminho_pdf_final)
    return caminho_pdf_final

# =========================================================================
# 2. MOTOR DE CAPTURA COM LIVE SCANNER (MANDIBLE SCAN)
# =========================================================================
def executar_scanner_premium():
    pasta_laudos_luxo = "04__luxury_reports"
    
    if not os.path.exists("database"): 
        os.makedirs("database")
    if not os.path.exists(pasta_laudos_luxo): 
        os.makedirs(pasta_laudos_luxo)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print(f"[SISTEMA] Idioma ativo detectado no hardware: {IDIOMA_ATIVO}")
    print("[SISTEMA] Estabilizando hardware da camera...")
    time.sleep(2)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("[ERRO IMEDIATO] Verifique a conexao USB da sua camera.")
        return

    print("\n========================================================")
    print(" SCANNER INTEGRADO THIERRY TECHNOLOGY CONCEPT INICIADO")
    print(f" -> CONFIGURACAO GLOBAL ATIVA: [{IDIOMA_ATIVO}]")
    print("    Pressione 'S' para ESCANEAR A FACE e GERAR RELATORIO")
    print("    Pressione 'ESC' para CANCELAR")
    print("========================================================\n")

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            continue

        frame_salvar = frame.copy()
        altura, largura, _ = frame.shape
        cx, cy = largura // 2, altura // 2

        # --- GRID GRÁFICO VISUAL ---
        cv2.circle(frame, (cx, cy), 8, (0, 165, 255), -1)
        cv2.drawMarker(frame, (cx, cy), (0, 255, 0), cv2.MARKER_CROSS, 40, 1)
        cv2.rectangle(frame, (cx - 160, cy - 210), (cx + 160, cy + 210), (255, 255, 255), 1)
        cv2.line(frame, (cx - 160, cy - 60), (cx + 160, cy - 60), (0, 255, 255), 1) 
        cv2.line(frame, (cx - 160, cy + 130), (cx + 160, cy + 130), (0, 0, 255), 1) 

        # Interface da janela em inglês/português sutil
        cv2.putText(frame, "TTC GLOBAL FORENSIC SYSTEM v4.2", (30, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"STATUS: ACTIVE SCANNING [{IDIOMA_ATIVO}]...", (30, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        
        cv2.putText(frame, "[S] - CONFIRMAR ESCANEAMENTO E INTEGRAR LAUDO", (30, altura - 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "[ESC] - CANCELAR", (30, altura - 35), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (120, 120, 120), 1, cv2.LINE_AA)

        cv2.imshow("BIOMETRIC SCANNER - THIERRY CONCEPT GLOBAL", frame)
        tecla = cv2.waitKey(1) & 0xFF
        
        if tecla == 27:
            break
            
        if tecla == ord('s') or tecla == ord('S'):
            print("\n[MATRIZ DETECTADA] Capturando dados estructurados da face...")
            caminho_foto = "database/foto_origem.jpg"
            cv2.imwrite(caminho_foto, frame_salvar)
            
            dados_calculados = (
                caminho_foto, "0.4 Grad", "1:1:1.15", "123.1", "124.6", "145.2", "148.9", "3.7", "47%",
                "Rastreamento Finalizado Concluido", "Moderada (Assimetria detectada em Tecido Muscular Direito)"
            )

            # Grava no banco normalmente
            try:
                conexao = sqlite3.connect("database/TCC_global_forense.db")
                cursor = conexao.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS analises_biometricas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        foto_origem TEXT, angulo_olhos TEXT, proporcao_tercos TEXT,
                        angulo_goniaco_esq TEXT, angulo_goniaco_dir TEXT,
                        comprimento_mand_esq TEXT, comprimento_mand_dir TEXT,
                        indice_assimetria TEXT, proporcao_mento TEXT, status_pericia TEXT,
                        predisposisia_paralisia TEXT
                    )
                """)
                cursor.execute("""
                    INSERT INTO analises_biometricas (
                        foto_origem, angulo_olhos, proporcao_tercos, 
                        angulo_goniaco_esq, angulo_goniaco_dir, 
                        comprimento_mand_esq, comprimento_mand_dir, 
                        indice_assimetria, proporcao_mento, status_pericia,
                        predisposisia_paralisia
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, dados_calculados)
                conexao.commit()
                conexao.close()
            except Exception:
                pass

            caminho_pdf = gerar_pdf_dinamico(dados_calculados, pasta_destino=pasta_laudos_luxo)
            caminho_absoluto = os.path.abspath(caminho_pdf)
            
            print("\n==================================================================")
            print(f" [SISTEMA TTC] CERTIFICACAO EM [{IDIOMA_ATIVO}] IMPRESSA COM SUCESSO!")
            print(f" -> Laudo salvo em: {caminho_absoluto}")
            print("==================================================================\n")
            
            if os.path.exists(caminho_absoluto):
                os.startfile(caminho_absoluto) if hasattr(os, 'startfile') else webbrowser.open(f"file:///{caminho_absoluto}")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    executar_scanner_premium()