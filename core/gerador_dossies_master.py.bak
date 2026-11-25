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
Versão: 6.9.2 - DINÂMICO, SOBERANO E BILÍNGUE (PT / EN)
Descrição: Orquestrador Mestre dinâmico com integração de memória, telemetria/LLM
           e evolução longitudinal (5, 10 e 15 anos) para compilação dos dossiês
           e contrato global em Português e Inglês.
"""

import os
import sys
import datetime
import traceback
import re
from typing import Dict, Any, Optional

# --- PONTE DE MEMÓRIA AUTOMÁTICA (THIERRY TECH) ---
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:
        class MemoriaMock:
            def salvar_dados(self, chave: str, valor: Any) -> None:
                pass

            def registrar(self, chave: str, valor: Any) -> None:
                pass

            def ler_dados(self, chave: Optional[str] = None) -> Any:
                return None

        memoria = MemoriaMock()
# ---------------------------------------------------

# Garante a resolução de escopo para o core do ecossistema
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# =====================================================================
# IMPORTAÇÃO SEGURA DOS MOTORES DO ECOSSISTEMA (1 A 6) + EVOLUÇÃO
# =====================================================================
MOTORES_STATUS: Dict[str, str] = {}

obter_evolucao_titular: Any = None
try:
    from core.diagnostico_evolucao import obter_evolucao_titular as _obt_evo_titular  # type: ignore
    obter_evolucao_titular = _obt_evo_titular
except ImportError:
    obter_evolucao_titular = None

# Motor 1: Inteligência Soberana C2
try:
    from core.c2_sovereign_intelligence import C2SovereignIntelligenceEngine  # type: ignore
    MOTORES_STATUS["Motor 1"] = "OK"
except ImportError as e:
    MOTORES_STATUS["Motor 1"] = f"Indisponível ({e})"

# Motor 2: Super Retorno Financeiro
try:
    from core.super_retorno_financeiro import C2SovereignROIEngine  # type: ignore
    MOTORES_STATUS["Motor 2"] = "OK"
except ImportError as e:
    MOTORES_STATUS["Motor 2"] = f"Indisponível ({e})"

# Motor 3: Tricologia Ultra Avançada
try:
    from core.tricologia_ultra_avancada import C2UltraAdvancedTrichologyEngine  # type: ignore
    MOTORES_STATUS["Motor 3"] = "OK"
except ImportError as e:
    MOTORES_STATUS["Motor 3"] = f"Indisponível ({e})"

# Motor 4: Carta Internacional UHNW
try:
    from core.carta_internacional_engine import CartaInternacionalEngine  # type: ignore
    MOTORES_STATUS["Motor 4"] = "OK"
except ImportError as e:
    MOTORES_STATUS["Motor 4"] = f"Indisponível ({e})"

# Motor 5: Modelagem Computacional & Valuación Mônaco
try:
    from core.monaco_modelagem_engine import C2MonacoModelingEngine  # type: ignore
    MOTORES_STATUS["Motor 5"] = "OK"
except ImportError as e:
    MOTORES_STATUS["Motor 5"] = f"Indisponível ({e})"

# Motor 6: Contrato Global de Licenciamento (Prioriza a pasta oficial /legal)
try:
    from legal.contrato_global_engine import C2GlobalContractEngine  # type: ignore
    MOTORES_STATUS["Motor 6"] = "OK (Via /legal)"
except ImportError:
    try:
        from core.contrato_global_engine import C2GlobalContractEngine  # type: ignore
        MOTORES_STATUS["Motor 6"] = "OK (Via /core)"
    except ImportError as e:
        MOTORES_STATUS["Motor 6"] = f"Indisponível ({e})"


def limpar_markdown_para_pdf(texto_cru: str) -> str:
    """
    Remove tags de Markdown cruas (###, **, ---) para que o PDF
    exiba um texto limpo, elegante e executivo nos anexos.
    """
    if not isinstance(texto_cru, str):
        texto_cru = str(texto_cru)

    texto = re.sub(r'#{1,6}\s*', '', texto_cru)
    texto = re.sub(r'\*\*', '', texto)
    texto = re.sub(r'\*', '', texto)
    texto = re.sub(r'---+', '', texto)

    return texto.strip()


def _montar_contexto_memoria_e_llm(telemetria_dinamica: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Une os dados da memória do sistema com a telemetria/análise da sessão atual
    sem fabricar métricas ou textos extras.
    """
    contexto: Dict[str, Any] = {}

    try:
        dados_mem = memoria.ler_dados()
        if isinstance(dados_mem, dict):
            contexto.update(dados_mem)
    except Exception:
        pass

    if isinstance(telemetria_dinamica, dict):
        contexto.update(telemetria_dinamica)

    for chave_analise in ("analise_gemini_recente", "analise_gemini"):
        if chave_analise in contexto and isinstance(contexto[chave_analise], str):
            contexto[chave_analise] = limpar_markdown_para_pdf(contexto[chave_analise])

    return contexto


def _anexar_evolucao_longitudinal(contexto: Dict[str, Any], titular: str, empresa: str) -> None:
    """
    Anexa ao contexto o histórico local e as projeções de 5, 10 e 15 anos
    para consumo pelo Motor 1 no dossiê de inteligência.
    """
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
    """
    Executa o pipeline mestre dinâmico unindo memória, telemetria/LLM e evolução
    longitudinal, compilando os dossiês e o contrato global no idioma solicitado ('PT' ou 'EN').
    """
    session_data: Dict[str, Any] = _montar_contexto_memoria_e_llm(telemetria_dinamica)

    c_name = str(ceo_name) if ceo_name else ""
    s_cli = str(session_data.get("nome_cliente", "")) if session_data.get("nome_cliente") else ""
    s_nom = str(session_data.get("nome", "")) if session_data.get("nome") else ""
    m_cli = str(memoria.ler_dados("nome_cliente") or "")
    m_tit = str(memoria.ler_dados("titular") or "")

    nome_titular_efetivo: str = c_name or s_cli or s_nom or m_cli or m_tit or "CLIENTE UHNW"
    _anexar_evolucao_longitudinal(session_data, titular=nome_titular_efetivo, empresa=company_name)

    idioma_limpo = str(lang).upper() if lang and isinstance(lang, str) else "PT"
    if idioma_limpo not in ("PT", "EN"):
        idioma_limpo = "PT"

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

    # 1. Compilação Motor 1 (C2 Sovereign Intelligence)
    if "OK" in MOTORES_STATUS.get("Motor 1", ""):
        try:
            print(f"[1/6] Compilando Inteligência Soberana C2 [{idioma_limpo}]...")
            engine_1 = C2SovereignIntelligenceEngine(  # type: ignore
                ceo_name=nome_titular_efetivo,
                company_name=company_name,
                market_segment=market_segment,
                horizon_years=horizon_years,
                telemetria=session_data,
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

    # 2. Compilação Motor 2 (Super Retorno Financeiro)
    if "OK" in MOTORES_STATUS.get("Motor 2", ""):
        try:
            print(f"[2/6] Compilando Super Retorno Financeiro [{idioma_limpo}]...")
            engine_2 = C2SovereignROIEngine(  # type: ignore
                titular=nome_titular_efetivo,
                market_segment=market_segment,
                horizon_years=horizon_years,
                telemetria=session_data,
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

    # 3. Compilação Motor 3 (Tricologia Ultra Avançada)
    if "OK" in MOTORES_STATUS.get("Motor 3", ""):
        try:
            print(f"[3/6] Compilando Tricologia Ultra Avançada [{idioma_limpo}]...")
            engine_3 = C2UltraAdvancedTrichologyEngine(  # type: ignore
                ceo_name=nome_titular_efetivo,
                company_name=company_name,
                telemetria=session_data,
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

    # 4. Compilação Motor 4 (Carta Internacional UHNW)
    if "OK" in MOTORES_STATUS.get("Motor 4", ""):
        try:
            print(f"[4/6] Compilando Carta Internacional UHNW [{idioma_limpo}]...")
            engine_4 = CartaInternacionalEngine(  # type: ignore
                nome_cliente=nome_titular_efetivo,
                operador=operador,
                telemetria=session_data,
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

    # 5. Compilação Motor 5 (Modelagem Computacional Mônaco)
    if "OK" in MOTORES_STATUS.get("Motor 5", ""):
        try:
            print(f"[5/6] Compilando Modelagem Computacional & Valuación Mônaco [{idioma_limpo}]...")
            engine_5 = C2MonacoModelingEngine(  # type: ignore
                ceo_name=nome_titular_efetivo,
                company_name=company_name,
                market_segment=market_segment,
                horizon_years=horizon_years,
                operador=operador,
                telemetria=session_data,
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

    # 6. Compilação Motor 6 (Contrato Global de Licenciamento)
    if "OK" in MOTORES_STATUS.get("Motor 6", ""):
        try:
            print(f"[6/6] Compilando Contrato de Licenciamento Global [{idioma_limpo}]...")
            licenciado_alvo = str(session_data.get("licenciado_nome") or nome_titular_efetivo)
            engine_contrato = C2GlobalContractEngine(  # type: ignore
                licenciado_nome=licenciado_alvo,
                pais_destino="MC",
                plano_escolhido="Monaco_Supremacy",
                lang=idioma_limpo,
                telemetria=session_data,
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

    # RELATÓRIO DE AUDITORIA COMPLETO NO TERMINAL
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
    """
    Executa a compilação em Português ('PT') e Inglês ('EN') em sequência.
    """
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


if __name__ == "__main__":
    compilar_dossies_master(lang="PT")