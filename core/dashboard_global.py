# -*- coding: utf-8 -*-
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def construir_pdf(dados):
    if not os.path.exists("LAUDOS"):
        os.makedirs("LAUDOS")
        
    caminho = os.path.join("LAUDOS", "Laudo_Final_TTC.pdf")
    pdf = canvas.Canvas(caminho, pagesize=A4)
    
    # Cabeçalho
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, 800, "RELATÓRIO DE CONSULTORIA DE ELITE - T.T.C.")
    
    # Informações com fonte reduzida (tamanho 8)
    pdf.setFont("Helvetica", 8) 
    y = 770
    
    for categoria, conteudo in dados.items():
        if categoria == "contexto_ambiental" and isinstance(conteudo, dict):
            # Quebra do Contexto Ambiental em duas linhas
            pdf.drawString(50, y, f"CONTEXTO AMBIENTAL: {conteudo.get('local')} | {conteudo.get('data')}")
            y -= 12
            pdf.drawString(50, y, f"CLIMA: Temp: {conteudo.get('temperatura')} | Cond: {conteudo.get('condicao')} | Umid: {conteudo.get('umidade')}")
        else:
            pdf.drawString(50, y, f"{categoria.upper()}: {conteudo}")
        
        y -= 15 
        
    pdf.save()
    os.startfile(caminho)