# -*- coding: utf-8 -*-
"""
Script: varredura_sistema_pdf.py
Finalidade: Varredura alinhada do sistema com saída limpa em [OK], ignorando
            pastas de reserva/cofre de recuperação, tratando arquivos vazios
            de backup/permitidos sem gerar alertas vermelhos desnecessários,
            leitura profunda do texto dos PDFs do projeto (contratos, normas e
            relatórios), geração do relatório em formato A4 na pasta pdfs_finais
            e parecer final sobre integridade e prontidão documental dos PDFs.
"""

import hashlib
import os
import py_compile
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Set, Tuple, TypedDict

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable

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

EXTENSOES_CODIGO: Set[str] = {
    ".py",
    ".html",
    ".css",
    ".js",
    ".bat",
    ".ps1",
    ".sh",
}

ARQUIVOS_ESSENCIAIS: List[str] = [
    "main.py",
    "core/gerador_dossies_master.py",
    "legal/contrato_global_engine.py",
]

# Arquivos vazios (0 bytes) aceitos como [OK] sem gerar alerta
ARQUIVOS_PERMITIDOS_VAZIOS: Set[str] = {
    "log_seguranca.txt",
    "documentos/th.prn",
    "storage_data/thierry_tech_biogenio.db",
    "security/core/ultimo_motodiagnostico.json",
    "tools/vault_internal_audit.log",
}

# Sobras zeradas sem referência que podem ser apagadas direto quando não tiverem cópia com conteúdo
ALVOS_APAGAR_DIRETO: Set[str] = set()

# Códigos ANSI para terminal
VERDE: str = "\033[92m"
AMARELO: str = "\033[93m"
VERMELHO: str = "\033[91m"
NEGRITO: str = "\033[1m"
RESET: str = "\033[0m"


class AuditoriaPdfItem(TypedDict):
    arquivo: str
    tamanho_bytes: int
    paginas: int
    chars_extraidos: int
    eh_contrato_ou_norma: bool
    lacunas: List[str]


class DadosVarredura(TypedDict):
    total_arquivos: int
    total_linhas_py: int
    arquivos_html: List[str]
    por_extensao: Dict[str, int]
    modulos_py: List[Tuple[str, int, str]]
    faltantes: List[str]
    avisos: List[str]
    integridade_ok: bool
    detalhe_integridade: str
    pdfs_auditados: List[AuditoriaPdfItem]
    parecer_documental_pdfs: str


def _habilitar_cores_windows() -> None:
    if os.name == "nt":
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_ulong()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except Exception:
            pass


def _ok(msg: str) -> None:
    print(f"{VERDE}[OK]{RESET} {str(msg)}")


def _info(msg: str) -> None:
    print(f"{AMARELO}[PARECER]{RESET} {str(msg)}")


def _alerta(msg: str) -> None:
    print(f"{VERMELHO}{NEGRITO}[ALERTA]{RESET} {VERMELHO}{str(msg)}{RESET}")


def _normalizar_rel(rel: str) -> str:
    return str(rel).replace("\\", "/").strip().lower()


def _extrair_texto_pdf(caminho_pdf: str) -> Tuple[int, str, str]:
    """Tenta extrair texto de todas as páginas de um PDF. Retorna (paginas, texto, metodo)."""
    if os.path.getsize(caminho_pdf) == 0:
        return 0, "", "vazio_0_bytes"

    # 1. pypdf / PyPDF2
    for mod_nome in ("pypdf", "PyPDF2"):
        try:
            mod: Any = __import__(mod_nome)
            reader = mod.PdfReader(caminho_pdf)
            paginas: int = len(reader.pages)
            partes: List[str] = []
            for p in reader.pages:
                partes.append(str(p.extract_text() or ""))
            return paginas, "\n".join(partes), mod_nome
        except Exception:
            continue

    # 2. pymupdf (fitz)
    try:
        import fitz  # type: ignore

        doc = fitz.open(caminho_pdf)
        paginas = len(doc)
        partes = [str(page.get_text("text") or "") for page in doc]
        doc.close()
        return paginas, "\n".join(partes), "fitz"
    except Exception:
        pass

    # 3. Fallback textual básico
    try:
        with open(caminho_pdf, "rb") as f:
            raw: bytes = f.read()
        trechos: List[bytes] = re.findall(rb"\(([^()]{3,200})\)", raw)
        texto_bruto: str = " ".join(
            t.decode("latin-1", errors="ignore") for t in trechos
        )
        texto_limpo: str = re.sub(r"\s+", " ", texto_bruto).strip()
        return 1 if raw.startswith(b"%PDF") else 0, texto_limpo, "fallback_bruto"
    except Exception:
        return 0, "", "erro_leitura"


def _auditar_pdfs_projeto(raiz: str, pdf_rel_atual: str) -> Tuple[List[AuditoriaPdfItem], str]:
    itens: List[AuditoriaPdfItem] = []
    alvo_atual_norm: str = _normalizar_rel(pdf_rel_atual)

    for atual, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]
        for nome in sorted(arquivos):
            if not nome.lower().endswith(".pdf"):
                continue
            caminho: str = os.path.join(atual, nome)
            rel: str = os.path.relpath(caminho, raiz).replace("\\", "/")
            if _normalizar_rel(rel) == alvo_atual_norm:
                continue

            tam: int = os.path.getsize(caminho) if os.path.isfile(caminho) else 0
            paginas, texto, _ = _extrair_texto_pdf(caminho)
            texto_low: str = texto.lower()
            chars: int = len(texto.strip())

            eh_doc_legal: bool = any(
                k in _normalizar_rel(rel) or k in texto_low
                for k in (
                    "contrato",
                    "licen",
                    "norma",
                    "lgpd",
                    "gdpr",
                    "inpi",
                    "clausula",
                    "cláusula",
                    "foro",
                    "arbitrag",
                )
            )

            lacunas: List[str] = []
            if tam == 0:
                lacunas.append("PDF de 0 bytes (arquivo vazio / inválido)")
            elif chars < 80:
                lacunas.append("Pouco ou nenhum texto extraído (pode ser imagem/escaneado ou incompleto)")

            if eh_doc_legal:
                if not re.search(r"\b(foro|lei aplic[aá]vel|jurisdi[cç][aã]o|arbitragem)\b", texto_low):
                    lacunas.append("Sem menção clara a foro / lei aplicável / jurisdição")
                if not re.search(r"\b(propriedade intelectual|titularidade|inpi|direitos autorais|engenharia reversa)\b", texto_low):
                    lacunas.append("Sem menção clara a titularidade / PI / INPI / engenharia reversa")
                if not re.search(r"\b(lgpd|gdpr|dados pessoais|dados sens[ií]veis|biometr|privacidade|confidencialidade)\b", texto_low):
                    lacunas.append("Sem menção clara a privacidade / proteção de dados / confidencialidade")
                if not re.search(r"\b(responsabilidade|indeniza[cç][aã]o|rescis[aã]o|pagamento|licen[cç]a)\b", texto_low):
                    lacunas.append("Sem menção clara a licenciamento / pagamento / responsabilidade")

            item_pdf: AuditoriaPdfItem = {
                "arquivo": rel,
                "tamanho_bytes": tam,
                "paginas": paginas,
                "chars_extraidos": chars,
                "eh_contrato_ou_norma": eh_doc_legal,
                "lacunas": lacunas,
            }
            itens.append(item_pdf)

    parecer: str
    if not itens:
        parecer = (
            "Nenhum outro PDF encontrado além do relatório atual. Se aparecer um comprador hoje, "
            "você não tem documentação contratual/normativa em PDF pronta para fechamento e "
            "precisará de advogado para redigir/validar os instrumentos e a transferência/licença."
        )
        return itens, parecer

    docs_legais: List[AuditoriaPdfItem] = [i for i in itens if i["eh_contrato_ou_norma"]]
    pdfs_com_falha: List[AuditoriaPdfItem] = [i for i in itens if i["lacunas"]]

    if not docs_legais:
        parecer = (
            f"Foram inspecionados {len(itens)} PDF(s), mas nenhum parece ser contrato/norma estruturada. "
            "Se aparecer um comprador hoje, a varredura documental aponta que falta lastro contratual "
            "formalizado em PDF — valide com advogado antes de fechar negócio."
        )
    elif not pdfs_com_falha:
        parecer = (
            f"Foram inspecionados {len(itens)} PDF(s) (incluindo {len(docs_legais)} de perfil contratual/normativo) "
            "sem lacunas óbvias de texto/cláusulas na varredura automática. Ainda assim, isso é apenas uma "
            "checagem textual de arquivos: se aparecer um comprador hoje, a validação jurídica formal "
            "(especialmente envolvendo contrato, PI/INPI, estrutura societária e operação nacional/internacional) "
            "deve ser feita por advogado."
        )
    else:
        parecer = (
            f"Foram inspecionados {len(itens)} PDF(s) e {len(pdfs_com_falha)} apresentaram lacunas/pontos de atenção "
            "no texto ou estrutura. Se aparecer um comprador hoje, NÃO está 100% redondinho só pelo texto dos PDFs — "
            "é recomendável e prudente passar por advogado para revisar cláusulas, titularidade/INPI e enquadramento legal."
        )

    return itens, parecer


def _encontrar_referencias_codigo(raiz: str, termos: Set[str]) -> Set[str]:
    citados: Set[str] = set()
    for atual, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]
        for nome in sorted(arquivos):
            ext: str = os.path.splitext(nome)[1].lower()
            if ext not in EXTENSOES_CODIGO:
                continue
            caminho: str = os.path.join(atual, nome)
            try:
                with open(caminho, "r", encoding="utf-8", errors="replace") as f:
                    conteudo: str = f.read().lower().replace("\\", "/")
                for termo in termos:
                    if termo and termo in conteudo:
                        citados.add(termo)
            except OSError:
                pass
    return citados


def verificar_integridade_programa(raiz: str, faltantes: List[str]) -> Tuple[bool, str]:
    """Verifica se os módulos compilam e se main.py carrega/roda sem quebrar."""
    erros: List[str] = []

    if faltantes:
        erros.extend(faltantes)

    main_py: str = os.path.join(raiz, "main.py")
    if not os.path.isfile(main_py):
        erros.append("Arquivo principal 'main.py' não encontrado.")
        return False, " | ".join(erros)

    candidatos_compilacao: List[str] = [main_py]
    for subpasta in ("core", "legal", "security", "tools"):
        pasta_abs: str = os.path.join(raiz, subpasta)
        if os.path.isdir(pasta_abs):
            for atual, dirs, arquivos in os.walk(pasta_abs):
                dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]
                for nome in sorted(arquivos):
                    if nome.endswith(".py"):
                        candidatos_compilacao.append(os.path.join(atual, nome))

    for arq in candidatos_compilacao:
        try:
            py_compile.compile(arq, doraise=True)
        except py_compile.PyCompileError as exc:
            erros.append(f"Falha de sintaxe em {os.path.relpath(arq, raiz)}: {exc}")

    codigo_sonda: str = (
        "import importlib.util, sys\n"
        f"spec = importlib.util.spec_from_file_location('main_probe', r'{main_py}')\n"
        "if spec is None or spec.loader is None:\n"
        "    raise RuntimeError('Não foi possível carregar main.py')\n"
        "mod = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(mod)\n"
        "print('SONDA_OK')\n"
    )
    try:
        proc = subprocess.run(
            [sys.executable, "-c", codigo_sonda],
            cwd=raiz,
            capture_output=True,
            text=True,
            timeout=25,
        )
        if proc.returncode != 0 or "SONDA_OK" not in proc.stdout:
            detalhe = (proc.stderr or proc.stdout or "Erro desconhecido ao executar main.py").strip()
            erros.append(f"Falha na execução de main.py: {detalhe}")
    except subprocess.TimeoutExpired:
        erros.append("Tempo esgotado ao verificar execução de main.py.")
    except Exception as exc:
        erros.append(f"Erro ao rodar sonda de integridade: {exc}")

    if erros:
        return False, " | ".join(erros)
    return True, "Todos os módulos essenciais e testes de execução passaram."


def escanear_e_sanear_projeto(raiz: str, pdf_rel_atual: str) -> DadosVarredura:
    total_arquivos: int = 0
    total_linhas: int = 0
    por_extensao: Dict[str, int] = {}
    arquivos_html: List[str] = []
    avisos: List[str] = []
    faltantes: List[str] = []
    modulos_py: List[Tuple[str, int, str]] = []
    indice_por_nome: Dict[str, List[Tuple[str, int]]] = {}
    zerados_encontrados: List[Tuple[str, str, str]] = []

    permitidos_norm: Set[str] = {_normalizar_rel(p) for p in ARQUIVOS_PERMITIDOS_VAZIOS}
    apagar_norm: Set[str] = {_normalizar_rel(p) for p in ALVOS_APAGAR_DIRETO}
    pasta_reserva: str = os.path.join(raiz, "_reserva_segura")

    print("=" * 72)
    print(f"{NEGRITO}VARREDURA GERAL DO SISTEMA — RAIZ: {raiz}{RESET}")
    print("=" * 72)

    for rel_essencial in ARQUIVOS_ESSENCIAIS:
        caminho_essencial: str = os.path.join(raiz, rel_essencial.replace("/", os.sep))
        if os.path.isfile(caminho_essencial):
            _ok(f"Item essencial presente: {rel_essencial}")
        else:
            faltantes.append(f"Item essencial ausente: {rel_essencial}")

    # 1ª passada: mapear arquivos e identificar os de 0 bytes fora dos permitidos
    for atual, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]
        for nome in sorted(arquivos):
            caminho: str = os.path.join(atual, nome)
            rel_barra: str = os.path.relpath(caminho, raiz).replace("\\", "/")
            rel_low: str = _normalizar_rel(rel_barra)
            ext_item: str = os.path.splitext(nome)[1].lower()
            try:
                if os.path.isfile(caminho):
                    if ext_item == ".html":
                        arquivos_html.append(rel_barra)
                    tam: int = os.path.getsize(caminho)
                    indice_por_nome.setdefault(nome.lower(), []).append((rel_barra, tam))
                    if tam == 0 and rel_low not in permitidos_norm:
                        zerados_encontrados.append((caminho, rel_barra, nome))
            except OSError:
                pass

    termos_busca: Set[str] = set()
    for _, rel_barra, nome in zerados_encontrados:
        termos_busca.add(nome.lower())
        termos_busca.add(_normalizar_rel(rel_barra))
    citados_codigo: Set[str] = _encontrar_referencias_codigo(raiz, termos_busca)

    for caminho_z, rel_barra, nome in zerados_encontrados:
        if not os.path.exists(caminho_z):
            continue
        rel_low = _normalizar_rel(rel_barra)
        nome_low: str = nome.lower()
        ext_low: str = os.path.splitext(nome)[1].lower()

        tem_ref_codigo: bool = (nome_low in citados_codigo) or (rel_low in citados_codigo)
        if tem_ref_codigo or ext_low == ".db":
            continue

        tem_copia_com_conteudo: bool = any(
            outro_rel != rel_barra and outro_tam > 0
            for outro_rel, outro_tam in indice_por_nome.get(nome_low, [])
        )

        if rel_low in apagar_norm and not tem_copia_com_conteudo:
            try:
                os.remove(caminho_z)
                _ok(f"Sobra zerada removida: {rel_barra}")
            except OSError as exc:
                avisos.append(f"{rel_barra}: falha ao remover ({exc})")
        else:
            try:
                destino_res: str = os.path.join(pasta_reserva, rel_barra.replace("/", os.sep))
                os.makedirs(os.path.dirname(destino_res), exist_ok=True)
                shutil.move(caminho_z, destino_res)
                _ok(f"Sobra zerada movida para '_reserva_segura': {rel_barra}")
            except OSError as exc:
                avisos.append(f"{rel_barra}: falha ao mover para reserva ({exc})")

    # 2ª passada: varredura limpa do estado atual
    for atual, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]

        for nome in sorted(arquivos):
            caminho = os.path.join(atual, nome)
            rel: str = os.path.relpath(caminho, raiz)
            rel_low = _normalizar_rel(rel)
            ext: str = os.path.splitext(nome)[1].lower() or "(sem_ext)"

            try:
                if not os.path.isfile(caminho):
                    faltantes.append(f"Arquivo não regular ou inexistente: {rel}")
                    continue

                tam_bytes: int = os.path.getsize(caminho)
                if tam_bytes == 0:
                    if rel_low in permitidos_norm:
                        _ok(f"{rel} | vazio permitido (0 bytes)")
                    else:
                        avisos.append(f"{rel}: arquivo vazio (0 bytes)")

                total_arquivos += 1
                por_extensao[ext] = por_extensao.get(ext, 0) + 1

                if ext == ".py":
                    with open(caminho, "rb") as f_bin:
                        digest: str = hashlib.sha256(f_bin.read()).hexdigest()[:12].upper()
                    with open(caminho, "r", encoding="utf-8", errors="replace") as f_txt:
                        linhas: int = sum(1 for _ in f_txt)
                    total_linhas += linhas
                    modulos_py.append((rel, linhas, digest))
                    _ok(f"{rel} | {linhas} linhas | SHA-256: {digest}")
                elif tam_bytes > 0:
                    _ok(f"{rel} | tipo: {ext}")
            except (PermissionError, OSError) as exc:
                avisos.append(f"{rel}: {exc}")

    pdfs_auditados, parecer_pdfs = _auditar_pdfs_projeto(raiz, pdf_rel_atual)
    integridade_ok, detalhe_integridade = verificar_integridade_programa(raiz, faltantes)
    if not integridade_ok:
        avisos.append(f"Integridade do programa: {detalhe_integridade}")

    print("-" * 72)
    _ok(
        f"Resumo da varredura: {total_arquivos} arquivo(s) | "
        f"{len(modulos_py)} .py ({total_linhas} linhas) | "
        f"{len(arquivos_html)} .html | {len(pdfs_auditados)} .pdf inspecionado(s)"
    )

    for item_pdf in pdfs_auditados:
        if item_pdf["lacunas"]:
            _info(
                f"PDF '{item_pdf['arquivo']}' ({item_pdf['paginas']} pág., {item_pdf['chars_extraidos']} chars) -> "
                f"Pontos: {'; '.join(item_pdf['lacunas'])}"
            )
        else:
            _ok(
                f"PDF '{item_pdf['arquivo']}' ({item_pdf['paginas']} pág., {item_pdf['chars_extraidos']} chars) -> "
                "Texto íntegro na inspeção automática"
            )

    itens_vermelhos: List[str] = faltantes + avisos
    print("=" * 72)
    print(f"{VERMELHO}{NEGRITO}BLOCO FINAL — ITENS EM VERMELHO / ALERTA ({len(itens_vermelhos)}){RESET}")
    print("=" * 72)
    if itens_vermelhos:
        for item in itens_vermelhos:
            _alerta(item)
    else:
        _ok("TUDO OK — Nenhum item em vermelho ou alerta encontrado.")
    print("=" * 72)

    if integridade_ok and not itens_vermelhos:
        _ok(f"ESTADO FINAL DO PROGRAMA: ÍNTEGRO — {detalhe_integridade}")
    else:
        _alerta(f"ESTADO FINAL DO PROGRAMA: NÃO ÍNTEGRO — {detalhe_integridade}")

    _info(f"AVALIAÇÃO DOS PDFS / CONTRATOS / NORMAS: {parecer_pdfs}")
    _info(
        "Nota: Checagem automatizada de texto/cláusulas não substitui parecer jurídico "
        "de advogado em caso de venda/licenciamento do programa."
    )
    print("=" * 72)

    return {
        "total_arquivos": total_arquivos,
        "total_linhas_py": total_linhas,
        "arquivos_html": arquivos_html,
        "por_extensao": por_extensao,
        "modulos_py": modulos_py,
        "faltantes": faltantes,
        "avisos": avisos,
        "integridade_ok": integridade_ok and not itens_vermelhos,
        "detalhe_integridade": detalhe_integridade,
        "pdfs_auditados": pdfs_auditados,
        "parecer_documental_pdfs": parecer_pdfs,
    }


def gerar_pdf_varredura(caminho_pdf: str, dados: DadosVarredura, raiz: str) -> str:
    pasta_saida: str = os.path.dirname(os.path.abspath(caminho_pdf))
    os.makedirs(pasta_saida, exist_ok=True)

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
        "TituloVarredura",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=azul,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    st_sub = ParagraphStyle(
        "SubVarredura",
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor=ouro,
        alignment=TA_CENTER,
        spaceAfter=10,
    )
    st_h2 = ParagraphStyle(
        "H2Varredura",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        textColor=azul,
        spaceBefore=10,
        spaceAfter=4,
    )
    st_txt = ParagraphStyle(
        "TxtVarredura",
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        alignment=TA_JUSTIFY,
        spaceAfter=4,
    )
    st_cel_h = ParagraphStyle("CelH", fontName="Helvetica-Bold", fontSize=7.5, textColor=azul)
    st_cel = ParagraphStyle("Cel", fontName="Helvetica", fontSize=7, leading=9)

    agora_utc: str = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S UTC")
    modulos_py: List[Tuple[str, int, str]] = dados["modulos_py"]
    faltantes: List[str] = dados["faltantes"]
    avisos: List[str] = dados["avisos"]
    por_ext: Dict[str, int] = dados["por_extensao"]
    pdfs_auditados: List[AuditoriaPdfItem] = dados["pdfs_auditados"]
    status_integridade: str = "ÍNTEGRO" if dados["integridade_ok"] else "NÃO ÍNTEGRO"

    story: List[Flowable] = [
        Paragraph("RELATÓRIO DE VARREDURA GERAL DO SISTEMA", st_titulo),
        Paragraph("AUDITORIA TÉCNICA DETERMINÍSTICA • FORMATO A4", st_sub),
        Paragraph(
            f"<b>Raiz inspecionada:</b> {str(raiz)}<br/>"
            f"<b>Data/Hora (UTC):</b> {str(agora_utc)}<br/>"
            f"<b>Estado do programa:</b> {status_integridade} — {str(dados['detalhe_integridade'])}<br/>"
            f"<b>Total de arquivos:</b> {int(dados['total_arquivos'])} | "
            f"<b>Linhas em .py:</b> {int(dados['total_linhas_py'])} | "
            f"<b>Arquivos .html:</b> {len(dados['arquivos_html'])} | "
            f"<b>Alertas/Avisos:</b> {len(faltantes) + len(avisos)}",
            st_txt,
        ),
        Paragraph("PARECER DOCUMENTAL — PDFS, CONTRATOS E NORMAS", st_h2),
        Paragraph(str(dados["parecer_documental_pdfs"]), st_txt),
    ]

    for p_item in pdfs_auditados[:30]:
        lac_txt: str = (
            f"Lacunas/pontos: {'; '.join(p_item['lacunas'])}"
            if p_item["lacunas"]
            else "Sem lacunas textuais detectadas"
        )
        story.append(
            Paragraph(
                f"• <b>{str(p_item['arquivo'])}</b> ({int(p_item['paginas'])} pág., "
                f"{int(p_item['chars_extraidos'])} chars): {lac_txt}",
                st_txt,
            )
        )

    story.append(Paragraph("RESUMO POR EXTENSÃO", st_h2))
    ext_rows: List[List[Paragraph]] = [
        [Paragraph("<b>Extensão</b>", st_cel_h), Paragraph("<b>Quantidade</b>", st_cel_h)]
    ]
    for ext, qtd in sorted(por_ext.items(), key=lambda x: (-x[1], x[0]))[:15]:
        ext_rows.append([Paragraph(str(ext), st_cel), Paragraph(str(int(qtd)), st_cel)])

    t_ext = Table(ext_rows, colWidths=[largura_util * 0.65, largura_util * 0.35])
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

    story.append(Paragraph("ARQUIVOS PYTHON (.PY) INSPECIONADOS", st_h2))
    py_rows: List[List[Paragraph]] = [
        [
            Paragraph("<b>Arquivo</b>", st_cel_h),
            Paragraph("<b>Linhas</b>", st_cel_h),
            Paragraph("<b>SHA-256 (12)</b>", st_cel_h),
        ]
    ]
    for rel, linhas, digest in modulos_py[:120]:
        py_rows.append(
            [
                Paragraph(str(rel), st_cel),
                Paragraph(str(int(linhas)), st_cel),
                Paragraph(f"<font name='Courier'>{str(digest)}</font>", st_cel),
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

    if len(modulos_py) > 120:
        story.append(Spacer(1, 4))
        story.append(
            Paragraph(
                f"<i>Exibindo os primeiros 120 de {len(modulos_py)} arquivos .py para manter o relatório compacto e rápido.</i>",
                st_txt,
            )
        )

    if faltantes or avisos:
        story.append(Paragraph("BLOCO FINAL — ITENS AUSENTES / ALERTAS / AVISOS", st_h2))
        for item in faltantes[:30]:
            story.append(Paragraph(f"• [ALERTA] {str(item)}", st_txt))
        for av in avisos[:30]:
            story.append(Paragraph(f"• [ALERTA] {str(av)}", st_txt))

    doc.build(story)
    return caminho_pdf


def executar_varredura() -> None:
    _habilitar_cores_windows()
    raiz: str = os.path.abspath(os.path.dirname(__file__))
    destino: str = os.path.join(raiz, "pdfs_finais", "07_Varredura_Geral_Sistema.pdf")
    pdf_rel_atual: str = os.path.relpath(destino, raiz).replace("\\", "/")
    dados: DadosVarredura = escanear_e_sanear_projeto(raiz, pdf_rel_atual)
    gerar_pdf_varredura(destino, dados, raiz)

    if os.path.exists(destino) and os.path.getsize(destino) > 0:
        tamanho_kb: float = os.path.getsize(destino) / 1024.0
        _ok(f"PDF gerado em 'pdfs_finais': {destino} ({tamanho_kb:.2f} KB)")
    else:
        _alerta("O PDF de varredura não foi gerado corretamente.")
        sys.exit(1)


if __name__ == "__main__":
    executar_varredura()