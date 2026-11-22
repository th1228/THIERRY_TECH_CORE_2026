# -*- coding: utf-8 -*-
import re
import shutil
from pathlib import Path

HTML_PATH = Path("index.html")
BACKUP_PATH = Path("index.html.bak")

def auditor_master_tcc():
    if not HTML_PATH.exists():
        print("[ERRO] index.html não encontrado no diretório.")
        return

    # 1. Backup de segurança obrigatório
    shutil.copy2(HTML_PATH, BACKUP_PATH)
    print(f"[INFO] Backup de segurança criado em: {BACKUP_PATH}")

    conteudo = HTML_PATH.read_text(encoding="utf-8")

    # 2. Troca APENAS os textos visíveis detectados no relatório (zero alteração em IDs, classes ou JS)
    trocas_visiveis = [
        # As 10 frases exatas reveladas pelo rastreador
        ("Thierry Technology Concept Global • Monaco Tier-1 Audit Terminal", "Thierry Technology Concept Global • Global Tier-1 Audit Terminal"),
        ("sob a Governança Mônaco.", "sob a Governança Global."),
        ("Stripe Secure Checkout 🔒", "Global Executive Secure Checkout 🔒"),
        ("LICENCIAMENTO TIER-1 MÔNACO", "LICENCIAMENTO EXECUTIVO TIER-1 GLOBAL"),
        ("Informações do Cartão de Crédito / Stripe Elements:", "Informações de Credencial Executiva / Gateway Global:"),
        ("sob os padrões da Governança Mônaco.", "sob os padrões da Governança Global."),
        ("[>] APLICAR PROTOCOLO MÔNACO", "[>] APLICAR PROTOCOLO GLOBAL"),
        ("FR • json - França (Paris / Monaco Border)", "FR • json - França (Paris / Riviera Executive)"),
        ("MC • json - Mônaco (Monte Carlo • Tier-1 Sovereign)", "EU • json - Europa Central (Tier-1 Sovereign)"),
        ("CENTRAL DE LICENCIAMENTO STRIPE • TCC GLOBAL", "CENTRAL DE LICENCIAMENTO EXECUTIVO • TCC GLOBAL"),
        ("ADQUIRIR MÔNACO (EUR)", "ADQUIRIR LICENÇA EUROPA (EUR)"),

        # Garantia dos nomes oficiais da barra lateral e botões
        ("Autoliderança & Comando Global", "Autoliderança & Comando Soberano"),
        ("Clínica (Estética / ROI)", "Clínica & Rejuvenescimento Facial"),
        ("Visagismo & Tricologia Avançada", "Visagismo & Tricologia Ultra Avançada"),
        ("Pilares de Arquitetura Sênior", "Pilares de Soberania Clínica"),
        ("Métricas Dinâmicas do Motor", "Telemetria Biométrica Avançada"),
        ("STATUS DO MOTOR GLOBAL", "STATUS DO NÚCLEO GLOBAL"),
        ("sob o Padrão Mônaco.", "sob o Padrão Global."),
        ("COMPRAR LICENÇA STRIPE", "ATIVAR LICENÇA EXECUTIVA"),
        ("MÔNACO TIER-1", "GLOBAL TIER-1"),
    ]

    alteracoes = 0
    for antigo, novo in trocas_visiveis:
        if antigo in conteudo:
            conteudo = conteudo.replace(antigo, novo)
            alteracoes += 1
            print(f"[OK] Texto atualizado: '{antigo}' -> '{novo}'")

    HTML_PATH.write_text(conteudo, encoding="utf-8")
    print("=" * 75)
    print(f"[SUCESSO] {alteracoes} textos visíveis limpos com 100% de segurança!")
    print("=" * 75)

if __name__ == "__main__":
    auditor_master_tcc()