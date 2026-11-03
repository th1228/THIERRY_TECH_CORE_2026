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

import importlib.metadata
import os
import sys


def verificar_dependencias(requirements_path="requirements.txt"):
  print("=" * 60)
  print(" [TCC GLOBAL CORP] — MONITOR DE INTEGRIDADE DE DEPENDÊNCIAS")
  print("=" * 60)

  if not os.path.exists(requirements_path):
    print(f" [AVISO] Arquivo '{requirements_path}' não encontrado na raiz.")
    return False

  divergencias = 0
  checados = 0

  with open(requirements_path, "r", encoding="utf-8") as f:
    linhas = f.readlines()

  for linha in linhas:
    linha = linha.strip()
    if not linha or linha.startswith("#"):
      continue

    # Identifica o formato do requisito (== ou >=)
    if "==" in linha:
      pacote_esperado, versao_esperada = linha.split("==")
      operador = "=="
    elif ">=" in linha:
      pacote_esperado, versao_esperada = linha.split(">=")
      operador = ">="
    else:
      pacote_esperado = linha
      versao_esperada = None
      operador = None

    pacote_esperado = pacote_esperado.strip()
    checados += 1

    try:
      versao_atual = importlib.metadata.version(pacote_esperado)
      if operador == "==" and versao_atual != versao_esperada.strip():
        print(
            f" [ATENÇÃO] {pacote_esperado}: Instalada ({versao_atual}) diverge"
            f" da versão homologada ({versao_esperada.strip()})."
        )
        divergencias += 1
      else:
        print(f" [OK] {pacote_esperado} v{versao_atual} — Sincronizado.")
    except importlib.metadata.PackageNotFoundError:
      print(f" [FALHA] O pacote essencial '{pacote_esperado}' não está instalado.")
      divergencias += 1

  print("\n" + "=" * 60)
  print(f" - Pacotes Analisados  : {checados}")
  print(f" - Avisos de Divergência: {divergencias}")
  if divergencias == 0:
    print(" - STATUS DO AMBIENTE  : ESTÁVEL E SEGURO PARA EXECUÇÃO")
  else:
    print(" - STATUS DO AMBIENTE  : ATENÇÃO REQUERIDA NAS BIBLIOTECAS")
  print("=" * 60)
  return divergencias == 0


if __name__ == "__main__":
  verificar_dependencias()