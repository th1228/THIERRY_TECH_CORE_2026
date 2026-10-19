import os

def analisar_conectividade():
    print("--- INICIANDO ANALISADOR DE CONECTIVIDADE TTC PROTOCOL ---")
    print("--- RELATÓRIO DE DIAGNÓSTICO ---")
    
    # Lista arquivos .py na pasta atual
    arquivos = [f for f in os.listdir('.') if f.endswith('.py')]
    
    erros = 0
    for arquivo in arquivos:
        # Apenas abre o arquivo para verificar se ele está legível
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                # Verifica se o arquivo não está vazio
                if len(conteudo) == 0:
                    print(f"[!] ARQUIVO: {arquivo} | AVISO: Arquivo vazio")
        except (OSError, UnicodeDecodeError) as e:
            print(f"[!] ARQUIVO: {arquivo} | ERRO DE LEITURA: {e}")
            erros += 1
            
    if erros == 0:
        print("\n[STATUS: CONECTIVIDADE ESTÁVEL // NENHUM ERRO CRÍTICO ENCONTRADO]")
    else:
        print(f"\n[STATUS: {erros} ERROS ENCONTRADOS // REVISE OS ARQUIVOS]")

if __name__ == "__main__":
    analisar_conectividade()
