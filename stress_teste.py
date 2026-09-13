import time
import sys
import os

# Adiciona o diretório atual ao path para garantir que o Python encontre os módulos
sys.path.append(os.getcwd())

from security.Ratelimiting import RateLimiting

def simular_ataque():
    print("--- INICIANDO TESTE DE ESTRESSE: RATE LIMITER ---")
    print("Regra: 5 requisições permitidas por janela.\n")
    
    for i in range(1, 11):
        try:
            # Tenta realizar a requisição usando o método estático do seu RateLimiting
            RateLimiting.verificar_vazao(identificador="teste_ataque")
            print(f"Requisição {i}: PERMITIDA ✅")
        except Exception as e:
            print(f"Requisição {i}: BLOQUEADA PELO RATE LIMITER ❌ ({e})")
        
        # Intervalo curto entre as requisições para estourar o limite
        time.sleep(0.1)

    print("\n--- TESTE FINALIZADO ---")

if __name__ == "__main__":
    simular_ataque()