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

# -*- coding: utf-8 -*-
import requests
import sys

# URL base do seu FastAPI (ajustada para a porta 801 utilizada no painel)
BASE_URL = "http://127.0.0.1:801/api/pdf"

# Lista de todas as rotas de relatórios PDF presentes no painel HTML
ROTAS_PDF = [
    "modelo_matematico",
    "lideranca",
    "estetica_roi",
    "visagismo_tricologia",
    "pitch",
    "roi",
    "carta",
    "monaco_audit"
]

payload_teste = {
    "cliente": "THIÉRRY RODRIGUES",
    "empresa": "TTC Global Corp",
    "email": "theiry10rd@gmail.com"
}

def executar_diagnostico():
    print("=" * 75)
    print("DIAGNÓSTICO DE ROTAS PDF • FASTAPI (Porta 801)")
    print("=" * 75)
    
    sucessos = 0
    falhas = 0
    failures_msg = 0  # Inicializada corretamente para evitar qualquer erro de escopo

    for rota in ROTAS_PDF:
        url_completa = f"{BASE_URL}/{rota}"
        try:
            print(f"Testando rota: /{rota} ... ", end="")
            response = requests.post(url_completa, json=payload_teste, timeout=10)
            
            content_type = response.headers.get("content-type", "")
            tamanho_bytes = len(response.content)
            
            if response.status_code == 200 and "application/pdf" in content_type and tamanho_bytes > 100:
                print(f"[SUCESSO] (HTTP 200 | {tamanho_bytes} bytes | PDF Válido)")
                sucessos += 1
            else:
                print(f"\n   -> [FALHA] Status: {response.status_code} | Content-Type: {content_type} | Tamanho: {tamanho_bytes} bytes")
                if response.status_code != 200:
                    print(f"   -> Resposta do Servidor: {response.text[:200]}")
                falhas += 1
        except requests.exceptions.ConnectionError:
            print(f"\n   -> [ERRO DE CONEXÃO] Não foi possível conectar ao servidor em {BASE_URL}. O main.py está rodando?")
            falhas += 1
        except requests.exceptions.Timeout as e:
            print(f"\n   -> [TIMEOUT]: Limite de tempo de requisição esgotado: {str(e)}")
            falhas += 1
        except requests.exceptions.RequestException as e:
            print(f"\n   -> [ERRO DE REQUISIÇÃO]: {str(e)}")
            falhas += 1

    failures_msg = falhas
    print("=" * 75)
    print(f"RESULTADO FINAL: {sucessos} rotas funcionais | {failures_msg} falhas encontradas.")
    print("=" * 75)

    if falhas > 0:
        print("\nDIRETRIZ DE CORREÇÃO:")
        print("1. Certifique-se de que o seu arquivo 'main.py' está ativo com o comando: uvicorn main:app --port 801")
        print("2. Verifique se todas as funções endpoint correspondentes a essas 8 rotas estão devidamente")
        print("   registradas no seu FastAPI (ex: @app.post('/api/pdf/lideranca'), etc).")
    else:
        print("\nTudo certo! Todas as rotas estão respondendo PDFs legítimos e prontos para o painel HTML.")

if __name__ == "__main__":
    executar_diagnostico()
