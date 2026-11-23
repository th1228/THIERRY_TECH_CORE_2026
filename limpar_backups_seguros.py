# -*- coding: utf-8 -*-
"""
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
LIMPEZA SEGURA DE PASTAS DE BACKUP / SNAPSHOT DUPLICADAS
"""

import os
import re
import sys
import shutil
from pathlib import Path
from typing import List, Set, Tuple

PASTAS_PROTEGIDAS: Set[str] = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "core",
    "security",
    "pdfs_finais",
    "tests",
    "_reserva_segura",
}

PADRAO_PASTA_BACKUP = re.compile(
    r"^(_backup_seguro|_organizador_aa|\.auditor_backup|snap_\d+.*|.*backup.*)$",
    re.IGNORECASE,
)


def _calcular_tamanho_pasta(caminho: Path) -> Tuple[int, int]:
    total_bytes = 0
    total_arquivos = 0
    for raiz_atual, _, arquivos in os.walk(caminho):
        for nome in arquivos:
            arq = Path(raiz_atual) / nome
            try:
                total_bytes += arq.stat().st_size
                total_arquivos += 1
            except OSError:
                pass
    return total_arquivos, total_bytes


def localizar_pastas_backup(raiz: Path) -> List[Path]:
    alvos: List[Path] = []
    for atual, dirs, _ in os.walk(raiz):
        caminho_atual = Path(atual)
        dirs[:] = [d for d in dirs if d not in PASTAS_PROTEGIDAS]

        mantidas: List[str] = []
        for d in dirs:
            if PADRAO_PASTA_BACKUP.match(d):
                alvos.append(caminho_atual / d)
            else:
                mantidas.append(d)
        dirs[:] = mantidas

    return sorted(alvos, key=lambda p: len(p.parts), reverse=True)


def _formatar_tamanho(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes} B"
    if num_bytes < 1024 ** 2:
        return f"{num_bytes / 1024:.1f} KB"
    return f"{num_bytes / (1024 ** 2):.2f} MB"


def executar_limpeza(raiz: Path, aplicar: bool = False, forcar: bool = False) -> None:
    alvos = localizar_pastas_backup(raiz)
    if not alvos:
        print("[OK] Nenhuma pasta de backup/snapshot encontrada para remover.")
        return

    print(f"Pastas de backup/snapshot encontradas ({len(alvos)}):")
    soma_arquivos = 0
    soma_bytes = 0
    for pasta in alvos:
        qtd_arq, tam = _calcular_tamanho_pasta(pasta)
        soma_arquivos += qtd_arq
        soma_bytes += tam
        print(f"  - {pasta.relative_to(raiz)} ({qtd_arq} arquivo(s), {_formatar_tamanho(tam)})")

    print(f"\nTotal: {soma_arquivos} arquivo(s) | {_formatar_tamanho(soma_bytes)}")

    if not aplicar:
        print("\nModo SIMULAÇÃO ativo: nenhum arquivo foi apagado.")
        print("Para remover de verdade, rode: python .\\limpar_backups_seguros.py --limpar")
        return

    if not forcar:
        resposta = input("\nConfirma a remoção definitiva dessas pastas de backup? Digite SIM para confirmar: ").strip()
        if resposta.upper() != "SIM":
            print("Operação cancelada. Nenhum arquivo foi removido.")
            return

    removidas = 0
    falhas = 0
    for pasta in alvos:
        try:
            shutil.rmtree(pasta)
            removidas += 1
            print(f"[REMOVIDA] {pasta.relative_to(raiz)}")
        except Exception as erro:
            falhas += 1
            print(f"[ERRO] {pasta.relative_to(raiz)}: {erro}")

    print(f"\nConcluído: {removidas} pasta(s) removida(s), {falhas} falha(s).")


if __name__ == "__main__":
    raiz_projeto = Path.cwd().resolve()
    args = set(sys.argv[1:])
    modo_aplicar = bool(args & {"--limpar", "--aplicar"})
    modo_forcar = bool(args & {"--forcar", "-y"})
    executar_limpeza(raiz_projeto, aplicar=modo_aplicar, forcar=modo_forcar)