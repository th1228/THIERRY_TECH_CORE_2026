import os
from pathlib import Path


def executar_pipeline_mestre(diretorio_raiz):
  print("=" * 65)
  print("🚀 THIERRY TECH CONCEPT GLOBAL - AUDITORIA E CHECKOUT MESTRE")
  print("=" * 65)

  caminho_base = Path(diretorio_raiz)

  if not caminho_base.exists():
    print(f"❌ Erro: O diretório {diretorio_raiz} não foi encontrado.")
    return

  # 1. MAPEAMENTO E CONTAGEM TOTAL (Ignora pastas de sistema)
  todos_arquivos = [
      f
      for f in caminho_base.rglob("*")
      if f.is_file()
      and "__pycache__" not in str(f)
      and ".git" not in str(f)
      and f.name != "acao_mestre.py"  # Ignora o próprio script da contagem
  ]
  total_inicial = len(todos_arquivos)
  print(f"📁 Total de arquivos encontrados inicialmente: {total_inicial}")

  # 2. IDENTIFICAÇÃO E LIMPEZA DE DUPLICADOS
  mapa_nomes = {}
  for arq in todos_arquivos:
    nome = arq.name
    if nome not in mapa_nomes:
      mapa_nomes[nome] = []
    mapa_nomes[nome].append(arq)

  duplicados = {
      nome: lista for nome, lista in mapa_nomes.items() if len(lista) > 1
  }
  removidos = 0

  if duplicados:
    print(
        f"🧹 {sum(len(l) - 1 for l in duplicados.values())} arquivos duplicados"
        " detectados. Removendo cópias antigas..."
    )
    for nome, lista in duplicados.items():
      # Mantém o mais recente com base na data de modificação
      lista_ordenada = sorted(
          lista, key=lambda x: x.stat().st_mtime, reverse=True
      )
      oficial = lista_ordenada[0]
      excedentes = lista_ordenada[1:]

      print(f"   [MANTEVE] {oficial}")
      for exc in excedentes:
        try:
          exc.unlink()
          removidos += 1
          print(f"   [DELETOU CÓPIA] {exc}")
        except Exception as e:
          print(f"   [ERRO AO DELETAR] {exc}: {e}")
  else:
    print("✨ Nenhum arquivo duplicado encontrado. Estrutura limpa.")

  total_final = total_inicial - removidos
  print("-" * 65)
  print(f"📊 Total de arquivos após a limpeza: {total_final}")

  # 3. CHECKOUT DE INTEGRAÇÃO (Verifica se os arquivos vitais existem)
  print("=" * 65)
  print("🔍 EXECUTANDO CHECKOUT DE INTEGRAÇÃO DOS MÓDULOS...")

  essenciais = [
      "main.py",
      "licenca.py",
      "licenca_ativa.json",
  ]

  integracao_ok = True
  for essencial in essenciais:
    encontrado = list(caminho_base.rglob(essencial))
    if encontrado:
      print(f"   [OK] Módulo essencial presente: {essencial}")
    else:
      print(f"   [FALTA] Módulo essencial ausente: {essencial}")
      integracao_ok = False

  print("=" * 65)
  if integracao_ok:
    print("✅ STATUS DO SISTEMA: INTEGRAÇÃO APROVADA E PRONTA PARA ZIPAR.")
  else:
    print("⚠️ STATUS DO SISTEMA: ALGUNS MÓDULOS ESSENCIAIS ESTÃO FALTANDO.")
  print("=" * 65)


if __name__ == "__main__":
  # Pega automaticamente a pasta exata onde este script está rodando (a raiz)
  diretorio_alvo = os.path.dirname(os.path.abspath(__file__))
  executar_pipeline_mestre(diretorio_alvo)