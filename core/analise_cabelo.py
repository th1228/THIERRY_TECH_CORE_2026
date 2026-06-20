# -*- coding: utf-8 -*-
import cv2
import mediapipe as mp
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import motor_dados

# Variáveis globais de controle
congelado = False
dados_fixos = {"d": 0, "o": 0, "a": 0, "m": 0, "s": 0, "iq": 0}

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5)

def extrair_metricas_fixas(roi):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    d = np.sum(cv2.Canny(gray, 50, 150) > 0) / 10
    o = np.mean(gray)
    a = 100 - (np.std(roi) * 0.4)
    m = d * 0.8
    s = max(0, 100 - int(np.std(gray) * 0.8))
    iq = int(np.std(gray) * 0.8)
    return d, o, a, m, s, iq

def desenhar_micromalha(frame, lm):
    global congelado, dados_fixos
    h, w, _ = frame.shape
    cx, cy = int(lm.landmark[1].x * w), int(lm.landmark[1].y * h)
    y_queixo, y_testa = int(lm.landmark[152].y * h), int(lm.landmark[10].y * h)
    cor_ciano = (255, 255, 0)
    
    # Desenho da Micromalha
    for i in range(-40, 41): 
        x_pos = cx + (i * 3)
        cv2.line(frame, (x_pos, y_queixo), (x_pos, y_testa - 50), cor_ciano, 1, cv2.LINE_AA)
    for i in range(15):
        raio = 40 + (i * 8)
        cv2.ellipse(frame, (cx, cy), (raio, raio + 10), 0, 180, 360, cor_ciano, 1, cv2.LINE_AA)

    if not congelado:
        roi = frame[y_testa-50:y_testa+50, cx-50:cx+50]
        if roi.size > 0:
            d, o, a, m, s, iq = extrair_metricas_fixas(roi)
            dados_fixos = {"d": d, "o": o, "a": a, "m": m, "s": s, "iq": iq}
    
    # Painel com "IDADE FIO"
    cv2.rectangle(frame, (10, 380), (320, 480), (0, 0, 0), -1)
    cv2.putText(frame, f"DENS: {dados_fixos['d']:.1f} | MASSA: {dados_fixos['m']:.1f} | AGUA: {dados_fixos['a']:.1f}%", (20, 400), 0, 0.35, (255,255,255), 1)
    cv2.putText(frame, f"OLEO: {dados_fixos['o']:.1f} | SAUDE: {dados_fixos['s']:.1f}% | IDADE FIO: {dados_fixos['iq']:.0f} anos", (20, 425), 0, 0.35, (255,255,255), 1)
    status = "CONGELADO" if congelado else "CALCULANDO..."
    cv2.putText(frame, f"[ESPAC O] {status} | [S] SALVAR", (20, 455), 0, 0.4, cor_ciano, 1)

def capturar_analise():
    global congelado
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks:
            for lm in results.multi_face_landmarks:
                desenhar_micromalha(frame, lm)
        cv2.imshow("Bioarquitetura Capilar - Laudo Tecnico", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 32: congelado = not congelado
        elif key == ord('s'):
            motor_dados.salvar("diagnostico_final", dados_fixos)
            print("Diagnostico salvo com sucesso.")
        elif key == ord('q'): break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capturar_analise()