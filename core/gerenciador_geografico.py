# -*- coding: utf-8 -*-
import sys
import os
import json

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

class GerenciadorGeografico:
    def __init__(self, pasta_config='config/paises'):
        self.pasta_config = pasta_config
        self.configuracao_ativa = None

    def carregar_pais(self, codigo_iso):
        """Carrega o JSON do país, define as regras e sincroniza com a Memória Comum 🧠."""
        caminho = os.path.join(self.pasta_config, f"{codigo_iso}.json")
        if os.path.exists(caminho):
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    self.configuracao_ativa = json.load(f)
                
                # Sincronização automática com a Memória Comum 🧠
                memoria.salvar_dados("contexto_geografico", codigo_iso)
                memoria.salvar_dados("configuracao_geografica_ativa", self.configuracao_ativa)
                
                print(f"[SISTEMA] Contexto geográfico definido e sincronizado: {codigo_iso}")
                return self.configuracao_ativa
            except Exception as e:
                print(f"[ERRO] Falha ao processar JSON do país {codigo_iso}: {e}")
                return None
        else:
            print(f"[ERRO] País {codigo_iso} não configurado em {caminho}.")
            return None

    def obter(self, chave):
        """Retorna uma regra específica do país ativo"""
        return self.configuracao_ativa.get(chave) if self.configuracao_ativa else None

# Instância global para ser usada em todo o sistema
gerente_geo = GerenciadorGeografico()

def processar(frame=None, codigo_iso="KR"):
    """Função de compatibilidade direta com o orquestrador 💻."""
    return gerente_geo.carregar_pais(codigo_iso)