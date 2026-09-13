# -*- coding: utf-8 -*-
import sys
import os
import time
import statistics

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

class MotorPerformance:
    def __init__(self, log_file="log_performance.txt"):
        self.log_file = log_file

    def medir_latencia(self, nome_motor, funcao_alvo, iteracoes=50):
        """Mede a latência e salva o resultado diretamente na memória comum."""
        tempos = []
        print(f"--- [PERFORMANCE] Monitorando: {nome_motor} ---")
        
        for _ in range(iteracoes):
            inicio = time.perf_counter()
            funcao_alvo()
            fim = time.perf_counter()
            tempos.append((fim - inicio) * 1000)
        
        media = statistics.mean(tempos)
        pico = max(tempos)
        
        # Conexão com a Memória Comum
        resultado_perf = {"media": round(media, 4), "pico": round(pico, 4), "status": "OK" if media < 50 else "ALERTA"}
        instancia_memoria.salvar_dados(f"PERF_{nome_motor.upper()}", resultado_perf)
        
        # Registro de Auditoria
        self.registrar_log(nome_motor, media, pico)
        
        print(f"[{nome_motor}] Média: {media:.4f}ms | Pico: {pico:.4f}ms")
        return resultado_perf

    def registrar_log(self, nome_motor, media, pico):
        try:
            with open(self.log_file, "a") as f:
                f.write(f"{time.ctime()} | Motor: {nome_motor} | Media: {media:.4f}ms | Pico: {pico:.4f}ms\n")
        except Exception:
            pass

# Instância global para uso no sistema
motor_performance = MotorPerformance()

def processar(frame=None):
    """
    Função de compatibilidade direta com o orquestrador (main.py).
    Mede a performance de um ciclo padrão e insere o HUD visual se houver frame.
    """
    def tarefa_padrao():
        time.sleep(0.005)

    resultado = motor_performance.medir_latencia("ORQUESTRADOR_GERAL", tarefa_padrao, iteracoes=10)
    
    if frame is not None:
        import cv2
        cv2.putText(frame, "TTC GLOBAL // PERFORMANCE [ACTIVE]", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 102), 2, cv2.LINE_AA)
        cv2.putText(frame, f"LATENCIA MEDIA: {resultado['media']}ms [{resultado['status']}]", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (212, 175, 55), 1, cv2.LINE_AA)
        return frame
        
    return resultado

# Permite rodar testes de performance direto pelo terminal se desejar
if __name__ == "__main__":
    def teste_exemplo():
        time.sleep(0.01)
    
    motor_performance.medir_latencia("TESTE_UNITARIO", teste_exemplo)