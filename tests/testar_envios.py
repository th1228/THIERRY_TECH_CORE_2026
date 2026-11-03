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

import os
import smtplib
import socket
import ssl
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Carrega as variáveis do ficheiro .env
load_dotenv()

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465  # Porta SSL segura para o Gmail
SMTP_USER = os.getenv("SMTP_USER", "thelry10rd@gmail.com")
SMTP_PASS = os.getenv("SMTP_PASS", "")

PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "1350488628152077")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "")

def testar_smtp_avancado(destinatario_teste):
    print("\n==================================================")
    print("=== DIAGNÓSTICO FORENSE DO SMTP (GMAIL) ===")
    print("==================================================")
    print(f"Utilizador configurado: {SMTP_USER}")
    print(f"Servidor Alvo: {SMTP_HOST}:{SMTP_PORT}")
    
    if not SMTP_PASS:
        print("[FALHA CRÍTICA]: A palavra-passe do SMTP (SMTP_PASS) está vazia no .env!")
        return

    # Passo 1: Testar conectividade TCP pura
    print("\n[Passo 1/3] A testar conectividade TCP de rede com o Google...")
    try:
        sock = socket.create_connection((SMTP_HOST, SMTP_PORT), timeout=10)
        print("[SUCESSO TCP]: A ligação de rede à porta do Google foi aberta com sucesso.")
        sock.close()
    except socket.timeout:
        print("[FALHA DE REDE]: Tempo limite esgotado. O firewall ou a rede bloqueiam a porta 465!")
        return
    except Exception as e:
        print(f"[FALHA DE REDE INESPERADA]: {type(e).__name__} -> {e}")
        return

    # Passo 2 & 3: Testar o canal SSL e a Autenticação
    print("\n[Passo 2/3] A estabelecer o canal seguro SSL e handshake com o Gmail...")
    try:
        contexto_ssl = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=contexto_ssl, timeout=10) as servidor:
            print("[SUCESSO SSL]: Canal seguro estabelecido com o Google.")
            
            print("\n[Passo 3/3] A tentar autenticação com a palavra-passe de aplicação...")
            servidor.login(SMTP_USER, SMTP_PASS)
            print("[SUCESSO AUTENTICAÇÃO]: O Google validou as credenciais com sucesso!")
            
            msg = MIMEMultipart()
            msg['From'] = SMTP_USER
            msg['To'] = destinatario_teste
            msg['Subject'] = "Diagnóstico Forense TCC Global - SMTP"
            msg.attach(MIMEText("Este é o teste forense de envio de e-mail do TCC Global.", 'plain', 'utf-8'))
            
            servidor.sendmail(SMTP_USER, destinatario_teste, msg.as_string())
            print("[SUCESSO TOTAL]: E-mail enviado e despachado pelo SMTP!")
            
    except smtplib.SMTPAuthenticationError as e:
        # Linha corrigida corretamente com f-string e aspas
        print(f"\n[FALHA DE AUTENTICAÇÃO DO GOOGLE]: Código {e.smtp_code} | Resposta: {e.smtp_error.decode('utf-8', errors='ignore')}")
    except ssl.SSLError as e:
        print(f"\n[FALHA DE SSL/CERTIFICADO]: Erro de criptografia. Detalhes: {e}")
    except Exception as e:
        print(f"\n[FALHA CRÍTICA NO SMTP]: Tipo: {type(e).__name__} | Mensagem: {e}")

def testar_whatsapp_meta(telefone_destino):
    print("\n==================================================")
    print("=== DIAGNÓSTICO WHATSAPP (META CLOUD API) ===")
    print("==================================================")
    if not ACCESS_TOKEN:
        print("[FALHA]: WHATSAPP_ACCESS_TOKEN não está configurado.")
        return
        
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": telefone_destino,
        "type": "text",
        "text": {"body": "Teste de diagnóstico TCC Global: Mensagem via Meta API."}
    }
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"A enviar requisição para a Meta API (ID: {PHONE_NUMBER_ID})...")
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        print(f"Status HTTP retornado pela Meta: {resp.status_code}")
        print(f"Corpo da resposta: {resp.text}")
        if resp.status_code in [200, 201]:
            print("[SUCESSO] WhatsApp despachado pela Meta!")
        else:
            print("[FALHA] A Meta rejeitou o envio.")
    except Exception as e:
        print(f"[FALHA DE REDE/CONEXÃO WHATSAPP]: {e}")

if __name__ == "__main__":
    print("=== INICIANDO SCRIPT DE DIAGNÓSTICO FORENSE TCC GLOBAL ===")
    email_teste = "thelry10rd@gmail.com"
    telefone_teste = "5598987569494"
    
    testar_smtp_avancado(email_teste)
    testar_whatsapp_meta(telefone_teste) 