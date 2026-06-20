import cv2
import mediapipe as mp
import numpy as np
import sqlite3
import datetime

class BiogenioDatabase:
    def __init__(self):
        # Conecta ao banco de dados (cria o arquivo se não existir)
        self.conn = sqlite3.connect('thierry_tech_biogenio.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS analises 
                             (id INTEGER PRIMARY KEY, data TEXT, hand_score REAL)''')
        self.conn.commit()

    def salvar(self, score):
        self.cursor.execute("INSERT INTO analises (data, hand_score) VALUES (?, ?)", 
                           (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), score))
        self.conn.commit()

class BiogenioCore:
    def __init__(self):
        self.db = BiogenioDatabase()
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

    def processar(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res_hands = self.hands.process(frame_rgb)
        
        if res_hands.multi_hand_landmarks:
            for hand_lms in res_hands.multi_hand_landmarks:
                # Cálculo de textura (ROI)
                h, w, c = frame.shape
                cx, cy = int(hand_lms.landmark[0].x * w), int(hand_lms.landmark[0].y * h)
                roi = frame[max(0, cy-50):min(h, cy+50), max(0, cx-50):min(w, cx+50)]
                score = np.std(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)) if roi.size > 0 else 0
                
                # Feedback visual
                cv2.putText(frame, f"SCORE: {score:.2f} | PRESSIONE 'S' PARA SALVAR", (20, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                
                return frame, score
        return frame, None

# Execução
cap = cv2.VideoCapture(0)
biogenio = BiogenioCore()

while True:
    success, frame = cap.read()
    if not success: break
    frame = cv2.flip(frame, 1)
    frame, score = biogenio.processar(frame)
    
    cv2.imshow("THIERRY TECH - BIOGENIO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s') and score is not None:
        biogenio.db.salvar(score)
        print(f"Dados salvos: {score}")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()