# -*- coding: utf-8 -*-
import cv2
import mediapipe as mp
import winsound
import numpy as np
import os

# --- CONFIGURAÇÃO INICIAL ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

# Garantir que a pasta exista
if not os.path.exists("Arquivos_TTC"): os.makedirs("Arquivos_TTC")

print("Scanner pronto. Pressione S para salvar ou Q para sair.")

while True:
    ret, frame = cap.read()
    if not ret: break
    
    frame = cv2.flip(frame, 1)
    
    # Processamento facial
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    
    if results.multi_face_landmarks:
        for face in results.multi_face_landmarks:
            for lm in face.landmark:
                h, w, _ = frame.shape
                cv2.circle(frame, (int(lm.x*w), int(lm.y*h)), 1, (50, 255, 120), -1)

    cv2.imshow("TTC - Cybernetic Scan Engine", frame)

    # --- LEITURA FORÇADA DE TECLA ---
    k = cv2.waitKey(10) # Aumentado para 10ms para garantir a leitura
    if k & 0xFF == ord('s'):
        winsound.Beep(1000, 500)
        cv2.imwrite("Arquivos_TTC/captura_rosto.jpg", frame)
        print("SALVO COM SUCESSO!")
        break
    elif k & 0xFF == ord('q'):
        print("SAINDO...")
        break

cap.release()
cv2.destroyAllWindows()