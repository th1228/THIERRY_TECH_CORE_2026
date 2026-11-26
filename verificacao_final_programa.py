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

import importlib
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = (
    os.path.abspath(os.path.join(CURRENT_DIR, ".."))
    if os.path.basename(CURRENT_DIR).lower() in ("core", "legal")
    else CURRENT_DIR
)

for _caminho in (ROOT_DIR, CURRENT_DIR):
    if _caminho and os.path.isdir(_caminho) and _caminho not in sys.path:
        sys.path.insert(0, _caminho)

MODULOS_ESSENCIAIS: List[Tuple[str, List[str]]] = [
    ("MemoriaComum", ["memoria_comum", "core.memoria_comum"]),
    ("GeradorDossiesMaster", ["gerador_dossies_master", "core.gerador_dossies_master"]),
    ("CartaInternacionalEngine", ["carta_internacional_engine", "core.carta_internacional_engine"]),
    ("C2MonacoModelingEngine", ["monaco_modelagem_engine", "core.monaco_modelagem_engine"]),
    ("C2GlobalContractEngine", ["contrato_global_engine", "legal.contrato_global_engine", "core.contrato_global_engine"]),
]


def _tentar_importar(nomes: List[str]) -> Tuple[Optional[str], Optional[Any], Optional[str]]:
    ultimo_erro = "Módulo não encontrado"
    for nome in nomes:
        try:
            mod = importlib.import_module(nome)
            return nome, mod, None
        except Exception as exc:
            ultimo_erro = f"{nome}: {exc}"
    return None, None, ultimo_erro


def _verificar_memoria() -> Tuple[bool, str]:
    _, mod, erro = _tentar_importar(["memoria_comum", "core.memoria_comum"])
    if not mod:
        return False, f"Memória comum indisponível ({erro})"

    mem = getattr(mod, "instancia_memoria", None) or getattr(mod, "memoria_global", None)
    if mem is None:
        return False, "Instância global da memória comum ausente"

    for metodo in ("salvar_dados", "ler_dados", "obter_para_destino"):
        if not hasattr(mem, metodo):
            return False, f"Método obrigatório ausente na memória: {metodo}"

    if hasattr(mem, "obter_para_destino"):
        pacote_restrito = mem.obter_para_destino("motor_4")
        if isinstance(pacote_restrito, dict):
            vazamentos = [k for k in ("analise_gemini", "analise_dermica_hsv", "secoes_dossie_json") if k in pacote_restrito]
            if vazamentos:
                return False, f"Vazamento em obter_para_destino('motor_4'): {', '.join(vazamentos)}"

    return True, "Memória comum ativa e isolando destinos"


def _verificar_isolamento_master() -> Tuple[bool, str]:
    _, mod, erro = _tentar_importar(["gerador_dossies_master", "core.gerador_dossies_master"])
    if not mod:
        return False, f"Gerador master indisponível ({erro})"

    fn_pacotes = getattr(mod, "_montar_pacotes_por_motor", None)
    if not callable(fn_pacotes):
        return False, "Função _montar_pacotes_por_motor não encontrada"

    amostra: Dict[str, Any] = {
        "nome_cliente": "Auditoria Final",
        "analise_gemini": "Texto clínico de teste",
        "analise_dermica_hsv": "Simulação paramétrica de teste",
        "secoes_dossie_json": {"diagnostico_estrutural": "Teste"},
    }
    pacotes = fn_pacotes(amostra, "PT")
    for motor_restrito in ("motor_4", "motor_5", "motor_6"):
        pct = pacotes.get(motor_restrito, {})
        for chave_proibida in ("analise_gemini", "analise_dermica_hsv", "secoes_dossie_json"):
            if chave_proibida in pct:
                return False, f"{motor_restrito} recebeu chave proibida '{chave_proibida}'"

    return True, "Isolamento de pacotes por motor validado (Motores 4, 5 e 6 limpos)"


def verificar_programa_completo() -> bool:
    print("=" * 62)
    print("VERIFICAÇÃO FINAL DO PROGRAMA - STATUS GERAL DO ECOSSISTEMA")
    print("=" * 62)

    falhas: List[str] = []
    modulos_ok = 0

    for rotulo, candidatos in MODULOS_ESSENCIAIS:
        modulo_usado, _, erro = _tentar_importar(candidatos)
        if modulo_usado:
            modulos_ok += 1
            print(f"[OK] {rotulo} -> {modulo_usado}")
        else:
            falhas.append(f"{rotulo} ({erro})")
            print(f"[FALHA] {rotulo} -> {erro}")

    mem_ok, mem_msg = _verificar_memoria()
    print(f"[{'OK' if mem_ok else 'FALHA'}] {mem_msg}")
    if not mem_ok:
        falhas.append(mem_msg)

    iso_ok, iso_msg = _verificar_isolamento_master()
    print(f"[{'OK' if iso_ok else 'FALHA'}] {iso_msg}")
    if not iso_ok:
        falhas.append(iso_msg)

    print("-" * 62)
    print(f"Módulos essenciais carregados: {modulos_ok}/{len(MODULOS_ESSENCIAIS)}")

    if not falhas:
        print("VEREDITO FINAL: PROGRAMA 100% PRONTO E OPERACIONAL.")
        print("=" * 62)
        return True

    print("VEREDITO FINAL: PENDÊNCIAS ENCONTRADAS:")
    for item in falhas:
        print(f"  - {item}")
    print("=" * 62)
    return False


if __name__ == "__main__":
    ok = verificar_programa_completo()
    sys.exit(0 if ok else 1)