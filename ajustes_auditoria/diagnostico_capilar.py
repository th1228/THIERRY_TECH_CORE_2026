# -*- coding: utf-8 -*-
"""
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
Avaliacao deterministica de tricologia e saude do couro cabeludo.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
from .memoria_tricologia_helper import registrar_na_memoria_comum


def _carregar_memoria() -> Any:
    try:
        from memoria_comum import instancia_memoria as memoria
        try:
            _payload_mem = memoria.para_dict() if hasattr(memoria, 'para_dict') else memoria
            _cliente_mem = getattr(memoria, 'cliente', None) or getattr(memoria, 'nome_cliente', None) or 'Paciente / Cliente'
            registrar_na_memoria_comum('diagnostico_capilar', _payload_mem, cliente=_cliente_mem)
        except Exception:
            pass
        return memoria
    except ImportError:
        try:
            from core.memoria_comum import instancia_memoria as memoria
            try:
                _payload_mem = memoria.para_dict() if hasattr(memoria, 'para_dict') else memoria
                _cliente_mem = getattr(memoria, 'cliente', None) or getattr(memoria, 'nome_cliente', None) or 'Paciente / Cliente'
                registrar_na_memoria_comum('diagnostico_capilar', _payload_mem, cliente=_cliente_mem)
            except Exception:
                pass
            return memoria
        except ImportError:
            class _MemoriaFallback:
                def __init__(self) -> None:
                    self._dados: Dict[str, Any] = {}

                def salvar_dados(self, chave: str, valor: Any) -> bool:
                    self._dados[chave] = valor
                    return True

                def registrar(self, chave: str, valor: Any) -> bool:
                    self._dados[chave] = valor
                    return True

                def ler_dados(self, chave: str) -> Any:
                    return self._dados.get(chave)

            return _MemoriaFallback()


memoria = _carregar_memoria()


def _limitar_percentual(valor: Any, padrao: float) -> float:
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        try:
            _payload_mem = padrao.para_dict() if hasattr(padrao, 'para_dict') else padrao
            _cliente_mem = getattr(padrao, 'cliente', None) or getattr(padrao, 'nome_cliente', None) or 'Paciente / Cliente'
            registrar_na_memoria_comum('diagnostico_capilar', _payload_mem, cliente=_cliente_mem)
        except Exception:
            pass
        return padrao
    if numero < 0.0:
        return 0.0
    if numero > 100.0:
        return 100.0
    return round(numero, 2)


@dataclass
class AvaliacaoCapilar:
    cliente: str
    operador: str
    indice_densidade_folicular: float
    indice_integridade_fibra: float
    saude_couro_cabeludo: float
    score_geral_tricologia: float
    classificacao: str
    alertas: List[str] = field(default_factory=list)
    metricas_brutas: Dict[str, Any] = field(default_factory=dict)

    def para_dict(self) -> Dict[str, Any]:
        return {
            "cliente": self.cliente,
            "operador": self.operador,
            "indice_densidade_folicular": self.indice_densidade_folicular,
            "indice_integridade_fibra": self.indice_integridade_fibra,
            "saude_couro_cabeludo": self.saude_couro_cabeludo,
            "score_geral_tricologia": self.score_geral_tricologia,
            "classificacao": self.classificacao,
            "alertas": list(self.alertas),
            "metricas_brutas": dict(self.metricas_brutas),
        }


class DiagnosticoCapilar:
    """
    Motor deterministico de avaliacao tricologica.
    Consolida indicadores da fibra capilar e do couro cabeludo.
    """

    def __init__(self, operador: str = "Operador TTC") -> None:
        self.operador = operador.strip() if isinstance(operador, str) and operador.strip() else "Operador TTC"

    def avaliar(self, dados: Dict[str, Any] | None = None, cliente: str = "Paciente / Cliente") -> AvaliacaoCapilar:
        payload: Dict[str, Any] = dados if isinstance(dados, dict) else {}

        nome_resolvido = (
            str(payload.get("cliente") or payload.get("nome_cliente") or payload.get("nome") or cliente).strip()
            or "Paciente / Cliente"
        )

        densidade = _limitar_percentual(payload.get("densidade_folicular"), 80.0)
        integridade = _limitar_percentual(payload.get("integridade_fibra"), 75.0)
        couro = _limitar_percentual(payload.get("saude_couro_cabeludo"), 80.0)

        score_geral = round((densidade * 0.35) + (integridade * 0.35) + (couro * 0.30), 2)

        if score_geral >= 85.0:
            classificacao = "Alta Integridade"
        elif score_geral >= 65.0:
            classificacao = "Atencao Moderada"
        else:
            classificacao = "Intervencao Prioritaria"

        alertas: List[str] = []
        if densidade < 70.0:
            alertas.append("Densidade folicular abaixo do limiar ideal; avaliar afinamento e ciclo anageno.")
        if integridade < 70.0:
            alertas.append("Integridade da fibra comprometida; priorizar reposicao proteica e lipidica.")
        if couro < 70.0:
            alertas.append("Couro cabeludo com sinais de desequilibrio; investigar oleosidade, descamacao ou sensibilidade.")
        if not alertas:
            alertas.append("Parametros tricologicos dentro da faixa de manutencao preventiva.")

        avaliacao = AvaliacaoCapilar(
            cliente=nome_resolvido,
            operador=self.operador,
            indice_densidade_folicular=densidade,
            indice_integridade_fibra=integridade,
            saude_couro_cabeludo=couro,
            score_geral_tricologia=score_geral,
            classificacao=classificacao,
            alertas=alertas,
            metricas_brutas=payload,
        )

        try:
            memoria.salvar_dados(f"tricologia_ultimo_diagnostico_{nome_resolvido}", avaliacao.para_dict())
        except Exception:
            pass

        try:
            _payload_mem = avaliacao.para_dict() if hasattr(avaliacao, 'para_dict') else avaliacao
            _cliente_mem = getattr(avaliacao, 'cliente', None) or getattr(avaliacao, 'nome_cliente', None) or 'Paciente / Cliente'
            registrar_na_memoria_comum('diagnostico_capilar', _payload_mem, cliente=_cliente_mem)
        except Exception:
            pass
        return avaliacao
