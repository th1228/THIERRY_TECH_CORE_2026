# -*- coding: utf-8 -*-
import re
import shutil
from pathlib import Path

HTML_PATH = Path("index.html")
BACKUP_PATH = Path("index.html.pre_refino.bak")

def aplicar_refinamento_executivo():
    if not HTML_PATH.exists():
        print("[ERRO] index.html não encontrado na raiz.")
        return

    # 1. Backup automático de segurança
    shutil.copy2(HTML_PATH, BACKUP_PATH)
    print(f"[INFO] Backup salvo em: {BACKUP_PATH}")

    conteudo = HTML_PATH.read_text(encoding="utf-8")

    # 2. Troca APENAS os textos visíveis (Português e Inglês)
    trocas_nomenclatura = [
        # Títulos principais
        ("Pilares de Arquitetura Sênior", "Pilares de Soberania Clínica"),
        ("Senior Architecture Pillars", "Clinical Sovereignty Pillars"),

        # Subtítulo de métricas (removendo "Motor")
        ("Métricas Dinâmicas do Motor", "Telemetria Biométrica Avançada"),
        ("Dynamic Engine Metrics", "Advanced Biometric Telemetry"),

        # Rótulo da barra de status inferior (removendo "Motor")
        ("STATUS DO MOTOR GLOBAL", "STATUS DO NÚCLEO GLOBAL"),
        ("Status do Motor Global", "Status do Núcleo Global"),
        ("GLOBAL ENGINE STATUS", "GLOBAL CORE STATUS"),
    ]

    trocas_feitas = 0
    for antigo, novo in trocas_nomenclatura:
        if antigo in conteudo:
            conteudo = conteudo.replace(antigo, novo)
            trocas_feitas += 1
            print(f"[OK] Nomenclatura atualizada: '{antigo}' -> '{novo}'")

    # 3. Afina levemente os cartões de métricas (Integridade, Colágeno, Valor Hídrico) sem quebrar o grid
    css_refino_metricas = """
    <style id="auditor-refino-metricas">
        /* AFINA SUAVEMENTE OS CARTÕES DE MÉTRICAS SEM ALTERAR A ESTRUTURA */
        .metric-card, .telemetry-card, [class*="metric-item"], [class*="telemetry-box"] {
            padding-top: 7px !important;
            padding-bottom: 7px !important;
            min-height: unset !important;
        }
        .metric-card .metric-value, .telemetry-card .metric-value {
            font-size: 0.92rem !important;
            line-height: 1.2 !important;
        }
    </style>
    """

    # Remove versão anterior deste bloco se existir e insere antes do </head>
    conteudo = re.sub(r'<style id="auditor-refino-metricas">.*?</style>\s*', '', conteudo, flags=re.DOTALL)
    if "</head>" in conteudo:
        conteudo = conteudo.replace("</head>", f"{css_refino_metricas}\n</head>", 1)
        print("[OK] Ajuste fino de espessura das métricas aplicado.")

    HTML_PATH.write_text(conteudo, encoding="utf-8")
    print("=" * 75)
    print(f"[SUCESSO] {trocas_feitas} títulos sofisticados aplicados com garantia visual!")
    print("=" * 75)

if __name__ == "__main__":
    aplicar_refinamento_executivo()