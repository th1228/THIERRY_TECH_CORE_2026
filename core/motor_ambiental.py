# -*- coding: utf-8 -*-
import sys
import os

# --- BLOCO DE CONEXÃO ESTRUTURAL ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

class MotorBlindagemAmbiental:
    """
    Motor de análise ambiental para o THIERRY_TECH_CORE_2026.
    Gerencia a ativação de protocolos de longevidade baseados em métricas climáticas.
    """
    def __init__(self, temperatura=26.6, umidade=45.0):
        self.temp = temperatura
        self.umidade = umidade
        
    def calcular_risco(self):
        if self.umidade > 60 and self.temp < 25: 
            return 1
        elif self.umidade > 40: 
            return 2
        elif self.temp > 28: 
            return 3
        elif self.umidade < 30: 
            return 4
        else: 
            return 5
    
    def definir_protocolo(self):
        nivel = self.calcular_risco()
        protocolos = {
            1: {"acao": "Manutenção", "tecnologia": "Hidratação profunda basal"},
            2: {"acao": "Blindagem Preditiva", "tecnologia": "Intervenção osteométrica e neuro-olfativa de efeito gravitacional ao sistema límbico, parassimpático e regenerativo para longevidade"},
            3: {"acao": "Blindagem Ativa", "tecnologia": "Peptídeos Biomiméticos"},
            4: {"acao": "Regeneração Avançada", "tecnologia": "Infusão de Exossomos"},
            5: {"acao": "Protocolo de Choque", "tecnologia": "Terapia Autóloga + Exossomos Concentrados"}
        }
        return protocolos[nivel]

    def executar(self):
        """
        Executa o protocolo, salva na memória e retorna o resultado.
        """
        resultado = self.definir_protocolo()
        memoria.salvar_dados("BLINDAGEM_AMBIENTAL", resultado)
        return resultado

def processar(frame=None, temperatura=26.6, umidade=45.0):
    """
    Função de compatibilidade direta para o orquestrador (main.py).
    """
    motor = MotorBlindagemAmbiental(temperatura=temperatura, umidade=umidade)
    resultado = motor.executar()
    
    if frame is not None:
        import cv2
        cv2.putText(frame, "TTC GLOBAL // BLINDAGEM AMBIENTAL [ACTIVE]", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 102), 2, cv2.LINE_AA)
        cv2.putText(frame, f"ACAO: {resultado['acao']}", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (212, 175, 55), 1, cv2.LINE_AA)
        return frame
        
    return resultado

# Exemplo de execução via terminal
if __name__ == "__main__":
    res = processar(temperatura=26.6, umidade=45.0)
    print(f"[MÔNACA NÚCLEO] Ação: {res['acao']} | Tecnologia: {res['tecnologia']}")