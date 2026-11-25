import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
Auditor de diagnostico e metrica objetiva de seguranca (security/ e storage/).
"""

import ast
import json
import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SUSPECT_SECRET_NAMES = re.compile(
    r"(secret|password|senha|api_key|apikey|token|private_key|master_key)",
    re.IGNORECASE,
)

NON_ASCII_RE = re.compile(r"[^\x00-\x7F]")


def _is_security_file(rel_path: str) -> bool:
    norm = rel_path.replace("\\", "/").lstrip("./")
    return norm == "security" or norm.startswith("security/")


def _auditar_arquivo_python(raiz: Path, arquivo: Path) -> list[dict[str, Any]]:
    rel_path = str(arquivo.relative_to(raiz)).replace("\\", "/")
    achados: list[dict[str, Any]] = []
    falha_seguranca_ou_codigo = False

    try:
        raw_text = arquivo.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            raw_text = arquivo.read_text(encoding="latin-1")
            falha_seguranca_ou_codigo = True
            achados.append({
                "arquivo": rel_path,
                "status": "ATENCAO",
                "risco": "MEDIO",
                "categoria_achado": "ENCODING",
                "detalhe": "Arquivo nao esta em UTF-8 puro (requereu fallback latin-1).",
            })
        except OSError as exc:
            achados.append({
                "arquivo": rel_path,
                "status": "ERRADO",
                "risco": "ALTO",
                "categoria_achado": "IO_LEITURA",
                "detalhe": f"Falha de leitura do arquivo: {exc}",
            })
            return achados
    except OSError as exc:
        achados.append({
            "arquivo": rel_path,
            "status": "ERRADO",
            "risco": "ALTO",
            "categoria_achado": "IO_LEITURA",
            "detalhe": f"Falha de leitura do arquivo: {exc}",
        })
        return achados

    # 1. Sintaxe AST
    try:
        tree = ast.parse(raw_text, filename=rel_path)
    except SyntaxError as exc:
        achados.append({
            "arquivo": rel_path,
            "status": "ERRADO",
            "risco": "CRITICO",
            "categoria_achado": "SINTAXE",
            "detalhe": f"Erro de sintaxe na linha {exc.lineno}: {exc.msg}",
        })
        return achados

    # 2. Caracteres nao-ASCII (observacao de portabilidade em UTF-8; nao reprova sozinho)
    linhas_non_ascii = [
        idx + 1
        for idx, linha in enumerate(raw_text.splitlines())
        if NON_ASCII_RE.search(linha)
    ]
    if linhas_non_ascii:
        preview_linhas = ", ".join(str(n) for n in linhas_non_ascii[:6])
        achados.append({
            "arquivo": rel_path,
            "status": "OBSERVACAO",
            "risco": "INFORMATIVO",
            "categoria_achado": "NAO_ASCII_UTF8",
            "detalhe": f"Contem caracteres nao-ASCII em UTF-8 ({len(linhas_non_ascii)} linha(s), ex.: {preview_linhas}).",
        })

    # 3. Analise AST: except amplo e possiveis literais sensiveis
    except_generico_linhas: list[int] = []
    possiveis_segredos_linhas: list[int] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None or (
                isinstance(node.type, ast.Name) and node.type.id == "Exception"
            ):
                except_generico_linhas.append(node.lineno)

        elif isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                valor = node.value.value.strip()
                if len(valor) >= 8 and not valor.startswith(("${", "ENV_", "http")):
                    nomes = [
                        t.id for t in node.targets if isinstance(t, ast.Name)
                    ]
                    if any(SUSPECT_SECRET_NAMES.search(n) for n in nomes):
                        possiveis_segredos_linhas.append(node.lineno)

    if except_generico_linhas:
        falha_seguranca_ou_codigo = True
        achados.append({
            "arquivo": rel_path,
            "status": "ATENCAO",
            "risco": "MEDIO",
            "categoria_achado": "EXCECAO_AMPLA",
            "detalhe": f"Uso de 'except Exception' ou bare except nas linhas: {except_generico_linhas[:8]}.",
        })

    if possiveis_segredos_linhas:
        falha_seguranca_ou_codigo = True
        achados.append({
            "arquivo": rel_path,
            "status": "ATENCAO",
            "risco": "ALTO",
            "categoria_achado": "LITERAL_SENSIVEL",
            "detalhe": f"Atribuicao literal com nome sensivel nas linhas: {possiveis_segredos_linhas[:8]}.",
        })

    if not falha_seguranca_ou_codigo:
        achados.append({
            "arquivo": rel_path,
            "status": "CERTO",
            "risco": "BAIXO",
            "categoria_achado": "CONFORME",
            "detalhe": "Sintaxe valida, sem excecoes amplas ou literais sensiveis detectados.",
        })

    return achados


def _auditar_bancos_sqlite(raiz: Path) -> list[dict[str, Any]]:
    resultados_db: list[dict[str, Any]] = []
    pasta_storage = raiz / "storage"

    if not pasta_storage.exists():
        return resultados_db

    for db_file in sorted(pasta_storage.rglob("*.db")):
        rel_path = str(db_file.relative_to(raiz)).replace("\\", "/")
        try:
            conn = sqlite3.connect(f"file:{db_file}?mode=ro", uri=True, timeout=5.0)
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                )
                tabelas = [row[0] for row in cur.fetchall()]
            finally:
                conn.close()

            if not tabelas:
                resultados_db.append({
                    "banco": rel_path,
                    "situacao": "ATENCAO",
                    "risco": "MEDIO - Banco vazio (0 tabelas)",
                    "tabelas": [],
                })
            else:
                resultados_db.append({
                    "banco": rel_path,
                    "situacao": "CERTO",
                    "risco": "BAIXO - Banco acessivel e estruturado",
                    "tabelas": tabelas,
                })
        except sqlite3.Error as exc:
            resultados_db.append({
                "banco": rel_path,
                "situacao": "ERRADO",
                "risco": f"ALTO - Falha ao abrir SQLite: {exc}",
                "tabelas": [],
            })

    return resultados_db


def gerar_resumo_security(itens_python: list[dict[str, Any]]) -> dict[str, Any]:
    sec_itens = [
        item for item in itens_python if _is_security_file(str(item.get("arquivo", "")))
    ]

    certos = [i for i in sec_itens if i.get("status") == "CERTO"]
    atencao = [i for i in sec_itens if i.get("status") == "ATENCAO"]
    observacoes = [i for i in sec_itens if i.get("status") == "OBSERVACAO"]
    errados = [i for i in sec_itens if i.get("status") == "ERRADO"]

    altos_ou_criticos = [
        i for i in (errados + atencao) if i.get("risco") in {"ALTO", "CRITICO"}
    ]
    medios = [i for i in atencao if i.get("risco") == "MEDIO"]

    # Base de avaliacao de conformidade = CERTO + ATENCAO + ERRADO (exclui OBSERVACAO informativa)
    base_avaliada = len(certos) + len(atencao) + len(errados)
    if base_avaliada == 0:
        indice = 0.0
        categoria = "SEM DADOS AVALIADOS DE SECURITY"
    else:
        indice = round((len(certos) / base_avaliada) * 100, 1)

        if len(errados) > 0 or len(altos_ou_criticos) > 0:
            categoria = "REQUER REPARACAO / RISCO ALTO OU FALHA"
        elif len(medios) == 0 and indice == 100.0:
            categoria = "CONFORME / AUDITAVEL"
        elif indice >= 70.0:
            categoria = "ATENCAO MODERADA / ENDURECIMENTO NECESSARIO"
        else:
            categoria = "FRÁGIL / REVISAO PRIORITARIA"

    return {
        "total_achados_security": len(sec_itens),
        "base_avaliada_conformidade": base_avaliada,
        "indice_conformidade": indice,
        "categoria_seguranca": categoria,
        "contagem": {
            "certo": len(certos),
            "atencao": len(atencao),
            "reparacao": len(errados),
            "observacao_nao_ascii": len(observacoes),
            "risco_medio": len(medios),
            "risco_alto_ou_critico": len(altos_ou_criticos),
        },
        "certo": certos,
        "pontos_de_atencao": atencao,
        "onde_precisa_reparacao": errados,
        "observacoes_utf8": observacoes,
    }


def imprimir_metrica_security(resumo: dict[str, Any]) -> None:
    cont = resumo["contagem"]
    logger.info("\n" + "=" * 72)
    logger.info("METRICA FINAL - CATEGORIA E DIAGNOSTICO OBJETIVO DE SECURITY")
    logger.info("=" * 72)
    logger.info(f"Categoria de Seguranca : {resumo['categoria_seguranca']}")
    logger.info(
        f"Indice de Conformidade : {resumo['indice_conformidade']}% "
        f"({cont['certo']}/{resumo['base_avaliada_conformidade']} itens avaliados sem falha/excecao ampla)"
    )
    logger.info(
        f"Achados de Risco       : REPARACAO={cont['reparacao']} | "
        f"RISCO_ALTO_CRITICO={cont['risco_alto_ou_critico']} | "
        f"RISCO_MEDIO={cont['risco_medio']} | OBS_UTF8={cont['observacao_nao_ascii']}"
    )

    logger.info("\n[O QUE ESTA CERTO]")
    if resumo["certo"]:
        for item in resumo["certo"]:
            logger.info(f"  - {item['arquivo']}: {item['detalhe']}")
    else:
        logger.info("  - Nenhum item classificado como CERTO.")

    logger.info("\n[PONTOS DE ATENCAO - EXCECOES AMPLAS / LITERAIS / ENCODING]")
    if resumo["pontos_de_atencao"]:
        for item in resumo["pontos_de_atencao"]:
            logger.info(f"  - {item['arquivo']} [{item['risco']} / {item['categoria_achado']}]: {item['detalhe']}")
    else:
        logger.info("  - Nenhum ponto de atencao.")

    logger.info("\n[ONDE PRECISA DE REPARACAO]")
    if resumo["onde_precisa_reparacao"]:
        for item in resumo["onde_precisa_reparacao"]:
            logger.info(f"  - {item['arquivo']} [{item['risco']} / {item['categoria_achado']}]: {item['detalhe']}")
    else:
        logger.info("  - Nenhum item exigindo reparacao imediata.")

    logger.info("\n[OBSERVACOES INFORMATIVAS - CARACTERES NAO-ASCII EM UTF-8]")
    logger.info(f"  - Total de arquivos com caracteres nao-ASCII em UTF-8: {cont['observacao_nao_ascii']} (nao penaliza a nota de conformidade).")
    logger.info("=" * 72)


def executar_auditoria(raiz_projeto: Path) -> dict[str, Any]:
    pastas_ignorar = {"__pycache__", ".git", ".venv", "venv", "env", "node_modules"}
    itens_python: list[dict[str, Any]] = []

    for dirpath, dirnames, filenames in os.walk(raiz_projeto):
        dirnames[:] = [d for d in dirnames if d not in pastas_ignorar]
        for fname in sorted(filenames):
            if fname.endswith(".py"):
                caminho_py = Path(dirpath) / fname
                itens_python.extend(_auditar_arquivo_python(raiz_projeto, caminho_py))

    bancos = _auditar_bancos_sqlite(raiz_projeto)

    # Conta apenas itens avaliados (exclui OBSERVACAO informativa da contagem de ATENCAO)
    errado_geral = sum(1 for i in itens_python if i["status"] == "ERRADO") + sum(
        1 for b in bancos if b["situacao"] == "ERRADO"
    )
    atencao_geral = sum(1 for i in itens_python if i["status"] == "ATENCAO") + sum(
        1 for b in bancos if b["situacao"] == "ATENCAO"
    )
    certo_geral = sum(1 for i in itens_python if i["status"] == "CERTO") + sum(
        1 for b in bancos if b["situacao"] == "CERTO"
    )

    for b in bancos:
        logger.info(f"BANCO: {b['banco']}")
        logger.info(f"  SITUACAO : {b['situacao']}")
        logger.info(f"  RISCO    : {b['risco']}")
        if b["tabelas"]:
            logger.info(f"  - Tabelas: {', '.join(b['tabelas'])}")
        else:
            logger.info("  - Sem tabelas criadas.")

    logger.info("\nRESUMO FINAL")
    logger.info(f"  ERRADO  : {errado_geral}")
    logger.info(f"  ATENCAO : {atencao_geral}")
    logger.info(f"  CERTO   : {certo_geral}")

    resumo_security = gerar_resumo_security(itens_python)
    imprimir_metrica_security(resumo_security)

    relatorio = {
        "gerado_em_utc": datetime.now(timezone.utc).isoformat(),
        "raiz": str(raiz_projeto),
        "resumo_geral": {
            "ERRADO": errado_geral,
            "ATENCAO": atencao_geral,
            "CERTO": certo_geral,
        },
        "bancos_sqlite": bancos,
        "itens_python": itens_python,
        "metrica_security": resumo_security,
    }

    saida_json = raiz_projeto / "diagnostico_modulos_ttc.json"
    saida_json.write_text(
        json.dumps(relatorio, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    logger.info(f"\nResumo exato salvo em: {saida_json.name}")
    return relatorio


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parent
    executar_auditoria(raiz)