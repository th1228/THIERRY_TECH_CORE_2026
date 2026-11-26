# -*- coding: utf-8 -*-
"""
Script Pontual: patch_tricologia_ultra.py
Objetivo: Remover/limpar exclusivamente referências a herpes (ex.: "herpes simplex",
          "simplex virale") em atualizar_tricologia_ultra.py, com backup automático
          e preservação integral do restante do arquivo.
"""

import datetime
import os
import re
import shutil
import sys
from typing import List


ALVO_ARQUIVO = "atualizar_tricologia_ultra.py"

PADROES_HERPES = [
    # Remove frases inteiras que mencionem herpes (PT / EN / variações)
    re.compile(
        r"[^.!?\n\r;]*\bherpes(?:\s+simplex(?:\s+vir(?:al|ale))?)?\b[^.!?\n\r;]*[.!?;]?",
        flags=re.IGNORECASE,
    ),
    # Remove qualquer menção residual solta à palavra "herpes"
    re.compile(r"\bherpes\b", flags=re.IGNORECASE),
]


def _localizar_arquivo(nome_arquivo: str) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidatos = [
        os.path.join(base_dir, nome_arquivo),
        os.path.join(os.getcwd(), nome_arquivo),
        os.path.join(base_dir, "core", nome_arquivo),
    ]
    for caminho in candidatos:
        if os.path.isfile(caminho):
            return caminho
    raise FileNotFoundError(f"Arquivo '{nome_arquivo}' não encontrado nas pastas padrão.")


def _limpar_trecho_herpes(texto: str) -> str:
    limpo = texto
    for padrao in PADROES_HERPES:
        limpo = padrao.sub("", limpo)

    # Ajusta separadores duplos ou espaços extras deixados após remover uma frase
    limpo = re.sub(r"\s*-\s*-\s*", " - ", limpo)
    limpo = re.sub(r"[ \t]{2,}", " ", limpo)
    limpo = re.sub(r"\(\s*\)", "", limpo)
    limpo = re.sub(r"\[\s*\]", "", limpo)
    limpo = re.sub(r"\n{3,}", "\n\n", limpo)
    return limpo


def aplicar_patch_herpes(caminho_arquivo: str) -> None:
    with open(caminho_arquivo, "r", encoding="utf-8", errors="replace") as f:
        linhas_originais = f.readlines()

    carimbo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_backup = f"{caminho_arquivo}.bak_{carimbo}"
    shutil.copy2(caminho_arquivo, caminho_backup)
    print(f"[BACKUP] Criado em: {caminho_backup}")

    linhas_alteradas: List[int] = []
    novas_linhas: List[str] = []

    for idx, linha in enumerate(linhas_originais, start=1):
        if "herpes" in linha.lower():
            nova_linha = _limpar_trecho_herpes(linha)
            if nova_linha != linha:
                linhas_alteradas.append(idx)
            novas_linhas.append(nova_linha)
        else:
            novas_linhas.append(linha)

    conteudo_final = "".join(novas_linhas)

    # Validação de sintaxe Python antes de gravar o arquivo final
    compile(conteudo_final, caminho_arquivo, "exec")

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo_final)

    print(f"[CONCLUÍDO] Arquivo atualizado: {caminho_arquivo}")
    if linhas_alteradas:
        print(f"[LINHAS ALTERADAS] {linhas_alteradas}")
    else:
        print("[AVISO] Nenhuma ocorrência de 'herpes' foi encontrada para alteração.")


if __name__ == "__main__":
    try:
        alvo = _localizar_arquivo(ALVO_ARQUIVO)
        aplicar_patch_herpes(alvo)
    except Exception as erro:
        print(f"[ERRO] {erro}")
        sys.exit(1)