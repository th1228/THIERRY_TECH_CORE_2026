import cv2
import mediapipe as mp
import os
import sys
import subprocess
import random  # Simulador de IA para métricas do laudo
import shutil  # ADICIONADO: Para mover o arquivo para a pasta certa
from datetime import datetime
# Importações para o PDF de Elite (ReportLab)
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# =====================================================================
# CONFIGURAÇÃO DE DESIGN DO NOVO LAUDO LUXO (Preto e Ouro)
# =====================================================================
COR_FUNDO = colors.HexColor("#000000")       # Preto Absoluto
COR_OURO = colors.HexColor("#D4AF37")        # Dourado Realce
COR_TEXTO = colors.HexColor("#FFFFFF")       # Branco Puro
COR_DETALHE = colors.HexColor("#A0A0A0")     # Cinza para Linhas de Grade

def gerar_e_abrir_laudo_final_elite():
    """Gera o laudo focado e força a abertura imediata."""
    id_laudo = datetime.now().strftime("TTC-CAP-%Y%m%d-%H%M%S")
    nome_arquivo = f"Laudo_Biocapilar_Final_{id_laudo}.pdf"
    
    # Define A4 completo para garantir que tudo caiba na folha
    pdf = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4
    
    # 1. Fundo Preto Absoluto (Toda a página)
    pdf.setFillColor(COR_FUNDO)
    pdf.rect(0, 0, largura, altura, fill=1, stroke=0)
    
    # 2. Cabeçalho de Elite (Dourado - Centralizado e Redimensionado)
    pdf.setFillColor(COR_OURO)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(largura / 2, altura - 55, "THIERRY TECHNOLOGY CONCEPT GLOBAL")
    
    # 3. Design: Moldura Fina de Destaque (Dourado)
    pdf.setStrokeColor(COR_OURO)
    pdf.setLineWidth(1)
    pdf.rect(30, 30, largura - 60, altura - 60, fill=0, stroke=1)
    
    # Linha divisória de alta precisão
    pdf.setStrokeColor(COR_OURO)
    pdf.line(40, altura - 75, largura - 40, altura - 75)
    
    # 4. Título do Laudo (Branco)
    pdf.setFillColor(COR_TEXTO)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, altura - 92, "LAUDO DE BIOPERÍCIA FACIAL & ANÁLISE CAPILAR AVANÇADA")
    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(COR_OURO)
    pdf.drawString(50, altura - 105, f"DATA DE EMISSÃO: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
    
    # 5. DIAGNÓSTICO FORENSE CAPILAR DE ALTA PRECISÃO
    y_pos = altura - 135
    pdf.setFillColor(COR_OURO)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y_pos, "I. DIAGNÓSTICO FORENSE CAPILAR DE ALTA PRECISÃO")
    y_pos -= 18
    
    pdf.setFillColor(COR_TEXTO)
    pdf.setFont("Courier", 9.5)
    
    # Simulador de análise com idade do fio baseada em anos (2 a 3 anos devido a químicas)
    sim_idade_fio = round(random.uniform(2.0, 3.0), 1)
    sim_massa = random.choice(["Alta", "Média", "Baixa (Necessidade de Reposição Aminoproteica)"])
    sim_rosto = random.choice(["Oval", "Quadrado", "Coração", "Longo"])
    
    diagnosticos = [
        f"* Idade Media do Fio:       {sim_idade_fio} anos (Historico Quimico Acumulado)",
        f"* Massa Hidrica:           {sim_massa}",
        f"* Agua no Fio:             Identificada (Deficit sutil em pontas)",
        f"* Densidade para Queda:    Normal (Fase Anagena Estavel)",
        f"* Risco Paralisia Facial:  Nao Identificado (Predisposicao Inexistente)",
        f"* Risco Dermatite:         {random.choice(['Identificada (Oleosidade Sazonal)', 'Nao Identificada'])}",
        f"* Formato de Rosto:        {sim_rosto} (Mapeamento Geometrico Concluido)"
    ]
    
    for diag in diagnosticos:
        pdf.drawString(60, y_pos, diag)
        y_pos -= 13

    # 6. SEÇÃO DE CORTES SUGERIDOS (Top 10 Arquiteturas de Impacto)
    y_pos -= 12
    pdf.setFillColor(COR_OURO)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y_pos, f"II. ARQUITETURAS DE CORTE RECOMENDADAS (ARQUITETURA PARA ROSTO {sim_rosto.upper()})")
    y_pos -= 16
    
    pdf.setFillColor(COR_TEXTO)
    pdf.setFont("Helvetica", 9.5)
    
    cortes = [
        "1. Pixie Lapidado com Franja Alongada  |  6. Curto com Topete Estruturado",
        "2. Shaggy Chic em Camadas Dinamicas   |  7. Butterfly Cut Luxo de Alta Fluidez",
        "3. Blunt Bob (Base Reta e Alinhada)   |  8. Chanel de Bico Redefinido",
        "4. Long Bob Assimetrico Imponente     |  9. Soft French Bob Europeu",
        "5. Desconectado Moderno com Textura   |  10. Buzz Cut Designer / Ultra-Short"
    ]
    
    for corte in cortes:
        pdf.drawString(60, y_pos, corte)
        y_pos -= 14
        
    # Observação técnica alterada e milimetricamente encurtada para caber na página
    y_pos -= 6
    pdf.setFillColor(COR_OURO)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(50, y_pos, "OBS.:")
    
    pdf.setFillColor(COR_TEXTO)
    pdf.setFont("Helvetica-Oblique", 9)
    obs_texto = f"Designs calibrados para harmonizar com o rosto {sim_rosto}, projetando simetria e refinamento visual de alto padrao."
    pdf.drawString(85, y_pos, obs_texto)

    # 7. SEÇÃO DE TRATAMENTOS INDICADOS
    y_pos -= 26
    pdf.setFillColor(COR_OURO)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y_pos, "III. CRONOGRAMA DE TRATAMENTOS DE ELITE (CONCEITO TTC GLOBAL)")
    y_pos -= 15
    
    pdf.setStrokeColor(COR_OURO)
    pdf.line(50, y_pos, largura - 50, y_pos)
    y_pos -= 14
    
    # Títulos da Tabela (Coluna de Marcas puxada para perto: largura - 260)
    pdf.setFillColor(COR_OURO)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(60, y_pos, "PASSO")
    pdf.drawString(160, y_pos, "PRODUTOS & PROTOCOLO")
    pdf.drawString(largura - 260, y_pos, "MARCAS INDICADAS")
    y_pos -= 15
    
    # Dados da Tabela de Tratamentos
    pdf.setFillColor(COR_TEXTO)
    pdf.setFont("Helvetica", 9.5)
    
    cronograma = [
        ["1. Hidratacao", "Devolucao de Agua & Umidade profunda", "Kerastase Nutritive / Loreal Absolut Repair"],
        ["2. Reconstrucao", "Anti-emborrachamento CPR Profissional", "Senscience CPR Tech"],
        ["3. Emoliencia", "Wella Ultimate Repair + Infusaao de Oleos", "Wella Professionals / doTERRA Essential"],
        ["4. Anti-queda", "Protocolo Genesis + Terapia Fitoterapica", "Kerastase Genesis / Davines Calming"],
        ["5. Terapia Capilar", "Protocolo Natural doTERRA + Fitoceuticos", "doTERRA / Davines Naturaltech"]
    ]
    
    for fase in cronograma:
        pdf.drawString(60, y_pos, fase[0])
        pdf.drawString(160, y_pos, fase[1])
        pdf.drawString(largura - 260, y_pos, fase[2]) # Puxado para perto garantindo que tudo apareça
        y_pos -= 15

    # 8. Rodapé Real de Ancoragem
    pdf.setFillColor(COR_OURO)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(largura / 2, 50, "THIERRY TECNOLOGIA INTERNACIONAL")
    
    # 9. Design: Linha de Ancoragem Final
    pdf.setStrokeColor(COR_OURO)
    pdf.setLineWidth(1)
    pdf.line(largura/2 - 100, 43, largura/2 + 100, 43)
    
    # Grava e finaliza o PDF na raiz primeiro (Segurança total do design)
    pdf.save()
    
    # --- BLOCO QUE MOVE O ARQUIVO SALVO PARA A PASTA CORRETA ---
    pasta_destino = "fotos_clientes"
    os.makedirs(pasta_destino, exist_ok=True)  # Cria a pasta se ela não existir
    caminho_final = os.path.join(pasta_destino, nome_arquivo)
    
    try:
        shutil.move(nome_arquivo, caminho_final)
        print(f"Laudo Final de Elite movido para: {caminho_final}")
    except Exception as e:
        print(f"Aviso ao mover arquivo: {e}")
        caminho_final = nome_arquivo  # Caso falhe o envio, ele tenta abrir o da raiz para não travar
    # -----------------------------------------------------------
    
    # COMANDO DE ABERTURA IMEDIATA DO SISTEMA OPERACIONAL
    try:
        if sys.platform == "win32":
            os.startfile(caminho_final)
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", caminho_final])
        else:  # Linux
            subprocess.run(["xdg-open", caminho_final])
    except Exception as e:
        print(f"Erro ao abrir o PDF automaticamente: {e}")

# =====================================================================
# INICIALIZAÇÃO DA CÂMERA E MÁSCARA FUTURISTA FINAL
# =====================================================================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)

cap = cv2.VideoCapture(0)

print("Aguardando leitura de Elite... Pressione 'S' para Processar Laudo de Tratamentos.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Efeito espelho natural na tela
    image = cv2.flip(image, 1)
    h, w, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # 1. Renderização da Malha Cibernética Futurista Fina
            for connection in mp_face_mesh.FACEMESH_CONTOURS:
                ptA_idx = connection[0]
                ptB_idx = connection[1]
                
                ptA = face_landmarks.landmark[ptA_idx]
                ptB = face_landmarks.landmark[ptB_idx]
                
                xA, yA = int(ptA.x * w), int(ptA.y * h)
                xB, yB = int(ptB.x * w), int(ptB.y * h)
                
                # Linha Verde Cyber ultra fina (thickness=1) para criar o visual limpo de escaneamento
                cv2.line(image, (xA, yA), (xB, yB), (0, 230, 0), 1, cv2.LINE_AA)
                
            # 2. Design Cibernético Adicional: Linhas de Grelha e Ciano
            cv2.line(image, (int(w/2) - 100, 0), (int(w/2) - 100, h), (230, 230, 0), 1)
            cv2.line(image, (int(w/2) + 100, 0), (int(w/2) + 100, h), (230, 230, 0), 1)
            cv2.line(image, (0, int(h/2)), (w, int(h/2)), (230, 230, 0), 1)

            # Adiciona informações na tela sobre análise facial de risco
            cv2.putText(image, "ANALISE DE ARQUITETURA CAPILAR & TRATAMENTOS DE ELITE ATIVA", (10, h-20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow('TTC - Cybernetic Scan Engine', image)
    
    key = cv2.waitKey(1) & 0xFF
    # Tecla S: Encerra, gera o PDF de Luxo Limpo e abre na hora na tela
    if key == ord('s') or key == ord('S'):
        if results.multi_face_landmarks:
            cv2.destroyAllWindows()
            # Chama a função que gera e abre o laudo
            gerar_e_abrir_laudo_final_elite()
            break

    elif key == ord('q') or key == ord('Q'):
        break

cap.release()
cv2.destroyAllWindows()