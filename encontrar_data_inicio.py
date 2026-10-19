import os
from datetime import datetime

caminho_base = r"C:\projetos python" 
print(f"Varredura profunda iniciada (filtrando a partir de 2026): {caminho_base}\nAguarde...")

arquivo_mais_antigo = None
menor_tempo = float('inf')
total_verificados = 0

for raiz, diretorios, arquivos in os.walk(caminho_base):
    # Ignora pastas de sistema desnecessárias
    if any(p in raiz for p in ['.git', '__pycache__', 'venv', 'node_modules']):
        continue
        
    for arquivo in arquivos:
        caminho_completo = os.path.join(raiz, arquivo)
        try:
            tempo_criacao = os.path.getctime(caminho_completo)
            tempo_mod = os.path.getmtime(caminho_completo)
            tempo_real = min(tempo_criacao, tempo_mod)
            
            data_arquivo = datetime.fromtimestamp(tempo_real)
            
            # Filtra estritamente para o ano de 2026 em diante
            if data_arquivo.year >= 2026:
                total_verificados += 1
                if tempo_real < menor_tempo:
                    menor_tempo = tempo_real
                    arquivo_mais_antigo = caminho_completo
        except (OSError, ValueError, OverflowError):
            pass

print(f"\n--- RESULTADO DA VARREDURA (2026) ---")
print(f"Total de arquivos analisados em 2026: {total_verificados}")

if arquivo_mais_antigo:
    data_encontrada = datetime.fromtimestamp(menor_tempo)
    print(f"Arquivo mais antigo deste ano encontrado:")
    print(f"-> {arquivo_mais_antigo}")
    print(f"-> Data: {data_encontrada.strftime('%d/%m/%Y às %H:%M:%S')}")
else:
    print("Nenhum arquivo encontrado para o ano de 2026.")
