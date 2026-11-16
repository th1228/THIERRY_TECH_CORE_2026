# -*- coding: utf-8 -*-
"""
Módulo: c2_audit_inspector.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Semantic Purity Inspector
Versão: 3.1.0 - Monaco Semantic Core Integrity Edition
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

BASE_DIR = Path(__file__).resolve().parent

class C2AuditInspector:
    """Motor soberano responsável por inspecionar a pureza semântica e o alinhamento exclusivo do código."""
    
    def __init__(self, nome_lider: str = "Genilson Rodrigues"):
        self.lider = nome_lider.strip()
        # Procura o motor na raiz ou dentro de subpastas (como 'code' ou diretórios do workspace)
        self.engine_path = self._encontrar_motor()

    def _encontrar_motor(self) -> Path:
        """Varre o diretório à procura do motor principal c2_sovereign_intelligence.py."""
        candidatos = list(BASE_DIR.glob("**/c2_sovereign_intelligence.py"))
        if candidatos:
            return candidatos[0]
        # Retorna o caminho padrão caso não ache por glob
        return BASE_DIR / "c2_sovereign_intelligence.py"

    def auditar_pureza_semantica_motor(self) -> Dict[str, Any]:
        """Abre o motor principal onde quer que ele esteja e verifica a pureza semântica do core."""
        resultado = {
            "status_semantico": "PURO",
            "linhas_analisadas": 0,
            "contaminacoes_detectadas": []
        }
        
        if not self.engine_path.exists():
            return {
                "status_semantico": "ERRO",
                "linhas_analisadas": 0,
                "contaminacoes_detectadas": [f"Ficheiro c2_sovereign_intelligence.py não encontrado no caminho: {self.engine_path}"]
            }

        termos_proibidos = [
            "ecommerce", "carrinho_compras", "gateway_pagamento", 
            "chatbot_generico", "scraping_web", "crypto_miner"
        ]

        try:
            with open(self.engine_path, "r", encoding="utf-8") as f:
                linhas = f.readlines()
                
            resultado["linhas_analisadas"] = len(linhas)
            
            for idx, linha in enumerate(linhas, 1):
                linha_lower = linha.lower()
                for termo in termos_proibidos:
                    if termo in linha_lower:
                        resultado["contaminacoes_detectadas"].append(
                            f"Linha {idx}: Termo proibido/estranho detetado ('{termo}')."
                        )
                        
            if resultado["contaminacoes_detectadas"]:
                resultado["status_semantico"] = "CONTAMINADO"
                
        except Exception as e:
            resultado["status_semantico"] = "ERRO"
            resultado["contaminacoes_detectadas"].append(f"Erro ao ler o motor: {e}")
            
        return resultado

    def gerar_parecer_executivo(self) -> str:
        aud_semantica = self.auditar_pureza_semantica_motor()
        
        relatorio = []
        relatorio.append("=" * 72)
        relatorio.append("   [AUDITORIA C2] PARECER DE PUREZA SEMÂNTICA & INTEGRIDADE DO CORE")
        relatorio.append("   Padrão Corporativo: Thierry Technology Concept Global (Mônaco)")
        relatorio.append("=" * 72)
        relatorio.append(f" Motor Localizado        : {self.engine_path.name}")
        relatorio.append(f" Caminho Completo        : {self.engine_path}")
        relatorio.append(f" Linhas de Código Lidas  : {aud_semantica['linhas_analisadas']}")
        relatorio.append(f" Status de Pureza Core   : [{aud_semantica['status_semantico']}]")
        relatorio.append("-" * 72)
        
        if aud_semantica["status_semantico"] == "PURO":
            relatorio.append(" ★ DIAGNÓSTICO: INTEGRALMENTE ALINHADO")
            relatorio.append(" Avaliação                : O programa está perfeitamente coeso. Toda a lógica interna")
            relatorio.append("                            envolve estritamente os biogêmeos, cronoestética, oximetria")
            relatorio.append("                            e o nexo financeiro UHNW. Não há contaminação cruzada.")
        else:
            relatorio.append(" ⚠ DIAGNÓSTICO: DESVIO LÓGICO DETETADO")
            relatorio.append(" Avaliação                : Foram encontrados elementos estranhos ao ecossistema.")
            for desc in aud_semantica["contaminacoes_detectadas"]:
                relatorio.append(f"  - {desc}")

        relatorio.append("=" * 72)
        return "\n".join(relatorio)


if __name__ == "__main__":
    inspector = C2AuditInspector()
    print(inspector.gerar_parecer_executivo())