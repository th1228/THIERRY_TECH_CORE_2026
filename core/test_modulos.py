import sys, os

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys, os

# -*- coding: utf-8 -*-
# Correção: Importando do arquivo correto 'biometria.py'
from biometria import obter_dados
from memoria_comum import memoria

def executar_validacao_completa():
    print("[SYSTEM] Iniciando Ciclo de Validação Biométrica...")
    
    # 1. Executa a leitura da biometria
    # Usando a função que você definiu no biometria.py
    resultado = obter_dados()
    
    # 2. Conecta ao motor: atualiza a memória global
    # Atualizamos o status na memória com o que veio da biometria
    memoria.status = resultado
    
    print("-" * 30)
    print("[OK] Integração Concluída.")
    print(f"Status da Biometria na Memória: {memoria.status}")
    print("-" * 30)

if __name__ == "__main__":
    executar_validacao_completa()