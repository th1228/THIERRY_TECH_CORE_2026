# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
Script dedicado para conectar automaticamente os modulos de
core/tricologia_saude/ ao memoria_tricologia_helper.py (memoria_comum).
===========================================================================
"""

import argparse
import os
import re
from pathlib import Path
from typing import List, Tuple


IMPORT_LINHA = "from .memoria_tricologia_helper import registrar_na_memoria_comum"

ARQUIVOS_IGNORADOS = {
    "__init__.py",
    "memoria_tricologia_helper.py",
    "help_memoria_tricologia_help.py",
    "aplicar_memoria_tricologia.py",
}


def _deduzir_nome_secao(nome_arquivo: str) -> str:
    base = Path(nome_arquivo).stem.lower()
    for prefixo in ("analise_", "protocolo_", "detector_", "correlacao_"):
        if base.startswith(prefixo):
            base = base[len(prefixo) :]
            break
    return re.sub(r"[^a-z0-9_]+", "_", base).strip("_") or "modulo_trico"


def _inserir_import(conteudo: str) -> Tuple[str, bool]:
    if IMPORT_LINHA in conteudo:
        return conteudo, False

    linhas = conteudo.splitlines(keepends=True)
    idx_insercao = 0

    for i, linha in enumerate(linhas):
        stripped = linha.strip()
        if stripped.startswith(("import ", "from ")):
            idx_insercao = i + 1
        elif idx_insercao > 0 and stripped and not stripped.startswith("#"):
            # Terminou o bloco inicial de imports
            break

    nova_linha = f"{IMPORT_LINHA}\n"
    if idx_insercao == 0:
        # Após docstring inicial ou cabeçalho
        for i, linha in enumerate(linhas):
            if linha.strip().startswith(("import ", "from ", "def ", "class ")):
                idx_insercao = i
                break

    linhas.insert(idx_insercao, nova_linha)
    return "".join(linhas), True


def _inserir_chamadas_retorno(conteudo: str, secao: str) -> Tuple[str, int]:
    """
    Insere registrar_na_memoria_comum(...) imediatamente antes de linhas
    'return <variavel>' que pareçam retornar um relatorio/resultado.
    """
    if "registrar_na_memoria_comum(" in conteudo:
        return conteudo, 0

    linhas = conteudo.splitlines(keepends=True)
    alteracoes = 0
    novas_linhas: List[str] = []

    padrao_return = re.compile(r"^(\s*)return\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:#.*)?$")

    for linha in linhas:
        sem_quebra = linha.rstrip("\r\n")
        quebra = linha[len(sem_quebra) :] if len(linha) > len(sem_quebra) else "\n"
        match = padrao_return.match(sem_quebra)

        if match:
            indent = match.group(1)
            var_retorno = match.group(2)
            # Evita interceptar retornos simples de booleanos/strings/None
            if var_retorno.lower() not in {"none", "true", "false", "self"}:
                chamada = (
                    f"{indent}try:\n"
                    f"{indent}    _payload_mem = {var_retorno}.para_dict() if hasattr({var_retorno}, 'para_dict') else {var_retorno}\n"
                    f"{indent}    _cliente_mem = getattr({var_retorno}, 'cliente', None) or getattr({var_retorno}, 'nome_cliente', None) or 'Paciente / Cliente'\n"
                    f"{indent}    registrar_na_memoria_comum('{secao}', _payload_mem, cliente=_cliente_mem)\n"
                    f"{indent}except Exception:\n"
                    f"{indent}    pass\n"
                )
                novas_linhas.append(chamada)
                alteracoes += 1

        novas_linhas.append(sem_quebra + quebra)

    return "".join(novas_linhas), alteracoes


def processar_pasta(pasta_alvo: Path, aplicar: bool = False) -> None:
    if not pasta_alvo.exists() or not pasta_alvo.is_dir():
        print(f"[ERRO] Pasta não encontrada: {pasta_alvo}")
        return

    arquivos_py = sorted(
        p for p in pasta_alvo.glob("*.py") if p.name not in ARQUIVOS_IGNORADOS
    )

    if not arquivos_py:
        print(f"[AVISO] Nenhum módulo encontrado em: {pasta_alvo}")
        return

    modo = "APLICANDO ALTERAÇÕES" if aplicar else "SIMULAÇÃO (--dry-run)"
    print(f"=== {modo} em {pasta_alvo} ===")

    for arquivo in arquivos_py:
        secao = _deduzir_nome_secao(arquivo.name)
        original = arquivo.read_text(encoding="utf-8")

        atualizado, import_adicionado = _inserir_import(original)
        atualizado, qtd_retornos = _inserir_chamadas_retorno(atualizado, secao)

        if not import_adicionado and qtd_retornos == 0:
            print(f"  [OK / SEM MUDANÇA] {arquivo.name} (seção: '{secao}')")
            continue

        if aplicar:
            arquivo.write_text(atualizado, encoding="utf-8")
            print(
                f"  [ATUALIZADO] {arquivo.name} -> seção='{secao}' "
                f"(import={import_adicionado}, pontos_retorno={qtd_retornos})"
            )
        else:
            print(
                f"  [PREVISTO] {arquivo.name} -> seção='{secao}' "
                f"(import={import_adicionado}, pontos_retorno={qtd_retornos})"
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Conecta módulos de Tricologia & Saúde ao memoria_tricologia_helper.py."
    )
    parser.add_argument(
        "--pasta",
        type=str,
        default=None,
        help="Caminho para core/tricologia_saude (opcional; detecta automaticamente).",
    )
    parser.add_argument(
        "--aplicar",
        action="store_true",
        help="Grava as alterações nos arquivos. Sem esta flag, roda apenas em simulação.",
    )
    args = parser.parse_args()

    if args.pasta:
        pasta = Path(args.pasta).resolve()
    else:
        aqui = Path(__file__).resolve()
        # Se o script estiver dentro de tricologia_saude, usa o próprio diretório; senão procura core/tricologia_saude
        if aqui.parent.name == "tricologia_saude":
            pasta = aqui.parent
        elif (aqui.parent / "core" / "tricologia_saude").exists():
            pasta = aqui.parent / "core" / "tricologia_saude"
        elif (aqui.parent.parent / "core" / "tricologia_saude").exists():
            pasta = aqui.parent.parent / "core" / "tricologia_saude"
        else:
            pasta = aqui.parent

    processar_pasta(pasta, aplicar=args.aplicar)

    if not args.aplicar:
        print("\nDica: revise a prévia acima e rode com '--aplicar' para salvar nos arquivos.")


if __name__ == "__main__":
    main()