# -*- coding: utf-8 -*-
"""
Auditoria Final de Conectividade: Thierry Technology Concept Global
Verifica se todos os motores ativos possuem código de integração ativo.
"""

import os

def verificar_status():
    print("\n" + "═" * 65)
    print("   AUDITORIA FINAL: VERIFICAÇÃO DE INTEGRAÇÃO DE MOTORES")
    print("═" * 65)

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    termos_busca = ["memoria_comum", "memoria_global", "instancia_memoria", "salvar_dados", "registrar"]

    arquivos_py = []
    for f in os.listdir(diretorio_atual):
        if f.endswith('.py') and f != 'verificar_status_final.py':
            arquivos_py.append(f)
    
    pasta_core = os.path.join(diretorio_atual, 'core')
    if os.path.exists(pasta_core) and os.path.isdir(pasta_core):
        for f in os.listdir(pasta_core):
            if f.endswith('.py'):
                arquivos_py.append(os.path.join('core', f))

    total_integrados = 0
    total_verificados = 0

    for arq in arquivos_py:
        caminho_completo = os.path.join(diretorio_atual, arq)
        try:
            with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as arquivo:
                conteudo = arquivo.read()
                
            encontrados = [termo for termo in termos_busca if termo in conteudo]
            total_verificados += 1
            
            if len(encontrados) >= 1:
                print(f" [INTEGRADO] 🟢 {arq}")
                print(f"    └─ Elementos detectados: {', '.join(encontrados)}")
                total_integrados += 1
            else:
                print(f" [PENDENTE]  🔴 {arq}")
        except Exception as e:
            print(f" [ERRO AO LER] 🔴 {arq}: {e}")

        print("-" * 65)

    print(f"\nResumo Final: {total_integrados} de {total_verificados} arquivos estão integrados e prontos!")
    print("═" * 65 + "\n")

if __name__ == "__main__":
    verificar_status()