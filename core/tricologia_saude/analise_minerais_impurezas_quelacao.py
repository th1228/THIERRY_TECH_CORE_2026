# -*- coding: utf-8 -*-
"""
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
Analise de texturizacao mineralizada, minerais, cloro, metais pesados,
impurezas e radicais livres no fio, protocolo de quelacao/remocao
e acompanhamento de evolucao comparativa.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .diagnostico_capilar import AvaliacaoCapilar, _limitar_percentual, memoria
from .memoria_tricologia_helper import registrar_na_memoria_comum


@dataclass
class RelatorioMineraisImpurezasEvolucao:
    cliente: str
    # Percentuais (0.0 a 100.0)
    percentual_texturizacao_mineralizada: float
    percentual_minerais_gerais: float
    percentual_cloro: float
    percentual_metais_pesados: float
    percentual_outras_impurezas: float
    percentual_radicais_livres: float
    indice_contaminacao_total: float
    pureza_fibra_percentual: float
    nivel_carga_contaminacao: str
    # Tratamento especifico para metais pesados, cloro e impurezas
    protocolo_remocao_metais_e_impurezas: List[str] = field(default_factory=list)
    cuidados_pos_quelacao: List[str] = field(default_factory=list)
    # Evolucao em relacao a leitura anterior
    status_evolucao: str = "Primeira Leitura (Sem Base Anterior)"
    variacao_contaminacao_pct: float = 0.0
    variacao_radicais_pct: float = 0.0
    detalhes_evolucao: List[str] = field(default_factory=list)
    intervalo_reavaliacao_dias: int = 21

    def para_dict(self) -> Dict[str, Any]:
        return {
            "cliente": self.cliente,
            "percentual_texturizacao_mineralizada": self.percentual_texturizacao_mineralizada,
            "percentual_minerais_gerais": self.percentual_minerais_gerais,
            "percentual_cloro": self.percentual_cloro,
            "percentual_metais_pesados": self.percentual_metais_pesados,
            "percentual_outras_impurezas": self.percentual_outras_impurezas,
            "percentual_radicais_livres": self.percentual_radicais_livres,
            "indice_contaminacao_total": self.indice_contaminacao_total,
            "pureza_fibra_percentual": self.pureza_fibra_percentual,
            "nivel_carga_contaminacao": self.nivel_carga_contaminacao,
            "protocolo_remocao_metais_e_impurezas": list(self.protocolo_remocao_metais_e_impurezas),
            "cuidados_pos_quelacao": list(self.cuidados_pos_quelacao),
            "status_evolucao": self.status_evolucao,
            "variacao_contaminacao_pct": self.variacao_contaminacao_pct,
            "variacao_radicais_pct": self.variacao_radicais_pct,
            "detalhes_evolucao": list(self.detalhes_evolucao),
            "intervalo_reavaliacao_dias": self.intervalo_reavaliacao_dias,
        }


def _extrair_anterior(
    payload: Dict[str, Any],
    brutas: Dict[str, Any],
    chave_memoria: str,
) -> Dict[str, Any] | None:
    candidato = payload.get("leitura_anterior") or brutas.get("leitura_anterior")
    if isinstance(candidato, dict):
        try:
            _payload_mem = candidato.para_dict() if hasattr(candidato, 'para_dict') else candidato
            _cliente_mem = getattr(candidato, 'cliente', None) or getattr(candidato, 'nome_cliente', None) or 'Paciente / Cliente'
            registrar_na_memoria_comum('minerais_impurezas_quelacao', _payload_mem, cliente=_cliente_mem)
        except Exception:
            pass
        return candidato
    try:
        salvo = memoria.ler_dados(chave_memoria)
        if isinstance(salvo, dict):
            try:
                _payload_mem = salvo.para_dict() if hasattr(salvo, 'para_dict') else salvo
                _cliente_mem = getattr(salvo, 'cliente', None) or getattr(salvo, 'nome_cliente', None) or 'Paciente / Cliente'
                registrar_na_memoria_comum('minerais_impurezas_quelacao', _payload_mem, cliente=_cliente_mem)
            except Exception:
                pass
            return salvo
    except Exception:
        pass
    return None


class AnaliseMineraisImpurezasEvolucao:
    """
    Calcula percentuais de mineralizacao, cloro, metais pesados, impurezas
    e radicais livres na fibra, define tratamento de remocao/quelacao e
    compara a evolucao entre leituras.
    """

    def analisar(
        self,
        avaliacao: AvaliacaoCapilar | None = None,
        dados: Dict[str, Any] | None = None,
    ) -> RelatorioMineraisImpurezasEvolucao:
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

        # Percentuais individuais (0.0 a 100.0)
        minerais_gerais = _limitar_percentual(
            payload.get("percentual_minerais", payload.get("minerais_pct", brutas.get("percentual_minerais"))),
            25.0,
        )
        cloro = _limitar_percentual(
            payload.get("percentual_cloro", payload.get("cloro_pct", brutas.get("percentual_cloro"))),
            15.0,
        )
        metais_pesados = _limitar_percentual(
            payload.get(
                "percentual_metais_pesados",
                payload.get("metais_pesados_pct", brutas.get("percentual_metais_pesados")),
            ),
            20.0,
        )
        outras_impurezas = _limitar_percentual(
            payload.get(
                "percentual_outras_impurezas",
                payload.get("impurezas_pct", brutas.get("percentual_outras_impurezas")),
            ),
            20.0,
        )
        radicais_livres = _limitar_percentual(
            payload.get(
                "percentual_radicais_livres",
                payload.get("radicais_pct", brutas.get("percentual_radicais_livres")),
            ),
            25.0,
        )

        # Texturizacao mineralizada: mede o quanto os minerais/residuos alteram textura, rigidez e toque do fio
        texturizacao_padrao = round(
            (minerais_gerais * 0.45) + (metais_pesados * 0.35) + (cloro * 0.20),
            2,
        )
        texturizacao_mineralizada = _limitar_percentual(
            payload.get(
                "percentual_texturizacao_mineralizada",
                payload.get("texturizacao_mineralizada_pct", brutas.get("percentual_texturizacao_mineralizada")),
            ),
            texturizacao_padrao,
        )

        # Contaminacao total e pureza da fibra
        contaminacao_total = round(
            (minerais_gerais * 0.22)
            + (cloro * 0.18)
            + (metais_pesados * 0.28)
            + (outras_impurezas * 0.14)
            + (radicais_livres * 0.18),
            2,
        )
        pureza_fibra = round(max(0.0, 100.0 - contaminacao_total), 2)

        if contaminacao_total >= 65.0 or metais_pesados >= 55.0:
            nivel_carga = "Critica / Alta Deposicao e Oxidacao"
            intervalo = 14
        elif contaminacao_total >= 40.0 or cloro >= 40.0 or radicais_livres >= 50.0:
            nivel_carga = "Moderada a Alta"
            intervalo = 21
        elif contaminacao_total >= 20.0:
            nivel_carga = "Leve a Moderada"
            intervalo = 30
        else:
            nivel_carga = "Baixa / Fibra Limpa"
            intervalo = 45

        # Protocolo especifico para remover metais pesados, cloro, impurezas e radicais
        protocolo: List[str] = [
            "1. Quelacao e Remocao de Metais Pesados: aplicar protocolo quelante direcionado para complexar e remover "
            "ions metalicos depositados na cuticula e no cortex.",
            "2. Neutralizacao de Cloro e Residuos: realizar lavagem purificante/neutralizante para retirar cloro residual, "
            "sais minerais e impurezas ambientais/cosmeticas.",
            "3. Combate a Radicais Livres / Estresse Oxidativo: associar ativos antioxidantes e quelantes de radicais "
            "para conter degradacao oxidativa da queratina e dos pigmentos.",
        ]
        if texturizacao_mineralizada >= 45.0:
            protocolo.append(
                "4. Desmineralizacao e Reequilibrio de Textura: quebrar o enrijecimento/aspereza da texturizacao "
                "mineralizada antes de aplicar mascaras de tratamento."
            )

        cuidados_pos: List[str] = [
            "Logo apos a quelacao/limpeza profunda, repor agua (hidratacao), lipidios (nutricao) e/ou massa "
            "(reconstrucao) para evitar rigidez ou ressecamento pos-remocao.",
            "Evitar agua muito quente e banhos prolongados em agua clorada ou de alto teor mineral sem protecao previa.",
            "Proteger o fio contra exposicao solar/UV e calor excessivo para reduzir nova formacao de radicais livres.",
        ]

        # Evolucao comparativa com leitura anterior (se existir)
        chave_memoria = f"tricologia_minerais_impurezas_{cliente}"
        anterior = _extrair_anterior(payload, brutas, chave_memoria)

        detalhes_evolucao: List[str] = []
        status_evolucao = "Primeira Leitura (Sem Base Anterior)"
        var_cont = 0.0
        var_rad = 0.0

        if isinstance(anterior, dict) and "indice_contaminacao_total" in anterior:
            cont_ant = _limitar_percentual(anterior.get("indice_contaminacao_total"), contaminacao_total)
            rad_ant = _limitar_percentual(anterior.get("percentual_radicais_livres"), radicais_livres)
            met_ant = _limitar_percentual(anterior.get("percentual_metais_pesados"), metais_pesados)
            clo_ant = _limitar_percentual(anterior.get("percentual_cloro"), cloro)

            var_cont = round(contaminacao_total - cont_ant, 2)
            var_rad = round(radicais_livres - rad_ant, 2)
            var_met = round(metais_pesados - met_ant, 2)
            var_clo = round(cloro - clo_ant, 2)

            detalhes_evolucao.append(
                f"Contaminacao total: {cont_ant}% -> {contaminacao_total}% ({var_cont:+.2f} p.p.)."
            )
            detalhes_evolucao.append(
                f"Metais pesados: {met_ant}% -> {metais_pesados}% ({var_met:+.2f} p.p.) | Cloro: {clo_ant}% -> {cloro}% ({var_clo:+.2f} p.p.)."
            )
            detalhes_evolucao.append(
                f"Radicais livres: {rad_ant}% -> {radicais_livres}% ({var_rad:+.2f} p.p.)."
            )

            if var_cont <= -10.0:
                status_evolucao = "Evolucao Positiva (Reducao Relevante de Impurezas)"
            elif var_cont < 0.0:
                status_evolucao = "Melhora Progressiva (Leve Reducao de Carga)"
            elif var_cont == 0.0 and var_rad == 0.0:
                status_evolucao = "Estavel (Sem Alteracao em Relacao a Leitura Anterior)"
            else:
                status_evolucao = "Alerta de Acumulo / Piora (Aumento de Carga ou Radicais)"
        else:
            detalhes_evolucao.append(
                "Leitura inicial registrada; nas proximas avaliacoes o sistema calculara a evolucao percentual automaticamente."
            )

        relatorio = RelatorioMineraisImpurezasEvolucao(
            cliente=cliente,
            percentual_texturizacao_mineralizada=texturizacao_mineralizada,
            percentual_minerais_gerais=minerais_gerais,
            percentual_cloro=cloro,
            percentual_metais_pesados=metais_pesados,
            percentual_outras_impurezas=outras_impurezas,
            percentual_radicais_livres=radicais_livres,
            indice_contaminacao_total=contaminacao_total,
            pureza_fibra_percentual=pureza_fibra,
            nivel_carga_contaminacao=nivel_carga,
            protocolo_remocao_metais_e_impurezas=protocolo,
            cuidados_pos_quelacao=cuidados_pos,
            status_evolucao=status_evolucao,
            variacao_contaminacao_pct=var_cont,
            variacao_radicais_pct=var_rad,
            detalhes_evolucao=detalhes_evolucao,
            intervalo_reavaliacao_dias=intervalo,
        )

        try:
            memoria.salvar_dados(chave_memoria, relatorio.para_dict())
        except Exception:
            pass

        try:
            _payload_mem = relatorio.para_dict() if hasattr(relatorio, 'para_dict') else relatorio
            _cliente_mem = getattr(relatorio, 'cliente', None) or getattr(relatorio, 'nome_cliente', None) or 'Paciente / Cliente'
            registrar_na_memoria_comum('minerais_impurezas_quelacao', _payload_mem, cliente=_cliente_mem)
        except Exception:
            pass
        return relatorio
