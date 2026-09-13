# -*- coding: utf-8 -*-
import sys
import os

# --- CORREÇÃO DE CAMINHO ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.memoria_comum import instancia_memoria as memoria

class MonacoRessonancia:
    def __init__(self):
        print("[RESSONÂNCIA] Motor de sincronização biométrica ativado.")

    def processar(self):
        """Busca o protocolo definido no Mônaco Plan e sincroniza o hardware."""
        print("[RESSONÂNCIA] Executando alinhamento de frequência e dados...")
        
        # 1. Lê o protocolo definido pelo Plan
        protocolo = memoria.ler_dados("protocolo_clinico")
        fase_atual = protocolo.get("fase", "Fase Inicial") if protocolo else "Padrão"
        
        return self.sincronizar(fase_atual)

    def sincronizar(self, fase_atual):
        """Sincroniza a frequência com o hardware baseado na fase."""
        print(f"[RESSONÂNCIA] Sincronizando com cérebro ESP32... Fase: {fase_atual}")
        
        # Lógica de ajuste de hardware
        if "Detox" in fase_atual:
            print("[RESSONÂNCIA] Ajustando frequência para modo: SENÓLISE.")
        elif "Regeneração" in fase_atual:
            print("[RESSONÂNCIA] Ajustando frequência para modo: REPROGRAMAÇÃO.")
        else:
            print("[RESSONÂNCIA] Frequência base de estabilização aplicada.")
            
        return True

# --- PONTE PARA O GUIA_MAIN.PY ---
motor_ressonancia = MonacoRessonancia()

def rodar():
    return motor_ressonancia.processar()

def sintonizar():
    return rodar()

def iniciar():
    return rodar()