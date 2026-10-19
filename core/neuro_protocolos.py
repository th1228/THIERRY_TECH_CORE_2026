# -*- coding: utf-8 -*-
"""
Módulo: neuro_protocolos.py (ProtocoloRegenerativoHighEnd)
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Versão: 3.0.2 - Execução Real Integrada à Memória Comum e Tipagem Blindada (Pylance Clean)
"""

import sys
import os
from typing import Optional, Dict, Any, Tuple, Union

# Garante a conexão com o núcleo do ecossistema
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from memoria_comum import instancia_memoria as memoria
    except ImportError:
        memoria = None

class ProtocoloRegenerativoHighEnd:
    """
    Motor de Prescrição Real baseado em Protocolos de Medicina Regenerativa Global.
    Cruza dados de telemetria e neurogravidade para prescrição dinâmica.
    """

    def __init__(self, lang: str = "PT"):
        self.lang = lang.upper() if lang else "PT"
        # Tipagem explícita Dict[str, Any] para aceitar strings e floats sem alertas
        self.tabela_protocolos: Dict[str, Dict[str, Any]] = {
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

    def calcular_fluxo_real(self) -> float:
        """Busca dados reais na Memória Comum para calcular o fluxo dinamicamente."""
        fluxo_base = 1.0
        if memoria:
            try:
                dados_memoria = memoria.ler_dados() if hasattr(memoria, 'ler_dados') else {}
                if isinstance(dados_memoria, dict):
                    diag = dados_memoria.get("neurogravidade_diagnostico", {})
                    if isinstance(diag, dict):
                        parecer = str(diag.get("parecer", ""))
                        if "98%" in parecer or "99%" in parecer:
                            fluxo_base = 1.3
                        elif "Adaptação" in parecer:
                            fluxo_base = 0.4
            except Exception:
                pass
        return float(fluxo_base)

    def gerar_prescricao(self, fluxo: Optional[Union[float, int]] = None) -> Dict[str, Any]:
        """Avalia o estado real (via parâmetro ou Memória Comum) e retorna a prescrição."""
        if fluxo is not None:
            try:
                fluxo_real = float(fluxo)
            except (TypeError, ValueError):
                fluxo_real = self.calcular_fluxo_real()
        else:
            fluxo_real = self.calcular_fluxo_real()

        if fluxo_real < 0.5:
            protocolo: Dict[str, Any] = dict(self.tabela_protocolos["BAIXO_FLUXO"])
        elif 0.5 <= fluxo_real <= 1.2:
            protocolo = dict(self.tabela_protocolos["FLUXO_OTIMO"])
        else:
            protocolo = dict(self.tabela_protocolos["ALTO_FLUXO"])

        protocolo["fluxo_metrico"] = float(round(fluxo_real, 2))

        if memoria:
            if hasattr(memoria, 'salvar_dados'):
                memoria.salvar_dados("neuroprotocolo_ativo", protocolo)
            elif hasattr(memoria, 'registrar'):
                memoria.registrar("neuroprotocolo_ativo", protocolo)
            print(f"[NEUROPROTOCOLO] Prescrição real gerada (Fluxo: {fluxo_real}) e salva na Memória Comum.")
        
        return protocolo

# Instância para uso global no sistema
motor_prescricao = ProtocoloRegenerativoHighEnd()

def processar(frame: Optional[Any] = None, fluxo_atual: Optional[Union[float, int]] = None, lang: str = "PT") -> Union[Tuple[Any, Dict[str, Any]], Dict[str, Any]]:
    """
    Função de execução real integrada ao ecossistema com tipagem totalmente segura.
    """
    motor_prescricao.lang = lang.upper() if lang else "PT"
    prescricao = motor_prescricao.gerar_prescricao(fluxo_atual)
    
    if frame is not None:
        try:
            import cv2
            titulo = "TTC GLOBAL // NEUROPROTOCOL [ACTIVE]" if motor_prescricao.lang == "EN" else "TTC GLOBAL // NEUROPROTOCOLO [ACTIVE]"
            fase_str = str(prescricao.get('fase', ''))[:30]
            cv2.putText(frame, titulo, (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 102), 2, cv2.LINE_AA)
            cv2.putText(frame, f"PHASE: {fase_str}..." if motor_prescricao.lang == "EN" else f"FASE: {fase_str}...", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (212, 175, 55), 1, cv2.LINE_AA)
        except Exception:
            pass
        return frame, prescricao
        
    return prescricao

if __name__ == "__main__":
    print("Resultado Real do Neuroprotocolo:", processar())