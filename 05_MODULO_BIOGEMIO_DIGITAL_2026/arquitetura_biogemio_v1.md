import cv2
import mediapipe as mp
import numpy as np

# Configuração de Identidade Visual Thierry Technology
COLOR_TTC = (127, 0, 255)  # Rosa/Roxo Luxo
COLOR_SCAN = (0, 255, 0)   # Verde de busca

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success: break

    image = cv2.flip(image, 1)
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # PONTOS CHAVE PARA O BIOGÊMEO (X, Y, Z)
            nose = face_landmarks.landmark[1]
            l_ear = face_landmarks.landmark[234]
            r_ear = face_landmarks.landmark[454]

            # CÁLCULO DE PROFUNDIDADE LATERAL
            depth_ratio = abs(l_ear.z - r_ear.z)
            
            if depth_ratio > 0.08:
                status = "BIOGEMEO: CAPTURANDO PROFUNDIDADE"
                current_color = COLOR_TTC
                # Aqui simularemos o envelhecimento futuro
            else:
                status = "POSICIONE O ROSTO DE LADO"
                current_color = COLOR_SCAN

            # HUD - INTERFACE DO USUÁRIO
            cv2.putText(image, status, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, current_color, 2)
            
            # DESENHO DA MALHA TTC (478 PONTOS)
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=current_color, thickness=1)
            )

    cv2.imshow('Thierry Tech - Deep Scan V1', image)
    if cv2.waitKey(5) & 0xFF == 27: break # ESC para sair

cap.release()
cv2.destroyAllWindows()