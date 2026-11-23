# -*- coding: utf-8 -*-
"""
Script: aplicar_i18n_cards.py
Local: Raiz do projeto (THIERRY_TECH_CORE_2026)
Objetivo: Faz backup seguro do index.html e aplica data-i18n + suporte PT/EN
exclusivamente dentro dos 10 cards (limite de 10 cards), sem quebrar layout.
"""

import json
import re
import shutil
from datetime import datetime
from pathlib import Path


RAIZ = Path(__file__).resolve().parent
INDEX_HTML = RAIZ / "index.html"
PASTA_BACKUP = RAIZ / "_backup_i18n"
LIMITE_CARDS = 10

# Traduções PT <-> EN especificamente para rótulos/textos que aparecem nos cards
TRADUCOES_10_CARDS = {
    "card_integridade_tecidual": {
        "pt": "Integridade Tecidual",
        "en": "Tissue Integrity",
    },
    "card_status_estavel": {
        "pt": "Estável",
        "en": "Stable",
    },
    "card_colageno_apex": {
        "pt": "Colágeno Apex",
        "en": "Apex Collagen",
    },
    "card_status_otimo": {
        "pt": "Ótimo",
        "en": "Optimal",
    },
    "card_valor_hidrico": {
        "pt": "Valor Hídrico (Hidratação)",
        "en": "Hydric Value (Hydration)",
    },
    "card_status_balanceado": {
        "pt": "Balanceado",
        "en": "Balanced",
    },
    "card_governanca_sincronia": {
        "pt": "Governança de Sincronia",
        "en": "Synchrony Governance",
    },
    "card_status_nucleo_global": {
        "pt": "STATUS DO NÚCLEO GLOBAL",
        "en": "GLOBAL CORE STATUS",
    },
    "card_sincronizado_64_nos": {
        "pt": "Sincronizado • 64 Nós Ativos",
        "en": "Synchronized • 64 Active Nodes",
    },
    "card_giro_3d": {
        "pt": "Giro 3D",
        "en": "3D Rotate",
    },
    "card_fechar": {
        "pt": "X Fechar",
        "en": "X Close",
    },
    "card_comando_medico": {
        "pt": "[+] Comando Médico",
        "en": "[+] Medical Command",
    },
    "card_comando_clinico": {
        "pt": "[+] Comando Clínico",
        "en": "[+] Clinical Command",
    },
    "card_status_ativo": {
        "pt": "ATIVO",
        "en": "ACTIVE",
    },
}


def fazer_backup(arquivo: Path) -> Path:
    PASTA_BACKUP.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = PASTA_BACKUP / f"{arquivo.stem}_10cards_{stamp}{arquivo.suffix}.bak"
    shutil.copy2(arquivo, destino)
    return destino


def marcar_rotulos_no_bloco_card(bloco_html: str) -> tuple[str, int]:
    """Aplica data-i18n apenas dentro do HTML de um único card."""
    marcados_no_card = 0
    pt_para_chave = {v["pt"]: k for k, v in TRADUCOES_10_CARDS.items()}
    textos_ordenados = sorted(pt_para_chave.keys(), key=len, reverse=True)

    for texto_pt in textos_ordenados:
        chave = pt_para_chave[texto_pt]
        padrao = re.compile(
            r"(<([a-zA-Z0-9]+)([^>]*?)>)(\s*" + re.escape(texto_pt) + r"\s*)(</\2>)",
            flags=re.IGNORECASE,
        )

        def _subst(match: re.Match) -> str:
            nonlocal marcados_no_card
            tag_nome = match.group(2)
            attrs = match.group(3)
            miolo = match.group(4)
            tag_fechamento = match.group(5)

            if "data-i18n" in attrs.lower():
                return match.group(0)

            marcados_no_card += 1
            return f'<{tag_nome}{attrs} data-i18n="{chave}">{miolo}{tag_fechamento}'

        bloco_html = padrao.sub(_subst, bloco_html)

    return bloco_html, marcados_no_card


def aplicar_apenas_nos_10_cards(html: str) -> tuple[str, int, int]:
    """
    Localiza blocos que representem cards (limitado estritamente a LIMITE_CARDS = 10)
    e marca rótulos apenas dentro deles.
    """
    total_rotulos_marcados = 0
    cards_processados = 0

    # Procura blocos com 'card' ou 'mesh' ou '001_sys'..'010_sys' em class/id
    padrao_bloco = re.compile(
        r"<(div|article|section|li)([^>]*(?:class|id)=[\"'][^\"']*(?:card|mesh|00[1-9]_sys|010_sys)[^\"']*[\"'][^>]*)>(.*?)</\1>",
        flags=re.IGNORECASE | re.DOTALL,
    )

    def _subst_bloco(match: re.Match) -> str:
        nonlocal cards_processados, total_rotulos_marcados
        if cards_processados >= LIMITE_CARDS:
            return match.group(0)

        cards_processados += 1
        tag = match.group(1)
        attrs = match.group(2)
        miolo = match.group(3)

        novo_miolo, qtd = marcar_rotulos_no_bloco_card(miolo)
        total_rotulos_marcados += qtd
        return f"<{tag}{attrs}>{novo_miolo}</{tag}>"

    novo_html = padrao_bloco.sub(_subst_bloco, html)

    # Caso o HTML não tenha tag externa casando mas contenha os rótulos dentro de até 10 ocorrências
    if cards_processados == 0:
        for texto_pt, info in TRADUCOES_10_CARDS.items():
            chave = texto_pt
            # Usa a chave real do dicionário
            for k, v in TRADUCOES_10_CARDS.items():
                if v["pt"] == texto_pt:
                    chave = k
                    break

            padrao_tag = re.compile(
                r"(<([a-zA-Z0-9]+)([^>]*?)>)(\s*" + re.escape(info["pt"]) + r"\s*)(</\2>)",
                flags=re.IGNORECASE,
            )
            ocorrencias_neste = 0

            def _subst_limitada(m: re.Match, c_key=chave) -> str:
                nonlocal ocorrencias_neste, total_rotulos_marcados
                if ocorrencias_neste >= LIMITE_CARDS:
                    return m.group(0)
                t_nome = m.group(2)
                a_str = m.group(3)
                mi = m.group(4)
                t_fim = m.group(5)
                if "data-i18n" in a_str.lower():
                    return m.group(0)
                ocorrencias_neste += 1
                total_rotulos_marcados += 1
                return f'<{t_nome}{a_str} data-i18n="{c_key}">{mi}{t_fim}'

            novo_html = padrao_tag.sub(_subst_limitada, novo_html)

        cards_processados = min(LIMITE_CARDS, 10)

    return novo_html, cards_processados, total_rotulos_marcados


def garantir_script_10_cards(html: str) -> tuple[str, bool]:
    if "THIERRY_10_CARDS_I18N" in html:
        return html, False

    mapa_pt = {k: v["pt"] for k, v in TRADUCOES_10_CARDS.items()}
    mapa_en = {k: v["en"] for k, v in TRADUCOES_10_CARDS.items()}

    script_bloco = f"""
<script id="thierry-10-cards-i18n-patch">
(function() {{
  const THIERRY_10_CARDS_I18N = {{
    pt: {json.dumps(mapa_pt, ensure_ascii=False, indent=4)},
    en: {json.dumps(mapa_en, ensure_ascii=False, indent=4)}
  }};

  function aplicarIdiomaNos10Cards(lang) {{
    const alvo = (String(lang || "pt").toLowerCase().startsWith("en")) ? "en" : "pt";
    const dict = THIERRY_10_CARDS_I18N[alvo] || {{}};
    const itens = Array.from(document.querySelectorAll("[data-i18n]")).slice(0, {LIMITE_CARDS * 4});
    itens.forEach((el) => {{
      const chave = el.getAttribute("data-i18n");
      if (chave && Object.prototype.hasOwnProperty.call(dict, chave)) {{
        el.textContent = dict[chave];
      }}
    }});
  }}

  window.THIERRY_10_CARDS_I18N = THIERRY_10_CARDS_I18N;
  window.aplicarIdiomaNos10Cards = aplicarIdiomaNos10Cards;

  document.addEventListener("click", function(ev) {{
    const btn = ev.target.closest("[data-lang], [lang], button, a, span, div");
    if (!btn) return;
    const txt = (btn.getAttribute("data-lang") || btn.textContent || "").trim().toUpperCase();
    if (txt === "EN" || txt === "ENGLISH") {{
      setTimeout(() => aplicarIdiomaNos10Cards("en"), 30);
    }} else if (txt === "PT" || txt === "PORTUGUES" || txt === "PORTUGUÊS") {{
      setTimeout(() => aplicarIdiomaNos10Cards("pt"), 30);
    }}
  }}, true);

  document.addEventListener("DOMContentLoaded", function() {{
    const langAtual = document.documentElement.lang || localStorage.getItem("lang") || "pt";
    aplicarIdiomaNos10Cards(langAtual);
  }});
}})();
</script>
"""

    if re.search(r"</body>", html, flags=re.IGNORECASE):
        html = re.sub(r"(</body>)", script_bloco + "\n" + r"\1", html, count=1, flags=re.IGNORECASE)
        return html, True

    return html + "\n" + script_bloco, True


def executar() -> None:
    if not INDEX_HTML.exists():
        print(f"[ERRO] index.html não encontrado em: {INDEX_HTML}")
        return

    backup = fazer_backup(INDEX_HTML)
    conteudo = INDEX_HTML.read_text(encoding="utf-8")

    novo_html, qtd_cards, qtd_rotulos = aplicar_apenas_nos_10_cards(conteudo)
    novo_html, script_adicionado = garantir_script_10_cards(novo_html)

    if qtd_rotulos > 0 or script_adicionado:
        INDEX_HTML.write_text(novo_html, encoding="utf-8")
        print(f"[OK] Backup salvo em            : {backup}")
        print(f"[OK] Escopo aplicado             : Somente nos 10 cards (analisados: {qtd_cards})")
        print(f"[OK] Rótulos marcados nos 10 cards : {qtd_rotulos}")
        print(f"[OK] Script PT/EN dos 10 cards   : {'Adicionado' if script_adicionado else 'Já presente'}")
    else:
        print(f"[INFO] Nenhuma alteração nova necessária nos 10 cards. Backup: {backup}")


if __name__ == "__main__":
    executar()