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
import sys
import os

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

"""
TTC GLOBAL - MOTOR DE FATURAMENTO E ORDEM DE PAGAMENTO GLOBAL
Localização: core/gerador_faturamento.py
"""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import time
from core.precificacao_motor import GerenciadorCotasGlobais
from core.gerenciador_geografico import gerente_geo

class GeradorFaturamento:
    def __init__(self, lang: str = "PT"):
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.gerenciador_cotas = GerenciadorCotasGlobais()

    def gerar_ordem_pagamento_global(self):
        """Identifica o contexto atual e gera a ordem de pagamento real baseada na cota e região (Blindado contra None)."""
        try:
            pais_codigo = gerente_geo.obter("codigo_pais") or "BR"
            pais_nome = gerente_geo.obter("nome_pais") or "Brasil"
            
            cotas = self.gerenciador_cotas.obter_dados_cotas()
            
            # Fallback de segurança se as cotas não carregarem corretamente
            if not cotas or not isinstance(cotas, list):
                cota_selecionada = {
                    "id": "COTA-FALLBACK",
                    "mercado": "Global Standard",
                    "valor_brl": 50000.0,
                    "moeda": "R$"
                }
            else:
                # Seleção segura baseada no país ativo com checagem de limites
                if pais_codigo == "BR":
                    cota_selecionada = cotas[0] if len(cotas) > 0 else cotas[0]
                elif "Estados Unidos" in str(pais_nome) or pais_codigo == "US":
                    cota_selecionada = next((c for c in cotas if "Estados Unidos" in str(c.get('mercado', ''))), cotas[min(7, len(cotas)-1)])
                elif "Mônaco" in str(pais_nome) or pais_codigo == "MC":
                    cota_selecionada = next((c for c in cotas if "Mônaco" in str(c.get('mercado', ''))), cotas[min(9, len(cotas)-1)])
                else:
                    cota_selecionada = cotas[min(3, len(cotas)-1)]

            id_cota = cota_selecionada.get('id', 'COTA-01')
            mercado_nome = cota_selecionada.get('mercado', 'Global')
            valor = cota_selecionada.get('valor_brl', 50000.0)
            moeda = cota_selecionada.get('moeda', 'R$')

            nome_arquivo = os.path.join(self.output_dir, f"Ordem_Pagamento_{id_cota}_{pais_codigo}.pdf")
            
            c = canvas.Canvas(nome_arquivo, pagesize=A4)
            largura, altura = A4
            
            # Design All Black / High-End
            c.setFillColorRGB(0.04, 0.04, 0.04)
            c.rect(0, 0, largura, altura, fill=1)
            
            # Detalhes Dourados / Texto
            c.setFillColorRGB(0.77, 0.62, 0.35) # #C5A059
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, altura - 60, "THIERRY GLOBAL TECH — SOBERANIA E AQUISIÇÃO")
            
            c.setFont("Helvetica", 11)
            c.setFillColorRGB(1, 1, 1)
            c.drawString(50, altura - 95, f"Cota Vinculada: {id_cota} — {mercado_nome}")
            c.drawString(50, altura - 120, f"Jurisdição / Região: {pais_nome} ({pais_codigo})")
            
            valor_fmt = f"{moeda} {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            c.drawString(50, altura - 145, f"Valor da Licença Global: {valor_fmt}")
            c.drawString(50, altura - 170, f"Timestamp de Emissão: {time.strftime('%d/%m/%Y %H:%M:%S')}")
            
            # Instruções de Liquidação com sua Chave Pix / CNPJ
            c.setFillColorRGB(0.77, 0.62, 0.35)
            c.setFont("Helvetica-Bold", 13)
            c.drawString(50, altura - 220, "PROTOCOLO DE LIQUIDAÇÃO FINANCEIRA CORPORATIVA:")
            
            c.setFont("Helvetica", 10)
            c.setFillColorRGB(0.85, 0.85, 0.85)
            c.drawString(50, altura - 250, "• Modalidade: Pix Direto de Alta Governança / Conta PJ")
            c.drawString(50, altura - 275, f"• Chave Pix (CNPJ): 57.646.942/0001-69")
            c.drawString(50, altura - 300, "• Criptografia do Nó: Injeção de Hash Air-Gapped após confirmação de custódia")
            
            c.drawString(50, altura - 360, "Documento gerado automaticamente pelo ecossistema central de governança.")
            
            c.save()
            caminho_absoluto = os.path.abspath(nome_arquivo)
            
            # Sincronização automática com a Memória Comum 🧠
            try:
                memoria.salvar_dados("ordem_pagamento", {
                    "id_cota": id_cota,
                    "mercado": mercado_nome,
                    "valor": valor,
                    "caminho_pdf": caminho_absoluto,
                    "status": "GERADO_COM_SUCESSO"
                })
            except Exception:
                pass

            print(f"[FATURAMENTO REAL] Dossiê gerado para {pais_nome} ({id_cota}): {nome_arquivo}")
            return caminho_absoluto
            
        except Exception as e:
            print(f"[ERRO CRÍTICO NO FATURAMENTO] {e}")
            return None

# Instância global para uso no ecossistema
_faturamento_global = GeradorFaturamento()

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    return _faturamento_global.gerar_ordem_pagamento_global()