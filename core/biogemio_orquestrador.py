# -*- coding: utf-8 -*-
import os
import cv2
import math
import time
import pyttsx3
import threading
import numpy as np
import mediapipe as mp
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
from flask import Flask, Response, render_template_string, jsonify, request
import logging

# Silencia os logs de requisição do Werkzeug para manter o terminal limpo
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

try:
    from core.script_clima import obter_dados as obter_clima_atual # type: ignore
except ImportError:
    try:
        from script_clima import obter_dados as obter_clima_atual # type: ignore
    except ImportError:
        def obter_clima_atual():
            return {
                "status": "sucesso",
                "clima_agora": "27.1°C – Algumas nuvens",
                "regiao": "São Luís, BR",
                "qualidade_ar": "Bom (1 AQI)",
                "material_particulado_pm25": "2.5 µg/m³"
            }

def emitir_voz_sincronizada():
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 145) 
        engine.say("Varredura osteométrica facial e auditoria UHNWI inicializadas.")
        engine.runAndWait()
    except:
        pass

class BiogemEngine:
    def __init__(self, tipo_relatorio="monaco", nome_cliente="FORBES 400 / CLIENTE VIP", transaction_id="TX-9082-MONACO"):
        self.tipo_relatorio = tipo_relatorio
        self.nome_cliente = nome_cliente
        self.transaction_id = transaction_id
        
        self.app = Flask(__name__)
        self.frame_atual = None
        self.lock = threading.Lock()
        
        # Estados do fluxo
        self.captura_realizada = False
        self.disparar_leitura = False
        self.solicitar_captura_manual = False
        self.status_hud_web = "AGUARDANDO POSICIONAMENTO & CAPTURA..."
        self.fase_atual = "CAPTURA_LIMPA" 
        
        # Perfis Executivos UHNWI com Termos de Alta Precisão e Gestão de Riscos
        self.banco_perfis = {
            1: {
                "nome": "FORBES 400 / HIGH-NET-WORTH",
                "risco": "CRITICAL RISK (78%)",
                "dores": ["Desgaste por Decisões de Alto Impacto", "Erosão de Contorno Mandibular", "Fadiga Celular Sistêmica"],
                "fase_1": "PHASE I: CELLULAR STABILIZATION (0-90 Days)",
                "fase_2": "PHASE II: VASCULAR REJUVENATION (90-180 Days)",
                "fase_3": "PHASE III: MOLECULAR LONGEVITY (180+ Days)",
                "dep_5":  "Ano 5: Passivo Biológico Acumulado.",
                "dep_10": "Ano 10: Vulnerabilidade Biológica Exposta.",
                "dep_15": "Ano 15: Projeção de Entropia Celular."
            }
        }
        self.perfil_ativo = self.banco_perfis[1]

        self._configurar_rotas_flask()

    def escrever_texto_premium(self, imagem, texto, posicao, tamanho_fonte, cor):
        img_pil = Image.fromarray(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        try:
            fonte = ImageFont.truetype("arial.ttf", tamanho_fonte)
        except:
            fonte = ImageFont.load_default()
        draw.text(posicao, texto, font=fonte, fill=cor)
        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    def aplicar_filtro_biogemeo(self, imagem_base, modo, anos):
        h, w, _ = imagem_base.shape
        if "PRESERVAÇÃO" in modo:
            filtrada = cv2.edgePreservingFilter(imagem_base, flags=1, sigma_s=10, sigma_r=0.25)
            filtrada = cv2.convertScaleAbs(filtrada, alpha=1.05, beta=5)
            cor_borda = (130, 210, 0)
        else:
            gray = cv2.cvtColor(imagem_base, cv2.COLOR_BGR2GRAY)
            laplacian = cv2.Laplacian(gray, cv2.CV_8U, ksize=3)
            laplacian_color = cv2.cvtColor(laplacian, cv2.COLOR_GRAY2BGR)
            filtrada = cv2.addWeighted(imagem_base, 0.9, laplacian_color, 0.1, 0)
            filtrada = cv2.convertScaleAbs(filtrada, alpha=0.88, beta=-10)
            cor_borda = (0, 0, 180) # Vinho escuro para alertas de risco/entropia
            
        cv2.rectangle(filtrada, (0, 0), (w, h), cor_borda, 2)
        texto_topo = f"{modo} | +{anos}A"
        filtrada = self.escrever_texto_premium(filtrada, texto_topo, (10, 10), 10, (255, 255, 255))
        return filtrada

    def _configurar_rotas_flask(self):
        HTML_PAINEL = """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>Thierry Technology Concept Global - Master UHNWI</title>
            <style>
                body { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin: 0; padding: 20px; }
                h1 { color: #58a6ff; font-size: 22px; margin-bottom: 5px; }
                .container { position: relative; display: inline-block; border: 2px solid #30363d; border-radius: 8px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.5); }
                img { display: block; width: 850px; height: auto; }
                .painel-botoes { margin-top: 15px; display: flex; justify-content: center; gap: 15px; }
                .btn { background: rgba(22, 27, 34, 0.8); color: #58a6ff; border: 1px solid #58a6ff; padding: 12px 24px; font-size: 14px; font-weight: bold; border-radius: 6px; cursor: pointer; transition: all 0.3s ease; text-transform: uppercase; }
                .btn:hover { background: #58a6ff; color: #0d1117; box-shadow: 0 0 15px rgba(88, 166, 255, 0.4); }
                .btn-gold { border-color: #d4af37; color: #d4af37; }
                .btn-gold:hover { background: #d4af37; color: #0d1117; box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); }
                #status-bar { margin-top: 10px; font-size: 13px; color: #8b949e; font-family: monospace; }
            </style>
        </head>
        <body>
            <h1>THIERRY TECHNOLOGY CONCEPT GLOBAL - UHNWI AUDIT</h1>
            <div id="status-bar">SISTEMA CONECTADO // PRONTO PARA CAPTURA</div>
            <br>
            <div class="container">
                <img src="/video_feed" alt="Stream BioGême">
            </div>
            
            <div class="painel-botoes">
                <button class="btn" onclick="capturarFoto()">📷 Capturar Foto Limpa</button>
                <button class="btn btn-gold" onclick="dispararVarredura()">⚡ Iniciar Varredura M&A</button>
                <button class="btn" style="border-color: #f85149; color: #f85149;" onclick="reiniciarSistema()">🔄 Reiniciar Fluxo</button>
            </div>

            <script>
                function capturarFoto() {
                    fetch('/capturar_manual', {method: 'POST'}).then(res => res.json()).then(data => alert(data.mensagem));
                }
                function dispararVarredura() {
                    fetch('/disparar_varredura', {method: 'POST'}).then(res => res.json()).then(data => alert(data.mensagem));
                }
                function reiniciarSistema() {
                    fetch('/reiniciar', {method: 'POST'}).then(res => res.json()).then(data => alert(data.mensagem));
                }
                setInterval(() => {
                    fetch('/status_biometria').then(res => res.json()).then(data => {
                        document.getElementById('status-bar').innerText = data.status;
                    });
                }, 1000);
            </script>
        </body>
        </html>
        """

        @self.app.route('/')
        def index():
            return render_template_string(HTML_PAINEL)

        @self.app.route('/video_feed')
        def video_feed():
            return Response(self._gerar_stream_web(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/status_biometria')
        def status_biometria():
            return jsonify({
                "status": self.status_hud_web, 
                "captura_concluida": self.captura_realizada,
                "disparado": self.disparar_leitura,
                "fase": self.fase_atual
            })

        @self.app.route('/capturar_manual', methods=['POST'])
        def capturar_manual():
            self.solicitar_captura_manual = True
            return jsonify({"status": "sucesso", "mensagem": "Comando de captura enviado!"})

        @self.app.route('/disparar_varredura', methods=['POST'])
        def disparar_varredura():
            self.disparar_leitura = True
            return jsonify({"status": "sucesso", "mensagem": "Varredura M&A disparada!"})

        @self.app.route('/reiniciar', methods=['POST'])
        def reiniciar():
            self.captura_realizada = False
            self.disparar_leitura = False
            self.solicitar_captura_manual = False
            self.fase_atual = "CAPTURA_LIMPA"
            return jsonify({"status": "sucesso", "mensagem": "Sistema reiniciado!"})

    def _gerar_stream_web(self):
        while True:
            with self.lock:
                if self.frame_atual is None:
                    continue
                (flag, encodedImage) = cv2.imencode(".jpg", self.frame_atual)
                if not flag:
                    continue
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
            time.sleep(0.03)

    def capturar_foto_instantanea(self, frame_atual):
        os.makedirs("core/capturas", exist_ok=True)
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho_foto = f"core/capturas/FOTO_BIOGEME_{timestamp_str}.png"
        cv2.imwrite(caminho_foto, frame_atual)
        print(f"[FOTO CAPTURADA] Salva em: {caminho_foto}")
        return caminho_foto

    def iniciar_feed_camera_integrado(self, indice_preferido=0, modo_web=True, porta_web=801):
        print(f"\n[BIO-ORQUESTRADOR] Inicializando hardware de vídeo...")
        if modo_web:
            threading.Thread(target=self._loop_camera_processamento, args=(indice_preferido, True), daemon=True).start()
            print(f"[BIO-ORQUESTRADOR] Servidor rodando em http://localhost:{porta_web}")
            self.app.run(host='0.0.0.0', port=porta_web, debug=False, threaded=True)
            return
        self._loop_camera_processamento(indice_preferido, modo_web=False)

    def _loop_camera_processamento(self, indice_preferido, modo_web=True):
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.6, min_tracking_confidence=0.6)

        COR_CYAN_HUD = (255, 230, 0)
        COR_VERDE_ESTAVEL = (50, 240, 100)
        COR_PONTO_BASE = (255, 255, 255)
        COR_PULSO_LINHA = (255, 180, 50)

        PONTOS_ESQUERDA = [127, 234, 93, 58, 172, 136, 150, 149, 176, 148, 152, 377, 400, 378]
        PONTOS_DIREITA  = [356, 454, 323, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149]

        SIGLAS_ESQ = ["HAIR_D_L", "HYDR_L", "ALOP_L", "VIS_L", "CELL_L", "SKIN_L", "OXIM_L", "NEUR_L", "DERM_L", "POST_L", "FAC_L", "EYE_L", "CART_L", "MAND_L"]
        SIGLAS_DIR = ["HAIR_D_R", "HYDR_R", "ALOP_R", "VIS_R", "CELL_R", "SKIN_R", "OXIM_R", "NEUR_R", "DERM_R", "POST_R", "FAC_R", "EYE_R", "CART_R", "MAND_R"]
        VAL_ESQ: list[float] = [142.0, 0.93, 0.12, 0.95, 0.88, 0.76, 0.94, 0.92, 0.91, 0.85, 0.92, 0.34, 0.94, 0.96]
        VAL_DIR: list[float] = [145.0, 34.5, 0.10, 31.5, 22.8, 74.2, 13.9, 20.0, 37.3, 88.1, 40.2, 38.9, 35.0, 33.4]

        # Testador dinâmico integrado para evitar puxar a câmera errada (substituindo a inicialização estática)
        cameras_para_testar = [indice_preferido, 1, 2, 0, 3]
        cameras_testadas = set()
        cap = None
        indice_ativo_encontrado = 0

        for idx in cameras_para_testar:
            if idx in cameras_testadas: 
                continue
            cameras_testadas.add(idx)
            
            temp_cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW if os.name == 'nt' else cv2.CAP_ANY)
            if temp_cap.isOpened():
                ret, frame_teste = temp_cap.read()
                if ret and frame_teste is not None:
                    cap = temp_cap
                    indice_ativo_encontrado = idx
                    print(f"[SUCESSO] >>> Câmera conectada no ÍNDICE: {idx} <<<")
                    break
                else:
                    temp_cap.release()
            else:
                temp_cap.release()

        if cap is None or not cap.isOpened():
            print("[ERRO CRÍTICO] Nenhuma câmera funcional foi detectada.")
            return

        foto_crua = None
        tela_final_consolidada = None
        tempo_varredura_inicio: float = time.time()  # Inicializado como float para evitar warning do Pylance
        bip_1, bip_2, bip_3, bip_fim = False, False, False, False

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (640, 480))
            h, w, _ = frame.shape

            # FASE 1: Câmera Limpa
            if self.fase_atual == "CAPTURA_LIMPA":
                self.status_hud_web = f"CÂMERA LIMPA [INDEX: {indice_ativo_encontrado}] // AGUARDANDO COMANDO"
                bip_1, bip_2, bip_3, bip_fim = False, False, False, False
                if self.solicitar_captura_manual:
                    print('\a', flush=True)
                    foto_crua = frame.copy()
                    self.capturar_foto_instantanea(frame)
                    self.captura_realizada = True
                    self.solicitar_captura_manual = False
                    self.fase_atual = "STANDBY"

            # FASE 2: Standby para Disparo
            elif self.fase_atual == "STANDBY":
                self.status_hud_web = "FOTO CAPTURADA // AGUARDANDO DISPARO M&A"
                if self.disparar_leitura:
                    self.fase_atual = "VARREDURA"
                    tempo_varredura_inicio = time.time()
                    threading.Thread(target=emitir_voz_sincronizada, daemon=True).start()

            # FASE 3: Varredura com malha
            elif self.fase_atual == "VARREDURA":
                tempo_passado = time.time() - tempo_varredura_inicio
                if tempo_passado < 3.0:
                    estagio_max = 4; status_hud = "SCANNING: CELLULAR STABILIZATION"
                    if not bip_1: print('\a', flush=True); bip_1 = True
                elif 3.0 <= tempo_passado < 6.0:
                    estagio_max = 9; status_hud = "SCANNING: VASCULAR REJUVENATION"
                    if not bip_2: print('\a', flush=True); bip_2 = True
                elif 6.0 <= tempo_passado < 10.0:
                    estagio_max = 14; status_hud = "SCANNING: OSTEOMETRY STRUCTURAL"
                    if not bip_3: print('\a', flush=True); bip_3 = True
                else:
                    estagio_max = 14; status_hud = "CONSOLIDATION COMPLETE"
                    if not bip_fim: print('\a', flush=True); bip_fim = True
                    self.fase_atual = "BIOGEMEOS"

                self.status_hud_web = status_hud
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb_frame)
                
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        for idx in range(estagio_max):
                            ponto_id = PONTOS_ESQUERDA[idx]
                            landmark = face_landmarks.landmark[ponto_id]
                            rx, ry = int(landmark.x * w), int(landmark.y * h)
                            cv2.circle(frame, (rx, ry), 2, COR_CYAN_HUD, -1)

            # FASE 4: Renderização da Grade e Laudo Lateral M&A com Termos de Alta Precisão (Pillow)
            elif self.fase_atual == "BIOGEMEOS":
                self.status_hud_web = "MATRIZ DE BIOGÊMEOS E LAUDO UHNWI PRONTOS"
                if tela_final_consolidada is None and foto_crua is not None:
                    mini_w, mini_h = int(w / 3), int(h / 2)
                    mini_base = cv2.resize(foto_crua, (mini_w, mini_h))
                    
                    p5 = self.aplicar_filtro_biogemeo(mini_base.copy(), "PRESERVAÇÃO", 5)
                    p10 = self.aplicar_filtro_biogemeo(mini_base.copy(), "PRESERVAÇÃO", 10)
                    p15 = self.aplicar_filtro_biogemeo(mini_base.copy(), "PRESERVAÇÃO", 15)
                    
                    # Substituição pelos termos de alta performance / inteligência de risco
                    d5 = self.aplicar_filtro_biogemeo(mini_base.copy(), "PASSIVO BIOLÓGICO", 5)
                    d10 = self.aplicar_filtro_biogemeo(mini_base.copy(), "VULNERABILIDADE", 10)
                    d15 = self.aplicar_filtro_biogemeo(mini_base.copy(), "ENTROPIA CELULAR", 15)
                    
                    linha_sup = np.hstack([p5, p10, p15])
                    linha_inf = np.hstack([d5, d10, d15])
                    grade_final = np.vstack([linha_sup, linha_inf])
                    
                    largura_painel = 480
                    altura_exata = grade_final.shape[0]
                    painel = np.zeros((altura_exata, largura_painel, 3), dtype="uint8")
                    painel[:] = (15, 15, 15)
                    
                    p = self.perfil_ativo
                    linhas_laudo = [
                        ("THIERRY TECH - UHNWI AUDIT", (240, 240, 240)),
                        ("--------------------------------------------------", (120, 120, 120)),
                        (f"PERFIL: {p['nome']}", (0, 215, 255)),
                        (f"BIOLOGICAL RISK: {p['risco']}", (0, 0, 180)),
                        ("", (255, 255, 255)),
                        ("CRONOGRAMA M&A EXECUTIVO:", (130, 210, 0)),
                        (f" {p['fase_1']}", (130, 210, 0)),
                        (f" {p['fase_2']}", (130, 210, 0)),
                        (f" {p['fase_3']}", (130, 210, 0)),
                        ("", (255, 255, 255)),
                        ("AUDITORIA DE RISCO E ENTROPIA:", (0, 0, 180)),
                        (f" 5A  -> {p['dep_5']}", (0, 0, 180)),
                        (f" 10A -> {p['dep_10']}", (0, 0, 180)),
                        (f" 15A -> {p['dep_15']}", (0, 0, 180))
                    ]
                    
                    y_pos = 25
                    for linha, cor in linhas_laudo:
                        if linha != "":
                            painel = self.escrever_texto_premium(painel, linha, (15, y_pos), 9, cor)
                        y_pos += 22
                        
                    tela_final_consolidada = np.hstack([grade_final, painel])
                
                if tela_final_consolidada is not None:
                    frame = tela_final_consolidada

            with self.lock:
                self.frame_atual = frame.copy()

            if not modo_web:
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27: break

        cap.release()
        if not modo_web: cv2.destroyAllWindows()

if __name__ == "__main__":
    engine = BiogemEngine()
    engine.iniciar_feed_camera_integrado(indice_preferido=0, modo_web=True, porta_web=801)