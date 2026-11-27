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
import shutil
import sys
from typing import Any, Dict, List, Tuple

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

VERDE_ANSI = "\033[92m"
AMARELO_ANSI = "\033[93m"
RESET_ANSI = "\033[0m"

ARQUIVO_SNAPSHOT = ".guardiao_snapshot.json"
ARQUIVO_HISTORICO = ".guardiao_historico.json"
RELATORIO_GIGANTES = "_archive/nivel5_arquivos_gigantes.json"


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
            if rel in {ARQUIVO_SNAPSHOT, ARQUIVO_HISTORICO}:
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

    # Avaliação independente por nível para refletir o estado real do repositório
    n1 = (qtd_erros_sintaxe == 0) and tem_snapshot
    n2 = (len(backups_fora) == 0)
    pasta_auditoria_ok = os.path.isdir(os.path.join(raiz, PASTA_DEDICADA_AUDITORIA))
    n3 = (len(auditorias_fora) == 0) or pasta_auditoria_ok
    # Painel HTML separado e mantido intocado por segurança
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

    if aplicar_n2:
        aplicar_nivel_2(raiz, caminho_hist, simular=simular)

    if aplicar_n3:
        aplicar_nivel_3(raiz, caminho_hist, simular=simular)

    if aplicar_n4:
        aplicar_nivel_4(raiz, caminho_hist, simular=simular)

    if aplicar_n5:
        aplicar_nivel_5(raiz, simular=simular)

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

    print(verde("-" * 72))
    if not erros_sintaxe:
        print(verde("STATUS DO GUARDIAO: SEGURO (NENHUMA QUEBRA DE SINTAXE DETECTADA)."))
        print(verde("=" * 72))
        return True

    print("STATUS DO GUARDIAO: ATENCAO - ERRO DE SINTAXE DETECTADO.")
    print("=" * 72)
    return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Guardião com escala de 1 a 5, pasta dedicada de auditoria/ajuste e desfazer."
    )
    parser.add_argument("--snapshot", action="store_true", help="Salva fotografia atual do repositório.")
    parser.add_argument("--comparar", action="store_true", help="Compara o estado atual com o snapshot salvo.")
    parser.add_argument("--desfazer", action="store_true", help="Desfaz o último lote de movimentações registrado.")
    parser.add_argument("--aplicar-nivel2", action="store_true", help="Isola backups e testes registrando o lote.")
    parser.add_argument("--aplicar-nivel3", action="store_true", help="Centraliza scripts de auditoria/ajuste registrando o lote.")
    parser.add_argument("--aplicar-nivel4", action="store_true", help="Organiza CSS/JS mantendo o painel HTML separado e intacto.")
    parser.add_argument("--aplicar-nivel5", action="store_true", help="Mapeia arquivos gigantes (>=2000 linhas) em _archive.")
    parser.add_argument("--simular", action="store_true", help="Mostra o que seria feito/desfeito sem alterar arquivos.")
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
    )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()