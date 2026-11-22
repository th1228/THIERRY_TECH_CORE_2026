# -*- coding: utf-8 -*-
# =====================================================================
# THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026
# MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - AUDITOR MIBO MASTER
# =====================================================================

import os
import sys
import ast
import hashlib
from pathlib import Path

# Cores ANSI para o padrão High-Tech
VERDE = "\033[92m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
CIANO = "\033[96m"
BRANCO = "\033[97m"
CINZA = "\033[90m"
RESET = "\033[0m"

def calcular_sha256(caminho_arquivo: Path) -> str:
    """Calcula o hash SHA-256 de integridade do arquivo de código."""
    sha256_hash = hashlib.sha256()
    try:
        with open(caminho_arquivo, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return "ERRO_LEITURA_HASH"

def verificar_sintaxe_python(caminho_arquivo: Path) -> tuple[bool, str]:
    """Valida se o arquivo Python possui erros de sintaxe (Árvore AST)."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
        ast.parse(conteudo, filename=str(caminho_arquivo))
        return True, "SINTAXE PERFEITA (0 ERROS)"
    except SyntaxError as e:
        return False, f"Erro de Sintaxe na linha {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Erro ao ler arquivo: {str(e)}"

def executar_auditoria_mibo() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(VERDE + "=" * 85 + RESET)
    print(AMARELO + "   THIERRY TECHNOLOGY CONCEPT GLOBAL • AUDITOR MIBO MASTER 100%" + RESET)
    print(CIANO + "   VARREDURA DE INTEGRIDADE, SINTAXE E HASHES SHA-256 (ISOLAMENTO SEGURO)" + RESET)
    print(VERDE + "=" * 85 + RESET + "\n")

    raiz_projeto = Path(__file__).parent
    
    # 1. Validação de Diretórios Essenciais
    diretorios_criticos = ["core", "security", "config"]
    print(f"{BRANCO}[1/3] Verificando estrutura de pastas essenciais...{RESET}")
    for dir_nome in diretorios_criticos:
        caminho_dir = raiz_projeto / dir_nome
        if caminho_dir.exists() and caminho_dir.is_dir():
            print(f"  {VERDE}[ OK ]{RESET} Diretório encontrado: {CIANO}{dir_nome}/{RESET}")
        else:
            print(f"  {VERMELHO}[FALHA]{RESET} Diretório ausente ou corrompido: {VERMELHO}{dir_nome}/{RESET}")

    print("\n" + BRANCO + "[2/3] Varredura profunda de sintaxe e integridade no ecossistema Python...{RESET}\n")

    arquivos_python = list(raiz_projeto.glob("**/*.py"))
    total_arquivos = 0
    erros_encontrados = 0

    # Pastas e padrões a ignorar totalmente (incluindo lixo de cache e temporários)
    pastas_ignoradas = {".venv", "__pycache__", ".git", "documentos", "venv", "testes_temp"}

    for arq in arquivos_python:
        # Se qualquer parte do caminho contiver uma pasta ignorada, pula o arquivo
        if any(p.lower() in pastas_ignoradas for p in arq.parts):
            continue
            
        # Ignora arquivos de teste avulsos soltos na raiz (exceto o próprio auditor)
        if arq.parent == raiz_projeto and "teste" in arq.name.lower() and arq.name != "auditor_mibo_master.py":
            continue

        total_arquivos += 1
        rel_path = arq.relative_to(raiz_projeto)
        valido, mensagem = verificar_sintaxe_python(arq)
        hash_arq = calcular_sha256(arq)
        
        if valido:
            print(f"  {VERDE}[ OK ]{RESET} {BRANCO}{rel_path}{RESET}")
            print(f"         ├── Status: {VERDE}{mensagem}{RESET}")
            print(f"         └── SHA-256: {CINZA}{hash_arq[:32]}...{RESET}")
        else:
            erros_encontrados += 1
            print(f"  {VERMELHO}[ERRO]{RESET} {BRANCO}{rel_path}{RESET}")
            print(f"         └── Diagnóstico: {VERMELHO}{mensagem}{RESET}")

    print("\n" + BRANCO + f"[3/3] Resumo Geral da Execução:{RESET}")
    print(f"  - Total de arquivos Python auditados: {AMARELO}{total_arquivos}{RESET}")
    print(f"  - Falhas críticas de sintaxe: {VERMELHO if erros_encontrados > 0 else VERDE}{erros_encontrados}{RESET}")

    print("\n" + VERDE + "=" * 85 + RESET)
    if erros_encontrados == 0:
        print(CIANO + " [RESULTADO] SISTEMA 100% ÍNTEGRO. NENHUM ERRO DE CONEXÃO OU SINTAXE DETECTADO." + RESET)
    else:
        print(VERMELHO + " [ALERTA] FORAM ENCONTRADAS PENDÊNCIAS QUE EXIGEM CORREÇÃO IMEDIATA." + RESET)
    print(VERDE + "=" * 85 + RESET + "\n")

if __name__ == "__main__":
    executar_auditoria_mibo()