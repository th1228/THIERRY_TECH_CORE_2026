# -*- coding: utf-8 -*-
# =====================================================================
# THIERRY TECHNOLOGY CONCEPT GLOBAL - AUDITORIA JURÍDICA & CONTRATUAL
# Varre o projeto, lê o contrato atual, dá nota (1-100), explica o
# porquê, aponta lacunas e gera o alinhamento no final do relatório.
# Exibe direto no terminal E salva o arquivo .txt completo em disco.
# =====================================================================

import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------
# COLE AQUI O TEXTO DO CONTRATO INTERNACIONAL QUE VOCÊ JÁ TEM
# (Se deixar vazio, o script avisa e avalia com base no texto atual)
# ---------------------------------------------------------------------
CONTRATO_INTERNACIONAL_ATUAL = """
""".strip()

# Opcional: se você preferir colocar o contrato em um arquivo na raiz do projeto,
# informe o nome aqui (ex.: "contrato_minuta.txt"). Se existir, ele lê o arquivo.
ARQUIVO_CONTRATO_OPCIONAL = ""

# Cores ANSI para destaque no terminal
VERDE = "\033[92m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
CIANO = "\033[96m"
BRANCO = "\033[97m"
CINZA = "\033[90m"
NEGRITO = "\033[1m"
RESET = "\033[0m"

# Mapeamento de países, enclaves e jurisdições a serem buscados no código
PAISES_E_ENCLAVES = {
    "Brasil": [r"\bbrasil\b", r"\bbrazil\b", r"\blgpd\b", r"\binpi\b", r"\bc[oó]digo\s+civil\b"],
    "Mônaco": [r"\bm[oô]naco\b", r"\bmonaco\b"],
    "Suíça (Genebra / Zurique)": [
        r"\bsu[ií][cç]a\b", r"\bswitzerland\b", r"\bgenebra\b", r"\bgeneva\b", r"\bzurique\b", r"\bzurich\b"
    ],
    "União Europeia / Europa": [
        r"\bun[ií][aã]o\s+europeia\b", r"\beuropa\b", r"\beurope\b", r"\bgdpr\b", r"\beu\b"
    ],
    "Reino Unido (Londres)": [
        r"\breino\s+unido\b", r"\bunited\s+kingdom\b", r"\buk\b", r"\blondres\b", r"\blondon\b"
    ],
    "Emirados Árabes Unidos (Dubai)": [r"\bemirados\b", r"\buae\b", r"\bdubai\b"],
    "Singapura": [r"\bsingapura\b", r"\bsingapore\b"],
    "Estados Unidos": [r"\bestados\s+unidos\b", r"\bunited\s+states\b", r"\beua\b", r"\busa\b", r"\bhipaa\b"],
    "Outros / Genérico Internacional": [
        r"\binternacional\b", r"\bglobal\b", r"\benclave\b", r"\bjurisdi[cç][aã]o\b",
        r"\bjurisdiction\b", r"\bgoverning\s+law\b", r"\barbitration\b", r"\bforo\b"
    ],
}

PALAVRAS_CHAVE_GERAIS = [
    r"\bjurisdi[cç][aã]o\b", r"\bjurisdiction\b", r"\bgoverning\s+law\b", r"\barbitration\b",
    r"\bliability\b", r"\bindemnification\b", r"\bdata\s+retention\b", r"\bencryption\b",
    r"\bconsent\b", r"\bforo\b", r"\bgdpr\b", r"\bhipaa\b", r"\blgpd\b", r"\bias\s*38\b",
    r"\biso\b", r"\benclave\b", r"\binpi\b", r"\bpropriedade\s+intelectual\b",
    r"\bconfidencialidade\b", r"\bsigilo\b", r"\boffline\b", r"\bzero[-\s]?trust\b",
    r"\blicen[cç]a\b", r"\bstripe\b", r"\b10\s+licen[cç]as\b", r"\b10\s+vagas\b",
    r"\b21\s+dias\b", r"\bbiometr\w*\b", r"\bbiometric\w*\b", r"\bhealth\b",
    r"\btelemedicin\w*\b", r"\btricolog\w*\b", r"\bcl[ií]nic\w*\b",
]

PASTAS_IGNORADAS = {".venv", "__pycache__", ".git", "node_modules", "testes_temp", "sandbox_temp"}
EXTENSOES_TEXTO = {
    ".py", ".html", ".htm", ".js", ".ts", ".css", ".json",
    ".md", ".txt", ".yaml", ".yml", ".csv", ".log"
}


def arquivo_seguro_para_varrer(caminho: Path) -> bool:
    nome = caminho.name.lower()
    if nome == ".env" or (nome.startswith(".env.") and nome != ".env.example"):
        return False
    if any(parte in PASTAS_IGNORADAS for parte in caminho.parts):
        return False
    if not caminho.is_file():
        return False
    return nome == ".env.example" or caminho.suffix.lower() in EXTENSOES_TEXTO


def sha256_arquivo(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def obter_texto_contrato(raiz: Path) -> str:
    if ARQUIVO_CONTRATO_OPCIONAL.strip():
        arq = raiz / ARQUIVO_CONTRATO_OPCIONAL.strip()
        if arq.exists() and arq.is_file():
            return arq.read_text(encoding="utf-8", errors="replace").strip()
    return CONTRATO_INTERNACIONAL_ATUAL.strip()


def avaliar_contrato_e_alinhar(texto_contrato: str, paises_encontrados: dict, achados_gerais: list) -> dict:
    """
    Avalia o contrato de 0 a 100 com base nos critérios exigidos pelo escopo do código
    e monta a justificativa da nota, os pontos faltantes e as cláusulas/ajustes alinhados.
    """
    if not texto_contrato:
        return {
            "nota": 0,
            "classificacao": "SEM TEXTO DE CONTRATO INSERIDO",
            "motivos_nota": [
                "Nenhum texto de contrato foi colado em CONTRATO_INTERNACIONAL_ATUAL nem carregado via ARQUIVO_CONTRATO_OPCIONAL (0/100)."
            ],
            "faltas_e_alinhamentos": [
                "Inserir a minuta completa do contrato internacional no script para que cada cláusula seja auditada contra o código."
            ],
            "bloco_alinhamento": (
                "AÇÃO NECESSÁRIA ANTES DE ENVIAR AO ADVOGADO:\n"
                "Cole o texto do seu contrato internacional dentro de CONTRATO_INTERNACIONAL_ATUAL e rode novamente.\n"
                "Assim que você colar, o script calculará a nota real (0 a 100), apontará o que falta e\n"
                "montará a versão alinhada com os países, conformidades, arquitetura offline e limites de licença."
            ),
        }

    c = texto_contrato.lower()
    nota = 0
    motivos = []
    faltas = []
    sugestoes_clausulas = []

    # 1. Jurisdição, lei aplicável, foro/arbitragem e países (20 pts)
    tem_jurisdicao = bool(re.search(r"\b(jurisdi[cç][aã]o|jurisdiction|foro|lei\s+aplic[aá]vel|governing\s+law|arbitragem|arbitration)\b", c))
    paises_citados_no_contrato = [
        pais for pais, padroes in PAISES_E_ENCLAVES.items()
        if pais != "Outros / Genérico Internacional" and any(re.search(p, c, re.IGNORECASE) for p in padroes)
    ]
    if tem_jurisdicao and paises_citados_no_contrato:
        nota += 20
        motivos.append(f"+20 pts: Define lei/foro/jurisdição e menciona países/enclaves ({', '.join(paises_citados_no_contrato)}).")
    elif tem_jurisdicao:
        nota += 12
        motivos.append("+12 pts: Menciona lei/foro/jurisdição, mas não detalha explicitamente os países/enclaves de atuação.")
        faltas.append("Especificar no contrato os países/enclaves de operação e a regra de lei aplicável e foro/arbitragem por território.")
        sugestoes_clausulas.append(
            "CLÁUSULA — TERRITÓRIOS, LEI APLICÁVEL E RESOLUÇÃO DE CONTROVÉRSIAS:\n"
            "A presente licença abrange as operações e enclaves acordados entre as partes, regendo-se pelas leis "
            "designadas para o respectivo território/enclave, com eleição de foro ou arbitragem expressa para dirimir disputas."
        )
    else:
        faltas.append("Ausência de cláusula clara de jurisdição, lei aplicável, foro/arbitragem e países/enclaves cobertos.")
        motivos.append("0/20 pts: Falta definição clara de lei aplicável, foro/arbitragem e países de atuação.")
        sugestoes_clausulas.append(
            "CLÁUSULA — TERRITÓRIOS, LEI APLICÁVEL E RESOLUÇÃO DE CONTROVÉRSIAS:\n"
            "Este contrato aplica-se aos países e enclaves definidos no Anexo Comercial, sujeitando-se à legislação "
            "aplicável e ao foro/câmara arbitral expressamente pactuados pelas partes."
        )

    # 2. Dados sensíveis, saúde, biometria e privacidade/DPA (20 pts)
    tem_dados_sensiveis_codigo = any(
        re.search(r"\b(biometr\w*|biometric\w*|health|telemedicin\w*|tricolog\w*|cl[ií]nic\w*)\b", linha, re.IGNORECASE)
        for item in achados_gerais for _, linha in item["ocorrencias"]
    )
    tem_privacidade_contrato = bool(re.search(r"\b(lgpd|gdpr|hipaa|dados\s+pessoais|dados\s+sens[ií]veis|biometr\w*|sa[uú]de|privacidade|dpa|consentimento|consent)\b", c))
    if tem_privacidade_contrato:
        nota += 20
        motivos.append("+20 pts: Contempla privacidade/proteção de dados e termos sensíveis/regulatórios.")
    else:
        if tem_dados_sensiveis_codigo:
            faltas.append("O código apresenta referências a biometria/saúde/clínica, mas o contrato não trata adequadamente de dados sensíveis, consentimento, retenção e DPA (LGPD/GDPR/HIPAA).")
            motivos.append("0/20 pts: Código trata/menciona biometria/saúde/clínica, mas o contrato omite cláusulas de dados sensíveis e conformidade (LGPD/GDPR/HIPAA).")
        else:
            faltas.append("Falta cláusula de proteção de dados, consentimento, retenção e conformidade regulatória (LGPD/GDPR/HIPAA).")
            motivos.append("0/20 pts: Ausência de cláusula de privacidade e conformidade de dados.")
        sugestoes_clausulas.append(
            "CLÁUSULA — DADOS SENSÍVEIS, BIOMETRIA, SAÚDE E CONFORMIDADE REGULATÓRIA:\n"
            "O tratamento de quaisquer informações pessoais, clínicas ou biométricas observará as leis aplicáveis "
            "(incluindo LGPD, GDPR e/ou HIPAA, conforme o território), com base legal/consentimento válido, "
            "política de retenção/descarte e responsabilidades claras entre controlador e operador/licenciado."
        )

    # 3. Arquitetura 100% offline, zero-trust e segurança/criptografia (20 pts)
    tem_seguranca_contrato = bool(re.search(r"\b(offline|local|zero[-\s]?trust|criptograf\w*|encryption|seguran[cç]a|sha[-\s]?256)\b", c))
    if tem_seguranca_contrato:
        nota += 20
        motivos.append("+20 pts: Descreve segurança, criptografia ou execução local/offline/zero-trust.")
    else:
        nota += 6
        motivos.append("+6 pts: Abordagem de segurança/arquitetura insuficiente face ao caráter offline/criptográfico do sistema.")
        faltas.append("Alinhar o contrato à arquitetura real do programa (execução local/offline, sem envio indevido a nuvem externa, integridade/criptografia).")
        sugestoes_clausulas.append(
            "CLÁUSULA — ARQUITETURA DE EXECUÇÃO, SIGILO E SEGURANÇA DA INFORMAÇÃO:\n"
            "O software opera em ambiente local/controlado conforme sua arquitetura técnica, com medidas de "
            "segurança da informação, integridade e confidencialidade compatíveis com o nível de sigilo exigido."
        )

    # 4. Propriedade intelectual, registros (INPI/IAS 38) e anti-engenharia reversa (20 pts)
    tem_pi_contrato = bool(re.search(r"\b(propriedade\s+intelectual|intellectual\s+property|c[oó]digo[-\s]?fonte|engenharia\s+reversa|reverse\s+engineering|inpi|confidencialidade|nda)\b", c))
    if tem_pi_contrato:
        nota += 20
        motivos.append("+20 pts: Protege propriedade intelectual, confidencialidade ou vedação de engenharia reversa.")
    else:
        nota += 5
        motivos.append("+5 pts: Proteção de propriedade intelectual e proibição de engenharia reversa incompletas.")
        faltas.append("Reforçar titularidade exclusiva da propriedade intelectual, sigilo do código-fonte e proibição expressa de engenharia reversa, cópia ou sublicenciamento não autorizado.")
        sugestoes_clausulas.append(
            "CLÁUSULA — PROPRIEDADE INTELECTUAL E VEDAÇÃO DE ENGENHARIA REVERSA:\n"
            "Todos os direitos de propriedade intelectual sobre o software, algoritmos, interfaces e documentação "
            "pertencem exclusivamente à licenciadora. É expressamente vedada a engenharia reversa, decompilação, "
            "cópia, modificação não autorizada ou sublicenciamento fora dos termos deste instrumento."
        )

    # 5. Licenciamento, cotas/vagas, prazos, pagamentos e responsabilidade (20 pts)
    tem_licenca_e_limites = bool(re.search(r"\b(licen[cç]a|license|vagas|seats|prazo|vig[eê]ncia|pagamento|stripe|responsabilidade|liability|indeniza[cç][aã]o|indemnification)\b", c))
    if tem_licenca_e_limites:
        nota += 15
        motivos.append("+15 pts: Trata de licenciamento, pagamentos ou limites/responsabilidades.")
        if not re.search(r"\b(10\s+licen[cç]as|10\s+vagas|21\s+dias)\b", c):
            faltas.append("Conferir se os limites comerciais específicos do projeto (ex.: cota de 10 licenças/vagas e prazos/ciclos como 21 dias ou meios de pagamento) estão expressos sem ambiguidade.")
            sugestoes_clausulas.append(
                "CLÁUSULA — ESCOPO DE LICENÇAS, COTAS, PRAZOS E CONDIÇÕES COMERCIAIS:\n"
                "A licença outorgada respeita os limites quantitativos, prazos de ativação/vigência e condições "
                "financeiras estabelecidos no Quadro Comercial, não gerando cessão definitiva de direitos autorais."
            )
        else:
            nota += 5
            motivos.append("+5 pts: Inclui parâmetros numéricos específicos de cotas/prazos.")
    else:
        faltas.append("Faltam regras claras de licenciamento, limites de vagas/licenças, prazos, pagamento e limitação de responsabilidade/indenização.")
        motivos.append("0/20 pts: Ausência de cláusulas essenciais de licenciamento, prazos/pagamentos e responsabilidade.")
        sugestoes_clausulas.append(
            "CLÁUSULA — LICENCIAMENTO, LIMITES DE USO E RESPONSABILIDADE:\n"
            "O uso do software limita-se às licenças/vagas contratadas e aos prazos pactuados, observadas as "
            "regras de pagamento e os limites de responsabilidade e indenização cabíveis conforme a lei aplicável."
        )

    nota = max(0, min(100, nota))
    if nota >= 85:
        classificacao = "ALTO ALINHAMENTO (PRONTO PARA REFINAMENTO FINAL COM O ADVOGADO)"
    elif nota >= 60:
        classificacao = "ALINHAMENTO INTERMEDIÁRIO (REQUER AJUSTES PONTUAIS ANTES DO ADVOGADO)"
    elif nota >= 30:
        classificacao = "ALINHAMENTO BAIXO (HÁ LACUNAS RELEVANTES DE ESCOPO/CONFORMIDADE)"
    else:
        classificacao = "CRÍTICO / INCOMPLETO (NECESSITA ESTRUTURAÇÃO E ALINHAMENTO)"

    if not faltas:
        faltas.append("Nenhuma lacuna crítica óbvia detectada pelos critérios automáticos; revise apenas detalhes comerciais específicos com seu advogado.")

    if not sugestoes_clausulas:
        sugestoes_clausulas.append(
            "REVISÃO FINAL SUGERIDA:\n"
            "Mantenha as cláusulas atuais e valide com seu advogado a adequação de foro, DPA e limites "
            "de responsabilidade para cada país contemplado na operação."
        )

    return {
        "nota": nota,
        "classificacao": classificacao,
        "motivos_nota": motivos,
        "faltas_e_alinhamentos": faltas,
        "bloco_alinhamento": "\n\n".join(sugestoes_clausulas),
    }


def gerar_relatorio_juridico(imprimir_no_terminal: bool = True) -> Path:
    raiz = Path(__file__).resolve().parent
    saida_dir = raiz / "core" / "storage" / "juridico"
    saida_dir.mkdir(parents=True, exist_ok=True)

    padrao_geral = re.compile("|".join(PALAVRAS_CHAVE_GERAIS), re.IGNORECASE)
    padroes_paises = {
        pais: re.compile("|".join(regex_list), re.IGNORECASE)
        for pais, regex_list in PAISES_E_ENCLAVES.items()
    }

    achados_gerais = []
    mapa_paises = {pais: [] for pais in PAISES_E_ENCLAVES}

    arquivos_varridos = 0
    total_linhas = 0

    for caminho in sorted(raiz.rglob("*")):
        if not arquivo_seguro_para_varrer(caminho):
            continue

        arquivos_varridos += 1
        try:
            linhas = caminho.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue

        total_linhas += len(linhas)
        rel_path = str(caminho.relative_to(raiz))
        matches_gerais = []

        for idx, linha in enumerate(linhas, start=1):
            trecho = linha.strip()
            if len(trecho) > 220:
                trecho = trecho[:217] + "..."

            if padrao_geral.search(linha):
                matches_gerais.append((idx, trecho))

            for pais, padrao_pais in padroes_paises.items():
                if padrao_pais.search(linha):
                    mapa_paises[pais].append((rel_path, idx, trecho))

        if matches_gerais:
            achados_gerais.append({
                "rel_path": rel_path,
                "sha256": sha256_arquivo(caminho),
                "ocorrencias": matches_gerais,
            })

    agora_utc = datetime.now(timezone.utc)
    timestamp_legivel = agora_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    timestamp_arquivo = agora_utc.strftime("%Y%m%d_%H%M%SZ")

    nome_relatorio = f"evidencias_contrato_juridico_{timestamp_arquivo}.txt"
    destino = saida_dir / nome_relatorio

    paises_encontrados = {p: occ for p, occ in mapa_paises.items() if occ}
    texto_contrato = obter_texto_contrato(raiz)
    avaliacao = avaliar_contrato_e_alinhar(texto_contrato, paises_encontrados, achados_gerais)

    linhas_relatorio = [
        "=" * 92,
        "RELATÓRIO TÉCNICO DE EVIDÊNCIAS, PAÍSES, CONFORMIDADES E ALINHAMENTO CONTRATUAL",
        "THIERRY TECHNOLOGY CONCEPT GLOBAL",
        f"Gerado em (UTC): {timestamp_legivel}",
        f"Arquivos de texto/código varridos: {arquivos_varridos} | Total de linhas: {total_linhas:,}",
        f"Países/enclaves com ocorrências no código: {len(paises_encontrados)} | Arquivos com termos jurídicos: {len(achados_gerais)}",
        f"Nota do Contrato Internacional Atual: {avaliacao['nota']}/100 ({avaliacao['classificacao']})",
        "Política de privacidade da auditoria: arquivos .env reais ignorados; sem truncamento de ocorrências.",
        "=" * 92,
        "",
        "NOTA PARA O ASSESSOR JURÍDICO:",
        "Este relatório reúne ocorrências literais encontradas no código e nos arquivos do projeto",
        "(com hash SHA-256 de integridade), avalia a minuta contratual informada e apresenta",
        "sugestões de alinhamento para acelerar a revisão jurídica. A validação legal definitiva cabe ao advogado.",
        "",
        "=" * 92,
        "1. PAÍSES, ENCLAVES E REFERÊNCIAS GEOGRÁFICAS/NORMATIVAS ENCONTRADAS NO CÓDIGO",
        "=" * 92,
    ]

    if not paises_encontrados:
        linhas_relatorio.append("Nenhuma referência explícita a países ou enclaves foi encontrada nos arquivos varridos.")
        linhas_relatorio.append("")
    else:
        for pais, ocorrencias in paises_encontrados.items():
            linhas_relatorio.append("-" * 92)
            linhas_relatorio.append(f"PAÍS / ENCLAVE : {pais}  ({len(ocorrencias)} ocorrência(s) completa(s))")
            for arq, num_linha, trecho in ocorrencias:
                linhas_relatorio.append(f"  [{arq} : L{num_linha}] {trecho}")
            linhas_relatorio.append("")

    linhas_relatorio.extend([
        "=" * 92,
        "2. OCORRÊNCIAS COMPLETAS POR ARQUIVO (NORMAS, LICENCIAMENTO, DADOS SENSÍVEIS E ARQUITETURA)",
        "=" * 92,
        "",
    ])

    for item in achados_gerais:
        linhas_relatorio.append("-" * 92)
        linhas_relatorio.append(f"ARQUIVO : {item['rel_path']}")
        linhas_relatorio.append(f"SHA-256 : {item['sha256']}")
        linhas_relatorio.append(f"OCORRÊNCIAS ({len(item['ocorrencias'])}):")
        for num_linha, trecho in item["ocorrencias"]:
            linhas_relatorio.append(f"  [L{num_linha}] {trecho}")
        linhas_relatorio.append("")

    # -----------------------------------------------------------------
    # BLOCO FINAL: CONTRATO ATUAL, NOTA (1-100), PORQUÊ E ALINHAMENTO
    # -----------------------------------------------------------------
    linhas_relatorio.extend([
        "=" * 92,
        "3. CONTRATO INTERNACIONAL ATUAL, NOTA (1 A 100), JUSTIFICATIVA E ALINHAMENTO",
        "=" * 92,
        "",
        "--- A) TEXTO DO CONTRATO INTERNACIONAL ATUAL ---",
        texto_contrato if texto_contrato else "[NENHUM TEXTO DE CONTRATO INSERIDO EM CONTRATO_INTERNACIONAL_ATUAL]",
        "",
        "--- B) NOTA DO CONTRATO E POR QUE ELE RECEBEU ESSA NOTA ---",
        f"NOTA GERAL: {avaliacao['nota']} / 100",
        f"STATUS    : {avaliacao['classificacao']}",
        "JUSTIFICATIVA DA PONTUAÇÃO:",
    ])
    for motivo in avaliacao["motivos_nota"]:
        linhas_relatorio.append(f"  - {motivo}")

    linhas_relatorio.extend([
        "",
        "--- C) O QUE FALTA OU PRECISA SER ALINHADO ---",
    ])
    for falta in avaliacao["faltas_e_alinhamentos"]:
        linhas_relatorio.append(f"  - {falta}")

    linhas_relatorio.extend([
        "",
        "--- D) ALINHAMENTO PROPOSTO PARA PREPARAR ENVIO AO ADVOGADO ---",
        avaliacao["bloco_alinhamento"],
        "",
        "=" * 92,
    ])

    conteudo_final = "\n".join(linhas_relatorio)
    destino.write_text(conteudo_final, encoding="utf-8")

    if imprimir_no_terminal:
        print(f"\n{VERDE}{NEGRITO}{'=' * 92}{RESET}")
        print(f"{AMARELO}{NEGRITO}  AUDITORIA JURÍDICA & CONTRATUAL — SAÍDA DIRETA NO TERMINAL + ARQUIVO SALVO{RESET}")
        print(f"{CIANO}  Gerado em (UTC): {timestamp_legivel}{RESET}")
        print(
            f"{BRANCO}  Arquivos: {arquivos_varridos} | Linhas: {total_linhas:,} | "
            f"Países/Enclaves: {len(paises_encontrados)} | Nota do Contrato: {AMARELO}{NEGRITO}{avaliacao['nota']}/100{RESET}"
        )
        print(f"{VERDE}{NEGRITO}{'=' * 92}{RESET}\n")

        print(f"{AMARELO}{NEGRITO}[RESUMO RÁPIDO DE PAÍSES / ENCLAVES NO TERMINAL]{RESET}")
        if paises_encontrados:
            for pais, ocorrencias in paises_encontrados.items():
                print(f"  {VERDE}•{RESET} {BRANCO}{pais}:{RESET} {CIANO}{len(ocorrencias)} ocorrência(s){RESET}")
        else:
            print(f"  {CINZA}Nenhuma referência explícita a países ou enclaves encontrada.{RESET}")

        print(f"\n{AMARELO}{NEGRITO}[RELATÓRIO COMPLETO + AVALIAÇÃO E ALINHAMENTO DO CONTRATO]{RESET}\n")
        print(conteudo_final)
        print(f"{VERDE}{NEGRITO}Arquivo completo salvo também em:{RESET} {CIANO}{destino}{RESET}\n")

    return destino


if __name__ == "__main__":
    gerar_relatorio_juridico(imprimir_no_terminal=True)