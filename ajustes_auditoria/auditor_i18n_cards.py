# -*- coding: utf-8 -*-
"""
Script: auditor_i18n_cards.py
Local: Raiz do projeto (THIERRY_TECH_CORE_2026)
Objetivo: Faz backup seguro do index.html, audita cards e textos sem tradução
PT/EN, gera relatório do que precisa ser feito e pode aplicar marcações
data-i18n + dicionário EN sem quebrar o layout.
"""

import re
import shutil
from datetime import datetime
from pathlib import Path


RAIZ = Path(__file__).resolve().parent
INDEX_HTML = RAIZ / "index.html"
PASTA_BACKUP = RAIZ / "_backup_i18n"
RELATORIO_TXT = RAIZ / "relatorio_i18n_cards.txt"

# Traduções base para termos comuns dos cards / painel (PT -> EN)
MAPA_PT_EN = {
    "integridade": "Integrity",
    "colágeno": "Collagen",
    "colageno": "Collagen",
    "hidratação": "Hydration",
    "hidratacao": "Hydration",
    "elasticidade": "Elasticity",
    "luminosidade": "Luminosity",
    "firmeza": "Firmness",
    "textura": "Texture",
    "simetria": "Symmetry",
    "vitalidade": "Vitality",
    "harmonia": "Harmony",
    "equilíbrio": "Equilibrium",
    "equilibrio": "Equilibrium",
    "governança": "Governance",
    "governanca": "Governance",
    "telemetria": "Telemetry",
    "visagismo": "Visagism",
    "tricologia": "Trichology",
    "rejuvenescimento": "Rejuvenation",
    "sincronizado": "Synchronized",
    "ativos": "Active",
    "nós": "Nodes",
    "nos": "Nodes",
    "relatório": "Report",
    "relatorio": "Report",
    "executar": "Execute",
    "ativar": "Activate",
}


def fazer_backup_seguro(arquivo: Path) -> Path:
    PASTA_BACKUP.mkdir(exist_ok=True)
    carimbo = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = PASTA_BACKUP / f"{arquivo.stem}_{carimbo}{arquivo.suffix}.bak"
    shutil.copy2(arquivo, destino)
    return destino


def limpar_tags(trecho_html: str) -> str:
    sem_tags = re.sub(r"<[^>]+>", " ", trecho_html)
    return re.sub(r"\s+", " ", sem_tags).strip()


def auditar_html(html: str) -> dict:
    tem_i18n = bool(re.search(r"data-i18n", html, flags=re.IGNORECASE))
    tem_troca_idioma = bool(
        re.search(r"(setLanguage|switchLang|applyLang|lang\s*===?\s*['\"]en['\"]|i18n)", html, flags=re.IGNORECASE)
    )

    # Captura blocos que pareçam cards por classe ou id
    padrao_card = re.compile(
        r"<([a-z0-9]+)([^>]*(?:class|id)=[\"'][^\"']*card[^\"']*[\"'][^>]*)>(.*?)</\1>",
        flags=re.IGNORECASE | re.DOTALL,
    )
    cards_encontrados = []
    for idx, m in enumerate(padrao_card.finditer(html), start=1):
        tag_abertura = f"<{m.group(1)}{m.group(2)}>"
        miolo = m.group(3)
        texto_limpo = limpar_tags(miolo)
        possui_attr_i18n = "data-i18n" in tag_abertura.lower() or "data-i18n" in miolo.lower()
        cards_encontrados.append(
            {
                "indice": idx,
                "possui_attr_i18n": possui_attr_i18n,
                "texto": texto_limpo[:120],
            }
        )

    # Captura textos visíveis dentro de tags comuns que não tenham data-i18n
    textos_sem_i18n = []
    for tag_m in re.finditer(
        r"<(h[1-6]|p|span|label|button|strong|small|div)([^>]*)>([^<]{2,100})</\1>",
        html,
        flags=re.IGNORECASE,
    ):
        attrs = tag_m.group(2)
        texto = re.sub(r"\s+", " ", tag_m.group(3)).strip()
        if not texto or texto.isdigit():
            continue
        if "data-i18n" not in attrs.lower():
            # Filtra textos que pareçam palavras/rótulos legíveis
            if re.search(r"[A-Za-zÀ-ÿ]{2,}", texto):
                textos_sem_i18n.append((tag_m.group(1).lower(), texto))

    return {
        "tem_i18n": tem_i18n,
        "tem_troca_idioma": tem_troca_idioma,
        "cards": cards_encontrados,
        "textos_sem_i18n": textos_sem_i18n,
    }


def sugerir_en(texto_pt: str) -> str:
    chave_lower = texto_pt.strip().lower()
    if chave_lower in MAPA_PT_EN:
        return MAPA_PT_EN[chave_lower]
    for pt_termo, en_termo in MAPA_PT_EN.items():
        if pt_termo in chave_lower:
            return re.sub(re.escape(pt_termo), en_termo, texto_pt, flags=re.IGNORECASE)
    return f"[EN] {texto_pt}"


def gerar_relatorio(caminho_html: Path, backup_path: Path, diag: dict) -> str:
    linhas = [
        "=" * 70,
        "AUDITORIA DE TRADUÇÃO (PT / EN) & CARDS — THIERRY TECHNOLOGY CONCEPT GLOBAL",
        "=" * 70,
        f"Data/Hora       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Arquivo auditado: {caminho_html}",
        f"Backup seguro   : {backup_path}",
        f"Usa data-i18n? : {'Sim' if diag['tem_i18n'] else 'Não'}",
        f"Função idioma? : {'Sim' if diag['tem_troca_idioma'] else 'Não/Verificar'}",
        f"Cards mapeados : {len(diag['cards'])}",
        f"Textos s/ i18n : {len(diag['textos_sem_i18n'])}",
        "-" * 70,
        "O QUE PRECISA SER FEITO SEM QUEBRAR O LAYOUT:",
        "1. Não alterar classes de grid (.biogen-imperial-grid), z-index nem estrutura",
        "   de contêineres; mexer apenas no conteúdo textual/atributos data-i18n",
        "   e no dicionário de tradução PT/EN.",
        "2. Se algum card for renderizado via JavaScript, garantir que a função de",
        "   troca de idioma (PT/EN) chame novamente a renderização dos cards.",
        "3. Conferir cada rótulo de card no navegador após alternar para EN.",
        "-" * 70,
        "CARDS DETECTADOS NO HTML:",
    ]

    if not diag["cards"]:
        linhas.append("  [AVISO] Nenhum bloco com 'card' no class/id foi pego por regex estática.")
        linhas.append("          Verifique se os cards são gerados por JS ou usam outra classe.")
    else:
        for c in diag["cards"]:
            status = "COM data-i18n" if c["possui_attr_i18n"] else "SEM data-i18n"
            linhas.append(f"  Card #{c['indice']:02d} [{status}]: {c['texto'] or '(vazio/dinâmico)'}")

    linhas.append("-" * 70)
    linhas.append("AMOSTRA DE RÓTULOS/TEXTOS SEM data-i18n (ATÉ 40 ITENS):")
    vistos = set()
    contador = 0
    for tag, txt in diag["textos_sem_i18n"]:
        chave = (tag, txt)
        if chave in vistos:
            continue
        vistos.add(chave)
        contador += 1
        linhas.append(f"  [{tag}] '{txt}'  -->  Sugestão EN: '{sugerir_en(txt)}'")
        if contador >= 40:
            break

    if contador == 0:
        linhas.append("  Nenhum texto direto sem data-i18n detectado nas tags inspecionadas.")

    linhas.append("=" * 70)
    return "\n".join(linhas)


def executar_auditoria(caminho_html: Path = INDEX_HTML) -> None:
    if not caminho_html.exists():
        print(f"[ERRO] index.html não encontrado em: {caminho_html}")
        return

    backup = fazer_backup_seguro(caminho_html)
    conteudo = caminho_html.read_text(encoding="utf-8")
    diag = auditar_html(conteudo)
    texto_relatorio = gerar_relatorio(caminho_html, backup, diag)

    RELATORIO_TXT.write_text(texto_relatorio, encoding="utf-8")
    print(texto_relatorio)
    print(f"\n[OK] Cópia de segurança salva em: {backup}")
    print(f"[OK] Relatório completo salvo em: {RELATORIO_TXT}")


if __name__ == "__main__":
    executar_auditoria()