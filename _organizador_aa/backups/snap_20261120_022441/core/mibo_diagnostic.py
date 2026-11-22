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
import sys
import os
import json

# --- CORREÇÃO DE CAMINHO ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# --- IMPORTAÇÕES SEGURAS DO NÚCLEO (CORE) ---
try:
    from core.memoria_comum import instancia_memoria as memoria
    print("[INTEGRADOR] Memoria comum carregada com sucesso.")
except Exception as e:
    memoria = None
    print(f"[ERRO MEMORIA] Falha ao carregar memoria_comum: {e}")

try:
    from core.protocolo_logica import processar_protocolo
except ImportError:
    processar_protocolo = None

try:
    from core import motor_biometrico
except ImportError:
    motor_biometrico = None

# Importação correta apontando para a pasta core onde o Sovereign está localizado
try:
    from core.c2_sovereign_intelligence import SovereignC2DefenseEngine
    print("[INTEGRADOR] SovereignC2DefenseEngine carregado com sucesso da pasta core!")
except Exception as e:
    SovereignC2DefenseEngine = None
    print(f"[ERRO DE IMPORTAÇÃO] Falha ao carregar SovereignC2DefenseEngine: {e}")

class MonacoIntegrador:
    def __init__(self):
        print("[INTEGRADOR] Motor de consolidação de dados ativado.")

    def processar(self):
        """Ponto de convergência: consolida tudo o que foi gravado pelos módulos."""
        print("[INTEGRADOR] Consolidando resultados de todos os módulos...")
        return self.integrar_resultados()

    def integrar_resultados(self):
        """Unifica os dados e dispara a geração do relatório."""
        print("[INTEGRADOR] Unificando perícia e gerando estrutura final...")
        
        # 1. Coleta dados com segurança do motor biométrico
        emg = motor_biometrico.get_emg() if motor_biometrico and hasattr(motor_biometrico, 'get_emg') else 0
        vfc = motor_biometrico.get_vfc() if motor_biometrico and hasattr(motor_biometrico, 'get_vfc') else 0
        fase = processar_protocolo(emg, vfc, True) if processar_protocolo else "Fase Base"
        
        # 2. Estrutura
        dados_biometricos = {
            "CLIENTE": "Thierry",
            "SCANNER_OSTEOMETRIA": str(emg),
            "STATUS_SISTEMA": fase
        }
        
        if memoria and hasattr(memoria, 'salvar_dados'):
            try:
                memoria.salvar_dados("BIOMETRIA", dados_biometricos)
            except Exception as e:
                print(f"[AVISO MEMORIA] Erro ao salvar dados biométricos: {e}")
        
        # 3. Consolidação final
        dados_ambiente = memoria.ler_dados("ambiente") if memoria and hasattr(memoria, 'ler_dados') else {}
        dados_consciencia = memoria.ler_dados("consciencia") if memoria and hasattr(memoria, 'ler_dados') else {}
        dados_eminencia = memoria.ler_dados("eminencia") if memoria and hasattr(memoria, 'ler_dados') else {}

        relatorio_consolidado = {
            "BIOMETRIA": dados_biometricos,
            "ambiente": dados_ambiente,
            "consciencia": dados_consciencia,
            "eminencia": dados_eminencia,
            "fase_protocolo": fase
        }
        
        if memoria and hasattr(memoria, 'salvar_dados'):
            try:
                memoria.salvar_dados("integrador", relatorio_consolidado)
            except Exception as e:
                print(f"[AVISO MEMORIA] Erro ao salvar integrador: {e}")
        
        # 4. GERAÇÃO SEGURA DO DOSSIÊ MASTER (SOVEREIGN C2 DEFENSE ENGINE)
        try:
            print("[INTEGRADOR] Disparando Sovereign C2 Defense Engine...")
            if SovereignC2DefenseEngine:
                engine = SovereignC2DefenseEngine(
                    codinome_lider="Thierry (Diretor Executivo)",
                    entidade_soberana="Thierry Technology Concept Global",
                    setor_atuacao="Infraestrutura Tecnológica & Soberania Digital",
                    aum_bilhoes_eur=25.0,
                    fator_ameaca_mercado=0.35
                )
                
                if hasattr(engine, 'gerar_pdf_defensivo_soberano'):
                    pdf_gerado = engine.gerar_pdf_defensivo_soberano("c2_sovereign_intelligence_dossier.pdf")
                    print(f"[INTEGRADOR] Dossiê gerado com sucesso em: {pdf_gerado}")
                else:
                    print("[AVISO] Método de geração de PDF não encontrado no motor soberano.")
            else:
                print("[AVISO] SovereignC2DefenseEngine não foi carregado corretamente.")
        except Exception as e:
            print(f"[ERRO NO GERADOR DE RELATÓRIO] Detalhes: {e}")

        # 5. DESPEJO DE TELEMETRIA DA MEMÓRIA COMUM NO TERMINAL
        print("\n" + "="*60)
        print("[MEMÓRIA COMUM] ESTADO ATUAL DOS DADOS INTEGRADOS NO SISTEMA:")
        print("="*60)
        if memoria and hasattr(memoria, 'obter_todos_dados'):
            for chave, valor in memoria.obter_todos_dados().items():
                print(f" -> [{chave}]: {valor}")
        elif memoria and hasattr(memoria, 'dados'):
            for chave, valor in memoria.dados.items():
                print(f" -> [{chave}]: {valor}")
        else:
            print(json.dumps(relatorio_consolidado, indent=2, ensure_ascii=False))
        print("="*60 + "\n")
        
        print("[INTEGRADOR] Estrutura final gerada com sucesso.")
        return True

# --- INSTÂNCIA DO SERVIÇO ---
service_integrador = MonacoIntegrador()

# --- INTERFACES DE EXECUÇÃO ---
def rodar():
    return service_integrador.processar()

def sincronizar():
    return service_integrador.processar()

def iniciar():
    return service_integrador.processar()

if __name__ == "__main__":
    service_integrador.processar()