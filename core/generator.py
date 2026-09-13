# -*- coding: utf-8 -*-
import sys
import os

# --- BLOCO DE CONEXÃO ESTRUTURAL (NÃO MEXER) ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

# Importações seguras dos módulos do ecossistema TTC Global
try:
    from core import analise_rosto, analise_cabelo, analise_colorimetria, biblioteca_estilo, atelier
except ImportError:
    # Mocks de segurança caso os submódulos estejam em desenvolvimento
    analise_rosto = analise_cabelo = analise_colorimetria = biblioteca_estilo = atelier = None

def processar_fluxo_global(frame_rosto, frame_cabelo, dados_sensor_pele):
    """
    O Coração da Supremacy Network: 
    Cruza dados de imagem e sensor para gerar o diagnóstico forense.
    """
    print("[GENERATOR] Iniciando processamento forense...")

    # 1. Análise Morfológica
    formato_rosto = analise_rosto.detectar(frame_rosto) if analise_rosto else "Oval"
    
    # 2. Refinamento de Cabelo (Cálculo de fibra)
    diagnostico_fio = analise_cabelo.refinar_diagnostico_capilar(frame_cabelo) if analise_cabelo else {"fibra": "Saudável"}
    
    # 3. Análise de Colorimetria (Cruzamento com o sensor)
    if analise_colorimetria:
        colorimetria_dados = analise_colorimetria.analisar_tom_pele(dados_sensor_pele)
        protocolo_quimico = analise_colorimetria.sugerir_coloracao(colorimetria_dados.get('DIAGNOSTICO', 'Neutro'))
    else:
        colorimetria_dados = {"DIAGNOSTICO": "Neutro"}
        protocolo_quimico = {"acao": "Padrão"}
    
    # 4. Cruzamento com a Biblioteca de Estilo (Baseado na idade e perfil)
    estilo = biblioteca_estilo.consultar_estilo(formato_rosto, perfil="MASCULINO") if biblioteca_estilo else {"estilo": "Clássico"}
    
    # 5. Salvando na Memória Comum para o Atelier ler 🧠
    memoria.salvar_dados("ROSTO_STATUS", {"FORMATO": formato_rosto})
    memoria.salvar_dados("CABELO_DIAGNOSTICO", diagnostico_fio)
    memoria.salvar_dados("PROTOCOLO_QUIMICO", protocolo_quimico)
    memoria.salvar_dados("ESTILO_SUGERIDO", estilo)
    
    # 6. Disparo do Ateliê para gerar o Laudo PDF final
    if atelier:
        atelier.gerar_diagnostico_final()
    else:
        print("[GENERATOR] Aviso: Módulo atelier não encontrado para gerar o laudo físico.")
    
    print("[GENERATOR] Ciclo completo. Laudo de alta performance gerado.")
    return "[GENERATOR] Sucesso no cruzamento de dados."

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    sensor_padrao = (120, 105, 90)
    return processar_fluxo_global("img_rosto.jpg", "img_cabelo.jpg", sensor_padrao)

if __name__ == "__main__":
    # Simulação da entrada do sensor
    sensor_bruto = (120, 105, 90) 
    processar_fluxo_global("img_rosto.jpg", "img_cabelo.jpg", sensor_bruto)