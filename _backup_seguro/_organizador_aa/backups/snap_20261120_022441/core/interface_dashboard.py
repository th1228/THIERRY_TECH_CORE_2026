# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the 
intellectual property of Thierry Technology Concept Global. Unauthorized 
distribution, reverse engineering, or usage without a signed NDA/License 
agreement is strictly prohibited under international copyright frameworks.
===========================================================================
"""

import sys
import os
import json
import asyncio
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn
from dotenv import load_dotenv

# Carrega o .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI()

def verificar_sessao_ativa():
    try:
        caminho_sessao = os.path.join(os.path.dirname(__file__), 'sessao.json')
        with open(caminho_sessao, 'r') as f:
            data = json.load(f)
            return data.get("ativo") == True
    except Exception:
        return False

# Interface Básica
INTERFACE_HUD_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>TTC Global</title>
</head>
<body style="background: #040814; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; font-family: sans-serif;">
    <h1>SISTEMA TTC GLOBAL ONLINE</h1>
    <script>
        const socket = new WebSocket("ws://" + window.location.host + "/ws/dados");
        socket.onmessage = function(event) {
            const dados = JSON.parse(event.data);
            if(dados.status === "DENIED") { window.location.reload(); }
        };
    </script>
</body>
</html>
"""

@app.get("/")
async def pagina_principal():
    if not verificar_sessao_ativa():
        return HTMLResponse("<h1>ACESSO NEGADO</h1>", status_code=403)
    return HTMLResponse(INTERFACE_HUD_HTML)

@app.websocket("/ws/dados")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            if not verificar_sessao_ativa():
                await websocket.send_text(json.dumps({"status": "DENIED"}))
                break
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Sessão encerrada.")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)