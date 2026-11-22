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

class CameraHub:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(CameraHub, cls).__new__(cls)
                # Abre a câmera apenas UMA vez para o sistema todo
                cls._instance.cap = cv2.VideoCapture(0, cv2.CAP_ANY)
                
                # Configurações de alta performance
                cls._instance.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                cls._instance.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                cls._instance.cap.set(cv2.CAP_PROP_FPS, 60)
                
                status_camera = cls._instance.cap.isOpened()
                print(f"[HARDWARE] Câmera inicializada pelo CameraHub. Status: {status_camera}")
                
                # Sincronização automática com a Memória Comum 🧠
                try:
                    memoria.salvar_dados("camera_hub_status", {"aberta": status_camera})
                except Exception:
                    pass
                    
        return cls._instance

    def get_frame(self):
        # Retorna o frame atual da câmera
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            return frame if ret else None
        return None

    def release(self):
        # Apenas fecha se realmente precisar desligar tudo
        if self.cap and self.cap.isOpened():
            self.cap.release()
            print("[HARDWARE] Câmera liberada.")
            try:
                memoria.salvar_dados("camera_hub_status", {"aberta": False})
            except Exception:
                pass

# Instância global ajustada para o padrão esperado pelo ecossistema
instancia_camera = CameraHub()

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    f = instancia_camera.get_frame()
    return {"status": "Frame capturado" if f is not None else "Falha na captura", "frame_disponivel": f is not None}

if __name__ == "__main__":
    frame_teste = instancia_camera.get_frame()
    print("Teste de frame obtido:", frame_teste is not None)