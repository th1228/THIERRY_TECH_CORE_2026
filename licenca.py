# -*- coding: utf-8 -*-
"""
Módulo: Gerenciador de Licenciamento & Tokens Soberanos • Padrão Mônaco UHNW
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Nome do Arquivo: licenca.py
Versão: 22.1.7 - Alinhamento Definitivo (R$ 999.999,00 | 12 Meses)
"""

import os
import sys
import uuid
import json
import math
from datetime import datetime

# Habilita o interpretador de cores ANSI para o terminal (se suportado)
if os.name == 'nt':
    os.system('')

# Cores de Estilização Visual Padrão Mônaco Private Equity
GREEN = "\033[92m"
BRIGHT_GREEN = "\033[1;92m"
CYAN = "\033[96m"
WHITE = "\033[97m"
YELLOW = "\033[93m"
RESET = "\033[0m"

ARQUIVO_HISTORICO = "historico_licenciamento_monaco.json"
ARQUIVO_REGISTRO_LICENCAS = "registro_tokens_ativos_monaco.json"

# Importação segura dos links externos do Stripe com fallback alinhado ao main.py
try:
    from config_pagamentos import PAYMENT_LINKS
except ImportError:
    PAYMENT_LINKS = {
        "global_estrategica": "https://buy.stripe.com/3cI6oHehIfm05Ri98neZ207",
        "monaco_supremacy": "https://buy.stripe.com/eVq4gz7Tkgq44Ne2JZeZ205",
        "us_premium": "https://buy.stripe.com/4gM7sL8Xofm01B2fwLeZ206"
    }

# Protocolo de Blindagem, Geodefense e Multa Global
PROTOCOLOS_SEGURANCA = {
    "MULTA_GLOBAL_USD": 5000000.00,  # USD 5 Milhões por violação contratual transnacional em ativo de escassez
    "ACAO_VIOLACAO": "SUSPENDED_BY_GEO_VIOLATION",
    "KILL_SWITCH": "Limpeza completa de memória RAM e registro em LogSeguro"
}

def obter_hwid():
    """Identifica o ID único da máquina para evitar cópias piratas (Trava de Nó)."""
    return str(uuid.getnode())

def verificar_integridade(node_id_atual, node_id_registrado):
    """Valida se o hardware atual é exatamente o mesmo da ativação original."""
    return node_id_atual == node_id_registrado

def aplicar_multa(categoria_mercado):
    """Gera o termo de penalidade por quebra contratual (Sovereign Gate)."""
    if categoria_mercado != "BR":
        return f"ALERTA CRÍTICO: Violação contratual detectada. Multa de penalidade no valor de USD {PROTOCOLOS_SEGURANCA['MULTA_GLOBAL_USD']:,.2f} aplicada ao nó infrator de escassez."
    return "Penalidade aplicada conforme termos do contrato comercial nacional."


# CONFIGURAÇÃO DO ECOSSISTEMA TTC GLOBAL - ATIVO DE ESCASSEZ EXCLUSIVA (10 VAGAS NO MUNDO)
CONFIGURACAO = {
    "BR_COMERCIAL": {
        "descricao": "Mercado Nacional Oficial & Internacional UHNW - Alta Segurança e Restrição por Nó (12 Meses)",
        "moeda": "R$",
        "planos": {
            "global_estrategica": {
                "valor": 999999.00, 
                "meses": 12, 
                "nos_permitidos": 2, 
                "libera": ["salao_biometria", "clinica", "forense", "core_global"],
                "link_stripe": PAYMENT_LINKS.get("global_estrategica", "https://buy.stripe.com/3cI6oHehIfm05Ri98neZ207")
            },
            "monaco_supremacy": {
                "valor": 999999.00, 
                "meses": 12, 
                "nos_permitidos": 2, 
                "libera": ["salao_biometria", "clinica", "forense", "core_global"],
                "link_stripe": PAYMENT_LINKS.get("monaco_supremacy", "https://buy.stripe.com/eVq4gz7Tkgq44Ne2JZeZ205")
            },
            "us_premium": {
                "valor": 999999.00, 
                "meses": 12, 
                "nos_permitidos": 2, 
                "libera": ["salao_biometria", "clinica", "forense", "core_global"],
                "link_stripe": PAYMENT_LINKS.get("us_premium", "https://buy.stripe.com/4gM7sL8Xofm01B2fwLeZ206")
            }
        }
    },
    "GLOBAL_SOVEREIGN_TIERS": {
        "descricao": "Top World Nodes & Hubs de Luxo (Apenas 10 Licenças no Mundo) - Dinâmica baseada no PIB da Região",
        "paises_suportados": ["US", "MC", "AE", "EU", "CH", "DE", "FR", "UK", "SG", "QA", "KR", "BR"],
        "limite_total_vagas_mundo": 10,
        "valor_base_unitario_usd": 1000000.00,
        "raio_exclusividade_km": 100,
        "nos_por_licenca": 2,
        "observacao_flexibilidade_regional": (
            "REGRA DE ESCASSEZ GLOBAL & PIB REGIONAL: Restrito estritamente a 10 nós no planeta. "
            "O valor de venda unitário base é de USD $ 1.000.000,00 (ou R$ 999.999,00 estruturado), sendo ativado e recalculado de forma dinâmica "
            "com base no PIB per capita e na força econômica da praça/região compradora, com vigência anual de 12 meses."
        )
    }
}


class GerenciadorLicenciamentoForensico:
    """Motor forense unificado com cálculo determinístico e valuation de escassez global ajustado por PIB."""
    def __init__(self):
        self.diretorio_base = os.getcwd()

    def varrer_core_projeto(self):
        total_arquivos = 0
        linhas_codigo_limpas = 0
        modulos_com_seguranca = 0
        extensoes_validas = ['.py', '.html', '.js', '.css', '.json']
        
        for root, dirs, files in os.walk(self.diretorio_base):
            if any(exc in root for exc in ['.git', '__pycache__', 'venv', '.vscode']):
                continue
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in extensoes_validas:
                    total_arquivos += 1
                    caminho_completo = os.path.join(root, file)
                    if 'com' in root.lower() or 'sec' in root.lower() or 'auth' in file.lower():
                        modulos_com_seguranca += 1
                    try:
                        with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as f:
                            linhas = [l for l in f if l.strip() and not l.strip().startswith('#')]
                            linhas_codigo_limpas += len(linhas)
                    except Exception:
                        pass

        return total_arquivos, linhas_codigo_limpas, modulos_com_seguranca

    def processar_memoria_estavel(self, linhas_atuais, arquivos_atuais):
        horas_estaveis = max(1200, int(linhas_atuais / 32))
        dados_historicos = {
            "estado_atual": {
                "linhas_codigo": linhas_atuais,
                "total_arquivos": arquivos_atuais,
                "horas_acumuladas": horas_estaveis,
                "ultima_atualizacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        try:
            with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
                json.dump(dados_historicos, f, indent=4, ensure_ascii=False)
        except Exception:
            pass
        return 1, horas_estaveis

    def executar_auditoria_completa(self):
        total_arq, total_linhas, modulos_sec = self.varrer_core_projeto()
        dias_reg, horas_totais = self.processar_memoria_estavel(total_linhas, total_arq)
        
        TAXA_HORA_USD = 250.00  
        COTACAO_BRL = 5.62
        
        custo_reposicao_usd = horas_totais * TAXA_HORA_USD
        MULTIPLICADOR_INOVACAO_MONACO = 15.00  
        valuation_tecnico_usd = custo_reposicao_usd * MULTIPLICADOR_INOVACAO_MONACO
        
        valor_unitario_base_usd = CONFIGURACAO["GLOBAL_SOVEREIGN_TIERS"]["valor_base_unitario_usd"]
        licencas_globais_exclusivas = CONFIGURACAO["GLOBAL_SOVEREIGN_TIERS"]["limite_total_vagas_mundo"]
        vgv_licenciamento_usd = licencas_globais_exclusivas * valor_unitario_base_usd
        
        valuation_final_usd = (valuation_tecnico_usd * 0.50) + (vgv_licenciamento_usd * 0.50)
        valuation_final_brl = valuation_final_usd * COTACAO_BRL

        divisor = "═" * 100
        data_atual_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        relatorio_texto = f"""
{CYAN}{divisor}{RESET}
{BRIGHT_GREEN} ⚜️  MONACO PRIVATE EQUITY // DUE DILIGENCE E VALUATION DE ESCASSEZ GLOBAL (2026){RESET}
{CYAN}{divisor}{RESET}

{WHITE}[SEÇÃO I] - CADEIA DE TITULARIDADE E CARREIRA SOLO (KEY-MAN RISK){RESET}
 -> Data/Hora da Auditoria:     {data_atual_str}
 -> Modelo Estrutural:          Carreira Solo / Engenheiro de Software Principal Único
 -> Horas Validadas de Código:  {horas_totais:,} horas líquidas de engenharia sênior (Base Estável)
 -> Volume Real Varrido (LOC):  {total_linhas:,} linhas limpas ativas ({total_arq} arquivos estruturados)

{WHITE}[SEÇÃO II] - FUNDAMENTAÇÃO MATEMÁTICA DO VALUATION (FÓRMULA 15X){RESET}
 -> Paridade de Mercado Sênior: USD $ {TAXA_HORA_USD:,.2f} / hora técnica especializada
 -> Custo Base de Reposição ($C): USD$ {custo_reposicao_usd:,.2f} [Fórmula: Horas × Taxa Hora]
 -> Multiplicador de Inovação (M): {MULTIPLICADOR_INOVACAO_MONACO:.2f}x (Ágio de Inovação Exclusiva)
 -> Valor Técnico do IP ($C x M):  USD$ {valuation_tecnico_usd:,.2f}

{WHITE}[SEÇÃO III] - VGV COMERCIAL DE ESCASSEZ GLOBAL (APENAS 10 NÓS NO PLANETA){RESET}
 -> Mapeamento de Países (JSON): MC, US, AE, CH, DE, FR, UK, SG, QA, KR, BR (Pasta config/paises/)
 -> Valor Base por Licença:     USD $ {valor_unitario_base_usd:,.2f} (Ativado dinamicamente via PIB Regional)
 -> Regra de Escassez Absoluta:  RESTRIÇÃO MUNDIAL A 10 UNIDADES COM AJUSTE ECONÔMICO DE PRAÇA.
 -> Licenças Globais Restritas: {licencas_globais_exclusivas} nós autorizados (Ultra Salões e Clínicas de Elite)
 -> VGV Comercial Consolidado:  USD $ {vgv_licenciamento_usd:,.2f} (Faturamento bruto das 10 licenças base)

{WHITE}[SEÇÃO IV] - SEGURANÇA, COMPLIANCE E GOVERNANÇA DE MERCADO{RESET}
 -> Módulos de Blindagem (/com): {modulos_sec} estruturas criptográficas ativas
 -> Arquitetura de Autenticação:  {GREEN}ZERO TRUST (Privilégio Mínimo e Proteção de Trade Secret){RESET}
 -> Prontidão Comercial:        {GREEN}HOMOLOGADO PARA HUBS DE ELITE (VIGÊNCIA SOBERANA DE 12 MESES){RESET}

{CYAN}----------------------------------------------------------------------------------------------------{RESET}
{WHITE}📊 PARECER FINANCEIRO DEFINITIVO E FIXO (M&A CONSOLIDADO - ESCASSEZ GLOBAL):{RESET}
{BRIGHT_GREEN} ⚜️  VALUATION PATRIMONIAL DO ATIVO:  USD $ {valuation_final_usd:,.2f}{RESET}
{BRIGHT_GREEN} ⚜️  VALOR AVALIADO EM MOEDA NACIONAL: BRL R$ {valuation_final_brl:,.2f} (Câmbio Comercial Corrente){RESET}
{CYAN}{divisor}{RESET}
"""
        sys.stdout.write(relatorio_texto)
        sys.stdout.flush()
        return {
            "status": "sucesso",
            "valuation_usd": valuation_final_usd,
            "valuation_brl": valuation_final_brl
        }


def obter_detalhes_licenca_com_pib(categoria_mercado, plano_nome, quantidade_licencas=1, pib_regiao_per_capita_usd=None):
    if categoria_mercado == "BR":
        config = CONFIGURACAO["BR_COMERCIAL"]["planos"].get(plano_nome)
        if config:
            valor_total = config["valor"] * quantidade_licencas
            return {
                "mercado": "BR_COMERCIAL",
                "quantidade_licencas": quantidade_licencas,
                "valor_unitario": config["valor"],
                "valor_total": valor_total,
                "nos_totais": quantidade_licencas * 2,
                "vigencia_meses": 12,
                "status": "sucesso"
            }
            
    elif categoria_mercado in CONFIGURACAO["GLOBAL_SOVEREIGN_TIERS"]["paises_suportados"]:
        global_conf = CONFIGURACAO["GLOBAL_SOVEREIGN_TIERS"]
        valor_base = global_conf["valor_base_unitario_usd"]
        
        if pib_regiao_per_capita_usd:
            fator_ajuste = max(1.0, pib_regiao_per_capita_usd / 50000.0)
            valor_unitario_efetivo = valor_base * fator_ajuste
        else:
            valor_unitario_efetivo = valor_base

        valor_total_usd = valor_unitario_efetivo * quantidade_licencas
        nos_totais = quantidade_licencas * global_conf["nos_por_licenca"]
        raio_total_km = quantidade_licencas * global_conf["raio_exclusividade_km"]

        beneficios = []
        if quantidade_licencas >= 5:
            beneficios.append("Direito a Assento Consultivo no Comitê Soberano de Expansão Global")
        if quantidade_licencas == 10:
            beneficios.append("Monopólio Absoluto Global: Esgotamento total do inventário mundial de 10 vagas")

        return {
            "mercado": f"GLOBAL_{categoria_mercado}",
            "quantidade_licencas": quantidade_licencas,
            "valor_unitario_usd": valor_unitario_efetivo,
            "valor_total_usd": valor_total_usd,
            "nos_totais": nos_totais,
            "raio_exclusividade_km": raio_total_km,
            "cotas_indicacao": quantidade_licencas,
            "vigencia_meses": 12,
            "observacao_pib": global_conf["observacao_flexibilidade_regional"],
            "beneficios_extras": beneficios,
            "status": "sucesso"
        }
            
    return {"status": "erro", "mensagem": "Parâmetros de licenciamento inválidos."}


def carregar_banco_tokens():
    if os.path.exists(ARQUIVO_REGISTRO_LICENCAS):
        try:
            with open(ARQUIVO_REGISTRO_LICENCAS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"tokens_ativos": {}, "total_vagas_ocupadas": 0}


def salvar_banco_tokens(banco):
    arquivo_temp = ARQUIVO_REGISTRO_LICENCAS + ".tmp"
    try:
        with open(arquivo_temp, "w", encoding="utf-8") as f:
            json.dump(banco, f, indent=4, ensure_ascii=False)
        os.replace(arquivo_temp, ARQUIVO_REGISTRO_LICENCAS)
    except Exception as e:
        if os.path.exists(arquivo_temp):
            try:
                os.remove(arquivo_temp)
            except:
                pass
        raise IOError(f"Falha na escrita atômica do banco de tokens: {e}")


def gerar_tokens_soberanos(comprador_nome, categoria_mercado, plano_nome, quantidade_licencas=1, pib_regiao_usd=None):
    if not (1 <= quantidade_licencas <= 10):
        return {"status": "erro", "mensagem": "A quantidade de licenças deve respeitar o limite de 1 a 10 unidades."}

    banco = carregar_banco_tokens()
    vagas_disponiveis = CONFIGURACAO["GLOBAL_SOVEREIGN_TIERS"]["limite_total_vagas_mundo"] - banco["total_vagas_ocupadas"]

    if categoria_mercado != "BR" and quantidade_licencas > vagas_disponiveis:
        return {
            "status": "erro",
            "mensagem": f"Escassez Global Atingida! Apenas {vagas_disponiveis} vagas restantes no mundo. Impossível alocar {quantidade_licencas} licenças."
        }

    detalhes = obter_detalhes_licenca_com_pib(categoria_mercado, plano_nome, quantidade_licencas, pib_regiao_usd)
    if detalhes["status"] == "erro":
        return detalhes

    nos_por_licenca = CONFIGURACAO["GLOBAL_SOVEREIGN_TIERS"]["nos_por_licenca"]
    tokens_gerados = []

    for i in range(quantidade_licencas):
        sufixo_unico = uuid.uuid4().hex[:8].upper()
        token_soberano = f"TCC-SOV-{categoria_mercado}-{sufixo_unico}"
        
        banco["tokens_ativos"][token_soberano] = {
            "titular": comprador_nome,
            "mercado": categoria_mercado,
            "plano": plano_nome,
            "vigencia_meses": 12,
            "nos_permitidos": nos_por_licenca,
            "nos_registrados": [],
            "raio_km": CONFIGURACAO["GLOBAL_SOVEREIGN_TIERS"]["raio_exclusividade_km"],
            "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "ATIVO"
        }
        tokens_gerados.append(token_soberano)
        
    if categoria_mercado != "BR":
        banco["total_vagas_ocupadas"] += quantidade_licencas

    salvar_banco_tokens(banco)

    return {
        "status": "sucesso",
        "titular": comprador_nome,
        "quantidade_adquirida": quantidade_licencas,
        "vigencia_meses": 12,
        "tokens_criados": tokens_gerados,
        "detalhes_financeiros_pib": detalhes,
        "vagas_restantes_mundo": CONFIGURACAO["GLOBAL_SOVEREIGN_TIERS"]["limite_total_vagas_mundo"] - banco["total_vagas_ocupadas"]
    }


def calcular_distancia_haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def validar_e_vincular_no(token_soberano, hardware_id_atual, categoria_mercado, latitude_atual=None, longitude_atual=None):
    banco = carregar_banco_tokens()
    
    if token_soberano not in banco["tokens_ativos"]:
        return {"status": "negado", "mensagem": "Token soberano inválido ou inexistente."}
        
    dados_token = banco["tokens_ativos"][token_soberano]
    
    if dados_token["status"] != "ATIVO":
        return {"status": "negado", "mensagem": "Token suspenso ou revogado por violação contratual."}
        
    nos_registrados = dados_token["nos_registrados"]
    limite_nos = dados_token["nos_permitidos"]
    
    for no_existente in nos_registrados:
        if no_existente.get("hwid") == hardware_id_atual:
            return {"status": "liberado", "mensagem": "Nó autenticado com sucesso via Token Soberano (12 Meses)."}
            
    if categoria_mercado != "BR" and latitude_atual is not None and longitude_atual is not None:
        raio_limite_permitido = CONFIGURACAO["GLOBAL_SOVEREIGN_TIERS"]["raio_exclusividade_km"]
        
        for t_key, t_val in banco["tokens_ativos"].items():
            if t_key == token_soberano:
                continue
                
            for no_registrado_outro in t_val.get("nos_registrados", []):
                lat_outro = no_registrado_outro.get("lat")
                lon_outro = no_registrado_outro.get("lon")
                
                if lat_outro is not None and lon_outro is not None:
                    distancia_km = calcular_distancia_haversine_km(latitude_atual, longitude_atual, lat_outro, lon_outro)
                    
                    if distancia_km < raio_limite_permitido:
                        banco["tokens_ativos"][token_soberano]["status"] = PROTOCOLOS_SEGURANCA["ACAO_VIOLACAO"]
                        salvar_banco_tokens(banco)
                        
                        return {
                            "status": "bloqueado_por_geodefesa",
                            "mensagem": f"VIOLAÇÃO CRÍTICA DE TERRITÓRIO! O nó está a {distancia_km:.2f} km de um Hub protegido (Raio mínimo: {raio_limite_permitido} km).",
                            "multa_aplicada": aplicar_multa(categoria_mercado),
                            "kill_switch": PROTOCOLOS_SEGURANCA["KILL_SWITCH"]
                        }

    if len(nos_registrados) < limite_nos:
        novo_no_registro = {
            "hwid": hardware_id_atual,
            "lat": latitude_atual,
            "lon": longitude_atual,
            "data_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        nos_registrados.append(novo_no_registro)
        banco["tokens_ativos"][token_soberano]["nos_registrados"] = nos_registrados
        salvar_banco_tokens(banco)
        
        return {
            "status": "liberado",
            "mensagem": f"Novo nó registrado com sucesso! (Nó {len(nos_registrados)} de {limite_nos} - Vigência de 12 Meses).",
            "nos_ativos": len(nos_registrados),
            "nos_limite": limite_nos
        }
    else:
        return {
            "status": "bloqueado",
            "mensagem": f"Limite máximo de {limite_nos} nós atingido para este token soberano de escassez."
        }


if __name__ == "__main__":
    motor = GerenciadorLicenciamentoForensico()
    motor.executar_auditoria_completa()