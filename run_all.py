# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the 
intellectual property of Thierry Technology Concept Global. Unauthorized 
distribution, reverse engineering, or usage without a signed NDA/License 
agreement is strictly prohibited under international copyright frameworks.
===========================================================================
"""

# -*- coding: utf-8 -*-
import sys
import os

# Configuração de caminhos para encontrar os módulos
raiz = os.path.dirname(os.path.abspath(__file__))
sys.path.append(raiz)
sys.path.append(os.path.join(raiz, 'core'))

# Importa os módulos principais
from security import blindagem
from auditoria_profunda import auditar_imports

def menu_principal():
    while True:
        print("\n--- PAINEL DE CONTROLE THIERRY TECH CORE 2026 ---")
        print("1. Iniciar Scanner Biométrico (Protegido)")
        print("2. Ativar Blindagem Manual")
        print("3. Executar Auditoria Profunda")
        print("4. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        try:
            if escolha == "1":
                print("\n[SISTEMA] Preparando captura...")
                # A blindagem já ativa todos os outros módulos (Portaria, Detector, Honeypot)
                frame_seguro = blindagem.rodar("FRAME_CAPTURA_BIOMETRICA")
                
                from core.scanner import ScannerCamera
                ScannerCamera().processar(frame_seguro)
                
            elif escolha == "2":
                # Ativa manualmente todas as camadas de segurança
                blindagem.ativar_protecao()
                
            elif escolha == "3":
                # Executa a sua auditoria de imports
                auditar_imports()
                
            elif escolha == "4":
                print("Encerrando sistema... Até logo!")
                break
                
            else:
                print("Opção inválida, tente novamente.")
                
        except Exception as e:
            print(f"\n[ERRO DURANTE EXECUÇÃO]: {e}")

if __name__ == "__main__":
    menu_principal()