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

import cv2
import sys

def inspecionar_sistema_video():
    print("=" * 60)
    print("INSPEÇÃO DE CÂMERAS E FLUXOS DE VÍDEO - THIERRY TECH")
    print("=" * 60)
    
    # 1. Varredura de índices de hardware locais (OpenCV VideoCapture)
    print("\n[1] Varrendo índices de hardware locais (0 a 5)...")
    cameras_ativas = []
    for i in range(6):
        cap = cv2.VideoCapture(i, cv2.CAP_ANY)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                h, w, _ = frame.shape
                cameras_ativas.append((i, w, h))
                print(f" -> Câmera física/virtual detectada no Índice {i}: Resolução {w}x{h}")
            cap.release()
            
    if not cameras_ativas:
        print(" -> Nenhuma câmera aberta diretamente via OpenCV nos índices testados.")
    else:
        print(f" -> Total de {len(cameras_ativas)} dispositivo(s) físico(s)/virtual(is) pronto(s).")
        print(f" -> RECOMENDAÇÃO PARA O SEU MAIN.PY: O OpenCV está pegando a câmera principal geralmente no índice 0 (ou índice 1 se houver software virtual). Verifique se o seu FastAPI está chamando `cv2.VideoCapture(0)`.")

    # 2. Verificação de rotas e integração com o HTML
    print("\n[2] Mapeamento da Conexão HTML <-> Backend (FastAPI):")
    print(" -> No seu arquivo HTML, o elemento responsável por receber o vídeo é:")
    print("    <img id=\"webcam-feed\" src=\"\" alt=\"Live Camera Stream\">")
    print(" -> A rota que alimenta essa tag no painel HTML é acionada por:")
    print("    feedElement.src = \"/video_feed?t=\" + new Date().getTime();")
    print(" -> Quem está gerando e passando essa imagem para a tag <img> do HTML é a função de rota do FastAPI no seu backend (main.py), que faz um loop lendo o frame do OpenCV (`cv2.VideoCapture`) e fazendo o yield do stream multipart (MJPEG).")

    print("\n[3] Onde remover os pontos brancos (malhas) de vez:")
    print(" -> No seu backend Python (main.py ou arquivo de processamento de imagem), procure onde a biblioteca **MediaPipe** (`mp.solutions.face_mesh`) ou **OpenCV** desenha os círculos (`cv2.circle`) ou conexões (`mp.solutions.drawing_utils.draw_landmarks`) sobre o rosto.")
    print(" -> Para a câmera ficar 100% limpa igual na foto que você enviou, o backend Python deve enviar o frame *bruto* capturado da câmera, sem passar pelas funções de desenho da malha facial antes de renderizar o feed.")
    print("=" * 60)

if __name__ == "__main__":
    inspecionar_sistema_video()