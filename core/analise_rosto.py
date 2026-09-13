# -*- coding: utf-8 -*-
import sys
import os
import cv2
import mediapipe as mp
import numpy as np

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def registrar(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(refine_landmarks=True, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Visual: Azul Ciano Neon (Pontos apenas, sem malha)
cyan_spec = mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=1, circle_radius=1)

def classificar_formato(lm):
    # Largura (pontas da mandíbula/têmpora) e Altura (topo ao queixo)
    largura = abs(lm[234].x - lm[454].x)
    altura = abs(lm[10].y - lm[152].y)
    proporcao = altura / (largura + 1e-6)
    
    if proporcao < 1.1: return "QUADRADO"
    if proporcao < 1.25: return "QUADRADO"
    if proporcao > 1.5: return "ALONGADO"
    return "OVAL"

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    if frame is None:
        return {"status": "Frame não fornecido"}

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # DESENHA APENAS OS PONTOS (Sem conexões/malha)
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=None,  
                landmark_drawing_spec=cyan_spec)

        lm = results.multi_face_landmarks[0].landmark
        formato = classificar_formato(lm)
        proporcao_val = round(abs(lm[10].y - lm[152].y) / abs(lm[234].x - lm[454].x), 2)
        
        status_rosto = {"FORMATO": formato, "PROPORCAO": proporcao_val}
        
        # Sincronização segura com a Memória Comum 🧠
        try:
            if hasattr(memoria, 'salvar_dados'):
                memoria.salvar_dados("ROSTO_STATUS", status_rosto)
            elif hasattr(memoria, 'registrar'):
                memoria.registrar("ROSTO_STATUS", status_rosto)
        except Exception:
            pass
        
        # Texto Neon Ciano 👁️
        cv2.putText(frame, f"TIPO: {formato}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    return frame

if __name__ == "__main__":
    print("Módulo analise_rosto inicializado com sucesso.")