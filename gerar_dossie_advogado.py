import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -*- coding: utf-8 -*-
"""
Script: gerar_dossie_advogado.py
Finalidade: Gera um PDF técnico-jurídico em formato A4 para apoiar a revisão
            de um advogado, exibindo saída estruturada no terminal e incluindo
            Glossário Técnico no PDF e no console, além de:
            - Inventário do sistema e hashes SHA-256
            - Leitura do contrato_global_engine.py e auditoria de PDFs
            - Tabela e resumo limpo (OK / FALTA) dos 17 enclaves/jurisdições
            - Bloco de licenças, estrutura atual e nota de prontidão internacional
            - Encerramento com ponto de vista jurídico internacional e nota de 1 a 100.
"""

import hashlib
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Set, Tuple, TypedDict

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    Flowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

PASTAS_IGNORADAS: Set[str] = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    "_reserva_segura",
    "_cofre_recuperacao_zerados",
}

EXTENSOES_TEXTO: Set[str] = {
    ".py",
    ".html",
    ".css",
    ".js",
    ".json",
    ".md",
    ".txt",
}

GLOSSARIO_TECNICO: List[Tuple[str, str]] = [
    (
        "Local-First / On-Premise",
        "Execução do software e guarda de dados no ambiente/hardware local, sem depender de nuvem externa para funcionar ou armazenar registros.",
    ),
    (
        "Zero-Retention",
        "Política/prática de não reter dados brutos ou sessões após o processamento, descartando ou limpando resíduos conforme o fluxo definido.",
    ),
    (
        "EULA",
        "End User License Agreement — contrato de licença de usuário final que define permissões, restrições e condições de uso do software.",
    ),
    (
        "SHA-256",
        "Função criptográfica de resumo (hash) usada para verificar integridade e gerar identificação única de arquivos ou payloads.",
    ),
    (
        "Hardware ID (HWID)",
        "Identificador associado ao hardware/máquina onde a instância é executada ou vinculada.",
    ),
    (
        "LGPD / GDPR Art. 9 / CCPA",
        "Marcos normativos de proteção de dados pessoais (Brasil, União Europeia — incluindo categorias especiais — e Califórnia, EUA), a serem conferidos conforme a operação.",
    ),
    (
        "APDP / Lei nº 1.565",
        "Autoridade/regime de proteção de dados de Mônaco citados no motor contratual; exige conferência de aplicabilidade e foro perante a lei local.",
    ),
]

ENCLAVES_17_BASE: List[Tuple[str, str, str, str, List[str]]] = [
    (
        "Dubai / Abu Dhabi",
        "Emirados Árabes Unidos",
        "AE.json",
        "Enclave internacional de isolamento e operação",
        ["ae.json", "dubai", "abu dhabi", "emirados"],
    ),
    (
        "São Luís / Matriz Global",
        "Brasil",
        "BR.json",
        "Base operacional / matriz e referência nacional (LGPD)",
        ["br.json", "são luís", "sao luis", "brasil", "lgpd"],
    ),
    (
        "Zurique / Genebra",
        "Suíça",
        "CH.json",
        "Enclave internacional de referência",
        ["ch.json", "zurique", "zurich", "genebra", "suíça", "suica"],
    ),
    (
        "Frankfurt / Munique",
        "Alemanha",
        "DE.json",
        "Enclave europeu (GDPR)",
        ["de.json", "frankfurt", "munique", "alemanha", "gdpr"],
    ),
    (
        "Paris / Global Border",
        "França",
        "FR.json",
        "Enclave europeu e fronteira global",
        ["fr.json", "paris", "frança", "franca"],
    ),
    (
        "Seul",
        "Coreia do Sul",
        "KR.json",
        "Enclave asiático de referência",
        ["kr.json", "seul", "coreia do sul"],
    ),
    (
        "Europa Central - Tier-1 Sovereign",
        "Global / Mônaco",
        "MC.json",
        "Enclave soberano e referência regulatória/contratual",
        ["mc.json", "mônaco", "monaco", "apdp", "1.565", "tier-1 sovereign"],
    ),
    (
        "Doha",
        "Catar",
        "QA.json",
        "Enclave no Oriente Médio",
        ["qa.json", "doha", "catar", "qatar"],
    ),
    (
        "Singapura",
        "Singapura",
        "SG.json",
        "Enclave financeiro e tecnológico na Ásia",
        ["sg.json", "singapura", "singapore"],
    ),
    (
        "Londres / Mayfair",
        "Reino Unido",
        "UK.json",
        "Enclave no Reino Unido",
        ["uk.json", "londres", "london", "mayfair", "reino unido"],
    ),
    (
        "Alaska Sovereign",
        "Estados Unidos (US)",
        "US-AS.json",
        "Enclave regional sob a jurisdição dos EUA",
        ["us-as.json", "alaska sovereign", "alaska"],
    ),
    (
        "Atlanta Hub",
        "Estados Unidos (US)",
        "US-AT.json",
        "Enclave regional sob a jurisdição dos EUA",
        ["us-at.json", "atlanta hub", "atlanta"],
    ),
    (
        "Beverly Hills UHNW",
        "Estados Unidos (US)",
        "US-BH.json",
        "Enclave regional sob a jurisdição dos EUA",
        ["us-bh.json", "beverly hills uhnw", "beverly hills"],
    ),
    (
        "New York / Harbor",
        "Estados Unidos (US)",
        "US-HB.json",
        "Enclave regional sob a jurisdição dos EUA",
        ["us-hb.json", "new york / harbor", "new york", "harbor"],
    ),
    (
        "Palm Beach",
        "Estados Unidos (US)",
        "US-PB.json",
        "Enclave regional sob a jurisdição dos EUA",
        ["us-pb.json", "palm beach"],
    ),
    (
        "Reno / High-Tech",
        "Estados Unidos (US)",
        "US-RH.json",
        "Enclave regional sob a jurisdição dos EUA",
        ["us-rh.json", "reno / high-tech", "reno"],
    ),
    (
        "Federal Core",
        "Estados Unidos (US)",
        "US.json",
        "Núcleo federal sob a jurisdição dos EUA",
        ["us.json", "federal core", "estados unidos", "ccpa"],
    ),
]


class ModuloInfo(TypedDict):
    caminho: str
    linhas: int
    sha256_12: str


class PdfResumo(TypedDict):
    arquivo: str
    tamanho_kb: float
    paginas: int
    chars: int
    observacao: str


class CidadeJurisdicaoItem(TypedDict):
    indice: int
    cidade: str
    pais_jurisdicao: str
    codigo: str
    funcao: str
    no_programa: str


def _normalizar_rel(rel: str) -> str:
    return str(rel).replace("\\", "/").strip().lower()


def _extrair_texto_pdf(caminho_pdf: str) -> Tuple[int, str]:
    if not os.path.isfile(caminho_pdf) or os.path.getsize(caminho_pdf) == 0:
        return 0, ""

    for mod_nome in ("pypdf", "PyPDF2"):
        try:
            mod: Any = __import__(mod_nome)
            reader = mod.PdfReader(caminho_pdf)
            paginas: int = len(reader.pages)
            texto: str = "\n".join(str(p.extract_text() or "") for p in reader.pages)
            return paginas, texto
        except Exception:
            continue

    try:
        import fitz  # type: ignore

        doc = fitz.open(caminho_pdf)
        paginas = len(doc)
        texto = "\n".join(str(page.get_text("text") or "") for page in doc)
        doc.close()
        return paginas, texto
    except Exception:
        pass

    try:
        with open(caminho_pdf, "rb") as f:
            raw: bytes = f.read()
        trechos: List[bytes] = re.findall(rb"\(([^()]{3,200})\)", raw)
        texto_limpo: str = re.sub(
            r"\s+", " ", " ".join(t.decode("latin-1", errors="ignore") for t in trechos)
        ).strip()
        return (1 if raw.startswith(b"%PDF") else 0), texto_limpo
    except Exception:
        return 0, ""


def coletar_modulos_python(raiz: str) -> Tuple[List[ModuloInfo], int, Dict[str, int]]:
    modulos: List[ModuloInfo] = []
    total_linhas: int = 0
    por_extensao: Dict[str, int] = {}

    for atual, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]
        for nome in sorted(arquivos):
            caminho: str = os.path.join(atual, nome)
            if not os.path.isfile(caminho):
                continue
            rel: str = os.path.relpath(caminho, raiz).replace("\\", "/")
            ext: str = os.path.splitext(nome)[1].lower() or "(sem_ext)"
            por_extensao[ext] = por_extensao.get(ext, 0) + 1

            if ext == ".py":
                try:
                    with open(caminho, "rb") as fb:
                        digest: str = hashlib.sha256(fb.read()).hexdigest()[:12].upper()
                    with open(caminho, "r", encoding="utf-8", errors="replace") as ft:
                        linhas: int = sum(1 for _ in ft)
                    total_linhas += linhas
                    modulos.append({"caminho": rel, "linhas": linhas, "sha256_12": digest})
                except OSError:
                    modulos.append(
                        {"caminho": rel, "linhas": 0, "sha256_12": "ERRO_LEITURA"}
                    )

    return modulos, total_linhas, por_extensao


def _coletar_arquivos_e_corpus(raiz: str, pdf_rel_atual: str) -> Tuple[Set[str], str]:
    arquivos_rel_low: Set[str] = set()
    partes: List[str] = []
    alvo_norm: str = _normalizar_rel(pdf_rel_atual)

    for atual, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]
        for nome in sorted(arquivos):
            caminho: str = os.path.join(atual, nome)
            if not os.path.isfile(caminho):
                continue
            rel: str = os.path.relpath(caminho, raiz).replace("\\", "/")
            rel_low: str = _normalizar_rel(rel)
            arquivos_rel_low.add(rel_low)
            arquivos_rel_low.add(nome.lower())

            if rel_low == alvo_norm:
                continue
            ext: str = os.path.splitext(nome)[1].lower()
            try:
                if ext in EXTENSOES_TEXTO:
                    with open(caminho, "r", encoding="utf-8", errors="replace") as f:
                        partes.append(f.read())
                elif ext == ".pdf":
                    _, txt_pdf = _extrair_texto_pdf(caminho)
                    if txt_pdf:
                        partes.append(txt_pdf)
            except OSError:
                pass

    return arquivos_rel_low, "\n".join(partes)


def mapear_17_cidades_jurisdicoes(raiz: str, pdf_rel_atual: str) -> List[CidadeJurisdicaoItem]:
    """
    Mapeia os 17 enclaves/cidades/jurisdições e retorna 'OK' se existir/estiver
    referenciado no projeto, ou 'FALTA' caso contrário.
    """
    arquivos_low, corpus = _coletar_arquivos_e_corpus(raiz, pdf_rel_atual)
    corpus_low: str = corpus.lower()

    itens: List[CidadeJurisdicaoItem] = []
    for idx, (cidade, pais, codigo, funcao, termos) in enumerate(ENCLAVES_17_BASE, start=1):
        cod_low: str = codigo.lower()
        existe: bool = (cod_low in arquivos_low) or any(t in corpus_low for t in termos)

        itens.append(
            {
                "indice": idx,
                "cidade": cidade,
                "pais_jurisdicao": pais,
                "codigo": codigo,
                "funcao": funcao,
                "no_programa": "OK" if existe else "FALTA",
            }
        )

    return itens


def auditar_contrato_e_licencas(raiz: str) -> Dict[str, Any]:
    caminho_engine: str = os.path.join(raiz, "legal", "contrato_global_engine.py")
    if not os.path.isfile(caminho_engine):
        return {
            "engine_presente": False,
            "presentes": ["legal/contrato_global_engine.py não encontrado na raiz inspecionada."],
            "estrutura_licencas": [
                "Motor contratual não localizado para inspeção automática das cláusulas de licença."
            ],
            "nota_internacional": 2.0,
            "justificativa_nota": (
                "Nota técnica indicativa baixa (2,0/10) porque o motor do contrato não foi "
                "encontrado no caminho esperado para conferência completa."
            ),
            "atencao": [
                "Localizar ou gerar legal/contrato_global_engine.py e submeter à revisão de advogado."
            ],
        }

    try:
        with open(caminho_engine, "r", encoding="utf-8", errors="replace") as f:
            codigo: str = f.read()
    except OSError as exc:
        return {
            "engine_presente": False,
            "presentes": [f"Falha ao ler contrato_global_engine.py: {exc}"],
            "estrutura_licencas": ["Não foi possível ler o arquivo do contrato."],
            "nota_internacional": 2.0,
            "justificativa_nota": "Nota técnica indicativa limitada por erro de leitura do arquivo.",
            "atencao": ["Verificar permissões e integridade do arquivo antes da revisão jurídica."],
        }

    low: str = codigo.lower()
    presentes: List[str] = []
    estrutura_licencas: List[str] = []
    atencao: List[str] = []

    pontos_positivos: int = 0
    total_criterios: int = 7

    if "eula" in low:
        presentes.append("EULA estruturado na abertura do contrato")
        pontos_positivos += 1
    if "lgpd" in low or "gdpr" in low or "ccpa" in low:
        presentes.append("Menções normativas de privacidade (LGPD / GDPR / CCPA)")
        pontos_positivos += 1
    if "local-first" in low or "zero-retention" in low or "on-premise" in low:
        presentes.append("Descrição de operação local-first / zero-retention / on-premise")
        pontos_positivos += 1
    if "mônaco" in low or "monaco" in low or "apdp" in low:
        presentes.append("Referências a Mônaco / APDP / Lei nº 1.565")
        pontos_positivos += 1

    if "10 (dez) licenças" in low or "10 (ten) active licenses" in low:
        estrutura_licencas.append("Teto de escassez declarado de 10 licenças/nós globais")
        pontos_positivos += 1
    if "12 (doze) meses" in low or "12-month" in low:
        estrutura_licencas.append("Vigência contratual de 12 meses com renovação auditada")
        pontos_positivos += 1
    if "stripe" in low or "tabela_pib" in low:
        estrutura_licencas.append(
            "Cobrança/gateway referenciando Stripe e multiplicadores regionais/PIB"
        )
        pontos_positivos += 1
    if "engenharia reversa" in low or "reverse engineering" in low:
        estrutura_licencas.append(
            "Vedação expressa a cópia, clonagem, sublicenciamento e engenharia reversa"
        )

    nota_internacional: float = round(
        min(10.0, max(1.0, (pontos_positivos / total_criterios) * 8.5)), 1
    )

    justificativa_nota: str = (
        f"Nota técnica/documental indicativa: {nota_internacional:.1f} / 10,0. "
        "O contrato já apresenta boa base redacional (EULA, proteção contra engenharia reversa, "
        "menção a LGPD/GDPR/CCPA, arquitetura local-first/zero-retention, teto de licenças e "
        "vigência), mas não atinge nota máxima na análise automática porque escolhas de foro/lei "
        "estrangeira (Mônaco/APDP), aderência aos enclaves/países (incluindo os enclaves dos EUA), "
        "titularidade/estrutura empresarial e limites de responsabilidade dependem de validação jurídica "
        "formal por advogado."
    )

    atencao.append(
        "Foro, lei aplicável e exequibilidade internacional: revisar a eleição de Mônaco/APDP "
        "e a prevalência de idioma frente às leis locais do comprador e do Brasil."
    )
    atencao.append(
        "Enclaves e jurisdições: conferir como os 17 enclaves (incluindo os enclaves dos EUA) "
        "se relacionam à lei aplicável, proteção de dados e restrição territorial/licença."
    )
    atencao.append(
        "Titularidade, registro e regime da operação: conferir quem figura como titular/licenciante, "
        "registros existentes e se o instrumento atende a licenciamento ou venda/cessão."
    )
    atencao.append(
        "Dados sensíveis/biometria e responsabilidade: revisar cláusulas de consentimento prévio/"
        "expresso, DPA/responsabilidade do operador e limites de indenização/responsabilidade."
    )
    if "placeholder_licenciado" in low or "[a preencher" in low:
        atencao.append(
            "Campos em aberto: preencher identificação completa do licenciado/comprador e parâmetros "
            "finais antes da assinatura."
        )

    return {
        "engine_presente": True,
        "presentes": presentes,
        "estrutura_licencas": estrutura_licencas,
        "nota_internacional": nota_internacional,
        "justificativa_nota": justificativa_nota,
        "atencao": atencao,
    }


def avaliar_jurisdicao_internacional_1_a_100(
    raiz: str,
    auditoria_lic: Dict[str, Any],
    cidades_17: List[CidadeJurisdicaoItem],
    total_linhas: int,
) -> Dict[str, Any]:
    """
    Calcula uma nota indicativa de 1 a 100 do que o programa já reúne no código,
    contrato e mapeamento de enclaves sob a ótica da jurisdição internacional,
    e gera um texto explicativo baseado no que o programa é.
    """
    caminho_engine: str = os.path.join(raiz, "legal", "contrato_global_engine.py")
    codigo_low: str = ""
    if os.path.isfile(caminho_engine):
        try:
            with open(caminho_engine, "r", encoding="utf-8", errors="replace") as f:
                codigo_low = f.read().lower()
        except OSError:
            codigo_low = ""

    enclaves_ok: int = sum(1 for c in cidades_17 if c["no_programa"] == "OK")
    qtd_cidades: int = max(1, len(cidades_17))

    pts_enclaves: float = (enclaves_ok / qtd_cidades) * 25.0
    pts_motor: float = 15.0 if auditoria_lic.get("engine_presente") else 0.0
    pts_privacidade: float = (
        15.0 if any(k in codigo_low for k in ("lgpd", "gdpr", "ccpa", "apdp")) else 0.0
    )
    pts_arquitetura: float = (
        15.0
        if any(k in codigo_low for k in ("local-first", "zero-retention", "on-premise"))
        else 0.0
    )
    pts_licenca: float = (
        15.0
        if any(
            k in codigo_low
            for k in ("10 (dez) licenças", "10 (ten) active licenses", "12 (doze) meses", "stripe")
        )
        else 0.0
    )
    pts_pi_eula: float = (
        15.0
        if ("eula" in codigo_low and ("engenharia reversa" in codigo_low or "reverse engineering" in codigo_low))
        else 0.0
    )

    nota_1_100: int = int(
        round(
            min(
                100.0,
                max(
                    1.0,
                    pts_enclaves + pts_motor + pts_privacidade + pts_arquitetura + pts_licenca + pts_pi_eula,
                ),
            )
        )
    )

    texto_juridico_internacional: str = (
        f"Nota indicativa de prontidão jurisdicional internacional (varredura do sistema): "
        f"{nota_1_100} / 100 (enclaves presentes: {enclaves_ok}/{qtd_cidades}; base inspecionada: "
        f"{total_linhas} linhas em .py). "
        "Do ponto de vista jurídico internacional, este programa é um ecossistema de software "
        "focado em análise facial/visagismo, tricologia, simulações/projeções e controle perimetral, "
        "estruturado para operar com foco local/on-premise, minimização/descarte de dados em nuvem "
        "externa e segmentação por 17 enclaves/jurisdições (incluindo Brasil, enclaves sob os EUA, "
        "Europa, Ásia, Oriente Médio e referências como Mônaco/APDP). "
        "O que já existe no programa oferece um esboço técnico e contratual inicial (EULA, vedação "
        "a engenharia reversa, referências a LGPD/GDPR/CCPA/APDP, parâmetros de licença/vigência e "
        "tabela de 17 enclaves), mas uma nota abaixo de 100 na varredura indica que a validade, "
        "a execução transfronteiriça, a escolha de foro/lei aplicável, a adequação a cada país/estado "
        "(como regras estaduais dos EUA e normas da UE/Brasil), a titularidade formal do ativo e "
        "as obrigações sobre dados sensíveis/biométricos exigem revisão e validação jurídica de um advogado."
    )

    return {
        "nota_1_100": nota_1_100,
        "enclaves_ok": enclaves_ok,
        "qtd_cidades": qtd_cidades,
        "texto_juridico_internacional": texto_juridico_internacional,
    }


def auditar_pdfs(raiz: str, pdf_rel_atual: str) -> List[PdfResumo]:
    resumos: List[PdfResumo] = []
    alvo_norm: str = _normalizar_rel(pdf_rel_atual)

    for atual, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]
        for nome in sorted(arquivos):
            if not nome.lower().endswith(".pdf"):
                continue
            caminho: str = os.path.join(atual, nome)
            rel: str = os.path.relpath(caminho, raiz).replace("\\", "/")
            if _normalizar_rel(rel) == alvo_norm or not os.path.isfile(caminho):
                continue

            tam_bytes: int = os.path.getsize(caminho)
            paginas, texto = _extrair_texto_pdf(caminho)
            chars: int = len(texto.strip())

            if tam_bytes == 0:
                obs = "Arquivo vazio (0 bytes)"
            elif chars < 80:
                obs = "Pouco texto extraído (pode ser imagem/escaneado ou incompleto)"
            else:
                obs = "Texto extraído com sucesso"

            resumos.append(
                {
                    "arquivo": rel,
                    "tamanho_kb": round(tam_bytes / 1024.0, 2),
                    "paginas": paginas,
                    "chars": chars,
                    "observacao": obs,
                }
            )

    return resumos


def imprimir_resumo_terminal(
    caminho_pdf: str,
    raiz: str,
    modulos: List[ModuloInfo],
    total_linhas: int,
    auditoria_lic: Dict[str, Any],
    cidades_17: List[CidadeJurisdicaoItem],
    pdfs_encontrados: List[PdfResumo],
    avaliacao_intl: Dict[str, Any],
) -> None:
    logger.info("=" * 72)
    logger.info("DOSSIÊ TÉCNICO-JURÍDICO PARA REVISÃO ADVOCATÍCIA")
    logger.info("=" * 72)
    logger.info(f"Raiz auditada     : {raiz}")
    logger.info(f"PDF gerado        : {caminho_pdf}")
    logger.info(f"Módulos .py       : {len(modulos)} | Total de linhas: {total_linhas}")
    logger.info(f"PDFs inspecionados : {len(pdfs_encontrados)}")
    logger.info(f"Nota licenças     : {auditoria_lic['nota_internacional']:.1f} / 10,0 (apoio técnico)")
    logger.info("-" * 72)
    logger.info("17 ENCLAVES / JURISDIÇÕES:")
    for c in cidades_17:
        logger.info(
            f"  {c['indice']:02d}. {c['codigo']:<10} | {c['pais_jurisdicao']:<22} | "
            f"{c['cidade']:<32} | {c['no_programa']}"
        )
    logger.info("-" * 72)
    logger.info("GLOSSÁRIO TÉCNICO:")
    for termo, definicao in GLOSSARIO_TECNICO:
        logger.info(f"  • {termo}: {definicao}")
    logger.info("-" * 72)
    logger.info("PONTO DE VISTA JURÍDICO INTERNACIONAL (ENCERRAMENTO):")
    logger.info(f"  Nota jurisdição internacional (1 a 100): {avaliacao_intl['nota_1_100']} / 100")
    logger.info(f"  {avaliacao_intl['texto_juridico_internacional']}")
    logger.info("=" * 72)


def gerar_relatorio_advogado(caminho_pdf: str, raiz: str) -> str:
    pasta_saida: str = os.path.dirname(os.path.abspath(caminho_pdf))
    if pasta_saida:
        os.makedirs(pasta_saida, exist_ok=True)

    pdf_rel_atual: str = os.path.relpath(caminho_pdf, raiz).replace("\\", "/")
    modulos, total_linhas, por_ext = coletar_modulos_python(raiz)
    auditoria_lic = auditar_contrato_e_licencas(raiz)
    cidades_17 = mapear_17_cidades_jurisdicoes(raiz, pdf_rel_atual)
    pdfs_encontrados = auditar_pdfs(raiz, pdf_rel_atual)
    avaliacao_intl = avaliar_jurisdicao_internacional_1_a_100(
        raiz=raiz,
        auditoria_lic=auditoria_lic,
        cidades_17=cidades_17,
        total_linhas=total_linhas,
    )

    agora_utc: str = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S UTC")
    largura_util: float = float(A4[0]) - 80.0

    doc = SimpleDocTemplate(
        caminho_pdf,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=45,
        bottomMargin=45,
    )

    azul = colors.HexColor("#0A192F")
    ouro = colors.HexColor("#B8860B")
    cinza = colors.HexColor("#F4F6F9")
    borda = colors.HexColor("#CBD5E1")

    st_titulo = ParagraphStyle(
        "AdvTitulo",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=azul,
        alignment=TA_CENTER,
        spaceAfter=3,
    )
    st_sub = ParagraphStyle(
        "AdvSub",
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor=ouro,
        alignment=TA_CENTER,
        spaceAfter=10,
    )
    st_h2 = ParagraphStyle(
        "AdvH2",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        textColor=azul,
        spaceBefore=10,
        spaceAfter=4,
    )
    st_txt = ParagraphStyle(
        "AdvTxt",
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        alignment=TA_JUSTIFY,
        spaceAfter=4,
    )
    st_cel_h = ParagraphStyle(
        "AdvCelH", fontName="Helvetica-Bold", fontSize=7, textColor=azul, leading=9
    )
    st_cel = ParagraphStyle("AdvCel", fontName="Helvetica", fontSize=6.8, leading=8.8)

    story: List[Flowable] = [
        Paragraph("DOSSIÊ TÉCNICO-JURÍDICO PARA REVISÃO ADVOCATÍCIA", st_titulo),
        Paragraph("SISTEMA, 17 ENCLAVES/JURISDIÇÕES, LICENÇAS E GLOSSÁRIO TÉCNICO", st_sub),
        Paragraph(
            f"<b>Raiz auditada:</b> {str(raiz)}<br/>"
            f"<b>Gerado em (UTC):</b> {str(agora_utc)}<br/>"
            f"<b>Módulos .py encontrados:</b> {len(modulos)} | "
            f"<b>Total de linhas em .py:</b> {total_linhas} | "
            f"<b>PDFs inspecionados:</b> {len(pdfs_encontrados)}<br/>"
            f"<b>Aviso:</b> Relatório técnico-documental para apoiar o advogado; não substitui "
            f"parecer jurídico nem validação formal do profissional.",
            st_txt,
        ),
        Paragraph("1. VISÃO GERAL DO PROGRAMA E ARQUITETURA", st_h2),
        Paragraph(
            "• <b>O que o programa faz:</b> Plataforma de software voltada a análise facial/visagismo, "
            "tricologia, simulações/projeções e módulos de controle, segurança e emissão de relatórios/dossiês.",
            st_txt,
        ),
        Paragraph(
            "• <b>Arquitetura e dados:</b> Projetada com foco em execução local/on-premise e "
            "minimização/descarte de dados em nuvem externa, exigindo atenção jurídica quanto ao "
            "consentimento do titular, tratamento de dados sensíveis/biométricos e responsabilidade operacional.",
            st_txt,
        ),
        Paragraph("2. BLOCO DE LICENÇAS, ESTRUTURA E NOTA DE PRONTIDÃO INTERNACIONAL", st_h2),
        Paragraph(str(auditoria_lic["justificativa_nota"]), st_txt),
    ]

    for item_lic in auditoria_lic["estrutura_licencas"]:
        story.append(Paragraph(f"• <b>Licenças / Estrutura:</b> {str(item_lic)}", st_txt))
    for item_pres in auditoria_lic["presentes"]:
        story.append(Paragraph(f"• <b>Consta no motor:</b> {str(item_pres)}", st_txt))
    for item_at in auditoria_lic["atencao"]:
        story.append(Paragraph(f"• <b>Conferir com advogado:</b> {str(item_at)}", st_txt))

    story.append(Paragraph("3. MAPEAMENTO DOS 17 ENCLAVES, JURISDIÇÕES, FUNÇÕES E STATUS", st_h2))
    story.append(
        Paragraph(
            "Tabela com os 17 enclaves/praças (incluindo os enclaves sob a jurisdição dos EUA), "
            "código/arquivo .json, função e status no projeto (OK / FALTA):",
            st_txt,
        )
    )

    cid_rows: List[List[Paragraph]] = [
        [
            Paragraph("<b>#</b>", st_cel_h),
            Paragraph("<b>Código / JSON</b>", st_cel_h),
            Paragraph("<b>País / Jurisdição</b>", st_cel_h),
            Paragraph("<b>Cidade / Praça</b>", st_cel_h),
            Paragraph("<b>Função</b>", st_cel_h),
            Paragraph("<b>Status</b>", st_cel_h),
        ]
    ]
    for c in cidades_17:
        cid_rows.append(
            [
                Paragraph(str(c["indice"]), st_cel),
                Paragraph(str(c["codigo"]), st_cel),
                Paragraph(str(c["pais_jurisdicao"]), st_cel),
                Paragraph(str(c["cidade"]), st_cel),
                Paragraph(str(c["funcao"]), st_cel),
                Paragraph(str(c["no_programa"]), st_cel),
            ]
        )

    t_cid = Table(
        cid_rows,
        colWidths=[
            largura_util * 0.05,
            largura_util * 0.13,
            largura_util * 0.18,
            largura_util * 0.21,
            largura_util * 0.34,
            largura_util * 0.09,
        ],
    )
    t_cid.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                ("GRID", (0, 0), (-1, -1), 0.5, borda),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, cinza]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("PADDING", (0, 0), (-1, -1), 2.5),
            ]
        )
    )
    story.append(t_cid)

    story.append(Paragraph("4. GLOSSÁRIO TÉCNICO", st_h2))
    for termo, definicao in GLOSSARIO_TECNICO:
        story.append(Paragraph(f"• <b>{termo}:</b> {definicao}", st_txt))

    story.append(Paragraph("5. PDFS ENCONTRADOS NO PROJETO", st_h2))
    if pdfs_encontrados:
        for p in pdfs_encontrados[:25]:
            story.append(
                Paragraph(
                    f"• <b>{str(p['arquivo'])}</b> ({p['tamanho_kb']} KB, {p['paginas']} pág., "
                    f"{p['chars']} chars): {str(p['observacao'])}",
                    st_txt,
                )
            )
    else:
        story.append(
            Paragraph("Nenhum outro PDF localizado fora deste relatório no momento.", st_txt)
        )

    story.append(Paragraph("6. RESUMO POR EXTENSÃO", st_h2))
    ext_rows: List[List[Paragraph]] = [
        [Paragraph("<b>Extensão</b>", st_cel_h), Paragraph("<b>Qtd.</b>", st_cel_h)]
    ]
    for ext, qtd in sorted(por_ext.items(), key=lambda x: (-x[1], x[0]))[:15]:
        ext_rows.append([Paragraph(str(ext), st_cel), Paragraph(str(qtd), st_cel)])

    t_ext = Table(ext_rows, colWidths=[largura_util * 0.70, largura_util * 0.30])
    t_ext.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                ("GRID", (0, 0), (-1, -1), 0.5, borda),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, cinza]),
                ("PADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(t_ext)

    story.append(Paragraph("7. INVENTÁRIO DE MÓDULOS PYTHON (.PY)", st_h2))
    py_rows: List[List[Paragraph]] = [
        [
            Paragraph("<b>Arquivo</b>", st_cel_h),
            Paragraph("<b>Linhas</b>", st_cel_h),
            Paragraph("<b>SHA-256 (12)</b>", st_cel_h),
        ]
    ]
    for m in modulos[:120]:
        py_rows.append(
            [
                Paragraph(str(m["caminho"]), st_cel),
                Paragraph(str(m["linhas"]), st_cel),
                Paragraph(f"<font name='Courier'>{str(m['sha256_12'])}</font>", st_cel),
            ]
        )

    t_py = Table(py_rows, colWidths=[largura_util * 0.62, largura_util * 0.13, largura_util * 0.25])
    t_py.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                ("GRID", (0, 0), (-1, -1), 0.5, borda),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, cinza]),
                ("PADDING", (0, 0), (-1, -1), 2.5),
            ]
        )
    )
    story.append(t_py)

    if len(modulos) > 120:
        story.append(Spacer(1, 4))
        story.append(
            Paragraph(
                f"<i>Exibindo os primeiros 120 de {len(modulos)} arquivos .py.</i>",
                st_txt,
            )
        )

    story.append(
        Paragraph(
            f"8. PONTO DE VISTA JURÍDICO INTERNACIONAL (NOTA INDICATIVA: {avaliacao_intl['nota_1_100']} / 100)",
            st_h2,
        )
    )
    story.append(Paragraph(str(avaliacao_intl["texto_juridico_internacional"]), st_txt))

    doc.build(story)
    imprimir_resumo_terminal(
        caminho_pdf=caminho_pdf,
        raiz=raiz,
        modulos=modulos,
        total_linhas=total_linhas,
        auditoria_lic=auditoria_lic,
        cidades_17=cidades_17,
        pdfs_encontrados=pdfs_encontrados,
        avaliacao_intl=avaliacao_intl,
    )
    return caminho_pdf


def executar_dossie_advogado() -> str:
    raiz: str = os.path.abspath(os.path.dirname(__file__))
    destino: str = os.path.join(raiz, "pdfs_finais", "Dossie_Tecnico_Advogado.pdf")
    return gerar_relatorio_advogado(destino, raiz)


if __name__ == "__main__":
    executar_dossie_advogado()