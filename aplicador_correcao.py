import os

# Linha de correção oficial
LINHA_CORRECAO = "import sys, os\nsys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))"

def aplicar_correcao_definitiva():
    # Caminho base do projeto
    base_dir = os.getcwd()
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        conteudo = f.read()
                    
                    # Remove correções antigas se existirem para evitar poluição
                    novo_conteudo = conteudo.replace("import sys, os\nsys.path.append(os.path.dirname(os.path.abspath(__file__))))", "")
                    
                    # Adiciona a correção correta se não estiver lá
                    if "sys.path.append" not in novo_conteudo:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(LINHA_CORRECAO + "\n\n" + novo_conteudo.lstrip())
                            print(f"[BLINDADO] {file}")
                    else:
                        print(f"[OK] Já integrado: {file}")
                        
                except (OSError, UnicodeError) as e:
                    print(f"[ERRO] Falha ao processar {file}: {e}")

if __name__ == "__main__":
    aplicar_correcao_definitiva()
    print("\n--- SISTEMA INTEGRADO COM SUCESSO. DORMIR! ---")
