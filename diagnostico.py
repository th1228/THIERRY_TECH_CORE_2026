# -*- coding: utf-8 -*-
"""
Script de Diagnóstico - TCC Global
Simula o envio dos 5 tipos de relatórios para o backend FastAPI e verifica o retorno.
"""

import requests

URL = "http://127.0.0.1:801/gerar-pdf"
tipos_para_testar = [
    "biogem_core", 
    "estetica_roi", 
    "visagismo_tricologia", 
    "carta", 
    "modelagem"
]

print("=" * 60)
print(" INICIANDO DIAGNÓSTICO DE RETORNO DO PAINEL HTML")
print("=" * 60)

for tipo in tipos_para_testar:
    dados_form = {
        "tipo": tipo,
        "cliente": "Titular Teste",
        "empresa": "TTC Global Corp",
        "email": "teste@tccglobal.com",
        "operador": "Thierry (Diagnóstico)"
    }
    
    try:
        resposta = requests.post(URL, data=dados_form, timeout=5)
        content_disp = resposta.headers.get("content-disposition", "")
        
        if resposta.status_code == 200:
            print(f" [ENVIADO: {tipo.upper()}] -> Status 200 OK | Arquivo retornado: {content_disp}")
        else:
            print(f" [FALHA: {tipo.upper()}] -> Status {resposta.status_code} | Erro: {resposta.text}")
            
    except requests.exceptions.ConnectionError:
        print(" [ERRO CRÍTICO] O servidor FastAPI NÃO está rodando na porta 801. Certifique-se de que o main.py está ativo.")
        break

print("=" * 60)
print(" DIAGNÓSTICO FINALIZADO.")
print("=" * 60)
