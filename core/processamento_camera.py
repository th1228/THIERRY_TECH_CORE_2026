# main.py
import processamento_câmera as cam
import motor_dados as motor
import gerador_relatorio as relatorio

def rodar_sistema_completo():
    print("--- INICIANDO SISTEMA DE ENGENHARIA DA ALMA ---")
    
    # 1. Captura e Processamento (Abre a câmera, lê respiração e face)
    print("[1/2] Iniciando Scan...")
    dados_biometricos = cam.rodar_scanner() 
    
    # 2. Salva e Gera o Relatório
    print("[2/2] Gerando Relatório Dinâmico...")
    motor.salvar_dados(dados_biometricos)
    relatorio.gerar_pdf()
    
    print("--- SINCRONIA TOTAL CONCLUÍDA ---")

if __name__ == "__main__":
    rodar_sistema_completo()