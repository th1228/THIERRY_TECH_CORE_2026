# -*- coding: utf-8 -*-
"""
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
Avaliacao de fator fadiga, queda capilar, dinamica sanguinea/horarios
e criterios objetivos de encaminhamento medico para protocolo de plasma.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .diagnostico_capilar import AvaliacaoCapilar, _limitar_percentual
from .memoria_tricologia_helper import registrar_na_memoria_comum


@dataclass
class PlanoPlasmaFadiga:
    cliente: str
    fator_fadiga: float
    queda_ativa: bool
    velocidade_fluxo_sangue: float
    encaminhamento_medico_obrigatorio: bool
    criterios_encaminhamento: List[str]
    janela_horario_sugerida: str
    indicacao_plasma: str
    justificativa_tecnica: str
    etapas_protocolo: List[str] = field(default_factory=list)
    intervalo_sessoes_dias: int = 30

    def para_dict(self) -> Dict[str, Any]:
        return {
            "cliente": self.cliente,
            "fator_fadiga": self.fator_fadiga,
            "queda_ativa": self.queda_ativa,
            "velocidade_fluxo_sangue": self.velocidade_fluxo_sangue,
            "encaminhamento_medico_obrigatorio": self.encaminhamento_medico_obrigatorio,
            "criterios_encaminhamento": list(self.criterios_encaminhamento),
            "janela_horario_sugerida": self.janela_horario_sugerida,
            "indicacao_plasma": self.indicacao_plasma,
            "justificativa_tecnica": self.justificativa_tecnica,
            "etapas_protocolo": list(self.etapas_protocolo),
            "intervalo_sessoes_dias": self.intervalo_sessoes_dias,
        }


class ProtocoloPlasmaFadiga:
    """
    Avalia fadiga, queda capilar e indice de velocidade/dinamica sanguinea
    para definir janela de horario, cadencia e criterios de encaminhamento medico.
    """

    def avaliar_e_gerar(
        self,
        avaliacao: AvaliacaoCapilar,
        dados_adicionais: Dict[str, Any] | None = None,
    ) -> PlanoPlasmaFadiga:
        extra: Dict[str, Any] = dados_adicionais if isinstance(dados_adicionais, dict) else {}
        brutas = avaliacao.metricas_brutas if isinstance(avaliacao.metricas_brutas, dict) else {}

        fadiga_raw = extra.get("fator_fadiga", brutas.get("fator_fadiga", 100.0 - avaliacao.saude_couro_cabeludo))
        fator_fadiga = _limitar_percentual(fadiga_raw, 30.0)

        queda_raw = extra.get("queda_ativa", brutas.get("queda_ativa", avaliacao.indice_densidade_folicular < 75.0))
        queda_ativa = bool(queda_raw)

        # Indice de dinamica/velocidade do fluxo sanguineo (0 a 100)
        fluxo_padrao = round(max(10.0, min(95.0, (avaliacao.saude_couro_cabeludo * 0.6) + ((100.0 - fator_fadiga) * 0.4))), 2)
        fluxo_raw = extra.get(
            "velocidade_fluxo_sangue",
            extra.get("velocidade_sangue", brutas.get("velocidade_fluxo_sangue", fluxo_padrao)),
        )
        velocidade_fluxo = _limitar_percentual(fluxo_raw, fluxo_padrao)

        # Criterios objetivos de encaminhamento medico
        criterios: List[str] = []
        if avaliacao.saude_couro_cabeludo < 55.0:
            criterios.append(
                "Couro cabeludo abaixo de 55.0: investigar processo inflamatorio, infeccioso ou lesional antes de procedimento."
            )
        if queda_ativa and fator_fadiga >= 60.0:
            criterios.append(
                "Queda ativa associada a fadiga >= 60.0: avaliar causas sistemicas, hormonais, nutricionais ou efluvio."
            )
        if avaliacao.indice_densidade_folicular < 55.0:
            criterios.append(
                "Densidade folicular < 55.0: avaliar rarefacao avancada e risco de alopecia cicatricial/androgenetica."
            )
        if fator_fadiga >= 75.0:
            criterios.append(
                "Fator fadiga >= 75.0: quadro de fadiga acentuada; priorizar avaliacao medica antes de protocolo invasivo."
            )

        encaminhamento_obrigatorio = len(criterios) > 0
        if not criterios:
            criterios.append("Sem criterio critico imediato; manter acompanhamento e avaliacao clinica quando indicado.")

        # Janela de horario alinhada a dinamica de fluxo sanguineo e fadiga
        if velocidade_fluxo < 45.0 or fator_fadiga >= 65.0:
            janela_horario = "08:30 - 11:30 (fluxo mais baixo/estabilizando e menor desgaste acumulado no dia)"
        elif velocidade_fluxo >= 70.0 and fator_fadiga < 50.0:
            janela_horario = "15:00 - 18:00 (dinamica circulatoria mais ativa com fadiga controlada)"
        else:
            janela_horario = "14:00 - 17:00 (janela intermediaria de perfusao com monitoracao da fadiga)"

        # Indicacao de trilha de plasma e intervalo entre sessoes
        if encaminhamento_obrigatorio and queda_ativa:
            indicacao = "Encaminhamento Medico Prioritario para Avaliacao de Plasma"
            justificativa = (
                f"Ha criterio clinico de encaminhamento com queda ativa e fator de fadiga em {fator_fadiga}%; "
                "a avaliacao medica define elegibilidade e seguranca para aplicacao de plasma."
            )
            intervalo = 21
        elif queda_ativa and fator_fadiga >= 45.0:
            indicacao = "Elegivel para Trilha de Plasma sob Avaliacao Medica"
            justificativa = (
                f"Queda ativa com fadiga em {fator_fadiga}% e dinamica sanguinea em {velocidade_fluxo}; "
                "estruturar protocolo em janela compativel com o fluxo e a tolerancia do paciente."
            )
            intervalo = 21
        elif velocidade_fluxo >= 65.0 or avaliacao.indice_densidade_folicular < 75.0:
            indicacao = "Suporte Folicular e Avaliacao de Plasma Moderada"
            justificativa = (
                f"Parametros moderados (densidade {avaliacao.indice_densidade_folicular}%, fluxo {velocidade_fluxo}); "
                "acompanhar resposta folicular e cronograma."
            )
            intervalo = 30
        else:
            indicacao = "Manutencao sem Prioridade de Plasma"
            justificativa = (
                f"Quadro estavel com fadiga em {fator_fadiga}% e fluxo em {velocidade_fluxo}; "
                "manter rotina preventiva e reavaliacao periodica."
            )
            intervalo = 45

        etapas: List[str] = [
            f"Etapa 1 - Triagem e Fluxo Base: Registrar queda, fator de fadiga ({fator_fadiga}%) e indice de fluxo ({velocidade_fluxo}).",
            f"Etapa 2 - Agendamento na Janela: Priorizar atendimento na faixa {janela_horario}.",
            "Etapa 3 - Avaliacao e Execucao Clinica: Encaminhar ao medico responsavel para validacao e execucao do protocolo de plasma.",
            f"Etapa 4 - Reavaliacao de Ciclo: Retornar em {intervalo} dias para comparar densidade, fadiga e resposta folicular.",
        ]

        return PlanoPlasmaFadiga(
            cliente=avaliacao.cliente,
            fator_fadiga=fator_fadiga,
            queda_ativa=queda_ativa,
            velocidade_fluxo_sangue=velocidade_fluxo,
            encaminhamento_medico_obrigatorio=encaminhamento_obrigatorio,
            criterios_encaminhamento=criterios,
            janela_horario_sugerida=janela_horario,
            indicacao_plasma=indicacao,
            justificativa_tecnica=justificativa,
            etapas_protocolo=etapas,
            intervalo_sessoes_dias=intervalo,
        )
