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
import os
import sys
import subprocess
import traceback

def executar_e_capturar_erros():
    print("=" * 65)
    print(" MONITOR DE DIAGNÓSTICO E CAPTURA DE ERROS - TCC CORE ")
    print("=" * 65)

    # Caminho onde o orquestrador está localizado
    caminho_orquestrador = os.path.join("core", "biogemio_orquestrador.py")
    
    # Se não achar na pasta core com caminho relativo, tenta buscar pelo diretório atual
    if not os.path.exists(caminho_orquestrador):
        if os.path.exists("biogemio_orquestrador.py"):
            caminho_orquestrador = "biogemio_orquestrador.py"
        else:
            # Tenta varrer pastas para achar o arquivo exato
            encontrado = None
            for raiz, dirs, arquivos in os.walk("."):
                if "biogemio_orquestrador.py" in arquivos:
                    encontrado = os.path.join(raiz, "biogemio_orquestrador.py")
                    break
            if encontrado:
                caminho_orquestrador = encontrado
            else:
                print(f"[!] ERRO CRÍTICO: Não foi possível localizar o arquivo 'biogemio_orquestrador.py' em nenhuma pasta.")
                return

    print(f"[+] Orquestrador localizado em: {caminho_orquestrador}")
    print("[+] Iniciando o sistema com rastreamento ativo de exceções (Câmera + Painel HTML)...\n")
    print("-" * 65)

    try:
        # Executa o script do orquestrador em tempo real, redirecionando a saída direto para o seu terminal
        processo = subprocess.Popen(
            [sys.executable, "-u", caminho_orquestrador],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )

        # Fica escutando a saída do terminal linha por linha
        while True:
            linha = processo.stdout.readline()
            if not linha and processo.poll() is not None:
                break
            if linha:
                print(linha, end="")

    except Exception as e:
        print(f"\n[!] Exceção capturada pelo monitor de diagnóstico:")
        traceback.print_exc()

    print("\n" + "=" * 65)
    print(" Execução encerrada. Verifique acima a linha exata onde ocorreu a falha.")
    print("=" * 65)

if __name__ == "__main__":
    executar_e_capturar_erros()