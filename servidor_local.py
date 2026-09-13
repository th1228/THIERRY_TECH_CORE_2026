import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import json
import threading
import cv2
import mediapipe as mp
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Banco de dados em tempo real da telemetria quântica de visagismo
estado_sistema = {
    "scanner_ativo": False,
    "frame_camera": "",
    "pitch": 0.0,
    "yaw": 0.0,
    "roll": 0.0,
    "biogenomica_status": "OPTIMAL",
    "neuro_index": "88.4",
    "inflamacao_rate": "12%"
}

# ==========================================
# 1. MOTOR DE INTELIGÊNCIA ARTIFICIAL FACIAL
# ==========================================
def loop_visao_computacional():
    global estado_sistema
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
    cap = cv2.VideoCapture(0)
    
    while True:
        if estado_sistema["scanner_ativo"] and cap.isOpened():
            success, image = cap.read()
            if not success:
                continue
            
            image = cv2.flip(image, 1)
            h, w, _ = image.shape
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image_rgb)
            
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    nariz = face_landmarks.landmark[1]
                    estado_sistema["pitch"] = round((nariz.y - 0.5) * -50, 1)
                    estado_sistema["yaw"] = round((nariz.x - 0.5) * 50, 1)
                    
                    # Desenha a malha cibernética de alta densidade no rosto
                    for i in range(0, 468, 6):
                        pt = face_landmarks.landmark[i]
                        cx, cy = int(pt.x * w), int(pt.y * h)
                        cv2.circle(image, (cx, cy), 1, (254, 242, 0), -1)
            
            _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 70])
            import base64
            base64_str = base64.b64encode(buffer).decode('utf-8')
            estado_sistema["frame_camera"] = f"data:image/jpeg;base64,{base64_str}"
        else:
            estado_sistema["frame_camera"] = ""
            threading.Event().wait(0.1)

threading.Thread(target=loop_visao_computacional, daemon=True).start()

# ==========================================
# 2. CANAL DE SINCRONIZAÇÃO DE DADOS (WS)
# ==========================================
@app.websocket("/ws/visagismo")
async def canal_comunicacao(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_text(json.dumps(estado_sistema))
            try:
                dados_recebidos = await asyncio.wait_for(websocket.receive_text(), timeout=0.01)
                comando = json.loads(dados_recebidos)
                if "comando" in comando and comando["comando"] == "toggle_scanner":
                    estado_sistema["scanner_ativo"] = not estado_sistema["scanner_ativo"]
            except asyncio.TimeoutError:
                pass
            await asyncio.sleep(0.02)
    except Exception:
        pass

# ==========================================
# 3. INTERFACE SCI-FI CINEMATOGRÁFICA
# ==========================================
INTERFACE_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Quantum Visagism Interface Suite</title>
    <style>
        * { box-sizing: border-box; user-select: none; }
        body, html {
            margin: 0; padding: 0; width: 100%; height: 100%;
            background: #010206; font-family: 'Courier New', monospace, sans-serif;
            overflow: hidden; color: #00f2fe;
        }

        #cenario3d { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
        
        #video-overlay {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 48%; height: 58%; z-index: 3; display: none;
            border: 1px solid rgba(0, 242, 254, 0.6); border-radius: 4px;
            box-shadow: 0 0 40px rgba(0, 242, 254, 0.2); object-fit: cover;
        }

        .painel-hud {
            position: absolute; z-index: 10;
            background: rgba(2, 6, 16, 0.75);
            border: 1px solid rgba(0, 242, 254, 0.25);
            backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);
            padding: 24px;
        }

        .painel-hud::before, .painel-hud::after {
            content: ''; position: absolute; width: 12px; height: 12px; border-color: #00f2fe; border-style: solid;
        }
        .painel-hud::before { top: -2px; left: -2px; border-width: 2px 0 0 2px; }
        .painel-hud::after { bottom: -2px; right: -2px; border-width: 0 2px 2px 0; }

        #lado-esquerdo { top: 40px; left: 40px; width: 340px; display: flex; flex-direction: column; gap: 14px; }
        #lado-direito { top: 40px; right: 40px; width: 360px; display: flex; flex-direction: column; gap: 16px; }
        #seletor-lingua { top: 40px; left: 50%; transform: translateX(-50%); display: flex; gap: 15px; padding: 10px 20px; }

        .tag-titulo {
            font-size: 11px; letter-spacing: 3px; color: #ffffff; font-weight: bold;
            border-bottom: 1px solid rgba(0, 242, 254, 0.4); padding-bottom: 8px; margin-bottom: 10px;
            text-shadow: 0 0 8px rgba(0,242,254,0.6);
        }

        .btn-premium {
            background: rgba(0, 242, 254, 0.03); border: 1px solid rgba(0, 242, 254, 0.4);
            color: #ffffff; padding: 14px; font-size: 11px; font-weight: bold; font-family: inherit;
            letter-spacing: 2px; cursor: pointer; transition: all 0.2s ease;
            display: flex; justify-content: space-between; align-items: center;
        }
        .btn-premium:hover {
            background: rgba(0, 242, 254, 0.15); border-color: #00f2fe;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.3); transform: scale(1.02);
        }
        
        .btn-lang { background: transparent; border: 1px solid rgba(0,242,254,0.3); color: #cbd5e1; padding: 6px 14px; cursor: pointer; font-size: 10px; font-weight: bold; font-family: inherit;}
        .btn-lang.active { border-color: #00f2fe; color: #00f2fe; background: rgba(0,242,254,0.15); box-shadow: 0 0 8px rgba(0,242,254,0.3); }

        .bloco-metrica { border-left: 3px solid #00f2fe; background: rgba(0, 242, 254, 0.02); padding: 12px; }
        .label-metrica { font-size: 10px; color: #8ea2b0; text-transform: uppercase; margin-bottom: 5px; letter-spacing: 1px; }
        .valor-metrica { font-size: 24px; font-weight: bold; color: #ffffff; text-shadow: 0 0 10px rgba(0,242,254,0.8); }

        .crosshair-h { position: absolute; top: 50%; left: 5%; width: 90%; height: 1px; background: rgba(0, 242, 254, 0.1); z-index: 2; pointer-events: none;}
        .crosshair-v { position: absolute; left: 50%; top: 5%; width: 1px; height: 90%; background: rgba(0, 242, 254, 0.1); z-index: 2; pointer-events: none;}

        .scanlines {
            position: absolute; width: 100%; height: 100%; z-index: 20; pointer-events: none;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            background-size: 100% 4px, 6px 100%; opacity: 0.4;
        }
    </style>
</head>
<body>

    <div class="scanlines"></div>
    <div class="crosshair-h"></div>
    <div class="crosshair-v"></div>
    <div id="cenario3d"></div>
    <img id="video-overlay" src="" alt="Live Scanner Feed">

    <div id="seletor-lingua" class="painel-hud">
        <button id="btn-pt" class="btn-lang active" onclick="mudarIdioma('pt')">SYS.LOC // PT-BR</button>
        <button id="btn-en" class="btn-lang" onclick="mudarIdioma('en')">SYS.LOC // EN-US</button>
    </div>

    <div id="lado-esquerdo" class="painel-hud">
        <div class="tag-titulo"><span class="lang-txt" data-pt="COREIA VISAGISMO ENGINE" data-en="KOREA VISAGISM ENGINE">COREIA VISAGISMO ENGINE</span></div>
        <button class="btn-premium" onclick="acionarScanner()"><span class="lang-txt" data-pt="🔬 LABORATÓRIO SCANNER" data-en="🔬 SCANNER LABORATORY">🔬 LABORATÓRIO SCANNER</span> <span id="lbl-scan-status" style="color:#ff4757;">[OFFLINE]</span></button>
        <button class="btn-premium"><span class="lang-txt" data-pt="🧬 DESIGN ENGINE 4D" data-en="🧬 4D DESIGN ENGINE">🧬 DESIGN ENGINE 4D</span></button>
        <button class="btn-premium"><span class="lang-txt" data-pt="🔲 MONOBLOCO DIGITAL" data-en="🔲 DIGITAL MONOBLOCK">🔲 MONOBLOCO DIGITAL</span></button>
        <button class="btn-premium"><span class="lang-txt" data-pt="🛡️ ANTIPOLUIÇÃO CORTICAL" data-en="🛡️ CORTICAL ANTIPOLLUTION">🛡️ ANTIPOLUIÇÃO CORTICAL</span></button>
    </div>

    <div id="lado-direito" class="painel-hud">
        <div class="tag-titulo"><span class="lang-txt" data-pt="DIAGNÓSTICO BIOMÉTRICO" data-en="BIOMETRIC DIAGNOSTICS">DIAGNÓSTICO BIOMÉTRICO</span></div>
        
        <div class="bloco-metrica">
            <div class="label-metrica lang-txt" data-pt="Biogenômica Celular" data-en="Cellular Biogenomics">Biogenômica Celular</div>
            <div class="valor-metrica" id="val-biogenomica">OPTIMAL</div>
        </div>

        <div class="bloco-metrica">
            <div class="label-metrica lang-txt" data-pt="Índice de Neuroplasticidade" data-en="Neuroplasticity Index">Índice de Neuroplasticidade</div>
            <div class="valor-metrica" id="val-neuro" style="color:#bc6ffb;">88.4</div>
        </div>

        <div class="bloco-metrica">
            <div class="label-metrica lang-txt" data-pt="Taxa de Inflamação Cortical" data-en="Cortical Inflammation Rate">Taxa de Inflamação Cortical</div>
            <div class="valor-metrica" id="val-inflamacao" style="color:#ff4757;">12%</div>
        </div>
    </div>

    <script>
        const ws = new WebSocket("ws://" + window.location.host + "/ws/visagismo");
        let scannerAtivo = false;

        ws.onmessage = function(event) {
            const dados = JSON.parse(event.data);
            
            const imgElement = document.getElementById("video-overlay");
            if (dados.frame_camera && dados.frame_camera !== "") {
                imgElement.src = dados.frame_camera;
                imgElement.style.display = "block";
            } else {
                imgElement.style.display = "none";
            }

            document.getElementById("val-biogenomica").innerText = dados.biogenomica_status;
            document.getElementById("val-neuro").innerText = dados.neuro_index;
            document.getElementById("val-inflamacao").innerText = dados.inflamacao_rate;
        };

        function acionarScanner() {
            scannerAtivo = !scannerAtivo;
            ws.send(JSON.stringify({ "comando": "toggle_scanner" }));
            
            const statusLbl = document.getElementById("lbl-scan-status");
            if (scannerAtivo) {
                statusLbl.innerText = "[ONLINE]";
                statusLbl.style.color = "#00f2fe";
            } else {
                statusLbl.innerText = "[OFFLINE]";
                statusLbl.style.color = "#ff4757";
            }
        }

        function mudarIdioma(lang) {
            document.querySelectorAll('.btn-lang').forEach(b => b.classList.remove('active'));
            document.getElementById('btn-' + lang).classList.add('active');

            document.querySelectorAll('.lang-txt').forEach(el => {
                const texto = el.getAttribute('data-' + lang);
                if (texto) el.innerText = texto;
            });
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def pagina_principal():
    return HTMLResponse(content=INTERFACE_HTML)

if __name__ == "__main__":
    uvicorn.run("servidor_local:app", host="127.0.0.1", port=8000, reload=True)