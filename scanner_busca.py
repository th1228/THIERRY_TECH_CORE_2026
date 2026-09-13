import os

# Termos que estamos caçando no código
TERMOS_BUSCA = ["300000", "300.000", "stripe", "buy.stripe.com", "unit_amount"]

def varrer_projeto():
    print(">>> Iniciando varredura no diretório por vestígios de valores ou links do Stripe...\n")
    diretorio_atual = os.getcwd()
    
    encontrados = 0
    
    for root, dirs, files in os.walk(diretorio_atual):
        # Ignorar pastas de ambiente virtual ou git para acelerar
        if "venv" in root or ".git" in root or "__pycache__" in root:
            continue
            
        for file in files:
            if file.endswith((".py", ".html", ".json", ".txt")):
                caminho_completo = os.path.join(root, file)
                try:
                    with open(caminho_completo, "r", encoding="utf-8", errors="ignore") as f:
                        linhas = f.readlines()
                        for numero_linha, linha in enumerate(linhas, 1):
                            for termo in TERMOS_BUSCA:
                                if termo.lower() in linha.lower():
                                    print(f"[{file}] Linha {numero_linha} (Termo: '{termo}'):")
                                    print(f"   -> {linha.strip()}")
                                    encontrados += 1
                except Exception as e:
                    pass
                    
    print(f"\n>>> Varredura concluída. Total de ocorrências encontradas: {encontrados}")

if __name__ == "__main__":
    varrer_projeto()