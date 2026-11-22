# -*- coding: utf-8 -*-
"""
MIBO SOVEREIGN ENGINE - IP PROTECTOR & BLINDAGE TOOL
---------------------------------------------------
Este motor varre o projeto para injetar os cabeçalhos oficiais de proteção
de Propriedade Intelectual e Acordo de Confidencialidade (NDA).
"""

import os
import datetime

# Cabeçalho Institucional de Elite (Tier-1 Monaco Standards)
CABECALHO_PROTECAO = f"""# -*- coding: utf-8 -*-
\"\"\"
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © {datetime.datetime.now().year} | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the 
intellectual property of Thierry Technology Concept Global. Unauthorized 
distribution, reverse engineering, or usage without a signed NDA/License 
agreement is strictly prohibited under international copyright frameworks.
===========================================================================
\"\"\"
"""

def aplicar_blindagem_patrimonial():
    print("=" * 65)
    print("   MIBO SOVEREIGN ENGINE - INTELLECTUAL PROPERTY BLINDAGE")
    print("   Thierry Technology Concept Global | Deep Tech Governance")
    print("=" * 65)

    arquivos_protegidos = 0

    # Varre todos os arquivos do projeto
    for root, dirs, files in os.walk('.'):
        # Ignora pastas do sistema ou arquivos de teste temporários
        if any(ignored in root for ignored in ['.git', '__pycache__', 'venv', '.vscode', 'generated', 'pdfs_finals']):
            continue
            
        for file in files:
            # Ignora o próprio script de blindagem para não duplicar
            if file.endswith('.py') and file != 'blindar_codigo.py':
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        conteudo_original = f.read()

                    # Verifica se o arquivo já possui a blindagem ativa da Thierry Tech
                    if "THIERRY TECHNOLOGY CONCEPT GLOBAL" in conteudo_original:
                        print(f"  • SEGURO: {file} já possui blindagem de IP ativa.")
                        continue

                    # Injeta o cabeçalho no topo do arquivo de código
                    conteudo_blindado = CABECALHO_PROTECAO + "\n" + conteudo_original
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(conteudo_blindado)
                    
                    print(f"  🔒 BLINDADO: Notificação de IP inserida em {file}")
                    arquivos_protegidos += 1
                except Exception as e:
                    print(f"  ⚠️  Erro ao processar o arquivo {file}: {str(e)}")

    print("-" * 65)
    print(f"🏆 GESTÃO DE GOVERNANÇA CONCLUÍDA COM SUCESSO!")
    print(f"   Foram blindados {arquivos_protegidos} módulos de software ativos.")
    print("   Seu código-fonte agora carrega proteção legal institucional.")
    print("=" * 65)

if __name__ == '__main__':
    aplicar_blindagem_patrimonial()