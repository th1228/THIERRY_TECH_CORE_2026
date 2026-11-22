from pathlib import Path
import re
import shutil

RAIZ = Path(".")
EXTENSOES = {".html", ".htm", ".py", ".js", ".css", ".json", ".txt", ".md"}
IGNORAR = {".git", "__pycache__", "node_modules", ".venv", "venv", "_backup_seguro"}

# Alvos exatos para trocar (evita mexer em código ou tags)
TROCAS = {
    "Tecnologia & Visagismo / Intangíveis": "Tecnologia & Visagismo / Intangíveis",
    "": "",
}


def deve_ignorar(caminho: Path) -> bool:
  return any(parte in IGNORAR for parte in caminho.parts)


def limpar_espacos_duplos_na_ocorrencia(texto: str, antigo: str, novo: str) -> str:
  if novo != "":
    return texto.replace(antigo, novo)

  padrao = re.compile(r"[ \t]*" + re.escape(antigo) + r"[ \t]*")

  def substituir(match):
    antes = texto[max(0, match.start() - 1) : match.start()]
    depois = texto[match.end() : min(len(texto), match.end() + 1)]
    if antes in (" ", "\t") and depois in (" ", "\t"):
      return " "
    return ""

  return padrao.sub(substituir, texto)


def main():
  pasta_backup = RAIZ / "_backup_seguro"
  total_arquivos = 0
  total_trocas = 0
  erros = []

  for arquivo in RAIZ.rglob("*"):
    if not arquivo.is_file() or deve_ignorar(arquivo):
      continue
    if arquivo.suffix.lower() not in EXTENSOES:
      continue

    try:
      try:
        original = arquivo.read_text(encoding="utf-8")
        encoding_usado = "utf-8"
      except UnicodeDecodeError:
        original = arquivo.read_text(encoding="latin-1")
        encoding_usado = "latin-1"

      atualizado = original
      trocas_no_arquivo = 0

      for antigo, novo in TROCAS.items():
        padrao_contagem = (
            r"[ \t]*" + re.escape(antigo) + r"[ \t]*"
            if novo == ""
            else re.escape(antigo)
        )
        ocorrencias = len(re.findall(padrao_contagem, atualizado))
        if ocorrencias > 0:
          atualizado = limpar_espacos_duplos_na_ocorrencia(
              atualizado, antigo, novo
          )
          trocas_no_arquivo += ocorrencias

      if atualizado != original:
        destino_bkp = pasta_backup / arquivo.relative_to(RAIZ)
        destino_bkp.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(arquivo, destino_bkp)

        arquivo.write_text(atualizado, encoding=encoding_usado)
        total_arquivos += 1
        total_trocas += trocas_no_arquivo
        print(f"[OK] {arquivo} ({trocas_no_arquivo} alteração(ões))")

    except Exception as exc:
      erros.append((str(arquivo), str(exc)))
      print(f"[ERRO] {arquivo}: {exc}")

  print("\n" + "=" * 45)
  if erros:
    print(f"STATUS: DEU PROBLEMA EM {len(erros)} ARQUIVO(S).")
    for arq, msg in erros:
      print(f"  - {arq}: {msg}")
  elif total_trocas > 0:
    print("STATUS: DEU CERTO!")
    print(f"Alterações feitas: {total_trocas}")
    print(f"Arquivos atualizados: {total_arquivos}")
    print(f"Backup salvo em: {pasta_backup.resolve()}")
  else:
    print("STATUS: NADA ALTERADO (termo não encontrado nos arquivos).")
  print("=" * 45)


if __name__ == "__main__":
  main()