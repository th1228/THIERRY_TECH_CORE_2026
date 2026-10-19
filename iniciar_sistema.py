# -*- coding: utf-8 -*-
import subprocess
import sys
from pathlib import Path

DEPENDENCIAS = [
    "fastapi", 
    "uvicorn", 
    "pydantic", 
    "opencv-python", 
    "pillow", 
    "numpy", 
    "reportlab", 
    "pymupdf", 
    "cryptography", 
    "weasyprint"
]

def verificar_e_instalar():
    print("[TCC] A verificar integridade do ambiente...")
    for pacote in DEPENDENCIAS:
        nome_import = pacote.replace("-python", "").replace("pymupdf", "fitz")
        try:
            __import__(nome_import)
        except ImportError:
            print(f"[TCC] A instalar dependência em falta: {pacote}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
    print("[TCC] Ambiente verificado com sucesso.")

if __name__ == "__main__":
    verificar_e_instalar()
    caminho_main = Path(__file__).resolve().parent / "main.py"
    if caminho_main.exists():
        print(f"[TCC] A iniciar o orquestrador principal na porta 801...")
        subprocess.run([sys.executable, str(caminho_main)])
    else:
        print("[ERRO] O ficheiro 'main.py' não foi encontrado na pasta.")