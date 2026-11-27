import os
import re
from pathlib import Path

# Códigos de cores ANSI para o terminal
VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
AZUL = "\033[94m"
RESET = "\033[0m"

# Configurações da auditoria
DIRETORIO_PROJETO = "."
EXTENSOES_ALVO = {".html", ".css", ".js", ".jsx", ".ts", ".tsx", ".py", ".vue"}
PASTAS_IGNORADAS = {"node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build"}

REGRAS = {
    "1.1_css_zindex_alto": {
        "descricao": "Possível conflito de sobreposição (z-index >= 100) na interface",
        "padrao": re.compile(r"z-index\s*:\s*([1-9]\d{2,})", re.IGNORECASE),
        "tipo": "alerta",
        "extensoes_validas": {".html", ".css", ".vue", ".jsx", ".tsx"}
    },
    "1.2_vazamento_terminal": {
        "descricao": "Comandos de terminal ou processos vazados no Front-end",
        "padrao": re.compile(r"(powershell|subprocess|traceback|cmd\.exe|shell=True)", re.IGNORECASE),
        "tipo": "alerta",
        "extensoes_validas": {".html", ".css", ".vue", ".jsx", ".tsx", ".js", ".ts"}
    },
    "2.1_dados_valuation": {
        "descricao": "Métricas comerciais/valuation encontradas na interface do cliente",
        "padrao": re.compile(r"(valuation|faturamento|apex capital|equity|mrr|arr|pitch deck)", re.IGNORECASE),
        "tipo": "alerta",
        "extensoes_validas": {".html", ".vue", ".jsx", ".tsx", ".js", ".ts"}
    },
    "2.2_disclaimer_legal": {
        "descricao": "Presença de disclaimer de suporte à decisão (estética/tricologia/visagismo)",
        "padrao": re.compile(r"(suporte à decisão|decision support|isenção de responsabilidade|disclaimer|tricologia|visagismo)", re.IGNORECASE),
        "tipo": "obrigatorio",
        "extensoes_validas": {".html", ".py", ".vue", ".jsx", ".tsx", ".js", ".ts"}
    },
    "3.1_internacionalizacao_pdf": {
        "descricao": "Suporte a idiomas (PT/EN) e estrutura de PDF",
        "padrao": re.compile(r"(pt-br|en-us|i18n|translate|jspdf|reportlab|pdfkit|html2pdf)", re.IGNORECASE),
        "tipo": "obrigatorio",
        "extensoes_validas": {".html", ".py", ".vue", ".jsx", ".tsx", ".js", ".ts"}
    }
}

def executar_auditoria():
    resultados = {chave: [] for chave in REGRAS}
    arquivos_analisados = 0

    for raiz, pastas, arquivos in os.walk(DIRETORIO_PROJETO):
        pastas[:] = [p for p in pastas if p not in PASTAS_IGNORADAS]

        for arquivo in arquivos:
            # Ignora scripts de auditoria para evitar autoinfluência nos resultados
            if "auditoria" in arquivo.lower() or "auditor" in arquivo.lower():
                continue
                
            caminho = Path(raiz) / arquivo
            extensao = caminho.suffix.lower()
            
            if extensao not in EXTENSOES_ALVO:
                continue

            arquivos_analisados += 1
            try:
                conteudo = caminho.read_text(encoding="utf-8", errors="ignore")
                linhas = conteudo.splitlines()

                for num_linha, texto_linha in enumerate(linhas, start=1):
                    for chave, regra in REGRAS.items():
                        # Valida se o tipo de arquivo deve ser auditado por esta regra específica
                        if extensao not in regra["extensoes_validas"]:
                            continue
                            
                        if regra["padrao"].search(texto_linha):
                            resultados[chave].append(f"  - {caminho} (Linha {num_linha}): {texto_linha.strip()[:80]}")
            except Exception as e:
                print(f"{VERMELHO}Erro ao ler {caminho}: {e}{RESET}")

    print(f"\n{AZUL}" + "=" * 65 + f"{RESET}")
    print(f"{AZUL}RELATÓRIO DE AUDITORIA TÉCNICA - MIBO ({arquivos_analisados} arquivos lidos){RESET}")
    print(f"{AZUL}" + "=" * 65 + f"{RESET}")

    for chave, regra in REGRAS.items():
        ocorrencias = resultados[chave]
        print(f"\n{AMARELO}[{regra['descricao']}]{RESET}")

        if regra["tipo"] == "alerta":
            if ocorrencias:
                print(f"  {VERMELHO}STATUS: PENDENTE ({len(ocorrencias)} ocorrência(s) para revisar/remover){RESET}")
                for item in ocorrencias[:10]:
                    print(f"  {VERMELHO}{item}{RESET}")
                if len(ocorrencias) > 10:
                    print(f"  {VERMELHO}... e mais {len(ocorrencias) - 10} ocorrências.{RESET}")
            else:
                print(f"  {VERDE}STATUS: OK (Nenhuma ocorrência indevida encontrada){RESET}")

        elif regra["tipo"] == "obrigatorio":
            if ocorrencias:
                print(f"  {VERDE}STATUS: OK ({len(ocorrencias)} referência(s) encontrada(s)){RESET}")
                for item in ocorrencias[:5]:
                    print(f"  {VERDE}{item}{RESET}")
            else:
                print(f"  {VERMELHO}STATUS: FALTANDO (Nenhuma implementação detectada no projeto){RESET}")

    print(f"\n{AZUL}" + "=" * 65 + f"{RESET}\n")

if __name__ == "__main__":
    executar_auditoria()