import os
from biogenio_engine import rodar_scanner
# Caminho exato para as suas fotos (ajuste se precisar)
PASTA_FOTOS = os.path.join("02_biometric_masks", "assets", "referencias", "feminino")

MODELOS_ROSTO_BIOMETRIA = {
    "Oval": {"proporcao_ideal": 1.6, "foto": os.path.join(PASTA_FOTOS, "corte_oval.jpeg")},
    "Triangulo": {"proporcao_ideal": 1.4, "foto": os.path.join(PASTA_FOTOS, "corte_triangular.jpeg")},
    "Quadrado": {"proporcao_ideal": 1.2, "foto": os.path.join(PASTA_FOTOS, "corte_quadrado.jpeg")},
    "Redondo": {"proporcao_ideal": 1.1, "foto": os.path.join(PASTA_FOTOS, "corte_redondo.jpeg")},
    "Diamante": {"proporcao_ideal": 1.7, "foto": os.path.join(PASTA_FOTOS, "corte_diamante.jpeg")},
    "Retangular": {"proporcao_ideal": 1.3, "foto": os.path.join(PASTA_FOTOS, "corte_retangular.jpeg")},
    "Oblongo": {"proporcao_ideal": 1.8, "foto": os.path.join(PASTA_FOTOS, "corte_oblongo.jpeg")}
}