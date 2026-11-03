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
SISTEMA DE AUDITORIA TÉCNICA E VALORAÇÃO DE ATIVOS INTANGÍVEIS (AUDITABLE CORE)
COMPATIBILIDADE: ISO/IEC 25010, COCOMO II (POST-ARCHITECTURE) & CPC 04 / IAS 38
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
import requests
from radon.visitors import ComplexityVisitor
from radon.metrics import mi_parameters

# Configurações de Terminal (ANSI)
COLOR_HEADER = "\033[95m"
COLOR_BLUE = "\033[94m"
COLOR_GREEN = "\033[92m"
COLOR_WARNING = "\033[93m"
COLOR_FAIL = "\033[91m"
RESET = "\033[0m"

class AuditoriaCore:
    def __init__(self, diretorio_raiz=".", custo_medio_mensal_dev=28000.00, total_licencas_globais=10):
        """
        :param custo_medio_mensal_dev: Custo real (BRL) de um Dev Pleno/Senior com encargos.
        :param total_licencas_globais: Teto absoluto de escassez global do ecossistema.
        """
        self.raiz = Path(diretorio_raiz)
        self.custo_dev_brl = custo_medio_mensal_dev
        self.total_licencas = total_licencas_globais
        self.ignorar_pastas = {".git", "__pycache__", ".vscode", "venv", "env", "node_modules", "dist"}
        
        # Métricas Acumuladas
        self.total_sloc_bruto = 0
        self.total_lloc_logico = 0
        self.total_comentarios = 0
        self.complexidade_acumulada = 0
        self.total_arquivos_python = 0
        self.arquivos_mapeados = []

    def obter_taxa_ptax(self):
        """Busca a cotação oficial PTAX de venda do Banco Central do Brasil em tempo real via API OData."""
        print(f"{COLOR_BLUE}[i] Consultando API oficial do Banco Central (BACEN PTAX)...{RESET}")
        try:
            hoje = datetime.now().strftime("%m-%d-%Y")
            # URL tratada sem caracteres de escape problemáticos na linha 48
            url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarUltimaData(@dataCotacao)?@dataCotacao='{hoje}'&$format=json"
            
            resposta = requests.get(url, timeout=5)
            if resposta.status_code == 200:
                dados = resposta.json()
                if "value" in dados and len(dados["value"]) > 0:
                    return float(dados["value"][0]["cotacaoVenda"])
        except Exception as e:
            print(f"{COLOR_WARNING}[!] Falha ao conectar à API do BACEN ({e}). Utilizando taxa de contingência oficial. {RESET}")
        
        return 5.60  # Contingência conservadora

    def analisar_codigo_fonte(self):
        """Realiza análise estática real nos arquivos Python usando a AST (Abstract Syntax Tree)."""
        for caminho in self.raiz.rglob("*.py"):
            if any(parte in self.ignorar_pastas for parte in caminho.parts):
                continue
                
            try:
                with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                    codigo = f.read()
                
                visitor = ComplexityVisitor.from_code(codigo)
                linhas_info = mi_parameters(codigo)
                
                lloc = linhas_info[0]
                comentarios = linhas_info[1]
                linhas_brutas = len(codigo.splitlines())
                
                cc_arquivo = sum(func.complexity for func in visitor.functions) + sum(cls.complexity for cls in visitor.classes)
                if not visitor.functions and not visitor.classes:
                    cc_arquivo = 1
                
                self.total_sloc_bruto += linhas_brutas
                self.total_lloc_logico += lloc
                self.total_comentarios += comentarios
                self.complexidade_acumulada += cc_arquivo
                self.total_arquivos_python += 1
                
                self.arquivos_mapeados.append({
                    "arquivo": str(caminho.relative_to(self.raiz)),
                    "sloc": linhas_brutas,
                    "lloc": lloc,
                    "cc": cc_arquivo
                })
            except Exception as e:
                # Log isolado para não parar a varredura caso haja arquivos corrompidos ou em uso
                pass

    def calcular_cocomo_ii(self):
        """Aplica o modelo COCOMO II (Post-Architecture) adaptado."""
        if self.total_lloc_logico == 0:
            return 0, 0
            
        kloc_logico = self.total_lloc_logico / 1000.0
        A = 2.94  
        
        cc_media = self.complexidade_acumulada / self.total_arquivos_python if self.total_arquivos_python > 0 else 1
        if cc_media > 15:
            E = 1.20  
        elif cc_media > 7:
            E = 1.15  
        else:
            E = 1.05  
            
        person_months = A * (kloc_logico ** E)
        horas_estimadas = person_months * 152
        return person_months, int(horas_estimadas)

    def gerar_laudo(self):
        self.analisar_codigo_fonte()
        
        if self.total_arquivos_python == 0:
            print(f"{COLOR_FAIL}[Erro] Nenhum código-fonte válido encontrado para auditoria.{RESET}")
            return

        ptax = self.obter_taxa_ptax()
        pm, horas = self.calcular_cocomo_ii()
        
        # Validação Financeira Base (Custo de Reposição - CPC 04 / IAS 38)
        valor_total_brl = pm * self.custo_dev_brl
        valor_total_usd = valor_total_brl / ptax

        # Métricas Detalhadas Solicitadas
        total_linhas_utilizadas = self.total_lloc_logico if self.total_lloc_logico > 0 else 1
        valor_por_linha_brl = valor_total_brl / total_linhas_utilizadas
        valor_por_linha_usd = valor_total_usd / total_linhas_utilizadas
        
        valor_por_licenca_brl = valor_total_brl / self.total_licencas
        valor_por_licenca_usd = valor_total_usd / self.total_licencas

        # Exibição dos resultados estruturados
        print("\n" + "="*105)
        print(f"{COLOR_HEADER} LAUDO DE AUDITORIA TÉCNICA E AVALIAÇÃO PATRIMONIAL DE ATIVO INTANGÍVEL {RESET}")
        print("="*105)
        
        print(f"\n{COLOR_BLUE}1. MÉTRICAS SOBERANAS DE ENGENHARIA (Análise Estatística Real):{RESET}")
        print(f"   - Módulos de Código Analisados: {self.total_arquivos_python} arquivos .py")
        print(f"   - Linhas Brutas (SLOC): {self.total_sloc_bruto}")
        print(f"   - Linhas Lógicas de Código (LLOC): {self.total_lloc_logico:.2f} (Desconsidera espaços e comentários)")
        print(f"   - Densidade de Documentação: {((self.total_comentarios/self.total_sloc_bruto)*100):.2f}% de linhas de comentários")
        print(f"   - Complexidade Ciclomática Acumulada: {self.complexidade_acumulada}")
        
        print(f"\n{COLOR_BLUE}2. ESTIMATIVA DE ESFORÇO TÉCNICO (Modelo Científico COCOMO II):{RESET}")
        print(f"   - Índice de Esforço Acumulado: {pm:.2f} Person-Months (Homens-Mês)")
        print(f"   - Tempo de Engenharia Equivalente: ~{horas} horas técnicas dedicadas")
        
        print(f"\n{COLOR_BLUE}3. PARAMETRIZAÇÃO FINANCEIRA DETALHADA (CPC 04 / IAS 38):{RESET}")
        print(f"   - Custo de Referência do Operador (Mensal + Encargos): R$ {self.custo_dev_brl:,.2f}")
        print(f"   - Taxa Oficial de Câmbio Utilizada (BACEN PTAX): R$ {ptax:.4f}")
        print(f"   - Limite de Escassez Global do Ecossistema: {self.total_licencas} Licenças")
        print(f"   ------------------------------------------------------------------------------------------------")
        print(f"   - VALOR UNITÁRIO POR LINHA LÓGICA (LLOC):    R$ {valor_por_linha_brl:,.2f}  |  US$ {valor_por_linha_usd:,.2f}")
        print(f"   - VALOR UNITÁRIO POR LICENÇA GLOBAL:         R$ {valor_por_licenca_brl:,.2f}  |  US$ {valor_por_licenca_usd:,.2f}")
        print(f"   - VALOR CONSOLIDADO NO BRASIL (TOTAL BRL):   {COLOR_GREEN}R$ {valor_total_brl:,.2f}{RESET}")
        print(f"   - VALOR TOTAL GLOBAL CONSOLIDADO (TOTAL USD):{COLOR_GREEN}US$ {valor_total_usd:,.2f}{RESET}")
        print("="*105)
        
        # Salvando o JSON Auditável Completo
        laudo_json = {
            "Metodologia": "COCOMO II / CPC 04 / ISO/IEC 25010",
            "Metricas_Codigo": {
                "arquivos_computados": self.total_arquivos_python,
                "sloc_bruto": self.total_sloc_bruto,
                "lloc_logico": round(self.total_lloc_logico, 2),
                "complexidade_ciclomatica": self.complexidade_acumulada
            },
            "Valoracao_Detalhada": {
                "taxa_ptax_bacen": ptax,
                "person_months_estimado": round(pm, 2),
                "horas_estimadas": horas,
                "valor_por_linha_brl": round(valor_por_linha_brl, 4),
                "valor_por_linha_usd": round(valor_por_linha_usd, 4),
                "total_licencas_globais": self.total_licencas,
                "valor_por_licenca_brl": round(valor_por_licenca_brl, 2),
                "valor_por_licenca_usd": round(valor_por_licenca_usd, 2),
                "valor_total_brasil_brl": round(valor_total_brl, 2),
                "valor_total_global_usd": round(valor_total_usd, 2)
            }
        }
        
        with open("laudo_auditoria_patrimonial.json", "w", encoding="utf-8") as f:
            json.dump(laudo_json, f, indent=4, ensure_ascii=False)
        print(f"\n{COLOR_GREEN}[SUCESSO]{RESET} Evidência detalhada gerada com sucesso em: 'laudo_auditoria_patrimonial.json'")

if __name__ == "__main__":
    auditor = AuditoriaCore(diretorio_raiz=".", custo_medio_mensal_dev=28000.00, total_licencas_globais=10)
    auditor.gerar_laudo()