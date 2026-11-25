import ast
import re
import shutil
from pathlib import Path

RAIZ = Path(".")
IGNORAR_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "backups",
}

PADRAO_CLASSE_MOCK = re.compile(
    r"^(?P<indent>[ \t]*)class MemoriaMock:[^\n]*\n"
    r"(?:(?P=indent)[ \t]+[^\n]*\n|[ \t]*\n)*",
    re.MULTILINE,
)


def montar_bloco_identado(indent: str) -> str:
    corpo = [
        "class MemoriaMock:",
        "    def __init__(self):",
        "        self._dados = {}",
        "",
        "    def salvar_dados(self, chave, valor):",
        "        self._dados[chave] = valor",
        "        return True",
        "",
        "    def registrar(self, chave, valor):",
        "        self._dados[chave] = valor",
        "        return True",
        "",
        "    def ler_dados(self, chave):",
        "        return self._dados.get(chave)",
    ]
    return "\n".join((indent + linha) if linha else "" for linha in corpo) + "\n"


def listar_arquivos_py() -> list[Path]:
    arquivos = []
    for p in sorted(RAIZ.rglob("*.py")):
        if any(parte in IGNORAR_DIRS for parte in p.parts):
            continue
        if p.name.endswith(".bak") or p.name == "aplicar_memoria_mock.py":
            continue
        arquivos.append(p)
    return arquivos


def tem_memoria_mock_pass(texto: str) -> bool:
    if "class MemoriaMock:" not in texto:
        return False
    try:
        arvore = ast.parse(texto)
    except SyntaxError:
        return False

    for node in ast.walk(arvore):
        if isinstance(node, ast.ClassDef) and node.name == "MemoriaMock":
            for item in node.body:
                if (
                    isinstance(item, ast.FunctionDef)
                    and item.name in {"salvar_dados", "registrar"}
                    and len(item.body) == 1
                    and isinstance(item.body[0], ast.Pass)
                ):
                    return True
    return False


def main() -> None:
    arquivos = listar_arquivos_py()
    alterados = 0
    erros_sintaxe = 0

    for arq in arquivos:
        texto = arq.read_text(encoding="utf-8", errors="replace")
        if not tem_memoria_mock_pass(texto):
            continue

        match = PADRAO_CLASSE_MOCK.search(texto)
        if not match:
            continue

        indent = match.group("indent")
        bloco_novo = montar_bloco_identado(indent)
        novo_texto = texto[: match.start()] + bloco_novo + texto[match.end() :]

        if novo_texto == texto:
            continue

        try:
            ast.parse(novo_texto, filename=str(arq))
        except SyntaxError as exc:
            erros_sintaxe += 1
            print(f"[AVISO] Sintaxe invalida apos substituicao em {arq}: {exc}")
            continue

        backup = arq.with_name(arq.name + ".bak")
        shutil.copy2(arq, backup)
        arq.write_text(novo_texto, encoding="utf-8")
        alterados += 1
        print(f"[OK] Atualizado (backup em {backup.name}): {arq}")

    print("-" * 60)
    print(f"Arquivos atualizados : {alterados}")
    print(f"Erros de sintaxe     : {erros_sintaxe}")


if __name__ == "__main__":
    main()