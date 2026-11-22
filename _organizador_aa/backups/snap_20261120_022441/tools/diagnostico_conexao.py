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

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Libera o CORS para evitar bloqueios do navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mapeamento exato das chaves de pagamento
STRIPE_LINKS = {
    "tatica_nacional": "https://buy.stripe.com/28E6oH6Pg6Pu5Ri3O3eZ204",
    "soberana_nacional": "https://buy.stripe.com/28E6oH6Pg6Pu5Ri3O3eZ204",
    "global_estrategica": "https://buy.stripe.com/3cI6oHehIfm05Ri98neZ207",
    "monaco_supremacy": "https://buy.stripe.com/eVq4gz7Tkgq44Ne2JZeZ205",
    "us_premium": "https://buy.stripe.com/4gM7sL8Xofm01B2fwLeZ206"
}

@app.post("/obter-link-stripe")
async def obter_link_stripe(tier: str = Form(...)):
    chave = tier.strip().lower().replace("-", "_")
    if chave in STRIPE_LINKS:
        return {"url_checkout": STRIPE_LINKS[chave]}
    raise HTTPException(status_code=400, detail=f"Tier '{tier}' não encontrado.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=801, reload=True)