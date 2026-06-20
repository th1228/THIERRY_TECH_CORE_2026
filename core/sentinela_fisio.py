# -*- coding: utf-8 -*-
import numpy as np
from biometria import MODELOS_ROSTO_BIOMETRIA

class SentinelaFisio:
    def analisar_tudo(self, Landmarks):
        # Cálculo da proporção
        p1 = np.array([Landmarks[234].x, Landmarks[234].y])
        p2 = np.array([Landmarks[454].x, Landmarks[454].y])
        largura = np.linalg.norm(p1 - p2)
        comprimento = abs(Landmarks[10].y - Landmarks[152].y)
        proporcao = comprimento / (largura + 0.001)
        
        # Prioridade para o Triangular
        if 1.15 <= proporcao <= 1.30:
            formato = "Triangular"
        else:
            # Busca matemática nos outros modelos
            formato = min(MODELOS_ROSTO_BIOMETRIA.keys(), 
                          key=lambda m: abs(MODELOS_ROSTO_BIOMETRIA[m]["proporcao_ideal"] - proporcao))
        
        return {"visagismo": f"Rosto {formato}", "texto_tela": f"Rosto: {formato}"}