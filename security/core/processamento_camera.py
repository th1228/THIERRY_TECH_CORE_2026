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

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys, os

import cv2
import mediapipe as mp
import winsound

class ScannerCamera:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.6
        )
        self.cor_neon = (255, 0, 255)

    def processar(self, nome_cliente):
        """O Mônaco chama este método. A câmera só abre aqui."""
        cap = cv2.VideoCapture(0)
        
        # A lógica permanece igual, mas agora ela é um "serviço"
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb)
            
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    for lm in face_landmarks.landmark:
                        h, w, _ = frame.shape
                        x, y = int(lm.x * w), int(lm.y * h)
                        cv2.circle(frame, (x, y), 1, self.cor_neon, -1)

            cv2.imshow('TTC CORE 2026', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                self._executar_salvamento(frame, nome_cliente)
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return "SUCESSO"

    def _executar_salvamento(self, frame, nome):
        flash = frame.copy()
        flash[:] = (255, 255, 255)
        cv2.imshow('TTC CORE 2026', flash)
        winsound.Beep(1500, 300) 
        cv2.waitKey(150)
        
        nome_arquivo = f"diagnostico_{nome}.jpg"
        cv2.imwrite(nome_arquivo, frame)
        print(f"[CÂMERA] Imagem salva: {nome_arquivo}")

# REMOVIDO O BLOCO IF __NAME__ == "__main__":
# Agora este arquivo é um Módulo de Serviço Silencioso.