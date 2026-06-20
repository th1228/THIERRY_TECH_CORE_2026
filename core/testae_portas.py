import serial.tools.list_ports

def encontrar_arduino():
    portas = list(serial.tools.list_ports.comports())
    for p in portas:
        if "Arduino" in p.description or "CH340" in p.description:
            return p.device
    return None # Nenhuma placa encontrada