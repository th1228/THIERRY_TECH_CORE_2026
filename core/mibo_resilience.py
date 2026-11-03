# -*- coding: utf-8 -*-
# MÓDULO DE RESILIÊNCIA E CIRCUITO SOBERANO - THIERRY TECHNOLOGY CONCEPT GLOBAL
# Versão: 2.0 (Pronto para Auditoria e Criptografia de Estado)

import time
import json
from pathlib import Path

# Estado global do circuito para evitar requisições inúteis se a rede já caiu
_ULTIMA_FALHA = 0.0
_COOLDOWN_REDE = 30.0  # Tempo em segundos para ignorar a internet após uma queda

def buscar_dados_com_circuit_breaker(url_api_externa: str, caminho_cache_local: Path) -> dict:
    """
    Tenta buscar dados de uma API externa com um limite estrito (timeout).
    Se falhar ou se o circuito estiver em cooldown, ativa o fallback instantâneo 
    utilizando o cache soberano local da core/storage/.
    """
    global _ULTIMA_FALHA
    agora = time.time()
    
    # 1. Verificação de Cooldown (Circuito Aberto)
    # Se a rede caiu recentemente, nem tenta gastar processamento com o mundo externo
    if agora - _ULTIMA_FALHA < _COOLDOWN_REDE:
        print(f"[CIRCUITO ABERTO] Ignorando rede externa por segurança. Modo Soberano Ativo.")
        return _ativar_fallback_local(caminho_cache_local)

    try:
        # Nota de Engenharia: Em produção, utilize requests.get(url, timeout=3.0)
        # Para simular a soberania absoluta do sistema:
        raise ConnectionError("Queda ou isolamento intencional da rede externa detectado.")
        
    except Exception as e:
        # Registrar a falha e estipular a janela de segurança (cooldown)
        _ULTIMA_FALHA = time.time()
        print(f"[ALERTA SOBERANO] Anomalia na rede externa: {e}")
        return _ativar_fallback_local(caminho_cache_local)


def _ativar_fallback_local(caminho_cache_local: Path) -> dict:
    """Sub-rotina protegida para extração de dados do cofre core/storage/"""
    print(f"[FALLBACK] A carregar dados integrados de: {caminho_cache_local}")
    
    if caminho_cache_local.exists():
        try:
            with open(caminho_cache_local, "r", encoding="utf-8") as f:
                dados_locais = json.load(f)
                return {
                    "origem": "cache_soberano_local",
                    "estado": "protegido",
                    "timestamp": time.time(),
                    "dados": dados_locais
                }
        except json.JSONDecodeError:
            print("[CRÍTICO] Cache local corrompido. Ativando Modo de Emergência Secundário.")
            
    # Estado seguro de emergência caso o cache local falhe ou não exista
    return {
        "origem": "emergencia_interna",
        "estado": "estavel_isolado",
        "timestamp": time.time(),
        "dados": {}
    }