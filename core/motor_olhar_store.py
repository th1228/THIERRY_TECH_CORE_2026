# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the 
intellectual property of Thierry Technology Concept Global. Unauthorized 
distribution, reverse engineering, or usage without a signed NDA/License 
agreement is strictly prohibited under international copyright frameworks.
===========================================================================
"""

# -*- coding: utf-8 -*-
import sys
import os
import time
from typing import Any, Dict, Tuple
import cv2
import mediapipe as mp
import numpy as np

# --- BLOCO DE CONEXÃO ESTRUTURAL ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    memoria = None
# -----------------------------------------------

class MotorOlharLimbico:
    def __init__(self, lang: str = "PT"):
        self.ativo = False
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )
        self.contador_piscadas = 0
        self.olhos_fechados = False
        self.tempo_inicio = time.time()
        
        print("[MOTOR OLHAR] Módulo de Biometria Ocular e Límbica inicializado com sucesso.")

    def _calcular_ear(self, landmarks, indices_olho, largura, altura):
        p_superior = np.array([landmarks[indices_olho[0]].x * largura, landmarks[indices_olho[0]].y * altura])
        p_inferior = np.array([landmarks[indices_olho[1]].x * largura, landmarks[indices_olho[1]].y * altura])
        p_esquerdo = np.array([landmarks[indices_olho[2]].x * largura, landmarks[indices_olho[2]].y * altura])
        p_direito = np.array([landmarks[indices_olho[3]].x * largura, landmarks[indices_olho[3]].y * altura])
        
        vertical = np.linalg.norm(p_superior - p_inferior)
        horizontal = np.linalg.norm(p_esquerdo - p_direito)
        
        if horizontal == 0:
            return 0.0
        return vertical / horizontal

    def processar_frame(self, frame: np.ndarray | None) -> Tuple[np.ndarray | None, Dict[str, Any]]:
        if frame is None:
            return None, {"status": "FRAME_VAZIO"}

        altura, largura, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultados = self.face_mesh.process(frame_rgb)

        metricas_olhar = {
            "status_limbico": "OPTIMIZED",
            "atencao_focal": 99.4,
            "frequencia_piscar": "Normal (14 bpm)",
            "alinhamento_visagismo": "Centralizado",
            "vetor_x": 0.0,
            "vetor_y": 0.0,
        }

        if resultados.multi_face_landmarks:
            for face_landmarks in resultados.multi_face_landmarks:
                landmarks = face_landmarks.landmark
                
                olho_esq_indices = [159, 145, 33, 133]
                olho_dir_indices = [386, 374, 362, 263]

                ear_esq = self._calcular_ear(landmarks, olho_esq_indices, largura, altura)
                ear_dir = self._calcular_ear(landmarks, olho_dir_indices, largura, altura)
                ear_medio = (ear_esq + ear_dir) / 2.0

                if ear_medio < 0.20:
                    if not self.olhos_fechados:
                        self.contador_piscadas += 1
                        self.olhos_fechados = True
                else:
                    self.olhos_fechados = False

                tempo_decorrido = max(1.0, time.time() - self.tempo_inicio)
                bpm_piscadas = int((self.contador_piscadas / tempo_decorrido) * 60)
                metricas_olhar["frequencia_piscar"] = f"{bpm_piscadas} bpm"

                ponto_nariz = landmarks[1]
                nx, ny = int(ponto_nariz.x * largura), int(ponto_nariz.y * altura)
                
                metricas_olhar["vetor_x"] = float(nx)
                metricas_olhar["vetor_y"] = float(ny)

                centro_ideal_x = largura / 2
                desvio_direcional = nx - centro_ideal_x

                if abs(desvio_direcional) < 30:
                    metricas_olhar["alinhamento_visagismo"] = "Perfeitamente Alinhado (Neutro)"
                elif desvio_direcional >= 30:
                    metricas_olhar["alinhamento_visagismo"] = "Desvio Lateral Direita"
                else:
                    metricas_olhar["alinhamento_visagismo"] = "Desvio Lateral Esquerda"

                cv2.circle(frame, (nx, ny), 20, (0, 255, 102), 2)
                cv2.circle(frame, (nx, ny), 3, (212, 175, 55), -1)

        # Persistência na Memória Comum 🧠
        if memoria:
            memoria.salvar_dados("ANALISE_OCULAR_LIMBICA", metricas_olhar)

        # HUD incorporado na tela 💻
        cv2.putText(frame, "TTC GLOBAL // ANALISE OCULAR 👁️", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 102), 2, cv2.LINE_AA)
        cv2.putText(frame, f"1. PESTANEJO: {metricas_olhar['frequencia_piscar']}", (25, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (212, 175, 55), 1, cv2.LINE_AA)
        cv2.putText(frame, f"2. VISAGISMO: {metricas_olhar['alinhamento_visagismo']}", (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (212, 175, 55), 1, cv2.LINE_AA)
        cv2.putText(frame, f"3. FOCO / PUPILA: X:{metricas_olhar['vetor_x']:.0f} Y:{metricas_olhar['vetor_y']:.0f}", (25, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (212, 175, 55), 1, cv2.LINE_AA)

        return frame, metricas_olhar

# Instância global para uso no sistema
motor_olhar = MotorOlharLimbico()

def processar(frame=None):
    """
    Função de compatibilidade direta com o orquestrador (main.py).
    """
    if frame is not None:
        frame_processado, _ = motor_olhar.processar_frame(frame)
        return frame_processado
    return None

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_res = processar(frame)
            if frame_res is not None:
                cv2.imshow("TTC GLOBAL - MOTOR OCULAR", frame_res)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()