import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -*- coding: utf-8 -*-
import requests
import logging
# Agora chamando a função correta que você tem no seu motor_dados
from core.motor_dados import inserir_cliente 

# Configuração de log
logging.basicConfig(level=logging.INFO)

def checar_licenca_na_nuvem(chave):
    logging.info("Verificando licença com servidor...")
    try:
        # A URL que você definiu para o seu serviço de segurança
        url_do_servidor = "https://sua-nuvem-de-seguranca.com/validar"
        
        # Fazendo a requisição real
        # Descomente a linha abaixo quando estiver pronto para testar com o servidor real
        # resposta = requests.post(url_do_servidor, data={'chave': chave}, timeout=5)
        # status_servidor = resposta.status_code
        
        # Mantendo sua lógica de simulação para evitar que o código trave agora:
        status_servidor = 200 
        
        if status_servidor == 200:
            # Registra o sucesso no seu banco de dados
            inserir_cliente("Nuvem_Auth", 1.0, "VALIDACAO_SUCESSO")
            return True
        else:
            inserir_cliente("Nuvem_Auth", 0.0, "VALIDACAO_NEGADA")
            return False
            
    except Exception as e:
        logging.error(f"Erro de conexão: {e}")
        inserir_cliente("Nuvem_Auth", 0.0, "ERRO_CONEXAO_NUVEM")
        return False

# --- EXECUÇÃO ---
if __name__ == "__main__":
    chave_teste = "THIERRY_2026_PRO"
    if checar_licenca_na_nuvem(chave_teste):
        print("\n[OK] Licença validada. Iniciando Mônaco Plan...")
    else:
        print("\n[ERRO CRÍTICO] Sistema bloqueado. Contate o administrador.")
        sys.exit()