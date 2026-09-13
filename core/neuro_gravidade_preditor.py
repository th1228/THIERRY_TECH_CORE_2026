# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.memoria_comum import instancia_memoria as memoria
except ImportError:
    memoria = None

class NeuroGravidadePreditor:
    """
    Motor de processamento de Bioarquitetura Neural.
    Cruza dados de imagem com a linhagem ancestral.
    """

    def processar_biometria(self, dados_brutos):
        simetria = dados_brutos.get('simetria_mandibula', "0%")
        
        if "98%" in simetria:
            ancestralidade = "Sincronia Total - Linhagem de Fogo e Ouro"
        else:
            ancestralidade = "Adaptação de Linhagem em Curso - Foco em Ancestrais de Terra"
            
        resultado = {
            "neurogravidade": "Fluxo Bio-Ancestral Estável",
            "ancestralidade": ancestralidade,
            "parecer": f"Estrutura com {simetria} de harmonia biométrica."
        }

        # Persistência na Memória Comum 💾
        if memoria:
            memoria.salvar_dados("neurogravidade_diagnostico", resultado)
            print("[NEUROGRAVIDADE] Dados salvos na Memória Comum.")

        return resultado

def processar(frame=None, dados_brutos=None):
    """Função de ponte para o orquestrador principal."""
    if dados_brutos is None:
        dados_brutos = {'simetria_mandibula': "98% (Alta Simetria)"}
        
    preditor = NeuroGravidadePreditor()
    resultado = preditor.processar_biometria(dados_brutos)
    
    if frame is not None:
        import cv2
        cv2.putText(frame, "TTC GLOBAL // NEUROGRAVIDADE [ACTIVE]", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 102), 2, cv2.LINE_AA)
        cv2.putText(frame, f"LINHAGEM: {resultado['ancestralidade'][:25]}...", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (212, 175, 55), 1, cv2.LINE_AA)
        return frame, resultado
        
    return resultado

if __name__ == "__main__":
    print(processar())