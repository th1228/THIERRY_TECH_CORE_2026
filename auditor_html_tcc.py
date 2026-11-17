# -*- coding: utf-8 -*-
import re
import shutil
from pathlib import Path

HTML_PATH = Path("index.html")
BACKUP_PATH = Path("index.html.bak")

def auditor_organizar_sem_quebrar():
    if not HTML_PATH.exists():
        print("[ERRO] index.html não encontrado no diretório.")
        return

    # 1. Backup de segurança obrigatório
    shutil.copy2(HTML_PATH, BACKUP_PATH)
    print(f"[INFO] Backup de segurança criado em: {BACKUP_PATH}")

    conteudo = HTML_PATH.read_text(encoding="utf-8")

    # 2. Remove qualquer bloco antigo do auditor antes de aplicar o novo (evita duplicação)
    conteudo = re.sub(r'<style id="auditor-tcc-styles">.*?</style>\s*', '', conteudo, flags=re.DOTALL)

    # 3. Regras puras de respiro, bordas suaves e contraste (zero risco de quebra)
    css_organizacao_limpa = """
    <style id="auditor-tcc-styles">
        /* ORGANIZAÇÃO VISUAL, RESPIRO E SUAVIZAÇÃO DE BORDAS */
        .biogen-imperial-grid {
            gap: 18px !important;
            padding: 22px !important;
        }
        .grid-cell {
            padding: 14px !important;
            border-width: 1px !important;
            border-radius: 10px !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }
        .grid-cell:hover {
            transform: translateY(-2px) !important;
        }

        /* PROTEÇÃO DE CONTRASTE NO MODO CLARO */
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
        conteudo = conteudo.replace("</head>", f"{css_organizacao_limpa}\n</head>", 1)
        HTML_PATH.write_text(conteudo, encoding="utf-8")
        print("=" * 75)
        print("[SUCESSO] Organização visual e respiro aplicados com 100% de segurança!")
        print("=" * 75)
    else:
        print("[ERRO] Tag </head> não encontrada no index.html.")

if __name__ == "__main__":
    auditor_organizar_sem_quebrar()