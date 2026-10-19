# -*- coding: utf-8 -*-
"""
=============================================================================
MÓDULO: Auditoria de Integridade Global (TTC - Sovereign Master)
Finalidade: Varredura profunda do ecossistema, identificando exato arquivo, 
linha e anomalia em dados biométricos, métricas ou relatórios UHNW.
=============================================================================
"""

import os
import hashlib
import datetime
from typing import Dict, Any, List, Optional

class AuditorIntegridadeGlobal:
    def __init__(self, limiar_confianca_minimo: float = 100.0):
        self.limiar_confianca_minimo = limiar_confianca_minimo
        
        # Termos estritamente proibidos que indicam falha ou dados genéricos
        self.termos_proibidos = [
            "placeholder", 
            "n/a", 
            "vazio", 
            "null", 
            "undefined", 
            "generico", 
            "teste", 
            "nao informado",
            "sem dados"
        ]

    def inspecionar_dicionario_metricas(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Inspeciona exaustivamente o dicionário de métricas em busca de anomalias."""
        anomalias: List[str] = []
        total_campos = len(dados) if len(dados) > 0 else 1
        campos_validos = 0

        for chave, valor in dados.items():
            valor_str = str(valor).strip().lower()
            contem_termo_proibido = any(termo in valor_str for termo in self.termos_proibidos)
            
            if contem_termo_proibido:
                anomalias.append(f"Campo '{chave}' possui valor inválido ou genérico: '{valor}'")
            elif not valor_str or valor_str == "":
                anomalias.append(f"Campo '{chave}' está vazio ou não preenchido.")
            else:
                campos_validos += 1

        indice_integridade = (campos_validos / total_campos) * 100.0
        status_aprovacao = (indice_integridade >= self.limiar_confianca_minimo) and (len(anomalias) == 0)

        return {
            "status_aprovacao": status_aprovacao,
            "indice_integridade_percentual": round(indice_integridade, 2),
            "anomalias_encontradas": anomalias,
            "timestamp_auditoria": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def varrer_projeto_por_anomalias(self, diretorio_raiz: str = ".") -> None:
        """
        Varre recursivamente todos os arquivos .py do diretório do projeto 
        procurando por termos proibidos (como 'N/A' ou 'placeholder') escritos no código 
        e imprime no terminal exatamente o arquivo e a linha da irregularidade.
        """
        print(f"\n[TTC AUDITOR] Iniciando varredura profunda no diretório: {os.path.abspath(diretorio_raiz)}")
        print("-" * 70)
        
        erros_encontrados = 0
        
        for root, _, files in os.walk(diretorio_raiz):
            # Ignora pastas virtuais ou de ambiente
            if any(p in root for p in ['.git', '__pycache__', 'venv', 'env', '.vscode']):
                continue
                
            for file in files:
                if file.endswith(".py") and file != "auditor_integridade_global.py":
                    caminho_arquivo = os.path.join(root, file)
                    try:
                        with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as f:
                            linhas = f.readlines()
                            for num_linha, linha in enumerate(linhas, 1):
                                linha_lower = linha.lower()
                                for termo in self.termos_proibidos:
                                    if f"'{termo}'" in linha_lower or f'"{termo}"' in linha_lower or f": {termo}" in linha_lower:
                                        erros_encontrados += 1
                                        print(f"[ALERTA DE ANOMALIA]")
                                        print(f"  -> Arquivo : {caminho_arquivo}")
                                        print(f"  -> Linha   : {num_linha}")
                                        print(f"  -> Termo   : '{termo}' detectado.")
                                        print(f"  -> Conteúdo: {linha.strip()}")
                                        print("-" * 50)
                    except Exception as e:
                        print(f"[ERRO] Não foi possível ler o arquivo {caminho_arquivo}: {e}")

        if erros_encontrados == 0:
            print("[SUCESSO] Nenhuma anomalia estática de código encontrada. O projeto está limpo.")
        else:
            print(f"[ATENÇÃO] Total de {erros_encontrados} ocorrências suspeitas encontradas nos arquivos acima.")
        print("-" * 70)

    def gerar_selo_criptografico_soberano(self, dados: Dict[str, Any], identificador_transacao: str) -> str:
        conteudo_serializado = str(sorted(dados.items())) + identificador_transacao + str(datetime.datetime.now().date())
        selo_hash = hashlib.sha256(conteudo_serializado.encode('utf-8')).hexdigest().upper()
        return f"TTC-SECURE-SHA256-{selo_hash[:32]}"

# Bloco de Execução Direta via Terminal (Ex: python auditor_integridade_global.py)
if __name__ == "__main__":
    auditor = AuditorIntegridadeGlobal(limiar_confianca_minimo=100.0)
    auditor.varrer_projeto_por_anomalias(".")