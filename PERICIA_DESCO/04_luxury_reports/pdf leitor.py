import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def capturar_foto_webcam(nome_arquivo="foto_cliente.jpg"):
    # Remove arquivo anterior se existir para evitar confusão
    if os.path.exists(nome_arquivo):
        os.remove(nome_arquivo)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a câmera.")
        return False
        
    print("\n--- SISTEMA DE CAPTURA INICIADO ---")
    print("Pressione 's' para SALVAR a foto | 'k' para FECHAR e gerar o laudo")
    
    foto_salva = False
    while True:
        ret, frame = cap.read()
        if not ret: break
            
        cv2.imshow('Scanner - Pressione S(salvar) ou K(sair)', frame)
        
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord('s'):
            cv2.imwrite(nome_arquivo, frame)
            print(f"[*] FOTO SALVA: {nome_arquivo}")
            foto_salva = True
        elif tecla == ord('k'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return foto_salva

def criar_relatorio_thierry(foto_path="foto_cliente.jpg"):
    filename = "Certificacao_Craniometrica_Bioidentica.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos
    style_header = ParagraphStyle('Header', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#555555'))
    style_titulo = ParagraphStyle('Titulo', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.black, spaceAfter=15)
    style_secao = ParagraphStyle('Secao', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, spaceBefore=15, spaceAfter=8)
    
    story.append(Paragraph("THIERRY TECHNOLOGY CONCEPT GLOBAL", style_header))
    story.append(Paragraph("CERTIFICAÇÃO CRANIOMÉTRICA BIOIDÊNTICA", style_titulo))
    
    # Inserção Condicional
    if os.path.exists(foto_path):
        story.append(Paragraph("<b>Registro Fotográfico Capturado:</b>", style_secao))
        img = Image(foto_path, width=4*inch, height=3*inch)
        story.append(img)
        story.append(Spacer(1, 15))
    else:
        story.append(Paragraph("<i>Aviso: Nenhuma imagem foi capturada.</i>", style_header))

    story.append(Paragraph("1. Leituras Craniométricas Forenses", style_secao))
    
    dados_cranio = [
        ["Parâmetro Estrutural Ósseo", "Valor Metric Forense Obtido"],
        ["Ângulo Goníaco Esquerdo", "123.1 Grad"],
        ["Ângulo Goníaco Direito", "124.6 Grad"],
        ["Predisposição a Paralisia Facial", "Moderada"]
    ]
    
    t1 = Table(dados_cranio, colWidths=[3.8*inch, 3.2*inch])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E0E0E0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDBDBD')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t1)

    doc.build(story)
    print(f"\n[!] SUCESSO: Relatório gerado: {filename}")

if __name__ == "__main__":
    if capturar_foto_webcam():
        criar_relatorio_thierry("foto_cliente.jpg")
    else:
        print("[-] Operação cancelada ou falha na captura.")