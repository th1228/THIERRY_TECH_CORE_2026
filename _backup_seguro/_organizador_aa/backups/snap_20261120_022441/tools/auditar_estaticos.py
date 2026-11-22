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
from collections import defaultdict

def auditar_pdf_clientes(diretorio_base=".", termo_busca="Genilson"):
    print(f"\n🔍 AUDITORIA DE PDF: Localizando onde o nome '{termo_busca}' injeta dados no PDF do Cliente\n" + "="*75)
    
    # Arquivos que geram os PDFs e Dossiês do cliente
    arquivos_relatorio_pdf = {
        'gerador_dossies_master.py',
        'monaco_modelagem_engine.py',
        'super_retorno_financeiro.py',
        'tricologia_ultra_avancada.py'
    }
    
    pastas_ignoradas = {'.git', '__pycache__', 'venv', '.venv', 'env', '.vscode', 'node_modules'}
    ocorrencias_por_arquivo = defaultdict(list)
    
    for raiz, diretorios, arquivos in os.walk(diretorio_base):
        diretorios[:] = [d for d in diretorios if d not in pastas_ignoradas]
            
        for arquivo in arquivos:
            if arquivo in arquivos_relatorio_pdf:
                caminho_completo = os.path.join(raiz, arquivo)
                try:
                    with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as f:
                        for numero_linha, linha in enumerate(f, 1):
                            if termo_busca.lower() in linha.lower():
                                caminho_relativo = os.path.relpath(caminho_completo, diretorio_base)
                                ocorrencias_por_arquivo[caminho_relativo].append((numero_linha, linha.strip()))
                except Exception:
                    pass

    print("🎯 ARQUIVOS EXATOS QUE GERAM O PDF E PRECISAM DE DADOS DINÂMICOS:\n")
    
    if not ocorrencias_por_arquivo:
        print("✅ Nenhum arquivo de relatório/PDF com valor estático foi encontrado!")
    else:
        for i, (arquivo, linhas) in enumerate(ocorrencias_por_arquivo.items(), 1):
            print(f"[{i}] Arquivo: {arquivo}")
            for num_linha, conteudo in linhas:
                print(f"    └─ Linha {num_linha}: {conteudo}")
            print("-" * 75)

    print("\n📌 RESUMO DE AÇÃO:")
    print("Abra no VS Code exatamente os arquivos listados acima e substitua 'Genilson Rodrigues'")
    print("pela variável dinâmica do cliente/paciente (ex: `dados_paciente['nome']`).")
    print("="*75 + "\n")

if __name__ == "__main__":
    auditar_pdf_clientes(".", "Genilson")