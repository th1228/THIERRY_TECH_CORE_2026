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

# -*- coding: utf-8 -*-
"""
Módulo: memoria_comum.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Versão: 1.4.1 - Thread-Safe State Manager & Shared Memory Bridge
"""

import copy
import json
import os
import threading
from typing import Any, Dict, Optional

_BLOQUEIO_CARTA_CONTRATO = {
    "analise_gemini",
    "analise_gemini_recente",
    "analise_gemini_carta",
    "parecer_carta",
    "secoes_dossie_json",
    "secoes_json",
    "diagnostico_estrutural",
    "analise_dermica_hsv",
    "projecao_temporal",
    "recomendacao_tecnica",
    "secao_tricologia",
    "dados_tricologia_isolados",
    "secao_financeiro",
    "contexto_biometrico_parametrico",
    "evolucao_longitudinal",
    "projecao_ciclos",
}

_CHAVES_TRICOLOGIA = {
    "dados_tricologia",
    "tricologia",
    "secao_tricologia",
    "analise_capilar",
    "dados_tricologia_isolados",
    "diagnostico_estrutural",
    "projecao_temporal",
    "recomendacao_tecnica",
    "secoes_dossie_json",
    "secoes_json",
    "analise_gemini",
    "analise_gemini_recente",
}


class MemoriaComum:
    """
    Gerenciador Central de Estado e Fila de Tarefas com Thread-Safety.
    Atua como o Hub Único de Leitura/Escrita para todos os motores do ecossistema.
    """

    def __init__(self, arquivo_estado: str = "estado_sistema.json", lang: str = "PT") -> None:
        self.arquivo_estado = arquivo_estado
        self.lang = lang
        self.lock = threading.Lock()
        self.fila_tarefas = []
        self.dados: Dict[str, Any] = {}
        self._carregar_estado()
        print("[MEMÓRIA] Gerente de Filas e Estado ativado com sucesso.")

    def adicionar_tarefa(self, tarefa: Any) -> None:
        """Adiciona uma nova tarefa na fila central com segurança de thread."""
        with self.lock:
            self.fila_tarefas.append(tarefa)
            print(f"[MEMÓRIA] Tarefa '{tarefa}' adicionada à fila.")

    def pegar_proxima_tarefa(self) -> Any:
        """Retira e retorna a próxima tarefa da fila."""
        with self.lock:
            if self.fila_tarefas:
                return self.fila_tarefas.pop(0)
            return None

    def salvar_dados(self, chave: str, valor: Any) -> bool:
        """Salva dados no estado compartilhado com segurança de thread."""
        with self.lock:
            self.dados[chave] = valor
            self._salvar_estado()
            return True

    def registrar(self, chave: str, valor: Any) -> bool:
        """Alias de compatibilidade para registro de dados na memória comum."""
        return self.salvar_dados(chave, valor)

    def obter_dados(self, chave: str) -> Any:
        """Busca dados salvos na memória comum pelo identificador de chave."""
        with self.lock:
            return copy.deepcopy(self.dados.get(chave))

    def ler_dados(self, chave: Optional[str] = None) -> Any:
        """
        Método universal de compatibilidade para atender motores legados
        ou chamadas diretas que passam ou não uma chave.
        """
        with self.lock:
            if chave:
                return copy.deepcopy(self.dados.get(chave))
            return copy.deepcopy(self.dados)

    def exportar_estado_completo(self) -> Dict[str, Any]:
        """
        Retorna uma cópia completa de todo o dicionário de estado.
        Ideal para o Orquestrador, LLM e Gerador de PDF extraírem todas as métricas de uma só vez.
        """
        with self.lock:
            return copy.deepcopy(self.dados)

    def obter_para_destino(self, destino: str, chave: Optional[str] = None) -> Any:
        """Entrega dados filtrados por destino ('motor_1'..'motor_6', 'carta', 'contrato', 'tricologia')."""
        with self.lock:
            base = copy.deepcopy(self.dados)

        dest = (destino or "").strip().lower()
        if dest in ("motor_4", "carta", "motor_6", "contrato"):
            filtrado = {k: v for k, v in base.items() if k not in _BLOQUEIO_CARTA_CONTRATO}
        elif dest in ("motor_3", "tricologia"):
            filtrado = {k: v for k, v in base.items() if k in _CHAVES_TRICOLOGIA or k not in _BLOQUEIO_CARTA_CONTRATO}
        else:
            filtrado = base

        return filtrado.get(chave) if chave else filtrado

    def _salvar_estado(self) -> None:
        """Persiste o dicionário de dados em disco como JSON (executado dentro do lock)."""
        try:
            with open(self.arquivo_estado, "w", encoding="utf-8") as f:
                json.dump(self.dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[ERRO MEMÓRIA] Falha ao persistir estado em disco: {e}")

    def _carregar_estado(self) -> None:
        """Carrega o estado existente do disco para a memória volátil."""
        if os.path.exists(self.arquivo_estado):
            try:
                with open(self.arquivo_estado, "r", encoding="utf-8") as f:
                    carregado = json.load(f)
                    self.dados = carregado if isinstance(carregado, dict) else {}
            except Exception as e:
                print(f"[AVISO MEMÓRIA] Não foi possível ler {self.arquivo_estado}: {e}. Inicializando estado vazio.")
                self.dados = {}


# --- APELIDOS E INSTÂNCIAS DE COMPATIBILIDADE ---
MemoriaComumEcossistema = MemoriaComum

# Instâncias globais para exportação e sincronização no ecossistema
instancia_memoria = MemoriaComum()
memoria_global = instancia_memoria