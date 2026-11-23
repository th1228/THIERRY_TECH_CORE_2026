# -*- coding: utf-8 -*-
"""
Script: reparar_painel_visual.py
Local: Raiz do projeto (THIERRY_TECH_CORE_2026)
Objetivo: Garante meta viewport e regras CSS @media (max-width: 1024px e 640px)
no index.html localizado na raiz do projeto.
"""

import re
import shutil
from pathlib import Path


RAIZ_PROJETO = Path(__file__).resolve().parent
INDEX_HTML = RAIZ_PROJETO / "index.html"

BLOCO_RESPONSIVO = """
/* === RESPONSIVIDADE TABLET (<= 1024px) & CELULAR (<= 640px) === */
@media (max-width: 1024px) {
  .biogen-imperial-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
  }

  body {
    overflow-x: hidden;
  }
}

@media (max-width: 640px) {
  .biogen-imperial-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  body {
    font-size: 14px;
    padding: 12px;
    overflow-x: hidden;
  }
}
"""


def reparar_painel_na_raiz(caminho_html: Path) -> None:
    print(f"Raiz        : {RAIZ_PROJETO}")
    print(f"Arquivo alvo: {caminho_html}")

    if not caminho_html.exists() or not caminho_html.is_file():
        print("[ERRO] index.html não encontrado na raiz do projeto.")
        return

    conteudo = caminho_html.read_text(encoding="utf-8")
    backup = caminho_html.with_suffix(".html.bak")
    shutil.copy2(caminho_html, backup)

    alterado = False

    if 'name="viewport"' not in conteudo and "name='viewport'" not in conteudo:
        meta_tag = '  <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
        if re.search(r"</head>", conteudo, flags=re.IGNORECASE):
            conteudo = re.sub(
                r"(</head>)", meta_tag + r"\1", conteudo, count=1, flags=re.IGNORECASE
            )
            alterado = True
            print('[OK] Tag <meta name="viewport"> adicionada ao <head>.')

    tem_1024 = bool(re.search(r"@media[^\{]*max-width\s*:\s*1024px", conteudo, flags=re.IGNORECASE))
    tem_640 = bool(re.search(r"@media[^\{]*max-width\s*:\s*640px", conteudo, flags=re.IGNORECASE))

    if not (tem_1024 and tem_640):
        if re.search(r"</style>", conteudo, flags=re.IGNORECASE):
            conteudo = re.sub(
                r"(</style>)",
                BLOCO_RESPONSIVO + "\n" + r"\1",
                conteudo,
                count=1,
                flags=re.IGNORECASE,
            )
            alterado = True
            print("[OK] Regras @media (1024px e 640px) inseridas no <style>.")
        elif re.search(r"</head>", conteudo, flags=re.IGNORECASE):
            bloco_style = f"<style>\n{BLOCO_RESPONSIVO}\n</style>\n"
            conteudo = re.sub(
                r"(</head>)",
                bloco_style + r"\1",
                conteudo,
                count=1,
                flags=re.IGNORECASE,
            )
            alterado = True
            print("[OK] Bloco <style> criado com regras @media (1024px e 640px).")
    else:
        print("[OK] Regras @media para 1024px e 640px já constam no index.html.")

    if alterado:
        caminho_html.write_text(conteudo, encoding="utf-8")
        print(f"[SALVO] {caminho_html.name} atualizado (backup em {backup.name}).")
    else:
        if backup.exists():
            backup.unlink()
        print("[INFO] Nenhuma alteração foi necessária no index.html.")


if __name__ == "__main__":
    reparar_painel_na_raiz(INDEX_HTML)