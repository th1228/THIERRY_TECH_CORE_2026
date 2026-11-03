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
import json
import time

# --- CORREÇÃO DE CAMINHO ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.camera_hub import instancia_camera
from core.memoria_comum import instancia_memoria as memoria

class MonacoConsciencia:
    def __init__(self, arquivo_memoria="memoria_historica.json"):
        self.arquivo = arquivo_memoria
        print("[CONSCIÊNCIA] Motor de memória persistente ativado.")

    def processar(self, nome_cliente="Cliente Padrão"):
        """Busca o frame atual e registra a consciência para o cliente informado."""
        print(f"[CONSCIÊNCIA] Analisando estado atual para: {nome_cliente}...")
        
        frame = instancia_camera.get_frame()
        if frame is not None:
            self.aprender_com_sucesso(
                nome_cliente=nome_cliente,
                dados="Diagnóstico visual capturado via sistema central",
                protocolo="CAPTURA_VIVA_2026",
                nivel="AVANCADO"
            )
            return True
        else:
            print("[CONSCIÊNCIA] ERRO: Câmera não disponível.")
            return False

    def aprender_com_sucesso(self, nome_cliente, dados, protocolo, nivel):
        """Salva no histórico e também na memória_comum para o Mônaco Plan ler."""
        historico = {"registros": []}
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, "r", encoding="utf-8") as f:
                    historico = json.load(f)
            except: pass
        
        novo_registro = {
            "cliente": nome_cliente,
            "timestamp": time.strftime("%d/%m/%Y %H:%M:%S"),
            "dados": dados,
            "protocolo": protocolo,
            "nivel": nivel
        }
        historico["registros"].append(novo_registro)
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(historico, f, indent=4, ensure_ascii=False)
        
        memoria.salvar_dados("consciencia", {"status": "captura_realizada", "ultimo_registro": novo_registro})
        
        print(f"[CONSCIÊNCIA] {nome_cliente} registrado na memória histórica e comum.")
        return True

# --- PONTE DE INTEGRAÇÃO ---
motor_consciencia = MonacoConsciencia()

def rodar(nome_cliente="Cliente Padrão"):
    return motor_consciencia.processar(nome_cliente)

def iniciar(nome_cliente="Cliente Padrão"):
    return rodar(nome_cliente)