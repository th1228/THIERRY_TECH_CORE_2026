# -*- coding: utf-8 -*-
"""
Módulo: audit_engine.py
Descrição: Varredura global compacta com guia de resolução para blocos except genéricos.
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, Any, List

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


class GenericExceptLocator(ast.NodeVisitor):
    """Percorre a árvore de sintaxe para encontrar blocos except genéricos ou vazios."""
    def __init__(self) -> None:
        self.blocos_encontrados: List[Dict[str, Any]] = []

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        is_generico = False
        if node.type is None:
            is_generico = True
        elif isinstance(node.type, ast.Name) and node.type.id == 'Exception':
            is_generico = True

        if is_generico:
            self.blocos_encontrados.append({
                "linha": node.lineno,
                "coluna": node.col_offset
            })
        self.generic_visit(node)


def varrer_projeto_inteiro(diretorio_raiz: str = ".") -> Dict[str, Any]:
    """Varre recursivamente todas as pastas em busca de ficheiros .py e analisa-os."""
    caminho_base = Path(diretorio_raiz)
    lista_consolidada = []
    pastas_ignoradas = {".venv", "venv", "__pycache__", ".git", "build", "dist"}

    for caminho_arquivo in caminho_base.rglob("*.py"):
        if any(parte in pastas_ignoradas for parte in caminho_arquivo.parts):
            continue

        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                linhas_codigo = f.readlines()

            conteudo_bruto = "".join(linhas_codigo)
            tree = ast.parse(conteudo_bruto)
            
            locator = GenericExceptLocator()
            locator.visit(tree)

            for item in locator.blocos_encontrados:
                num_linha = int(item["linha"])
                # Pega a linha exata do código limpa de espaços excessivos
                trecho_linha = linhas_codigo[num_linha - 1].strip() if 0 < num_linha <= len(linhas_codigo) else "N/A"
                
                lista_consolidada.append({
                    "arquivo": str(caminho_arquivo),
                    "linha": num_linha,
                    "codigo": trecho_linha
                })
        except (OSError, UnicodeDecodeError, SyntaxError, ValueError):
            pass

    return {
        "itens": lista_consolidada,
        "total": len(lista_consolidada)
    }


if __name__ == "__main__":
    print("🔍 A executar varredura global compacta...\n")
    resultado = varrer_projeto_inteiro(".")

    print("==================================================================================")
    print(f"               RELATÓRIO CONSOLIDADO: {resultado['total']} EXCEÇÕES GENÉRICAS")
    print("==================================================================================")
    print(f"{'FICHEIRO':<35} | {'LINHA':<6} | {'CÓDIGO ENCONTRADO'}")
    print("-" * 82)

    if resultado['total'] == 0:
        print("🎉 Parabéns! Nenhum bloco except genérico encontrado no projeto.")
    else:
        for item in resultado['itens']:
            # Encurta o caminho do arquivo se for muito longo para caber bonito no print
            arq_curto = (item['arquivo'][:32] + '..') if len(item['arquivo']) > 35 else item['arquivo']
            print(f"{arq_curto:<35} | {item['linha']:<6} | {item['codigo']}")

    print("==================================================================================")
    print("                     GUIA PRÁTICO DE COMO RESOLVER")
    print("==================================================================================")
    print("• O problema do 'except:' ou 'except Exception:' puro é que ele oculta erros")
    print("  críticos de sintaxe, digitação ou falhas de sistema inesperadas.")
    print("• **Como corrigir:** Substitua por exceções específicas baseadas no contexto:")
    print("    1. Se lê ficheiros  -> use `except (FileNotFoundError, IOError):`")
    print("    2. Se converte dados -> use `except (ValueError, TypeError):`")
    print("    3. Se acessa chaves  -> use `except KeyError:`")
    print("    4. Se usa APIs/Web   -> use exceções específicas da biblioteca ou `requests.exceptions.RequestException`")
    print("==================================================================================")
