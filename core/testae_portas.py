
# --- PONTE DE MEMÓRIA AUTOMÁTICA (THIERRY TECH) ---
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:
        class MemoriaMock:
            def salvar_dados(self, chave, valor): pass
            def registrar(self, chave, valor): pass
            def ler_dados(self, chave): return None
        memoria = MemoriaMock()
# ---------------------------------------------------

import sys, os

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys, os

import serial.tools.list_ports

def encontrar_arduino():
    portas = list(serial.tools.list_ports.comports())
    for p in portas:
        if "Arduino" in p.description or "CH340" in p.description:
            return p.device
    return None # Nenhuma placa encontrada