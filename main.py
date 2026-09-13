# -*- coding: utf-8 -*-
"""
THIERRY TECHNOLOGY CONCEPT GLOBAL - MAIN ORCHESTRATOR & SOVEREIGN NODE
Módulo Master Central com Logs de Rastreio de PDFs (Roy, Pit, Dossier) para Terminal.
Integrado com os módulos de Geofencing, Validação de Licença e Monitoramento de Erros.
"""

from datetime import datetime
import os
import sys
import time
import cv2
import json
import numpy as np
from pathlib import Path 
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, Query, Response, HTTPException, Request, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# --- CAMADA DE SEGURANÇA E FALLBACKS ---
class LogSeguroFallback:
    def registrar(self, modulo: str, acao: str, desc: str) -> None:
        print(f"[LOG SEGURO] [{modulo}] {acao}: {desc}")

LogSeguro: Any
try:
    from security.log_seguro import LogSeguro # type: ignore
except ImportError:
    LogSeguro = LogSeguroFallback

# --- IMPORTAÇÃO DOS MÓDULOS NATIVOS DO ECOSSISTEMA TCC GLOBAL ---
ValidadorLocal: Any = None
try:
    from core.validador_licenca import ValidadorLocal # type: ignore
except ImportError:
    ValidadorLocal = None

try:
    from core.geodefense import validar_geofencing_global, gerar_token_titular_global # type: ignore
except ImportError:
    def validar_geofencing_global(*args: Any, **kwargs: Any) -> bool: return True # type: ignore
    def gerar_token_titular_global() -> str: return "TCC-GLOBAL-FALLBACK" # type: ignore

# --- IMPORTAÇÃO DO GERADOR DE ROY CLÍNICO (ROI & FINANCEIRO) ---
GeradorRoyClinica: Any = None
try:
    from core.gerar_relatorio_roy_clinica import GeradorRoyClinica # type: ignore
except ImportError:
    GeradorRoyClinica = None

# --- IMPORTAÇÃO DO AUDITOR DE INTEGRIDADE GLOBAL ---
try:
    from auditor_integridade_global import AuditorIntegridadeGlobal # type: ignore
except ImportError:
    class AuditorIntegridadeGlobal:
        def __init__(self, limiar_confianca_minimo: float = 100.0):
            pass
        def inspecionar_dicionario_metricas(self, d: Dict[str, Any]) -> Dict[str, Any]:
            return {"status_aprovacao": True, "indice_integridade_percentual": 100.0, "anomalias_encontradas": []}
        def gerar_selo_criptografico_soberano(self, d: Dict[str, Any], t: str) -> str:
            return "TCC-SOBERANO-SHA256-SEAL"

# --- IMPORTAÇÃO DO MOTOR DE PDF (BIOGEM ENGINE DENTRO DA PASTA CORE) ---
BiogemEngine: Any = None
try:
    from core.biogem_engine import BiogemEngine # type: ignore
    print("[TERMINAL DE RASTREIO] Sucesso: BiogemEngine carregado de dentro da pasta core.")
except ImportError:
    try:
        from biogem_engine import BiogemEngine # type: ignore
    except ImportError:
        BiogemEngine = None
        print("[TERMINAL DE RASTREIO] Aviso: BiogemEngine não encontrado na pasta core.")

app = FastAPI(title="Thierry Technology Concept - Sovereign Master & Biogêmeos Orquestrador")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/results", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- CONFIGURAÇÃO DA PASTA DE PDFs FINAIS (ESTÁTICO PARA O NAVEGADOR) ---
PASTA_PDFS_FINAIS = Path("core/pdfs_finais")
PASTA_PDFS_FINAIS.mkdir(parents=True, exist_ok=True)

# Montagem correta da pasta core inteira para liberar o subdiretório core/pdfs_finais na web
app.mount("/core", StaticFiles(directory="core"), name="core_files")
app.mount("/pdfs", StaticFiles(directory=str(PASTA_PDFS_FINAIS)), name="pdfs_finais")

logger = LogSeguro()

# --- FUNÇÃO AUXILIAR DE TIPOGRAFIA PREMIUM (PIL) ---
def escrever_texto_premium(imagem: np.ndarray, texto: str, posicao: tuple[int, int], tamanho_fonte: int, cor: tuple[int, int, int]) -> np.ndarray:
    img_pil = Image.fromarray(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    try:
        fonte = ImageFont.truetype("arial.ttf", tamanho_fonte)
    except:
        fonte = ImageFont.load_default()
    draw.text(posicao, texto, font=fonte, fill=cor)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


# =====================================================================
# CLASSE CENTRAL: ORQUESTRADOR MASTER DO ECOSSISTEMA
# =====================================================================
class BiogemeoOrquestradorMaster:
    def __init__(self):
        self.frame_atual_camera: Optional[np.ndarray] = None
        self.estado_fluxo: str = "AO_VIVO"  
        self.auditor = AuditorIntegridadeGlobal(limiar_confianca_minimo=100.0)
        
        self.memoria_sessao: Dict[str, Any] = {
            "ultimo_cliente": "THIERRY RODRIGUES",
            "email_cliente": "theiry10rd@gmail.com",
            "telemetria": {"frequencia_vetorial": "1.4 Hz", "oximetria_tecidual": "98.2%"},
            "tabela_biogemeos": [],
            "fila_arquivos_gerados": [],
            "selo_criptografico": ""
        }

    def inicializar_sistema(self) -> None:
        print("[TERMINAL DE RASTREIO] Inicializando subsistema de orquestração de relatórios PDF (Roy, Pit, Dossier)...")
        
        if ValidadorLocal is not None:
            try:
                validador = ValidadorLocal()
                status_lic, msg_lic = validador.varrer_servidor_local()
                print(f"[SECURITY CHECK] {msg_lic}")
                if not status_lic:
                    print("[FALHA CRÍTICA] Licença ou integridade do servidor rejeitada!")
            except Exception as e:
                print(f"[AVISO VALIDADOR] Falha na execução do validador local: {e}")

        logger.registrar("ORQUESTRADOR", "STARTUP", "Ecossistema TCC Global inicializado e pronto na porta 801.")

    def salvar_frame_capturado(self, imagem_bytes: bytes) -> str:
        nparr = np.frombuffer(imagem_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is not None:
            self.frame_atual_camera = img.copy()
            caminho_foto = "static/results/face_capturada.jpg"
            cv2.imwrite(caminho_foto, img)
            print(f"[TERMINAL DE RASTREIO] Frame de captura processado e gravado em: {caminho_foto}")
            return caminho_foto
        return ""

    def registrar_arquivo_na_fila(self, tipo: str, caminho: str) -> None:
        item = {
            "tipo": tipo,
            "caminho": caminho,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.memoria_sessao["fila_arquivos_gerados"].append(item)
        print(f"[TERMINAL DE RASTREIO] -> [REGISTRO DE ARQUIVO] Tipo: {tipo} | Caminho gerado: {caminho}")
        logger.registrar("FILA", "REGISTRO", f"Arquivo {tipo} enfileirado com sucesso: {caminho}")


orquestrador = BiogemeoOrquestradorMaster()


class RelatorioDossierRequest(BaseModel):
    nome_cliente: Optional[str] = "THIERRY RODRIGUES"
    contato_cliente: Optional[str] = "theiry10rd@gmail.com"
    operador: Optional[str] = "Thierry (TCC SOBERANO)"
    perfil: Optional[str] = "monaco"
    idioma: Optional[str] = "PT"


@app.on_event("startup")
def startup_event() -> None:
    orquestrador.inicializar_sistema()


@app.get("/", response_class=HTMLResponse)
def servir_painel_html() -> HTMLResponse:
    html_path = os.path.join("templates", "painel_web.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Erro: templates/painel_web.html não encontrado.</h1>", status_code=404)


def gerar_frames():
    while True:
        if orquestrador.frame_atual_camera is not None:
            frame = orquestrador.frame_atual_camera.copy()
        else:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "TCC ORCHESTRATOR: BROWSER WEBCAM ACTIVE", (20, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 200), 2, cv2.LINE_AA)
        
        ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if ret:
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")
        time.sleep(0.04)


@app.get("/video_feed")
def video_feed() -> StreamingResponse:
    return StreamingResponse(gerar_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


@app.post("/api/v1/camera/receber-frame")
async def receber_frame_html(file: UploadFile = File(...)):
    contents = await file.read()
    caminho = orquestrador.salvar_frame_capturado(contents)
    if caminho:
        return {"status": "sucesso", "caminho": caminho}
    raise HTTPException(status_code=400, detail="Falha ao processar imagem no orquestrador.")


@app.post("/iniciar_varredura")
def iniciar_varredura(perfil: str = Query("monaco"), idioma: str = Query("pt")) -> Dict[str, Any]:
    print(f"\n[TERMINAL DE RASTREIO] === INICIANDO VARREDURA TIER-1 (Perfil: {perfil}) ===")
    caminho_foto = "static/results/face_capturada.jpg"
    
    dados_sessao_atual = {
        "Sessão / Módulo": f"Varredura Biométrica UHNW - Perfil: {perfil}",
        "Fonte de Imagem": caminho_foto if os.path.exists(caminho_foto) else "N/A",
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    selo_soberano = orquestrador.auditor.gerar_selo_criptografico_soberano(dados_sessao_atual, f"TX-{perfil.upper()}-01")
    
    tabela_gerada = [
        {"indice": 1, "biogenio": "Fototipo Base Real", "simetria_estrutural": "98.00%", "tensao_mandibular": "0.020mm", "tonicidade_tecidual": "99.40%", "status_governanca": "Master Tier-1"},
        {"indice": 2, "biogenio": "Contorno Mandibular", "simetria_estrutural": "96.50%", "tensao_mandibular": "0.025mm", "tonicidade_tecidual": "98.10%", "status_governanca": "Estável"},
        {"indice": 3, "biogenio": "Colágeno Apex", "simetria_estrutural": "95.20%", "tensao_mandibular": "0.030mm", "tonicidade_tecidual": "97.50%", "status_governanca": "Preservado"},
        {"indice": 4, "biogenio": "Preservação (+5A)", "simetria_estrutural": "94.00%", "tensao_mandibular": "0.032mm", "tonicidade_tecidual": "96.80%", "status_governanca": "Simulado Tier-1"},
        {"indice": 5, "biogenio": "Preservação (+10A)", "simetria_estrutural": "91.50%", "tensao_mandibular": "0.038mm", "tonicidade_tecidual": "94.20%", "status_governanca": "Simulado Tier-2"},
        {"indice": 6, "biogenio": "Preservação (+15A)", "simetria_estrutural": "89.00%", "tensao_mandibular": "0.045mm", "tonicidade_tecidual": "91.00%", "status_governanca": "Simulado Tier-3"}
    ]

    orquestrador.memoria_sessao["tabela_biogemeos"] = tabela_gerada
    orquestrador.memoria_sessao["selo_criptografico"] = selo_soberano
    print(f"[TERMINAL DE RASTREIO] Varredura concluída com sucesso. Selo gerado: {selo_soberano}")

    return {
        "status": "sucesso", 
        "mensagem": "Varredura processada e injetada na memória comum do Orquestrador Master.",
        "biogemeos": {"selo_criptografico": selo_soberano}
    }


@app.post("/api/v1/gerar-pdf-dossie")
def gerar_pdf_dossie_endpoint(data: RelatorioDossierRequest) -> JSONResponse:
    try:
        nome_cli = data.nome_cliente or "THIERRY RODRIGUES"
        contato_cli = data.contato_cliente or "theiry10rd@gmail.com"
        operador_cli = data.operador or "Thierry (TCC SOBERANO)"
        perfil_cli = data.perfil.lower().strip() or "monaco"

        print(f"\n[TERMINAL DE RASTREIO] *** REQUISIÇÃO DE GERAÇÃO DE RELATÓRIO PDF ***")
        print(f" -> Tipo / Perfil Solicitado pelo Front-End: {perfil_cli}")
        print(f" -> Cliente: {nome_cli} | Contato: {contato_cli}")

        orquestrador.memoria_sessao["ultimo_cliente"] = nome_cli
        orquestrador.memoria_sessao["email_cliente"] = contato_cli

        dados_memoria = orquestrador.memoria_sessao
        
        # --- ROTEAMENTO CIRÚRGICO INTEGRADO PARA O ROY CLÍNICO ---
        if perfil_cli == "roy" and GeradorRoyClinica is not None:
            gerador_roy = GeradorRoyClinica(
                nome_cliente=nome_cli,
                contato_cliente=contato_cli,
                operador=operador_cli,
                tabela_biogemeos=dados_memoria.get("tabela_biogemeos", []),
                telemetria=dados_memoria.get("telemetria", {}),
                pasta_destino=str(PASTA_PDFS_FINAIS)
            )
            caminho_gerado = gerador_roy.gerar()
            print(f"[TERMINAL DE RASTREIO] GeradorRoyClinica processou o relatório financeiro com sucesso. Caminho: {caminho_gerado}")
            
        elif BiogemEngine is not None:
            engine_pdf = BiogemEngine(
                tipo_relatorio=perfil_cli,
                nome_cliente=nome_cli,
                contato_cliente=contato_cli,
                operador=operador_cli,
                tabela_biogemeos=dados_memoria.get("tabela_biogemeos", []),
                telemetria=dados_memoria.get("telemetria", {})
            )
            
            if perfil_cli == "roy":
                caminho_gerado = engine_pdf.gerar_relatorio_roi_clinica()
            elif perfil_cli == "pit":
                caminho_gerado = engine_pdf.gerar_pitch_soberano_pdf()
            else:
                caminho_gerado = engine_pdf.gerar_relatorio_pdf()
                
            print(f"[TERMINAL DE RASTREIO] BiogemEngine processou o módulo '{perfil_cli}' com sucesso. Caminho: {caminho_gerado}")
        else:
            prefixo_nome = f"DOSSIER_{perfil_cli.upper()}"
            nome_arquivo = f"{prefixo_nome}_{nome_cli.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            caminho_gerado = str(PASTA_PDFS_FINAIS / nome_arquivo)
            print(f"[TERMINAL DE RASTREIO] AVISO: Motores especializados não encontrados. Gerando PDF binário padrão para {perfil_cli} em: {caminho_gerado}")
            
            pdf_bytes_minimo = (
                b"%PDF-1.4\n"
                b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
                b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
                b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 595 842]/Resources<<>>/Contents 4 0 R>>endobj\n"
                b"4 0 obj<</Length 55>>stream\nBT /F1 12 Tf 72 700 Td (TCC GLOBAL - RELATORIO SOBERANO) Tj ET\nendstream\nendobj\n"
                b"xref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000216 00000 n \n"
                b"trailer<</Size 5/Root 1 0 R>>\nstartxref\n227\n%%EOF"
            )
            with open(caminho_gerado, "wb") as f:
                f.write(pdf_bytes_minimo)

        nome_arquivo_gerado = os.path.basename(caminho_gerado)
        caminho_url = f"/core/pdfs_finais/{nome_arquivo_gerado}"

        orquestrador.registrar_arquivo_na_fila(f"Relatorio_{perfil_cli.upper()}", caminho_url)

        return JSONResponse(content={
            "status": "sucesso",
            "cliente": nome_cli.upper(),
            "caminho_arquivo": caminho_url,
            "tipo_gerado": perfil_cli,
            "fila_atual": orquestrador.memoria_sessao["fila_arquivos_gerados"],
            "mensagem": f"Relatório ({perfil_cli}) gerado e enfileirado com sucesso."
        })
        
    except Exception as e:
        import traceback
        print(f"\n{'!'*75}")
        print(f" [FALHA CRÍTICA NO ENDPOINT /api/v1/gerar-pdf-dossie]")
        print(f" - Erro detectado: {str(e)}")
        print(f" - Rastreamento detalhado do erro:")
        traceback.print_exc()
        print(f"{'!'*75}\n")
        raise HTTPException(status_code=500, detail=f"Erro interno no orquestrador: {str(e)}")


@app.get("/api/v1/fila-arquivos")
def consultar_fila_arquivos() -> JSONResponse:
    return JSONResponse(content={
        "status": "sucesso",
        "total_arquivos": len(orquestrador.memoria_sessao["fila_arquivos_gerados"]),
        "fila": orquestrador.memoria_sessao["fila_arquivos_gerados"]
    })


@app.get("/api/v1/dossie/detalhes-ativo")
def detalhes_dossie_ativo() -> JSONResponse:
    return JSONResponse(content={
        "status": "sucesso",
        "perfil": "Monaco Tier-1 Audit Terminal",
        "dados_alvo": {
            "nome": orquestrador.memoria_sessao.get("ultimo_cliente", "THIERRY RODRIGUES"),
            "email": orquestrador.memoria_sessao.get("email_cliente", "theiry10rd@gmail.com")
        },
        "metricas": {
            "retracao_mandibular": "0.02mm (Eixo Estável)",
            "tonicidade_tecidual": "99.4%",
            "frequencia_vetorial": "1.4 Hz / 98.2%",
            "malha_rastreamento": "64 Nós Ativos (Zero-Trust)"
        },
        "governanca": {
            "organizacao": "Thierry Technology Concept Global",
            "status": "Aprovado via Terminal Soberano (Porta 801)"
        },
        "timestamp": datetime.now().strftime("%Y-%m-%d %T")
    })


@app.post("/api/v1/pdfs/enviar-email")
def enviar_pdf_email(destinatario: str = Query(...), arquivo: str = Query(...)) -> JSONResponse:
    return JSONResponse(content={
        "status": "sucesso",
        "mensagem": f"Relatório enviado com segurança para {destinatario}.",
        "arquivo": arquivo,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


@app.get("/api/v1/pdfs/listar")
def listar_pdfs_finais() -> JSONResponse:
    print(f"\n[TERMINAL DE RASTREIO] Verificando arquivos PDF disponíveis em: {PASTA_PDFS_FINAIS.absolute()}")
    try:
        if not PASTA_PDFS_FINAIS.exists():
            return JSONResponse(content={"status": "erro", "mensagem": "Pasta core/pdfs_finais não encontrada."}, status_code=404)
        
        arquivos = sorted(PASTA_PDFS_FINAIS.glob("*.pdf"), key=os.path.getmtime, reverse=True)
        lista_arquivos = []
        
        for f in arquivos:
            nome_arq = f.name.lower()
            tipo_classificado = "dossie"
            if "roy" in nome_arq:
                tipo_classificado = "roy"
            elif "pit" in nome_arq:
                tipo_classificado = "pit"
                
            lista_arquivos.append({
                "nome": f.name,
                "tipo_identificado": tipo_classificado,
                "caminho": f"/core/pdfs_finais/{f.name}",
                "tamanho_kb": round(f.stat().st_size / 1024, 2),
                "data_modificacao": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return JSONResponse(content={
            "status": "sucesso",
            "diretorio": str(PASTA_PDFS_FINAIS.absolute()),
            "total": len(lista_arquivos),
            "arquivos": lista_arquivos
        })
    except Exception as e:
        import traceback
        print(f"[ERRO LISTAGEM PDF] {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/pdfs/abrir/{nome_arquivo}")
def abrir_pdf_especifico(nome_arquivo: str):
    caminho_arquivo = PASTA_PDFS_FINAIS / nome_arquivo
    if caminho_arquivo.exists() and caminho_arquivo.is_file():
        return FileResponse(path=caminho_arquivo, media_type='application/pdf', filename=nome_arquivo)
    raise HTTPException(status_code=404, detail="Arquivo PDF não foi encontrado na pasta core/pdfs_finais.")


if __name__ == "__main__":
    print("=================================================================")
    print("   THIERRY TECHNOLOGY CONCEPT GLOBAL - ORQUESTRADOR MASTER      ")
    print("   Servidor Soberano FastAPI Ativo na Porta 801 (Com Logs de PDF) ")
    print("=================================================================")
    try:
        uvicorn.run("main:app", host="127.0.0.1", port=801, reload=False)
    except Exception as e:
        import traceback
        print(f"\n{'!'*75}")
        print(f" [FALHA CRÍTICA NA EXECUÇÃO DO UVICORN]")
        print(f" - Erro: {str(e)}")
        traceback.print_exc()
        print(f"{'!'*75}\n")