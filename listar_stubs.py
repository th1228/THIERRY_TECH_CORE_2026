import ast
from pathlib import Path

IGNORAR = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "backups",
}


def main() -> None:
    for p in sorted(Path(".").rglob("*.py")):
        if any(parte in IGNORAR for parte in p.parts) or p.name.endswith(".bak"):
            continue
        texto = p.read_text(encoding="utf-8", errors="replace")
        arvore = ast.parse(texto, filename=str(p))
        for n in ast.walk(arvore):
            if (
                isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                and len(n.body) == 1
                and isinstance(n.body[0], ast.Pass)
            ):
                print(f"{p}:{n.lineno} -> {n.name} (pass)")
            elif isinstance(n, ast.Raise) and "NotImplementedError" in ast.dump(n):
                print(f"{p}:{n.lineno} -> <raise NotImplementedError>")


if __name__ == "__main__":
    main()