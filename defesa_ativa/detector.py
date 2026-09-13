import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -*- coding: utf-8 -*-
import json
import os

# Configuração do caminho do arquivo de blacklist
BLACKLIST_FILE = os.path.join(os.path.dirname(__file__), 'blacklist.json')

def iniciar_monitoramento():
    """Ativa o monitoramento de ameaças."""
    print("[DETECTOR] Monitoramento de ameaças iniciado.")
    if not os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, 'w') as f:
            json.dump({"ips_bloqueados": []}, f)
    return True

def carregar_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        return {"ips_bloqueados": []}
    with open(BLACKLIST_FILE, 'r') as f:
        return json.load(f)

def is_ip_bloqueado(ip_do_usuario):
    data = carregar_blacklist()
    return ip_do_usuario in data["ips_bloqueados"]

def adicionar_ao_blacklist(ip_do_usuario):
    data = carregar_blacklist()
    if ip_do_usuario not in data["ips_bloqueados"]:
        data["ips_bloqueados"].append(ip_do_usuario)
        with open(BLACKLIST_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"[DETECTOR] IP {ip_do_usuario} adicionado à blacklist.")

def verificar_anomalia():
    """
    Função necessária para o main.py.
    Verifica comportamento anômalo (ex: se o IP do usuário está na blacklist).
    Retorna True se houver anomalia, False caso contrário.
    """
    # Exemplo de integração: verificar se o IP local está bloqueado
    # Como não temos um IP real agora, mantemos a verificação baseada na lista
    data = carregar_blacklist()
    if len(data["ips_bloqueados"]) > 0:
        print("[DETECTOR] Anomalia detectada: IP em blacklist.")
        return True
    return False