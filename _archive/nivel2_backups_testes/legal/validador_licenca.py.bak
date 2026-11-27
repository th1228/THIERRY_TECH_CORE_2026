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


# --- PONTE DE MEMÓRIA AUTOMÁTICA (THIERRY TECH) ---
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:
        class MemoriaMock:
            def salvar_dados(self, chave, valor): pass
            def registrar(self, chave, valor): pass
            def ler_dados(self, chave): return None
        memoria = MemoriaMock()
# ---------------------------------------------------

import hashlib
import os
import platform
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -*- coding: utf-8 -*-
"""
TTC GLOBAL - VALIDADOR DE LICENÇA E VARREDURA LOCAL
Localização: core/validador_licenca.py
"""


class ValidadorLocal:

  def __init__(self, lang: str = "PT"):
    self.diretorio_base = os.getcwd()

  def varrer_servidor_local(self):
    """Simula ou executa a varredura de integridade no ambiente local."""
    print("[TTC SECURITY] Iniciando varredura de ambiente local...")

    # Exemplo de verificação de diretórios essenciais do ecossistema
    pastas_criticas = ["core", "config"]
    status_integridade = True

    for pasta in pastas_criticas:
      caminho = os.path.join(self.diretorio_base, pasta)
      if os.path.exists(caminho):
        print(f"[OK] Diretório seguro verificado: {pasta}/")
      else:
        print(f"[ALERTA] Diretório ausente: {pasta}/")
        status_integridade = False

    # Identificação de hardware básico para amarrar a licença à máquina
    node_id = platform.node()
    assinatura_maquina = (
        hashlib.sha256(node_id.encode()).hexdigest()[:16].upper()
    )

    print(f"[SECURITY] Nó de Hardware Validado: {assinatura_maquina}")

    if status_integridade:
      return True, f"Soberania Local Confirmada ({assinatura_maquina})"
    else:
      return False, "Falha de Integridade no Ambiente"