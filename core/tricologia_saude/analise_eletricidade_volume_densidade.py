# -*- coding: utf-8 -*-
"""
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
Analise da eletricidade do fio (carga eletrostatica), correlacao com
densidade e volume capilar e tratamentos direcionados.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .diagnostico_capilar import AvaliacaoCapilar, _limitar_percentual
from .memoria_tricologia_helper import registrar_na_memoria_comum


@dataclass
class RelatorioEletricidadeVolumeDensidade:
    cliente: str
    eletricidade_fio: float
    densidade_capilar: float
    volume_aparente: float
    estado_eletrico: str
    correlacao_densidade_volume: str
    tratamentos_adequados: List[str] = field(default_factory=list)
    cuidados_praticos: List[str] = field(default_factory=list)
    intervalo_reavaliacao_dias: int = 21

    def para_dict(self) -> Dict[str, Any]:
        return {
            "cliente": self.cliente,
            "eletricidade_fio": self.eletricidade_fio,
            "densidade_capilar": self.densidade_capilar,
            "volume_aparente": self.volume_aparente,
            "estado_eletrico": self.estado_eletrico,
            "correlacao_densidade_volume": self.correlacao_densidade_volume,
            "tratamentos_adequados": list(self.tratamentos_adequados),
            "cuidados_praticos": list(self.cuidados_praticos),
            "intervalo_reavaliacao_dias": self.intervalo_reavaliacao_dias,
        }


class AnaliseEletricidadeVolumeDensidade:
    """
    Avalia a eletricidade do fio e sua relacao com densidade e volume,
    indicando protocolos de tratamento ajustados ao quadro.
    """

    def analisar(
        self,
        avaliacao: AvaliacaoCapilar | None = None,
        dados: Dict[str, Any] | None = None,
    ) -> RelatorioEletricidadeVolumeDensidade:
        payload: Dict[str, Any] = dados if isinstance(dados, dict) else {}
        brutas: Dict[str, Any] = (
            avaliacao.metricas_brutas
            if avaliacao is not None and isinstance(avaliacao.metricas_brutas, dict)
            else {}
        )

        cliente = (
            str(
                payload.get("cliente")
                or brutas.get("cliente")
                or (avaliacao.cliente if avaliacao is not None else "Paciente / Cliente")
            ).strip()
            or "Paciente / Cliente"
        )

        eletricidade = _limitar_percentual(
            payload.get(
                "eletricidade_fio",
                payload.get("carga_eletrica_fio", brutas.get("eletricidade_fio")),
            ),
            35.0,
        )

        densidade = (
            avaliacao.indice_densidade_folicular
            if avaliacao is not None
            else _limitar_percentual(
                payload.get("densidade_folicular", payload.get("densidade_capilar")),
                80.0,
            )
        )

        # Se nao vier volume explicito, estima um patamar inicial a partir da eletricidade e densidade
        volume_padrao = round(
            max(10.0, min(100.0, (densidade * 0.55) + (eletricidade * 0.45))),
            2,
        )
        volume = _limitar_percentual(
            payload.get("volume_aparente", payload.get("volume_fio", brutas.get("volume_aparente"))),
            volume_padrao,
        )

        tratamentos: List[str] = []
        cuidados: List[str] = []

        if eletricidade >= 65.0:
            estado_eletrico = "Alta Carga Eletrostatica / Repulsao Elevada"
            correlacao = (
                f"Eletricidade alta ({eletricidade}%) eleva a repulsao entre os fios e infla o volume aparente "
                f"({volume}%) independentemente da densidade real ({densidade}%), gerando fios arrepiados/volateis."
            )
            tratamentos.extend([
                "Tratamento antiestatico e condicionamento catiônico para neutralizar cargas superficiais e reduzir repulsao.",
                "Reposicao hidrica + selagem lipidica leve para aumentar a condutividade/estabilidade da fibra e baixar o frizz eletrico.",
            ])
            cuidados.extend([
                "Evitar atrito excessivo com tecidos sinteticos ou escovacao a seco agressiva.",
                "Manter hidratacao da fibra em dia, especialmente em ambientes secos ou com ar-condicionado.",
            ])
            intervalo = 15
        elif eletricidade >= 40.0:
            estado_eletrico = "Carga Eletrica Moderada / Instabilidade de Volume"
            correlacao = (
                f"Eletricidade moderada ({eletricidade}%) influencia parcialmente o volume ({volume}%) sobre uma "
                f"densidade de {densidade}%, exigindo equilibrio entre corpo e controle de dispersao dos fios."
            )
            tratamentos.extend([
                "Alinhamento cuticular suave e nutricao equilibrada para estabilizar o volume sem tirar o movimento natural.",
                "Uso de finalizador leve com acao anti-frizz para controlar fios soltos sem pesar.",
            ])
            cuidados.extend([
                "Controlar temperatura de secador/ferramentas termicas e usar protetor termico.",
                "Evitar excesso de produto pesado na raiz se o objetivo for manter volume controlado.",
            ])
            intervalo = 21
        else:
            estado_eletrico = "Carga Eletrica Baixa / Estavel"
            correlacao = (
                f"Eletricidade baixa ({eletricidade}%): o volume aparente ({volume}%) reflete mais de perto a "
                f"densidade ({densidade}%) e o peso/caimento natural da fibra do que repulsao eletrostatica."
            )
            if volume < 50.0 or densidade < 70.0:
                tratamentos.extend([
                    "Protocolo de encorpamento e leveza: reposicao de massa/aminoacidos e limpeza equilibrada para nao pesar a raiz.",
                    "Estimulo de densidade e suporte folicular quando houver afinamento ou queda associada.",
                ])
                cuidados.extend([
                    "Evitar excesso de oleos pesados ou cremes densos proximos ao couro cabeludo.",
                    "Priorizar finalizacao que preserve raiz solta e corpo estrutural.",
                ])
            else:
                tratamentos.extend([
                    "Manutencao preventiva com hidratacao, nutricao e reconstrucao leve para preservar densidade, corpo e brilho.",
                ])
                cuidados.extend([
                    "Manter rotina regular de cuidados e reavaliacao periodica.",
                ])
            intervalo = 30

        return RelatorioEletricidadeVolumeDensidade(
            cliente=cliente,
            eletricidade_fio=eletricidade,
            densidade_capilar=densidade,
            volume_aparente=volume,
            estado_eletrico=estado_eletrico,
            correlacao_densidade_volume=correlacao,
            tratamentos_adequados=tratamentos,
            cuidados_praticos=cuidados,
            intervalo_reavaliacao_dias=intervalo,
        )
