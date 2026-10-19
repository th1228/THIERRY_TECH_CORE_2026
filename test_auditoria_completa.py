# -*- coding: utf-8 -*-
"""
Módulo de Auditoria Automatizada Integrada - Thierry Technology Concept Global
Executa verificação de segurança (Bandit), análise sintática (AST) e consolida
todos os erros e falhas exclusivamente no relatório final.
"""

import os
import sys
import ast
import subprocess

TARGET_FILE = "mapeamento_avaliação.py"  # Altere para o nome exato do arquivo alvo se necessário

def print_header(title):
    print("\n" + "="*80)
    print(f" {title} ".center(80, "="))
    print("="*80)

def executar_auditoria():
    erros_criticos = []
    alertas_seguranca = []
    
    print_header("INICIANDO VARREDURA DE AUDITORIA GLOBAL")
    
    # 1. Verificação de Existência do Arquivo
    if not os.path.exists(TARGET_FILE):
        erros_criticos.append({
            "fator": "Existência do Arquivo",
            "detalhe": f"O arquivo alvo '{TARGET_FILE}' não foi encontrado no diretório.",
            "correcao": "Certifique-se de colocar o script na mesma pasta do arquivo a ser auditado ou corrigir o caminho em TARGET_FILE."
        })
        # Se o arquivo não existe, já retorna o relatório com o erro fatal
        exibir_relatorio_final(erros_criticos, alertas_seguranca)
        sys.exit(1)
        
    print(f"[+] Ativo localizado: {os.path.abspath(TARGET_FILE)}")

    # 2. Análise Estrutural AST e Sintaxe
    try:
        with open(TARGET_FILE, "r", encoding="utf-8") as f:
            origem = f.read()
        arvore = ast.parse(origem)
        print("[+] Análise sintática AST concluída com sucesso.")
    except SyntaxError as e:
        erros_criticos.append({
            "fator": "Erro de Sintaxe (AST)",
            "detalhe": f"Linha {e.lineno}: {e.msg}",
            "correcao": "Corrija a estrutura sintática incorreta apontada no código Python."
        })
    except Exception as e:
        erros_criticos.append({
            "fator": "Erro de Leitura",
            "detalhe": str(e),
            "correcao": "Verifique as permissões de leitura do arquivo."
        })

    # 3. Execução do Bandit (Análise de Segurança OWASP)
    print("[*] Executando varredura de segurança OWASP via Bandit...")
    try:
        resultado_bandit = subprocess.run(
            ["bandit", "-r", TARGET_FILE, "-f", "json"],
            capture_output=True,
            text=True
        )
        
        if resultado_bandit.returncode != 0 and resultado_bandit.stdout:
            import json
            dados_bandit = json.loads(resultado_bandit.stdout)
            for resultado in dados_bandit.get("results", []):
                alertas_seguranca.append({
                    "severidade": resultado.get("severity"),
                    "confianca": resultado.get("confidence"),
                    "teste_id": resultado.get("test_id"),
                    "linha": resultado.get("line_number"),
                    "descricao": resultado.get("issue_text"),
                    "correcao": f"Revisar o trecho na linha {resultado.get('line_number')} conforme diretriz de segurança OWASP para o código {resultado.get('test_id')}."
                })
        else:
            print("[+] Nenhuma vulnerabilidade crítica detectada pelo Bandit.")
    except FileNotFoundError:
        alertas_seguranca.append({
            "severidade": "AVISO",
            "confianca": "ALTA",
            "teste_id": "DEPENDENCY_MISSING",
            "linha": 0,
            "descricao": "A ferramenta 'bandit' não está instalada no ambiente Python.",
            "correcao": "Instale o bandit executando 'pip install bandit' no seu terminal."
        })
    except Exception as e:
        alertas_seguranca.append({
            "severidade": "ERRO",
            "confianca": "MÉDIA",
            "teste_id": "EXECUTION_ERROR",
            "linha": 0,
            "descricao": f"Falha ao executar o Bandit: {str(e)}",
            "correcao": "Verifique o ambiente e as dependências instaladas."
        })

    # Exibe o relatório consolidado apenas ao final
    exibir_relatorio_final(erros_criticos, alertas_seguranca)

def exibir_relatorio_final(erros_criticos, alertas_seguranca):
    print_header("RELATÓRIO CONSOLIDADO DE FALHAS E AUDITORIA")
    
    total_erros = len(erros_criticos)
    total_alertas = len(alertas_seguranca)
    
    print(f"Total de Erros Críticos Encontrados: {total_erros}")
    print(f"Total de Alertas de Segurança (Bandit): {total_alertas}")
    print("-" * 80)
    
    if total_erros == 0 and total_alertas == 0:
        print("\n[SUCESSO] O código passou em todas as verificações sem nenhuma falha detectada!")
    else:
        if total_erros > 0:
            print("\n[!] ERROS CRÍTICOS A CORRIGIR:")
            for i, err in enumerate(erros_criticos, 1):
                print(f"  {i}. Fator: {err['fator']}")
                print(f"     Detalhe: {err['detalhe']}")
                print(f"     Como arrumar: {err['correcao']}")
                print()
                
        if total_alertas > 0:
            print("\n[!] ALERTAS DE SEGURANÇA E VULNERABILIDADES (BANDIT):")
            for i, alt in enumerate(alertas_seguranca, 1):
                print(f"  {i}. [Severidade: {alt['severidade']}] ID: {alt['teste_id']} (Linha {alt['linha']})")
                print(f"     Descrição: {alt['descricao']}")
                print(f"     Como arrumar: {alt['correcao']}")
                print()
                
    print("=" * 80)
    print("FIM DA AUDITORIA".center(80, "="))
    print("=" * 80)

if __name__ == "__main__":
    executar_auditoria()