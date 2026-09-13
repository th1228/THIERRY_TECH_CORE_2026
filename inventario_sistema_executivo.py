import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os

def diagnostico_hierarquia_executiva():
    print(f"\n{'='*10} MAPPING ARQUITETURA TTC GLOBAL 2026 {'='*10}")
    
    # Hierarquia de dependência mapeada (Quem chama quem)
    fluxo = {
        "gui_main.py": ["Inicia a Interface", "Chama sentinela.py", "Aguarda inputs do Usuário"],
        "sentinela.py": ["Valida integridade do Core", "Monitora memória comum"],
        "neural_core/analise.py": ["Recebe dados da Câmera", "Processa Landmarks (468 pts)", "Salva na Memória Comum"],
        "MEMORIA_COMUM (Variáveis)": ["Armazena PHI, DEV, DEPTH", "Disponível para Relatório"],
        "Gerador_Relatorio": ["Extrai da MEMÓRIA COMUM", "Exporta para PDF"]
    }

    print("SEQUÊNCIA DE OPERAÇÃO (FLUXO DE DADOS):")
    for i, (modulo, acoes) in enumerate(fluxo.items(), 1):
        print(f"{i}. [MÓDULO: {modulo}]")
        for acao in acoes:
            print(f"   --> {acao}")
    
    print(f"\n{'='*10} STATUS: AGUARDANDO COMANDO DE EXECUÇÃO {'='*10}\n")

if __name__ == "__main__":
    diagnostico_hierarquia_executiva()