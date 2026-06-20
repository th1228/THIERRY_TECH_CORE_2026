# -*- coding: utf-8 -*-
import serial
import json
import time

class MonacoComunicacao:
    def __init__(self, porta="COM3", baudrate=115200):
        try:
            self.ser = serial.Serial(porta, baudrate, timeout=1)
            time.sleep(2) # Tempo para estabilizar a conexão com o ESP32
            print(f"[COMUNICAÇÃO] Conectado com sucesso na porta {porta}")
        except Exception as e:
            print(f"[COMUNICAÇÃO] Erro ao conectar na porta {porta}: {e}")
            self.ser = None

    def ler_dados_esp32(self):
        """Lê os sensores via Serial e retorna o JSON como dicionário."""
        if self.ser and self.ser.in_waiting > 0:
            try:
                linha = self.ser.readline().decode('utf-8').strip()
                return json.loads(linha)
            except:
                return None
        return None