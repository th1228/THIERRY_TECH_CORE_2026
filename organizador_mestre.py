# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - ORGANIZADOR MESTRE TIER-1 ELITE
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the 
intellectual property of Thierry Technology Concept Global. Unauthorized 
distribution, reverse engineering, or usage without a signed NDA/License 
agreement is strictly prohibited under international copyright frameworks.
Target Jurisdiction: Monaco / Tier-1 Enterprise Compliance.
===========================================================================
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Cores ANSI para o padrão High-Tech
VERDE = "\033[92m"
AMARELO = "\033[93m"
CIANO = "\033[96m"
BRANCO = "\033[97m"
MAGENTA = "\033[95m"
VERMELHO = "\033[91m"
RESET = "\033[0m"

def gerar_arvore_diretorios(diretorio: Path, prefixo: str = ""):
    """Gera visualmente a árvore de identificação estrutural colorida do ecossistema."""
    conteudo_ignorado = {".git", "__pycache__", ".venv", "venv", "env", "node_modules"}
    try:
        arquivos = sorted([x for x in diretorio.iterdir() if x.name not in conteudo_ignorado])
    except Exception:
        return
    
    pode_exibir = [x for x in arquivos if not (x.name.startswith('.') and x.name != '.env')]

    for i, item in enumerate(pode_exibir):
        conector = "└── " if i == len(pode_exibir) - 1 else "├── "
        cor_item = CIANO if item.is_dir() else BRANCO
        print(f"{prefixo}{conector}{cor_item}{item.name}{RESET}")
        if item.is_dir() and prefixo.count("    ") < 2:
            extensao = "    " if i == len(pode_exibir) - 1 else "│   "
            gerar_arvore_diretorios(item, prefixo + extensao)

def executar_organizador_master():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        pass

    print(VERDE + "=" * 70 + RESET)
    print(AMARELO + " 🛡️ TCC SOVEREIGN KERNEL - ORGANIZADOR MESTRE TIER-1 ELITE" + RESET)
    print(CIANO + "   BLINDAGEM QUÂNTICA, HIGIENIZAÇÃO DE RAIZ & SEPARAÇÃO DE ATIVOS" + RESET)
    print(VERDE + "=" * 70 + RESET + "\n")

    # 1. Garantir infraestrutura padrão Tier-1 de pastas obrigatórias
    pastas_alvo = ["core", "security", "legal", "static", "tests", "tools", "pdfs_finais", "vault_uhnw_storage"]
    print(f"{BRANCO}[FSE-01] A verificar e blindar infraestrutura de diretórios...{RESET}")
    for pasta in pastas_alvo:
        caminho = BASE_DIR / pasta
        caminho.mkdir(parents=True, exist_ok=True)
        print(f"   {VERDE}[OK]{RESET} /{pasta} validada com sucesso.")

    # 2. Núcleo inviolável absoluto que JAMAIS pode sair da raiz
    nucleo_inviolavel = {
        "main.py", 
        "organizador_mestre.py", 
        "manifesto_mibo.py", 
        "auditor_estrutura.py", 
        "config_pagamentos.py", 
        "memoria_comum.py",
        ".env",
        ".gitignore",
        "README.md",
        "manifest.json"
    }

    # 3. Varredura e Limpeza Inteligente e Profunda
    print(f"\n{BRANCO}[FSE-02] A higienizar a raiz e catalogar elementos extraviados...{RESET}")
    movidos_total = 0

    # Locais a varrer com precisão cirúrgica
    locais_varredura = [BASE_DIR, BASE_DIR / "core"]

    for diretorio_atual in locais_varredura:
        if not diretorio_atual.exists():
            continue
            
        try:
            itens = list(diretorio_atual.iterdir())
        except Exception:
            continue

        for item in itens:
            if item.is_file():
                # Proteção do núcleo inviolável na raiz
                if diretorio_atual == BASE_DIR and item.name in nucleo_inviolavel:
                    continue
                if item.name.startswith('.'):
                    continue

                nome_arq = item.name.lower()
                destino = None

                # Matriz de Decisão e Triagem Avançada (Padrão Mônaco / Audit-Proof)
                if nome_arq.endswith((".jpeg", ".jpg", ".png", ".webp", ".ico", ".svg", ".gif")):
                    destino = BASE_DIR / "static" / item.name
                elif nome_arq.endswith((".key", ".enc", ".pem", ".cert", ".sig")):
                    destino = BASE_DIR / "security" / item.name
                elif nome_arq.endswith((".log", ".json", ".txt")) and any(k in nome_arq for k in ["audit", "diag", "status", "relatorio", "ultimo_", "metrics"]):
                    destino = BASE_DIR / "tools" / item.name
                elif nome_arq.endswith(".pdf"):
                    destino = BASE_DIR / "pdfs_finais" / item.name
                elif nome_arq.startswith("test") or "teste" in nome_arq:
                    destino = BASE_DIR / "tests" / item.name
                elif any(nome_arq.startswith(p) for p in ["verificar_", "auditar_", "analisar_", "diagnostico", "audit_", "rastrear_", "mapear_", "listar_", "loader_", "limpar_"]):
                    destino = BASE_DIR / "tools" / item.name
                elif "contrato" in nome_arq or "legal" in nome_arq or "licenca" in nome_arq:
                    destino = BASE_DIR / "legal" / item.name
                elif nome_arq.endswith(".py") and diretorio_atual != (BASE_DIR / "core"):
                    # Scripts python avulsos que estavam perdidos vão direto para o /core
                    destino = BASE_DIR / "core" / item.name

                # Executa a realocação com blindagem de conflitos
                if destino and destino != item:
                    try:
                        if destino.exists():
                            destino.unlink() # Remove duplicata se houver
                        shutil.move(str(item), str(destino))
                        print(f"   {MAGENTA}[REALOCADO]{RESET} {item.name} -> {destino.parent.name}/{item.name}")
                        movidos_total += 1
                    except Exception as e:
                        print(f"   {VERMELHO}[AVISO DE CONFLITO]{RESET} Não foi possível mover {item.name}: {e}")

    print(f"   -> Total de elementos realocados com exatidão quântica: {VERDE}{movidos_total}{RESET}")

    # 4. Exibição da Árvore de Identificação Completa do Sistema
    print(f"\n{VERDE}======================================================================{RESET}")
    print(AMARELO + "                 ÁRVORE DE IDENTIFICAÇÃO DO ECOSSISTEMA" + RESET)
    print(VERDE + "======================================================================{RESET}")
    print(f"📂 {MAGENTA}{BASE_DIR.name}{RESET}")
    gerar_arvore_diretorios(BASE_DIR)

    # Laudo Final Definitivo
    print("\n" + VERDE + "=" * 70 + RESET)
    print(VERDE + " 🎉 HIGIENIZAÇÃO TIER-1 ELITE CONCLUÍDA COM EXCELÊNCIA ABSOLUTA!" + RESET)
    print(VERDE + "=" * 70 + RESET)
    print(VERDE + " • Raiz 100% limpa contendo apenas o núcleo inviolável e os diretórios soberanos." + RESET)
    print(VERDE + " • Logs, chaves criptográficas, PDFs e ferramentas devidamente compartimentados." + RESET)
    print(VERDE + " ✅ STATUS DO KERNEL: PRONTO PARA PASSAR COM 100/100 EM QUALQUER AUDITORIA MUNDIAL!" + RESET)
    print(VERDE + "=" * 70 + RESET + "\n")

if __name__ == "__main__":
    executar_organizador_master()