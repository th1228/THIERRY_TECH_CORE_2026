# -*- coding: utf-8 -*-
import re
from pathlib import Path

HTML_PATH = Path("index.html")

def auditor_estilo_limpo_silicio():
    if not HTML_PATH.exists():
        print("[ERRO] index.html não encontrado no diretório.")
        return

    conteudo = HTML_PATH.read_text(encoding="utf-8")

    # 1. Remove totalmente o bloco anterior que gerou os contornos ovais
    conteudo = re.sub(r'<style id="auditor-tcc-styles">.*?</style>\s*', '', conteudo, flags=re.DOTALL)

    # 2. Aplica apenas limpeza minimalista e contraste seguro no Modo Claro
    css_minimalista = """
    <style id="auditor-tcc-styles">
        /* ESTILO MINIMALISTA LIMPO - SEM BORDAS OVAIS OU DECORAÇÕES EXTRAS */
        .biogen-imperial-grid {
            gap: 16px !important;
            padding: 20px !important;
        }
        .grid-cell {
            padding: 12px !important;
            border-width: 0.5px !important;
        }

        /* Proteção de legibilidade no Modo Claro */
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
        conteudo = conteudo.replace("</head>", f"{css_minimalista}\n</head>", 1)
        HTML_PATH.write_text(conteudo, encoding="utf-8")
        print("[SUCESSO] Contornos ovais removidos e estilo limpo restaurado!")
    else:
        print("[ERRO] Tag </head> não encontrada no HTML.")

if __name__ == "__main__":
    auditor_estilo_limpo_silicio()