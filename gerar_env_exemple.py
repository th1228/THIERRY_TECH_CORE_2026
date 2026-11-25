from pathlib import Path


def criar_env_example_automatico(caminho_projeto: str = "."):
    raiz = Path(caminho_projeto).resolve()
    origem = raiz / ".env"
    destino = raiz / ".env.example"

    if not origem.exists():
        print("Nenhum arquivo .env encontrado na raiz do projeto.")
        return

    conteudo = origem.read_text(encoding="utf-8", errors="ignore")
    destino.write_text(conteudo, encoding="utf-8")
    print(f".env.example criado automaticamente a partir de .env em: {destino}")


if __name__ == "__main__":
    criar_env_example_automatico(".")