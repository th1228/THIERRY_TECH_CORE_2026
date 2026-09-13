import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os

# O código que queremos injetar no topo de cada arquivo
ponte = """import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""

pasta_core = 'core'

for nome_arquivo in os.listdir(pasta_core):
    if nome_arquivo.endswith('.py') and nome_arquivo != '__init__.py':
        caminho_completo = os.path.join(pasta_core, nome_arquivo)
        
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            
        # Verifica se a ponte já não existe para não duplicar
        if "sys.path.insert" not in conteudo:
            with open(caminho_completo, 'w', encoding='utf-8') as f:
                f.write(ponte + "\n" + conteudo)
                print(f"[OK] Ponte injetada em: {nome_arquivo}")
        else:
            print(f"[SKIP] Já possui ponte: {nome_arquivo}")

print("--- Manutenção concluída ---")