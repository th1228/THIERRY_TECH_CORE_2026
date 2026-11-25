# -*- coding: utf-8 -*-
"""
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
Gerador deterministico de protocolos de reconstrucao e manutencao tricologica.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .diagnostico_capilar import AvaliacaoCapilar, DiagnosticoCapilar
from .memoria_tricologia_helper import registrar_na_memoria_comum


@dataclass
class PlanoTratamentoCapilar:
    cliente: str
    score_origem: float
    classificacao_origem: str
    fases: List[str] = field(default_factory=list)
    cuidados_domiciliares: List[str] = field(default_factory=list)
    frequencia_reavaliacao_dias: int = 30

    def para_dict(self) -> Dict[str, Any]:
        return {
            "cliente": self.cliente,
            "score_origem": self.score_origem,
            "classificacao_origem": self.classificacao_origem,
            "fases": list(self.fases),
            "cuidados_domiciliares": list(self.cuidados_domiciliares),
            "frequencia_reavaliacao_dias": self.frequencia_reavaliacao_dias,
        }


class ProtocoloReconstrucao:
    """
    Traduz uma avaliacao tricologica em etapas objetivas de tratamento.
    """

    def __init__(self, diagnostico_motor: DiagnosticoCapilar | None = None) -> None:
        self.diagnostico_motor = diagnostico_motor or DiagnosticoCapilar()

    def gerar_plano(self, avaliacao: AvaliacaoCapilar) -> PlanoTratamentoCapilar:
        fases: List[str] = [
            "Fase 1 - Higienizacao e Preparacao: Equilibrio do couro cabeludo e remocao de residuos/metais antes de ativos intensivos.",
            "Fase 2 - Reconstrucao e Selagem: Reposicao estrutural da fibra e alinhamento cuticular conforme deficit identificado.",
        ]

        cuidados: List[str] = [
            "Evitar excesso termico direto sem protecao termica adequada.",
            "Manter rotina de limpeza suave respeitando a sensibilidade do couro cabeludo.",
        ]

        frequencia = 30
        if avaliacao.score_geral_tricologia < 65.0:
            fases.append("Fase 3 - Acompanhamento Intensivo: Sessoes quinzenais com monitoramento fotografico e tricoscopico.")
            cuidados.append("Realizar check-in quinzenal para ajuste fino de ativos e tolerancia.")
            frequencia = 15
        elif avaliacao.score_geral_tricologia < 85.0:
            fases.append("Fase 3 - Consolidacao: Manutencao periodica para estabilizar elasticidade e brilho.")
            frequencia = 30
        else:
            fases.append("Fase 3 - Blindagem Preventiva: Rotina de preservacao da fibra e longevidade capilar.")
            frequencia = 45

        return PlanoTratamentoCapilar(
            cliente=avaliacao.cliente,
            score_origem=avaliacao.score_geral_tricologia,
            classificacao_origem=avaliacao.classificacao,
            fases=fases,
            cuidados_domiciliares=cuidados,
            frequencia_reavaliacao_dias=frequencia,
        )
