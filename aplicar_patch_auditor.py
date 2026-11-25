from pathlib import Path
import py_compile
import shutil
import sys

ALVO = Path("auditor_global_mercado.py")
BACKUP = Path("auditor_global_mercado.py.bak")


def main() -> int:
    if not ALVO.exists():
        print(f"[ERRO] Arquivo alvo nao encontrado: {ALVO}")
        return 1

    shutil.copy2(ALVO, BACKUP)
    print(f"[OK] Backup criado em: {BACKUP}")

    codigo = ALVO.read_text(encoding="utf-8")
    codigo_original = codigo

    # Padroniza quebras de linha e remove espacos em branco no fim das linhas
    linhas = [linha.rstrip() for linha in codigo.splitlines()]
    codigo_limpo = "\n".join(linhas) + "\n"

    if codigo_limpo != codigo_original:
        ALVO.write_text(codigo_limpo, encoding="utf-8")
        print("[OK] Formatacao limpa aplicada com sucesso.")
    else:
        print("[INFO] Nenhuma alteracao de espacamento necessaria.")

    py_compile.compile(str(ALVO), doraise=True)
    print(f"[OK] Compilacao verificada sem erros de sintaxe: {ALVO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())