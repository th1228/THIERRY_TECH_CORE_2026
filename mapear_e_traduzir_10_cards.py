# -*- coding: utf-8 -*-
"""
Script: corrigir_loop_10_cards.py
Local: Raiz do projeto (THIERRY_TECH_CORE_2026)
Objetivo: Substitui o patch anterior dos 10 cards por uma versão sem loop
(pausa MutationObserver durante a escrita e respeita o estado ativo de EN/PT),
mantendo backup em _backup_i18n e sem alterar layout, CSS ou z-index.
"""

import json
import re
import shutil
from datetime import datetime
from pathlib import Path


RAIZ = Path(__file__).resolve().parent
INDEX_HTML = RAIZ / "index.html"
PASTA_BACKUP = RAIZ / "_backup_i18n"

PARES_PT_EN = {
    "fototipo": "Phototype",
    "contorno": "Contour",
    "colágeno": "Collagen",
    "colageno": "Collagen",
    "liderança": "Leadership",
    "lideranca": "Leadership",
    "vitalidade": "Vitality",
    "aprovado": "Approved",
    "otimizado": "Optimized",
    "anos": "Years",
    "nós": "Nodes",
    "nos": "Nodes",
    "integridade tecidual": "Tissue Integrity",
    "estável": "Stable",
    "estavel": "Stable",
    "ótimo": "Optimal",
    "otimo": "Optimal",
    "hidratação": "Hydration",
    "hidratacao": "Hydration",
    "balanceado": "Balanced",
    "ativo": "Active",
}


def fazer_backup(arquivo: Path) -> Path:
    PASTA_BACKUP.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = PASTA_BACKUP / f"{arquivo.stem}_sem_loop_{stamp}{arquivo.suffix}.bak"
    shutil.copy2(arquivo, destino)
    return destino


def remover_patches_antigos(html: str) -> str:
    html = re.sub(
        r"\n?<script id=\"thierry-10-cards-i18n-patch\">.*?</script>",
        "",
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    html = re.sub(
        r"\n?<script id=\"thierry-10-cards-live-i18n\">.*?</script>",
        "",
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    html = re.sub(
        r"\n?<script id=\"thierry-10-cards-estavel-i18n\">.*?</script>",
        "",
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    return html


def injetar_patch_estavel(html: str) -> str:
    pares_json = json.dumps(PARES_PT_EN, ensure_ascii=False, indent=4)

    script_estavel = (
        '<script id="thierry-10-cards-estavel-i18n">\n'
        "(function() {\n"
        f"  const PARES_EN = {pares_json};\n"
        "  const PARES_PT = Object.fromEntries(\n"
        "    Object.entries(PARES_EN).map(([pt, en]) => [en.toLowerCase(), pt])\n"
        "  );\n\n"
        "  let idiomaFixo = null;\n"
        "  let pausarObserver = false;\n"
        "  let timerDebounce = null;\n\n"
        "  function detectarIdiomaAtual() {\n"
        "    if (idiomaFixo === 'en' || idiomaFixo === 'pt') return idiomaFixo;\n\n"
        '    const htmlLang = (document.documentElement.getAttribute("lang") || "").toLowerCase();\n'
        '    if (htmlLang.startsWith("en")) return "en";\n'
        '    if (htmlLang.startsWith("pt")) return "pt";\n\n'
        '    const saved = (localStorage.getItem("lang") || localStorage.getItem("language") || localStorage.getItem("i18nLang") || "").toLowerCase();\n'
        '    if (saved.startsWith("en")) return "en";\n'
        '    if (saved.startsWith("pt")) return "pt";\n\n'
        "    return \"pt\";\n"
        "  }\n\n"
        "  function escaparRegex(str) {\n"
        '    return str.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&");\n'
        "  }\n\n"
        "  function traduzirTexto(texto, alvo) {\n"
        '    if (!texto || typeof texto !== "string") return texto;\n'
        '    const mapa = alvo === "en" ? PARES_EN : PARES_PT;\n'
        "    let saida = texto;\n"
        "    const chaves = Object.keys(mapa).sort((a, b) => b.length - a.length);\n"
        "    for (const termo of chaves) {\n"
        '      const regex = new RegExp("(?<![A-Za-zÀ-ÿ0-9_])" + escaparRegex(termo) + "(?![A-Za-zÀ-ÿ0-9_])", "gi");\n'
        "      saida = saida.replace(regex, (match) => {\n"
        "        const trad = mapa[termo.toLowerCase()];\n"
        "        if (!trad) return match;\n"
        "        if (match === match.toUpperCase()) return trad.toUpperCase();\n"
        "        if (match[0] === match[0].toUpperCase()) return trad.charAt(0).toUpperCase() + trad.slice(1);\n"
        "        return trad;\n"
        "      });\n"
        "    }\n"
        "    return saida;\n"
        "  }\n\n"
        "  function obterAlvosDos10Cards() {\n"
        '    const candidatos = Array.from(document.querySelectorAll("div, article, section, li"));\n'
        "    const cards = candidatos.filter((el) => {\n"
        '      const txt = (el.textContent || "");\n'
        '      return /ID\\s*0(?:0[1-9]|10)\\b/i.test(txt) && txt.length < 600 && el.children.length >= 2;\n'
        "    });\n"
        "    return cards.slice(0, 10);\n"
        "  }\n\n"
        "  function aplicarNos10Cards(langForcado) {\n"
        "    if (langForcado === 'en' || langForcado === 'pt') {\n"
        "      idiomaFixo = langForcado;\n"
        "    }\n"
        "    const alvo = detectarIdiomaAtual();\n"
        "    const cards = obterAlvosDos10Cards();\n"
        "    const escopos = cards.length > 0 ? cards : [document.body];\n\n"
        "    pausarObserver = true;\n"
        "    try {\n"
        "      escopos.forEach((raizCard) => {\n"
        "        if (!raizCard) return;\n"
        "        const walker = document.createTreeWalker(raizCard, NodeFilter.SHOW_TEXT);\n"
        "        let node;\n"
        "        while ((node = walker.nextNode())) {\n"
        "          const pai = node.parentElement;\n"
        '          if (!pai || ["SCRIPT", "STYLE", "NOSCRIPT"].includes(pai.tagName)) continue;\n'
        "          const original = node.nodeValue;\n"
        "          const traduzido = traduzirTexto(original, alvo);\n"
        "          if (traduzido !== original) {\n"
        "            node.nodeValue = traduzido;\n"
        "          }\n"
        "        }\n"
        "      });\n"
        "    } finally {\n"
        "      setTimeout(() => { pausarObserver = false; }, 30);\n"
        "    }\n"
        "  }\n\n"
        "  window.aplicarNos10Cards = aplicarNos10Cards;\n\n"
        '  document.addEventListener("click", function(ev) {\n'
        '    const alvoBtn = ev.target.closest("button, [data-lang], a, span, div");\n'
        "    if (!alvoBtn) return;\n"
        '    const rotulo = (alvoBtn.getAttribute("data-lang") || alvoBtn.textContent || "").trim().toUpperCase();\n'
        '    if (rotulo === "EN" || rotulo === "ENGLISH") {\n'
        "      idiomaFixo = 'en';\n"
        '      [60, 180, 400].forEach((ms) => setTimeout(() => aplicarNos10Cards("en"), ms));\n'
        '    } else if (rotulo === "PT" || rotulo === "PORTUGUÊS" || rotulo === "PORTUGUES") {\n'
        "      idiomaFixo = 'pt';\n"
        '      [60, 180, 400].forEach((ms) => setTimeout(() => aplicarNos10Cards("pt"), ms));\n'
        "    }\n"
        "  }, true);\n\n"
        "  const observer = new MutationObserver(() => {\n"
        "    if (pausarObserver || !idiomaFixo) return;\n"
        "    clearTimeout(timerDebounce);\n"
        "    timerDebounce = setTimeout(() => aplicarNos10Cards(idiomaFixo), 90);\n"
        "  });\n\n"
        '  document.addEventListener("DOMContentLoaded", function() {\n'
        "    const inicial = detectarIdiomaAtual();\n"
        "    if (inicial === 'en') idiomaFixo = 'en';\n"
        "    aplicarNos10Cards(inicial);\n"
        "    if (document.body) {\n"
        "      observer.observe(document.body, { childList: true, subtree: true, characterData: true });\n"
        "    }\n"
        "  });\n"
        "})();\n"
        "</script>"
    )

    if re.search(r"</body>", html, flags=re.IGNORECASE):
        return re.sub(
            r"(</body>)",
            lambda m: script_estavel + "\n" + m.group(1),
            html,
            count=1,
            flags=re.IGNORECASE,
        )
    return html + "\n" + script_estavel


def executar() -> None:
    if not INDEX_HTML.exists():
        print(f"[ERRO] index.html não encontrado em: {INDEX_HTML}")
        return

    backup = fazer_backup(INDEX_HTML)
    conteudo = INDEX_HTML.read_text(encoding="utf-8")
    limpo = remover_patches_antigos(conteudo)
    final_html = injetar_patch_estavel(limpo)
    INDEX_HTML.write_text(final_html, encoding="utf-8")

    print(f"[OK] Backup salvo em : {backup}")
    print("[OK] Patches antigos removidos e versão sem loop aplicada nos 10 cards.")


if __name__ == "__main__":
    executar()