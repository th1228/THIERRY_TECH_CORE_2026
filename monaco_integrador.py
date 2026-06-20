# -*- coding: utf-8 -*-
from monaco_nucleo_acesso import MonacoNucleoAcesso

class MonacoIntegrador:
    def __init__(self):
        # Inicializa sem os dados, vamos pedir depois
        self.cliente = {}

    def solicitar_dados_cliente(self):
        print("\n" + "="*50)
        print("    INICIALIZAÇÃO DO SISTEMA MÔNACO | TTC GLOBAL    ")
        print("="*50)
        self.cliente['nome'] = input("NOME DO CLIENTE: ")
        self.cliente['idade'] = input("IDADE: ")
        self.cliente['documento'] = input("CPF/CNPJ: ")
        self.cliente['local'] = input("ENDEREÇO/LOCAL: ")
        
        # Cria o Núcleo com os dados coletados
        self.nucleo = MonacoNucleoAcesso(self.cliente['nome'], self.cliente['local'])
        print("\n[INTEGRADOR] Dados registrados com sucesso.")

    def executar_sistema(self):
        # 1. Coleta os dados primeiro
        self.solicitar_dados_cliente()
        
        # 2. Chama o Portal (O Núcleo de Acesso)
        if not self.nucleo.iniciar_portal():
            print("\n[ERRO] Integração abortada pelo Núcleo de Segurança.")
            return

        # 3. Se validado, aqui é onde chamaremos os outros módulos amanhã
        print("\n" + "*"*50)
        print(f"  ACESSO CONCEDIDO: {self.cliente['nome'].upper()}")
        print("  INICIALIZANDO MÓDULOS DE BIOMETRIA E PDF...")
        print("*"*50)
        print("[SUCESSO] Sistema pronto para processar dados de elite.")

# Para rodar direto neste arquivo:
if __name__ == "__main__":
    integrador = MonacoIntegrador()
    integrador.executar_sistema()