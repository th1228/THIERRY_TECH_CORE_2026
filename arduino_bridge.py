# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the 
intellectual property of Thierry Technology Concept Global. Unauthorized 
distribution, reverse engineering, or usage without a signed NDA/License 
agreement is strictly prohibited under international copyright frameworks.
===========================================================================
"""

import serial
import serial.tools.list_ports

def ler_dados_esp32(porta_serial=None, baudrate=115200):
    """
    Lê os dados ambientais e de sensores enviados pelo ESP32 via porta serial (USB).
    """
    if not porta_serial:
        portas = list(serial.tools.list_ports.comports())
        for p in portas:
            if "CP210" in p.description or "CH340" in p.description or "USB" in p.description:
                porta_serial = p.device
                break
        if not porta_serial and portas:
            porta_serial = portas[0].device

    if not porta_serial:
        print("[i] ESP32 não encontrado na USB. Sistema rodando em modo autônomo.")
        return None

    try:
        conexao = serial.Serial(porta_serial, baudrate, timeout=2)
        linha = conexao.readline().decode('utf-8').strip()
        conexao.close()
        
        if linha:
            print(f"[✓] Dados recebidos do ESP32: {linha}")
            return linha
    except (serial.SerialException, UnicodeDecodeError, OSError) as e:
        print(f"[!] Erro ao ler a porta serial: {e}")
    
    return None

if __name__ == "__main__":
    print("[*] Testando leitura do Hub de Sensores...")
    ler_dados_esp32()
