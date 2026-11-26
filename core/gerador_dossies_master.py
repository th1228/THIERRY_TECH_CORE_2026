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
Módulo Mestre: gerador_dossies_master.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Versão: 6.9.6 - DINÂMICO, SOBERANO, ROTEADO POR DOMÍNIO E BILÍNGUE (PT / EN)
Descrição: Orquestrador Mestre dinâmico com integração direta à memória comum,
           telemetria/LLM, roteamento isolado por motor (executivo/cronoestética,
           financeiro, tricologia e diplomacia) e evolução longitudinal (5, 10 e 15 anos).
"""

import copy
import datetime
import os
import re
import sys
import traceback
from typing import Any, Callable, Dict, List, Optional

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

for _caminho in (ROOT_DIR, CURRENT_DIR):
    if _caminho and os.path.isdir(_caminho) and _caminho not in sys.path:
        sys.path.insert(0, _caminho)

# --- PONTE DE MEMÓRIA AUTOMÁTICA (THIERRY TECH) ---
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:

        class MemoriaMock:
            def __init__(self) -> None:
                self._dados: Dict[str, Any] = {}

            def salvar_dados(self, chave: str, valor: Any) -> bool:
                self._dados[chave] = valor
                return True

            def registrar(self, chave: str, valor: Any) -> bool:
                self._dados[chave] = valor
                return True

            def ler_dados(self, chave: Optional[str] = None) -> Any:
                if chave is None:
                    return copy.deepcopy(self._dados)
                return copy.deepcopy(self._dados.get(chave))

            def obter_para_destino(self, destino: str, chave: Optional[str] = None) -> Any:
                return self.ler_dados(chave)

        memoria = MemoriaMock()
# ---------------------------------------------------

MOTORES_STATUS: Dict[str, str] = {}

obter_evolucao_titular: Any = None
try:
    from core.diagnostico_evolucao import obter_evolucao_titular as _obt_evo_titular  # type: ignore
    obter_evolucao_titular = _obt_evo_titular
except ImportError:
    obter_evolucao_titular = None

try:
    from core.c2_sovereign_intelligence import C2SovereignIntelligenceEngine  # type: ignore
    MOTORES_STATUS["Motor 1"] = "OK"
except ImportError as e:
    MOTORES_STATUS["Motor 1"] = f"Indisponível ({e})"

try:
    from core.super_retorno_financeiro import C2SovereignROIEngine  # type: ignore
    MOTORES_STATUS["Motor 2"] = "OK"
except ImportError as e:
    MOTORES_STATUS["Motor 2"] = f"Indisponível ({e})"

try:
    from core.tricologia_ultra_avancada import C2UltraAdvancedTrichologyEngine  # type: ignore
    MOTORES_STATUS["Motor 3"] = "OK"
except ImportError as e:
    MOTORES_STATUS["Motor 3"] = f"Indisponível ({e})"

try:
    from core.carta_internacional_engine import CartaInternacionalEngine  # type: ignore
    MOTORES_STATUS["Motor 4"] = "OK"
except ImportError as e:
    MOTORES_STATUS["Motor 4"] = f"Indisponível ({e})"

try:
    from core.monaco_modelagem_engine import C2MonacoModelingEngine  # type: ignore
    MOTORES_STATUS["Motor 5"] = "OK"
except ImportError as e:
    MOTORES_STATUS["Motor 5"] = f"Indisponível ({e})"

try:
    from legal.contrato_global_engine import C2GlobalContractEngine  # type: ignore
    MOTORES_STATUS["Motor 6"] = "OK (Via /legal)"
except ImportError:
    try:
        from core.contrato_global_engine import C2GlobalContractEngine  # type: ignore
        MOTORES_STATUS["Motor 6"] = "OK (Via /core)"
    except ImportError as e:
        MOTORES_STATUS["Motor 6"] = f"Indisponível ({e})"


PALAVRAS_TRICOLOGIA = (
    "tricologia",
    "capilar",
    "cabelo",
    "fios",
    "densidade capilar",
    "área t",
    "area t",
    "couro cabeludo",
    "folículo",
    "foliculo",
    "alopecia",
    "eflúvio",
    "efluvio",
    "micropigmentação",
    "micropigmentacao",
    "selamento de fios",
    "queda capilar",
)

PALAVRAS_FINANCEIRO = (
    "financeiro",
    "retorno",
    "roi",
    "valuation",
    "valuación",
    "orçamento",
    "orcamento",
    "custo",
    "receita",
    "margem",
    "patrimônio",
    "patrimonio",
    "licenciamento",
    "investimento",
    "econômic",
    "economic",
)

CHAVES_LLM_E_SECOES = (
    "analise_gemini",
    "analise_gemini_recente",
    "analise_gemini_carta",
    "parecer_carta",
    "secoes_dossie_json",
    "secoes_json",
    "diagnostico_estrutural",
    "analise_dermica_hsv",
    "projecao_temporal",
    "recomendacao_tecnica",
    "secao_tricologia",
    "dados_tricologia_isolados",
    "secao_financeiro",
    "contexto_biometrico_parametrico",
    "evolucao_longitudinal",
    "projecao_ciclos",
)

_REGEX_REMOVER_HERPES = re.compile(
    r"[^.!?\n\r;]*\b(?:herpes|simplex\s+vir(?:al|ale))\b[^.!?\n\r;]*[.!?;]?",
    flags=re.IGNORECASE,
)


def _ler_memoria_segura(chave: Optional[str] = None, destino: Optional[str] = None) -> Any:
    """Lê diretamente da memória comum usando o roteamento por destino quando disponível."""
    try:
        if destino and hasattr(memoria, "obter_para_destino"):
            return memoria.obter_para_destino(destino, chave)
        if hasattr(memoria, "ler_dados"):
            return memoria.ler_dados(chave)
        if chave and hasattr(memoria, "obter_dados"):
            return memoria.obter_dados(chave)
    except Exception:
        pass
    return {} if chave is None else None


def _sanitizar_sem_herpes(texto: str) -> str:
    if not isinstance(texto, str) or not texto.strip():
        return texto
    limpo = _REGEX_REMOVER_HERPES.sub("", texto)
    limpo = re.sub(r"\s*-\s*-\s*", " - ", limpo)
    limpo = re.sub(r"[ \t]{2,}", " ", limpo)
    limpo = re.sub(r"\n{3,}", "\n\n", limpo)
    return limpo.strip()


def limpar_markdown_para_pdf(texto_cru: str) -> str:
    if not isinstance(texto_cru, str):
        texto_cru = str(texto_cru)

    texto = re.sub(r"#{1,6}\s*", "", texto_cru)
    texto = re.sub(r"\*\*", "", texto)
    texto = re.sub(r"\*", "", texto)
    texto = re.sub(r"---+", "", texto)
    texto = _sanitizar_sem_herpes(texto)

    return texto.strip()


def _filtrar_sentencas_por_palavras(texto: str, termos_alvo: tuple, excluir_termos: tuple = ()) -> str:
    if not texto or not isinstance(texto, str):
        return ""

    texto_limpo = limpar_markdown_para_pdf(texto)
    partes = re.split(r"(?<=[.!?])\s+|\n+", texto_limpo)
    selecionadas: List[str] = []

    for parte in partes:
        trecho = parte.strip()
        if not trecho:
            continue
        baixo = trecho.lower()
        tem_alvo = any(t in baixo for t in termos_alvo)
        tem_exclusao = any(ex in baixo for ex in excluir_termos)
        if tem_alvo and not tem_exclusao:
            selecionadas.append(trecho)

    return " ".join(selecionadas).strip()


def _extrair_secoes_json_seguras(contexto: Dict[str, Any]) -> Dict[str, str]:
    chaves_4 = (
        "diagnostico_estrutural",
        "analise_dermica_hsv",
        "projecao_temporal",
        "recomendacao_tecnica",
    )
    origem: Dict[str, Any] = {}
    for cand in ("secoes_dossie_json", "secoes_json"):
        if isinstance(contexto.get(cand), dict):
            origem.update(contexto[cand])

    for chave in chaves_4:
        if chave in contexto and contexto[chave] is not None:
            origem[chave] = contexto[chave]

    resultado: Dict[str, str] = {}
    for chave in chaves_4:
        val = origem.get(chave)
        if isinstance(val, str) and val.strip():
            resultado[chave] = limpar_markdown_para_pdf(val)
    return resultado


def _remover_chaves_llm_e_secoes(pacote: Dict[str, Any]) -> Dict[str, Any]:
    for chave in CHAVES_LLM_E_SECOES:
        pacote.pop(chave, None)
    return pacote


def _montar_pacotes_por_motor(session_data: Dict[str, Any], lang: str) -> Dict[str, Dict[str, Any]]:
    secoes_4 = _extrair_secoes_json_seguras(session_data)

    blocos_trico: List[str] = []
    for chave_extra in ("dados_tricologia", "tricologia", "secao_tricologia", "analise_capilar"):
        val_extra = session_data.get(chave_extra)
        if isinstance(val_extra, str) and val_extra.strip():
            blocos_trico.append(limpar_markdown_para_pdf(val_extra))
        elif isinstance(val_extra, dict) and val_extra:
            blocos_trico.append(limpar_markdown_para_pdf(str(val_extra)))

    for chave_sec in ("diagnostico_estrutural", "projecao_temporal", "recomendacao_tecnica"):
        trecho_trico = _filtrar_sentencas_por_palavras(
            secoes_4.get(chave_sec, ""),
            PALAVRAS_TRICOLOGIA,
        )
        if trecho_trico:
            blocos_trico.append(trecho_trico)

    if not blocos_trico:
        for chave_llm in ("analise_gemini_recente", "analise_gemini"):
            val_llm = session_data.get(chave_llm)
            if isinstance(val_llm, str) and val_llm.strip():
                trecho_llm_trico = _filtrar_sentencas_por_palavras(val_llm, PALAVRAS_TRICOLOGIA)
                if trecho_llm_trico:
                    blocos_trico.append(trecho_llm_trico)

    texto_tricologia = "\n\n".join(dict.fromkeys([b for b in blocos_trico if b])).strip()

    blocos_fin: List[str] = []
    for chave_fin in ("dados_financeiros", "financeiro", "secao_financeiro", "roi"):
        val_fin = session_data.get(chave_fin)
        if isinstance(val_fin, str) and val_fin.strip():
            blocos_fin.append(limpar_markdown_para_pdf(val_fin))
        elif isinstance(val_fin, dict) and val_fin:
            blocos_fin.append(limpar_markdown_para_pdf(str(val_fin)))

    for chave_sec in ("projecao_temporal", "recomendacao_tecnica", "diagnostico_estrutural"):
        trecho_fin = _filtrar_sentencas_por_palavras(
            secoes_4.get(chave_sec, ""),
            PALAVRAS_FINANCEIRO,
            excluir_termos=PALAVRAS_TRICOLOGIA,
        )
        if trecho_fin:
            blocos_fin.append(trecho_fin)

    texto_financeiro = "\n\n".join(dict.fromkeys([b for b in blocos_fin if b])).strip()

    secoes_motor_1: Dict[str, str] = {}
    for chave_sec, valor_sec in secoes_4.items():
        if chave_sec == "analise_dermica_hsv":
            secoes_motor_1[chave_sec] = valor_sec
        else:
            sem_trico = _filtrar_sentencas_por_palavras(
                valor_sec,
                termos_alvo=(" ",),
                excluir_termos=PALAVRAS_TRICOLOGIA,
            )
            secoes_motor_1[chave_sec] = sem_trico or valor_sec

    pacote_m1 = copy.deepcopy(session_data)
    pacote_m1["secoes_dossie_json"] = secoes_motor_1
    pacote_m1["secoes_json"] = secoes_motor_1
    pacote_m1.update(secoes_motor_1)
    for chave_llm in ("analise_gemini_recente", "analise_gemini"):
        if isinstance(pacote_m1.get(chave_llm), str) and pacote_m1[chave_llm].strip():
            limpo_llm = _filtrar_sentencas_por_palavras(
                pacote_m1[chave_llm],
                termos_alvo=(" ",),
                excluir_termos=PALAVRAS_TRICOLOGIA,
            )
            pacote_m1[chave_llm] = limpo_llm or pacote_m1[chave_llm]
    pacote_m1.pop("secao_tricologia", None)
    pacote_m1.pop("resumo_diplomatico", None)

    pacote_m2 = copy.deepcopy(session_data)
    _remover_chaves_llm_e_secoes(pacote_m2)
    pacote_m2["secao_financeiro"] = texto_financeiro
    pacote_m2.pop("resumo_diplomatico", None)

    pacote_m3 = copy.deepcopy(session_data)
    pacote_m3["secao_tricologia"] = texto_tricologia
    pacote_m3["dados_tricologia_isolados"] = texto_tricologia
    secoes_m3: Dict[str, str] = {}
    for k_sec, v_sec in secoes_4.items():
        filtrado = _filtrar_sentencas_por_palavras(v_sec, PALAVRAS_TRICOLOGIA)
        if filtrado:
            secoes_m3[k_sec] = filtrado
    pacote_m3["secoes_dossie_json"] = secoes_m3
    pacote_m3["secoes_json"] = secoes_m3
    for k_sec in ("diagnostico_estrutural", "analise_dermica_hsv", "projecao_temporal", "recomendacao_tecnica"):
        if k_sec in secoes_m3:
            pacote_m3[k_sec] = secoes_m3[k_sec]
        else:
            pacote_m3.pop(k_sec, None)
    if texto_tricologia:
        pacote_m3["analise_gemini_recente"] = texto_tricologia
        pacote_m3["analise_gemini"] = texto_tricologia
    else:
        pacote_m3.pop("analise_gemini_recente", None)
        pacote_m3.pop("analise_gemini", None)

    pacote_m4 = copy.deepcopy(session_data)
    _remover_chaves_llm_e_secoes(pacote_m4)
    pacote_m4["anexo_diplomatico_limpo"] = True

    pacote_m5 = copy.deepcopy(session_data)
    _remover_chaves_llm_e_secoes(pacote_m5)

    pacote_m6 = copy.deepcopy(session_data)
    _remover_chaves_llm_e_secoes(pacote_m6)

    return {
        "motor_1": pacote_m1,
        "motor_2": pacote_m2,
        "motor_3": pacote_m3,
        "motor_4": pacote_m4,
        "motor_5": pacote_m5,
        "motor_6": pacote_m6,
    }


def _montar_contexto_memoria_e_llm(
    telemetria_dinamica: Optional[Dict[str, Any]] = None,
    destino: str = "motor_1",
) -> Dict[str, Any]:
    contexto: Dict[str, Any] = {}

    dados_mem = _ler_memoria_segura(destino=destino)
    if isinstance(dados_mem, dict):
        contexto.update(dados_mem)

    if isinstance(telemetria_dinamica, dict):
        contexto.update(telemetria_dinamica)

    for chave_analise in ("analise_gemini_recente", "analise_gemini"):
        if chave_analise in contexto and isinstance(contexto[chave_analise], str):
            contexto[chave_analise] = limpar_markdown_para_pdf(contexto[chave_analise])

    return contexto


def _anexar_evolucao_longitudinal(contexto: Dict[str, Any], titular: str, empresa: str) -> None:
    if not callable(obter_evolucao_titular):
        return
    try:
        dados_evo = obter_evolucao_titular(titular=titular, empresa=empresa)
        if isinstance(dados_evo, dict) and dados_evo.get("execucoes"):
            execucoes = dados_evo["execucoes"]
            ultimo = execucoes[-1] if isinstance(execucoes, list) else {}
            contexto["evolucao_longitudinal"] = {
                "titular": titular,
                "empresa": empresa,
                "total_execucoes": dados_evo.get("total_execucoes", len(execucoes)),
                "historico_ciclos": execucoes,
                "projecao_ciclos": ultimo.get("projecao_ciclos", {}),
                "comparativo_snapshot_anterior": ultimo.get("comparativo_snapshot_anterior"),
            }
            if isinstance(ultimo.get("projecao_ciclos"), dict):
                contexto["projecao_ciclos"] = ultimo["projecao_ciclos"]
    except Exception as e:
        print(f"[AVISO EVOLUÇÃO MASTER] Falha ao carregar histórico: {e}")


def compilar_dossies_master(
    ceo_name: Optional[str] = None,
    company_name: str = "Thierry Technology Concept Global",
    market_segment: str = "Tecnologia e Inovação",
    horizon_years: int = 10,
    operador: str = "THIERRY (TCC SOBERANO)",
    telemetria_dinamica: Optional[Dict[str, Any]] = None,
    lang: str = "PT",
) -> Dict[str, str]:
    session_data: Dict[str, Any] = _montar_contexto_memoria_e_llm(telemetria_dinamica, destino="motor_1")

    c_name = str(ceo_name) if ceo_name else ""
    s_cli = str(session_data.get("nome_cliente", "")) if session_data.get("nome_cliente") else ""
    s_nom = str(session_data.get("nome", "")) if session_data.get("nome") else ""
    m_cli = str(_ler_memoria_segura(chave="nome_cliente", destino="motor_1") or "")
    m_tit = str(_ler_memoria_segura(chave="titular", destino="motor_1") or "")

    nome_titular_efetivo: str = c_name or s_cli or s_nom or m_cli or m_tit or "CLIENTE UHNW"
    _anexar_evolucao_longitudinal(session_data, titular=nome_titular_efetivo, empresa=company_name)

    idioma_limpo = str(lang).upper() if lang and isinstance(lang, str) else "PT"
    if idioma_limpo not in ("PT", "EN"):
        idioma_limpo = "PT"

    pacotes_motor = _montar_pacotes_por_motor(session_data, lang=idioma_limpo)
    timestamp_autentico = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

    print("=" * 65)
    print(f"PIPELINE MASTER DINÂMICO: COMPILANDO OS DOSSIÊS + CONTRATO GLOBAL [LANG: {idioma_limpo}]")
    print(f"Titular: {nome_titular_efetivo} | Operador: {operador} | Emissão: {timestamp_autentico}")
    print("=" * 65)

    for motor, status in MOTORES_STATUS.items():
        print(f"[{motor}] Status de Carregamento: {status}")
    print("-" * 65)

    resultados_geracao: Dict[str, str] = {}
    pasta_finais = os.path.join(ROOT_DIR, "pdfs_finais")
    os.makedirs(pasta_finais, exist_ok=True)

    if "OK" in MOTORES_STATUS.get("Motor 1", ""):
        try:
            print(f"[1/6] Compilando Inteligência Soberana C2 [{idioma_limpo}]...")
            engine_1 = C2SovereignIntelligenceEngine(  # type: ignore
                ceo_name=nome_titular_efetivo,
                company_name=company_name,
                market_segment=market_segment,
                horizon_years=horizon_years,
                telemetria=pacotes_motor["motor_1"],
                lang=idioma_limpo,
            )

            caminho_1 = os.path.join(pasta_finais, "01_Dossie_Sovereign_Intelligence.pdf")
            if hasattr(engine_1, "gerar_pdf_defensivo_soberano"):
                try:
                    engine_1.gerar_pdf_defensivo_soberano(caminho_1, lang=idioma_limpo)
                except TypeError:
                    engine_1.gerar_pdf_defensivo_soberano(caminho_1)
            elif hasattr(engine_1, "gerar_dossie"):
                try:
                    engine_1.gerar_dossie(caminho_1, lang=idioma_limpo)
                except TypeError:
                    engine_1.gerar_dossie(caminho_1)

            resultados_geracao["01_Sovereign_Intelligence"] = caminho_1
            print(f" -> Sucesso: {caminho_1}")
        except Exception as e:
            print(f" -> Erro na execução do Motor 1: {e}")
            traceback.print_exc()

    if "OK" in MOTORES_STATUS.get("Motor 2", ""):
        try:
            print(f"[2/6] Compilando Super Retorno Financeiro [{idioma_limpo}]...")
            engine_2 = C2SovereignROIEngine(  # type: ignore
                titular=nome_titular_efetivo,
                market_segment=market_segment,
                horizon_years=horizon_years,
                telemetria=pacotes_motor["motor_2"],
                lang=idioma_limpo,
            )

            caminho_2 = os.path.join(pasta_finais, "02_Super_Retorno_Financeiro.pdf")
            if hasattr(engine_2, "gerar_dossie"):
                try:
                    engine_2.gerar_dossie(caminho_2, lang=idioma_limpo)
                except TypeError:
                    engine_2.gerar_dossie(caminho_2)
            elif hasattr(engine_2, "gerar_pdf"):
                try:
                    engine_2.gerar_pdf(caminho_2, lang=idioma_limpo)
                except TypeError:
                    engine_2.gerar_pdf(caminho_2)

            resultados_geracao["02_Super_Retorno_Financeiro"] = caminho_2
            print(f" -> Sucesso: {caminho_2}")
        except Exception as e:
            print(f" -> Erro na execução do Motor 2: {e}")
            traceback.print_exc()

    if "OK" in MOTORES_STATUS.get("Motor 3", ""):
        try:
            print(f"[3/6] Compilando Tricologia Ultra Avançada [{idioma_limpo}]...")
            engine_3 = C2UltraAdvancedTrichologyEngine(  # type: ignore
                ceo_name=nome_titular_efetivo,
                company_name=company_name,
                telemetria=pacotes_motor["motor_3"],
                lang=idioma_limpo,
            )

            caminho_3 = os.path.join(pasta_finais, "03_Dossie_Tricologia_Avancada.pdf")
            if hasattr(engine_3, "gerar_dossie"):
                try:
                    engine_3.gerar_dossie(caminho_3, lang=idioma_limpo)
                except TypeError:
                    engine_3.gerar_dossie(caminho_3)
            elif hasattr(engine_3, "gerar_pdf"):
                try:
                    engine_3.gerar_pdf(caminho_3, lang=idioma_limpo)
                except TypeError:
                    engine_3.gerar_pdf(caminho_3)

            resultados_geracao["03_Tricologia_Avancada"] = caminho_3
            print(f" -> Sucesso: {caminho_3}")
        except Exception as e:
            print(f" -> Erro na execução do Motor 3: {e}")
            traceback.print_exc()

    if "OK" in MOTORES_STATUS.get("Motor 4", ""):
        try:
            print(f"[4/6] Compilando Carta Internacional UHNW [{idioma_limpo}]...")
            engine_4 = CartaInternacionalEngine(  # type: ignore
                nome_cliente=nome_titular_efetivo,
                operador=operador,
                telemetria=pacotes_motor["motor_4"],
                lang=idioma_limpo,
            )

            caminho_4 = os.path.join(pasta_finais, "04_Carta_Internacional_UHNW.pdf")
            if hasattr(engine_4, "gerar_carta_apresentacao"):
                try:
                    engine_4.gerar_carta_apresentacao(caminho_salvamento=caminho_4, lang=idioma_limpo)
                except TypeError:
                    engine_4.gerar_carta_apresentacao(caminho_salvamento=caminho_4)
            elif hasattr(engine_4, "gerar_dossie"):
                try:
                    engine_4.gerar_dossie(caminho_4, lang=idioma_limpo)
                except TypeError:
                    engine_4.gerar_dossie(caminho_4)

            resultados_geracao["04_Carta_UHNW"] = caminho_4
            print(f" -> Sucesso: {caminho_4}")
        except Exception as e:
            print(f" -> Erro na execução do Motor 4: {e}")
            traceback.print_exc()

    if "OK" in MOTORES_STATUS.get("Motor 5", ""):
        try:
            print(f"[5/6] Compilando Modelagem Computacional & Valuación Mônaco [{idioma_limpo}]...")
            engine_5 = C2MonacoModelingEngine(  # type: ignore
                ceo_name=nome_titular_efetivo,
                company_name=company_name,
                market_segment=market_segment,
                horizon_years=horizon_years,
                operador=operador,
                telemetria=pacotes_motor["motor_5"],
                lang=idioma_limpo,
            )

            caminho_5 = os.path.join(pasta_finais, "05_Dossie_Modelagem_Computacional.pdf")
            if hasattr(engine_5, "gerar_dossie_modelagem"):
                try:
                    engine_5.gerar_dossie_modelagem(caminho_5, lang=idioma_limpo)
                except TypeError:
                    engine_5.gerar_dossie_modelagem(caminho_5)
            elif hasattr(engine_5, "gerar_dossie"):
                try:
                    engine_5.gerar_dossie(caminho_5, lang=idioma_limpo)
                except TypeError:
                    engine_5.gerar_dossie(caminho_5)

            resultados_geracao["05_Modelagem_Computacional"] = caminho_5
            print(f" -> Sucesso: {caminho_5}")
        except Exception as e:
            print(f" -> Erro na execução do Motor 5: {e}")
            traceback.print_exc()

    if "OK" in MOTORES_STATUS.get("Motor 6", ""):
        try:
            print(f"[6/6] Compilando Contrato de Licenciamento Global [{idioma_limpo}]...")
            licenciado_alvo = str(session_data.get("licenciado_nome") or nome_titular_efetivo)
            engine_contrato = C2GlobalContractEngine(  # type: ignore
                licenciado_nome=licenciado_alvo,
                pais_destino="MC",
                plano_escolhido="Monaco_Supremacy",
                lang=idioma_limpo,
                telemetria=pacotes_motor["motor_6"],
            )

            caminho_contrato = os.path.join(pasta_finais, "06_Contrato_Licenciamento_Global.pdf")
            if hasattr(engine_contrato, "gerar_pdf"):
                try:
                    engine_contrato.gerar_pdf(caminho_contrato, lang=idioma_limpo)
                except TypeError:
                    engine_contrato.gerar_pdf(caminho_contrato)
            elif hasattr(engine_contrato, "gerar_contrato"):
                try:
                    engine_contrato.gerar_contrato(caminho_contrato, lang=idioma_limpo)
                except TypeError:
                    engine_contrato.gerar_contrato(caminho_contrato)

            resultados_geracao["06_Contrato_Licenciamento_Global"] = caminho_contrato
            print(f" -> Sucesso: {caminho_contrato}")
        except Exception as e:
            print(f" -> Erro na execução do Contrato Global: {e}")
            traceback.print_exc()

    try:
        if hasattr(memoria, "salvar_dados"):
            memoria.salvar_dados("ultimo_dossie_gerado", {
                "titular": nome_titular_efetivo,
                "idioma": idioma_limpo,
                "emitido_em": timestamp_autentico,
                "arquivos": resultados_geracao,
            })
    except Exception:
        pass

    print("=" * 75)
    print(" [RELATÓRIO DE AUDITORIA DO TERMINAL - ARQUIVOS NA PASTA PDFS_FINAIS]")
    print("=" * 75)
    for chave, caminho in resultados_geracao.items():
        if os.path.exists(caminho):
            tamanho_kb = os.path.getsize(caminho) / 1024
            print(f" 📂 [{chave.upper()}] Status: OK | Tamanho: {tamanho_kb:.2f} KB")
            print(f"    └─ Caminho: {caminho}")
        else:
            print(f" ❌ [{chave.upper()}] Status: FALHOU OU ARQUIVO NÃO ENCONTRADO")
    print("=" * 75)

    print(f"PIPELINE CONCLUÍDO ÀS {timestamp_autentico}. TODOS OS RELATÓRIOS FORAM PROCESSADOS.")
    print("=" * 65)
    return resultados_geracao


def compilar_dossies_bilingue(
    ceo_name: Optional[str] = None,
    company_name: str = "Thierry Technology Concept Global",
    market_segment: str = "Tecnologia e Inovação",
    horizon_years: int = 10,
    operador: str = "THIERRY (TCC SOBERANO)",
    telemetria_dinamica: Optional[Dict[str, Any]] = None,
) -> Dict[str, Dict[str, str]]:
    return {
        "PT": compilar_dossies_master(
            ceo_name=ceo_name,
            company_name=company_name,
            market_segment=market_segment,
            horizon_years=horizon_years,
            operador=operador,
            telemetria_dinamica=telemetria_dinamica,
            lang="PT",
        ),
        "EN": compilar_dossies_master(
            ceo_name=ceo_name,
            company_name=company_name,
            market_segment=market_segment,
            horizon_years=horizon_years,
            operador=operador,
            telemetria_dinamica=telemetria_dinamica,
            lang="EN",
        ),
    }


def _montar_contexto_biometrico_seguro() -> str:
    for mod_name in ("contexto_biometrico", "core.contexto_biometrico"):
        try:
            mod = __import__(mod_name, fromlist=["montar_contexto_biometrico"])
            fn = getattr(mod, "montar_contexto_biometrico", None)
            if callable(fn):
                return _sanitizar_sem_herpes(str(fn(memoria)))
        except Exception:
            continue

    dados_motor: Any = _ler_memoria_segura(chave="motor_biometrico_atual", destino="motor_1")

    if not isinstance(dados_motor, dict) or not dados_motor:
        raise ValueError("Motor biométrico sem frame válido processado em memória.")

    phi = float(dados_motor.get("phi_global") or 0.0)
    proj = dados_motor.get("projecoes_anos") if isinstance(dados_motor.get("projecoes_anos"), dict) else {}
    p5 = proj.get("5_anos") if isinstance(proj.get("5_anos"), dict) else {}
    p10 = proj.get("10_anos") if isinstance(proj.get("10_anos"), dict) else {}
    p15 = proj.get("15_anos") if isinstance(proj.get("15_anos"), dict) else {}

    return f"""
DADOS DO MOTOR BIOMÉTRICO (MODELO PARAMÉTRICO):
- Proporção Áurea Global (Phi): {phi:.3f}
- Refletância: {float(dados_motor.get("refletancia_pele") or 0.0):.1f}%
- Água Estimada: {float(dados_motor.get("agua_estimada") or 0.0):.1f}% | Reposição Sugerida: {int(float(dados_motor.get("agua_necessaria_ml") or 0))} mL
- 5 Anos: Queda {float(p5.get("dist_descolamento_mm") or 0.0):.2f} mm | Grau Envelhecimento: {float(p5.get("grau_envelhecimento") or 0.0):.1f}/10
- 10 Anos: Queda {float(p10.get("dist_descolamento_mm") or 0.0):.2f} mm | Grau Envelhecimento: {float(p10.get("grau_envelhecimento") or 0.0):.1f}/10
- 15 Anos: Queda {float(p15.get("dist_descolamento_mm") or 0.0):.2f} mm | Grau Envelhecimento: {float(p15.get("grau_envelhecimento") or 0.0):.1f}/10

INSTRUÇÃO: Utilize exatamente os números acima como simulação paramétrica computacional (não diagnóstico clínico).
""".strip()


def compilar_dossies_com_biometria_e_json(
    chamar_llm: Optional[Callable[[str], str]] = None,
    ceo_name: Optional[str] = None,
    company_name: str = "Thierry Technology Concept Global",
    market_segment: str = "Tecnologia e Inovação",
    horizon_years: int = 10,
    operador: str = "THIERRY (TCC SOBERANO)",
    lang: str = "PT",
    telemetria_dinamica: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    idioma_limpo = str(lang).upper() if lang and isinstance(lang, str) else "PT"
    if idioma_limpo not in ("PT", "EN"):
        idioma_limpo = "PT"

    try:
        contexto_bio: Optional[str] = _montar_contexto_biometrico_seguro()
    except Exception as e_bio:
        contexto_bio = None
        print(f"[AVISO BIOMETRIA MASTER] Sem frame em memória no momento: {e_bio}")

    telemetria_extra: Dict[str, Any] = {}
    if isinstance(telemetria_dinamica, dict):
        telemetria_extra.update(telemetria_dinamica)
    if contexto_bio:
        telemetria_extra["contexto_biometrico_parametrico"] = contexto_bio

    secoes_json: Optional[Dict[str, str]] = None
    for mod_name in ("orquestrador_json", "core.orquestrador_json"):
        try:
            mod_json = __import__(mod_name, fromlist=["gerar_secoes_dossie", "gerar_secoes_dossie_json"])
            if callable(chamar_llm) and hasattr(mod_json, "gerar_secoes_dossie") and callable(getattr(mod_json, "gerar_secoes_dossie")):
                fn_secoes = getattr(mod_json, "gerar_secoes_dossie")
                try:
                    secoes_json = fn_secoes(memoria, chamar_llm=chamar_llm, lang=idioma_limpo)
                except TypeError:
                    secoes_json = fn_secoes(memoria, chamar_llm=chamar_llm)
                break
            if hasattr(mod_json, "gerar_secoes_dossie_json") and callable(getattr(mod_json, "gerar_secoes_dossie_json")):
                res_json, _ = mod_json.gerar_secoes_dossie_json(lang=idioma_limpo)
                if isinstance(res_json, dict):
                    secoes_json = res_json
                break
        except Exception as e_json:
            print(f"[AVISO JSON MASTER ({mod_name})] {e_json}")

    if isinstance(secoes_json, dict) and secoes_json:
        secoes_limpas = {
            k: limpar_markdown_para_pdf(v) if isinstance(v, str) else v
            for k, v in secoes_json.items()
        }
        secoes_json = secoes_limpas
        telemetria_extra["secoes_dossie_json"] = secoes_limpas
        telemetria_extra["secoes_json"] = secoes_limpas
        telemetria_extra.update(secoes_limpas)

    pdfs = compilar_dossies_master(
        ceo_name=ceo_name,
        company_name=company_name,
        market_segment=market_segment,
        horizon_years=horizon_years,
        operador=operador,
        telemetria_dinamica=telemetria_extra if telemetria_extra else None,
        lang=idioma_limpo,
    )

    return {
        "pdfs": pdfs,
        "secoes_json": secoes_json,
        "contexto_biometrico": contexto_bio,
    }


if __name__ == "__main__":
    compilar_dossies_master(lang="PT")