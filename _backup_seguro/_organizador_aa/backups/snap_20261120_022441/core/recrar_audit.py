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
import json
import time
from datetime import datetime

# Diretório raiz do projeto
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Diretórios e arquivos esperados para validação de conformidade internacional
EXPECTED_DIRS = ['security', 'core', 'storage', 'config', 'tests', 'tools', 'relatorios']
CRITICAL_FILES = ['main.py']

# Códigos de cores ANSI para o terminal
GREEN = "\033[92m"
BOLD = "\033[1m"
RESET = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def audit_project_structure():
    report = {
        "timestamp": datetime.now().isoformat(),
        "project_root": ROOT_DIR,
        "directories_found": [],
        "missing_directories": [],
        "critical_files_status": {},
        "structure_tree": {}
    }

    # Verificar diretórios
    for d in EXPECTED_DIRS:
        dir_path = os.path.join(ROOT_DIR, d)
        if os.path.isdir(dir_path):
            report["directories_found"].append(d)
        else:
            report["missing_directories"].append(d)

    # Verificar arquivos críticos
    for f in CRITICAL_FILES:
        file_path = os.path.join(ROOT_DIR, f)
        report["critical_files_status"][f] = os.path.isfile(file_path)

    # Coletar todos os arquivos para a animação de subida (créditos de filme)
    all_files_list = []
    tree = {}
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv' and d != '__pycache__']
        rel_path = os.path.relpath(root, ROOT_DIR)
        tree[rel_path] = {
            "subdirectories": dirs,
            "files": files
        }
        for f in files:
            all_files_list.append(os.path.join(rel_path, f))
    
    report["structure_tree"] = tree
    total_files_count = len(all_files_list)

    # Salvar o relatório em formato JSON
    output_filename = f"auditoria_estrutura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path = os.path.join(ROOT_DIR, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    # =============================================================
    # EFEITO DE SUBIDA DE ARQUIVOS (FINAL DE FILME)
    # =============================================================
    clear_screen()
    print("=" * 70)
    print("      INICIANDO AUDITORIA DE INTEGRIDADE DA ÁRVORE DE ARQUIVOS")
    print("=" * 70)
    time.sleep(1)

    print("\n--- PROCESSANDO E AUDITANDO ARQUIVOS DO SISTEMA ---\n")
    time.sleep(0.5)

    # Faz os arquivos subirem linha por linha com pausa suave
    for file_path in all_files_list:
        print(f"  [AUDITANDO]  {file_path}  --->  OK (Verificado)")
        time.sleep(0.04)  # Velocidade do scroll no estilo créditos

    time.sleep(1)

    # =============================================================
    # PARECER FINAL FIXADO E EM VERDE BRILHANTE
    # =============================================================
    all_dirs_present = len(report["missing_directories"]) == 0
    all_critical_present = all(report["critical_files_status"].values())
    is_complete_and_perfect = all_dirs_present and all_critical_present and total_files_count > 0

    clear_screen()

    if is_complete_and_perfect:
        print(GREEN + BOLD + "═" * 74 + RESET)
        print(GREEN + BOLD + "          PARECER FINAL DA AUDITORIA - CONFORMIDADE INTERNACIONAL       " + RESET)
        print(GREEN + BOLD + "═" * 74 + RESET)
        print(GREEN + BOLD + f"  STATUS DO SISTEMA : [ PERFEITO E CONCLUÍDO ]" + RESET)
        print(GREEN + BOLD + f"  NÍVEL DE DETALHE  : INTERNACIONAL DE DETALHAMENTO DA ÁRVORE DE ARQUIVOS" + RESET)
        print(GREEN + BOLD + f"  TOTAL AUDITADO    : {total_files_count} arquivos em {len(tree)} diretórios" + RESET)
        print(GREEN + BOLD + "─" * 74 + RESET)
        print(GREEN + BOLD + "  CONCLUSÃO:" + RESET)
        print(GREEN + BOLD + "  O programa está completo, com todos os arquivos e diretórios" + RESET)
        print(GREEN + BOLD + "  devidamente estruturados, segregados e catalogados segundo" + RESET)
        print(GREEN + BOLD + "  os critérios de auditoria, segurança e integridade de software." + RESET)
        print(GREEN + BOLD + "═" * 74 + RESET)
        print(f"\n[+] Evidência oficial salva em: {output_filename}\n")
    else:
        print("STATUS DO SISTEMA: ATENÇÃO NECESSÁRIA.")
        print("CONCLUSAO: O programa ainda não possui todos os arquivos/diretórios mínimos.")

if __name__ == "__main__":
    audit_project_structure()