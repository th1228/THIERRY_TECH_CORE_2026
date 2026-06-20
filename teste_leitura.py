# teste_leitura.py
from biogemio_test import realizar_leitura_manual
from genereitor import gerar_laudo

print("--- INICIANDO TESTE DE LEITURA ---")

# 1. Tenta ler da câmera
valor_mao = realizar_leitura_manual()
print(f"DEBUG: Valor lido da câmera: {valor_mao}")

# 2. Monta um pacote de teste
dados_teste = {
    'simetria_ini': '10%',
    'parecer': 'Teste de leitura final.',
    'densidade_mao': valor_mao
}

# 3. Tenta gerar o PDF
try:
    nome = gerar_laudo(dados_teste)
    print(f"PDF gerado com sucesso: {nome}")
except Exception as e:
    print(f"ERRO AO GERAR PDF: {e}")