# -*- coding: utf-8 -*-
"""
Script: aplicar_i18n_cards.py
Local: Raiz do projeto (THIERRY_TECH_CORE_2026)
Objetivo: Faz backup seguro do index.html, aplica data-i18n + suporte PT/EN
completo (incluindo títulos/selos internos dos 10 cards e valores compostos de telemetria)
e controla o ciclo de energia da câmera local (desligando o hardware de verdade).
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

# Dicionário completo PT <-> EN (cards internos, selos, telemetria, menus e barra)
TRADUCOES_10_CARDS = {
    # Títulos dos 10 cards (01 a 10)
    "card_01_arquetipo": {"pt": "01. ARQUÉTIPO", "en": "01. ARCHETYPE"},
    "card_02_contorno": {"pt": "02. CONTORNO", "en": "02. CONTOUR"},
    "card_03_colageno": {"pt": "03. COLÁGENO", "en": "03. COLLAGEN"},
    "card_04_olhares": {"pt": "04. OLHARES", "en": "04. GAZE"},
    "card_05_microexpressao": {"pt": "05. MICRO-EXPRESSÃO", "en": "05. MICRO-EXPRESSION"},
    "card_05_microexpressao_alt": {"pt": "05. MICROEXPRESSÃO", "en": "05. MICRO-EXPRESSION"},
    "card_06_15_anos": {"pt": "06. +15 ANOS", "en": "06. +15 YEARS"},
    "card_07_lideranca": {"pt": "07. LIDERANÇA", "en": "07. LEADERSHIP"},
    "card_08_vitalidade": {"pt": "08. VITALIDADE", "en": "08. VITALITY"},
    "card_09_soberania": {"pt": "09. SOBERANIA", "en": "09. SOVEREIGNTY"},
    "card_10_simetria": {"pt": "10. SIMETRIA", "en": "10. SYMMETRY"},

    # Selos / tarjas internas dos 10 cards
    "selo_aprovado": {"pt": "APROVADO", "en": "APPROVED"},
    "selo_normal": {"pt": "NORMAL", "en": "NORMAL"},
    "selo_style": {"pt": "STYLE", "en": "STYLE"},
    "selo_estilo": {"pt": "ESTILO", "en": "STYLE"},
    "selo_imperial": {"pt": "IMPERIAL", "en": "IMPERIAL"},
    "selo_otimizado": {"pt": "OTIMIZADO", "en": "OPTIMIZED"},
    "selo_estavel_upper": {"pt": "ESTÁVEL", "en": "STABLE"},
    "selo_zona_critica": {"pt": "ZONA CRÍTICA", "en": "CRITICAL ZONE"},
    "selo_critico": {"pt": "CRÍTICO", "en": "CRITICAL"},
    "selo_alerta": {"pt": "ALERTA", "en": "ALERT"},
    "selo_soberano": {"pt": "SOBERANO", "en": "SOVEREIGN"},
    "selo_maximo": {"pt": "MÁXIMO", "en": "MAXIMUM"},
    "selo_autonomo": {"pt": "AUTÔNOMO", "en": "AUTONOMOUS"},

    # Rótulos gerais e telemetria
    "card_integridade_tecidual": {"pt": "Integridade Tecidual", "en": "Tissue Integrity"},
    "card_status_estavel": {"pt": "Estável", "en": "Stable"},
    "card_colageno_apex": {"pt": "Colágeno Apex", "en": "Apex Collagen"},
    "card_status_otimo": {"pt": "Ótimo", "en": "Optimal"},
    "card_valor_hidrico": {"pt": "Valor Hídrico (Hidratação)", "en": "Hydric Value (Hydration)"},
    "card_status_balanceado": {"pt": "Balanceado", "en": "Balanced"},
    "card_governanca_sincronia": {"pt": "Governança de Sincronia", "en": "Synchrony Governance"},
    "card_status_nucleo_global": {"pt": "STATUS DO NÚCLEO GLOBAL", "en": "GLOBAL CORE STATUS"},
    "card_sincronizado_64_nos": {"pt": "Sincronizado • 64 Nós Ativos", "en": "Synchronized • 64 Active Nodes"},
    "card_giro_3d": {"pt": "Giro 3D", "en": "3D Rotate"},
    "card_fechar": {"pt": "X Fechar", "en": "X Close"},
    "card_comando_medico": {"pt": "[+] Comando Médico", "en": "[+] Medical Command"},
    "card_comando_clinico": {"pt": "[+] Comando Clínico", "en": "[+] Clinical Command"},
    "card_status_ativo": {"pt": "ATIVO", "en": "ACTIVE"},

    # Menu direito/esquerdo, barra superior e rodapé
    "ui_historico_evolucao_uhnw": {"pt": "HISTÓRICO & EVOLUÇÃO UHNW", "en": "UHNW HISTORY & EVOLUTION"},
    "ui_auditoria_ativa": {"pt": "AUDITORIA ATIVA", "en": "ACTIVE AUDIT"},
    "ui_64_nos": {"pt": "64 Nós", "en": "64 Nodes"},
    "ui_ajustes": {"pt": "AJUSTES", "en": "SETTINGS"},
    "ui_cam_ligada": {"pt": "CAM: LIGADA", "en": "CAM: ON"},
    "ui_cam_bloqueada": {"pt": "CAM: BLOQUEADA", "en": "CAM: LOCKED"},
    "ui_ligar": {"pt": "LIGAR", "en": "ON"},
    "ui_desligar": {"pt": "DESLIGAR", "en": "OFF"},
}


def fazer_backup(arquivo: Path) -> Path:
    PASTA_BACKUP.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = PASTA_BACKUP / f"{arquivo.stem}_10cards_{stamp}{arquivo.suffix}.bak"
    shutil.copy2(arquivo, destino)
    return destino


def _construir_mapa_rotulos_para_chave() -> dict[str, str]:
    rotulo_para_chave: dict[str, str] = {}
    for chave, idiomas in TRADUCOES_10_CARDS.items():
        for valor in (idiomas.get("pt"), idiomas.get("en")):
            if valor and valor not in rotulo_para_chave:
                rotulo_para_chave[valor] = chave
    return rotulo_para_chave


def _marcar_rotulos_em_html(html_fragmento: str) -> tuple[str, int]:
    marcados = 0
    rotulo_para_chave = _construir_mapa_rotulos_para_chave()
    textos_ordenados = sorted(rotulo_para_chave.keys(), key=len, reverse=True)

    for texto_alvo in textos_ordenados:
        chave = rotulo_para_chave[texto_alvo]
        padrao = re.compile(
            r"(<([a-zA-Z0-9]+)([^>]*?)>)(\s*" + re.escape(texto_alvo) + r"\s*)(</\2>)",
            flags=re.IGNORECASE,
        )

        def _subst(match: re.Match, c_key=chave) -> str:
            nonlocal marcados
            tag_nome = match.group(2)
            attrs = match.group(3)
            miolo = match.group(4)
            tag_fechamento = match.group(5)

            if "data-i18n" in attrs.lower():
                return match.group(0)

            marcados += 1
            return f'<{tag_nome}{attrs} data-i18n="{c_key}">{miolo}{tag_fechamento}'

        html_fragmento = padrao.sub(_subst, html_fragmento)

    return html_fragmento, marcados


def aplicar_apenas_nos_10_cards(html: str) -> tuple[str, int, int]:
    total_rotulos_marcados = 0
    cards_processados = 0

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

        novo_miolo, qtd = _marcar_rotulos_em_html(miolo)
        total_rotulos_marcados += qtd
        return f"<{tag}{attrs}>{novo_miolo}</{tag}>"

    novo_html = padrao_bloco.sub(_subst_bloco, html)

    partes = re.split(
        r"(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>)",
        novo_html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    for i, parte in enumerate(partes):
        if parte.lower().startswith("<script") or parte.lower().startswith("<style"):
            continue
        novo_parte, qtd_extra = _marcar_rotulos_em_html(parte)
        partes[i] = novo_parte
        total_rotulos_marcados += qtd_extra

    novo_html = "".join(partes)
    if cards_processados == 0:
        cards_processados = min(LIMITE_CARDS, 10)

    return novo_html, cards_processados, total_rotulos_marcados


def _inserir_ou_atualizar_bloco(html: str, bloco_id: str, novo_bloco: str) -> tuple[str, bool]:
    padrao = re.compile(
        r'<script\b[^>]*\bid=["\']' + re.escape(bloco_id) + r'["\'][^>]*>.*?</script>',
        flags=re.IGNORECASE | re.DOTALL,
    )
    if padrao.search(html):
        return padrao.sub(lambda _: novo_bloco, html, count=1), True

    if re.search(r"</body>", html, flags=re.IGNORECASE):
        return re.sub(r"(</body>)", novo_bloco + "\n" + r"\1", html, count=1, flags=re.IGNORECASE), True

    return html + "\n" + novo_bloco, True


def garantir_script_10_cards(html: str) -> tuple[str, bool]:
    mapa_pt = {k: v["pt"] for k, v in TRADUCOES_10_CARDS.items()}
    mapa_en = {k: v["en"] for k, v in TRADUCOES_10_CARDS.items()}

    pares_pt_en = sorted(
        [(v["pt"], v["en"]) for v in TRADUCOES_10_CARDS.values() if v.get("pt") and v.get("en") and v["pt"] != v["en"]],
        key=lambda item: len(item[0]),
        reverse=True,
    )
    pares_en_pt = sorted(
        [(v["en"], v["pt"]) for v in TRADUCOES_10_CARDS.values() if v.get("pt") and v.get("en") and v["pt"] != v["en"]],
        key=lambda item: len(item[0]),
        reverse=True,
    )

    script_bloco = f"""<script id="thierry-10-cards-i18n-patch">
(function() {{
  const THIERRY_10_CARDS_I18N = {{
    pt: {json.dumps(mapa_pt, ensure_ascii=False, indent=4)},
    en: {json.dumps(mapa_en, ensure_ascii=False, indent=4)}
  }};

  const PARES_PT_EN = {json.dumps(pares_pt_en, ensure_ascii=False)};
  const PARES_EN_PT = {json.dumps(pares_en_pt, ensure_ascii=False)};

  let idiomaAtual = (String(document.documentElement.lang || localStorage.getItem("lang") || "pt").toLowerCase().startsWith("en")) ? "en" : "pt";
  let aplicando = false;

  function escaparRegex(str) {{
    return str.replace(/[.*+?^${{}}()|[\\]\\\\]/g, "\\\\$&");
  }}

  function aplicarIdiomaNos10Cards(lang) {{
    if (aplicando) return;
    aplicando = true;
    try {{
      const alvo = (String(lang || idiomaAtual || "pt").toLowerCase().startsWith("en")) ? "en" : "pt";
      idiomaAtual = alvo;
      const dict = THIERRY_10_CARDS_I18N[alvo] || {{}};

      document.querySelectorAll("[data-i18n]").forEach((el) => {{
        const chave = el.getAttribute("data-i18n");
        if (chave && Object.prototype.hasOwnProperty.call(dict, chave)) {{
          if (el.textContent.trim() !== dict[chave]) {{
            el.textContent = dict[chave];
          }}
        }}
      }});

      const pares = alvo === "en" ? PARES_PT_EN : PARES_EN_PT;
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = walker.nextNode())) {{
        const parentTag = node.parentElement ? node.parentElement.tagName : "";
        if (parentTag === "SCRIPT" || parentTag === "STYLE") continue;

        let texto = node.nodeValue || "";
        if (!texto.trim()) continue;

        let modificado = false;
        for (let i = 0; i < pares.length; i++) {{
          const origem = pares[i][0];
          const destino = pares[i][1];
          if (texto.includes(origem)) {{
            const rx = new RegExp("(^|[^A-Za-zÀ-ÿ0-9_])" + escaparRegex(origem) + "(?=$|[^A-Za-zÀ-ÿ0-9_])", "g");
            const novoTexto = texto.replace(rx, "$1" + destino);
            if (novoTexto !== texto) {{
              texto = novoTexto;
              modificado = true;
            }}
          }}
        }}
        if (modificado) {{
          node.nodeValue = texto;
        }}
      }}
    }} finally {{
      aplicando = false;
    }}
  }}

  window.THIERRY_10_CARDS_I18N = THIERRY_10_CARDS_I18N;
  window.aplicarIdiomaNos10Cards = aplicarIdiomaNos10Cards;

  document.addEventListener("click", function(ev) {{
    const btn = ev.target.closest("[data-lang], [lang], button, a, span, div");
    if (!btn) return;
    const txt = (btn.getAttribute("data-lang") || btn.textContent || "").trim().toUpperCase();
    if (txt === "EN" || txt === "ENGLISH") {{
      idiomaAtual = "en";
      setTimeout(() => aplicarIdiomaNos10Cards("en"), 40);
      setTimeout(() => aplicarIdiomaNos10Cards("en"), 250);
    }} else if (txt === "PT" || txt === "PORTUGUES" || txt === "PORTUGUÊS") {{
      idiomaAtual = "pt";
      setTimeout(() => aplicarIdiomaNos10Cards("pt"), 40);
      setTimeout(() => aplicarIdiomaNos10Cards("pt"), 250);
    }}
  }}, true);

  const observer = new MutationObserver(function() {{
    if (!aplicando) {{
      aplicarIdiomaNos10Cards(idiomaAtual);
    }}
  }});

  document.addEventListener("DOMContentLoaded", function() {{
    aplicarIdiomaNos10Cards(idiomaAtual);
    observer.observe(document.body, {{ childList: true, subtree: true }});
  }});
}})();
</script>"""

    return _inserir_ou_atualizar_bloco(html, "thierry-10-cards-i18n-patch", script_bloco)


def garantir_controle_camera_sob_demanda(html: str) -> tuple[str, bool]:
    script_camera = """<script id="thierry-camera-power-patch">
(function() {
  let streamAtivo = null;
  let cameraLigada = false;

  function pararTracksDeStream(stream) {
    if (!stream) return;
    try {
      if (typeof stream.getTracks === "function") {
        stream.getTracks().forEach((track) => {
          try {
            track.enabled = false;
            track.stop();
          } catch (_) {}
        });
      }
      if (typeof stream.getVideoTracks === "function") {
        stream.getVideoTracks().forEach((track) => {
          try {
            track.enabled = false;
            track.stop();
          } catch (_) {}
        });
      }
    } catch (_) {}
  }

  function matarStreamsGlobaisNaWindow() {
    try {
      const chaves = Object.getOwnPropertyNames(window);
      for (let i = 0; i < chaves.length; i++) {
        const k = chaves[i];
        let val = null;
        try {
          val = window[k];
        } catch (_) {
          continue;
        }
        if (val && typeof val === "object" && typeof val.getTracks === "function") {
          pararTracksDeStream(val);
          try {
            window[k] = null;
          } catch (_) {}
        }
      }
    } catch (_) {}
  }

  function atualizarBadgeCamera(ligada) {
    const btn = document.getElementById("btn-toggle-camera");
    if (!btn) return;
    const isEn = String(document.documentElement.lang || localStorage.getItem("lang") || "pt")
      .toLowerCase().startsWith("en");
    if (ligada) {
      btn.textContent = isEn ? "CAM: ON" : "CAM: LIGADA";
      btn.classList.add("active-lang");
    } else {
      btn.textContent = isEn ? "CAM: LOCKED" : "CAM: BLOQUEADA";
      btn.classList.remove("active-lang");
    }
  }

  function desligarCameraLocal() {
    cameraLigada = false;

    // 1. Para tracks e limpa TODOS os elementos <video> da página
    const videos = Array.from(document.querySelectorAll("video"));
    videos.forEach((vid) => {
      try {
        pararTracksDeStream(vid.srcObject);
        vid.pause();
        vid.srcObject = null;
        vid.removeAttribute("src");
        vid.load();
      } catch (_) {}
    });

    // 2. Para o stream rastreado pelo patch e varre referências globais de MediaStream
    pararTracksDeStream(streamAtivo);
    streamAtivo = null;
    matarStreamsGlobaisNaWindow();

    // 3. Re-aplica limpeza curta caso algum listener nativo tente reassociar stream logo em seguida
    setTimeout(() => {
      if (!cameraLigada) {
        document.querySelectorAll("video").forEach((vid) => {
          if (vid.srcObject) {
            pararTracksDeStream(vid.srcObject);
            vid.srcObject = null;
          }
        });
        matarStreamsGlobaisNaWindow();
      }
    }, 120);

    atualizarBadgeCamera(false);
  }

  async function ligarCameraLocal() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      return null;
    }
    if (streamAtivo && typeof streamAtivo.getVideoTracks === "function" &&
        streamAtivo.getVideoTracks().some((t) => t.readyState === "live")) {
      cameraLigada = true;
      atualizarBadgeCamera(true);
      return streamAtivo;
    }

    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "user" },
      audio: false
    });
    streamAtivo = stream;
    cameraLigada = true;

    const vidPrincipal = document.getElementById("webcam-feed-main") || document.querySelector("video");
    if (vidPrincipal) {
      vidPrincipal.srcObject = stream;
      try { await vidPrincipal.play(); } catch (_) {}
    }

    atualizarBadgeCamera(true);
    return stream;
  }

  window.desligarCameraLocal = desligarCameraLocal;
  window.ligarCameraLocal = ligarCameraLocal;

  // Intercepta clique no botão de câmera e em controles explícitos de ligar/desligar câmera
  document.addEventListener("click", function(ev) {
    const alvo = ev.target.closest("#btn-toggle-camera, [data-camera-action], button, a");
    if (!alvo) return;

    const isBtnCam = alvo.id === "btn-toggle-camera" || alvo.hasAttribute("data-camera-action");
    const rotulo = (alvo.textContent || "").trim().toUpperCase();
    const acaoAttr = (alvo.getAttribute("data-camera-action") || "").trim().toLowerCase();

    if (acaoAttr === "off" || acaoAttr === "stop" || rotulo === "DESLIGAR" || rotulo === "OFF") {
      if (isBtnCam || alvo.closest("[id*='cam' i], [class*='cam' i]")) {
        ev.preventDefault();
        ev.stopImmediatePropagation();
        desligarCameraLocal();
        return;
      }
    }

    if (alvo.id === "btn-toggle-camera") {
      ev.preventDefault();
      ev.stopImmediatePropagation();
      if (cameraLigada) {
        desligarCameraLocal();
      } else {
        ligarCameraLocal().catch(() => desligarCameraLocal());
      }
    }
  }, true);

  ["startCinematicScan", "dispararVarreduraComGateway"].forEach((fnName) => {
    const originalFn = window[fnName];
    if (typeof originalFn === "function") {
      window[fnName] = async function(...args) {
        if (!cameraLigada) {
          try { await ligarCameraLocal(); } catch (_) {}
        }
        return originalFn.apply(this, args);
      };
    }
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => setTimeout(desligarCameraLocal, 50));
  } else {
    setTimeout(desligarCameraLocal, 50);
  }

  document.addEventListener("visibilitychange", function() {
    if (document.hidden && cameraLigada) {
      desligarCameraLocal();
    }
  });
  window.addEventListener("beforeunload", desligarCameraLocal);
})();
</script>"""

    return _inserir_ou_atualizar_bloco(html, "thierry-camera-power-patch", script_camera)


def executar() -> None:
    if not INDEX_HTML.exists():
        print(f"[ERRO] index.html não encontrado em: {INDEX_HTML}")
        return

    backup = fazer_backup(INDEX_HTML)
    conteudo = INDEX_HTML.read_text(encoding="utf-8")

    novo_html, qtd_cards, qtd_rotulos = aplicar_apenas_nos_10_cards(conteudo)
    novo_html, script_i18n_ok = garantir_script_10_cards(novo_html)
    novo_html, script_cam_ok = garantir_controle_camera_sob_demanda(novo_html)

    if qtd_rotulos > 0 or script_i18n_ok or script_cam_ok:
        INDEX_HTML.write_text(novo_html, encoding="utf-8")
        print(f"[OK] Backup salvo em            : {backup}")
        print(f"[OK] Escopo aplicado             : Cards (analisados: {qtd_cards}) + Barra/Menu/Telemetria/Rodapé")
        print(f"[OK] Rótulos marcados            : {qtd_rotulos}")
        print(f"[OK] Script PT/EN                : {'Atualizado/Adicionado' if script_i18n_ok else 'Já presente'}")
        print(f"[OK] Controle câmera sob demanda: {'Atualizado/Adicionado' if script_cam_ok else 'Já presente'}")
    else:
        print(f"[INFO] Nenhuma alteração nova necessária. Backup: {backup}")


if __name__ == "__main__":
    executar()