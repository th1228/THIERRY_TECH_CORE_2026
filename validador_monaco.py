# -*- coding: utf-8 -*-
"""
Módulo: auditor_jurisdicao_monaco.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Descrição: Script de varredura e conformidade perante as leis de Mônaco e diretrizes APDP/CCIN.
"""

import os
import re

# Caminho corrigido para buscar dentro da pasta core/
ARQUIVO_ALVO = os.path.join("core", "contrato_global_engine.py")

# Critérios e palavras-chave baseados na regulamentação de Mônaco e regras de privacidade/APDP
PADROES_CONFORMIDADE = {
    "Privacidade e Consentimento": [
        r"consent", r"consentimento", r"privacy_policy", r"politica_privacidade", 
        r"termo_de_uso", r"opt_in", r"explicit_consent"
    ],
    "Arquitetura Biométrica Segura": [
        r"hash", r"encrypt", r"criptografia", r"template", r"vector", 
        r"anonymize", r"anonimizado"
    ],
    "Direitos do Usuário (Acesso/Exclusão)": [
        r"delete", r"excluir", r"purge", r"remove", r"right_to_erase", 
        r"portabilidade", r"portability", r"rectify", r"retificar"
    ],
    "Estrutura Regulatória de Mônaco": [
        r"apdp", r"ccin", r"monaco", r"dpo", r"encarregado", r"dpia", r"register"
    ],
    "Gatilhos de Risco (Excesso de armazenamento)": [
        r"save_image", r"raw_photo", r"camera_capture", r"database", r"base_de_dados"
    ]
}

def analisar_script(caminho_arquivo):
    print(f"=== INICIANDO VARREDURA DE JURISDIÇÃO: MÔNACO ===")
    print(f"Alvo: {caminho_arquivo}\n" + "-"*50)
    
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
            linhas = conteudo.splitlines()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado na pasta core.")
        return

    resultados = {}
    
    for categoria, termos in PADROES_CONFORMIDADE.items():
        resultados[categoria] = []
        for termo in termos:
            for num_linha, linha in enumerate(linhas, 1):
                if linha.strip().startswith("#"):
                    continue
                if re.search(termo, linha, re.IGNORECASE):
                    resultados[categoria].append((num_linha, termo, linha.strip()[:60]))

    # Exibição do relatório
    pontos_fortes = 0
    alertas_risco = 0

    for categoria, correspondencias in resultados.items():
        print(f"\nCategoria: {categoria}")
        if not correspondencias:
            print("  [ ] Nenhuma referência encontrada. Atenção necessária.")
            if "Risco" not in categoria:
                alertas_risco += 1
        else:
            print(f"  [X] {len(correspondencias)} ocorrência(s) encontrada(s):")
            if "Risco" in categoria:
                alertas_risco += len(correspondencias)
            else:
                pontos_fortes += 1
            for num, termo, trecho in correspondencias[:3]:
                print(f"    Linha {num} (Termo: '{termo}'): {trecho}...")

    print("\n" + "="*50)
    print("=== DIAGNÓSTICO PRELIMINAR ===")
    
    if resultados["Estrutura Regulatória de Mônaco"] == []:
        print("❌ REPROVADO: O script não cita conformidades locais (APDP/Mônaco) ou estruturas de DPO.")
    elif resultados["Privacidade e Consentimento"] == []:
        print("❌ REPROVADO: Biometria em Mônaco exige registro de consentimento explícito e inequívoco no fluxo do código.")
    else:
        print("⚖️ EM ANÁLISE: Foram detectados parâmetros de governança, mas valide as regras de armazenamento abaixo.")

    print("\n💡 RECOMENDAÇÃO TÉCNICA PRINCIPAL PARA MÔNACO:")
    print("A autoridade de Mônaco (APDP) proíbe rigorosamente salvar a foto bruta ('raw_photo') ou imagem do rosto do cliente.")
    print("O programa deve obrigatoriamente converter a face em um vetor matemático ('template' ou 'hash') criptografado e descartar a imagem original imediatamente.")

if __name__ == "__main__":
    analisar_script(ARQUIVO_ALVO)