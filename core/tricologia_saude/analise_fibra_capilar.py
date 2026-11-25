# -*- coding: utf-8 -*-
"""
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
Analise avancada da fibra capilar: saude do fio, espessura, idade,
refletancia, saude hidrica e tratamentos direcionados por deficiencia.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .diagnostico_capilar import _limitar_percentual
from .memoria_tricologia_helper import registrar_na_memoria_comum


@dataclass
class DiagnosticoFibraCapilar:
    cliente: str
    saude_fio: float
    espessura_fio: float
    idade_fio_anos_estimada: float
    indice_envelhecimento_fibra: float
    refletancia_fio: float
    saude_hidrica_fio: float
    score_fibra: float
    deficiencias_detectadas: List[str] = field(default_factory=list)
    tratamentos_por_deficiencia: Dict[str, List[str]] = field(default_factory=dict)

    def para_dict(self) -> Dict[str, Any]:
        return {
            "cliente": self.cliente,
            "saude_fio": self.saude_fio,
            "espessura_fio": self.espessura_fio,
            "idade_fio_anos_estimada": self.idade_fio_anos_estimada,
            "indice_envelhecimento_fibra": self.indice_envelhecimento_fibra,
            "refletancia_fio": self.refletancia_fio,
            "saude_hidrica_fio": self.saude_hidrica_fio,
            "score_fibra": self.score_fibra,
            "deficiencias_detectadas": list(self.deficiencias_detectadas),
            "tratamentos_por_deficiencia": {
                k: list(v) for k, v in self.tratamentos_por_deficiencia.items()
            },
        }


def _converter_float_positivo(valor: Any, padrao: float) -> float:
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        try:
            _payload_mem = padrao.para_dict() if hasattr(padrao, 'para_dict') else padrao
            _cliente_mem = getattr(padrao, 'cliente', None) or getattr(padrao, 'nome_cliente', None) or 'Paciente / Cliente'
            registrar_na_memoria_comum('fibra_capilar', _payload_mem, cliente=_cliente_mem)
        except Exception:
            pass
        return padrao
    return max(0.0, round(numero, 2))


class AnaliseFibraCapilar:
    """
    Avalia os indicadores da fibra capilar e associa protocolos de tratamento
    especificos para cada deficiencia identificada.
    """

    def analisar(self, dados: Dict[str, Any] | None = None, cliente: str = "Paciente / Cliente") -> DiagnosticoFibraCapilar:
        payload: Dict[str, Any] = dados if isinstance(dados, dict) else {}

        nome = (
            str(payload.get("cliente") or payload.get("nome_cliente") or payload.get("nome") or cliente).strip()
            or "Paciente / Cliente"
        )

        # Indicadores principais (escala 0 a 100, salvo idade estimada do fio em anos)
        saude_fio = _limitar_percentual(payload.get("saude_fio", payload.get("integridade_fibra")), 75.0)
        espessura_fio = _limitar_percentual(payload.get("espessura_fio", payload.get("calibre_fio")), 75.0)
        refletancia_fio = _limitar_percentual(payload.get("refletancia_fio", payload.get("brilho_fio")), 75.0)
        saude_hidrica_fio = _limitar_percentual(
            payload.get("saude_hidrica_fio", payload.get("hidratacao_fio")), 75.0
        )

        # Idade estimada da fibra (ex.: 0.5 a 6.0 anos conforme comprimento/tempo de permanencia do fio)
        idade_anos = _converter_float_positivo(payload.get("idade_fio_anos"), 1.5)
        indice_envelhecimento = _limitar_percentual(
            payload.get("indice_envelhecimento_fibra", (idade_anos / 4.0) * 100.0),
            35.0,
        )

        # Score composto da fibra (quanto menor o envelhecimento da fibra, melhor)
        vitalidade_por_idade = round(100.0 - indice_envelhecimento, 2)
        score_fibra = round(
            (saude_fio * 0.25)
            + (espessura_fio * 0.20)
            + (refletancia_fio * 0.15)
            + (saude_hidrica_fio * 0.20)
            + (vitalidade_por_idade * 0.20),
            2,
        )

        deficiencias: List[str] = []
        tratamentos: Dict[str, List[str]] = {}

        # 1. Saude do fio
        if saude_fio < 70.0:
            deficiencias.append("saude_fio")
            tratamentos["saude_fio"] = [
                "Reconstrucao estrutural com reposicao de aminoacidos, queratina/proteinas hidrolisadas e ligacoes da fibra.",
                "Pausa em processos quimicos agressivos ou fontes de calor excessivo ate estabilizar a resistencia.",
                "Tratamento quelante/desintoxicante quando houver acumulo de metais ou residuos oxidativos.",
            ]

        # 2. Espessura do fio
        if espessura_fio < 70.0:
            deficiencias.append("espessura_fio")
            tratamentos["espessura_fio"] = [
                "Protocolo de encorpamento e reposicao de massa cortical/aminoacidos para ganho de corpo e resistencia.",
                "Estimulo e cuidado do microambiente folicular para reduzir afinamento progressivo dos novos fios.",
                "Evitar excesso de tensao mecanica (penteados muito apertados) sobre fios finos/afinados.",
            ]

        # 3. Idade do fio (desgaste acumulado / envelhecimento da fibra)
        if idade_anos >= 2.5 or indice_envelhecimento >= 60.0:
            deficiencias.append("idade_fio")
            tratamentos["idade_fio"] = [
                "Protocolo anti-envelhecimento da fibra / longevidade com antioxidantes e reposicao lipidica profunda.",
                "Aparar pontas desgastadas periodicamente para remover extremidades cronicamente oxidadas.",
                "Protecao termica e UV diaria para frear degradacao cumulativa ao longo do comprimento.",
            ]

        # 4. Refletancia do fio (brilho e alinhamento cuticular)
        if refletancia_fio < 70.0:
            deficiencias.append("refletancia_fio")
            tratamentos["refletancia_fio"] = [
                "Alinhamento e selagem das cuticulas com acidificacao de pH e ativos emolientes de alto brilho.",
                "Finalizacao com oleos leves/reparadores de alta refletancia sem pesar a fibra.",
                "Enxague final em temperatura moderada/fria para favorecer compactacao cuticular.",
            ]

        # 5. Saude hidrica do fio
        if saude_hidrica_fio < 70.0:
            deficiencias.append("saude_hidrica_fio")
            tratamentos["saude_hidrica_fio"] = [
                "Reposicao hidrica intensiva com umectantes e agentes hidratantes para devolver maleabilidade e maciez.",
                "Associar nutricao lipidica logo em seguida para reter a agua dentro da fibra e evitar ressecamento rapido.",
                "Evitar lavagens com agua muito quente e shampoos excessivamente adstringentes.",
            ]

        if not deficiencias:
            tratamentos["manutencao_geral"] = [
                "Fibra com bons indices: manter cronograma equilibrado de hidratacao, nutricao e reconstrucao preventiva.",
                "Manter protecao termica e reavaliacao periodica.",
            ]

        return DiagnosticoFibraCapilar(
            cliente=nome,
            saude_fio=saude_fio,
            espessura_fio=espessura_fio,
            idade_fio_anos_estimada=idade_anos,
            indice_envelhecimento_fibra=indice_envelhecimento,
            refletancia_fio=refletancia_fio,
            saude_hidrica_fio=saude_hidrica_fio,
            score_fibra=score_fibra,
            deficiencias_detectadas=deficiencias,
            tratamentos_por_deficiencia=tratamentos,
        )
