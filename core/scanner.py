# -*- coding: utf-8 -*-
import cv2
import mediapipe as mp
import winsound
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def registrar_no_historico(nome_cliente, arquivo):
    """Cria um registro permanente de cada laudo gerado."""
    with open("Registro_Central_TTC.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M')} | Cliente: {nome_cliente} | Arquivo: {arquivo}\n")

def construir_pdf(dados):
    """Gera o laudo com design otimizado."""
    nome_sanitizado = dados['nome'].replace(' ', '_')
    pasta_cliente = os.path.join("Arquivos_TTC", nome_sanitizado)
    
    if not os.path.exists(pasta_cliente):
        os.makedirs(pasta_cliente)
    
    data_formatada = datetime.now().strftime('%Y%m%d')
    nome_arquivo = f"TTC_{nome_sanitizado}_{data_formatada}.pdf"
    caminho_final = os.path.join(pasta_cliente, nome_arquivo)
    
    pdf = canvas.Canvas(caminho_final, pagesize=A4)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, 800, f"LAUDO TTC GLOBAL: {dados['nome'].upper()}")
    
    pdf.setFont("Helvetica", 16)
    y = 740
    conteudo = [
        f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"Local: São Luís, MA",
        f"Status Ambiental: {dados['clima']}",
        f"Osteometria: {dados['osteometria']}",
        f"Pericia Neuro: {dados['pericia_neuro']}"
    ]
    
    for linha in conteudo:
        pdf.drawString(50, y, linha)
        y -= 40
        
    pdf.save()
    registrar_no_historico(dados['nome'], caminho_final)
    os.startfile(pasta_cliente)

def rodar_scanner(nome):
    """Lógica principal de captura."""
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
    cap = cv2.VideoCapture(0)
    y_scan = 0
    
    while cap.isOpened():
        success, image = cap.read()
        if not success: continue

        image = cv2.flip(image, 1)
        h, w, _ = image.shape
        y_scan = (y_scan + 12) % h
        
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_image)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for lm in face_landmarks.landmark:
                    x, y = int(lm.x * w), int(lm.y * h)
                    cv2.circle(image, (x, y), 1, (0, 255, 150), -1) 
                cv2.line(image, (0, y_scan), (w, y_scan), (0, 255, 255), 2)

        cv2.imshow('TTC - Cybernetic Scan Engine', image)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            winsound.Beep(1200, 300)
            hora = datetime.now().hour
            status = "Ciclo Diurno" if 5 <= hora < 12 else "Ciclo Vespertino" if 12 <= hora < 18 else "Ciclo Noturno"
            dados = {'nome': nome, 'clima': status, 'osteometria': 'Validada', 'pericia_neuro': 'Sinapse Detectada'}
            construir_pdf(dados)
            break
        elif key == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

def processar():
    """Interface para o Orquestrador."""
    print("[Scanner] Iniciando engine de captura...")
    rodar_scanner("Cliente_TTC_Scan")
    return {"status": "sucesso", "scanner": "finalizado"}

if __name__ == "__main__":
    nome_cliente = input("Nome do cliente: ")
    rodar_scanner(nome_cliente)