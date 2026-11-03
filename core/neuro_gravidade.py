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
"""
Módulo: neuro_gravidade.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Versão: 2.0.0 - Bioarquitetura Neural & Linhagem Ancestral (Suporte PT/EN)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from memoria_comum import instancia_memoria as memoria
    except ImportError:
        memoria = None

class NeuroGravidadePreditor:
    """
    Motor de processamento de Bioarquitetura Neural.
    Cruza dados de imagem com a linhagem ancestral.
    """
    def __init__(self, lang: str = "PT"):
        self.lang = lang.upper() if lang else "PT"

    def processar_biometria(self, dados_brutos):
        simetria_val = dados_brutos.get('simetria_mandibula', "98%")
        
        # Converte para string de forma segura para análise
        simetria_str = str(simetria_val)
        
        # Verificação flexível de alta simetria (aceita 98%, 0.98 ou valores acima de 97)
        alta_simetria = False
        if "98" in simetria_str or "99" in simetria_str or "100" in simetria_str:
            alta_simetria = True
        elif isinstance(dados_brutos.get('simetria_mandibula'), (int, float)):
            if dados_brutos.get('simetria_mandibula') >= 0.97:
                alta_simetria = True

        if self.lang == "EN":
            ancestralidade = "Total Synchrony - Fire & Gold Lineage" if alta_simetria else "Lineage Adaptation in Progress - Earth Ancestors Focus"
            neuro_status = "Stable Bio-Ancestral Flow"
            parecer_texto = f"Structure with {simetria_str} biometric harmony."
        else:
            ancestralidade = "Sincronia Total - Linhagem de Fogo e Ouro" if alta_simetria else "Adaptação de Linhagem em Curso - Foco em Ancestrais de Terra"
            neuro_status = "Fluxo Bio-Ancestral Estável"
            parecer_texto = f"Estrutura com {simetria_str} de harmonia biométrica."
            
        resultado = {
            "neurogravidade": neuro_status,
            "ancestralidade": ancestralidade,
            "parecer": parecer_texto
        }

        # Persistência na Memória Comum 💾
        if memoria:
            if hasattr(memoria, 'salvar_dados'):
                memoria.salvar_dados("neurogravidade_diagnostico", resultado)
            elif hasattr(memoria, 'registrar'):
                memoria.registrar("neurogravidade_diagnostico", resultado)
            print("[NEUROGRAVIDADE] Dados salvos na Memória Comum.")

        return resultado

def processar(frame=None, dados_brutos=None, lang: str = "PT"):
    """Função de ponte para o orquestrador principal com suporte a idioma."""
    if dados_brutos is None:
        dados_brutos = {'simetria_mandibula': "98% (Alta Simetria)"}
        
    preditor = NeuroGravidadePreditor(lang=lang)
    resultado = preditor.processar_biometria(dados_brutos)
    
    if frame is not None:
        try:
            import cv2
            titulo_tela = "TTC GLOBAL // NEUROGRAVITY [ACTIVE]" if lang.upper() == "EN" else "TTC GLOBAL // NEUROGRAVIDADE [ACTIVE]"
            cv2.putText(frame, titulo_tela, (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 102), 2, cv2.LINE_AA)
            cv2.putText(frame, f"LINEAGE: {resultado['ancestralidade'][:25]}..." if lang.upper() == "EN" else f"LINHAGEM: {resultado['ancestralidade'][:25]}...", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (212, 175, 55), 1, cv2.LINE_AA)
        except Exception:
            pass
        return frame, resultado
        
    return resultado

if __name__ == "__main__":
    print(processar())