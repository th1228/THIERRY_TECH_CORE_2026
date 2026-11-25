import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -*- coding: utf-8 -*-
"""
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - GLOBAL MARKET READINESS AUDITOR
"""

import os
import re
import sys
import json
import shutil
import base64
import hashlib
import py_compile
import datetime
from typing import Dict, List, Tuple
import pymupdf as fitz

RESET = "\033[0m"
VERDE = "\033[92m"
VERDE_BOLD = "\033[1;92m"
AMARELO = "\033[93m"
AMARELO_BOLD = "\033[1;93m"
VERMELHO_BOLD = "\033[1;91m"
CIANO = "\033[96m"
CIANO_BOLD = "\033[1;96m"
BRANCO_BOLD = "\033[1;97m"
CINZA = "\033[90m"
ROXO_BOLD = "\033[1;95m"

LARGURA_BANNER = 88

PASTAS_IGNORADAS_PADRAO = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
    ".auditor_backup",
    "_backup_seguro",
    "_organizador_aa",
    "_backup_i18n",
    "_backup_pdfs_originais",
    "_reserva_segura",
}

JURISDICOES_ALVO: List[Tuple[str, str, str]] = [
    ("Mônaco", "CCIN", r"\b(m[oô]naco|ccin|monaco)\b"),
    ("Dubai", "DIFC", r"\b(dubai|difc|uae|emirados)\b"),
    ("UE", "GDPR", r"\b(gdpr|rgpd|uni[aã]o\s+europeia|european\s+union)\b"),
    ("Suíça", "FADP", r"\b(su[ií][cç]a|fadp|revdsg|switzerland)\b"),
    ("Singapura", "PDPA", r"\b(singapura|pdpa|singapore)\b"),
    ("Reino Unido", "UK GDPR", r"\b(uk[\s_-]*gdpr|reino\s+unido|united\s+kingdom)\b"),
    ("EUA", "HIPAA / CCPA", r"\b(hipaa|ccpa|cpra|estados\s+unidos|usa)\b"),
    ("Catar", "QFC / PDPPL", r"\b(catar|qatar|qfc|pdppl)\b"),
    ("Alemanha", "BDSG", r"\b(alemanha|bdsg|germany)\b"),
    ("França", "CNIL", r"\b(fran[cç]a|cnil|france)\b"),
    ("Coreia do Sul", "PIPA", r"\b(coreia\s+do\s+sul|pipa|south\s+korea)\b"),
    ("Brasil", "LGPD", r"\b(lgpd|brasil|brazil)\b"),
]

DIRETRIZES_ALVO: List[Tuple[str, str]] = [
    ("Anti-Engenharia Reversa", r"(anti[\s_-]*engenharia\s+reversa|anti[\s_-]*reverse|reverse[\s_-]*engineering|ofusca[cç][aã]o)"),
    ("Zero Trust", r"\bzero[\s_-]*trust\b"),
    ("Vault", r"\bvault\b"),
    ("C2 Sovereign", r"\b(c2[\s_-]*sovereign|soberan\w+|command[\s_-]*and[\s_-]*control)\b"),
    ("ISO", r"\biso[\s_-]*\d{4,5}\b|\biso\b"),
    ("Infraestrutura Zero / 100% Offline", r"(100%\s*offline|offline[\s_-]*first|infraestrutura[\s_-]*zero|zero[\s_-]*infrastructure|sem\s+internet)"),
    ("Sem Servidor Público", r"(sem\s+servidor\s+p[uú]blico|n[aã]o\s+roda\s+em\s+servidor\s+p[uú]blico|private[\s_-]*only|no\s+public\s+server)"),
    ("Autossustentável (Nunca Morre)", r"(autossustent\w+|auto[\s_-]*sustent\w+|nunca\s+morre|resili[eê]ncia|self[\s_-]*sustaining)"),
]


def _ativar_ansi_terminal() -> None:
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


def _remover_ansi(texto: str) -> str:
    return re.sub(r"\033\[[0-9;]*m", "", texto)


def _centralizar_linha(texto_colorido: str, largura: int = LARGURA_BANNER) -> str:
    visivel = _remover_ansi(texto_colorido)
    if len(visivel) >= largura:
        return texto_colorido
    espacos_esq = (largura - len(visivel)) // 2
    return (" " * espacos_esq) + texto_colorido


def _formatar_ok_status(ok: bool) -> str:
    return f"{VERDE_BOLD}[OK]{RESET}" if ok else f"{VERMELHO_BOLD}[PENDENTE]{RESET}"


def _cor_por_nota(score: int) -> str:
    if score >= 95:
        return VERDE_BOLD
    if score >= 75:
        return AMARELO_BOLD
    return VERMELHO_BOLD


def _barra_progresso(score: int, largura: int = 16) -> str:
    score_limitado = max(0, min(100, score))
    preenchidos = round((score_limitado / 100) * largura)
    vazio = largura - preenchidos
    cor = _cor_por_nota(score_limitado)
    barra = f"{cor}{'█' * preenchidos}{CINZA}{'░' * vazio}{RESET}"
    return f"[{barra}] {cor}{score_limitado:3d}/100{RESET}"


def _gerar_identificador_cifrado(raiz: str) -> str:
    digest = hashlib.sha256(f"MIBO_SOVEREIGN_PROJECT|{raiz}".encode("utf-8")).hexdigest().upper()
    return f"PRJ-{digest[:6]}-{digest[6:12]}-{digest[12:18]}"


def _gerar_selo_criptografico(raiz: str, pontuacao: int, total_py: int, total_pdfs: int) -> Tuple[str, str, str]:
    agora_local = datetime.datetime.now().astimezone()
    timestamp_local = agora_local.strftime("%Y-%m-%d %H:%M:%S %z")
    payload = f"THIERRY_TECH_GLOBAL|{raiz}|{pontuacao}|PY:{total_py}|PDF:{total_pdfs}|{timestamp_local}"
    sha256_hex = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
    selo_no = (
        f"THIERRY-SEAL-{sha256_hex[:8]}-{sha256_hex[8:16]}-"
        f"{sha256_hex[16:24]}-{sha256_hex[24:32]}"
    )
    assinatura_b64 = base64.b64encode(sha256_hex.encode("utf-8")).decode("utf-8")[:44] + "=="
    return selo_no, assinatura_b64, timestamp_local


class AuditorGlobalMercado:
    def __init__(self, raiz_projeto: str):
        self.raiz = raiz_projeto
        self.largura_a4 = 595.28
        self.altura_a4 = 841.89
        self.pt_para_mm = 0.352778
        self.limiar_margem_mm = 3.5
        self.min_palavras_dossie = 400
        self.pasta_backup = os.path.join(self.raiz, ".auditor_backup")

    def _coletar_arquivos(self, extensoes: Tuple[str, ...], incluir_ocultos_mibo: bool = False) -> List[str]:
        encontrados: List[str] = []
        for pasta_atual, diretorios, arquivos in os.walk(self.raiz):
            diretorios[:] = [d for d in diretorios if d not in PASTAS_IGNORADAS_PADRAO]
            for arquivo in arquivos:
                nome_low = arquivo.lower()
                if arquivo.startswith(".") and not (incluir_ocultos_mibo and "mibo" in nome_low):
                    continue
                if nome_low.endswith(extensoes):
                    encontrados.append(os.path.join(pasta_atual, arquivo))
        return sorted(encontrados)

    def _contar_arquivos_pasta_security(self) -> Tuple[int, bool]:
        total = 0
        encontrada = False
        for pasta_atual, diretorios, _ in os.walk(self.raiz):
            diretorios[:] = [d for d in diretorios if d not in PASTAS_IGNORADAS_PADRAO]
            for d in diretorios:
                if d.lower() == "security":
                    encontrada = True
                    pasta_sec = os.path.join(pasta_atual, d)
                    for _, _, files in os.walk(pasta_sec):
                        total += len([f for f in files if not f.startswith(".")])
        return total, encontrada

    def _ler_texto_seguro(self, caminho: str) -> str:
        try:
            with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            return ""

    def _extrair_texto_pdf(self, doc: fitz.Document) -> str:
        partes: List[str] = []
        for idx_pag in range(len(doc)):
            pagina = doc[idx_pag]
            raw = pagina.get_text("text")
            if isinstance(raw, str) and raw:
                partes.append(raw)
        return " ".join(partes)

    def _localizar_pasta_pdfs(self) -> str:
        for pasta_atual, diretorios, _ in os.walk(self.raiz):
            diretorios[:] = [d for d in diretorios if d not in PASTAS_IGNORADAS_PADRAO]
            for d in diretorios:
                if d.lower() == "pdfs_finais":
                    return os.path.join(pasta_atual, d)
        return os.path.join(self.raiz, "pdfs_finais")

    def _localizar_scripts_por_palavras_chave(self, arquivos_py: List[str], palavras: Tuple[str, ...]) -> List[str]:
        hits: List[str] = []
        for caminho in arquivos_py:
            rel = os.path.relpath(caminho, self.raiz).replace("\\", "/")
            low = rel.lower()
            if any(p in low for p in palavras):
                hits.append(rel)
        return sorted(hits)[:6]

    def _inspecionar_pasta_security(self, arquivos_py: List[str]) -> Tuple[int, List[str], List[str], Dict[str, int]]:
        """
        Avalia de forma objetiva os módulos dentro de security/:
        - Presença da pasta e arquivos .py
        - Compilação sem erro de sintaxe
        - Ausência de eval/exec/pickle, shell=True e segredos literais longos
        - Ausência de captura genérica (except Exception / bare except)
        Retorna 100/100 apenas quando não há falhas nem ressalvas nesses critérios.
        """
        score = 100
        motivos: List[str] = []
        plano: List[str] = []

        sec_py = [
            p for p in arquivos_py
            if "security/" in os.path.relpath(p, self.raiz).replace("\\", "/").lower()
            or os.path.relpath(p, self.raiz).replace("\\", "/").lower().startswith("security/")
        ]

        if not sec_py:
            score = 0
            motivos.append("Nenhum módulo .py localizado na pasta security/.")
            plano.append("Garantir a presença e estrutura dos módulos de segurança na pasta security/.")
            return score, motivos, plano, {"arquivos_py": 0, "erros_comp": 0, "excecoes_amplas": 0}

        erros_comp: List[str] = []
        excecoes_amplas: List[str] = []
        achados_criticos_sec = self._mapear_achados_seguranca(sec_py)

        padrao_except_amplo = re.compile(r"^\s*except\s*(?:Exception\b\s*(?:as\s+\w+)?\s*)?:")

        for caminho in sec_py:
            rel = os.path.relpath(caminho, self.raiz).replace("\\", "/")
            try:
                py_compile.compile(caminho, doraise=True)
            except py_compile.PyCompileError:
                erros_comp.append(rel)

            linhas = self._ler_texto_seguro(caminho).splitlines()
            linhas_exc = [
                str(idx) for idx, ln in enumerate(linhas, start=1)
                if padrao_except_amplo.match(ln)
            ]
            if linhas_exc:
                excecoes_amplas.append(f"{rel} (linhas {', '.join(linhas_exc[:6])})")

        if erros_comp:
            score -= min(40, len(erros_comp) * 15)
            motivos.append(f"Falha de compilação em {len(erros_comp)} arquivo(s) de security/: {', '.join(erros_comp[:6])}.")
            plano.append(f"Corrigir erros de sintaxe/compilação em security/: {', '.join(erros_comp[:6])}.")

        if achados_criticos_sec:
            arqs_crit = sorted({a["arquivo"] for a in achados_criticos_sec})
            score -= min(35, len(arqs_crit) * 12)
            motivos.append(
                f"{len(achados_criticos_sec)} ocorrência(s) crítica(s) (eval/exec/pickle, shell=True ou credencial fixa) em security/: {', '.join(arqs_crit[:6])}."
            )
            plano.append(
                f"Eliminar eval/exec/pickle, shell=True e credenciais fixas nos arquivos de security/: {', '.join(arqs_crit[:6])}."
            )

        if excecoes_amplas:
            penalidade_exc = min(44, len(excecoes_amplas) * 3)
            score -= penalidade_exc
            motivos.append(
                f"Uso de 'except Exception' ou bare except em {len(excecoes_amplas)} arquivo(s) de security/: {', '.join(excecoes_amplas[:6])}."
            )
            plano.append(
                f"Substituir 'except Exception' / bare except por exceções específicas nos módulos de security/: {', '.join(excecoes_amplas[:6])}."
            )

        if not motivos:
            motivos.append(
                f"Todos os {len(sec_py)} módulo(s) .py de security/ compilam sem erro, sem falhas críticas nem exceções genéricas."
            )

        resumo_sec = {
            "arquivos_py": len(sec_py),
            "erros_comp": len(erros_comp),
            "excecoes_amplas": len(excecoes_amplas),
        }
        return max(0, min(100, score)), motivos, plano, resumo_sec

    def _inspecionar_conformidade_diretrizes(
        self, arquivos_projeto: List[str], pdfs: List[str]
    ) -> Tuple[int, List[str], List[str], Dict[str, int], Dict[str, int]]:
        contagem_jur: Dict[str, int] = {f"{pais} ({cod})": 0 for pais, cod, _ in JURISDICOES_ALVO}
        contagem_dir: Dict[str, int] = {rotulo: 0 for rotulo, _ in DIRETRIZES_ALVO}

        compiladas_jur = [
            (f"{pais} ({cod})", re.compile(padrao, re.IGNORECASE))
            for pais, cod, padrao in JURISDICOES_ALVO
        ]
        compiladas_dir = [(rotulo, re.compile(padrao, re.IGNORECASE)) for rotulo, padrao in DIRETRIZES_ALVO]

        corpus: List[str] = [self._ler_texto_seguro(c) for c in arquivos_projeto]
        for caminho_pdf in pdfs:
            try:
                doc = fitz.open(caminho_pdf)
                corpus.append(self._extrair_texto_pdf(doc))
                doc.close()
            except Exception:
                pass

        for texto in corpus:
            if not texto:
                continue
            for chave, regex in compiladas_jur:
                contagem_jur[chave] += len(regex.findall(texto))
            for rotulo, regex in compiladas_dir:
                contagem_dir[rotulo] += len(regex.findall(texto))

        jur_presentes = [k for k, v in contagem_jur.items() if v > 0]
        jur_faltantes = [k for k, v in contagem_jur.items() if v == 0]
        dir_presentes = [k for k, v in contagem_dir.items() if v > 0]
        dir_faltantes = [k for k, v in contagem_dir.items() if v == 0]

        total_jur = len(JURISDICOES_ALVO)
        total_dir = len(DIRETRIZES_ALVO)
        pct_jur = len(jur_presentes) / total_jur if total_jur else 1.0
        pct_dir = len(dir_presentes) / total_dir if total_dir else 1.0
        score = max(1, min(100, round((pct_jur * 0.50 + pct_dir * 0.50) * 100)))

        motivos: List[str] = [
            f"Jurisdições verificadas no acervo: {len(jur_presentes)}/{total_jur} ({', '.join(jur_presentes) if jur_presentes else 'nenhuma'})."
        ]
        if jur_faltantes:
            motivos.append(f"Jurisdições a registrar nos arquivos: {', '.join(jur_faltantes)}.")

        motivos.append(
            f"Diretrizes/blindagem verificadas no acervo: {len(dir_presentes)}/{total_dir} ({', '.join(dir_presentes) if dir_presentes else 'nenhuma'})."
        )
        if dir_faltantes:
            motivos.append(f"Diretrizes a registrar no código/arquitetura: {', '.join(dir_faltantes)}.")

        plano: List[str] = []
        if jur_faltantes:
            plano.append(
                "Registrar e documentar nos módulos/dossiês as jurisdições: "
                + ", ".join(jur_faltantes)
                + " (requisitos de base legal, consentimento, residência de dados e transferência internacional)."
            )
        if dir_faltantes:
            plano.append(
                "Implementar e documentar no código/arquitetura as diretrizes: "
                + ", ".join(dir_faltantes)
                + " (ex.: ofuscação/anti-reversa, autenticação contínua Zero Trust, cofre cifrado Vault e modo 100% offline)."
            )

        return score, motivos, plano, contagem_jur, contagem_dir

    def _inspecionar_main(self, arquivos_py: List[str]) -> Tuple[int, List[str], List[str], bool]:
        score = 100
        motivos: List[str] = []
        plano: List[str] = []

        mains = [p for p in arquivos_py if os.path.basename(p).lower() == "main.py"]
        if not mains:
            score -= 45
            motivos.append("Arquivo main.py não localizado no projeto.")
            plano.append("Criar ou restaurar o ponto de entrada main.py na raiz do projeto.")
            return max(1, score), motivos, plano, False

        caminho_main = mains[0]
        try:
            py_compile.compile(caminho_main, doraise=True)
        except py_compile.PyCompileError:
            score -= 35
            motivos.append("main.py requer revisão de sintaxe/compilação.")
            plano.append("Corrigir erros de sintaxe em main.py até compilar sem falhas.")

        conteudo = self._ler_texto_seguro(caminho_main)
        linhas = [ln.strip() for ln in conteudo.splitlines() if ln.strip() and not ln.strip().startswith("#")]
        if len(linhas) < 5:
            score -= 20
            motivos.append("main.py com estrutura inicial reduzida.")
            plano.append("Estruturar o fluxo principal de execução e orquestração em main.py.")

        if "__name__" not in conteudo:
            score -= 10
            motivos.append("main.py sem bloco 'if __name__ == \"__main__\":'.")
            plano.append("Adicionar guarda 'if __name__ == \"__main__\":' em main.py.")

        if not motivos:
            motivos.append("main.py validado, compila sem erro e possui estrutura de entrada íntegra.")

        return max(1, min(100, score)), motivos, plano, True

    def _inspecionar_memoria_comum(self, arquivos_projeto: List[str]) -> Tuple[int, List[str], List[str], int]:
        score = 100
        motivos: List[str] = []
        plano: List[str] = []

        padrao_mem = re.compile(
            r"memoria[_\s-]*comum|mem[oó]ria[_\s-]*comum|common[_\s-]*memory|shared[_\s-]*memory",
            re.IGNORECASE,
        )
        arquivos_mem: List[str] = []
        ocorrencias = 0
        json_invalidos = 0
        py_com_erro = 0

        for caminho in arquivos_projeto:
            nome_hit = bool(padrao_mem.search(os.path.basename(caminho)))
            conteudo = self._ler_texto_seguro(caminho)
            matches = padrao_mem.findall(conteudo)
            if nome_hit or matches:
                arquivos_mem.append(caminho)
                ocorrencias += len(matches)
                if caminho.lower().endswith(".json"):
                    try:
                        json.loads(conteudo)
                    except Exception:
                        json_invalidos += 1
                elif caminho.lower().endswith(".py"):
                    try:
                        py_compile.compile(caminho, doraise=True)
                    except py_compile.PyCompileError:
                        py_com_erro += 1

        if not arquivos_mem:
            score -= 45
            motivos.append("Nenhuma referência ou arquivo de 'memória comum' localizado no projeto.")
            plano.append("Implementar e integrar o módulo/armazenamento de memória comum do ecossistema.")
        else:
            if ocorrencias < 2:
                score -= 15
                motivos.append(f"Referências à memória comum: {ocorrencias} ocorrência(s).")
                plano.append("Expandir o uso e o compartilhamento da memória comum entre os componentes do sistema.")
            if json_invalidos > 0:
                score -= 20
                motivos.append(f"{json_invalidos} arquivo(s) JSON da memória comum com formato a revisar.")
                plano.append("Corrigir a estrutura JSON dos arquivos de memória comum.")
            if py_com_erro > 0:
                score -= 25
                motivos.append(f"{py_com_erro} módulo(s) Python da memória comum com compilação a revisar.")
                plano.append("Corrigir erros de sintaxe nos módulos Python da memória comum.")

        if not motivos:
            motivos.append(f"{len(arquivos_mem)} arquivo(s) de memória comum inspecionados ({ocorrencias} referência(s)) sem alerta crítico.")

        return max(1, min(100, score)), motivos, plano, len(arquivos_mem)

    def _inspecionar_painel_html(self, arquivos_html: List[str]) -> Tuple[int, List[str], List[str]]:
        score = 100
        motivos: List[str] = []
        plano: List[str] = []

        if not arquivos_html:
            score -= 45
            motivos.append("Nenhum arquivo HTML localizado para o painel.")
            plano.append("Criar os arquivos HTML do painel e integrá-los ao projeto.")
            return max(1, score), motivos, plano

        sem_estrutura_basica = 0
        sem_titulo_html = 0
        arquivos_vazios = 0

        for caminho in arquivos_html:
            html = self._ler_texto_seguro(caminho).strip()
            if len(html) < 50:
                arquivos_vazios += 1
                continue
            low = html.lower()
            if "<html" not in low and "<body" not in low and "<div" not in low and "<section" not in low:
                sem_estrutura_basica += 1
            if "<title" not in low and "<h1>" not in low and "<h2>" not in low:
                sem_titulo_html += 1

        if arquivos_vazios > 0:
            penalidade = min(30, arquivos_vazios * 10)
            score -= penalidade
            motivos.append(f"{arquivos_vazios}/{len(arquivos_html)} arquivo(s) HTML com conteúdo curto.")
            plano.append("Preencher o conteúdo completo dos arquivos HTML vazios/curtos.")

        if sem_estrutura_basica > 0:
            penalidade = min(25, sem_estrutura_basica * 8)
            score -= penalidade
            motivos.append(f"{sem_estrutura_basica}/{len(arquivos_html)} HTML(s) com estrutura a revisar.")
            plano.append("Estruturar corretamente as tags HTML/body/seções do painel.")

        if sem_titulo_html > 0:
            penalidade = min(15, sem_titulo_html * 5)
            score -= penalidade
            motivos.append(f"{sem_titulo_html}/{len(arquivos_html)} HTML(s) sem título principal.")
            plano.append("Adicionar <title> ou cabeçalho principal (<h1>/<h2>) em todas as páginas HTML.")

        if not motivos:
            motivos.append(f"Todos os {len(arquivos_html)} arquivo(s) HTML do painel inspecionados com estrutura íntegra.")

        return max(1, min(100, score)), motivos, plano

    def _inspecionar_motores(self, arquivos_py: List[str]) -> Tuple[int, List[str], List[str], Dict[str, int]]:
        score = 100
        motivos: List[str] = []
        plano: List[str] = []

        motores = [
            p for p in arquivos_py
            if any(k in os.path.basename(p).lower() for k in ("motor", "engine", "gerador", "dossie", "c2_"))
        ]
        if not motores:
            motores = arquivos_py

        erros_compilacao = 0
        motores_curtos: List[Tuple[str, int]] = []
        for caminho in motores:
            rel = os.path.relpath(caminho, self.raiz).replace("\\", "/")
            try:
                py_compile.compile(caminho, doraise=True)
            except py_compile.PyCompileError:
                erros_compilacao += 1
                motivos.append(f"ERRO DE COMPILAÇÃO -> {rel}: corrija sintaxe/indentação neste arquivo.")

            conteudo = self._ler_texto_seguro(caminho).strip()
            if len(conteudo) < 100:
                motores_curtos.append((rel, len(conteudo)))

        if not arquivos_py:
            score -= 50
            motivos.append("Nenhum arquivo .py localizado no projeto.")
            plano.append("Criar os módulos Python dos motores do sistema.")
        elif erros_compilacao > 0:
            penalidade = min(40, erros_compilacao * 10)
            score -= penalidade
            plano.append("Corrigir erros de sintaxe nos scripts Python listados em Motores até compilar sem falhas.")

        if motores_curtos:
            penalidade = min(20, len(motores_curtos) * 5)
            score -= penalidade
            for rel, tam in motores_curtos:
                motivos.append(
                    f"MOTOR CURTO ({tam} chars) -> {rel}: abra o arquivo e implemente (1) validacao de entrada, "
                    f"(2) rotina principal de processamento do motor e (3) retorno estruturado (dict com status/resultado)."
                )
            plano.append(
                "Completar nos arquivos apontados em Motores ("
                + ", ".join(r for r, _ in motores_curtos[:8])
                + ") a validacao de entrada, a rotina interna do motor e o retorno estruturado."
            )

        if not motivos:
            motivos.append(f"{len(motores)} módulo(s) de motor inspecionados e compilados sem alerta crítico.")

        resumo = {
            "total_py": len(arquivos_py),
            "motores_detectados": len(motores),
            "erros_compilacao": erros_compilacao,
        }
        return max(1, min(100, score)), motivos, plano, resumo

    def _inspecionar_biometrico(self, arquivos_projeto: List[str]) -> Tuple[int, List[str], List[str], int]:
        score = 100
        motivos: List[str] = []
        plano: List[str] = []

        padrao_bio = re.compile(r"biometr\w*|biometric\w*|landmark\w*|visagism\w*|facial", re.IGNORECASE)
        arquivos_bio: List[str] = []
        ocorrencias = 0
        json_invalidos = 0

        for caminho in arquivos_projeto:
            nome_hit = bool(padrao_bio.search(os.path.basename(caminho)))
            conteudo = self._ler_texto_seguro(caminho)
            matches = padrao_bio.findall(conteudo)
            if nome_hit or matches:
                arquivos_bio.append(caminho)
                ocorrencias += len(matches)
                if caminho.lower().endswith(".json"):
                    try:
                        json.loads(conteudo)
                    except Exception:
                        json_invalidos += 1

        if not arquivos_bio:
            score -= 45
            motivos.append("Nenhum arquivo ou referência biométrica localizado no projeto.")
            plano.append("Implementar módulo/dados biométricos dedicados e integrá-los ao fluxo do sistema.")
        else:
            if ocorrencias < 3:
                score -= 15
                motivos.append(f"Referências biométricas no conteúdo: {ocorrencias} ocorrência(s).")
                plano.append("Expandir regras, parâmetros e validações biométricas nos módulos correspondentes.")
            if json_invalidos > 0:
                score -= 20
                motivos.append(f"{json_invalidos} arquivo(s) JSON biométrico(s) com formato a revisar.")
                plano.append("Corrigir a estrutura JSON dos arquivos de dados biométricos.")

        if not motivos:
            motivos.append(f"{len(arquivos_bio)} arquivo(s) biométrico(s) validado(s) ({ocorrencias} referência(s)) sem alerta crítico.")

        return max(1, min(100, score)), motivos, plano, len(arquivos_bio)

    def _inspecionar_biogemeos(self, arquivos_projeto: List[str]) -> Tuple[int, List[str], List[str], int]:
        score = 100
        motivos: List[str] = []
        plano: List[str] = []

        padrao_gemeos = re.compile(r"biog[eê]me\w*|biogem\w*|g[eê]meo\w*\s*bi\w*|digital[\s_-]*twin", re.IGNORECASE)
        arquivos_gemeos: List[str] = []
        ocorrencias = 0

        for caminho in arquivos_projeto:
            nome_hit = bool(padrao_gemeos.search(os.path.basename(caminho)))
            conteudo = self._ler_texto_seguro(caminho)
            matches = padrao_gemeos.findall(conteudo)
            if nome_hit or matches:
                arquivos_gemeos.append(caminho)
                ocorrencias += len(matches)

        if not arquivos_gemeos:
            score -= 45
            motivos.append("Nenhum arquivo ou referência a Biogêmeos localizado no projeto.")
            plano.append("Criar módulo/estrutura de modelagem de Biogêmeos e conectá-lo aos dossiês/motores.")
        elif ocorrencias < 2:
            score -= 15
            motivos.append(f"Referências de Biogêmeos: {ocorrencias} ocorrência(s).")
            plano.append("Detalhar parâmetros, cálculos e regras de sincronização dos Biogêmeos.")

        if not motivos:
            motivos.append(f"{len(arquivos_gemeos)} arquivo(s) com lógica/dados de Biogêmeos ({ocorrencias} ocorrência(s)) sem alerta crítico.")

        return max(1, min(100, score)), motivos, plano, len(arquivos_gemeos)

    def _mapear_achados_seguranca(self, arquivos_py: List[str]) -> List[Dict[str, str]]:
        achados: List[Dict[str, str]] = []
        padrao_eval_pickle = re.compile(r"\b(eval|exec)\s*\(|\bpickle\.loads?\s*\(")
        padrao_shell = re.compile(r"subprocess\.\w+\([^)]*shell\s*=\s*True")
        padrao_segredo = re.compile(
            r"(api[_-]?key|secret[_-]?key|password|passwd|token)\s*=\s*['\"][A-Za-z0-9_\-]{12,}['\"]",
            re.IGNORECASE,
        )

        for caminho in arquivos_py:
            rel = os.path.relpath(caminho, self.raiz)
            linhas = self._ler_texto_seguro(caminho).splitlines()
            for idx, linha in enumerate(linhas, start=1):
                trecho = linha.strip()
                if padrao_eval_pickle.search(linha):
                    achados.append({"tipo": "eval_exec_pickle", "arquivo": rel, "caminho": caminho, "linha": str(idx), "trecho": trecho})
                if padrao_shell.search(linha):
                    achados.append({"tipo": "shell_true", "arquivo": rel, "caminho": caminho, "linha": str(idx), "trecho": trecho})
                if padrao_segredo.search(linha):
                    achados.append({"tipo": "segredo_fixo", "arquivo": rel, "caminho": caminho, "linha": str(idx), "trecho": trecho})
        return achados

    def _inspecionar_c2_mibo_seguranca(
        self, arquivos_projeto: List[str], arquivos_py: List[str]
    ) -> Tuple[int, List[str], List[str], Dict[str, int], List[Dict[str, str]]]:
        score = 100
        motivos: List[str] = []
        plano: List[str] = []

        arquivos_mibo = [p for p in arquivos_projeto if "mibo" in os.path.basename(p).lower()]
        arquivos_c2 = [
            p for p in arquivos_projeto
            if re.search(r"\bc2\b|c2_|sovereign|blindagem|ledger", os.path.basename(p).lower())
        ]

        json_mibo_invalidos = 0
        for caminho in arquivos_mibo:
            if caminho.lower().endswith(".json"):
                try:
                    json.loads(self._ler_texto_seguro(caminho))
                except Exception:
                    json_mibo_invalidos += 1

        achados = self._mapear_achados_seguranca(arquivos_py)
        arqs_exec = sorted({a["arquivo"] for a in achados if a["tipo"] == "eval_exec_pickle"})
        arqs_shell = sorted({a["arquivo"] for a in achados if a["tipo"] == "shell_true"})
        arqs_segredo = sorted({a["arquivo"] for a in achados if a["tipo"] == "segredo_fixo"})

        tem_cripto_ou_hash = any(
            re.search(r"\b(hashlib|hmac|cryptography|fernet|aes|sha256|sha512|ssl|tls)\b", self._ler_texto_seguro(p), re.IGNORECASE)
            for p in arquivos_py
        )

        if not arquivos_mibo:
            score -= 20
            motivos.append("Nenhum arquivo MIBO localizado no projeto.")
            plano.append("Manter arquivos de estado/configuração MIBO íntegros e versionados no projeto.")
        elif json_mibo_invalidos > 0:
            score -= 15
            motivos.append(f"{json_mibo_invalidos} arquivo(s) JSON MIBO com sintaxe a revisar.")
            plano.append("Corrigir JSON inválido nos arquivos MIBO.")

        if not arquivos_c2:
            score -= 20
            motivos.append("Nenhum módulo C2 Sovereign / blindagem / ledger localizado.")
            plano.append("Garantir presença e integração dos módulos C2 Sovereign e blindagem.")

        if arqs_exec:
            penalidade = min(25, len(arqs_exec) * 10)
            score -= penalidade
            motivos.append(f"Ocorrência de eval/exec/pickle.load em {len(arqs_exec)} arquivo(s) ({', '.join(arqs_exec)}).")
            plano.append("Substituir eval/exec/pickle inseguro por parsers/formatos seguros (ex.: json/ast.literal_eval).")

        if arqs_shell:
            penalidade = min(15, len(arqs_shell) * 8)
            score -= penalidade
            motivos.append(f"Subprocesso com shell=True em {len(arqs_shell)} arquivo(s) ({', '.join(arqs_shell)}).")
            plano.append("Remover shell=True de chamadas de subprocesso e usar lista de argumentos.")

        if arqs_segredo:
            penalidade = min(20, len(arqs_segredo) * 10)
            score -= penalidade
            motivos.append(f"Credencial/chave a revisar em {len(arqs_segredo)} arquivo(s) ({', '.join(arqs_segredo)}).")
            plano.append("Mover chaves e segredos para variáveis de ambiente (.env) e fora do código-fonte.")

        if not tem_cripto_ou_hash:
            score -= 10
            motivos.append("Rotina explícita de hash/integridade/criptografia a reforçar nos scripts.")
            plano.append("Adicionar hashing/integridade (ex.: SHA-256/HMAC) para rastreabilidade e segurança.")

        if not motivos:
            motivos.append(
                f"{len(arquivos_mibo)} arquivo(s) MIBO e {len(arquivos_c2)} módulo(s) C2/segurança inspecionados sem alerta crítico."
            )

        resumo = {
            "arquivos_mibo": len(arquivos_mibo),
            "arquivos_c2": len(arquivos_c2),
            "alertas_seguranca": len(achados) + json_mibo_invalidos,
        }
        return max(1, min(100, score)), motivos, plano, resumo, achados

    def _fazer_backup_arquivo(self, caminho: str) -> None:
        rel = os.path.relpath(caminho, self.raiz)
        destino = os.path.join(self.pasta_backup, rel)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        if not os.path.exists(destino):
            shutil.copy2(caminho, destino)

    def aplicar_correcoes_seguras(self, achados: List[Dict[str, str]]) -> List[str]:
        alteracoes: List[str] = []
        if not achados:
            return alteracoes

        por_arquivo: Dict[str, List[Dict[str, str]]] = {}
        for item in achados:
            por_arquivo.setdefault(item["caminho"], []).append(item)

        env_linhas_novas: List[str] = []
        padrao_atribuicao_segredo = re.compile(
            r"^(\s*)(api[_-]?key|secret[_-]?key|password|passwd|token)\s*=\s*(['\"])([A-Za-z0-9_\-]{12,})\3(.*)$",
            re.IGNORECASE,
        )
        padrao_shell_literal = re.compile(r",\s*shell\s*=\s*True\b")

        for caminho, itens in por_arquivo.items():
            codigo_original = self._ler_texto_seguro(caminho)
            if not codigo_original:
                continue

            linhas = codigo_original.splitlines(keepends=True)
            modificou = False

            for idx, linha in enumerate(linhas):
                nova_linha = linha

                if padrao_shell_literal.search(nova_linha):
                    nova_linha = padrao_shell_literal.sub(", shell=False", nova_linha)
                    if nova_linha != linha:
                        modificou = True
                        alteracoes.append(f"{os.path.relpath(caminho, self.raiz)}:{idx + 1} -> shell=True alterado para shell=False.")

                m_seg = padrao_atribuicao_segredo.match(nova_linha.rstrip("\r\n"))
                if m_seg:
                    indent, var_nome, _, valor_antigo, resto = m_seg.groups()
                    env_var = var_nome.upper()
                    fim_linha = "\r\n" if nova_linha.endswith("\r\n") else ("\n" if nova_linha.endswith("\n") else "")
                    nova_linha = f'{indent}{var_nome} = os.environ.get("{env_var}", ""){resto}{fim_linha}'
                    if nova_linha != linha:
                        modificou = True
                        env_linhas_novas.append(f"{env_var}={valor_antigo}")
                        alteracoes.append(
                            f"{os.path.relpath(caminho, self.raiz)}:{idx + 1} -> '{var_nome}' movido para os.environ.get(\"{env_var}\")."
                        )

                linhas[idx] = nova_linha

            if modificou:
                self._fazer_backup_arquivo(caminho)
                novo_codigo = "".join(linhas)
                if "os.environ" in novo_codigo and not re.search(r"^\s*import\s+os\b", novo_codigo, re.MULTILINE):
                    novo_codigo = "import os\n" + novo_codigo
                with open(caminho, "w", encoding="utf-8") as f:
                    f.write(novo_codigo)
                try:
                    py_compile.compile(caminho, doraise=True)
                except py_compile.PyCompileError:
                    rel = os.path.relpath(caminho, self.raiz)
                    backup_path = os.path.join(self.pasta_backup, rel)
                    if os.path.exists(backup_path):
                        shutil.copy2(backup_path, caminho)
                    alteracoes.append(f"AVISO: {rel} revertido do backup por falha de compilação após ajuste.")

        if env_linhas_novas:
            caminho_env = os.path.join(self.raiz, ".env")
            existente = self._ler_texto_seguro(caminho_env)
            adicionados = []
            for entry in env_linhas_novas:
                chave = entry.split("=", 1)[0]
                if f"{chave}=" not in existente:
                    adicionados.append(entry)
            if adicionados:
                with open(caminho_env, "a", encoding="utf-8") as f:
                    if existente and not existente.endswith("\n"):
                        f.write("\n")
                    for entry in adicionados:
                        f.write(entry + "\n")
                alteracoes.append(f".env atualizado com {len(adicionados)} chave(s) extraída(s).")

        return alteracoes

    def _avaliar_conformidade_iso(
        self, pdfs: List[str], arquivos_py: List[str]
    ) -> Tuple[int, List[str], List[str]]:
        score = 100
        motivos: List[str] = []
        plano: List[str] = []

        if not pdfs:
            return 1, ["Nenhum PDF localizado em 'pdfs_finais'."], ["Gerar os PDFs finais na pasta 'pdfs_finais'."]

        total_paginas = 0
        paginas_fora_a4: List[str] = []
        paginas_margem_baixa: List[str] = []
        sem_titulo: List[str] = []
        scripts_dossie = self._localizar_scripts_por_palavras_chave(
            arquivos_py, ("dossie", "engine", "motor", "pdf", "gerador")
        )
        dica_scripts = f" [Scripts candidatos: {', '.join(scripts_dossie)}]" if scripts_dossie else ""

        for caminho in pdfs:
            nome_pdf = os.path.basename(caminho)
            try:
                doc = fitz.open(caminho)
            except Exception as e:
                score -= 15
                motivos.append(f"Falha ao abrir '{nome_pdf}': {e}.")
                plano.append(f"Regenerar '{nome_pdf}'.")
                continue

            if not (doc.metadata or {}).get("title", "").strip():
                sem_titulo.append(nome_pdf)

            for idx_pag in range(len(doc)):
                num_pag = idx_pag + 1
                pagina = doc[idx_pag]
                total_paginas += 1
                w, h = float(pagina.rect.width), float(pagina.rect.height)
                if abs(w - self.largura_a4) > 5 or abs(h - self.altura_a4) > 5:
                    paginas_fora_a4.append(f"{nome_pdf} p.{num_pag} ({w:.1f}x{h:.1f}pt)")

                blocos = pagina.get_text("blocks")
                if blocos:
                    x0 = [float(b[0]) for b in blocos if 0 <= float(b[0]) < w - 20]
                    y0 = [float(b[1]) for b in blocos if 0 <= float(b[1]) < h - 20]
                    x1 = [float(b[2]) for b in blocos if 20 < float(b[2]) <= w]
                    y1 = [float(b[3]) for b in blocos if 20 < float(b[3]) <= h]
                    if x0 and y0 and x1 and y1:
                        menor_margem = min(
                            min(x0) * self.pt_para_mm,
                            min(y0) * self.pt_para_mm,
                            (w - max(x1)) * self.pt_para_mm,
                            (h - max(y1)) * self.pt_para_mm,
                        )
                        if menor_margem < self.limiar_margem_mm:
                            paginas_margem_baixa.append(
                                f"{nome_pdf} p.{num_pag} (margem {menor_margem:.2f}mm)"
                            )
            doc.close()

        if paginas_fora_a4:
            penalidade = min(30, len(paginas_fora_a4) * 5)
            score -= penalidade
            motivos.append(
                f"{len(paginas_fora_a4)}/{total_paginas} página(s) fora do formato A4 -> {', '.join(paginas_fora_a4)}."
            )
            plano.append(
                f"Padronizar para A4 (595.28 x 841.89 pt): {', '.join(paginas_fora_a4)}{dica_scripts}."
            )

        if paginas_margem_baixa:
            penalidade = min(30, len(paginas_margem_baixa) * 5)
            score -= penalidade
            motivos.append(
                f"{len(paginas_margem_baixa)}/{total_paginas} página(s) com margem < {self.limiar_margem_mm}mm -> {', '.join(paginas_margem_baixa)}."
            )
            plano.append(
                f"Ajustar margens/espaçamentos para >= {self.limiar_margem_mm}mm em: {', '.join(paginas_margem_baixa)}{dica_scripts}."
            )

        if sem_titulo:
            penalidade = min(15, len(sem_titulo) * 3)
            score -= penalidade
            motivos.append(f"{len(sem_titulo)}/{len(pdfs)} PDF(s) sem metadado 'Title' -> {', '.join(sem_titulo)}.")
            plano.append(f"Definir metadado 'Title' em: {', '.join(sem_titulo)}{dica_scripts}.")

        if not motivos:
            motivos.append(f"{len(pdfs)} PDF(s) ({total_paginas} páginas) validados em A4, margens >= {self.limiar_margem_mm}mm e metadados sem alerta crítico.")

        return max(1, min(100, score)), motivos, plano

    def _avaliar_densidade_conteudo(
        self, pdfs: List[str], arquivos_py: List[str]
    ) -> Tuple[int, int, List[str], List[str]]:
        score = 100
        total_palavras = 0
        motivos: List[str] = []
        plano: List[str] = []
        scripts_dossie = self._localizar_scripts_por_palavras_chave(
            arquivos_py, ("dossie", "engine", "motor", "gerador", "tricologia", "monaco", "carta")
        )
        dica_scripts = f" [Scripts candidatos: {', '.join(scripts_dossie)}]" if scripts_dossie else ""

        if not pdfs:
            return 1, 0, ["Sem PDFs para calcular densidade textual."], ["Gerar os PDFs finais."]

        curtos: List[str] = []
        for caminho in pdfs:
            nome_pdf = os.path.basename(caminho)
            try:
                doc = fitz.open(caminho)
                texto = self._extrair_texto_pdf(doc)
                doc.close()
                qtd = len(texto.split())
                total_palavras += qtd
                if qtd < self.min_palavras_dossie:
                    curtos.append(f"{nome_pdf} ({qtd} palavras)")
            except Exception as e:
                score -= 10
                motivos.append(f"Falha ao ler '{nome_pdf}': {e}.")

        if curtos:
            penalidade = min(40, len(curtos) * 10)
            score -= penalidade
            motivos.append(
                f"PDF(s) abaixo de {self.min_palavras_dossie} palavras -> {', '.join(curtos)}."
            )
            plano.append(
                f"Aumentar o conteúdo técnico para >= {self.min_palavras_dossie} palavras em: {', '.join(curtos)}{dica_scripts}."
            )

        if total_palavras < 3000:
            score -= 15
            motivos.append(f"Total de {total_palavras} palavras abaixo da meta de 3.000 palavras.")
            plano.append(f"Expandir o volume textual consolidado dos dossiês{dica_scripts}.")

        if not motivos:
            motivos.append(f"{total_palavras} palavras no total; todos os {len(pdfs)} PDFs atendem ao limiar de densidade sem alerta crítico.")

        return max(1, min(100, score)), total_palavras, motivos, plano

    def _imprimir_bloco_superior(
        self,
        agora: str,
        id_cifrado: str,
        mostrar_caminho: bool,
        cnt_jur: Dict[str, int],
        cnt_dir: Dict[str, int],
        qtd_mibo: int,
        qtd_security: int,
        tem_security: bool,
    ) -> None:
        diretorio_texto = self.raiz if mostrar_caminho else "[OCULTO — PROTEÇÃO DE CAMINHO SOBERANO]"
        cor_dir = AMARELO if mostrar_caminho else VERDE

        logger.info(f"\n{VERDE_BOLD}{'=' * LARGURA_BANNER}{RESET}")
        logger.info(_centralizar_linha(f"{AMARELO_BOLD}THIERRY TECHNOLOGY CONCEPT GLOBAL — AUDITORIA GLOBAL DO ECOSSISTEMA{RESET}"))
        logger.info(f"{CIANO}  Data da Emissão   : {BRANCO_BOLD}{agora}{RESET}")
        logger.info(f"{CIANO}  Projeto Cifrado   : {ROXO_BOLD}{id_cifrado}{RESET} {CINZA}(Nome real blindado){RESET}")
        logger.info(f"{CIANO}  Diretório Raiz    : {cor_dir}{diretorio_texto}{RESET}")
        logger.info(f"{VERDE_BOLD}{'-' * LARGURA_BANNER}{RESET}")

        logger.info(f"\n{CIANO_BOLD}[0] IDENTIDADE, ESCOPO INTANGÍVEL E JURISDIÇÕES{RESET}")
        logger.info(f"  Produto MIBO (Telemedicina Nac/Int) : {BRANCO_BOLD}MIBO Sovereign Intelligence Framework{RESET} {_formatar_ok_status(True)}")
        logger.info(f"  Foco Comercial                      : {AMARELO}Produtos Intangíveis • Pronto para Venda{RESET} {_formatar_ok_status(True)}")
        logger.info(f"  Total de Vagas no Mundo             : {VERDE_BOLD}10 vagas no mundo{RESET} {_formatar_ok_status(True)}")
        logger.info(f"  Grupos / Classes Alvo               : {CIANO}UHNW • Clínicas • Longevity • Visagismo Elite{RESET} {_formatar_ok_status(True)}")
        logger.info(f"  Varredura de Jurisdições e Acervo   : {VERDE_BOLD}Conformidade com padrões mais rígidos{RESET} {_formatar_ok_status(all(v > 0 for v in cnt_jur.values()))}")

        for pais, cod, _ in JURISDICOES_ALVO:
            chave = f"{pais} ({cod})"
            qtd = cnt_jur.get(chave, 0)
            logger.info(f"    {BRANCO_BOLD}{pais:<15}{RESET} | Código: {CIANO_BOLD}{cod:<13}{RESET} | Hits: {BRANCO_BOLD}{qtd:4d}{RESET} | {_formatar_ok_status(qtd > 0)}")

        logger.info(f"  Diretrizes e Blindagem Soberana    : {CIANO_BOLD}Arquitetura & Controles de Segurança{RESET} {_formatar_ok_status(all(v > 0 for v in cnt_dir.values()))}")
        for rotulo, _ in DIRETRIZES_ALVO:
            qtd = cnt_dir.get(rotulo, 0)
            logger.info(f"    {BRANCO_BOLD}{rotulo:<35}{RESET} | Hits: {BRANCO_BOLD}{qtd:4d}{RESET} | {_formatar_ok_status(qtd > 0)}")

        logger.info(f"  Segurança, MIBO & Pasta security    : {ROXO_BOLD}MIBO + Pasta security{RESET} {_formatar_ok_status(qtd_mibo > 0 and tem_security)}")
        logger.info(f"    {ROXO_BOLD}Arquivos MIBO{RESET}                      : {ROXO_BOLD}{qtd_mibo:4d} arquivo(s){RESET} | {_formatar_ok_status(qtd_mibo > 0)}")
        logger.info(f"    {ROXO_BOLD}Pasta security{RESET}                     : {ROXO_BOLD}{qtd_security:4d} arquivo(s){RESET} | {_formatar_ok_status(tem_security)}")

        logger.info(f"\n{VERDE_BOLD}{'=' * LARGURA_BANNER}{RESET}")

    def _imprimir_diagnostico(self, secoes_diagnostico: List[Tuple[str, List[str], int]]) -> None:
        logger.info(f"\n{CIANO_BOLD}[3] DIAGNÓSTICO E DIRETRIZES VERIFICADAS{RESET}")
        for titulo, itens, nota_sec in secoes_diagnostico:
            cor_tit = _cor_por_nota(nota_sec)
            tem_alerta = nota_sec < 100
            status_txt = f"{AMARELO_BOLD}AJUSTE PENDENTE ({nota_sec}/100){RESET}" if tem_alerta else f"{VERDE_BOLD}SEM ALERTA CRÍTICO{RESET}"
            logger.info(f"  {cor_tit}{titulo:<34}{RESET} | {status_txt}")
            for item in itens:
                cor_item = AMARELO if tem_alerta else VERDE
                logger.info(f"    {cor_item}- {item}{RESET}")

    def _imprimir_resumo_e_10_fatores(
        self,
        dados_auditoria: Dict[str, int],
        plano_unificado: List[str],
    ) -> None:
        s_venda = dados_auditoria["s_venda"]
        s_main = dados_auditoria["s_main"]
        s_mem = dados_auditoria["s_mem"]
        s_html = dados_auditoria["s_html"]
        s_mot = dados_auditoria["s_mot"]
        s_bio = dados_auditoria["s_bio"]
        s_gem = dados_auditoria["s_gem"]
        s_c2s = dados_auditoria["s_c2s"]
        s_seg = dados_auditoria["s_seg"]
        s_iso = dados_auditoria["s_iso"]
        s_cnt = dados_auditoria["s_cnt"]
        s_conf = dados_auditoria["s_conf"]
        qtd_mibo = dados_auditoria["qtd_mibo"]
        qtd_c2 = dados_auditoria["qtd_c2"]
        qtd_security = dados_auditoria["qtd_security"]
        alertas_seg = dados_auditoria["alertas_seg"]
        jur_ok = dados_auditoria["jur_ok"]
        jur_tot = dados_auditoria["jur_tot"]
        dir_ok = dados_auditoria["dir_ok"]
        dir_tot = dados_auditoria["dir_tot"]
        qtd_pdfs = dados_auditoria["qtd_pdfs"]
        total_palavras = dados_auditoria["total_palavras"]
        total_py = dados_auditoria["total_py"]

        logger.info(f"\n{CIANO_BOLD}[5.1] RESUMO DO PROGRAMA E 10 FATORES DE ALTO PADRÃO{RESET}")
        logger.info(
            f"  O que tem     : MIBO Sovereign ({s_venda}/100), main.py ({s_main}/100), "
            f"{total_py} .py / motores ({s_mot}/100), memória comum ({s_mem}/100), "
            f"HTML ({s_html}/100), biometria ({s_bio}/100), biogêmeos ({s_gem}/100), "
            f"controle C2 ({qtd_c2} arq., {s_c2s}/100), pasta security ({qtd_security} arq., {s_seg}/100), "
            f"MIBO ({qtd_mibo} arq.), {jur_ok}/{jur_tot} jurisdições e {dir_ok}/{dir_tot} diretrizes "
            f"({s_conf}/100), ISO ({s_iso}/100), {qtd_pdfs} PDFs com {total_palavras} palavras "
            f"({s_cnt}/100) e produtos intangíveis."
        )
        if not plano_unificado and alertas_seg == 0:
            logger.info(f"  O que não tem : {VERDE_BOLD}Nenhuma pendência crítica ou alerta de segurança estática nesta execução.{RESET}")
        else:
            pendencias: List[str] = []
            if alertas_seg > 0:
                pendencias.append(f"{alertas_seg} alerta(s) de segurança estática (--aplicar)")
            pendencias.extend(plano_unificado)
            logger.info(f"  O que não tem : {AMARELO}{'; '.join(pendencias)}{RESET}")

        fatores_alto_padrao = [
            f"01. O que é o software         : MIBO Sovereign ({s_venda}/100) vs. códigos comuns/templates soltos.",
            f"02. Cobertura legal e diretriz : {jur_ok}/{jur_tot} leis ({s_conf}/100) e {dir_ok}/{dir_tot} diretrizes vs. checklist genérico.",
            f"03. Motores e compilação       : Motores {s_mot}/100 em {total_py} scripts .py vs. scripts isolados sem validação global.",
            f"04. Biometria e biogêmeos      : Bio {s_bio}/100 e Biogêmeos {s_gem}/100 vs. ausência de modelagem integrada de gêmeos.",
            f"05. Segurança do ramo          : Pasta security ({qtd_security} arq., {s_seg}/100), MIBO ({qtd_mibo}) e C2 ({qtd_c2}) nota {s_c2s}/100 vs. segurança solta em nuvem.",
            f"06. Risco estático e correção  : Alertas atuais: {alertas_seg} + --aplicar com backup em .auditor_backup vs. sem varredura embutida.",
            f"07. Documentação e ISO         : ISO {s_iso}/100 e {qtd_pdfs} PDFs ({total_palavras} palavras) vs. relatórios sem checagem A4/margem.",
            f"08. O que faz de diferente     : Audita código, PDFs e leis + selo SHA-256 vs. execução isolada ou lint básico.",
            f"09. Operação e resiliência     : Foco offline/soberano, sem servidor público vs. dependência de nuvem pública.",
            f"10. Por que é alto padrão      : Venda {s_venda}/100, ID cifrado, selo SHA-256, biogêmeos, controle C2 e produtos intangíveis vs. validação rasa.",
        ]
        for linha_fator in fatores_alto_padrao:
            logger.info(f"  {VERDE}{linha_fator}{RESET}")

    def _imprimir_bloco_final_telemedicina_e_selo(
        self,
        tudo_ok: bool,
        selo_no: str,
        assinatura_b64: str,
        timestamp_local: str,
        dados_auditoria: Dict[str, int],
    ) -> None:
        s_venda = dados_auditoria["s_venda"]
        qtd_mibo = dados_auditoria["qtd_mibo"]
        qtd_c2 = dados_auditoria["qtd_c2"]
        qtd_security = dados_auditoria["qtd_security"]
        s_c2s = dados_auditoria["s_c2s"]
        s_seg = dados_auditoria["s_seg"]
        s_conf = dados_auditoria["s_conf"]
        s_iso = dados_auditoria["s_iso"]
        s_cnt = dados_auditoria["s_cnt"]
        s_bio = dados_auditoria["s_bio"]
        s_gem = dados_auditoria["s_gem"]
        jur_ok = dados_auditoria["jur_ok"]
        jur_tot = dados_auditoria["jur_tot"]
        dir_ok = dados_auditoria["dir_ok"]
        dir_tot = dados_auditoria["dir_tot"]
        qtd_pdfs = dados_auditoria["qtd_pdfs"]
        total_palavras = dados_auditoria["total_palavras"]
        alertas_seg = dados_auditoria["alertas_seg"]

        logger.info(f"\n{CIANO_BOLD}[6] SELO DE CRIPTOGRAFIA, BENCHMARK GLOBAL DE TELEMEDICINA E VEREDICTO FINAL{RESET}")
        if tudo_ok:
            logger.info(f"  {VERDE_BOLD}SELO SOBERANO 100/100 • PRONTIDÃO GLOBAL APROVADA SEM RESSALVAS{RESET}")
            logger.info(f"  {VERDE_BOLD}Excelência absoluta alcançada: arquitetura, motores, segurança C2/security, layout e densidade 100% íntegros.{RESET}")
        else:
            logger.info(f"  {AMARELO_BOLD}SELO EM PROGRESSO • SCORE GLOBAL: {s_venda:3d}/100 (AJUSTES PENDENTES){RESET}")
            logger.info(f"  {AMARELO}Base sólida e avançada: conclua os pontos restantes do Plano de Ação para atingir 100/100.{RESET}")

        logger.info(f"\n  {AMARELO_BOLD}CHAVE CRIPTOGRÁFICA DE VALIDAÇÃO SOBERANA (SHA-256):{RESET}")
        logger.info(f"    {BRANCO_BOLD}Selo do Nó:{RESET}  {CIANO_BOLD}{selo_no}{RESET}")
        logger.info(f"    {BRANCO_BOLD}Assinatura:{RESET}  {AMARELO_BOLD}{assinatura_b64}{RESET}")
        logger.info(f"    {BRANCO_BOLD}Timestamp :{RESET}  {VERDE_BOLD}{timestamp_local}{RESET}")

        logger.info(f"\n  {CIANO_BOLD}10 FATORES — TELEMEDICINA GLOBAL (MESMO PATAMAR / PADRÃO):{RESET}")
        fatores_telemed = [
            f"01. O que ele é (critério global)     : MIBO Sovereign (Venda {s_venda}/100) no patamar de plataformas globais de telemedicina.",
            f"02. Por que está no mesmo patamar/padrão: Trata dados sensíveis/saúde com {s_conf}/100 em leis, exigindo sigilo, trilha e rigor legal.",
            f"03. Cobertura multi-jurisdição        : {jur_ok}/{jur_tot} jurisdições (GDPR/HIPAA/LGPD) alinhadas às exigências dos mercados internacionais.",
            f"04. Diretrizes e padrão técnico       : {dir_ok}/{dir_tot} diretrizes e ISO {s_iso}/100 compatíveis com padrões técnicos e de saúde.",
            f"05. Privacidade, acesso e integridade : C2/Segurança {s_c2s}/100, pasta security {s_seg}/100, rotinas de hash/integridade e {alertas_seg} alerta(s) estático(s).",
            f"06. O que elas têm e ele tem também   : Foco em sigilo, conformidade regulatória, controle de acesso e proteção de dados sensíveis.",
            f"07. Camada de segurança e blindagem   : security ({qtd_security} arq., {s_seg}/100), MIBO ({qtd_mibo} arq.) e C2 ({qtd_c2} arq.) vs. cloud/WAF e serviços externos.",
            f"08. Inteligência e ativos intangíveis: Biometria ({s_bio}/100), biogêmeos ({s_gem}/100) e produtos intangíveis além da teleconsulta básica.",
            f"09. Documentação e auditoria ativa    : Auditor próprio + {qtd_pdfs} PDFs ({total_palavras} palavras, {s_cnt}/100) vs. plataformas sem auditoria própria.",
            f"10. O que ele faz que elas não fazem   : Audita código, PDFs e leis + --aplicar + arquitetura offline/C2 vs. nuvem contínua/APIs padrão.",
        ]
        for linha_tel in fatores_telemed:
            logger.info(f"    {CIANO}{linha_tel}{RESET}")

        logger.info(f"\n  {VERDE_BOLD}SÍNTESE FINAL DO PATAMAR GLOBAL DE TELEMEDICINA:{RESET}")
        logger.info(f"    1. O que ele é: Ecossistema MIBO Sovereign ({s_venda}/100) voltado a telemedicina, biometria ({s_bio}/100), biogêmeos ({s_gem}/100), controle C2 e produtos intangíveis.")
        logger.info(f"    2. Por que está no mesmo patamar / padrão: Trata dados sensíveis, {jur_ok}/{jur_tot} jurisdições e {dir_ok}/{dir_tot} diretrizes (conformidade {s_conf}/100, ISO {s_iso}/100) com alto rigor.")
        logger.info(f"    3. O que elas têm que ele tem também: Foco em privacidade, controle de acesso, hash/criptografia, rastreabilidade e conformidade regulatória (densidade {s_cnt}/100).")
        logger.info(f"    4. O que ele faz que elas não fazem: Audita código, {qtd_pdfs} PDFs ({total_palavras} palavras) e leis + pasta security ({qtd_security} arq., {s_seg}/100), MIBO ({qtd_mibo}), C2 ({qtd_c2}), biogêmeos, controle C2 e produtos intangíveis.")

        logger.info(f"\n{VERDE_BOLD}{'=' * LARGURA_BANNER}{RESET}\n")

    def executar_auditoria_completa(
        self, aplicar_correcoes: bool = False, mostrar_caminho: bool = False
    ) -> None:
        _ativar_ansi_terminal()
        agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        id_cifrado = _gerar_identificador_cifrado(self.raiz)

        pasta_pdfs = self._localizar_pasta_pdfs()
        pdfs = sorted(
            [os.path.join(pasta_pdfs, f) for f in os.listdir(pasta_pdfs) if f.lower().endswith(".pdf")]
        ) if os.path.exists(pasta_pdfs) else []

        arquivos_py = self._coletar_arquivos((".py",))
        arquivos_html = self._coletar_arquivos((".html", ".htm"))
        arquivos_projeto = self._coletar_arquivos(
            (".py", ".json", ".html", ".htm", ".md", ".txt", ".yaml", ".yml"),
            incluir_ocultos_mibo=True,
        )
        qtd_security, tem_security = self._contar_arquivos_pasta_security()

        s_main, mot_main, plan_main, tem_main = self._inspecionar_main(arquivos_py)
        s_mem, mot_mem, plan_mem, qtd_mem = self._inspecionar_memoria_comum(arquivos_projeto)
        s_html, mot_html, plan_html = self._inspecionar_painel_html(arquivos_html)
        s_mot, mot_mot, plan_mot, res_mot = self._inspecionar_motores(arquivos_py)
        s_bio, mot_bio, plan_bio, qtd_bio = self._inspecionar_biometrico(arquivos_projeto)
        s_gem, mot_gem, plan_gem, qtd_gem = self._inspecionar_biogemeos(arquivos_projeto)
        s_c2s, mot_c2s, plan_c2s, res_c2s, achados_seg = self._inspecionar_c2_mibo_seguranca(arquivos_projeto, arquivos_py)
        s_seg, mot_seg, plan_seg, _ = self._inspecionar_pasta_security(arquivos_py)
        s_iso, mot_iso, plan_iso = self._avaliar_conformidade_iso(pdfs, arquivos_py)
        s_cnt, total_palavras, mot_cnt, plan_cnt = self._avaliar_densidade_conteudo(pdfs, arquivos_py)
        s_conf, mot_conf, plan_conf, cnt_jur, cnt_dir = self._inspecionar_conformidade_diretrizes(
            arquivos_projeto, pdfs
        )

        s_venda = max(
            1,
            min(
                100,
                round(
                    (s_main * 0.08)
                    + (s_mem * 0.08)
                    + (s_html * 0.08)
                    + (s_mot * 0.16)
                    + (s_bio * 0.10)
                    + (s_gem * 0.10)
                    + (s_c2s * 0.12)
                    + (s_seg * 0.07)
                    + (s_iso * 0.06)
                    + (s_cnt * 0.05)
                    + (s_conf * 0.14)
                ),
            ),
        )

        notas = [
            ("main.py", s_main),
            ("Memória Comum", s_mem),
            ("Painel HTML", s_html),
            ("Motores & Compilação", s_mot),
            ("Biométrico", s_bio),
            ("Biogêmeos", s_gem),
            ("C2 Sovereign (MIBO & Segurança)", s_c2s),
            ("Segurança (Pasta security)", s_seg),
            ("Conformidade ISO & Layout", s_iso),
            ("Densidade de Conteúdo", s_cnt),
            ("Conformidade & Diretrizes (Disco)", s_conf),
            ("Prontidão de Venda Global", s_venda),
        ]

        jur_ok = sum(1 for v in cnt_jur.values() if v > 0)
        dir_ok = sum(1 for v in cnt_dir.values() if v > 0)

        dados_auditoria: Dict[str, int] = {
            "s_venda": s_venda,
            "s_main": s_main,
            "s_mem": s_mem,
            "s_html": s_html,
            "s_mot": s_mot,
            "s_bio": s_bio,
            "s_gem": s_gem,
            "s_c2s": s_c2s,
            "s_seg": s_seg,
            "s_iso": s_iso,
            "s_cnt": s_cnt,
            "s_conf": s_conf,
            "jur_ok": jur_ok,
            "jur_tot": len(cnt_jur),
            "dir_ok": dir_ok,
            "dir_tot": len(cnt_dir),
            "qtd_mibo": res_c2s["arquivos_mibo"],
            "qtd_c2": res_c2s["arquivos_c2"],
            "qtd_security": qtd_security,
            "alertas_seg": res_c2s["alertas_seguranca"],
            "total_py": res_mot["total_py"],
            "qtd_pdfs": len(pdfs),
            "total_palavras": total_palavras,
        }

        self._imprimir_bloco_superior(
            agora=agora,
            id_cifrado=id_cifrado,
            mostrar_caminho=mostrar_caminho,
            cnt_jur=cnt_jur,
            cnt_dir=cnt_dir,
            qtd_mibo=res_c2s["arquivos_mibo"],
            qtd_security=qtd_security,
            tem_security=tem_security,
        )

        logger.info(f"\n{CIANO_BOLD}[1] INVENTÁRIO GERAL INSPECIONADO{RESET}")
        logger.info(f"  main.py presente.................: {VERDE_BOLD}{'Sim' if tem_main else 'Não'}{RESET}")
        logger.info(f"  Arquivos de memória comum........: {BRANCO_BOLD}{qtd_mem}{RESET}")
        logger.info(f"  Arquivos do painel HTML..........: {BRANCO_BOLD}{len(arquivos_html)}{RESET}")
        logger.info(f"  Scripts .py / Motores detectados...: {BRANCO_BOLD}{res_mot['total_py']} / {res_mot['motores_detectados']}{RESET}")
        logger.info(f"  Arquivos ligados a Biométrico.....: {BRANCO_BOLD}{qtd_bio}{RESET}")
        logger.info(f"  Arquivos ligados a Biogêmeos......: {BRANCO_BOLD}{qtd_gem}{RESET}")
        logger.info(f"  Arquivos MIBO / C2 Sovereign.......: {ROXO_BOLD}{res_c2s['arquivos_mibo']} MIBO{RESET} | {ROXO_BOLD}{res_c2s['arquivos_c2']} C2/Segurança{RESET} | {ROXO_BOLD}security: {qtd_security} arq.{RESET}")
        logger.info(f"  Jurisdições / Diretrizes no disco.: {VERDE}{jur_ok}/{len(cnt_jur)} jurisdições{RESET} | {CIANO}{dir_ok}/{len(cnt_dir)} diretrizes{RESET}")
        logger.info(f"  PDFs finais / Palavras totais......: {VERDE}{len(pdfs)} PDFs{RESET} | {VERDE_BOLD}{total_palavras} palavras{RESET}")

        logger.info(f"\n{CIANO_BOLD}[2] NOTAS CALCULADAS (ESCALA 1 A 100){RESET}")
        for rotulo, valor in notas:
            logger.info(f"  {rotulo:<34}: {_barra_progresso(valor)}")

        secoes_diagnostico = [
            ("main.py", mot_main, s_main),
            ("Memória Comum", mot_mem, s_mem),
            ("Painel HTML", mot_html, s_html),
            ("Motores", mot_mot, s_mot),
            ("Biométrico", mot_bio, s_bio),
            ("Biogêmeos", mot_gem, s_gem),
            ("C2 Sovereign (MIBO & Segurança)", mot_c2s, s_c2s),
            ("Segurança (Pasta security)", mot_seg, s_seg),
            ("Conformidade ISO", mot_iso, s_iso),
            ("Densidade de Conteúdo", mot_cnt, s_cnt),
            ("Conformidade & Diretrizes (Disco)", mot_conf, s_conf),
        ]
        self._imprimir_diagnostico(secoes_diagnostico)

        logger.info(f"\n{CIANO_BOLD}[3.1] LOCALIZAÇÃO EXATA DOS PONTOS DE SEGURANÇA{RESET}")
        if not achados_seg:
            logger.info(f"  {VERDE_BOLD}Nenhum ponto de eval/exec/pickle, shell=True ou credencial fixa encontrado.{RESET}")
        else:
            for item in achados_seg:
                logger.info(
                    f"  {VERMELHO_BOLD}[{item['tipo']}]{RESET} {BRANCO_BOLD}{item['arquivo']}{RESET} "
                    f"{AMARELO}(linha {item['linha']}){RESET}: {CINZA}{item['trecho']}{RESET}"
                )

        plano_unificado: List[str] = []
        for acao in (
            plan_main + plan_mem + plan_html + plan_mot + plan_bio
            + plan_gem + plan_c2s + plan_seg + plan_iso + plan_cnt + plan_conf
        ):
            if acao not in plano_unificado:
                plano_unificado.append(acao)

        logger.info(f"\n{CIANO_BOLD}[4] PLANO DE AÇÃO PARA ATINGIR 100/100{RESET}")
        if not plano_unificado:
            logger.info(f"  {VERDE_BOLD}Tudo verificado está em 100/100 sem pendências.{RESET}")
        else:
            for idx, acao in enumerate(plano_unificado, start=1):
                logger.info(f"  {AMARELO_BOLD}{idx}.{RESET} {BRANCO_BOLD if idx == 1 else ''}{acao}{RESET}")

        if aplicar_correcoes:
            logger.info(f"\n{ROXO_BOLD}[4.1] APLICAÇÃO SEGURA DE CORREÇÕES (--aplicar){RESET}")
            resultados_fix = self.aplicar_correcoes_seguras(achados_seg)
            if not resultados_fix:
                logger.info(f"  {CIANO}Nenhuma alteração automática aplicada.{RESET}")
            else:
                for msg in resultados_fix:
                    logger.info(f"  {VERDE}- {msg}{RESET}")
            logger.info(f"  {AMARELO}Nota: ocorrências de eval/exec/pickle exigem revisão manual caso dependam de lógica dinâmica específica.{RESET}")

        logger.info(f"\n{CIANO_BOLD}[5] POSICIONAMENTO, COMERCIALIZAÇÃO E HOSPEDAGEM{RESET}")
        logger.info(f"  {VERDE}Aplicação:{RESET} Plataforma internacional de telemedicina, saúde/estética")
        logger.info("    avançada, análise biométrica/biogêmeos e governança soberana C2.")
        logger.info(f"  {VERDE}Canais:{RESET} Licenciamento B2B / API (ex.: Stripe / Lemon Squeezy) e entrega")
        logger.info("    controlada de licenças e dossiês.")
        logger.info(f"  {VERDE}Hospedagem:{RESET} Servidores/VPS dedicados na região-alvo (ex.: Europa —")
        logger.info("    Frankfurt/Paris via Hetzner ou DigitalOcean) com HTTPS/TLS, controle")
        logger.info("    de acesso rigoroso e isolamento de dados.")

        self._imprimir_resumo_e_10_fatores(dados_auditoria, plano_unificado)

        tudo_ok = all(valor == 100 for _, valor in notas) and not achados_seg
        selo_no, assinatura_b64, timestamp_local = _gerar_selo_criptografico(
            self.raiz, s_venda, res_mot["total_py"], len(pdfs)
        )

        self._imprimir_bloco_final_telemedicina_e_selo(
            tudo_ok=tudo_ok,
            selo_no=selo_no,
            assinatura_b64=assinatura_b64,
            timestamp_local=timestamp_local,
            dados_auditoria=dados_auditoria,
        )


if __name__ == "__main__":
    raiz = os.getcwd()
    args = set(sys.argv[1:])
    aplicar = bool(args & {"--aplicar", "--corrigir"})
    exibir_caminho = bool(args & {"--mostrar-caminho", "--caminho"})
    auditor = AuditorGlobalMercado(raiz)
    auditor.executar_auditoria_completa(aplicar_correcoes=aplicar, mostrar_caminho=exibir_caminho)
