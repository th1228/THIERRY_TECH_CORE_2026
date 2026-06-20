import cv2
import mediapipe as mp
import numpy as np
import time
import random

# Configuração de Cores TTC Global - LUXO
COLOR_FIXO = (255, 255, 0)      # Azul Ciano (Base)
COLOR_SCANNER = (220, 220, 220) # Prata Brilhante
COLOR_GOLD_NEON = (0, 215, 255) # Dourado Forte
COLOR_LILAS = (255, 0, 255)     # Lilás (Números e Setas)
COLOR_WHITE = (255, 255, 255)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)
scan_pos = 0

while cap.isOpened():
    success, image = cap.read()
    if not success: break
    
    h, w, _ = image.shape
    image = cv2.flip(image, 1)
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Velocidade do Scanner
    scan_pos += 12
    if scan_pos > h: scan_pos = 0

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for i, landmark in enumerate(face_landmarks.landmark):
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                
                # Desenha a malha base
                cv2.circle(image, (cx, cy), 1, COLOR_FIXO, -1)
                
                # Efeito de Números e Setas acompanhando o Scanner
                if abs(cy - scan_pos) < 25:
                    # Setas Lilás
                    cv2.arrowedLine(image, (cx + 10, cy - 10), (cx, cy), COLOR_LILAS, 1, tipLength=0.3)
                    
                    # Números pequenos e brilhantes "flutuando" (Efeito Matrix/Forense)
                    if i % 5 == 0: # Coloca números em alguns pontos para não travar
                        valor_aleatorio = str(random.randint(10, 99))
                        cv2.putText(image, valor_aleatorio, (cx + 12, cy), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, COLOR_LILAS, 1)

            # Captura e Relatório
            key = cv2.waitKey(5) & 0xFF
            if key == ord('s'):
                # BIP do Sistema
                print('\a') # Emite o som de BIP padrão do Windows/Linux
                
                # Flash de captura
                cv2.rectangle(image, (0,0), (w,h), COLOR_WHITE, -1)
                cv2.imshow('SISTEMA MONACO', image)
                cv2.waitKey(100)
                
                protocolo = int(time.time())
                # Salva o relatório com os 468 pontos
                with open(f"Relatorio_Full_Forense_{protocolo}.txt", "w") as f:
                    f.write(f"=== TTC GLOBAL - LAUDO TECNICO LUXO ===\n")
                    for idx, lm in enumerate(face_landmarks.landmark):
                        f.write(f"Ponto {idx:03}: X={lm.x:.6f} | Y={lm.y:.4f} | Z={lm.z:.6f}\n")
                
                cv2.imwrite(f"SCAN_MONACO_{protocolo}.png", image)
                print(f"BIP! Dados Forenses Arquivados.")

    # Rodapé Internacional
    paises = "MONACO | USA | SWITZERLAND | FRANCE | BRAZIL | UK | UAE | JAPAN"
    cv2.putText(image, paises, (30, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_WHITE, 1)
    cv2.putText(image, "TTC GLOBAL - SCAN LUXO V4", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_GOLD_NEON, 2)
    
    cv2.imshow('SISTEMA MONACO', image)
    if cv2.waitKey(5) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()