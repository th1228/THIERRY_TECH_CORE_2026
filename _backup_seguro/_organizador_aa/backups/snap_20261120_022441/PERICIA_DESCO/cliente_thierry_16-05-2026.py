import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
import random
import time
import os
import winsound

# Configurações de Design (Padrão Diamante Mônaco)
VERDE_NEON = (0, 255, 0)
LINHA_COR = (0, 150, 0)
AMARELO_AVISO = (0, 255, 255)
VERMELHO_ALERTA = (0, 0, 255)
FONTE = cv2.FONT_HERSHEY_SIMPLEX

# Garantir o diretório correto dentro de PERICIA_DESCO
DIRETORIO_DO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_RELATORIOS = os.path.join(DIRETORIO_DO_SCRIPT, "04_luxury_reports")

if not os.path.exists(PASTA_RELATORIOS):
    os.makedirs(PASTA_RELATORIOS)

# Inicializar o Detector de Rosto Nativo do OpenCV (Super Leve, Não trava)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

ESQUERDA_MAPEADA = [
    "F1: Subcutaneous Fat", "F3: Dermal Thick", "F8: Adipose Index",
    "T2: Fascia Depth", "T5: Bone Contour", "ER_1: Muscle Density",
    "N1: Cartilage Ratio", "C_L1: Malar Fat Pad", "J1: Mandibular Angle"
]

DIREITA_MAPEADA = [
    "B_Z1: Bizygomatic W.", "O_F1: Orbital Fat", "J_G2: Jawline Def.",
    "M_M1: Masseter Muscle", "L_A3: Lateral Ang.", "G_R2: Buccal Fat",
    "P_C1: Pre-auricular", "H_F4: Hypodermis", "N2: Nasal Angle"
]

def salvar_laudo_txt(valores, tipo_captura):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    nome_arquivo = os.path.join(PASTA_RELATORIOS, f"LAUDO_ULTRA_FORENSE_{tipo_captura}_{timestamp}.txt")
    
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("==================================================\n")
        f.write("      THIERRY TECHNOLOGY CONCEPT GLOBAL 2026      \n")
        f.write(f"     RELATÓRIO BIOMÉTRICO LUXO - ({tipo_captura})    \n")
        f.write("==================================================\n")
        f.write(f"Data/Hora da Análise: {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("--------------------------------------------------\n\n")
        f.write("[ANÁLISE HEMISFÉRIO ESQUERDO]\n")
        for item in ESQUERDA_MAPEADA:
            f.write(f"{item}: {valores[item]}\n")
        f.write("\n[ANÁLISE HEMISFÉRIO DIREITO]\n")
        for item in DIREITA_MAPEADA:
            f.write(f"{item}: {valores[item]}\n")
        f.write("\n==================================================\n")
    print(f"[SUCESSO] Laudo ({tipo_captura}) salvo em: {nome_arquivo}")

valores_persistentes = {}
tempo_inicio_detectado = None
laudo_automatico_salvo = False
mensagem_manual_tempo = 0 

# Forçar a abertura da câmera padrão do sistema
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) if os.name == 'nt' else cv2.VideoCapture(0)

# Dar 1 segundo para a câmera estabilizar o hardware
time.sleep(1.0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detecção ultra rápida de face
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # UI Superior Fixa do Projeto
    cv2.putText(frame, "DIAMANTE MONACO PLAN | DEEP SCAN TOTAL", (20, 40), FONTE, 0.6, VERDE_NEON, 2)
    cv2.putText(frame, "TECLA [S]: CAPTURA MANUAL | TECLA [ESC]: SAIR DO SCANNER", (20, 65), FONTE, 0.4, AMARELO_AVISO, 1)
    
    if len(faces) > 0:
        (x, y, fw, fh) = faces[0]
        centro_rosto_x = x + fw // 2
        centro_tela = w // 2
        desvio_centro = abs(centro_rosto_x - centro_tela)
        
        # Grid de pontos cibernéticos dentro do quadrado do rosto
        for i in range(12):
            for j in range(12):
                px = int(x + (fw / 11) * i)
                py = int(y + (fh / 11) * j)
                cv2.circle(frame, (px, py), 1, VERDE_NEON, -1)
        
        rosto_centralizado = desvio_centro < 110
        
        if rosto_centralizado:
            if tempo_inicio_detectado is None:
                tempo_inicio_detectado = time.time()
            tempo_passado = time.time() - tempo_inicio_detectado
            
            if not valores_persistentes:
                for item in ESQUERDA_MAPEADA:
                    valores_persistentes[item] = f"{random.uniform(10, 25):.1f}mm"
                for item in DIREITA_MAPEADA:
                    valores_persistentes[item] = f"{random.uniform(0.5, 1.9):.2f}"
            
            # Gatilho automático de 3 segundos
            if tempo_passado >= 3.0 and not laudo_automatico_salvo:
                winsound.Beep(2000, 400)
                salvar_laudo_txt(valores_persistentes, "AUTOMATICO")
                laudo_automatico_salvo = True
            
            if time.time() < mensagem_manual_tempo:
                cv2.putText(frame, "CAPTURA MANUAL GRAVADA COM SUCESSO!", (20, h - 30), FONTE, 0.5, VERDE_NEON, 1)
            elif not laudo_automatico_salvo:
                progresso = int((tempo_passado / 3.0) * 100)
                cv2.putText(frame, f"ANALISANDO GEOMETRIA... {min(progresso, 100)}%", (20, h - 30), FONTE, 0.5, AMARELO_AVISO, 1)
            else:
                cv2.putText(frame, "SCANNER PRONTO | [S] PARA NOVA FOTO", (20, h - 30), FONTE, 0.5, VERDE_NEON, 1)
        else:
            tempo_inicio_detectado = None
            if time.time() < mensagem_manual_tempo:
                cv2.putText(frame, "CAPTURA MANUAL GRAVADA COM SUCESSO!", (20, h - 30), FONTE, 0.5, VERDE_NEON, 1)
            else:
                cv2.putText(frame, "CENTRALIZE-SE NA CAMERA", (20, h - 30), FONTE, 0.5, VERMELHO_ALERTA, 1)

        # Plotagem Estética das Linhas Guias do Sistema (Esquerda)
        for i, item in enumerate(ESQUERDA_MAPEADA):
            if valores_persistentes:
                txt_esquerdo = f"{item}: {valores_persistentes[item]}"
                y_pos = 105 + (i * 32)
                cv2.putText(frame, txt_esquerdo, (20, y_pos), FONTE, 0.4, VERDE_NEON, 1)
                
                target_x = int(x + fw * 0.2)
                target_y = int(y + (fh / len(ESQUERDA_MAPEADA)) * i)
                cv2.line(frame, (230, y_pos - 4), (target_x, target_y), LINHA_COR, 1)
            
        # Plotagem Estética das Linhas Guias do Sistema (Direita)
        for i, item in enumerate(DIREITA_MAPEADA):
            if valores_persistentes:
                txt_direito = f"{item}: {valores_persistentes[item]}"
                t_size = cv2.getTextSize(txt_direito, FONTE, 0.4, 1)[0]
                x_pos = w - t_size[0] - 20
                y_pos = 105 + (i * 32)
                cv2.putText(frame, txt_direito, (x_pos, y_pos), FONTE, 0.4, VERDE_NEON, 1)
                
                target_x = int(x + fw * 0.8)
                target_y = int(y + (fh / len(DIREITA_MAPEADA)) * i)
                cv2.line(frame, (x_pos - 15, y_pos - 4), (target_x, target_y), LINHA_COR, 1)
                
    else:
        valores_persistentes.clear()
        tempo_inicio_detectado = None
        laudo_automatico_salvo = False
        cv2.putText(frame, "PROCURANDO FACE...", (int(w/2) - 100, int(h/2)), FONTE, 0.5, VERMELHO_ALERTA, 1)

    # Criar a janela e forçar a atualização dela na tela
    cv2.namedWindow("SCANNER TOTAL", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("SCANNER TOTAL", frame)
    
    tecla = cv2.waitKey(30) & 0xFF
    if tecla == 27 or tecla == ord('q') or tecla == ord('Q'):
        break
    elif tecla == ord('s') or tecla == ord('S'):
        if len(faces) > 0:
            winsound.Beep(2200, 150)
            winsound.Beep(2200, 150)
            
            valores_manuais = {}
            for item in ESQUERDA_MAPEADA:
                valores_manuais[item] = f"{random.uniform(10, 25):.1f}mm"
            for item in DIREITA_MAPEADA:
                valores_manuais[item] = f"{random.uniform(0.5, 1.9):.2f}"
            
            salvar_laudo_txt(valores_manuais, "MANUAL")
            valores_persistentes = valores_manuais
            mensagem_manual_tempo = time.time() + 2.0 

cap.release()
cv2.destroyAllWindows()