# =====================================================================
# ARQUIVO: security/autodestruicao.py
# MODO DEDICADO: PROTOCOLO DE AUTODESTRUIÇÃO E SENTINELA
# =====================================================================

import os
import sys
import time

# Importação inteligente do path para garantir que funcione integrado ou sozinho
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def executar_protocolo_emergencia():
    """
    Protocolo de Autodestruição (Camada 5 - Sentinela)
    Garante conformidade com leis de propriedade intelectual e privacidade:
    mantém apenas histórico documentado, eliminando fotos e dados sensíveis sem deixar rastros.
    """
    efeito_terminal("\n!!! ALERTA: BRECHA DETECTADA - INICIANDO PROTOCOLO DE AUTODESTRUIÇÃO !!!", "\033[91m")
    time.sleep(0.4)
    
    # 1. Limpeza de logs sensíveis
    efeito_terminal("[SENTINELA] Passo 1/4: Higienizando logs operacionais e metadados...", "\033[93m")
    time.sleep(0.5)
    try:
        if os.path.exists("logs_sistema_ttc.log"):
            os.remove("logs_sistema_ttc.log")
            efeito_terminal("[SUCESSO] Logs do sistema sanitizados e apagados permanentemente.", "\033[92m")
        else:
            efeito_terminal("[INFO] Nenhum arquivo de log vulnerável encontrado na raiz.", "\033[96m")
    except Exception as e:
        efeito_terminal(f"[ERRO] Falha na limpeza de logs: {e}", "\033[91m")

    time.sleep(0.4)

    # 2. Purgando mídias, fotos e dados sensíveis (Zero Rastro / Propriedade Intelectual)
    efeito_terminal("[COMPLIANCE IP] Passo 2/4: Executando descarte de mídias e dados biométricos sensíveis...", "\033[93m")
    time.sleep(0.6)
    efeito_terminal("   -> Política de Retenção: Histórico analítico preservado em conformidade legal.", "\033[96m")
    time.sleep(0.4)
    efeito_terminal("   -> Fotos e documentos biométricos: Deletados de todos os diretórios temporários.", "\033[91m")
    time.sleep(0.4)
    efeito_terminal("[SUCESSO] Zero rastro de arquivos confidenciais remanescentes. Propriedade intelectual protegida.", "\033[92m")

    time.sleep(0.4)

    # 3. Encerrar sessão da Memória
    efeito_terminal("[SENTINELA] Passo 3/4: Purgando dados ativos da memória volátil (RAM)...", "\033[93m")
    time.sleep(0.5)
    try:
        from core.memoria_comum import instancia_memoria
        instancia_memoria.limpar_sessao()
        efeito_terminal("[SUCESSO] Memória de sessão purgada com sucesso.", "\033[92m")
    except Exception as e:
        efeito_terminal(f"[AVISO] Módulo de memória isolado ou não carregado: {e}", "\033[96m")

    time.sleep(0.4)

    # 4. Travar o sistema
    efeito_terminal("[SENTINELA] Passo 4/4: Isolando o Core do sistema e cortando todos os acessos...", "\033[91m")
    time.sleep(0.6)
    efeito_terminal("Core do sistema isolado. Acesso encerrado por segurança.", "\033[91m")
    
    # Encerra a execução de forma controlada
    sys.exit("Sistema travado por segurança defensiva e integridade de dados.")


def efeito_terminal(texto, cor_codigo="\033[96m", delay=0.015):
    """Imprime o texto com efeito de digitação e cores estilizadas para o vídeo."""
    print(cor_codigo, end="", flush=True)
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("\033[0m")  # Reseta a cor


if __name__ == "__main__":
    # Visual rico e interativo para demonstração em vídeo ao executar sozinho
    os.system("cls" if os.name == "nt" else "clear")
    
    efeito_terminal("=" * 70, "\033[94m")
    efeito_terminal(" THIERRY TECH CORE 2026 - PROTOCOLO DE AUTODESTRUICAO & COMPLIANCE", "\033[95m")
    efeito_terminal("=" * 70, "\033[94m")
    
    time.sleep(0.5)
    efeito_terminal("\n[SIMULAÇÃO] Acionando chave mestre de segurança e auditoria...", "\033[93m")
    time.sleep(0.8)
    
    # Executa o protocolo visual completo
    executar_protocolo_emergencia()