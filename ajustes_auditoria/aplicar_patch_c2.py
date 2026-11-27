# -*- coding: utf-8 -*-
"""Patch cirúrgico e idempotente para core/c2_sovereign_intelligence.py."""

from pathlib import Path
import sys

ALVO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("core/c2_sovereign_intelligence.py")
if not ALVO.exists():
    ALVO = Path("c2_sovereign_intelligence.py")

if not ALVO.exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {ALVO}")

codigo = ALVO.read_text(encoding="utf-8")

MARCA = "# --- PATCH C2 SOVEREIGN INTELLIGENCE v17.0.5 ---"
if MARCA in codigo:
    print(f"Patch já aplicado em {ALVO}.")
    sys.exit(0)

# 1. Garante imports necessários
if "import tempfile" not in codigo:
    codigo = codigo.replace("import json\n", "import json\nimport uuid\nimport tempfile\n", 1)

# 2. Torna MemoriaMock transparente e adiciona helper numérico + alias SovereignC2DefenseEngine
bloco_topo_extra = f"""
{MARCA}
def _extrair_float_c2(valor, padrao):
    if valor is None:
        return padrao
    if isinstance(valor, (int, float)):
        return float(valor)
    txt = str(valor).strip()
    if not txt:
        return padrao
    buf = []
    dot = False
    sign = False
    for ch in txt:
        if ch in "+-" and not buf and not sign:
            buf.append(ch)
            sign = True
        elif ch.isdigit():
            buf.append(ch)
        elif ch in ".," and not dot:
            buf.append(".")
            dot = True
        elif buf:
            break
    try:
        return float("".join(buf)) if buf else padrao
    except ValueError:
        return padrao
"""

codigo = codigo.replace(
    "class C2SovereignSecurityCore:",
    bloco_topo_extra + "\n\nclass C2SovereignSecurityCore:",
    1,
)

# 3. Gráfico temporário único via tempfile + limpeza garantida no finally
antigo_grafico = '        caminho_grafico_temp = "chart_temp.png"\n        self._gerar_grafico_erosao(dados_motor["projecao_temporal"], caminho_grafico_temp)'
novo_grafico = """        fd_g, caminho_grafico_temp = tempfile.mkstemp(
            prefix=f"c2_chart_{uuid.uuid4().hex[:8]}_",
            suffix=".png"
        )
        import os as _os_patch
        _os_patch.close(fd_g)
        self._gerar_grafico_erosao(dados_motor["projecao_temporal"], caminho_grafico_temp)"""

if antigo_grafico in codigo:
    codigo = codigo.replace(antigo_grafico, novo_grafico, 1)

# 4. Datas fixas antigas (14/10/2026 / 24/10/2026) -> dinâmicas com base na execução atual
codigo = codigo.replace('"24/10/2026"', '(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=10)).strftime("%d/%m/%Y")')
codigo = codigo.replace('"14/10/2026"', 'datetime.datetime.now(datetime.timezone.utc).strftime("%d/%m/%Y")')

# 5. Alias de compatibilidade caso o orquestrador importe SovereignC2DefenseEngine daqui
if "SovereignC2DefenseEngine =" not in codigo:
    codigo = codigo.rstrip() + "\n\nSovereignC2DefenseEngine = C2SovereignIntelligenceEngine\n"

backup = ALVO.with_suffix(ALVO.suffix + ".bak")
backup.write_text(ALVO.read_text(encoding="utf-8"), encoding="utf-8")
ALVO.write_text(codigo, encoding="utf-8")
print(f"Patch aplicado com sucesso em {ALVO}. Backup salvo em {backup}.")