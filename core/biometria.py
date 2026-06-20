import os

# Aponta diretamente para a pasta que você mostrou na foto
PASTA_FOTOS = "02_biometric_masks/assets/referencias/feminino"

MODELOS_ROSTO_BIOMETRIA = {
    "Personalizado": {"proporcao_ideal": 0.808, "foto": os.path.join(PASTA_FOTOS, "corte_personalizado.jpeg")},
    "Oval": {"proporcao_ideal": 1.6, "foto": os.path.join(PASTA_FOTOS, "corte_oval.jpeg")},
    "Triangulo": {"proporcao_ideal": 1.4, "foto": os.path.join(PASTA_FOTOS, "corte_triangular.jpeg")},
    "Quadrado": {"proporcao_ideal": 1.2, "foto": os.path.join(PASTA_FOTOS, "corte_quadrado.jpeg")},
    "Redondo": {"proporcao_ideal": 1.1, "foto": os.path.join(PASTA_FOTOS, "corte_redondo.jpeg")},
    "Diamante": {"proporcao_ideal": 1.7, "foto": os.path.join(PASTA_FOTOS, "corte_diamante.jpeg")},
    "Retangular": {"proporcao_ideal": 1.3, "foto": os.path.join(PASTA_FOTOS, "corte_retangular.jpeg")},
    "Oblongo": {"proporcao_ideal": 1.8, "foto": os.path.join(PASTA_FOTOS, "corte_oblongo.jpeg")}
}

def encontrar_melhor_match(proporcao_calculada):
    """
    Função que compara a proporção real capturada pela câmera
    com os modelos ideais da sua base de dados.
    """
    melhor_modelo = None
    menor_diferenca = float('inf')
    
    for modelo, dados in MODELOS_ROSTO_BIOMETRIA.items():
        # Calcula a distância matemática para encontrar o modelo mais próximo
        diferenca = abs(dados["proporcao_ideal"] - proporcao_calculada)
        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            melhor_modelo = modelo
            
    return melhor_modelo

def testar_biometria():
    print("Iniciando teste de Bioarquitetura Neural...")
    # Testando com a sua proporção específica
    proporcao_teste = 0.808
    resultado = encontrar_melhor_match(proporcao_teste)
    print(f"Resultado do teste para proporção {proporcao_teste}: {resultado}")

def obter_dados():
    """
    Interface que o Orquestrador espera.
    """
    # Proporção capturada definida como a sua
    proporcao_capturada = 0.808 
    resultado = encontrar_melhor_match(proporcao_capturada)
    
    return {
        "tipo_rosto": resultado,
        "proporcao": proporcao_capturada,
        "status": "sucesso"
    }

if __name__ == "__main__":
    testar_biometria()