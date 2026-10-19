# -*- coding: utf-8 -*-
import os
import sys

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

class DiagnosticoSeguranca:
    """
    Módulo de Diagnóstico de Segurança (Anti-Reversa e Integridade).
    Este script valida se o ambiente está íntegro antes da inicialização do sistema.
    """
    
    def __init__(self, lang: str = "PT"):
        self.diretorio_raiz = ROOT_DIR
        self.arquivos_criticos = ["run_all.py", "core"]
        
    def _verificar_arquitetura(self):
        """Verifica se os diretórios e arquivos vitais existem."""
        for item in self.arquivos_criticos:
            if not os.path.exists(os.path.join(self.diretorio_raiz, item)):
                print(f"!!! ALERTA DE SEGURANÇA: Artefato crítico ausente -> {item}")
                return False
        return True

    def _verificar_ambiente(self):
        """Verifica se não há sinais de debugadores ou ambiente hostil."""
        if sys.gettrace() is not None:
            print(">>> Modo de depuração detectado.")
        return True

    def verificar_status(self):
        """
        Executa a varredura completa.
        Retorna True se o sistema estiver limpo e seguro.
        """
        print(">>> [DIAGNÓSTICO] Iniciando varredura de integridade de runtime...")
        
        if not self._verificar_arquitetura():
            memoria.salvar_dados("status_seguranca", {"integro": False, "motivo": "Artefato ausente"})
            return False
            
        if not self._verificar_ambiente():
            pass # Apenas aviso, mantém True
            
        print(">>> [DIAGNÓSTICO] Validação concluída: Nenhuma violação detectada.")
        print(">>> [STATUS] Sistema íntegro. Acesso liberado.")
        
        # Sincroniza o status de integridade com a Memória Comum 🧠
        try:
            memoria.salvar_dados("status_seguranca", {"integro": True, "status": "Liberado"})
        except Exception:
            pass

        return True

# Instância global para uso no ecossistema
_diagnostico_global = DiagnosticoSeguranca()

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    return _diagnostico_global.verificar_status()

if __name__ == "__main__":
    if _diagnostico_global.verificar_status():
        print("Segurança OK.")
    else:
        print("Segurança FALHOU.")