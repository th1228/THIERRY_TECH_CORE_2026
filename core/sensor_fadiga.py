# -*- coding: utf-8 -*-
import cv2
import mediapipe as mp
import datetime
import numpy as np

# --- NOVO: MÓDULO DE CLIMA ---
def obter_temp_ambiente():
    # Aqui você pode integrar com uma API de clima ou um sensor físico
    # Por enquanto, simulamos um valor (ex: 10 para frio intenso, 30 para calor)
    return 10 

def ajustar_biometria_clima(dados, temperatura):
    fadiga, assimetria, densidade, hidratacao = dados
    
    # Lógica de Cruzamento: Impacto no Frio (< 15°C)
    if temperatura < 15:
        # No frio, o corpo tensiona, aumentando a fadiga e diminuindo a hidratação da pele
        fadiga = min(fadiga + 2, 10)
        hidratacao = max(hidratacao - 2, 0)
        densidade = max(densidade - 1, 0) # Efeito de ressecamento
        status_clima = "CLIMA FRIO - Impacto aplicado"
    else:
        status_clima = "CLIMA QUENTE/NEUTRO - Normal"
        
    return (fadiga, assimetria, densidade, hidratacao), status_clima

# [Inicialização do MediaPipe permanece igual...]
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

def analisar_fenotipo(frame, landmarks, w, h):
    # 1. Fadiga Neural
    p1 = landmarks.landmark[10]
    p2 = landmarks.landmark[152]
    fadiga = int(min(((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5 * 10, 10))
    
    # 2. Assimetria Facial
    lado_dir = landmarks.landmark[234].y
    lado_esq = landmarks.landmark[454].y
    assimetria = abs(lado_dir - lado_esq) * 100
    
    # 3. Análise Capilar/Pele
    roi_cabelo = frame[0:int(h*0.25), 0:w]
    gray = cv2.cvtColor(roi_cabelo, cv2.COLOR_BGR2GRAY)
    densidade = np.sum(cv2.Canny(gray, 100, 200)) / 1000
    hidratacao = np.mean(roi_cabelo) / 25
    
    return fadiga, min(int(assimetria), 10), min(int(densidade), 10), min(int(hidratacao), 10)

def rodar_scanner():
    cam = cv2.VideoCapture(0)
    print("Iniciando varredura com modulação climática...")
    
    dados = (5, 0, 5, 5)
    while True:
        ret, frame = cam.read()
        if not ret: break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        h, w, _ = frame.shape
        
        if results.multi_face_landmarks:
            for lm in results.multi_face_landmarks:
                dados = analisar_fenotipo(frame, lm, w, h)
        
        # --- APLICAÇÃO DA MODULAÇÃO CLIMÁTICA ---
        temp = obter_temp_ambiente()
        dados_ajustados, msg = ajustar_biometria_clima(dados, temp)
        
        cv2.putText(frame, f"FADIGA: {dados_ajustados[0]} | ASSIMETRIA: {dados_ajustados[1]}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"DENSIDADE: {dados_ajustados[2]} | HIDRATACAO: {dados_ajustados[3]}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.imshow('THIERRY_TECH_CORE - MODULACAO ATIVA', frame)
        
        k = cv2.waitKey(1)
        if k % 256 == 32: # ESPACO
            cam.release()
            cv2.destroyAllWindows()
            return dados_ajustados # Retorna o dado já com o impacto do frio
        elif k % 256 == 113: # Q
            break
    cam.release()
    cv2.destroyAllWindows()
    return None

if __name__ == "__main__":
    resultado = rodar_scanner()
    if resultado:
        agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with open("log_performance.txt", "a", encoding="utf-8") as f:
            f.write(f"{agora} | Fadiga:{resultado[0]} | Assimetria:{resultado[1]} | Densidade:{resultado[2]} | Hidratacao:{resultado[3]}\n")
        print(f"[OK] Dados modulados gravados com sucesso.")