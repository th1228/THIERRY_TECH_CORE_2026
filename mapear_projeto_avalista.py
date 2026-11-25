import ast
import json
from datetime import datetime
from pathlib import Path

PASTAS_IGNORADAS = {
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "testes_temp",
    "sandbox_temp",
    "node_modules",
}

EXTENSOES_TEXTO = {
    ".py",
    ".html",
    ".htm",
    ".js",
    ".css",
    ".json",
    ".md",
    ".txt",
    ".bat",
    ".ps1",
    ".sh",
}

EXTENSOES_BINARIAS_COMUNS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".ico",
    ".pdf",
    ".mp4",
    ".mp3",
    ".exe",
    ".dll",
    ".bin",
    ".zip",
}

PALAVRAS_FALLBACK = (
    "default",
    "padrao",
    "padrão",
    "base",
    "fallback",
    "mock",
    "simula",
    "estimad",
    "placeholder",
)


def gerar_arvore_visual(raiz: Path, prefixo: str = "") -> list[str]:
    entradas = [
        p for p in sorted(raiz.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        if p.name not in PASTAS_IGNORADAS
    ]
    linhas = []
    total = len(entradas)

    for idx, item in enumerate(entradas):
        eh_ultimo = idx == total - 1
        conector = "└── " if eh_ultimo else "├── "
        if item.is_dir():
            linhas.append(f"{prefixo}{conector}{item.name}/")
            extensao = "    " if eh_ultimo else "│   "
            linhas.extend(gerar_arvore_visual(item, prefixo + extensao))
        else:
            tamanho_kb = round(item.stat().st_size / 1024, 1)
            linhas.append(f"{prefixo}{conector}{item.name} ({tamanho_kb} KB)")
    return linhas


def inspecionar_arquivos_python(raiz: Path) -> tuple[list[dict], set[str]]:
    arquivos_py = [
        p for p in sorted(raiz.rglob("*.py"))
        if not any(parte in PASTAS_IGNORADAS for parte in p.parts)
    ]

    detalhes_py = []
    nomes_modulos_internos = {p.stem for p in arquivos_py}
    referencias_encontradas = set()

    arquivos_texto = [
        p for p in raiz.rglob("*")
        if p.is_file()
        and not any(parte in PASTAS_IGNORADAS for parte in p.parts)
        and p.suffix.lower() in EXTENSOES_TEXTO
    ]

    for arq_txt in arquivos_texto:
        try:
            txt = arq_txt.read_text(encoding="utf-8", errors="ignore")
            for nome_mod in nomes_modulos_internos:
                if arq_txt.stem != nome_mod and nome_mod in txt:
                    referencias_encontradas.add(nome_mod)
        except OSError:
            pass

    for caminho in arquivos_py:
        codigo = caminho.read_text(encoding="utf-8", errors="ignore")
        linhas = codigo.splitlines()
        relativo = str(caminho.relative_to(raiz))

        classes = []
        funcoes = []
        imports = []
        erro_ast = None

        try:
            arvore = ast.parse(codigo)
            for no in ast.walk(arvore):
                if isinstance(no, ast.ClassDef):
                    classes.append(no.name)
                elif isinstance(no, ast.FunctionDef):
                    funcoes.append(no.name)
                elif isinstance(no, ast.Import):
                    for alias in no.names:
                        imports.append(alias.name)
                elif isinstance(no, ast.ImportFrom):
                    modulo = no.module or ""
                    imports.append(modulo)
        except SyntaxError as exc:
            erro_ast = f"Linha {exc.lineno}: {exc.msg}"

        ocorrencias_fallback = []
        for num_linha, conteudo_linha in enumerate(linhas, start=1):
            low = conteudo_linha.lower()
            if any(p in low for p in PALAVRAS_FALLBACK):
                ocorrencias_fallback.append({
                    "linha": num_linha,
                    "trecho": conteudo_linha.strip()[:120],
                })

        detalhes_py.append({
            "arquivo": relativo,
            "linhas": len(linhas),
            "erro_sintaxe": erro_ast,
            "classes": classes,
            "funcoes": funcoes,
            "imports": sorted(set(i for i in imports if i)),
            "referenciado_por_outros": (caminho.stem in referencias_encontradas) or (caminho.name == "main.py"),
            "qtd_padroes_fallback_ou_estimativa": len(ocorrencias_fallback),
            "amostra_fallback": ocorrencias_fallback[:5],
        })

    return detalhes_py, referencias_encontradas


def montar_texto_resumo_final(relatorio: dict) -> str:
    resumo = relatorio["resumo_objetivo"]
    pontos = relatorio["pontos_rigidos_avalista"]

    total_uteis = resumo["total_arquivos_uteis"]
    total_py = resumo["total_arquivos_py"]
    total_linhas = resumo["total_linhas_py"]
    qtd_erros = resumo["erros_sintaxe_py"]
    qtd_orfaos = resumo["modulos_py_sem_referencia_cruzada"]
    qtd_outros_sem_ref = resumo["arquivos_texto_config_sem_citacao_py"]
    lista_fallback = pontos["modulos_com_padroes_fallback_ou_estimativa"]

    partes = [
        "\n======================================================================",
        "RESUMO FINAL DO QUE ACONTECEU NA AUDITORIA",
        "======================================================================",
        (
            f"O mapeamento analisou '{relatorio['raiz_auditada']}' e encontrou "
            f"{total_uteis} arquivos úteis no total, sendo {total_py} arquivos Python "
            f"({total_linhas} linhas somadas)."
        ),
    ]

    if qtd_erros == 0:
        partes.append(
            "Sintaxe: Nenhum erro de sintaxe AST foi encontrado nos arquivos Python, "
            "ou seja, a estrutura base consegue ser lida pelo interpretador."
        )
    else:
        exemplos_erro = "; ".join(
            f"{e['arquivo']} ({e['erro']})" for e in pontos["erros_sintaxe"][:5]
        )
        partes.append(
            f"Sintaxe: Foram encontrados {qtd_erros} erro(s) de sintaxe que merecem "
            f"atenção antes de executar: {exemplos_erro}."
        )

    if lista_fallback:
        top_fallback = ", ".join(
            f"{item['arquivo']} ({item['qtd']})" for item in lista_fallback[:6]
        )
        partes.append(
            f"Fallbacks / Padrões / Estimativas: {len(lista_fallback)} módulo(s) "
            f"concentram termos ligados a padrão, fallback, simulação ou estimativa "
            f"(3 ou mais ocorrências). Principais: {top_fallback}."
        )
    else:
        partes.append(
            "Fallbacks / Padrões / Estimativas: Nenhum módulo atingiu 3 ou mais "
            "ocorrências desses termos."
        )

    if qtd_orfaos > 0 or qtd_outros_sem_ref > 0:
        exemplos_orfaos = ", ".join(pontos["modulos_py_sem_referencia_cruzada"][:6])
        texto_ref = (
            f"Referências cruzadas: {qtd_orfaos} módulo(s) .py não apareceram citados "
            f"diretamente em outros arquivos"
        )
        if exemplos_orfaos:
            texto_ref += f" (ex.: {exemplos_orfaos})"
        texto_ref += (
            f" e {qtd_outros_sem_ref} arquivo(s) de texto/config não foram citados em .py. "
            "Isso pode ser código auxiliar/CLI/estático ou coisa solta — vale conferir só "
            "no que importa para o fluxo principal."
        )
        partes.append(texto_ref)
    else:
        partes.append(
            "Referências cruzadas: Todos os módulos .py e arquivos de texto/config "
            "tiveram referência encontrada."
        )

    partes.append(
        "Conclusão prática: Use este resumo para escolher o primeiro bloco da auditoria "
        "real (sintaxe se houver, pontos de fallback/simulação ou os módulos principais "
        "do sistema) sem perder tempo mexendo no que já está funcional."
    )
    partes.append("======================================================================\n")

    return "\n\n".join(partes)


def mapear_projeto_avalista(
    pasta_projeto: str = ".",
    pasta_saida: str = "auditoria_avalista",
    salvar_arquivos: bool = False,
) -> dict:
    raiz = Path(pasta_projeto).resolve()

    arvore_linhas = [f"{raiz.name}/"] + gerar_arvore_visual(raiz)
    detalhes_py, _ = inspecionar_arquivos_python(raiz)

    todos_arquivos = [
        p for p in raiz.rglob("*")
        if p.is_file() and not any(parte in PASTAS_IGNORADAS for parte in p.parts)
    ]

    contagem_ext = {}
    arquivos_sem_ref_py = []

    for arq in todos_arquivos:
        ext = arq.suffix.lower() or "[sem_extensao]"
        contagem_ext[ext] = contagem_ext.get(ext, 0) + 1

        if ext not in {".py"} and ext not in EXTENSOES_BINARIAS_COMUNS:
            citado_em_py = False
            for py_file in raiz.rglob("*.py"):
                if any(parte in PASTAS_IGNORADAS for parte in py_file.parts):
                    continue
                try:
                    if arq.name in py_file.read_text(encoding="utf-8", errors="ignore"):
                        citado_em_py = True
                        break
                except OSError:
                    pass
            if not citado_em_py:
                arquivos_sem_ref_py.append(str(arq.relative_to(raiz)))

    modulos_orfaos_py = [
        item["arquivo"]
        for item in detalhes_py
        if not item["referenciado_por_outros"] and not item["arquivo"].endswith("__init__.py")
    ]

    erros_sintaxe = [
        {"arquivo": item["arquivo"], "erro": item["erro_sintaxe"]}
        for item in detalhes_py
        if item["erro_sintaxe"]
    ]

    modulos_com_muito_fallback = sorted(
        [
            {
                "arquivo": item["arquivo"],
                "qtd": item["qtd_padroes_fallback_ou_estimativa"],
                "amostra": item["amostra_fallback"],
            }
            for item in detalhes_py
            if item["qtd_padroes_fallback_ou_estimativa"] >= 3
        ],
        key=lambda x: x["qtd"],
        reverse=True,
    )

    relatorio = {
        "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "raiz_auditada": str(raiz),
        "resumo_objetivo": {
            "total_arquivos_uteis": len(todos_arquivos),
            "total_arquivos_py": len(detalhes_py),
            "total_linhas_py": sum(m["linhas"] for m in detalhes_py),
            "contagem_por_extensao": dict(sorted(contagem_ext.items())),
            "erros_sintaxe_py": len(erros_sintaxe),
            "modulos_py_sem_referencia_cruzada": len(modulos_orfaos_py),
            "arquivos_texto_config_sem_citacao_py": len(arquivos_sem_ref_py),
        },
        "pontos_rigidos_avalista": {
            "erros_sintaxe": erros_sintaxe,
            "modulos_py_sem_referencia_cruzada": modulos_orfaos_py,
            "arquivos_texto_config_sem_citacao_py": arquivos_sem_ref_py[:30],
            "modulos_com_padroes_fallback_ou_estimativa": modulos_com_muito_fallback,
        },
        "arvore_arquivos": arvore_linhas,
        "modulos_python": detalhes_py,
    }

    texto_final = montar_texto_resumo_final(relatorio)
    print(texto_final)

    if salvar_arquivos:
        saida_dir = Path(pasta_saida)
        saida_dir.mkdir(parents=True, exist_ok=True)
        carimbo = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho_json = saida_dir / f"mapa_avalista_{carimbo}.json"
        caminho_txt = saida_dir / f"resumo_avalista_{carimbo}.txt"

        linhas_detalhadas = [
            f"Data/Hora : {relatorio['gerado_em']}",
            f"Raiz      : {relatorio['raiz_auditada']}",
            "",
            "--- ÁRVORE DO PROJETO ---",
            *arvore_linhas,
            texto_final,
        ]
        caminho_json.write_text(json.dumps(relatorio, indent=2, ensure_ascii=False), encoding="utf-8")
        caminho_txt.write_text("\n".join(linhas_detalhadas), encoding="utf-8")

    return relatorio


if __name__ == "__main__":
    mapear_projeto_avalista(".", salvar_arquivos=False)