# -*- coding: utf-8 -*-
import sys
import os

# --- CORREÇÃO DE CAMINHO ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.memoria_comum import instancia_memoria as memoria

class MonacoNucleoAcesso:
    def __init__(self):
        print("[NÚCLEO_ACESSO] Motor de auditoria e acesso ativado.")

    def processar(self):
        """Busca o consolidado final do Integrador e realiza a auditoria."""
        print("[NÚCLEO_ACESSO] Consolidando resultados do sistema...")
        
        # O Núcleo Acesso agora busca o resultado final do Integrador
        dados = memoria.ler_dados("integrador")
        
        if dados:
            return self.integrar_resultados(dados)
        else:
            print("[NÚCLEO_ACESSO] Erro: Nenhum dado do Integrador disponível.")
            return False

    def integrar_resultados(self, dados):
        """Unificação, Auditoria e Registro Permanente."""
        try:
            # Caminho de log mantido conforme sua estrutura
            log_caminho = "storage/backup_auditoria.txt"
            os.makedirs(os.path.dirname(log_caminho), exist_ok=True)
            
            # Formatação do log
            acao = "Intervenção de Auditoria Concluída"
            with open(log_caminho, "a", encoding="utf-8") as f:
                f.write(f"Consolidação Realizada: {acao} | Fase: {dados.get('fase_protocolo', 'N/A')}\n")
            
            print(f"[NÚCLEO_ACESSO] Auditoria concluída. Registro salvo em {log_caminho}")
            return True
            
        except Exception as e:
            print(f"[NÚCLEO_ACESSO] Falha crítica na auditoria: {e}")
            return False

# Instância única
nucleo_acesso = MonacoNucleoAcesso()

def rodar():
    return nucleo_acesso.processar()

def iniciar():
    return rodar()