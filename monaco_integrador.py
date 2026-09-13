# -*- coding: utf-8 -*-
import sys
import os

# --- CORREÇÃO DE CAMINHO ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.memoria_comum import instancia_memoria as memoria
from core.protocolo_logica import processar_protocolo
from core import motor_biometrico
from core.biogem_engine import BiogemEngine

class MonacoIntegrador:
    def __init__(self):
        print("[INTEGRADOR] Motor de consolidação de dados ativado.")

    def processar(self):
        """Ponto de convergência: consolida tudo o que foi gravado pelos módulos."""
        print("[INTEGRADOR] Consolidando resultados de todos os módulos...")
        return self.integrar_resultados()

    def integrar_resultados(self):
        """Unifica os dados e dispara a geração do relatório."""
        print("[INTEGRADOR] Unificando perícia e gerando estrutura final...")
        
        # 1. Coleta dados com segurança do motor biométrico
        emg = motor_biometrico.get_emg() 
        vfc = motor_biometrico.get_vfc()
        fase = processar_protocolo(emg, vfc, True)
        
        # 2. Estrutura
        dados_biometricos = {
            "CLIENTE": "Thierry",
            "SCANNER_OSTEOMETRIA": str(emg),
            "STATUS_SISTEMA": fase
        }
        
        memoria.salvar_dados("BIOMETRIA", dados_biometricos)
        
        # 3. Consolidação final
        relatorio_consolidado = {
            "BIOMETRIA": dados_biometricos,
            "ambiente": memoria.ler_dados("ambiente"),
            "consciencia": memoria.ler_dados("consciencia"),
            "eminencia": memoria.ler_dados("eminencia"),
            "fase_protocolo": fase
        }
        
        memoria.salvar_dados("integrador", relatorio_consolidado)
        
        # 4. GERAÇÃO SEGURA DO DOSSIÊ MASTER (BIOGEM ENGINE)
        try:
            print("[INTEGRADOR] Disparando Biogem Engine...")
            engine = BiogemEngine(tipo_relatorio="monaco", nome_cliente="Thierry")
            engine.gerar_relatorio_pdf()
        except Exception as e:
            print(f"[ERRO NO GERADOR PDF] Detalhes: {e}")
        
        print("[INTEGRADOR] Estrutura final gerada com sucesso.")
        return True

# --- INSTÂNCIA DO SERVIÇO ---
service_integrador = MonacoIntegrador()

# --- INTERFACES DE EXECUÇÃO ---
def rodar():
    return service_integrador.processar()

def sincronizar():
    return service_integrador.processar()

def iniciar():
    return service_integrador.processar()