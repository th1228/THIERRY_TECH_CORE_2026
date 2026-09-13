import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -*- coding: utf-8 -*-
import cv2
import threading

class CameraManager:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.frame = None
        self.lock = threading.Lock()
        self.running = True
        
        # Inicia a thread de captura contínua
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        while self.running:
            if self.camera.isOpened():
                ret, frame = self.camera.read()
                if ret:
                    with self.lock:
                        self.frame = frame
            else:
                import time
                time.sleep(0.1)

    def get_frame(self):
        with self.lock:
            return self.frame

    # --- ESTE É O MÉTODO QUE ESTAVA FALTANDO ---
    def encerrar(self):
        self.running = False
        if self.camera is not None:
            self.camera.release()
            print("[CÂMERA] Dispositivo liberado com sucesso.")

# Instância única para ser importada
instancia_camera = CameraManager()