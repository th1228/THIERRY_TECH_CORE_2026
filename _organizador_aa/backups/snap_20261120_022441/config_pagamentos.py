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

# config_pagamentos.py

STRIPE_PRODUCTS = {
    # Licenciamento Global / USD (Américas, Oriente Médio, Ásia e Global)
    "LICENCA_MONACO_USD": {
        "name": "LICENÇA TCCGLOBAL - MONACO SUPREMACY",
        "price": 999999.00,
        "currency": "usd",
        "interval": "year",
        "payment_link": "https://buy.stripe.com/dRm7sLc9A8XCbbCckzeZ20b",
        "active": True
    },
    
    # Licenciamento Europa / Zona Euro (EUR)
    "LICENCA_MONACO_EUR": {
        "name": "LICENÇA MONACO EUR",
        "price": 999999.00,
        "currency": "eur",
        "interval": "year",
        "payment_link": "https://buy.stripe.com/dRmaEX4H80r64Ne1FVeZ20c",
        "active": True
    }
}

def obter_link_pagamento(regiao="global"):
    """
    Retorna o link de pagamento e o produto Stripe correspondente 
    com base na região do cliente (ex: 'europe' ou 'global').
    """
    if regiao.lower() in ["europe", "europa", "eur"]:
        return STRIPE_PRODUCTS["LICENCA_MONACO_EUR"]
    
    # Padrão global / Oriente Médio / Américas em USD
    return STRIPE_PRODUCTS["LICENCA_MONACO_USD"]