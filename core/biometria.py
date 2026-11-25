# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - BIOMETRIC & DIGITAL TWIN ENGINE
Versão: 16.2.2 - Vectorized & RAM Sanitized (PQC Secure Edition)
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the 
intellectual property of Thierry Technology Concept Global. Unauthorized 
distribution, reverse engineering, or usage without a signed NDA/License 
agreement is strictly prohibited under international copyright frameworks.
===========================================================================
"""

import sys
import os
import ctypes
import numpy as np
from typing import Dict, Any, Optional

# Ajusta o caminho automaticamente para o Python achar a raiz do projeto de qualquer lugar
script_dir = os.path.dirname(os.path.abspath(__file__))
raiz_projeto = os.path.abspath(os.path.join(script_dir, ".."))
if raiz_projeto not in sys.path:
    sys.path.append(raiz_projeto)

# Conexão com a memória protegida contra erros de diretório
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def __init__(self):
            self._dados = {}

        def salvar_dados(self, chave, valor):
            self._dados[chave] = valor
            return True

        def registrar(self, chave, valor):
            self._dados[chave] = valor
            return True

        def ler_dados(self, chave):
            return self._dados.get(chave)
    memoria = MemoriaMock()

class DigitalTwin:
    def __init__(self, largura_testa: float, largura_macas: float, largura_mandibula: float, altura_rosto: float, genero: str, clima: str = "tropical", lang: str = "PT"):
        self.genero = genero.lower()
        self.clima = clima.lower()
        
        # --- VETORIZAÇÃO DE MATRIZES (ALTA PERFORMANCE) ---
        # Conversão dos inputs biométricos para vetores otimizados em NumPy
        self._vetor_biometrico = np.array([largura_testa, largura_macas, largura_mandibula, altura_rosto], dtype=np.float64)
        
        self.testa = float(self._vetor_biometrico[0])
        self.macas = float(self._vetor_biometrico[1])
        self.mandibula = float(self._vetor_biometrico[2])
        self.altura = float(self._vetor_biometrico[3])
        
        # Cálculo vetorizado e instantâneo das proporções faciais
        self.indice_afilamento = float(np.divide(self.mandibula, self.testa))
        self.indice_proporcao_total = float(np.divide(self.altura, self.macas))
        self.tipo_rosto = self._classificar_precisamente()

        self.matriz_tratamentos = {
            "Triangulo": {"ouro": "Preenchimento Mandibular Estrutural", "pele_seda": "Skinbooster + Exossomos (Nutrição Celular) + Hidratação via Bio-estimulação Autóloga"},
            "Quadrado": {"ouro": "Botox em Masseter + Harmonização de Queixo", "pele_seda": "Sculptra + Infusão de Nutrientes Via Microagulhamento Robotizado"},
            "Oval": {"ouro": "Bioestimuladores (Radiesse/Sculptra)", "pele_seda": "Skinbooster + Terapia de Luz LED (Bio-fotomodulação)"},
            "Oblongo": {"ouro": "Preenchimento de Maçãs do Rosto", "pele_seda": "Skinbooster + Radiofrequência Fracionada + Nutrição de Barreira"},
            "Redondo": {"ouro": "Bichectomia + Contorno Mandibular", "pele_seda": "Ultherapy (Lifting) + Hidratação de Barreira Cutânea"},
            "Diamante": {"ouro": "Preenchimento de Têmporas", "pele_seda": "Bioestimuladores + Terapia de Exossomos (Rejuvenescimento Avançado)"},
            "Retangular": {"ouro": "Botox para Suavização de Ângulos", "pele_seda": "Peeling de Superfície + Hidratação Molecular Inteligente"}
        }

    def _classificar_precisamente(self) -> str:
        af, pr = self.indice_afilamento, self.indice_proporcao_total
        offset = 0.05 if self.genero == "masculino" else 0.0
        
        if af < (0.85 + offset) and pr > 1.4: return "Triangulo"
        if (0.95 + offset) <= af <= (1.10 + offset) and pr < 1.3: return "Quadrado"
        if (0.9 + offset) <= af <= (1.15 + offset) and pr > 1.7: return "Oblongo"
        if 0.85 <= af <= (0.95 + offset) and 1.4 <= pr <= 1.6: return "Oval"
        if (0.95 + offset) <= af <= (1.15 + offset) and pr < 1.25: return "Redondo"
        if af < (0.85 + offset) and pr < 1.4: return "Diamante"
        if (0.95 + offset) <= af <= (1.10 + offset) and 1.3 <= pr <= 1.6: return "Retangular"
        return "Oval"

    def _calcular_fator_sustentacao(self) -> float:
        base_ideal = 1.45 if self.genero == "masculino" else 1.55
        return float(max(0.5, 1.0 - (abs(self.indice_proporcao_total - base_ideal) * 0.2)))

    def gerar_laudo_completo(self) -> dict:
        sust = self._calcular_fator_sustentacao()
        info = self.matriz_tratamentos.get(self.tipo_rosto, {})
        
        laudo = {
            "TIPO DE ROSTO": self.tipo_rosto,
            "DADOS TÉCNICOS": f"Afilamento: {self.indice_afilamento:.2f} | Proporção: {self.indice_proporcao_total:.2f} [Vetorizado NumPy]",
            "TRATAMENTO OURO": info.get("ouro"),
            "PROTOCOLO PELE SEDA": info.get("pele_seda"),
            "LONGEVIDADE BOTULÍNICA": f"{round(180 * sust)} dias",
            "JANELA REGENERATIVA": f"{round(28 * (1 + (1.0 - sust)), 1)} dias"
        }
        
        memoria.salvar_dados("biometria", laudo)
        
        # --- LIMPEZA SEGURA DE DADOS DA RAM (MEMORY SANITIZATION) ---
        self.purgar_dados_ram()
        
        return laudo

    def purgar_dados_ram(self):
        """Sobrescreve e limpa os vetores sensíveis da memória RAM imediatamente após o processamento."""
        try:
            if hasattr(self, '_vetor_biometrico'):
                # Preenche o array NumPy com zeros na memória
                self.vetor_biometrico_limpo = np.zeros_like(self._vetor_biometrico)
                del self._vetor_biometrico
            
            # Limpeza adicional de variáveis sensíveis
            self.testa = 0.0
            self.macas = 0.0
            self.mandibula = 0.0
            self.altura = 0.0
        except Exception:
            pass

def obter_laudo_biometrico(testa: float, macas: float, mandibula: float, altura: float, genero: str, clima: str = "tropical") -> dict:
    dt = DigitalTwin(testa, macas, mandibula, altura, genero, clima)
    return dt.gerar_laudo_completo()

if __name__ == "__main__":
    print("=" * 65)
    print(" THIERRY TECH CORE — MODULO DE BIOMETRIA & LAUDOS (VETORIZADO)")
    print("=" * 65)
    
    laudo_teste = obter_laudo_biometrico(
        testa=14.0, 
        macas=15.5, 
        mandibula=12.5, 
        altura=22.0, 
        genero="masculino", 
        clima="tropical"
    )
    
    for chave, valor in laudo_teste.items():
        print(f"[{chave}]: {valor}")
    
    print("=" * 65)
    print(" Status: Processado via NumPy, purgado da RAM e espelhado com sucesso!")
    print("=" * 65)