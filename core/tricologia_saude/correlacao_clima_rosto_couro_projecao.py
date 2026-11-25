# -*- coding: utf-8 -*-
"""
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
Correlacao ambiental (clima), visagismo/imagem do rosto, proposta visual,
projecao de resultado e tratamento terapeutico especifico do couro cabeludo.
Sequencia: Couro (base) -> Cabelo (fibra) -> Couro (terapia) -> Projecao.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .diagnostico_capilar import AvaliacaoCapilar, _limitar_percentual
from .memoria_tricologia_helper import registrar_na_memoria_comum


@dataclass
class RelatorioClimaRostoCouroProjecao:
    cliente: str
    sequencia_analise: str
    # 1. Couro (base)
    leitura_base_couro: str
    # 2. Cabelo (fibra e queda)
    leitura_base_cabelo: str
    # 3. Couro (tratamento especifico terapeutico)
    tratamento_terapeutico_couro_cabeludo: List[str] = field(default_factory=list)
    # 4. Projecao (clima + imagem do rosto + resultado)
    clima_resumo: str = ""
    impacto_climatico_fio_e_couro: List[str] = field(default_factory=list)
    formato_rosto_avaliado: str = ""
    o_que_o_protocolo_propoe_fazer: List[str] = field(default_factory=list)
    como_a_imagem_sera_vista_melhor: str = ""
    como_vai_deixar_a_pessoa: str = ""
    frequencia_cuidado_dias: int = 21

    def para_dict(self) -> Dict[str, Any]:
        return {
            "cliente": self.cliente,
            "sequencia_analise": self.sequencia_analise,
            "leitura_base_couro": self.leitura_base_couro,
            "leitura_base_cabelo": self.leitura_base_cabelo,
            "tratamento_terapeutico_couro_cabeludo": list(self.tratamento_terapeutico_couro_cabeludo),
            "clima_resumo": self.clima_resumo,
            "impacto_climatico_fio_e_couro": list(self.impacto_climatico_fio_e_couro),
            "formato_rosto_avaliado": self.formato_rosto_avaliado,
            "o_que_o_protocolo_propoe_fazer": list(self.o_que_o_protocolo_propoe_fazer),
            "como_a_imagem_sera_vista_melhor": self.como_a_imagem_sera_vista_melhor,
            "como_vai_deixar_a_pessoa": self.como_vai_deixar_a_pessoa,
            "frequencia_cuidado_dias": self.frequencia_cuidado_dias,
        }


def _converter_float(valor: Any, padrao: float) -> float:
    try:
        return round(float(valor), 2)
    except (TypeError, ValueError):
        try:
            _payload_mem = padrao.para_dict() if hasattr(padrao, 'para_dict') else padrao
            _cliente_mem = getattr(padrao, 'cliente', None) or getattr(padrao, 'nome_cliente', None) or 'Paciente / Cliente'
            registrar_na_memoria_comum('clima_rosto_couro_projecao', _payload_mem, cliente=_cliente_mem)
        except Exception:
            pass
        return padrao


class CorrelacaoClimaRostoCouroProjecao:
    """
    Executa a correlacao seguindo a ordem:
    Couro -> Cabelo -> Couro -> Projecao (clima, imagem do rosto e resultado).
    """

    def gerar_correlacao(
        self,
        avaliacao: AvaliacaoCapilar,
        dados: Dict[str, Any] | None = None,
    ) -> RelatorioClimaRostoCouroProjecao:
        payload: Dict[str, Any] = dados if isinstance(dados, dict) else {}
        brutas: Dict[str, Any] = (
            avaliacao.metricas_brutas
            if isinstance(avaliacao.metricas_brutas, dict)
            else {}
        )

        cliente = (
            str(payload.get("cliente") or brutas.get("cliente") or avaliacao.cliente).strip()
            or "Paciente / Cliente"
        )

        # 1. COURO (base)
        couro = avaliacao.saude_couro_cabeludo
        densidade = avaliacao.indice_densidade_folicular
        integridade = avaliacao.indice_integridade_fibra

        leitura_couro = (
            f"Saude do couro cabeludo em {couro}% e densidade folicular em {densidade}%."
        )

        # 2. CABELO (fibra)
        leitura_cabelo = (
            f"Integridade da fibra em {integridade}% (score geral tricológico {avaliacao.score_geral_tricologia}%)."
        )

        # 4A. CLIMA
        umidade = _limitar_percentual(
            payload.get("umidade_relativa", brutas.get("umidade_relativa")), 65.0
        )
        temperatura = _converter_float(
            payload.get("temperatura_c", brutas.get("temperatura_c")), 29.0
        )
        uv = _converter_float(
            payload.get("indice_uv", brutas.get("indice_uv")), 7.0
        )
        clima_resumo = f"Temperatura {temperatura}°C | Umidade relativa {umidade}% | UV {uv}"

        impactos_clima: List[str] = []
        if umidade >= 75.0 and temperatura >= 27.0:
            impactos_clima.append(
                "Calor e umidade elevados: aumentam transpiracao, oleosidade no couro cabeludo e tendencia a frizz/expansao cuticular."
            )
        elif umidade < 45.0:
            impactos_clima.append(
                "Umidade baixa / ar seco: favorece perda hidrica da fibra, ressecamento, rigidez e eletricidade estatica."
            )
        else:
            impactos_clima.append(
                "Condicao climatica moderada: manter equilibrio hidrico-lipidico e controle de oleosidade sem excessos."
            )

        if uv >= 7.0:
            impactos_clima.append(
                "Indice UV elevado: acelera foto-oxidacao de pigmentos, lipidios e queratina no couro cabeludo e comprimentos."
            )

        # 3. COURO (tratamento especifico terapeutico)
        tratamento_couro: List[str] = [
            "Limpeza terapeutica equilibrada (pH compativel e tensoativos suaves) para remover oleosidade oxidada, sujidade e residuos sem agredir a barreira.",
        ]
        if couro < 70.0 or umidade >= 75.0:
            tratamento_couro.append(
                "Controle de microambiente e oleosidade/desequilibrio: aplicar ativos calmantes, purificantes e reguladores "
                "do couro cabeludo, evitando agua quente e excesso de oclusao na raiz."
            )
        else:
            tratamento_couro.append(
                "Manutencao da barreira cutanea do couro cabeludo: hidratacao leve e protecao antioxidante contra radicais livres e UV."
            )
        if densidade < 70.0:
            tratamento_couro.append(
                "Suporte folicular direcionado: massagem estimulante suave para microcirculacao e acompanhamento da densidade/queda."
            )

        # 4B. PROJECAO (imagem do rosto, proposta, como sera vista melhor e como vai deixar a pessoa)
        formato_raw = str(
            payload.get("formato_rosto")
            or payload.get("proporcao_rosto")
            or brutas.get("formato_rosto")
            or "equilibrado / oval"
        ).strip().lower()

        if "redond" in formato_raw:
            formato_exibicao = "Redondo"
            o_que_propoe = [
                "Criar leve altura/alongamento no topo sem exagerar e controlar volume excessivo nas laterais.",
                "Promover selagem cuticular e brilho direcionado para manter linhas limpas junto ao rosto.",
            ]
            como_sera_vista_melhor = (
                "O rosto sera visto com maior alongamento vertical e contornos laterais mais limpos, "
                "valorizando o centro da face e o olhar sem alargar as bochechas."
            )
            como_vai_deixar = (
                "Deixa a pessoa com visual mais harmonioso, leve e definido, realcando a expressao com "
                "caimento equilibrado e aspecto saudavel."
            )
        elif "quadrad" in formato_raw or "angulos" in formato_raw:
            formato_exibicao = "Quadrado / Anguloso"
            o_que_propoe = [
                "Suavizar arestas e angulos marcados com movimento fluido e acabamento polido.",
                "Equilibrar textura e brilho para reduzir rigidez visual no contorno da mandibula e testa.",
            ]
            como_sera_vista_melhor = (
                "O rosto sera visto com suavizacao dos angulos mais marcados, ganhando fluidez visual "
                "e foco equilibrado nos olhos e na expressao facial."
            )
            como_vai_deixar = (
                "Deixa a pessoa com presenca mais fluida, refinada e equilibrada, preservando a forca dos tracos "
                "com um acabamento mais suave."
            )
        elif "oblong" in formato_raw or "alongad" in formato_raw:
            formato_exibicao = "Oblongo / Alongado"
            o_que_propoe = [
                "Distribuir volume lateral controlado e acabamento na altura das macas/maxilar.",
                "Evitar excesso de altura vertical no topo para nao acentuar o alongamento da face.",
            ]
            como_sera_vista_melhor = (
                "O rosto sera visto com maior equilibrio horizontal e proporcao central, "
                "encurtando visualmente o excesso de alongamento e destacando o terco medio."
            )
            como_vai_deixar = (
                "Deixa a pessoa com aspecto mais proporcional, acolhedor e harmonioso, "
                "com moldura capilar mais equilibrada ao redor do rosto."
            )
        else:
            formato_exibicao = "Oval / Proporcional"
            o_que_propoe = [
                "Preservar o equilibrio proporcional com tratamento de integridade, brilho e controle de frizz.",
                "Ajustar acabamento e luminosidade conforme a luz e o clima do dia a dia.",
            ]
            como_sera_vista_melhor = (
                "O rosto sera visto com ainda mais nitidez, simetria percebida e destaque natural "
                "para o olhar e o sorriso."
            )
            como_vai_deixar = (
                "Deixa a pessoa com imagem limpa, sofisticada e saudavel, valorizando a moldura natural "
                "sem sobrecarregar os tracos."
            )

        frequencia = (
            15
            if (couro < 60.0 or densidade < 60.0)
            else (21 if umidade >= 75.0 or umidade < 45.0 else 30)
        )

        return RelatorioClimaRostoCouroProjecao(
            cliente=cliente,
            sequencia_analise="Couro -> Cabelo -> Couro -> Projecao",
            leitura_base_couro=leitura_couro,
            leitura_base_cabelo=leitura_cabelo,
            tratamento_terapeutico_couro_cabeludo=tratamento_couro,
            clima_resumo=clima_resumo,
            impacto_climatico_fio_e_couro=impactos_clima,
            formato_rosto_avaliado=formato_exibicao,
            o_que_o_protocolo_propoe_fazer=o_que_propoe,
            como_a_imagem_sera_vista_melhor=como_sera_vista_melhor,
            como_vai_deixar_a_pessoa=como_vai_deixar,
            frequencia_cuidado_dias=frequencia,
        )
