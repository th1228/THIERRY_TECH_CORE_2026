import sys, os

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys, os

# -*- coding: utf-8 -*-
import cv2
import mediapipe as mp
import time
import winsound

# Importe os seus três motores (certifique-se de que eles estão na pasta core)
import analise_rosto
import analise_cabelo
import sensor_fadiga

def main():
    camera = cv2.VideoCapture(0)
    
    # Setup único do MediaPipe (compartilhado)
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
    
    print("[INFO] Sistema Integrado Iniciado. Pressione 'q' para sair.")

    while True:
        ret, frame = camera.read()
        if not ret: break

        # O MESTRE chama os motores passando o frame
        # Cada motor deve apenas desenhar no frame e retornar o frame modificado
        frame = analise_rosto.processar(frame)
        frame = analise_cabelo.processar(frame)
        frame = sensor_fadiga.processar(frame)

        cv2.imshow("THIERRY TECH - SISTEMA INTEGRADO", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()