# -*- coding: utf-8 -*-
from monaco_nucleo_acesso import MonacoNucleoAcesso
from monaco_integrador import MonacoIntegrador

class MonacoPlan:
    def __init__(self, cliente, local):
        # 1. Instancia o Núcleo de Acesso (Segurança)
        self.nucleo = MonacoNucleoAcesso(cliente, local)
        # 2. Instancia o Motor (Processamento Core)
        self.motor = MonacoIntegrador()
        self.cliente = cliente

    def rodar_protocolo_completo(self):
        """O fluxo definitivo: Segurança -> Processamento -> Laudo."""
        
        # A. Validação de Elite (Portal)
        if not self.nucleo.iniciar_portal():
            print("[ERRO] Falha de segurança. Acesso negado.")
            return

        # B. Execução do Motor de Biometria
        print(f"\n[MÔNACO PLAN] Executando motores de alta performance para {self.cliente}...")
        dados_processados = self.motor.rodar_loop_real()
        
        # C. Síntese do Laudo Final (PDF Exclusivo)
        print("[MÔNACO PLAN] Gerando Laudo Definitivo...")
        self.emitir_pdf_monaco(dados_processados)
        print("[MÔNACO PLAN] Protocolo concluído com sucesso.")

    def emitir_pdf_monaco(self, dados):
        """Gera o laudo com a identidade visual soberana."""
        # Aqui você insere a lógica de exportação (ReportLab)
        print(f"--- [PDF] Laudo emitido para {self.cliente} ---")

if __name__ == "__main__":
    # Início da ignição oficial do sistema
    sistema = MonacoPlan(cliente="Thierry Elite", local="Unidade 01")
    sistema.rodar_protocolo_completo()