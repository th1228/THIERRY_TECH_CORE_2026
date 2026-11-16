# -*- coding: utf-8 -*-
# =====================================================================
# THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026
# MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - AUDITOR DE ESTRUTURA EXECUTIVO
# =====================================================================

import os
from pathlib import Path

# Cores ANSI para o padrão High-Tech
VERDE = "\033[92m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
CIANO = "\033[96m"
BRANCO = "\033[97m"
CINZA = "\033[90m"
RESET = "\033[0m"

def auditar_estrutura_projeto(raiz="."):
    raiz_path = Path(raiz).resolve()
    
    print(VERDE + "=" * 85 + RESET)
    print(AMARELO + "   THIERRY TECHNOLOGY CONCEPT GLOBAL • AUDITOR EXECUTIVO DE ESTRUTURA" + RESET)
    print(CIANO + "   VARREDURA INTELIGENTE & RELATÓRIO CONSOLIDADO DE ARQUITETURA" + RESET)
    print(VERDE + "=" * 85 + RESET + "\n")

    total_analisados = 0
    certos = []
    incorretos = []
    avisos_raiz = []

    print(f"{BRANCO}[🔍] A executar varredura completa no ecossistema...{RESET}\n")

    for arquivo in raiz_path.glob("**/*.py"):
        # Ignora pastas virtuais, cache e controle de versão
        if any(p in arquivo.parts for p in [".git", "__pycache__", "venv", "env", "node_modules"]):
            continue

        total_analisados += 1
        rel_path = arquivo.relative_to(raiz_path)
        nome_arq = arquivo.name
        pasta_atual = rel_path.parent.name if len(rel_path.parts) > 1 else "."

        # Regras de validação da arquitetura
        if "quantum_shield" in nome_arq.lower() or "quantum_shild" in nome_arq.lower():
            if pasta_atual != "security":
                incorretos.append({
                    "arquivo": str(rel_path),
                    "problema": "Quantum Shield fora da pasta de segurança",
                    "acao": "Mover obrigatoriamente para a pasta 'security/'"
                })
            else:
                certos.append(str(rel_path))
                
        elif nome_arq == "main.py":
            if pasta_atual != ".":
                incorretos.append({
                    "arquivo": str(rel_path),
                    "problema": "Script principal 'main.py' fora da raiz",
                    "acao": "Mover para a raiz principal do projeto"
                })
            else:
                certos.append(str(rel_path))
                
        elif (nome_arq.startswith("mibo_") or nome_arq.startswith("monaco_")) and pasta_atual == ".":
            avisos_raiz.append({
                "arquivo": str(rel_path),
                "problema": "Módulo principal de ecossistema solto na raiz",
                "acao": "Recomendado mover para a pasta 'core/' para limpar a raiz"
            })
        else:
            certos.append(str(rel_path))

    # =====================================================================
    # RELATÓRIO EXECUTIVO FINAL ORGANIZADO EM TEXTO
    # =====================================================================
    print(VERDE + "\n" + "=" * 85 + RESET)
    print(AMARELO + "                       RELATÓRIO EXECUTIVO DA AUDITORIA" + RESET)
    print(VERDE + "=" * 85 + RESET)
    print(f" • Total de Ficheiros Python Escaneados : {BRANCO}{total_analisados}{RESET}")
    print(f" • Ficheiros no Local Correto         : {VERDE}{len(certos)}{RESET}")
    print(f" • Módulos na Raiz (Requer Organização) : {AMARELO}{len(avisos_raiz)}{RESET}")
    print(f" • Erros Críticos de Localização      : {VERMELHO if len(incorretos) > 0 else VERDE}{len(incorretos)}{RESET}")
    print(VERDE + "-" * 85 + RESET)

    if incorretos:
        print(VERMELHO + "\n [!] ITENS COM LOCALIZAÇÃO INCORRETA (EXIGEM CORREÇÃO):" + RESET)
        for item in incorretos:
            print(f"   • Ficheiro: {BRANCO}{item['arquivo']}{RESET}")
            print(f"     -> Problema: {VERMELHO}{item['problema']}{RESET}")
            print(f"     -> O que fazer: {CIANO}{item['acao']}{RESET}")

    if avisos_raiz:
        print(AMARELO + "\n [!] MÓDULOS DE ECOSSISTEMA SOLTOS NA RAIZ (SUGESTÃO DE LIMPEZA):" + RESET)
        for item in avisos_raiz:
            print(f"   • Ficheiro: {BRANCO}{item['arquivo']}{RESET}")
            print(f"     -> Ação: {CIANO}{item['acao']}{RESET}")

    print(VERDE + "\n" + "=" * 85 + RESET)
    if not incorretos and not avisos_raiz:
        print(VERDE + " ✨ STATUS: ECOSSISTEMA 100% ORGANIZADO E ALINHADO COM A ARQUITETURA! ✨" + RESET)
    else:
        print(AMARELO + " 💡 AÇÃO RECOMENDADA: Siga os passos descritos acima para consolidar o projeto." + RESET)
    print(VERDE + "=" * 85 + RESET + "\n")

if __name__ == "__main__":
    auditar_estrutura_projeto()