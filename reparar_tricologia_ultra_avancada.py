# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
Script reparador cirurgico para integrar o cruzamento com memoria_comum
no tricologia_ultra_avancada.py sem necessidade de colar o arquivo inteiro.
===========================================================================
"""

import argparse
import re
import shutil
from pathlib import Path
from typing import Optional


MARCADOR_HELPERS = "# === [REPARADOR TTC] PONTE LEITURA MEMORIA TRICOLOGIA ==="
MARCADOR_INIT = "# === [REPARADOR TTC] CRUZAMENTO MEMORIA INIT ==="


BLOCO_HELPERS = f"""
{MARCADOR_HELPERS}
MAPA_SECOES_TRICOLOGIA = {{
    "diagnostico": ("diagnostico", "diagnostico_capilar"),
    "reconstrucao": ("reconstrucao", "protocolo_reconstrucao"),
    "plasma_fadiga": ("plasma_fadiga", "protocolo_plasma_fadiga"),
    "queda": ("queda", "queda_capilar", "detector_queda_capilar"),
    "fibra": ("fibra", "fibra_capilar"),
    "minerais_impurezas": ("minerais_impurezas", "minerais_impurezas_quelacao"),
    "eletricidade_volume": ("eletricidade_volume", "eletricidade_volume_densidade"),
    "projecao_clima_rosto": ("projecao_clima_rosto", "clima_rosto_couro_projecao"),
    "cronograma": ("cronograma", "cronograma_capilar"),
}}


def _ttc_extrair_numero(valor):
    if valor is None or isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        num = float(valor)
        return num if np.isfinite(num) else None
    if isinstance(valor, str):
        match = re.search(r"-?\\d+(?:[\\.,]\\d+)?", valor.strip())
        if match:
            try:
                num = float(match.group(0).replace(",", "."))
                return num if np.isfinite(num) else None
            except ValueError:
                return None
    return None


def _ttc_buscar_numero(d, chaves):
    if not isinstance(d, dict):
        return None
    for chave in chaves:
        if chave in d:
            num = _ttc_extrair_numero(d[chave])
            if num is not None:
                return num
    for sub in d.values():
        if isinstance(sub, dict):
            num = _ttc_buscar_numero(sub, chaves)
            if num is not None:
                return num
    return None


def puxar_dados_tricologia_memoria(cliente=None, dados_iniciais=None, memoria_instancia=None):
    mem_alvo = memoria_instancia if memoria_instancia is not None else memoria
    dossie = dict(dados_iniciais) if isinstance(dados_iniciais, dict) else {{}}
    secoes_saida = dict(dossie["secoes"]) if isinstance(dossie.get("secoes"), dict) else {{}}

    for caminho_helper in (
        "core.tricologia_saude.memoria_tricologia_helper",
        "tricologia_saude.memoria_tricologia_helper",
        "memoria_tricologia_helper",
    ):
        try:
            mod_helper = __import__(caminho_helper, fromlist=["ler_dossie_tricologia_memoria"])
            fn_ler = getattr(mod_helper, "ler_dossie_tricologia_memoria", None)
            if callable(fn_ler):
                lido = fn_ler(cliente=cliente, memoria_instancia=mem_alvo)
                if isinstance(lido, dict):
                    if lido.get("cliente") and not dossie.get("cliente"):
                        dossie["cliente"] = lido["cliente"]
                    if lido.get("atualizado_em_utc"):
                        dossie["atualizado_em_utc"] = lido["atualizado_em_utc"]
                    if isinstance(lido.get("secoes"), dict):
                        secoes_saida.update(lido["secoes"])
                    for k, v in lido.items():
                        if k not in {{"secoes", "cliente", "atualizado_em_utc"}} and isinstance(v, dict):
                            dossie[k] = v
                break
        except Exception:
            continue

    if mem_alvo is not None and hasattr(mem_alvo, "ler_dados"):
        try:
            consolidado_raw = mem_alvo.ler_dados("tricologia_dossie_consolidado")
            if isinstance(consolidado_raw, dict):
                if consolidado_raw.get("cliente") and not dossie.get("cliente"):
                    dossie["cliente"] = consolidado_raw["cliente"]
                if isinstance(consolidado_raw.get("secoes"), dict):
                    for chave_sec, valor_sec in consolidado_raw["secoes"].items():
                        if isinstance(valor_sec, dict) and chave_sec not in secoes_saida:
                            secoes_saida[chave_sec] = valor_sec
        except Exception:
            pass

        for chave_canonica, aliases in MAPA_SECOES_TRICOLOGIA.items():
            if chave_canonica in secoes_saida and isinstance(secoes_saida[chave_canonica], dict):
                continue
            for alias in aliases:
                candidato = None
                try:
                    if cliente:
                        candidato = mem_alvo.ler_dados(f"tricologia_{{alias}}_{{cliente}}")
                    if candidato is None:
                        candidato = mem_alvo.ler_dados(f"tricologia_{{alias}}")
                except Exception:
                    candidato = None
                if isinstance(candidato, dict):
                    secoes_saida[chave_canonica] = candidato
                    break

    for chave_canonica, valor_sec in secoes_saida.items():
        if isinstance(valor_sec, dict):
            dossie[chave_canonica] = valor_sec

    dossie["secoes"] = secoes_saida
    if cliente:
        dossie["cliente"] = cliente
    elif not dossie.get("cliente"):
        dossie["cliente"] = "Cliente UHNW"
    return dossie
# === [/REPARADOR TTC] PONTE LEITURA MEMORIA TRICOLOGIA ===
"""


BLOCO_INIT = f"""
        {MARCADOR_INIT}
        _cliente_mem_alvo = ceo_name or self.telemetria_externa.get("nome_cliente") or self.telemetria_externa.get("nome")
        self.dossie_memoria = puxar_dados_tricologia_memoria(
            cliente=_cliente_mem_alvo,
            dados_iniciais=self.telemetria_externa,
            memoria_instancia=memoria,
        )
        _secoes_mem = self.dossie_memoria.get("secoes") if isinstance(self.dossie_memoria.get("secoes"), dict) else {{}}
        if not ceo_name and not self.telemetria_externa.get("nome_cliente") and not self.telemetria_externa.get("nome"):
            if self.dossie_memoria.get("cliente") and self.dossie_memoria.get("cliente") != "Cliente UHNW":
                self.ceo = self.dossie_memoria["cliente"]
        _dens_mem = _ttc_buscar_numero(_secoes_mem, ("densidade_fios_estimada", "densidade_fios", "densidade_cm2", "densidade"))
        _mini_mem = _ttc_buscar_numero(_secoes_mem, ("miniaturizacao_pct", "taxa_miniaturizacao", "miniaturizacao"))
        _umid_mem = _ttc_buscar_numero(_secoes_mem, ("umidade_ar_pct", "umidade_ar", "umidade_relativa", "umidade"))
        _temp_mem = _ttc_buscar_numero(_secoes_mem, ("temp_externa_c", "temperatura_externa", "temperatura_c", "temperatura"))
        if _dens_mem is not None and abs(self.densidade_fios - 130.0) < 1e-6:
            self.densidade_fios = float(_dens_mem)
        if _mini_mem is not None and abs(self.miniaturizacao - 22.5) < 1e-6:
            self.miniaturizacao = max(0.0, float(_mini_mem))
        if _umid_mem is not None and abs(self.umidade_ar - 85.0) < 1e-6:
            self.umidade_ar = max(0.0, min(100.0, float(_umid_mem)))
        if _temp_mem is not None and abs(self.temp_externa - 32.0) < 1e-6:
            self.temp_externa = float(_temp_mem)
        if not self.analise_llm and _secoes_mem:
            _linhas_sec = []
            for _nsec, _csec in _secoes_mem.items():
                if isinstance(_csec, dict) and _csec:
                    _itens = [f"{{k}}: {{v}}" for k, v in list(_csec.items())[:4] if v is not None and v != ""]
                    if _itens:
                        _linhas_sec.append(f"• {{_nsec}}: " + " | ".join(_itens))
            if _linhas_sec:
                self.analise_llm = "\\n".join(_linhas_sec)
        # === [/REPARADOR TTC] CRUZAMENTO MEMORIA INIT ===
"""


def _localizar_arquivo_alvo(caminho_informado: Optional[str]) -> Optional[Path]:
    if caminho_informado:
        p = Path(caminho_informado).resolve()
        return p if p.exists() else None

    raiz = Path(__file__).resolve().parent
    candidatos = [
        raiz / "core" / "tricologia_saude" / "tricologia_ultra_avancada.py",
        raiz / "core" / "tricologia_ultra_avancada.py",
        raiz / "tricologia_ultra_avancada.py",
        raiz.parent / "core" / "tricologia_saude" / "tricologia_ultra_avancada.py",
    ]
    for c in candidatos:
        if c.exists():
            return c.resolve()
    return None


def reparar_conteudo(conteudo: str) -> tuple[str, bool]:
    alterado = False
    texto = conteudo

    if MARCADOR_HELPERS not in texto:
        alvo_ancora = "TEXTOS_TRICOLOGIA = {"
        if alvo_ancora in texto:
            texto = texto.replace(alvo_ancora, BLOCO_HELPERS + "\n\n" + alvo_ancora, 1)
            alterado = True

    if MARCADOR_INIT not in texto:
        padrao_fim_init = re.compile(
            r"(class C2UltraAdvancedTrichologyEngine:[\s\S]*?def __init__[\s\S]*?)(\n    def formatar_moeda_eur)",
            re.MULTILINE,
        )
        match = padrao_fim_init.search(texto)
        if match:
            texto = texto[: match.start(2)] + BLOCO_INIT + texto[match.start(2) :]
            alterado = True

    return texto, alterado


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Repara e integra a leitura da memoria_comum no tricologia_ultra_avancada.py."
    )
    parser.add_argument("--arquivo", type=str, default=None, help="Caminho para tricologia_ultra_avancada.py")
    parser.add_argument("--aplicar", action="store_true", help="Grava as alterações no arquivo.")
    args = parser.parse_args()

    alvo = _localizar_arquivo_alvo(args.arquivo)
    if alvo is None:
        print("[ERRO] Não foi possível localizar tricologia_ultra_avancada.py automaticamente. Use --arquivo.")
        return

    original = alvo.read_text(encoding="utf-8")
    reparado, alterado = reparar_conteudo(original)

    if not alterado:
        print(f"[OK] Nenhuma alteração pendente em {alvo} (já reparado ou âncoras não encontradas).")
        return

    if not args.aplicar:
        print(f"[SIMULAÇÃO] Reparo previsto para: {alvo}")
        print(f"  Tamanho original: {len(original)} chars -> reparado: {len(reparado)} chars")
        print("  Rode com '--aplicar' para criar o backup (.bak) e salvar.")
        return

    backup = alvo.with_suffix(alvo.suffix + ".bak")
    shutil.copy2(alvo, backup)
    alvo.write_text(reparado, encoding="utf-8")
    print(f"[APLICADO] Backup salvo em: {backup}")
    print(f"[APLICADO] Arquivo atualizado: {alvo}")


if __name__ == "__main__":
    main()