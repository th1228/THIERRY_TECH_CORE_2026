# -*- coding: utf-8 -*-
import cv2
import mediapipe as mp
import math
import time

class CameraEngine:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(refine_landmarks=True)
        self.t_inicio = time.time()
        
        # CORES (BGR)
        self.COR_BASE_CANAVIAL = (50, 255, 100)
        self.COR_LASER_ELETRICO = (255, 255, 0)

    def processar_frame(self, frame):
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        t = (time.time() - self.t_inicio) * 3.5 
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                centro_x = 0.5 + 0.4 * math.sin(t * 0.9)
                centro_y = 0.5 + 0.4 * math.cos(t * 1.3)

                for lm in face_landmarks.landmark:
                    px, py = int(lm.x * w), int(lm.y * h)
                    dist = math.sqrt((lm.x - centro_x)**2 + (lm.y - centro_y)**2)
                    if dist < 0.18: 
                        cv2.circle(frame, (px, py), 2, self.COR_LASER_ELETRICO, -1, cv2.LINE_AA)
                    else:
                        cv2.circle(frame, (px, py), 1, self.COR_BASE_CANAVIAL, -1, cv2.LINE_AA)
        return frame

# --- FUNÇÃO DE TESTE E AUTONOMIA ---
if __name__ == "__main__":
    print("Iniciando modo de teste: Câmera Engine...")
    cap = cv2.VideoCapture(0)
    engine = CameraEngine()
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        frame = engine.processar_frame(frame)
        cv2.imshow("TESTE DE ENGINE: TTC ELITE", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()