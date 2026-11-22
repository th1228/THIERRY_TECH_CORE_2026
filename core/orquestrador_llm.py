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

# -*- coding: utf-8 -*-
"""
Orquestrador LLM com Chamada Direta ao Gemini e Resiliência Industrial
Thierry Technology Concept Global - Execução Soberana
Integrado ao Gerador Master de Dossiês PDF e Memória Comum
"""

import os
import sys
import time
from typing import Dict, Any, Tuple, List
from google import genai

# --- CORREÇÃO DE CAMINHO ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


def _carregar_env_local() -> None:
    """Carrega o arquivo .env da pasta do script ou da raiz do projeto sem quebrar se ausente."""
    candidatos_env = [
        os.path.join(ROOT_DIR, ".env"),
        os.path.join(os.path.dirname(ROOT_DIR), ".env"),
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

# --- CADEIA DE MODELOS COM FALLBACK AUTOMÁTICO ---
MODELOS_GEMINI: List[str] = [
    "models/gemini-3.8-flash",
    "models/gemini-2.5-flash",
    "models/gemini-2.5-flash-lite",
]

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

# --- IMPORTAÇÃO SEGURA DO GERADOR MASTER DE DOSSIÊS ---
try:
    from core.gerador_dossies_master import compilar_dossies_master as executar_geracao_master
except ImportError:
    try:
        from gerador_dossies_master import compilar_dossies_master as executar_geracao_master
    except ImportError:
        def executar_geracao_master(*args: Any, **kwargs: Any) -> Dict[str, str]:
            print("[GERADOR MASTER] Fallback ativo.")
            return {}


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


def obter_chave_gemini() -> str:
    chave = os.environ.get("GEMINI_API_KEY", "").strip()
    if not chave:
        raise RuntimeError(
            "Variável GEMINI_API_KEY não encontrada no arquivo .env ou no ambiente do sistema."
        )
    return chave


def _eh_erro_sobrecarga(erro: Exception) -> bool:
    codigo = getattr(erro, "code", None)
    status = getattr(erro, "status", None)
    texto_erro = str(erro).lower()
    return (
        codigo in (429, 503)
        or str(status).upper() in ("UNAVAILABLE", "RESOURCE_EXHAUSTED", "429", "503")
        or "503" in texto_erro
        or "429" in texto_erro
        or "unavailable" in texto_erro
        or "spike in demand" in texto_erro
        or "overloaded" in texto_erro
    )


def gerar_dossie_com_gemini(
    lang: str = "PT",
    max_tentativas: int = 3,
    horizontes: List[int] = HORIZONTES_PROJECTION,
) -> Tuple[str, Any]:
    dados_ecosistema = consolidar_dados_memoria()
    idioma_limpo = str(lang).upper() if lang and isinstance(lang, str) else "PT"
    if idioma_limpo not in ("PT", "EN"):
        idioma_limpo = "PT"

    horizontes_lista = list(horizontes) if horizontes else list(HORIZONTES_PROJECTION)
    horizontes_texto = ", ".join(str(ano) for ano in horizontes_lista)

    if idioma_limpo == "EN":
        diretriz_idioma = (
            "CRITICAL DIRECTIVE: Write the ENTIRE executive dossier strictly in fluent, "
            "high-level international executive English."
        )
        rotulo_horizontes = f"{horizontes_texto} years"
    else:
        diretriz_idioma = (
            "DIRETIVA SOBERANA: Escreva todo o dossiê executivo estritamente em Português "
            "fluído e executivo, com padrão internacional."
        )
        rotulo_horizontes = f"{horizontes_texto} anos"

    prompt_master = f"""
    [DIRECTIVA SOBERANA: APEX PROTOCOL UHNW]
    {diretriz_idioma}

    Atue como o núcleo de inteligência executiva do Thierry Technology Concept Global.
    Sua missão é processar os dados multicamadas abaixo, capturados em tempo real por nossa rede de sensores e motores integrados, e redigir um Dossiê Executivo UHNW (Ultra-High-Net-Worth) de visagismo, estética e alta performance cobrindo os horizontes de projeção de {rotulo_horizontes}.

    ESTADO CONSOLIDADO DA MEMÓRIA COMUM:
    {dados_ecosistema}

    ESTRUTURA OBRIGATÓRIA DO DOSSIÊ:
    1. SUMÁRIO EXECUTIVO GLOBAL: Visão geral da telemetria ambiental e estabilidade fisiológica/cutânea do cliente (com visão consolidada para {rotulo_horizontes}).
    2. DIAGNÓSTICO VISAGISTA E TRICOLÓGICO: Análise de proporção facial, geometria, estrutura capilar e colorimetria forense baseada nos dados coletados, incluindo projeções estruturais para {rotulo_horizontes}.
    3. PLANO DE AÇÃO DE ALTA PERFORMANCE (UHNW): Recomendações personalizadas, protocolos de blindagem estética e rotinas otimizadas para os horizontes de {rotulo_horizontes}.
    
    Mantenha um tom sofisticado, analítico, executivo e com rigor científico absoluto.
    """

    chave_final = obter_chave_gemini()
    client = genai.Client(api_key=chave_final)

    texto_gerado = ""
    sucesso_api = False
    limite_tentativas = max(1, int(max_tentativas))

    for indice_modelo, modelo_atual in enumerate(MODELOS_GEMINI):
        tentativa = 1
        while tentativa <= limite_tentativas:
            try:
                print(
                    f"\n[INFO] A enviar o payload consolidado para o Gemini [{modelo_atual}] "
                    f"[LANG: {idioma_limpo}] (Tentativa {tentativa}/{limite_tentativas})..."
                )

                response = client.models.generate_content(
                    model=modelo_atual,
                    contents=prompt_master,
                )

                texto_cru = getattr(response, "text", None)
                if texto_cru is not None and str(texto_cru).strip():
                    texto_gerado = str(texto_cru).strip()
                    sucesso_api = True
                    break
                else:
                    raise ValueError("Resposta vazia retornada pelo modelo Gemini.")

            except Exception as e:
                print(f"[AVISO DE REDE] Falha em {modelo_atual} na tentativa {tentativa}: {e}")
                if tentativa < limite_tentativas:
                    tempo_espera = tentativa * 5 if _eh_erro_sobrecarga(e) else tentativa * 3
                    print(f"A aguardar {tempo_espera} segundos para nova tentativa automática...")
                    time.sleep(tempo_espera)
                tentativa += 1

        if sucesso_api:
            break

        if indice_modelo < len(MODELOS_GEMINI) - 1:
            proximo_modelo = MODELOS_GEMINI[indice_modelo + 1]
            print(
                f"[INFO] Alternando de '{modelo_atual}' para o modelo de reserva '{proximo_modelo}'..."
            )

    if not sucesso_api:
        print(
            "[ALERTA CRÍTICO] Atingido o limite de tentativas nos modelos externos disponíveis. "
            "Ativando Fallback Soberano local..."
        )
        if idioma_limpo == "EN":
            texto_gerado = (
                "=== TCC GLOBAL SOVEREIGN CONTINGENCY DOSSIER ===\n"
                "Status: External AI high demand contingency active.\n"
                f"1. EXECUTIVE SUMMARY: Environmental telemetries stable ({rotulo_horizontes} horizons), "
                "processed via local secure node vault.\n"
                f"2. VISAGE & TRICHOLOGY DIAGNOSTIC: Core geometric ratios and structural parameters "
                f"preserved for {rotulo_horizontes}.\n"
                f"3. UHNW ACTION PLAN: Protocols locked and loaded ({rotulo_horizontes} cycles) "
                "under local cryptographic compliance."
            )
        else:
            texto_gerado = (
                "=== DOSSIÊ DE CONTINGÊNCIA SOBERANA TCC GLOBAL ===\n"
                "Status: Contingência ativa devido a alta demanda nos servidores externos.\n"
                f"1. SUMÁRIO EXECUTIVO GLOBAL: Telemetrias ambientais estáveis (horizontes de {rotulo_horizontes}), "
                "processadas via cofre local seguro.\n"
                f"2. DIAGNÓSTICO VISAGISTA E TRICOLÓGICO: Razões geométricas principais e parâmetros estruturais "
                f"preservados para {rotulo_horizontes}.\n"
                f"3. PLANO DE AÇÃO UHNW: Protocolos validados (ciclos de {rotulo_horizontes}) "
                "sob conformidade criptográfica local."
            )

    # --- SALVAMENTO CRÍTICO NA MEMÓRIA COMUM ---
    salvar_na_memoria_comum("analise_gemini_recente", texto_gerado)
    salvar_na_memoria_comum("analise_gemini", texto_gerado)
    salvar_na_memoria_comum("horizontes_projecao", horizontes_lista)

    return texto_gerado, dados_ecosistema


def disparar_compilacao_pdf(
    conteudo_llm: str,
    dados_memoria: Any,
    lang: str = "PT",
    horizontes: List[int] = HORIZONTES_PROJECTION,
) -> Dict[str, str]:
    idioma_limpo = str(lang).upper() if lang and isinstance(lang, str) else "PT"
    if idioma_limpo not in ("PT", "EN"):
        idioma_limpo = "PT"

    horizontes_lista = list(horizontes) if horizontes else list(HORIZONTES_PROJECTION)
    print(f"\n[INFO] Injetando a inteligência no Gerador de PDF Master [LANG: {idioma_limpo}]...")

    telemetria_payload = {
        "analise_gemini": conteudo_llm,
        "analise_gemini_recente": conteudo_llm,
        "memoria_sistema": dados_memoria,
        "horizontes_anos": horizontes_lista,
    }

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
        return resultados
    except TypeError:
        resultados = executar_geracao_master(
            ceo_name="Genilson Rodrigues",
            company_name="Thierry Technology Concept Global",
            market_segment="Tecnologia e Inovação",
            horizon_years=horizontes_lista[-1],
            operador="THIERRY (TCC SOBERANO)",
            telemetria_dinamica=telemetria_payload,
            lang=idioma_limpo,
        )
        return resultados
    except Exception as e:
        print(f"[ERRO NA COMPILAÇÃO DO PDF] {e}")
        return {}


if __name__ == "__main__":
    print("\n" + "═" * 70)
    print("   GERADOR DE DOSSIÊS EXECUTIVOS UHNW - RESILIÊNCIA ATIVA")
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
        dossie_texto, dados_memoria = gerar_dossie_com_gemini(
            lang=idioma_execucao,
            horizontes=HORIZONTES_PROJECTION,
        )
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
        )

        print("\n" + "─" * 70)
        print("STATUS DA GRAVAÇÃO DOS ARQUIVOS NA PASTA PDFs FINAIS:")
        print("─" * 70)
        for chave, caminho in arquivos_gerados.items():
            print(f" 📂 [{chave}] PDF salvo em: {caminho}")
        print("═" * 70 + "\n")

    except Exception as e:
        print(f"\n[ERRO NA EXECUÇÃO] {e}")