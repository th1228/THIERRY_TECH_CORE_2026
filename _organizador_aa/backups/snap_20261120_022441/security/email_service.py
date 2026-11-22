# -*- coding: utf-8 -*-
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

def secure_delivery(email, nome_cliente, arquivo_json_path, perfil_ativo):
    try:
        with open(arquivo_json_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        nome_pdf = f"Dossie_TTC_{nome_cliente.replace(' ', '_')}.pdf"
        c = canvas.Canvas(nome_pdf, pagesize=A4)
        largura, altura = A4

        # 1. EFEITO DE CÉDULA (Borda de Luxo)
        # Se você tiver uma imagem de borda, substitua o caminho abaixo:
        # c.drawImage("borda_dinheiro.png", 0, 0, width=largura, height=altura)
        
        # Como não tenho a imagem, vou desenhar uma borda "guilhochê" estilizada
        c.setStrokeColor(colors.gold)
        c.setLineWidth(15)
        c.rect(20, 20, largura-40, altura-40) # Moldura Dourada

        # 2. CABEÇALHO COM ESTILO
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.navy)
        c.drawCentredString(largura/2, altura - 70, "THIERRY TECHNOLOGY")
        c.setFont("Helvetica", 14)
        c.drawCentredString(largura/2, altura - 90, "CERTIFICADO DE AUTENTICIDADE E DIAGNÓSTICO")

        # 3. TABELA DE DADOS (Organização Premium)
        # Aqui organizamos o que vem do JSON em colunas bonitas
        data = [
            ["MÓDULO", "ANÁLISE DETALHADA"],
            ["Biometria/Áurea", "Análise de proporções e harmonia facial."],
            ["Forense/Osteo", "Estrutura óssea e densidade tricologia."],
            ["Visagismo", "Perfil comportamental sensorial."]
        ]
        
        # SE FOR PREMIUM, ADICIONA A REGENERAÇÃO NA TABELA
        if perfil_ativo == "plano_premium":
            data.append(["CLÍNICA (MÔNACO)", "Protocolo de Exossomos e Regeneração Celular Ativado."])

        tabela = Table(data, colWidths=[150, 300])
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.gold),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.cyan),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]))
        
        tabela.wrapOn(c, 100, 500)
        tabela.drawOn(c, 60, altura - 300)

        # 4. RODAPÉ DE VALOR
        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(largura/2, 60, "DOCUMENTO OFICIAL THIERRY TECHNOLOGY CONCEPT GLOBAL")

        c.save()
        return {"sucesso": True, "mensagem": "PDF Gerado com sucesso."}

    except Exception as e:
        return {"sucesso": False, "mensagem": str(e)}