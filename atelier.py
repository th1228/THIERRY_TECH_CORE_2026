import os
from fpdf import FPDF

# ==============================================================================
# 1. BASE DE DADOS DO DIAGNÓSTICO (O Coração do Sistema)
# ==============================================================================
# Aqui ficam guardados os dados coletados na análise visagista
dados_diagnostico = {
    "Client Name": "Exemplo Client Manhattan",
    "Natural Element": "Fogo -> Dinâmico, expressivo, líder, solar",
    "Dominant Cranian Angle": "Focus on Right Profile / Inclinado Direito",
    "Haute Couture Tailoring": "Seda e Crepe (Fluido e esvoaçante + Lapelas suaves, cortes precisos)",
    "Luxury Jewelry Accent": "Esmeralda -> Pontos de contraste magnético e elegância discreta",
    "Soundscape Active": "Playing 'Classic Symphony Remix (Vivaldi)'",
    "Final Style Silhouette": "Textura fluida, com movimento natural ('fios ao vento'), que transite bem entre o corporativo e o casual de luxo"
}

# ==============================================================================
# 2. CRIAÇÃO E CONFIGURAÇÃO DO PDF (Visual de Alto Padrão)
# ==============================================================================

# Inicializa o PDF com as configurações da biblioteca atualizada
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Escreve o título (w=0 faz ocupar a largura total de forma dinâmica e segura)
pdf.cell(w=0, h=10, txt="=== BESPOKE VISUAL DIAGNOSIS: TTC GLOBAL ===", new_x="LMARGIN", new_y="NEXT", align='C')
pdf.ln(10)

# Varre o dicionário e escreve cada linha no relatório
for chave, valor in dados_diagnostico.items():
    linha_texto = f"[{chave}] : {valor}"
    
    # O tratamento de encode/decode previne que o PDF trave com acentos (ex: 'Dinâmico', 'líder')
    linha_formatada = linha_texto.encode('latin-1', 'replace').decode('latin-1')
    
    # multi_cell com w=0 quebra as linhas longas respeitando as margens do papel perfeitamente
    pdf.multi_cell(w=0, h=10, txt=linha_formatada, new_x="LMARGIN", new_y="NEXT")

# ==============================================================================
# 3. SALVAMENTO E DIRETÓRIO (Segurança e Organização de Arquivos)
# ==============================================================================

# Define onde o relatório premium será armazenado
caminho_pasta = r"c:\projetos python\THIERRY_TECHNOLOGY_CORE"
nome_arquivo = "diagnostico_manhattan.pdf"
caminho_completo = os.path.join(caminho_pasta, nome_arquivo)

# Verifica se a pasta existe no Windows; se não existir, cria automaticamente
if not os.path.exists(caminho_pasta):
    os.makedirs(caminho_pasta)

# Consolida e gera o arquivo físico no disco
pdf.output(caminho_completo)

print("-" * 60)
print(f"SUCESSO! PDF de alto padrão gerado em:")
print(f"-> {caminho_completo}")
print("-" * 60)