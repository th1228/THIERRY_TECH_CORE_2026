import sys, os

# -*- coding: utf-8 -*-
"""
TTC GLOBAL - MÓDULO DE PRECIFICAÇÃO E COTAS GLOBAIS
Localização: core/precificacao_motor.py
"""

class GerenciadorCotasGlobais:
    def __init__(self, valor_base_referencia=50000.00, cotacao_euro=5.83):
        self.cotas = []
        self.cotacao_euro = cotacao_euro
        
        # Bloco Nacional: 3 Vagas exclusivas (Brasil) - Valores ajustados temporariamente
        valores_nacionais = [5000.00, 10000.00, 15000.00]
        for i, val in enumerate(valores_nacionais, start=1):
            self.cotas.append({
                "id": f"BR-0{i}", 
                "mercado": f"Brasil (Nacional - Tier {i})", 
                "valor_brl": val, 
                "moeda": "R$",
                "status": "Disponível"
            })
        
        # Bloco Internacional: Vagas Globais de Hiper-Luxo (Demais mercados)
        valor_intl_eur = 250000.00
        valor_intl_brl = valor_intl_eur * self.cotacao_euro
        for i in range(4, 8):
            self.cotas.append({
                "id": f"INT-0{i}", 
                "mercado": "Internacional (Global High-End)", 
                "valor_brl": valor_intl_brl, 
                "moeda": "R$",
                "status": "Disponível"
            })
            
        # Estados Unidos (Cota 08): 30x o valor base
        valor_usa = valor_base_referencia * 30
        self.cotas.append({
            "id": "INT-08",
            "mercado": "Estados Unidos (USA Plan)",
            "valor_brl": valor_usa,
            "moeda": "R$",
            "status": "Disponível / Master USA"
        })

        # Emirados Árabes / Oriente Médio (Cota 09): 40x o valor base
        valor_uae = valor_base_referencia * 40
        self.cotas.append({
            "id": "INT-09",
            "mercado": "Emirados Árabes / Oriente Médio (Dubai Plan)",
            "valor_brl": valor_uae,
            "moeda": "R$",
            "status": "Disponível / Master UAE"
        })

        # Mônaco (Cota 10): 50x o valor base
        valor_monaco = valor_base_referencia * 50
        self.cotas.append({
            "id": "INT-10",
            "mercado": "Mônaco (O Ápice Global Absoluto)",
            "valor_brl": valor_monaco,
            "moeda": "R$",
            "status": "Disponível / Exclusivo Master"
        })

    def obter_dados_cotas(self):
        """Retorna a lista completa de cotas para exibição na interface gráfica."""
        return self.cotas

    def obter_cota_por_pais(self, sigla):
        """Busca a cota correspondente com base na sigla do país (BR, US, MC)."""
        if not sigla:
            sigla = "BR"
            
        sigla = str(sigla).upper()
        mapeamento_ids = {
            "BR": "BR-01",
            "US": "INT-08",
            "MC": "INT-10"
        }
        id_alvo = mapeamento_ids.get(sigla, "BR-01")
        
        for cota in self.cotas:
            if cota["id"] == id_alvo:
                return {
                    "valor": int(cota["valor_brl"] * 100), 
                    "moeda": cota["moeda"],
                    "mercado": cota["mercado"]
                }
                
        return {
            "valor": 50000000, 
            "moeda": "R$",
            "mercado": "Padrão de Segurança"
        }

if __name__ == "__main__":
    motor = GerenciadorCotasGlobais()
    print("=" * 60)
    print("TTC GLOBAL — VALIDAÇÃO DE COTAS EM FILA")
    print("=" * 60)
    for cota in motor.obter_dados_cotas():
        print(f"[{cota['id']}] {cota['mercado']} ---> {cota['moeda']} {cota['valor_brl']:,.2f}")
    print("=" * 60)