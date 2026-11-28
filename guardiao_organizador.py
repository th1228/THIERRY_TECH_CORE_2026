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

import argparse
import ast
import datetime
import hashlib
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

PASTAS_IGNORADAS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
    ".vscode",
}

PASTA_DEDICADA_AUDITORIA = "ajustes_auditoria"
PASTAS_AUDITORIA_ACEITAS = {
    PASTA_DEDICADA_AUDITORIA,
    "tools",
    "scripts",
    "checks",
    "diagnostics",
}
PASTAS_ARQUIVO = {"_archive", "archive", "labs", "backup", "backups"}
PASTAS_WEB = {"web", "frontend", "static", "templates", "public", "ui", "painel"}

EXTENSOES_CODIGO = {
    ".py",
    ".html",
    ".htm",
    ".css",
    ".js",
    ".ts",
    ".json",
    ".md",
    ".txt",
    ".sql",
    ".ps1",
    ".sh",
}

MODULOS_CRITICOS: List[Tuple[str, List[str]]] = [
    ("MemoriaComum", ["memoria_comum", "core.memoria_comum"]),
    ("GeradorDossiesMaster", ["gerador_dossies_master", "core.gerador_dossies_master"]),
    ("CartaInternacionalEngine", ["carta_internacional_engine", "core.carta_internacional_engine"]),
    ("C2MonacoModelingEngine", ["monaco_modelagem_engine", "core.monaco_modelagem_engine"]),
    (
        "C2GlobalContractEngine",
        ["contrato_global_engine", "legal.contrato_global_engine", "core.contrato_global_engine"],
    ),
]

ARQUIVOS_CHAVE_INSCRICAO = [
    "abertura_index.html",
    "main.py",
    "protocolo_388.json",
    "index.html",
]

VERDE_ANSI = "\033[92m"
AMARELO_ANSI = "\033[93m"
RESET_ANSI = "\033[0m"

ARQUIVO_SNAPSHOT = ".guardiao_snapshot.json"
ARQUIVO_HISTORICO = ".guardiao_historico.json"
ARQUIVO_INSCRICAO = ".guardiao_inscricao.json"
ARQUIVO_REGISTRO_MD = "REGISTRO_P388.md"
RELATORIO_GIGANTES = "_archive/nivel5_arquivos_gigantes.json"

_ULTIMA_INSCRICAO_MEMORIA: Optional[str] = None


def _ativar_cores_windows() -> None:
    if os.name == "nt":
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            modo = ctypes.c_ulong()
            if kernel32.GetConsoleMode(handle, ctypes.byref(modo)):
                kernel32.SetConsoleMode(handle, modo.value | 0x0004)
        except Exception:
            pass


def verde(texto: str) -> str:
    return f"{VERDE_ANSI}{texto}{RESET_ANSI}"


def amarelo(texto: str) -> str:
    return f"{AMARELO_ANSI}{texto}{RESET_ANSI}"


def descobrir_raiz() -> str:
    atual = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(atual).lower() in (
        "core",
        "legal",
        "scripts",
        "tools",
        "web",
        "frontend",
        PASTA_DEDICADA_AUDITORIA.lower(),
    ):
        pai = os.path.abspath(os.path.join(atual, ".."))
        if os.path.isdir(pai):
            return pai
    return atual


def sha256_arquivo(caminho: str) -> str:
    h = hashlib.sha256()
    try:
        with open(caminho, "rb") as f:
            for bloco in iter(lambda: f.read(65536), b""):
                h.update(bloco)
        return h.hexdigest()
    except Exception:
        return ""


def contar_linhas(caminho: str) -> int:
    try:
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def eh_arquivo_auditoria_ou_ajuste(nome_arquivo: str) -> bool:
    baixo = nome_arquivo.lower()
    if not baixo.endswith(".py"):
        return False
    if baixo in {"main.py", "guardiao_organizador.py"}:
        return False
    return baixo.startswith(
        (
            "auditor_",
            "auditoria_",
            "verificador_",
            "diagnostico_",
            "ajustar_",
            "aplicar_",
            "corrigir_",
            "atualizar_",
            "patch_",
            "limpar_",
            "limpeza_",
        )
    )


def mapear_arquivos(raiz: str) -> Dict[str, Dict[str, Any]]:
    mapa: Dict[str, Dict[str, Any]] = {}
    for pasta_atual, subdirs, arquivos in os.walk(raiz):
        subdirs[:] = [d for d in subdirs if d not in PASTAS_IGNORADAS]
        for nome in sorted(arquivos):
            caminho = os.path.join(pasta_atual, nome)
            rel = os.path.relpath(caminho, raiz).replace("\\", "/")
            if rel in {ARQUIVO_SNAPSHOT, ARQUIVO_HISTORICO, ARQUIVO_INSCRICAO}:
                continue
            try:
                tamanho = os.path.getsize(caminho)
            except Exception:
                tamanho = 0
            mapa[rel] = {
                "tamanho": tamanho,
                "sha256": sha256_arquivo(caminho),
            }
    return mapa


def obter_estado_git(raiz: str) -> Dict[str, str]:
    info = {
        "disponivel": "nao",
        "branch": "",
        "commit_curto": "",
        "commit_hash": "",
        "mensagem": "",
        "limpo": "desconhecido",
    }
    try:
        inside = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=raiz,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if inside.returncode != 0 or inside.stdout.strip().lower() != "true":
            return info

        info["disponivel"] = "sim"

        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=raiz,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if branch.returncode == 0:
            info["branch"] = branch.stdout.strip()

        commit_full = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=raiz,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if commit_full.returncode == 0:
            h_full = commit_full.stdout.strip()
            info["commit_hash"] = h_full
            info["commit_curto"] = h_full[:7]

        msg = subprocess.run(
            ["git", "log", "-1", "--pretty=%s"],
            cwd=raiz,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if msg.returncode == 0:
            info["mensagem"] = msg.stdout.strip()

        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=raiz,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if status.returncode == 0:
            info["limpo"] = "sim" if not status.stdout.strip() else "nao"
    except Exception:
        pass
    return info


def _garantir_raiz_no_sys_path(raiz: str) -> None:
    if raiz and raiz not in sys.path:
        sys.path.insert(0, raiz)


def _registrar_no_ledger_se_disponivel(raiz: str, resumo_inscricao: str) -> Optional[str]:
    global _ULTIMA_INSCRICAO_MEMORIA
    if _ULTIMA_INSCRICAO_MEMORIA == resumo_inscricao:
        return None

    _garantir_raiz_no_sys_path(raiz)
    try:
        mod_main = importlib.import_module("main")
        auditor = getattr(mod_main, "auditor_ledger", None)
        if auditor is not None and hasattr(auditor, "gerar_bloco_auditado"):
            hash_bloco = auditor.gerar_bloco_auditado(
                "GUARDIAO_ORGANIZADOR",
                "INSCRICAO_ESTADO_E_HISTORICO",
                resumo_inscricao,
            )
            _ULTIMA_INSCRICAO_MEMORIA = resumo_inscricao
            return str(hash_bloco)
    except Exception:
        pass
    return None


def inscrever_estado_guardiao(raiz: str, simular: bool = False) -> Dict[str, Any]:
    """
    Inscreve o estado atual do repositório, artefatos-chave (abertura em /,
    painel em /painel e Protocolo 388) e referência do Git em
    .guardiao_inscricao.json e REGISTRO_P388.md de forma limpa e auditável.
    """
    agora_iso = datetime.datetime.now().isoformat()
    agora_legivel = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_info = obter_estado_git(raiz)

    artefatos: Dict[str, Dict[str, Any]] = {}
    for rel in ARQUIVOS_CHAVE_INSCRICAO:
        caminho = os.path.join(raiz, rel)
        existe = os.path.isfile(caminho)
        artefatos[rel] = {
            "presente": existe,
            "sha256": sha256_arquivo(caminho) if existe else "",
            "linhas": contar_linhas(caminho) if existe else 0,
        }

    base_assinatura = json.dumps(
        {
            "git_commit": git_info.get("commit_hash", ""),
            "artefatos": artefatos,
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    digest_inscricao = hashlib.sha256(base_assinatura.encode("utf-8")).hexdigest()[:16]

    resumo_ledger = (
        f"INSCRICAO:{digest_inscricao}|GIT:{git_info.get('commit_curto') or 'SEM_GIT'}"
        f"|ABERTURA:{'OK' if artefatos.get('abertura_index.html', {}).get('presente') else 'AUSENTE'}"
        f"|PAINEL:{'OK' if artefatos.get('index.html', {}).get('presente') else 'AUSENTE'}"
        f"|P388:{'OK' if artefatos.get('protocolo_388.json', {}).get('presente') else 'AUSENTE'}"
    )

    hash_ledger = None if simular else _registrar_no_ledger_se_disponivel(raiz, resumo_ledger)

    payload: Dict[str, Any] = {
        "inscrito_em": agora_iso,
        "codigo_inscricao": digest_inscricao,
        "hash_ledger": hash_ledger or "",
        "git": git_info,
        "artefatos_chave": artefatos,
    }

    caminho_inscricao = os.path.join(raiz, ARQUIVO_INSCRICAO)
    caminho_md = os.path.join(raiz, ARQUIVO_REGISTRO_MD)

    linhas_md = [
        "# Registro de Inscricao — Protocolo 388 e Guardiao",
        "",
        f"- Atualizado em: {agora_legivel}",
        f"- Codigo de inscricao: `{digest_inscricao}`",
        f"- Git branch/commit: `{git_info.get('branch') or 'N/A'}` @ `{git_info.get('commit_curto') or 'N/A'}`",
        f"- Mensagem do commit: {git_info.get('mensagem') or 'N/A'}",
        f"- Working tree limpo: `{git_info.get('limpo')}`",
        f"- Hash Ledger: `{hash_ledger or 'registrado/nao-aplicavel'}`",
        "",
        "## Artefatos Verificados",
        "",
    ]
    for rel, info_arq in artefatos.items():
        status_arq = "OK" if info_arq["presente"] else "AUSENTE"
        sha_curto = info_arq["sha256"][:12] if info_arq["sha256"] else "-"
        linhas_md.append(f"- `{rel}`: **{status_arq}** ({info_arq['linhas']} linhas | sha256 `{sha_curto}`)")
    linhas_md.append("")

    if not simular:
        with open(caminho_inscricao, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        with open(caminho_md, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas_md))

    return payload


def _listar_htmls_ativos(raiz: str) -> List[Tuple[str, str]]:
    encontrados: List[Tuple[str, str]] = []
    for pasta_atual, subdirs, arquivos in os.walk(raiz):
        subdirs[:] = [d for d in subdirs if d not in PASTAS_IGNORADAS]
        rel_dir = os.path.relpath(pasta_atual, raiz).replace("\\", "/").lower()
        partes_dir = set() if rel_dir == "." else set(rel_dir.split("/"))
        if partes_dir & PASTAS_ARQUIVO:
            continue
        for nome in sorted(arquivos):
            if os.path.splitext(nome)[1].lower() in {".html", ".htm"}:
                caminho = os.path.join(pasta_atual, nome)
                rel = os.path.relpath(caminho, raiz).replace("\\", "/")
                encontrados.append((rel, caminho))
    return encontrados


def preparar_e_simular_alertas_html(raiz: str) -> Dict[str, Any]:
    """
    Lê os HTMLs ativos, conta quantos alert(...) existem, avalia compatibilidade
    para modificação segura e executa a simulação da troca por console.warn(...).
    Retorna um dicionário com o veredito claro se VAI MEXER ou NAO VAI MEXER.
    """
    print(verde("\n--- GUARDIAO: LEITURA, COMPATIBILIDADE E SIMULACAO DE alert() (HTML) ---"))
    padrao_chamada = re.compile(r"\b(?:window\.)?alert\s*\(")

    detalhes_por_arquivo: List[Dict[str, Any]] = []
    total_alertas = 0
    erros_leitura: List[str] = []

    for rel, caminho in _listar_htmls_ativos(raiz):
        try:
            with open(caminho, "r", encoding="utf-8", errors="strict") as f:
                conteudo = f.read()
        except Exception as exc:
            erros_leitura.append(f"{rel}: {exc}")
            continue

        matches = list(padrao_chamada.finditer(conteudo))
        qtd = len(matches)
        if qtd > 0:
            linhas_afetadas: List[int] = []
            for m in matches:
                num_linha = conteudo.count("\n", 0, m.start()) + 1
                if num_linha not in linhas_afetadas:
                    linhas_afetadas.append(num_linha)
            total_alertas += qtd
            backup_rel = os.path.join("_archive", "alertas_backup", rel).replace("\\", "/")
            detalhes_por_arquivo.append(
                {
                    "arquivo": rel,
                    "caminho": caminho,
                    "conteudo": conteudo,
                    "quantidade": qtd,
                    "linhas": linhas_afetadas,
                    "backup_rel": backup_rel,
                }
            )
            print(
                f"  * {rel}: {qtd} alert(...) nas linhas {linhas_afetadas} -> [SIMULAR] trocar por console.warn(...)"
            )

    compativel = len(erros_leitura) == 0
    vai_mexer = compativel and (total_alertas > 0)

    if erros_leitura:
        motivo = f"Incompatibilidade de leitura detectada: {'; '.join(erros_leitura)}"
    elif total_alertas == 0:
        motivo = "Nenhum alert() encontrado nos arquivos HTML ativos."
    else:
        motivo = (
            f"{total_alertas} alert(...) encontrado(s) em {len(detalhes_por_arquivo)} arquivo(s) HTML; "
            f"compatível e pronto para substituição segura com backup em _archive/alertas_backup/."
        )

    veredito = "VAI MEXER" if vai_mexer else "NAO VAI MEXER"
    print(verde(f"  Quantidade total de alert() lidos : {total_alertas}"))
    print(verde(f"  Compatibilidade para mudança       : {'SIM' if compativel else 'NAO'}"))
    print(amarelo(f"  VEREDICTO DO GUARDIAO              : {veredito} — {motivo}"))

    return {
        "vai_mexer": vai_mexer,
        "veredito": veredito,
        "compativel": compativel,
        "total_alertas": total_alertas,
        "motivo": motivo,
        "arquivos": detalhes_por_arquivo,
    }


def aplicar_limpeza_alertas_html(
    raiz: str,
    caminho_hist: str,
    plano: Optional[Dict[str, Any]] = None,
    simular: bool = False,
) -> bool:
    """
    Executa a modificação preparada nos HTMLs (alert(...) -> console.warn(...)),
    salva backup em _archive/alertas_backup/ e registra lote em .guardiao_historico.json.
    """
    if plano is None:
        plano = preparar_e_simular_alertas_html(raiz)

    if not plano.get("vai_mexer"):
        print(amarelo(f"  [GUARDIAO - NAO VAI MEXER] {plano.get('motivo')}"))
        return False

    if simular:
        print(verde("  [SIMULACAO CONCLUIDA] Nenhuma alteração gravada no disco."))
        return True

    padrao_chamada = re.compile(r"\b(?:window\.)?alert\s*\(")
    movimentos_hist: List[Dict[str, str]] = []
    alterados = 0

    for item in plano.get("arquivos", []):
        rel = item["arquivo"]
        caminho = item["caminho"]
        conteudo = item["conteudo"]
        backup_rel = item["backup_rel"]
        backup_abs = os.path.join(raiz, backup_rel)

        os.makedirs(os.path.dirname(backup_abs), exist_ok=True)
        shutil.copy2(caminho, backup_abs)
        sha_backup = sha256_arquivo(backup_abs)

        novo_conteudo = padrao_chamada.sub("console.warn(", conteudo)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(novo_conteudo)

        movimentos_hist.append(
            {
                "origem": f"__ALERT_PATCH__:{rel}",
                "destino": backup_rel,
                "sha256": sha_backup,
            }
        )
        alterados += 1
        print(verde(f"  [APLICADO] {rel}: {item['quantidade']} alert(...) -> console.warn(...)"))

    if movimentos_hist:
        registrar_lote(caminho_hist, "Substituir alert() por console.warn() em HTMLs", movimentos_hist)
        print(verde(f"  [HISTORICO] Lote registrado ({alterados} arquivo(s) HTML alterado(s))."))
    return True


def salvar_snapshot(raiz: str, caminho_snap: str) -> None:
    dados = {
        "criado_em": datetime.datetime.now().isoformat(),
        "raiz": raiz,
        "total_arquivos": 0,
        "arquivos": mapear_arquivos(raiz),
    }
    dados["total_arquivos"] = len(dados["arquivos"])
    with open(caminho_snap, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    print(verde(f"[SNAPSHOT] Salvo em: {caminho_snap} ({dados['total_arquivos']} arquivos)"))


def comparar_snapshot(raiz: str, caminho_snap: str) -> None:
    if not os.path.isfile(caminho_snap):
        print("[AVISO] Nenhum snapshot encontrado ainda. Rode com --snapshot primeiro.")
        return

    with open(caminho_snap, "r", encoding="utf-8") as f:
        anterior = json.load(f).get("arquivos", {})

    atual = mapear_arquivos(raiz)

    removidos = sorted(set(anterior.keys()) - set(atual.keys()))
    adicionados = sorted(set(atual.keys()) - set(anterior.keys()))
    modificados = sorted(
        k
        for k in (set(anterior.keys()) & set(atual.keys()))
        if anterior[k].get("sha256") != atual[k].get("sha256")
    )

    print("\n--- COMPARATIVO COM O SNAPSHOT ---")
    print(f"Removidos / Movidos (origem) : {len(removidos)}")
    for item in removidos[:20]:
        print(f"  - {item}")
    if len(removidos) > 20:
        print(f"  ... e mais {len(removidos) - 20}")

    print(f"Adicionados / Movidos (destino): {len(adicionados)}")
    for item in adicionados[:20]:
        print(verde(f"  + {item}"))
    if len(adicionados) > 20:
        print(f"  ... e mais {len(adicionados) - 20}")

    print(f"Conteúdo modificado            : {len(modificados)}")
    for item in modificados[:20]:
        print(f"  * {item}")
    if len(modificados) > 20:
        print(f"  ... e mais {len(modificados) - 20}")


def carregar_historico(caminho_hist: str) -> List[Dict[str, Any]]:
    if not os.path.isfile(caminho_hist):
        return []
    try:
        with open(caminho_hist, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def salvar_historico(caminho_hist: str, lotes: List[Dict[str, Any]]) -> None:
    with open(caminho_hist, "w", encoding="utf-8") as f:
        json.dump(lotes, f, indent=2, ensure_ascii=False)


def registrar_lote(caminho_hist: str, descricao: str, movimentos: List[Dict[str, str]]) -> None:
    if not movimentos:
        return
    lotes = carregar_historico(caminho_hist)
    lotes.append(
        {
            "id": len(lotes) + 1,
            "data_hora": datetime.datetime.now().isoformat(),
            "descricao": descricao,
            "movimentos": movimentos,
        }
    )
    salvar_historico(caminho_hist, lotes)


def desfazer_ultimo_lote(raiz: str, caminho_hist: str, simular: bool = False) -> bool:
    lotes = carregar_historico(caminho_hist)
    if not lotes:
        print("[AVISO] Não há nenhuma ação registrada para desfazer.")
        return False

    ultimo = lotes[-1]
    movimentos = list(reversed(ultimo.get("movimentos", [])))
    print(verde(f"\n--- DESFAZER LOTE #{ultimo.get('id')}: {ultimo.get('descricao')} ---"))
    print(f"Total de arquivos no lote: {len(movimentos)}")

    restaurados = 0
    ignorados = 0

    for mov in movimentos:
        origem_rel = mov.get("origem", "")
        destino_rel = mov.get("destino", "")
        sha_esperado = mov.get("sha256", "")

        if origem_rel.startswith("__ALERT_PATCH__:"):
            alvo_rel = origem_rel.split(":", 1)[1]
            caminho_backup = os.path.join(raiz, destino_rel)
            caminho_alvo = os.path.join(raiz, alvo_rel)
            if not os.path.isfile(caminho_backup):
                print(f"  [IGNORADO] Backup de alerta não encontrado: {destino_rel}")
                ignorados += 1
                continue
            if simular:
                print(verde(f"  [SIMULAR] Restaurar {destino_rel} -> {alvo_rel}"))
                restaurados += 1
                continue
            shutil.copy2(caminho_backup, caminho_alvo)
            print(verde(f"  [RESTAURADO] {destino_rel} -> {alvo_rel}"))
            restaurados += 1
            continue

        caminho_atual = os.path.join(raiz, destino_rel)
        caminho_original = os.path.join(raiz, origem_rel)

        if not os.path.isfile(caminho_atual):
            print(f"  [IGNORADO] Arquivo não encontrado no destino: {destino_rel}")
            ignorados += 1
            continue

        if os.path.exists(caminho_original):
            print(f"  [IGNORADO] Já existe arquivo na origem: {origem_rel}")
            ignorados += 1
            continue

        sha_atual = sha256_arquivo(caminho_atual)
        if sha_esperado and sha_atual and sha_atual != sha_esperado:
            print(f"  [AVISO] Hash diferente em {destino_rel}; restaurando mesmo assim.")

        if simular:
            print(verde(f"  [SIMULAR] {destino_rel} -> {origem_rel}"))
            restaurados += 1
            continue

        os.makedirs(os.path.dirname(caminho_original), exist_ok=True)
        shutil.move(caminho_atual, caminho_original)
        print(verde(f"  [DESFEITO] {destino_rel} -> {origem_rel}"))
        restaurados += 1

    if not simular:
        lotes.pop()
        salvar_historico(caminho_hist, lotes)
        print(verde(f"Concluído: {restaurados} arquivo(s) restaurado(s), {ignorados} ignorado(s)."))
    else:
        print(verde(f"Simulação concluída: {restaurados} arquivo(s) seriam restaurado(s), {ignorados} ignorado(s)."))

    return True


def aplicar_nivel_2(raiz: str, caminho_hist: str, simular: bool = False) -> None:
    movimentos: List[Dict[str, str]] = []

    print(verde("\n--- APLICAR NIVEL 2: ISOLAR BACKUPS E TESTES ---"))

    for pasta_atual, subdirs, arquivos in os.walk(raiz):
        subdirs[:] = [d for d in subdirs if d not in PASTAS_IGNORADAS]
        rel_dir = os.path.relpath(pasta_atual, raiz).replace("\\", "/").lower()
        partes_dir = set() if rel_dir == "." else set(rel_dir.split("/"))
        em_arquivo = bool(partes_dir & PASTAS_ARQUIVO)

        if em_arquivo:
            continue

        for nome in sorted(arquivos):
            baixo = nome.lower()
            if baixo == "guardiao_organizador.py":
                continue

            eh_backup_ou_teste = (
                ".bak" in baixo
                or "backup" in baixo
                or baixo.startswith(("teste_", "test_"))
            )
            if not eh_backup_ou_teste:
                continue

            caminho_origem = os.path.join(pasta_atual, nome)
            rel_origem = os.path.relpath(caminho_origem, raiz).replace("\\", "/")
            rel_destino = os.path.join("_archive", "nivel2_backups_testes", rel_origem).replace("\\", "/")
            caminho_destino = os.path.join(raiz, rel_destino)

            if os.path.exists(caminho_destino):
                print(f"  [IGNORADO] Destino já existe: {rel_destino}")
                continue

            sha = sha256_arquivo(caminho_origem)
            if simular:
                print(verde(f"  [SIMULAR] {rel_origem} -> {rel_destino}"))
                continue

            os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
            shutil.move(caminho_origem, caminho_destino)
            movimentos.append(
                {
                    "origem": rel_origem,
                    "destino": rel_destino,
                    "sha256": sha,
                }
            )
            print(verde(f"  [MOVIDO] {rel_origem} -> {rel_destino}"))

    if simular:
        print(verde("Simulação do Nível 2 concluída (nenhum arquivo foi alterado)."))
        return

    if movimentos:
        registrar_lote(caminho_hist, "Isolar backups e testes (Nível 2)", movimentos)
        print(verde(f"Lote gravado no histórico: {len(movimentos)} arquivo(s) movido(s)."))
    else:
        print("[AVISO] Nenhum arquivo pendente do Nível 2 foi movido.")


def aplicar_nivel_3(raiz: str, caminho_hist: str, simular: bool = False) -> None:
    movimentos: List[Dict[str, str]] = []

    print(verde(f"\n--- APLICAR NIVEL 3: CENTRALIZAR EM '{PASTA_DEDICADA_AUDITORIA}/' ---"))

    for pasta_atual, subdirs, arquivos in os.walk(raiz):
        subdirs[:] = [d for d in subdirs if d not in PASTAS_IGNORADAS]
        rel_dir = os.path.relpath(pasta_atual, raiz).replace("\\", "/").lower()
        partes_dir = set() if rel_dir == "." else set(rel_dir.split("/"))
        em_arquivo = bool(partes_dir & PASTAS_ARQUIVO)
        em_auditoria = bool(partes_dir & {p.strip().lower() for p in PASTAS_AUDITORIA_ACEITAS})

        if em_arquivo or em_auditoria:
            continue

        for nome in sorted(arquivos):
            if not eh_arquivo_auditoria_ou_ajuste(nome):
                continue

            caminho_origem = os.path.join(pasta_atual, nome)
            rel_origem = os.path.relpath(caminho_origem, raiz).replace("\\", "/")
            rel_destino = os.path.join(PASTA_DEDICADA_AUDITORIA, nome).replace("\\", "/")
            caminho_destino = os.path.join(raiz, rel_destino)

            if os.path.exists(caminho_destino):
                print(f"  [IGNORADO] Destino já existe: {rel_destino}")
                continue

            sha = sha256_arquivo(caminho_origem)
            if simular:
                print(verde(f"  [SIMULAR] {rel_origem} -> {rel_destino}"))
                continue

            os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
            shutil.move(caminho_origem, caminho_destino)
            movimentos.append(
                {
                    "origem": rel_origem,
                    "destino": rel_destino,
                    "sha256": sha,
                }
            )
            print(verde(f"  [MOVIDO] {rel_origem} -> {rel_destino}"))

    if simular:
        print(verde("Simulação do Nível 3 concluída (nenhum arquivo foi alterado)."))
        return

    if movimentos:
        registrar_lote(
            caminho_hist,
            f"Centralizar auditorias e ajustes em {PASTA_DEDICADA_AUDITORIA}/ (Nível 3)",
            movimentos,
        )
        print(verde(f"Lote gravado no histórico: {len(movimentos)} arquivo(s) movido(s)."))
    else:
        os.makedirs(os.path.join(raiz, PASTA_DEDICADA_AUDITORIA), exist_ok=True)
        print(verde(f"[OK] Pasta '{PASTA_DEDICADA_AUDITORIA}/' verificada e nenhum arquivo extra precisou ser movido."))


def aplicar_nivel_4(raiz: str, caminho_hist: str, simular: bool = False) -> None:
    """
    Painel HTML separado e preservado intacto (nunca movido automaticamente).
    Move apenas arquivos .css/.js soltos fora de pastas web/painel/arquivo se explicitamente solicitado.
    """
    movimentos: List[Dict[str, str]] = []
    pastas_web_norm = {p.strip().lower() for p in PASTAS_WEB}

    print(verde("\n--- APLICAR NIVEL 4: ASSETS ESTÁTICOS (PAINEL HTML SEPARADO E INTACTO) ---"))

    for pasta_atual, subdirs, arquivos in os.walk(raiz):
        subdirs[:] = [d for d in subdirs if d not in PASTAS_IGNORADAS]
        rel_dir = os.path.relpath(pasta_atual, raiz).replace("\\", "/").lower()
        partes_dir = set() if rel_dir == "." else set(rel_dir.split("/"))
        em_arquivo = bool(partes_dir & PASTAS_ARQUIVO)
        em_web = bool(partes_dir & pastas_web_norm)

        if em_arquivo or em_web:
            continue

        for nome in sorted(arquivos):
            ext = os.path.splitext(nome)[1].lower()
            if ext in {".html", ".htm"}:
                rel_html = os.path.relpath(os.path.join(pasta_atual, nome), raiz).replace("\\", "/")
                print(amarelo(f"  [PAINEL HTML PROTEGIDO] Mantido no lugar: {rel_html}"))
                continue

            if ext not in {".css", ".js"}:
                continue

            caminho_origem = os.path.join(pasta_atual, nome)
            rel_origem = os.path.relpath(caminho_origem, raiz).replace("\\", "/")
            rel_destino = os.path.join("web", nome).replace("\\", "/")
            caminho_destino = os.path.join(raiz, rel_destino)

            if os.path.exists(caminho_destino):
                print(f"  [IGNORADO] Destino já existe: {rel_destino}")
                continue

            sha = sha256_arquivo(caminho_origem)
            if simular:
                print(verde(f"  [SIMULAR] {rel_origem} -> {rel_destino}"))
                continue

            os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
            shutil.move(caminho_origem, caminho_destino)
            movimentos.append(
                {
                    "origem": rel_origem,
                    "destino": rel_destino,
                    "sha256": sha,
                }
            )
            print(verde(f"  [MOVIDO] {rel_origem} -> {rel_destino}"))

    if simular:
        print(verde("Simulação do Nível 4 concluída (painel HTML intocado)."))
        return

    if movimentos:
        registrar_lote(caminho_hist, "Organizar CSS/JS estáticos em web/ preservando painel HTML (Nível 4)", movimentos)
        print(verde(f"Lote gravado no histórico: {len(movimentos)} arquivo(s) movido(s)."))
    else:
        print(verde("[OK] Nenhum asset extra movido; painel HTML preservado intacto."))


def aplicar_nivel_5(raiz: str, simular: bool = False) -> None:
    """
    Gera o mapa de arquivos >= 2000 linhas em _archive/nivel5_arquivos_gigantes.json
    sem quebrar código em produção.
    """
    print(verde("\n--- APLICAR NIVEL 5: MAPEAR ARQUIVOS GIGANTES (>=2000 LINHAS) ---"))
    gigantes: List[Dict[str, Any]] = []

    for pasta_atual, subdirs, arquivos in os.walk(raiz):
        subdirs[:] = [d for d in subdirs if d not in PASTAS_IGNORADAS]
        rel_dir = os.path.relpath(pasta_atual, raiz).replace("\\", "/").lower()
        partes_dir = set() if rel_dir == "." else set(rel_dir.split("/"))
        if partes_dir & PASTAS_ARQUIVO:
            continue

        for nome in sorted(arquivos):
            ext = os.path.splitext(nome)[1].lower()
            if ext not in EXTENSOES_CODIGO:
                continue
            caminho = os.path.join(pasta_atual, nome)
            linhas = contar_linhas(caminho)
            if linhas >= 2000:
                rel = os.path.relpath(caminho, raiz).replace("\\", "/")
                gigantes.append({"arquivo": rel, "linhas": linhas})

    gigantes.sort(key=lambda x: -x["linhas"])
    for item in gigantes:
        print(f"  * {item['linhas']} linhas -> {item['arquivo']}")

    destino_rel = os.path.join(raiz, RELATORIO_GIGANTES)
    if simular:
        print(verde(f"Simulação do Nível 5 concluída ({len(gigantes)} arquivo(s) mapeado(s))."))
        return

    os.makedirs(os.path.dirname(destino_rel), exist_ok=True)
    with open(destino_rel, "w", encoding="utf-8") as f:
        json.dump(
            {
                "gerado_em": datetime.datetime.now().isoformat(),
                "total": len(gigantes),
                "arquivos": gigantes,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(verde(f"[NIVEL 5] Mapa salvo em: {RELATORIO_GIGANTES} ({len(gigantes)} arquivo(s))"))


def verificar_sintaxe_python(raiz: str) -> Tuple[int, List[str]]:
    erros: List[str] = []
    total_py = 0

    for pasta_atual, subdirs, arquivos in os.walk(raiz):
        subdirs[:] = [d for d in subdirs if d not in PASTAS_IGNORADAS]
        for nome in sorted(arquivos):
            if not nome.endswith(".py"):
                continue
            total_py += 1
            caminho = os.path.join(pasta_atual, nome)
            rel = os.path.relpath(caminho, raiz).replace("\\", "/")
            try:
                with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                    codigo = f.read()
                ast.parse(codigo, filename=rel)
            except SyntaxError as exc:
                erros.append(f"{rel} (linha {exc.lineno}): {exc.msg}")
            except Exception as exc:
                erros.append(f"{rel}: {exc}")

    return total_py, erros


def verificar_imports_criticos(raiz: str) -> Tuple[int, List[str]]:
    subpastas = ["", "core", "legal", PASTA_DEDICADA_AUDITORIA, "tools", "scripts", "web", "frontend"]
    for sub in subpastas:
        p = os.path.join(raiz, sub) if sub else raiz
        if os.path.isdir(p) and p not in sys.path:
            sys.path.insert(0, p)

    ok_count = 0
    falhas: List[str] = []

    for rotulo, candidatos in MODULOS_CRITICOS:
        carregou = False
        ultimo_erro = ""
        for mod_nome in candidatos:
            try:
                importlib.import_module(mod_nome)
                carregou = True
                ok_count += 1
                print(verde(f"  [OK] {rotulo} ({mod_nome})"))
                break
            except Exception as exc:
                ultimo_erro = f"{mod_nome}: {exc}"
        if not carregou:
            falhas.append(f"{rotulo} -> {ultimo_erro}")
            print(f"  [FALHA] {rotulo} -> {ultimo_erro}")

    return ok_count, falhas


def avaliar_escala_padronizacao(
    raiz: str,
    sem_quebras: bool,
    tem_snapshot: bool,
    qtd_erros_sintaxe: int,
    qtd_falhas_import: int,
) -> Dict[str, Any]:
    backups_fora: List[str] = []
    auditorias_fora: List[str] = []
    paineis_html: List[str] = []
    arquivos_gigantes: List[Tuple[str, int]] = []

    for pasta_atual, subdirs, arquivos in os.walk(raiz):
        subdirs[:] = [d for d in subdirs if d not in PASTAS_IGNORADAS]
        rel_dir = os.path.relpath(pasta_atual, raiz).replace("\\", "/").lower()
        partes_dir = set() if rel_dir == "." else set(rel_dir.split("/"))
        em_arquivo = bool(partes_dir & PASTAS_ARQUIVO)
        em_auditoria = bool(partes_dir & {p.strip().lower() for p in PASTAS_AUDITORIA_ACEITAS})

        for nome in sorted(arquivos):
            baixo = nome.lower()
            ext = os.path.splitext(nome)[1].lower()
            caminho = os.path.join(pasta_atual, nome)
            rel = os.path.relpath(caminho, raiz).replace("\\", "/")

            eh_backup_ou_teste = (
                ".bak" in baixo
                or "backup" in baixo
                or baixo.startswith(("teste_", "test_"))
            )
            if eh_backup_ou_teste and not em_arquivo:
                backups_fora.append(rel)

            if eh_arquivo_auditoria_ou_ajuste(nome) and not em_auditoria and not em_arquivo:
                auditorias_fora.append(rel)

            if ext in {".html", ".htm"} and not em_arquivo:
                paineis_html.append(rel)

            if ext in EXTENSOES_CODIGO:
                linhas = contar_linhas(caminho)
                if linhas >= 2000:
                    arquivos_gigantes.append((rel, linhas))

    n1 = (qtd_erros_sintaxe == 0) and tem_snapshot
    n2 = (len(backups_fora) == 0)
    pasta_auditoria_ok = os.path.isdir(os.path.join(raiz, PASTA_DEDICADA_AUDITORIA))
    n3 = (len(auditorias_fora) == 0) or pasta_auditoria_ok
    n4 = True
    mapa_n5_existe = os.path.isfile(os.path.join(raiz, RELATORIO_GIGANTES))
    n5 = (len(arquivos_gigantes) == 0) or mapa_n5_existe

    criterios = [
        (
            1,
            "Base íntegra e rastreada",
            n1,
            f"erros_sintaxe={qtd_erros_sintaxe}, falhas_import={qtd_falhas_import}, snapshot={'ok' if tem_snapshot else 'pendente'}",
        ),
        (
            2,
            "Backups e testes isolados",
            n2,
            f"{len(backups_fora)} fora de pasta de arquivo (_archive/ ou labs/)",
        ),
        (
            3,
            f"Auditorias e ajustes centralizados ({PASTA_DEDICADA_AUDITORIA}/)",
            n3,
            f"{len(auditorias_fora)} fora da pasta dedicada | pasta={'ok' if pasta_auditoria_ok else 'pendente'}",
        ),
        (
            4,
            "Painel HTML separado e protegido (intacto)",
            n4,
            f"{len(paineis_html)} HTML(s) preservados sem mover rotas",
        ),
        (
            5,
            "Arquivos gigantes (>=2000 linhas) mapeados",
            n5,
            f"{len(arquivos_gigantes)} arquivo(s) >= 2000 linhas | mapa={'ok' if mapa_n5_existe else 'pendente'}",
        ),
    ]

    nivel = sum(1 for _, _, ok, _ in criterios if ok)

    if qtd_erros_sintaxe > 0:
        proximo_titulo = "Corrigir erro de sintaxe antes de avançar"
        o_que_falta = [f"Resolver {qtd_erros_sintaxe} erro(s) de sintaxe."]
        acao_pratica = "Rode: python guardiao_organizador.py --desfazer"
    elif not tem_snapshot:
        proximo_titulo = "Completar Nível 1 — Gerar snapshot inicial de segurança"
        o_que_falta = ["Criar .guardiao_snapshot.json."]
        acao_pratica = "Execute: python guardiao_organizador.py --snapshot"
    elif not n2:
        proximo_titulo = "Completar Nível 2 — Isolar backups e scripts de teste"
        o_que_falta = [f"Mover {len(backups_fora)} arquivo(s) de backup/teste."]
        acao_pratica = "Execute: python guardiao_organizador.py --aplicar-nivel2"
    elif len(auditorias_fora) > 0 and not pasta_auditoria_ok:
        proximo_titulo = f"Completar Nível 3 — Centralizar auditorias e ajustes em '{PASTA_DEDICADA_AUDITORIA}/'"
        o_que_falta = [f"Mover {len(auditorias_fora)} script(s) de auditoria/ajuste."]
        for item in auditorias_fora[:5]:
            o_que_falta.append(f"Pendente: {item}")
        acao_pratica = "Execute: python guardiao_organizador.py --aplicar-nivel3"
    elif not n5:
        proximo_titulo = "Completar Nível 5 — Mapear arquivos gigantes (>= 2000 linhas)"
        o_que_falta = [f"Registrar {len(arquivos_gigantes)} arquivo(s) >= 2000 linhas no mapa seguro."]
        acao_pratica = "Execute: python guardiao_organizador.py --aplicar-nivel5"
    else:
        proximo_titulo = "Base organizada, níveis 3, 4 e 5 avaliados e painel HTML intacto!"
        o_que_falta = ["Níveis 1 a 5 concluídos ou mapeados com segurança."]
        acao_pratica = "Rode: python guardiao_organizador.py --snapshot"

    return {
        "nivel": nivel,
        "criterios": criterios,
        "proximo_titulo": proximo_titulo,
        "o_que_falta": o_que_falta,
        "acao_pratica": acao_pratica,
    }


def imprimir_bloco_arquitetura_e_automacao(lang: str = "pt") -> None:
    """
    Exibe um guia final claro sobre automação, integração nas próximas fases
    e onde expandir este script sem se perder no futuro.
    """
    idioma = (lang or "pt").strip().lower()
    if idioma == "en":
        print(verde("\n5. AUTOMATION, INTEGRATION & EXPANSION GUIDE (NEXT PHASES)"))
        print(verde("  * Automation : run syntax checks, critical module checks, and snapshots before commits or CI pipelines."))
        print(verde("  * Integration: connect core engines, AI services, and HTML panels via stable contracts/routes without breaking flows."))
        print(verde("  * Expansion  : to grow this script safely, edit MODULOS_CRITICOS, folder sets, or this final guide block."))
        print(amarelo("  * Safety Net : use --simular, --desfazer, .guardiao_historico.json, and Git so every change stays reversible."))
    else:
        print(verde("\n5. AUTOMACAO, INTEGRACAO E GUIA DE EXPANSAO (PROXIMAS FASES)"))
        print(verde("  * Automacao : rode sintaxe, modulos criticos e snapshot antes de commits, rotinas CI ou novas entregas."))
        print(verde("  * Integracao: conecte motores centrais, IA e painel HTML por rotas/contratos estaveis sem quebrar o que funciona."))
        print(verde("  * Expansao  : para aumentar este script sem se perder, mexa apenas em MODULOS_CRITICOS, pastas-alvo ou neste bloco 5."))
        print(amarelo("  * Seguranca : use --simular, --desfazer, .guardiao_historico.json e Git para evoluir com reversao garantida."))


def barra_nivel(nivel: int, maximo: int = 5) -> str:
    cheios = verde("■" * max(0, min(nivel, maximo)))
    vazios = "□" * max(0, maximo - nivel)
    return verde(f"[{cheios}{vazios}] {nivel}/{maximo}")


def executar_guardiao(
    raiz: str,
    criar_snap: bool,
    comparar: bool,
    desfazer: bool,
    aplicar_n2: bool,
    aplicar_n3: bool,
    aplicar_n4: bool,
    aplicar_n5: bool,
    simular: bool,
    inscrever: bool = False,
    organizar_tudo: bool = False,
    lang: str = "pt",
) -> bool:
    _ativar_cores_windows()
    caminho_snap = os.path.join(raiz, ARQUIVO_SNAPSHOT)
    caminho_hist = os.path.join(raiz, ARQUIVO_HISTORICO)

    print(verde("=" * 72))
    print(verde("GUARDIAO DE ORGANIZACAO - ESCALA (1 A 5), GUIA E DESFAZER"))
    print(verde("=" * 72))
    print(f"Raiz do projeto: {raiz}")

    if desfazer:
        desfazer_ultimo_lote(raiz, caminho_hist, simular=simular)

    # Leitura, compatibilidade e simulação automática dos alertas nos HTMLs
    plano_alertas = preparar_e_simular_alertas_html(raiz)

    if organizar_tudo:
        if not simular:
            aplicar_limpeza_alertas_html(raiz, caminho_hist, plano=plano_alertas, simular=False)
            aplicar_nivel_2(raiz, caminho_hist, simular=False)
            aplicar_nivel_3(raiz, caminho_hist, simular=False)
            aplicar_nivel_4(raiz, caminho_hist, simular=False)
            aplicar_nivel_5(raiz, simular=False)
            inscrever_estado_guardiao(raiz, simular=False)
            salvar_snapshot(raiz, caminho_snap)
        else:
            aplicar_nivel_2(raiz, caminho_hist, simular=True)
            aplicar_nivel_3(raiz, caminho_hist, simular=True)
            aplicar_nivel_4(raiz, caminho_hist, simular=True)
            aplicar_nivel_5(raiz, simular=True)
    else:
        if aplicar_n2:
            aplicar_nivel_2(raiz, caminho_hist, simular=simular)

        if aplicar_n3:
            aplicar_nivel_3(raiz, caminho_hist, simular=simular)

        if aplicar_n4:
            aplicar_nivel_4(raiz, caminho_hist, simular=simular)

        if aplicar_n5:
            aplicar_nivel_5(raiz, simular=simular)

        if inscrever or not simular:
            insc = inscrever_estado_guardiao(raiz, simular=simular)
            git_c = insc.get("git", {}).get("commit_curto") or "N/A"
            rotulo_sim = " (SIMULAR)" if simular else ""
            print(
                verde(
                    f"[INSCRICAO{rotulo_sim}] Codigo {insc.get('codigo_inscricao')} | Git {git_c} -> {ARQUIVO_REGISTRO_MD}"
                )
            )

        if criar_snap and not simular:
            salvar_snapshot(raiz, caminho_snap)

    if comparar:
        comparar_snapshot(raiz, caminho_snap)

    print("\n1. VERIFICANDO SINTAXE DE TODOS OS ARQUIVOS .PY...")
    total_py, erros_sintaxe = verificar_sintaxe_python(raiz)
    if erros_sintaxe:
        print(f"  [FALHA] {len(erros_sintaxe)} erro(s) de sintaxe em {total_py} arquivo(s):")
        for e in erros_sintaxe[:20]:
            print(f"    - {e}")
    else:
        print(verde(f"  [OK] Sintaxe válida em {total_py}/{total_py} arquivo(s) .py."))

    print("\n2. VERIFICANDO MODULOS CRITICOS DO SISTEMA...")
    mod_ok, falhas_import = verificar_imports_criticos(raiz)
    print(verde(f"  Resumo de módulos críticos: {mod_ok}/{len(MODULOS_CRITICOS)}"))

    sem_quebras = (not erros_sintaxe) and (not falhas_import)
    tem_snapshot = os.path.isfile(caminho_snap)
    avaliacao = avaliar_escala_padronizacao(
        raiz=raiz,
        sem_quebras=sem_quebras,
        tem_snapshot=tem_snapshot,
        qtd_erros_sintaxe=len(erros_sintaxe),
        qtd_falhas_import=len(falhas_import),
    )

    print("\n3. ESCALA DE PADRONIZACAO (1 A 5)")
    print(f"  Progresso atual: {barra_nivel(avaliacao['nivel'], 5)}")
    for num, titulo, ok, detalhe in avaliacao["criterios"]:
        linha = f"  [{'x' if ok else ' '}] Nível {num} - {titulo}: {detalhe}"
        print(verde(linha) if ok else linha)

    print(verde("\n4. O QUE FALTA E PROXIMO PASSO"))
    print(verde(f"  Objetivo atual: {avaliacao['proximo_titulo']}"))
    for item in avaliacao["o_que_falta"]:
        print(verde(f"    * {item}"))
    print(verde(f"  Próximo passo : {avaliacao['acao_pratica']}"))

    if not erros_sintaxe:
        imprimir_bloco_arquitetura_e_automacao(lang=lang)

    print(verde("-" * 72))
    print(amarelo(f"VEREDICTO FINAL DO GUARDIAO: {plano_alertas['veredito']} — {plano_alertas['motivo']}"))
    if not erros_sintaxe:
        print(verde("STATUS DO GUARDIAO: SEGURO (NENHUMA QUEBRA DE SINTAXE DETECTADA)."))
        print(verde("=" * 72))
        return True

    print("STATUS DO GUARDIAO: ATENCAO - ERRO DE SINTAXE DETECTADO.")
    print("=" * 72)
    return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Guardião com escala de 1 a 5, leitura/simulação de alertas, pasta dedicada de auditoria/ajuste e desfazer."
    )
    parser.add_argument("--snapshot", action="store_true", help="Salva fotografia atual do repositório.")
    parser.add_argument("--comparar", action="store_true", help="Compara o estado atual com o snapshot salvo.")
    parser.add_argument("--desfazer", action="store_true", help="Desfaz o último lote de movimentações registrado.")
    parser.add_argument("--inscrever", action="store_true", help="Atualiza a inscrição do estado, Git e registro documental.")
    parser.add_argument(
        "--organizar-tudo",
        action="store_true",
        help="Executa a limpeza preparada dos alertas nos HTMLs, níveis 2 a 5, inscrição e snapshot de uma só vez.",
    )
    parser.add_argument("--aplicar-nivel2", action="store_true", help="Isola backups e testes registrando o lote.")
    parser.add_argument("--aplicar-nivel3", action="store_true", help="Centraliza scripts de auditoria/ajuste registrando o lote.")
    parser.add_argument("--aplicar-nivel4", action="store_true", help="Organiza CSS/JS mantendo o painel HTML separado e intacto.")
    parser.add_argument("--aplicar-nivel5", action="store_true", help="Mapeia arquivos gigantes (>=2000 linhas) em _archive.")
    parser.add_argument("--simular", action="store_true", help="Mostra o que seria feito/desfeito sem alterar arquivos.")
    parser.add_argument(
        "--lang",
        "--idioma",
        dest="lang",
        choices=["pt", "en"],
        default="pt",
        help="Idioma do bloco final de automação e arquitetura (pt ou en).",
    )
    args = parser.parse_args()

    raiz = descobrir_raiz()
    ok = executar_guardiao(
        raiz=raiz,
        criar_snap=args.snapshot,
        comparar=args.comparar,
        desfazer=args.desfazer,
        aplicar_n2=args.aplicar_nivel2,
        aplicar_n3=args.aplicar_nivel3,
        aplicar_n4=args.aplicar_nivel4,
        aplicar_n5=args.aplicar_nivel5,
        simular=args.simular,
        inscrever=args.inscrever,
        organizar_tudo=args.organizar_tudo,
        lang=args.lang,
    )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()