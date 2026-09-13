# -*- coding: utf-8 -*-
import os
import sys

# Ajusta o path para garantir que o 'core' seja encontrado a partir da raiz do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def executar_protocolo_emergencia():
    """
    Protocolo de Autodestruição (Camada 5 - Sentinela)
    Limpa a memória e protege o core TTC Global.
    """
    print("!!! ALERTA: BRECHA DETECTADA - INICIANDO PROTOCOLO DE AUTODESTRUIÇÃO !!!")
    
    # 1. impeza de logs sensíveis
    try:
        if os.path.exists("logs_sistema_ttc.log"):
            os.remove("logs_sistema_ttc.log")
            print("Logs sanitizados.")
    except Exception as e:
        print(f"Erro na limpeza de logs: {e}")

    # 2. Encerrar sessão da Memória
    try:
        from core.memoria_comum import instancia_memoria
        instancia_memoria.limpar_sessao()
        print("Memória de sessão purgada com sucesso.")
    except Exception as e:
        print(f"Erro ao purgar memória: {e}")

    # 3. Travar o sistema
    print("Core do sistema isolado. Acesso encerrado.")
    sys.exit("Sistema travado por segurança.")