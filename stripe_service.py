# -*- coding: utf-8 -*-
import os
import stripe

# Sua chave secreta oficial da Stripe configurada diretamente
stripe.api_key = "sk_test_51TvS1JC55HXXtTqcWignVHKR0LQNy8uAg3yQy121xrNKco7PYMzRkwavrM8nzRNPgrAzxrfQod3rCtmk3sGX3Dft00kZkKgUCD"

def criar_sessao_pagamento(nome_produto, valor_em_centavos):
    """
    Gera uma sessão de checkout diretamente na Stripe e retorna a URL de pagamento oficial.
    """
    try:
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