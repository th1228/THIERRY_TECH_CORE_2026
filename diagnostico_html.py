import os

def diagnosticar_modulo_html():
    print("=== DIAGNÓSTICO DO MÓDULO HTML / PAINEL ===")
    
    # Procurar por ficheiros que contenham 'html' ou 'painel' no nome
    ficheiros_encontrados = []
    for raiz, _, ficheiros in os.walk('.'):
        for f in ficheiros:
            if 'html' in f.lower() or 'painel' in f.lower():
                ficheiros_encontrados.append(os.path.join(raiz, f))
                
    if ficheiros_encontrados:
        print(f"[+] Ficheiros relacionados encontrados: {len(ficheiros_encontrados)}")
        for path in ficheiros_encontrados:
            print(f"    - {path}")
    else:
        print("[-] Nenhum ficheiro com 'html' ou 'painel' foi encontrado no diretório.")

    # Verificar se o main.py referencia rotas web
    if os.path.exists('main.py'):
        with open('main.py', 'r', encoding='utf-8', errors='ignore') as f:
            conteudo = f.read()
            if 'render_template' in conteudo or '@app.route' in conteudo:
                print("[+] O 'main.py' contém rotas web / Flask configuradas.")
            else:
                print("[-] O 'main.py' parece não ter rotas web aparentes.")
    else:
        print("[-] Ficheiro 'main.py' não encontrado na raiz.")

if __name__ == '__main__':
    diagnosticar_modulo_html()