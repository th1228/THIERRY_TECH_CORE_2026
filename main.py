import cv2
import mediapipe as mp
import os
import winsound
import numpy as np
import shutil

# Identidade Visual Thierry Technology Concept
GOLD, PINK = (0, 215, 255), (147, 20, 255)
mp_face_mesh = mp.solutions.face_mesh
cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True) as face_mesh:
    print("\n" + "="*60)
    print("SISTEMA TTC GLOBAL - FULL HUD MATRIX ATIVADO")
    print("="*60)

    while cap.isOpened():
        success, image = cap.read()
        if not success: continue

        image = cv2.flip(image, 1)
        h, w, _ = image.shape
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_image)

        if results.multi_face_landmarks:
            for face in results.multi_face_landmarks:
                # --- O PULO DO GATO: INDEXAÇÃO DE TODOS OS 468 PONTOS NA TELA ---
                for i, lm in enumerate(face.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # Desenha o ponto
                    cv2.circle(image, (cx, cy), 1, PINK, -1)
                    # Desenha o número do índice (Muito pequeno para "encher" a tela)
                    cv2.putText(image, str(i), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.25, GOLD, 1)

                # Métricas de Bioperícia para o Dossiê
                glab_z = face.landmark[10].z * 100
                olho_abert = abs(face.landmark[159].y - face.landmark[145].y) * h

        cv2.putText(image, "TTC GLOBAL - HUD MATRIX SCAN", (20, 40), 1, 1.5, GOLD, 2)
        cv2.imshow('TTC Global - Scanner Pro', image)

        key = cv2.waitKey(1) & 0xFF
        if key == 27: break
        elif key == ord('s'):
            winsound.Beep(1300, 300)
            tk = np.random.randint(1000, 9999)
            
            # Relatório Integral (468 pontos + Decisão de Tratamento)
            with open(f"Dossie_Final_Matrix_{tk}.txt", "w", encoding="utf-8") as f:
                f.write("============== TTC GLOBAL - LAUDO TECNICO INTEGRAL ==============\n")
                f.write(f"PROTOCOLO: {tk} | MÉTODO: MÔNACO HUD SCAN\n\n")
                
                f.write("[MAPEAMENTO DE COORDENADAS 3D]\n")
                for i, lm in enumerate(face.landmark):
                    f.write(f"ID_{i:03}: X={lm.x:.4f} | Y={lm.y:.4f} | Z={lm.z:.4f}\n")

                f.write("\n[PLANO DE INTERVENÇÃO FINAL]\n")
                if glab_z > 0.45: f.write("- FOCO: Relaxamento da zona de irritabilidade (Glabela).\n")
                if olho_abert < 10: f.write("- FOCO: Abertura do olhar fadigado (Fox Eyes/Toxina).\n")
                f.write("\n============== FINAL DO DOSSIÊ 2026 ==============\n")

            print(f"[TTC GLOBAL]: Escaneamento {tk} arquivado na Pasta 04.")

cap.release()
cv2.destroyAllWindows()

def organizar_ambiente_luxury():
    origem, destino = ".", "04_luxury_reports"
    if not os.path.exists(destino): os.makedirs(destino)
    for f in os.listdir(origem):
        if f.startswith("Dossie_Final") or f.endswith(".jpg"):
            try: shutil.move(os.path.join(origem, f), os.path.join(destino, f))
            except: pass

organizar_ambiente_luxury()