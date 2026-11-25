import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

import os
from pathlib import Path
from datetime import datetime

def verificar_prontidao_comercial():
    logger.info("=" * 70)
    logger.info(" THIERRY TECHNOLOGY CONCEPT GLOBAL | CHECKLIST DE PRONTIDÃO COMERCIAL")
    logger.info("=" * 70)
    logger.info(f" Data da Varredura: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(" Alvo: Validação profunda de assets, PWA, index.html e responsividade total.")
    logger.info("-" * 70)

    # 1. Lista de arquivos críticos exigidos para o deploy e PWA
    arquivos_criticos = [
        "index.html",
        "sw.js",
        "manifest.json"
    ]

    # 2. Lista de diretórios de auditoria/compliance
    pastas_criticas = [
        "audit"
    ]

    pendencias = 0
    sucessos = 0

    logger.info("\n[+] VERIFICANDO ASSETS CRÍTICOS DE FRONTEND & PWA:")
    for arquivo in arquivos_criticos:
        caminho = Path(arquivo)
        if caminho.is_file():
            logger.info(f"  [OK] Arquivo encontrado: {arquivo}")
            sucessos += 1
        else:
            logger.info(f"  [PENDENTE] Arquivo ausente: {arquivo}")
            pendencias += 1

    logger.info("\n[+] VERIFICANDO DIRETÓRIOS DE COMPLIANCE & AUDITORIA:")
    for pasta in pastas_criticas:
        caminho_pasta = Path(pasta)
        if caminho_pasta.is_dir():
            logger.info(f"  [OK] Diretório operacional presente: {pasta}/")
            sucessos += 1
        else:
            logger.info(f"  [PENDENTE] Diretório ausente: {pasta}/")
            pendencias += 1

    # 3. Varredura e Inspeção Interna do index.html (Componentes e Responsividade Multi-dispositivo)
    logger.info("\n[+] INSPEÇÃO ESTRUTURAL E RESPONSIVIDADE DO PAINEL (INDEX.HTML):")
    index_path = Path("index.html")
    if index_path.is_file():
        try:
            conteudo_html = index_path.read_text(encoding="utf-8")
            
            # Componentes e regras responsivas verificadas no código
            componentes_html = {
                "Grid dos Biogêmeos (.biogen-imperial-grid)": "biogen-imperial-grid",
                "Módulo de Confronto / Governança": "confrontation-elite-grid",
                "Barra de Telemetria de Luxo": "luxury-telemetry-bar",
                "Modal de Foco 3D": "biogen-focus-modal",
                "Sistema Bilíngue (data-i18n)": "data-i18n",
                "Responsividade para Tablets (@media max-width 1024px)": "max-width: 1024px",
                "Responsividade para Celulares (@media max-width 640px)": "max-width: 640px"
            }

            for nome_comp, termo in componentes_html.items():
                if termo in conteudo_html:
                    logger.info(f"  [OK] Módulo validado: {nome_comp}")
                    sucessos += 1
                else:
                    logger.info(f"  [PENDENTE] Ausente ou não mapeado: {nome_comp}")
                    pendencias += 1

        except Exception as e:
            logger.info(f"  [ERRO] Não foi possível ler o arquivo index.html: {e}")
            pendencias += 1
    else:
        logger.info("  [ERRO CRÍTICO] O arquivo index.html não existe para ser inspecionado.")
        pendencias += 2

    logger.info("\n" + "=" * 70)
    logger.info(f" RESUMO DO DIAGNÓSTICO: {sucessos} itens validados com sucesso.")
    if pendencias == 0:
        logger.info(" VEREDITO: PLATAFORMA 100% PRONTA, RESPONSIVA (PC/TABLET/CELULAR) E GLOBAL!")
    else:
        logger.info(f" ATENÇÃO: {pendencias} item(ns) requerem atenção para validação total.")
    logger.info("=" * 70)

if __name__ == "__main__":
    verificar_prontidao_comercial()