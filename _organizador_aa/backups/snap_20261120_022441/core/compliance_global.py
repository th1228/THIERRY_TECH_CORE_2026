# -*- coding: utf-8 -*-
"""
Módulo Oficial de Compliance e Auditoria - Thierry Technology Concept Global
Validação Estrutural, Volumétrica e Relatório Consolidado Alinhado
"""

import os
import sys
import ast
import subprocess

REPORT_FILE = "relatorio_compliance.txt"

def obter_arquivos_producao():
    """Identifica apenas os ficheiros de produção reais do projeto."""
    arquivos_alvo = []
    for root, dirs, files in os.walk('.'):
        if any(p in root for p in ['.git', '__pycache__', 'venv', '.vscode']):
            continue
        for file in files:
            if file.endswith('.py'):
                if file.startswith('test_') or file.startswith('auditor') or file.startswith('complies') or 'tempCodeRunnerFile' in file:
                    continue
                caminho_relativo = os.path.join(root, file)
                arquivos_alvo.append(caminho_relativo)
    return arquivos_alvo

def auditar_ativos(arquivos, output):
    """Executa a análise estrutural e volumetria dos ativos de código."""
    output.write("="*80 + "\n")
    output.write("1. ANÁLISE ESTRUTURAL E VOLUMETRIA DE ATIVOS (PRODUÇÃO)\n")
    output.write("="*80 + "\n")
    
    if not arquivos:
        output.write("\n[-] Nenhum ativo de produção localizado para análise.\n")
        return

    for arq in arquivos:
        output.write(f"\n[+] ATIVO ANALISADO: {arq}\n")
        output.write(f"    - Tamanho: {os.path.getsize(arq)} bytes\n")
        
        with open(arq, "r", encoding="utf-8", errors="ignore") as f:
            linhas = f.readlines()
        total_linhas = len(linhas)
        linhas_vazias = sum(1 for l in linhas if not l.strip())
        comentarios = sum(1 for l in linhas if l.strip().startswith("#"))
        linhas_codigo = total_linhas - linhas_vazias - comentarios
        
        output.write(f"    - Total de Linhas: {total_linhas}\n")
        output.write(f"    - Linhas de Código Efetivo: {linhas_codigo}\n")
        output.write(f"    - Linhas de Comentários: {comentarios}\n")
        
        with open(arq, "r", encoding="utf-8", errors="ignore") as f:
            origem = f.read()
        try:
            arvore = ast.parse(origem)
            funcoes = [n for n in ast.walk(arvore) if isinstance(n, ast.FunctionDef)]
            classes = [n for n in ast.walk(arvore) if isinstance(n, ast.ClassDef)]
            
            output.write(f"    - Classes Mapeadas: {len(classes)}\n")
            output.write(f"    - Funções Extraídas: {len(funcoes)}\n")
            
            res = subprocess.run([sys.executable, "-m", "py_compile", arq], capture_output=True, text=True)
            status = "OK (Integridade Confirmada)" if res.returncode == 0 else "FALHA NA COMPILAÇÃO"
            output.write(f"    - Status de Integridade: {status}\n")
            
        except SyntaxError as e:
            output.write(f"    [-] ERRO DE SINTAXE: Linha {e.lineno}: {e.msg}\n")
        output.write("-" * 50 + "\n")

def executar_seguranca(arquivos, output):
    """Executa a verificação estática de segurança utilizando a lista limpa."""
    output.write("\n" + "="*80 + "\n")
    output.write("2. AUDITORIA DE SEGURANÇA E COMPLIANCE INTERNACIONAL\n")
    output.write("="*80 + "\n")
    
    if not arquivos:
        output.write("[*] Nenhum ficheiro para análise de segurança.\n")
        return

    output.write(f"[*] Executando varredura estática em {len(arquivos)} módulos limpos...\n\n")
    
    try:
        comando = ["bandit"] + arquivos
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        if resultado.returncode == 0 or resultado.returncode == 1:
            if resultado.stdout.strip():
                output.write(resultado.stdout)
            else:
                output.write("[+] Status: Nenhuma violação detectada nos módulos auditados.\n")
        else:
            output.write("[-] A ferramenta retornou um aviso de execução.\n")
            output.write(resultado.stderr)
            
    except FileNotFoundError:
        output.write("[-] Ferramenta 'bandit' não localizada no ambiente Python.\n")

def gerar_sumario_alinhado(arquivos):
    """Gera um sumário executivo formatado em colunas alinhadas no terminal."""
    print("\n" + "="*85)
    print("                    SUMÁRIO EXECUTIVO DE ATIVOS DE PRODUÇÃO")
    print("="*85)
    print(f"{'FICHEIRO DE ATIVO':<50} | {'STATUS DE INTEGRIDADE':<30}")
    print("-" * 85)
    
    status_lista = []
    for arq in arquivos:
        try:
            res = subprocess.run([sys.executable, "-m", "py_compile", arq], capture_output=True, text=True)
            if res.returncode == 0:
                status = "[OK] APROVADO"
            else:
                status = "[!] FALHA DE SINTAXE"
        except (subprocess.SubprocessError, OSError):
            status = "[X] ERRO CRÍTICO"
            
        print(f"{arq:<50} | {status:<30}")
        status_lista.append((arq, status))
        
    print("="*85)
    return status_lista

if __name__ == "__main__":
    print("[*] Iniciando compliance e auditoria global...")
    
    ativos = obter_arquivos_producao()
    
    with open(REPORT_FILE, "w", encoding="utf-8") as relatorio:
        relatorio.write("="*80 + "\n")
        relatorio.write("   RELATÓRIO OFICIAL DE COMPLIANCE - THIERRY TECHNOLOGY CONCEPT GLOBAL\n")
        relatorio.write("="*80 + "\n")
        
        auditar_ativos(ativos, relatorio)
        executar_seguranca(ativos, relatorio)
        
        relatorio.write("\n" + "="*80 + "\n")
        relatorio.write("               FIM DO RELATÓRIO - AUDITORIA CONCLUÍDA COM SUCESSO\n")
        relatorio.write("="*80 + "\n")

    # Exibe o relatório detalhado e logo abaixo o sumário alinhado no terminal
    with open(REPORT_FILE, "r", encoding="utf-8") as relatorio:
        print(relatorio.read())
        
    gerar_sumario_alinhado(ativos)
    
    print(f"\n[+] SUCESSO! Relatório consolidado guardado em: {os.path.abspath(REPORT_FILE)}")
