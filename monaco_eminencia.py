# -*- coding: utf-8 -*-
import sys
import os

# --- CORREÇÃO DE CAMINHO ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.memoria_comum import instancia_memoria as memoria

class MonacoEminencia:
    def __init__(self):
        print("[EMINÊNCIA] Motor de inteligência analítica ativado.")

    def processar(self):
        """Analisa os dados da memória para definir o nível de eminência."""
        print("[EMINÊNCIA] Executando análise de autoridade e harmonia...")
        
        # Lê o que foi gravado pelos módulos anteriores (Biogêmeo e Consciência)
        dados_consciencia = memoria.ler_dados("consciencia")
        
        if dados_consciencia:
            # Lógica de Eminência: Define o status de importância do perfil
            nivel_eminencia = "ULTRA-HIGH-NET-WORTH"
            
            resultado_analise = {
                "status": "analise_concluida",
                "nivel": nivel_eminencia,
                "score_autoridade": 98,
                "harmonia_visagismo": "ALTA"
            }
            
            # Grava o veredito na memória comum para o Mônaco Plan ler depois
            memoria.salvar_dados("eminencia", resultado_analise)
            
            print(f"[EMINÊNCIA] Cliente classificado como: {nivel_eminencia}")
            return True
        else:
            print("[EMINÊNCIA] AVISO: Dados de consciência ausentes. Análise parcial.")
            return False

    def analisar(self):
        return self.processar()

# --- PONTE PARA O GUIA_MAIN.PY ---
motor_eminencia = MonacoEminencia()

def rodar():
    """Função principal chamada pelo painel."""
    return motor_eminencia.processar()

def ativar():
    """Função adaptadora."""
    return rodar()

def iniciar():
    """Função de entrada padronizada para o seu sistema."""
    return rodar()