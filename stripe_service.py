# -*- coding: utf-8 -*-
import os
import stripe
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Puxa a chave da Stripe de forma segura via variável de ambiente (Blindado para Auditoria)
stripe.api_key = os.getenv("STRIPE_API_KEY", "")

def criar_sessao_pagamento(nome_produto, valor_em_centavos):
    """
    Gera uma sessão de checkout diretamente na Stripe e retorna a URL de pagamento oficial.
    """
    try:
        if not stripe.api_key:
            print("[ERRO STRIPE] Chave da Stripe não encontrada nas variáveis de ambiente (.env).")
            return None

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'brl',
                    'product_data': {
                        'name': nome_produto,
                    },
                    'unit_amount': int(valor_em_centavos),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://sucesso.com',
            cancel_url='https://cancelado.com',
        )
        return session.url
    except Exception as e:
        print(f"[ERRO STRIPE] Falha ao criar sessão de pagamento: {e}")
        return None