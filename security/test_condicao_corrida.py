# =====================================================================
# ARQUIVO: security/test_condicao_corrida.py
# Teste de Condição de Corrida (Carga Extrema: 200k operações)
# =====================================================================

import os
import sys
import time
import threading

# Garante a raiz do projeto no path do Python
raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if raiz_projeto not in sys.path:
    sys.path.append(raiz_projeto)

from security.log_seguro import LogSeguro

logger = LogSeguro()

# Recurso partilhado simulado
estado_compartilhado = {
    "contador_transacoes": 0,
    "lock_recurso": threading.Lock()
}

def rotina_atualizacao(id_thread: int, iteracoes: int):
    """Simula rotina pesada de concorrência com 200k ops no total."""
    for _ in range(iteracoes):
        with estado_compartilhado["lock_recurso"]:
            valor_atual = estado_compartilhado["contador_transacoes"]
            estado_compartilhado["contador_transacoes"] = valor_atual + 1

def executar_teste_corrida():
    print("\033[94m" + "=" * 65 + "\033[0m")
    print("\033[95m INICIANDO TESTE DE CONDIÇÃO DE CORRIDA (Carga Absoluta: 200k ops)\033[0m")
    print("\033[94m" + "=" * 65 + "\033[0m")
    
    # Reinicia o contador
    estado_compartilhado["contador_transacoes"] = 0
    
    # Parâmetros de estresse máximo
    num_threads = 100
    iteracoes_por_thread = 2000
    total_esperado = num_threads * iteracoes_por_thread

    threads = []
    
    inicio = time.time()
    
    # Dispara as 100 threads em simultâneo
    for i in range(num_threads):
        t = threading.Thread(target=rotina_atualizacao, args=(i, iteracoes_por_thread))
        threads.append(t)
        t.start()
        
    # Aguarda todas concluírem
    for t in threads:
        t.join()
        
    tempo_gasto = (time.time() - inicio) * 1000
    resultado_obtido = estado_compartilhado["contador_transacoes"]

    print(f"\n\033[96m[RESULTADOS DO TESTE DE CARGA ABSOLUTA (200K)]\033[0m")
    print(f" -> Operações Esperadas: \033[93m{total_esperado:,}\033[0m".replace(",", "."))
    print(f" -> Operações Registadas: \033[93m{resultado_obtido:,}\033[0m".replace(",", "."))
    print(f" -> Tempo de Execução: \033[93m{tempo_gasto:.2f} ms\033[0m")

    if resultado_obtido == total_esperado:
        logger.registrar("RACE_CONDITION_ULTIMATE", "SUCESSO", f"Sucesso absoluto em {total_esperado} operações concorrentes.")
        print("\n\033[92m[VEREDITO] Surpreendente! 200 mil operações processadas sem uma única falha de concorrência.\033[0m")
    else:
        logger.registrar("RACE_CONDITION_ULTIMATE", "ALERTA", f"Divergência sob 200k! Esperado: {total_esperado}, Obtido: {resultado_obtido}")
        print("\n\033[91m[VEREDITO] Atenção: Limite físico atingido ou perda de dados detetada.\033[0m")
    
    print("\033[94m" + "=" * 65 + "\033[0m")

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    executar_teste_corrida()