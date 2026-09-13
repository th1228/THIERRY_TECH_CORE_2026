# -*- coding: utf-8 -*-
import threading
import json
import os

class MemoriaComum:
    def __init__(self, arquivo_estado="estado_sistema.json"):
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
        """Salva dados no estado compartilhado com segurança."""
        with self.lock:
            self.dados[chave] = valor
            self._salvar_estado()

    def obter_dados(self, chave):
        """Busca dados salvos na memória comum."""
        with self.lock:
            return self.dados.get(chave)

    def ler_dados(self, chave=None):
        """Método de compatibilidade para atender motores que chamam ler_dados."""
        with self.lock:
            if chave:
                return self.dados.get(chave)
            return self.dados

    def _salvar_estado(self):
        with open(self.arquivo_estado, "w", encoding="utf-8") as f:
            json.dump(self.dados, f, indent=4, ensure_ascii=False)

    def _carregar_estado(self):
        if os.path.exists(self.arquivo_estado):
            try:
                with open(self.arquivo_estado, "r", encoding="utf-8") as f:
                    self.dados = json.load(f)
            except:
                self.dados = {}

# --- APELIDOS DE COMPATIBILIDADE ---
MemoriaComumEcossistema = MemoriaComum

# Instância global unificada para todo o sistema importar
instancia_memoria = MemoriaComum()
memoria_global = instancia_memoria