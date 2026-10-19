# -*- coding: utf-8 -*-
import sys
import os

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
# -----------------------------------------------

class MemoriaTTC:
    def __init__(self, lang: str = "PT"):
        self._dados = {}
        print("[MEMÓRIA TTC] Instância global de estado iniciada com sucesso.")

    def salvar_dados(self, chave, valor):
        """Salva ou atualiza um dado no barramento global de memória."""
        self._dados[chave] = valor

    def ler_dados(self, chave):
        """Lê um dado específico do barramento global."""
        return self._dados.get(chave, None)

    def listar_tudo(self):
        """Retorna todo o dicionário de estado global."""
        return self._dados

# Instância global padrão para ser importada por todos os motores 🧠
instancia_memoria = MemoriaTTC()