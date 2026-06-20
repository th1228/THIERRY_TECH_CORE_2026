# -*- coding: utf-8 -*-
import sys
import os

# --- PONTE DE BUSCA ---
# Isso garante que o Python procure os arquivos na pasta pai (raiz)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- IMPORTAÇÕES DIRETAS (Sem referências a pastas antigas) ---
from monaco_blindagem import MonacoBlindagem
from monaco_consciencia import MonacoConsciencia
from monaco_eminencia import MonacoEminencia
from monaco_integrador import MonacoIntegrador
from monaco_ressonancia import MonacoRessonancia

# --- LÓGICA DO GERADOR ---
class Generator:
    def __init__(self):
        print("Iniciando Mônaco Core 2026...")

    def run(self):
        try:
            print("Instanciando módulos...")
            blindagem = MonacoBlindagem("MONACO_GOLD_2026_SYSTEM")
            consciencia = MonacoConsciencia()
            eminencia = MonacoEminencia()
            integrador = MonacoIntegrador()
            ressonancia = MonacoRessonancia()
            
            print("Executando pipeline...")
            # Aqui você chama os métodos de processamento de cada um
            # Certifique-se de que cada classe tem o método .processar()
            blindagem.processar()
            consciencia.processar()
            eminencia.processar()
            integrador.processar()
            ressonancia.processar()
            
            print("Pipeline concluído com sucesso!")
            
        except Exception as e:
            print(f"Erro crítico no sistema: {e}")

if __name__ == "__main__":
    app = Generator()
    app.run()