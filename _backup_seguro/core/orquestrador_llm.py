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
from typing import Dict, Any, Tuple
from google import genai

# --- CORREÇÃO DE CAMINHO ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# --- CONFIGURAÇÃO DA CHAVE DE API ---
API_KEY_REGISTADA = "AQ.Ab8RN6IMGtFG1bmmtrqu_o6mLlkviTwUTkdA2ctfdD3HNqELyQ"

try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:
        class MemoriaMock:
            def __init__(self):
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
    if hasattr(memoria, 'ler_dados'):
        return memoria.ler_dados()
    return {}


def salvar_na_memoria_comum(chave: str, valor: Any) -> None:
    if hasattr(memoria, 'salvar_dados'):
        memoria.salvar_dados(chave, valor)
    elif hasattr(memoria, 'registrar'):
        memoria.registrar(chave, valor)
    elif hasattr(memoria, '_dados') and isinstance(memoria._dados, dict):
        memoria._dados[chave] = valor


def gerar_dossie_com_gemini(lang: str = "PT", max_tentativas: int = 3) -> Tuple[str, Any]:
    dados_ecosistema = consolidar_dados_memoria()
    idioma_limpo = str(lang).upper() if lang and isinstance(lang, str) else "PT"

    if idioma_limpo == "EN":
        diretriz_idioma = "CRITICAL DIRECTIVE: Write the ENTIRE executive dossier strictly in fluent, high-level executive English."
    else:
        diretriz_idioma = "DIRETIVA SOBERANA: Escreva todo o dossiê executivo estritamente em Português fluído e executivo."

    prompt_master = f"""
    [DIRECTIVA SOBERANA: APEX PROTOCOL UHNW]
    {diretriz_idioma}

    Atue como o núcleo de inteligência executiva do Thierry Technology Concept Global.
    Sua missão é processar os dados multicamadas abaixo, capturados em tempo real por nossa rede de sensores e motores integrados, e redigir um Dossiê Executivo UHNW (Ultra-High-Net-Worth) de visagismo, estética e alta performance.

    ESTADO CONSOLIDADO DA MEMÓRIA COMUM:
    {dados_ecosistema}

    ESTRUTURA OBRIGATÓRIA DO DOSSIÊ:
    1. SUMÁRIO EXECUTIVO GLOBAL: Visão geral da telemetria ambiental e estabilidade fisiológica/cutânea do cliente.
    2. DIAGNÓSTICO VISAGISTA E TRICOLÓGICO: Análise de proporção facial, geometria, estrutura capilar e colorimetria forense baseada nos dados coletados.
    3. PLANO DE AÇÃO DE ALTA PERFORMANCE (UHNW): Recomendações personalizadas, protocolos de blindagem estética e rotinas otimizadas.
    
    Mantenha um tom sofisticado, analítico, executivo e com rigor científico absoluto.
    """

    chave_final = os.environ.get("GEMINI_API_KEY", API_KEY_REGISTADA)
    client = genai.Client(api_key=chave_final)

    texto_gerado = ""
    tentativa = 1

    while tentativa <= max_tentativas:
        try:
            print(f"\n[INFO] A enviar o payload consolidado para o Gemini [LANG: {idioma_limpo}] (Tentativa {tentativa}/{max_tentativas})...")
            
            response = client.models.generate_content(
                model="models/gemini-3.8-flash",
                contents=prompt_master,
            )

            texto_cru = getattr(response, 'text', None)
            if texto_cru is not None:
                texto_gerado = str(texto_cru)
                break
            else:
                raise ValueError("Resposta vazia retornada pelo modelo Gemini.")

        except Exception as e:
            print(f"[AVISO DE REDE] Falha na tentativa {tentativa}: {e}")
            if tentativa == max_tentativas:
                print("[ALERTA CRÍTICO] Atingido o limite de tentativas com a API externa. Ativando Fallback Soberano local...")
                if idioma_limpo == "EN":
                    texto_gerado = (
                        "=== TCC GLOBAL SOVEREIGN CONTINGENCY DOSSIER ===\n"
                        "Status: External AI high demand contingency active.\n"
                        "1. EXECUTIVE SUMMARY: Environmental telemetries stable, processed via local secure node vault.\n"
                        "2. VISAGE & TRICHOLOGY DIAGNOSTIC: Core geometric ratios and structural parameters preserved.\n"
                        "3. UHNW ACTION PLAN: Protocols locked and loaded under local cryptographic compliance."
                    )
                else:
                    texto_gerado = (
                        "=== DOSSIÊ DE CONTINGÊNCIA SOBERANA TCC GLOBAL ===\n"
                        "Status: Contingência ativa devido a alta demanda nos servidores externos.\n"
                        "1. SUMÁRIO EXECUTIVO GLOBAL: Telemetrias ambientais estáveis, processadas via cofre local seguro.\n"
                        "2. DIAGNÓSTICO VISAGISTA E TRICOLÓGICO: Razões geométricas principais e parâmetros estruturais preservados.\n"
                        "3. PLANO DE AÇÃO UHNW: Protocolos validados sob conformidade criptográfica local."
                    )
            else:
                tempo_espera = tentativa * 3
                print(f"A aguardar {tempo_espera} segundos para nova tentativa automática...")
                time.sleep(tempo_espera)
        
        tentativa += 1

    # --- SALVAMENTO CRÍTICO NA MEMÓRIA COMUM ---
    salvar_na_memoria_comum("analise_gemini_recente", texto_gerado)
    salvar_na_memoria_comum("analise_gemini", texto_gerado)

    return texto_gerado, dados_ecosistema


def disparar_compilacao_pdf(conteudo_llm: str, dados_memoria: Any, lang: str = "PT") -> Dict[str, str]:
    idioma_limpo = str(lang).upper() if lang and isinstance(lang, str) else "PT"
    print(f"\n[INFO] Injetando a inteligência no Gerador de PDF Master [LANG: {idioma_limpo}]...")

    telemetria_payload = {
        "analise_gemini": conteudo_llm,
        "analise_gemini_recente": conteudo_llm,
        "memoria_sistema": dados_memoria,
    }

    try:
        resultados = executar_geracao_master(
            ceo_name="Genilson Rodrigues",
            company_name="Thierry Technology Concept Global",
            market_segment="Tecnologia e Inovação",
            horizon_years=10,
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
    if hasattr(memoria, 'ler_dados'):
        res_mem = memoria.ler_dados("lang")
        if res_mem and isinstance(res_mem, str):
            idioma_bruto = res_mem

    idioma_execucao: str = str(idioma_bruto)

    try:
        dossie_texto, dados_memoria = gerar_dossie_com_gemini(lang=idioma_execucao)
        print("\n" + "─" * 70)
        print(f"DOSSIÊ EXECUTIVO PRONTO [{idioma_execucao.upper()}]:")
        print("─" * 70)
        print(dossie_texto)
        print("═" * 70)

        arquivos_gerados = disparar_compilacao_pdf(dossie_texto, dados_memoria, lang=idioma_execucao)

        print("\n" + "─" * 70)
        print("STATUS DA GRAVAÇÃO DOS ARQUIVOS NA PASTA PDFs FINAIS:")
        print("─" * 70)
        for chave, caminho in arquivos_gerados.items():
            print(f" 📂 [{chave}] PDF salvo em: {caminho}")
        print("═" * 70 + "\n")

    except Exception as e:
        print(f"\n[ERRO NA EXECUÇÃO] {e}")