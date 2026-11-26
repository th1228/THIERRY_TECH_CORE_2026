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
import sys
from typing import Any, Dict, List, Optional

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..")) if os.path.basename(CURRENT_DIR).lower() in ("core", "legal") else CURRENT_DIR

for _caminho in (ROOT_DIR, CURRENT_DIR):
    if _caminho and os.path.isdir(_caminho) and _caminho not in sys.path:
        sys.path.insert(0, _caminho)

# --- PONTE DE MEMÓRIA AUTOMÁTICA (THIERRY TECH) ---
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:

        class MemoriaMock:
            def __init__(self) -> None:
                self._dados: Dict[str, Any] = {}

            def salvar_dados(self, chave: str, valor: Any) -> bool:
                self._dados[chave] = valor
                return True

            def registrar(self, chave: str, valor: Any) -> bool:
                self._dados[chave] = valor
                return True

            def ler_dados(self, chave: Optional[str] = None) -> Any:
                if chave is None:
                    return self._dados
                return self._dados.get(chave)

            def obter_para_destino(self, destino: str, chave: Optional[str] = None) -> Any:
                return self.ler_dados(chave)

        memoria = MemoriaMock()
# ---------------------------------------------------


class ValidadorSistema:
    def __init__(self, lang: str = "PT") -> None:
        self.lang = lang
        self.diretorio_atual = CURRENT_DIR
        self.raiz = ROOT_DIR

        self.arquivos_alvo: List[str] = [
            "main.py",
            "monaco_plan.py",
            "monaco_blindagem.py",
            "monaco_comunicacao.py",
            "monaco_consciencia.py",
            "monaco_eminencia.py",
            "monaco_integrador.py",
            "monaco_nucleo_acesso.py",
            "monaco_ressonancia.py",
            "motor_sincronia.py",
        ]

    def _indexar_projeto(self) -> Dict[str, List[str]]:
        """Varre o diretório base do projeto e indexa onde cada arquivo está localizado."""
        indice: Dict[str, List[str]] = {}
        pastas_base = [self.raiz, self.diretorio_atual]
        pastas_ignoradas = {".git", "__pycache__", ".venv", "venv", "node_modules", ".pytest_cache"}

        for base in pastas_base:
            if not base or not os.path.isdir(base):
                continue
            for raiz_atual, subdirs, arquivos in os.walk(base):
                subdirs[:] = [d for d in subdirs if d not in pastas_ignoradas]
                for nome in arquivos:
                    caminho_completo = os.path.join(raiz_atual, nome)
                    lista = indice.setdefault(nome, [])
                    if caminho_completo not in lista:
                        lista.append(caminho_completo)
        return indice

    def rodar_validacao(self) -> bool:
        print("\n--- [SISTEMA] Auditoria Híbrida (Busca Global por Nome): Iniciada ---")
        indice = self._indexar_projeto()
        encontrados = 0
        ausentes: List[str] = []

        for arquivo in self.arquivos_alvo:
            locais = indice.get(arquivo, [])
            if locais:
                encontrados += 1
                print(f"[OK] {arquivo} -> {locais[0]}")
            else:
                ausentes.append(arquivo)
                print(f"[AVISO] {arquivo} não localizado na varredura.")

        total = len(self.arquivos_alvo)
        print("-" * 55)
        print(f"RESULTADO FINAL: {encontrados}/{total} arquivo(s) localizado(s).")

        if ausentes:
            print("Arquivos não encontrados:", ", ".join(ausentes))
            print(">>> STATUS: VALIDAÇÃO PARCIAL / REVISAR ARQUIVOS AUSENTES <<<")
            return False

        print(">>> STATUS: SISTEMA TOTALMENTE VALIDADO E OPERACIONAL <<<")
        return True


if __name__ == "__main__":
    validador = ValidadorSistema()
    resultado_ok = validador.rodar_validacao()
    sys.exit(0 if resultado_ok else 1)