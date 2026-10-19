# -*- coding: utf-8 -*-
# =====================================================================
# CAMADA DE GEODEFESA & PERÍMETRO GLOBAL (MONACO COMPLIANT)
# CONFORMIDADE: PRIVACY BY DESIGN - ZERO RETENÇÃO EM DISCO (RAM VOLÁTIL)
# =====================================================================

import sys
import os

# Adiciona a raiz do projeto ao path do Python para garantir o acesso à core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import math
import uuid
import datetime
from core.memoria_comum import memoria_global

def calcular_distancia_km(lat1, lon1, lat2, lon2):
    # Fórmula de Haversine para cálculo preciso de distância entre coordenadas globais
    R = 6371.0  # Raio da Terra em km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)
    ) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))  
    return R * c

def gerar_token_titular_global():
    return f"TTC-GLOBAL-{uuid.uuid4().hex[:8].upper()}"

def gerar_senha_temporaria_perimetro():
    return f"TMP-{uuid.uuid4().hex[:6].upper()}"

def registrar_bonus_indicacao(empresa_indicadora):
    # Sincroniza o registro de bônus estritamente com a memória volátil central
    estado_atual = memoria_global.ler_dados()
    registro_bonus = estado_atual.get("registro_indicacoes_bonus", {})
    
    if empresa_indicadora not in registro_bonus:
        registro_bonus[empresa_indicadora] = {
            "indicacoes_realizadas": 1,
            "desconto_acumulado": "10% de desconto na próxima renovação"
        }
    else:
        registro_bonus[empresa_indicadora]["indicacoes_realizadas"] += 1
        
    memoria_global.salvar_dados("registro_indicacoes_bonus", registro_bonus)
    print(f"\n[REGISTRO FINANCEIRO - RAM] Bonificação computada para '{empresa_indicadora}': Desconto garantido na próxima renovação.")

def executar_onboarding_e_indicacao():
    print("\n" + "="*60)
    print(" [PAINEL DE CADASTRO E CO-PARTICIPAÇÃO - TCC GLOBAL]")
    print("="*60)
    
    nome_empresa = input("-> Digite o nome da sua Empresa / Clínica: ").strip()
    endereco = input("-> Digite o endereço completo: ").strip()
    
    print("\n-> Possui indicação de algum parceiro ou rede de elite?")
    possui_indicacao = input("-> Digite 'S' para SIM ou 'N' para NÃO: ").strip().upper()
    
    if possui_indicacao == 'S':
        indicado_por = input("-> Digite o NOME DA EMPRESA ou do AMIGO PARCEIRO que indicou: ").strip()
        print(f"[REGISTRO DE REDE] Indicação de '{indicado_por}' computada com segurança.")
        registrar_bonus_indicacao(indicado_por)
    
    print("\n[DADOS SALVOS - VOLÁTIL] Informações armazenadas estritamente em memória RAM.")
    print("[REDIRECIONAMENTO] Abrindo gateway de pagamento seguro (Stripe)...")
    
    return simular_pagamento_stripe(nome_empresa)

def simular_pagamento_stripe(nome_empresa):
    print(f"\n[STRIPE CHECKOUT] Processando fatura de licença para: {nome_empresa}...")
    print("[STRIPE APROVADO] Pagamento confirmado! Nó ativado de forma segura.")
    return True

def validar_geofencing_global(nova_lat, nova_lon, token_titular_atual, base_licencas_ativas):
    RAIO_LIMITE_KM = 100.0

    for licenca in base_licencas_ativas:
        distancia = calcular_distancia_km(nova_lat, nova_lon, licenca["lat"], licenca["lon"])

        if distancia < RAIO_LIMITE_KM:
            if licenca["tenant_id"] == token_titular_atual:
                print(f"[AUTORIZADO GLOBAL] Expansão multiloja permitida para o titular {token_titular_atual} (Distância: {round(distancia, 2)} km).")
                return True
            else:
                print(f"\n[BLOQUEIO GLOBAL - MÔNACO] Conflito territorial detectado: Raio de 100km violado.")
                
                senha_desafio = gerar_senha_temporaria_perimetro()
                solicitacao_id = uuid.uuid4().hex[:8].upper()
                expiracao = datetime.datetime.now() + datetime.timedelta(hours=24)
                
                # Salva solicitações pendentes centralizadas na memória RAM comum
                estado_atual = memoria_global.ler_dados()
                solicitacoes = estado_atual.get("solicitacoes_pendentes", {})
                solicitacoes[solicitacao_id] = {
                    "senha": senha_desafio,
                    "expiracao": expiracao.isoformat()
                }
                memoria_global.salvar_dados("solicitacoes_pendentes", solicitacoes)
                
                print("*" * 60)
                print(f" MENSAGEM DE GOVERNANÇA: Acesso em zona restrita (perímetro de 100 km).")
                print(f" Código da Requisição: {solicitacao_id}")
                print("*" * 60)
                
                tentativa_senha = input("-> [ADMIN] Insira a senha temporária para desbloquear o perímetro: ").strip()
                
                if tentativa_senha == senha_desafio:
                    print(f"\n[ACESSO MASTER CONCEDIDO] Perímetro liberado com sucesso!")
                    return executar_onboarding_e_indicacao()
                else:
                    print("\n[ACESSO NEGADO] Senha inválida ou expirada. Instalação bloqueada.")
                    return False

    print("[AUTORIZADO GLOBAL] Posição aprovada fora do perímetro restrito.")
    return executar_onboarding_e_indicacao()

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DIRETO - CAMADA DE GEODEFESA & MEMÓRIA GLOBAL")
    print("=" * 60)
    
    licencas_exemplo = [
        {"tenant_id": "TTC-GLOBAL-ORIGINAL", "lat": -2.5307, "lon": -44.3068}
    ]
    
    try:
        validar_geofencing_global(
            nova_lat=-2.4000, 
            nova_lon=-44.2000, 
            token_titular_atual="TTC-GLOBAL-NOVO", 
            base_licencas_ativas=licencas_exemplo
        )
    except Exception as e:
        print(f"Execução finalizada: {e}")
    print("=" * 60)