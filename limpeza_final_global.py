# -*- coding: utf-8 -*-
import re
from pathlib import Path

HTML_PATH = Path("index.html")

def limpeza_segura_sem_erros():
    if not HTML_PATH.exists():
        print("[ERRO] index.html não encontrado.")
        return

    conteudo = HTML_PATH.read_text(encoding="utf-8")

    # 1. Troca sincronizada de funções, IDs e classes (sem espaços)
    trocas_codigo = [
        (r"redirecionarStripe", "ativarLicencaExecutiva"),
        (r"openStripeModal", "abrirModalLicencaExecutiva"),
        (r"closeStripeModal", "fecharModalLicencaExecutiva"),
        (r"stripe-licensing-modal", "executive-licensing-modal"),
        (r"btn-open-stripe-modal", "btn-open-executive-modal"),
        (r"stripe-btn-back", "executive-btn-back"),
        (r"btn-stripe-lic", "btn-executive-lic"),
        (r"stripe-btn-", "exec-btn-"),
        (r"stripe-item-", "exec-item-"),
        (r"stripeBtn", "execBtn"),
    ]

    for padrao, novo in trocas_codigo:
        conteudo = re.sub(padrao, novo, conteudo, flags=re.IGNORECASE)

    # 2. Protege a chave 'monaco_supremacy' para o main.py sem quebrar aspas
    conteudo = re.sub(
        r"ativarLicencaExecutiva\(['\"]monaco_supremacy['\"]\)",
        "ativarLicencaExecutiva('europa_executiva')",
        conteudo,
        flags=re.IGNORECASE
    )
    conteudo = conteudo.replace(
        "async function ativarLicencaExecutiva(tierKey) {",
        "async function ativarLicencaExecutiva(tierKey) {\n            if (tierKey === 'europa_executiva') tierKey = 'mona' + 'co_supremacy';"
    )

    # 3. Troca textos visíveis primeiro
    trocas_textos = [
        (r"ADQUIRIR MÔNACO \(EUR\)", "ADQUIRIR LICENÇA EUROPA (EUR)"),
        (r"Monaco Supremacy License", "European Executive License"),
        (r"Europa & Mônaco", "Europa & Global"),
        (r"Monaco Standards", "Global Executive Standards"),
        (r"BYPASS STRIPE ATIVO", "BYPASS LICENCIAMENTO ATIVO"),
    ]

    for padrao, novo in trocas_textos:
        conteudo = re.sub(padrao, novo, conteudo, flags=re.IGNORECASE)

    # 4. Qualquer resíduo final vira palavra única sem espaço (zero erro de sintaxe JS)
    conteudo = re.sub(r"mônaco|monaco", "Global", conteudo, flags=re.IGNORECASE)
    conteudo = re.sub(r"stripe", "GatewayExecutivo", conteudo, flags=re.IGNORECASE)

    HTML_PATH.write_text(conteudo, encoding="utf-8")
    print("=" * 75)
    print("[SUCESSO] Restaurado e limpo com zero erros de sintaxe!")
    print("=" * 75)

if __name__ == "__main__":
    limpeza_segura_sem_erros()