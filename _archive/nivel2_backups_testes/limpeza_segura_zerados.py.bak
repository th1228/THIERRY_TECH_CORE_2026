# -*- coding: utf-8 -*-
"""
Script: limpeza_segura_zerados.py
Finalidade: Verifica referências antes de agir, apaga sobras de 0 bytes sem
            referência/cópia e move outros itens zerados sem referência para
            uma pasta reservada (_reserva_segura), preservando o que é citado
            no código para evitar erros no sistema.
"""

import os
import shutil
from typing import Dict, List, Set, Tuple

PASTAS_IGNORADAS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    "pdfs_finais",
    "_reserva_segura",
}

EXTENSOES_TEXTO_REFERENCIA = {
    ".py",
    ".html",
    ".css",
    ".js",
    ".json",
    ".toml",
    ".bat",
    ".ps1",
    ".sh",
    ".md",
    ".txt",
}

ALVOS_APAGAR_DIRETO = {
    "documentos/th.prn",
    "documentos/thierry technology - pericia cyberpunk.png",
    "checklist_seguranca.txt",
    "log_seguranca.txt",
    "ui_resources",
}


def coletar_arquivos(raiz: str) -> List[Tuple[str, str, int]]:
    itens: List[Tuple[str, str, int]] = []
    for atual, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]
        for nome in sorted(arquivos):
            caminho = os.path.join(atual, nome)
            rel = os.path.relpath(caminho, raiz).replace("\\", "/")
            try:
                if os.path.isfile(caminho):
                    itens.append((rel, nome, os.path.getsize(caminho)))
            except OSError:
                pass
    return itens


def encontrar_referencias(raiz: str, nomes_alvo: Set[str]) -> Set[str]:
    """Retorna o conjunto de nomes/caminhos (em minúsculo) citados nos arquivos do projeto."""
    citados: Set[str] = set()
    for atual, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]
        for nome in sorted(arquivos):
            ext = os.path.splitext(nome)[1].lower()
            if ext not in EXTENSOES_TEXTO_REFERENCIA and nome.lower() not in {"dockerfile", "makefile"}:
                continue
            caminho = os.path.join(atual, nome)
            try:
                with open(caminho, "r", encoding="utf-8", errors="replace") as f:
                    conteudo = f.read().lower()
                for alvo in nomes_alvo:
                    if alvo and alvo in conteudo:
                        citados.add(alvo)
            except OSError:
                pass
    return citados


def executar_limpeza_segura() -> None:
    raiz = os.path.abspath(os.path.dirname(__file__))
    pasta_reserva = os.path.join(raiz, "_reserva_segura")

    todos = coletar_arquivos(raiz)
    zerados = [(rel, nome) for rel, nome, tam in todos if tam == 0]

    if not zerados:
        print("[OK] Nenhum arquivo de 0 bytes encontrado para limpar.")
        return

    por_nome: Dict[str, List[Tuple[str, int]]] = {}
    for rel, nome, tam in todos:
        por_nome.setdefault(nome.lower(), []).append((rel, tam))

    candidatos_termos: Set[str] = set()
    for rel, nome in zerados:
        candidatos_termos.add(nome.lower())
        candidatos_termos.add(rel.lower())
        sem_ext = os.path.splitext(nome)[0].lower()
        if len(sem_ext) >= 5:
            candidatos_termos.add(sem_ext)

    citados = encontrar_referencias(raiz, candidatos_termos)

    apagados: List[str] = []
    reservados: List[str] = []
    protegidos: List[str] = []

    print("=" * 72)
    print("LIMPEZA SEGURA DE ARQUIVOS ZERADOS (0 BYTES)")
    print("=" * 72)

    for rel, nome in zerados:
        caminho_origem = os.path.join(raiz, rel.replace("/", os.sep))
        if not os.path.exists(caminho_origem):
            continue

        nome_low = nome.lower()
        rel_low = rel.lower()
        sem_ext_low = os.path.splitext(nome)[0].lower()
        ext_low = os.path.splitext(nome)[1].lower()

        tem_referencia = (
            nome_low in citados
            or rel_low in citados
            or (len(sem_ext_low) >= 5 and sem_ext_low in citados)
        )

        # Protege arquivos referenciados no código ou bancos de dados para evitar erro no sistema
        if tem_referencia or ext_low == ".db":
            protegidos.append(rel)
            print(f"[PROTEGIDO] {rel} -> citado em código ou .db (mantido intacto)")
            continue

        tem_copia_com_conteudo = any(
            outro_rel != rel and outro_tam > 0
            for outro_rel, outro_tam in por_nome.get(nome_low, [])
        )

        # Apaga apenas sobras claras sem referência e sem cópia ativa
        if rel_low in ALVOS_APAGAR_DIRETO and not tem_copia_com_conteudo:
            try:
                os.remove(caminho_origem)
                apagados.append(rel)
                print(f"[APAGADO] {rel}")
            except OSError as exc:
                protegidos.append(rel)
                print(f"[FALHA AO APAGAR] {rel} -> {exc}")
            continue

        # Move automaticamente o restante sem referência para a pasta reservada
        try:
            destino_reserva = os.path.join(pasta_reserva, rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(destino_reserva), exist_ok=True)
            shutil.move(caminho_origem, destino_reserva)
            reservados.append(rel)
            print(f"[RESERVADO] {rel} -> _reserva_segura/{rel}")
        except OSError as exc:
            protegidos.append(rel)
            print(f"[FALHA AO MOVER] {rel} -> {exc}")

    print("-" * 72)
    print(
        f"Resumo: {len(apagados)} apagado(s) | "
        f"{len(reservados)} movido(s) para '_reserva_segura' | "
        f"{len(protegidos)} protegido(s)"
    )
    print("=" * 72)


if __name__ == "__main__":
    executar_limpeza_segura()