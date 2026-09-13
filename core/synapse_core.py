import sys, os

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
Módulo: Synapse Core (TTC Global)
Função: Gestão de Rede Neural, Análise Dual (Câmera + Arduino), 
Fatores Climáticos, Memória Comum e Frequências de Regeneração.
"""

class SynapseCore:
    def __init__(self):
        # Definição dos 3 Níveis de Frequência Harmônica ("Frequência de Deus")
        self.niveis_frequencia = {
            1: {"nome": "Nível Base / Calibragem Sináptica", "hz": 432.0, "limite_estresse": 50},
            2: {"nome": "Nível Intermediário / Coerência Neural", "hz": 528.0, "limite_estresse": 30},
            3: {"nome": "Nível Avançado / Regeneração Celular Plena", "hz": 639.0, "limite_estresse": 15}
        }
        
        # Métrica base da rede (metáfora dos 100 milhões de conexões/neurônios ativos)
        self.capacidade_total_rede = 100_000_000  

    def processar_sessao_completa(self, dados_camera: dict, dados_arduino: dict, dados_clima: dict, memoria_historica: dict) -> dict:
        """
        Cruza a consciência do sistema:
        1. Leitura da Câmera (Visão/Respiração)
        2. Leitura do Arduino (Sensor Óptico/Fisiológico)
        3. Fator Ambiental / Clima
        4. Consulta à Memória Comum (Histórico do Paciente)
        """
        
        # Extração de parâmetros físicos e visuais
        respiracao_visual = dados_camera.get("respiracao_ciclos", 20)
        tensao_facial = dados_camera.get("tensao_facial", 50)
        
        pulso_optico = dados_arduino.get("pulso_cardiaco", 80)
        spo2 = dados_arduino.get("spo2", 98)
        
        # Fator climático (temperatura/umidade influenciam a vasodilatação e resposta basal)
        temperatura_ambiente = dados_clima.get("temperatura", 25.0)
        fator_termico_ajuste = 1.0 if 20 <= temperatura_ambiente <= 26 else 1.05

        # Ponderação do índice de estresse real (Arduino + Câmera + Clima)
        indice_estresse_base = (tensao_facial * 0.4) + ((pulso_optico - 60) * 0.6)
        indice_estresse_geral = max(0.0, indice_estresse_base * fator_termico_ajuste)

        # Consciência integrada com a Memória Comum (compara com o histórico anterior se houver)
        historico_anterior = memoria_historica.get("ultimo_estresse", indice_estresse_geral)
        estresse_consciente = (indice_estresse_geral * 0.7) + (historico_anterior * 0.3)

        # Determina o nível de aptidão para a frequência
        nivel_apto = self._calcular_nivel_apto(estresse_consciente)

        # Calcula o crescimento da rede (densidade dos 100 milhões de neurônios ativos)
        densidade_ativa = self._calcular_densidade_neuronal(estresse_consciente)

        # Retorna o pacote completo informando a consciência do sistema
        return {
            "estresse_consciente": round(estresse_consciente, 2),
            "nivel_frequencia_liberado": nivel_apto,
            "dados_frequencia": self.niveis_frequencia.get(nivel_apto, self.niveis_frequencia[1]),
            "densidade_sinaptica_ativa": densidade_ativa,
            "status_consciencia": "Sincronizado com Memória Comum e Ambiente",
        }

    def _calcular_nivel_apto(self, estresse: float) -> int:
        """Avalia qual dos 3 níveis de frequência o paciente está apto a receber."""
        if estresse > self.niveis_frequencia[1]["limite_estresse"]:
            return 1  # Calibragem inicial
        elif self.niveis_frequencia[2]["limite_estresse"] <= estresse <= self.niveis_frequencia[1]["limite_estresse"]:
            return 2  # Coerência intermediária
        else:
            return 3  # Regeneração Celular Avançada (Nível máximo)

    def _calcular_densidade_neuronal(self, estresse: float) -> int:
        """Métrica dos 100 milhões de neurônios sincronizados com o estado do paciente."""
        fator_coerencia = max(0.1, (100 - estresse) / 100)
        neurônios_ativos = int(self.capacidade_total_rede * fator_coerencia)
        return neurônios_ativos