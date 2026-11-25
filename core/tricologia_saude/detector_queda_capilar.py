# -*- coding: utf-8 -*-
"""
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
Detector e quantificador de intensidade/queda capilar para Tricologia & Saude.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .diagnostico_capilar import AvaliacaoCapilar, _limitar_percentual
from .memoria_tricologia_helper import registrar_na_memoria_comum


@dataclass
class ResultadoQuedaCapilar:
    cliente: str
    indice_queda: float
    nivel_queda: str
    queda_ativa: bool
    fios_observados_dia: int | None
    sinais_detectados: List[str] = field(default_factory=list)
    recomendacao_imediata: str = ""

    def para_dict(self) -> Dict[str, Any]:
        return {
            "cliente": self.cliente,
            "indice_queda": self.indice_queda,
            "nivel_queda": self.nivel_queda,
            "queda_ativa": self.queda_ativa,
            "fios_observados_dia": self.fios_observados_dia,
            "sinais_detectados": list(self.sinais_detectados),
            "recomendacao_imediata": self.recomendacao_imediata,
        }


def _converter_inteiro_positivo(valor: Any) -> int | None:
    if valor is None or isinstance(valor, bool):
        return None
    try:
        numero = int(float(valor))
    except (TypeError, ValueError):
        return None
    return max(0, numero)


class DetectorQuedaCapilar:
    """
    Avalia a intensidade e os sinais de queda capilar a partir de metricas
    observadas ou da avaliacao capilar base.
    """

    def detectar(
        self,
        avaliacao: AvaliacaoCapilar | None = None,
        dados: Dict[str, Any] | None = None,
    ) -> ResultadoQuedaCapilar:
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

        fios_dia = _converter_inteiro_positivo(
            payload.get("fios_queda_dia", payload.get("fios_observados_dia", brutas.get("fios_queda_dia")))
        )

        densidade = (
            avaliacao.indice_densidade_folicular
            if avaliacao is not None
            else _limitar_percentual(payload.get("densidade_folicular"), 80.0)
        )
        couro = (
            avaliacao.saude_couro_cabeludo
            if avaliacao is not None
            else _limitar_percentual(payload.get("saude_couro_cabeludo"), 80.0)
        )

        # Componente de queda por fios observados no dia (referencia: > 100 fios/dia passa a elevar o indice)
        if fios_dia is not None:
            score_fios = _limitar_percentual((fios_dia / 180.0) * 100.0, 20.0)
        else:
            score_fios = _limitar_percentual(payload.get("indice_queda_observado", brutas.get("indice_queda_observado")), 25.0)

        deficit_densidade = _limitar_percentual(100.0 - densidade, 20.0)
        deficit_couro = _limitar_percentual(100.0 - couro, 20.0)

        indice_queda = round((score_fios * 0.50) + (deficit_densidade * 0.30) + (deficit_couro * 0.20), 2)

        sinais: List[str] = []
        if fios_dia is not None:
            if fios_dia > 100:
                sinais.append(f"Contagem diaria elevada ({fios_dia} fios observados acima do patamar de referencia de 100/dia).")
            else:
                sinais.append(f"Contagem diaria em {fios_dia} fios observados.")
        if densidade < 70.0:
            sinais.append(f"Densidade folicular reduzida ({densidade}%).")
        if couro < 70.0:
            sinais.append(f"Alteracao no couro cabeludo ({couro}%) favorecendo desprendimento/fragilidade.")

        if indice_queda >= 65.0:
            nivel = "Critica"
            queda_ativa = True
            recomendacao = "Queda intensa/critica: priorizar avaliacao clinica/medica e protocolo direcionado."
        elif indice_queda >= 40.0:
            nivel = "Moderada a Alta"
            queda_ativa = True
            recomendacao = "Queda ativa relevante: monitorar evolucao, proteger couro cabeludo e avaliar protocolo de plasma."
        elif indice_queda >= 25.0 or (fios_dia is not None and fios_dia > 100):
            nivel = "Leve a Moderada"
            queda_ativa = True
            recomendacao = "Sinais iniciais de queda ativa: acompanhar contagem e manter rotina de suporte folicular."
        else:
            nivel = "Baixa / Fisiologica"
            queda_ativa = False
            recomendacao = "Sem queda acentuada detectada: manter acompanhamento preventivo."

        if not sinais:
            sinais.append("Sem sinais criticos adicionais informados na leitura atual.")

        return ResultadoQuedaCapilar(
            cliente=cliente,
            indice_queda=indice_queda,
            nivel_queda=nivel,
            queda_ativa=queda_ativa,
            fios_observados_dia=fios_dia,
            sinais_detectados=sinais,
            recomendacao_imediata=recomendacao,
        )
