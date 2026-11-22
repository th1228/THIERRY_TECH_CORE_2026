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
THIERRY TECH GLOBAL - DISPOSITIVO DE AUDITORIA DE CHAVES
-------------------------------------------------------
Este script isolado inspeciona o contrato de dados do Mibo para
garantir que nenhuma variável financeira retorne vazia (None).
"""

import os
import json

def executar_auditoria_de_chaves():
    print("=" * 65)
    print("   MIBO SOVEREIGN DIAGNOSTIC - VERIFICAÇÃO INTEGRAL DE CHAVES")
    print("   Thierry Technology Concept Global | Deep Tech & IP Moat")
    print("=" * 65)

    # Procuro o arquivo gerado pelo motor do seu Ledger
    arquivo_alvo = "c2_ledger_result.json"
    
    if not os.path.exists(arquivo_alvo):
        print(f"⚠️  [ARQUIVO AUSENTE]: Não encontrei o arquivo '{arquivo_alvo}' na raiz.")
        print("Certifique-se de que o motor que calcula os $3.5M USD rodou primeiro.")
        return

    try:
        with open(arquivo_alvo, 'r', encoding='utf-8') as f:
            dados_json = json.load(f)
    except Exception as e:
        print(f"❌ [ERRO DE LEITURA]: O arquivo JSON está corrompido ou malformado: {str(e)}")
        return

    # Captura das chaves da forma como o Python precisa ler para o PDF
    hash_criptografico = dados_json.get("sha256_ledger_hash", "NÃO ENCONTRADO")
    payload = dados_json.get("payload", {})
    financeiro = payload.get("financial_valuation", {})
    metrics_source = payload.get("metrics_source", {})
    meta_metricas = metrics_source.get("meta", {})
    score_saude = metrics_source.get("health_score", "NÃO ENCONTRADO")

    # Extração das variáveis finais de impacto do Mibo
    total_linhas_codigo = meta_metricas.get('total_lloc', None)
    modulos_escaneados = meta_metricas.get('scanned_modules', None)
    valor_em_usd = financeiro.get('asset_value_usd', None)
    valor_em_brl = financeiro.get('asset_value_brl', None)

    # EXIBIÇÃO DO VEREDITO NO TERMINAL
    print("\n🔍 [CONTRATO DE VARIÁVEIS EXTRAÍDO]:")
    print(f"   -> Hash do Ledger: {hash_criptografico}")
    print(f"   -> Score de Saúde: {score_saude}")
    print(f"   -> Linhas de Código (LLOC): {total_linhas_codigo}")
    print(f"   -> Módulos Analisados: {modulos_escaneados}")
    print(f"   -> Valoração Calculada (USD): {valor_em_usd}")
    print(f"   -> Valoração Calculada (BRL): {valor_em_brl}")
    print("-" * 65)

    # ANÁLISE DE ALINHAMENTO DA LÓGICA
    if None in [total_linhas_codigo, modulos_escaneados, valor_em_usd, valor_em_brl] or total_linhas_codigo == 0:
        print("❌ [ALERTA DE DESALINHAMENTO]: O Python encontrou valores vazios (None).")
        print("   As chaves internas do seu JSON não estão batendo com a pinça do get().")
    else:
        print("🏆 [SUCESSO ABSOLUTO]: Todas as chaves foram mapeadas com precisão!")
        print("   Seu pipeline de dados está pronto para alimentar a tabela do PDF de luxo.")
    print("=" * 65)

if __name__ == '__main__':
    executar_auditoria_de_chaves()