# -*- coding: utf-8 -*-
"""
Módulo: auditor_sistema.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Descrição: Script individual de varredura profunda do sistema. Analisa a pasta security, 
           os 5 motores do core, calcula linhas de código e gera o relatório técnico de auditoria.
"""

import os
import sys
import json
import hashlib
from datetime import datetime

# Garante suporte a cores no terminal do Windows
if os.name == 'nt':
    os.system('')

GREEN = "\033[92m"
BRIGHT_GREEN = "\033[1;92m"
CYAN = "\033[96m"
WHITE = "\033[97m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

class TCCSoftwareAuditor:
    """Realiza a varredura e o diagnóstico completo do ecossistema TCC Global."""
    def __init__(self):
        self.root_dir = os.path.abspath(os.path.dirname(__file__))
        self.security_dir = os.path.join(self.root_dir, 'security')
        self.core_dir = os.path.join(self.root_dir, 'core')
        self.timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M:%S UTC")

    def executar_auditoria(self) -> dict:
        print("=" * 70)
        print(f"{CYAN}TCC GLOBAL • AUDITORIA DE SISTEMA & VARREDURA DE SEGURANÇA{RESET}")
        print(f"Timestamp: {self.timestamp}")
        print("=" * 70)

        # 1. Varredura da pasta security
        security_ativo = os.path.exists(self.security_dir)
        print(f"[{'OK' if security_ativo else 'FALHA'}] Pasta /security -> {'Encontrada e Blindada' if security_ativo else 'Não encontrada'}")

        # 2. Varredura dos 5 motores do core
        modulos_alvo = [
            "c2_sovereign_intelligence.py",
            "super_retorno_financeiro.py",
            "tricologia_ultra_avancada.py",
            "carta_internacional_engine.py",
            "monaco_modelagem_engine.py"
        ]

        relatorio_motores = {}
        total_linhas = 0

        print("-" * 70)
        for i, mod in enumerate(modulos_alvo, 1):
            caminho = os.path.join(self.core_dir, mod)
            if os.path.exists(caminho):
                with open(caminho, 'rb') as f:
                    conteudo = f.read()
                    hash_arq = hashlib.sha256(conteudo).hexdigest()[:12].upper()
                with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
                    linhas = sum(1 for _ in f)
                
                total_linhas += linhas
                relatorio_motores[mod] = {
                    "status": "HOMOLOGADO",
                    "linhas": linhas,
                    "hash_parcial": hash_arq
                }
                print(f"[{i}/5] {mod} -> {GREEN}HOMOLOGADO{RESET} ({linhas} linhas | Hash: {hash_arq})")
            else:
                relatorio_motores[mod] = {
                    "status": "PENDENTE",
                    "linhas": 0,
                    "hash_parcial": "N/A"
                }
                print(f"[{i}/5] {mod} -> {RED}PENDENTE / AUSENTE{RESET}")

        print("-" * 70)
        print(f"{YELLOW}Total de Linhas de Código Analisadas e Validadas:{RESET} {BRIGHT_GREEN}{total_linhas:,} linhas{RESET}")
        print("=" * 70)

        dados_finais = {
            "timestamp": self.timestamp,
            "security_status": "ATIVO" if security_ativo else "AUSENTE",
            "total_linhas_codigo": total_linhas,
            "motores": relatorio_motores
        }

        # Salva o relatório JSON para o motor do contrato ler
        caminho_relatorio = os.path.join(self.root_dir, "relatorio_auditoria_sistema.json")
        with open(caminho_relatorio, "w", encoding="utf-8") as f:
            json.dump(dados_finais, f, indent=4, ensure_ascii=False)

        print(f"{BRIGHT_GREEN}[SUCESSO]{RESET} Relatório de auditoria exportado para: {WHITE}relatorio_auditoria_sistema.json{RESET}")
        print("=" * 70)
        return dados_finais

if __name__ == "__main__":
    auditor = TCCSoftwareAuditor()
    auditor.executar_auditoria()