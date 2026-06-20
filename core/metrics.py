import math
from typing import Dict, Any

def calculate_visagism_metrics(facial_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Engine de Alta Performance para Análise Biométrica e Visagismo.
    Processa as dimensões extraídas da malha tridimensional.
    """
    # 1. Recupera as informações brutas enviadas pelo engine.py
    height = facial_data.get("face_height_px", 0.0)
    width = facial_data.get("face_width_px", 0.0)
    
    # Evita divisão por zero
    if width <= 0 or height <= 0:
        return {
            "status": "Aguardando Alinhamento",
            "proportional_index": 0.0,
            "symmetry_score": "0%"
        }

    # 2. Cálculo da Proporção Facial
    face_ratio = height / width
    
    # 3. Classificação Biométrica (Prioridade Triangular Adicionada)
    # A regra abaixo força o Triangular antes de qualquer outra análise matemática
    if 1.10 <= face_ratio <= 1.35:
        formato = "Triangular"
    elif face_ratio > 1.70:
        formato = "Perfil Alongado / Retangular"
    elif 1.55 <= face_ratio <= 1.70:
        formato = "Proporcao Aurea (Oval / Simetrico)"
    elif 1.40 <= face_ratio < 1.55:
        formato = "Perfil Harmonico Quadrado"
    else:
        formato = "Perfil Arredondado / Largo"

    # 4. Cálculo de Estabilidade de Simetria
    symmetry_deviation = abs(face_ratio - 1.58)
    symmetry_percentage = max(0, min(100, int((1 - symmetry_deviation) * 100)))

    # 5. Retorno dos Dados Estruturados
    return {
        "status": f"{formato}",
        "proportional_index": round(face_ratio, 2),
        "symmetry_score": f"{symmetry_percentage}%",
        "raw_height": round(height, 1),
        "raw_width": round(width, 1)
    }

class NeuralMatrix:
    @staticmethod
    def process_face(data: dict) -> dict:
        return calculate_visagism_metrics(data)