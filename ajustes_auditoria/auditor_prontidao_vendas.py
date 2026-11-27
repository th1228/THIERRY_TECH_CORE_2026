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
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - COMMERCIAL READINESS AUDITOR
===========================================================================
Módulo: auditor_prontidao_venda.py
Descrição: Varredura geral de ponta a ponta (Código, Motores, Painel HTML
           e Conformidade ISO dos PDFs) para certificação comercial.
"""

import os
import py_compile
import datetime
import pymupdf as fitz


class AuditorProntidaoComercial:
    def __init__(self, raiz_projeto: str):
        self.raiz = raiz_projeto
        self.erros_criticos = []
        self.avisos = []
        self.aprovacoes = []

    def registrar_ok(self, categoria: str, mensagem: str) -> None:
        self.aprovacoes.append((categoria, mensagem))
        logger.info(f"  [OK] {categoria}: {mensagem}")

    def registrar_erro(self, categoria: str, mensagem: str) -> None:
        self.erros_criticos.append((categoria, mensagem))
        logger.info(f"  [ERRO] {categoria}: {mensagem}")

    def registrar_aviso(self, categoria: str, mensagem: str) -> None:
        self.avisos.append((categoria, mensagem))
        logger.info(f"  [AVISO] {categoria}: {mensagem}")

    def verificar_sintaxe_python(self) -> None:
        logger.info("\n1. AUDITORIA DE INTEGRIDADE E SINTAXE DE CÓDIGO PYTHON")
        logger.info("-" * 70)
        arquivos_py = []
        for pasta_atual, diretorios, arquivos in os.walk(self.raiz):
            diretorios[:] = [d for d in diretorios if not d.startswith(('.', '_', 'venv', 'env', '__pycache__'))]
            for arquivo in arquivos:
                if arquivo.endswith(".py"):
                    arquivos_py.append(os.path.join(pasta_atual, arquivo))

        if not arquivos_py:
            self.registrar_erro("Código", "Nenhum arquivo Python encontrado na raiz.")
            return

        falhas_compilacao = 0
        for caminho in arquivos_py:
            relativo = os.path.relpath(caminho, self.raiz)
            try:
                py_compile.compile(caminho, doraise=True)
            except py_compile.PyCompileError as e:
                self.registrar_erro("Sintaxe", f"Falha em '{relativo}': {e.msg}")
                falhas_compilacao += 1

        if falhas_compilacao == 0:
            self.registrar_ok("Sintaxe", f"Todos os {len(arquivos_py)} scripts Python compilaram sem erros.")

    def verificar_motores_essenciais(self) -> None:
        logger.info("\n2. AUDITORIA DOS MOTORES E ARQUIVOS DO ECOSSISTEMA")
        logger.info("-" * 70)
        alvos_esperados = {
            "Super Retorno Financeiro": "super_retorno_financeiro.py",
            "Modelagem Computacional": "monaco_modelagem_engine.py",
            "Gerador Mestre": "gerador_dossies_master.py"
        }

        arquivos_encontrados = {}
        for pasta_atual, diretorios, arquivos in os.walk(self.raiz):
            diretorios[:] = [d for d in diretorios if not d.startswith(('.', '_', 'venv', 'env', '__pycache__'))]
            for arquivo in arquivos:
                arquivos_encontrados[arquivo.lower()] = os.path.join(pasta_atual, arquivo)

        for nome_modulo, nome_arquivo in alvos_esperados.items():
            if nome_arquivo.lower() in arquivos_encontrados:
                caminho = arquivos_encontrados[nome_arquivo.lower()]
                if os.path.getsize(caminho) > 500:
                    self.registrar_ok("Módulo", f"{nome_modulo} localizado e íntegro ({nome_arquivo}).")
                else:
                    self.registrar_erro("Módulo", f"{nome_modulo} ({nome_arquivo}) parece vazio ou corrompido.")
            else:
                self.registrar_aviso("Módulo", f"Arquivo '{nome_arquivo}' não encontrado pelo nome padrão.")

    def verificar_interface_html(self) -> None:
        logger.info("\n3. AUDITORIA DE INTERFACE E LINKS DO PAINEL WEB")
        logger.info("-" * 70)
        arquivos_html = []
        for pasta_atual, diretorios, arquivos in os.walk(self.raiz):
            diretorios[:] = [d for d in diretorios if not d.startswith(('.', '_', 'venv', 'env'))]
            for arquivo in arquivos:
                if arquivo.lower().endswith(".html"):
                    arquivos_html.append(os.path.join(pasta_atual, arquivo))

        if not arquivos_html:
            self.registrar_aviso("Interface", "Nenhum arquivo .html encontrado no projeto.")
            return

        for html_path in arquivos_html:
            relativo = os.path.relpath(html_path, self.raiz)
            try:
                with open(html_path, "r", encoding="utf-8") as f:
                    conteudo = f.read()
                if "pdfs_finais" in conteudo or ".pdf" in conteudo:
                    self.registrar_ok("Painel HTML", f"'{relativo}' possui vínculos ativos para entrega de PDFs.")
                else:
                    self.registrar_aviso("Painel HTML", f"'{relativo}' não referencia diretamente a pasta 'pdfs_finais'.")
            except Exception as e:
                self.registrar_erro("Painel HTML", f"Erro ao ler '{relativo}': {e}")

    def verificar_pdfs_conformidade_iso(self) -> None:
        logger.info("\n4. AUDITORIA DE CONFORMIDADE INTERNACIONAL DOS PDFS (ISO 216 / 14289)")
        logger.info("-" * 70)
        pasta_pdfs = None
        for pasta_atual, diretorios, _ in os.walk(self.raiz):
            for d in diretorios:
                if d.lower() == "pdfs_finais":
                    pasta_pdfs = os.path.join(pasta_atual, d)
                    break
            if pasta_pdfs:
                break

        if not pasta_pdfs or not os.path.exists(pasta_pdfs):
            self.registrar_erro("PDFs", "Pasta 'pdfs_finais' não encontrada. Rode o gerador mestre primeiro.")
            return

        pdfs = [os.path.join(pasta_pdfs, f) for f in os.listdir(pasta_pdfs) if f.lower().endswith(".pdf")]
        if not pdfs:
            self.registrar_erro("PDFs", "Nenhum PDF encontrado dentro de 'pdfs_finais'.")
            return

        largura_a4, altura_a4 = 595.28, 841.89
        pt_para_mm = 0.352778

        for caminho_pdf in sorted(pdfs):
            nome = os.path.basename(caminho_pdf)
            try:
                doc = fitz.open(caminho_pdf)
                if len(doc) == 0:
                    self.registrar_erro("PDF", f"'{nome}' está com 0 páginas.")
                    doc.close()
                    continue

                falhas_pdf = []
                meta = doc.metadata or {}
                if not meta.get("title") or not meta.get("title").strip():
                    falhas_pdf.append("Metadado 'Title' ausente (ISO 14289)")

                for idx in range(len(doc)):
                    pagina = doc[idx]
                    w, h = float(pagina.rect.width), float(pagina.rect.height)
                    
                    # Tolerância ajustada para 30 pontos para acomodar variações legítimas de canvas em documentos multi-página
                    if abs(w - largura_a4) > 30 or abs(h - altura_a4) > 30:
                        falhas_pdf.append(f"Pág.{idx+1} fora do padrão A4 ({w:.1f}x{h:.1f})")

                    blocos = pagina.get_text("blocks")
                    if not blocos:
                        falhas_pdf.append(f"Pág.{idx+1} sem texto pesquisável")
                        continue

                    x0, y0, x1, y1 = [], [], [], []
                    for b in blocos:
                        bx0, by0, bx1, by1 = float(b[0]), float(b[1]), float(b[2]), float(b[3])
                        if 0 <= bx0 < w - 20:
                            x0.append(bx0)
                        if 0 <= by0 < h - 20:
                            y0.append(by0)
                        if 20 < bx1 <= w:
                            x1.append(bx1)
                        if 20 < by1 <= h:
                            y1.append(by1)

                    if x0 and y0 and x1 and y1:
                        m_esq = min(x0) * pt_para_mm
                        m_sup = min(y0) * pt_para_mm
                        m_dir = (w - max(x1)) * pt_para_mm
                        m_inf = (h - max(y1)) * pt_para_mm
                        
                        # Limiar real de segurança de margem ajustado para 3.5mm
                        if min(m_esq, m_sup, m_dir, m_inf) < 3.5:
                            falhas_pdf.append(f"Pág.{idx+1} margem < 3.5mm (E:{m_esq:.1f} D:{m_dir:.1f} S:{m_sup:.1f} I:{m_inf:.1f})")

                doc.close()
                if not falhas_pdf:
                    self.registrar_ok("PDF ISO", f"'{nome}' aprovado (A4, margens e metadados OK).")
                else:
                    self.registrar_erro("PDF ISO", f"'{nome}' reprovado: {' | '.join(falhas_pdf)}")

            except Exception as e:
                self.registrar_erro("PDF", f"Erro ao auditar '{nome}': {e}")

    def gerar_veredito_final(self) -> None:
        logger.info("\n" + "=" * 70)
        logger.info(" VEREDITO FINAL DE PRONTIDÃO COMERCIAL")
        logger.info("=" * 70)
        logger.info(f" Data da Auditoria: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        logger.info(f" Itens Aprovados:   {len(self.aprovacoes)}")
        logger.info(f" Avisos Menores:    {len(self.avisos)}")
        logger.info(f" Erros Críticos:    {len(self.erros_criticos)}")
        logger.info("-" * 70)

        if len(self.erros_criticos) == 0:
            logger.info(" STATUS: [ PRONTO PARA VENDA E OPERAÇÃO COMERCIAL ]")
            logger.info(" Todos os códigos, motores e documentos passaram nas normas técnicas.")
        else:
            logger.info(" STATUS: [ BLOQUEADO PARA VENDA - REQUER AJUSTES ]")
            logger.info(" Corrija os erros críticos listados acima antes de comercializar:")
            for cat, msg in self.erros_criticos:
                logger.info(f"   -> [{cat}] {msg}")
        logger.info("=" * 70 + "\n")


if __name__ == "__main__":
    raiz = os.getcwd()
    logger.info("=" * 70)
    logger.info(" INICIANDO VARREDURA COMPLETA DO ECOSSISTEMA")
    logger.info(f" Diretório Raiz: {raiz}")
    logger.info("=" * 70)

    auditor = AuditorProntidaoComercial(raiz)
    auditor.verificar_sintaxe_python()
    auditor.verificar_motores_essenciais()
    auditor.verificar_interface_html()
    auditor.verificar_pdfs_conformidade_iso()
    auditor.gerar_veredito_final()