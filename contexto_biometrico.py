# -*- coding: utf-8 -*-
from typing import Any


def _para_float(valor: Any, padrao: float = 0.0) -> float:
    if valor is None:
        return padrao
    try:
        return float(valor)
    except (TypeError, ValueError):
        return padrao


def _para_int(valor: Any, padrao: int = 0) -> int:
    if valor is None:
        return padrao
    try:
        return int(float(valor))
    except (TypeError, ValueError):
        return padrao


def _ler_motor_atual(memoria_global: Any) -> dict[str, Any]:
    if memoria_global is None:
        return {}
    if hasattr(memoria_global, "obter_dados"):
        dados = memoria_global.obter_dados("motor_biometrico_atual")
        return dados if isinstance(dados, dict) else {}
    if isinstance(memoria_global, dict):
        dados = memoria_global.get("motor_biometrico_atual")
        return dados if isinstance(dados, dict) else {}
    return {}


def _pegar_horizonte(mapa: dict[Any, Any], chave_str: str, chave_int: int) -> dict[str, Any]:
    if chave_str in mapa and mapa[chave_str] is not None:
        item = mapa[chave_str]
    elif chave_int in mapa and mapa[chave_int] is not None:
        item = mapa[chave_int]
    else:
        item = None
    return item if isinstance(item, dict) else {}


def montar_contexto_biometrico(memoria_global: Any) -> str:
    """Extrai métricas reais do motor biométrico e monta o bloco para injeção no prompt."""
    dados = _ler_motor_atual(memoria_global)
    phi_global = _para_float(dados.get("phi_global"), 0.0)

    if not dados or not dados.get("face_detectada") or phi_global <= 0.0:
        raise ValueError("Motor biométrico sem dados válidos na memoria_global.")

    proj_bruto = dados.get("projecoes_anos")
    proj: dict[Any, Any] = proj_bruto if isinstance(proj_bruto, dict) else {}

    pele_bruto = dados.get("metricas_pele")
    pele_nested: dict[str, Any] = pele_bruto if isinstance(pele_bruto, dict) else {}

    extras_bruto = dados.get("metricas_avancadas")
    extras: dict[str, Any] = extras_bruto if isinstance(extras_bruto, dict) else {}

    p5 = _pegar_horizonte(proj, "5_anos", 5)
    p10 = _pegar_horizonte(proj, "10_anos", 10)
    p15 = _pegar_horizonte(proj, "15_anos", 15)

    refletancia = _para_float(
        dados.get("refletancia_pele")
        if dados.get("refletancia_pele") is not None
        else pele_nested.get("refletancia"),
        0.0,
    )
    agua_estimada = _para_float(
        dados.get("agua_estimada")
        if dados.get("agua_estimada") is not None
        else pele_nested.get("agua_estimada"),
        0.0,
    )
    agua_necessaria_ml = _para_int(
        dados.get("agua_necessaria_ml")
        if dados.get("agua_necessaria_ml") is not None
        else pele_nested.get("agua_necessaria_ml"),
        0,
    )
    indice_hidratacao = _para_float(
        extras.get("indice_hidratacao")
        if extras.get("indice_hidratacao") is not None
        else pele_nested.get("indice_hidratacao"),
        0.0,
    )
    variancia_tonal = _para_float(
        extras.get("variancia_tonal")
        if extras.get("variancia_tonal") is not None
        else pele_nested.get("variancia_tonal"),
        0.0,
    )
    total_pontos = _para_int(dados.get("total_pontos"), 100380)

    queda_5 = _para_float(p5.get("dist_descolamento_mm"), 0.0)
    grau_5 = _para_float(p5.get("grau_envelhecimento"), 0.0)

    queda_10 = _para_float(p10.get("dist_descolamento_mm"), 0.0)
    grau_10 = _para_float(p10.get("grau_envelhecimento"), 0.0)

    queda_15 = _para_float(p15.get("dist_descolamento_mm"), 0.0)
    grau_15 = _para_float(p15.get("grau_envelhecimento"), 0.0)

    return f"""
DADOS DO MOTOR BIOMÉTRICO (MODELO PARAMÉTRICO - MALHA {total_pontos:,} PONTOS):
- Proporção Áurea Global (Phi): {phi_global:.3f}
- Espectrofotometria HSV (Ponto 117):
  * Refletância: {refletancia:.1f}%
  * Água Estimada: {agua_estimada:.1f}% | Reposição Sugerida: {agua_necessaria_ml} mL
  * Índice de Hidratação: {indice_hidratacao:.2f} | Variância Tonal: {variancia_tonal:.2f}

PROJEÇÕES GRAVITACIONAIS SIMULADAS (Escala 0.12 mm/px):
- 5 Anos: Queda {queda_5:.2f} mm | Grau Envelhecimento: {grau_5:.1f}/10
- 10 Anos: Queda {queda_10:.2f} mm | Grau Envelhecimento: {grau_10:.1f}/10
- 15 Anos: Queda {queda_15:.2f} mm | Grau Envelhecimento: {grau_15:.1f}/10

INSTRUÇÃO OBRIGATÓRIA:
Redija o dossiê utilizando exatamente os valores numéricos acima. Não invente medições adicionais nem crie placeholders. Apresente todos os resultados explicitamente como projeções de simulação paramétrica computacional (não diagnóstico médico ou clínico).
""".strip()