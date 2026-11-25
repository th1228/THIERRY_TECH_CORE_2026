# -*- coding: utf-8 -*-
"""Patch direcionado e seguro para auditor_global_mercado.py."""

from pathlib import Path
import py_compile
import sys

ALVO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("auditor_global_mercado.py")
if not ALVO.exists():
    for cand in sorted(Path(".").rglob("auditor_global_mercado.py")):
        ALVO = cand
        break

if not ALVO.exists():
    raise FileNotFoundError("Arquivo auditor_global_mercado.py não encontrado.")

MARCA = "# --- PATCH ENXUTO AUDITOR GLOBAL MERCADO ---"
codigo = ALVO.read_text(encoding="utf-8", errors="ignore")

if MARCA in codigo:
    print(f"Patch já aplicado em {ALVO}.")
    sys.exit(0)

# Remove linha inicial "Import logging" solta caso exista
if codigo.startswith("Import logging\r\n"):
    codigo = codigo.replace("Import logging\r\n\r\n", "", 1)
elif codigo.startswith("Import logging\n"):
    codigo = codigo.replace("Import logging\n\n", "", 1)

# Corrige o final truncado na chamada de _imprimir_bloco_final_telemedicina_e_selo e fecha o __main__
marcador_final = "        self._imprimir_bloco_final_telemedicina_e_selo("
idx_final = codigo.rfind(marcador_final)
if idx_final != -1:
    trecho_apos = codigo[idx_final:]
    if "assina" in trecho_apos or "dados_auditoria=dados_auditoria," in trecho_apos or "if __name__" not in trecho_apos:
        codigo = codigo[:idx_final] + """        self._imprimir_bloco_final_telemedicina_e_selo(
            tudo_ok=tudo_ok,
            selo_no=selo_no,
            assinatura_b64=assinatura_b64,
            timestamp_local=timestamp_local,
            dados_auditoria=dados_auditoria
        )


if __name__ == "__main__":
    raiz = os.getcwd()
    args = set(sys.argv[1:])
    aplicar = bool(args & {"--aplicar", "--corrigir"})
    exibir_caminho = bool(args & {"--mostrar-caminho", "--caminho"})
    auditor = AuditorGlobalMercado(raiz)
    auditor.executar_auditoria_completa(aplicar_correcoes=aplicar, mostrar_caminho=exibir_caminho)
"""

# Adiciona helper enxuto antes da classe AuditorGlobalMercado
helper_linhas = f"""{MARCA}
def _logar_linhas_formatadas(linhas: List[str], cor: str, indent: str = "  ") -> None:
    for linha in linhas:
        logger.info(f"{{indent}}{{cor}}{{linha}}{{RESET}}")
"""

if "class AuditorGlobalMercado:" in codigo:
    codigo = codigo.replace("class AuditorGlobalMercado:", helper_linhas + "\n\nclass AuditorGlobalMercado:", 1)

# Enxuga loops repetitivos de impressão de fatores
for var_nome, cor_nome, indent_str in [
    ("fatores_alto_padrao", "VERDE", "  "),
    ("fatores_telemed", "CIANO", "    "),
]:
    for item_var in ("linha_fator", "linha_tel"):
        bloco_antigo = f"""        for {item_var} in {var_nome}:
            logger.info(f"{indent_str}{{{cor_nome}}}{{{item_var}}}{{RESET}}")"""
        if bloco_antigo in codigo:
            codigo = codigo.replace(
                bloco_antigo,
                f"        _logar_linhas_formatadas({var_nome}, {cor_nome}, {indent_str!r})",
            )

backup = ALVO.with_suffix(ALVO.suffix + ".bak")
backup.write_text(ALVO.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")
ALVO.write_text(codigo, encoding="utf-8")

try:
    py_compile.compile(str(ALVO), doraise=True)
    print(f"[OK] Patch aplicado e compilado com sucesso em {ALVO} (backup: {backup}).")
except py_compile.PyCompileError as err:
    ALVO.write_text(backup.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")
    raise RuntimeError(f"Falha na compilação; backup restaurado: {err}") from err