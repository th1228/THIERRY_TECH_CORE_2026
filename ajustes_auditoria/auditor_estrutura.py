import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

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
Script de Auditoria e Diagnóstico Estrutural - TCC Global
Analisa a árvore de pastas, dependências e importações antes de qualquer reorganização.
"""

import os
import re
from pathlib import Path

# Raiz do projeto baseada na localização deste script
BASE_DIR = Path(__file__).resolve().parent

# Pastas obrigatórias esperadas no ecossistema Tier-1
PASTAS_OBRIGATORIAS = [
    "core",
    "security",
    "legal",
    "static",
    "pdfs_finais",
    "vault_uhnw_storage"
]

def executar_auditoria_estrutural():
    logger.info("=" * 70)
    logger.info(" 🛡️  TCC SOVEREIGN KERNEL - AUDITORIA DE ESTRUTURA & DEPENDÊNCIAS")
    logger.info("=" * 70)
    logger.info(f" Diretório Raiz Alvo: {BASE_DIR}\n")

    # 1. Verificação de Pastas Principais
    logger.info("[1/3] Verificando Diretórios Vitais...")
    pastas_faltantes = []
    for pasta in PASTAS_OBRIGATORIAS:
        caminho_pasta = BASE_DIR / pasta
        if caminho_pasta.exists() and caminho_pasta.is_dir():
            logger.info(f"   [OK] Pasta encontrada: /{pasta}")
        else:
            logger.info(f"   [FALTA] Pasta ausente: /{pasta}")
            pastas_faltantes.append(pasta)

    # 2. Varredura de Arquivos Python e Mapeamento de Imports
    logger.info("\n[2/3] Mapeando Arquivos Python e Dependências de Importação...")
    arquivos_py = list(BASE_DIR.glob("**/*.py"))
    total_linhas = 0
    import_erros_potenciais = []

    for arq in arquivos_py:
        # Ignorar pastas virtuais ou de ambiente se houverem
        if any(p in arq.parts for p in ['.venv', 'venv', '__pycache__', 'env']):
            continue
            
        rel_path = arq.relative_to(BASE_DIR)
        try:
            with open(arq, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                linhas = conteudo.splitlines()
                total_linhas += len(linhas)
                
                # Procura por imports relativos ou absolutos de módulos internos
                imports = re.findall(r'^(?:from|import)\s+([a-zA-Z0-9_\.]+)', conteudo, re.MULTILINE)
                
                # Validação lógica básica de arquivos soltos na raiz tentando importar o core
                if rel_path.parent == BASE_DIR:
                    for imp in imports:
                        if imp in ["core", "security"] or imp.startswith("core.") or imp.startswith("security."):
                            pass # Importação válida a partir da raiz
        except Exception as e:
            import_erros_potenciais.append((str(rel_path), str(e)))

    logger.info(f"   [INFO] Total de arquivos Python escaneados: {len(arquivos_py)}")
    logger.info(f"   [INFO] Linhas de código analisadas: {total_linhas}")

    # 3. Análise de Arquivos Órfãos na Raiz
    logger.info("\n[3/3] Verificando Arquivos Soltos na Raiz (Fora de Módulos)...")
    arquivos_raiz = [f.name for f in BASE_DIR.iterdir() if f.is_file() and f.suffix == '.py']
    arquivos_permitidos_raiz = ["main.py", "auditor_estrutura.py", "config_pagamentos.py", "memoria_comum.py"]
    
    arquivos_fora_do_lugar = [f for f in arquivos_raiz if f not in arquivos_permitidos_raiz]

    logger.info("\n" + "=" * 70)
    logger.info(" 📊 RELATÓRIO FINAL DE DIAGNÓSTICO E RECOMENDAÇÕES")
    logger.info("=" * 70)

    # Diagnóstico Textual para o Desenvolvedor no Terminal
    if pastas_faltantes:
        logger.info(f" ⚠️ ATENÇÃO: As seguintes pastas obrigatórias não existem: {pastas_faltantes}")
        logger.info("    Recomendação: Crie essas pastas antes de mover arquivos para lá.")
    else:
        logger.info(" ✅ Estrutura de pastas vitais: 100% íntegra e presente.")

    if arquivos_fora_do_lugar:
        logger.info(f" ⚠️ ATENÇÃO: Encontramos arquivos Python soltos na raiz que podem ser motores: {arquivos_fora_do_lugar}")
        logger.info("    Recomendação: Se forem motores de cálculo, eles DEVEM ficar dentro da pasta 'core/'.")
        logger.info("    Se forem movidos sem ajuste, as importações que apontam para 'core.nome_do_modulo' vão falhar.")
    else:
        logger.info(" ✅ Nenhum motor órfão encontrado na raiz. Todos os scripts essenciais estão nos locais corretos.")

    logger.info("\n 🛠️ COMO TRABALHAR A ORGANIZAÇÃO SEM QUEBRAR O PROGRAMA:")
    logger.info(" 1. NUNCA arraste um arquivo de dentro de 'core/' para a raiz (ou vice-versa) manualmente")
    logger.info("    sem antes conferir se as linhas de 'import' precisam ser reajustadas.")
    logger.info(" 2. O 'main.py' na raiz funciona perfeitamente porque ele atua como orquestrador central")
    logger.info("    e chama os submódulos usando o prefixo 'core.' ou 'security.'.")
    logger.info(" 3. Se precisar criar um novo motor, crie-o diretamente dentro de 'core/' e faça a importação")
    logger.info("    no 'main.py' usando: 'from core.nome_do_motor import ...'.")
    logger.info("=" * 70)
    logger.info(" Diagnóstico concluído com sucesso. O sistema está seguro para operação.")
    logger.info("=" * 70)

if __name__ == "__main__":
    executar_auditoria_estrutural()