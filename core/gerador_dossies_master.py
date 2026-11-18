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
Versão: 6.9.2 - DINÂMICO, SOBERANO E PADRONIZADO ISO A4 (MEDIABOX LIMPO)
Descrição: Orquestrador Mestre dinâmico com normalização automática ISO 216 (A4)
           via ajuste direto de caixa de mídia para perfeita compatibilidade com o auditor.
"""

import os
import sys
import datetime
import traceback
import re
from typing import Dict, Any, Optional
import pymupdf as fitz

# --- PONTE DE MEMÓRIA AUTOMÁTICA (THIERRY TECH) ---
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:
        class MemoriaMock:
            def salvar_dados(self, chave: str, valor: Any) -> None: pass
            def registrar(self, chave: str, valor: Any) -> None: pass
            def ler_dados(self, chave: Optional[str] = None) -> Any: return None
        memoria = MemoriaMock()
# ---------------------------------------------------

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# =====================================================================
# IMPORTAÇÃO SEGURA DOS MOTORES DO ECOSSISTEMA (1 A 6)
# =====================================================================
MOTORES_STATUS = {}

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


def padronizar_pdf_iso_a4(caminho_pdf: str) -> None:
    """
    Garante que o PDF esteja estritamente no formato ISO A4 (595.28 x 841.89 pt)
    e com metadado 'Title' preenchido (ISO 14289), ajustando a caixa de mídia
    diretamente sem redimensionar ou alterar as coordenadas internas do texto.
    """
    if not os.path.exists(caminho_pdf):
        return

    largura_a4, altura_a4 = 595.28, 841.89
    doc = fitz.open(caminho_pdf)
    
    meta = doc.metadata or {}
    if not meta.get("title") or not meta.get("title").strip():
        meta["title"] = os.path.splitext(os.path.basename(caminho_pdf))[0].replace("_", " ")
        doc.set_metadata(meta)

    precisa_ajuste = False
    for pagina in doc:
        w, h = float(pagina.rect.width), float(pagina.rect.height)
        if abs(w - largura_a4) > 5 or abs(h - altura_a4) > 5:
            precisa_ajuste = True
            break

    if not precisa_ajuste:
        doc.close()
        return

    retangulo_a4 = fitz.Rect(0, 0, largura_a4, altura_a4)
    for pagina in doc:
        pagina.set_mediabox(retangulo_a4)

    caminho_temp = caminho_pdf + ".a4.tmp"
    doc.save(caminho_temp, garbage=4, deflate=True)
    doc.close()

    os.replace(caminho_temp, caminho_pdf)


def limpar_markdown_para_pdf(texto_cru: str) -> str:
    if not isinstance(texto_cru, str):
        return str(texto_cru)
    texto = re.sub(r'#{1,6}\s*', '', texto_cru)
    texto = re.sub(r'\*\*', '', texto)
    texto = re.sub(r'\*', '', texto)
    texto = re.sub(r'---+', '', texto)
    return texto.strip()


def compilar_dossies_master(
    ceo_name: Optional[str] = None,
    company_name: str = "Thierry Technology Concept Global",
    market_segment: str = "Tecnologia e Inovação",
    horizon_years: int = 10,
    operador: str = "THIERRY (TCC SOBERANO)",
    telemetria_dinamica: Optional[Dict[str, Any]] = None,
    lang: str = "PT"
) -> Dict[str, str]:
    session_data: Dict[str, Any] = telemetria_dinamica or {}
    
    c_name = str(ceo_name) if ceo_name else ""
    s_cli = str(session_data.get('nome_cliente', '')) if session_data.get('nome_cliente') else ""
    s_nom = str(session_data.get('nome', '')) if session_data.get('nome') else ""
    m_cli = str(memoria.ler_dados("nome_cliente") or "")
    m_tit = str(memoria.ler_dados("titular") or "")

    nome_titular_efetivo: str = c_name or s_cli or s_nom or m_cli or m_tit or "CLIENTE UHNW"
    idioma_limpo = str(lang).upper() if lang and isinstance(lang, str) else "PT"
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

    # 1. Compilação Motor 1
    if "OK" in MOTORES_STATUS.get("Motor 1", ""):
        try:
            print(f"[1/6] Compilando Inteligência Soberana C2 [{idioma_limpo}]...")
            engine_1 = C2SovereignIntelligenceEngine(  # type: ignore
                ceo_name=nome_titular_efetivo,
                company_name=company_name,
                market_segment=market_segment,
                horizon_years=horizon_years,
                telemetria=session_data,
                lang=idioma_limpo
            )
            caminho_1 = os.path.join(pasta_finais, "01_Dossie_Sovereign_Intelligence.pdf")
            if hasattr(engine_1, 'gerar_pdf_defensivo_soberano'):
                try:
                    engine_1.gerar_pdf_defensivo_soberano(caminho_1, lang=idioma_limpo)
                except TypeError:
                    engine_1.gerar_pdf_defensivo_soberano(caminho_1)
            elif hasattr(engine_1, 'gerar_dossie'):
                try:
                    engine_1.gerar_dossie(caminho_1, lang=idioma_limpo)
                except TypeError:
                    engine_1.gerar_dossie(caminho_1)
            
            padronizar_pdf_iso_a4(caminho_1)
            resultados_geracao["01_Sovereign_Intelligence"] = caminho_1
            print(f" -> Sucesso: {caminho_1}")
        except Exception as e:
            print(f" -> Erro na execução do Motor 1: {e}")
            traceback.print_exc()

    # 2. Compilação Motor 2
    if "OK" in MOTORES_STATUS.get("Motor 2", ""):
        try:
            print(f"[2/6] Compilando Super Retorno Financeiro [{idioma_limpo}]...")
            engine_2 = C2SovereignROIEngine(  # type: ignore
                titular=nome_titular_efetivo,
                market_segment=market_segment,
                horizon_years=horizon_years,
                telemetria=session_data,
                lang=idioma_limpo
            )
            caminho_2 = os.path.join(pasta_finais, "02_Super_Retorno_Financeiro.pdf")
            if hasattr(engine_2, 'gerar_dossie'):
                try:
                    engine_2.gerar_dossie(caminho_2, lang=idioma_limpo)
                except TypeError:
                    engine_2.gerar_dossie(caminho_2)
            elif hasattr(engine_2, 'gerar_pdf'):
                try:
                    engine_2.gerar_pdf(caminho_2, lang=idioma_limpo)
                except TypeError:
                    engine_2.gerar_pdf(caminho_2)
            
            padronizar_pdf_iso_a4(caminho_2)
            resultados_geracao["02_Super_Retorno_Financeiro"] = caminho_2
            print(f" -> Sucesso: {caminho_2}")
        except Exception as e:
            print(f" -> Erro na execução do Motor 2: {e}")

    # 3. Compilação Motor 3
    if "OK" in MOTORES_STATUS.get("Motor 3", ""):
        try:
            print(f"[3/6] Compilando Tricologia Ultra Avançada [{idioma_limpo}]...")
            engine_3 = C2UltraAdvancedTrichologyEngine(  # type: ignore
                ceo_name=nome_titular_efetivo,
                company_name=company_name,
                telemetria=session_data,
                lang=idioma_limpo
            )
            caminho_3 = os.path.join(pasta_finais, "03_Dossie_Tricologia_Avancada.pdf")
            if hasattr(engine_3, 'gerar_dossie'):
                try:
                    engine_3.gerar_dossie(caminho_3, lang=idioma_limpo)
                except TypeError:
                    engine_3.gerar_dossie(caminho_3)
            elif hasattr(engine_3, 'gerar_pdf'):
                try:
                    engine_3.gerar_pdf(caminho_3, lang=idioma_limpo)
                except TypeError:
                    engine_3.gerar_pdf(caminho_3)
            
            padronizar_pdf_iso_a4(caminho_3)
            resultados_geracao["03_Tricologia_Avancada"] = caminho_3
            print(f" -> Sucesso: {caminho_3}")
        except Exception as e:
            print(f" -> Erro na execução do Motor 3: {e}")

    # 4. Compilação Motor 4
    if "OK" in MOTORES_STATUS.get("Motor 4", ""):
        try:
            print(f"[4/6] Compilando Carta Internacional UHNW [{idioma_limpo}]...")
            engine_4 = CartaInternacionalEngine(  # type: ignore
                nome_cliente=nome_titular_efetivo,
                operador=operador,
                telemetria=session_data,
                lang=idioma_limpo
            )
            caminho_4 = os.path.join(pasta_finais, "04_Carta_Internacional_UHNW.pdf")
            if hasattr(engine_4, 'gerar_carta_apresentacao'):
                try:
                    engine_4.gerar_carta_apresentacao(caminho_salvamento=caminho_4, lang=idioma_limpo)
                except TypeError:
                    engine_4.gerar_carta_apresentacao(caminho_salvamento=caminho_4)
            elif hasattr(engine_4, 'gerar_dossie'):
                try:
                    engine_4.gerar_dossie(caminho_4, lang=idioma_limpo)
                except TypeError:
                    engine_4.gerar_dossie(caminho_4)
            
            padronizar_pdf_iso_a4(caminho_4)
            resultados_geracao["04_Carta_UHNW"] = caminho_4
            print(f" -> Sucesso: {caminho_4}")
        except Exception as e:
            print(f" -> Erro na execução do Motor 4: {e}")

    # 5. Compilação Motor 5
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
                lang=idioma_limpo
            )
            caminho_5 = os.path.join(pasta_finais, "05_Dossie_Modelagem_Computacional.pdf")
            if hasattr(engine_5, 'gerar_dossie_modelagem'):
                try:
                    engine_5.gerar_dossie_modelagem(caminho_5, lang=idioma_limpo)
                except TypeError:
                    engine_5.gerar_dossie_modelagem(caminho_5)
            elif hasattr(engine_5, 'gerar_dossie'):
                try:
                    engine_5.gerar_dossie(caminho_5, lang=idioma_limpo)
                except TypeError:
                    engine_5.gerar_dossie(caminho_5)
            
            padronizar_pdf_iso_a4(caminho_5)
            resultados_geracao["05_Modelagem_Computacional"] = caminho_5
            print(f" -> Sucesso: {caminho_5}")
        except Exception as e:
            print(f" -> Erro na execução do Motor 5: {e}")

    # 6. Compilação Motor 6
    if "OK" in MOTORES_STATUS.get("Motor 6", ""):
        try:
            print(f"[6/6] Compilando Contrato de Licenciamento Global [{idioma_limpo}]...")
            engine_contrato = C2GlobalContractEngine(  # type: ignore
                licenciado_nome=company_name,
                pais_destino="MC",
                plano_escolhido="Monaco_Supremacy",
                lang=idioma_limpo
            )
            caminho_contrato = os.path.join(pasta_finais, "06_Contrato_Licenciamento_Global.pdf")
            if hasattr(engine_contrato, 'gerar_pdf'):
                try:
                    engine_contrato.gerar_pdf(caminho_contrato, lang=idioma_limpo)
                except TypeError:
                    engine_contrato.gerar_pdf(caminho_contrato)
            elif hasattr(engine_contrato, 'gerar_contrato'):
                try:
                    engine_contrato.gerar_contrato(caminho_contrato, lang=idioma_limpo)
                except TypeError:
                    engine_contrato.gerar_contrato(caminho_contrato)

            padronizar_pdf_iso_a4(caminho_contrato)
            resultados_geracao["06_Contrato_Licenciamento_Global"] = caminho_contrato
            print(f" -> Sucesso: {caminho_contrato}")
        except Exception as e:
            print(f" -> Erro na execução do Contrato Global: {e}")

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


if __name__ == "__main__":
    compilar_dossies_master(lang="PT")