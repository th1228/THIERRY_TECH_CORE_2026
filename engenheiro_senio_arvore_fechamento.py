import ast
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Habilita sequencias ANSI no terminal Windows (PowerShell / CMD / VS Code)
if os.name == "nt":
    os.system("")

COR_RESET = "\033[0m"
COR_VERDE = "\033[92m"
COR_AMARELO = "\033[93m"
COR_NEGRITO = "\033[1m"


def _colorir(texto: str, cor: str) -> str:
    if not sys.stdout.isatty() and os.name != "nt":
        return texto
    return f"{cor}{texto}{COR_RESET}"


PASTAS_IGNORADAS = {
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".git",
    ".vscode",
    ".idea",
    "node_modules",
    "build",
    "dist",
    ".pytest_cache",
    ".mypy_cache",
}

# Pilares especificos avaliados antes de "Nucleo & Memoria" para nao capturar pastas "core"
PILARES_ARQUITETURA = {
    "Tricologia & Saude": [
        "tricologia_saude",
        "tricolog",
        "capilar",
        "saude",
        "estetica",
        "protocolo",
        "longevidade",
    ],
    "Biometria & Visao 3D": [
        "biometr",
        "visao",
        "vision",
        "monaco",
        "3d",
        "face",
        "mesh",
        "osteometr",
        "mediapipe",
        "opencv",
        "rppg",
    ],
    "Biogemeos & IA": [
        "biogemeo",
        "neuro",
        "predit",
        "solver",
        "sovereign",
        "inteligencia",
        "ia",
        "gemini",
        "gravidade",
    ],
    "Seguranca & Soberania": [
        "seguranca",
        "security",
        "soberania",
        "soerania",
        "blindagem",
        "cripto",
        "crypt",
        "ledger",
        "cofre",
        "auth",
    ],
    "Relatorios & Auditoria": [
        "laudo",
        "pdf",
        "report",
        "auditor",
        "auditoria",
        "juridic",
        "conformidade",
        "inpi",
        "parecer",
        "relatorio",
    ],
    "Comercial & Vendas": [
        "venda",
        "sentinela",
        "stripe",
        "comercial",
        "licenca",
        "plano",
        "mercado",
        "checkout",
    ],
    "Nucleo & Memoria": [
        "memoria",
        "core",
        "hub",
        "main",
        "app",
        "server",
        "api",
        "engine",
        "orquestr",
    ],
}

ORDEM_EXIBICAO_PILARES = [
    "Nucleo & Memoria",
    "Biometria & Visao 3D",
    "Biogemeos & IA",
    "Tricologia & Saude",
    "Seguranca & Soberania",
    "Relatorios & Auditoria",
    "Comercial & Vendas",
    "Utilidades & Testes",
]

LIBS_REAIS_RELEVANTES = {
    "cv2",
    "mediapipe",
    "numpy",
    "scipy",
    "pandas",
    "fastapi",
    "uvicorn",
    "reportlab",
    "fitz",
    "pymupdf",
    "cryptography",
    "hashlib",
    "hmac",
    "sqlite3",
    "sqlalchemy",
    "requests",
    "httpx",
    "stripe",
    "google",
    "PIL",
    "skimage",
}


def deve_ignorar(caminho: Path) -> bool:
    if any(parte in PASTAS_IGNORADAS for parte in caminho.parts):
        return True
    if caminho.name.startswith("tempCodeRunnerFile"):
        return True
    return False


def classificar_pilar(caminho_relativo: str) -> str:
    nome_lower = caminho_relativo.replace("\\", "/").lower()
    nome_arq = Path(nome_lower).name

    if nome_arq.startswith("test_") and any(
        k in nome_arq
        for k in ("relator", "auditor", "laudo", "pdf", "report", "parecer")
    ):
        return "Relatorios & Auditoria"

    if nome_arq.startswith("test_") and any(
        k in nome_arq
        for k in ("comercial", "venda", "stripe", "sentinela", "licenca", "plano", "checkout")
    ):
        return "Comercial & Vendas"

    for pilar, palavras in PILARES_ARQUITETURA.items():
        if any(p in nome_lower for p in palavras):
            return pilar

    return "Utilidades & Testes"


def analisar_arquivo_python(arquivo: Path, raiz: Path) -> dict:
    rel = str(arquivo.relative_to(raiz))
    pilar = classificar_pilar(rel)
    nome_arq_lower = arquivo.name.lower()
    rel_lower = rel.replace("\\", "/").lower()
    eh_teste = (
        nome_arq_lower.startswith("test_")
        or "test" in nome_arq_lower
        or "teste" in rel_lower
    )

    info = {
        "arquivo": rel,
        "pilar": pilar,
        "linhas": 0,
        "erro_sintaxe": None,
        "stubs": [],
        "libs_reais": [],
        "eh_teste": eh_teste,
    }

    try:
        conteudo = arquivo.read_text(encoding="utf-8", errors="replace")
        info["linhas"] = len(conteudo.splitlines())
        arvore = ast.parse(conteudo, filename=rel)
    except SyntaxError as e:
        info["erro_sintaxe"] = f"Linha {e.lineno}: {e.msg}"
        return info
    except Exception as e:
        info["erro_sintaxe"] = str(e)
        return info

    imports_encontrados = set()

    for node in ast.walk(arvore):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            corpo = [
                n
                for n in node.body
                if not (
                    isinstance(n, ast.Expr)
                    and isinstance(getattr(n, "value", None), ast.Constant)
                    and isinstance(n.value.value, str)
                )
            ]
            if not corpo:
                info["stubs"].append(f"{node.name} (L{node.lineno}: vazio)")
            elif len(corpo) == 1:
                unico = corpo[0]
                if isinstance(unico, ast.Pass):
                    info["stubs"].append(f"{node.name} (L{node.lineno}: pass)")
                elif isinstance(unico, ast.Raise):
                    exc_nome = ""
                    if isinstance(unico.exc, ast.Call) and isinstance(unico.exc.func, ast.Name):
                        exc_nome = unico.exc.func.id
                    elif isinstance(unico.exc, ast.Name):
                        exc_nome = unico.exc.id
                    if exc_nome == "NotImplementedError":
                        info["stubs"].append(
                            f"{node.name} (L{node.lineno}: NotImplementedError)"
                        )

        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports_encontrados.add(alias.name.split(".")[0])

        elif isinstance(node, ast.ImportFrom) and node.module:
            imports_encontrados.add(node.module.split(".")[0])

    info["libs_reais"] = sorted(imports_encontrados.intersection(LIBS_REAIS_RELEVANTES))
    return info


def avaliar_pilar(dados: dict) -> dict:
    if dados["arquivos"] == 0:
        return {
            "nota": 0.0,
            "situacao": "NAO INICIADO",
            "o_que_falta": "Criar modulos do pilar",
        }

    nota = 10.0
    faltas = []

    if dados["erros_sintaxe"] > 0:
        nota -= dados["erros_sintaxe"] * 3.0
        faltas.append(f"{dados['erros_sintaxe']} erro(s) sintaxe")

    if dados["stubs"] > 0:
        nota -= dados["stubs"] * 1.0
        faltas.append(f"{dados['stubs']} stub(s)/vazio(s)")

    if dados["com_libs_reais"] == 0:
        nota -= 1.5
        faltas.append("sem libs reais")

    if dados["arquivos_teste"] == 0:
        nota -= 0.5
        faltas.append("sem teste")

    nota = round(max(0.0, min(10.0, nota)), 1)

    if nota == 10.0 and dados["stubs"] == 0 and dados["erros_sintaxe"] == 0:
        situacao = "CONCLUIDO"
        resumo_falta = "Nada pendente"
    elif dados["erros_sintaxe"] > 0:
        situacao = "ERRO SINTAXE"
        resumo_falta = ", ".join(faltas)
    elif nota >= 8.0:
        situacao = "QUASE PRONTO"
        resumo_falta = ", ".join(faltas)
    else:
        situacao = "EM ANDAMENTO"
        resumo_falta = ", ".join(faltas)

    return {
        "nota": nota,
        "situacao": situacao,
        "o_que_falta": resumo_falta,
    }


def gerar_arvore_visual(raiz: Path) -> list[str]:
    linhas = [
        f"ARVORE DO PROJETO: {raiz.name}",
        f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 76,
        "",
    ]

    for dirpath, dirnames, filenames in os.walk(raiz):
        dirnames[:] = sorted(d for d in dirnames if d not in PASTAS_IGNORADAS)
        caminho_atual = Path(dirpath)
        if deve_ignorar(caminho_atual.relative_to(raiz)) and caminho_atual != raiz:
            continue

        nivel = len(caminho_atual.relative_to(raiz).parts)
        indent = "    " * nivel
        nome_pasta = raiz.name if caminho_atual == raiz else caminho_atual.name
        linhas.append(f"{indent}[DIR] {nome_pasta}/")

        arquivos_validos = sorted(
            f
            for f in filenames
            if not f.endswith(".pyc")
            and not f.startswith("tempCodeRunnerFile")
            and f not in {"ARVORE_ESTRUTURAL_PROJETO.txt"}
        )
        for arq in arquivos_validos:
            linhas.append(f"{indent}    |-- {arq}")

    return linhas


def imprimir_tabela_pilares(pilares_dict: dict):
    col_pilar = 24
    col_arqs = 6
    col_linhas = 8
    col_nota = 8
    col_sit = 14
    col_falta = 32

    linha_sep = (
        f"+{'-' * (col_pilar + 2)}"
        f"+{'-' * (col_arqs + 2)}"
        f"+{'-' * (col_linhas + 2)}"
        f"+{'-' * (col_nota + 2)}"
        f"+{'-' * (col_sit + 2)}"
        f"+{'-' * (col_falta + 2)}+"
    )

    cabecalho = (
        f"| {'PILAR':<{col_pilar}} "
        f"| {'ARQS':>{col_arqs}} "
        f"| {'LINHAS':>{col_linhas}} "
        f"| {'NOTA':>{col_nota}} "
        f"| {'SITUACAO':<{col_sit}} "
        f"| {'O QUE FALTA':<{col_falta}} |"
    )

    print(linha_sep)
    print(cabecalho)
    print(linha_sep)

    for nome_pilar in ORDEM_EXIBICAO_PILARES:
        if nome_pilar not in pilares_dict:
            continue
        dados = pilares_dict[nome_pilar]
        ok = dados["status_conclusao"] == "CONCLUIDO"
        cor_linha = COR_VERDE if ok else COR_AMARELO

        nota_str = f"{dados['nota_1_a_10']:.1f}/10"
        pilar_fmt = _colorir(f"{nome_pilar[:col_pilar]:<{col_pilar}}", cor_linha)
        arqs_fmt = _colorir(f"{dados['arquivos']:>{col_arqs}}", cor_linha)
        linhas_fmt = _colorir(f"{dados['linhas']:>{col_linhas}}", cor_linha)
        nota_fmt = _colorir(f"{nota_str:>{col_nota}}", cor_linha)
        sit_fmt = _colorir(f"{dados['status_conclusao'][:col_sit]:<{col_sit}}", cor_linha)
        falta_fmt = _colorir(f"{dados['o_que_falta'][:col_falta]:<{col_falta}}", cor_linha)

        print(
            f"| {pilar_fmt} "
            f"| {arqs_fmt} "
            f"| {linhas_fmt} "
            f"| {nota_fmt} "
            f"| {sit_fmt} "
            f"| {falta_fmt} |"
        )

    print(linha_sep)


def executar_diagnostico(raiz: Path) -> dict:
    linhas_arvore = gerar_arvore_visual(raiz)
    arquivo_arvore = raiz / "ARVORE_ESTRUTURAL_PROJETO.txt"
    arquivo_arvore.write_text("\n".join(linhas_arvore), encoding="utf-8")

    arquivos_py = sorted(
        p for p in raiz.rglob("*.py") if not deve_ignorar(p.relative_to(raiz))
    )
    resultados = [analisar_arquivo_python(p, raiz) for p in arquivos_py]

    pilares_resumo = {
        p: {
            "arquivos": 0,
            "linhas": 0,
            "com_libs_reais": 0,
            "arquivos_teste": 0,
            "stubs": 0,
            "erros_sintaxe": 0,
        }
        for p in ORDEM_EXIBICAO_PILARES
    }

    erros_sintaxe = []
    todos_stubs = []

    for r in resultados:
        p = r["pilar"]
        if p not in pilares_resumo:
            p = "Utilidades & Testes"
        pilares_resumo[p]["arquivos"] += 1
        pilares_resumo[p]["linhas"] += r["linhas"]
        if r["libs_reais"]:
            pilares_resumo[p]["com_libs_reais"] += 1
        if r["eh_teste"]:
            pilares_resumo[p]["arquivos_teste"] += 1
        pilares_resumo[p]["stubs"] += len(r["stubs"])
        if r["erro_sintaxe"]:
            pilares_resumo[p]["erros_sintaxe"] += 1
            erros_sintaxe.append({"arquivo": r["arquivo"], "erro": r["erro_sintaxe"]})
        for s in r["stubs"]:
            todos_stubs.append({"arquivo": r["arquivo"], "pilar": p, "detalhe": s})

    concluidos = 0
    notas = []

    for p in ORDEM_EXIBICAO_PILARES:
        dados = pilares_resumo[p]
        avaliacao = avaliar_pilar(dados)
        dados["nota_1_a_10"] = avaliacao["nota"]
        dados["status_conclusao"] = avaliacao["situacao"]
        dados["o_que_falta"] = avaliacao["o_que_falta"]
        notas.append(avaliacao["nota"])
        if avaliacao["situacao"] == "CONCLUIDO":
            concluidos += 1

    print("\n" + "=" * 102)
    print("DIAGNOSTICO DO PROJETO — ARVORE, NOTAS (1 A 10) E FECHAMENTO")
    print("=" * 102)
    print(f"Arvore salva em : {arquivo_arvore.name}")
    print(f"Arquivos .py    : {len(resultados)} | Linhas totais: {sum(r['linhas'] for r in resultados)}")
    print()

    imprimir_tabela_pilares(pilares_resumo)

    nota_media = round(sum(notas) / len(notas), 1) if notas else 0.0
    pronto = len(erros_sintaxe) == 0 and len(todos_stubs) == 0
    veredicto = (
        "PRONTO PARA ENCERRAR SEM PENDENCIAS"
        if pronto
        else "FECHAR STUBS / SINTAXE LISTADOS ABAIXO PARA ENCERRAR"
    )
    cor_veredicto = COR_VERDE if (pronto and concluidos == len(pilares_resumo)) else COR_AMARELO
    media_str = f"{nota_media:.1f}/10"
    concluidos_str = f"{concluidos}/{len(pilares_resumo)}"

    print(
        f"\nMedia geral: {_colorir(media_str, cor_veredicto)}"
        f" | Concluidos (10/10): {_colorir(concluidos_str, cor_veredicto)}"
    )
    print(f"Conclusao  : {_colorir(veredicto, cor_veredicto)}")

    if erros_sintaxe or todos_stubs:
        print("\nITENS PARA FECHAR:")
        for e in erros_sintaxe:
            print(_colorir(f"  - [SINTAXE] {e['arquivo']} -> {e['erro']}", COR_AMARELO))
        for s in todos_stubs:
            print(_colorir(f"  - [STUB]    {s['arquivo']} ({s['pilar']}) -> {s['detalhe']}", COR_AMARELO))

    relatorio_json = {
        "gerado_em": datetime.now().isoformat(),
        "raiz": str(raiz),
        "total_arquivos_py": len(resultados),
        "total_linhas": sum(r["linhas"] for r in resultados),
        "nota_media_1_a_10": nota_media,
        "pilares_concluidos": f"{concluidos}/{len(pilares_resumo)}",
        "conclusao": veredicto,
        "pilares": pilares_resumo,
        "erros_sintaxe": erros_sintaxe,
        "pendencias_stubs": todos_stubs,
    }

    arquivo_parecer = raiz / "PARECER_ENGENHARIA_SENIOR.json"
    arquivo_parecer.write_text(
        json.dumps(relatorio_json, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"JSON salvo em   : {arquivo_parecer.name}")
    return relatorio_json


def terminal_embutido(raiz: Path, ultimo_parecer: dict):
    print("\n" + "-" * 102)
    print("TERMINAL EMBUTIDO | Comandos: tabela | pendencias | arvore | reanalisar | sair")
    print("-" * 102)

    while True:
        try:
            cmd = input("\nfechamento> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrado.")
            break

        if not cmd:
            continue

        c = cmd.lower()
        if c in {"sair", "exit", "quit", "0"}:
            print("Saindo.")
            break
        elif c == "tabela":
            imprimir_tabela_pilares(ultimo_parecer["pilares"])
        elif c == "pendencias":
            print(
                f"Sintaxe: {len(ultimo_parecer['erros_sintaxe'])} | "
                f"Stubs: {len(ultimo_parecer['pendencias_stubs'])}"
            )
            for e in ultimo_parecer["erros_sintaxe"]:
                print(_colorir(f"  - [SINTAXE] {e['arquivo']} -> {e['erro']}", COR_AMARELO))
            for s in ultimo_parecer["pendencias_stubs"]:
                print(_colorir(f"  - [STUB]    {s['arquivo']} -> {s['detalhe']}", COR_AMARELO))
        elif c == "arvore":
            arq_arv = raiz / "ARVORE_ESTRUTURAL_PROJETO.txt"
            print(arq_arv.read_text(encoding="utf-8") if arq_arv.exists() else "Sem arvore.")
        elif c == "reanalisar":
            ultimo_parecer = executar_diagnostico(raiz)
        else:
            subprocess.run(cmd, shell=True, cwd=str(raiz))


if __name__ == "__main__":
    raiz_projeto = Path.cwd()
    parecer = executar_diagnostico(raiz_projeto)
    terminal_embutido(raiz_projeto, parecer)