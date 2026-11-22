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

import os
import re

def scan_project_for_php_docker(base_dir):
    print(f"=== Varrendo diretório em busca de referências ao PHP no Docker/Servidores ===")
    print(f"Diretório base: {base_dir}\n")
    
    found_dockerfiles = 0
    found_compose = 0

    for root, dirs, files in os.walk(base_dir):
        # Ignorar pastas virtuais ou de controle de versão
        if any(excluded in root for excluded in ['.git', '__pycache__', 'node_modules', 'venv']):
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            
            # Analisa Dockerfiles
            if file.lower() == "dockerfile" or file.lower().startswith("dockerfile."):
                found_dockerfiles += 1
                check_dockerfile_content(file_path)
                
            # Analisa arquivos Docker Compose
            elif file.lower() in ["docker-compose.yml", "docker-compose.yaml"]:
                found_compose += 1
                check_compose_content(file_path)

    print("\n--- Resumo da Varredura ---")
    print(f"Dockerfiles analisados: {found_dockerfiles}")
    print(f"Arquivos Docker Compose analisados: {found_compose}")

def check_dockerfile_content(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Procura por imagens base do PHP (ex: php:8.2, php:8.3-fpm, etc.)
            matches = re.findall(r"FROM\s+([^\s]*php[^\s]*)", content, re.IGNORECASE)
            if matches:
                print(f"[ALERTA DOCKERFILE] Encontrado em: {path}")
                for img in matches:
                    print(f"    -> Imagem PHP utilizada: {img}")
                    if any(ver in img for ver in ["8.2", "8.3", "8.4", "8.5"]):
                        print(f"    [!] Verifique se a tag da imagem usa uma subversão corrigida (ex: >= 8.2.35 / 8.3.36).")
    except Exception as e:
        pass

def check_compose_content(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if "php" in content.lower():
                print(f"[COMPOSE] Menção ao PHP encontrada em: {path}")
    except Exception as e:
        pass

if __name__ == "__main__":
    # Pega o diretório atual onde o script está rodando
    current_dir = os.getcwd()
    scan_project_for_php_docker(current_dir)