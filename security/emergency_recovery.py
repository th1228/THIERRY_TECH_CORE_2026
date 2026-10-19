# =====================================================================
# ARQUIVO: security/emergency_recovery.py
# Módulo de Recuperação de Desastres e Override de Segurança
# =====================================================================

import os
import sys

# Garante a raiz do projeto no path do Python
raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if raiz_projeto not in sys.path:
    sys.path.append(raiz_projeto)

# Importação absoluta limpa e direta (Zero erros do Pylance)
from security.log_seguro import LogSeguro

logger = LogSeguro()

class EmergencyRecovery:
    """
    Controlador de Emergência para desbloqueio de instâncias travadas
    por falsos positivos ou falhas de integridade no ecossistema.
    """
    
    # Senha mestre configurada pelo operador
    SENHA_MESTRE = "124577"

    @staticmethod
    def validar_token_mestre(token_fornecido: str) -> bool:
        """Valida se o token de resgate inserido confere com a chave mestre."""
        return token_fornecido.strip() == EmergencyRecovery.SENHA_MESTRE

    @classmethod
    def executar_reset_total(cls, token_fornecido: str) -> bool:
        """Executa o desbloqueio forçado e limpa as flags de restrição do sistema."""
        print("\033[93m[EMERGÊNCIA] Acionando protocolo de recuperação de desastres...\033[0m")
        
        # Validação de Segurança (Token ou Variável de Ambiente Admin Override)
        token_valido = cls.validar_token_mestre(token_fornecido)
        override_ativo = os.getenv("THIEXEC_ADMIN_OVERRIDE") == "true"

        if not token_valido and not override_ativo:
            logger.registrar("SECURITY_BREACH", "CRITICO", "Tentativa de bypass de emergência com credenciais inválidas.")
            print("\033[91m[ERRO] Credenciais de emergência rejeitadas! Acesso negado.\033[0m")
            return False

        print("\033[92m[SUCESSO] Credenciais validadas. Iniciando procedimento de limpeza...\033[0m")

        # Remoção de ficheiros de bloqueio/trava locais do sistema (se existirem)
        caminho_lock = os.path.join(os.path.dirname(__file__), 'system.lock')
        if os.path.exists(caminho_lock):
            try:
                os.remove(caminho_lock)
                print(" -> Arquivo de bloqueio (system.lock) removido com sucesso.")
            except Exception as e:
                print(f" -> Aviso ao remover lock: {e}")
        else:
            print(" -> Nenhum arquivo de bloqueio ativo encontrado.")

        # Registo de Auditoria de Resgate
        logger.registrar("EMERGENCY_OVERRIDE", "ALERTA", "O sistema foi destravado manualmente via script de recuperação.")
        print("\033[92m[CONCLUÍDO] Sistema restabelecido ao estado operacional padrão com sucesso.\033[0m")
        return True


def efeito_terminal(texto, cor_codigo="\033[96m", delay=0.012):
    """Efeito visual de terminal para logs de recuperação."""
    print(cor_codigo, end="", flush=True)
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
    print("\033[0m")


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    
    print("\033[94m" + "=" * 65 + "\033[0m")
    efeito_terminal(" THIEXEC TECH CORE 2026 - PROTOCOLO DE RECUPERAÇÃO", "\033[95m")
    print("\033[94m" + "=" * 65 + "\033[0m")
    
    token_input = input("\n\033[93mInsira o Token Mestre de Recuperação: \033[0m")
    print()
    
    sucesso = EmergencyRecovery.executar_reset_total(token_input)
    
    print("\033[94m" + "=" * 65 + "\033[0m")
    if sucesso:
        efeito_terminal(" STATUS: SISTEMA DESTRAVADO E PRONTO PARA OPERAR.", "\033[92m")
    else:
        efeito_terminal(" STATUS: OPERAÇÃO ABORTADA. ACESSO NEGADO.", "\033[91m")
    print("\033[94m" + "=" * 65 + "\n" + "\033[0m")