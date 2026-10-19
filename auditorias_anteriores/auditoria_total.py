import os
import time

def print_status(componente, status):
    print(f"[{status.upper():<25}] {componente}")

def run_auditoria_total():
    print("=====================================================================")
    print(" THIERRY TECHNOLOGY // SYSTEM INTEGRITY CHECKER // VERSION 9.0")
    print("=====================================================================\n")
    
    # Estrutura final e limpa: focado no que realmente existe
    check_list = {
        "CORE_SYSTEM": ["templates/index.html", "gui_main.py", "iniciar.py"],
        "SEGURANÇA_E_LOGICA": ["gerar_son.py", "integracao_google.py", "interface_dashboard.py"],
        "IDENTIDADE": ["identity/MANIFESTO.md"]
    }

    falhas = 0
    sucessos = 0

    for categoria, arquivos in check_list.items():
        print(f"--- VERIFICANDO CATEGORIA: {categoria} ---")
        for arquivo in arquivos:
            if os.path.exists(arquivo):
                print_status(arquivo, "SUCESSO")
                sucessos += 1
            else:
                print_status(arquivo, "ERRO // NÃO ENCONTRADO")
                falhas += 1
            time.sleep(0.05)
        print("")

    print("=====================================================================")
    print(f" RESUMO FINAL: {sucessos} SUCESSOS / {falhas} FALHAS")
    
    if falhas == 0:
        print("\n[STATUS: SISTEMA 100% ÍNTEGRO // PRONTO PARA COMPRESSÃO]")
    else:
        print("\n[STATUS: SISTEMA COM FALHAS // CORRIJA ANTES DE ZIPAR]")
    print("=====================================================================")

if __name__ == "__main__":
    run_auditoria_total()