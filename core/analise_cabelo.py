# -*- coding: utf-8 -*-
import sys
import os
import cv2
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

def calcular_vitalidade_completa(hidrofobia, espessura, dermatite_risco, tipo_reflexo):
    peso_reflexo = {"BRILHOSO": 10, "TRANSLUCIDO": 5, "OPACO": 2}
    score = (hidrofobia * 0.3) + (espessura * 0.2) + (peso_reflexo[tipo_reflexo] * 0.3) + (10 if dermatite_risco == "BAIXA" else 3) * 0.2
    return round(max(1, min(10, score / 10)), 1)

def processar(frame=None):
    if frame is None: 
        return frame
    
    # Área de análise centralizada
    roi = frame[50:200, 200:400] 
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # 1. Análise de Densidade (Fios por cm²)
    edges = cv2.Canny(gray, 50, 150)
    contagem_fios = cv2.countNonZero(edges)
    densidade_fios = contagem_fios / 100  # Estimativa de fios/cm² na área
    espessura_media = np.mean(edges) / 10.0 
    
    # 2. Detecção de Alopecia (Áreas Lisas)
    media_brilho = np.mean(gray)
    risco_alopecia = "ALERTA: POSSÍVEL ALOPECIA" if (densidade_fios < 5 and media_brilho > 150) else "SAUDÁVEL"
    
    # Classificação de Reflexo
    if media_brilho > 180: tipo_reflexo = "BRILHOSO"
    elif media_brilho > 100: tipo_reflexo = "TRANSLUCIDO"
    else: tipo_reflexo = "OPACO"
    
    nivel_hidrofobia = media_brilho / 25.5
    tendencia_dermatite = "BAIXA" if np.std(gray) > 30 else "ALTA"
    
    vitalidade = calcular_vitalidade_completa(nivel_hidrofobia, espessura_media, tendencia_dermatite, tipo_reflexo)
    
    dados_cabelo = {
        "VITALIDADE_SCORE": vitalidade,
        "DENSIDADE_CM2": round(densidade_fios, 1),
        "RISCO_ALOPECIA": risco_alopecia,
        "REFLEXO": tipo_reflexo,
        "SAUDE_COURO": tendencia_dermatite
    }
    
    # Gravação segura no sistema de memória 🧠
    try:
        if hasattr(memoria, 'salvar_dados'):
            memoria.salvar_dados("CABELO_DIAGNOSTICO", dados_cabelo)
        elif hasattr(memoria, 'registrar'):
            memoria.registrar("CABELO_DIAGNOSTICO", dados_cabelo)
    except Exception:
        pass
    
    # Feedback Visual High-End
    cor_alerta = (0, 0, 255) if risco_alopecia != "SAUDÁVEL" else (0, 255, 0)
    
    cv2.putText(frame, f"VITALIDADE: {vitalidade}/10", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"DENSIDADE: {dados_cabelo['DENSIDADE_CM2']} fios/cm2", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, f"STATUS: {risco_alopecia}", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor_alerta, 2)
    
    return frame

if __name__ == "__main__":
    print("Módulo analise_cabelo integrado com sucesso.")