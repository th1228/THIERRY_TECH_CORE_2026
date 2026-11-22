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

# =====================================================================
# ARQUIVO: security/geo_defense.py
# Módulo de Blindagem Geoespacial, Sub-licenças e Soberania Territorial
# =====================================================================

import sys
import os
import math
from typing import List, Tuple, Dict

# TÉCNICA DE BLINDAGEM DE PATH: Força o Python a enxergar a raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from security.log_seguro import LogSeguro

logger = LogSeguro()

class GeoDefense:
    
    # Raio da Terra em Quilômetros para o cálculo trigonométrico
    RAIO_TERRA_KM = 6371.0

    @staticmethod
    def _modo_desenvolvedor_ativo() -> bool:
        """Verifica se está em modo desenvolvedor (ignora restrições no seu notebook)."""
        return os.getenv("TTC_DEV_MODE", "false").lower() == "true"

    @classmethod
    def calcular_distancia(cls, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcula a distância real em quilômetros entre dois pontos usando a fórmula de Haversine."""
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        
        c = 2 * math.asin(math.sqrt(a))
        return cls.RAIO_TERRA_KM * c

    @classmethod
    def validar_perimetro_interno_loja(cls, gps_atual: Tuple[float, float], gps_autorizado: Tuple[float, float], tolerancia_metros: float = 30.0) -> bool:
        """
        Garante que o software/hardware só rode estritamente dentro da unidade (Master ou Satélite) licenciada,
        com tolerância fixa de 30 metros para cobrir o espaço físico sem falsos bloqueios.
        """
        if cls._modo_desenvolvedor_ativo():
            logger.registrar("SISTEMA", "DEV_MODE_BYPASS", "GeoDefense Interno ignorado por estar em Modo Desenvolvedor.")
            return True

        distancia_km = cls.calcular_distancia(gps_atual[0], gps_atual[1], gps_autorizado[0], gps_autorizado[1])
        distancia_metros = distancia_km * 1000.0
        
        if distancia_metros <= tolerancia_metros:
            logger.registrar("SISTEMA", "GEO_INTERNO_SUCCESS", f"Unidade validada dentro do perímetro físico de 30m. Desvio: {distancia_metros:.1f}m.")
            return True
        else:
            logger.registrar("SISTEMA", "FRAUDE_GEO_MIGRACAO", f"Alerta crítico: Tentativa de uso fora da unidade autorizada! Desvio de {distancia_metros:.1f}m.")
            return False

    @classmethod
    def validar_soberania_territorial(cls, novo_ponto: Tuple[float, float], nos_masters_existentes: List[Tuple[float, float]], distancia_minima_km: float = 100.0) -> bool:
        """
        Garante a exclusividade global de 100 km entre os 10 Nós Masters do mundo.
        Nenhuma nova licença master pode ser ativada a menos de 100 km de um master existente.
        """
        if cls._modo_desenvolvedor_ativo():
            return True

        for i, m_existente in enumerate(nos_masters_existentes):
            distancia = cls.calcular_distancia(novo_ponto[0], novo_ponto[1], m_existente[0], m_existente[1])
            if distancia < distancia_minima_km:
                logger.registrar("SISTEMA", "GEO_VIOLATION_SOVEREIGNTY", f"Conflito Master: Ponto a {distancia:.2f} km do Master {i+1} (Mínimo: {distancia_minima_km}km).")
                return False
        return True

    @classmethod
    def validar_sub_licenca_satelite(cls, gps_satelite: Tuple[float, float], master_proprietario: Tuple[float, float], raio_maximo_master_km: float = 100.0) -> bool:
        """
        Valida se um sub-nó (satélite) criado por um cliente Master está operando 
        estritamente dentro da zona de dominação de 100 km pertencente àquele Master.
        """
        if cls._modo_desenvolvedor_ativo():
            return True

        distancia = cls.calcular_distancia(gps_satelite[0], gps_satelite[1], master_proprietario[0], master_proprietario[1])
        
        if distancia <= raio_maximo_master_km:
            logger.registrar("SISTEMA", "SUB_NODE_SUCCESS", f"Sub-licença validada dentro do império de 100km do Master. Distância: {distancia:.2f}km.")
            return True
        else:
            logger.registrar("SISTEMA", "SUB_NODE_VIOLATION", f"Violação de Franquia: Sub-nó tentou operar fora do raio de {raio_maximo_master_km}km do Master proprietário ({distancia:.2f}km).")
            return False

# BLOCO DE TESTE AUTOMÁTICO
if __name__ == "__main__":
    print("--- TESTE DA ARQUITETURA DE FRANQUIAS E SOBERANIA GLOBAL ---")
    
    # Coordenada do Nó Master (Ex: Mônaco)
    master_monaco = (-2.5307, -44.3068)
    
    # Coordenada de um Sub-nó (Satélite) criado pelo Master dentro dos 100 km permitidos
    satelite_valido = (-2.4800, -44.2800)
    
    # Validação do Sub-nó
    status_sub = GeoDefense.validar_sub_licenca_satelite(satelite_valido, master_monaco, 100.0)
    print(f"Ativação de Sub-nó Satélite dentro do império (Esperado True): {status_sub}")