import ast
import shutil
from pathlib import Path

AJUSTES = [
    (
        Path("core/biogemio_orquestrador.py"),
        "        def __init__(self, limiar_confianca_minimo: float = 100.0, lang: str = \"PT\"):\n            pass",
        "        def __init__(self, limiar_confianca_minimo: float = 100.0, lang: str = \"PT\"):\n            self.limiar_confianca_minimo = limiar_confianca_minimo\n            self.lang = lang",
    ),
    (
        Path("core/dashboard_global.py"),
        "    def gerar_diagnostico_final(*args, **kwargs): pass",
        "    def gerar_diagnostico_final(*args, **kwargs):\n        return {\"status\": \"fallback\", \"origem\": \"dashboard_global\", \"diagnostico\": None}",
    ),
    (
        Path("core/gerenciador_global.py"),
        "    def iniciar_prognostico(): pass",
        "    def iniciar_prognostico():\n        return {\"status\": \"fallback\", \"modulo\": \"prognostico\"}",
    ),
    (
        Path("core/gerenciador_global.py"),
        "    def executar_coleta_inicial(): pass",
        "    def executar_coleta_inicial():\n        return {\"status\": \"fallback\", \"etapa\": \"coleta_inicial\"}",
    ),
]


def main() -> None:
    por_arquivo: dict[Path, list[tuple[str, str]]] = {}
    for caminho, antigo, novo in AJUSTES:
        por_arquivo.setdefault(caminho, []).append((antigo, novo))

    alterados = 0
    for caminho, pares in por_arquivo.items():
        if not caminho.exists():
            print(f"[AVISO] Não encontrado: {caminho}")
            continue
        original = caminho.read_text(encoding="utf-8", errors="replace")
        novo_texto = original
        for antigo, novo in pares:
            if antigo in novo_texto:
                novo_texto = novo_texto.replace(antigo, novo, 1)
            else:
                print(f"[AVISO] Trecho exato não encontrado em {caminho}:\n{antigo}")

        if novo_texto != original:
            ast.parse(novo_texto, filename=str(caminho))
            bak = caminho.with_suffix(caminho.suffix + ".bak")
            shutil.copy2(caminho, bak)
            caminho.write_text(novo_texto, encoding="utf-8")
            alterados += 1
            print(f"[OK] Atualizado (backup em {bak.name}): {caminho}")

    print(f"Arquivos alterados: {alterados}")


if __name__ == "__main__":
    main()