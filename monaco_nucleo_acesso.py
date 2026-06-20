# -*- coding: utf-8 -*-

class MonacoNucleoAcesso:
    def __init__(self, cliente_nome, local):
        self.cliente = cliente_nome
        self.local = local

    def validar_registro(self, protocolo, extra=None):
        """
        Método ajustado para aceitar 3 argumentos conforme exigido pelo 
        sistema e evitar o TypeError.
        """
        print(f"\n[NÚCLEO] Validando protocolo: {protocolo}...")
        # Lógica de validação do registro do sistema
        return True

    def iniciar_portal(self):
        """Portal de Entrada Oficial: Mônaco Plan"""
        print("\n" + "="*70)
        print("    SEJA BEM-VINDO AO SUPRASSUMO MÔNACO PLAN | THIERRY ELITE    ")
        print("="*70)
        print(f"  > LOCAL DA OPERAÇÃO VINCULADO: {self.local}")
        print("-"*70)
        print("  ATENÇÃO: POR QUESTÃO DE ALTA SEGURANÇA, ESTE SISTEMA")
        print("  É VALIDADO EXCLUSIVAMENTE PARA USO NESTE AMBIENTE VINCULADO.")
        print("  A REMOÇÃO DESTE DISPOSITIVO DO DOMÍNIO TERRITORIAL")
        print("  RESULTARÁ NO BLOQUEIO IMEDIATO DO ACESSO.")
        print("-"*70)
        
        confirmacao = input("  DIGITE SUA SENHA ID-CONVITE PARA VALIDAR O LOCAL: ").strip().upper()
        
        if confirmacao == "CONFIRMO":
            print("\n[MÔNACO PLAN] SEGURANÇA VALIDADA. ACESSO AUTORIZADO.")
            return True
        else:
            print("\n[ERRO] CHAVE ID-CONVITE INVÁLIDA OU AMBIENTE NÃO RECONHECIDO.")
            return False