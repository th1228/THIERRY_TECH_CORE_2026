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

# Tabela Mundial de Colorimetria (Baseada em círculo cromático e fototipos)
MAPA_CIENTIFICO_COR = {
    "FRIA": {
        "BASE_RAIZ": ["Castanho Profundo (2.0)", "Castanho Acinzentado (4.1)", "Preto Natural (1.0)"],
        "MECHAS": ["Platinado (10.01)", "Pérola (9.89)", "Bege Acinzentado (8.11)", "Violeta"],
        "REFLETANCIA": "Alta (Foco em neutralizar o amarelo/laranja)"
    },
    "QUENTE": {
        "BASE_RAIZ": ["Castanho Dourado (4.3)", "Chocolate (5.7)", "Louro Mel (7.3)"],
        "MECHAS": ["Dourado (9.3)", "Mel (8.3)", "Caramelo (7.7)", "Cobre (7.4)"],
        "REFLETANCIA": "Média (Foco em iluminar com calor)"
    },
    "NEUTRA": {
        "BASE_RAIZ": ["Castanho Natural (4.0)", "Louro Escuro (6.0)"],
        "MECHAS": ["Champanhe (9.02)", "Amêndoa (8.7)", "Dourado Suave (9.31)"],
        "REFLETANCIA": "Equilibrada (Foco em harmonia)"
    }
}

def calcular_cor_forense(dados_rgb_sensor):
    """
    1. Extrai a média de RGB da pele.
    2. Calcula a temperatura (R vs B).
    3. Cruza com os Fototipos Mundiais e salva na Memória Comum 🧠.
    """
    r, g, b = dados_rgb_sensor
    
    temperatura = "QUENTE" if r > b else "FRIA"
    if abs(r - b) < 10: temperatura = "NEUTRA"
    
    resultado = {
        "DIAGNOSTICO": temperatura,
        "DADOS": MAPA_CIENTIFICO_COR[temperatura]
    }
    
    try:
        memoria.salvar_dados("COLORIMETRIA_STATUS", resultado)
    except Exception:
        pass
        
    return resultado

def processar(dados_entrada=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    if dados_entrada and isinstance(dados_entrada, (list, tuple)) and len(dados_entrada) == 3:
        return calcular_cor_forense(dados_entrada)
    # Fallback padrão caso nenhum dado RGB seja passado na chamada
    return calcular_cor_forense((150, 120, 100))