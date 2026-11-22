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
from pathlib import Path
import os

print("=" * 60)
print("  MAPA DE RASTREABILIDADE E CAMINHOS DOS PDFS - TCC GLOBAL")
print("=" * 60)

# 1. Definição e validação do caminho base
BASE_DIR = Path(__file__).resolve().parent
print(f"\n[1] Diretório Base do Projeto:\n    -> {BASE_DIR}")

# 2. Possíveis locais onde os PDFs podem estar a ser salvos
possiveis_pastas = [
    BASE_DIR / "core" / "pdfs_finais",
    BASE_DIR / "pdfs_finais",
    BASE_DIR / "output",
    BASE_DIR / "relatorios"
]

print("\n[2] Verificação de Pastas de Destino (Onde o PDF deveria ficar):")
pasta_ativa = None
for pasta in possiveis_pastas:
    existe = pasta.exists()
    status = "ENCONTRADA 🟢" if existe else "NÃO EXISTE 🔴"
    print(f"    - {pasta.relative_to(BASE_DIR) if existe else pasta}: {status}")
    if existe and not pasta_ativa:
        pasta_ativa = pasta

# 3. Listagem dos PDFs existentes na pasta ativa
print("\n[3] Auditoria de Arquivos Físicos (PDFs Gerados):")
if pasta_ativa:
    print(f"    Varrendo a pasta ativa: {pasta_ativa.relative_to(BASE_DIR)}")
    pdfs = list(pasta_ativa.glob("*.pdf"))
    if pdfs:
        for pdf in pdfs:
            print(f"      📄 [ARQUIVO ENCONTRADO]: {pdf.name} (Tamanho: {pdf.stat().st_size} bytes)")
    else:
        print("      ⚠️ A pasta existe, mas está VAZIA. Nenhum PDF foi gerado/salvo aqui ainda.")
else:
    print("      ❌ Nenhuma pasta de PDFs válida foi encontrada na estrutura!")

# 4. Mapeamento de quem busca quem (A Lógica de Entrega)
print("\n[4] Mapeamento Lógico de Quem Busca Quem (Fluxo de Entrega):")
print("    ┌────────────────────────┐       ┌────────────────────────┐       ┌────────────────────────┐")
print("    │ 1. index.html (Botões) │ ───>  │ 2. main.py (Porta 801) │ ───>  │ 3. core/pdfs_finais    │")
print("    │    Dispara o fetch()   │       │    Intercepta a Rota   │       │    FileResponse(PDF)   │")
print("    └────────────────────────┘       └────────────────────────┘       └────────────────────────┘")
print("\n    Regra de Ouro:")
print("    - O botão no front-end precisa chamar a URL exata configurada no `main.py`.")
print("    - O `main.py` precisa procurar o arquivo exatamente na `pasta_ativa` listada acima.")
print("=" * 60)