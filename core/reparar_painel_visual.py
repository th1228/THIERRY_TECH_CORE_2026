# -*- coding: utf-8 -*-
"""
Módulo: reparar_painel_visual.py
Descrição: Varre ficheiros HTML e CSS do painel, normalizando z-index >= 100
para 50 (auditoria MIBO), substituindo termos indesejados no HTML visível,
simplificando/centralizando os identificadores MESH / _SYS no rodapé dos
cards (garantindo ID 010 · 64N no 10º card) sem quebrar blocos existentes
e oferecendo restauração via S ou V em caso de erro.
"""

import re
import sys
from pathlib import Path

SUBSTITUICOES_HTML = {
    "Tecnologia & Visagismo Trilionário": "Tecnologia & Visagismo / Intangíveis",
    "Visagismo Trilionário": "Visagismo / Intangíveis",
}

PASTAS_IGNORADAS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".idea",
    "build",
    "dist",
    "node_modules",
    "_backup_seguro",
    "_backup_cirurgico",
    "_backup_html_painel",
    "_organizador_aa",
    "backups",
}

STYLE_ID_MESH = """<style id="reparo-rodape-mesh">
  .mesh-rodape-limpo {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    gap: 2px !important;
    padding: 4px 6px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    font-size: 0.68rem !important;
    line-height: 1.25 !important;
    letter-spacing: 0.2px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
  }
</style>"""

SCRIPT_ID_MESH = """<script id="reparo-rodape-mesh-js">
(function () {
  function extrairNumeroDoCard(el, indiceFallback) {
    const card = el.closest("[class*='card'], [id*='card'], article, li, .item") || el.parentElement;
    const textoCard = card ? (card.innerText || card.textContent || "") : "";

    if (/\\b10\\s*[.\\-–—:]\\s*AUT[OÔ]NOMO\\b/i.test(textoCard)) {
      return "010";
    }

    const matchPrefixo = textoCard.match(/(?:^|\\n|\\s)(0?[1-9]|10)\\s*[.\\-–—:]\\s*[A-ZÁÉÍÓÚÂÊÔÃÕÇ]/i);
    if (matchPrefixo) {
      return String(parseInt(matchPrefixo[1], 10)).padStart(3, "0");
    }

    return String(indiceFallback).padStart(3, "0");
  }

  function formatarIdentificadorCurto(raw, el, indiceFallback) {
    const fonte = el.getAttribute("title") || raw || "";
    const limpo = fonte.replace(/\\s+/g, " ").trim();

    const numMatch =
      limpo.match(/\\b(\\d{3})_SYS\\b/i) ||
      limpo.match(/\\bID\\s*0*(\\d{1,3})\\b/i);

    const meshMatch =
      limpo.match(/MESH_(\\d+N)(?:_[A-Z0-9_]+)?/i) ||
      limpo.match(/\\b(\\d+N)\\b/i);

    const numeroCard = extrairNumeroDoCard(el, indiceFallback);
    const idFinal = numMatch
      ? String(parseInt(numMatch[1], 10)).padStart(3, "0")
      : numeroCard;

    const malhaFinal = meshMatch ? meshMatch[1].toUpperCase() : "64N";
    return `ID ${idFinal} · ${malhaFinal}`;
  }

  function organizarRodapeMesh() {
    const candidatos = Array.from(
      document.querySelectorAll("div, span, p, small, footer, label, code")
    );
    let indiceCard = 0;

    candidatos.forEach((el) => {
      if (el.closest("#reparo-rodape-mesh-js")) return;
      if (el.children.length > 2) return;

      const txt = (el.textContent || "").trim();
      if (!txt || txt.length > 90) return;

      const ehAlvo =
        /MESH_[A-Z0-9_]+/i.test(txt) ||
        /\\b\\d{3}_SYS\\b/i.test(txt) ||
        /^ID\\s*\\d{1,3}(\\s*[·•-]\\s*\\d+N)?$/i.test(txt) ||
        /^\\d+N$/i.test(txt) ||
        /^ID\\s*:?$/i.test(txt);

      if (ehAlvo) {
        indiceCard += 1;
        if (!el.getAttribute("title")) {
          el.setAttribute("title", txt);
        }
        el.classList.add("mesh-rodape-limpo");
        el.textContent = formatarIdentificadorCurto(txt, el, indiceCard);
        el.dataset.meshFormatado = "3";
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", organizarRodapeMesh);
  } else {
    organizarRodapeMesh();
  }
  setTimeout(organizarRodapeMesh, 400);
})();
</script>"""


def deve_ignorar(caminho: Path) -> bool:
    return any(
        parte.lower() in PASTAS_IGNORADAS or parte.lower().startswith("snap_")
        for parte in caminho.parts
    )


def substituir_no_html_visivel(html: str, antigo: str, novo: str) -> str:
    """Substitui apenas fora de <script> e <style> para não quebrar JS/CSS."""
    protegidos = []

    def guardar_bloco(match):
        protegidos.append(match.group(0))
        return f"__BLOCO_PROTEGIDO_{len(protegidos) - 1}__"

    texto = re.sub(
        r"<(script|style)\b[^>]*>.*?</\1>",
        guardar_bloco,
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )

    texto = texto.replace(antigo, novo)

    for idx, bloco in enumerate(protegidos):
        texto = texto.replace(f"__BLOCO_PROTEGIDO_{idx}__", bloco)

    return texto


def reparar_rodape_mesh_html(html: str) -> tuple[str, int]:
    """
    Aplica ou atualiza o estilo e ajuste DOM focado nos identificadores MESH / _SYS
    na base dos cards, garantindo que o 10º card receba ID 010 · 64N.
    """
    if "MESH_" not in html and "_SYS" not in html and "reparo-rodape-mesh" not in html:
        return html, 0

    alteracoes = 0
    atualizado = html

    padrao_style = re.compile(
        r'<style\s+id=["\']reparo-rodape-mesh["\']\s*>.*?</style>',
        flags=re.IGNORECASE | re.DOTALL,
    )
    if padrao_style.search(atualizado):
        novo_html = padrao_style.sub(lambda _m: STYLE_ID_MESH, atualizado, count=1)
        if novo_html != atualizado:
            atualizado = novo_html
            alteracoes += 1
    elif re.search(r"</head>", atualizado, flags=re.IGNORECASE):
        atualizado = re.sub(
            r"</head>",
            lambda _m: f"{STYLE_ID_MESH}\n</head>",
            atualizado,
            count=1,
            flags=re.IGNORECASE,
        )
        alteracoes += 1

    padrao_script = re.compile(
        r'<script\s+id=["\']reparo-rodape-mesh-js["\']\s*>.*?</script>',
        flags=re.IGNORECASE | re.DOTALL,
    )
    if padrao_script.search(atualizado):
        novo_html = padrao_script.sub(lambda _m: SCRIPT_ID_MESH, atualizado, count=1)
        if novo_html != atualizado:
            atualizado = novo_html
            alteracoes += 1
    elif re.search(r"</body>", atualizado, flags=re.IGNORECASE):
        atualizado = re.sub(
            r"</body>",
            lambda _m: f"{SCRIPT_ID_MESH}\n</body>",
            atualizado,
            count=1,
            flags=re.IGNORECASE,
        )
        alteracoes += 1

    return atualizado, alteracoes


def restaurar_backups(backups_criados: list[tuple[Path, Path]]) -> None:
    """Restaura os arquivos originais a partir dos backups gerados nesta execução."""
    restaurados = 0
    for arquivo_original, arquivo_bak in backups_criados:
        if arquivo_bak.exists():
            dados = arquivo_bak.read_bytes()
            arquivo_original.write_bytes(dados)
            restaurados += 1
            print(
                f"↩️ [RESTAURADO] {arquivo_original.name} "
                f"voltou ao estado anterior ({arquivo_bak.name})."
            )
    print(f"\n✅ Restauração concluída! {restaurados} arquivo(s) revertido(s) como era antes.")


def perguntar_e_restaurar_se_quiser(backups_criados: list[tuple[Path, Path]]) -> None:
    if not backups_criados:
        print("ℹ️ Nenhum backup novo foi alterado nesta rodada para reverter.")
        return

    print("\n⚠️ Ocorreu erro durante a operação.")
    print(
        "Aperte S ou V e dê Enter para voltar tudo como era antes "
        "(ou qualquer outra tecla para manter):"
    )
    try:
        resposta = input("> ").strip().upper()
    except EOFError:
        resposta = ""

    if resposta in {"S", "V"}:
        restaurar_backups(backups_criados)
    else:
        print("Mantido o estado atual sem reversão automática.")


def reparar_camadas_painel():
    diretorio_base = Path.cwd()
    print(
        f"🎨 [SEGURANÇA ATIVA] Verificação profunda de camadas e textos em: "
        f"{diretorio_base}\n"
    )

    arquivos_alvo = [
        p for p in diretorio_base.rglob("*")
        if p.is_file()
        and p.suffix.lower() in {".html", ".htm", ".css"}
        and not deve_ignorar(p)
    ]

    if not arquivos_alvo:
        print("⚠️ Nenhum ficheiro HTML ou CSS encontrado para varredura.")
        print("\nSTATUS FINAL: NADA ALTERADO.")
        return

    print(f"📁 Total de ficheiros de layout mapeados: {len(arquivos_alvo)}")
    print("=" * 60)

    total_corrigidos = 0
    total_trocas_texto = 0
    total_ajustes_mesh = 0
    erros: list[tuple[str, str]] = []
    backups_desta_ronda: list[tuple[Path, Path]] = []

    for caminho in arquivos_alvo:
        try:
            try:
                conteudo_original = caminho.read_text(encoding="utf-8")
                encoding_usado = "utf-8"
            except UnicodeDecodeError:
                conteudo_original = caminho.read_text(encoding="latin-1")
                encoding_usado = "latin-1"

            def substituir_z_index(match):
                valor_str = match.group(1)
                if not valor_str or not valor_str.isdigit():
                    return match.group(0)
                valor = int(valor_str)
                if valor >= 100:
                    return "z-index: 50"
                return match.group(0)

            conteudo_atualizado = re.sub(
                r"z-index\s*:\s*(\d+)",
                substituir_z_index,
                conteudo_original,
                flags=re.IGNORECASE,
            )

            trocas_neste_arquivo = 0
            ajustes_mesh_neste_arquivo = 0

            if caminho.suffix.lower() in {".html", ".htm"}:
                for antigo, novo in SUBSTITUICOES_HTML.items():
                    antes = conteudo_atualizado.count(antigo)
                    if antes > 0:
                        conteudo_atualizado = substituir_no_html_visivel(
                            conteudo_atualizado, antigo, novo
                        )
                        depois = conteudo_atualizado.count(antigo)
                        feitas = max(0, antes - depois)
                        trocas_neste_arquivo += feitas
                        total_trocas_texto += feitas

                conteudo_atualizado, ajustes_mesh_neste_arquivo = reparar_rodape_mesh_html(
                    conteudo_atualizado
                )
                total_ajustes_mesh += ajustes_mesh_neste_arquivo

            if conteudo_atualizado != conteudo_original:
                backup_path = caminho.with_suffix(caminho.suffix + ".bak")
                backup_path.write_text(conteudo_original, encoding=encoding_usado)
                backups_desta_ronda.append((caminho, backup_path))

                caminho.write_text(conteudo_atualizado, encoding=encoding_usado)
                total_corrigidos += 1
                print(
                    f"✔ [CORRIGIDO] {caminho.name} "
                    f"(trocas de texto: {trocas_neste_arquivo} | "
                    f"ajustes rodapé MESH: {ajustes_mesh_neste_arquivo} | "
                    f"Backup: {backup_path.name})"
                )
            else:
                print(f"✔ [ESTÁVEL] {caminho.name} sem alterações necessárias.")

        except Exception as e:
            erros.append((caminho.name, str(e)))
            print(f"❌ Erro em {caminho.name}: {e}")

    print("=" * 60)
    print(f"🎯 Varredura concluída! Ficheiros corrigidos nesta ronda: {total_corrigidos}")
    print(f"📝 Substituições de texto feitas no HTML: {total_trocas_texto}")
    print(f"🧩 Ajustes de rodapé MESH aplicados: {total_ajustes_mesh}\n")

    if erros:
        print(f"STATUS FINAL: DEU PROBLEMA EM {len(erros)} ARQUIVO(S).")
        for nome_arq, msg_erro in erros:
            print(f"  - {nome_arq}: {msg_erro}")
        perguntar_e_restaurar_se_quiser(backups_desta_ronda)
        sys.exit(1)
    elif total_corrigidos > 0:
        print("STATUS FINAL: DEU CERTO! Painel atualizado com segurança.")
    else:
        print("STATUS FINAL: DEU CERTO, MAS NADA PRECISOU SER ALTERADO.")


if __name__ == "__main__":
    try:
        reparar_camadas_painel()
    except Exception as erro_critico:
        print(f"\n❌ Erro inesperado na execução: {erro_critico}")
        perguntar_e_restaurar_se_quiser([])
        sys.exit(1)