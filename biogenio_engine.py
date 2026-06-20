# -*- coding: utf-8 -*-
import cv2
import mediapipe as mp
import numpy as np
import os

# Inicializa o MediaPipe
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(refine_landmarks=True)

def rodar_biogenio():
    cam = cv2.VideoCapture(0)
    anos = 5
     
    # Cria janela e trackbar
    cv2.namedWindow("BIOGENIO TTC - ANALISE NEURAL")
    def nada(x): global anos; anos = x
    cv2.createTrackbar("Anos", "BIOGENIO TTC - ANALISE NEURAL", 5, 15, nada)
    
    print("Sistema Ativo. [S] p/ Salvar | [Q] p/ Sair")
    
    while True:
        ret, frame = cam.read()
        if not ret: break
        
        # Processamento
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        
        # Montagem da tela (1280x480)
        tela = np.zeros((480, 1280, 3), dtype=np.uint8)
        tela[0:480, 0:640] = cv2.resize(frame, (640, 480))
        
        # Simulação com pontos
        img_pontos = frame.copy()
        if results.multi_face_landmarks:
            for fl in results.multi_face_landmarks:
                for idx, lm in enumerate(fl.landmark):
                    h, w, _ = img_pontos.shape
                    cor = (255, 255, 0) if idx % 2 == 0 else (255, 0, 255)
                    cv2.circle(img_pontos, (int(lm.x*w), int(lm.y*h)), 2, cor, -1)
        
        tela[0:480, 640:1280] = cv2.resize(img_pontos, (640, 480))
        
        # Informações
        cv2.putText(tela, f"PROJECAO: +{anos} ANOS", (660, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(tela, "[S] SALVAR  [Q] SAIR", (1000, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        cv2.imshow("BIOGENIO TTC - ANALISE NEURAL", tela)
        
        # Controle
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'): break
        elif k == ord('s'): 
            nome_arquivo = f"diagnostico_{anos}anos.jpg"
            cv2.imwrite(nome_arquivo, tela)
            print(f"Salvo: {os.path.abspath(nome_arquivo)}")

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    rodar_biogenio()