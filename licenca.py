import os
import uuid
import platform

# Se preferir manter separado, garanta que o config_pagamentos.py tenha os links corretos.
# Caso contrário, você pode colar os links da Stripe diretamente nas chaves abaixo.
try:
    from config_pagamentos import PAYMENT_LINKS
except ImportError:
    PAYMENT_LINKS = {}

# Protocolo de Blindagem e Multa
PROTOCOLOS_SEGURANCA = {
    "MULTA_GLOBAL_USD": 1000000.00,  # Ajustado para 1 milhão por violação contratual
    "ACAO_VIOLACAO": "SUSPENDED_BY_GEO_VIOLATION",
    "KILL_SWITCH": "Limpeza completa de memória RAM e registro em LogSeguro"
}

def obter_hwid():
    """Identifica o ID único da máquina para evitar cópias piratas (Trava de Nó)."""
    return str(uuid.getnode())

def verificar_integridade(node_id_atual, node_id_registrado):
    """Valida se o hardware atual é exatamente o mesmo da ativação original."""
    return node_id_atual == node_id_registrado

def aplicar_multa(categoria_mercado):
    """Gera o termo de penalidade por quebra contratual (Sovereign Gate)."""
    if categoria_mercado != "BR":
        return f"ALERTA CRÍTICO: Violação contratual detectada. Multa de penalidade no valor de USD {PROTOCOLOS_SEGURANCA['MULTA_GLOBAL_USD']:,.2f} aplicada ao nó infrator."
    return "Penalidade aplicada conforme termos do contrato comercial nacional."

# CONFIGURAÇÃO DO ECOSSISTEMA TTC GLOBAL - PROPRIEDADE INTELECTUAL DE ELITE
CONFIGURACAO = {
    "BR_COMERCIAL": {
        "descricao": "Mercado Nacional Oficial - Alta Segurança e Restrição por Nó",
        "moeda": "R$",
        "planos": {
            "Tatica_Nacional": {
                "valor": 50000.00, 
                "meses": 6, 
                "nos_permitidos": 1, 
                "libera": ["salao_biometria"],
                "link_stripe": PAYMENT_LINKS.get("licenca_tatica_nacional", "https://buy.stripe.com/SEU_LINK_REAL_AQUI")
            },
            "Estrategica_Nacional": {
                "valor": 100000.00, 
                "meses": 12, 
                "nos_permitidos": 1, 
                "libera": ["salao_biometria", "clinica"],
                "link_stripe": PAYMENT_LINKS.get("licenca_estrategica_nacional", "https://buy.stripe.com/SEU_LINK_REAL_AQUI")
            },
            "Anual_Nacional": {
                "valor": 150000.00, 
                "meses": 12, 
                "nos_permitidos": 1, 
                "libera": ["salao_biometria", "clinica", "forense_basica"],
                "link_stripe": PAYMENT_LINKS.get("licenca_anual_nacional", "https://buy.stripe.com/SEU_LINK_REAL_AQUI")
            },
            "Soberana_Nacional": {
                "valor": 200000.00, 
                "meses": 12, 
                "nos_permitidos": 1, 
                "libera": ["salao_biometria", "clinica", "forense", "core_global"],
                "link_stripe": PAYMENT_LINKS.get("licenca_soberana_nacional", "https://buy.stripe.com/SEU_LINK_REAL_AQUI")
            }
        }
    },
    "GLOBAL_SOVEREIGN_TIERS": {
        "descricao": "Top 10 World Nodes - Propriedade Intelectual e Monopólio Regional",
        "paises_suportados": ["US", "MC", "AE", "EU", "CH", "DE", "FR", "UK", "SG", "QA"],
        "planos_internacionais": {
            "Monaco_Supremacy": {
                "duracao_meses": 12,
                "valor_brl": 999999.00,
                "descricao_codigo": "Licença Exclusiva Mônaco Supremacy",
                "link_stripe": PAYMENT_LINKS.get("licenca_monaco_supremacy", "https://buy.stripe.com/SEU_LINK_REAL_AQUI")
            },
            "Premium_EUA": {
                "duracao_meses": 12,
                "valor_brl": 999999.00,
                "descricao_codigo": "Monitoramento EAR, Oximetria, Ciclos Cutâneos - EUA",
                "link_stripe": PAYMENT_LINKS.get("licenca_premium_eua", "https://buy.stripe.com/SEU_LINK_REAL_AQUI")
            },
            "Global_Estrategica": {
                "duracao_meses": 12,
                "valor_brl": 999999.00,
                "descricao_codigo": "Atualizações Nível 9, Auditoria LogSeguro - Global",
                "link_stripe": PAYMENT_LINKS.get("licenca_global_estrategica", "https://buy.stripe.com/SEU_LINK_REAL_AQUI")
            },
            "Premio_Emirados_EAU": {
                "duracao_meses": 12,
                "valor_brl": 999999.00,
                "descricao_codigo": "Monopólio Regional Estrito - Emirados Árabes",
                "link_stripe": PAYMENT_LINKS.get("licenca_premio_emirados_eau", "https://buy.stripe.com/SEU_LINK_REAL_AQUI")
            }
        },
        "regra_seguranca_global": {
            "raio_km": 100,
            "status_violacao": "SUSPENDED_BY_GEO_VIOLATION",
            "multa_penalidade_usd": 1000000.00,
            "acao_kill_switch": "Limpeza completa de memória RAM e registro em LogSeguro"
        }
    }
}

def obter_detalhes_licenca(categoria_mercado, plano_nome):
    """Retorna os parâmetros de valor, vigência, restrição de nós e o link de pagamento do Stripe."""
    if categoria_mercado == "BR":
        config = CONFIGURACAO["BR_COMERCIAL"]["planos"].get(plano_nome)
        if config:
            return {**config, "mercado": "BR_COMERCIAL", "status": "sucesso"}
            
    elif categoria_mercado in CONFIGURACAO["GLOBAL_SOVEREIGN_TIERS"]["paises_suportados"]:
        global_config = CONFIGURACAO["GLOBAL_SOVEREIGN_TIERS"]["planos_internacionais"].get(plano_nome)
        if global_config:
            return {**global_config, "mercado": f"GLOBAL_{categoria_mercado}", "status": "sucesso"}
            
    return {"status": "erro", "mensagem": "Parâmetros de licenciamento inválidos ou não autorizados."}

def validar_acesso(categoria_mercado, plano_nome, hardware_id):
    """
    Função principal de controle: Verifica a integridade da licença, 
    executa a trava de hardware e aplica multa contratual caso haja violação.
    """
    detalhes = obter_detalhes_licenca(categoria_mercado, plano_nome)
    
    if detalhes["status"] == "erro":
        return detalhes
    
    # Validação de Hardware (Trava de Nó)
    if not verificar_integridade(hardware_id, obter_hwid()):
        return {
            "status": "bloqueado",
            "mensagem": "Violação de nó de hardware detectada. Acesso revogado imediatamente."
        }
        
    # Acionamento de Multa e Segurança Global
    if categoria_mercado != "BR":
        detalhes["protocolo_multa"] = aplicar_multa(categoria_mercado)
        detalhes["status_seguranca"] = PROTOCOLOS_SEGURANCA["ACAO_VIOLACAO"]
        detalhes["acao_kill_switch"] = PROTOCOLOS_SEGURANCA["KILL_SWITCH"]
        
    return detalhes