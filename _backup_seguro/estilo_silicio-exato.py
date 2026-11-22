# -*- coding: utf-8 -*-
import re
import shutil
from pathlib import Path

HTML_PATH = Path("index.html")
BACKUP_PATH = Path("index.html.pre_silicio.bak")

def aplicar_refino_exato_silicio():
    if not HTML_PATH.exists():
        print("[ERRO] index.html não encontrado na raiz.")
        return

    # 1. Backup automático de segurança
    shutil.copy2(HTML_PATH, BACKUP_PATH)
    print(f"[INFO] Backup de segurança salvo em: {BACKUP_PATH}")

    conteudo = HTML_PATH.read_text(encoding="utf-8")

    # 2. Troca dos 3 títulos (mantendo IDs e data-i18n intactos)
    trocas_titulos = [
        ("Pilares de Arquitetura Sênior", "Pilares de Soberania Clínica"),
        ("Senior Architecture Pillars", "Clinical Sovereignty Pillars"),
        ("Métricas Dinâmicas do Motor", "Telemetria Biométrica Avançada"),
        ("Dynamic Engine Metrics", "Advanced Biometric Telemetry"),
        ("STATUS DO MOTOR GLOBAL", "STATUS DO NÚCLEO GLOBAL"),
        ("GLOBAL ENGINE STATUS", "GLOBAL CORE STATUS"),
    ]

    for antigo, novo in trocas_titulos:
        conteudo = conteudo.replace(antigo, novo)

    # 3. Compactação exata das 3 caixas de métricas e da caixa de status inferior
    # Diminui o gap entre as 3 métricas de 10px para 6px
    conteudo = conteudo.replace(
        '<div style="display: flex; flex-direction: column; gap: 10px;">\n                    <!-- Métrica 1: Integridade Tecidual -->',
        '<div style="display: flex; flex-direction: column; gap: 6px;">\n                    <!-- Métrica 1: Integridade Tecidual -->'
    )

    # Afina o padding interno das caixas de métricas (de 8px 10px para 5px 10px) e arredonda para 10px
    conteudo = conteudo.replace(
        'style="background: rgba(59, 94, 102, 0.08); border: 1px solid var(--border-sovereign); padding: 8px 10px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;"',
        'style="background: rgba(59, 94, 102, 0.08); border: 1px solid var(--border-sovereign); padding: 5px 10px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center;"'
    )

    # Afina também a caixa inferior "STATUS DO NÚCLEO GLOBAL" para manter a mesma proporção
    conteudo = conteudo.replace(
        'style="background: rgba(59, 94, 102, 0.08); border: 1px solid var(--border-sovereign); padding: 8px 10px; border-radius: 8px;">\n                    <span style="color: var(--text-secondary); display: block; font-size: 9px;">STATUS DO NÚCLEO GLOBAL</span>',
        'style="background: rgba(59, 94, 102, 0.08); border: 1px solid var(--border-sovereign); padding: 6px 10px; border-radius: 10px;">\n                    <span style="color: var(--text-secondary); display: block; font-size: 8.5px; letter-spacing: 0.4px;">STATUS DO NÚCLEO GLOBAL</span>'
    )

    # Afina levemente a fonte dos valores das métricas (de 11px para 10px) e o ponto luminoso (de 8px para 6px)
    conteudo = conteudo.replace('font-weight: 700; font-size: 11px;">99.4%', 'font-weight: 700; font-size: 10px;">99.4%')
    conteudo = conteudo.replace('font-weight: 700; font-size: 11px;">98.8%', 'font-weight: 700; font-size: 10px;">98.8%')
    conteudo = conteudo.replace('font-weight: 700; font-size: 11px;">88.5%', 'font-weight: 700; font-size: 10px;">88.5%')
    conteudo = conteudo.replace('style="width: 8px; height: 8px;', 'style="width: 6px; height: 6px;')

    # 4. Estilo Vale do Silício global (tipografia tabular e respiro suave nos cartões centrais)
    conteudo = re.sub(r'<style id="auditor-silicio-ui">.*?</style>\s*', '', conteudo, flags=re.DOTALL)
    css_silicio = """
    <style id="auditor-silicio-ui">
        body {
            -webkit-font-smoothing: antialiased !important;
            -moz-osx-font-smoothing: grayscale !important;
            font-variant-numeric: tabular-nums !important;
        }
        .luxury-sidebar {
            gap: 10px !important;
        }
        .elite-menu-btn {
            border-radius: 10px !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        .biogen-imperial-grid {
            gap: 16px !important;
            padding: 20px !important;
        }
        .grid-cell {
            border-radius: 12px !important;
            transition: transform 0.2s ease !important;
        }
    </style>
    """

    if "</head>" in conteudo:
        conteudo = conteudo.replace("</head>", f"{css_silicio}\n</head>", 1)

    HTML_PATH.write_text(conteudo, encoding="utf-8")
    print("=" * 75)
    print("[SUCESSO] Títulos executivos e compactação estilo Vale do Silício aplicados!")
    print("=" * 75)

if __name__ == "__main__":
    aplicar_refino_exato_silicio()