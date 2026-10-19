# -*- coding: utf-8 -*-
import os
from pathlib import Path

# Termo exato que aparece na imagem impressa no PDF
TERMO_ALVO = "thiébry"

def varrer_sistema():
    diretorio_raiz = Path(__file__).resolve().parent
    print(f"[🔍 FORENSE TCC] A procurar pelo termo exato '{TERMO_ALVO}' a partir de: {diretorio_raiz}\n")
    
    arquivos_encontrados = 0
    pastas_ignoradas = ['.git', '__pycache__', 'venv', 'env', 'pdfs_finais', 'monaco_security_vault']
    
    for caminho_arquivo in diretorio_raiz.glob("**/*"):
        if any(p in caminho_arquivo.parts for p in pastas_ignoradas):
            continue
            
        if caminho_arquivo.is_file():
            try:
                with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as f:
                    conteudo = f.read()
                    
                if TERMO_ALVO in conteudo.lower():
                    arquivos_encontrados += 1
                    print(f"🎯 [ENCONTRADO] Ficheiro: {caminho_arquivo.relative_to(diretorio_raiz)}")
                    
                    with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as f:
                        for num_linha, linha in enumerate(f, 1):
                            if TERMO_ALVO in linha.lower():
                                print(f"   -> Linha {num_linha}: {linha.strip()[:120]}")
                    print("-" * 50)
                    
            except (OSError, UnicodeError):
                continue
                
    print(f"\n[🏁 FIM] Varredura concluída. Total de ficheiros contendo '{TERMO_ALVO}': {arquivos_encontrados}")

if __name__ == "__main__":
    varrer_sistema()
