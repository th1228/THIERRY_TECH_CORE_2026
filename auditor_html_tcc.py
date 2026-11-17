# -*- coding: utf-8 -*-
import re
import shutil
from pathlib import Path

HTML_PATH = Path("index.html")
BACKUP_PATH = Path("index.html.bak")

def auditor_master_tcc():
    if not HTML_PATH.exists():
        print("[ERRO] index.html não encontrado no diretório.")
        return

    # 1. Backup de segurança automático antes de qualquer alteração
    shutil.copy2(HTML_PATH, BACKUP_PATH)
    print(f"[INFO] Backup de segurança criado em: {BACKUP_PATH}")

    conteudo = HTML_PATH.read_text(encoding="utf-8")

    # 2. Remoção definitiva do termo "ROI" e aplicação dos nomes oficiais escolhidos (PT e EN)
    trocas_nomenclatura = [
        # Botão 1: Autoliderança & Comando Soberano
        ("Autoliderança & Comando Global", "Autoliderança & Comando Soberano"),
        ("Self-Leadership & Global Command", "Self-Leadership & Sovereign Command"),

        # Botão 2: Clínica & Rejuvenescimento Facial (Removendo ROI)
        ("Clínica (Estética / ROI)", "Clínica & Rejuvenescimento Facial"),
        ("Clinic (Aesthetics / ROI)", "Clinical & Facial Rejuvenation"),

        # Botão 3: Visagismo & Tricologia Ultra Avançada
        ("Visagismo & Tricologia Avançada", "Visagismo & Tricologia Ultra Avançada"),
        ("Advanced Visagism & Trichology", "Ultra-Advanced Visagism & Trichology"),

        # Títulos de Soberania Clínica e Telemetria (sem "Sênior" ou "Motor")
        ("Pilares de Arquitetura Sênior", "Pilares de Soberania Clínica"),
        ("Senior Architecture Pillars", "Clinical Sovereignty Pillars"),
        ("Métricas Dinâmicas do Motor", "Telemetria Biométrica Avançada"),
        ("Métricas de Postura de Comando", "Telemetria Biométrica Avançada"),
        ("Dynamic Engine Metrics", "Advanced Biometric Telemetry"),
        ("Command Posture Metrics", "Advanced Biometric Telemetry"),
        ("REGENERATIVE & STRUCTURAL", "GLOBAL CLINICAL COMPLIANCE"),
        ("Regenerative & Structural", "Global Clinical Compliance"),

        # Barra de status inferior
        ("STATUS DO MOTOR GLOBAL", "STATUS DO NÚCLEO GLOBAL"),
        ("GLOBAL ENGINE STATUS", "GLOBAL CORE STATUS"),

        # Padronização de licenciamento executivo global
        ("sob o Padrão Mônaco.", "sob o Padrão Global."),
        ("COMPRAR LICENÇA STRIPE", "ATIVAR LICENÇA EXECUTIVA"),
        ("Comprar Licença Stripe", "Ativar Licença Executiva"),
        ("MÔNACO TIER-1", "GLOBAL TIER-1"),
        ("Purchase Stripe License", "Activate Executive License"),
        ("PURCHASE STRIPE LICENSE", "ACTIVATE EXECUTIVE LICENSE"),
        ("Monaco Standards.", "Global Executive Standards."),
        ("MONACO TIER-1", "GLOBAL TIER-1"),
        ("Monaco Supremacy License", "European Executive License"),
        ("Europa & Mônaco.", "Europa & Global."),
        ("ADQUIRIR MÔNACO (EUR)", "ADQUIRIR LICENÇA EUROPA (EUR)"),
        ("BYPASS STRIPE ATIVO", "BYPASS LICENCIAMENTO ATIVO"),
    ]

    alteracoes = 0
    for antigo, novo in trocas_nomenclatura:
        if antigo in conteudo:
            conteudo = conteudo.replace(antigo, novo)
            alteracoes += 1
            print(f"[OK] Atualizado: '{antigo}' -> '{novo}'")

    # 3. Compactação elegante das 3 métricas laterais e status inferior (Estilo Vale do Silício)
    conteudo = conteudo.replace(
        '<div style="display: flex; flex-direction: column; gap: 10px;">\n                    <!-- Métrica 1: Integridade Tecidual -->',
        '<div style="display: flex; flex-direction: column; gap: 6px;">\n                    <!-- Métrica 1: Integridade Tecidual -->'
    )
    conteudo = conteudo.replace(
        'style="background: rgba(59, 94, 102, 0.08); border: 1px solid var(--border-sovereign); padding: 8px 10px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;"',
        'style="background: rgba(59, 94, 102, 0.08); border: 1px solid var(--border-sovereign); padding: 5px 10px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center;"'
    )
    conteudo = conteudo.replace(
        'style="background: rgba(59, 94, 102, 0.08); border: 1px solid var(--border-sovereign); padding: 8px 10px; border-radius: 8px;">\n                    <span style="color: var(--text-secondary); display: block; font-size: 9px;">STATUS DO NÚCLEO GLOBAL</span>',
        'style="background: rgba(59, 94, 102, 0.08); border: 1px solid var(--border-sovereign); padding: 6px 10px; border-radius: 10px;">\n                    <span style="color: var(--text-secondary); display: block; font-size: 8.5px; letter-spacing: 0.4px;">STATUS DO NÚCLEO GLOBAL</span>'
    )
    conteudo = conteudo.replace('font-weight: 700; font-size: 11px;">99.4%', 'font-weight: 700; font-size: 10px;">99.4%')
    conteudo = conteudo.replace('font-weight: 700; font-size: 11px;">98.8%', 'font-weight: 700; font-size: 10px;">98.8%')
    conteudo = conteudo.replace('font-weight: 700; font-size: 11px;">88.5%', 'font-weight: 700; font-size: 10px;">88.5%')
    conteudo = conteudo.replace('style="width: 8px; height: 8px;', 'style="width: 6px; height: 6px;')

    # 4. Injeção limpa de respiro, micro-tipografia e contraste WCAG
    conteudo = re.sub(r'<style id="auditor-tcc-styles">.*?</style>\s*', '', conteudo, flags=re.DOTALL)
    conteudo = re.sub(r'<style id="auditor-silicio-ui">.*?</style>\s*', '', conteudo, flags=re.DOTALL)
    conteudo = re.sub(r'<style id="auditor-refino-metricas">.*?</style>\s*', '', conteudo, flags=re.DOTALL)

    css_unificado = """
    <style id="auditor-tcc-styles">
        /* ORGANIZAÇÃO VALE DO SILÍCIO, RESPIRO E PROTEÇÃO DE CONTRASTE */
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
            padding: 14px !important;
            border-width: 1px !important;
            border-radius: 12px !important;
            transition: transform 0.2s ease !important;
        }
        body.light-theme,
        body.light-mode,
        html[data-theme="light"] body {
            background-color: #f8fafc !important;
            color: #0f172a !important;
            --card-final-bg: #ffffff !important;
            --text-biogen-title: #0f172a !important;
            --text-biogen-metadata: #047857 !important;
        }
        body.light-theme :is(h1, h2, h3, h4, p, span, label, small, div, td, th),
        body.light-mode :is(h1, h2, h3, h4, p, span, label, small, div, td, th),
        html[data-theme="light"] :is(h1, h2, h3, h4, p, span, label, small, div, td, th) {
            color: #0f172a !important;
        }
        body.light-theme .metadata,
        body.light-mode .metadata,
        html[data-theme="light"] .metadata {
            color: #047857 !important;
        }
    </style>
    """

    if "</head>" in conteudo:
        conteudo = conteudo.replace("</head>", f"{css_unificado}\n</head>", 1)

    HTML_PATH.write_text(conteudo, encoding="utf-8")
    print("=" * 75)
    print(f"[SUCESSO] Auditoria finalizada com os nomes oficiais ({alteracoes} blocos atualizados)!")
    print("=" * 75)

if __name__ == "__main__":
    auditor_master_tcc()