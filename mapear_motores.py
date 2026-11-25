import ast
from pathlib import Path

PASTAS = [Path("core"), Path(".")]
TERMOS = ("roi", "visagis", "tricolog", "retorno", "c2", "math", "biogem", "motor")


def listar_arquivos() -> list[Path]:
    encontrados: dict[str, Path] = {}
    for pasta in PASTAS:
        if not pasta.exists():
            continue
        for arq in sorted(pasta.glob("*.py")):
            nome = arq.name.lower()
            if any(t in nome for t in TERMOS):
                encontrados[str(arq).lower()] = arq
    return list(encontrados.values())


def inspecionar(arq: Path) -> None:
    try:
        arvore = ast.parse(arq.read_text(encoding="utf-8"), filename=str(arq))
    except Exception as exc:
        print(f"[ERRO PARSE] {arq}: {exc}")
        return

    classes = [n.name for n in ast.walk(arvore) if isinstance(n, ast.ClassDef)]
    funcoes = [n.name for n in arvore.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    self_attrs = sorted({
        nd.attr
        for nd in ast.walk(arvore)
        if isinstance(nd, ast.Attribute) and isinstance(nd.value, ast.Name) and nd.value.id == "self"
    })

    print(f"\n=== {arq} ===")
    print(f"  Classes : {classes or 'nenhuma'}")
    print(f"  Funções : {funcoes[:10]}{' ...' if len(funcoes) > 10 else ''}")
    print(f"  self.*  : {self_attrs[:15]}{' ...' if len(self_attrs) > 15 else ''}")


def main() -> None:
    arquivos = listar_arquivos()
    print(f"Arquivos encontrados ({len(arquivos)}):")
    for a in arquivos:
        print(f"  - {a}")
    for a in arquivos:
        inspecionar(a)


if __name__ == "__main__":
    main()