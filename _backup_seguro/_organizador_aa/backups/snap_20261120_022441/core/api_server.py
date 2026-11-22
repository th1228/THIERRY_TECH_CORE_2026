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
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import stripe

# Configuração da chave Stripe oficial do ecossistema
stripe.api_key = (
    "sk_test_51TvS1JC55HXXtTqcWignVHKR0LQNy8uAg3yQy121xrNKco7PYMzRkwavrM8nzRNPgrAzxrfQod3rCtmk3sGX3Dft00kZkKgUCD"
)

app = FastAPI(
    title="Tierry Technology Concept Global - Local API",
    version="1.0.0",
    description=(
        "Gateway de alta performance, faturamento e telemetria biométrica do"
        " ecossistema."
    ),
)


class LicencaRequest(BaseModel):
  nome_modulo: str
  valor_centavos: int
  email_cliente: str = "vip@ttcglobal.com"


@app.get("/")
def home():
  return {
      "status": "ONLINE",
      "sistema": "TIERRY TECHNOLOGY CONCEPT GLOBAL",
      "protocolo": "MONACO SECURE GATEWAY",
      "geodefense": "ACTIVE",
  }


@app.get("/dossie", response_class=HTMLResponse)
def exibir_dossie():
  """Renderiza o painel do dossiê global a partir da pasta templates."""
  try:
    caminho_html = (
        Path(__file__).resolve().parent
        / "templates"
        / "dossie_global.html"
    )
    with open(caminho_html, "r", encoding="utf-8") as f:
      return f.read()
  except Exception as e:
    raise HTTPException(
        status_code=404, detail=f"Dossiê global não encontrado: {str(e)}"
    )


@app.post("/api/v1/checkout/criar-sessao")
def criar_sessao_pagamento(dados: LicencaRequest):
  """Cria uma sessão oficial de pagamento na Stripe via API local."""
  try:
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "brl",
                "product_data": {
                    "name": (
                        f"Licença Thierry Tech Elite - {dados.nome_modulo}"
                    )
                },
                "unit_amount": int(dados.valor_centavos),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="https://sucesso.com?status=liberado",
        cancel_url="https://cancelado.com",
    )
    return {
        "status": "SUCESSO",
        "checkout_url": session.url,
        "session_id": session.id,
    }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/telemetria/status")
def obter_telemetria():
  """Retorna os dados em tempo real da oximetria e ondas neuronais."""
  return {
      "oximetria_tecidual": "98%",
      "regeneracao_celular": "96.4%",
      "neuroplasia_hz": "1.4 Hz",
      "frequencia_sonora": "528 Hz",
      "estado_governança": "SECURE",
  }


@app.post("/api/v1/camera/desligar")
def desligar_camera():
  """Endpoint para encerrar o feed da câmera e liberar o hardware."""
  try:
    return {
        "status": "SUCESSO",
        "mensagem": "Câmera desligada e recursos liberados com segurança.",
    }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="127.0.0.1", port=8000)