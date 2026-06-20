import numpy as np

class VisagismoNeuralEngine:
    def __init__(self):
        # Índices chave do MediaPipe Face Mesh
        self.LANDMARKS = {
            "TRICHION": 10,        # Início do couro cabeludo (testa)
            "GLABELLA": 168,      # Entre as sobrancelhas
            "SUBNASALE": 164,     # Base do nariz
            "MENTON": 152,        # Base do queixo
            "ZYGOMA_LEFT": 234,   # Extremidade lateral esquerda do rosto
            "ZYGOMA_RIGHT": 454,  # Extremidade lateral direita do rosto
            "EYE_LEFT_OUTER": 263,# Canto externo do olho esquerdo
            "EYE_LEFT_INNER": 362,# Canto interno do olho esquerdo
            "EYE_RIGHT_INNER": 133,# Canto interno do olho direito
            "EYE_RIGHT_OUTER": 33  # Canto externo do olho direito
        }

    def _calcular_distancia_3d(self, p1, p2):
        """Calcula a distância euclidiana tridimensional entre dois pontos."""
        return np.linalg.norm(np.array(p1) - np.array(p2))

    def analisar_proporcoes(self, landmarks_mesh):
        """
        Recebe a lista de landmarks extraída pelo MediaPipe e calcula as
        proporções áureas, terços faciais e coeficientes neuroestéticos.
        """
        # Extração das coordenadas reais dos pontos de interesse
        pontos = {nome: [landmarks_mesh[idx].x, landmarks_mesh[idx].y, landmarks_mesh[idx].z] 
                  for nome, idx in self.LANDMARKS.items()}

        # 1. CÁLCULOS DOS TERÇOS FACIAIS (Dimensão Vertical)
        terco_superior = self._calcular_distancia_3d(pontos["TRICHION"], pontos["GLABELLA"])
        terco_medio = self._calcular_distancia_3d(pontos["GLABELLA"], pontos["SUBNASALE"])
        terco_inferior = self._calcular_distancia_3d(pontos["SUBNASALE"], pontos["MENTON"])
        
        soma_tercos = terco_superior + terco_medio + terco_inferior
        
        pct_superior = (terco_superior / soma_tercos) * 100
        pct_medio = (terco_medio / soma_tercos) * 100
        pct_inferior = (terco_inferior / soma_tercos) * 100

        # 2. PROPORÇÃO DA FACE (Aspect Ratio)
        altura_facial = self._calcular_distancia_3d(pontos["TRICHION"], pontos["MENTON"])
        largura_facial = self._calcular_distancia_3d(pontos["ZYGOMA_LEFT"], pontos["ZYGOMA_RIGHT"])
        proporcao_aspecto = altura_facial / largura_facial if largura_facial > 0 else 1

        # 3. TRADUÇÃO NEURAL E TEMPERAMENTAL (Algoritmo de Decisão)
        diagnostico = self._decodificar_temperamento(pct_superior, pct_medio, pct_inferior, proporcao_aspecto)

        return {
            "metricas": {
                "proporcao_aspecto": round(proporcao_aspecto, 3),
                "terco_superior_pct": round(pct_superior, 1),
                "terco_medio_pct": round(pct_medio, 1),
                "terco_inferior_pct": round(pct_inferior, 1)
            },
            "diagnostico_neural": diagnostico
        }

    def _decodificar_temperamento(self, sup, med, inf, aspect_ratio):
        """
        Aplica as regras da neuroestética baseada nas dominâncias geométricas.
        Idealmente, um equilíbrio perfeito seria de 33.3% para cada terço.
        """
        dominancia_vertical = max(sup, med, inf)
        
        # Determinação do arquétipo estrutural do formato do rosto
        if aspect_ratio > 1.35:
            formato_base = "Perfil Alongado/Retangular ou Oval"
            forca_estrutural = "Alta Preservação e Foco Longo"
        else:
            formato_base = "Perfil Dinâmico/Quadrado ou Redondo"
            forca_estrutural = "Alta Prontidão e Força de Arranque"

        # Cruzamento neuroestético: Terço Dominante determina o canal cerebral dominante
        if dominancia_vertical == sup:
            arquetipo = "Intelectual / Racional (Melancólico/Cerebral)"
            comunicacao_inconsciente = "Transmite autoridade pelo intelecto, estratégia, profunda capacidade reflexiva e análise."
            direcionamento_design = "Suavizar linhas da testa com elementos dinâmicos ou reforçar com linhas retas para máxima imponência corporativa."
        
        elif dominancia_vertical == med:
            arquetipo = "Emocional / Relacional (Sanguíneo/Expressivo)"
            comunicacao_inconsciente = "Transmite empatia, alta capacidade de conexão humana, dinamismo social e persuasão."
            direcionamento_design = "Uso de eixos diagonais para controlar o excesso de expressividade ou acentuar o magnetismo pessoal."
        
        else:
            arquetipo = "Instintivo / Executante (Colérico/Realizador)"
            comunicacao_inconsciente = "Transmite forte senso de ação, liderança primitiva, vigor físico, foco em resultados e territorialidade."
            direcionamento_design = "Equilibrar a mandíbula para evitar agressividade visual involuntária ou criar linhas de pura liderança."

        return {
            "formato_base": formato_base,
            "arquetipo_neuro": arquetipo,
            "forca_estrutural": forca_estrutural,
            "comunicacao_inconsciente": comunicacao_inconsciente,
            "direcionamento_design": direcionamento_design,
            "aderencia_proporcao_aurea": round((1.618 / aspect_ratio) * 100 if aspect_ratio > 1 else (aspect_ratio / 1.618) * 100, 1)
        }