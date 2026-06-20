import cv2
import mediapipe as mp
import numpy as np
import winsound
from datetime import datetime

# Configuração do MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

def calcular_dist(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

while cap.isOpened():
    success, image = cap.read()
    if not success: break

    image = cv2.flip(image, 1)
    h, w, _ = image.shape
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    relatorio_dados = {}

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # 1. MÁSCARA DE PONTOS DE LUZ PINK
            for lm in face_landmarks.landmark:
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(image, (cx, cy), 1, (255, 0, 255), -1)

            # 2. DEFINIÇÃO DAS 10 MEDIÇÕES DIVIDIDAS
            # Lado Esquerdo (Saída para a esquerda da tela)
            medidas_esq = {
                "SOBRANCELHA_ESQ": (70, 105),
                "OLHO_ESQ": (33, 133),
                "MANDIBULA_ESQ": (172, 136),
                "ASA_NARIZ_ESQ": (102, 2),
                "CANTO_BOCA_ESQ": (61, 0)
            }
            # Lado Direito (Saída para a direita da tela)
            medidas_dir = {
                "SOBRANCELHA_DIR": (300, 334),
                "OLHO_DIR": (362, 263),
                "MANDIBULA_DIR": (397, 365),
                "ASA_NARIZ_DIR": (331, 2),
                "CANTO_BOCA_DIR": (291, 0)
            }

            # Desenhar Medidas da Esquerda
            y_off_esq = 100
            for nome, (idx1, idx2) in medidas_esq.items():
                p1, p2 = face_landmarks.landmark[idx1], face_landmarks.landmark[idx2]
                pos1, pos2 = (int(p1.x * w), int(p1.y * h)), (int(p2.x * w), int(p2.y * h))
                dist = calcular_dist(pos1, pos2)
                relatorio_dados[nome] = round(dist, 2)

                cv2.line(image, pos1, (180, y_off_esq), (255, 255, 0), 1)
                cv2.putText(image, f"{nome}: {relatorio_dados[nome]}", (10, y_off_esq), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)
                y_off_esq += 40

            # Desenhar Medidas da Direita
            y_off_dir = 100
            for nome, (idx1, idx2) in medidas_dir.items():
                p1, p2 = face_landmarks.landmark[idx1], face_landmarks.landmark[idx2]
                pos1, pos2 = (int(p1.x * w), int(p1.y * h)), (int(p2.x * w), int(p2.y * h))
                dist = calcular_dist(pos1, pos2)
                relatorio_dados[nome] = round(dist, 2)

                cv2.line(image, pos1, (w - 180, y_off_dir), (255, 255, 0), 1)
                cv2.putText(image, f"{nome}: {relatorio_dados[nome]}", (w - 175, y_off_dir), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)
                y_off_dir += 40

    # Interface de Luxo
    cv2.putText(image, "TTC GLOBAL SYSTEM - BIOMETRIA SIMETRICA", (20, 40), 
                cv2.FONT_HERSHEY_TRIPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(image, "- TECNOLOGIA LUXO", (20, h - 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow('TTC GLOBAL SYSTEM', image)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        winsound.Beep(1200, 200) # Apito de captura
        data = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"Relatorio_Simetria_{data}.txt", "w") as f:
            f.write("TTC GLOBAL SYSTEM - ANALISE DE SIMETRIA FACIAL\n")
            f.write("="*45 + "\n")
            for m, v in relatorio_dados.items():
                f.write(f"{m.ljust(25)}: {v} px\n")
        cv2.imwrite(f"Captura_Simetrica_{data}.jpg", image)
        print("✅ Analise completa salva!")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()