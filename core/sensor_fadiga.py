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
Módulo: sensor_fadiga.py
Sistema: Thierry Technology Concept Global - Motor de Fadiga Biométrico & Climático
"""

import os
import random
from datetime import datetime

# Importação segura da Memória Comum do Ecossistema
try:
    from core.memoria_comum import memoria_global
except ImportError:
    try:
        from memoria_comum import memoria_global
    except ImportError:
        memoria_global = None

# Cores ANSI para exibição estilizada no terminal
RESET   = "\033[0m"
BOLD    = "\033[1m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
CYAN    = "\033[36m"
MAGENTA = "\033[35m"

class SensorFadigaClimatico:
    def __init__(self, temperatura_padrao: float = 27.0, umidade_padrao: float = 60.0, lang: str = "PT"):
        self.temperatura = temperatura_padrao
        self.umidade = umidade_padrao
        self._sincronizar_memoria()

    def _sincronizar_memoria(self):
        """Puxa os dados climáticos em tempo real da Memória Comum, se disponíveis."""
        if memoria_global:
            dados_clima = memoria_global.ler_dados("dados_climaticos")
            if dados_clima and 'clima_regional' in dados_clima:
                try:
                    partes = dados_clima['clima_regional'].split('|')
                    temp_str = partes[0].strip().split('°')[0]
                    umid_str = partes[1].strip().split(':')[1].replace('%', '').strip()
                    self.temperatura = float(temp_str)
                    self.umidade = float(umid_str)
                except Exception as e:
                    print(f"[SENSOR FADIGA AVISO] Usando valores padrão. Erro ao ler memória: {e}")

    def calcular_indice_fadiga_cutanea(self, micro_movimentos_faciais: int = 18) -> dict:
        """
        Cruza os dados climáticos da memória com os sinais faciais, 
        imprime no terminal e injeta o resultado de volta na Memória Comum.
        """
        self._sincronizar_memoria()

        fator_termico = max(0.0, (self.temperatura - 24.0) * 1.5)
        fator_higrometrico = max(0.0, (50.0 - self.umidade) * 0.8) if self.umidade < 50 else 0.0
        
        score_fadiga = min(max((micro_movimentos_faciais * 1.2) + fator_termico + fator_higrometrico, 5.0), 98.5)
        
        if score_fadiga > 70.0:
            status = f"{RED}ALERTA: Fadiga Crítica / Alta Desidratação Térmica{RESET}"
        elif score_fadiga > 40.0:
            status = f"{YELLOW}ATENÇÃO: Fadiga Moderada por Influência Ambiental{RESET}"
        else:
            status = f"{GREEN}ESTÁVEL: Boa Resiliência Cutânea e Térmica{RESET}"

        resultados = {
            "timestamp": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            "temperatura": f"{self.temperatura}°C",
            "umidade": f"{self.umidade}%",
            "micro_movimentos": micro_movimentos_faciais,
            "fator_termico": round(fator_termico, 1),
            "fator_higrometrico": round(fator_higrometrico, 1),
            "score_fadiga": round(score_fadiga, 1),
            "status": status
        }
        
        if memoria_global:
            memoria_global.salvar_dados("dados_fadiga", resultados)
            print("[MEMÓRIA] Dados de fadiga injetados com sucesso na Memória Comum.")

        self._imprimir_terminal(resultados)
        return resultados

    def _imprimir_terminal(self, res: dict):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        divisoria = f"{CYAN}" + "═" * 60 + f"{RESET}"
        linha_fina = f"{CYAN}" + "─" * 60 + f"{RESET}"

        print(divisoria)
        print(f"{BOLD}{MAGENTA}   DIAGNÓSTICO EM TEMPO REAL: SENSOR DE FADIGA & CLIMA{RESET}")
        print(divisoria)
        print(f" {YELLOW}Horário da Varredura :{RESET} {res['timestamp']}")
        print(f" {YELLOW}Temperatura Ambiente :{RESET} {BOLD}{res['temperatura']}{RESET}")
        print(f" {YELLOW}Umidade Relativa     :{RESET} {BOLD}{res['umidade']}{RESET}")
        print(f" {YELLOW}Micro-movimentos     :{RESET} {res['micro_movimentos']} vértices monitorados")
        print(f" {YELLOW}Impacto Térmico      :{RESET} +{res['fator_termico']} pts")
        print(f" {YELLOW}Impacto Higrométrico :{RESET} +{res['fator_higrometrico']} pts")
        print(linha_fina)
        print(f" {BOLD}SCORE DE FADIGA      :{RESET} {CYAN}{BOLD}{res['score_fadiga']}%{RESET}")
        print(f" {BOLD}ESTADO CLÍNICO       :{RESET} {res['status']}")
        print(divisoria + "\n")

if __name__ == "__main__":
    sensor = SensorFadigaClimatico()
    sensor.calcular_indice_fadiga_cutanea(micro_movimentos_faciais=16)