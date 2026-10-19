# -*- coding: utf-8 -*-
import os
import json
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

ARQUIVO_REGISTRO_LICENCAS = "registro_tokens_ativos_monaco.json"
SENHA_MASTER_OFICIAL = "124577"

def validar_senha_master(senha_digitada):
    """Valida se a senha informada no painel administrativo corresponde à credencial master de escassez."""
    if senha_digitada == SENHA_MASTER_OFICIAL:
        return {"status": "sucesso", "mensagem": "Acesso Master autorizado pelo protocolo Mônaco."}
    return {"status": "negado", "mensagem": "ALERTA: Senha master incorreta. Tentativa de intrusão registrada."}

def carregar_dados_empresas():
    """Carrega o banco de tokens e empresas cadastradas no ecossistema."""
    if os.path.exists(ARQUIVO_REGISTRO_LICENCAS):
        try:
            with open(ARQUIVO_REGISTRO_LICENCAS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"tokens_ativos": {}, "total_vagas_ocupadas": 0}

def salvar_dados_empresas(banco):
    """
    Salva de forma atômica o banco atualizado utilizando arquivo temporário `.tmp` 
    para evitar corrupção de dados sob concorrência.
    """
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
        raise IOError(f"Falha na escrita atômica do registro de licenças: {e}")

def alterar_status_empresa(senha_digitada, token_ou_empresa, novo_status):
    """
    Permite bloquear ou desbloquear manualmente o painel/empresa 
    exigindo obrigatoriamente a senha master oficial.
    """
    auth = validar_senha_master(senha_digitada)
    if auth["status"] != "sucesso":
        return auth

    banco = carregar_dados_empresas()
    encontrado = False

    for token, dados in banco["tokens_ativos"].items():
        if token == token_ou_empresa or dados.get("titular", "").lower() == token_ou_empresa.lower():
            dados["status"] = novo_status.upper() # Ex: "ATIVO" ou "BLOQUEADO"
            encontrado = True
            break

    if encontrado:
        salvar_dados_empresas(banco)
        return {
            "status": "sucesso", 
            "mensagem": f"Status da empresa alterado para: {novo_status.upper()} com sucesso sob governança Mônaco."
        }
    
    return {"status": "erro", "mensagem": "Empresa ou token soberano não encontrado no registro global."}

def verificar_vigencia_licenca(token_ou_empresa):
    """Verifica a vigência temporal da licença e executa o bloqueio automático se o prazo expirar."""
    banco = carregar_dados_empresas()
    
    for token, dados in banco["tokens_ativos"].items():
        if token == token_ou_empresa or dados.get("titular", "").lower() == token_ou_empresa.lower():
            if dados.get("status") != "ATIVO":
                return {"status": "expirado_ou_bloqueado", "mensagem": "Acesso suspenso ou licença inativa no ecossistema."}
            
            data_criacao_str = dados.get("data_criacao")
            if data_criacao_str:
                data_criacao = datetime.strptime(data_criacao_str, "%Y-%m-%d %H:%M:%S")
                dias_decorridos = (datetime.now() - data_criacao).days
                
                # Ciclo padrão de 365 dias para expiração automática
                if dias_decorridos > 365:
                    dados["status"] = "EXPIRADO_AUTOMATICO"
                    salvar_dados_empresas(banco)
                    return {
                        "status": "expirado_ou_bloqueado", 
                        "mensagem": "Prazo de vigência anual esgotado. Sistema bloqueado automaticamente."
                    }
                    
            return {"status": "ativo", "mensagem": "Licença dentro do prazo de vigência operacional."}
            
    return {"status": "erro", "mensagem": "Registro de licença não localizado no sistema."}