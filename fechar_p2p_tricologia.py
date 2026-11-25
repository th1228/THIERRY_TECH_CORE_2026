import hashlib
import inspect
import json
from datetime import datetime, timezone
from pathlib import Path

from core.tricologia_ultra_avancada import C2UltraAdvancedTrichologyEngine


def sha256_arquivo(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def rodar_cenario(nome: str, kwargs_init: dict, pasta_saida: Path) -> dict:
    motor = C2UltraAdvancedTrichologyEngine(**kwargs_init)
    telemetria = motor.calcular_telemetria_capilar()

    pdf_path = pasta_saida / f"dossier_tricologia_{nome}.pdf"
    pdf_erro = None
    try:
        sig_pdf = inspect.signature(motor.gerar_pdf_tricologia_avancada)
        params = list(sig_pdf.parameters.keys())
        if params:
            motor.gerar_pdf_tricologia_avancada(**{params[0]: str(pdf_path)})
        else:
            motor.gerar_pdf_tricologia_avancada()
    except Exception as exc:
        pdf_erro = f"{type(exc).__name__}: {exc}"

    evidencia_pdf = None
    if pdf_path.exists():
        evidencia_pdf = {
            "arquivo": str(pdf_path),
            "tamanho_bytes": pdf_path.stat().st_size,
            "sha256": sha256_arquivo(pdf_path),
        }

    return {
        "cenario": nome,
        "parametros_init": kwargs_init,
        "telemetria": telemetria,
        "pdf": evidencia_pdf,
        "pdf_erro": pdf_erro,
    }


def main() -> None:
    pasta = Path("evidencias_p2p_tricologia_ultra")
    pasta.mkdir(exist_ok=True)

    cenarios = [
        rodar_cenario(
            "cenario_base",
            {"miniaturizacao_pct": 10.0, "umidade_ar_pct": 50.0, "temp_externa_c": 26.0},
            pasta,
        ),
        rodar_cenario(
            "cenario_critico",
            {"miniaturizacao_pct": 35.0, "umidade_ar_pct": 88.0, "temp_externa_c": 34.0},
            pasta,
        ),
    ]

    relatorio = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "motor": "core.tricologia_ultra_avancada.C2UltraAdvancedTrichologyEngine",
        "cenarios": cenarios,
    }

    out_json = pasta / "fechamento_tricologia.json"
    out_json.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Fechamento salvo em: {out_json}")
    for c in cenarios:
        t = c["telemetria"]
        print(
            f"- {c['cenario']}: miniaturizacao={t.get('taxa_miniaturizacao')} | "
            f"fluxo={t.get('fluxo_q')} | pdf={c['pdf']['arquivo'] if c['pdf'] else c['pdf_erro']}"
        )


if __name__ == "__main__":
    main()