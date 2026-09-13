# -*- coding: utf-8 -*-
import sys
import os
from datetime import datetime, timedelta

# --- BLOCO DE CONEXÃO ESTRUTURAL ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    # Fallback para testes isolados
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

class MotorPrognostico:
    def __init__(self):
        self.tratamentos = ["Absolute Rep Molecular", "Davines", "Kerastase", "Joico", "Senscience", "CPR", "Nutri Wella"]
        self.massagens = ["Shiatsu", "Infomfacial", "Drenagem", "Ayurvédica"]
        self.frequencias = ["528Hz", "432Hz", "Lo-fi", "Binaural", "Ambient"]
        self.cortes = ["Curto Masculino", "Curto Feminino", "Médio Masculino", "Médio Feminino", "Longo", "Infantil", "Afro", "Ondulado", "Liso", "Caucasiano"]
        self.decisoes = ["Estratégica", "Assertiva", "Metódica"]
        self.status_toxina = ["Manutenção", "Absorção Ativa", "Reforço Osteométrico", "Estabilização"]

    def calcular_matriz_total(self):
        matriz = []
        hoje = datetime.now()
        
        for i in range(16):
            data = hoje + timedelta(days=i)
            clima = "Seco" if i % 2 == 0 else "Úmido"
            
            item = {
                "DATA": data.strftime("%d/%m"),
                "CLIMA": clima,
                "NECESSIDADE_HIDRATAÇÃO": "Intensiva" if clima == "Seco" else "Equilíbrio",
                "TRATAMENTO_CAPILAR": self.tratamentos[i % len(self.tratamentos)],
                "PENTEADO_CORTE": self.cortes[i % len(self.cortes)],
                "DECISÃO_ESTRATÉGICA": self.decisoes[i % len(self.decisoes)],
                "LADO_ESCUTA": "Direito" if i % 2 == 0 else "Esquerdo",
                "ÓLEO_TERAPIA": ["Gerânio", "Olíbano", "Lavanda", "Hortelã", "Capim-Limão"][i % 5],
                "MASSAGEM": self.massagens[i % len(self.massagens)],
                "TOM_VOZ": ["Alto", "Médio", "Baixo"][i % 3],
                "FREQUÊNCIA_MUSICAL": self.frequencias[i % len(self.frequencias)],
                "LONGEVIDADE_BOTULÍNICA": self.status_toxina[i % len(self.status_toxina)],
                "STATUS_NEURONAL": "Barreira Ativa"
            }
            matriz.append(item)
        
        return matriz

def iniciar():
    try:
        motor = MotorPrognostico()
        dados = motor.calcular_matriz_total()
        memoria.salvar_dados("PROGNOSTICO_16_DIAS", dados)
        print("[MOTOR PROGNÓSTICO] Matriz de 16 dias gerada e salva com sucesso.")
        return dados
    except Exception as e:
        print(f"[ERRO NO MOTOR PROGNÓSTICO] Falha na matriz: {e}")
        return None

def processar(frame=None):
    """
    Função de compatibilidade direta com o orquestrador (main.py).
    """
    dados = iniciar()
    
    if frame is not None:
        import cv2
        cv2.putText(frame, "TTC GLOBAL // PROGNOSTICO [ACTIVE]", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 102), 2, cv2.LINE_AA)
        cv2.putText(frame, "MATRIZ 16 DIAS: SINCRONIZADA", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (212, 175, 55), 1, cv2.LINE_AA)
        return frame
        
    return dados

if __name__ == "__main__":
    iniciar()