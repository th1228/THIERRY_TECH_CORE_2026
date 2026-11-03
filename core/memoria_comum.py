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
Versão: 1.3.0 - Thread-Safe State Manager & Shared Memory Bridge
"""

import threading
import json
import os

class MemoriaComum:
    """
    Gerenciador Central de Estado e Fila de Tarefas com Thread-Safety.
    Atua como o Hub Único de Leitura/Escrita para todos os motores do ecossistema.
    """
    def __init__(self, arquivo_estado="estado_sistema.json", lang: str = "PT"):
        self.arquivo_estado = arquivo_estado
        self.lock = threading.Lock()
        
        # Fila central de tarefas do ecossistema
        self.fila_tarefas = [] 
        
        # Estado atual compartilhado
        self.dados = {}
        self._carregar_estado()
        print("[MEMÓRIA] Gerente de Filas e Estado ativado com sucesso.")

    def adicionar_tarefa(self, tarefa):
        """Adiciona uma nova tarefa na fila central com segurança de thread."""
        with self.lock:
            self.fila_tarefas.append(tarefa)
            print(f"[MEMÓRIA] Tarefa '{tarefa}' adicionada à fila.")

    def pegar_proxima_tarefa(self):
        """Retira e retorna a próxima tarefa da fila."""
        with self.lock:
            if self.fila_tarefas:
                return self.fila_tarefas.pop(0)
            return None

    def salvar_dados(self, chave, valor):
        """Salva dados no estado compartilhado com segurança de thread."""
        with self.lock:
            self.dados[chave] = valor
            self._salvar_estado()

    def obter_dados(self, chave):
        """Busca dados salvos na memória comum pelo identificador de chave."""
        with self.lock:
            return self.dados.get(chave)

    def ler_dados(self, chave=None):
        """
        Método universal de compatibilidade para atender motores legados 
        ou chamadas diretas que passam ou não uma chave.
        """
        with self.lock:
            if chave:
                return self.dados.get(chave)
            return self.dados

    def exportar_estado_completo(self):
        """
        ✨ NOVO: Retorna uma cópia completa de todo o dicionário de estado.
        Ideal para o Orquestrador, LLM e Gerador de PDF extraírem todas as métricas de uma só vez.
        """
        with self.lock:
            return dict(self.dados)

    def _salvar_estado(self):
        """Persiste o dicionário de dados em disco como JSON (executado dentro do lock)."""
        try:
            with open(self.arquivo_estado, "w", encoding="utf-8") as f:
                json.dump(self.dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[ERRO MEMÓRIA] Falha ao persistir estado em disco: {e}")

    def _carregar_estado(self):
        """Carrega o estado existente do disco para a memória volátil."""
        if os.path.exists(self.arquivo_estado):
            try:
                with open(self.arquivo_estado, "r", encoding="utf-8") as f:
                    self.dados = json.load(f)
            except Exception as e:
                print(f"[AVISO MEMÓRIA] Não foi possível ler {self.arquivo_estado}: {e}. Inicializando estado vazio.")
                self.dados = {}

# --- APELIDOS E INSTÂNCIAS DE COMPATIBILIDADE ---
MemoriaComumEcossistema = MemoriaComum

# Instâncias globais para exportação e sincronização no ecossistema
instancia_memoria = MemoriaComum()
memoria_global = instancia_memoria