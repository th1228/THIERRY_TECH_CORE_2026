import sys, os

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -*- coding: utf-8 -*-

TRADUCOES = {
    "PT": {
        "protocolo_ativo": "Protocolo Ativo",
        "total": "Total",
        "reposicao": "Vitamina C e Minerais Inclusos",
        "ghk_desc": "Protocolo GHK",
        "glow_desc": "Protocolo GLOW",
    },
    "EN": {
        "protocolo_ativo": "Active Protocol",
        "total": "Total",
        "reposicao": "Vitamin C and Minerals Included",
        "ghk_desc": "GHK Protocol",
        "glow_desc": "GLOW Protocol",
    },
}

# Idioma atual do sistema (pode ser alterado dinamicamente pelo gerente geográfico ou configuração)
IDIOMA_ATUAL = "PT"


def definir_idioma(sigla):
  global IDIOMA_ATUAL
  if sigla.upper() in TRADUCOES:
    IDIOMA_ATUAL = sigla.upper()


def t(chave):
  return TRADUCOES.get(IDIOMA_ATUAL, TRADUCOES["PT"]).get(chave, chave)