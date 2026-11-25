# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
Modulo: memoria_tricologia_helper.py
Sistema: Thierry Technology Concept Global - Trichology & Longevity Engine
Descricao: Helper centralizado para gravar e consolidar dados de todos os
           modulos do pilar Tricologia & Saude na memoria_comum, garantindo
           que o motor de PDF (tricologia_ultra_avancada.py) puxe tudo.
===========================================================================
"""

import datetime
from typing import Any, Dict, List, Optional
from .memoria_tricologia_helper import registrar_na_memoria_comum


CHAVE_CONSOLIDADO = "tricologia_dossie_consolidado"
CHAVE_INDICE = "tricologia_indice_secoes"


def obter_memoria_comum(memoria_instancia: Optional[Any] = None) -> Any:
    """
    Retorna a instancia compartilhada de memoria_comum.
    Se nao estiver acessivel no ambiente atual, retorna um fallback local seguro
    para nao interromper a execucao dos modulos.
    """
    if memoria_instancia is not None:
        return memoria_instancia

    for caminho in ("memoria_comum", "core.memoria_comum"):
        try:
            modulo = __import__(caminho, fromlist=["instancia_memoria"])
            instancia = getattr(modulo, "instancia_memoria", None)
            if instancia is not None:
                return instancia
        except Exception:
            continue

    class _MemoriaFallbackLocal:
        modo_fallback = True
        _dados: Dict[str, Any] = {}

        def salvar_dados(self, chave: str, valor: Any) -> None:
            self._dados[chave] = valor

        def ler_dados(self, chave: str) -> Any:
            return self._dados.get(chave)

        def registrar(self, chave: str, valor: Any = None) -> None:
            self._dados[chave] = valor

    return _MemoriaFallbackLocal()


def _normalizar_payload(valor: Any) -> Dict[str, Any]:
    """Converte dicionarios ou objetos com para_dict() em um dict limpo."""
    if isinstance(valor, dict):
        return dict(valor)
    if hasattr(valor, "para_dict") and callable(getattr(valor, "para_dict")):
        resultado = valor.para_dict()
        if isinstance(resultado, dict):
            return dict(resultado)
    return {"valor": valor}


def registrar_na_memoria_comum(
    secao: str,
    payload: Any,
    cliente: str = "Paciente / Cliente",
    memoria_instancia: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Grava o resultado de um modulo de tricologia na memoria_comum:
      - Salva na chave da secao (ex.: 'tricologia_fibra')
      - Salva na chave por cliente (ex.: 'tricologia_fibra_Nome do Cliente')
      - Atualiza o dossie consolidado ('tricologia_dossie_consolidado')
      - Atualiza o indice de secoes ('tricologia_indice_secoes')
    """
    mem = obter_memoria_comum(memoria_instancia)
    secao_limpa = (secao or "modulo").strip().lower().replace(" ", "_")
    cliente_limpo = (str(cliente).strip() if cliente else "") or "Paciente / Cliente"
    dados_dict = _normalizar_payload(payload)

    timestamp_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    registro_meta = {
        "secao": secao_limpa,
        "cliente": cliente_limpo,
        "atualizado_em_utc": timestamp_utc,
        "dados": dados_dict,
    }

    chave_secao = f"tricologia_{secao_limpa}"
    chave_cliente = f"{chave_secao}_{cliente_limpo}"

    try:
        if hasattr(mem, "salvar_dados"):
            mem.salvar_dados(chave_secao, dados_dict)
            mem.salvar_dados(f"{chave_secao}_meta", registro_meta)
            mem.salvar_dados(chave_cliente, dados_dict)

        consolidado_atual = mem.ler_dados(CHAVE_CONSOLIDADO) if hasattr(mem, "ler_dados") else None
        if not isinstance(consolidado_atual, dict):
            consolidado_atual = {}

        secoes_map = consolidado_atual.get("secoes")
        if not isinstance(secoes_map, dict):
            secoes_map = {}

        secoes_map[secao_limpa] = dados_dict
        consolidado_atual["cliente"] = cliente_limpo
        consolidado_atual["atualizado_em_utc"] = timestamp_utc
        consolidado_atual["secoes"] = secoes_map
        consolidado_atual[secao_limpa] = dados_dict

        if hasattr(mem, "salvar_dados"):
            mem.salvar_dados(CHAVE_CONSOLIDADO, consolidado_atual)

        indice_atual = mem.ler_dados(CHAVE_INDICE) if hasattr(mem, "ler_dados") else None
        if not isinstance(indice_atual, list):
            indice_atual = []

        secoes_registradas: List[str] = [str(item) for item in indice_atual]
        if secao_limpa not in secoes_registradas:
            secoes_registradas.append(secao_limpa)

        if hasattr(mem, "salvar_dados"):
            mem.salvar_dados(CHAVE_INDICE, secoes_registradas)

        if hasattr(mem, "registrar"):
            try:
                mem.registrar(chave_secao, registro_meta)
            except TypeError:
                mem.registrar(chave_secao)
    except Exception:
        pass

    return dados_dict


def ler_dossie_tricologia_memoria(
    cliente: Optional[str] = None,
    memoria_instancia: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Recupera os dados consolidados de tricologia da memoria_comum,
    fazendo fallback para as chaves individuais caso necessario.
    """
    mem = obter_memoria_comum(memoria_instancia)
    consolidado = mem.ler_dados(CHAVE_CONSOLIDADO) if hasattr(mem, "ler_dados") else None
    resultado: Dict[str, Any] = dict(consolidado) if isinstance(consolidado, dict) else {}

    secoes_conhecidas = [
        "diagnostico",
        "reconstrucao",
        "plasma_fadiga",
        "cronograma",
        "queda",
        "fibra",
        "minerais_impurezas",
        "eletricidade_volume",
        "projecao_clima_rosto",
    ]

    secoes_dict = resultado.get("secoes")
    if not isinstance(secoes_dict, dict):
        secoes_dict = {}

    if hasattr(mem, "ler_dados"):
        for sec in secoes_conhecidas:
            if sec in secoes_dict and isinstance(secoes_dict[sec], dict):
                continue

            dados_sec = None
            if cliente:
                dados_sec = mem.ler_dados(f"tricologia_{sec}_{cliente}")
            if dados_sec is None:
                dados_sec = mem.ler_dados(f"tricologia_{sec}")

            if isinstance(dados_sec, dict):
                secoes_dict[sec] = dados_sec
                resultado[sec] = dados_sec

    resultado["secoes"] = secoes_dict
    if cliente and not resultado.get("cliente"):
        resultado["cliente"] = cliente
    return resultado