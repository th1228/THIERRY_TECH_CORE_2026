# Central de Links de Pagamento - TTC Global
# Mapeamento oficial sincronizado com os valores do painel Stripe

PAYMENT_LINKS = {
    # Nacionais
    "licenca_tatica_nacional": "https://buy.stripe.com/5kQ3cv0qSc9OenOckzeZ200",     # R$ 50.000,00
    "licenca_estrategica_nacional": "https://buy.stripe.com/28E28r5Lc1va0wYckzeZ201",  # R$ 100.000,00
    "licenca_anual_nacional": "https://buy.stripe.com/eVq6oHflMc9ObbCckzeZ202",         # R$ 150.000,00
    "licenca_soberana_nacional": "https://buy.stripe.com/28E6oH6Pg6Pu5Ri3O3eZ204",     # R$ 200.000,00
    
    # Internacionais / Elite (R$ 999.999,00)
    "licenca_monaco_supremacy": "https://buy.stripe.com/eVq4gz7Tkgq44Ne2JZeZ205",      # R$ 999.999,00
    "licenca_premium_eua": "https://buy.stripe.com/4gM7sL8Xofm01B2fwLeZ206",           # R$ 999.999,00
    "licenca_global_estrategica": "https://buy.stripe.com/3cI6oHehIfm05Ri98neZ207",    # R$ 999.999,00
    "licenca_premio_emirados_eau": "https://buy.stripe.com/9B64gz7Tka1G6Vm4S7eZ208"    # R$ 999.999,00
}

def get_link(key):
    """Retorna o link de pagamento correspondente à chave especificada."""
    return PAYMENT_LINKS.get(key)