import ast
import shutil
from pathlib import Path

ALVO = Path("core/visagismo_estetica_roi.py")

BLOCO_IMPORT = """try:
    from core.c2_sovereign_intelligence import BiogemEngine
except ImportError:
    from c2_sovereign_intelligence import BiogemEngine"""


def main() -> None:
    if not ALVO.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {ALVO}")

    conteudo = ALVO.read_text(encoding="utf-8")
    linha_antiga = "from c2_sovereign_intelligence import BiogemEngine"

    if linha_antiga not in conteudo and "from core.c2_sovereign_intelligence import BiogemEngine" not in conteudo:
        raise RuntimeError("Linha de importação esperada não encontrada em core/visagismo_estetica_roi.py.")

    if "from core.c2_sovereign_intelligence import BiogemEngine" not in conteudo:
        novo_conteudo = conteudo.replace(linha_antiga, BLOCO_IMPORT, 1)
    else:
        novo_conteudo = conteudo

    ast.parse(novo_conteudo, filename=str(ALVO))
    bak = ALVO.with_suffix(ALVO.suffix + ".bak")
    shutil.copy2(ALVO, bak)
    ALVO.write_text(novo_conteudo, encoding="utf-8")
    print(f"[OK] Importação corrigida em {ALVO} (backup em {bak})")


if __name__ == "__main__":
    main()