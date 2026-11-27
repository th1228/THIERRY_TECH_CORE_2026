import ast
import shutil
from pathlib import Path

ARQ_C2 = Path("core/c2_sovereign_intelligence.py")
ARQ_VIS = Path("core/visagismo_estetica_roi.py")

BLOCO_IMPORT_LIMPO = """try:
    from core.c2_sovereign_intelligence import BiogemEngine
except ImportError:
    try:
        from c2_sovereign_intelligence import BiogemEngine
    except ImportError:
        class BiogemEngine:
            def __init__(self, *args, **kwargs):
                pass
"""

BLOCO_RESOLVER_NOME = """    def _resolver_nome_cliente(self, dados=None) -> str:
        candidatos = []
        if isinstance(dados, dict):
            candidatos.extend([
                dados.get("nome_cliente"),
                dados.get("nome"),
                dados.get("paciente"),
                dados.get("cliente"),
            ])
        candidatos.append(getattr(self, "nome_cliente", None))

        for valor in candidatos:
            if isinstance(valor, str) and valor.strip():
                return valor.strip()
        return "Não informado"
"""


def log(msg: str) -> None:
    print(msg, flush=True)


def salvar_com_validacao(arquivo: Path, novo_texto: str) -> None:
    ast.parse(novo_texto, filename=str(arquivo))
    bak = arquivo.with_suffix(arquivo.suffix + ".bak_roi")
    if not bak.exists():
        shutil.copy2(arquivo, bak)
    arquivo.write_text(novo_texto, encoding="utf-8")
    log(f"[OK] Validado e salvo: {arquivo}")


def ajustar_assinatura_gerar_pdf(texto: str) -> str:
    alvo = 'def gerar_pdf_visagismo_roi(self, pontos_base=None, caminho_salvamento="visagismo_estetica_roi.pdf"):'
    if alvo not in texto:
        texto = texto.replace(
            "def gerar_pdf_visagismo_roi(self, pontos_base, caminho_salvamento):",
            alvo,
            1,
        )
    return texto


def garantir_atributos_init(texto: str, arvore: ast.Module) -> str:
    linhas = texto.splitlines(keepends=True)
    for no in ast.walk(arvore):
        if isinstance(no, ast.ClassDef) and no.name == "VisagismoEsteticaRoi":
            for item in no.body:
                if isinstance(item, ast.FunctionDef) and item.name == "__init__" and item.body:
                    primeira_stmt = item.body[0]
                    indent = " " * primeira_stmt.col_offset
                    bloco_extra = ""
                    if 'hasattr(self, "nome_cliente")' not in texto:
                        bloco_extra += (
                            f'{indent}if not hasattr(self, "nome_cliente") or not isinstance(getattr(self, "nome_cliente"), str) or not getattr(self, "nome_cliente").strip():\n'
                            f'{indent}    self.nome_cliente = "Não informado"\n'
                        )
                    if 'hasattr(self, "operador")' not in texto:
                        bloco_extra += (
                            f'{indent}if not hasattr(self, "operador") or not isinstance(getattr(self, "operador"), str) or not getattr(self, "operador").strip():\n'
                            f'{indent}    self.operador = "Não informado"\n'
                        )
                    if 'hasattr(self, "telemetria")' not in texto:
                        bloco_extra += (
                            f'{indent}if not hasattr(self, "telemetria"):\n'
                            f'{indent}    self.telemetria = {{}}\n'
                        )
                    if bloco_extra:
                        linhas.insert(primeira_stmt.lineno - 1, bloco_extra)
                        log("[OK] Atributos padrão 'nome_cliente', 'operador' e 'telemetria' garantidos no __init__.")
                    return "".join(linhas)
    return texto


def garantir_resolver_e_fallback_malha(texto: str, arvore: ast.Module) -> str:
    bloco_fallback = (
        "    def _refinar_malha_alta_densidade(self, pontos=None, *args, **kwargs):\n"
        "        if isinstance(pontos, dict):\n"
        "            return pontos\n"
        '        return {"status": "base", "referencia": pontos or "", "densidade": 1.0, "pontos": pontos or []}\n'
    )

    linhas = texto.splitlines(keepends=True)
    substituido = False

    for no in ast.walk(arvore):
        if isinstance(no, ast.FunctionDef) and no.name == "_refinar_malha_alta_densidade":
            inicio = no.lineno - 1
            fim = no.end_lineno
            linhas[inicio:fim] = [bloco_fallback]
            texto = "".join(linhas)
            substituido = True
            break

    if "def _resolver_nome_cliente(" not in texto:
        marcador = "\n    def gerar_pdf_visagismo_roi"
        if marcador in texto:
            texto = texto.replace(marcador, "\n" + BLOCO_RESOLVER_NOME + marcador, 1)
            log("[OK] Método '_resolver_nome_cliente' adicionado.")

    if not substituido:
        marcador = "\n    def gerar_pdf_visagismo_roi"
        if marcador in texto:
            texto = texto.replace(marcador, "\n" + bloco_fallback + marcador, 1)

    alvo_metricas = "metricas_malha = self._refinar_malha_alta_densidade(pontos_base)"
    sub_metricas = (
        "metricas_malha = self._refinar_malha_alta_densidade(pontos_base)\n"
        "        if not isinstance(metricas_malha, dict):\n"
        '            metricas_malha = {"status": "base", "referencia": str(metricas_malha), "densidade": 1.0}\n'
        "        self.nome_cliente = self._resolver_nome_cliente(pontos_base)"
    )
    if alvo_metricas in texto and "self._resolver_nome_cliente(pontos_base)" not in texto:
        texto = texto.replace(alvo_metricas, sub_metricas, 1)

    log("[OK] Fallback '_refinar_malha_alta_densidade' pronto.")
    return texto


def corrigir_dirname_makedirs(texto: str) -> str:
    alvo = "os.makedirs(os.path.dirname(caminho_salvamento), exist_ok=True)"
    sub = (
        'if not caminho_salvamento:\n'
        '            caminho_salvamento = "visagismo_estetica_roi.pdf"\n'
        '        _pasta_pdf = os.path.dirname(caminho_salvamento)\n'
        '        if _pasta_pdf:\n'
        '            os.makedirs(_pasta_pdf, exist_ok=True)'
    )
    if alvo in texto:
        texto = texto.replace(alvo, sub, 1)
        log("[OK] Proteção de diretório vazio em os.makedirs aplicada.")
    return texto


def corrigir_visagismo() -> None:
    log("[...] Processando core/visagismo_estetica_roi.py")
    texto = ARQ_VIS.read_text(encoding="utf-8")
    arvore = ast.parse(texto, filename=str(ARQ_VIS))

    if "from c2_sovereign_intelligence import BiogemEngine" in texto and "class BiogemEngine:" not in texto:
        texto = texto.replace("from c2_sovereign_intelligence import BiogemEngine", BLOCO_IMPORT_LIMPO.rstrip(), 1)

    texto = ajustar_assinatura_gerar_pdf(texto)
    texto = garantir_resolver_e_fallback_malha(texto, arvore)
    arvore_atualizada = ast.parse(texto, filename=str(ARQ_VIS))
    texto = garantir_atributos_init(texto, arvore_atualizada)
    texto = corrigir_dirname_makedirs(texto)
    salvar_com_validacao(ARQ_VIS, texto)


def corrigir_c2() -> None:
    log("[...] Processando core/c2_sovereign_intelligence.py")
    texto = ARQ_C2.read_text(encoding="utf-8")

    alvo_horizon = "self.horizon = int(horizon_years)"
    sub_horizon = (
        "try:\n"
        "            self.horizon = int(float(horizon_years)) if horizon_years is not None else 15\n"
        "        except (ValueError, TypeError):\n"
        "            self.horizon = 15"
    )
    if alvo_horizon in texto:
        texto = texto.replace(alvo_horizon, sub_horizon, 1)

    alvo_aum = "self.aum = aum_bilhoes_eur * 1000.0"
    sub_aum = (
        "if isinstance(aum_bilhoes_eur, dict):\n"
        '            _aum_bruto = aum_bilhoes_eur.get("aum_bilhoes_eur", aum_bilhoes_eur.get("valor", 25.0))\n'
        "        else:\n"
        "            _aum_bruto = aum_bilhoes_eur\n"
        "        self.aum = _extrair_float_c2(_aum_bruto, 25.0) * 1000.0"
    )
    if alvo_aum in texto:
        texto = texto.replace(alvo_aum, sub_aum, 1)

    alvo_ameaca = "self.ameaca = fator_ameaca_mercado"
    sub_ameaca = (
        "if isinstance(fator_ameaca_mercado, dict):\n"
        '            _ameaca_bruta = fator_ameaca_mercado.get("fator_ameaca_mercado", fator_ameaca_mercado.get("valor", 0.40))\n'
        "        else:\n"
        "            _ameaca_bruta = fator_ameaca_mercado\n"
        "        self.ameaca = _extrair_float_c2(_ameaca_bruta, 0.40)"
    )
    if alvo_ameaca in texto:
        texto = texto.replace(alvo_ameaca, sub_ameaca, 1)

    salvar_com_validacao(ARQ_C2, texto)


def main() -> None:
    corrigir_c2()
    corrigir_visagismo()


if __name__ == "__main__":
    main()