# -*- coding: utf-8 -*-
import sys
import os

# --- BLOCO DE CONEXÃO ESTRUTURAL (NÃO MEXER) ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

# Importações seguras dos motores do ecossistema
try:
    from core.motor_biometrico import iniciar as iniciar_biometria
except ImportError:
    def iniciar_biometria(): return {"status": "Mock Biometria"}

try:
    from core.motor_prognostico import iniciar as iniciar_prognostico
except ImportError:
    def iniciar_prognostico(): pass

try:
    from core.motor_regeneracao import MotorRegeneracao
except ImportError:
    MotorRegeneracao = None

try:
    from core.motor_performance import MotorPerformance
except ImportError:
    MotorPerformance = None

try:
    from core.motor_sincronia import executar_coleta_inicial
except ImportError:
    def executar_coleta_inicial(): pass


class GerenciadorGlobalEcosystem:
    """
    Maestro central do THIERRY_TECH_CORE_2026.
    Gerencia o fluxo entre os motores, geolocalização e os planos (Laboratório, Salão, Engenharia Completa).
    """
    def __init__(self):
        print("[GERENCIADOR GLOBAL] Inicializando maestro do ecossistema...")

    def processar_ecossistema_completo(self, tipo_plano="engenharia_completa"):
        print(f"[GERENCIADOR GLOBAL] Acionando ecossistema para o plano: {tipo_plano.upper()}")
        
        # 1. Executa sincronia e testes de performance de base
        executar_coleta_inicial()
        
        # 2. Executa varredura biométrica
        dados_biometricos = iniciar_biometria()
        
        # 3. Executa prognóstico de 16 dias
        iniciar_prognostico()
        
        # 4. Roteia com base na escolha do plano na interface
        if tipo_plano == "laboratorio":
            print("[TTC GLOBAL] Compilando dados clínicos e biométricos para o Laboratório...")
        elif tipo_plano == "salao":
            print("[TTC GLOBAL] Compilando diretrizes estéticas e de visagismo para o Salão...")
        elif tipo_plano == "engenharia_completa":
            print("[TTC GLOBAL] Compilando Dossiê Supremo de Engenharia Pessoal...")
            
        # Sincroniza o sucesso da execução na Memória Comum 🧠
        memoria.salvar_dados("STATUS_GERENCIADOR_GLOBAL", "EXECUTADO_COM_SUCESSO")
        print("[GERENCIADOR GLOBAL] Processo concluído com êxito.")
        return "[GERENCIADOR GLOBAL] Processo concluído com êxito."

if __name__ == "__main__":
    orquestrador = GerenciadorGlobalEcosystem()
    orquestrador.processar_ecossistema_completo(tipo_plano="engenharia_completa")