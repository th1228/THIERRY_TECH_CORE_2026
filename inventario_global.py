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
import os
import sys

# Garante o acesso aos caminhos da raiz e da pasta core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def gerar_inventario_completo():
    print("=================================================================")
    print("📋 RAIO-X GLOBAL DO PROJETO - INVENTÁRIO E ESTRUTURA")
    print("=================================================================")
    
    diretorio_raiz = "."
    pasta_core = "core"
    
    # 1. Análise da Raiz (Onde ficam o main.py e os núcleos Monaco)
    print("\n[1] MÓDULOS E ARQUIVOS NA RAIZ (Controle e Orquestração):")
    arquivos_raiz = [f for f in os.listdir(diretorio_raiz) if os.path.isfile(f)]
    
    total_raiz = 0
    for arq in sorted(arquivos_raiz):
        if arq.endswith(".py"):
            print(f"   🐍 (Python) {arq}")
            total_raiz += 1
        elif arq.endswith((".txt", ".json", ".pdf", ".html")):
            print(f"   📄 (Dado/Config) {arq}")
    print(f"   ➡️ Total de arquivos Python na raiz: {total_raiz}")

    # 2. Análise da Pasta Core (Onde ficam os motores especializados)
    print("\n[2] MÓDULOS NA PASTA CORE (Motores Especializados):")
    total_core = 0
    if os.path.exists(pasta_core):
        arquivos_core = os.listdir(pasta_core)
        for arq in sorted(arquivos_core):
            if arq.endswith(".py"):
                print(f"   ⚙️ core.{arq[:-3]}")
                total_core += 1
    else:
        print("   ⚠️ A pasta 'core' não foi encontrada.")
    print(f"   ➡️ Total de motores na pasta core: {total_core}")

    # 3. Verificação do Orquestrador e Memória Comum
    print("\n[3] STATUS DOS NÚCLEOS PRINCIPAIS:")
    tem_main = os.path.exists("main.py")
    tem_memoria = os.path.exists(os.path.join(pasta_core, "memoria_comum.py"))
    
    print(f"   🎯 Orquestrador principal (main.py): {'✅ Presente' if tem_main else '❌ Ausente'}")
    print(f"   🧠 Memória Comum (core/memoria_comum.py): {'✅ Presente' if tem_memoria else '❌ Ausente'}")

    # 4. Tentativa de inspecionar o comportamento da Memoria Comum (Fila/Dados)
    if tem_memoria:
        try:
            from core.memoria_comum import instancia_memoria
            if instancia_memoria is not None:
                print("\n[4] DIAGNÓSTICO DA MEMÓRIA COMUM:")
                print("   🔗 Instância da memória carregada com sucesso pelo inventário.")
                # Tenta puxar dados se houver método compatível
                if hasattr(instancia_memoria, "carregar_dados"):
                    dados = instancia_memoria.carregar_dados()
                    print(f"   📦 Registros atuais na fila/memória: {len(dados) if dados else 0}")
                else:
                    print("   📦 Memória ativa e operando por fluxo direto.")
            else:
                print("\n[4] ⚠️ A memória comum existe, mas a instância retornou vazia.")
        except Exception as e:
            print(f"\n[4] ⚠️ Não foi possível inspecionar os dados internos da memória: {e}")

    print("\n=================================================================")
    print(f"📊 RESUMO: {total_raiz} scripts na raiz + {total_core} motores no core.")
    print("=================================================================")

if __name__ == "__main__":
    gerar_inventario_completo()