import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -*- coding: utf-8 -*-
import os
import subprocess

def carregar_core():
    # Define o caminho da pasta core a partir da UI
    pasta_core = os.path.join(os.path.dirname(os.path.dirname(__file__)), "core")
    
    # Lista de arquivos que devem ser carregados da core
    arquivos_core = [
        "biogenio_scanner.py",
        "verificador_nuvem.py",
        "analise_cabelo.py"
    ]
    
    print("--- INICIANDO CARGA DE MÓDULOS CORE ---")
    for arquivo in arquivos_core:
        caminho = os.path.join(pasta_core, arquivo)
        if os.path.exists(caminho):
            print(f">>> Iniciando {arquivo}")
            subprocess.run(["python", caminho])
        else:
            print(f"!!! ERRO: {arquivo} não encontrado em {caminho}")