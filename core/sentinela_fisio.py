import sys, os

import sys, os

# -*- coding: utf-8 -*-
import sys
import os

# Adiciona a raiz (THIERRY_TECH_CORE_2026) ao Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# IMPORTAÇÃO CORRETA:
# Você entra na pasta 'core' e pega o arquivo 'biometria.py'
from core import biometria

# Se precisar de uma função específica dentro do arquivo:
# from core.biometria import obter_laudo_biometrico
# --- ADICIONE ESTE TESTE DE VIDA AO FINAL DO SENTINELA ---
if __name__ == "__main__":
    print("\n--- [SENTINELA] STATUS CHECK ---")
    try:
        # Tenta carregar o módulo para confirmar que o caminho está certo
        from core import biometria
        print("[SENTINELA] Motor de Biometria: OK")
        print("[SENTINELA] Sentinela está vigiando as metas.")
    except Exception as e:
        print(f"[SENTINELA] ERRO: Falha ao carregar motor de biometria: {e}")
    print("---------------------------------\n")