# -*- coding: utf-8 -*-
from pathlib import Path
import re

HTML_PATH = Path("index.html")

def limpar_chaves_vazias_css():
    if not HTML_PATH.exists():
        print("[ERRO] index.html não encontrado.")
        return

    print("=" * 75)
    print("AUDITOR: REMOVENDO BLOCOS CSS VAZIOS PARA LIMPAR A ABA DE PROBLEMAS")
    print("=" * 75)

    conteudo = HTML_PATH.read_text(encoding="utf-8")

    # Regex cirúrgica para encontrar seletores CSS com chaves totalmente vazias (ex: .classe { }) e removê-los
    conteudo_limpo, count = re.subn(r'[a-zA-Z0-9_.-]+\s*\{\s*\}', '', conteudo)

    HTML_PATH.write_text(conteudo_limpo, encoding="utf-8")

    print("=" * 75)
    print(f"[SUCESSO] {count} blocos vazios foram eliminados do ficheiro!")
    print("-> Guarde o ficheiro, execute o script no terminal e veja a aba 'Problems' limpar-se instantaneamente.")
    print("=" * 75)

if __name__ == "__main__":
    limpar_chaves_vazias_css()