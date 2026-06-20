import cv2
import mediapipe as mp
import os
import winsound
from datetime import datetime

# Garante a pasta para o Plano Mônaco
PASTA = "04_luxury_reports"
if not os.path.exists(PASTA):
    os.makedirs(PASTA)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

VERDE_NEON = (0, 255, 0)
LINHA_COR = (0, 100, 0)
FONTE = cv2.FONT_HERSHEY_SIMPLEX

# Listas baseadas na sua imagem 275854.jpg
ESQUERDA = [
    "F1: Subcutaneous Fat 13mm", "F3: Dermal Thickness 1.1mm", 
    "F8: Adipose Dist. Index 0.7", "T2: Fascia Depth 23mm", 
    "T5: Bone Contour Anglo 95", "ER_2: Lid Thickness 0.8mm",
    "ER_1: Fasce Precs 9.5mm", "M1: Muscle Density (ratio)"
]

DIREITA = [
    "C_M1: Superficial Fat", "G_D2: Deep Fat 2.3mm",
    "MF1: Nasolabial Fold", "MF3: Maxillary Contour",
    "CF8: Lower Lip Fat 12mm", "CH1: Chin Length 102.8mm",
    "V1: Visagismo Index 9.8", "D1: Deep Tissue Analysis"
]

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    cv2.putText(frame, "DIAMANTE | MONACO PLAN", (w//2 - 150, 40), FONTE, 0.8, VERDE_NEON, 2)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Desenha os pontos no rosto
            for landmark in face_landmarks.landmark:
                cv2.circle(frame, (int(landmark.x * w), int(landmark.y * h)), 1, VERDE_NEON, -1)

            # LADO ESQUERDO
            for i, texto in enumerate(ESQUERDA):
                y = 80 + (i * 25)
                cv2.putText(frame, texto, (20, y), FONTE, 0.4, VERDE_NEON, 1)
                # Linha conectando ao rosto
                ponto = face_landmarks.landmark[10 + i]
                cv2.line(frame, (180, y-5), (int(ponto.x * w), int(ponto.y * h)), LINHA_COR, 1)

            # LADO DIREITO
            for i, texto in enumerate(DIREITA):
                y = 80 + (i * 25)
                cv2.putText(frame, texto, (w - 220, y), FONTE, 0.4, VERDE_NEON, 1)
                # Linha conectando ao rosto
                ponto = face_landmarks.landmark[150 + i]
                cv2.line(frame, (w - 230, y-5), (int(ponto.x * w), int(ponto.y * h)), LINHA_COR, 1)

    cv2.imshow("SCANNER TOTAL TTC", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        winsound.Beep(1000, 200) # BIP de captura
        timestamp = datetime.now().strftime("%H%M%S")
        cv2.imwrite(f"{PASTA}/Captura_{timestamp}.jpg", frame)
        with open(f"{PASTA}/Relatorio_Vip_{timestamp}.txt", "w") as f:
            f.write("BONE CONTOUR: Diamond\nVISAGISMO INDEX: 9.8\nMUSCLE DENSITY: High")
        print(f"Relatório e Foto salvos com Sucesso!")
    elif key == ord('q'): break

cap.release()
cv2.destroyAllWindows()