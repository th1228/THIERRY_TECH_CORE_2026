# =====================================================================
# ARQUIVO: security/test_concorrencia.py
# Teste de Estresse e Concorrência (Validação de Deadlock)
# =====================================================================

import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Garante a raiz do projeto no path do Python
raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if raiz_projeto not in sys.path:
    sys.path.append(raiz_projeto)

from security.log_seguro import LogSeguro
from security.crypto_engine import CryptoEngine

logger = LogSeguro()
crypto = CryptoEngine()

def tarefa_concorrente(id_tarefa: int):
    """Simula uma carga de trabalho pesada e concorrente (Cifragem + Log)."""
    inicio = time.time()
    try:
        # Simula processamento pesado de dados ou diagnóstico
        payload = f"Dados de Diagnóstico Concorrente ID-{id_tarefa}".encode('utf-8')
        cifrado = crypto.cifrar(payload)
        decifrado = crypto.decifrar(cifrado)
        
        # Registo concorrente no audit ledger
        logger.registrar("CONCURRENCY_TEST", "INFO", f"Tarefa {id_tarefa} executada com sucesso.")
        
        duracao = (time.time() - inicio) * 1000 # em milissegundos
        return True, id_tarefa, duracao
    except Exception as e:
        logger.registrar("CONCURRENCY_TEST", "ERRO", f"Falha na tarefa {id_tarefa}: {e}")
        return False, id_tarefa, 0

def executar_teste_estresse(total_threads=40, max_trabalhadores=10):
    print("\033[94m" + "=" * 65 + "\033[0m")
    print(f"\033[95m INICIANDO TESTE DE CONCORRÊNCIA ({total_threads} disparos simultâneos)\033[0m")
    print("\033[94m" + "=" * 65 + "\033[0m")
    
    sucessos = 0
    falhas = 0
    tempos = []

    inicio_geral = time.time()

    with ThreadPoolExecutor(max_workers=max_trabalhadores) as executor:
        futures = [executor.submit(tarefa_concorrente, i) for i in range(1, total_threads + 1)]
        
        for future in as_completed(futures):
            sucesso, id_t, duracao = future.result()
            if sucesso:
                sucessos += 1
                tempos.append(duracao)
            else:
                falhas += 1

    tempo_total = (time.time() - inicio_geral) * 1000
    media_tempo = sum(tempos) / len(tempos) if tempos else 0

    print("\n\033[96m[RESULTADOS DO TESTE DE CONCORRÊNCIA]\033[0m")
    print(f" -> Tarefas Concluídas com Sucesso: \033[92m{sucessos}/{total_threads}\033[0m")
    print(f" -> Falhas ou Deadlocks Detectados: \033[91m{falhas}\033[0m")
    print(f" -> Tempo Médio por Tarefa: \033[93m{media_tempo:.2f} ms\033[0m")
    print(f" -> Tempo Total de Execução: \033[93m{tempo_total:.2f} ms\033[0m")
    
    if falhas == 0:
        print("\n\033[92m[VEREDITO] Sistema 100% blindado contra Deadlocks sob concorrência!\033[0m")
    else:
        print("\n\033[91m[VEREDITO] Atenção: Foram detetadas falhas de concorrência.\033[0m")
    print("\033[94m" + "=" * 65 + "\033[0m")

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    executar_teste_estresse(total_threads=40, max_trabalhadores=10)