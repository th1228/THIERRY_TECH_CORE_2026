# -*- coding: utf-8 -*-
import sys
import os
import threading
import random
import time

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

try:
    import serial
except ImportError:
    serial = None

class GerenciadorHardwareBiometrico:
    def __init__(self, porta="COM3", baudrate=9600):
        self.porta = porta
        self.baudrate = baudrate
        self.conexao_ativa = False
        self.serial_conn = None
        
        self.dados_atuais = {
            "bpm": 76,
            "spo2": 99.0,
            "gsr": 1.2,
            "status": "SIMULADO (Aguardando Arduino)"
        }
        
        self.thread = threading.Thread(target=self._escutar_hardware, daemon=True)
        self.thread.start()

    def _escutar_hardware(self):
        while True:
            if serial is None:
                self._gerar_valores_simulados()
                self._sincronizar_memoria()
                time.sleep(0.5)
                continue

            try:
                if not self.conexao_ativa:
                    self.serial_conn = serial.Serial(self.porta, self.baudrate, timeout=1)
                    self.conexao_ativa = True
                    self.dados_atuais["status"] = "ARDUINO CONECTADO [AO VIVO]"
                
                linha = self.serial_conn.readline().decode('utf-8').strip()
                if linha:
                    partes = linha.split(",")
                    if len(partes) >= 3:
                        self.dados_atuais["bpm"] = int(partes[0])
                        self.dados_atuais["spo2"] = float(partes[1])
                        self.dados_atuais["gsr"] = float(partes[2])
            except Exception:
                self.conexao_ativa = False
                self._gerar_valores_simulados()
            
            self._sincronizar_memoria()
            time.sleep(0.5)

    def _gerar_valores_simulados(self):
        self.dados_atuais["bpm"] = 75 + random.randint(-2, 3)
        self.dados_atuais["spo2"] = 98 + (random.randint(0, 10) / 10.0)
        self.dados_atuais["gsr"] = 1.2 + (random.randint(-1, 1) / 10.0)

    def _sincronizar_memoria(self):
        """Salva os dados de hardware no barramento compartilhado 🧠."""
        try:
            memoria.salvar_dados("hardware_biometrico", self.dados_atuais)
        except Exception:
            pass

    def obter_dados(self):
        return self.dados_atuais

# Instância global para uso no ecossistema
_gerenciador_global = GerenciadorHardwareBiometrico()

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador 💻."""
    return _gerenciador_global.obter_dados()