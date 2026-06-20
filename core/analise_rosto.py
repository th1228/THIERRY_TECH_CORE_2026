# -*- coding: utf-8 -*-
import cv2
import mediapipe as mp
import numpy as np
import winsound
import warnings
import time
import serial  # Certifique-se de ter instalado: pip install pyserial

# Configuração Segura do Motor
motor = None
motor_conectado = False
try:
    motor = serial.Serial('COM3', 9600, timeout=1)
    motor_conectado = True
    print("Motor conectado na porta COM3.")
except:
    print("Motor não detectado. O programa continuará funcionando normalmente.")

# Bloqueia avisos
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5)

def desenhar_scanner_denso(frame, lm):
    h, w, _ = frame.shape
    pos_y = int((cv2.getTickCount() / cv2.getTickFrequency() * 150) % h)
    
    for landmark in lm.landmark:
        x, y = int(landmark.x * w), int(landmark.y * h)
        
        # Área de detecção do scanner
        if abs(y - pos_y) < 25:
            cv2.circle(frame, (x, y), 4, (255, 255, 0), -1)
        else:
            cv2.circle(frame, (x, y), 2, (100, 50, 0), -1)

def gerar_flash(frame):
    return np.full(frame.shape, 255, dtype=np.uint8)

def rodar_scanner():
    cap = cv2.VideoCapture(0)
    flash_ativo = False
    flash_tempo_inicio = 0
    flash_duracao = 0.05 

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        
        # Filtro de cor azulado
        frame[:, :, 0] = np.clip(frame[:, :, 0] + 60, 0, 255)
        
        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks:
            for lm in results.multi_face_landmarks:
                desenhar_scanner_denso(frame, lm)
                
        # Lógica do flash na tela
        if flash_ativo:
            if (time.time() - flash_tempo_inicio) < flash_duracao:
                frame = gerar_flash(frame)
            else:
                flash_ativo = False

        cv2.imshow("TTC CORE - SCANNER DENSO", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        # Tecla 's' para salvar, bipar, flash e acionar motor
        if key == ord('s'):
            winsound.Beep(1200, 300)      # Bipe
            flash_ativo = True            # Ativa flash visual
            flash_tempo_inicio = time.time()
            
            # Salva o frame
            cv2.imwrite("scan_final_denso.jpg", frame)
            
            # Comando para o motor
            if motor_conectado:
                motor.write(b'1')
            print("Captura salva e comando enviado ao motor.")
            
        elif key == ord('q'): 
            break
            
    cap.release()
    cv2.destroyAllWindows()
    if motor_conectado: motor.close()

if __name__ == "__main__":
    try:
        rodar_scanner()
    except Exception as e:
        print(f"Erro ao rodar o scanner: {e}")