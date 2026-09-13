# -*- coding: utf-8 -*-
import sys
import os

# --- CORREÇÃO DE CAMINHO ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.memoria_comum import instancia_memoria as memoria

class MonacoComunicacao:
    def __init__(self):
        print("[COMUNICAÇÃO] Canal de transmissão de dados ativado.")

    def processar(self):
        """Busca o consolidado na memória e transmite."""
        print("[COMUNICAÇÃO] Consolidando dados do ecossistema...")
        
        # Lê o que foi gravado pelos outros módulos
        dados_ambiente = memoria.ler_dados("ambiente")
        dados_biometria = memoria.ler_dados("biometria")
        
        # Simula o envio do pacote final
        pacote_final = {
            "ambiente": dados_ambiente,
            "biometria": dados_biometria,
            "status": "Transmissão Concluída"
        }
        
        return self.transmitir(pacote_final)

    def transmitir(self, pacote):
        # Aqui você pode expandir para enviar via API, salvar em arquivo, etc.
        print(f"[COMUNICAÇÃO] Protocolo enviado: {pacote.get('status')}")
        return True

# Instância global
comunicador = MonacoComunicacao()

def rodar():
    """Função chamada pelo painel principal."""
    return comunicador.processar()

def iniciar():
    """Ponte padronizada."""
    return rodar()

if __name__ == "__main__":
    print(rodar())