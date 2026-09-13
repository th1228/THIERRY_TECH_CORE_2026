import sys, os

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys, os

import cv2
import mediapipe as mp
import subprocess

def executar_analise_e_abrir_laudo(nome_cliente):
    print(f"\n--- Iniciando motor de analise para: {nome_cliente} ---")
    try:
        subprocess.run(["python", "core/analise.py"], check=True)
    except Exception as e:
        print(f"Erro: {e}")

# Configuração do Scanner
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)

cap = cv2.VideoCapture(0)
nome_cliente_input = input("Digite o nome completo do cliente para iniciar: ")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)
    h, w, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)

    # EFEITO NEON: Renderização de pontos de luz
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for lm in face_landmarks.landmark:
                # Pontos fluorescentes (Borda amarela/limão brilhante)
                cv2.circle(image, (int(lm.x * w), int(lm.y * h)), 1, (0, 255, 255), 1)

    cv2.imshow('TTC - Cybernetic Scan Engine', image)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s') or key == ord('S'):
        cap.release()
        cv2.destroyAllWindows()
        executar_analise_e_abrir_laudo(nome_cliente_input)
        break
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()