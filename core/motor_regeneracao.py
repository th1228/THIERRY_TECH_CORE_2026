# -*- coding: utf-8 -*-
import sys
import os
import datetime

# --- BLOCO DE CONEXÃO ESTRUTURAL (NÃO MEXER) ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from memoria_comum import instancia_memoria
except ImportError:
    # Fallback para testes isolados
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    instancia_memoria = MemoriaMock()
# -----------------------------------------------

class MotorRegeneracao:
    """
    Motor de Gestão de Neuroplasticidade (Protocolo TTC-01)
    Integrado com a Memória Comum do sistema.
    """
    
    def __init__(self, log_path="prontuario_paciente.log"):
        self.oximetria_ideal = 98.0
        self.log_path = log_path
        
    def _validar_clima(self, clima_status):
        return 1.0 if clima_status == "OTIMIZADO" else 0.5

    def calcular_fpn(self, oximetria_atual, clima_status, estado_parasimp):
        """
        Calcula o Fator de Plasticidade Neuro-Regenerativa (FPN).
        """
        # 1. Termo de Estresse 📊
        diferenca = max(0, (self.oximetria_ideal - oximetria_atual))
        fator_estresse = max(0, (self.oximetria_ideal - diferenca) / self.oximetria_ideal)
        
        # 2. Termo Metabólico 🧬
        fator_clima = self._validar_clima(clima_status)
        
        # 3. Fator Parassimpático ⚡
        sp = 1.0 if estado_parasimp == "REPOUSO" else 0.2
        
        # 4. Cálculo Final 🧮
        fpn = round(fator_estresse * fator_clima * sp, 3)
        
        # Registro e Gravação 📝
        self._registrar_log(fpn, oximetria_atual)
        
        # Comunicação Direta com a Memória Comum 💾
        instancia_memoria.salvar_dados("FPN_ATUAL", fpn)
        
        print(f"[MOTOR REGENERAÇÃO] FPN calculado e salvo: {fpn}")
        return fpn

    def _registrar_log(self, fpn, ox):
        """ Gera registro de auditoria """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = 'AUTORIZADO' if fpn > 0.7 else 'RESTRITO'
        log_entry = f"[{timestamp}] | FPN: {fpn} | Oximetria: {ox} | Status: {status}\n"
        
        try:
            with open(self.log_path, "a") as f:
                f.write(log_entry)
        except Exception:
            pass

    def obter_status_protocolo(self, fpn):
        if fpn > 0.7:
            return "JANELA_ABERTA: Protocolo de Renovação Celular Iniciado"
        else:
            return "MODO_PROTECAO: Manter repouso metabólico"

# Instância global para uso no sistema
motor_regeneracao = MotorRegeneracao()

def processar(frame=None, oximetria=97.0, clima="OTIMIZADO", parasimp="REPOUSO"):
    """
    Função de ponte para integração direta com o orquestrador (main.py).
    """
    fpn = motor_regeneracao.calcular_fpn(oximetria, clima, parasimp)
    status_proto = motor_regeneracao.obter_status_protocolo(fpn)
    
    if frame is not None:
        import cv2
        cv2.putText(frame, "TTC GLOBAL // REGENERACAO [ACTIVE]", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 102), 2, cv2.LINE_AA)
        cv2.putText(frame, f"FPN: {fpn} | STATUS: {status_proto[:18]}...", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (212, 175, 55), 1, cv2.LINE_AA)
        return frame
        
    return fpn

# Permite rodar teste direto no terminal
if __name__ == "__main__":
    fpn_teste = motor_regeneracao.calcular_fpn(97.0, "OTIMIZADO", "REPOUSO")
    print(f"Status do Protocolo: {motor_regeneracao.obter_status_protocolo(fpn_teste)}")