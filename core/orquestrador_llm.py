# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the
intellectual property of Thierry Technology Concept Global. Unauthorized
distribution, reverse engineering, or usage without a signed NDA/License
agreement is strictly prohibited under international copyright frameworks.
===========================================================================
"""

"""
Orquestrador Multi-IA com Sanitização, Resiliência, JSON Estruturado e Fallback Soberano
Thierry Technology Concept Global - Execução Soberana
Integrado ao Gerador Master de Dossiês PDF e Memória Comum
"""

import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

from google import genai
from google.genai import types

# --- CORREÇÃO DE CAMINHO (INSERE RAIZ DO PROJETO E PASTA ATUAL NO INÍCIO DO SYS.PATH) ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)

for _caminho in (PARENT_DIR, SCRIPT_DIR):
    if _caminho and os.path.isdir(_caminho) and _caminho not in sys.path:
        sys.path.insert(0, _caminho)


def _carregar_env_local() -> None:
    """Carrega o arquivo .env da pasta do script, da raiz do projeto ou do diretório atual."""
    candidatos_env = [
        os.path.join(SCRIPT_DIR, ".env"),
        os.path.join(PARENT_DIR, ".env"),
        ".env",
    ]

    try:
        from dotenv import load_dotenv

        for caminho_env in candidatos_env:
            if os.path.isfile(caminho_env):
                load_dotenv(dotenv_path=caminho_env, override=False)
                break
        else:
            load_dotenv(override=False)
        return
    except ImportError:
        pass

    for caminho_env in candidatos_env:
        if os.path.isfile(caminho_env):
            try:
                with open(caminho_env, "r", encoding="utf-8") as arquivo_env:
                    for linha in arquivo_env:
                        linha_limpa = linha.strip()
                        if not linha_limpa or linha_limpa.startswith("#") or "=" not in linha_limpa:
                            continue
                        chave, valor = linha_limpa.split("=", 1)
                        chave = chave.strip()
                        valor = valor.strip().strip('"').strip("'")
                        if chave and chave not in os.environ:
                            os.environ[chave] = valor
                break
            except Exception:
                pass


_carregar_env_local()

# --- HORIZONTES DE PROJEÇÃO PADRÃO ---
HORIZONTES_PROJECTION: List[int] = [5, 10, 15]

# --- TIMEOUT PARA REQUISIÇÕES EXTERNAS (SEGUNDOS) ---
TIMEOUT_REQUISICAO_SEGUNDOS: int = 20

# --- CHAVES JSON OBRIGATÓRIAS ---
CHAVES_JSON_DOSSIE: List[str] = [
    "diagnostico_estrutural",
    "analise_dermica_hsv",
    "projecao_temporal",
    "recomendacao_tecnica",
]

# --- CADEIA DE MODELOS GEMINI ---
MODELOS_GEMINI: List[str] = [
    "models/gemini-2.5-flash",
    "models/gemini-2.5-flash-lite",
]

# --- CADEIA DE PROVEDORES COMPATÍVEIS COM OPENAI ---
PROVEDORES_OPENAI_COMPATIVEIS: List[Dict[str, str]] = [
    {
        "nome": "Groq",
        "env_key": "GROQ_API_KEY",
        "env_url": "GROQ_BASE_URL",
        "url_padrao": "https://api.groq.com/openai/v1/chat/completions",
        "env_model": "GROQ_MODEL",
        "modelo_padrao": "llama-3.3-70b-versatile",
    },
    {
        "nome": "OpenRouter",
        "env_key": "OPENROUTER_API_KEY",
        "env_url": "OPENROUTER_BASE_URL",
        "url_padrao": "https://openrouter.ai/api/v1/chat/completions",
        "env_model": "OPENROUTER_MODEL",
        "modelo_padrao": "openrouter/free",
    },
]

_CACHE_DOSSIE: Dict[str, Dict[str, Any]] = {}

try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:

        class MemoriaMock:
            def __init__(self) -> None:
                self._dados: Dict[str, Any] = {}

            def ler_dados(self, chave: Any = None) -> Any:
                if chave and isinstance(chave, str):
                    return self._dados.get(chave)
                return self._dados

            def salvar_dados(self, chave: str, valor: Any) -> None:
                self._dados[chave] = valor

            def registrar(self, chave: str, valor: Any) -> None:
                self._dados[chave] = valor

        memoria = MemoriaMock()


def _resolver_gerador_master():
    """Carrega o compilador master sem quebrar caso a função tenha outro nome."""
    for mod_name in ("core.gerador_dossies_master", "gerador_dossies_master"):
        try:
            mod = __import__(mod_name, fromlist=["*"])
            for fn_name in (
                "compilar_dossies_com_biometria_e_json",
                "compilar_dossies_master",
            ):
                if hasattr(mod, fn_name) and callable(getattr(mod, fn_name)):
                    return getattr(mod, fn_name)
        except Exception:
            continue

    def _fallback_master(*args: Any, **kwargs: Any) -> Dict[str, str]:
        print("[GERADOR MASTER] Fallback ativo.")
        return {}

    return _fallback_master


executar_geracao_master = _resolver_gerador_master()


# --- SANITIZAÇÃO ---
def _sanitizar_texto_base(texto: str, max_chars: Optional[int] = None) -> str:
    """Remove caracteres de controle perigosos/inválidos e normaliza UTF-8."""
    if not isinstance(texto, str):
        texto = str(texto or "")
    limpo = texto.encode("utf-8", errors="ignore").decode("utf-8")
    limpo = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", limpo)
    limpo = re.sub(
        r"<\s*(script|style)[^>]*>.*?<\s*/\s*\1\s*>",
        "",
        limpo,
        flags=re.IGNORECASE | re.DOTALL,
    )
    limpo = limpo.strip()
    if max_chars is not None and max_chars > 0 and len(limpo) > max_chars:
        limpo = limpo[:max_chars] + "... [SANITIZADO/TRUNCADO]"
    return limpo


def _sanitizar_payload(dados: Any, max_chars: int = 5000) -> str:
    """Serializa e sanitiza os dados da memória para envio seguro."""
    try:
        if isinstance(dados, (dict, list)):
            bruto = json.dumps(dados, ensure_ascii=False, default=str)
        else:
            bruto = str(dados)
    except Exception:
        bruto = str(dados)
    return _sanitizar_texto_base(bruto, max_chars=max_chars)


def _sanitizar_saida(texto: str) -> str:
    """Sanitiza o texto gerado antes de salvar na memória e enviar ao PDF."""
    limpo = _sanitizar_texto_base(texto, max_chars=None)
    limpo = re.sub(r"\n{4,}", "\n\n\n", limpo)
    return limpo


def consolidar_dados_memoria() -> Any:
    if hasattr(memoria, "ler_dados"):
        return memoria.ler_dados()
    return {}


def salvar_na_memoria_comum(chave: str, valor: Any) -> None:
    if hasattr(memoria, "salvar_dados"):
        memoria.salvar_dados(chave, valor)
    elif hasattr(memoria, "registrar"):
        memoria.registrar(chave, valor)
    elif hasattr(memoria, "_dados") and isinstance(memoria._dados, dict):
        memoria._dados[chave] = valor


def obter_chave_gemini() -> Optional[str]:
    chave = (
        os.environ.get("GEMINI_API_KEY", "").strip()
        or os.environ.get("GOOGLE_API_KEY", "").strip()
    )
    return chave or None


def _json_contingencia(idioma_limpo: str, rotulo_horizontes: str) -> Dict[str, str]:
    if idioma_limpo == "EN":
        return {
            "diagnostico_estrutural": (
                f"Structural geometry and proportional balance compiled directly from "
                f"computed baseline parameters across {rotulo_horizontes}."
            ),
            "analise_dermica_hsv": (
                "Surface reflectance, chromatic balance, and environmental telemetry "
                "consolidated from verified local measurements with full integrity."
            ),
            "projecao_temporal": (
                f"Longitudinal evolution mapped for {rotulo_horizontes} based on "
                "deterministic calculation models and baseline telemetry."
            ),
            "recomendacao_tecnica": (
                f"Structured maintenance and periodic review cadence established for "
                f"{rotulo_horizontes} in alignment with calculated parameters."
            ),
        }
    return {
        "diagnostico_estrutural": (
            f"Leitura geométrica e equilíbrio estrutural consolidados a partir dos "
            f"parâmetros calculados para os horizontes de {rotulo_horizontes}."
        ),
        "analise_dermica_hsv": (
            "Leitura cromática, refletância de superfície e parâmetros ambientais "
            "registrados a partir da telemetria apurada com integridade preservada."
        ),
        "projecao_temporal": (
            f"Evolução longitudinal estruturada para {rotulo_horizontes} com base "
            "nos modelos determinísticos e nos dados calculados."
        ),
        "recomendacao_tecnica": (
            f"Diretrizes técnicas de acompanhamento e revisão periódica alinhadas "
            f"aos parâmetros apurados para {rotulo_horizontes}."
        ),
    }


def _extrair_json_4_chaves(
    texto_bruto: str,
    idioma_limpo: str,
    rotulo_horizontes: str,
) -> Dict[str, str]:
    """Extrai e normaliza o JSON nas 4 chaves obrigatórias a partir da resposta do LLM."""
    base_fallback = _json_contingencia(idioma_limpo, rotulo_horizontes)
    if not texto_bruto or not texto_bruto.strip():
        return base_fallback

    limpo = texto_bruto.strip()
    # Remove cercas de código ```json ... ```
    limpo = re.sub(r"^```(?:json)?\s*", "", limpo, flags=re.IGNORECASE)
    limpo = re.sub(r"\s*```$", "", limpo)

    candidatos: List[str] = [limpo]
    match_bloco = re.search(r"\{.*\}", limpo, flags=re.DOTALL)
    if match_bloco:
        candidatos.insert(0, match_bloco.group(0))

    for candidato in candidatos:
        try:
            parsed = json.loads(candidato)
            if isinstance(parsed, dict):
                resultado: Dict[str, str] = {}
                for chave in CHAVES_JSON_DOSSIE:
                    valor = parsed.get(chave)
                    if isinstance(valor, (dict, list)):
                        texto_val = json.dumps(valor, ensure_ascii=False)
                    else:
                        texto_val = str(valor or "").strip()
                    resultado[chave] = _sanitizar_saida(texto_val) or base_fallback[chave]
                return resultado
        except Exception:
            continue

    # Caso venha texto corrido sem JSON válido, aproveita o conteúdo sanitizado e completa faltantes
    texto_limpo = _sanitizar_saida(limpo)
    return {
        "diagnostico_estrutural": texto_limpo or base_fallback["diagnostico_estrutural"],
        "analise_dermica_hsv": base_fallback["analise_dermica_hsv"],
        "projecao_temporal": base_fallback["projecao_temporal"],
        "recomendacao_tecnica": base_fallback["recomendacao_tecnica"],
    }


def _formatar_dossie_legivel(secoes: Dict[str, str], idioma_limpo: str) -> str:
    """Formata as 4 seções em texto estruturado para exibição e injeção no gerador de PDF."""
    if idioma_limpo == "EN":
        titulos = {
            "diagnostico_estrutural": "1. STRUCTURAL DIAGNOSTIC",
            "analise_dermica_hsv": "2. DERMAL & HSV ANALYSIS",
            "projecao_temporal": "3. TEMPORAL PROJECTION",
            "recomendacao_tecnica": "4. TECHNICAL RECOMMENDATION",
        }
    else:
        titulos = {
            "diagnostico_estrutural": "1. DIAGNÓSTICO ESTRUTURAL",
            "analise_dermica_hsv": "2. ANÁLISE DÉRMICA E HSV",
            "projecao_temporal": "3. PROJEÇÃO TEMPORAL",
            "recomendacao_tecnica": "4. RECOMENDAÇÃO TÉCNICA",
        }

    blocos = []
    for chave in CHAVES_JSON_DOSSIE:
        conteudo = _sanitizar_saida(secoes.get(chave, ""))
        blocos.append(f"### {titulos[chave]}\n{conteudo}")
    return "\n\n".join(blocos)


def _criar_cliente_rapido(chave_api: str) -> genai.Client:
    try:
        http_opts = types.HttpOptions(timeout=int(TIMEOUT_REQUISICAO_SEGUNDOS))
        return genai.Client(api_key=chave_api, http_options=http_opts)
    except Exception:
        return genai.Client(api_key=chave_api)


def _tentar_gemini(prompt_master: str, idioma_limpo: str, max_tentativas: int) -> Optional[str]:
    chave_final = obter_chave_gemini()
    if not chave_final:
        print("[AVISO AMBIENTE/CHAVE] Chave Gemini não encontrada; pulando cadeia Gemini.")
        return None

    client = _criar_cliente_rapido(chave_final)
    limite_tentativas = max(1, int(max_tentativas))

    for indice_modelo, modelo_atual in enumerate(MODELOS_GEMINI):
        tentativa = 1
        while tentativa <= limite_tentativas:
            try:
                print(
                    f"\n[INFO] Gemini [{modelo_atual}] [LANG: {idioma_limpo}] "
                    f"(Tentativa {tentativa}/{limite_tentativas}, timeout={TIMEOUT_REQUISICAO_SEGUNDOS}s)..."
                )
                response = client.models.generate_content(
                    model=modelo_atual,
                    contents=prompt_master,
                )
                texto_cru = getattr(response, "text", None)
                if texto_cru is not None and str(texto_cru).strip():
                    return _sanitizar_saida(str(texto_cru))
                raise ValueError("Resposta vazia retornada pelo modelo Gemini.")
            except Exception as e:
                print(f"[AVISO DE REDE] Falha em {modelo_atual}: {e}")
                if tentativa < limite_tentativas:
                    time.sleep(0.5)
                tentativa += 1

        if indice_modelo < len(MODELOS_GEMINI) - 1:
            print(f"[INFO] Alternando de '{modelo_atual}' para '{MODELOS_GEMINI[indice_modelo + 1]}'...")

    return None


def _tentar_provedor_openai_compativel(
    cfg: Dict[str, str],
    prompt_master: str,
    idioma_limpo: str,
) -> Optional[str]:
    chave = os.environ.get(cfg["env_key"], "").strip()
    if not chave:
        return None

    url = os.environ.get(cfg["env_url"], "").strip() or cfg["url_padrao"]
    modelo = os.environ.get(cfg["env_model"], "").strip() or cfg["modelo_padrao"]

    print(
        f"\n[INFO] Tentando provedor alternativo [{cfg['nome']} / {modelo}] "
        f"[LANG: {idioma_limpo}] (timeout={TIMEOUT_REQUISICAO_SEGUNDOS}s)..."
    )

    payload = {
        "model": modelo,
        "messages": [
            {"role": "user", "content": prompt_master},
        ],
        "temperature": 0.3,
    }

    req = urllib.request.Request(
        url=url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {chave}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_REQUISICAO_SEGUNDOS) as resp:
            corpo = resp.read().decode("utf-8", errors="ignore")
            dados_json = json.loads(corpo)
            escolhas = dados_json.get("choices") or []
            if escolhas:
                mensagem = (escolhas[0].get("message") or {}).get("content") or ""
                if mensagem.strip():
                    return _sanitizar_saida(mensagem)
        return None
    except urllib.error.HTTPError as e_http:
        print(f"[AVISO PROVEDOR {cfg['nome']}] HTTP {e_http.code}: {e_http.reason}")
        return None
    except Exception as e:
        print(f"[AVISO PROVEDOR {cfg['nome']}] Falha: {e}")
        return None


def gerar_secoes_dossie_json(
    lang: str = "PT",
    max_tentativas: int = 1,
    horizontes: List[int] = HORIZONTES_PROJECTION,
    dados_entrada: Optional[Any] = None,
) -> Tuple[Dict[str, str], Any]:
    """Gera as 4 seções estruturadas em JSON preservando os valores numéricos calculados."""
    dados_ecosistema = dados_entrada if dados_entrada is not None else consolidar_dados_memoria()
    idioma_limpo = str(lang).upper() if lang and isinstance(lang, str) else "PT"
    if idioma_limpo not in ("PT", "EN"):
        idioma_limpo = "PT"

    horizontes_lista = list(horizontes) if horizontes else list(HORIZONTES_PROJECTION)
    horizontes_texto = ", ".join(str(ano) for ano in horizontes_lista)
    rotulo_horizontes = f"{horizontes_texto} years" if idioma_limpo == "EN" else f"{horizontes_texto} anos"

    resumo_sanitizado = _sanitizar_payload(dados_ecosistema, max_chars=5000)

    chave_cache = hashlib.sha256(
        f"JSON4|{idioma_limpo}|{rotulo_horizontes}|{resumo_sanitizado}".encode("utf-8")
    ).hexdigest()

    if chave_cache in _CACHE_DOSSIE:
        secoes_cache = dict(_CACHE_DOSSIE[chave_cache])
        texto_cache = _formatar_dossie_legivel(secoes_cache, idioma_limpo)
        salvar_na_memoria_comum("secoes_dossie_json", secoes_cache)
        salvar_na_memoria_comum("analise_gemini_recente", texto_cache)
        salvar_na_memoria_comum("analise_gemini", texto_cache)
        salvar_na_memoria_comum("horizontes_projecao", horizontes_lista)
        return secoes_cache, dados_ecosistema

    diretriz_idioma = (
        "Write all JSON values strictly in fluent, high-level international English."
        if idioma_limpo == "EN"
        else "Escreva todos os valores do JSON estritamente em Português claro, elegante, preciso e executivo."
    )

    prompt_master = _sanitizar_texto_base(
        f"""
[DIRECTIVA SOBERANA: APEX PROTOCOL UHNW - REDACAO TECNICA]
{diretriz_idioma}

Papel: Redator técnico do Thierry Technology Concept Global.
Regras fundamentais:
1. Python já calculou os números e parâmetros; redija com clareza, elegância e fidelidade estrita aos valores fornecidos.
2. Não invente métricas, exames, patologias, condições clínicas ou procedimentos que não estejam explícitos nos dados.
3. Preserve exatamente os números, proporções, pontos, medidas (mm, mL, graus, %) e horizontes ({rotulo_horizontes}) presentes nos dados.

DADOS CONSOLIDADOS (SANITIZADOS):
{resumo_sanitizado}

Responda EXCLUSIVAMENTE com um objeto JSON válido contendo exatamente estas 4 chaves:
{{
  "diagnostico_estrutural": "...",
  "analise_dermica_hsv": "...",
  "projecao_temporal": "...",
  "recomendacao_tecnica": "..."
}}
""",
        max_chars=12000,
    )

    resposta_bruta: Optional[str] = _tentar_gemini(prompt_master, idioma_limpo, max_tentativas)

    if not resposta_bruta:
        for provedor in PROVEDORES_OPENAI_COMPATIVEIS:
            resposta_bruta = _tentar_provedor_openai_compativel(provedor, prompt_master, idioma_limpo)
            if resposta_bruta:
                break

    if not resposta_bruta:
        print(
            "\n[ALERTA CRÍTICO] Nenhuma IA externa respondeu a tempo. "
            "Ativando Contingência Soberana local em JSON..."
        )
        secoes_final = _json_contingencia(idioma_limpo, rotulo_horizontes)
    else:
        secoes_final = _extrair_json_4_chaves(resposta_bruta, idioma_limpo, rotulo_horizontes)

    _CACHE_DOSSIE[chave_cache] = dict(secoes_final)
    texto_formatado = _formatar_dossie_legivel(secoes_final, idioma_limpo)

    salvar_na_memoria_comum("secoes_dossie_json", secoes_final)
    salvar_na_memoria_comum("analise_gemini_recente", texto_formatado)
    salvar_na_memoria_comum("analise_gemini", texto_formatado)
    salvar_na_memoria_comum("horizontes_projecao", horizontes_lista)

    return secoes_final, dados_ecosistema


def gerar_dossie_com_gemini(
    lang: str = "PT",
    max_tentativas: int = 1,
    horizontes: List[int] = HORIZONTES_PROJECTION,
    dados_entrada: Optional[Any] = None,
) -> Tuple[str, Any]:
    """Mantém a assinatura original retornando o texto formatado das 4 seções e os dados."""
    idioma_limpo = str(lang).upper() if lang and isinstance(lang, str) else "PT"
    if idioma_limpo not in ("PT", "EN"):
        idioma_limpo = "PT"

    secoes_json, dados_ecosistema = gerar_secoes_dossie_json(
        lang=idioma_limpo,
        max_tentativas=max_tentativas,
        horizontes=horizontes,
        dados_entrada=dados_entrada,
    )
    return _formatar_dossie_legivel(secoes_json, idioma_limpo), dados_ecosistema


def disparar_compilacao_pdf(
    conteudo_llm: str,
    dados_memoria: Any,
    lang: str = "PT",
    horizontes: List[int] = HORIZONTES_PROJECTION,
    secoes_json: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    idioma_limpo = str(lang).upper() if lang and isinstance(lang, str) else "PT"
    if idioma_limpo not in ("PT", "EN"):
        idioma_limpo = "PT"

    conteudo_limpo = _sanitizar_saida(conteudo_llm)
    horizontes_lista = list(horizontes) if horizontes else list(HORIZONTES_PROJECTION)
    print(f"\n[INFO] Injetando a inteligência sanitizada no Gerador de PDF Master [LANG: {idioma_limpo}]...")

    secoes_ativas = secoes_json
    if not secoes_ativas and isinstance(dados_memoria, dict):
        candidata = dados_memoria.get("secoes_dossie_json")
        if isinstance(candidata, dict):
            secoes_ativas = candidata

    telemetria_payload: Dict[str, Any] = {
        "analise_gemini": conteudo_limpo,
        "analise_gemini_recente": conteudo_limpo,
        "memoria_sistema": dados_memoria,
        "horizontes_anos": horizontes_lista,
    }
    if secoes_ativas:
        telemetria_payload["secoes_json"] = secoes_ativas
        telemetria_payload.update(secoes_ativas)

    try:
        resultados = executar_geracao_master(
            ceo_name="Genilson Rodrigues",
            company_name="Thierry Technology Concept Global",
            market_segment="Tecnologia e Inovação",
            horizon_years=horizontes_lista,
            operador="THIERRY (TCC SOBERANO)",
            telemetria_dinamica=telemetria_payload,
            lang=idioma_limpo,
        )
        return resultados if isinstance(resultados, dict) else {}
    except TypeError:
        try:
            resultados = executar_geracao_master(
                ceo_name="Genilson Rodrigues",
                company_name="Thierry Technology Concept Global",
                market_segment="Tecnologia e Inovação",
                horizon_years=horizontes_lista[-1],
                operador="THIERRY (TCC SOBERANO)",
                telemetria_dinamica=telemetria_payload,
                lang=idioma_limpo,
            )
            return resultados if isinstance(resultados, dict) else {}
        except Exception as e_inner:
            print(f"[ERRO NA COMPILAÇÃO DO PDF] {e_inner}")
            return {}
    except Exception as e:
        print(f"[ERRO NA COMPILAÇÃO DO PDF] {e}")
        return {}


if __name__ == "__main__":
    print("\n" + "═" * 70)
    print("   GERADOR DE DOSSIÊS EXECUTIVOS UHNW - MULTI-IA & SANITIZAÇÃO")
    print("═" * 70)

    idioma_bruto = "PT"
    if hasattr(memoria, "ler_dados"):
        res_mem = memoria.ler_dados("lang")
        if res_mem and isinstance(res_mem, str):
            idioma_bruto = res_mem

    idioma_execucao: str = str(idioma_bruto).upper()
    if idioma_execucao not in ("PT", "EN"):
        idioma_execucao = "PT"

    try:
        secoes_geradas, dados_memoria = gerar_secoes_dossie_json(
            lang=idioma_execucao,
            max_tentativas=1,
            horizontes=HORIZONTES_PROJECTION,
        )
        dossie_texto = _formatar_dossie_legivel(secoes_geradas, idioma_execucao)

        print("\n" + "─" * 70)
        print(f"JSON ESTRUTURADO [{idioma_execucao}]:")
        print("─" * 70)
        print(json.dumps(secoes_geradas, ensure_ascii=False, indent=2))

        print("\n" + "─" * 70)
        print(f"DOSSIÊ EXECUTIVO PRONTO [{idioma_execucao}]:")
        print("─" * 70)
        print(dossie_texto)
        print("═" * 70)

        arquivos_gerados = disparar_compilacao_pdf(
            dossie_texto,
            dados_memoria,
            lang=idioma_execucao,
            horizontes=HORIZONTES_PROJECTION,
            secoes_json=secoes_geradas,
        )

        print("\n" + "─" * 70)
        print("STATUS DA GRAVAÇÃO DOS ARQUIVOS NA PASTA PDFs FINAIS:")
        print("─" * 70)
        for chave, caminho in arquivos_gerados.items():
            print(f" 📂 [{chave}] PDF salvo em: {caminho}")
        print("═" * 70 + "\n")

    except Exception as e:
        print(f"\n[ERRO NA EXECUÇÃO] {e}")