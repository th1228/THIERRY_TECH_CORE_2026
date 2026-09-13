import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -*- coding: utf-8 -*-
import os

def gerar_mapa():
    print("--- GERANDO MAPA DE CONEXÃO E CORREÇÃO ---")
    raiz = os.getcwd()
    
    # Estrutura esperada pelo sistema
    arquivos_esperados = {
        "scanner.py": "core/scanner.py",
        "main.py": "main.py",
        "run_all.py": "run_all.py"
    }

    print(f"\n[DIRETÓRIO ATUAL]: {raiz}")
    print("-" * 50)

    # Varredura Real
    for nome, local_correto in arquivos_esperados.items():
        encontrado = False
        for root, dirs, files in os.walk(raiz):
            if nome in files:
                caminho_atual = os.path.join(root, nome)
                encontrado = True
                if caminho_atual.replace(raiz + os.sep, "").replace("\\", "/") == local_correto:
                    print(f"[OK] {nome} está no lugar certo: {local_correto}")
                else:
                    print(f"[ERRO DE LOCAL] {nome} está em: {caminho_atual.replace(raiz, '')}")
                    print(f"    -> AÇÃO: Mova este arquivo para: {local_correto}")
        
        if not encontrado:
            print(f"[CRÍTICO] {nome} NÃO foi encontrado em lugar nenhum do projeto.")

    print("\n--- RESUMO DE AÇÕES ---")
    print("1. Se apareceu [ERRO DE LOCAL], mova o arquivo conforme a indicação.")
    print("2. Após mover, apague os arquivos 'tempCodeRunnerFile.py' que aparecerem.")
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    gerar_mapa()