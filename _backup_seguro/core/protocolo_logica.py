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

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -*- coding: utf-8 -*-
import datetime
import os

# --- Configurações de Limiar ---
LIMIAR_EMG = 500  
LIMIAR_VFC = 60   

def registrar_log(estado, fase):
    """Registra a ação na pasta raiz do projeto para auditoria centralizada."""
    caminho_log = os.path.join(os.path.dirname(__file__), "..", "protocolo_monaco_log.txt")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensagem = f"{timestamp} | Estado: {estado} | Ação: {fase}\n"
    
    with open(caminho_log, "a") as f:
        f.write(mensagem)
    print(f"[LOG MONACO]: {mensagem.strip()}")

def processar_protocolo(emg_valor, vfc_valor, refletancia_ok):
    """Motor de decisão do Protocolo Mônaco com conversão de tipos blindada."""
    try:
        # Tratamento preventivo para valores nulos ou vazios
        emg_str = str(emg_valor) if emg_valor is not None else "0"
        vfc_str = str(vfc_valor) if vfc_valor is not None else "0"

        # Extrai apenas os dígitos com segurança
        digitos_emg = ''.join(filter(str.isdigit, emg_str))
        digitos_vfc = ''.join(filter(str.isdigit, vfc_str))

        emg_int = int(digitos_emg) if digitos_emg else 0
        vfc_int = int(digitos_vfc) if digitos_vfc else 0
        
        # Lógica de decisão
        if emg_int > LIMIAR_EMG and vfc_int < LIMIAR_VFC:
            estado = "Simpático"
            fase = "Fase 1: Detox Seletivo (Senolíticos/Calma)"
            registrar_log(estado, fase)
            return fase
            
        elif emg_int < LIMIAR_EMG and vfc_int > LIMIAR_VFC and refletancia_ok:
            estado = "Parassimpático"
            fase = "Fase 2: Regeneração (Autólogos/Exossomos)"
            registrar_log(estado, fase)
            return fase
        
        else:
            return "Estado Neutro - Monitorando..."
            
    except Exception as e:
        print(f"[ERRO NO PROTOCOLO] Falha ao processar: {e}")
        return "Erro de Processamento"