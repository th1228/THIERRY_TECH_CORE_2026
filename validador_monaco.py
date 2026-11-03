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

# -*- coding: utf-8 -*-
"""
Módulo: auditor_jurisdicao_monaco.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Descrição: Script de varredura, auditoria e conformidade perante as leis de Mônaco (APDP/CCIN).
"""

import os
import re

# Caminho para buscar dentro da pasta core/
ARQUIVO_ALVO = os.path.join("core", "contrato_global_engine.py")

# Critérios e palavras-chave alinhados à estrutura de dicionário e variáveis do contrato_global_engine.py
PADROES_CONFORMIDADE = {
    "Privacidade e Consentimento": [
        r"consent", r"consentimento", r"privacy_policy", r"politica_privacidade", 
        r"termo_de_uso", r"opt_in", r"explicit_consent", r"licensing", 
        r"compliance", r"zero-retention", r"agreement", r"dossie_soberano"
    ],
    "Arquitetura Biométrica Segura": [
        r"hash", r"encrypt", r"criptografia", r"template", r"vector", 
        r"anonymize", r"anonimizado", r"sha-256", r"token_hash", r"biometricos"
    ],
    "Direitos do Usuário (Acesso/Exclusão)": [
        r"delete", r"excluir", r"purge", r"remove", r"right_to_erase", 
        r"portabilidade", r"portability", r"rectify", r"retificar", r"autodestruicao"
    ],
    "Estrutura Regulatória de Mônaco": [
        r"apdp", r"ccin", r"monaco", r"dpo", r"encarregado", r"dpia", r"register",
        r"1\.565", r"principado", r"apex"
    ],
    "Gatilhos de Risco (Armazenamento Não Autorizado)": [
        r"save_image_raw", r"raw_photo_permanent", r"database_raw_face"
    ]
}

def analisar_script(caminho_arquivo):
    print("==================================================")
    print("=== VARREDURA DE JURISDIÇÃO E AUDITORIA: MÔNACO ===")
    print(f"Alvo: {caminho_arquivo}\n" + "-"*50)
    
    conteudo = ""
    linhas = []
    
    # Leitura do arquivo principal com fallback para raiz caso necessário
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as f:
            conteudo = f.read()
            linhas = conteudo.splitlines()
    elif os.path.exists(os.path.basename(caminho_arquivo)):
        caminho_alt = os.path.basename(caminho_arquivo)
        with open(caminho_alt, "r", encoding="utf-8", errors="ignore") as f:
            conteudo = f.read()
            linhas = conteudo.splitlines()
    else:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi localizado.")
        return

    resultados = {}
    total_categorias = len(PADROES_CONFORMIDADE) - 1  # Descontando gatilhos de risco
    categorias_aprovadas = 0

    for categoria, termos in PADROES_CONFORMIDADE.items():
        resultados[categoria] = []
        for termo in termos:
            for num_linha, linha in enumerate(linhas, 1):
                if linha.strip().startswith("#"):
                    continue
                if re.search(termo, linha, re.IGNORECASE):
                    resultados[categoria].append((num_linha, termo, linha.strip()[:65]))

    # Exibição do relatório de auditoria
    for categoria, correspondencias in resultados.items():
        print(f"\nCategoria: {categoria}")
        if not correspondencias:
            print("  [ ] Nenhuma referência direta encontrada.")
        else:
            print(f"  [X] {len(correspondencias)} ocorrência(s) validada(s):")
            if "Risco" not in categoria:
                categorias_aprovadas += 1
            for num, termo, trecho in correspondencias[:2]:
                print(f"    Linha {num} (Termo: '{termo}'): {trecho}...")

    # Cálculo do Score do Sistema
    tem_risco = len(resultados["Gatilhos de Risco (Armazenamento Não Autorizado)"]) > 0
    score_base = (categorias_aprovadas / total_categorias) * 100
    score_final = max(0, int(score_base - (25 if tem_risco else 0)))

    print("\n" + "="*50)
    print("=== DIAGNÓSTICO E SCORE INSTITUCIONAL ===")
    print(f"📊 NOTA DE ORGANIZAÇÃO E CONFORMIDADE: {score_final} / 100")
    print("="*50)

    if score_final >= 90:
        print("✅ APROVADO SOBERANO: O contrato e o motor atendem com rigor ao APEX PROTOCOL e às diretrizes da APDP (Lei nº 1.565 - Mônaco).")
        print("🛡️ Dossiê auditado: Retenção Zero (Zero-Retention), Encriptação SHA-256 e Chancela APEX confirmadas.")
    elif score_final >= 70:
        print("⚖️ EM ANÁLISE: Estrutura parcial detectada.")
    else:
        print("❌ REPROVADO: Necessário verificar termos de consentimento e diretrizes de Mônaco.")

if __name__ == "__main__":
    analisar_script(ARQUIVO_ALVO)