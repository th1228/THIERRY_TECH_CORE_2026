import os
import json
from datetime import datetime
from metrics import STORAGE_DIR, STORAGE_PATH, log_status, salvar_dados_matrix

# Estrutura de fábrica (Estado Inicial do Sistema)
CONFIG_PADRAO_ELITE = {
    "sistema": {
        "nome": "THIERRY_TECH_CORE",
        "versao": "2026.1.0",
        "status": "Iniciando",
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    "configuracoes_rede": {
        "host": "127.0.0.1",
        "porta": 8080,
        "debug": True
    },
    "metricas_acumuladas": {
        "requisicoes_totais": 0,
        "tempo_atividade_segundos": 0,
        "historico_erros": []
    }
}

def inicializar_sistema():
    """Garante o estado inicial do sistema (Bootstrapping)."""
    print("-" * 50)
    log_status("VERIFICANDO ESTADO DE INICIALIZAÇÃO DA MATRIX...")
    print("-" * 50)
    
    # 1. Verifica se a pasta storage existe
    if not os.path.exists(STORAGE_DIR):
        log_status(f"Pasta storage não encontrada. Criando diretório em: {STORAGE_DIR}")
        os.makedirs(STORAGE_DIR, exist_ok=True)

    # 2. Verifica se o arquivo de dados já existe
    if os.path.exists(STORAGE_PATH):
        log_status("Arquivo de persistência já existente detectado.")
        log_status("Nenhuma alteração foi necessária. Preservando integridade dos dados.")
        
        # Apenas para conferência, vamos ler o que já está lá
        with open(STORAGE_PATH, "r", encoding="utf-8") as f:
            dados_atuais = json.load(f)
        log_status(f"Sistema pronto. Versão atual rodando: {dados_atuais.get('sistema', {}).get('versao', 'Desconhecida')}")
    
    else:
        log_status("Primeira execução detectada! Arquivo de dados ausente.")
        log_status("Injetando configurações de fábrica na Matrix...")
        
        # Salva as configurações padrão usando a função do nosso módulo metrics
        salvar_dados_matrix(CONFIG_PADRAO_ELITE)
        log_status("Inicialização da Matrix concluída com sucesso!")

if __name__ == "__main__":
    inicializar_sistema()
    print("-" * 50)