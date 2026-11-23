# -*- coding: utf-8 -*-
"""
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
C2 MASTER AUDIT GLOBAL - SOVEREIGN INTELLIGENCE ENGINE
"""

import os
import json
import hashlib
import datetime
import importlib.util
from pathlib import Path
from typing import Any, Dict, List, Optional


def _validar_entrada(raiz_projeto: Optional[str], contexto: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """(1) Validação de entrada do motor C2 Master Audit Global."""
    caminho_base = Path(raiz_projeto).resolve() if raiz_projeto else Path(__file__).resolve().parent
    if not caminho_base.exists() or not caminho_base.is_dir():
        return {
            "valida": False,
            "erro": f"Diretorio raiz invalido ou inexistente: {caminho_base}",
            "raiz": str(caminho_base),
            "contexto": contexto if isinstance(contexto, dict) else {},
        }

    dados_ctx = contexto if isinstance(contexto, dict) else {}
    return {
        "valida": True,
        "erro": None,
        "raiz": caminho_base,
        "contexto": dados_ctx,
    }


def _carregar_motor_c2(raiz: Path) -> Optional[Any]:
    """Localiza e carrega o motor C2 se existir na pasta core ou na raiz."""
    candidatos = [
        raiz / "core" / "C2_sovereign_inteligência.py",
        raiz / "core" / "c2_sovereign_intelligence.py",
        raiz / "C2_sovereign_inteligência.py",
        raiz / "c2_sovereign_intelligence.py",
    ]
    for caminho in candidatos:
        if caminho.exists():
            spec = importlib.util.spec_from_file_location("c2_sovereign_dinamico", str(caminho))
            if spec and spec.loader:
                modulo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modulo)
                if hasattr(modulo, "C2SovereignIntelligenceEngine"):
                    return getattr(modulo, "C2SovereignIntelligenceEngine")
    return None


def _processar_rotina_principal(raiz: Path, contexto: Dict[str, Any]) -> Dict[str, Any]:
    """(2) Rotina principal de processamento do motor."""
    pastas_ignoradas = {".git", ".venv", "venv", "env", "__pycache__", ".auditor_backup"}
    total_py = 0
    total_json = 0
    for pasta_atual, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in pastas_ignoradas]
        for nome in arquivos:
            baixo = nome.lower()
            if baixo.endswith(".py"):
                total_py += 1
            elif baixo.endswith(".json"):
                total_json += 1

    motor_cls = _carregar_motor_c2(raiz)
    motor_ativo = bool(motor_cls is not None)
    timestamp_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    resumo_payload = {
        "motor": "c2_master_audit_global",
        "raiz": str(raiz),
        "total_py": total_py,
        "total_json": total_json,
        "motor_c2_disponivel": motor_ativo,
        "timestamp_utc": timestamp_utc,
        "contexto_recebido": contexto,
    }
    hash_integridade = hashlib.sha256(
        json.dumps(resumo_payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest().upper()

    return {
        "processado": True,
        "raiz": str(raiz),
        "total_arquivos_py": total_py,
        "total_arquivos_json": total_json,
        "motor_c2_disponivel": motor_ativo,
        "hash_sha256": hash_integridade,
        "timestamp_utc": timestamp_utc,
    }


def executar_motor_c2_master(
    raiz_projeto: Optional[str] = None,
    contexto: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Executa validação, rotina principal e devolve o retorno estruturado dict com status/resultado."""
    validacao = _validar_entrada(raiz_projeto, contexto)
    if not validacao["valida"]:
        return {
            "status": "ERRO_VALIDACAO",
            "resultado": {
                "valido": False,
                "detalhe": validacao["erro"],
                "raiz": validacao["raiz"],
            },
        }

    raiz: Path = validacao["raiz"]
    dados_ctx: Dict[str, Any] = validacao["contexto"]
    processamento = _processar_rotina_principal(raiz, dados_ctx)

    # (3) Retorno estruturado (dict com status / resultado)
    return {
        "status": "OK",
        "resultado": processamento,
    }


if __name__ == "__main__":
    saida = executar_motor_c2_master()
    print(json.dumps(saida, indent=2, ensure_ascii=False))