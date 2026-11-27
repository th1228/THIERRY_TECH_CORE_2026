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

import os
from collections import defaultdict
from typing import Dict, List, Tuple

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

EXTENSOES_SAIDA_BINARIA = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".mp3", ".wav", ".zip"}


def descobrir_raiz() -> str:
    atual = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(atual).lower() in ("core", "legal", "scripts", "tools", "web"):
        pai = os.path.abspath(os.path.join(atual, ".."))
        if os.path.isdir(pai):
            return pai
    return atual


def contar_linhas_seguro(caminho: str) -> int:
    try:
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def classificar_modulo(rel_path: str, nome: str) -> str:
    baixo_path = rel_path.replace("\\", "/").lower()
    baixo_nome = nome.lower()

    if baixo_path.startswith("pdfs_finais/") or baixo_nome.endswith(".pdf"):
        return "Saidas / PDFs Gerados"
    if (
        ".bak" in baixo_nome
        or "backup" in baixo_nome
        or baixo_nome.startswith("teste_")
        or baixo_nome.startswith("test_")
        or baixo_nome.startswith("corrigir_")
        or baixo_nome.startswith("patch_")
        or baixo_nome.startswith("atualizar_")
    ):
        return "Backups, Patches e Testes"
    if baixo_nome.endswith((".html", ".htm", ".css", ".js")) or baixo_path.startswith(("web/", "frontend/")):
        return "Interface Web (HTML / CSS / JS)"
    if "contrato" in baixo_nome or "juridic" in baixo_nome or "monaco" in baixo_nome or baixo_path.startswith("legal/"):
        return "Juridico e Jurisdicao"
    if "memoria" in baixo_nome or "estado_sistema" in baixo_nome or "sessao" in baixo_nome:
        return "Memoria e Estado"
    if (
        "validador" in baixo_nome
        or "verificador" in baixo_nome
        or "diagnostico" in baixo_nome
        or "auditor" in baixo_nome
        or "varredura" in baixo_nome
    ):
        return "Validadores e Diagnosticos"
    if "engine" in baixo_nome or "motor" in baixo_nome or "orquestrador" in baixo_nome or "dossie" in baixo_nome or baixo_path.startswith("core/"):
        return "Nucleo, Motores e Orquestracao"
    if baixo_nome == "main.py":
        return "Entrada Principal (main.py)"
    return "Utilitarios e Outros"


def auditar_organizacao(raiz: str) -> None:
    total_arquivos = 0
    total_linhas = 0
    por_modulo: Dict[str, List[Tuple[str, int, float]]] = defaultdict(list)
    por_extensao: Dict[str, int] = defaultdict(int)
    arquivos_grandes: List[Tuple[str, int]] = []
    soltos_na_raiz: List[str] = []
    candidatos_limpeza: List[str] = []

    for pasta_atual, subdirs, arquivos in os.walk(raiz):
        subdirs[:] = [d for d in subdirs if d not in PASTAS_IGNORADAS]

        for nome in sorted(arquivos):
            caminho = os.path.join(pasta_atual, nome)
            rel = os.path.relpath(caminho, raiz)
            ext = os.path.splitext(nome)[1].lower() or "(sem_ext)"

            total_arquivos += 1
            por_extensao[ext] += 1

            try:
                tamanho_kb = os.path.getsize(caminho) / 1024.0
            except Exception:
                tamanho_kb = 0.0

            linhas = contar_linhas_seguro(caminho) if ext in EXTENSOES_CODIGO else 0
            total_linhas += linhas

            modulo = classificar_modulo(rel, nome)
            por_modulo[modulo].append((rel, linhas, tamanho_kb))

            if linhas >= 1000:
                arquivos_grandes.append((rel, linhas))

            if os.path.dirname(rel) == "" and ext == ".py" and nome != "main.py":
                soltos_na_raiz.append(rel)

            if modulo == "Backups, Patches e Testes":
                candidatos_limpeza.append(rel)

    print("=" * 72)
    print("AUDITORIA DE ORGANIZACAO POR MODULO - DIAGNOSTICO ATUAL")
    print("=" * 72)
    print(f"Pasta base : {raiz}")
    print(f"Arquivos   : {total_arquivos}")
    print(f"Linhas (cod): {total_linhas:,}".replace(",", "."))
    print("-" * 72)

    print("\n1. DISTRIBUICAO POR MODULO / FUNCAO")
    for modulo in sorted(por_modulo.keys()):
        itens = por_modulo[modulo]
        qtd = len(itens)
        lin_mod = sum(x[1] for x in itens)
        print(f"  - {modulo:<34} | {qtd:>3} arq | {lin_mod:>7} linhas")

    print("\n2. DISTRIBUICAO POR EXTENSAO")
    for ext, qtd in sorted(por_extensao.items(), key=lambda x: (-x[1], x[0])):
        print(f"  - {ext:<12} : {qtd} arquivo(s)")

    print("\n3. ARQUIVOS MAIORES (>= 1.000 LINHAS)")
    if arquivos_grandes:
        for rel, lin in sorted(arquivos_grandes, key=lambda x: -x[1])[:15]:
            print(f"  - {lin:>6} linhas -> {rel}")
    else:
        print("  - Nenhum arquivo acima de 1.000 linhas.")

    print(f"\n4. SCRIPTS SOLTOS NA RAIZ (.PY EXCETO MAIN.PY): {len(soltos_na_raiz)}")
    for rel in soltos_na_raiz[:20]:
        print(f"  - {rel}")
    if len(soltos_na_raiz) > 20:
        print(f"  ... e mais {len(soltos_na_raiz) - 20} arquivo(s).")

    print(f"\n5. BACKUPS, PATCHES, TEMPORARIOS E TESTES: {len(candidatos_limpeza)}")
    for rel in candidatos_limpeza[:20]:
        print(f"  - {rel}")
    if len(candidatos_limpeza) > 20:
        print(f"  ... e mais {len(candidatos_limpeza) - 20} arquivo(s).")

    print("\n" + "=" * 72)
    print("6. POR ONDE COMECAR A ORGANIZAR (ORDEM SEGURA)")
    print("=" * 72)
    print(
        "Passo 1 - Congelar o que ja funciona:\n"
        "  Nao mexa de imediato nos motores validados e no fluxo principal.\n"
        "  Use o verificador final como referencia antes e depois de cada etapa.\n\n"
        "Passo 2 - Separar rascunho/backup/teste do codigo ativo:\n"
        "  Mova backups (.bak, copias), patches pontuais e scripts de teste para\n"
        "  uma pasta isolada (ex.: _archive/ ou labs/) para limpar a visao.\n\n"
        "Passo 3 - Agrupar interfaces Web (HTML/CSS/JS):\n"
        "  Reuna paginas HTML, estilos e scripts de front-end em web/ (ou\n"
        "  frontend/), mantendo caminhos e referencias atualizados com cuidado.\n\n"
        "Passo 4 - Organizar validadores e diagnosticos:\n"
        "  Junte verificadores, auditores e scripts de diagnostico em scripts/\n"
        "  ou checks/, deixando o nucleo em core/ e regras juridicas em legal/.\n\n"
        "Passo 5 - Quebrar apenas arquivos gigantes/misturados:\n"
        "  Só depois que as pastas estiverem limpas, divida arquivos muito longos\n"
        "  ou com muitas responsabilidades em funcoes/modulos menores, testando a\n"
        "  cada commit no Git."
    )
    print("=" * 72)


if __name__ == "__main__":
    auditar_organizacao(descobrir_raiz())