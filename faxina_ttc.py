import os
import shutil

# Extensões e pastas mapeadas para a faxina do ecossistema
EXTENSOES_ALVO = ['.log', '.tmp', '.bak']
PASTAS_ALVO = ['__pycache__', 'temp_reports', 'logs_antigos']

def varrer_e_limpar(diretorio_raiz, executar_remocao=True):
    arquivos_para_apagar = []
    pastas_para_apagar = []

    print(f"[*] Varredura iniciada em: {diretorio_raiz}\n")

    for root, dirs, files in os.walk(diretorio_raiz, topdown=False):
        # Identificar pastas indesejadas (como __pycache__)
        for d in dirs:
            if d in PASTAS_ALVO:
                caminho_pasta = os.path.join(root, d)
                pastas_para_apagar.append(caminho_pasta)

        # Identificar arquivos temporários ou relatórios antigos por extensão
        for f in files:
            if any(f.endswith(ext) for ext in EXTENSOES_ALVO):
                caminho_arquivo = os.path.join(root, f)
                arquivos_para_apagar.append(caminho_arquivo)

    # Exibe o relatório do que foi localizado
    print("--- ITENS ENCONTRADOS PARA REMOÇÃO ---")
    print(f"Total de arquivos identificados: {len(arquivos_para_apagar)}")
    for arq in arquivos_para_apagar:
        print(f"  [ARQUIVO] {arq}")

    print(f"\nTotal de pastas identificadas: {len(pastas_para_apagar)}")
    for pas in pastas_para_apagar:
        print(f"  [PASTA] {pas}")
    print("--------------------------------------\n")

    if executar_remocao:
        print("[!] Executando limpeza definitiva...")
        for arq in arquivos_para_apagar:
            try:
                os.remove(arq)
            except Exception as e:
                print(f"Erro ao apagar arquivo {arq}: {e}")

        for pas in pastas_para_apagar:
            try:
                shutil.rmtree(pas)
            except Exception as e:
                print(f"Erro ao apagar pasta {pas}: {e}")
        print("[✓] Faxina concluída com sucesso! Projeto limpo e pronto para compactar.")
    else:
        print("[i] Modo de simulação (Dry Run). Nenhum arquivo foi apagado.")

if __name__ == "__main__":
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Já configurado para True para limpar de vez os relatórios e logs
    executar_remocao = True 
    
    varrer_e_limpar(diretorio_atual, executar_remocao=executar_remocao)