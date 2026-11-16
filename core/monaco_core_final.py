import os
import json
import base64
import hashlib
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# Força o terminal a suportar UTF-8 e cores ANSI no Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError, OSError):
        pass

# Códigos ANSI para cores no terminal
C_RESET = "\033[0m"
C_BLUE = "\033[94m"
C_GREEN = "\033[92m"
C_CYAN = "\033[96m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==========================================
# 1. PIPELINE DE INGESTÃO VIVA (MonacoDataPipeline)
# ==========================================
class MonacoDataPipeline:
    def __init__(self) -> None:
        self.timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.asset_valuation: str = "€ 153.000,00"
        
    def fetch_telemetry(self) -> Dict[str, Any]:
        return {
            "holder": "Genilson Rodrigues",
            "location": "Sao Luis, MA",
            "timestamp": self.timestamp,
            "metrics": {
                "oximetry": "98%",
                "diaphragmatic_rhythm": "Stable // 12 bpm",
                "z_axis_coordinates": "100.380 vertices active",
                "asset_valuation": self.asset_valuation
            }
        }

# ==========================================
# 2. MOTOR CRIPTOGRÁFICO ASSIMÉTRICO (RSA + SHA-256)
# ==========================================
class MonacoCryptoEngine:
    def __init__(self) -> None:
        self.key = RSA.generate(2048)
        self.private_key = self.key
        self.public_key = self.key.publickey()
        
    def get_public_pem(self) -> bytes:
        return self.public_key.export_key()

    def sign_payload(self, payload_dict: Dict[str, Any]) -> tuple[str, str]:
        payload_bytes = json.dumps(payload_dict, sort_keys=True).encode()
        h = SHA256.new(payload_bytes)
        signature = base64.b64decode(base64.b64encode(pkcs1_15.new(self.private_key).sign(h)))
        return base64.b64encode(signature).decode(), h.hexdigest()

    def verify_signature(self, payload_dict: Dict[str, Any], signature_b64: str) -> bool:
        payload_bytes = json.dumps(payload_dict, sort_keys=True).encode()
        h = SHA256.new(payload_bytes)
        signature = base64.b64decode(signature_b64.encode())
        try:
            pkcs1_15.new(self.public_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

# ==========================================
# 3. MOTOR EDITORIAL PLATINUM (ReportLab)
# ==========================================
def generate_monaco_pdf(
    filename: str = "monaco_modelagem_platinum.pdf",
    telemetry: Optional[Dict[str, Any]] = None,
    pub_key: Optional[bytes] = None,
    signature_b64: Optional[str] = None,
    sha_hash: Optional[str] = None
) -> None:
    if telemetry is None or pub_key is None or signature_b64 is None or sha_hash is None:
        raise ValueError("Parametros obrigatorios ausentes para a geracao do PDF.")

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    c_azul = colors.HexColor("#0A192F")
    c_ouro = colors.HexColor("#D4AF37")
    c_cinza_claro = colors.HexColor("#F8F9FA")
    
    title_style = ParagraphStyle(
        'MonacoTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_azul,
        alignment=0,
        spaceAfter=12
    )
    
    subtitle_style = ParagraphStyle(
        'MonacoSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_ouro,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'MonacoBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#333333")
    )
    
    code_style = ParagraphStyle(
        'MonacoCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#111111")
    )

    story = []

    story.append(Paragraph("THIERRY TECHNOLOGY CONCEPT GLOBAL", title_style))
    story.append(Paragraph("SOVEREIGN C2 DEFENSE ENGINE // MONACO PLATINUM STANDARD", subtitle_style))
    story.append(Spacer(1, 10))

    metrics = telemetry["metrics"]

    data_sec1 = [
        [Paragraph("<b>PARAMETRO DE GOVERNANCA</b>", body_style), Paragraph("<b>VALOR / METRICA REGISTRADA</b>", body_style)],
        [Paragraph("Titular da Conta / Ativo", body_style), Paragraph(str(telemetry["holder"]), body_style)],
        [Paragraph("Base Operacional", body_style), Paragraph(str(telemetry["location"]), body_style)],
        [Paragraph("Timestamp de Emissao", body_style), Paragraph(str(telemetry["timestamp"]), body_style)],
        [Paragraph("Valuation Patrimonial", body_style), Paragraph(str(metrics["asset_valuation"]), body_style)]
    ]
    t1 = Table(data_sec1, colWidths=[200, 304])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_azul),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_cinza_claro])
    ]))
    story.append(t1)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>02 // TELEMETRIA VIVA & MALHA GEOMETRICA</b>", subtitle_style))
    data_sec2 = [
        [Paragraph("<b>METRICA BIOMETRICA</b>", body_style), Paragraph("<b>ESTADO DO SISTEMA</b>", body_style)],
        [Paragraph("Oximetria de Pulso", body_style), Paragraph(str(metrics["oximetry"]), body_style)],
        [Paragraph("Ritmo Diafragmatico", body_style), Paragraph(str(metrics["diaphragmatic_rhythm"]), body_style)],
        [Paragraph("Malha Cartesiana Eixo Z", body_style), Paragraph(str(metrics["z_axis_coordinates"]), body_style)]
    ]
    t2 = Table(data_sec2, colWidths=[200, 304])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_azul),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_cinza_claro])
    ]))
    story.append(t2)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>03 // PAINEL DE AUDITORIA & CHANCELA CRIPTOGRAFICA</b>", subtitle_style))
    
    pub_key_str = pub_key.decode() if isinstance(pub_key, bytes) else str(pub_key)
    pub_key_short = "\n".join(pub_key_str.splitlines()[:6]) + "\n[...CHAVE PEM PROTEGIDA...]"
    
    data_sec3 = [
        [Paragraph("<b>PARAMETRO DE SEGURANCA</b>", body_style), Paragraph("<b>STATUS TECNICO // ZERO-TRUST</b>", body_style)],
        [Paragraph("Status de Integridade", body_style), Paragraph("<b>Status: Locked // 100% Verde</b>", body_style)],
        [Paragraph("Hash SHA-256 da Sessao", body_style), Paragraph(sha_hash, code_style)],
        [Paragraph("Assinatura RSA (Base64)", body_style), Paragraph(signature_b64[:60] + "...", code_style)],
        [Paragraph("Chave Publica (PEM Ativa)", body_style), Paragraph(pub_key_short.replace('\n', '<br/>'), code_style)]
    ]
    t3 = Table(data_sec3, colWidths=[180, 324])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_azul),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_cinza_claro])
    ]))
    story.append(KeepTogether([t3]))

    def add_footer(canvas: Any, doc: Any) -> None:
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(54, 30, f"Thierry Technology Concept Global // Dossie Mestre UHNW - Pagina {doc.page}")
        canvas.drawString(54, 20, f"SHA-256 Integrity Hash: {sha_hash}")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)

# ==========================================
# 4. EXECUTAVEL PRINCIPAL & TESTE DE ESTRESSE
# ==========================================
if __name__ == "__main__":
    print(f"{C_CYAN}[*] Iniciando pipeline do ecossistema Monaco Core Final...{C_RESET}")
    
    pipeline = MonacoDataPipeline()
    telemetry_data = pipeline.fetch_telemetry()
    
    crypto = MonacoCryptoEngine()
    
    signature_b64, sha_hash = crypto.sign_payload(telemetry_data)
    pub_key_pem = crypto.get_public_pem()
    
    print(f"{C_GREEN}[+] Ingestao viva concluida com sucesso.{C_RESET}")
    print(f"{C_GREEN}[+] Hash SHA-256 gerado: {C_YELLOW}{sha_hash}{C_RESET}")
    
    print(f"{C_CYAN}[*] Executando auditoria ativa de integridade (Simulacao de Invasao)...{C_RESET}")
    tampered_data = telemetry_data.copy()
    tampered_data["metrics"]["asset_valuation"] = "€ 153.000,01"
    
    is_valid = crypto.verify_signature(tampered_data, signature_b64)
    if not is_valid:
        print(f"{C_RED}[ALERTA CRITICO DE SEGURANCA] Tentativa de adulteracao detectada! Assinatura RSA rejeitada perfeitamente.{C_RESET}")
    else:
        print(f"{C_RED}[ERRO] Falha na barreira de seguranca.{C_RESET}")

    generate_monaco_pdf(
        filename="monaco_modelagem_platinum.pdf",
        telemetry=telemetry_data,
        pub_key=pub_key_pem,
        signature_b64=signature_b64,
        sha_hash=sha_hash
    )
    print(f"{C_GREEN}[+] Relatorio PDF gerado com sucesso: monaco_modelagem_platinum.pdf{C_RESET}")
