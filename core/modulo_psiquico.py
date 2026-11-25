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
import math
import cv2
import numpy as np
from datetime import datetime

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
        def __init__(self):
            self._dados = {}

        def salvar_dados(self, chave, valor):
            self._dados[chave] = valor
            return True

        def registrar(self, chave, valor):
            self._dados[chave] = valor
            return True

        def ler_dados(self, chave):
            return self._dados.get(chave)
    memoria = MemoriaMock()

# Constante da Frequência de Sincronização Sônica (Frequência de Deus - 528 Hz)
FREQUENCIA_BASE_DIVINA = 528.0

def calcular_ressonancia_biogênica():
    """Calcula a coerência baseada na frequência de 528Hz e no tempo atual."""
    fase_onda = math.sin(datetime.now().second * (FREQUENCIA_BASE_DIVINA / 1000.0))
    return round(abs(fase_onda), 4)

def obter_axioma_estoico(temperamento):
    """Mapeia o temperamento e a frequência para um axioma estoico soberano."""
    acervo = {
        "Colérico": "A força do comando reside no domínio das próprias emoções perante o caos externo.",
        "Sanguíneo": "A flexibilidade e o entusiasmo alinhados à clareza mental constroem impérios duradouros.",
        "Fleumático / Melancólico": "A análise profunda e a serenidade silenciosa revelam a verdadeira ordem das coisas.",
        "Equilibrado": "A mente em harmonia com a frequência pura transcende qualquer perturbação externa."
    }
    return acervo.get(temperamento, acervo["Equilibrado"])

def processar_analise(caminho_foto):
    """
    Módulo Psíquico: Lê o status biométrico da memória, infere o perfil temperamental,
    aplica a modulação da Frequência de Deus (528Hz) e sintetiza o axioma estoico.
    """
    # Lê usando o método correto da instância de memória
    status_biometrico = str(memoria.ler_dados("ROSTO_STATUS") or "Desconhecido")
    
    # Lógica de inferência baseada na morfologia facial/status
    if "Triangular" in status_biometrico or "Invertido" in status_biometrico:
        temperamento = "Colérico"
    elif "Oval" in status_biometrico or "Redondo" in status_biometrico:
        temperamento = "Sanguíneo"
    elif "Quadrado" in status_biometrico or "Retangular" in status_biometrico:
        temperamento = "Fleumático / Melancólico"
    else:
        temperamento = "Equilibrado"

    # Aplicação da Frequência de Deus e Axioma Estoico
    coerencia = calcular_ressonancia_biogênica()
    axioma = obter_axioma_estoico(temperamento)
    
    laudo_completo = f"{temperamento} (Coerência 528Hz: {coerencia} | Axioma: '{axioma}')"

    # Salva o laudo psíquico e os parâmetros na memória para o motor consumir
    memoria.salvar_dados("laudo_psiquico", laudo_completo)
    memoria.salvar_dados("PSICO_STATUS", "Concluído")
    memoria.salvar_dados("FREQUENCIA_SONICA", FREQUENCIA_BASE_DIVINA)
    memoria.salvar_dados("COERENCIA_BIOGINICA", coerencia)
    
    print(f"\n🕊️ [MÓDULO PSIQUICO • 528Hz] SÍNTESE ESTOICA CONCLUÍDA")
    print(f"   Perfil / Temperamento -> {temperamento}")
    print(f"   Ressonância Sônica    -> {FREQUENCIA_BASE_DIVINA} Hz (Coerência: {coerencia})")
    print(f"   Axioma de Sabedoria   -> \"{axioma}\"")
    print(f"   [INFO] Laudo gravado com sucesso na memória.\n")
    
    return laudo_completo

def processar(frame):
    """
    Função de compatibilidade direta chamada pelo orquestrador principal (main.py).
    Processa o frame recebido, faz a inferência e retorna o frame com HUD visual adaptado.
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

    coerencia = calcular_ressonancia_biogênica()

    # HUD visual incorporado no frame para acompanhamento em tempo real (Padrão TTC Global)
    cv2.putText(frame, "TTC GLOBAL // MODULO PSIQUICO [ACTIVE 528Hz]", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 102), 2, cv2.LINE_AA)
    cv2.putText(frame, f"PERFIL: {temperamento}", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (212, 175, 55), 2, cv2.LINE_AA)
    cv2.putText(frame, f"FREQUENCIA: 528Hz | COERENCIA: {coerencia}", (25, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    return frame

def capturar_e_analisar():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERRO] Câmera não acessível para o Módulo Psíquico.")
        return

    print("Capturando para análise psíquica e harmonia sônica... [Pressione ESPAÇO para capturar ou 'Q' para sair]")
    
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            break
            
        # Aplica a interface visual
        frame_hud = processar(frame)
        cv2.imshow('TTC GLOBAL - Modulo Psiquico 528Hz', frame_hud)
        
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