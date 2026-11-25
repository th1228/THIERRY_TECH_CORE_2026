# -*- coding: utf-8 -*-
"""Verificação rápida de saúde dos módulos principais e PDFs gerados."""

import importlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

modulos = [
    "main",
    "core.c2_sovereign_intelligence",
    "core.tricologia_ultra_avancada",
]

print("=== 1. TESTE DE IMPORTAÇÃO ===")
for nome in modulos:
    try:
        importlib.import_module(nome)
        print(f"[OK] {nome} importado sem erro.")
    except Exception as exc:
        print(f"[FALHA] {nome}: {type(exc).__name__}: {exc}")

print("\n=== 2. TESTE RÁPIDO DO MOTOR DE TRICOLOGIA ===")
try:
    from core.tricologia_ultra_avancada import C2UltraAdvancedTrichologyEngine

    pdfs_dir = ROOT / "pdfs_finais"
    pdfs_dir.mkdir(exist_ok=True)
    saida = pdfs_dir / "check_rapido_tricologia.pdf"

    motor = C2UltraAdvancedTrichologyEngine(
        ceo_name="Genilson Rodrigues",
        market_segment="Tecnologia",
        net_worth_eur=4500000.0,
        lang="PT",
    )
    caminho = motor.gerar_pdf_tricologia_avancada(str(saida))
    tamanho = Path(caminho).stat().st_size
    print(f"[OK] PDF gerado: {caminho} ({tamanho} bytes)")
except Exception as exc:
    print(f"[FALHA] Teste do motor de tricologia: {type(exc).__name__}: {exc}")

print("\n=== 3. ARQUIVOS EM pdfs_finais ===")
pdfs_dir = ROOT / "pdfs_finais"
if pdfs_dir.exists():
    arquivos = sorted(pdfs_dir.glob("*.pdf"))
    for arq in arquivos:
        print(f" - {arq.name}: {arq.stat().st_size} bytes")
else:
    print("[AVISO] Pasta pdfs_finais ainda não existe.")