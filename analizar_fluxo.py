import os
import re

def mapear_toda_hierarquia():
    print(f"{'ARQUIVO':<40} | {'CHAMA (IMPORTAÇÕES)'}")
    print("-" * 100)
    
    # Percorre todas as pastas recursivamente
    for raiz, pastas, arquivos in os.walk('.'):
        for arquivo in arquivos:
            if arquivo.endswith('.py'):
                caminho = os.path.join(raiz, arquivo)
                
                with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
                    conteudo = f.read()
                    # Procura por 'from X import' ou 'import X'
                    imports = re.findall(r'(?:from|import)\s+([\w\.]+)', conteudo)
                    
                    # Filtra apenas o que parece ser um módulo interno seu (não bibliotecas padrão)
                    # Consideramos interno se não for algo óbvio do sistema (tipo os, sys, cv2, json)
                    padroes_internos = ['core', 'motores', 'security', 'monaco', 'motor', 'db', 'interface']
                    conexoes = [i for i in imports if any(p in i for p in padroes_internos)]
                    
                    if conexoes:
                        print(f"{caminho:<40} | {', '.join(set(conexoes))}")

if __name__ == "__main__":
    mapear_toda_hierarquia()