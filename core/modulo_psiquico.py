# -*- coding: utf-8 -*-
import cv2
import mediapipe as mp
import os

def capturar_e_analisar():
    """Abre a câmera, captura uma foto e gera o laudo psíquico imediatamente."""
    cap = cv2.VideoCapture(0) # Abre a webcam padrão
    print("Posicione-se para a leitura psíquica... [Pressione ESPAÇO para capturar]")
    
    while True:
        ret, frame = cap.read()
        cv2.imshow('Captura Psiquica', frame)
        if cv2.waitKey(1) & 0xFF == ord(' '): # Espaço captura
            cv2.imwrite("foto_diaria.jpg", frame)
            break
            
    cap.release()
    cv2.destroyAllWindows()
    
    # Processa a foto recém capturada
    processar_analise("foto_diaria.jpg")

def processar_analise(caminho_foto):
    # Aqui entra o seu motor de MediaPipe que já discutimos
    # Após gerar os resultados, salva no arquivo:
    with open("laudo_psiquico.txt", "w", encoding="utf-8") as f:
        f.write("Temperamento: Colérico (Alta Predisposição ao Comando)\n")
        f.write("Lado: Direito\n")
        f.write("Emocional: Estável\n")
    print("Laudo gerado com sucesso em 'laudo_psiquico.txt'")

if __name__ == "__main__":
    capturar_e_analisar()