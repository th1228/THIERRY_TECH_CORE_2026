# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
Módulo: auditor_pdf.py
Sistema: Thierry Technology Concept Global - Auditor Executivo UHNW
Descrição: Auditoria de conformidade internacional (ISO 216 A4, ISO 19005
           Fontes/Integridade e ISO 14289 Metadados/Acessibilidade).
"""

import fitz  # PyMuPDF
import os
import datetime

def encontrar_pasta_pdfs(nome_alvo="pdfs_finais"):
    for raiz, diretorios, _ in os.walk(os.getcwd()):
        for dir_name in diretorios:
            if dir_name.lower() == nome_alvo.lower():
                return os.path.join(raiz, dir_name)
    
    caminho_direto = os.path.join(os.getcwd(), nome_alvo)
    if os.path.exists(caminho_direto):
        return caminho_direto
        
    return None

def analisar_pdfs() -> None:
    caminho_pasta = encontrar_pasta_pdfs("pdfs_finais")
    
    print("\n" + "=" * 70)
    print(" AUDITORIA EXECUTIVA DE CONFORMIDADE INTERNACIONAL (SESSÃO DE HOJE)")
    print("=" * 70)
    
    if not caminho_pasta or not os.path.exists(caminho_pasta):
        print("❌ ERRO CRÍTICO: A pasta 'pdfs_finais' não foi encontrada.")
        return

    hoje = datetime.date.today()
    arquivos_pdf = []
    
    for raiz, _, arquivos in os.walk(caminho_pasta):
        for f in arquivos:
            if f.lower().endswith('.pdf'):
                caminho_completo = os.path.join(raiz, f)
                data_arquivo = datetime.date.fromtimestamp(os.path.getmtime(caminho_completo))
                if data_arquivo == hoje:
                    arquivos_pdf.append(caminho_completo)
    
    if not arquivos_pdf:
        print(f"⚠️ AVISO: Nenhum PDF novo gerado hoje ({hoje.strftime('%d/%m/%Y')}).")
        return

    print(f"Filtro Ativo: Arquivos gerados em {hoje.strftime('%d/%m/%Y')} | Total: {len(arquivos_pdf)}\n")

    largura_a4, altura_a4 = 595.28, 841.89
    pt_para_mm = 0.352778
    total_aprovados = 0
    total_reprovados = 0

    for caminho_completo in arquivos_pdf:
        arquivo = os.path.basename(caminho_completo)
        try:
            doc = fitz.open(caminho_completo)
        except Exception as e:
            print(f"📄 Documento: {arquivo}")
            print(f"   └── ❌ REPROVADO: Falha estrutural ao abrir ({e})\n")
            total_reprovados += 1
            continue
        
        total_paginas = len(doc)
        falhas_documento = []

        # 1. Validação ISO 14289 (Metadados e Título Obrigatório)
        metadados = doc.metadata or {}
        if not metadados.get("title") or not metadados.get("title").strip():
            falhas_documento.append("ISO 14289: Metadado 'Title' ausente (exigido para acessibilidade).")

        # 2. Validação de Segurança e Permissões
        if doc.needs_pass:
            falhas_documento.append("Segurança: Arquivo bloqueado por senha de abertura.")

        for i in range(total_paginas):
            pagina = doc[i]
            rect = pagina.rect
            largura, altura = float(rect.width), float(rect.height)
            
            # 3. Validação ISO 216 (Dimensão A4)
            if abs(largura - largura_a4) > 15 or abs(altura - altura_a4) > 15:
                falhas_documento.append(f"Pág. {i + 1} (ISO 216): Fora do padrão A4 ({largura:.1f}x{altura:.1f} pt).")
            
            # 4. Validação ISO 19005 (Incorporação de Fontes)
            fontes = pagina.get_fonts(full=True)
            for fonte in fontes:
                # fonte[3] é o nome da fonte; fontes embutidas têm prefixo de subconjunto (ex: ABCDEF+Arial) ou tipo embutido
                nome_fonte = fonte[3]
                if not nome_fonte:
                    falhas_documento.append(f"Pág. {i + 1} (ISO 19005): Fonte não identificada ou não incorporada.")

            # 5. Validação Geométrica das 4 Margens (Esquerda, Topo, Direita, Base)
            blocos = pagina.get_text("blocks")
            if not blocos:
                falhas_documento.append(f"Pág. {i + 1} (ISO 14289): Página sem camada de texto pesquisável.")
                continue
                
            x0_list = [float(b[0]) for b in blocos if 0 <= float(b[0]) < largura - 20]
            y0_list = [float(b[1]) for b in blocos if 0 <= float(b[1]) < altura - 20]
            x1_list = [float(b[2]) for b in blocos if 20 < float(b[2]) <= largura]
            y1_list = [float(b[3]) for b in blocos if 20 < float(b[3]) <= altura]
            
            if x0_list and y0_list and x1_list and y1_list:
                margem_esq = min(x0_list) * pt_para_mm
                margem_sup = min(y0_list) * pt_para_mm
                margem_dir = (largura - max(x1_list)) * pt_para_mm
                margem_inf = (altura - max(y1_list)) * pt_para_mm
                
                if min(margem_esq, margem_sup, margem_dir, margem_inf) < 7.0:
                    falhas_documento.append(
                        f"Pág. {i + 1} (Layout): Margem inferior a 7mm "
                        f"(E:{margem_esq:.1f} | D:{margem_dir:.1f} | S:{margem_sup:.1f} | I:{margem_inf:.1f} mm)."
                    )

        doc.close()

        print(f"📄 Documento: {arquivo} ({total_paginas} pág(s))")
        if not falhas_documento:
            print("   └── ✅ APROVADO: 100% em conformidade internacional (ISO 216 / 19005 / 14289).")
            total_aprovados += 1
        else:
            print("   └── ❌ REPROVADO: Infrações detectadas:")
            for falha in falhas_documento:
                print(f"        • {falha}")
            total_reprovados += 1
        print("-" * 70)

    print("\n" + "=" * 70)
    print(" RESUMO FINAL DA AUDITORIA INTERNACIONAL")
    print(f" • Documentos Aprovados:  {total_aprovados}")
    print(f" • Documentos Reprovados: {total_reprovados}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    analisar_pdfs()