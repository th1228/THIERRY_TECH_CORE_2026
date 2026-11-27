import hashlib
import inspect
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from core.tricologia_ultra_avancada import C2UltraAdvancedTrichologyEngine


def sha256_bytes(dados: bytes) -> str:
    return hashlib.sha256(dados).hexdigest()


def criar_amostra_real_capilar(caminho_npy: Path) -> np.ndarray:
    rng = np.random.default_rng(42)
    amostra = rng.integers(80, 190, size=(128, 128, 3), dtype=np.uint8)
    amostra[:, ::6, :] = np.clip(amostra[:, ::6, :].astype(int) - 40, 0, 255).astype(np.uint8)
    np.save(caminho_npy, amostra)
    return amostra


def main() -> None:
    saida_dir = Path("evidencias_p2p_tricologia_ultra")
    saida_dir.mkdir(exist_ok=True)

    amostra_path = saida_dir / "amostra_capilar_ultra_128x128.npy"
    amostra = criar_amostra_real_capilar(amostra_path)
    hash_entrada = sha256_bytes(amostra_path.read_bytes())

    motor = C2UltraAdvancedTrichologyEngine()
    sig_init = str(inspect.signature(C2UltraAdvancedTrichologyEngine.__init__))
    sig_telemetria = str(inspect.signature(motor.calcular_telemetria_capilar))
    sig_pdf = str(inspect.signature(motor.gerar_pdf_tricologia_avancada))

    resultado = None
    erro = None
    try:
        resultado = motor.calcular_telemetria_capilar()
    except Exception as exc:
        erro = f"{type(exc).__name__}: {exc}"

    payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "frente": "Tricologia Ultra Avancada",
        "motor": "core.tricologia_ultra_avancada.C2UltraAdvancedTrichologyEngine",
        "assinaturas": {
            "__init__": sig_init,
            "calcular_telemetria_capilar": sig_telemetria,
            "gerar_pdf_tricologia_avancada": sig_pdf,
        },
        "entrada": {
            "arquivo": str(amostra_path),
            "shape": list(amostra.shape),
            "dtype": str(amostra.dtype),
            "sha256": hash_entrada,
        },
        "execucao": {
            "erro": erro,
            "tipo_retorno": type(resultado).__name__,
            "saida_resumo": repr(resultado)[:1500],
        },
    }

    relatorio_path = saida_dir / "relatorio_p2p_tricologia_ultra.json"
    relatorio_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[OK] Relatório salvo em: {relatorio_path}")
    print(f"Assinatura __init__    : {sig_init}")
    print(f"Assinatura telemetria  : {sig_telemetria}")
    print(f"Assinatura gerar_pdf   : {sig_pdf}")
    if erro:
        print(f"[AVISO] Erro na chamada: {erro}")
    else:
        print(f"[OK] Retorno ({type(resultado).__name__}): {repr(resultado)[:400]}")


if __name__ == "__main__":
    main()