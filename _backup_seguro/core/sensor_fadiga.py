# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
Módulo: sensor_fadiga_climatico.py
Versão: 6.1.0 - TIER-1 DYNAMIC USER RESOLVER
===========================================================================
"""

import os
import datetime
import hashlib
import math
from typing import Dict, Any, Tuple, Optional

# --- PONTE DE MEMÓRIA AUTOMÁTICA (THIERRY TECH) ---
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:
        class MemoriaMock:
            def __init__(self):
                self.db = {}
            def salvar_dados(self, chave: str, valor: Any): self.db[chave] = valor
            def ler_dados(self, chave: str) -> Any: return self.db.get(chave, None)
        memoria = MemoriaMock()

# Cores ANSI para o terminal estilo Centro de Comando (C2)
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

class SensorFadigaClimaticoTier1:
    """
    Motor Ultra-Performance de Telemetria Biométrica com Identificação Dinâmica de Operador.
    """
    def __init__(self, usuario: Optional[str] = None):
        # Resolução Dinâmica: Argumento direto > Memória Comum > Fallback Soberano
        resolvedor_nome = (
            usuario 
            or memoria.ler_dados("nome_cliente") 
            or memoria.ler_dados("titular") 
            or memoria.ler_dados("operador_ativo") 
            or "OPERADOR UHNW"
        )
        self.usuario = str(resolvedor_nome).upper()
        
    def _calcular_fator_circadiano(self) -> float:
        """[CRONOBIOLOGIA ATIVA] Aplica multiplicador biológico baseado no horário do sistema."""
        hora_atual = datetime.datetime.now().hour
        if 16 <= hora_atual <= 19:
            return 1.15  # Pico do fim da tarde
        elif 0 <= hora_atual <= 5:
            return 1.30  # Janela Crítica da Madrugada
        elif 6 <= hora_atual <= 11:
            return 0.85  # Alta Performance Matinal
        else:
            return 1.00  # Platô Base

    def _analisar_tendencia_temporal(self, score_atual: float) -> Tuple[float, str]:
        """[ANÁLISE DE TENDÊNCIA VETORIAL] Compara com o histórico dinâmico do operador."""
        chave_historico = f"historico_fadiga_{self.usuario}"
        historico_passado = memoria.ler_dados(chave_historico)
        
        if not historico_passado or not isinstance(historico_passado, dict):
            return 0.0, "Estável (Primeira Leitura)"
        
        score_anterior = historico_passado.get("score_fadiga", score_atual)
        if score_anterior == 0:
            score_anterior = 1.0
            
        delta_percentual = ((score_atual - score_anterior) / score_anterior) * 100.0
        
        if delta_percentual > 0:
            status_tendencia = f"+{delta_percentual:.1f}% vs leitura anterior (Aceleração)"
        elif delta_percentual < 0:
            status_tendencia = f"{delta_percentual:.1f}% vs leitura anterior (Recuperação)"
        else:
            status_tendencia = "Estável (Sem variação)"
            
        return delta_percentual, status_tendencia

    def executar_varredura(self, micro_movimentos_fixos: float = 12.5) -> Dict[str, Any]:
        """Executa a telemetria unindo clima, biometria, cronobiologia e criptografia."""
        print("=" * 70)
        print(f"{BOLD}{CYAN}THIERRY TECH C2 - SENSOR DE FADIGA BIOMÉTRICA TIER-1{RESET}")
        print(f"Data/Hora: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 70)

        # 1. Coleta de Inputs Inteligentes
        clima_memoria = memoria.ler_dados("dados_climaticos") or {}
        temperatura = clima_memoria.get("temperatura", 27.0)
        umidade = clima_memoria.get("umidade", 60.0)

        # 2. Processamento Não-Linear
        impacto_termico = max(0.0, (temperatura - 22.0) * 0.4)
        impacto_higrometrico = max(0.0, (umidade - 50.0) * 0.1)
        score_base = micro_movimentos_fixos + impacto_termico + impacto_higrometrico
        
        # 3. Vetor Circadiano
        fator_tempo = self._calcular_fator_circadiano()
        score_modulado = min(100.0, max(0.0, score_base * fator_tempo))

        # 4. Tendência Temporal
        delta, tendencia_txt = self._analisar_tendencia_temporal(score_modulado)

        # 5. Assinatura SHA-256
        timestamp_iso = datetime.datetime.now().isoformat()
        payload = f"{self.usuario}|{score_modulado:.4f}|{temperatura}|{umidade}|{timestamp_iso}"
        integrity_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest().upper()

        # 6. Consolidação do Pacote C2
        dados_fadiga = {
            "usuario": self.usuario,
            "timestamp": timestamp_iso,
            "score_fadiga": round(score_modulado, 2),
            "fator_circadiano": fator_tempo,
            "delta_aceleracao": round(delta, 2),
            "clima_referencia": {"temp": temperatura, "umi": umidade},
            "integrity_hash": integrity_hash
        }

        # Persistência na Memória Comum
        memoria.salvar_dados(f"historico_fadiga_{self.usuario}", dados_fadiga)
        memoria.salvar_dados("dados_fadiga", dados_fadiga)

        # 7. Output no Terminal
        cor_alerta = GREEN if score_modulado < 35 else (YELLOW if score_modulado < 65 else RED)
        
        print(f"  • Usuário Monitorado  : {self.usuario}")
        print(f"  • Temperatura / UR    : {temperatura}°C | {umidade}%")
        print(f"  • Modulador Circadiano: {fator_tempo:.2f}x")
        print(f"  • Tendência Temporal  : {cor_alerta}{tendencia_txt}{RESET}")
        print(f"  • {BOLD}SCORE DE FADIGA REAL : {cor_alerta}{score_modulado:.2f}%{RESET}")
        print(f"  • SHA-256 BLOCK HASH  : {CYAN}{integrity_hash}{RESET}")
        print("=" * 70)

        return dados_fadiga


if __name__ == "__main__":
    # Exemplo 1: Sem passar nada, ele busca automaticamente da memória ou assume o padrão UHNW
    sensor_padrao = SensorFadigaClimaticoTier1()
    sensor_padrao.executar_varredura(micro_movimentos_fixos=14.0)
    
    # Exemplo 2: Passando o nome dinamicamente vindo de uma requisição ou painel
    sensor_dinamico = SensorFadigaClimaticoTier1(usuario="Thierry TCC")
    sensor_dinamico.executar_varredura(micro_movimentos_fixos=18.5)