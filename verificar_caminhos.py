import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys
import os

print(f"Diretório atual: {os.getcwd()}")
print("\nCaminhos de busca do Python (sys.path):")
for path in sys.path:
    print(path)

# Verifica se o arquivo existe na pasta atual
arquivo = "Monaco_nucleo_acesso.py"
if os.path.exists(arquivo):
    print(f"\n[OK] O arquivo {arquivo} foi encontrado na pasta raiz.")
else:
    print(f"\n[ERRO] O arquivo {arquivo} não foi encontrado na pasta raiz.")