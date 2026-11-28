# -*- coding: utf-8 -*-
import datetime
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

import guardiao_organizador as g


def _formatar_data(caminho: str) -> str:
    try:
        ts = os.path.getmtime(caminho)
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "desconhecida"


def _formatar_kb(caminho: str) -> str:
    try:
        return f"{os.path.getsize(caminho) / 1024:.1f} KB"
    except Exception:
        return "0.0 KB"


def _sugerir_acao(rel: str) -> str:
    if "/" not in rel:
        return "MOVER -> ajustes_auditoria/ (solto na raiz; conferir se nada chama por caminho fixo)"
    return "AVALIAR MOVER -> ajustes_auditoria/ (conferir imports/referências antes de aplicar)"


def listar_pendentes_nivel3_detalhado() -> list[dict]:
    raiz = g.descobrir_raiz()
    aceitas = {p.strip().lower() for p in g.PASTAS_AUDITORIA_ACEITAS}
    detalhes: list[dict] = []

    for pasta_atual, subdirs, arquivos in os.walk(raiz):
        subdirs[:] = [d for d in subdirs if d not in g.PASTAS_IGNORADAS]
        rel_dir = os.path.relpath(pasta_atual, raiz).replace("\\", "/").lower()
        partes_dir = set() if rel_dir == "." else set(rel_dir.split("/"))

        em_arquivo = bool(partes_dir & g.PASTAS_ARQUIVO)
        em_auditoria = bool(partes_dir & aceitas)
        if em_arquivo or em_auditoria:
            continue

        for nome in sorted(arquivos):
            if g.eh_arquivo_auditoria_ou_ajuste(nome):
                caminho = os.path.join(pasta_atual, nome)
                rel = os.path.relpath(caminho, raiz).replace("\\", "/")
                detalhes.append(
                    {
                        "arquivo": rel,
                        "linhas": g.contar_linhas(caminho),
                        "tamanho": _formatar_kb(caminho),
                        "modificado": _formatar_data(caminho),
                        "decisao": _sugerir_acao(rel),
                    }
                )

    return detalhes


if __name__ == "__main__":
    itens = listar_pendentes_nivel3_detalhado()
    print(f"Total de arquivos pendentes no Nível 3: {len(itens)}")
    print("-" * 68)
    if not itens:
        print("Nenhum arquivo pendente fora das pastas aceitas.")
    else:
        for idx, item in enumerate(itens, start=1):
            print(f"{idx}. {item['arquivo']}")
            print(f"   Linhas     : {item['linhas']} | Tamanho: {item['tamanho']} | Modificado: {item['modificado']}")
            print(f"   No ponto de: {item['decisao']}")
            print("-" * 68)