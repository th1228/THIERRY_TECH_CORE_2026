from datetime import datetime
import json
from pathlib import Path
import re
import sys

TERMOS_EXAGERADOS = [
    r"military-grade",
    r"10 famílias",
    r"r\$\s*1[.,]5\s*bi",
    r"vida artificial",
    r"reescreve o próprio código",
    r"imune ao tempo",
    r"supercomputador de bolso",
    r"biologia digital",
    r"darwinismo de código",
    r"garantia matemática",
]

TERMOS_RECOMENDADOS = [
    "5, 10 e 15 anos",
    "privacidade",
    "local",
    "auditoria",
    "integridade",
    "inpi",
    "lgpd",
]


def auditar_markdown(caminho_arquivo: str) -> dict:
    arquivo = Path(caminho_arquivo)
    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    conteudo = arquivo.read_text(encoding="utf-8")
    linhas = conteudo.splitlines()
    alertas = []

    for indice, linha in enumerate(linhas, start=1):
        for padrao in TERMOS_EXAGERADOS:
            if re.search(padrao, linha, flags=re.IGNORECASE):
                alertas.append({
                    "linha": indice,
                    "padrao": padrao,
                    "trecho": linha.strip(),
                })

    conteudo_lower = conteudo.lower()
    pilares_presentes = [
        termo for termo in TERMOS_RECOMENDADOS if termo in conteudo_lower
    ]
    pilares_ausentes = [
        termo for termo in TERMOS_RECOMENDADOS if termo not in conteudo_lower
    ]

    return {
        "arquivo": str(arquivo),
        "auditoria_em": datetime.now().isoformat(timespec="seconds"),
        "total_linhas": len(linhas),
        "total_alertas": len(alertas),
        "alertas": alertas,
        "pilares_presentes": pilares_presentes,
        "pilares_ausentes": pilares_ausentes,
    }


def gerar_relatorio(resultado: dict) -> str:
    linhas_saida = [
        "=" * 60,
        "AUDITOR DE DOCUMENTAÇÃO MIBO",
        "=" * 60,
        f"Arquivo:           {resultado['arquivo']}",
        f"Data/Hora:         {resultado['auditoria_em']}",
        f"Total de linhas:   {resultado['total_linhas']}",
        f"Alertas de hype:   {resultado['total_alertas']}",
        "",
        "--- ALERTAS ENCONTRADOS ---",
    ]

    if not resultado["alertas"]:
        linhas_saida.append("Nenhum termo exagerado encontrado.")
    else:
        for item in resultado["alertas"]:
            linhas_saida.append(
                f" [Linha {item['linha']}] Padrão '{item['padrao']}': {item['trecho']}"
            )

    linhas_saida.extend([
        "",
        "--- PILARES TÉCNICOS / GOVERNANÇA ---",
        "Presentes: "
        + (
            ", ".join(resultado["pilares_presentes"])
            if resultado["pilares_presentes"]
            else "Nenhum"
        ),
        "Ausentes:  "
        + (
            ", ".join(resultado["pilares_ausentes"])
            if resultado["pilares_ausentes"]
            else "Nenhum"
        ),
        "=" * 60,
    ])

    return "\n".join(linhas_saida)


def salvar_json(resultado: dict, caminho_saida: str) -> Path:
    destino = Path(caminho_saida)
    destino.write_text(
        json.dumps(resultado, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return destino


if __name__ == "__main__":
    alvo = sys.argv[1] if len(sys.argv) > 1 else "mibo_dna_checklist.md"
    salvar_relatorio_json = "--json" in sys.argv

    try:
        dados = auditar_markdown(alvo)
        print(gerar_relatorio(dados))

        if salvar_relatorio_json:
            nome_json = f"{Path(alvo).stem}_auditoria.json"
            arquivo_json = salvar_json(dados, nome_json)
            print(f"\nRelatório JSON salvo em: {arquivo_json}")

    except FileNotFoundError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        sys.exit(1)