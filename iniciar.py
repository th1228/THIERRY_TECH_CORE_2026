import sys
import os

# Correção automática de caminho
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from monaco_integrador import MonacoIntegrador

def executar_sistema():
    print("--- INICIANDO SISTEMA MONACO ---")
    try:
        sistema = MonacoIntegrador()
        print(sistema.processar())
    except Exception as e:
        print(f"Erro ao iniciar motor: {e}")
    print("--- SISTEMA OPERACIONAL ---")

if __name__ == "__main__":
    executar_sistema()