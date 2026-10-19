
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

# -*- coding: utf-8 -*-
"""
Script de Diagnóstico Corrigido para a Pasta Core
"""
import os
import sys

# Garante que a pasta pai e a pasta core estão no path do Python
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.dirname(ROOT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

print("=" * 60)
print("DIAGNÓSTICO DE MÓDULOS E GERAÇÃO DE PDFS (CORRIGIDO)")
print("=" * 60)

# Mapeamento real baseado nos arquivos visíveis na pasta core
modulos_para_testar = [
    ("Carta Internacional", "carta_internacional"),
    ("Clínica Estética / Tricologia", "clinica_estetica_roi"),
    ("Biometria", "biometria"),
    ("C2 Sovereign", "c2_sovereign_intelli"),
]

for nome_amigavel, nome_arquivo in modulos_para_testar:
    print(f"\n[TESTANDO] {nome_amigavel} ({nome_arquivo}.py)...")
    try:
        mod = __import__(nome_arquivo)
        print(f"  -> Módulo '{nome_arquivo}' importado com sucesso!")
        
        # Lista funções ou classes disponíveis no arquivo
        componentes = [c for c in dir(mod) if not c.startswith("_")]
        print(f"  -> Componentes disponíveis: {componentes}")
        
    except Exception as e:
        print(f"  -> FALHA AO IMPORTAR {nome_arquivo}: {e}")

print("\n" + "=" * 60)
print("Fim do diagnóstico.")
print("=" * 60)