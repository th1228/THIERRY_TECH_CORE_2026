# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the
intellectual property of Thierry Technology Concept Global. Unauthorized
distribution, reverse engineering, or usage without a signed NDA/License
agreement is strictly prohibited under international copyright frameworks.
===========================================================================
"""

"""
DIAGNÓSTICO DE EVOLUÇÃO LOCAL (CICLOS 5, 10 E 15 ANOS)
Registra snapshots locais a cada geração do Dossiê de Inteligência (01)
e compara a evolução entre execuções ao longo do tempo.
"""

import datetime
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_DIAGNOSTICO = BASE_DIR / "monaco_security_vault" / "diagnostico_evolucao"
PASTA_DIAGNOSTICO.mkdir(parents=True, exist_ok=True)


def _extrair_numero(valor: Any, padrao: float) -> float:
    if valor is None:
        return padrao
    if isinstance(valor, (int, float)):
        return float(valor)
    texto = str(valor).replace(",", ".")
    match = re.search(r"[-+]?\d*\.?\d+", texto)
    if match:
        try:
            return float(match.group(0))
        except ValueError:
            return padrao
    return padrao


def _slug_titular(nome: str) -> str:
    limpo = re.sub(r"[^a-zA-Z0-9_-]+", "_", (nome or "titular").strip().lower())
    return limpo.strip("_") or "titular"


def _caminho_historico(titular: str, empresa: str) -> Path:
    chave_raw = f"{titular.strip().lower()}|{empresa.strip().lower()}"
    digest = hashlib.sha256(chave_raw.encode("utf-8")).hexdigest()[:12]
    return PASTA_DIAGNOSTICO / f"evolucao_{_slug_titular(titular)}_{digest}.json"


def _projetar_ciclos(metricas: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
    """
    Projeta os ciclos de 5, 10 e 15 anos com base nos indicadores atuais
    de regeneração, densidade, idade biológica e adesão.
    """
    regeneracao_base = metricas["regeneracao_pct"]
    densidade_base = metricas["densidade_fios_cm2"]
    idade_bio_base = metricas["idade_biologica_anos"]
    adesao_base = metricas["adesao_pct"]

    fator_adesao = min(max(adesao_base / 100.0, 0.05), 0.50)
    ciclos: Dict[str, Dict[str, Any]] = {}

    for anos in (5, 10, 15):
        fator_tempo = anos / 5.0
        regeneracao_proj = round(min(99.9, regeneracao_base + (fator_tempo * 1.4 * (1.0 + fator_adesao))), 2)
        densidade_proj = round(densidade_base + (fator_tempo * 4.5 * (1.0 + fator_adesao)), 2)
        # Delta etário biológico relativo em relação ao ponto atual (negativo = preservação/rejuvenescimento)
        delta_idade_bio = round(-0.6 * fator_tempo * (1.0 + fator_adesao), 2)
        idade_bio_proj = round(max(18.0, idade_bio_base + anos + delta_idade_bio), 1)

        ciclos[f"{anos}_anos"] = {
            "horizonte_anos": anos,
            "regeneracao_projetada_pct": regeneracao_proj,
            "densidade_projetada_fios_cm2": densidade_proj,
            "idade_biologica_projetada_anos": idade_bio_proj,
            "delta_idade_biologica_vs_baseline": delta_idade_bio,
            "indice_estabilidade_ciclo": round(min(100.0, 75.0 + (fator_adesao * 40.0) - (anos * 0.4)), 2),
        }

    return ciclos


def registrar_diagnostico_evolucao(payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Registra um novo snapshot local de evolução a partir do payload do Dossiê 01
    e retorna o consolidado com comparação histórica e projeções de 5, 10 e 15 anos.
    """
    dados = dict(payload or {})
    titular = str(dados.get("titular") or dados.get("ceo_name") or dados.get("nome_cliente") or "Genilson Rodrigues").strip()
    empresa = str(dados.get("empresa") or dados.get("company_name") or "Thierry Technology Concept Global").strip()
    documento = str(dados.get("documento") or "01_Dossie_Sovereign_Intelligence").strip()

    metricas = {
        "regeneracao_pct": _extrair_numero(dados.get("regeneracao"), 92.17),
        "densidade_fios_cm2": _extrair_numero(dados.get("densidade"), 128.0),
        "idade_biologica_anos": _extrair_numero(dados.get("idade_bio"), 31.0),
        "adesao_pct": _extrair_numero(dados.get("adesao"), 18.5),
    }

    ciclos_5_10_15 = _projetar_ciclos(metricas)
    agora_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    arquivo_hist = _caminho_historico(titular, empresa)
    historico: List[Dict[str, Any]] = []
    if arquivo_hist.exists():
        try:
            conteudo_existente = json.loads(arquivo_hist.read_text(encoding="utf-8"))
            if isinstance(conteudo_existente, list):
                historico = conteudo_existente
        except (OSError, json.JSONDecodeError):
            historico = []

    snapshot_anterior = historico[-1] if historico else None
    comparativo_snapshot_anterior: Optional[Dict[str, Any]] = None

    if snapshot_anterior and isinstance(snapshot_anterior.get("metricas"), dict):
        prev_m = snapshot_anterior["metricas"]
        comparativo_snapshot_anterior = {
            "snapshot_anterior_em": snapshot_anterior.get("registrado_em_utc"),
            "delta_regeneracao_pct": round(metricas["regeneracao_pct"] - _extrair_numero(prev_m.get("regeneracao_pct"), metricas["regeneracao_pct"]), 2),
            "delta_densidade_fios_cm2": round(metricas["densidade_fios_cm2"] - _extrair_numero(prev_m.get("densidade_fios_cm2"), metricas["densidade_fios_cm2"]), 2),
            "delta_idade_biologica_anos": round(metricas["idade_biologica_anos"] - _extrair_numero(prev_m.get("idade_biologica_anos"), metricas["idade_biologica_anos"]), 2),
            "delta_adesao_pct": round(metricas["adesao_pct"] - _extrair_numero(prev_m.get("adesao_pct"), metricas["adesao_pct"]), 2),
        }

    assinatura_payload = hashlib.sha256(
        json.dumps({"titular": titular, "empresa": empresa, "metricas": metricas, "ts": agora_utc}, sort_keys=True).encode("utf-8")
    ).hexdigest()

    registro_atual: Dict[str, Any] = {
        "execucao_numero": len(historico) + 1,
        "registrado_em_utc": agora_utc,
        "titular": titular,
        "empresa": empresa,
        "documento": documento,
        "modo_operacao": "LOCAL_OFFLINE_FIRST",
        "metricas": metricas,
        "comparativo_snapshot_anterior": comparativo_snapshot_anterior,
        "projecao_ciclos": ciclos_5_10_15,
        "hash_snapshot": assinatura_payload,
    }

    historico.append(registro_atual)
    arquivo_hist.write_text(json.dumps(historico, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "status": "registrado",
        "arquivo_historico": str(arquivo_hist),
        "total_execucoes": len(historico),
        "ultimo_registro": registro_atual,
    }


def obter_evolucao_titular(titular: str, empresa: str = "Thierry Technology Concept Global") -> Dict[str, Any]:
    """Lê todo o histórico local salvo para o titular/empresa sem gerar novos snapshots."""
    arquivo_hist = _caminho_historico(titular, empresa)
    if not arquivo_hist.exists():
        return {"status": "vazio", "titular": titular, "empresa": empresa, "execucoes": []}
    try:
        historico = json.loads(arquivo_hist.read_text(encoding="utf-8"))
        if not isinstance(historico, list):
            historico = []
    except (OSError, json.JSONDecodeError):
        historico = []
    return {
        "status": "ok",
        "titular": titular,
        "empresa": empresa,
        "total_execucoes": len(historico),
        "execucoes": historico,
    }