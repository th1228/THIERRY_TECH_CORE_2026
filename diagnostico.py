# -*- coding: utf-8 -*-
import importlib.util
import os
import sys

# Adiciona a pasta atual ao caminho do sistema para garantir que ele ache os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def diagnosticar():
    print("--- INICIANDO DIAGNÓSTICO DO MÔNACO ---")
    
    # 1. Testar se o arquivo do script_clima existe e pode ser importado
    try:
        import core.script_clima as clima
        print("OK: core.script_clima carregado.")
        # Testar se a função rodar existe
        if hasattr(clima, 'rodar'):
            print("OK: Função 'rodar' encontrada em script_clima.")
        else:
            print("ERRO: Função 'rodar' NÃO encontrada em script_clima.")
    except Exception as e:
        print(f"ERRO: Não foi possível importar core.script_clima: {e}")

    # 2. Testar se o monaco_plan existe e pode ser importado
    try:
        import monaco_plan
        print("OK: monaco_plan carregado.")
    except Exception as e:
        print(f"ERRO: Não foi possível importar monaco_plan: {e}")

    # 3. Testar a Memória
    try:
        import core.memoria_comum as mem
        if hasattr(mem, 'instancia_memoria'):
            print("OK: memoria_comum carregada e 'instancia_memoria' encontrada.")
        else:
            print("ERRO: memoria_comum carregada, mas 'instancia_memoria' NÃO encontrada.")
    except Exception as e:
        print(f"ERRO: Não foi possível importar core.memoria_comum: {e}")

if __name__ == "__main__":
    diagnosticar()