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
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - AUDITOR DE CONTEÚDO E PROFUNDIDADE
===========================================================================
Módulo: auditor_conteudo_profundidade.py
Descrição: Varredura analítica de densidade textual, contagem de palavras,
           volume de blocos e validação de riqueza semântica nos PDFs finais.
"""

import os
import pymupdf as fitz

class AuditorConteudoProfundidade:
    def __init__(self, raiz_projeto: str):
        self.raiz = raiz_projeto
        self.limiar_minimo_palavras = 350  # Mínimo exigido por dossiê para densidade UHNW

    def executar_auditoria(self) -> None:
        logger.info("=" * 70)
        logger.info(" INICIANDO AUDITORIA DE CONTEÚDO, TAMANHO E PROFUNDIDADE DOS PDFS")
        logger.info("=" * 70)

        pasta_pdfs = os.path.join(self.raiz, "pdfs_finais")
        if not os.path.exists(pasta_pdfs):
            logger.info(" [ERRO] Pasta 'pdfs_finais' não encontrada. Execute o gerador mestre primeiro.")
            return

        pdfs = [os.path.join(pasta_pdfs, f) for f in os.listdir(pasta_pdfs) if f.lower().endswith(".pdf")]
        if not pdfs:
            logger.info(" [ERRO] Nenhum PDF encontrado na pasta 'pdfs_finais'.")
            return

        total_geral_palavras = 0
        aprovados_conteudo = 0

        for caminho_pdf in sorted(pdfs):
            nome = os.path.basename(caminho_pdf)
            try:
                doc = fitz.open(caminho_pdf)
                total_paginas = len(doc)
                texto_acumulado = []

                for pagina in doc:
                    txt = pagina.get_text("text")
                    if txt:
                        texto_acumulado.append(str(txt))
                
                doc.close()

                texto_completo = " ".join(texto_acumulado)
                palavras = texto_completo.split()
                qtd_palavras = len(palavras)
                total_geral_palavras += qtd_palavras

                status_densidade = "ATENÇÃO (CONTEÚDO ENXUTO)"
                if qtd_palavras >= self.limiar_minimo_palavras:
                    status_densidade = "APROVADO (ROBUSTO E DENSO)"
                    aprovados_conteudo += 1

                logger.info(f"\n 📄 Documento: {nome}")
                logger.info(f"    ├─ Total de Páginas: {total_paginas}")
                logger.info(f"    ├─ Contagem de Palavras: {qtd_palavras} palavras")
                logger.info(f"    └─ Veredito de Densidade: [{status_densidade}]")

            except Exception as e:
                logger.info(f" ❌ Erro ao analisar '{nome}': {e}")

        logger.info("\n" + "=" * 70)
        logger.info(" RESUMO DA ANÁLISE DE PROFUNDIDADE SEMÂNTICA")
        logger.info(f" • Total de Documentos Analisados: {len(pdfs)}")
        logger.info(f" • Volume Textual Consolidado: {total_geral_palavras} palavras")
        logger.info(f" • Documentos com Densidade Adequada: {aprovados_conteudo}/{len(pdfs)}")
        logger.info("=" * 70)
        
        if aprovados_conteudo == len(pdfs):
            logger.info(" STATUS FINAL: [ CONTEÚDO À ALTURA DO PADRÃO INTERNACIONAL ]")
            logger.info(" Os relatórios possuem profundidade e volume textuais excelentes.")
        else:
            logger.info(" STATUS FINAL: [ ALGUNS DOCUMENTOS EXIGEM MAIS DETALHAMENTO ]")
            logger.info(" Recomendado expandir as diretrizes dos motores nos itens enxutos.")
        logger.info("=" * 70 + "\n")

if __name__ == "__main__":
    raiz = os.getcwd()
    auditor = AuditorConteudoProfundidade(raiz)
    auditor.executar_auditoria()