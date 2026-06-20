# -*- coding: utf-8 -*-
import os
import json
import sys
import serial  # Certifique-se de ter instalado: pip install pyserial
from datetime import datetime

# Garante que o Python encontre o pacote 'core'
raiz = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(raiz))

# --- CONFIGURAÇÃO DO MOTOR ---
# Ajuste a porta COM3 para a que aparecer no seu Gerenciador de Dispositivos
PORTA_SERIAL = 'COM3' 

# Tenta carregar o preditor se existir
try:
    import neuro_gravidade_preditor
except ImportError:
    neuro_gravidade_preditor = None

# Define a pasta de laudos
PASTA_LAUDO = os.path.join(raiz, "..", "laudos")
if not os.path.exists(PASTA_LAUDO):
    os.makedirs(PASTA_LAUDO)

def disparar_motor():
    """Tenta disparar o motor, mas ignora silenciosamente se o hardware não estiver lá."""
    try:
        # Tenta abrir a porta e enviar o comando
        arduino = serial.Serial(PORTA_SERIAL, 9600, timeout=1)
        arduino.write(b'1')
        arduino.close()
        print("[MOTOR] Comando de giro enviado com sucesso.")
    except (serial.SerialException, FileNotFoundError):
        # Esta parte é a sua segurança: se não encontrar o hardware, ele apenas avisa
        print("[MOTOR] Simulando disparo: Hardware não detectado (Tudo normal para testes).")
    except Exception as e:
        print(f"[MOTOR] Erro inesperado ao tentar acionar o motor: {e}")

def _obter_caminho_arquivo():
    nome_cliente = "cliente_padrao" 
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(PASTA_LAUDO, f"{nome_cliente}_{data_hoje}.json")

def salvar(modulo, dados):
    try:
        arquivo_path = _obter_caminho_arquivo()
        conteudo = {}
        if os.path.exists(arquivo_path):
            with open(arquivo_path, "r", encoding="utf-8") as f:
                try: conteudo = json.load(f)
                except: conteudo = {}
        
        conteudo[modulo] = dados
        with open(arquivo_path, "w", encoding="utf-8") as f:
            json.dump(conteudo, f, ensure_ascii=False, indent=4)
        
        # Após salvar com sucesso, disparamos o motor
        disparar_motor()
            
    except Exception as e:
        print(f"[MOTOR] Erro ao salvar: {e}")

def ler(modulo):
    arquivo_path = _obter_caminho_arquivo()
    if not os.path.exists(arquivo_path): return None
    try:
        with open(arquivo_path, "r", encoding="utf-8") as f:
            conteudo = json.load(f)
            return conteudo.get(modulo)
    except: return None

def obter_laudo_completo():
    arquivo_path = _obter_caminho_arquivo()
    laudo = {}
    if os.path.exists(arquivo_path):
        with open(arquivo_path, "r", encoding="utf-8") as f:
            try: laudo = json.load(f)
            except: laudo = {}
    
    if neuro_gravidade_preditor:
        try:
            dados_camera = {'simetria_mandibula': '98%', 'densidade_mao': 'Nível 8'}
            resultado = neuro_gravidade_preditor.processar(dados_camera)
            laudo["neurogravidade"] = resultado.get("neurogravidade", "Processado")
        except Exception as e:
            laudo["neurogravidade"] = f"Erro no preditor: {e}"
    else:
        laudo["neurogravidade"] = "Módulo de Predição não instalado"
            
    return laudo

if __name__ == "__main__":
    print("[MOTOR] Sistema pronto e carregado.")