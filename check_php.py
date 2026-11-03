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

import subprocess
import re
import sys

# Versões seguras mínimas lançadas pela PHP Foundation em Outubro de 2026
SAFE_VERSIONS = {
    "8.2": (8, 2, 35),
    "8.3": (8, 3, 36),
    "8.4": (8, 4, 27),
    "8.5": (8, 5, 12),
}

def get_php_version():
    try:
        result = subprocess.run(["php", "-v"], capture_output=True, text=True, check=True)
        first_line = result.stdout.splitlines()[0]
        # Exemplo de saída: PHP 8.3.14 (cli) ...
        match = re.search(r"PHP\s+(\d+)\.(\d+)\.(\d+)", first_line)
        if match:
            return int(match.group(1)), int(match.group(2)), int(match.group(3)), first_line
    except (subprocess.SubprocessError, FileNotFoundError):
        return None
    return None

def main():
    print("=== Verificador de Vulnerabilidade do PHP (PHP2Shell) ===")
    php_info = get_php_version()
    
    if not php_info:
        print("\n[!] O executável do PHP não foi encontrado no PATH do sistema.")
        print("    Se o seu projeto roda em containers Docker ou servidores remotos, verifique a imagem base.")
        return

    major, minor, patch, full_string = php_info
    print(f"\nVersão detectada: {full_string}")
    
    version_key = f"{major}.{minor}"
    
    # Abaixo de 8.2 (ex: 8.1, 7.4, etc.) já estão em Fim de Vida (EOL) e não receberão patch oficial
    if major < 8 or (major == 8 and minor < 2):
        print("\n[ALERTA CRÍTICO] Você está usando uma versão do PHP abaixo da 8.2 (End-of-Life).")
        print("    Essa versão NÃO recebeu patch oficial da fundação PHP e está altamente vulnerável!")
        sys.exit(1)
        
    if version_key in SAFE_VERSIONS:
        safe_major, safe_minor, safe_patch = SAFE_VERSIONS[version_key]
        if (major, minor, patch) < (safe_major, safe_minor, safe_patch):
            print(f"\n[ALERTA] Sua versão ({major}.{minor}.{patch}) é VULNERÁVEL ao PHP2Shell!")
            print(f"    -> Ação necessária: Atualize imediatamente para o PHP {safe_major}.{safe_minor}.{safe_patch} ou superior.")
            sys.exit(1)
        else:
            print(f"\n[SEGURO] Sua versão do PHP ({major}.{minor}.{patch}) já possui o patch de correção aplicado.")
    else:
        print(f"\n[AVISO] Versão {version_key} não mapeada. Certifique-se de que está utilizando uma versão segura.")

if __name__ == "__main__":
    main()