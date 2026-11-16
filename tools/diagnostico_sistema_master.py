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
Script de Varredura e Auditoria Completa (Versão Blindada & Tipada)
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent

def encontrar_arquivo_direto(nome_arquivo: str) -> Optional[Path]:
    """Busca o arquivo na raiz ou diretamente na pasta core."""
    caminho_raiz = BASE_DIR / nome_arquivo
    if caminho_raiz.exists():
        return caminho_raiz
        
    caminho_core = BASE_DIR / "core" / nome_arquivo
    if caminho_core.exists():
        return caminho_core
        
    return None

def auditoria_arquivo(nome_arquivo: str, termos_busca: list):
    print(f"\n==================================================")
    print(f"🔎 AUDITANDO: {nome_arquivo}")
    print(f"==================================================")
    
    arquivo_path = encontrar_arquivo_direto(nome_arquivo)
    
    if not arquivo_path or not arquivo_path.exists():
        print(f"❌ Arquivo não encontrado (Raiz ou core/): {nome_arquivo}")
        return

    print(f"✅ Localizado em: {arquivo_path.relative_to(BASE_DIR)}")

    try:
        with open(arquivo_path, "r", encoding="utf-8", errors="ignore") as f:
            conteudo = f.read()
            
        print(f"   • Tamanho: {len(conteudo)} caracteres.")
        
        for termo in termos_busca:
            ocorrencias = conteudo.count(termo)
            print(f"   • Ocorrências de '{termo}': {ocorrencias}")
            
        print("\n📌 Trechos Relevantes Encontrados:")
        linhas = conteudo.splitlines()
        encontrou_linha = False
        for idx, linha in enumerate(linhas, 1):
            linha_strip = linha.strip()
            linha_lower = linha.lower()
            
            if any(t.lower() in linha_lower for t in ["nome", "ceo_name", "cliente", "historico_clientes", "jose", "payload", "fetch", "body"]):
                if not linha_strip.startswith("#") and not linha_strip.startswith("//") and "import " not in linha_lower:
                    print(f"     [Linha {idx:04d}]: {linha_strip}")
                    encontrou_linha = True
                    
        if not encontrou_linha:
            print("   ⚠️ Nenhuma linha crítica de atribuição identificada.")

    except Exception as e:
        print(f"❌ Erro ao analisar {nome_arquivo}: {e}")

def auditoria_paineis_html():
    print(f"\n==================================================")
    print(f"🌐 AUDITORIA: PAINEIS HTML & SCRIPTS JS FRONT-END")
    print(f"==================================================")
    
    html_files = list(BASE_DIR.glob("**/*.html")) + list(BASE_DIR.glob("**/*.js"))
    files_filtrados = [f for f in html_files if "node_modules" not in str(f) and ".venv" not in str(f)]
    
    print(f"📄 Arquivos HTML/JS identificados: {len(files_filtrados)}")
    
    for arquivo in files_filtrados:
        rel_path = arquivo.relative_to(BASE_DIR)
        print(f"\n🔍 Front-end: {rel_path}")
        try:
            with open(arquivo, "r", encoding="utf-8", errors="ignore") as f:
                conteudo = f.read()
                
            tem_fetch = "fetch(" in conteudo or "axios." in conteudo or "$.ajax" in conteudo
            tem_ceo_name = "ceo_name" in conteudo.lower() or "nome" in conteudo.lower()
            
            print(f"   • Envia Requisição? {'SIM ✅' if tem_fetch else 'NÃO ❌'}")
            print(f"   • Contém campos de Nome? {'SIM ✅' if tem_ceo_name else 'NÃO ❌'}")
            
            linhas = conteudo.splitlines()
            for idx, linha in enumerate(linhas, 1):
                if any(k in linha.lower() for k in ["body:", "data:", "ceo_name", "gerar_dossie", "nome"]):
                    print(f"     [Linha {idx:04d}]: {linha.strip()}")
                    
        except Exception as e:
            print(f"   ❌ Erro ao ler {rel_path}: {e}")

def executar_varredura():
    print("==================================================")
    print("🚀 INICIANDO VARREDURA DOS 4 PILARES")
    print("==================================================")
    
    # 1. main.py
    auditoria_arquivo("main.py", ["gerar_dossie", "payload", "request", "nome", "CEO_NAME", "José"])
    
    # 2. HTML/JS Front-end
    auditoria_paineis_html()
    
    # 3. Gerador Master (na pasta core)
    auditoria_arquivo("gerador_dossies_master.py", ["gerar_dossie_auditoria", "nome", "cliente", "CEO_NAME", "José"])
    
    # 4. C2 Sovereign Intelligence (na pasta core)
    auditoria_arquivo("c2_sovereign_intelligence.py", ["lider", "ceo_name", "historico_clientes.json", "José"])

    print("\n==================================================")
    print("🏁 VARREDURA CONCLUÍDA COM SUCESSO")
    print("==================================================")

if __name__ == "__main__":
    executar_varredura()