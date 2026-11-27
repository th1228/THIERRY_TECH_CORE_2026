# -*- coding: utf-8 -*-
"""
Script: diagnostico_arquivos_zerados.py
Finalidade: Varrer o projeto e diagnosticar (sem excluir ou alterar nada)
            arquivos de 0 bytes: referências em .py, indícios de uso/escrita,
            ocorrências em outras pastas e risco de erro/necessidade.
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Tuple

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
}

PADROES_USO = re.compile(
    r"(open\s*\(|write\s*\(|writelines|json\.(dump|load)|sqlite3|connect\s*\(|"
    r"makedirs|mkdir|exists|isfile|remove|unlink|rename|replace|logging|log_path|db_path)",
    re.IGNORECASE,
)


def coletar_arquivos(raiz: str) -> List[Tuple[str, str, int, float]]:
    itens: List[Tuple[str, str, int, float]] = []
    for atual, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]
        for nome in sorted(arquivos):
            caminho = os.path.join(atual, nome)
            rel = os.path.relpath(caminho, raiz)
            try:
                if os.path.isfile(caminho):
                    st = os.stat(caminho)
                    itens.append((rel, nome, st.st_size, st.st_mtime))
            except OSError:
                pass
    return itens


def analisar_referencias_py(
    raiz: str, alvos: List[Tuple[str, str]]
) -> Dict[str, List[Tuple[str, int, str, bool]]]:
    """
    Retorna por caminho_rel_zerado:
      [(arquivo_py, linha, trecho, tem_indicio_io)]
    """
    mapa: Dict[str, List[Tuple[str, int, str, bool]]] = {rel: [] for rel, _ in alvos}

    for atual, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]
        for nome in sorted(arquivos):
            if not nome.lower().endswith(".py"):
                continue
            caminho_py = os.path.join(atual, nome)
            rel_py = os.path.relpath(caminho_py, raiz)
            try:
                with open(caminho_py, "r", encoding="utf-8", errors="replace") as f:
                    for num_linha, linha in enumerate(f, start=1):
                        low = linha.lower()
                        trecho = linha.strip()
                        for rel_alvo, nome_alvo in alvos:
                            nome_low = nome_alvo.lower()
                            sem_ext_low = os.path.splitext(nome_alvo)[0].lower()
                            casou = (nome_low in low) or (
                                len(sem_ext_low) >= 6 and sem_ext_low in low
                            )
                            if casou:
                                tem_io = bool(PADROES_USO.search(trecho))
                                mapa[rel_alvo].append((rel_py, num_linha, trecho, tem_io))
            except OSError:
                pass

    return mapa


def classificar_item(
    rel: str,
    nome: str,
    outras_copias: List[Tuple[str, int]],
    refs: List[Tuple[str, int, str, bool]],
) -> Tuple[str, str]:
    copias_com_conteudo = [(p, t) for p, t in outras_copias if t > 0]
    tem_io_py = any(r[3] for r in refs)
    ext = os.path.splitext(nome)[1].lower()

    if copias_com_conteudo and refs:
        return (
            "POSSÍVEL SOBRA / CAMINHO ANTIGO COM CÓPIA ATIVA",
            "Há versão com conteúdo em outra pasta e menção em código. Confira se o script "
            "ainda aponta para este caminho vazio ou para a outra pasta antes de apagar.",
        )

    if copias_com_conteudo and not refs:
        return (
            "DUPLICATA VAZIA (HÁ CÓPIA COM CONTEÚDO EM OUTRA PASTA)",
            "Existe arquivo com o mesmo nome e tamanho > 0 em outro diretório e nenhuma "
            "referência direta em .py. Costuma ser candidato forte a remoção após conferência.",
        )

    if refs and (tem_io_py or ext in {".db", ".log", ".json"}):
        return (
            "REFERENCIADO NO CÓDIGO (PODE SER CRIADO/USADO PELO SISTEMA)",
            "Um script cita o arquivo ou parâmetro relacionado. Apagar sem checar o trecho "
            "pode fazer o código recriá-lo vazio ou gerar aviso/erro se esperar leitura.",
        )

    if not refs and not outras_copias:
        return (
            "SEM REFERÊNCIA EM .PY E SEM CÓPIA NO PROJETO",
            "Pode ser sobra de teste/experimento ou arquivo de apoio/mídia/rascunho. "
            "Verifique se algum script externo, HTML/CSS/JS, batch ou arquivo de config o usa.",
        )

    return (
        "REQUER CONFERÊNCIA MANUAL",
        "Há indícios parciais no projeto. Inspecione o arquivo e os scripts próximos antes de excluir.",
    )


def diagnosticar() -> None:
    raiz = os.path.abspath(os.path.dirname(__file__))
    todos = coletar_arquivos(raiz)
    zerados = [(rel, nome, mtime) for rel, nome, tam, mtime in todos if tam == 0]

    print("=" * 76)
    print(f"DIAGNÓSTICO DE ARQUIVOS ZERADOS (0 BYTES) — {raiz}")
    print("=" * 76)

    if not zerados:
        print("Nenhum arquivo de 0 bytes encontrado.")
        return

    por_nome: Dict[str, List[Tuple[str, int]]] = {}
    for rel, nome, tam, _ in todos:
        por_nome.setdefault(nome.lower(), []).append((rel, tam))

    alvos = [(rel, nome) for rel, nome, _ in zerados]
    refs_por_alvo = analisar_referencias_py(raiz, alvos)

    for idx, (rel, nome, mtime) in enumerate(zerados, start=1):
        dt_str = datetime.fromtimestamp(mtime).strftime("%d/%m/%Y %H:%M:%S")
        outras = [
            (outro_rel, outro_tam)
            for outro_rel, outro_tam in por_nome.get(nome.lower(), [])
            if outro_rel != rel
        ]
        refs = refs_por_alvo.get(rel, [])
        status_diag, orientacao = classificar_item(rel, nome, outras, refs)

        print(f"\n[{idx}] {rel}")
        print(f"    • Última modificação : {dt_str}")
        print(f"    • Diagnóstico       : {status_diag}")
        print(f"    • Orientação        : {orientacao}")

        if outras:
            outras_fmt = ", ".join(f"{p} ({t} B)" for p, t in outras)
            print(f"    • Mesmo nome em     : {outras_fmt}")
        else:
            print("    • Mesmo nome em     : nenhum outro arquivo com esse nome no projeto")

        if refs:
            print(f"    • Citações em .py ({len(refs)}):")
            for arq_py, num_l, trecho, tem_io in refs[:6]:
                tag_io = " [I/O/PATH]" if tem_io else ""
                print(f"        - {arq_py}:{num_l}{tag_io} -> {trecho}")
            if len(refs) > 6:
                print(f"        - ... (+{len(refs) - 6} citação(ões))")
        else:
            print("    • Citações em .py     : nenhuma menção encontrada nos arquivos .py")

    print("\n" + "=" * 76)
    print("Diagnóstico concluído. Nenhum arquivo foi modificado ou excluído.")
    print("=" * 76)


if __name__ == "__main__":
    diagnosticar()