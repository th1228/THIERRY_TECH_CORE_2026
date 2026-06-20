# -*- coding: utf-8 -*-
from datetime import datetime
import sensor_fadiga  # Seu motor de leitura
import biogenio_engine # Seu motor visual e de máscara
import pywhatkit as kit
import cv2

def fluxo_operacional_completo():
    # 1. Abre a câmera com a interface do BioGênio (já com a máscara e diagnóstico)
    print("Iniciando BioGênio Digital...")
    dados_sensor = biogenio_engine.rodar_biogenio_digital()
    
    if not dados_sensor:
        print("Operação cancelada ou sem leitura.")
        return

    # 2. Gera o laudo baseado nos dados capturados
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    laudo = (
        f"LAUDO TTC GLOBAL: TG\n"
        f"Data/Hora: {agora}\n"
        f"Fadiga Neural detectada: {dados_sensor[0]}\n"
        f"Densidade dérmica: {dados_sensor[2]}\n"
        f"--- MENSAGEM DO BIO-GÊNIO ---\n"
        f"Sua BioArquitetura está sendo otimizada. Siga o protocolo recomendado."
    )
    
    # 3. Pergunta de Envio
    print("\n--- LAUDO GERADO ---")
    print(laudo)
    escolha = input("\nDeseja enviar este laudo para um cliente? (s/n): ")
    
    if escolha.lower() == 's':
        telefone = input("Digite o número com DDD (ex: +5598999999999): ")
        try:
            # Envia daqui a 2 minutos para garantir que o navegador abra
            kit.sendwhatmsg_instantly(telefone, laudo, wait_time=15)
            print(f"Mensagem disparada para {telefone}!")
        except Exception as e:
            print(f"Falha no envio: {e}")
    else:
        print("Envio cancelado. Laudo salvo apenas localmente.")

if __name__ == "__main__":
    fluxo_operacional_completo()