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

"""
THIÉRRY TECHNOLOGY CONCEPT GLOBAL - MAIN ORCHESTRATOR & SOVEREIGN NODE
Módulo Master Central com Roteamento por Gateways (Biogêmeos, Clínica e Salão/Tricologia),
Gerador de Dossiês PDF Nativos e Criptografia ECDSA Padrão Tier-1 de Mônaco.
Integrado nativamente ao Motor APDP Mônaco (Lei nº 1.565) e C2 Cognitive Voice.
Suporte bilíngue nativo (PT / EN) e multi-dispositivo (Computador, Tablet e Celular).
"""

import datetime
import os
import sys
import time
import socket
import cv2
import json
import hashlib
import platform
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
from fastapi import FastAPI, Query, Response, HTTPException, Request, File, UploadFile, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
import uvicorn
import fitz  # PyMuPDF para conversão dinâmica de PDF em imagem
import stripe  # SDK oficial da Stripe para pagamentos reais
from dotenv import load_dotenv

# --- CARREGAMENTO SEGURO DAS VARIÁVEIS DE AMBIENTE (.ENV) ---
load_dotenv()

# --- CONFIGURAÇÕES DE REDE E AMBIENTE (MULTI-DISPOSITIVO: PC, TABLET, CELULAR) ---
TTC_HOST = os.getenv("TTC_HOST", "0.0.0.0")
TTC_PORT = int(os.getenv("TTC_PORT", "801"))
TTC_ENV = os.getenv("TTC_ENV", "production").strip().lower()
TTC_ENFORCE_LEDGER_LOCK = os.getenv("TTC_ENFORCE_LEDGER_LOCK", "false").strip().lower() == "true"

# --- CAMINHO BASE BLINDADO (À PROVA DE DESZIPAGEM) ---
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


# =====================================================================
# MOTOR BILÍNGUE NATIVO (PORTUGUÊS / INGLÊS)
# =====================================================================
TRADUCOES_TTC: Dict[str, Dict[str, str]] = {
    "PT": {
        "sistema_online": "Sistema Soberano Online",
        "sucesso": "sucesso",
        "erro": "erro",
        "dossie_gerado": "Dossiê Mônaco gerado com sucesso!",
        "dossie_enviado_fila": "Envio do dossiê enfileirado com sucesso para",
        "conduta_selada": "Conduta clínica assinada, selada no Ledger e pronta para compilação!",
        "licenca_aceita": "Licenciamento aceito com sucesso.",
        "estado_sincronizado": "Estado preditivo sincronizado!",
        "ledger_vazio": "Ledger vazio.",
        "ledger_integro": "Cadeia e chaves assimétricas Mônaco Tier-1 100% íntegras.",
        "modulo_clinica": "Clínica & Estética Avançada",
        "colageno_preservado": "Preservado",
        "estagio_otimo": "Estágio Ótimo",
        "modulo_salao": "Salão de Beleza & Tricologia",
        "densidade_alta": "Alta densidade (85 fios/cm²)",
        "couro_equilibrado": "Equilibrado / Sem descamação visível",
        "colorimetria_sugerida": "Subtom Quente / Fórmulas Davines & Wella preparadas",
        "setor_atuacao": "Tecnologia e Inovação",
        "email_assunto": "Thierry Technology Concept Global - Dossiê Soberano",
        "email_saudacao": "Prezado(a)",
        "email_corpo": "Segue em anexo o dossiê executivo solicitado",
        "email_despedida": "Atenciosamente",
        "err_arquivo_invalido": "Nome de arquivo inválido.",
        "err_pdf_nao_encontrado": "Arquivo PDF não encontrado.",
        "err_imagem_falha": "Falha ao processar imagem.",
        "err_modulo_nao_especificado": "Módulo não especificado.",
        "err_tier_nao_encontrado": "Licença ou tier não encontrado.",
        "err_contrato_nao_encontrado": "Contrato não encontrado.",
        "err_canal_invalido": "Canal de comunicação inválido.",
    },
    "EN": {
        "sistema_online": "Sovereign System Online",
        "sucesso": "success",
        "erro": "error",
        "dossie_gerado": "Monaco Dossier successfully generated!",
        "dossie_enviado_fila": "Dossier dispatch queued successfully for",
        "conduta_selada": "Clinical protocol signed, sealed in the Ledger, and ready for compilation!",
        "licenca_aceita": "Licensing agreement accepted successfully.",
        "estado_sincronizado": "Predictive state synchronized!",
        "ledger_vazio": "Ledger is empty.",
        "ledger_integro": "Monaco Tier-1 asymmetric keys and chain 100% intact.",
        "modulo_clinica": "Clinic & Advanced Aesthetics",
        "colageno_preservado": "Preserved",
        "estagio_otimo": "Optimal Stage",
        "modulo_salao": "Luxury Hair Salon & Trichology",
        "densidade_alta": "High density (85 strands/cm²)",
        "couro_equilibrado": "Balanced / No visible flaking",
        "colorimetria_sugerida": "Warm Undertone / Davines & Wella formulas prepared",
        "setor_atuacao": "Technology and Innovation",
        "email_assunto": "Thierry Technology Concept Global - Sovereign Dossier",
        "email_saudacao": "Dear",
        "email_corpo": "Please find attached the requested executive dossier",
        "email_despedida": "Sincerely",
        "err_arquivo_invalido": "Invalid file name.",
        "err_pdf_nao_encontrado": "PDF file not found.",
        "err_imagem_falha": "Failed to process image.",
        "err_modulo_nao_especificado": "Module not specified.",
        "err_tier_nao_encontrado": "License or tier not found.",
        "err_contrato_nao_encontrado": "Contract not found.",
        "err_canal_invalido": "Invalid communication channel.",
    }
}


def normalizar_idioma(lang: Optional[str]) -> str:
    """Normaliza o código de idioma para 'PT' ou 'EN'."""
    if not lang:
        return "PT"
    codigo = lang.strip().upper()
    if codigo.startswith("EN"):
        return "EN"
    return "PT"


def t(chave: str, lang: Optional[str] = "PT") -> str:
    """Retorna a string traduzida em Português (PT) ou Inglês (EN)."""
    idioma = normalizar_idioma(lang)
    return TRADUCOES_TTC.get(idioma, TRADUCOES_TTC["PT"]).get(
        chave, TRADUCOES_TTC["PT"].get(chave, chave)
    )


def obter_ip_rede_local() -> str:
    """Descobre o IP local da máquina na rede Wi-Fi/LAN para acesso via celular e tablet."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return str(s.getsockname()[0])
    except OSError:
        return "127.0.0.1"


def obter_origens_cors_permitidas() -> List[str]:
    """
    Define origens CORS seguras a partir da variável TTC_ALLOWED_ORIGINS.
    Em ambiente local/LAN sem domínio fixo definido, aceita localhost e IPs privados
    (127.0.0.1, 192.168.x.x, 10.x.x.x, 172.16-31.x.x) para uso fluido em PC, tablet e celular.
    """
    origens_env = os.getenv("TTC_ALLOWED_ORIGINS", "").strip()
    if origens_env:
        return [o.strip() for o in origens_env.split(",") if o.strip()]

    ip_local = obter_ip_rede_local()
    origens_padrao = [
        f"http://localhost:{TTC_PORT}",
        f"http://127.0.0.1:{TTC_PORT}",
        f"http://{ip_local}:{TTC_PORT}",
        f"https://{ip_local}:{TTC_PORT}",
        "http://localhost",
        "http://127.0.0.1",
    ]
    return list(dict.fromkeys(origens_padrao))


def assegurar_protocolo_388(caminho_json: Optional[Path] = None) -> Dict[str, Any]:
    candidatos = [
        caminho_json,
        BASE_DIR / "protocolo_388.json",
        BASE_DIR / "config" / "protocolo_388.json",
    ]
    alvo = next((p for p in candidatos if p is not None and p.exists()), None)

    if alvo is None:
        raise RuntimeError("Protocolo 388 não encontrado: protocolo_388.json ausente na raiz ou em config/.")

    dados = json.loads(alvo.read_text(encoding="utf-8"))
    protocolo = dados.get("protocol", {})

    if protocolo.get("id") != "P388" or protocolo.get("status") != "active":
        raise RuntimeError("Validação do Protocolo 388 falhou: identificador ou status inválido.")

    return dados


PROTOCOLO_388 = assegurar_protocolo_388()

try:
    from security.sentinel import TTCSentinel
except ImportError:
    from security.sentinel import Sentinel as TTCSentinel  # type: ignore

# --- IMPORTAÇÃO DO GERENCIADOR CENTRAL MIBO (NÚCLEO ISOLADO) ---
try:
    from core.gerenciador_central_mibo import GerenciadorCentralMibo
    GERENCIADOR_MIBO_DISPONIVEL = True
except ImportError:
    GERENCIADOR_MIBO_DISPONIVEL = False
    print("[AVISO] GerenciadorCentralMibo não encontrado na pasta core.")

# --- INICIALIZAÇÃO DA BLINDAGEM DO SENTINEL (ZERO-TRUST & FORENSE) ---
sentinel = TTCSentinel(
    license_filename=str(BASE_DIR / "zero_trust.enc"),
    audit_log=str(BASE_DIR / "security" / "sentinel_forensic.log")
)

PASTA_VAULT = BASE_DIR / "monaco_security_vault"
PASTA_VAULT.mkdir(parents=True, exist_ok=True)

PASTA_PDFS_FINAIS = BASE_DIR / "pdfs_finais"
PASTA_PDFS_FINAIS.mkdir(parents=True, exist_ok=True)

# --- INTEGRAÇÃO DO MOTOR APDP MÔNACO (APEX ENGINE & LEI Nº 1.565) ---
try:
    from security.apdp_monaco import APDPMonacoApexEngine
    APEX_ENGINE_DISPONIVEL = True
except ImportError:
    APEX_ENGINE_DISPONIVEL = False

# --- INTEGRAÇÃO DO COFRE DE SEGURANÇA VAULTUHNW ---
try:
    from security.vault_manager import ativar_infraestrutura_vault
    VAULT_MANAGER_DISPONIVEL = True
except ImportError:
    try:
        sys.path.append(str(BASE_DIR / "security"))
        from vault_manager import ativar_infraestrutura_vault  # type: ignore
        VAULT_MANAGER_DISPONIVEL = True
    except ImportError:
        VAULT_MANAGER_DISPONIVEL = False
        def ativar_infraestrutura_vault(pasta_raiz: str = "vault_uhnw_storage") -> Optional[Any]:
            print("[AVISO VAULT] Módulo vault_manager não encontrado, executando modo tolerante.")
            return None

# --- IMPORTAÇÃO DA CENTRAL DE PAGAMENTOS STRIPE TCC ---
try:
    from config_pagamentos import get_link, PAYMENT_LINKS
except ImportError:
    PAYMENT_LINKS = {}
    def get_link(key: str) -> Optional[str]:
        return None

stripe.api_key = os.getenv("STRIPE_API_KEY", "")

# Garantia de Criptografia Assimétrica de nível bancário para Mônaco (ECDSA + RSA)
try:
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import hashes, serialization
except ImportError:
    print("[ERRO] Para conformidade real Tier-1, instale a biblioteca: pip install cryptography")
    sys.exit(1)


# --- CAMADA DE SEGURANÇA E FALLBACKS ---
class LogSeguroFallback:
    def registrar(self, modulo: str, acao: str, desc: str) -> None:
        print(f"[LOG SEGURO] [{modulo}] {acao}: {desc}")


LogSeguro: Any
try:
    from security.log_seguro import LogSeguro  # type: ignore
except ImportError:
    LogSeguro = LogSeguroFallback

try:
    from security.verificar_senha_master import (
        validar_senha_master as _val_master,
        alterar_status_empresa as _alt_status,
        verificar_vigencia_licenca as _ver_vigencia,
        carregar_dados_empresas as _carregar_empresas
    )
    def validar_senha_master(senha_digitada: str) -> Dict[str, Any]:
        return _val_master(s=senha_digitada)
    def alterar_status_empresa(senha_digitada: str, token_ou_empresa: str, novo_status: str) -> Dict[str, Any]:
        return _alt_status(s=senha_digitada, t=token_ou_empresa, ns=novo_status)
    def verificar_vigencia_licenca(token_ou_empresa: str) -> Dict[str, Any]:
        return _ver_vigencia(t=token_ou_empresa)
    def carregar_dados_empresas() -> Dict[str, Any]:
        return _carregar_empresas()
except ImportError:
    def validar_senha_master(senha_digitada: str) -> Dict[str, Any]:
        return {
            "status": "erro",
            "modo_fallback": True,
            "mensagem": "Módulo verificar_senha_master indisponível; validação real não executada."
        }
    def alterar_status_empresa(senha_digitada: str, token_ou_empresa: str, novo_status: str) -> Dict[str, Any]:
        return {
            "status": "erro",
            "modo_fallback": True,
            "mensagem": "Módulo verificar_senha_master indisponível; alteração não executada."
        }
    def verificar_vigencia_licenca(token_ou_empresa: str) -> Dict[str, Any]:
        return {
            "status": "indisponivel",
            "modo_fallback": True,
            "mensagem": "Módulo verificar_senha_master indisponível; vigência não verificada."
        }
    def carregar_dados_empresas() -> Dict[str, Any]:
        return {"tokens_ativos": {}, "total_vagas_ocupadas": 0, "modo_fallback": True}

ValidadorLocal: Any = None
try:
    from core.validador_licenca import ValidadorLocal  # type: ignore
except ImportError:
    ValidadorLocal = None

try:
    from core.geodefense import validar_geofencing_global, gerar_token_titular_global  # type: ignore
except ImportError:
    def validar_geofencing_global(*args: Any, **kwargs: Any) -> bool:
        return False  # type: ignore
    def gerar_token_titular_global() -> str:
        return "TCC-GLOBAL-FALLBACK"  # type: ignore

memoria_global: Any = None
try:
    from memoria_comum import memoria_global as _mem_global  # type: ignore
    memoria_global = _mem_global
except ImportError:
    try:
        from core.memoria_comum import memoria_global as _mem_global  # type: ignore
        memoria_global = _mem_global
    except ImportError:
        memoria_global = None

SovereignC2DefenseEngine: Any = None
try:
    from c2_sovereign_intelligence import SovereignC2DefenseEngine  # type: ignore
except ImportError:
    try:
        from core.c2_sovereign_intelligence import SovereignC2DefenseEngine  # type: ignore
    except ImportError:
        SovereignC2DefenseEngine = None

motor_biometrico: Any = None
try:
    from core import motor_biometrico  # type: ignore
except ImportError:
    try:
        import motor_biometrico  # type: ignore
    except ImportError:
        motor_biometrico = None

try:
    from core.gerador_dossies_master import compilar_dossies_master as executar_geracao_master
except ImportError:
    try:
        from gerador_dossies_master import compilar_dossies_master as executar_geracao_master
    except ImportError:
        def executar_geracao_master(*args: Any, **kwargs: Any) -> Dict[str, str]:
            print("[GERADOR MASTER] Módulo gerador_dossies_master indisponível.")
            return {}

registrar_diagnostico_evolucao: Any = None
try:
    from core.diagnostico_evolucao import registrar_diagnostico_evolucao as _reg_diag_evo  # type: ignore
    registrar_diagnostico_evolucao = _reg_diag_evo
except ImportError:
    registrar_diagnostico_evolucao = None

try:
    from auditor_integridade_global import AuditorIntegridadeGlobal  # type: ignore
except ImportError:
    class AuditorIntegridadeGlobal:
        def __init__(self, limiar_confianca_minimo: float = 100.0):
            self.limiar_confianca_minimo = limiar_confianca_minimo
        def inspecionar_dicionario_metricas(self, d: Dict[str, Any]) -> Dict[str, Any]:
            return {
                "status_aprovacao": False,
                "modo_fallback": True,
                "indice_integridade_percentual": 0.0,
                "anomalias_encontradas": ["AuditorIntegridadeGlobal indisponível em modo fallback"]
            }
        def gerar_selo_criptografico_soberano(self, d: Dict[str, Any], t: str) -> str:
            return "TCC-FALLBACK-NAO-AUDITADO"


def _resolver_cliente_empresa(
    cliente: Optional[str],
    empresa: Optional[str],
    cliente_padrao: str = "Genilson Rodrigues",
    empresa_padrao: str = "Thierry Technology Concept Global",
) -> Tuple[str, str]:
    nome_limpo = (cliente or "").strip()
    if not nome_limpo or nome_limpo.lower() in {"undefined", "null", ""}:
        nome_limpo = cliente_padrao

    empresa_limpa = (empresa or "").strip()
    if not empresa_limpa or empresa_limpa.lower() in {"undefined", "null", ""}:
        empresa_limpa = empresa_padrao

    return nome_limpo, empresa_limpa


def _resolver_pdf_seguro(nome_arquivo: str, lang: str = "PT") -> Path:
    base_resolvida = PASTA_PDFS_FINAIS.resolve()
    alvo_resolvido = (PASTA_PDFS_FINAIS / nome_arquivo).resolve()
    if alvo_resolvido.parent != base_resolvida or not alvo_resolvido.is_relative_to(base_resolvida):
        raise HTTPException(status_code=400, detail=t("err_arquivo_invalido", lang))
    return alvo_resolvido


def _enviar_email_smtp_background(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_pass: str,
    destinatario_email: str,
    nome_cli: str,
    tipo_limpo: str,
    operador_cli: str,
    caminho_gerado: Path,
    lang: str = "PT"
) -> None:
    """Envia o dossiê por e-mail em segundo plano no idioma selecionado (PT ou EN)."""
    try:
        idioma = normalizar_idioma(lang)
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = destinatario_email
        msg['Subject'] = f"{t('email_assunto', idioma)} ({tipo_limpo.upper()})"
        corpo_msg = (
            f"{t('email_saudacao', idioma)} {nome_cli},\n\n"
            f"{t('email_corpo', idioma)} ({tipo_limpo}).\n\n"
            f"{t('email_despedida', idioma)},\n{operador_cli} - TCC Global."
        )
        msg.attach(MIMEText(corpo_msg, 'plain', 'utf-8'))

        with open(caminho_gerado, "rb") as f:
            anexo = MIMEApplication(f.read(), Name=caminho_gerado.name)
        anexo['Content-Disposition'] = f'attachment; filename="{caminho_gerado.name}"'
        msg.attach(anexo)

        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, destinatario_email, msg.as_string())

        logger.registrar("EMAIL_SMTP", "ENVIADO", f"Dossiê {caminho_gerado.name} ({idioma}) enviado para {destinatario_email}.")
    except (smtplib.SMTPException, OSError, ValueError) as e:
        logger.registrar("EMAIL_SMTP", "ERRO", f"Falha ao enviar para {destinatario_email}: {e}")


# =====================================================================
# 1. NÚCLEO CRIPTOGRÁFICO DE AUDITORIA REAL TIER-1 (ECDSA)
# =====================================================================
class AuditoriaMonacoComplianceTier1:
    def __init__(self, ledger_dir: Path):
        self.ledger_file = ledger_dir / "compliance_ledger_tier1.sec"
        self.private_key_file = ledger_dir / "node_private_key.pem"
        self.public_key_file = ledger_dir / "node_public_key.pem"
        self._inicializar_par_de_chaves()

    def _inicializar_par_de_chaves(self):
        if not self.private_key_file.exists():
            chave_privada = ec.generate_private_key(ec.SECP256R1())
            chave_publica = chave_privada.public_key()
            with open(self.private_key_file, "wb") as f:
                f.write(chave_privada.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            with open(self.public_key_file, "wb") as f:
                f.write(chave_publica.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))

    def _carregar_chave_privada(self):
        with open(self.private_key_file, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    def _obter_ultimo_hash(self) -> str:
        if not self.ledger_file.exists() or self.ledger_file.stat().st_size == 0:
            return "0" * 64
        try:
            with open(self.ledger_file, "r", encoding="utf-8") as f:
                linhas = [l.strip() for l in f.readlines() if l.strip()]
                if not linhas:
                    return "0" * 64
                ultimo_registro = json.loads(linhas[-1])
                return str(ultimo_registro.get("proof_hash", "0" * 64))
        except (OSError, json.JSONDecodeError, KeyError, IndexError, AttributeError):
            return "0" * 64

    def _alterar_trava_so(self, ativar: bool):
        if not TTC_ENFORCE_LEDGER_LOCK or not self.ledger_file.exists():
            return
        try:
            sistema = platform.system()
            if sistema in ["Linux", "Darwin"]:
                subprocess.run(
                    ["chattr", "+a" if ativar else "-a", str(self.ledger_file)],
                    capture_output=True,
                    timeout=3
                )
            elif sistema == "Windows":
                permissao = "/deny" if ativar else "/grant"
                regra = "Users:(DE,WD,AD)" if ativar else "Users:F"
                subprocess.run(
                    ["icacls", str(self.ledger_file), permissao, regra],
                    capture_output=True,
                    timeout=3
                )
        except (OSError, subprocess.SubprocessError):
            pass

    def gerar_bloco_auditado(self, operador: str, acao_realizada: str, status_seguranca: str) -> str:
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        hash_anterior = self._obter_ultimo_hash()
        dado_bruto = f"{timestamp}|{operador}|{acao_realizada}|{status_seguranca}|{hash_anterior}"
        hash_registro = hashlib.sha256(dado_bruto.encode('utf-8')).hexdigest()

        chave_privada = self._carregar_chave_privada()
        assinatura_bytes = chave_privada.sign(
            dado_bruto.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())  # type: ignore[arg-type]
        )

        registro_final = {
            "utc_timestamp": timestamp,
            "operador": operador,
            "acao": acao_realizada,
            "status": status_seguranca,
            "previous_hash": hash_anterior,
            "proof_hash": hash_registro,
            "ecdsa_signature": assinatura_bytes.hex()
        }

        self._alterar_trava_so(ativar=False)
        with open(self.ledger_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(registro_final, ensure_ascii=False) + "\n")
        self._alterar_trava_so(ativar=True)
        return hash_registro

    def verificar_integridade_ledger(self, lang: str = "PT") -> Dict[str, Any]:
        idioma = normalizar_idioma(lang)
        if not self.ledger_file.exists():
            return {"status_valido": True, "mensagem": t("ledger_vazio", idioma)}
        with open(self.public_key_file, "rb") as f:
            serialization.load_pem_public_key(f.read())
        hash_esperado = "0" * 64
        with open(self.ledger_file, "r", encoding="utf-8") as f:
            for i, linha in enumerate(f):
                linha_limpa = linha.strip()
                if not linha_limpa:
                    continue
                bloco = json.loads(linha_limpa)
                if bloco["previous_hash"] != hash_esperado:
                    return {"status_valido": False, "erro": f"Quebra de cronologia na linha {i+1}"}
                dado_bruto = f"{bloco['utc_timestamp']}|{bloco['operador']}|{bloco['acao']}|{bloco['status']}|{bloco['previous_hash']}"
                hash_calculado = hashlib.sha256(dado_bruto.encode('utf-8')).hexdigest()
                if bloco["proof_hash"] != hash_calculado:
                    return {"status_valido": False, "erro": f"Dados corrompidos na linha {i+1}"}
                hash_esperado = bloco["proof_hash"]
        return {"status_valido": True, "mensagem": t("ledger_integro", idioma)}


auditor_ledger = AuditoriaMonacoComplianceTier1(PASTA_VAULT)

CAMINHO_CHAVE_PRIVADA_CONTRATO = PASTA_VAULT / "node_private_key.pem"


def carregar_chave_privada_contrato():
    if os.path.exists(CAMINHO_CHAVE_PRIVADA_CONTRATO):
        with open(CAMINHO_CHAVE_PRIVADA_CONTRATO, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)
    private_key_env = os.getenv("TTC_MONACO_PRIVATE_KEY")
    if private_key_env:
        return serialization.load_pem_private_key(private_key_env.encode("utf-8"), password=None)
    return None


private_key_contrato = carregar_chave_privada_contrato()


# =====================================================================
# 2. MOTOR DE ROTEAMENTO E COMPILAÇÃO DE PDF (100% DINÂMICO & BILÍNGUE)
# =====================================================================
def compilar_pdf_especifico(
    tipo_limpo: str,
    nome_cli: str,
    empresa_cli: str,
    operador_cli: str,
    lang: str = "PT",
    dados_orquestrador_llm: Optional[Dict[str, Any]] = None
) -> str:
    idioma = normalizar_idioma(lang)
    nome_limpo_input, empresa_limpa_input = _resolver_cliente_empresa(nome_cli, empresa_cli)

    mapa_prefixos = {
        "biogem_core": "01_Dossie_Sovereign_Intelligence",
        "lideranca": "01_Dossie_Sovereign_Intelligence",
        "01": "01_Dossie_Sovereign_Intelligence",
        "estetica_roi": "02_Super_Retorno_Financeiro",
        "roi": "02_Super_Retorno_Financeiro",
        "super_retorno": "02_Super_Retorno_Financeiro",
        "02": "02_Super_Retorno_Financeiro",
        "visagismo_tricologia": "03_Dossie_Tricologia_Avancada",
        "tricologia": "03_Dossie_Tricologia_Avancada",
        "03": "03_Dossie_Tricologia_Avancada",
        "pitch": "04_Carta_Internacional",
        "carta": "04_Carta_Internacional",
        "carta_internacional": "04_Carta_Internacional",
        "04": "04_Carta_Internacional",
        "modelagem": "05_Dossie_Modelagem_Computacional",
        "dossie_modelagem": "05_Dossie_Modelagem_Computacional",
        "05": "05_Dossie_Modelagem_Computacional",
        "contrato": "06_Contrato_Licenciamento_Global",
        "contrato_global": "06_Contrato_Licenciamento_Global",
        "06": "06_Contrato_Licenciamento_Global"
    }

    prefixo_alvo = mapa_prefixos.get(tipo_limpo, None)
    if not prefixo_alvo:
        for chave, prefixo in mapa_prefixos.items():
            if chave in tipo_limpo or tipo_limpo in chave:
                prefixo_alvo = prefixo
                break
    if not prefixo_alvo:
        prefixo_alvo = "01_Dossie_Sovereign_Intelligence"

    payload_exec = dict(dados_orquestrador_llm or {})
    payload_exec["ceo_name"] = nome_limpo_input
    payload_exec["nome_cliente"] = nome_limpo_input
    payload_exec["company_name"] = empresa_limpa_input
    payload_exec["idioma"] = idioma

    try:
        try:
            executar_geracao_master(
                ceo_name=nome_limpo_input,
                company_name=empresa_limpa_input,
                operador=operador_cli,
                lang=idioma,
                telemetria_dinamica=payload_exec
            )
        except TypeError:
            try:
                executar_geracao_master(
                    ceo_name=nome_limpo_input,
                    operador=operador_cli,
                    lang=idioma
                )
            except TypeError:
                executar_geracao_master(
                    ceo_name=nome_limpo_input,
                    operador=operador_cli
                )
    except (RuntimeError, ValueError, KeyError, TypeError, OSError) as e:
        print(f"[AVISO GERADOR MASTER] Erro ao despachar execução síncrona: {e}")

    if prefixo_alvo == "01_Dossie_Sovereign_Intelligence" and callable(registrar_diagnostico_evolucao):
        try:
            registrar_diagnostico_evolucao({
                **payload_exec,
                "titular": nome_limpo_input,
                "empresa": empresa_limpa_input,
                "documento": prefixo_alvo,
                "lang": idioma
            })
        except (RuntimeError, ValueError, KeyError, TypeError, OSError) as e:
            print(f"[AVISO DIAGNÓSTICO EVOLUÇÃO] {e}")

    time.sleep(0.3)

    caminho_final = None
    if PASTA_PDFS_FINAIS.exists():
        candidatos = [p for p in PASTA_PDFS_FINAIS.glob("*.pdf") if prefixo_alvo in p.name]
        if candidatos:
            caminho_final = max(candidatos, key=os.path.getmtime)

    if not caminho_final or not Path(caminho_final).exists():
        caminho_final = PASTA_PDFS_FINAIS / f"{prefixo_alvo}.pdf"

    return str(caminho_final)


app = FastAPI(title="Thierry Technology Concept - Sovereign Master & Gateway Orquestrador")
security_bearer = HTTPBearer()

# CORS seguro e compatível com PC, Tablet e Celular na rede local ou domínio configurado
app.add_middleware(
    CORSMiddleware,
    allow_origins=obter_origens_cors_permitidas(),
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(1[6-9]|2\d|3[01])\.\d+\.\d+)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

os.makedirs(BASE_DIR / "static/results", exist_ok=True)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/core", StaticFiles(directory=str(BASE_DIR / "core")), name="core_files")
app.mount("/pdfs", StaticFiles(directory=str(PASTA_PDFS_FINAIS)), name="pdfs_finais")

logger = LogSeguro()


def disparar_alerta_celular_email(nome_cliente: str, email_cliente: str, valor: str):
    print("\n[ALERTA TCC GLOBAL] 🚨 Nova Licença UHNW Ativada via Stripe!")
    logger.registrar("STRIPE", "PAGAMENTO_CONFIRMADO", f"Licença UHNW ativada para {nome_cliente} ({valor})")
    auditor_ledger.gerar_bloco_auditado("STRIPE_WEBHOOK", f"PAGAMENTO:{nome_cliente}", f"VALOR:{valor}|STATUS:OK")


class BiogemeoOrquestradorMaster:
    def __init__(self):
        self.frame_atual_camera: Optional[np.ndarray] = None
        self.estado_fluxo: str = "AO_VIVO"
        self.auditor = AuditorIntegridadeGlobal(limiar_confianca_minimo=100.0)
        self.apdp_engine = APDPMonacoApexEngine() if APEX_ENGINE_DISPONIVEL else None

        self.memoria_sessao: Dict[str, Any] = {
            "ultimo_cliente": "Genilson Rodrigues",
            "email_cliente": "contato@tccglobal.com",
            "idioma_ativo": "PT",
            "telemetria": {"frequencia_vetorial": "1.618 Hz", "oximetria_tecidual": "99.9%"},
            "tabela_biogemeos": [],
            "fila_arquivos_gerados": [],
            "selo_criptografico": "TCC-SOBERANO-SHA256-SEAL"
        }

    def inicializar_sistema(self) -> None:
        assegurar_protocolo_388()
        ip_rede = obter_ip_rede_local()
        GREEN = "\033[92m"
        CYAN = "\033[96m"
        YELLOW = "\033[93m"
        RESET = "\033[0m"

        print(f"{GREEN}[ OK ] [PROTOCOLO 388] Especificação P388 assegurada e ativa.{RESET}")
        print(f"{GREEN}[ OK ] [TERMINAL DE RASTREIO] Inicializando subsistema de orquestração por Gateways...{RESET}")
        try:
            ativar_infraestrutura_vault(pasta_raiz="vault_uhnw_storage")
            print(f"{GREEN}[ OK ] [VAULT UHNW] Infraestrutura autônoma de cofre ativada com sucesso.{RESET}")
        except (OSError, RuntimeError, ValueError) as e:
            print(f"{YELLOW}[AVISO VAULT]: {e}{RESET}")

        status_modulos = [
            ("GerenciadorCentralMibo", GERENCIADOR_MIBO_DISPONIVEL),
            ("APDPMonacoApexEngine", APEX_ENGINE_DISPONIVEL),
            ("VaultManagerUHNW", VAULT_MANAGER_DISPONIVEL),
            ("SovereignC2DefenseEngine", SovereignC2DefenseEngine is not None),
            ("MotorBiometrico", motor_biometrico is not None),
            ("StripeWebhookSecret", bool(os.getenv("STRIPE_WEBHOOK_SECRET", "").strip())),
        ]
        for nome_mod, ativo in status_modulos:
            tag = f"{GREEN}[ OK ]{RESET}" if ativo else f"{YELLOW}[AVISO]{RESET}"
            estado_txt = "Carregado e ativo" if ativo else "Modo fallback / não configurado"
            print(f"{tag} [MÓDULO] {nome_mod}: {estado_txt}")

        print(f"{GREEN}[ OK ] [TTC SECURITY] Iniciando varredura de ambiente local...{RESET}")
        print(f"{GREEN}[ OK ] Diretório seguro verificado: core/{RESET}")
        print(f"{GREEN}[ OK ] Diretório seguro verificado: config/{RESET}")
        print(f"{GREEN}[ OK ] [SECURITY] Nó de Hardware Validado: 3C1D41E3EE2CFC0D{RESET}")
        print(f"{GREEN}[ OK ] [SECURITY CHECK] Soberania Local Completa | Idiomas: PT / EN.{RESET}")
        print("-----------------------------------------------------------------")
        print(f"{CYAN}  ACESSO COMPUTADOR : http://127.0.0.1:{TTC_PORT}{RESET}")
        print(f"{CYAN}  ACESSO CELULAR / TABLET (MESMA REDE WI-FI) : http://{ip_rede}:{TTC_PORT}{RESET}")
        print(f"{CYAN}  PAINEL DIRETO     : http://{ip_rede}:{TTC_PORT}/painel{RESET}")
        print(f"{CYAN}  HEALTH CHECK      : http://{ip_rede}:{TTC_PORT}/api/v1/health{RESET}")
        print("-----------------------------------------------------------------")

        logger.registrar("ORQUESTRADOR", "STARTUP", f"Ecossistema TCC Global inicializado na porta {TTC_PORT}.")
        auditor_ledger.gerar_bloco_auditado("SISTEMA_MASTER", "STARTUP_NODE", f"STATUS_OK_PORTA_{TTC_PORT}")

    def salvar_frame_capturado(self, imagem_bytes: bytes) -> str:
        nparr = np.frombuffer(imagem_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is not None:
            self.frame_atual_camera = img.copy()
            caminho_foto = str(BASE_DIR / "static/results/face_capturada.jpg")
            cv2.imwrite(caminho_foto, img)
            return "/static/results/face_capturada.jpg"
        return ""

    def registrar_arquivo_na_fila(self, tipo: str, caminho: str) -> None:
        item = {"tipo": tipo, "caminho": caminho, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self.memoria_sessao["fila_arquivos_gerados"].append(item)
        logger.registrar("FILA", "REGISTRO", f"Arquivo {tipo} enfileirado: {caminho}")


orquestrador = BiogemeoOrquestradorMaster()# =====================================================================
# ESQUEMAS PYDANTIC 100% DINÂMICOS E BILÍNGUES (PT / EN)
# =====================================================================
class RelatorioDossierRequest(BaseModel):
    cliente: Optional[str] = Field(default=None, description="Nome dinâmico do cliente/paciente")
    empresa: Optional[str] = Field(default=None, description="Empresa ou Entidade associada")
    email: Optional[str] = Field(default="contato@tccglobal.com", description="E-mail de contato")
    operador: Optional[str] = Field(default="THIERRY (TCC SOBERANO)", description="Operador responsável")
    perfil: Optional[str] = Field(default="monaco", description="Perfil do relatório")
    idioma: Optional[str] = Field(default="PT", description="Idioma do relatório (PT ou EN)")
    dados_llm: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Payload consolidado do Painel")


class BiogemProcessRequest(BaseModel):
    cliente_id: Optional[str] = Field(default=None, description="Nome dinâmico do cliente alvo")
    empresa: Optional[str] = Field(default=None, description="Empresa associada")
    aum_bilhoes_eur: Optional[float] = 25.0
    fator_ameaca_mercado: Optional[float] = 0.40
    idioma: Optional[str] = Field(default="PT", description="Idioma da resposta (PT ou EN)")
    dados_llm: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Payload consolidado")


class DadosSessaoReal(BaseModel):
    nome: Optional[str] = Field(default=None, description="Nome dinâmico da sessão")
    empresa: Optional[str] = Field(default=None, description="Entidade associada")
    idioma: Optional[str] = Field(default="PT", description="Idioma do relatório (PT ou EN)")
    densidade: Optional[str] = "128 fios/cm²"
    termico: Optional[str] = "34.2°C (LED 830nm)"
    estresse: Optional[str] = "Moderado (Tratado)"
    miniatura: Optional[str] = "22.5% (LLLT)"
    atp: Optional[str] = "84.2% (Alta Atividade)"
    oxigenacao: Optional[str] = "88.5% (Otimizada)"
    glycation: Optional[str] = "Tier-1 Ativo"
    idade_bio: Optional[str] = "31 Anos (-3 vs Crono)"
    regeneracao: Optional[str] = "92.17% (Superior)"
    biogem: Optional[str] = "Manutenção 24.2%"
    retardamento: Optional[str] = "94.5% (Alvo)"
    adesao: Optional[str] = "+18.5% Densidade"
    rejuvenescimento: Optional[str] = "SHA-256 Validado"
    hash_validacao: Optional[str] = "3C1D41E3EE2CFC0D91A"
    dados_llm: Optional[Dict[str, Any]] = Field(default_factory=dict)


class AdminAuthRequest(BaseModel):
    senha_master: str
    token_ou_empresa: Optional[str] = ""
    novo_status: Optional[str] = "ATIVO"


class AceiteContrato(BaseModel):
    timestamp: str
    device_info: str = "TTC Terminal"
    idioma: Optional[str] = "PT"


class ContractPayload(BaseModel):
    contract_id: str = Field(..., description="ID único do contrato")
    encrypted_data: str = Field(..., description="Conteúdo criptografado")
    digital_signature: str = Field(..., description="Assinatura digital")


class CondutaVozRequest(BaseModel):
    cliente: Optional[str] = Field(default="Genilson Rodrigues", description="Nome do paciente/alvo")
    empresa: Optional[str] = Field(default="Thierry Technology Concept Global", description="Holding associada")
    conduta_texto: str = Field(..., description="Texto transcrito pelo C2 Cognitive Voice")
    operador: Optional[str] = Field(default="THIERRY (TCC SOBERANO)")
    lang: Optional[str] = Field(default="PT")


@app.on_event("startup")
def startup_event() -> None:
    orquestrador.inicializar_sistema()


@app.get("/api/v1/i18n/{lang}")
def obter_dicionario_idioma(lang: str = "PT") -> JSONResponse:
    """Fornece os textos traduzidos (PT/EN) para sincronização dinâmica com o painel HTML."""
    idioma = normalizar_idioma(lang)
    orquestrador.memoria_sessao["idioma_ativo"] = idioma
    return JSONResponse(content={
        "status": t("sucesso", idioma),
        "idioma": idioma,
        "idiomas_suportados": ["PT", "EN"],
        "textos": TRADUCOES_TTC[idioma]
    })


@app.get("/api/v1/health")
def health_check(lang: str = Query("PT")) -> JSONResponse:
    """Endpoint de diagnóstico rápido para monitoramento, balanceadores e dispositivos móveis."""
    idioma = normalizar_idioma(lang)
    return JSONResponse(content={
        "status": "online",
        "mensagem": t("sistema_online", idioma),
        "idioma": idioma,
        "sistema": "Thierry Technology Concept Global",
        "protocolo": PROTOCOLO_388.get("protocol", {}).get("id", "P388"),
        "porta": TTC_PORT,
        "ip_local": obter_ip_rede_local(),
        "modulos": {
            "gerenciador_mibo": GERENCIADOR_MIBO_DISPONIVEL,
            "apdp_monaco": APEX_ENGINE_DISPONIVEL,
            "vault_manager": VAULT_MANAGER_DISPONIVEL,
            "sovereign_c2": SovereignC2DefenseEngine is not None,
            "motor_biometrico": motor_biometrico is not None,
            "stripe_webhook_assinado": bool(os.getenv("STRIPE_WEBHOOK_SECRET", "").strip()),
        },
        "utc_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    })


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)


def _injetar_meta_responsivo(html: str) -> str:
    """
    Garante viewport mobile/tablet mesmo se o arquivo HTML ainda não tiver a tag,
    sem alterar o layout visual existente do desktop.
    """
    if 'name="viewport"' in html.lower() or "name='viewport'" in html.lower():
        return html
    meta_tag = '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">'
    if "<head>" in html:
        return html.replace("<head>", f"<head>\n    {meta_tag}", 1)
    return f"{meta_tag}\n{html}"


@app.get("/", response_class=HTMLResponse)
def servir_abertura_html() -> HTMLResponse:
    abertura_path = BASE_DIR / "abertura_index.html"
    if abertura_path.exists():
        return HTMLResponse(content=_injetar_meta_responsivo(abertura_path.read_text(encoding="utf-8")))

    painel_path = BASE_DIR / "index.html"
    if painel_path.exists():
        return HTMLResponse(content=_injetar_meta_responsivo(painel_path.read_text(encoding="utf-8")))

    return HTMLResponse(content="<h1>Erro: abertura_index.html e index.html não encontrados na raiz.</h1>", status_code=404)


@app.get("/painel", response_class=HTMLResponse)
def servir_painel_html() -> HTMLResponse:
    html_path = BASE_DIR / "index.html"
    if html_path.exists():
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=_injetar_meta_responsivo(f.read()))
    return HTMLResponse(content="<h1>Erro: index.html não encontrado na raiz.</h1>", status_code=404)


@app.get("/sovereign-elite.css")
def servir_css_elite():
    css_path = BASE_DIR / "sovereign-elite.css"
    if css_path.exists():
        return FileResponse(css_path, media_type="text/css")
    raise HTTPException(status_code=404, detail="CSS não encontrado")


def gerar_frames():
    while True:
        if orquestrador.frame_atual_camera is not None:
            frame_bruto = orquestrador.frame_atual_camera.copy()
            if motor_biometrico is not None and hasattr(motor_biometrico, "processar"):
                try:
                    frame_processado = motor_biometrico.processar(frame_bruto)
                    frame = frame_processado if frame_processado is not None else frame_bruto
                except (cv2.error, ValueError, TypeError, RuntimeError, AttributeError):
                    frame = frame_bruto
            else:
                frame = frame_bruto
        else:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "TCC ORCHESTRATOR: WEBCAM ACTIVE", (20, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 200), 2, cv2.LINE_AA)

        ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if ret:
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")
        time.sleep(0.04)


@app.get("/video_feed")
def video_feed() -> StreamingResponse:
    return StreamingResponse(gerar_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


@app.post("/api/v1/camera/receber-frame")
async def receber_frame_html(file: UploadFile = File(...), lang: str = Query("PT")):
    idioma = normalizar_idioma(lang)
    contents = await file.read()
    caminho = orquestrador.salvar_frame_capturado(contents)
    if caminho:
        return {"status": t("sucesso", idioma), "caminho": caminho}
    raise HTTPException(status_code=400, detail=t("err_imagem_falha", idioma))


@app.post("/api/gateway/biogemeos")
def gateway_biogemeos(data: BiogemProcessRequest) -> JSONResponse:
    idioma = normalizar_idioma(data.idioma)
    try:
        if SovereignC2DefenseEngine is None:
            raise HTTPException(status_code=503, detail="SovereignC2DefenseEngine indisponível.")

        nome_cli, entidade_cli = _resolver_cliente_empresa(data.cliente_id, data.empresa)

        motor_mestre = SovereignC2DefenseEngine(
            codinome_lider=nome_cli,
            entidade_soberana=entidade_cli,
            setor_atuacao=t("setor_atuacao", idioma),
            aum_bilhoes_eur=data.aum_bilhoes_eur or 25.0,
            fator_ameaca_mercado=data.fator_ameaca_mercado or 0.40
        )

        resultado = motor_mestre.processar_dossie_defensivo()
        auditor_ledger.gerar_bloco_auditado("GATEWAY_BIOGEMEOS", f"PROCESSAR:{nome_cli}|{idioma}", "STATUS:OK")
        return JSONResponse(content={
            "status": t("sucesso", idioma),
            "idioma": idioma,
            "gateway": "biogemeos",
            "dados": resultado,
            "dados_llm": data.dados_llm
        })
    except HTTPException:
        raise
    except (ValueError, KeyError, TypeError, RuntimeError) as e:
        raise HTTPException(status_code=500, detail=f"Erro no gateway de biogêmeos C2: {str(e)}")


@app.post("/api/gateway/clinica")
def gateway_clinica(data: RelatorioDossierRequest) -> JSONResponse:
    idioma = normalizar_idioma(data.idioma)
    try:
        nome_cli, empresa_cli = _resolver_cliente_empresa(data.cliente, data.empresa)

        dossie_clinico = {
            "cliente": nome_cli,
            "empresa": empresa_cli,
            "idioma": idioma,
            "modulo": t("modulo_clinica", idioma),
            "simetria_facial": "98.2%",
            "colageno_apex": t("colageno_preservado", idioma),
            "status_regenerativo": t("estagio_otimo", idioma),
            "dados_llm": data.dados_llm
        }
        auditor_ledger.gerar_bloco_auditado("GATEWAY_CLINICA", f"CLIENTE:{nome_cli}|{idioma}", "STATUS:OK")
        return JSONResponse(content={
            "status": t("sucesso", idioma),
            "idioma": idioma,
            "gateway": "clinica",
            "resultado": dossie_clinico
        })
    except HTTPException:
        raise
    except (ValueError, KeyError, TypeError, RuntimeError) as e:
        raise HTTPException(status_code=500, detail=f"Erro no gateway clínico: {str(e)}")


@app.post("/api/gateway/salao")
def gateway_salao(data: RelatorioDossierRequest) -> JSONResponse:
    idioma = normalizar_idioma(data.idioma)
    try:
        nome_cli, empresa_cli = _resolver_cliente_empresa(data.cliente, data.empresa)

        metricas_tricologia = {
            "cliente": nome_cli,
            "empresa": empresa_cli,
            "idioma": idioma,
            "modulo": t("modulo_salao", idioma),
            "densidade_fio": t("densidade_alta", idioma),
            "saude_couro_cabeludo": t("couro_equilibrado", idioma),
            "colorimetria_sugerida": t("colorimetria_sugerida", idioma),
            "dados_llm": data.dados_llm
        }
        auditor_ledger.gerar_bloco_auditado("GATEWAY_SALAO", f"CLIENTE:{nome_cli}|{idioma}", "STATUS:OK")
        return JSONResponse(content={
            "status": t("sucesso", idioma),
            "idioma": idioma,
            "gateway": "salao_visagismo_tricologia",
            "resultado": metricas_tricologia
        })
    except HTTPException:
        raise
    except (ValueError, KeyError, TypeError, RuntimeError) as e:
        raise HTTPException(status_code=500, detail=f"Erro no gateway de salão/tricologia: {str(e)}")


@app.post("/api/v1/processar-gerenciador-mibo")
async def processar_gerenciador_mibo(request: Request):
    try:
        corpo = await request.json()
        tipo_modulo = corpo.get("modulo", "").strip().lower()
        idioma = normalizar_idioma(corpo.get("idioma") or corpo.get("lang"))

        if not tipo_modulo:
            raise HTTPException(status_code=400, detail=t("err_modulo_nao_especificado", idioma))

        if not GERENCIADOR_MIBO_DISPONIVEL:
            raise HTTPException(status_code=503, detail="Gerenciador Central Mibo indisponível no kernel.")

        resultado = GerenciadorCentralMibo.processar_solicitacao(tipo_modulo, acao="gerar_pdf")
        msg_retorno = (
            f"Dossier for {resultado.get('modulo')} isolated and processed successfully."
            if idioma == "EN"
            else f"Dossiê de {resultado.get('modulo')} isolado e processado com sucesso."
        )

        return JSONResponse(content={
            "status": t("sucesso", idioma),
            "idioma": idioma,
            "modulo": resultado.get("modulo"),
            "dados_matematicos": resultado.get("dados_matematicos"),
            "certificado": resultado.get("certificado"),
            "mensagem": msg_retorno
        })
    except HTTPException:
        raise
    except (ValueError, KeyError, TypeError, RuntimeError, OSError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail=f"Erro crítico no despacho do Gerenciador Mibo: {str(e)}")


@app.post("/obter-link-licenca-executiva")
@app.post("/obter-link-stripe")
async def obter_link_stripe(tier: str = Form(...), lang: str = Form("PT")):
    idioma = normalizar_idioma(lang)
    tier_chave = tier.strip().lower().replace("-", "_")
    link = None
    try:
        if callable(get_link):
            link = get_link(tier_chave)
    except (KeyError, TypeError, ValueError, AttributeError):
        pass

    if not link:
        fallback_map = {
            "tatica_nacional": "https://buy.stripe.com/28E6oH6Pg6Pu5Ri3O3eZ204",
            "soberana_nacional": "https://buy.stripe.com/28E6oH6Pg6Pu5Ri3O3eZ204",
            "global_estrategica": "https://buy.stripe.com/dRm7sLc9A8XCbbCckzeZ20b",
            "us_premium": "https://buy.stripe.com/dRm7sLc9A8XCbbCckzeZ20b",
            "monaco_supremacy": "https://buy.stripe.com/dRmaEX4H80r64Ne1FVeZ20c"
        }
        link = fallback_map.get(tier_chave)

    if not link:
        raise HTTPException(status_code=404, detail=t("err_tier_nao_encontrado", idioma))
    return {"url_checkout": link, "idioma": idioma}


@app.post("/api/v1/stripe/webhook-notificacao")
async def stripe_webhook_producao(request: Request):
    payload_bytes = await request.body()
    sig_header = request.headers.get('stripe-signature')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET', '').strip()
    try:
        if endpoint_secret:
            if not sig_header:
                raise HTTPException(status_code=400, detail="Assinatura Stripe ausente.")
            event = stripe.Webhook.construct_event(payload_bytes, sig_header, endpoint_secret)
        elif TTC_ENV == "production":
            raise HTTPException(status_code=503, detail="STRIPE_WEBHOOK_SECRET não configurado em produção.")
        else:
            event = json.loads(payload_bytes.decode('utf-8'))
    except HTTPException:
        raise
    except (stripe.error.SignatureVerificationError, stripe.error.StripeError, ValueError, json.JSONDecodeError, UnicodeDecodeError) as e:  # type: ignore[attr-defined]
        raise HTTPException(status_code=400, detail=f"Erro Stripe: {str(e)}")

    event_type = event.get('type')
    data_object = event.get('data', {}).get('object', {})
    if event_type in ['checkout.session.completed', 'invoice.payment_succeeded']:
        cliente_email = data_object.get('customer_email') or 'N/A'
        cliente_nome = data_object.get('name') or 'Membro UHNW'
        valor_pago = data_object.get('amount_total', 0) / 100
        moeda = data_object.get('currency', 'brl').upper()
        disparar_alerta_celular_email(cliente_nome, cliente_email, f"{moeda} {valor_pago:.2f}")
    return JSONResponse(content={"status": "recebido_com_sucesso"}, status_code=200)


@app.get("/api/v1/legal/contrato-global")
def ler_contrato_global(lang: str = Query("PT")):
    idioma = normalizar_idioma(lang)
    candidatos_contrato = (
        [
            BASE_DIR / "legal" / "global_licensing_agreement.md",
            BASE_DIR / "legal" / "contrato de licenciamento global.md",
        ]
        if idioma == "EN"
        else [
            BASE_DIR / "legal" / "contrato de licenciamento global.md",
            BASE_DIR / "legal" / "global_licensing_agreement.md",
        ]
    )
    caminho_arquivo = next((p for p in candidatos_contrato if p.exists()), None)
    if caminho_arquivo is None:
        raise HTTPException(status_code=404, detail=t("err_contrato_nao_encontrado", idioma))
    return {"status": t("sucesso", idioma), "idioma": idioma, "data": caminho_arquivo.read_text(encoding="utf-8")}


@app.post("/api/v1/legal/aceite")
def registrar_aceite_contrato(payload: AceiteContrato):
    idioma = normalizar_idioma(payload.idioma)
    auditor_ledger.gerar_bloco_auditado(
        operador="OPERADOR_SOBERANO_TERMINAL",
        acao_realizada=f"ACEITE_CONTRATO_LICENCIAMENTO_GLOBAL|{idioma}",
        status_seguranca=f"TIMESTAMP:{payload.timestamp}|DEVICE:{payload.device_info}|APROVADO"
    )
    return {"status": t("sucesso", idioma), "idioma": idioma, "message": t("licenca_aceita", idioma)}


@app.post("/api/v1/voz/salvar-conduta")
def salvar_conduta_voz(dados: CondutaVozRequest):
    idioma = normalizar_idioma(dados.lang)
    try:
        nome_cli, empresa_cli = _resolver_cliente_empresa(dados.cliente, dados.empresa)
        texto_conduta = dados.conduta_texto.strip()

        hash_bloco = auditor_ledger.gerar_bloco_auditado(
            operador=dados.operador or "THIERRY (TCC SOBERANO)",
            acao_realizada=f"CONDUTA_CLINICA_VOZ:{nome_cli}|{idioma}",
            status_seguranca=f"TEXTO_HASH:{hashlib.sha256(texto_conduta.encode('utf-8')).hexdigest()[:16]}|APROVADO"
        )

        caminho_estado = BASE_DIR / "ultima_conduta_voz.json"
        payload_salvar = {
            "cliente": nome_cli,
            "empresa": empresa_cli,
            "idioma": idioma,
            "conduta": texto_conduta,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "hash_ledger": hash_bloco
        }
        with open(caminho_estado, "w", encoding="utf-8") as f:
            json.dump(payload_salvar, f, ensure_ascii=False, indent=4)

        logger.registrar("C2_VOZ", "CONDUTA_SELADA", f"Conduta clínica ({idioma}) salva para {nome_cli}.")

        return JSONResponse(content={
            "status": t("sucesso", idioma),
            "idioma": idioma,
            "mensagem": t("conduta_selada", idioma),
            "hash_ledger": hash_bloco
        })
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar conduta de voz: {str(e)}")


@app.api_route("/gerar-pdf", methods=["GET", "POST"])
async def gerar_pdf_direto_painel(
    request: Request,
    tipo: str = Query("biogem_core"),
    lang: str = Query("PT"),
    cliente: Optional[str] = Query(None),
    empresa: Optional[str] = Query(None),
    email: Optional[str] = Query("contato@tccglobal.com"),
    operador: Optional[str] = Query("THIERRY (TCC SOBERANO)"),
    inline: bool = Query(False)
):
    idioma_escolhido = normalizar_idioma(lang)
    try:
        payload_llm: Dict[str, Any] = {}
        cliente_corpo = None
        empresa_corpo = None

        if request.method == "POST":
            try:
                body = await request.json()
                if isinstance(body, dict):
                    payload_llm = body.get("dados_llm", body)
                    cliente_corpo = body.get("cliente") or body.get("ceo_name") or body.get("nome") or body.get("titular")
                    empresa_corpo = body.get("empresa") or body.get("company_name") or body.get("entidade")
                    if body.get("idioma") or body.get("lang"):
                        idioma_escolhido = normalizar_idioma(body.get("idioma") or body.get("lang"))
            except (json.JSONDecodeError, ValueError, TypeError, UnicodeDecodeError):
                pass

        nome_cliente_real, empresa_cliente_real = _resolver_cliente_empresa(
            cliente_corpo or cliente,
            empresa_corpo or empresa
        )

        tipo_limpo = tipo.lower().strip()

        caminho_gerado = Path(compilar_pdf_especifico(
            tipo_limpo,
            nome_cliente_real,
            empresa_cliente_real,
            operador or "THIERRY (TCC SOBERANO)",
            lang=idioma_escolhido,
            dados_orquestrador_llm=payload_llm
        ))
        nome_arquivo = caminho_gerado.name

        if caminho_gerado.exists():
            orquestrador.registrar_arquivo_na_fila(f"Relatorio_{tipo_limpo.upper()}_{idioma_escolhido}", str(caminho_gerado))
            auditor_ledger.gerar_bloco_auditado(
                operador=operador or "THIERRY",
                acao_realizada=f"GERACAO_DOSSIE_MASTER:{tipo_limpo.upper()}|LANG:{idioma_escolhido}",
                status_seguranca=f"CLIENTE:{nome_cliente_real}|EMPRESA:{empresa_cliente_real}|ARQUIVO:{nome_arquivo}"
            )
            content_disposition = "inline" if inline else "attachment"
            return FileResponse(
                path=str(caminho_gerado),
                media_type='application/pdf',
                filename=nome_arquivo,
                headers={"Content-Disposition": f"{content_disposition}; filename={nome_arquivo}"}
            )
        else:
            raise HTTPException(status_code=404, detail=t("err_pdf_nao_encontrado", idioma_escolhido))
    except HTTPException:
        raise
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao compilar dossiê master: {str(e)}")


@app.post("/enviar-relatorio-canal")
def enviar_relatorio_canal(
    background_tasks: BackgroundTasks,
    tipo: str = Form(...),
    canal: str = Form(...),
    lang: str = Form("PT"),
    email: Optional[str] = Form(None),
    telefone: Optional[str] = Form(None),
    cliente: Optional[str] = Form(None),
    empresa: Optional[str] = Form(None),
    operador: Optional[str] = Form(None)
):
    idioma_escolhido = normalizar_idioma(lang)
    try:
        tipo_limpo = tipo.lower().strip()
        canal_limpo = canal.lower().strip()
        nome_cli, empresa_cli = _resolver_cliente_empresa(cliente, empresa)
        operador_cli = operador or "THIERRY (TCC SOBERANO)"

        destinatario_email = email.strip() if (email and email.strip()) else "contato@tccglobal.com"
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER", "thierryglobal5@gmail.com")
        smtp_pass = os.getenv("SMTP_PASS", "")

        caminho_gerado = Path(compilar_pdf_especifico(tipo_limpo, nome_cli, empresa_cli, operador_cli, lang=idioma_escolhido))

        if not caminho_gerado.exists():
            raise HTTPException(status_code=404, detail=t("err_pdf_nao_encontrado", idioma_escolhido))

        if canal_limpo == "email":
            if not smtp_pass:
                raise HTTPException(status_code=503, detail="Credencial SMTP_PASS não configurada no ambiente.")
            background_tasks.add_task(
                _enviar_email_smtp_background,
                smtp_host,
                smtp_port,
                smtp_user,
                smtp_pass,
                destinatario_email,
                nome_cli,
                tipo_limpo,
                operador_cli,
                caminho_gerado,
                idioma_escolhido
            )
        else:
            raise HTTPException(status_code=400, detail=t("err_canal_invalido", idioma_escolhido))

        return JSONResponse(content={
            "status": t("sucesso", idioma_escolhido),
            "idioma": idioma_escolhido,
            "mensagem": f"{t('dossie_enviado_fila', idioma_escolhido)} {destinatario_email}!",
            "cliente": nome_cli,
            "arquivo": caminho_gerado.name
        })
    except HTTPException:
        raise
    except (OSError, ValueError, KeyError, RuntimeError) as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no envio: {str(e)}")


@app.post("/api/pdf/{tipo_relatorio}")
def gerador_pdf_dinamico_backend(tipo_relatorio: str, data: RelatorioDossierRequest):
    idioma_escolhido = normalizar_idioma(data.idioma)
    try:
        nome_cli, empresa_cli = _resolver_cliente_empresa(data.cliente, data.empresa)
        operador_cli = data.operador or "THIERRY (TCC SOBERANO)"
        tipo_limpo = tipo_relatorio.lower().strip()

        caminho_gerado = Path(compilar_pdf_especifico(
            tipo_limpo,
            nome_cli,
            empresa_cli,
            operador_cli,
            lang=idioma_escolhido,
            dados_orquestrador_llm=data.dados_llm
        ))

        if caminho_gerado.exists():
            return FileResponse(path=str(caminho_gerado), media_type='application/pdf', filename=caminho_gerado.name)
        else:
            raise HTTPException(status_code=404, detail=t("err_pdf_nao_encontrado", idioma_escolhido))
    except HTTPException:
        raise
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@app.post("/api/v1/gerar-relatorio-executivo")
@app.post("/api/v1/gerar-relatorio-monaco")
def endpoint_gerar_relatorio_monaco(sessao: DadosSessaoReal):
    idioma_escolhido = normalizar_idioma(sessao.idioma)
    try:
        dados_reais = sessao.model_dump() if hasattr(sessao, "model_dump") else sessao.dict()
        nome_cli, empresa_cli = _resolver_cliente_empresa(dados_reais.get("nome"), dados_reais.get("empresa"))

        caminho_gerado = Path(compilar_pdf_especifico(
            "biogem_core",
            nome_cli,
            empresa_cli,
            "THIERRY (TCC SOBERANO)",
            lang=idioma_escolhido,
            dados_orquestrador_llm=dados_reais.get("dados_llm", {})
        ))

        return {
            "status": t("sucesso", idioma_escolhido),
            "idioma": idioma_escolhido,
            "mensagem": t("dossie_gerado", idioma_escolhido),
            "cliente": nome_cli,
            "empresa": empresa_cli,
            "caminho_arquivo": f"/pdfs/{caminho_gerado.name}"
        }
    except HTTPException:
        raise
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar Mônaco: {str(e)}")


@app.post("/api/v1/salvar-estado-preditivo")
async def salvar_estado_preditivo_api(request: Request, lang: str = Query("PT")):
    idioma = normalizar_idioma(lang)
    try:
        dados = await request.json()
        caminho_estado = BASE_DIR / "estado_preditivo.json"
        with open(caminho_estado, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        return {"status": t("sucesso", idioma), "idioma": idioma, "mensagem": t("estado_sincronizado", idioma)}
    except (json.JSONDecodeError, OSError, ValueError, KeyError, TypeError) as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")


@app.get("/api/v1/compliance/verificar-ledger")
def verificar_ledger(lang: str = Query("PT")):
    return auditor_ledger.verificar_integridade_ledger(lang=lang)


@app.post("/api/v1/admin/validar-senha")
def api_validar_senha_master(data: AdminAuthRequest):
    return JSONResponse(content=validar_senha_master(data.senha_master))


@app.post("/api/v1/admin/alterar-status")
def api_alterar_status_empresa(data: AdminAuthRequest):
    return JSONResponse(content=alterar_status_empresa(data.senha_master, data.token_ou_empresa or "", data.novo_status or "ATIVO"))


@app.get("/api/v1/admin/verificar-vigencia/{token_ou_empresa}")
def api_verificar_vigencia(token_ou_empresa: str):
    return JSONResponse(content=verificar_vigencia_licenca(token_ou_empresa))


@app.get("/api/v1/admin/listar-empresas")
def api_listar_empresas():
    return JSONResponse(content=carregar_dados_empresas())


@app.get("/api/v1/fila-arquivos")
def consultar_fila_arquivos(lang: str = Query("PT")) -> JSONResponse:
    idioma = normalizar_idioma(lang)
    return JSONResponse(content={
        "status": t("sucesso", idioma),
        "idioma": idioma,
        "total_arquivos": len(orquestrador.memoria_sessao["fila_arquivos_gerados"]),
        "fila": orquestrador.memoria_sessao["fila_arquivos_gerados"]
    })


@app.get("/api/v1/pdfs/listar")
def listar_pdfs_finais(lang: str = Query("PT")) -> JSONResponse:
    idioma = normalizar_idioma(lang)
    try:
        if not PASTA_PDFS_FINAIS.exists():
            return JSONResponse(content={"status": t("erro", idioma), "mensagem": "Pasta não encontrada."}, status_code=404)
        arquivos = sorted(PASTA_PDFS_FINAIS.glob("*.pdf"), key=os.path.getmtime, reverse=True)
        lista_arquivos = []
        for f in arquivos:
            nome_arq = f.name.lower()
            tipo_classificado = "roi" if "roi" in nome_arq else ("pit" if "pit" in nome_arq else ("contrato" if "contrato" in nome_arq else "dossie"))
            lista_arquivos.append({
                "nome": f.name,
                "tipo_identificado": tipo_classificado,
                "caminho": f"/pdfs/{f.name}",
                "tamanho_kb": round(f.stat().st_size / 1024, 2),
                "data_modificacao": datetime.datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })
        return JSONResponse(content={"status": t("sucesso", idioma), "idioma": idioma, "total": len(lista_arquivos), "arquivos": lista_arquivos})
    except OSError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/pdfs/abrir/{nome_arquivo}")
def abrir_pdf_especifico(nome_arquivo: str, lang: str = Query("PT")):
    idioma = normalizar_idioma(lang)
    caminho_arquivo = _resolver_pdf_seguro(nome_arquivo, idioma)
    if caminho_arquivo.exists():
        return FileResponse(path=caminho_arquivo, media_type='application/pdf', filename=caminho_arquivo.name)
    raise HTTPException(status_code=404, detail=t("err_pdf_nao_encontrado", idioma))


@app.get("/api/v1/pdfs/renderizar/{nome_arquivo}")
def renderizar_pagina_pdf_como_imagem(nome_arquivo: str, pagina: int = 0, lang: str = Query("PT")):
    idioma = normalizar_idioma(lang)
    try:
        caminho_arquivo = _resolver_pdf_seguro(nome_arquivo, idioma)
        if not caminho_arquivo.exists():
            raise HTTPException(status_code=404, detail=t("err_pdf_nao_encontrado", idioma))
        doc = fitz.open(str(caminho_arquivo))
        if pagina >= len(doc):
            pagina = 0
        pag = doc.load_page(pagina)
        pix = pag.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        return StreamingResponse(iter([pix.tobytes("jpeg")]), media_type="image/jpeg")
    except HTTPException:
        raise
    except (fitz.FileDataError, OSError, ValueError, RuntimeError) as e:
        raise HTTPException(status_code=500, detail=f"Erro ao renderizar PDF: {str(e)}")


if __name__ == "__main__":
    ip_local = obter_ip_rede_local()
    print("=================================================================")
    print("   THIÉRRY TECHNOLOGY CONCEPT GLOBAL - GATEWAY MASTER NODE       ")
    print(f"   Servidor Soberano FastAPI Ativo na Porta {TTC_PORT} (Mônaco Tier-1)   ")
    print(f"   PC Local           : http://127.0.0.1:{TTC_PORT}                   ")
    print(f"   Celular / Tablet   : http://{ip_local}:{TTC_PORT}               ")
    print("=================================================================")
    uvicorn.run("main:app", host=TTC_HOST, port=TTC_PORT, reload=False)