import os

# Diretório raiz do seu projeto conforme a imagem
diretorio_raiz = "." 

# Termos para procurar nos scripts Python
termos_busca = [
    "arquivo_morto",
    "shutil.move",
    "shutil.copy",
    "os.remove",
    "unlink",
    "pdf"
]

print("Iniciando varredura nos scripts do projeto...\n")

for pasta_atual, subpastas, arquivos in os.walk(diretorio_raiz):
    # Ignora a própria pasta __pycache__ para otimizar
    if "__pycache__" in pasta_atual:
        continue
        
    for arquivo in arquivos:
        if arquivo.endswith(".py") and arquivo != "rastrear_limpeza.py":
            caminho_completo = os.path.join(pasta_atual, arquivo)
            try:
                with open(caminho_completo, "r", encoding="utf-8", errors="ignore") as f:
                    conteudo = f.read()
                    
                encontrados = [termo for termo in termos_busca if termo in conteudo]
                if encontrados:
                    print(f"[ENCONTRADO] Arquivo: {caminho_completo}")
                    print(f"   Termos detectados: {', '.join(encontrados)}")
                    print("-" * 50)
            except Exception as e:
                print(f"[ERRO] Não foi possível ler {caminho_completo}: {e}")

print("\nVarredura concluída. Verifique acima qual script gerencia essa pasta.")