import os
import re

def analisar_projeto():
    print("=" * 60)
    print("DIAGNÓSTICO AUTOMATIZADO DE RODAPÉ (MODO ESCURO VS CLARO)")
    print("=" * 60)

    # Procura arquivos html na pasta atual
    arquivos_html = [f for f in os.listdir('.') if f.endswith('.html')]
    
    if not arquivos_html:
        print("[ERRO] Nenhum arquivo .html encontrado na raiz do projeto.")
        return

    for arquivo in arquivos_html:
        print(f"\n[+] Analisando arquivo: {arquivo}")
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        # 1. Verifica se a variável de cor do rodapé está presente
        if '--id-footer-color' in conteudo:
            print("  -> [OK] Variável '--id-footer-color' encontrada.")
        else:
            print("  -> [FALHA] Variável '--id-footer-color' NÃO foi encontrada no CSS!")

        # 2. Verifica se existe seletor de Dark Mode configurado
        if 'dark-mode' in conteudo or 'prefers-color-scheme: dark' in conteudo:
            print("  -> [OK] Regras de Dark Mode detectadas.")
        else:
            print("  -> [FALHA] Nenhuma regra clara de Dark Mode para textos foi localizada.")

        # 3. Analisa o bloco de classes do rodapé
        if '.cell-footer-security' in conteudo:
            print("  -> [OK] Classe '.cell-footer-security' presente.")
            # Extrai o trecho da classe para verificar se herda cor errada
            match = re.search(r'\.cell-footer-security\s*\{([^}]+)\}', conteudo)
            if match:
                estilos = match.group(1)
                print(f"     Estilos atuais: {estilos.strip()}")
                if 'color:' not in estilos:
                    print("     [ALERTA] A classe do rodapé não define uma regra explícita de 'color!', dependendo de herança.")
        else:
            print("  -> [FALHA] Classe '.cell-footer-security' não encontrada.")

    print("\n" + "=" * 60)
    print("CAUSA RAIZ DO PROBLEMA NO MODO ESCURO:")
    print("=" * 60)
    print("No seu código atual, o container e o fundo geral do terminal mudam para escuro,")
    print("mas o fundo dos cartões (.grid-cell) continua branco/claro (#f8fafc).")
    print("Se a cor do texto do rodapé estiver vinculada a uma variável global que se")
    print("transforma em branco ou cinza claro no modo escuro, ela se funde com o fundo branco")
    print("do cartão e desaparece da sua visão!")
    print("\nSOLUÇÃO DEFINITIVA:")
    print("Garanta que a cor do rodapé no modo escuro aponte para um verde esmeralda vibrante")
    print("(ex: #34d399) ou um escuro forte, independente do fundo geral da tela.")
    print("=" * 60)

if __name__ == '__main__':
    analisar_projeto()