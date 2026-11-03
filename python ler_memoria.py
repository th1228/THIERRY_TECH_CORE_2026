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

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -*- coding: utf-8 -*-
import os
import json

CAMINHO_SESSAO = "storage/memoria_sessao.json"

# Lista de todas as chaves esperadas pelo ecossistema TTC Global
CHAVES_ESPERADAS = [
    "ultimo_clima_capturado",
    "biometria",
    "tipo_rosto",
    "hash_cript",
    "base_pintura",
    "mechas",
    "longevidade_botulinica",
    "arduino_sensor_link",
    "indice_inflamatorio",
    "laudo_limbico",
    "cortes_sugeridos",
    "penteados",
    "ultimo_relatorio_gerado"
]

def inspecionar_tudo():
    print("=" * 70)
    print("  INSPEÇÃO DE INTEGRIDADE DA MEMÓRIA COMUM — TTC GLOBAL")
    print("=" * 70)
    
    # Carrega os dados reais do arquivo JSON
    dados_salvos = {}
    if os.path.exists(CAMINHO_SESSAO):
        try:
            with open(CAMINHO_SESSAO, "r", encoding="utf-8") as f:
                dados_salvos = json.load(f)
        except Exception as e:
            print(f"[ALERTA] Erro ao ler o arquivo JSON: {e}")
    else:
        print(f"[AVISO] Arquivo de sessão não encontrado em '{CAMINHO_SESSAO}'. Nenhuma chave foi gravada ainda.\n")

    print("\n🟢 [ 1. DADOS GRAVADOS NA SESSÃO ATUAL ]")
    print("-" * 50)
    if dados_salvos:
        for chave, conteudo in dados_salvos.items():
            if isinstance(conteudo, dict):
                valor = conteudo.get("valor", conteudo)
                ts = conteudo.get("timestamp", "Sem timestamp")
                print(f"  • {chave.upper()}")
                print(f"    └─ Valor: {valor}")
                print(f"    └─ Atualizado em: {ts}")
            else:
                print(f"  • {chave.upper()}: {conteudo}")
    else:
        print("  (Nenhum dado gravado até o momento)")

    print("\n🔴 [ 2. CHAVES PENDENTES / NÃO GRAVADAS NA MEMÓRIA ]")
    print("-" * 50)
    pendentes = [c for c in CHAVES_ESPERADAS if c not in dados_salvos]
    
    if pendentes:
        for chave in pendentes:
            print(f"  • {chave.upper()} (Aguardando injeção ou leitura de hardware/módulo)")
    else:
        print("  (Excelente! Todas as chaves esperadas do ecossistema estão preenchidas)")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    inspecionar_tudo()