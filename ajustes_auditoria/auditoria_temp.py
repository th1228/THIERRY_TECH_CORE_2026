import ast
import hashlib
import json
import os
import re
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

IGNORAR_DIRS = {
    '__pycache__', '.git', 'node_modules', 'venv', '.venv',
    'env', '.idea', '.vscode', 'dist', 'build',
    '_archive', 'ajustes_auditoria'
}
AUTO_ARQUIVOS = {'auditoria_temp.py', 'auditoria_real.py'}
ARQUIVO_ESTADO_PAINEIS = '.auditoria_painéis_estado.json'
PASTA_SAIDA_JSON = Path('ajustes_auditoria') / 'relatorios_json'
ARQUIVO_ULTIMA_JSON = Path('ajustes_auditoria') / 'ultima_auditoria.json'

PALAVRAS_PT = {
    'visagismo', 'tricologia', 'telemedicina', 'diagnóstico', 'diagnostico',
    'relatório', 'relatorio', 'clínica', 'clinica', 'segurança', 'seguranca',
    'configuração', 'configuracao', 'módulo', 'modulo', 'usuário', 'usuario',
    'capilar', 'avaliação', 'avaliacao'
}
PALAVRAS_EN = {
    'trichology', 'visagism', 'telemedicine', 'diagnostics', 'governance',
    'architecture', 'security', 'endpoint', 'compliance', 'clinical', 'report',
    'biometric', 'longevity', 'intangible'
}


def calcular_sha256_texto(texto: str) -> str:
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()


def remover_comentarios_js(codigo_js: str) -> str:
    """Remove comentários de bloco /* ... */ e de linha // ... para evitar falsos avisos."""
    sem_bloco = re.sub(r'/\*[\s\S]*?\*/', ' ', codigo_js)
    linhas_limpas = []
    for linha in sem_bloco.splitlines():
        idx_barra = linha.find('//')
        if idx_barra != -1:
            antes = linha[:idx_barra]
            if (
                antes.count("'") % 2 == 0
                and antes.count('"') % 2 == 0
                and antes.count('`') % 2 == 0
            ):
                linha = antes
        linhas_limpas.append(linha)
    return "\n".join(linhas_limpas)


class AuditorHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.scripts = []
        self.links = []
        self.botoes = []
        self.inputs = []
        self.forms = []
        self.canvas = 0
        self.videos = 0
        self._in_script = False
        self._script_atual = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == 'html' and 'lang' in attr_dict:
            self.lang = attr_dict['lang']
        elif tag == 'script':
            if 'src' in attr_dict:
                self.links.append(('script', attr_dict['src']))
            else:
                self._in_script = True
                self._script_atual = []
        elif tag == 'a' and 'href' in attr_dict:
            self.links.append(('a', attr_dict['href']))
        elif tag == 'link' and 'href' in attr_dict:
            self.links.append(('link', attr_dict['href']))
        elif tag == 'button':
            self.botoes.append(attr_dict.get('onclick', 'sem_evento'))
        elif tag == 'input':
            self.inputs.append(attr_dict.get('type', 'text'))
        elif tag == 'form':
            self.forms.append(attr_dict.get('action', 'sem_action'))
        elif tag == 'canvas':
            self.canvas += 1
        elif tag == 'video':
            self.videos += 1

    def handle_endtag(self, tag):
        if tag == 'script' and self._in_script:
            self._in_script = False
            self.scripts.append("".join(self._script_atual))

    def handle_data(self, data):
        if self._in_script:
            self._script_atual.append(data)


def gerar_arvore_diretorios(raiz: Path, max_profundidade: int = 3) -> list[str]:
    linhas = [f"{raiz.name}/"]

    def _percorrer(atual: Path, prefixo: str, nivel: int):
        if nivel > max_profundidade:
            return
        try:
            itens = sorted(
                [
                    p for p in atual.iterdir()
                    if p.name not in IGNORAR_DIRS and p.name not in AUTO_ARQUIVOS
                ],
                key=lambda p: (not p.is_dir(), p.name.lower())
            )
        except PermissionError:
            return

        for idx, item in enumerate(itens):
            ultimo = idx == len(itens) - 1
            conector = "└── " if ultimo else "├── "
            proximo_prefixo = "    " if ultimo else "│   "
            nome_exibicao = f"{item.name}/" if item.is_dir() else item.name
            linhas.append(f"{prefixo}{conector}{nome_exibicao}")
            if item.is_dir():
                _percorrer(item, prefixo + proximo_prefixo, nivel + 1)

    _percorrer(raiz, "", 1)
    return linhas


def analisar_python(caminho: Path, raiz: Path) -> dict:
    rel_str = str(caminho.relative_to(raiz)).replace('\\', '/')
    info = {
        "arquivo": rel_str,
        "linhas": 0,
        "valido": True,
        "erro_sintaxe": None,
        "classes": [],
        "funcoes": [],
        "rotas_api": [],
        "imports": [],
        "tem_try_except": False,
        "tem_cors_ou_env": False,
        "riscos": []
    }
    try:
        codigo = caminho.read_text(encoding='utf-8', errors='replace')
        info["linhas"] = len(codigo.splitlines())
        arvore = ast.parse(codigo, filename=str(caminho))
    except SyntaxError as e:
        info["valido"] = False
        info["erro_sintaxe"] = f"Linha {e.lineno}: {e.msg}"
        return info

    texto_lower = codigo.lower()
    if any(k in texto_lower for k in ('cors', 'os.getenv', 'load_dotenv', 'pydantic', 'basemodel')):
        info["tem_cors_ou_env"] = True

    for node in ast.walk(arvore):
        if isinstance(node, ast.Try):
            info["tem_try_except"] = True
        elif isinstance(node, ast.ClassDef):
            info["classes"].append(node.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            info["funcoes"].append(node.name)
            for dec in node.decorator_list:
                dec_str = ast.dump(dec)
                if any(r in dec_str for r in ['route', 'get', 'post', 'put', 'delete', 'patch']):
                    info["rotas_api"].append(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                info["imports"].append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            info["imports"].append(node.module)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {'eval', 'exec'}:
                info["riscos"].append(f"Uso inseguro de '{node.func.id}()' na linha {node.lineno}")

    return info


def analisar_html(caminho: Path, raiz: Path, estado_anterior: dict) -> dict:
    conteudo = caminho.read_text(encoding='utf-8', errors='replace')
    sha_atual = calcular_sha256_texto(conteudo)
    mtime_atual = datetime.fromtimestamp(caminho.stat().st_mtime).strftime('%d/%m/%Y %H:%M:%S')
    linhas_atual = len(conteudo.splitlines())

    parser = AuditorHTML()
    parser.feed(conteudo)

    js_bruto = "\n".join(parser.scripts)
    js_ativo = remover_comentarios_js(js_bruto)

    funcoes_js = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', js_ativo)
    chamadas_rede = re.findall(
        r'(?:fetch|axios|XMLHttpRequest|WebSocket)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]',
        js_ativo
    )
    redirecionamentos_comentados = re.findall(
        r'//\s*window\.location\.href\s*=\s*[\'"`]([^\'"`]+)[\'"`]',
        js_bruto
    )
    alerts_ativos = len(re.findall(r'\b(?:window\.)?alert\s*\(', js_ativo))
    alerts_brutos = len(re.findall(r'\b(?:window\.)?alert\s*\(', js_bruto))

    links_quebrados = []
    for tipo, destino in parser.links:
        destino_limpo = destino.strip()
        if (
            not destino_limpo
            or destino_limpo.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'data:', '{{', '{%', '/'))
        ):
            continue
        alvo = (caminho.parent / destino_limpo.split('?')[0]).resolve()
        if not alvo.exists():
            links_quebrados.append(f"{tipo} -> '{destino}' (arquivo local não encontrado)")

    texto_visivel = re.sub(r'<[^>]+>', ' ', conteudo).lower()
    qtd_pt = sum(1 for p in PALAVRAS_PT if re.search(rf'\b{re.escape(p)}\b', texto_visivel))
    qtd_en = sum(1 for p in PALAVRAS_EN if re.search(rf'\b{re.escape(p)}\b', texto_visivel))
    bilingue_ok = qtd_pt > 0 and qtd_en > 0

    rel_str = str(caminho.relative_to(raiz)).replace('\\', '/')
    anterior = estado_anterior.get(rel_str)

    if anterior is None:
        status_mudanca = "NOVO (primeira leitura real registrada)"
        mudou_de_fato = True
    elif anterior.get("sha256") != sha_atual:
        diff_linhas = linhas_atual - anterior.get("linhas", linhas_atual)
        diff_alerts = alerts_ativos - anterior.get("alerts_ativos", alerts_ativos)
        status_mudanca = (
            f"MUDADO DE FATO (hash alterado | linhas: {diff_linhas:+d} | "
            f"alert() ativos: {anterior.get('alerts_ativos', 0)} -> {alerts_ativos} [{diff_alerts:+d}])"
        )
        mudou_de_fato = True
    else:
        status_mudanca = "SEM MUDANÇA (hash idêntico à leitura anterior)"
        mudou_de_fato = False

    snapshot_novo = {
        "sha256": sha_atual,
        "linhas": linhas_atual,
        "mtime": mtime_atual,
        "alerts_ativos": alerts_ativos,
        "alerts_brutos": alerts_brutos,
        "botoes": len(parser.botoes),
        "inputs": len(parser.inputs),
    }

    return {
        "arquivo": rel_str,
        "linhas": linhas_atual,
        "mtime": mtime_atual,
        "sha256": sha_atual,
        "status_mudanca": status_mudanca,
        "mudou_de_fato": mudou_de_fato,
        "snapshot_novo": snapshot_novo,
        "lang": parser.lang,
        "qtd_pt": qtd_pt,
        "qtd_en": qtd_en,
        "bilingue_ok": bilingue_ok,
        "funcoes_js": funcoes_js,
        "chamadas_rede": chamadas_rede,
        "redirecionamentos_comentados": redirecionamentos_comentados,
        "alerts_ativos": alerts_ativos,
        "alerts_brutos": alerts_brutos,
        "links_quebrados": links_quebrados,
        "botoes": len(parser.botoes),
        "inputs": len(parser.inputs),
        "canvas": parser.canvas,
        "videos": parser.videos
    }


def carregar_estado_paineis(caminho_estado: Path) -> dict:
    if not caminho_estado.exists():
        return {}
    try:
        dados = json.loads(caminho_estado.read_text(encoding='utf-8'))
        return dados.get("paineis", {}) if isinstance(dados, dict) else {}
    except Exception:
        return {}


def salvar_estado_paineis(caminho_estado: Path, raiz: Path, mapa_paineis: dict) -> None:
    payload = {
        "atualizado_em": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        "raiz": str(raiz),
        "paineis": mapa_paineis,
    }
    caminho_estado.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')


def salvar_registro_json(raiz: Path, agora: datetime, dados_auditoria: dict) -> tuple[Path, Path]:
    pasta_hist = raiz / PASTA_SAIDA_JSON
    pasta_hist.mkdir(parents=True, exist_ok=True)

    caminho_ultima = raiz / ARQUIVO_ULTIMA_JSON
    caminho_ultima.parent.mkdir(parents=True, exist_ok=True)

    nome_hist = f"auditoria_{agora.strftime('%Y%m%d_%H%M%S')}.json"
    caminho_hist = pasta_hist / nome_hist

    conteudo_json = json.dumps(dados_auditoria, indent=2, ensure_ascii=False)
    caminho_hist.write_text(conteudo_json, encoding='utf-8')
    caminho_ultima.write_text(conteudo_json, encoding='utf-8')

    return caminho_hist, caminho_ultima


def executar_auditoria():
    agora = datetime.now()
    raiz = Path(".").resolve()
    caminho_estado = raiz / ARQUIVO_ESTADO_PAINEIS
    estado_anterior = carregar_estado_paineis(caminho_estado)

    arquivos_py = []
    arquivos_html = []
    arquivos_js = []
    arquivos_json = []
    segredos_expostos = []
    tem_env_example = False
    tem_gitignore = False
    tem_requirements_ou_pyproject = False
    tem_testes = False

    padrao_segredo = re.compile(
        r'(?:api_key|apikey|secret_key|private_key|bearer_token)\s*[:=]\s*[\'"]([A-Za-z0-9_\-\.]{16,})[\'"]',
        re.IGNORECASE
    )

    for dirpath, dirnames, filenames in os.walk(raiz):
        dirnames[:] = [d for d in dirnames if d not in IGNORAR_DIRS]
        for fname in filenames:
            if fname in AUTO_ARQUIVOS or fname == ARQUIVO_ESTADO_PAINEIS:
                continue
            fpath = Path(dirpath) / fname
            ext = fpath.suffix.lower()

            if fname == '.env.example':
                tem_env_example = True
            if fname == '.gitignore':
                tem_gitignore = True
            if fname in {'requirements.txt', 'pyproject.toml', 'setup.py'}:
                tem_requirements_ou_pyproject = True
            if 'test' in fname.lower() and ext == '.py':
                tem_testes = True

            if ext in {'.py', '.html', '.htm', '.js', '.json', '.env'}:
                try:
                    txt = fpath.read_text(encoding='utf-8', errors='ignore')
                    for m in padrao_segredo.finditer(txt):
                        trecho = m.group(0).lower()
                        if any(ex in trecho for ex in ('example', 'sample', 'your_', 'changeme', 'placeholder', 'test_')):
                            continue
                        segredos_expostos.append(
                            f"{fpath.relative_to(raiz)} -> chave '{m.group(0)[:24]}...' possivelmente hardcoded"
                        )
                except Exception:
                    pass

            if ext == '.py':
                arquivos_py.append(fpath)
            elif ext in {'.html', '.htm'}:
                arquivos_html.append(fpath)
            elif ext == '.js':
                arquivos_js.append(fpath)
            elif ext == '.json':
                arquivos_json.append(fpath)

    falhas_bloqueantes = []
    avisos_otimizacao = []
    arquivos_bilingues = 0
    total_en_detectado = 0
    total_rotas_api = 0
    algum_try_except = False
    algum_config_segura = False

    detalhes_py = []
    lista_py_json = []
    for py in arquivos_py:
        res = analisar_python(py, raiz)
        lista_py_json.append(res)
        nome_rel = py.relative_to(raiz)
        total_rotas_api += len(res["rotas_api"])
        if res["tem_try_except"]:
            algum_try_except = True
        if res["tem_cors_ou_env"]:
            algum_config_segura = True

        if not res["valido"]:
            falhas_bloqueantes.append(f"Erro de sintaxe em {nome_rel}: {res['erro_sintaxe']}")
            detalhes_py.append(f"  [ERRO DE SINTAXE] {nome_rel} -> {res['erro_sintaxe']}")
        else:
            detalhes_py.append(
                f"  [OK] {nome_rel} ({res['linhas']} linhas): {len(res['classes'])} classes, "
                f"{len(res['funcoes'])} funções, {len(res['rotas_api'])} rotas API"
            )
            if res["imports"]:
                detalhes_py.append(f"       Imports: {', '.join(sorted(set(res['imports']))[:12])}")
            for risco in res["riscos"]:
                falhas_bloqueantes.append(f"{nome_rel}: {risco}")
                detalhes_py.append(f"       [RISCO] {risco}")

    detalhes_html = []
    resumo_mudancas_html = []
    lista_html_json = []
    novo_estado_paineis = {}
    paineis_mudados = 0

    for html in arquivos_html:
        res = analisar_html(html, raiz, estado_anterior)
        lista_html_json.append({
            k: v for k, v in res.items() if k != "snapshot_novo"
        })
        novo_estado_paineis[res["arquivo"]] = res["snapshot_novo"]
        if res["mudou_de_fato"]:
            paineis_mudados += 1
        resumo_mudancas_html.append(f"  • {res['arquivo']} -> {res['status_mudanca']} (modificado em {res['mtime']})")

        total_en_detectado += res["qtd_en"]
        if res["bilingue_ok"]:
            arquivos_bilingues += 1

        detalhes_html.append(
            f"  • {res['arquivo']} ({res['linhas']} linhas | lang='{res['lang'] or 'não definido'}' | {res['status_mudanca']})"
        )
        detalhes_html.append(
            f"    Elementos: {res['botoes']} botões | {res['inputs']} inputs | "
            f"{res['canvas']} canvas | {res['videos']} vídeos | sha256={res['sha256'][:12]}..."
        )

        if res["bilingue_ok"]:
            detalhes_html.append(
                f"    [BILÍNGUE OK] Termos em PT ({res['qtd_pt']}) e EN ({res['qtd_en']}) "
                f"confirmados como arquitetura bilíngue."
            )
        elif res["qtd_en"] > 0:
            detalhes_html.append(f"    [EN OK] Termos em inglês detectados ({res['qtd_en']}).")
        elif res["qtd_pt"] > 0:
            avisos_otimizacao.append(f"{res['arquivo']} possui apenas termos em PT ({res['qtd_pt']}); confira suporte EN.")
            detalhes_html.append(f"    [I18N] Apenas termos em PT ({res['qtd_pt']}) detectados.")

        if not res["lang"]:
            avisos_otimizacao.append(f"{res['arquivo']} sem atributo 'lang' no <html>.")
            detalhes_html.append("    [AVISO] Atributo 'lang' ausente na tag <html>.")
        if res["chamadas_rede"]:
            detalhes_html.append(f"    Conexões de rede: {', '.join(res['chamadas_rede'])}")
        if res["redirecionamentos_comentados"]:
            avisos_otimizacao.append(f"{res['arquivo']} tem redirecionamento comentado.")
            detalhes_html.append(f"    [AVISO] Redirecionamento comentado: {', '.join(res['redirecionamentos_comentados'])}")
        if res["alerts_ativos"] > 0:
            avisos_otimizacao.append(f"{res['arquivo']} tem {res['alerts_ativos']} alert() ativo(s).")
            detalhes_html.append(f"    [AVISO] {res['alerts_ativos']} chamada(s) 'alert()' ativa(s) encontrada(s).")
        elif res["alerts_brutos"] > 0:
            detalhes_html.append(
                f"    [OK] {res['alerts_brutos']} ocorrência(s) de 'alert(' apenas em comentários (0 ativas)."
            )
        for lq in res["links_quebrados"]:
            falhas_bloqueantes.append(f"{res['arquivo']} tem link quebrado: {lq}")
            detalhes_html.append(f"    [QUEBRADO] {lq}")

    salvar_estado_paineis(caminho_estado, raiz, novo_estado_paineis)

    detalhes_json = []
    lista_json_validados = []
    for js_file in arquivos_json:
        rel_json = str(js_file.relative_to(raiz)).replace('\\', '/')
        try:
            json.loads(js_file.read_text(encoding='utf-8'))
            detalhes_json.append(f"  [OK] {rel_json}")
            lista_json_validados.append({"arquivo": rel_json, "valido": True, "erro": None})
        except Exception as e:
            falhas_bloqueantes.append(f"JSON inválido em {rel_json}: {e}")
            detalhes_json.append(f"  [ERRO JSON] {rel_json} -> {e}")
            lista_json_validados.append({"arquivo": rel_json, "valido": False, "erro": str(e)})

    for s in segredos_expostos:
        falhas_bloqueantes.append(s)

    if arquivos_html and total_en_detectado == 0:
        falhas_bloqueantes.append("Nenhum termo em inglês detectado nos arquivos HTML para nível internacional.")

    pontos_senior = []
    if arquivos_py:
        pontos_senior.append(
            f"Backend Python: {len(arquivos_py)} arquivo(s), {total_rotas_api} rota(s) mapeada(s), "
            f"tratamento try/except {'presente' if algum_try_except else 'ausente'}."
        )
    else:
        pontos_senior.append("Backend Python: nenhum arquivo .py encontrado.")

    pontos_senior.append(
        f"Segurança & Env: sem segredos óbvios expostos | .gitignore={'OK' if tem_gitignore else 'ausente'} | "
        f".env.example={'OK' if tem_env_example else 'ausente'} | config/CORS/env={'OK' if algum_config_segura else 'não detectado'}."
    )
    pontos_senior.append(
        f"Empacotamento & Testes: manifesto de dependências={'OK' if tem_requirements_ou_pyproject else 'ausente'} | "
        f"arquivos de teste={'OK' if tem_testes else 'ausente'}."
    )
    pontos_senior.append(
        f"Internacionalização (PT/EN): {arquivos_bilingues} HTML(s) bilíngue(s) validado(s) e "
        f"{total_en_detectado} ocorrência(s) de termos-chave em inglês."
    )

    ta_pronto = len(falhas_bloqueantes) == 0
    status_msg = (
        "STATUS: TÁ PRONTO PARA NÍVEL INTERNACIONAL"
        if ta_pronto
        else "STATUS: NÃO TÁ PRONTO PARA NÍVEL INTERNACIONAL"
    )

    dados_json = {
        "data_hora": agora.strftime('%d/%m/%Y %H:%M:%S'),
        "timestamp_iso": agora.isoformat(),
        "raiz": str(raiz),
        "pronto_nivel_internacional": ta_pronto,
        "status_msg": status_msg,
        "inventario": {
            "python": len(arquivos_py),
            "html": len(arquivos_html),
            "js": len(arquivos_js),
            "json": len(arquivos_json),
            "paineis_html_lidos": len(arquivos_html),
            "paineis_html_com_mudanca": paineis_mudados,
            "htmls_bilingues": arquivos_bilingues,
            "ocorrencias_en": total_en_detectado,
            "rotas_api": total_rotas_api,
        },
        "seguranca_e_projeto": {
            "gitignore": tem_gitignore,
            "env_example": tem_env_example,
            "manifesto_dependencias": tem_requirements_ou_pyproject,
            "arquivos_teste": tem_testes,
            "try_except_presente": algum_try_except,
            "config_cors_ou_env": algum_config_segura,
            "segredos_expostos": segredos_expostos,
        },
        "falhas_bloqueantes": falhas_bloqueantes,
        "avisos_otimizacao": avisos_otimizacao,
        "visao_senior": pontos_senior,
        "arvore_diretorios": gerar_arvore_diretorios(raiz),
        "analise_python": lista_py_json,
        "analise_html_paineis": lista_html_json,
        "validacao_json": lista_json_validados,
    }

    caminho_hist, caminho_ultima = salvar_registro_json(raiz, agora, dados_json)

    rel = [
        "=" * 78,
        status_msg,
        f"Data: {agora.strftime('%d/%m/%Y %H:%M:%S')} | Raiz: {raiz}",
        "=" * 78,
        "",
        "[0] VEREDITO RÁPIDO",
        f"  -> {status_msg}",
        f"  -> Varredura real de painéis HTML: {len(arquivos_html)} lido(s) | {paineis_mudados} com alteração detectada.",
        f"  -> Suporte bilíngue PT/EN: {arquivos_bilingues} arquivo(s) HTML com ambos os idiomas reconhecidos como válido.",
        f"  -> Registro JSON salvo em: {caminho_ultima.relative_to(raiz)}",
        f"  -> Histórico datado salvo em: {caminho_hist.relative_to(raiz)}",
    ]

    if resumo_mudancas_html:
        rel.append("  Diagnóstico real de mudança nos painéis:")
        rel.extend(resumo_mudancas_html)

    if falhas_bloqueantes:
        rel.append("  Falhas bloqueantes encontradas:")
        for f in falhas_bloqueantes:
            rel.append(f"    [BLOQUEIO] {f}")
    else:
        rel.append("  -> Nenhuma falha técnica bloqueante encontrada na checagem estática.")

    if avisos_otimizacao:
        rel.append("  Pontos de otimização (não bloqueiam, mas refinam o acabamento):")
        for a in avisos_otimizacao:
            rel.append(f"    [OTIMIZAR] {a}")

    rel.append("\n[1] VISÃO DO ENGENHEIRO SÊNIOR (ARQUITETURA, SEGURANÇA & ESCALA)")
    for ps in pontos_senior:
        rel.append(f"  • {ps}")

    rel.append("\n[2] ÁRVORE DE ESTRUTURA E INVENTÁRIO")
    for linha_arv in gerar_arvore_diretorios(raiz):
        rel.append(f"  {linha_arv}")
    rel.append(
        f"\n  • Python (.py): {len(arquivos_py)} | HTML: {len(arquivos_html)} | "
        f"JS: {len(arquivos_js)} | JSON: {len(arquivos_json)}"
    )

    rel.append("\n[3] ANÁLISE PYTHON (AST)")
    if not detalhes_py:
        rel.append("  ! Nenhum arquivo .py encontrado neste diretório.")
    else:
        rel.extend(detalhes_py)

    rel.append("\n[4] INTERFACES E SUPORTE BILÍNGUE (HTML/JS)")
    if not detalhes_html:
        rel.append("  ! Nenhum arquivo .html/.htm encontrado neste diretório.")
    else:
        rel.extend(detalhes_html)

    rel.append("\n[5] VALIDAÇÃO JSON")
    if not detalhes_json:
        rel.append("  ! Nenhum arquivo .json encontrado neste diretório.")
    else:
        rel.extend(detalhes_json)

    rel.extend([
        "",
        "=" * 78,
        status_msg,
        "=" * 78,
    ])

    print("\n".join(rel))


if __name__ == "__main__":
    executar_auditoria()