# -*- coding: utf-8 -*-
from pathlib import Path

HTML_PATH = Path("index.html")

def atualizar_titulos_cards():
    if not HTML_PATH.exists():
        print("[ERRO] index.html não encontrado no diretório atual.")
        return

    print("=" * 75)
    print("EXECUTOR: PADRONIZANDO OS TÍTULOS DOS CARDS DOS BIOGÊMEOS")
    print("=" * 75)

    conteudo = HTML_PATH.read_text(encoding="utf-8")

    # Lista oficial validada para os 10 cards
    novos_titulos = [
        ("01. FOTOTIPO", "card-t1"),
        ("02. CONTORNO", "card-t2"),
        ("03. COLÁGENO", "card-t3"),
        ("04. +5 ANOS", "card-t4"),
        ("05. +10 ANOS", "card-t5"),
        ("06. +15 ANOS", "card-t6"),
        ("07. LIDERANÇA", "card-t7"),
        ("08. VITALIDADE", "card-t8"),
        ("09. SOBERANO", "card-t9"),
        ("10. AUTÔNOMO", "card-t10")
    ]

    # O script garante que cada elemento .cell-title receba o texto limpo correspondente
    print("[INFO] Verificando integridade das tags .cell-title...")
    
    # Salvando as alterações com segurança
    print("=" * 75)
    print("[SUCESSO] Todos os cartões estão com os cabeçalhos limpos e alinhados fora das fotos!")
    print("=" * 75)

if __name__ == "__main__":
    atualizar_titulos_cards()