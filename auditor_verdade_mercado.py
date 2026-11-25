import ast
import json
import re
from datetime import datetime
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

TERMOS_SIMULACAO = re.compile(
    r"\b(fallback|simul\w*|mock\w*|fake|dummy|stub|placeholder|estimativ\w*|default_\w*|padrao_\w*)\b",
    re.IGNORECASE,
)

IMPORTS_PROCESSAMENTO_REAL = {
    "cv2",
    "mediapipe",
    "numpy",
    "scipy",
    "pandas",
    "sklearn",
    "torch",
    "tensorflow",
    "onnxruntime",
    "sqlite3",
    "sqlalchemy",
    "psycopg2",
    "pymongo",
    "requests",
    "httpx",
    "aiohttp",
    "fastapi",
    "flask",
    "cryptography",
    "hashlib",
    "hmac",
    "fitz",
    "pymupdf",
    "reportlab",
}

DOMINIOS_MERCADO = {
    "Biometria & Visão Computacional": re.compile(r"(biometr|landmark|rppg|face|visagism|iris|retina)", re.I),
    "Biogêmeos & Modelagem": re.compile(r"(biogemeo|biogêmeo|digital_twin|twin|modelagem)", re.I),
    "Tricologia & Saúde/Estética": re.compile(r"(tricol|capilar|telemed|saude|saúde|clinica|clínica)", re.I),
    "Segurança, Criptografia & C2": re.compile(r"(c2|sovereign|vault|zero_trust|crypto|sha256|security|blindag)", re.I),
    "Conformidade Regulatória": re.compile(r"(lgpd|gdpr|hipaa|ccpa|regulament|conformidade|jurisdic)", re.I),
    "Comercialização & Licenciamento": re.compile(r"(licenc|stripe|lemon|contrato|uhnw|private|venda|retorno)", re.I),
}


def listar_arquivos_py() -> list[Path]:
    arquivos = []
    for p in RAIZ.rglob("*.py"):
        if any(parte in IGNORAR_DIRS for parte in p.parts):
            continue
        if p.name.endswith(".bak"):
            continue
        arquivos.append(p)
    return sorted(arquivos)


def analisar_python(caminho: Path) -> dict:
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    linhas = texto.splitlines()
    resultado = {
        "arquivo": str(caminho),
        "linhas": len(linhas),
        "erro_sintaxe": None,
        "funcoes": 0,
        "classes": 0,
        "stubs_ou_pass": 0,
        "imports_reais": [],
        "ocorrencias_simulacao": len(TERMOS_SIMULACAO.findall(texto)),
        "dominios": [],
        "eh_teste": "test" in caminho.name.lower() or "tests" in [x.lower() for x in caminho.parts],
    }

    for nome_dom, rx in DOMINIOS_MERCADO.items():
        if rx.search(caminho.name) or rx.search(texto[:8000]):
            resultado["dominios"].append(nome_dom)

    try:
        arvore = ast.parse(texto, filename=str(caminho))
    except SyntaxError as exc:
        resultado["erro_sintaxe"] = f"Linha {exc.lineno}: {exc.msg}"
        return resultado

    imports_encontrados = set()
    for node in ast.walk(arvore):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            resultado["funcoes"] += 1
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                resultado["stubs_ou_pass"] += 1
        elif isinstance(node, ast.ClassDef):
            resultado["classes"] += 1
        elif isinstance(node, ast.Raise):
            if isinstance(node.exc, ast.Call) and getattr(node.exc.func, "id", "") == "NotImplementedError":
                resultado["stubs_ou_pass"] += 1
            elif getattr(node.exc, "id", "") == "NotImplementedError":
                resultado["stubs_ou_pass"] += 1
        elif isinstance(node, ast.Import):
            for alias in node.names:
                raiz_imp = alias.name.split(".")[0]
                if raiz_imp in IMPORTS_PROCESSAMENTO_REAL:
                    imports_encontrados.add(raiz_imp)
        elif isinstance(node, ast.ImportFrom) and node.module:
            raiz_imp = node.module.split(".")[0]
            if raiz_imp in IMPORTS_PROCESSAMENTO_REAL:
                imports_encontrados.add(raiz_imp)

    resultado["imports_reais"] = sorted(imports_encontrados)
    return resultado


def inspecionar_pdfs() -> dict:
    pdfs = sorted(RAIZ.glob("pdfs_finais/*.pdf"))
    detalhes = []
    total_palavras = 0
    try:
        import pymupdf as fitz  # type: ignore
    except ImportError:
        try:
            import fitz  # type: ignore
        except ImportError:
            fitz = None

    for pdf in pdfs:
        palavras = 0
        paginas = 0
        if fitz is not None:
            doc = fitz.open(pdf)
            paginas = len(doc)
            palavras = sum(len(pg.get_text("text").split()) for pg in doc)
            doc.close()
        total_palavras += palavras
        detalhes.append({"arquivo": str(pdf), "paginas": paginas, "palavras": palavras})

    return {"quantidade": len(pdfs), "total_palavras": total_palavras, "arquivos": detalhes}


def main() -> None:
    arquivos_py = listar_arquivos_py()
    analises = [analisar_python(p) for p in arquivos_py]
    pdfs_info = inspecionar_pdfs()

    total_py = len(analises)
    total_linhas = sum(a["linhas"] for a in analises)
    erros_sintaxe = [a for a in analises if a["erro_sintaxe"]]
    modulos_com_motor_real = [a for a in analises if a["imports_reais"] and not a["eh_teste"]]
    modulos_teste = [a for a in analises if a["eh_teste"]]
    modulos_alta_simulacao = sorted(
        [a for a in analises if a["ocorrencias_simulacao"] >= 5],
        key=lambda x: x["ocorrencias_simulacao"],
        reverse=True,
    )
    total_stubs = sum(a["stubs_ou_pass"] for a in analises)

    cobertura_dominios = {}
    for dom in DOMINIOS_MERCADO:
        mods = [a for a in analises if dom in a["dominios"] and not a["eh_teste"]]
        mods_reais = [a for a in mods if a["imports_reais"]]
        cobertura_dominios[dom] = {
            "total_modulos": len(mods),
            "com_processamento_real": len(mods_reais),
            "exemplos": [m["arquivo"] for m in mods_reais[:3]],
        }

    # Parecer técnico independente
    pendencias_tecnicas = []
    if erros_sintaxe:
        pendencias_tecnicas.append(f"{len(erros_sintaxe)} arquivo(s) com erro de sintaxe.")
    if len(modulos_alta_simulacao) > 20:
        pendencias_tecnicas.append(
            f"{len(modulos_alta_simulacao)} módulos têm 5+ ocorrências de fallback/simulação/estimativa — exigir separação clara entre dado real e contingência."
        )
    if len(modulos_teste) < 5:
        pendencias_tecnicas.append(
            f"Apenas {len(modulos_teste)} arquivo(s) de teste automatizado detectado(s) para {total_py} módulos."
        )
    if total_stubs > 0:
        pendencias_tecnicas.append(f"{total_stubs} função(ões) vazia(s) ou NotImplementedError encontrada(s).")

    pendencias_mercado = [
        "Evidência externa: código e PDFs no disco não substituem validação com clientes reais (piloto pago, métricas de antes/depois, taxa de retenção).",
        "Rastreabilidade ponta a ponta: cada promessa nos dossiês (biometria, biogêmeos, tricologia, conformidade) precisa de caso de teste reproduzível com entrada real e saída auditável.",
    ]

    veredicto = (
        "APROVADO EM ESTRUTURA E MOTOR BASE, COM RESSALVAS PARA VALIDAÇÃO DE PRODUÇÃO E MERCADO"
        if not erros_sintaxe and len(modulos_com_motor_real) >= 10
        else "NECESSITA CORREÇÃO ESTRUTURAL ANTES DE AVALIAÇÃO DE MERCADO"
    )

    relatorio = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "veredicto_independente": veredicto,
        "resumo_codigo": {
            "arquivos_py": total_py,
            "linhas_totais": total_linhas,
            "erros_sintaxe": len(erros_sintaxe),
            "modulos_com_bibliotecas_reais": len(modulos_com_motor_real),
            "arquivos_de_teste": len(modulos_teste),
            "funcoes_stub_ou_pass": total_stubs,
            "modulos_com_5_ou_mais_termos_simulacao_fallback": len(modulos_alta_simulacao),
        },
        "top_10_simulacao_fallback": [
            {"arquivo": m["arquivo"], "ocorrencias": m["ocorrencias_simulacao"], "imports_reais": m["imports_reais"]}
            for m in modulos_alta_simulacao[:10]
        ],
        "aderencia_dominios_mercado": cobertura_dominios,
        "dossies_pdf": pdfs_info,
        "pendencias_verdade_tecnica": pendencias_tecnicas,
        "pendencias_dor_de_mercado": pendencias_mercado,
    }

    Path("parecer_avalista_mercado.json").write_text(
        json.dumps(relatorio, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print("=" * 78)
    print("PARECER INDEPENDENTE DE VERDADE TÉCNICA E ADERÊNCIA DE MERCADO")
    print("=" * 78)
    print(f"Data/Hora                : {relatorio['timestamp']}")
    print(f"Veredicto                : {veredicto}")
    print("-" * 78)
    print("[1] VERDADE TÉCNICA DO CÓDIGO")
    print(f"  Arquivos .py / Linhas  : {total_py} arquivos | {total_linhas} linhas")
    print(f"  Erros de sintaxe AST   : {len(erros_sintaxe)}")
    print(f"  Motores com libs reais : {len(modulos_com_motor_real)} módulos (visão, dados, crypto, API, PDF)")
    print(f"  Arquivos de teste      : {len(modulos_teste)}")
    print(f"  Stubs / pass vazios    : {total_stubs}")
    print(f"  Módulos >=5 fallback/simulação : {len(modulos_alta_simulacao)}")
    print("\n  Top módulos com termos de fallback/simulação/estimativa:")
    for item in relatorio["top_10_simulacao_fallback"][:6]:
        libs = ", ".join(item["imports_reais"]) if item["imports_reais"] else "sem lib externa pesada"
        print(f"   - {item['arquivo']}: {item['ocorrencias']} ocorrências ({libs})")

    print("\n[2] COBERTURA POR FRENTE DE DOR DE MERCADO (CÓDIGO REAL NO DISCO)")
    for dom, info in cobertura_dominios.items():
        print(
            f"  - {dom}: {info['com_processamento_real']}/{info['total_modulos']} módulos com libs de processamento real"
        )

    print(f"\n[3] LASTRO DOCUMENTAL (PDFs): {pdfs_info['quantidade']} PDFs | {pdfs_info['total_palavras']} palavras")
    print("\n[4] O QUE FALTA PARA UM AVALISTA DE MERCADO ASSINAR SEM RESSALVAS")
    for p in pendencias_tecnicas:
        print(f"  [Técnico] {p}")
    for p in pendencias_mercado:
        print(f"  [Mercado] {p}")
    print("\n[OK] Relatório completo salvo em: parecer_avalista_mercado.json")


if __name__ == "__main__":
    main()