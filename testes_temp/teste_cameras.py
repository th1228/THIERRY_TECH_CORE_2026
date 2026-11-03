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

# -*- coding: utf-8 -*-
import cv2

def identificar_cameras():
    print("--- INICIANDO VARREDURA DE CÂMERAS ---")
    cameras_detectadas = []
    
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"[SUCESSO] Câmera {i}: Disponível.")
            cameras_detectadas.append(i)
            cap.release()
        else:
            # Tenta verificar se o erro é por ocupação
            # Nota: O OpenCV não dá o nome do programa, mas confirma o status
            print(f"[AVISO] Câmera {i}: Não acessível (ou ocupada por outro processo).")
        cap.release()

    print("--- RESULTADO DA VARREDURA ---")
    if not cameras_detectadas:
        print("Nenhuma câmera disponível no momento. Verifique se o Teams/Zoom/WhatsApp estão abertos.")
    else:
        print(f"Câmeras prontas para uso: {cameras_detectadas}")
    print("--- FIM ---")

if __name__ == "__main__":
    identificar_cameras()