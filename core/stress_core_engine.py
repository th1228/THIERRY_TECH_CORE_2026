
# --- PONTE DE MEMÓRIA AUTOMÁTICA (THIERRY TECH) ---
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:
        class MemoriaMock:
            def salvar_dados(self, chave, valor): pass
            def registrar(self, chave, valor): pass
            def ler_dados(self, chave): return None
        memoria = MemoriaMock()
# ---------------------------------------------------

import sys, os

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import aiohttp
import time

# Configuração do alvo
TARGET_URL = "http://localhost:8000" 

async def testar_servidor(session, user_id):
    start_time = time.perf_counter()
    try:
        async with session.get(TARGET_URL, timeout=5) as response:
            if response.status == 200:
                latency = (time.perf_counter() - start_time) * 1000
                return True, latency
            return False, 0
    except Exception:
        return False, 0

async def stress_test():
    chunk_size = 10000        # Mantemos um lote estável para não sobrecarregar
    total_requisicoes = 500000 # O volume total que você quer validar
    requisicoes_realizadas = 0
    
    print(f"Iniciando Teste de Estresse: {total_requisicoes} requisições.")
    
    async with aiohttp.ClientSession() as session:
        while requisicoes_realizadas < total_requisicoes:
            tasks = [testar_servidor(session, j) for j in range(chunk_size)]
            results = await asyncio.gather(*tasks)
            
            sucessos = sum(1 for r in results if r[0])
            latencia_media = sum(r[1] for r in results if r[0]) / (sucessos if sucessos > 0 else 1)
            
            requisicoes_realizadas += chunk_size
            output = f"Progresso: {requisicoes_realizadas}/{total_requisicoes} | Sucessos: {sucessos}/{chunk_size} | Latência Média: {latencia_media:.2f}ms"
            print(output)
            
            with open("stress_test_completo.log", "a") as f:
                f.write(output + "\n")
            
            # Pequena pausa para o sistema respirar entre os lotes
            await asyncio.sleep(0.5)
    
    print("Teste finalizado com sucesso.")

if __name__ == "__main__":
    asyncio.run(stress_test())