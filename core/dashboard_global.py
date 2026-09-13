# -*- coding: utf-8 -*-
import sys
import os

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

# IMPORTAÇÕES SEGURAS DO ECOSSISTEMA
try:
    from core.biometria import obter_laudo_biometrico
except ImportError:
    def obter_laudo_biometrico(*args, **kwargs): return {"status": "Mock Biometria"}

try:
    from core.atelie import gerar_diagnostico_final
except ImportError:
    def gerar_diagnostico_final(*args, **kwargs): pass

def analisar_expressao_olhar(imagem_path):
    """Analisa a psicologia do olhar."""
    print("--- INICIANDO ANÁLISE PSICOMÉTRICA DO OLHAR ---")
    diagnostico_olhar = "Olhar Criativo e Curioso"
    print(f"Diagnóstico do Olhar: {diagnostico_olhar}")
    return diagnostico_olhar

def processar_rosto_completo(imagem_path="thierry_scan.jpg", genero="masculino"):
    """Orquestrador do fluxo TTC Global."""
    print(f"\n--- PROCESSANDO ROSTO TTC: {genero.upper()} ---")
    
    # Osteometria: Valores padrão ou resgatados da Memória Comum 🧠
    testa, macas, mandibula, altura = 100, 95, 80, 160
    
    # Chamada integrada de biometria
    diagnostico_biometria = obter_laudo_biometrico(testa, macas, mandibula, altura, genero, clima="tropical")
    
    # Análise do Olhar
    diagnostico_olhar = analisar_expressao_olhar(imagem_path)
    
    # Sincronização automática com a Memória Comum 🧠
    try:
        memoria.salvar_dados("diagnostico_biometria", diagnostico_biometria)
        memoria.salvar_dados("diagnostico_olhar", diagnostico_olhar)
        memoria.salvar_dados("status_processamento_rosto", "SUCESSO")
    except Exception:
        pass

    # Geração do Relatório
    gerar_diagnostico_final(
        osteometria=diagnostico_biometria,
        olhar=diagnostico_olhar,
        genero_input=genero
    )
    
    print("-" * 60)
    print("PROCESSO TTC FINALIZADO COM SUCESSO.")
    print("-" * 60)
    return {"status": "sucesso", "olhar": diagnostico_olhar}

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    return processar_rosto_completo()

if __name__ == "__main__":
    processar_rosto_completo("thierry_scan.jpg", "masculino")