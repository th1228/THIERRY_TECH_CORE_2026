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
import importlib

# --- BLOCO DE CONEXÃO ESTRUTURAL ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from core.memoria_comum import instancia_memoria
    print("🧠 Memória Comum conectada com sucesso.")
except ImportError as e:
    instancia_memoria = None
    print(f"⚠️ Memória Comum não encontrada: {e}")

def carregar_todos_os_modulos():
    """
    Varre tanto a raiz do projeto quanto a pasta core para 
    integrar dinamicamente todos os motores disponíveis.
    """
    modulos_carregados = 0
    diretorio_raiz = "."
    pasta_core = "core"

    # 1. Carrega motores da raiz (como os arquivos monaco_*.py)
    print("\n🔍 Verificando motores na Raiz...")
    for arquivo in os.listdir(diretorio_raiz):
        if arquivo.endswith(".py") and arquivo not in ["carregador_automatico.py", "__init__.py"]:
            nome_modulo = arquivo[:-3]
            try:
                importlib.import_module(nome_modulo)
                print(f"✅ Módulo raiz integrado: {nome_modulo}")
                modulos_carregados += 1
            except Exception as e:
                # Ignora arquivos que não são módulos importáveis diretamente
                pass

    # 2. Carrega motores de dentro da pasta core
    print("\n🔍 Verificando motores na pasta Core...")
    if os.path.exists(pasta_core):
        for arquivo in os.listdir(pasta_core):
            if arquivo.endswith(".py") and arquivo != "__init__.py":
                nome_modulo = arquivo[:-3]
                try:
                    importlib.import_module(f"{pasta_core}.{nome_modulo}")
                    print(f"✅ Módulo core integrado: {nome_modulo}")
                    modulos_carregados += 1
                except Exception as e:
                    print(f"⚠️ Falha ao carregar core.{nome_modulo}: {e}")

    print(f"\n📊 Total geral de módulos integrados: {modulos_carregados}")

    if instancia_memoria is not None:
        instancia_memoria.salvar_dados("STATUS_AUTO_CARREGAMENTO", {
            "total_integrados": modulos_carregados,
            "status": "ativo"
        })

if __name__ == "__main__":
    print("=========================================================")
    print("TTC GLOBAL - CARREGAMENTO HÍBRIDO (RAIZ + CORE)")
    print("=========================================================")
    carregar_todos_os_modulos()
    print("=========================================================")