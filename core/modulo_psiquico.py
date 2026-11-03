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
import numpy as np

# Garante que o Python enxergue a raiz do projeto para importar a memória comum
script_dir = os.path.dirname(os.path.abspath(__file__))
raiz_projeto = os.path.abspath(os.path.join(script_dir, ".."))
if raiz_projeto not in sys.path:
    sys.path.append(raiz_projeto)

# Importa a instância real da memória comum
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def ler_dados(self, chave): return "Rosto Oval (Exemplo)"
        def salvar_dados(self, chave, valor): pass
    memoria = MemoriaMock()

def processar_analise(caminho_foto):
    """
    Módulo Psíquico: Lê o status biométrico da memória e infere o perfil temperamental.
    """
    # Lê usando o método correto da instância de memória
    status_biometrico = str(memoria.ler_dados("ROSTO_STATUS") or "Desconhecido")
    
    # Lógica de inferência baseada na morfologia facial/status
    if "Triangular" in status_biometrico or "Invertido" in status_biometrico:
        temperamento = "Colérico (Alta Predisposição ao Comando e Foco)"
    elif "Oval" in status_biometrico or "Redondo" in status_biometrico:
        temperamento = "Sanguíneo (Flexível, Comunicativo e Dinâmico)"
    elif "Quadrado" in status_biometrico or "Retangular" in status_biometrico:
        temperamento = "Fleumático / Melancólico (Analítico e Estruturado)"
    else:
        temperamento = "Adaptável (Equilíbrio Interno e Versatilidade)"

    # Salva o laudo psíquico na memória para o motor de PDF consumir
    memoria.salvar_dados("laudo_psiquico", temperamento)
    memoria.salvar_dados("PSICO_STATUS", "Concluído")
    
    print(f"[PSY-ENGINE] Laudo gerado e salvo na memória: {temperamento}")
    return temperamento

def processar(frame):
    """
    Função de compatibilidade direta chamada pelo orquestrador principal (main.py).
    Processa o frame recebido, faz a inferência e retorna o frame com HUD visual.
    """
    if frame is None:
        return frame

    # Lê o status atual da memória
    status_biometrico = str(memoria.ler_dados("ROSTO_STATUS") or "Perfil Padrão")
    
    if "Triangular" in status_biometrico:
        temperamento = "Colérico"
    elif "Oval" in status_biometrico:
        temperamento = "Sanguíneo"
    else:
        temperamento = "Equilibrado"

    # HUD visual incorporado no frame para acompanhamento em tempo real
    cv2.putText(frame, "TTC GLOBAL // MODULO PSIQUICO [ACTIVE]", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 102), 2, cv2.LINE_AA)
    cv2.putText(frame, f"PERFIL: {temperamento}", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (212, 175, 55), 2, cv2.LINE_AA)

    return frame

def capturar_e_analisar():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERRO] Câmera não acessível para o Módulo Psíquico.")
        return

    print("Capturando para análise psíquica... [Pressione ESPAÇO para capturar ou 'Q' para sair]")
    
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            break
            
        # Aplica a interface visual
        frame_hud = processar(frame)
        cv2.imshow('TTC GLOBAL - Modulo Psiquico', frame_hud)
        
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord(' '):
            caminho_foto = os.path.join(script_dir, "foto_diaria.jpg")
            cv2.imwrite(caminho_foto, frame)
            print("[INFO] Foto capturada com sucesso.")
            processar_analise(caminho_foto)
            break
        elif tecla == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capturar_e_analisar()