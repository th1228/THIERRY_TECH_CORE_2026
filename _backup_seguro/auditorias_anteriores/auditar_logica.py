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
from pathlib import Path

def auditar_projeto():
    raiz = Path.cwd()
    print("=" * 65)
    print("       DIAGNÓSTICO E AUDITORIA DE INTEGRAÇÃO - TCC GLOBAL")
    print("=" * 65)
    print(f"Diretório atual de varredura: {raiz}\n")

    # 1. Verificação de Arquivos Críticos
    print("[1] Verificação de Arquivos Críticos na Raiz:")
    
    # Procura por arquivos HTML dinamicamente se o nome exato variar
    arquivos_html = list(raiz.glob("*.html"))
    tem_html = len(arquivos_html) > 0
    
    main_path = raiz / "main.py"
    tem_main = main_path.exists()

    print(f"  - main.py (Orquestrador): {'✅ ENCONTRADO' if tem_main else '❌ AUSENTE'}")
    if tem_html:
        nomes_html = [h.name for h in arquivos_html]
        print(f"  - Painel(is) HTML encontrado(s): ✅ ENCONTRADO ({', '.join(nomes_html)})")
    else:
        print("  - Painel HTML: ❌ NENHUM ARQUIVO .HTML ENCONTRADO NA RAIZ")

    # 2. Verificação de Pastas de Relatórios
    print("\n[2] Verificação de Diretórios de Saída (Relatórios):")
    pastas_alvo = ["relatorios_gerados", "relatorios", "output"]
    pasta_encontrada = False
    for p in pastas_alvo:
        cp = raiz / p
        if cp.exists() and cp.is_dir():
            print(f"  - Pasta '{p}/': ✅ EXISTE")
            pasta_encontrada = True
    if not pasta_encontrada:
        print("  - ⚠️ Nenhuma pasta padrão de relatórios ('relatorios_gerados') encontrada (o main.py precisará criá-la dinamicamente).")

    # 3. Análise de Código do main.py
    print("\n[3] Análise de Rotas e Integração no 'main.py':")
    if tem_main:
        try:
            conteudo_main = main_path.read_text(encoding="utf-8", errors="ignore")
            
            tem_fastapi = "fastapi" in conteudo_main.lower()
            tem_html_response = "htmlresponse" in conteudo_main.lower() or "fileresponse" in conteudo_main.lower()
            tem_rota_pdf = "/api/pdf" in conteudo_main or "api/pdf" in conteudo_main
            tem_cors = "cors" in conteudo_main.lower()

            print(f"  - Framework FastAPI/Servidor ativo: {'✅ Sim' if tem_fastapi else '❌ Não detectado'}")
            print(f"  - Servir arquivos/HTML configurado: {'✅ Sim' if tem_html_response else '❌ Pendente'}")
            print(f"  - Rota de API para PDF (/api/pdf/...): {'✅ Configurada' if tem_rota_pdf else '❌ Faltando no main.py'}")
            print(f"  - Middleware CORS ativado: {'✅ Sim' if tem_cors else '⚠️ Não (Pode bloquear requisições do front)'}")
        except Exception as e:
            print(f"  - ❌ Erro ao ler o conteúdo do main.py: {e}")
    else:
        print("  - ❌ Impossível analisar o main.py porque o arquivo não existe.")

    # 4. Conclusão e Próximos Passos
    print("\n" + "=" * 65)
    print("   DIAGNÓSTICO FINAL: O QUE FALTA PARA CONECTAR?")
    print("=" * 65)
    
    pendencias = []
    if not tem_main:
        pendencias.append("Criar ou posicionar o arquivo 'main.py' na raiz.")
    if not tem_html:
        pendencias.append("Colocar o arquivo do painel HTML na mesma pasta do 'main.py'.")
    if tem_main and not "api/pdf" in main_path.read_text(encoding="utf-8", errors="ignore"):
        pendencias.append("Adicionar a rota POST '/api/pdf/{tipo}' no 'main.py' para aceitar os relatórios.")

    if pendencias:
        for idx, pend in enumerate(pendencias, 1):
            print(f"  {idx}. {pend}")
    else:
        print("  ✅ Estrutura básica alinhada! O programa está pronto para subir.")
        print("  Execute no terminal: python main.py")
        print("  Acesse no navegador: http://localhost:8000")
    print("=" * 65)

if __name__ == "__main__":
    auditar_projeto()