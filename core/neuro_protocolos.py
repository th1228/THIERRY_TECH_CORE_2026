# -*- coding: utf-8 -*-
import sys
import os

# Garante a conexão com o núcleo do ecossistema
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.memoria_comum import instancia_memoria as memoria
except ImportError:
    memoria = None

class ProtocoloRegenerativoHighEnd:
    """
    Motor de Prescrição Baseado em Protocolos de Medicina Regenerativa Global.
    Focado em Neurogenese e Modulação Mitocondrial.
    """

    def __init__(self):
        self.tabela_protocolos = {
            "BAIXO_FLUXO": {
                "fase": "Protocolo de Otimização Mitocondrial",
                "intervencao": "Protocolo NAD+ / Coenzima Q10 (Ubiquinol) 200mg",
                "estimulo": "Fotobiomodulação (Infravermelho Próximo) 810nm - 15 min",
                "objetivo": "Aumentar a biogênese mitocondrial para suporte a novos neurônios."
            },
            "FLUXO_OTIMO": {
                "fase": "Janela Ápice de Neurogenese",
                "intervencao": "Protocolo Senolítico (Fisetina 500mg / Quercetina 500mg)",
                "estimulo": "Jejum intermitente estratégico (16h) + Meditação Guiada Delta",
                "objetivo": "Apoptose seletiva de células senescentes e ativação de BDNF."
            },
            "ALTO_FLUXO": {
                "fase": "Protocolo de Reparo e Homeostase",
                "intervencao": "Protocolo de Magnésio Treonato + L-Teanina",
                "estimulo": "Imersão em água fria (ou Vagal Tone Exercises)",
                "objetivo": "Redução do estresse oxidativo e estabilização de membrana neuronal."
            }
        }

    def gerar_prescricao(self, fluxo: float) -> dict:
        """Avalia o estado real do cliente e retorna a prescrição regenerativa."""
        if fluxo < 0.5:
            protocolo = self.tabela_protocolos["BAIXO_FLUXO"]
        elif 0.5 <= fluxo <= 1.2:
            protocolo = self.tabela_protocolos["FLUXO_OTIMO"]
        else:
            protocolo = self.tabela_protocolos["ALTO_FLUXO"]

        # Persistência automática na Memória Comum
        if memoria:
            memoria.salvar_dados("neuroprotocolo_ativo", protocolo)
            print("[NEUROPROTOCOLO] Prescrição gerada e salva na Memória Comum.")
        
        return protocolo

# Instância para uso global no sistema
motor_prescricao = ProtocoloRegenerativoHighEnd()

def processar(frame=None, fluxo_atual=1.0):
    """
    Função de compatibilidade direta com o orquestrador (main.py).
    Avalia o fluxo, salva na memória e opcionalmente desenha o status no HUD se houver frame.
    """
    prescricao = motor_prescricao.gerar_prescricao(fluxo_atual)
    
    if frame is not None:
        import cv2
        cv2.putText(frame, "TTC GLOBAL // NEUROPROTOCOLO [ACTIVE]", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 102), 2, cv2.LINE_AA)
        cv2.putText(frame, f"FASE: {prescricao['fase'][:30]}...", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (212, 175, 55), 1, cv2.LINE_AA)
        return frame
        
    return prescricao

if __name__ == "__main__":
    # Teste isolado do motor
    resultado = motor_prescricao.gerar_prescricao(0.8)
    print("Protocolo de Teste:", resultado)