import hashlib
import json
import os
import re
from pathlib import Path

IGNORAR_PASTAS = {
    ".git", "__pycache__", ".venv", "venv", "env",
    "node_modules", ".next", "dist", "build", ".idea", ".vscode"
}

ARQUIVO_INTEGRIDADE = ".auditoria_integridade.json"

EXTENSOES_TEXTO = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css",
    ".json", ".yaml", ".yml", ".toml", ".md", ".txt", ".env", ".sql"
}


def calcular_sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def verificar_integridade(raiz: Path, arquivos_info: list):
    caminho_snapshot = raiz / ARQUIVO_INTEGRIDADE
    atual_mapa = {}

    for arq in arquivos_info:
        rel = str(arq.get("caminho", ""))
        if rel == ARQUIVO_INTEGRIDADE:
            continue
        caminho_fisico = raiz / rel
        if caminho_fisico.exists() and caminho_fisico.is_file():
            try:
                atual_mapa[rel] = calcular_sha256(caminho_fisico)
            except Exception:
                pass

    if not caminho_snapshot.exists():
        caminho_snapshot.write_text(
            json.dumps({"arquivos": atual_mapa}, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        return (
            "BASE CRIADA (Primeiro registro de integridade salvo; próximas execuções compararão alterações)."
        )

    try:
        anterior_dados = json.loads(caminho_snapshot.read_text(encoding="utf-8"))
        anterior_mapa = anterior_dados.get("arquivos", {})
    except Exception:
        anterior_mapa = {}

    alterados = []
    novos = []
    removidos = []

    for rel, hash_atual in atual_mapa.items():
        if rel not in anterior_mapa:
            novos.append(rel)
        elif anterior_mapa[rel] != hash_atual:
            alterados.append(rel)

    for rel in anterior_mapa:
        if rel not in atual_mapa:
            removidos.append(rel)

    # Atualiza o snapshot para a próxima rodada
    caminho_snapshot.write_text(
        json.dumps({"arquivos": atual_mapa}, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    if not alterados and not novos and not removidos:
        return "ÍNTEGRO (Nenhuma alteração detectada nos arquivos desde a última auditoria)."

    partes = []
    if alterados:
        partes.append(f"{len(alterados)} alterado(s) [{', '.join(alterados[:3])}]")
    if novos:
        partes.append(f"{len(novos)} novo(s) [{', '.join(novos[:3])}]")
    if removidos:
        partes.append(f"{len(removidos)} removido(s) [{', '.join(removidos[:3])}]")

    return "ALTERADO / NÃO ÍNTEGRO -> " + " | ".join(partes)


def varrer_sistema(raiz: Path):
    arquivos = []
    pastas = set()
    extensoes = {}
    conteudo_amostra = []
    total_linhas_codigo = 0

    for atual, dirs, files in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in IGNORAR_PASTAS]
        caminho_atual = Path(atual)

        for d in dirs:
            pastas.add(str((caminho_atual / d).relative_to(raiz)).lower())

        for f in files:
            caminho_arq = caminho_atual / f
            rel = str(caminho_arq.relative_to(raiz))
            ext = caminho_arq.suffix.lower()
            extensoes[ext] = extensoes.get(ext, 0) + 1

            linhas = 0
            texto = ""
            if ext in EXTENSOES_TEXTO:
                try:
                    texto = caminho_arq.read_text(encoding="utf-8", errors="ignore")
                    linhas = len(texto.splitlines())
                except Exception:
                    pass

            if ext in {".py", ".js", ".ts", ".jsx", ".tsx"}:
                total_linhas_codigo += linhas

            arquivos.append({
                "caminho": rel,
                "nome": f.lower(),
                "ext": ext,
                "linhas": linhas,
                "texto": texto
            })

            if len(" ".join(conteudo_amostra)) < 60000 and texto:
                conteudo_amostra.append(f"--- {rel} ---\n{texto[:2500]}")

    return {
        "arquivos": arquivos,
        "pastas": pastas,
        "extensoes": extensoes,
        "total_linhas_codigo": total_linhas_codigo,
        "amostra": "\n".join(conteudo_amostra)
    }


def identificar_categoria_e_funcao(dados: dict, raiz: Path):
    texto_geral = str(dados.get("amostra", "")).lower()
    nomes_arq = " ".join(str(a.get("nome", "")) for a in dados.get("arquivos", []))
    pastas_str = " ".join(str(p) for p in dados.get("pastas", []))

    scores_cat = {
        "API / Backend Web": 0,
        "Aplicação Web / Frontend": 0,
        "Visão Computacional / IA / Dados": 0,
        "Automação / Script / CLI": 0,
        "Sistema / Aplicação Completa": 0,
    }

    if any(k in texto_geral for k in ["fastapi", "flask", "django", "express", "router", "endpoint", "@app.get", "@app.post"]):
        scores_cat["API / Backend Web"] += 3
    if any(k in texto_geral for k in ["react", "next", "vite", "tailwind", "component", "usestate", "<div", "<html"]):
        scores_cat["Aplicação Web / Frontend"] += 3
    if any(k in texto_geral for k in ["cv2", "mediapipe", "numpy", "pandas", "torch", "tensorflow", "sklearn", "landmark", "ppg"]):
        scores_cat["Visão Computacional / IA / Dados"] += 3
    if any(k in texto_geral for k in ["argparse", "click", "typer", "subprocess", "schedule", "pyautogui", "os.walk"]):
        scores_cat["Automação / Script / CLI"] += 2
    if len(dados.get("pastas", [])) >= 4 and int(dados.get("total_linhas_codigo", 0)) > 800:
        scores_cat["Sistema / Aplicação Completa"] += 2

    categoria = "Programa / Script Geral"
    maior_pontuacao = 0
    for cat_nome, pontos in scores_cat.items():
        if pontos > maior_pontuacao:
            maior_pontuacao = pontos
            categoria = cat_nome

    descricao = "Finalidade não declarada explicitamente em README ou cabeçalho."
    for a in dados.get("arquivos", []):
        if a.get("nome") in {"readme.md", "readme.txt"} and str(a.get("texto", "")).strip():
            linhas_limpas = [
                ln.strip("# ").strip()
                for ln in str(a.get("texto", "")).splitlines()
                if ln.strip() and not ln.strip().startswith("```")
            ]
            if linhas_limpas:
                descricao = " ".join(linhas_limpas[:3])[:220]
                break
    else:
        for a in dados.get("arquivos", []):
            texto_arq = str(a.get("texto", "")).strip()
            if a.get("ext") == ".py" and texto_arq.startswith(('"""', "'''")):
                doc = re.split(r'"""|\'\'\'', texto_arq[3:])[0].strip()
                if doc:
                    descricao = " ".join(doc.splitlines())[:220]
                    break

    pistas = []
    for termo, rotulo in [
        ("auth", "autenticação/segurança"),
        ("database", "banco de dados"),
        ("sql", "consultas SQL"),
        ("api", "integração via API"),
        ("test", "testes automatizados"),
        ("config", "configurações"),
    ]:
        if termo in nomes_arq or termo in pastas_str:
            pistas.append(rotulo)

    return categoria, descricao, pistas


def auditar_para_categoria(categoria: str, dados: dict, raiz: Path):
    nota = 100
    achados = []

    def penalizar(pontos: int, motivo: str):
        nonlocal nota
        nota -= pontos
        achados.append(f"[-{pontos}] {motivo}")

    arquivos = dados.get("arquivos", [])
    pastas = dados.get("pastas", set())

    tem_readme = any(a.get("nome") in {"readme.md", "readme.txt"} for a in arquivos)
    if not tem_readme:
        penalizar(12, "Sem README.md explicando objetivo, instalação e execução.")

    tem_env_example = any(
        any(padrao in str(a.get("nome", "")) for padrao in (".env.example", "env.example", ".env.sample", "env.sample"))
        for a in arquivos
    )
    usa_env = any(
        "os.getenv" in str(a.get("texto", ""))
        or "process.env" in str(a.get("texto", ""))
        or "dotenv" in str(a.get("texto", ""))
        for a in arquivos
    )
    if usa_env and not tem_env_example:
        penalizar(8, "Usa variáveis de ambiente, mas não possui .env.example.")

    termos_ruins = ("copia", "copy", "_old", "antigo", "backup", "rascunho", ".bak", "teste2", "final2")
    sujos = [str(a.get("caminho", "")) for a in arquivos if any(t in str(a.get("nome", "")) for t in termos_ruins)]
    if sujos:
        penalizar(min(20, len(sujos) * 5), f"Arquivos com indício de cópia/rascunho: {', '.join(sujos[:4])}")

    arquivos_gigantes = [
        a for a in arquivos
        if a.get("ext") in {".py", ".js", ".ts", ".jsx", ".tsx"} and int(a.get("linhas", 0)) > 500
    ]
    if arquivos_gigantes:
        penalizar(
            min(18, len(arquivos_gigantes) * 6),
            "Arquivos muito grandes (>500 linhas): "
            + ", ".join(f"{a.get('caminho')} ({a.get('linhas')}l)" for a in arquivos_gigantes[:3])
        )

    tem_pasta_modulo = any(
        str(p).split("/")[0] in {"src", "app", "core", "modules", "services", "routes", "api", "backend", "frontend"}
        for p in pastas
    )
    tem_testes = any("test" in str(p) for p in pastas) or any("test" in str(a.get("nome", "")) for a in arquivos)

    if categoria in {"API / Backend Web", "Aplicação Web / Frontend", "Sistema / Aplicação Completa"}:
        if not tem_pasta_modulo:
            penalizar(15, f"Para '{categoria}', falta separação modular em pastas (ex.: src/, app/, modules/, routes/).")
        if not tem_testes:
            penalizar(12, f"Para '{categoria}', não foram encontrados testes ou scripts de verificação.")
    elif categoria == "Visão Computacional / IA / Dados":
        if not tem_pasta_modulo:
            penalizar(12, "Para IA/Dados, convém separar pipeline/modelos/processamento em pastas ou módulos.")
        if not tem_testes:
            penalizar(8, "Sem scripts de teste/validação para verificar entradas e saídas do modelo/pipeline.")
    elif categoria == "Automação / Script / CLI":
        if int(dados.get("total_linhas_codigo", 0)) > 350 and not tem_pasta_modulo:
            penalizar(10, "Automação cresceu e já justifica separar funções/configuração em módulos.")

    prints_excessivos = [
        str(a.get("caminho", "")) for a in arquivos
        if a.get("ext") == ".py" and len(re.findall(r"\bprint\s*\(", str(a.get("texto", "")))) > 15
    ]
    if prints_excessivos:
        penalizar(7, f"Muitos print() em: {', '.join(prints_excessivos[:3])} (considere usar logging).")

    nota_final = max(1, min(100, nota))
    return nota_final, achados


def classificar_auditoria(nota: int):
    if nota >= 85:
        return "APROVADO PARA AUDITORIA (Nível alto de organização para a categoria)"
    if nota >= 65:
        return "ATENÇÃO LEVE (Funcional, mas vale ajustar pontos específicos antes de apresentar)"
    if nota >= 40:
        return "AJUSTES NECESSÁRIOS (Organização parcial; pode gerar questionamentos em auditoria)"
    return "CRÍTICO (Requer organização estrutural antes de avaliação ou entrega)"


def main(caminho: str = "."):
    raiz = Path(caminho).resolve()
    dados = varrer_sistema(raiz)
    categoria, descricao, pistas = identificar_categoria_e_funcao(dados, raiz)
    nota, achados = auditar_para_categoria(categoria, dados, raiz)
    veredito = classificar_auditoria(nota)
    integridade = verificar_integridade(raiz, dados.get("arquivos", []))

    print("=" * 60)
    print(f"PROJETO: {raiz.name}")
    print(f"CATEGORIA IDENTIFICADA: {categoria}")
    print(f"O QUE PARECE FAZER: {descricao}")
    if pistas:
        print(f"ÁREAS DETECTADAS: {', '.join(pistas)}")
    print("-" * 60)
    print(f"NOTA DE AUDITORIA: {nota}/100")
    print(f"STATUS: {veredito}")
    print(f"INTEGRIDADE: {integridade}")
    print("-" * 60)
    if achados:
        print("PONTOS PARA MELHORAR:")
        for item in achados:
            print(f"  {item}")
    else:
        print("Nenhum ponto crítico encontrado nas regras atuais.")
    print("=" * 60)


if __name__ == "__main__":
    main(".")