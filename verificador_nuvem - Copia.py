import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -*- coding: utf-8 -*-
import requests
import logging
import sys
# Importa o seu motor de dados para registrar a auditoria
from core.motor_dados import processar_dados 

# Configuração de log
logging.basicConfig(level=logging.INFO)

def checar_licenca_na_nuvem(chave):
    logging.info("Verificando licença com servidor...")
    try:
        # URL de teste
        url_do_servidor = "https://sua-nuvem-de-seguranca.com/validar"
        # Em um cenário real, você enviaria a chave aqui
        # Por enquanto, simulamos uma resposta positiva para o teste
        # resposta = requests.post(url_do_servidor, data={'chave': chave}, timeout=5)
        
        # SIMULAÇÃO: Vamos fingir que o servidor respondeu 200 (OK)
        status_servidor = 200 
        
        if status_servidor == 200:
            processar_dados({'tipo': 'autenticacao', 'status': 'sucesso'})
            return True
        else:
            processar_dados({'tipo': 'autenticacao', 'status': 'falha_licenca'})
            return False
            
    except Exception as e:
        logging.error(f"Erro de conexão: {e}")
        processar_dados({'tipo': 'autenticacao', 'status': 'erro_conexao'})
        return False

# --- O QUE FAZ ELE COMEÇAR SOZINHO ---
if __name__ == "__main__":
    chave_teste = "THIERRY_2026_PRO"
    if checar_licenca_na_nuvem(chave_teste):
        print("\n[OK] Licença validada. Iniciando Mônaco Plan...")
        # AQUI VOCÊ PODE CHAMAR O SEU OUTRO SCRIPT PRINCIPAL, EX:
        # import gui_main
        # gui_main.iniciar()
    else:
        print("\n[ERRO CRÍTICO] Sistema bloqueado. Contate o administrador.")
        sys.exit()