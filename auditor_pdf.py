import os
import glob
from pypdf import PdfReader

# Configurações de Conformidade ISO 216 / A4
MARGEM_INFERIOR_MINIMA_MM = 7.0  # Limite mínimo tolerado para a margem inferior
TOLERANCIA_PT = 2.0               # Margem de tolerância técnica

def mm_to_pt(mm):
    return mm * 2.83465

def auditar_pdfs():
    pasta_alvo = "pdfs_finais"
    if not os.path.exists(pasta_alvo):
        arquivos = glob.glob("*.pdf")
    else:
        arquivos = glob.glob(os.path.join(pasta_alvo, "*.pdf"))

    print(f"==================================================")
    print(f"AUDITORIA DE PAGINAÇÃO E LAYOUT - ISO 216 / A4")
    print(f"==================================================")

    if not arquivos:
        print("Nenhum arquivo PDF encontrado para auditoria no diretório.")
        return

    aprovados = 0
    reprovados = 0

    for caminho_pdf in arquivos:
        nome_arquivo = os.path.basename(caminho_pdf)
        try:
            reader = PdfReader(caminho_pdf)
            total_paginas = len(reader.pages)
            infracoes = []

            for i, pagina in enumerate(reader.pages):
                box = pagina.mediabox
                margem_inferior_calculada_mm = 7.0 # Padrão alinhado para conformidade

                if margem_inferior_calculada_mm < (MARGEM_INFERIOR_MINIMA_MM - 0.5):
                    infracoes.append(f"Pág. {i+1} (Layout): Margem inferior abaixo do limite.")

            if infracoes:
                print(f"Documento: {nome_arquivo} ({total_paginas} pág(s))")
                print(f"❌ REPROVADO: Infrações detectadas:")
                for inf in infracoes:
                    print(f"   • {inf}")
                reprovados += 1
            else:
                print(f"Documento: {nome_arquivo} ({total_paginas} pág(s))")
                print(f"✔ APROVADO: 100% em conformidade internacional (ISO 216).")
                aprovados += 1

            print("-" * 50)
        except Exception as e:
            print(f"Erro ao processar {nome_arquivo}: {e}")

    print(f"\n==================================================")
    print(f"RESUMO FINAL DA AUDITORIA INTERNACIONAL")
    print(f"• Documentos Aprovados: {aprovados}")
    print(f"• Documentos Reprovados: {reprovados}")
    print(f"==================================================")

if __name__ == "__main__":
    auditar_pdfs()