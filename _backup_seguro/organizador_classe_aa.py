# -*- coding: utf-8 -*-
"""
Script: organizador_classe_aa.py
Finalidade: Diagnostica e organiza o inventário/arquitetura do sistema de forma
            segura e não-destrutiva (dry-run por padrão, backup automático ao
            aplicar, classificação por papel, detecção de duplicatas/backups e
            relatório claro no terminal).
"""

import argparse
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from typing import Any, Dict, List, Set

PASTAS_IGNORADAS: Set[str] = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    "_backups_central",
    "_central_dados",
    "_organizador_aa",
    "_reserva_segura",
    "_cofre_recuperacao_zerados",
}

EXTENSOES_TEXTO: Set[str] = {
    ".py",
    ".html",
    ".css",
    ".js",
    ".json",
    ".md",
    ".txt",
}


def sha256_arquivo(caminho: str) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        while True:
            bloco = f.read(65536)
            if not bloco:
                break
            h.update(bloco)
    return h.hexdigest()


def classificar_papel(rel_path: str, nome: str) -> str:
    r = rel_path.lower()
    n = nome.lower()

    if any(k in n for k in (".bak", "backup", "copia", "cópia", "_old", "_zerad")):
        return "backup_ou_copia_legada"
    if "contrato" in n or "dossie" in n or "advogado" in n or "legal/" in r or "jurid" in r:
        return "juridico_e_dossies"
    if r.endswith(".pdf"):
        return "documentos_pdf"
    if r.endswith((".html", ".css", ".js")):
        return "interface_web_ui"
    if r.endswith(".json"):
        if any(k in n for k in ("enclave", "jurisd", "pais", "país", "geo", "us-", "br.", "mc.")):
            return "dados_jurisdicoes_enclaves"
        return "dados_e_configuracoes"
    if r.endswith(".py"):
        if any(k in n for k in ("auditor", "central", "organizador", "gerar_", "diagnost", "investigar")):
            return "ferramentas_auditoria_e_automacao"
        return "nucleo_e_modulos_python"
    return "outros_arquivos"


def escanear_sistema(raiz: str) -> List[Dict[str, Any]]:
    itens: List[Dict[str, Any]] = []
    for atual, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]
        for nome in sorted(arquivos):
            caminho = os.path.join(atual, nome)
            if not os.path.isfile(caminho):
                continue
            rel = os.path.relpath(caminho, raiz).replace("\\", "/")
            ext = os.path.splitext(nome)[1].lower() or "(sem_ext)"
            try:
                st = os.stat(caminho)
                linhas = 0
                if ext in EXTENSOES_TEXTO:
                    with open(caminho, "r", encoding="utf-8", errors="replace") as ft:
                        linhas = sum(1 for _ in ft)
                digest = sha256_arquivo(caminho)
                itens.append(
                    {
                        "arquivo": rel,
                        "nome": nome,
                        "extensao": ext,
                        "papel": classificar_papel(rel, nome),
                        "tamanho_bytes": st.st_size,
                        "linhas": linhas,
                        "sha256": digest,
                    }
                )
            except OSError as exc:
                itens.append(
                    {
                        "arquivo": rel,
                        "nome": nome,
                        "extensao": ext,
                        "papel": "erro_leitura",
                        "tamanho_bytes": 0,
                        "linhas": 0,
                        "sha256": "ERRO",
                        "erro": str(exc),
                    }
                )
    return itens


def detectar_duplicatas_exatas(itens: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    por_hash: Dict[str, List[str]] = {}
    for it in itens:
        h = it.get("sha256", "")
        if h and h != "ERRO":
            por_hash.setdefault(h, []).append(it["arquivo"])
    return {h: paths for h, paths in por_hash.items() if len(paths) > 1}


def fazer_backup_seguro(raiz: str, destino_base: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    pasta_bk = os.path.join(destino_base, "backups", f"snap_{ts}")
    os.makedirs(pasta_bk, exist_ok=True)

    for atual, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]
        for nome in sorted(arquivos):
            orig = os.path.join(atual, nome)
            if not os.path.isfile(orig):
                continue
            rel = os.path.relpath(orig, raiz)
            alvo = os.path.join(pasta_bk, rel)
            os.makedirs(os.path.dirname(alvo), exist_ok=True)
            shutil.copy2(orig, alvo)
    return pasta_bk


def executar_organizador(raiz: str, aplicar: bool) -> None:
    itens = escanear_sistema(raiz)
    duplicatas = detectar_duplicatas_exatas(itens)

    contagem_papel: Dict[str, int] = {}
    total_linhas = 0
    for it in itens:
        papel = it["papel"]
        contagem_papel[papel] = contagem_papel.get(papel, 0) + 1
        total_linhas += int(it.get("linhas", 0))

    legados = [it["arquivo"] for it in itens if it["papel"] == "backup_ou_copia_legada"]

    print("=" * 74)
    print("ORGANIZADOR CLASSE AA — DIAGNÓSTICO E ESTRUTURAÇÃO SEGURA")
    print("=" * 74)
    print(f"Raiz inspecionada : {raiz}")
    print(f"Modo de execução : {'APLICAR (com backup)' if aplicar else 'SIMULAÇÃO / DRY-RUN (nada alterado)'}")
    print(f"Arquivos auditados : {len(itens)} | Total de linhas (texto): {total_linhas}")
    print(f"Hashes duplicados: {len(duplicatas)} grupos | Arquivos .bak/legados: {len(legados)}")
    print("-" * 74)
    print("CLASSIFICAÇÃO POR PAPEL:")
    for papel, qtd in sorted(contagem_papel.items(), key=lambda x: (-x[1], x[0])):
        print(f"  • {papel:<34}: {qtd}")

    if duplicatas:
        print("-" * 74)
        print("ARQUIVOS COM CONTEÚDO IDÊNTICO (MESMO SHA-256):")
        for _, paths in list(duplicatas.items())[:15]:
            print("  - " + "  ==  ".join(paths))

    if legados:
        print("-" * 74)
        print("CÓPIAS / .BAK / ARQUIVOS LEGADOS DETECTADOS:")
        for lg in legados[:15]:
            print(f"  - {lg}")

    if aplicar:
        pasta_org = os.path.join(raiz, "_organizador_aa")
        os.makedirs(pasta_org, exist_ok=True)
        bk_dir = fazer_backup_seguro(raiz, pasta_org)

        mapa_path = os.path.join(pasta_org, "mapa_sistema_aa.json")
        payload = {
            "gerado_em_utc": datetime.now(timezone.utc).isoformat(),
            "raiz": raiz,
            "backup_snapshot": bk_dir,
            "total_arquivos": len(itens),
            "total_linhas_texto": total_linhas,
            "resumo_por_papel": contagem_papel,
            "grupos_duplicados_sha256": duplicatas,
            "arquivos_legados_ou_bak": legados,
            "inventario_completo": itens,
        }
        with open(mapa_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        print("-" * 74)
        print(f"Backup criado em : {bk_dir}")
        print(f"Mapa salvo em    : {mapa_path}")
    else:
        print("-" * 74)
        print("Dica: para gerar o backup e salvar o mapa JSON sem mover seus códigos,")
        print("rode: python organizador_classe_aa.py --aplicar")
    print("=" * 74)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organizador seguro do sistema (padrão classe AA).")
    parser.add_argument(
        "--aplicar",
        action="store_true",
        help="Cria backup de segurança e grava o mapa estruturado em _organizador_aa/mapa_sistema_aa.json.",
    )
    args = parser.parse_args()
    raiz_atual = os.path.abspath(os.path.dirname(__file__))
    executar_organizador(raiz_atual, aplicar=bool(args.aplicar))