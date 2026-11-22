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
import cv2
import mediapipe as mp
import threading

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

def rodar_camera():
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        # Processamento leve do MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        
        # O resultado aparece no terminal e atualiza a Memória Comum 🧠
        if results.multi_face_landmarks:
            print("Scanner Ativo: Rosto detectado com sucesso.")
            try:
                memoria.salvar_dados("scanner_rosto_status", {"detectado": True, "status": "Ativo"})
            except Exception:
                pass
            
        if cv2.waitKey(5) & 0xFF == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()

def iniciar_scanner_thread():
    """Inicia a câmera em segundo plano sem travar o layout All Black 💻."""
    t = threading.Thread(target=rodar_camera, daemon=True)
    t.start()
    print("[SCANNER] Thread de captura iniciada em background.")
    return t

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    iniciar_scanner_thread()
    return {"status": "Scanner inicializado em background"}

if __name__ == "__main__":
    iniciar_scanner_thread()
    # Mantém o script principal rodando para testar a thread
    import time
    while True:
        time.sleep(1)